from __future__ import annotations

import pytest

from rawlsing_next.fiabc_lm2_r1e_wvs7_mapping_authority import mapping_authority_snapshot
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
from rawlsing_next.pre553_physical_native_representation import (
    PhysicalNativeRepresentationError,
    UPSTREAM_DECODER_LAW_EVIDENCE_KIND,
    VARIABLE_TYPE_EVIDENCE_KIND,
    build_representation_authority_snapshot,
    resolve_authorized_physical_binding,
    validate_representation_authority,
)
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key

SOURCE = "a" * 64
OTHER_SOURCE = "b" * 64
CODEC = R5TypedValueCodec()
SOURCE_AUTH = AuthorityRef("SYNTHETIC-SOURCE-SEMANTICS", "1.0.0", "c" * 64)
SPECIALS = {
    -5: "MISSING",
    -4: "NOT_ASKED",
    -2: "SOURCE_SPECIFIC_SPECIAL",
    -1: "DK",
}


def _ref(kind: str, label: str) -> ExactRef:
    h = semantic_hash({"kind": kind, "label": label})
    return ExactRef(kind, f"urn:test:{label}:sha256:{h}", h)


UNIVERSE = _ref("EmpiricalUniverse@1.0.0", "universe")
RISK = _ref("SyntheticRiskSet@1.0.0", "risk")
DECODER_EVIDENCE = _ref(UPSTREAM_DECODER_LAW_EVIDENCE_KIND, "decoder")
TYPE_EVIDENCE = _ref(VARIABLE_TYPE_EVIDENCE_KIND, "types")
NEGATIVE = (
    _ref("SyntheticNegativeLimit@1.0.0", "no-global-coercion"),
    _ref("SyntheticNegativeLimit@1.0.0", "no-candidate-parentage"),
)


def _row(name: str, ordinal: int, code: int, state: str):
    if code in SPECIALS:
        physical_state = PhysicalMissingState.FORMAT_USER_MISSING_RANGE.value
        declaration = {"kind": "range", "lo": -5, "hi": -1}
    else:
        physical_state = PhysicalMissingState.OBSERVED_STORAGE_VALUE.value
        declaration = None
    return {
        "source_sha256": SOURCE,
        "variable": {"ordinal": ordinal, "name": name},
        "native_code_token": CODEC.encode(code),
        "native_response_state": state,
        "decoder_value_token": CODEC.encode(float(code)),
        "physical_missing_state": physical_state,
        "source_missing_declaration": declaration,
    }


def _snapshot():
    rows = []
    for name, ordinal in (("Q291G5", 388), ("Q291P5", 394)):
        rows.extend(_row(name, ordinal, code, "SUBSTANTIVE_RESPONSE") for code in (1, 2, 3, 4, 5))
        rows.extend(_row(name, ordinal, code, state) for code, state in SPECIALS.items())
    return build_representation_authority_snapshot(
        authority_id="SYNTHETIC-Q291-PHYSICAL-NATIVE-BINDING",
        authority_version="1.0.0",
        source_sha256=SOURCE,
        source_universe_ref=UNIVERSE,
        target_use_ref="SYNTHETIC_EXACT_USE",
        predicate_or_risk_set_ref=RISK,
        source_semantics_authority_ref=SOURCE_AUTH,
        upstream_decoder_law_evidence_ref=DECODER_EVIDENCE,
        variable_type_evidence_ref=TYPE_EVIDENCE,
        exact_representation_bindings=rows,
        negative_limit_refs=NEGATIVE,
        effective_time_or_interval={"court": "R1J-C-SYNTHETIC"},
    )


def test_global_int_and_float_physical_keys_remain_distinct():
    state = PhysicalMissingState.OBSERVED_STORAGE_VALUE
    assert physical_value_binding_key(1, state) != physical_value_binding_key(1.0, state)


def test_no_generic_integral_float_coercion_exists():
    snapshot = _snapshot()
    with pytest.raises(PhysicalNativeRepresentationError, match="native code must be an exact integer"):
        resolve_authorized_physical_binding(
            snapshot,
            source_sha256=SOURCE,
            variable_ordinal=388,
            variable_name="Q291G5",
            native_code=1.0,
            native_response_state="SUBSTANTIVE_RESPONSE",
        )


def test_exact_authorized_source_variable_native_code_representation_succeeds():
    snapshot = _snapshot()
    binding = resolve_authorized_physical_binding(
        snapshot,
        source_sha256=SOURCE,
        variable_ordinal=388,
        variable_name="Q291G5",
        native_code=1,
        native_response_state="SUBSTANTIVE_RESPONSE",
    )
    assert binding.decoder_value == 1.0
    assert binding.decoder_value_token == CODEC.encode(1.0)
    assert binding.physical_key == physical_value_binding_key(
        1.0,
        PhysicalMissingState.OBSERVED_STORAGE_VALUE,
        None,
    )
    assert binding.physical_key != physical_value_binding_key(
        1,
        PhysicalMissingState.OBSERVED_STORAGE_VALUE,
        None,
    )


