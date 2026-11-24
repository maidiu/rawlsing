"""Actual generated SAV -> saved C11 -> issued Batch -> S2-F -> cold S04."""
from dataclasses import replace
from pathlib import Path
from time import monotonic
import shutil
import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_durable_empirical_closure import DurableEmpiricalClosureError
from rawlsing_next.pre553_issued_workload import WorkloadAdmissionError
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_governed_query_issuer_v2 import _issue_compiled_governed_queries_v2
from rawlsing_next.pre553_saved_durable_delivery import (
    execute_publish_saved, open_saved_product, SavedDeliveryError,
)
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.tests import test_pyat997_s1e_saved_native_first_consumer as s1e
from rawlsing_next.tests.test_pyat997_r03_governed_query_issuer_v2 import _v2_admission


def test_generated_sav_saved_workload_durable_cold_delivery(tmp_path, monkeypatch):
    handoff, estate, initial, v1, _, _ = s1e._full(tmp_path / "source")
    issue = _issue_compiled_governed_queries_v2(v1)
    workload = issue.issued.workload
    resolver = TestOnlyDecisionResolver(issue.issued.record)
    calls = []
    original = DirectEstateI03Session._build

    def counted(self):
        calls.append(1)
        return original(self)

    monkeypatch.setattr(DirectEstateI03Session, "_build", counted)
    assert handoff.stats.source_reads == 1
    product = execute_publish_saved(
        workload, resolver, host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
        saved_admission_factory=lambda: _v2_admission(initial, workload.catalog),
        root_dir=tmp_path / "products",
    )
    assert calls == [1]
    assert product.batch_census["complete"]
    assert product.batch_census["unit_count"] == len(workload.requests) + 1
    assert len(workload.requests) > 1
    assert product.receipt.published
    # Remove the actual saved C11 to make accidental cold native recomputation impossible.
    shutil.rmtree(estate.path)

    def forbidden(*args, **kwargs):
        raise AssertionError("cold serving reopened the native reader")

    monkeypatch.setattr(DirectEstateI03Session, "_build", forbidden)
    monkeypatch.setattr(SavedC11Admission, "open", forbidden)
    kwargs = dict(expected_root=product.receipt.root_identity,
                  expected_release_ref=initial.release_ref,
                  expected_saved_manifest_sha256=initial.manifest_sha256,
                  workload=workload, resolver=resolver, host=s1e._NATIVE_HOST,
                  purpose=s1e._NATIVE_PURPOSE)
    cold = open_saved_product(product.receipt.root_path, **kwargs)
    reads = [cold.read_s04(r.query_ref) for r in workload.requests]
    assert {r.first_consumer.execution.query_ref for r in reads} == {
        r.query_ref for r in workload.requests}
    assert {r.first_consumer.knowledge.material()["state"] for r in reads} >= {
        "SUPPORTED_SAMPLE_DESCRIPTIVE", "PRODUCER_TYPED_HELD"}
    negative_scope_count = 0
    for read in reads:
        native_fact = read.first_consumer.execution.facts[0]
        if not hasattr(native_fact, "risk_set_member_refs"):
            negative_scope_count += 1
            scope = read.observation_scope.material()
            assert scope["i03_risk_member_extent_n"] is None
            assert scope["i03_known_true_condition_n"] is None
            assert scope["verified_eligible_member_set_sha256"] is None
            assert scope["state"] == "ORIGINAL_I03_NONPOSITIVE__COHORT_NOT_QUALIFIED"
    assert negative_scope_count > 0
    for request, read in zip(workload.requests, reads):
        assert read.first_consumer.execution.query_ref == request.query_ref
        assert read.observation_scope.material()["fact_ref"] == (
            read.first_consumer.execution.facts[0].ref.as_dict())
    assert cold.read_s04(workload.requests[0].query_ref).first_consumer.knowledge.ref == (
        reads[0].first_consumer.knowledge.ref)
    with pytest.raises(SavedDeliveryError, match="QUERY_NOT_IN_RETAINED"):
        cold.read_s04(workload.discoveries[0])
    with pytest.raises(SavedDeliveryError, match="BINDING_DRIFT"):
        open_saved_product(product.receipt.root_path, **{
            **kwargs, "expected_saved_manifest_sha256": "0" * 64})
    with pytest.raises(DurableEmpiricalClosureError):
        open_saved_product(product.receipt.root_path, **{
            **kwargs, "expected_root": "0" * 64})
    # Revoke independently at the resolver boundary, not by modifying a receipt.
    revoked = TestOnlyDecisionResolver(replace(issue.issued.record, currentness="REVOKED"))
    with pytest.raises(WorkloadAdmissionError):
        open_saved_product(product.receipt.root_path, **{**kwargs, "resolver": revoked})
    manifest_path = Path(product.receipt.root_path) / "manifest.json"
    raw = manifest_path.read_bytes()
    manifest_path.write_bytes(b"{}")
    with pytest.raises(DurableEmpiricalClosureError):
        open_saved_product(product.receipt.root_path, **kwargs)
    manifest_path.write_bytes(raw)
    restored = open_saved_product(product.receipt.root_path, **kwargs)
    assert restored.read_s04(workload.requests[0].query_ref).first_consumer.knowledge.ref == (
        reads[0].first_consumer.knowledge.ref)
    print("SAVED_DELIVERY", product.execution_seconds, product.publication_seconds,
          product.receipt.root_identity, product.batch_census["unit_count"])


