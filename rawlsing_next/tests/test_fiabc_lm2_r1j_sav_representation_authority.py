from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import pytest

from rawlsing_next.fiabc_lm2_r1e_common_c11 import _materializer, _structural_material
from rawlsing_next.fiabc_lm2_r1e_wvs7_mapping_authority import (
    MAPPING_AUTHORITY_REF,
    NEGATIVE_LIMITS as R1E_NEGATIVE_LIMITS,
    mapping_authority_snapshot,
)
from rawlsing_next.fiabc_lm2_r1j_wvs7_representation_authority import (
    AUTHORITY_KIND,
    AUTHORIZED_R5_TOKENS,
    NATIVE_CODES,
    NEGATIVE_LIMITS,
    OPERATION,
    Q291_VARIABLES,
    REPRESENTATION_AUTHORITY_REF,
    SOURCE_SHA256,
    authorized_decoder_physical_value,
    representation_authority_snapshot,
)
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_empirical_authority import (
    Pre553AuthorityError,
    require_positive_authority,
    validate_authority_snapshot,
)
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState, classify_physical_value
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key

ROOT = Path(__file__).resolve().parents[2]
R1I_INVENTORY = ROOT / "WORKER_RETURNS/FIABC-LM2-R1I-PHYSICAL-NATIVE-BINDING/01_PHYSICAL_KEY_INVENTORY.json"
QUESTIONS = ("Q291G5", "Q291P5")
SPECIALS = (-5, -4, -2, -1)
OLD_PROJECTION_AUTHORITY_HASH = "6b0dba629206c563d30bdb86f4f8bb112b24eb0ceaf05e47aec6aa049dbf23c0"
OLD_PROJECTION_IDENTITY_HASH = "8d6ee3fac396d7bd0e0afdf2f4fb13bcc8f040e53d63dd4c0d559b65c9ade4df"
LOCK2 = "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"


@lru_cache(maxsize=1)
def _projection_and_variables():
    module = _materializer()
    structural_doc, variables, _country = _structural_material(module)
    projection = module.materialize_from_structural_input(structural_doc)
    return module, projection, {v.name: v for v in variables}


def _r1i_physical_keys():
    doc = json.loads(R1I_INVENTORY.read_text(encoding="utf-8"))
    assert doc["source_sha256"] == SOURCE_SHA256
    assert doc["carrier"]["candidate_neutral"] is True
    assert doc["carrier"]["contains_candidate_output"] is False
    return {
        q: {row["physical_value_binding_key"] for row in doc["variables"][q]}
        for q in QUESTIONS
    }


def test_global_int_float_physical_identity_remains_distinct():
    assert physical_value_binding_key(
        1, PhysicalMissingState.OBSERVED_STORAGE_VALUE
    ) != physical_value_binding_key(
        1.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE
    )
    decl = {"kind": "range", "lo": -5, "hi": -1}
    assert physical_value_binding_key(
        -1, PhysicalMissingState.FORMAT_USER_MISSING_RANGE, decl
    ) != physical_value_binding_key(
        -1.0, PhysicalMissingState.FORMAT_USER_MISSING_RANGE, decl
    )


def test_representation_helper_is_exact_source_variable_code_and_type_bounded():
    codec = R5TypedValueCodec()
    for name, ordinal in Q291_VARIABLES.items():
        for code in NATIVE_CODES:
            value = authorized_decoder_physical_value(
                source_sha256=SOURCE_SHA256,
                variable_name=name,
                ordinal=ordinal,
                native_code=code,
            )
            assert type(value) is float
            assert codec.encode(value) == AUTHORIZED_R5_TOKENS[code]
    hostile = (
        dict(source_sha256="0" * 64, variable_name="Q291G5", ordinal=388, native_code=1),
        dict(source_sha256=SOURCE_SHA256, variable_name="Q291G4", ordinal=387, native_code=1),
        dict(source_sha256=SOURCE_SHA256, variable_name="Q291G5", ordinal=394, native_code=1),
        dict(source_sha256=SOURCE_SHA256, variable_name="Q291G5", ordinal=388, native_code=0),
        dict(source_sha256=SOURCE_SHA256, variable_name="Q291G5", ordinal=388, native_code=6),
        dict(source_sha256=SOURCE_SHA256, variable_name="Q291G5", ordinal=388, native_code=1.0),
        dict(source_sha256=SOURCE_SHA256, variable_name="Q291G5", ordinal=388, native_code="1"),
        dict(source_sha256=SOURCE_SHA256, variable_name="Q291G5", ordinal=388, native_code=True),
    )
    for case in hostile:
        with pytest.raises(ValueError):
            authorized_decoder_physical_value(**case)


def test_exact_r1i_float_carrier_keyspace_now_matches_governed_numeric_rules():
    module, projection, variables = _projection_and_variables()
    physical = _r1i_physical_keys()
    slots = {slot.slot.name: slot for slot in projection.response_slots}
    system_key = physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING, None)
    for q in QUESTIONS:
        assert variables[q].storage_type is None  # structural preimage was not regenerated
        governed = {rule.physical_key for rule in slots[q].values}
        assert len(physical[q]) == 9
        assert len(governed) == 10
        assert physical[q] <= governed
        assert governed - physical[q] == {system_key}
        for code in NATIVE_CODES:
            value = authorized_decoder_physical_value(
                source_sha256=SOURCE_SHA256,
                variable_name=q,
                ordinal=Q291_VARIABLES[q],
                native_code=code,
            )
            state, declaration = classify_physical_value(value, variables[q].missing_declarations)
            assert physical_value_binding_key(value, state, declaration) in physical[q]


