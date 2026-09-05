# GT12 R4D — ACTUAL CURRENT QUERY/FACT REHYDRATION R1

Repository: `maidiu/rawlsing`

Worker branch:

`agent/rabochii-gt12-r4d-actual-current-rehydration-r1`

Exact working start:

`a1630969f8e0b1003e657a38f77abbc413f83f2e`

Profile: `IMPLEMENT -> VERIFY_REGRESSION`

No Library. No source data. No empirical re-execution. No E2B.

## FIRST ACTION — NO BROAD ORIENTATION

1. verify branch HEAD exactly;
2. read only this handoff;
3. inspect only:
   - `rawlsing_next/pre553_repo_native_current_payload.py`
   - `rawlsing_next/pre553_repo_native_seal.py`
   - `rawlsing_next/pre553_empirical_objects.py`
   - A's committed constructor manifest + three payload binaries;
4. identify the minimal current-loader write set;
5. externalize progress immediately by committing the first coherent bounded implementation/checkpoint once that seam is known.

Do not read the full R4 program, old worker chats, old R4A attempts, or unrelated governance unless a concrete open claim requires it.

## Frozen actual Worker A state

Worker A terminal SHA:

`96ca3f02959905a88561fee5fdfa55d4aa144e48`

Durable EXECUTE checkpoint:

`43cf3df0fc9002a38d72ad57f1fe4dfe1f3736fb`

Exact current identities:

- predicate `bd91b40575035a9ff9ad2e7c507adc2610bfebdcc7fa38ce1cd697b37559cea3`
- query `e4ec3998664975c6a5f9e020b7815cfe6d39a212e264963d8037e6f0db87d0d0`
- fact `540236d533e9123f6d7b4d1edd4cf0951277154e72c7667deb09fb6550f11f46`
- replay `c0c23ca2bb439364756503722b60d047139d42a6128411cc19bfbd87d33c884f`

Committed constructor transport root:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/GT1_GT2_BOUNDED_CLOSURE_FANOUT_R1/R3_PERMISSION_TRANSLATION_AUTHORITY_CONSTITUTION_R1/R4_E2A_RUNTIME_TRANSPORT_SEAL_R1/R4A_CURRENT_GT2_EXECUTION_CONSTRUCTOR_COMPLETE_EXTRACTION_R2/`

Manifest:

`02_CONSTRUCTOR_COMPLETE_MANIFEST.json`

Manifest SHA-256:

`c2d008a96ce1cf9156cd9e10ebaf513f300139853a60db5856569f1375233c89`

Payloads:

- respondent refs:
  `payload/respondent_ref_hashes.bin`
  19,210 / 614,720 bytes /
  `9c34860a8a2a474e667e72ec5141e199b853672efb851bddebbd2dcde0d7a80b`

- routing refs:
  `payload/routing_ref_hashes.bin`
  38,420 / 1,229,440 bytes /
  `9ab1b53264a159d9446c8cfaef4c63c7c9786cd12e6e96d143ee57e6ad894825`

- event refs:
  `payload/event_ref_hashes.bin`
  38,420 / 1,229,440 bytes /
  `2fa09161ad457750dc3c80865811731908bdeb1c82dfdd36e958f178ede041b1`

Manifest reconstruction law is authoritative:

- respondent exact refs regenerate from 32-byte hashes using the frozen kind/object-id template;
- routing exact refs likewise;
- event exact refs likewise;
- risk-set members = respondent refs;
- denominator members = respondent refs;
- provenance = canonical ExactRef set(release, replay manifest, empirical universe, routing refs, event refs);
- dependencies = canonical ExactRef set(query ref, predicate ref, replay ref, provenance).

## Existing Worker B framework

Already in the candidate:

- `rawlsing_next/pre553_repo_native_seal.py`
- `rawlsing_next/pre553_repo_native_current_payload.py`
- `rawlsing_next/tests/test_pre553_repo_native_seal.py`

The generic seal/rehydrator returns ordinary existing `EmpiricalQuerySpec` + `EmpiricalFact` and contains hostile tamper checks.

Worker B intentionally left:

`CURRENT_GT2_PAYLOAD = None`

because Worker A had not yet supplied real payload material.

## Mission

Implement the smallest repo-native current-object bridge from A's **committed fixed repo seal** into B's ordinary-object loader.

Requirements:

1. current entry remains no-argument;
2. caller cannot supply path, identity, authority, or permission overrides;
3. fixed repo-native A manifest/payload identities are constants;
4. verify manifest SHA, each payload SHA, exact byte counts, exact ref counts;
5. reconstruct exact refs exactly per A's manifest law;
6. reconstruct ordinary existing `EmpiricalQuerySpec` and `EmpiricalFact` through their existing constructors;
7. constructors must independently recompute/validate the frozen content hashes;
8. require exact current query/fact/replay/predicate identities;
9. no Library/source/carrier access;
10. no raw respondent values, source rows, or `.sav`;
11. no semantic/hash-law change;
12. no caller-selected filesystem path. A fixed internal repo-resource location is permitted because the repo seal itself is the transport object.

Prefer:
- one small current-specific loader module, or the smallest edit to the existing current-payload seam;
- keep the generic B seal unchanged unless necessary.

## Hostile actual court

Must prove:

- exact current no-Library load returns ordinary exact `EmpiricalQuerySpec` + `EmpiricalFact`;
- query hash exactly `e4ec3998...`;
- fact hash exactly `540236d5...`;
- replay exactly `c0c23ca2...`;
- predicate exactly `bd91b405...`;
- denominator exactly 19,210;
- manifest tamper fails;
- any binary payload tamper fails;
- truncated/extra payload fails;
- wrong ref count fails;
- wrong fixed identity fails;
- historical A3 cannot impersonate current;
- no caller path/authority/identity parameter exists;
- runtime succeeds with Library/source/carrier access unavailable.

Run B's synthetic seal hostile tests plus the smallest PRE553 current-object regressions required.

Use one governed court proof owner. Do not create alternate CI infrastructure.

## Terminal

PASS only as:

`PASS__GT12_R4D_ACTUAL_CURRENT_QUERY_FACT_REHYDRATION_EXACT__NO_LIBRARY`

Return:
- exact terminal SHA;
- exact current-loader API;
- exact governed court run/count;
- confirmation ordinary current query/fact were reconstructed from the committed A seal without empirical re-execution.

Do not issue final R4 transport PASS. Do not execute E2B.
