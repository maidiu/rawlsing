# R91 R04_JOINED R2 contract — actual native partial restart

Status: frozen before R2 code commit. Implements the R04V defects inside the two
authorized R04 paths. Sourcefree TEST_ONLY local trusted host; R03/native owners
and R04.byte decoder unchanged.

## Accepted native objects

`capture_joined_checkpoint` accepts both actual R03 governed
`NativeDiscoveryExecution` (native_result/manifest/receipts/facts) and actual
`NativeWorkloadResult` query/discovery runs. It retains the original manifest
unit specs, completed receipt preimages, completed output fact OBJECT material by
unit, exact output refs and source/envelope/decision identities. It supports:
- COMPLETED full prefix;
- real PARTIAL `NativeWorkloadResult` prefix (`execute_issued_workload(max_units)`)
  with completed/pending units preserved.

Empty or duplicate-unit prefixes refuse. Discovery output facts/manifest are
retained, not replaced by a synthetic manifest/empty outputs.

## External original pin

The coordinator captures the live checkpoint and retains `checkpoint_hash`
separately. `restore_joined_checkpoint(material, expected_checkpoint_ref)` and
`resume_joined_workloads(... expected_checkpoint_ref)` require that genuine pin;
missing/wrong pin and internally recomputed forged hashes refuse. No pin is taken
from submitted payload. Same-host replacement of both pin and candidate remains
excluded (R61AV).

## Resume

Completed units are reconstructed from retained facts/receipts/manifest and are
not executed. PARTIAL entries reconstruct prior receipts/outputs and call the
existing `execute_issued_workload` lead with `prior_receipts`/`prior_outputs`;
Batch skips completed units and runs pending units through existing
C11/I03/I05/Batch. Current grant/source identity rechecked before pending work.
Exact combined output refs/receipts/multiplicity must match uninterrupted run.

## Limits

No indivisible discovery split, new lineage engine, R05+, original science,
global durable exactly-once, CI/prod/N11/N12/Sorok/J52/W52. Workload/unit
granularity only; automatic governed-discovery caller wiring beyond the tested
interface is not claimed.
