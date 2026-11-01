"""M35 source-binding falsifier.

Run from a disposable clone of the rawlsing M35 branch with the warm JOIN-E
return available (the return's install.py selects it):

  PYTHONDONTWRITEBYTECODE=1 python3 -B \
    WORKER_RETURNS/SOROK-20261024-BP2-FIRSTCLASS-B-SOURCE-R1/oracles/m35_source_mutation_oracle.py

The supplied source is first-class only if it is the exact observed B/E1
preimage from the case, not merely a valid-looking envelope.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

RETURN = Path("WORKER_RETURNS/SOROK-20261024-BP2-FIRSTCLASS-B-SOURCE-R1").resolve()
sys.path.insert(0, str(RETURN))

import install  # noqa: E402

install.install()

import firstclass  # noqa: E402
from r31j.scenarios import evaluated  # noqa: E402


def main() -> int:
    case = evaluated(share=True, e2=False)["case"]
    base = firstclass.source_from_case(case)
    mutations = {
        "wrong_owner": {"b_owner": "FAKE_OWNER"},
        "wrong_event_ref": {"b_event_ref": "TEST_ONLY_FAKE_EVENT"},
        "wrong_event_hash": {"b_event_hash": "0" * 64},
        "wrong_clock": {"b_clock": 999},
        "wrong_operation": {"b_operation": "REFUSE_TOOL", "b_quantity": 0},
        "wrong_quantity": {"b_quantity": 5},
        "wrong_e1_ref": {"a_e1_ref": "TEST_ONLY_FAKE_E1"},
        "wrong_e1_hash": {"a_e1_hash": "0" * 64},
        "wrong_e1_clock": {"a_e1_clock": 999},
    }
    rows = []
    for label, mutation in mutations.items():
        source = dict(base)
        source.update(mutation)
        with tempfile.TemporaryDirectory(prefix=f"m35-{label}-") as tmp:
            try:
                partial, producer = firstclass.c9_only(
                    Path(tmp) / "state", case=case, source=source)
                rows.append({
                    "label": label,
                    "accepted": True,
                    "material_access": partial.get("material_access"),
                    "c9_target_branch": (partial.get("c9") or {}).get(
                        "target_branch"),
                    "c9_target_id": (partial.get("c9") or {}).get("target_id", ""),
                })
                producer.close()
            except Exception as exc:  # noqa: BLE001
                rows.append({
                    "label": label,
                    "accepted": False,
                    "error": type(exc).__name__,
                    "code": getattr(exc, "code", ""),
                })
    failed = [row for row in rows if row["accepted"]]
    print(json.dumps({
        "schema": "M35_SOURCE_MUTATION_ORACLE@1",
        "cut": "55377b554ce49941665ae4080f70f2132ad963f5",
        "source_commit": "2d11e32c2d5e7d44449e03c6af68aa75d4de1a60",
        "base": "76961d2e58e7139ddd63f1758aea19a8026b375f",
        "counts": {"PASS": len(rows) - len(failed), "FAIL": len(failed)},
        "red_oracles": [row["label"] for row in failed],
        "rows": rows,
    }, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
