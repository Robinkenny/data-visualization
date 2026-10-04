#!/usr/bin/env python3
"""Parse draw lines (6 comma-separated ints) into draws.json."""
import json
import re
import sys
from pathlib import Path


def parse_text(text: str) -> list[list[int]]:
    draws = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = re.split(r"[,，\s]+", line)
        nums = [int(p) for p in parts if p.isdigit()]
        if len(nums) == 6 and all(1 <= n <= 49 for n in nums):
            draws.append(nums)
    return draws


def main() -> None:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "data/draws.txt")
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "data/draws.json")
    text = src.read_text(encoding="utf-8")
    draws = parse_text(text)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(draws, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {len(draws)} draws to {out}")


if __name__ == "__main__":
    main()
