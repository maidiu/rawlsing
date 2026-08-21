# FIRST LAUNCH ORDER SEQUENCE

## ORDER SR01 — SOURCE BYTE CENSUS — HQ/browser
Status: `ACCEPTED`
Output: `SOURCE_BYTE_INVENTORY.csv`.
Observed: 35 governed source files, 31 SAV, 4 DTA. AppleDouble packaging artifacts excluded.
Gate: G-SR01 ACCEPTED.

## ORDER SR02 — LEGACY WRITER + ACTUAL V550 DB DEPENDENCY GENEALOGY — HQ/browser + local read-only receipt
Status: `ACCEPTED__PROVENANCE_CLOSED`

Binding closure: `15_SR02_R3_ADJUDICATION.md`.

Decisive holdings include:

- legacy runtime-critical Postgres carriers are evidence, not rebuilt source authority;
- Mode-A July-20 post-load response inserts are attributable and respondent association is not trusted;
- Mode-B later Asian W6 route is historical/excluded from CLOSED_35;
- LiTS I historical country decoding used an incompatible numeric code map, dropping exactly 1000 Moldova respondents and misclassifying many retained country codes;
- later weight/source-wave/QSM materializations are operational/governance layers, not raw source truth.

No further local SR02 execution is ordered.
Gate: G-SR02 ACCEPTED.

## ORDER SR03 — 35-SOURCE PHYSICAL METADATA EXTRACTION — local Codex + HQ adjudication
Status: `ACCEPTED__35_SOURCE_PHYSICAL_CENSUS_COMPLETE`

Binding closure: `16_SR03_R3_ADJUDICATION.md`.

All 35 exact source snapshots were physically censused with row/cell conservation. The corpus confirms cross-source SPSS user-missing exposure, SAV/DTA physical-state heterogeneity, multiple-response metadata, source-reader encoding heterogeneity, and native-ID diversity without requiring a C11 architecture change.

No further SR03 run is ordered unless source bytes/decoder dependency/config changes.
Gate: G-SR03 ACCEPTED.

## ORDER SR05 — FORMAT-NEUTRAL SOURCE CONSTITUTION — HQ/browser
Status: `ACCEPTED__RECLOSED_AFTER_FULL_CENSUS`

Binding closure: `17_SR05_SOURCE_CONSTITUTION_RECLOSURE.md`.

The full corpus fits the frozen boundary:

`source bytes -> physical decoder -> format-neutral raw incidence -> source authority pack -> governed C11 state`

Remaining source-semantic/text-encoding/source-equivalence questions are assigned to G-SR07/G-SR08/G-SR09 and do not block carrier selection.
Gate: G-SR05 ACCEPTED.

## ORDER SR04 — PHYSICAL CARRIER BAKEOFF — bounded local Codex harness cell
Status: `LAUNCH_ORDER_FROZEN__RETURN_REQUIRED`

Binding authorities:

- `11_PHYSICAL_CARRIER_SELECTION_COURT.md`
- `18_SR04_CARRIER_BAKEOFF_EXECUTION_CONTRACT.md`
- `SR04_LOCAL_EXECUTION_ORDER.md`

Candidates:

- Parquet + DuckDB direct;
- DuckDB native;
- fresh disposable local PostgreSQL;
- SQLite.

Decision priority is exact: **flawless effectiveness -> fast -> light**.

The bakeoff uses exact WVS7 + LiTS I source snapshots, every respondent, and a deterministic 24-variable fixture per source (~3.03M event rows). Correctness requires complete candidate readback digests plus an independently computed Python query oracle. Performance uses I03/I05-equivalent joint/risk-set/weighted/branch/XOR/recursive/Simpson-shaped queries. Source-semantic certification remains later-gate work.

Hard safety law: live Postgres is never benchmarked or written; candidate storage is disposable; at least 5 GiB free-disk reserve is preserved; candidate storage/time ceilings are fail-closed.

The local worker may implement only `SR04_CARRIER_BAKEOFF.py`, commit/push that one harness, then execute from its exact committed head and return the small metrics package.

Gate: G-SR04 awaits the bakeoff return + HQ adjudication.

## ORDER SR06 — SELECTED CARRIER / C11 DECODER IMPLEMENTATION
Status: `BLOCKED_ON_G_SR04`

No production/runtime implementation worker launches until G-SR04 closes.
