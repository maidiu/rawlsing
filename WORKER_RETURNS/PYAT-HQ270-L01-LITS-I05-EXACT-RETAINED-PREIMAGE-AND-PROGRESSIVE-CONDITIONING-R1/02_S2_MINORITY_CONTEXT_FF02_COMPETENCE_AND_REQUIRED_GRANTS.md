# HQ270-L01 — S2: Minority Context, FF02 Competence, and Required Grants

**Commission:** `PYAT-HQ270-L01-LITS-I05-EXACT-RETAINED-PREIMAGE-AND-PROGRESSIVE-CONDITIONING-R1`
**Branch:** `agent/rabochii-pyat-hq270-l01-lits-retained-preimage-nested-query-r1`

## 1. Minority / nonmodal cells (25, retained as separate typed truth)

The `comparison_fact_manifest` in the checkpoint tail contains **25** `MINORITY_OR_NONMODAL_DEPARTURE` candidates, all:

- **Rule:** `D02_P4_MINORITY_NONMODAL_COMPLETE_JOINT_CELLS`
- **Typed state:** `DISCOVERED_RESULT_SUPPORTED`
- **Role:** `BASE`
- **Raw denominator:** 24630 (the joint q301_2×q301_7 risk set)
- **Validation:** `TARGET_CELL_SUPPORTED` with exact-decimal target cells (e.g. `[{"$exact_decimal":"3"},{"$exact_decimal":"1"}]`)
- **Uncertainty:** `UNCERTAINTY_UNQUANTIFIED`, no weights

These are complete joint response cells on the (q301_2, q301_7) pair that are minority/nonmodal relative to the marginal modes. Exact native codes are **not force-labeled** (preserved from HQ269 S01 disposition: "25 retained supported D02_P4 candidates, exact native codes not force-labeled").

They are retained here as **separate typed truth** from the D02_P1 joint-dependence positive and the D02_P3 VALID_EMPTY negative. They do not collapse into either.

## 2. Bounded K-way configuration candidates (23, SUPPORTED)

The manifest also contains 23 `BOUNDED_K_WAY_RESPONSE_CONFIGURATION` candidates, all `DISCOVERED_RESULT_SUPPORTED`, with `CONDITION`/`BASELINE` or `BASE` roles. These are bounded k-way response-configuration discoveries on the same risk set. They are noted for completeness; they are not the D02_P1 joint co-travel positive and are not used to claim a nested A,B,Y triple.

## 3. FF02 competence and the actor-independent source-indexed question

### Retained FF02 status

From the retained `ff02_readiness_disposition.json` (source-retry evidence):

| Field | Value |
|---|---|
| `ff02_executed` | `false` |
| `structural_admission_created` | `false` |
| `structural_admission_object_count` | `0` |
| `status` | `FF02_READY__NO_SOURCE_REOPEN_REQUIRED` |
| `source_reopen_required` | `false` |
| `provenance_authority_risk_release_replay_and_exact_ref_closure` | `PASS__RETAINED_AND_CHECKPOINT_VALIDATED` |
| `unrecoverable_downstream_object_classes` | `[]` |

Retrievable exact object classes: `EmpiricalFact@1.0.0`, `EmpiricalQuerySpec@1.0.0`, `EmpiricalPredicate@1.0.0`, `AuthoritySnapshot@1.0.0`, `DiscoveryAuthority@1.0.0`, `DiscoveryResultReceipt@1.0.0`, `EmpiricalUniverse@1.0.0`.

### The commission's question

> "Also assess whether an exact retained source item can be offered as **actor-independent source-indexed observed social-context contribution**, separately from actual structural/causal mechanisms."

### Assessment

**No.** An actor-independent source-indexed observed social-context contribution **cannot** currently be offered from the retained products, because:

1. **FF02 has not been executed.** `ff02_executed=false`. The Field Forge structural-relation admission (ASTRA-FF02 / D04 learned-product → actor-independent relation / structural-admission authority court) has not run. No structural admission object exists (`structural_admission_object_count=0`).

