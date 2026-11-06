# R3 — genuine SRC27–SRC30 DTA physical execution evidence

**FINDING:** All four genuine DTA originals were read through the accepted projected reader and produced exact full-row selected streams. SRC27 and SRC30 also completed the current full-cell-filter baseline; their selected-cell digests matched the projected route exactly. SRC28 and SRC29 full-frame baselines failed closed at the frozen whole-frame reader before cell comparison; projected selected reads succeeded because unselected failing string columns were never decoded.

**INTERPRETATION:** This closes the genuine-DTA measurement gap for the accepted producer, not the native pipeline. Projection remains physical-only. The two full-frame failures are exact decoder-format limits, not permission to guess encodings or force source values.

**ACTION:** D can use the projected route for selected metadata input on all four DTA sources. Native C11/I03/I05/Batch execution, respondent linkage, administration and all35 native economics remain separate and not claimed.

**OWNER:** D for native consumer; A for source mapping; G already accepted r2 code scoped. No self-review.

## Code/evidence identity

- Code head unchanged: `7a404b0dcaac0e4dd027b9edb98c9038d89dbd9a` (accepted scoped `a66e4a62…`).
- Branch: `codex/pyat-universal35-physical-stream-20261106-r1`.
- Execution script: `tools/dta_source_compare.py` (local read-only physical profiling; source root runtime binding only).
- Results: `results/SRC27-30_{projected,baseline}.json`, `results/dta_source_summary.json`.

## Genuine DTA results

| Source | Bytes | Rows | Slots | Selected metadata columns | Selected cells | Projected wall | Projected peak RSS | Full baseline |
|---|---:|---:|---:|---|---:|---:|---:|---|
| SRC27 | 139,531,180 | 29,002 | 1,198 | `q103_1`, `country` | 58,004 | 2.455 s | 130.5 MB | OK: 34,744,396 cells, 118.684 s, 1.227 GB |
| SRC28 | 199,716,969 | 38,864 | 627 | `q102_1`, `country` | 77,728 | 2.361 s | 128.0 MB | FAILED after 6.305 s: `ReadstatError: Unable to convert string to the requested encoding (invalid byte sequence)` |
| SRC29 | 170,487,994 | 51,206 | 1,290 | `gender_pr`, `country` | 102,412 | 4.596 s | 158.2 MB | FAILED after 6.177 s: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb5 in position 3` |
| SRC30 | 110,465,945 | 37,478 | 1,319 | `sampapp`, `country` | 74,956 | 2.885 s | 178.5 MB | OK: 49,433,482 cells, 174.838 s, 1.748 GB |

SRC27/30 exact checks: selected-cell digest, selected count, row count, source SHA and physical metadata digest all equal between baseline and projected. SRC27 digest `30f25e8f…`; SRC30 digest `b9105955…`.

Projected routes preserved every declared row: 29,002 / 38,864 / 51,206 / 37,478 selected rows respectively. No sampled rows. Batch size 10,000; no giant cell tuple retained; digest was streamed.

## DTA implications and limits

- The projected DTA path uses windowed `read_dta(usecols=..., row_offset=..., row_limit=...)` on the existing content-bound `/dev/fd` snapshot; no mutable original reopen and no full-source copy.
- SRC28/SRC29 full-frame baseline failure is retained as a real format/encoding limit. No encoding guess or unselected string coercion was introduced.
- Projection does not remove the full-frame DTA decode cost where the full frame succeeds; SRC27/30 baseline memory/time stays visible.
- Physical parity does not establish respondent/household linkage, administration, weights, C11/native facts, or scientific meaning.
- Native C11/I03/I05/Batch, all35, 16-GiB and native economics remain **NOT_RUN**.

## PROGRAMMA_DELTA

| Field | Value |
|---|---|
| Identity | Genuine DTA physical evidence at code `7a404b0d…`, accepted scoped `a66e4a62…`; no code change. |
| Function | Existing bounded selected physical-cell producer on actual SRC27–SRC30. |
| Input -> output | source-bound DTA incidence + selected response/coordinate names -> exact full-row selected stream/digest. |
| Evidence | all four projected OK; SRC27/30 exact baseline parity; SRC28/29 finite full-frame encoding failures. |
| First consumer | D selected native compiler input; native end-to-end still NOT_RUN. |
| Next | D/A end-to-end; no further C kernel. |
