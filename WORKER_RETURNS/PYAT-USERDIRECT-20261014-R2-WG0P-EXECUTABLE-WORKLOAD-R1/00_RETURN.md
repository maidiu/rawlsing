# R2 WG0P — Executable Original-Item Workload Return

**Branch:** `agent/userdirect-pyat-20261014-r2-wg0p-executable-workload-r1`
**Sealed startup:** `b183146c52b91bf5dc88d75ada034be097f0b20f`
**Predecessor WG0:** `5e11d186a5ccd74faa13687adafda3942834a475`

## Conceptual defects corrected

1. **PRODUCED label is not a produced result.** Only `BatchExecutionRunner` COMPLETED receipts count as results. Dispositions remain pre-result; `test_produced_label_is_not_produced_result` asserts no receipt/result attributes on candidates.
2. **Self-counted oracle is not independent coverage.** `oracle_eligible_operations()` is frozen independently of `WorkloadBuilder.enumerate()`; `test_independent_oracle_matches_builder_exactly` requires exact set equality including reasons.
3. **Same unit is not same person.** Conditioning requires same unit + same wave + same source. Cross-wave, cross-source, and cross-unit pairs are recorded INADMISSIBLE with exact reasons, never dropped, never conditioned.
4. **Fixture authority is not a license.** `authority_ref` is the typed hold `HELD_PENDING_SOURCE_ISSUER`, never a grant.

## Independent oracle

Five invented fixture items (ordinal respondent, household multiple-response, routed without evidence, withdrawn-grant ordinal, second-wave ordinal). Oracle enumerates marginals plus same-person conditionals plus inadmissible cross pairs. Builder output matches exactly (op_id, disposition, reason).

## Real owner execution

- `BatchExecutionRunner` imported from `rawlsing_next/pre553_batch_runner.py` (blob `2d291600b9a10c56d9c6f6de7f7d619f6c52e829`).
- `ExactRef`/`semantic_hash` from `rawlsing_next/pre553_empirical_objects.py` (blob `a61365b994e5c3c50de0f598fcf40e90abf757b6`).
- `C11Repository` from `rawlsing_next/pre553_c11_repository.py` (blob `67c6eb6494522cd11aab1b93d0e73f9cef6036f3`).
- Release refs are opaque test-harness occupants (no C11 semantics claimed), mirroring the accepted owner test pattern.
- Executor computes exact `Fraction` values per unit; receipts are COMPLETED with `execution_performed=True`; summary reaches `FULL_MANIFEST_COVERAGE`.

## Numeric consumer evidence

- Changed input (9/16 to 5/8 on one unit) changes that unit's result ref; all other units stable.
- Identical re-run produces identical receipt hashes.
- Zero numerator (0/16) and minority (1/16) complete normally as results.

## Frontier, sharding, resume, revoke

- Frontier freeze blocks post-hoc additions.
- `max_units=1` leaves `INCOMPLETE_MANIFEST_COVERAGE` with exact pending set; prior receipts resume to `FULL_MANIFEST_COVERAGE`.
- Revoking SRC-B leaves W1 marginals unchanged.

## Tests: 14/14 PASS

`python3 -m pytest WORKER_RETURNS/PYAT-USERDIRECT-20261014-R2-WG0P-EXECUTABLE-WORKLOAD-R1/repro/test_wg0p_executable_workload.py -v` -- exit 0.

## Ceilings

- Invented fixtures with source-custody HOLD. Not 35 waves, not 1,890 cells, not N11.
- No raw survey, no canonical/owner changes, no V3.
- Next authorization: exact source/E/model issuer grant for real source metadata.

## Terminal

`R2_WG0P_EXECUTABLE_WORKLOAD_REAL_BATCH_RUN__14_TESTS_PASS__NO_ALL35_CLAIM__AWAITING_INDEPENDENT_REVIEW`
