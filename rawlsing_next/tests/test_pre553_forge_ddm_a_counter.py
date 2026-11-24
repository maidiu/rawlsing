"""Counter-turn: actual native complete frontier and recursive ancestry."""
from dataclasses import replace
from itertools import product
import pytest
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_s04_i05_reception import (
    S04I05ReceptionError, receive_s04_i05_adaptive_outcome, receive_s04_i05_role,
    _require_pinned_frontier,
)
from rawlsing_next.pre553_discovery_adaptive import execute_adaptive_exploration
from rawlsing_next.pre553_recursive_handoff import (
    execute_exact_bounded_discovery_with_handoffs, recursive_parent_atom,
    replay_recursive_branch_membership, _derived_ref,
)
from rawlsing_next.tests import test_pre553_discovery_exact as i05
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.tests import test_pre553_discovery_adaptive as adaptive
from rawlsing_next.tests import test_pre553_recursive_handoff as recursive
from rawlsing_next.tests.test_pre553_forge_ddm_analytical_a import _actual, _workspace


def _unit(discovery, tag, extra=()):
    authority, registry, rule, child_rule = adaptive._authority(tag)
    determinant = adaptive._ref("DETERMINANT", tag)
    root = adaptive._unit("root", determinant, rule, rank=1,
                          extra=(discovery.discovery_authority_ref, *extra))
    return authority, registry, determinant, root, child_rule


def _receive(discovery, unit, **kw):
    return receive_s04_i05_adaptive_outcome(
        unit=unit, discovery=discovery, expected_replay_ref=discovery.replay_ref,
        current_guard=lambda: True, **kw)


def test_genuine_zero_candidate_frontier_closes_scheduler_without_invented_fact():
    source = native._build_source("COUNTER-EMPTY", [
        {"id": "R0", "responses": {"Y":0}}, {"id":"R1","responses":{"Y":1}}])
    qa, da = native._query_authority("COUNTER-EMPTY"), i05._d_auth("COUNTER-EMPTY-discovery")
    grammar = i05._grammar(operation="I03-OP-COUNTER-EMPTY", atoms=(),
                            templates=(), rules=(), allow_empty=True)
    result = i05._execute(source,qa,da,grammar,(),())
    assert result.valid_empty and result.candidate_count == 0
    authority, registry, determinant, root, _ = _unit(result,"counter-empty")
    import os, importlib.util, sys
    old_path = os.environ.get("FORGE_B_PREDECESSOR_I05")
    if old_path:
        spec = importlib.util.spec_from_file_location("forge_b_frozen_receiver",old_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        try:
            spec.loader.exec_module(module)
            with pytest.raises(module.S04I05ReceptionError, match="nonempty role"):
                module.receive_s04_i05_adaptive_outcome(
                    unit=root,discovery=result,expected_replay_ref=result.replay_ref,
                    candidate_receipt_ref=None,query_role=None,current_guard=lambda:True)
        finally:
            sys.modules.pop(spec.name,None)
    def evaluate(unit, history):
        knowledge, role, outcome = _receive(result,unit,candidate_receipt_ref=None,query_role=None)
        assert knowledge is None and role is None
        assert outcome.unit_result_state == "I05_COMPLETE_DECLARED_FRONTIER__ZERO_CANDIDATES"
        assert outcome.proposal_basis_ref == result.replay_ref
        assert not outcome.global_negative_claim and not outcome.proposal_units
        return outcome
    search = execute_adaptive_exploration(discovery_authority=authority,authority_registry=registry,
        determinant_state_ref=determinant,initial_units=(root,),evaluate_unit=evaluate,budget=1)
    assert search.visited_unit_refs == (root.unit_ref,) and not search.unvisited_unit_refs


def _two_parents():
    source, auth = recursive._fixture()
    parent, first, _ = recursive._generation_one(source, auth)
    h1 = native._predicate(source,auth,native._response_leaf(source,auth,"H",1),tag="counter-h1")
    q = native._query(source,auth,parent,("H",),tag="counter-h")
    da = i05._d_auth("counter-sibling")
    grammar = i05._grammar(operation="I03-OP-counter-sibling",
        atoms=[i05._atom("PARENT",parent,"BRANCH"),i05._atom("H1",h1,"RESPONSE")],
        templates=[i05._qt("H",q)],
        rules=[i05._rule("sibling","RECURSIVE_SUBGROUP_FORK","SINGLE_ATOM",
            atom_ids=("H1",),baseline_atom_id="PARENT",query_template_id="H",
            validation={"kind":"DISTRIBUTION_DIFFERS_FROM_BASELINE"})],k=2)
    authority = i05._discovery_authority(source,grammar,da,tag="counter-sibling")
    second = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],discovery_authority=authority,
        authority_registry=native._registry(source,auth,da),
        release_refs=(source["release_ref"],),predicate_catalog=(parent,h1),
        query_template_catalog=(q,))
    p1,p2 = first.handoffs[0],second.handoffs[0]
    q3 = native._query(source,auth,p1.winning_predicate,("H",),tag="counter-intersection")
    da3 = i05._d_auth("counter-intersection")
    grammar3 = i05._grammar(operation="I03-OP-counter-intersection",
        atoms=[recursive_parent_atom(p1,"A"),recursive_parent_atom(p2,"B")],
        templates=[i05._qt("H",q3)],
        rules=[i05._rule("intersection","RECURSIVE_SUBGROUP_FORK","SINGLE_ATOM",
            atom_ids=("B",),baseline_atom_id="A",query_template_id="H",
            validation={"kind":"DISTRIBUTION_DIFFERS_FROM_BASELINE"})],k=2)
    authority3 = i05._discovery_authority(source,grammar3,da3,tag="counter-intersection")
    reg3 = native._registry(source,auth,da3)
    third = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],discovery_authority=authority3,authority_registry=reg3,
        release_refs=(source["release_ref"],),predicate_catalog=(p1.winning_predicate,p2.winning_predicate),
        query_template_catalog=(q3,))
    return source, first, (p1,p2), authority3, reg3, third


