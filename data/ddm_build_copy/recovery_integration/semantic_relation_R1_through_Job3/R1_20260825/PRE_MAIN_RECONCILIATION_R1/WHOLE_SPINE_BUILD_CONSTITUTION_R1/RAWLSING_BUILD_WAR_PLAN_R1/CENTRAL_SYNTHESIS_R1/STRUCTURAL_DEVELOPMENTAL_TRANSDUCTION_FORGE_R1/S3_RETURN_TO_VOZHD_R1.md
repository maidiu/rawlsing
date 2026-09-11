# S3 RETURN TO VOZHD R1

TERMINAL STATUS:
`PASS__S3_R4_DERIVATION_INVALIDATION_SPEC_READY_FOR_VOZHD_RECONCILIATION`

CAMPAIGN: `STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1`

WORKER BRANCH:
`agent/rabochii-sdtf-r1-r4-s3-derivation-invalidation-replay`

COMMISSIONED FROM EXACT COORDINATOR STATE:
`02d4a75c030ed22da48b64718618242fc10ad858`

FROZEN R4 TARGET:
`dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

SCOPE OBSERVED:
- no mutation of main/coordinator/HQ/frozen R4;
- no S1/S2/S4/S5 return consumed;
- no runtime implementation;
- no OBL062 solution;
- no D2/D3/D4/P6 invention.

---

## 1. Terminal answers

### A. What minimum dependency graph is required?

A bipartite direct-dependency graph at rule-application grain:

```text
EXACT CURRENT DETERMINANT FACT/BINDING/WITNESS/RULE VERSION
-> RULE_APPLICATION_ID
-> DERIVED_FACT_REF
```

Minimum semantics:

```text
RULE_APPLICATION_ID
DERIVED_FACT_REF
MECHANISM_RULE_REF + exact version
DIRECT_DETERMINANT_REF(S) + determinant role
ACTOR/WORLD/CONTEXT/POSITION bindings as required
VALID_TIME_OR_INTERVAL
TYPE-COMPATIBLE WITNESS REF(S) where required
EVIDENCE_CEILING
CURRENTNESS STATUS
```

Reverse dependency discoverability is required so a changed determinant can locate only its descendants. A particular graph database/index is not required.

### B. Can generic provenance already supply it?

Only if `DERIVATION_PROVENANCE` is not opaque and already exposes the exact direct determinant set, producing application identity, exact rule version, interval/currentness, required witness refs and reverse dependency discoverability.

A generic blob/citation bundle that cannot answer `WHY DOES THIS FACT EXIST RIGHT NOW?` and `WHICH FACTS DIRECTLY DEPEND ON THIS CHANGED DETERMINANT?` is insufficient.

### C. What exactly triggers invalidation?

A required direct determinant ceasing to be valid/applicable for the asserted interval, or a competent supersession/termination/negative fact defeating the assertion under the exact rule.

Covered triggers:

```text
source correction
source expiry
required witness expiry/currentness failure
rule version change
rule invalidation/withdrawal
actor position exit
context closure
counterpart relation termination
constitutive institutional-configuration change
new governed superseding treatment
explicit type-compatible negative witness
```

Missing evidence alone never creates a negative fact.

### D. How is determinant-scoped recomputation achieved semantically?

```text
CHANGED DETERMINANT ID/VERSION
-> CURRENT DIRECTLY DEPENDENT APPLICATIONS
-> reevaluate exact contracts
-> close/invalidate unsupported outputs
-> recurse only through applications consuming changed outputs
-> rerun only newly/currently applicable governed rules
-> preserve all unrelated facts and historical provenance.
```

The determinant refs themselves are the canonical invalidation keys; no second free-standing invalidation-key ontology is required.

### E. What cycle law is required?

Default:

```text
NO D1' DERIVED FACT AT THE SAME WORLD/STATE VERSION AND VALID-TIME SLICE
MAY BE ITS OWN ANCESTOR.
```

Same-time acyclic constitutive chains remain lawful. Same-time self-support is not.

### F. What iterative processes remain lawful?

Those that advance through at least one of:

```text
time;
state/source version;
new external source-owned fact;
new competent witness;
explicit competent iteration/fixed-point authority.
```

S3 creates no generic iterative/fixed-point owner. Typed cumulative chains require distinct step/application identities and direct determinants. `CUMULATIVE DISADVANTAGE -> MORE CUMULATIVE DISADVANTAGE` is not an admissible recursive scalar.

### G. How is evidence/authority laundering prevented?

Every derived fact carries an effective evidence ceiling no stronger than the exact governed rule's causal-use/claim authority and every required truth-determining antecedent/witness, while preserving context/history/portability limits.

```text
DERIVED AUTHORITY DOES NOT STRENGTHEN THROUGH COMPOSITION.
SOURCE CITATION != CAUSAL-USE AUTHORITY.
RULE CURRENT != FACT CURRENT.
```

Incomparable evidence dimensions remain a conjunction/vector of limits rather than being promoted to a stronger scalar certainty.

### H. Does any requirement create a new D2/D3 owner?

No.

- Lifecycle/currentness is conformance to existing time/state/history owners; no D2.
- External reciprocal change remains sourced by competent world/institution/source owners; no D3.
- V3 private state never authors/invalidate D1' facts directly.

### I. Does anything alter D1'/P1-P5?

No topology change.

```text
D1' SURVIVES UNCHANGED IN JURISDICTION.
P1-P5 SURVIVE UNCHANGED AS MECHANISM-RULE CLASSES.
S3 SPECIFIES G2 DIRECT DEPENDENCY / INVALIDATION / REPLAY SAFETY ONLY.
```

No P6, D4, new status ontology, new psychology, or event laundering is introduced.

---

## 2. Minimal derivation graph

```text
DIRECT DETERMINANT FACT/BINDING/WITNESS/RULE VERSION
        ↓
