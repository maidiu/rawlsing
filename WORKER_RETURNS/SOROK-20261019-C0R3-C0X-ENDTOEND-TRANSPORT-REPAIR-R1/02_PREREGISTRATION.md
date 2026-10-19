# C0R3 prospective test preregistration

**Status:** frozen design for the corrected two-owner transport and C10 receiving court. This file is written before the final selected execution. The inherited C0R2 `or True` test remains byte-exact and is not counted as proof.

**Scope:** `TEST_ONLY_SOURCEFREE`; no Pyat producer edit, no new probability, no actor, no C11 weld.

## Claims and oracles

| Claim ID | Actual consumer | Positive oracle |
|---|---|---|
| `C0R3_E2E_N9_TRANSPORT` | corrected C0P facade → corrected C0X receiver | complete 17-field `GENERIC_WORLD_SELECTION@1.0.0`; 5 selection records, 5 payloads; lossless JSON; genuine `values_read` |
| `C0R3_E2E_N10_TRANSPORT` | corrected C0P facade → corrected C0X receiver | complete 20-field `GENERIC_ORDERED_POSSIBILITY@1.0.0`; 3 ordered steps; exact materialized parent refs; lossless JSON |
| `C0R3_E2E_RELOCATION` | relocated corrected facade over the same actual native runtime | relocated `module.__file__`; actual `RUNTIME`; both producer source identities; identical owner hashes/JSON; deterministic |
| `C0R3_E2E_TYPED_TEMPORAL` | pre-publication unavailable clock | typed `TEMPORAL_SOURCE_REF_UNAVAILABLE_AT_ASOF`, no receipt and no positive; every missing field named |
| `C0R3_E2E_PROVIDER_SWAP` | actual provider replacement | `PARTIAL`; training `BLOCKED_BY_MODELED_RULE`; civil `ELIGIBLE` |
| `C0R3_E2E_REVOCATION` | actual `training_access` revocation | `PARTIAL`; training `UNAVAILABLE_AUTHORITY_OR_CLOCK`; civil preserved |
| `C0R3_E2E_OWNER_SUBSTITUTION` | wrong owner contract for demand | `OWNER_SUBSTITUTION` |
| `C0R3_E2E_INVALID_PARENT` | non-exact parent ref | `PARENT_RECEIPT_REF_NOT_EXACT` |
| `C0R3_E2E_NO_CHANGE` | identical input twice | exact same owner hashes/JSON; no mutation |
| `C0R3_E2E_COLD` | two fresh child processes | equal complete receipts, transport and JSON payload |

## Claim-specific fault witnesses

| Claim ID | Positive node | Fault | Expected |
|---|---|---|---|
| `C0R3_N9_SELECTION_DRIVES_THE_ACTUAL_C0X_RECEIVER` | `tests/test_c0r3_endtoend.py::test_relocated_candidate_preserves_both_owner_sources_and_json_values` | `"selection": selection,` → `"selection": [],` in corrected facade | same test fails by its selection assertion |
| `C0R3_N10_ORDERED_STEPS_DRIVE_THE_ACTUAL_C0X_RECEIVER` | same relocation test | `"ordered_steps": steps,` → `"ordered_steps": [],` | same test fails by its ordered-step assertion |
| `C0R3_ROOT_PARENT_REF_IS_MATERIALIZED_NOT_CALLABLE` | `tests/test_c0r3_endtoend.py::test_corrected_parent_ref_is_materialized_exact_ref` | root parent ref materialization → `None` | same test fails by exact-parent assertion |

The original C0R2 test `test_r1_relocation_changes_no_consumer_value` ends in literal `or True` at line 72. It is copied byte-exact from `55d2daa…` and its green is never counted as proof. The new relocation test replaces its evidentiary role.

## Pre-freeze harness corrections (disclosed)

Before this freeze, the first implementation runs exposed two test-harness expectation errors, not candidate defects:
- the ordered-step parent hash is the previous native empirical step hash (stored in the previous step's `new_binding.hash`), not a hash of the full ordered-step envelope;
- the N10 source identity is carried in the facade lineage `producer_blob`/`producer`, not a `repository_refs` field on the 20-field possibility envelope.

Both were corrected in the test only. No claim, oracle, owner contract, native source or fault was redefined after observing candidate output.

## Authority ceiling

The only expected REDs are the inherited C0I three on the original facade, the inherited C0X transport HOLD on the original receiver, the byte-exact C0R2 vacuous test (not trusted), and the original callable-parent defect. The corrected candidate must be green on these prospective claims without any fabricated source, rule, actor or probability.
