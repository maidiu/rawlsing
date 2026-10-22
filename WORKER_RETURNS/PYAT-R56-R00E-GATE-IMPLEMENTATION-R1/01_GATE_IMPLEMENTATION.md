# R00E gate implementation

## Public boundary

```python
evaluate_r56_sourcefree_claim(
    submitted_claim: Mapping[str, Any],
    *,
    externally_pinned_policy: PinnedPolicyHandle,
    verified_evidence: Any = None,
) -> dict
```

`submitted_claim` is untrusted. `externally_pinned_policy` must be the opaque handle produced by `load_pinned_policy`, which resolves the five R2 files from the pinned commit and verifies their freeze SHA-1 blobs. `verified_evidence` is not used to manufacture native authority.

## Policy resolution

`load_pinned_policy(commit, root, variant_id)`:

- reads `CONTRACT.md`, `policy.json`, `synthetic_universes.json`, `decision_cases.json`, `freeze.json` from Git;
- verifies the four content blobs against `freeze.successor_content_blobs`;
- selects `CANONICAL_V1` (`synthetic_universes.expected_operations`) or the frozen `ARC1_BIJECTIVE_Q301_LOCAL` full materialized variant;
- returns `PinnedPolicyHandle(commit, root, variant_id, policy, synthetic, freeze, expected_operations, expected_ids, blobs, verified)`.

The candidate cannot choose a variant through `submitted.candidate_variant_selection`; a mismatch between the claim's variant and the handle, a candidate pin, or an unverified handle yields `REFUSE_PIN`.

## Typed identity

`canonical_typed_identity` encodes explicit `null`, boolean, integer, decimal, string, ordered array and object entries. Object keys are sorted; arrays preserve declared order; null remains a value, not a missing key. `operation_identity_digest` hashes this versioned encoding. Semantic mismatches are computed per operation, not by count/name only.

## Candidate operation handling

The evaluator materializes candidate operations from `operation_objects` when supplied, or from the claim's `operation_ids_override` against the pinned expected set. It applies ID/status/disposition edits, then compares the full accepted operation objects, exact ID multiset, duplicates and semantic projections.

The gate does not branch on case ID. It does not use a literal q301_2/q301_7 blacklist; `ARC1_BIJECTIVE_Q301_LOCAL` is admitted only because the external pinned variant contains the full 18 renamed operation objects and bijections. A noninjective candidate rename is refused.

## Decisions and reasons

Precedence follows the frozen contract:

1. independent pin / candidate pin / variant mismatch;
2. forged native evidence (candidate boolean, trace, wrong attestation, mock transport);
3. exact K/currentness and permission;
4. original35 unissued hold;
5. status/disposition contradictions;
6. frontier/duplicate/semantic substitution;
7. generic/execution trust holds;
8. local policy-consistency allow.

Reason IDs are the policy's `P00`–`P17`. `grade_ceiling` is `LOCAL_ONLY_POLICY_CONSISTENT` only for local policy consistency; `NONE` for refusals and original/generic positive claims that lack trust. `actual_consumer_values_read` remains null. `published_original_grant` remains `UNISSUED`.

## Why native claims cannot pass

The evaluator has no R09 runner, native event verifier or original permission. Candidate `native=true`, `proof_transport`, trace objects, attestation objects and mock transports are treated as untrusted. A merely unverifiable native claim returns `HOLD_TRUSTED_NATIVE`/`HOLD_GENERIC_R09`; a demonstrably forged one refuses. There is no pretend signing or CI.

## Files

- `CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py`
- `tests/universal_execution_oracle/test_r56_gate.py`
- `tests/universal_execution_oracle/conftest.py`
- replay and witness tooling under the return subtree.
