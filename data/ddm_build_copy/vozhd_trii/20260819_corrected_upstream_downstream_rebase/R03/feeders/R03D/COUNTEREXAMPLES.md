# R03D — ONTOLOGY / AUTHORITY LEAKAGE COUNTEREXAMPLES

**Authority:** `NON_DISPOSITIVE_HOSTILE_EVIDENCE`  
**Repository:** `maidiu/rawlsing`  
**Worker branch:** `agent/vozhd-trii-dr-r03d-ontology-authority-audit`  
**Issued exact worker base:** `138ded52ae6c7d26e9a3671e39d779965b5dc6f4`

These constructions deliberately make one canonical object mean more than its frozen authority permits. A counterexample succeeds only if the illicit promotion can become semantic/runtime authority. Merely retaining an opaque provenance or replay reference is not leakage.

## D01 — Discovery score -> structural truth

Construct a `DiscoveryResultReceipt` whose selected candidate has an extreme score and apparently strong support. Present the receipt directly to V553/V554 as if the discovery score itself proves a structural relation.

**Required rejection:** the receipt may identify discovery/query/cohort provenance, but structural use must resolve an exact underlying `EmpiricalFact` and pass a separately governed `StructuralEmpiricalAdmission`. R02 gives the receipt no automatic structural semantic consumer.

**Result:** `SURVIVES`.

## D02 — Raw EmpiricalFact -> structural truth

Construct a raw `EmpiricalFact` with exact source, time, support, uncertainty and query identity. Use its completeness as an excuse to skip `StructuralEmpiricalAdmission`, first by feeding it to V553 and then by feeding it directly to V554.

**Required rejection:** completeness of empirical provenance does not create structural meaning. `StructuralEmpiricalAdmission` remains the first empirical->structural authority seam. The corrected V553 intake and V554 basis registry still need exact negative schema closure.

**Result:** `SURVIVES_WITH_QUALIFICATION` — `NEGATIVE_AUTHORITY_HARDENING_REQUIRED` at V553/V554 close-read.

## D03 — PSEPF -> structural repository

Take one source-indexed `PositionedSubjectEmpiricalPossibilityField` and try to publish it through V557 as a runtime structural object, then insert/index it in V558 `StructuralPriorRepository` so `ContextResolver` can return it as structural context.

**Required rejection:** PSEPF is population empirical possibility and its only lawful semantic lane is V3 possibility intake. V557/V558 can at most preserve unrelated opaque provenance when separately authorized; the field itself is forbidden structural repository content.

**Result:** `SURVIVES_WITH_QUALIFICATION` — V557/V558 publication/repository type-family exclusion must be hardened at close-read.

## D04 — PSEPF mass -> actor psyche

Use the field as a direct actor-state template:

```text
belief_probability = field.mass
response_probability = field.mass
actor.identity = modal_configuration
actor.memory = survey_configuration
actor.knowledge = field_component
```

**Required rejection:** V3 developmental causality, including actual history, encounter, exposure, mediation, relationships and path dependence, remains mandatory. The PSEPF can only be made available through a V3-specific intake under a separate metabolism authority; field geometry is not actor state.

**Result:** `SURVIVES_WITH_QUALIFICATION` — R01 explicitly records `V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY` as a hard blocker. `NEGATIVE_AUTHORITY_HARDENING_REQUIRED`.

## D05 — Comparator receipt -> actor prior

Take `ActorComparatorReceipt` and bypass possibility production. Treat the mapped predicate, coordinate or comparator result as a developmental prior or actor fact inside V3.

**Required rejection:** the receipt proves why exact objective actor facts were comparable to one empirical conditioner. Its direct semantic consumer is `PossibilityFieldService`; V3 receives only transitive provenance behind PSEPF / `V3EmpiricalPossibilityInput`.

**Result:** `SURVIVES_WITH_QUALIFICATION` — exact V3 intake must explicitly reject comparator receipts as standalone priors.

## D06 — Structural context -> persona / voice

Take a `ResolvedStructuralContext` containing lawful actor-independent structural pressures and feed it directly to V2/application. Render its pressures as personality, beliefs, voice, preferences or behavioral certainty without a V3 developmental realization.

**Required rejection:** `ResolvedStructuralContext` has one direct semantic consumer: V3. V2 consumes V3-generated actor-accessible/render truth, not raw structural context.

**Result:** `SURVIVES_WITH_QUALIFICATION` — R01 MD14 leaves explicit V2/app nonconsumption as material hardening. `NEGATIVE_AUTHORITY_HARDENING_REQUIRED`.

## D07 — Publication/repository -> producer reownership

Copy a producer-owned V554/V555/V556 object into V557/V558 under a new semantic identifier. Change the copy while leaving the producer immutable, then allow downstream resolution to select the changed copy.

**Required rejection:** V557 owns publication/use governance and V558 owns immutable repository/index/resolution. Neither owns producer-domain meaning. A packaged or indexed copy is nonsemantic; producer content-addressed identity remains authoritative and mismatch fails closed.

**Result:** `SURVIVES_WITH_QUALIFICATION` — the theorem is explicit, but corrected reference registration and standalone packaging must be hardened in V557/V558 close-read.

## D08 — Structural admission -> generated actor position

Take a lawful `StructuralEmpiricalAdmission` about a structural relation, stratum or population-level proposition. Assign that structural target directly to a generated person as lived position, identity, experience, belief or psyche.

**Required rejection:** admission authorizes bounded structural use. Its semantic consumers are V553 or direct V554 according to routing need; it has no V3 reverse-lane or V2/app semantic authority.

**Result:** `SURVIVES`.

## D09 — Replay receipt -> causal prior

Take a `ReplayReceipt` content hash or historical replay locator and treat it as a structural weight, actor-developmental trigger or causal parent whose value changes the generated state.

**Required rejection:** the receipt is an audit/replay locator only. It can identify exact historical semantic/authority/input bindings but cannot constrain structural or actor development by its own domain meaning.

**Result:** `SURVIVES`.

## D10 — Generated structural position -> survey comparator

Take a generated actor's nine-stratum/structural position and use it as the empirical survey comparator predicate, or as fuzzy evidence that the actor is close enough to a source coordinate. Also try nearest-cohort fallback when the exact objective fact is unavailable.

**Required rejection:** `ActorComparabilityService` maps exact governed objective actor facts at an effective time to source/time-specific empirical coordinates. Generated structural position is a distinct ontology and may not substitute for objective facts, belief, memory, fuzzy similarity or nearest-cohort inference.

**Result:** `SURVIVES_WITH_QUALIFICATION` — R01 MD12 identifies the objective actor-fact publication seam as a reverse-lane hard blocker, so the comparator intake must carry explicit negative type authority.

## Cross-case conclusion

No hostile construction falsifies the R02 ontology separation. The attack does reveal a consistent enforcement pattern:

1. **Already exact at broad authority level:** discovery receipt is not structural meaning; structural admission is not actor state; replay receipt is not causal meaning.
2. **Correct holding but close-read enforcement still required:** raw fact rejection at V553/V554; PSEPF exclusion from V557/V558; V3 metabolism; comparator-as-prior exclusion; V2/app nonconsumption; producer nonreownership packaging; objective actor-fact comparator intake.
3. **No feeder redesign authority:** these are hardening obligations for synthesis/stage close-read, not permission for R03D to select final schemas or algorithms.
