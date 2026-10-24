"""Minimal runnable S39 source-bound generated-response consumer."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

from s39.session import S39GeneratedSession  # noqa: E402
from s37.harness import (  # noqa: E402
    case_for,
    setup_neutral_language,
    source_for,
)


def run_one(root: Path, *, share: bool) -> dict:
    label = "share" if share else "refuse"
    state = root / label
    case = case_for(share)
    session = S39GeneratedSession.start(state, case=case, source=source_for(case))
    try:
        generated = session.read_generation()
        read = session.read_s36()
        setup_neutral_language(session)
        said = session.say("Hello.")
        speech_id = said["admission"]["speech_event_id"]
        view = session.language_view(speech_id, locale="en")
        status = session.status()
        verify = session.verify()
    finally:
        session.close()
    cold = S39GeneratedSession.open(state)
    try:
        cold_generated = cold.read_generation()
        cold_read = cold.read_s36()
        cold_view = cold.language_view(speech_id, locale="en")
        cold_verify = cold.verify()
    finally:
        cold.close()
    return {
        "label": label,
        "source_operation": session.meta["source"]["b_operation"],
        "selected_option": generated["selected_option"],
        "attempt_status": generated["attempt_status"],
        "performed": generated["performed"],
        "action_event_id": generated["event_id"],
        "action_event_hash": generated["event_hash"],
        "generation_hash": generated["generation_hash"],
        "attempt_hash": generated["attempt_hash"],
        "provenance": generated["provenance"],
        "s36_outcome": read["outcome"],
        "s36_response_kind": read["response_kind"],
        "target_branch": read["target_branch"],
        "target_reason": read["target_reason"],
        "target_proposals": read["target_proposals"],
        "target_state_rows": read["target_state_rows"],
        "language": {
            "strategy": said["strategy"],
            "native_text": said["language"]["native_artifact"]["text"],
            "english_text": said["language"]["translation_artifact"]["text"],
            "view_status": view["status"],
            "view_mode": view["display_mode"],
            "product_model_calls": 0,
        },
        "status_s39": status.get("s39_generation", {}),
        "verify_ok": verify["ok"],
        "cold": {
            "generation_hash": cold_generated["generation_hash"],
            "attempt_hash": cold_generated["attempt_hash"],
            "action_event_hash": cold_generated["event_hash"],
            "s36_response_ref": cold_read["response_ref"],
            "s36_outcome": cold_read["outcome"],
            "english_text": cold_view["translation_text"],
            "verify_ok": cold_verify["ok"],
        },
    }


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-s39-"))
    report = {
        "schema": "SOROK_S39_GENERATED_RESPONSE_RUN@1",
        "grade": "TEST_ONLY_CONSTRUCTIVE_GENERATION_NOT_EXTERNALLY_OBSERVED",
        "native": False,
        "provider_calls": 0,
        "product_model_calls": 0,
        "state_root": str(root),
        "chains": [run_one(root, share=True), run_one(root, share=False)],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
