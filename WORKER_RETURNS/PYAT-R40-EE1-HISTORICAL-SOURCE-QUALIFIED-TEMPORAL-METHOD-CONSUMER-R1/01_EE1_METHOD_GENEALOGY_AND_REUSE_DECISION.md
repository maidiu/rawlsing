# R40 EE1 — Exact V553 → current temporal-function ownership ledger and reuse decision

All inherited functions below were executed unmodified on synthetic TEST_ONLY
inputs. "Current owner semantics" is what the code actually enforces, read from
source and confirmed by execution. Blob ids are git blobs at sealed startup
`1150e836`.

## Ledger

| # | Inherited function (file) | Blob | What it actually enforces | EE1 decision | Executed evidence |
|---|---|---|---|---|---|
| L1 | `normalize_temporal_report_identity` (`data/ddm_build_copy/ddm_v553_temporal_identity.py`) | `bbbef131…` | Exactly ONE survey family, ONE country, ONE calendar anchor per year over the temporal input; typed `SurveyIdentityError` on mixtures ("requires exactly one explicit survey family", "requires exactly one explicit country_code", "one anchor per calendar year") | **REUSE (unmodified)** | C2/C3 tests |
| L2 | `build_v553_wave_harmonization_report` (`ddm_v553_harmonization.py`) | `153f3dbe…` | Two-wave comparability authority: per-pair shared semantic/directionality/position structure over the actual overlay files, `pair_harmonization_status ∈ {aligned, insufficient_shared_*}`; `ready_for_v553`; `comparison_authority_status = multi_wave_authorized | insufficient_multi_wave_authority`; comparable/partial matrices; harmonization/readiness scores | **REUSE (unmodified)** | C2c/C3c |
| L3 | `_authorize_v553_multi_wave_key` (`ddm_v553_temporal_pressure.py`) | `5304b70f…` | Multi-wave key status: `AUTHORIZED_SPARSE_TEMPORAL_KEY` only with ≥2 probe-ready resolved structural anchors **and** harmonizer authorization; otherwise `PROBE_ONLY_TEMPORAL_KEY`/`BLOCKED_TEMPORAL_KEY` with typed reasons | **REUSE (unmodified)** | C2d |
| L4 | `_build_v553_cross_wave_delta_index` (same) | `5304b70f…` | Deltas carry `delta_value_kind ∈ {probe_delta, authorized_structural}`; `delta_interpretation_permission = True` only when BOTH anchors are `observed_authorized_anchor`; otherwise `blocked_reason = probe_only_temporal_field` | **REUSE (unmodified)** | C2e probe + authorized control |
| L5 | `_build_absence_noncomparability_register` (same) | `5304b70f…` | Missing years inside an anchored span become `register_status = unknown_noncomparable`, reason `missing_gap_stays_unknown_noncomparable`; interpolation only relabels to `interpolated_with_authority` under explicit allowance | **REUSE (unmodified)** | C2f |
| L6 | `validate_v553_temporal_pressure_readiness` (same) | `5304b70f…` | The thin temporal layer is NOT runtime consumable; 45 typed missing-artifact/authority errors on empty input (owner must supply 33 artifacts + 6 scores) | **REUSE (unmodified)** | C2g (45 errors reproduced) |
| L7 | `ddm_v553_canonical_harmonization.py`, `ddm_v553_schema.py`, `ddm_v553_repo_discovery.py` | `1951ada5…`, `b41b4485…`, `41e0c85d…` | Canonicalization/schema/discovery support for the full V553 compile; not required for the bounded two-period contract | **EXAMINED — NOT EXERCISED** (available for the future authorized full-layer run) | — |
| L8 | `rawlsing_next/pre553_source_relations.py` (P07 relation guards: `guard_sample_pooling`, `guard_estimand_composition`, `guard_backfill`, resolver) | `5b67e3f9…` | Two-source relation authority requires exact `AuthoritySnapshot`s and positive authority material; refusal by construction without them | **EXAMINED — NOT USED** (reserved for the source-authorized stage; no authority exists to instantiate it) | — |
| L9 | Accepted R35 T35 two-epoch world + R13 E05R adapter (staged) | `690790e8…` adapter, product blobs | The actual historical selected-world consumer: publication/effective/as-of clocks, revocation typing, `historical_receipt` archival-only path, unchanged E04 clients | **REUSE (unmodified, staged byte-identical)** | C0/C1/C4 |
| L10 | Accepted T35 `n8e_sourcefree_comparator.py` | staged from `8bfb145f7` | HYPOTHETICAL-only admissibility: refusals for non-hypothetical/Ghana claims, stale releases, design variance methods (IID/headline), missing EE12/science authority; weighted interval when fully positive; frozen Ghana null record | **REUSE (unmodified)** | C3 design/authority channels + C5 |
| L11 | Naive source-mismatch subtraction | — | Produces an untyped number with no comparability or clock discipline; would report 0.15 from the frozen shares even under population change and would silently interpolate gap years | **REPLACE (rejected baseline)** — comparative proof: inherited+EE1 path types the same numbers as refusal (population), `probe_only_temporal_field` (unauthorized), or `unknown_noncomparable` (gap) | C2/C3/C6 |

## The genuinely missing connection (finding)

No inherited component compares the two periods' **respondent population,
estimand, response topology, wording or design signature** before permitting a
historical delta:

* L1 identity law is family/country/calendar only;
* L2 shared-structure is structural (overlay schema), not population identity;
* L10 comparator validates each wave's own topology/design/authority but has no
  cross-wave population-equality check;
* L9 world is a rule-world and never sources population.

EE1 therefore **ADAPTS** the inherited exact-key discipline (L4's
"permission required" semantics) into `population_estimand_gate`
(`runtime/ee1_temporal_owner.py`) and binds it into the consumer chain order:
identity → population/estimand → clocks → comparability authority → delta.
This is the smallest connection that makes "changing sampling frame or source
edition that does NOT support the apparent numerical comparison" detectable,
and it is severed-and-RED-proven (witness W2; see 03).

## Why not a new temporal engine (commission constraint honored)

The experiment reuses the actual V553 chain end-to-end for identity,
comparability authority, multi-wave authorization, delta permission and
absence typing, and reuses the accepted T35 world as the consumer. New code is
limited to (a) the population/estimand identity gate, (b) clock-discipline
composition, and (c) the comparison consumer product — together under 300
lines, each severed by an executable witness.
