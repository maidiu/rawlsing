from dataclasses import replace

import pandas as pd
import pytest

from rawlsing_next.pre553_c11_ingest import (
    INGEST_CONTRACT_VERSION, C11IngestValidationError, C11SourceReleaseCandidate,
    SourceReleaseManifest, build_candidate_replay_manifest, validate_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact, EmpiricalQuerySpec, EmpiricalUniverse, ExactRef,
    RespondentEvent, RoutingEligibilityFact, WeightMeasureFact, canonicalize,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_physical_decoder import (
    PhysicalCell, PhysicalMissingState, PhysicalSourceIncidence, PhysicalVariable,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    CONTRACT_ID, CoordinateSlotRule, ExactPhysicalCellStream, GovernedC11Projection,
    OccurrenceRule, PhysicalSlot, ResponseSlotRule, ResponseValueRule,
    RowRespondentBinding, SourceBackedC11FacadeError, SourceBackedC11SessionCache,
    WeightSlotRule, build_source_backed_c11_repository,
    build_validated_source_backed_c11_release,
    build_validated_source_backed_c11_release_from_stream,
    physical_value_binding_key, project_c11_candidate_from_physical_cells,
    raw_physical_value_witness,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _auth, _branch_predicate, _build_source, _cell_map, _h, _predicate, _query,
    _query_authority, _ref, _response_leaf,
)


def _fixture(tag="facade"):
    source_auth = _auth(f"source-{tag}", "SOURCE_SEMANTICS_TOPOLOGY",
                        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"))
    mapping_auth = _auth(f"mapping-{tag}", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
                         families=("RespondentEvent@1.0.0",))
    coord_auth = _auth(f"coord-{tag}", "COORDINATE_SEMANTICS",
                       families=("EmpiricalCoordinateFact@1.0.0",))
    routing_auth = _auth(f"routing-{tag}", "ROUTING_RISK_SET",
                         families=("RoutingEligibilityFact@1.0.0",))
    weight_auth = _auth(f"weight-{tag}", "WEIGHT_DESIGN_ESTIMAND",
                        families=("WeightMeasureFact@1.0.0",))
    replay_auth = _auth(f"replay-{tag}", "REPLAY_PROTOCOL",
                        families=("ReplayReceipt@1.0.0",))
    projection_auth = _auth(
        f"projection-{tag}", "SOURCE_SEMANTICS_TOPOLOGY",
        families=("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0", "WeightMeasureFact@1.0.0"),
    )
    authorities = (source_auth, mapping_auth, coord_auth, routing_auth, weight_auth, replay_auth, projection_auth)
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED", authority_snapshot_refs=(source_auth.authority_ref,), dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"universe-{tag}"), raw_source_identity=f"RAW-{tag}",
        source_family="SURVEY", study_product_release=f"STUDY-{tag}/REL-1", instrument_release=f"INST-{tag}",
        country_geography="US", sampling_geography="US-NATIONAL", raw_wave="W1", canonical_wave_if_governed=None,
        field_or_reference_time="2026-01", target_population_and_sample_frame="ADULTS", sampling_design_regime="DESIGN-C05R2A",
        respondent_namespace=f"NS-{tag}", source_artifact_import_lineage=f"SOURCE-LINEAGE-{tag}",
        harmonization_authority_ref=None, source_relation_refs=(),
    )
    names = ("X", "Y", "M", "O", "R")
    qrefs = {q: _ref("QUESTION_NATIVE", f"c05r2a-shared-{q}") for q in names}
    questions = tuple(QuestionVariableBinding(
        empirical_universe_ref=universe.ref, native_question_ref=qrefs[q], instrument_question_version="1",
        canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
        component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        semantic_authority_ref=source_auth.authority_ref, topology_authority_ref=source_auth.authority_ref,
    ) for q in names)
    qbind = {q: questions[i] for i, q in enumerate(names)}
    respondents = tuple(RespondentIdentity(
        empirical_universe_ref=universe.ref, respondent_key=f"R{i}",
        source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", f"{tag}-R{i}"),
        identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
    ) for i in range(1, 4))
    by_id = {f"R{i}": respondents[i-1] for i in range(1, 4)}
    risk = _ref("RISK_SET", "c05r2a-shared-R")
    routing = []
    for q in names:
        members = {"R1", "R2"} if q == "Y" else {"R1", "R2", "R3"}
        for rid, respondent in by_id.items():
            state = "ELIGIBLE_APPLICABLE" if rid in members else "NOT_ELIGIBLE"
            routing.append(RoutingEligibilityFact(
                typed_state=state, authority_snapshot_refs=(routing_auth.authority_ref,), dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"routing-{tag}-{rid}-{q}"),
                empirical_universe_ref=universe.ref, scoped_respondent_ref=respondent.ref, question_or_target_ref=qrefs[q],
                risk_set_ref=risk, routing_rule_ref=_ref("ROUTING_RULE", f"{tag}-{q}"),
                applicability_state=state, routing_state=state, parent_predicate_refs=(),
                member_set_replay_ref=_ref("MEMBER_SET", f"{tag}-{q}-{'-'.join(sorted(members))}"),
            ))
    rows = [
        ["1", "1", "AB", "AB", "XY", "A", 2],
        ["0", "0", "A", "BA", "XZ", "B", 1],
        [None, "1", "", "AB", "XY", "A", 3],
    ]
    var_names = ("X", "Y", "M", "O", "R", "G", "W")
    variables = tuple(PhysicalVariable(i, name, None, f"label-{name}", {}, (), {}, {})
                      for i, name in enumerate(var_names, 1))
    source_sha = _h(f"c05r2a-source:{tag}")
    incidence = PhysicalSourceIncidence(
        source_sha256=source_sha, source_format="SYNTHETIC", row_count=3, variables=variables,
        reader_configuration={"fixture":"c05r2a"}, file_metadata={"fixture":"c05r2a"},
        _frame=pd.DataFrame(rows, columns=var_names),
    )
    cells = tuple(incidence.iter_cells())
    pkey = lambda raw, state=PhysicalMissingState.OBSERVED_STORAGE_VALUE: physical_value_binding_key(raw, state)
    scalar = lambda q: OccurrenceRule("0", _ref("TOPOLOGY", f"c05r2a-{q}-SCALAR"), {"kind":"SCALAR_SINGULAR","index":0})
    response_slots = (
    ResponseSlotRule(PhysicalSlot(1,"X"), qbind["X"], (
            ResponseValueRule(pkey("1"), "SUBSTANTIVE_RESPONSE", (scalar("X"),), "1", mapping_auth.authority_ref),
            ResponseValueRule(pkey("0"), "SUBSTANTIVE_RESPONSE", (scalar("X"),), "0", mapping_auth.authority_ref),
            ResponseValueRule(pkey(None, PhysicalMissingState.SYSTEM_MISSING), "MISSING", (scalar("X"),)),
        )),
        ResponseSlotRule(PhysicalSlot(2,"Y"), qbind["Y"], (
            ResponseValueRule(pkey("1"), "SUBSTANTIVE_RESPONSE", (scalar("Y"),), "1", mapping_auth.authority_ref),
            ResponseValueRule(pkey("0"), "SUBSTANTIVE_RESPONSE", (scalar("Y"),), "0", mapping_auth.authority_ref),
        )),
        ResponseSlotRule(PhysicalSlot(3,"M"), qbind["M"], (
            ResponseValueRule(pkey("AB"), "SUBSTANTIVE_RESPONSE", (
                OccurrenceRule("0", _ref("TOPOLOGY","c05r2a-M-MULTI"), {"kind":"MULTISELECT","index":0}),
                OccurrenceRule("1", _ref("TOPOLOGY","c05r2a-M-MULTI"), {"kind":"MULTISELECT","index":1}),
            ), "AB", mapping_auth.authority_ref),
            ResponseValueRule(pkey("A"), "SUBSTANTIVE_RESPONSE", (
                OccurrenceRule("0", _ref("TOPOLOGY","c05r2a-M-MULTI"), {"kind":"MULTISELECT","index":0}),
            ), "A", mapping_auth.authority_ref),
            ResponseValueRule(pkey(""), "SUBSTANTIVE_RESPONSE", (), "", mapping_auth.authority_ref),
        )),
        ResponseSlotRule(PhysicalSlot(4,"O"), qbind["O"], tuple(
            ResponseValueRule(pkey(value), "SUBSTANTIVE_RESPONSE", (
                OccurrenceRule("0", _ref("TOPOLOGY","c05r2a-O-ORDERED"), {"kind":"ORDERED_SEQUENCE","semantic_ordinal":0}),
                OccurrenceRule("1", _ref("TOPOLOGY","c05r2a-O-ORDERED"), {"kind":"ORDERED_SEQUENCE","semantic_ordinal":1}),
            ), value, mapping_auth.authority_ref) for value in ("AB","BA")
        )),
        ResponseSlotRule(PhysicalSlot(5,"R"), qbind["R"], tuple(
            ResponseValueRule(pkey(value), "SUBSTANTIVE_RESPONSE", (
                OccurrenceRule("0", _ref("TOPOLOGY","c05r2a-R-REPEATED"), {"kind":"REPEATED_EVENT","multiplicity_index":0}),
                OccurrenceRule("1", _ref("TOPOLOGY","c05r2a-R-REPEATED"), {"kind":"REPEATED_EVENT","multiplicity_index":1}),
            ), value, mapping_auth.authority_ref) for value in ("XY","XZ")
        )),
    )
    projection = GovernedC11Projection(
        projection_identity_ref=_ref("C11_SEMANTIC_PROJECTION", f"c05r2a-{tag}"),
        source_artifact_id=f"SOURCE-{tag}", expected_source_sha256=source_sha, source_family_id="SURVEY",
        study_product_id=f"STUDY-{tag}", release_id=f"REL-{tag}", instrument_release_id=f"INST-{tag}",
        source_snapshot_retention_ref=ExactRef("SOURCE_SNAPSHOT", f"urn:test:c05r2a:snapshot:{tag}", source_sha),
        universes=(universe,), respondents=respondents,
        row_bindings=tuple(RowRespondentBinding(i, respondents[i-1].ref) for i in range(1,4)),
        questions=questions, response_slots=response_slots,
        coordinate_slots=(CoordinateSlotRule(PhysicalSlot(6,"G"), _ref("COORDINATE_NATIVE","c05r2a-shared-G"),
            _ref("UNIT_TAXONOMY","c05r2a-shared-G"), "2026-01", coord_auth.authority_ref, copy_observed_raw=True),),
        routing=tuple(routing),
        weight_slots=(WeightSlotRule(PhysicalSlot(7,"W"), "W", _ref("WEIGHT_SOURCE",f"{tag}-W"),
            weight_auth.authority_ref, weight_auth.authority_ref, _ref("SCOPE",f"{tag}-W"), copy_observed_numeric=True),),
        authority_snapshots=authorities, source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"), comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"), structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(a.authority_ref for a in authorities),
        projection_authority_ref=projection_auth.authority_ref, replay_authority_ref=replay_auth.authority_ref,
        tie_order_ref=_ref("ORDER_RULE","CANONICAL-REF-SORT"), replay_protocol_version="1.0.0",
    )
    return {"incidence":incidence,"cells":cells,"projection":projection,"source_sha":source_sha,"universe":universe,
            "respondents":by_id,"qrefs":qrefs,"crefs":{"G":_ref("COORDINATE_NATIVE","c05r2a-shared-G")},"risk_refs":{"R":risk},
            "source_auth":source_auth,"coord_auth":coord_auth,"routing_auth":routing_auth,"weight_auth":weight_auth,
            "replay_auth":replay_auth,"projection_auth":projection_auth,"authorities":authorities}


