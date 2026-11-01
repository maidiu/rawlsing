# CURRENT RECEIVER AND CUT MAP

## Current PREMAIN cut

- Read live at start and end:
  `8e44ca9c751049d65e6def47600b5c073ee04b29`
  (`integration/pre-main-reconciliation-r1`, commit date 2026-10-31T02:26:29-04:00).
- Exact `ls-remote` readback at both ends matched this 40-hex SHA.
- Exact primary presence of the 97: **0/97 blobs, 0/97 paths, 0 proved callers**.
- No PREMAIN file was modified by this investigation.

## Actual current test-only receivers

| Receiver | Exact branch tip / content | What it actually carries/executes | 97 rows served | Proof grade |
|---|---|---|---|---|
| RRIF R2/R3 sourcefree person/writer closure | `agent/sorok-rrif-r3-four-unintegrated-assets-genuine-consumer-fanin-20261031` @ `248618e6ea9549439b5a146246bc1eb2e0076cf6` (R2 content `1745fbb68d...`, R2 review `8090a1ea30...`) | `SOROK_PRODUCT_CONTROL_ROOM/RRIF/CODE_CANDIDATE/RRIF_R2`: 444-file vendored closure; `joined/` modules; R2 `tests/test_join.py` + `tests/test_rrif_r2_c12.py`; R3 extension `rrif_r3_extension/` | C8O/BP1/BP2/BP2P4J/BP3/BP4/G18/R26V/R27P/R31E/R31J; S36 base vendor files | R2 return records **20/20**; R3 return records **9/9**; exact `SOURCE_MANIFEST.json` blobs; NOT_RUN here |
| I1 sourcefree continuing person | `agent/sorok-i1-sourcefree-continuing-person-joined-implementation-20261030-r1` @ `7d44e30064f8e873e1a3ff9cb05fe75456756b88` | `WORKER_RETURNS/SOROK-I1-CONTINUING-PERSON-R1/candidate`: BP2P4J vendor + BP4R `GuardedC12Store`/`c9_actor_r3`; `bp2p4/i1_product.py` `GuardedJoinedProduct`; `tests/test_i1_guarded_consumer.py` | BP2P4J (exact vendor), BP4 (via BP4R guarded successor) | I1 return records **50/50** (33 BP2P4J + 9 BP4R + 8 I1); NOT_RUN here |
| G17 hostile-material repair | `agent/sorok-g17-forged-material-future-child-c9-source-repair-r1` @ `8b9a39da552a224bddf486603179f565003f38bb` | Candidate overlay: `lab_sgi1/continuation.py`, `lab_sgi1/pipeline.py`, `c9_handoff_consumer.py`; reviewer and author courts | G17 original cut `90d0eb79...` (three original REDs closed) | Patched reviewer **14/14**, patched author **13/13**, cold replay; original **11/3** preserved; NOT_RUN here |
| RA-D executed S39-S52/G18/JOIN-E/language | `agent/rabochii-sorok-20261026-ra-d-mac-executable-reality-r1` @ `6d3610c576dc...` | Exact S39-S52 closure; G18 `lab_sgi1`; JOIN-E `joined`; language mediation; `EXECUTION_LEDGER.json`; focused tests and entrypoints | S36/S37/S39-S52, M35, language mediation, G18, JOIN-E | RA-D records **131 focused sourcefree tests** and individual suites (10/10/21/17/17/12/13/5/13/13); NOT_RUN here |
| F0-R3 portable source custody | `agent/sorok-syn02-f0-r3-source-custody-repair-r1` @ `70470a9fe3593f7561e716ec30e2a2ebcc61885b` | `WORKER_RETURNS/SOROK-SYN02-F0-R2-PORTABILITY/source_manifest.json` (31 sources), `tests/test_f0_source_portability.py`, `tests/test_source_custody_r2.py`, `test_r3_adversarial.py`, `s52/source_registry.py` | S48/S49/S51/S52, G18, R30A; S49 `CUTS` names M35/S36/S37/S39-S52/language/JOIN-E | Source manifest and source-custody tests present; NOT_RUN here |
| M04R terminal ADP017 repair | `agent/sorok-r4-m04-unjournaled-adp017-terminal-repair-20261030` @ `8f200fd6ff6ce10e9effb017d2c265163e287105` | `WORKER_RETURNS/M04R-R4/candidate/claim_provenance.py` + `test_m04r_journal_coverage.py` | M05 row 50 predecessor | M04R return records 51/51, 587/587, 4 new controls; NOT_RUN here |
| C0RI onecall independent court | `agent/userdirect-sorok-20261018-onecall-c0ri-independent-repair-court-r1` @ `5abd3c5d243c...` | Contains repaired C0R `onecall_c0.py` plus independent historical/new hostile tests | Onecall C0R row 78 | Return records unchanged 18 historical + 4 new REDs; no product consumer |
| OC5 custody reproduction | `agent/sorok-oc5-custody-49-hostile-defect-repair-r1` @ `e8b127b68c18...` | Reproduces OC4 blob `af2b7e94...`; **no patch**; 349/66 and 159/49 | OC4 predecessor, not OC6 | Owner HOLD; later than OC6 but did not carry OC6 |

