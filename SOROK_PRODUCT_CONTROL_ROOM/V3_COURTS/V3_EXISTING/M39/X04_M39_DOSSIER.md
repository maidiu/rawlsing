# X04 M39 — band-age/manual rupture injection

**Court grade:** `HISTORICAL_SOURCE_AUDITED` + `HISTORICAL_RUN`; current integration `UNTRACED`.
**Coverage:** `REPLACE`; serious disruptions must be admitted events with provenance, not age-random injection.
**Authority:** historical server policy only; no native rule.

## 1. Direct source map

| Symbol | File:lines | Input → output | Actual role |
|---|---|---|---|
| `maybe_inject_rupture_at_band_age` | `v3/engine/effects/metabolization_effects.py:273-332` | state → shard/process/wound mutation | Band-age probabilistic rupture |
| `create_rupture_shard_from_event` | `metabolization_effects.py:144-214` | state + event-like dict → RuptureShard/Process/plasticity | Creates records; no canonical event id/parent |
| `RUPTURE_BAND_AGES` local constant | `metabolization_effects.py:277` | age → probability | `3:.60, 7:.70, 11:.65, 14:.60, 17:.55, 24:.45, 30:.30` |
| `update_wound_vector_from_rupture` | `metabolization_effects.py:239-270` | severity/domain/opacity → wound bump | Direct wound mutation |
| server call | `server/generation/simulation.py:538-539` | after `run_one_year` → injection | Runs outside event/year ledger |
| tests | `test_metabolization_effects.py` 6 passed | template/helpers | No test of band-age injection |

## 2. Actual behavior

- At exact band ages, `random.random()` compared to a fixed probability; then `random.choices` picks templates, severity, opacity.
- It uses the module-global `random` with no caller seed; server calls it outside any canonical event ledger after `run_one_year`.
- It creates `RuptureShard` + `MetabolizationProcess`, sets `plasticity_window`, and **directly mutates the wound vector**.
- Reviewer probe with `random.seed(1)`, age 3: 1 shard, 1 process, abandonment 50→58, fear 50→52; `state.events_this_year` unchanged; shard keys contain no event id, owner, access/source, causal parents or rule/version; `plasticity_window.years_left=2`.
- `create_rupture_shard_from_event` also uses template `get_template_for_age` and mode sampling (`random` or NarrationSupport), cluster candidate first; no canonical event parent.
- Server calls injection after the annual step and before the optional LLM band; the rupture is not in `year_record.event_ledger` and not in `llm_band_ledger` selected events.
- Tests cover `create_rupture_shard_from_event`/templates but **not** `maybe_inject_rupture_at_band_age`; no actor/world/source test.

## 3. N03/N05/N11 differential

N03/N05/N11 need **admitted, world/actor-grounded disruptions** with source, participants, access, clocks and a lawful transition; repair and no-change are distinct. M39 provides:
- real rupture/metabolization machinery (candidate reuse);
- age-band random event injection with no event ledger/source/actor/access;
- direct wound mutation outside event admission;
- no repair/no-change semantics.

**Coverage:** `REPLACE`; retain `RuptureShard`/`MetabolizationProcess`/`compute_metabolization_delta` as candidate machinery, remove automatic age ritual.

## 4. Disposition / first consumer / owner

**Retain:** rupture/metabolization record shapes, templates as candidate vocabulary, plastic window, mode/cluster computation (with owner review).
**Adapt:** drive only from admitted canonical events with actor access/source/participants; make band-age a source-grounded event generator, not a probability ritual.
**Create:** `OccurrenceAdmission`, `RuptureCandidate`, actor access and repair/no-change; no automatic age-based wound write.

First consumer: server year/persona sheets; rupture survivors; no current C9/C12 semantic consumer.

**Owner:** CAN012/CAN011/ADP019/ADP016 + C9/C12; no native grant.

**Negative/fault:** same state but no event yields a shard at age 3 solely by chance; a manual band-age injection with no event id/source changes wound vector. Both are source-edge faults for any claim that rupture is event-grounded.
