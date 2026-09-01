# FFIF002 — IDENTITY AND EQUIVALENCE ONTOLOGY R1

## Status
Semantic / representational authority design only. No respondent association, Position Role Authority adjudication, FFX002 execution, source acquisition, or project integration is performed here.

## Terminal proposition

`GLOBAL_EQUIVALENCE_LAYER_REJECTED__CLAIM_SCOPED_TYPED_TRANSFORM_AUTHORITY_WITH_SOURCE_NATIVE_ANCESTRY_REQUIRED`

The governing error is to represent every lawful use of `same`, `ordered`, `grouped`, `comparable`, or `mapped` as one identity relation. Rawlsing needs separate relation families whose authority, scope, information loss, and consumption rules differ.

## Identity / equivalence relation families

| Type | Meaning | May collapse distinct source-native states? | Scope | Authority consequence |
|---|---|---:|---|---|
| `PHYSICAL_IDENTITY` | Same byte, row, stored object, or immutable artifact. | No | physical/provenance scope | Provenance fact only; says nothing about semantic sameness. |
| `SOURCE_NATIVE_SEMANTIC_IDENTITY` | The source/codebook itself declares two encodings to instantiate the same source meaning. | Only if source explicitly does so | source-defined | Ingest source authority exactly; preserve source declaration and loss. |
| `PROJECT_SEMANTIC_IDENTITY` | Current project authority adjudicates two objects as the same semantic object independent of one analytic claim. | Yes, but only under unusually strong finite adjudication | project semantic scope | Must be explicit, evidence-backed, supersedable, and ancestry-preserving. |
| `ANALYTIC_EQUIVALENCE` | Distinct source/project states may be treated together for one bounded claim. | Yes | claim-scoped | This is permission, not identity. It is not globally transitive or reusable by default. |
| `ORDER_PARTITION_AUTHORITY` | States may be ordered, binned, partitioned, or collapsed according to an explicit relation. | Possibly | source/project/claim scope | Order does not imply cardinal distance; a partition does not imply semantic identity. |
| `REPRESENTATIONAL_EQUIVALENCE` | Objects may occupy one modality/node/coordinate class inside a specified representation. | Possibly | representation-scoped | Cannot leak backward to project semantics or sideways to another representation. |
| `TRANSPORT_EQUIVALENCE` | Objects across contexts may be compared/mapped for a named invariant. | Possibly | claim + transport scope | Must name the invariant and contexts; comparability is not global sameness. |
| `PERSON_ACTOR_IDENTITY` | Identity of persons/actors across records or contexts. | N/A | separate identity system | Explicitly out of FFIF002 scope. |

These distinctions are substantively correct but are sufficient only if they are implemented as different typed relation families, not values in a generic `same_as` column.

## Core law

`SAME` and `ALLOWED_TO_TREAT_AS_SAME` are different propositions.

Therefore:

1. analytic equivalence never upgrades itself to source-native or project semantic identity;
2. representation-specific equivalence never becomes common-input semantics by reuse;
3. transport equivalence is always indexed to an invariant and bounded context set;
4. order authority never entails equal interval or Euclidean distance;
5. no equivalence receipt acquires transitive closure merely because two receipts share an endpoint.

## Minimum surviving authority object

The smallest lawful object is a **typed transformation authority receipt**, abbreviated here as `TTAR`. The name is descriptive, not a newly minted project authority.

A TTAR is not itself a transformed dataset and is not an identity node. It is a replayable permission/assertion object attached to source-native ancestors.

Minimum fields:

- `transform_authority_id`
- `authority_class`
- `claim_scope_ref` — required for analytic or transport equivalence; nullable only where source-native or project-semantic authority itself is sufficient
- `source_scope`
- `input_state_refs`
- `transformation_type`
- `output_state_spec_or_ref`
- `semantic_assertion`
- `allowed_uses`
- `forbidden_uses`
- `loss_profile`
- `authority_ref`
- `evidence_refs`
- `ancestry_spec`
- `replay_spec`
- `validity_conditions`
- `invalidation_conditions`
- `supersedes`
- optional `representation_scope`

A receipt is invalid if the `input_state_refs` cannot recover the exact source-native states actually consumed.

## Why the candidate names are insufficient

- `ANALYTIC_EQUIVALENCE_AUTHORITY` is too narrow: ordering, monotonic transformation, source-native harmonization consumption, and noncomparability are not all equivalence.
- `STATE_TRANSFORMATION_AUTHORITY` is closer but can conceal who owns the semantic proposition and whether the transform is claim-scoped.
- `REVERSIBLE_RECODING_RECEIPT` overstates literal invertibility and understates authority.
- `CLAIM_SCOPED_IDENTITY_TRANSFORM` is dangerous because analytic permission is not identity and some lawful transforms are not claim-scoped.

`TYPED_TRANSFORM_AUTHORITY_RECEIPT` survives because it carries authority + type + scope + loss + ancestry without asserting that every lawful transform makes its inputs identical.

## Closure prohibition

No TTAR may be composed automatically into a stronger semantic proposition. If receipt R1 maps A/B -> X for claim C1, and R2 maps X/Y -> Z for claim C2, Rawlsing may not infer A/B/Y -> Z for C1, C2, or any third claim. Composition itself requires a new authority determination.

## Governing result

Rawlsing does not need a universal equivalence ontology above sources. It needs source-native semantic identity preserved below a finite set of typed, scoped, supersedable transformation receipts. This makes comparison possible without allowing preprocessing to become invisible ontology.