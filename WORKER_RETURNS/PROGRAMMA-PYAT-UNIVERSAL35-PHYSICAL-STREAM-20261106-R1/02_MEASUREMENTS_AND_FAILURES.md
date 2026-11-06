# Measured genuine-source decode, bounded stream, and exact blockers

## Measurement scope

Lower-level frozen-decoder profiling under the user's explicit read-only local physical-engineering authorization. No governed `SourceReadDecision` was minted, no native/science grant is claimed, and no source rows/values are published. Runtime source root was supplied only by `.local-logs/pyat-universal35/source-runtime-binding.local.json` (alias `USER_ORIGINAL35_DATA_ROOT`); it is not hardcoded in the module.

## Genuine source decode

| Source | Bytes | Rows | Slots | Reader | Decode wall | Decode peak RSS |
|---|---:|---:|---:|---|---:|---:|
| SRC31 | 595,974 | 8,442 | 68 | SAV, no encoding override | 0.493 s | 94.0 MB |
| SRC16 | 1,647,241 | 1,613 | 216 | SAV, no encoding override | 0.631 s | 122.2 MB |
| SRC04 | 1,531,099 | 7,337 | 181 | SAV, no encoding override | 0.733 s | 107.5 MB |
| SRC13 | 31,857,144 | 41,125 | 513 | SAV, exact latin1 compatibility | 5.415 s | 806.4 MB |

SRC13 confirms the frozen decoder's latin1 compatibility full-frame read remains a memory ceiling independent of the producer.

## SRC31 bounded stream versus eager materialization

| Mode | Cells | Wall | CPU | RSS after | Peak RSS |
|---|---:|---:|---:|---:|---:|
| decode only | 0 returned | 0.493 s | 1.295 s | 93.9 MB | 94.0 MB |
| eager tuple materialize | 574,056 | 2.551 s | 2.529 s | 225.8 MB | 225.9 MB |
| bounded stream pass 1 | 574,056 | 2.247 s | 2.234 s | 101.2 MB | 101.3 MB |
| bounded stream pass 2 | 574,056 | 2.274 s | 2.257 s | 101.6 MB | 101.6 MB |
| filtered stream pass 1 (4 columns) | 33,768 | 2.103 s | 2.093 s | 101.2 MB | 101.3 MB |
| filtered stream pass 2 (4 columns) | 33,768 | 2.123 s | 2.110 s | 99.4 MB | 101.7 MB |

The two full stream passes had identical first cell `[1,1,v1]`, last cell `[8442,68,d13]`, and exact full count. The filtered passes selected `d18c`, `c13a`, `b8`, `d18k`, preserved all 8,442 rows, and repeated exactly. The producer therefore removes the measured eager-cell tuple peak on this shape while preserving replay/full-row identity for both factory and D selected-item use.

## Genuine C11 build refusal

`build_validated_c11_release_from_config(config, incidence=...)` was attempted on SRC31 and SRC16. Both failed closed before release construction with:

```text
SourceBackedC11FacadeError: unbound response value/state;
no label/frequency/missingness inference
```

D's published original attempts independently record SRC31 C11 refusal at 8,442 rows, 94.603 s, 1.66 GB peak RSS; SRC09/SRC10/SRC11/SRC15 native-R03 `max_items=1` attempts did not finish within 600 s before eager decode/facts. D's evidence confirms the exact filtered stream need, not an adapter estimate. Source: `115fe70e660fb19a65ca49b4a12ffc8876be065c`/`WORKER_RETURNS/PROGRAMMA-PYAT-UNIVERSAL35-D-20261106-R1/evidence/native_attempts.json`.

A owns the final source-mapping defect disposition and its prescan counts. This lane only observed the frozen current factory's unbound-value refusal; it does not reinterpret unknown codes, labels, frequencies, missingness, or held states to make a release pass.

## Existing factory parity

On the existing R157 SRC09 nonrespondent fixture, the bounded stream produced the same `C11LogicalRelease` ref, replay ref, and full public-object material as the permitted-incidence path through `build_validated_c11_release_from_config`. New adapter tests also prove:

- genuine SAV two-pass exact cell replay,
- source-snapshot stability after source path mutation,
- wrong source custody SHA refusal,
- invalid batch-size refusal,
- reordered and truncated full-grid refusal.

Test result: **4 adapter tests passed**; **34 focused ABI/read-admission/original35-operations/source-config tests passed**. Log: `results/focused_tests.log`.

## Not run

- Original35 native execution: **NOT_RUN** (blocked by unbound source values, not by producer).
- All35 physical streaming/build: **NOT_RUN**.
- 16-GiB operational suitability: **NOT_RUN**.
- Full SRC13 bounded scan/C11 build: **NOT_RUN** after 806 MB decode ceiling; no largest-source blind materialization.
- Independent review and protected merge: **HOLD**.
