# SOROK S49 — independent actor-parameterized producer

**RESULT:** `S49_FINAL_REPAIR__NO_CACHE_ACCESS__EXACT_CANONICAL_INTENT__MANDATORY_CANONICAL_PERFORMER_RESULT__BASE_S42_CHAIN_GUARD__CONTROLLED_REFUSAL_NORMAL_C8__ACTUAL_ROOT_B_CONTEXT_HOLD__NO_PROVIDER__NO_NATIVE_GRANT`.

S49 adds the missing actor-parameterized generation/performer path over the same S48/S47 person. Actor B independently receives the current event under a B access witness, runs the accepted S39 guarded-comparison rule with B-owned source records, produces its own generation and attempt receipt, and an independent B performer realizes only the selected attempt under actual world constraints. A minimal typed source adapter maps only a performed `EXPLICIT_REFUSAL` to `REFUSE_TOOL` and sends it through the normal S42/S47 C8/C9 path. The actual root has no current B-owned context source, so its actual path remains a typed `S49_MISSING_CURRENT_B_ACTOR_OWNED_CONTEXT` hold with no B world event and no C8.

## Scope and base

- Branch `codex/sorok-s49-independent-actor-producer`; base S48 `9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7`; accepted S47 `765a441f87292aa4c17794745b65cb54e6aaa83f`.
- Writes only `WORKER_RETURNS/SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1/**`; no accepted component rewrite, provider call, agent, native grant, new psyche/learning/weights, or broad accepted-suite run.
- Reuses S39 `generate_choice`/`FULL_RULE` and source validation, S36 access witness, BP4 world events, S48 canonical store/dispatch/replay, and S42 normal C8 consumer.

## Implemented

- B access is derived every time from the canonical C12 perception store and current action event identity/location/clock/channel/hash. The session metadata cache was removed. If the store has no qualifying perception row, access is `NOT_WITNESSED`; presence alone is not access and metadata cannot create it.
- `s49/actor.py` uses the accepted S39 FULL_RULE and B-owned source records, with root/role/rule/access/source-chain binding. The performer validates the exact canonical C12 generation episode plus the canonical attempt-intent episode: sealed body, actor B, branch, root ID/hash, current event ref/hash/time/as-of, FULL_RULE rule ID/version/content hash, source refs, access source/hash, source-chain digest, option and attempt request link. Forged/mutated role, root, rule, source refs, actor/branch/event, or access are denied before any world event.
- `s49/session.py` appends B generation, attempt-intent, performer and result episodes to the same C12 store and uses a typed adapter only for `EXPLICIT_REFUSAL -> REFUSE_TOOL`. Source and case bind generation hash, attempt hash, rule hash, access preimages and source-chain hash. `ATTEND_OBJECT`/`REQUEST_TOOL` remain typed source-adapter holds.
- A minimal S42 `admit_event` base-class mandatory guard now validates the S49 chain at the actual normal consumer before C8, independently of the optional S49 override. It detects a generated B source from canonical world provenance even when every `s49_` extension is stripped and fails closed if the canonical chain is absent; it independently accepts only a complete canonical chain. The optional override being monkeypatched to no-op cannot bypass it. Legacy actual non-S49 sources remain unchanged.
- The mandatory guard requires exactly one actual canonical `B_PERFORMER` result for the generation, a sealed attempt, `ADMITTED`/performed status, generation/actor/branch/event/hash/world-clock linkage, and exact `attempt.hash == source.s49_attempt_hash`. Missing, ambiguous, denied, foreign or substituted results fail closed before C8; removing and restoring the canonical performer result is tested.
- The exact canonical attempt-intent episode is compared field-for-field with the expected attempt preimage: actor B, role, root ID/hash, branch, event ref/hash, generation hash, request hash, option, FULL_RULE ID/version/content hash, access refs/hashes, source-chain digest and seal. A forged sealed intent is denied before any B world event.
- Actual root B sources are deliberately empty: the accepted root history/state does not supply a current B-owned S39 predicate source. No urgency, willingness, preference, demographic, resource, or project prose is converted into a B premise. This is the exact remaining content dependency.
- Controlled B sources use the explicit S39 TEST_ONLY model-premise grade and are labeled `TEST_ONLY_S49_CONTROLLED_B_MODEL_PREMISE`; they are not claimed as observed B inner life. The controlled positive also requires a genuine B perception/ADP017 witness delivered through the C12 perception path; the model premise alone cannot license access.
- SCI05 nonempty self-account hold, no narrative psyche write, no target, and S48 dispatch/replay/cold/no-fake-positive guarantees remain intact. No new provider call is made.

