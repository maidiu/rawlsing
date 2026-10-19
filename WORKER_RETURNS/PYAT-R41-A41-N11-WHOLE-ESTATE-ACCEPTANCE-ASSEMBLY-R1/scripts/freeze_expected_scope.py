#!/usr/bin/env python3
"""Freeze the independent expected scope. MUST run before any assessor logic.

Reads only the four declared HQ estate documents at their exact Git preimages.
Never reads a producer receipt, a consumer output or an assessor result.

Usage (from the A41 return root):
    python3 scripts/freeze_expected_scope.py [--repo REPO_ROOT]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETURN_ROOT = HERE.parent
sys.path.insert(0, str(RETURN_ROOT))

from a41.gitpreimage import GitPreimage  # noqa: E402
from a41 import expected_scope  # noqa: E402

STARTUP = "c4934fd71120d37a4d06f7c830891e6e97fe4ecf"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path,
                    default=RETURN_ROOT.parents[1])
    ap.add_argument("--startup", default=STARTUP)
    ap.add_argument("--out", type=Path,
                    default=RETURN_ROOT / "evidence" / "expected_scope_frozen.json")
    args = ap.parse_args()

    gp = GitPreimage(args.repo)
    scope = expected_scope.build_expected_scope(gp, args.startup)

    # Assessor logic must not exist when this freeze is written.
    assessor = RETURN_ROOT / "a41" / "estate_assessor.py"
    frozen_record = {
        "frozen_before_assessor_logic": not assessor.exists(),
        "assessor_path_checked": str(assessor.relative_to(RETURN_ROOT)),
    }
    scope["freeze_order_discipline"] = frozen_record

    payload = json.dumps(scope, indent=2, sort_keys=True) + "\n"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(payload, encoding="utf-8")
    sha = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    print(json.dumps({
        "out": str(args.out),
        "sha256_of_written_file": sha,
        "scope_digest": scope["scope_digest"],
        "expected_cell_count": scope["expected_cell_count"],
        "register_151_count": scope["register_151_count"],
        "ledger_101_count": scope["ledger_101_count"],
        "crosswalk_edges": len(scope["crosswalk_151_101"]["edges"]),
        "unmatched_register_rows": len(scope["crosswalk_151_101"]["unmatched_register_rows"]),
        "unmatched_ledger_rows": len(scope["crosswalk_151_101"]["unmatched_ledger_rows"]),
        "frozen_before_assessor_logic": frozen_record["frozen_before_assessor_logic"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
