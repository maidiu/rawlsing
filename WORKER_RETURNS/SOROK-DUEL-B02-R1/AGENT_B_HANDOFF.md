# SOROK B02 AGENT B — historical calendar / S46 period construction

**Packet:** B02 `Map historical calendar/as-of to existing P3/S46 logical clock and split periods`, CG-B.
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, actor/human right, source right, Pyat rule, S14/A5 grant, or protected merge.
**Branch:** `codex/sorok-duel-b03-counter-b02-b-20261112-r1`.
**Start/frozen A result:** `5bc29474e769b928d9264f1607bab605e2b1c7e9`.
**A B01/B03 implementation:** `99333985190d872d825a1ec205db224179daa4af`.
**B02 implementation SHA:** `509784c2850c499d1f640c9f43c569416081d76d`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.
**B02 ABI:** `B02_ABI.md`; machine records: `PROGRAMMA_DELTA.json`, `impact.json`.
**Main relay handoff:** `WORKER_RETURNS/SOROK-DUEL-B03-R1/AGENT_B_HANDOFF.md`.

## 1. Exact artifact

Code at `509784c2850c499d1f640c9f43c569416081d76d`:

| Path | Change |
|---|---|
| `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/p2_owner.py` | `MATERIAL_FACT_SLOTS` gains `p6_employment` and `p6_historical_period`. P2Owner constructor/`validate_proposal`/`realize`/participant methods unchanged. |
| `WORKER_RETURNS/SOROK-DUEL-B02-R1/historical_period.py` | Bounded historical-period module: two sourcefree P2 facts, explicit Gregorian-date/S46-tick mapping, employment as-of reader, idempotent S46 period materializer, actual material-period reader, exact P3 interval adapter. |
| `WORKER_RETURNS/SOROK-DUEL-B02-R1/test_b02_period.py` | Seven positive/negative/cold/fork tests. |
| `WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_same_root_psyche.py` | Closes A's strongest B03 evidence gap with an actual-root PsycheStore injection; no B03 production change. |

Evidence is under `WORKER_RETURNS/SOROK-DUEL-B02-R1/evidence/` and `WORKER_RETURNS/SOROK-DUEL-B03-R1/evidence/`.

Commands actually run with the qualified environment:

```text
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B02-R1/test_b02_period.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_household.py \
  WORKER_RETURNS/SOROK-DUEL-B01-R1/test_b01_fork_provenance.py \
  WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_dwelling.py \
  WORKER_RETURNS/SOROK-DUEL-B03-R1/test_b03_same_root_psyche.py \
  WORKER_RETURNS/SOROK-DUEL-B02-R1/test_b02_period.py
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_house.py \
  WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/tests/test_p2_owner.py \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_actor_scene_context.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py::test_process_reopens_same_actual_p2_root \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py::test_actual_p2_root_configuration_and_combined_statehash
/private/tmp/rawlsing-oct28-p1r1/venv/bin/python -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/test_mii.py
```

## 2. Independent reconstruction before trusting A

I read the frozen 27-packet programme, B02/B03 packets, the owner reconciliation, and the user-directed duration/material requirement before reading A's relay/B03 handoffs. My reconstruction:

- B02 must use the existing P3/S46 logical clock and P2 material owner. It must not rename workshop ticks as years or add a second scheduler. It needs actual calendar-date duration arithmetic, an explicit conversion to logical ticks, two dated periods, a consequential mid-period employment change that splits the period, an as-of reader that cannot return stale employment, and cold/retry replay without duplicate periods.
- B02 must not implement purchase, debit, recurring cost, mother decision, utterance, trait, or psychology. B04/B05/C03/C04 own those.
- B03 must commit dwelling/tenancy/noise/space/resource facts through P2/P6 and make a concrete drum-kit availability depend on them, with legitimate unknown/refusal states and no class-to-trait or possession creation.
- The two complete ChatGPT Library conceptual/operational sources remain **NOT_INSPECTED locally**; no contents are claimed.

## 3. A's verified improvements and my concessions

A's relay and B03 work is strong; these are genuine improvements and are preserved:

