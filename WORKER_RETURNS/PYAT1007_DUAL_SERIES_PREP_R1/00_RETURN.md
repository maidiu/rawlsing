# PYAT1007 — EARLY SOURCEFREE FIXTURE PREP return

`SOURCEFREE_PREP_ONLY` — not the full Arab Barometer + WVS real-source pilot.
No protected merge, no original-source grade, no automatic G5.

## Exact scope executed

Only the optional early sourcefree fixture-preparation tranche in
`ISSUE_1007_CURRENT.md` comment `6865974469`. The full real-source #1007
pilot, #997 source-to-saved bridge, #998 joined vertical, #1002 current
permission decision, #1006 economics and #999 early-gate dispositions are
separate and untouched.

One generic config-driven path was executed for three small
`NONRESPONDENT_FIXTURE_ONLY` shapes:

| fixture | R157 metadata basis | format | distinguishing semantics |
|---|---|---|---|
| Arab Barometer | `SRC07` Wave VIII, exact selected variable labels/states | SAV | row-ordinal identity; 0–10 scale with 98/99 missing; multiselect/ranked occurrence fixture; route-UNKNOWN control |
| WVS | `SRC35` Wave 7, exact selected variable labels/states | SAV | source-native `S007` key grain; `-1/-2/-4/-5` missing codes; 3-question same-respondent joint; route-UNKNOWN control |
| LiTS hostile control | `SRC28` Wave II, exact selected variable labels/states | DTA | unrelated family; repeated household-roster event; `-90/-97/-98/-99` states; mixed actual routing |

The path is the existing S1-B R157 config/decoder/projection/factory →
S2-B direct I02 → accepted S2-C Parquet/Zstd estate → accepted S2-D cold
I03/I05/Batch admission. No production file was edited and no second
decoder/writer/engine/bridge was created.

R157 metadata was read only from the accepted immutable Git blob
`1924499ef52403a0f331b8aff9b7c7eff99bf1e2`; no original respondent bytes,
original source hash, .env, credential or original byte holding was read.
The fixture configs use a synthetic TEST_ONLY original-identity SHA and
explicitly differ from the declared R157 metadata hashes.

## Actual executable evidence

Command (existing read-only venv; absolute path intentionally not committed):

```text
PYTHONPATH=. <existing read-only PYAT1006 venv python> \
  -m pytest -q WORKER_RETURNS/PYAT1007_DUAL_SERIES_PREP_R1/tests/test_dual_series_prep.py
```

Actual result: **12 passed, exit 0**. Raw logs and timing are in
`evidence/pytest_actual.log`, `evidence/pytest_actual.time` and
`evidence/pytest_exit.txt`.

Covered actual courts:

- all three series: positive cold I03 from the persisted release, with
  `source_opens=0`, `full_c11_repository_builds=0`,
  `persistent_body_corpora=0`;
- route `ROUTING_UNKNOWN` → typed `UNAVAILABLE` / `RISK_SET_UNAVAILABLE`,
  never zero;
- missing DK/refusal/inapplicable are not valid zero; observed zero is a
  real substantive cell and an absent valid zero is exact zero support;
- multiselect/ranked occurrence identity preserved; duplicate occurrence
  identity refused by accepted S2-B;
- WVS source-native key grain; missing key cell → typed `UNKNOWN`;
- no weight slots / typed weight absence; weighted query → typed
  `MEASURE_UNAVAILABLE` (no default weight 1);
- forged original identity, source-binding mismatch, revoked current,
  wrong independently held I02 and cross-series joint scope all refused;
- changed synthetic input → different actual fact → exact restore;
- fresh interpreter cold I03 against the same persisted release;
- cold I05 matches the existing native C11 oracle;
- Batch with QUERY + DISCOVERY units completes.

## Actual resource and contention

- pytest: 12 passed; 8.07 s reported, 9.17 s wall; maximum RSS
  **112,820,224 B (~107.6 MiB)**; peak memory footprint 91,193,344 B.
- fixture regeneration: 4.18 s wall; maximum RSS 107,339,776 B.
- fixture inputs total after generation: 6,984 B; persisted estates total:
  **1,760,894 B** for all three series.
- all runs stayed under 1 GiB; no performance-scale/100k workload was run.
- host was contended: load average approximately **7.8–8.9**, existing
  #1006 runner PID 45447 active throughout, free disk approximately
  **15.2–16.3 GB**. An isolated baseline was **not** run, so no relative
  slowdown claim is made.
- SAV writer embeds a wall-clock timestamp: the exact fixture SHA is
  recorded per build and the decoded synthetic cell manifest was
  deterministic across two builds. DTA fixture bytes and estate manifest
  were deterministic.
- provider/quota/token cost: `UNOBSERVED`; no invoice claim.

## Holds preserved

- real original bytes: `SOURCE_BYTES_UNAVAILABLE`;
- current source/use permission: `SOURCE_PERMISSION_HELD`;
- true #997 P0/P1 source→saved→receipt/fate vertical: `HOLD_DEPENDENCY`,
  NOT_RUN; Browser bridge not pulled, executed or repaired;
- #998 staging `d88630a448905856f980f7573442617813afda88` is separate;
- #999 S2-A remains `REVISE_EXACT_DEFECT` while actual I03 refuses the
  poison; not repaired here;
- #1002 restored historical SRC04/SRC17 grants are not a new source
  permission; no new source read;
- #1008/#1010 Browser duels are outside this control; not monitored,
  fetched, inspected or coordinated;
- no original35 blanket ingestion, protected merge, production CURRENT,
  Field Forge/PRE-V3/V3 extension, design issuer, weight authority or
  scientific comparability claim.

Scoped ABI result: **no frozen-writer edit was needed and no minimal
first-consumer blocker was found** for this sourcefree prep path. This is
not evidence that the real #997 bridge or original-source pilot is complete.

## Legitimate later owner/input list

1. Source/rights owner (#1002): exact current use grant, permitted
   host/purpose/retention and original bytes for the chosen Arab Barometer
   and WVS editions; exact wave/translation/instrument/response/design/
   weight evidence from the competent issuer.
2. #997 Browser S1-E: accepted one-pass source→saved 13-family bridge,
   terminal receipt/fate join and independent G5. P0/P1 remain NOT_RUN.
3. #998: separate integration receiver for the joined S01–S05 vertical.
4. #1006: physical economics measurement; this prep did not duplicate its
   workload or read its uncommitted harness.
5. #1001: separate 100k distinct respondents / 6 GiB scale gate.

## Pins and files

- worktree base: `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`;
- exact code/test/evidence cut: `6f7369f004573bfd09d961f8bd92076eae228237`;
- accepted interfaces: S1-B `dedd2fb8…`, S1-C `dae66cd…`, S2-B
  `092db6bc…` / G5 `96ad0fe2…`, S2-C `b7b697b…` / #990, S2-D `9d96a9c…` /
  G5 `ba8d760c…`;
- exact imported-file blob/SHA-256 pins: `evidence/SOURCE_PINS.json`;
- fixture/config/estate regeneration identities:
  `evidence/FIXTURE_REGENERATION_MANIFEST.json`;
- actual run receipt: `evidence/RUN_RECEIPT.json`;
- code/tests: `fixture_harness.py`, `tests/test_dual_series_prep.py`,
  `extract_r157_metadata.py`, `measure_fixtures.py`;
- concise delta: `PROGRAMMA_DELTA.md`; draft PR text: `PR_BODY.md`.

**STOP.** No protected merge, no original-source pilot, no automatic G5.
