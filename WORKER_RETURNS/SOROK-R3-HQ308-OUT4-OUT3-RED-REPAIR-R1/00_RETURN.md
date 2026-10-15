# Sorok HQ308 OUT4 — bounded source-free outbox regression repair

**Disposition:** `SOURCEFREE_REPAIR_CANDIDATE_RETURNED__BASELINE_135P_2_RETAINED_REDS__29_NEW_HOSTILES_PASS__OUT3_22_EXACT_SOURCE_NOT_RERUN__I2_REVIEW_REQUIRED__NO_ADOPTION`.

**Role:** One commissioned bounded implementer; NOT HQ, independent accepting reviewer, competent ADP019 owner, material-world owner, actor or real perception witness. All committed files confined to `WORKER_RETURNS/SOROK-R3-HQ308-OUT4-OUT3-RED-REPAIR-R1/`. **Sealed startup:** `b9c43dad31771b97cc1a2a8fffd25fae77bbbe55`, direct remote HEAD matched before worker edits.

## 1. Exact source, frozen authority and environment

- OUT2 authored source bank: `b1004a43eb0309af99e1b7ce9d5290df3c07f3cd`, original archive SHA-256 `812070f33567fbac5ebada32cfa18fdc190e855230f87cc6108bfc4941b5a2f5` (verified byte-identical on this host).
- Original OUT2 import `outbox_prototype.py` native Git blob SHA-1 `d40f532a2f9c4ee12a7f99f0ef37164fe997518b`. Repaired isolated candidate native Git blob SHA-1 `c7bb4169d43c715de7dd113b24d3ce897e37beab`. Module import is from `stage/outbox_prototype.py`, not production or owner code.
- Frozen S01–S28 *semantic* specification blob `782ba75ee94f24908100b1f3464e7035497d546c` unchanged; all eight original source/testing blobs pinned by OUT2 hash receipt verify **identical** here. No original tests rewritten, xfailed or skipped.
- Independent OUT3 review source at commit `0ab31e4198299708e700840c1b68e0d94a2ced06` reports 22 independent hostility tests / 17 REDs; its archive SHA256 `fc876b665bd9af6328deec86aa66e93ec0eebf9048ca7a5a0d7d0630cd48bddd` and Git blob `a9c4ee7344526fa335605d76d08def2ac5dcba2a` were authenticated. **Its 22 original executable test source files were NOT materialized or run here.** GitHub delivered their binary archive as encoded connector content, but source extraction into this isolated runtime was blocked; newly written OUT4 tests follow the reported failure classes and are **not** falsely described as byte-identical OUT3 tests. This is an explicit material outstanding test gate, not a complete 17/17 independent closure certification.

## 2. Actual executed suites

| Executed | PASS | RED | Exit | Grade |
|---|---:|---:|---:|---|
| Original 137 before repair | 135 | 2 | 1 | source-free pinned original |
| Original 137 after repair (unmodified) | 135 | 2 | 1 | source-free pinned original |
| OUT4 author-authored hostile/cold cases | 29 | 0 | 0 | source-free new, not independent OUT3 exact bank |
| Combined observed postrepair | 164 | 2 | 1 | baseline plus added cases |
| Independent OUT3 exact 22 | NOT EXECUTED | NOT EXECUTED | N/A | source-transport blocker |

**Deliberately retained RED 1:** original authored `test_s27_material_move_needs_world_owner` expects mug change from table to hand, contradicting frozen S27 `world_authority=MISSING`; mug remains unchanged. **RED 2:** original `test_replay_manual_two_writers_can_lose_first_committed_event` demonstrates stale simultaneous writers can overwrite an earlier journal snapshot. The candidate explicitly supports ONLY one writer, not multiwriter linearizability or accepted ADP019 durability.

Real Python 3.13.5 and pytest 9.0.2 with subprocess/os._exit(79) tested. New 29 include before-rename exit=79, after-commit exit=79, independent recovery of revoked viewer state, a corrupted rehashed journal, failure-atomic restore, malformed global/client counts, and strict receipt transitions. Raw real stdout/JUnit and source files are in `OUT4_EXECUTED_EVIDENCE.tar.xz`.

## 3. Source-free repairs and positives

1. **No omitted-mode owner downgrade.** The original minimal S01–S28 fixture path is preserved. A proposal shaped like a complete owner/issuer envelope with no explicit `STRICT` is refused `MISSING_STRICT_ENVELOPE_MODE`; unknown explicit modes are still rejected.
2. **Normalize forbidden directives.** Case variants, separator variants, camelCase and nested/list keys such as `WORLD_OWNER`, `worldOwner`, `MEMORY_DELTA`, `Client_Perceived` are structurally refused, including under a synthetic positive decider. This is a bounded denylist and not a full ADP019 canonical grammar.
3. **Reference validation.** Empty/whitespace source and participant reference items are rejected; `parent_refs=None` returns a typed refusal before iteration rather than uncaught TypeError; strict callback is still an injected test-only witness, not issuer authentication.
4. **Viewer permission and revoke.** Empty viewer IDs are refused; viewer revocation persists through the journal as a monotonic source-free denylist, and the public regrant path cannot reverse it. No production issuer/role registry is constructed.
5. **No false human perception.** `perceive` and `has_perceived` cannot return actual human-perceived evidence from externally mutable fixture `perceived`, even if a forged callback or direct dict mutation asserts success. `validate_state` separately refuses attempted persisted human perception.
6. **Global receipt provenance.** When viewer-scoped paths exist or the event is in strict synthetic mode, aggregate `deliver`/`ack` cannot advance without an authorized per-viewer client delivery plus recorded opportunity; legacy no-viewer scalar counters remain documented fixture-only. Revocation shuts down those aggregate transitions. Per-client receipts remain distinct from human knowledge.
7. **Persistence invariants.** Snapshot/restore checks actual nonnegative aggregate attempts, legal finite ACK values and state/attempt coherence, stronger client attempt/ACK coherence, revoked-viewer consistency, and links client receipts to global intent. Failed restore remains failure-atomic. Legacy V1 journal remains refused; no fictional schema migration.

## 4. Limits, BLOCK and next competent actions

The **independent OUT3 exact 22 execution gate is unsatisfied**, despite 29 new author tests passing. Separate I2 review MUST materialize exact `OUT3_EXECUTED_EVIDENCE.tar.xz`, rerun the untouched 22, and challenge false-positive source-free permissions before any `REVIEW_PASS`. Material-world ownership/S27 oracle-custodian disposition, multiwriter journal architecture, cryptographically authenticated disk protection, external client dispatch/ACK and human perception are independent owner fronts, NOT implied by this source-free repair. Neither a synthetic `admission_decider=True` nor a SHA-256 file digest authenticates competent ADP019 authority. No model calls, original data, V3 actors, production code changes, protected CURRENT/PRE-MAIN mutation or adoption.

## 5. Recorded execution commands and remote custody

Run from isolated `stage/`:

```
python -m pytest -q test_sr_28_falsifier_court.py test_rsr_independent.py test_rsr_cold_replay.py test_cold_repair.py test_rto_hostile.py test_out2_cross.py --junitxml=after_137_junit.xml
python -m pytest -q test_out4_independent_harness.py --junitxml=after_new29_junit.xml
```

True original suite exit 1 is the two known REDs. New suite exit 0. All paths in a sandboxed return archive. This report intentionally does not self-embed a future commit SHA; direct final branch head is checked AFTER push and transmitted in the worker response.
