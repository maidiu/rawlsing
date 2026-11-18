# S1 — COMMON FRAME (frozen before architecture selection)

**Candidate root:** `WORKER_RETURNS/ANVIL_ARCHITECTURE_20261117/`
**Author:** one integrated architect, not HQ, not independent C, not H1.
**Frame:** `S1/FRAME.json`, digest
`7e7bfb9638f23894fd244a703e8a6b88d361f90fafa5b2b10ac78c1f24229913`
(the exact guard digest is recomputed over the canonical JSON; see `S1/FRAME_GUARD.txt`).
**Product cut inspected:** `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`.
**Protected currentness observed:** `31291d08179890852246c8742700e055168e9933`.
**Currentness register snapshot:** `b830458c3ebfe0a3f0e2d18e516e68b90324c88a` (Nov 15 R03/W05), distinct from protected `31291` and the later `cea2d4d` prepared session.
**Source/evidence cut for the 118 inventory:** `7fc00289dd801d2d0a8ce159986c7595fc27a4d9`.

This frame is an author checkpoint, not independent acceptance. The accepted
16 requirement narratives and 118 mixed identity rows are the reviewed common
frame; the added `frame_basis`, `grounding_delta`, `actual_code_pins`,
`cost_witness` and source-snapshot index are this author's reconciliation of
actual current code and are subject to independent C.

## 0. Currentness and authority state actually read

- The canonical first-position protected OATH and the full PROGRAMMA entrypoint
  were read from the frozen protected evidence at `31291`. The paired
  `CURRENT_PROGRESS.md` / `.json` revision is 10. This is a read, not HQ
  accreditation and not a protected write.
- `#1097` remains the P0 operating register (17 capabilities, 52 T1/T2
  contracts, 24 paths, 21 prospects). `#960` is the controlling sourcefree
  S01–S05 priority. `#997` is the S1-E source-body bridge; `#998` is the joined
  first-consumer vertical; `#1006` is the measured physical-cost court;
  `#1001` is the distinct-100k/6 GiB gate. `#1108` is documentary ANVIL
  preservation, **not** an architecture selection. `#1133` is the SEAM
  reverse-consumer advisory. No protected adoption follows from reading them.
- The product cut `cea2d4d` adds one authenticated cold saved C11 session reused
  across many I03/I05 operations. Its author reports 80 sourcefree tests and
  1.69–1.70× distinct-operation improvement. It has **no independent G5, no
  native/original35 grant, no production 100k claim**. The underlying accepted
  S2-C/D physical code remains the earlier scoped-accepted cut; the prepared
  session is a candidate descendant.
- `b830` is the Nov 15 R03/W05 materialization of exact issued query-role
  preimages and the v2 saved-fate join. It is older than protected `31291` and
  is not the current protected head. It is used here only for the actual
  sourcefree first-consumer route it pins.
- Native/original35 source rights, F1–F8/N9/N10W/SOROK actual first readers,
  independent C, protected H1 and 100k/6 GiB/1/10/100 economics remain
  unmade. No local flag changes that.

## 1. Actual accepted capital and its true first consumers

| Layer | Actual code/symbol | What it really is | First real consumer | Grade |
|---|---|---|---|---|
| Source projection | `pre553_source_i02_handoff.build_source_i02_handoff` / `SourceI02Handoff` | one source decode, typed family projection, temporary I02 certificate | S2-C body sink / native compiler | sourcefree scoped, TEST_ONLY where stated |
| Source→saved bridge | `pre553_source_saved_body_bridge.SourceSavedBodySink` | journals exact 13 family bodies to temporary private JSONL, then replays into frozen S2-C | `write_direct_estate` | sourcefree candidate; second I02 certification disclosed |
| Physical writer | `pre553_source_direct_parquet_estate.write_direct_estate` | one pass over 13 family iterators; Parquet/Zstd `body_json` + typed columns; event locator; temporary SQLite I02 proof; full physical re-read/re-encode verification; atomic manifest | `VerifiedDirectEstate` | scoped accepted sourcefree (`b7b697b…`) |
| Cold reader | `VerifiedDirectEstate` | hashes every member against independently held manifest; checks counts; refuses changed/revoked | `SavedC11Admission` | scoped accepted sourcefree |
| Native I03 view | `DirectEstateI03Session` | per-open temporary SQLite `events`/`members` index built by scanning all event and side-family row groups; lazy body reads | native `execute_empirical_query` | scoped accepted sourcefree |
| Native I03 evaluator | `execute_empirical_query` | existing authoritative query/risk/denominator/authority/fact/replay semantics | I03 facts / Batch / F1–F4 | native evaluator; sourcefree scoped |
| Native I05 | `execute_exact_bounded_discovery` | existing bounded discovery owner on the saved view | I05 branch/minority/recursive receipts | scoped accepted sourcefree |
| Prepared session | `PreparedI03Session` / `PreparedSavedC11Admission` | one exact `DirectEstateI03Session` reused by many I03/I05 operations; current/revocation checked after each | P0 repeated-operation consumer | author candidate, `cea2d4d` |
| Saved Batch/NORMAL/resume | `pre553_saved_workload_integration.execute_saved_batch/normal/resume` | adapters over existing shared owners; explicit owner-ACK refusals where shared files are not handed off | Batch/NORMAL/resume | typed owner hold / partial |
| F1–F4 | `pre553_analytical_composition.AnalyticalCompositionResult`, native joint/denominator/recursive code | true same-person k≥3, directional denominators, minority/recursive, typed missing | FF descriptive / later world | scoped accepted sourcefree; no native source-science issue |
| FF | `field_forge_conditional_support`, `pre553_learned_world_composition` | FF01 descriptive vs FF02 independent structural; learned M1/M2/B5 | N9/world and later owner | sourcefree scoped; FF02/N9 actual owner remains separate |
| SEAM/actor | `sorok_history.owner.HistoricalWorld`, `SurfaceParticular`, provider | separate actor/world reader; encounter/access boundaries | SOROK continuation | exact owner hold; no source→actor promotion |

