"""Actual one-call product turn on the accepted same-person S47 session."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from s48.bootstrap import install  # noqa: E402

install()

from s45.fixtures import root_bundle  # noqa: E402
from s46.model import make_domain  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from s48.session import S48Session  # noqa: E402


def _start(state):
    case = case_for(True)
    return S48Session.start(
        state,
        bundle=root_bundle("01" * 32),
        case=case,
        source=source_for(case),
        language_context={"milieu_id": "workshop"},
    )


def main() -> int:
    state = RETURN / "runtime" / "entrypoint-state"
    if state.exists():
        shutil.rmtree(state)
    state.mkdir(parents=True)
    workdir = RETURN / "runtime" / "product-workdir"
    session = _start(state)
    try:
        session.produce_interval(
            make_domain(
                mode="SCHEDULED_ONLY",
                start=session.clock(),
                end=session.clock() + 4,
            )
        )
        before_events = session.read_events()
        source_event = before_events[-1]
        root_hash = session.read_root()["root_hash"]
        source_before = session.c9_interval_source()
        turn = session.run_turn(
            product_workdir=workdir,
            product_log_dir=RETURN / "logs",
            timeout=300,
        )
        source_after = session.c9_interval_source()
        after_events = session.read_events()
        product_turn_record = session.product_turn(turn.get("source_event_ref", ""))
        event = turn.get("event") or {}
        c9 = None
        if turn.get("event_ref"):
            c9 = session.read_c9_conditioning(turn["event_ref"])
        verify = session.verify()
    finally:
        session.close()

    cold = S48Session.open(state)
    try:
        cold_turn = cold.run_turn(
            source_event_ref=turn.get("source_event_ref"),
            product_workdir=workdir,
            product_log_dir=RETURN / "logs",
            timeout=300,
        )
        cold_events = cold.read_events()
        cold_root = cold.read_root()["root_hash"]
        cold_verify = cold.verify()
    finally:
        cold.close()

    report = {
        "schema": "SOROK_S48_ONE_CALL_RUN@1",
        "actual_provider_call": bool(
            ((product_turn_record or {}).get("body", {}).get("call_receipt") or {})
            .get("actual_provider_call")
        ),
        "provider": "opencode-go",
        "model": "opencode-go/deepseek-v4.1-flash",
        "variant": "max",
        "source_event": {
            "event_ref": source_event.get("e1_event_id"),
            "event_hash": source_event.get("e1_event_hash"),
            "event_ordinal": source_event.get("event_ordinal"),
            "event_time": source_event.get("event_time"),
        },
        "root_hash": root_hash,
        "root_unchanged": cold_root == root_hash,
        "s47_condition_before": {
            "source_ref": source_before.get("source_ref") if source_before else "",
            "source_hash": source_before.get("source_hash") if source_before else "",
            "access": (
                (source_before.get("content") or {}).get("access")
                if source_before else ""
            ),
        },
        "s47_condition_after": {
            "source_ref": source_after.get("source_ref") if source_after else "",
            "source_hash": source_after.get("source_hash") if source_after else "",
            "access": (
                (source_after.get("content") or {}).get("access")
                if source_after else ""
            ),
        },
        "turn_id": turn.get("turn_id"),
        "turn_status": turn.get("status"),
        "source_owner": turn.get("source_owner", ""),
        "source_performer_owner": turn.get("source_performer_owner", ""),
        "source_actor": turn.get("source_actor", ""),
        "candidate_source_event_ref": turn.get("source_event_ref_candidate", ""),
        "candidate_source_event_hash": turn.get("source_event_hash_candidate", ""),
        "provider_call_count": turn.get("provider_call_count", 0),
        "cached_on_cold": cold_turn.get("cached"),
        "cold_provider_call_count": cold_turn.get("provider_call_count", 0),
        "same_event_on_cold": (
            cold_turn.get("event_ref") == turn.get("event_ref")
            if turn.get("event_ref") else True
        ),
        "candidate_id": turn.get("candidate_id", ""),
        "no_input_barrier": turn.get("no_input_barrier", ""),
        "sci05_hold": bool(turn.get("sci05_hold")),
        "event": {
            "event_ref": event.get("e1_event_id", ""),
            "event_hash": event.get("e1_event_hash", ""),
            "event_ordinal": event.get("event_ordinal"),
            "event_time": event.get("event_time"),
            "status": turn.get("admission_status"),
            "selected_option": event.get("selected_option"),
            "action_event_kind": event.get("action_event_kind"),
            "target_branch": (
                (event.get("c9") or {}).get("target_branch")
                if isinstance(event.get("c9"), dict)
                else ""
            ),
            "target_proposals": list(event.get("target_proposals") or []),
        },
        "c9": {
            "event_ref": (c9 or {}).get("event_ref", ""),
            "s47_source_ref": (c9 or {}).get("s47_source_ref", ""),
            "s47_source_hash": (c9 or {}).get("s47_source_hash", ""),
            "s47_source_in_readset": (c9 or {}).get("s47_source_in_readset", False),
            "objective_material_eligible": (
                (c9 or {}).get("objective_material_eligible")
            ),
            "target_branch": (c9 or {}).get("target_branch", ""),
            "target_reason": (c9 or {}).get("target_reason", ""),
            "target_proposals": list((c9 or {}).get("target_proposals") or []),
        },
        "event_count_before": len(before_events),
        "event_count_after": len(after_events),
        "cold_event_count": len(cold_events),
        "event_order": [
            {
                "event_ordinal": row.get("event_ordinal"),
                "e1_event_id": row.get("e1_event_id"),
            }
            for row in after_events
        ],
        "verify_ok": verify["ok"] and cold_verify["ok"],
        "event_call_receipt": (
            ((product_turn_record or {}).get("body", {}).get("call_receipt") or {})
        ),
        "target_proposals": [],
        "native_grants": {
            "actor": False, "rule": False, "source": False, "human": False,
            "c8": False, "c9": False, "c12": False,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["verify_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
