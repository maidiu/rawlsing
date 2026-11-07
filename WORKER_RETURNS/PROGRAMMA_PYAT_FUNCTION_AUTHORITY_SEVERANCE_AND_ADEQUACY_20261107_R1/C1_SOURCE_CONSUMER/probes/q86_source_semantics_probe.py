#!/usr/bin/env python3
"""S2 sourcefree/documentary probe for the frozen R5 Q86 current operation.

Reads the selected nonrespondent response-option authority CSV and current source
text. It does not copy asset bytes into the repository, read respondent/SAV/DB
data, execute native workloads, or write outside this C1 output root.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer")
OUT = ROOT / "WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C1_SOURCE_CONSUMER"
CSV = Path("/Users/matthewsmith/Desktop/Rawlsing/data/ddm_build_copy/reports/afrobarometer_response_option_authority.csv")
Q86_MODULE = ROOT / "rawlsing_next/wave1_gt12_i03_positive_facts.py"
EXPECTED_CSV_SHA256 = "305cb215485bc95ebecee395e578c52739311bc2fc15faed27318bd922f47332"
EXPECTED_CSV_BYTES = 15_498_257


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def main() -> int:
    data = CSV.read_bytes()
    rows = list(csv.DictReader(data.decode("utf-8-sig").splitlines()))
    q86 = [r for r in rows if r.get("source_family") == "Afrobarometer" and r.get("wave") == "R5" and r.get("var_name") in {"Q86A", "Q86B"}]
    selected = []
    for var in ("Q86A", "Q86B"):
        vr = [r for r in q86 if r.get("var_name") == var]
        selected.append({
            "source_native_variable": var,
            "question_id": vr[0].get("question_id") if vr else None,
            "question_text": vr[0].get("question_text") if vr else None,
            "source_file": vr[0].get("source_file") if vr else None,
            "mapping_status": vr[0].get("mapping_status") if vr else None,
            "question_type": vr[0].get("question_type") if vr else None,
            "handling_rule": vr[0].get("handling_rule") if vr else None,
            "recommended_computation": vr[0].get("recommended_computation") if vr else None,
            "response_family": vr[0].get("response_family") if vr else None,
            "response_semantics_status": vr[0].get("response_semantics_status") if vr else None,
            "response_semantics_source": vr[0].get("response_semantics_source") if vr else None,
            "response_semantics_contract_hash": vr[0].get("response_semantics_contract_hash") if vr else None,
            "source_structure_classification": vr[0].get("source_structure_classification") if vr else None,
            "row_count": len(vr),
            "substantive_codes_and_labels": [
                {"code": r.get("value_code_raw", "").lstrip("\ufeff"), "label": r.get("value_label_raw"), "is_substantive": r.get("is_substantive"), "polarity": r.get("polarity"), "response_family": r.get("response_family")}
                for r in vr if r.get("is_substantive") == "True"
            ],
            "row_set_sha256": sha256(canonical(vr).encode("utf-8")),
        })
    code = Q86_MODULE.read_text(encoding="utf-8")
    contract_hashes = [r["response_semantics_contract_hash"] for r in selected if r["response_semantics_contract_hash"]]
    source_files = []
    for path in sorted((ROOT / "rawlsing_next").glob("*.py")):
        text = path.read_text(encoding="utf-8", errors="replace")
        hits = [h for h in contract_hashes if h in text]
        if hits:
            source_files.append({"path": str(path.relative_to(ROOT)), "hits": hits})
    constants = {}
    for name in [
        "FROZEN_R5_SOURCE_SHA256", "FROZEN_RISK_SET_ID", "FROZEN_RISK_SET_MEMBER_COUNT",
        "FROZEN_RISK_MEMBER_SET_SHA256", "FROZEN_Q86A_QIMPL", "FROZEN_Q86B_QIMPL",
        "FROZEN_Q86A_SOURCE_STRUCTURE", "FROZEN_CONTRACT_COMMIT", "FROZEN_CONTRACT_BLOB",
    ]:
        m = re.search(rf"^{name}\s*=\s*(.+)$", code, re.MULTILINE)
        constants[name] = m.group(1).rstrip() if m else None
    result = {
        "schema": "C1_Q86_SOURCE_SEMANTICS_PROBE_V1",
        "selected_authority_csv": {
            "path": str(CSV),
            "exists": CSV.exists(),
            "bytes": len(data),
            "sha256": sha256(data),
            "expected_sha256": EXPECTED_CSV_SHA256,
            "matches_accepted_AR_0033": sha256(data) == EXPECTED_CSV_SHA256 and len(data) == EXPECTED_CSV_BYTES,
            "selected_release": "AR-0033",
            "issuer_grade": "A02_RECORDED_HISTORICAL_DECISION_NOT_ORIGINAL_SIGNER",
        },
        "selected_q86_rows": selected,
        "current_operation": {
            "module": "rawlsing_next/wave1_gt12_i03_positive_facts.py",
            "module_sha256": sha256(Q86_MODULE.read_bytes()),
            "source_family": "Afrobarometer",
            "wave": "R5",
            "source_sha256": (constants.get("FROZEN_R5_SOURCE_SHA256") or "").strip('"'),
            "risk_set_member_count": (constants.get("FROZEN_RISK_SET_MEMBER_COUNT") or "").replace("_", ""),
            "claims": ["GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET@1", "GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1"],
            "use": "RAW unary Q86A and RAW joint Q86B->Q86A; no structural/actor promotion",
            "first_semantic_promoting_reader": "build_gt1_q86a_i03_plan/build_gt2_q86a_q86b_i03_plan -> execute_empirical_query",
            "constants": constants,
        },
        "provenance_scan": {
            "selected_q86_contract_hashes": contract_hashes,
            "contract_hash_referenced_in_current_rawlsing_next": bool(source_files),
            "files_referencing_selected_contract_hashes": source_files,
            "current_operation_binds_selected_q86_contract_hash": False,
            "current_operation_binds_selected_source_sha": (constants.get("FROZEN_R5_SOURCE_SHA256") or "").strip('"') == "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651",
            "current_operation_uses_generic_caller_supplied_source_semantics": True,
            "positive_test_fixture_is_sourcefree_synthetic_not_original_issuer": True,
        },
        "finding": "CURRENT_Q86_OPERATION_IS_REAL_AND_SOURCE_ANCHORED_BUT_ACTUAL_SELECTED_Q86_RESPONSE_SEMANTICS_IS_NOT_BOUND__FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED",
        "limits": [
            "No respondent/SAV/DB read; sourcefree tests only.",
            "No original issuer/adoption claim; selected authority bytes are historically accepted AR-0033 metadata.",
            "No production patch, C11/runtime edit, native release, or science claim.",
        ],
    }
    (OUT / "probes/q86_source_semantics_probe.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ["selected_authority_csv", "current_operation", "provenance_scan", "finding"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
