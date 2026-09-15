from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import base64
import zlib
from collections import Counter

from rawlsing_next import n04_r2_whole_corpus_t03_release as n04r2
from rawlsing_next import n04_r3_carrier_specific_production_binding as n04r3

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
RETURN_ROOT = (
    REPO_ROOT
    / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3"
    / "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1"
    / "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1"
    / "ASTRA_PREV3_COMPLETION_AUDIT_R1"
    / "POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1"
    / "PSC_FIRST_ACTIVE_WAVE_R1/WORKER_RETURNS/N04-R4B"
)

N02_COMMIT = "b01c5620c592274fa9acd0eab1c9ef38e79071a3"
N02_MANIFEST_PATH = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "ASTRA_PREV3_COMPLETION_AUDIT_R1/"
    "POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1/"
    "PSC_FIRST_ACTIVE_WAVE_R1/WORKER_RETURNS/N02-R2/"
    "01_AUTHORITY_AND_LEDGER_MANIFEST.json"
)
N02_CANONICAL_ROW_JSONL_SHA256 = (
    "0f0b367275c931efec69918a82a1b78355f6b6050b6c2017990061578bef6ad0"
)
N04_R3_COMMIT = "8e0266703bbf3b060abcd6fbe53c7ef6c49062c5"
RESPONSE_BINDING_BLOB = "ef77bcbe61385a10fe28b67c15a13f4f794e58e0"
SELECTED_ACCOUNTING_PATH = RETURN_ROOT / "02_SELECTED_159_ROUTING_ACCOUNTING.jsonl.zlib.b64"

ROUTING_STATE = "UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY"
PREDECESSOR_STATUS = "BLOCKED_CURRENT_POSITIVE__MISSING_ROUTING_APPLICABILITY_REF"
BINDING_DISPOSITION = "PRESERVE_UNRESOLVED__NO_APPLICABLE_CURRENT_ROUTING_REF_BOUND"


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _response_row_number(refs: list[str], qid: str) -> int:
    matches = [
        ref
        for ref in refs
        if ref.startswith(
            f"V550_V551_RESPONSE_SEMANTICS_BINDING@{RESPONSE_BINDING_BLOB}:"
        )
    ]
    assert len(matches) == 1, (qid, matches)
    marker = ":rows="
    assert marker in matches[0], (qid, matches[0])
    raw = matches[0].split(marker, 1)[1]
    assert "," not in raw, (qid, raw)
    return int(raw)


def build():
    accounting, _raw_vector, _vector_b64, _frontier, predecessor_summary = n04r3.build()
    selected_ids = sorted(
        row["question_implementation_id"]
        for row in accounting
        if row["binding_status"] == PREDECESSOR_STATUS
    )
    assert len(selected_ids) == 159
    assert len(set(selected_ids)) == 159

    ledger, _n03_vector, n03_summary = n04r2._load_n03_r2_replay()
    by_id = {row["question_implementation_id"]: row for row in ledger}
    assert len(by_id) == 18276

    n02_manifest = json.loads(n04r2._git_bytes(N02_COMMIT, N02_MANIFEST_PATH))
    assert n02_manifest["ledger"]["canonical_row_jsonl_sha256"] == N02_CANONICAL_ROW_JSONL_SHA256
    assert n02_manifest["ledger"]["rows"] == 18276
    assert n02_manifest["ledger"]["unique_ids"] == 18276

    records = []
    authority_code_counts = Counter()
    state_counts = Counter()
    for qid in selected_ids:
        source = by_id[qid]
        assert source["top_level_disposition"] == "CURRENT_GOVERNED_POSITIVE"
        assert source["response_binding_count"] == 1
        assert source["routing_disposition"] == ROUTING_STATE
        assert source["routing_scope"] == ""
        authority_code = source["routing_authority_code"]
        assert authority_code in n02_manifest["authorities"]
        authority_code_counts[authority_code] += 1
        state_counts[ROUTING_STATE] += 1

        response_row_number = _response_row_number(source["top_level_authority_refs"], qid)
        registry_indices = source["response_registry_key_indices"]
        assert len(registry_indices) == 1, (qid, registry_indices)

        records.append(
            {
                "question_implementation_id": qid,
                "source_family": source["source_family"],
                "wave": source["wave"],
                "source_variable_code": source["source_variable_code"],
                "response_semantics_ref": (
                    f"V550_V551_RESPONSE_SEMANTICS_BINDING@{RESPONSE_BINDING_BLOB}:"
                    f"row={response_row_number}"
                ),
                "v551_registry_key_index": int(registry_indices[0]),
                "n02_r2_routing_row_ref": f"N02-R2@{N02_COMMIT}:qid={qid}",
                "routing_state": ROUTING_STATE,
                "routing_applicability_ref": None,
                "typed_residual": "routing_applicability_ref",
            }
        )

    canonical = b"".join(
        (
            json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
        for record in records
    )
    id_stream = ("".join(qid + "\n" for qid in selected_ids)).encode("utf-8")

    committed_b64 = SELECTED_ACCOUNTING_PATH.read_bytes().strip()
    committed = zlib.decompress(base64.b64decode(committed_b64))
    assert committed == canonical

    summary = {
        "selected_rows": 159,
        "unique_selected_ids": 159,
        "selected_sorted_id_stream_sha256": sha256(id_stream),
        "selected_accounting_jsonl_bytes": len(canonical),
        "selected_accounting_jsonl_sha256": sha256(canonical),
        "preserved_state_counts": {
            "APPLICABLE_OR_CURRENT_ROUTING_REF_BOUND": 0,
            "GOVERNED_KNOWN_ABSENCE_OR_NONAPPLICABILITY": 0,
            "OUTSIDE_ROUTING_BEARING_JURISDICTION": 0,
            ROUTING_STATE: 159,
        },
        "routing_applicability_refs_bound": 0,
        "typed_residual_counts": {"routing_applicability_ref": 159},
        "routing_authority_code_counts": dict(sorted(authority_code_counts.items())),
        "predecessor_terminal": predecessor_summary["terminal"],
        "n03_ledger_canonical_jsonl_sha256": n03_summary["ledger_canonical_jsonl_sha256"],
        "n02_canonical_row_jsonl_sha256": N02_CANONICAL_ROW_JSONL_SHA256,
        "terminal": (
            "PASS__N04_R4B_159_ROUTING_STATES_ACCOUNTED__"
            "ZERO_APPLICABLE_CURRENT_REFS__159_UNRESOLVED_PRESERVED"
        ),
    }
    return records, summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-jsonl", type=pathlib.Path)
    args = parser.parse_args()
    records, summary = build()
    if args.emit_jsonl:
        args.emit_jsonl.write_text(
            "".join(
                json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                + "\n"
                for record in records
            ),
            encoding="utf-8",
        )
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
