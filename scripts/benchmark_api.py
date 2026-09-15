from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path

import httpx
from fastapi.testclient import TestClient

from riskqueue.api.main import app


def payload(index: int) -> dict:
    return {
        "transaction_id": f"bench-{index}",
        "step": index % 24,
        "type": "TRANSFER",
        "amount": 1250 + index,
        "nameOrig": f"C{index}",
        "nameDest": f"M{index}",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Local development benchmark—not production throughput"
    )
    parser.add_argument("--url", default="http://localhost:8000")
    parser.add_argument("--in-process", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("artifacts/reports/api_benchmark.json"))
    args = parser.parse_args()
    context = TestClient(app) if args.in_process else httpx.Client(base_url=args.url, timeout=30)
    results = []
    with context as client:
        for size in (1, 10, 100, 1000):
            times = []
            for _ in range(10):
                start = time.perf_counter()
                if size == 1:
                    response = client.post("/v1/score", json=payload(0))
                else:
                    response = client.post(
                        "/v1/score/batch", json={"transactions": [payload(i) for i in range(size)]}
                    )
                response.raise_for_status()
                times.append((time.perf_counter() - start) * 1000)
            ordered = sorted(times)
            row = {
                "batch_size": size,
                "median_ms": statistics.median(times),
                "p95_ms": ordered[9],
                "mode": "in-process local development" if args.in_process else "local HTTP",
            }
            results.append(row)
            print(
                f"batch={size:4d} median={statistics.median(times):7.2f} ms p95={ordered[9]:7.2f} ms"
            )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
