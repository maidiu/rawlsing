# S3 R4 CYCLE AND ITERATION COURT R1

STATUS: `DEFAULT_ACYCLICITY_AND_LAWFUL_ITERATION_BOUNDARY_SPECIFIED`

This court addresses only derivation safety for D1'. It creates no fixed-point engine, cumulative-disadvantage scalar, D2 owner, D3 owner, or runtime solver.

---

## 1. Default cycle law

The required default law is:

```text
NO D1' DERIVED FACT AT A GIVEN WORLD/STATE VERSION AND VALID-TIME SLICE
MAY BE ITS OWN ANCESTOR.
```

Equivalently, absent explicit competent iterative authority, the direct determinant graph for one asserted state slice must be acyclic.

Forbidden:

```text
A(t,v) -> B(t,v) -> A(t,v)
```

where the second `A` is being used to support the same factual state/version that began the chain.

This prohibition is semantic, not a demand for a particular cycle-detection implementation.

---

## 2. Why same-time self-support fails

Two individually plausible rules do not jointly create authority for circular truth.

### Resource example

```text
resource scarcity(t)
-> exit constraint(t)
-> resource scarcity(t)
```

The second edge may describe reinforcement in ordinary language, but it cannot retroactively supply the antecedent truth needed for the first application at the same state slice.

### Authority example

```text
authority(t)
-> obligation(t)
-> authority(t)
```

An obligation may arise from authority, but the derived obligation cannot constitute the very authority fact used to derive it unless a separate competent constitutive rule and independent determinant establish a later/new state.

### Support example

```text
support channel(t)
-> support relation(t)
-> support channel(t)
```

A channel and a realized support relation are distinct assertion kinds. Neither may bootstrap the other without independent source-owned relation/witness authority.

---

## 3. Fact identity for cycle purposes

Cycle testing concerns semantic state identity, not merely textual fact names.

Minimum identity includes the applicable subset of:

```text
ACTOR_REF
CONSEQUENCE_TYPE
WORLD/CONTEXT
COUNTERPART/POSITION when constitutive
VALID_TIME_OR_INTERVAL
STATE_VERSION / SOURCE VERSION where applicable
```

A later fact of the same type is not automatically the same node.

Thus:

```text
RESOURCE_STATE_t1 -> ACTION/EXTERNAL_RESPONSE_t2 -> RESOURCE_STATE_t3
```

can be lawful because the later resource state has a new external determinant and a later state/time identity.

---

## 4. Lawful iterative processes

An iterative/cumulative process remains lawful only if each step is anchored by at least one genuine advancement condition:

```text
TIME ADVANCES;
STATE/SOURCE VERSION ADVANCES;
A NEW EXTERNAL SOURCE-OWNED FACT ENTERS;
A NEW TYPE-COMPATIBLE WITNESS ENTERS;
OR AN EXACT COMPETENT ITERATION/FIXED-POINT OWNER EXPLICITLY AUTHORIZES THE PROCESS.
```

S3 does not create the last kind of owner and found no basis to assume one generically.

---

## 5. Typed cumulative process law

The R4 candidate already permits `CUMULATIVE PROCESS [typed iteration]` as a temporal form without creating D2. S3 sharpens the derivation condition:

```text
STATE_t
+ CURRENT RULE
+ NEW/ADVANCED DETERMINANT_t+1
-> STATE_t+1
```

Each iteration must have its own producing rule-application identity and direct determinants.

Forbidden shortcut:

```text
CUMULATIVE DISADVANTAGE
-> MORE CUMULATIVE DISADVANTAGE
```

unless decomposed into domain-specific objective facts and separately governed updates.

---

## 6. Same-time constitutive chains

Acyclic same-time chains remain lawful:

```text
OPERATIVE RULE + POSITION
-> ELIGIBILITY
-> QUALIFIED ACCESS ROUTE
```

provided:

- each output is a distinct fact;
- every rule application cites direct independent determinants;
- no output appears in its own ancestry;
- contingent realization is not smuggled in from qualification.

Therefore S3 does not require time to advance after every derivation edge. It requires ancestry to advance without self-support.

---

## 7. Explicit iteration authority boundary

If a future competent project owner defines an iterative/fixed-point semantics, that owner must specify at minimum:

```text
ITERATION AUTHORITY REF
STATE IDENTITY
INITIAL EXOGENOUS/INDEPENDENT SEED CONDITIONS
UPDATE RULE
CONVERGENCE/TERMINATION OR BOUNDED-STEP LAW
EVIDENCE/AUTHORITY CEILING
CYCLE SAFETY / NONSELFBOOTSTRAP CONDITION
```

S3 does not authorize or implement such an owner. In its absence the default DAG law controls.

---

## 8. Reciprocal social-developmental loops

The broader developmental pattern remains compatible with the cycle law:

```text
D1' OBJECTIVE CONSEQUENCE_t
-> V3 uptake/action under existing V3 authority
-> EXTERNAL ACTION OCCURRENCE_t+1
-> COMPETENT EXTERNAL RESPONSE
-> SOURCE OWNER AUTHORS NEW WORLD FACT_t+2
-> D1' INVALIDATION/REDERIVATION
-> NEW OBJECTIVE CONSEQUENCE_t+2
```

This is not a D1' circular derivation because the world fact at `t+2` is newly authored by a competent external owner.

Direct:

```text
D1' FACT -> V3 ACTION -> D1' FACT
```

without the external occurrence/response/source-owned world fact remains forbidden.

---

## 9. Court verdict

```text
DEFAULT: DIRECT D1' DERIVATION GRAPH IS ACYCLIC WITHIN ONE FACTUAL STATE/TIME SLICE.
ITERATION: LAWFUL ONLY THROUGH TIME/STATE ADVANCEMENT, NEW EXTERNAL FACT/WITNESS,
OR EXPLICIT COMPETENT ITERATION AUTHORITY.
NO GENERIC SOLVER OR RECURSIVE SCALAR IS CREATED.
```
