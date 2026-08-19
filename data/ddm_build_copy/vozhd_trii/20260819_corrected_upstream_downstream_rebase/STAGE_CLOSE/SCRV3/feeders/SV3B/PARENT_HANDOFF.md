# SV3B — PARENT HANDOFF TO SCRV3

**Feeder:** `SV3B_OBJECTIVE_ACTOR_FACT_COMPARATOR_SNAPSHOT`  
**Authority:** `NON_DISPOSITIVE_TO_SCRV3`  
**Recommended feeder token:** `SV3B_FEEDER_COMPLETE`

## 1. Finite handoff

SV3B finds no broad-topology contradiction and no authority conflict requiring a block.

The comparator-facing V3 seam can close without inventing a new broad owner if SCRV3 preserves two separate gates:

```text
G1 objective actor fact existence/currentness under exact V3 owner
G2 exact ACTOR_EMPIRICAL_COMPARATOR_AUTHORITY mapping for source/coordinate/time
```

Only after both gates pass may `ActorComparabilityService` emit an exact `ActorComparatorReceipt` / empirical conditioner predicate.

## 2. Main result

The word **objective** is not sufficient comparator authority.

A V3 object can be objectively true and still be ineligible for comparator use unless a field/source/time-specific comparator rule explicitly names its fact class and owner.

This qualification is especially important for:

- ADP-009 structural position;
- ADP-015 household/relationship/genealogy facts;
- CAN-009 material/embodied actor state.

The accepted D15 list of candidate demographic/biographical families is an eligibility frontier, not a fact-generation registry and not a set of automatic mappings.

## 3. Current positive fact-owner findings

### ADP-007

`V3InitialGeneratedFact` is a lawful generic record family, but `V3_INITIAL_FACT_RULE_REGISTRY@1.0.0` contains no registered domain initial-fact rules in v1.

Therefore ADP-007 alone supplies no current generic sex/gender, education, language, religion, ethnicity, income, employment or occupation fact.

### ADP-009

`V3StructuralPositionFact` is an objective generated runtime fact when lawfully created.

However D15 explicitly states generated structural position is **not a generic comparator key**. Exact comparator use requires an explicit rule naming the exact ADP-009 fact class/dimension, owner, target source coordinate and temporal relation.

### ADP-015

Objective fact families include `V3HouseholdMembershipFact`, `V3ParenthoodFact`, relationship lifecycle/objective state refs and exact household/genealogy history.

These may be comparator candidates only under exact construct mapping. Subjective `V3ActorPerceivedRelationshipState` is not an objective comparator substitute.

### CAN-009

Actor-specific material/organismic dimensions are objective V3 causal state when lawfully committed, but their semantics do not automatically equal common survey constructs.

Examples:

- `MATERIAL_MONEY_CAPACITY != income` by default;
- `MATERIAL_JOB_INSECURITY != employment status` by default;
- `MATERIAL_MOBILITY_CAPACITY != migration/travel status` by default.

## 4. Candidate families with no generic current fact owner located

SV3B did not locate a generic accepted V3 fact owner that, by itself, supplies current comparator-ready facts for:

- age as a demographic fact (V3 effective time exists; phase/time is not age fact);
- sex/gender;
- education;
- language;
- religion/sect self-identification;
- ethnicity;
- income;
- employment status;
- occupation.

This is not a broad-topology defect. The D15 comparator authority already requires exact actor-side ownership. Missing actor facts therefore fail closed.

SCRV3 must not create those facts inside the comparator seam merely to make reverse inference work.

## 5. Snapshot candidate

SV3B proposes a parent-adoptable reference-only object:

`V3ObjectiveActorFactSnapshot@SV3B-0.1`

Core properties:

- one exact `actor_id`;
- one V3 `snapshot_effective_time` + time basis;
- explicit requested fact slots;
- only exact objective fact refs/hashes and their owner authority ID/version/hash;
- owner-defined currentness proof per binding;
- explicit missing/blocked slot records;
- no full actor state;
- no belief/memory/persona/response/perceived-relationship/V2 material;
- deterministic content hash;
- historical snapshots immutable; later requests construct a later-time snapshot rather than mutating old evidence.

The requested slot set is part of identity so an unrequested fact cannot be misread as missing.

## 6. Projection contract

SV3B proposes:

`ActorComparatorProjectionRequest@SV3B-0.1`

A positive rule must bind:

- allowed actor fact class and owner authority;
- exact universe and coordinate semantics;
- source/historical scope;
- projection form;
- actor-time/source-time alignment;
- multiplicity semantics;
- crosswalk/normalization authority if any;
- exact predicate grammar.

Allowed D15 projection forms remain exact equality, governed crosswalk, range/band containment, governed geography hierarchy, source-specific construct equivalence, temporally conditional equivalence, or explicit noncomparability.

Fuzzy matching and population imputation remain forbidden.

## 7. Typed absence / failure

Keep D15 semantic comparator outcomes:

- `ACTOR_PROPERTY_MISSING`;
- `NO_COMPARATOR`;
- `AMBIGUOUS_COMPARATOR`;
- `TEMPORAL_NONCOMPARABLE`.

SV3B also recommends pre-semantic integrity blockers for missing owner authority, snapshot hash mismatch, comparator-rule hash mismatch and unresolved currentness. These must not collapse into actor-property values.

Explicit fact-owner absence, when a fact owner lawfully supports such an assertion, remains different from missing.

`NOT_REQUESTED` is also distinct from missing at the snapshot layer.

## 8. Source applicability boundary

Comparator success is not source admission.

`SERVICE_SOURCE_APPLICABILITY_AUTHORITY` remains a later/separate gate. If it rejects the universe, there is no automatic regional/global backfill.

## 9. Receipt role

`ActorComparatorReceipt` remains:

```text
semantic input to PossibilityFieldService
transitive provenance/replay only in V3
```

It must not become:

- V3 developmental prior;
- actor propensity score;
- actor fact source;
- V2/application persona/expression authority.

## 10. Parent integration requests

SCRV3 should decide/freeze the final names and machine schemas, but should preserve these invariants:

1. reference-only query-minimal snapshot, not full actor state;
2. owner authority + fact hash + effective-time/currentness proof on every positive binding;
3. requested slots and typed missing/blocked records are identity-bearing;
4. fact existence and comparator eligibility are distinct gates;
5. exact comparator rule must name source coordinate/universe/time and multiplicity semantics;
6. no generic structural-position bridge;
7. no source-label/population/prevalence/nearest-cohort fact invention;
8. no belief/memory/knowledge/persona/response/perceived-relationship conditioning;
9. same-respondent conjunction for multi-property predicates;
10. comparator receipt provenance-only downstream of field production in V3.

## 11. Files supplied

- `RESULT.md`
- `RESULT.json`
- `OBJECTIVE_FACT_ELIGIBILITY_MATRIX.csv`
- `SNAPSHOT_IDENTITY_CANDIDATE.md`
- `PROJECTION_CONTRACT.md`
- `HOSTILE_FIXTURES.md`
- `PARENT_HANDOFF.md`

## 12. Unknowns intentionally not invented

- concrete positive per-source comparator-rule registry entries for every D15 candidate family;
- missing domain fact owners for several candidate demographic/biographical properties;
- final SCRV3-selected snapshot schema name/version;
- final SCRV3 integration with its PSEPF lifecycle/metabolism contract.

These unknowns do not require a broad-DAG amendment because the accepted architecture already defines fail-closed behavior when facts or comparator authority are absent.
