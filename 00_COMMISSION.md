# T02 — GENERIC R4 BATCH ADAPTER IMPLEMENTATION R1

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-w18-t02-generic-r4-batch-adapter-impl-r1`

Commission base: `190e74d0266b6bc75bd24a34ff5a139590f0ce30`

Exact grain:

`SDTF_R4_GENERIC_BATCH_ENVELOPE_ADAPTER_IMPLEMENTATION_R1_ONLY`

Library: `NO`

## Governing inputs

S03 return tip:
`a718682521fe9b5c1d3b90e6a9c9e765ed892e8a`

Generic contract artifact blob:
`0a2eb3da6d755f12197348a71cfa7d1dd97d7b4d`

Generic contract ref:
`SDTF_R4_GENERIC_BATCH_ENVELOPE_CONTRACT|SDTF_R4_GENERIC_BATCH_RULE_ENVELOPE_INTAKE_AND_CONSTRUCTOR_CONTRACT_R1@1.0.0|abc44b2b4ff04e164b5188e5929b0c10ca1b6e582b28207bb7e464ace698a83d`

Underlying authoritative final-envelope validator:
`SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING_R1@1.0.0`

Implementation blob named by adopted R03/S03 authority:
`c94997f5c7f2bbee9cd99c570554fd48c0f47556`

## Mission

Implement the narrow generic adapter required by S03.

The adapter must:

1. ingest candidate-agnostic batch rows governed by the exact S03 contract;
2. validate batch/row identities, generations, predecessor refs, 28 typed determinant cells, package states and provenance refs;
3. preserve fail-closed states `SATISFIED_CURRENT`, `SATISFIED_CANDIDATE_ONLY`, `MISSING`, `BLOCKED`, `NOT_APPLICABLE`;
4. reject silent N/A, mutable selectors, identity conflicts, invalid predecessor chains, authority-role/value-mode/currentness mismatches;
5. project only fully resolved or explicitly lawful N/A cells into the existing adopted R4 constructor;
6. preserve the exact 28-field mapping and six package partition;
7. emit deterministic per-candidate receipts and batch receipts;
8. make execution order, shard, retry order, duplicate presentation, wall clock and worker identity nonsemantic;
9. support idempotent exact duplicate row refs but quarantine conflicting same-key/same-generation hashes;
10. never choose a winner among conflicting governed rows.

Use M10-M01 only as a non-normative conformance fixture. No M10-specific default, branch, hard-coded authority, source family, mechanism name or semantic path may enter the generic implementation.

## Implementation ceiling

This commission implements adapter/runtime plumbing only. It does not issue semantic authority.

The existing R4 constructor remains the final authoritative validator for projected fully resolved envelopes.

## Required tests

At minimum prove deterministically:

- exact contract identity accepted;
- wrong/mutable contract selector rejected;
- 28-field mapping complete and one-to-one;
- package partition exact;
- valid unresolved candidate row remains governed without projection;
- fully resolved candidate row projects exactly into R4;
- silent N/A rejected;
- candidate-only value cannot masquerade as current binding;
- row identity conflict quarantined;
- predecessor-chain error rejected;
- duplicate exact refs idempotently deduplicated;
- reordering/sharding does not alter semantic receipts;
- M10 fixture path uses only generic fields;
- no authority/ref/body/currentness is invented by the adapter.

## PASS law

PASS requires a committed generic adapter implementation plus deterministic local tests sufficient for a later independent qualification lane.

PASS wakes **separate independent hostile qualification of the generic adapter**. It does not make the adapter independently qualified by itself.

## Forbidden

- no concrete M10 or other mechanism rule minting;
- no `CURRENT_ACCEPTED` selection;
- no new RULE_OWNER/CAUSAL_USE/other authority issuance;
- no invented exact refs, N/A bases, rule bodies or hashes;
- no source semantic adjudication;
- no actor-position materialization;
- no topology;
- no V3/person state;
- no OBL063 semantics;
- no Library;
- no MAIN/PRE-MAIN mutation.

Commit the governed return and report final branch tip, implementation artifact identities, exact tests and terminal.
