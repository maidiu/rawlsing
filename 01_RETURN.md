# S03 — GENERIC R4 BATCH RULE-ENVELOPE INTAKE / CONSTRUCTOR CONTRACT R1 — RETURN

Repository: `maidiu/rawlsing`

Worker branch: `agent/rabochii-prev3-w17-s03-generic-r4-batch-envelope-contract-r1`

Commission tip: `a50a8c3ad18a3e5033ffe6572bc3d5f733cdb49f`

Commission base / HQ authority: `8306aab9a3174f65c611f8157530307dabaf539c`

Exact grain:

`SDTF_R4_GENERIC_BATCH_RULE_ENVELOPE_INTAKE_AND_CONSTRUCTOR_CONTRACT_R1_ONLY`

Library: `NOT USED`

## Terminal

**PASS**

`S03_PASS__GENERIC_R4_BATCH_ENVELOPE_CONTRACT_FROZEN__SEPARATE_GENERIC_ADAPTER_REQUIRED`

PASS freezes a candidate-agnostic batch interface only. No concrete mechanism rule, authority, `CURRENT_ACCEPTED` rule, actor-position fact, topology, V3/person state, or OBL063 object is created.

## Governed contract

Artifact:

`02_GENERIC_R4_BATCH_ENVELOPE_CONTRACT.json`

Git blob:

`0a2eb3da6d755f12197348a71cfa7d1dd97d7b4d`

Semantic contract ref:

`SDTF_R4_GENERIC_BATCH_ENVELOPE_CONTRACT|SDTF_R4_GENERIC_BATCH_RULE_ENVELOPE_INTAKE_AND_CONSTRUCTOR_CONTRACT_R1@1.0.0|abc44b2b4ff04e164b5188e5929b0c10ca1b6e582b28207bb7e464ace698a83d`

The semantic hash is over the artifact's explicit `canonical_identity_material` under the project PRE553 canonical JSON / SHA-256 law. The non-normative M10 conformance fixture is excluded from that identity, so removing or replacing the fixture does not alter the generic field grammar.

## Complete generic constructor surface

The contract lifts the adopted R03 28-row canary inventory into a source- and candidate-agnostic interface. It exposes exactly the external determinants required by `SDTF_R4_MECHANISM_RULE_AUTHORITY_BINDING_R1@1.0.0`:

- 3 rule-identity atoms;
- 1 mechanism-class field;
- 1 constitution-current-selection ref;
- all 13 `RuleTraceBinding` fields;
- all 6 authority-role bindings;
- 1 value-mode field;
- all 3 rule-currentness fields.

The generic determinant ids are `GBE-R4-001` through `GBE-R4-028`. No Wright, M10, source-family, author, mechanism-name, authority-id, or candidate-specific default appears in a determinant name or type rule.

## Typed status law

Every determinant is carried through the same explicit status cell with one of:

`SATISFIED_CURRENT`

`SATISFIED_CANDIDATE_ONLY`

`MISSING`

`BLOCKED`

`NOT_APPLICABLE`

The states fail closed. `MISSING` never becomes N/A by omission. `BLOCKED` requires exact blocker refs. Candidate-only evidence cannot be projected as a runtime binding. `NOT_APPLICABLE` is legal only where the determinant's conditional law permits it and, for authority roles, requires the exact N/A basis demanded by the underlying R4 contract.

Field-level `SATISFIED_CURRENT` is not rule currentness. The contract preserves:

`CONSTITUTION_CURRENT != RULE_CURRENT != APPLICATION_CURRENT != FACT_CURRENT != WITNESS_CURRENT`

and:

`AUTHORITY_CURRENT != RULE_CURRENT`

## Six generic closure packages

The 28 determinants are partitioned exactly once across six reusable packages:

1. `PKG-A_RULE_IDENTITY_SHAPE_VALUE_CLASS` — rule id/version/hash, mechanism class, normalized mechanism, permitted shape, value mode.
2. `PKG-B_MANDATORY_AUTHORITIES` — `RULE_OWNER` and `CAUSAL_USE`, both mandatory `BOUND` roles.
3. `PKG-C_AUXILIARY_AUTHORITY_DISPOSITIONS` — measurement, estimand, identification, calibration.
4. `PKG-D_TRACE_EXACT_REF_LIFT` — constitution/source/claim/evidence/objective-input/currentness/historical/negative/V3-stop refs.
5. `PKG-E_QUALIFICATION_TEMPORAL_PORTABILITY` — qualification/realization, temporal/currentness, portability refs.
6. `PKG-F_RULE_CURRENTNESS_SELECTION` — rule-currentness enum plus current-selection/noncurrent-disposition refs.

`PKG-A` through `PKG-E` may close substantially in parallel. The only local serial dependency inside them is calibration after `value_mode` is known. A candidate may be assembled as `CANDIDATE_NOT_CURRENT`, but transition to `CURRENT_ACCEPTED` is the final serial gate: A–E must already be closed for the exact row, the exact projection must validate under the base R4 constructor, and independent rule-current-selection evidence must then be supplied by separately competent authority.

## Authority and value-mode preservation

The generic contract preserves all six `AuthorityCeilingBinding` roles with no role-specific fallback.

