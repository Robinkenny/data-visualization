#!/usr/bin/env python3
"""Fetch Mark Six draws from HKJC GraphQL and write data/draws.txt (newest first)."""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

GRAPHQL_URL = "https://info.cld.hkjc.com/graphql/base/"
QUERY = """
fragment lotteryDrawsFragment on LotteryDraw {
  drawDate
  drawResult { drawnNo }
}
query marksixResult($startDate: String, $endDate: String, $drawType: LotteryDrawType) {
  lotteryDraws(startDate: $startDate, endDate: $endDate, drawType: $drawType) {
    ...lotteryDrawsFragment
  }
}
"""


def fetch_range(start: datetime, end: datetime) -> list[dict]:
    payload = {
        "operationName": "marksixResult",
        "variables": {
            "startDate": start.strftime("%Y%m%d"),
            "endDate": end.strftime("%Y%m%d"),
            "drawType": "MARKSIX",
        },
        "query": QUERY,
    }
    req = Request(
        GRAPHQL_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "data-visualization/1.0"},
        method="POST",
    )
    with urlopen(req, timeout=60) as resp:
        body = json.loads(resp.read().decode())
    if "errors" in body:
        raise RuntimeError(body["errors"])
    return body.get("data", {}).get("lotteryDraws") or []


def main() -> None:
    out = Path(__file__).resolve().parents[1] / "data" / "draws.txt"
    start = datetime(1993, 1, 1)
    end = datetime.now() + timedelta(days=1)
    all_draws: list[tuple[str, list[int]]] = []

    chunk_start = start
    while chunk_start < end:
        chunk_end = min(chunk_start + timedelta(days=89), end)
        print(f"Fetching {chunk_start.date()} .. {chunk_end.date()} ...", flush=True)
        try:
            rows = fetch_range(chunk_start, chunk_end)
        except Exception as e:
            print(f"  failed: {e}", file=sys.stderr)
            rows = []
        for row in rows:
            dr = row.get("drawResult") or {}
            nums = dr.get("drawnNo") or []
            if len(nums) != 6:
                continue
            nums = [int(n) for n in nums]
            all_draws.append((row.get("drawDate", ""), nums))
        chunk_start = chunk_end + timedelta(days=1)
        time.sleep(0.25)

    # Dedupe by date+nums, sort by date desc (newest first like user's paste)
    seen = set()
    unique: list[tuple[str, list[int]]] = []
    for d, nums in sorted(all_draws, key=lambda x: x[0]):
        key = tuple(sorted(nums))
        if key in seen:
            continue
        seen.add(key)
        unique.append((d, nums))
    unique.reverse()

    lines = [",".join(str(n) for n in nums) for _, nums in unique]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    print(f"Wrote {len(lines)} draws to {out}")
    if lines:
        print(f"Newest: {lines[0]}")
        print(f"Oldest: {lines[-1]}")


if __name__ == "__main__":
    main()
