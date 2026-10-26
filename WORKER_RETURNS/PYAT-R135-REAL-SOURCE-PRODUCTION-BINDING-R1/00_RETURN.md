# R135 — real-source production binding into existing Route B owners

**Status:** `PRODUCTION_TRANSPORT_QUALIFIED_ON_SYNTHETIC_HARNESS__NOT_SOURCE_RUN`

This is a code candidate, not source or scientific adoption. No source file,
checkpoint, raw response, or original product was opened. The proof uses a
clearly marked synthetic source and test-harness issuer objects; those are not
source permission or scientific issuance.

## Implemented seam

- `pre553_source_native_preimage_adapter.materialize_native_preimages` now
  accepts an optional externally supplied 7-authority exact set, validates
  ALLOW/roles, and does not generate authority when supplied. Existing test-only
  default remains unchanged.
- `pre553_native_workload_binding.build_projection_catalog` now accepts an
  optional externally supplied exact `PREDICATE_GRAMMAR` authority; the
  existing TEST_ONLY default remains unchanged.
- New `pre553_production_binding.py` transports caller-supplied descriptor,
  exact `NativeWorkload` inputs, and external `IssuedWorkloadRecord` into the
  unchanged `execute_issued_workload(... allow_test_only=False)` route.
  It does not construct authority, a grant, a descriptor default, a source
  reader, or an `IssuedWorkloadRecord`.
- `build_production_workload` accepts external request(s)/discovery refs, so the
  query/discovery law is supplied by the caller. No easier frontier is selected.

## Actual proof (synthetic harness only)

- New focused tests: **5 passed**.
- Affected existing source projection and workload custody tests: **5 passed**.
- One native production transport positive emitted a real native
  `EmpiricalFact@1.0.0` output with `scope=ORIGINAL_SOURCE_GRANTED`:
  `9fc7b48d1e6f840618c337d77ef08ff3bf3b4001104b01ee333a508f0c2186b4`.
- A different harness response emitted:
  `dca636b9ff9b61a717b2818d2383c0ff18ba2be298117fbed731d99d9e6c73b1`.
- Exact restoration returned the same fact refs and manifest hash.
- Refused before prohibited source invocation: TEST_ONLY record, wrong host,
  wrong envelope, wrong source SHA, wrong expected jobs, wrong U root, wrong
  Epre root, wrong native universe, wrong authority role, unbound risk
  descriptor, and TEST_ONLY query authority.
- No skip counted as pass.

## External production objects still required

The code now accepts, but does not issue:

- exact source-specific `AuthoritySnapshot` set from the source/semantic owner;
- externally issued exact query/discovery authority/policy and U/Epre roots;
- exact source descriptor and native projection/catalog/request/discovery refs;
- genuine current `IssuedWorkloadRecord` with source/scientific permissions,
  host, purpose, currentness/revocation, envelope, expected jobs and native
  universes.

The smallest unresolved decision is therefore the source-specific production
issuance tuple, not a missing Python module and not a global source denial. The
source/licence custodian and competent scientific owner must supply it; this
adapter does not silently choose one.

## Canonical identities

- `rawlsing_next/pre553_source_native_preimage_adapter.py`: blob
  `f21e01b19c921be169a96da825910d9836f4b974`.
- `rawlsing_next/pre553_native_workload_binding.py`: blob
  `a166d687786fe89879d2301bc904f1227038d3ac`.
- `rawlsing_next/pre553_production_binding.py`: blob
  `a34252a89afc8de2e37854f5d3acc4e655287838`.
- `rawlsing_next/tests/test_pre553_production_binding.py`: blob
  `4e3158cfcbedcc29d8bf1f34fd6186599ab85285`.

## Limits

R131 remains stopped. No learned/M2/B5, FF/V553, actor, CI/prod, N11/N12,
Sorok, J52/W52, all35, source, or scientific grant is claimed. M1 is not forced
for every fact. Distinct existing reviewer required.