`RULE_OWNER` and `CAUSAL_USE` are always mandatory `BOUND` roles with exact scope, exact `AuthorityRef`, and nonempty authority-current-selection evidence.

`MEASUREMENT`, `ESTIMAND`, and `IDENTIFICATION` require explicit `BOUND` or explicit `NOT_APPLICABLE`; absence is invalid.

`CALIBRATION` remains conditional exactly as in R4:

`NUMERIC -> CALIBRATION BOUND`

`NONNUMERIC -> CALIBRATION NOT_APPLICABLE + exact N/A basis`

The batch contract never infers `NONNUMERIC` from qualitative prose and never treats source citation or mechanism-class membership as causal-use authority.

## Candidate identity, batch intake, dedup and replay

The generic schema separates a logical candidate key from immutable governed snapshots. A row carries an opaque `candidate_namespace` + `candidate_id`, an explicit nonnegative `row_generation`, an exact predecessor row ref for successor generations, exactly 28 requirement cells, and exact provenance refs.

Each candidate-row snapshot is content-addressed as:

`SDTF_R4_GENERIC_BATCH_CANDIDATE_ROW|<namespace>:<candidate_id>:g<N>|<sha256>`

Any governed value/status change creates a new row generation and content hash. No consumer may select the maximum generation or use `latest`, `default`, fuzzy, nearest, or semver fallback.

A batch is itself content-addressed from the generic contract ref, an exact batch namespace/id, and sorted unique candidate-row/provenance refs. Exact duplicate row refs are idempotently deduplicated. The same candidate namespace/id/generation with different hashes is `ROW_IDENTITY_CONFLICT`; the contract does not choose a winner. Similar semantics or common source family never trigger dedup.

Rows are independent and may run in parallel. A blocker on one candidate does not stop unrelated candidates unless the blocker itself explicitly names a shared contract/authority surface.

Per-candidate receipts bind the contract ref, batch ref, exact candidate-row ref, all 28 determinant states, six package states, blockers/integrity failures, runtime-projection state, optional runtime binding ref, current-selection state, and receipt predecessor. Replay identity is independent of worker count, execution order, and duplicate presentation.

## Failure / blocker semantics

The frozen fail-closed classes include:

`MALFORMED_EXACT_REF`

`MUTABLE_SELECTOR_FORBIDDEN`

`SILENT_NA_FORBIDDEN`

`ROLE_DISPOSITION_INVALID`

`VALUE_MODE_CALIBRATION_MISMATCH`

`CURRENTNESS_EVIDENCE_MISMATCH`

`ROW_IDENTITY_CONFLICT`

`PREDECESSOR_CHAIN_INVALID`

`CANDIDATE_BLOCKED`

No failure state manufactures an opposite fact, N/A disposition, authority, or currentness proof.

## Existing R4 runtime: direct consumption decision

**Direct consumption: NO. A separately authorized generic adapter implementation is required.**

The existing R4 implementation accepts a fully resolved `MechanismRuleIdentity`, `RuleTraceBinding`, six `AuthorityCeilingBinding` objects, exact refs, `RuleValueMode`, `RuleCurrentness`, and current/noncurrent ref tuples. It does not implement batch rows, typed unresolved statuses, dedup, snapshot lineage, package scheduling, or per-candidate receipts.

The required future adapter is narrow: validate this generic intake contract; project only exact resolved/explicit-N/A cells into the already-adopted R4 constructor; preserve the 28-field mapping; emit deterministic receipts. It must not mint authorities or refs, invent rule bodies/hashes, infer N/A, choose mutable selectors, materialize facts/topology, or issue rule `CURRENT_ACCEPTED` unless separately commissioned with the competent selection authority.

This is an adapter requirement, not a new R4 architecture requirement. The existing R4 constructor remains the authoritative final envelope validator.

## M10 canary conformance only

M10-M01 is retained solely as a non-normative fixture. At the adopted HQ base, its Q01 `RULE_OWNER` binding and R02 `CAUSAL_USE` binding occupy the same generic rows 19 and 23 any future candidate would use. No M10-specific codepath or default is introduced, and this return does not construct an M10 rule.

## Static qualification

Interface audit: **PASS**.

- determinant count: `28/28`;
- determinant ordinals: contiguous `1..28`;
- package partition: every determinant appears exactly once;
- authority-role count: `6/6`;
- trace-field count: `13/13`;
- currentness fields: `3/3`;
- semantic contract hash replay: `abc44b2b4ff04e164b5188e5929b0c10ca1b6e582b28207bb7e464ace698a83d`;
- no S01/S02 provisional output consumed;
- no Library use;
- MAIN/PRE-MAIN untouched.

## Boundary preservation

This PASS does not implement the adapter and does not authorize candidate-specific semantics. It mints no concrete mechanism rule, source/claim authority, actor fact, topology, numeric effect, `CURRENT_ACCEPTED` rule, V3/person state, or OBL063 object.

`GENERIC_BATCH_SCHEMA_READY != GENERIC_BATCH_ADAPTER_IMPLEMENTED`

`BATCH_ROW_READY != CONCRETE_RULE_CURRENT`

`S03_PASS__GENERIC_R4_BATCH_INTERFACE_READY_FOR_SEPARATELY_AUTHORIZED_ADAPTER_IMPLEMENTATION`
