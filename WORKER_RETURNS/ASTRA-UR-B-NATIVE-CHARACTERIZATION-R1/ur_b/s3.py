"""S3 SAV repeated-occasion / MR / rank / form shape."""
from __future__ import annotations

from pathlib import Path

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_empirical_objects import EmpiricalUniverse, ExactRef, RoutingEligibilityFact
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState, decode_sav
from rawlsing_next.pre553_source_backed_c11_facade import (
    CoordinateSlotRule, GovernedC11Projection, OccurrenceRule, PhysicalSlot,
    ResponseSlotRule, ResponseValueRule, RowRespondentBinding,
    physical_value_binding_key,
)
from rawlsing_next.pre553_source_backed_c11_facade import build_validated_source_backed_c11_release
from rawlsing_next.tests.test_pre553_empirical_query import _auth, _ref


def build(path, *, respondents_count=12, repeated=True) -> dict:
    path = Path(path)
    incidence = decode_sav(path)
    tag = f"ur-b-s3-{respondents_count}-{'rep' if repeated else 'flat'}"
    auths = (
        _auth(f"{tag}-source", "SOURCE_SEMANTICS_TOPOLOGY",
              families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0")),
        _auth(f"{tag}-mapping", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
              families=("RespondentEvent@1.0.0",)),
        _auth(f"{tag}-coord", "COORDINATE_SEMANTICS",
              families=("EmpiricalCoordinateFact@1.0.0",)),
        _auth(f"{tag}-routing", "ROUTING_RISK_SET",
              families=("RoutingEligibilityFact@1.0.0",)),
        _auth(f"{tag}-replay", "REPLAY_PROTOCOL",
              families=("ReplayReceipt@1.0.0",)),
        _auth(f"{tag}-projection", "SOURCE_SEMANTICS_TOPOLOGY",
              families=("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0")),
    )
    source_auth, mapping_auth, coord_auth, routing_auth, replay_auth, projection_auth = auths
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
    names = ("SCORE", "MR1", "MR2", "RANK1", "RANK2", "FORM")
    qrefs = {name: _ref("QUESTION_NATIVE", f"{tag}-{name}") for name in names}
    questions = tuple(QuestionVariableBinding(
        empirical_universe_ref=universe.ref, native_question_ref=qrefs[name],
        instrument_question_version="1",
        canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
        component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        semantic_authority_ref=source_auth.authority_ref,
        topology_authority_ref=source_auth.authority_ref) for name in names)
    qbind = dict(zip(names, questions))
    respondents = tuple(RespondentIdentity(
        empirical_universe_ref=universe.ref, respondent_key=f"P{i}",
        source_native_respondent_key_ref_or_typed_absence=_ref(
            "SOURCE_RESPONDENT", f"{tag}-P{i}"),
        identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"))
        for i in range(1, respondents_count + 1))
    by_id = {f"P{i}": respondents[i - 1] for i in range(1, respondents_count + 1)}
    risk = _ref("RISK_SET", f"{tag}-risk")
    routing = tuple(RoutingEligibilityFact(
        typed_state="ELIGIBLE_APPLICABLE",
        authority_snapshot_refs=(routing_auth.authority_ref,), dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", f"{tag}-routing-{rid}-{q}"),
        empirical_universe_ref=universe.ref, scoped_respondent_ref=respondent.ref,
        question_or_target_ref=qrefs[q], risk_set_ref=risk,
        routing_rule_ref=_ref("ROUTING_RULE", f"{tag}-{q}"),
        applicability_state="ELIGIBLE_APPLICABLE",
        routing_state="ELIGIBLE_APPLICABLE", parent_predicate_refs=(),
        member_set_replay_ref=_ref("MEMBER_SET", f"{tag}-{q}"))
        for q in names for rid, respondent in by_id.items())
    variables = {v.name: v for v in incidence.variables}
    cells = list(incidence.iter_cells())
    bycell = {(c.row_ordinal, c.variable_name): c for c in cells}

    def key(cell):
        return physical_value_binding_key(cell.raw_value, cell.missing_state,
                                          cell.source_missing_declaration)

    def response(name, values, occurrences, missing=True):
        rules = []
        for value in values:
            cell = next(c for c in cells if c.variable_name == name
                        and c.raw_value == value
                        and c.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE)
            rules.append(ResponseValueRule(key(cell), "SUBSTANTIVE_RESPONSE",
                                           occurrences, str(int(value)),
                                           mapping_auth.authority_ref))
        if missing:
            miss = next((c for c in cells if c.variable_name == name
                         and c.missing_state is PhysicalMissingState.SYSTEM_MISSING), None)
            if miss is not None:
                rules.append(ResponseValueRule(key(miss), "MISSING", occurrences))
        return ResponseSlotRule(PhysicalSlot(variables[name].ordinal, name),
                                qbind[name], tuple(rules))

    repeated_occ = (
        OccurrenceRule("0", _ref("TOPOLOGY", f"{tag}-repeated"),
                       {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
        OccurrenceRule("1", _ref("TOPOLOGY", f"{tag}-repeated"),
                       {"kind": "REPEATED_EVENT", "multiplicity_index": 1}),
    )
    mr1_occ = (OccurrenceRule("0", _ref("TOPOLOGY", f"{tag}-mr1"),
                              {"kind": "MULTISELECT", "index": 0}),)
    mr2_occ = (OccurrenceRule("0", _ref("TOPOLOGY", f"{tag}-mr2"),
                              {"kind": "MULTISELECT", "index": 1}),)
    rank1_occ = (OccurrenceRule("0", _ref("TOPOLOGY", f"{tag}-rank1"),
                                {"kind": "ORDERED_SEQUENCE", "semantic_ordinal": 0}),)
    rank2_occ = (OccurrenceRule("0", _ref("TOPOLOGY", f"{tag}-rank2"),
                                {"kind": "ORDERED_SEQUENCE", "semantic_ordinal": 1}),)
    scalar = (OccurrenceRule("0", _ref("TOPOLOGY", f"{tag}-scalar"),
                             {"kind": "SCALAR_SINGULAR", "index": 0}),)
    response_slots = (
        response("SCORE", (0.0, 1.0, 2.0), repeated_occ if repeated else scalar, missing=False),
        response("MR1", (0.0, 1.0), mr1_occ, missing=True),
        response("MR2", (0.0, 1.0), mr2_occ, missing=True),
        response("RANK1", (0.0, 1.0, 2.0), rank1_occ, missing=True),
        response("RANK2", (0.0, 1.0, 2.0), rank2_occ, missing=True),
        response("FORM", (0.0, 1.0), scalar, missing=False),
    )
    if repeated:
        bindings = tuple(RowRespondentBinding(row, respondents[(row - 1) % respondents_count].ref)
                         for row in range(1, 25))
    else:
        # Flattening variant: one respondent per physical row.
        respondents = tuple(RespondentIdentity(
            empirical_universe_ref=universe.ref, respondent_key=f"R{i}",
            source_native_respondent_key_ref_or_typed_absence=_ref(
                "SOURCE_RESPONDENT", f"{tag}-R{i}"),
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"))
            for i in range(1, 25))
        by_id = {f"R{i}": respondents[i - 1] for i in range(1, 25)}
        bindings = tuple(RowRespondentBinding(i, respondents[i - 1].ref)
                         for i in range(1, 25))
    projection = GovernedC11Projection(
        projection_identity_ref=_ref("C11_SEMANTIC_PROJECTION", tag),
        source_artifact_id=f"SOURCE-{tag}", expected_source_sha256=incidence.source_sha256,
        source_family_id="SURVEY", study_product_id=f"STUDY-{tag}",
        release_id=f"REL-{tag}", instrument_release_id=f"INST-{tag}",
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:test:{tag}:snapshot", incidence.source_sha256),
        universes=(universe,), respondents=respondents, row_bindings=bindings,
        questions=questions, response_slots=response_slots,
        coordinate_slots=(CoordinateSlotRule(
            PhysicalSlot(variables["OCCASION"].ordinal, "OCCASION"),
            _ref("COORDINATE_NATIVE", f"{tag}-OCCASION"),
            _ref("UNIT_TAXONOMY", f"{tag}-OCCASION"), "2026-01",
            coord_auth.authority_ref, copy_observed_raw=True),),
        routing=tuple(routing), weight_slots=(),
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
              "authorities": auths}
    return {"incidence": incidence, "projection": projection, "source": source,
            "authorities": auths, "risk": risk, "qrefs": qrefs,
            "repeated": repeated, "respondents_count": respondents_count}


def release(path, *, respondents_count=12, repeated=True):
    fx = build(path, respondents_count=respondents_count, repeated=repeated)
    return fx, build_validated_source_backed_c11_release(fx["incidence"], fx["projection"])