def _logical_oracle_release(fx):
    p=fx["projection"]; cells=fx["cells"]; by_cell={(c.row_ordinal,c.variable_ordinal,c.variable_name):c for c in cells}
    respondents={x.row_ordinal: next(r for r in p.respondents if r.ref==x.respondent_ref) for x in p.row_bindings}
    def dref(kind,ns,material):
        h=semantic_hash(material); return ExactRef(kind,f"urn:rawlsing:pre553:c05r2a:{ns}:sha256:{h}",h)
    def auths(xs): return tuple(sorted(set(xs),key=lambda r:r.key))
    def refs(xs): return tuple(sorted(set(xs),key=lambda r:r.key))
    events=[]
    for slot in p.response_slots:
        values={v.physical_key:v for v in slot.values}; q=slot.question_binding
        for row in range(1,4):
            cell=by_cell[(row,slot.slot.ordinal,slot.slot.name)]; value=values[physical_value_binding_key(cell.raw_value,cell.missing_state,cell.source_missing_declaration)]
            respondent=respondents[row]
            for occ in value.occurrences:
                material={"contract":CONTRACT_ID,"projection":p.projection_identity_ref.as_dict(),"source_sha":p.expected_source_sha256,
                          "row":row,"respondent":respondent.ref.as_dict(),"question":q.ref.as_dict(),"slot":slot.slot.key,
                          "physical_value_key":value.physical_key,"occurrence":occ.key}
                group=semantic_hash({**material,"role":"GROUP"}); eid=semantic_hash({**material,"role":"EVENT"})
                a=[p.projection_authority_ref,q.semantic_authority_ref,q.topology_authority_ref,*value.extra_authority_refs]
                if value.transform_authority_ref is not None:a.append(value.transform_authority_ref)
                events.append(RespondentEvent(
                    typed_state=value.response_state,authority_snapshot_refs=auths(a),dependency_refs=refs((respondent.ref,q.ref)),
                    producer_replay_locator_or_reference_root=dref("PRE553_C05R2A_EVENT_REPLAY_ROOT","event",material),
                    empirical_universe_ref=respondent.empirical_universe_ref,scoped_respondent_ref=respondent.ref,native_question_ref=q.native_question_ref,
                    canonical_question_ref_if_authorized=None,component_or_subitem_ref=occ.component_ref,
                    event_group_id=f"urn:rawlsing:pre553:c05r2a:event-group:sha256:{group}",
                    response_event_id_or_deterministic_index=f"urn:rawlsing:pre553:c05r2a:event:sha256:{eid}",raw_response_value=raw_physical_value_witness(cell.raw_value),
                    canonical_response_value_if_authorized=canonicalize(value.canonical_value),value_transform_authority_ref=value.transform_authority_ref,
                    response_topology_ref=occ.topology_ref,multiplicity_order_rank_fields=canonicalize(occ.multiplicity_order_rank_fields),response_state=value.response_state))
    coords=[]
    slot=p.coordinate_slots[0]
    for row in range(1,4):
        cell=by_cell[(row,slot.slot.ordinal,slot.slot.name)]; respondent=respondents[row]
        material={"contract":CONTRACT_ID,"projection":p.projection_identity_ref.as_dict(),"source_sha":p.expected_source_sha256,"row":row,
                  "respondent":respondent.ref.as_dict(),"slot":slot.slot.key,
                  "physical_value_key":physical_value_binding_key(cell.raw_value,cell.missing_state,cell.source_missing_declaration)}
        coords.append(EmpiricalCoordinateFact(
            typed_state="OBSERVED_COORDINATE",authority_snapshot_refs=auths((p.projection_authority_ref,slot.source_semantic_authority_ref)),dependency_refs=(respondent.ref,),
            producer_replay_locator_or_reference_root=dref("PRE553_C05R2A_COORDINATE_REPLAY_ROOT","coordinate",material),
            empirical_universe_ref=respondent.empirical_universe_ref,scoped_respondent_ref=respondent.ref,native_coordinate_ref=slot.native_coordinate_ref,
            canonical_coordinate_ref_if_authorized=None,raw_coordinate_value=raw_physical_value_witness(cell.raw_value),canonical_coordinate_value_if_authorized=None,
            unit_category_taxonomy_ref=slot.unit_taxonomy_ref,effective_or_reference_time=slot.effective_time,coordinate_state="OBSERVED_COORDINATE",
            normalization_crosswalk_authority_ref=None,source_semantic_authority_ref=slot.source_semantic_authority_ref))
    weights=[]; slot=p.weight_slots[0]
    for row in range(1,4):
        cell=by_cell[(row,slot.slot.ordinal,slot.slot.name)]; respondent=respondents[row]
        material={"contract":CONTRACT_ID,"projection":p.projection_identity_ref.as_dict(),"source_sha":p.expected_source_sha256,"row":row,
                  "respondent":respondent.ref.as_dict(),"slot":slot.slot.key,
                  "physical_value_key":physical_value_binding_key(cell.raw_value,cell.missing_state,cell.source_missing_declaration),"basis":slot.weight_basis_id}
        weights.append(WeightMeasureFact(
            typed_state="WEIGHT_VALID_AUTHORIZED",authority_snapshot_refs=auths((p.projection_authority_ref,slot.design_authority_ref,slot.estimand_authority_ref)),
            dependency_refs=(respondent.ref,),producer_replay_locator_or_reference_root=dref("PRE553_C05R2A_WEIGHT_REPLAY_ROOT","weight",material),
            empirical_universe_ref=respondent.empirical_universe_ref,scoped_respondent_ref=respondent.ref,weight_basis_id="W",
            exact_weight_value_representation=str(cell.raw_value),weight_state="WEIGHT_VALID_AUTHORIZED",weight_source_ref=slot.weight_source_ref,
            design_authority_ref=slot.design_authority_ref,estimand_authority_ref=slot.estimand_authority_ref,
            normalization_or_recalibration_rule_ref=None,effective_scope_ref=slot.effective_scope_ref))
    events=tuple(sorted(events,key=lambda x:x.ref.key));coords=tuple(sorted(coords,key=lambda x:x.ref.key));weights=tuple(sorted(weights,key=lambda x:x.ref.key))
    counts={"EmpiricalUniverse":1,"RespondentIdentity":3,"QuestionVariableBinding":5,"RespondentEvent":len(events),
            "RoutingEligibilityFact":len(p.routing),"EmpiricalCoordinateFact":3,"WeightMeasureFact":3,"AuthoritySnapshot":len(p.authority_snapshots),
            "SourceUniverseRelation":0,"EmpiricalPredicateReplayBinding":0,"ComparatorReplayBinding":0,"DiscoveryBranchReplayBinding":0,
            "StructuralAdmissionReplayBinding":0,"ReplayManifest":1}
    manifest=SourceReleaseManifest(source_artifact_id=p.source_artifact_id,source_artifact_content_hash=p.expected_source_sha256,source_family_id=p.source_family_id,
        study_product_id=p.study_product_id,release_id=p.release_id,instrument_release_id=p.instrument_release_id,ingest_contract_version=INGEST_CONTRACT_VERSION,
        declared_universe_refs=(p.universes[0].ref,),declared_authority_snapshot_refs=tuple(sorted((a.authority_ref for a in p.authority_snapshots),key=lambda r:r.key)),
        declared_record_counts_by_logical_family=counts,source_snapshot_retention_ref=p.source_snapshot_retention_ref)
    c=C11SourceReleaseCandidate(manifest,tuple(p.universes),tuple(p.respondents),tuple(p.questions),events,tuple(sorted(p.routing,key=lambda x:x.ref.key)),coords,weights,
        tuple(sorted(p.authority_snapshots,key=lambda x:x.authority_ref.key)),p.source_relations,p.predicate_replay,p.comparator_replay,p.discovery_replay,p.structural_replay,None)
    replay=build_candidate_replay_manifest(c,replay_protocol_authority_ref=p.replay_authority_ref,deterministic_tie_order_rules_ref=p.tie_order_ref,replay_protocol_version=p.replay_protocol_version)
    return validate_c11_source_release(replace(c,candidate_replay_manifest=replay))


