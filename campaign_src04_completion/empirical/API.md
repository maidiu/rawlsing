# Lane C — observed-response / co-observed API

The public execution family is unchanged: callers construct an
`EmpiricalQuerySpec@1.0.0`, an `EmpiricalPredicate@1.0.0`, and call the existing
`rawlsing_next.pre553_empirical_query.execute_empirical_query` (or
`replay_empirical_query`).  Canonical truth remains in the returned
`EmpiricalFact@1.0.0`; this lane adds a separately authority-bound risk-set profile
and a ledger, not a parallel tally engine.

## Exact profile fields

Add these to `EmpiricalQuerySpec.requested_output_grain`:

```json
{
  "risk_set_type": "OBSERVED_RESPONSE_RISK_SET",
  "measure_kind": "RAW",
  "query_operation": "PRE553_OBSERVED_RESPONSE_EMPIRICAL_OPERATIONS@1.0.0",
  "observed_response_contract_ref": {"kind": "OBSERVED_RESPONSE_CONTRACT", "object_id": "...", "content_hash": "..."},
  "observed_response_contract": { "...exact PRE553_OBSERVED_RESPONSE_CONTRACT@1.0.0 material..." }
}
```

For a same-respondent multi-target/co-observed operation use
`"risk_set_type": "CO_OBSERVED_RESPONSE_RISK_SET"`.  The query must be
`SINGLE_UNIVERSE`, `RAW`, and its target components must carry the exact target
topology and source-native topology binding approved by the contract.  The
contract ref must be in `query.dependency_refs`; the contract's operation
authority must be the query's exact `query_authority_refs` and the predicate's
`grammar_authority_ref`.

The execution boundary refuses:

- a pending, missing, deferred or mismatched operation/topology authority;
- fixture-only authority in an `ORIGINAL_SCIENTIFIC` contract;
- release, source-artifact, manifest, universe or risk-set identity mismatch;
- a routing/applicability predicate in an observed-response condition;
- `GOVERNED_WEIGHTED` observed-response profiles; and
- routing unknown treated as nonmembership.  `_risk_membership` retains its
  original refusal semantics for eligible-risk profiles.

## Output family

The existing `EmpiricalFact` is returned.  Observed-response facts additionally
carry:

```text
fact.target_topology["observed_response"] = {
  "contract_ref": {...},
  "status": "OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION",
  "not_eligible_population_estimate": true,
  "ledger": {
    "scoped_respondents": ...,
    "target_observed": ...,
    "target_unobserved": ...,
    "condition_unobserved": ...,
    "condition_false": ...,
    "denominator": ...,
    "resolved_targets": ...,
    "unresolved_after_denominator": ...,
    "denominator_policy": "PER_TARGET_OBSERVED | CO_OBSERVED_TARGETS",
    "condition_observation_policy": "ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED",
    "not_eligible_population_estimate": true
  }
}
```

`raw_numerator_support` and `raw_denominator_support` remain the existing exact
`EmpiricalFact` fields.  `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET` means an observed
zero numerator with a positive exact denominator; it is not `ZERO_SUPPORT`.

## Contract/material API

`rawlsing_next.pre553_observed_response` exports:

- `OBSERVED_RESPONSE_RISK_SET`, `CO_OBSERVED_RESPONSE_RISK_SET`
- `ObservedResponseContract`, `ObservedResponseTopologyBinding`
- `validate_contract_authority`
- `validate_contract_for_query`
- `contract_for_query`
- `topology_binding_for`
- `predicate_requirements`

`ObservedResponseContract.from_mapping(...)` round-trips the exact contract
material and verifies its `contract_ref`.  `with_release_binding(...)` binds an
approval-ready contract to the exact full release ref, manifest hash, universe and
positive authority refs; it constructs identifiers only and does not create
authority.

## Lane D consumption

Lane D should treat the returned `EmpiricalFact` exactly like any other I03 fact
for provenance/replay, and must use the `observed_response` ledger to preserve:

- observed/not-eligible-population status;
- target observation versus condition observation versus condition-false counts;
- per-target versus common-observation denominator policy; and
- the contract ref that authorized the operation.

It must not relabel these facts as eligible-risk or weighted-population estimates,
and it must not issue I03/I05 or structural claims without the separate exact
authority required by the standing program.
