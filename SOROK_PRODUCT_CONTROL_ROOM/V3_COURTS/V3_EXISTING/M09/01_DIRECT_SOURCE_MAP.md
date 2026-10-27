# M09 — direct source map

**Court:** HISTORICAL_V3 / EXACT_MECHANISM; X03 independent source return, awaiting independent review. **Coverage:** PARTIAL_WRONG_MEANING

**Source identity:** X03 sealed startup `2647a4cf25d8bb33a00471e1af9c5e58c2825efb`; direct read-only files are hashed in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`. The S50-selected files are 31/31 exact. X03 files outside S50 were matched to `CAN_011_V3_MIDDLE_STATE/AUTHORITY.json`, `CAN_012_V3_RUPTURE_METABOLIZATION/AUTHORITY.json`, `CAN_010_V3_NEED_EXPECTATION_STRIVING/AUTHORITY.json`, `ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json`, or are explicitly local-source-only. The local staging zip `3f2c5ed9…` is not the TD-R05 archive `953c9149…`; archive-level exactness is not claimed.

**Claim ceiling:** historical source and sourcefree probe behavior at the cited grain. This is not current C9/C12 integration, a native person, a scientific law, or a source/actor/C8/C9/C11/C12/Pyat grant.


## Function and call-path map

| Symbol | File:lines | Inputs | Actual operation | State read/write | Callers/consumers | Test entry |
|---|---|---|---|---|---|---|
| `Crack` | `v3/core/state.py:150–160` | typed crack fields | stores type, intensity, latent pressure, active flag, origin year | `cracks[]` | JSON; seeders; update_cracks | no focused lifecycle test |
| `update_cracks` | `v3/systems/cracks.py:25–61` | state.events_this_year, config, plasticity_window | sums event crack_deltas by list index; caps intensity/latent delta; clamps | `state.cracks[].intensity/latent_pressure` | yearly_step cracks_and_alienation_update | test_step_logic::test_cracks_update_applies_event_deltas |
| `_get_crack_delta_cap` | `v3/systems/cracks.py:15–22` | config.cracks_rules.annual_update.intensify_range | uses only max of intensify_range as cap; no spawn/activation/decay | `none` | update_cracks | none |
| `ensure_min_cracks` | `v3/core/invariants.py:253–274` | state, config | appends active placeholder cracks until min_cracks; records degraded yearly_integrity | `state.cracks; yearly_integrity` | yearly_step.run_one_year 25–30; assert_backbone_invariants repair path | test_invariants::test_backbone_invariants_pass_on_default_state |
| `seed_cracks_from_identity` | `v3/io/seed_frameworks.py:193–250,303–353` | identity religion/religiosity/SES/minority, year, age | creates sacred/family/identity/class cracks from demographic identity; caps active at 3 | `state.cracks` | identity_to_backbone 607–625 | no focused seed test |
| `compute_metabolic_style` | `v3/core/derived.py:166–199` | state.cracks, capacity, coherence, hostage, insulation | crack_load contributes to contradiction load and metabolic style | `state.metabolic_style / derived` | cracks step derived schedule; Pass 1 | indirect smoke only |
| `active_cracks summary` | `v3/engine/llm_contract.py:604–615` | state.cracks | exposes active non-placeholder cracks to Pass 1 | `Pass 1 summary only` | run_llm_band Pass 1 | test_llm_contract presence |

## What is actually run

- `update_cracks` is event-delta only. It does not spawn, intensify from contradiction pressure, decay latent pressure, activate, deactivate, or reactivate. `derived` is accepted but not read. The only config rule actually used is the maximum of `cracks_rules.annual_update.intensify_range`; `spawn`, `latent_decay_if_insulated`, `activation_threshold`, `deactivation_threshold`, and `brittleness` are dead in this call path.
- `Crack.active` is written by the identity seeder and by placeholder repair, then never changed by the annual step. A latent crack remains latent forever; an active crack remains active forever, independently of later episodes, insulation, support, or repair.
- `ensure_min_cracks` manufactures two active `type="placeholder"`, intensity 5, latent 5 cracks on a default adult state. The function records `placeholder_repair.status="degraded"`, but it nevertheless satisfies the hard minimum and contributes to `crack_load`; Pass 1 hides placeholder types, so the model sees no crack while the hidden placeholder still affects derived style.
- `seed_cracks_from_identity` manufactures cracks from religion/religiosity, SES, minority status, and age. In the probe, an age-8 working, minoritized, religious persona received four cracks, three active; an age-40 middle, dominant, nonreligious persona received zero and then `ensure_min_cracks` supplied two placeholders. The identity recipe is not an actual contradiction episode.
- Several seeded `origin_year` formulas can point into the future for young ages: `_identity_coherence_crack` uses `year - age + 12` and `_class_aspiration_crack` uses `year - age + 10`. For an age-8 persona in 2000 these become 2004 and 2002. The field is not causally validated.
- The actual downstream consumers are `compute_metabolic_style` (crack_load), Pass 1 `active_cracks`, persona `norm_conflicts`, and mechanical event sampling. There is no direct crack consumer in `update_domains` or topology/boundary; the step-order claim that cracks respond to contradiction pressure/insulation is not implemented.

## Real affordance

- Typed persistence and JSON carrier exist.
- Cracks can receive bounded event-driven numeric deltas.
- The Pass 1 and persona surfaces can expose a crack label; the probe confirmed the carrier changes when an event explicitly supplies `crack_deltas`.
- The placeholder-repair degradation is recorded, rather than silently swallowed.

## Source-level REDs

- Minimum-count filler is substantive hidden state, not a harmless guard.
- Demographic/age seeds convert structure into personality pathology.
- There is no contradiction formation, activation, deactivation, decay, support, scope, evidence, or reactivation.
- Event deltas are positional (`crack_deltas[i]`) rather than stable-ID, so list order is identity.
- The probe shows a latent inactive crack at intensity 80/70 remains exactly unchanged after a no-event year; the code has no latent-decay path.

## Tests actually covering this mechanism

- `test_step_logic::test_cracks_update_applies_event_deltas` — event delta only.
- `test_invariants::test_backbone_invariants_pass_on_default_state` — accepts placeholder repair.
- No test covers spawn, latent decay, activation, deactivation, reactivation, demographic seed, or hidden placeholder effects.

## Probe evidence

Probe evidence: default adult -> two active placeholders; child identity -> four seeded cracks (three active); adult identity -> zero then placeholders; no-event latent crack -> unchanged; one event `crack_deltas[0]` -> intensity 10→20, latent 5→15.

## Identity and authority note

`v3/systems/cracks.py` comments and `v3config.yaml:277–292` describe spawn and activation, but the body reads only the intensify cap. `v3/OVERVIEW_INTEGRATED.md:174` restates the unimplemented rules.

The source files and hashes are in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`; the executable probe is `TEST_SOURCE_AND_LOGS/probe_x03.py` with output `probe_x03.json`. No production or source file was modified.
