# SOROK S39 — source-bound generated response in the continuing S37 consumer

**RESULT:** `S39_SOURCEBOUND_GENERATED_ATTEMPT__DETERMINISTIC_UNIQUE_SELECTION__M35_C8_E1_TO_ACTUAL_TARGETLESS_C12_C9_LANGUAGE__10_OF_10_FOCUSED_TESTS_PASS__ENTRYPOINT_0__NO_TARGET__NATIVE_HOLD`.

This is one bounded sourcefree constructive-generation experiment. A deterministic, explicitly declared guarded-comparison rule generates an attempted action from source-bound synthetic actor context/history and exact M35 E1/access, without receiving the desired current response or a performed-response witness. The independent targetless performer admits or denies the attempt. The actual result reaches the same S37 C12/C9 consumer and language writer, persists with generation provenance, and survives cold reopen. All target proposals remain empty; CAN011 remains `NO_CHANGE/NO_PROPOSAL`; no T implementation or native authority is added.

## Session, base and scope

- Owner/session: existing OpenCode author `ses_e9387509affeR5dC27RoUy3WSH`; no new agents, no provider/domain/model calls, no timeout wrapper.
- Assigned branch: `codex/sorok-s39-sourcebound-generated-response`; base accepted S37 `e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9`.
- Write scope only: `WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1/**`.
- S38 adjudication `8f037c2f553a902df41b9db3333f41cda26a830e` and court `2d34e1310e51a5a4ff248baa4eb7f9e938d6880e` are reused as settled scope. Only uniquely supported deterministic selection acts; OPEN/cycles do not append an actor action. No stochastic choice, default draw, first-option fallback or enacted inaction.

## What was implemented

- `s39/sources.py`: sealed synthetic `CURRENT_PROJECT`, `ACTOR_PRIORITY` and `HISTORICAL_EPISODE` records. They are labeled `TEST_ONLY_SYNTHETIC_ACTOR_CONTEXT_MODEL_PREMISE_NOT_OBSERVED`; they are not empirical psychology or original human data. Historical sources are available for causal recruitment without a conscious-recall requirement. Forbidden input keys such as `selected_action`, `desired_action`, `response_witness` and `performed_response` are refused. Demographic/type labels are ignored by the reason graph.
- `s39/model.py`: finite options `ATTEND_OBJECT`, `REQUEST_TOOL`, `EXPLICIT_REFUSAL`; typed source-bound `SUPPORTS`/`OBSTRUCTS` reasons; declared versioned rule `S39_GUARDED_CONTEXTUAL_COMPARISON@1` (`rule_content_hash b5de8b26…` in the captured evidence). Pairwise guarded comparisons only; no scalar motive, no universal deliberative agent, no source-free LLM choice. Selection requires exactly one undefeated eligible option. Several survivors or a cycle return typed unresolved and no attempt.
- `s39/performer.py`: routes the selected attempt to existing targetless C12/world/expression writers: `product.inspect` for `ATTEND_OBJECT`, existing actor speech writer for `REQUEST_TOOL`, and the world `REFUSAL` event writer for `EXPLICIT_REFUSAL`. The performer independently checks world/tool state; a denied request produces no action event. No legacy `candidate.action_admission` target is fabricated.
- `s39/producer.py`: reuses S37 `IntegratedProducer.stage_m35`/`evaluate_s36`; checks event access through the actual S36 consumer; builds the S36 response witness only from the independently admitted performer result.
- `s39/session.py`: `S39GeneratedSession` reuses the S37 targetless product/session/reader and language writer, keeps the same actor root/source lineage, writes generation/attempt/S36 episodes, and inherits S37 cold reopen. It advances the C12 world to the E1 clock before action, then commits the S36 targetless response.
- `s39/reader.py`: reads the persisted generation/attempt episodes and binds them to the same C9 response, C12 action event, C8/E1/source and session metadata. Generation/action/C9/C12 mismatch refuses.

## Explicit model premises

1. `REPAIR_URGENT` is a declared synthetic current-project premise.
2. `AVOID_DEBT` and `PREFER_INDEPENDENT` are declared synthetic actor-priority premises.
3. `PRIOR_B_SHARE` and `PRIOR_B_REFUSAL` are declared synthetic historical-episode premises.
4. The guarded comparison rule is a finite product-modeling choice, not empirical psychological law.
5. `REQUEST_TOOL`/`ATTEND_OBJECT`/`EXPLICIT_REFUSAL` are a finite option vocabulary, not a universal action theory.
6. World tool/material/free-hours/actor-presence checks are objective prerequisites; the performer's result is independent of the selector's assertion.

## Actual behavior evidence

Choice probes (`evidence/choices.json`):

