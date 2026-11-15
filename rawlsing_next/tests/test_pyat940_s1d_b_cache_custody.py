"""S1-D B follow-up: retained-output cache/custody attack and repair proof.

The fixtures are the same synthetic sourcefree SAV rows used by the frozen
S1-D court. The adversarial cases construct a *corrupt* completed checkpoint:
one keeps the original checkpoint hash (a mutated in-memory object), the other
recomputes both content hashes (a corrupt producer). The repaired first reader
must refuse both before any source open or positive result. The restore helper
must not reconstruct native empirical outputs before a current decision; the
resume path must parse them only after admission.

No original35 respondent/source byte is read.
"""
from __future__ import annotations

import copy
from dataclasses import replace

import pytest

import rawlsing_next.pre553_issued_workload as issued_module
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import EmpiricalFact, ExactRef, semantic_hash
from rawlsing_next.pre553_issued_workload import (
    IssuedWorkloadRecord, NativeWorkload,
    WorkloadAdmissionError, capture_joined_checkpoint, execute_issued_workload,
    operation_jobs, restore_joined_checkpoint, resume_joined_workloads,
)
from rawlsing_next.pre553_native_workload_binding import (
    TestOnlyDecisionResolver, TestOnlyIssuedWorkload as _TestOnlyIssuedWorkload,
)
from rawlsing_next.pre553_universal_workload import (
    compile_governed_frontier, compile_universal_workload,
)
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import (
    CurrentIssuer, HOST, PURPOSE, _build_multi_unit_issued, _ref_keys,
)
from rawlsing_next.tests.test_universal_source_projection import build_s3, s3_rows
from rawlsing_next.tests.test_universal_workload import (
    _frontier_bundle, _frontier_fixture,
)


def _entry_hash(entry):
    """Independent entry content address (same preimage the module captures)."""
    payload = {
        key: value for key, value in entry.material().items()
        if key != "entry_hash"
    }
    return semantic_hash(payload)


def _checkpoint_hash(checkpoint):
    return semantic_hash({
        "schema": checkpoint.schema,
        "entries": [entry.material() for entry in checkpoint.entries],
    })


def _poison_first_completed_output(checkpoint, *, rehash_entry, rehash_checkpoint):
    """Replace one retained fact with a different *valid* fact under its receipt."""
    entry = checkpoint.entries[0]
    unit_hash, row = next(iter(entry.completed_outputs.items()))
    if row["kind"] != "QUERY":
        pytest.fail("fixture must have a QUERY prefix")
    fact = row["facts"][0]
    semantic = dict(fact["semantic_fields"])
    semantic["execution_detail"] = "B-POISONED-CACHE-CONTENT"
    poisoned = EmpiricalFact(
        typed_state=fact["typed_state"],
        authority_snapshot_refs=fact["authority_snapshot_refs"],
        dependency_refs=fact["dependency_refs"],
        producer_replay_locator_or_reference_root=(
            fact["producer_replay_locator_or_reference_root"]
        ),
        **semantic,
    )
    assert poisoned.ref.key != fact["object_id"]
    poisoned_row = copy.deepcopy(row)
    poisoned_row["facts"][0] = poisoned.as_dict()
    outputs = dict(entry.completed_outputs)
    outputs[unit_hash] = poisoned_row
    poisoned_entry = replace(entry, completed_outputs=outputs)
    if rehash_entry:
        poisoned_entry = replace(poisoned_entry, entry_hash=_entry_hash(poisoned_entry))
    poisoned_checkpoint = replace(checkpoint, entries=(poisoned_entry,))
    if rehash_checkpoint:
        poisoned_checkpoint = replace(
            poisoned_checkpoint,
            checkpoint_hash=_checkpoint_hash(poisoned_checkpoint),
        )
    return poisoned_checkpoint, poisoned.ref.key


