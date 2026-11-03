# SRC04 decline-code recheck — exact 1110093f3

**Candidate:** `1110093f324fe591246c56bf8f2e742a57c9201e`  
**Review start:** `9d3d42984f37c01129e47d3dd5570608972cafba`  
**Metadata origin:** `056849e23a83d7f4fa33fe4dc8eb65eaf7e2a102`  
**Mode:** TEST_ONLY sourcefree metadata/aggregate review; no original respondent read.

## Verdict

**`PASS_SCOPED`** for the q101 code-99 correction.

- Candidate q101 correction replays exactly:
  **7129 valid / 204 explicit nonresponse / 4 missing / 7337 total**.
- Explicit nonresponse is **171 DK + 33 refusals**; observed response remains 7333.
- The 33 code-99 q101 responses are exactly the delta from the old
  `7162 / 171` values.
- The q101 overlay changes only q101 code 99 from
  `SUBSTANTIVE_RESPONSE`/canonical `"99"` to `REFUSAL`/null, with
  `production_config_adopted=false`.
- Routing remains `ROUTING_UNKNOWN` for all 42 selected fields; 42 unresolved
  risk-set refs; 0 exact skip rules. No routing was inferred.

The wider code-99 result is split by exact per-item authority status:

- **42/42 selected fields are field-level inconsistent**: each exact W1
  option-authority row for code 99 says `decline to answer`,
  `option_group=special`, `is_substantive=False`, `is_refusal=True`,
  `is_missing=True`, `response_kind=special_missing`; each source-config slot
  maps code 99 to `SUBSTANTIVE_RESPONSE`.
- **28/42 are certified correction allowlist**: 28 exact rows have
  `response_semantics_status=certified`. This includes q101 and 27 other fields.
- **14/42 are typed unknown for correction**: their exact rows have
  `response_semantics_status=preserved_not_certified`; the code-99 label and
  flags are exact, but certification is absent. They are not silently
  allowlisted and q101 semantics are not generalized to them.

The 14 typed-unknown fields are:

`q202, q207, q210, q212, q216, q222, q224, q226, q227, q228, q2301, q2302, q2311, q2312`

There are **no missing or ambiguous authority rows**: all 42 selected fields
have exactly one exact W1 `var_name + value_code_numeric=99.0` authority row.
There are no consistent fields in the accepted slice.

## Replay

The candidate correction receipt and overlay are byte-identical to the replay
from the disposable snapshot:

- Correction receipt:
  `399fa2a71a49cff8ada8cff4f9d1118f2ab2a3edf64b47d23726751014053d86`
- Overlay:
  `df5814340b2c98a8db4340a06a1227ee3fbf1a31594a5f35c6b4b62c0a31dcc8`
- Focused tests: **5 passed** in 0.02s
- Replayed aggregate identity:
  `7129 + 204 + 4 = 7337`

Exact q101 authority row:

- `question_id=Arab Barometer:I:q101`
- `wave=I`, `value_code_numeric=99.0`
- `value_label_raw=decline to answer`
- `option_group=special`
- `is_substantive=False`
- `is_refusal=True`
- `is_missing=True`
- `response_kind=special_missing`
- `response_semantics_status=certified`

## Per-item join result

Join keys:

- Source config: `response_slots[].question_id` + value `raw_value=99`
- Option authority: `var_name=qid` + `wave=I` + `canonical_wave=I` +
  `value_code_numeric=99.0`
- Retained tally: `fields[].question_id` + `native_value_counts[].native_value=99`

Results:

| Classification | Count |
|---|---:|
| Selected fields | 42 |
| Exact one-to-one authority rows found | 42 |
| Field-level inconsistent | 42 |
| Other 41 field-level inconsistent | 41 |
| Certified correction allowlist | 28 |
| Other 41 certified correction allowlist | 27 |
| Typed unknown for correction (`preserved_not_certified`) | 14 |
| Missing/ambiguous authority rows | 0 |
| Consistent fields | 0 |

The candidate's `same_mapping_defect_in_selected_metadata` count of 42 is
confirmed at the **source-config field level**, but it is not itself a certified
correction allowlist. Candidate applied only the q101 correction; this review
does not adopt any other correction.

## Routing

- `state=ROUTING_UNKNOWN`
- 42 selected routing entries unknown
- 42 selected risk-set refs unresolved
- 0 exact skip rules
- accepted routing binding: **false**
- eligibility/denominator binding: **false**
- routing corrected: **false**

The q101 response-state correction does not change any routing state.

## Exact evidence files

- `evidence/CHECKS.json`: complete join and aggregate evidence.
- `evidence/FIELD_INCONSISTENCY_ALLOWLIST.csv`: all 42 field-level inconsistent
  entries.
- `evidence/CORRECTION_ALLOWLIST.csv`: 28 certified correction allowlist rows.
- `evidence/TYPED_UNKNOWN.csv`: 14 preserved-not-certified rows.
- `evidence/REPLAYED_CORRECTION_RECEIPT.json`: 399fa2…
- `evidence/REPLAYED_OVERLAY.json`: df5814…
- `evidence/replayed_test.log`: 5 passed.

## Commands

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007 \
  archive 1110093f3 rawlsing_next \
  WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/decline-code-fix \
  WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/routing \
  | tar -x -C <snapshot>
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007 \
  archive 056849e23 rawlsing_next/source_configuration \
  rawlsing_next/pre553_source_read_admission.py source_pre553_validation/SRC04 \
  | tar -x -C <snapshot>

PYTHONPATH=<snapshot> python3 -B \
  <snapshot>/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/decline-code-fix/decline_code_fix.py \
  --package-root <snapshot> ... \
  --output <review>/evidence/REPLAYED_CORRECTION_RECEIPT.json \
  --overlay <review>/evidence/REPLAYED_OVERLAY.json

PYTHONPATH=<snapshot> python3 -B -m pytest \
  <snapshot>/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/decline-code-fix/test_decline_fix.py \
  -q -o addopts='' -p no:cacheprovider

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 \
  WORKER_RETURNS/PYAT-REAL-METADATA-INDEPENDENT-REVIEW/decline-code-recheck/check_decline_allowlist.py
```

## Scope

Metadata and retained aggregate counts only. No original SAV/DTA or respondent
rows were read; no original workload, new authority, source execution,
production edit, production config adoption, merge, CI or adoption was made.
Only `WORKER_RETURNS/PYAT-REAL-METADATA-INDEPENDENT-REVIEW/decline-code-recheck/**`
was written.
