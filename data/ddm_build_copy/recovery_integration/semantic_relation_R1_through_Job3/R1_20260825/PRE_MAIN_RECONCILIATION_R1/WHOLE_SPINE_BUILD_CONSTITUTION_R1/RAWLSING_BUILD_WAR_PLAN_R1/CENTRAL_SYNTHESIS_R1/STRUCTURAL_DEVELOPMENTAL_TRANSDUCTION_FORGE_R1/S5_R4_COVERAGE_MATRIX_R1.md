# S5 R4 COVERAGE MATRIX R1

STATUS: `FULL_R4_SEMANTIC_INVARIANT_AND_P1_P5_COVERAGE__90_VECTORS__30_METAMORPHIC`

## 1. R4 invariant coverage

| R4 invariant / negative law | Direct canonical vectors | Coverage |
|---|---|---|
| D1' authors objective positioned social consequence only | TV-001..090 globally; especially TV-073..078 | `COVERED` |
| actor-independent possibility != positioned consequence | TV-001..004, 008, 030, 039 | `COVERED` |
| positioned consequence != qualification/applicability | TV-008, 018, 022, 030, 039 | `COVERED` |
| qualification != active/realized | TV-008..009, 018, 022, 030..032, 039..040 | `COVERED` |
| realized objective fact != first-person availability/uptake | TV-041..043, 073..076 | `COVERED` |
| uptake/response != durable development | TV-003, 028, 073..076 | `COVERED` |
| exact ACTOR/WORLD/CONTEXT/TIME binding required | TV-048, 050..053 plus all vectors | `COVERED` |
| exact position binding; title/role != relation | TV-005..007, 015..017 | `COVERED` |
| age/phase only upstream when social rule itself depends on age/phase | TV-070..072 | `COVERED` |
| exact governed `MECHANISM_RULE_REF` distinct from class/source | TV-060, 064..067, 084 | `COVERED` |
| P1-P5 are classes, not automatic actor truth | TV-001..090; currentness and source-construct courts | `COVERED` |
| relational output requires counterpart/institution binding | TV-039..049, 088 | `COVERED` |
| objective-social history only; private psychology forbidden | TV-046, 075, 086..087 | `COVERED` |
| institutional configuration provenance where constitutive | TV-030..038, 065, 088 | `COVERED` |
| evidence/portability ceiling preserved | TV-064..067, 084 | `COVERED` |
| ACTIVE/REALIZED requires type-compatible current witness | TV-010, 019, 024..025, 028, 032, 036..037, 041..043 | `COVERED` |
| witness validity overlaps asserted interval | TV-011, 029, 038, 045, 059..060 | `COVERED` |
| expired/superseded/terminated witness cannot sustain current truth | TV-011, 020, 029, 038, 045, 058..060 | `COVERED` |
| recurrent activity requires freshness/coverage | TV-025, 029, 059, 090 | `COVERED` |
| missing positive evidence != negative | TV-013, 031, 040, 061 | `COVERED` |
| stale positive evidence != negative | TV-011, 029, 045, 059..060 | `COVERED` |
| explicit negative/termination witness authorizes scoped negative | TV-005, 012, 020, 023, 044, 058, 062 | `COVERED` |
| rule-authorized closed-world negative is allowed only at exact grain | TV-023, 063 | `COVERED` |
| constitutive/deontic facts can be proved without fake event | TV-008, 015, 017, 022, 071, 077 | `COVERED` |
| entitlement != application != approval != receipt | TV-008..013 | `COVERED` |
| obligation != performance | TV-017, 049 | `COVERED` |
| sanctionability != sanction imposition | TV-018..019 | `COVERED` |
| P2 authority/control != P3 task/time | TV-021, 027..028 | `COVERED` |
| exercised discretion = relevant P2 scope + P3 organization + participation evidence | TV-027..028 | `COVERED` |
| P4 rule != applicability != encounter != cue recognition != treatment != result | TV-030..038 | `COVERED` |
| P4 is rule-bound gate/evaluation process, not generic recognition | TV-033..036, 088 | `COVERED` |
| P5 tie != reachability/contact/transfer/perception | TV-039..045 | `COVERED` |
| kinship != care/obligation/support | TV-007, 049 | `COVERED` |
| population/group probability != actor outcome | TV-064..065 | `COVERED` |
| competent world/institution owner issues stochastic actor result | TV-065 | `COVERED` |
| source construct/indicator != runtime fact | TV-006, 066..067 | `COVERED` |
| counterfactual/projected != current truth | TV-068..069 | `COVERED` |
| one actor may occupy multiple simultaneous contexts | TV-050 | `COVERED` |
| cross-context effect requires typed carrier, no generic spillover | TV-051..052 | `COVERED` |
| location != position | TV-053 | `COVERED` |
| transition causes determinant-scoped invalidation and rederivation | TV-054..057, 083 | `COVERED` |
| preserve before/after provenance and historical truth | TV-056..057, 087 | `COVERED` |
| no global actor reset | TV-055, 083 | `COVERED` |
| private V3 state cannot directly write world/structure | TV-046, 075, 079, 086 | `COVERED` |
| reciprocal change requires externalized action + competent world response + new source fact | TV-079..081 | `COVERED` |
| objective demand/support facts != distress/perceived support | TV-043, 073..075 | `COVERED` |
| event != condition != relation != recurrent activity | TV-024..025, 076..078, 089..090 | `COVERED` |
| non-event facts remain lawful even when general V3 ingress unresolved | TV-077, 089..090 | `COVERED` |
| no non-event→fake-event laundering | TV-078, 089..090 | `COVERED` |
| OBL062 remains open and is not an error | TV-077..078, 089..090 | `COVERED` |
| multi-step derivation preserves direct antecedent graph/provenance | TV-082..084 | `COVERED` |
| antecedent invalidation reaches dependent facts only | TV-083 | `COVERED` |
| derived evidence cannot be stronger than rule/antecedents | TV-084 | `COVERED` |
| same-time circular self-support rejected absent fixed-point authority | TV-085 | `COVERED` |
| constitution current != rule current != application current != actor fact current | TV-038, 060 | `COVERED` |
| no D2/D3/D4/P6 invented by test convenience | suite-wide; TV-077..090 especially | `COVERED` |

