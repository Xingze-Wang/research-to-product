<p align="center">
  <img src="assets/logo.png" alt="MiraclePlus" width="120" />
</p>

<h1 align="center">research-to-product</h1>

<p align="center">
  <strong>Your paper got accepted. Now ship it.</strong>
</p>

<p align="center">
  Production-grade templates for turning research code into real products.<br/>
  Built by <a href="https://www.miracleplus.com">MiraclePlus (奇绩创坛)</a> — YC's partner in China.
</p>

<p align="center">
  <a href="#quickstart">Quickstart</a> •
  <a href="#templates">Templates</a> •
  <a href="#guides">Guides</a> •
  <a href="#contribute">Contribute</a>
</p>

---

## The Problem

You published at NeurIPS. Your demo runs on a single A100. Your `train.py` has 47 hardcoded paths.

Now a customer wants to try it. An investor asks for a live demo. A co-founder candidate wants to see "the product."

**The gap between a research prototype and a shippable product is ~6 months of engineering work that no paper teaches you.** We've watched hundreds of researcher-founders hit the same walls. This repo exists to eliminate the most common ones.

## Quickstart

**Turn your model into an API in 3 minutes:**

```bash
git clone https://github.com/nichole-liu/research-to-product.git
cp -r templates/paper-to-api my-project
cd my-project && make serve
```

**Go from training script to production deployment:**

```bash
cp -r templates/train-to-deploy my-project
# Edit config.yaml with your model details
make train    # distributed training with fault tolerance
make export   # ONNX/TensorRT export
make deploy   # containerized deployment with autoscaling
```

That's it. No 200-page docs. No "enterprise architecture." Just code that works.

## Templates

### [`paper-to-api/`](templates/paper-to-api/)

The fastest path from "my model works in a notebook" to "here's an API endpoint."

| What you get | Why it matters |
|---|---|
| FastAPI server with automatic OpenAPI docs | Investors and customers can try your model in 30 seconds |
| Docker + docker-compose | "Works on my machine" → works everywhere |
| GPU inference with batching | 10x throughput without changing your model code |
| Health checks + structured logging | You'll need these the first time your demo crashes at 2am |
| Load testing script | Know your limits before your users find them |

### [`train-to-deploy/`](templates/train-to-deploy/)

Production training pipeline that scales from 1 GPU to a cluster.

| What you get | Why it matters |
|---|---|
| Distributed training (DDP/FSDP) config | Stop rewriting your training loop for every new machine |
| Experiment tracking (W&B / MLflow) | Reproduce any result from 3 months ago |
| Model export (ONNX, TensorRT, vLLM) | 5x inference speedup for free |
| K8s deployment manifests | From `python inference.py` to autoscaling service |
| Cost calculator | Know your burn rate per 1M API calls before you price |

## Guides

Hard-won lessons from 500+ researcher-founders. No fluff.

- **[`open-source-trap.md`](guides/open-source-trap.md)** — GPL vs Apache vs BSL: How your license choice on Day 1 determines your exit options on Day 1000. Most researchers get this catastrophically wrong.

- **[`equity-for-scientists.md`](guides/equity-for-scientists.md)** — Your professor wants 30% for "the IP." Your co-founder wants 50% because they "handle business." Here's the framework that actually works.

- **[`compute-economics.md`](guides/compute-economics.md)** — The real cost of GPU compute in China vs. US. Cloud vs. co-lo vs. owned. When to optimize inference and when to just throw money at it.

## What This Repo Is NOT

- **Not a course.** We don't explain transformers. You know more about your model than we ever will.
- **Not a framework.** No vendor lock-in. Eject anytime.
- **Not marketing.** There's no sales funnel here. If you want to talk to us, [you will](https://www.miracleplus.com/apply).

## Contribute

We accept PRs, not pitch decks.

If you've solved a hard engineering problem that other researcher-founders face, open a PR. **High-quality contributions get a fast-track interview at MiraclePlus.** Not because we're doing you a favor — because the kind of person who writes production-grade open source is exactly who we want to back.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for details.

## The Reverse Pitch

Every week, we pick a recent paper and break down: *What would it take to turn this into a product?*

- Technical feasibility
- Engineering hard parts
- Market size and timing
- Ideal founding team

**Join the discussion** in [GitHub Discussions →](../../discussions)

We're not here to judge your research. We're here to help you figure out if it's a business — and if so, how to build it fast.

---

<p align="center">
  <sub>Built by engineers at <a href="https://www.miracleplus.com">MiraclePlus</a>. We back technical founders.</sub><br/>
  <sub>If you're turning research into product, <a href="https://www.miracleplus.com/apply">talk to us</a>.</sub>
</p>
