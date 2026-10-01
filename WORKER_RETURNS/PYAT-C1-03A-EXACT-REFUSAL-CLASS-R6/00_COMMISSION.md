# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C1-03A — EXACT REFUSAL-CLASS CORRECTION — R6
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq160-c1-03a-exact-refusal-class-r6`

Exact base:
`7a316e4deb655a64853eccdfd719efcd83f140e4`

Final rereview:
`agent/reviewer-pyat-hq159-c1-03a-r5-final-rereview-r1 @ bd16efae659fe3c44f700d756a2016f1dd6b246c`

Disposition:
`CHANGES_REQUIRED`

Sole blocker:
`C1-03A-R5-FINAL-REVIEW-BLOCK-REFUSAL-CLASS-001`

Do not reopen any other C1-03A behavior.

## Problem

`capture_empirical_integrity_refusal` currently catches:

`except Pre553IntegrityError as exc:`

and then witnesses the refusal unless it is `Pre553AuthorityError`.

That is too broad. `Pre553SemanticCollapseError` is a canonical subclass of `Pre553IntegrityError`, and the reviewer proved a real constructor-path hostile where a caller-controlled nested Mapping behaves normally during the pre-try binding canonicalization and raises `Pre553SemanticCollapseError` only during the actual `RespondentEvent(**kwargs)` canonicalization.

R5 then wrongly certifies that distinct subclass meaning as:
`EMPIRICAL_INTEGRITY_REFUSAL -> INTEGRITY_FAILURE`.

## Required correction

At this exact AT14 boundary, witness only an exception whose exact runtime type is:

`Pre553IntegrityError`

No subclass may mint this refusal witness.

The narrow expected shape is:

```python
except Pre553IntegrityError as exc:
    if type(exc) is not Pre553IntegrityError:
        raise OwnerProjectionError(...) from exc
    ...
```

Equivalent finite exact-class logic is acceptable.

Do not:
- widen the captured meaning;
- create a new semantic state;
- alter the truthful RespondentEvent owner label;
- alter release/object/family provenance;
- alter discovery refusal handling;
- alter G5/AT15/AT16.

## Mandatory hostile

Add an official-subclass hostile that reaches `Pre553SemanticCollapseError` during the actual `RespondentEvent` constructor call—not a manually supplied exception—and proves:

- no `OwnerRefusalWitness` is minted;
- no `INTEGRITY_FAILURE` projection can result;
- the subclass is converted to typed fail-closed `OwnerProjectionError` (or equivalent existing projection-layer refusal).

Use the reviewer's stateful nested-`Mapping` pattern or an equally strong construction.

Also retain/directly prove:
1. normal stale sealed identity raises exact base `Pre553IntegrityError` and still mints the lawful refusal witness;
2. truthful owner label remains the canonical RespondentEvent integrity construction;
3. exact governed release/object/family gates remain unchanged;
4. bare exception minting remains closed;
5. discovery refusal remains authentic and byte-unchanged;
6. G5 remains closed;
7. AT15 remains green;
8. AT16 54/6 remains SUPPORTED;
9. producer → C1 composition → named consumer remains green;
10. C1-02 untouched.

## Write terrain

Modify only:
- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`
- `WORKER_RETURNS/PYAT-C1-03A-EXACT-REFUSAL-CLASS-R6/**`

Do not modify the AT14 fixture unless strictly necessary. Prefer proving against the existing governed fixture.

Do not modify C11, empirical objects, empirical query, discovery, structural admission, composition, consumer, or authority owner modules.

## Court

Run the same ten-file C1-03A court.

R5 baseline:
`223 passed, 0 failed, 0 errors, 0 skipped`.

Record exact final counts and runtime on the final commit.

## Return

Write:
`WORKER_RETURNS/PYAT-C1-03A-EXACT-REFUSAL-CLASS-R6/**`

Required:
- `00_RETURN.md`
- `01_BLOCKER_DISPOSITION.json`
- `02_EXACT_REFUSAL_CLASS_RECEIPT.json`
- `03_EXECUTION_RECEIPT.json`
- `04_FINAL_DISPOSITION.json`

Allowed:
- `PASS_C1_03A_EXACT_REFUSAL_CLASS_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`
- `UNEXPECTED_BROADER_DEFECT__HQ_ADJUDICATION_REQUIRED`
- `ARCHITECTURE_WARRANT`

No merge/self-adoption. No C1-03 join. No C1-R. No raw sources. No V3.

Terminal:
`C1_03A_EXACT_REFUSAL_CLASS_RETURNED__HQ_ADJUDICATION_REQUIRED`
