# P05-S1 — Consumer-first native execution and exact crash-resumable receipt contract

**HQ directly selected engineering design, 2026-10-28.** **NOT CODED, ORIGINAL GRANT OR NEW REAL CONSUMER PROVED.** No rabochiis, no replacement I03, no new semantic owner. Source control `299f41e97a43c67be9cc76a79fa49b48f4e12e54`; SRC04 packet fixed SHA `94661c14548947bd1c540482841c7c81c7dfc4861b5907f18b91a9e34cd24a5b`.
**Mandatory S0:** `P05_S0_SRC04_CONSUMER_RESUME_FORENSIC_AUDIT_R1.md`, which proves F01–F08 incl four sourcefree original adapter counterexamples.
**Selected direction:** native I03 exact outputs, a first durable verified source-local unary + conditional microflight, actual read-only Lane D and I05 consumption, **then** independently resumable remainder. Use existing PRE-MAIN `BatchManifest`/`UnitExecutionReceipt` and native `EmpiricalFact`/replay as authorities, not a second execution engine.

## 1. One actual first consumer vs catalogue

**Consumer-critical path** (all under current source/custody/target-use/operation/consumer authority):
1. Admit pinned original C11 source release and accepted/qualified Source04 exact ObservedResponseContract, with retained held slots unchanged. **Do not** reread original SAV merely for this consumer, and **do not** infer active original permissions from the file's presence.
2. Build **exactly one supported ordinary unary** `NativeOperation` using existing `_target_views`, `_make_predicate`, `_make_query`; existing 177 unary receipts can be used as candidates only after provenance, contract, query/predicate, native fact identity and execution code version are verified. Reexecution of a selected unary for Lane D is allowed under qualified actual execution; a JSONL word SUPPORTED is not authority.
3. Build **one valid separately issued conditional** from a distinct qualified conditioner with an observed permitted condition (the current actual 31 J2 receipts are not that operation). Use exact existing `_condition_members`, `_condition_predicate_ast`, I03, source risk denominator, authority and native fact; no invented direction from marginal counts.
4. Atomically publish one `CONSUMER_READY` checkpoint containing exact release/source+retention/authority refs, original query/predicate/fact/replay refs, complete zero-inclusive cell projections and exact native reconstruction recipes for BOTH operations. Persist nothing that would require declassifying respondent rows. This is a *qualified operational handoff*, not a new `EmpiricalFact`.
5. Immediately call existing Lane D `consume_native_producer` with *the genuine two operation objects* and release/query/predicate/repository; existing Lane D re-executes I03 and `replay_empirical_query` and must independently accept exact fact identity and produce genuine discovery result. Record product/ref, accepted claim ceiling and source-value-sensitive evidence/refusal. If Lane D not joined, record `D_CONSUMER_DEPENDENCY_NOT_JOINED` and stop this milestone, **not synthetic PASS**.
6. Resume/schedule the rest of every actually authorized native operation family independently after the first consumer; no claim that the 15,576 ordered/unordered pair catalogue (177 choose 2 = 15,576) was completed by two operations. A completed consumer doesn't close F1–F8, Authority-37, all35 N11 or Pyat N12. P05 just removes a false predecessor barrier.

**Operation order:** deterministically preserve the *same family/target/condition* exact identities as current native builder; reordering for priority is an operational schedule mutation, NOT semantic authority. Proof: every completed old and new native operation has identical `operation_id`, `query_ref`, `predicate_ref`, `fact_ref`, full receipt and replay. Refusals and ledger distinguish early microflight from deferred catalogue.

## 2. Exactly bound resume to one qualified execution campaign

Define `RunContext` in private scheduler (not native semantics) with:
- accepted `C11LogicalRelease.release_ref`, source_artifact_sha256 and `source_release_manifest_hash`, original source retention/custody binding, exact evidence version;
- `ObservedResponseContract.ref`, observed topology/target/held list, positive exact target-use/operation authority refs and current source/grant scope;
- `WorkloadPolicy` full immutable projection and enumerator version, operation family/arity/conditional policy;
- exact I03 query contract/source code version, exact query/predicate builder code version and current runtime successor/catalog authority binding;
- exact first/next consumer identity, permitted claim ceiling and type; exact current `BatchManifest.manifest_hash` where used.

Compute **operational** `run_fingerprint = semantic_hash(canonical_json-compatible immutable RunContext)`; not a new C11 semantic hash. A SHA of a caller-provided JSON manifest is **integrity**, not verification that its source/authority grant is genuine; validate actual owners independently at resume. Separate changed authority/runtime epoch, code version, source, contract or policy triggers **new run**, not silent reuse even if operation_id same.

## 3. Native per-operation journal and transaction

One full receipt per exact attempt:
```
{
 schema: "PYAT_P05_NATIVE_OPERATION_ATTEMPT@1.0.0",
 run_fingerprint, batch_manifest_hash,
 operation_id, family, exact_target_refs, condition_ref, condition_spec,
 query_ref, predicate_ref, full_workload_policy_hash,
 attempt_index, issued_source_custody_ref, positive_exact_execution_authorities,
 state: "COMPLETED_NATIVE"|"PERMANENT_REFUSAL"|"TRANSIENT_FAILURE"|"DEFERRED"|"INCOMPLETE",
 native_fact_ref, native_fact_state,
 native_query_replay_ref, complete_cell_semantic_projection,
 exact_raw_numerator, exact_raw_denominator, observed_ledger,
 accepted_downstream_evidence_refs, exception_type, exception_detail,
 previous_receipt_hash, receipt_hash
}
```
This is an **operational receipt wrapper** and must NOT mutate `NativeOperation.receipt()`, public empirical objects or source, replace the full original `EmpiricalFact` or create a second scientific issuer. Existing `UnitExecutionReceipt` controls manifest identity, contiguous attempt numbers and immutable prior completion; use an adapter around it to preserve exact unit identity/provenance without assigning inappropriate scientific meaning to an operational receipt.

