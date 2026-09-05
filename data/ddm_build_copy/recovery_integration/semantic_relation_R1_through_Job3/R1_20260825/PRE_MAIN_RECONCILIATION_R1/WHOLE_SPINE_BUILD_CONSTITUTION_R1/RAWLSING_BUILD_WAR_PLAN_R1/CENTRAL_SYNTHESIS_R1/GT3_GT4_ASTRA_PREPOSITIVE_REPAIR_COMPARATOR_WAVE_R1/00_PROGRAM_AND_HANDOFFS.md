# GT3/GT4 ASTRA PRE-POSITIVE REPAIR + COMPARATOR WAVE R1

Repository: `maidiu/rawlsing`

Exact common working start:

`3aaf6759f270c9b730db5d09bb6a87f92ec34345`

This instruction commit is evidence only. Every worker begins from the exact SHA above.

## Frozen current project state

GT1/GT2 is `CLOSED_ACCEPTED_CURRENT`.

Astra audit package is banked as evidence.

HQ current Astra disposition:

- ASTRA-003 = CLOSED by post-audit repair + real E2B proof.
- ASTRA-001 = current defect, must close before first positive V3 execution.
- ASTRA-002 = current shared-boundary authority defect, must close before first positive V3 execution.
- ASTRA-004 = architecture-level invocation binding now represented by the adopted metabolism contract, but concrete operation/effect runtime proof remains required before first positive V3 execution.
- ASTRA-005 = banked identity-preserving optimization, not a current correctness blocker.
- ASTRA-006 = open bounded reconstruction/dependency-role question, must be closed or its trust boundary proved before the first positive owner relies on transitive dependency roles.

Adopted valid-empty authority:

`V3_EMPIRICAL_POSSIBILITY_METABOLISM_AUTHORITY@1.0.0`

hash:

`e1ce806ebd443d562c7d5afdb14f00739a3b7478e2a2fcf1acfc9acb89b2e34e`

with valid-empty registry hash:

`b65c4577893878ceb36a3b8b74ad7cf873a7807a35ad209efafcd8be5d1f547c`

and zero positive operations.

Adopted valid-empty CAN-008 subordinate target authority:

`V3_CAN008_INTERNAL_TARGET_EFFECT_AUTHORITY@1.0.0`

hash:

`cb745b0a119d764c00db366274736d3e837879534a9d8ae02907002d85965b01`

with valid-empty rule registry hash:

`6a2f68c6e38bcd816dc05ba852eb7f9c169c30f30da559490b222abfe62adaad`

and zero positive rules.

Q69B candidate is semantically and physically ready but HQ adoption is held only until ASTRA-001 identity-preservation repair proves unchanged canonical identities.

Q69B candidate authority:

`R5_Q69B_PUBLIC_CLINIC_EXPERIENCE_PRE553_D08_CONDITIONER_COORDINATE_AUTHORITY@1.0.0`

hash:

`cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c`

Q69B candidate release:

`R5_GT34_N2_Q69B_BOUNDED_CANDIDATE_R1`

hash:

`15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4`

Q69B replay manifest hash:

`8ec8450d41524015c8e6b2716c00f622a9792334d2b952cac585b3b2971cb539`

Q69B transport semantic hash:

`c90ef7eaeea4b1536d3153beb344ce22156bf15bf835a3182c1b5784b8f238c5`

Q69B coordinate hash:

`7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937`

Accepted actor-side owner for the first comparator route:

`ADP-010 / V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0`

Relevant positive actor fact:

`V3OEERealizationRecord`

with:
- `realization_state = ENCOUNTER`
- `event_effect_kind = OEE_ENCOUNTER_OCCURRED`
- independently authoritative public-clinic-or-hospital subject semantics
- exact event time unambiguously inside the Q69B DATEINTR-anchored source-native twelve-month window.

Silence in actor history is NOT a negative fact.

No worker in this wave may execute a positive V3 mutation.

---

# WORKER O1 — PRE553 DEEP IMMUTABILITY / AUTHENTICATED READ REPAIR R1

Branch:

`agent/rabochii-gt34-o1-pre553-deep-immutability-repair-r1`

Profile:

`IMPLEMENT -> HOSTILE_VERIFY -> REGRESSION`

## Mission

Close ASTRA-001 exactly, without changing accepted semantic meaning or any unchanged canonical identity.

