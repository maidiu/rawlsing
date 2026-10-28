"""Independent changed issuer/actual-carrier review tests.

Fixture-only; no original SRC04 source or original product is opened.  Tests
record the candidate's current behavior.  Tests whose names end in ``_DEFECT``
assert the observed failure so the review return can identify an exact unmet
requirement without editing author code.
"""
from __future__ import annotations

from copy import deepcopy
import copyreg
import hashlib
import json
from pathlib import Path
import pickle
import types

import pytest

from campaign_src04_completion.empirical.actual_carrier import (
    ActualCarrierRefusal,
    load_actual_carrier_release,
)
from campaign_src04_completion.empirical.authorized_execution import (
    AuthorizedExecutionRefusal,
    _topology_valid_targets,
    authenticate_grant,
    issue_authorized_execution,
)
from campaign_src04_completion.empirical.native_workload import (
    WorkloadPolicy,
    build_native_workload,
    execute_native_workload,
)
from rawlsing_next.tests.test_observed_response import _Context
from rawlsing_next.source_configuration.factory import build_validated_c11_release_from_config
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.schema import load_source_config

ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = ROOT / "source_pre553_validation/SRC04/fixture.config.json"
FIXTURE_PATH = ROOT / "source_pre553_validation/SRC04/fixture.json"
GRANT_PATH = ROOT / "campaign_src04_completion/empirical/USER_EMPIRICAL_GRANT.json"
SCOPE_PATH = ROOT / "campaign_src04_completion/empirical/SCOPE_LEDGER_V2.json"
CONTRACT_PATH = ROOT / "campaign_src04_completion/empirical/CONTRACT_APPROVAL_READY_V2.json"


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _write_stream(path: Path, values) -> int:
    count = 0
    with path.open("wb") as handle:
        for value in values:
            pickle.dump(value, handle, protocol=pickle.HIGHEST_PROTOCOL)
            count += 1
    return count


def _write_bundle(tmp_path: Path, release, source_sha: str):
    """Write the actual carrier shape using only the labelled fixture release."""
    copyreg.pickle(types.MappingProxyType, lambda mapping: (dict, (dict(mapping),)))
    public = tmp_path / "public_objects.pkl"
    internal = tmp_path / "internal_records.pkl"
    public_count = _write_stream(public, release.public_objects)
    internal_count = _write_stream(internal, release.internal_records)
    replay = tmp_path / "replay_manifest.json"
    replay.write_text(json.dumps(release.replay_manifest.as_dict(), indent=2) + "\n", encoding="utf-8")
    local = {
        "schema": "PYAT_SRC04_FULL_LOCAL_RELEASE@1.0.0",
        "bundle_id": "REVIEW-FIXTURE-ACTUAL-CARRIER",
        "runtime_scope": "LOCAL_FILESYSTEM_OUTSIDE_GIT",
        "source_id": "SRC04",
        "source_sha256": source_sha,
        "release_ref": release.release_ref.as_dict(),
        "semantic_release_hash": release.semantic_release_hash,
        "source_release_manifest_hash": release.source_release_manifest_hash,
        "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
        "selected_response_slots": [1],
        "selected_coordinate_slots": [1],
        "response_positions": 8,
        "public_objects": {
            "file": public.name,
            "lines": public_count,
            "bytes": public.stat().st_size,
            "sha256": _sha(public),
        },
        "internal_records": {
            "file": internal.name,
            "lines": internal_count,
            "bytes": internal.stat().st_size,
            "sha256": _sha(internal),
        },
        "replay_manifest": {"file": replay.name, "sha256": _sha(replay)},
        "local_only": True,
        "raw_respondent_cells_committed": False,
    }
    local_path = tmp_path / "receipt.json"
    local_path.write_text(json.dumps(local), encoding="utf-8")
    release_receipt = {
        "schema": "PYAT_SRC04_FULL_RELEASE_RECEIPT@1.0.0",
        "source_id": "SRC04",
        "source_sha256": source_sha,
        "release_ref": release.release_ref.as_dict(),
        "source_release_manifest_hash": release.source_release_manifest_hash,
        "source_read_performed": True,
        "release_audit": {
            "source_artifact_sha": True,
            "semantic_hash_matches_ref": True,
            "no_canonical": True,
        },
    }
    release_path = tmp_path / "release_receipt.json"
    release_path.write_text(json.dumps(release_receipt), encoding="utf-8")
    primary_path = tmp_path / "primary.json"
    primary_path.write_text(
        json.dumps({"schema": "PYAT_SRC04_FULL_PRIMARY_RUN@1.0.0", "status": "FULL_PRIMARY_COMPLETE"}),
        encoding="utf-8",
    )
    return local_path, release_path, primary_path, public, internal


