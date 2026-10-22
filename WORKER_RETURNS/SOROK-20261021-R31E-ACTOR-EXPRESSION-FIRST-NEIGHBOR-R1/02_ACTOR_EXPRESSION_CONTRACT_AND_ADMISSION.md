# R31E actor-expression contract, candidates and admission

## Separation preserved

`ACTOR/WORLD TRUTH != ACTOR-ACCESSIBLE KNOWLEDGE != OBJECTIVE OCCURRENCE != USER PHENOMENAL SURFACE != INTERPRETATION`

The actor-side contract may consume actor-authorized source/world/history state. The user surface is produced only from admitted world events and U's actual perception rows. User attention is not in the actor contract.

## `R31E_ACTOR_REALIZATION_CONTRACT@1`

`r31e/expression.py::compile_contract` compiles:

- **source/custody:** R29P ref, target id, consumed-state hash, C8 digest, CAN008/CAN011 hashes, E2 hash, actor id;
- **actor:** role, material position, availability status, free hours, material/tools, completed/debt units, health, practices, project labels;
- **world:** clock, positions, resources, scene-open, contact, actor-presence;
- **B:** public role/position, co-presence, A-perceived B events and whether A observed B's offscreen act;
- **knowledge:** A-perceived event ids, exact user utterances A heard, A's own speech;
- **history:** prior help, prior contact, prior refusal, prior user-turn count/texts, prior user-event id;
- **situation:** trigger kind/text/event id, time/material pressure, availability, `attention_excluded=true`;
- **features:** bounded semantic features (question/offer/contact/private/intimacy/coercion/insult/about-B/work/invitation/self-disclosure/unsupported memory/prior reference/known topic);
- **motive status:** `MATERIAL_TIME_CONSTRAINT_ONLY` or `MOTIVE_UNDERDETERMINED`; no hidden trait is invented;
- **expression port:** `R31E_EXPRESSION_PORT@1`, `LIVE_ACTOR_MODEL_NOT_RUN`.

`contract_hash` is the canonical digest. It is stored in every admitted event and every admission record.

## Candidate proposal

`propose()` selects a strategy from the contract:

- boundaries: insult, coercion, privacy, forced intimacy;
- contact: grant/defer/refuse based on actual availability and prior help/contact/user turns;
- help: accept/refuse based on actual free hours, material, tool and availability;
- work: explain, recall prior help, or defer under time/material pressure;
- reciprocity after self-disclosure, with a bounded topic slot;
- recall of a prior user utterance only when that exact event is in A's knowledge;
- B knowledge: present, observed-offscreen, or `UNKNOWN_B` when A did not observe;
- invitation decline, unknown-topic defer, unsupported-memory refusal;
- acknowledgement, actor initiation, departure, later message, return;
- lawful task-bound silence.

Each strategy has multiple structured templates. A stable index over `(contract_hash, strategy)` selects a variant; this is **not** user-attention-dependent and not a single keyword-to-line mapping. The proposal set and strategy rationale are stored in the admission record.

## Admission checks

`r31e/expression.py::validate` re-renders the template from its slots and rejects unless all pass:

- scene open (or the typed `MESSAGE` outside-portal occurrence);
- actor present (or message);
- contract clock equals session clock;
- template known and exact re-render equals candidate speech;
- speech nonempty/single-line/<=240 chars;
- no forbidden private token (`cash`, `debt_units`, `free_hours`, `material_remaining`, source/history ids, etc.);
- no private numeric values in speech;
- every `fact` is supported by actor/world/history/knowledge (actor fields, project, tool resource, time/material pressure, prior help, user event, actor knowledge, knowledge absence, B presence, memory absence, contact feasibility);
- every `knowledge_ref` is an A-perceived event;
- repair capacity and workshop location for a repair action;
- contact feasibility for a grant;
- established channel for a message.

If no candidate passes, one bounded `SILENCE` occurrence is admitted; there is no LLM rerender/reviewer loop.

## Binding/admission record

`admit()` writes:

1. optional exact `REPAIR` world event with owner receipt;
2. exact `SPEECH` world event with `body.text`, `gesture`, `tone`, strategy, contract hash, admission id;
3. or exact `MESSAGE` C12 episode for outside-portal traffic;
4. or `NO_CHANGE` silence world event with strategy/admission id;
5. `EXPRESSION_ADMISSION` C12 episode containing the admission record and candidate;
6. optional A/U `CONTACT` C12 episodes;
7. a checkpoint.

`R31E_EXPRESSION_ADMISSION@1` includes source ref, target, consumed hash, contract hash, strategy/template, exact speech event id/hash, action event id, message episode id, validation checks, `attention_excluded=true`, and motive status. The user surface uses only the bound text/gesture/action; it never reads the contract.

## Port for later integration

`R31E_EXPRESSION_PORT@1` (v1) is in `evidence/port_receipt.json`:

- contract schema, candidate schema, admission schema;
- 60 templates / strategy families;
- source R29P ref;
- `live_actor_model: LIVE_ACTOR_MODEL_NOT_RUN`;
- zero provider calls.

Future R31J/R30G integration can supply the same actor/world/readset into this port without importing unreturned sibling code. No original semantic owner is replaced.

## Source/custody

- R30A return: `ce0dfc67ef5058338f4d7161d32a8cb5bdf733a6`.
- R29P return: `001b506fa26ae879ff5b6e57138fc2696e12b538`.
- Vendored R30A/R29P code: `vendor/r30a/` (186 files), hashes in `evidence/source_manifest.json`.
- Live M6 blob `74d9701c…`; live guard blob `e0528d65…`.
- Actual C12 copies: `evidence/c12_available.sqlite` (`1c859cad…`), `evidence/c12_pressed.sqlite` (`3a2710a4…`); both `root` and `first_session` verify with `R26E_QUALIFIED_C12_PREIMAGE`.
