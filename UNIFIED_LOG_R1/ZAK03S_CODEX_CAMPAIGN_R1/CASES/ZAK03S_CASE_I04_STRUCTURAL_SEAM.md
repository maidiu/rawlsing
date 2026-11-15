# ZAK03S:SEAM:I04 — current structural-admission seam and its missing selected-rule reader

**Linked historical T:** `ZAK03:T:0004` (`F03_QRA`), original primary owner ZAK-02. **This is not a new historical T.** It is a current-first mechanism/consumer case for the modern seam that most closely resembles F03 structural authorization. **Source cut:** protected `6a5c12f04323d74001f9632063ec907f4fc4468e`. **Evidence:** `ZAK03S:EV101;EV102;EV103;EV105;EV106;EV107;EV112;EV114;EV115;EV119;EV120`. **Prior F03 case:** `../../ZAK03_SOURCE_AUTHORITY_RECON_R3/CASES/ZAK03_T_0004.md`.

## 1. Identity and reason

Old F03 turned a selected QSM relation row into directional/context/administrative/blocked bridge authority. The modern protected machine has a module whose name and decision vocabulary directly address “structural admission”: `rawlsing_next/pre553_structural_admission.py` (blob `fe8f706afbb5739d026846952681081b2937e9a8`). It defines `PRE553_I04_STRUCTURAL_ADMISSION_V553@1.0.0`, a `StructuralAdmissionRule`, a 13-state decision precedence and a public `StructuralEmpiricalAdmission@1.0.0`. The reason it matters is that it may be the lawful modern owner of the structural meaning that F03 once issued — or it may be a general service seam with no F03 binding. This case determines which.

## 2. Old inbound data and knowledge

Old F03 input was a V550 bridge row keyed source family, canonical wave, country, question and variable, plus a selected QSM registry path/version/row and possible certified QUC prior evidence. It produced an authority-annotated bridge row with six structural coordinates, polarity/reversal, `RELATION_EVIDENCE`, `current_directional_atom_eligible`, `allowed_as_v551_relation_evidence`, coverage/pressure/review states, or a certified QUC preservation. The knowledge produced was: **whether this precise question may contribute directional relation evidence, contextual coverage, administrative exclusion, or permitted certified prior evidence.** See prior `ZAK03:T:0004` and `ZAK03:EV007–012`.

## 3. Modern inbound data

I04 receives:

- an exact `EmpiricalQuerySpec` and `EmpiricalFact` from I03;
- a `requested_admission_authority_ref` (`AuthorityRef`);
- a `StructuralAdmissionRule | None`;
- a `StructuralAdmissionRequest` containing native-scope, effective-time, estimand, measure/weight, support/uncertainty, interpretation-critical, conditions, discovery and legacy-compatibility refs;
- an exact `AuthorityRegistry`;
- a producer replay locator or reference root.

The rule itself requires: `admission_authority_ref`, `admission_operation`, `target_use`, allowed fact states/families/query families, exact predicate/target semantics refs, structural target identity refs, focal structural proposition ref, structural semantic identity refs, interpretation/transformation semantics, directionality/role semantics, `target_use_permission_refs`, allowed native scope/time/estimand/measure refs, uncertainty states, disagreement policy, negative authority refs, required authority bindings, time/geography, effective period, downstream producer/use, replay semantics, and optional legacy compatibility refs. `ZAK03S:EV101;EV102`.

**Concrete illustrative shape:** a rule whose `target_use` is `STRUCTURAL_RELATION`, whose `required_authority_bindings` include `TARGET_USE_PERMISSION` and `STRUCTURAL_TARGET`, and whose `structural_semantic_identity_refs` name a specific directional proposition. This is illustrative, not a selected QSM row.

## 4. Transformation and branches

`evaluate_structural_empirical_admission` verifies query/fact identity and content hashes, fact-to-query binding, universe identity, upstream authority closure, rule identity/content hash, admission authority state, rule membership of fact/query families, predicate/target semantics, native scope, effective time, estimand, measure/weight, uncertainty, each required authority binding, multi-universe source-relation authority, and legacy compatibility parity. It then chooses the first matching state in the fixed precedence:

`INTEGRITY_FAILURE` → `MISSING_STRUCTURAL_ADMISSION_AUTHORITY` → `UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY` → `ADMISSION_DENIED` → `NEGATIVE_AUTHORITY_ONLY` → `SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE` → `EMPIRICAL_FACT_NONCOMPARABLE` → `TEMPORAL_SCOPE_MISMATCH` → `STRUCTURAL_TARGET_UNRESOLVED` → `INSUFFICIENT_EVIDENCE_UNDER_RULE` → `ADMISSION_DEFERRED` → `VALID_EMPTY` → `ADMITTED`.

Only `ADMITTED` sets `positive_structural_evidence=True` and `m1_direct_projection_allowed=True`. Every other state is nonpositive but still replayable. `ZAK03S:EV101`.

**Important negative:** a valid `TARGET_USE_PERMISSION` is not enough. The rule must also bind exact structural target/semantic identity and directionality/role semantics. If the rule is missing, the state is `MISSING_STRUCTURAL_ADMISSION_AUTHORITY`; if the requested rule ref mismatches, `INTEGRITY_FAILURE`; if a required binding is unavailable, `UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY`; if the source/use scope is outside the rule, `SOURCE_NOT_APPLICABLE_TO_STRUCTURAL_USE`. `ZAK03S:EV101;EV102`.

## 5. Output and carrier

