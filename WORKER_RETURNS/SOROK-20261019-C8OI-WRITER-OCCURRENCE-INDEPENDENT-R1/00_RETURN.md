# SOROK C8OI — independent writer-security, occurrence-custody and receiving-consumer court R1

## Three-court verdict

| Court | Verdict | Scope |
|---|---|---|
| **Engineering** | `ACCEPT_SCOPED` | Complete C8O implementation executes as claimed: 270/2 inherited, OUT12 9/9, OUT13 23/23, OUT14 27/27, C8O 62/62, OUT13-under-OUT14 22/1 defect-oracle closed. Writer races, SIGKILL boundaries, cold reopen and no-ghost all confirmed. |
| **Scientific** | `ACCEPT_SCOPED` with precise limits | OS tests demonstrate process-death recovery, not power-loss durability. Unkeyed digests detect accidental corruption, not writer authentication. Format-only capability is not trust. Detection ≠ prevention. |
| **Authority** | `HOLD` | D1 (old-writer exclusivity), D2 (external anchor / keyed capability), D3 (ADP019 admitted occurrence + C9 E2 performer) all remain unissued. Reviewer cannot sign these. |

**Overall: `ACCEPT_SCOPED__ENGINEERING_AND_SCIENTIFIC__AUTHORITY_HELD__SECURITY_NOT_PROVED`.**

Repository: private `maidiu/rawlsing`. Branch `agent/reviewer-sorok-20261019-c8oi-writer-authority-and-occurrence-independent-r1` at sealed startup `f68512d05a0d10c7711ca7149f2e12bf891eb6de`. Exact review target: C8O author `9784bc1dbae0c9ac13670d5e442ed9cabb6be7fe`. Writes only to `WORKER_RETURNS/SOROK-20261019-C8OI-WRITER-OCCURRENCE-INDEPENDENT-R1/`.

## 1. Inherited suite reproduction

| Suite | Expected | Independently reproduced | JUnit |
|---|---|---|---|
| Original 272 (OUT9-era union) | 270 PASS / 2 historical RED | **270 PASS / 2 historical RED** | `evidence/ind_original_272.xml` |
| OUT12 author | 9/9 | **9/9** | `evidence/ind_out12_9.xml` |
| OUT13 frozen hostile | 23/23 | **23/23** | `evidence/ind_out13_23.xml` |
| OUT14 new court | 27/27 | **27/27** | `evidence/ind_out14_27.xml` |
| C8O author court | 62/62 | **62/62** | `junit/c8o_new_court.xml` |
| OUT13 under OUT14 repair | 22 PASS / 1 defect-oracle RED | **22 PASS / 1 RED** | `evidence/ind_out13_under_out14.xml` |

Both historical REDs preserved unmodified:
- `test_rto_hostile.py::test_replay_manual_two_writers_can_lose_first_committed_event`
- `test_sr_28_falsifier_court.py::test_s27_material_move_needs_world_owner`

The OUT13 HP8 divergence (`test_hp8_corrupting_writer_version_resets_to_zero_and_defeats_the_CAS`) is `HP8_DEFECT_ORACLE_CLOSED_BY_OUT14_REPAIR`, not a safety regression.

## 2. Independent adversarial court (17 tests)

### Engineering findings

| Test | Finding |
|---|---|
| `test_legacy_journal_commit_destroys_acknowledged_events` | Old `Journal.commit` remains legally callable and replaces entire journal, destroying acknowledged events |
| `test_legacy_writer_bypass_after_green_wrapper` | Old writer erases state after wrapper commit; only detected after the fact (`LEGACY_UNVERSIONED_OVERWRITE`) |
| `test_two_real_writer_pids_no_acknowledged_loss` | Two cooperating writers produce no acknowledged event loss |
| `test_stale_cas_typed_conflict` | Stale CAS produces typed `StaleJournalConflict` |
| `test_sigkill_before_rename_preserves_prior_state` | SIGKILL rc=-9 before rename preserves prior state byte-identical |
| `test_cold_reopen_sees_only_committed_state` | Cold reopen in fresh process sees only committed state |
| `test_process_death_is_not_power_loss_durability` | SIGKILL after commit preserves new state — process-death only |

### Scientific findings

| Test | Finding |
|---|---|
| `test_unkeyed_digest_forgery_is_accepted` | Full unkeyed forgery (recomputed `state_digest`, `version_state_digest`, `ledger_prefix_digest`, `commit_receipt_id`) passes every check — `VERSIONED_VALID`. **Recomputable unkeyed digests are not writer authentication.** |
| `test_format_only_capability_passes_check` | Format-only `WriterCapability` produces a fingerprint — not authentication |
| `test_rollback_to_byte_valid_earlier_version_passes` | Rollback to byte-valid earlier version passes all unkeyed checks |
| `test_anti_rollback_refuses_without_anchor` | `anti_rollback_check` refuses with typed `C8_TRUSTED_ANCHOR_UNISSUED` |

### Authority findings