Astra demonstrated that:
- `CanonicalSemanticObject` protects only the outer container;
- nested dictionaries/lists in identity-bearing semantic material remain publicly mutable through exported aliases/projections;
- exact repository reads may return those same objects;
- ordinary I03 can consume changed nested bodies under stale source/event refs unless a separate integrity check happens to run.

The repair must establish:

> after construction/seal, no ordinary public API can mutate repository-owned identity-bearing semantic bodies; and any exported representation is detached or immutable enough that mutation cannot change the sealed object's future semantic projection.

Do not rely on caller discipline.

## Required first inspection

Read only:
- Astra ASTRA-001 record and cited current files;
- `rawlsing_next/pre553_empirical_objects.py`;
- `rawlsing_next/pre553_c11_repository.py`;
- `rawlsing_next/pre553_empirical_query.py`;
- `rawlsing_next/_pre553_query_predicate.py`;
- direct representation-sensitive consumers, especially GT12 release-member validation and current Q69B projection tests.

Do not redesign PRE553.

## Repair law

Choose the smallest lawful implementation among:
- recursively immutable internal semantic descendants plus detached canonical export;
- or an equally strong authenticated read boundary that prevents stale body consumption.

A repair that only shallow-copies `as_dict()` while `semantic_fields` or direct attribute access still exposes mutable descendants is insufficient.

A repair that changes semantic JSON, object IDs, content hashes, ordering, set-like canonicalization, or exact-ref meaning is forbidden.

If internal nested mappings become immutable proxy/frozen structures, audit every representation-sensitive consumer and repair only compatibility assumptions, not semantic law.

## Mandatory exact identity preservation

For unchanged accepted objects, prove byte-identical canonical semantic projections and identical content hashes.

At minimum prove unchanged:
- current GT2 predicate/query/fact/replay identities;
- Q86 release identity;
- Q69B candidate authority hash:
  `cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c`;
- Q69B candidate release hash:
  `15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4`;
- Q69B replay manifest hash:
  `8ec8450d41524015c8e6b2716c00f622a9792334d2b952cac585b3b2971cb539`;
- Q69B transport identities.

No empirical reexecution from raw R5 source is required if repo-native Q69B transport deterministically reconstructs the candidate.

## Hostile mutation court

Reproduce Astra's strongest class of attack and prove it is closed:

1. construct/seal a small source-backed C11 release;
2. obtain semantic material through every ordinary public exposure:
   - direct semantic-field attribute;
   - `semantic_fields`;
   - `semantic_projection()`;
   - `as_dict()`;
   - exact repository resolution;
3. attempt nested mutation of identity-bearing respondent/event/authority/ref material;
4. require either:
   - mutation impossible; or
   - mutation affects only a detached export and leaves repository-owned body/projection/hash unchanged;
5. rerun the exact query and require identical cells/fact/replay.

Also prove any deliberately corrupted reconstructed object fails authenticated integrity before ordinary execution can treat its stale ref as valid.

## Regression

Run the smallest relevant PRE553/C11/I03/Q86/Q69B/E2B suites needed to prove:
- canonical bytes unchanged;
- query behavior unchanged;
- Q69B candidate identity unchanged;
- no consumer breaks from immutable representation.

Do not rerun raw-source empirical GT1/GT2.

## Terminal

PASS only:

`PASS__GT34_O1_ASTRA001_PRE553_DEEP_IMMUTABILITY_CLOSED__CANONICAL_IDENTITIES_UNCHANGED`

FAIL if canonical identities must change:

`FAIL__GT34_O1_ASTRA001_REPAIR_CHANGES_ACCEPTED_SEMANTIC_IDENTITY`

BLOCK if an unavoidable architecture ambiguity prevents a safe minimal repair:

`NEEDS_HQ_DECISION__GT34_O1_ASTRA001_IMMUTABILITY_BOUNDARY_UNRESOLVED`

Return:

`.../GT3_GT4_ASTRA_PREPOSITIVE_REPAIR_COMPARATOR_WAVE_R1/O1_PRE553_DEEP_IMMUTABILITY_REPAIR_R1/00_RETURN.md`

Production changes permitted only in the smallest PRE553 representation/read-boundary surface plus directly necessary tests.

---

# WORKER O2 — SHARED I03 / M1->M4 AUTHORITY BOUNDARY REPAIR R1

Branch:

