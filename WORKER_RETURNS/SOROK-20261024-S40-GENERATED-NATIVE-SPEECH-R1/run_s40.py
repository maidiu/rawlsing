"""Minimal runnable S40 generated-native-speech consumer."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from s40.session import S40GeneratedSession  # noqa: E402
from s39.sources import context_records  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _records(producer_actor: str, as_of: int, **flags) -> list[dict]:
    return context_records(
        actor_id=producer_actor, branch_id="first_session", as_of=as_of, **flags
    )


def run_one(root: Path, *, label: str, share: bool, context: str) -> dict:
    case = case_for(share)
    source = source_for(case)
    from s39.producer import GeneratedProducer

    probe = GeneratedProducer(root / f"probe-{label}", case=case, source=source)
    try:
        probe.stage_m35()
        if context == "request":
            records = _records(
                probe.occurrence.actor_id, probe.as_of,
                repair_urgent=True, avoid_debt=True, prior_b_share=True,
            )
        elif context == "refusal":
            records = _records(
                probe.occurrence.actor_id, probe.as_of, prior_b_refusal=True,
            )
        elif context == "attend":
            records = _records(
                probe.occurrence.actor_id, probe.as_of,
                avoid_debt=True, prefer_independent=True,
            )
        else:
            records = _records(probe.occurrence.actor_id, probe.as_of)
    finally:
        probe.close()

    state = root / label
    session = S40GeneratedSession.start(
        state, case=case, source=source, source_records=records
    )
    try:
        s40 = session.read_s40()
        read = session.read_s36()
        status = session.status()
        verify = session.verify()
    finally:
        session.close()
    cold = S40GeneratedSession.open(state)
    try:
        cold_s40 = cold.read_s40()
        cold_read = cold.read_s36()
        cold_verify = cold.verify()
    finally:
        cold.close()
    return {
        "label": label,
        "context": context,
        "source_operation": source["b_operation"],
        "selected_option": s40["selected_option"],
        "attempt_status": s40["attempt_status"],
        "performed": s40["performed"],
        "language_status": s40["language_status"],
        "speech_event_id": s40["speech_event_id"],
        "speech_event_hash": s40["speech_event_hash"],
        "native_text": s40["native_text"],
        "translation_text": s40["translation_text"],
        "plan_hash": s40["plan_hash"],
        "equivalence_receipt_hash": s40["equivalence_receipt_hash"],
        "e1_event_id": s40.get("e1_event_id", ""),
        "e1_event_hash": s40.get("e1_event_hash", ""),
        "s36_outcome": read["outcome"],
        "s36_response_kind": read["response_kind"],
        "target_branch": read["target_branch"],
        "target_reason": read["target_reason"],
        "target_proposals": read["target_proposals"],
        "target_state_rows": read["target_state_rows"],
        "status_s40": status.get("s40_language", {}),
        "verify_ok": verify["ok"],
        "cold": {
            "selected_option": cold_s40["selected_option"],
            "attempt_status": cold_s40["attempt_status"],
            "language_status": cold_s40["language_status"],
            "speech_event_hash": cold_s40["speech_event_hash"],
            "native_text": cold_s40["native_text"],
            "translation_text": cold_s40["translation_text"],
            "plan_hash": cold_s40["plan_hash"],
            "s36_response_ref": cold_read["response_ref"],
            "verify_ok": cold_verify["ok"],
        },
    }


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-s40-"))
    report = {
        "schema": "SOROK_S40_GENERATED_NATIVE_SPEECH_RUN@1",
        "grade": "TEST_ONLY_S40_GENERATED_INTENT_LANGUAGE_MODEL_PREMISE_NOT_GENERAL_TRANSLATION",
        "native": False,
        "provider_calls": 0,
        "product_model_calls": 0,
        "state_root": str(root),
        "chains": [
            run_one(root, label="share-request", share=True, context="request"),
            run_one(root, label="share-refusal-speech", share=True, context="refusal"),
            run_one(root, label="refuse-denied", share=False, context="request"),
            run_one(root, label="share-attend-nonverbal", share=True, context="attend"),
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
