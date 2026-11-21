"""S2-D five remaining readers on one accepted saved estate.

The fixture is the existing S1-D sourcefree S3 bundle.  The same bundle's
projection is projected into the accepted S2-C Parquet estate, so the saved
consumer and the legacy oracle consume the same exact source, release and
native query/discovery objects.
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

pytest.importorskip("pyarrow")

import rawlsing_next.pre553_issued_workload as issued_module
import rawlsing_next.tests.test_pre553_direct_estate_i03 as s2c
from rawlsing_next._pre553_direct_i02_sourcefree import direct_sections_from_candidate
from rawlsing_next.pre553_c11_ingest import build_candidate_replay_manifest
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_issued_workload import (
    _checkpoint_content_hash,
    material,
    capture_joined_checkpoint,
    execute_issued_workload,
    restore_joined_checkpoint,
    resume_joined_workloads,
)
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_batch,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_source_backed_c11_repository,
    project_c11_candidate_from_physical_cells,
)
from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import (
    AS_OF,
    HOST,
    PURPOSE,
    CurrentIssuer,
    _build_multi_unit_issued,
    _count_builds,
    _counted_source,
)
from rawlsing_next.tests.test_universal_source_projection import (
    build_s3,
    load_s3,
    s3_rows,
)


def _saved_estate(tmp_path, bundle):
    """Build the accepted S2-C estate from the same S1-D source bundle."""
    candidate = project_c11_candidate_from_physical_cells(
        source_sha256=bundle.source_sha256,
        row_count=bundle.physical_stream.row_count,
        cells=bundle.physical_stream.iter_cells(),
        projection=bundle.projection,
    )
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=bundle.projection.replay_authority_ref,
        deterministic_tie_order_rules_ref=bundle.projection.tie_order_ref,
        replay_protocol_version=bundle.projection.replay_protocol_version,
    )
    candidate = replace(candidate, candidate_replay_manifest=replay)
    sections = direct_sections_from_candidate(
        candidate,
        replay_protocol_authority_ref=bundle.projection.replay_authority_ref,
        replay_protocol_version=bundle.projection.replay_protocol_version,
        deterministic_tie_order_rules_ref=bundle.projection.tie_order_ref,
    )
    root = tmp_path / "saved-estate"
    root.mkdir(mode=0o700)
    receipt = write_direct_estate(
        sections, bundle.projection.universes[0].ref, root, chunk_rows=2,
    )
    assert receipt.reconstructed_v1_release_ref == bundle.release.release_ref
    return root, receipt


def _admission_for(root, receipt, workload, current_authorizer):
    return SavedC11Admission.open(
        root=root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        release_ref=receipt.reconstructed_v1_release_ref,
        runtime_catalog=workload.catalog,
        current_authorizer=current_authorizer,
    )


def _release_from_receipt(receipt):
    return receipt.reconstructed_v1_release_ref


def _fixture(tmp_path):
    path = tmp_path / "source.sav"
    oracle_bundle = build_s3(path, s3_rows(respondents=4, occasions=2))
    saved_bundle = load_s3(path)
    issued = _build_multi_unit_issued(oracle_bundle)
    root, receipt = _saved_estate(tmp_path, saved_bundle)
    issuer = CurrentIssuer((issued.record,))
    return path, oracle_bundle, saved_bundle, issued, root, receipt, issuer


def test_saved_batch_actual_native_scheduler(tmp_path, monkeypatch):
    _, _, _, issued, root, receipt, issuer = _fixture(tmp_path)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    # Build the manifest exactly as the normal issued path does.
    oracle = execute_issued_workload(
        issued.workload, issuer,
        source_factory=lambda _ref: _fixture_bundle(tmp_path).physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    predicate_by_query = {
        request.query_ref.key: request.predicate_ref
        for request in issued.workload.requests
    }
    runner = execute_saved_batch(
        admission, manifest=oracle.manifest,
        predicate_ref_by_query=predicate_by_query,
        prior_receipts=(),
    )
    assert len(runner.receipts) == len(oracle.receipts)
    assert {r.state for r in runner.receipts} == {"COMPLETED"}
    assert tuple(sorted(ref.key for r in runner.receipts for ref in r.result_refs)) == tuple(
        sorted(ref.key for r in oracle.receipts for ref in r.result_refs)
    )


def _fixture_bundle(tmp_path):
    path = tmp_path / "source.sav"
    # The source file already exists; load the exact same projection.
    return load_s3(path)


def test_saved_normal_matches_legacy_native_and_never_opens_source(tmp_path, monkeypatch):
    _, oracle_bundle, _, issued, root, receipt, issuer = _fixture(tmp_path)
    oracle = execute_issued_workload(
        issued.workload, issuer,
        source_factory=lambda _ref: oracle_bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    builds = _count_builds(monkeypatch)
    source_calls = {"n": 0}

    def forbidden_source(_ref):
        source_calls["n"] += 1
        raise AssertionError("saved normal path called source factory")

    def admission_factory():
        # The factory must run only after the external CURRENT admission.
        assert issuer.calls > 0
        return _admission_for(
            root, receipt, issued.workload,
            lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
        )

    observed = execute_issued_workload(
        issued.workload, issuer,
        saved_admission_factory=admission_factory,
        source_factory=forbidden_source,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    assert source_calls["n"] == 0
    assert builds["count"] == 0
    assert observed.manifest.manifest_hash == oracle.manifest.manifest_hash
    assert tuple(ref.key for ref in observed.output_refs) == tuple(
        ref.key for ref in oracle.output_refs
    )
    assert tuple(material_receipt(r) for r in observed.receipts) == tuple(
        material_receipt(r) for r in oracle.receipts
    )


def material_receipt(receipt):
    from rawlsing_next.pre553_issued_workload import material
    return material(receipt)


def test_saved_completed_partial_absent_use_existing_resume(tmp_path, monkeypatch):
    _, oracle_bundle, _, issued, root, receipt, issuer = _fixture(tmp_path)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    forbidden_calls = {"n": 0}

    def forbidden_source(_ref):
        forbidden_calls["n"] += 1
        raise AssertionError("saved resume path called source factory")

    full = execute_issued_workload(
        issued.workload, issuer,
        saved_admission_factory=lambda: admission,
        source_factory=forbidden_source,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    partial = execute_issued_workload(
        issued.workload, issuer,
        saved_admission_factory=lambda: admission,
        source_factory=forbidden_source,
        host=HOST, purpose=PURPOSE, allow_test_only=True, max_units=1,
    )
    assert forbidden_calls["n"] == 0
    binding = admission.binding_receipt()
    completed_checkpoint = capture_joined_checkpoint(
        (full,), saved_binding=binding,
    )
    partial_checkpoint = capture_joined_checkpoint(
        (partial,), saved_binding=binding,
    )
    absent_checkpoint = capture_joined_checkpoint((), saved_binding=binding)
    assert completed_checkpoint.entries[0].state == "COMPLETED"
    assert partial_checkpoint.entries[0].state == "PARTIAL"

    completed = resume_joined_workloads(
        workloads=(issued,), resolver=issuer,
        saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE,
        checkpoint=completed_checkpoint,
        expected_checkpoint_ref=completed_checkpoint.checkpoint_hash,
        allow_test_only=True,
    )
    assert completed.completed_results
    assert tuple(sorted(ref.key for ref in completed.output_refs)) == tuple(
        sorted(ref.key for ref in full.output_refs)
    )

    partial_result = resume_joined_workloads(
        workloads=(issued,), resolver=issuer,
        saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE,
        checkpoint=partial_checkpoint,
        expected_checkpoint_ref=partial_checkpoint.checkpoint_hash,
        allow_test_only=True,
    )
    assert partial_result.resumed_results
    assert tuple(sorted(ref.key for ref in partial_result.output_refs)) == tuple(
        sorted(ref.key for ref in full.output_refs)
    )

    absent_result = resume_joined_workloads(
        workloads=(issued,), resolver=issuer,
        saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE,
        checkpoint=absent_checkpoint,
        expected_checkpoint_ref=absent_checkpoint.checkpoint_hash,
        allow_test_only=True,
    )
    assert absent_result.resumed_results
    assert tuple(sorted(ref.key for ref in absent_result.output_refs)) == tuple(
        sorted(ref.key for ref in full.output_refs)
    )


def test_saved_forged_checkpoint_binding_refused_before_restore(tmp_path):
    _, oracle_bundle, _, issued, root, receipt, issuer = _fixture(tmp_path)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    full = execute_issued_workload(
        issued.workload, issuer, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    checkpoint = capture_joined_checkpoint(
        (full,), saved_binding=admission.binding_receipt(),
    )
    forged_binding = replace(
        admission.binding_receipt(), manifest_sha256="0" * 64,
    )
    forged_checkpoint = type(checkpoint)(
        schema=checkpoint.schema,
        entries=checkpoint.entries,
        checkpoint_hash=checkpoint.checkpoint_hash,
        saved_binding=forged_binding,
    )
    forged_checkpoint = replace(
        forged_checkpoint,
        checkpoint_hash=_checkpoint_content_hash(forged_checkpoint),
    )
    with pytest.raises(Exception, match="SAVED_BINDING"):
        resume_joined_workloads(
            workloads=(issued,), resolver=issuer,
            saved_admission_factory=lambda: admission, source_factory=None,
            host=HOST, purpose=PURPOSE, checkpoint=forged_checkpoint,
            expected_checkpoint_ref=forged_checkpoint.checkpoint_hash,
            allow_test_only=True,
        )


def test_saved_normal_revoked_current_refuses_before_admission_factory(
    tmp_path, monkeypatch,
):
    _, _, _, issued, root, receipt, issuer = _fixture(tmp_path)
    factory_calls = {"n": 0}
    source_calls = {"n": 0}

    def factory():
        factory_calls["n"] += 1
        return _admission_for(
            root, receipt, issued.workload,
            lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
        )

    def source(_ref):
        source_calls["n"] += 1
        raise AssertionError("source factory called on revoked saved path")

    issuer.revoke()
    with pytest.raises(Exception, match="CURRENT"):
        execute_issued_workload(
            issued.workload, issuer, saved_admission_factory=factory,
            source_factory=source, host=HOST, purpose=PURPOSE,
            allow_test_only=True,
        )
    assert factory_calls["n"] == 0
    assert source_calls["n"] == 0


def test_saved_resume_refuses_missing_binding_and_source_factory(tmp_path):
    _, _, _, issued, root, receipt, issuer = _fixture(tmp_path)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    checkpoint = capture_joined_checkpoint((), saved_binding=None)
    with pytest.raises(Exception, match="SAVED_CHECKPOINT_BINDING_REQUIRED"):
        resume_joined_workloads(
            workloads=(issued,), resolver=issuer,
            saved_admission_factory=lambda: admission,
            source_factory=None, host=HOST, purpose=PURPOSE,
            checkpoint=checkpoint,
            expected_checkpoint_ref=checkpoint.checkpoint_hash,
            allow_test_only=True,
        )
    binding_checkpoint = capture_joined_checkpoint(
        (), saved_binding=admission.binding_receipt(),
    )
    with pytest.raises(Exception, match="SAVED_CHECKPOINT_REQUIRES_SAVED_ADMISSION"):
        resume_joined_workloads(
            workloads=(issued,), resolver=issuer,
            source_factory=lambda _ref: (_ for _ in ()).throw(AssertionError("source")),
            saved_admission_factory=None, host=HOST, purpose=PURPOSE,
            checkpoint=binding_checkpoint,
            expected_checkpoint_ref=binding_checkpoint.checkpoint_hash,
            allow_test_only=True,
        )


def _fresh_process_capsule(tmp_path, issued, admission, checkpoint=None, mode="normal"):
    workload_material = material(issued.workload)
    workload_material["descriptor_hex"] = workload_material.pop("descriptor").hex()
    capsule = {
        "root": str(admission._estate.root) if False else None,
        "workload": workload_material,
        "record": material(issued.record),
        "release": admission.release_ref.as_dict(),
        "i02": admission.i02.__dict__,
        "checkpoint": None if checkpoint is None else checkpoint.material(),
        "mode": mode,
    }
    # Public property avoids relying on the private estate attribute.
    capsule["root"] = str(admission.estate_path).rsplit("/releases/", 1)[0]
    capsule["exact_path"] = admission.estate_path
    capsule["manifest_sha256"] = admission.manifest_sha256
    capsule_path = tmp_path / "capsule.json"
    capsule_path.write_text(json.dumps(capsule, sort_keys=True), encoding="utf-8")
    child = r"""
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_issued_workload import (
    I03ExecutionRequest, IssuedWorkloadRecord, NativeWorkload,
    execute_issued_workload, restore_joined_checkpoint, resume_joined_workloads,
)
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
c = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
wm = c["workload"]
class CapsuleProjection:
    def __init__(self, document, source_sha):
        self.document = document
        self.expected_source_sha256 = source_sha
        self.release_id = document["release_id"]
    def as_dict(self):
        return self.document
