# PYAT R39 F6P — native F6M partial-bound evidence consumer

**Disposition: IMPLEMENTED, EXECUTED_GREEN and mechanically dependency-proved at
the bounded TEST_ONLY consumer grain. Not an independent scientific acceptance,
issuer adoption or production integration.**

The consumer reads the **actual repaired F6M bundle** (Git blob
`2df811d76db258d98d89ffb43c830cb221ff9a7d`), verifies its exact replay hash, and
exposes supported synthesis, incomplete coverage, lost planned source share,
partial bounds, unidentified joints, refused transport/model-use, source
exclusions, incompatible respondents/populations and self-conditioning. The
named consumer assertion was shown RED when the actual F6M product was severed;
the exact source was restored and the cold court replayed green.

## Position

- Branch: `agent/rabochii-pyat-r39-f6p-partial-bound-evidence-consumer-r1`
- Exact startup: `2e6c189fd54b818556a44419b19691938ea76d5a`
- F6C author return: `c1ebe091fa2bd12b254e5599cf37975fe438d462`
- F6M implementation: blob `2df811d76db258d98d89ffb43c830cb221ff9a7d`
- Corrected A (S03FO): commit `1428c2e92bce1a49efd87378cb23df936d646dc5`,
  blob `fc5e37fa5b2f0eb689593b42d95479d1327cb94c`
- A0 historical control: blob `182cc7970d7624f6614015f5a51d0602e1630d52`
  — used only as the historical negative control, never reported as A.
- Shared object module: blob `a61365b994e5c3c50de0f598fcf40e90abf757b6`
- Evidence commit before this document: `e75541d74d0db0ae2a654edb679a5862521521d2`

## Exact consumer functionality

`f6p_partial_bound_evidence_consumer.consume_f6m_evidence(bundle, request)`:

1. verifies the actual F6M bundle's `content_hash` over every field except
   `content_hash` (a fixture, stale cache or forged product fails closed);
2. reads the F6M decision, target-joint status, covered subprobability,
   uncovered target mass, support/exclusion reasons, uncertainty bounds and
   sampling status;
3. calls the actual F6M `conditional` for the request and classifies it;
4. returns a typed evidence result with `supported_point` **only** for complete
   supported synthesis, explicit partial bounds and **no point** otherwise;
5. never emits `route_probability` or `selection_weight`; never assigns a
   missing weight the value one; never infers a common respondent; never
   converts conditional aggregate evidence into an individual route;
6. refuses real-use/transport/model-use requests and self-declared admissions.

The source product is recorded with its module path, SHA-256 and Git blob, and
the exact fields read are listed in `values_read`.

## Frozen A/B/C experiment (exact rationals)

| Case | A corrected S03FO | B repaired F6M (consumed) | C no-pooling |
|---|---|---|---|
| W1 full coverage | complete, uncovered 0; conditional formal 5/8, informal 3/8 | same conditional 5/8, 3/8; consumer `SUPPORTED_SYNTHESIS` | total unknown 1; marginal bounds [0,1] |
| W2 mixed eligibility | **uncovered 0**, tidy point formal 7/10, informal 3/10 | **uncovered 1/4**, covered [1/4,1/8,3/16,3/16], no distribution; consumer `PARTIAL_IDENTIFICATION`, S_A minority excluded, no point | total unknown 1 |
| W7 source excluded all strata | **uncovered 0**, tidy point formal 3/5, informal 2/5 | **uncovered 1/2**, covered [3/20,1/10,1/8,1/8], no distribution; consumer `PARTIAL_IDENTIFICATION`, S_A excluded in both strata, no point | total unknown 1 |
| W3 minority absent | uncovered 1/5 but mislabels `SYNTHETIC_CANDIDATE` with no distribution; consumer `PRODUCT_INCONSISTENT` | uncovered 1/5, `PARTIAL_IDENTIFICATION_ONLY`, S_A/S_B `NO_SOURCE_STRATUM`; consumer `PARTIAL_IDENTIFICATION` | bounds only |

## Consumer states

| Case | Consumer state | Key values |
|---|---|---|
| W1 | `SUPPORTED_SYNTHESIS` | uncovered 0; point formal 5/8, informal 3/8 |
| W2 | `PARTIAL_IDENTIFICATION` | uncovered 1/4; covered [1/4,1/8,3/16,3/16]; no point; S_A minority exclusion |
| W7 | `PARTIAL_IDENTIFICATION` | uncovered 1/2; covered [3/20,1/10,1/8,1/8]; no point; S_A both strata |
| W3 | `PARTIAL_IDENTIFICATION` | uncovered 1/5; S_A/S_B `NO_SOURCE_STRATUM`; no point |
| W4 | `SELF_CONDITIONING` | `DESCRIPTIVE_SELF_CONDITIONING` / `OUTCOME_LEAKAGE_TAUTOLOGY`; no predictive point |
| W6 | `INCOMPATIBLE_RESPONDENT` | F6M backoff, candidate null, `DUPLICATE_SAMPLE` |
| W8 | `CATEGORY_OUTSIDE_SUPPORT` | F6M conditional `CATEGORY_OUTSIDE_MAPPED_SUPPORT` |
| A W2/W7 product | `FALSE_FULL_COVERAGE` | excluded source present while uncovered is 0; no point |
| A W3 product | `PRODUCT_INCONSISTENT` | decision/status does not match coverage; no point |

