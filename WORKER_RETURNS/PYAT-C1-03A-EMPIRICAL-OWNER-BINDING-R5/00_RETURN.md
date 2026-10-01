# PYAT C1-03A — EMPIRICAL REFUSAL OWNER-BINDING CORRECTION — R5

Status: `PASS_C1_03A_EMPIRICAL_OWNER_BINDING_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`

Branch: `agent/opencode-pyat-hq158-c1-03a-empirical-owner-binding-r5`
Commission tip: `25c76a6829217919462d8581c8ed19300bbb24db`
Base: `b46fcf2b951d3ecbc7d17be45a36b37ff7c2f494`
Rereview: `agent/reviewer-pyat-hq157-c1-03a-r4-final-rereview-r1 @ 599833bb` — `CHANGES_REQUIRED`

Sole blocker: `C1-03A-R4-FINAL-REVIEW-BLOCK-EMPIRICAL-CAPTURE-OWNER-FAMILY-001`

## Court

| Suite | Tests |
|---|---|
| `test_pre553_analytical_state_and_route.py` | 86 |
| `test_pre553_analytical_composition_higher_order.py` | 35 |
| `test_pre553_empirical_query.py` | 32 |
| `test_pre553_structural_admission.py` | 17 |
| `test_pre553_discovery_exact.py` | 14 |
| `test_pre553_analytical_composition.py` | 13 |
| `test_source_backed_positioned_subject_possibility.py` | 13 |
| `test_pre553_discovery_adaptive.py` | 8 |
| `test_pre553_discovery_adaptive_admission.py` | 3 |
| `test_pre553_recursive_handoff.py` | 2 |
| **total** | **223 passed, 0 failed, 0 errors, 0 skipped** |

Runtime 18.26 s, exit 0. Prior baseline 212; +11 new R5 courts, 3 R4 courts corrected
(they asserted the false label), none deleted or weakened. **Only these ten files were
executed — no broader sweep claimed.**

## The reviewer caught a false statement in my own R4 work

R4's witness claimed the INTEGRITY_FAILURE owner was
`pre553_empirical_query.execute_empirical_query`. **That function was never invoked.**
The refusal came from the canonical `RespondentEvent` construction/integrity path. My
envelope therefore attested that a competent owner had refused, naming an owner that
had not run. R4's authenticity work fixed *fabrication* while leaving a *misattribution*
standing — and I reported it as established.

The governing law is the one HQ cited: a mandatory negative state need not occur on the
empirical-query path, and where it cannot occur there, the competent path where it
genuinely occurs must be exercised. For this fixture that path is the canonical
integrity rejection of an exact `RespondentEvent` body retaining a stale sealed
identity.

## What changed

The capture now takes **governed identity, not an object instance**:

```
capture_empirical_integrity_refusal(
    repository, release_ref, respondent_event_ref, tampered_semantic_fields
)
```

`original_object` is gone. Gates, in order:

1. `type(repository) is C11Repository`
2. the exact `C11LogicalRelease` resolves through the repository — an unresolvable
   release **fails closed with a typed refusal**
3. exactly one public object at `respondent_event_ref` **within that release**
4. `type(resolved) is RespondentEvent` — exact type identity, **not** `isinstance`
5. `resolved.FAMILY == "RespondentEvent@1.0.0"` matches the declared AT14 grain
6. the real canonical `RespondentEvent(**attempted_body)` is invoked
7. exactly `Pre553IntegrityError` is captured; `Pre553AuthorityError` is refused
8. constructor acceptance ⇒ no witness

The broad `CanonicalSemanticObject` `isinstance` gate is gone, so another canonical
family, a caller-defined `CanonicalSemanticObject` subclass, and a caller-defined
`RespondentEvent` subclass are all refused — a court proves each subclass *would* have
satisfied a broad gate, so the refusals cannot be credited to an accidental mismatch.

The truthful label is now:

```
rawlsing_next.pre553_empirical_objects.RespondentEvent (canonical integrity construction)
```

The witness binds the exact release ref, the exact resolved `RespondentEvent.ref`, the
object family, the attempted-body invocation binding, and the object's real
authority/dependency/replay closure.

**Bounded as instructed:** no generic "any `CanonicalSemanticObject` integrity"
authority was created. This stays on the declared AT14 `RespondentEvent` path only.

## Hostiles

All seventeen required hostiles proven, including all four preserve items: G5 remains
closed, AT15's genuine `ADMITTED` route stays green, AT16 54/6 stays `SUPPORTED`, and
producer → C1 composition → named consumer stays green. The discovery refusal path is
byte-unchanged and its own hostile confirms it still binds
`execute_exact_bounded_discovery` truthfully.

## One robustness gap my own hostile found

Writing hostile 2 exposed that an unresolvable release leaked a raw
`KeyError("exact C11 release unavailable")` out of the capture instead of a typed
refusal. A caller substituting a foreign release ref would have seen an internal
exception type rather than a governed refusal. Now converted to a typed
`OwnerProjectionError`, and covered by a hostile.

## Changed files

- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/c1_at14_at16_fixture.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`
- `WORKER_RETURNS/PYAT-C1-03A-EMPIRICAL-OWNER-BINDING-R5/**`

`pre553_c11_repository.py`, `pre553_c11_integrity.py`, `pre553_empirical_objects.py`,
`pre553_empirical_query.py`, `pre553_discovery_exact.py`,
`pre553_analytical_composition.py` and `source_backed_positioned_subject_possibility.py`
all verified byte-unchanged.

## Non-claims

No raw sources. No C1-03 join. Not merged, not self-adopted.

## Terminal

`C1_03A_EMPIRICAL_OWNER_BINDING_RETURNED__HQ_ADJUDICATION_REQUIRED`
