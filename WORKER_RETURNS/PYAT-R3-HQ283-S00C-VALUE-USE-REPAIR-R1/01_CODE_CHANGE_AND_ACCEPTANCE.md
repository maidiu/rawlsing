# S00C code and acceptance map (authoritative writer limitations)

## Allowlisted paths only
`rawlsing_next/r3_s02_seam_witness.py` and matching `rawlsing_next/tests/test_r3_s02_seam_witness.py`, plus this own return folder. Historical S00 target manifest left byte-identical at startup because not on write list; it remains semantically invalid and may NOT be treated as an authoritative social construct, even if historical test asserts its existence.

## Numeric producer-to-consumer dataflow

`build_sociological_bundle` invokes accepted P04 `select_world`, `run_progressive_chain` and `verify_chain_preserves_contract`. The three P04 steps yield exact synthetic owner-generated cell numerators (18/14, 10/6, 6/2), step denominators 32,16,8, shared release/risk and producer evidence refs. Every generated channel is marked `TRANSFORMED`, `test_origin=True`, `source_scope=P04_SYNTHETIC_58_RESPONDENT_FIXTURE`; world metadata says NONE/geography, simulated subjects, `SOURCE_FREE_SYNTHETIC`, no real source value.

`ContractOnlySeamConsumer._validate_bundle` checks self-excluded bundle content hash, selected-world replay identity, `SOURCE_FREE_ONLY` grant, test origin, per-channel expected synthetic scope, exact recorded risk set and currentness rejection. For each requested exact condition step, `compute_scenario` calls `read_value` for exact category 0 and 1 channel IDs. It verifies that their step identity, conditioner list, raw count types, per-step denominator, declared risk and source agree. It computes denominator exactly once from the two target numerators, then `Fraction(n,d)` and marks those specific read receipts used. Its final output includes the final step's denominator, used channel refs/hashes and full ordered progressive trace, not a sum of overlapping supports.

Read alone: `VALUE_READ_ONLY`; actually used: `VALUE_USED_IN_EXACT_CONDITIONAL` only after compute. `get_receipt` sets its own hash field to empty before deriving hash so repeated receipt reads are stable. All returned source value numeric identities remain synthetic.

## Native Q86 source-free test seam
`build_source_free_native_joint_bundle({(Q86Bcode,Q86Acode): count})` accepts exactly four nonnegative integer 0/1×0/1 cells, with correct role order Q86B CONDITIONER, Q86A TARGET. It emits two independent exact conditional steps (`P_Q86A_given_Q86B_0` and `..._1`), **not** a fictional three-predicate cumulative chain and not a real survey. Full domain here is only the substantive 2×2 *invented test fixture*; real Field Forge also has nonsubstantive native states and rights constraints. It is tagged `SOURCE_FREE_SYNTHETIC_Q86B_Q86A_JOINT`, not source-measured. Consumer refuses grouping these disjoint x=0/x=1 as a "cumulative" step.

## Required scientific refusals
- Unknown exact condition selector: `NO_SUPPORT/NO_MATCHING_CHANNELS`.
- Source-free valid exact step but denominator zero: `ZERO_SUPPORT/ZERO_DENOMINATOR_ABSTENTION`.
- Wrong code/site/conditioning: `SOURCE_NATIVE_PREDICATE_DRIFT`.
- Wrong risk: `RISK_SET_OR_SELECTION_BINDING_MISMATCH`.
- Wrong channel scope/test origin/evidence: `SOURCE_SCOPE_OR_VALUE_ORIGIN_MISMATCH`.
- Rewritten input without corresponding complete exact digest: `BUNDLE_CONTENT_HASH_MISMATCH`.
- Changed numerator whose partner/denominator is inconsistent: `SOURCE_COUNT_CLOSURE_MISMATCH`.
- Unearned retained source: `UNISSUED_SOURCE_QUALIFICATION`, with hard source ingress `GT2_VALUE_HOLD`.
- False social construct scenario: `FALSE_S00_Q86_SOURCE_MEANING`.
- No unauthorized multi-conditioner beyond P04 proof: `NONCUMULATIVE_P04_STEP_SEQUENCE`.
- No real V3/V2/actor/person/current side effects.

## Preserved oracles and remaining work
P04 source-free fixture, actual N10E/C1/F8 code, 42 P04 tests, frozen S00R review/hostiles, canonical Field Forge and protected semantic controls untouched. Two inherited seam assertions were misleading: instant "read-and-used" without computation, and comparing IDs as a claim of different-joint sensitivity. They are strengthened, not marked historical passes. S00 remains outside authority and must be repaired by competent owner. Native 2×2 source-free counterpart is executable **only after qualified host runs the tests**. Real aggregate read permissions, full native Q86 response-state denominator and consumer use acceptance remain science HOLD. Independent S00CR review is REQUIRED.

**No environment performed source-row execution or model read of restricted data.**
