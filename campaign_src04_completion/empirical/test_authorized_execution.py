"""Focused tests for human grant authentication and issuer preflight."""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import pytest

from campaign_src04_completion.empirical.authorized_execution import (
    AuthorizedExecutionRefusal,
    authenticate_grant,
    issue_authorized_execution,
    preflight,
)
from campaign_src04_completion.empirical.consumer_bridge import consume_with_lane_d
from campaign_src04_completion.empirical.native_workload import WorkloadPolicy
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.pre553_observed_response import ObservedResponseContract
from rawlsing_next.source_configuration.factory import build_validated_c11_release_from_config
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.schema import load_source_config

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
