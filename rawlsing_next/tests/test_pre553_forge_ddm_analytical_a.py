"""Commission A: native empirical production, sourcefree only.
No independently sampled survey pooling, new issuer, or replacement scheduler.
"""
from dataclasses import replace
from itertools import product

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, canonical_json, exact_ref, semantic_hash
from rawlsing_next.pre553_s04_general_joint_algebra import (
    S04GeneralJointWorkspace, S04GeneralAlgebraError, S04Projection,
    S04ProjectionAnswer,
)
from rawlsing_next.pre553_s04_dhikr_comparative import (
    DHIKRComparisonRequest, DHIKRComparisonReceipt, read_dhikr_sample_estimate,
)
from rawlsing_next.pre553_s04_observed_research import receive_s04_i03_research
from rawlsing_next.pre553_s04_i05_reception import (
    receive_s04_i05_role, receive_s04_i05_adaptive_outcome, S04I05ReceptionError,
)
from rawlsing_next.pre553_discovery_adaptive import execute_adaptive_exploration
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.tests.test_pre553_s04_observed_research import _real
from rawlsing_next.tests.test_pyat1009_ff01_i05_role_ingress import _real_frontier
from rawlsing_next.tests import test_pre553_discovery_adaptive as adaptive


def _workspace(query, execution, **guards):
    knowledge = receive_s04_i03_research(query=query, execution=execution)
    return S04GeneralJointWorkspace(
        knowledge=knowledge, expected_knowledge_ref=knowledge.ref, **guards,
    )


def _actual(tag, rows, names):
    source = native._build_source(tag, rows)
    auth = native._query_authority(tag)
    pred = native._branch_predicate(source, auth)
    query = native._query(source, auth, pred, names, tag="forge-a")
    execution = native._run(source, auth, pred, query)
    assert execution.facts[0].typed_state == "SUPPORTED"
    return source, auth, pred, query, execution


def _counts(answer):
    return {tuple(row["output_states"]): row["raw_count"]
            for row in answer.material()["complete_output_cells"]}


def _score(node, axes):
    entry = next(r for r in node["comparative_group_evidence"] if r["axes"] == list(axes))
    return read_dhikr_sample_estimate(entry["information_bits"])


def test_exact_semantic_roles_forward_reverse_and_anti_parity():
    _, _, _, q1, ex1 = _real(0, tag="FORGE-A-PARITY")
    _, _, _, q2, ex2 = _real(1, tag="FORGE-A-ANTIPARITY")
    a, b = _workspace(q1, ex1), _workspace(q2, ex2)
    x, y, z = tuple(exact_ref(r) for r in q1.target_refs)
    for axes in ((0,), (1,), (2,), (0,1), (0,2), (1,2)):
        assert _counts(a.query(S04Projection(axes, {}))) == _counts(b.query(S04Projection(axes, {})))
    assert _counts(a.query(S04Projection((0,1,2), {}))) != _counts(b.query(S04Projection((0,1,2), {})))
    assert a.query_by_refs((z,), {x:"0", y:"0"}).ref == a.query(S04Projection((2,), {0:"0",1:"0"})).ref
    assert a.query_by_refs((x,y), {z:"0"}).ref == a.query(S04Projection((0,1), {2:"0"})).ref
    foreign = ExactRef(x.kind, x.object_id, semantic_hash("wrong-source"))
    for refs, conditions in (((foreign,), {}), ((x,x), {}), ((x,), {x:"0"})):
        with pytest.raises(S04GeneralAlgebraError):
            a.query_by_refs(refs, conditions)


def test_three_predictor_synergy_full_hierarchy_and_exact_projection_receipts():
    names = ("A","B","C","Y")
    rows = [{"id": f"R{a}{b}{c}", "responses": dict(zip(names,(a,b,c,a^b^c)))}
            for a,b,c in product((0,1), repeat=3)]
    _, _, _, q, ex = _actual("FORGE-A-THREE", rows, names)
    ws = _workspace(q, ex)
    req = DHIKRComparisonRequest(3,(0,1,2),max_depth=0,include_group_evidence=True)
    result = ws.compare_dhikr(req)
    material = result.material()
    root = material["nodes"][0]
    assert root["comparative_group_state"] == "ALL_GROUPS_WITHIN_DECLARED_ORDER_EVALUATED"
    assert len(root["comparative_group_evidence"]) == 7
    assert root["comparative_group_evidence"][0]["axes"] == [0,1,2]
    assert _score(root,(0,1,2)) == 1
    for axes in ((0,), (1,), (2,), (0,1), (0,2), (1,2)):
        assert _score(root,axes) == 0
    assert material["source_predicate_ref"] == exact_ref(q.condition_predicate_ref).as_dict()
    for group in root["comparative_group_evidence"]:
        p = group["projection_material"]
        projection = S04ProjectionAnswer(
            canonical_json(p),
            semantic_hash(p),
        )
        assert projection.ref.as_dict() == group["projection_ref"]
        assert projection.ref == ws.query(S04Projection((*group["axes"],3),{})).ref
        assert sum(row["raw_count"] for row in p["complete_output_cells"]) == 8
    assert DHIKRComparisonReceipt(result.payload_json,result.content_hash).ref == result.ref


