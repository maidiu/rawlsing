from __future__ import annotations

import hashlib
import json
from pathlib import Path

from persona import s39_audit, sources
from persona.input import build_persona_input, evaluate_persona_response

RETURN = Path(__file__).resolve().parents[1]
EVIDENCE = RETURN / "evidence"


def _dump(name: str, payload: dict) -> None:
    (EVIDENCE / name).write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf8",
    )


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    performed = sources.run_probe(
        state_root=RETURN / ".runtime" / "evidence" / "performed",
        disposition="PERFORMED",
        perform="omit",
        mode="start",
        do_help=True,
    )
    refused = sources.run_probe(
        state_root=RETURN / ".runtime" / "evidence" / "refused",
        disposition="REFUSED",
        mode="start",
        do_help=True,
    )
    intact = evaluate_persona_response(performed)
    event_id = intact["persona_input"]["selected_event_id"]
    objective_only = evaluate_persona_response(
        performed, event_id=event_id, include_perception=False
    )
    history_severed = evaluate_persona_response(
        performed, include_history=False
    )
    restored = evaluate_persona_response(
        performed, event_id=event_id, include_perception=True, include_history=True
    )
    refused_result = evaluate_persona_response(refused)
    _dump(
        "persona_evidence.json",
        {
            "schema": "SOROK_PERSONA_INPUT_EVIDENCE@1",
            "grade": "TEST_ONLY_SOURCEFREE_PERSONA_INPUT_NOT_NATIVE",
            "native": False,
            "intact": intact,
            "objective_availability_without_perception": objective_only,
            "history_severed": history_severed,
            "restored": restored,
            "refused": refused_result,
            "store_mutated": any(
                item["store_mutated"]
                for item in (intact, objective_only, history_severed, restored)
            ),
        },
    )
    join_e_manifest = sources.JOIN_E_ROOT / "SOURCE_MANIFEST.json"
    _dump(
        "source_manifest.json",
        {
            "schema": "SOROK_PERSONA_INPUT_SOURCE_MANIFEST@1",
            "join_e_commit": sources.JOIN_E_COMMIT,
            "join_e_return": sources.JOIN_E_RETURN,
            "join_e_manifest_sha256": hashlib.sha256(
                join_e_manifest.read_bytes()
            ).hexdigest(),
            "s35_commit": "ce2478aa38eec7fb021aa95c01464a468a46fbc9",
            "s35_return": "WORKER_RETURNS/SOROK-S35-C9R-ACCESS-R1",
            "s11_spec": (
                "WORKER_RETURNS/SOROK-S11-ENCOUNTER-EXIT-SPEC-R1/"
                "02_WP19_CONSUMABLE_INTERFACE.json"
            ),
            "s11_spec_sha256": (
                "ad4add0d10aadf3ebdb4f30ff36d30da0f0e9356e9c5ca714c6e0e55b3071619"
            ),
            "s39_audit": s39_audit.audit(),
            "performed": {
                "state_root": performed["state_root"],
                "c9_sha256": sources.store_hash(
                    {"c12_path": performed["c9_path"]}
                ),
                "c12_sha256": sources.store_hash(performed),
                "e1_event_hash": performed["e1_event_hash"],
                "branch_id": performed["branch_id"],
                "branch_clock": performed["branch_clock"],
                "event_clock": performed["event_time"],
                "history_hash": performed["history"]["history_hash"],
                "history_event_head": performed["history"]["event_head"],
                "history_event_count": performed["history"]["event_count"],
                "history_last_clock": performed["history"]["last_clock"],
                "performed_action_refs": performed["history"][
                    "performed_action_refs"
                ],
                "objective_refs": performed["history"]["objective_refs"],
            },
            "refused": {
                "state_root": refused["state_root"],
                "c12_sha256": sources.store_hash(refused),
                "e1_event_hash": refused["e1_event_hash"],
                "branch_id": refused["branch_id"],
                "event_clock": refused["event_time"],
                "history_hash": refused["history"]["history_hash"],
            },
        },
    )
    print(
        json.dumps(
            {
                "intact": intact["outcome"],
                "objective_only": objective_only["outcome"],
                "history_severed": history_severed["outcome"],
                "restored": restored["outcome"],
                "refused": refused_result["outcome"],
                "store_mutated": any(
                    item["store_mutated"]
                    for item in (
                        intact,
                        objective_only,
                        history_severed,
                        restored,
                    )
                ),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
