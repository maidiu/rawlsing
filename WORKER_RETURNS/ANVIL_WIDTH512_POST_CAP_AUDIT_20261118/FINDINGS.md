# WIDTH512 post-cap metadata audit — read-only

**Status:** `READ_ONLY_METADATA_INSPECTION_COMPLETE`  
**Source evidence:** construction return `9ba991847ec043ab12f00244c4d3a0301ddb0f98`  
**Source cap:** `WALL_600S`, `writing`, 1,951,192,968 partial bytes.  
**No rebuild, query, benchmark, recovery, checkpoint, mutation, or 1.8 GB copy.**

## Parquet footer presence and expected rows

All five present Parquet files start with `PAR1` but end with a non-`PAR1` tail. PyArrow rejects every footer. Therefore **exact file rows and row-groups are unknown/unreadable**, not zero.

| Family | Expected rows | File bytes | Footer | Readable rows / row-groups | SQLite ingested rows |
|---|---:|---:|---|---|---:|
| EmpiricalUniverse | 1 | 0 | absent file | n/a | 1 |
| RespondentIdentity | 512 | 99,217 | **no** | **unknown** | 512 |
| QuestionVariableBinding | 600 | 100,778 | **no** | **unknown** | 600 |
| RespondentEvent | 275,839 | 89,285,610 | **no** | **unknown** | 275,839 |
| RoutingEligibilityFact | 307,200 | 41,209,051 | **no** | **unknown** | **131,112 partial** |
| EmpiricalCoordinateFact | 512 | 0 | absent | n/a | 0 |
| WeightMeasureFact | 512 | 0 | absent | n/a | 0 |
| AuthoritySnapshot | 6 | 0 | absent | n/a | 0 |
| SourceUniverseRelation | 0 | 0 | absent | n/a | 0 |
| EmpiricalPredicateReplayBinding | 0 | 0 | absent | n/a | 0 |
| ComparatorReplayBinding | 0 | 0 | absent | n/a | 0 |
| DiscoveryBranchReplayBinding | 0 | 0 | absent | n/a | 0 |
| StructuralAdmissionReplayBinding | 0 | 0 | absent | n/a | 0 |
| event_locator | 275,839 | 22,499,128 | **no** | **unknown** | n/a |

SQLite counts are committed snapshot observations, **not proof of Parquet row counts**. The writer taps each object into Parquet and the same stream into I02, so the counts are useful as an ingest position, not as a file census.

## SQLite staging and hot journal

- Staging DB: `.s2b-direct-stage-cce5x0l2.tmp`, SQLite, 1,789,673,472 B.
- Journal: `.s2b-direct-stage-cce5x0l2.tmp-journal`, 8,325,712 B.
- Journal header: magic `d9d505f920a163d7`, `nrec=381`, initial DB pages `436604`, sector `512`, page size `4096`.
- DB pages `436932`; page size `4096`; freelist `0`; `journal_mode=delete`; schema version `9`.
- Tables: `objects=408,064`, `closure=408,064`, `scoped_names=512`, `event_occurrences=275,839`, `bindings=600`, `header=0`, `selectors=0`.
- Family position: universe 1, identity 512, bindings 600, events 275,839, routing **131,112 of 307,200**. No coordinate, weight, authority, or replay-family rows were ingested before the cap.
- Access was `mode=ro&immutable=1` with `PRAGMA query_only=ON`. **Caveat:** immutable access ignores the hot rollback journal. Uncommitted journal pages and their logical rows are unknown; no recovery, checkpoint, or mutation was attempted.

## Tap / I02 activity and publication

**Tap/I02 ingest was active.** The I02 staging SQLite exists, is populated, and its committed family position stops inside routing. The producer co-writes Parquet before consuming each object, and the final `.i02-proof.sqlite` was never linked.

**Validation/publication was not reached:** no `manifest.pending`, no `manifest.json`, no `releases/`, no final `.i02-proof.sqlite`, no header rows, and no selector rows. These are missing completion artifacts, not a failed validation verdict.

## Samples timeline

2,111 samples; first at 0.253 s, last at 600.148 s. Peak sampled RSS 128,729,088 B; final sampled scratch 1,951,192,968 B.

| Elapsed s | Scratch B | RSS B |
|---:|---:|---:|
| 0.253 | 0 | 23,838,720 |
| 1.103 | 1,908,736 | 60,678,144 |
| 10.116 | 50,579,895 | 122,970,112 |
| 60.186 | 476,119,766 | 125,992,960 |
| 120.014 | 479,652,998 | 113,258,496 |
| 300.284 | 1,291,052,950 | 125,710,336 |
| 450.105 | 1,572,837,786 | 74,600,448 |
| 540.200 | 1,800,602,809 | 80,592,896 |
| 600.148 | 1,951,192,968 | 83,271,680 |

File mtimes: identity 18:10:17.862 UTC; bindings 18:10:18.086; events and locator 18:17:42.496–.499; routing 18:20:16.244. The absolute run start was not stored, so these support ordering, not exact stage durations.

## Known / unknown

**Known:** cap at 600 s; writer stage; five footerless Parquet files; SQLite staging DB and hot journal; 408,064 committed objects; routing partial at 131,112; header and selectors empty; no publication/validation marker; samples and partial bytes.

**Unknown:** exact Parquet rows and row-groups; exact uncommitted journal contents; exact pending buffer contents; final I02 validation result; exact per-family completion times.

The smallest exact dynamic boundary available is the writer start lower bound: `fixture_context 0.00133 s + width_population 0.12537 s = 0.12670 s`; the writer then ran to the 600 s cap. No additional dynamic timing measurement is indispensable for this audit.