def test_context_reverses_predictor_priority_and_retains_nonmodal_alternatives():
    names = ("D","X","Z","Y")
    rows = []
    for d,x,z in product((0,1), repeat=3):
        for i in range(4):
            y = (x if d==0 else z) ^ int(i==0)
            rows.append({"id":f"R{d}{x}{z}{i}","responses":dict(zip(names,(d,x,z,y)))})
    _, _, _, q, ex = _actual("FORGE-A-CONTEXT", rows, names)
    ws = _workspace(q,ex)
    def comparison(d, **kw):
        return ws.compare_dhikr(DHIKRComparisonRequest(
            3,(1,2),fixed_context=((0,str(d)),),include_group_evidence=True,
            max_depth=0,**kw,
        )).material()
    a,b = (comparison(d)["nodes"][0] for d in (0,1))
    assert a["raw_same_case_n"] == b["raw_same_case_n"] == 16
    assert _score(a,(1,)) > _score(a,(2,))
    assert _score(b,(2,)) > _score(b,(1,))
    for root, axis in ((a,1),(b,2)):
        chosen = next(r for r in root["comparative_group_evidence"] if r["axes"] == [axis])
        cells = chosen["projection_material"]["complete_output_cells"]
        assert sorted(row["raw_count"] for row in cells) == [2,2,6,6]
    limited = comparison(0,max_group_projection_cells=0)
    assert limited["group_projection_cells_used"] == 0
    assert limited["nodes"][0]["group_projection_coverage"] == "PARTIAL_EXPLICIT_CELL_BUDGET"
    assert len(limited["nodes"][0]["comparative_group_evidence"]) == 3
    assert all(r["projection_ref"] is None for r in limited["nodes"][0]["comparative_group_evidence"])
    held = comparison(0,min_branch_n=17)["nodes"][0]
    assert held["comparative_group_state"] == "HELD_BELOW_MINIMUM_CONTEXT_SUPPORT"
    assert held["comparative_group_evidence"] == []
    assert held["raw_target_counts"] == []


def test_actual_saved_native_joint_same_evidence_and_current(tmp_path, monkeypatch):
    pytest.importorskip("pyarrow")
    from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor, RuntimeObjectCatalog
    from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate, DirectEstateError
    from rawlsing_next.pre553_s04_dynamic_research import S04DynamicResearchSession, S04DynamicQuestion
    from rawlsing_next.pre553_distinct_cold_s04_batch import SOURCEFREE_ONLY_ASSERTION
    from rawlsing_next.tests.test_pre553_direct_estate_i03 import _cold
    captured = {}
    ingest = native.ingest_c11_source_release
    def capture(candidate, repo):
        captured["candidate"] = candidate
        return ingest(candidate, repo)
    with monkeypatch.context() as patch:
        patch.setattr(native,"ingest_c11_source_release",capture)
        source, auth, pred, query, oracle = _real(tag="FORGE-A-SAVED-XOR")
    root, receipt = _cold(tmp_path,captured["candidate"],source["universe"].ref,"FORGE-A-SAVED-XOR")
    live = {"yes":True}
    estate = VerifiedDirectEstate(
        root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        current_authorizer=lambda _:live["yes"],
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"],auth)),predicates=(pred,),
        queries=(query,),discovery_authorities=(),
    )
    executor = CarrierNeutralResearchExecutor(
        repository=estate,release_refs=(source["release_ref"],),runtime_catalog=catalog,
    )
    with S04DynamicResearchSession(executor=executor,sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION) as session:
        actual = session.ask(S04DynamicQuestion(query.ref,pred.ref))
        assert actual.original.execution.facts[0].ref == oracle.facts[0].ref
        ws = actual.joint_workspace
        req = DHIKRComparisonRequest(2,(0,1),include_group_evidence=True,max_depth=1)
        comparison = ws.compare_dhikr(req).material()
        assert _score(comparison["nodes"][0],(0,1)) == 1
        assert actual.observation_scope.material()["fact_ref"] == oracle.facts[0].ref.as_dict()
        assert session.stats()["original_native_i03_queries_executed"] == 1
        live["yes"] = False
        with pytest.raises(DirectEstateError):
            ws.compare_dhikr(req)


