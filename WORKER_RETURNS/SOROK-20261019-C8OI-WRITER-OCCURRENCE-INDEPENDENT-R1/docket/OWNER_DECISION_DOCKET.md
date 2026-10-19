# SOROK C8O — competent-owner decision docket R1

**Return:** `WORKER_RETURNS/SOROK-20261019-C8O-OUT14-WRITER-AUTHORITY-EXECUTABLE-BOUNDARY-R1`
**Worker role:** bounded source-free C8 occurrence/event journal and trusted-writer
integration candidate author / owner-custody investigator. **This worker issues
nothing.** No trusted-writer grant, no ADP019 admission, no native actor/event
admission, no production installation, no permission to any writer is created by
this docket. Every item below is a request to a named competent owner.

---

## D1 — Old-writer exclusivity (close the accepted `Journal.commit` bypass)

**Typed residual:** `LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED`
**Security claim:** `NOT_PROVED`

**Fact (executed, not argued).** The accepted OUT9 `outbox_prototype.Journal`
(`331840768ce0b5f6f73e5e93094ca0d217ddaebf`) exposes
`commit(self, p, crash_boundary=None)` and `admit_and_queue(...)`. Neither takes a
lock, a version precondition or a writer capability. A real separate OS process
calling that accepted API replaced a journal holding three acknowledged
occurrences (before/after bytes, PIDs and destroyed occurrence ids recorded in
`evidence/legacy_writer_bypass_counterexample.json`). The wrapper only detects the
bypass afterwards (`LEGACY_WRITER_BYPASS_DETECTED`, `evidence/write_entrypoint_enumeration.json`).
An interleaved stale accepted commit also loses a cooperative event
(`evidence/interleaved_legacy_lost_event.json`), and the wrapper's own green
receipts do not bind that writer (`evidence/green_wrapper_then_bypass_erasure.json`).

**Who has jurisdiction.** The owner of the accepted `outbox_prototype` public
write interface (the OUT9 accepted source custodian), acting with the Sorok
product owner who governs C8 occurrence custody. Not this worker, not OUT12,
OUT13, OUT14 and not any wrapper author.

**Exact owner action required (one of):**
1. Deprecate/deny `Journal.commit` and `Journal.admit_and_queue` as writers of
   the C8 journal path (raise a typed `LEGACY_WRITER_DISABLED` at those entrypoints
   when a versioned envelope is present), **or**
2. install a capability-checked writer gate in front of every write entrypoint
   (accepted + wrapper + direct file replacement), **or**
3. grant exclusive writer status to `C8OccurrenceJournal.commit` in an owner
   document binding every authorized writer, and record the installation scope.

**Changed callable API / permission / installation implied:** at minimum a source
change in the accepted module or an owner-managed install-time writer gate; plus a
written grant enumerating authorized writers. **Existing grants found in source:
none.** No accepted source, HQ motion or ADP019 document examined here restricts
the old writer; ADP019 governs *event admission*, not journal file writers.

**If granted:** the candidate may then claim wrapper exclusivity at the granted
scope and the bypass court becomes a refusal court. **If not issued:**
`LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED` stands and no multiwriter security
acceptance may be claimed.

---

## D2 — Trusted anti-rollback anchor and keyed writer authenticity

**Typed residual:** `C8_TRUSTED_ANCHOR_UNISSUED`, `C8_CAPABILITY_TRUST_ANCHOR_UNISSUED`
**Security claim:** `NOT_PROVED`

**Fact (executed, not argued).** Every digest in the candidate envelope
(`state_digest`, `version_state_digest`, `ledger_prefix_digest`,
`capability_fingerprint`, `commit_receipt_id`) is an **unkeyed** recomputable
hash. Executed counterexamples:
- recompute-over-forged-version: accepted reader returns the forged version
  (`evidence/unkeyed_digest_forgery_counterexample.json`);
- full history rewrite with every digest recomputed is accepted
  (`evidence/history_rewrite_counterexample.json`);
