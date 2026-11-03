# SRC04 certified-refusal recheck — exact ddc85dd29

**Candidate:** `ddc85dd298d36d4825d42cd4931a0cac5d91cb73`  
**Review start:** `ad205744c288acc8b4c0dadb1fb4607c38c74fd0`  
**Mode:** TEST_ONLY sourcefree metadata/aggregate review; no original respondent read.

## Verdict

**`PASS_SCOPED`**

- 28 certified fields changed; 14 uncertified fields held unchanged.
- Existing source-configuration schema validation: **valid**.
- All 42 per-field source-record denominators are exactly 7337 and all
  old/corrected field identities conserve.
- Aggregate correction is exactly **2185 field responses**.
- q101 remains exactly: **7129 valid / 204 explicit nonresponse / 4 missing /
  7337 total**.
- Routing remains `ROUTING_UNKNOWN` for 42/42 with 42 unresolved risk sets.
- The aggregate is **field-response observations, not unique people**.

## Replay

Candidate correction receipt and overlay are byte-identical to the exact
disposable-snapshot replay:

- Receipt: `cee52e2f9537e6ce0ad3bfe0e331f86c3dffdb0f642f882702a0308a689b162c`
- Overlay: `997e29662f44beb8f345925b9189a251fa391ccc44bd4fe3045ed4b620eb5eb5`
- Focused tests: **5 passed** in 0.03s

The script reads only metadata, the accepted aggregate tally, the prior exact
allowlist, and routing metadata. It does not open the SRC04 SAV.

## 28 certified / 14 held

- Selected fields: **42**
- Certified overlay entries: **28** (q101 + 27 additional)
- Held entries: **14**
- Overlay held entries: **14**
- Only certified entries changed: **true**
- Held entries changed: **false**
- Universal code-99 rule: **false**
- Production config adopted: **false**

Held fields, all still `SUBSTANTIVE_RESPONSE`:

`q202, q207, q210, q212, q216, q222, q224, q226, q227, q228, q2301, q2302, q2311, q2312`

Each held field was checked against the source config after the overlay; its
code-99 state and canonical value are unchanged. The exact per-item certified
fields and held fields are in `evidence/CERTIFIED_ENTRIES.csv` and
`evidence/HELD_ENTRIES.csv`.

## q101 exact prior correction

- Prior q101 correction receipt:
  `399fa2a71a49cff8ada8cff4f9d1118f2ab2a3edf64b47d23726751014053d86`
- Old q101: `7162 valid / 171 explicit`
- Corrected q101: `7129 valid / 204 explicit` (`171 DK + 33 refusals`)
- Missing: `4`
- Total: `7337`
- Candidate q101 row matches the prior correction exactly.

## Per-field and aggregate denominators

Every selected field:

- `source_record_denominator = 7337`
- old `valid + explicit + missing = 7337`
- corrected certified/held identity `valid + explicit + missing = 7337`

All 42 per-field rows are in `evidence/PER_FIELD_DENOMINATORS.csv`.

Aggregate old / corrected:

| Measure | Old | Corrected |
|---|---:|---:|
| Valid answer | 277582 | **275397** |
| Explicit nonresponse | 21237 | **23422** |
| Refusal from certified code-99 | 0 | **2185** |
| Missing or unobserved | 9335 | 9335 |
| Observed response | 298819 | 298819 |
| Source-record denominator | 308154 | 308154 |

Identity:

```text
275397 + 23422 + 9335 = 308154
```

The correction moves exactly `2185` certified code-99 field responses from
substantive to refusal. The 14 held fields contribute `1645` code-99 counts that
remain substantive; total selected code-99 observations are `3830`.

## No unique-person interpretation

The aggregate is **42 field-response denominators over the same 7337-source-row
universe**:

```text
42 * 7337 = 308154 field-response records
```

- `308154` is not a unique-person count.
- `2185` is a field-response reclassification count across 28 fields, not a
  unique-person count.
- No deduplication was performed or needed for the field-response arithmetic.
- Candidate receipt/overlay/return contain no unique-people/unique-respondents
  claim; `unique_people_claimed=false`, `unique_people_count=null`.
- The same 7337 interview rows are represented once per selected field; they
  must not be summed as distinct people.

## Schema validation

The independent check reconstructs the corrected configuration from the exact
28 overlay entries and calls the existing owner:

`rawlsing_next.source_configuration.schema.validate_source_config`

Result: **valid**. The changed question set is exactly the 28 certified fields;
all 14 held fields remain byte-equivalent at their code-99 state/canonical value.

## Routing

- `ROUTING_UNKNOWN`
- 42/42 selected routing entries unknown
- 42/42 risk-set refs unresolved
- 0 exact skip rules
- accepted routing binding: **false**
- eligibility/denominator binding: **false**
- routing preserved: **true**

No routing or denominator was inferred from response counts.

## Exact files / commands

- `evidence/CHECKS.json`: complete replay, partition, per-field, aggregate,
  schema, record-scope and routing evidence.
- `evidence/REPLAYED_CERTIFIED_RECEIPT.json`: cee52e…
- `evidence/REPLAYED_CERTIFIED_OVERLAY.json`: 997e29…
- `evidence/PER_FIELD_DENOMINATORS.csv`: 42 rows.
- `evidence/CERTIFIED_ENTRIES.csv`: 28 rows.
- `evidence/HELD_ENTRIES.csv`: 14 rows.

Commands:

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007 \
  archive ddc85dd29 rawlsing_next \
  WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/certified-refusal-fix \
  WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/routing \
  | tar -x -C <snapshot>
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007 \
  archive 056849e23 rawlsing_next/source_configuration \
  rawlsing_next/pre553_source_read_admission.py source_pre553_validation/SRC04 \
  | tar -x -C <snapshot>

PYTHONPATH=<snapshot> python3 -B \
  <snapshot>/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/certified-refusal-fix/certified_refusal_fix.py \
  --package-root <snapshot> ... \
  --output <review>/evidence/REPLAYED_CERTIFIED_RECEIPT.json \
  --overlay <review>/evidence/REPLAYED_CERTIFIED_OVERLAY.json

PYTHONPATH=<snapshot> python3 -B -m pytest \
  <snapshot>/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/certified-refusal-fix/test_certified_fix.py \
  -q -o addopts='' -p no:cacheprovider

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 \
  WORKER_RETURNS/PYAT-REAL-METADATA-INDEPENDENT-REVIEW/certified-refusal-recheck/check_certified_refusal.py
```

## Scope

Metadata and retained aggregate counts only. No original SAV/DTA or respondent
rows were read; no original workload, new authority, source execution,
production edit, production config adoption, merge, CI or adoption was made.
Only
`WORKER_RETURNS/PYAT-REAL-METADATA-INDEPENDENT-REVIEW/certified-refusal-recheck/**`
was written.