def test_generated_sav_saved_first_consumer_supports_semantic_projection(tmp_path):
    pytest.importorskip("pyarrow")
    from rawlsing_next.tests.test_pyat997_s1e_saved_native_first_consumer import _full
    from rawlsing_next.tests.test_pyat997_saved_s04_observation_vertical import _issued_q101
    from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03_to_s04
    _, _, admission, compilation, _, _ = _full(tmp_path/"actual")
    query = _issued_q101(compilation)
    result = execute_saved_i03_to_s04(admission,query=query,predicate_ref=exact_ref(query.condition_predicate_ref))
    knowledge = result.first_consumer.knowledge
    ws = S04GeneralJointWorkspace(knowledge=knowledge,expected_knowledge_ref=knowledge.ref,current_guard=admission.check_current)
    projection = ws.query_by_refs((exact_ref(query.target_refs[0]),),{})
    assert projection.material()["raw_selected_full_case_n"] == 5
    assert projection.material()["source_fact_ref"] == result.execution.facts[0].ref.as_dict()
    assert result.observation_scope.material()["fact_ref"] == projection.material()["source_fact_ref"]


def test_actual_i05_to_existing_adaptive_scheduler_retains_visited_and_unknown():
    discovery = _real_frontier()
    positive = next(r for r in discovery.receipts if r.typed_state=="DISCOVERED_RESULT_SUPPORTED")
    negative = next(r for r in discovery.receipts if r.typed_state=="VALID_EMPTY")
    authority, registry, rule, child_rule = adaptive._authority("forge-a")
    determinant = adaptive._ref("DETERMINANT","forge-a")
    root = adaptive._unit("root",determinant,rule,rank=10,extra=(discovery.discovery_authority_ref,))
    other = adaptive._unit("other",determinant,rule,rank=0,extra=(discovery.discovery_authority_ref,))
    _, basis = receive_s04_i05_role(discovery=discovery,candidate_receipt_ref=positive.ref,query_role="BASE")
    child = adaptive._unit("child",determinant,child_rule,rank=20,generation=1,parent=root.unit_ref,
                           extra=(discovery.discovery_authority_ref,discovery.replay_ref,basis.ref))
    def evaluate(unit, history):
        selected = positive if unit==root else negative
        observed, role, outcome = receive_s04_i05_adaptive_outcome(
            unit=unit,discovery=discovery,expected_replay_ref=discovery.replay_ref,
            candidate_receipt_ref=selected.ref,query_role="BASE",current_guard=lambda:True,
            proposal_units=(child,) if unit==root else (),
        )
        assert observed.material()["state"] == "SUPPORTED_SAMPLE_DESCRIPTIVE"
        assert outcome.proposal_basis_ref == role.ref
        return outcome
    first = execute_adaptive_exploration(discovery_authority=authority,authority_registry=registry,
        determinant_state_ref=determinant,initial_units=(root,other),evaluate_unit=evaluate,budget=1)
    assert set(first.unvisited_unit_refs)=={child.unit_ref,other.unit_ref}
    assert first.global_negative_claim is False
    final = execute_adaptive_exploration(discovery_authority=authority,authority_registry=registry,
        determinant_state_ref=determinant,initial_units=(root,other),evaluate_unit=evaluate,budget=3,
        resume_from=first.checkpoint)
    assert final.visited_unit_refs == (root.unit_ref,child.unit_ref,other.unit_ref)
    assert final.checkpoint.visits[1].outcome.unit_result_state == "I05_COMPLETE_FRONTIER__SELECTED_VALID_EMPTY"
    assert final.global_negative_claim is False
    for guard,replay in ((lambda:False,discovery.replay_ref),(lambda:True,root.unit_ref)):
        with pytest.raises(S04I05ReceptionError):
            receive_s04_i05_adaptive_outcome(unit=root,discovery=discovery,expected_replay_ref=replay,
                candidate_receipt_ref=positive.ref,query_role="BASE",current_guard=guard)


