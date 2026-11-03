# Independent review — PYAT real metadata binding

## Verdict

**REVISE** — the real-metadata projection, exact crosswalk, fixture distinction,
replay and tests pass. The return’s **first-missing classification** is incorrect:
the prior accepted bounded single-SAV SRC04 slice already establishes form/repeat
as null/not-applicable. The first genuinely unresolved source input is the
routing/eligibility and denominator/risk-set handoff.

## Exact candidate and replay

- Candidate: `c8e0215f6f222eb7b09ef0a8d198b23f0780dac2`
- Metadata origin: `agent/pyat-pre553-r157-integration@056849e23`
- Disposable snapshot: c8e0215 worker/rawlsing code plus the pinned R157
  configuration/fixture package.
- Replayed `bind_real_metadata.py` output is byte-identical to the candidate
  `01_REDACTED_RECEIPT.json`:
  `f2f30d55dd3bfe9d284641db39afc8335d19a94c6b8c5cfa42ac0cb68bc50283`
- Replayed focused tests: **4 passed**.

## Positive metadata binding

- Real SRC04 metadata edition: `2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18`
- Rows / columns: `7,337 / 181`
- Config file: `eb4c051ff2845bf3c8c7b5bfee08ea4c9879c7a5264cf1aa6290e3fd457bc900`
- Config canonical: `0e86814b62eb51dc9da22793b6de3e3598c3415632accb80f33bac965185f284`
- Crosswalk: `034d626365249941618d66f6103a557209fce5d95362e3ddf77e29f2fe7fba23`,
  method `EXACT_NAMES`; 181 ordinal/name-exact entries; 181 config items have
  exact crosswalk names.
- Codebook: 181 rows, `8ad1af17…`
- Directionality: 181 rows, `a071c889…` (122 CERTIFIED / 59 NOT_CERTIFIED)
- Option authority: 12,160 rows, `5ef7a0e9…`
- C11 metadata projection: `60206b998f89711801fa689283c20a6589281b77575a5ab002ad7c8cf23a51a8`
- Metadata projection counts: 7,337 respondents, 178 questions, 178 response
  slots, 3 coordinates, 1,305,986 routing facts.
- Original source read: **false**.

## Fixture distinction

The replayed harness also builds the declared nonrespondent fixture release:

- Fixture source: `506d92179dcb76a3b1d5e0710d95472fa20313fcaf8b77cb6f548924c6e5d51b`
- Fixture rows: 8
- Release: `9026fa33bb5739b87b06309f12e1d31fe6fd21fb471237eda870d6d278d47f42`
- Public objects: 2,880

This is clearly distinct from the 7,337-row metadata projection and is not an
original-source empirical result.

## Prior accepted bounded SRC04 slice

Read-only prior artifacts:

- `campaign_a_src04/evidence/RELEASE_RECEIPT.json`
- `campaign_a_src04/evidence/SLICE_SELECTION.json`
- accepted release `fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec`
- selected 42 response slots / 2 coordinate slots

Findings:

- `supported_unit_slice = SOURCE_INTERVIEW_ROW`
- `supported_form_slice = SINGLE_SAV_FILE_NO_FORM_VARIABLE_EVIDENCE`
- The accepted bounded slice is a single SAV, single interview-row shape. R03
  keys with `form_id=None`, `repeat_id=None` are the exact bounded shape; this is
  **not** an estate-wide claim and not a new missing form artifact.
- The accepted slice/receipt explicitly keeps `routing_state = ROUTING_UNKNOWN`;
  the source config has 178 routing entries with 178 `ROUTING_UNKNOWN` states and
  178 unresolved risk-set refs.
- Therefore the first genuinely unresolved source input is exact
  routing/eligibility and denominator/risk-set handoff, not form/repeat.
- The downstream R03 `GrammarPolicy`/authorized direction grant remains absent.

## Reusable artifacts / correction

Reusable: the exact config, crosswalk, codebook, directionality, option authority,
validation results, C11 metadata projection, fixture release, prior accepted
release/slice selection. The metadata return’s `first_missing` should be corrected
to routing/eligibility/risk-set; form/repeat must not be declared absent across
the estate from the metadata package alone.

## Commands

```sh
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007 \
  archive c8e0215f6 rawlsing_next WORKER_RETURNS/PYAT-REAL-METADATA-BINDING \
  | tar -x -C <snapshot>
git -C /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-gap007 \
  archive 056849e23 rawlsing_next/source_configuration \
  rawlsing_next/pre553_source_read_admission.py source_pre553_validation/SRC04 \
  | tar -x -C <snapshot>

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<snapshot> \
  python3 <snapshot>/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/bind_real_metadata.py ...
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<snapshot> \
  python3 -m pytest <snapshot>/WORKER_RETURNS/PYAT-REAL-METADATA-BINDING/test_metadata_binding.py -q -o addopts=''
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
  python3 WORKER_RETURNS/PYAT-REAL-METADATA-INDEPENDENT-REVIEW/check_metadata.py
```

## Scope

Sourcefree metadata/fixture engineering only. No original SAV/DTA or respondent
rows read; no original workload issued; no production edit, merge, CI or adoption.
Only `WORKER_RETURNS/PYAT-REAL-METADATA-INDEPENDENT-REVIEW/**` written.
