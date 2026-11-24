"""Native, sourcefree scientific counter-court. No synthetic empirical facts."""
from itertools import product
from fractions import Fraction
import pytest
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref, semantic_hash
from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.tests import test_pre553_discovery_exact as i05
from rawlsing_next.tests import c1_at08_at13_fixture as fx


def _c1(tag, *, narrow=False, weighted=False):
    rows=[{"id":f"R{x}{z}","responses":{"X":x,"Z":z,"Y":z}}
          for x,z in product((0,1),repeat=2)]
    weights={r["id"]:("WEIGHT_VALID_AUTHORIZED","3" if r["responses"]["Z"] else "1") for r in rows}
    source=native._build_source(tag,rows,weights=weights if weighted else None)
    qa=native._query_authority(tag)
    x=native._response_leaf(source,qa,"X",0)
    ast={"op":"AND","children":[x,native._response_leaf(source,qa,"Z",0)]} if narrow else x
    pred=native._predicate(source,qa,ast,tag=tag)
    q=native._query(source,qa,pred,("Y",),measure="GOVERNED_WEIGHTED" if weighted else "RAW",tag=tag)
    universe,release=source["universe"].ref,source["release_ref"]
    coord,pairing=source["qrefs"]["X"],fx.make_pairing_authority(tag)
    b=fx.make_conditioner_binding(binding_id="X",subject_fact_ref=ExactRef(**fx.subject_fact_ref(source,"X",0)),
        empirical_coordinate_ref=coord,comparability_authority_ref=pairing,
        source_universe_ref=universe,release_ref=release)
    consumer=fx.make_multi_conditioner_consumer_query(query_id=tag,
        subject_ref=ExactRef("TEST_ONLY_SUBJECT","urn:test:"+tag,semantic_hash(tag)),
        target_ref=source["qrefs"]["Y"],source_universe_ref=universe,release_ref=release,
        bindings=[b],projection_kind="TEST_ONLY_EXACT_CONDITIONAL")
    witness=fx.build_witness_for_binding(witness_object_id="urn:test:"+tag+":witness",
        consumer_query=consumer,producer_query=q,producer_predicate=pred,bindings=[b],
        coordinate_value_pairs=[(coord,0)],pairing_authority=pairing,source_universe_ref=universe,release_ref=release)
    result=compose_positioned_subject_possibility(repository=source["repo"],empirical_query=q,predicate=pred,
        authority_registry=native._registry(source,qa),release_refs=(release,),consumer_query=consumer,
        model_rule=fx.make_model_rule(universe,tag),condition_binding_witness=witness)
    return source,pred,q,result


def test_c1_weighted_geometry_carries_both_exact_measures():
    source,pred,q,result=_c1("R3-weighted",weighted=True)
    assert result.raw_denominator_support==2
    geometry=result.consumer_result_or_null.exact_geometry
    cells={c["cell"]:c for c in geometry["cells"]}
    assert cells["0"]["raw_probability_exact_fraction"]=={"$exact_fraction":[1,2]}
    assert cells["1"]["raw_probability_exact_fraction"]=={"$exact_fraction":[1,2]}
    assert cells["0"]["weighted_probability_exact_fraction_if_authorized"]=={"$exact_fraction":[1,4]}
    assert cells["1"]["weighted_probability_exact_fraction_if_authorized"]=={"$exact_fraction":[3,4]}
    assert geometry["denominator"]["weighted_denominator_support_if_authorized"]=={"$exact_fraction":[4,1]}


def test_c1_narrower_stratum_not_full_subject_condition():
    _,_,_,broad=_c1("R3-broad")
    source,pred,q,narrow=_c1("R3-narrow",narrow=True)
    assert broad.raw_denominator_support==2 and narrow.raw_denominator_support==1
    g=narrow.consumer_result_or_null.exact_geometry
    assert {c["cell"]:c["raw_numerator_support"] for c in g["cells"]}=={"0":1,"1":0}
    scope=g["condition_scope"]
    assert scope["state"]=="ADDITIONAL_OR_UNPROVED_RESTRICTIONS"
    assert scope["producer_predicate_ref"]==pred.ref.as_dict()
    assert scope["producer_predicate_ast"]==pred.predicate_ast
    assert scope["full_subject_condition_equivalence_established"] is False
    assert narrow.consumer_result_or_null.exact_reason=="EXACT_PRODUCER_STRATUM_SUPPORTED__SUBJECT_CONDITION_COVERAGE_NOT_ESTABLISHED"
    assert broad.consumer_result_or_null.exact_reason=="EXACT_POSITIONED_STRATUM_SUPPORTED"


