# SOROK C9C12-R2 — durable clock, actor readset and C12 fork integrity

## Identity and terminal

| Binding | Value |
|---|---|
| Repository | `maidiu/rawlsing` (private) |
| Branch | `agent/sorok-c9c12-r2-durable-clock-actor-integrity-20261030` |
| Worktree | `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/sorok-c9c12-r2-durable-clock-actor-integrity-20261030` |
| PRE-MAIN | `750548ddbb9b4392a16ce93097b856f349e16182` |
| Inputs | I1 `7d44e300…`; O1 `501ea1f5…`; RCF-B `397c6d61…`; BP2P4J `5b3e657…`; BP4R `693d25bf…`; C9 R3B `fac064c9…` |
| Host / model | `oldMac`; OpenCode `1.18.34`; `opencode-go/deepseek-v4.1-flash`, local variant `max`; provider-side effort unverified |
| Session | `ses_e77c423e1ffealQLzYonSQTRRf`; actual title `INDEX_B 282-branch indexing commission`; R2 suggested title not applied |

**Terminal:** `C9C12_R2_SOURCEFREE_CANDIDATE__CLOCK_ANCHOR_FIXED__C9_SNAPSHOT_READER__OWNER_ANCHOR_AND_MIGRATION_HOLD`

Observed FINDING: the sourcefree C12 edge can preserve immutable episode origin separately from SQL location, reject `@2`, reject perception clock 11 followed by episode 10, and bind actor IDs/created clock into the anchor payload. A C9 R3B actor-snapshot/outbox reader can read genesis and held state without writes. Causal INTERPRETATION: the remaining incompatibilities are owner contracts—external anchor custody, C9R durable writer/mirror ACK, and the old-count version split—not missing local checks. Proposed HQ ACTION: owner-review the candidate edge and keep canonical adoption HOLD. Accountable OWNER: original C9R/BP4/C12 owners and separate reviewer.

## Implemented candidate

- `candidate/c12_guard.py` blob `8f629c29…`, SHA-256 `104dc91c…`: BP4R immutable-origin guard plus `GuardedC12Store.append_episode` enforcing `NON_MONOTONIC_GLOBAL_CLOCK` against perception and all append-only rows; `anchor_payload` now includes `branch_identity.actor_ids`, `created_clock`, `fork_clock`, `root_hash`.
- `candidate/c9_actor_r3.py` blob `b9000cdb…`, SHA-256 `65da5b08…`: BP4R-patched C9 writer/reader/mirror helper, supports `BP4_C12_STORE@1`, rejects `@2`; original C9 R3B source remains `67f34f69…`.
- `candidate/c9c12_reader.py` blob `db38d05d…`, SHA-256 `9621cae0…`: read-only `read_actor_snapshot`, `guarded_c12_cold_read`, and `read_composite` first consumer; external custody always `OWNER_ANCHOR_REQUIRED`.
- `candidate/schema_actor_r3.sql` `0ae69ef5…`, `candidate/schema_mirror_r3.sql` `5f3f2895…`; `candidate/tests/test_c9c12_r2.py` blob `4249cb86…`.

## Actual tests

| Court | Result |
|---|---|
| Candidate C9/C12 fault/restore suite | **6 passed**, 0 failed/errors/skipped, exit 0; JUnit `91e31487…` |
| Historical C9 R3B original-version court | **14 passed / 1 failed**, exit 1; unchanged `test_c6_same_count_perception_substitution_is_held`; JUnit `8bfa25e4…` |
| Historical BP4R diagnostics against repaired candidate | **7 passed / 2 failed**, exit 1; exactly the old writer-clock and anchor-coverage diagnostic tests, preserved as historical vulnerability witnesses, JUnit `8cf5bfb5…` |
| BP2P4J performed-E2 vs offered-only pair | **2 passed**, exit 0; JUnit `64b095b3…` |

Candidate coverage: intact append/fork/cold reopen; C9 genesis snapshot and composite; writer-clock inversion refused; forged actor/created clock changes anchor; writer `@2` and missing-parent refused; forged child transplant refused then restored green; missing C8 receipt refused; missing outbox typed; restored outbox remains typed PENDING/held. C9R mirror ACK cross-database identity, held Rule A/T finalization and native E2 semantics are NOT_RUN, not fabricated.

## Three courts

- ENGINEERING: **SOURCEFREE CANDIDATE PASS SCOPED** — 6/6 candidate tests, 14/1 historical C9 preserved, 7/2 BP4R historical diagnostics intentionally retained, 2/2 E2 pair.
- SCIENTIFIC: **HOLD** — no native C8/C9/C12/Rule A/T/E2/person; C9 R3B has no native E2 field.
- AUTHORITY: **HOLD** — external anchor custodian absent, C9R writer/mirror version and old-count split are owner decisions, no merge/adoption.

## First consumer and owner handoff

`c9c12_reader.read_composite(c9_path, c12_path, actor_id=..., c12_branch_id=...)` returns actor head/version/outbox/mirror state plus C12 cold read and `OWNER_ANCHOR_REQUIRED`. It is a sourcefree I1/CP-A5-compatible reader, not an owner-frozen or native consumer.

Required owner decisions: external C12 anchor issuer/key/sequence/rollback window; anchor preimage including actor/created-clock binding; `@2` migration vs refusal; C9 old-count version split; C9R durable store vs separate actor store; mirror/outbox ACK contract; performed vs offered E2 at the C9 boundary.

## Artifacts

- `00_RETURN.md`
- `01_VERSIONED_WRITER_READER_AND_CLOCK_CONTRACT.json`
- `02_POSITIVE_FAULT_RESTORE_TESTS.md`
- `03_OWNER_ANCHOR_MIRROR_AND_MIGRATION_DECISIONS.md`
- `04_ROLLBACK_AND_PROVENANCE.json`
- `candidate/` source, schemas and tests

DONE: exact clock/anchor fixes, C9 snapshot/outbox reader, first-consumer composite, fault/restore tests, historical REDs preserved. REMAINING: owner anchor/mirror/version decisions; C9R durable adapter; native A0–A5. CRITICAL BLOCKERS: external custodian absent; C9R mirror ACK unproven; C9 old-count split. LARGEST MOVE: owner issues anchor and C9 writer-version decision, then review the exact candidate. FLIGHT: sourcefree local Python/SQLite only; no PRE-MAIN/PR/original branch/live DB mutation. DELTA: the sourcefree C12 edge is green under corrected clock/anchor tests while all historical failures and owner holds remain explicit.

The exact pushed return SHA is the HEAD of this branch and is reported with the final return message. No self-adoption.
