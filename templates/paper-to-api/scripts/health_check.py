"""Health check script for Docker HEALTHCHECK and monitoring."""

import sys
import httpx


def check(host: str) -> bool:
    try:
        resp = httpx.get(f"{host}/health", timeout=5.0)
        data = resp.json()
        if data.get("status") == "ok":
            print(f"OK — {data.get('model_name')} v{data.get('model_version')}, GPU: {data.get('gpu_name', 'N/A')}")
            return True
        print(f"UNHEALTHY — {data}")
        return False
    except Exception as e:
        print(f"UNREACHABLE — {e}")
        return False


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    sys.exit(0 if check(host) else 1)
