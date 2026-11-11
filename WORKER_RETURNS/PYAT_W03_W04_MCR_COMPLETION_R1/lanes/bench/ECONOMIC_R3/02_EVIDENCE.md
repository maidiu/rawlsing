# Small evidence

## Exact source inputs

- current benchmark code source head: `07f37e47893fdbc956766cea7d3ef550f064d8c7`
- frozen baseline: `46b7325637e68f78ccc7487d4b1abc7009c5ac0b`
- protected baseline: `4f3413fc5c37b589be3412f826bf8f68ee617d4a`
- coupled source pins: `2709733e`, `558f4169`

## Parity (64 rows cold, actual I03/I05)

| Profile | Events | Fingerprint (current / 46b / 4f identical) |
|---|---:|---|
| narrow | 128 | `97c93ac1...` |
| repeat | 384 | `adca1205...` |
| wide | 384 | `4acb0294...` |

Current cold has **zero** derived files (ECON-M1). No canonical persistence in `cold`.

## Full-matrix 64 (actual normal caller + governed policy)

- cold: derived miss/write, canonical files 13
- warm: derived hit (same envelope/mtime), canonical reopen hit, consumer fingerprint parity true
- delete/rebuild: derived miss/write, canonical rebuild
- final matrix eligibility false; acceptance status non-final diagnostic
- current cold wide stage peak 63,348,736 B vs protected 103,825,408 B (small diagnostic; not final)
- repeat no-acceleration restart ratio 1.447 (>0.90) → `DO_NOT_RETAIN`; no PASS

## Falsifiers

- 8 MiB cap: `BLOCKED_EXACT_DEPENDENCY`, `cap_enforced=true`, reason `CHILD_RSS_EXCEEDED_AUTHORIZED_CAP_BEFORE_COMPLETION`.
- no-baseline `--acceptance-gate`: exit 2, status `NO_BASELINE`.
- wrong rows/host and cold-only missing-warm baseline: gate pass false, no crash.
- three warm fresh processes: PIDs `78863, 78906, 78951`, derived hits `[true,true,true]`, canonical hits `[true,true,true]`, amortization `0.0681`.

`evidence_summary.json` contains file hashes and compact receipts; raw JSON files are committed under this sublease.
