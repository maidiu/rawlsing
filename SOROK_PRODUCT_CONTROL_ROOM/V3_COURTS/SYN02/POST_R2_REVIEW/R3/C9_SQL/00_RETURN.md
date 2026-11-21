# SYN02-C9-R3 — test-only actor idempotency, status, CAS, mirror and C12 fork proof

**Return status:** `C9_R3_TESTONLY_SQL_DELIVERED__EXACT_REPLAY_AND_TYPED_CONFLICT_PROVED__HELD_FINAL_ORTHOGONALITY_PROVED__REQUALIFICATION_GRANT_REQUIRED__CAS_AND_ROLLBACK_PROVED__S36_SEVEN_TABLE_READSET_UNCHANGED__ACTUAL_C12_PERCEPTION_SUFFIX_FORK_HELD__C12_SOURCE_RED_REMAINS__OWNER_FREEZE_HELD__NO_NATIVE_GRANT`.

**Worker:** isolated sourcefree SQL engineer; not C9/C12/C8 storage owner, CAN/ADP/SCI05 issuer, production editor, independent hostile reviewer or self-adopter.

**Sealed startup:** `6b31fd3b87f757f1a67b119068c6f8d4198f15f9`.

**Active branch:** `agent/sorok-syn02-c9-r3-testonly-idempotency-isolated-r2`.

**Branch deviation:** the commission names `agent/sorok-syn02-c9-r3-testonly-idempotency-r1`. The original worktree at `/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/syn02-c9-r3-wt` was preserved after concurrent external writes appeared in `C9_SQL/` and `tests/`; the user directed continuation in a different worktree. The isolated branch above was created from the sealed startup. No original branch or worktree was rewritten, committed or pushed. The fixed branch name is not satisfied by this return and remains an owner/reviewer disposition.

