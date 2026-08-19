# SV3B — HOSTILE FIXTURES

**Authority:** `NON_DISPOSITIVE_TO_SCRV3`  
**Target seam:** objective actor fact snapshot -> `ActorComparabilityService` -> `ActorComparatorReceipt`.

The fixtures are contract oracles, not production tests.

## HF01 — missing sex/gender fact + source prevalence

**Setup:** source coordinate is sex/gender; actor has no independently owned current fact. Source population is 55% category A.

**Attack:** fill the actor fact from population prevalence.

**Required:** `ACTOR_PROPERTY_MISSING`. Zero comparator predicate. No draw, modal fill, or prevalence imputation.

## HF02 — source label manufactures actor fact

**Setup:** source coordinate label is `urban`; actor snapshot has no exact region/urban fact.

**Attack:** create actor `urban=true` from the coordinate name or source applicability.

**Required:** `ACTOR_PROPERTY_MISSING`. Coordinate semantics never create actor truth.

## HF03 — ADP-009 position label matches survey label

**Setup:** exact current `V3StructuralPositionFact` has a label resembling the empirical coordinate.

**Attack:** map it by string equality without a comparator rule naming the ADP-009 fact class/dimension/source/time.

**Required:** `NO_COMPARATOR`.

## HF04 — exact ADP-009 fact + exact comparator rule

**Setup:** exact current ADP-009 fact; comparator authority explicitly names that fact kind/owner, target universe/coordinate, semantic mapping and time alignment.

**Required:** positive comparator receipt with exact fact ref/hash, owner authority, rule, source coordinate and predicate AST. The fixture proves conditional use, not generic structural-position eligibility.

## HF05 — stale structural position

**Setup:** fact was current at t1 and ended before snapshot time t2.

**Attack:** use the immutable old fact as the “latest known” value.

**Required:** no positive projection. Snapshot records missing/noncurrent state; no nearest-prior carry-forward without exact temporal authority.

## HF06 — temporal mismatch

**Setup:** actor fact is current at actor time t2; source construct is only lawfully comparable to a different historical scope and no alignment rule bridges them.

**Required:** `TEMPORAL_NONCOMPARABLE`.

## HF07 — household membership does not imply marital status

**Setup:** actor has exact current `V3HouseholdMembershipFact`; source asks marital status.

**Attack:** infer married/cohabiting from household membership.

**Required:** `NO_COMPARATOR` unless an exact rule explicitly maps the relevant household/relationship semantics.

## HF08 — perceived relationship state as objective fact

**Setup:** actor has `V3ActorPerceivedRelationshipState` but no exact objective relationship status fact for the requested construct.

**Attack:** use the perceived state as the objective comparator property.

**Required:** hard reject / `ACTOR_FACT_CLASS_NOT_ELIGIBLE`; no positive receipt.

## HF09 — two concurrent household memberships

**Setup:** two exact current household memberships; comparator rule expects exactly one household category and supplies no multiplicity semantics.

**Attack:** choose first/newest/highest-score membership.

**Required:** `AMBIGUOUS_COMPARATOR`. Preserve both facts.

## HF10 — explicit multiplicity rule

**Setup:** two current household memberships; comparator rule explicitly defines `SET_MEMBERSHIP_ANY` for a specific respondent coordinate.

**Required:** deterministic exact predicate under that rule, with both fact refs retained in receipt provenance.

## HF11 — parenthood implies marriage

**Setup:** exact `V3ParenthoodFact`; no objective marital fact.

**Attack:** infer marriage or cohabitation.

**Required:** `NO_COMPARATOR`.

## HF12 — CAN-009 money capacity as income

**Setup:** actor has `MATERIAL_MONEY_CAPACITY`; source asks household/personal income band.

**Attack:** compare normalized numeric ranges or bin the capacity value as income.

**Required:** `NO_COMPARATOR` absent exact source-specific construct-equivalence authority.

## HF13 — job insecurity as employment status

**Setup:** actor has `MATERIAL_JOB_INSECURITY` but no separately owned employment-status fact.

**Attack:** infer employed/unemployed/labor-force category.

**Required:** `ACTOR_PROPERTY_MISSING` or `NO_COMPARATOR`; no semantic substitution.

## HF14 — developmental phase as age

**Setup:** actor has an ADP-008 developmental phase and ADP-021 effective time; no exact age/chronology fact accepted for comparator use.

**Attack:** infer source age band from phase label.

**Required:** `ACTOR_PROPERTY_MISSING` / `NO_COMPARATOR`.

## HF15 — belief as religion self-identification

**Setup:** actor has an ADP-017 belief concerning religion; no objective self-identification fact owner has emitted a comparator-eligible fact.

**Attack:** map belief to survey religion/sect coordinate.

**Required:** hard reject as `DENIED_NON_OBJECTIVE_COMPARATOR_SOURCE`.

## HF16 — memory as employment biography

**Setup:** actor remembers working at a place; no exact objective employment fact is current.

**Attack:** use memory content as employment coordinate.

**Required:** hard reject. Memory is not objective fact authority.

## HF17 — knowledge as demographic fact

**Setup:** actor knows a proposition about self; objective fact registry does not independently contain that demographic fact.

**Attack:** treat knowledge as proof of the fact.

**Required:** hard reject. Epistemic stance is not objective fact ownership.

## HF18 — rendered persona as source coordinate

**Setup:** V2 says the actor sounds working-class/religious/urban.

**Attack:** project style/persona into empirical coordinates.

**Required:** hard reject; V2/application is outside comparator fact authority.

## HF19 — current simulated response as conditioner