def _weighted_joint(tag, dependent=False, missing=False):
    rows=[{"id":f"R{x}{y}{z}","responses":{"X":x,"Y":y,"Z":z}}
          for x,y,z in product((0,1),repeat=3)]
    weights={r["id"]:("WEIGHT_VALID_AUTHORIZED",str((1+r["responses"]["X"])*(1+2*r["responses"]["Y"])*(1+r["responses"]["Z"]))) for r in rows}
    if dependent:
        weights["R111"]=("WEIGHT_VALID_AUTHORIZED","19")
    rows.extend([{"id":"E0","responses":{"X":0,"Y":0,"Z":0}},{"id":"E1","responses":{"X":0,"Y":0,"Z":0}}])
    weights.update({"E0":("WEIGHT_VALID_AUTHORIZED","23"),"E1":("WEIGHT_VALID_AUTHORIZED","29")})
    common={r["id"] for r in rows[:8]}
    if missing:
        del rows[0]["responses"]["Z"]
    source=native._build_source(tag,rows,weights=weights,risk_sets={"R":{"X":{r["id"] for r in rows},"Y":common,"Z":common}})
    qa,da=native._query_authority(tag),i05._d_auth(tag+"-discovery")
    pred=native._branch_predicate(source,qa,tag="all")
    names=("Z","X","Y")
    q=native._query(source,qa,pred,names,measure="GOVERNED_WEIGHTED",tag="J")
    margins=[native._query(source,qa,pred,(name,),measure="GOVERNED_WEIGHTED",tag=name) for name in names]
    grammar=i05._grammar(operation="I03-OP-"+tag+"-discovery",
        atoms=[i05._atom("ALL",pred,"BRANCH")],templates=[i05._qt("J",q),*[i05._qt(n,m) for n,m in zip(names,margins)]],
        rules=[i05._rule("joint","BOUNDED_K_WAY_RESPONSE_CONFIGURATION","JOINT_DEPENDENCE",baseline_atom_id="ALL",
            joint_template_id="J",marginal_template_ids=names,validation={"kind":"JOINT_NOT_PRODUCT_OF_MARGINALS"})],j=3)
    return i05._execute(source,qa,da,grammar,(pred,),(q,*margins))


@pytest.mark.parametrize("dependent",[False,True])
def test_weighted_three_axis_native_factorization_with_unequal_risk(dependent):
    result=_weighted_joint("R3-weighted-"+str(dependent),dependent)
    receipt=result.receipts[0]
    facts={f.ref:f for f in result.empirical_facts}
    refs=receipt.support_uncertainty_state["query_role_fact_refs"]
    joint=facts[exact_ref(refs["JOINT"][0])]
    mx=facts[exact_ref(refs["MARGINAL_1"][0])]
    assert joint.typed_state==mx.typed_state=="SUPPORTED"
    assert joint.raw_denominator_support==8 and mx.raw_denominator_support==10
    assert joint.weighted_denominator_support_if_authorized=={"$exact_fraction":[43 if dependent else 36,1]}
    assert receipt.typed_state==("DISCOVERED_RESULT_SUPPORTED" if dependent else "VALID_EMPTY")
    assert receipt.support_uncertainty_state["joint_dependence_comparison"][0]["basis"]=="JOINT_COMPLETE_CASE_MARGINAL_PROJECTIONS"


def test_partially_resolved_native_joint_not_promoted():
    result=_weighted_joint("R3-partial",missing=True)
    receipt=result.receipts[0]
    assert receipt.typed_state=="COVERAGE_LIMITED"
    assert receipt.coverage_state=="EVALUATED_UNRESOLVED"
    assert any(f.typed_state=="UNRESOLVED" for f in result.empirical_facts)


def _reversal(tag, *, omitted=False, overlap=False):
    rows=[]
    for g,x,y,n in [("A",1,1,3),("A",0,1,8),("A",0,0,2),("B",1,1,2),("B",1,0,8),("B",0,0,2)]:
        for i in range(n): rows.append({"id":f"{g}{x}{y}-{i}","responses":{"X":x,"Y":y},"coords":{"G":g}})
    if omitted:
        rows.extend([{"id":"C1","responses":{"X":1,"Y":0},"coords":{"G":"C"}},
                     {"id":"C0","responses":{"X":0,"Y":1},"coords":{"G":"C"}}])
    source=native._build_source(tag,rows)
    qa,da=native._query_authority(tag),i05._d_auth(tag+"-discovery")
    allp=native._branch_predicate(source,qa,tag="all")
    xp,xn=(native._predicate(source,qa,native._response_leaf(source,qa,"X",x),tag="x"+str(x)) for x in (1,0))
    ga=native._predicate(source,qa,native._coordinate_leaf(source,"G","A"),tag="A")
    gb=native._predicate(source,qa,native._coordinate_leaf(source,"G","A" if overlap else "B"),tag="B")
    q=native._query(source,qa,allp,("Y",),tag="Y")
    grammar=i05._grammar(operation="I03-OP-"+tag+"-discovery",
        atoms=[i05._atom(k,p,kind) for k,p,kind in (("ALL",allp,"BRANCH"),("P",xp,"RESPONSE"),("N",xn,"RESPONSE"),("A",ga,"COORDINATE"),("B",gb,"COORDINATE"))],
        templates=[i05._qt("Y",q)],rules=[i05._rule("reversal","CONDITIONAL_REVERSAL_OR_SIMPSON","REVERSAL_GRID",
            baseline_atom_id="ALL",exposure_positive_atom_id="P",exposure_negative_atom_id="N",
            stratum_atom_ids=("A","B"),query_template_id="Y",validation={"kind":"CONDITIONAL_REVERSAL","target_cell":"1"})],k=2)
    return i05._execute(source,qa,da,grammar,(allp,xp,xn,ga,gb),(q,))