1. **Shared-prefix repair is valid.** My prior `branch_is_ancestor` trusted `inherits_verified_prefix`/`shared_root_equal`/mutable `root_counts`; A's `_copied_prefix_equal` compares actual copied episode/world-event/checkpoint/perception rows per edge and checks the recorded root hash. A's test `test_actual_copied_prefix_not_mutable_root_counts` passes independently. This was a real error in my B01 repair; A found and fixed it.
2. **P6 provenance disclosure is valid.** A surfaced `stored_branch/current_branch/inherited/scope/fork_state` at `read_household` and `parent_choice_input`, instead of exposing the scope only at `P2Owner.material_fact`. This is additive and B01's tests remain green.
3. **Post-fork epoch and child action tests are real additions.** The epoch-after-fork refusal/restore and child `GO` stored-on-child/parent-provenance tests close evidence gaps I left.
4. **A's B03 is actual source/consumer construction.** `p6_dwelling` is a real P2 world resource, `read_dwelling` cross-checks B01 household/place/owner/landlord and the P6 room set, and `material_feasibility` actually returns `ADMISSIBLE`/`REFUSED`/`UNKNOWN` from committed space/acoustics/tenancy/cost facts and live cash. It creates no drum-kit object, no class trait, and no mother action. Its 8 tests pass independently.
5. **A's P3 code-pin disclosure is correct.** The p2_owner byte cuts invalidate prior P3 roots; A did not hide or weaken this.

## 4. A's remaining gaps and my refutations/limits

1. **Same-root PsycheStore negative was missing.** A's B03 runtime negative used a separate test store, not the actual P6 root's `p3_psyche.sqlite3`. I added `test_b03_same_root_psyche.py`: a valid MEDIATOR is written through the actual root's PsycheStore protocol; `read_dwelling`, `material_feasibility` and `mother_material_input` remain unchanged and contain no kitchen/record hash; severing `p6_dwelling` refuses the world readers while the PsycheStore query remains; restoring returns the exact baseline. This is an evidence repair, not a B03 production change.
2. **Ancestor provenance relabel remains possible.** Changing a stored branch to another verified ancestor keeps the content source valid. A disclosed this; it is not repaired here. It does not block B02's dated period facts, and turning it into a new provenance-security programme would be disproportionate.
3. **Perception-prefix content is still partial.** A's prefix check compares `(seq,event_id,actor_id)` for perception rows; channel/clock are not part of the comparison or fork root hash. I did not add a perception-integrity ledger; this remains an actor-perception-owned residual for D02/D03, not a B02 material-period defect.
4. **B03 child new occupancy, cold fork, and acoustic rule boundary remain.** A disclosed them. B03 production is adequate for its packet; I did not fabricate a new-occupancy ABI or an acoustic propagation model.
5. **No false attack is asserted against A's B03.** The `social_class`/trait, possession, unknown, and source severance negatives hold; the same-root negative now also holds. The B03 boundary facts (`sound_rating_db`, `wall_construction`, `neighbor_shared_walls`, `monthly_rent`) are declared context, not used in the bounded rule; that is a documented rule boundary, not a hidden claim.

## 5. Repairs implemented — B02

### 5.1 Two sourcefree P2 facts

- `p6_employment`: versioned terms with effective ISO dates, employer/role/workplace refs, daily wage context, no debit.
- `p6_historical_period`: explicit `GREGORIAN_PROLEPTIC_UTC_DATE` and `S46_TEST_ONLY_LOGICAL_TICK_DAY_V1` bases, `ticks_per_day=1`, anchor date/clock, two contiguous periods, employment content source link.

Both use `p2_owner.write_material_fact` → the existing S47/P2 checkpoint. No second ledger or scheduler.

### 5.2 Dated split and actual S46 production

Default periods are `2026-01-01..2026-07-01` and `2026-07-01..2027-01-01`, anchored at the current session clock. The employment change at `2026-03-15` is exactly 73 days after the anchor; the first S46 domain is split into `(start, start+73)` and `(start+73, end)`, the second has one segment. `materialize_periods` calls the existing `session.produce_interval` with `SCHEDULED_ONLY` domains. The resulting S46 states are `NOT_PERFORMED` (no daily action, no psychology) but carry real logical start/end ticks and segment boundaries.

### 5.3 As-of reader and no stale employment

`read_material_period(session, as_of_date)` maps the date to a logical tick using the stored anchor, chooses the containing period, and selects the latest employment term with `effective_from <= as_of_date`. Before the first term it returns `employment=None`/`UNKNOWN_NO_EFFECTIVE_TERM`, never an old term. After the effective date it returns the new term. The actual S46 interval state is found by its domain hash; if absent it reports `NOT_MATERIALIZED`, and on an inherited fork it reports `NOT_AVAILABLE_ON_FORK` rather than inventing S46 state.

### 5.4 No duplicate period, cold replay, fork boundary

`materialize_periods` reuses exactly one existing S46 state per domain hash, refuses duplicate states, and refuses a missing interval whose start is already in the past. A retry returns `REPLAYED` and appends no period. A cold subprocess reopens the same state and returns identical plan/employment/material-period JSON. On a child fork, plan/employment material facts are readable with provenance, but new materialization is refused because S46 interval state is not forked.

