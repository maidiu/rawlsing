# PYAT960 Q2 S1-E — A implementation handoff

**Role:** A / bounded source-direct implementation author · **session:** `ses_e3122f686ffeByL78cGOKAacTS`
**Fixed rival:** B `ses_e3120baacffegE3ZnR5uZcHb0N` (idle)
**Branch:** `agent/pyat960-s1e-a-r1`
**Base:** `591056a948fb0fdd68adbd581301dd903485adc8`
**Return implementation SHA:** `75d09e87dbaf8273fab3a5ece2bb7981328113ce`
**Contract v1 SHA-256:** `0ed0384411441b2f647dc5ea3369931c88d408c71802ec8cd7eaff00c3052a40`
**Provisional ABI SHA-256:** `cbc8988b6f38fc354311d7db7afe02a5bd66c8e53ab2c6f9cca2b5134d383f54`
**Integration:** `UNMERGED` · **G5:** `NOT_RUN` · original task not complete.

## 0. Required S01–S05 / reuse acknowledgements

- The five terminal outputs are: S01 governed source meaning/entitlement, S02 exhaustive qualified operation/fate census, S03 one compact authenticated source-direct C11 estate, S04 full native I03/I05/Batch scientific outputs, and S05 durable learned products. Q2 is the S1-E source→direct I02 handoff, not S03/S04/S05 completion.
- The selected destination is the Oct 28 respondent-coherent typed C11 estate plus the Nov 11 lock: source-direct bounded I02, one semantic corpus, no compulsory full `C11LogicalRelease.public_objects/internal_records`, no giant `ReplayManifest.closure_refs`, and no second authoritative full event corpus. Rejected physical order: eager full-object C11 candidate first, then a compact copy.
- Reused source/operation/receiver functions are listed in §3 with pinned path/blob. The legacy full-object writer and `direct_sections_from_candidate` are retained only as read/compatibility evidence where needed; they are not the Q2 production order.
- Historical W03/W04 memory pilot is preserved as a negative: its matched direct saved-artifact pilot peaked at `6,468,513,792` bytes, above the `6,442,450,944`-byte 6 GiB cap and was killed. Q2 makes no 100k/6 GiB claim and does not reuse the old full-object-first order.
- Named first readers: existing S2-B `SourcefreeDirectI02Sections` + `build_sourcefree_direct_i02`; existing `VerifiedExternalI02` cold reader/native bridge where host-capable. G1–G5 are accounted below; G5 is not self-issued.
- Live ownership: only this new worktree/branch and `WORKER_RETURNS/PYAT960_S1E_A/` were written. Upstream S1-B/S1-C/S1-D/S2-B owners, protected facade, #922, W03/W04, other worktrees and controller paths were not modified.
- Highest-risk false-green: treating a successfully built direct SQLite certificate as proof of the native I03/Batch consumer on a host where `VerifiedExternalI02` cannot open its Linux `/proc/self/fd` path. This return explicitly separates those grades.

## 1. Exact artifact

- New code: `rawlsing_next/pre553_source_i02_handoff.py`
- New tests: `rawlsing_next/tests/test_pyat960_s1e_source_i02.py`
- Return: `WORKER_RETURNS/PYAT960_S1E_A/receipt.json`, `00_HANDOFF.md`, `resource_probe.py`, `evidence/`
- Commands:
  - `python3 -m pytest -q rawlsing_next/tests/test_pyat960_s1e_source_i02.py -o addopts=''`
  - `python3 -m pytest -q rawlsing_next/tests/test_pyat_r3_s1c_source_operation_fates.py -o addopts=''`
  - inherited S1-B and decoder/custody suites in `evidence/`.

## 2. Implemented stream API

`build_source_i02_handoff(...)` accepts an accepted R157 `SourceConfig`, a permitted physical SAV/DTA path, a destination `.sqlite`, the S1-C `FrozenInputCensus`/`SourceInventory`/`GrammarPolicy`/`ScientificFrontier`, optional source-native keys for keyed configs, and an optional independent source-read resolver for an original source.

Flow:

