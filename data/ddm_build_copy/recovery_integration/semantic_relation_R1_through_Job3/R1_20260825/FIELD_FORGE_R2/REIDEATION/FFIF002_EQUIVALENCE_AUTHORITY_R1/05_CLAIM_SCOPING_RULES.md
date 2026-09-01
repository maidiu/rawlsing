# FFIF002 — CLAIM SCOPING RULES R1

## Governing proposition

Analytic equivalence is a permission indexed to a proposition, not a discovery that its inputs are identical.

`A ~ B FOR CLAIM C` does not entail `A = B`, `A ~ B FOR CLAIM D`, or `A ~ B IN EVERY REPRESENTATION`.

## When claim scope is mandatory

`claim_scope_ref` is mandatory whenever a transformation:

- collapses or groups source/project semantic distinctions for analytic convenience or substantive focus;
- asserts cross-context/wave comparability that is not already source-native or project-semantic identity;
- chooses a bin/partition whose boundaries encode a substantive analytic proposition;
- standardizes/ranks values under a particular comparison universe;
- treats wording/category differences as immaterial only for a bounded question;
- changes semantic eligibility for an analysis.

It may be null only when the transform is a pure deterministic syntax normalization, explicit source-native semantic declaration, or sufficiently adjudicated project semantic identity independent of a particular claim.

## A claim reference must be operational, not rhetorical

A lawful claim scope must identify enough structure to decide whether reuse is warranted. At minimum it should bind:

1. `claim_id` — immutable project claim/proposition identifier;
2. `comparison_target` — what relation/difference/distribution is being estimated or described;
3. `population_scope` — contexts/waves/subpopulations covered;
4. `measurement_scope` — variables/states involved;
5. `invariant_or_distinction_preserved` — what must remain meaningful after transform;
6. `distinctions_declared_immaterial` — what is intentionally lost;
7. `allowed_uses`;
8. `forbidden_uses`.

A prose token such as `employment`, `education`, or `class` is not enough. Broad labels can launder global equivalence.

## Examples

### Employment
States A and B may be lawfully grouped for:

`broadly employed versus not employed`

while remaining distinct for:

`labor-market insecurity`, `formal/informal employment`, or `employment stability`.

The first receipt cannot be reused for the latter claims.

### Education
Two credential categories may share an ordinal relation for:

`position in a locally defined credential hierarchy`

without being equivalent for:

`field-specific cultural capital`, `institutional prestige`, or a universal conversion to `years of education`.

### Income
Literal income, ordinal income situation, and food insufficiency may all bear on material position. That does not make them interchangeable measurements. A percentile/rank transform must name the reference universe and the claim for which relative position is the authorized invariant.

## Scope intersection rule

A TTAR is consumable only when downstream use is contained inside the intersection of:

`source_scope ∩ claim_scope ∩ validity_conditions ∩ allowed_uses ∩ representation_scope(if any)`.

If downstream use exceeds that intersection, a new authority determination is required.

## No implicit inheritance across claims

Two claims sharing vocabulary do not share transform authority automatically.

Reuse is permitted only if one of these holds:

- the receipt explicitly lists both immutable claim IDs and their relevant invariants are identical;
- a stronger project-semantic authority has subsequently superseded the claim-local equivalence;
- a new adjudication issues a new receipt referencing the earlier evidence.

## No implicit transitivity

If A~B for C and B~D for C, A~D is not inferred automatically unless the receipt's transformation is explicitly defined as a partition/equivalence class over {A,B,D}. Pairwise receipts do not create closure by accident.

Across different claims, transitive closure is prohibited.

## Allowed and forbidden uses are first-class

Positive permission alone is insufficient. Receipts should state predictable misuses explicitly.

Example:

- allowed: binary broad employment contrast in claim C;
- forbidden: labor insecurity gradient, occupational prestige geometry, cross-wave employment stability, reuse as project-semantic identity.

This prevents a lawful local simplification from becoming de facto global ontology through convenient reuse.

## Representational relation

A claim-scoped semantic transform that changes which empirical states count as same/different/comparable must be resolved before representations compete on common input.

A representation may add method-local coordinate transforms afterward only if those transforms do not alter the semantic distinctions authorized by the claim scope.

## Invalidation

A claim-scoped receipt becomes invalid when:

- source/codebook interpretation changes;
- a previously ignored distinction becomes constitutive of the claim;
- population/context scope expands beyond evidence;
- a method requires a stronger measurement property than the receipt authorizes;
- a new wave changes the category/wording relation;
- ancestry or replay becomes unavailable.

Invalidity triggers supersession/re-adjudication, not silent fallback.

## Anti-laundering test

Before approving a claim-scoped transform, ask:

> If this receipt were copied into every downstream view without its claim label, what false ontology would it manufacture?

If the answer names a plausible false sameness, ordering, metric, or comparability proposition, the receipt needs a narrower scope and stronger forbidden-use statement.