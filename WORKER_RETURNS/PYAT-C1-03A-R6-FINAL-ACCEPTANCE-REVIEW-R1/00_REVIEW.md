# PYAT C1-03A — R6 FINAL ACCEPTANCE REVIEW — R1

Disposition: `APPROVE_AT_DECLARED_GRAIN`

Review branch: `agent/reviewer-pyat-hq161-c1-03a-r6-final-acceptance-r1`
Commission tip: `bcc0e7616e8c13442efef69b63719fd41b47f191`
Reviewed implementation return: `4f5555459e5ffdb240fc9e6e94178ec5e4b3eff1`
Prior final rereview: `bd16efae659fe3c44f700d756a2016f1dd6b246c` — `CHANGES_REQUIRED`
Prior blocker: `C1-03A-R5-FINAL-REVIEW-BLOCK-REFUSAL-CLASS-001`

## Final result

No blocking counterexample remains at the declared C1-03A source-free grain.

R6 closes the sole R5 blocker exactly, without widening the captured meaning or disturbing the previously accepted C1-03A terrain.

## 1. Prior blocker independently reproduced from R5 source

R5 executed:

```python
binding = semantic_hash(kwargs)
try:
    RespondentEvent(**kwargs)
except Pre553IntegrityError as exc:
    if type(exc).__name__ == "Pre553AuthorityError":
        ...
    return OwnerRefusalWitness(...)
```

`Pre553SemanticCollapseError` is a canonical subclass of `Pre553IntegrityError`.

The stateful nested-`Mapping` hostile is source-valid against the governed AT14 fixture:

1. caller-controlled nested semantic material is included in `kwargs`;
2. `semantic_hash(kwargs)` canonicalizes it before the constructor `try`;
3. the same nested material is canonicalized again inside the real `RespondentEvent(**kwargs)` call;
4. a stateful mapping can behave normally during the binding pass and raise `Pre553SemanticCollapseError` during the constructor pass;
5. R5's family catch catches that subclass;
6. the R5 name check excludes only `Pre553AuthorityError`;
7. therefore R5 could mint `EMPIRICAL_INTEGRITY_REFUSAL` carrying `refusal_type=Pre553SemanticCollapseError`, which projected to retained `INTEGRITY_FAILURE`.

That is the exact prior blocker.

## 2. R6 exact refusal-class correction — PASS

R6 now executes:

```python
except Pre553IntegrityError as exc:
    if type(exc) is not Pre553IntegrityError:
        raise OwnerProjectionError(...) from exc
```

This closes the prior path exactly:

- witness minting occurs only for exact runtime type `Pre553IntegrityError`;
- every subclass is refused;
- `Pre553SemanticCollapseError` cannot mint a witness;
- `Pre553AuthorityError`, itself a subclass, cannot mint a witness;
- the refused subclass is preserved as `__cause__` through `raise ... from exc`;
- no new retained semantic state is introduced;
- the ordinary stale-sealed-identity path still raises the base `Pre553IntegrityError` and still lawfully projects to `INTEGRITY_FAILURE`.

The R6 official-subclass hostile is substantive, not a hand-supplied-exception court. Its `_R6StatefulMapping` is inserted into the real governed fixture's attempted body, survives the pre-try binding canonicalization, and raises `Pre553SemanticCollapseError` only when the real `RespondentEvent(**body)` constructor re-canonicalizes the value. The court verifies the resulting `OwnerProjectionError.__cause__` is the original `Pre553SemanticCollapseError`.

A second court verifies the stateful mapping accumulated accesses before the refusal, establishing traversal through the pre-try binding pass and then the constructor path.

## 3. R5 provenance/authenticity closure — preserved

R6 changes only the refusal-class handling inside the already accepted capture. The R5 provenance boundary remains intact:

- exact `C11Repository` type gate;
- exact release resolution through that repository;
- exact `C11LogicalRelease` type gate;
- exactly one public object at the requested ref within that release;
- exact `RespondentEvent` type identity, not `isinstance`;
- exact family `RespondentEvent@1.0.0`;
- other genuine canonical families rejected;
- caller-defined `CanonicalSemanticObject` subclasses cannot substitute as the governed object;
- caller-defined `RespondentEvent` subclasses cannot substitute as the governed object;
- absent object / foreign or unresolvable release remains typed fail-closed;
- truthful owner remains `rawlsing_next.pre553_empirical_objects.RespondentEvent (canonical integrity construction)`;
- witness still binds exact governing release ref, resolved event ref, object family, attempted-body invocation hash, and owner-derived authority/dependency/replay closure;
- owner acceptance of an untampered body still yields no witness;
- bare exception minting remains closed.

