# PYAT C1-02 — CORRECTED HIGHER-ORDER / JOINT / RECURSIVE ANALYTICAL COMPOSITION — INDEPENDENT REVIEW R1

Status: COMPLETE__CHANGES_REQUIRED__HQ_ADJUDICATION_REQUIRED

Review branch:
`agent/reviewer-pyat-hq142-c1-02-correction-r1`

Commission tip:
`b33488a79103704aea8a6fa1163a764045bcf4c9`

Corrected return reviewed:
`6e0f7b438089a542c9949b604cd55cbb3eaf8b2b`

Code/test state reviewed:
`795bd0814980b06174119a766a3f3940a2842385`

Immutable Kimi return:
`21254c57d92c6411282de13450fc2bdfab21d345`

Accepted C1-01 baseline:
`5fafb499d53dddadaf8a7b4fd46506e91a09d270`

## Disposition

`CHANGES_REQUIRED`

The corrected return repairs the prior evidentiary failure in a substantial and mostly successful way. The corrected AT08–AT13 matrix now cites real tests; the synthetic oracles are materially instantiated; the 105-test commissioned court is coherently attributed; the three claimed owner fixes are real, local, and responsive to actual owner-law defects; C1-01 behavior is preserved at the exercised grain; wider-regression attribution supports `NO_WIDER_REGRESSIONS_DETECTED_AT_ACCEPTED_C1_01_BASELINE_GRAIN`; and the final documentary commit preserves the tested executable/test/fixture blobs byte-for-byte.

The return nevertheless cannot be approved at the declared grain because the C1-02 multi-conditioner witness verifier contains an acceptance-bypassing relation-integrity defect.

## Blocking counterexample — C1-02 witness relation law is incomplete

Path:
`rawlsing_next/pre553_analytical_composition.py`

Function:
`_verify_witness(...)`

In the non-legacy / multi-conditioner branch, the intended per-conditioner pairing-ground-truth checks are indented beneath:

```python
if not match_found:
    raise ConditionValueRelationMismatch(...)

    pair = canonicalize(witness.pairing_ground_truth_materials[i])
    ...
```

The `pair = ...` block and its four semantic consistency checks are therefore unreachable. This is not merely dead redundant code. The legacy C1-01 witness path performs these checks, while the generalized C1-02 path does not.

A self-consistent hostile witness can therefore:

1. retain a valid consumer binding, subject preimage, producer predicate leaf, universe, release, and pairing authority;
2. alter one `pairing_ground_truth_materials[i]` field such as `required_exact_value`, `required_semantic_ref`, `subject_preimage_ref`, or `predicate_leaf_preimage_ref`;
3. recompute that pairing ref from the altered pairing material;
4. recompute the outer witness identity/ref from the altered pairing ref/material;
5. pass `ConditionValueBindingWitness.verify_identity()` because every ref still hashes its supplied material;
6. pass the remainder of the multi-conditioner `_verify_witness` path because the altered pairing relation is never compared back to the exact subject/leaf relation.

That violates the declared C1 relation law: a hash-consistent custody object is not sufficient if the custody material can state a false relation and still reach evidence construction and the consumer.

This counterexample is established by exact static inspection of the committed code state. I did not modify implementation or tests and did not execute a local/runtime counterexample.

### Required correction

The correction owner should restore the per-conditioner pairing checks to the reachable success path, preserving the exact legacy semantics:

- pairing subject ref == exact subject preimage ref;
- pairing predicate-leaf ref == exact producer leaf ref;
- pairing required semantic ref == exact subject/binding semantic ref;
- pairing required exact value == exact subject/producer value.

A hostile court should then mutate at least one pairing-ground-truth relation field, recompute all dependent hashes/refs so the object remains internally hash-consistent, and require fail-closed before evidence construction or consumer invocation. A simple stale-hash mutation is not sufficient to prove this law.

## AT10 scope adjudication

The worker's shorthand `out of scope` is too broad, but its result at this grain is acceptable.

The original commission makes the underpowered-state obligation conditional: **if** an underpowered branch is also exercised by the competent discovery owner, its distinct state must survive. The corrected AT10 court exercises a complete exact-bounded frontier containing the supported modal/minority/counterpattern branches and does not exercise an underpowered branch. Full AT14 negative-state coverage is expressly deferred.

Therefore C1-02 did **not** require inventing an underpowered/adaptive branch solely for AT10. If such a state had arisen in the exercised frontier, it would have been in scope to preserve.

## AT11 adaptive/unvisited adjudication

No `EXPLICIT_UNKNOWN_UNVISITED` adaptive route was required here.

The actual discovery owner used by AT11 is exact-bounded: `ExactBoundedDiscoveryResult` requires `COMPLETE_FOR_EXACT_DECLARED_FRONTIER`, requires `candidate_count == covered_candidate_count`, and the executor evaluates every compiled candidate. The recursive wrapper returns both the full `discovery_result` and the selected supported handoff(s); the persisted positive handoff bundle is therefore not the sole coverage record.

