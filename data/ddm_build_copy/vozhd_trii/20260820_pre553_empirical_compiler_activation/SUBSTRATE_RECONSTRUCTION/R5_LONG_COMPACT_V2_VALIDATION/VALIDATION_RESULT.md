# R5 LONG COMPACT V2 exact validation

Validation branch HEAD: `568e63367cb8871c4b06d43aa5fcb04ead4d4835`.
Frozen compact implementation: `b643ea6ea08a6ed29e31453135ac9113286d581d`.

The complete relevant R5 suite passed: 68 passed, 0 failed, 0 skipped. Candidate code, tests, decoder, and frozen PRE553 runtime were not modified.

Exact WVS7 source SHA, shape, and decoder contract passed. The sequential compact density checkpoints all sealed, reopened, fully audited, and produced matching logical/audit digests:

| Physical cells | Sealed bytes | Bytes/cell | Projected full WVS | Peak RSS | Build | Reopen/audit |
|---:|---:|---:|---:|---:|---:|---:|
| 250,000 | 3,740,628 | 14.962512 | 0.830 GiB | 135,675,904 | 55.05 s | 27.53 s |
| 1,000,000 | 14,399,893 | 14.399893 | 0.799 GiB | 140,902,400 | 226.55 s | 103.78 s |
| 2,000,000 | 28,877,077 | 14.438539 | 0.801 GiB | 141,787,136 | 456.23 s | 209.88 s |

All checkpoints are at or below the preferred 36 B/event threshold. Final disposition: `R5_LONG_COMPACT_V2_VALIDATED__PREFERRED_DENSITY_PASS`.

Required return token: `PRE553_R5_LONG_COMPACT_V2_VALIDATION_RETURNED`.
