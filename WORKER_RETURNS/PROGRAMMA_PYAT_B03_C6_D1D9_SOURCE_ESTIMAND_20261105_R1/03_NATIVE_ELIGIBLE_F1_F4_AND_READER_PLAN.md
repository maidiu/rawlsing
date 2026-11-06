# Smallest genuinely eligible native F1–F4 operation and exact current first-reader plan

**Status: DESIGN_CONDITIONED_ON_ISSUANCE / NATIVE_NOT_RUN.** No original35 source/host/item/operation packet has been evidenced; this document specifies a falsifiable one-edition pilot, not an executed original release or licensed request. Authority cannot be minted by the proposed objects, tests or fixture results.

## 1. Eligibility gate: first find a *lawful* local source

Choose **one** original SRCxx candidate after the competent current custodian supplies a verified immutable file edition/hash, host/storage/account/purpose/terms, and science owner approves **one country/form/mode/sample frame** with exactly coexposed `D,A,B,C`. Do not pick a wave just because a fixture or current scanner can decode it. An authoritative `INAPPLICABLE` joint requires confirmed noncoexposure; absent form evidence is `HELD_UNKNOWN`.

The smallest *potential* operation bundle is:

| ID | Frozen native operation | Required evidence; positive/negative |
| --- | --- | --- |
| `C6.F1.A`, `.B`, `.C`, `.D` | Four RAW original value marginals on explicit eligible respondent masks | Source-exact complete domain and cell counts, raw denominator/observed missing; `UNRESOLVED` if incomplete |
| `C6.F2.D_TO_A` | `P(A=a | D=d)` | Predicate binds exact D coordinate and value; denominator all eligible D=d respondents with valid A exposure |
| `C6.F2.A_TO_D` | `P(D=d | A=a)` | New original query/predicate/consumer role witness and **different** A=a denominator; not a relabel |
| `C6.F2.D_TO_ABC` | `P(A=a,B=b,C=c | D=d)` (same risk as F4) | One frozen same-person/source/form joint risk; complete cell domain and explicit missing status |
| `C6.F3.MINORITY` | All eligible nonmodal/low-support cells, defined before reading outcomes | All nonmajority tuples retained; zero/low counts and refusals; no top-k pruning of licensed frontier |
| `C6.F3.XOR` | One predeclared counterpattern/XOR rule over eligible components | Genuine same-person conjunctive/XOR facts; report `FALSE` and `UNKNOWN_UNVISITED` separately |
| `C6.F3.BRANCH` | One bounded branch split, with parent/child/stop coverage | Finite K/J/D scope, ancestry, all predicted and failed children; recursion may be `INAPPLICABLE` if not permitted |
| `C6.F4.ABC_GIVEN_D` | One full J=3 contingency table of A×B×C inside D=d | Exact same respondent triple, complete Cartesian domain, positive and valid zero cells, missing/zero-overlap distinct |

These are **proposed logical identities**, not native `ExactRef`s or claimed approved Epre IDs. The source owner may issue fewer/more appropriate legitimate ops; the independent frozen expected set must follow that issuance, not this proposal by fiat. Reuse the *same observed joint* for multiple denominated projections only after identical coexposure/risk/measure/rights are proven; independently publish each governed fact/ref/consumer receipt.

### Required bounded source input

Each asserted physical respondent has one `(source_edition, country/form, respondent_key)` identity, one unit type (person/household/proxy), a source-owned D response and three A/B/C original **administered occurrences**. A long form with one row per response must be deduplicated/normalized before I03; question order/multiplicity cannot mutate person identity. Missing states, structural skip, not asked, DK/refusal, repeat and multi-response must remain typed. There is no common denominator across noncoexposed forms by mere file concatenation.

Minimal admissible source packet fields:

```text
source_id; original_file_SHA256; dataset/release/version/country/form/language/mode/fieldwork
custodian/host/account/purpose licence receipt + storage/derived-use/retention terms
questionnaire/codebook and physical variable+occurrence/value-domain/route evidence for D,A,B,C
row_key → unique respondent namespace; household/proxy/multiple/duplicate adjudication
risk/denominator policy; eligible target population; missing/DK/refusal/skip policy
RAW sample-descriptive permission OR exact weight basis + design/PSU/strata/variance permission
U_item/U_unit/U_app and E_pre original issued refs, each operation and target use
frozen expected operation IDs, source/authority/consumer identity and replay requirements
```

