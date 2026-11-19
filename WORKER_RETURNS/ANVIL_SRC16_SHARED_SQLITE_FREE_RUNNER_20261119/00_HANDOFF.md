# SRC16 native mapping — age refusal and bounded gap census

## Finding

The admitted native run at `3d63d416e9ed…` refused before publish with:

```json
{"code":"UNBOUND_RESPONSE_CELL","detail":{"row":1,"slot":[11,"age"]}}
```

The pinned config has an `age` response slot whose configured substantive value
set is only `89 = 89 or older`.  Its other 13 values are typed missing/special
codes.  The existing `GSS1972-codebook.csv` likewise gives only
`response_options_substantive = "89 = 89 or older"` and does not state the
ordinary age range.  Therefore the ordinary age tokens at physical ordinal 11
are not inferable from the pinned config/codebook alone.  Adding a guessed
`18..88` range or accepting arbitrary numeric codes would be semantic invention
and is not done.

The `.sav` was not modified.  No source was opened by this worker.

## One bounded precheck correction

`common/sqlite_free_single_pass.py` now invokes
`common/mapped_slot_precheck.py` **once after exact decode and before spool or
projection**.  It aggregates unresolved physical tokens for every mapped
response/coordinate/weight slot, plus missing and duplicate mapped cells, and
refuses with `UNBOUND_MAPPED_SLOTS` containing the whole aggregate report.
This prevents repeated full runs that would stop at age first.

The sourcefree path was re-run through the actual common supervisor after the
change: `COMPLETE`, producer/reader exit 0, distinct child PIDs `84780`/`84791`,
6 rows, no SQLite.  `copy_observed_raw` coordinate handling is respected.

Synthetic yes/no witness (`synthetic_mapping_witness.out`):

- pinned config file `1106de3e…`;
- configured age values: 14;
- `89` bound: yes;
- typed missing `-99`, `-98`, system missing: bound: yes;
- ordinary `18` unresolved: yes;
- arbitrary code `3` not made valid: yes;
- one precheck collected `18` and `30` together: yes;
- no respondent rows emitted and no source read.

## Exact missing evidence: one controller census

The worker cannot run the source.  The owner/controller can run this one bounded
census under the **existing exact SRC16 construction grant**, using the existing
profile and resolver, without any new grant or wider scope:

```bash
PYTHONPATH="$PRIVATE_CANDIDATE_TREE:$RETURN/common" \
PYTHONDONTWRITEBYTECODE=1 \
python3 -B "$RETURN/common/gap_census.py" \
  --profile "$PRIVATE_SRC16_PROFILE" \
  --out "$PRIVATE_GAP_CENSUS_JSON" \
  --controller-run
```

`$PRIVATE_SRC16_PROFILE` is the existing exact SRC16 profile containing
`binding_dir`, `config`, and `source_path`.  The script:

1. loads the pinned config and exact current resolver;
2. verifies config file SHA `1106de3e…`, canonical SHA `c26e8e71…`, source SHA
   `e368fc0f…`, currentness and revocation;
3. performs one bounded physical pass;
4. writes only aggregate per-slot unresolved tokens/counts, missing/duplicate
   slot counts, and no respondent rows, identity keys, source bytes, or
   decoded response table.

The output must remain local/private, not Git.  It collects all mapped-slot
unresolved coverage at once, not just age.

## Exact repair content after census

The exact repair is to add, for each **observed** unresolved age token returned
by the census, a rule with the original token and physical state:

```json
{
  "raw_value": "<observed decoded age token>",
  "missing_state": "OBSERVED_STORAGE_VALUE",
  "source_missing_declaration": null,
  "response_state": "SUBSTANTIVE_RESPONSE",
  "occurrences": "<copy the existing age scalar occurrence exactly>",
  "canonical_value": null,
  "transform_authority_ref": null,
  "extra_authority_refs": []
}
```

Only tokens actually observed in the exact source are added.  Unobserved
arbitrary codes remain unbound.  No canonical recoding, range invention,
category invention, or field discard is performed.  Other unresolved slots in
the census are reported together and must be adjudicated from their own exact
codebook evidence; they are not silently coerced.

This worker has not mutated the pinned config or published an override because
the census tokens have not been supplied.  That census output is the exact
missing evidence required to finish the age construction mapping.

## Metadata-only agreement

`generic_cli.py --mode src16-metadata` still passes through the actual source
adapter:

- source SHA `e368fc0f…`;
- config file `1106de3e…`, canonical `c26e8e71…`;
- 1,613 rows / 216 physical / 157 response / 2 coordinates / 0 weights;
- `CURRENT_GRANTED`, no revocation;
- other-source, analysis-purpose and incorrect-scope cases refused with
  `EXACT_REQUEST_MISMATCH`;
- `source_read_performed: false`.

## Residual / scope

- Native SRC16 remains **READY-INPUT, NOT RERUN**.
- Exact age mapping remains blocked only on the aggregate census token set.
- No new wave, Q2/science, protected write, runner redesign beyond the bounded
  aggregate precheck, alternate lifecycle, or DHIKR was added.
- Source config and authorization identity remain pinned; `.sav` unchanged.

## Files

- `common/mapped_slot_precheck.py`
- `common/gap_census.py`
- `common/synthetic_mapping_witness.py`
- `common/sqlite_free_single_pass.py`
- `common/sqlite_free_witness.py`
- `sourcefree_precheck_test.out`
- `sourcefree_precheck_receipts.json`
- `synthetic_mapping_witness.out`
- `src16_metadata_mapping_repair.out`
- `src16_denial.out`
- `receipt.json`
