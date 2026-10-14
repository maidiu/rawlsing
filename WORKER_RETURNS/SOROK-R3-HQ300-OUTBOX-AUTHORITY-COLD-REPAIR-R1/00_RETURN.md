# SOROK HQ300 OUT — source-free occurrence/outbox authority and cold-crash repair

**Terminal disposition:** `SOURCEFREE_CANDIDATE_RETURN__12_RSR_REDS_NOW_GREEN__ACTUAL_COLD_JOURNAL_EXECUTED__FROZEN_S27_AUTHORED_TEST_RED__I2_REVIEW_REQUIRED__NO_OWNER_ADOPTION`.

**Role:** independent bounded implementer (not Sorok HQ, ADP-019 issuer, world/effect owner, V3 executor, renderer, actual-client/perception witness or independent accepting reviewer). Repository `maidiu/rawlsing` private. Allowed writes only `WORKER_RETURNS/SOROK-R3-HQ300-OUTBOX-AUTHORITY-COLD-REPAIR-R1/`.

## 1. Exact start and independent evidence

Owner-dispatched original startup: `0dc74e65057df6edfc69893abfae0fd25187ec71`. The directly observed remote branch tip before writer action was `3f8759107f96cffc4503a2e92328f5267753ddf6` (parent = exact original startup): an HQ-posted routing erratum explicitly permits an agent previously launched from the original seal to finish without reset, rebase or relaunch. This candidate preserves that tip as its direct commit parent. HQ300 parent `28d791df05b4d24ebe48b4298101af6951035a36` is not substituted for either. New I2 independent review comes later, not a same-worker self-adoption.

Frozen source inputs:
- Original S01–S28 *specification* at `99f2e7128a8417dfeaa39468c45ba65f6958c061`, Git blob `782ba75ee94f24908100b1f3464e7035497d546c` (unchanged, not re-authored).
- The exact authored S01–S28 Python test blob `a6263f8903f22da2b1cde3999d950328d19c9e21` (verified native Git blob SHA-1).
- Independent RSR 17 Python test blob `044b9cb48c2e4e3d825e7a2cbb52bb412d1366d7` (verified unchanged).
- Independent RSR old cold-harness source/test blobs `0c8676aaa3ff6605f3fb7a987e29f88d26fafb03` and `ad132e7e852d3873597276b51afda86b8296f891` (verified unchanged).
- RSR original return `5ac66779ab76575d0d145829073371d35197a457` with twelve actual REDs; SR source author return `8da45605c267ea60b664d00fc8444d8c9b007628`.

Exact original files staged byte-for-byte and their Git `SHA1(b"blob "+str(length)+b"\\0"+bytes)` recomputed. New `outbox_prototype.py` is a candidate replacement only. The governing ADP019/CAN022/CAN025/CAN015 **document** blobs were fetched; no accepted owner code imported. No original respondent/survey material, paid models, physical actors, production service, V3 event ledger, or source-authority use.

## 2. Actual executed pytest matrix

| Executed suite | PASSED | FAILED | Status |
|---|---:|---:|---|
| Frozen original authored S01–S28 | **27** | **1** | `S27 RED; authored test contradicts frozen oracle` |
| Unchanged RSR independent 17, including all twelve previously RED | **17** | **0** | `ALL_12_RSR_REDS_ADDRESSED_AT_SOURCEFREE_GRAIN` |
| Unchanged original RSR harness cold subprocess two | **2** | **0** | `OLD_HARNESS_REPRODUCED_ONLY` |
| New HQ300 nine hostile tests incl. two new cold-process crash boundaries | **9** | **0** | `SOURCEFREE_JOURNAL_COLD_CRASH_PASS` |
| **Total** | **55** | **1** | `BOUNDED; NOT ACCEPTED V3` |

Actual command: `python -m pytest -q test_sr_28_falsifier_court.py test_rsr_independent.py test_rsr_cold_replay.py test_cold_repair.py --junitxml=all_56_junit.xml` (exit **1**, 55 PASSED, 1 FAILED); separate per-suite XML/stdout and corresponding entrypoint/test source in bundled archive. No `xfail`, `skip`, changed frozen assertion or self-granted adoption.

The original Python S27 specifically asserts a mug *must move to hand* if the payload contains `world_owner="NADIA"`; the frozen S27 actually specifies MISSING materialization owner, unchanged mug and no emitted move. The candidate rejects the payload `world_owner` sidecar; the old S27 therefore fails. That is a warranted **RED test**, not a reason to change the frozen specification. Original S28's rollback-in-same-process test continues to pass but still does not test the missing causal time that S28 specifies. New strict-time test does. S19's old Python test directly mutates a mutable fixture `world_state["actor_memory"]` without ADP016, so its Python PASS remains a coverage hole. S23's valid empty fixture is green but only the new hostile contrast distinguishes explicit missing source authority from synthetic `VALID_EMPTY`.

## 3. Repairs established by live tests

