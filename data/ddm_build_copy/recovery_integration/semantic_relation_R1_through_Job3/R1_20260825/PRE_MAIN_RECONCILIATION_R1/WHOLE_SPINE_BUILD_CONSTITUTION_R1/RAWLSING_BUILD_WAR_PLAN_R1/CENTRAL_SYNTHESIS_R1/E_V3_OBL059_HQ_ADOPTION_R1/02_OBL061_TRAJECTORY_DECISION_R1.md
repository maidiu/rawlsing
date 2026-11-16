# VOZHD / HQ — OBL061 BOUNDED RUNTIME-CONSTRUCTION TRAJECTORY R1

Basis:
- OBL058 authority contract: PROJECT-CURRENT
- OBL059 authority contract: PROJECT-CURRENT by HQ adoption `d523a23c6203ced0e4e1d379b3a56f2864868f7d`
- OBL060 authority contract: PROJECT-CURRENT
- OBL056 acceptance registry authority: PROJECT-CURRENT, ZERO POSITIVE ENTRIES
- OBL055 executor: PROJECT-CURRENT, NOT EXECUTED
- current first-canary ENCOUNTER/OEE: ABSENT

This document authorizes trajectory decomposition only. It does not itself mint a current actor, phase, event, source fact, acceptance entry, ENCOUNTER or OEE.

## Ownership decomposition

One exact grain, one owner. No worker may mint the entire chain for convenience.

### Stage A — runtime anchors
A1. ADP-007 current actor-activation instance.
A2. ADP-008 current active-developmental-phase instance bound to the exact actor.
A3. Exact world/time/context/opportunity binding for the first canary.

A1 and A3 may proceed independently if they do not invent each other's facts. A2 consumes the exact admitted actor identity.

### Stage B — source-owned positive facts
After the required anchor bindings exist:
B1. OBL058 positive causal-use permission fact.
B2. OBL059 positive applicability fact through the adopted R13 canonical boundary.
B3. ADP-019 contact-occurrence witness/event.
B4. OBL060 witness-independence fact, consuming the exact B3 occurrence.

B1, B2 and B3 are separate source-owned grains and should run in parallel where their exact prerequisites permit. B4 depends on B3.

### Stage C — acceptance
C1. Install exactly the required OBL056 CURRENT_ACCEPTED entries for:
- CAUSAL_USE_PERMISSION
- POSITIVE_APPLICABILITY
- CONTACT_OCCURRENCE_WITNESS
- CONTACT_WITNESS_INDEPENDENCE

Acceptance verifies provenance/membership/scope. It does not create the underlying semantic truth.

### Stage D — first current OEE
D1. Recompose the complete exact OBL055 input set from A/B/C.
D2. Independent pre-execution replay/hostile court.
D3. Separate VOZHD/HQ current-effect authorization.
D4. Only after D3, execute the adopted OBL055 executor to produce the first current ENCOUNTER/OEE.

No D-stage worker may backfill or infer a missing A/B/C fact.

## Hard prohibitions
- authority-contract currentness != positive fact currentness;
- no synthetic fixture identity may substitute for a current generated-world object;
- no co-location or co-presence inference may become ENCOUNTER;
- no caller assertion may authenticate authority;
- no source-specific representation adapter may become OBL059 decision authority;
- no OBL056 acceptance entry may be created before its source-owned fact exists;
- OBL055 must not execute before the exact chain is current and separately authorized;
- OBL032/A remains asleep until a lawful current ENCOUNTER/OEE exists.

## HQ disposition

`OBL061 = TRAJECTORY_DECOMPOSED__RUNTIME_CONSTRUCTION_NOT_YET_EXECUTED`

SUB-VOZHD E may be reactivated only under a fresh bounded OBL061 continuation that preserves this ownership split. It is stood down from further authority engineering.

