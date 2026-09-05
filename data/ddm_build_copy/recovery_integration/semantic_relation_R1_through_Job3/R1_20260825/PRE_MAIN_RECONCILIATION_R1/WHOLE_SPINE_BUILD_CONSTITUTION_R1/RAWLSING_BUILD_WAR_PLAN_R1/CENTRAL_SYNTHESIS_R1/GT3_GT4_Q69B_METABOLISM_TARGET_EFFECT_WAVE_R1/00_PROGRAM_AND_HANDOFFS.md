# GT3/GT4 Q69B + METABOLISM + TARGET-EFFECT WAVE R1

Repository: `maidiu/rawlsing`

Exact common working start:

`913f2274bfb5a2b204a8666b34aa1b658eb86966`

This instruction commit is evidence only. Every worker starts from the exact SHA above.

## Frozen inherited state

GT1/GT2 remains `CLOSED_ACCEPTED_CURRENT`.

K1/K2/K3 and L1A/L1B/L2/L3 are banked on the common start.

### Primary comparator route selected for review only

L1A terminal:

`PASS__GT34_L1A_R5_CONDITIONER_ENDPOINT_CANDIDATE_MATCHING_EXISTING_ACTOR_FACT_DEFINED__NO_ADOPTION`

Candidate empirical endpoint:

`Afrobarometer R5 Q69B -> PUBLIC_CLINIC_EXPERIENCE_STATUS`

Candidate authority:

`R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY@1.0.0`

authority hash:

`3484a855a4726ffb1e13776bf57e17fa226a41e237b92f2e89f8fe443a90453a`

coordinate hash:

`7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937`

crosswalk:

`R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_STATUS_CROSSWALK@1.0.0`

hash:

`fde63966f0d8204d698047eb38d64faa2230543dff62928cdc513cdf56aae095`

time rule:

`R5_Q69B_SOURCE_NATIVE_PAST_12_MONTHS_AT_DATEINTR@1.0.0`

hash:

`4a771c6a27703bde285cedfe7b97da8bc29e953ef068ba22354e8af3f1fe6cf2`

measure basis:

`R5_Q69B_RAW_CONDITIONER_MEMBERSHIP_BASIS@1.0.0`

hash:

`f2a33c3674e924cb535038e96554f838616c034141e265aa391c864f53f2c1c3`

actor relation proof:

`GT34_L1A_Q69B_TO_ADP010_ENCOUNTER_RELATION_PROOF@1.0.0`

hash:

`7eaa5197a26c3e5ddc65b631453007f2a5ed9ba9310da6c9c233eaef6fb12aa9`

Actor-side owner:

`ADP-010 / V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0`

Relevant actor-side state:

`ENCOUNTER / OEE_ENCOUNTER_OCCURRED`

The candidate uses only source-native public-clinic experience applicability:
- native 0,1,2,3 -> PRESENT
- native 7 -> ABSENT
- native 9 -> UNKNOWN
- native 998 -> REFUSAL / NOT_LAWFULLY_CONDITIONABLE
- native -1 -> MISSING

It does NOT compare clinic-problem frequency and does NOT infer the named survey problem into actor history.

The positive future comparator is only lawful when the actor has an independently authoritative ADP-010 encounter whose subject resolves to public-clinic-or-hospital contact/use and whose event time is within the Q69B twelve-month DATEINTR window.

Absence of an actor encounter record is NOT evidence of absence.

### Fallback route

L1B terminal:

`PASS__GT34_L1B_MINIMAL_OBJECTIVE_ACTOR_ENDPOINT_CANDIDATE_FOR_R5_DEMOGRAPHIC_DEFINED__NO_ADOPTION`

Fallback actor endpoint:

`V3_OBJECTIVE_CHRONOLOGICAL_AGE_FACT_RULE@1.0.0`

This remains fallback only because it still needs a separate R5 age endpoint. Do not discard it, but do not develop it in this wave unless Q69B is invalidated.

### Metabolism authority

K2 candidate:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.0.0`

claimed hash:

`bc6c75adbb783b0c00af503375a77ef53be905d3113b4c433f10ddc7d6c96334`

initial registry:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_REGISTRY@1.0.0`

claimed hash:

`b65c4577893878ceb36a3b8b74ad7cf873a7807a35ad209efafcd8be5d1f547c`

L2 terminal:

`FAIL__GT34_L2_METABOLISM_AUTHORITY_CANDIDATE_HOSTILE_AUDIT__EXACT_DEFECT`

