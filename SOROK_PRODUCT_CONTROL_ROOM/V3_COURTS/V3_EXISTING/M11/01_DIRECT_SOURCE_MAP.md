# M11 — direct source map

**Court:** HISTORICAL_V3 / EXACT_MECHANISM; X03 independent source return, awaiting independent review. **Coverage:** PARTIAL_WRONG_MEANING

**Source identity:** X03 sealed startup `2647a4cf25d8bb33a00471e1af9c5e58c2825efb`; direct read-only files are hashed in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`. The S50-selected files are 31/31 exact. X03 files outside S50 were matched to `CAN_011_V3_MIDDLE_STATE/AUTHORITY.json`, `CAN_012_V3_RUPTURE_METABOLIZATION/AUTHORITY.json`, `CAN_010_V3_NEED_EXPECTATION_STRIVING/AUTHORITY.json`, `ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json`, or are explicitly local-source-only. The local staging zip `3f2c5ed9…` is not the TD-R05 archive `953c9149…`; archive-level exactness is not claimed.

**Claim ceiling:** historical source and sourcefree probe behavior at the cited grain. This is not current C9/C12 integration, a native person, a scientific law, or a source/actor/C8/C9/C11/C12/Pyat grant.


## Function and call-path map

| Symbol | File:lines | Inputs | Actual operation | State read/write | Callers/consumers | Test entry |
|---|---|---|---|---|---|---|
| `Framework` | `v3/core/state.py:186–203` | id, weight, acute/chronic deltas, half-life, failure mode, enemy requirement, affinities, tenure | stores operator fields | `frameworks[]` | JSON; seed; update | no semantic operator test |
| `update_framework_weights` | `v3/systems/frameworks.py:33–102` | state.frameworks, events_this_year, plasticity_window, capacity/psych capacity | event weight deltas by index; then acute or chronic operator by tenure vs half-life; scale 0.3, cap 2 per field/year; tenure++ | `framework.weight/tenure; capacity; psychological_capacity` | yearly_step frameworks_update | test_step_logic::test_frameworks_update_applies_event_deltas |
| `enforce_framework_caps` | `v3/systems/frameworks.py:104–119` | state.frameworks | moves weight<5 to dormant entries; caps dormant list at 10 | `frameworks, frameworks_dormant` | yearly_step 37–43 | test_v5_framework_dormancy |
| `seed_frameworks_from_identity` | `v3/io/seed_frameworks.py:54–186,257–300` | religion/religiosity, SES, minority, age | creates faith/class/identity-search/in-group frameworks with age-derived tenure | `state.frameworks` | identity_to_backbone 607–625 | no focused seed/operator test |
| `Pass 1 consumer` | `v3/engine/llm_contract.py:599–603,676` | state.frameworks | exposes active non-placeholder IDs/weights | `Pass 1 summary` | run_llm_band | test_llm_contract presence |
| `update_domains` | `v3/systems/domains.py:50–56` | events only | does not read frameworks despite step-order input declaration | `domains` | yearly_step domains_update | test_step_logic domain delta only |

## What is actually run

- The operator path is real. `update_framework_weights` chooses `chronic_delta` when `half_life_years > 0` and `tenure_years >= half_life_years`, otherwise `acute_delta`; effective delta is `raw_delta * (weight/100) * 0.3`, capped at ±2 per field per year. The probe on a synthetic weight-100 framework showed binding +1.5 in years 1–2, then −1.5 in year 3 after the half-life switch.
- Frameworks are not acquired. They are seeded from religion, religiosity, SES, minority status, and age. Age sets `tenure_years` directly: a 40-year-old middle/dominant persona starts with meritocracy tenure 34 and institutional-trust tenure 32, so both are already chronic at first update. A 35-year-old religious/working/minoritized persona starts with age-based tenures and may be acute or chronic by arithmetic, not by lived duration of an acquired commitment.
- Event changes are positional: `framework_deltas[i]` changes `state.frameworks[i]`; there is no stable framework ID in the event. No path creates a new framework from instruction, participation, conversion, contradiction, or social use; no path reactivates a dormant framework.
- `failure_mode`, `enemy_requirement`, and `institutional_affinities` are stored but not read by the update or by the domain step. `framework_switch_sensitivity` only changes the event-delta cap; it does not select, switch, or acquire a framework.
- `enforce_framework_caps` moves any weight<5 framework to a dormant dict and caps that list at 10. There is no active-count enforcement of the declared `max_active=6`, no reactivation, and dormant entries are not full Framework objects.
- The step-order `domains_update` description says it uses frameworks, insulation, intensity, and practices; the actual `update_domains` applies only event `domain_deltas`. A probe with identical events but framework weight 5/practice 5 versus 95/95 produced exactly the same A=28, V=5, S=0, Aim=0 domains.

## Real affordance

- Acute/chronic operator arithmetic exists and changes psychological/material capacity.
- Framework persistence, weight caps, dormancy recording, JSON, and Pass 1 visibility exist.
- The synthetic half-life probe demonstrates an actual within-source temporal switch, not merely a field name.

## Source-level REDs

- A framework is an age/class/religion-derived recipe, not a historically acquired and used concept.
- Tenure is inferred from chronological age at initialization, producing an already-chronic adult stance.
- No acquisition, instruction, participation, scope, conflicting framework, use, dormancy/reactivation rule, or domain consumer exists.
- The domain step ignores frameworks, so the stated metabolic influence on A/S/V/Aim is absent even though capacity effects exist.
- Positional event deltas and hardcoded operator scale/cap are not stable-ID or semantically governed.

## Tests actually covering this mechanism

- `test_step_logic::test_frameworks_update_applies_event_deltas` — weight delta only.
- `test_v5_framework_dormancy` — weight<5 and JSON only.
- No test covers acquisition, acute/chronic boundary, target consumption, reactivation, or a real historical tenure.

## Probe evidence

Probe evidence: child identity -> four frameworks with tenures 0–3 and acute phases; adult identity -> meritocracy/institutional trust with tenures 32–34 and chronic phases; synthetic weight-100 framework -> binding +1.5, +1.5, then −1.5; weight 4 -> dormant; domains identical under high/low framework weight.

## Identity and authority note

CAN_011 authority explicitly marks demographic recipes `REMOVE/REJECT`, weight/acute/chronic/half-life/tenure `COMPATIBILITY_ONLY`, and `framework_deltas` positional lists `REMOVE/REJECT`. The source still runs those legacy recipes.

The source files and hashes are in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`; the executable probe is `TEST_SOURCE_AND_LOGS/probe_x03.py` with output `probe_x03.json`. No production or source file was modified.
