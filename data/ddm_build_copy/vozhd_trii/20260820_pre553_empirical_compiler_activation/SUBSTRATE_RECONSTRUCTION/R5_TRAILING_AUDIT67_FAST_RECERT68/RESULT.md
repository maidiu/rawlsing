# Authority 68 fast trailing-audit recertification

Starting HEAD: `5e781eafe79a8f35921d48dd5c23798de723b352`

Source: `/Users/matthewsmith/Desktop/Rawlsing/data/Data/WVS Wave 7.sav`

Source SHA-256: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

Complete relevant R5 suite: `96 passed in 38.29s`, `0 failed`, `0 skipped`.
The Authority-68 hostile/process court itself passed `16 passed`, `0 skipped`.

The only real-source runs were RECERT-250K and RECERT-2M, each comparing
ordinary accepted V4 plus post-build `full_audit()` with the frozen fast
overlap candidate. Exact carrier/root/inventory/member parity and ordinary
versus trailing audit equality passed at both checkpoints. Canonical rows,
logical stream digests, and physical roots matched.

| checkpoint | ordinary total | overlap total | speedup | overlap builder | builder slowdown |
|---:|---:|---:|---:|---:|---:|
| 250,000 | 65.35063808000268s | 44.49150997800098s | 1.468813x | 44.50347068300107s | 2.903% |
| 2,000,000 | 681.4949035620011s | 566.752039545001s | 1.2024569053322116x | 566.7596225590023s | 42.09297166787307% |

At 2M, the preferred `>=1.25x` speedup gate is MISS and the preferred
`<=10%` builder-slowdown gate is MISS. Exact, hostile/process, queue, and
resource integrity gates passed. The measured queue peak was `1` against
capacity `8`; pending/in-flight/outstanding sub-peaks were not instrumented
by the frozen candidate.

Final disposition:

`R5_TRAILING_AUDIT67_FAST_RECERTIFIED__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED`

No implementation file, callback, V4 configuration, process topology, queue
capacity, readiness payload, audit semantics, carrier layout, or downstream
runtime was modified. Full WVS7 certification was not run.