The output is `StructuralEmpiricalAdmission@1.0.0` with `admission_decision_state`, `decision_reason_code`, query/fact refs, admission authority ref, source universe refs, native scope, target use, target-use permission refs, focal structural proposition, structural semantic identity refs, temporal/estimand/measure refs, support/uncertainty, applicable negatives, interpretation-critical refs, authority closure and optional structural interpretation payload. It can be projected to a V553 participant envelope and, only when `ADMITTED`, to an M1 direct basis candidate. `ZAK03S:EV101`.

C11 can carry a `StructuralAdmissionReplayBinding` with `state` `PRESENT`/`NOT_APPLICABLE`, `structural_admission_authority_ref_or_typed_absence`, target structural producer/use ref, negative limits and transformation replay. `pre553_c11_ingest` requires the M15 section to be explicit and permits `TypedAbsence("NOT_APPLICABLE")`; it does not verify that a `PRESENT` binding came from an `ADMITTED` evaluation. `ZAK03S:EV105;EV106`.

## 6. First reader — actual result

**No direct non-test invocation of I04 was found, but a real receipt consumer exists.** A whole-tree search for `evaluate_structural_empirical_admission(` returned the definition, `rawlsing_next/tests/c1_at14_at16_fixture.py`, `test_pre553_analytical_state_and_route.py`, `test_pre553_diagnostics.py`, `test_pre553_structural_admission.py` and `test_pre553_whole_machine_hostile_acceptance.py`. Separately, `pre553_analytical_state_and_route.RouteObligation.from_structural_admission` is a real non-test static consumer of an `AdmissionEvaluation` and its canonical `StructuralEmpiricalAdmission` receipt: it requires exact owner types, reads every authoritative route fact from the receipt, validates decision/reason/target-use/authority/fact refs, and derives route facts. It does not invoke I04; its own callers are tests only. `objective_consumer_bounded_evidence.OC02` names I04 as a current seam but does not invoke it. `ZAK03S:EV103;EV114;EV115`.

The actual issued-workload reader `pre553_issued_workload.execute_issued_workload` (blob `28174766…`) admits a `NativeWorkload`, calls `execute_route_b_production`, executes `CarrierNeutralResearchExecutor.execute_i03`/`execute_i05`, and runs `BatchExecutionRunner`. It does not import or call I04. Batch receipts record unit kind, ref, state and result refs, not a structural admission. `ZAK03S:EV112;EV113`.

## 7. Selected-rule provenance

No protected code derives a `StructuralAdmissionRule` from an F03/QSM row. The rule is content-addressed and caller-supplied. The protected source-native adapter offers a `NativeSourcePackage` with `selected`/`excluded`/`held`/`unknown` rules, but its authorities are `R56-TEST-ONLY-AUTH-*` at `TEST_ONLY_SOURCEFREE`, and it sets `structural_replay=TypedAbsence("NOT_APPLICABLE")`. Protected B49 (`pre553_native_workload_binding.py`) is explicitly TEST_ONLY and uses `B49-TEST-ONLY-QUERY-AUTH`. The candidate B49 `pre553_inherited_source_rules.py` at `b5600da9…` is imported by that candidate’s adapter at line 49, but the protected adapter blob `dd0d6960…` has no such import. Candidate R157 is candidate-only. `ZAK03S:EV107;EV108;EV109;EV110;EV111`.

## 8. Mechanism comparison (summary)

| Old F03 mechanism | Modern closest operation | Relation | Crucial negative |
|---|---|---|---|
| S01 selected authority file path/version | Candidate PR1042/1043 only; no protected selector | `CANDIDATE` | Swap selected file; modern snapshot unchanged |
| S02 exact source/wave/country/question/var resolution | I03 exact C11 release + exact query/predicate; I04 exact rule | `ANALOGOUS` | Exactness of envelope ≠ same selected rule identity |
| S03 directional six-coordinate structural use | I04 structural target/semantic/directionality rule | `PARTIAL` | Same fact + same target-use but changed structural semantic must change admission |
| S04 context-only clear | I03 fact without I04 admission | `PARTIAL/ANALOGOUS` | Valid empirical fact must not be promoted to structural relation |
| S05 administrative/blocked | I04 decision precedence + I03 typed negatives | `ANALOGOUS` | Blocked/negative must not become `ADMITTED` |
| S06 QUC certified no-match | No modern five-conjunct branch found | `UNKNOWN` | Certified QUC no-match must remain eligible if full successor is claimed |

## 9. Dispositions and future utility

**Disposition:** `OPEN_PROOF_GAP` at S1 source-evidence grade. The I04 rule schema and C11 carrier are reusable structural-admission capital. The missing piece is a selected-rule/version producer and a direct non-test I04 invoker; one non-test receipt consumer exists, but its own callers are tests. This is not a recommendation to build; it is a precise owner-held question.

**Smallest discriminating check:** hold the source fact and target-use permission fixed; change `structural_semantic_identity_refs`/`focal_structural_proposition_ref`; observe whether I04 changes state. Then check whether any rule is bound to a selected historical QSM row/version. A positive answer would narrow the gap; a negative confirms a generic policy seam.

## 10. Plain-English summary

Old F03 decided whether a selected question could be used as directional relation evidence. Modern I03 decides whether an empirical query may produce a fact; its optional target-use flag is not F03. Modern I04 is a much closer structural-admission decision, with a rich rule schema and typed positives/negatives. But I04 is called only by tests, its rule is caller-supplied, and C11 can carry a `NOT_APPLICABLE` structural binding. The actual issued-workload path runs I03/I05/Batch without I04. Therefore the structural vocabulary is real, but the selected QSM→I04 binding and production reader are **NOT_PROVED**, not missing code and not a supersession.
