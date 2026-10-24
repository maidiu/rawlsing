"""S40 plan public-fact binding falsifier.

The authorized plan's public ADMITTED_E1 fact must name the actual E1 event ID and
hash, not use the E1 hash as both values.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from s40.bootstrap import install

install()

from s37.harness import case_for, source_for  # noqa: E402
from s40.session import S40GeneratedSession  # noqa: E402


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="s40-e1-plan-"))
    case = case_for(True)
    session = S40GeneratedSession.start(
        root, case=case, source=source_for(case)
    )
    try:
        actual_id = session.meta["c8"]["e1_event_id"]
        actual_hash = session.meta["c8"]["e1_event_hash"]
        plan = None
        for row in session.product.store.episodes(session.branch_id):
            if row.get("kind") == "EXPRESSION_ADMISSION":
                plan = (row.get("body") or {}).get("admission", {}).get("plan")
                break
        assert plan is not None
        facts = (plan.get("readset") or {}).get("public_outward_facts") or []
        fact = next(item for item in facts if item.get("kind") == "ADMITTED_E1")
        observed = {
            "actual_e1_event_id": actual_id,
            "actual_e1_event_hash": actual_hash,
            "plan_public_e1": fact,
            "plan_hash": plan.get("plan_hash"),
        }
        ok = fact.get("event_id") == actual_id and fact.get("event_hash") == actual_hash
        result = {
            "schema": "SOROK_REVIEW_S40_E1_PLAN_BINDING_V1",
            "cut": "1d6f89b2ef60f4713741c9432c63940737248984",
            "base": "e41513fa65601a37e7b3b430d26c626ae0217d90",
            "counts": {"PASS": 1 if ok else 0, "FAIL": 0 if ok else 1},
            "red_oracles": [] if ok else ["ADMITTED_E1"],
            "observed": observed,
        }
        print(json.dumps(result, indent=2))
        return 0 if ok else 1
    finally:
        session.close()


if __name__ == "__main__":
    raise SystemExit(main())
