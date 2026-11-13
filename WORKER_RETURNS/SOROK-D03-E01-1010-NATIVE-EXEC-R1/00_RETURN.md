# SOROK #1010 — native execution and G2 handoff

**Disposition:** `NATIVE_INTEGRATION_EXECUTED__37_PASS__REAL_P3_PENDING_COVERED__G2_HELD__STOP`.

**Branch:** `sorok-1010-native-exec-g2-20261113-r1`
**Frozen source:** `b50d51214be038c4e8288d72e650b2f194a2c55e`
**Grade:** `SOURCEFREE_S2_ONLY`. No native psychological science, actor rights, protected merge, self-acceptance or G5 is claimed.

## 1. What was actually executed

From this real checkout, at the frozen commit plus the additive test in this return:

```sh
python3 -B -m pytest -q -p no:cacheprovider --tb=short \
  WORKER_RETURNS/SOROK-E01-J1-995-R1/test_j1_three_head_join.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_d03_e01_performer.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-B-R1/test_b_guard_unit.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-B-R1/test_b_hostile.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_a_final_custody_unit.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_a_final_hostile.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-B-R2/test_b_final_preflight.py
```

Observed: **35 passed, 0 failed, 0 skipped, 592.61 s** (`evidence/integration-run-1.log`).

The same seven files plus this return's real-reservation tests:

Observed: **37 passed, 0 failed, 0 skipped, 570.69 s**
(`evidence/integration-run-2-with-real-pending.log`).

Focused world/cold/pending run:

Observed: **4 passed, 197.52 s** (`evidence/cold-world-and-real-pending.log`).

Environment: Python 3.11.3, Darwin 22.3.0 x86_64, pytest 9.0.2. No CI run is claimed.

## 2. Genuine repair

No production defect was demonstrated in the seven required files. All seven pass unchanged at the frozen cut.

One **test-oracle defect** in this return's first draft was found and corrected: after a hostile provider inserts a real P3 `PREPARED` row, `BatchEngine` exists far enough to create its empty journal file before the provider call, so `journal-not-exists` was the wrong assertion. The corrected assertion is the substantive one: the journal contains **zero batches and zero events**, world events are unchanged, and the real P3 pending row remains. The production adapter was not changed.

## 3. Real P3 pending reservations, not only monkeypatches

`test_real_p3_pending.py` creates actual `PREPARED` rows through the frozen `PsycheStore.reserve` ABI (a real plan, real expected/base state, real psyche head). `pending()` reports them while `head()` is unchanged.

- Preexisting real reservation: D03 refuses at entry with `D03_PENDING_OPERATION`; provider never called, no world event, no cycle file, no journal, pending row retained.
- Real reservation created by a hostile provider after a real J1 receipt: the post-provider barrier refuses with `E01_POSTPROVIDER_P3_PENDING_OPERATION`; no world event, journal has zero batches/events, pending row retained.
- The earlier monkeypatched B R2 tests remain intact and pass; these new tests exercise the real store semantics rather than a stubbed `pending()`.

## 4. Actual P2 world events and cold recovery

`test_event_is_real_world_history_and_cold_first_consumer` and `test_j1_full_chain_and_cold_reopen` pass. They establish, at this sourcefree P2 scope:

- the existing `BatchEngine`/`P2Owner` writes real E1 events;
- the ordinary world reader (`session.read_event`) and the ordinary C9 conditioning reader see them;
- a cold reopen returns the same events and batch history hash with no duplicate writes;
- the P3 head is unchanged by the P2-only route.

This is actual P2 event execution and recovery, **not** evidence that Nadia selected the activity.

## 5. G2 determination — still held

| # | #1010 requirement | Current evidence | Disposition |
|---|---|---|---|
| 1 | Consume Nadia's actual actor-accessible circumstances and plural P3 organization | J1/D03 context consumes actual C04 speech, P3 streams, contradictions, eligible/withheld record hashes, prior scope; two different histories produce distinct context hashes | **PRESENT (context only)** |
| 2 | Generate and evaluate alternative prospective activities without inventing a dominant-motive selector | `ExactActorProvider` constructs fixed proposals before it sees context; `RecursionCycle._parse_proposals` requires 3–5 events and `BatchEngine.run_batch` realizes every one in order. No selector/evaluator exists | **ABSENT** |
| 3 | Commit a qualified activity through the existing competent world owner | P2 can write, but only for its prebound `case/source`; P3 requires a prebound plan keyed by exact `event_id + proposal_hash`. No owner-authorized plan creation or selected-activity binding exists | **PARTIAL / NOT G2** |
| 4 | Materially different result under altered historical conditions | Context differs; the realized activity does not, because the provider proposals are fixed. Existing test explicitly proves only context difference, not motive law | **NOT SATISFIED** |
| 5 | Cold restoration and a distinct later ordinary consumer | P2 cold reopen and C9 conditioning consumer work. There is no qualified selected activity to restore, and no distinct later *actor performance* consumer | **PARTIAL / NOT G2** |

**G2 remains HOLD.** No new dominant-motive selector, hidden action table, provider-as-psychology, `eligible_modes`-as-action promotion, random/first-candidate selection, or protected P2/P3 write was introduced.