## Exact 97-row carrier groups

| Family | 97 rows | Actual receiver / successor |
|---|---|---|
| BP joined person/writer | 016, 017, 018, 019, 020 | RRIF R2 `248618e6`; I1 `7d44e300`; HR1 BP2P4J repair `0636d257`; BP4R `693d25bf` |
| G18/G17 material history | 012, 013, 014 | G17 repair `8b9a39da`; G18 in R2 `248618e6`; RA-D `6d3610c5`; F0 `70470a9f` |
| C8O/OUT writer | 009 | R2 `248618e6` exact `outbox_prototype.py` blob `33184076`; I1 vendor `7d44e300` |
| Historical actor/expression | 022, 023, 027, 028 | R2 `248618e6`; JOIN-E `7bf2da30`; RA-D `6d3610c5` |
| M35/S36/language | 030, 031, 275 | S49 `CUTS`; F0 `70470a9f`; RA-D `6d3610c5` |
| S37-S52 | 278, 280-293 | RA-D `6d3610c5`; S49/S52 `6604f2d9`/`c821b488`; F0 `70470a9f` |
| CAN2/M memory/claim | 057, 062, 065, 068, 071, 072, 075 | M01 `02187a14`; M03 `e1f7a74e`; M05 `8b7f3ed2`; MS3 `48200cf0`; M04R `8f200fd6` |
| SGI/G12 genealogy | 050, 054, 078, 087 | G12 `27f2dbfe`; G15/G17/G18 `lab_sgi1` |
| OC custody | 061, 063, 066, 069 | OC6 `873ce1c7`; C07P `805d0a07`; OC5 `e8b127b6` (reproduction only) |
| C0P/C0R2 Pyat port | 048, 056, 077, 090 | C0P `154a4dd5` -> C0R2 `55d2daa4` |
| V2 B-first | 091-098, 238 | B2R1 `358fd108`; B3 `47b46a85`; M4 `858bc2d9`; experimental M2 `e8f375e9` |
| Onecall C0 | 250-253 | C0R `98fdbdf0`; C0RI `5abd3c5d` |
| Low/doc/test | 079, 242, 244, 257, 261 | Document/test evidence only |
| Old same-person join | 237 | Defective predecessor of JOIN-E `7bf2da30` and R2 `248618e6` |

## Exact 97-row code that has **no** later receiver

- C0R3 row 007: no R2/I1/F0/RA-D/PREMAIN consumer.
- OUT14 row 089: no later carrier; its own new court collection-ERROR/NOT_RUN.
- SR outbox row 053: no later carrier.
- OC6 row 069: no later carrier; OC5 used older OC4.
- C07P row 073: no later carrier.
- C0R2 row 090: no Sorok product consumer.
- V2 B3/M4/experimental M2 rows 097/098/238: no later carrier.
- CLR rows 003/004: no later carrier.
- RFA-06C2 row 046: no later carrier.
- R3 final courts rows 047/052/054/055/075/081: no later carrier.
- Onecall C0R row 252: exact code is in C0RI, but no production consumer.

## Accepted 8 crosscheck map

| Accepted cut | Relationship | Reuse consequence |
|---|---|---|
| B3AS `16f15a12` | No exact 97 descendant identified | Do not repeat accepted B3AS review. |
| C9R `6fa29399` | Primary proof-integrity file, not runtime engine | Do not requeue C9R; locate a real C9 engine separately if needed. |
| R26E `eb0a2b90` | C12 integrity engine, vendored by R2 | Do not rebuild R26E; select a real C12 consumer. |
| R29P `001b506f` | Shared `historical_actor_producer.py` blob with R26V/R27P/R31J | Shared blob is not unique shared change; branch-unique files differ. |
| R30A `ce0dfc67` | First-neighbor session, vendored by R2 | Do not rebuild R30A. |
| R30G `024e77f0` | Shares the same producer blob as R29P | Do not infer R30G=R29P from blob identity. |
| JOIN-E `7bf2da30` | Accepted same-root join; old `13dfd6ba` defective | Do not resurrect old join defect. |
| same-person old `13dfd6ba` | Older defective cut | Superseded by JOIN-E/R2 same-root consumer. |

## Non-97 later assets (do not confuse with residual A)

`C9C12-R2`, `CP-A5-R2`, `B-F1CR-R2`, `V3CORE-R1`, `R6`, `R41`, and the F0/SYN02 sourcefree
build are later named assets outside this 97-row workload. They are cited only as carriers or
context. They do not become current PREMAIN or native authority through this return.
