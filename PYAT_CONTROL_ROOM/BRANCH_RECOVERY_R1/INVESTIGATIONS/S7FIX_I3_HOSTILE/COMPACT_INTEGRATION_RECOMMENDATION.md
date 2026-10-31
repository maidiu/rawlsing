# Compact integration recommendation

## Decision

**Do not merge the S7-FIX 47 MB artifact or any historical nested-owner code into
production.** Keep the six historical boundary corrections and negative custody.
Correct the current-ownership fields before any current ABI claim. No duplicate
47 MB artifact was created by this review.

## Corrections required in the S7-FIX mapping

1. **Nested owners are historical-only.** For every nested
   `_make_sealed_source_relation_owner.SourceRelationResolver` member, replace
   `current_implementation_candidate = ...SourceRelationResolver.<method>` with:
   - `current_implementation_candidate: null`
   - `current_receiver_status: NO_CURRENT_NESTED_OWNER__HISTORICAL_ONLY`
   - `current_receiver_or_unknown: []`

   The current source has no nested owner. Mapping nested defects to the current
   outer class is the outer/nested conflation this court rejects.

2. **S5 outer current rows are not exact AST.** The five S5 outer rows claim
   `EXACT_AST_SAME_PATH`, but the current outer method ASTs differ from the
   historical S4 outer ASTs. Replace with:
   - `CURRENT_PATH_SYMBOL_ONLY__AST_DIFFERENT__BEHAVIORAL_EQUIVALENCE_NOT_CLAIMED`
   - keep the historical AST/blob as the identity source, not the current bytes.

3. **First-consumer evidence is stale for source relations.**
   `rawlsing_next/pre553_temporal_comparability.py` is absent. The current source
   relations consumer is test-only, plus a string map in
   `fiabc_succession_producer.py:59`. Replace current-first-consumer claims with
   `HISTORICAL_FIRST_CONSUMER_ONLY__CURRENT_PATH_ABSENT` and
   `CURRENT_EXECUTED_CONSUMER=TEST_ONLY`.

4. **Historical emit join is not current emit.** Keep the join
   `S7FAM-41da3f505673271b` for the four historical variants with AST
   `4f7cd7cc...`. Record current `pre553_physical_decoder.py` blob
   `8732e34d...` as:
   - `CURRENT_PR526_DIFFERENT_AST__77d9be6c...`
   - `CURRENT_PR526_TESTS_PASS_AT_TEST_SCOPE`
   - `BEHAVIORAL_EQUIVALENCE=NOT_CLAIMED`.

5. **Preserve negative custody unchanged.** Nested F7/P07 defects
   (`_validate_positive`, `decide`, `resolve_exact`) stay under nested families.
   Nested `__init__` stays review/revise; nested `require` stays
   positive-author-only. Outer S5 rows stay contextual-only. Do not reattribute
   nested F7/P07 findings to outer `SourceRelationResolver`.

6. **Preserve HQ240/HQ245–HQ248.** Keep them as historical source/review findings.
   Do not compile or execute the native C attacks; no source/actor grant exists.

## Current consumer truth

- `pre553_source_relations.py`: no production import; only
  `tests/test_pre553_source_relations.py` imports it. This is **test-only**.
- `pre553_physical_decoder.py`: production static import sites exist; current
  tests execute `materialize_native_preimages -> iter_cells -> iter_batches ->
  emit`. This is current PR526 behavior, not historical emit equivalence.
- Current sourcefree tests actually run:
  - `test_pre553_source_relations.py`: 24 passed.
  - `test_universal_source_byte_custody.py`: 26 passed.
  - `test_universal_source_projection.py`: 31 passed.
  - `test_pre553_sr06_decoder_carrier.py`: 16 passed, 1 skipped.
- **No production whole-service consumer was executed.**

## If the owner wants current source-relations integration

1. Name an actual production consumer and call path.
2. Either port/implement a current nested sealed owner with exact tests, or
   explicitly retire the nested historical owner and keep its defects historical.
3. Add current positive and fault-negative tests for the chosen ABI:
   - alias/provenance substitution;
   - conflicting positive/denied relation;
   - exact historical authority ref;
   - reversal/refusal;
   - current nested/outer authority separation.
4. Do not use AST equality as behavioral or scientific acceptance.
5. Do not transplant the old artifact or 47 MB receiver.

## If the owner keeps historical-only

1. Keep the six family corrections and negative custody.
2. Mark all nested current ownership `HISTORICAL_ONLY`.
3. Mark source relations current consumer `TEST_ONLY`.
4. Keep current decoder PR526 tests and do not equate them with historical emit.
5. Route F7/P07 and native findings to the original U/E/source owner.

## Verification sequence

```bash
# Historical membership and negative custody
python3 /tmp/opencode/s7fix-i3/validator.py \
  --dir <S7-FIX-artifact-dir> --json
python3 /tmp/opencode/s7fix-i3/validator.py \
  --dir <S7-FIX-artifact-dir> --self-test

# Current sourcefree tests
PYTHONPATH=. python3 -m pytest -q -p no:cacheprovider \
  rawlsing_next/tests/test_pre553_source_relations.py \
  rawlsing_next/tests/test_universal_source_byte_custody.py \
  rawlsing_next/tests/test_universal_source_projection.py \
  rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py
```

Expected current receipts: 24 + 26 + 31 + 16 passed, 1 skipped. These are
sourcefree test-scope results, not production acceptance.

## Rollback

- This review branch changes only the investigation directory. Delete/leave
  unmerged; no production source or PRE-MAIN change.
- The S7-FIX artifact remains on its own branch. Do not copy or duplicate it.
- If a current owner mapping was edited in future, revert that edit and re-run
  the validator and current sourcefree tests.
- No production merge is recommended.

## Final recommendation

`KEEP_HISTORICAL_SIX_BOUNDARIES__FIX_CURRENT_OWNERSHIP_CONFLATION__HOLD_SOURCE_RELATIONS_CURRENT_ABI__KEEP_CURRENT_PR526_TESTS__NO_MERGE__NO_47MB_DUPLICATION`.