def _source_dict(fx, repo, release):
    return {**fx,"repo":repo,"release_ref":release.release_ref}


def test_facade_matches_independent_logical_c11_and_frozen_i03_oracle_exactly():
    fx=_fixture(); oracle=_logical_oracle_release(fx)
    facade=build_validated_source_backed_c11_release(fx["incidence"],fx["projection"])
    assert facade.release_ref==oracle.release_ref
    assert facade.replay_manifest.ref==oracle.replay_manifest.ref
    assert tuple(x.ref for x in facade.public_objects)==tuple(x.ref for x in oracle.public_objects)
    assert tuple(x.ref for x in facade.internal_records)==tuple(x.ref for x in oracle.internal_records)
    qa=_query_authority("c05r2a-parity")
    oracle_source=_source_dict(fx,C11Repository((oracle,)),oracle); facade_source=_source_dict(fx,C11Repository((facade,)),facade)
    pred=_branch_predicate(oracle_source,qa,tag="all"); query=_query(oracle_source,qa,pred,("Y",),tag="parity")
    registry=AuthorityRegistry((*fx["authorities"],qa))
    left=execute_empirical_query(repository=oracle_source["repo"],query=query,predicate=pred,authority_registry=registry,release_refs=(oracle.release_ref,))
    right=execute_empirical_query(repository=facade_source["repo"],query=query,predicate=pred,authority_registry=registry,release_refs=(facade.release_ref,))
    assert right==left
    assert tuple(f.ref for f in right.facts)==tuple(f.ref for f in left.facts)


