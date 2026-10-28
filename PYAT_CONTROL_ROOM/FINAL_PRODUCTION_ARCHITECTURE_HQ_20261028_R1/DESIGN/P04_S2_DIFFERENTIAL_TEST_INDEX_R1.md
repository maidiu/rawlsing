# P04-S2 — 42 mandatory differential tests (Git succession index)

**Status:** Specified, NOT executed against a new I03 engine. Code base `299f41e97a43c67be9cc76a79fa49b48f4e12e54`. Every test must compare untouched old I03 native `EmpiricalFact.ref` and full `as_dict()`, execution replay.ref, provenance and authority, risk/denom refs, full zero-inclusive cells, source scope, negative detail and existing I05 consumer as applicable. Native positive sourcefree test then actual source only under its grant. Tests 03/21/22/23 partly covered by bounded 64-case I01/packet-helper probe; 20 float refusal separately native I01; **none constitutes new engine parity**. The complete matrix with evidence labels, technical expected outcomes and dependency gates is in archive `PYAT_P04_HQ_S0_S1_S2_20261028.zip`, SHA256 `7b74b7cc8cf5bf0e3e02fdec23b6e45bf7199876cb32dfc229f9cf41e0d5fbf5`.

| Test | Ticket | Falsification target |
|---|---|---|
| P04-T01 | B00 | freeze old accepted Fact.ref/as_dict & replay |
| P04-T02 | B00 | freeze old typed positive/negative & cells |
| P04-T03 | B01 | duplicate and shuffled visited objects |
| P04-T04 | B01 | same ref visited repeatedly |
| P04-T05 | B01 | same object ID incompatible hash rejects |
| P04-T06 | B01 | ref append only after native validation |
| P04-T07 | B01 | OR true+forbidden authority still errors |
| P04-T08 | B01 | AND false+evidence visits second leaf |
| P04-T09 | B01 | excluded invalid target remains skipped |
| P04-T10 | B01 | excluded missing weight remains skipped |
| P04-T11 | B01 | routing unknown/conflicting member sets refuse |
| P04-T12 | B02 | old full C11 manifest vs verified replay ref |
| P04-T13 | B02 | unverified forged manifest ref fails |
| P04-T14 | B02 | corrupt/revoked cache cannot mint release |
| P04-T15 | B02 | old cold ReplayManifest closure audit remains |
| P04-T16 | B03 | one cell projection yields identical replay/fact |
| P04-T17 | B03 | empty full domain preserves VALID_EMPTY |
| P04-T18 | B03 | full zero-inclusive domain not sparse |
| P04-T19 | B03 | duplicate domain cells reject |
| P04-T20 | B03 | Unicode exact numbers, no float |
| P04-T21 | B04 | same count different members have different identity |
| P04-T22 | B04 | same replay different provenance different Fact.ref |
| P04-T23 | B04 | visit ordering canonical sorted provenance |
| P04-T24 | B04 | same replay altered authority changes fact |
| P04-T25 | B04 | risk members vs denominator members kept distinct |
| P04-T26 | B04 | runtime grant revoked no permission from refs |
| P04-T27 | B04 | ContextVar runtime switch never reuses permission |
| P04-T28 | B05 | first error class/detail unchanged with multiple failures |
| P04-T29 | B05 | different negative details different ref |
| P04-T30 | B05 | source-indexed versus authorized composite |
| P04-T31 | B05 | unary conditional J2 J3 exact same-person |
| P04-T32 | B05 | same C11 original ref across legacy and view |
| P04-T33 | B06 | I05 every candidate role/full receipt unchanged |
| P04-T34 | B06 | fixed I05 not Authority37 fracture completion |
| P04-T35 | B06 | consumer-first and actual resume complete cells |
| P04-T36 | B07 | cold old/new native query replay exact refs |
| P04-T37 | B07 | full original source-equivalence/replay audit |
| P04-T38 | B07 | source attestation and authority invalidations |
| P04-T39 | B07 | actual cold/warm 16GiB host RSS/disk/times |
| P04-T40 | B07 | all35 diversity and Sorok permission firewall |
| P04-T41 | B07 | independent hostile original/new falsifier review |
| P04-T42 | B07 | ref-only alone cannot claim 7.9GB elimination |

**Admission gates:** B00 independent old golden, B01 ref ledger and original stage checks, B02 I02-certified replay manifest ref + full audit, B03 exact once-cell projection, B04 both native identities, B05 errors/runtime/source-use, B06 I05/P05 consumer and P06 science boundary, B07 hostile review, source-free and qualified original host measurements. Never accept only equal numeric counts or only equal execution replay ref.
