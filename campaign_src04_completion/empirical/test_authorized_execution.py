"""Focused tests for human grant authentication and issuer preflight."""
from __future__ import annotations

from dataclasses import replace
import copyreg
import json
import pickle
from pathlib import Path
import types

import pytest

from campaign_src04_completion.empirical.authorized_execution import (
    AuthorizedExecutionRefusal,
    authenticate_fixture_grant,
    authenticate_grant,
    execute_issued,
    issue_authorized_execution,
    issue_fixture_execution,
    preflight,
)
from campaign_src04_completion.empirical.actual_carrier import (
    ActualCarrierRefusal,
    load_actual_carrier_release,
)
from campaign_src04_completion.empirical.consumer_bridge import consume_with_lane_d
from campaign_src04_completion.empirical.native_workload import WorkloadPolicy
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.pre553_observed_response import ObservedResponseContract
from rawlsing_next.source_configuration.factory import build_validated_c11_release_from_config
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.schema import load_source_config
from rawlsing_next.tests.test_observed_response import _Context

ROOT = Path(__file__).resolve().parents[2]
EMPIRICAL = ROOT / "campaign_src04_completion/empirical"
GRANT = EMPIRICAL / "USER_EMPIRICAL_GRANT.json"
SCOPE = EMPIRICAL / "SCOPE_LEDGER_V2.json"
CONTRACT = EMPIRICAL / "CONTRACT_APPROVAL_READY_V2.json"
FIXTURE_CONFIG = ROOT / "source_pre553_validation/SRC04/fixture.config.json"
FIXTURE = ROOT / "source_pre553_validation/SRC04/fixture.json"


def _contract():
    return ObservedResponseContract.from_mapping(
        json.loads(CONTRACT.read_text(encoding="utf-8"))["contract"])


def test_human_grant_authenticates_exact_sha_and_scope():
    grant = authenticate_grant(GRANT)
    assert grant.sha256 == "757ee9e0eddd933b9d23d9cb84450e0dafabd8b1b6a1ad7e737d433b32c0130f"
    assert grant.ref.kind == "USER_EMPIRICAL_GRANT"
    assert grant.document["decision"] == "ALLOW_WITHIN_EXACT_SCOPE"
    assert "UNARY_OBSERVED_DISTRIBUTION" in grant.document["scope"]["methods"]


def test_wrong_grant_sha_is_refused():
    with pytest.raises(AuthorizedExecutionRefusal, match="GRANT_SHA256_MISMATCH"):
        authenticate_grant(GRANT, "0" * 64)


def test_preflight_authenticates_grant_and_keeps_release_input_pending():
    grant = authenticate_grant(GRANT)
    scope = json.loads(SCOPE.read_text(encoding="utf-8"))
    result = preflight(grant=grant, pending_contract=_contract(), scope=scope)
    assert result["status"] == "AUTHENTICATED_GRANT_ISSUER_READY__RELEASE_INPUT_PENDING"
    assert result["grant"]["sha256"] == grant.sha256
    assert result["release_input_required"]["source_sha256"] == (
        "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
    )
    assert result["original_workload_issued"] is False


def test_fixture_release_cannot_be_issued_as_original():
    config = load_source_config(FIXTURE_CONFIG)
    stream = load_fixture_stream(FIXTURE)
    release = build_validated_c11_release_from_config(config, stream=stream)
    with pytest.raises(AuthorizedExecutionRefusal, match="RELEASE_SOURCE_IDENTITY_MISMATCH"):
        issue_authorized_execution(
            grant=authenticate_grant(GRANT),
            release=release,
            pending_contract=_contract(),
            policy=WorkloadPolicy.from_mapping(
                json.loads(SCOPE.read_text(encoding="utf-8"))["workload_policy"]),
        )


def test_source_literal_contract_material_round_trips_without_changing_old_contract():
    contract = _contract()
    old_ref = contract.ref
    literal_ref = AuthorityRef("SRC04-USER-SOURCE-LITERAL", "1.0.0", "1" * 64)
    event_ref = AuthorityRef("SRC04-HISTORICAL-EVENT", "1.0.0", "2" * 64)
    authorized = replace(
        contract,
        source_literal_authority_ref=literal_ref,
        source_literal_operation="OBSERVED_RESPONSE_SOURCE_LITERAL_BINDING@1.0.0",
        source_event_authority_refs=(event_ref,),
    )
    assert authorized.ref != old_ref
    roundtrip = ObservedResponseContract.from_mapping(authorized.as_dict())
    assert roundtrip.ref == authorized.ref
    assert contract.ref == old_ref


