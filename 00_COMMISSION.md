# T03 — GENERIC PRE-V3 STRUCTURAL BATCH CONTROL-PLANE IMPLEMENTATION R1

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-prev3-w18-t03-generic-structural-batch-control-plane-impl-r1`

Commission base: `190e74d0266b6bc75bd24a34ff5a139590f0ce30`

Exact grain:

`PREV3_GENERIC_SOURCE_SEMANTIC_BATCH_CONTROL_PLANE_IMPLEMENTATION_R1_ONLY`

Library: `NO`

## Governing inputs

S02 return tip:
`3e90760614d9bd90ddf28a7470d037eb68e6b8f0`

S02 governed audit blob:
`7192c089f566aceba1e55fbd966fc1a5bde62bd0`

Adopted scaling law:
`QUESTION_COUNT != POSITION_COUNT != RULE_COUNT != TOPOLOGY_COUNT`

Adopted staged model:
`SOURCE_LOCAL_INTAKE -> CLAIM_NORMALIZATION -> SEMANTIC_CORE_REDUCTION -> GENERIC_CONTRACT_VALIDATION -> AUTHORITY_CLOSURE -> QUALIFICATION/ENVELOPE -> INDEPENDENT_CURRENT_SELECTION`

Topology remains outside automatic candidate processing.

## Mission

Implement the generic **control plane** needed to run many source/evidence records through shared governed structural semantics without one bespoke worker chain per source question.

This is not the R4 rule-envelope adapter; T02 owns that separate runtime adapter. T03 owns only the generic cross-candidate control plane up to routing into specialized governed contracts.

Implement reusable typed records/interfaces for at minimum:

1. `SourceLocalIntakeRecord` — exact source/local identity, state/claim/evidence/provenance refs and replay identity;
2. `SemanticCandidateRecord` — content-addressed candidate semantic core plus exact evidence/admission refs and type/class ceiling;
3. occupant-independent position-semantic-core records distinct from later occupant/materialization requests;
4. mechanism-rule-candidate routing records distinct from concrete rule envelopes;
5. typed candidate status/blocker/quarantine records;
6. deterministic semantic-core reduction/dedup that deduplicates exact-equal governed semantic cores while retaining every contributing evidence/admission ref;
7. deterministic stage receipts / predecessor lineage;
8. explicit routing into specialized downstream contracts (e.g. R4 generic batch envelope adapter) without embedding those contracts' authority logic into the control plane;
9. fail-closed handling for malformed refs, replay mismatch, identity conflict, semantic-core conflict, missing authority/admission and quarantined candidates.

## Critical scaling behavior

Many source questions/evidence nodes may reduce to one shared semantic core **only when exact governed semantic identity is equal**. Similar wording, shared survey family, variable naming, common source author or model guess is never sufficient dedup authority.

Dedup must never drop provenance. A shared semantic core must retain a deterministic exact set of contributing evidence/admission refs.

Actor-indexed facts, concrete rule envelopes, rule currentness, application currentness and topology remain separate downstream identities.

Batch/shard/retry/order/wall-clock/worker identity are nonsemantic.

## Implementation ceiling

T03 implements control-plane plumbing and deterministic record contracts only.

It does not adjudicate new source semantics, invent semantic cores from unowned source text, issue authority, qualify a semantic candidate, materialize actor facts, construct mechanism rules, or create topology.

M10/Q03 may be used only as conformance fixtures for generic interfaces; no M10-specific path/default may enter implementation.

## Required tests

At minimum prove:

- exact source-local inputs replay deterministically;
- same governed semantic core + distinct evidence refs dedups core identity while preserving all evidence refs;
- semantically nonidentical cores never dedup merely from similar labels/text;
- occupant identity is rejected from reusable position-semantic-core identity;
- occupant/materialization request keeps separate identity;
- mechanism candidate routing does not mint a concrete rule;
- blockers/quarantines stay candidate-local unless exact shared contract blocker is named;
- batch order/shard/retry does not change semantic outputs;
- malformed/mutable refs fail closed;
- conflicting same-key governed semantic snapshots quarantine rather than winner-select;
- topology cannot be emitted by automatic batch processing;
- no source semantic/admission/authority widening occurs in control plane.

## PASS law

PASS requires committed generic control-plane implementation plus deterministic local tests sufficient for later independent qualification.

PASS wakes **separate independent hostile qualification of this generic control plane**. It does not make the implementation qualified by itself.

## Forbidden

- no new source semantic adjudication;
- no automatic semantic inference from question text;
- no concrete M10 rule;
- no `CURRENT_ACCEPTED` rule selection;
- no actor-indexed objective-position fact;
- no topology;
- no V555/M2 use;
- no V3/person state;
- no OBL063 semantics;
- no Library;
- no MAIN/PRE-MAIN mutation.

Commit the governed return and report final branch tip, implementation/test artifact identities and terminal.