Exact defect:

`UNDERDEFINED_SELF_HASHING_OPERATION_ENTRY_AND_UNDEFINED_DECISION_RECEIPT_HASH_PROJECTION`

All other hostile questions passed at L2 grain, including:
- valid-empty registry has zero positive authority;
- no hidden mutation permission;
- no measurement-portability leakage;
- no CAN-008 selection without exact registry entry;
- no raw PSEPF -> psyche shortcut.

Smallest repair:
1. explicit operation-entry semantic projection excluding only derived content hash from its own projection;
2. explicit decision-receipt semantic projection/formula excluding only derived receipt hash and defining exact ordering/canonicalization law.

### CAN-008 first-positive boundary

K3 selected:

`CAN-008 / V3_ACTOR_RESPONSE_PRESSURE_FLOW_TRANSACTION_RULESET@1.0.0`

L3 terminal:

`PASS__GT34_L3_CAN008_REQUIRES_ADDITIONAL_TARGET_EFFECT_AUTHORITY__EXACT_GAP_PROVED`

CAN-008 can own the transaction, but the response-history ledger is provenance/path dependence and is NOT itself a target-effect semantic family.

A nonempty BUFFER/AMPLIFY/DEFLECT/REROUTE/TRANSFORM/BLOCK effect requires exact target-effect semantics and authority.

The field-independent seam is already clear through:

`metabolism-approved V3EmpiricalPossibilityInput`
-> exact registered metabolism operation
-> exact `V3_EMPIRICAL_POSSIBILITY_METABOLISM_CAUSAL_EVENT`
-> CAN-008 rule court
-> BLOCKED at exact target-effect authority.

## Wave goal

Run five independent workers.

M1A: hostile-review the Q69B endpoint semantics before HQ adopts anything.

M1B: prove production materialization feasibility and, if lawful, implement a bounded candidate Q69B PRE553/C11 projection without adopting it.

M2: repair K2 content-addressing law exactly; no semantic widening.

M3A: determine whether an already-accepted V3 target-state/effect authority can lawfully serve the first CAN-008 effect.

M3B: independently define the smallest CAN-008-internal target-effect authority candidate if HQ wants the first canary to avoid mutating another V3 subsystem.

No PSEPF production or positive actor mutation is authorized in this wave.

---

# WORKER M1A — Q69B ENDPOINT HOSTILE AUDIT R1

Branch:

`agent/rabochii-gt34-m1a-q69b-endpoint-hostile-audit-r1`

Profile:

`HOSTILE_AUDIT`

Read-only except bounded return.

## Mission

Try to falsify the exact L1A endpoint candidate.

Read:
- L1A return;
- exact R5 codebook/source-semantic evidence used by L1A;
- ADP-010 accepted authority;
- PRE553 coordinate/predicate law;
- no unrelated archaeology.

Audit at minimum:

1. Is the exact Q69B question really the cited clinic/hospital past-12-month problem question?
2. Do native codes 0-3 positively imply clinic/hospital experience for this field?
3. Does native 7 exactly mean no experience with public clinic in past 12 months?
4. Are 9/998/-1 typed correctly and nonpromotable?
5. Is collapsing 0-3 to PRESENT semantically lawful for conditioner membership while explicitly discarding frequency ordering?
6. Does Q69B permit only public-clinic/hospital experience status, not occurrence of the named shortage problem in generated actor history?
7. Is the DATEINTR twelve-month window exact enough for the proposed actor-side comparison?
8. Is ADP-010 ENCOUNTER the narrowest legitimate actor-side fact, and is EXPOSURE correctly not required?
9. Does the positive actor guard require an independently authoritative subject ref resolving to public-clinic-or-hospital contact/use?
10. Is silence in actor history correctly forbidden as evidence of empirical ABSENT?
11. Does the proposal avoid portability, pooling, estimand composition and source mixing?
12. Does the PRE553 D08 conditioner authority add only a new conditioner-use permission and not widen COUNTRY_ALPHA3 or the old Q86 release?
13. Do all candidate hashes recompute exactly?
14. Is a new immutable bounded C11 release required rather than in-place mutation?
15. Is there any hidden mismatch between respondent applicability semantics and actor ENCOUNTER semantics that makes the entire route noncomparable?

PASS only as:

`PASS__GT34_M1A_Q69B_ENDPOINT_HOSTILE_AUDIT__LAWFUL_FOR_BOUNDED_ADOPTION`

Otherwise:

