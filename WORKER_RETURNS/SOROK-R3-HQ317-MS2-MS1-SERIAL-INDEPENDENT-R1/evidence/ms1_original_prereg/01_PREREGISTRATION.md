# HQ316 MS1 — PREREGISTERED SERIAL ADP016→ADP017→CAN008 MEDIATION DESIGN (FROZEN PRE-EXECUTION)

**Status:** `FROZEN_BEFORE_ANY_NEW_RULE_OR_TEST_CODE`
**Role:** independent bounded source-free causal experimenter. NOT HQ, NOT a semantic
issuer, NOT M06, NOT an acceptance reviewer of M05, NOT a V3 person.
**Grade:** test-only feasibility and causal identification. No accepted new psychological,
actor or model law is created, proposed as operative, or adopted here.

---

## 0. The question, stated so it can fail

Can a genuine **serial** chain be *constructed and causally identified* at lawful
source-free TEST_ONLY grain —

`ADP016 committed memory CONTENT` → `ADP017 private BELIEF / access state` → `later CAN008 response`

— using **actual accepted-owner native interfaces**, such that the response is shown to
change when memory content changes and to change back when the epistemic mediator is
lawfully interrupted, with event history and direct actor-facing inputs held fixed?

This is deliberately **not** the M01/M02/M04 result. Those established **parallel**
memory→response and BELIEF/access→response transfer functions. Parallel effects do not
establish a serial path: two arrows out of two causes are observationally consistent
with any serial story unless the mediator can be cut.

---

## 1. Native interface facts read from pinned blobs BEFORE any new code

These are the load-bearing constraints. Each was read directly out of the pinned native
source; none is a paraphrase of an author's claim.

| ID | Native fact | Where | Consequence |
|---|---|---|---|
| **F1** | `adp016_form_causal_trace` computes genuine source-linked **content**: per-feature `source_feature_bindings` with `state=content_state`, and `uncertainty_state ∈ {CERTAIN, UNCERTAIN}` derived from `content_state`. | `owner_transitions.py` L118 | Real memory content exists and differs by construction. |
| **F2** | The `memory_id` preimage is `['V3_MEMORY', authority_id, authority_version, actor_id, src, trace_key, memory_id_override, rule_id, rule_version, rule_hash]` — **`content_state` is absent**. | `owner_transitions.py` L117 | The **same memory ID** may carry **different verified content**. This is the legal lever for a content intervention that keeps identity fixed. |
| **F3** | `adp017_apply_epistemic_effect` requires `stance_kind == grant['stance_kind']`, and `bind_claim` hard-fails unless `stance_kind == 'BELIEF'`. | `owner_transitions.py` L160, L76 | The **only lawful stance is private BELIEF**. K5 ceiling is native, not self-imposed. |
| **F4** | `memory_basis_refs` are checked for **existence only**: `if any(m not in context.memories …)`. The native epistemic path **never reads memory content**. | `owner_transitions.py` L165 | **There is no native memory-content→stance computation.** Mere attachment of a reference is provably not a transition. |
| **F5** | `claim_accessibility` is a lawful caller parameter that lands in real owner state (`current_claim_accessibility`) and selects `first_person_permission`: `CLAIM_ACCESSIBLE`→`PERMIT_FIRST_PERSON_BELIEF`, `CLAIM_INACCESSIBLE`→`DENY_FIRST_PERSON_CLAIM`, `CLAIM_ACCESS_UNKNOWN`→`DEFER_MISSING_AUTHORITY`. | `owner_transitions.py` L168/L179–182; `adopted_contract.py` L283–297 | This is the **only native channel** on which a content-derived quantity can act on epistemic state. |
| **F6** | `stance_operation` ∈ `ADD/WITHDRAW/SUPERSEDE_EXACT_RECORD/NO_CHANGE`; `WITHDRAW` with an exact `target_record_ref` genuinely deletes the stance from owner state. | `owner_transitions.py` L167, L171–174 | **Mediator withdrawal is a native admissible condition**, not a simulation. |
| **F7** | Accepted ADP017 text (pinned blob `eece4f3f…`): trace refs *"may condition a private update but never establish conscious acquisition or a knowledge grant."* | accepted authority | Conditioning a **private update** on trace refs is contemplated by accepted text, not forbidden. This is the source-anchored legal foothold for the hypothetical mediator. |
| **F8** | Native `response_rule_apply(coupling, prestate, binding, requested_effect)` takes the effect **from the caller**; `coupline_evaluate` verifies only that memory/stance refs *exist and match*. | `can008_candidate_rule.py` L202–222 | Native CAN008 **computes no response from epistemic state**. Any epistemic-state-reading consumer is necessarily a hypothetical rule. |

