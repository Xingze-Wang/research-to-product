"""
Training loop with distributed training support (DDP/FSDP).
Handles: mixed precision, gradient accumulation, checkpointing, logging.

You edit model.py and dataset.py. This file does the rest.
"""

import os
import argparse
import yaml
import time
from pathlib import Path

import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler
from torch.cuda.amp import GradScaler, autocast

from src.model import build_model
from src.dataset import build_dataset


def setup_distributed():
    """Initialize distributed training if launched with torchrun."""
    if "RANK" in os.environ:
        dist.init_process_group("nccl")
        rank = int(os.environ["RANK"])
        local_rank = int(os.environ["LOCAL_RANK"])
        world_size = int(os.environ["WORLD_SIZE"])
        torch.cuda.set_device(local_rank)
        return rank, local_rank, world_size
    return 0, 0, 1


def cleanup_distributed():
    if dist.is_initialized():
        dist.destroy_process_group()


def log_print(rank, msg):
    """Only print from rank 0."""
    if rank == 0:
        print(msg)


def train(config_path: str, resume: bool = False):
    rank, local_rank, world_size = setup_distributed()
    device = torch.device(f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu")

    with open(config_path) as f:
        config = yaml.safe_load(f)

    tc = config["training"]
    torch.manual_seed(config.get("seed", 42))

    # --- Model ---
    model = build_model(config["model"]).to(device)
    if world_size > 1:
        model = DDP(model, device_ids=[local_rank])
    log_print(rank, f"Model params: {sum(p.numel() for p in model.parameters()):,}")

    # --- Data ---
    train_dataset = build_dataset(config["data"], split="train")
    val_dataset = build_dataset(config["data"], split="val")

    train_sampler = DistributedSampler(train_dataset) if world_size > 1 else None
    train_loader = DataLoader(
        train_dataset,
        batch_size=tc["batch_size"],
        sampler=train_sampler,
        shuffle=(train_sampler is None),
        num_workers=config["data"].get("num_workers", 4),
        pin_memory=True,
        drop_last=True,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=tc["batch_size"],
        num_workers=config["data"].get("num_workers", 4),
        pin_memory=True,
    )

    # --- Optimizer ---
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=tc["lr"], weight_decay=tc["weight_decay"]
    )

    # --- Mixed Precision ---
    use_amp = tc.get("mixed_precision", "no") != "no"
    dtype = torch.bfloat16 if tc.get("mixed_precision") == "bf16" else torch.float16
    scaler = GradScaler(enabled=(use_amp and dtype == torch.float16))

    # --- Training Loop ---
    save_dir = Path(config["checkpointing"]["save_dir"])
    save_dir.mkdir(parents=True, exist_ok=True)
    grad_accum = tc.get("gradient_accumulation_steps", 1)
    best_val_loss = float("inf")

    for epoch in range(tc["epochs"]):
        model.train()
        if train_sampler:
            train_sampler.set_epoch(epoch)

        epoch_loss = 0.0
        start_time = time.time()

        for step, batch in enumerate(train_loader):
            # Move batch to device (customize if your batch structure differs)
            batch = {k: v.to(device) if torch.is_tensor(v) else v for k, v in batch.items()}

            with autocast(device_type="cuda", dtype=dtype, enabled=use_amp):
                loss = model(**batch) if isinstance(batch, dict) else model(batch)
                loss = loss / grad_accum

            scaler.scale(loss).backward()

            if (step + 1) % grad_accum == 0:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), tc.get("max_grad_norm", 1.0))
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()

            epoch_loss += loss.item() * grad_accum

        # --- Validation ---
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for batch in val_loader:
                batch = {k: v.to(device) if torch.is_tensor(v) else v for k, v in batch.items()}
                with autocast(device_type="cuda", dtype=dtype, enabled=use_amp):
                    loss = model(**batch) if isinstance(batch, dict) else model(batch)
                val_loss += loss.item()

        avg_train = epoch_loss / len(train_loader)
        avg_val = val_loss / max(len(val_loader), 1)
        elapsed = time.time() - start_time

        log_print(rank, f"Epoch {epoch+1}/{tc['epochs']} | "
                       f"Train: {avg_train:.4f} | Val: {avg_val:.4f} | "
                       f"Time: {elapsed:.1f}s")

        # --- Checkpointing ---
        if rank == 0:
            save_every = config["checkpointing"].get("save_every_n_epochs", 5)
            if (epoch + 1) % save_every == 0 or avg_val < best_val_loss:
                ckpt_path = save_dir / f"epoch_{epoch+1}.pt"
                torch.save({
                    "epoch": epoch + 1,
                    "model_state_dict": model.module.state_dict() if world_size > 1 else model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "val_loss": avg_val,
                }, ckpt_path)
                log_print(rank, f"Saved checkpoint: {ckpt_path}")

                if avg_val < best_val_loss:
                    best_val_loss = avg_val
                    best_path = save_dir / "best.pt"
                    torch.save(torch.load(ckpt_path), best_path)

    cleanup_distributed()
    log_print(rank, f"Training complete. Best val loss: {best_val_loss:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    train(args.config, args.resume)
