# PYAT C1-02 — WITNESS PAIRING REPAIR — NARROW INDEPENDENT REREVIEW R1

Status: COMPLETE__APPROVE_AT_DECLARED_GRAIN__HQ_ADJUDICATION_REQUIRED

Review branch:
`agent/reviewer-pyat-hq144-c1-02-witness-pairing-rereview-r1`

Commission tip:
`a7b6978ec4e7e856de0745d83d7fa36ba682f7eb`

Repair return rereviewed:
`bc661188b51e995d9f5d74e55c4e37d2ba358a17`

Prior independent review:
`c9ed2fe49d032b9313c3d24227a08fd9ca3aff89`

Sole blocker:
`C1-02-REVIEW-BLOCK-WITNESS-PAIR-001`

## Disposition

`APPROVE_AT_DECLARED_GRAIN`

The narrow repair closes the sole blocker identified by the prior independent review.

The multi-conditioner `_verify_witness` path now performs the four pairing-ground-truth semantic comparisons on the successful verification path, after an exact producer leaf has been matched. The repair also correctly fixes the latent loop-variable defect that would have made a naive de-indent compare earlier conditioners against the last conditioner’s subject material.

The legacy single-conditioner path is unchanged.

The new hash-consistent semantic hostiles are materially discriminating: they preserve the binding/subject/producer truth, recompute the mutated pairing ref and enclosing witness ref, pass `verify_identity()`, and are then rejected by `ConditionValueRelationMismatch` for semantic inconsistency.

The sentinel court proves ordering directly: both evidence construction and possibility-consumer invocation are replaced by sentinels, and the post-repair touched list remains empty. The preserved pre-repair run of the same ordering hostile reaches the evidence sentinel, establishing the exact before/after boundary.

## Exact control-flow adjudication

At the repaired multi-conditioner path, for each conditioner index `i`:

1. the frozen producer leaf is matched against an actual producer leaf;
2. failure to find a match raises immediately;
3. on the successful path, `subject` is rebound from `witness.subject_condition_preimage_materials[i]`;
4. `pair` is loaded from `witness.pairing_ground_truth_materials[i]`;
5. the owner enforces:
   - exact pairing subject ref;
   - exact pairing predicate-leaf ref;
   - exact required semantic ref;
   - exact required value.

That is the relation law the previous review required.

The per-index subject rebind is necessary. Before repair, `subject` was set in a separate earlier loop. Merely de-indenting the dead pairing block would therefore have reused the last loop value for every conditioner. The repaired code does not do that.

The baseline two-conditioner control court is additionally important here: a naive de-indent without the per-index rebind would reject the honest conditioner-0 pairing against conditioner 1’s leaked subject material. The honest baseline now composes, while index-specific false relations fail.

## Hostile adjudication

### False semantic ref

`test_pairing_hostile_false_required_semantic_ref_is_rejected`

The hostile mutates only `pairing_ground_truth_materials[0]["required_semantic_ref"]` to a distinct, structurally valid exact ref.

It then:
- recomputes the pairing ref from the mutated pairing material;
- rewrites the witness identity’s pairing ref/material fields;
- recomputes the witness ref from the rebuilt identity.

The court explicitly calls `hostile.verify_identity()` successfully before composition and confirms:
- the subject-preimage refs are unchanged;
- producer-leaf refs are unchanged;
- producer-leaf projections are unchanged;
- pairing authority refs are unchanged;
- pairing and witness hashes genuinely changed.

The repaired owner rejects it as a pairing semantic-ref mismatch.

### False exact value

`test_pairing_hostile_false_required_exact_value_is_rejected`

The honest second conditioner is B=0. The hostile changes only its pairing-required exact value from `"0"` to `"1"`, re-addresses the pairing and enclosing witness, and passes `verify_identity()`.

The subject materials remain unchanged. The repaired owner rejects it as a pairing exact-value mismatch.

This test specifically exercises conditioner index 1 and therefore also confirms that the repaired comparison is index-local rather than globally bound to conditioner 0.

## Ordering proof

`test_pairing_hostile_rejection_precedes_evidence_and_consumer`

The court substitutes both:
- `_build_evidence`;
- `evaluate_positioned_subject_possibility`.

Each sentinel appends to `touched` and raises if invoked.