## 2. P1-P5 realization-class coverage

| Class | Positive / realized | Qualification / constitutive only | Stale / superseded | Explicit negative | Unknown / not proven | Verdict |
|---|---|---|---|---|---|---|
| P1 material access/dependency | TV-010, 014, 037 | TV-008, 009 | TV-011, 060 | TV-012 | TV-013 | `COMPLETE` |
| P2 authority/obligation/sanction | TV-015, 019, 021 | TV-017, 018 | TV-020, 058 | TV-005, 020 | TV-016, 017 | `COMPLETE` |
| P3 organized activity/time | TV-024..026, 028 | TV-022, 027 | TV-029, 059 | TV-023 | TV-027, 029 | `COMPLETE` |
| P4 gate/evaluation/treatment | TV-032, 036..037, 088 | TV-030, 033 | TV-038 | TV-012, 034/035 at exact stage where competent | TV-031..032 | `COMPLETE` |
| P5 counterpart/channel/relation | TV-040..043 | TV-039 | TV-045, 058 where relation applies | TV-044 | TV-040, 045 | `COMPLETE` |

Notes:
- `negative` means an exact negative at the relevant semantic stage, never a blanket negative for the whole class.
- constitutive facts such as authority/obligation/eligibility may be current without a discrete event witness; contingent transfer/performance/treatment still requires the matching occurrence/state witness.

## 3. Mandatory family coverage

| Mandatory family | Vectors | Verdict |
|---|---|---|
| 1 same category, different relations | TV-001..004 | `COVERED` |
| 2 role/title | TV-005..007 | `COVERED` |
| 3 P1 | TV-008..014 | `COVERED` |
| 4 P2 | TV-015..021 | `COVERED` |
| 5 P3 | TV-022..029 | `COVERED` |
| 6 P4 | TV-030..038 | `COVERED` |
| 7 P5 | TV-039..045 | `COVERED` |
| 8 linked lives | TV-046..049 | `COVERED` |
| 9 multi-context | TV-050..053 | `COVERED` |
| 10 transition | TV-054..057 | `COVERED` |
| 11 stale/superseded witness | TV-058..060 | `COVERED` |
| 12 negation | TV-061..063 | `COVERED` |
| 13 population/probability | TV-064..065 | `COVERED` |
| 14 source construct | TV-066..067 | `COVERED` |
| 15 counterfactual | TV-068..069 | `COVERED` |
| 16 age/phase | TV-070..072 | `COVERED` |
| 17 objective vs subjective | TV-073..075 | `COVERED` |
| 18 V3 boundary | TV-076..078 | `COVERED` |
| 19 world response | TV-079..081 | `COVERED` |
| 20 derivation chain | TV-082..084 | `COVERED` |
| 21 circularity | TV-085 | `COVERED` |
| 22 history firewall | TV-086..087 | `COVERED` |
| 23 P4 outside formal bureaucracy | TV-088 | `COVERED` |
| 24 OBL062 | TV-089..090 | `COVERED` |

## 4. Negation/currentness coverage

