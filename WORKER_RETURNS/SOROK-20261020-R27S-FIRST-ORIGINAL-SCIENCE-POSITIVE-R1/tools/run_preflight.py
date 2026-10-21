"""Run the fail-closed native input preflight over one JSON bundle."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

from native_input_preflight import STATUS_REFUSED, evaluate  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args(argv)
    bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
    receipt = evaluate(bundle)
    json.dump(receipt, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 2 if receipt["status"] == STATUS_REFUSED else 0


if __name__ == "__main__":
    raise SystemExit(main())
