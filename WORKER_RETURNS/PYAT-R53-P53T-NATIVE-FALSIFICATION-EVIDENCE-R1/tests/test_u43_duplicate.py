from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
U43 = HERE / "_pinned/u43/pre553_issued_workload.py"
EXPECTED_SHA256 = "8a420647ec32e1e6935e2b359c0c6e3cab1f802be59c3861a8ba2393b3351ac6"


def load_u43():
    spec = importlib.util.spec_from_file_location("p53t_u43", U43)
    module = importlib.util.module_from_spec(spec)
    sys.modules["p53t_u43"] = module
    spec.loader.exec_module(module)
    return module


def fixture(module):
    ref = module.ExactRef
    source_ref = ref("Source", "urn:test:src", "a" * 64)
    decision_ref = ref("Decision", "urn:test:dec", "b" * 64)
    discovery_ref = ref("DiscoveryAuthority", "urn:test:disc", "c" * 64)
    release_ref = ref("C11LogicalRelease", "urn:test:rel", "d" * 64)
    replay_ref = ref("ReplayManifest", "urn:test:rep", "e" * 64)
    record = SimpleNamespace(
        source_sha256="a" * 64, envelope_sha256="f" * 64,
        decision_ref=decision_ref, original_wave_identity=None, scope="TEST_ONLY")
    release = SimpleNamespace(
        release_ref=release_ref,
        replay_manifest=SimpleNamespace(ref=replay_ref))
    workload = SimpleNamespace(
        source_factory_ref=source_ref, projection=object(), catalog=object(),
        requests=(), discoveries=(discovery_ref,), decision_ref=decision_ref,
        envelope=lambda: {})
    return source_ref, decision_ref, discovery_ref, release_ref, replay_ref, record, release, workload


def install(module, monkeypatch, calls, record, release, source_ref):
    monkeypatch.setattr(module, "admit", lambda *a, **k: record)

    def route_b(**kwargs):
        calls.append(("ROUTE_B_SURFACE", kwargs["discovery_authority_ref"].key))
        return SimpleNamespace()

    monkeypatch.setattr(module, "execute_route_b_production", route_b)
    monkeypatch.setattr(
        module, "build_source_backed_c11_repository",
        lambda *a, **k: (object(), release))

    class Executor:
        def __init__(self, *a, **k):
            pass

        def execute_i03(self, **kwargs):
            return SimpleNamespace(facts=(SimpleNamespace(ref=source_ref),))

        def execute_i05(self, **kwargs):
            calls.append(("BATCH_SURFACE", kwargs["discovery_authority_ref"].key))
            return SimpleNamespace(receipts=(SimpleNamespace(ref=source_ref),))

    class Runner:
        def __init__(self, *, manifest, repository, prior_receipts=()):
            self.manifest = manifest
            self.receipts = []

        def run(self, executors, max_units=None):
            for unit in self.manifest.units:
                outcome = executors[unit.job_kind].execute(unit)
                self.receipts.append(SimpleNamespace(
                    state="COMPLETED", result_refs=outcome.result_refs))

        def summary(self):
            return {"units": len(self.manifest.units)}

    monkeypatch.setattr(module, "CarrierNeutralResearchExecutor", Executor)
    monkeypatch.setattr(module, "BatchExecutionRunner", Runner)


def test_u43_pinned_source_identity():
    data = U43.read_bytes()
    assert hashlib.sha256(data).hexdigest() == EXPECTED_SHA256
    assert "execute_issued_workload" in data.decode()


def test_u43_discovery_surface_is_entered_by_route_b_and_batch(monkeypatch):
    module = load_u43()
    source_ref, decision_ref, discovery_ref, release_ref, replay_ref, record, release, workload = \
        fixture(module)
    calls = []
    install(module, monkeypatch, calls, record, release, source_ref)
    result = module.execute_issued_workload(
        workload, SimpleNamespace(),
        source_factory=lambda ref: SimpleNamespace(source_sha256="a" * 64),
        host="test-host", purpose="test-purpose", allow_test_only=True)
    assert calls == [
        ("ROUTE_B_SURFACE", discovery_ref.key),
        ("BATCH_SURFACE", discovery_ref.key),
    ]
    assert len(result.receipts) == 1
    assert result.decision_ref == decision_ref
    assert result.envelope_sha256 == "f" * 64


def test_u43_prior_receipts_are_refused_before_batch(monkeypatch):
    module = load_u43()
    source_ref, decision_ref, discovery_ref, release_ref, replay_ref, record, release, workload = \
        fixture(module)
    calls = []
    install(module, monkeypatch, calls, record, release, source_ref)
    try:
        module.execute_issued_workload(
            workload, SimpleNamespace(),
            source_factory=lambda ref: SimpleNamespace(source_sha256="a" * 64),
            host="test-host", purpose="test-purpose", allow_test_only=True,
            prior_receipts=(object(),))
    except module.WorkloadAdmissionError as error:
        assert str(error) == "RESTORE_THROUGH_EXISTING_ISSUED_FACT_RECEIPT_CUSTODY_REQUIRED"
    else:
        raise AssertionError("prior receipt ingress was not refused")
    assert calls == []
