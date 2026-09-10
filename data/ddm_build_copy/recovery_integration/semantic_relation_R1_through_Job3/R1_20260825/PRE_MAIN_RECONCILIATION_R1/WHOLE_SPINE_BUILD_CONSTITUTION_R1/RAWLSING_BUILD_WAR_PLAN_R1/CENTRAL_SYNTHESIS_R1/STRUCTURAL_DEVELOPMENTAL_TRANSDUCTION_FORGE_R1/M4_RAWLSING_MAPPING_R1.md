# M4_RAWLSING_MAPPING_R1

STATUS: `M4_FROZEN_RAWLSING_MAPPING_COMPLETE_R1`

PRIMARY SOURCE: Klaus Holzkamp, *Grundlegung der Psychologie*.

RAWLSING BASIS USED:

- coordinator state: `f591dcea5fb2dfcdd16c05f88196e7155da9226b`
- frozen synthesis target: `9cf100a101e92891e2b4d0af0e308d27f7015a6b`
- frozen D1/D2/D3 candidate constitution and frozen coverage/disposition/temporal courts only.

No M1–M3 or M5–M11 return was consumed.

---

## 1. Governing mapping result

Holzkamp does **not** require Rawlsing to merge PRE-V3 and V3. The full source instead strengthens the jurisdictional firewall and supplies a more exact boundary:

```text
PRE-V3 / SDTF OBJECTIVE SIDE

objective societal fact / relation
-> objective meaning / structural possibility
-> exact actor position / life-situation / context qualification
-> typed actor-relative objective social fact / action possibility

================== BOUNDARY ==================

V3 SUBJECT SIDE

first-person / phenomenal givenness
-> subjective possibility space
-> premise
-> ground/reason
-> motive / refusal / coercion / decision
-> action / response
-> memory / learning / durable development if earned
```

The phrase `subject-relative` must therefore be used carefully. Holzkamp has both:

1. **objective possibilities relevant to a concretely positioned individual**, and
2. a genuinely **subjective possibility space** (`subjektiver Möglichkeitsraum`) constituted through phenomenal/biographical subject mediation.

Rawlsing must not use one object for both.

---

## 2. Source concept × Rawlsing owner crosswalk

| HOLZKAMP FUNCTION | SOURCE | PRE-V3 / CURRENT FROZEN BOOKEND | D1/D2/D3 ROLE | V3 RECEIVER / BOUNDARY | M4 JUDGMENT |
|---|---|---|---|---|---|
| objective historically produced social conditions | Ch. 5 pp. 191–203 | PRE-V3 structural/source facts, structural pressure/relations | D1 input | none yet | `REUSE` |
| objective societal meaning/action structures | Ch. 6 pp. 229–238 | structural possibility / route / topology / applicable social fact region | D1 input | none yet | `REUSE/GENERALIZE` |
| exact `Position` / `Lebenslage` specification | Ch. 5 pp. 195 ff; Ch. 7 pp. 358 ff | OBL032/031 actor/context evaluation + activation/world/time/context patterns | D1 required qualifier | later V3 actor identity/history remains separate | `GENERALIZE_EXISTING_BINDING_PATTERN` |
| life-situation-specific `Infrastrukturen` / meaning constellations | Ch. 7 pp. 358–367 | no general actor-relative ecology producer recovered in frozen matrix | D1 core derivation | no V3 state yet | `NEW_CONNECTIVE_SEMANTICS_REQUIRED` |
| objective action/thought possibility for actor/position | Ch. 6 pp. 233–238; Ch. 7 p. 359 | OBL059 narrow applicability pattern is closest frozen precedent | D1 output | V3 may later receive | `D1_SURVIVES` |
| actual subjective possibility space | Ch. 7 pp. 367–369 | **not PRE-V3 output** | D1 must stop before this | ADP-017 + CAN-010/011/008 region requires reconciliation | `V3_BOUNDARY_FUNCTION_REQUIRED` |
| `Prämisse` | Ch. 7 pp. 351–356, 367–369 | **not structural prerequisite/applicability** | not D1 output | V3 subject mediation | `BOUNDARY_RECONCILE` |
| subjective ground/reason | Ch. 7 pp. 348–356 | none | outside D1 | V3 subject-side response/motive/practice region | `V3_ONLY` |
| motivated/refused/coerced orientation | Ch. 7 pp. 315–324 | none | outside D1/D2 social derivation | CAN-008/010/011 region | `REUSE_V3_BOUNDARY` |
| realized action | Ch. 6–7 | external event/action admission boundary | D3 input only after externalization | V3 owns action project; social world owns realized external consequences | `D3_INTERFACE_REQUIRED` |
| relation/condition persistence | Ch. 5–7 | current state/binding/relationship fragments | D2 interval semantics | V3 history consumes effects | `GENERALIZE_EXISTING_OWNER` |
| prior realization/nonrealization shapes later possibility | Ch. 7 pp. 367–369; Ch. 8 | V3 history + social facts | D2 requalification | V3 biography and later D1 inputs must stay separated | `D2_STRENGTHENED` |
| institutional/context change changes possibility field | Ch. 8 pp. 473–493 | phase/world/context bindings are closest frozen pattern | D2 transition rebinding | later V3 premise/response after requalification | `GENERALIZE` |
| action reproduces/changes conditions | Ch. 5 p. 191; Ch. 7 | no general reciprocal world updater recovered | D3 | later D1/D2 consumes new social fact | `NEW_CONNECTIVE_SEMANTICS_REQUIRED` |
| collective association/counter-power | Ch. 7 pp. 354, 370–401 | topology/route possibility only | D3 collective gate | V3 actors retain separate motives/reasons | `D3_STRENGTHENED` |
| developmental persistence/change | Ch. 8 | PRE-V3 no jurisdiction | seam must preserve history-relevant facts only | V3 memory/history/practice/development | `REUSE_V3__NO_NEW_M4_OWNER` |

