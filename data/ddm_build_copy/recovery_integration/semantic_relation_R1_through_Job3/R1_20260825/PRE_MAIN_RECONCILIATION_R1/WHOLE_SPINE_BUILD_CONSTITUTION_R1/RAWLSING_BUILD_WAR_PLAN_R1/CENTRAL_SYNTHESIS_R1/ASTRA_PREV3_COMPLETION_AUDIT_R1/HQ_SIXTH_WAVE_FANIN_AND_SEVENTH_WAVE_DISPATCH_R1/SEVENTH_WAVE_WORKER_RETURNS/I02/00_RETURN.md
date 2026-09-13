# I02 — learned-world canonical I03 target-resolution repair and real re-execution R1 — governed return

Status:

`PASS__CANONICAL_I03_TARGET_RESOLUTION_REPAIR_AND_FULL_FROZEN_50_77_REAL_REEXECUTION_COMPLETE__LEARNED_POSITIVE_WORKLOAD_GATE_REMAINS_BLOCKED`

Exact grain:

`PREV3_LEARNED_WORLD_CANONICAL_I03_TARGET_RESOLUTION_REPAIR_AND_REAL_REEXECUTION_R1_ONLY`

Branch:

`agent/rabochii-prev3-w7-i02-learned-i03-repair-r1`

Commission tip:

`c318dfacdeabd900dd8ed35ff464398da9fb1e0c`

Final branch tip is reported externally after this sealing commit resolves; this artifact does not claim its own circular commit identity.

## Holding

I02 closes H02's qualified implementation defect without changing the frozen learned frontier or inventing a semantic rescue for LiTS-I q301 values.

Accepted AS2B source authority already establishes that q301 raw codes `6` and `7` are `SOURCE_SPECIFIC_SPECIAL`, not automatic DK/IAP, while physical system missing remains separately typed. Canonical PRE553 I03 requires:

`raw_resolved_target_support != raw_denominator_support => UNRESOLVED`

Accordingly, I02 does **not** recode `6/7`, drop denominator members, widen the frozen target domain, mutate the frontier, or proceed to semantic validation when a required query role is unresolved.

The repair/re-execution grain itself therefore PASSes, because the implementation now obeys canonical I03 and the entire frozen workload was truthfully re-executed. That PASS is **not** a positive learned-world qualification. The inherited positive-control gate remains blocked because P0 has `0/5` supported candidates after lawful target resolution.

Downstream gate state:

`BLOCKED__NO_P0_SUPPORTED_AFTER_CANONICAL_I03_REPAIR`

## Exact source and authority

Exact Library carrier:

- file: `LITS-2006-data.dta`
- Library id/version: `file_0000000036dc81f8b8b546e356590a03 / 1`
- bytes: `139531180`
- SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- rows / variables: `29002 / 1198`

Frozen/accepted authority remained:

- D02 authority commit: `40cb8585f076a66d9884b99022a59bb909606c03`
- D02 frontier blob: `5399a3f64642c8d9f8a0644db0adc15d38642971`
- F02 return: `482bb884a99e31ba77e904d0df39fffc872cbed3`
- F02 release hash: `bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297`
- F02 frontier readoption: `07c6175b1d3828f8dc8763c51f3eb44a3cba6812bb128d4f0b84ffc5096cb851`
- G02 frozen preexecution seal: `ca47c52f925b126878cd9e0be433bd6a28bec5a8623784bfbf5eaf7523b21bea`
- canonical I03 blob: `e2d91984541df7c692a1b2f32370500838a2a000`
- accepted AS2B source/C11 authority commit: `923f2c00b6145182a5e2be5038f579845951da19`

F02 q310/q311 selector counts and all six selector roots replayed exactly.

## Exact q301 target-resolution facts

For `q301_2`:

- native 1..5 counts: `4377, 6440, 5226, 6972, 1882`
- source-specific special 6/7: `1774 / 2327`
- system missing: `4`
- denominator: `29002`
- resolved frozen substantive target support: `24897`
- unresolved denominator members: `4105`

For `q301_7`:

- native 1..5 counts: `2889, 6112, 6511, 10334, 2479`
- source-specific special 6/7: `224 / 442`
- system missing: `11`
- denominator: `29002`
- resolved frozen substantive target support: `28325`
- unresolved denominator members: `677`

For the frozen q301_2 × q301_7 5×5 joint target:

- denominator: `29002`
- fully resolved target configurations: `24630`
- unresolved denominator members: `4372`

These exact facts reproduce the canonical I03 reason H02 rejected G02's P0 treatment.

## Full frozen re-execution

Frozen membership was preserved exactly:

