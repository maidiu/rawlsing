# SOROK C8O — executable trusted outbox and legacy-writer boundary R1

## Identity, custody and governing law

- Repository: private `maidiu/rawlsing`.
- Assigned branch: `agent/rabochii-sorok-20261019-c8o-out14-writer-authority-executable-boundary-r1`.
- Sealed startup (commission-only commit, verified remote before work): `27c3a802ff4d55cc9ad0c045cf56b32a48e15884` — parent `9fa6744878a7bb493b4202fa80fcc900e74a7c7c`, sole changed file `WORKER_COMMISSIONS/SOROK-20261019-C8O-OUT14-WRITER-AUTHORITY-EXECUTABLE-BOUNDARY-R1/00_COMMISSION.md`.
- Exact OUT14 return intake: `a77f0f8e45ee27133576209c315e53341dcb5a9e` (`WORKER_RETURNS/SOROK-V2-HQ322-OUT14-MULTIWRITER-INTEGRITY-REPAIR-R1/00_RETURN.md`).
- HQ routing addendum read: `SOROK_PRODUCT_CONTROL_ROOM/HQ_MOTIONS/20261019_FOUR_LANE_DUAL_SIDED_MODEL_ECONOMY_ADDENDUM_R1.md` (C8O lane = `IN_BETWEEN_MEDIUM_RECOMMENDED`). Model selected: **MiMo-V2.6-Pro** in the user-selected OpenCode harness; model tier `IN_BETWEEN`, zero model switches, zero harness switches.
- Role: bounded source-free C8 occurrence/event journal and trusted-writer **integration candidate / owner-custody investigator**. NOT HQ, NOT ADP019 issuer, NOT production integrator, NOT independent I2 reviewer, NOT Pyat worker.
- Write scope: **only** `WORKER_RETURNS/SOROK-20261019-C8O-OUT14-WRITER-AUTHORITY-EXECUTABLE-BOUNDARY-R1/`. Original OUT9/12/13/14 sources and frozen tests are staged read-only and byte-verified; no canon, ADP019, CAN, production, PRE-MAIN, Pyat or HQ CURRENT edits.

## Disposition

**`EXECUTABLE_SOURCEFREE_C8_INTEGRATION_CANDIDATE_COMPLETE__SECURITY_NOT_PROVED`**

Typed authority HOLDS preserved (nothing self-granted):

| Typed form | Status |
|---|---|
| `C8_TRUSTED_WRITE_OWNER_HELD` | **HELD** — no owner issued old-writer exclusivity or trusted-writer grant |
| `LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED` | **OPEN** — accepted `Journal.commit` remains a legally callable writer (executed counterexample) |
| `C8_TRUSTED_ANCHOR_UNISSUED` | **HELD** — no external monotonic anchor issued |
| `C8_CAPABILITY_TRUST_ANCHOR_UNISSUED` | **HELD** — no keyed writer capability issuer exists; fingerprints are unkeyed |
| `C8_EFFECTIVE_CLOCK_SOURCE_UNTRUSTED` | **HELD** — real OS clock recorded with source label; trusted time refused typed |
| `ADP019_ADMISSION_RECEIPT_ABSENT` | **HELD** — worker is not the V3 External Admission Court |
| `C9_LATER_ACTION_CONSUMER_UNBOUND` | **HELD** — interface request exposed, no native C9 positive |
| security claim | **`NOT_PROVED`** for writer authentication and anti-rollback |

---

## A. Inherited real executable closure — RECONSTRUCTED AND EXECUTED

The earlier Browser environment failed only for want of the pinned local
`outbox_prototype` module. Locally the full Git object store was available; the
closure was reconstructed byte-exactly and every staged file verified against its
Git blob SHA-1 (`evidence/source_import_ledger.json`, 33 rows, all verified;
`runtime/stage_out12/outbox_prototype.py` = `331840768ce0b5f6f73e5e93094ca0d217ddaebf`
= the accepted OUT9 baseline; OUT12 module `99217d390a452f22fc1a470abc411c6ca84b86ba`;
OUT14 repaired module `7488353f492cccac86a5d6a02937d3f2bf052341`; OUT14 frozen test
`1cc37c428a995e89419b4b4ceb8e95995c4ff7f6`). Import paths were verified to resolve
inside this return (`court/test_c8o_source_ledger.py`).

Executed suites (real `python3 -m pytest`, JUnit + stdout in `junit/`, `logs/`):

