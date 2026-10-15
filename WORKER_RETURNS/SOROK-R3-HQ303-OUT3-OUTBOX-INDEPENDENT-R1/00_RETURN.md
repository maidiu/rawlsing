# SOROK HQ303 OUT3 — Independent I2 sourcefree court

**Disposition: REVIEW_REVISE. NO semantic adoption, owner issuance, V3 operation, or production claim.**

## Verified custody and execution

Reviewer branch sealed at `65125e8c64aba28b79e49e64b24b2350f77a2f10`, confirmed identical to the direct remote ref before work. OUT2 author commit `b1004a43eb0309af99e1b7ce9d5290df3c07f3cd`. Its archive `OUT2_EXECUTED_EVIDENCE.tar.xz` independently fetched via authenticated GitHub, verified SHA-256 `812070f33567fbac5ebada32cfa18fdc190e855230f87cc6108bfc4941b5a2f5`, and safely extracted with all 16 original members and Git blob identity receipts. Imported candidate `outbox_prototype.py` Git blob `d40f532a2f9c4ee12a7f99f0ef37164fe997518b`. Frozen S01–S28 semantic specification independently read at exact Git blob `782ba75ee94f24908100b1f3464e7035497d546c`.

Observed Python 3.13.5, pytest 9.0.2, filesystem and true subprocess/os._exit (79) operation. **Original 137-case court independently rerun, not inferred from author logs: 135 PASS, 2 FAIL, 0 SKIP, exit 1.** Suite counts: frozen authored S01–S28 27/28, RSR 17/17, RSR cold 2/2, HQ300 cold 9/9, independent RTO 56/57, OUT2 combinations 24/24. The historic 83 PASS/30 RED baseline is author evidence only; the current 28 previously failed RTO cases run green now, while prior RED provenance was not independently re-executed.

Both original FAILs **intentionally retained**: `test_s27_material_move_needs_world_owner` is an authored assertion demanding a mug move contradictory to frozen S27 `world_authority=MISSING` requiring HOLD, no material transition. `test_replay_manual_two_writers_can_lose_first_committed_event` reproduces lost updates in concurrent stale single-writer snapshots; no multiwriter guarantee is issued.

## Independent new hostile evidence

22 NEW hostile cases authored and actually executed: **5 PASS / 17 FAIL**. Combined 159-case court: **140 PASS / 19 FAIL, exit 1**. Full per-case matrix, original and hostile JUnit, full stdout, reviewer-authored executable test source and sanitized environment passport are in the evidence archive `OUT3_EXECUTED_EVIDENCE.tar.xz` (local SHA-256 `fc876b665bd9af6328deec86aa66e93ec0eebf9048ca7a5a0d7d0630cd48bddd`).

- H02: omitted `envelope_mode` allows fully owner/issuer-shaped proposal to enter source-free legacy fixture path without a decider. H01 old minimal compatibility passes, but fixture privilege has no explicit boundary. Commission acceptance explicitly vetoes default legacy bypass.
- H03 × 4: differently cased nested `WORLD_OWNER`, `worldOwner`, `MEMORY_DELTA`, `Client_Perceived` evade case-sensitive directive denylist and are admitted under positive synthetic decider. No real downstream world mutation asserted.
- H04 × 3 and H05: whitespace source refs, empty or whitespace participant refs accepted in strict; `parent_refs=None` raises uncontrolled TypeError rather than typed refusal.
- H06: while public `perceive()` refuses a claimed human, public mutability of `projection.perceived` allows `has_perceived` to immediately return True for a caller-injected event; persistence validator blocks that particular forged record, but live in-memory witness query is unprotected against caller mutation.
- H07/H08: aggregate `deliver/ack` can advance without valid per-viewer opportunity and after sole viewer revocation. Per-viewer `offer` is still denied, so this is receipt-provenance confusion, **not** proof of genuine human perception.
- H09/H10/H11: restore accepts nonsensical global receipt counts and client ACK state; independent cold process accepts rehashed journal with negative aggregate delivery attempts. This demonstrates inadequate state validation, **not** an authenticated hostile-disk threat claim.
- H16/H17: empty viewer IDs can be authorized, and revoked viewer can be publicly regranted with no competent owner boundary on this sourcefree object. Does not establish actual production owner bypass.
- GREEN controls: H01 minimal legacy compatibility; H12 unkeyed hostile disk-forgery exclusion as *negative control*, not a security PASS; H13 negative synthetic decider; H14 cold revoked viewer denial; H15 explicit V1-to-V2 incompatibility refusal.

## Scientific grade and necessary action

**Positive evidence at sourcefree single-writer grade only:** real independent 135/137 replication; exact frozen semantic oracle custody; true pre/post-rename crash replay; per-viewer opportunity/refusal under tested paths; reproducible RTO repairs. Distinguish opaque metadata DIGEST binding from ADP019 issuer authentication; reliable POSIX-like isolated single-writer save from multiwriter transactional durability; projected opportunity or ACK from actual human perception.

**REVISE before scoped PASS:** isolate omitted legacy fixture capability; typed fail-closed nested admission schema, identity and parent-ref validation; immutable/query-authorized human-perception boundary; per-viewer-linked global receipts; strict global/client persisted-state invariants and failed-restore atomicity, followed by independent re-review. Competent S27 oracle custodian and multiwriter durable-store/ADP019 owner separately own the two retained original REDs. NO original respondent data, actual actor, client, human perception, production semantic or V3 grant was used. One reviewer, one isolated sourcefree workspace; no production files edited.

Raw testing receipts, all per-case identities, commands and logs are in `OUT3_EXECUTED_EVIDENCE.tar.xz`. The source-free archive is evidence, not an owner/issuer proof.