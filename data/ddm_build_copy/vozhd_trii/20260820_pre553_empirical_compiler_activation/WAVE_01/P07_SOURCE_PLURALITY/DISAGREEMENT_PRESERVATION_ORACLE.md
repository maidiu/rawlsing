# PRE553 P07 — Disagreement Preservation Oracle

**Assignment:** `PRE553-W01-P07-001`  
**Role:** `PRE553_P07_SOURCE_PLURALITY`  
**Authority:** non-dispositive preflight only.

## Constitutional rule

Distinct respondent universes remain distinct by default. Source-indexed disagreement is information. No disagreement state is permission to pool, link, compose, backfill, select a majority source, or convert population disagreement into actor belief/uncertainty.

`PROVENANCE != SEMANTIC_EQUIVALENCE != RESPONDENT_LINKAGE != NONDUPLICATION != POOLING != COMPOSITION != BACKFILL`

Every positive cross-source operation requires its own exact operation-specific authority at time of use.

## Hostile fixtures

| ID | Attack | Required disposition |
|---|---|---|
| P07-H01 | Two sources use the same canonical question label; pool them automatically | Reject. Alias/harmonization is not semantic or sample equivalence. |
| P07-H02 | Two source-native questions have a semantic-equivalence receipt; assume same respondents | Reject. Semantic equivalence does not grant respondent linkage. |
| P07-H03 | Exact respondent linkage exists; assume no double-counting risk | Reject. Linkage does not prove disjointness/nonduplication. |
| P07-H04 | Sources have no known linkage; assume they are disjoint | Reject. Unknown overlap remains `UNKNOWN_OVERLAP`. |
| P07-H05 | Source A and B disagree; choose the majority source | Reject absent exact composition authority. Preserve both source-indexed results/states. |
| P07-H06 | Source A has more respondents; treat it as canonical | Reject. Sample size is not authority precedence. |
| P07-H07 | Sources share provenance ancestor | Reject composition/linkage inference. Provenance proves origin only. |
| P07-H08 | Sources are co-located/co-temporal | Reject composition/linkage inference. Location/time relation is not sample authority. |
| P07-H09 | Same display respondent ID appears in two sources | Reject exact linkage unless a linkage authority binds scoped identities. |
| P07-H10 | Pool exact rows by concatenation because schemas match | Reject. Schema parity is not design/estimand/weight/nonduplication authority. |
| P07-H11 | Average source-level estimates because scales match | Reject absent exact estimand-composition authority including mixture/weight and uncertainty treatment. |
| P07-H12 | Backfill `DECLARED_NONE` from another source | Reject. Declared none is a typed state, not missingness. |
| P07-H13 | Backfill `SOURCE_NOT_APPLICABLE` or `TEMPORAL_NONCOMPARABLE` | Reject. Applicability/noncomparability cannot be laundered into donor data. |
| P07-H14 | Backfill `OBSERVED_ZERO` or `ZERO_SUPPORT` | Reject. Explicit zero/no empirical basis is not missingness. |
| P07-H15 | Backfill an `UNSPECIFIED` state with exact directional authority naming that state | May proceed only within that authority's exact semantic/design/weight/overlap/effective scope. Original source state remains replayable. |
| P07-H16 | Pool sources with semantic equivalence but unknown overlap | Reject when the operation requires nonduplication proof. |
| P07-H17 | Pool sources with overlap authority but no semantic equivalence | Reject. Overlap handling does not establish common meaning/estimand. |
| P07-H18 | Pool with semantic equivalence and nonduplication but no pooling authority | Reject. Preconditions are not operation permission. |
| P07-H19 | One pooling authority is reused for a different estimand/risk set/time | Reject as out of scope/stale authority. |
| P07-H20 | A later authority supersedes an earlier one; rewrite historical receipt | Reject. New authority is prospective; historical replay remains bound to historical authority. |
| P07-H21 | Conflict between two active composition authorities | Fail closed as `CONFLICTING_AUTHORITY`; preserve source-indexed inputs. |
| P07-H22 | Missing composition authority | Fail closed as `UNKNOWN_AUTHORITY`/no composition effect. |
| P07-H23 | M4 co-resolves objects from two sources | No relation/composition grant. Co-resolution is administrative. |
| P07-H24 | M5 receives source disagreement in upstream empirical material | Disagreement remains upstream/source-indexed; do not convert to actor contradiction, belief, memory, or uncertainty. |
| P07-H25 | Repository/index/locator proximity is used as evidence of source relationship | Reject. Infrastructure is nonsemantic. |
| P07-H26 | Harmonization transform is reversible and hash-bound; infer pooling | Reject. Exact transform integrity still does not create sample/estimand authority. |
| P07-H27 | Exact respondent linkage plus semantic equivalence; infer pooling | Reject until overlap/nonduplication, design/estimand/weight and positive pooling authority are bound. |
| P07-H28 | A source is missing from an operation; silently use nearest available source | Reject. No nearest/default/latest source fallback. |

## Positive controls

A lawful pooling operation must bind exact participating source universes, target query/estimand, risk set/denominator, semantic equivalence, sample-design compatibility, overlap/nonduplication treatment, weights/measure authority, typed missingness/applicability, composition method and effective scope. If respondent identity is material to deduplication or analysis, exact respondent-linkage authority is additionally required.

A lawful backfill is directional and names exactly which target missingness states are eligible. It never overwrites the historical target state; it produces a separately receipted governed operation result.

## Replay

For every cross-source operation, replay binds source-universe identities, component object hashes/states, relation-authority IDs/versions/hashes, effective scope, query/estimand/risk-set identity, overlap/linkage/weight rules and operation result. Same exact input and authority must replay identically. Later authority never rewrites prior receipts.

## Acceptance

Pass only when disagreement survives without majority collapse and every cross-universe operation is impossible by default until all relation-specific positive authority is exact and current.