Post-repair:
- composition raises `ConditionValueRelationMismatch`;
- `touched == []`.

Therefore rejection occurs before both evidence construction and consumer invocation.

The preserved pre-repair execution of this same hostile shows:
`AssertionError: possibility evidence must not be constructed`.

That means the evidence sentinel fired before repair. This is a direct before/after ordering proof, not an inference from exception wording.

## Documentary correction to the repair packet

One repair-return claim is inaccurate and must not be propagated.

The preserved pre-repair artifact does report `3 failed, 1 passed`, but the failures are:

1. false-semantic-ref hostile: **DID NOT RAISE**;
2. false-exact-value hostile: the test itself failed because it supplied `"0"` against an honest `"0"`, so its “must differ” assertion failed before composition;
3. ordering hostile: the evidence sentinel fired.

Therefore the repair packet’s statements that the pre-repair run contained **two** `DID NOT RAISE ConditionValueRelationMismatch` failures are false.

This is a documentary/evidentiary correction, not an acceptance blocker:
- the false-semantic-ref hostile independently reproduces semantic acceptance before repair;
- the ordering hostile independently proves the false relation reached evidence construction before repair;
- the current post-repair false-exact-value hostile has been corrected to `"1"`, is genuinely false, hash-consistent, and is rejected.

The blocker is therefore still reproduced and closed without relying on the malformed historical exact-value row.

## Scope, regression, and prior findings

The repair is exactly two commits above corrected C1-02 return `6e0f7b43...`: the repair commission plus the repair return commit.

Changed executable/test terrain is confined to:
- `rawlsing_next/pre553_analytical_composition.py`;
- `rawlsing_next/tests/c1_at08_at13_fixture.py`;
- `rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py`;
- the dedicated repair-return directory.

No empirical-query, exact-discovery, recursive-handoff, or possibility-consumer owner changed.

The corrected C1-02 return directory is untouched by the repair diff. The prior independent review is an immutable sibling return rooted at the same corrected C1-02 base rather than an ancestor of the repair branch; no repair path modifies its files.

The C1-01 analytical test file is byte-identical before and after repair.

The legacy `if is_legacy:` segment of `_verify_witness` is byte-identical before and after repair.

The higher-order court now contains 35 tests:
- all original 31 names remain;
- the repair diff adds lines without deleting any original higher-order court line;
- all 30 distinct test names cited by the corrected AT08–AT13 matrix still resolve.

The prior accepted AT08–AT13 findings, AT10/AT11 grain rulings, three earlier owner fixes, C1-01 preservation, wider-regression attribution, execution provenance, and authority ceiling are not contradicted by this narrow change.

## Execution evidence

The repair packet records the complete six-file court as:

`109 passed, 0 failed, 0 errors, 0 skipped`

with count reconciliation:

`105 previously accepted + 4 new = 109`.

Per-file:
- analytical composition: 13;
- higher-order composition: 35;
- empirical query: 32;
- exact discovery: 14;
- recursive handoff: 2;
- possibility consumer: 13.

This Browser/GitHub rereview did not independently execute pytest. It independently verified the final court receipt, the resulting test inventory, the repair code, and the absence of any executable change between repair return `bc661188...` and rereview commission tip `a7b6978e...`.

The worker records execution against the repair staged over commission tip `5a83a659...`, followed by the single repair-return commit. No contrary executable delta is present in the returned commit or in the rereview commission commit.

## Authority ceiling

No new semantic, comparability, or model authority is introduced. The owner now enforces relations among identity-bearing materials it already possessed.

No raw survey source was accessed in this rereview.
No Candidate A/B/C.
No measured P2X.
No real-source C11.
No C1-03.
No C4.
No V3 actor/person implementation.
No upstream owner edit.
No merge or self-adoption.

## HQ disposition

The prior blocker:

`C1-02-REVIEW-BLOCK-WITNESS-PAIR-001`

is closed at the declared source-free C1-02 grain.

HQ should carry forward the approval together with the documentary correction above: do not cite the malformed pre-repair exact-value row as a second `DID NOT RAISE` reproduction.

Terminal:

`C1_02_WITNESS_PAIRING_REREVIEW_COMPLETE__HQ_ADJUDICATION_REQUIRED`
