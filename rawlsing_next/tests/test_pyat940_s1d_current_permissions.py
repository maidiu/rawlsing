"""S1-D frozen-court: independent CURRENT decisions in normal and all resume fates.

All fixtures are synthetic sourcefree SAV rows built through the existing
source-projection/test-only path. No original35 respondent/source byte is read.
The ``CurrentIssuer`` classes are explicit test doubles for an external
current-decision reader; they are not a production issuer or credential store.
"""
from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

import rawlsing_next.pre553_issued_workload as issued_module
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_issued_workload import (
    IssuedWorkloadRecord, NativeWorkload, WorkloadAdmissionError, admit,
    capture_joined_checkpoint, execute_issued_workload, operation_jobs,
    restore_joined_checkpoint, resume_joined_workloads,
)
from rawlsing_next.pre553_native_workload_binding import (
    OperationFixture, TestOnlyDecisionResolver,
    TestOnlyIssuedWorkload as _IssuedWorkload,
    build_projection_catalog,
)
from rawlsing_next.tests.test_universal_source_projection import (
    build_s3, load_s3, s3_rows,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
AS_OF = "2026-10-24"
HOST = "local-s1d-current"
PURPOSE = "TEST_ONLY_SOURCEFREE"


def _merge_by_ref(values):
    by_key = {value.ref.key: value for value in values}
    return tuple(by_key[key] for key in sorted(by_key))


def _merge_by_authority_ref(values):
    by_key = {value.authority_ref.key: value for value in values}
    return tuple(by_key[key] for key in sorted(by_key))


def _build_multi_unit_issued(
    bundle, *, as_of: str = AS_OF, host: str = HOST, purpose: str = PURPOSE,
) -> _IssuedWorkload:
    """Build a real two-query native workload so PARTIAL has an actual prefix."""
    catalogs = []
    for value in ("0", "1"):
        fixture = OperationFixture(
            fixture_id="S1D-MULTI-" + value,
            target_variable_code="SCORE",
            response_value=value,
        )
        catalog, request = build_projection_catalog(
            bundle=bundle, operation=fixture, as_of=as_of,
        )
        catalogs.append((catalog, request))
    runtime_catalog = RuntimeObjectCatalog(
        authorities=_merge_by_authority_ref(
            [obj for catalog, _ in catalogs for obj in catalog.authorities]
        ),
        predicates=_merge_by_ref(
            [obj for catalog, _ in catalogs for obj in catalog.predicates]
        ),
        queries=_merge_by_ref(
            [obj for catalog, _ in catalogs for obj in catalog.queries]
        ),
        discovery_authorities=(),
    )
    requests = tuple(request for _, request in catalogs)
    descriptor = {
        "source_edition": bundle.source_sha256,
        "native_item_ids": sorted(
            item.source_variable_code for item in bundle.administered
        ),
        "release_tag": bundle.projection.instrument_release_id,
        "routing_and_risk": {
            "routing_facts": len(bundle.projection.routing),
            "risk_tag": "S1D-CURRENT",
        },
        "carrier": {
            "source_format": "SYNTHETIC_NONRESPONDENT_FIXTURE",
            "source_artifact_id": bundle.projection.source_artifact_id,
        },
        "country_and_population": {"country": "US", "population": "ADULTS"},
        "weight_design_estimand": {"weight_basis": "W", "estimand": "TEST_ONLY"},
        "missing_and_occurrence_policy": {
            "missing": "EXPLICIT_TYPED_STATES", "occurrence": "SCALAR_SINGULAR",
        },
        "target_conditioner_roles": {
            "target": "Y", "conditioner": None, "measure_kind": "BOTH",
        },
    }
    descriptor_bytes = json.dumps(
        descriptor, sort_keys=True, separators=(",", ":")
    ).encode()
    workload = NativeWorkload(
        decision_ref=ExactRef(
            "TEST_ONLY_DECISION", "urn:test:s1d:multi", "9" * 64,
        ),
        source_factory_ref=ExactRef(
            "SOURCE_FACTORY", "urn:test:s1d:source", "b" * 64,
        ),
        descriptor=descriptor_bytes,
        projection=bundle.projection,
        catalog=runtime_catalog,
        requests=requests,
        discoveries=(),
        original_u_root="c" * 64,
        expected_frontier_root="d" * 64,
    )
    record = IssuedWorkloadRecord(
        decision_ref=workload.decision_ref,
        source_permission_ref=ExactRef(
            "TEST_ONLY_SOURCE_PERMISSION", "urn:test:s1d:sp", "e" * 64,
        ),
        scientific_permission_refs=(
            ExactRef("TEST_ONLY_SCIENTIFIC_PERMISSION", "urn:test:s1d:sc", "f" * 64),
        ),
        host=host,
        purpose=purpose,
        source_sha256=bundle.source_sha256,
        envelope_sha256=semantic_hash(workload.envelope()),
        original_u_root=workload.original_u_root,
        expected_frontier_root=workload.expected_frontier_root,
        expected_jobs=operation_jobs(requests, ()),
        currentness="CURRENT_GRANTED",
        scope="TEST_ONLY_SOURCEFREE",
    )
    return _IssuedWorkload(
        workload=workload,
        record=record,
        descriptor=descriptor,
        envelope_sha256=record.envelope_sha256,
    )


class CurrentIssuer:
    """Repeatable, explicitly TEST_ONLY current-decision test double."""

    def __init__(
        self, records, *, revoked=(), expired=(), revoke_on_call=None,
        change_on_call=None, changed=None,
    ):
        self._records = {record.decision_ref.key: record for record in records}
        self._revoked = set(revoked)
        self._expired = set(expired)
        self._revoke_on_call = revoke_on_call
        self._change_on_call = change_on_call
        self._changed = changed
        self.calls = 0

    def revoke(self, *keys):
        self._revoked.update(keys or self._records)

    def restore(self, *keys):
        if keys:
            self._revoked.difference_update(keys)
            self._expired.difference_update(keys)
        else:
            self._revoked.clear()
            self._expired.clear()

    def resolve_current(self, decision_ref):
        self.calls += 1
        if self._revoke_on_call is not None and self.calls >= self._revoke_on_call:
            raise WorkloadAdmissionError("INDEPENDENT_CURRENT_DECISION_REVOKED")
        if decision_ref.key not in self._records:
            raise KeyError(decision_ref.key)
        if self._change_on_call is not None and self.calls >= self._change_on_call:
            return self._changed
        record = self._records[decision_ref.key]
        if decision_ref.key in self._revoked:
            return replace(record, currentness="REVOKED")
        if decision_ref.key in self._expired:
            return replace(record, currentness="EXPIRED")
        return record


def _counted_source(bundle, *, after_open=None):
    calls = {"count": 0}

    def factory(_ref):
        calls["count"] += 1
        source = bundle.physical_stream
        if after_open is not None:
            after_open()
        return source

    return calls, factory


def _count_builds(monkeypatch):
    calls = {"count": 0}
    original = issued_module.build_source_backed_c11_repository

    def counted(*args, **kwargs):
        calls["count"] += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(
        issued_module, "build_source_backed_c11_repository", counted
    )
    return calls


def _count_restores(monkeypatch):
    calls = {"count": 0}
    original = issued_module._restore_output_material

    def counted(row):
        calls["count"] += 1
        return original(row)

    monkeypatch.setattr(issued_module, "_restore_output_material", counted)
    return calls


def _ref_keys(refs):
    return tuple(sorted(ref.key for ref in refs))


def _variant_issued(issued, *, decision_ref):
    workload = replace(issued.workload, decision_ref=decision_ref)
    record = replace(
        issued.record,
        decision_ref=decision_ref,
        envelope_sha256=semantic_hash(workload.envelope()),
    )
    return _IssuedWorkload(
        workload=workload, record=record, descriptor=issued.descriptor,
        envelope_sha256=record.envelope_sha256,
    )


def _execute(court, issuer, source_factory, **kwargs):
    return execute_issued_workload(
        court.issued.workload, issuer, source_factory=source_factory,
        host=HOST, purpose=PURPOSE, allow_test_only=True, **kwargs,
    )


def _resume(court, issuer, checkpoint, source_factory, **kwargs):
    return resume_joined_workloads(
        workloads=(court.issued,), resolver=issuer, source_factory=source_factory,
        host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
        expected_checkpoint_ref=checkpoint.checkpoint_hash,
        allow_test_only=True, **kwargs,
    )


def _checkpoints(court):
    return {
        "completed": court.completed_checkpoint,
        "partial": court.partial_checkpoint,
        "absent": court.absent_checkpoint,
    }


@pytest.fixture(scope="module")
def court(tmp_path_factory):
    path = tmp_path_factory.mktemp("s1d-current") / "s1d-current.sav"
    bundle = build_s3(path, s3_rows(respondents=6, occasions=2))
    issued = _build_multi_unit_issued(bundle)
    resolver = TestOnlyDecisionResolver(issued.record)
    full = execute_issued_workload(
        issued.workload, resolver,
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    partial = execute_issued_workload(
        issued.workload, resolver,
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True, max_units=1,
    )
    assert len(full.receipts) == 2
    assert len(partial.receipts) == 1
    completed_checkpoint = capture_joined_checkpoint((full,))
    partial_checkpoint = capture_joined_checkpoint((partial,))
    absent_checkpoint = capture_joined_checkpoint(())
    assert completed_checkpoint.entries[0].state == "COMPLETED"
    assert partial_checkpoint.entries[0].state == "PARTIAL"
    return SimpleNamespace(
        path=path,
        bundle=bundle,
        issued=issued,
        full=full,
        partial=partial,
        completed_checkpoint=completed_checkpoint,
        partial_checkpoint=partial_checkpoint,
        absent_checkpoint=absent_checkpoint,
    )


# D01 ---------------------------------------------------------------------
def test_d01_normal_current_change_restore(court, monkeypatch):
    builds = _count_builds(monkeypatch)
    issuer = CurrentIssuer((court.issued.record,))
    calls, factory = _counted_source(court.bundle)
    first = _execute(court, issuer, factory)
    assert calls["count"] == 1
    assert builds["count"] == 1
    assert _ref_keys(first.output_refs) == _ref_keys(court.full.output_refs)
    assert first.manifest.manifest_hash == court.full.manifest.manifest_hash

    issuer.revoke()
    revoked_calls, revoked_factory = _counted_source(court.bundle)
    with pytest.raises(WorkloadAdmissionError):
        _execute(court, issuer, revoked_factory)
    assert revoked_calls["count"] == 0
    assert builds["count"] == 1

    issuer.restore()
    restored_calls, restored_factory = _counted_source(court.bundle)
    restored = _execute(court, issuer, restored_factory)
    assert restored_calls["count"] == 1
    assert builds["count"] == 2
    assert _ref_keys(restored.output_refs) == _ref_keys(first.output_refs)
    assert restored.manifest.manifest_hash == first.manifest.manifest_hash


def test_d01_changed_valid_permission_midjob_refuses_before_publication(
    court, monkeypatch,
):
    changed = replace(
        court.issued.record,
        source_permission_ref=ExactRef(
            "TEST_ONLY_SOURCE_PERMISSION", "urn:test:s1d:sp:changed", "a" * 64,
        ),
    )
    issuer = CurrentIssuer(
        (court.issued.record,), change_on_call=3, changed=changed,
    )
    calls, factory = _counted_source(court.bundle)
    with pytest.raises(WorkloadAdmissionError, match="SNAPSHOT_CHANGED"):
        _execute(court, issuer, factory)
    assert calls["count"] == 1


# D02 ---------------------------------------------------------------------
def test_d02_completed_current_change_restore(court, monkeypatch):
    builds = _count_builds(monkeypatch)
    restores = _count_restores(monkeypatch)
    issuer = CurrentIssuer((court.issued.record,))
    calls, factory = _counted_source(court.bundle)
    result = _resume(court, issuer, court.completed_checkpoint, factory)
    assert len(result.completed_results) == 1
    assert result.resumed_results == ()
    assert calls["count"] == 0
    assert builds["count"] == 0
    assert restores["count"] >= 1
    assert _ref_keys(result.output_refs) == _ref_keys(court.full.output_refs)

    issuer.revoke()
    before_restores = restores["count"]
    revoked_calls, revoked_factory = _counted_source(court.bundle)
    with pytest.raises(WorkloadAdmissionError):
        _resume(court, issuer, court.completed_checkpoint, revoked_factory)
    assert revoked_calls["count"] == 0
    assert builds["count"] == 0
    assert restores["count"] == before_restores

    issuer.restore()
    restored_calls, restored_factory = _counted_source(court.bundle)
    restored = _resume(court, issuer, court.completed_checkpoint, restored_factory)
    assert restored_calls["count"] == 0
    assert _ref_keys(restored.output_refs) == _ref_keys(court.full.output_refs)


# D03 ---------------------------------------------------------------------
def test_d03_partial_current_change_restore(court, monkeypatch):
    builds = _count_builds(monkeypatch)
    restores = _count_restores(monkeypatch)
    issuer = CurrentIssuer((court.issued.record,))
    calls, factory = _counted_source(court.bundle)
    result = _resume(court, issuer, court.partial_checkpoint, factory)
    assert len(result.completed_results) == 0
    assert len(result.resumed_results) == 1
    assert calls["count"] == 1
    assert builds["count"] == 1
    assert restores["count"] >= 1
    assert _ref_keys(result.output_refs) == _ref_keys(court.full.output_refs)
    final = result.resumed_results[0]
    assert len(final.receipts) == 2
    assert all(receipt.state == "COMPLETED" for receipt in final.receipts)
    assert len({receipt.unit_ref.key for receipt in final.receipts}) == 2
    assert final.outputs_by_unit and len(final.outputs_by_unit) == 2

    issuer.revoke()
    before_restores = restores["count"]
    revoked_calls, revoked_factory = _counted_source(court.bundle)
    with pytest.raises(WorkloadAdmissionError):
        _resume(court, issuer, court.partial_checkpoint, revoked_factory)
    assert revoked_calls["count"] == 0
    assert builds["count"] == 1
    assert restores["count"] == before_restores

    issuer.restore()
    restored_calls, restored_factory = _counted_source(court.bundle)
    restored = _resume(court, issuer, court.partial_checkpoint, restored_factory)
    assert restored_calls["count"] == 1
    assert builds["count"] == 2
    assert _ref_keys(restored.output_refs) == _ref_keys(court.full.output_refs)


# D04 ---------------------------------------------------------------------
def test_d04_absent_current_change_restore(court, monkeypatch):
    builds = _count_builds(monkeypatch)
    issuer = CurrentIssuer((court.issued.record,))
    calls, factory = _counted_source(court.bundle)
    result = _resume(court, issuer, court.absent_checkpoint, factory)
    assert len(result.completed_results) == 0
    assert len(result.resumed_results) == 1
    assert calls["count"] == 1
    assert builds["count"] == 1
    assert _ref_keys(result.output_refs) == _ref_keys(court.full.output_refs)

    issuer.revoke()
    revoked_calls, revoked_factory = _counted_source(court.bundle)
    with pytest.raises(WorkloadAdmissionError):
        _resume(court, issuer, court.absent_checkpoint, revoked_factory)
    assert revoked_calls["count"] == 0
    assert builds["count"] == 1

    issuer.restore()
    restored_calls, restored_factory = _counted_source(court.bundle)
    restored = _resume(court, issuer, court.absent_checkpoint, restored_factory)
    assert restored_calls["count"] == 1
    assert builds["count"] == 2
    assert _ref_keys(restored.output_refs) == _ref_keys(court.full.output_refs)


# D05 ---------------------------------------------------------------------
@pytest.mark.parametrize("fate", ("normal", "completed", "partial", "absent"))
def test_d05_frozen_granted_external_revoked_zero_opens_all4(
    court, fate, monkeypatch,
):
    # The historical item.record remains CURRENT_GRANTED; only the independent
    # resolver says REVOKED.
    assert court.issued.record.currentness == "CURRENT_GRANTED"
    issuer = CurrentIssuer(
        (court.issued.record,),
        revoked={court.issued.record.decision_ref.key},
    )
    builds = _count_builds(monkeypatch)
    restores = _count_restores(monkeypatch)
    calls, factory = _counted_source(court.bundle)
    with pytest.raises(WorkloadAdmissionError):
        if fate == "normal":
            _execute(court, issuer, factory)
        else:
            _resume(court, issuer, _checkpoints(court)[fate], factory)
    assert calls["count"] == 0
    assert builds["count"] == 0
    assert restores["count"] == 0


def test_d05_historical_revoked_external_granted_serves(court):
    # The historical record is not authority in either direction. A stale
    # REVOKED snapshot does not defeat a genuinely current external grant.
    historical = replace(
        court.issued,
        record=replace(court.issued.record, currentness="REVOKED"),
    )
    issuer = CurrentIssuer((court.issued.record,))
    calls, factory = _counted_source(court.bundle)
    result = resume_joined_workloads(
        workloads=(historical,), resolver=issuer, source_factory=factory,
        host=HOST, purpose=PURPOSE, checkpoint=court.completed_checkpoint,
        expected_checkpoint_ref=court.completed_checkpoint.checkpoint_hash,
        allow_test_only=True,
    )
    assert calls["count"] == 0
    assert len(result.completed_results) == 1
    assert _ref_keys(result.output_refs) == _ref_keys(court.full.output_refs)


def test_d05_cold_restore_guard_refuses_before_payload_parse(court, monkeypatch):
    key = court.issued.record.decision_ref.key
    issuer = CurrentIssuer((court.issued.record,), revoked={key})
    restores = _count_restores(monkeypatch)

    def guard(_refs):
        admit(
            court.issued.workload, issuer, host=HOST, purpose=PURPOSE,
            allow_test_only=True,
        )

    with pytest.raises(WorkloadAdmissionError):
        restore_joined_checkpoint(
            court.completed_checkpoint.material(),
            expected_checkpoint_ref=court.completed_checkpoint.checkpoint_hash,
            current_guard=guard,
        )
    assert restores["count"] == 0

    # Restoring the same current decision rehydrates the exact pinned checkpoint.
    issuer.restore()
    restored = restore_joined_checkpoint(
        court.completed_checkpoint.material(),
        expected_checkpoint_ref=court.completed_checkpoint.checkpoint_hash,
        current_guard=guard,
    )
    assert restored.checkpoint_hash == court.completed_checkpoint.checkpoint_hash
    assert restored.material() == court.completed_checkpoint.material()


# D06 ---------------------------------------------------------------------
@pytest.mark.parametrize(
    "label,record_factory",
    (
        ("wrong_source", lambda r: replace(r, source_sha256="f" * 64)),
        ("wrong_host", lambda r: replace(r, host="wrong-host")),
        ("wrong_purpose", lambda r: replace(r, purpose="wrong-purpose")),
        ("wrong_envelope", lambda r: replace(r, envelope_sha256="0" * 64)),
        ("wrong_jobs", lambda r: replace(
            r, expected_jobs=(("QUERY", "bad", "bad"),),
        )),
        ("wrong_decision", lambda r: replace(
            r, decision_ref=ExactRef(
                "TEST_ONLY_DECISION", "urn:test:s1d:other", "8" * 64,
            ),
        )),
        ("expired", lambda r: replace(r, currentness="EXPIRED")),
    ),
)
def test_d06_wrong_decision_fields_refuse_normal(court, label, record_factory):
    issuer = CurrentIssuer((record_factory(court.issued.record),))
    calls, factory = _counted_source(court.bundle)
    with pytest.raises(WorkloadAdmissionError):
        _execute(court, issuer, factory)
    assert calls["count"] == 0, label


def test_d06_unknown_issuer_decision_refuses(court):
    issuer = CurrentIssuer(())
    calls, factory = _counted_source(court.bundle)
    with pytest.raises(WorkloadAdmissionError):
        _execute(court, issuer, factory)
    assert calls["count"] == 0


@pytest.mark.parametrize("fate", ("completed", "partial", "absent"))
@pytest.mark.parametrize(
    "label,record_factory",
    (
        ("wrong_source", lambda r: replace(r, source_sha256="f" * 64)),
        ("wrong_host", lambda r: replace(r, host="wrong-host")),
        ("wrong_purpose", lambda r: replace(r, purpose="wrong-purpose")),
        ("wrong_envelope", lambda r: replace(r, envelope_sha256="0" * 64)),
    ),
)
def test_d06_wrong_decision_fields_refuse_all_resume_fates(
    court, fate, label, record_factory, monkeypatch,
):
    issuer = CurrentIssuer((record_factory(court.issued.record),))
    builds = _count_builds(monkeypatch)
    restores = _count_restores(monkeypatch)
    calls, factory = _counted_source(court.bundle)
    with pytest.raises(WorkloadAdmissionError):
        _resume(court, issuer, _checkpoints(court)[fate], factory)
    assert calls["count"] == 0, label
    assert builds["count"] == 0
    assert restores["count"] == 0


def test_d06_asof_is_bound_in_envelope_and_changes_admission(tmp_path):
    first_path = tmp_path / "asof-a.sav"
    first_bundle = build_s3(first_path, s3_rows(respondents=4, occasions=2))
    second_bundle = load_s3(first_path)
    first = _build_multi_unit_issued(first_bundle, as_of="2026-10-24")
    second = _build_multi_unit_issued(second_bundle, as_of="2026-10-25")
    assert first.workload.envelope() != second.workload.envelope()
    assert first.record.envelope_sha256 != second.record.envelope_sha256
    stale = replace(
        second.record,
        decision_ref=first.workload.decision_ref,
        envelope_sha256=semantic_hash(second.workload.envelope()),
    )
    issuer = CurrentIssuer((stale,))
    calls = {"count": 0}

    def factory(_ref):
        calls["count"] += 1
        return first_bundle.physical_stream

    with pytest.raises(WorkloadAdmissionError):
        execute_issued_workload(
            first.workload, issuer, source_factory=factory,
            host=HOST, purpose=PURPOSE, allow_test_only=True,
        )
    assert calls["count"] == 0
    # The same source bytes with the exact original as-of envelope is admitted.
    granted = CurrentIssuer((first.record,))
    result = execute_issued_workload(
        first.workload, granted, source_factory=factory,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    assert result.envelope_sha256 == first.record.envelope_sha256


# D07 ---------------------------------------------------------------------
def test_d07_midjob_and_pre_serve_revocation(court, monkeypatch):
    # Revoked between admission and source factory: zero source opens.
    issuer = CurrentIssuer((court.issued.record,), revoke_on_call=2)
    calls, factory = _counted_source(court.bundle)
    with pytest.raises(WorkloadAdmissionError):
        _execute(court, issuer, factory)
    assert calls["count"] == 0

    # Revoked by the source factory after the source has opened: no result.
    issuer = CurrentIssuer((court.issued.record,))
    calls, factory = _counted_source(
        court.bundle, after_open=lambda: issuer.revoke(),
    )
    with pytest.raises(WorkloadAdmissionError):
        _execute(court, issuer, factory)
    assert calls["count"] == 1

    # COMPLETED: restore happens, then the pre-serve recheck refuses.
    issuer = CurrentIssuer((court.issued.record,), revoke_on_call=3)
    restores = _count_restores(monkeypatch)
    calls, factory = _counted_source(court.bundle)
    with pytest.raises(WorkloadAdmissionError):
        _resume(court, issuer, court.completed_checkpoint, factory)
    assert calls["count"] == 0
    assert restores["count"] >= 1

    # PARTIAL and ABSENT: revoke after source open, before publication.
    for fate in ("partial", "absent"):
        issuer = CurrentIssuer((court.issued.record,))
        calls, factory = _counted_source(
            court.bundle, after_open=lambda: issuer.revoke(),
        )
        with pytest.raises(WorkloadAdmissionError):
            _resume(court, issuer, _checkpoints(court)[fate], factory)
        assert calls["count"] == 1


def test_d07_final_publication_recheck_covers_earlier_completed_result(court):
    second = _variant_issued(
        court.issued,
        decision_ref=ExactRef(
            "TEST_ONLY_DECISION", "urn:test:s1d:multi-second", "7" * 64,
        ),
    )
    counting = CurrentIssuer((court.issued.record, second.record))
    calls, factory = _counted_source(court.bundle)
    first_run = resume_joined_workloads(
        workloads=(court.issued, second), resolver=counting, source_factory=factory,
        host=HOST, purpose=PURPOSE, checkpoint=court.completed_checkpoint,
        expected_checkpoint_ref=court.completed_checkpoint.checkpoint_hash,
        allow_test_only=True,
    )
    assert len(first_run.completed_results) == 1
    assert len(first_run.resumed_results) == 1
    assert calls["count"] == 1
    total_reads = counting.calls
    assert total_reads > 0

    changed = replace(
        second.record,
        source_permission_ref=ExactRef(
            "TEST_ONLY_SOURCE_PERMISSION", "urn:test:s1d:sp:final", "6" * 64,
        ),
    )
    final_issuer = CurrentIssuer(
        (court.issued.record, second.record),
        change_on_call=total_reads, changed=changed,
    )
    calls, factory = _counted_source(court.bundle)
    with pytest.raises(
        WorkloadAdmissionError, match="ISSUER_SNAPSHOT_CHANGED_BEFORE_PUBLICATION"
    ):
        resume_joined_workloads(
            workloads=(court.issued, second), resolver=final_issuer,
            source_factory=factory, host=HOST, purpose=PURPOSE,
            checkpoint=court.completed_checkpoint,
            expected_checkpoint_ref=court.completed_checkpoint.checkpoint_hash,
            allow_test_only=True,
        )
    assert calls["count"] == 1
    assert final_issuer.calls == total_reads


# D08 ---------------------------------------------------------------------
def test_d08_retry_checkpoint_conservation_and_no_authority_cache(
    court, monkeypatch,
):
    material = json.dumps(court.partial_checkpoint.material(), sort_keys=True)
    assert "CURRENT_GRANTED" not in material
    assert "REVOKED" not in material
    assert "currentness" not in material
    assert "source_permission_ref" not in material
    assert "scientific_permission_refs" not in material

    issuer = CurrentIssuer((court.issued.record,))
    issuer.revoke()
    calls, factory = _counted_source(court.bundle)
    with pytest.raises(WorkloadAdmissionError):
        _resume(court, issuer, court.partial_checkpoint, factory)
    assert calls["count"] == 0

    issuer.restore()
    calls, factory = _counted_source(court.bundle)
    retried = _resume(court, issuer, court.partial_checkpoint, factory)
    assert calls["count"] == 1
    assert _ref_keys(retried.output_refs) == _ref_keys(court.full.output_refs)
    final = retried.resumed_results[0]
    assert len(final.receipts) == 2
    assert all(receipt.state == "COMPLETED" for receipt in final.receipts)


def test_d08_prior_output_injection_refused(court):
    entry = court.partial_checkpoint.entries[0]
    prior_receipts = tuple(
        issued_module._restore_receipt(row) for row in entry.receipt_materials
    )
    prior_outputs = {
        unit_hash: issued_module._restore_output_material(row)
        for unit_hash, row in entry.completed_outputs.items()
    }
    unit_hash = next(iter(prior_outputs))
    poisoned = replace(prior_outputs[unit_hash], facts=())
    issuer = CurrentIssuer((court.issued.record,))
    calls, factory = _counted_source(court.bundle)
    with pytest.raises(
        WorkloadAdmissionError, match="PRIOR_OUTPUT_RECEIPT_MISMATCH"
    ):
        _execute(
            court, issuer, factory,
            prior_receipts=prior_receipts,
            prior_outputs={unit_hash: poisoned},
        )
    assert calls["count"] == 1


def test_d08_prior_output_without_receipt_refused(court):
    entry = court.partial_checkpoint.entries[0]
    prior_outputs = {
        unit_hash: issued_module._restore_output_material(row)
        for unit_hash, row in entry.completed_outputs.items()
    }
    issuer = CurrentIssuer((court.issued.record,))
    calls, factory = _counted_source(court.bundle)
    with pytest.raises(
        WorkloadAdmissionError, match="PRIOR_OUTPUT_WITHOUT_COMPLETED_RECEIPT"
    ):
        _execute(court, issuer, factory, prior_outputs=prior_outputs)
    assert calls["count"] == 1


def test_d08_cold_fresh_process_partial_resume(court, tmp_path):
    checkpoint_path = tmp_path / "s1d-partial-checkpoint.json"
    checkpoint_path.write_text(
        json.dumps(court.partial_checkpoint.material(), sort_keys=True)
    )
    code = """
import json, sys
from pathlib import Path
from rawlsing_next.pre553_issued_workload import (
    admit, restore_joined_checkpoint, resume_joined_workloads,
)
from rawlsing_next.tests.test_universal_source_projection import load_s3
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import (
    CurrentIssuer, _build_multi_unit_issued,
)
bundle = load_s3(Path(sys.argv[1]))
issued = _build_multi_unit_issued(
    bundle, as_of=sys.argv[3], host=sys.argv[4], purpose=sys.argv[5])
issuer = CurrentIssuer((issued.record,))
def guard(_refs):
    admit(issued.workload, issuer, host=sys.argv[4], purpose=sys.argv[5],
          allow_test_only=True)
checkpoint = restore_joined_checkpoint(
    json.loads(Path(sys.argv[2]).read_text()),
    expected_checkpoint_ref=sys.argv[6], current_guard=guard)
result = resume_joined_workloads(
    workloads=(issued,), resolver=issuer,
    source_factory=lambda _ref: bundle.physical_stream,
    host=sys.argv[4], purpose=sys.argv[5], checkpoint=checkpoint,
    expected_checkpoint_ref=sys.argv[6], allow_test_only=True)
print(json.dumps({
    "completed": len(result.completed_results),
    "resumed": len(result.resumed_results),
    "output_refs": [ref.as_dict() for ref in result.output_refs],
}, sort_keys=True))
"""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-c", code, str(court.path),
         str(checkpoint_path), AS_OF, HOST, PURPOSE,
         court.partial_checkpoint.checkpoint_hash],
        cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-2000:]
    child = json.loads(proc.stdout)
    assert child["completed"] == 0
    assert child["resumed"] == 1
    assert sorted(
        (ref["kind"], ref["object_id"], ref["content_hash"])
        for ref in child["output_refs"]
    ) == sorted(
        (ref.kind, ref.object_id, ref.content_hash)
        for ref in court.full.output_refs
    )


# D09 ---------------------------------------------------------------------
def test_d09_existing_issued_native_first_reader_parity(court):
    full = court.full
    assert len(full.native_outputs) == 2
    assert len(full.receipts) == 2
    assert all(receipt.state == "COMPLETED" for receipt in full.receipts)
    full_facts = {
        unit_hash: tuple(sorted(fact.ref.key for fact in output.facts))
        for unit_hash, output in full.outputs_by_unit.items()
    }
    for fate, checkpoint in _checkpoints(court).items():
        issuer = CurrentIssuer((court.issued.record,))
        calls, factory = _counted_source(court.bundle)
        result = _resume(court, issuer, checkpoint, factory)
        assert _ref_keys(result.output_refs) == _ref_keys(full.output_refs), fate
        results = tuple(result.all_results)
        assert len(results) == 1
        native = results[0]
        assert native.manifest.manifest_hash == full.manifest.manifest_hash, fate
        assert native.envelope_sha256 == full.envelope_sha256, fate
        assert native.decision_ref == full.decision_ref, fate
        observed = {
            unit_hash: tuple(sorted(fact.ref.key for fact in output.facts))
            for unit_hash, output in native.outputs_by_unit.items()
        }
        assert observed == full_facts, fate
        assert calls["count"] == (0 if fate == "completed" else 1), fate