1. Validate destination, source-native key requirement and source/config identity.
2. Build the existing `GovernedC11Projection` from the accepted config.
3. Verify the complete supplied operation/fate census **before any source byte open**: exact source SHA/id/slot union, operation/fate hashes, source-vs-science anti-join, duplicate detection, pending/execution/result axes, unknown/excluded/deferred/inventory ledger conservation, optional-weight RAW fates.
4. One permitted physical read/parse; one bounded cell pass generates only `RespondentEvent`, `EmpiricalCoordinateFact` and `WeightMeasureFact` records into a private ephemeral JSONL spool. Static universes/respondents/questions/routing/authorities/relations/replay states come from the existing projection.
5. Build the exact `SourceReleaseManifest` counts after the one pass and hand all 13 family iterables to the existing `build_sourcefree_direct_i02`.
6. Delete the private spool; return external `ExternalI02Roots`, manifest/counts, census audit, all operation fates, source/row counters and resource counters.

`open_certificate()` exposes the existing `VerifiedExternalI02` cold reader. `open_direct_native_i03(handoff, repository, release_ref)` exposes the existing direct→native selector bridge for a caller-supplied already-sealed body repository; it never builds a legacy candidate.

## 3. G1 reuse matrix (function-level)

| Prior owner / frozen locator | Disposition | Function/consumer | Reason |
|---|---|---|---|
| `rawlsing_next/pre553_r157_projection_adapter.py` blob `d4d84ef164feba6fb0de0851568738eb5f5e937d` | `REUSE_AS_IS` | `SourceConfig`, `build_governed_c11_projection`, fixture decode, source-read admission, manifest identities | Exact R157 source/config/row/occurrence and permission semantics are already accepted; no second source semantics owner. |
| `rawlsing_next/pre553_physical_decoder.py` blob `85ce3290d1dc8e1eb1362c22f200715b3d22758a` | `REUSE_AS_IS` | `decode_sav/decode_dta`, `iter_cells`, custody/metadata | Bounded physical reader; no decoder rewrite. |
| `rawlsing_next/pre553_source_backed_c11_facade.py` blob `7c967b8227a2843971c7cd9f61f3deaa423af866` | `REUSE_AS_IS` | `GovernedC11Projection`, `_event`, `_coordinate`, `_weight`, `_cell_key` | Existing semantic/occurrence construction; Q2 only streams its records. |
| `rawlsing_next/pre553_operation_fate_census.py` blob `dd5bf3940083679612d73f98e6a7b7711c223fd5` | `REUSE_AS_IS` | `verify_frozen_inputs`, `FrozenInputCensus`, `ScientificFate`, `SourceQualifiedCandidate` | Exact S1-C pre-source operation/fate anti-join and optional-weight/pending conservation. |
| `rawlsing_next/_pre553_direct_i02_sourcefree.py` blob `451727511af7f727b082c518aae2f4a3dbe2ba3a` | `REUSE_AS_IS` | `SourcefreeDirectI02Sections`, `build_sourcefree_direct_i02` | Actual direct I02 receiver and certificate builder; no full C11 candidate. |
| `rawlsing_next/_pre553_external_i02_certificate.py` blob `cd5368e46a5f2d6016afc2d421717b4191a03005` | `REUSE_AS_IS` | `ExternalI02Roots`, `VerifiedExternalI02`, `install_direct_sourcefree_i02_i03` | Existing external-root verifier/native bridge; Linux-host capability is explicit. |
| `rawlsing_next/pre553_issued_workload.py` blob `47db61752d08fa5c774436b2c29e489a8d91c3f2` | `HOLD_AUTHORITY` | S1-D current issuer | No production CURRENT decision is minted; sourcefree fixtures use the test-only source-read stand-in. |
| `direct_sections_from_candidate` / legacy full-object writer | `LEGACY_READ_COMPAT` | identity comparator only in tests | Q2 production path does not build full candidate/public/internal/ReplayManifest. |
| W03/W04 compressed-body path | `RETIRE_PROVED` for Q2 physical order | historical economics only | Full-object-first construction and the failed 6.47 GB pilot are not the Q2 foundation; branches remain paused. |

No-loss tests: S1-B inherited B01–B09 packet suite 33 passed; S1-C operation/fate suite 18 passed; decoder/custody 56 passed/1 skipped; Q2 tests 11 passed. See `evidence/`.

## 4. G2 result — direct I02 positive/change/restore

