# MX01 Recursive Topology Closure R1 — Fixture Specification

Status: `FIXTURE_FROZEN__EXECUTION_STOPS_AT_RECURSIVE_HANDOFF_GAP`

This is a candidate-neutral PRE-V3 synthetic respondent fixture. It is not an A/B/C carrier benchmark and contains no V3 actor semantics.

## 1. Respondent universe

Eight exact scoped respondents are used. `PARENT` is an exact derived branch cohort containing R1–R6; R7–R8 are outside that parent.

| respondent | PARENT | X | H | Y | Z |
|---|---:|---:|---:|---:|---:|
| R1 | 1 | 1 | 1 | 1 | 1 |
| R2 | 1 | 1 | 1 | 0 | 0 |
| R3 | 1 | 1 | 0 | 1 | 0 |
| R4 | 1 | 1 | 0 | 0 | 1 |
| R5 | 1 | 0 | 1 | 1 | 1 |
| R6 | 1 | 0 | 0 | 0 | 0 |
| R7 | 0 | 1 | 1 | 1 | 0 |
| R8 | 0 | 0 | 0 | 0 | 1 |

All response/coordinate evaluation is same-respondent and exact-ref scoped.

## 2. Required recursive path

### Generation 0 — parent

`PARENT = {R1,R2,R3,R4,R5,R6}`

The parent must be represented as an exact governed `DERIVED_BRANCH_COHORT`, not as a question-level label.

### Generation 1 — discovered child

Condition inside `PARENT` on `X=1`:

`CHILD = PARENT AND X=1 = {R1,R2,R3,R4}`

The child must be produced by discovery as a canonical predicate/branch result whose exact immediate parent is `PARENT`.

### Generation 2 — grandchild

Condition the discovered `CHILD` on `H=1`:

`GRANDCHILD = CHILD AND H=1 = {R1,R2}`

The generation-2 operation must consume the generation-1 branch through a governed recursive handoff. Pre-authoring `GRANDCHILD` independently from the original fixture does not satisfy recursive child discovery.

## 3. Branch-conditioned same-respondent cotravel

Within `GRANDCHILD`, condition on response `Y=1` and query response `Z`.

- `GRANDCHILD` baseline Z distribution: `{0:1, 1:1}`.
- `GRANDCHILD AND Y=1`: only R1, therefore Z=`1` with support 1.
- The conditional distribution differs from the grandchild baseline and must be `DISCOVERED_RESULT_SUPPORTED` when the minimum-support rule permits support 1.

This is cross-question same-respondent cotravel conditioned on an actual recursive branch cohort.

## 4. Superficially similar unconditional lookalike

Across the full eight-respondent universe, condition on `Y=1` and query `Z`.

- `Y=1` members are R1,R3,R5,R7.
- Their Z distribution is `{0:2, 1:2}`.
- The full-universe Z distribution is also `{0:4, 1:4}`.

Therefore the unconditional/pairwise lookalike is `VALID_EMPTY` for distribution difference while the recursive grandchild-conditioned cotravel is supported. A successor that returns the same answer for both has lost branch conditioning.

## 5. Typed-negative lanes

### Valid empty

The unconditional `Y=1 -> Z` lookalike above must terminate as exact `VALID_EMPTY` / `EVALUATED_VALID_EMPTY`, not search miss or absence.

### Underpowered

Under `PARENT`, the branch `X=0 AND H=1` contains only R5. With an exact `minimum_raw_denominator=2`, a query returning a supported empirical fact on that branch must terminate as `INSUFFICIENT_SUPPORT` / `EVALUATED_UNDERPOWERED`, not `VALID_EMPTY` and not `DISCOVERED_RESULT_SUPPORTED`.

## 6. Replay requirement

A fresh process must reproduce, byte-for-byte/hash-for-hash where identity-bearing:

1. parent branch predicate identity;
2. child branch predicate identity;
3. exact immediate-parent relation `CHILD -> PARENT`;
4. grandchild predicate identity;
5. exact immediate-parent relation `GRANDCHILD -> CHILD`;
6. replay-equivalent cohort membership for PARENT/CHILD/GRANDCHILD;
7. branch-conditioned cotravel receipt identity and facts;
8. `VALID_EMPTY` and `INSUFFICIENT_SUPPORT` terminal identities.

The current experiment stops before generation 2 because the current common public result does not provide the required canonical recursive child-to-parent handoff.