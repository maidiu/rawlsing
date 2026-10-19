# PYAT R39 F6P — Phase A prefreeze (written before the consumer was executed)

**Role:** independent bounded source-free F6 scientific-evidence consumer
implementer. Not HQ, F6 semantic issuer, original-source owner, N10W route-model
issuer, independent scientific acceptance reviewer or Sorok actor.

**Branch:** `agent/rabochii-pyat-r39-f6p-partial-bound-evidence-consumer-r1`
**Exact startup:** `2e6c189fd54b818556a44419b19691938ea76d5a`
**F6C author return:** `c1ebe091fa2bd12b254e5599cf37975fe438d462`
**F6M implementation:** Git blob `2df811d76db258d98d89ffb43c830cb221ff9a7d`
**Corrected S03FO A:** commit `1428c2e92bce1a49efd87378cb23df936d646dc5`, blob
`fc5e37fa5b2f0eb689593b42d95479d1327cb94c`
**A0 historical negative control:** blob `182cc7970d7624f6614015f5a51d0602e1630d52`
— explicitly **not** A and not the current S03FO comparison.
**Shared object module:** `a61365b994e5c3c50de0f598fcf40e90abf757b6`

## Claim frozen before execution

`claim_id`: `F6P_F6M_PARTIAL_BOUND_CONSUMER_DEPENDS_ON_ACTUAL_F6M_PRODUCT`

The named consumer `f6p_partial_bound_evidence_consumer.consume_f6m_evidence`
reads the **actual F6M bundle** returned by the F6M producer and exposes its
supported / partial / unidentified / refused evidence states. The real F6M
product must be the consumer input; no independently recreated fixture, stale
cache or aggregate-count reconstruction may substitute.

**Positive node:** `tests/test_f6p_consumer.py::test_w2_partial_preserves_uncovered_mass`
**Actual observables:** `evidence_state`, `uncovered_target_mass`,
`covered_subprobability`, `supported_point`, `exclusions`, `bounds`.

## Frozen positive oracle (from the R35 F6C exact-rational oracle)

| Case | Expected F6M/consumer result |
|---|---|
| W1 full coverage | A and B both complete, **uncovered 0**; F6M supported conditional formal `5/8`, informal `3/8`; consumer `SUPPORTED_SYNTHESIS` |
| W2 mixed eligibility | A reports **uncovered 0**, tidy point formal `7/10`, informal `3/10`; B preserves **uncovered 1/4**, covered subprobability `[1/4, 1/8, 3/16, 3/16]`, distribution `None`, decision `PARTIAL_IDENTIFICATION_ONLY`, S_A excluded in minority with `AGGREGATE_SUPPORT_OR_MASS_INSUFFICIENT`; consumer `PARTIAL_IDENTIFICATION`, no point |
| W7 source excluded all strata | A reports **uncovered 0**, tidy point formal `3/5`, informal `2/5`; B preserves **uncovered 1/2**, covered `[3/20, 1/10, 1/8, 1/8]`, S_A excluded in both strata; consumer `PARTIAL_IDENTIFICATION`, no point |
| W3 minority absent | B uncovered **1/5**, S_A and S_B excluded `NO_SOURCE_STRATUM`; consumer `PARTIAL_IDENTIFICATION` |
| W4 outcome leakage | conditioning on the outcome returns `DESCRIPTIVE_SELF_CONDITIONING` / `OUTCOME_LEAKAGE_TAUTOLOGY`; consumer `SELF_CONDITIONING`, no predictive point |
| W6 duplicate sample | F6M `SOURCE_INDEXED_BACKOFF`, candidate `None`, overlap `DUPLICATE_SAMPLE`; consumer `INCOMPATIBLE_RESPONDENT` |
| W8 category outside support | F6M conditional `UNAVAILABLE` / `CATEGORY_OUTSIDE_MAPPED_SUPPORT`; consumer `CATEGORY_OUTSIDE_SUPPORT` |

**C (no-pooling bounds):** without an explicit transport permission, C reports
complete ignorance (`total_unknown_mass = 1`, target marginal bounds `[0,1]`).
C is an independent conservative oracle, not a replacement for the F6M product.
The A/B/C W1 full-coverage invariance is retained: A and B conditional values
are identical on W1; A's W2/W7 full-coverage claims are the defect under test.

## Decisive negative experiment (frozen before implementation)

Hold the F6C world inputs, request and F6M producer fixed. At the consumer
boundary, sever/corrupt the actual F6M product:

- fault: in `native/rawlsing_next/pre553_heterogeneous_synthesis.py`, change
  `"uncovered_target_mass": str(uncovered),` to
  `"uncovered_target_mass": "0",`;
- the W2 F6M product then claims zero uncovered mass while carrying no complete
  distribution and a `PARTIAL_IDENTIFICATION_ONLY` decision;
- **expected RED:** `test_w2_partial_preserves_uncovered_mass` fails **by its
  assertion** (`PARTIAL_IDENTIFICATION` / `1/4` expected, `FALSE_FULL_COVERAGE`
  or equivalent inconsistent state observed), not by import error or unrelated
  failure;
- restore the exact F6M source and reproduce the exact valid consumer output.

A stale cache, an unrelated fixture calculation or a coincident output must not
keep the consumer green.

## Frozen hostile states

| Hostile | Expected consumer outcome |
|---|---|
| False full coverage (A product with excluded source + uncovered 0) | `FALSE_FULL_COVERAGE`, no point |
| Uncovered mass converted to zero | `FALSE_FULL_COVERAGE` or `PRODUCT_INCONSISTENT` |
| Incorrect denominator / nonconserving product | `PRODUCT_INCONSISTENT` |
| Incorrect stratum / scope | `INCOMPATIBLE_POPULATION_OR_STRATUM` |
| Missing or substituted source | `SOURCE_EXCLUDED` / `REVOKED_EVIDENCE` |
| Unknown design/weight + population request | `WEIGHT_OR_DESIGN_UNKNOWN`, no weight default of 1 |
| Incomplete native joint domain (W5) | producer `SynthesisError`; consumer cannot accept a product; typed `INCOMPLETE_NATIVE_JOINT_DOMAIN` at the input boundary |
| Positivity violation | producer refusal, no consumer point |
| Outcome-as-own-condition | `SELF_CONDITIONING`, no predictive point |
| Duplicate/fictitious common respondents (W6) | `INCOMPATIBLE_RESPONDENT` |
| Unsupported transport / real-use request | `PROHIBITED_MODEL_USE`, `UNVERIFIED_TRANSPORT` |
| Minority pruning / partial bound as point | `PARTIAL_IDENTIFICATION`, `supported_point = null` |
| Wrong clock/source version | `WRONG_SOURCE_VERSION` |
| Revoked evidence | `REVOKED_EVIDENCE` |
| Forged model-use admission | `PROHIBITED_MODEL_USE` / `FORGED_ADMISSION`; never a probability or route |

## Scientific ceiling

Source-free read-only TEST_ONLY evidence. Not original-source F6 issuance, an
installed N9/OC05 world, a joint structural/empirical route model, a behavioral
route probability, Field Forge semantic authority, Sorok C0/actor execution,
N11/N12 or V3. No `route_probability`, `selection_weight`, original U/E_pre,
model-use permission or production adoption. If a semantic/model-use right is
required and absent, the consumer must return HOLD/refusal, not invent it.

## Chronology

This prefreeze is written after reading the F6C return, F6M source and F6C
frozen oracle, and after verifying the pinned source blobs, but **before**
implementing or executing the F6P consumer. The expected values above come from
the F6C exact-rational oracle and the F6M method contract, not from the F6P
consumer's output.
