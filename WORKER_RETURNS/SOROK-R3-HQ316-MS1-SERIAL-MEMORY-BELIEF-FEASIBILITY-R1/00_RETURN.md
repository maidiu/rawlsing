# HQ316 MS1 — SERIAL ADP016→ADP017→CAN008 MEDIATION FEASIBILITY EXPERIMENT

## Verdict

# `SERIAL_MECHANISM_IDENTIFICATION_HOLD`

**The mechanism is CONSTRUCTIBLE. Serial mediation is IDENTIFIED ONLY IN ONE ARM.**
General serial identification is **not** achieved, and I am not awarding the top
candidate verdict — because my own frozen preregistration's gate for it is not met.

Warranted claim grade, per the 00B ladder, **separately per question**:

| # | Question | Grade | One-line answer |
|---|---|---|---|
| a | Expressibility/constructibility of a stipulated memory→belief mediator inside synthetic accepted-owner APIs | **F3** at bounded sourcefree grain | It actually ran: native ADP016 committed content-bearing memory, a hypothetical mediator mapped real content into the native ADP017 accessibility channel, and a hypothetical consumer turned real owner state into a real native CAN008 response. |
| b | Causal contrast in the bounded constructed experiment | **F3, CONDITIONAL** | 12 of 13 preregistered predictions held. The contrast is real *in the `CLAIM_ACCESSIBLE` arm* and **unobservable** in the `CLAIM_ACCESS_UNKNOWN` arm. |
| c | Independently valid source/provenance and transactional integrity | **F3** | All staged bytes verified 9/9 against authoritative Git blobs; every refused outcome left owner state byte-identical; P10/P11 passed. |
| d | Serial path relative to alternative DIRECT/PARALLEL DAGs | **F2, ARM-QUALIFIED** | History-only (D3) excluded on three independent contrasts. Direct (D2) not observed — but only for a consumer deliberately built without one. D1 holds in the permitting arm only. |
| e | Whether operative accepted V3 rule is authorized | **NO — FU, not claimed** | No accepted law authorizes any of this. Both rules are **unissued synthetic TEST_ONLY** artifacts I invented. |
| f | Real human psychological calibration | **NOT CLAIMED** | Out of scope and never asserted. |

---

## 1. Bottom line

**Can a genuine serial memory→belief→later-response chain be built at lawful
source-free grain? Yes. I built it and it ran.**

**Is serial mediation causally identified? Only where the epistemic mediator's
accessibility class is `CLAIM_ACCESSIBLE`.** Where memory content yields
`CLAIM_ACCESS_UNKNOWN`, every mediator state — active, natively withdrawn, or
never applied — produces the same nonproductive refusal. The intervention I
designed to cut the mediator has **no identifying power in that arm**, and that
is a real limitation of the experiment, not a passing result.

**Why not the top verdict.** My preregistration stated the top verdict
`SOURCEFREE_SYNTHETIC_SERIAL_MEDIATION_CANDIDATE_REQUIRES_I2` applies *only if*
P1–P11 hold *and* no global falsifier fires. **Prediction P3b was falsified and
global falsifier F-B therefore fired.** The gate is not satisfied. I will not
quietly reinterpret my own gate after seeing the data.

---

## 2. The decisive finding, stated plainly

The pinned native ADP017 interface has **no memory-content→stance rule**. This is
verified structurally against the pinned bytes, not asserted
(`test_native_adp017_never_reads_memory_content`):

- `memory_basis_refs` are checked for **existence only** — `if any(m not in context.memories …)`.
- The native epistemic function never consults a memory's content
  (`uncertainty_state`, `source_feature_bindings`) anywhere in its body.
- `bind_claim` hard-fails unless `stance_kind == 'BELIEF'`, so the only lawful
  stance is private BELIEF regardless of memory.

So **no serial path already exists in the accepted contract.** What I could build
is a *hypothetical* mediator that decides the one native quantity memory content
can lawfully reach — `claim_accessibility` — and applies it through the real
native transition. That is a bounded constructibility result, and it is the
furthest the accepted interfaces permit without a new accepted rule.

The corresponding legal foothold is genuine: the accepted ADP017 authority text
(pinned blob `eece4f3f…`) states trace refs *"may condition a private update but
never establish conscious acquisition or a knowledge grant."* Conditioning a
**private update** is contemplated. **Knowledge** is not, and was not attempted.

---

## 3. What actually ran

Two **hypothetical, unissued** TEST_ONLY rules, invented here, quarantined to
this return, labelled unissued in every artifact:

- **`MS1_SERIAL_MEDIATOR@1.0.0-TEST_ONLY`** — reads *real committed memory
  content* from actual owner state, re-derives the memory hash, verifies the
  formation transition and admitted source event, then maps
  `CERTAIN→CLAIM_ACCESSIBLE`, `UNCERTAIN→CLAIM_ACCESS_UNKNOWN` and calls the
  **real** `adp017_apply_epistemic_effect`.
- **`MS1_SERIAL_CONSUMER@1.0.0-TEST_ONLY`** — reads *only* real epistemic owner
  state. It receives **no memory argument at all**, so a direct memory→response
  path is structurally absent rather than merely untested
  (`test_p4b` inspects the signature and the source).

Everything else is pinned native candidate source staged byte-exact from CAN2
authored `ee6a48b40247b113c614fe2099d4c443e8dd7bb7`.

### Per-cell receipts (real owner state, not a synthetic table)

All cells share **memory ID `752391fcda…`** and identical E1/E2 event hashes and
claim identity; only memory *content* and mediator state vary. That is the legal
lever: the native `memory_id` preimage excludes `content_state`.

| Cell | Content | Mediator | Owner permission | Response | Decision |
|---|---|---|---|---|---|
| C1 | CERTAIN | active | `PERMIT_FIRST_PERSON_BELIEF` | **REROUTE** | produced |
| C2 | UNCERTAIN | active | `DEFER_MISSING_AUTHORITY` | — | refusal |
| C3 | CERTAIN | **natively withdrawn** | `DENY_FIRST_PERSON_CLAIM` | **BLOCK** | produced |
| C4 | UNCERTAIN | **natively withdrawn** | `DEFER_MISSING_AUTHORITY` | — | refusal |
| C4b | UNCERTAIN | withdrawn, access forced | `DENY_FIRST_PERSON_CLAIM` | **BLOCK** | produced |
| C5 | CERTAIN | absent | — | — | `RESPONSE_INPUTS_VALID_EMPTY` |
| C6 | UNCERTAIN | absent | — | — | `RESPONSE_INPUTS_VALID_EMPTY` |
| C7 | CERTAIN | active, **clamped** | `DENY_FIRST_PERSON_CLAIM` | **BLOCK** | produced |
| C8 | UNCERTAIN | active, **clamped** | `DENY_FIRST_PERSON_CLAIM` | **BLOCK** | produced |
| C9 | CERTAIN | active, history withheld | `PERMIT_FIRST_PERSON_BELIEF` | **REROUTE** | produced |
| C10 | CERTAIN | active, **reference-only** | `PERMIT_FIRST_PERSON_BELIEF` | **REROUTE** | produced |
| tamper | UNCERTAIN | active, **forged content** | — | — | refused `MEMORY_STATE_MISMATCH` |

---

## 4. Prediction ledger — including what failed

| ID | Claim | Result |
|---|---|---|
| P1 | C1 ≠ C2 — content moves the response, all else fixed | **HELD** |
| P2a | C1 ≠ C5 — mediator present vs absent | **HELD** |
| P2b | C2 ≠ C6 — same, UNCERTAIN arm | HELD **but weak**: differs only in typed decision state; both nonproductive |
| P3a | C1 ≠ C3 — real native withdrawal, CERTAIN arm | **HELD** |
| **P3b** | **C2 ≠ C4 — real native withdrawal, UNCERTAIN arm** | **FALSIFIED** |
| P4 | **DECISIVE** — C7 = C8 with belief/access clamped | **HELD** |
| P5 | C1 = C9 — history withheld does not move the choice | **HELD** |
| P6 | private BELIEF only; no KNOWLEDGE; no public standing | **HELD** |
| P7 | causal trace never first-person claimable (K3) | **HELD** |
| P8 | C10 ≠ C2 — reference-only does not reproduce P1 | **HELD** |
| P9 | forged content refused, no epistemic state | **HELD** |
| P10 | refusals leave owner state byte-identical | **HELD** |
| P11 | foreign / cross-actor / cross-claim / cross-time / unknown-memory refused | **HELD** |

Global falsifiers: **F_B FIRED** (via P3b). F_A, F_C, F_D, F_E did not fire.

### 4.1 My own preregistration was wrong — correction protocol (00B §12)

**P3b was mis-specified, and I want that on the record rather than buried.**

