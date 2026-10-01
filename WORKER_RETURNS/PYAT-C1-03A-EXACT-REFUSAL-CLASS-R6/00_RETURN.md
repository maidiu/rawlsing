# PYAT C1-03A — EXACT REFUSAL-CLASS CORRECTION — R6

Status: `PASS_C1_03A_EXACT_REFUSAL_CLASS_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`

Branch: `agent/opencode-pyat-hq160-c1-03a-exact-refusal-class-r6`
Commission tip: `310dadf0a6057cd6a473e8562532410e40945119`
Base: `7a316e4deb655a64853eccdfd719efcd83f140e4`
Rereview: `agent/reviewer-pyat-hq159-c1-03a-r5-final-rereview-r1 @ bd16efae` — `CHANGES_REQUIRED`

Sole blocker: `C1-03A-R5-FINAL-REVIEW-BLOCK-REFUSAL-CLASS-001`

## Court

| Suite | Tests |
|---|---|
| `test_pre553_analytical_state_and_route.py` | 92 |
| `test_pre553_analytical_composition_higher_order.py` | 35 |
| `test_pre553_empirical_query.py` | 32 |
| `test_pre553_structural_admission.py` | 17 |
| `test_pre553_discovery_exact.py` | 14 |
| `test_pre553_analytical_composition.py` | 13 |
| `test_source_backed_positioned_subject_possibility.py` | 13 |
| `test_pre553_discovery_adaptive.py` | 8 |
| `test_pre553_discovery_adaptive_admission.py` | 3 |
| `test_pre553_recursive_handoff.py` | 2 |
| **total** | **229 passed, 0 failed, 0 errors, 0 skipped** |

Runtime 19.43 s, exit 0. R5 baseline 223; +6 new R6 courts, none removed or weakened.
**Only these ten files were executed — no broader sweep claimed.**

## The defect, reproduced first

R5 caught `Pre553IntegrityError` with a broad `except` and excluded only
`Pre553AuthorityError`. Since `Pre553SemanticCollapseError` is a canonical subclass, a
forbidden cross-ontology substitution was being certified as
`EMPIRICAL_INTEGRITY_REFUSAL -> INTEGRITY_FAILURE` — a distinct owner meaning
collapsed into a mandatory state.

I built the reviewer's stateful nested-`Mapping` and measured the split precisely:

```
accesses during the pre-try invocation-binding hash : 2
accesses inside the real RespondentEvent(**body)   : 2  -> subclass raised here

witness refusal_type : Pre553SemanticCollapseError
witness refusal_kind : EMPIRICAL_INTEGRITY_REFUSAL
projected state      : INTEGRITY_FAILURE
```

The mapping behaves normally while the capture canonicalizes the attempted body, then
raises only inside the real constructor call. So the subclass genuinely arises through
the owner path — not from a hand-supplied exception.

## The correction

```python
except Pre553IntegrityError as exc:
    if type(exc) is not Pre553IntegrityError:
        raise OwnerProjectionError(...) from exc
```

The captured set is exactly **one** class. The meaning was not widened, no new semantic
state was created, and the subclass is preserved as `__cause__` so the original refusal
cause is never lost.

A side effect worth naming: `Pre553AuthorityError` is still refused here, but now by
the exact-type rule rather than a class-name comparison — strictly stronger, since the
name check could have been satisfied by any exception merely *named* that.

The whole correction is **10 insertions, 2 deletions in one source file**.

## Mandatory hostile

The official-subclass hostile proves, against the existing governed fixture:

- no `OwnerRefusalWitness` is minted;
- no `INTEGRITY_FAILURE` projection can result;
- the subclass becomes a typed fail-closed `OwnerProjectionError` citing the blocker id;
- the subclass truly arrives via the constructor — a separate court proves the binding
  hash consumed successful accesses *before* the hostile began raising, which is only
  possible inside the `try`.

## Retained proofs

All ten hold: base-class stale identity still mints the lawful witness; the truthful
`RespondentEvent` owner label is unchanged; release/object/family gates unchanged; bare
exception minting closed; discovery refusal authentic and byte-unchanged; G5 closed;
AT15 green; AT16 54/6 `SUPPORTED`; producer → composition → consumer green; C1-02
untouched. A targeted preserve selection (`hq_e or hq_f or hq_g or at15 or at16 or
factory`) ran **26 passed**.

The AT14 fixture was **not** modified — the proof runs against the existing governed
fixture, as instructed. All nine owner modules verified byte-unchanged.

## Changed files

- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`
- `WORKER_RETURNS/PYAT-C1-03A-EXACT-REFUSAL-CLASS-R6/**`

## Non-claims

No raw sources. No C1-03 join. No C1-R. No V3. Not merged, not self-adopted.

## Terminal

`C1_03A_EXACT_REFUSAL_CLASS_RETURNED__HQ_ADJUDICATION_REQUIRED`
