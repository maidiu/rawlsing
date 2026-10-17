from dataclasses import replace
import inspect
import math
from collections.abc import Mapping

import pytest

from rawlsing_next.pre553_empirical_objects import Pre553IntegrityError, canonicalize
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_r5_codec import CODEC_VERSION, R5TypedValueCodec, canonical_bytes
from rawlsing_next.pre553_source_backed_c11_facade import (
    CoordinateSlotRule,
    ExactPhysicalCellStream,
    ResponseSlotRule,
    ResponseValueRule,
    SourceBackedC11FacadeError,
    build_validated_source_backed_c11_release_from_stream,
    physical_value_binding_key,
    raw_physical_value_witness,
)
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture


CODEC = R5TypedValueCodec()


def test_r1_exact_r5_tokens_preserve_hostile_physical_distinctions():
    cases = (
        (1.5, {"t": "float64_finite", "bits": "3ff8000000000000"}),
        (-2.25, {"t": "float64_finite", "bits": "c002000000000000"}),
        (0.0, {"t": "float64_finite", "bits": "0000000000000000"}),
        (-0.0, {"t": "float64_finite", "bits": "8000000000000000"}),
        (float("nan"), {"t": "float64_nan_decoder_state"}),
        (float("inf"), {"t": "float64_pos_inf"}),
        (float("-inf"), {"t": "float64_neg_inf"}),
    )
    tokens = [CODEC.encode(value) for value, _ in cases]
    assert tokens == [expected for _, expected in cases]
    assert canonical_bytes(tokens[0]) == canonical_bytes(tokens[0])
    assert CODEC.encode(1) != CODEC.encode(1.0)
    assert CODEC.encode(True) != CODEC.encode(1)
    assert CODEC.encode("inf") != CODEC.encode(float("inf"))
    assert CODEC.encode("é") != CODEC.encode("e\u0301")


def test_r2_semantic_float_ban_is_unchanged():
    for value in (1.5, float("nan"), float("inf"), float("-inf")):
        with pytest.raises(Pre553IntegrityError, match="float/NaN/Infinity forbidden"):
            canonicalize(value)


def test_r3_physical_binding_key_includes_exact_type_bits_state_and_declaration():
    state = PhysicalMissingState.OBSERVED_STORAGE_VALUE
    declaration = {"upper": 1.5}
    assert physical_value_binding_key(1.5, state, declaration) == physical_value_binding_key(1.5, state, declaration)
    assert physical_value_binding_key(0.0, state) != physical_value_binding_key(-0.0, state)
    assert physical_value_binding_key(1, state) != physical_value_binding_key(1.0, state)
    assert physical_value_binding_key(True, state) != physical_value_binding_key(1, state)
    assert physical_value_binding_key("inf", state) != physical_value_binding_key(float("inf"), state)
    assert physical_value_binding_key(float("nan"), state) != physical_value_binding_key(float("inf"), state)
    assert physical_value_binding_key(float("inf"), state) != physical_value_binding_key(float("-inf"), state)
    assert physical_value_binding_key(1.5, state) != physical_value_binding_key(1.5, PhysicalMissingState.SYSTEM_MISSING)
    assert physical_value_binding_key(1.5, state, {"upper": 1.5}) != physical_value_binding_key(1.5, state, {"upper": 2.5})


def _physical_fixture_stream():
    fx = _fixture("r1e-n1")
    p = fx["projection"]
    x = p.response_slots[0]
    occurrence = x.values[0].occurrences
    x = replace(
        x,
        values=(
            ResponseValueRule(
                physical_value_binding_key(1.5, PhysicalMissingState.OBSERVED_STORAGE_VALUE),
                "SUBSTANTIVE_RESPONSE", occurrence,
            ),
            ResponseValueRule(
                physical_value_binding_key(float("inf"), PhysicalMissingState.OBSERVED_STORAGE_VALUE),
                "SUBSTANTIVE_RESPONSE", occurrence,
            ),
            ResponseValueRule(
                physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING),
                "MISSING", occurrence,
            ),
        ),
    )
    p = replace(p, response_slots=(x, *p.response_slots[1:]))
    cells = []
    for cell in fx["cells"]:
        value = cell.raw_value
        if cell.variable_name == "X":
            value = {1: 1.5, 2: float("inf"), 3: None}[cell.row_ordinal]
        elif cell.variable_name == "G":
            value = {1: 0.0, 2: -0.0, 3: 0.0}[cell.row_ordinal]
        cells.append(replace(cell, raw_value=value))
    return fx, p, tuple(cells)