**Do not equate status == EXECUTED with independently verified scientific acceptance.** A native I03 negative fact can be a completed evaluation but not a source-local supported positive. Preserve exact typed negative and failure code.

Append safely via a staging frame + checksum + single writer lock and durable flush; store last valid complete-record offset. Before new append on resume, verify every committed record against run context, operation identity, exact query/predicate/fact refs/authority, canonical type, sequence, `prev_receipt_hash` and expected status. Duplicate/conflicting receipt, interior corruption, mismatched run fingerprint, truncated/cross-source receipt => fail closed/quarantine; only an uncommitted tail after last accepted newline may be truncated to previously proved byte offset **with recovery receipt**. If a file is not a trusted append-only log, rebuild a clean verified checkpoint from exact sourcefree/full native receipts; never append behind a broken final line.

A completed operation means *qualified exact completed receipt*, not bare operation_id. Retry requires explicit changed attempt index and typed policy. Permanent scientific refusal remains refusal and cannot be laundered into success; transient unavailable/IO/interruption can retry with scope authority and revalidation. Unexpected Exception is **FAILED_UNCLASSIFIED/HOLD** until adjudicated, not automatically permanently completed or automatically retryable.

## 4. Cold-resume native consumer invariants

Persist and restore **all** original `NativeOperation.receipt()` fields (including `cells`, `observed_ledger`, `condition_counts`, error, fact state, query/predicate refs), and reconstruct same query/predicate under exact selected code/contract. `prior_*_record["cells"] = []` is FORBIDDEN. If a completed operation's native QuerySpec/Predicate cannot be reconstructed with original exact refs, **HOLD** and reissue an authorized attempt; do not fabricate a near-equivalent query.

For consumer-ready checkpoint, revalidate materialized/view C11 source, native full fact/ref and `replay_empirical_query`; do not infer that full acceptance follows from valid receipt SHA. Lane D requires a concrete `C11LogicalRelease` and source-certified root at current contract; until P01 S3/B05 view/materialization qualified, explicitly use existing accepted materialized release (with measured memory cost) rather than a counterfeit stub.

Resume must not re-execute all 15,576 pairs just to recover two consumer outputs. Restore those two from independently validated receipts and let Lane D itself reexecute/replay its chosen base query. If the real consumer requires additional native work, schedule that finite work under the same current authority before the catalogue, not a fabricated fallback.

## 5. Existing code patch owners and gates

| Ordered ticket | Original/current owner | Exact delta |
|---|---|---|
| **B00** | Source/authority accepted R157/SRC04 owner, current PRE-MAIN / SRC04 packet | Pin exact author/consumer code branch and authority, fixture vs original 175-vs-177 target scope, current grant, real Lane D code, 208 existing receipts. No original read without independent permission. |
| **B01** | `test_authorized_execution.py`, native old I03 and consumer | Freeze full synthetic golden receipts (cells+replay+authority), old conditional and actual Lane D fixture, false all-pairs dependency, four proven counterexamples; owner of expected values distinct from new scheduler. |
| **B02** | `native_streaming.py`, `pre553_batch_runner.py` | Add private immutable RunContext, manifest-qualified `UnitExecutionReceipt` adapter, framed log validation, exact attempt state, crash recovery and atomic checkpoints. No new semantic owner. |
| **B03** | `native_streaming.py`, `native_workload.py` | Preserve original `NativeOperation.receipt` and full `cells`; restore all exact fields and verify query/predicate/Fact identity before marking completed. |
| **B04** | `native_streaming.py`, `run_original_execution.py` | Consumer-first deterministic unary+one conditional scheduling; issue/publish `CONSUMER_READY` before broader J2; resume microflight independently. |
| **B05** | `consumer_bridge.py`, joined `consumers/consumer.py`, current I03/I05 | Real Lane D invocation and full exact discovery product/scope; sourcefree old/new agreement and original-source grant separation; record true positive/HOLD. |
| **B06** | batch scheduler + P01/P03/P04 exact read owners | Complete remaining permitted ops, repeated crash recovery, progress log append, test no duplicate refs and bounded resources, no all-pairs blocking first consumer; cannot claim P03 speedup or P01 memory saving before code runs. |
| **B07** | separate hostile reviewer; competent source/issuer and Codex HQ | Negative/restore/double replay, original-source qualified final consumer, exact SHA/test/provenance, host RSS/disk/wall, 35-wave applicability held unless actually tested. |

**Writer collision:** B02/B03/B04 share `native_streaming.py`; ONE engineering owner, no parallel divergent writer commits. Browser HQ owns the architecture decision and empirical-claim adjudication, not production editor/native source or science issuer. B05 consumer code held read-only unless competent consumer editor grants modification. Full `CodeX` order follows separately.

## 6. Nonpromotion and testing priority

Hard acceptance: actual independent old/new sourcefree complete identity across one first consumer, crash/torn lines, duplicate ref/conflicting attempt, source/authority change, exact source/value/held topology, per-operation native replay, then original source and native consumer actual result under qualified grant. A 200-line JSONL status log is not a product. Execution receipts that say SUPPORTED alone are not authority or accepted consumer. No person, no FF, no original science from this P05 migration.

**S1 disposition:** selected precise implementation, NOT coding. Next S2: complete differential/hostile acceptance matrix, high-resolution return ledger and exact independent Codex flight. The four proven adapter-local faults remain OPEN in production until repaired and tested under an actual selected author SHA.
