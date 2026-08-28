# I08 — INDEPENDENT FRACTURE-MAP ANTI-CHEAT / REPLAY VALIDATION PREP R1

Repository: `maidiu/rawlsing`
Branch: `agent/verkhovod-fracturemap-i08-independent-validation-prep-r1`
Exact launch base before this command: `9bafaf2cb96cc3fb46fef6785d486f08987ab71c`

Read Authority 37, G04/G05, L02/L03, D01-D04. Remain sibling-blind to I01-I07 implementation findings.

Design and, where production-independent, implement the independent validation surface that HQ will run after integrating I01-I04.

It must detect:
- caller/oracle leakage of modal response, predictor, branch membership, secondary splitters, grandchild path or cotravel targets;
- partial-result mutation of an already-open I05 frontier;
- score/top-k/prevalence pruning of lawful candidates;
- `NOT P` swallowing missing predictor values;
- substantive `NM` swallowing DK/refusal/missing/inapplicable;
- pairwise projection being mislabeled as J=3;
- branch membership privately reconstructed instead of exact handoff/replay;
- retention loss when recursion stops;
- nondeterministic frontier/map/replay identity;
- actor/V3/personality leakage;
- irrelevant determinant mutation invalidating unrelated topology;
- relevant determinant mutation failing to invalidate descendants.

Prepare a merge-independent validation contract and tests/stubs that can be pointed at the integrated implementation later. No production semantics changes.

Return `RESULT.md`, `RESULT.json`, `INDEPENDENT_VALIDATION_MATRIX.csv`, `ANTI_CHEAT_CONTRACT.md`, `TEST_RECEIPT.txt`, `CHANGED_FILES.txt`.

Success token: `I08_INDEPENDENT_FRACTURE_MAP_VALIDATION_PREP_R1_COMPLETE`
