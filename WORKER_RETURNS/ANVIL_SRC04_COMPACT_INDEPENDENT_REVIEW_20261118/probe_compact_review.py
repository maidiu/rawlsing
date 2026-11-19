#!/usr/bin/env python3
"""Independent ordered-object review of the compact-vs-baseline rehearsal."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
CAND = Path(sys.argv[3]).resolve()
sys.path.insert(0, str(CAND))

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES


def load_receipt(name: str) -> dict:
    return json.loads((ROOT / name).read_text())


def open_estate(private: Path, receipt: dict):
    held = ExternalI02Roots(**receipt["i02"])
    estate = VerifiedDirectEstate(
        private, exact_path=receipt["path"],
        independently_held_manifest_sha256=receipt["manifest_sha256"],
        independently_held_i02=held,
        current_authorizer=lambda roots, h=held: roots == h,
    )
    ordered = {
        family: tuple(obj.as_dict() for obj in estate.iter_family(family, batch_size=7))
        for family in ALL_FAMILIES
    }
    return estate, ordered


def main() -> None:
    baseline_receipt = load_receipt("baseline-resume.json")
    compact_receipt = load_receipt("compact-resume.json")
    baseline_estate, baseline = open_estate(ROOT / "baseline-private", baseline_receipt)
    compact_estate, compact = open_estate(ROOT / "compact-private", compact_receipt)

    ordered_equal = baseline == compact
    counts_equal = {
        family: len(baseline[family]) == len(compact[family])
        for family in ALL_FAMILIES
    }
    root_equal = baseline_estate.i02 == compact_estate.i02
    manifest_equal = baseline_receipt["manifest_sha256"] == compact_receipt["manifest_sha256"]
    replay_equal = (
        baseline_estate.manifest.get("reconstructed_v1_release_ref")
        == compact_estate.manifest.get("reconstructed_v1_release_ref")
        and baseline_estate.i02.replay == compact_estate.i02.replay
    )

    baseline_events = [obj for obj in baseline["RespondentEvent"]]
    compact_events = [obj for obj in compact["RespondentEvent"]]
    raw = [event["semantic_fields"].get("raw_response_value")
           for event in baseline_events]
    typed = Counter(str(event["semantic_fields"].get("response_state"))
                    for event in baseline_events)
    raw_repr = [json.dumps(value, sort_keys=True) for value in raw]
    duplicate_value_count = len(raw_repr) - len(set(raw_repr))
    token_classes = Counter()
    for value in raw:
        token = (value or {}).get("$raw_physical_value", {}).get("token", {})
        token_classes[str(token.get("t")) + ":" + str(token.get("bits"))] += 1
    event_evidence = {
        "events": len(raw),
        "raw_none": sum(
            (value or {}).get("$raw_physical_value", {}).get("token", {}).get("t") == "none"
            for value in raw
        ),
        "raw_zero": sum(
            (value or {}).get("$raw_physical_value", {}).get("token", {}).get("bits")
            == "0000000000000000" for value in raw
        ),
        "raw_negative": sum(
            (value or {}).get("$raw_physical_value", {}).get("token", {}).get("bits")
            == "bff0000000000000" for value in raw
        ),
        "typed_states": dict(sorted(typed.items())),
        "raw_token_classes": dict(sorted(token_classes.items())),
        "duplicate_value_occurrences": duplicate_value_count,
        "compact_event_payload_equal": compact_events == baseline_events,
        "weight_count": len(baseline["WeightMeasureFact"]),
        "coordinate_count": len(baseline["EmpiricalCoordinateFact"]),
    }
    payload = {
        "schema": "ANVIL_SRC04_COMPACT_INDEPENDENT_ORDER_REVIEW@1",
        "sourcefree_test_only": True,
        "ordered_payload_equal": ordered_equal,
        "counts_equal": counts_equal,
        "exact_roots_equal": root_equal,
        "manifest_equal": manifest_equal,
        "replay_equal": replay_equal,
        "family_order_digest": {
            variant: {
                family: hashlib.sha256(
                    json.dumps(list(rows), sort_keys=True, separators=(",", ":")).encode()
                ).hexdigest()
                for family, rows in families.items()
            }
            for variant, families in (("baseline", baseline), ("compact", compact))
        },
        "event_evidence": event_evidence,
        "counts": {family: len(rows) for family, rows in baseline.items()},
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    if not (ordered_equal and all(counts_equal.values()) and root_equal and manifest_equal and replay_equal):
        raise SystemExit("INDEPENDENT_COMPACT_ORDER_REVIEW_FAILED")
    print(json.dumps({
        "ordered_payload_equal": ordered_equal,
        "counts_equal": all(counts_equal.values()),
        "exact_roots_equal": root_equal,
        "manifest_equal": manifest_equal,
        "replay_equal": replay_equal,
        "events": event_evidence["events"],
        "typed_states": event_evidence["typed_states"],
        "raw_none": event_evidence["raw_none"],
        "raw_zero": event_evidence["raw_zero"],
        "raw_negative": event_evidence["raw_negative"],
        "weight_count": event_evidence["weight_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
