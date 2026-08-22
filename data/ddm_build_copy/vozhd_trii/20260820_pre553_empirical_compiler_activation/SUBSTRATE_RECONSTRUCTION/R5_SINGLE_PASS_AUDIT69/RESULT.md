# Authority 69 single-pass full-audit return

Starting HEAD: `55d4bae445b5eb837aec6f3c67083e131d8e3b0c`

Source: `/Users/matthewsmith/Desktop/Rawlsing/data/Data/WVS Wave 7.sav`

Source SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Complete relevant R5 suite: `96 passed in 32.67s`, `0 failed`, `0 skipped`.
The Authority-69 hostile equivalence court passed `19 passed`, `0 skipped`.

One accepted serial V4 carrier was built at each checkpoint. Ordinary
`full_audit()` and the additive single-pass audit then ran against the same
sealed carrier; no overlap implementation was run.

| checkpoint | ordinary audit | single-pass audit | speedup | ordinary rows/s | single-pass rows/s | exact equality |
|---:|---:|---:|---:|---:|---:|:---:|
| 250,000 | 25.15058713899998s | 21.21488576900083s | 1.18551602930382x | 9,964.538745 | 11,813.120407 | PASS |
| 2,000,000 | 174.29865614400114s | 133.3463220119993s | 1.307112588589558x | 11,478.080464 | 15,003.143467 | PASS |

At 2M both audits produced 2,000,614 canonical rows, the same logical
stream digest, relation counts, and physical root. The 2M selection threshold
`>=1.20x` is met.

Bounded hostile instrumentation proved one `_logical_wire(row)` call per
canonical row in the single-pass path. The ordinary path has two calls per
canonical row by its existing `iter_rows()` plus `full_audit()` path:
250K: ordinary 501,228 / single-pass 250,614; 2M: ordinary 4,001,228 /
single-pass 2,000,614.

Final disposition:

`R5_SINGLE_PASS_AUDIT69_VALIDATED__USE_FOR_FULL_WVS7_CERTIFICATION`

No accepted carrier runtime, `_logical_wire`, `_decode_storage`, V4, source
semantics, or downstream runtime was modified. Full WVS and LiTS were not run.
