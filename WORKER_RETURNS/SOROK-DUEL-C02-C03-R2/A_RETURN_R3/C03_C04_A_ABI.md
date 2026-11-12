# C03/C04 A relay ABI — decision/action/utterance and actual Nadia experience

**Status:** sourcefree `SOURCEFREE_S2_ONLY`; C03/C04 public act/perception consumer constructed. Not native parent psychology or durable Nadia memory.
**Implementation SHA:** `61f2918ec947e44dd7ecff8fd3359734469e9a90`.
**B implementation/return:** `255fd4905990e3c0cab3e2d95ba91b851ea701a8` / `1510d835fcf0a35a5b352b27f4daf4b1f0bb6b34`.
**Composition start:** `01b2d2d23259969778ce996f5527037d666f46f8`.
**Contract:** `08a323b490df4e2ddd0dca7f8b3cd394dfe17e0a`; protected baseline `6a5c12f04323d74001f9632063ec907f4fc4468e`.

## C03 — truthful decision/action inputs

B's `parent_decision.py` remains the decision owner: explicit sourcefree
obligation/purchase rule, caller-supplied objective request, no Nadia state,
no LLM, admitted decision then separately performed action.

A added disclosure fields, without changing the rule:

```text
decision receipt:
  request_source = CALLER_SUPPLIED_OBJECTIVE_REQUEST
  decision_evidence = EXPLICIT_SOURCEFREE_RULE_NOT_NATIVE
  physical_admission = NOT_YET_PERFORMED
  language_generation_owner = C04_CALLER_SUPPLIED_TEXT
  native_science = false

action receipt:
  decision_evidence = ADMITTED_DECISION_REEVALUATED_AT_PERFORM
  physical_admission = PERFORMED | VALID_EMPTY | HELD
  language_generation_owner = C04_CALLER_SUPPLIED_TEXT
  native_science = false
```

The perform path revalidates the admitted decision proposal under the repaired
market→parent lock composition, then uses B04's actual unlocked writer. A stale
decision refuses `PARENT_DECISION_STALE`; replay returns the stored action
receipt without a second debit; a B04 refusal becomes an explicit non-performed
action receipt, not a fabricated success. The decision rule is sourcefree
engineering evidence, not native/MIII mother science.

## C04 — parent utterance and actual Nadia consumer

B's `parent_speech.perform_parent_utterance` remains the writer: one actual P2
`SPEECH` event; parent `own_speech` receipt; child `speech` receipt only under
the bounded same-room registration; hidden reason/hash in a separate self-only
C12 utterance episode.

A added `parent_speech.read_child_experience` and the normal P6 consumer:

```text
run_p6.experience(state, command="child-experience",
                  event_id=<id> OR operation_id=<utterance op>)
```

The P6 command opens the normal owner, checks source/boundary, then:

1. resolves the exact parent utterance episode;
2. requires child = focal root actor and actual child alias;
3. verifies utterance root/branch, actor/alias, event ID/hash, SPEECH kind,
   occurrence clock, text, and recomputed `utterance_source`;
4. requires the parent `own_speech` receipt at the event clock;
5. requires the child `speech` receipt via `read_child_uptake`;
6. requires the event in `situated.recent_speech` — the existing P6 actor
   perception/current-experience path — and matches text/speaker/clock;
7. requires the admitted parent decision episode to exist and match the
   utterance's decision action, without exposing its basis;
8. returns only public speech + a bounded response input.

Returned child experience:

```text
SOROK_CHILD_SPEECH_EXPERIENCE@1
status=PERCEIVED
speaker_actor_id/alias, child_actor_id/alias,
event_id/hash, occurrence_clock, read_clock, receipt clock/channel,
public event projection (no hidden reason/hash),
access_condition=SAME_ROOM_AT_ADMISSION,
access_owner=C12_SPEECH_PERCEPTION_RECEIPT,
text_source=CALLER_SUPPLIED_NOT_GENERATED,
language_generation_owner=NOT_IMPLEMENTED,
hidden_reason=NOT_READ, decision_state=NOT_READ,
custody=C12_SPEECH_RECEIPT_NOT_MEMORY,
durable_acquisition=MISSING_RULE,
user_view=NOT_EXPOSED,
response_input=SOROK_CHILD_SPEECH_RESPONSE_INPUT@1
```

The response input is an actual input for the next actor response owner, not a
memory, acquired trait, native rule or generated reply. Hidden reason/hash and
the parent decision action/basis are not child-facing. Same outward text with
different hidden reasons yields the same public text/input; parent self-read
remains distinct.

Negatives:

- no child receipt (child elsewhere, or co-presence without receipt) → P6/child
  experience `NOT_PERCEIVED`, no text;
- missing parent `own_speech` receipt → `PARENT_ACTIVITY...`/child experience
  receipt refusal;
- child receipt wrong channel/clock → `CHILD_UPTAKE_RECEIPT_MISMATCH`;
- severed speech event → `CHILD_UPTAKE_EVENT_SEVERED`; decision remains;
- forged event author/hash/source → child experience mismatch refusal;
- ordinary P6 user view/say do not expose the parent utterance; Nadia's
  experience is a separate actor-facing result.

The bounded same-room condition is the existing writer's experimental access
rule; this does not claim general senses or turn arbitrary co-presence into
knowledge. The C12 receipt is the access owner. No P4 user-speech semantics,
P3 psychology/context, P6 house/situated file or Pair1/2 module was edited.

## Remaining owner seams

- C03 text/hidden reason remain caller inputs; no general parent language
  generation owner is implemented. The exact remaining seam is a parent
  decision/expression generator with its own competent source/authority, not
  an LLM sentence counted as an act.
- C04 response input is ready for a next response owner; no durable
  psychological uptake/native CAN rule is issued.
- Full P3 `BatchEngine` actor-decision consumption and P3 source closure remain
  Pair2/shared-owner integration.
- MI/P5/P6 exposure of `MATERIAL_ACTIVITY`/parent speech remains unextended;
  the user view is intentionally not the Nadia experience.
- E03 SIGKILL composite recovery, forks and shared household economics remain later tasks.
