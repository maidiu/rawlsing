#!/usr/bin/env python3
"""D01 source-free contract tripwire. Run only on an authorized checked-out tree.

Usage: python3 WORKER_RETURNS/PYAT-HQ280-PV3-D01-OBJECTIVE-FIELD-DEMAND-CONSUMER-R1/repro/check_d01_contracts.py .
This is a static source check, not a source/semantic permission, runtime/pytest or proof of world occupancy.
"""
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
TESTS = {
 "rawlsing_next/field_forge_conditional_support.py": {
   "bounded_family": r"EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1\.0\.0",
   "native_conditioner": r'CONDITIONER_SOURCE_NATIVE_VARIABLE\s*=\s*"Q86B"',
   "native_target": r'TARGET_SOURCE_NATIVE_VARIABLE\s*=\s*"Q86A"',
   "producer_exists": r"def produce_exact_conditional_support_profile\(",
 },
 "rawlsing_next/gt12_e2b_publication_governance_binding.py": {
   "sig004": r"GT12_V554_SIG004_ADMITTED_RELATION_CONTEXT_PUBLICATION_RULE",
   "context_only": r'V557_ALLOWED_USES\s*=\s*\("CONTEXT",\)',
 },
 "rawlsing_next/prev3_objective_position_v557_v558_publication.py": {
   "bounded_proving_fact": r"fact\.fact_ref\.object_id != PROVING_FACT_ID",
   "first_consumer": r"def resolve_bound_objective_position_context\(",
 },
 "rawlsing_next/sdtf_r4_world_response_redrive.py": {
   "no_d1_mint": r"NO_D1_FACT_MINTING",
   "request_not_result": r"def request_r4_invalidation_rederivation\(",
 },
 "rawlsing_next/sdtf_r4_mechanism_rule_authority_binding.py": {
   "classes": r"P1_MATERIAL_ACCESS_DEPENDENCY",
   "current_rule_gate": r"def require_current_rule_admission\(",
 },
}
count=0
for rel, cases in TESTS.items():
    src=(ROOT / rel)
    if not src.is_file():
        raise SystemExit(f"MISSING_OWNER_FILE: {rel}")
    body=src.read_text(encoding="utf-8")
    for name, pattern in cases.items():
        if not re.search(pattern, body):
            raise SystemExit(f"FAIL {rel} :: {name}")
        print(f"PASS {rel} :: {name}")
        count+=1
print(f"STATIC_ONLY_PASS {count}; no runtime/world/grant claim")
