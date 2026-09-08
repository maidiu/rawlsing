"""Frozen Route-A R5 physical-cell -> C05R2A source-backed adapter.

This module is deliberately mechanical.  It validates the reopened frozen R5
physical carrier, reconstructs decoder-normalized PhysicalCell objects exactly,
and passes an ExactPhysicalCellStream into the already-governed C05R2A facade.
It assigns no semantic meaning and owns no cache or alternate authority carrier.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Mapping

from rawlsing_next import pre553_r5_compact_carrier as frozen
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_r5_codec import CODEC_VERSION, R5TypedValueCodec, canonical_bytes
from rawlsing_next.pre553_r5_model import R5CanonicalRow, R5IntegrityError
from rawlsing_next.pre553_r5_seam import SEAM_VERSION
from rawlsing_next.pre553_r5_single_pass_audit69 import single_pass_full_audit
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
    GovernedC11Projection,
    build_source_backed_c11_repository,
)

CONTRACT_ID = "PRE553_R5_ROUTE_A_TO_C05R2A_ADAPTER@1.0.0"
SOURCE_METADATA_RELATION = "source_metadata"
SOURCE_METADATA_FAMILY = "R5SourceMetadata@1.0.0"
SOURCE_VARIABLE_RELATION = "source_variables"
SOURCE_VARIABLE_FAMILY = "R5PhysicalVariable@1.0.0"
SOURCE_CELL_RELATION = "source_physical_cells"
SOURCE_CELL_FAMILY = "R5PhysicalCell@1.0.0"


class R5SourceBackedAdapterError(R5IntegrityError):
    pass


@dataclass(frozen=True)
class R5SourcePhysicalDescriptor:
    source_sha256: str
    row_count: int
    variable_count: int
    variable_slots: tuple[tuple[int, str], ...]
    physical_root_id: str
    logical_stream_digest: str
    canonical_rows: int
    relation_counts: Mapping[str, int]


def _sha(value: Any, name: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or value != value.lower()
        or any(c not in "0123456789abcdef" for c in value)
    ):
        raise R5SourceBackedAdapterError(f"{name} must be lowercase sha256")
    return value


def _int(value: Any, name: str, *, minimum: int = 0) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise R5SourceBackedAdapterError(f"{name} must be integer >= {minimum}")
    return value


def _payload(row: R5CanonicalRow, *, relation: str, family: str, keys: set[str]) -> Mapping[str, Any]:
    if not isinstance(row, R5CanonicalRow):
        raise R5SourceBackedAdapterError("R5 adapter requires canonical R5 rows")
    if row.relation != relation or row.object_family != family:
        raise R5SourceBackedAdapterError(f"{relation} row family mismatch")
    if not isinstance(row.payload, Mapping) or set(row.payload) != keys:
        raise R5SourceBackedAdapterError(f"{relation} payload shape mismatch")
    expected_hash = hashlib.sha256(canonical_bytes(row.payload)).hexdigest()
    if row.content_hash != expected_hash:
        raise R5SourceBackedAdapterError(f"{relation} content hash mismatch")
    return row.payload


def _decode_exact(codec: R5TypedValueCodec, encoded: Any, name: str) -> Any:
    if not isinstance(encoded, Mapping):
        raise R5SourceBackedAdapterError(f"{name} must be an R5 typed-value mapping")
    try:
        value = codec.decode(encoded)
        rebound = codec.encode(value)
    except Exception as exc:
        raise R5SourceBackedAdapterError(f"{name} typed-value decode failed") from exc
    if canonical_bytes(rebound) != canonical_bytes(encoded):
        raise R5SourceBackedAdapterError(f"{name} typed-value encoding is noncanonical")
    return value


def _validate_metadata(row: R5CanonicalRow, codec: R5TypedValueCodec) -> dict[str, Any]:
    keys = {
        "seam_version", "source_sha256", "source_format", "row_count", "variable_count",
        "reader_configuration", "file_metadata",
    }
    p = _payload(row, relation=SOURCE_METADATA_RELATION, family=SOURCE_METADATA_FAMILY, keys=keys)
    if p["seam_version"] != SEAM_VERSION:
        raise R5SourceBackedAdapterError("source metadata seam version mismatch")
    source_sha = _sha(p["source_sha256"], "source metadata SHA")
    expected_id = f"source:{source_sha}:metadata"
    if row.object_id != expected_id:
        raise R5SourceBackedAdapterError("source metadata object id mismatch")
    if not isinstance(p["source_format"], str) or not p["source_format"]:
        raise R5SourceBackedAdapterError("source format missing")
    row_count = _int(p["row_count"], "source row_count")
    variable_count = _int(p["variable_count"], "source variable_count")
    reader_configuration = _decode_exact(codec, p["reader_configuration"], "reader_configuration")
    file_metadata = _decode_exact(codec, p["file_metadata"], "file_metadata")
    if not isinstance(reader_configuration, Mapping) or not isinstance(file_metadata, Mapping):
        raise R5SourceBackedAdapterError("source metadata typed maps did not decode as mappings")
    return {
        "source_sha256": source_sha,
        "row_count": row_count,
        "variable_count": variable_count,
    }


def _validate_variable(row: R5CanonicalRow, codec: R5TypedValueCodec, source_sha: str) -> tuple[int, str]:
    keys = {
        "seam_version", "source_sha256", "ordinal", "name", "storage_type",
        "variable_label", "value_labels", "missing_declarations",
        "display_metadata", "topology_metadata",
    }
    p = _payload(row, relation=SOURCE_VARIABLE_RELATION, family=SOURCE_VARIABLE_FAMILY, keys=keys)
    if p["seam_version"] != SEAM_VERSION or p["source_sha256"] != source_sha:
        raise R5SourceBackedAdapterError("source variable binding mismatch")
    ordinal = _int(p["ordinal"], "variable ordinal", minimum=1)
    name = p["name"]
    if not isinstance(name, str) or not name:
        raise R5SourceBackedAdapterError("variable name must be non-empty")
    if p["storage_type"] is not None and not isinstance(p["storage_type"], str):
        raise R5SourceBackedAdapterError("variable storage_type malformed")
    if row.object_id != f"source:{source_sha}:variable:{ordinal}":
        raise R5SourceBackedAdapterError("source variable object id mismatch")
    _decode_exact(codec, p["variable_label"], "variable_label")
    labels = _decode_exact(codec, p["value_labels"], "value_labels")
    display = _decode_exact(codec, p["display_metadata"], "display_metadata")
    topology = _decode_exact(codec, p["topology_metadata"], "topology_metadata")
    if not isinstance(labels, Mapping) or not isinstance(display, Mapping) or not isinstance(topology, Mapping):
        raise R5SourceBackedAdapterError("variable metadata typed maps malformed")
    declarations = p["missing_declarations"]
    if not isinstance(declarations, list):
        raise R5SourceBackedAdapterError("missing declarations must be a canonical list")
    for index, declaration in enumerate(declarations):
        decoded = _decode_exact(codec, declaration, f"missing_declarations[{index}]")
        if not isinstance(decoded, Mapping):
            raise R5SourceBackedAdapterError("missing declaration did not decode as mapping")
    return ordinal, name


def _validate_cell_envelope(
    row: R5CanonicalRow,
    *,
    source_sha: str,
    row_count: int,
    variable_count: int,
) -> tuple[int, int, str]:
    keys = {
        "seam_version", "source_sha256", "row_ordinal", "variable_ordinal",
        "variable_name", "raw_value", "missing_state", "source_missing_declaration",
        "raw_value_label", "explicit_source_coordinates", "source_cell_locator",
    }
    p = _payload(row, relation=SOURCE_CELL_RELATION, family=SOURCE_CELL_FAMILY, keys=keys)
    if p["seam_version"] != SEAM_VERSION or p["source_sha256"] != source_sha:
        raise R5SourceBackedAdapterError("physical cell source/seam mismatch")
    row_no = _int(p["row_ordinal"], "cell row ordinal", minimum=1)
    var_no = _int(p["variable_ordinal"], "cell variable ordinal", minimum=1)
    if row_no > row_count or var_no > variable_count:
        raise R5SourceBackedAdapterError("physical cell coordinate outside source geometry")
    name = p["variable_name"]
    if not isinstance(name, str) or not name:
        raise R5SourceBackedAdapterError("physical cell variable name malformed")
    if p["explicit_source_coordinates"] != [row_no, var_no]:
        raise R5SourceBackedAdapterError("explicit physical coordinates mismatch")
    if row.object_id != f"source:{source_sha}:cell:{row_no}:{var_no}":
        raise R5SourceBackedAdapterError("physical cell object id mismatch")
    locator = p["source_cell_locator"]
    if locator is not None and (
        not isinstance(locator, int) or isinstance(locator, bool) or locator < 0
    ):
        raise R5SourceBackedAdapterError("source_cell_locator malformed")
    try:
        PhysicalMissingState(p["missing_state"])
    except Exception as exc:
        raise R5SourceBackedAdapterError("unknown physical missing state") from exc
    return row_no, var_no, name


def inspect_reopened_r5_physical_source(
    reader: frozen.R5LongShardedReader,
    *,
    expected_source_sha256: str | None = None,
) -> R5SourcePhysicalDescriptor:
    if not isinstance(reader, frozen.R5LongShardedReader):
        raise R5SourceBackedAdapterError("exact frozen R5LongShardedReader required")
    if reader.root.get("carrier_schema_version") != frozen.CARRIER_SCHEMA_VERSION:
        raise R5SourceBackedAdapterError("R5 compact carrier schema mismatch")
    if reader.root.get("typed_codec_version") != CODEC_VERSION:
        raise R5SourceBackedAdapterError("R5 typed codec version mismatch")
    source_ref = reader.release_identity.get("source_artifact_ref")
    if not isinstance(source_ref, Mapping):
        raise R5SourceBackedAdapterError("R5 release identity lacks exact source artifact ref")
    root_source_sha = _sha(source_ref.get("content_hash"), "R5 release source SHA")
    if not isinstance(source_ref.get("kind"), str) or not source_ref.get("kind"):
        raise R5SourceBackedAdapterError("R5 release source ref kind missing")
    if not isinstance(source_ref.get("object_id"), str) or not source_ref.get("object_id"):
        raise R5SourceBackedAdapterError("R5 release source ref object_id missing")
    if expected_source_sha256 is not None and root_source_sha != _sha(expected_source_sha256, "expected source SHA"):
        raise R5SourceBackedAdapterError("R5 release source SHA differs from expected source")

    codec = R5TypedValueCodec()
    metadata: dict[str, Any] | None = None
    variables: dict[int, str] = {}
    names: set[str] = set()
    observed_slots: set[tuple[int, str]] = set()
    cell_count = 0

    def collect_and_wire(row: R5CanonicalRow) -> bytes:
        nonlocal metadata, cell_count
        wire = frozen._logical_wire(row)
        if row.relation == SOURCE_METADATA_RELATION:
            if metadata is not None:
                raise R5SourceBackedAdapterError("multiple source metadata rows")
            metadata = _validate_metadata(row, codec)
            if metadata["source_sha256"] != root_source_sha:
                raise R5SourceBackedAdapterError("R5 metadata/source-ref SHA mismatch")
        elif row.relation == SOURCE_CELL_RELATION:
            if metadata is None:
                raise R5SourceBackedAdapterError("physical cell precedes exact source metadata")
            row_no, var_no, name = _validate_cell_envelope(
                row,
                source_sha=root_source_sha,
                row_count=metadata["row_count"],
                variable_count=metadata["variable_count"],
            )
            observed_slots.add((var_no, name))
            cell_count += 1
        elif row.relation == SOURCE_VARIABLE_RELATION:
            if metadata is None:
                raise R5SourceBackedAdapterError("source variable precedes exact source metadata")
            ordinal, name = _validate_variable(row, codec, root_source_sha)
            if ordinal in variables or name in names:
                raise R5SourceBackedAdapterError("duplicate source variable ordinal/name")
            variables[ordinal] = name
            names.add(name)
        return wire

    audit = single_pass_full_audit(reader, logical_wire=collect_and_wire)
    if metadata is None:
        raise R5SourceBackedAdapterError("exact source metadata row missing")
    variable_count = metadata["variable_count"]
    row_count = metadata["row_count"]
    if set(variables) != set(range(1, variable_count + 1)):
        raise R5SourceBackedAdapterError("source variable ordinals do not exactly cover declared geometry")
    declared_slots = {(ordinal, name) for ordinal, name in variables.items()}
    if row_count > 0 and observed_slots != declared_slots:
        raise R5SourceBackedAdapterError("physical cell variable slots diverge from source variable inventory")
    if cell_count != row_count * variable_count:
        raise R5SourceBackedAdapterError("physical cell count does not bind exact row/variable geometry")

    return R5SourcePhysicalDescriptor(
        source_sha256=root_source_sha,
        row_count=row_count,
        variable_count=variable_count,
        variable_slots=tuple(sorted(declared_slots)),
        physical_root_id=audit["physical_root_id"],
        logical_stream_digest=audit["logical_stream_digest"],
        canonical_rows=audit["canonical_rows"],
        relation_counts=dict(audit["relation_counts"]),
    )


def _iter_exact_physical_cells(
    reader: frozen.R5LongShardedReader,
    descriptor: R5SourcePhysicalDescriptor,
):
    codec = R5TypedValueCodec()
    slots = set(descriptor.variable_slots)
    count = 0
    previous_object_id: str | None = None
    for row in reader.iter_rows(relation=SOURCE_CELL_RELATION):
        row_no, var_no, name = _validate_cell_envelope(
            row,
            source_sha=descriptor.source_sha256,
            row_count=descriptor.row_count,
            variable_count=descriptor.variable_count,
        )
        if (var_no, name) not in slots:
            raise R5SourceBackedAdapterError("physical cell variable slot is absent from exact source inventory")
        if previous_object_id is not None and row.object_id <= previous_object_id:
            raise R5SourceBackedAdapterError("physical cell stream is duplicate/noncanonical")
        previous_object_id = row.object_id
        p = row.payload
        raw_value = _decode_exact(codec, p["raw_value"], "physical raw_value")
        declaration = None
        if p["source_missing_declaration"] is not None:
            declaration = _decode_exact(codec, p["source_missing_declaration"], "source_missing_declaration")
            if not isinstance(declaration, Mapping):
                raise R5SourceBackedAdapterError("source missing declaration is not a mapping")
        raw_label = _decode_exact(codec, p["raw_value_label"], "raw_value_label")
        state = PhysicalMissingState(p["missing_state"])
        count += 1
        yield PhysicalCell(
            row_ordinal=row_no,
            variable_ordinal=var_no,
            variable_name=name,
            raw_value=raw_value,
            missing_state=state,
            source_missing_declaration=declaration,
            raw_value_label=raw_label,
        )
    if count != descriptor.row_count * descriptor.variable_count:
        raise R5SourceBackedAdapterError("reopened physical-cell stream cardinality changed after audit")


def prepare_r5_exact_physical_cell_stream(
    reader: frozen.R5LongShardedReader,
    *,
    expected_source_sha256: str | None = None,
) -> tuple[ExactPhysicalCellStream, R5SourcePhysicalDescriptor]:
    descriptor = inspect_reopened_r5_physical_source(
        reader, expected_source_sha256=expected_source_sha256
    )
    stream = ExactPhysicalCellStream(
        source_sha256=descriptor.source_sha256,
        row_count=descriptor.row_count,
        cell_iter_factory=lambda: _iter_exact_physical_cells(reader, descriptor),
        transport_identity=f"{CONTRACT_ID}:{descriptor.physical_root_id}",
    )
    return stream, descriptor


def build_r5_source_backed_c11_repository(
    reader: frozen.R5LongShardedReader,
    projection: GovernedC11Projection,
):
    if not isinstance(projection, GovernedC11Projection):
        raise R5SourceBackedAdapterError("explicit GovernedC11Projection required")
    stream, descriptor = prepare_r5_exact_physical_cell_stream(
        reader, expected_source_sha256=projection.expected_source_sha256
    )
    repository, release = build_source_backed_c11_repository(
        stream, projection, cache=None
    )
    if release.source_artifact_ref.content_hash != descriptor.source_sha256:
        raise R5SourceBackedAdapterError("C05R2A release lost exact source SHA binding")
    return repository, release, descriptor


__all__ = [
    "CONTRACT_ID",
    "R5SourceBackedAdapterError",
    "R5SourcePhysicalDescriptor",
    "inspect_reopened_r5_physical_source",
    "prepare_r5_exact_physical_cell_stream",
    "build_r5_source_backed_c11_repository",
]
