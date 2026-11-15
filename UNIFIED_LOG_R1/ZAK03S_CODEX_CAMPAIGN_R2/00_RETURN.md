# ZAK-03S — UNIFIED LOG R1 return, R2 producer/binding tract

**Publication mode:** documentary-only return under `UNIFIED_LOG_R1/ZAK03S_CODEX_CAMPAIGN_R2/`. HQ publishes after intake. No commit/push, test, execution, CI, subagent, scientific function, raw respondent read or product edit.

**Exact cuts:** protected `integration/pre-main-reconciliation-r1@6a5c12f04323d74001f9632063ec907f4fc4468e`; historical `9253064bc9423a0f0ccda4fbdea43c2f54f800c6`; R1 frozen `0098b058b569471e140710f11d0efe029ecb0c50::UNIFIED_LOG_R1/ZAK03S_CODEX_CAMPAIGN_R1/`; predecessor R3 `21bbe210a068001e99785ac954618a14be93b1bc::UNIFIED_LOG_R1/ZAK03_SOURCE_AUTHORITY_RECON_R3/`; candidates `b5600da9…`, `d81bc2c6…`, `ad17076c…`, `0d90c247…`. Shared #1054 `d25836436c16efda51ca1935c1c979b396eb61bd` unchanged.

## Direct answer

**No protected non-test producer of `StructuralAdmissionRule` was found.** The only concrete constructor is the test fixture `environment()` in `rawlsing_next/tests/test_pre553_structural_admission.py`, which builds the rule, computes its content hash, and creates a matching `AUTH-admit` `AuthoritySnapshot` of kind `STRUCTURAL_ADMISSION`. That is a self-consistent fixture object, not a selected QSM row and not a production issuer. `ZAK03S:R2:EV001;EV002;EV003;EV004`.

**`target_use_permission_refs` are not produced by I04 itself.** In I04 they are a required field of the rule and a carried field of the receipt. The actual gate is a separate `RequiredAuthorityBinding` whose `authority_kind="TARGET_USE_PERMISSION"` is resolved and checked against the exact `target_use_ref`. The receipt copies `rule.target_use_permission_refs`, but `_authority_closure_material` does not automatically include those refs. The test fixture happens to use a permission `ExactRef` and a separate permission `AuthorityRef` with the same tag. This is a **declared-ref versus checked-binding gap**, not proof that the receipt’s permission refs were the granting authority. `ZAK03S:R2:EV002;EV005;EV006`.

**The only selected-QSM→current binding found is candidate-only and goes to I03, not I04.** PR1042/PR1043’s `SelectedQsmRequest` binds exact QSM `authority_path`, `expected_file_sha256`, `expected_row_hash`, `expected_authority_version`, `expected_rule_id`, source family/wave/country/variable and a native question ref. It requires the selected QSM row’s status/disposition/source scope to match and then requires a **separate caller-supplied current target-use permission triple** on each I03 query. It calls `execute_route_b_production` (I03/I05); it does not construct a `StructuralAdmissionRule` or call I04. `ZAK03S:R2:EV007;EV008;EV009`.

**B49 and R157 are real source-rule producers, but not I04 rule producers.** Candidate B49 `select_source_rules` produces a `SelectedSourceRulePackage` of `SelectedItemRule` records (implementation id, source variable, disposition, semantic direction, routing/response status, evidence refs, exact identity hash) and feeds the source-native C11 adapter. R157’s factory produces a `GovernedC11Projection` and uses a typed structural replay absence. Neither emits `StructuralAdmissionRule`, `RequiredAuthorityBinding`, or I04 `target_use_permission_refs`. `ZAK03S:R2:EV010;EV011;EV012;EV013`.

