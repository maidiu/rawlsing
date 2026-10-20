# SOROK BP3 — real C8 exclusive writer and external monotonic anchor

## Identity / custody

- Repository: private `maidiu/rawlsing`.
- Branch: `agent/rabochii-sorok-20261020-bp3-c8-exclusive-writer-external-anchor-r1`.
- Sealed startup used: **`529232d9867a5bdc0889f43fb5293131ef806055`** — the latest physical HQ commit containing the BP3 commission (`8ee55a7d3`), four-return adjudication (`4e1a209ef`) and C9RI acceptance (`529232d98`). The launch did not carry a literal startup SHA; I did not use a floating branch. C8O `9784bc1…`, C8OI `f4200eb…`.
- Role: sourcefree C8 writer/anchor implementation. NOT C8O/C8OI author, HQ, ADP019 issuer, key/anchor custodian, C9RI worker or production installer.
- Write scope: only `WORKER_RETURNS/SOROK-20261020-BP3-C8-WRITER-TRUST-R1/**`. No accepted Journal, C8O/C8OI, C9R/C9RI, Pyat, PRE-MAIN, CAN/ADP, production or original grant was edited.
- Sourcefree/test-only. No native key, anchor, ADP019, actor, E2, C11 or production security claim.

## FINDING

The accepted OUT9 `outbox_prototype.Journal.commit`/`admit_and_queue` are still the old callable writer. The BP3 candidate installs an executable compatibility gate over those **exact class methods** at import, and adds a keyed compare-and-append journal whose proof is bound to an independently held monotonic witness. With the candidate loaded and the key/anchor external, the old class writer and forged/rolled-back state are refused; the accepted read-only consumer and a sourcefree C9 ingress consume the actual committed state.

Exact receipts:

| Check | Result |
|---|---:|
| BP3 writer/anchor/consumer/OS court | **18 PASS / 0 RED** |
| BP3 five same-assertion proof claims | **5/5 BOUNDED_MUTATION_DETECTED** |
| Cold seeds 0/1 | **18 PASS each** |
| C8O historical original 272 | **270 PASS / 2 preserved RED** |
| OUT12 author 9 | **9 PASS / 0 RED** |
| OUT13 hostile 23 | **23 PASS / 0 RED** |
| OUT14 new 27 | **27 PASS / 0 RED** |
| C8O 62 independent rerun | **62 PASS / 0 RED** |
| C8OI independent 17 rerun | **17 PASS / 0 RED** |
| OUT13 under OUT14 regression | **22 PASS / 1 inherited RED** (`test_hp8_corrupting_writer_version_resets_to_zero_and_defeats_the_CAS`) |

The two original 272 REDs remain exactly:
`test_replay_manual_two_writers_can_lose_first_committed_event`,
`test_s27_material_move_needs_world_owner`.
No frozen test was changed. The OUT13-under-OUT14 regression is inherited and preserved, not fabricated as a BP3 success.

## What is actually implemented

### A. Old writer gate (compatibility, not native cutover)

`c8_exclusive_writer.py:install_exclusive_gate()` replaces:

- `outbox_prototype.Journal.commit`
- `outbox_prototype.Journal.admit_and_queue`

with `LegacyWriterRouteClosed`. This is an executable gate in any process that imports the candidate. The accepted module bytes remain untouched; a process that never imports the gate can still call the old class method. That is **D1**, not a native retirement claim. The test `test_old_journal_commit_route_closed_preserves_acknowledged_bytes` shows an attempted old commit leaves the acknowledged bytes and occurrence count unchanged.

### B. Single new write path

`c8_exclusive_writer.ExclusiveJournal` subclasses the C8O `C8OccurrenceJournal` (version CAS, lock, acknowledged-prefix custody) and adds:

- `KeyedCapability` HMAC-SHA256 test capability bound to exact journal ID, `EXCLUSIVE_APPEND` role, writer, nonce and expiry;
- `KeyedMonotonicAnchor` in a directory outside the journal, with keyed row and separately held watermark;
- `ExclusiveJournal.commit` proof over journal ID, capability nonce, writer/version, receipt/state/version-state digests and anchor sequence/row;
- `verify_journal` proof/anchor verification;
- `append_occurrence` with duplicate no-op, stale-version retry support and no old writer fallback;
- `c9_event_ingress.receive_event`, which requires a proof verifier and reads the actual committed state digest.

### C. Crypto and anchor receipts

- Test key: **TEST_ONLY** HMAC-SHA256 key in a separate key file, loaded via `WriterKeyStore`; key inside the journal directory is refused `KeyCustodyNotExternal`.
- No public hash, unkeyed digest or bearer token is called a signature.
- Anchor: keyed monotonic rows + separately held watermark outside the journal. Offline anchor, invalid MAC, rotated key and older byte-valid journal + proof are refused (`AnchorUnavailable` / `AnchorRollbackDetected`).
- Key-leak test is intentionally honest: an attacker with the test key can mint a valid capability/proof; the security boundary is the external key custodian (D2), not an in-code secret.

### D. Actual OUT9 read-only consumer and C9 ingress

- The accepted C8O `C8ReadOnlyConsumer` reads the BP3-committed C8O-compatible journal. Positive: one occurrence, actual readset state digest/version.
- `c9_event_ingress.receive_event` consumes that actual receipt only when given `journal.verify_journal` as a proof verifier. It returns `ADP019_ADMISSION_RECEIPT_ABSENT`, `e2_performed=False`, `native_actor_admitted=False`, `route_probability=None`, `selection_weight=None`.
- C9 ingress with a severed expected digest refuses. Full C9/ADP019 native admission and performed E2 remain unissued.