I preregistered that a native mediator withdrawal would change the response in
the UNCERTAIN arm. It does not. This was **derivable from my own preregistered
fact F5 before I ever executed anything**: native
`first_person_permission` returns `DEFER_MISSING_AUTHORITY` for
`CLAIM_ACCESS_UNKNOWN` *regardless of whether a stance record exists*. I recorded
F5 and then failed to derive the consequence when writing P3.

The error is mine, not the mechanism's. But it has a real scientific cost: it
removed the identifying contrast in that arm, which is why F_B fires and why the
top verdict is withheld. The prediction was **not edited after execution**; the
falsification is recorded and asserted by a deliberately named test,
`test_p3b_PREREGISTERED_PREDICTION_IS_FALSIFIED_and_is_reported_as_such`.

Cell C4b is the instructive contrast: withdrawing the stance *while forcing
accessibility back to `CLAIM_ACCESSIBLE`* flips the outcome to `BLOCK`. So
**accessibility class dominates**, and the stance record is only observable when
access permits. That is the mechanism's real identifying limit.

---

## 5. Alternative-DAG adjudication

- **D1 SERIAL** (`M_content → B_access → Y`) — **supported in the
  `CLAIM_ACCESSIBLE` arm only.** Backed by P1, P2a, P3a, P4, P5, P8. Contradicted
  by P3b.
- **D2 PARALLEL/DIRECT** (`M → Y`, belief independent) — **no direct path
  observed**, but this is bounded: the consumer was *built* without one. P4 tests
  this consumer; it is not proof that no other rule could expose a direct path.
- **D3 SHORTCUT/HISTORY-ONLY** — **excluded at this grain** on three independent
  contrasts (P1 content-vs-history, P5 history ablation, P8 reference-vs-content).

---

## 6. What this does **not** establish

- **No human psychological discovery or calibration.** `ACTOR_SYNTH_1` is a
  fixture. Nothing here says anything about a real person.
- **No operative V3 mediation and no accepted semantic law.** Both rules are
  unissued synthetic artifacts of this experiment. `production_owner_commit` is
  `False` in every cell; no production registry entry exists.
- **No generality.** One actor, one world cut, one event pair, one finite content
  alphabet, deterministic closure. Per 00B §0A.6 a bounded construct may test a
  seam and receives **no credit** for the problems it removed.
- **No dependency on M05.** M05 is author-only under M06 review; this experiment
  used only pinned CAN2 native candidate source.
- **Not a claim that the accepted contract *should* grow this transition.** The
  minimal interface proposal in §7 is a request for owner adjudication, not a
  design mandate.

---

## 7. Exact missing interface (for the competent owner)

The experiment does **not** need a new owner to exist. It needs one narrow thing
the accepted contract currently lacks: **a lawful way for memory content to
determine an epistemic quantity, rather than merely being attached as a
reference.** Concretely, an accepted rule would have to specify, at minimum:

1. a **content→epistemic map** — which verified memory content states may select
   which native accessibility classes (the map used here is a hypothesis, not a law);
2. an **issuer** — no accepted semantic issuer exists for any of this;
3. a **destination-owner binding** — native code already carries
   `HOLD_NO_ACCEPTED_ADP016_ADP017_POSITIVE_AUTHORITY`;
4. a **lawful knowledge path** — deliberately untouched; BELIEF is the ceiling and
   `adp017_apply_epistemic_effect` refuses `KNOWLEDGE` natively.

Source-anchored counterexample for owner adjudication: with the mediator cut
(C4), the owner state genuinely loses the stance record
(`withdrawn_effect_id` absent from `stances_after_mediation`), yet the later
response is **unchanged** from C2. Any accepted law claiming a memory-content
mediator must explain why a real epistemic deletion produced no downstream change
in that arm — which is exactly why I am not claiming the mechanism generally.

---

## 8. Reproduction

```
python3 -m pytest candidate/can2_test_repair.py test_ms1_serial.py -q
```
Python 3.11.3, pytest 9.0.2, git 2.43.0. **118 passed, 2 failed** — the 2 REDs
are the documented CAN2 law-map artifacts described in
`evidence/native_control_receipt.json`, deliberately not restaged from my own
re-transcription because that would falsify provenance. They are unrelated to
serial mediation.

- `junit/combined_final.xml`, `logs/combined_final_stdout.log`
- `evidence/intervention_receipts.json` — per-cell real owner-state receipts
- `evidence/dag_adjudication.json` — predictions, falsifiers, DAG adjudication
- `evidence/native_source_ledger.json` — 9/9 blobs verified
- `evidence/native_control_receipt.json` — native execution proof

**Model calls by this worker: 0. Cash: UNKNOWN (nothing billed).**