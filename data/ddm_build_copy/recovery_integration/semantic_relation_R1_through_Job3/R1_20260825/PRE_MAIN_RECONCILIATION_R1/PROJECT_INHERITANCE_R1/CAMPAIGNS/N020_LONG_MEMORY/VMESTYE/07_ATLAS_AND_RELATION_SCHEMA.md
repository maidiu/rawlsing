# VMESTYE — CANONICAL NORMALIZED ATLAS CONTRACT
The complete atlas is a **cross-referenced graph represented by version-controlled tabular files**; narrative is a human projection of the same facts. A single giant comparative spreadsheet would lose many-to-many relations, per-row source provenance and conditional edges.

## Canonical entities
1. **Function** `function_id`: semantic purpose, required input, transformation, output, negative contract, consumer reason, historical provenance, current necessity and owner. Original names remain aliases; no silent ID reassignment.
2. **Operation** `operation_id`: a concrete producer body or semantic transformation at exact SHA and scope. Many-to-many with functions, code and authorities.
3. **Authority** `authority_id`: source/semantic/issuer/version/selection and individual rule application; role and rule payload distinction. Many-to-many with operations.
4. **Implementation** `implementation_id`: code symbol/blob, adopted or branch-only, executable/fixture/native scope, rights and consumer.
5. **Consumer edge** `edge_id`: producer→consumer input/output contract, MUST/IF/ALTERNATE predicate, first read, proof, negative and terminal relevance.
6. **Evidence** `evidence_id`: immutable cut/path/blob/line-or-row, type, claim and evidence ceiling.
7. **Historical campaign stage** `generation_id`: original V550+/J, Dva, Trii, Chetiri, Long Memory, Pyat, PROGRAMMA. Existence in one era is not evidence of implementation in another.
8. **Dispute/decision event** `decision_id`: reason, old/new state, contradiction, reviewer and falsifier at immutable cut.

## Storage relationships
`DATA/LMX44_SEED.tsv` and `DATA/LMQ30_SEED.tsv` are **inherited frozen immutable identity snapshots** with `NOT_ASSESSED_CURRENT`; not another scientific baseline.
`DATA/FUNCTION_ATLAS.tsv` holds accepted *current comparative observations*, not copied source-corpus authority.
`DATA/OPERATION_TRACES.tsv` makes X→Y→Z→reader explicit.
`DATA/AUTHORITY_APPLICATIONS.tsv` distinguishes held, referenced, selected, applied and enforced-negative.
`DATA/RELATIONS.tsv` links any entities by precise edge type and source evidence; both forward and reverse navigation must be derivable.
`DATA/EVIDENCE.tsv` pins facts; `DATA/DECISION_EVENTS.tsv` records adjudicated changes.
`CONTROL/ESTATE_COVERAGE.tsv` records full denominators and whether their **content has actually been joined**; enumerating an ID is not a substantive coverage pass.

## Permitted relation types
`ORIGINATED_AS`, `PRESERVED_BY`, `SHARPENED_BY`, `CORRECTED_BY`, `SPLIT_INTO`, `COMPOSED_FROM`, `SUPERSEDED_BY`, `REJECTED_WITH_REASON`, `ASSIGNED_TO`, `REQUIRES_AUTHORITY`, `SELECTS_RULE`, `APPLIES_RULE`, `PRODUCES`, `CONSUMED_BY`, `IF_CONDITION`, `MUST_DEPENDENCY`, `ALTERNATIVE_TO`, `TESTED_BY`, `HELD_BY`, `STRANDED_ON`, `BLOCKED_BY`, `FALSIFIED_BY`, `ALIAS_OF`. New types require schema revision and migration.
Every actual-application edge requires independent evidence; an intention or naming similarity can only receive a `PLANNED_OR_CANDIDATE` grade.

## Mandatory node grain
The minimum comparison is *input and source identity*, *operation and rule*, *output shape/meaning*, *first actual consumer*, *negative/ceiling*, *current code and test at SHA*, *Dva/Trii/Chetiri/LMX disposition*, and *smallest missing proof*. For some functions the meaningful unit is a row or clause rather than a whole document; for others a behavioral contract rather than individual code lines. Don't force false one-to-one matches.

## Current status is a view of evidence at a cut
Do not overwrite frozen 2026-era original judgments. Link them to later evidence/dispositions. Display explicit `NOT_ASSESSED_CURRENT`, `NOT_INSPECTED`, `OPEN_PROOF_GAP`, `PARTIAL_SUCCESSION` etc. Passing 44/30 IDs is only `BASELINE_ID_INTEGRITY`, not `ZERO_LOSS`.

## Mechanical validators
See `validation/README.md` for lint/static consistency and final gate requirements. An independent reviewer still adjudicates same-grain semantic equivalence and science/authority matters; scripts do not mint them.
