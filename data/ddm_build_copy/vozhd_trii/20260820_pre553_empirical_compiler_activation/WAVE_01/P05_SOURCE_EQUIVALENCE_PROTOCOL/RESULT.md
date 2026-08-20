# PRE553 P05 — SOURCE→C11 EQUIVALENCE PROTOCOL RESULT

**Assignment:** `PRE553-W01-P05-001`  
**Agent:** `PRE553_P05_SOURCE_EQUIVALENCE_PROTOCOL`  
**Class:** `INSPECTORATE`  
**Branch:** `agent/vozhd-trii-pre553-w05-source-equivalence-protocol`  
**Exact base:** `e51730e461a15b0ad20f02f2efb4bccd751c2c81`  
**Semantic authority:** `NONE`  
**Runtime writes:** `NONE`

## Disposition

`SOURCE_TO_C11_EQUIVALENCE_PROTOCOL_FROZEN__POPULATED_PER_SOURCE_EXECUTION_REQUIRED__NO_SCHEMA_COUNT_OR_AGGREGATE_SHORTCUT`

Return token:

`PRE553_P05_SOURCE_EQUIVALENCE_PROTOCOL_COMPLETE`

## Core holding

Source→C11 equivalence is a per-source/per-release certification relation. It is not established by matching schemas, row counts, selected aggregates, file hashes, canonical labels, or a bounded query sample.

A local populated runner may return exactly one of:

- `CERTIFIED`
- `FAILED`
- `BLOCKED`

for each exact source/release/universe lane.

`CERTIFIED` requires complete applicable dimensional proof over source-native evidence and C11, including D13B P01–P20, the D13 C11 information obligations M01–M18, and the D12/D13 retained replay frontier T01–T18. Every mandatory dimension must pass; no mandatory `FAIL`, `BLOCKED`, `UNKNOWN`, silent default, coercion, or guessed interpretation is compatible with certification.

`FAILED` means required evidence is available and demonstrates a semantic mismatch, information loss, authority mismatch, nondeterminism, illegal default/coercion, or replay mismatch.

`BLOCKED` means a required source artifact, source-native semantic authority, topology/routing/weight basis, immutable identity, populated relation, or execution prerequisite is unavailable or cannot be lawfully resolved. Blocked is a valid result and never authorizes guessing.

## Source-safety holding

Original source/native snapshots remain retained for `CERTIFIED`, `FAILED`, and `BLOCKED` lanes. A certification receipt is not source-retirement authority. D15 permits only a later separate governance action to consider retirement after positive certification.

## Required proof surface

The protocol requires proof of at least:

1. exact source/release/universe and respondent identity;
2. source-native and canonical question/component/coordinate identity without raw-identity collapse;
3. response-event multiplicity and topology: scalar, multiselect set, repeated/sequence, ranked/order;
4. exact routing/applicability and risk-set member identity;
5. typed substantive/missing/DK/refusal/IAP/not-asked/inapplicable states;
6. raw support, weighted support, exact weight value/status/design/basis;
7. empirical-coordinate incidence including units/taxonomy/effective time and governed normalization/crosswalk authority;
8. predicate, condition-AST and target identity;
9. branch/cohort membership, k-way joint topology and same-respondent incidence;
10. authority identity, lineage, logical semantic integrity and deterministic replay;
11. duplicate semantics and order-independence under explicit topology;
12. exact source→C11 ingest/replay provenance with zero silent default/coercion.

## Certification non-shortcuts

The following can be useful diagnostics but can never independently certify equivalence:

- schema equality;
- table/column presence;
- source and C11 total row-count equality;
- respondent-count equality without exact scoped respondent-set equality;
- aggregate/prevalence equality;
- selected-query equality;
- serialized-file hash equality;
- schema hash equality;
- shared canonical labels;
- a current fixed V550 indicator inventory;
- default-filled weights/topology/absence states.

The logical semantic hash is an integrity seal only after dimensional proof establishes that its projection includes every proof-relevant field.

## Local runner law

The populated runner is an executor, not a semantic authority. It runs from an exact clean checkout, inventories the exact source/release artifacts and populated relations, computes source-native diagnostics before normalization claims, ingests a deliberately bounded source/release only under accepted ingest authority, executes the frozen equivalence protocol, and returns an immutable receipt bundle.

The runner may reveal a defect and return `FAILED` or `BLOCKED`. It may not repair contracts, invent mappings, choose defaults, pool sources, normalize fuzzy labels, or alter semantic truth conditions during the run.

## Replay identity

A certification receipt is bound to:

`source/release/universe identity × source snapshot hash set × C11 universe/content identity × authority snapshot × ingest/query code/config hashes × proof protocol version × proof dimension evidence × replay root`

A later source release, authority revision, semantic mapping change, topology rule change, weight-basis change, or C11 rebuild with different semantic content requires a new certification. `latest` is never a valid binding.

## Scope hygiene

This package:

- defines no runtime;
- writes no production code;
- certifies no populated source without populated evidence;
- changes no D13/D15 semantic authority;
- authorizes no source pooling;
- authorizes no source deletion;
- authorizes no V553 or downstream interface change.
