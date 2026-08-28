# WORKER COMMAND — G02 CURRENT COMMON/I05 FRACTURE-MAP CAPABILITY AUDIT

Role: `VOZHD TRII — GITHUB-ONLY CURRENT IMPLEMENTATION AUDIT`

Repository: `maidiu/rawlsing`
Branch: `agent/verkhovod-fracturemap-g02-current-i05-audit-r1`
Starting authority: Authority 35.

## Mission

Audit the current accepted common PRE553/I05 implementation against all 20 Authority35 clauses. Determine what the runtime can actually represent and execute today, including the newly accepted MX01R2 recursive handoff, without repairing anything.

## Required scope

Inspect current accepted implementations and tests for:
- common empirical objects and exact query engine;
- I05 bounded discovery/candidate grammar;
- validation evidence/status handling;
- MX01R2 recursive handoff;
- routing/risk-set/source semantics;
- multi-select topology support;
- respondent membership and same-respondent laws;
- typed negative states;
- any current branch-level determinicity, modal/minority classification, residual search, or co-signature products.

## Required questions

For every Authority35 requirement R01-R20 classify:
- `EXECUTABLE_AND_TESTED`
- `REPRESENTABLE_NOT_GENERATED`
- `PARTIAL`
- `MISSING_COMMON_CONTRACT`
- `MISSING_CONTROLLER/GENERATOR`
- `BLOCKED_MISSING_AUTHORITY`
- `NOT_CURRENT_JURISDICTION`

Pay special attention to whether current I05 requires caller-predeclared predicates/candidate grammars versus discovering branch roles itself.

Do not mistake MX01R2's N->N+1 transport closure for autonomous fracture-map discovery.

## Required outputs

- `RESULT.md`
- `RESULT.json`
- `AUTH35_CURRENT_CAPABILITY_MATRIX.csv`
- `CURRENT_OBJECT_AND_EXECUTOR_MAP.md`
- `REPRESENTABLE_VS_AUTONOMOUS_GENERATION.csv`
- `NEGATIVE_STATE_COVERAGE.csv`
- `CURRENT_TEST_EVIDENCE_LEDGER.csv`
- `MINIMUM_GAP_STATEMENT.md`
- `EXACT_REF_LEDGER.csv`
- `CHANGED_FILES.txt`

## Prohibitions

No production code changes. No new tests that smuggle in missing semantics. No sibling findings. No architecture selection. No V3 work.

Success token:
`G02_CURRENT_I05_FRACTURE_MAP_AUDIT_R1_COMPLETE`
