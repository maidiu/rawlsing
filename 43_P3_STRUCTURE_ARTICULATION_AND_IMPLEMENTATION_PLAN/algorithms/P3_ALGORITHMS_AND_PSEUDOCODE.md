
# Rawlsing P3 Algorithms and Pseudocode

## Governing principle

P3 may generate candidates. It may not manufacture pair authority, canonical family authority, measurement compatibility, causal authority, strata direction, or runtime substitutability.

All algorithms are deterministic under a frozen input manifest. Every builder sorts inputs by stable identifiers before allocating derived row order. Durable object IDs come from the governed ID registry, never from transient row order or current membership hashes.

## A. Normalize P2 authority

Inputs:

- closed P2 proposition relations;
- exact-foundation rulings;
- structure-member rulings;
- negative, redirect, and unresolved authority;
- evidence records and semantic overlays.

Output: `p3_pair_fact_bundles.csv`.

Pseudocode:

```text
for each direct P2 ruling:
    resolve each endpoint to a source-local lineage or approved P3 segment
    canonicalize endpoint order for symmetric relations
    preserve direction for nested and constituent relations
    classify relation_type
    assign maximum portability ceiling from the P2 ruling
    set connectivity_allowed only for:
        PROPOSITION_RESPONSE_IDENTITY
        PROPOSITION_IDENTITY_ONLY
    bind every source P2 ruling ID and both endpoint evidence surfaces
    assert creates_endpoint_authority = false
```

A path between two nodes never produces a new pair fact.

## B. Recover proposition signatures

Evidence precedence:

1. source-native direct question;
2. source-native parent prompt;
3. source-native response dictionary;
4. adjudicated source structure;
5. source-local lineage implementation history;
6. direct P2 ruling evidence;
7. corrected semantic overlay for diagnostic location only.

For each signature field:

```text
collect authoritative evidence values
if one authoritative value:
    state = KNOWN
elif source explicitly omits the dimension:
    state = EXPLICITLY_UNSPECIFIED
elif field does not apply:
    state = NOT_APPLICABLE
elif evidence is absent:
    state = UNRECOVERED
elif implementations differ materially:
    state = HETEROGENEOUS
elif authoritative records conflict:
    state = CONFLICTING
elif only diagnostic inference exists:
    state = DIAGNOSTIC_ONLY
```

A `KNOWN` field requires an evidence ID. A diagnostic value never satisfies canonical evidence sufficiency.

## C. Detect lineage drift and create P3 segments

P2 lineage authority remains immutable.

```text
for each lineage:
    derive implementation-level proposition signatures
    compare target, operator, modality, timeframe, population scope,
            geographic scope, polarity, and direct/derived status
    if differences do not change the social proposition:
        retain one P3 subject
    else:
        identify contiguous or explicitly governed implementation groups
        allocate P3 segment IDs
        preserve exact implementation membership and historical interval
        create BLOCK_HETEROGENEOUS_LINEAGE against unsplit family use
```

Segmentation is a P3 family-authority device. It does not deny longitudinal continuity.

## D. Construct connectivity and constraint graphs

Connectivity graph contains only direct:

- `PROPOSITION_RESPONSE_IDENTITY`;
- `PROPOSITION_IDENTITY_ONLY`.

Constraint graph contains:

- all typed collisions;
- unresolved authority;
- nested/hierarchical relations;
- structure-only relations;
- response incompatibilities;
- heterogeneous-lineage blockers;
- semantic redirects.

Coordinate relations remain outside both family connectivity and collision blocking unless a separate P2 ruling supplies a direct constraint.

## E. Generate strict seed components

```text
G_strict = graph(nodes=lineages_or_segments)
add only PROPOSITION_RESPONSE_IDENTITY edges
seed_components = connected_components(G_strict)

for each seed_component:
    materialize exact member set
    create internal pair matrix over all n*(n-1)/2 pairs
    attach direct pair facts and collision facts
    compare proposition signatures
    classify every internal pair:
        DIRECT_POSITIVE
        DIRECT_COLLISION
        HIERARCHICAL_ONLY
        UNRULED
        SIGNATURE_CONFLICT
        SIGNATURE_COMPATIBLE
```

Connectedness is only a candidate-generation device.

## F. Attach proposition-only relations

A `PROPOSITION_IDENTITY_ONLY` edge may:

- propose a new candidate around isolated endpoints;
- attach a lineage as a response variant proposal;
- connect two candidates for adjudication.

It may not automatically merge two strict components.

```text
for each proposition-only edge:
    if both endpoints already in same candidate:
        record supporting fact
    elif one endpoint belongs to a candidate:
        create ATTACHMENT_REVIEW closure obligation
    elif endpoints belong to different candidates:
        create MERGE_OR_SIBLING_REVIEW closure obligation
    else:
        create proposition-only candidate
```

## G. Partition by signature compatibility

The default proposition-defining dimensions are:

- subject role;
- operator;
- target;
- object or outcome;
- modality;
- material timeframe;
- condition;
- population scope;
- geographic scope;
- polarity;
- direct/derived status.

Response topology is a variant dimension, not a proposition dimension.