@pytest.mark.parametrize("omitted,overlap",[(False,False),(True,False),(False,True)])
def test_reversal_retains_exact_partition_qualification(omitted,overlap):
    result=_reversal(f"R3-reversal-{omitted}-{overlap}",omitted=omitted,overlap=overlap)
    r=result.receipts[0]
    assert r.typed_state=="DISCOVERED_RESULT_SUPPORTED" # selected-grid sign reversal remains real
    q=r.support_uncertainty_state["conditional_reversal_comparison"]
    assert q["pooled_exposures_disjoint"] is True
    assert q["complete_disjoint_partition"] is (not omitted and not overlap)
    assert q["interpretation"]==("DESCRIPTIVE_PARTITION_REVERSAL" if not omitted and not overlap else
                                 "SELECTED_GRID_REVERSAL_ONLY__NOT_COMPLETE_SIMPSON_PARTITION")
    assert any(x["omitted_pooled_member_n"]>0 for x in q["exposure_partitions"]) is (omitted or overlap)
    assert any(x["overlap_member_n"]>0 for x in q["exposure_partitions"]) is overlap


def _temporal_coordinate_case(tag, producer_time, subject_time):
    rows=[{"id":"R0","responses":{"Y":0},"coords":{"G":"A"}},
          {"id":"R1","responses":{"Y":1},"coords":{"G":"B"}}]
    source=native._build_source(tag,rows)
    qa=native._query_authority(tag)
    leaf=native._coordinate_leaf(source,"G","A")
    if producer_time is not None:
        leaf["effective_or_reference_time"]=producer_time
    pred=native._predicate(source,qa,leaf,tag=tag)
    q=native._query(source,qa,pred,("Y",),tag=tag)
    actual=native._run(source,qa,pred,q).facts[0]
    assert actual.typed_state=="SUPPORTED" and actual.raw_denominator_support==1
    universe,release=source["universe"].ref,source["release_ref"]
    coord,pairing=source["crefs"]["G"],fx.make_pairing_authority(tag)
    binding=fx.make_conditioner_binding(binding_id="G",subject_fact_ref=ExactRef(**fx.subject_fact_ref(source,"G","A")),
        empirical_coordinate_ref=coord,comparability_authority_ref=pairing,
        source_universe_ref=universe,release_ref=release,effective_time_or_interval=subject_time)
    consumer=fx.make_multi_conditioner_consumer_query(query_id=tag,
        subject_ref=ExactRef("TEST_ONLY_SUBJECT","urn:test:"+tag,semantic_hash(tag)),
        target_ref=source["qrefs"]["Y"],source_universe_ref=universe,release_ref=release,
        bindings=[binding],projection_kind="TEST_ONLY_TEMPORAL_CONDITION")
    witness=fx.build_witness_for_binding(witness_object_id="urn:test:"+tag+":witness",
        consumer_query=consumer,producer_query=q,producer_predicate=pred,bindings=[binding],
        coordinate_value_pairs=[(coord,"A")],pairing_authority=pairing,source_universe_ref=universe,
        release_ref=release,leaf_type="EMPIRICAL_POSITION_COORDINATE")
    return compose_positioned_subject_possibility(repository=source["repo"],empirical_query=q,predicate=pred,
        authority_registry=native._registry(source,qa),release_refs=(release,),consumer_query=consumer,
        model_rule=fx.make_model_rule(universe,tag),condition_binding_witness=witness)


def test_c1_explicit_coordinate_time_mismatch_refused():
    from rawlsing_next.pre553_analytical_composition import ConditionValueRelationMismatch
    with pytest.raises(ConditionValueRelationMismatch,match="time"):
        _temporal_coordinate_case("R3-time-mismatch","2026-01","2026-11")


@pytest.mark.parametrize("producer_time,subject_time",[
    ("2026-01","2026-01"),("2026-01",None),(None,"2026-01"),
])
def test_c1_coordinate_time_exact_or_explicitly_qualified(producer_time,subject_time):
    result=_temporal_coordinate_case(f"R3-time-{producer_time}-{subject_time}",producer_time,subject_time)
    consumer=result.consumer_result_or_null
    assert consumer.result_state=="EXACT_SUPPORTED"
    assert (consumer.exact_geometry.get("condition_scope") is not None) is (producer_time!=subject_time)
    if producer_time!=subject_time:
        assert consumer.exact_reason.endswith("SUBJECT_CONDITION_COVERAGE_NOT_ESTABLISHED")
