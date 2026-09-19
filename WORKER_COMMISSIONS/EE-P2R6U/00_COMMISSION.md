# EE-P2R6U — ADOPTED R6A RUNTIME SUBSTRATE FAN-IN PREPARATION

Repository: `maidiu/rawlsing`

## Execution surface
**BROWSER**

## Library access
**NO**

Exact branch:
`agent/rabochii-prev3-ee-p2r6u-r6a-runtime-substrate-fanin-r1`

Exact base:
`ae8b1db9d8c3288e002950ac01123c70f3138320`

Before doing anything else resolve live `HQ_HANDOFF/LATEST.json` and verify the immutable checkpoint packet.

At commission time:
- checkpoint: `20260919T0327-0400`
- immutable handoff: `b994ea63d2b9571415677e0d47a16bcd3e8322bf`
- controlling decision: `HQD-2026-09-19-081`

## Mission

Prepare the exact already-adopted EE-P2R6A runtime substrate required by the existing R6S LiTS runtime support. This is not a new runtime design.

The current P2X tree lacks `pre553_runtime_authority.py`, `pre553_runtime_context.py`, `pre553_runtime_composition.py`, the five exact R6A R4A authority fixtures, and carries pre-R6A versions of the runtime-aware query/discovery implementation.

The authoritative adopted R6A head is:

`3f382e6abd6c4f6f2271440041be27ceaf4900ee`

R6A PASS authority remains controlling.

### Exact adopted production blobs

Audit and, if lawful, materialize these exact adopted R6A bytes on this worker branch:

- `rawlsing_next/_pre553_query_common.py` — `938a6b03a63dd34ef4f0f63655ed8f11f65c5d92`
- `rawlsing_next/_pre553_query_eval.py` — `128b31fa60c2650d8c7af30f1f4b1d1470acd2b6`
- `rawlsing_next/_pre553_query_predicate.py` — `edc943ca6690ac73f24492f3d01ad9ee17f70f21`
- `rawlsing_next/pre553_discovery_exact.py` — `c7380774e8a1959da5ed8c6f23c2fc3cf99ad18d`
- `rawlsing_next/pre553_empirical_query.py` — `482778348d6b450f46985c2161af32f2961d8384`
- `rawlsing_next/pre553_runtime_authority.py` — `2ddc591f2572983d18f8f3e8f81a33b80b3bca7b`
- `rawlsing_next/pre553_runtime_composition.py` — `3753c183ddb25b1b0eb0ce84db1868f39f50d3fa`
- `rawlsing_next/pre553_runtime_context.py` — `3c26c77892395a4825b377b740e37df7ea1148d4`

Exact authority fixtures required by the already-fanned R6S LiTS runtime support:

- `ee_p2r6a_r4a_01_dialect.json` — `e49b33417ea1f57e5eacb557c173507a118e11de`
- `ee_p2r6a_r4a_02_respondent.json` — `490434c1fc87decb97d187e6185e1848045dd9c5`
- `ee_p2r6a_r4a_03_mixed.json` — `a18fd79609f080062b93dfe0e2bab8e9bf865af3`
- `ee_p2r6a_r4a_04_derived.json` — `5000020fa6554be9c2ad2ab418b6f5269b59d69a`
- `ee_p2r6a_r4a_05_successor.json` — `e19d076e2d2b0ecbf7ccacba5e23dd185ce43cfc`

Do not blindly overwrite a later independently adopted change. First prove the current P2X versions are pre-R6A/non-R6A rather than post-R6A supersessions. If any exact file has later adopted authority incompatible with the R6A bytes, BLOCK with that exact conflict.

## Required qualification

Without carrier access, prove:

1. all exact adopted blobs/fixtures are present;
2. the existing R6S LiTS support module imports successfully;
3. `materialize_runtime_authority_set()` returns exact `Pre553RuntimeAuthoritySet`;
4. `materialize_runtime_package()` still yields runtime catalog identity `5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02`;
5. 50 candidates / 77 query-role executions remain exact;
6. active binding `a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308` and runtime release `192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f` remain exact;
7. mixed R4A composition remains required and accepted;
8. legacy/no-runtime-context query paths retain accepted behavior;
9. no source/carrier/outcome/performance access.

Write only `WORKER_RETURNS/EE-P2R6U/**` plus the exact adopted runtime files/fixtures.

PASS:
`EE_P2R6U_PASS__EXACT_ADOPTED_R6A_RUNTIME_SUBSTRATE_MATERIALIZED_AND_R6S_LITS_RUNTIME_REQUALIFIED__READY_FOR_HQ_SELECTIVE_FANIN`

BLOCK:
`EE_P2R6U_BLOCK__<EXACT_FIRST_ADOPTED_RUNTIME_SUBSTRATE_CONFLICT_OR_QUALIFICATION_FAILURE>`

Do not move P2X. Return to HQ.
