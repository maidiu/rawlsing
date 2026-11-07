# T03 - FROZEN FIELD FORGE ALTERNATE PAIR REACHABILITY

## Reachability evidence
Production search over `rawlsing_next` excluding tests and bytecode found only:
- `field_forge_conditional_support.py:467` definition and `:588` replay wrapper calling the same frozen producer.
- `gt12_c_to_d_relation_bridge.py:5,32,93,131-137` bridge definition and calls, with `producer_function` naming the same producer.
- No production import or caller of the producer/bridge outside those definitions.

All actual calls found are in tests or the test harness:
- `rawlsing_next/tests/gt12_e2b_actual_object_consumer_harness.py:281,291`
- `rawlsing_next/tests/test_gt12_e2b_actual_object_consumer_harness.py:290,298`
- `rawlsing_next/tests/test_field_forge_conditional_support.py`
- `rawlsing_next/tests/test_gt12_closure_b_c_to_d_bridge.py`
- `rawlsing_next/tests/test_pre553_gt2_structural_positive_realization_court.py`

The production-like path in `wave1_gt12_i03_positive_facts.py:469-527,646-714` uses the frozen Q86A/Q86B execution binding and frozen target-use guards; it does not call `produce_exact_conditional_support_profile` for an arbitrary pair, and it does not provide a generic alternate caller.

## Direct synthetic falsifier
A proper synthetic same-risk two-target joint fact/query was built from the Field Forge test fixture with refs changed consistently to `Q99B`/`Q99A`. The producer still emitted literal roles:

- `CONDITIONER`: `source_native_variable = Q86B`, ref `urn:test:i03:question:Q99B`
- `TARGET`: `source_native_variable = Q86A`, ref `urn:test:i03:question:Q99A`

`bridge.admit_gt12_c_relation` returned `ADMITTED` with participants:
- `CONDITIONER / Q86B / urn:test:...:Q99B`
- `TARGET / Q86A / urn:test:...:Q99A`

The bridge check at `gt12_c_to_d_relation_bridge.py:78-79` validates only the literal Q86B/Q86A labels and separately checks that participant refs equal the relation's own refs. It does not prove the refs are the Q86 pair. Baseline Q86 relation was also `ADMITTED`; cold restore reproduced the baseline relation ref.

## Verdict
`NO_ALTERNATE_CALLER__FROZEN_FIRST_READER_CLOSURE__NO_PRESENT_DEFECT`.

The direct-call mislabel is a latent producer invariant gap, not a current production-reachable defect. Do not genericize Field Forge or change its frozen role semantics in this commission. If a future caller needs an alternate pair, that requires a separate code-owning commission to make the role/source invariant exact (reject non-Q86 refs or bind the refs to their native variable identity) with independent review.