cat_doc = wm["catalog"]
catalog = RuntimeObjectCatalog.from_documents(
    authority_documents=cat_doc["authorities"],
    predicate_documents=cat_doc["predicates"],
    query_documents=cat_doc["queries"],
    discovery_authority_documents=cat_doc["discovery_authorities"],
)
record = IssuedWorkloadRecord(
    decision_ref=exact_ref(c["record"]["decision_ref"]),
    source_permission_ref=exact_ref(c["record"]["source_permission_ref"]),
    scientific_permission_refs=tuple(exact_ref(x) for x in c["record"]["scientific_permission_refs"]),
    host=c["record"]["host"], purpose=c["record"]["purpose"],
    source_sha256=c["record"]["source_sha256"],
    envelope_sha256=c["record"]["envelope_sha256"],
    original_u_root=c["record"]["original_u_root"],
    expected_frontier_root=c["record"]["expected_frontier_root"],
    expected_jobs=tuple(tuple(x) for x in c["record"]["expected_jobs"]),
    currentness=c["record"]["currentness"], scope=c["record"]["scope"],
    original_wave_identity=None,
    native_universe_refs=tuple(),
)
projection = CapsuleProjection(wm["projection"], record.source_sha256)
workload = NativeWorkload(
    decision_ref=exact_ref(wm["decision_ref"]),
    source_factory_ref=exact_ref(wm["source_factory_ref"]),
    descriptor=bytes.fromhex(wm["descriptor_hex"]),
    projection=projection,
    catalog=catalog,
    requests=tuple(I03ExecutionRequest(exact_ref(r["query_ref"]), exact_ref(r["predicate_ref"])) for r in wm["requests"]),
    discoveries=tuple(exact_ref(x) for x in wm["discoveries"]),
    original_u_root=wm["original_u_root"],
    expected_frontier_root=wm["expected_frontier_root"],
    original_wave_identity=None,
)
def admission_factory():
    return SavedC11Admission.open(
        root=c["root"], exact_path=c["exact_path"],
        independently_held_manifest_sha256=c["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**c["i02"]),
        release_ref=exact_ref(c["release"]), runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )
resolver = TestOnlyDecisionResolver(record)
if c["mode"] == "normal":
    result = execute_issued_workload(
        workload, resolver, saved_admission_factory=admission_factory,
        source_factory=None, host=record.host, purpose=record.purpose,
        allow_test_only=True,
    )
    print(json.dumps({"output_refs": [r.as_dict() for r in result.output_refs]}, sort_keys=True))
else:
    checkpoint = restore_joined_checkpoint(
        c["checkpoint"], expected_checkpoint_ref=c["checkpoint"]["checkpoint_hash"],
    )
    result = resume_joined_workloads(
        workloads=(SimpleNamespace(workload=workload, record=record),),
        resolver=resolver, saved_admission_factory=admission_factory,
        source_factory=None, host=record.host, purpose=record.purpose,
        checkpoint=checkpoint, expected_checkpoint_ref=checkpoint.checkpoint_hash,
        allow_test_only=True,
    )
    print(json.dumps({"output_refs": [r.as_dict() for r in result.output_refs]}, sort_keys=True))
"""
    return capsule_path, child


def test_saved_normal_and_completed_survive_fresh_process(tmp_path, monkeypatch):
    _, oracle_bundle, _, issued, root, receipt, issuer = _fixture(tmp_path)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    full = execute_issued_workload(
        issued.workload, issuer, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    partial = execute_issued_workload(
        issued.workload, issuer, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE, allow_test_only=True,
        max_units=1,
    )
    binding = admission.binding_receipt()
    completed_checkpoint = capture_joined_checkpoint((full,), saved_binding=binding)
    partial_checkpoint = capture_joined_checkpoint((partial,), saved_binding=binding)
    absent_checkpoint = capture_joined_checkpoint((), saved_binding=binding)
    for mode, checkpoint_arg in (
        ("normal", None),
        ("completed", completed_checkpoint),
        ("partial", partial_checkpoint),
        ("absent", absent_checkpoint),
    ):
        capsule_path, child = _fresh_process_capsule(
            tmp_path, issued, admission, checkpoint_arg, mode=mode,
        )
        completed = subprocess.run(
            [sys.executable, "-c", child, str(capsule_path)],
            cwd=str(Path(__file__).resolve().parents[2]),
            capture_output=True, text=True, timeout=120,
        )
        assert completed.returncode == 0, completed.stderr
        observed = json.loads(completed.stdout)
        expected = tuple(sorted(ref.key for ref in full.output_refs))
        assert tuple(sorted(x["object_id"] for x in observed["output_refs"])) == tuple(
            sorted(ref.object_id for ref in full.output_refs)
        )