def _load(
    local_path,
    release_path,
    primary_path,
    bundle_dir,
    *,
    expected_source_sha256,
    local_receipt_sha256=None,
    release_receipt_sha256=None,
    primary_run_sha256=None,
):
    return load_actual_carrier_release(
        local_receipt_path=local_path,
        release_receipt_path=release_path,
        primary_run_path=primary_path,
        bundle_dir=bundle_dir,
        expected_source_sha256=expected_source_sha256,
        local_receipt_sha256=local_receipt_sha256,
        release_receipt_sha256=release_receipt_sha256,
        primary_run_sha256=primary_run_sha256,
    )


@pytest.fixture(scope="module")
def fixture_material():
    config = load_source_config(CONFIG_PATH)
    stream = load_fixture_stream(FIXTURE_PATH)
    release = build_validated_c11_release_from_config(config, stream=stream)
    return config, stream, release


def test_fixture_carrier_adapter_rehydrates_native_release(tmp_path, fixture_material):
    _, stream, release = fixture_material
    paths = _write_bundle(tmp_path, release, stream.source_sha256)
    reopened = _load(*paths[:3], tmp_path, expected_source_sha256=stream.source_sha256)
    assert reopened.release_ref == release.release_ref
    assert reopened.source_artifact_ref.content_hash == stream.source_sha256
    assert len(reopened.public_objects) == len(release.public_objects)
    assert len(reopened.internal_records) == len(release.internal_records)


def test_required_fixture_issuer_executor_path_is_refused_DEFECT(tmp_path, fixture_material):
    """The commission requires the labelled fixture through issuer/executor/D."""
    _, stream, release = fixture_material
    paths = _write_bundle(tmp_path, release, stream.source_sha256)
    reopened = _load(*paths[:3], tmp_path, expected_source_sha256=stream.source_sha256)
    context = _Context()
    grant = authenticate_grant(GRANT_PATH)
    scope = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))
    policy = WorkloadPolicy.from_mapping(scope["workload_policy"])
    with pytest.raises(AuthorizedExecutionRefusal) as exc:
        issue_authorized_execution(
            grant=grant,
            release=reopened,
            pending_contract=context.contract,
            policy=policy,
        )
    # Current failure: the issuer only accepts original source identity/7,337
    # respondents, so the required fixture issuer/executor/D path cannot start.
    assert exc.value.code == "RELEASE_SOURCE_IDENTITY_MISMATCH"


def test_fixture_source_literal_topology_has_no_qualified_targets_DEFECT():
    context = _Context()
    with pytest.raises(AuthorizedExecutionRefusal) as exc:
        _topology_valid_targets(context.release, context.contract)
    assert exc.value.code == "NO_SOURCE_QUALIFIED_TARGETS"
    # The labelled fixture does not provide a source-literal projection that the
    # new issuer can qualify; it therefore produces no source-qualified target.
    events = [obj for obj in context.release.public_objects if obj.schema_id == "RespondentEvent"]
    assert events


def test_malformed_pickle_is_untyped_DEFECT(tmp_path, fixture_material):
    _, stream, release = fixture_material
    local_path, release_path, primary_path, public, _ = _write_bundle(
        tmp_path, release, stream.source_sha256
    )
    bad = tmp_path / "public_bad.pkl"
    bad.write_bytes(b"not-a-pickle")
    local = json.loads(local_path.read_text(encoding="utf-8"))
    local["public_objects"].update({
        "file": bad.name,
        "lines": 1,
        "bytes": bad.stat().st_size,
        "sha256": _sha(bad),
    })
    local_path.write_text(json.dumps(local), encoding="utf-8")
    with pytest.raises(Exception) as exc:
        _load(local_path, release_path, primary_path, tmp_path,
              expected_source_sha256=stream.source_sha256)
    assert not isinstance(exc.value, ActualCarrierRefusal)
    assert isinstance(exc.value, pickle.UnpicklingError)


