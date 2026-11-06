# Measured selected-reader comparison, decode ceilings, and blockers

## Scope

Lower-level frozen-decoder profiling under the user's explicit read-only local physical-engineering authorization. No governed `SourceReadDecision` was minted, no native/science grant claimed, and no source rows/values published. Runtime root came only from `.local-logs/pyat-universal35/source-runtime-binding.local.json` alias `USER_ORIGINAL35_DATA_ROOT`; it is not in the module.

## Genuine source decode

| Source | Bytes | Rows | Slots | Reader | Decode wall | Decode peak RSS |
|---|---:|---:|---:|---|---:|---:|
| SRC31 | 595,974 | 8,442 | 68 | SAV, no override | 0.49–0.66 s | 94.0 MB |
| SRC16 | 1,647,241 | 1,613 | 216 | SAV, no override | 0.63 s | 122.2 MB |
| SRC04 | 1,531,099 | 7,337 | 181 | SAV, no override | 0.73 s | 107.5 MB |
| SRC09 | 7,735,596 | 20,667 | 289 | SAV, no override | 0.65–0.80 s | 114.2 MB |
| SRC13 | 31,857,144 | 41,125 | 513 | SAV, latin1 compatibility | 5.42 s | 806.4 MB |

SRC13 confirms the frozen decoder's latin1 compatibility full-frame read remains a memory ceiling independent of projection.

## Current D-style filter versus projected reader

The earlier 226 MB tuple-versus-101 MB comparison was an eager-materialization diagnostic, **not** the current D first-consumer baseline. The corrected comparison uses D's `incidence.iter_cells()` filter over all cells versus this module's selected-column reader.

| Source | Selection | Current D path | Projected path | Selected cells | Exact |
|---|---|---|---:|---:|---:|---|
| SRC31 | `d18c,c13a,b8,d18k` | 574,056 all cells; 2.45–2.72 s/pass | 0.14–0.17 s/pass | 33,768/pass | yes |
| SRC09 | `q74` + `ir2b` (D `max_items=1`) | 5,972,763 all cells; 46.4–47.6 s/pass | 0.44–0.53 s/pass | 41,334/pass | yes |

SRC09 projected versus current selected-cell sequence SHA-256 was identical: `1d23d7813ca7a24eda8c7c6538cae6485c53d0320dab2bb0740398621f2381d4`. Both full-row ranges and source SHA were retained; no row sampling.

Native-package consumer parity on SRC09: release ref `38f8d092e57fec00ef3829ab1d62d92a380b549466a1945cd8a8fc209440956b`, replay ref `ded005be7735e4f4e61eb367c456f402a3b4fbb363ba12f17f4a12816c8a060d`, and 62,009 public objects matched. The native-package materialization itself remained about 42–47 s in this probe, so no full-D speedup is claimed.

## Genuine C11 refusal and D attempts

`build_validated_c11_release_from_config(config, incidence=...)` on SRC31 and SRC16 failed closed with:

```text
SourceBackedC11FacadeError: unbound response value/state;
no label/frequency/missingness inference
```

A owns the final source-mapping disposition and its prescan counts. This lane does not reinterpret unknown codes, labels, frequencies, missingness, or held states.

D's published attempts `115fe70e660fb19a65ca49b4a12ffc8876be065c`/`WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-D-20261106-R1/evidence/native_attempts.json` record SRC31 C11 refusal at 8,442 rows, 94.603 s, 1.66 GB peak, and SRC09/10/11/15 native-R03 `max_items=1` attempts not finishing 600 s before facts. The physical selected-reader improvement above is necessary but does not by itself claim to repair the full D 600 s end-to-end path.

## Tests and limits

- Adapter tests: **5 passed**.
- Focused ABI/read-admission/original35-operations/source-config suite: **35 passed**. Log: `results/focused_tests.log`.
- Existing fixture full-factory and native-package parity passed.
- Refused: wrong source custody SHA, invalid batch, full-grid truncation/reorder, absent/duplicate selected column, changed source identity.
- Already-materialized compatibility frames stay in memory; projection does not remove that prior history.
- Original35 native, all35 physical streaming, and 16-GiB operational tests remain **NOT_RUN**.
