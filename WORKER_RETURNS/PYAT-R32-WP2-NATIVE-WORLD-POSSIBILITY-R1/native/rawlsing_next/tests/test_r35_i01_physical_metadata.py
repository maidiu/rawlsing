from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

from rawlsing_next import pre553_physical_decoder as decoder


SOURCE_SHA = "a" * 64
READER_CONFIG = {
    "reader": "pyreadstat",
    "reader_version": "hostile-fixture",
    "decoder_implementation": decoder.DECODER_IMPLEMENTATION_ID,
    "physical_metadata_contract": decoder.PHYSICAL_METADATA_CONTRACT,
    "user_missing": True,
    "apply_value_formats": False,
    "encoding": None,
    "authority_status": None,
}


def sav_header(*, nominal_case_size: int, declared_case_count: int = 7) -> bytes:
    header = bytearray(176)
    header[0:4] = b"$FL2"
    header[4:64] = b"@(#) SPSS DATA FILE R35-I01".ljust(60, b" ")
    header[64:68] = (2).to_bytes(4, "little", signed=True)
    header[68:72] = nominal_case_size.to_bytes(4, "little", signed=True)
    header[72:76] = (1).to_bytes(4, "little", signed=True)
    header[76:80] = (0).to_bytes(4, "little", signed=True)
    header[80:84] = declared_case_count.to_bytes(4, "little", signed=True)
    return bytes(header)


def make_variables(count: int, *, first_format: str | None = None) -> tuple[decoder.PhysicalVariable, ...]:
    variables = []
    for ordinal in range(1, count + 1):
        variables.append(decoder.PhysicalVariable(
            ordinal=ordinal,
            name=f"V{ordinal}",
            storage_type="double",
            variable_label=None,
            value_labels={},
            missing_declarations=(),
            display_metadata={
                "storage_width": 8,
                "display_width": 2 if ordinal == 1 and first_format else None,
                "alignment": None,
                "measure": None,
                "format": first_format if ordinal == 1 else None,
            },
            topology_metadata={"multiple_response_sets": {}},
        ))
    return tuple(variables)


def fake_metadata(*, number_columns: int, number_rows: int) -> SimpleNamespace:
    return SimpleNamespace(
        number_columns=number_columns,
        number_rows=number_rows,
        file_format="sav",
        file_encoding="UTF-8",
    )


def contract_for(
    *,
    nominal_case_size: int = 174,
    variable_count: int = 332,
    first_format: str | None = None,
) -> tuple[dict, tuple[decoder.PhysicalVariable, ...]]:
    variables = make_variables(variable_count, first_format=first_format)
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "hostile.sav"
        path.write_bytes(sav_header(nominal_case_size=nominal_case_size))
        metadata = decoder._file_metadata_contract(
            source=path,
            source_format="SAV",
            metadata=fake_metadata(number_columns=variable_count, number_rows=7),
            variables=variables,
            row_count=7,
        )
    return dict(metadata), variables


class R35I01PhysicalMetadataCourt(unittest.TestCase):
    def test_nominal_header_count_and_traversed_stream_width_both_survive(self) -> None:
        metadata, _variables = contract_for(nominal_case_size=174, variable_count=332)

        raw = metadata["raw_layout_declarations"]["format_native_header"]
        geometry = metadata["normalized_geometry"]

        self.assertEqual(raw["parse_status"], "PARSED_FIXED_HEADER")
        self.assertEqual(raw["nominal_case_size"], 174)
        self.assertEqual(geometry["traversed_dictionary_variable_count"], 332)
        self.assertEqual(geometry["traversed_stream_cell_width"], 332)
        self.assertNotEqual(raw["nominal_case_size"], geometry["traversed_stream_cell_width"])

    def test_metadata_mismatch_is_preserved_not_normalized(self) -> None:
        metadata, _variables = contract_for(nominal_case_size=174, variable_count=332)

        raw = metadata["raw_layout_declarations"]
        self.assertEqual(raw["format_native_header"]["nominal_case_size"], 174)
        self.assertEqual(raw["reader_declared"]["number_columns"], 332)
        self.assertEqual(metadata["number_columns"], 332)

        # No "resolved", "corrected", or winner field is allowed to erase either witness.
        flattened_keys = set(metadata) | set(raw) | set(raw["format_native_header"])
        self.assertFalse({"resolved_number_columns", "corrected_number_columns", "authoritative_number_columns"} & flattened_keys)

    def test_display_format_remains_distinct_from_stored_magnitude(self) -> None:
        metadata, variables = contract_for(variable_count=1, first_format="F2.0")
        cell = decoder.PhysicalCell(
            row_ordinal=1,
            variable_ordinal=1,
            variable_name="V1",
            raw_value=9876543210,
            missing_state=decoder.PhysicalMissingState.OBSERVED_STORAGE_VALUE,
            source_missing_declaration=None,
        )

        self.assertEqual(metadata["display_metadata"][0]["display_metadata"]["format"], "F2.0")
        self.assertEqual(variables[0].display_metadata["format"], "F2.0")
        self.assertEqual(cell.raw_value, 9876543210)

    def test_candidate_representation_dropping_physical_witness_is_rejected(self) -> None:
        metadata, variables = contract_for()
        incidence = decoder.PhysicalSourceIncidence(
            SOURCE_SHA, "SAV", 7, variables, READER_CONFIG, metadata
        )
        expected = incidence.physical_metadata_digest

        dropped = dict(metadata)
        dropped.pop("raw_layout_declarations")
        hostile = replace(incidence, file_metadata=dropped)

        with self.assertRaisesRegex(decoder.DecoderError, "missing required physical witness"):
            hostile.require_physical_metadata_digest(expected)

    def test_equal_semantic_projection_can_have_unequal_required_physical_metadata_digest(self) -> None:
        semantic_projection = {"Q1": "same-governed-result"}
        metadata_a, variables_a = contract_for(nominal_case_size=174, variable_count=1, first_format="F2.0")
        metadata_b, variables_b = contract_for(nominal_case_size=175, variable_count=1, first_format="F2.0")

        digest_a = decoder.compute_physical_metadata_digest(
            source_sha256=SOURCE_SHA,
            source_format="SAV",
            reader_configuration=READER_CONFIG,
            file_metadata=metadata_a,
            variables=variables_a,
        )
        digest_b = decoder.compute_physical_metadata_digest(
            source_sha256=SOURCE_SHA,
            source_format="SAV",
            reader_configuration=READER_CONFIG,
            file_metadata=metadata_b,
            variables=variables_b,
        )

        self.assertEqual(semantic_projection, {"Q1": "same-governed-result"})
        self.assertNotEqual(digest_a, digest_b)

    def test_reader_config_is_bound_into_physical_metadata_digest(self) -> None:
        metadata, variables = contract_for(variable_count=1)
        other_config = dict(READER_CONFIG)
        other_config["reader_version"] = "different"

        digest_a = decoder.compute_physical_metadata_digest(
            source_sha256=SOURCE_SHA,
            source_format="SAV",
            reader_configuration=READER_CONFIG,
            file_metadata=metadata,
            variables=variables,
        )
        digest_b = decoder.compute_physical_metadata_digest(
            source_sha256=SOURCE_SHA,
            source_format="SAV",
            reader_configuration=other_config,
            file_metadata=metadata,
            variables=variables,
        )

        self.assertNotEqual(digest_a, digest_b)


if __name__ == "__main__":
    unittest.main()
