# SOROK B01/B03 AGENT B RELAY — B03 verification and B02 advancement

**Round:** Pair1, same persistent Agent B versus the same Pair1 Agent A.
**A result inspected:** `5bc29474e769b928d9264f1607bab605e2b1c7e9`.
**A implementation:** `99333985190d872d825a1ec205db224179daa4af`; B03 feature `6deb7b71d0f8d761ae7734868c693dcb5dd253d8`.
**B implementation this round:** `509784c2850c499d1f640c9f43c569416081d76d`.
**Branch:** `codex/sorok-duel-b03-counter-b02-b-20261112-r1`.
**Running contract SHA:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`.
**Protected inspection baseline:** `6a5c12f04323d74001f9632063ec907f4fc4468e`.
**Grade:** `SOURCEFREE_S2_ONLY`. No native science, actor/human right, source right, Pyat rule, S14/A5 grant, or protected merge. No terminal acceptance is claimed.

## 1. Valid A corrections and concessions

A's relay and B03 work are not being disparaged for competition. These are real improvements and I preserve them:

1. **A found a genuine error in my B01 prefix repair.** My `branch_is_ancestor` trusted `inherits_verified_prefix`/`shared_root_equal` and the mutable branch `root_counts`. A's `_copied_prefix_equal` compares the actual copied episode/world-event/checkpoint/perception prefix rows per fork edge and verifies the branch root hash. A's `test_actual_copied_prefix_not_mutable_root_counts` passes independently. I concede this was a real hole in my earlier work.
2. **A correctly exposed fork scope at the P6 consumer.** `read_household` and `parent_choice_input` now carry `provenance` (`stored_branch`, `current_branch`, `inherited`, `scope=P6_MATERIAL_FACT_ONLY`, `fork_state`), and the parent source carries the same inherited/fork markers. This is additive and does not rebind the stored fact. B01's own tests remain green.
3. **A closed real B01 evidence gaps.** The post-fork epoch refusal/restore and the child `GO` stored-on-child/parent-house-provenance tests are genuine additions. A's claim that the child event body retains parent house provenance is verified.
4. **A's B03 is actual construction, not narrative.** `p6_dwelling` is one P2 world resource through the existing checkpoint writer. `read_dwelling` cross-checks the B01 household/place/owner/landlord and P6 room set. `material_feasibility` returns real `ADMISSIBLE`/`REFUSED`/`UNKNOWN` verdicts from committed space/acoustics/tenancy/cost facts and live household cash. It does not create a drum-kit object, class trait, possession, or mother action. A's 8 B03 tests pass independently.
5. **A's P3 code-pin disclosure is correct.** The byte change invalidates prior P3 roots; A did not hide or weaken it.

## 2. A's invalid, incomplete, or residual claims

1. **Same-root PsycheStore negative was missing.** A's B03 negative used a separate test store. I added `test_b03_same_root_psyche.py`, which writes a valid MEDIATOR into the actual P6 root's `p3_psyche.sqlite3`, verifies the world readers and mother material input are unchanged, severs `p6_dwelling` to make the world readers refuse, verifies the PsycheStore query still returns the mediator, and restores the exact baseline. This is an evidence repair; no B03 production change was needed.
2. **Ancestor provenance relabel remains.** Changing a stored branch to a different verified ancestor keeps the content source valid. A disclosed this. I did not add a checkpoint-history provenance ledger; that is not required for B02 and would be another security programme.
3. **Perception-prefix content is still partial.** A's prefix comparison includes perception `(seq,event_id,actor_id)` but not channel/clock; the fork root hash also excludes perception. This is an actor-perception residual, not a B02 material-period fact; I do not claim full perception-prefix integrity.
4. **B03 child new occupancy remains a boundary.** A's B01 household cross-check refuses a different dwelling/room/owner/landlord on a child. That is disclosed and not repaired; B03 can commit tenancy/noise/space/cost on the inherited home identity.
5. **B03 acoustic rule boundary remains.** `sound_rating_db`, `wall_construction`, `neighbor_shared_walls`, and `monthly_rent` are committed context; the bounded feasibility rule uses max indoor loudness, space/clearance, rent due/currency and live cash. This is a declared rule boundary, not a fabricated propagation/economic model.
6. **No false accusation is maintained against B03.** The class/trait, possession, unknown, severance, cold, child-fork, and source-link negatives hold. The same-root negative now also holds.
7. **Refuted/withdrawn B-side criticisms.** None of A's B01 corrections was false: the `root_counts` bypass, the missing P6 provenance, and the missing post-fork epoch test were all real. I also withdraw any implication that A's `_copied_prefix_equal` is merely a relabel of `root_counts`; it compares actual copied rows and is a substantive repair. I found no false A attack requiring a counterrefutation in this round.

## 3. New B02 construction

B02 was still unbuilt and blocks C02/D02. This round advances it as authorized CG-B construction:

- New `WORKER_RETURNS/SOROK-DUEL-B02-R1/historical_period.py`.
- `p6_employment` and `p6_historical_period` added to the bounded P2 material-slot allowlist.
- Explicit calendar/logical bases: `GREGORIAN_PROLEPTIC_UTC_DATE` and `S46_TEST_ONLY_LOGICAL_TICK_DAY_V1`, `ticks_per_day=1`, inclusive start/exclusive end.
- Two dated periods: `2026-01-01..2026-07-01` and `2026-07-01..2027-01-01`.
- Employment terms: term A effective `2026-01-01`, term B effective `2026-03-15`; the midperiod change splits the first S46 domain at anchor+73 days.
- `materialize_periods` calls the existing `session.produce_interval` with `SCHEDULED_ONLY` domains; the S46 states are `NOT_PERFORMED` (no daily work, no psychology).
- `read_material_period(as_of_date)` returns the containing dated period, logical tick, latest effective employment term (or explicit `UNKNOWN_NO_EFFECTIVE_TERM`), the actual S46 interval summary, source hashes, and material-only provenance.
- `p3_interval_span` returns exactly the existing `EventProposal.interval` shape; `P2Owner.validate_proposal` accepts it in the test.
- No new scheduler, clock, database, event journal, psychology, purchase, debit, recurring cost, or parent action.

B02 details: `WORKER_RETURNS/SOROK-DUEL-B02-R1/AGENT_B_HANDOFF.md`, `B02_ABI.md`, `PROGRAMMA_DELTA.json`, `impact.json`.

## 4. Corrections and repairs actually implemented

1. `p2_owner.MATERIAL_FACT_SLOTS` expanded for the two B02 facts; P2Owner constructor/`validate_proposal`/`realize`/participant methods untouched.
2. `historical_period` facts are written through `p2_owner.write_material_fact` and the existing S47/P2 checkpoint writer.
3. B02 materialization is idempotent by S46 domain hash: retry and cold reopen return `REPLAYED`, `produced_states=0`, identical state IDs and counts; no duplicate period.
4. B02 cold subprocess reads plan, employment, and material-period state identically.
5. Employment transitions are as-of correct: pre-term is `UNKNOWN_NO_EFFECTIVE_TERM`; before the change returns term A; after returns term B; no stale term survives the effective date.
6. Severance/restore of either employment or plan fact refuses and then restores exact baseline.
7. Clock/term tampering is refused; outside-plan date is refused; custom-date plan anchor/clock mapping is tested.
8. Fork period facts are material-only; `materialize_periods` on a fork is refused; the S46 interval is `NOT_AVAILABLE_ON_FORK`, not fabricated.
9. B03 same-root PsycheStore negative is now an actual executed test (no B03 production change).

## 5. Proof

| Suite | Result | Evidence |
|---|---|---|
| B02 period | **7 passed in 50.13s** | `SOROK-DUEL-B02-R1/evidence/b02_period.log` |
| B01 + B03 + B03 same-root + B02 combined | **27 passed in 165.75s** | `SOROK-DUEL-B02-R1/evidence/b01_b02_b03_combined.log` |
| P6 house + P2 owner + actor scene + selected P3 reopen/config | **17 passed in 217.45s** | `SOROK-DUEL-B02-R1/evidence/p6_adjacent.log` |
| P6 MII | **18 passed in 242.53s** | `SOROK-DUEL-B02-R1/evidence/p6_mii.log` |
| B03 same-root PsycheStore negative | **1 passed in 7.18s** | `SOROK-DUEL-B03-R1/evidence/b03_same_root_psyche.log` |

The B02 proof includes actual date arithmetic, two periods, midperiod split, source clocks, employment as-of change, actual S46 interval state IDs, cold/retry no duplicate, severance/restore, tamper refusal, custom plan, P2 material reads, and exact P3 interval validation. The B03 same-root negative is the actual P6 root store, not a separate test store.

## 6. Preserved functionality and boundaries

- B01 household/read behavior, B03 dwelling/feasibility/mother input, P6 house, P6 MII, and P2 owner suites remain green.
- No P6 `situated.py`, MII/MIII owner, P3 file, `model_cycle.py`, `supporting_actor.py`, shared guide, CURRENT_PROGRESS, workflow, Pyat, credential, or global config was edited.
- No new owner, scheduler, person-world ledger, clock, database, event journal, economy, or universal world/psyche engine.
- No PsycheStore record, class label, trait, mother decision, utterance, hidden reason, possession, purchase, debit, or recurring cost enters the period/feasibility readers.
- S46 `SCHEDULED_ONLY` states mean period/clock state, not performed daily activity.
- Native/science/rights/human/merge holds remain separate.
- The two complete ChatGPT Library architecture records remain **NOT_INSPECTED locally**; no contents claimed.

## 7. New attack surfaces

1. **P3 code-pin break is wider.** The p2_owner byte change invalidates A `5bc29474`/`993339851`, B `362719b40`, and earlier P3 roots. Fresh final-code roots only; no migration.
2. **B02 is not a full P3 cycle.** It exposes the exact interval and material-period ABI but does not run a P3 DevelopmentOwner batch or write psychology.
3. **Partial crash atomicity remains.** Employment/plan writes are two checkpoints; a crash after S46 issuance but before state can leave an orphan issuance. Existing interval states are reused, so no duplicate period state is produced, but this is not a crash-atomic multi-fact transaction; B04/E03 own recovery.
4. **Fork S46 interval is unavailable.** Period/employment facts can be read with material provenance, but interval state is not forked; `materialize_periods` refuses on a fork.
5. **B02 plan is one-shot at its anchor clock.** A later-clock plan update, new period, or re-anchoring is not provided; B05/multicycle work must add one deliberately.
6. **B03 residuals remain** (child new occupancy, ancestor relabel, perception-prefix content, acoustic rule boundary). They do not block B02.
7. **Pair2 D02 input must not be silently rebased.** Active D02 work with `acfcb72f49102cd2fdc7d165b1d5a8e2b5b60f5d` can consume B02 only after HQ reconciliation at this ABI.

## 8. Surviving disagreements and material questions

- Should B02 use the existing `SCHEDULED_ONLY` S46 state as the material-period representation, or is a separate period interval type required by the next P3 cycle? I used the existing producer and state and did not invent a second interval owner.
- Is the one-day-per-tick sourcefree mapping acceptable, or does the next consumer require a different explicit ticks-per-day/per-month convention? It is frozen as `ticks_per_day=1` and exposed in every read; a different convention needs a new plan source/basis, not a silent change.
- Should employment be separate from the B03 dwelling/feasibility material fact? I kept it separate because B02 is a period/as-of fact and B04 owns work/care consequences; no duplicate ledger.
- How should the P3 pin break be migrated? Not in this lease; fresh roots are tested.
- Can the ancestor relabel/perception-prefix residual be repaired without a second provenance ledger? A's challenge remains open.
- Full P3/D02 consumption, cold fork, B04 purchase/debit, B05 recurrence, and parent decision/utterance remain unproved.

## 9. Challenge to SAME A

1. Attack B02's partial materialization: crash after issuance before state, retry, and show the exact owner/step that must reconcile the orphan. Do not accept a duplicate period.
2. Attack the date/clock boundary: custom anchor, leap day, period-boundary employment change, later-clock restore, and clock tamper. B02 must refuse/UNKNOWN, not silently re-anchor.
3. Attack employment as-of: term before/at/after the anchor and period boundaries; no stale term. Try class/trait/extra fields; refuse.
4. Attack the P3 interval seam with a real `EventProposal` and later P3 cycle. Determine whether `SCHEDULED_ONLY/NOT_PERFORMED` is the correct material-period representation.
5. Attack fork period reads and materialization; no S46 interval may be fabricated on a child.
6. Solve or price the P3 pin migration without weakening pins or rewriting accepted state.
7. Consume B02 in D02/C02 without silently rebasing Pair2's active input and without turning employment into a mother action/trait/possession.

**Returned for the same rival, not terminal acceptance.**