def test_v1_requires_actual_discovery_before_open(tmp_path):
    _, _, _, v1, _, _ = s1e._full(tmp_path / "source")
    issue = _issue_compiled_governed_queries_v2(v1)
    # A caller cannot simply remove a discovery from its governed descriptor.
    forged = replace(issue.issued.workload, discoveries=())
    with pytest.raises(WorkloadAdmissionError):
        execute_publish_saved(
            forged, TestOnlyDecisionResolver(issue.issued.record),
            host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
            saved_admission_factory=lambda: pytest.fail("source opened before admission"),
            root_dir=tmp_path / "never",
        )
    assert not (tmp_path / "never").exists()


def _joint_fixture(root, source_format):
    """Generated actual two-item source, not separately manufactured joint facts."""
    from copy import deepcopy
    import pandas as pd
    import pyreadstat
    from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture
    from rawlsing_next.tests.test_pyat940_s1b_support import sha256_file, sha256_text
    from rawlsing_next.tests.test_pyat960_s1e_native_fact import _native_document
    from rawlsing_next.tests.test_universal_grammar import _occurrence, _frontier
    from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import _freeze_packet
    from rawlsing_next.pre553_r157_projection_adapter import SourceConfig, build_governed_c11_projection
    from rawlsing_next.pre553_empirical_objects import exact_ref
    values = (0., 0., 1., 1., 1.)
    other = (0., 1., 0., 1., 1.)
    fx = source_fixture(root, source_format=source_format, values=values,
                        policy_kwargs={"j": 2, "k": 1, "d": 0})
    frame = pd.DataFrame({"q101": values, "country": [1.]*5, "q102": other})
    writer = pyreadstat.write_sav if source_format == "SAV" else pyreadstat.write_dta
    writer(frame, str(fx["path"]), variable_value_labels={
        "q101": {1.: "one", 7.: "DK"}, "q102": {1.: "one", 7.: "DK"}})
    source_sha = sha256_file(fx["path"])
    doc = _native_document(fx["document"])

    def clone(value):
        if isinstance(value, str):
            return value.replace("q101", "q102")
        if isinstance(value, list):
            return [clone(x) for x in value]
        if isinstance(value, dict):
            result = {k: clone(v) for k, v in value.items()}
            if "object_id" in value and result["object_id"] != value["object_id"]:
                result["content_hash"] = sha256_text(
                    result["kind"] + ":" + result["object_id"])
            return result
        return value

    for field in ("questions", "items", "response_slots", "routing"):
        doc[field].append(clone(doc[field][0]))
    doc["items"][1]["exact_identity_sha256"] = sha256_text("item:q102")
    doc["response_slots"][1]["slot"]["ordinal"] = 3
    # Both targets have the same observed full-risk membership, explicitly.
    doc["routing"][1]["risk_set_ref"] = deepcopy(doc["routing"][0]["risk_set_ref"])
    doc["routing"][1]["member_set_replay_ref"] = deepcopy(doc["routing"][0]["member_set_replay_ref"])
    slot = clone(doc["physical_slots"][0])
    slot["ordinal"] = 3
    doc["physical_slots"].append(slot)
    doc["identity"].update(source_column_count=3, codebook_rows=3, original_item_count=2)
    doc["binding"]["source_sha256"] = source_sha
    doc["binding"]["source_snapshot_ref"]["content_hash"] = source_sha
    doc["supported_scope"]["supported_question_ids"].append("q102")
    doc["coverage"].update(physical_slots_total=3, items_total=2)
    config = SourceConfig(doc)
    projection = build_governed_c11_projection(config)
    risk = exact_ref(projection.routing[0].risk_set_ref)
    inventory = replace(
        fx["inventory"], source_sha256=source_sha,
        occurrences=tuple(replace(_occurrence(k), risk_set_refs=(risk.key,))
                          for k in ("q101", "q102")),
        risk_set_refs=(risk.key,),
    )
    frontier = _frontier(inventory, fx["policy"])
    fx.update(document=doc, config=config, projection=projection,
              source_sha=source_sha, inventory=inventory, frontier=frontier,
              census=_freeze_packet(frontier))
    return s1e._fixed_fixture(fx)


