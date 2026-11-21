# PYAT991 — narrow owner handoff acknowledgement

## Identity and status

- Existing S1-D owner A: `ses_e3120ba7affeNBHUoX1HIP3G4r`
- Handoff branch: `agent/pyat991-owner-handoff-r1`
- Base / qualified saved implementation: `eccc0ad4980261bdf7e77d4e18569f334089d7df`
- Qualified implementation code: `5478210b7aeedf608a3e9754bf891d4d0262817f`
- Prior machine disposition: `dec3e0290ce1c98e23de7e51761592a68c9a64b9:WORKER_COMMISSIONS/PYAT_SUCCESSOR_960/S2D_G5_FINAL_DISPOSITION.json`
- Status: **ACK** for the two narrow shared-file entries.
- No code, test, product, source, prior return, controller or other worktree was written.

## Parent/user grant vs A's actual ownership

The user/HQ960 direction of 2026-11-13 is the functional allocation for the two shared files. It retains the original #919 S2-D allocation and the prior disposition's named competent owners. It is **not** a new HQ, owner, packet or architecture campaign.

- **Batch:** A is **not** the historical R16 Batch author. `pre553_batch_runner.py` has been unchanged since `eb89fb48c6cfa5855b559ffb9bc5536c6d8b5974`; no distinct live Batch-author session is evidenced. The acknowledgement is the requested inherited native Batch/issuer-composition maintainer acknowledgement within the existing S1-D owner lane, under the parent user/HQ960 functional grant and original #919 S2-D allocation. It does not fabricate a personal Batch authorship or a new owner.
- **Issued workload:** A is the existing S1-D implementation owner. The original pair terminal implementation is `dfdbddad946f9a82cb3008148cb9669f8632ba4`; A's S1-D code ancestry includes `06c1213149e4649c62dcb6133669dec90cd4d29f`. The parent user/HQ960 direction and original #919 S2-D allocation authorize the saved-admission extension.

## Entry 1 — Batch saved admission

**File:** `rawlsing_next/pre553_batch_runner.py`  
**Current blob:** `2d291600b9a10c56d9c6f6de7f7d619f6c52e829`  
**Exact function:** `BatchExecutionRunner.__init__` and only the directly indispensable exact saved-identity release resolution used there.

**Permitted:** narrowly accept an exact independently certified `SavedC11Admission` (existing `pre553_saved_c11_admission.py`) and its identity-only `SavedReleaseIdentity` in `BatchExecutionRunner.__init__`, then use the actual native Batch engine. No source/query/discovery selector or cache hit becomes authority.

**Required invariants:** existing deterministic manifest/schedule/unit/receipt/state/`record_receipt`/summary/failure behavior unchanged; existing genuine `C11Repository` path unchanged; no fake `C11Repository`, fabricated seal or full C11 graph; wrong/unknown/mismatched release refuses before scheduling or positive receipt; no science math, Batch rewrite or test weakening. New tests only `test_pyat991_s2d_*`.

**Receiving workers:** S2-D A `ses_e3120ba1cffeO1w43uU5MLh4yq`, B `ses_e3120b9efffegreD5YfH7dOO15`, serial on `agent/pyat991-s2d-a-r1`. Lease valid through implementation and frozen terminal independent G5 by `ses_e30c25800ffeT8XbyTuHekRCme`; parent HQ controls serial turns and no other owner writes. No production/science/source/CURRENT/protected effect.

## Entry 2 — Issued workload saved path

**File:** `rawlsing_next/pre553_issued_workload.py`  
**Current blob:** `47db61752d08fa5c774436b2c29e489a8d91c3f2`  
**Exact symbols:** `execute_issued_workload`, `resume_joined_workloads`, `JoinedWorkloadCheckpoint`, `capture_joined_checkpoint`, and only directly indispensable optional saved-admission/current integration helpers.

**Permitted:** add a lawful optional saved-admission path that skips original source/full C11 build; bind checkpoint exact manifest/direct I02/reconstructed release; preserve normal and COMPLETED/PARTIAL/ABSENT receipts, prefixes, outputs and live current checks.

**Required invariants:** existing `CurrentDecisionResolver` API, issuer competence, host/purpose, envelope/source SHA/expected jobs/as-of, revocation/expiry semantics unchanged; fresh admission before source/cache/restore/serve; no fallback to historical `item.record`; legacy path remains supported; no stale permission/fake seal; exact partial retry/cold recovery conservation; no new issuer, science, fates or authority promotion; existing tests read/run only, new `test_pyat991_s2d_*` only.

**Receiving workers / lease:** same serial S2-D A/B and G5 as above.

## Signatures inspected at this cut

- `BatchExecutionRunner.__init__(*, manifest: BatchManifest, repository: C11Repository, prior_receipts: Iterable[UnitExecutionReceipt] = ())`; current guard calls `repository.resolve_release_exact(release_ref)`.
- `SavedC11Admission.resolve_release_exact(ref: ExactRef) -> SavedReleaseIdentity`; `SavedReleaseIdentity(release_ref: ExactRef)` is identity-only, not a `C11LogicalRelease`.
- `execute_issued_workload(workload, resolver, *, source_factory, host, purpose, allow_test_only=False, prior_receipts=(), prior_outputs=None, max_units=None, expected_wave=None, group_scope=None)`.
- `resume_joined_workloads(*, workloads, resolver, source_factory, host, purpose, checkpoint, expected_checkpoint_ref=None, allow_test_only=False)`.
- `JoinedWorkloadCheckpoint(schema, entries, checkpoint_hash)`; `capture_joined_checkpoint(results, *, source_sha256_by_decision=None)`.
- `restore_joined_checkpoint(...)` and `admit(...)` are directly related current/custody helpers; any touch must stay within optional saved/current integration and the same no-loss invariants.

## Boundaries

No new preflight, S2-C rewrite, architecture campaign, worker/model/provider/harness change, autowake/polling or owner discovery. No production CURRENT, original35/source/science, N11/N12, protected merge, W03/W04/Q3 work. The lease is a narrow file-owner acknowledgement that enables the exact next S2-D product code and five remaining native paths; it is not product acceptance or G5.

**Ack file:** `owner_ack.json` in this directory.
