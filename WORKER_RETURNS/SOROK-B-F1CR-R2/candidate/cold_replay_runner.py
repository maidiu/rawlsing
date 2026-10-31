#!/usr/bin/env python3
"""Fresh-process cold replay for the H06... no, B-F1CR-R2 targetless C10 ledger."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import targetless_c10_consumer as T


def main() -> None:
    source = Path(sys.argv[1])
    target = Path(sys.argv[2])
    payload = json.loads(source.read_text(encoding="utf-8"))
    result = T.cold_replay(payload)
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")


if __name__ == "__main__":
    main()