**Actual source cuts:** S36 `8da78d8031a06a4bd7e1297fd713e573299c0860`, file hash `d8d5d36ff68a1fa254c829ffa07a8d19699533769791a6d49b0cdfdd23baa803`; imported C12/JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`, store hash `bb7bd721fa6b021a5b5163427495fd308236788d1738b8326f9f1093159b3c8b`, verifier hash `534780fe4631caadacac73e457afbb86bcc207686b1ebb433087ad6270abf710`.

## 1. Three court verdicts

| Court | Verdict | Meaning |
|---|---|---|
| **ENGINEERING** | `PASS_SCOPED_TESTONLY / CONTRACT_EXERCISED / C12_PERCEPTION_SUFFIX_FORK_HELD / C12_SOURCE_RED_REMAINS / OWNER_FREEZE_REQUIRED` | The test-only SQL helper implements exact replay, typed payload conflict, held/final status separation, fresh-grant requalification, CAS, source-change fork isolation, scoped two-actor targets, outbox/mirror/ACK recovery, and fail-closed C12 fork checks. It is not production C9/C12 code. |
| **SCIENCE** | `HOLD / RULE_A_T_SCI05_UNISSUED` | No Rule A/T, SCI05 admission, need, motive, care, memory, true-no-change or learning law is issued or proved. All rule and world values here are TEST_ONLY. |
| **AUTHORITY** | `HOLD / NO_NATIVE_GRANT / OWNER_FREEZE_NOT_ISSUED` | No C9/C12/C8/C11/Pyat/CAN/ADP/SCI05 storage or source-owner approval, native C12 release, A0–A5 person, production database or provider grant is issued. F1.1 is not authorized. |

## 2. Implemented test-only contract

Files are under `SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_R2_REVIEW/R3/C9_SQL/`.

- `schema_actor_r3.sql` — actor branch/version/head, receipt, attempt, fresh requalification grant, scoped target, external world receipt, legacy bridge, outbox, reconciliation and migration metadata. Append-only triggers cover Rule issuance, actor versions, receipts, attempts, world receipts, legacy bridge, targets and requalification grants. `decision_final_requires_issued_rule` refuses a final receipt without an issued Rule T.
- `schema_mirror_r3.sql` — C12 mirror branch with exact base perception identity, receipt projection, watermark and fault records. The watermark insert/update triggers require the exact receipt and projection at the claimed sequence.
- `c9_actor_r3.py` — application-level helper around those schemas. It is not a production C9 actor and does not edit C9/C12 source.
- `tests/test_c9_r3.py` — 15 sourcefree pytest cases covering C0–C7.
- `probes/actual_sources.py` — executable sourcefree probe over the actual S36 and imported C12 sources.
- `evidence/actual_sources.json` — captured probe output.

Behavior enforced:

1. A same-key/same-request-digest retry returns the exact original receipt and attempt, with no new sequence, version, receipt, attempt or Rule issuance. The unique idempotency key is read before insertion, so retry does not raise a raw `UNIQUE` exception.
2. A same-key/different-digest request raises `IdempotencyConflict`; a same-key/different-actor request raises `IDEMPOTENCY_KEY_SCOPE_MISMATCH`. Neither mutates the head.
3. A held decision cannot carry a committed Rule T status or evaluation basis. `TRUE_NO_CHANGE_EVALUATED` requires a concrete issued/evaluated Rule T, an occurred world receipt, co-presence and reception; it is never inferred from `NO_PROPOSAL` or `NO_EVENT`.
4. A final bit cannot be re-evaluated after `EVENT_ALREADY_FINALIZED`. A held attempt may be requalified only with the immediately next attempt number and a fresh `requalification_grant` referencing an issued Rule A/T or source issuance for that prior held attempt. The prior held receipt remains `HELD`.
5. Branch source cut/root changes are refused on the existing branch and require a fork branch. A fork inherits the exact parent semantic state while binding the new source cut, root, grant and C12 base identity.
6. CAS requires the complete expected branch epoch/version/head/receipt/finalized tuple. Partial mappings and stale heads return `CAS_CONFLICT`. Injected pre-commit failure rolls back the receipt, version, attempt, target, outbox and head update.
7. C9 commits first and creates a `PENDING` outbox row. Mirror projection is sequence-strict, requires a `CLEAN` watermark, is replay-safe, and does not duplicate the mirror receipt. ACK requires `PROJECTED` plus the exact mirror projection and a clean watermark; repeat ACK is a replay. Status is `CLEAN` only for an ACKed receipt whose projection matches the mirror.
8. C12 fork guard returns `FORK_HELD` for a perception-only suffix, an unproven/mismatched base perception set, a wrong base root, a non-clean mirror state, a missing branch or an unreadable source. It never returns `CLEAN`.
9. The S36 legacy publication domain remains exactly seven tables and is not written by the C9 actor DB.

## 3. Executed evidence

Host: Darwin 22.6.0 x86_64; Python 3.11.3; SQLite 3.40.1; pytest 9.1.1; local sourcefree execution only.

| Check | Result |
|---|---|
| `python3 -m pytest -q tests/test_c9_r3.py` | **15 passed** |
| C0 S36 isolation | Actual targetless S36 receipt `1cec8633d861959c7d4b744c6770f9720110e977f021f460a1608e1aebbf4ee9`; seven tables; readset `b3cc7c9e4a55ccce935f0cdbea9fbd8db003c59467748f805df317d51310214d` unchanged after isolated C9 writes |
| C1 exact replay | Exact receipt JSON and attempt returned; no new version, receipt, attempt or Rule issuance |
| C2 conflict | `IdempotencyConflict` for changed digest; `IDEMPOTENCY_KEY_SCOPE_MISMATCH` for another actor; head unchanged |
| C3 CAS/fault | Stale and partial expected heads refused; injected `C3_INJECTED_FAILURE` leaves no ghost receipt, version, attempt or outbox |
| C4 commit-before-mirror | C9 outbox `PENDING`; status `SYNC_HELD`; projection allowed only with clean watermark; `SYNC_HELD` blocks project; status `CLEAN` only after mirror and ACK |
| C5 ACK idempotency | Duplicate project leaves one mirror receipt and one projection attempt; duplicate ACK replays; one mirror receipt remains |
| C6 actual C12 suffix | Parent `QualifiedC12Store.verify` `ok: true`, `last_clock()=10`, perceptions `[10,11]`; guard `FORK_HELD / C12_PERCEPTION_ONLY_SUFFIX`, `fork_cut=11` |
| C6 same-count substitution | Child `QualifiedC12Store.verify` `ok: true`, equal perception count, parent perception hash `e125cee41e099b21bbf426527b780dda564931961328496bd0a9e6cf6e497b22`, child hash `9216978656742b5273bf0eb4fefcd76ae1df58522b7d40f59cf012ed4b3af0ba`; guard `FORK_HELD / C12_BASE_PERCEPTION_IDENTITY_MISMATCH` |
| C6 wrong root / missing source | `FORK_HELD / C12_BASE_ROOT_MISMATCH`; `FORK_HELD / C12_READ_FAILED` |
| C7 orthogonality/raw guards | Held + committed status refused; no-proposal true-nochange refused; final without issued Rule T refused; old held receipt preserved; append-only and outbox/watermark triggers refuse mutation |
| C7 two actors | Actors A and B commit the same legacy target ID in separate actor-scoped rows |
| C7 normal fork | Identity-unproven base stays held; exact supplied base identity returns `FORK_READY` with cut 10 |
| C7 true no change | Issued Rule T creates `ADMINISTRATIVE_NOCHANGE` and an `ok` actor verification |

Actual probe command and evidence:

```sh
cd SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_R2_REVIEW/R3/C9_SQL
python3 -m pytest -v tests/test_c9_r3.py
python3 probes/actual_sources.py --json-out evidence/actual_sources.json
python3 -m py_compile c9_actor_r3.py probes/actual_sources.py tests/test_c9_r3.py
```

The actual S36 probe reports old receipt before/after hashes `9c5137f214d299bdb627c72ac8ff1880be98822d56082ec8ecce3eea0ba3fe62` and `07d38064535ec54c9d96a570775dc70b4a4d285453ccdcbe739ecb8ba3df01b6`; its seven-table readset is `b3cc7c9e4a55ccce935f0cdbea9fbd8db003c59467748f805df317d51310214d` before and after the isolated C9 writes.

## 4. Exact artifacts

| Artifact | SHA-256 |
|---|---|
| `schema_actor_r3.sql` | `0ae69ef5b76177950c0b9c40e7bb20db11cf41d4697a5e4a1d6b08b459c82b90` |
| `schema_mirror_r3.sql` | `5f3f2895af2a5443dd87ade6714675677b96be23be15544714fdc16e12f58821` |
| `c9_actor_r3.py` | `ee4765e28d80531e6b5450296ed209ef4e3303b827910bbf20b73dfaba52725e` |
| `tests/test_c9_r3.py` | `35b8affe9256314619d7695321b4d5562a1c0cc8631a5740516e013ceff69b46` |
| `probes/actual_sources.py` | `1bca8091b175fe4f8b9721f851c52f2567594c79fa328924235c6e5ca68d9813` |
| `evidence/actual_sources.json` | `c2d7b979cd1e64524919678bb85b9eef7bfa7ea5e57785d8ad0334623aad21a6` |

The actor schema application ID is `1129533491`; the mirror schema application ID is `1129533492`; both declare `NOT_OWNER_FROZEN`.

## 5. Future E2 semantic reader proposal

First proposed consumer: `E2_SEMANTIC_READER_TESTONLY@0`, not implemented and not authorized.

- Input: exact `actor_id`, `branch_id`, `branch_epoch` and a read-only C9 actor database.
- Read only `actor_head`, its referenced `actor_version`, and the referenced `decision_receipt`; return `version_hash`, `semantic_hash`, `canonical_state_json`, `source_cut_hash`, `last_receipt_seq`, `last_finalized_seq` and a drift hash.
- Refuse on missing/mismatched head/version/epoch, a non-final version with a final decision, a receipt/version hash mismatch, or any semantic projection that cannot be reconstructed from the stored version.
- Never evaluate Rule A/T, never write C9/C12, never treat an outbox or mirror row as source authority, and never return `CLEAN` for a held C12 fork.
- Require the caller to present `projection_outbox` and mirror status only as separate delivery evidence, not as actor semantic authority.

## 6. Owner freeze gate and residual risks

No owner freeze is issued. Before any production or F1.1 use, the C9 and C12 owners must independently decide:

1. Whether this actor schema and its exact hash are acceptable as a basis for an owner-frozen C9 actor contract.
2. Whether the C12 owner patches perception-inclusive fork/root/count/transaction behavior or hard-installs `FORK_HELD`; this return does not repair C12 source.
3. How a real adapter binds the frozen S36 publication domain, separate C9 actor DB, C12 source and mirror without claiming cross-database ACID.
4. Which actual C8 world receipt, C1 recovery case, Rule A/T issuance and SCI05 admission are authoritative.
5. Which distinct independent reviewer accepts or rejects this return; this worker cannot self-adopt.

Residual risks and limits:

- C12 remains a reproduced source RED: actual `fork` loses a perception-only clock suffix while `QualifiedC12Store.verify` still returns `ok`.
- `c12_fork_guard` is a fail-closed test guard, not an original C12 source fix. It requires callers to provide the exact base root/perception identity; unproven identity returns held.
- `MirrorStore.verify` checks internal mirror consistency only; it does not read the live C12 source. A production adapter must combine it with `c12_fork_guard`.
- Mirror receipt commit and actor outbox update are separate SQLite transactions. The outbox is intentionally allowed to remain `PENDING`/`PROJECTED` for recovery; no cross-database atomicity is claimed.
- The helper uses TEST_ONLY hashes and no cryptographic signing or native custody. It is not an authorization system.
- The original worktree contains untrusted concurrent changes and is preserved but not used or committed.

## 7. NOT_RUN

- Full S36 39-test suite and full BP4/C12 15-test suite; only the targeted actual-source probes and the 15 C9-R3 tests were run here.
- Production C9/C12 integration, native C8/C9/C11/C12/A5, C11/Pyat, real B/world, SCI05, Rule A/T issuance, paid provider/model calls, production database, owner freeze.
- Distinct independent hostile review and owner adoption; the compact review below is non-independent.

## 8. Compact self-review — non-independent

**Findings:** the helper is test-only and does not implement a production publisher; the mirror is not a live C12 adapter; and the C12 guard is a detector/guard rather than a source repair. Those are intentional limits, not PASS claims.

**Tested failure paths:** raw UNIQUE replay, digest conflict, cross-actor key scope, held/committed status contradiction, true-nochange without Rule T, no-proposal true-nochange, final without issued Rule T, stale/partial CAS, injected rollback, source change on a live branch, missing/failed requalification grant, duplicate project/ACK, non-clean watermark, exact watermark receipt, append-only mutation, two actors sharing a target ID, C12 perception suffix, same-count substitution and missing C12 source.

**Residual review risk:** `MirrorStore.verify` and `ActorAuthority.verify` are internal invariant checks, not formal proofs. An independent reviewer must inspect the exact schema, replay the commands, and verify that the test-only adapter boundary is not mistaken for production authority.

**Remote SHA:** deliberately not embedded in this self-modifying return; the committing worker must read back the final remote branch SHA after push and report it externally.

**No source edit outside `C9_SQL`. No production DB. No owner freeze. No Rule A/T. No science. No native C12/A5. STOP.**
