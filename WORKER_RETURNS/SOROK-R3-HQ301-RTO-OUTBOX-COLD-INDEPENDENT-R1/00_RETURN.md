# SOROK HQ301 RTO — independent I2 outbox / cold-crash sourcefree court

**Terminal scientific recommendation: `REVIEW_REVISE__56_BASELINE_REPRODUCED_55_PASS_S27_RED__12_PRIOR_INDEPENDENT_REDS_CLOSED_AT_FIXTURE_GRAIN__29_NEW_HOSTILE_REDS__NO_ADOPTION`**.

**Role:** independent I2 reviewer of the HQ300 implementation, not its author, Sorok HQ, ADP019/CAN issuer, world-state/actor owner or human-perception witness. Scope exclusively sourcefree synthetic events/outbox/journal. No production implementation, original WVS/respondents, paid model or live V3 action was invoked.

## 1. Pinned identity and environment

- Repository private `maidiu/rawlsing`; commissioned reviewer branch `agent/reviewer-sorok-r3-hq301-rto-outbox-cold-court-r1` directly verified BEFORE writes at **exact sealed startup** `9df61e0279b996a61ce13ac862c9e4614d2f98ea` (parent `896d8bcbfb9257c190fc9e4241b3a0176594d08e`).
- Candidate exact returned SHA `e09d6497b7e0118b063b3620729f59b47f88a819`; archived `CANDIDATE_EXECUTED_BUNDLE.tar.xz` exact native Git blob **`61f5b960ef05a74d10db11b0fae2bca703ae0ae4`**, 20,028 bytes, independently decoded into an isolated reviewer staging tree. The archive had 23 file members, all inspected for safe relative paths before extraction.
- Candidate imported `outbox_prototype.py` native Git blob **`76a0b2bb8f6161e6807789f88a1a35cc9e93e968`**. Source/test/log hashes were reverified against committed `01_EVIDENCE_MATRIX.json`. All bundled expected files matched EXCEPT that `regression_47_junit.xml` and `regression_47_stdout.txt`, named in evidence metadata, were absent from the archive; this is a provenance completeness exception, not an excuse to relabel new execution.
- Frozen original S01–S28 semantic specification, exact Git blob `782ba75ee94f24908100b1f3464e7035497d546c`; original authored Python tests `a6263f8903f22da2b1cde3999d950328d19c9e21`; unchanged RSR strict 17 `044b9cb48c2e4e3d825e7a2cbb52bb412d1366d7`; original cold driver/test `0c8676aaa3ff6605f3fb7a987e29f88d26fafb03` / `ad132e7e852d3873597276b51afda86b8296f891`.
- Read exact HQ301 commission and Sorok HQ301 parent intake, `00_READ_ME_FIRST`, `00B`, `00C`, `00D`; compared accepted ADP019/CAN022/CAN025/CAN015 with RSR's pinned original authority identities. No accepted modules were imported or exercised.
- Independently isolated sourcefree Browser container: observed Python **3.13.5**, pytest **9.0.2**, git **2.47.3**, shell/subprocess/forced `os._exit(79)` and writable files; no full private Git checkout, no continuity assumption from author runtime. See `environment_passport_delta.json` and hash ledger.

## 2. Authentic executed suites (no rewritten oracles, skip, xfail or greenwashing)

| Execution | Actual result | Evidence |
|---|---|---|
| Exact unchanged HQ300 56-case suite | **55 PASS, 1 RED**, exit 1 | `baseline56.xml`, `baseline56.stdout` |
| Unchanged RSR independent 17 | **17/17 PASS**, twelve previously RED all physically repaired at isolated fixture grain | Included as subset of baseline |
| Original S01–S28 authored Python | **27/28 PASS; S27 RED**, exact original bytes | Included as subset of baseline |
| Prior RSR two subprocess cases | **2/2 PASS** | Included as subset of baseline |
| HQ300 nine new repair/cold | **9/9 PASS** | Included as subset of baseline |
| Independently authored HQ301 hostile | **28 PASS, 29 RED** (57 cases), exit 1 | `hostile_full.xml`, `hostile_full.stdout`; source in `test_rto_hostile.py` |
| Combined unchanged 56 + new 57 | **83 PASS, 30 RED** (113 cases), exit 1 | `combined_113.xml`, `combined_113.stdout` |

Original S27's authored test treats `payload.world_owner='NADIA'` as permission to mutate a mug; it then *requires* the mug to move. Frozen S27 explicitly specifies `world_authority=MISSING`, `HOLD_MISSING_MATERIALIZATION_OWNER`, unchanged mug and no emitted move. The repaired candidate refuses the sidecar and the original Python test correctly remains **RED**. Do not modify either frozen oracle or original Python test to get 56/56. S28's original test rollbacks a snapshot rather than testing an unresolved causal window; stricter causal_time=None refusal passes separately. S19's authored memory append is fixture mutation without ADP016 / ADP017 effect/perception/encoding. S23's authored empty payload alone does not establish VALID_EMPTY vs UNAUTHORIZED; explicit missing `source_refs=[]` refusal is a distinct positive.

## 3. New hostile findings: 29 true executed REDs (not 29 accepted production defects)