def test_native_and_replay_equivalent_transport_are_semantically_identical_and_deterministic():
    fx=_fixture("transport"); native=build_validated_source_backed_c11_release(fx["incidence"],fx["projection"])
    stream=ExactPhysicalCellStream(fx["source_sha"],3,lambda:iter(tuple(reversed(fx["cells"]))),"V4_LIKE_REORDERED_EXACT_STREAM")
    replay=build_validated_source_backed_c11_release_from_stream(stream,fx["projection"])
    replay2=build_validated_source_backed_c11_release_from_stream(ExactPhysicalCellStream(fx["source_sha"],3,lambda:iter(fx["cells"])),fx["projection"])
    assert native.release_ref==replay.release_ref==replay2.release_ref
    assert native.replay_manifest.ref==replay.replay_manifest.ref==replay2.replay_manifest.ref


def test_source_sha_projection_authority_and_replay_manifest_fail_closed():
    fx=_fixture("failclosed"); p=fx["projection"]
    with pytest.raises(SourceBackedC11FacadeError):
        build_validated_source_backed_c11_release(fx["incidence"],None)
    bad_sha=_h("wrong-source")
    badp=replace(p,expected_source_sha256=bad_sha,source_snapshot_retention_ref=ExactRef("SOURCE_SNAPSHOT","urn:test:bad",bad_sha))
    with pytest.raises(SourceBackedC11FacadeError): build_validated_source_backed_c11_release(fx["incidence"],badp)
    with pytest.raises(SourceBackedC11FacadeError):
        replace(p,authority_snapshots=tuple(a for a in p.authority_snapshots if a!=fx["projection_auth"]))
    candidate=project_c11_candidate_from_physical_cells(source_sha256=fx["source_sha"],row_count=3,cells=fx["cells"],projection=p)
    with pytest.raises(C11IngestValidationError): validate_c11_source_release(replace(candidate,candidate_replay_manifest=None))
    bad_replay=replace(candidate.candidate_replay_manifest,semantic_projection_hash=_h("tampered-replay"))
    with pytest.raises(C11IngestValidationError): validate_c11_source_release(replace(candidate,candidate_replay_manifest=bad_replay))


