# Original V3, Neo-V3, Astra and user-product contradictions

## 1. Source boundary

Original V3 is **not present as a Python path in current PREMAIN `c061dc018`**. It
exists in the external extracted archive
`/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging/v3/`:
114 Python modules, 579 functions and 43 classes after AST counting of the package,
and 114/114 `v3/*.py` archive members byte-identical to the extracted tree.

The archive container itself is not the container claimed by the earlier ruling:

```text
actual Rawlsing_code_bundle_staging.zip SHA-256:
3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289

expected SHA-256 in W1_FIRST_BATCH_INTERIM_RULING:
953c9149bd03877206e3cb440d1f4db35dea6473af30b97fd23b7e76c6fc0086
```

This is a container-identity mismatch, not a demonstrated member-byte loss.
The selected V3 member bytes are present and checked. The earlier R5 finding of
31/31 selected and 488/488 `.py` equality is historical evidence, not rerun here.

## 2. Original V3 actual code and its real consumer

The external app's actual path is:

```text
server/generation/simulation.py::run_simulation_for_session
  -> v3.io.identity_to_backbone.backbone_state_from_identity
  -> v3.engine.yearly_step.run_one_year
  -> optional v3.engine.run_llm_band.run_llm_band_year
  -> v3.io.persona_sheet.build_persona_sheet
  -> server/chat/turn.py::chat_turn
  -> v2.run_conversation_chat.load_persona_sheet_with_integrity
  -> v2 prepare_conversation_turn
```

Exact source symbols read:

- `v3/io/identity_to_backbone.py::backbone_state_from_identity` L209
- `v3/engine/yearly_step.py::run_one_year` L12
- `v3/engine/step_runner.py::run_n_years` L13
- `v3/engine/event_engine.py::sample_events` L127
- `v3/engine/run_llm_band.py::run_llm_band_year` L146
- `v3/render/phenomenology.py::render_year` L55
- `v3/io/persona_sheet.py::build_persona_sheet` L579
- `server/generation/simulation.py::run_simulation_for_session` L890
- `server/chat/turn.py:127-157`
- `v2/run_conversation_chat.py::load_persona_sheet_with_integrity` L36

This is a real external-staging application path, not a claim that current
PREMAIN imports it. Current PREMAIN has no `v3/` directory and no
`BackboneState`/`v3.engine` importer outside `WORKER_RETURNS` and recovery data.

## 3. Original V3 versus current accepted Neo science

### 3.1 Numeric defaults and scalar psychology

`v3/core/state.py` defaults `Capacity`, `PsychologicalCapacity`,
`ReproductionConstraints`, `AlienationVector`, `Registers` and `WoundVector` to
50/0–100. `v3/engine/event_engine.py::sample_events` generates code-only
`pseudo_random_mechanical` events with numeric deltas and artificial event
counts. The app renders those into a persona.

Current W1/CAN holdings contradict treating those values as terminal science:

- CAN-009: no universal recovered 0..100, midpoint 50, common additive
  normalized delta or universal clamp; quantity/measurement contracts are
  parametric and missing authority fails closed.
- CAN-010: need axis tokens are reference vocabulary, not magnitudes,
  priorities, birth profiles or desire; zero strivings is lawful.
- CAN-011: the six historical modules are not permanent psyche families;
  terminal middle state is a minimum `V3MS_MEDIATOR`, `V3MS_TENSION`,
  `V3MS_PRACTICE` registry with exact causal parentage.
- CAN-008: response requires concrete actor-specific Rule A over exact
  admitted parent streams; a pseudo-random event is not a response.
- ADP-017: objective truth does not automatically become actor knowledge;
  memory does not automatically become first-person permission.

**Verdict:** the external V3 state is historical executable architecture and
demo surface, not current native psychological rule authority.

### 3.2 Parent driver → Enneagram → child surface

The external app's parent flow calls:

`v2/parent_type_inference.py::infer_parent_type_most_likely` L129
with `v2.parent_type_inference.infer_parent_type` L33 and
`server/generation/simulation.py:359-438`, using `get_driver_vec` and
parental warmth/authority/material support. It then writes
`parent_expectation_baseline`/`transmission_regime` and
`v3/io/identity_to_backbone.py` L515-560 calls
`v3/io/parent_baseline_from_behavior.infer_parent_baseline_and_regime` L25 and
`child_model_from_parent_baseline_and_regime` L60.

The actual legacy JS stack is separate:

- `enneagrams/cross-data/driverSchema.json`: 40 driver keys.
- `enneagrams/cross-data/driverTypeWeights.js`: 40 driver maps × 9 type
  weights; `getTypeScores`/`processCSV` in `enneagramBatch.js`.
- `enneagram.js`: `computeEnneagramProfile` L11, `sampleEnneagramType` L104,
  `getTypeName` L124.
- `init.js:868` calls `computeEnneagramProfile`.
- `V2_V3_DIRECTORY_REQUIREMENTS.md` states `init.js` and the legacy JS stack
  are **not used by v2/v3** at runtime.

**Verdict:** the JS `driverSchema`/`driverTypeWeights`/`enneagramBatch` are
historical Node artifact producers, not a current V3 runtime. The Python
parent-type heuristic is a real external-app consumer, but its Enneagram
typing and parent→child inference have no current CAN/ADP/SCI05 authority.

### 3.3 V3 LLM band and persona rendering

`run_llm_band_year` executes `parse_candidate_packet_with_fallback`,
`select_candidates`, delta application and `render_year`; it has an explicit
`fallback_first_candidate` path and a retry path in `render_year`. The
external app calls it at selected band ages when an API key exists.

Current law distinguishes:

- `CAN-022`: renderer is wording-only; a final semantic plan must be admitted;
  valid-empty means no model call and no fallback utterance; hidden
  biography/persona/raw V3 is not prompt material.
