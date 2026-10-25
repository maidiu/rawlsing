# SOROK S48 repair2 — current source-owner closure

**RESULT:** `S48_REPAIR2__CURRENT_BP4_OTHER_SOURCE__ROOT_B_OWNER__WORLD_PERFORMER__SOURCE_BEFORE_C8__ADVANCE_REPLAY_PENDING_PRESERVED__ACTUAL_NEW_CUT_PROVIDER_1__OLD_CUT_PROOFS_PRESERVED__SCI05_HOLD__NO_NATIVE_GRANT`.

S48 repair2 replaces the foreign R31J share/refusal fixtures with a current independently performed BP4 other-actor source. The product may propose only a source-qualified current operation; the selected operation is performed after the no-input barrier, with an owner receipt and a current world-journal event, before the existing S42 C8/C9 path. Static/foreign candidates are rejected with `SOURCE_OWNER_HOLD`.

## Scope and base

- Branch `codex/sorok-s48-one-call-continuing-turn`; prior cut `ee4b2dd9c025cfd537cf8ac048a6b8619284ebf5`; base accepted S47 `765a441f87292aa4c17794745b65cb54e6aaa83f`.
- Writes only `WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/**`; no accepted S47/S42/S37 edits, agents, native grants, provider/model change, private config reads, or broad accepted-suite run.
- The final commit SHA is the exact repair cut; the new actual provider run was made in this repair worktree and is labeled with that commit in the completion response. Captured old-cut provider proofs remain separately preserved.

## Source-owner repair

- Removed the static `TEST_ONLY_EVENT_share`/`TEST_ONLY_EVENT_refuse` candidates and all `case_for(share)` construction from the turn path.
- `s48/sources.py` exposes only a currently supported independent BP4 operation: an owner-receipted `REFUSAL` by the root's current `TEST_ONLY_BP1_R26V_ACTOR_B`. The source owner is that root actor; the BP4 world owner is recorded separately as the operation performer.
- The operation is not preperformed. After the product's explicit no-input barrier, S48 issues one BP4 world event at the current clock, adds it to the canonical world journal, and only then constructs the source. Source-before-C8 ordering is exact. The event has owner/actor receipt, current root, current clock and operation `REFUSE_TOOL`; no material mutation or new willingness law is introduced.
- The source is validated against the current first event E1 and the dynamically constructed B/E1 case. The product proposal is only a world possibility, not the other person's intention. A stale/foreign/static share fixture is excluded and returns `SOURCE_OWNER_HOLD`; no dependent event is realized.
- The product can still return narrative and optional self-account. Nonempty self-account remains exact `SCI05_HOLD` with no second V3; explicit absence records `SELF_ACCOUNT_ABSENT_NO_NEW_INTERPRETIVE_INPUT`.

## Closed semantics retained

- Default `run_turn()` advances from the current event; a realized next event starts a new turn and provider invocation.
- `run_turn(source_event_ref=...)` and `run_turn(replay_turn_id=...)` replay the same logical canonical turn and never reissue the provider.
- `S48_PRODUCT_DISPATCH` remains a pre-call C12 intent. Crash after provider before terminal turn gives `PENDING_UNKNOWN`/`S48_DISPATCH_WITHOUT_RESULT_NOT_REISSUED`; no blind duplicate call or fake receipt.
- Cold replay returns the same canonical event/turn; no target or narrative psyche write.

## Evidence

- New repair-cut actual entrypoint: `logs/entrypoint.log` / `evidence/entrypoint.json`; actual envelope `evidence/actual_envelope.json`; raw CLI `logs/product_c0914678feb16918.stdout.jsonl`.
- New actual call: `provider_call_count: 1`, one step/session, `self_account: null`, candidate `OTHER_REFUSES_TOOL`, source actor `TEST_ONLY_BP1_R26V_ACTOR_B`, source owner B, performer owner `TEST_ONLY_BP4_WORLD_OWNER`.
- Actual event order: occurred event ordinal 1 → product call/no-input barrier → independently performed BP4 B refusal at current clock → S42 event ordinal 2 → C9. Cold same-turn replay uses `source_event_ref` and records `cached_on_cold: true`, `cold_provider_call_count: 0`.
- Actual next C9 remains targetless `NO_CHANGE`/`NO_PROPOSAL`; S47 interval source `d73a00…` remains in the readset; root unchanged `3bcb21fc…`.
- Current-source chronology (`evidence/chronology.json`, `logs/repro_candidate_source_chronology.log`): source owner is in root actor IDs, actor B is the root B, performer is current world owner, event exists in world journal at current clock, source precedes C8.
- Foreign/static candidate regression returns `SOURCE_OWNER_HOLD` and realizes no event. Current positive regression uses the BP4 refusal source; warm/cold normal consumer paths are covered.
- Old-cut provider proofs preserved exactly under `evidence/old_cut_ae021e/` and `evidence/old_cut_ee4b2dd9/`; they are not rewritten as proof of this repair.
- Controlled SCI05 hold and call-failure evidence remains non-provider and marked `actual_provider_call: false` (`evidence/controlled.json`).
- Focused S48 tests: **16 passed**, 0 failed/error/skipped; `junit/s48_full.xml`, `logs/s48_full.log`, `evidence/test_run.json`.
- Reviewer chronology oracle had an obsolete `candidate_source` import; `evidence/repro_candidate_source_chronology.py` is the honest schema update only for that import and current source API, with unchanged chronology claims.

## Limits

- The only current independently supported other-actor operation is BP4 refusal. The product cannot manufacture a share/help will or a mutually exclusive future; a claim without a current authorized operation is source-owner held.
- Source bytes are TEST_ONLY sourcefree BP4/root records, not native/empirical B psychology. B actor/root identity is current; owner registration is the root B actor, performer is the BP4 world owner. No new owner, grant, target, psyche, or T is issued.
- Actual provider output remains bounded sourcefree generation; no broad provider/science campaign was run. The old-cut and new-cut actual receipts are distinct and separately labeled.

## Commands

```text
PYTHONPATH=$PWD/WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1 \
M35_JOIN_E_RETURN=/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
TMPDIR=$PWD/WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/logs \
python3 WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/run_s48.py \
> WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/logs/entrypoint.log 2>&1
```

**Terminal:** `S48_REPAIR2__CURRENT_BP4_OTHER_SOURCE__ROOT_B__WORLD_PERFORMER__SOURCE_BEFORE_C8__ADVANCE_REPLAY_PENDING__ACTUAL_1__OLD_PROOFS__SCI05_HOLD__NO_NATIVE_GRANT`. Final commit and remote SHA are verified after push.