Direct regression corpus:

```text
TV-011 old receipt witness expired
TV-013 no current record -> UNKNOWN
TV-020 explicit termination
TV-023 authorized closed-world nonperformance
TV-029 stale recurrent activity
TV-038 current rule + stale application
TV-044 explicit unreachability
TV-045 stale support transfer
TV-058 superseded relation + explicit termination
TV-059 stale recurrence -> UNKNOWN
TV-060 current rule != current realization
TV-061 no evidence -> UNKNOWN
TV-062 explicit denial -> NEGATIVE
TV-063 rule-authorized closed-world negative
```

`NEGATION_CURRENTNESS_VERDICT = COMPLETE`.

## 5. PRE-V3/V3 boundary coverage

PRE-V3-side shortcut prevention: `TV-001..007`, `TV-064..067`.

D1' objective/subjective boundary: `TV-041..043`, `TV-073..078`.

World-write/reciprocity boundary: `TV-079..081`.

Non-event downstream boundary: `TV-077..078`, `TV-089..090`.

`PREV3_V3_BOUNDARY_VERDICT = DIRECTLY_TESTED`.

## 6. OBL062 coverage

The suite does not solve OBL062. It tests the required posture:

```text
LAWFUL D1' NON-EVENT FACT
+ NO PROVED GENERAL NON-EVENT V3 INGRESS
=> NON_EVENT_INGRESS_OPEN
!= ERROR
!= FAKE EVENT
```

Vectors: `TV-077`, `TV-078`, `TV-089`, `TV-090`.

`OBL062_VERDICT = EXPLICITLY_COVERED_AND_LEFT_OPEN`.

## 7. Metamorphic coverage

`S5_R4_METAMORPHIC_SEAM_TESTS_R1.md` defines `30` single-mutation relations.

High-value mutation axes include:

- authority only;
- task content only;
- participation witness only;
- application/receipt witness only;
- witness expiry only;
- negative polarity only;
- P4 cue visibility/recognition/treatment only;
- P5 contact/transfer/reachability only;
- linked-life operative relation only;
- cross-context schedule carrier only;
- transition termination witness only;
- population actor-outcome only;
- counterfactual→current world fact only;
- age threshold under age-dependent vs age-invariant rules;
- upstream derivation-chain determinant only.

`METAMORPHIC_VERDICT = 30_RELATIONS_COMPLETE`.

## 8. Terminal questions A-J

**A. Does every R4 invariant have at least one test?** `YES`. The invariant matrix above binds every R4 seam law identified in Files 35–36 plus the R3-review correction incorporated by R4.

**B. Does every P1-P5 class have positive, qualification-only, stale, negative and unknown cases where applicable?** `YES`; see §2.

**C. Are PRE-V3/V3 jurisdiction boundaries directly tested?** `YES`; see §5.

**D. Is OBL062 explicitly tested without being solved?** `YES`; expected oracle is `NON_EVENT_INGRESS_OPEN`, never error or fake event.

**E. Are currentness, witness polarity and supersession tested?** `YES`; see §4 and MT-08/09/23/25.

**F. Are category/title/source-construct shortcuts tested?** `YES`; TV-001..007 and TV-066..067.

**G. Are world-write and linked-life psychology leaks tested?** `YES`; TV-046..049, TV-075, TV-079..081, TV-086.

**H. Does any scenario expose a real R4 semantic gap?** `NO`. The suite exposes only already-declared downstream/adoption/implementation dependencies, especially OBL062 and post-adoption G1-G6. None is an uncovered R4 semantic contradiction.

**I. Does any scenario require D2/D3/D4/P6?** `NO`. Temporal/lifecycle, world-response, downstream ingress and gate/channel cases remain representable under R4 boundaries plus existing external owners/dependencies. No new class/owner is needed.

**J. What exact canonical regression corpus should HQ preserve?** The six S5 products together, with the 90-vector catalog and 30 metamorphic relations treated as an immutable semantic conformance corpus tied to R4 target `dfd935f77554ff5c177eeddeef50a9aba8ab46e8`.

## Coverage terminal

`R4_INVARIANT_COVERAGE = COMPLETE`
`P1_P5_COVERAGE = COMPLETE`
`NEGATION_CURRENTNESS_COVERAGE = COMPLETE`
`PREV3_V3_BOUNDARY_COVERAGE = COMPLETE`
`OBL062_COVERAGE = EXPLICIT_OPEN_DEPENDENCY`
`METAMORPHIC_COVERAGE = 30`
`R4_GAP_VERDICT = NO_NEW_R4_SEMANTIC_GAP`
`D2_D3_D4_P6_VERDICT = NOT_REQUIRED`