# I01 — FRACTURE-MAP POLICY / RECEIPT CONTRACT IMPLEMENTATION R1

Repository: `maidiu/rawlsing`
Branch: `agent/verkhovod-fracturemap-i01-policy-objects-r1`
Exact launch base before this command: `9bafaf2cb96cc3fb46fef6785d486f08987ab71c`

## Read first
1. `37_ORIGINARY_FRACTURE_MAP_FULL_JOIN_AND_IMPLEMENTATION_AUTHORITY.md`
2. Authority 35 and Authority 36A/preliminary join surfaces referenced by Authority 37.
3. L01, L04, L05, D02, D03 exact returns named by Authority 37.
4. Current `rawlsing_next/pre553_empirical_objects.py`, discovery/query/replay object law and tests.

## Assignment
Implement only the Authority-37 controller policy/object/receipt contract surface. Do NOT implement the controller traversal itself and do NOT modify I05 candidate evaluation semantics.

Required implementation:
- a versioned controller policy object carrying at least `minimum_split_raw_n=50`, `minimum_report_raw_n=25`, `maximum_depth=4`, and the exact policy authority/ref identity;
- exact controller continuation dispositions and terminal stop reasons required by Authority 37/D03, preserving producer typed states rather than replacing them;
- `EmpiricalFractureMapReceipt@1.0.0` as a ref-only aggregate semantic/replay receipt, containing no copied empirical payload and no actor/V3 semantics;
- deterministic canonical serialization/hash identity and strict validation;
- explicit PRE-V3 noninference firewall fields/contracts where needed;
- tests proving deterministic identity, retention != recursion, typed-state preservation, policy-version sensitivity, no copied payload, and replay-safe refs.

Use existing common exact object patterns wherever possible. Do not create `FractureMapNode`, `BranchObject`, stage courier bundles, or a new empirical warehouse.

## Noninterference
- no controller traversal;
- no J=3 query-engine modification;
- no co-signature enumeration implementation;
- no A/B/C or MX04 decision;
- no V3 work.

## Return
Under `.../ORIGINARY_FRACTURE_MAP_IMPLEMENTATION_R1/I01_POLICY_OBJECTS/` write `RESULT.md`, `RESULT.json`, `TEST_RECEIPT.txt`, `CHANGED_FILES.txt`, `EXACT_REF_LEDGER.csv`.

Return exact final commit and test counts.

Success token:
`I01_FRACTURE_MAP_POLICY_OBJECTS_R1_COMPLETE`
