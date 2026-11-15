# VOZHD PYAT — HQ234 F7 CLOSURE-CELL HOSTILE LEAD — R1

**DECISION:** `HQD-2026-10-07-234`  
**DATE:** 2026-10-07  
**STATUS:** RATIFIED SUPPLEMENTAL REVIEW INPUT — NOT YET A DEFECT ADOPTION

## Origin

A superseded browser reviewer launched from the earlier F7 rereview commission tip:

`4ff9974fc64f11d45095270cd6afefa160e87fb6`

correctly observed that the branch had subsequently been reassigned to DeepSeek-Harness/OpenCode at:

`b030d870abdacf20d689d17ef6828d4e26dfedd6`

and therefore did **not** push a return onto the reassigned reviewer branch.

That non-push was correct.

## Supplemental hostile lead

Proposed blocker:

`F7-RR-04G__LEXICAL_CUSTODY_LEDGER_CELL_IS_CALLER_REBINDABLE`

The HQ231 candidate stores authenticated owner custody in the nonlocal closure binding:

`entries: tuple[tuple[Any, _AuthenticatedResolverState], ...] = ()`

inside `_make_sealed_source_relation_owner`.

The current HQ231 hostile court already recovers:
- `authenticated_source_relation_decision.__closure__`;
- callable `_state_or_refuse`;
- `source_state = loader(source)`;
- `victim_state = loader(victim)`;
- the lexical `entries` tuple through `loader.__closure__`.

But the court only proves that the **tuple object** does not support item assignment:

`ledger[0] = ledger[-1]` -> `TypeError`.

The proposed hostile lead attacks the **closure cell binding**, not tuple mutability.

Python's callable data model exposes closure cells through `function.__closure__`; cell `cell_contents` is gettable and settable in the relevant CPython family.

## Exact reproduction target

The active DeepSeek hostile reviewer must attempt an attack of this shape against the exact current candidate and governed hostile model:

1. construct source resolver A with a genuine positive authorized relation;
2. construct victim resolver B without that relation, using the same registry where the existing HQ231 fixture does so;
3. recover `_state_or_refuse` through `authenticated_source_relation_decision.__closure__`;
4. recover the exact closure cell in `loader.__closure__` whose `cell_contents` is the lexical `entries` tuple;
5. obtain `source_state` and `victim_state`;
6. construct a state carrying source custody material but bound to `victim_state.owner_ref`;
7. rebind `entries_cell.cell_contents` to a tuple in which victim maps to that forged state;
8. invoke the normal authenticated F7 path for victim.

Dispositive question:

> Does victim become positive using source's legitimate relation/snapshot/hash/custody material after the caller rebinds the lexical ledger cell?

If yes:
- return `F7_SEALED_CUSTODY_PARTIAL__NAMED_DEFECT`;
- name blocker `F7-RR-04G__LEXICAL_CUSTODY_LEDGER_CELL_IS_CALLER_REBINDABLE`;
- classify it as a bounded provenance/custody implementation defect unless reproduction exposes something broader;
- do not repair in the review lane.

If no:
- commit the exact attack and the exact reason it fails;
- identify the load-bearing invariant that defeats cell rebinding.

## Why existing fail-capability is insufficient

The current fail-capability replaces the F7 authenticated entrypoint with a deliberately transplantable path. That proves dependency on the authenticated entrypoint. It does not prove that the **actual lexical custody cell used by that entrypoint** is protected from a reflection primitive already admitted by the HQ231 hostile court.

## Current HQ posture

This lead is strong enough that F7 adoption remains prohibited pending the active DeepSeek review.

It is **not** independently adopted as a proved defect until the active local reviewer reproduces or falsifies it against the exact commissioned candidate.

The parallel F7 runtime qualification remains useful and should continue. A green execution of the existing court cannot by itself close this lead because the existing court does not exercise `cell.cell_contents` rebinding.

## Branch ownership

Do not ask the superseded browser reviewer to push.

Do not move or rewrite the active DeepSeek review branch merely to store this lead.

The authoritative active reviewer remains:

`agent/reviewer-pyat-hq232-f7-sealed-owner-state-final-rereview-r1 @ b030d870abdacf20d689d17ef6828d4e26dfedd6`

This document is HQ-supplied supplemental evidence for that reviewer.

Terminal:

`PYAT_HQ234_F7_CLOSURE_CELL_HOSTILE_LEAD_BANKED__ACTIVE_DEEPSEEK_REVIEW_MUST_REPRODUCE_OR_FALSIFY__NO_BRANCH_OWNERSHIP_COLLISION`
