# Typed unknown, routing, zero and first-consumer falsifier court

**Scope:** S0–S1 typed semantics plus proposed future canaries. The labels in the table are explicitly marked **CURRENT CODE** when observed in inspected protected modules, or **REQUESTED EXTERNAL TYPE** when an original source/issuance gap needs its own ledger. A source-native test did **not** run here.

## 1. State discriminations that must never be conflated

| Situation | Correct state/type and grade | Truth that can/cannot be asserted |
| --- | --- | --- |
| Admitted, matched eligible/condition-selected respondent cohort, all targets resolve | `SUPPORTED` — CURRENT I03 `_pre553_query_eval.py:476` | A complete raw finite-sample domain of observed counts and zeros is meaningful; source-native qualification still separate |
| Declared valid tuple has no respondents **inside a positive, supported denominator** | `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET` — CURRENT I03 cell state :506–511 | A measured sample zero; does **not** prove impossible, causal absence or zero population probability |
| Declared valid tuple has positive observed count | `OBSERVED_POSITIVE` — CURRENT I03 cell state :508–510 | Observed source-scoped count only |
| No eligible/respondent risk members, or condition selects none | `ZERO_SUPPORT` — CURRENT I03 :464–468 | Undefined conditional probability; no 0/0 → 0 or invented smoothing |
| Each target has eligible members but their common J-way risk intersection is empty | `ZERO_OVERLAP` — CURRENT I03 :456–460 | No actual same-person coexposure; not a zero-valued A×B×C cell |
| Route says target not applicable throughout scoped respondent domain | `NOT_APPLICABLE` — CURRENT I03 only on proven routing law :460–462 | Valid negative but requires original instrument owner evidence; lack of form evidence ≠ inapplicable |
| Declared target domain itself is explicitly empty | `VALID_EMPTY` — CURRENT I03 :469–471 | No meaningful positive cell distribution; don't use as data-derived proof |
| Eligible denominator positive but one or more required answers unresolved | `UNRESOLVED` — CURRENT I03 :472–474 | Distinguish target missing/DK/refusal/route mismatch; not count it as measured zero or complete-case support |
| Unasked due to survey split/ballot; source file happens to contain harmonized column | `NOT_ASKED` / `FORM_NONEXPOSURE` — REQUESTED EXTERNAL TYPE | Source owner must prove administered exposure; this is not `NO` or respondent missing-at-random |
| DK/refusal/other substantive/special value | `DK`, `REFUSAL`, `SPECIAL_CODE` — REQUESTED EXTERNAL SOURCE STATES | Retain exact physical code and missing semantics; include as category or exclusion only by original item rule |
| Repeat, multiselect, ranked/sequence, household/proxy roster | `REPEATED`, `MULTISELECT`, `RANKED`, `PROXY` — REQUESTED EXTERNAL QUALIFIER | Distinct original topology and respondent unit, never silently coercible to one yes/no |
| Original source hash/release, item route or current use warrant absent | `HELD_SOURCE_RIGHTS` / `HELD_ISSUER` — REQUESTED EXTERNAL GATE | No original read/run; not same as empirically observed zero |
| Query source/condition/proxy or cross-position target unsupported | `UNAUTHORIZED` / `NONCOMPARABLE` / `PROXY_UNQUALIFIED` — CURRENT I03 may emit negative classes, external granularity requested | No exact probability consumer; no substitution from a similar position/survey |
| Adaptive frontier or recursive descendants were not evaluated | `UNKNOWN_UNVISITED` — CURRENT `pre553_discovery_adaptive.py` policy/custody, not I03 cell state | Absence of search result is not a negative discovered rule |
| Sampling weights/design missing or unissued | `WEIGHT_ESTIMAND_HELD`, `UNCERTAINTY_UNQUANTIFIED` — REQUESTED EXTERNAL gate; latter in current query profile | RAW exact support may be described as a sample result if permitted; no survey target-population CI |
| Full empirical fact has nonpositive state | N10E `REFUSED` with no generated geometry — CURRENT `pre553_empirical_possibility_provider.py:588–615` | Provider must not smooth or silently use a synthetic proxy |

**Code nuance:** current `_cell_projection` assigns per-cell `ZERO_SUPPORT` when denominator is zero. The outer fact's `NOT_APPLICABLE`, `ZERO_OVERLAP`, `VALID_EMPTY` or `UNRESOLVED` state is authoritative context; a cell's zero-looking projection alone is not proof of a measured zero. Source-negative classifications and literal code states may differ from proposed audit labels; retain both without misrepresenting an unimplemented label as a native enum.

## 2. Finite pre-registered adversarial canaries

