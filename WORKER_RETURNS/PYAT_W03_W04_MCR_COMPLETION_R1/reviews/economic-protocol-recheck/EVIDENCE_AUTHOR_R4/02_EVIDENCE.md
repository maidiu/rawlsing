# Evidence index

## Code/test bytes

```text
d4fbce68af10f8cfa7b84f513322053cfa4e4e83e070d8358c05cf7ad55ad4cc  rawlsing_next/bench_w03_w04_physical.py
c6dd3aa11a25743b5a6489b79a2665443b749fbd6a03275cb53770a2ffe0cdd2  rawlsing_next/tests/test_bench_w03_w04_physical.py
949918f44a6bab0850997c304f1a1c890d7bcdb65ac41a5041ac9117223d21d5  rawlsing_next/tests/test_bench_w03_w04_physical.py.proof.json
```

## Tiny paired result

- Current source head: `9a71d0a0825c142372e56ac5d6bd34847ce6f227`
- Baseline source head: `4f3413fc5c37b589be3412f826bf8f68ee617d4a`
- Method SHA256: `d4fbce68...`
- External baseline file SHA256: `b35d5bf2...`
- Identity: all true
- Event/fingerprint parity: true, 6 comparisons
- Cap: true, sampled monitor, no overshoot
- Cold RSS threshold: true (33.60%)
- Repeat launch-to-firstconsumer ratio: 0.790474 (target <=0.90)
- Regression pass: true, no unresolved >10% items
- `final_shape=false`, `final_matrix_eligible=false`, `pass=false` by design for 8 rows

## Core probes

- `env_isolation_probe.json` — inherited policy present in parent, stripped; foreign files 0; cold derived write false.
- `cap_probe.json` — 8 MiB blocked; sampled peak 15,245,312; `cap_pass=false`.
- `derived_corruption_probe.json` — body-page corruption same size, mtime restored before read; read false, write true; release/event identity preserved.
- `tiny_pair_summary.json` — actual derived write wall/CPU/bytes, read validation cost, canonical cost, warm PIDs and amortization.

## Limits

No 100k/full matrix, no 86-court repeat, no 256-row smoke repeat. The tiny pair is method evidence only, not an economic or 12-ID acceptance.
