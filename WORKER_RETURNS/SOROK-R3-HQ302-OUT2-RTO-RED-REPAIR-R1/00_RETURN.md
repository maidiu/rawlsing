# SOROK HQ302 OUT2 — bounded sourcefree RTO repair return

**Disposition:** `SOURCEFREE_28_OF_29_RTO_REDS_REPAIRED__S27_ORACLE_CONFLICT_RED_RETAINED__MULTIWRITER_NON_GOAL_RED_RETAINED__INDEPENDENT_I2_REQUIRED__NO_ADOPTION`.

**Identity:** repo `maidiu/rawlsing` (private); assigned branch `agent/rabochii-sorok-r3-hq302-out2-rto-red-repair-r1`; exact direct sealed startup `3944ea001a9f946745c2142c223e4d5b856b40d4`. HQ302 parent `75341803ace63da30dfcd66273b6e3d75ad87132` does not replace worker seal. One Browser/GitHub GPT-6 medium bounded worker, isolated Browser Python and GitHub connector. Writes restricted to own `WORKER_RETURNS/SOROK-R3-HQ302-OUT2-RTO-RED-REPAIR-R1/`.

## Frozen inputs and execution

Candidate exact commit `e09d6497b7e0118b063b3620729f59b47f88a819`; RTO independent review `767618db9fa01b83a461869c2ae06541684d18bf`; original semantic S01–S28 specification Git blob `782ba75ee94f24908100b1f3464e7035497d546c`. All authored/RSR tests and RTO hostile tests are byte-identical to pinned blobs, enumerated with actual `blob <len>\0` SHA-1 in `01_EXECUTION_MATRIX.json`. Isolated workspace, observed Python 3.13.5 and pytest 9.0.2; actual OS process termination 79 and cold replay run. No source/respondent material, actual model/actor/client, production code or accepting issuer imported.

**True baseline prepatch:** 83 PASS / 30 RED in 113 cases (27/28 original, 17/17 RSR independent, 2/2 RSR old cold, 9/9 HQ300 added tests, 28/57 independent RTO hostile).

**Final executed:** 135 PASS / 2 RED in 137 cases: original S01–S28 27 PASS / S27 RED; RSR 17/17 PASS; original RSR cold 2/2 PASS; HQ300 repair 9/9 PASS; RTO 56/57 PASS; 24/24 new OUT2 cross-combination PASS. Real `--junitxml` and full stdout within evidence tar. `pytest` exit 1, no xfail/skip/modified old assertions. RTO newly green 28 of prior 29. Exact remaining REDs below.

## Repairs materially demonstrated

1. **Fail-closed mode and candidate directives:** any explicit unrecognized/typo/null/legacy `envelope_mode` now refuses rather than downgrading to implicit legacy fixture; omission remains permitted *only* for old sourcefree authored fixture compatibility. Strict and legacy reject top-level or nested ownership/issue directions, event IDs, cursors, state/effect deltas, material/objective state and memory directives even when an injected synthetic decider returns True. No original S27 mug movement.
2. **Opaque metadata bound without owner issuance:** immutable hash uses *all* canonical present proposal fields, including ADP019-shaped opaque keys, not only former narrow digest keys; canonical preimage is stored and checked after cold restore. Replay of same candidate ID with changed producer/receipt/cursor/hash metadata rejects conflict. These opaque strings do NOT prove valid ADP019 identity, issuer signature, causal owner or JCS canonical compliance; strict synthetic callback remains nontransferable fixture authority.
3. **Viewer revocation and perception:** after revocation, pending send and ACK refuse, local projection opportunity is cleared, per-viewer cold recovery preserves receipt history without creating a live opportunity. Direct viewer-set removal also blocks delivery/ACK. `perceive` never asserts a real human perceived on this unowned source-free surface, even under caller-owned `True` callbacks. `emit_to` now ensures an admitted global outbox intent exists. These calls remain local simulations and do not witness actual renderer/user client delivery.
4. **Saved-state and failure atomicity:** validates event payload/preimage digests, unknown grades, delivery IDs/attempt IDs/counts, ghost perceived entries per user, strict opportunity linked to allowed delivered fixture, forbidden owner world state even if unkeyed JSON digest recomputed. Restore validates on a separate object before any live instance mutation. `OUTBOX_F2_JOURNAL_V2` schema intentionally rejects non-migrated V1 snapshots (no unilateral migration of previously persisted data).
5. **Real cold process:** `os._exit(79)` before atomic rename causes no durable event/outbox; after fsync and directory fsync, new process sees one event/intent. Separate new-process delivery, revocation, re-fsync and another fresh-process recovery preserves the revoked permission boundary and one event/one delivery identity. Still POSIX-like isolated single-writer snapshot experiment.

## Two openly retained REDs

- **Frozen S27 authored-test RED (test_s27_material_move_needs_world_owner):** old Python asserts payload `world_owner=NADIA` causes mug to move; frozen semantic oracle says `world_authority=MISSING` means `HOLD_MISSING_MATERIALIZATION_OWNER`, mug unchanged, no move. Fixing code to pass this old Python would violate source authority. Competent frozen-oracle custodian must resolve the authored test versus frozen spec; worker edits neither.
- **RTO stale-two-writer RED (test_replay_manual_two_writers_can_lose_first_committed_event):** two stale local snapshots each write same file; second can overwrite first. Explicit single-writer architecture lacks CAS/locking/linearizable transactions. No multiwriter guarantee claimed and no false green. Competent durable-store/ADP019 owner decides a future design if genuinely needed.

## Non-goals and owner conditions

No cryptographic authenticity against an attacker with filesystem write access; recomputed unkeyed digest over unauthorized world sidecar is now refused because world owner is missing, **not** proof against arbitrary hostile disk rewriting. Opaque full ADP019 keys are digest-bound, not validated issued envelopes. No ADP016/017 memory changes, actual material effect, human perception, real networking, cross-host exactly-once, multiwriter durability, surveyed sources, V3/N12 wake, canonical PRE-MAIN merge, or semantic adoption. Independent high-I2 acceptance commissioned by HQ after return.

## Custody

Source and tests, raw before/after JUnit and stdout, reproduction commands and hashes in `OUT2_EXECUTED_EVIDENCE.tar.xz` + `01_EXECUTION_MATRIX.json`. Changed repo paths confined to OUT2 own return directory. `environment_passport_delta.json` records tested local closure and UNKNOWN account monetary/quota metrics. Exact pushed commit SHA to be verified externally by direct remote HEAD readback; it cannot be embedded in its own commit.
