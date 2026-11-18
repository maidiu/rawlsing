# Writer tap / I02 proof timed run

## Status

**`CAPPED_WALL_600S__ATTRIBUTION_TO_I02_PROOF_RESIDUAL`**

One supervised 512×600 run only; no retry, no query, no publication.

- Instrument: `9e46202457c4ad69e714045e6cf831f0251695c2`
- Writer: unchanged `68aa` / SHA-256 `068fc525…`
- I02 proof: `b70e9a49…`
- Run wall: **600.1917 s**
- Exit: `-15` SIGTERM
- RSS peak: **139,546,624 B**
- Scratch peak: **1,948,384,851 B**
- Partial bytes: **1,943,852,728 B**
- Output root: own `.local-data-width512-timed`; **not committed**.

## Attribution

| Boundary | Measured |
|---|---:|
| Context | 0.00121 s |
| Width population | 0.11345 s |
| Sink add inclusive | **117.1075 s** |
| Index add inclusive | **1.8972 s** |
| I02 proof active at cap | **594.4323 s** |
| Proof residual at cap | **≈475.4275 s** |

Proof residual = proof active − completed sink/index add. It is **not pure SQL**:
it includes validation, hashing, SQLite insert/commit and proof bookkeeping.
The proof call was still active at SIGTERM; residuals carry pending/reporting
uncertainty.

Per-family sink counts/times:

- `RespondentEvent`: 275,839 calls, 80.5758 s
- `RoutingEligibilityFact`: **127,139 of 307,200**, 35.6575 s
- `RespondentIdentity`: 512 calls, 0.7479 s
- `QuestionVariableBinding`: 600 calls, 0.1251 s

`RespondentEvent` was complete; routing proof was still being consumed. No
verification or publication stage was reached.

## Partial storage

- Proof SQLite DB: **1,789,673,472 B**
- Proof journal: **985,472 B**
- Parquet side-family bytes: 99,217 / 89,285,610 / 41,209,051 / 100,778 / 22,499,128
- Partial tree is unsealed and not in Git.

## Actionable boundary

**Dominant measured bucket: I02 proof residual (~475 s), not sink add.**
The residual is not yet divided into validation/hash versus SQLite
insert/commit. Do not implement a proof-stripping or speculative optimization.

Smallest next measurement: narrow test-only counters around
`_insert_object`, authority-ref walks, and SQLite commit boundaries on the
preserved writer. Candidate repair only after that: reuse the writer’s already
materialized row/projection at the tap boundary when populating proof tables,
retaining exact external I02, duplicate/occurrence/closure/negative/census,
atomic publication and recovery.

No claim that SQLite alone causes the cap. Correctness at `aee954…` /
`bbc3114f…` is not reopened.

## Raw evidence

- `RUN_RECEIPT.json`
- `PROGRESS.json`
- `SAMPLES.json`
- `BUILD_STAGES.json`
- `RUN_STDOUT.txt`, `RUN_TIME.txt`

**STOP after commit/push/remote verification.** No partial estate bytes committed.