def test_truncated_pickle_is_untyped_DEFECT(tmp_path, fixture_material):
    _, stream, release = fixture_material
    local_path, release_path, primary_path, public, _ = _write_bundle(
        tmp_path, release, stream.source_sha256
    )
    bad = tmp_path / "public_truncated.pkl"
    data = public.read_bytes()
    bad.write_bytes(data[:max(1, len(data) // 2)])
    local = json.loads(local_path.read_text(encoding="utf-8"))
    local["public_objects"].update({
        "file": bad.name,
        "lines": 1,
        "bytes": bad.stat().st_size,
        "sha256": _sha(bad),
    })
    local_path.write_text(json.dumps(local), encoding="utf-8")
    with pytest.raises(Exception) as exc:
        _load(local_path, release_path, primary_path, tmp_path,
              expected_source_sha256=stream.source_sha256)
    assert not isinstance(exc.value, ActualCarrierRefusal)
    assert isinstance(exc.value, pickle.UnpicklingError)


def test_missing_receipt_with_pin_is_untyped_DEFECT(tmp_path, fixture_material):
    _, stream, release = fixture_material
    _, release_path, primary_path, _, _ = _write_bundle(tmp_path, release, stream.source_sha256)
    missing = tmp_path / "missing_receipt.json"
    with pytest.raises(Exception) as exc:
        _load(missing, release_path, primary_path, tmp_path,
              expected_source_sha256=stream.source_sha256,
              local_receipt_sha256="0" * 64)
    assert not isinstance(exc.value, ActualCarrierRefusal)
    assert isinstance(exc.value, FileNotFoundError)


def test_receipt_pin_source_and_manifest_refusals_are_typed(tmp_path, fixture_material):
    _, stream, release = fixture_material
    local_path, release_path, primary_path, public, _ = _write_bundle(
        tmp_path, release, stream.source_sha256
    )
    with pytest.raises(ActualCarrierRefusal) as exc:
        _load(local_path, release_path, primary_path, tmp_path,
              expected_source_sha256=stream.source_sha256, local_receipt_sha256="0" * 64)
    assert exc.value.code == "LOCAL_RECEIPT_SHA256_MISMATCH"

    with pytest.raises(ActualCarrierRefusal) as exc:
        _load(local_path, release_path, primary_path, tmp_path,
              expected_source_sha256="2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18")
    assert exc.value.code == "LOCAL_SOURCE_MISMATCH"

    data = bytearray(public.read_bytes())
    data[-1] ^= 0xFF
    public.write_bytes(bytes(data))
    with pytest.raises(ActualCarrierRefusal) as exc:
        _load(local_path, release_path, primary_path, tmp_path,
              expected_source_sha256=stream.source_sha256)
    assert exc.value.code == "LOCAL_RECEIPT_PUBLIC_OBJECTS_SHA_MISMATCH"

    malformed = tmp_path / "malformed.json"
    malformed.write_text("{not-json", encoding="utf-8")
    with pytest.raises(ActualCarrierRefusal) as exc:
        _load(malformed, release_path, primary_path, tmp_path,
              expected_source_sha256=stream.source_sha256,
              local_receipt_sha256=_sha(malformed))
    assert exc.value.code == "ACTUAL_RECEIPT_UNREADABLE"


def test_grant_authentication_and_wrong_grant_sha_refuse():
    grant = authenticate_grant(GRANT_PATH)
    assert grant.sha256 == "757ee9e0eddd933b9d23d9cb84450e0dafabd8b1b6a1ad7e737d433b32c0130f"
    with pytest.raises(AuthorizedExecutionRefusal) as exc:
        authenticate_grant(GRANT_PATH, "0" * 64)
    assert exc.value.code == "GRANT_SHA256_MISMATCH"


def test_changed_native_condition_counts_remain_executable():
    context = _Context()
    scope = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))
    policy = WorkloadPolicy.from_mapping(scope["workload_policy"])
    workload = build_native_workload(
        repository=context.repository,
        release_ref=context.release.release_ref,
        contract=context.contract,
        policy=policy,
    )
    executed = execute_native_workload(
        repository=context.repository,
        release_ref=context.release.release_ref,
        contract=context.contract,
        authority_registry=context.registry,
        policy=policy,
    )
    assert len(workload.operations) == 44
    assert executed.accounting["executed_operations"] == 44
    assert executed.accounting["refused_operations"] == 0
    conditional = [
        operation for operation in executed.operations
        if operation.family == "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION"
    ]
    assert len(conditional) == 38
    assert all(
        operation.condition_counts is not None
        and operation.condition_counts["condition_true"] >= 0
        and operation.observed_ledger is not None
        and operation.observed_ledger["condition_unobserved"]
        == operation.condition_counts["condition_unobserved"]
        and operation.observed_ledger["condition_false"]
        == operation.condition_counts["condition_false"]
        for operation in conditional
    )


def test_accepted_d_dependency_is_present_and_exact():
    import campaign_src04_completion.consumers.consumer as accepted_d

    assert _sha(Path(accepted_d.__file__)) == (
        "728fbc9a09291ae9c9d578fbed7641acd4499a2ff4158b7588e1cc5afa18f8ae"
    )
