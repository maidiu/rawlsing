# S5 R4 CANONICAL CONFORMANCE SUITE R1

STATUS: `CANONICAL_SEMANTIC_REGRESSION_CORPUS__READY`

CAMPAIGN: `STRUCTURAL_DEVELOPMENTAL_TRANSDUCTION_FORGE_R1`

WORKER: `agent/rabochii-sdtf-r1-r4-s5-seam-conformance-regression`

COORDINATOR START: `02d4a75c030ed22da48b64718618242fc10ad858`

FROZEN R4 TARGET: `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`

CANDIDATE UNDER TEST: `OBJECTIVE_POSITIONED_SOCIAL_CONSEQUENCE_DERIVATION_CONSTITUTION@1.0.0-CANDIDATE.R4`

## 1. Purpose and non-purpose

This suite is a semantic conformance court for the PRE-V3 -> D1' -> V3 seam. It is not a generic software unit-test suite and does not prescribe implementation language, storage, APIs, execution engines, or production runtime.

Every vector asks exactly:

> Would the proposed Rawlsing system author the correct objective social fact for this actor, with the correct truth/assertion status, provenance, temporal form, currentness, negation semantics, and V3 boundary?

The suite does not adopt R4, create production mechanism rules, solve OBL062, or create D2, D3, D4, P6, a generic event generator, a generic social-capital object, a theory-name operator, or any new person-side owner.

## 2. Authority basis

The suite was derived from the mandatory corpus only:

- `35_MINIMAL_PREV3_V3_TRANSDUCTION_CONSTITUTION_CANDIDATE_R4.md` at the commissioned coordinator state;
- `36_FINAL_HQ_ADOPTION_READINESS_PACKET_R2.md`;
- `16_SOCIAL_CAUSAL_HOSTILE_SCENARIO_COURT_R1.md`;
- `27_SECOND_PASS_CORPUS_COMPLETENESS_AND_CONTRADICTION_AUDIT_R1.md`;
- `28_SECOND_PASS_ARCHITECTURE_MINIMALITY_AND_JURISDICTION_AUDIT_R1.md`;
- `32_THIRD_PASS_RULE_FACT_STATUS_NEGATION_AND_DERIVATION_AUDIT_R1.md`;
- `R3_FINAL_REVIEW_SOURCE_REGRESSION_AND_SCENARIO_REPLAY_R1.md` at R3 independent-review tip `fbe2f584589fcdfad6db6a2c4f6d761b1e7ab84a`;
- `R3_FINAL_INDEPENDENT_REVIEW_R1.md` at the same R3 review tip.

No S1-S4 return was inspected.

The R3 final review found one narrow witness-currentness/polarity defect; R4 already incorporates that correction. S5 therefore tests the corrected law as binding: stale, expired, superseded, invalidated, terminated, or insufficiently fresh positive evidence cannot sustain current realized truth and cannot be converted into a negative fact.

## 3. Governing semantic ladder

The suite treats the following inequalities as regression invariants:

```text
STRUCTURAL / SOCIAL POSSIBILITY
!= OBJECTIVE POSITIONED CONSEQUENCE
!= QUALIFIED POSSIBILITY / APPLICABILITY
!= ACTIVE / REALIZED SOCIAL STATE OR OCCURRENCE
!= FIRST-PERSON AVAILABILITY
!= PREMISE / REASON / GROUND
!= APPRAISAL / UPTAKE
!= RESPONSE
!= DURABLE DEVELOPMENT
```

Additional mandatory separations:

```text
CATEGORY != RELATION != CONSEQUENCE
TITLE != OPERATIVE AUTHORITY != TASK CONTENT
RULE VALIDITY != ACTOR APPLICATION != ACTOR FACT CURRENTNESS
QUALIFICATION != REALIZATION
ENTITLEMENT != APPLICATION != APPROVAL != RECEIPT
OBLIGATION != PERFORMANCE
SANCTION POSSIBILITY != SANCTION IMPOSITION
TIE != REACHABILITY != CONTACT != TRANSFER != PERCEIVED SUPPORT
GATE RULE != APPLICABILITY != ENCOUNTER != CUE RECOGNITION != TREATMENT != DOWNSTREAM RESULT
NO EVIDENCE != NEGATIVE EVIDENCE
SOURCE CONSTRUCT != RUNTIME WORLD FACT
POPULATION RATE != ACTOR TRUTH
COUNTERFACTUAL != CURRENT TRUTH
V3 ACTION != STRUCTURAL WORLD WRITE
```

## 4. Test-oracle vocabulary

These labels are **test-oracle labels only**. They are not new architecture, runtime assertion kinds, or production enums.

