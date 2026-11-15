# ZAK03S:R2:CASE:PRODUCER_MAP — who writes the structural rule and what binds it

**Linked historical T:** `ZAK03:T:0004` (`F03_QRA`), original primary owner ZAK-02. This is a current-first producer/binding case, not a new T. **Protected cut:** `6a5c12f04323d74001f9632063ec907f4fc4468e`. **Candidates:** B49 `b5600da9…`, R157 `d81bc2c6…`, PR1042 `ad17076c…`, PR1043 `0d90c247…`. **Historical cut:** `9253064bc9423a0f0ccda4fbdea43c2f54f800c6`. **Evidence:** `ZAK03S:R2:EV001..024`.

## 1. Identity and question

The question is not whether I04 has a rich schema. It does. The question is who, in the tracked protected code, actually constructs a `StructuralAdmissionRule` and its `target_use_permission_refs`, and whether any construction is bound to a selected historical QSM row/version. The answer is a producer map, not a new theory.

## 2. Historical F03 inbound and outbound fields

`resolve_question_relation_authority` takes `source_family`/`source`, `canonical_wave`/`wave`, `country_code`, `question_id`, `var_code` and an authority path/row. `apply_question_relation_authority` copies a V550 bridge row and overwrites its structural semantics from the selected QSM row.

The six coordinate fields are `driver_id`, `driver_facet_id`, `question_block_id`, `structural_domain_id`, `relation_axis_id`, `target_entity_id`. The polarity fields are `source_response_polarity`, `relation_projection_polarity`, `item_reversal`. Directional rows also set `current_directional_atom_eligible`, `allowed_as_v551_relation_evidence`, `question_relation_coverage_eligible`, `question_relation_pressure_eligible`, `structural_mapping_status`, `mapping_status`, `semantic_role`, `semantic_role_authority_status`, `v551_visible`. Non-directional/admin/blocked rows clear coordinates and set review. A QUC-certified no-match survives only if `semantic_role_authority_status=CERTIFIED`, `semantic_role=RELATION_EVIDENCE`, `current_directional_atom_eligible`, `allowed_as_v551_relation_evidence`, and `structural_mapping_status=COMPLETE`.

Authority metadata includes `question_relation_authority_joined`, resolution status, lookup key, match count, country code, `relation_use_status`, `evidence_disposition`, `authority_status`, `authority_rule_id`, `authority_version`, `authority_artifact_path`, `authority_artifact_sha256`, `authority_row_payload_hash`, review status/notes and reason. `ZAK03S:R2:EV001;EV002`.

## 3. Current I04 rule fields

`StructuralAdmissionRule` is a content-addressed dataclass. Its fields include `admission_authority_ref`, `admission_operation`, `target_use`, allowed fact/query families, required predicate/target semantics refs, `structural_target_identity_refs`, `focal_structural_proposition_ref`, `structural_semantic_identity_refs`, interpretation/transformation semantics, directionality/role semantics, `target_use_permission_refs`, allowed native scope/time/estimand/measure refs, uncertainty states, disagreement policy, negative authority refs, `required_authority_bindings`, time/geography, effective period, downstream producer/use, replay semantics, and optional compatibility refs. `ZAK03S:R2:EV003`.

The class does **not** have a `from_dict`, `to_dict`, JSON loader, or materializer. A targeted whole-file search found none. `ZAK03S:R2:EV003`.

## 4. Who actually constructs it?

Only the test fixture. `environment().mk(a)` in `tests/test_pre553_structural_admission.py` constructs the rule with:

- `admission_operation="ADMIT_EMPIRICAL_FACT_TO_STRUCTURAL_USE"`;
- `target_use="STRUCTURAL_MEDIATION_INPUT"`;
- `structural_target_identity_refs=(TARGET,)` where `TARGET=STRUCTURAL_TARGET:RESOURCE_PRESSURE`;
- `target_use_permission_refs=(PERM,)` where `PERM=TARGET_USE_PERMISSION:P`;
- a `RequiredAuthorityBinding("TARGET_USE_PERMISSION", pa.authority_ref, "TARGET_USE_PERMISSION", "ALLOW_STRUCTURAL_USE", target_use_ref=USE)`;
- `focal_structural_proposition_ref`, `structural_semantic_identity_refs`, negative and compatibility refs.

It then computes `exact = AuthorityRef("AUTH-admit", version, semantic_hash(provisional.semantic_material))` and creates `adm = authority("admit","STRUCTURAL_ADMISSION",...,digest=exact.authority_content_hash)`. The authority snapshot therefore matches the fixture rule’s own content hash. This is a self-consistent test fixture, not an external issuer and not a QSM row. `ZAK03S:R2:EV004;EV006`.

## 5. The permission-ref versus binding gap