def test_native_multi_parent_cannot_be_received_with_one_parent():
    source, first, (p1,p2), authority, registry, third = _two_parents()
    result = third.discovery_result
    receipt = result.receipts[0]
    assert receipt.typed_state == "DISCOVERED_RESULT_SUPPORTED"
    assert {exact_ref(r) for r in receipt.branch_or_parent_ancestry_refs} == {p1.ref,p2.ref}
    assert len(replay_recursive_branch_membership(repository=source["repo"],
        handoff=third.handoffs[0],authority_registry=registry)) == 2
    _,_,_,unit,_ = _unit(result,"counter-multi",extra=(
        p1.ref,p2.ref,p1.winning_predicate.ref,p2.winning_predicate.ref))
    with pytest.raises(S04I05ReceptionError):
        _receive(result,unit,candidate_receipt_ref=receipt.ref,query_role="CONDITION",parent_handoff=p1)


def test_rehashed_winning_handoff_cannot_substitute_immediate_baseline():
    source, auth = recursive._fixture()
    _, first, _ = recursive._generation_one(source,auth)
    discovery = first.discovery_result
    original = first.handoffs[0]
    receipt = discovery.receipts[0]
    foreign = original.winning_predicate.ref
    assert foreign != original.immediate_parent_branch_ref
    deterministic = dict(original.deterministic_parameters)
    deterministic["immediate_parent_branch_ref"] = foreign.as_dict()
    binding = replace(original.branch_replay_binding,
        parent_branch_ref_or_typed_absence=foreign,
        deterministic_parameters_ref_or_typed_absence=_derived_ref(
            "PRE553_RECURSIVE_DETERMINISTIC_PARAMETERS","deterministic-parameters",deterministic))
    counterfeit = replace(original,branch_replay_binding=binding,
                          deterministic_parameters=deterministic)
    assert counterfeit.ref != original.ref
    _,_,determinant,root,child_rule = _unit(discovery,"counter-baseline")
    _, role = receive_s04_i05_role(discovery=discovery,candidate_receipt_ref=receipt.ref,
                                  query_role="CONDITION")
    child = adaptive._unit("child",determinant,child_rule,rank=2,generation=1,parent=root.unit_ref,
        extra=(discovery.replay_ref,role.ref,counterfeit.ref,counterfeit.winning_predicate.ref))
    with pytest.raises(S04I05ReceptionError):
        _receive(discovery,root,candidate_receipt_ref=receipt.ref,query_role="CONDITION",
                 next_handoff=counterfeit,proposal_units=(child,))


