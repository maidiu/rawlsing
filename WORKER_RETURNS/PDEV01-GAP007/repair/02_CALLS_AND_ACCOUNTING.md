# GAP-007 repaired receiver calls and accounting

## Exact source/C11 lineage

- Synthetic source SHA-256: `443ebf5c74ad119fed2f79e148146e8772ad6f12317dcfcfcbe014136bf27eb4`
- Source rows: 12; physical columns: 71 (70 P1 item codes + FORM)
- Actual C11 logical release: `R56-SYNTHETIC-RELEASE`
- Release ref: `383716e4c9d233df69ef8cd508f7ffa5053d7a7355e7135a170eb1c2b337d9c1`
- Release public objects: 1,700; internal records: 82
- Built with existing `build_source_backed_c11_repository` from the synthetic source and projection.

## P1 plan binding

The exact P1 plan at `d1278613e9e1a5d986ccce15782a697f19cbd722` was reconstructed with the same 35 wave identities and item codes. Its original operation identity list is preserved exactly:

- Original P1 plan ref: `e0d4180cbfc43a1ddc5965ff20afb9cb284676c6c4981d9681d3e35121ac59ea`
- Bound plan ref: identical
- Original operation count: 840
- Bound plan manifest units: 210 (only P1 DISTRIBUTION operations)
- Typed unsupported operations: 630:
  - CONDITIONAL 210
  - JOINT 210
  - HETEROGENEITY 105
  - RECURSIVE_BRANCH 105

Each bound P1 distribution operation maps one-to-one to a distinct current `EmpiricalQuerySpec`:

- 210 distinct original operation refs
- 210 distinct bound query refs
- 210 distinct bound batch unit refs
- 210 bound units, no duplicate identities

P1 unsupported kinds are never turned into invented queries; they retain their original operation ref and a typed refusal `P1_OPERATION_KIND_HAS_NO_EXACT_CURRENT_I03_BINDING`.

## Actual I03/Batch calls

The binding constructs a current `BatchManifest` with 210 QUERY units and runs it through:

```python
BatchExecutionRunner(manifest=manifest, repository=repository)
CarrierNeutralResearchExecutor(repository, (release.release_ref,), catalog)
executor.execute_i03(query_ref=unit.job_ref, predicate_ref=bound_predicate)
```

Observed:

- 210 Batch receipts
- 210 COMPLETED
- 210 returned `EmpiricalFact` result refs
- 210 facts typed `SUPPORTED`
- P1 original operation count fully accounted: 840

## Actual I05 call

On the same synthetic source, a current governed frontier was compiled and executed through `execute_governed_frontier`:

- Native result type: `ExactBoundedDiscoveryResult`
- Receipts: 16
- Empirical facts: 30
- Candidate count: 16
- Coverage: `COMPLETE_FOR_EXACT_DECLARED_FRONTIER`
- Status: `EXECUTED`

This is a real I05 receiver capability call, not a P1 unit binding; P1 RECURSIVE operations remain explicitly refused rather than mapped by invented semantics.

## Refusals

- Wrong C11 release in a Batch unit: `BatchIntegrityError: exact C11 release unavailable; no latest/default/fuzzy/nearest fallback`
- Wrong query ref in actual catalog/executor: `CarrierExecutionBindingError: query_ref exact preimage unavailable; no latest/default/fuzzy/hash-inversion fallback`

Full trace: `01_ACTUAL_RECEIPT.json`.
