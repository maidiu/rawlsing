# M18 — direct source map

**Court:** HISTORICAL_V3 / EXACT_MECHANISM; X03 independent source return, awaiting independent review. **Coverage:** PARTIAL_WRONG_MEANING

**Source identity:** X03 sealed startup `2647a4cf25d8bb33a00471e1af9c5e58c2825efb`; direct read-only files are hashed in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`. The S50-selected files are 31/31 exact. X03 files outside S50 were matched to `CAN_011_V3_MIDDLE_STATE/AUTHORITY.json`, `CAN_012_V3_RUPTURE_METABOLIZATION/AUTHORITY.json`, `CAN_010_V3_NEED_EXPECTATION_STRIVING/AUTHORITY.json`, `ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json`, or are explicitly local-source-only. The local staging zip `3f2c5ed9…` is not the TD-R05 archive `953c9149…`; archive-level exactness is not claimed.

**Claim ceiling:** historical source and sourcefree probe behavior at the cited grain. This is not current C9/C12 integration, a native person, a scientific law, or a source/actor/C8/C9/C11/C12/Pyat grant.


## Function and call-path map

| Symbol | File:lines | Inputs | Actual operation | State read/write | Callers/consumers | Test entry |
|---|---|---|---|---|---|---|
| `RuptureShard` | `v3/core/state.py:367–384` | id, year, age, violated assumption, domain, opacity, prediction error, status, IRR, meaning attempts | persistent actor-specific rupture record | `rupture_shards[]` | JSON; persona; Pass 1 | presence only |
| `create_rupture_shard_from_event` | `v3/engine/effects/metabolization_effects.py:144–214` | event rupture/implicated/intensity + narration support | creates shard and process; maps intensity to severity; samples cluster/mode; sets plasticity window | `rupture_shards, metabolization_processes, plasticity_window` | delta_templates apply_deltas; maybe_inject | test_metabolization_effects; test_wave4 |
| `update_wound_vector_from_rupture` | `v3/engine/effects/metabolization_effects.py:217–270` | severity, domain, opacity | maps domain to wound, bumps primary/secondary | `wound_vector` | maybe_inject only | no test |
| `maybe_inject_rupture_at_band_age` | `v3/engine/effects/metabolization_effects.py:273–332` | state.age + global random + templates | age-band probability; template/severity/opacity selection; creates shard/process; bumps wound | `rupture_shards, processes, plasticity, wound` | server/generation/simulation.py:539 after run_one_year | no test |
| `event path` | `v3/engine/effects/delta_templates.py:331–358` | selected epistemic_rupture event | creates shard/process but does not call wound update | `rupture_shards, processes, plasticity` | run_llm_band apply_deltas | test_wave4 |
| `persona surface` | `v3/io/persona_sheet.py:270–284,414–439,928–934` | rupture_shards/processes | renders unresolved notes; expects nonexistent `metabolization_mode` attr | `persona output` | V2 persona | presence test only |

## What is actually run

- The LLM/event path creates a `RuptureShard` and one `MetabolizationProcess`, both status `"raw"`, and sets a plasticity window. It does not update the wound vector. The age-band server path calls both `create_rupture_shard_from_event` and `update_wound_vector_from_rupture`.
- Severity is inconsistent. `create_rupture_shard_from_event` maps `intensity` `"major"`/`"shock"` to `"major"`; every other value, including `"malheur"` and `"minor"`, becomes `"micro"`. `update_wound_vector_from_rupture` is passed the original `"malheur"` by the age path, so the process can be `"micro"` while the wound receives the +15 malheur bump. Probe: malheur event -> process severity micro, shard raw; direct malheur wound update changed abandonment 50→69; create-only left wounds unchanged.
- `RuptureShard.current_status` is created `"raw"` and never changed. `meaning_attempts` stays empty. `MetabolizationProcess` starts `"raw"` with empty narrators/provisional frame/reactivation triggers and remains so. Persona code reads a nonexistent `metabolization_mode` attribute in two places, so that branch is always false.
- `maybe_inject_rupture_at_band_age` uses hardcoded age bands (3, 7, 11, 14, 17, 24, 30) and global `random.random()/choices()`; template selection, severity, opacity, and mode are sampled. Probe at age 14 with seeds 0–19 injected 14 times, with process status raw, modes varying (accommodation, collapse, sealing, assimilation, mis_aim), and wound changes from the original severity.
- The server calls `maybe_inject_rupture_at_band_age` after every `run_one_year` (simulation.py:539). The event path is separate. There is no admission rule, pre-event actor-state hash, exact parent event, actor-specific basis, or rule receipt.
- The process severity `"micro"`/`"major"` makes `is_malheur(proc.severity, ...)` false in the yearly path; the `"malheur"` multiplier is therefore not reached for the malheur case. `reactivation_triggers` is never populated, so `delta_templates`’ reactivation bump has no matches.

## Real affordance

- Typed persistent shard/process records and JSON exist.
- Epistemic rupture events can create a shard/process through the event path.
- The age path can add a bounded wound increment; the direct malheur probe shows a real numeric effect.
- Pass 1/persona have rupture/context surfaces, even though they are incomplete.

## Source-level REDs

- Age-band probability is an automatic trauma generator without actor basis.
- Global/unnamed RNG violates replay and ADP-020 semantics.
- Severity mapping contradicts the wound update; malheur is silently converted to micro for the process.
- LLM event path has no wound update; age path does. The two causal paths disagree.
- Shard/process statuses and meaning attempts are never developed.
- The persona’s mode field does not exist; the displayed rupture meaning is incomplete.

## Tests actually covering this mechanism

- `test_metabolization_effects::test_create_rupture_shard_from_event` checks count/fields only.
- `test_wave4` checks shard/process creation from an event.
- No test covers wound path, age injection, severity mismatch, status, meaning attempts, or actor history.

## Probe evidence

Probe evidence: malheur event -> process micro/raw, create-only wounds unchanged; direct malheur wound update 50→69; age 14 seeds 0–19 -> 14 injections, all raw; persona mode attribute absent.

## Identity and authority note

CAN_012 explicitly rejects age-band/random injection, direct wound mutation, unnamed RNG, and label-only admission; it preserves immutable rupture history and a persistent process tracker. The source still implements the rejected shortcuts.

The source files and hashes are in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`; the executable probe is `TEST_SOURCE_AND_LOGS/probe_x03.py` with output `probe_x03.json`. No production or source file was modified.