| Case | Status | Selected / survivors |
|---|---|---|
| P: urgent repair + prior share + debt aversion | `UNIQUE_SELECTED` | `REQUEST_TOOL`, with `AVOID_DEBT` retained as contrary reason |
| C1: only independent-inspection/debt context | `UNIQUE_SELECTED` | `ATTEND_OBJECT` |
| C2: only prior B refusal | `UNIQUE_SELECTED` | `EXPLICIT_REFUSAL` |
| OPEN: no guarded comparison | `OPEN_CHOICE_SET` | `ATTEND_OBJECT`, `EXPLICIT_REFUSAL`, `REQUEST_TOOL`; no attempt |
| CYCLE: conflicting guarded comparisons | `CONFLICT_UNRESOLVED` | `COMPARISON_CYCLE`; no attempt |
| Missing comparison coverage | `OPEN_CHOICE_SET` | `MISSING_COMPARISON`; no attempt |
| Label-only perturbation | `UNIQUE_SELECTED` | identical `REQUEST_TOOL`; label refs ignored |
| Missing prior-share source | `OPEN_CHOICE_SET` | multiple survivors; no attempt |
| Tampered governing source | `REFUSED` | `S39_SOURCE_INTEGRITY_REFUSAL`; restore returns `REQUEST_TOOL` |

End-to-end (`evidence/chain.json`, `evidence/entrypoint.json`):

- SHARE: B source `16f11d2e…`, C8 `e472d9f9…`; generated `REQUEST_TOOL`; performer `ADMITTED`; C9 `OBSERVED_IMMEDIATE_OBJECT_ORIENTATION`; `NO_CHANGE/NO_PROPOSAL`; zero target proposals/rows; cold verify.
- REFUSE: B source `3e00199d…`, C8 `5e92ae09…`; same generator selects `REQUEST_TOOL`; performer independently `DENIED` (`TOOL_NOT_AVAILABLE`); no actor action event; C9 `RECEIVABLE_NO_OBSERVED_UPTAKE`; `NO_CHANGE/NO_PROPOSAL`; zero target proposals/rows; cold verify. The denied attempt is not success or practice.
- Both histories use the same neutral language plan/native speech/labeled English view. The language plan readset does not include the generation source refs or E1; the renderer does not choose an unresolved action or expose private causal sources.
- Warm/cold `read_generation` returns the same generation hash, attempt hash, action event hash and C9 response ref. A tampered generation binding refuses (`S39_GENERATION_HASH_MISMATCH`); a persisted duplicate/mismatched C12 generation binding also refuses through the same verify path.

Focused tests: **10 passed** (`junit/s39_full.xml`), including end-to-end positive, changed-context choice/unresolved, OPEN/cycle no-action start, label invariance, missing/tampered source and restore, forbidden answer/witness input, independent performer denial, cold reopen and mismatch refusal. Entrypoint exit 0 (`evidence/entrypoint.json`). No broad historical reruns.

## Reused roots/cuts

- M35 `4170fbf19a9d5a64bc728f5b22156bbffcec51e5`; S36 `8da78d8031a06a4bd7e1297fd713e573299c0860`; S37 `e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9`; language `8d2920da951f98cd8246d7c34cac777928e0c732`; JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`.
- S37 is read-only and used through its public `s37/{bootstrap,producer,session,reader,product,harness}.py` seams; no S37 file is edited.
- The recorded S37 source manifest certifies M35 10/10, S36 14/14, language 7/7 and JOIN-E 8/8 exact; S39 reuses those roots and records its own local hashes/origins in `evidence/source_manifest.json`.
- `candidate` originates in the accepted S36 return; `s37.*` originates in accepted S37; `s39.*` is this return. M35 BP2 comes from the S37-vendored exact M35 surface.

## Limits

TEST_ONLY sourcefree synthetic construction. No native CAN008/CAN011 rule or grant, no T implementation, no original/human data, no native C8/C11/C12 or A5 claim. The actor context/history and comparison rule are explicit model premises, not measurements or a validated prediction of a real person. No acquired practice, motive, emotion, belief or durable state is inferred. No provider/domain/model call, new review session, worker spawn, controller/M35/language/PRE-MAIN edit, target fabrication or native promotion. Speech equality across histories is deliberate and does not assert psychological equivalence.

**Terminal:** `S39_GENERATED_ATTEMPT_ACTUAL_CHAIN__UNIQUE_DETERMINISTIC_SELECTION__OPEN_AND_CYCLES_NO_ACTION__PERFORMER_DENIAL_STAYS_DENIED__PERSISTED_PROVENANCE_COLD__10_OF_10_TESTS__NO_TARGET__NATIVE_HOLD`. Final commit and remote SHA are verified after push and reported in the final handback.