def test_r4_r5_response_and_coordinate_witness_seams_are_separate_from_semantics():
    fx, projection, cells = _physical_fixture_stream()
    stream = ExactPhysicalCellStream(fx["source_sha"], 3, lambda: iter(cells))
    release = build_validated_source_backed_c11_release_from_stream(stream, projection)
    events = [x for x in release.public_objects if getattr(x, "native_question_ref", None) == fx["qrefs"]["X"].as_dict()]
    assert {x.raw_response_value["$raw_physical_value"]["token"]["t"] for x in events} >= {
        "float64_finite", "float64_pos_inf", "none",
    }
    assert all(isinstance(x.raw_response_value, Mapping) for x in events)
    coords = [x for x in release.public_objects if getattr(x, "native_coordinate_ref", None) == fx["crefs"]["G"].as_dict()]
    bits = {
        x.raw_coordinate_value["$raw_physical_value"]["token"].get("bits")
        for x in coords
    }
    assert {"0000000000000000", "8000000000000000"}.issubset(bits)
    assert all(x.canonical_coordinate_value_if_authorized is None for x in coords)

    bad_cells = list(cells)
    bad_index = next(i for i, x in enumerate(bad_cells) if x.variable_name == "G" and x.row_ordinal == 1)
    bad_cells[bad_index] = replace(
        bad_cells[bad_index],
        raw_value=None,
        missing_state=PhysicalMissingState.SYSTEM_MISSING,
    )
    with pytest.raises(SourceBackedC11FacadeError, match="unbound/missing coordinate"):
        build_validated_source_backed_c11_release_from_stream(
            ExactPhysicalCellStream(fx["source_sha"], 3, lambda: iter(bad_cells)), projection
        )


def test_r6_weight_boundary_remains_governed_and_nonfinite_is_not_admitted():
    from rawlsing_next.pre553_source_backed_c11_facade import _numeric

    assert _numeric(1.5) == "1.5"
    assert physical_value_binding_key(1.5, PhysicalMissingState.OBSERVED_STORAGE_VALUE) != physical_value_binding_key(1, PhysicalMissingState.OBSERVED_STORAGE_VALUE)
    for value in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(SourceBackedC11FacadeError, match="weight cannot be NaN/inf"):
            _numeric(value)


def test_r7_unprojected_physical_cells_emit_no_semantic_object():
    fx, projection, cells = _physical_fixture_stream()
    extra = PhysicalCell(1, 9999, "UNPROJECTED", float("nan"), PhysicalMissingState.OBSERVED_STORAGE_VALUE, None)
    stream = ExactPhysicalCellStream(fx["source_sha"], 3, lambda: iter((*cells, extra)))
    release = build_validated_source_backed_c11_release_from_stream(stream, projection)
    assert not any(getattr(x, "schema_id", "") == "UNPROJECTED" for x in release.public_objects)


def test_r8_replay_is_stable_and_r9_seam_is_candidate_neutral():
    fx, projection, cells = _physical_fixture_stream()
    first = build_validated_source_backed_c11_release_from_stream(
        ExactPhysicalCellStream(fx["source_sha"], 3, lambda: iter(cells)), projection
    )
    second = build_validated_source_backed_c11_release_from_stream(
        ExactPhysicalCellStream(fx["source_sha"], 3, lambda: iter(reversed(cells))), projection
    )
    assert first.release_ref == second.release_ref
    assert raw_physical_value_witness(1.5) == raw_physical_value_witness(1.5)
    assert "LITS" not in inspect.getsource(physical_value_binding_key)
    assert CODEC_VERSION == "PRE553_R5_TYPED_VALUE_CODEC@1.0.0"