def test_pinned_frontier_rejects_dropped_receipts_and_false_empty():
    discovery = _real_frontier()
    positive = next(r for r in discovery.receipts if r.typed_state == "DISCOVERED_RESULT_SUPPORTED")
    _, _, rule, _ = adaptive._authority("forged-frontier")
    determinant = adaptive._ref("DETERMINANT","forged-frontier")
    root = adaptive._unit("root",determinant,rule,rank=0,extra=(discovery.discovery_authority_ref,))
    # Native dataclass alone permits a changed receipt tuple with the old
    # claimed replay. The new sealed-result receiver checks the actual closure.
    smaller = tuple(r for r in discovery.receipts if r.ref != discovery.receipts[-1].ref
                    or r.ref == positive.ref)
    if len(smaller) == len(discovery.receipts):
        smaller = tuple(r for r in discovery.receipts if r.ref != discovery.receipts[0].ref
                        or r.ref == positive.ref)
    assert len(smaller) == len(discovery.receipts)-1
    for counterfeit in (
        replace(discovery, receipts=smaller),
        replace(discovery, receipts=smaller, candidate_count=len(smaller), covered_candidate_count=len(smaller)),
        replace(discovery, valid_empty=True),
    ):
        with pytest.raises(S04I05ReceptionError):
            receive_s04_i05_adaptive_outcome(
                unit=root,discovery=counterfeit,expected_replay_ref=discovery.replay_ref,
                candidate_receipt_ref=positive.ref,query_role="BASE",current_guard=lambda:True,
            )


