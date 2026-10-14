"""Path setup and verdict ledger for the G12 court.

The bridge imports the blob-verified staged S-GI1 (commit 27ca1f2792a5...).
"""
import json
import sys
from pathlib import Path

RET = Path(__file__).resolve().parent
for p in (str(RET), str(RET / "staging" / "sigi1_src" / "01_LAB_IMPLEMENTATION")):
    if p not in sys.path:
        sys.path.insert(0, p)

VERDICTS: dict = {}


def pytest_sessionfinish(session, exitstatus):
    out = RET / "outputs" / "gi2_57_predicates.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "schema": "G12_GI2_57_PREDICATES_ON_SGI1@1",
        "n_predicates": len(VERDICTS),
        "tally": {
            v: sum(1 for x in VERDICTS.values() if x["verdict"] == v)
            for v in sorted({x["verdict"] for x in VERDICTS.values()})
        },
        "predicates": VERDICTS,
    }, indent=2, sort_keys=True) + "\n")