I04 requires `target_use_permission_refs` nonempty and requires a `TARGET_USE_PERMISSION` binding. But `_authority_closure_material` collects query/fact authority refs, the requested admission authority, and `binding.authority_ref`; it does **not** add `rule.target_use_permission_refs`. The receipt copies `rule.target_use_permission_refs` as semantic fields. In the test, `PERM` is an `ExactRef` and the granting authority is a separate `AuthorityRef` with tag `AUTH-perm`.

So the actual gate is the binding, while the receipt names the declared permission ref. No equality check ties them. That is a field-level provenance gap, not a claim that the test’s `ADMITTED` result is invalid. `ZAK03S:R2:EV004;EV005;EV006`.

## 6. Receipt consumers

`RouteObligation.from_structural_admission` is a real non-test static receiver. It requires an exact `AdmissionEvaluation` and a canonical `StructuralEmpiricalAdmission`, reads decision/reason/target-use/authority/fact refs from the receipt, validates a positive rule payload, and derives route facts. It does not invoke I04. Its own callers are tests only. `ZAK03S:R2:EV007`.

`pre553_carrier_execution.materialize_public_object` is a generic exact deserializer. It supports `StructuralEmpiricalAdmission` among public schemas and re-materializes from a full canonical preimage, recomputing object id/content hash. It is not a rule producer; it needs a receipt document that some producer must supply. `ZAK03S:R2:EV008`.

`pre553_issued_workload.execute_issued_workload` runs Route B/I03/I05/Batch and does not call I04. `ZAK03S:R2:EV010`.

## 7. Selected-QSM candidates

PR1042/PR1043 `SelectedQsmRequest` is the closest selected-QSM binding. It names:

`authority_path`, `expected_file_sha256`, `expected_row_hash`, `expected_authority_version`, `expected_rule_id`, `source_family`, `canonical_wave`, `country_code`, `var_code`, `native_question_ref`, `target_use_ref`, `target_use_authority_ref`, `target_use_operation`.

`_exact_selection` checks the QSM file hash, row payload hash, authority version/rule id, positive status/disposition, source/wave/country, and a unique same-code native C11 slot. `execute_selected_qsm_route_b` then requires each I03 query to contain the selected target-use triple, checks `TARGET_USE_PERMISSION`, and calls `execute_route_b_production` (I03/I05). Its binding receipt records `i05_historical_qsm_authority_established=False` and `original35_native_or_historical_production=False`.

This is a real candidate selected-QSM→I03 path. It is not an I04 rule producer and it does not call I04. `ZAK03S:R2:EV014;EV015`.

## 8. B49/R157 and adjacent FF

B49 `select_source_rules` produces a `SelectedSourceRulePackage` of `SelectedItemRule` records with implementation id, source variable, disposition, semantic direction, routing/response status, status/reason, authority evidence refs and exact identity hash. It feeds the source-native C11 adapter. It has no `target_use_permission_refs`, structural target identity, or I04 call. `ZAK03S:R2:EV011;EV012`.

R157 `build_governed_c11_projection` builds a `GovernedC11Projection` from a validated config and sets `structural_replay=_replay_absence(doc,"structural")`. It does not construct `StructuralAdmissionRule`. `ZAK03S:R2:EV013`.

F07 `instantiate_second_canary_admission` is a real protected FF receipt producer with `admission_authority_ref`, `admission_rule_ref` and `target_use_permission_refs=[permission:STRUCTURAL_MEDIATION_INPUT]`. GT12 `make_gt2_relation_admission_rule` is an FF rule producer and explicitly states no I04/P06 call. These are adjacent owner paths, not I04. `ZAK03S:R2:EV016;EV017`.

## 9. Dispositions and next source question

**Disposition:** `OPEN_PROOF_GAP`. The rule schema, receipt receiver, deserializer and candidate selected-QSM→I03 path are real. The missing edge is a protected non-test rule producer and a selected-QSM→I04 binding. No runtime/adoption claim follows.

**Next source-only question:** does any tracked producer outside `rawlsing_next/tests/` construct a `StructuralAdmissionRule` by direct call, `replace`, `from_dict`/JSON loader, or content-addressed materializer — and does any field cite a selected QSM row/version?

## 10. Plain-English summary

Old F03 selected a QSM row and copied six structural coordinates plus polarity/eligibility into a V550 bridge row. Modern I04 defines a rich rule and can produce a receipt, but protected code never constructs that rule outside tests. The only concrete constructor is a test fixture whose authority snapshot is derived from its own rule hash. `target_use_permission_refs` are carried receipt fields; the actual gate is a separate required authority binding. The real receipt receiver and generic deserializer exist, but the receiver’s callers are tests. The closest selected-QSM binding is unmerged PR1042/1043, and it goes to I03 target-use, not I04. B49/R157 feed C11, and F07/GT12 are separate FF owners. Therefore: no protected selected-QSM→I04 producer is proved; this is a missing edge, not a missing engine.