- `CAN-024`: presentation is noncausal by default; in-world causal mode is
  explicit and packaging-eligible only.
- `CAN-025`: packaging is not admission, occurrence or downstream effect.
- `ADP-017`: first-person claim permission is an explicit ceiling.
- `CAN-017`: register may narrow or withhold, never widen epistemic access;
  no demographic personality voice.
- `CAN-016`: salience is turn-local and cannot manufacture first-person truth.

The old `build_persona_sheet` composes voice, wound pattern, backstory,
micro-traces and lifestyle into a V2 prompt surface. It is an **external
presentation compiler**, not a current M6 actor-safe claim envelope. Its
outputs include exactly the kind of biography/persona material CAN-022
forbids as hidden renderer input.

## 4. Neo-V3 and sourcefree actual chain

The historical Neo/sourcefree chain is real code with real first consumers:

```text
BP1 build_two_actor_life
  -> BP3 ExclusiveJournal / KeyedMonotonicAnchor
  -> BP2 JoinedProducer (E1, TEST RULE_A, TEST RULE_T, C9 target, E2)
  -> BP4 c10.receive + C12Store + A0–A3 product
  -> BP2P4J JoinedProduct (actual target/practice materialization)
  -> R31J PreC9Producer + R31JProduct
  -> R31E R31ESession actor expression
  -> JOIN JoinedSession.start/open
```

Actual consumers:

- `BP4Product.observe` calls `c10.receive` and exposes M6 claims.
- `JoinedProduct` subclasses `BP4Product` and materializes BP2 target/E2.
- `JoinedSession.start` calls `build_product` and `material_inspect` or
  `record_omission`; `JoinedSession.open` reopens `R31JProduct` and verifies.
- `R31ESession.say` composes an actor surface after M6 readiness.

Limits from actual source, not labels:

- BP1 sources are `TEST_ONLY_BP1_*`, roles `repair`/`finishing`, with no
  psychology or native grant.
- BP2 Rule A/ Rule T / E2 are TEST_ONLY; the source contains a finite
  scientific-decision request, not issued native rules.
- BP3 key and anchor are TEST_ONLY external files, not D1/D2 native custody.
- BP4 `C12Store.verify` is self-referential: `BP2P4J/c12_verify.py` documents
  and verifies the actual `digest(body without hash)` chain independently.
  The delivered C12 verifier is an engineering REVISE; the positive is not
  erased.
- BP2P4J `c12_verify` exists precisely because the upstream verifier is
  defective; this is an actual code defect, not a recovered speculation.
- R31J `prepare_life` edits the A snapshot with `tools_remaining=1` when
  `material_feasible_after` is true, so binding a B source hash is not proof
  that C9 reads the complete B material fields.
- R31E `expression.py` is a deterministic template/proposal/admission path,
  not an open-ended language model or human A5.
- JOIN sourcefree acceptance covers bounded same-root/fork behavior only; the
  hostile review does not prove full original B pre-C8 severance.

## 5. Current PREMAIN structural estate versus V3

Current `rawlsing_next` implements a different lineage:

```text
m1 temporal/V554 admission
  -> m2 V555 atomic route
  -> m3 V556 higher-order structural
  -> m4 V557 publication + V558 immutable repository/resolver
  -> m5 currentness/RSC/peer-prior
  -> m6 actor-safe expression
  -> render_bounded_expression (positive authority blocked)
```

`wsc_gt0_end_to_end` deliberately returns
`BLOCKED_POSITIVE_ACTOR_PATH__SEMANTIC_CONSERVATION_PASS`; `run_gt0_prev3_v3`
uses the zero-positive V3 guard and `run_gt0_v3_v2` refuses to create a claim
or render. This is an actual negative-path consumer, not a person runtime.

`data/ddm_build_copy` is a separate V550–V558 build/certification harness. Its
V554 seed contract, V555 mediation, V556 pressure-flow, V557 renderer contract
and V558 runtime gate are contract/audit producers; `ddm_v5_thin_end_to_end`
builds a thin packet chain. It has no current app importer and does not compile
a V3 person.

**Conclusion:** current PREMAIN has robust structural/contract/zero-positive
machinery, but no current V3 actor runtime and no V3→V2→A5 app path.

## 6. Astra and product evidence

Astra was not read by this code flight. The user/vision worker owns the
00–87+ and Astra corpus. Therefore this return does not claim whole-Programma
completeness; it provides the engineering/source/consumer delta that the
vision and HQ flights must join to the same future reference.

Product contradictions that remain material:

- Original V3's persona sheet is a rich authored/rendered surface; current
  actor-safe law requires source-bound, actor-limited claims and wording-only
  rendering.
- Original V3's parent typing and driver→child heuristics can create a
  demographic/typological causal shortcut; current law explicitly rejects
  demographic/Enneagram authority.
- The historical sourcefree chain has real material/tool/event/clock behavior
  but no native world, native B, native C8/C9/C12, native CAN/ADP/SCI05, C11,
  or human A5.
- The external app's `OPENAI_API_KEY` path can generate parent narratives and
  V3 scenes, but no provider call was made here and no model output is
  scientific authority.

## 7. Test and evidence status

- Original V3 tests exist in `v3/tests/`; R7 records the earlier RCF-A court
  as 40 passed and a mutated step order failing its named invariant. This
  flight did not rerun them because no per-run execution permission was given.
- BP2P4J author tests and BP2P4JI independent review are historical evidence;
  BP2P4JI returned engineering REVISE on the delivered verifier.
- JOIN hostile review covers bounded sourcefree behavior; no native or human
  proof.
- No external app, API, model, database, native source or human participant
  was executed in this flight.
