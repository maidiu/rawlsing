#!/usr/bin/env python3
"""C11 Q3/F08 exact historical authority -> unchanged consumer replay.

S2 test-time replay only. Reads exact nonrespondent authority rows and stages
the exact historical code from 9ba4764 under the C11 lease; no respondent,
source SAV/DTA/DB, native, science or production data is read.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer")
OUT = ROOT / "WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C11_Q3_F08_FIRST_CONSUMER_EFFECT"
REPLAY = OUT / "replay_src"
A47 = REPLAY / "data/ddm_build_copy/manifests/question_wave_itinerary.csv"
A48 = REPLAY / "data/ddm_build_copy/manifests/question_use_overrides.csv"
A50 = REPLAY / "data/ddm_build_copy/manifests/question_type_taxonomy.yaml"
A49 = Path("/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_Authority_Document_Archive_2026-08-24/documents/ledgers-registries-and-matrices/data/ddm_build_copy/manifests/question_structure_register.csv")

sys.path.insert(0, str(REPLAY))
import pandas as pd
from data.ddm_build_copy.ddm_v550_question_use import (
    build_question_use_contract,
    load_question_use_overrides,
    load_question_wave_itinerary,
)
from data.ddm_build_copy.ddm_v550_source_structure import (
    load_question_structure_register,
    match_source_structure_row,
)
from data.ddm_build_copy.build_question_structure_register import load_taxonomy


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


def row_key(row: dict) -> dict:
    keys = [
        "source", "canonical_wave", "question_id", "var_code", "semantic_role",
        "manual_override_used", "manual_override_basis", "manual_override_reason",
        "itinerary_review_priority", "itinerary_manual_designation_required",
        "source_structure_classification", "source_structure_source",
        "source_structure_fields_joined", "allowed_as_response_distribution",
        "allowed_as_v551_relation_evidence", "review_required", "disallowed_reason",
        "question_use_contract_hash",
    ]
    return {k: row.get(k) for k in keys}


def main() -> int:
    assert sha(A47) == "866eb3ab25fbd9479781c15a0aecbb00a9d547fdc947cc443e8b904262b86eb3"
    assert sha(A48) == "29e7706b7467f9435e57e78a7c8cf1314d9760f03d4d14d2bcf0d54f51809479"
    assert sha(A49) == "15f7b5613b7cb106c2d2db233925891d5392917b66eee19c1a5eff8e0655585b"
    assert sha(A50) == "3612c6b400008467471b71cc38d811b8c5349bac0617e974a72e76e584e86b27"

    reg = load_question_structure_register(A49)
    assert len(reg) == 18792
    selected = reg[
        reg["source"].astype(str).eq("GSS")
        & reg["wave"].astype(str).eq("1973")
        & reg["var_name"].astype(str).eq("uswar")
    ]
    assert len(selected) == 1
    selected_row = selected.iloc[0].to_dict()
    structure, join_key, join_confidence = match_source_structure_row(selected_row, reg)
    question = {
        **selected_row,
        **structure,
        "source": "GSS",
        "source_family": "GSS",
        "wave": "1973",
        "canonical_wave": "1973",
        "question_id": selected_row["question_id"],
        "var_code": selected_row["var_name"],
        "var_name": selected_row["var_name"],
    }

    def contract(overrides=A48, itinerary=A47):
        frame = build_question_use_contract(
            pd.DataFrame([question]),
            question_use_overrides_path=Path(overrides),
            wave_itinerary_path=Path(itinerary),
        )
        assert len(frame) == 1
        return frame.iloc[0].to_dict()

    positive = contract()
    positive_summary = row_key(positive)
    positive_hash = stable(positive_summary)

    # Exact selected rows and their direct loader behavior.
    overrides = load_question_use_overrides(A48)
    itineraries = load_question_wave_itinerary(A47)
    override_match = overrides[
        overrides["source"].astype(str).eq("GSS")
        & overrides["wave"].astype(str).eq("1973")
        & overrides["var_code"].astype(str).eq("uswar")
    ]
    itinerary_match = itineraries[
        itineraries["source"].astype(str).eq("GSS")
        & itineraries["wave"].astype(str).eq("1973")
    ]
    assert len(override_match) == 1 and len(itinerary_match) == 1
    selected_override = override_match.iloc[0].to_dict()
    selected_itinerary = itinerary_match.iloc[0].to_dict()

    # Missing selected override: exact authority removed from disposable copy.
    missing_override_path = OUT / "tmp/question_use_overrides_missing.csv"
    with A48.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
        fields = list(rows[0])
    selected_raw_override = next(
        r for r in rows
        if r.get("source") == "GSS" and r.get("wave") == "1973" and r.get("var_code") == "uswar"
    )
    kept = [r for r in rows if r is not selected_raw_override]
    with missing_override_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(kept)
    missing = contract(overrides=missing_override_path)
    missing_summary = row_key(missing)

    # Duplicate selected override: exact conflict must raise, not choose.
    duplicate_path = OUT / "tmp/question_use_overrides_duplicate.csv"
    with duplicate_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows + [selected_raw_override])
    try:
        contract(overrides=duplicate_path)
        duplicate_result = "NO_EXCEPTION"
    except Exception as exc:
        duplicate_result = f"{type(exc).__name__}: {exc}"

    # Missing structure register: actual source-structure consumer fallback.
    fallback_structure, fallback_key, fallback_confidence = match_source_structure_row(
        question, pd.DataFrame()
    )
    fallback_frame = build_question_use_contract(
        pd.DataFrame([{**question, **fallback_structure}]),
        question_use_overrides_path=A48,
        wave_itinerary_path=A47,
    )
    fallback_contract = fallback_frame.iloc[0].to_dict()
    # Wrong itinerary: disposable copy without the exact GSS 1973 row.
    missing_itinerary_path = OUT / "tmp/question_wave_itinerary_missing_gss1973.csv"
    with A47.open(newline="", encoding="utf-8") as fh:
        itinerary_rows = list(csv.DictReader(fh))
        itinerary_fields = list(itinerary_rows[0])
    kept_i = [r for r in itinerary_rows if not (r.get("source") == "GSS" and r.get("wave") == "1973")]
    with missing_itinerary_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=itinerary_fields)
        writer.writeheader()
        writer.writerows(kept_i)
    no_itinerary = contract(itinerary=missing_itinerary_path)
    no_itinerary_summary = row_key(no_itinerary)

    # Taxonomy is an actual register-builder consumer; it has no QUC runtime path.
    taxonomy = load_taxonomy()
    taxonomy_single = taxonomy.get("single_choice", {})

    restored = contract()
    restored_hash = stable(row_key(restored))

    result = {
        "schema": "C11_Q3_F08_HISTORICAL_CONSUMER_REPLAY_V1",
        "execution_kind": "S2_TEST_TIME_HISTORICAL_REPLAY__NOT_ORIGINAL_HISTORICAL_RUN",
        "authority_pins": {
            "AR-0047": {"path": "data/ddm_build_copy/manifests/question_wave_itinerary.csv", "sha256": sha(A47), "bytes": A47.stat().st_size},
            "AR-0048": {"path": "data/ddm_build_copy/manifests/question_use_overrides.csv", "sha256": sha(A48), "bytes": A48.stat().st_size},
            "AR-0049": {"path": str(A49), "sha256": sha(A49), "bytes": A49.stat().st_size},
            "AR-0050": {"path": "data/ddm_build_copy/manifests/question_type_taxonomy.yaml", "sha256": sha(A50), "bytes": A50.stat().st_size},
        },
        "historical_code_pin": {
            "commit": "9ba4764bef551b1ce498e5772d60b73d69337d4b",
            "module": "data/ddm_build_copy/ddm_v550_question_use.py",
            "module_sha256": sha(REPLAY / "data/ddm_build_copy/ddm_v550_question_use.py"),
            "source_structure_module": "data/ddm_build_copy/ddm_v550_source_structure.py",
            "source_structure_module_sha256": sha(REPLAY / "data/ddm_build_copy/ddm_v550_source_structure.py"),
            "entrypoint": "build_question_use_contract -> build_question_use_contract_row",
            "selector_functions": ["load_question_use_overrides", "load_question_wave_itinerary", "_select_override", "_select_itinerary"],
        },
        "selected_row": {
            "source": "GSS", "wave": "1973", "question_id": selected_row["question_id"], "var_code": "uswar",
            "ar0048_override": selected_override,
            "ar0047_itinerary": selected_itinerary,
            "ar0049_structure_join": {"join_key": join_key, "join_confidence": join_confidence, "classification": structure.get("source_structure_classification"), "fields_joined": structure.get("source_structure_fields_joined")},
        },
        "positive": {"summary": positive_summary, "output_hash": positive_hash},
        "selected_rows": {
            "ar0048_override_count": len(overrides),
            "ar0047_itinerary_count": len(itineraries),
            "ar0049_register_rows": len(reg),
            "ar0050_question_types": sorted(taxonomy),
            "ar0050_single_choice": taxonomy_single,
        },
        "negative": {
            "missing_override": missing_summary,
            "duplicate_override": duplicate_result,
            "missing_structure_register": {"fallback": fallback_structure, "join_key": fallback_key, "confidence": fallback_confidence, "contract_summary": row_key(fallback_contract), "output_hash": stable(row_key(fallback_contract))},
            "missing_itinerary": no_itinerary_summary,
        },
        "restore": {"summary": row_key(restored), "output_hash": restored_hash, "matches_positive": restored_hash == positive_hash},
        "authority_effect": {
            "positive_manual_override_used": positive.get("manual_override_used"),
            "positive_semantic_role": positive.get("semantic_role"),
            "positive_itinerary_priority": positive.get("itinerary_review_priority"),
            "positive_structure_classification": positive.get("source_structure_classification"),
            "taxonomy_runtime_effect": "NO_QUC_READER_IN_CURRENT_PATH__REGISTER_BUILDER_ONLY",
        },
        "execution_limits": [
            "Test-time replay now, not evidence that the original historical run occurred.",
            "Uses exact selected nonrespondent authority rows and exact historical code only.",
            "No source/respondent/SAV/DTA/DB read, no native scientific execution.",
            "AR-0050 taxonomy is loaded by the historical register-builder consumer; the QUC contract entrypoint does not load it directly.",
            "No substitution of source-authored authority semantics with a hardcoded fixture.",
        ],
    }
    (OUT / "probes/q3_f08_replay.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
