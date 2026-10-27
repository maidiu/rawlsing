# M16 — direct source map

**Court:** HISTORICAL_V3 / EXACT_MECHANISM; X03 independent source return, awaiting independent review. **Coverage:** PARTIAL_WRONG_MEANING

**Source identity:** X03 sealed startup `2647a4cf25d8bb33a00471e1af9c5e58c2825efb`; direct read-only files are hashed in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`. The S50-selected files are 31/31 exact. X03 files outside S50 were matched to `CAN_011_V3_MIDDLE_STATE/AUTHORITY.json`, `CAN_012_V3_RUPTURE_METABOLIZATION/AUTHORITY.json`, `CAN_010_V3_NEED_EXPECTATION_STRIVING/AUTHORITY.json`, `ADP_007_V3_ACTOR_INITIALIZATION/AUTHORITY.json`, or are explicitly local-source-only. The local staging zip `3f2c5ed9…` is not the TD-R05 archive `953c9149…`; archive-level exactness is not claimed.

**Claim ceiling:** historical source and sourcefree probe behavior at the cited grain. This is not current C9/C12 integration, a native person, a scientific law, or a source/actor/C8/C9/C11/C12/Pyat grant.


## Function and call-path map

| Symbol | File:lines | Inputs | Actual operation | State read/write | Callers/consumers | Test entry |
|---|---|---|---|---|---|---|
| `StrivingObject` | `v3/core/state.py:312–336` | id, label, axis, age, investment, identity load, feasibility, support, momentum, tags, secrecy, costs, active | persistent pursuit carrier | `striving_objects[]` | JSON; spawn/update; event targeting | presence tests only |
| `spawn_striving_objects_for_age` | `v3/engine/striving_objects.py:127–213` | age, expectation_baseline, existing, static proxy map, rng, config | nearest age bracket, weighted axis, static entry; random feasibility/support/momentum; budget by age | `striving_objects` | update_striving_step | no spawn test |
| `_make_object_from_entry` | `v3/engine/striving_objects.py:82–124` | YAML entry + baseline multipliers + rng | investment/identity from defaults*multiplier; feasibility 60/45 ±10; support 55 ±15; momentum ±10 | `new StrivingObject` | spawn | none |
| `update_existing_objects` | `v3/engine/striving_objects.py:216–239` | config, rng | momentum decay, investment/identity drift, random retirement, remove inactive | `striving_objects` | update_striving_step | none |
| `update_striving_step` | `v3/engine/striving_objects.py:242–272` | state age/year/baseline/config | setdefault all axes hopeful; update existing; unseeded spawn | `striving_objects; expectation_baseline` | yearly_step striving_update | test_step_logic full run only |
| `proxy map` | `v3/proxy_striving_map.yaml:1–…; v3/v3config.yaml:518–522` | static age/baseline lexicon + config | candidate labels/default investments | `static input` | spawn | none |
| `event targeting` | `v3/engine/expectation_events.py:169–186; v3/tests/test_wave4.py:169–187` | active striving objects | suggests fulfillment/violation targets | `events` | LLM Pass 1 | test_wave4 target presence |

## What is actually run

- Strivings are spawned by chronological age and a static YAML proxy map. `update_striving_step` calls `update_existing_objects` and `spawn_striving_objects_for_age` without an RNG, so each call constructs an unnamed `random.Random()`. Five fresh age-14 runs produced five different object sets: meaning/eros; beauty/belonging; belonging/eros; justice/eros; beauty/justice. The source is not replayable from state.
- The map supplies labels, tags, default investment and identity load. The runtime supplies random feasibility (60/45 ±10), random social support (55 ±15), random momentum (−10..10), and baseline multipliers. These are not observed support or activity.
- Existing-object update decays momentum by 0.6, drifts investment from momentum/feasibility/support, drifts identity load, and retires with probability 0.35 when investment<15 and identity<25. Retirement is random; the probe retired only at seed 1, not seed 0. No actual loss, failure, prohibition, or withdrawal is required.
- `update_striving_step` fills every missing expectation axis with `"hopeful"` every year. It does not read `events_this_year`, practice support, recognition, material opportunity, or contradiction. Event targeting can cite an existing object, but that is a proposal/consumer seam, not formation.
- The object has persistent identity and fields, but inactive objects are removed from `state.striving_objects`; historical retired objects are not preserved in that list. Pass 1/persona expose only active labels/investment.
- There are no tests for spawn, update, retirement, activity dependence, support dependence, or replay. `test_wave4` tests gift/disruption targeting and suggestion presence only.

## Real affordance

- Persistent object identity and lifecycle fields exist.
- Exact striving IDs can be referenced by later events; gift/disruption and Pass 1/persona consumers exist.
- The carrier supports investment, identity load, momentum, support, tags, secrecy, and costs as compatibility fields.
- Zero strivings is representable and lawful.

## Source-level REDs

- Age bracket and baseline map generate desire/direction without activity.
- Random support/feasibility/momentum and random retirement are unnamed RNG, not evidence.
- No actual object, activity, social recognition, practical support, contradiction, or prohibition input.
- `hopeful` fill and baseline multipliers manufacture a universal motivational profile.
- Retired history is dropped from the active list; no imposed/not-yet-thinkable distinction.

## Tests actually covering this mechanism

- `test_wave4` tests gift/disruption targeting and suggestion presence, not spawn/update.
- `test_llm_contract` checks serialization presence; no lifecycle test.
- No test covers age spawn, random support, retirement, activity dependence, or replay.

## Probe evidence

Probe evidence: five unseeded age-14 runs -> five different sets; seeded RNG7 -> two objects; empty baseline -> all ten axes hopeful; retirement at seed 1 only; no event input.

## Identity and authority note

CAN_010 explicitly rejects age-bracket spawn, baseline multipliers, random initialization/retirement, and the proxy map as desire authority; retains object identity and exact event attachment.

The source files and hashes are in `WORKER_RETURNS/X03/SOURCE_IDENTITIES.json`; the executable probe is `TEST_SOURCE_AND_LOGS/probe_x03.py` with output `probe_x03.json`. No production or source file was modified.
