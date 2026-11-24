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
