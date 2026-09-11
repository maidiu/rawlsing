# R3 FINAL REVIEW — RULE AND REALIZATION AUTHORITY COURT R1

STATUS: `PASS_WITH_NARROWING__WITNESS_VALIDITY_AND_POLARITY_LAW_REQUIRED`

FROZEN R3 TARGET: `3e1c72b49e28485a5bd39e5b09e0d418420f49a4`

## 1. Questions before the court

This court tested two independent safeguards:

1. whether `MECHANISM_RULE_REF` is authoritative enough to prevent free-form social interpretation from becoming actor truth; and
2. whether `REALIZATION_WITNESS` is strong enough to prevent applicability, stale evidence, missing evidence, or source-rule validity from masquerading as an active/realized actor consequence.

The first passes. The second requires one exact hardening.

## 2. `MECHANISM_RULE_REF` authority verdict

R3 requires a rule reference with, at minimum:

- `RULE_ID`
- `RULE_VERSION`
- `COMPETENT_OWNER/AUTHORITY_REF`
- `MECHANISM_CLASS`
- `ALLOWED_INPUT_TYPES`
- `REQUIRED_BINDINGS`
- `OUTPUT_CONSEQUENCE_TYPES`
- qualification/applicability law
- `REALIZATION_WITNESS_SCHEMA`
- temporal/lifecycle requirements
- context/institution/historical validity
- boundary conditions
- source/claim status
- portability scope
- calibration status when relevant
- negative ceiling

This is sufficient as a semantic authority contract **provided the runtime/HQ implementation refuses unregistered or authority-incompatible rules**. It prevents a theory label, category label, analyst intuition, correlation, group probability, or source quotation from being treated as a free-standing actor-level causal rule.

`MECHANISM_RULE_REF VERDICT: PASS__AUTHORITY_CONTRACT_IS_ADEQUATE_AT_THE_CONSTITUTIONAL_LEVEL`

No sixth rule primitive is required.

## 3. Qualification is not realization

The following ladder is binding:

```text
RULE EXISTS
!= INPUTS MATCH RULE TYPES
!= ACTOR/POSITION/CONTEXT/TIME BINDINGS SATISFY APPLICABILITY
!= GATE/CHANNEL/TASK/RESOURCE/RELATION IS ENCOUNTERED OR ACTIVE
!= CONSEQUENCE IS REALIZED
!= CONSEQUENCE IS PHENOMENALLY AVAILABLE
!= PERSON TAKES IT UP / APPRAISES IT / RESPONDS
```

A legal entitlement may be valid while payment never arrives. A formal authority scope may exist while the task is never performed. A care tie may exist while no assistance is exchanged. A gate may apply while no decision has yet occurred.

R3 correctly requires a competent realization witness for an `ACTIVE/REALIZED` assertion.

## 4. Counterfeit tests

### Counterfeit A — source rule remains valid after witness expiry

Suppose a rule continues to authorize a recurring transfer, but the last receipt witness covered only a prior interval. The rule's continued validity cannot keep the transfer `ACTIVE/REALIZED` now.

Current R3 has lifecycle and witness-schema fields, but it does not state the global overlap/currentness rule with enough force to exclude stale-witness carry-forward in every class.

### Counterfeit B — superseded witness

A source records an active authority relation, then a later competent source records termination. The earlier witness must no longer sustain current active authority even if the underlying institutional rule remains unchanged.

### Counterfeit C — missing positive evidence becomes negative

A household has no current payment record. That proves neither denial nor non-receipt unless the competent source and rule establish a closed/complete observation or an explicit denial/non-occurrence fact.

### Counterfeit D — negative result inferred from expired evidence

An expired positive witness may lower current epistemic status to unknown/not-proven-realized. It cannot create a negative consequence.

### Counterfeit E — recurrent practice from one old observation

One observed instance of a task cannot sustain a claim of current recurrent activity across an interval unless the rule's witness schema defines adequate recurrence coverage/freshness.

These counterfeits expose one real constitutional gap, not a new mechanism class.

## 5. Exact required narrowing

R3 must add the following universal realization-witness law, or semantically equivalent binding language:

> **UNIVERSAL REALIZATION-WITNESS VALIDITY / POLARITY LAW.** Every `ACTIVE` or `REALIZED` consequence assertion MUST cite at least one type-compatible competent realization witness whose validity overlaps the asserted consequence interval and that is not expired, superseded, terminated, invalidated, or otherwise outside the rule's lifecycle requirements. For recurrent-activity or continuing-state claims, the witness schema MUST define sufficient coverage/currentness/freshness for the interval asserted. Rule validity or qualification alone MUST NOT extend a realization witness. Missing, expired, superseded, invalidated, or insufficiently current positive evidence yields `UNKNOWN` / `NOT_PROVEN_REALIZED`, never a negative consequence. A denial, absence, non-occurrence, termination, unavailability, or other negative actor fact may be emitted only from explicit competent negative evidence, an explicit denial/termination witness, or a rule-authorized closed-world observation whose negative semantics are itself provenance-bearing.

The same rule should be reflected in `MECHANISM_RULE_REF.REALIZATION_WITNESS_SCHEMA` by requiring, where applicable:

```text
WITNESS_TYPE
WITNESS_POLARITY
COMPETENT_SOURCE / OWNER
VALID_FROM / VALID_TO or event time
CURRENTNESS / FRESHNESS REQUIREMENT
SUPERSESSION / TERMINATION / INVALIDATION STATUS
RECURRENCE_COVERAGE where recurrent truth is asserted
ASSERTED_CONSEQUENCE_INTERVAL
```

This is a narrowing/hardening of R3, not a sixth primitive, not a new D-lane, and not production runtime implementation.

## 6. Missing evidence / negation firewall

After the narrowing above:

```text
NO EVIDENCE != NEGATIVE EVIDENCE
MISSING POSITIVE WITNESS != DENIAL
EXPIRED WITNESS != NON-OCCURRENCE
RULE VALIDITY != CURRENT REALIZATION
QUALIFICATION != RECEIPT / TREATMENT / CONTACT / PERFORMANCE
```

`MISSING-EVIDENCE/NEGATION VERDICT: PASS_WITH_NARROWING__GLOBAL_POLARITY_AND_CURRENTNESS_LAW_REQUIRED`

## 7. Court verdicts

`REALIZATION_WITNESS VERDICT: PASS_WITH_NARROWING__CURRENTNESS_OVERLAP_SUPERSESSION_AND_POLARITY_MUST_BE_GLOBAL`

`EXACT REQUIRED CORRECTION: ADD THE UNIVERSAL REALIZATION-WITNESS VALIDITY/POLARITY LAW ABOVE; DO NOT OTHERWISE EXPAND R3.`

The defect is small enough for `PASS_WITH_NARROWING`, but exact enough that R3 should not be considered final without the correction.