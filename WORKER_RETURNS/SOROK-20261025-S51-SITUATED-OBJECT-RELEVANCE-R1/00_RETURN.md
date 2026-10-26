# SOROK S51 repair2 — next-received-event boundary and semantic recomputation

**RESULT:** `S51_SITUATED_OBJECT_RELEVANCE__NEXT_RECEIVED_EVENT_BOUND__DISTINCT_WITHDRAWN_EXPIRED_CONSUMED_HOLDS__CANONICAL_READSET_RELATION_RECOMPUTED__S49_QUALIFIED_OPEN__NO_EXISTING_OPTION_RELATION__ACTUAL_PURPOSE_UNPROVED`.

This repair preserves the accepted closure gains: the actual world-owned offer and B perception/access, canonical S49 turn/source binding, foreign-input refusal, inert generic supplemental reasons, `OPEN_CHOICE_SET` without a fabricated B action, and the TEST_ONLY/non-native ceiling.

## Changed behavior

- **Next actual received event:** each declaration records the canonical B-perception baseline. The exact next B-received world event is bound in the immutable journal: an offer event becomes `BOUND`; an unrelated received event immediately becomes `EXPIRED` with its event id/hash/clock. A later offer cannot skip or reuse that event. Fresh declarations after consumed/expired/withdrawn states remain possible; prior declarations are not silently extended.
- **Distinct lifecycle holds:** public evaluation now returns `HYPOTHESIS_WITHDRAWN`, `HYPOTHESIS_EXPIRED`, and `HYPOTHESIS_CONSUMED` as distinct typed holds. Missing/inactive declarations remain non-evidence about B's motives.
- **Canonical semantic recomputation:** each relevance episode retains only the evaluation clock and the existing immutable C12 checkpoint hash as its actor/world readset evidence. Live consumption and cold verification resolve canonical object, hypothesis, world offer, access and offer contract; recover the evaluation checkpoint; recompute the relation from permit/payment/task-hours/free-hours; and compare status, relation, financial fields, actor, access, hypothesis and other semantic fields plus the stored digest. Self-consistent false results, a missing readset, or readset substitution are refused. A valid cold replay remains valid and does not use current mutable actor state in place of the recorded checkpoint.
- The offer/access seam, S39 `FULL_RULE`, canonical S49 generation/turn, and generic reason removal from repair1 are unchanged. No option-specific paid-finishing relation, preference ranking, B action, C8 performance, or native purpose was invented.

## Executed evidence

- Focused S51 tests: **13 passed**, 0 failed/error/skipped; `junit/s51_full.xml`, `logs/s51_full.log`, `evidence/test_run.json`.
- Entrypoint: `run_s51.py` exits **0**; `evidence/entrypoint.json`, `logs/entrypoint.log`.
- Original review51 probe: still exits **0**; captured at `logs/review51_probe_repair2.json`.
- Closure probe: the unchanged probe stops at cold `S51Session.open(root/"rehash")` with a typed `SessionRefusal`/`S37_VERIFY_FAILED` containing `S51_RELEVANCE_INVALID:S51_RELEVANCE_READSET_MISSING` and `S51_HYPOTHESIS_CONSUMED_EVENT_MISMATCH`; it no longer reaches a false `verify_ok`. Captured at `logs/review52_closure_probe_after.json`.
- Focused edge checks through the actual APIs: unrelated next event -> `EXPIRED` then `HYPOTHESIS_EXPIRED`; withdrawn/expired/fresh -> `HYPOTHESIS_WITHDRAWN`/`HYPOTHESIS_EXPIRED`/`FACILITATES`; forged self-consistent relevance with a copied evaluation checkpoint -> `S51_INPUT_REFUSED` and `verify()["ok"] is False`; intact cold replay -> true and same relevance hash.
- Source manifest: `evidence/source_manifest.json`, including S39 model, S49 actor/session seams and accepted S49 base `6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43`.

## Remaining scope

The full actor-relevance-to-behavior function remains **NOT_DONE** for the separately reported missing paid-offer action relation: `NO_EXISTING_S49_OPTION_EXPRESSES_PAID_FINISHING_EQUIPMENT_OFFER`. The canonical result remains an `OPEN_CHOICE_SET` with qualified source content and no option-specific reason, selected option, performer, or C8 action. The actual G18 object is finite sourcefree research input; current actual purpose and native object formation remain unproved. No native rule, durable purpose, preference, Pyat, human authority, or CAN010/CAN011 update was added. Untracked S50 runtime data was not touched or committed.

**Terminal:** `S51_SITUATED_OBJECT_RELEVANCE__NEXT_RECEIVED_EVENT__DISTINCT_LIFECYCLE_HOLDS__RECOMPUTED_CANONICAL_RELEVANCE__S49_QUALIFIED_OPEN__FULL_BEHAVIOR_NOT_DONE__NATIVE_RULE_NEEDED`.
