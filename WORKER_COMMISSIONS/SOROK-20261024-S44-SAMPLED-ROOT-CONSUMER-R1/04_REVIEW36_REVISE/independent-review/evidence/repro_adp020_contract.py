import json
import os
import sys
from pathlib import Path

RETURN = Path(os.environ["S44_RETURN"]).resolve()
sys.path.insert(0, str(RETURN))

from s44.bootstrap import install

install()

from s44.bundle import default_bundle
from s44.root import generate_root

REQUIRED_CANDIDATE_FIELDS = [
    "candidate_id",
    "candidate_replay_hash",
    "candidate_authority_id",
    "candidate_authority_version",
    "eligibility_or_admission_receipt_hash",
]
REQUIRED_COORDINATE_FIELDS = [
    "scope_kind",
    "scope_id",
    "stream_name",
    "anchor_event_index",
    "anchor_event_id_or_init_checkpoint_hash",
    "rule_invocation_id",
    "decision_slot",
    "occurrence_index",
    "draw_index",
]


def main() -> int:
    root = generate_root(default_bundle(root_seed="11" * 32))
    draw = next(
        row for row in root.receipt["draw_receipts"]
        if row.get("operation") == "WEIGHTED_CANDIDATE_INTEGER"
    )
    entries = (draw.get("candidate_set") or {}).get("entries") or []
    entry = entries[0] if entries else {}
    coordinate = draw.get("coordinate") or {}
    report = {
        "schema": "SOROK_S44_ADP020_CONTRACT_REPRO@1",
        "candidate_entry": entry,
        "candidate_missing_required_fields": [
            field for field in REQUIRED_CANDIDATE_FIELDS if field not in entry
        ],
        "candidate_set_identity_mode": (draw.get("candidate_set") or {}).get(
            "identity_mode"
        ),
        "candidate_set_hash": draw.get("candidate_set_hash"),
        "coordinate": coordinate,
        "coordinate_missing_required_fields": [
            field for field in REQUIRED_COORDINATE_FIELDS
            if field not in coordinate
        ],
        "coordinate_has_anchor_event_id": "anchor_event_id" in coordinate,
        "decision_replay_identity_hash": draw.get(
            "decision_replay_identity_hash"
        ),
        "draw_consumed": draw.get("draw_consumed"),
        "selected_candidate_id": draw.get("selected_candidate_id"),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
