# PYAT C1-01 — EXACT AT07 VERTICAL SLICE IMPLEMENTATION — R1 RETURN

## Disposition

`BLOCKED_CONTRACT_COUNTEREXAMPLE`

The C1-01 composition implementation is banked inside the exact write allowlist, but the frozen C1-00 package does not expose enough identity material to lawfully prove the two mandatory frozen AT07 consumer/evidence identities without weakening the accepted witness law.

## Exact branch / base

- branch: `agent/rabochii-pyat-hq130-c1-01-vertical-slice-r1`
- commission tip: `c833ac97afccf5eee3f6d3bc0fac5d89ceb2aec8`
- exact implementation base: `171200320b4acdbb8ba32106a992d76fa8ac7d8a`
- C1-00 disposition at base: `APPROVE_AT_DECLARED_GRAIN`

## Banked implementation

Created:

- `rawlsing_next/pre553_analytical_composition.py`
- `rawlsing_next/tests/test_pre553_analytical_composition.py`

No existing producer, consumer, authority, lifecycle, discovery, recursive-handoff, workflow, court-spec, facade, physical-decoder, or other test owner was edited.

The composition layer:

1. calls the public `execute_empirical_query(...)`;
2. selects the actual returned `EmpiricalFact`;
3. verifies the condition/value witness and actual producer predicate leaf before evidence construction;
4. preserves exact source/release/target/risk/measure/provenance/replay identities;
5. derives a noncircular `C1_POSITIONED_SUBJECT_SLICE_EVIDENCE_PREIMAGE@1`;
6. sets `raw_support = EmpiricalFact.raw_denominator_support`;
7. uses exact `Fraction` material rather than float identity;
8. constructs the current public `PossibilitySliceEvidence`;
9. calls the public `evaluate_positioned_subject_possibility(...)` only for a lawful supported slice;
10. retains the actual `QueryExecutionResult`, producer fact state, derived evidence and consumer result in the composition envelope.

## Exact counterexample

The accepted R2 relation law says the witness identity is:

`sha256(canonical_json(full_material))`

and requires the implementation to recompute, among other fields:

- `consumer_query_ref`;
- full `consumer_binding_material`;
- `consumer_binding_fingerprint`;
- `producer_query_ref`;
- `producer_predicate_ref`;
- exact subject-condition preimage;
- exact predicate-leaf preimage;
- exact pairing-ground-truth ref;
- exact source/release/effective-time tuple.

The accepted R3 evidence freeze publishes the resulting exact forward/reverse:

- consumer query refs;
- condition-value witness refs;
- complete evidence identity preimages.

It does **not** publish the canonical material of either frozen consumer query or either frozen witness instance.

That omission is decisive because the mandatory evidence hashes include the frozen witness ref in geometry/provenance, while the accepted witness law simultaneously forbids treating that ref as an opaque trusted label. SHA-256 is not invertible into the missing query/witness material.

Therefore C1-01 cannot simultaneously prove all three required statements from the accepted packet:

1. the actual consumer query recomputes to the frozen consumer-query ref;
2. the actual full witness material recomputes to the frozen witness ref;
3. the derived evidence recomputes to the frozen forward/reverse evidence hashes.

Trusting the published refs would manufacture identity authority; constructing new internally consistent query/witness objects would reidentify the evidence and violate the frozen hashes.

The banked red contract regression test makes this exact missing-preimage condition explicit.

## Frozen identities preserved

The return does not alter or reinterpret:

- forward arithmetic: `54/60`;
- reverse arithmetic: `54/62`;
- projection schema hash: `c00e038dd2c1177bfc7842f12febef7b3e30b92bc421df244e2a8e3c4a20b17a`;
- forward evidence hash: `fe5cd7783ac84f0298fb7f56a621d7b0e494bd9348d080dc68ceee09abb546f5`;
- reverse evidence hash: `b54201c8ba8743922e51627e621cc4f3d1c563a43b70167a0720fbb0028ccf72`;
- accepted universe/release/query-authority identities.

## Exact residual needed from HQ / C1-00 authority

Freeze and expose, without changing existing owners:

1. complete canonical `PositionedSubjectPossibilityQuery.material()` for forward and reverse AT07, sufficient to recompute:
   - `83727ca59eaf43085324ee7dc7db5ce4ecf4e4bf1f1284692cd3ad3f192df027`;
   - `cb2d085675c137848bb40f191ba8992100513eaa904a09cd54064f6ef51d3d8a`;
2. complete canonical `C1_CONDITION_VALUE_BINDING_WITNESS@2` material for forward and reverse, sufficient to recompute:
   - `c93e840c06da9ab8de9ca237863d52858fe6765d5bfd7c7efb42b879440663c9`;
   - `e81c4e19144a749877a6f6e7e48a213e869bfe5d04ba81372ca5384b7cf5e700`.

No change to `source_backed_positioned_subject_possibility.py` is presently required by this residual.

## Execution

No lawful off-Mac execution surface available to this Browser/GitHub worker can run the commissioned new test file without editing a forbidden workflow/court-spec owner. No PASS is claimed.

Exact unexecuted command is recorded in `04_EXECUTION_RECEIPT.json`.

C1-02 was not started.
