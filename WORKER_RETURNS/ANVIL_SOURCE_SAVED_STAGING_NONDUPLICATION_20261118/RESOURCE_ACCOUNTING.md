# Resource accounting and limits

## Fixture phase observations

| Phase | I02 passes this phase | Projection spool | Body journal | Explicit first cert | Writer stage | Root total |
|---|---:|---:|---:|---:|---:|---:|
| baseline first I02 complete | 1 | 31,100 | 63,356 | 176,128 | 0 | 270,584 |
| baseline writer entry | 1 | 0 | 78,168 | 176,128 | 0 | 254,296 |
| baseline writer I02 complete | 2 | 0 | 78,168 | 176,128 | 288,601 | 542,897 |
| baseline complete retained | 2 | 0 | 0 | 176,128 | 0 | 532,787 |
| candidate sections ready | 0 | 31,100 | 0 | 0 | 0 | 31,100 |
| candidate writer I02 complete | 1 | 31,100 | 0 | 0 | 288,601 | 319,701 |
| candidate complete retained | 1 | 0 | 0 | 0 | 0 | 356,659 |

Baseline peak observed phase: **610,955 bytes** (baseline writer complete).
Candidate peak observed phase: **387,759 bytes** (candidate writer complete).
Observed removal: **223,196 bytes**, with baseline 2 I02 passes and candidate 1.

The final retained bytes are equal because both outputs are the same exact
estate; the difference is temporary assembly. The candidate still uses the
projection JSONL spool and the existing writer's one-pass I02/Parquet stage.

## Live aggregate snapshot (read-only, not sampled)

From `evidence/SRC04_LIVE_STAGING_FOOTPRINT.json`:

- projection JSONL: 4,505,034,543 bytes
- replay body journal: 8,276,350,027 bytes
- writer/direct stage: 13,743,239,168 bytes
- free bytes: 16,101,466,112
- launcher cutoff: 12,970,801,234 bytes

The candidate removes the replay body journal (**8,276,350,027 bytes in this
snapshot**) and one explicit I02 pass. It does **not** remove projection JSONL or
the existing writer's one-pass stage. Therefore the proof supports lower
temporary assembly, not a guarantee that a real run will stay above the
launcher cutoff. A full real run remains out of scope and must not be inferred
from this fixture-sized measurement.