def test_same_representation_on_another_source_fails_closed():
    snapshot = _snapshot()
    with pytest.raises(PhysicalNativeRepresentationError, match="source outside exact representation authority"):
        resolve_authorized_physical_binding(
            snapshot,
            source_sha256=OTHER_SOURCE,
            variable_ordinal=388,
            variable_name="Q291G5",
            native_code=1,
            native_response_state="SUBSTANTIVE_RESPONSE",
        )


def test_same_representation_on_another_variable_fails_closed():
    snapshot = _snapshot()
    with pytest.raises(PhysicalNativeRepresentationError, match="no unique exact authorized representation binding"):
        resolve_authorized_physical_binding(
            snapshot,
            source_sha256=SOURCE,
            variable_ordinal=999,
            variable_name="OTHER_VARIABLE",
            native_code=1,
            native_response_state="SUBSTANTIVE_RESPONSE",
        )


def test_unlisted_numeric_value_fails_closed():
    snapshot = _snapshot()
    with pytest.raises(PhysicalNativeRepresentationError, match="no unique exact authorized representation binding"):
        resolve_authorized_physical_binding(
            snapshot,
            source_sha256=SOURCE,
            variable_ordinal=388,
            variable_name="Q291G5",
            native_code=6,
            native_response_state="SUBSTANTIVE_RESPONSE",
        )


def test_special_code_receives_source_state_but_no_canonical_mapping_surface():
    snapshot = _snapshot()
    binding = resolve_authorized_physical_binding(
        snapshot,
        source_sha256=SOURCE,
        variable_ordinal=388,
        variable_name="Q291G5",
        native_code=-1,
        native_response_state="DK",
    )
    assert binding.native_response_state == "DK"
    assert binding.physical_missing_state is PhysicalMissingState.FORMAT_USER_MISSING_RANGE
    assert binding.decoder_value == -1.0
    assert not hasattr(binding, "canonical_value")


def test_r1e_native_to_program_mapping_authority_cannot_authorize_a_to_b():
    with pytest.raises(Exception, match="authority kind mismatch"):
        validate_representation_authority(mapping_authority_snapshot())


def test_representation_authority_keeps_canonical_question_mapping_absent():
    snapshot = _snapshot()
    assert snapshot.scope_envelope["canonical_question_mapping"] == "ABSENT_NOT_AUTHORIZED"
    assert snapshot.scope_envelope["native_to_canonical_mapping"] == "OUT_OF_SCOPE"


def test_representation_authority_keeps_cross_source_relation_absent():
    snapshot = _snapshot()
    assert snapshot.scope_envelope["cross_source_relation"] == "NONE_AUTHORIZED"
    with pytest.raises(PhysicalNativeRepresentationError, match="source outside exact representation authority"):
        resolve_authorized_physical_binding(
            snapshot,
            source_sha256=OTHER_SOURCE,
            variable_ordinal=394,
            variable_name="Q291P5",
            native_code=-1,
            native_response_state="DK",
        )


def test_candidate_output_cannot_substitute_for_required_upstream_evidence_class():
    candidate = _ref("CandidateOutput@1.0.0", "candidate")
    rows = [_row("Q291G5", 388, 1, "SUBSTANTIVE_RESPONSE")]
    with pytest.raises(PhysicalNativeRepresentationError, match="wrong upstream decoder-law evidence class"):
        build_representation_authority_snapshot(
            authority_id="SYNTHETIC-INVALID-CANDIDATE-PARENT",
            authority_version="1.0.0",
            source_sha256=SOURCE,
            source_universe_ref=UNIVERSE,
            target_use_ref="SYNTHETIC_EXACT_USE",
            predicate_or_risk_set_ref=RISK,
            source_semantics_authority_ref=SOURCE_AUTH,
            upstream_decoder_law_evidence_ref=candidate,
            variable_type_evidence_ref=TYPE_EVIDENCE,
            exact_representation_bindings=rows,
            negative_limit_refs=NEGATIVE,
            effective_time_or_interval={"court": "R1J-C-SYNTHETIC"},
        )


def test_system_missing_is_not_routed_through_source_native_representation_authority():
    bad = {
        "source_sha256": SOURCE,
        "variable": {"ordinal": 388, "name": "Q291G5"},
        "native_code_token": CODEC.encode(-1),
        "native_response_state": "MISSING",
        "decoder_value_token": CODEC.encode(None),
        "physical_missing_state": PhysicalMissingState.SYSTEM_MISSING.value,
        "source_missing_declaration": None,
    }
    with pytest.raises(PhysicalNativeRepresentationError, match="system missing is outside"):
        build_representation_authority_snapshot(
            authority_id="SYNTHETIC-INVALID-SYSTEM-MISSING",
            authority_version="1.0.0",
            source_sha256=SOURCE,
            source_universe_ref=UNIVERSE,
            target_use_ref="SYNTHETIC_EXACT_USE",
            predicate_or_risk_set_ref=RISK,
            source_semantics_authority_ref=SOURCE_AUTH,
            upstream_decoder_law_evidence_ref=DECODER_EVIDENCE,
            variable_type_evidence_ref=TYPE_EVIDENCE,
            exact_representation_bindings=(bad,),
            negative_limit_refs=NEGATIVE,
            effective_time_or_interval={"court": "R1J-C-SYNTHETIC"},
        )
