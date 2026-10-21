"""S2 DTA household/person unit/risk/occurrence shape."""
from __future__ import annotations

from pathlib import Path

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_empirical_objects import EmpiricalUniverse, ExactRef, RoutingEligibilityFact
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState, decode_dta
from rawlsing_next.pre553_source_backed_c11_facade import (
    CoordinateSlotRule, CoordinateValueRule, GovernedC11Projection, OccurrenceRule, PhysicalSlot,
    ResponseSlotRule, ResponseValueRule, RowRespondentBinding, WeightSlotRule,
    WeightValueRule, physical_value_binding_key,
)
from rawlsing_next.tests.test_pre553_empirical_query import _auth, _ref


def _authorities(tag):
    source = _auth(f"{tag}-source", "SOURCE_SEMANTICS_TOPOLOGY",
                   families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"))
    mapping = _auth(f"{tag}-mapping", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
                    families=("RespondentEvent@1.0.0",))
    coord = _auth(f"{tag}-coord", "COORDINATE_SEMANTICS",
                  families=("EmpiricalCoordinateFact@1.0.0",))
    routing = _auth(f"{tag}-routing", "ROUTING_RISK_SET",
                    families=("RoutingEligibilityFact@1.0.0",))
    weight = _auth(f"{tag}-weight", "WEIGHT_DESIGN_ESTIMAND",
                   families=("WeightMeasureFact@1.0.0",))
    replay = _auth(f"{tag}-replay", "REPLAY_PROTOCOL",
                   families=("ReplayReceipt@1.0.0",))
    projection = _auth(f"{tag}-projection", "SOURCE_SEMANTICS_TOPOLOGY",
                       families=("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0",
                                 "WeightMeasureFact@1.0.0"))
    return (source, mapping, coord, routing, weight, replay, projection)


def build_person(path) -> dict:
    path = Path(path)
    incidence = decode_dta(path)
    tag = "ur-b-s2-person"
    auths = _authorities(tag)
    source_auth, mapping_auth, coord_auth, routing_auth, weight_auth, replay_auth, projection_auth = auths
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,), dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"{tag}-universe"),
        raw_source_identity=f"RAW-{tag}", source_family="SURVEY",
        study_product_release=f"STUDY-{tag}/REL-1", instrument_release=f"INST-{tag}",
        country_geography="ZZ", sampling_geography="ZZ-NATIONAL", raw_wave="W1",
        canonical_wave_if_governed=None, field_or_reference_time="2026-01",
        target_population_and_sample_frame="SYNTHETIC-PERSONS",
        sampling_design_regime="TEST-ONLY", respondent_namespace=f"NS-{tag}",
        source_artifact_import_lineage=f"LINEAGE-{tag}",
        harmonization_authority_ref=None, source_relation_refs=())
    qrefs = {name: _ref("QUESTION_NATIVE", f"{tag}-{name}")
             for name in ("OUTCOME", "PITEM", "PITEM_B")}
    questions = tuple(
        QuestionVariableBinding(
            empirical_universe_ref=universe.ref, native_question_ref=qrefs[name],
            instrument_question_version="1",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=source_auth.authority_ref,
            topology_authority_ref=source_auth.authority_ref)
        for name in qrefs)
    qbind = dict(zip(qrefs, questions))
    respondents = tuple(
        RespondentIdentity(
            empirical_universe_ref=universe.ref, respondent_key=f"P{i}",
            source_native_respondent_key_ref_or_typed_absence=_ref(
                "SOURCE_RESPONDENT", f"{tag}-P{i}"),
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"))
        for i in range(1, 17))
    by_id = {f"P{i}": respondents[i - 1] for i in range(1, 17)}
    risk = _ref("RISK_SET", f"{tag}-risk")
    # Person item is eligible only for person unit p=1 (row odd ordinals).
    routing = []
    for q in qrefs:
        for i, (rid, respondent) in enumerate(by_id.items(), 1):
            eligible = q == "OUTCOME" or ((i - 1) % 2 == 1)
            state = "ELIGIBLE_APPLICABLE" if eligible else "NOT_ELIGIBLE"
            routing.append(RoutingEligibilityFact(
                typed_state=state,
                authority_snapshot_refs=(routing_auth.authority_ref,), dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref(
                    "REPLAY_ROOT", f"{tag}-routing-{rid}-{q}"),
                empirical_universe_ref=universe.ref, scoped_respondent_ref=respondent.ref,
                question_or_target_ref=qrefs[q], risk_set_ref=risk,
                routing_rule_ref=_ref("ROUTING_RULE", f"{tag}-{q}"),
                applicability_state=state, routing_state=state, parent_predicate_refs=(),
                member_set_replay_ref=_ref("MEMBER_SET", f"{tag}-{q}-{state}")))
    variables = {v.name: v for v in incidence.variables}
    cells = {(c.row_ordinal, c.variable_name): c for c in incidence.iter_cells()}

    def pkey(name, row, value):
        cell = cells[(row, name)]
        if cell.raw_value != value and cell.missing_state is not PhysicalMissingState.SYSTEM_MISSING:
            raise AssertionError((name, row, value, cell.raw_value, cell.missing_state))
        return physical_value_binding_key(cell.raw_value, cell.missing_state,
                                          cell.source_missing_declaration)

    def slot(name, values, missing=True):
        physical = PhysicalSlot(variables[name].ordinal, name)
        rules = []
        for value in values:
            cell = next(c for (r, n), c in cells.items()
                        if n == name and c.raw_value == value
                        and c.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE)
            rules.append(ResponseValueRule(
                physical_value_binding_key(cell.raw_value, cell.missing_state,
                                           cell.source_missing_declaration),
                "SUBSTANTIVE_RESPONSE",
                (OccurrenceRule("0", _ref("TOPOLOGY", f"{tag}-{name}-scalar"),
                                {"kind": "SCALAR_SINGULAR", "index": 0}),),
                str(int(value)), mapping_auth.authority_ref))
        if missing:
            miss = next(c for (r, n), c in cells.items()
                        if n == name and c.missing_state is PhysicalMissingState.SYSTEM_MISSING)
            rules.append(ResponseValueRule(
                physical_value_binding_key(miss.raw_value, miss.missing_state,
                                           miss.source_missing_declaration),
                "MISSING",
                (OccurrenceRule("0", _ref("TOPOLOGY", f"{tag}-{name}-scalar"),
                                {"kind": "SCALAR_SINGULAR", "index": 0}),)))
        return ResponseSlotRule(physical, qbind[name], tuple(rules))

    response_slots = (
        slot("OUTCOME", (0.0, 1.0, 2.0), missing=False),
        slot("PITEM", (0.0, 1.0, 2.0), missing=True),
        slot("PITEM_B", (0.0, 1.0, 2.0), missing=True),
    )
    weight_values = tuple(
        WeightValueRule(physical_value_binding_key(float(v), PhysicalMissingState.OBSERVED_STORAGE_VALUE), v)
        for v in range(1, 9))
    projection = GovernedC11Projection(
        projection_identity_ref=_ref("C11_SEMANTIC_PROJECTION", tag),
        source_artifact_id=f"SOURCE-{tag}", expected_source_sha256=incidence.source_sha256,
        source_family_id="SURVEY", study_product_id=f"STUDY-{tag}",
        release_id=f"REL-{tag}", instrument_release_id=f"INST-{tag}",
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:test:{tag}:snapshot", incidence.source_sha256),
        universes=(universe,), respondents=respondents,
        row_bindings=tuple(RowRespondentBinding(i, respondents[i - 1].ref)
                           for i in range(1, 17)),
        questions=questions, response_slots=response_slots,
        coordinate_slots=(CoordinateSlotRule(
            PhysicalSlot(variables["HID"].ordinal, "HID"),
            _ref("COORDINATE_NATIVE", f"{tag}-HID"),
            _ref("UNIT_TAXONOMY", f"{tag}-HID"), "2026-01",
            coord_auth.authority_ref, copy_observed_raw=True,
            normalization_ref=mapping_auth.authority_ref,
            values=tuple(CoordinateValueRule(
                physical_value_binding_key(float(v), PhysicalMissingState.OBSERVED_STORAGE_VALUE),
                "OBSERVED_COORDINATE", str(v)) for v in range(8))),),
        routing=tuple(routing),
        weight_slots=(WeightSlotRule(
            PhysicalSlot(variables["PWEIGHT"].ordinal, "PWEIGHT"), "W",
            _ref("WEIGHT_SOURCE", f"{tag}-W"), weight_auth.authority_ref,
            weight_auth.authority_ref, _ref("SCOPE", f"{tag}-W"),
            values=weight_values),),
        authority_snapshots=auths, source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"),
        structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(a.authority_ref for a in auths),
        projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay_auth.authority_ref,
        tie_order_ref=_ref("ORDER_RULE", f"{tag}-canonical-ref-sort"),
        replay_protocol_version="1.0.0")
    source = {"universe": universe, "respondents": by_id, "qrefs": qrefs,
              "risk_refs": {"R": risk}, "source_auth": source_auth,
              "authorities": auths, "coord_auth": coord_auth,
              "crefs": {"HID": _ref("COORDINATE_NATIVE", f"{tag}-HID")}}
    return {"incidence": incidence, "projection": projection, "source": source,
            "authorities": auths, "risk": risk, "qrefs": qrefs}


def build_household(path) -> dict:
    path = Path(path)
    incidence = decode_dta(path)
    tag = "ur-b-s2-house"
    auths = _authorities(tag)
    source_auth, mapping_auth, coord_auth, routing_auth, weight_auth, replay_auth, projection_auth = auths
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,), dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"{tag}-universe"),
        raw_source_identity=f"RAW-{tag}", source_family="SURVEY",
        study_product_release=f"STUDY-{tag}/REL-1", instrument_release=f"INST-{tag}",
        country_geography="ZZ", sampling_geography="ZZ-NATIONAL", raw_wave="W1",
        canonical_wave_if_governed=None, field_or_reference_time="2026-01",
        target_population_and_sample_frame="SYNTHETIC-HOUSEHOLDS",
        sampling_design_regime="TEST-ONLY", respondent_namespace=f"NS-{tag}",
        source_artifact_import_lineage=f"LINEAGE-{tag}",
        harmonization_authority_ref=None, source_relation_refs=())
    qref = _ref("QUESTION_NATIVE", f"{tag}-HMEAS")
    question = QuestionVariableBinding(
        empirical_universe_ref=universe.ref, native_question_ref=qref,
        instrument_question_version="1",
        canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
        component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        semantic_authority_ref=source_auth.authority_ref,
        topology_authority_ref=source_auth.authority_ref)
    respondents = tuple(
        RespondentIdentity(
            empirical_universe_ref=universe.ref, respondent_key=f"H{i}",
            source_native_respondent_key_ref_or_typed_absence=_ref(
                "SOURCE_RESPONDENT", f"{tag}-H{i}"),
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"))
        for i in range(1, 9))
    by_id = {f"H{i}": respondents[i - 1] for i in range(1, 9)}
    risk = _ref("RISK_SET", f"{tag}-risk")
    routing = tuple(
        RoutingEligibilityFact(
            typed_state="ELIGIBLE_APPLICABLE",
            authority_snapshot_refs=(routing_auth.authority_ref,), dependency_refs=(),
            producer_replay_locator_or_reference_root=_ref(
                "REPLAY_ROOT", f"{tag}-routing-{rid}"),
            empirical_universe_ref=universe.ref, scoped_respondent_ref=respondent.ref,
            question_or_target_ref=qref, risk_set_ref=risk,
            routing_rule_ref=_ref("ROUTING_RULE", f"{tag}-HMEAS"),
            applicability_state="ELIGIBLE_APPLICABLE",
            routing_state="ELIGIBLE_APPLICABLE", parent_predicate_refs=(),
            member_set_replay_ref=_ref("MEMBER_SET", f"{tag}-HMEAS"))
        for rid, respondent in by_id.items())
    variables = {v.name: v for v in incidence.variables}
    cells = {(c.row_ordinal, c.variable_name): c for c in incidence.iter_cells()}
    values = []
    for value in (0.0, 1.0):
        cell = next(c for c in cells.values()
                    if c.variable_name == "HMEAS" and c.raw_value == value)
        values.append(ResponseValueRule(
            physical_value_binding_key(cell.raw_value, cell.missing_state,
                                       cell.source_missing_declaration),
            "SUBSTANTIVE_RESPONSE",
            (OccurrenceRule("0", _ref("TOPOLOGY", f"{tag}-HMEAS-scalar"),
                            {"kind": "SCALAR_SINGULAR", "index": 0}),),
            str(int(value)), mapping_auth.authority_ref))
    projection = GovernedC11Projection(
        projection_identity_ref=_ref("C11_SEMANTIC_PROJECTION", tag),
        source_artifact_id=f"SOURCE-{tag}", expected_source_sha256=incidence.source_sha256,
        source_family_id="SURVEY", study_product_id=f"STUDY-{tag}",
        release_id=f"REL-{tag}", instrument_release_id=f"INST-{tag}",
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:test:{tag}:snapshot", incidence.source_sha256),
        universes=(universe,), respondents=respondents,
        row_bindings=tuple(RowRespondentBinding(i, respondents[i - 1].ref)
                           for i in range(1, 9)),
        questions=(question,),
        response_slots=(ResponseSlotRule(
            PhysicalSlot(variables["HMEAS"].ordinal, "HMEAS"), question, tuple(values)),),
        coordinate_slots=(CoordinateSlotRule(
            PhysicalSlot(variables["HID"].ordinal, "HID"),
            _ref("COORDINATE_NATIVE", f"{tag}-HID"),
            _ref("UNIT_TAXONOMY", f"{tag}-HID"), "2026-01",
            coord_auth.authority_ref, copy_observed_raw=True,
            normalization_ref=mapping_auth.authority_ref,
            values=tuple(CoordinateValueRule(
                physical_value_binding_key(float(v), PhysicalMissingState.OBSERVED_STORAGE_VALUE),
                "OBSERVED_COORDINATE", str(v)) for v in range(8))),),
        routing=routing, weight_slots=(),
        authority_snapshots=auths, source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"),
        structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(a.authority_ref for a in auths),
        projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay_auth.authority_ref,
        tie_order_ref=_ref("ORDER_RULE", f"{tag}-canonical-ref-sort"),
        replay_protocol_version="1.0.0")
    source = {"universe": universe, "respondents": by_id,
              "qrefs": {"HMEAS": qref}, "risk_refs": {"R": risk},
              "source_auth": source_auth, "authorities": auths, "coord_auth": coord_auth}
    return {"incidence": incidence, "projection": projection, "source": source,
            "authorities": auths, "risk": risk, "qrefs": {"HMEAS": qref}}