def test_physical_missing_requires_explicit_semantic_binding_and_one_cell_can_emit_zero_one_many():
    fx=_fixture("occurrence"); p=fx["projection"]
    x=p.response_slots[0]; x_without_missing=replace(x,values=tuple(v for v in x.values if v.response_state!="MISSING"))
    with pytest.raises(SourceBackedC11FacadeError):
        project_c11_candidate_from_physical_cells(source_sha256=fx["source_sha"],row_count=3,cells=fx["cells"],projection=replace(p,response_slots=(x_without_missing,*p.response_slots[1:])))
    release=build_validated_source_backed_c11_release(fx["incidence"],p)
    events=[e for e in release.public_objects if isinstance(e,RespondentEvent) and e.native_question_ref==fx["qrefs"]["M"].as_dict()]
    counts={rid:sum(e.scoped_respondent_ref==fx["respondents"][rid].ref.as_dict() for e in events) for rid in ("R1","R2","R3")}
    assert counts=={"R1":2,"R2":1,"R3":0}
    assert len({e.response_event_id_or_deterministic_index for e in events})==3


def test_ordered_and_repeated_topology_fields_survive_projection_and_validation():
    fx=_fixture("topology"); release=build_validated_source_backed_c11_release(fx["incidence"],fx["projection"])
    ordered=[e for e in release.public_objects if isinstance(e,RespondentEvent) and e.native_question_ref==fx["qrefs"]["O"].as_dict()]
    repeated=[e for e in release.public_objects if isinstance(e,RespondentEvent) and e.native_question_ref==fx["qrefs"]["R"].as_dict()]
    assert {e.multiplicity_order_rank_fields["kind"] for e in ordered}=={"ORDERED_SEQUENCE"}
    assert {e.multiplicity_order_rank_fields["semantic_ordinal"] for e in ordered}=={0,1}
    assert {e.multiplicity_order_rank_fields["kind"] for e in repeated}=={"REPEATED_EVENT"}
    assert {e.multiplicity_order_rank_fields["multiplicity_index"] for e in repeated}=={0,1}