## Multiwriter, crash, rollback and no-effect

- 2/3/5 real subprocess writers: no acknowledged occurrence loss; version equals writer count; cold reopen sees the committed state.
- Stale writer: C8O/C8O `StaleJournalConflict`; no silent overwrite.
- Old writer: `LegacyWriterRouteClosed`; acknowledged bytes preserved.
- Byte-valid rollback with old proof: `AnchorRollbackDetected`.
- Anchor offline: `AnchorUnavailable`; rotated anchor key: `AnchorUnavailable`.
- Forged capability: `CapabilityRefused`.
- Unkeyed receipt rewrite: `KeyedProofInvalid`; the OUT9-style unkeyed read is not treated as keyed authentication.
- Crash before rename: prior bytes preserved; crash after commit: journal is visible but proof sidecar is stale and `verify_journal` refuses — an **unacknowledged crash state** requiring repair, not a successful ack.
- Duplicate occurrence: `DUPLICATE_NO_CHANGE`, no second append/version.
- Raw filesystem overwrite is not prevented: this is OS/D1, not the class API. It is covered in the threat model, not claimed as a security success.

## Threat model / residual limits

**Closed in the candidate process:** old `Journal.commit`/`admit_and_queue`; caller Boolean owner; forged capability; unkeyed digest/token accepted as auth; byte-valid rollback unless the separately held witness is also rolled back; offline/rotated anchor; duplicate append; stale writer; ordinary 2/3/5 writer races.

**Residual, typed:**

1. **D1 (cutover/OS):** a process that does not import the candidate, direct filesystem writes, OS-privileged deletion and file-permission bypass are not closed; native original API retirement requires accepted owner action.
2. **D2 (key/anchor custody):** test key is not production KMS/HSM; a leaked writer key can forge valid proof; anchor log + watermark rolled back together defeat detection; anchor availability/rotation/revocation is an external custodian service.
3. **D3 (native event):** no ADP019 admission, actual actor occurrence, later performed E2 or native C9 binding; C9 ingress is test-only.
4. **Crash after journal rename before proof sidecar:** state visible to a raw OUT9 reader but unacknowledged; `verify_journal` refuses. Reconciliation/repair is not issued.
5. **Durability:** `fsync`/rename evidence is not a power-failure guarantee on exotic filesystems; no production FS assumption is made.
6. **Source semantics:** C8 occurrence custody is not actor psychology, historical development or performed E2.

## Owner handback

`OWNER_HANDBACK_D1_D2_D3.md` gives exact decisions, owners, code paths and evidence for D1, D2 and D3.

## Three courts

**ENGINEERING — `ACCEPT_SCOPED_SOURCEFREE_C8_WRITER_CANDIDATE`.** The old callable class writer is refused in the gated process; the new path is keyed, CAS, anchored, crash/multiwriter tested, and the actual OUT9/C9 sourcefree positives run. Scope excludes D1 native cutover, raw OS bypass, production key custody and native ADP019/E2. The crash-after-proof gap and D1/D2 are typed, not hidden.

**SCIENTIFIC — `ACCEPT_SCOPED_CUSTODY_DISTINCTION__HOLD_NATIVE_ADP019_E2`.** The candidate demonstrates source/event custody and consumer binding, not an actual actor occurrence, historically developed person, ADP019 admission or performed E2. No fixture-native claim.

**AUTHORITY — `HOLD`.** D1 accepted original writer cutover, D2 independent key/anchor authority and D3 ADP019 external source/E2 remain with their owners. No native credentials, production trust, CAN/ADP/C11/Pyat authority or self-adoption.

## Exact source blobs and artifacts

- Accepted old writer: `outbox_prototype.py` blob `331840768ce0b5f6f73e5e93094ca0d217ddaebf`.
- C8O trusted wrapper: `c8o_trusted_outbox.py` blob `7d785d35be09ab2ca5877a89a7880c70f2fe488c`.
- C8O read-only consumer: `c8_readonly_consumer.py` blob `5ae9360963a98d7a715ea94ef8883e35d5f3442d`.
- BP3 source/custody: `evidence/source_provenance.json`; tests/JUnit: `evidence/bp3_native.xml`, `evidence/bp3_post_witness.xml`, `evidence/bp3_cold_0.xml`, `evidence/bp3_cold_1.xml`; proof: `evidence/proof_witness_receipt.json`; historical: `evidence/c8o_historical_status.json`, `evidence/original_272.xml`, `evidence/out12_author_9.xml`, `evidence/out13_hostile_23.xml`, `evidence/out14_new_court.xml`, `evidence/c8o_62.xml`, `evidence/c8oi_17.xml`.

## Not run / limits

Native ADP019 admission, genuine actor occurrence/performed E2, C9R native binding, C11 physical weld, Pyat N11/N12, production key/anchor installation, OS power-failure proof, raw respondent/source access, and any real original Journal API modification are **NOT_RUN / HOLD**. No self-issued authority.

## Exact pushed ref

The final ordinary non-force HEAD and `git ls-remote` proof are bound in `PUBLICATION_RECEIPT.json` and the final response. No force push, no branch reset, no outside-return mutation.