```text
for each candidate:
    build compatibility keys from KNOWN and EXPLICITLY_UNSPECIFIED fields
    preserve UNRECOVERED, HETEROGENEOUS, and CONFLICTING as blockers
    if multiple incompatible complete keys:
        partition into candidate families
        preserve original component as parent diagnostic object
```

## H. Build closure obligations

Create an obligation for every internal pair with:

- direct hard collision;
- unresolved relation;
- no direct P2 ruling;
- signature conflict;
- incomplete essential signature;
- heterogeneous lineage;
- proposition-only relation joining strict components;
- value-portability blocker relevant to variant planning.

No candidate becomes `EVIDENCE_COMPLETE` until every required obligation exists. No candidate becomes canonical until every essential obligation has a terminal disposition.

## I. Construct variants

Permitted default variant dimensions:

- response topology;
- wording or translation;
- source-specific response form;
- historical interval where proposition identity is explicitly preserved.

Default split dimensions:

- target;
- operator;
- modality;
- actual behavior versus willingness or intention;
- direct item versus derived index;
- materially different population or geographic scope;
- timeframe that changes the social claim.

```text
if proposition signature is identical:
    group members by response topology
    create explicit variants where needed
    set value_portability_status = NOT_AUTHORIZED_BY_P3
else:
    split or create hierarchy
```

## J. Construct hyperedges

Permitted P3 hyperedges:

- battery;
- cross-source battery analogy;
- derived-index constitution;
- sibling-family construct;
- target hierarchy;
- response-contract class.

Each hyperedge records participant roles and an authority effect. `causal_authority` is always false in P3.

## K. Rank candidates lexicographically

Ranking tuple:

```text
(
    status_rank,
    hard_collision_count,
    unresolved_obligation_count,
    negative_signature_completeness,
    negative_source_count,
    negative_lineage_count,
    negative_direct_positive_density,
    negative_structure_support,
    response_variant_complexity
)
```

The tuple orders review. It never decides authority. Hard blockers cannot be compensated by broad source coverage.

## L. Select pilot candidates

Generate candidates globally from all 641 proposition relations. Select at most forty candidates according to `P3_PILOT_SELECTION_RULES.yaml`. Category overlap is allowed. Shortfalls must be documented.

The selected pilot becomes a permanent regression set.

## M. Structured adjudication

The adjudicator completes explicit fields:

```text
decision_status
canonical_proposition
accepted_members
excluded_members
variant_assignments
hierarchical_relations
collision_dispositions
unresolved_boundaries
rationale
evidence_bundle_hash
```

No parser infers authority from free prose.

## N. Doctrine delta and rebuild

```text
when a candidate reveals a missing general rule:
    write doctrine delta
    identify affected objects from dependency ledger
    add example/property/mutation tests
    choose rebuild scope
    rebuild affected surface
    rerun pilot gold fixtures
```

A candidate-specific judgment is not generalized without a doctrine delta.

## O. Stable identity allocation

- IDs are allocated from `p3_object_id_registry`.
- Candidate IDs survive membership edits.
- Canonical family IDs survive ordinary revisions.
- A split or merge creates new canonical family IDs.
- Predecessors remain in genealogy.
- Content hashes identify definitions and evidence bundles, not durable objects.

## P. Dependency and dirty-set computation

```text
changed_ids = corrected authority, vocabulary, schema, builder, or evidence IDs
dirty = direct dependents(changed_ids)
while new dependents exist:
    dirty += dependents(dirty)
classify rebuild scope:
    candidate local
    component local
    affected dependency closure
    global candidate inventory
    full P3 authority
```

The impact report lists every candidate, canonical family, hyperedge, release, and runtime artifact affected.

## Q. New-wave attachment

```text
ingest implementation
adjudicate source-local lineage attachment
recover implementation proposition signature
compare with lineage signature
if material drift:
    segment or block
evaluate canonical family exclusions
outcome:
    attach to existing variant
    create new variant proposal
    create new family candidate
    create hierarchy proposal
    fail closed
rebuild only dirty dependency closure
```

## R. Release, shadow install, and rollback

P3 pilot remains file-based. P3 closure produces an authority release and PostgreSQL-compatible migration artifacts.

Runtime sequence:

```text
validate migration in isolated test database
install into shadow namespace
rebuild runtime artifacts under prior and proposed authority
compare all family memberships, packets, certifications, gaps, and outputs
if all governed changes reconcile:
    promote transactionally
else:
    block promotion and roll back
```

No live installation occurs without a user-designated current repository or database.

## S. Determinism

Every builder must:

- sort inputs by stable identifiers;
- normalize Unicode and whitespace under explicit rules;
- reject duplicate normalized keys;
- write stable column order;
- avoid timestamps inside hashed canonical payloads;
- record builder and schema versions;
- create no cache or bytecode debris in the handoff;
- reproduce canonical and derived artifacts hash-identically.

## T. No-authority-leak assertions

The verifier must prove:

- coordinate, redirect, negative, and unresolved edges never enter connectivity;
- graph paths never become pair authority;
- family acceptance never writes value portability;
- P3 hyperedges never assert causality;
- strata context never becomes causal direction;
- diagnostic rankings never become canonical decisions;
- historical decisions remain immutable.
