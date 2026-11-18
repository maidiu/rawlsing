#!/usr/bin/env python3
"""ONE local bounded q217-only aggregate check through the exact SRC04 grant gate.

The program decodes the exact granted SRC04 file, but emits only:
  - exact source/config/grant pins,
  - q217 raw-code counts and physical missing states.
It never emits respondent rows, identifiers, combinations, values by row, or
arbitrary samples. No source bytes are written.
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMPLEMENTER = HERE.parents[1]
MP = IMPLEMENTER.parent / "MEASUREMENT_PREP"
GATE = MP / "WORKER_RETURNS" / "ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118"
sys.path.insert(0, str(IMPLEMENTER))
sys.path.insert(0, str(GATE))

from existing_grant_binding import (  # exact dbeada9 route, no edits
    ConfigBinding, ExternalTrust, ExistingGrantResolver, bind_existing_grant,
)
from rawlsing_next.pre553_r157_projection_adapter import decode_with_source_read_permission


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "evidence" / "q217_aggregate.json"))
    ap.add_argument("--config", default=str(IMPLEMENTER / "WORKER_RETURNS/ANVIL_ALL35_C11_INPUTS_20261118/inputs/SRC04/source.config.repaired.v2.json"))
    ap.add_argument("--gate-dir", default=str(GATE))
    args = ap.parse_args()
    gate = Path(args.gate_dir)
    config_path = Path(args.config)
    # Exact config is loaded only through the accepted current validator.
    from rawlsing_next.pre553_r157_projection_adapter import canonical_config_hash, load_source_config
    cfg = load_source_config(config_path)
    if cfg.source_id != "SRC04" or cfg.active_source_sha256 != "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18":
        raise SystemExit("CONFIG_IDENTITY_DRIFT")
    if sha(config_path) != "5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5":
        raise SystemExit("CONFIG_FILE_DRIFT")
    if canonical_config_hash(cfg) != "28630f26b491dcbce411667e3ad285ea42b40abf2d0176056a8a15d1ecad768d":
        raise SystemExit("CONFIG_CANONICAL_DRIFT")
    slot = [x for x in cfg.document.get("physical_slots", []) if x.get("name") == "q217"]
    if len(slot) != 1:
        raise SystemExit("Q217_SLOT_NOT_EXACT")
    raw = json.loads((gate / "fixtures" / "SRC04_CONFIG_BINDING.json").read_text())
    config_binding = ConfigBinding(
        **{k: v for k, v in raw.items() if k != "metadata_freeze_refs"},
        metadata_freeze_refs=tuple(raw["metadata_freeze_refs"]),
    )
    trust = ExternalTrust(**{
        k: json.loads((gate / "TRUST_POLICY.json").read_text())[k]
        for k in ("grant_sha256", "grant_path", "config_file_sha256",
                  "config_canonical_sha256", "config_binding_sha256")
    })
    grant_path = gate / "fixtures" / "SRC04_FULL_SOURCE_GRANT.json"
    bound = bind_existing_grant(grant_path=grant_path, config=config_binding, trust=trust)
    resolver = ExistingGrantResolver(grant_path, trust, bound.request)
    grant_doc = json.loads(grant_path.read_text())
    source_path = grant_doc["source_path"]
    incidence = decode_with_source_read_permission(
        source_path=source_path, request=bound.request, resolver=resolver,
    )
    try:
        codes = Counter()
        states = Counter()
        labels = Counter()
        var = next((v for v in incidence.variables if v.name == "q217"), None)
        if var is None:
            raise SystemExit("Q217_COLUMN_NOT_FOUND")
        for batch in incidence.iter_batches(batch_size=100_000):
            for cell in batch:
                if cell.variable_name != "q217":
                    continue
                key = repr(cell.raw_value)
                codes[key] += 1
                states[cell.missing_state.value] += 1
                labels[repr(cell.raw_value_label)] += 1
        total = sum(codes.values())
        if total != incidence.row_count:
            raise SystemExit(f"Q217_COVERAGE_DRIFT:{total}!={incidence.row_count}")
        payload = {
            "schema": "ANVIL_SRC04_Q217_AGGREGATE_CHECK@1",
            "sourcefree_test_only": False,
            "source_id": "SRC04",
            "wave": "I",
            "source_path_sha256": incidence.source_sha256,
            "source_rows": incidence.row_count,
            "source_columns": len(incidence.variables),
            "config": {
                "path": "rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json",
                "commit": "da23c65d1e211cb7e8ce416e98757f321b78d25e",
                "file_sha256": sha(config_path),
                "canonical_sha256": canonical_config_hash(cfg),
                "q217_labels": slot[0].get("value_labels"),
                "q217_missing_declarations": slot[0].get("missing_declarations"),
            },
            "grant": {
                "commit": "303a57851785557fff8229e29a5554717168cbd1",
                "sha256": sha(grant_path),
                "route_commit": "dbeada9a272ff94a9bff68cf4352b6f1e5a01594",
                "route_module": "MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118/existing_grant_binding.py",
                "request_digest": bound.request_digest,
                "status": bound.status,
            },
            "q217": {
                "column_ordinal": var.ordinal,
                "observed_rows": total,
                "codes": {k: codes[k] for k in sorted(codes, key=lambda x: (len(x), x))},
                "missing_states": {k: states[k] for k in sorted(states)},
                "label_occurrences": {k: labels[k] for k in sorted(labels)},
                "labels_declared": var.value_labels,
                "missing_declarations": var.missing_declarations,
            },
            "output_scope": "CODES_AND_COUNTS_ONLY__NO_RESPONDENT_RECORDS_IDS_COMBINATIONS_OR_VALUES_BY_ROW",
            "source_read_performed": True,
            "respondent_records_emitted": False,
        }
        Path(args.out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(json.dumps({"status": "Q217_AGGREGATE_OK", "rows": total, "codes": payload["q217"]["codes"], "states": payload["q217"]["missing_states"]}, sort_keys=True))
    finally:
        incidence.close()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