- Actual generated nonrespondent SAV and DTA bytes → bounded decoder → accepted R157 projection → one cell pass/spool → existing direct builder → external logical/physical roots.
- Positive: `SourceI02Handoff` external roots, exact manifest counts, 13 sections consumed; direct builder output validated structurally; event/respondent refs match the existing sealed-owner fixture identity for the same source.
- Changed valid source meaning (response-state mapping) changes direct logical/physical roots and exact event refs; exact restore reproduces the original roots and event refs.
- Operation/fate change: a different frozen frontier changes the conserved operation/fate audit; no dropped operation IDs.
- A denied original-source decision refuses before destination/source bytes; no output artifact.
- **G2 direct I02 builder: PASS at sourcefree direct-I02 grade.**
- **G2 native I03/Batch direct bridge: HOLD_DEPENDENCY.** The existing `VerifiedExternalI02` requires Linux `/proc/self/fd`; this host is Darwin. The Q2 code path is implemented (`open_certificate` / `open_direct_native_i03`) but no native cold consumer is claimed here. The existing S2-B cold suite records this host dependency, not a fabricated green. A Linux host must run the native bridge.

## 5. G3 hostile controls

- Census omission, duplicate operation, source SHA/id mismatch, occurrence/item not in physical source, wrong authority/source identity, and operation-target absence refuse **before** source open (monkeypatched decode count zero).
- Destination collision/new-SQLite refusal is typed and creates no second output.
- Unknown/excluded/deferred/inventory-ledger and pending/execution/result axes are consumed by `verify_frozen_inputs`; optional-weight sample RAW remains eligible while population HELD fates remain held.
- Direct builder retains its existing duplicate occurrence/respondent/authority/path/root/self-hash refusals.
- Original35 held ledger and 26 unjoined source items remain inherited preparation, not Q2 science.

## 6. G4 resources (small sourcefree fixture; not 100k)

`evidence/resource.json`:

- 1,200 rows; 1,200 events; 1,200 coordinates; source reads 1; cell passes 1; full C11 builds 0.
- Private spool 7,464,000 bytes, 3 files, cleaned; certificate 19,345,408 bytes.
- Process baseline RSS 117,047,296; peak 128,376,832 bytes (single process, no children).
- Cold 5.419 s; repeat 5.394 s; retained certificate root remains; no second persistent corpus.
- 100k/6 GiB integrated gate NOT_RUN and not claimed. Old W03/W04 failed pilot remains explicit.

## 7. Holds and proof boundaries

- **G2 native direct consumer** HOLD_DEPENDENCY: Linux `/proc/self/fd` cold reader / actual native I03/Batch bridge not executable on this host.
- Upstream S1-C and S2-B independent G5 are still pending; Q2 does not self-accept them.
- Original35 source/science/respondent/source-read entitlement HOLD.
- S1-D production CURRENT issuer HOLD; Q2 uses only test-only sourcefree permission.
- Protected facade/#922, W03/W04, other worktrees and controller untouched.
- 100k/6 GiB integrated resource gate NOT_RUN; original35 QSM/source ownership HOLD.
- Legacy full-C11 identity parity is a test comparator, not Q2 production order.
- The original-source path retains the existing S1-B admission pre-hash plus snapshot acquisition. The measured one-open result is the sourcefree fixture path; no original-source positive was run.

## 8. Remaining attack surfaces

- On Linux, run `VerifiedExternalI02` cold reader and `install_direct_sourcefree_i02_i03` against an externally supplied sealed body release; verify native I03/Batch changed/restore.
- Attack the one-pass spool reconstruction for exotic canonical semantic fields, replay tuples, multiple universes, typed absences and wide/multiselect occurrences.
- Attack operation/fate census axes not exercised by the q101 fixture: unknown routing, nonadministered denominator, malformed current, missing receipt, duplicate/omitted operation.
- Verify the spool is actually deleted and no full candidate/C11 build occurs under failure paths.
- Confirm source-read denial, destination collision and spool cleanup under exceptions.

## 9. Disposition

`HOLD_EXTERNAL` for the native direct-I02→I03/Batch first-reader grade because the existing cold owner is host-blocked; the sourcefree direct I02 builder and operation/fate conservation are implemented and locally tested. This is not `ACCEPT_SCOPED`, not a G5 pass, and integration is `UNMERGED`.