## Evidence

- Working entrypoint: `run_s49.py` exits 0; `logs/entrypoint.log`, `evidence/entrypoint.json`.
- Actual root: `B_CONTEXT_HOLD`, reason `S49_MISSING_CURRENT_B_ACTOR_OWNED_CONTEXT`; world events 13→13, clock 222→222, C12 events 1→1, no B event/C8, verify true.
- Controlled B path: B actor `TEST_ONLY_BP1_R26V_ACTOR_B`, selected `EXPLICIT_REFUSAL`, performer `ADMITTED`, actual B refusal event, adapter `REFUSE_TOOL`, normal consumer event ordinal 2, C9 `NO_CHANGE`/`NO_PROPOSAL`, zero targets.
- Controlled source cut/restore: removing controlled B sources produces no B event/C8; restoring them produces a new independent B attempt and consumer path. The second normal-consumer status may be typed `OPEN` if the accepted finite generation/history set is unresolved; it is not labeled success.
- Base guard stripping/bypass regressions and exact forged-intent regression are in the focused suite.
- Performer denial: controlled B `REQUEST_TOOL` with actual zero B free hours is denied, no event. Forged generation/attempt bodies are denied before any world event; the review access/forgery reproducer exits 0 with absent access `NOT_WITNESSED`, forged result `DENIED`, world event count unchanged, and verify true.
- Closure probes exit 0: access cache bypass is `NOT_WITNESSED` both ways; role/root/rule/source-ref mutations are DENIED with 13 world events; clean normal consumer is OK; rehashed chain is refused at normal consumer; foreign/stale source is refused. `logs/repro_s49_closure_probes.log`.
- Cold: canonical B generation/attempt/result episodes reopen and verify with no provider call.
- Focused S49 tests: **13 passed**, 0 failed/error/skipped; `junit/s49_full.xml`, `logs/s49_full.log`, `evidence/test_run.json`.
- Preserved reviewer access/forgery reproducer: `logs/repro_s49_access_and_forgery.log` (not a provider call).
- Preserved reviewer closure probes: `logs/repro_s49_closure_probes.log`.
- Final legacy/bypass probe: `logs/repro_s49_legacy_bypass.log`: stripped S49 source refused; a valid chain with a bypassed override is still independently base-validated; forged intent DENIED at 13 world events. Normal-consumer performer cut/restore and rehashed attempt substitution are covered by focused tests.
- Source manifest: `evidence/source_manifest.json`; S48 files exact at accepted cut; S49 files local; minimal S42 normal-consumer seam hash recorded.

## Known interfaces and exact missing content

- Reused: S44 root B actor/world state, BP4 world events and access, S39 source/model/rule, S36 actor access, S42/S47 normal consumer, S48 canonical store and dispatch/replay.
- Present: B actor ID, B access witness, B performer constraint checks, B source generation/attempt receipts, normal source adapter for performed refusal.
- Absent: a current B-owned S39 context/history source with registered test-model/actor/source/time/custody sufficient to select a unique actual B option. The actual root cannot support a genuine B-positive without that source; S49 leaves the path held instead of deriving motive from state or demographics.
- If a real B source provider is later installed, it must bind root/owner/actor/branch/time/receipt chain and pass the normal S42 consumer before C8; no callback/dict-as-authority or permissive grant exists.

## Limits

- `TEST_ONLY` controlled B premises are not observed B inner life, a human B, native actor/science, T, SCI05, OBL062, or Pyat. No new empirical weights, preferred action, willingness policy, desired action, or demographic inference was added.
- Actual root B positive remains content-held. The controlled positive is labeled controlled grade and is not advertised as generated actual life. The actual root B access is observed through C12 perception, but the B context source is absent.
- No provider call was made; no native/source/human/C8/C9/C12 grant was issued.

**Terminal:** `S49_INDEPENDENT_ACTOR_PRODUCER__B_ROLE__S39_REUSED__CONTROLLED_REFUSAL_NORMAL_C8__ACTUAL_ROOT_MISSING_B_CONTEXT__NO_PROVIDER__NO_NATIVE_GRANT`.