`agent/rabochii-gt34-o2-shared-authority-boundary-repair-r1`

Profile:

`IMPLEMENT -> HOSTILE_VERIFY -> REGRESSION`

## Mission

Close ASTRA-002 at the shared operation boundaries without changing accepted authority meaning.

Astra proved two instances of one root problem:

1. ordinary/shared I03 execution can accept an ALLOW query authority whose declared family or exact source scope is unfit, even though stronger GT12 builders reject it;
2. shared `structural_objects_from_accepted_m1(...)` can accept caller-selected producer uses such as `REVIEW`, even though the governed GT12 relation wrapper derives exact adopted CONTEXT-only use and rejects widening.

The repair must make unsafe shared invocation impossible.

## I03 boundary law

At the canonical ordinary query-execution boundary, require exact authority fitness for the actual operation:
- authority kind/status/hash valid;
- exact governed object family;
- exact source/universe scope where the authority contract requires it;
- exact target-use/operation permission;
- no generic ALLOW fallback;
- typed negatives remain typed negatives.

Do not hardcode only GT2/Q86 law into the generic executor.

Use existing authority validators/contracts where possible.

If a truly unchecked lower-level kernel must remain, make it non-public/internal enough that ordinary exported execution cannot reach it without an already-validated non-forgeable binding.

## M1->M4 boundary law

Do not impose `CONTEXT` globally on unrelated M1/M2/M3 contracts.

For the shared relation M1->M4 path:
- caller-selected use labels alone must never be authority;
- exact producer use must be proven by a validated authority/binding appropriate to the relation contract;
- the adopted GT12 path must remain exactly `("CONTEXT",)`;
- `REVIEW`, `ACTIVE_CAUSAL`, mixed sets, missing binding, wrong authority/adoption must fail at the shared boundary;
- lawful unrelated relation contracts must retain their own explicitly governed use semantics.

You may introduce a validated-binding type/token if it is the smallest non-forgeable shared contract and does not create semantic authority itself.

## Mandatory hostile controls

I03:
- correct authority hash but wrong family;
- correct kind/operation but source-universe excluded;
- wrong target use;
- stale/revoked/nonpositive authority;
- lawful exact current query unchanged.

M1->M4:
- raw caller `REVIEW`;
- raw caller `ACTIVE_CAUSAL`;
- mixed `CONTEXT+REVIEW`;
- absent binding;
- wrong authority hash;
- wrong adoption;
- lawful GT12 CONTEXT path unchanged.

No public/shared path may produce a governed structural object from caller-selected use alone.

## Identity / semantic ceiling

This is an enforcement repair.

Do not change:
- GT1/GT2 current query/fact/replay;
- FIELD FORGE semantics;
- adopted permission translation mapping;
- V557/V558 semantics;
- V3 zero-positive law.

## Terminal

PASS only:

`PASS__GT34_O2_ASTRA002_SHARED_AUTHORITY_BOUNDARIES_CLOSED__NO_AUTHORITY_WIDENING`

If safe repair would require a new semantic permission model:

`NEEDS_HQ_DECISION__GT34_O2_ASTRA002_REPAIR_REQUIRES_AUTHORITY_MODEL_CHANGE`

Return:

`.../GT3_GT4_ASTRA_PREPOSITIVE_REPAIR_COMPARATOR_WAVE_R1/O2_SHARED_AUTHORITY_BOUNDARY_REPAIR_R1/00_RETURN.md`

---

# WORKER O3 — V558 DEPENDENCY-ROLE RECONSTRUCTION BOUNDARY AUDIT R1

Branch:

`agent/rabochii-gt34-o3-v558-dependency-role-boundary-audit-r1`

Profile:

`HOSTILE_AUDIT`

Read-only except bounded return.

## Mission

Close ASTRA-006 as an open question, not as a presumed defect.

Find the exact accepted serialization/reconstruction boundary actually used for V557/V558 structural repository/bundle material that the next downstream consumer would receive.

Then inspect exactly one first downstream consumer's treatment of:
- required dependency roles;
- negative dependency roles;
- exact repository edges;
- opaque lineage/provenance refs;
- permission checks.

Do not audit every storage system.

## Questions