`FAIL__GT34_M1A_Q69B_ENDPOINT_HOSTILE_AUDIT__EXACT_DEFECT`

Return:

`.../GT3_GT4_Q69B_METABOLISM_TARGET_EFFECT_WAVE_R1/M1A_Q69B_ENDPOINT_HOSTILE_AUDIT_R1/00_RETURN.md`

No adoption, no implementation, no source-row execution.

---

# WORKER M1B — Q69B ENDPOINT MATERIALIZATION / BOUNDED C11 CANDIDATE R1

Branch:

`agent/rabochii-gt34-m1b-q69b-endpoint-materialization-r1`

Profile:

`REAL_EXECUTION -> IMPLEMENT -> VERIFY_REGRESSION`

This is a candidate implementation only. It is NOT project adoption.

## Mission

Prove whether the exact accepted Afrobarometer R5 source can be materialized and used to build a new bounded Q69B PRE553 conditioner coordinate/C11 logical release while preserving the old Q86 release unchanged.

Accepted source:

`Data/Afro Barometer Round 5.sav`

SHA-256:

`c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651`

Rows:

`51,587`

Accepted codebook hash:

`7e02c649c8ae69c61f88c116fdad92353b7f06cba9e160d9ae4be18e72276735`

Candidate semantics are frozen from L1A for execution purposes only; do not widen them.

## Source law

Use only already-authorized accepted R5 source/carrier access available to the project.

No new source acquisition.

Verify source bytes exactly before reading Q69B.

Immediately persist a write-ahead checkpoint after source identity + Q69B variable/value-label semantics are verified.

If source bytes are unavailable, return the exact materialization blocker without inventing values.

## Implementation target

Prefer one narrow new module, e.g.:

`rawlsing_next/wave2_r5_q69b_conditioner_projection.py`

or equivalent.

Do NOT alter the meaning or identity of:
- `R5_GT12_Q86A_Q86B_FROZEN`;
- its current query/fact/replay;
- COUNTRY_ALPHA3 authority;
- GT1/GT2 adoption.

Create a NEW bounded release identity.

It must contain only the minimum new Q69B coordinate material necessary for the future D08 conditioner endpoint plus inherited exact respondent/routing/source identity needed for replay.

## Exact Q69B mapping

Only if source labels independently verify L1A:

- 0,1,2,3 -> PUBLIC_CLINIC_EXPERIENCE_PRESENT
- 7 -> PUBLIC_CLINIC_EXPERIENCE_ABSENT
- 9 -> UNKNOWN
- 998 -> REFUSAL / NOT_LAWFULLY_CONDITIONABLE
- -1 -> MISSING

Do not assume undocumented codes.

## Required output

Create ordinary PRE553-compatible exact coordinate facts/material for Q69B and a new bounded C11 logical release.

Record:
- exact source hash;
- exact Q69B variable label/question/value labels;
- source-native row count;
- count per native Q69B code;
- count per typed endpoint state;
- exact DATEINTR availability required for temporal anchoring;
- new release ID/hash;
- coordinate authority candidate/ref/hash used;
- coordinate object ID/hash;
- replay/provenance hashes;
- deterministic rehydration/replay proof.

Do NOT create a comparator predicate yet.

## Hostile tests

Reject:
- source hash drift;
- wrong variable;
- wrong codebook;
- undocumented Q69B code;
- 9/998/-1 positive promotion;
- frequency-order use;
- in-place Q86 release widening;
- country-authority widening;
- respondent count mismatch;
- missing DATEINTR when needed;
- cross-source or portability leakage.

## Checkpoint law

Checkpoint:
1. source + Q69B semantic verification;
2. new release/coordinate identities after successful build;
before broad regression.

## Outcomes

PASS only if the new bounded projection is genuinely constructible and deterministic:

`PASS__GT34_M1B_Q69B_BOUNDED_PRE553_C11_CANDIDATE_MATERIALIZED__NO_ADOPTION`

If source bytes cannot be materialized:

`BLOCKED__GT34_M1B_ACCEPTED_R5_SOURCE_BYTES_NOT_MATERIALIZABLE`

If source data contradicts L1A:

`FAIL__GT34_M1B_Q69B_SOURCE_SEMANTICS_CONTRADICT_L1A_CANDIDATE`

Return path:

`.../GT3_GT4_Q69B_METABOLISM_TARGET_EFFECT_WAVE_R1/M1B_Q69B_ENDPOINT_MATERIALIZATION_R1/00_RETURN.md`