def test_all_native_parents_survive_persist_reload_and_intersection(tmp_path):
    from rawlsing_next.pre553_recursive_handoff import (
        write_recursive_handoff_bundle, load_recursive_handoff_bundle,
    )
    source, _, parents, authority, registry, third = _two_parents()
    p1,p2 = parents
    result = third.discovery_result
    path = tmp_path/"parents.json"
    pin = write_recursive_handoff_bundle(path,parents)
    restored_pin, restored = load_recursive_handoff_bundle(path)
    assert restored_pin == pin and {p.ref for p in restored} == {p1.ref,p2.ref}
    _,_,_,unit,_ = _unit(result,"counter-multi-positive",extra=(
        p1.ref,p2.ref,p1.winning_predicate.ref,p2.winning_predicate.ref))
    kwargs = dict(candidate_receipt_ref=result.receipts[0].ref,query_role="CONDITION")
    observed, role, outcome = _receive(result,unit,**kwargs,
        parent_handoffs=restored,discovery_authority=authority)
    assert observed.material()["raw_fully_resolved_joint_n"] == 2
    assert outcome.proposal_basis_ref == role.ref
    for wrong in (dict(parent_handoffs=restored),dict(parent_handoffs=(p1,p1),discovery_authority=authority),
                  dict(parent_handoffs=(p1,),discovery_authority=authority)):
        with pytest.raises(S04I05ReceptionError):
            _receive(result,unit,**kwargs,**wrong)


def test_default_dhikr_exact_predecessor_identity_across_noncanonical_contexts():
    import importlib.util
    import os
    import sys
    from rawlsing_next.pre553_s04_dhikr_comparative import DHIKRComparisonRequest
    path = os.environ.get("FORGE_A_PREDECESSOR")
    if not path:
        pytest.skip("exact predecessor source supplied by counter CI")
    spec = importlib.util.spec_from_file_location("forge_a_frozen_predecessor",path)
    frozen = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = frozen
    try:
        spec.loader.exec_module(frozen)
        names = ("A","B","C","D","E","Y")
        rows = []
        for a,b,c,d,e in product((0,1),repeat=5):
            for i in range(2):
                y = (a ^ b ^ c) if d else (e ^ int(i==0 and a==1))
                rows.append({"id":f"R{a}{b}{c}{d}{e}{i}","responses":dict(zip(names,(a,b,c,d,e,y)))})
        _,_,_,q,ex = _actual("COUNTER-LEGACY-PARITY",rows,names)
        ws = _workspace(q,ex)
        for order, depth, context, bootstrap in product((1,2,3),(0,2),((),((3,"0"),)),(0,12)):
            args = dict(target_axis=5,predictor_axes=(4,2,0,3,1),max_interaction_order=order,
                        max_depth=depth,fixed_context=context,bootstrap_replicates=bootstrap)
            prior = frozen.analyze_s04_dhikr(ws,frozen.DHIKRComparisonRequest(**args))
            actual = ws.compare_dhikr(DHIKRComparisonRequest(**args))
            assert actual.ref == prior.ref
            assert actual.payload_json == prior.payload_json
    finally:
        sys.modules.pop(spec.name,None)


