# I05 HOSTILE ACCEPTANCE CONTRACT — AUTHORITY 37 / G04 R1

Status: `PREPARED__PRODUCTION_INDEPENDENT__ANSWER_LEAKAGE_GUARDED__CURRENT_INTEGRATION_FAIL_CLOSED`

## Exact authority and oracle binding

- Authority 37: `data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/37_ORIGINARY_FRACTURE_MAP_FULL_JOIN_AND_IMPLEMENTATION_AUTHORITY.md`
  - Git blob: `48c0860ff2d7548ff2fa98d20021149aa2049953`
- Frozen G04 hostile-oracle return commit: `8620265b95f5b3bf8c210674a7735e0ce8dac88c`
- Frozen G04 fixture:
  - `data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/ORIGINARY_FRACTURE_MAP_COURT_R1/G04_HOSTILE_ORACLE/SYNTHETIC_RESPONDENTS.csv`
  - Git blob: `4e535ac553e3e58d29390c94c964535b050a51a0`
  - SHA-256: `83c496c9482c2e9736a6797e243965110899c1aa97436d752795b15d483a8215`
  - logical digest: `e4ef71ccf3815b0734013a5ebf1c85f9f3ac94720b30f2c5cf6285aa784a0017`
- Frozen answer-side oracle files:
  - `EXPECTED_FRACTURE_MAP.json` — blob `8f17d399b46f4ccef0614fbbadf59dab3a089bde`
  - `EXPECTED_COSIGNATURES.json` — blob `fb1c87ac1fb8064d91298678717d697258311ddf`
  - `EXPECTED_BRANCH_DETERMINICITY.csv` — blob `f84c92d85638d0a2c2558471b14fc3b45a4d1fcf`
  - `NEGATIVE_AND_STOP_ORACLE.csv` — blob `b3f98354f92bdc2d4f56e12e5ae402d2e2bab1fc`
  - `PAIRWISE_FAILURE_ORACLE.md` — blob `340848ea61a211057ea9863ff8a663778477333b`

The oracle-side files are never copied into the future controller seed.

## Seed / oracle separation

The future controller seed is built from the G04 source fixture and Authority-37 controller policy only.

Permitted seed material:

1. governed root response surface `TARGET_MULTISELECT`;
2. exact respondent/source rows and replay keys;
3. governed coordinate/source authority;
4. complete available source response fields without designating any one as a cotravel target;
5. weighting, eligibility and typed response-state fields;
6. controller policy parameters.

Forbidden seed material includes expected modal pattern, a winner/primary predictor, branch IDs or memberships, secondary-predictor answers, grandchild route answers, cotravel target answers, expected determinicity results, expected stop outcomes, expected higher-order result, and expected selective-invalidation result.

The frozen G04 `segment` column is specifically **derived answer material**. `hostile_acceptance_adapter.py` removes it before seed construction and rejects any seed in which it remains.

`SOURCE_DATA != EXPECTED_ANSWER`

`SOURCE_COORDINATE_AUTHORITY != WINNING_PREDICTOR`

`AVAILABLE_RESPONSE_SURFACE != COTRAVEL_TARGET_ANSWER`

## Hostile acceptance assertions

A future Authority-37 controller adapter must canonically project its result to `I05_HOSTILE_ACCEPTANCE_ACTUAL_R1`. The harness compares that projection with the independently frozen G04 oracle and therefore freezes all of the following acceptance obligations:

1. modal and exact multi-label response-pattern morphology;
2. all four P fracture quadrants;
3. distinct branch-specific Q, R and S secondary structure;
4. depth > 1 recursion using actual discovered-parent membership;
5. global C1/C2 negative relation versus positive branch-conditioned relation;
6. non-identifiability of exact multi-label morphology from presence marginals;
7. exact three-way XOR structure despite null pairwise association;
8. stable supported minority preservation;
9. underpowered and valid-empty terminal states;
10. substantive `NONE` distinct from missing/refused/not-applicable/unknown;
11. deterministic replay identity and digest;
12. selective invalidation: the single permitted R perturbation changes R-dependent topology only.

The canonical answer-side comparison uses the complete `EXPECTED_FRACTURE_MAP.json`, `EXPECTED_COSIGNATURES.json`, and `EXPECTED_BRANCH_DETERMINICITY.csv`; the additional G04 negative/stop and pairwise documents remain exact dependency witnesses.

## Hostile policy

The hostile synthetic fixture uses its frozen test-policy threshold `minimum_split_raw_n=3`; this is a controller-policy input, not an answer. The future harness also binds `maximum_depth=4`, `maximum_target_arity_J=3`, exhaustive governed pattern/coordinate enumeration, typed-negative exclusion from boolean complements, stopped-branch retention, and nonadaptive within-invocation frontiers.

This hostile-fixture policy does not silently rewrite Authority 37's ordinary production defaults.

## Future integration entrypoint

`hostile_acceptance_adapter.py` is the production-independent entrypoint.

Future HQ integration supplies:

- the exact G04 source fixture path;
- the exact G04 oracle directory;
- an adapter command that invokes the joined production controller and emits a canonical `I05_HOSTILE_ACCEPTANCE_ACTUAL_R1` JSON.

Invocation shape:

```text
python hostile_acceptance_adapter.py   --fixture-csv <G04/SYNTHETIC_RESPONDENTS.csv>   --oracle-dir <G04_HOSTILE_ORACLE>   --production-adapter-command "<future HQ adapter>"
```

The future adapter command receives `--seed-json <path>` and `--output-json <path>`. This layer intentionally does not import or prescribe I01-I04 implementation internals.

## Current fail-closed law

No Authority-37 production controller integration surface exists on the launch branch. Therefore omission of `--production-adapter-command` returns exit code `42` with:

`FAIL_CLOSED__PRODUCTION_CONTROLLER_ADAPTER_ABSENT`

That state is required today and is **not** a hostile-acceptance pass.

Prep completion and future production acceptance are distinct:

`PREP_COMPLETE != PRODUCTION_ACCEPTANCE_PASS`