**Critical actual-code finding.** The accepted writer and the #997 bridge are
correct but deliberately redundant:

1. Q2 projects the source once and builds I02 certificate **#1**.
2. `SourceSavedBodySink` writes 13 temporary JSONL journals (exact bodies).
3. Frozen S2-C replays the journals and builds I02 certificate **#2**.
4. S2-C then re-reads **every Parquet row**, reconstructs the object from
   `body_json`, recomputes `_row`, and compares every typed/identity lane.
5. A new process hashes **every member**, then `DirectEstateI03Session` scans
   **all** event and side-family row groups to build a temporary SQLite index.
6. Only then can one narrow I03 query run.

The 100k-shape sourcefree witness reports **3033.723 s** writer,
**310.16 MB** retained, **5.26 GB** staging, **4.39 GB** temporary I02,
**1.30 GB** native session index, and **562.362 s** for one pre-W05 selected
query. This is a cut-specific sourcefree cost failure, not comparable merely
because it is “100k”; the 3.245-events/respondent canary is not real-width
proof. These numbers are the frame's physical constraint, not an acceptance.

## 2. The 118 mixed identities — actual status, not 118 tickets

Counts: **118 = 29 K1_CAP + 26 PYAT_PC + 14 P4R + 10 SEAM_B + 8 SEAM_S +
8 ANVIL_L + 7 BOUNDARY + 16 TERMINAL**. 95 exact Git rows plus 23 ZIP
objects/scalars.

- `K1-CAP-01..29`: historical/current conservation identities. They are
  **PRESENT_PRESERVED** only at the source-bound/typed-consumer grade stated
  in each row, never as native scientific equivalence. `K1-CAP-24` (F26) is an
  exact source-owner hold, not a claim that the old caller exists.
- `PYAT-PC-*` ×26: **RETAINED_HISTORICAL_NONADOPTED**. No row is adopted by
  this architecture. They are prospective owner decisions, not implementation
  tickets.
- `P4R-R01..14`: **EXACT_OWNER_HOLD**. No proof is closed. `P4R-R02` is the
  F26 caller/invalidation hold.
- `SEAM_B` ×10, `SEAM_S` ×8, `ANVIL_L` ×8: future nonpreclusion / boundary
  requirements. They constrain present physical preservation (source native
  meaning, occurrence, missingness, time, weights, strata, language) without
  authorizing future psychology or world science.
- `BOUNDARY` T1–T7: seven typed boundary interrogations, not seven stages.
- `TERMINAL` ×16: F1–F8, N9, N10E, N10W, N11, N12, PRE-V3, SEAM, SOROK. All
  are explicit graph nodes or exact holds; none is an implemented reader merely
  because it is named.

The separate **52 T1/T2 contracts, 24 paths and 21 prospects** in #1097 are
continuing source obligations, **not** 97 additional implementation tickets and
not addable to 118. The 52/24/21 estate is navigational and negative; it does
not change the 118 identity statuses.

## 3. The 16 common requirements (frozen)

The exact rows, positive/negative probes and source pins are in
`S1/FRAME.json` (copied from the accepted common frame; hashes unchanged).
Their operative content:

