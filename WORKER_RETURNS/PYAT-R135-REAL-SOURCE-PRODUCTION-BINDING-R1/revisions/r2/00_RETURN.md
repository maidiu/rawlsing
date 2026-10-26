# R137 — exact repair of R136 production-binding defects

**Status:** `TOPOLOGY_SUPPORTED_NATIVE_POSITIVE_ON_SYNTHETIC_HARNESS__NOT_SOURCE`
**Code candidate:** same-owner repair of `bda89324a85ce06d44a19e6b19994e5543c065de`
**Governance:** R137 commission `a68f25aecb0add942a75573502485f9a65abeb66`; R136 REVISE `28b29b5c7919f85989b03b40654ebb7caa0bc9c5`.
**Source reads:** 0. All physical data is synthetic harness data; `ORIGINAL_SOURCE_GRANTED` is a code-path label, not issuance.

## Repairs completed

1. **Actual native positive.** With the exact external query authority supplied, `build_projection_catalog` now derives the target topology and domain from the materialized native release instead of hardcoding `SCALAR_SINGULAR`. The repeated-event target executes through the unchanged I03/Batch/C11 owners. Actual result: typed `SUPPORTED`, `raw_numerator_support=2`, `raw_denominator_support=2`, six exact repeated-event target cells, detail `exact governed target distribution resolved`. Response `0` and `1` produce different facts; restore reproduces the exact fact refs/manifest.
2. **Exact external query authority.** Before building the catalog, the repair requires exact `PREDICATE_GRAMMAR` ALLOW state, exact source SHA, exact universe set, exact risk set, one exact operation, and required object families. Foreign source/universe/risk/operation/role are refused. Original supplied authority refs are preserved.
3. **Exact source authority pre-check.** Supplied seven-role source sets now require exact source SHA and role order before response materialization. R136's foreign-source-authority repro now refuses with `SUPPLIED_AUTHORITY_SOURCE_MISMATCH`.
4. **Descriptor binding.** Production descriptors are compared against bundle/projection: source edition, native item IDs, release, routing/risk, carrier format/artifact, country/population, weight basis/design-estimand authority, missing/occurrence topology, and target/conditioner/measure roles. R136's foreign descriptor repro now refuses with `DESCRIPTOR_NOT_BOUND_TO_SOURCE`; caller metadata substitution is not accepted.
5. **No false discovery claim.** `build_production_workload` now refuses any discovery-only request with `PRODUCTION_DISCOVERY_ISSUANCE_CONTRACT_MISSING`; discovery refs are not accepted-but-unused. See banked decision below.
6. **Evidence count corrected.** Focused production tests: **10 passed**. Explicit affected regression nodes: **4 passed** (not 5). No skip counted as pass.

## Actual refusal replay (R136 exact cases)

| R136 case | Result |
|---|---|
| foreign query-authority source | refused `SUPPLIED_QUERY_AUTHORITY_SOURCE_MISMATCH` |
| foreign source-authority snapshot | refused `SUPPLIED_AUTHORITY_SOURCE_MISMATCH` |
| foreign descriptor metadata | refused `DESCRIPTOR_NOT_BOUND_TO_SOURCE` |
| actual supported positive | passes: `SUPPORTED`, 2/2 support, repeated topology |
| value change/restore | passes: different fact refs; exact restore |

The frozen R136 probe functions assert a returned non-positive result rather than an exception, so their original three tests now error on the refusal exception (`2 passed, 3 errors`). The semantic outcome is refusal, not acceptance; the exact exception codes are in `evidence/PROOF_RECEIPT.json`. No claim is made that the frozen probe form is a pass.

## Banked exact missing contracts

- **Permission before physical decode.** Current `IssuedWorkloadRecord` binds `envelope_sha256` of a `NativeWorkload` that requires an already-materialized `GovernedC11Projection` and `RuntimeObjectCatalog`; the source bytes are decoded before that record can exist. `admit` correctly precedes `source_factory`, but cannot cover the earlier decode. No existing source-read grant type exists. Smallest decision: an externally issued metadata-only source-read grant (source ID/SHA, host, purpose, read operation, scope, currentness/revocation, issuer authority, consumer) checked by the decoder owner before open/decode. See `CONTRACT_DECISIONS.json`.
- **Bounded production discovery/frontier ingress.** Existing `build_frontier_native_catalog`/`build_discovery_authority` generate `R03-TEST-ONLY-FRONTIER-QUERY-AUTH` and `R03-TEST-ONLY-DISCOVERY-AUTH`; `build_test_only_discovery_workload` and `execute_test_only_discovery_workload` hard-require `TEST_ONLY_SOURCEFREE`/`allow_test_only=True`. No external production discovery authority/frontier ingress exists. The repair therefore refuses discovery submission rather than claiming an unused path. See `CONTRACT_DECISIONS.json`.

## Preserved limits

R131 remains stopped. No real source, original 35/1890/F1–F8/global F6/F7/F8, learned/FF/V553, actor/M1-for-all, R09/CI/prod/N11/N12/Sorok/J52/W52/all35, or source/scientific grant is claimed. M1 is only for constitutive learned claims. Old R135 and R136 evidence are not rewritten.

## Code pins

- `rawlsing_next/pre553_source_native_preimage_adapter.py`: `79f9131366574a9c7bc787f71722dbbdda09814c`
- `rawlsing_next/pre553_native_workload_binding.py`: `b60f72668d99cd7c9f4583457be5a4d32b3168d8`
- `rawlsing_next/pre553_production_binding.py`: `6656e657c9a113f66dd7002706fbe876fcbc4bad`
- `rawlsing_next/tests/test_pre553_production_binding.py`: `a49a88dafc5f667838626e15395692098cdee0b8`