- rollback to an earlier byte-valid receipt is accepted by every unkeyed check
  (`evidence/legacy_receipt_rollback_without_anchor.json`);
- a forged `WriterCapability` passes the format check
  (`evidence/capability_format_not_authentication.json`).

Rollback **is** detectable when a separately trusted monotonic anchor observes
each version (`evidence/rollback_detected_only_by_external_anchor.json`), but the
shipped `FileBackedMonotonicAnchor` is `TEST_FIXTURE_ONLY_LOCAL_ANCHOR_NOT_OWNER_ISSUED`.

**Who has jurisdiction.** A competent owner able to custody a secret key and/or a
monotonic counter outside every journal writer (an issuer distinct from the
writer). Capability issuance is explicitly out of role for this worker.

**Exact owner action required:**
1. issue a keyed writer capability/verifier (HMAC or signature over
   `writer_id|writer_version|receipt_id`) and bind it into the commit path, **and/or**
2. custody an external monotonic version anchor (hardware/owner service/append-only
   owner log) outside the journal directory, and bind `observe/check` into commit
   and read.

**If granted:** anti-rollback and writer authenticity may be re-tested and graded;
until then every digest-based authenticity reading is falsified by the court above.

---

## D3 — ADP019 occurrence-admission interface (C8 receipt → admitted event)

**Typed residual:** `ADP019_ADMISSION_RECEIPT_ABSENT`
**Native positive:** none. `C9_NATIVE_POSITIVE_HELD` unchanged.

**Fact.** The committed C8 receipt now carries an exact byte-verifiable readset
(state, version-state, ledger-prefix digests, commit receipt id, writer id,
effective clock) and per-occurrence identity
(candidate/issuer/authority/participant/source refs, admission grade). The
consumer exposes it read-only (`consumer/c8_readonly_consumer.py`) and returns a
typed absence for any ADP019 admission receipt.

**Who has jurisdiction.** The V3 External Admission Court (ADP019) / owner of
`V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE@1.0.0`. This worker may not issue,
simulate or pre-sign a `V3_EXTERNAL_ADMISSION_RECEIPT`.

**Exact owner action required:**
1. admit (or reject) the exact precipitating occurrence proposed from this C8
   receipt and emit the owner receipt (`receipt_id = v3admrcpt:<JCS SHA256>`) with
   the effective clock and event-ledger cursor update, **then**
2. bind the C8 readset (`commit_receipt_id`, `state_digest`,
   `ledger_prefix_digest`, occurrence identity) into that admission decision, **then**
3. the C9P owner binds a named later-action consumer
   (`LATER_ACTION_CONSUMER_UNBOUND` today) to the same readset and issues distinct
   native C9 authority for person×event consequences.

**Interface request (exact fields C9P would receive from C8):** see
`C8ReadOnlyConsumer.c9_later_action_receiving_interface_request()` —
`C8_COMMITTED_OCCURRENCE_RECEIPT` with the five digests, occurrence identity,
ADP019 receipt and owner identity binding.

---

## Docket state

| Item | Typed residual | Owner | Issued? |
|---|---|---|---|
| D1 old-writer exclusivity | `LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED` | accepted `Journal` write-interface custodian + Sorok C8 owner | **NO** |
| D2 trusted anchor / keyed capability | `C8_TRUSTED_ANCHOR_UNISSUED`, `C8_CAPABILITY_TRUST_ANCHOR_UNISSUED` | secret-custody issuer outside the writer | **NO** |
| D3 ADP019 admission + C9 binding | `ADP019_ADMISSION_RECEIPT_ABSENT`, `C9_LATER_ACTION_CONSUMER_UNBOUND` | V3 External Admission Court (ADP019); C9P owner | **NO** |

Terminal: `C8_TRUSTED_WRITE_OWNER_HELD__SECURITY_NOT_PROVED__LEGACY_WRITER_AUTHORIZATION_BYPASS_UNCLOSED__NO_SELF_GRANT`