**Setup:** actor gives a current answer to target or related question.

**Attack:** use the response to choose the comparator cohort for the same reverse field.

**Required:** hard reject absent separate explicit authority; no circular response->conditioner promotion.

## HF20 — ADP-019 caller assertion

**Setup:** external statement says “I am married.” ADP-019 admits only the occurrence of the assertion as an external event.

**Attack:** treat assertion content as objective marital fact.

**Required:** no comparator fact. A separate V3 objective fact owner must independently establish the proposition.

## HF21 — nearest cohort fallback

**Setup:** required education fact missing.

**Attack:** choose a nearby cohort based on known region/age or population majority.

**Required:** `ACTOR_PROPERTY_MISSING`; no weakened predicate.

## HF22 — fuzzy label substitution

**Setup:** actor fact value and source coordinate value are similar but not connected by an exact crosswalk.

**Attack:** use string similarity, embeddings or LLM semantic match.

**Required:** `NO_COMPARATOR`.

## HF23 — ambiguous crosswalk

**Setup:** exact actor fact maps to two source categories under an incomplete crosswalk and the rule provides no multi-alternative semantics.

**Required:** `AMBIGUOUS_COMPARATOR`, not Cartesian field explosion.

## HF24 — exact historical crosswalk

**Setup:** versioned source/time-specific crosswalk produces exactly one coordinate predicate.

**Required:** positive receipt binds exact crosswalk authority/version/hash and historical scope.

## HF25 — source applicability after comparator success

**Setup:** comparator mapping succeeds, but `SERVICE_SOURCE_APPLICABILITY_AUTHORITY` rejects the source universe for the target reverse inference.

**Attack:** treat comparator success as source admission.

**Required:** no field from that source; preserve separate source nonapplicability. No broader-source automatic backfill.

## HF26 — multi-property conjunction with one missing property

**Setup:** rule/query requires region AND household state; region maps positively, household state missing.

**Attack:** drop the missing condition and run region-only field.

**Required:** no exact requested conjunction; typed failure unless query authority explicitly declared the property optional.

## HF27 — independent marginals masquerade as same-person conjunction

**Setup:** two comparator predicates individually map.

**Attack:** multiply marginal probabilities instead of querying same-respondent conjunction.

**Required:** reject; exact conjunction over respondent incidence is required.

## HF28 — snapshot hash mismatch

**Setup:** snapshot ref resolves to content with different hash.

**Required:** `SNAPSHOT_HASH_MISMATCH`; no repair or latest snapshot substitution.

## HF29 — missing fact-owner authority

**Setup:** fact record/hash exists but its owner authority version/hash is missing or unresolvable.

**Required:** `FACT_OWNER_AUTHORITY_MISSING`; no positive comparator use.

## HF30 — missing comparator authority

**Setup:** objective fact exists and is current; no exact comparator rule for requested source coordinate.

**Required:** `NO_COMPARATOR` or explicit missing comparator authority; fact existence does not authorize mapping.

## HF31 — comparator rule hash mismatch

**Setup:** rule ID/version resolve but content hash differs.

**Required:** integrity failure; no latest-version substitution.

## HF32 — hidden wall clock

**Setup:** identical semantic inputs replay on a later real-world day.

**Required:** identical snapshot/projection outcome. Wall clock is not actor/source effective time.

## HF33 — same snapshot/rule replay

**Setup:** exact snapshot, rule, universe, coordinate and temporal alignment repeat.

**Required:** deterministic same receipt identity/result or exact idempotent equivalent.

## HF34 — actor fact changes after historical snapshot

**Setup:** snapshot S1 at t1 is valid; actor fact changes at t2.

**Attack:** mutate S1 or treat it as current at t2.

**Required:** S1 remains immutable historical evidence; a new snapshot S2 is required for a t2 request.

## HF35 — explicit absence versus missing

**Setup:** an accepted fact owner supports an explicit absence assertion and has emitted it; another actor has no fact.

**Required:** explicit absence and missing remain distinct. Comparator may map explicit absence only if its rule permits; missing yields `ACTOR_PROPERTY_MISSING`.

## HF36 — ActorComparatorReceipt direct V3 prior

**Setup:** positive comparator receipt exists.

**Attack:** insert receipt into V3 as a developmental prior or propensity score.

**Required:** reject. V3 may reach it only transitively for provenance/replay behind the PSEPF/intake path.

## HF37 — comparator receipt to V2

**Attack:** expose comparator coordinate/mapping to V2 to select voice/persona.

**Required:** reject; no expression authority.

## HF38 — source disagreement creates actor fact

**Setup:** two sources disagree about population distributions.

**Attack:** choose the stronger source and write its modal category into actor snapshot.

**Required:** impossible by contract; source evidence cannot write actor facts.

## HF39 — snapshot includes full actor state

**Attack:** serialize ActorCausalState into comparator snapshot and allow downstream filtering over arbitrary keys.

**Required:** reject. Snapshot is query-minimal allowlist of requested objective fact refs only.

## HF40 — unrequested slot treated as absent

**Setup:** snapshot was created only for household state.

**Attack:** infer that education is missing because no education binding appears.

**Required:** reject. Unrequested fact class is `NOT_REQUESTED`, not `ACTOR_PROPERTY_MISSING`.

## Oracle summary

A hostile suite passes only if:

```text
fact absence never becomes imputation
objective truth never becomes generic comparator permission
source labels never manufacture actor truth
semantic similarity never substitutes for authority
currentness is owner/time-bound
multiplicity is preserved unless exact rule resolves it
source applicability stays separate
ActorComparatorReceipt never becomes V3/V2 behavioral authority
```