**Consequence of F3+F4+F8 taken together:** a serial path is **not** already present in the
accepted contract. It must be *stipulated by a hypothetical TEST_ONLY mediator* applied
*through* the real native formation/application interfaces. That is exactly the bounded
object of this experiment, and it is not an accepted rule.

---

## 2. The two hypothetical TEST_ONLY rules (invented here, unissued)

Both are **hand-authored synthetic candidates**. Neither has an issuer, an authority
grant, a production registry entry, or an accepted semantic identity. They are
quarantined to this return directory and are labelled unissued in every artifact.

### 2.1 `MS1_SERIAL_MEDIATOR@1.0.0-TEST_ONLY`

Reads **real committed memory content from actual owner state** — never a caller label:
1. re-verifies `memory.current_state_hash == memory_semantic_hash(memory)`;
2. verifies provenance: memory ID present in `ctx.memories`, formation transition present
   in `ctx.memory_transitions`, `objective_source_event_refs` bound to a registry-admitted
   source event, actor and time consistent;
3. applies the **content-sensitive map**:

   | actual stored memory content | → native `claim_accessibility` |
   |---|---|
   | `uncertainty_state == 'CERTAIN'` | `CLAIM_ACCESSIBLE` |
   | `uncertainty_state == 'UNCERTAIN'` | `CLAIM_ACCESS_UNKNOWN` |

4. applies the transition by calling the **real native**
   `adp017_apply_epistemic_effect(stance_kind='BELIEF', stance_operation='ADD',
   memory_basis_refs=[memory_id], actor_facing_basis_refs=[E1 ref], …)`.

The mediator decides **only** the accessibility class. The stance, the claim identity,
the actor-facing basis, the rule identity and the time authority all remain native-owned.
No caller-chosen BELIEF outcome is possible: BELIEF is forced by `bind_claim` (F3).

### 2.2 `MS1_SERIAL_CONSUMER@1.0.0-TEST_ONLY`

The later CAN008 candidate consumer. It **reads epistemic owner state and never reads
memory**:
- verifies actor / world / time and `ctx.verify()`;
- reads `ctx.state_sets[claim_id].current_claim_accessibility` and
  `ctx.permissions[claim_id].permission` from real owner state;
- **structurally cannot see memory content** (it never receives a memory argument) —
  this is what makes the direct path structurally absent rather than merely untested;

| real owner permission | chosen effect |
|---|---|
| `PERMIT_FIRST_PERSON_BELIEF` | `REROUTE` |
| `DENY_FIRST_PERSON_CLAIM` | `BLOCK` |
| `DEFER_MISSING_AUTHORITY` | typed nonpositive refusal, **no productive effect** |
| no epistemic state at all | `RESPONSE_INPUTS_VALID_EMPTY` |

The chosen effect is then applied through the **real native** `coupline_evaluate` →
`response_rule_apply` → `build_response_receipt`, and committed to a verified journal.

---

## 3. Competing DAGs (declared before execution)

- **D1 SERIAL:** `M_content → B_access → Y`. The belief/access state is the *only* channel
  from memory to the later response.
- **D2 PARALLEL/DIRECT:** `M → Y` while `B` arises independently from the E1 actor-facing
  event. Memory affects the response without passing through belief.
- **D3 SHORTCUT / HISTORY-ONLY:** the first-event and prior-response history drives both
  `B` and `Y`; `memory_basis_refs` is an inert label and content is irrelevant.

D1 is supported only if **P1–P4** below all hold. D2 is excluded only by **P4**. D3 is
excluded only by **P1** and **P5**.

---

## 4. Intervention matrix (executed cells)

Fixed in every cell: E1 event id/hash/features/time/admission, world cut, actor,
direct actor-facing inputs (`actor_facing_basis_refs`), claim identity, prior CAN008
response history, rule identity/hash, and the later E2 event id/hash/features/time.

