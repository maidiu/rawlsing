# D15 — REVERSE POSITIONED-SUBJECT ARCHITECTURE

## 1. Target object

The target object is:

`PositionedSubjectEmpiricalPossibilityField`

with semantic form:

```text
P(Q1,...,Qk
  | exact lawfully comparable generated-subject empirical properties,
    exact source/historical scope)
```

It is population empirical possibility geometry. It is not actor belief, psyche, persona, identity, memory, knowledge, response or generated structural position.

## 2. End-to-end path

```text
objective generated actor fact(s)
        ↓ exact fact owner/reference
ActorComparabilityService
        ↓
ActorComparatorReceipt(s)
        ↓
exact empirical conditioner predicate AST
        + SERVICE_SOURCE_APPLICABILITY_AUTHORITY
        ↓
admitted EmpiricalUniverse(s)
        ↓
EmpiricalQueryEngine
        ↓
exact conditional unary/J-way EmpiricalFact per universe
        ↓
support + uncertainty method/state + source provenance
        ↓
PositionedSubjectEmpiricalPossibilityField[source-indexed]
        ↓
V3EmpiricalPossibilityInput
        ↓
V3 developmental metabolism
```

## 3. Actor facts eligible for comparison

Only objective generated demographic/biographical facts with an accepted actor-side owner may enter comparator resolution. Candidate families may include age/time, sex/gender where source semantics permit, education, household facts, resources/income, employment, language, religion/sect self-identification, ethnicity, region/locality, urban/rural, marital/household state, migration/travel and occupation.

Listing a family does not create a comparator. Every field/source/time relation needs its own authority.

Generated structural position is not a generic comparator key.

Actor belief, memory, self-report generated later, or current simulated response cannot be retroactively used as objective comparator absent separate explicit authority.

## 4. Comparator resolution

Allowed rule forms:

- exact value equality;
- versioned normalization/crosswalk;
- range/band containment;
- historically governed geographic hierarchy;
- source-specific construct equivalence;
- temporally conditional equivalence;
- explicit not-lawfully-comparable.

Each positive receipt binds:

- actor fact ref/hash + fact owner;
- effective actor time;
- comparator authority ID/version/hash;
- target EmpiricalUniverse and coordinate identity;
- exact resolved predicate AST/hash;
- match cardinality and any semantic transformation.

No global comparator mode exists.

## 5. Fail-closed comparator states

### Actor property missing

Return `ACTOR_PROPERTY_MISSING`. Population prevalence is not a lawful imputation of the actor.

### No comparator

Return `NO_COMPARATOR`. No fuzzy string, semantic guess, nearest geography or structural-position substitution.

### Ambiguous comparator

Return `AMBIGUOUS_COMPARATOR`. Do not explode a Cartesian set of plausible mappings unless a separate authority explicitly requests multiple alternative fields.

### Temporal mismatch

Return `TEMPORAL_NONCOMPARABLE` where the actor fact and survey construct cannot be lawfully aligned.

## 6. Source applicability

Comparator success does not itself authorize a source for reverse inference.

`SERVICE_SOURCE_APPLICABILITY_AUTHORITY` evaluates whether a respondent universe is admissible for the target actor/query/time/population context.

Multiple admitted universes remain source-indexed. Locality does not automatically make a source superior, and a broader regional/global source is not an automatic backfill.

## 7. Exact conditioning

Multiple actor properties create one exact conjunction over respondent-coordinate incidence. The engine may not multiply independent marginal filters/probabilities as a substitute for same-respondent conjunction.

The risk set is independently governed and exact. Routing/applicability is part of the denominator.

## 8. Target response field

For target arity `J`:

- `J=1`: exact conditional distribution;
- `J=2`: complete exact pair contingency;
- `J>2`: complete exact requested J-way support/mass.

Sparse physical representation is allowed when response domains are exact, all occupied cells are preserved and observed-zero states are inferable without truncation. Pairwise marginals cannot replace a requested J-way field.

