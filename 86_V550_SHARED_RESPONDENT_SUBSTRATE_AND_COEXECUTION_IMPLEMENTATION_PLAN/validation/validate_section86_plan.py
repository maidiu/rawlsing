#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path

SECTION = Path(__file__).resolve().parents[1]
REQUIRED = [
    'README_FIRST.md','ARCHITECTURE_DECISION.md','CODEX_IMPLEMENTATION_INSTRUCTIONS.md',
    'EXACT_IMPLEMENTATION_SEQUENCE.md','ACCEPTANCE_GATES.md','CURRENT_STATE.json',
    'contracts/SHARED_RESPONDENT_SUBSTRATE_CONTRACT.md',
    'contracts/CLI_STORAGE_AND_RESUME_CONTRACT.md',
    'manifests/FILE_CHANGE_MAP.csv','validation/TEST_AND_MUTATION_MATRIX.csv'
]

def main() -> int:
    missing=[p for p in REQUIRED if not (SECTION/p).exists()]
    state=json.loads((SECTION/'CURRENT_STATE.json').read_text())
    changes=list(csv.DictReader((SECTION/'manifests/FILE_CHANGE_MAP.csv').open(encoding='utf-8',newline='')))
    tests=list(csv.DictReader((SECTION/'validation/TEST_AND_MUTATION_MATRIX.csv').open(encoding='utf-8',newline='')))
    checks={
        'required_files_present': not missing,
        'status_ready': state.get('status')=='PASS_IMPLEMENTATION_PLAN_READY',
        'real_execution_not_authorized': state.get('real_respondent_execution_authorized') is False,
        'full_generation_not_authorized': state.get('full_35_wave_generation_authorized') is False,
        'file_change_map_nonempty': len(changes)>=10,
        'test_matrix_nonempty': len(tests)>=40,
        'privacy_package_mutation_present': any(r.get('id')=='M16' for r in tests),
        'one_query_test_present': any(r.get('id')=='T17' for r in tests),
        'no_db_test_present': any(r.get('id')=='T22' for r in tests),
    }
    payload={
        'status':'PASS' if all(checks.values()) else 'FAIL',
        'checks':checks,
        'missing_files':missing,
        'file_change_count':len(changes),
        'test_matrix_count':len(tests),
    }
    (SECTION/'validation/SECTION86_VALIDATION_RETURN.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload,indent=2))
    return 0 if payload['status']=='PASS' else 1

if __name__=='__main__':
    raise SystemExit(main())