## 6. Exact source findings and missing contracts

1. **Batch-execution ABI is not an alternatives court.**
   `developmental_recursion/model_cycle.py:508-512` requires 3–5 prospective documents; `developmental_recursion/engine.py:398` iterates over the whole list and calls `owner.realize` for each. This is an ordered batch, not a competing-activity menu.
2. **P3 plan admission is prebound and has no production creator.**
   `p3/p3_owner.py:217` builds `_plans_by_event` only from constructor-supplied plans; `p3/p3_owner.py:393-397` refuses any proposal without an exact prebound plan. `p3/test_rules.py:115-131` requires `event_id + proposal_hash` plus source/registry identity. The only builder is the test fixture `tests/p3_fixture_support.py:93 plan_for`. A newly selected proposal cannot lawfully create its own plan.
3. **P2 writes only its prebound case/source.**
   `developmental_recursion/p2_owner.py:379` requires `proposal.source_refs == (self.source_ref,)`; `:557-559` calls `session.admit_event(case=self.case, source=self.source, ...)`. The existing writer cannot prove that a selected candidate is Nadia's historically conditioned act.
4. **D03 deliberately does not issue an action.**
   `p3/immediate_uptake.py:509-525` returns `native_action = NOT_ISSUED_BY_D03_RULE`, `native_rule = MISSING_RULE`, `eligible_modes` as candidates; `j1_join.py:214-220` returns `NO_COMPETENT_SOURCEFREE_CHILD_EVENT_PERFORMER`. D04/D05 remain queued and unlaunched.
5. **Historical V3 selection is reuse evidence, not current authority.**
   `git cat-file -e HEAD:v3/engine/scoring.py` and `HEAD:v3/engine/run_llm_band.py` both fail; no current `v3/` runtime tree exists at the frozen commit. A local historical tree contains `v3/engine/scoring.py` at the manifest hash `36833287c72ffa40d0ece1ebc66fb0d685a92fc71aab1d211be9b21bfd0a82cb`, but `select_candidates` scores year-event/magnet candidates and selects up to five for simulation, using heuristic weights and `rng or random.Random()`; `run_llm_band_year` has a first-candidate fallback. ADP-020 and the V3 completion ruling forbid those as causal authority. It is not an actor alternative evaluator and is not importable/qualified here.
6. **ADP-019/ADP-020/CAN-008 are authority documents without installed production implementations.**
   The authority documents exist under `data/ddm_build_copy/...`. No checked-in module implements `V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE@1.0.0`; the only reference is a `NONCURRENT_SYNTHETIC` candidate fixture (`rawlsing_next/v3_contact_witness_independence_source_authority_candidate_r1.py`) with forbidden effect surfaces. The CAN-008 response registry in the vendored `candidate/response_rules.py` has an empty production registry and TEST_ONLY rules only. The existing lab selection (`vendor/.../lab_sgi1/selection.py`) is a provisional conception-scenario selector, not actor activity.
7. **No existing qualified alternative evaluator was found.**
   Searches for actor-prospective/activity-candidate/selector implementations found only the fixed `ExactActorProvider`, the 3–5 batch ABI, the TEST_ONLY S36/S37 response bridge (always zero target proposals), and historical V3 batch/scoring code. None can lawfully generate and evaluate Nadia's plural prospective activities.

## 7. Exact next dependency

The next dependency is **not another lock review**. It is one explicit owner/rule issuance:

**`V3_ACTOR_PROSPECTIVE_ALTERNATIVE_EVALUATION_AND_EVENT_ADMISSION`** — requirement label, not an issued rule ID — comprising:

1. a source-owner-issued candidate schema for at least two actual, materially possible activity alternatives (including ordinary unrelated activity/no recruitment and possible inaction), with proposer/source/rule provenance and candidate hashes;
2. a versioned actor-source evaluation rule that selects exactly one lawful candidate or returns a typed unresolved/deferral/**evaluated inaction** result; no dominant-motive scalar, hidden screenplay, default-first/random rescue, or `eligible_modes` promotion;
3. an owner-authorized **P3 plan creation/binding** path for the selected proposal, or an explicit narrow handoff to the existing `P3Owner` plan ABI;
4. an owner-authorized **P2 selected-activity binding** so `P2Owner.admit_event` cannot be treated as proof of a motivated act merely because a proposal was written;
5. ADP-019 admission receipts for any external-interaction event, ADP-020 decision/draw receipts only if a semantic rule authorizes stochastic selection, and a concrete CAN-008 production rule if a response transaction is claimed;
6. a distinct later ordinary P4/P6/world actor consumer plus altered-history, cold-reopen and anti-duplication negatives.

Minimum authorization therefore is: **the actor/source owner must issue the alternative-generation/evaluation rule and the P3 plan/P2 selected-activity binding contract**. Without that, implementing G2 in this repository would fabricate the missing psychological rule or the missing owner authority. D04/D05 code alone is insufficient because a target/recruiter writer still would not generate or evaluate competing prospective activities.

## 8. Stop

The executable result and exact next dependency are established. No protected merge, no new review fleet, no self-acceptance, and no G5 were performed. **STOP.**
