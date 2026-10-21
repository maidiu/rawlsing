"""Fresh-process worker for BP4 cold reentry evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RET))

from bp4.product import BP4Product  # noqa: E402


def main() -> int:
    mode, root = sys.argv[1], Path(sys.argv[2])
    product = BP4Product(root)
    try:
        if mode == "build":
            product.say("cold build speech")
            product.wait(30)
            product.travel("market")
            product.attend()
            result = product.observe()
        elif mode == "observe":
            result = product.reenter()
        else:
            raise SystemExit("UNKNOWN_MODE")
        print(json.dumps(result, sort_keys=True))
        return 0
    finally:
        product.close()


if __name__ == "__main__":
    raise SystemExit(main())
