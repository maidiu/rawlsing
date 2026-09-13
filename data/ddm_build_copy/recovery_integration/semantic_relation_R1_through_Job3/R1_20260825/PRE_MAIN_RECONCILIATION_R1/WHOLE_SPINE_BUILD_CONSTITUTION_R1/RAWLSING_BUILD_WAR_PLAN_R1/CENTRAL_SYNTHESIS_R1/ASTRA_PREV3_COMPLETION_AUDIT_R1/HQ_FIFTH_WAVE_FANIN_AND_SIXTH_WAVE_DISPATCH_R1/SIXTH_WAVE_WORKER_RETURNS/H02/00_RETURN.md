# H02 — independent qualification of real LiTS-I learned-world execution R1 — governed return

Status:
`BLOCKED__G02_P0_TARGET_RESOLUTION_DIVERGES_FROM_CANONICAL_I03__29002_DENOMINATOR_VS_28787_RESOLVED_Q301_2_TARGET_SUPPORT__REQUIRED_5_OF_5_POSITIVE_CONTROL_NOT_QUALIFIED`

Exact grain:
`PREV3_LEARNED_WORLD_REAL_EXECUTION_INDEPENDENT_QUALIFICATION_R1_ONLY`

Branch:
`agent/rabochii-prev3-w6-h02-learned-independent-qual-r1`

Commission tip:
`1247d8e6a5b10ed47046410cfdde15efd7cfe2f3`

Producer reviewed:
`agent/rabochii-prev3-w5-g02-learned-real-execution-r2` at terminal tip `01e1e8071ea98587dfbb755ec0fdc0da2f5e1663`.

## Holding

H02 rejects independent qualification of G02's claimed learned-world PASS at the smallest required positive-control seam. The exact LiTS-I carrier and F02 q310/q311 selector replay are correct, but G02's P0 execution semantics diverge from the canonical I03 target-resolution contract.

D02 freezes q301_2's source-native substantive target domain to values `1..5` and excludes source-native specials `6/7`. On the exact LiTS-I carrier, q301_2 contains:

- 1 = 4,501
- 2 = 7,141
- 3 = 6,460
- 4 = 7,631
- 5 = 3,054
- 6 = 137
- 7 = 62
- system missing = 16

Therefore:

- condition-selected P0 denominator under `A000` = `29,002`
- resolved rows in the frozen q301_2 substantive target domain 1..5 = `28,787`
- denominator members without a resolved target configuration = `215`

G02's `_query` implementation counts every condition-selected row in `raw_denominator_support`, while its q301_2 target projection emits only cells 1..5. Its P0 validator then treats positive cell counts as `EVALUATED_SUPPORTED` without rejecting incomplete target resolution.

Canonical I03 at the exact H02 ancestry does the opposite: denominator membership is recorded before target resolution, and when `raw_resolved_target_support != raw_denominator_support` the fact state is exactly `UNRESOLVED` with detail `positive denominator exists but exact target configuration is unresolved for one or more denominator members`.

Thus the five required P0 positive controls cannot lawfully be qualified as G02's `EVALUATED_SUPPORTED` receipts. Because commission PASS requires P0 5/5 positive controls, this is the smallest exact global PASS blocker. H02 does not continue into speculative repair or rewrite the remaining lane outcomes.

## Independent source attack

Exact carrier:

- Library file id: `file_0000000036dc81f8b8b546e356590a03`
- version: `1`
- name: `LITS-2006-data.dta`
- bytes: `139531180`
- SHA-256: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- rows / variables: `29002 / 1198`

Independent direct-carrier replay reproduced F02 exactly:

- q310 row root: `a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455`
- q311 row root: `af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa`
- all six q310/q311 selector roots: exact match

The defect is therefore not source identity, q310/q311 selector resolution, or F02 carrier replay.

## Producer evidence preserved

H02 found no need to dispute the producer's static preexecution membership evidence:

- frozen candidates: `50`
- frozen query roles: `77`
- preexecution seal: `ca47c52f925b126878cd9e0be433bd6a28bec5a8623784bfbf5eaf7523b21bea`
- no post-data frontier mutation proven by this attack

Those facts do not cure the P0 target-resolution defect.

## Authority boundary

H02 has zero repair authority. It performed no:

- G02 production-code repair;
- frontier mutation;
- selector substitution;
- validator mutation;
- ranking or pruning;
- structural admission;
- causal promotion;
- population generalization;
- person-state construction;
- V3 construction;
- MAIN or PRE-MAIN mutation.

PRE-V3 remains objective-world only.

## Governed artifacts

- `01_INDEPENDENT_HOSTILE_REPLAY_MATRIX.json`
- `02_SOURCE_AND_SELECTOR_REPLAY_RECEIPT.json`
- independent qualification test: `rawlsing_next/tests/test_prev3_learned_real_execution_independent_qualification_h02.py`

Court/test receipt will be sealed after the bounded independent court and does not change this semantic holding.

## Disposition

Return the exact blocker to HQ. Any cure belongs to a separately commissioned competent producer/repair lane. H02 does not specify or implement a repair beyond identifying the exact semantic mismatch.

Terminal marker:

`H02_BLOCKER__G02_REQUIRED_P0_5_OF_5_POSITIVE_CONTROL_NOT_INDEPENDENTLY_QUALIFIED__CANONICAL_I03_REQUIRES_UNRESOLVED_FOR_29002_DENOMINATOR_VS_28787_RESOLVED_Q301_2_TARGET_SUPPORT__ZERO_REPAIR_AUTHORITY__RETURN_TO_HQ`