EXACT RULE APPLICATION
        ↓
D1' DERIVED FACT
        ↓ when used by another rule
LATER EXACT RULE APPLICATION
```

Required invariant:

```text
CURRENT DERIVED FACT
=> current producing application
=> current exact rule version
=> all required direct determinants current/applicable
=> all required realization witnesses valid/current for asserted interval
=> effective evidence ceiling preserved.
```

`PARENT_DERIVATION_STEP_REF` and stored depth are optional because each derived antecedent resolves to its producing application. `SUPERSEDES_REF` is conditional on actual replacement semantics.

---

## 3. Invalidation law

```text
INVALIDATE/TERMINATE BY DIRECT DETERMINANT IDENTITY,
NOT BY ACTOR OR DOMAIN RESET.
```

A real transition closes affected current intervals while preserving prior lawful history. A retrospective source correction can invalidate prior assertions within the corrected scope. Witness expiry may reduce `ACTIVE/REALIZED` to `UNKNOWN/NOT_PROVEN_REALIZED` while a separately supported qualification/constitutive fact survives.

---

## 4. Transition law

```text
COMPETENT BINDING/WORLD CHANGE
-> locate exact changed determinant
-> invalidate only dependent D1' facts
-> preserve before/after provenance
-> preserve unrelated facts
-> rerun only affected current rules under new bindings
-> issue new fact/application identities for replacement state.
```

Mandatory scenarios all pass under this law:

```text
infrastructure/service outage chain;
institutional-record/gate/employment/resource/household chain;
job termination with household/school/network survival;
parent job loss -> resource -> task allocation -> child time obligation;
network relation termination without unrelated material-resource deletion.
```

---

## 5. Cycle law

```text
DEFAULT D1' DERIVATION IS ACYCLIC WITHIN ONE FACTUAL STATE/TIME SLICE.
NO FACT MAY BE ITS OWN ANCESTOR.
```

Future explicit iterative authority could define bounded/fixed-point semantics, but none is created or presumed here.

---

## 6. Evidence ceiling law

```text
OUTPUT_EVIDENCE_CEILING
<= exact rule causal/claim authority
AND
<= every required determinant/witness authority,
with all context/portability/currentness limits preserved.
```

No composition step can upgrade observational support to randomized certainty, source citation to causal-use authority, stale evidence to current fact, or absent positive evidence to negative truth.

---

## 7. World-write verdict

`PASS__WORLD_CHANGE_FIREWALL_PRESERVED`.

Required route remains:

```text
V3 ACTION
-> EXTERNAL ACTION OCCURRENCE
-> COMPETENT EXTERNAL RESPONSE
-> COMPETENT SOURCE OWNER AUTHORS NEW WORLD FACT
-> NORMAL D1' INVALIDATION/REDERIVATION.
```

Forbidden:

```text
V3 PRIVATE STATE -> D1' FACT
V3 ACTION -> DIRECT D1' INVALIDATION/WORLD WRITE
D1' -> NEW STRUCTURAL TRUTH WITHOUT COMPETENT SOURCE OWNER
```

---

## 8. R4 topology verdict

`R4_TOPOLOGY_SURVIVES_UNCHANGED__D1_PRIME_ONLY__P1_P5_ONLY__NO_D2_D3_D4_P6`.

S3 is exactly the post-adoption/readiness G2 companion grain already banked by Files 34-36: direct antecedent provenance, determinant-scoped invalidation/replay, cycle protection and no evidence-authority laundering.

---

## 9. Exact companion specification required

S3 cannot by itself make a concrete D1' rule executable. Integration requires the separately governed companion contracts already named by R4 readiness:

```text
G1 MECHANISM-RULE ADMISSION/CURRENTNESS CONTRACT
+
G3 TYPE-SPECIFIC REALIZATION/STATE WITNESS LIFECYCLE CONTRACT
```

They must supply, respectively:

```text
exact current MECHANISM_RULE_REF/version/causal-use authority
and
exact witness type/polarity/currentness/supersession/termination semantics.
```

S3 then supplies G2 dependency/replay semantics over those inputs.

OBL062/G4 remains external and unresolved by design.

---

## 10. Required product paths

```text
data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1/S3_R4_DERIVATION_GRAPH_CONTRACT_R1.md

data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1/S3_R4_INVALIDATION_AND_REDERIVATION_COURT_R1.md

data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1/S3_R4_CYCLE_AND_ITERATION_COURT_R1.md

data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1/S3_R4_EVIDENCE_CEILING_PROPAGATION_R1.md

data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1/S3_R4_TRANSITION_SCENARIO_REPLAY_R1.md

data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1/S3_RETURN_TO_VOZHD_R1.md
```

---

## 11. Exact blocker

`NONE`.

No source/theory/topology blocker was found at S3 specification grain.

FINAL TERMINAL:

`PASS__S3_R4_DERIVATION_INVALIDATION_SPEC_READY_FOR_VOZHD_RECONCILIATION`.