| Suite | Command scope | Result | JUnit |
|---|---|---|---|
| Inherited original court (OUT9-era union incl. OUT9's 25 hostiles) | `runtime/stage_out12`, all inherited `test_*.py` except OUT12's | **272 cases: 270 PASS / 2 historical RED preserved** | `junit/original_272.xml` |
| OUT12 nine author cases (unedited) | `test_out12_multiwriter_court.py` | **9/9 PASS** | `junit/out12_author_9.xml` |
| OUT13 frozen hostile court (unedited) | `runtime/out13_return/test_out13_hostile.py` | **23/23 PASS** | `junit/out13_hostile_23.xml` |
| OUT14 new court (previously NOT_RUN) | `runtime/stage_out14/test_out14_integrity.py` | **27/27 PASS** | `junit/out14_new_court.xml` |
| New C8O hostile court (this return) | `court/` | **62/62 PASS** | `junit/c8o_new_court.xml` |
| Regression: inherited 272 under the OUT14-repaired module | `runtime/stage_out14` | **270 PASS / 2 historical RED preserved** | `junit/regression_272_under_out14.xml` |
| Regression: OUT12 nine under the OUT14-repaired module | `runtime/stage_out14` | **9/9 PASS** | `junit/regression_out12_9_under_out14.xml` |
| Regression: OUT13 twenty-three under the OUT14-repaired module | `runtime/out13_return_out14` | **22 PASS / 1 RED (see below)** | `junit/regression_out13_23_under_out14.xml` |

Both historical REDs are preserved, unmodified, unskipped and unrelabeled:

- `test_rto_hostile.py::test_replay_manual_two_writers_can_lose_first_committed_event`
- `test_sr_28_falsifier_court.py::test_s27_material_move_needs_world_owner`

**Two honest staging facts.**

1. OUT14's frozen crash-worker case spawns `worker.py` with `subprocess.run`
   without its own `sys.path` staging, so its four
   `test_rename_crash_boundaries_and_true_signal` cases need the staged candidate
   dir on the ambient `PYTHONPATH` (without it: 23 passed / 4 `ModuleNotFoundError`).
   With the pinned `PYTHONPATH` the whole OUT14 court executes 27/27. This is an
   import-staging defect of the frozen OUT14 test, not a mechanism failure; the
   frozen file was not edited (`logs/out14_new_court_stdout.log`).
2. OUT13's `test_hp8_corrupting_writer_version_resets_to_zero_and_defeats_the_CAS`
   is a **defect-demonstration oracle** ("HP8 FAILED: CAS did not accept the reset
   version"). It necessarily REDs once OUT14's repair refuses the corrupted version
   with typed `VERSION_STATE_UNREADABLE`. The divergence is recorded as
   `HP8_DEFECT_ORACLE_CLOSED_BY_OUT14_REPAIR`, never as a safety regression.

## B. Owner-authority / bypass reality — EXECUTED COUNTEREXAMPLE

Complete legally-callable write entrypoint enumeration with lock / version /
capability attributes per entrypoint: `evidence/write_entrypoint_enumeration.json`.
The accepted `outbox_prototype.Journal.commit(self, p, crash_boundary=None)` and
`admit_and_queue(...)` take **no lock, no version precondition, no capability**;
`court/test_c8o_legacy_writer_bypass.py` proves in a **real separate OS process**
that this writer:

- **wipes/replaces** a journal holding three acknowledged occurrences
  (before/after bytes, attacker PID and destroyed occurrence ids:
  `evidence/legacy_writer_bypass_counterexample.json`);
- can do so **while the wrapper's own receipts are green**
  (`evidence/green_wrapper_then_bypass_erasure.json`);
- **loses a cooperative event** on an interleaved stale commit
  (`evidence/interleaved_legacy_lost_event.json`);
- is only **detected after the fact** (`LEGACY_WRITER_BYPASS_DETECTED`, prevention
  `NOT_POSSIBLE_WITH_CURRENT_LEGAL_CALLABLE_API`).

**Determination on whether any competent accepted authority restricts it: NO.**
No accepted source, HQ motion, grant or ADP019 document examined restricts the old
journal writer (ADP019 governs event admission, not file writers). The candidate
therefore leaves `LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED` typed and operates
under an explicit local declared single-authority assumption. The precise
competent-owner decision docket (D1 old-writer exclusivity, D2 trusted anchor /
keyed capability, D3 ADP019 interface) is `docket/OWNER_DECISION_DOCKET.md`.
No grant is issued or simulated here.

## C. Trusted writing, rollback and receipt — COUNTEREXAMPLES EXECUTED

Mechanism preserved in `candidate/c8o_trusted_outbox.py` (new, coherent,
non-installing): atomic compare-and-append under real `fcntl.flock`; sealed
`writer_version` + `version_state_digest` + `ledger_prefix_digest` + writer
identity + effective clock; genesis version zero only for a nonexistent file;
typed `VERSION_STATE_UNREADABLE` / `LEGACY_WRITER_BYPASS_DETECTED` /
`ACKNOWLEDGED_LEDGER_PREFIX_REWRITE_NOT_GRANTED` / `GHOST_REPLAY_REFUSED` /
`WRITER_CAPABILITY_REQUIRED` / `JOURNAL_LOCK_TIMEOUT` / `STALE_JOURNAL_CONFLICT`;
real effective clock with `C8_EFFECTIVE_CLOCK_SOURCE_UNTRUSTED` label and typed
refusal of trusted-time claims.

Executed falsifiers (these are the security science of the return):

| Counterexample | Evidence |
|---|---|
| recomputed unkeyed digest over a forged version/writer is accepted | `evidence/unkeyed_digest_forgery_counterexample.json` |
| full history rewrite with every digest recomputed is accepted | `evidence/history_rewrite_counterexample.json` |
| rollback to an earlier **byte-valid** receipt passes every unkeyed check | `evidence/legacy_receipt_rollback_without_anchor.json` |
| forged `WriterCapability` passes the format check | `evidence/capability_format_not_authentication.json` |
| the same rollback **is** detected only by a separately trusted monotonic anchor | `evidence/rollback_detected_only_by_external_anchor.json` |

Conclusion carried in code and tests: a recomputable unkeyed digest detects
accidental corruption only; it cannot authenticate a writer and cannot prevent
rollback to an earlier valid journal without a separately trusted anchor.
`anti_rollback_check` refuses with typed `C8_TRUSTED_ANCHOR_UNISSUED` when no
anchor exists; capability trust verification raises
`C8_CAPABILITY_TRUST_ANCHOR_UNISSUED`. Security claim stays `NOT_PROVED`.

Concurrency / crash / custody (all real OS processes, real barrier, real signals):

- 2 / 3 / 5 genuinely simultaneous writers: no acknowledged committed event lost;
  durable identities == acknowledged identities; committed versions strictly
  monotone 1..n (`evidence/writer_race_{2,3,5}.json`, PIDs recorded).
- stale CAS typed `STALE_JOURNAL_CONFLICT`, lawful retry succeeds.
- acknowledged ledger prefix cannot be rewritten or reordered.
- real `SIGKILL` before rename: rc **-9**, prior state **byte-identical**, cold
  reopen at prior version; real `SIGKILL` after commit: rc **-9**, newest state
  durable (`evidence/crash_boundary_*.json`). `os._exit(79)` boundaries kept
  separately labelled as abrupt exits, not signals (OUT13's C7 label defect cured).
- cold reopen via a fresh interpreter process (`cold_reopen`) sees only committed
  state; killed writer leaves no ghost (`evidence/kill_after_writer_race.json`).
- replay/no-ghost: re-presentation of an already committed occurrence creates no
  duplicate or out-of-order occurrence; crafted duplicate/out-of-order occurrence
  states are refused; valid-empty/unpermitted commits preserve other writers'
  committed source byte-for-byte.
- durability limit recorded honestly: process-death recovery only;
  **not** power-loss durability, **not** `fdatasync`/`syncfs` media barriers,
  **not** exactly-once delivery (`evidence/durability_limit_receipt.json`).

## D. C8 committed receipt → actual downstream read-only consumer

`consumer/c8_readonly_consumer.py` binds the byte-exact committed journal receipt
to **one existing lawful C8 read-only recipient** — the accepted OUT9
`UserProjection` / `Outbox` viewer-client path (the only reader of committed
outbox/occurrence state in the accepted source) — and to **typed absence**
elsewhere:

- byte-exact canonical re-read, envelope + digest + prefix validation before any
  view is exposed; readset carries `state_digest`, `version_state_digest`,
  `ledger_prefix_digest`, `commit_receipt_id`, `writer_version`, `writer_id`,
  occurrence ids and the canonical-bytes digest;
- event/actor/action owner identity binding with typed `OWNER_IDENTITY_MISMATCH`;
- strictly read-only (journal bytes asserted unchanged under consumer operations);
- `ADP019_ADMISSION_RECEIPT_ABSENT` and `C9_LATER_ACTION_CONSUMER_UNBOUND` typed
  absences plus the exact `C8_COMMITTED_OCCURRENCE_RECEIPT` receiving-interface
  request for C9P; **no C9 native positive**, no manufactured actor, encounter or
  perception (`perceive`/`has_perceived` remain False in the accepted prototype).

Same-named source-severance witnesses (prospective `<test>.proof.json`, shared
CROSS_HQ gate `proof_integrity_gate_r1.py` staged byte-verified
`774d338cdbeea68ab09006807431cc8d17a22345`): **5/5 claims** baseline PASS and
same-named assertion RED under the exact source fault, grade
`BOUNDED_MUTATION_DETECTED` / `TARGET_ASSERTION_FAILED`
(`court/test_c8o_consumer_severance.py.proof.json`, `evidence/proof_witness_consumer.json`).

## E. Terminal integration evidence and C8→C9→C12 delta

One coherent runnable source-free candidate (`candidate/c8o_trusted_outbox.py`) +
consumer (`consumer/c8_readonly_consumer.py`) + full harness (`court/`, 62 cases,
`severance/`) with all inherited courts intact and executed.

C8→C9→C12 delta (honest, no native positive):

- **C8 now provides:** durable versioned occurrence custody with acknowledged
  prefix integrity, writer/capability separation (format-only), effective clock
  provenance, byte-exact committed readset receipts and an executed consumer
  binding — i.e. the authentic durable occurrence/source-custody substrate C9
  needs to read.
- **C8→C9 interface request (owner action):** bind `C8_COMMITTED_OCCURRENCE_RECEIPT`
  (five digests + occurrence identity + effective clock) into an ADP019 admission
  decision for the precipitating occurrence; then the C9P owner binds a named
  later-action consumer to that readset and issues distinct native C9 authority
  (`ADP019_ACTOR_EVENT_WITNESS_MISSING`, `LATER_ACTION_CONSUMER_UNBOUND` remain).
- **C9→C12:** unchanged and unclaimed; `C9_NATIVE_POSITIVE_HELD` stands; C12 lived
  reentry requires native person×event consequences this worker cannot issue.
- Cell-level state: multiwriter integrity and transport cells **executed**; trusted
  writer/anti-rollback cells **held** (`C8_TRUSTED_WRITE_OWNER_HELD`, `NOT_PROVED`).

## Return inventory

| Artifact | Path |
|---|---|
| complete candidate | `candidate/c8o_trusted_outbox.py` |
| read-only downstream consumer | `consumer/c8_readonly_consumer.py` |
| hostile court (62 cases) + worker + support | `court/` |
| severance runner + shared gate (byte-verified) | `severance/proof_integrity_gate_r1.py` |
| prospective proof contract + gate receipt | `court/test_c8o_consumer_severance.py.proof.json`, `evidence/proof_witness_consumer.json` |
| source/import ledger (33 rows, all blob-verified) | `evidence/source_import_ledger.json` |
| independent writer-race evidence (2/3/5, PIDs) | `evidence/writer_race_{2,3,5}.json` |
| old-writer bypass counterexample + enumeration | `evidence/legacy_writer_bypass_counterexample.json`, `evidence/write_entrypoint_enumeration.json` |
| rollback / digest-forgery / capability receipts | `evidence/{legacy_receipt_rollback_without_anchor,unkeyed_digest_forgery_counterexample,history_rewrite_counterexample,capability_format_not_authentication,rollback_detected_only_by_external_anchor}.json` |
| SIGKILL / cold-process receipts | `evidence/crash_boundary_*.json`, `evidence/durability_limit_receipt.json`, `evidence/kill_after_writer_race.json` |
| all JUnit incl. historical 2 REDs | `junit/` |
| owner decision docket | `docket/OWNER_DECISION_DOCKET.md` |
| sanitized environment passport | `environment_passport_delta.json` |
| remote verification receipt | `evidence/remote_verification.json` (second commit, after push) |

Prohibitions respected: no trusted-writer issuance, no native actor/event
admission, no production installation, no Pyat mutation, no ADP019/CAN issuance,
no semantic adoption, no V3 claim, no self-acceptance, no independent-I2 claim,
no historical RED suppression, zero model switches.