def test_governed_not_uses_exact_risk_set_not_physical_row_complement():
    fx=_fixture("not"); release=build_validated_source_backed_c11_release(fx["incidence"],fx["projection"]); source=_source_dict(fx,C11Repository((release,)),release)
    qa=_query_authority("c05r2a-not")
    leaf=_response_leaf(source,qa,"X",1); pred=_predicate(source,qa,{"op":"NOT","children":[leaf]},tag="not-x1")
    query=_query(source,qa,pred,("Y",),tag="not-risk")
    result=execute_empirical_query(repository=source["repo"],query=query,predicate=pred,authority_registry=AuthorityRegistry((*fx["authorities"],qa)),release_refs=(release.release_ref,))
    assert result.facts[0].raw_denominator_support==1
    assert _cell_map(result.facts[0])["0"]["raw_numerator_support"]==1


def test_raw_and_weighted_estimands_remain_distinct_and_weight_authority_never_falls_back():
    fx=_fixture("weight"); release=build_validated_source_backed_c11_release(fx["incidence"],fx["projection"]); source=_source_dict(fx,C11Repository((release,)),release)
    qa=_query_authority("c05r2a-weight"); pred=_branch_predicate(source,qa)
    raw=_query(source,qa,pred,("Y",),measure="RAW",tag="raw"); weighted=_query(source,qa,pred,("Y",),measure="GOVERNED_WEIGHTED",tag="weighted")
    full=AuthorityRegistry((*fx["authorities"],qa))
    raw_fact=execute_empirical_query(repository=source["repo"],query=raw,predicate=pred,authority_registry=full,release_refs=(release.release_ref,)).facts[0]
    weighted_fact=execute_empirical_query(repository=source["repo"],query=weighted,predicate=pred,authority_registry=full,release_refs=(release.release_ref,)).facts[0]
    assert raw_fact.ref!=weighted_fact.ref
    assert raw_fact.raw_denominator_support==2
    assert weighted_fact.weighted_denominator_support_if_authorized is not None
    missing_weight_registry=AuthorityRegistry((*tuple(a for a in fx["authorities"] if a!=fx["weight_auth"]),qa))
    failed=execute_empirical_query(repository=source["repo"],query=weighted,predicate=pred,authority_registry=missing_weight_registry,release_refs=(release.release_ref,)).facts[0]
    assert failed.typed_state=="UNAVAILABLE"
    assert failed.weighted_denominator_support_if_authorized is None