### 5.5 P3 interval seam

`p3_interval_span` returns exactly `{"mode": "SCHEDULED_ONLY", "span": ticks}`; the test passes it to the existing `P2Owner.validate_proposal`, proving the next P3 cycle's interval seam accepts the mapping. No P3 file was edited.

## 6. Proof of improvement

| Command | Result | Evidence |
|---|---|---|
| B02 period suite | **7 passed in 50.13s** | `evidence/b02_period.log` |
| B01 + B03 + B03 same-root + B02 combined | **27 passed in 165.75s** | `evidence/b01_b02_b03_combined.log` |
| P6 house + P2 owner + actor scene + selected P3 reopen/config | **17 passed in 217.45s** | `evidence/p6_adjacent.log` |
| P6 MII | **18 passed in 242.53s** | `evidence/p6_mii.log` |
| B03 same-root PsycheStore negative | **1 passed in 7.18s** | `WORKER_RETURNS/SOROK-DUEL-B03-R1/evidence/b03_same_root_psyche.log` |

The B02 tests cover: date/duration arithmetic, two periods, 73-day midperiod split, logical ticks, employment before/after/absent, material feasibility of an actual later period read, source-clock preservation, P2 slots, no duplicate on retry, cold subprocess replay, severance/restore, clock/term tamper refusal, outside-plan refusal, custom plan anchor, and fork material-only/refusal.

## 7. New attack surfaces and unresolved questions

1. **P3 code-pin break is wider.** The final p2_owner has new material slots; every prior B01/B02/B03 cut's P3 roots refuse `P3_CONFIG_CHANGED`. Fresh final-code roots are used; no migration. P3/Pair2 receiving must decide migration.
2. **B02 is not a full P3 cycle.** It exposes the exact interval/read ABI but does not run a P3 DevelopmentOwner batch or write P3 psychology. Pair2/D02 or the next P3 cycle must consume it.
3. **SCHEDULED_ONLY is a period/clock state, not work participation.** The S46 intervals are `NOT_PERFORMED`; B02 does not claim actual daily work, care, or recurring material activity. B04/B05 own those.
4. **Partial crash atomicity is not solved.** `establish_period_plan` writes employment then plan; `materialize_periods` can leave an orphan issuance if it crashes between issuance and state. It will not duplicate an existing interval state, but it is not a crash-atomic multi-fact transaction; B04/E03 own that.
5. **Fork interval is unavailable.** S46 state is not forked. B02 fork reads are material-only; interval status is `NOT_AVAILABLE_ON_FORK`; no cold fork.
6. **B02 custom plan one-shot.** The plan/employment facts are one-shot at the anchor clock; a later-clock re-establishment or new-period update is not provided. B05/multi-period work must add a deliberate update path.
7. **Acoustic and B03 residual boundaries remain** (wall context, child occupancy, ancestor relabel, perception prefix content). They do not block B02's material-period proof.
8. **No full P3/D02 composition, no parent action, no purchase/debit, no native/science/rights/human/merge.**

## 8. Exact challenge to SAME A

1. Attack B02's partial materialization: crash after the S46 issuance but before the interval state, then retry. Show whether an orphan issuance can be reconciled without a duplicate period; if not, identify the exact owner/step that must handle it.
2. Attack the date/clock boundary: a custom plan with a period starting at a different anchor; a change exactly at a period boundary; a leap-year date; a clock mismatch; a plan restored at a later session clock. B02 should refuse/UNKNOWN rather than silently re-anchor.
3. Attack the employment as-of reader: a term effective before the plan, at the anchor, at a period boundary, or after the last period; no stale term may persist. Try a term extra field/class/trait; it must refuse.
4. Attack the P3 interval seam with a real `EventProposal`/`P2Owner.validate_proposal` and then a later P3 cycle. Show whether `SCHEDULED_ONLY` `NOT_PERFORMED` is the correct material-period representation or whether an existing S46 interval pattern should be reused differently.
5. Attack fork semantics: read plan/employment on a child, then attempt materialization; no S46 state may be fabricated. Attack the ancestor relabel and the perception-prefix content separately if actor perception is at stake.
6. Solve or price the P3 code-pin migration. Do not weaken pins or rewrite accepted state.
7. Consume B02 in D02/C02 without treating employment as a mother action, private reason, trait, or possession, and without silently rebasing Pair2's active D02 input.

**No terminal acceptance is claimed.** This is a sourcefree candidate for independent receiving.