def test_all_eleven_native_candidate_families_and_every_role_reach_reception():
    from rawlsing_next.pre553_discovery_exact import CANDIDATE_FAMILIES
    rows = [{"id":f"R{x}{y}{g}","responses":{"X":x,"Y":y,"Z":x^y},
             "coords":{"G":g}} for x,y,g in product((0,1),(0,1),("A","B"))]
    source = native._build_source("COUNTER-FAMILIES",rows)
    qa, da = native._query_authority("COUNTER-FAMILIES"), i05._d_auth("COUNTER-FAMILIES-discovery")
    all_p = native._branch_predicate(source,qa,tag="all")
    x1 = native._predicate(source,qa,native._response_leaf(source,qa,"X",1),tag="x1")
    x0 = native._predicate(source,qa,native._response_leaf(source,qa,"X",0),tag="x0")
    ga = native._predicate(source,qa,native._coordinate_leaf(source,"G","A"),tag="ga")
    gb = native._predicate(source,qa,native._coordinate_leaf(source,"G","B"),tag="gb")
    yq = native._query(source,qa,all_p,("Y",),tag="Y")
    jq = native._query(source,qa,all_p,("X","Y","Z"),tag="J")
    mq = [native._query(source,qa,all_p,(name,),tag="m"+name) for name in ("X","Y","Z")]
    rules = []
    for family in sorted(CANDIDATE_FAMILIES - {"BOUNDED_K_WAY_RESPONSE_CONFIGURATION","CONDITIONAL_REVERSAL_OR_SIMPSON"}):
        if family in {"RESPONSE_X_COORDINATE_CONJUNCTION","BOUNDED_COORDINATE_CONJUNCTION"}:
            form, args = "AND_COMBINATIONS",dict(atom_ids=("X1","GA") if family.startswith("RESPONSE") else ("GA","GB"),arity=2)
        else:
            form, args = "SINGLE_ATOM",dict(atom_ids=("GA",) if family in {"RESPONSE_X_EMPIRICAL_COORDINATE","UNARY_SOCIAL_FORK","MINORITY_OR_NONMODAL_DEPARTURE"} else ("X1",))
        rules.append(i05._rule(family,family,form,baseline_atom_id="ALL",query_template_id="Y",
                               validation={"kind":"DISTRIBUTION_DIFFERS_FROM_BASELINE"},**args))
    rules.extend([
        i05._rule("joint","BOUNDED_K_WAY_RESPONSE_CONFIGURATION","JOINT_DEPENDENCE",
            baseline_atom_id="ALL",joint_template_id="J",marginal_template_ids=("M0","M1","M2"),
            validation={"kind":"JOINT_NOT_PRODUCT_OF_MARGINALS"}),
        i05._rule("reversal","CONDITIONAL_REVERSAL_OR_SIMPSON","REVERSAL_GRID",
            baseline_atom_id="ALL",exposure_positive_atom_id="X1",exposure_negative_atom_id="X0",
            stratum_atom_ids=("GA","GB"),query_template_id="Y",
            validation={"kind":"CONDITIONAL_REVERSAL","target_cell":"1"}),
    ])
    grammar = i05._grammar(operation="I03-OP-COUNTER-FAMILIES-discovery",
        atoms=[i05._atom(k,p,kind) for k,p,kind in
               (("ALL",all_p,"BRANCH"),("X1",x1,"RESPONSE"),("X0",x0,"RESPONSE"),("GA",ga,"COORDINATE"),("GB",gb,"COORDINATE"))],
        templates=[i05._qt("Y",yq),i05._qt("J",jq),*[i05._qt("M"+str(i),q) for i,q in enumerate(mq)]],
        rules=rules,k=2,j=3)
    result = i05._execute(source,qa,da,grammar,(all_p,x1,x0,ga,gb),(yq,jq,*mq))
    assert {r.candidate_identity["family"] for r in result.receipts} == CANDIDATE_FAMILIES
    _require_pinned_frontier(result,result.replay_ref)
    _,_,_,unit,_ = _unit(result,"counter-families")
    observed_roles = set()
    for receipt in result.receipts:
        for entry in receipt.candidate_identity["query_roles"]:
            knowledge, role, outcome = _receive(result,unit,candidate_receipt_ref=receipt.ref,query_role=entry["role"])
            assert role.material()["candidate_validation_state"] == receipt.typed_state
            assert knowledge.material()["query_ref"] == dict(entry["query_ref"])
            observed_roles.add(entry["role"])
            assert not outcome.global_negative_claim
    assert {"JOINT","MARGINAL_0","CONDITION","BASELINE","POOLED_POS","STRATUM:GA:NEG"} <= observed_roles


