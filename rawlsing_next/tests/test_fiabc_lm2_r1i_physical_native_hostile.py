from __future__ import annotations

from rawlsing_next.fiabc_lm2_r1e_common_c11 import _materializer, _structural_material
from rawlsing_next.fiabc_lm2_r1e_wvs7_mapping_authority import (
    MAPPING_AUTHORITY_REF,
    NEGATIVE_LIMITS,
    mapping_authority_snapshot,
)
from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError, require_positive_authority
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState, classify_physical_value
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key

QUESTIONS = ("Q291G5", "Q291P5")
SPECIALS = (-5, -4, -2, -1)


def _projection_and_variables():
    module = _materializer()
    structural_doc, variables, _country = _structural_material(module)
    return module, module.materialize_from_structural_input(structural_doc), {v.name: v for v in variables}


def test_global_exact_type_law_remains_int_float_distinct():
    assert physical_value_binding_key(1, PhysicalMissingState.OBSERVED_STORAGE_VALUE) != physical_value_binding_key(
        1.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE
    )
    assert physical_value_binding_key(-1, PhysicalMissingState.FORMAT_USER_MISSING_RANGE, {"kind":"range","lo":-5,"hi":-1}) != physical_value_binding_key(
        -1.0, PhysicalMissingState.FORMAT_USER_MISSING_RANGE, {"kind":"range","lo":-5,"hi":-1}
    )


def test_current_wvs_structural_projection_has_no_storage_type_representation_premise():
    _module, _projection, variables = _projection_and_variables()
    for q in QUESTIONS:
        assert variables[q].storage_type is None


def test_native_to_canonical_mapping_authority_does_not_bridge_physical_representation():
    module, projection, variables = _projection_and_variables()
    slots = {slot.slot.name: slot for slot in projection.response_slots}
    for q in QUESTIONS:
        variable = variables[q]
        rule = next(x for x in slots[q].values if x.canonical_value == "1")
        state, declaration = classify_physical_value(1, variable.missing_declarations)
        assert rule.physical_key == physical_value_binding_key(1, state, declaration)
        assert rule.transform_authority_ref == MAPPING_AUTHORITY_REF
        assert rule.physical_key != physical_value_binding_key(1.0, state, declaration)
    assert "NO_CANDIDATE_OUTPUT_PARENTAGE" in NEGATIVE_LIMITS


def test_nearby_unapproved_physical_representations_remain_distinct():
    observed = PhysicalMissingState.OBSERVED_STORAGE_VALUE
    int_key = physical_value_binding_key(1, observed)
    assert int_key != physical_value_binding_key(1.0, observed)
    assert int_key != physical_value_binding_key("1", observed)


def test_special_states_remain_noncanonical_and_mapping_authority_does_not_leak():
    module, projection, variables = _projection_and_variables()
    slots = {slot.slot.name: slot for slot in projection.response_slots}
    for q in QUESTIONS:
        variable = variables[q]
        for code in SPECIALS:
            state, declaration = classify_physical_value(code, variable.missing_declarations)
            int_key = physical_value_binding_key(code, state, declaration)
            rule = next(x for x in slots[q].values if x.physical_key == int_key)
            assert rule.canonical_value is None
            assert rule.transform_authority_ref is None
            assert MAPPING_AUTHORITY_REF not in rule.extra_authority_refs
            assert int_key != physical_value_binding_key(float(code), state, declaration)


def test_system_missing_remains_separate_from_user_missing_codes():
    _module, projection, _variables = _projection_and_variables()
    system_key = physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING, None)
    slots = {slot.slot.name: slot for slot in projection.response_slots}
    for q in QUESTIONS:
        matches = [x for x in slots[q].values if x.physical_key == system_key]
        assert len(matches) == 1
        assert matches[0].canonical_value is None
        assert matches[0].transform_authority_ref is None
        assert all(
            x.physical_key != system_key
            for x in slots[q].values
            if x.response_state != "MISSING" or x.physical_key != system_key
        )


def test_canonical_question_mapping_remains_absent():
    _module, projection, _variables = _projection_and_variables()
    questions = {q.native_question_ref.object_id: q for q in projection.questions}
    assert len(questions) == 2
    for q in projection.questions:
        value = q.canonical_question_ref_or_typed_absence
        assert isinstance(value, TypedAbsence)
        assert value.state == "NOT_AUTHORIZED"


def test_common_authority_gate_does_not_treat_source_semantics_as_mapping():
    _module, projection, _variables = _projection_and_variables()
    source_snapshot = next(
        x for x in projection.authority_snapshots
        if x.authority_kind == "SOURCE_SEMANTICS_TOPOLOGY"
    )
    import pytest
    with pytest.raises(Pre553AuthorityError, match="authority kind mismatch"):
        require_positive_authority(
            source_snapshot,
            authority_kind="NATIVE_CANONICAL_MAPPING_HARMONIZATION",
        )
