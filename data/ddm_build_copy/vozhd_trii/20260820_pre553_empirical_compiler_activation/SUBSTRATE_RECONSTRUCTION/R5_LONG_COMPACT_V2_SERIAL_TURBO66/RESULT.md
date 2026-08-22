# Authority 66 Serial Turbo Court

Source SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Relevant R5 suite: `68 passed, 0 failed, 0 skipped`.

Recommended variant: **V4** — V1 geometry, gzip-1 disposable temporary runs, temporary fsync OFF, baseline final layout/compression.

| court | build s | reopen + audit s | total s | runs / passes | members | density B/cell | peak RSS | scratch peak |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 250K V0 | 52.982 | 25.769 | 78.751 | 62 / 1 | 16 | 14.962512 | 201 MB | 10.3 MB temp output |
| 250K V4 | 49.273 | 26.976 | 76.249 | 4 / 0 | 16 | 14.962512 | 268 MB | 6.3 MB temp output |
| 250K V5 | 49.438 | 27.584 | 77.022 | 4 / 0 | 16 | 14.962512 | 268 MB | 106.1 MB raw temp |
| 250K V6B | 50.385 | 27.045 | 77.430 | 4 / 0 | 1 | 14.904824 | 268 MB | 6.3 MB temp output |
| 250K V7 | 56.788 | 33.340 | 90.128 | 4 / 0 | 1 | 18.654940 | 268 MB | 6.3 MB temp output |
| 2M V0 | 459.004 | 226.853 | 685.857 | 489 / 2 | 123 | 14.438538 | 268 MB | 121.0 MB temp output |
| 2M V4 | 392.056 | 204.893 | 596.949 | 31 / 0 | 123 | 14.438538 | 268 MB | 49.9 MB temp output |
| 2M V6B | 442.879 | 232.602 | 675.481 | 31 / 0 | 4 | 14.378376 | 268 MB | 49.9 MB temp output |
| 2M V7 | 461.912 | 216.412 | 678.324 | 31 / 0 | 4 | 18.003386 | 268 MB | 49.9 MB temp output |

V1–V5 were root/member byte-identical to V0 at 250K; V4 was also root/member byte-identical to V0 at 2M. V6 and V7 preserved the exact logical stream and full audit while changing physical root/layout. All 2M finalists reported 2,000,614 canonical rows, 2,000,000 source physical cells, 613 source variables, and one source-metadata relation.

V4 2M build speedup is `1.17075x`; build-plus-reopen/audit speedup is `1.14898x`. V6/V7 did not beat V4 on total wall time. V7 passed preferred density and projected full-WVS storage (about 1.05 GiB), but was slower and is not recommended.

Disposition: `R5_SERIAL_TURBO_VALIDATED__MODEST_GAIN__HQ_DECISION_REQUIRED`