1. What exact accepted codec/loader/reconstructor exists today, if any?
2. Does construction validate required + negative dependency completeness?
3. What dependency-role material is content-addressed?
4. What role material is reconstructed from trusted builder law rather than object payload identity?
5. Are opaque M1 lineage refs intentionally non-executable provenance?
6. Can a roundtrip omit or reclassify a negative dependency while keeping a valid-looking repository identity?
7. Does the first consumer infer permission/causal readiness merely from a lineage ref being present?
8. Does resolver permission remain itemwise after roundtrip?
9. Is there a documented/executable trusted boundary that makes the current design sound?
10. If no accepted external codec exists and only trusted in-memory construction is current, is that itself enough to close Astra-006 for the first canary by forbidding alternate reconstruction paths?

## Required proof

If an accepted codec exists:
- roundtrip one bounded repository with both positive required and negative dependencies;
- verify exact closure/roles after reconstruction;
- attempt omission/reassignment and require rejection.

If no accepted codec exists:
- prove the actual first consumer receives only a trusted in-memory bundle built by the validated builder;
- prove no alternate public constructor/loader can bypass dependency-role validation;
- state the future serialization precondition explicitly.

## Outcomes

A — trust boundary is sound, no defect:

`PASS__GT34_O3_ASTRA006_DEPENDENCY_ROLE_BOUNDARY_PROVED__NO_DEFECT`

B — real role-loss/bypass defect demonstrated:

`FAIL__GT34_O3_ASTRA006_DEPENDENCY_ROLE_RECONSTRUCTION_DEFECT_PROVED`

C — no current codec and future serialization remains a deferred requirement, but first canary is safe in-memory:

`PASS__GT34_O3_ASTRA006_FIRST_CANARY_TRUST_BOUNDARY_PROVED__FUTURE_CODEC_REQUIREMENT_BANKED`

Do not implement a broader codec or add identity fields merely to satisfy the audit.

Return:

`.../GT3_GT4_ASTRA_PREPOSITIVE_REPAIR_COMPARATOR_WAVE_R1/O3_V558_DEPENDENCY_ROLE_BOUNDARY_AUDIT_R1/00_RETURN.md`

---

# WORKER O4 — ADP-010 <-> Q69B FIELD-SPECIFIC COMPARATOR AUTHORITY CANDIDATE R1

Branch:

`agent/rabochii-gt34-o4-adp010-q69b-comparator-authority-candidate-r1`

Profile:

`SEMANTIC_AUTHORITY`

No production implementation.
No adoption.
No PSEPF.
No actor mutation.

## Mission

Define the exact first real OBL031 field-specific comparator authority candidate using the now-materialized Q69B endpoint candidate and already-accepted ADP-010 objective encounter fact.

This work is conditional on Q69B final HQ adoption after O1 identity preservation.

Do not invent a generic comparator framework.

## Frozen empirical side

Candidate coordinate:

`Afrobarometer/R5:Q69B:PUBLIC_CLINIC_EXPERIENCE_STATUS`

hash:

`7a9910beead34e2617f5fdbacdd762fdde89b3614b90444c2e30f61a1a601937`

Candidate repaired coordinate authority hash:

`cb84cf0962f5d11e7713912bc80d2078c89635ac09d7a24e39b7586591b4135c`

Candidate release:

`R5_GT34_N2_Q69B_BOUNDED_CANDIDATE_R1`

hash:

`15b39da2a58bdb0716e8e84dd63b215e2fc5b6abdc3bc6edf8c282cf4813dbc4`

Source-native statuses:
- PRESENT from native 0/1/2/3;
- ABSENT from native 7;
- UNKNOWN from 9;
- REFUSAL nonconditionable from 998;
- MISSING from -1.

Frequency ordering among 0/1/2/3 is irrelevant to comparator membership.

## Frozen actor side

Accepted owner:

`ADP-010 / V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0`

Positive comparator source fact must be an exact accepted:
`V3OEERealizationRecord`
with:
- actor ref;
- `realization_state = ENCOUNTER`;
- `event_effect_kind = OEE_ENCOUNTER_OCCURRED`;
- independently authoritative subject ref whose exact semantics resolve to public-clinic-or-hospital contact/use;
- exact event time;
- exact owner authority/ref/hash and replay.

Exposure is not required.

Actor-history silence is not negative evidence.

## Comparator direction

The first positive comparator is:

> exact actor ENCOUNTER with public clinic/hospital, inside the exact source-native twelve-month comparison window -> D08 predicate selecting Q69B PUBLIC_CLINIC_EXPERIENCE_PRESENT respondents.

