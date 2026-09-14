#!/usr/bin/env python3
"""Machine-readable checks for the PRE-V3 source-state disposition contract."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
HELPER = ROOT / "tools" / "prev3_source_state_target_disposition.py"
FIXTURE = ROOT / "evidence" / "fixtures" / "prev3_source_state_target_disposition_fixture.json"
RECEIPT = ROOT / "evidence" / "receipts" / "PREV3_EMPIRICAL_SOURCE_STATE_TO_PRODUCT_TARGET_DISPOSITION_CONTRACT_R1.json"
NOTE = ROOT / "evidence" / "validation" / "prev3" / "PREV3_EMPIRICAL_SOURCE_STATE_TO_PRODUCT_TARGET_DISPOSITION_CONTRACT_R1.md"

spec = importlib.util.spec_from_file_location("prev3_source_state_contract", HELPER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

checks = []


def check(check_id, condition, detail):
    if not condition:
        raise AssertionError(f"{check_id}: {detail}")
    checks.append({"check_id": check_id, "status": "PASS", "detail": detail})


resolved = fixture["resolved_case"]
unresolved = fixture["unresolved_case"]

first = module.audit_record(resolved["records"][0])
second = module.audit_record(resolved["records"][1])
first_raw = first["audit_trail"][0]["value"]
second_raw = second["audit_trail"][0]["value"]
first_semantic = first["audit_trail"][1]["value"]["semantic_state"]
second_semantic = second["audit_trail"][1]["value"]["semantic_state"]
check(
    "same_native_code_source_local_divergence",
    first_raw["native_state"] == second_raw["native_state"] == 7
    and first_raw["source_id"] != second_raw["source_id"]
    and first_semantic != second_semantic,
    "same native numeric state is retained across two synthetic sources while governed meanings remain source-local",
)

unresolved_audit = module.audit_record(unresolved["records"][0])
check(
    "governed_state_may_remain_unresolved",
    unresolved_audit["audit_trail"][1]["value"]["authority_id"].startswith("SYNTHETIC_AUTHORITY_")
    and unresolved_audit["audit_trail"][2]["value"] == module.UNRESOLVED,
    "an explicitly governed source-local state may still have unresolved target disposition",
)

gate = module.denominator_resolution_check(unresolved)
blocked = False
try:
    module.emit_empirical_result(unresolved)
except module.ContractError:
    blocked = True
check(
    "unresolved_blocks_empirical_result",
    gate["passed"] is False and blocked,
    "empirical result emission is forbidden before the concrete target gate passes",
)

result = module.emit_empirical_result(resolved)
expected = resolved["expected"]
check(
    "arithmetic_after_gate_only",
    result["denominator_resolution_check"]["passed"] is True
    and result["numerator"] == expected["numerator"]
    and result["denominator"] == expected["denominator"]
    and result["value"] == expected["value"],
    "numerator and denominator are emitted only with an attached passing gate",
)
check(
    "excluded_state_absent_from_denominator",
    result["excluded"] == expected["excluded"]
    and result["denominator"] == 2
    and len(resolved["records"]) == 3,
    "excluded record is audited but does not enter the denominator",
)

all_source_ids = [
    record["raw_source_state"]["source_id"]
    for case_name in ("resolved_case", "unresolved_case")
    for record in fixture[case_name]["records"]
]
check(
    "synthetic_only_source_identifiers",
    all(value.startswith("SYNTHETIC_SOURCE_") for value in all_source_ids),
    "fixture uses synthetic source identifiers only",
)

expected_stages = [
    module.RAW_SOURCE_STATE,
    module.SOURCE_LOCAL_GOVERNED_STATE,
    module.PRODUCT_TARGET_DISPOSITION,
]
check(
    "auditable_stage_sequence",
    [entry["stage"] for entry in first["audit_trail"]] == expected_stages
    and gate["stage"] == module.DENOMINATOR_RESOLUTION_CHECK
    and result["stage"] == module.EMPIRICAL_RESULT,
    "all five contract stages are explicit and independently inspectable",
)

artifact_paths = [HELPER, FIXTURE, HERE, RECEIPT, NOTE]
banned = ("dri" + "ver", "ty" + "pe", "person" + "-terminal")
violations = []
for path in artifact_paths:
    text = path.read_text(encoding="utf-8").lower()
    for token in banned:
        if token in text:
            violations.append(f"{path.relative_to(ROOT)}:{token}")
check(
    "new_artifacts_free_of_prohibited_legacy_vocabulary",
    not violations,
    "new contract artifacts contain none of the prohibited legacy vocabulary",
)

output = {
    "contract_id": fixture["contract_id"],
    "status": "PASS",
    "checks": checks,
}
json.dump(output, sys.stdout, indent=2, sort_keys=True)
sys.stdout.write("\n")