## 2. Current protected producer → **real code reader** (not an abstract estimator)

### Current code path for the pilot, if source-qualified

1. **Original owner/custodian produces a permitted physical+semantic release.** `rawlsing_next/pre553_source_native_preimage_adapter.py::materialize_native_preimages:524` can turn *caller-supplied* `NativeSourcePackage` and original occurrence plans into typed materials; it does **not** establish that they were administered or permitted. The existing physical path `rawlsing_next/pre553_source_backed_c11_facade.py::build_source_backed_c11_repository:656–686` consumes a `PhysicalSourceIncidence` or `ExactPhysicalCellStream` and a source-qualified `GovernedC11Projection`; it yields `C11Repository` and a validated `C11LogicalRelease.release_ref`. Every response/coordinate/routing/weight owner and source file hash must be pinned.
2. **Current I03 produces the actual native fact object** with `rawlsing_next/pre553_empirical_query.py::execute_empirical_query:434–600` over `C11Repository, EmpiricalQuerySpec, EmpiricalPredicate, AuthorityRegistry, (release_ref,)`. Query `requested_output_grain` must bind `SINGLE_UNIVERSE`, selected `RAW` or duly authorized `GOVERNED_WEIGHTED`, exact risk type, `response_state_semantics_ref`, `query_operation`, and any target-use trio. The current query checks family/operation/use permission (`:289–431`). Result: `QueryExecutionResult` with `EmpiricalFact` or typed negatives, original release and provenance/replay refs. Source physics are verified by C11; source science remains the caller/issuer obligation.
3. **J=3 respondent joint actually comes from current I03**, not a standalone speculative graph. `rawlsing_next/_pre553_query_common.py::_parse_target_plan:312–390` demands exactly three ordered `target_refs`, three typed components and a full product/joint declared domain. `rawlsing_next/_pre553_query_eval.py::_target_configuration:253–272` looks up all three target events on **the same `RespondentIdentity`**. `_evaluate_index_group:313–493` checks each component's routing, selects the condition, counts full target tuples, and refuses `UNRESOLVED` when some eligible denominator member lacks a valid tuple. `_cell_projection:502–519` marks measured-zero cells distinctly.
4. **Exact current first N10E reader (direct single conditioner):** `rawlsing_next/pre553_empirical_possibility_provider.py::provide_empirical_possibility_slice:531–631` calls `rawlsing_next/pre553_analytical_composition.py::compose_positioned_subject_possibility:1029–1236` with that same repository, original query, predicate, authority registry, release refs, `PositionedSubjectPossibilityQuery`, `PositionedSubjectPossibilityModelRule`, and `ConditionValueBindingWitness`. C1 **calls I03** (:1095–1101); the supported fact becomes `PossibilitySliceEvidence` with exact raw cell fractions (:839–924), then C1 calls the actual `evaluate_positioned_subject_possibility` (:1152–1156). N10E returns composed identity, provider receipt, consumer result; negative facts refuse with **no invented geometry** (:588–615). This is a present code call at current protected SHA.
5. **Real multi-conditioner/J=3 and F3 routes:** `rawlsing_next/pre553_universal_empirical_extension.py::provide_empirical_possibility_slice_ext:335–531` calls C1 for multi-bindings, finite I05 discovery, or recursively supplied handoff, otherwise delegates to the exact accepted provider. `rawlsing_next/pre553_learned_world_composition.py::TrustedNativeGraphCoordinator.execute:1692–1852` on a trusted *admitted* slot calls C1 (:1748) and, if the slot contains E41 input, the extension (:1750–1762), compares composed identity, source/release, target arity/order and receipt (:1763–1835). This is an **actual current reader**, not a grant for arbitrary historical J42/E04 or a proven native original35 consumption.
6. **Cold replay and no-drop:** `replay_empirical_query:603` and `replay_empirical_possibility_slice:634` compare exact output identity. Independently freeze `expected_operation_ids` before running; compare expected→I03 facts→C1/E41 receipts→N10E accepted/refused outcomes by exact source/measure/target/condition. A missing unit, wrong role, changed source hash, expired permission, missing zero cell, or wrong consumer value causes a named RED; no fixture self-oracle.

### Identity contract for each consumed product

Emit (not merely log) one immutable manifest row per legitimate operation containing:

