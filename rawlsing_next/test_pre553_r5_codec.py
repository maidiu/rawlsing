from dataclasses import dataclass
from enum import Enum
import math, struct, unicodedata
import pytest

from rawlsing_next.pre553_r5_codec import R5CodecError, R5OpaqueValue, R5TypedValueCodec
from rawlsing_next.pre553_r5_seam import (
    R5GeometryCertificate, normalize_decoder_batch, normalize_variables,
)


class State(str, Enum):
    OBSERVED = "OBSERVED_STORAGE_VALUE"
    SYSTEM = "SYSTEM_MISSING"
    USER = "FORMAT_USER_MISSING_VALUE"

@dataclass(frozen=True)
class Cell:
    row_ordinal: int
    variable_ordinal: int
    variable_name: str
    raw_value: object
    missing_state: State
    source_missing_declaration: object = None
    raw_value_label: object = None

@dataclass(frozen=True)
class Var:
    ordinal: int
    name: str
    storage_type: str | None
    variable_label: str | None
    value_labels: dict
    missing_declarations: tuple
    display_metadata: dict
    topology_metadata: dict

@dataclass(frozen=True)
class Incidence:
    source_sha256: str
    variables: tuple


def bits(v): return struct.pack(">d", v).hex()


def test_signed_zero_and_finite_float_bits_exact():
    codec = R5TypedValueCodec()
    for value in (-0.0, 0.0, 1.25, -1.25, 2.0 ** -1022, 1.7976931348623157e308):
        enc = codec.encode(value)
        assert enc["bits"] == bits(value)
        assert bits(codec.decode(enc)) == bits(value)
    assert codec.typed_key(-0.0) != codec.typed_key(0.0)


def test_nan_state_does_not_invent_payload_and_text_infinity_stays_text():
    codec = R5TypedValueCodec()
    enc = codec.encode(float("nan"))
    assert enc == {"t": "float64_nan_decoder_state"}
    assert math.isnan(codec.decode(enc))
    assert codec.decode(codec.encode("inf")) == "inf"
    assert codec.encode("inf")["t"] == "str"


def test_large_integer_escape_is_exact_no_wrap():
    codec = R5TypedValueCodec(inline_integer_bits=31)
    value = 2 ** 4096 + 123
    enc = codec.encode(value)
    assert enc["t"] == "int_escape"
    assert codec.decode(enc) == value


def test_bool_int_float_typed_keys_never_collide():
    codec = R5TypedValueCodec()
    assert len({codec.typed_key(True), codec.typed_key(1), codec.typed_key(1.0)}) == 3


def test_strings_preserve_empty_nul_controls_and_normalization_sensitive_unicode():
    codec = R5TypedValueCodec()
    values = ["", "A\x00B\x01\x1f", "é", "e\u0301", "ß", "İ"]
    for value in values:
        assert codec.decode(codec.encode(value)) == value
    assert codec.typed_key("é") != codec.typed_key("e\u0301")
    assert unicodedata.normalize("NFC", "e\u0301") == "é"  # proves fixture sensitivity


def test_bytes_and_opaque_escape_roundtrip():
    codec = R5TypedValueCodec()
    for value in (b"\x00\xffabc", R5OpaqueValue("NATIVE_SPECIAL@1", b"\x00\x01")):
        assert codec.decode(codec.encode(value)) == value


def test_date_time_invention_is_rejected():
    import datetime
    with pytest.raises(R5CodecError):
        R5TypedValueCodec().encode(datetime.datetime(2020, 1, 1))


def test_decoder_seam_preserves_missing_state_selected_label_and_explicit_coordinates():
    sha = "a" * 64
    cells = (
        Cell(1, 0, "q", 0, State.OBSERVED, None, "missing"),
        Cell(2, 0, "q", None, State.SYSTEM, {"kind": "system"}, None),
    )
    batch = normalize_decoder_batch(sha, cells)
    assert batch.cells[0].missing_state == "OBSERVED_STORAGE_VALUE"
    assert batch.cells[1].missing_state == "SYSTEM_MISSING"
    assert batch.cells[0].explicit_source_coordinates == (1, 0)
    assert batch.cells[0].source_cell_locator is None
    codec = R5TypedValueCodec()
    assert codec.decode(batch.cells[0].raw_value_label) == "missing"


def test_missing_declaration_order_zero_incidence_and_topology_metadata_preserved():
    sha = "b" * 64
    declarations = ({"kind": "value", "value": -1}, {"kind": "range", "lo": -9, "hi": -2})
    topo = {"mr_sets": [{"id": "A", "members": ["q1", "q2"]}, {"id": "B", "members": ["q1", "q2"]}],
            "ranked": True}
    inc = Incidence(sha, (Var(0, "q1", "F8", "Question", {"-1": "Missing"}, declarations, {"format": "F2.0"}, topo),))
    records = normalize_variables(inc)
    codec = R5TypedValueCodec()
    assert [codec.decode(v) for v in records[0].missing_declarations] == list(declarations)
    assert codec.decode(records[0].topology_metadata) == topo


def test_certified_source_cell_locator_is_not_event_identity():
    sha = "c" * 64
    cert = R5GeometryCertificate(sha, row_count=2, variable_count=1, complete_rectangular_row_major=True, certificate_id="fixture")
    cell = Cell(2, 0, "q", 1.5, State.OBSERVED)
    batch = normalize_decoder_batch(sha, (cell,), geometry=cert)
    assert batch.cells[0].source_cell_locator == 1
    assert not hasattr(batch.cells[0], "semantic_event_id")


def test_vector_finite_float_hot_path_is_bit_identical_to_scalar_fallback():
    sha = "d" * 64
    cells = tuple(Cell(i + 1, 0, "q", (-1.0) ** i * (i + 0.25), State.OBSERVED) for i in range(8))
    fast = normalize_decoder_batch(sha, cells, permit_vector_hot_path=True)
    slow = normalize_decoder_batch(sha, cells, permit_vector_hot_path=False)
    assert fast.vector_fast_path_used
    assert [x.raw_value for x in fast.cells] == [x.raw_value for x in slow.cells]


def test_non_float_vector_input_uses_exact_fallback():
    sha = "e" * 64
    batch = normalize_decoder_batch(sha, (Cell(1, 0, "q", 2**100, State.USER, {"value": 2**100}),))
    assert not batch.vector_fast_path_used
    assert batch.vector_fallback_count == 1

def test_source_native_rows_include_metadata_zero_incidence_declarations_and_every_cell():
    from rawlsing_next.pre553_r5_seam import iter_source_native_rows
    class FullIncidence:
        source_sha256="f"*64
        source_format="SAV"
        row_count=2
        reader_configuration={"encoding_mode":"EXACT"}
        file_metadata={"declared_encoding":"UTF-8"}
        variables=(Var(0,"q","F8","Question",{"-1":"Missing"},({"kind":"value","value":-1},),{"format":"F2.0"},{"mr_sets":[]}),)
        def iter_batches(self,batch_size):
            yield (Cell(1,0,"q",1,State.OBSERVED,None,"One"),Cell(2,0,"q",2,State.OBSERVED,None,"Two"))
    material=list(iter_source_native_rows(FullIncidence(),batch_size=1))
    assert [r.relation for r in material].count("source_metadata")==1
    assert [r.relation for r in material].count("source_variables")==1
    assert [r.relation for r in material].count("source_physical_cells")==2
    variable=next(r for r in material if r.relation=="source_variables")
    assert len(variable.payload["missing_declarations"])==1  # declaration retained with zero incidence
