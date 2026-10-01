# PYAT C1-03A — R5 EMPIRICAL OWNER-BINDING FINAL INDEPENDENT REREVIEW — R1

Disposition: `CHANGES_REQUIRED`

Review branch: `agent/reviewer-pyat-hq159-c1-03a-r5-final-rereview-r1`
Commission tip: `b809236c894fb8fbcd4ecb60354e8dcc6bec9ae0`
Reviewed implementation return: `7a316e4deb655a64853eccdfd719efcd83f140e4`
Prior final rereview: `599833bb77d29abd21cf08ab0500491bef7ea49c` — `CHANGES_REQUIRED`

## Result

R5 closes the R4 owner-family / false-attribution defect, but it does **not** close the final refusal-class requirement.

The corrected capture now genuinely resolves the exact governed `RespondentEvent@1.0.0` from an exact `C11LogicalRelease`, rejects cross-family and subclass object substitution, invokes `RespondentEvent(**kwargs)`, and truthfully labels that constructor/integrity path rather than `execute_empirical_query`.

The remaining blocker is narrower:

`capture_empirical_integrity_refusal` catches the entire `Pre553IntegrityError` subclass family:

```python
try:
    RespondentEvent(**kwargs)
except Pre553IntegrityError as exc:
    if type(exc).__name__ == "Pre553AuthorityError":
        ...
    return OwnerRefusalWitness(...)
```

That does not mean "exactly `Pre553IntegrityError`". It admits at least the canonical subclass `Pre553SemanticCollapseError`.

## Decisive refusal-class counterexample

The normal stale-sealed-identity fixture is sound in isolation:

- changing `raw_response_value` changes the semantic digest;
- the retained stale `object_id` is rejected by `CanonicalSemanticObject.__init__`;
- that rejection is an exact base `Pre553IntegrityError`;
- exact `RespondentEvent` has no normal family-specific path to `Pre553SemanticCollapseError`;
- `RespondentEvent@1.0.0` is a declared public family.

But that is not enough at this trust boundary, because `tampered_semantic_fields` is caller-controlled `Mapping[str, Any]`, and canonicalization executes methods on nested caller-provided `Mapping` values.

The capture first computes:

```python
binding = semantic_hash(kwargs)
```

outside the constructor `try`, and then `RespondentEvent(**kwargs)` canonicalizes the same nested values again inside the caught region.

A minimal caller-controlled mapping can therefore behave normally during the binding pass and raise the canonical `Pre553SemanticCollapseError` on the constructor pass:

```python
class SecondReadSemanticCollapse(Mapping):
    def __init__(self):
        self.iterations = 0

    def __iter__(self):
        self.iterations += 1
        # canonicalize(Mapping) iterates twice on the first binding pass:
        # once for key validation, once for sorted(value).
        if self.iterations >= 3:
            raise Pre553SemanticCollapseError("distinct semantic-collapse meaning")
        return iter(("k",))

    def __len__(self):
        return 1

    def __getitem__(self, key):
        return "v"

capture_empirical_integrity_refusal(
    repository=governed_repository,
    release_ref=governed_release_ref,
    respondent_event_ref=governed_respondent_event_ref,
    tampered_semantic_fields={
        "raw_response_value": SecondReadSemanticCollapse(),
    },
)
```

Source consequence:

1. the first `semantic_hash(kwargs)` pass succeeds;
2. the real `RespondentEvent` constructor begins;
3. constructor canonicalization re-enters the caller mapping;
4. the mapping raises the canonical `Pre553SemanticCollapseError`;
5. `except Pre553IntegrityError` catches it;
6. the exact-name exclusion only rejects `Pre553AuthorityError`, so semantic collapse is accepted;
7. the witness records `refusal_type="Pre553SemanticCollapseError"`;
8. `from_empirical_integrity_refusal` projects that witness to retained `INTEGRITY_FAILURE`.

That is exactly the laundering the commission required this rereview to attack: a distinct `Pre553IntegrityError` subclass meaning can be certified as the AT14 empirical integrity refusal.

Blocker:

`C1-03A-R5-FINAL-REVIEW-BLOCK-REFUSAL-CLASS-001`

## Minimal correction required

At the declared commission grain, fail closed unless the caught exception is **exactly** the base class:

```python
if type(exc) is not Pre553IntegrityError:
    raise OwnerProjectionError(...) from exc
```

Equivalent ordered subclass refusal is acceptable if it proves the same finite boundary.

