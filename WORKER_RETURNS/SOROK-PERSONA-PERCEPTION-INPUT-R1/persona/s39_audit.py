"""Read-only audit of the S39 producer at the pinned cut."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
S39_COMMIT = "6604f2d9"
S39_PRODUCER = (
    "WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1/s39/producer.py"
)


def audit() -> dict:
    blob = subprocess.run(
        ["git", "rev-parse", f"{S39_COMMIT}:{S39_PRODUCER}"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    text = subprocess.run(
        ["git", "show", f"{S39_COMMIT}:{S39_PRODUCER}"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return {
        "schema": "SOROK_PERSONA_S39_PRODUCER_AUDIT@1",
        "commit": S39_COMMIT,
        "path": S39_PRODUCER,
        "git_blob": blob,
        "sha256": hashlib.sha256(text.encode("utf8")).hexdigest(),
        "uses_synthetic_source_records": "source_records" in text,
        "uses_test_only_response_witness": (
            "make_actor_owned_response_witness" in text
            and "TEST_ONLY_CONSTRUCTIVE_GENERATION_NOT_EXTERNALLY_OBSERVED"
            in text
        ),
        "operation_only_availability": (
            '"tool_available": self.source["b_operation"] == "SHARE_TOOL"'
            in text
        ),
        "used_by_persona_input": False,
        "reason": (
            "S39 generates a synthetic attempt from TEST_ONLY source records, "
            "derives tool availability from B operation, and fabricates a "
            "TEST_ONLY response witness from the generated attempt. It cannot "
            "supply actual persona perception/history behavior."
        ),
    }


__all__ = ["S39_COMMIT", "S39_PRODUCER", "audit"]
