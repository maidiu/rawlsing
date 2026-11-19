# SRC04 witness b3dd74d16 — hostile exact-lineage integration repair

**Parent:** b3dd74d16c71f9f63b10510af041ec83a1b5c3de.
**Authority:** Source-static same-branch author repair only; no new source launch, science, owner, protected CAS, test PASS or independent G5.

## Five independently visible source defects

- Direct producer bypassed supervisor --authorized-source-launch.
- Checkpoint HMAC/spool was under root/private, but resume passed root and supervisor always created a fresh unrelated run root.
- Reader could calculate historic SRC04 count and reconstructed release-hash mismatch and still produce READER_OPENED/COMPLETE.
- Reader CURRENT callback omitted decision identity, revocation, source SHA and extended source-format/custody-locator scope; strict producer verification was not shared.
- Preflight could record request_equal_to_approved=false while exiting success (and accidentally used a default grant directory).

## Repaired boundary

Caller now requires launch flag even on direct producer, reuses the original private checkpoint and root for resumption (with symlink and mode protections), rechecks CURRENT after writer creation, refuses SRC04 exact-reference mismatch at reader, and distinguishes replay-from-checkpoint from source decode in the current process. The reader callback and checkpoint verifier now validate the same source-format, locator and decision-scope fields. Metadata preflight refuses a mismatching grant request.

The pinned core writer/source C11 product and existing q217 hold/177 response+3 coordinate scope remain intact. Historical b3dd RETURN.json and old green sourcefree rehearsal evidence are not altered. New author-only test_witness_integration_guards.py exists but **has NOT been executed**, nor has a real resume/source read/reviewer G5. A specific new physical release differing legitimately from the historic SRC04 reference must return a typed HELD/nonparity, never be declared historical-equivalent by suppressing the mismatch. Nothing here grants an original35 scientific or actor product.

**Next executable:** on an authorized local sourcefree checkout, run the new test plus caller checkpoint interruption→supervisor resume with exact original work root and wrong-root/denied-current negatives. Independent reviewer must validate that same cut before any SRC04 original-source run; external source owner and host/lease permission are separately required. No parallel plan or physics redesign.

`ANVIL_SRC04_HOSTILE_AUTHOR_REPAIR_CANDIDATE__NEW_TESTS_NOT_RUN__SOURCE_NATIVE_NOT_LAUNCHED__INDEPENDENT_REVIEW_PENDING__PROTECTED_HOLD`

## Second hostile review: supervisor liveness + historical grade

A source progress stream could fill the unread Popen PIPEs and hang the
supervisor indefinitely. Producer also truncated the log paths, and the
reference helper silently omitted an absent event/coordinate family.
The repaired caller uses file-backed logs and a kill/reap-on-monitor-error
helper; exact SRC04 parity requires both expected family counts and the
reference release. Unit tests exercise over-pipe-capacity child output,
monitor failure reaping and missing-count refusals. A new offline runner
pins exact HEAD and all witness manifest file digests before tests.
The prior manifest's ambiguous source_read_performed=true referred to
sourcefree fixture activity; explicit original SRC04 access remains FALSE.

These are **author source modifications only**. No new test execution,
true same-supervisor checkpoint resume, native SRC04 source read,
independent G5 or protected receiving occurred.
