# SOROK #1010 — AGENT B exact counterbuild return

**Disposition:** `REPAIRED_PREWRITE_CUSTODY_AT_SOURCE / G2_HELD_EXACT_PERFORMER / J1_INTEGRATION_NOT_RUN / STOP_FOR_A`.
**Role:** adversarial B on ONE shared A→B lineage. This return is a repair candidate, not G5 receiving or a protected adoption.

## 1. Immutable ancestry and source custody

- Original user-selected issue: https://github.com/maidiu/rawlsing/issues/1010; original 27-task D02/D03/E01 packet at `227ce149fc7864c83c179a7d3ecaef2b92c5bdab`.
- Protected PRE-MAIN (read-only): `6a5c12f04323d74001f9632063ec907f4fc4468e`.
- PR #996 joined J1 source: `fb061dec16c8386b9caa1b5ea75ec7645aff88a7`, underlying code `c724d1a89626f3e177acd004c0be20029dc7ade4`.
- Original Agent A frozen immutable parent: `6248547b2ad98002245b69cec9e399277d090f12`, PR #1016. B branch `agent/sorok-d03-e01-1010-b-counterbuilder-r1` descends from that exact SHA, not a competing reimplementation.
- B files: **modified** A's `d03_e01_performer.py` (only adapter/custody and honest reporting), **added** adjacent `post_provider_guard.py` (pure nonwriting CallProvider proxy); **added** `test_b_hostile.py`, `test_b_guard_unit.py`; this handoff and mandatory self-attack. No edits to original P2Owner, P3Owner, B04/B05, C03/C04, J1, CG-A, #1008, protected PRE-MAIN.
- Exact source blobs before this return: updated adapter `4be495b390b5edd40b437838d6f8390a4d1bf205`; guard `633435c5fa52528265401535986d1dbc3fcafb1d`; full-fixture B negatives `d237147eccffd56a2f75b5b6947ce2f46f6c08ef`; isolated differential `b312758563092b134eedc085f3e3a2d11c3d1395`.
- Final immutable HEAD = the commit containing this return; read branch SHA directly. Do not confuse source blob hashes with Git commits.

## 2. Independent reconstruction and predecessor strengths

Directly inspected `j1_join.compose_j1`, `immediate_uptake.build_immediate_uptake`, P3Owner plan/realize, P2Owner validate/realize, RecursionCycle._call/_parse_proposals/_run_batch, BatchEngine and A's three source files. A genuinely preserved the read-only J1 C04/P6/D03 boundary, existing `BatchEngine(P2Owner)` admission, identity checks and eventual ordinary `session.read_event` readback. A correctly refused to elevate D03 eligible modes into acts, invent Rule A/T or claim that its fixed precomputed `ExactActorProvider` responds to Nadia's historical organization. A's executable assertions remain NOT_RUN and are **not** independently verified execution.

`RecursionCycle` consumes 3–5 **ordered-to-be-executed** `EventProposal` documents, not 3–5 mutually exclusive psychological alternatives. A was right; I did not replace it with a choice engine.

## 3. Established findings

**B-01: P2 prebound-case execution is not Nadia-conditioned performance (source-semantics defect, G2 HOLD).** `P2Owner.validate_proposal` accepts only `ADMIT_EVENT`, the bound `source_ref`, allowed participants, future time, optional history_refs/language_context. `P2Owner._realize` invokes `session.admit_event(case=self.case, source=self.source, history_event_refs=..., event_time=...)`. It does not consume the D03 stream meanings to determine which activity occurs. The A fixture creates `EventProposal` objects *before* `CallProvider.call` receives Nadia's P3 context. `BatchEngine(owner.base_owner)` therefore could establish genuine P2 event readback while never invoking `P3Owner.realize` for those new proposals. This is not proof of a source-qualified actor choice or new P3 development. **No authority to mint a new P3 plan/Rule A/T or rewrite the read-only owner; preserve the precise HOLD.**

**B-02: late P3/source stale detection could occur after P2 world writes (source-backed implementation defect, patched).** In A, `owner.store.head() == joined...after` was checked only after `RecursionCycle.bootstrap` completed. The cycle checks `engine.owner.snapshot()`, and the engine owner is `owner.base_owner` (P2), not P3. Thus P3 head/source drift after the external provider response could escape the P2 provider-state check; a later P3 check could throw only *after* effects were written. Original ordering is demonstrated by exact A source; full real-world race not executed on a qualifying integrated runner.

**B-03: success-label ambiguity (patched).** P2 readback can be true while G2 is still held. Report now explicitly emits `g2_historical_child_performance=HELD_NOT_ESTABLISHED`, `performed_event_owner_scope=P2_PREBOUND_CASE_NOT_P3_PLAN`, and `distinct_later_actor_performance_reader=NOT_ESTABLISHED`. Original P2 event status and grade remain unchanged.

## 4. Actual B repairs