| Oracle | Meaning in this suite |
|---|---|
| `DERIVE_CONSTITUTIVE` | A current objective positional/deontic/constitutive fact follows from a governed rule plus competent current antecedents; no contingent occurrence witness is required unless the rule says otherwise. |
| `QUALIFY_ONLY` | Applicability/eligibility/channel possibility/scheduled possibility is established, but a contingent realization has not been proved. |
| `ACTIVE_REALIZED` | A contingent current occurrence/state is proved by a type-compatible competent witness satisfying interval/currentness/supersession rules. |
| `UNKNOWN_NOT_PROVEN` | The positive current fact is not established; lack/staleness of evidence does not authorize its negation. |
| `EXPLICIT_NEGATIVE` | A negative actor fact is proved only by competent explicit negative/denial/termination/nonoccurrence evidence or a provenance-bearing authorized closed-world rule. |
| `REJECT_INVALID_RULE` | No governed rule with compatible inputs/output/current authority exists. |
| `REJECT_MISSING_BINDING` | Actor/world/context/position/time or required counterpart/institution binding is absent or incompatible. |
| `REJECT_PSYCHOLOGY_LEAK` | Private belief, motive, distress, trait, appraisal, premise, memory, or other person-side state is being used to author an objective social fact without an admitted external carrier. |
| `REJECT_CATEGORY_SHORTCUT` | Category, title, role label, kinship label, demographic label, country/system label, or source construct is being substituted for the operative relation/rule. |
| `REJECT_SOURCE_CONSTRUCT_LEAK` | A source measurement/scale/construct is being silently treated as the actor's runtime social fact. |
| `WORLD_OWNER_REQUIRED` | A stochastic/external outcome or world change must first be authored by a competent world/institution/source owner. |
| `V3_BOUNDARY` | D1' may hold the objective fact but must stop before premise/appraisal/reason/response/development. |
| `NON_EVENT_INGRESS_OPEN` | A lawful non-event D1' fact exists, but general non-event V3 ingress remains OBL062; no fake event is allowed. |
| `COUNTERFACTUAL_ONLY` | A projected/hypothetical result is preserved as noncurrent counterfactual material and cannot enter current biography. |
| `REJECT_CIRCULAR_DERIVATION` | Same-time self-supporting derivation is rejected absent explicit iterative/fixed-point authority. |

## 5. Assertion/truth-status vocabulary

Also test-only, not architecture:

```text
CONSTITUTIVE_CURRENT
QUALIFIED_NOT_REALIZED
REALIZED_CURRENT
EXPLICIT_NEGATIVE_CURRENT
UNKNOWN_CURRENT
HISTORICAL_NOT_CURRENT
COUNTERFACTUAL_NONCURRENT
REJECTED_NO_FACT
BOUNDARY_ONLY
```

A vector may expect more than one lawful D1' fact while still having one primary oracle. Example: a scheduled task may be `CONSTITUTIVE_CURRENT` while actual performance is `EXPLICIT_NEGATIVE_CURRENT`.

## 6. Synthetic fixture discipline

The catalog uses synthetic fixture identifiers so the vectors are stable and replayable without pretending to register production rules.

### 6.1 Actors / worlds / contexts / time

```text
A1, A2, A3                 synthetic actors
WORLD.W1                   admitted external world
CTX.WORK                   workplace context
CTX.HOUSE                  household context
CTX.SCHOOL                 school context
CTX.CARE                   care/service context
CTX.GATE                   organized selection/evaluation context
T0 < T1 < T2 < T3          ordered fixture times
I01, I12, I23              corresponding intervals
```

### 6.2 Test-fixture rule assumptions

Each `RULE.*` identifier means: **assume for this vector only that an exact governed mechanism rule exists with the R4-required owner/version/input/binding/output/qualification/witness/lifecycle/configuration/boundary/source/negative-ceiling fields**. It does not register or authorize that rule in Rawlsing.

```text
RULE.P1.ELIGIBILITY        constitutive material/service eligibility
RULE.P1.APPROVAL           constitutive approval/entitlement state
RULE.P1.RECEIPT            contingent payment/resource receipt
RULE.P1.ACCESS             material/infrastructure-to-access consequence
RULE.P2.AUTHORITY          directed authority/control scope
RULE.P2.OBLIGATION         directed obligation/duty
RULE.P2.SANCTION           sanction possibility/imposition
RULE.P3.SCHEDULE           scheduled task/time obligation
RULE.P3.PERFORMANCE        task/activity occurrence
RULE.P3.RECURRENT          recurrent activity with freshness/coverage schema
RULE.P3.DISCRETION         exercised task discretion requires P2 scope + P3 participation
RULE.P4.GATE               governed selection/evaluation/treatment ladder
RULE.P5.CHANNEL            relation/reachability/contact/channel use
RULE.P5.TRANSFER           information/support/provision transfer
RULE.LINKED                cross-person objective propagation through exact P5 relation
RULE.CROSSCTX              typed cross-context carrier rule
RULE.TRANSITION            determinant-scoped transition invalidation/rebinding
RULE.CHAIN                 multi-step derivation with direct antecedent provenance
RULE.AGE.ELIGIBILITY       objective social rule whose applicability changes at legal age
RULE.WORLD.RESPONSE        consumes competent source-authored institutional/world response
```