```text
original SRCxx + current physical SHA256 + release/semantic root + country/form/route/occurrence
unique sample-unit/risk-set/member identity and eligible/complete-case denominator policy
ordered target refs, full cell domain and response-state codes; D predicate exact value/role
raw counts/cell fractions; weighted sums if allowed; strata/PSU/design/uncertainty if issued
query_ref, predicate_ref, EmpiricalFact.ref/replay_ref, C1 composed hash
N10E provider/extension receipt/ref, consumer_query/ref, model_rule_hash, consumer state/hash
all typed zero/unresolved/inapplicable/permission/negative/unvisited states and anti-join
source license/scope/expiry/consumer permission authority and measured execution grade
```

## 3. What the present receiver **does not** prove

- The current C1 direct validator `_validate_direct_grain:816–836` binds source+release and first target; the dormant `_validate_joint_grain:699–724` would check all target components against consumer conditioner count/order but is not called. The current witness verifier instead binds conditioner predicate leaves. A hostile k-way target reorder/semantic substitution needs an **independent direct route test** to decide if a real missing read contract exists. C6 has not executed that test or pronounced a runtime vulnerability.
- The current `_supported_geometry` sets weighted probability and design/estimand context to null. The reader can consume **exact RAW** cell fractions when fully resolved, but no trustworthy weighted population-probability surface follows without additional code/scientific receiving.
- `Unordered` multi-select, ranked/repeated, and routed carriers have special `_target_component_value` logic; an absent event must not be counted as an empty selected set if the actual questionnaire signifies not-asked. The source owner must issue the topology and routing contract before any positive k-way claim.
- No observed original SRCxx `A,B,C,D` coexposure, original country/form, weights, permission, frozen expected set, real native `EmpiricalFact` or native N10E consumer receipt is present in this C6 run.
- No `N9 AND N10E → N10W` actual world-conditioned service, R118 candidate receiving, J42 generalized correctness, N11 formal acceptance or Sorok causal actor operation is established by the local function call.

## 4. Finite independent acceptance sequence, once rights arrive

1. **Pre-run frozen expectation:** independent item/form/design issuer and expectation custodian sign original D/A/B/C availability, denominators, legitimate K/J/D and all allowed/blocked/unknown operation identities; publish hashes and a source-native read grant.
2. **Source admission:** permitted S3 worker resolves exact SHA/file/host, codebook, physical occurrences, row-to-respondent uniqueness and routing in one isolated authorized environment. Integrity/rights invalidation stops before publication.
3. **Compute original conditional/joint:** four marginals, forward/inverse F2, full 3-way F4, one minority/XOR and bounded branch; source-local raw first. All valid zeros and invalid/missing states present; weighted output only after D4 owner adjudication.
4. **Adversarial canaries:** wrong reverse denominator, duplicate respondent, unmatched form, question occurrence, jumbled component order, DK/not asked, zero overlap, one missing expected unit, one byte/release and authority mutation. Demonstrate positive→named RED→restored positive without repinning frozen expected facts.
5. **Exact first consumer:** replay through current N10E/C1 (and separately admitted E41/world slot if selected); assert exact target/condition/ref/receipt and model-use permission, **not only an object shape**. For weighted population requests, expect held/no positive current weighted N10E until geometry and uncertainty contract are accepted.
6. **Independent receiving:** separate nonauthor tests scientific correctness, privacy/use rights, current schema/ABI/replay, no loss and all typed refusals. N11 independently adjudicates each applicable original SRCxx gate; C6's author cannot sign that court.

## 5. Five-test historical-succession disposition

Current requirement: `ROADMAP:S01–S04,S10.1/.4,S11.2`, `GAP-001–020,042,045,047`; F1–F4 descriptive and exact first reader. Historical V550/V550J (respondent substrate and joint patterns) is valuable as an **authorized comparison oracle**, not a newly missing engine by filename. Current lawful successor is actual C11/I03 k-way and C1/N10E at **sourcefree** grade; original rights and multi-way consumer proof are unmeasured. The first reader is named above. Reuse/adapt/test the current engine before any old-code port; no new generic estimator justified. **Disposition:** `PRESENT_COMPOSED_NO_BUILD` for sourcefree counting/reading; `SCIENCE/SOURCE/HOST_OWNER_HELD` for original native operation; `EXACT_ABI_COMPARE` for complete-target C1 check; `OWNER_DECIDE` for weighted probability/variance and model use. Falsifier: an authorized original 3-item same-person query with correct frozen source design that the current I03→N10E first reader demonstrably cannot preserve, with independent failure and no adequate lawful composition.
