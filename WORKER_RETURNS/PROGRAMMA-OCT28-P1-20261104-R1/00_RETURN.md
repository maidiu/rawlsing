# OCT28-P1 compact C11 respondent-event execution view

**Sourcefree implementation candidate for independent review**

This cut implements the respondent-event lane of `ROADMAP:S03.2` / `S-C11` (`W03/P01`) and its cross-session Parquet/Zstd accelerator (`W04/P02`). I02 still validates the current source and projection before either the compact view or the cache participates. The original release, native exact object lookup, I03/I05 evaluation and downstream replay identities govern the result.

| Input | Pin |
| --- | --- |
| Protected starting cut | `f58c8400a024d108a8ab9fa814c87967d336ea47` |
| Protected E1+E3 receiving | `2dcef17355e5a3548452cd9bd9c6b9531cf77e03` |
| E3 repair | `43d2b70ebae4d183aadbd9694624575857fd100f` |
| E4 independent acceptance | `7fb9a576fc5bf4d15e6bb91e5640ae50336ddb0c` |
| P1 code and tests | `0a63e7c90cabcfd01dbb169d477f2d0ead5be22c` |
| P41 reader | `f27d1101048638bba395143a48efb7ef00bfcda4` |
| E1 synthetic SAV and timing harness | `cba713d229c2e8c1c3ae28f100ac8f995c6cd8c8` |
| SAV SHA-256 | `c5ec6abad7311118651e79986322d4300409f4303d92cb17ce9440d630a7d56b` |

The user released isolated P1 code writes on synthetic data. The implementation used GPT-6.1 Sol High on `mainMac.lan`, Python 3.11.3 and a separate Git repository with the canonical object store as a read-only alternate. The branch was absent on the private remote at launch. Existing E1–E4 worktrees and protected PRE-MAIN were read-only inputs. [Runner and worktree provenance](PROVENANCE.log)

## Current ownership and actual call path

1. `decode_sav` acquires and verifies the source snapshot. `materialize_native_preimages` carries the accepted decoder metadata digest into the exact physical stream. The current projection and I02 validation continue to supply the source, respondent, occurrence, release and replay determinants.
2. `execute_issued_workload` checks the current issuer before source acquisition. Route B and direct Batch both call `build_source_backed_c11_repository`. The facade calls the existing validator and derives the private event lane from the newly sealed release. The release is represented with the same exact public/internal content. Repository indexing uses exact event locators for the compact lane.
3. `CarrierNeutralResearchExecutor.execute_i03` calls the existing `execute_empirical_query`. Its E3 repository-scoped index still binds the exact release and universe. `_build_release_index` uses the source-derived respondent groups. `_select_respondent_events` passes immutable typed event rows to the same predicate, target, risk, weight and authority logic. The normal hot path does not construct a full native event. Native exact-object lookup or legacy public-object iteration reconstructs the requested native event through `materialize_public_object` and checks its exact content identity.
4. I05 continues through the current evaluator. Batch/R04 resumes native receipts and R05 uses the actual P41 reader. The view and cache contribute no receipt fields and carry no authorization.

The existing canonical Parquet carrier serializes full logical releases and reopens by eagerly reconstructing all objects. It retains its separate persistence role. R4 supplied the respondent/event separation and typed selector precedent. Its fixed-width ordinals, locator rules and sparse override vocabulary are scoped to that carrier and do not cover arbitrary current native event extensions. P1 reuses the current R5 physical value path, canonical semantic byte preimages, exact public object materializer and existing Arrow/Parquet Zstd dependency. The five-test disposition supports adapting current machinery for a true current gap. W03/W04 are selected requirements. E3 and canonical Parquet leave the typed hot lane and disposable accelerator uncovered. The actual receiving path is I03/I05 through R04 and P41. Current exact identities and sourcefree authority limits make the existing materializer and codecs suitable for reuse. An R4 port would introduce its narrower historical event ABI. A second canonical carrier would duplicate storage, and deferring both selected capabilities would leave the measured gap in place. The retained code adapts existing semantics and compares gain at the current consumer.

## Cache and recovery

With `RAWLSING_C11_ACCELERATOR_DIR` set to an absolute caller-authorized directory owned by the runner with mode `0700`, the facade automatically uses the compact Parquet/Zstd backend. The compact in-process view still works without a configured storage grant or a file-decoder receipt for legacy in-memory incidence. Runtimes without Arrow retain the eager compatibility path. The accelerator is a disposable cache for compact canonical event preimages.

The key includes the schema/code contract, source SHA, decoder metadata when present, exact transport binding, R5 value contract, projection binding, current runtime authority snapshots, freshly selected release and replay refs, and the ordered event inventory. Occurrence and respondent grouping come from the current I02 objects. The expected byte hash for each cached member comes from that event's exact content hash in the freshly sealed release. A cache writer cannot make altered bytes admissible by rewriting Parquet metadata. I02 and the current workload/query authority checks run before the cache can affect execution.

The cache uses 16 direct-mapped slots. Distinct keys can coexist and a slot collision is a miss. The writer stages a private file, flushes it and atomically replaces one slot. Stale, absent, malformed or changed bodies fall back to the sealed source-derived bytes. A failed publication leaves the prior committed slot intact. A process killed before rename can leave a private staging file, which the reader ignores. The first trial with one slot produced two avoidable misses on every fresh joined process. [Retention falsifier](retention-falsifier.log)

## Sourcefree proof