## 9. Support / uncertainty semantics

Every field component carries:

- raw selected respondent support/denominator;
- raw configuration support;
- governed weighted mass when authorized;
- weight/design basis;
- low-support state;
- numeric uncertainty method + authority where governed, otherwise `UNCERTAINTY_UNQUANTIFIED`;
- exact risk-set/topology/provenance.

`LOW_SUPPORT` means supported but weak/uncertain, not impossible.

`OBSERVED_ZERO` means no observation in the exact supported risk set, not metaphysical impossibility.

`ZERO_SUPPORT` for the conditioner means no empirical conditional basis. It terminates without nearest-cohort fallback.

## 10. Target unavailable / routing states

If a target question does not exist in the admitted universe, return `TARGET_UNAVAILABLE` for that source.

If target observability is governed by routing, the field uses the exact routed risk set and preserves not-asked/inapplicable states. An unanswered target is never silently treated as a substantive zero.

## 11. Multiple source universes

Default output is a set/map:

```text
PositionedSubjectEmpiricalPossibilityField {
  source_components: [
    {universe_id: U1, exact_field: ...},
    {universe_id: U2, exact_field: ...}
  ],
  comparison_state: AGREEMENT | DISAGREEMENT | NONCOMPARABLE | NOT_REQUESTED,
  composition: NONE_BY_DEFAULT
}
```

No numeric weighted average is required. A later source composition authority may define a specific estimand, but generic composition remains absent.

## 12. Source disagreement

When source components disagree, the field preserves each component and an exact comparison state. Disagreement is information and may constrain V3 differently from apparent consensus, but V3 still cannot read disagreement as a belief assignment.

## 13. k-way sparse fields

Large J-way state spaces may be represented as:

- exact domain metadata per target;
- every occupied supported configuration + mass/support;
- exact denominator/risk-set;
- explicit truncation flag fixed to false for canonical exact field;
- observed-zero derivation semantics.

Top-k truncation is not a canonical field.

## 14. V3 boundary

The field enters V3 only through `V3EmpiricalPossibilityInput` under `V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY`.

The boundary exposes:

- source-indexed configuration geometry;
- support/uncertainty;
- actor comparator receipts;
- historical/source scope;
- exact field identity;
- negative/typed states.

It exposes no actor belief or response field.

## 15. V3 metabolism constraints

The new authority may let empirical possibility geometry constrain selection/proposal among otherwise lawful developmental possibilities only in conjunction with actual V3 state/history.

It must preserve V3 ownership of:

- opportunity and encounter availability;
- actual exposure;
- relationships and household history;
- mediation;
- actor action and prior consequences;
- knowledge/accessibility;
- memory;
- belief formation/change;
- path dependence;
- explicit lawful randomness.

The field cannot bypass these.

A simple direct rule such as `actor.belief_probability = field.mass` is forbidden.

## 16. Same field, different lives

A mandatory V3 fixture creates two actor histories with the same structural context and same empirical possibility field but different subsequent encounters/relationships/events. The architecture passes only if lawful divergence in later belief/action/attractor state remains possible and causally attributable to those histories.

## 17. Replay

A historical reverse field replay binds:

- exact actor objective fact refs/hashes + effective time;
- comparator authority snapshots and receipts;
- source applicability authority;
- admitted EmpiricalUniverses;
- exact EmpiricalQuerySpec;
- C11 content identity;
- uncertainty method authority;
- field producer version.

V3 replay additionally binds the metabolism authority and actual V3 causal history/randomness.

## 18. What does not survive from historical profile machinery

The historical intuition that demographics + same-person response geometry constrain plausible joint configurations survives.

The historical shortcut from that geometry to a finished profile/persona does not.

`PositionedSubjectEmpiricalPossibilityField` is therefore a lawful replacement for the empirical **possibility geometry**, not a renamed persona object.
