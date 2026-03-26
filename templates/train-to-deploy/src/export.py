"""
Export trained model to optimized inference formats.
ONNX → TensorRT → ready for production.
"""

import argparse
import yaml
from pathlib import Path

import torch

from src.model import build_model


def export_onnx(model, config, output_dir: Path):
    """Export to ONNX format."""
    output_path = output_dir / "model.onnx"
    # Customize dummy input to match your model
    dummy_input = torch.randn(1, 768).to(next(model.parameters()).device)

    torch.onnx.export(
        model,
        dummy_input,
        str(output_path),
        opset_version=17,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={
            "input": {0: "batch_size"},
            "output": {0: "batch_size"},
        },
    )
    print(f"ONNX exported: {output_path}")
    return output_path


def export_torchscript(model, config, output_dir: Path):
    """Export to TorchScript for C++ deployment."""
    output_path = output_dir / "model.pt"
    dummy_input = torch.randn(1, 768).to(next(model.parameters()).device)
    traced = torch.jit.trace(model, dummy_input)
    traced.save(str(output_path))
    print(f"TorchScript exported: {output_path}")
    return output_path


def optimize_tensorrt(onnx_path: Path, output_dir: Path):
    """Convert ONNX to TensorRT (requires tensorrt installed)."""
    try:
        import tensorrt as trt

        output_path = output_dir / "model.trt"
        logger = trt.Logger(trt.Logger.WARNING)
        builder = trt.Builder(logger)
        network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
        parser = trt.OnnxParser(network, logger)

        with open(onnx_path, "rb") as f:
            if not parser.parse(f.read()):
                for i in range(parser.num_errors):
                    print(f"TRT parse error: {parser.get_error(i)}")
                return None

        config = builder.create_builder_config()
        config.set_flag(trt.BuilderFlag.FP16)
        config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 30)

        engine = builder.build_serialized_network(network, config)
        with open(output_path, "wb") as f:
            f.write(engine)

        print(f"TensorRT exported: {output_path}")
        return output_path
    except ImportError:
        print("TensorRT not installed. Skipping. Install: pip install tensorrt")
        return None


def main(config_path: str):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    output_dir = Path(config.get("output_dir", "outputs/exported"))
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load best checkpoint
    checkpoint_path = config.get("checkpoint", "outputs/checkpoints/best.pt")
    model_config = config.get("model", {})
    model = build_model(model_config)

    ckpt = torch.load(checkpoint_path, map_location="cpu")
    model.load_state_dict(ckpt.get("model_state_dict", ckpt))
    model.eval()
    print(f"Loaded checkpoint: {checkpoint_path}")

    # Export formats
    formats = config.get("formats", ["onnx"])
    onnx_path = None

    if "onnx" in formats:
        onnx_path = export_onnx(model, config, output_dir)

    if "torchscript" in formats:
        export_torchscript(model, config, output_dir)

    if "tensorrt" in formats and onnx_path:
        optimize_tensorrt(onnx_path, output_dir)

    print(f"\nAll exports saved to {output_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/export.yaml")
    args = parser.parse_args()
    main(args.config)
