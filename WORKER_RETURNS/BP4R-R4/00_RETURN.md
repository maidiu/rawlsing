# SOROK R4 BP4R — episode-bearing fork and C9 writer-version repair

## Identity, custody and verdict

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `agent/sorok-r4-bp4-c12-episode-fork-writer-version-repair-20261030` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-r4-bp4-c12-episode-fork-writer-version-repair-20261030` |
| Commission head | `5677120c0048d168ce5fd98eed6663cc9531e8de` |
| Sealed startup ancestor | `299f41e97a43c67be9cc76a79fa49b48f4e12e54` |
| Device | `mainMac` (verified by `scutil --get ComputerName`) |
| Harness | OpenCode CLI `1.18.34` |
| Agent | `build` |
| Model | `opencode-go/deepseek-v4.1-flash` |
| Effort | `MAX` (`variant=max` read from the session record; no switch) |
| App session | title `Retained GT2 → N10E analytical consumer (H03)`; ID `ses_e7285576bffeqo0lE8N0HYK6gc` |
| Prior author locator | branch `agent/sorok-bp4-c12-chain-authenticity-writer-compatibility-r1`, return `790f793ea85c8aba914970b7d9c3c25f81bf8a01`; original app session ID UNKNOWN |
| Independent reviewer needed | separate I3 C9/C12 security reviewer, not this worker, not the BP4I3 reviewer |

**ENGINEERING:** `PASS_SCOPED_EPISODE_ORIGIN_AND_C9_WRITER_VERSION_REPAIR__REAL_CONSUMER_FORK_GREEN`

**SCIENTIFIC:** `HOLD__SOURCEFREE_TEST_ONLY__NO_NATIVE_WORLD_PERSON_OR_SOURCE`

**AUTHORITY:** `HOLD__NO_ADOPTION__ORIGINAL_OWNERS_AND_INDEPENDENT_REVIEW_REQUIRED`

## FINDING

The independent BP4I3 defects are real and were reproduced before repair:

1. **BP4I3-01:** a legitimate `JoinedProduct.say` followed by a guarded fork returned `fork_ok=true`, `content_ok=false`, `episode:0:branch_id_column_body_mismatch`. The child SQL location was `alt`; the sealed body origin remained `root`; the guard compared those two different concepts.
2. **BP4I3-02:** the actual C9 `c12_fork_guard` returned `FORK_READY` for a C12 database declaring `BP4_C12_STORE@2`, once supplied its perception digest. `two_store_readiness` also returned `READY` for two matching `@2` strings. The consumer never read `meta.schema`.

After repair:

- The same legitimate episode-bearing fork passes at `content_ok=true`, `fork_ok=true`, `schema_ok=true`, and survives cold reopen.
- A forged child-local episode transplanted to a foreign branch is refused at the same read with `branch_id_origin_mismatch`.
- The actual C9 consumer returns `FORK_HELD / C12_WRITER_SCHEMA_UNSUPPORTED` for `@2`; `@1` still returns `FORK_READY`/`READY`.
- Severing the C9 schema gate reproduces the old `@2 → FORK_READY` result; restoring it returns `FORK_HELD`.

## INTERPRETATION

Episode identity and branch location are distinct. The writer seals `branch_id` into the episode body and hash at authorship; a fork copies that body unchanged to a new SQL location. The reader must therefore resolve the **immutable origin** from the sealed body and the **current location** from the SQL column, using fork prefix counts to distinguish copied rows from child-local rows. The repair does not rewrite any hashed parent body and does not invent a new episode.

The C9 version defect is a consumer-boundary defect, not a missing helper: the actual reader must reject an unsupported writer schema before it treats C12 state as fork-ready. A standalone guard or two matching caller strings are insufficient.

## ACTION / OWNER

The candidate is routed to the original BP4/C12 writer/schema owner, C9-R3 actor/mirror owner, BP2P4J verifier owner, and a separate I3 security reviewer. The original owners must ratify or replace:

- the immutable-origin/location projection (or issue a versioned child-reissuance/migration contract);
- the supported C12 writer-schema set and SQLite version policy at the C9 consumer;
- the C12 external anchor issuer/custodian and finite coverage;
- the old-writer/new-writer test split for the C9/C12 suffix conflict.

No key, signer, trust root, native C12 receiver, source grant or adoption is invented.

## Actual test counts

| Court | Actual result |
|---|---|
| Original BP2P4J suite at `5b3e657` | **33 passed, 1 skipped**, exit 0 |
| Focused valid-SAY on original verifier | **1 failed** `episode:0:body_hash_mismatch`, exit 1 |
| Exact F2 overlay, full suite | **37 passed, 1 skipped**, exit 0 |
| Original BP4 guard court | **11 passed, 0 skipped**, exit 0 (exact C9 mirror schema path present and hash-matched; if absent the test is a typed skip, matching the reviewer's 10/1) |
| Original F2 + guard combined | **48 passed, 1 skipped**, exit 0 |
| Repaired candidate combined (F2 + guard + BP4R tests) | **57 passed, 1 skipped**, exit 0 |
| New BP4R fork/version court | **9 passed**, exit 0 |
| C9-R3 actual suite with staged exact C12/S36 sources | **14 passed, 1 failed**, exit 1 |
| C9 old-count conflict | preserved RED at `tests/test_c9_r3.py:476` (`parent perceptions=2, child=3`) |

The C9 failure is the known repaired-writer/suffix conflict. It was not weakened, deleted or renamed green. The old-writer fixture and the repaired-writer consumer need separate owner-issued versions.

## Exact evidence

- `evidence/01_ORIGINAL_BP2_33_1.xml`
- `evidence/02_F2_OVERLAY_37_1.xml`
- `evidence/03_GUARD_ORIGINAL_11_0.xml`
- `evidence/04_COMBINED_ORIGINAL_48_1.xml`
- `evidence/05_CANDIDATE_COMBINED.xml`
- `evidence/06_C9_PATCHED_14_1.xml`
- `evidence/07_C9_GATE_AND_FORK_COURT.xml`
- `evidence/08_PROBE_ORIGINAL_EPISODE_FORK.json`
- `evidence/09_PROBE_REPAIRED_EPISODE_FORK.json`
- `evidence/10_PROBE_ORIGINAL_C9_WRITER_VERSION.json`
- `evidence/11_PROBE_REPAIRED_C9_WRITER_VERSION.json`
- `evidence/12_RESIDUAL_HOLDS.json`

## Preserved RED/HOLDs

- C9 old-count/C12 suffix conflict: **RED**; exact old-writer fixture and separately versioned repaired-writer consumer are still required.
- Global writer chronology: perception clock 11 followed by episode clock 10 remains accepted by the writer; not repaired here.
- Anchor actor/created_clock coverage: changing root actors and `created_clock` to 999 leaves `anchor_payload` unchanged; external anchor contract still needed.
- Raw SQLite deletion, self-consistent injection, fully rehashed substitution and perception-channel substitution remain content-green in the existing guard court; only an owner-issued external anchor can address them.
- No external anchor/issuer/key exists. Authenticity/completeness remain UNVERIFIED.

## NOT RUN / limits

- No real signing key, trust root, anchor custodian, monotonic ledger or production receiver.
- No original survey/source/native C12/C11/CAN/ADP/Pyat data.
- No C9/C12 cross-database ACID claim.
- No protected PRE-MAIN CAS, merge or canonical registry update.
- No standalone original BP2/BP4 historical suites beyond the exact sourcefree cuts above.
- No QF2 work, no autonomous successor worker.

## DONE / REMAINING / BLOCKERS / LARGEST MOVE / FLIGHT / DELTA

**DONE:** reproduced BP4I3-01/02; implemented immutable-origin/location projection; enforced writer-schema checks in the actual C9 consumer; passed legitimate episode fork, cold reopen, foreign-transplant negative, version substitution and source severance; preserved C9 14/1 RED and external anchor HOLD; exact candidate files and replay evidence committed.

**REMAINING:** original owner ratification, independent I3 review, C9/C12 versioned test split, external anchor issuance and protected PRE-MAIN intake.

**CRITICAL BLOCKERS:** no owner-issued anchor/trust root; C9 old-count conflict unresolved; global writer chronology and anchor metadata coverage remain HOLDs.

**LARGEST PRODUCTIVE MOVE:** owner ratification of the origin/location and C9 writer-schema contracts, followed by a separately versioned C9/C12 suffix test and anchor custodian decision.

**FLIGHT:** sourcefree local Git/Python/SQLite; no native source, no model/harness switch, no other worker worktree changed.

**DELTA:** the episode-bearing fork now passes at the same reader that previously rejected it, and the actual C9 consumer now rejects `@2`; the old-count conflict and authenticity/anchor HOLD are explicit rather than hidden.

The exact pushed branch SHA is reported externally after push; a commit cannot contain its own final hash. No self-adoption.
