# SOROK D03/E01 #1010 — Agent A exact adversarial handoff (first turn)

**Disposition: IMPLEMENTED_CANDIDATE / EXECUTION_NOT_RUN / HOLD_FOR_REAL_S2_EVIDENCE.**
This is an honest bounded first build, **not** G5 acceptance or a claim that Nadia autonomously chose an action. The actual test-runner refused before allocating a runner, twice. Do not promote the source analysis or authored assertions to execution proof.

## 1. Exact artifact and custody

- Author branch: `agent/sorok-d03-e01-1010-a-performed-sourcefree-r1`.
- Immutable original PR #996 author return: `fb061dec16c8386b9caa1b5ea75ec7645aff88a7`; original joined code/test ancestor `c724d1a89626f3e177acd004c0be20029dc7ade4`.
- Baseline protected PRE-MAIN source cited by parent: `6a5c12f04323d74001f9632063ec907f4fc4468e`; **not modified**.
- Frozen candidate code+tests HEAD before this handoff: `5245c6010715aba494ebf7196ec5da1a67944457`. Read branch HEAD after this handoff for the final manifest, and compare it against `fb061dec16c8386b9caa1b5ea75ec7645aff88a7`.
- Files added (no inherited/parent/J1/P2/P3 files overwritten):
  1. `WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/d03_e01_performer.py`
  2. `WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_d03_e01_performer.py`
  3. This exact handoff.
- One temporary diagnostic GHA workflow was installed only to run scoped tests. It was removed from the final candidate. Historical run attempts remain as evidence.
- No protected merge, controller restart, worker launch, or review grant. No access to separate Browser B session implied.

## 2. Original requirements and source reconstruction

Governance: #1010; 27 frozen packet tasks `D02/D03/E01` (and B04/C04) at `227ce149fc7864c83c179a7d3ecaef2b92c5bdab`, actual J1 source in #996, original P2/P3, PROGRAMMA, adopted MCR-lite, provisional UM-SOROK R1/R2.

Direct source paths and audited functions:
- `WORKER_RETURNS/SOROK-E01-J1-995-R1/j1_join.py:compose_j1`: parent C04 -> P6 child speech experience -> D03; terminal subsequent child event *held*, not an action.
- `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/immediate_uptake.py:build_immediate_uptake`: read-only plural stream activation, may report CONTRADICTION or NO_PRIOR_ORGANIZATION; `eligible_modes` are candidate modes, never actions.
- `WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/p3/p3_owner.py:P3Owner.realize`: only writes for already source/plan-pinned proposals; cannot be given an invented D03 target without original source-authorized plan.
- `WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/model_cycle.py:RecursionCycle.bootstrap`: passes provider context and validates 3-5 **ordered-to-be-realized** prospective event documents. They are not a menu of mutually exclusive response modes.
- `.../developmental_recursion/engine.py:BatchEngine.run_batch` and `.../p2_owner.py:P2Owner.realize`: real sourcefree owner event admission, chain journal, replay refusal, source/identity/clock custody, `session.read_event` and `session.read_c9_conditioning` downstream.
- `WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py:child_speech_experience`: ordinary source-visible child speech consumer.

Critical distinction: the generic P2 event owner can realize a sourcefree E1 event. That does **not** establish that the originating prospective sourcefree provider has an issued actor-conditioned activity rule or that the fixed P2 source case represents Nadia's independently constituted volition.

## 3. Strongest source-backed implementation candidate

`run_d03_e01_first_batch` replays J1 read-only on the same live source-root and P3/P2 identity; aborts unperceived/stale/foreign/source-changed speech before provider or owner writes; passes **only an allowlisted public and plural P3 activation context** to the existing `CallProvider`. It does not choose a mode, insert a hidden reason, create a new state owner, or alter P3 storage.

`RecursionCycle` validates 3-5 actual `EventProposal` inputs, then `BatchEngine(P2Owner)` serially submits them to the existing owner and its transaction/operation journal. The adapter requires normal `session.read_event` readback of each `e1_event_id/e1_event_hash`, identity, clock and `performed=True` from the canonical owner. Separate actor observation is qualified honestly. The resulting report explicitly says that P3 durable formation and D03-driven motive causation are **NOT ESTABLISHED**.

The authored tests aim to assert: a real P2 event with first-reader/C9 and cold-reopened receipts, no duplicate on retry, no P3 head mutation, no provider call on child absence or forged source/actor, 3-event minimum, two different P3 history contexts without demanding different actions, and no parent private reason in the provider payload.

These are **authored test intentions, not observed passing results**.

## 4. Actual attempted execution / raw negative evidence

Diagnostic workflow name: `SOROK D03 E01 Agent A ephemeral sourcefree execution`.

