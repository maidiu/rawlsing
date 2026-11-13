"""#997: one actual SAV/DTA Q2 -> S2-C -> S2-D I03/I05/Batch and S1-C fate join.

All fixtures are TEST_ONLY_SOURCEFREE; neither saved current guard nor the
existing test-only issuer grants original35 or production source rights.
"""
from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_batch_runner import (
    BatchManifest, BatchUnitSpec, BatchExecutionRunner,
)
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission, SavedReleaseIdentity
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_i03, execute_saved_i05, execute_saved_batch,
)
from rawlsing_next.pre553_issued_workload import execute_issued_workload
from rawlsing_next.pre553_source_postconsumer_receipts import (
    join_saved_source_operation_fates, SourceReceiptJoinError,
)
from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
from rawlsing_next.tests.test_pyat960_s1e_native_fact import (
    _native_fixture, _native_bundle, _compile_native, _NATIVE_HOST, _NATIVE_PURPOSE,
)
from rawlsing_next.tests.test_pyat960_s1e_support import build


def _full(tmp_path: Path, values=(0., 1., 0., 1., 0.), source_format="SAV"):
    tmp_path.mkdir(parents=True, exist_ok=True)
    # R03 owner fixture has exact TEST_ONLY risk/authority and canonical cells.
    fixture = _native_fixture(tmp_path, values=values)
    private = tmp_path / "private"
    private.mkdir(mode=0o700)
    certificate = tmp_path / "source-i02.sqlite"
    sink = SourceSavedBodySink(
        certificate_path=certificate, authorized_private_root=private, chunk_rows=2,
    )
    handoff = build(
        tmp_path, fixture, name="source-i02.sqlite",
        body_sink=sink, chunk_size=2,
    )
    estate = sink.receipt
    assert estate.i02 == handoff.roots
    assert handoff.stats.source_reads == 1
    assert handoff.stats.full_c11_builds == 0
    # The native compiler only needs a *release identity* in this bundle;
    # saved reader uses the genuine qualified physical body and exact v1 ref.
    release_identity = SavedReleaseIdentity(estate.reconstructed_v1_release_ref)
    bundle = _native_bundle(handoff, fixture, fixture["projection"], release_identity)
    compilation = _compile_native(fixture, handoff, fixture["projection"], release_identity)
    issued = compilation.issued
    assert issued.workload.projection == fixture["projection"]
    admission = SavedC11Admission.open(
        root=private, exact_path=estate.path,
        independently_held_manifest_sha256=estate.manifest_sha256,
        independently_held_i02=estate.i02,
        release_ref=estate.reconstructed_v1_release_ref,
        runtime_catalog=issued.workload.catalog,
        current_authorizer=lambda _roots: True,
    )
    resolver = TestOnlyDecisionResolver(issued.record)
    return handoff, estate, admission, compilation, resolver, sink


def _native_i03(admission, compilation):
    for entry in compilation.plan.records:
        if entry.status != "SUPPORTED" or not entry.query_refs:
            continue
        query_ref = exact_ref(entry.query_refs[0], "lowering query")
        query = compilation.issued.workload.catalog.resolve_query_exact(query_ref)
        predicate_ref = exact_ref(query.condition_predicate_ref, "lowering predicate")
        result = execute_saved_i03(
            admission, query_ref=query_ref, predicate_ref=predicate_ref)
        if result.facts:
            return entry.operation_id, result
    pytest.fail("no S1-C supported saved-native I03 first reader")