---

# WORKER M2 — METABOLISM CONTENT-ADDRESSING REPAIR R1

Branch:

`agent/rabochii-gt34-m2-metabolism-content-address-repair-r1`

Profile:

`SEMANTIC_AUTHORITY`

No production implementation.
No adoption.
No PSEPF execution.
No actor mutation.

## Mission

Repair ONLY L2's two exact identity-law defects in the K2 candidate.

Do not change jurisdiction, decision semantics, valid-empty registry semantics, ownership boundaries, portability law, target-owner law, RNG law, or direct-assignment firewall unless required to make the hash projection internally coherent.

## Required repair A — operation entry

Define exact authority material:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_OPERATION_ENTRY_SEMANTIC_PROJECTION@1.0.0`

It must:
- enumerate every semantic field of an operation registry entry;
- exclude only derived identity/hash material from its own digest projection;
- define ordered vs set-like field handling explicitly;
- use repository canonical semantic JSON law;
- define exact SHA-256 formula;
- bind operation ID and version as semantic material;
- make `operation_content_hash` independently recomputable;
- prohibit self-reference and ambiguous alternate projections.

The final entry may carry an `operation_ref`, but the ref must be derived/validated from the already-hashed semantic projection rather than recursively hashed inside itself.

## Required repair B — decision receipt

Define exact authority material:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_DECISION_RECEIPT_SEMANTIC_PROJECTION@1.0.0`

It must:
- bind every replay-material semantic field required by K2;
- exclude only the derived `decision_receipt_hash` from its own projection;
- define exact canonicalization for ordered/set-like collections;
- define exact SHA-256 formula;
- make positive, negative, stale, noncomparable, valid-empty and unresolved receipts equally content-addressed;
- make the downstream owner able to independently recompute/verify the receipt hash.

## Recompute candidate

Produce a corrected complete K2 authority candidate + valid-empty registry with new semantic hashes if the authority material itself changes.

Explicitly state which old hashes are superseded.

The valid-empty registry must remain zero-positive-authority.

## Hostile self-checks

Prove:
- no self-hashing cycle;
- one semantic material -> one digest;
- field reorder canonicality where appropriate;
- ordered sequences remain ordered where semantically ordered;
- sets are canonically normalized where semantically set-like;
- changing any semantic field changes digest;
- changing only derived hash field cannot define a second compliant semantic object;
- no caller-selected hash/projection;
- no semantic widening.

Terminal:

`PASS__GT34_M2_METABOLISM_CONTENT_ADDRESSING_REPAIRED__CANDIDATE_READY_FOR_REAUDIT`

If repair requires changing the authority model substantively:

`NEEDS_HQ_DECISION__GT34_M2_HASH_REPAIR_REQUIRES_SEMANTIC_MODEL_CHANGE`

Return:

`.../GT3_GT4_Q69B_METABOLISM_TARGET_EFFECT_WAVE_R1/M2_METABOLISM_CONTENT_ADDRESS_REPAIR_R1/00_RETURN.md`

---

# WORKER M3A — EXISTING CAN-008 TARGET-EFFECT AUTHORITY DISCOVERY R1

Branch:

`agent/rabochii-gt34-m3a-existing-can008-target-effect-authority-r1`

Profile:

`DISCOVER -> SEMANTIC_AUTHORITY`

Read-only except bounded return.

No implementation.
No adoption.
No positive execution.

## Mission

Determine whether an existing accepted V3 semantic/state authority can lawfully serve as the target-effect owner for the first nonempty CAN-008 response effect downstream of the future metabolism causal event.

Inspect the strongest plausible accepted owners, including:
- CAN-009 material/vitality;
- CAN-010 need/expectation/striving;
- CAN-011 middle state;
- ADP-016 causal memory;
- other accepted V3 bounded state/effect owners if more exact.

Do NOT choose a target merely because CAN-008 has an effect verb that sounds compatible.

## Competence test

A candidate counts only if:
1. it owns a concrete target proposition/state/effect family now;
2. it has an exact lawful target-authority ref CAN-008 can validate;
3. one qualitative deterministic CAN-008 effect kind has exact semantics relative to that target;
4. no numeric formula is needed;
5. the target may lawfully receive the metabolism-event + independent actor-history parentage;
6. this is not population evidence directly assigned to state;
7. no unrelated unfinished subsystem must be built first;
8. one minimal positive mutation can be isolated and replayed;
9. typed negative/rollback states exist;
10. the first canary remains bounded and does not force V2.