The pinned baseline and candidate produced identical 53,463,055-byte native captures covering C11 source and occurrence objects, I03/I05 queries, predicates, exact facts and refs, replay and selected P41 values. The capture SHA-256 is `8048dee503f5d42079bae0b4cd43e944b4de60114b3efdd19b7929e70077254b`. The 28,017-byte checkpoint SHA-256 is `bbc9a626f1045a22e3f4b0f95b44ef62bc434dd593c55cfd818986978d850f9c`, and the selected P41 view is `c6aaef3c9816cdd63601703f4de52adf58d86ef0382adccb7cb6764f53812cf5`. The changed source determinant with recomputed internal checkpoint hashes failed the external checkpoint pin. Restoration resumed to the same P41 view. [Byte comparison](native-court.log) · [Exact capture](native.json.gz) · [Checkpoint](checkpoint-0.json)

The E3-related suite passed 209 with one installed-library Stata extended-missing capability skip. The focused and adjacent Route B/facade suite passed 40, and the fresh-process P41 checkpoint/resume test passed. Six focused tests covered exact lookup with no hot native event reconstruction, same-key changed Parquet bodies, deletion, stale keys, interrupted publication, revocation before cache access, E3 index recovery, and the legacy in-memory decoder-metadata case. Disabling the expected event-body hash check made the cache-rebuild assertion fail, and restoring the code returned it to PASS. [Regression logs](regression.log) · [Mutation RED and restoration](cache-integrity-witness.log)

## Same-host resource observations

The timed court used fresh processes and the same 12-row, 911-byte SAV on the same host. Order was baseline, cold compact, warm compact, baseline, corrupt compact, deleted compact. Joined wall excludes P41 archive extraction. Peak RSS covers the full process.

| Process | Joined wall | Peak RSS | Cache hits / misses / publications |
| --- | ---: | ---: | ---: |
| Baseline A | 23.813 s | 248,754,176 B | — |
| Compact cold | 23.773 s | 252,362,752 B | 4 / 2 / 2 |
| Compact warm | 23.266 s | 255,594,496 B | 6 / 0 / 0 |
| Baseline B | 23.798 s | 247,377,920 B | — |
| Compact corrupt | 23.321 s | 257,798,144 B | 4 / 2 / 2 |
| Compact deleted | 22.940 s | 252,313,600 B | 4 / 2 / 2 |

The paired observations were 0.17% lower cold and 2.23% lower warm versus baseline. Warm view construction across six builds was 31.75 ms versus 43.20 ms cold. The court resolves the difference in cache use. Whole-process timing is based on two pairs on one small fixture. Peak RSS was 3.61 MB higher cold and 8.22 MB higher warm, so a whole-process memory reduction remains unproved.

Each process acquired one 911-byte source snapshot. The measured release had 92 public and 15 internal objects. The hot lane kept 36 compact events and zero full native event envelopes in its public repository representation, with zero native event reconstructions in the joined timing. The body array was 118,512 bytes. Two compressed members occupied 41,708 bytes total, the largest staged member was 20,854 bytes and maximum active-plus-staged cache bytes were 41,727. The existing P41 runtime scratch footprint was 651,993 bytes on every run. The timed result parity digest was `5dd623dbfd4eb6b837644f84ccf4a2579d7403462d0c08fe26c4aff3d98e5287`. [Measurements](MEASUREMENTS.json) · [Raw phase and output evidence](timing-raw.tar.gz)

## Scope and receiving

- `W03/P01` has a source-derived compact respondent-event hot lane with exact reconstruction. Cold projection and I02 still construct the canonical candidate and other record families remain eager. Streaming cold I02 candidate validation and broader compaction remain separate slices.
- `W04/P02` has exercised cross-session reuse of event preimages in an authorized private cache. It avoids repeated event-body serialization on a hit. Source snapshots and I02 are still required. A cache that skips source projection or I02 would require a separately accepted authenticated preimage and custody contract. Real large-source performance and storage placement remain unmeasured.
- The remaining ABI chain starts at `project_c11_candidate_from_physical_cells → validate_c11_source_release`. Qualify bounded cold projection and complete I02 validation while preserving the existing seal and manifest roots. Then extend the private view and exact locator APIs to other respondent-grain families where their measured materialization dominates. An authenticated warm projection bypass, if justified and authorized, follows the same issuer check and requires an independently pinned projection preimage before it can enter I02. Carry exact resolver and R04/P41 parity through each incision.
- A separate reviewer should confirm the actual facade, I03/I05 and replay wiring and repeat the compact warm-index, same-key rewritten Parquet, revocation and first-consumer courts. The qualified receiving owner should refresh PRE-MAIN, verify the exact code delta and current storage grant, run the same tests on the receiving cut, and make the separate protected CAS decision.
- Roll back by reverting the code commit. Disable persistence by unsetting `RAWLSING_C11_ACCELERATOR_DIR` and discard the private cache files. Source, logical release, replay and checkpoint records require no migration. Original35, native S3, scientific issuance, FF/N9/N11 and actor/Sorok holds remain in force.

## Reproduce

Use a detached `base` worktree at the protected starting pin and a separate `p1` worktree at the code pin under the same scratch root. Extract the pinned E1 `profile_oct28.py` and `same-source.sav` into the fixture directory. Extract `related-suite-command.sh` from the E3 terminal return `3de9db3f0632c23c3a5817d0526c2f42caf5ebd1` and `capture_native.py` from E4. Use the pinned P41 Git object. The historical runtime authority regression requires the tracked `HQ_HANDOFF/DECISION_LEDGER.jsonl` and `WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py` if using sparse checkouts.

```sh
export PYTHONPATH=. PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LC_ALL=C
bash "$packet/run_pairs.sh" "$root" "$fixture"
python3 "$packet/compare.py" "$root/evidence"
bash "$packet/run_native_court.sh" "$root" "$fixture" "$e3_suite" "$e4_capture"
(cd "$root/p1" && python3 "$packet/cache_integrity_witness.py")
```
