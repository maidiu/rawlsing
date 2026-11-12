# SOROK D02 Agent A relay — qualified acquired state and current B02 ingress

**Task:** `D02` — actor-local situated-field projection of actual world, state and accessible relations.
**Status:** `IN_PROGRESS_PREREQUISITE_HELD` overall, but the two bounded gaps in this round are implemented: a qualified read-only **acquired-state contribution** through the existing P3 store/activation/projection machinery, and an actual **current B02 period ingress** with explicit historical/interleaving holds.
**Programme:** #939 / PR #938 at `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Branch:** `codex/sorok-duel-d02-a-acquired-period-20261112-r1`.
**Composition start:** `0c460c7a2a3ed0b6f485b1cc3131bef1b18c0569` (A D02 `76547199...` + C02 B `4d93685d...` + B02 B `4f78bf71...`).
**B return examined:** `0ac3002b94e8a5ebc31842c2686a6a664e8cd63a`; B code cut `dba782ddf15dd9d8db261c08b515944dcea4b8e4`.
**A code cut:** `71cd4dda7dde8d698c8b5146ec69224821297a9c`.
**Ceiling:** `SOURCEFREE_S2_ONLY`; no native CAN/ADP/Pyat, actor/human/source right, production or protected merge.

## 1. Exact artifact

| Path | SHA-256 / change |
|---|---|
| `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/situated_context.py` | `434843b1c1ecfa892cadd585d39e2a3921914ad7ce5ed6f4d36bd8ffeadab11b`; acquired-state activation and current B02 ingress. |
| `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/INTEGRATION_CONTRACT.md` | `4eabe29ce3f2bd884cd782b97d18046490865870285a9e1a75b57b2fdd14c4df`; additive optional D02 interface/source/evidence limits only. |
| `WORKER_RETURNS/SOROK-DUEL-D02-R1/D02_B02_INGRESS_CONTRACT.md` | `8e43dc53d32bc057ce60b1de7e3d9ea82d39fa4ee660690d5cd2bafbd308f2b0`; actual current-period ingress, historical/interleaving hold. |
| `WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/test_d02_a_acquired_period.py` | `ffb889caf3dc5f005861f7b7f71b12cf39273de938e9beae05d38f0dc7c934f9`; four new tests. |
| `WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/test_d02_composition_prereq.py` | `47bcca8ea843290a0a057cb07abc6ad4b8bdaed17bfead6cbe889a34baaeb76c`; acquired + B02 period added to fresh-root composition. |
| `WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/test_d02_b_repairs.py` | `d9ad684dc5b0359872caf68e5ba9124c19d97cbe7a1a419558948e522b594e62`; only the stale `B02 unbuilt` assertion/name updated to the source-present hold. B's other tests unchanged. |

No P2/material/period/supporting_actor/parent_activity/P4/P6/vendor source was edited. No new store, scheduler, rule, world writer, native science, rights or protected merge. The B02 module is imported read-only from `WORKER_RETURNS/SOROK-DUEL-B02-R1/historical_period.py` (SHA-256 `78e33649ed7c2a50d1cdea1692f04ea79ddb841748f7532d576c0436647ded22`).

Commands run (worktree root, no bytecode):

```sh
python3 -B -m pytest -vv -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-D02-R1/tests/
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-D01-R1/tests/
python3 -B -m pytest -q -p no:cacheprovider \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_state_store.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_rules.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_projections.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_owner.py \
  WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests/test_p3_goal_residuals.py
python3 -B -m pytest -q -p no:cacheprovider WORKER_RETURNS/SOROK-DUEL-B02-R1/test_b02_period.py
```

Observed:

| Suite | Result | Evidence |
|---|---|---|
| D02 all (A prior + B repairs + new acquired/period) | **20 passed in 866.40s** | `evidence/d02_a_acquired_period_all.log` |
| D01 all | **15 passed in 92.03s** | `evidence/d02_a_d01_regression.log` |
| P3 owner/store/rules/projections/goal-residual | **77 passed, 1 skipped in 51.12s** | `evidence/d02_a_p3_regression.log` |
| B02 source suite at this composition | **7 passed in 53.02s** | `evidence/d02_a_b02_source_regression.log` |

## 2. B's valid findings and improvements — conceded