@pytest.mark.parametrize("case,coverage",[
    ("empty","EVALUATED_VALID_EMPTY"),
    ("underpowered","EVALUATED_UNDERPOWERED"),
    ("unresolved","EVALUATED_UNRESOLVED"),
    ("unavailable","EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY"),
])
def test_native_nonpositive_fates_can_close_without_inventing_s04(case,coverage):
    from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
    from rawlsing_next.tests.mx01r2_fresh_process_runner import _authority_with_minimum
    tag="counter-fate-"+case
    source = native._build_source(tag,[{"id":"R0","responses":{"Y":0}},{"id":"R1","responses":{"Y":1}}],
        topology_by_question={"Y":"UNORDERED_MULTISELECT_SET"} if case=="unresolved" else None)
    qa,da=native._query_authority(tag),i05._d_auth(tag+"-discovery")
    pred=native._branch_predicate(source,qa,tag="all")
    q=native._query(source,qa,pred,("Y",),tag=tag)
    cell="1" if case!="empty" else "0"
    if case=="empty":
        pred=native._branch_predicate(source,qa,members=(),tag="empty")
        q=native._query(source,qa,pred,("Y",),tag=tag)
    grammar=i05._grammar(operation="I03-OP-"+tag+"-discovery",
        atoms=[i05._atom("ALL",pred,"BRANCH")],templates=[i05._qt("Y",q)],
        rules=[i05._rule("cell","UNARY_SOCIAL_FORK","BASE_QUERY",baseline_atom_id="ALL",query_template_id="Y",
                        target_cells=(cell,),validation={"kind":"TARGET_CELL_SUPPORTED"})])
    auth=_authority_with_minimum(source,grammar,da,3,tag=tag) if case=="underpowered" else i05._discovery_authority(source,grammar,da,tag=tag)
    release=native._ref("C11LogicalRelease","missing-counter") if case=="unavailable" else source["release_ref"]
    result=execute_exact_bounded_discovery(repository=source["repo"],discovery_authority=auth,
        authority_registry=native._registry(source,qa,da),release_refs=(release,),predicate_catalog=(pred,),
        query_template_catalog=(q,))
    receipt=result.receipts[0]
    assert receipt.coverage_state==coverage
    _,_,_,unit,_=_unit(result,tag)
    knowledge,role,outcome=_receive(result,unit,candidate_receipt_ref=receipt.ref,query_role=None)
    assert knowledge is None and role is None
    assert outcome.proposal_basis_ref==receipt.ref
    assert outcome.unit_result_state.endswith("__NATIVE_RECEIPT_ONLY")
    assert not outcome.global_negative_claim and not outcome.semantic_truth_effect


@pytest.mark.parametrize("source_format",["SAV","DTA"])
def test_combined_generated_cold_pipeline_exposes_revised_fibres(tmp_path,monkeypatch,source_format):
    from rawlsing_next.tests import test_pyat_commission_b_saved_delivery as delivery
    from rawlsing_next.pre553_s04_dhikr_comparative import DHIKRComparisonRequest
    from rawlsing_next.pre553_s04_general_joint_algebra import S04Projection
    opened=[]
    original=delivery.open_saved_product
    def capture(*args,**kwargs):
        cold=original(*args,**kwargs)
        opened.append(cold)
        return cold
    monkeypatch.setattr(delivery,"open_saved_product",capture)
    # Actual owner's complete generated-source -> deleted native estate ->
    # pinned S2-F -> FF01 and M1 test. No new source or custody implementation.
    delivery.test_generated_joint_source_to_persistent_ff01(tmp_path,monkeypatch,source_format)
    cold=opened[0]
    closure=cold._closure
    assert closure.i05_result.receipts
    _require_pinned_frontier(closure.i05_result,closure.i05_result.replay_ref)
    checked=0
    for execution in closure.i03_results:
        q=closure.query_by_ref(execution.query_ref)
        if len(q.target_refs)!=2 or execution.facts[0].typed_state!="SUPPORTED":
            continue
        ws=cold.joint_workspace(q.ref)
        comparison=ws.compare_dhikr(DHIKRComparisonRequest(1,(0,),max_depth=0,include_group_evidence=True))
        node=comparison.material()["nodes"][0]
        if not node["comparative_group_evidence"]:
            continue
        group=node["comparative_group_evidence"][0]
        for fibre in group["conditional_target_fibres"]:
            direct=ws.query(S04Projection((1,),{0:fibre["group_states"][0]})).material()
            assert fibre["raw_group_full_case_n"]==direct["raw_selected_full_case_n"]
            assert [r["conditional_raw_fraction"] for r in fibre["target_rows"]]==[
                r["raw_fraction_of_selected_full_cases"] for r in direct["complete_output_cells"]]
        checked+=1
    assert checked
