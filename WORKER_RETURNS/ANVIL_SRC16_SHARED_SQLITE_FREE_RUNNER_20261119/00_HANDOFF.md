# SRC16 shared SQLite-free runner injection

## Verdict

**Sourcefree keyed path: PASS.** **SRC16 metadata admission/refusal: PASS.**
**Native SRC16 source launch: READY-INPUT / EXACT BLOCKER — not executed.**

No original source bytes were opened. No private path, config value or grant
bytes are published here.

## Shared operator injection

`generic_cli.py` is an executable packaged successor over the existing shared
operator at `MEASUREMENT_PREP@1f8b61b8…`:

- `sourcefree` calls the existing shared `build_single_pass` and
  `open_stream_native_estate` (no separate GSS writer).
- `src16-metadata` loads the exact SRC16 config through the current parser and
  the exact existing private resolver; it performs metadata-only admission and
  negative cases.
- `src16-run` is the owner-only source injection path. It refuses before source
  I/O because the exact SRC16 config declares a source-native key slot and the
  shared single-pass builder does not yet pass same-decode `row_native_keys`
  into its projection.

The sourcefree keyed test injects derived keys from the same generated fixture
decode into the existing projection, not a new writer.

## Safe sourcefree keyed evidence

```json
{"status":"SOURCEFREE_KEYED_PASS","keyed":true,
 "family_counts":{"EmpiricalUniverse":1,"RespondentIdentity":6,
 "QuestionVariableBinding":1,"RespondentEvent":6,
 "RoutingEligibilityFact":6,"EmpiricalCoordinateFact":6,
 "WeightMeasureFact":0,"AuthoritySnapshot":7,
 "SourceUniverseRelation":0,"EmpiricalPredicateReplayBinding":0,
 "ComparatorReplayBinding":0,"DiscoveryBranchReplayBinding":0,
 "StructuralAdmissionReplayBinding":0},
 "proof_schema":"ANVIL_STREAM_C11_ESTATE@1",
 "sqlite_present":false,
 "progress_phases":["checkpoint_ready","stream_start","family_written",
 "footers_verified","published","reopened_validation"],
 "source_read":false}
```

The actual CLI performed normal build and fresh native reopen. No `.sqlite`
artifact was present. Existing caps/progress path was used unchanged.

## SRC16 metadata-only admission

Exact pinned config:

- source: `SRC16`, `GSS1972.sav`
- source SHA-256: `e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204`
- config file SHA-256: `1106de3e086032f5ac0b26fee0b56a147722399c80ac2841b70f0b851dea93b7`
- config canonical SHA-256: `c26e8e71afbc629a9f19708cedb7b38cc2ba3cefb9ac53f11e0608044e64b534`
- shape: 1,613 rows; 216 physical slots; 157 response slots; 2 coordinates;
  0 weights
- purpose/scope: `FULL_SRC16_ORIGINAL_C11_CONSTRUCTION_ONLY` /
  `C11_CONSTRUCTION_ONLY`, `NO_Q2`, `NO_SEMANTIC_ADOPTION`
- currentness: `CURRENT_GRANTED`; revocation: none
- source read performed: **false**

Metadata admission result: `SRC16_METADATA_ADMISSION_PASS`.

Negative refusal cases all pass without source read:
`other_source`, `analysis_purpose`, `incorrect_scope` →
`EXACT_REQUEST_MISMATCH`.

Grant hash is retained as metadata; grant bytes and private paths are not
published.

## Exact native blocker

`src16-run` refuses before source:

`SRC16_KEY_SLOT_REQUIRES_SAME_DECODE_ROW_NATIVE_KEYS_IN_SHARED_BUILD:
respondents.source_native_key_slot`

This is the existing shared single-pass field-proof gap, not a new SRC16 grant,
config or scientific issue. The existing resolution is
`row_native_keys_from_transport` over the same admitted decode; it must be
passed through the shared build path before a real SRC16 launch. No blanket
re-audit was performed.

## Exact owner launch form (not executed)

Environment values are supplied privately by the owner; no private paths are
published here.

```bash
ANVIL_CANDIDATE_TREE="$PRIVATE_CANDIDATE_TREE" \
ANVIL_SRC16_GRANT_DIR="$PRIVATE_SRC16_GRANT_DIR" \
ANVIL_SRC16_CONFIG="$PRIVATE_SRC16_CONFIG" \
ANVIL_SRC16_SOURCE_PATH="$PRIVATE_EXACT_SRC16_SOURCE" \
PYTHONPATH="$PRIVATE_CANDIDATE_TREE:$SHARED_OPERATOR_DIR:$RETURN_DIR" \
python3 generic_cli.py --mode src16-run --root "$PRIVATE_WORK_ROOT"
```

This is not ready to launch until the key-slot pass-through is added to the
same shared build path.

## Files

- `generic_cli.py`
- `sourcefree_test.out`
- `src16_metadata_test.out`
- `src16_run_refusal.out`
- `receipt.json`

No source bytes, respondent payload, config values, grant bytes, private paths,
product, protected refs, Q2/science, or other-wave authority were added or
changed.
