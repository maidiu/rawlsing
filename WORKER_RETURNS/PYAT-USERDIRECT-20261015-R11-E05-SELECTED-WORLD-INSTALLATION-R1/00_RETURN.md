# R11 E05 — Productive selected-world N9/OC05 interface installation preparation

**Repository:** `maidiu/rawlsing` (private) · **Platform:** OpenCode · Kimi K2.7 Code
**Branch:** `agent/userdirect-pyat-20261015-r11-e05-selected-world-n9-installation-r1`
**Exact sealed startup:** `c7a15d0555f396b3f3f1700912cbc8687bec7d06`
**Disposition:** `SOURCEFREE_NONINSTALLING_N9_FACING_ADAPTER_BUILT_AND_EXECUTED__OC05_REAL_INSTALLATION_NOT_YET_APPLICABLE__COMPETENT_ADOPTION_UNISSUED`

## Outcome

A bounded, **noninstalling** N9-facing selected-world adapter now links the
accepted M4/M5 V557/V558 publication + M5 RSC machinery, E04's sealed sourcefree
selected-world possibility service, and HQ297 N9C's exact two-field reader
contract through a **versioned request / acceptance / receipt** interface.  It
carries exact native field values, publication/as-of clocks, source and
permission identities, and a nonpooled multi-field readset, with atomic selected
snapshot consistency and typed partials.  **271 pytest cases PASS / 0 FAIL**,
plus a genuine separate-process cold replay.

| Suite | Cases | Grade |
|---|---:|---|
| E05 adapter tests | **38** | newly authored sourcefree |
| E04 candidate baseline | **37** | sealed immutable candidate (NOT independently accepted) |
| HQ297 N9C owner reader | **47** | exact accepted-owner contract |
| M4/M5 publication + RSC | **30** | accepted owners, unmodified |
| Empirical N10E/C1/F8 chains | **101** | accepted owners, unmodified |
| E03 N9/N10W progressive | **18** | sealed candidate |
| **Total** | **271** | 0 failures / 0 errors / 0 skips |
| Genuine cold process (`first` → fresh-interpreter `replay`) | — | bit-identical receipts |

## What was audited

The **actual canonical** `objective_consumer_bounded_evidence.installation_manifest()`
is read, never edited.  It reports:

| policy | current applicability | consumer seam |
|---|---|---|
| OC01 | `APPLICABLE_CURRENT` | `rawlsing_next.pre553_empirical_query.execute_empirical_query` |
| OC02 | `APPLICABLE_CURRENT` | `rawlsing_next.pre553_structural_admission` |
| OC03 | `NOT_YET_APPLICABLE` | `None` |
| OC04 | `NOT_YET_APPLICABLE` | `None` |
| **OC05** | **`NOT_YET_APPLICABLE`** | **`None`** |

`evaluate_current_consumer(policy_id=OC05, …)` still raises
`NotYetApplicableConsumer` before any values-read.  The adapter never claims
otherwise: every receipt carries `operative_N9=False`, `operative_OC05=False`,
`issued_N5N6=False`, `issued_EE13=False`, `grade=NONINSTALLING_SOURCEFREE_ADAPTER_CANDIDATE`,
and embeds the live manifest.

## The versioned interface

`R11_E05_N9_SELECTED_WORLD_INTERFACE@1` with three schema versions:

* `N9_SELECTED_WORLD_REQUEST@1` — purpose, structural readset, empirical target
  + ordered conditioner/value bindings, the **two separately native field roles**,
  an explicit synthetic clock pair (`mode`, `valid_at`, `published_asof`,
  `test_now`), and the anti-pooling / anti-person / anti-model request flags.
* `N9_SELECTED_WORLD_ACCEPTANCE@1` — binds the request to **one** atomic snapshot
  (snapshot hash, catalog hash, empirical source identity, permission roots,
  publication and effective clock pairs, per-field clock bindings) and records
  typed inconsistencies.
* `N9_SELECTED_WORLD_RECEIPT@1` — the result-bearing object: real structural
  values, the real empirical exact fractions, and both native field values with
  their own native units, plus two explicit identities (a total float-free
  semantic hash and a byte digest over the verbatim payload).

## Positive consumers (one current, one historical)

Both sinks serve `SELECTED_WORLD_VALUES_SERVED` with zero inconsistencies:

