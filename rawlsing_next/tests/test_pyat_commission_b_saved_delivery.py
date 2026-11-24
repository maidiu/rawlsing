"""Actual generated SAV -> saved C11 -> issued Batch -> S2-F -> cold S04."""
from dataclasses import replace
from pathlib import Path
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
    handoff = s1e.build(tmp_path, fx, name="q2.sqlite", body_sink=sink, chunk_size=2)
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
    cold = open_saved_product(
        result.receipt.root_path, expected_root=result.receipt.root_identity,
        expected_release_ref=estate.reconstructed_v1_release_ref,
        expected_saved_manifest_sha256=estate.manifest_sha256, workload=workload,
        resolver=resolver, host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE)
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
    read = cold.read_s04(query.ref, conditioner_index=0)
    ff = read.first_consumer.ff01
    assert ff is not None
    assert ff.semantic_projection()["raw_fully_resolved_joint_n"] == 5
    cells = {tuple(row["cell"]): row["raw_support"]
             for row in ff.semantic_projection()["complete_cells"]}
    assert sorted(cells.values()) == [1, 1, 1, 2]
    assert ff.ref == receive_ff01_observed_joint(
        query=query, execution=read.first_consumer.execution, conditioner_index=0,
        producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",)).ref
    assert cold.read_s04(query.ref, conditioner_index=0) is read
    ws = cold.joint_workspace(query.ref)
    projection_result = ws.query(S04Projection((0,1), {}))
    assert projection_result.material()["raw_selected_full_case_n"] == 5
    print("SAVED_JOINT_FF01", source_format, result.batch_census["unit_count"],
          result.execution_seconds, result.publication_seconds,
          result.receipt.referenced_physical_bytes, ff.ref.key)