## Decisive negative experiment

- **Claim:** `F6P_F6M_PARTIAL_BOUND_CONSUMER_DEPENDS_ON_ACTUAL_F6M_PRODUCT`
- **Actual target:** `consume_f6m_evidence`
- **Positive node:** `tests/test_f6p_consumer.py::test_w2_partial_preserves_uncovered_mass`
- **Fault:** `native/rawlsing_next/pre553_heterogeneous_synthesis.py`, exact line
  `"uncovered_target_mass": str(uncovered),` → `"uncovered_target_mass": "0",`
- **Baseline:** PASS
- **Fault probe:** `TARGET_ASSERTION_FAILED`
- **Grade:** `BOUNDED_MUTATION_DETECTED` (mechanical proof gate, not semantic
  adoption)
- **Restoration:** exact F6M SHA-256
  `2930b5cd15c899146e9552b2e6b0efa3fc5835e57e58a6c16d756093e21d3871` and Git blob
  `2df811d7…` restored; post-gate cold court green.

The proof gate `changed` run examined the named tests, executed the witness and
returned `MECHANICAL_PROOF_GATE_PASS_NOT_SCIENTIFIC_ADOPTION`. The consumer was
also independently severed at its input boundary (candidate removed → state no
longer `PARTIAL_IDENTIFICATION`).

## Hostiles executed (32 native tests)

False full coverage; uncovered-to-zero; nonconserving covered/uncovered mass;
incorrect denominator; incorrect scope/stratum; missing or revoked source;
unknown design/weight with no weight-one default; incomplete native joint
domain; positivity violation; outcome-as-own-condition; duplicate/fictitious
respondents; unsupported transport; minority pruning; wrong clock/source
version; partial bound as point; forged real-use/admission; bundle replay
mismatch; malformed product; category outside support; self-conditioning.

Native court: **32 passed / 0 failed / 0 error / 0 skip**.
Pre-gate cold (two seeds): **32/0**, **32/0**.
Post-gate cold (two seeds, after restoration): **32/0**, **32/0**.

## Scientific uncertainty / refusal outcomes

- W2/W7/W3 retain their uncovered mass and produce bounds with **no point**.
- W1 supported point is `SOURCEFREE_EXPERIMENT_ONLY`, not a real-use estimate.
- W4 self-conditioning is named, not sold as a predictive conditional.
- W6 duplicate respondents are refused, not joined.
- Unknown design/weight is exposed as `UNKNOWN_DESIGN`; no weight is imputed.
- Real-use/transport/model-use requests return typed refusal; the consumer
  issues no route probability or selection weight.

## Holds and authority ceiling

Original-source F6 issuance, installed N9/OC05 world, joint structural/empirical
route model, behavioral route probability, Field Forge semantic authority, Sorok
C0/actor execution, N11/N12, V3 and production adoption remain **not granted**.
The consumer is TEST_ONLY and source-free. The R35 sealed commission's obsolete A
pin remains an explicit HQ amendment/succession issue: this return uses the
corrected A `fc5e37fa` as method A and A0 only as a historical negative control;
it does not re-seal the commission or infer a new model-issuer permission.

## Smallest genuine unresolved owner edge

**A competent owner-issued real-use / transport admission** (or the equivalent
F6M consumer acceptance) is absent. The consumer can lawfully expose TEST_ONLY
supported/partial/unknown evidence, but cannot promote it to a real-use,
route-probability or world-consumer join. The consumer preserves that HOLD
exactly rather than inventing permission. Separately, the R35 sealed-A-pin
amendment is an HQ succession issue, not a consumer defect.

## Cost / environment

Local warm shared-store worktree, Python 3.11.3, pytest 9.1.1, Git 2.39.1; no
paid API call observed. Incremental cash/quota: **UNKNOWN** (see
`environment_passport_delta.json`).

## Evidence index

- `00_PHASE_A_PREFREEZE.md`, `00_FROZEN_CLAIM_AND_ORACLE.json` — pre-execution
  claim, exact A/B/C oracle and hostile expectations.
- `f6p_partial_bound_evidence_consumer.py` — consumer.
- `tests/test_f6p_consumer.py`, `tests/test_f6p_abc_oracle.py`,
  `tests/f6p_fixtures.py` — native positive/hostile court and A/B/C oracle.
- `tests/test_f6p_consumer.py.proof.json` — executable severance witness.
- `native/rawlsing_next/*` — exact F6M/A/A0/shared source blobs.
- `oracle/*` — F6C world builder, C method and frozen exact oracle.
- `evidence/native_court.xml`, `cold_0.xml`, `cold_1.xml`,
  `post_gate_cold_0.xml`, `post_gate_cold_1.xml` — JUnit.
- `evidence/proof_gate_changed_receipt.json`,
  `evidence/execution_receipts.json` — dependency proof and values-read/custody
  receipts.
- `environment_passport_delta.json`, `PUBLICATION_RECEIPT.json`.

The final remote SHA is verified by direct `git ls-remote` readback and bound by
`PUBLICATION_RECEIPT.json`.
