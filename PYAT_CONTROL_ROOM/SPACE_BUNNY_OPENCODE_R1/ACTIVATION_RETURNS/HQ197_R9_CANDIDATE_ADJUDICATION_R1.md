# HQ197 — R9 candidate adjudication

Status:
`BROKER_CONFIRMED__DQ01_REPAIRED__CANDIDATE_PARTIAL__PHYSICAL_SELECTED_AUTHORITY_OPEN__R7_REQUAL_REQUIRED`

Inputs:
- warrant successor `2410eb7b215f904fa428df82e47fb05ede91ee21`
- independent broker/selected review `2e43b8c1e975974add3ac2cecfbd6daa96afd98b`
- implementation candidate `d5ce4ecff6acc25d199577a7859de7e98514e9fd`

## Warrant successor

Accept structurally:
`WARRANT_ACCOUNTING_SUCCESSOR_STRUCTURE_READY__TECHNICAL_VALUES_PENDING`

DQ-01 is repaired: per-source accounting is restored and pre-launch budgets/basis are separated from runtime observed counts. The instrument remains unsigned, unissued and non-authorizing.

The packet carries an obsolete "independent integration review not completed" blocker. HQ already discharged that historical item under the completed independent C4 review chain. It must not reappear in the eventual successor.

## Broker route

Independent review confirms the pyreadstat 1.3.6 file-like route:
- application owns the source-path open;
- compiled ReadStat receives an empty path/no-op open handler on that route;
- no rebuild or privilege is required;
- R7 interpreter/package identity is unchanged.

Accepted constraints:
- raising from the bridge read callback can hang because the bridge catches exceptions;
- byte-cap failure must use a bridge-safe non-raising mechanism such as bounded read/premature EOF;
- correct seek/tell semantics are required;
- DTA chunk parses require position-zero fresh logical views/reset;
- pyreadstat version/seam must be pinned.

## Candidate still not accepted

### R9-BROKER-BYTE-CAP-001

The candidate exposes `reader_bytes` in `SourceAccessBudget`, but its governed `_read()` reads first and does not consult that ceiling before the read. Its committed C6 court does not test a `reader_bytes` cap.

Status: OPEN.

### R9-BROKER-R7-REQUAL-002

HQ196 incorrectly asked for a "55-carrier" rerun.

The governing R7 qualification is six exact test files / 55 collected tests / 55 passed twice:
- test_closed35_g01_sav_numeric_representation_authority.py — 9
- test_closed35_d01_declared_encoding_admission.py — 8
- test_closed35_d02_opaque_datetime_carrier.py — 13
- test_fiabc_lm2_r1j_sav_representation_authority.py — 9
- test_r35_i01_physical_metadata.py — 6
- test_pre553_source_backed_c11_facade.py — 10

Environment:
`/Users/matthewsmith/Desktop/Rawlsing/LOCAL_COURTS/qualification/r7-c4-source-free-venv`

The candidate's constructed 55-carrier corpus is useful synthetic evidence but is not that court.

Its reported two test failures in another sparse run are baseline missing-duckdb failures reproduced at the pristine freeze; they are not established candidate regressions. They also do not replace the six-file qualified court.

Status: OPEN.

### R9-SEL-PHYSICAL-SEMANTICS-003

Frozen law states:
- SRC02/SRC06: `BOUNDED_FRESH_PHYSICAL_SELECTED_VARIABLE_READ`
- SRC14: `BOUNDED_FRESH_PHYSICAL_READ_EXACT_VARIABLE`
- each: selected_reads=1, full_reads=0.

Both the independent review and candidate measured pyreadstat `usecols` as projection-only: returned columns change, underlying read calls/bytes do not.

HQ therefore does not authorize relabeling that route as the frozen physical selected-variable operation until the authority provenance is reconstructed.

Status: AUTHORITY_FORENSICS_REQUIRED.

## C4 closure

The raw-path sites in `runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py` are not in the accepted 23-module C4 producer-inclusive closure.

They do not block this C4/R9 broker candidate.

## Next wave

1. hostile review of the actual candidate;
2. hardening + exact R7 six-file court + C4 escape audit;
3. authority archaeology for the meaning of the physical-selected operation.

All are SPARSE_REQUIRED.

R9 remains open.
R7 remains closed at runtime/environment identity grain.
Live C4 remains separately blocked by host disk policy/capacity.
HQ182 C4 non-adoption hold remains pending reserved Astra decision.

All existing source/warrant/live/C7/actor holds remain.