---

## 3. PRE-V3 end point after M4

The strongest Holzkamp-compatible PRE-V3/SDTF output is:

```text
ACTOR_RELATIVE_OBJECTIVE_SOCIAL_FACT {
  actor_ref,
  position_ref,
  life_situation/context_ref,
  world_ref,
  valid_time_or_interval,
  source_structural_refs,
  mechanism_family,
  output_type,
  counterpart_or_institution_ref where required,
  temporal_form,
  realization_status,
  provenance,
  boundary_conditions,
  negative_ceiling
}
```

Semantically this may state, for example:

- actor A is under authority relation R with supervisor B in interval T;
- actor A is eligible/ineligible under institution rule G;
- actor A has resource access/exit dependency of type X;
- actor A has a recurrent task obligation of type Y;
- actor A has a reachable counterpart/information/support route of type Z;
- actor A is subject to a schedule/time restriction;
- actor A is in an active persistent social condition.

It may **not** state merely from those facts:

```text
A EXPERIENCES X AS PREMISE
A BELIEVES X
A IS MOTIVATED BY X
A HAS RESTRICTIVE/GENERALIZED HANDLUNGSFÄHIGKEIT
A WILL ACT IN WAY Y
```

---

## 4. V3 ingress after M4

M4 recommends an explicit ingress contract:

```text
ACTOR_RELATIVE_OBJECTIVE_SOCIAL_FACT
        ↓
V3 ACCESS / FIRST-PERSON AVAILABILITY / PHENOMENAL PROCESSING
        ↓
POSSIBLE SUBJECTIVE PREMISE
        ↓
POSSIBLE REASON / MOTIVE / RESPONSE
```

Required invariants:

```text
OBJECTIVE_TRUTH != ACTOR_ACCESS
ACTOR_ACCESS != PHENOMENAL_GIVENNESS
PHENOMENAL_GIVENNESS != PREMISE
PREMISE != REASON
REASON != ACTION
```

The frozen matrix identifies ADP-017 as the strongest objective-truth/actor-knowledge/access firewall, with CAN-010/011/008 nearby for needs/practices/response. M4 does not claim one of these alone already implements Holzkampian premise formation; it requires post-review reconciliation.

---

## 5. D1 mapping after M4

### Keep

- typed mechanism family;
- exact actor binding;
- exact position/context/world/time;
- counterpart/institution identity where relational;
- provenance;
- distinct qualification vs realization status.