### 6.3 Witness notation

```text
WIT+.<id>   competent positive witness
WIT-.<id>   competent explicit negative/denial/termination/nonoccurrence witness
WIT~.<id>   positive witness that is stale/expired/superseded/invalidated for asserted interval
NONE        no witness
```

For `ACTIVE_REALIZED`, the positive witness must be type-compatible, overlap the asserted interval, satisfy freshness/recurrence coverage, and remain unsuperseded/unexpired/uninvalidated. `WIT~` never becomes negative evidence by staleness alone.

### 6.4 Provenance minimum

Every expected positive fact must preserve at least:

```text
actor + world + context + position + valid time
+ exact RULE.* fixture ref
+ direct source/antecedent refs
+ counterpart/institution/config refs when relational or institutional
+ witness refs when contingent realization is claimed
+ objective-social-history refs when explicitly consumed
+ assertion/temporal/lifecycle status
```

Rejection/unknown vectors preserve a diagnostic provenance trail sufficient to show **why** no current fact was authored.

## 7. Canonical temporal-form court

The suite directly tests:

- `EVENT` — gate decision, sanction imposition, receipt, contact, transfer, discrete task instance;
- `CONDITION` — eligibility/resource/access/current constraint;
- `DIRECTED_RELATION` — authority, obligation, tie/channel relation;
- `RECURRENT_ACTIVITY` — repeated task/practice with recurrence identity and freshness;
- `TRANSITION` — job exit, relation termination, rule change;
- `ORDERED_HISTORY/TRAJECTORY` — prior external institutional/social history used only when an exact rule consumes it;
- `TURNING_POINT` — never primitive here; only a derived description downstream of a transition/history if earned;
- `CUMULATIVE_PROCESS` — typed iteration/history, not a single omnibus exposure.

A non-event fact must remain a non-event. Event packaging is not a laundering device for OBL062.

## 8. Canonical conformance decision procedure

For each vector, conformance requires this order:

```text
1. Validate actor/world/context/position/time bindings.
2. Validate exact governed mechanism-rule assumption and class P1-P5 composition.
3. Validate required counterpart/institution/configuration bindings.
4. Validate objective-social-history inputs; reject private psychology.
5. Determine assertion kind: constitutive/qualified/contingent realized/resultant active.
6. If ACTIVE/REALIZED, validate witness type, polarity, interval overlap, currentness,
   freshness/recurrence coverage, supersession, termination and invalidation.
7. Apply open-world negation law unless exact closed-world negative semantics are authorized.
8. Assign temporal form and provenance.
9. Apply determinant-scoped invalidation semantics.
10. Stop at the V3 boundary; do not mint premise/appraisal/response/development.
11. For non-event V3 ingress, report NON_EVENT_INGRESS_OPEN rather than fabricate an event.
```

## 9. Failure signatures this suite must detect

A candidate implementation/specification fails conformance if any vector reveals:

```text
DIRECT_CATEGORY_SHORTCUT
TITLE_OR_ROLE_SHORTCUT
QUALIFICATION_TO_REALIZATION_LEAK
MISSING_TO_NEGATIVE_LEAK
STALE_WITNESS_CARRY_FORWARD
PRIVATE_PSYCHOLOGY_TO_SOCIAL_WORLD_LEAK
P2_P3_DUPLICATION_OR_COLLAPSE
P4_GATE_STAGE_LEAK
GROUP_RATE_TO_ACTOR_TRUTH_LEAK
DIRECT_V3_TO_STRUCTURE_WRITE
TRANSITION_OVER_INVALIDATION
NON_EVENT_TO_FAKE_EVENT_LAUNDERING
SOURCE_CONSTRUCT_TO_RUNTIME_FACT_LEAK
COUNTERFACTUAL_TO_CURRENT_TRUTH_LEAK
SOURCE_CITATION_TO_EXECUTABLE_RULE_LEAK
RULE_VALIDITY_TO_ACTOR_FACT_CURRENTNESS_LEAK
CROSS_CONTEXT_GENERIC_SPILLOVER
CROSS_PERSON_RELATIONLESS_PROPAGATION
DERIVATION_EVIDENCE_LAUNDERING
SAME_TIME_CIRCULAR_SELF_SUPPORT
```

## 10. Corpus identity

The canonical S5 regression corpus is:

```text
S5_R4_CANONICAL_CONFORMANCE_SUITE_R1.md
S5_R4_TEST_VECTOR_CATALOG_R1.md          # 90 canonical vectors
S5_R4_METAMORPHIC_SEAM_TESTS_R1.md      # 30 single-mutation relations
S5_R4_NEGATIVE_AND_BOUNDARY_TESTS_R1.md
S5_R4_COVERAGE_MATRIX_R1.md
S5_RETURN_TO_VOZHD_R1.md
```

No test label in this corpus is an architectural owner. The frozen R4 target remains untouched.