- candidates: `50 / 50`
- query-role executions: `77 / 77`
- P0: `5 / 5`
- P1: `1 / 3`
- P2: `18 / 36`
- P3: `1 / 8`
- P4: `25 / 25`

Query fact states after canonical resolution:

- `SUPPORTED = 1`
- `UNRESOLVED = 76`
- `ZERO_SUPPORT = 0`

Candidate terminal states:

- `EVALUATED_UNRESOLVED = 50`

P0:

- supported candidates: `0 / 5`
- all five are `EVALUATED_UNRESOLVED` because the required q301_2/A000 role resolves `24897 / 29002` target configurations.

The sole fully resolved query role is one P2 condition:

`A1V5 AND Q310V3 AND Q311V2 -> q301_7`

with `38 / 38` resolved. Its P2 candidate still terminates `EVALUATED_UNRESOLVED` because the frozen q301_7/A000 baseline role is `28325 / 29002` and therefore canonical `UNRESOLVED`.

No observed outcome was removed or used to alter the frontier.

## Deterministic real replay

Two fresh Python processes executed the exact carrier and produced byte-identical outputs:

- full output bytes: `108824`
- full output SHA-256: `9ae0002a5b2eaa8c63081289dfeb823de3fd76ec5d41a39a9b0819b401b18cfb`
- semantic replay hash: `9f21f1e6f68ee929299f1f25a73d6719c4a141c0b01d7746b53c71ed2fe7222e`
- 77-role ledger root: `a86550b88cc3ea250ec74d11d98f84703af47dc7be1fe2bcb965fa8dae9e55a5`
- 50-candidate ledger root: `d174cb8c5dffa479b68253d54f9b1e59727c1c30719b1c76774fa069ade0a28d`

## Implementation and tests

Repair implementation:

- path: `rawlsing_next/prev3_learned_i03_repair_r1.py`
- commit: `fb724c0d910dde30b7c711c1fac46bf830557e85`
- blob: `c2550207ffa76469282f747002520987cad81343`

Qualification test:

- path: `rawlsing_next/tests/test_prev3_learned_i03_repair_r1.py`
- commit: `57e348ddce2fc5a5496e03462c19fb074e15c584`
- blob: `4644c9461a27ee54e59b32d6883e90262106f02b`

Inherited G02 invariant suite was also rerun unchanged:

- blob: `129e350915ba3401690eccdfadf6b9acf779bee4`

## Governed court

Temporary PR `#366` was used only to trigger the governed bounded court and was closed unmerged.

- workflow: `Rabochii Governed Bounded Court`
- run: `34787701925`
- job: `103806093826`
- semantic candidate: `e6e437292ccb4baf26aeccb9ca925715b73f581b`
- evidence execution SHA: `ee02c0280d1b43a78ba540872edb673d28c230d3`
- Python: `3.12.14`
- determinism: `EXACT`
- bounded court: `21 passed in 0.22s`
- protocol self-test: `20 passed in 0.11s`
- result: `PASS`
- artifact id: `10327022717`
- artifact digest: `sha256:5ebf4aaa7d02ba70de8cae07ccb8b28de268a86d577035a62ab5d688ee853e51`

The temporary `.rabochii/court_spec.json` was removed after court completion.

## Governed return artifacts

- `01_REAL_REEXECUTION_AND_REPLAY_RECEIPT.json`
- `02_CANONICAL_I03_REPAIR_AUTHORITY_RECEIPT.json`
- `03_ROLE_SIGNATURE_AND_LANE_ACCOUNTING.json`
- `04_TEST_AND_COURT_RECEIPT.json`

## Scope and mutation audit

I02 performed no:

- denominator deletion after observing results;
- q301 `6/7` recoding;
- target-domain widening to manufacture resolution;
- frontier membership mutation;
- post-data selector substitution;
- pruning, ranking, scoring or top-k selection;
- structural admission;
- causal promotion;
- population generalization;
- person-state construction;
- V3 construction;
- MAIN or PRE-MAIN mutation.

PRE-V3 remains objective-world only.

## Disposition

I02 result:

`I02_PASS__CANONICAL_I03_TARGET_RESOLUTION_REPAIR_AND_FULL_50_77_REAL_REEXECUTION_COMPLETE__76_QUERY_ROLES_UNRESOLVED__1_SUPPORTED__50_CANDIDATES_EVALUATED_UNRESOLVED__ZERO_FRONTIER_MUTATION__LEARNED_POSITIVE_WORKLOAD_GATE_BLOCKED_NO_P0_SUPPORTED__RETURN_TO_HQ`

Return to HQ for exact successor disposition. I02 does not self-authorize a new positive-control semantics, structural admission, or independent qualification lane.