1. **D02-B1 event-time selection is a real bug I missed.** My `_latest_perceived` tied candidates on the access reader's current `world_clock` and then selected a lexical action ID. B's actual-event/constant-clock evidence is correct. I preserve B's event-time/ordinal selection and checks.
2. **D02-B2 access-hash conflation is real.** Hashing the whole access document including read-time `world_clock` changed historical access identity when the clock advanced. I preserve the normalized event-access identity and read-world-clock separation.
3. **D02-B3 event/current co-presence conflation is real.** My single `co_present` field did not distinguish selected-event shared perception from current objective position. I preserve `event_co_present`/`current_co_present` and the both-required option.
4. **D02-B4 source-closure gap is real.** A D02 selector change did not invalidate the context closure. I preserve B's 12-file base closure and add a separate exact B02 `period_source` for the newly selected period reader, without expanding the global P3 pin.
5. **D02-B5 pending-operation refusal is correct.** I preserve it.
6. **D02-B6 read-boundary label correction is correct.** The P3 snapshot reads the head; claiming `psyche_store: NOT_READ` was false. I preserve `P3_HEAD_ONLY_NOT_RECORDS` when no plan scope is supplied and use `P3_ACQUIRED_RECORDS_ACTIVATION_READ` only when the explicit plan scope reads records.
7. **D02-B7's B02 hold was correct at B's cut.** At this composition the B02 source is present, so a global `B02_UNBUILT` claim is stale. I replace it with an actual current-period ingress and an exact historical/interleaving hold; B's hold test is updated only for that source-present distinction.
8. **B's D01 concession and its own limits are accepted.** No new D01 retention round was opened.

## 3. My own mistakes, false attacks and corrections

- **My D02-3 “bounded scan” description was insufficient.** B correctly exposed the constant-read-clock/lexical-ID failure. I did not defend it. The new selection basis is B's event time/ordinal.
- **My `psyche_store: NOT_READ`/P3_HEAD_ONLY claim did not address the actual acquired organization.** I previously wrote only that the head was read; that was truthful but incomplete for D02's user-described semantic gap. The new acquired-state path reads exact scoped records through the existing projection owner only when an actual later plan is supplied.
- **My earlier period hold was not a finite source-present contract.** B's ingress contract was useful; the new code uses the actual B02 reader and only holds when no plan/current period is available. I did not claim historical D02.
- **No valid B attack is rejected as false.** I found no need to relitigate B's event/access/co-presence/source-closure repairs. The only B statement I revise is the now-stale “B02 globally unbuilt” status, supported by the source present at the composition start.
- **I edited B's hold test name/assertion** because the actual B02 source changed the truthful label. This is disclosed; no B production code or other B test was weakened.
- **I did not spend this round on B's exact-response rule-value gap or a broader hash/scanner arms race.** The acquired-state semantic field was the higher-value gap.

## 4. Implemented repair 1 — qualified acquired-state contribution

`build_situated_context(owner, *, plan=None, ...)` now accepts an explicit later P3 plan and performs a strict read-only activation:

1. Validates plan root/actor/branch, source hash, registry hash, sourcefree grade, sealed plan hash (when present), permitted rule descriptors, and scope selectors. It refuses caller override keys `actor_observed`, `material_eligible`, `eligible`, `eligible_modes`, `record_hashes` (`D02_PLAN_OVERRIDE_FORBIDDEN`).
2. Reads `owner.store.query(project, counterpart, as_of=owner clock)` only; it captures the store head before and after and refuses if it changed.
3. Builds the activation context with `actor_observed` derived **only** from the actual selected focal `read_actor_access` status, and `material_eligible` derived only from objective household material + focal position presence. It does not accept a caller boolean.
4. Runs the existing `p3.projections.activate` with the owner identity/registry. It does not add a rule or store; no target is written.
5. Returns a bounded acquired-state field: status (`NO_PLAN_SCOPE`, `NO_RECORDS`, `HELD_NO_ELIGIBLE_RECORD`, `ELIGIBLE`, `CONTRADICTION`), eligible modes/hashes, withheld entries, active contradictions, latent contradictions, stored count, activation-context hash, exact source/registry hashes, and `native_rule: MISSING_RULE` / `memory_formation: MISSING_RULE` / `first_person_claims: []` / `decision: NOT_EVALUATED`.
6. A stored record is not automatically recruited: role/relation/access inhibition yields `HELD_NO_ELIGIBLE_RECORD`; unrelated scope yields `NO_RECORDS`; contradictory eligible records yield `CONTRADICTION` and are not reduced to one mode; a no-plan request yields `NO_PLAN_SCOPE`, not “no psychology.”
7. The field is included in the body/readset/hash and in the **existing** `RecursionCycle` provider context. The provider remains transport; the actual later P3 response is also checked.

Actual-owner evidence: same-path, same-seed recognized/imposed histories produce the same P2 formation/event identity and different sourcefree mediator modes. After bootstrap, the selector reads the admitted target, and `RecursionCycle.advance(context=selector)` delivers `eligible_modes` `joint_check` or `private_check` plus the exact record hash to the actual provider input. The same later P3 event response streams carry that mode/hash; the store head is unchanged. A zero-history control yields `NO_RECORDS`, provider input `NO_RECORDS`, and `inspect_alone`; no record is fabricated.

Scope/role transfer: the acquired record scope is the sourcefree plan's `vertical:project`/`vertical:counterpart`, **not** the C01 registered parent. The composition test keeps the parent relation separate and asserts the parent secret is absent from acquired state. The historical B1 fixed counterpart is not relabelled as the mother.

## 5. Implemented repair 2 — actual current B02 period ingress

The selector imports the actual B02 module and uses its source, not a mock calendar:

- `read_period_plan` supplies the declared calendar/clock basis, anchor date/clock, ticks/day, periods and employment source.
- The current P3 logical clock is mapped through the plan anchor to a current date; the mapping must be integral; `read_material_period` must return `logical_tick == current P3 clock`.
- Employment holder slot `A` must resolve to the focal D02 identity actor. Holder-A employment is never applied to the registered parent.
- The bounded period output includes exact period id/bounds, current date/logical tick, current employment term/status, interval status (currently `NOT_MATERIALIZED` in these tests), typed `p3_interval_span` (`SCHEDULED_ONLY`, read-only, not applied), plan/employment sources, provenance, exact B02 `period_source` SHA-256, and `date_scope.calendar = B02_CURRENT_LOGICAL_PERIOD`.
- Missing plan, before/outside-plan current clock, non-day-aligned clock, or holder mismatch returns an exact `HELD` reason. A historical date is not accepted as current state; no future employment is read. Tampered employment/period source refuses and exact restore returns the baseline hash.
- The B02 materializer/interleaving is **not** claimed. The typed interval span is a seam read, not a P3 cycle execution.

Evidence: on a fresh actual root, the plan establishes at clock 222; current period `period:2026-h1`, `2026-01-01`, term `employment:workshop-cooperative`, span 181, `NOT_MATERIALIZED`; after a real P2 event advances the clock to 312, the current date is `2026-04-01` and employment is `employment:civic-works`; severing/restoring the period fact and tampering/restoring employment source behave as exact refusal/restore.

## 6. Regression, negative and cold evidence

- D02 all 20 passed; D01 15; P3 77/1 skipped; B02 source 7.
- Negative controls include unrelated scope, inhibited role (record withheld), contradictory modes (no single selection), caller override refusal, zero-record provider control, stale/foreign state, pending operation, household source severance/tamper, B02 absence/tamper, and no store-head movement from selector reads.
- Cold/restore: the composition test cold-reopens the actual root and then reads household, parent public access, acquired state and B02 current period; D01 later consumer exact hashes and store head preserved. The B02 period test severs/restores source and exact hash; the acquired provider test compares same-path deterministic recognized/imposed histories.
- The composition remains one fresh root at the final code cut; old-code/pin roots are an exact hold and were not rewritten.

## 7. Unfulfilled requirements and held seams

- Full D02 is **not accepted**: B02 historical period split/materialization/P3 interleaving are not built; only current-logical-clock period read is used. The B02 materializer is whole-plan and Pair1 A is counterstriking its API; B04/B05 own duration/purchase.
- C02 B's direct world mutations still make the normal P6 consumer refuse `P4_COLD_STATE_MISMATCH`; Pair3 SAME A is repairing that. Our tests do **not** prove the live P6 join; they prove the P3 provider input and read-only period/acquired state at their honest grade.
- No historical as-of query, no midperiod P3 cycle, no parent-authored act/utterance, no D03/D04/D05, no native CAN/ADP/Pyat, no actor/human/source rights, no C12 issuance, no protected merge.
- The acquired-state `actor_observed` is derived from the selected actual perception, not from a future later event; the actual P3 owner re-evaluates with its own event. This is a decision-input boundary, not proof of actor cognition.
- The B02 source is imported by path and pinned in `period_source`, not added to the base 12-file D02 closure; source changes invalidate the selector hash but the closure distinction is explicit.
- The `P3 INTEGRATION_CONTRACT.md` update is an optional D02 API/source/evidence section; it is not a constitution rewrite or native acceptance.
- Tokens/USD are `UNKNOWN`; only wall times are measured. Full P3 vertical/full estate and P6/C02 live join were not rerun.

## 8. Strongest remaining attack surfaces and challenge to SAME B

- **Activation context vs later event:** show a case where the selector's selected prior perception makes a record eligible but the actual later P3 event's own actor access should withhold it; propose the exact two-event/time contract rather than a provider bypass.
- **Contradiction semantics:** find a legitimate contradiction that should retain both modes versus one that should be withheld entirely; the current active/latent distinction is sourcefree, not native.
- **B02 current-period boundary:** attack day alignment, custom anchors, period boundaries, holder-A/focal mismatch, and a current clock just outside the plan. Do not treat a historical as-of read as current state.
- **Interleaving:** implement actual B02 period/P3 interval coupling with a later actor decision; do not silently apply whole-plan materialization or future employment.
- **Acquired-state source closure:** decide whether `period_source` and `projections.py` belong in the same exact closure or a symbol-level closure; do not weaken the file hashes.
- **C02/P6 seam:** Pair3 must prove the live P4/P6 consumer; our selector proof stands only at its stated provider/read boundary.

**Hardest concrete challenge:** using the actual B02 plan and the actual P3 owner, build a dated period split that advances through an actual P3 batch and causes a later actor decision/response to consume the period/employment input, then cold-replay the exact eligible readset. If B02 materialization remains whole-plan, return the precise current-period/P3-interleaving hook that Pair1 must provide; do not fabricate a calendar or treat the period as a mediator.
