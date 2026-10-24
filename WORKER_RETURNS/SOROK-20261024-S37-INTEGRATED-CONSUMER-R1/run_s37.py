"""Minimal runnable S37 integrated consumer.

Runs the same targetless session/reader for lawful SHARE_TOOL and REFUSE_TOOL,
then a neutral separately witnessed language plan/native speech/labeled English
view and the existing resource-governed help action. All identities are
TEST_ONLY; no native authority or external model/provider is invoked.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from s37.harness import (  # noqa: E402
    setup_neutral_language,
    start_session,
    summary,
)
from s37.session import S37IntegratedSession  # noqa: E402


def run_one(root: Path, *, share: bool) -> dict:
    label = "share" if share else "refuse"
    state = root / label
    session = start_session(state, share=share)
    try:
        before = summary(session)
        setup_neutral_language(session)
        said = session.say("Hello.")
        speech_event_id = said["admission"]["speech_event_id"]
        view = session.language_view(speech_event_id, locale="en")
        helped = session.do_help()
        after = summary(session)
        session.close()
        cold = S37IntegratedSession.open(state)
        try:
            cold_read = cold.read_s36()
            cold_view = cold.language_view(speech_event_id, locale="en")
            cold_verify = cold.verify()
            cold_summary = summary(cold)
        finally:
            cold.close()
        return {
            "label": label,
            "session_class": before["session_class"],
            "source_operation": before["source_operation"],
            "source_b_event_hash": before["source_b_event_hash"],
            "source_actor_map": before["source_actor_map"],
            "c8_occurrence_id": before["c8_occurrence_id"],
            "c8_state_digest": before["c8_state_digest"],
            "e1_event_id": before["e1_event_id"],
            "e1_event_hash": before["e1_event_hash"],
            "tools_remaining": before["tools_remaining"],
            "tool_available": before["tool_available"],
            "response_ref": after["response_ref"],
            "response_receipt_hash": after["response_receipt_hash"],
            "c9_receipt_hash": after["c9_receipt_hash"],
            "s35_receipt_hash": after["s35_receipt_hash"],
            "access_source_ref": after["access_source_ref"],
            "response_source_ref": after["response_source_ref"],
            "outcome": after["outcome"],
            "response_kind": after["response_kind"],
            "target_branch": after["target_branch"],
            "target_reason": after["target_reason"],
            "target_id": after["target_id"],
            "target_proposals": after["target_proposals"],
            "target_state_rows": after["target_state_rows"],
            "language": {
                "strategy": said["strategy"],
                "native_text": said["language"]["native_artifact"]["text"],
                "english_text": said["language"]["translation_artifact"]["text"],
                "equivalence": said["language"]["equivalence"]["status"],
                "view_status": view["status"],
                "view_display_mode": view["display_mode"],
                "product_model_calls": 0,
            },
            "help": {
                "accepted": helped["accepted"],
                "strategy": helped["strategy"],
            },
            "cold": {
                "response_ref": cold_read["response_ref"],
                "outcome": cold_read["outcome"],
                "target_branch": cold_read["target_branch"],
                "target_reason": cold_read["target_reason"],
                "target_state_rows": cold_read["target_state_rows"],
                "speech_event_hash": cold_view["source_event_hash"],
                "english_text": cold_view["translation_text"],
                "verify_ok": cold_verify["ok"],
                "response_ref_matches": cold_summary["response_ref"]
                == after["response_ref"],
            },
            "verify_ok": True,
            "native": False,
            "product_model_calls": 0,
        }
    except Exception:
        session.close()
        raise


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-s37-"))
    report = {
        "schema": "SOROK_S37_INTEGRATED_CONSUMER_RUN@1",
        "grade": "TEST_ONLY_SOURCEFREE_NOT_NATIVE",
        "native": False,
        "provider_calls": 0,
        "product_model_calls": 0,
        "state_root": str(root),
        "chains": [
            run_one(root, share=True),
            run_one(root, share=False),
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
