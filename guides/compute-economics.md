# Compute Economics

**The real cost of GPU compute. Cloud vs. Co-lo vs. Owned. China vs. US.**

## Why This Matters

Compute is likely your #1 cost. Most researcher-founders have no idea how much they're actually spending (or will spend) per inference call. This guide gives you the numbers.

## The Quick Math

```
Cost per request = (GPU hourly rate) / (requests per hour)
Requests per hour = (1000 / latency_ms) × batch_size × utilization × 3600
```

**Use `scripts/cost_calculator.py` in the train-to-deploy template** to run this for your specific model.

## GPU Pricing Landscape (2024-2025)

### US Cloud (On-Demand)

| GPU | AWS ($/h) | GCP ($/h) | Lambda ($/h) | Together.ai ($/h) |
|---|---|---|---|---|
| A100 80GB | 4.10 | 3.67 | 1.10 | ~1.00 |
| H100 80GB | 12.00 | 11.50 | 2.49 | ~2.00 |
| L40S | 1.80 | 1.70 | — | — |

### China Cloud

| GPU | Alibaba Cloud ($/h) | Tencent Cloud ($/h) | Huawei Cloud ($/h) |
|---|---|---|---|
| A100 80GB | ~3.20 (23 RMB) | ~3.50 (25 RMB) | — |
| A800 80GB | ~2.80 (20 RMB) | ~3.00 (21 RMB) | — |
| Ascend 910B | — | — | ~2.50 (18 RMB) |

*Note: China GPU prices fluctuate significantly due to supply constraints and export controls. Check current rates.*

### Reserved / Spot Instances

Spot instances are 60-80% cheaper but can be interrupted. Good for training, bad for serving.

| Type | Discount vs On-Demand | Use Case |
|---|---|---|
| On-demand | Baseline | Production serving |
| 1-year reserved | 30-40% off | Steady-state serving |
| 3-year reserved | 50-60% off | If you're sure about volume |
| Spot/Preemptible | 60-80% off | Training, batch jobs |

### Co-location (Amortized)

If you're burning >$50K/month on cloud GPUs, co-lo starts making sense.

| Setup | Amortized $/h per A100 | Break-even vs Cloud |
|---|---|---|
| US co-lo (Equinix, CoreWeave) | ~1.20 | ~8 months |
| China co-lo (domestic IDC) | ~0.90 | ~6 months |
| Own hardware (depreciated over 3yr) | ~0.60 | ~12 months upfront |

## Decision Framework

### Stage 1: Pre-Product (0-6 months)
**Use cloud. Period.**

Don't buy hardware. Don't co-locate. You don't even know if your product works yet. Use Lambda, Together.ai, or Alibaba Cloud spot instances for training. Use a single reserved instance for your demo API.

Monthly budget: $1K-5K

### Stage 2: Early Customers (6-18 months)
**Reserve instances for serving. Spot for training.**

You have paying customers (or serious pilots). Your inference load is predictable enough to reserve. Still use cloud — but start tracking your cost-per-request religiously.

Monthly budget: $5K-30K

### Stage 3: Scaling (18+ months)
**Evaluate co-lo. Optimize inference.**

You're spending $30K+/month on compute. Time to:
1. Profile your model. Where is latency coming from?
2. Export to TensorRT/vLLM. Free 2-5x speedup.
3. Get co-lo quotes. Compare 1-year TCO vs cloud.
4. Consider Triton Inference Server for batching.

Monthly budget: $30K-200K+

## Optimization Checklist

Before spending more on GPUs, have you:

- [ ] **Quantized your model?** INT8 quantization often gives 2x speedup with <1% accuracy loss
- [ ] **Enabled dynamic batching?** Most serving frameworks support this out of the box
- [ ] **Exported to ONNX/TensorRT?** 2-5x speedup over vanilla PyTorch
- [ ] **Used vLLM for LLM serving?** PagedAttention = 2-4x throughput improvement
- [ ] **Profiled your pipeline?** Is the bottleneck actually GPU, or is it preprocessing/postprocessing?
- [ ] **Right-sized your GPU?** An L40S at $1.80/h might handle your workload as well as an A100 at $4/h
- [ ] **Enabled flash attention?** Easy 2x memory reduction for transformer models

## The China Factor

A few things specific to the Chinese compute landscape:

1. **A800 vs A100:** The A800 (export-compliant version) has lower interconnect bandwidth. For single-GPU inference, performance is nearly identical. For multi-GPU training, expect 10-20% slower communication.

2. **Domestic alternatives are improving:** Huawei Ascend 910B, Cambricon MLU370 — still behind NVIDIA but getting better. Government contracts increasingly require domestic chips.

3. **GPU supply is volatile.** Export controls mean supply can shift overnight. Don't sign 3-year contracts based on today's availability.

4. **Bandwidth costs matter:** If you're serving from China to global users, factor in cross-border bandwidth. A CDN won't help with real-time inference.

## The One Number to Know

**Calculate your cost per 1M requests.** If you can't answer this question in 5 seconds, you're not ready to price your product. Run the calculator:

```bash
python scripts/cost_calculator.py --latency 50 --batch 8 --gpu "A100-80GB (AWS)"
```