- Introduced `GuardedProvider`: calls the unchanged delegate, then calls a nonwriting validation barrier **before returning proposals to RecursionCycle**. Its exception follows RecursionCycle's existing durable `AMBIGUOUS_PROVIDER_CALL` / HOLD path, before `BatchEngine` can write an event.
- Adapter's `precommit_custody` rechecks P3 head, combined P2/P3 identity/clock/root/session and exact J1 source closure after the provider returns, immediately before proposal parsing and world-owner admission. Exact codes `E01_POSTPROVIDER_P3_HEAD_CHANGED`, `E01_POSTPROVIDER_OWNER_IDENTITY_CHANGED`, `E01_POSTPROVIDER_J1_SOURCE_CHANGED`.
- Added two inherited-fixture hostile tests injecting a changed P3 head and changed J1 source closure during provider.call; expected negative = provider called, durable cycle reservation/HOLD, **zero additional world events**. These tests are authored and syntax-checked but NOT_RUN in a full repo environment.
- Added isolated provider guard unit tests, including an old-postwrite vs new-prewrite differential. No new psychological selection, event writer, scheduler, P3 plan, native science or parent changes.

## 5. Executed evidence and limitations

- Independently reconstructed local copy of **exact GitHub blob** `633435c5fa52528265401535986d1dbc3fcafb1d` and B isolated test blob `b312758563092b134eedc085f3e3a2d11c3d1395`; `git hash-object` matches both bytes.
- Command `python -B -m pytest -q -p no:cacheprovider test_b_guard_unit.py` against those exact copies: **4 passed in 0.05s**. Includes differential A ordering `provider → world-write → detect-drift` vs B ordering `provider → detect-drift` and no world-write.
- B full-fixture hostile test blob `d237147eccffd56a2f75b5b6947ce2f46f6c08ef` reproduced locally byte-identically and `python -m py_compile` PASSED. **No inherited repository dependencies present in local container, so J1/P2/P3 S2 was NOT_RUN.**
- A's existing diagnostic run #43508991500 failed before runner allocation on both attempts, zero steps. This does **not** establish test RED or PASS. No observed provider costs/RSS, no independent cold J1 proof, no G5.

Actual full-suite run required in an authorized full checkout:
```sh
python -B -m pytest -q -x -p no:cacheprovider --tb=short \
  WORKER_RETURNS/SOROK-E01-J1-995-R1/test_j1_three_head_join.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-A-R1/test_d03_e01_performer.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-B-R1/test_b_guard_unit.py \
  WORKER_RETURNS/SOROK-D03-E01-1010-AGENT-B-R1/test_b_hostile.py
```

## 6. Attacks rejected / self-critical limits

- Rejected: all 3–5 prospectives must be rival action options. They are actual ordered batch events; using their labels as a mode selector would introduce a new wrong engine.
- Rejected: no P2 source-owned event exists. P2Owner really writes sourcefree E1 events; the missing proof is actor-conditioned *cause and performance semantics*, not an absence of any world writer.
- Rejected: D04/D05 original target formation is a universal prerequisite to E01. It is separately held, not a licence to invent motives.
- New risk from B: an additional J1 source-closure rehash and P3 snapshot check between model call and event realization; may increase latency and fail closed under concurrent code changes. **It is not an atomic P3↔P2 lock** and cannot prevent a race after this check, nor undo side effects a malicious provider performed by itself. The owner-controlled transaction/lease remains a separate requirement.
- The full tests could expose a source or ABI incompatibility with the new guard; if so, repair actual behavior, not weaken the original source/privacy checks.

## 7. G1–G5 and return

- **G1:** source reconstructed to actual P2/P3/J1 first reader, candidate code linked. FULL INTEGRATED S2 NOT_RUN.
- **G2:** `HELD_NO_SOURCE_QUALIFIED_HISTORICAL_NADIA_PERFORMER`. B improves custody; does not create/claim actor-conditioned selected act or separately qualified later performed consumer.
- **G3:** one independently established late-check timing defect; isolated differential RED→GREEN, 4 PASS. Two full-fixture source/P3 negatives authored; full suite NOT_RUN.
- **G4:** same world writer left untouched; additional precommit checks present. Cold/retry/first-reader execution remains NOT_RUN.
- **G5:** NOT_PERFORMED. No A/B self-acceptance or premature third reviewer.
- **Engineering:** bounded code repair/isolated proof; integrated NOT_RUN; G2 HOLD.
- **Scientific:** sourcefree-only; CAN/ADP native Rule A/T/memory/NO_CHANGE unissued.
- **Authority:** inherited A source-owner domain only; no read-only inherited owner changes, protected merge, Browser session monitoring or #939 restart.

### Strongest challenge to Agent A on the B descendant

On this **exact descendant**, show a source-authorized *real* P3/P2 prospective child activity whose input comes from several qualified Nadia organizations and whose actually admitted event varies meaningfully under a controlled altered historical input; show the distinct later ordinary performed consumer and changed/severed/restored/cold proof. **Do not pass P2's fixed source case off as Nadia's action; do not invent a choice table or bypass `P3Owner._plans_by_event`.** If original P3 source-pinned plan/actor performer cannot be supplied without edits outside granted custody, prove that exact missing owner/ABI and retain G2 HOLD. Independently run the B race negatives and identify any real regression introduced by the guard. This is the A final counter, not permission to start new agents.

**STOP — frozen B handback to user for A's independent next turn.**
