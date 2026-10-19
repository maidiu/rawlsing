# R40 EE1 — Functional results, grades and fault witnesses

Cold suite: **33 passed, 0 failed** in 19.74 s
(`evidence/ee1-suite.xml`; run
`python3 -m pytest -q -p no:cacheprovider
WORKER_RETURNS/PYAT-R40-EE1-.../tests --junitxml=...` from the worktree root,
`PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1`).

## Claim results (claim-grade truth per PRE-MAIN law)

| Claim | State | Grade |
|---|---|---|
| C0 custody: staged world files = upstream commit bytes; epoch receipt/snapshot hashes = accepted identity `4b592251…/7e746c12…` and `d29f2aab…/07aefe67…` | green | `EXECUTED_GREEN` |
| C1 T35 rule-only: fee 2→6, exit 2→8, revision 1→2, publication 2026-03-01→2027-06-01; training ELIGIBLE→BLOCKED_BY_MODELED_RULE; exit WITHIN_MODELED_BUDGET→RESOURCE_CONSTRAINED; civil unchanged; empirical steps identical `(32,{14,18}) (16,{6,10}) (8,{2,6})` | green | `EXECUTED_GREEN` — synthetic-institutional (TEST_ONLY), not measured source |
| C2 V553 reuse: identity accept; harmonization `multi_wave_authorized`/`aligned`/`comparable`; multi-wave key `AUTHORIZED_SPARSE_TEMPORAL_KEY`; delta probe 0.15 `probe_delta` + `delta_interpretation_permission=False` + `probe_only_temporal_field`; authorized control `authorized_structural` + permission; gap 2021 `unknown_noncomparable`; readiness 45 typed errors | green | `EXECUTED_GREEN` inherited-method reuse (synthetic inputs) |
| C3 refusals: mixed family/country typed at both identity and report-builder layers; disjoint semantic structure `insufficient_multi_wave_authority`/`insufficient_shared_semantic_structure`; population change `NONCOMPARABLE_POPULATION_OR_ESTIMAND` while naive subtraction yields untyped 0.15; estimand change refused | green + W2 | `EXECUTED_GREEN` + `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED` (population gate) |
| C4 clocks: E1 excludes 2027 publication/effective clocks; forced future-rule snapshot refused by the actual R13 adapter (`UNREGISTERED_SELECTED_SNAPSHOT`); bridge `FUTURE_RULE_AT_HISTORICAL_AS_OF`, `FUTURE_EVIDENCE_AT_HISTORICAL_AS_OF`, `OBSERVATION_AFTER_AS_OF`; archival receipt `archival_only=True/fresh_use_authorized=False`, product `ARCHIVAL_COMPARISON_ONLY__NOT_FRESH_USE` | green + W3 | `EXECUTED_GREEN` + `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED` (future-vintage gate) |
| C5 Ghana: null record (state `HELD_UPSTREAM_EVIDENCE_AND_ISSUANCE`, all numerics null); Ghana claim refused before any number; hypothetical exercise (explicitly labeled) delta≈0.20 variance≈0.0061 with `n8e_product/ee12_issued/ghana_claim` false; EE1 product embeds the verbatim null record | green | `EXECUTED_GREEN` synthetic-hypothetical-only; Ghana stays HOLD |
| C6 oracle: six frozen scenarios, oracle (import-independent) and bridge agree: comparable; mixed family; mixed country; population change; future rule; annual gap | green + W4 | `EXECUTED_GREEN` + `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED` (oracle family gate) |
| Consumer delta permission (probe never promoted to measured) | green + W5 | `CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED` |

## Executable fault witnesses (same normal pass; shared checker)

| Witness | Severed edge | Baseline | Mutant | Receipt |
|---|---|---|---|---|
| W2 | population/estimand gate (`ee1_temporal_owner.py`) | PASS | TARGET_ASSERTION_FAILED | `evidence/witness-test_ee1_uncomparable_population_refusal.json` |
| W3 | future-rule clock gate | PASS | TARGET_ASSERTION_FAILED | `evidence/witness-test_ee1_clock_discipline_and_future_rule.json` |
| W4 | oracle source-family check | PASS | TARGET_ASSERTION_FAILED | `evidence/witness-test_ee1_oracle_cross_check.json` |
| W5 | consumer `delta_interpretation_permission` gate | PASS | TARGET_ASSERTION_FAILED | `evidence/witness-test_ee1_t35_rule_only_positive.json` |

All four contracts are siblings of their named tests; sources were restored by
the checker (working tree diff after witnesses: none).

## The four commissioned discriminations, resolved

1. **Measured source change** — `NOT_RUN`: no original-source warrant exists.
   The method chain can express it (authorized-control branch of C2e behaves as
   the authorized path would), but no real measurement is claimed.
2. **Changing frame/edition that does not support the comparison** —
   `EXECUTED_GREEN` typed refusals (C3, C6) while the naive path manufactures
   an untyped delta.
3. **Partially identified change** — `EXECUTED_GREEN`: gap year stays
   `unknown_noncomparable` (absence ≠ no change); probe deltas stay
   `probe_only_temporal_field` without interpretation permission.
4. **Institutional TEST_ONLY rule change with unchanged evidence** —
   `EXECUTED_GREEN` (C1): affordability changed, empirical chain identical.

## Freeze corrections (visible, pre-run)

* **FC1** `delta_id` does not survive the inherited delta index schema reindex
  (`V553_CROSS_WAVE_DELTA_INDEX_SCHEMA.required_columns` has no `delta_id`);
  delta identity is `from_wave_id/to_wave_id`. Corrected in the bridge before
  the first suite run.
* **FC2** C6/S6 gap typing needed an explicit annual-coverage declaration
  (`annual_anchors_required`); without it every non-adjacent pair would type as
  gap, contradicting C2/S1. Gap remains an annotation otherwise. Corrected
  during implementation, before any suite run (no candidate output was used to
  choose either correction).

## Item 3 (authorized retained time series as historical receipt)

`TYPED NONAVAILABILITY`: the worktree contains no compiled V553 artifact to
reuse as a historical receipt (searches: `*v553_wave_harmonization_report*`,
`*v553*` run directories — none). The earliest real-source blocker is the N03
five-authority chain (official release/custody, source-read custodian,
independent statistics owner, EE12/C7 issuer, per-wave execution owner) under
`HOLD_SOURCE_RELEASE_METHOD_STATISTICS_AND_EE12_ISSUER`, with no current
source read warrant (`HOLD_NO_VERIFIED_CURRENT_SIGNED_ORIGINAL_RIGHT`,
original35 `PERMITTED=0`).

## What this return is not

No Ghana trend, no EE12/N8E/N8S issuance, no N9/OC05 installation, no N10W
route model, no actor, no source read, no measured claim. Every product carries
`test_only/sourcefree` markers and false authority flags.
