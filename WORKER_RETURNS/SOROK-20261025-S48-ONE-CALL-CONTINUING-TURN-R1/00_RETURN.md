# SOROK S48 repair1 — one-call continuing turn

**RESULT:** `S48_REPAIR1__EXPLICIT_TURN_ADVANCE_AND_REPLAY__DURABLE_DISPATCH_BEFORE_PROVIDER_EFFECT__SOURCE_QUALIFIED_OTHER_ACTOR_CANDIDATES__ACTUAL_NEW_CUT_PROVIDER_1__OLD_CUT_ACTUAL_PRESERVED__COLD_ZERO_RECALL__SCI05_HOLD_TYPED__NO_NATIVE_GRANT`.

S48 repair1 fixes the three review defects on the same S47 person: distinct advance versus same-turn replay, a canonical dispatch intent before the provider effect, and removal of the material-to-other-actor-will candidate law. The accepted S47 source/root/C9 path is preserved.

## Scope and base

- Branch `codex/sorok-s48-one-call-continuing-turn`; prior cut `ae021e470cb6a6e144008e569a286a787120cb9d`; base accepted S47 `765a441f87292aa4c17794745b65cb54e6aaa83f`.
- Writes only `WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/**`; no accepted S47/S42/S37 edits, no new agents, native grants, psychology, provider/model switch, or broad accepted-suite run.
- The final commit SHA is the exact repair cut; the new actual provider run was made on this repair worktree and is labeled with the final commit in the response. The prior actual provider run at `ae021e…` is preserved unchanged under `evidence/old_cut_ae021e/`.

## Repair 1 — explicit turn identity

- `run_turn()` with no source advances from the current occurred event. A realized next event is therefore the source of a **new** turn and a new provider invocation.
- `run_turn(source_event_ref=...)` replays the logical turn for that exact canonical E1 source and returns its cached result with zero provider calls.
- `run_turn(replay_turn_id=...)` replays the exact canonical product turn ID.
- A pending dispatch or a final turn without a result returns typed `PENDING_UNKNOWN`; it is never silently reissued. Multi-turn and cold replay regressions are in `tests/test_s48_one_call.py`.

## Repair 2 — durable dispatch intent

- Before any provider effect, S48 appends canonical `S48_PRODUCT_DISPATCH` with a deterministic `turn_id`, source event ref/hash, payload/prompt hashes, clock and `DISPATCHED` status in the existing C12 store.
- The provider effect is followed by the canonical `S48_PRODUCT_TURN` and `S48_TURN_RESULT`. If the terminal append is interrupted, the dispatch remains and the next attempt returns `PENDING_UNKNOWN`/`S48_DISPATCH_WITHOUT_RESULT_NOT_REISSUED`; no provider call is repeated.
- The dispatch/result records are canonical C12 entries, not a parallel ledger. The actual call receipt is stored only after a successful terminal append; no fake receipt is written.

## Repair 3 — source-qualified other actor

- Removed `material_available → OTHER_SHARES/REFUSES` mapping and all `case_for(share)` construction from the turn path.
- Allowed candidates now point to two independently source-qualified existing R31J source records. Each carries `b_owner`, `b_actor`, performed event ref/hash, operation and source qualification; `firstclass.validate_source` must pass before a candidate is admitted.
- The product may select a source proposal but that is not another person's intention and does not create a new willingness policy. The source performer/owner remains the R31J source; S48 only passes the selected source to the existing independent S42 performer.
- Material availability is reported as accessible world fact but no longer selects the candidate or changes the allowed set. The candidate-mapping reproducer now reports unchanged candidates before/after an ACTUAL interval. If source qualification fails, the turn returns `SOURCE_OWNER_HOLD` with no event.

## Actual evidence

- New repair-cut actual entrypoint: `logs/entrypoint.log` / `evidence/entrypoint.json`; actual envelope `evidence/actual_envelope.json`; raw CLI `logs/product_07a3502e0c4a61b2.stdout.jsonl`.
- New actual call: `provider_call_count: 1`, `step_count: 1`, one model session, `self_account: null`, one source-qualified proposal `OTHER_SHARES_TOOL` with owner `TEST_ONLY_OWNER_share`, actor `TEST_ONLY_R31J_B`, source event ref `TEST_ONLY_EVENT_share`.
- Event order: occurred event ordinal 1 → one product call → independently admitted event ordinal 2 (`TEST_ONLY_BP2_E1_OCC-0002`). Cold replay uses `source_event_ref` of the same logical turn and records `cached_on_cold: true`, `cold_provider_call_count: 0`, same event, same turn ID.
- Same S47 root `3bcb21fc22df3255269382ad249f706dd6dd5378cb886af26542991ff516a4f7`; S47 interval source `d73a00…` remains in the C9 readset; C9 remains targetless `NO_CHANGE`/`NO_PROPOSAL`; no actor response was written by the product.
- Old-cut actual proof retained exactly: `evidence/old_cut_ae021e/entrypoint.json`, `product.stdout.jsonl`, `product.stderr.log`, `actual_envelope.json`, `source_manifest.json`.
- Controlled non-provider branches: exact SCI05 hold and `CALL_FAILED` both realize no next event (`evidence/controlled.json`).
- Reviewer reproducers run unchanged from `SOROK_REVIEW/S48/evidence`: `logs/repro_multiturn_cache.log`, `logs/repro_crash_retry.log`, `logs/repro_candidate_mapping.log`. They show second turn advances to event 3, crash/retry makes no second provider invocation and returns pending, and candidates do not change with material.
- Focused S48 tests: **14 passed**, 0 failed/error/skipped; `junit/s48_full.xml`, `logs/s48_full.log`, `evidence/test_run.json`.
- Source manifest: `evidence/source_manifest.json`; S47 source files exact at accepted cut; old-cut evidence hashes preserved.

## Limits

- The source candidates are the existing sourcefree R31J test source records, not a new live other-person performer or empirical intention. The independent source owner/performer qualification is the proof boundary; no material state is used as a proxy for another actor's will.
- A nonempty self-account still has no competent internal-act owner and yields exact `SCI05_HOLD`; no second V3, invented internal-act law, or forced absence was added.
- The actual repair-cut provider call is TEST_ONLY sourcefree product generation, not native science, an empirical probability, OBL062, T, human A5, or a production claim. No broad accepted-suite rerun was performed.
- The old-cut actual call is not rewritten as proof of repaired independence; it remains a separately labeled historical receipt.

## Commands

```text
PYTHONPATH=$PWD/WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1 \
M35_JOIN_E_RETURN=/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1 \
TMPDIR=$PWD/WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/logs \
python3 WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/run_s48.py \
> WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/logs/entrypoint.log 2>&1
```

**Terminal:** `S48_REPAIR1__ADVANCE_VS_REPLAY__DISPATCH_BEFORE_EFFECT__SOURCE_QUALIFIED_OTHER_ACTOR__ACTUAL_REPAIR_CUT_1__OLD_CUT_PRESERVED__COLD_ZERO__SCI05_HOLD_TYPED__NO_NATIVE_GRANT`. Final commit and remote SHA are verified after push.