**Real upstream FF/F07 producers exist but are a different owner.** `f07_second_canary_prev3_admission.py` constructs a claim-specific FF relation-admission receipt with its own `admission_authority_ref`, `admission_rule_ref` and `target_use_permission_refs=[permission:STRUCTURAL_MEDIATION_INPUT]`; `wave1_ff_prev3_relation_admission.py` has `make_gt2_relation_admission_rule` and explicitly does not call I04/P06. These are not `StructuralAdmissionRule` and do not prove an I04 path. `ZAK03S:R2:EV014;EV015`.

**The receipt side has real static readers.** `pre553_analytical_state_and_route.RouteObligation.from_structural_admission` is a real non-test static receiver of an `AdmissionEvaluation` and its canonical `StructuralEmpiricalAdmission`; it validates exact types and receipt fields and derives route facts, but its own callers are tests only. `pre553_carrier_execution.materialize_public_object` is a generic deserializer that can re-materialize a `StructuralEmpiricalAdmission` from a full canonical preimage; it is not a rule producer. The issued-workload path executes I03/I05/Batch and does not call I04. `ZAK03S:R2:EV016;EV017;EV018;EV019`.

## Five separate judgments

| # | Judgment | Count/denominator | Grade/residual |
|---|---|---|---|
| 1 | Commission/identity accounting | 14/14 inherited T references; 9/9 prior obligation IDs preserved by reference; 17/17 prior trace IDs preserved by reference | No new T. R2 is a producer/binding tract. |
| 2 | Historical capability discovery | 14 preserved T; **OPEN_DISCOVERY** | No V540–V548 or branch census. This tract adds field-level F03/QSM and current rule-producer evidence, not a new T. |
| 3 | Cross-domain matrix coverage | **21 literal rows**: **7 `FOUND`**, **1 `UNRESOLVED`**, **13 `NOT_INSPECTED`**. For T0004: 8 rows = 7 FOUND / 1 UNRESOLVED. | The 13 inherited non-T0004 rows remain NOT_INSPECTED; this is not a 154-cell recertification. |
| 4 | Mechanism/consumer reconciliation | 15 producer/consumer map edges; **0 current selected-QSM→I04 same-grain edges**; **1 real non-test receipt receiver**; **1 candidate selected-QSM→I03 edge**; **2 candidate source-rule/C11 producers**; **2 adjacent FF producers** | Producer, carrier, receipt consumer, actual runtime and adoption are separate. |
| 5 | Evidentiary/independent closure | 24 new atomic evidence rows (`ZAK03S:R2:EV001..024`); **0 S2/S3**, 0 executed runs, 0 independent reviewer | S0/S1 only. No original35/native/science/actor/merge claim. |

## Producer/consumer map (summary)

| Stage | Actual protected/candidate evidence | Grade | Missing edge |
|---|---|---|---|
| Historical F03→selected QSM row | `apply_question_relation_authority` reads source family/wave/country/question/var and copies six coords + polarity/eligibility; QUC five-conjunct preservation | S1 source | Historical execution not observed; selected file/version not recovered |
| Current I04 rule producer | Only `test_pre553_structural_admission.py::environment()` constructs `StructuralAdmissionRule` | TEST_FIXTURE | No protected non-test constructor/parser/materializer |
| I04 rule→authority | Test computes `AUTH-admit` hash from rule semantic material and creates matching `STRUCTURAL_ADMISSION` snapshot | TEST_FIXTURE | No external issuer or QSM-derived authority |
| I04→receipt | `evaluate_structural_empirical_admission` builds `StructuralEmpiricalAdmission`; only `ADMITTED` positive | STATIC/TEST | No non-test invocation |
| Receipt→route | `RouteObligation.from_structural_admission` validates exact `AdmissionEvaluation` + receipt and derives route facts | REAL_STATIC_RECEIVER | Its callers are tests only |
| Receipt→C11 | `StructuralAdmissionReplayBinding` M15; source-native adapter sets `NOT_APPLICABLE`; ingest permits absence | CARRIER_ONLY | No producer populates `PRESENT` from I04 |
| Selected QSM→I03 | PR1042/1043 `SelectedQsmRequest` binds file/row/version + separate target-use triple; calls Route B/I03 | CANDIDATE_STATIC | No I04 rule; no execution; not protected |
| Source-rule→C11 | B49 `SelectedSourceRulePackage` → native preimage adapter; R157 config → `GovernedC11Projection` | CANDIDATE_STATIC | No I04 rule; not protected |
| FF receipt/rule | F07 claim-specific receipt; GT12 FF rule; no I04 import/call | CROSS_OWNER | Not F03 empirical successor |

