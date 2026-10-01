# PYAT C1-02 — WITNESS PAIRING-GROUND-TRUTH REACHABILITY REPAIR — R1

Status: `PASS_BLOCKER_REPAIRED__NARROW_INDEPENDENT_REREVIEW_REQUIRED`

## Mission

Repair exactly one acceptance-blocking finding:

`C1-02-REVIEW-BLOCK-WITNESS-PAIR-001`

Branch: `agent/opencode-pyat-hq143-c1-02-witness-pairing-repair-r1`
Base: `6e0f7b438089a542c9949b604cd55cbb3eaf8b2b`
Independent review: `c9ed2fe49d032b9313c3d24227a08fd9ca3aff89`

C1-02 was **not** redesigned. No AT court, fixture oracle, hostile or documentary
artifact from the prior corrected return was reopened.

## The defect, exactly

In `rawlsing_next/pre553_analytical_composition.py`, function `_verify_witness`
(multi-conditioner branch), lines 656–667, the four per-conditioner
pairing-ground-truth semantic comparisons were indented one level deeper than an
unconditional `raise`:

```python
if not match_found:
    raise ConditionValueRelationMismatch(f"conditioner {i}: no matching producer leaf found")

    pair = canonicalize(witness.pairing_ground_truth_materials[i])   # unreachable
    ... four pairing comparisons ...                                # unreachable
```

Any execution reaching that block raised on the first statement, so the four
comparisons could never run on any path. The verifier therefore performed only
structural, count and hash-integrity checks and never compared the pairing
semantics back to the subject/binding/producer truth.

The legacy single-conditioner path already performed these same four comparisons
at owner lines 558–566 and was always reachable. That is exactly why the C1-01
legacy court stayed green while the generalized multi-conditioner path carried
the gap.

## A second defect found while repairing

The dead block read `subject` from the *earlier* per-binding loop. Because the
block was unreachable this never mattered, but naively de-indenting it would have
compared **every** conditioner's pairing against the **last** conditioner's
subject material. The repair re-binds `subject` from
`witness.subject_condition_preimage_materials[i]`. Both changes were required for
the checks to be *correct*, not merely reachable.

## Hostile construction

The commission's hard requirement was that the hostile must **not** pass by
corrupting a hash. `readdress_witness_with_false_pairing`
(`rawlsing_next/tests/c1_at08_at13_fixture.py`) therefore mutates only pairing
*semantics* and then re-content-addresses everything that depends on it:

- the mutated pairing material's own ref (`content_hash = semantic_hash(mutated)`)
- the witness identity material's pairing refs and materials
- the witness ref (`content_hash = semantic_hash(rebuilt identity)`)

Left deliberately unchanged: the consumer bindings, subject preimages, producer
leaf projections, pairing authorities, and the producer predicate/query and
consumer query.

Every hostile calls `hostile.verify_identity()` and **asserts it succeeds**
before composing. `verify_identity` *is* the hash/preimage-integrity gate, so
because it passes, the later rejection can only come from the newly reachable
semantic comparisons. The first hostile additionally asserts that the pairing ref
and the witness ref genuinely **changed**, proving they were recomputed rather
than left stale.

Two independent semantic lies are exercised, since a single helper parameter
made both cheap:

| Court | False relation | Truth preserved |
|---|---|---|
| `..._false_required_semantic_ref_is_rejected` | `required_semantic_ref` names a valid but wrong coordinate | subject preimage still `A=1` |
| `..._false_required_exact_value_is_rejected` | `required_exact_value` `'1'` vs truthful `'0'` | subject preimage still `'0'` |
| `..._rejection_precedes_evidence_and_consumer` | `required_exact_value` set to a bogus string | binding/subject/leaf untouched |

A control court (`..._baseline_witness_is_accepted`) proves the unmutated witness
composes, so the hostiles isolate pairing semantics rather than an unrelated
fixture defect.

## Fail-closed ordering is proven, not inferred

The ordering court temporarily replaces `_build_evidence` and
`evaluate_positioned_subject_possibility` with sentinels that record any call and
raise. After the repair, `touched == []`, proving possibility evidence was never
constructed and the consumer was never invoked.

Before the repair, the same court produced
`AssertionError: possibility evidence must not be constructed` — the evidence
sentinel **fired**. That is the decisive pre-repair reproduction.

## Evidence

Pre-repair reproduction, preserved verbatim:
`BLOCKER_REPRODUCTION_PRE_REPAIR.txt` — `3 failed, 1 passed`, with
`DID NOT RAISE ConditionValueRelationMismatch` twice and the evidence sentinel
firing once.

Post-repair, the same selection: `4 passed`.

## Final commissioned court

**109 passed, 0 failed, 0 errors, 0 skipped** (exit 0). Python 3.12.14, pytest 9.1.1.

| File | Tests |
|---|---|
| `test_pre553_analytical_composition.py` | 13 |
| `test_pre553_analytical_composition_higher_order.py` | 35 (31 original + 4 new) |
| `test_pre553_empirical_query.py` | 32 |
| `test_pre553_discovery_exact.py` | 14 |
| `test_pre553_recursive_handoff.py` | 2 |
| `test_source_backed_positioned_subject_possibility.py` | 13 |
| **total** | **109** |

Count reconciliation: **105 accepted + 4 new = 109**. The count did increase, as
the commission requires.

## Commission checks

- No regression from the accepted 105: **confirmed** (109 = 105 + 4).
- All original 31 higher-order tests present: **confirmed** (35 now, originals unchanged).
- All test names cited by the corrected matrix still exist: **confirmed** (30 cited, zero missing).
- C1-01 legacy analytical court green: **confirmed** (13 tests; legacy witness path untouched).
- Wider regression sweep: **not required and not run**. The repair changes only `_verify_witness` plus C1-02-owned test/fixture files, which the commission exempts. The prior three-tree attribution `NO_WIDER_REGRESSIONS_DETECTED_AT_ACCEPTED_C1_01_BASELINE_GRAIN` is retained and not contradicted.

## Accepted findings preserved

All twelve accepted independent-review findings stand untouched, including the
AT08–AT13 courts, the AT10 and AT11 grain rulings, all three earlier owner fixes,
C1-01 regression preservation, wider-regression attribution, execution provenance
and the authority ceiling. **No counterexample to any of them was found.** The
legacy single-conditioner witness path was not modified at all.

## Changed files

- `rawlsing_next/pre553_analytical_composition.py` — 7 lines de-indented, 1 rebind added, 4 comment lines
- `rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py` — 4 new courts
- `rawlsing_next/tests/c1_at08_at13_fixture.py` — `readdress_witness_with_false_pairing`
- `WORKER_RETURNS/PYAT-C1-02-WITNESS-PAIRING-REPAIR-R1/**` — this return

The prior corrected C1-02 return directory, the independent review directory, the
generic C1 packet and every upstream owner are **byte-unchanged**.

## Prohibitions

No raw survey files. No Candidate A/B/C. No measured P2X. No real-source C11. No
C4. No C1-03 implementation. No new semantic/comparability/model authority. No V3
actor/person implementation. Kimi's preserved branch untouched. Prior corrected
and review artifacts untouched. Not merged. Not self-adopted.

## Terminal

`C1_02_WITNESS_PAIRING_REPAIR_RETURNED__HQ_ADJUDICATION_REQUIRED`