### Add/strengthen semantically

1. **Life-situation/context specification is not optional.** Holzkamp’s `Lebenslage` is not reducible to work position.
2. D1 output should be described as an **objective actor-relative fact/action possibility**, not a “subjective possibility.”
3. D1 should be able to preserve historically specific meaning/function of the relation rather than only a scalar severity.
4. D1 history input must not silently consume V3 psychological state.

### Prohibit

```text
D1 -> premise
D1 -> ground/reason
D1 -> motive
D1 -> restrictive/generalized agency classification
```

### M4 D1 status

`KEEP__NARROW_OUTPUT__STRENGTHEN_POSITION_LIFE_SITUATION_BINDING`.

---

## 6. D2 mapping after M4

The frozen temporal court already requires:

```text
ACTIVE_INTERVAL(condition/relation)
RECURRENCE(activity/practice)
REBIND(transition)
ORDERED_HISTORY(trajectory)
ITERATE(update, prior_history)(cumulative_process)
```

Holzkamp adds primary-source reasons to preserve:

- persistent social position/dependency/authority conditions;
- recurrent situated alternatives;
- biographical history of prior realization/nonrealization;
- developmental possibilities of progress/stagnation/regression;
- institution/context changes that reconfigure objective meaning/action possibilities.

### Critical boundary

D2 social-world rebinding and V3 subjective rebinding must remain separate:

```text
TRANSITION CHANGES OBJECTIVE ECOLOGY
!= SUBJECT IMMEDIATELY FORMS NEW PREMISE
```

### M4 D2 status

`KEEP__SEMANTICALLY_STRENGTHEN_HISTORY_SENSITIVE_REQUALIFICATION__NO_NEW_TEMPORAL_CARRIER_PROVED`.

---

## 7. D3 mapping after M4

Required Rawlsing chain:

```text
V3 ACTOR ACTION PROJECT
-> REALIZED EXTERNAL ACTION / EVENT
-> COORDINATION / ORGANIZATION WHERE REQUIRED
-> COUNTERPART / INSTITUTION / COLLECTIVE RESPONSE GATE
-> CAUSALLY ADMITTED CHANGED RELATION / POSITION / RULE / RESOURCE / NETWORK
-> NEW SOCIAL FACT WITH PROVENANCE
-> D2 REBIND / D1 RE-DERIVE LATER ACTOR ECOLOGY
-> V3 SUBJECT CONSEQUENCES ONLY THROUGH LATER INGRESS
```

Holzkamp supplies strong theoretical support for reciprocal direction and collective mediation. Rawlsing supplies the explicit provenance/admission protocol.

### M4 D3 status

`KEEP__STRENGTHEN_ASSOCIATION_ORGANIZATION_AND_EXTERNAL_RESPONSE_GATES`.

---

## 8. Objective possibility → premise boundary mapping

### What PRE-V3/D1 can safely say

```text
FACT F IS OBJECTIVELY APPLICABLE / RELEVANT / AVAILABLE / CONSTRAINING
FOR ACTOR A IN POSITION P, CONTEXT C, INTERVAL T
```

### What requires V3

```text
F IS GIVEN TO A AS PART OF A'S SITUATION
F ENTERS A'S SUBJECTIVE POSSIBILITY SPACE
F FUNCTIONS AS A PREMISE IN A REASON NEXUS
```

### Important qualification

“Given to A” need not mean fully articulated propositional knowledge. The source includes partial, fragmented, distorted and emotionally evaluated givenness. V3’s ingress must therefore not reduce the transition to a knowledge boolean.

---

## 9. Restrictive/generalized action-capacity normalization

Rawlsing should retain **only the decomposed mechanism**, not the theory label as an object.

### Restrictive-direction decomposition

```text
constraint / threat
+ limited perceived/experienced collective alternative
+ immediate security/dependency stakes
-> subjectively grounded strategy within existing power relation
-> possible instrumentalization / accommodation
-> short-run gains may coexist with long-run narrowing of cooperative possibilities
```

### Generalized-direction decomposition

```text
constraint / threat
+ objective association route
+ subject-relative premise/grounds
+ real partners / organization / means / counter-power
+ external response gates
-> possible expansion of shared control over conditions
```