def test_no_generic_numeric_coercion_was_added_to_c11_key_law():
    module, projection, variables = _projection_and_variables()
    slots = {slot.slot.name: slot for slot in projection.response_slots}
    for q in QUESTIONS:
        var = variables[q]
        for code in (1, 2, 3, 4, 5):
            state, declaration = classify_physical_value(code, var.missing_declarations)
            assert physical_value_binding_key(code, state, declaration) not in {
                rule.physical_key for rule in slots[q].values
            }
        assert physical_value_binding_key(
            "1", PhysicalMissingState.OBSERVED_STORAGE_VALUE, None
        ) not in {rule.physical_key for rule in slots[q].values}


def test_special_codes_remain_noncanonical_and_system_missing_remains_separate():
    module, projection, variables = _projection_and_variables()
    slots = {slot.slot.name: slot for slot in projection.response_slots}
    system_key = physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING, None)
    for q in QUESTIONS:
        var = variables[q]
        for code in SPECIALS:
            value = authorized_decoder_physical_value(
                source_sha256=SOURCE_SHA256,
                variable_name=q,
                ordinal=Q291_VARIABLES[q],
                native_code=code,
            )
            state, declaration = classify_physical_value(value, var.missing_declarations)
            key = physical_value_binding_key(value, state, declaration)
            rule = next(x for x in slots[q].values if x.physical_key == key)
            assert rule.canonical_value is None
            assert rule.transform_authority_ref is None
            assert REPRESENTATION_AUTHORITY_REF in rule.extra_authority_refs
            assert MAPPING_AUTHORITY_REF not in rule.extra_authority_refs
        system = next(x for x in slots[q].values if x.physical_key == system_key)
        assert system.response_state == "MISSING"
        assert system.canonical_value is None
        assert system.transform_authority_ref is None
        assert REPRESENTATION_AUTHORITY_REF not in system.extra_authority_refs


def test_substantive_mapping_ceiling_and_question_mapping_are_unchanged():
    module, projection, _variables = _projection_and_variables()
    slots = {slot.slot.name: slot for slot in projection.response_slots}
    for slot in slots.values():
        substantive = [r for r in slot.values if r.canonical_value is not None]
        assert sorted(r.canonical_value for r in substantive) == ["1", "2", "3", "4", "5"]
        assert all(r.transform_authority_ref == MAPPING_AUTHORITY_REF for r in substantive)
        assert all(REPRESENTATION_AUTHORITY_REF in r.extra_authority_refs for r in substantive)
    for question in projection.questions:
        assert isinstance(question.canonical_question_ref_or_typed_absence, TypedAbsence)
        assert question.canonical_question_ref_or_typed_absence.state == "NOT_AUTHORIZED"
    mapping = mapping_authority_snapshot()
    assert mapping.authority_ref == MAPPING_AUTHORITY_REF
    assert mapping.authority_kind == "NATIVE_CANONICAL_MAPPING_HARMONIZATION"
    assert "NO_CANDIDATE_OUTPUT_PARENTAGE" in R1E_NEGATIVE_LIMITS


def test_representation_authority_kind_is_distinct_and_narrow():
    snapshot = representation_authority_snapshot()
    assert validate_authority_snapshot(snapshot) == snapshot
    assert require_positive_authority(
        snapshot,
        authority_kind=AUTHORITY_KIND,
        operation=OPERATION,
        object_family="RespondentEvent",
    ) == snapshot
    with pytest.raises(Pre553AuthorityError, match="authority kind mismatch"):
        require_positive_authority(snapshot, authority_kind="SOURCE_SEMANTICS_TOPOLOGY")
    for ceiling in (
        "NO_GLOBAL_INT_FLOAT_COERCION",
        "NO_OTHER_VARIABLES",
        "NO_OTHER_WVS_WAVES",
        "NO_OTHER_SOURCES",
        "NO_CANONICAL_QUESTION_MAPPING",
        "NO_NATIVE_TO_CANONICAL_MAPPING_BEYOND_R1E",
        "NO_CROSS_SOURCE_EQUIVALENCE",
        "NO_LABEL_OR_FREQUENCY_AUTHORITY",
        "NO_CANDIDATE_OUTPUT_PARENTAGE",
        "NO_SYSTEM_MISSING_REINTERPRETATION",
    ):
        assert ceiling in NEGATIVE_LIMITS


def test_projection_and_response_binding_reissued_but_lock2_preserved():
    module, projection, _variables = _projection_and_variables()
    assert module.LOCK2 == LOCK2
    assert module.TIE_ORDER_REF.content_hash == LOCK2
    assert module.RESPONSE_BINDING_REF.content_hash == module.RESPONSE_BINDING_HASH
    assert projection.projection_authority_ref.authority_content_hash != OLD_PROJECTION_AUTHORITY_HASH
    assert projection.projection_identity_ref.content_hash != OLD_PROJECTION_IDENTITY_HASH
    assert REPRESENTATION_AUTHORITY_REF in projection.required_authority_refs
    assert module.RESPONSE_BINDING_REF.as_dict() == module.PROJECTION_AUTHORITY_MATERIAL["response_binding_ref"]


def test_non_wvs_behavior_and_candidate_boundary_remain_closed():
    doc = json.loads(R1I_INVENTORY.read_text(encoding="utf-8"))
    assert doc["carrier"]["candidate_neutral"] is True
    assert doc["carrier"]["contains_candidate_output"] is False
    assert physical_value_binding_key(
        1, PhysicalMissingState.OBSERVED_STORAGE_VALUE
    ) != physical_value_binding_key(
        1.0, PhysicalMissingState.OBSERVED_STORAGE_VALUE
    )
    with pytest.raises(ValueError):
        authorized_decoder_physical_value(
            source_sha256=SOURCE_SHA256,
            variable_name="Q291G5",
            ordinal=388,
            native_code=-3,
        )
