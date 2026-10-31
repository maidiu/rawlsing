# Integration or non-adoption plan — V2K vs current R61

**Decision:** non-adoption/retirement of historical V2K as a current interface. No production merge.

## 1. Retain current R61

- Keep `rawlsing_next/pre553_issued_workload.py` blob `31e84f49...` unchanged.
- Keep `pre553_native_workload_binding.py` blob `dac73e48...` as the current TEST_ONLY builder/first consumer.
- Keep `pre553_source_native_preimage_adapter.py` blob `a6299c1a...`, `GovernedC11Projection` blob `8a761119...`, and current C11/Route B/I03/I05/Batch owners.
- No source/branch merge; current PRE-MAIN remains authoritative.

## 2. Retire historical V2K exact interface

- Do not transplant `V2ExpectedWorkDeclaration`, `v2_bind_semantic_to_dispatch`, `V2DispatchBinding`, `V2ExecutedWorkload`, `v2_execute_through_a04`, `v2_reconcile`, `v2_to_a05_universe`, `OriginalIdentity`, `OriginalExpectedWork`, `FrozenOriginalExpected`, `OwnerScopePlan`, `_validate_original_against_c11` or `run_sourcefree` into current source.
- Keep the historical source/test blobs as evidence references only.
- Close the old V2K exact-identity recovery action as `RETIRED_SUPERSEDED_BY_CURRENT_R61_ENVELOPE`; do not re-add the stranded dependency modules to PRE-MAIN.
- Preserve the current-R61 negative oracle tests as the active negative coverage.

## 3. Current negative oracles

`tests/test_current_r61_contract_negatives.py` (8 passed) exercises:

1. baseline TEST_ONLY admission;
2. foreign issuer/wrong decision;
3. removed held row/expected job multiset;
4. mutated expected-work identity/envelope;
5. wrong role/target-condition direction;
6. replay/prior caller receipts;
7. wrong source edition/source factory;
8. severed current resolver.

These are the current contract's negative boundaries, not historical V2K code.

## 4. Conditions to reopen adaptation

Reopen only if all are true:

1. an original U/E/source owner supplies a competent current receiver that requires the granular V2K original identity fields;
2. the current `GovernedC11Projection` + `NativeWorkload` descriptor cannot carry the required fields without ambiguity;
3. a sourcefree field-by-field adapter can be specified with exact mapping and negative tests;
4. the current R61 `admit`/`execute_issued_workload` consumer can be exercised without inventing source/science/world/actor authority.

If reopened, implement the smallest adapter outside historical module paths, map only the required fields, and rerun the current negative suite plus a new positive current-consumer test. No wholesale transplant.

## 5. No-action conditions

- If no current consumer requires V2K exact identity fields, retirement is complete.
- If the only need is historical scientific comparison, preserve old blobs/tests as evidence under this return; do not integrate.
- If the current R61 contract is sufficient, do not add a new identity module.

## 6. Review and merge

- Independent I3 source and negative-oracle reviewer must inspect exact return SHA and current R61 tests.
- Incumbent Pyat/HQ owns any later adoption/CAS; no self-review.
- No automatic merge, source/science/world/actor grant or PRE-MAIN mutation.