@pytest.mark.parametrize("source_format", ["SAV", "DTA"])
def test_generated_joint_source_to_persistent_ff01(tmp_path, monkeypatch, source_format):
    from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
    from rawlsing_next.pre553_saved_c11_admission import SavedReleaseIdentity
    from rawlsing_next.pre553_universal_workload import compile_governed_frontier
    from rawlsing_next.pre553_source_native_preimage_adapter import AdministeredItem
    from rawlsing_next.tests.test_pyat960_s1e_native_fact import _NATIVE_AS_OF
    from rawlsing_next.pre553_empirical_objects import exact_ref
    from rawlsing_next.pre553_s04_general_joint_algebra import S04Projection
    from rawlsing_next.field_forge_generic_empirical_ingress import receive_ff01_observed_joint

    fx = _joint_fixture(tmp_path / "fixture", source_format)
    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    sink = SourceSavedBodySink(certificate_path=tmp_path / "q2.sqlite",
                               authorized_private_root=private, chunk_rows=2)
    ingestion_start = monotonic()
    handoff = s1e.build(tmp_path, fx, name="q2.sqlite", body_sink=sink, chunk_size=2)
    ingestion_seconds = monotonic() - ingestion_start
    estate = sink.receipt
    projection = fx["projection"]
    bundle = s1e._native_bundle(handoff, fx, projection,
                               SavedReleaseIdentity(estate.reconstructed_v1_release_ref))
    qrefs = {q.native_question_ref.object_id.split(":")[-1]: q.native_question_ref
             for q in projection.questions}
    assert set(qrefs) == {"q101", "q102"}
    bundle = replace(bundle,
        administered=tuple(AdministeredItem("Q2-BODY-"+k, k, "ADMINISTERED",
                    "TEST_ONLY_TWO_ITEM_SOURCE", "person", "OUTCOME") for k in qrefs),
        question_refs=qrefs)
    v1 = compile_governed_frontier(
        bundle=bundle, inventory=fx["inventory"], policy=fx["policy"],
        frontier=fx["frontier"], as_of=_NATIVE_AS_OF,
        host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE)
    issue = _issue_compiled_governed_queries_v2(v1)
    workload = issue.issued.workload
    resolver = TestOnlyDecisionResolver(issue.issued.record)
    def factory():
        return SavedC11Admission.open(
            root=private, exact_path=estate.path,
            independently_held_manifest_sha256=estate.manifest_sha256,
            independently_held_i02=estate.i02,
            release_ref=estate.reconstructed_v1_release_ref,
            runtime_catalog=workload.catalog, current_authorizer=lambda _: True)
    result = execute_publish_saved(
        workload, resolver, host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
        saved_admission_factory=factory, root_dir=tmp_path / "products")
    assert handoff.stats.source_reads == 1
    assert sink.stats["source_decodes_by_sink"] == 0
    shutil.rmtree(estate.path)
    fx["path"].unlink()
    def forbidden(*a, **kw):
        pytest.fail("cold retrieval attempted native computation")
    monkeypatch.setattr(SavedC11Admission, "open", forbidden)
    monkeypatch.setattr(DirectEstateI03Session, "_build", forbidden)
    cold_start = monotonic()
    cold = open_saved_product(
        result.receipt.root_path, expected_root=result.receipt.root_identity,
        expected_release_ref=estate.reconstructed_v1_release_ref,
        expected_saved_manifest_sha256=estate.manifest_sha256, workload=workload,
        resolver=resolver, host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE)
    cold_open_seconds = monotonic() - cold_start
    supported = []
    for req in workload.requests:
        query = workload.catalog.resolve_query_exact(req.query_ref)
        if {exact_ref(r) for r in query.target_refs} != set(qrefs.values()):
            continue
        read = cold.read_s04(query.ref)
        if read.first_consumer.knowledge.material()["state"] == "SUPPORTED_SAMPLE_DESCRIPTIVE":
            supported.append(query)
    assert supported, "the actual two-item governed source never issued a supported joint"
    query = supported[0]
    ff_start = monotonic()
    read = cold.read_s04(query.ref, conditioner_index=0)
    ff_seconds = monotonic() - ff_start
    ff = read.first_consumer.ff01
    assert ff is not None
    assert ff.semantic_projection()["raw_fully_resolved_joint_n"] == 5
    from rawlsing_next.pre553_empirical_objects import canonical_json
    rows = ff.semantic_projection()["complete_cells"]
    cells = {canonical_json(row["cell"]): row["raw_support"] for row in rows}
    assert len(cells) == len(rows)
    # The profile explicitly includes zero-support special-state cells.
    assert sorted(n for n in cells.values() if n > 0) == [1, 1, 1, 2]
    assert sum(cells.values()) == 5
    assert all(n >= 0 for n in cells.values())
    assert ff.ref == receive_ff01_observed_joint(
        query=query, execution=read.first_consumer.execution, conditioner_index=0,
        producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",)).ref
    assert cold.read_s04(query.ref, conditioner_index=0) is read
    ws = cold.joint_workspace(query.ref)
    projection_result = ws.query(S04Projection((0,1), {}))
    assert projection_result.material()["raw_selected_full_case_n"] == 5
    assert ws.query_by_refs(tuple(exact_ref(r) for r in query.target_refs), {}).ref == projection_result.ref
    from rawlsing_next.pre553_s04_dhikr_comparative import DHIKRComparisonRequest
    comparison = ws.compare_dhikr(DHIKRComparisonRequest(
        1, (0,), max_depth=0, include_group_evidence=True))
    assert comparison.material()["nodes"][0]["raw_same_case_n"] == 5
    # Real archived discovery evidence, not an independently invented M1 bundle.
    from rawlsing_next.pre553_durable_empirical_closure import open_empirical_closure
    from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import (
        _binding, _m1_authority, _registry,
    )
    from rawlsing_next.tests.test_pre553_learned_world_composition import _contract
    closure = open_empirical_closure(result.receipt.root_path,
                                    expected_root=result.receipt.root_identity).require_trusted()
    discovery = closure.i05_result
    candidates = [r for r in discovery.receipts
                  if r.typed_state == "DISCOVERED_RESULT_SUPPORTED"]
    assert candidates, "no supported original discovery receipt"
    selected = candidates[0]
    authority = _m1_authority("commission-b-generated-" + source_format)
    binding = _binding(authority)
    ingress = _contract(route="M01_M1_M2_B5", binding=binding,
                        tag="commission-b-generated-" + source_format)
    bundle, disposition = cold.adjudicate_m1(
        contract=ingress, family_rule_binding=binding,
        selected_discovery_receipt_refs=(selected.ref,),
        requested_scope={"fixture": "GENERATED_SOURCEFREE_SAVED_PIPELINE"},
        validator_registry=_registry(binding),
        additional_authority_snapshots=(authority,),
    )
    assert selected.ref in disposition.discovery_result_receipt_refs
    assert {f.ref for f in bundle.empirical_facts}.issubset(
        {f.ref for f in closure.object_graph.empirical_facts})
    assert closure.exact_ref in bundle.additional_dependency_refs
    assert exact_ref(disposition.determinant_explanation_receipt.input_bundle_ref) == bundle.ref
    print("SAVED_M1", source_format, disposition.adjudication_outcome, selected.ref.key,
          canonical_json(selected.candidate_identity))
    print("SAVED_JOINT_FF01", source_format, result.batch_census["unit_count"],
          result.execution_seconds, result.publication_seconds,
          result.receipt.referenced_physical_bytes, ff.ref.key)

    print("SAVED_PIPELINE_COST", source_format, "ingest", ingestion_seconds,
          "native", result.execution_seconds, "s2f", result.publication_seconds,
          "cold_open", cold_open_seconds, "ff01", ff_seconds,
          "s2f_referenced_bytes", result.receipt.referenced_physical_bytes)
    _learned_vertical(cold, closure, tmp_path, source_format)


def _learned_vertical(cold, closure, tmp_path, source_format):
    """Actual saved-source I05 -> M1/M2/B5 -> cold S2-G consumer.
    
    Only the consumer request, comparator and validator are synthetic
    authorities; every empirical object comes from the physical source above.
    """
    from rawlsing_next.pre553_analytical_composition import (
        _actual_leaves, _validate_discovery_consumption,
        compose_positioned_subject_possibility,
    )
    from rawlsing_next.pre553_durable_learned_lifecycle import (
        LearnedConsumerDeterminants, DurableLearnedLifecycleError,
        DurableLearnedLifecycleRefusal, DurableLearnedLifecycleUntrusted,
        open_learned_lifecycle,
    )
    from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
    from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref, semantic_hash
    from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleExecutor
    from rawlsing_next.pre553_learned_product_release import M2Repository
    from rawlsing_next.tests import c1_at08_at13_fixture as fx
    from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import (
        _binding, _m1_authority, _registry,
    )
    from rawlsing_next.tests.test_pre553_learned_world_composition import _contract
    from rawlsing_next.tests.test_pyat960_s2g_durable_lifecycle import _attestation
    from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import _validator

    discovery = closure.i05_result
    tag = "commission-b-saved-learned-" + source_format
    release = closure.release_identities[0].release_ref
    predicates = {p.ref: p for p in discovery.executed_predicates}
    queries = {q.ref: q for q in discovery.executed_queries}
    chosen = None
    for receipt in discovery.receipts:
        if (receipt.typed_state != "DISCOVERED_RESULT_SUPPORTED"
                or receipt.candidate_identity.get("family") != "BRANCH_CONDITIONED_DISTRIBUTION"):
            continue
        predicate = predicates[exact_ref(receipt.winning_predicate_ref)]
        leaves = _actual_leaves(predicate)
        roles = [r for r in receipt.candidate_identity["query_roles"]
                 if r["role"] == "CONDITION" and exact_ref(r["predicate_ref"]) == predicate.ref]
        if len(leaves) == 1 and len(roles) == 1:
            leaf = leaves[0]
            if leaf["leaf_type"] != "SURVEY_RESPONSE_EVENT":
                continue
            query = queries[exact_ref(roles[0]["query_ref"])]
            if len(query.target_refs) == len(query.empirical_universe_refs) == 1:
                chosen = receipt, query, predicate, leaf
                break
    assert chosen is not None, "no actual supported value-conditioned discovery"
    receipt, query, predicate, leaf = chosen
    coord = exact_ref(leaf["question_semantic_ref"])
    value = leaf["exact_value"]
    universe = exact_ref(query.empirical_universe_refs[0])
    target = exact_ref(query.target_refs[0])
    pairing = fx.make_pairing_authority(tag)
    conditioner = fx.make_conditioner_binding(
        binding_id="condition", subject_fact_ref=ExactRef(**fx.subject_fact_ref(
            {"qrefs": {"condition": coord}}, "condition", value)),
        empirical_coordinate_ref=coord, comparability_authority_ref=pairing,
        source_universe_ref=universe, release_ref=release)
    consumer = fx.make_multi_conditioner_consumer_query(
        query_id=tag, subject_ref=ExactRef("TEST_ONLY_SUBJECT", "urn:test:" + tag,
                                           semantic_hash({"tag": tag})),
        target_ref=target, source_universe_ref=universe, release_ref=release,
        bindings=[conditioner], projection_kind="TEST_ONLY_SAVED_LEARNED")
    fact, pred, actual_query = _validate_discovery_consumption(
        discovery_result=discovery, consumer_query=consumer, receipt_ref=receipt.ref)
    assert actual_query.ref == query.ref and pred.ref == predicate.ref
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:" + tag + ":witness",
        consumer_query=consumer, producer_query=query, producer_predicate=predicate,
        bindings=[conditioner], coordinate_value_pairs=[(coord, value)],
        pairing_authority=pairing, source_universe_ref=universe, release_ref=release)
    model = fx.make_model_rule(universe, tag)
    composition = compose_positioned_subject_possibility(
        repository=None, empirical_query=query, predicate=predicate,
        authority_registry=AuthorityRegistry(closure.object_graph.authority_snapshots),
        release_refs=(release,), consumer_query=consumer, model_rule=model,
        condition_binding_witness=witness, discovery_result=discovery,
        discovery_receipt_ref=receipt.ref)
    assert composition.consumer_result_or_null is not None
    assert composition.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    # Independent physical five-row oracle: both columns have two zeroes
    # and three ones; the conditioned joint fibre is (1,1) or (1,2).
    assert float(value) in (0., 1.)
    expected_counts = [1, 1] if float(value) == 0. else [1, 2]
    assert fact.raw_denominator_support == sum(expected_counts)
    assert sorted(cell["raw_numerator_support"] for cell in
                  composition.consumer_result_or_null.exact_geometry["cells"]
                  if cell["raw_numerator_support"] > 0) == expected_counts
    authority = _m1_authority(tag)
    binding = _binding(authority)
    ingress = _contract(route="M01_M1_M2_B5", binding=binding, tag=tag)
    contract = _contract(route="M1_M2_B5", binding=binding, tag=tag,
                         actions=("REGISTER", "PUBLISH", "SELECT_CURRENT"))
    determinants = LearnedConsumerDeterminants(
        s2f_root_identity=closure.root_identity, discovery_receipt_ref=receipt.ref,
        producer_query_ref=query.ref, producer_predicate_ref=predicate.ref,
        release_ref=release, consumer_query=consumer, model_rule=model,
        condition_binding_witness=witness,
        expected_composition_identity=composition.composed_result_identity_hash,
        expected_consumer_result_hash=composition.consumer_result_or_null.result_hash,
        purpose_ref=contract.consumer_product_purpose_ref)
    args = dict(ingress_contract=ingress, product_contract=contract,
                family_rule_binding=binding, requested_scope={"fixture": tag},
                validator_registry=_registry(binding),
                additional_authority_snapshots=(authority,))
    executor = LearnedProductLifecycleExecutor()
    repository = M2Repository()
    initial_checkpoint = executor.export_checkpoint()
    def assert_unchanged(root):
        assert executor.export_checkpoint() == initial_checkpoint, (
            "INVALID_CONSUMER_MUTATED_B5_BEFORE_COLD_VALIDATION")
        assert all(not getattr(repository, name) for name in repository._store_names), (
            "INVALID_CONSUMER_MUTATED_M2_BEFORE_COLD_VALIDATION")
        assert not root.exists(), "INVALID_CONSUMER_PUBLISHED_ARTIFACT"

    for field in ("expected_composition_identity", "expected_consumer_result_hash"):
        invalid_root = tmp_path / ("invalid-" + field)
        with pytest.raises((SavedDeliveryError, DurableLearnedLifecycleError)):
            cold.publish_learned(**args, m2_repository=repository,
                lifecycle_executor=executor, root_dir=invalid_root,
                determinants=replace(determinants, **{field: "0"*64}))
        assert_unchanged(invalid_root)

    # An adversary can readdress the consumer and witness consistently:
    # merely checking the resulting composition hash cannot prove target identity.
    # Predecessor #1306 executed the wrong-target false acceptance. Now
    # C1 itself must refuse; S2-G independently refuses before mutation.
    wrong_target = ExactRef("TEST_ONLY_FOREIGN_TARGET", "urn:test:" + tag + ":foreign",
                            semantic_hash({"foreign": tag}))
    wrong_consumer = replace(consumer, target_ref=wrong_target)
    wrong_witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:" + tag + ":wrong-target",
        consumer_query=wrong_consumer, producer_query=query, producer_predicate=predicate,
        bindings=[conditioner], coordinate_value_pairs=[(coord, value)],
        pairing_authority=pairing, source_universe_ref=universe, release_ref=release)
    from rawlsing_next.pre553_analytical_composition import AnalyticalCompositionError
    with pytest.raises(AnalyticalCompositionError, match="TARGET_TOPOLOGY_OR_DOMAIN_MISMATCH"):
        compose_positioned_subject_possibility(
            repository=None, empirical_query=query, predicate=predicate,
            authority_registry=AuthorityRegistry(closure.object_graph.authority_snapshots),
            release_refs=(release,), consumer_query=wrong_consumer, model_rule=model,
            condition_binding_witness=wrong_witness, discovery_result=discovery,
            discovery_receipt_ref=receipt.ref)
    invalid_root = tmp_path / "wrong-target"
    with pytest.raises(DurableLearnedLifecycleError, match="unary target differs"):
        cold.publish_learned(**args, m2_repository=repository,
            lifecycle_executor=executor, root_dir=invalid_root,
            determinants=replace(determinants, consumer_query=wrong_consumer,
                condition_binding_witness=wrong_witness))
    assert_unchanged(invalid_root)
    print("SAVED_WRONG_TARGET_REFUSED", source_format, target.key, wrong_target.key)

    invalid_root = tmp_path / "negative-rule"
    negative = _registry(binding, _validator(outcome="RULE_NOT_SATISFIED"))
    _, negative_disposition = cold.adjudicate_m1(
        contract=ingress, family_rule_binding=binding,
        selected_discovery_receipt_refs=(receipt.ref,), requested_scope={"fixture": tag},
        validator_registry=negative, additional_authority_snapshots=(authority,))
    assert negative_disposition.adjudication_outcome == "RULE_NOT_SATISFIED"
    with pytest.raises(SavedDeliveryError, match="LEARNED_NONPRODUCTIVE_M1:RULE_NOT_SATISFIED"):
        cold.publish_learned(**{**args, "validator_registry": negative},
            m2_repository=repository, lifecycle_executor=executor, root_dir=invalid_root,
            determinants=determinants)
    assert_unchanged(invalid_root)

    # Corrupt after empirical admission but before learned publication. Refuse
    # before touching the external lifecycle, not after writing an artifact.
    invalid_root = tmp_path / "corrupt-archive"
    manifest = closure.root_path / "manifest.json"
    original = manifest.read_bytes()
    manifest.write_bytes(b"{}")
    try:
        with pytest.raises(DurableEmpiricalClosureError):
            cold.publish_learned(**args, m2_repository=repository,
                lifecycle_executor=executor, root_dir=invalid_root,
                determinants=determinants)
        assert_unchanged(invalid_root)
    finally:
        manifest.write_bytes(original)

    learned_start = monotonic()
    learned, consumed = cold.publish_learned(
        **args, m2_repository=repository, lifecycle_executor=executor,
        root_dir=tmp_path / "learned", determinants=determinants)
    learned_seconds = monotonic() - learned_start
    assert consumed.state == "LEARNED_CONSUMER_EXACT_SUPPORTED", consumed.reason_code
    assert consumed.consumer_result_hash == composition.consumer_result_or_null.result_hash
    retrieved = cold.read_learned(learned.artifact_path,
        expected_root=learned.root_identity, expected_purpose_ref=determinants.purpose_ref)
    assert retrieved.consumer_result_hash == consumed.consumer_result_hash
    artifact = open_learned_lifecycle(learned.artifact_path,
        expected_root=learned.root_identity).require_trusted()
    assert artifact.m1_disposition.ref == consumed.m1_disposition_ref
    assert receipt.ref in artifact.m1_disposition.discovery_result_receipt_refs
    assert fact.ref in artifact.m1_disposition.empirical_fact_refs

    # Historical selected state does not constitute live learned authority.
    # Exercise the real S2-G current attestation owner separately.
    good = _attestation(artifact)
    serve = dict(expected_root=learned.root_identity,
                 expected_purpose_ref=determinants.purpose_ref)
    view, current = cold.read_current_learned(learned.artifact_path, **serve,
        attestation=good, expected_attestation_root=good.content_root)
    assert view.state == "CURRENT_SELECTED"
    assert current.consumer_result_hash == consumed.consumer_result_hash
    with pytest.raises(DurableLearnedLifecycleUntrusted):
        cold.read_current_learned(learned.artifact_path, **serve,
            attestation=good, expected_attestation_root=None)
    revoked = _attestation(artifact, revoked=True)
    with pytest.raises(DurableLearnedLifecycleRefusal):
        cold.read_current_learned(learned.artifact_path, **serve,
            attestation=revoked, expected_attestation_root=revoked.content_root)
    with pytest.raises(SavedDeliveryError, match="PURPOSE_BINDING_DRIFT"):
        cold.read_learned(learned.artifact_path,
            expected_root=learned.root_identity, expected_purpose_ref=consumer.ref)
    assert cold.read_learned(learned.artifact_path, **serve).consumer_result_hash == (
        consumed.consumer_result_hash)

    # A legitimate historical product need not be selected CURRENT.
    historical_contract = _contract(route="M1_M2_B5", binding=binding, tag=tag,
                                     actions=("REGISTER", "PUBLISH"))
    historical, h_result = cold.publish_learned(
        **{**args, "product_contract": historical_contract},
        m2_repository=M2Repository(), lifecycle_executor=LearnedProductLifecycleExecutor(),
        root_dir=tmp_path / "historical-learned", determinants=determinants,
        require_current_selection=False)
    assert historical.selection_receipt_ref is None
    assert h_result.consumer_result_hash == consumed.consumer_result_hash
    archived = dict(expected_root=historical.root_identity,
                    expected_purpose_ref=determinants.purpose_ref)
    assert cold.read_learned(historical.artifact_path, **archived).state == "REFUSED"
    assert cold.read_learned(historical.artifact_path, **archived,
        require_current_selection=False).consumer_result_hash == consumed.consumer_result_hash

    # Reuse the incumbent fresh-process reader against THIS actual saved
    # pipeline's artifact, with no generated survey or C11 available.
    import json
    import os
    import subprocess
    import sys
    runner = Path(__file__).with_name("test_pyat960_s2g_fresh_process.py")
    env = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[2]),
               PYTHONDONTWRITEBYTECODE="1")
    child = subprocess.run(
        [sys.executable, str(runner), learned.artifact_path, learned.root_identity,
         str(closure.root_path), consumed.consumer_result_hash],
        cwd=tmp_path, env=env, capture_output=True, text=True, timeout=120)
    assert child.returncode == 0, child.stderr
    observed = json.loads(child.stdout)
    assert observed["state"] == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert observed["matches_expected"] and observed["source_opens"] == []
    assert observed["consumer_result_hash"] == consumed.consumer_result_hash
    print("SAVED_S2G", source_format, consumed.state, consumed.consumer_result_hash,
          learned.root_identity, learned.compressed_bytes,
          "publish_and_validate_seconds", learned_seconds,
          "fresh_cold_seconds", observed["elapsed_seconds"],
          "fresh_peak_rss_bytes", observed["process_tree_peak_rss_bytes"])
