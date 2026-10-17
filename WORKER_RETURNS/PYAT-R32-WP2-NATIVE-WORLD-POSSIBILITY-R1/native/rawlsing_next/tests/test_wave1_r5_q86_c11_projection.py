from dataclasses import replace
import hashlib

import pytest

from rawlsing_next.pre553_empirical_objects import RespondentEvent, semantic_hash
from rawlsing_next.pre553_source_backed_c11_facade import (
    SourceBackedC11FacadeError,
    build_validated_source_backed_c11_release_from_stream,
    project_c11_candidate_from_physical_cells,
)
from rawlsing_next.pre553_c11_ingest import (
    _candidate_projection, _candidate_projection_semantic_hash,
)
from rawlsing_next.wave1_r5_q86_c11_projection import (
    FROZEN_BINDINGS,
    R5Q86GovernedRow,
    R5Q86ProjectionError,
    R5Q86RiskSetMember,
    _build,
    _validate_claim_scope,
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
            respondent_local_id="sha256:" + _h("respondent-ken-1"),
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
            respondent_local_id="sha256:" + _h("respondent-egy-2"),
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
    for field in (
        "respondent_carrier_sha256",
        "response_fact_carrier_sha256",
        "exposure_fact_carrier_sha256",
    ):
        with pytest.raises(R5Q86ProjectionError, match="differs from frozen"):
            validate_frozen_bindings(
                replace(FROZEN_BINDINGS, **{field: _h("wrong-" + field)})
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


def _risk_member_for(row):
    return R5Q86RiskSetMember(
        row.country_native,
        row.respno,
        row.respondent_local_id,
        row.country_alpha3,
    )


def test_claim_scope_preserves_source_row_count_but_projects_only_exact_member_set():
    contract = _tiny_contract()
    rows = _rows()
    members = (_risk_member_for(rows[0]),)
    selected = _validate_claim_scope(
        rows, members, contract.risk_set_member_set_sha256, contract
    )
    assert contract.source_row_count == 2
    assert contract.risk_set_row_count == 1
    assert tuple(r.row_ordinal for r in selected) == (1,)

    package = _build(rows, contract, projection_rows=selected)
    assert package.stream.row_count == 1
    assert tuple(x.row_ordinal for x in package.projection.row_bindings) == (1,)
    release = build_validated_source_backed_c11_release_from_stream(
        package.stream, package.projection
    )
    assert len(release.public_objects) == 12
    assert len(release.internal_records) == 3


def test_claim_scope_member_and_source_reordering_are_semantically_inert():
    contract = _tiny_contract()
    rows = _rows()
    members = (_risk_member_for(rows[0]),)
    first_rows = _validate_claim_scope(
        rows, members, contract.risk_set_member_set_sha256, contract
    )
    second_rows = _validate_claim_scope(
        tuple(reversed(rows)),
        tuple(reversed(members)),
        contract.risk_set_member_set_sha256,
        contract,
    )
    first = _build(rows, contract, projection_rows=first_rows)
    second = _build(tuple(reversed(rows)), contract, projection_rows=second_rows)
    release_a = build_validated_source_backed_c11_release_from_stream(
        first.stream, first.projection
    )
    release_b = build_validated_source_backed_c11_release_from_stream(
        second.stream, second.projection
    )
    assert release_a.release_ref == release_b.release_ref
    assert release_a.replay_manifest.ref == release_b.replay_manifest.ref


def test_claim_scope_hash_missing_extra_duplicate_and_ref_tamper_fail_closed():
    contract = _tiny_contract()
    rows = _rows()
    member = _risk_member_for(rows[0])

    with pytest.raises(R5Q86ProjectionError, match="semantic member-set SHA"):
        _validate_claim_scope(rows, (member,), _h("tampered-risk"), contract)

    with pytest.raises(R5Q86ProjectionError, match="member count"):
        _validate_claim_scope(rows, (), contract.risk_set_member_set_sha256, contract)

    second_risk_row = replace(
        rows[1],
        country_native="BOT",
        country_alpha3="BOT",
        q86a_exposure_state="EXPOSED__PROVED",
        q86b_exposure_state="EXPOSED__PROVED",
    )
    two_risk_rows = (rows[0], second_risk_row)
    duplicate_contract = replace(contract, risk_set_row_count=2)
    second_member = _risk_member_for(second_risk_row)
    duplicate_ref_member = replace(
        second_member, respondent_local_id=member.respondent_local_id
    )
    with pytest.raises(R5Q86ProjectionError, match="duplicate exact risk-set respondent ref"):
        _validate_claim_scope(
            two_risk_rows, (member, duplicate_ref_member),
            duplicate_contract.risk_set_member_set_sha256, duplicate_contract,
        )

    duplicate_source_rows = (
        rows[0],
        replace(
            rows[1],
            country_native=rows[0].country_native,
            respno=rows[0].respno,
        ),
    )
    with pytest.raises(
        R5Q86ProjectionError, match=r"duplicate \(COUNTRY, RESPNO\) identity"
    ):
        _validate_claim_scope(
            duplicate_source_rows, (member,),
            contract.risk_set_member_set_sha256, contract,
        )

    wrong_ref = replace(member, respondent_local_id="sha256:" + _h("wrong-ref"))
    with pytest.raises(R5Q86ProjectionError, match="exact respondent ref mismatch"):
        _validate_claim_scope(
            rows, (wrong_ref,), contract.risk_set_member_set_sha256, contract
        )

    extra = _risk_member_for(rows[1])
    with pytest.raises(R5Q86ProjectionError, match="membership mismatch"):
        _validate_claim_scope(
            rows, (extra,), contract.risk_set_member_set_sha256, contract
        )


def test_claim_scoped_stream_accepts_noncontiguous_preserved_source_ordinals():
    contract = _tiny_contract()
    rows = _rows()
    # Exercise the shared facade repair directly: row_count is cardinality,
    # while exact source row ordinal 2 remains the row identity.
    package = _build(rows, contract, projection_rows=(rows[1],))
    assert package.stream.row_count == 1
    assert tuple(x.row_ordinal for x in package.projection.row_bindings) == (2,)
    release = build_validated_source_backed_c11_release_from_stream(
        package.stream, package.projection
    )
    assert release.release_ref.content_hash == release.semantic_release_hash


def test_streaming_candidate_projection_hash_is_identical_to_legacy_projection_hash():
    package = _build(_rows(), _tiny_contract())
    candidate = project_c11_candidate_from_physical_cells(
        source_sha256=package.stream.source_sha256,
        row_count=package.stream.row_count,
        cells=package.stream.iter_cells(),
        projection=package.projection,
    )
    legacy_hash = semantic_hash(_candidate_projection(candidate))
    assert _candidate_projection_semantic_hash(candidate) == legacy_hash
    assert candidate.candidate_replay_manifest.semantic_projection_hash == legacy_hash