| Cell | Memory content (M) | Mediator (G) | Clamp | Purpose |
|---|---|---|---|---|
| C1 | `AVAILABLE_SOURCE_BOUND` (CERTAIN) | ACTIVE | — | baseline |
| C2 | `AVAILABLE_UNCERTAIN` (UNCERTAIN) | ACTIVE | — | **memory-content intervention** |
| C3 | `AVAILABLE_SOURCE_BOUND` | **WITHDRAWN** (native `WITHDRAW`) | — | mediator cut, memory fixed |
| C4 | `AVAILABLE_UNCERTAIN` | **WITHDRAWN** | — | mediator cut under the other content |
| C5 | `AVAILABLE_SOURCE_BOUND` | **INHIBITED** (no belief formed) | — | mediator absent, memory fixed |
| C6 | `AVAILABLE_UNCERTAIN` | **INHIBITED** | — | mediator absent, other content |
| C7 | `AVAILABLE_SOURCE_BOUND` | ACTIVE | **BELIEF+access clamped to C8 value** | **direct-path probe** |
| C8 | `AVAILABLE_UNCERTAIN` | ACTIVE | **BELIEF+access clamped to C7 value** | **direct-path probe** |
| C9 | as C1 | ACTIVE | — | **history-only control**: prior response history withheld |
| C10 | as C1 | ACTIVE | — | **reference-only falsifier**: mediator decides without reading content |

C7/C8 form the decisive **clamp pair**. If the response differs between C7 and C8, a
direct memory→response path exists and **serial identification fails**.

---

## 5. Frozen falsifiable predictions

| ID | Prediction | Falsified if |
|---|---|---|
| **P1** | C1 ≠ C2 in later response, with all history and actor-facing inputs fixed | responses identical → no content-sensitive serial effect |
| **P2** | C1 ≠ C5 and C2 ≠ C6 (mediator present vs absent) | response insensitive to presence of epistemic state |
| **P3** | C1 ≠ C3 and C2 ≠ C4 (native withdrawal) | withdrawal changes nothing → mediation not real |
| **P4** | **C7 = C8** (belief/access clamped across differing memory content) | responses differ → **direct M→Y path exists; D2 survives; serial claim DEFEATED** |
| **P5** | C1 = C9 (withholding response history does not move the consumer's choice) | consumer secretly reads history → D3 not excluded |
| **P6** | stance is private `BELIEF` only; `PERMIT_FIRST_PERSON_KNOWLEDGE` never occurs; no public standing | any KNOWLEDGE/public grant |
| **P7** | causal trace is never first-person claimable; hidden origin always blocked | any first-person origin claim on a trace |
| **P8** | C10 ≠ C2: the reference-only mediator does **not** reproduce P1 | reference-only reproduces the effect → "mediation" was mere label attachment |
| **P9** | tampered memory content (hash mismatch) → mediator refuses, no epistemic state, response unchanged | forged content still drives the response |
| **P10** | every refused outcome leaves owner state **byte-identical** to its prestate | partial state survives a refusal |
| **P11** | cross-actor, cross-claim, cross-time and unknown-memory basis are refused | a foreign basis is accepted |

## 6. Global falsifiers — any one defeats the serial candidate verdict

- **F-A:** P4 fails → D2 (direct/parallel) is not excluded.
- **F-B:** P2 or P3 fails → the epistemic mediator is not on the causal path.
- **F-C:** the native ADP017 interface refuses every content-conditioned call → the
  correct verdict becomes **`SERIAL_MECHANISM_FEASIBILITY_HOLD`** with an exact missing
  interface proposal and a source-anchored counterexample.
- **F-D:** P8 fails → the effect is reference attachment, not mediation.
- **F-E:** P10 fails → transactional integrity is broken and no result is admissible.

## 7. Outcomes that may honestly be returned

- `SOURCEFREE_SYNTHETIC_SERIAL_MEDIATION_CANDIDATE_REQUIRES_I2` — only if P1–P11 hold and
  no global falsifier fires.
- `SERIAL_MECHANISM_IDENTIFICATION_HOLD` — if observational equivalence, the unissued
  rule, or a missing transition blocks proof, with positive **and** negative evidence.
- `SERIAL_MECHANISM_FEASIBILITY_HOLD` — if accepted contracts cannot support even the
  hypothetical mediator (F-C).

## 8. Explicit non-claims, frozen before execution

No human psychological discovery or calibration. No operative V3 mediation. No accepted
semantic law. No production issuer, registry entry, or activation. No original respondent
data. No external experimental model calls. No autonomous actor. No PRE-MAIN/CURRENT edit.
No V3/N12 operation. No dependency on M05 being accepted (M05 is author-only under M06).
No claim that a bounded source-free constructibility result generalizes to any real actor.

**Freeze declaration:** this document was written and committed **before** any new mediator,
consumer, or test code was written. Predictions above may be *reported as falsified*; they
may not be edited after execution.