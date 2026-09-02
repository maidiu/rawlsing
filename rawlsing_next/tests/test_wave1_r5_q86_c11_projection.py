from dataclasses import replace
import hashlib

import pytest

from rawlsing_next.pre553_empirical_objects import RespondentEvent
from rawlsing_next.pre553_source_backed_c11_facade import (
    SourceBackedC11FacadeError,
    build_validated_source_backed_c11_release_from_stream,
)
from rawlsing_next.wave1_r5_q86_c11_projection import (
    FROZEN_BINDINGS,
    R5Q86GovernedRow,
    R5Q86ProjectionError,
    _build,
    domain_ref,
    projection_identity_ref,
    q86_target_domain,
    validate_frozen_bindings,
)


def _h(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _tiny_contract():
    return replace(
        FROZEN_BINDINGS,
        source_artifact_id="fixture:r5-q86",
        source_sha256=_h("fixture-source"),
        source_row_count=2,
        respondent_carrier_id="FIXTURE_RESPONDENT_CARRIER@1",
        respondent_carrier_sha256=_h("fixture-respondent"),
        response_fact_carrier_sha256=_h("fixture-response"),
        exposure_fact_carrier_sha256=_h("fixture-exposure"),
        risk_set_id="FIXTURE_COMMON_RISK_SET@1",
        risk_set_row_count=1,
        risk_set_member_set_sha256=_h("fixture-risk"),
        source_structure_id="fixture-source-structure",
        source_structure_sha256=_h("fixture-structure"),
        codebook_sha256=_h("fixture-codebook"),
    )


def _rows(*, bad_exposure: bool = False):
    return (
        R5Q86GovernedRow(
            row_ordinal=1,
            country_native="KEN",
            respno="1",
            country_alpha3="KEN",
            q86a_raw_value="1",
            q86a_response_state="SUBSTANTIVE_RESPONSE",
            q86a_exposure_state="NOT_EXPOSED__PROVED" if bad_exposure else "EXPOSED__PROVED",
            q86b_raw_value="0",
            q86b_response_state="SUBSTANTIVE_RESPONSE",
            q86b_exposure_state="EXPOSED__PROVED",
        ),
        R5Q86GovernedRow(
            row_ordinal=2,
            country_native="EGY",
            respno="2",
            country_alpha3="EGY",
            q86a_raw_value="9",
            q86a_response_state="DK",
            q86a_exposure_state="NOT_EXPOSED__PROVED",
            q86b_raw_value="998",
            q86b_response_state="REFUSAL",
            q86b_exposure_state="NOT_EXPOSED__PROVED",
        ),
    )


def test_frozen_source_and_risk_set_tamper_fail_closed():
    assert validate_frozen_bindings(FROZEN_BINDINGS) is FROZEN_BINDINGS
    with pytest.raises(R5Q86ProjectionError, match="differs from frozen"):
        validate_frozen_bindings(replace(FROZEN_BINDINGS, source_sha256=_h("wrong-source")))
    with pytest.raises(R5Q86ProjectionError, match="differs from frozen"):
        validate_frozen_bindings(
            replace(FROZEN_BINDINGS, risk_set_member_set_sha256=_h("wrong-risk"))
        )


def test_source_native_domain_is_exact_and_administrative_states_are_not_dropped():
    for variable in ("Q86A", "Q86B"):
        domain = q86_target_domain(variable)
        assert tuple(row["code"] for row in domain) == ("0", "1", "9", "997", "998", "-1")
        assert {row["code"]: row["response_state"] for row in domain} == {
            "0": "SUBSTANTIVE_RESPONSE",
            "1": "SUBSTANTIVE_RESPONSE",
            "9": "DK",
            "997": "NOT_ASKED",
            "998": "REFUSAL",
            "-1": "MISSING",
        }
    assert domain_ref("Q86A") != domain_ref("Q86B")

    with pytest.raises(R5Q86ProjectionError, match="outside frozen source-native domain"):
        replace(_rows()[0], q86a_raw_value="2")
    with pytest.raises(R5Q86ProjectionError, match="does not match frozen code"):
        replace(_rows()[0], q86a_raw_value="9", q86a_response_state="SUBSTANTIVE_RESPONSE")


def test_response_presence_is_never_substituted_for_exposure():
    # A substantive response on a risk-set-country row does not prove exposure.
    with pytest.raises(R5Q86ProjectionError, match="independent EXPOSED__PROVED"):
        _build(_rows(bad_exposure=True), _tiny_contract())


def test_missing_required_authority_fails_at_projection_constructor():
    package = _build(_rows(), _tiny_contract())
    with pytest.raises(SourceBackedC11FacadeError, match="required authority absent"):
        replace(
            package.projection,
            authority_snapshots=package.projection.authority_snapshots[:-1],
        )


def test_projection_and_validated_release_identity_are_deterministic_under_row_reordering():
    contract = _tiny_contract()
    first = _build(_rows(), contract)
    second = _build(tuple(reversed(_rows())), contract)

    assert first.projection.projection_identity_ref == second.projection.projection_identity_ref
    assert projection_identity_ref(contract) == projection_identity_ref(contract)

    release_a = build_validated_source_backed_c11_release_from_stream(first.stream, first.projection)
    release_b = build_validated_source_backed_c11_release_from_stream(second.stream, second.projection)
    assert release_a.release_ref == release_b.release_ref
    assert release_a.replay_manifest.ref == release_b.replay_manifest.ref

    events = [obj for obj in release_a.public_objects if isinstance(obj, RespondentEvent)]
    assert len(events) == 4
    assert {event.typed_state for event in events} == {"SUBSTANTIVE_RESPONSE", "DK", "REFUSAL"}
    assert first.q86a_target_domain_replay_ref != first.q86b_target_domain_replay_ref