2. **No existing FF02 structural-admission producer/permission exists.** The ASTRA-FF02 commission (`WORKER_COMMISSIONS/ASTRA-FF02/00_COMMISSION.md`) defines the bounded D04 structural-relation formation + admission authority court. That court has not been convened and no producer/admission authority has been constructed. The commission explicitly says: *"Output existing exact producer/permission missing, not a synthetic 'structural pressure' score."*

3. **The retained D02_P1 structural interpretation is co-travel only.** HQ269 S01 disposition records the structural interpretation of the joint co-travel positive as `OPINION_COTRAVEL_ONLY_NOT_OBJECTIVE_REGIME_OR_CAUSAL_PRESSURE`. The pair (q301_2, q301_7) co-travels on the same respondents; this is a joint-response fact, not an actor-independent structural regime or causal pressure.

4. **Cross-source seed counts are zero.** The Afrobarometer×LiTS cross-source seed counts show `shared_seed_rows: 0`, `shared_proposition_seeds: 0`, `authority_grade: PROVISIONAL_NON_AUTHORITY`, implication `DOES_NOT_PROHIBIT_INDEXED_CO_PRESENCE_AND_DOES_NOT_GRANT_RELATION`. Indexed co-presence is not prohibited, but no relation is granted.

### What is missing (existing exact producer/permission)

The missing piece is the **existing FF02 structural-admission producer/permission** — specifically:

- An executed FF02 structural-admission run that creates at least one structural admission object (`structural_admission_object_count > 0`).
- The ASTRA-FF02 producer/admission authority (the bounded D04 actor-independent relation / structural-admission authority court) that would qualify the exact D04 empirical lanes to support bounded actor-independent structural relation objects.

This is a documentary naming of the missing edge. **No synthetic structural pressure score is offered. No structural admission is self-issued.**

## 4. Required grants (not issued)

The following grants would be needed before an actor-independent source-indexed social-context contribution or a same-respondent nested q(Y|A) → q(Y|A,B) operation could be lawfully offered. **None are issued by this return.**

| Grant | What it would enable | Current state |
|---|---|---|
| Extended AS2A projection authority admitting a third RespondentEvent slot (e.g. q310) | Same-respondent three-variable nested conditioning q(Y\|A) → q(Y\|A,B) with EXACT_SAME_RESPONDENT_ONLY on both steps | Not existing; current AS2A-BANKED-1.0.0 authorizes only q301_2 and q301_7 |
| Executed FF02 structural-admission producer/permission | Actor-independent source-indexed observed social-context contribution | `ff02_executed=false`, `structural_admission_created=false`, no producer exists |
| Separate positive EE15 LiTS structural-use/admission law | Downstream structural mediation input | Not existing (HQ269 S01: "missing") |
| Actual EE14 model-use/service/replay decision by HQ | Actual world consumer replay | Not issued (HQ269 S01: "HOLD_EXACT_UNPROVED_EDGE") |
| Design-based uncertainty authorization (weights, variance estimator) | Quantified uncertainty on raw denominators | Not authorized; all facts `UNCERTAINTY_UNQUANTIFIED`, `weighted_denominators_authorized=false` |

## 5. Preserved typed truths (summary)

| Truth | Hash / identifier | Typed state | Denominator(s) |
|---|---|---|---|
| D02_P1 joint co-travel (positive) | `0373f9117bb34274...` | `DISCOVERED_RESULT_SUPPORTED` | JOINT 24630 / M0 24897 / M1 28325 |
| D02_P3 conditional reversal (negative) | `a3dfb9c641e8efc1...` | `VALID_EMPTY` | 8 constituent facts SUPPORTED; pooled/stratum denoms [1854, 455, 384, 1455, 1523, 4327, 1013, 1337] |
| D02_P4 minority cells (25) | various | `DISCOVERED_RESULT_SUPPORTED` | 24630 |
| FF02 readiness | `ff02_readiness_disposition.json` | `FF02_READY__NO_SOURCE_REOPEN_REQUIRED` | ff02_executed=false |

These are retained as **separate typed truths** and are not collapsed, merged, or upgraded.