## Material negatives

- **A structurally rich rule is not a selected QSM by naming.** I04 rule fields (`structural_target_identity_refs`, `structural_semantic_identity_refs`, `directionality_or_role_semantics`, `target_use_permission_refs`) are content-addressed and caller-supplied; no field is a QSM row id/version.
- **`target_use_permission_refs` is not the gate.** The gate is `RequiredAuthorityBinding`; the permission refs are carried receipt semantics. The test fixture uses separate `ExactRef`/`AuthorityRef` objects. No code checks equality between them.
- **A missing direct constructor at protected is not global absence.** FF/F07 and service-applicability bindings produce related refs elsewhere, but they do not produce I04 rules.
- **No selected-QSM→I04 binding is proved.** Candidate PR1042/1043 stops at I03 target-use; B49/R157 stop at C11 projection; the I04 rule has no QSM import.
- **No runtime receipt.** No S2, no executed Batch/Route-B receipt, no current original issuer grant.

## Explicit unfinished cells

- Exact historical selected QSM file/version/row payload and original F03 execution receipt: **UNKNOWN**.
- Protected non-test `StructuralAdmissionRule` producer/parser/deserializer: **NOT_FOUND at declared protected scope**.
- Protected non-test `evaluate_structural_empirical_admission` invocation: **NOT_FOUND at declared protected scope**.
- Non-test caller of `RouteObligation.from_structural_admission`: **NOT_FOUND**; receiver callers are tests.
- C11 M15 `PRESENT` binding produced from an `ADMITTED` evaluation: **NOT_PROVED**; R1 recorded the protected source-native adapter setting `NOT_APPLICABLE` (`ZAK03S:EV107`).
- Candidate PR1042/1043 execution and adoption: **NOT_RUN / NOT_PROTECTED**.
- B49/R157 adoption: **NOT_PROVED**.
- V540–V548, intermediate branches, foreign SOROK/world/learned/temporal: **NOT_INSPECTED**.
- Reviewer: **NOT_RECEIVED**.

## One precise next source-only question

**Within the frozen protected cut, does any tracked producer outside `rawlsing_next/tests/` construct a `StructuralAdmissionRule` by direct call, dataclass `replace`, a `from_dict`/JSON loader, or a content-addressed materializer — and if so, does any field of that construction cite a selected QSM row/version or only caller-supplied refs?** This is a source-search question, not an execution request.

## Terminal completion sentence

**Contract identities:** 14/14 inherited T and 9/9 obligations by reference. **Historical discovery:** OPEN at declared scope; R2 closes the finite producer/binding question, not global T discovery. **Applicable T×domain matrix:** 21 rows (7 FOUND, 1 UNRESOLVED, 13 NOT_INSPECTED); T0004 8 rows (7/1/0). **Mechanism and consumer reconciliation:** 15 map edges; 0 selected-QSM→I04 same-grain; 1 real non-test receipt receiver; 1 candidate selected-QSM→I03; 2 candidate source-rule/C11 producers; 2 adjacent FF producers. **Independent evidence grade:** S0/S1 static documentary only; no S2/S3, native run, science/actor issuance or reviewer. **Legitimate future use:** exact owner-targeted source search for any non-test rule constructor and provenance of its fields. **Cannot claim:** selected QSM→I04 equivalence, current admission execution, whole-machine loss, native original35, adoption or protected integration.

**Disposition:** `ZAK03S_R2_RULE_PRODUCER_BINDING__NO_PROTECTED_NON_TEST_RULE_PRODUCER__OPEN_PROOF_GAP`.
