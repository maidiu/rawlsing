# Accepted ASTRA-D04-R2 Substantive Truth Inventory

## Adjudication of the proposed list

The proposed list is **necessary but incomplete**.

It correctly identifies the core outcome facts, but substantive conservation also needs the exact workload identity/mapping that gives those values meaning, the accepted R2/R7/R27 risk-set composition, and the F02 selector/conditioning facts present in the accepted source/replay receipt. Without those, identical terminal labels or even identical isolated values can be attached to a semantically drifted conditioning regime.

## Immutable accepted evidence

Read from accepted ASTRA-D04-R2 return branch:

- `01_TYPED_LEARNED_EMPIRICAL_PRODUCT.json`
- `02_77_ROLE_EXECUTION_RECEIPT.json`
- `03_SOURCE_AND_REPLAY_RECEIPT.json`
- `00_RETURN.md`

Accepted product identity:
`47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d`

Accepted semantic replay identity:
`301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5`

Accepted source:
- SHA `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- rows 29,002
- variables 1,198

Accepted frontier:
- 50 candidates
- 77 query roles
- frontier seal `ca47c52f925b126878cd9e0be433bd6a28bec5a8623784bfbf5eaf7523b21bea`

Accepted lane accounting:
- P0: 5 candidates / 5 roles
- P1: 1 candidate / 3 roles
- P2: 18 candidates / 36 roles
- P3: 1 candidate / 8 roles
- P4: 25 candidates / 25 roles
- total: 50 / 77

Accepted role execution:
- 77/77 role states = `SUPPORTED`
- role-result reuse count = 0
- final candidate terminal counts = 49 `EVALUATED_SUPPORTED`, 1 `EVALUATED_VALID_EMPTY`
- the sole valid-empty candidate is P3.

## R2 / R7 / R27 risk-set truth

Exact roots/counts:

- R2: count **24,897**, root `f224533ce0a705bf0839e6bb40bd49dec0c8366e5a5ede0a389e3e67811a13b3`
- R7: count **28,325**, root `0978bd4d87afd88831593ca5977fa9978948d598bf981adfd7fd96ceab979844`
- R27: count **24,630**, root `f9c87f610bcaf0539cc91e7f2608b230cea39d806d3611d6a398519a86386d29`

Exact role/risk composition:
- P0 + q301_2 marginal → R2
- q301_7 marginal + P2 + P3 → R7
- P1 joint + P4 → R27
- no predictor-missingness denominator rule was added.

This mapping is substantive because a numerically identical support under a different governed denominator is not the same empirical claim.

## F02 selector/conditioning premises that must not drift

Accepted source/replay evidence additionally records the conditioning populations:

### q310
Counts:
- 1 → 12,340
- 2 → 7,511
- 3 → 9,085
- MISSING → 66

row root:
`a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455`

selector roots:
- 1 → `0a62f6f0e3d78b429022b95c2594a3fcbf053b8af588f0ceb304ac3dafe700d2`
- 2 → `0bad1e397f5b74b6136ba82e8d81fc608d1df7124e6ff043048cc5cd91ef9c83`
- 3 → `b477bf705a93bb672d9ae670a1daa38013c2aa2841d0c506f722ab1bbdbb2f3d`
- MISSING → `810a81a5663c05dcd0e2f4c2c972f66dc16e7446c87054bb412242632dc57348`

### q311
Counts:
- 1 → 16,582
- 2 → 4,548
- 3 → 7,826
- MISSING → 46

row root:
`af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa`

selector roots:
- 1 → `bffb9d2e9da447a27aaf7c8f889a07d5c47389a58ad933d3ea9867f83e127869`
- 2 → `43ffb4ef1de60354b9c943135fd0f31ee54d31edbcd3bb6abf147e5bff1dce1f`
- 3 → `642a70ba00a4f7292d96267647068c3bfc83f5efc75451ce00a7df4cd2d62837`
- MISSING → `847c4e89a7336a5cb5ac6d73953b87091640231ba7cd5c5376e37044a12a03fb`

Where current machinery produces the same canonical root domain, these roots are lawful equality comparands. If current representation changes root schema, compare normalized membership/selector facts rather than forcing cross-schema hash equality.

## P0 — five exact supports/denominators

All terminal `EVALUATED_SUPPORTED`, all denominator R2 = 24,897:

| target q301_2 cell | support |
|---:|---:|
| 1 | 4,377 |
| 2 | 6,440 |
| 3 | 5,226 |
| 4 | 6,972 |
| 5 | 1,882 |

The parity object must bind target-cell identity to support; the unordered multiset is insufficient.

## P1 — exact joint-dependence witness

Accepted first dependence witness:
- cell: `[1,1]`
- joint: `1485 / 24630`
- marginal q301_2: `4377 / 24897`
- marginal q301_7: `2889 / 28325`

P1 candidate:
`38f4e2...66d34` in the accepted product.

The exact witness, not merely terminal support, must be conserved.

## P2 — 18 exact conditioned first-difference witnesses

Every P2 candidate is terminal supported. Baseline q301_7 cell 1 is always:
`2889 / 28325`.

Exact conditioned witnesses:

| q301_2 | q310 | q311 | conditioned support / denominator |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 352 / 1191 |
| 1 | 1 | 2 | 59 / 195 |
| 1 | 1 | 3 | 39 / 137 |
| 1 | 2 | 1 | 188 / 584 |
| 1 | 2 | 2 | 212 / 541 |
| 1 | 2 | 3 | 67 / 210 |
| 1 | 3 | 1 | 123 / 381 |
| 1 | 3 | 2 | 53 / 143 |
| 1 | 3 | 3 | 387 / 931 |
| 5 | 1 | 1 | 16 / 906 |
| 5 | 1 | 2 | 1 / 66 |
| 5 | 1 | 3 | 5 / 41 |
| 5 | 2 | 1 | 10 / 222 |
| 5 | 2 | 2 | 10 / 115 |
| 5 | 2 | 3 | 4 / 47 |
| 5 | 3 | 1 | 6 / 170 |
| 5 | 3 | 2 | 0 / 38 |
| 5 | 3 | 3 | 13 / 247 |

Parity must preserve:
- exact candidate identity;
- q301_2/q310/q311 condition tuple;
- target cell;
- exact conditioned numerator/denominator;
- exact baseline numerator/denominator;
- the canonical first-difference witness selection.

A candidate can remain “supported” after the first witness moves; terminal support is therefore insufficient.

## P3 — exact valid-empty reason

P3 candidate is the **one** accepted valid-empty result. Target q301_7 native cell = 5.

Exact fractions:
- POOLED_NEG: `206/4327`
- POOLED_POS: `595/1854`
- Q310V1_NEG: `81/1523`
- Q310V1_POS: `366/1013`
- Q310V2_NEG: `50/1337`
- Q310V2_POS: `29/96`
- Q310V3_NEG: `5/97`
- Q310V3_POS: `16/65`

Signs:
- pooled sign = `+1`
- stratum signs = `[+1,+1,+1]`

Therefore the reversal predicate is false for the accepted empirical reason: pooled and strata point the same way. “VALID_EMPTY” alone is not parity.

## P4 — exact keyed 5×5 support matrix

All 25 cells are supported. Exact cell→support:

| q301_2 \ q301_7 | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|
| 1 | 1485 | 976 | 873 | 787 | 206 |
| 2 | 555 | 2139 | 1543 | 1910 | 229 |
| 3 | 305 | 1029 | 1647 | 1841 | 347 |
| 4 | 232 | 1103 | 1439 | 3458 | 672 |
| 5 | 65 | 201 | 274 | 719 | 595 |

The matrix is keyed. A permutation of supports across cell labels is a parity failure even though all 25 remain supported and the multiset of supports is unchanged.

## Candidate identities and mapping law

The accepted ASTRA product partitions exactly 50 candidate identities across P0/P1/P2/P3/P4. Current parity must compare the exact candidate identity attached to each lane/parameter/cell fact, not just “50 unique hashes.”

Likewise, 77 roles must preserve exact candidate→query-role→risk-set semantics. `02_77_ROLE_EXECUTION_RECEIPT.json` additionally proves:
- P0=5, P1=3, P2=36, P3=8, P4=25 roles;
- all 77 role states supported;
- role-result reuse count zero.

## What is not itself substantive empirical equality

The following are important provenance/immutability anchors but are not replacements for empirical parity:
- ASTRA product hash;
- ASTRA semantic replay hash;
- candidate receipt ledger hash;
- role receipt ledger hash;
- decoder blob/version;
- run byte hashes;
- authority commit/blob hashes.

Verify them in their own domains. Do not use them as a shortcut for current-vs-ASTRA normalized fact equality.

## Minimum normalized parity object

Before LiTS oracle freeze, current neutral execution should deterministically normalize and compare at least:

1. source identity/shape;
2. exact frontier seal + exact candidate identities and lane/parameter mapping;
3. exact 77 role mapping and role states;
4. R2/R7/R27 counts/roots/composition;
5. q310/q311 selector counts and, when same-domain, selector roots;
6. P0 target→support/denominator;
7. P1 exact first dependence witness;
8. all 18 P2 exact conditioned first-difference witnesses + baseline;
9. P3 exact target, eight fractions, pooled/stratum signs, terminal valid-empty;
10. P4 exact keyed 25-cell matrix;
11. final 49/1 terminal counts.

Only after this comparison passes may the current object identities be frozen as the current oracle's identities.