def _write_pickle_stream(path, values):
    count = 0
    with path.open("wb") as handle:
        for value in values:
            pickle.dump(value, handle, protocol=pickle.HIGHEST_PROTOCOL)
            count += 1
    return count


def _write_actual_bundle(tmp_path, release, source_sha):
    copyreg.pickle(types.MappingProxyType, lambda mapping: (dict, (dict(mapping),)))
    public = tmp_path / "public_objects.pkl"
    internal = tmp_path / "internal_records.pkl"
    public_count = _write_pickle_stream(public, release.public_objects)
    internal_count = _write_pickle_stream(internal, release.internal_records)
    replay = tmp_path / "replay_manifest.json"
    replay.write_text(json.dumps(release.replay_manifest.as_dict(), indent=2) + "\n", encoding="utf-8")
    import hashlib
    sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
    local = {
        "schema": "PYAT_SRC04_FULL_LOCAL_RELEASE@1.0.0",
        "bundle_id": "TEST-ACTUAL-CARRIER",
        "runtime_scope": "LOCAL_FILESYSTEM_OUTSIDE_GIT",
        "source_id": "SRC04",
        "source_sha256": source_sha,
        "release_ref": release.release_ref.as_dict(),
        "semantic_release_hash": release.semantic_release_hash,
        "source_release_manifest_hash": release.source_release_manifest_hash,
        "source_artifact_ref": release.source_artifact_ref.as_dict(),
        "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
        "selected_response_slots": [1],
        "selected_coordinate_slots": [1],
        "response_positions": 8,
        "public_objects": {"file": public.name, "lines": public_count, "bytes": public.stat().st_size, "sha256": sha(public)},
        "internal_records": {"file": internal.name, "lines": internal_count, "bytes": internal.stat().st_size, "sha256": sha(internal)},
        "replay_manifest": {"file": replay.name, "sha256": sha(replay)},
        "local_only": True,
        "raw_respondent_cells_committed": False,
    }
    local_path = tmp_path / "receipt.json"
    local_path.write_text(json.dumps(local), encoding="utf-8")
    release_receipt = {
        "schema": "PYAT_SRC04_FULL_RELEASE_RECEIPT@1.0.0",
        "source_id": "SRC04", "source_sha256": source_sha,
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
    primary = {"schema": "PYAT_SRC04_FULL_PRIMARY_RUN@1.0.0", "status": "FULL_PRIMARY_COMPLETE"}
    primary_path = tmp_path / "primary.json"
    primary_path.write_text(json.dumps(primary), encoding="utf-8")
    return local_path, release_path, primary_path, public, internal


def test_actual_carrier_receipt_adapter_rehydrates_native_fixture_release(tmp_path):
    config = load_source_config(FIXTURE_CONFIG)
    stream = load_fixture_stream(FIXTURE)
    release = build_validated_c11_release_from_config(config, stream=stream)
    local_path, release_path, primary_path, _, _ = _write_actual_bundle(
        tmp_path, release, stream.source_sha256)
    reopened = load_actual_carrier_release(
        local_receipt_path=tmp_path / "receipt.json",
        release_receipt_path=tmp_path / "release_receipt.json",
        primary_run_path=tmp_path / "primary.json",
        bundle_dir=tmp_path,
        expected_source_sha256=stream.source_sha256,
    )
    assert reopened.release_ref == release.release_ref
    assert reopened.source_artifact_ref.content_hash == stream.source_sha256
    assert len(reopened.public_objects) == len(release.public_objects)
    assert len(reopened.internal_records) == len(release.internal_records)


def test_actual_carrier_receipt_adapter_rejects_mutated_stream(tmp_path):
    config = load_source_config(FIXTURE_CONFIG)
    stream = load_fixture_stream(FIXTURE)
    release = build_validated_c11_release_from_config(config, stream=stream)
    _, _, _, public, _ = _write_actual_bundle(tmp_path, release, stream.source_sha256)
    data = bytearray(public.read_bytes())
    data[-1] ^= 0xFF
    public.write_bytes(bytes(data))
    with pytest.raises(ActualCarrierRefusal, match="PUBLIC_OBJECTS_SHA_MISMATCH"):
        load_actual_carrier_release(
            local_receipt_path=tmp_path / "receipt.json",
            release_receipt_path=tmp_path / "release_receipt.json",
            primary_run_path=tmp_path / "primary.json",
            bundle_dir=tmp_path,
            expected_source_sha256=stream.source_sha256,
        )


def test_actual_carrier_fixture_issuer_executor_and_lane_d_end_to_end(tmp_path):
    config = load_source_config(FIXTURE_CONFIG)
    stream = load_fixture_stream(FIXTURE)
    release = build_validated_c11_release_from_config(config, stream=stream)
    local_path, release_path, primary_path, _, _ = _write_actual_bundle(
        tmp_path, release, stream.source_sha256)
    reopened = load_actual_carrier_release(
        local_receipt_path=local_path,
        release_receipt_path=release_path,
        primary_run_path=primary_path,
        bundle_dir=tmp_path,
        expected_source_sha256=stream.source_sha256,
        local_receipt_sha256=__import__("hashlib").sha256(local_path.read_bytes()).hexdigest(),
        release_receipt_sha256=__import__("hashlib").sha256(release_path.read_bytes()).hexdigest(),
        primary_run_sha256=__import__("hashlib").sha256(primary_path.read_bytes()).hexdigest(),
    )
    context = _Context()
    grant = authenticate_fixture_grant()
    policy = WorkloadPolicy.from_mapping(
        json.loads(SCOPE.read_text(encoding="utf-8"))["workload_policy"])
    issued = issue_fixture_execution(
        fixture_grant=grant,
        release=reopened,
        pending_contract=context.contract,
        policy=policy,
    )
    workload = execute_issued(issued)
    assert issued.fixture_only is True
    assert workload.accounting["executed_operations"] == 44
    assert workload.accounting["refused_operations"] == 0
    assert workload.accounting["operations_by_family"] == {
        "UNARY_OBSERVED_DISTRIBUTION": 3,
        "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION": 38,
        "SAME_RESPONDENT_JOINT_DISTRIBUTION": 3,
    }
    result = consume_with_lane_d(grant=grant, issued=issued, workload=workload)
    assert result.status == "FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE"
    assert result.product is not None
    assert result.product["fixture_only"] is True
    assert result.product["downstream_value_effect"] == "SUBSTANTIVE_DISCOVERY_RESULT_SUPPORTED"
    assert result.product["observed_response"]["status"] == "OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION"
    assert result.product["observed_response"]["ledger"]["not_eligible_population_estimate"] is True


def test_actual_carrier_missing_malformed_and_truncated_refusals(tmp_path):
    config = load_source_config(FIXTURE_CONFIG)
    stream = load_fixture_stream(FIXTURE)
    release = build_validated_c11_release_from_config(config, stream=stream)
    local_path, release_path, primary_path, public, _ = _write_actual_bundle(
        tmp_path, release, stream.source_sha256)
    missing = tmp_path / "missing_receipt.json"
    with pytest.raises(ActualCarrierRefusal) as exc:
        load_actual_carrier_release(
            local_receipt_path=missing,
            release_receipt_path=release_path,
            primary_run_path=primary_path,
            bundle_dir=tmp_path,
            expected_source_sha256=stream.source_sha256,
            local_receipt_sha256="0" * 64,
        )
    assert exc.value.code == "CARRIER_FILE_UNREADABLE"

    for name, payload in (("malformed.pkl", b"not-a-pickle"), ("truncated.pkl", public.read_bytes()[:8])):
        bad = tmp_path / name
        bad.write_bytes(payload)
        local = json.loads(local_path.read_text(encoding="utf-8"))
        local["public_objects"].update({
            "file": bad.name,
            "lines": 1,
            "bytes": bad.stat().st_size,
            "sha256": __import__("hashlib").sha256(bad.read_bytes()).hexdigest(),
        })
        local_path.write_text(json.dumps(local), encoding="utf-8")
        with pytest.raises(ActualCarrierRefusal) as exc:
            load_actual_carrier_release(
                local_receipt_path=local_path,
                release_receipt_path=release_path,
                primary_run_path=primary_path,
                bundle_dir=tmp_path,
                expected_source_sha256=stream.source_sha256,
            )
        assert exc.value.code in {"CARRIER_STREAM_UNREADABLE", "CARRIER_STREAM_FILE_UNREADABLE"}


def test_consumer_bridge_reports_dependency_pending_when_lane_d_not_joined():
    try:
        import campaign_src04_completion.consumers.consumer  # noqa: F401
    except Exception:
        joined = False
    else:
        joined = True
    if joined:
        pytest.skip("Lane D dependency is joined; the bridge executes against a real bundle")
    result = consume_with_lane_d(
        grant=authenticate_grant(GRANT),
        issued=None,  # type: ignore[arg-type]
        workload=None,  # type: ignore[arg-type]
    )
    assert result.status == "D_CONSUMER_DEPENDENCY_NOT_JOINED"
    assert result.product is None
