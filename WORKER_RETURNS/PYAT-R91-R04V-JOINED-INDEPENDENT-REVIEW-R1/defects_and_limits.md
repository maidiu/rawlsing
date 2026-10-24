# R91-R04V joined custody remaining failures — REVISE

Verdict: **REVISE**. The author's unary complete-workload sequence resumes
without rerun at that narrow grain, and the R03 suite remains green. It is not
a real joined partial governed-native-frontier resume: actual R03 governed
discovery results are not consumable, the checkpoint is self-hashed without the
R61AV external original pin, and completed resume loses native outputs/facts and
the original manifest.

## Prioritized remaining failures

### 1. Actual R03 governed-issued result cannot be consumed (blocking)

**Observed:** `capture_joined_checkpoint` accepts only `NativeWorkloadResult`.
The accepted R03 governed path
`compile_governed_frontier -> execute_test_only_discovery_workload` returns a
`NativeDiscoveryExecution` (actual governed I05/Batch discovery result). Passing
that real R03-issued object raises
`WorkloadAdmissionError("EXACT_NATIVE_WORKLOAD_RESULT_REQUIRED")`.

The author's tests use the unary `compile_universal_workload` path, whose issued
workloads are single-query `NativeWorkloadResult`s. The declared limitation
(workload granularity, fully completed results, unary fixtures, no automatic
governed-discovery caller wiring) is therefore not a real joined partial native
frontier resume under the grant.

**Required:** consume the actual R03 governed-issued discovery object through
the authorized joining interface, retaining its authority/grammar/frontier,
manifest/unit, receipts, native result/outputs and facts. If an additional R03
caller/adapter path is truly indispensable, return that exact path and
invocation dependency; do not claim automatic wiring without implementing it.

### 2. Checkpoint is self-hashed; no separately provisioned original pin (blocking)

**Observed:** `JoinedWorkloadCheckpoint.checkpoint_hash` is a self-hash of the
candidate-controlled material. `restore_joined_checkpoint` verifies only that
self-hash and entry hashes, and `resume_joined_workloads` verifies checkpoint
self-hash plus workload envelope/source/decision. Rewriting an entry's
`receipt_materials`/`output_refs` and recomputing the entry/checkpoint hashes is
accepted; no separately retained original checkpoint pin is required.

This is the same self-hashed candidate-copy trust gap R61AV fixed for R03, and
the R04V commission explicitly requires reuse of the external original
checkpoint boundary.

**Required:** a trusted-host capture returns a canonical checkpoint separately
retained by the coordinator; cold restore/resume requires that exact external
original pin (not a pin derived from submitted material) in addition to
structural validation. A forged/rehashed checkpoint must refuse.

### 3. Completed resume loses native outputs/facts and original manifest (blocking)

**Observed:** for a completed workload, `resume_joined_workloads` constructs a
synthetic `NativeWorkloadResult` with:
- `native_outputs=()`,
- `route_results=()`,
- a synthetic `BatchManifest` containing one `R04_JOINED_COMPLETED_UNIT`,
- `summary=None`.

The original native outputs/facts and manifest are not retained/rehydrated. The
author's test only compares unit receipt result refs/output refs. A same
consumer reading `native_outputs`/facts from the resumed completed result gets
nothing, while uninterrupted execution has the actual outputs. This does not
satisfy exact native operation/job/receipt/fact identity/multiplicity or the
same consumer assertion.

**Required:** retain and rehydrate the actual completed native outputs/facts
and the exact original manifest/unit identity (or exact fact refs/contents)
from the checkpoint; completed results must expose the same native facts/outputs
as uninterrupted execution, not only reconstructed Batch receipts.

### 4. Partial capture is refused rather than captured (blocking)

`capture_joined_checkpoint` rejects any result with a non-COMPLETED receipt
(`JOINED_CHECKPOINT_REQUIRES_COMPLETED_RESULTS`). The grant requires a real
partial native run followed by cold resume of remaining units; the author's
"partial" is a prefix of separate complete single-unit workloads, not a partial
multi-unit `NativeWorkloadResult`/manifest prefix. Capture and resume need the
actual partial receipts/pending units from the existing
`execute_issued_workload(max_units=...)`/Batch lifecycle, with completed units
not rerun and pending units honestly pending.

## Retained positives

- Author R04 focused suite 3/3; retained R03 suite 16/16.
- Unary complete-workload sequence: completed workloads are not rerun; revoked
  and wrong-source cases refuse; fresh-process checkpoint test passes at that
  narrow grain.
- U43 exact and unchanged; R04.byte decoder reused read-only, not rewritten;
  two authorized code paths only; R03/native owner bodies unchanged.
- No R05/original science/CI/prod/N11/N12/Sorok/J52/W52 claim.

## Limits / non-goals

Sourcefree TEST_ONLY trusted host only; no source respondent access. No new
global durable exactly-once/anti-fork, cryptographic issuer, R09, or R05
requirement is imposed. R04.byte custody is not re-litigated or edited. The
reviewer does not demand an unauthorized native-owner rewrite; the exact
indispensable additional path/dependency must be returned if the authorized
two-path interface cannot adapt the governed result.