For the exercised generation-one and generation-two frontiers, the court establishes a singleton supported receipt and the owner invariants establish that this is the complete declared frontier. Negative/unselected/unvisited territory inside those exact declared frontiers is empty. The commission's requirement to preserve unknown/unvisited work applies to adaptive/partial paths; no such path is consumed here, and the corrected return makes no broader exhaustive-coverage claim.

The worker's `PARTIAL` label is conservative. At this exact-bounded grain, absence of an adaptive unknown route is not an acceptance blocker.

## AT08–AT13 result

The corrected courts materially establish the requested shapes:

- AT08: attitude-to-different-attitude conditioning, multi-conditioner conditioning, value-driven reidentification, and release/universe/measure fail-closed are exercised.
- AT09: XOR flat unary marginals versus decisive joint signal, equal-marginals/different-joints, consumer preservation, and marginal-only insufficiency are exercised from independent synthetic tables.
- AT10: modal, minority, and counterpattern supported branches survive direct and exact-discovery composition without silent deletion.
- AT11: generation one, retained write/load, fresh-process replay, real depth two through the public recursive owner, depth-two consumer use, ancestry, and lookalike-lineage anti-aliasing are exercised.
- AT12: same-respondent empirical co-travel reaches the consumer without S14/semantic-relation authority being invented.
- AT13: ranked non-scalar morphology, source-native order, topology/component material, lawful reorder reidentification, scalarization refusal, and heterogeneous-authority fail-closed are exercised.

However, these positive courts all use honest fixture-built C1-02 witnesses. They do not close the hostile relation-integrity counterexample above. AT08/C1 witness-law acceptance therefore remains incomplete, and the overall C1-02 patch cannot be approved.

## Owner-fix review

The three reported owner fixes are independently supported:

1. **Coordinate value-bearing leaves** — necessary and local. The exact discovery owner lawfully exposes governed empirical-position coordinate leaves; C1 composition previously could not witness them. The fix retains exact leaf type/operator/value matching and uses the owner-native semantic-ref key.
2. **Discovery fact selection by winning predicate** — necessary and local. A discovery receipt can carry baseline and candidate facts; `fact_refs[0]` is not a semantic selector. Selecting the fact whose `condition_predicate_ref` equals the exact winning predicate is the lawful binding.
3. **Recursive lineage closure over owner-native `ancestry_refs`** — necessary and local for real depth-two continuation. `recursive_parent_atom` places the earlier handoff ref in the grammar atom's `ancestry_refs`; walking that retained owner-native material closes the full chain without inventing lineage.

None requires an upstream producer/discovery/recursive/consumer edit. None is rejected by this review. The blocking witness defect is distinct and pre-existed the correction commit in the Kimi C1-02 generalized path.

## C1-01 and wider regression

All 13 current analytical-composition regression tests execute green in the recorded 105-test court, including AT07 identity-bearing behavior and the legacy exact witness path. The C1-01 test file is not byte-identical to the accepted baseline: its signature whitelist was deliberately extended to admit the three C1-02 optional inputs. That is a bounded compatibility update, not evidence of an AT07 semantic regression.

The wider-regression packet provides an exact node-ID inventory and reports identical failing/error sets across accepted baseline, Kimi return, and corrected head, with no node passing at the accepted baseline and failing now. The listed byte-frozen courts do not freeze `pre553_analytical_composition.py), and no frozen expectation was edited. I accept:

`NO_WIDER_REGRESSIONS_DETECTED_AT_ACCEPTED_C1_01_BASELINE_GRAIN`

## Execution provenance

The corrected final return is one documentary commit after the tested code head. Independent blob comparison found exact equality between `795bd081...` and `6e0f7b43...` for:

- `rawlsing_next/pre553_analytical_composition.py`
- `rawlsing_next/tests/test_pre553_analytical_composition.py`
- `rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py`
- `rawlsing_next/tests/c1_at08_at13_fixture.py`
- `rawlsing_next/tests/c1_at08_at13_fresh_process_runner.py`

The recorded 105/105 execution therefore transfers to the final returned executable state. No ceremonial rerun is required merely because documentation was synchronized afterward.

## Authority ceiling

No reviewed diff requires raw survey access, Candidate A/B/C, measured P2X, real-source C11 execution, new real-source semantic/comparability/model authority, implicit pooling, V3 actor/person implementation, C1-03 implementation, or C4. This review did not access raw survey files.

The failure is narrower: source-free C1-02 custody/relation validation is not yet closed against a hash-consistent false pairing relation.

## HQ action

Return C1-02 for one bounded correction of the multi-conditioner witness relation verifier plus a hostile hash-consistent pairing-relation court. Preserve all currently green AT08–AT13 evidence, all three owner fixes, the C1-01 regression court, and the wider-regression attribution unless that bounded repair changes them.

Terminal:

`C1_02_CORRECTION_INDEPENDENT_REVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