The AT14 fixture blob is byte-identical from the R6 commission tip to the R6 return.

## 4. Previously accepted A terrain — preserved

No concrete R6 regression was found in:

- G5 receipt dominance;
- exact owner gates elsewhere;
- adaptive determinant provenance;
- adaptive `UNVISITED`;
- recursive owner-derived custody;
- no invented completeness;
- eight mandatory negative states remaining distinct;
- AT15 genuine learned/adjudicated `ADMITTED` route;
- failed / `DENY` laundering remaining closed;
- AT16 54 support / 6 oppose over denominator 60 remaining `SUPPORTED`;
- producer -> accepted C1 composition -> named consumer;
- discovery refusal authenticity and its distinct `BLOCKED_REQUIRED_AUTHORITY` state;
- final-SHA refusal-factory classmethod cleanup;
- C1-02 untouched.

The following accepted source blocks are byte/source-identical from R6 commission tip to R6 return:

- `RouteObligation`;
- `capture_required_authority_refusal`;
- `assert_route_not_laundered`;
- `require_positive_route`;
- `build_state_route_result`.

The reported unchanged fixture/owner surfaces were independently blob-checked and are identical:

- `c1_at14_at16_fixture.py`;
- `pre553_c11_repository.py`;
- `pre553_c11_integrity.py`;
- `pre553_empirical_objects.py`;
- `pre553_empirical_query.py`;
- `pre553_discovery_exact.py`;
- `pre553_structural_admission.py`;
- `pre553_analytical_composition.py`;
- `source_backed_positioned_subject_possibility.py`.

## 5. Execution provenance / false-green defense

The committed final execution receipt names the correct ten `pre553` test files. It contains no `pre753` typo.

Recorded final court:

- `test_pre553_analytical_state_and_route.py`: 92
- `test_pre553_analytical_composition_higher_order.py`: 35
- `test_pre553_empirical_query.py`: 32
- `test_pre553_structural_admission.py`: 17
- `test_pre553_discovery_exact.py`: 14
- `test_pre553_analytical_composition.py`: 13
- `test_source_backed_positioned_subject_possibility.py`: 13
- `test_pre553_discovery_adaptive.py`: 8
- `test_pre553_discovery_adaptive_admission.py`: 3
- `test_pre553_recursive_handoff.py`: 2

Total: **229 passed, 0 failed, 0 errors, 0 skipped**.

Static final-tree reconciliation independently matches 229:

- state/route has 92 direct test functions;
- higher-order composition 35;
- empirical query 30 direct functions plus one 3-case parametrized court = 32;
- structural admission 13 direct functions plus one 5-case parametrized court = 17;
- discovery exact 14;
- analytical composition 12 direct functions plus one 2-case parametrized court = 13;
- positioned-subject possibility 13;
- adaptive discovery 8;
- adaptive admission 3;
- recursive handoff 2.

R6 adds exactly six `test_r6_*` courts. The R6 test-file diff is 171 additions / 0 deletions, so no prior court was removed in this correction.

The final worker branch head is exactly `4f5555459e5ffdb240fc9e6e94178ec5e4b3eff1`; there is no later branch delta.

Browser/GitHub cannot itself rerun the local pytest command or inspect the worker's local `git status`. The committed JSON receipt does not encode separate `tested_commit` or `clean_tree` fields. Accordingly, those local-runtime details are not independently re-measured here. This does **not** create a semantic blocker: the exact final committed source, final court inventory, correct command, branch head, additive six-court delta, and recorded 229-pass evidence are all reconciled, and the refusal-class closure is independently established from final source.

No zero-test or no-tests-collected command is used as final evidence.

## 6. Diff / terrain — PASS

From exact R6 commission tip:

`310dadf0a6057cd6a473e8562532410e40945119`

to exact R6 return:

`4f5555459e5ffdb240fc9e6e94178ec5e4b3eff1`

the return is exactly **one commit ahead**.

The diff is confined to:

- `rawlsing_next/pre553_analytical_state_and_route.py` — 10 additions, 2 deletions;
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py` — additive R6 courts;
- `WORKER_RETURNS/PYAT-C1-03A-EXACT-REFUSAL-CLASS-R6/**`.

No out-of-terrain implementation file changed. C1-02 is untouched.

## Final disposition

The R5 refusal-class laundering counterexample is closed exactly. No new concrete blocker affects the declared C1-03A grain. All previously accepted A behavior remains preserved.

**Disposition:** `APPROVE_AT_DECLARED_GRAIN`

This review is terminal for the declared C1-03A acceptance grain and does not require another rereview layer.

**Terminal:** `C1_03A_R6_FINAL_ACCEPTANCE_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`