@pytest.fixture(scope="module")
def court(tmp_path_factory):
    path = tmp_path_factory.mktemp("s1d-b-cache") / "s1d-b-cache.sav"
    bundle = build_s3(path, s3_rows(respondents=6, occasions=2))
    issued = _build_multi_unit_issued(bundle)
    resolver = TestOnlyDecisionResolver(issued.record)
    full = execute_issued_workload(
        issued.workload, resolver,
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    checkpoint = capture_joined_checkpoint((full,))
    assert checkpoint.entries[0].state == "COMPLETED"
    return type("Court", (), {
        "bundle": bundle, "issued": issued, "full": full,
        "checkpoint": checkpoint,
    })()


def test_restore_without_guard_does_not_parse_protected_outputs(court, monkeypatch):
    calls = {"n": 0}
    original = issued_module._restore_output_material

    def counted(row):
        calls["n"] += 1
        return original(row)

    monkeypatch.setattr(issued_module, "_restore_output_material", counted)
    restored = restore_joined_checkpoint(
        court.checkpoint.material(),
        expected_checkpoint_ref=court.checkpoint.checkpoint_hash,
    )
    assert restored.checkpoint_hash == court.checkpoint.checkpoint_hash
    assert restored.material() == court.checkpoint.material()
    # The helper rehydrates custody material only. The protected empirical
    # output parse is deferred to resume after admission.
    assert calls["n"] == 0


def test_mutated_checkpoint_with_stale_hash_refuses_before_current_read(court):
    poisoned, _ = _poison_first_completed_output(
        court.checkpoint, rehash_entry=False, rehash_checkpoint=False,
    )
    issuer = CurrentIssuer((court.issued.record,))
    source_calls = {"n": 0}

    def factory(_ref):
        source_calls["n"] += 1
        return court.bundle.physical_stream

    with pytest.raises(
        WorkloadAdmissionError, match="JOINED_CHECKPOINT_HASH_MISMATCH"
    ):
        resume_joined_workloads(
            workloads=(court.issued,), resolver=issuer, source_factory=factory,
            host=HOST, purpose=PURPOSE, checkpoint=poisoned,
            expected_checkpoint_ref=poisoned.checkpoint_hash,
            allow_test_only=True,
        )
    assert issuer.calls == 0
    assert source_calls["n"] == 0


def test_recomputed_checkpoint_still_refuses_poisoned_retained_output(court, monkeypatch):
    poisoned, poisoned_ref = _poison_first_completed_output(
        court.checkpoint, rehash_entry=True, rehash_checkpoint=True,
    )
    assert poisoned.checkpoint_hash != court.checkpoint.checkpoint_hash
    issuer = CurrentIssuer((court.issued.record,))
    source_calls = {"n": 0}
    restore_calls = {"n": 0}
    original = issued_module._restore_output_material

    def counted(row):
        restore_calls["n"] += 1
        return original(row)

    monkeypatch.setattr(issued_module, "_restore_output_material", counted)

    def factory(_ref):
        source_calls["n"] += 1
        return court.bundle.physical_stream

    with pytest.raises(
        WorkloadAdmissionError, match="JOINED_CHECKPOINT_OUTPUT_RECEIPT_MISMATCH"
    ):
        resume_joined_workloads(
            workloads=(court.issued,), resolver=issuer, source_factory=factory,
            host=HOST, purpose=PURPOSE, checkpoint=poisoned,
            expected_checkpoint_ref=poisoned.checkpoint_hash,
            allow_test_only=True,
        )
    # Current authority was admitted before the retained payload parse; the
    # parse happened, but the poisoned fact did not match its receipt.
    assert issuer.calls >= 1
    assert restore_calls["n"] >= 1
    assert source_calls["n"] == 0
    # The poisoned ref was never accepted as a positive output.
    assert poisoned_ref not in {
        ref.key for result in (court.full,) for ref in result.output_refs
    }


def test_cold_restore_then_revoked_resume_refuses_before_payload_parse(
    court, monkeypatch,
):
    restored = restore_joined_checkpoint(
        court.checkpoint.material(),
        expected_checkpoint_ref=court.checkpoint.checkpoint_hash,
    )
    issuer = CurrentIssuer((court.issued.record,))
    issuer.revoke()
    restore_calls = {"n": 0}
    original = issued_module._restore_output_material

    def counted(row):
        restore_calls["n"] += 1
        return original(row)

    monkeypatch.setattr(issued_module, "_restore_output_material", counted)

    with pytest.raises(WorkloadAdmissionError):
        resume_joined_workloads(
            workloads=(court.issued,), resolver=issuer,
            source_factory=lambda _ref: court.bundle.physical_stream,
            host=HOST, purpose=PURPOSE, checkpoint=restored,
            expected_checkpoint_ref=restored.checkpoint_hash,
            allow_test_only=True,
        )
    assert restore_calls["n"] == 0


def test_valid_completed_checkpoint_still_reproduces_exact_outputs(court):
    issuer = CurrentIssuer((court.issued.record,))
    source_calls = {"n": 0}

    def factory(_ref):
        source_calls["n"] += 1
        return court.bundle.physical_stream

    result = resume_joined_workloads(
        workloads=(court.issued,), resolver=issuer, source_factory=factory,
        host=HOST, purpose=PURPOSE, checkpoint=court.checkpoint,
        expected_checkpoint_ref=court.checkpoint.checkpoint_hash,
        allow_test_only=True,
    )
    assert source_calls["n"] == 0
    assert _ref_keys(result.output_refs) == _ref_keys(court.full.output_refs)
    assert len(result.completed_results) == 1
    native = result.completed_results[0]
    assert native.manifest.manifest_hash == court.full.manifest.manifest_hash
    observed = {
        unit_hash: tuple(fact.ref.key for fact in output.facts)
        for unit_hash, output in native.outputs_by_unit.items()
    }
    expected = {
        unit_hash: tuple(fact.ref.key for fact in output.facts)
        for unit_hash, output in court.full.outputs_by_unit.items()
    }
    assert observed == expected


# D09 ---------------------------------------------------------------------
def _merge_refs(values):
    by_key = {value.ref.key: value for value in values}
    return tuple(by_key[key] for key in sorted(by_key))


def _merge_authority_refs(values):
    by_key = {value.authority_ref.key: value for value in values}
    return tuple(by_key[key] for key in sorted(by_key))


def test_d09_same_source_r04_partial_resume_native_parity(tmp_path):
    """Exercise the existing R04 partial-resume path with the required resolver.

    This is the same-source R04 -> native I03/I05/Batch first-reader scenario
    used by ``test_universal_world_binding.py``. The legacy call site there is
    readonly/outside this packet's grant and still omits the required resolver;
    this allowed test supplies a fresh TEST_ONLY resolver without weakening the
    original positive/negative assertions.
    """
    world_as_of = "2026-10-24"
    world_host = "local-r91-r04"
    world_purpose = "TEST_ONLY_SOURCEFREE"

    bundle, _ = _frontier_bundle(tmp_path / "s1d-b-same-source.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    governed = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=world_as_of, host=world_host, purpose=world_purpose,
    )
    universal = compile_universal_workload(
        bundle=bundle, as_of=world_as_of, host=world_host, purpose=world_purpose,
    )
    query_issued = universal.compiled[0].issued
    base = query_issued.workload
    discovery = governed.issued.workload
    catalog = RuntimeObjectCatalog(
        authorities=_merge_authority_refs(
            base.catalog.authorities + discovery.catalog.authorities
        ),
        predicates=_merge_refs(
            base.catalog.predicates + discovery.catalog.predicates
        ),
        queries=_merge_refs(base.catalog.queries + discovery.catalog.queries),
        discovery_authorities=_merge_refs(
            base.catalog.discovery_authorities
            + discovery.catalog.discovery_authorities
        ),
    )
    workload = NativeWorkload(
        decision_ref=ExactRef(
            "TEST_ONLY_DECISION", "urn:test:s1d-b:same-source", "9" * 64,
        ),
        source_factory_ref=base.source_factory_ref,
        descriptor=base.descriptor, projection=base.projection,
        catalog=catalog,
        requests=base.requests, discoveries=discovery.discoveries,
        original_u_root=base.original_u_root,
        expected_frontier_root=base.expected_frontier_root,
    )
    record = IssuedWorkloadRecord(
        decision_ref=workload.decision_ref,
        source_permission_ref=query_issued.record.source_permission_ref,
        scientific_permission_refs=query_issued.record.scientific_permission_refs,
        host=world_host, purpose=world_purpose,
        source_sha256=query_issued.record.source_sha256,
        envelope_sha256=semantic_hash(workload.envelope()),
        original_u_root=workload.original_u_root,
        expected_frontier_root=workload.expected_frontier_root,
        expected_jobs=operation_jobs(workload.requests, workload.discoveries),
        currentness="CURRENT_GRANTED", scope=query_issued.record.scope,
    )
    issued = _TestOnlyIssuedWorkload(
        workload=workload, record=record,
        descriptor=query_issued.descriptor,
        envelope_sha256=record.envelope_sha256,
    )
    resolver = TestOnlyDecisionResolver(record)

    partial = execute_issued_workload(
        workload, resolver,
        source_factory=lambda _ref: bundle.physical_stream,
        host=world_host, purpose=world_purpose, allow_test_only=True, max_units=1,
    )
    checkpoint = capture_joined_checkpoint((partial,))
    restored = restore_joined_checkpoint(
        checkpoint.material(), expected_checkpoint_ref=checkpoint.checkpoint_hash,
    )
    resumed = resume_joined_workloads(
        workloads=(issued,), resolver=resolver,
        source_factory=lambda _ref: bundle.physical_stream,
        host=world_host, purpose=world_purpose, checkpoint=restored,
        expected_checkpoint_ref=checkpoint.checkpoint_hash,
        allow_test_only=True,
    )
    final = resumed.resumed_results[0]
    full = execute_issued_workload(
        workload, resolver,
        source_factory=lambda _ref: bundle.physical_stream,
        host=world_host, purpose=world_purpose, allow_test_only=True,
    )
    assert len(partial.receipts) == 1
    assert checkpoint.entries[0].state == "PARTIAL"
    assert len(resumed.completed_results) == 0
    assert len(resumed.resumed_results) == 1
    assert len(final.receipts) == len(full.receipts) == 2
    assert final.output_refs == full.output_refs
    resumed_route = final.route_results[0]
    full_route = full.route_results[0]
    assert resumed_route.replay_receipt["receipt_identity"] == (
        full_route.replay_receipt["receipt_identity"]
    )
    assert tuple(
        ref.as_dict() for ref in resumed_route.object_graph.empirical_facts
    ) == tuple(
        ref.as_dict() for ref in full_route.object_graph.empirical_facts
    )

    revoked = replace(record, currentness="REVOKED")
    revoked_issued = _TestOnlyIssuedWorkload(
        workload=workload, record=revoked,
        descriptor=query_issued.descriptor,
        envelope_sha256=record.envelope_sha256,
    )
    with pytest.raises(WorkloadAdmissionError):
        resume_joined_workloads(
            workloads=(revoked_issued,),
            resolver=TestOnlyDecisionResolver(revoked),
            source_factory=lambda _ref: bundle.physical_stream,
            host=world_host, purpose=world_purpose, checkpoint=checkpoint,
            expected_checkpoint_ref=checkpoint.checkpoint_hash,
            allow_test_only=True,
        )
    bad_stream = replace(bundle.physical_stream, source_sha256="f" * 64)
    with pytest.raises(WorkloadAdmissionError):
        execute_issued_workload(
            workload, resolver, source_factory=lambda _ref: bad_stream,
            host=world_host, purpose=world_purpose, allow_test_only=True,
        )


def test_recomputed_checkpoint_still_refuses_entry_hash_tamper(court):
    entry = court.checkpoint.entries[0]
    tampered_entry = replace(entry, output_refs=())
    tampered = replace(court.checkpoint, entries=(tampered_entry,))
    tampered = replace(tampered, checkpoint_hash=_checkpoint_hash(tampered))
    issuer = CurrentIssuer((court.issued.record,))
    source_calls = {"n": 0}

    def factory(_ref):
        source_calls["n"] += 1
        return court.bundle.physical_stream

    with pytest.raises(
        WorkloadAdmissionError, match="JOINED_CHECKPOINT_ENTRY_HASH_MISMATCH"
    ):
        resume_joined_workloads(
            workloads=(court.issued,), resolver=issuer, source_factory=factory,
            host=HOST, purpose=PURPOSE, checkpoint=tampered,
            expected_checkpoint_ref=tampered.checkpoint_hash,
            allow_test_only=True,
        )
    assert source_calls["n"] == 0
