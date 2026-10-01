# PYAT C1-03A — INDEPENDENT ACCEPTANCE REVIEW — R1

**Disposition:** `CHANGES_REQUIRED`

**Terminal:** `C1_03A_INDEPENDENT_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`

Reviewed implementation return:
`a3c07426b0ad547287cc729b23cd8428c9fc0018`

Worker commission tip:
`da29402473ad671625feb49fad5142a1d689978b`

Adopted C1-02 base:
`bc661188b51e995d9f5d74e55c4e37d2ba358a17`

Reviewer issue tip:
`0b3c8ae01b1a33cc71ddb759cca65949a9e25a3f`

## Bottom line

The C1-03A return contains substantial real work and its recorded 157-test court is internally credible. The worker also correctly drove several important current owners: empirical-query negative states, exact-discovery underpower, adaptive unvisited coverage, structural admission, C1 composition, and the named positioned-subject possibility consumer.

It is **not independently acceptable yet** because the new C1-03A envelope does not itself enforce the semantic relations it claims to conserve. Three counterexamples are decisive.

## C1-03A-REVIEW-BLOCK-STATE-PROJECTION-001

`ProducerStateEvidence` accepts `producer_state` and `retained_state` as independent caller inputs. `build_state_route_result()` checks only that all supplied evidence items agree with each other on the retained label; it never validates that the retained label is the lawful projection of the producer-native state.

Therefore a caller can bind a real `SUPPORTED` producer ref to `VALID_EMPTY`, `UNVISITED`, `INTEGRITY_FAILURE`, etc., so long as the chosen retained label is in `RETAINABLE_STATES`.

The worker's own AT16 positive test demonstrates the defect in committed code: the real 54/6 ATT1→ATT2 composition has `analytical_state == "SUPPORTED"` and both target cells have positive support (54 and 6), but the final envelope is built with retained state `OBSERVED_ZERO`.

That is not merely a hostile possibility; the acceptance witness itself contains a false retained-state claim.

**Required correction:** derive or validate retained state from the actual competent owner object. A free caller-supplied `retained_state` must not be sufficient to establish the envelope's analytical state. Typed owner-specific constructors/validators are acceptable.

## C1-03A-REVIEW-BLOCK-ROUTE-DERIVATION-001

AT15 explicitly requires that route legitimacy not become true merely because the caller passes a route label.

The implementation does exactly that:

- `build_state_route_result()` accepts `route_class` directly.
- `assert_route_not_laundered()` accepts both `route_class` and `required_route_class` directly.
- no `AdmissionEvaluation`, `StructuralEmpiricalAdmission`, rule hash, admission-authority ref, target-use/use-contract identity, or equivalent owner-produced route obligation is an input to the laundering decision.

The AT15 tests first execute structural admission and observe a non-ADMITTED decision, but the result of that owner call is not supplied to the route guard. The test then separately tells the guard that `required_route_class="LEARNED_OR_ADJUDICATED_REQUIRED"`. The guard only proves that two caller strings differ.

The positive learned/adjudicated case is also incomplete: the court proves that `rule=None` cannot admit, but it does not produce a successful ADMITTED structural-use receipt and bind that exact receipt/rule/authority/use identity into a learned/adjudicated route envelope.

The return's claim that route classification "binds exact producer/result/authority identities" is therefore overstated. Authority refs are merely optional envelope inputs, and the worker even proves that a learned-labeled envelope with `authority_refs == ()` can be constructed.

**Required correction:** derive route obligation from an exact current owner/use contract. For the structural-admission example, bind the exact admission receipt, rule identity, requested admission authority, target-use/use contract and decision. The laundering guard must consume that owner-produced evidence, not a caller-supplied `required_route_class` string. Prove one positive ADMITTED learned/adjudicated route and the failed/DENY hostiles against the same route law.

## C1-03A-REVIEW-BLOCK-HANDOFF-COVERAGE-001

The positive-recursive-handoff hostile does not test the governing requirement.

The requirement is: a selected positive handoff must remain linked to / accompanied by access to the actual discovery/adaptive coverage record; a positive bundle alone cannot masquerade as complete coverage.

The current hostile instead tests:
1. relabel a positive handoff as `UNVISITED` with no unvisited refs; and
2. attach unvisited refs to a positive retained state.

