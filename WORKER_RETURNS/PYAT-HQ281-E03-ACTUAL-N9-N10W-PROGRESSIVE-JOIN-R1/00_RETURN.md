# PYAT HQ281 E03 — Actual source-free N9→N10W two-step progressive owner run

**TERMINAL:** `HQ281_E03_BOUNDED_PRODUCT_OR_EXACT_HOLD__GITHUB_PUSHED`
**RESULT:** `PASS__BOUNDED_PRODUCT_REAL_OWNERS__18_TESTS_PASS__FULL_PROGRESSIVE_CHAIN_P(Y|A)-P(Y|A,B)-P(Y|A,B,C)_MATCHES_HAND_DERIVED_ORACLE__11_HOSTILE_REFUSALS_DEMONSTRATED__N9_N10W_ABSENCE_RECORDED_NOT_FABRICATED__SOURCEFREE_ONLY__NONISSUING`

**Branch:** `agent/rabochii-pyat-hq281-e03-progressive-n9-n10w-owner-join-r1`
**Sealed startup (verified before mutation):** `e79c6a136748c204963d2169c4f64b0c48374437`
**Inherited parent:** `c2301a9bf42b5340ca752a51bf4b9f1d4eaeefa2` (E01)
**Authority:** HQD-2026-10-10-280; canonical `a70a069fa948e0f3c041b389edcc732b6b948a4f`; semantic PRE-MAIN `1f47063c3205a45888b3c55e81e7485943ed1390` (**unmutated**).

## 1. What was built (new files only — zero owner edits)

| File | Blob | Role |
|---|---|---|
| `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` | `84d404147547767be8ecd4b6e1541f5fa3a8c8a2` | the progressive join candidate (`PYAT_HQ281_E03_PROGRESSIVE_N9_N10W_JOIN_CANDIDATE@1.0.0`) |
| `rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py` | `2161c0fff86ecb7a2c9a40b29852075e802841fd` | 18 tests |
| `WORKER_RETURNS/…/repro/e03_evidence_recorder.py` | (return dir) | evidence recorder |

`git diff --name-only <sealed> -- rawlsing_next/` is **empty**; provider/composition/F8 blobs recorded in the evidence JSON.

## 2. Synthetic world law — hand-derived BEFORE any owner ran

58 respondents, binary A/B/C/Y. Cell counts (Y=1, Y=0):

| A B C | Y=1 | Y=0 |
|---|---|---|
| 1 1 1 | 6 | 2 |
| 1 1 0 | 4 | 4 |
| 1 0 1 | 5 | 3 |
| 1 0 0 | 3 | 5 |
| 0 1 1 | 4 | 2 |
| 0 1 0 | 2 | 4 |
| 0 0 1 | 3 | 3 |
| 0 0 0 | 2 | 6 |

Every positioned subject carries `real_subject: False`. One shared risk set across all respondents and questions, so every step measures over the exact same respondent pool with the same risk identity. **Never called real CURRENT.**

## 3. Real owner chain — actually executed, matches the oracle exactly

| step | owner invoked | denominator | cells | P(Y=1) exact | consumer |
|---|---|---|---|---|---|
| P(Y\|A=1) | **N10E** `provide_empirical_possibility_slice` | 32 | {0:14, 1:18} | **9/16** | `EXACT_SUPPORTED` |
| P(Y\|A=1,B=1) | **C1** `compose_positioned_subject_possibility` | 16 | {0:6, 1:10} | **5/8** | `EXACT_SUPPORTED` |
| P(Y\|A=1,B=1,C=1) | **C1** `compose_positioned_subject_possibility` | 8 | {0:2, 1:6} | **3/4** | `EXACT_SUPPORTED` |

Then each step's **own produced evidence object** was handed to the real plain **F8** evaluator as a separate consumption invocation — produced/ref-consumed identity verified equal for all three steps. Production and consumption logs carry distinct call identities.

**Conservation, verified:** same `release_ref` (REL-e03-progressive) and same `risk_set_ref` across all steps; both minority alternatives present in every step (min count 2 at depth 3); `UNCERTAINTY_UNQUANTIFIED` preserved.

**Command:** `PYTHONPATH=. python3 repro/e03_evidence_recorder.py`

## 4. Owner-absent edges — the honest ledger

The commission's conditional was resolved **positively**: the source-free joint owner interface *does* support three conditioners, so all three steps ran through real owners. The genuine missing edges, located precisely:

1. **N10E provider refuses multi-binding** — `ProviderRequestShapeError: PROVIDER_REQUEST_SHAPE_ERROR: N10E R1 follows the accepted C1-01 scalar grain…` at `pre553_empirical_possibility_provider.py:_single_binding`. That is why steps 2–3 route through the C1 multi-conditioner composition owner directly (the adapter is exactly that bounded route).
2. **N9 has no implementable selected join** (E01 API graph: `implemented: false`) — recorded `ABSENT__recorded_not_fabricated`.
3. **N10W has no implementable progressive world binding** (E01: `implemented: false`) — recorded `ABSENT__recorded_not_fabricated`.

**No N9/N10W owner was claimed implemented; no fake authority was substituted.**

## 5. Hostiles — 11 refusals demonstrated by execution (all real owner errors)

| hostile | observed refusal |
|---|---|
| unordered conditioner list [B,A] vs witness [A,B] | `ConditionValueRelationMismatch: witness field mismatch: consumer_query_ref` |
| wrong weighted measure (GOVERNED_WEIGHTED, weights absent) | analytical_state `UNAVAILABLE`, evidence null (raw measure stays distinct, 32) |
| cross-sample join (foreign universe/release) | `AnalyticalCompositionError: SOURCE_UNIVERSE_MISMATCH` |
| proxy presented as exact / false pairing value 1→0 | `ConditionValueRelationMismatch: conditioner 1: pairing exact value mismatch` |
| parent/coparent inference (own-topic A=1,A=1 joint) | `PositionedSubjectPossibilityError: duplicate conditioner binding` |
| exact stratum absence laundered to exact | `UNRESOLVED / EXACT_POSITIONED_STRATUM_ABSENT` |
| walkback proxy presented as exact | `EXACT_UNRESOLVED_PROXY_AVAILABLE` (proxy labelled, exact_evidence None) |
| false null from zero-support predicate | `ConditionValueRelationMismatch: no matching producer leaf` |
| fake G0b / B5 CURRENT / model-use | structural: effect flags all false; no lifecycle/B5/G0b imports; subjects synthetic |

Every refusal is the **owner's own typed error** — the adapter never pre-filtered anything into a softer shape.

## 6. Tests and scope

- Candidate suite: **18 passed**.
- Widest targeted run (candidate + analytical composition ×2 + possibility provider + empirical query + positioned-subject F8 + F8 court): **227 passed**.
- Resources: 4.88–6.42 s suite; recorder seconds. No capacity forecast.

## 7. Ceilings and holds

Source-free only. No raw SAV/DTA (0 files); no respondent row read; 35 waves/63 temporal pairs untouched; synthetic world only. No self-issued source/operation/model-use/Field-Forge/temporal/CURRENT/G0b/V3 right; every effect flag false (`real_current_claim: False`). No canonical/accepted-owner edit; no self-adoption; no ZIP relay. The chain is a development-grade demonstration that the progressive conditioning the N10E→N10W edge demands is reachable through real owners — it is **not** N10W implementation, not G0b, and not a CURRENT service. N9/N10W remain absent and are recorded as such.

**Terminal:** `HQ281_E03_BOUNDED_PRODUCT_OR_EXACT_HOLD__GITHUB_PUSHED`.