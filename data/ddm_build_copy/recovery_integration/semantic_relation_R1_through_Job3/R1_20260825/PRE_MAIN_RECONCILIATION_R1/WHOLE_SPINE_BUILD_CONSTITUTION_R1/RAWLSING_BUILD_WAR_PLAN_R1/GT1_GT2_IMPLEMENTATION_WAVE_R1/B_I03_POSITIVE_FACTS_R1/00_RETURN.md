# GT12-B — GT1 + GT2 EMPIRICAL I03 QUERY/FACT EXECUTION R1

## Terminal

`PASS__GT12B_I03_POSITIVE_FACT_EXECUTION_READY_FOR_CENTRAL_INTEGRATION`

Repository: `maidiu/rawlsing`

Branch:

`agent/rabochii-warplan-gt12-b-i03-positive-facts-r1`

Exact starting HEAD:

`2c95e64b9be9eb9c730028c840e04596dc556893`

Instruction/evidence ref:

`17b9abc5c8c3038d14670c6e68136bb868f5073a`

Frozen canary contract consumed:

`a9416094cbb4653dd2de2e4aa7b67577a355560c`

Sibling GT12 implementation branches consumed: `NO`.

Source acquisition: `NO`.

PRE-MAIN/main movement: `NO`.

## Implementation

Added bounded adapter:

`rawlsing_next/wave1_gt12_i03_positive_facts.py`

It uses the unchanged current:

`rawlsing_next/pre553_empirical_query.py`

and implements no parallel empirical executor.

The adapter expects one already validated `C11LogicalRelease` plus the exact projection/domain/authority bindings that central fan-in will receive from GT12-A. It does not import or consume GT12-A.

### Frozen GT1 surface

Claim:

`GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET@1`

The builder creates exactly:

- `SINGLE_UNIVERSE`;
- `RAW`;
- Q86A as the sole target;
- exact frozen risk-set ref;
- exact validated-projection Q86A source-native domain;
- exact target-domain replay ref;
- exact query/predicate authority;
- exact target-use permission binding;
- deterministic predicate/query identities and replay roots.

The GT1 target-use permission ceiling is pinned to:

`GT1_POSITIVE_EMPIRICAL_FACT_ONLY__NO_STRUCTURAL_OR_ACTOR_PROMOTION`.

### Frozen GT2 surface

Claim:

`GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1`

The empirical joint uses the frozen semantic component order:

`[Q86B, Q86A]`

so that the future FIELD FORGE projection can preserve:

- CONDITIONER = Q86B;
- TARGET = Q86A.

No conditioner/cause or target/effect semantics are minted by I03.

The query remains:

- `SINGLE_UNIVERSE`;
- `RAW`;
- `COMMON_ELIGIBLE_RISK_SET`;
- exactly two source-native targets;
- exact complete domains from the validated projection;
- deterministic replay.

## Jointability / denominator law

The adapter does not use Q86 source-block membership, source-structure co-membership, row co-presence or marginal distributions to establish jointability.

For the validated release it requires:

1. exact routing facts for every release respondent for Q86A and Q86B under the exact risk-set ref;
2. no unresolved routing state coerced to nonmembership;
3. exact equality of the Q86A and Q86B `ELIGIBLE_APPLICABLE` respondent sets;
4. exact member count `19,210` at production frozen grain;
5. exactly one included `SCALAR_SINGULAR` response event for each target for every frozen risk-set respondent;
6. every observed exact event state must occur in the complete target domain supplied by the validated projection.

Response presence is therefore checked separately from routing/exposure and cannot create eligibility.

## Exact frozen bindings

Production validation pins:

- source SHA-256 `c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`;
- risk-set identity `FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1`;
- risk-set rows `19,210`;
- semantic member-set SHA-256 `0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b`;
- Q86A qimpl `question_impl.phase0.67f036c0efb7fb98ff4a`;
- Q86B qimpl `question_impl.phase0.2fb3a62609dad4c1306d`;
- Q86A current source structure `cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4`;
- Q86B remains exact current Afrobarometer R5 source-structure grain.

Numeric source values remain identities only. No order or metric semantics are added.

## Authority / target-use law

Before constituting the query, B requires the supplied exact query authority to be positive `PREDICATE_GRAMMAR` authority for the named operation over:

- `EmpiricalPredicate@1.0.0`;
- `EmpiricalQuerySpec@1.0.0`;
- `EmpiricalFact@1.0.0`.

Target-use authority is separately required as exact positive `TARGET_USE_PERMISSION` for the supplied exact target-use ref and operation.

The target-use ref, target-use authority ref, operation and permission ceiling are included in query semantic identity without pretending that target-use permission is itself the I03 predicate grammar authority.

## Typed-negative preservation

B does not reinterpret current I03 results.

`execute_gt12b_i03_plan(...)` returns current I03 `EmpiricalFact` states unchanged and asserts only the existing PRE553 zero actor/V3/V2-effect invariant.

Thus lawful I03 states such as `UNAVAILABLE`, `NONCOMPARABLE`, `VALID_EMPTY`, `ZERO_SUPPORT`, `ZERO_OVERLAP` or `INTEGRITY_FAILURE` are not promoted to positive support.

## Deterministic replay

`replay_gt12b_i03_execution(...)` calls current `replay_empirical_query(...)` with the first execution's exact fact refs and fails closed if the replay result differs.

## Focused tests

Added:

`rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py`

Coverage includes:

- exact production frozen literals;
- lawful current I03 fixture -> positive GT1 unary `EmpiricalFact`;
- lawful current I03 fixture -> positive GT2 joint `EmpiricalFact`;
- frozen GT2 target order `[Q86B, Q86A]`;
- deterministic replay for both operations;
- source-native domain tamper fail-closed;
- risk-set ref tamper fail-closed;
- unequal Q86A/Q86B routing member sets fail-closed;
- missing exact query authority fail-closed;
- disappearance of target source authority after plan construction preserves current I03 `UNAVAILABLE`;
- GT1 permission-ceiling widening fail-closed.

The positive test fixture is explicitly nonauthoritative and small. It monkeypatches only the production source/risk literal constants inside the test so the current I03 mechanics can be exercised without fabricating a release that falsely claims to contain the real R5 bytes. Separate tests pin the actual production literals exactly.

## Execution evidence

Repository pytest was not executed by this worker: the connected GitHub surface provides repository read/write operations but no synchronous checkout executor, and the local container has no network-accessible repository checkout.

Local syntax compilation was performed successfully for the new module and focused test file. This is syntax evidence only, not pytest evidence.

Central fan-in must integrate the exact GT12-A validated release/domain/authority producer and run the focused test plus the required smallest inherited I03/source-backed regression subset in the real checkout execution environment.

## Changed files

1. `rawlsing_next/wave1_gt12_i03_positive_facts.py`
2. `rawlsing_next/tests/test_wave1_gt12_i03_positive_facts.py`
3. `data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/GT1_GT2_IMPLEMENTATION_WAVE_R1/B_I03_POSITIVE_FACTS_R1/00_RETURN.md`

No current I03 engine file was modified.
No structural admission, FIELD FORGE, M1/M4/M5, V3, V2, serving, persistence or physical-architecture semantics were changed.

Terminal:

`PASS__GT12B_I03_POSITIVE_FACT_EXECUTION_READY_FOR_CENTRAL_INTEGRATION`