Those are useful anti-collapse checks, but neither proves that a normal positive handoff envelope is forbidden when `coverage_record_ref=None`.

`build_state_route_result()` has no invariant requiring a positive recursive handoff to carry its `evaluated_frontier_ref`, discovery result/coverage receipt, or equivalent access path. A positive handoff can therefore be wrapped with no retained coverage record.

**Required correction:** bind recursive-handoff identity to the exact coverage record/frontier it came from, and reject the positive handoff when that access/custody is absent or mismatched. Test the actual missing-coverage-record hostile.

## Requirement adjudication

### AT14 — `CHANGES_REQUIRED`

Strong executed evidence exists for the underlying owner states:
- observed zero is correctly detected from the empirical cell projection;
- VALID_EMPTY is owner-produced;
- UNDERPOWERED is produced by exact discovery;
- UNRESOLVED and NONCOMPARABLE are owner-produced;
- UNVISITED is genuinely produced by adaptive budget truncation with exact unvisited refs;
- DENY authority and integrity tampering produce real owner refusals.

However, the bounded envelope does not enforce the mapping from those owner states/refusals to the retained label. BLOCKED and INTEGRITY_FAILURE are especially represented after an owner exception by caller-supplied retained labels rather than by a typed owner-derived projection. The positive-handoff coverage obligation is also not enforced.

### AT15 — `CHANGES_REQUIRED`

This is the decisive failure. The route requirement is caller asserted rather than owner derived/bound. Direct and learned labels reidentify the envelope, but identity binding of a label is not legitimacy. No positive learned/adjudicated receipt is bound into the route result.

### AT16 — `PARTIAL_PASS__CHANGES_REQUIRED_FOR_FINAL_ENVELOPE`

The actual source-free public path is real:

empirical producer → accepted C1 composition → named current possibility consumer.

The test correctly checks producer fact ref, generated evidence, composition identity, consumer query/rule, and consumer result identity. The handmade/direct-consumer hostile also correctly shows that a bare primitive result is weaker than the composed witness.

But the final C1-03A envelope attached to this witness carries the wrong retained state (`OBSERVED_ZERO` over an actually `SUPPORTED` 54/6 composition). Until state projection is owner-derived/validated, the final receipt cannot be accepted as an internally truthful AT16 result.

## Regression / provenance

- `da294024...a3c07426` is a one-commit fast-forward.
- Worker diff adds only the bounded C1-03A owner, its fixture/test files, and its return packet.
- The adopted C1-02 owner is not modified.
- The recorded test obligations reconcile:
  - C1-03A: 20 real test functions;
  - adopted C1-02 six-file court: 109, matching the prior accepted 13+35+32+14+2+13 inventory;
  - adaptive discovery: 8 + 3 = 11;
  - structural admission: 13 test functions with one 5-case parametrized court = 17;
  - total: 157.
- No fresh runtime execution was required to establish these static counterexamples.
- The commission references `PYAT_CONTROL_ROOM/OMEGA_VOZHD_ORCHESTRATION_R1/05_C1_EXECUTION_SPEC.md`, but that file is not present in the reviewed return/reviewer ancestry. For requirement interpretation, this review read exact live-control blob `f6f0e6624f87c631e3c65b9242cc2c2e7203a61b`; it reinforces the same state-collapse, route-legitimacy and coverage obligations already restated in the commission itself. This ancestry mismatch is documentary, not the reason for rejection.
- Live control observed during review: `26933640b75f833aae42eec71f650ec11e908a0a`; C1-03A implementation terrain is not present there, so no live adoption is inferred.

## Smallest repair

No adopted C1-02 owner change is justified.

Repair only the C1-03A owner/tests/return packet:

1. make retained-state projection owner-derived or fail-closed validated;
2. correct the AT16 positive envelope to its true retained state;
3. make route obligation owner/use-derived and bind exact structural-admission receipt/rule/authority/use identity;
4. add one successful learned/adjudicated route;
5. make positive recursive handoffs require exact coverage-record custody;
6. rerun the C1-03A court plus the same commissioned regression/relied-on courts and replace the return receipts consistently.

**Terminal:** `C1_03A_INDEPENDENT_REVIEW_RETURNED__HQ_ADJUDICATION_REQUIRED`
