# R91 R04_JOINED custody/resume contract

Status: frozen before the R91 code commit. Sourcefree TEST_ONLY local trusted
host. Reuses `NativeWorkloadResult`, U43 admission, C11/Batch owner objects and
R03-issued workloads; no decoder/native-engine rewrite, no R05 overlap.

## Capture

`capture_joined_checkpoint(results)` accepts only completed
`NativeWorkloadResult`s whose receipt count closes over the full manifest and
whose receipts are all COMPLETED. It records exact decision/envelope/source/
manifest identities, receipt preimages (including unit/provenance/result refs)
and output refs, with a canonical checkpoint hash and per-entry hash. Partial or
duplicate decisions refuse; unfinished results cannot be captured as complete.

## Resume

`resume_joined_workloads(workloads, source_factory, host, purpose, checkpoint)`
accepts actual R03-issued workload objects. It verifies checkpoint hash,
decision/envelope/source identity, no unknown/duplicate workloads, then:
- completed decisions are represented by retained receipts/output refs only and
  are not executed again;
- pending workloads run through the existing `execute_issued_workload`
  admission/source/Batch path with current grant and source identity rechecked;
- combined output refs and receipt materials must equal the uninterrupted
  sequence; partial/ambiguous units are never invented as complete.

Fresh-process resume loads the canonical checkpoint material and rebuilds the
same R03 workloads from the retained source/bundle, then resumes remaining work.
Revoked/current mismatch or wrong source edition refuses before native work.

## Limits

No R04 byte-decoder rewrite (R04.byte accepted body reused read-only), no new
trust service, no global durable exactly-once/anti-fork, no original science,
R05+, CI/prod/N11/N12/Sorok/J52/W52. The R03 compiler currently emits
single-unit workloads; joined resume is at workload granularity and does not
claim automatic governed-discovery caller wiring beyond the tested interface.
