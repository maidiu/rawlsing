# S5 R4 NEGATIVE AND BOUNDARY TESTS R1

STATUS: `R4_NEGATIVE_LAWS_AND_PREV3_V3_BOUNDARIES__DIRECTLY_TESTED`

This file is the concentrated failure court over the 90 canonical vectors. It does not add architecture. A candidate conforms only if it passes both the positive vector and the corresponding negative ceiling here.

| Court | Canonical vectors | Must reject / preserve | Required oracle |
|---|---|---|---|
| NB-01 CATEGORY SHORTCUT | TV-001..004, 019 | `CLASS/RACE/GENDER/RELIGION/POVERTY/COUNTRY -> actor consequence` without exact relation/rule | `REJECT_CATEGORY_SHORTCUT` |
| NB-02 TITLE/ROLE SHORTCUT | TV-005..007, 016 | title/role/kinship as operative authority/task/obligation/support | reject or unknown until exact relation is supplied |
| NB-03 QUALIFICATION→REALIZATION | TV-008, 009, 018, 022, 030, 039 | eligibility/entitlement/sanctionability/schedule/tie as receipt/treatment/performance/transfer | `QUALIFY_ONLY` where realization unproved |
| NB-04 MISSING→NEGATIVE | TV-013, 031, 040, 061 | no current record as denial/nonreceipt/noncontact/nontransfer | `UNKNOWN_NOT_PROVEN` |
| NB-05 STALE→CURRENT | TV-011, 029, 038, 045, 059, 060 | expired/superseded witness sustaining current realized truth | `UNKNOWN_NOT_PROVEN` unless current witness exists |
| NB-06 STALE→NEGATIVE | TV-011, 029, 045, 059, 060 | expiry/supersession itself becoming denial/nonoccurrence | prohibit; negative needs polarity authority |
| NB-07 PRIVATE PSYCHOLOGY→WORLD | TV-046, 075, 086 | belief/motive/distress/appraisal/trait as objective social antecedent | `REJECT_PSYCHOLOGY_LEAK` |
| NB-08 CROSS-PERSON PRIVATE LEAK | TV-046 | one actor’s private state authoring another actor’s objective ecology | reject until external state/action + exact relation |
| NB-09 P2/P3 DUPLICATION | TV-021, 027, 028 | formal control scope treated as task organization or exercised discretion | preserve separate P2/P3 rule refs |
| NB-10 P4 STAGE LEAK | TV-030..037 | rule/applicability/encounter/cue/recognition/treatment/result collapsed | only exact witnessed stage may be asserted |
| NB-11 P4 GENERIC RECOGNITION | TV-088 | casual recognition/classification treated as P4 without governed gate/evaluation | reject P4 overreach |
| NB-12 GROUP RATE→ACTOR TRUTH | TV-064, 065 | population coefficient/risk estimate minting actor outcome | `WORLD_OWNER_REQUIRED` until actor result exists |
| NB-13 SOURCE CONSTRUCT→RUNTIME FACT | TV-066, 067 | occupational self-direction scale/indicator becoming actor task/authority fact | `REJECT_SOURCE_CONSTRUCT_LEAK` absent exact semantic binding |
| NB-14 COUNTERFACTUAL→CURRENT | TV-068, 069 | hypothetical promotion/projected consequence entering current biography | `COUNTERFACTUAL_ONLY` until competent current transition |
| NB-15 DIRECT V3→STRUCTURE WRITE | TV-079..081 | intention/action/personality directly changing policy/position/world fact | `WORLD_OWNER_REQUIRED` for external response |
| NB-16 TRANSITION OVER-INVALIDATION | TV-054..057 | job exit deleting household/school/care facts or history | determinant-scoped invalidation only |
| NB-17 TRANSITION UNDER-INVALIDATION | TV-054, 057, 083 | terminated/superseded determinant leaving dependent current facts alive | descendants must rederive |
| NB-18 NON-EVENT→FAKE EVENT | TV-025, 077, 078, 089, 090 | condition/relation/recurrent activity packaged as synthetic event to bypass OBL062 | `NON_EVENT_INGRESS_OPEN` |
| NB-19 OBL062 FALSE CLOSURE | TV-077, 078, 089, 090 | claiming generic non-event V3 ingress is solved | preserve open interface dependency |
| NB-20 OBJECTIVE→SUBJECTIVE COLLAPSE | TV-041..043, 073..076 | transfer/demand/event automatically becoming belief, perceived support, distress, appraisal, response | `V3_BOUNDARY` |
| NB-21 AGE/PHASE LEAK | TV-070, 072 | developmental phase changing D1' when social rule is phase-invariant | no D1' change |
| NB-22 AGE SOCIAL-RULE MISS | TV-071 | refusing age dependence when exact legal/institutional rule uses age | derive exact eligibility transition |
| NB-23 CROSS-CONTEXT GENERIC SPILLOVER | TV-050..053 | work fact altering household/school/care without P1-P5 carrier | reject missing typed path |
| NB-24 LINKED-LIFE RELATIONLESS PROPAGATION | TV-047..049 | source actor transition changing target without exact P5 relation and target rule | `REJECT_MISSING_BINDING` |
| NB-25 DERIVATION EVIDENCE LAUNDERING | TV-082..084 | qualified/weak antecedent becoming stronger realized descendant | downstream ceiling <= rule + antecedents |
| NB-26 CIRCULAR SAME-TIME SUPPORT | TV-085 | `A_t -> B_t -> A_t` with no independent seed/fixed-point authority | `REJECT_CIRCULAR_DERIVATION` |
| NB-27 RULE CURRENT→FACT CURRENT | TV-038, 060 | current constitution/rule extending stale application/fact | preserve currentness firewall |
| NB-28 CONSTITUTIVE FACT→CONTINGENT EVENT | TV-008, 015, 017, 022 | eligibility/authority/obligation/schedule requiring fake occurrence witness or implying occurrence | preserve constitutive/deontic proof vs contingent realization |
| NB-29 NEGATIVE SCOPE OVERREACH | TV-062, 063 | explicit denial/closed-world nonoccurrence generalized beyond exact actor/time/fact grain | negative authority stays scoped |
| NB-30 WORLD/MATERIAL FACT→PSYCHOLOGY | TV-014, 082 | outage/service/access fact directly minting distress/trait | stop at objective positioned consequence |

