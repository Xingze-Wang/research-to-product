"""
Quick load test for your API.
Know your limits before your users find them.

Usage:
    python scripts/bench.py --users 50 --duration 60 --host http://localhost:8000
"""

import argparse
import asyncio
import time
import statistics
import json

import httpx


async def send_request(client: httpx.AsyncClient, url: str, payload: dict) -> float:
    """Send a single request, return latency in ms."""
    start = time.time()
    try:
        resp = await client.post(url, json=payload, timeout=30.0)
        latency = (time.time() - start) * 1000
        return {"status": resp.status_code, "latency_ms": latency}
    except Exception as e:
        latency = (time.time() - start) * 1000
        return {"status": "error", "latency_ms": latency, "error": str(e)}


async def run_bench(host: str, users: int, duration: int):
    """Run concurrent load test."""
    url = f"{host}/predict"
    # Edit this payload to match your model's input
    payload = {"input": "benchmark test input", "parameters": {}}

    results = []
    end_time = time.time() + duration

    print(f"Benchmarking {url}")
    print(f"  Concurrent users: {users}")
    print(f"  Duration: {duration}s")
    print(f"  Payload: {json.dumps(payload)}")
    print("-" * 50)

    async with httpx.AsyncClient() as client:
        while time.time() < end_time:
            tasks = [send_request(client, url, payload) for _ in range(users)]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            # Brief pause between batches
            await asyncio.sleep(0.1)

    # --- Report ---
    latencies = [r["latency_ms"] for r in results]
    successes = [r for r in results if r.get("status") == 200]
    errors = [r for r in results if r.get("status") != 200]

    print(f"\nResults ({len(results)} total requests):")
    print(f"  Successes: {len(successes)}")
    print(f"  Errors:    {len(errors)}")
    if latencies:
        print(f"  Latency p50:  {statistics.median(latencies):.1f}ms")
        print(f"  Latency p95:  {sorted(latencies)[int(len(latencies)*0.95)]:.1f}ms")
        print(f"  Latency p99:  {sorted(latencies)[int(len(latencies)*0.99)]:.1f}ms")
        print(f"  Throughput:   {len(results)/duration:.1f} req/s")

    if errors:
        print(f"\n  Sample errors:")
        for e in errors[:3]:
            print(f"    {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load test your model API")
    parser.add_argument("--host", default="http://localhost:8000")
    parser.add_argument("--users", type=int, default=10)
    parser.add_argument("--duration", type=int, default=30)
    args = parser.parse_args()

    asyncio.run(run_bench(args.host, args.users, args.duration))
