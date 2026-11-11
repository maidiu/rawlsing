# Authority 66 Narrow Compliance Closure

Starting HEAD: `c8859bebf5baccf0ac65932c08b5dbdcb60012d7`
Validated serial ancestor: `11877f5a043418100773b8a476ee425ec63305cd`
Source SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Tests: `77 passed, 0 failed, 0 skipped`. Safety-governor, failure-closure, codec-equivalence, ordering, cleanup, and determinism tests passed without allocating large memory. The actual V4 fan-in was 64 from requested 64; no OS limit was raised. Court scratch was cleaned.

| checkpoint | V0 build | V4 build | V0 reopen | V4 reopen | V0 audit | V4 audit | V0 runs/passes | V4 runs/passes |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 250,000 | 57.579907 | 53.911229 | 0.000172 | 0.000303 | 26.480472 | 27.392201 | 62 / 1 | 4 / 0 |
| 2,000,000 | 468.739863 | 389.066875 | 0.000348 | 0.000320 | 209.875188 | 210.809710 | 489 / 2 | 31 / 0 |

At 2M, V4 build speedup is `1.204779672x`; total certification speedup, using build + reopen + audit, is `1.131257750x`. V4 and V0 were exactly equal at both checkpoints for canonical row count, logical digest, physical root, root bytes, inventory bytes, member order/count, every member byte/hash/logical digest, and full audit.

V4 peak RSS was `200,540,160` bytes. Peak observed scratch was `78,693,265` bytes for V4 at 2M. V4 density was `14.438538 B/cell`; projected full WVS carrier is `0.801 GiB`. Canonical row generation is included in initial run generation/sort/write because it is not cleanly separable in the frozen decoder seam.

Disposition: `R5_SERIAL_TURBO_V4_COMPLIANCE_CLOSED__READY_FOR_FULL_SOURCE_HQ_AUTHORITY`