## PRE-V3 -> D1' boundary assertions

Every conforming system must preserve:

```text
ACTOR-INDEPENDENT STRUCTURAL / SOCIAL POSSIBILITY
!= D1' OBJECTIVE POSITIONED SOCIAL CONSEQUENCE
```

Direct tests: `TV-001..007`, `TV-030`, `TV-039`, `TV-064`, `TV-066`.

No category, population estimate, theory claim, source scale, title, or actor-independent possibility is itself a positive D1' fact. D1' requires exact actor/world/context/time/position binding plus an exact governed rule and all rule-required relational/institutional/history inputs.

## D1' -> V3 boundary assertions

Every conforming system must preserve:

```text
OBJECTIVE POSITIONED CONSEQUENCE
!= FIRST-PERSON AVAILABILITY
!= SUBJECTIVE PREMISE
!= REASON / GROUND
!= APPRAISAL / UPTAKE
!= RESPONSE
!= DURABLE DEVELOPMENT
```

Direct tests: `TV-041..043`, `TV-073..078`, `TV-089..090`.

Event-shaped facts may use the exact current event ingress when competent; the D1' suite never asserts that event receipt implies uptake. Persistent conditions, directed relations, and recurrent activities remain lawful D1' facts even while OBL062 is open.

## World-write boundary

Direct tests: `TV-079..081`.

```text
PRIVATE STATE OR V3 ACTION
!= STRUCTURAL / SOCIAL WORLD CHANGE

EXTERNALIZED ACTION
+ COMPETENT COUNTERPART / INSTITUTION / WORLD RESPONSE
+ NEW SOURCE-OWNED EXTERNAL FACT
-> ORDINARY ADMISSION / INVALIDATION / D1' REDERIVATION
```

No D3 owner is invented by this regression formulation.

## Negation/currentness canonical law

Direct tests: `TV-011`, `TV-013`, `TV-029`, `TV-038`, `TV-045`, `TV-058..063`.

```text
MISSING POSITIVE EVIDENCE != NEGATIVE FACT
STALE POSITIVE EVIDENCE != NEGATIVE FACT
SUPERSEDED POSITIVE EVIDENCE != NEGATIVE FACT
RULE VALIDITY != CURRENT REALIZATION
```

Negative actor truth is allowed only from explicit competent negative/denial/termination/nonoccurrence evidence or exact provenance-bearing rule-authorized closed-world semantics.

## Boundary terminal

`NEGATIVE_BOUNDARY_COURT = PASS_BY_CONSTRUCTION__90_VECTOR_CORPUS_DIRECTLY_EXERCISES_ALL_LISTED_FAILURE MODES`