Add a hostile using an official subclass such as `Pre553SemanticCollapseError` reached during the constructor call, not merely a manually supplied exception. Do not claim that normal `RespondentEvent` validation cannot raise the subclass as sufficient proof: caller-controlled nested semantic values are executable Python objects at this boundary.

## Exact governed provenance — PASS except refusal class

Verified at R5:

- exact `C11Repository` type gate;
- exact release resolution through that repository;
- exact `C11LogicalRelease` type gate;
- exactly one public object at the requested exact ref in that release;
- exact `RespondentEvent` type identity;
- exact declared family `RespondentEvent@1.0.0`;
- another genuine canonical family rejected;
- caller-defined `CanonicalSemanticObject` subclass cannot be supplied as the governed object;
- caller-defined `RespondentEvent` subclass cannot be supplied as the governed object;
- event absent from release rejected;
- foreign/unresolvable release converted to typed fail-closed `OwnerProjectionError`;
- no caller parameter for object instance, owner label, producer ref, supporting refs, reason, or witness family;
- witness binds governing release ref, resolved event ref, family, invocation binding, and owner-derived authority/dependency/replay closure.

## Truthful owner attribution — PASS

The witness owner is now:

`rawlsing_next.pre553_empirical_objects.RespondentEvent (canonical integrity construction)`

That is the operation actually invoked. The fixture uses the same identity. The empirical-query relabelling from R4 is gone. No generic any-`CanonicalSemanticObject` owner was introduced.

## Owner acceptance / state distinction — PASS

- Untampered governed body is accepted by the constructor and produces no witness.
- A manually constructed bare exception cannot mint a trusted projection.
- The discovery refusal capture is byte-identical across the R4-final base and R5 and still truthfully invokes/labels `execute_exact_bounded_discovery`.
- `INTEGRITY_FAILURE` and `BLOCKED_REQUIRED_AUTHORITY` remain distinct in owner, refusal kind, and retained state.

## Accepted A work — preserved

No concrete R5 regression found in the accepted terrain:

- G5 receipt dominance;
- exact owner gates elsewhere;
- adaptive determinant provenance;
- adaptive UNVISITED;
- recursive owner-derived custody;
- no invented completeness;
- eight mandatory negative states distinct;
- AT15 genuine learned/adjudicated `ADMITTED` route;
- failed/DENY route laundering remains closed;
- AT16 54 support / 6 oppose over denominator 60 remains `SUPPORTED`;
- producer -> accepted C1 composition -> named consumer remains exercised;
- final-SHA classmethod cleanup remains intact;
- C1-02 is untouched.

`RouteObligation`, `assert_route_not_laundered`, `require_positive_route`, `build_state_route_result`, and `capture_required_authority_refusal` are source-identical from the accepted R4-final base to R5.

## Court / provenance

The R5 diff is confined to:

- `rawlsing_next/pre553_analytical_state_and_route.py`;
- `rawlsing_next/tests/c1_at14_at16_fixture.py`;
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`;
- `WORKER_RETURNS/PYAT-C1-03A-EMPIRICAL-OWNER-BINDING-R5/**`.

The seven reported owner modules are blob-identical from `b46fcf2b951d3ecbc7d17be45a36b37ff7c2f494` to `7a316e4deb655a64853eccdfd719efcd83f140e4`.

The recorded ten-file court is internally and statically reconciled:

- state/route: 86 direct tests;
- higher-order composition: 35;
- empirical query: 30 direct functions with one 3-case parametrized test -> 32 collected;
- structural admission: 13 direct functions with one 5-case parametrized test -> 17 collected;
- discovery exact: 14;
- analytical composition: 12 direct functions with one 2-case parametrized test -> 13 collected;
- positioned-subject possibility: 13;
- adaptive discovery: 8;
- adaptive admission: 3;
- recursive handoff: 2.

Total: **223 passed, 0 failed, 0 errors, 0 skipped** in the worker receipt.

No fresh runtime was executed in this Browser/GitHub documentary rereview. The blocker is exact committed-source proof and does not depend on runtime timing or environment.

## Scope

No implementation mutation.
No merge or self-adoption.
No C1-03 join.
No raw source access.

## Final

R5 successfully repairs exact governed `RespondentEvent` provenance and truthful owner attribution. G5, AT15, AT16, discovery-refusal authenticity, and the 223-court provenance remain preserved.

The final C1-03A refusal-authenticity gate is still open because the superclass catch can certify `Pre553SemanticCollapseError` as the same AT14 `INTEGRITY_FAILURE`.

**Disposition:** `CHANGES_REQUIRED`

**Terminal:** `C1_03A_R5_FINAL_INDEPENDENT_REREVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`