## Outcomes

A — existing target suitable:

`PASS__GT34_M3A_EXISTING_TARGET_EFFECT_AUTHORITY_SUITABLE_FOR_CAN008_FIRST_POSITIVE_CANARY`

Return exact owner, exact target proposition, exact CAN-008 effect kind, exact target update law/registry prerequisite and why it is minimal.

B — no existing accepted target is directly suitable:

`PASS__GT34_M3A_NO_EXISTING_TARGET_EFFECT_AUTHORITY_DIRECTLY_SUITABLE__EXACT_GAP_PROVED`

C — multiple genuinely equal minima:

`NEEDS_HQ_DECISION__GT34_M3A_MULTIPLE_EQUAL_MINIMUM_TARGET_EFFECTS`

Return:

`.../GT3_GT4_Q69B_METABOLISM_TARGET_EFFECT_WAVE_R1/M3A_EXISTING_TARGET_EFFECT_AUTHORITY_R1/00_RETURN.md`

---

# WORKER M3B — MINIMAL CAN-008-INTERNAL TARGET-EFFECT AUTHORITY CANDIDATE R1

Branch:

`agent/rabochii-gt34-m3b-can008-internal-target-effect-candidate-r1`

Profile:

`SEMANTIC_AUTHORITY`

No implementation.
No adoption.
No positive execution.

## Mission

Independently determine whether the smallest first-positive canary should use a NEW CAN-008-internal target-effect state rather than mutating another V3 subsystem.

This candidate must be a real semantic state/effect target owned within CAN-008's immediate-response jurisdiction, distinct from the response-history ledger itself.

Do not merely rename "append history" as an effect.

## Candidate test

A lawful internal target must:
- represent an actual bounded immediate response-flow proposition owned by CAN-008;
- be semantically downstream of a generated causal input but upstream/independent of CAN-010/011/012, memory, position, attractor and V2;
- admit at least one qualitative deterministic effect kind from CAN-008's existing vocabulary;
- have exact pre/post state semantics;
- have a valid-empty initial registry/state if no concrete rule exists;
- define exact target authority/ref/hash and replay;
- avoid numeric psychology formulas;
- avoid belief, personality, motivation, memory or structural-position claims;
- not make the ledger itself the target.

Possible shape only if supported by CAN-008 law:
a bounded actor-internal immediate response-routing/containment state whose changes are things like presence/absence of a governed response-flow disposition or routing token. Do NOT assume this exists; derive or reject it.

## Outcomes

If a smallest lawful internal target can be defined:

`PASS__GT34_M3B_MINIMAL_CAN008_INTERNAL_TARGET_EFFECT_AUTHORITY_CANDIDATE_DEFINED__NO_ADOPTION`

Return:
- authority candidate;
- state schema;
- exact positive proposition;
- exact permissible CAN-008 effect kind;
- registry/state initialization law;
- replay;
- nonownership ceiling.

If any such target would be invented semantics inconsistent with accepted CAN-008:

`PASS__GT34_M3B_CAN008_INTERNAL_TARGET_EFFECT_ROUTE_REJECTED__MUST_USE_EXTERNAL_TARGET_OWNER`

If multiple equal minima remain:

`NEEDS_HQ_DECISION__GT34_M3B_MULTIPLE_EQUAL_MINIMUM_INTERNAL_TARGETS`

Return:

`.../GT3_GT4_Q69B_METABOLISM_TARGET_EFFECT_WAVE_R1/M3B_CAN008_INTERNAL_TARGET_EFFECT_CANDIDATE_R1/00_RETURN.md`

---

# FAN-IN LAW

M1A and M1B are complementary:
- M1A owns semantic validity;
- M1B owns physical/materialization feasibility.

M2 owns only the known K2 hash-contract repair.

M3A and M3B are competing target-effect routes:
- M3A asks whether an existing target is cheaper;
- M3B asks whether a narrow CAN-008-internal target is cheaper and lawful.

After fan-in, HQ will:
1. adopt/reject Q69B endpoint only if M1A passes and M1B proves materialization;
2. return to the field-specific comparator authority only after that endpoint is accepted;
3. re-audit and adopt the repaired metabolism authority if M2 succeeds;
4. choose exactly one target-effect route from M3A/M3B;
5. define/hostile-review the first complete positive operation;
6. implement before any real PSEPF -> positive V3 execution.

No positive actor mutation is authorized by this wave.