def test_real_recursive_handoff_to_new_native_i05_through_adaptive_resume(tmp_path):
    from rawlsing_next.pre553_recursive_handoff import (
        execute_exact_bounded_discovery_with_handoffs, recursive_parent_atom,
        write_recursive_handoff_bundle, load_recursive_handoff_bundle,
        replay_recursive_branch_membership,
    )
    from rawlsing_next.tests import test_pre553_recursive_handoff as recursive
    from rawlsing_next.tests import test_pre553_discovery_exact as i05
    source, auth = recursive._fixture()
    _, gen1, reg1 = recursive._generation_one(source,auth)
    first = gen1.discovery_result
    original_handoff = gen1.handoffs[0]
    assert len(replay_recursive_branch_membership(
        repository=source["repo"],handoff=original_handoff,authority_registry=reg1)) == 4
    first_receipt = first.receipts[0]
    _, basis = receive_s04_i05_role(discovery=first,candidate_receipt_ref=first_receipt.ref,query_role="CONDITION")
    authority, registry, rule, child_rule = adaptive._authority("forge-a-recursive")
    determinant = adaptive._ref("DETERMINANT","forge-a-recursive")
    root = adaptive._unit("root",determinant,rule,rank=1,extra=(first.discovery_authority_ref,))
    # Persist/reopen the original owner handoff before constructing generation 2.
    handoff_path = tmp_path/"branch.json"
    bundle = write_recursive_handoff_bundle(handoff_path,gen1.handoffs)
    loaded_bundle, handoffs = load_recursive_handoff_bundle(handoff_path)
    assert loaded_bundle == bundle
    parent = handoffs[0]
    assert parent.ref == original_handoff.ref
    h1 = native._predicate(source,auth,native._response_leaf(source,auth,"H",1),tag="mx01r2-h1")
    q = native._query(source,auth,parent.winning_predicate,("H",),tag="mx01r2-g2-h")
    da = i05._d_auth("mx01r2-g2-discovery")
    grammar = i05._grammar(
        operation="I03-OP-mx01r2-g2-discovery",
        atoms=[recursive_parent_atom(parent,"CHILD"),i05._atom("H1",h1,"RESPONSE")],
        templates=[i05._qt("H",q)],
        rules=[i05._rule("grandchild","RECURSIVE_SUBGROUP_FORK","SINGLE_ATOM",
                         atom_ids=("H1",),baseline_atom_id="CHILD",query_template_id="H",
                         validation={"kind":"DISTRIBUTION_DIFFERS_FROM_BASELINE"})],k=2,
    )
    da2 = i05._discovery_authority(source,grammar,da,tag="mx01r2-g2")
    reg2 = native._registry(source,auth,da)
    child = adaptive._unit("child",determinant,child_rule,rank=2,generation=1,parent=root.unit_ref,
        extra=(da2.ref,first.replay_ref,basis.ref,parent.ref,parent.winning_predicate.ref))
    executions = []
    def evaluate(unit,history):
        if unit == root:
            return receive_s04_i05_adaptive_outcome(
                unit=unit,discovery=first,expected_replay_ref=first.replay_ref,
                candidate_receipt_ref=first_receipt.ref,query_role="CONDITION",current_guard=lambda:True,
                proposal_units=(child,),next_handoff=parent,
            )[2]
        # The child is NOT a replay of the old candidate; run a newly issued
        # native exact frontier with the persisted discovered branch predicate.
        assert unit == child and len(history)==1
        actual = execute_exact_bounded_discovery_with_handoffs(
            repository=source["repo"],discovery_authority=da2,authority_registry=reg2,
            release_refs=(source["release_ref"],),predicate_catalog=(parent.winning_predicate,h1),
            query_template_catalog=(q,),
        )
        second = actual.discovery_result
        executions.append(second.replay_ref)
        assert second.replay_ref != first.replay_ref
        assert len(replay_recursive_branch_membership(
            repository=source["repo"],handoff=actual.handoffs[0],authority_registry=reg2)) == 2
        observed, role, outcome = receive_s04_i05_adaptive_outcome(
            unit=unit,discovery=second,expected_replay_ref=second.replay_ref,
            candidate_receipt_ref=second.receipts[0].ref,query_role="CONDITION",
            current_guard=lambda:True,parent_handoff=parent,
        )
        assert observed.material()["raw_fully_resolved_joint_n"] == 2
        # Ancestor hash in a scheduler determinant is not enough by itself.
        with pytest.raises(S04I05ReceptionError,match="parent handoff"):
            receive_s04_i05_adaptive_outcome(
                unit=unit,discovery=second,expected_replay_ref=second.replay_ref,
                candidate_receipt_ref=second.receipts[0].ref,query_role="CONDITION",current_guard=lambda:True,
            )
        return outcome
    with pytest.raises(S04I05ReceptionError,match="winning handoff"):
        receive_s04_i05_adaptive_outcome(
            unit=root,discovery=first,expected_replay_ref=first.replay_ref,
            candidate_receipt_ref=first_receipt.ref,query_role="CONDITION",current_guard=lambda:True,
            proposal_units=(child,),
        )
    partial = execute_adaptive_exploration(discovery_authority=authority,authority_registry=registry,
        determinant_state_ref=determinant,initial_units=(root,),evaluate_unit=evaluate,budget=1)
    assert partial.unvisited_unit_refs == (child.unit_ref,) and not executions
    restored = adaptive.AdaptiveSearchCheckpoint.from_dict(partial.checkpoint.as_dict())
    resumed = execute_adaptive_exploration(discovery_authority=authority,authority_registry=registry,
        determinant_state_ref=determinant,initial_units=(root,),evaluate_unit=evaluate,budget=1,resume_from=restored)
    assert len(executions)==1 and resumed.unvisited_unit_refs==()
    assert resumed.checkpoint.visits[-1].outcome.sealed_result_ref == executions[0]
    assert resumed.global_negative_claim is False


def test_s2f_original_native_closure_recreates_exact_analytical_outputs(tmp_path):
    from rawlsing_next.pre553_durable_empirical_closure import publish_empirical_closure, open_empirical_closure
    from rawlsing_next.tests.test_pyat940_s2f_durable_closure import _k_way_output
    native_output = _k_way_output()
    actual = native_output.i03_results[0]
    query = next(q for q in native_output.object_graph.executed_queries if q.ref == actual.query_ref)
    before = _workspace(query,actual)
    request = DHIKRComparisonRequest(3,(0,1,2),max_depth=1,include_group_evidence=True)
    projected = before.query(S04Projection((0,3),{1:"0"}))
    compared = before.compare_dhikr(request)
    saved = publish_empirical_closure(native_output,tmp_path/"cas")
    restored = open_empirical_closure(saved.root_path,expected_root=saved.root_identity).require_trusted()
    restored.assert_no_current_authority()
    cold = restored.i03_results[0]
    cold_query = next(q for q in restored.object_graph.executed_queries if q.ref == cold.query_ref)
    after = _workspace(cold_query,cold)
    assert cold.facts[0].ref == actual.facts[0].ref
    assert after.query(S04Projection((0,3),{1:"0"})).ref == projected.ref
    assert after.compare_dhikr(request).ref == compared.ref
