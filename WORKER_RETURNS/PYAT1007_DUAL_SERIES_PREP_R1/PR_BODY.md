Draft PR — PYAT1007 EARLY SOURCEFREE FIXTURE PREP

`SOURCEFREE_PREP_ONLY`; do not merge as protected/original-source acceptance.

## What this is

One isolated author cut for the optional early sourcefree fixture-preparation
tranche in issue #1007 comment 6865974469. It is not the full Arab Barometer +
WVS real-source pilot and does not claim a #997 source-to-saved vertical.

The added harness drives the existing generic path:

R157 metadata witness → closed NONRESPONDENT_FIXTURE config → synthetic
TEST_ONLY SAV/DTA cells → S1-B decoder/projection/factory → S2-B direct I02 →
accepted S2-C persisted Parquet/Zstd estate → accepted S2-D cold I03/I05/Batch.

Three contrasting shapes are exercised: Arab Barometer SRC07 (SAV, row-grain,
0–10 scale with 98/99, multiselect/ranked occurrence fixture), WVS SRC35 (SAV,
source-native S007 key, negative missing codes, 3-question joint) and an
unrelated hostile LiTS SRC28 (DTA, repeated household event, different missing
states). All semantic labels/value states come from exact R157 Git metadata;
routing/ranked overrides are explicitly TEST_ONLY fixture semantics.
No original respondent bytes, original source hash, translation, rights,
design issuer or weight authority is invented or read.

## Actual executed evidence

`12 passed`, exit 0, from:

```text
PYTHONPATH=. <existing read-only venv python> -m pytest -q \
  WORKER_RETURNS/PYAT1007_DUAL_SERIES_PREP_R1/tests/test_dual_series_prep.py
```

Covered: positive cold I03 for all three; route-UNKNOWN typed unavailable;
missing vs valid zero; ranked occurrence identity and duplicate refusal; ID
grain and missing key typed UNKNOWN; weight-design typed absence; forged
original/source-binding/current/I02 mismatch; cross-series joint refusal;
changed input → changed fact → exact restore; fresh interpreter cold I03;
cold I05 equals the native C11 oracle; Batch QUERY+DISCOVERY completes.

Actual bounded resource: maximum RSS 112,820,224 B; three persisted estates
1,760,894 B; under 1 GiB. Existing #1006 runner was active (PID 45447, load
~7.8–8.9); isolated baseline NOT_RUN, so no relative speed claim.

## Holds

- real original bytes `SOURCE_BYTES_UNAVAILABLE`; current permission
  `SOURCE_PERMISSION_HELD`;
- true #997 P0/P1 `HOLD_DEPENDENCY`, NOT_RUN; Browser bridge not pulled,
  executed or repaired;
- #998 staging `d88630a448905856f980f7573442617813afda88` separate; #999 S2-A
  remains REVISE; #1002 historical grants are not new permission; #1008/#1010
  Browser duels outside this control;
- no protected merge, original35 blanket ingestion, production CURRENT,
  scientific comparability, design/weight issuer, Field Forge/PRE-V3/V3 or
  automatic G5.

No frozen-writer edit was needed and no minimal first-consumer blocker was
found for this sourcefree prep path.

Exact code/test/evidence cut: see `RETURN_SHA.txt` / the branch commit
reported to HQ. Full log, pins and regeneration identities are under
`evidence/`.