| | CURRENT_TEST_CLOCK (2027-09-01) | HISTORICAL_AS_OF (valid 2026-06-01, pub 2026-03-01) |
|---|---|---|
| structural readset | `training_access=False` (rev 2), `exit_cost=8` (rev 2) | `training_access=True` (rev 1), `exit_cost=2` (rev 1) |
| empirical | 9/16, 5/8, 3/4 over 32/16/8 | identical |
| GSS (dwelling) | 2 388 192 / 3 288 063, published 72.6 % | identical |
| NCA (subscription) | 23 414 527 active | identical |
| NONPARENT_OPTIONS | `OPTIONS_AND_SOURCE_SUPPORT_PRODUCED` | `OPTIONS_AND_SOURCE_SUPPORT_PRODUCED` |
| CONCEPTION_SCENARIO_PROPOSALS | `FINITE_PROPOSALS_EVALUATED` | `FINITE_PROPOSALS_EVALUATED` |

A third sink, a published-as-of clock **before** NCA's publication, is a typed
`TYPED_PARTIAL_SELECTED_WORLD`: GSS only, NCA typed
`NOT_PUBLISHED_AT_SELECTED_ASOF`, both refs still in the dependency readset, and
no fabricated value.  Every positive number is independently precommitted in
`freezes/01_PRECOMMITTED_SELECTED_WORLD_EXPECTED_VALUES.json` before execution,
so a missing positive path cannot hide behind a TYPE_HOLD.

## Channel separation

* Empirical `Y` source mutation → only the empirical channel changes
  (19/32, 11/16, 7/8); structural values and both native field records are
  byte-identical.
* Structural revision → only the structural channel changes; the empirical
  geometry and both native field records are byte-identical.
* An unrelated native field perturbation changes no dependency, no value read
  and no consumer state.
* Revoking one world field permission changes only the dependent world route;
  the empirical channel and the native readset are untouched.  Revoking the
  empirical scope changes only the empirical channel.

## Two separately native units, never pooled

GSS carries `RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING` (households, `GHANA_RURAL`)
and NCA carries `ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS`
(subscriptions, `GHANA_NATIONAL`).  Both refs, both values and both native units
are carried separately.  There is no cross-field ratio, product, pooled value or
common denominator anywhere in the receipt; `pooling`, `person_exposure` and
`model_use` are hard `False`, and the two roles must stay in two distinct source
families or the receipt is refused.

## Hostiles executed

Wrong source/release binding, acceptance binding, snapshot substitution, wrong
publication clock (per-field clock pair against the one selection clock),
swapped native field role, foreign native field ref, source-class collision,
wrong native unit/geography/measure, person-inference labels, wall clock and
non-historical clock modes, pooling/person/model request flags, unknown
structural field, unknown native field role, duplicate field role, bad request
grammar, per-field mutation invalidation, revoked-scope invalidation, replay
determinism, and the exact N9C reader refusal taxonomy.

## Preserved and not reinvented

C1/N10E, Field Forge and N5/N6 arithmetic are executed by their own accepted
modules (`provide_empirical_possibility_slice`,
`compose_positioned_subject_possibility`,
`evaluate_positioned_subject_possibility`, `execute_empirical_query`); no
parallel estimator is published.  Every accepted owner blob is byte-identical
between the startup tree and the staged runtime.

## Files

| Path | Purpose |
|---|---|
| `repro/e05_n9_selected_world_adapter.py` | the versioned noninstalling adapter |
| `repro/emit_e05_expected.py` | precommits expected values to `freezes/` |
| `repro/stage_e05.py` | stages the exact sealed closure |
| `repro/run_e05_suites.py` | executes every graded suite |
| `repro/e05_cold_process.py` | genuine separate-process `first`/`replay` |
| `tests/test_e05_n9_selected_world.py` | 38 E05 tests |
| `freezes/01_PRECOMMITTED_SELECTED_WORLD_EXPECTED_VALUES.json` | precommit |
| `observations/*.xml`, `*.log`, `cold_*.json`, `source_manifest.json` | JUnit, stdout, cold evidence, staged object manifest |
| `01_`…`04_` | interface + authority residual, two-field owner trace, positive + hostiles, holds |
| `environment_passport_delta.json` | environment, sealed blobs, OC05 manifest, suite tallies |

A distinct independent court is required before any sourcefree acceptance or
adoption; adoption remains with the competent N9/OC05 owner.