| ID | Binding | What must survive physically |
|---|---|---|
| REQ-SOURCE-SEMANTICS | PRESENT_HARD | native question/option/routing/missing before normalization; no stratum→individual identity |
| REQ-C11-PERSISTENCE | PRESENT_HARD | exact body + locator + CURRENT; cold restore; a body hash alone is not source truth |
| REQ-CURRENT-I03-I05 | PRESENT_HARD | sourcefree I03/I05 labeled sourcefree; never relabeled native |
| REQ-HISTORICAL-DDM | PRESENT_HARD | V549/V550/V550J/F26 semantic functions; old carrier/bugs not required |
| REQ-F1-F4 | PRESENT_HARD | true same-person k≥3 joint, separate denominators, branch/minority |
| REQ-FIELD-FORGE | FUTURE_NONPRECLUSION | FF01 descriptive vs FF02 independent structural; no opinion→power |
| REQ-SEAM-WORLD-ACTOR | FUTURE_NONPRECLUSION | Other/encounter/access/SOROK; no survey→private knowledge |
| REQ-AUTHORITY-RECOVERY | PRESENT_HARD | I02 independent source comparison; revocation; cold restore |
| REQ-RESOURCE-ECONOMICS | PRESENT_HARD | 100k/6 GiB/1-10-100 **NOT_RUN**; no synthetic green claim |
| REQ-MULTIWAY-JOINT | PRESENT_HARD | even/odd parity witnesses; pairwise product insufficient |
| REQ-DENOMINATOR-MISSING-ROUTING | PRESENT_HARD | forward/reverse distinct eligible bases; NOT_ASKED is not zero |
| REQ-PHYSICAL-WORKLOAD-1-10-100 | PRESENT_HARD | 600–1,300 slots, process-tree, distinct operations; 3.245 is not representative |
| REQ-SOURCE-I02-REVOCATION | PRESENT_HARD | independent source comparison; revoked prepared member refuses |
| REQ-FF01-FF02-WORLD-ACTOR-FIREWALL | FUTURE_NONPRECLUSION | survey fixed, independent world/structural change only changes qualified world object |
| REQ-TERMINAL-F5-F8-N11-N12 | FUTURE_NONPRECLUSION | each terminal producer/authority/time/first reader or exact hold; not a serial pipeline |
| REQ-HISTORICAL-NOADOPTION-CONSERVATION | PRESENT_HARD | 26 NOT_ADOPTED and 14 HELD remain; no false adoption/closure |

`EXTERNAL_OWNER_HELD` rows are owner-held, not present-hard losses. A present-hard
requirement cannot be relabeled future merely because the physical design is
inconvenient; a future-owned science cannot be self-issued.

## 4. Source-specific loss / first consumer / physical consequence

The following are the non-negotiable information losses that constrain the
physical arrangement. Each is already in the 118 rows; the table makes the
physical consequence explicit.

| Source distinction | If lost | First consumer that breaks | Physical consequence |
|---|---|---|---|
| native option/code/form/translation/routing | normalized label replaces source meaning | S01→C11 native first read | keep native refs and exact body; do not derive only from display labels |
| respondent vs occurrence vs repeated/ranked event | first-value pivot erases repeated answers | I03/F4 and future repeated/ranked consumers | event table keyed by respondent + occurrence; no `aggfunc=first` |
| eligible / asked / observed / refused / inapplicable / routing-unknown | missing becomes zero / false denominator | F2 reverse, F4 risk set, F3 minority | typed state column + exact denominator basis; no one common denominator |
| survey design/stratum/PSU/weight | stratum becomes individual identity or weight=1 | F2/F4 weighted estimands | keep design and weight refs separate; typed absence |
| true same-person k≥3 | pairwise marginals replace joint | F4/FF | store respondent-coherent event rows; preserve joint support, not pairwise summary |
| observation/wave/as-of/actor time | wave time becomes childhood or present world | F7/N9/actor | separate time fields and graph time modes |
| source root/authority/revocation | self-consistent hash becomes source truth | I02/CURRENT/cold restore | independent roots + revocation; no producer-only proof |
| output evidence/replay | every query re-emits full corpus | downstream F1–F4/FF/N9 | content-addressed fact/replay fragments, shared denominator/risk sets |

## 5. Holds that are part of the frame

1. **Economics:** native dense 100k 600–1,300 slots, process-tree ≤6 GiB,
   cold 1/10/100 distinct operations, retained/scratch/output are **NOT_RUN**.
   The 3033.7 s/5.26 GB sourcefree witness is evidence of a cost problem, not a
   100k production acceptance.
2. **F26:** exact original caller/invalidation remains `K1-CAP-24` /
   `P4R-R02` / `PYAT-PC-R11-21`; no invented body or equivalence.
3. **Original35/source/science/actor:** no bulk 35-source prerequisite, no
   native original35, no FF02/N9/N10W/SOROK actual first reader.
4. **Historical statuses:** 26 NOT_ADOPTED, 14 HELD, 52/24/21 separate.
5. **Independent C / H1:** not performed by this author; no protected merge.
6. **Semantic truth:** exact bytes and authored summary are separate; the
   summary remains external C/source-owner review.
7. **Batch/NORMAL/resume:** existing native engines and saved adapters exist,
   but shared-file owner handoffs for complete Batch/NORMAL/resume are still
   typed holds, not silently claimed.

## 6. What this frame deliberately does not decide

No physical backend, no index format, no query engine, no new database and no
future science. Those are S2/S3. The frame only fixes the source, identity,
consumer, loss, authority and hold boundary that any architecture must satisfy.

## 7. Guard result

`S1/FRAME_GUARD.txt` records the exact `r7_integrated.py FRAME` invocation and
the local result `PASS_LOCAL_COMMON_REQUIREMENTS_SOURCE_IDENTITY_NOT_NATIVE_AUTHENTICATED`
with 16 requirements, 9 domains and 118 inventory entries. This local PASS is
not independent C, source authentication of every authored meaning, native
execution, or H1 receiving.