1. **Immutable deep copy and identity binding.** All admission input is canonicalized into fresh JSON bytes; returned event and ledger reads are deep copies; snapshot/restore is deep; content digest binds payload and separate identity digest binds candidate, source, issuer, release, artifact ID/hash, causal time, participant/parent references and named fixture grade. Changed source refs or artifact/time/parent with same candidate ID cannot replay as the same admission. Corrupt restored payload/identity/delivery identities reject.
2. **Admission/refusal.** Explicit empty authority refs reject `MISSING_SOURCE_AUTHORITY`; explicit absent time rejects `DEFER_MISSING_CAUSAL_TIME`; invalid strict temporal syntax/causal parent and forged material/actor-effect sidecars fail closed. Typed `STRICT` envelope requires an injected positive adjudicator; token-like strings alone do not grant it. The exact published ADP019 envelope, RFC8785 JCS and real V3 receipt/cursors are **not** implemented. Omission of both authority and time is allowed **only** in marked original legacy sourcefree fixture mode to reproduce authored tests; this is a synthetic, nontransferable scaffolding shortcut and would be unlawful as actual V3 admission.
3. **Unknown event and viewer refusal.** `Outbox.emit`, `UserProjection.offer` and source-free delivered/ACK transitions refuse unadmitted event IDs. Strict-mode offer additionally requires viewer authorization and actual per-client delivered receipt. Legacy fixture `offer` remains prospectively permissive for frozen authored tests and is not a proof of real user opportunity. ACK without a separately validated perception witness never marks user perception. A caller-created fake witness cannot pass without an injected external `perception_decider`.
4. **Per-client identity and retry.** Event ID remains singular. Every `(event,viewer)` has a deterministic distinct `DEL-...` identity. Every lost-ACK retry gets a new deterministic `ATT-...` attempt ID, while event and delivery IDs remain stable. ACK is idempotent, is not an ADP016 memory update, and cannot prove a human perceived an emitted artifact.
5. **Atomic source-free journal test.** `Journal.admit_and_queue` stores event + outbox intent + per-viewer delivery intent in one hashed snapshot, writes a same-directory temporary file, flushes and fsyncs the file, atomically renames it, then fsyncs the directory. `os._exit(79)` **before rename** recovers no event and no outbox; **after rename+fsync** recovers exactly one event and one intent in a different Python process. Replay does not duplicate event/history/attempt, and subsequent lost-ACK resend produces a second attempt, not a second event. The old RSR harness's manual-save cold tests separately continue to pass. The journal refuses to persist nonempty hand-mutated fixture `world_state` as owner truth.

## 4. Scientific HOLD ceilings and required independent I2 review

`SOURCEFREE_F2_EXECUTION` does NOT establish production ADP019 atomic admission: this is an isolated, single-writer local-filesystem journal. No cross-worker locking/linearizability, real network send acknowledgment, power-loss/uncertain filesystem fsync guarantees, exact ADP019 JCS/cursors/schema, governed event/actor/effect producer, ADP016/017 knowledge and memory, CAN025 package, CAN022 renderer or CAN015 actor-safe projection was executed. No human has been shown an artifact. In-memory `world_state` remains a deliberately mutable scaffold for untouched legacy Python tests, not a material-world owner. No event-driven world or actor memory transition is implemented.

**I2 separate hostile acceptance request:** a distinct GPT-6 High reviewer should stage this exact bundle and the frozen original oracle, rerun the exact 56 tests, independently inspect S27 (why original test must stay red), S28 temporal coverage, S19 ADP016/017, S23 VALID_EMPTY/UNAUTHORIZED; attack stale/revoked authorization after crash, negative/per-client delivery permissions, crafted source/issuer/parent identity collisions, malformed canonical hashes, forged material events/utterances, journal crash windows/replay, external display ACK versus human perception. Reject if the purportedly strict interface can be upgraded to V3 ADMIT with string refs, self-issued callbacks or a hypothetical filesystem durability assumption. Have the competent ADP019, material/world, scheduler, projection/ADP016/017, and independent frozen-oracle owners adjudicate only their own authority fronts. No I3 escalation currently established; no adoption or wake.

## 5. Return ledger and remote rule

Changed repo terrain: only `WORKER_RETURNS/SOROK-R3-HQ300-OUTBOX-AUTHORITY-COLD-REPAIR-R1/`. The reproducible source/test/JUnit/stdout files are packed in `CANDIDATE_EXECUTED_BUNDLE.tar.xz`; the manifest includes SHA-1 Git blob and SHA-256 per source/test/log. Additional top-level files: this report, `01_EVIDENCE_MATRIX.json`, `02_REVIEW_REQUEST.md`, `environment_passport_delta.json`, `03_CHANGE_MANIFEST.json` and the bundle. No secret, personal absolute path, raw respondent, locally configured credential or external model response in returned artifacts. Sourcefree result is a **candidate for review**, not a semantic law or production change.

**Final remote branch SHA:** verify *after* committing, in the worker chat return. A commit cannot truthfully predict or embed its own SHA.
