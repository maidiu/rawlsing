# FIABC-LM2-R1F — Minimal Local Cost Audit

Status: `SPECIFIED__NOT_EXECUTED__NO_MEASURED_LOCAL_COST_CLAIMED`

## Exact bounded work

The frozen local successor performs the following bounded operations and no others:

| Operation | Exact bounded quantity |
| --- | ---: |
| Raw source hash verification | one sequential pass over 185,163,494 source bytes |
| SAV decoder calls | exactly 1 |
| Requested source variables | exactly 2 |
| Requested source rows | exactly 97,220 |
| Application-level physical cells emitted | exactly 194,440 |
| Q291 variables | Q291G5 ordinal 388; Q291P5 ordinal 394 |
| Carrier validation | one local validation of the emitted carrier |
| Carrier SHA-256 | one sequential pass over the emitted carrier |
| Candidate/C11/oracle/P2X work | 0 |

The two-variable output frontier is 194,440 cells versus the full WVS7 physical universe of 59,595,860 cells. The successor therefore avoids constructing or traversing the 613-variable physical universe at the application layer.

## Important decoder caveat

The SAV is compressed. A selected-column `pyreadstat` call may internally scan/decompress more of the source stream than the two requested columns imply. This court therefore does **not** claim that only two-column byte ranges are physically read from disk.

The lawful minimization claim is narrower and exact:

- one decoder invocation;
- only two requested logical variables;
- no application-level construction of the other 611 variables;
- no second source decode;
- no 613-column physical-cell stream;
- no C11 build.

## Memory posture

The normative script holds a two-column 97,220-row frame plus the emitted 97,220-row carrier document before serialization/validation. That is intentionally bounded far below the historical all-613-column R5/SR07 carriers that hit multi-gigabyte resource tripwires.

R1F makes no numerical RSS claim because no local execution occurred.

## Measurements that remain intentionally unknown

Until the separately authorized local successor runs, all of the following remain unmeasured:

- hash wall time;
- selected-column decoder wall time;
- serialization wall time;
- carrier-validation wall time;
- total wall time;
- process RSS/peak memory;
- emitted carrier byte length;
- emitted carrier SHA-256;
- local `pyreadstat` version.

The local receipt must record measured values only. No projection, extrapolation, or synthetic zero may be substituted.

## Why this cost is irreducible

Browser recovery cannot provide the 194,440 ordered physical observations. A source hash, row-binding digest, semantic comparator, question metadata record, release identity, or aggregate digest cannot be inverted to those cells.

Consequently, at least one operation that observes the source values of both selected variables across all 97,220 rows is required. The frozen successor performs exactly that operation and stops.

Terminal inherited from the archaeology court:

`BROWSER_ARCHAEOLOGY_EXHAUSTED__LOCAL_Q291_EXTRACTION_PROVED_IRREDUCIBLE`
