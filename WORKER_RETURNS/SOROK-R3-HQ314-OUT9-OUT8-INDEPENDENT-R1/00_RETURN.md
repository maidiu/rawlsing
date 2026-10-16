# HQ314 OUT9 — independent OUT8 restored-receipt court — reviewer return

**Verdict:** `REVIEW_PASS_SCOPED_SINGLE_WRITER_SOURCEFREE`
**Scope of verdict:** source-free single-writer outbox custody court only — no
real client perception, no real material world, no multiwriter proof, no
ADP-019 event authority, no semantic adoption, no V3 operation.

## Role, branch, sealed startup

- **Role:** fresh independent I2 source-free outbox reviewer. NOT author
  OUT8/OUT6/OUT7, NOT HQ, NOT ADP019 issuer, NOT client-perception witness.
- **Branch:** `agent/reviewer-sorok-r3-hq314-out9-out8-independent-r1`.
- **EXACT SEALED STARTUP:** `f791d6881a465442ae6fc4a117b83e864ee8e426` — verified
  equal to direct remote branch HEAD before any write (launch SHA and branch tip
  agreed at start; no mid-flight commission revision occurred).
- **HQ314 parent:** `f9b4fd61eb64ad644b590b644450ac5563b6d151`.
- **Write terrain (exclusive):** `WORKER_RETURNS/SOROK-R3-HQ314-OUT9-OUT8-INDEPENDENT-R1/`.
- **Commission + binding reads:** commission file at startup; Sorok
  `00_READ_ME_FIRST`, `00B`, `00C` (§3A/§3B/§5A), `00D`; HQ314 intake
  `HQ314_OUT8_M03_RETURN_FANIN_OC6_PENDING_AND_TWO_INDEPENDENT_COURTS_R1.md` and
  HQ313 fan-in at parent; OUT8 author `0e05c7dab8334b96f2b2b79e935eeebb1c0f0d11`
  (00_RETURN, 01_EXECUTION_INDEX, 02_OWNER_HOLDS, 03_REPRODUCE, source/test
  archive); OUT7 independent `d3d0836d922dcb88eaf0a0591e66551aa6fb9f0a`; OUT6
  author `673233571b7d899c309dd26f9b9cd2508404c0b6`; OUT4
  `2afa3022e5551df71b739cf8689e832db85e1196`; OUT3 exact
  `0ab31e4198299708e700840c1b68e0d94a2ced06`.

## One coherent outcome

**The author's repaired closure reproduces exactly, and the repairs hold under
independent attack.** The literal 247-case suite was reconstructed from pinned
provenance (not from author claims), executed unchanged, and reproduced
**245 PASS / 2 retained historical REDs** — identical to the author expectation.
The two REDs are preserved untouched: `test_s27_material_move_needs_world_owner`
(S27 forbidden/unissued mug physical movement) and
`test_replay_manual_two_writers_can_lose_first_committed_event` (two-writer
stale journal race). No skip, xfail, edit or relabel was applied.

## Provenance reconstruction (independent, not author-trusted)

| Step | Evidence |
|---|---|
| original 137-suite closure | OUT4 archive `OUT4_EXECUTED_EVIDENCE.tar.xz` staged byte-exact (5 modules + 6 test files) |
| source lineage | original source `c7bb4169d43c715de7dd113b24d3ce897e37beab` → `patch OUT6_EXACT_SOURCE.patch` → verified `aa002cb634e81cb980820c14220a1ab55bc5e015` (sha256 `b58da0f5…`) → `patch OUT8_EXACT_SOURCE.patch` → verified `331840768ce0b5f6f73e5e93094ca0d217ddaebf` (sha256 `5c994f29…`) |
| test provenance | OUT3 `test_out3_independent_hostile.py` (`c1fce628…`), OUT4 harness (`337b1098…`), OUT6 `test_out6_receipt_repair.py` (`c1bbfddd…` from `.xz`), OUT7 `test_out7_independent_hostile.py` (`0a2bc82c…`), OUT8 `test_out8_restored_state_repair.py` (`d23e6cfc…`) |
| pin verification | **16/16 pinned files match their authoritative identities** (git blob SHA-1, NUL-header method) — see `evidence/source_hash_ledger.json`; the one non-pinned file is my own new court |
| imports | real `module.__file__` resolves into the isolated staging dir (`candidate/outbox_prototype.py`); subprocess cold tests run real child processes |
| JUnit/commands | exact author command form; `junit/literal247.xml`, `junit/out9_hostile_junit.xml`, `logs/*_stdout.log` |

