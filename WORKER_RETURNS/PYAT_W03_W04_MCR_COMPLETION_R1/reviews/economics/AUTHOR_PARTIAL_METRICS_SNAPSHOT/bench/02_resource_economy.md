# Bench lane — W34-RESOURCE-ECONOMY

**Status:** `INCOMPLETE` for the 15% cold-RSS target; benchmark harness delivered, final candidate matrix not authorized until an integrated candidate head exists.

## Delivered CLI

```text
python3 -m rawlsing_next.bench_w03_w04_physical \
  --scenario cold,cells-and-hash,full-matrix \
  --profiles narrow,wide,repeat \
  --rows 100000 --repetitions 3 --jsonpath <path>
```

- `cold`: exact fresh child, governed physical cells/projection → I02/C11 seal → compact → real I03/I05.
- `cells-and-hash`: same actual pipeline with the stage instrumentation; no handbuilt oracle.
- `full-matrix`: fresh cold, fresh process carrier reopen/warm, and delete/rebuild; persisted canonical `ParquetC11Carrier` only.
- `--source-root` allows the same benchmark file to load the protected 4f3413 or current 46b source without changing either tree.
- Child cap is 6 GiB; one measured child at a time; no downsizing and calling it a pass.

## Stage instrumentation

Process RSS is from `resource.getrusage` (Darwin bytes; Linux normalized). The benchmark records:
`profile_setup`, `cells` (lazy generation and peak), `decode` (explicitly not applicable for exact physical-cell streams), `projection`, `objectconstruction` + `canonicalhash` (combined at the current public candidate boundary), `i02_validation_seal`/`seal`, `compact`, `persist`, `reopen`, `firstconsumer`, and `repeat_firstconsumer`.
It also records true process wall/CPU, peak RSS, cache files/bytes, source opens (zero for the in-memory cell stream), cache-write amortization, host load, and fresh-process colder/warm/rebuild distinction.

## 1,000-row paired matrix (one fresh process per section; 46b current vs protected 4f3413)

| Profile | Cold wall current/protected | Cold RSS current/protected | Warm wall current/protected | Warm cache hit |
|---|---:|---:|---:|---|
| narrow | 8.17 s / 6.998 s (**+16.7% wall regression**) | 197.7 MB / 210.2 MB (−5.9%) | 4.44 s / 4.08 s (+8.8%) | yes |
| wide | 16.76 s / 17.96 s (−6.7%) | 344.6 MB / 379.3 MB (−9.1%) | 7.79 s / 9.54 s (−18.4%) | yes |
| repeat | 20.15 s / 20.30 s (−0.7%) | 345.9 MB / 381.2 MB (−9.3%) | 11.38 s / 13.18 s (−13.6%) | yes |

Immediate rebuild preserves the cold behavior; no regression is hidden. The narrow cold wall regression is preserved.

## 100,000-row narrow cold paired measurement

| Source | Wall | Peak RSS | Cells | Fact state |
|---|---:|---:|---:|---|
| current `46b73256` | 777.53 s | 5,923,426,304 B | 300,000 | `SUPPORTED` |
| protected `4f3413` | 997.04 s | 5,240,467,456 B | 300,000 | `SUPPORTED` |

- Wall ratio current/protected: **0.7798**.
- RSS ratio current/protected: **1.1303** — a **13.0% cold-RSS regression**, not a 15% improvement.
- Both exact sourcefree facts and consumer state are preserved.
- `100000` wide/repeat were not run in this author lane; the candidate final 3-repetition matrix must wait for an HQ-pinned integrated candidate head. No smaller run is relabeled as a 100k pass.

**This does not satisfy the user's >=15% cold-median-RSS target and does not satisfy final matrix acceptance.** It is a real paired baseline receipt and a precise integration boundary.

## Sourcefree limits

Grouped/Batch/P41 are `NOT_APPLICABLE` to this selected sourcefree physical fixture; no handbuilt substitute is used. No original respondent/SAV/DTA/DB/source bytes, native workload, original35, science or actor effect; no protected merge. The data are synthetic governed physical fixtures from the existing sourcefree route-B test path.