def _run(tmp_path, values):
    handoff, estate, admission, compilation, resolver, sink = _full(tmp_path, values)
    record = compilation.issued.record
    workload = compilation.issued.workload
    operation, fact_result = _native_i03(admission, compilation)
    authority_ref = workload.discoveries[0]
    discovery = execute_saved_i05(admission, discovery_authority_ref=authority_ref)
    assert discovery.receipts
    batch_manifest = BatchManifest((
        BatchUnitSpec("DISCOVERY", authority_ref,
                      (admission.release_ref,), (workload.decision_ref,)),
    ))
    batch = execute_saved_batch(
        admission, manifest=batch_manifest, predicate_ref_by_query={},
    )
    assert len(batch.receipts) == 1 and batch.receipts[0].state == "COMPLETED"
    # Also exercise the previously accepted S2-D normal issued-workload reader
    # with source_factory absent: it must NOT re-decode the SAV source.
    normal = execute_issued_workload(
        workload, resolver, source_factory=None,
        saved_admission_factory=lambda: admission,
        host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, allow_test_only=True,
    )
    assert all(r.state == "COMPLETED" for r in normal.receipts)
    joined = join_saved_source_operation_fates(
        handoff=handoff, estate_receipt=estate, admission=admission,
        compilation=compilation, workload=workload, resolver=resolver,
        host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, runner=batch,
    )
    assert len(joined.rows) == len(handoff.operation_fates)
    assert joined.audit["positive_native_linked_operations"] > 0
    assert joined.audit["native_discovery_candidates_exactly_joined"] > 0
    assert all(x["issued_receipt_refs"] == () for x in handoff.operation_fates)
    assert any(x["disposition"] != "ELIGIBLE" for x in joined.rows)
    assert all(
        not row["postconsumer_receipt_refs"]
        for row in joined.rows if row["disposition"] != "ELIGIBLE"
    )
    assert all(
        row["postconsumer_batch_receipt_refs"]
        for row in joined.rows
        if row["postconsumer_state"] == "TEST_ONLY_SAVED_NATIVE_DISCOVERY_RECEIPTED"
    )
    return (handoff, estate, admission, compilation, resolver, batch, joined,
            tuple(f.ref.key for f in fact_result.facts),
            tuple(r.ref.key for r in discovery.receipts))


def test_source_to_saved_cold_s1c_i03_i05_batch_normal_and_exact_fate_join(tmp_path):
    first = _run(tmp_path / "first", (0., 1., 0., 1., 0.))
    changed = _run(tmp_path / "changed", (0., 1., 1., 1., 0.))
    restored = _run(tmp_path / "restored", (0., 1., 0., 1., 0.))
    assert first[0].source_sha256 != changed[0].source_sha256
    assert first[1].i02.logical != changed[1].i02.logical
    assert first[1].i02.logical == restored[1].i02.logical
    assert first[7] != changed[7] or first[8] != changed[8]
    assert first[7] == restored[7]
    assert first[8] == restored[8]
    assert first[6].result_hash == restored[6].result_hash


def test_missing_issued_batch_receipt_stays_pending_not_invented(tmp_path):
    handoff, estate, admission, compilation, resolver, _ = _full(tmp_path / "missing")
    workload = compilation.issued.workload
    batch_manifest = BatchManifest((
        BatchUnitSpec("DISCOVERY", workload.discoveries[0],
                      (admission.release_ref,), (workload.decision_ref,)),
    ))
    never_executed = BatchExecutionRunner(
        manifest=batch_manifest, repository=admission, saved_mode=True)
    joined = join_saved_source_operation_fates(
        handoff=handoff, estate_receipt=estate, admission=admission,
        compilation=compilation, workload=workload, resolver=resolver,
        host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, runner=never_executed,
    )
    assert joined.audit["positive_native_linked_operations"] == 0
    assert joined.audit["pending_eligible_operations"] > 0
    assert not any(row["postconsumer_receipt_refs"] for row in joined.rows)


def test_mixed_source_issued_receipt_join_refused_before_claim(tmp_path):
    original = _full(tmp_path / "original")
    other = _full(tmp_path / "other", values=(1., 1., 1., 1., 1.))
    handoff, estate, admission, compilation, resolver, _ = original
    alien_admission = other[2]
    workload = compilation.issued.workload
    manifest = BatchManifest((
        BatchUnitSpec("DISCOVERY", workload.discoveries[0],
                      (alien_admission.release_ref,), (workload.decision_ref,)),
    ))
    runner = BatchExecutionRunner(manifest=manifest,
                                  repository=alien_admission, saved_mode=True)
    with pytest.raises(SourceReceiptJoinError, match="Q2_SAVED_REPLAY_AND_RELEASE_IDENTITY_DRIFT"):
        join_saved_source_operation_fates(
            handoff=handoff, estate_receipt=estate, admission=alien_admission,
            compilation=compilation, workload=workload, resolver=resolver,
            host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, runner=runner,
        )