Per-module literal result (matches the author's frozen counts exactly):

| Module | Cases | Pass | RED |
|---|---|---|---|
| test_sr_28_falsifier_court | 28 | 27 | 1 (S27) |
| test_rsr_independent | 17 | 17 | 0 |
| test_rsr_cold_replay | 2 | 2 | 0 |
| test_cold_repair | 9 | 9 | 0 |
| test_rto_hostile | 57 | 56 | 1 (two-writer race) |
| test_out2_cross | 24 | 24 | 0 |
| test_out3_independent_hostile | 22 | 22 | 0 |
| test_out4_independent_harness | 29 | 29 | 0 |
| test_out6_receipt_repair | 18 | 18 | 0 |
| test_out7_independent_hostile | 21 | 21 | 0 |
| test_out8_restored_state_repair | 20 | 20 | 0 |
| **TOTAL** | **247** | **245** | **2** |

## Independently frozen expectations (before any new test)

`01_INDEPENDENT_FROZEN_EXPECTATIONS.json` — frozen before executing my own
court; explicitly recognizes OUT7 I08/I09/I13/I14 as known findings and declares
N01–N25 as complementary (no duplication).

## My new independent court — 25/25 at real entrypoints

`candidate/test_out9_independent_hostile.py` (JUnit `junit/out9_hostile_junit.xml`,
stdout `logs/out9_hostile_stdout.log`). All expectations met:

**Legitimate positives enforced (must validate, and do):** N01/N02/N09 —
genuine historical receipts of formerly-authorized (now revoked) viewers survive
validation, including 3-viewer congruence with one revoked; N07 — ACTIVE
`NOT_SENT` zero-attempt placeholder remains lawful; N23 — complete lawful
multi-viewer chain survives cold reload and validates; N14 — a **valid** journal
record whose unkeyed digest was recomputed still recovers and validates
(recovery is not authorization); N18 — remaining-authorized viewer retries
lawfully after another viewer's revocation; N19 — terminal ACK immutability
across cold reload; N24 — duplicate admission returns the single deterministic
event identity.

**Hostiles refused with typed codes (all):** N03 `INCONSISTENT_DELIVERY_STATE`
(client zero-attempt masquerading as ACKed); N04 `BAD_DELIVERY_IDENTITY`
(ack_count=2); N05/N06 `BAD_AGGREGATE_DELIVERY_COUNTS` (aggregate ack=2 /
acknowledged-with-zero-attempts); N08 `FORGED_ZERO_ATTEMPT_CLIENT_HISTORY`
(revoked tombstone forged to zero attempts); N10 `GHOST_VIEWER_AUTHORIZATION`;
N11 `CORRUPT_REVOKED_VIEWER`; N12 `FORGED_LAST_ATTEMPT_ID`; N13
`BAD_WORLD_STATE_SHAPE` — N10–N13 each also verified **detached-restore
atomicity** (live snapshot byte-unchanged after refusal); N15 cold tampered
payload + recomputed digest refused; N20 revoked-viewer `emit_to` returns `None`
with no new attempt; N21 ghost projection opportunity refused; N22
`FORGED_AGGREGATE_ACK_WITHOUT_CLIENT_RECEIPT` (aggregate ACK with only a FAILED
client receipt); N25 cold-forged revoked tombstone refused with
`FORGED_ZERO_ATTEMPT_CLIENT_HISTORY`.

**Cold crash atomicity (real subprocess, `os._exit`, real files)** —
`evidence/cold_crash_evidence.json`: BEFORE_RENAME → child exit 79, prior
journal bytes **byte-identical**, only a pending temp file left, recovered prior
state validates; AFTER_COMMIT → exit 79, newest committed state durable,
recovered and validated; tampered payload with recomputed unkeyed digest →
REFUSED (`BAD_AGGREGATE_DELIVERY_COUNTS`).

## What this verdict does and does not establish

**Establishes (source-free grain):** the literal 247 reproduce exactly; the two
historical REDs are preserved; the OUT7-repaired invariants — strict aggregate
ACK/client-ACK congruence across ACTIVE and formerly-authorized REVOKED viewers,
forged zero-attempt revoked tombstones, detached-restore atomicity, cold
journal recovery after digest recompute, crash atomicity, multi-viewer
behavior and ACK terminal immutability — hold under my independent attacks; 25/25
new hostiles pass; 220-style owner-suite behavior unchanged (all pinned
identities verified).

**Does NOT establish:** real client ACKs (all client receipts are fixture
state); human perception (`projection.perceive` stays unauthorized; my tests
never assert it); multiwriter safety (the two-writer RED is preserved, not
repaired); ADP-019 event authority; any population/psychology claim; OUTP policy
selection; OUT5 acceptance.

## Non-claims honored by construction

- Unkeyed journal hash is not independent external provenance (N14: recomputing
  it over valid bytes only enables recovery, never authorization; N15/N25:
  tampering is refused by state validation, not by digest trust).
- No test reads OUT5's unpublished suite; OUT5 remains `NOT_RUN_UNPUBLISHED`.
- No helper agent, no model switching, no semantic adoption, no production
  registry, no V3 wake, no canonical merge.

## Deliverables (`WORKER_RETURNS/SOROK-R3-HQ314-OUT9-OUT8-INDEPENDENT-R1/`)

| Path | Content |
|---|---|
| `00_RETURN.md` | this reviewer return |
| `01_INDEPENDENT_FROZEN_EXPECTATIONS.json` | my frozen expectations + falsifiers (pre-execution) |
| `candidate/` | the full pinned closure (11 test modules + 5 modules) + my new court + `cold_crash_evidence.py` |
| `junit/` | `literal247.xml`, `out9_hostile_junit.xml` |
| `logs/` | `literal247_stdout.log`, `out9_hostile_stdout.log` |
| `evidence/` | `source_hash_ledger.json`, `case_by_case_matrix.json`, `per_module_247.json`, `cold_crash_evidence.json`, `final_run_summary.json` |
| `05_POLICY_AND_HOLDS.md` | OUTP L1/L2 + A1/A2 HOLDS, OUT5 NOT_RUN_UNPUBLISHED, model/privacy/usage HOLDs |
| `environment_passport_delta.json` | sanitized 00D passport |
| `06_REMOTE_VERIFICATION.json` | direct remote SHA + changed-path scope receipt (after push) |

## Environment / cost

Python 3.11.3, pytest 9.0.2, git 2.43.0, real subprocess cold tests. **Model
calls: 0. Cash: UNKNOWN (nothing billed).** Authoring environment: Step 5
Preview through the owner's OpenCode setup (user-reported free; no ongoing
capacity assumed). No pre-existing local Git object store was present; the
isolated closure was materialized minimally from authenticated reads with full
hash verification (no clone-per-worker, no giant history download).

## Remaining owner decisions (not mine)

1. OUTP L1 vs L2 legacy fixture grammar; OUTP A1 vs A2 transport vs
   projection-opportunity ACK — competent owner, downstream.
2. Real ADP-019 admission producer and external anchor.
3. The two preserved REDs remain separate scopes: S27 material-movement world
   owner; two-writer staleness (explicitly non-goal here).
4. OUT5's exact 14 remain publication evidence, not executable source here.
