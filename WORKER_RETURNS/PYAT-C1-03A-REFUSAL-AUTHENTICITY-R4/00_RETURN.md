# PYAT C1-03A — REFUSAL-AUTHENTICITY CORRECTION — R4

Status: `PASS_C1_03A_REFUSAL_AUTHENTICITY_CORRECTED__INDEPENDENT_REREVIEW_REQUIRED`

Branch: `agent/opencode-pyat-hq155-c1-03a-refusal-authenticity-r4`
Commission tip: `0b03f1d44d25a4476779f3afa7dd0412cfc4debc`
Base: `767bb9139b80e774093af8e765e57ee57a19e005`
Rereview: `agent/reviewer-pyat-hq154-c1-03a-r3-rereview-r1 @ 3ebde6d2` — `CHANGES_REQUIRED`

Blocker: `C1-03A-R3-REVIEW-BLOCK-REFUSAL-AUTHENTICITY-001`

## Court

| Suite | Tests |
|---|---|
| `test_pre553_analytical_state_and_route.py` | 71 |
| `test_pre553_analytical_composition_higher_order.py` | 35 |
| `test_pre553_empirical_query.py` | 32 |
| `test_pre553_structural_admission.py` | 17 |
| `test_pre553_discovery_exact.py` | 14 |
| `test_pre553_analytical_composition.py` | 13 |
| `test_source_backed_positioned_subject_possibility.py` | 13 |
| `test_pre553_discovery_adaptive.py` | 8 |
| `test_pre553_discovery_adaptive_admission.py` | 3 |
| `test_pre553_recursive_handoff.py` | 2 |
| **total** | **208 passed, 0 failed, 0 errors, 0 skipped** |

Runtime 21.58 s, exit 0. Python 3.12.14, pytest 9.1.1, darwin.
Historical R3 court: 199 passed. 9 new courts. **Only these ten files were executed
— no broader sweep is claimed.**

## The reviewer was right, and the aggravating detail matters

I reproduced both counterexamples against the owner before changing anything. Both
minted trusted state from nothing:

```
INTEGRITY_FAILURE minted : urn:t:totally-made-up   <- caller-chosen ref
BLOCKED minted          : urn:t:totally-made-up   <- caller-chosen ref
```

The detail that makes this worse than a missing check: the fabricated projection
carried the **real owner label**
`rawlsing_next.pre553_empirical_query.execute_empirical_query` even though no owner
execution had ever occurred. So the envelope attested that a competent owner had run
and refused, when nothing had run at all.

I also checked commission option (1) properly rather than assuming: there is **no**
canonical owner-produced refusal witness, receipt or rejection record type anywhere
in the owner modules, and both refusal types are bare `ValueError` subclasses with no
fields. Option (1) was genuinely unavailable; option (2) was the only lawful route.

## The mechanism

A trusted refusal now requires a token-guarded `OwnerRefusalWitness`, and only a
capture function that **invokes the real owner itself** can produce one.

- `capture_empirical_integrity_refusal` invokes `type(original_object)` — the
  canonical object class taken from a **genuine owner-produced object**, never from
  the caller. The refused ref is that object's own sealed `.ref`; the supporting refs
  are its own authority, dependency and replay bindings. The caller supplies only the
  tampered body.
- `capture_required_authority_refusal` imports and calls the real
  `execute_exact_bounded_discovery` itself. The owner function is never
  caller-supplied.
- Both catch only the exact expected type and bind `invocation_binding =
  semantic_hash(exact owner-call inputs)`.

The `exception`, `producer_ref`, `supporting_refs` and `reason` parameters were
**removed** from both refusal factories. A caller can no longer independently choose
the retained state, the producer/input ref, the supporting refs, or the owner label.

**Fail-closed:** if the owner *accepts* the input, there is no refusal — absence of
refusal is never converted into a governed state. A court proves this by capturing
against an untampered genuine body and expecting refusal of the *capture*, not a
state.

## The subclass trap stays controlling

`Pre553AuthorityError` subclasses `Pre553IntegrityError`. Each capture fixes its
`refusal_kind`, and each factory gates on that kind, so neither witness can be
replayed as the other state. No `isinstance` classification anywhere.

## Hostiles

All twelve required hostiles proven. Two prior exception-heuristic courts were
**rewritten** as authenticity hostiles (they tested the old substring/type rules,
which no longer exist); the rest are new.

The reviewer's stale short-circuited `coverage_custody.completeness_state` branch is
removed. Worth noting: it referenced a field deleted in R2 and would have raised
`AttributeError` had it been reached — the condition guarding it was unreachable, so
it was latent, not live. Handoff semantics unchanged.

## Preserved

All four R3 gates still enforced in the owner and their courts pass —
`DUCK-TYPED-OWNER-001`, `CALLER-SUPPORTING-REFS-001`, `RECEIPT-NOT-DOMINATED-001`,
`REQUESTED-USE-CONTRADICTION-001`. AT15's genuine `ADMITTED` route still binds its
exact rule hash. AT16 54/6 remains `SUPPORTED`. The eight negative states remain
distinct. C1-02 untouched. Receipt dominance, adaptive determinant provenance and
learned-route obligation law unchanged.

## Changed files

- `rawlsing_next/pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/test_pre553_analytical_state_and_route.py`
- `rawlsing_next/tests/c1_at14_at16_fixture.py`
- `WORKER_RETURNS/PYAT-C1-03A-REFUSAL-AUTHENTICITY-R4/**`

`pre553_empirical_query.py`, `pre553_discovery_exact.py`, `pre553_empirical_objects.py`,
`pre553_empirical_authority.py` and `pre553_analytical_composition.py` all verified
byte-unchanged. No owner module was modified and no receipt was fabricated.

## Non-claims

No raw sources. No C4/C7. No C1-03 join. No C1-R. No V3. No architecture warrant. Not
merged, not self-adopted.

## Terminal

`C1_03A_REFUSAL_AUTHENTICITY_RETURNED__HQ_ADJUDICATION_REQUIRED`