**At sourcefree candidate-interface grain:**
1. **Five envelope downgrade variants**: any explicit unrecognized `envelope_mode` (`STRICT_TYPO`, capitalization variant, `''`, null, fixture-looking string) is treated as legacy, admitted without a competent witness. The legacy compatibility lane has no authenticated fixture-only caller boundary, so this is a promotion risk.
2. **Six forbidden high-authority directives**: even when `STRICT` and a sourcefree boolean decider says true, fields `admit`, proposer-assigned event ID, state delta, `cursor_after`, effect result and memory delta are admitted as if inert unknown metadata; the ADP019 prohibition is not enforced at the candidate ingress.
3. **One top-level material assertion**: `objective_employment_transition` outside `payload` bypasses the candidate's sidecar filter. It does not mutate the fixture's actual world state, but is silently accepted as proposal metadata; this is not a competent event-effect receipt.
4. **Two stale viewer permissions**: after an explicit simulated revocation of the `viewers` set, `deliver_to` and `ack_to` still advance the former viewer's delivery. The candidate has no issued revocation protocol; both REDs mean it cannot claim that stronger authorization behavior.
5. **Two actor/user perception boundary REDs**: a caller-supplied `perception_decider=lambda *_: True` and forged witness can mark `perceived` in sourcefree state; a stale/failed viewer-specific delivery is ignored by `perceive` when a global outbox delivery exists. This does not demonstrate anyone in the real world perceived anything; nevertheless the field name and code path are too permissive for any actual-client claim.
6. **Two persisted-state validation bugs**: `validate_state` uses merged projection dictionaries `{**perceived, **opportunity}`, so a valid opportunity masks an invalid perceived ghost under the same user ID; forged `last_attempt_id='ATT-FORGED'` is persisted without recomputing deterministic attempt identity.
7. **Eight full-envelope identity omissions**: changing only ADP019-relevant producer instance/version, expected event cursor/history hash, render receipt/context, causal session cursor or payload hash under the same candidate ID produces an idempotent replay instead of collision. These are **sourcefree scope/accepted-contract gaps**, because the candidate had expressly excluded exact ADP019 envelope/JCS—not eight validated production vulnerabilities.
8. **One failed restore not failure-atomic**: a rejected corrupted snapshot leaves the original in-use ledger overwritten with corrupted bytes after raising. Cold `Journal.recover()` normally constructs a new instance and raises; this failed-restore defect is observable on the mutable `OutboxPrototype` interface.

**Explicitly unsupported threat model / non-goal controls:**
9. **One attacker-controlled disk rewrite**: a forged `world` state plus recomputed ordinary unkeyed `state_digest` rehydrates; SHA256 checks accidental or unsophisticated corruption, not authenticated origin. The journal never claimed MAC/signature or adversarial disk-writer security, but cannot be promoted as an authority grant.
10. **One deterministic stale two-writer overwrite**: two independent recovered instances, committed sequentially from an old snapshot, overwrite the first durable event with the second. This is an **actual executable loss at concurrent-stale-writer scenario**, explicitly outside the candidate's single-writer contract and decisive against cross-worker atomicity claims.

The exact per-case PASS/RED source, traceback, runtime and grade are contained in `01_EXECUTION_MATRIX.json`, `test_rto_hostile.py` and the raw JUnit/stdout archive.

## 4. Positive sourcefree cold-process and regression results

- Two reviewer-owned fresh-process tests kill the candidate's *own* `Journal.admit_and_queue` using genuine `os._exit(79)` before rename, and after file+directory fsync. New process checks: before → zero events and intents; after → one event and one outbox/client intent with stable delivery ID.
- A third independently kills a second admission **before rename** against a preexisting committed journal: the first durable event survives and the second does not. A fourth corrupts the on-disk snapshot and confirms a new process refuses (raises/nonzero), rather than reconstructing a valid event.
- Separate controls reconfirm lost ACK: same event ID and per-client delivery ID, changed retry attempt ID, no extra event, no implied perception. Existing original RSR two harness saves remain only harness persistence evidence; they do not replace the new Journal's own fsync tests.
- Narrow (candidate-recognized) source/issuer/release/artifact/participant/time substitutions correctly conflict; seeded 160 deterministic mutations pass, preserving the originally admitted event. Forged unknown event ID, explicit missing source/time, stale decider, denied viewer opportunity and false perception callback have bounded positive refusal tests.

## 5. Owner action, boundaries and terminal disposition

`REVIEW_REVISE` at advertised enhanced sourcefree occurrence/membrane grade: the repaired 12 RSR cases and single-writer crash durability are independently real, but new ingress, identity, viewer and restored-state REDs prevent stronger acceptance. The 29 new REDs must not be converted to xfail/skip, and no production-grade claim may borrow the existing 55 positive cases. The original 56 baseline has 1 expected authored-test RED, independently retained.

Next competent owner requirements, **not grants**:
- Sourcefree author: unknown-mode default-deny, forbidden top-level authority schema, comprehensive proposal identity or explicit quarantine, state validation, strict viewer delivery/revocation and atomic restore; maintain all prior frozen 12 and S27 RED.
- Independently competent oracle custodian/material-world owner: resolve contradiction of original S27 Python test vs specification without changing spec, establish actual world object transition rights. ADP019 owner must separately authorize real full-envelope canonical event admission/causal cursor and multiwriter concurrency if ever needed.
- Outbox/application permission owner and ADP016/017/CAN015 owners: per-viewer provenance, separately witnessed user opportunity/actual perception (never ACK equality), and memory/knowledge encoding. A sourcefree boolean callback or string authority ref cannot substitute.
- Transport durability owner: choose and prove actual deployment filesystem/power-loss, locking or compare-and-swap, failure recovery and authorization freshness. No exactly-once network transport claim.

**No accepted-law contradiction requiring I3 was established**: this is a bounded candidate and unimplemented owner interface, not conflicting accepted law. No new model/actor calls, no original survey, no V3/N12 wake or production/CURRENT mutation. Do not self-adopt.

Final remote SHA must be reported only after direct post-push readback; do not self-reference a future commit hash in this immutable file.