Do not infer the named medicine/supplies problem into actor history.

Do not infer actor absence from no encounter record.

A comparator to empirical ABSENT may exist only if a separately authoritative full-window actor nonoccurrence fact exists. If current ADP-010 does not own such a fact, the first authority must simply not provide an ABSENT actor comparator path.

## Candidate requirements

Define exact:

1. authority ID/version and semantic hash material;
2. actor fact family and exact accepted owner;
3. accepted subject semantic authority requirement;
4. actor event-time law;
5. empirical coordinate/release/source/universe/measure/time refs;
6. comparator rule ID/version/hash;
7. exact temporal comparability rule between actor event time and respondent DATEINTR-anchored source window;
8. exact value relation:
   `ADP010_PUBLIC_CLINIC_ENCOUNTER_IN_WINDOW -> Q69B_PUBLIC_CLINIC_EXPERIENCE_PRESENT`;
9. exact D08 predicate AST produced;
10. separate accepted D08 predicate grammar authority ref;
11. exact Q69B coordinate authority ref;
12. exact currentness/replay law;
13. comparator provenance receipt schema/hash projection;
14. typed outcomes:
   - MATCH / PREDICATE_PRODUCED;
   - NONCOMPARABLE_SUBJECT;
   - NONCOMPARABLE_TIME;
   - UNRESOLVED_ACTOR_FACT_AUTHORITY;
   - UNRESOLVED_EMPIRICAL_AUTHORITY;
   - STALE;
   - INTEGRITY_FAILURE;
   - NO_AUTHORIZED_NEGATIVE_COMPARATOR where appropriate.

If `NO_MATCH` would be semantically misleading because this first rule only admits an exact positive encounter branch, do not include a generic NO_MATCH; use a more exact typed outcome.

## Positive output ceiling

Only:

`EXACT_D08_EMPIRICAL_PREDICATE + COMPARATOR_PROVENANCE_RECEIPT`

The comparator authority does NOT create:
- PSEPF;
- actor belief;
- actor response;
- actor structural position;
- source portability;
- measurement equivalence;
- metabolism permission;
- CAN-008 authority;
- V3 mutation.

## Predicate shape

The resulting D08 predicate must select the exact Q69B coordinate's PRESENT state under separately accepted predicate grammar.

Do not select native 0/1/2/3 as an ordered metric.

Do not combine another survey field.

Do not add population weights unless separately authorized; this first comparator remains on the accepted raw conditioner membership basis.

## Terminal

PASS only:

`PASS__GT34_O4_ADP010_Q69B_FIELD_SPECIFIC_COMPARATOR_AUTHORITY_CANDIDATE_DEFINED__NO_ADOPTION`

If actor-side subject semantics cannot be bound exactly enough:

`BLOCKED__GT34_O4_ADP010_PUBLIC_CLINIC_SUBJECT_SEMANTICS_NOT_EXACTLY_OWNED`

If time comparison cannot be made exact:

`BLOCKED__GT34_O4_ADP010_Q69B_TEMPORAL_COMPARABILITY_NOT_EXACTLY_OWNED`

Return:

`.../GT3_GT4_ASTRA_PREPOSITIVE_REPAIR_COMPARATOR_WAVE_R1/O4_ADP010_Q69B_COMPARATOR_AUTHORITY_CANDIDATE_R1/00_RETURN.md`

---

# FAN-IN LAW

O1 owns only source-body immutability / authenticated read semantics and exact identity preservation.

O2 owns only shared operation-authority enforcement.

O3 owns only Astra-006 dependency-role boundary adjudication.

O4 owns only the first field-specific comparator authority candidate.

No worker may consume another in-flight worker's unbanked result.

After fan-in HQ will:

1. if O1 PASS, adopt Q69B authority + bounded release without source reacquisition;
2. if O2 PASS, bank/accept the shared-boundary enforcement repair;
3. if O3 PASS, close Astra-006 at the proved trust boundary;
4. hostile-review O4 and, after Q69B adoption, adopt the exact comparator authority;
5. then define the first concrete metabolism operation + CAN-008 BUFFER rule with ASTRA-004 invocation-binding requirements;
6. only after hostile review + implementation may the first positive PSEPF->V3 canary execute.

No positive V3 execution is authorized by this wave.