| Test | Finding |
|---|---|
| `test_d1_legacy_writer_remains_callable` | `Journal.commit` and `Journal.admit_and_queue` remain legally callable |
| `test_d2_capability_trust_anchor_unissued` | `verify_trust` raises typed `C8_CAPABILITY_TRUST_ANCHOR_UNISSUED` |
| `test_d3_adp019_admission_absent` | ADP019 admission receipt is typed absent, not fabricated |

### Consumer findings

| Test | Finding |
|---|---|
| `test_committed_receipt_reaches_consumer_with_readset` | Committed receipt reaches `C8ReadOnlyConsumer` with full readset (state_digest, version_state_digest, ledger_prefix_digest, writer_version, commit_receipt_id) |
| `test_consumer_is_strictly_read_only` | Consumer never mutates journal bytes |
| `test_no_perception_becomes_occurrence` | No perception becomes occurrence |

## 3. Security interpretation

**What the C8O implementation actually proves:**
- Durable versioned occurrence custody with acknowledged prefix integrity
- Process-crash recovery via atomic rename (SIGKILL before/after rename)
- CAS-based conflict detection between cooperating writers
- Typed refusals for stale, ghost, prefix-rewrite and capability-missing cases
- Byte-exact read-only consumer binding to committed state

**What remains insecure:**
- The old `Journal.commit` is a legally callable writer that destroys acknowledged events unnoticed by the security envelope. This is a **bypass**, not a defect: no accepted owner restricts it.
- Unkeyed digests (`state_digest`, `version_state_digest`, `ledger_prefix_digest`) are recomputable. An attacker who knows the hash function can forge any receipt. This is **corruption detection**, not **writer authentication**.
- `WriterCapability` fingerprint is an unkeyed hash. Format check ≠ trust.
- Rollback to any byte-valid earlier version passes all checks. Detection requires a separately trusted monotonic anchor.
- SIGKILL evidence demonstrates process-death recovery only. Power-loss durability (fdatasync/syncfs media barriers) is **not tested**. Exactly-once delivery is **not claimed**.

**Detection vs prevention:** the C8O wrapper detects legacy bypass after it occurs (`LegacyWriterBypassDetected`). It cannot prevent already-erased state and cannot withdraw the old writer's permission. A legal callable bypass is never a secure wrapper even if detected after damage.

## 4. Source-consumer severance (3 claims)

| Claim | Fault | Result |
|---|---|---|
| `C8OI_CONSUMER_READSET_BINDS_COMMITTED_RECEIPT` | `state_digest` → `"SEVERED"` | `TARGET_ASSERTION_FAILED` |
| `C8OI_CONSUMER_READSET_BINDS_VERSION_STATE_DIGEST` | `version_state_digest` → `"SEVERED"` | `TARGET_ASSERTION_FAILED` |
| `C8OI_CONSUMER_READSET_BINDS_LEDGER_PREFIX_DIGEST` | `ledger_prefix_digest` → `"SEVERED"` | `TARGET_ASSERTION_FAILED` |

Receipt: `evidence/proof_witness_receipt.json`. All `BOUNDED_MUTATION_DETECTED`.

## 5. D1–D3 owner decision packet

| Docket | Decision needed | Competent owner | Status |
|---|---|---|---|
| **D1** | Deprecate/gate/migrate old `Journal.commit` and `admit_and_queue`; establish writer exclusivity | Accepted writer custodian | **UNISSUED** |
| **D2** | Independently trusted capability/key custody and monotonic external anchor | Key/anchor custodian | **UNISSUED** |
| **D3** | ADP019 admitted occurrence receipt and independent C9 E2 performer | ADP019/C9 actor owners | **UNISSUED** |

A reviewer cannot sign any of these. Owner refusal blocks trusted-security claims but not already executed narrower material integration.

## 6. C8→C9→C12 terminal delta

C8 now provides: durable versioned occurrence custody, acknowledged prefix integrity, writer/capability separation (format-only), effective clock provenance, byte-exact committed readset receipts and an executed read-only consumer binding.

C8→C9 interface request: bind `C8_COMMITTED_OCCURRENCE_RECEIPT` into an ADP019 admission decision. C9 native positive remains held.

C9→C12: unchanged and unclaimed.

## 7. Proposed HQ ACTION

1. **D1:** Commission accepted writer custodian to deprecate/gate old `Journal.commit`/`admit_and_queue` or establish exclusive writer ownership.
2. **D2:** Commission independent key/anchor custodian to issue a monotonic external anchor and keyed capability issuer.
3. **D3:** Commission ADP019 admission court and C9 E2 performer for actual occurrence admission and later-action binding.

## 8. Environment

Model: DeepSeek V4.1-Flash MAX via OpenCode. Local Git object store, CPython 3.11.3, pytest 9.1.1. Cash/quota: UNKNOWN. No model switch, no delegation.

**Final:** `ACCEPT_SCOPED__ENGINEERING_AND_SCIENTIFIC__AUTHORITY_HELD__SECURITY_NOT_PROVED__D1_D2_D3_UNISSUED`.
