# I03 — AUTHORITY-37 EXACT J=3 TARGET TOPOLOGY IMPLEMENTATION R1

Repository: `maidiu/rawlsing`
Branch: `agent/verkhovod-fracturemap-i03-j3-topology-r1`
Exact launch base before this command: `9bafaf2cb96cc3fb46fef6785d486f08987ab71c`

## Read first
Authority 37; L03 real-data result; G03 audit; D04 design; current `EmpiricalQuerySpec`, I03 query execution, I05 validation/discovery, response topology, replay, typed-state tests.

## Assignment
Implement the smallest exact extension required for Authority-37 `maximum_target_arity_J = 3` under explicit versioned authority.

Requirements:
- do not weaken existing J<=2 semantics or tests;
- canonical exact target-triple ordering/deduplication;
- exact same-respondent 3-target joint cells/pattern membership;
- distinct source/risk, branch, per-target and three-way joint denominators;
- preserve source-native response semantics, multiplicity and typed special states;
- raw and governed-weighted supports remain separate;
- deterministic query/fact/replay identity;
- exact fail-closed behavior when authority J ceiling < requested arity or J>3;
- no composition of pairwise outputs may masquerade as J=3;
- tests with a three-way configuration whose every pairwise margin is information-insufficient, including XOR/parity-style fixture;
- compatibility with branch-conditioned query predicates.

Keep the change minimal and common. Do not implement controller target enumeration or fracture-map traversal here.

## Return
Write `RESULT.md`, `RESULT.json`, `TEST_RECEIPT.txt`, `J3_OBJECT_COMPATIBILITY.md`, `CHANGED_FILES.txt`, `EXACT_REF_LEDGER.csv` under I03.

Success token:
`I03_AUTH37_J3_TOPOLOGY_R1_COMPLETE`