| ID | Input intervention | Expected exact named rejection / differentiator | Potential false-green it catches |
| --- | --- | --- | --- |
| `T01_RIGHTS` | Same complete respondent file with expired, wrong-host or other-purpose licence | Refuse before S3; state `HELD_SOURCE_RIGHTS`; no derived publication | A file hash or public download mistaken for execution grant |
| `T02_EDITION` | Replace one byte in release or change official version | C11 source/replay or identity mismatch; invalidate index/cache and consumer receipt | Stale source labels producing unchanged native fact |
| `T03_FORM` | A and C on disjoint questionnaire forms or different countries | `ZERO_OVERLAP` or proven `NOT_APPLICABLE`, never 3-way observed zero | Cartesian joining separately administered data |
| `T04_UNASKED` | One J-way target not asked/route-skipped but physical value is sentinel | Missing/route typed; `UNRESOLVED` or qualified inapplicable, not `0`/false | Treating nonexposure as negative attitude |
| `T05_DK` | DK/refusal code appears in A or B, compared with legitimate 0 | Separate source response state; eligibility/denominator changes transparently | DK silently coalesced with a valid option |
| `T06_DUP` | Duplicate physical respondent key, repeated event, household respondent reused as person | Exact denial or source-approved repeat/multiselect topology; no inflated N | Row count replacing sample-unit count |
| `T07_PAIR_NOT_TRIPLE` | Two 3-binary datasets with identical one- and two-way margins but different 3-way interaction (e.g. XOR parity vs independent 8-cell) | F4 3-way cells or exact ref differ; pairwise summaries **do not** pass as joint | Claiming F4 from F1/F2/GF1 pair fragments |
| `T08_ZERO` | Valid 3-way tuple absent, other cells positive, all source routing complete | `SUPPORTED` with `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET` for exact tuple | Zero omitted from sparse output or misclassified unsupported |
| `T09_NO_DENOM` | Condition `D=d` has zero eligible respondents | `ZERO_SUPPORT`, no number/proxy geometry | Division-by-zero laundered as 0% |
| `T10_INVERSE` | Use asymmetric 2×2 counts `[[2,1],[3,4]]` | F2 `P(A=1|D=1)=4/7`; inverse `P(D=1|A=1)=4/5`; distinct query/receipt | Reversed roles with forward denominator |
| `T11_WITNESS` | Correct source fact but substitute requested condition value or coordinate ref | C1 `ConditionValueRelationMismatch`/typed refusal, no slice | J42/R53 wrong requested condition positive |
| `T12_J_ORDER` | Permute/change one of B/C target component refs while leaving first target and consumer binding unchanged | Must reject or produce correctly distinct full-target consumer identity; escalate C1 `_validate_joint_grain` dormant check if not | Arity-only/first-target check asserting false k-way consumer |
| `T13_MULTI` | Unordered multiselect with no response event vs legitimately chosen empty set; ranked repeat | Owner route/type distinguishes; scalar path rejects, cannot classify both as the same observed answer | False-empty set or collapse of multiplicity |
| `T14_WEIGHT` | Missing weight for one denominator member, negative weight or alternate weight design | I03 governed weight rejection; weighted N10E remains held until geometry/variance qualified | Raw fallback advertised as population-weighted |
| `T15_BOUND` | Drop one expected eligible I05 candidate; cap top-k; leave recursion unvisited | Exact I05 no-drop RED / `UNKNOWN_UNVISITED`; frozen expected anti-join differs | Majority-only or successful-scored frontier masking losses |
| `T16_CONSUMER` | Swap consumer query, target use, source release, rule hash or admitted slot | Provider/C1/native coordinator refuse or exact hash differs; no re-use of original receipt | Mere producer success counted as first reader |
| `T17_TRANSPORT` | Combine two surveys/years by same numeric respondent ID or proxy-demographic alias | Source-local no-pool/refusal; no unissued cross-position fact | Identity collision and false population generalization |
| `T18_PRIVACY` | Tiny rare cell proposed for external actor/model-facing use without output permission | Do not publish; authority request/suppression, preserve internal evidence as terms permit | Privacy/redistribution restrictions lost downstream |

For T07, a deliberately sourcefree fixture can use four parity configurations each repeated twice versus all eight configurations once; **all pairwise 2×2 margins are equal**, but the exact triple distribution differs. It is a *future test design*, not a measured real dataset. Source-native T07 may only use authorized respondents and source-specific domains.

## 3. Exact first-consumer guard questions that remain open

1. `pre553_analytical_composition.py::_validate_joint_grain:699` is defined but not invoked on the examined code path. Why does `_validate_direct_grain:816` validate only `targets[0]` against `consumer_query.target_ref` for arity >1? Which current `PositionedSubjectPossibilityQuery` fields represent all target roles, and do the current C1/extension witnessed associations preclude `T12_J_ORDER`? **S1 evidence does not prove answer; independent sourcefree test required.**
2. `_pre553_query_eval.py::_target_component_value:228–248` returns `True` with an empty collection for certain multiselect/repeat topologies when no event exists. Which exact source-owned `RoutingEligibilityFact` and target `included_states` guarantee this means a legitimate empty answer rather than not asked? **Source-specific issuance required.**
3. `_pre553_query_eval.py:418–450` has condition-selected denominator members before target resolution; `UNRESOLVED` then prohibits positive distribution. Which exact D4 missing policy, if any, authorizes complete-case conditioning and a *new* denominator? **No ad-hoc downstream renormalization.**
4. `pre553_analytical_composition.py::_supported_geometry:864,921` retains null weighted fractions/context, while I03 may carry weighted supports. A weighted model request must fail closed or be independently implemented/reviewed with source-owned estimand and variance, never implicitly raw.
5. An E41 sourcefree 31/31 positive and a J42 E04 TEST_ONLY receipt are not tests of these **original respondent** cases. R53 P53T found wrong-condition and zero/unsupported false positives in historical J42/P41 paths; do not equate them to protected native source science without exact independent current first-reader evidence.

## 4. Receipt and falsifier acceptance law

Pre-register expected operation IDs and exact source/form/routing/denominator/measure/consumer identity before any run. Record **every** positive, observed-zero, structurally inapplicable, unvisited, unresolved, missing-auth and consumer-refusal line. Demonstrate each candidate change as unchanged frozen positive → injected named RED → restored positive **without modifying expected evidence**. Independence: original issuer approves data/use; separate code owner executes; nonauthor reviewer checks source-native and semantic claims; N11 has its own receiving jurisdiction.

**C6 observed tests:** none. `NOT_RUN` is the honest execution grade; this table is a reproducible falsification specification.
