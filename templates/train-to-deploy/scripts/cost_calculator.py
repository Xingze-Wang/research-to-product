"""
Know your burn rate before you price.

Estimates the cost per 1M API calls based on your GPU,
inference latency, and cloud pricing.
"""

import argparse

# GPU hourly rates (USD) — update as needed
GPU_PRICES = {
    # --- US Cloud (on-demand) ---
    "A100-80GB (AWS)": 4.10,
    "A100-80GB (GCP)": 3.67,
    "H100 (AWS)": 12.00,
    "H100 (Lambda)": 2.49,
    # --- China Cloud ---
    "A100-80GB (Alibaba Cloud)": 3.20,  # ~23 RMB/h
    "A100-80GB (Tencent Cloud)": 3.50,  # ~25 RMB/h
    "A800 (China domestic)": 2.80,      # ~20 RMB/h
    # --- Co-location (amortized) ---
    "A100 co-lo (US, amortized)": 1.20,
    "A100 co-lo (CN, amortized)": 0.90,
}


def calculate_cost(
    latency_ms: float,
    batch_size: int,
    gpu: str,
    utilization: float = 0.7,
):
    """Calculate cost per 1M requests."""
    if gpu not in GPU_PRICES:
        print(f"Unknown GPU: {gpu}. Available:")
        for k in GPU_PRICES:
            print(f"  - {k}")
        return

    hourly_rate = GPU_PRICES[gpu]
    requests_per_second = (1000 / latency_ms) * batch_size * utilization
    requests_per_hour = requests_per_second * 3600
    cost_per_request = hourly_rate / requests_per_hour
    cost_per_million = cost_per_request * 1_000_000

    print(f"=== Cost Estimate ===")
    print(f"  GPU:              {gpu}")
    print(f"  Hourly rate:      ${hourly_rate:.2f}/h")
    print(f"  Latency:          {latency_ms}ms")
    print(f"  Batch size:       {batch_size}")
    print(f"  Utilization:      {utilization*100:.0f}%")
    print(f"  ---")
    print(f"  Throughput:       {requests_per_second:.1f} req/s")
    print(f"  Cost per 1M req:  ${cost_per_million:.2f}")
    print(f"  Monthly (10M/day): ${cost_per_million * 10 * 30:.0f}")
    print()

    return cost_per_million


def main():
    parser = argparse.ArgumentParser(description="Estimate inference cost")
    parser.add_argument("--latency", type=float, default=50, help="Inference latency in ms")
    parser.add_argument("--batch", type=int, default=1, help="Batch size")
    parser.add_argument("--gpu", type=str, default=None, help="GPU type")
    parser.add_argument("--utilization", type=float, default=0.7, help="GPU utilization (0-1)")
    args = parser.parse_args()

    print(f"\n{'='*50}")
    print(f"Inference Cost Calculator")
    print(f"{'='*50}\n")

    if args.gpu:
        calculate_cost(args.latency, args.batch, args.gpu, args.utilization)
    else:
        # Compare all GPUs
        for gpu in GPU_PRICES:
            calculate_cost(args.latency, args.batch, gpu, args.utilization)


if __name__ == "__main__":
    main()