- [Run 43508991500](https://github.com/maidiu/rawlsing/actions/runs/43508991500) attempt 1, HEAD `687ff6a1d840bbc9df7978a39d6db0a93fc71f14`: FAILURE before any job step; runner ID 0, runner name empty, no steps, no executable logs.
- Same run attempt 2 after one explicit bounded rerun: FAILURE before any job step; job `132174635005`, runner empty, zero steps.
- **No Python compile, no pytest, no actual event or cold process was executed.** This is a GitHub runner/allocation diagnostic, not a code-level RED and not an inferred GREEN.

Required next actual runtime commands from repository root, under the original frozen branch/source composition and installed Python 3.11+pytest:

```sh
python -m py_compile WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/d03_e01_performer.py WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_d03_e01_performer.py
python -B -m pytest -q -x -p no:cacheprovider --tb=short WORKER_RETURNS/SOROK-E01-J1-995-R1/test_j1_three_head_join.py WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_d03_e01_performer.py
```

For an independent execution compare actual repo-installed `j1_join.py` and all source-pin closures, print full tracebacks, repair exact failures on this same descendant, re-run first consumers, then publish the actual results. Do not invent them.

## 5. Self-hostile findings, strongest likely B attacks, causal limits

1. **Highest-risk false positive:** a fixture-configured `ExactActorProvider` supplies the same P2 source-case events regardless of P3 history. If those write through P2, they prove that the generic writer functions, **not** that Nadia selects an activity from historically conditioned organizations. B should challenge this immediately with a genuine provider/source-conditioned action and an independent later consumer. Do not claim G2 complete while that difference remains.
2. **P2 semantics are limited:** `P2Owner.validate_proposal` accepts only `ADMIT_EVENT`, `history_refs` and optional source-bound `language_context`; it does not accept a psychotherapeutic target, conscious reason, or arbitrary mother/Nadia act verb. Do not extend it from the D03 adapter without its competent owner. The existing `case` controls the kind of realized act.
3. **P3 source-locked plan:** fresh `P3Owner.realize` demands a preexisting plan bound to proposal hash, source, rules and identity. Our direct P2 path intentionally leaves P3 psychological store unchanged. This is **not** D04 acquisition or D05 target-mediated later action.
4. **3-5 prospective misconception:** existing `RecursionCycle` treats all 3-5 as ordered future events, not mutually exclusive psychological choices. Never implement a top-1 selector based on `eligible_modes`.
5. **Actor observation vs performed world event:** P2 may produce a performed E1 event while the actor access receipt is HELD. The adapter must downgrade accordingly; never call it Nadia's lived experience without OBSERVED receipt.
6. **Run infrastructure:** no tests executed. B must not use the unrun sourcefree assertions as evidence. Read the actual failure logs when a runner becomes available.
7. **Potential runtime integration defect:** parent B04/C04 world modifications may affect whether the old P2 fixed case admits its future event. Only the exact integrated test can resolve that. Do not move the goalposts to a synthetic stub.
8. **Retry/crash ambiguity:** existing P2/RecursionCycle must continue to fail closed on ambiguous partial commits; the adapter does not reconcile a half-batch itself. A second identical bootstrap must not commit another effect.
9. **Material change between proposal and realization / unrelated ordinary activity / substantive alternate histories:** test cases are incomplete; no first-consumer witnessed result. Remain explicit E01 open obligations.
10. **Cost and speed:** actual CPU, RSS, cold replay performance and provider costs NOT OBSERVED. No throughput/fidelity claims.

## 6. Rejected alternatives and proof boundaries

Rejected: selecting `joint_check` or `private_check` as an action; telling an LLM to write "Nadia argues" and treating it as world history; directly mutating world/psyche without P2/P3 owner; fabricating D04/Rule T, native CAN/ADP permission or `NO_CHANGE`; editing read-only parent B04/C04 or J1; commissioning another generic chooser or daily-life scheduler.

**G1:** direct source-chain analysis completed; executable exact-chain proof on new code NOT_RUN.

**G2:** genuine P2 owner-performance adapter AUTHORED but unexecuted; no demonstrated historically conditioned Nadia action, independent provider/decision qualification still open. `HOLD_EXACT_CONTEXT_TO_ACTUAL_ACTIVITY`.

**G3:** six hostile tests AUTHORED but NOT_RUN; no B opponent tests yet.

**G4:** retry/cold/world-reader source tests AUTHORED but NOT_RUN.

**G5:** NOT_REQUESTED; no independent nonauthor receiving.

**Engineering verdict:** `HOLD_EXECUTION_AND_ACTOR_CONDITIONED_EVENT_PROOF`.

**Scientific verdict:** `SOURCEFREE_ONLY__NATIVE_RULE_A_T_MEMORY_NOCHANGE_NOT_ISSUED`.

**Authority verdict:** `AUTHORED_ISOLATED_BRANCH__NO_PROTECTED_MERGE__NO_PYAT_SOURCE_OR_ACTOR_RIGHTS`.

This handoff invites an adversary to make the existing P2/P3 event genuinely actor-conditioned with sourcefree evidence and a later actual consumer. An exact missing competent owner is superior to a plausible false positive. **STOP for B.**
