# PYAT HQ120-J2 — CERTIFICATION-CONTRIBUTION SUCCESSION

## 1. Historical function

Historical V551J v2.2.3 did not merely carry a generic “role” string.

For each component it first determined exact V551 match/evidence conditions and then derived a contribution class.

The effective rule is:

```text
if exact/accepted match
   and component is relation-like
   and component is allowed as V551 relation evidence:
       relation_component
elif unmatched special/missing:
       special_or_missing_component
elif unmatched relation-ineligible/context/nonrelation:
       explained_nonrelation_component
elif matched:
       context_component
elif ambiguous:
       blocked_component
else:
       unresolved_component
```

The implementation emitted that token in both:

- `component_evidence_role`;
- `component_certification_contribution`.

At v2.2.3 those are two carrier names for the same derived classification.

## 2. Why it is constitutive

The packet-status function consumes `component_certification_contribution` directly.

It computes:

- `relation_count`;
- `context_count`.

It then:

- blocks if an `unresolved_component` exists;
- refuses joint-relation certification if `relation_count < 2`;
- distinguishes certified joint evidence with context from certified joint evidence without context.

Therefore the contribution vector is a **determinant of certification**, not decorative provenance.

It cannot be replaced by:

- component order;
- component presence;
- authority state alone;
- overall packet certification status;
- product lifecycle state;
- publication/current selection;
- a generic participant-role string.

## 3. Current M1 relationship

M1 is the correct present generic jurisdiction for the *act* of learned empirical adjudication.

An exact M1 family rule can specify:

- the claim family/rule;
- exact validator authority;
- exact current-selection authority where applicable;
- exact input families/states;
- prerequisite channels;
- source-relation requirements;
- measure/weight/estimand requirements;
- coverage requirements;
- validator parameters;
- replay contract;
- output semantic ceiling.

The validator is dispatched by exact immutable binding identity.

This architecture can replace the historical fact that “V551J packet code itself performs certification.”

But that does **not** yet replace the historical contribution semantics.

At the current head no exact M1 family binding/validator was found that:

- binds the historical family-item/evidence role authority;
- classifies components into the historical contribution states or an explicitly adjudicated successor vocabulary;
- consumes that classification in a certification decision;
- freezes the per-component contribution determinant in replayable output.

Thus:

`M1_CAN_OWN_CURRENT_CERTIFICATION_ACT`

does not imply:

`HISTORICAL_COMPONENT_CONTRIBUTION_FUNCTION_HAS_CURRENT_SUCCESSOR`.

## 4. Why B5 cannot retire this function

B5 operates later.

It owns product lifecycle:

- registration;
- publication;
- current selection;
- supersession;
- withdrawal/invalidation;
- historical retention;
- rebuild eligibility.

The V551J contribution classification answers a different question:

> what evidentiary/certification function does each component have inside this candidate joint-evidence object?

B5 answers:

> what is the lifecycle/currentness state of an already producer-owned learned product/release?

Those are not interchangeable semantic acts.

## 5. Exact retirement condition

The separate historical **field** `component_certification_contribution` can be retired only when one current exact rule proves the function remains available.

A lawful retirement proof would need:

1. exact governed component identities and order;
2. exact family-item/evidence-role authority;
3. exact match/eligibility/negative state inputs;
4. exact current family validation rule;
5. deterministic per-component classification or an explicitly governed successor classification;
6. exact certification decision consuming that classification;
7. exact determinant/replay material from which the classification is recoverable;
8. no widening from context/special/blocked/unresolved into positive relation evidence.

If those are met, the old dataframe column need not survive.

At the current head they are not met.

## 6. Current disposition

`CURRENT_RULE_PRODUCER_CONSUMER_MAPPING_MISSING`.

The missing object is not B5 and is not a resurrected V551J packet.

The minimum closure is an exact J-role authority/mapping plus a family-specific M1 validation binding/validator, using the already-adopted component-vector receipt where an independently dereferenceable per-component vector is required.