def test_unauthorized_cross_universe_composition_fails_closed():
    fx=_fixture("composition-a"); release=build_validated_source_backed_c11_release(fx["incidence"],fx["projection"])
    other=_build_source("composition-b",[{"id":"S1","responses":{"Y":1}}],question_namespace="c05r2a-shared",risk_namespace="c05r2a-shared")
    other_release=other["repo"].resolve_release_exact(other["release_ref"]); repo=C11Repository((release,other_release)); source=_source_dict(fx,repo,release)
    qa=_query_authority("c05r2a-composite"); pred=_branch_predicate(source,qa)
    query=_query(source,qa,pred,("Y",),source_mode="AUTHORIZED_COMPOSITE",universe_refs=(fx["universe"].ref,other["universe"].ref),tag="composite",
                 target_authority_refs=(fx["source_auth"].authority_ref,other["source_auth"].authority_ref))
    registry=AuthorityRegistry((*fx["authorities"],*other["authorities"],qa))
    result=execute_empirical_query(repository=repo,query=query,predicate=pred,authority_registry=registry,release_refs=(release.release_ref,other_release.release_ref))
    assert len(result.facts)==1
    assert result.facts[0].typed_state in {"NONCOMPARABLE","UNAVAILABLE"}


def test_optional_session_cache_delete_changes_cost_only_and_mismatch_recomputes_or_fails_closed():
    fx=_fixture("cache"); stream=ExactPhysicalCellStream(fx["source_sha"],3,lambda:iter(fx["cells"])); cache=SourceBackedC11SessionCache()
    _,first=build_source_backed_c11_repository(stream,fx["projection"],cache=cache); assert cache.entry_count==1
    _,cached=build_source_backed_c11_repository(stream,fx["projection"],cache=cache); assert cached.release_ref==first.release_ref
    cache.clear(); _,rebuilt=build_source_backed_c11_repository(stream,fx["projection"],cache=cache); assert rebuilt.release_ref==first.release_ref
    key=next(iter(cache._entries)); wrong=replace(key,projection_identity=_h("wrong-cache-key")); cache._entries[key]=(wrong,rebuilt)
    with pytest.raises(SourceBackedC11FacadeError): cache.get(key)


def test_transport_labels_and_physical_order_have_zero_semantic_authority():
    fx=_fixture("labels"); p=fx["projection"]
    bad=list(fx["cells"]); target=next(i for i,c in enumerate(bad) if c.row_ordinal==1 and c.variable_name=="X")
    bad[target]=replace(bad[target],raw_value="99",raw_value_label="Don't know")
    with pytest.raises(SourceBackedC11FacadeError):
        project_c11_candidate_from_physical_cells(source_sha256=fx["source_sha"],row_count=3,cells=reversed(bad),projection=p)