### Do not import

```text
RESTRICTIVE_HF = trait
GENERALIZED_HF = trait
HF = scalar
```

---

## 10. What Holzkamp does NOT fill in the frozen synthesis

The full book does **not** eliminate the need for other theory lanes or empirical mechanism definitions. It does not provide a domain-complete law for:

- material resource allocation;
- institutional eligibility/treatment;
- network transfer/support/closure/brokerage;
- discrimination mechanisms;
- household care allocation;
- stress-process effects;
- cumulative inequality mechanisms;
- exact organization/institution response to collective action.

Its value is principally the **mediation grammar and boundary law** that those concrete mechanisms must obey.

---

## 11. D4 mapping

No new D4 is licensed.

The exact unresolved question for post-review Vozhd is narrower:

> Do existing V3 owners, in composition, already own the transformation from premise-relevant actor-relative objective social facts to first-person/phenomenal premise formation without violating ADP-017 truth/access separation?

If yes: no D4.

If no: the missing function would be downstream subject mediation, not an expansion of D1 into psychology.

M4 does not pre-adjudicate that owner audit.

---

## 12. Concepts explicitly NOT to import into Rawlsing

1. `Handlungsfähigkeit` as scalar “agency”.
2. `produktive Bedürfnisse` as need-to-produce.
3. `Kontrollbedarf` as modern generic control need.
4. restrictive/generalized action-capacity as person/group/ideology type.
5. `Deuten/Begreifen` as fixed cognitive level.
6. `subjektiver Möglichkeitsraum` as PRE-V3 objective opportunity set.
7. `Prämisse` as structural prerequisite.
8. collective subjectivity as a supra-individual mind.
9. phylogenetic functional laws as present-day social update rules.
10. Chapter 8 process types as universal developmental ages/stages.
11. the p. 355 nonzero “second possibility” thesis as an executable option guarantee.
12. bourgeois class-form examples as transhistorical social psychology.

---

## 13. Smallest licensed architectural consequence

M4 licenses **one tightening of the frozen D1–D3 package, not a fourth package**:

```text
D1:
  objective structure
  -> actor-relative objective social ecology / possibility
  [STOP BEFORE subjective possibility space / premise]

V3 INGRESS CONTRACT:
  objective actor-relative fact
  -> first-person/phenomenal availability
  -> premise / reason only if earned

D2:
  preserve intervals, recurrence, biography-relevant history and transition after-state requalification

D3:
  require realized external action + collective/institutional/counterpart gate + causally admitted changed social fact + provenance
```

The smallest concrete semantic addition is therefore an explicit firewall/interface statement:

```text
ACTOR_RELATIVE_OBJECTIVE_SOCIAL_FACT
!= SUBJECTIVE_PREMISE
```

plus proof of a lawful receiving path on the V3 side.

No new theory-name object and no new generic psychology layer is licensed.

---

## 14. Terminal answers C, D, I, J

**C. Where does PRE-V3 end and V3 subject mediation begin?**

PRE-V3/SDTF ends at typed provenance-preserving actor-relative **objective** social facts/action possibilities. V3 begins with first-person/phenomenal availability, subjective possibility space, premise, ground/reason, motive and response.

**D. What part of restrictive/generalized agency survives normalization?**

Only the situational mechanism: coping within given dependency/power relations versus practically expanding shared control over conditions, each under concrete premises, resources, partners and risks. No person/group type survives.

**I. Which Holzkamp concepts should Rawlsing explicitly NOT import?**

The twelve-item list in §12.

**J. Smallest licensed architectural consequence?**

Tighten D1’s output boundary and define/verify the V3 ingress contract; strengthen D2 history-sensitive requalification and D3 external/collective gates. No D4 and no V3 redesign are licensed by M4.

---

## Terminal

`HOLZKAMP_MAPPING_PRESERVES_PREV3_V3_FIREWALL__D1_OBJECTIVE_ACTOR_RELATIVE_ONLY__V3_OWNS_PHENOMENAL_PREMISE_REASON_MEDIATION__D2_HISTORY_REQUALIFICATION__D3_GATED_RECIPROCITY__NO_D4`.