"""Frozen Route-C CACC1/CACC2 accelerators and exact-engine parity adapter.

Authority remains exact source + governed C11/I03/I05 objects.  These objects are
optional, content-addressed execution representations only.  They never define
semantic truth, candidate reachability, terminal states, or learned products.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import shutil
from typing import Any, Callable, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, exact_ref, semantic_hash
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
    GovernedC11Projection,
    SourceBackedC11FacadeError,
    build_source_backed_c11_repository,
    physical_value_binding_key,
)


ROUTE_C_CANDIDATE_HASH = "a476e6e44c21b8029ae5d3e6d387428a5fa19549a2126d61aae7c71c50c64a3c"
ROUTE_C_DELETE_REBUILD_LAW_HASH = "a582e303c8cd4ffabd3971ddc0b2d4b37d6d7327707e4df9778660088171cacc"
PINNED_PYARROW_VERSION = "25.0.1"
FROZEN_LITS1_SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
FROZEN_LITS1_C11_RELEASE_HASH = "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
FROZEN_PREDICATE_SEMANTIC_CATALOG_HASH = "8c559917640242e017b03e206d5a0a950cb2973c36a90e0be43d3c0fe7cc9293"
FROZEN_RISK_TOPOLOGY_PARTITION_HASH = "ed3b76242a588a5e2d4dacbb76f17ceef6185cd27a4080a2e8fb436056abfabf"
SUCCESSOR_DISCOVERY_AUTHORITY_HASH = "2e153a153c59bd0b920f8db376478ad1b07000710e79a158471490c11b610cea"
SUCCESSOR_OFFICIAL_FRONTIER_HASH = "7aca4dbe1ccd36c48444d6858d378084e41aa30b3197662b6225753d5fc82e24"
PRODUCTION_DISCOVERY_OPERATION = "PRE553_PRODUCTION_EXACT_BOUNDED_AUTONOMOUS_DISCOVERY@1.0.0"

CACC1_ID = "CACC1_LITS1_SEMANTIC_EXECUTION_BUNDLE"
CACC1_FORMAT = "AS3_CANONICAL_ARROW_IPC_EXECUTION_BUNDLE_V1"
CACC2_ID = "CACC2_FRONTIER_ATOMIC_PREDICATE_RISK_MASK_BANK"
CACC2_FORMAT = "AS3_DENSE_BITSET_BANK_V1"

CACC1_FIELD_ORDER = (
    "row_ordinal",
    "q301_2_raw",
    "q301_2_state",
    "q301_7_raw",
    "q301_7_state",
    "country_raw_cjson",
    "city_raw_cjson",
    "region_raw_cjson",
    "tablec_raw_cjson",
    "tabled_raw_cjson",
    "q301_risk_member",
)
CACC1_RESPONSE_NAMES = ("q301_2", "q301_7")
CACC1_COORDINATE_NAMES = ("country", "city", "region", "tablec", "tabled")
CACC1_PROJECTED_NAMES = CACC1_RESPONSE_NAMES + CACC1_COORDINATE_NAMES
CACC2_FROZEN_ROLE_ORDER = (
    "A000",
    "A1V1", "A1V2", "A1V3", "A1V4", "A1V5",
    "A1SSUB", "A1SSPS", "A1SMIS", "A1RAPP",
    "A2V1", "A2V2", "A2V3", "A2V4", "A2V5",
    "A2SSUB", "A2SSPS", "A2SMIS", "A2RAPP",
)
_ALLOWED_CACC2_MANIFEST_KEYS = {
    "schema", "accelerator_id", "format", "route_c_candidate_hash",
    "determinant_hash", "determinants", "row_count", "mask_byte_length",
    "bit_index", "bit_order_within_byte", "trailing_unused_bits",
    "entry_order", "risk_entry", "atom_entries", "logical_content_hash",
}


class RouteCAcceleratorError(RuntimeError):
    pass


class RouteCDeterminantMismatch(RouteCAcceleratorError):
    pass


class RouteCCorruptAccelerator(RouteCAcceleratorError):
    pass


class RouteCUnsupportedEnvironment(RouteCAcceleratorError):
    pass


def _cjson(value: Any) -> str:
    return json.dumps(
        canonicalize(value), sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    )


def _load_cjson(text: str) -> Any:
    if not isinstance(text, str):
        raise RouteCCorruptAccelerator("canonical JSON field must be UTF-8 text")
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RouteCCorruptAccelerator("invalid canonical JSON field") from exc
    if _cjson(value) != text:
        raise RouteCCorruptAccelerator("noncanonical JSON field")
    return value


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _require_sha(value: Any, label: str) -> str:
    if (
        not isinstance(value, str) or len(value) != 64 or value.lower() != value
        or any(ch not in "0123456789abcdef" for ch in value)
    ):
        raise RouteCDeterminantMismatch(f"{label} must be lowercase SHA-256")
    return value


def _write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def _write_json_atomic(path: Path, value: Mapping[str, Any]) -> None:
    _write_atomic(path, (_cjson(value) + "\n").encode("utf-8"))


def _load_json_object(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RouteCCorruptAccelerator(f"cannot load {path}") from exc
    if not isinstance(value, Mapping):
        raise RouteCCorruptAccelerator(f"{path} must contain one JSON object")
    return value


def _ref_dict(ref: ExactRef) -> Mapping[str, Any]:
    return exact_ref(ref, "exact ref").as_dict()


def _ref_from_dict(value: Mapping[str, Any]) -> ExactRef:
    if not isinstance(value, Mapping):
        raise RouteCCorruptAccelerator("exact ref must be an object")
    try:
        return ExactRef(str(value["kind"]), str(value["object_id"]), str(value["content_hash"]))
    except (KeyError, TypeError, ValueError) as exc:
        raise RouteCCorruptAccelerator("malformed exact ref") from exc


@dataclass(frozen=True)
class RouteCDeterminants:
    source_sha256: str
    decoder_identity: Mapping[str, Any]
    projection_authority_hash: str
    slot_ledger_hash: str
    governed_projection_hash: str
    c11_logical_release_hash: str
    replay_manifest_hash: str
    semantic_authority_closure_hash: str

    def __post_init__(self) -> None:
        for name in (
            "source_sha256", "projection_authority_hash", "slot_ledger_hash",
            "governed_projection_hash", "c11_logical_release_hash",
            "replay_manifest_hash", "semantic_authority_closure_hash",
        ):
            _require_sha(getattr(self, name), name)
        if not isinstance(self.decoder_identity, Mapping) or not self.decoder_identity:
            raise RouteCDeterminantMismatch("decoder_identity must be an exact nonempty mapping")

    def as_dict(self) -> Mapping[str, Any]:
        return {
            "source_sha256": self.source_sha256,
            "decoder_identity": canonicalize(self.decoder_identity),
            "projection_authority_hash": self.projection_authority_hash,
            "slot_ledger_hash": self.slot_ledger_hash,
            "governed_projection_hash": self.governed_projection_hash,
            "c11_logical_release_hash": self.c11_logical_release_hash,
            "replay_manifest_hash": self.replay_manifest_hash,
            "semantic_authority_closure_hash": self.semantic_authority_closure_hash,
        }

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.as_dict())

    def require_frozen_lits1_scope(self) -> None:
        if self.source_sha256 != FROZEN_LITS1_SOURCE_SHA256:
            raise RouteCDeterminantMismatch("Route-C candidate is frozen to exact LiTS-I source SHA")
        if self.c11_logical_release_hash != FROZEN_LITS1_C11_RELEASE_HASH:
            raise RouteCDeterminantMismatch("Route-C candidate is frozen to exact accepted LiTS-I C11 release")


@dataclass(frozen=True)
class Cacc1Paths:
    arrow_ipc: Path
    manifest: Path


@dataclass(frozen=True)
class Cacc1Bundle:
    paths: Cacc1Paths
    manifest: Mapping[str, Any]
    rows: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True)
class Cacc2AtomBinding:
    role_id: str
    semantic_atom_content_hash: str
    runtime_predicate_ref: ExactRef

    def __post_init__(self) -> None:
        if self.role_id not in CACC2_FROZEN_ROLE_ORDER:
            raise RouteCDeterminantMismatch(f"unknown frozen atom role {self.role_id!r}")
        _require_sha(self.semantic_atom_content_hash, "semantic_atom_content_hash")
        exact_ref(self.runtime_predicate_ref, "runtime_predicate_ref")


@dataclass(frozen=True)
class Cacc2Determinants:
    cacc1_determinant_hash: str
    discovery_authority_ref: ExactRef
    predicate_catalog_hash: str
    risk_partition_hash: str
    production_operation_identity: str
    candidate_frontier_ref: ExactRef

    def __post_init__(self) -> None:
        _require_sha(self.cacc1_determinant_hash, "cacc1_determinant_hash")
        exact_ref(self.discovery_authority_ref, "discovery_authority_ref")
        exact_ref(self.candidate_frontier_ref, "candidate_frontier_ref")
        _require_sha(self.predicate_catalog_hash, "predicate_catalog_hash")
        _require_sha(self.risk_partition_hash, "risk_partition_hash")
        if not isinstance(self.production_operation_identity, str) or not self.production_operation_identity:
            raise RouteCDeterminantMismatch("production_operation_identity required")

    def as_dict(self) -> Mapping[str, Any]:
        return {
            "cacc1_determinant_hash": self.cacc1_determinant_hash,
            "discovery_authority_ref": _ref_dict(self.discovery_authority_ref),
            "predicate_catalog_hash": self.predicate_catalog_hash,
            "risk_partition_hash": self.risk_partition_hash,
            "production_operation_identity": self.production_operation_identity,
            "candidate_frontier_ref": _ref_dict(self.candidate_frontier_ref),
        }

    @property
    def content_hash(self) -> str:
        return semantic_hash(self.as_dict())

    def require_successor_frozen_scope(self) -> None:
        if self.discovery_authority_ref.content_hash != SUCCESSOR_DISCOVERY_AUTHORITY_HASH:
            raise RouteCDeterminantMismatch("CACC2 must bind the accepted AS3R3 successor DiscoveryAuthority")
        if self.candidate_frontier_ref.content_hash != SUCCESSOR_OFFICIAL_FRONTIER_HASH:
            raise RouteCDeterminantMismatch("CACC2 must bind the accepted AS3R3 successor frontier")
        if self.predicate_catalog_hash != FROZEN_PREDICATE_SEMANTIC_CATALOG_HASH:
            raise RouteCDeterminantMismatch("CACC2 predicate semantic catalog changed")
        if self.risk_partition_hash != FROZEN_RISK_TOPOLOGY_PARTITION_HASH:
            raise RouteCDeterminantMismatch("CACC2 risk/topology partition changed")
        if self.production_operation_identity != PRODUCTION_DISCOVERY_OPERATION:
            raise RouteCDeterminantMismatch("CACC2 production operation identity changed")


def _pa():
    try:
        import pyarrow as pa
    except Exception as exc:
        raise RouteCUnsupportedEnvironment(
            "CACC1 requires pinned pyarrow to emit AS3 canonical Arrow IPC; "
            "no substitute physical format is authorized"
        ) from exc
    if str(pa.__version__) != PINNED_PYARROW_VERSION:
        raise RouteCUnsupportedEnvironment(
            "CACC1 Arrow implementation/version mismatch: "
            f"required pyarrow=={PINNED_PYARROW_VERSION}, observed {pa.__version__}"
        )
    return pa


def _cacc1_schema(pa):
    return pa.schema([
        pa.field("row_ordinal", pa.int64(), nullable=False),
        pa.field("q301_2_raw", pa.string(), nullable=False),
        pa.field("q301_2_state", pa.string(), nullable=False),
        pa.field("q301_7_raw", pa.string(), nullable=False),
        pa.field("q301_7_state", pa.string(), nullable=False),
        pa.field("country_raw_cjson", pa.string(), nullable=False),
        pa.field("city_raw_cjson", pa.string(), nullable=False),
        pa.field("region_raw_cjson", pa.string(), nullable=False),
        pa.field("tablec_raw_cjson", pa.string(), nullable=False),
        pa.field("tabled_raw_cjson", pa.string(), nullable=False),
        pa.field("q301_risk_member", pa.bool_(), nullable=False),
    ])


def _slot_maps(projection: GovernedC11Projection):
    if not isinstance(projection, GovernedC11Projection):
        raise RouteCDeterminantMismatch("exact GovernedC11Projection required")
    response = {slot.slot.name: slot for slot in projection.response_slots}
    coordinate = {slot.slot.name: slot for slot in projection.coordinate_slots}
    if not set(CACC1_RESPONSE_NAMES).issubset(response):
        raise RouteCDeterminantMismatch("projection omits q301_2/q301_7 response slots")
    if not set(CACC1_COORDINATE_NAMES).issubset(coordinate):
        raise RouteCDeterminantMismatch("projection omits frozen five coordinate slots")
    return response, coordinate


def _projected_response_state(cell: PhysicalCell, slot) -> str:
    key = physical_value_binding_key(
        cell.raw_value, cell.missing_state, cell.source_missing_declaration
    )
    matches = [value for value in slot.values if value.physical_key == key]
    if len(matches) != 1:
        raise RouteCAcceleratorError(
            f"physical cell {cell.variable_name}@{cell.row_ordinal} has no unique governed response binding"
        )
    return matches[0].response_state


def _routing_membership(projection: GovernedC11Projection) -> tuple[Mapping[Any, bool], ExactRef]:
    response, _ = _slot_maps(projection)
    qrefs = {name: response[name].question_binding.native_question_ref for name in CACC1_RESPONSE_NAMES}
    rows = {binding.respondent_ref: binding.row_ordinal for binding in projection.row_bindings}
    by_pair: dict[tuple[Any, Any], Any] = {}
    for fact in projection.routing:
        pair = (
            exact_ref(fact.scoped_respondent_ref, "routing scoped_respondent_ref"),
            exact_ref(fact.question_or_target_ref, "routing question_or_target_ref"),
        )
        if pair in by_pair:
            raise RouteCAcceleratorError("duplicate q301 routing fact")
        by_pair[pair] = fact
    result: dict[Any, bool] = {}
    risk_ref = None
    for respondent_ref, row in rows.items():
        facts = []
        for name in CACC1_RESPONSE_NAMES:
            fact = by_pair.get((respondent_ref, qrefs[name]))
            if fact is None:
                raise RouteCAcceleratorError("missing exact q301 routing fact")
            facts.append(fact)
        refs = {exact_ref(fact.risk_set_ref, "routing risk_set_ref") for fact in facts}
        if len(refs) != 1:
            raise RouteCAcceleratorError("q301 common routing facts disagree on exact risk ref")
        current_ref = next(iter(refs))
        if risk_ref is None:
            risk_ref = current_ref
        elif current_ref != risk_ref:
            raise RouteCAcceleratorError("q301 common risk ref varies across respondents")
        states = [
            fact.routing_state == "ELIGIBLE_APPLICABLE"
            and fact.applicability_state == "ELIGIBLE_APPLICABLE"
            for fact in facts
        ]
        if states[0] != states[1]:
            raise RouteCAcceleratorError("q301_2/q301_7 common-risk membership diverges")
        result[row] = states[0]
    if risk_ref is None:
        raise RouteCAcceleratorError("empty q301 risk routing closure")
    return result, exact_ref(risk_ref, "q301 common risk ref")


def _state_envelope(cell: PhysicalCell, projected_state: str) -> str:
    if cell.source_missing_declaration is not None:
        raise RouteCAcceleratorError(
            "frozen CACC1 logical layout has no source-missing-declaration field; "
            "fallback to cacheless exact source rather than widen accelerator semantics"
        )
    return _cjson({
        "physical_missing_state": cell.missing_state.value,
        "projected_response_typed_state": projected_state,
    })


def _coordinate_envelope(cell: PhysicalCell) -> str:
    if cell.source_missing_declaration is not None:
        raise RouteCAcceleratorError(
            "frozen CACC1 coordinate layout has no source-missing-declaration field; "
            "fallback to cacheless exact source rather than widen accelerator semantics"
        )
    return _cjson({
        "raw_value": canonicalize(cell.raw_value),
        "physical_missing_state": cell.missing_state.value,
    })


def materialize_cacc1_rows(
    stream: ExactPhysicalCellStream,
    projection: GovernedC11Projection,
) -> tuple[tuple[Mapping[str, Any], ...], ExactRef]:
    if not isinstance(stream, ExactPhysicalCellStream):
        raise RouteCDeterminantMismatch("CACC1 builder requires ExactPhysicalCellStream")
    if stream.source_sha256 != projection.expected_source_sha256:
        raise RouteCDeterminantMismatch("CACC1 source/projection SHA mismatch")
    response, coordinate = _slot_maps(projection)
    membership, risk_ref = _routing_membership(projection)
    selected: dict[int, dict[str, PhysicalCell]] = {}
    for cell in stream.iter_cells():
        if not isinstance(cell, PhysicalCell):
            raise RouteCAcceleratorError("CACC1 physical stream contains non-PhysicalCell")
        if cell.variable_name not in CACC1_PROJECTED_NAMES:
            continue
        row = selected.setdefault(cell.row_ordinal, {})
        if cell.variable_name in row:
            raise RouteCAcceleratorError("duplicate CACC1 row/slot physical cell")
        row[cell.variable_name] = cell
    if set(selected) != set(range(1, stream.row_count + 1)):
        raise RouteCAcceleratorError("CACC1 physical stream does not cover exact row ordinals")
    rows = []
    for row_ordinal in range(1, stream.row_count + 1):
        cells = selected[row_ordinal]
        if set(cells) != set(CACC1_PROJECTED_NAMES):
            raise RouteCAcceleratorError("CACC1 row does not contain exactly frozen seven projected slots")
        q2, q7 = cells["q301_2"], cells["q301_7"]
        row = {
            "row_ordinal": row_ordinal,
            "q301_2_raw": _cjson(q2.raw_value),
            "q301_2_state": _state_envelope(q2, _projected_response_state(q2, response["q301_2"])),
            "q301_7_raw": _cjson(q7.raw_value),
            "q301_7_state": _state_envelope(q7, _projected_response_state(q7, response["q301_7"])),
            "country_raw_cjson": _coordinate_envelope(cells["country"]),
            "city_raw_cjson": _coordinate_envelope(cells["city"]),
            "region_raw_cjson": _coordinate_envelope(cells["region"]),
            "tablec_raw_cjson": _coordinate_envelope(cells["tablec"]),
            "tabled_raw_cjson": _coordinate_envelope(cells["tabled"]),
            "q301_risk_member": bool(membership[row_ordinal]),
        }
        if tuple(row) != CACC1_FIELD_ORDER:
            raise RouteCAcceleratorError("internal CACC1 field-order violation")
        rows.append(row)
    return tuple(rows), risk_ref


def _logical_cacc1_hash(rows: Sequence[Mapping[str, Any]], risk_ref: ExactRef) -> str:
    return semantic_hash({
        "format": CACC1_FORMAT,
        "field_order": CACC1_FIELD_ORDER,
        "risk_ref": risk_ref.as_dict(),
        "rows": [canonicalize(row) for row in rows],
    })


def build_cacc1(
    *,
    stream: ExactPhysicalCellStream,
    projection: GovernedC11Projection,
    determinants: RouteCDeterminants,
    paths: Cacc1Paths,
    require_frozen_lits1: bool = False,
) -> Cacc1Bundle:
    if require_frozen_lits1:
        determinants.require_frozen_lits1_scope()
    if determinants.source_sha256 != stream.source_sha256:
        raise RouteCDeterminantMismatch("CACC1 determinant/source SHA mismatch")
    if determinants.governed_projection_hash != projection.cache_identity:
        raise RouteCDeterminantMismatch("CACC1 governed projection determinant mismatch")
    rows, risk_ref = materialize_cacc1_rows(stream, projection)
    pa = _pa()
    schema = _cacc1_schema(pa)
    arrays = [pa.array([row[name] for row in rows], type=schema.field(name).type) for name in CACC1_FIELD_ORDER]
    batch = pa.RecordBatch.from_arrays(arrays, schema=schema)
    paths.arrow_ipc.parent.mkdir(parents=True, exist_ok=True)
    tmp = paths.arrow_ipc.with_name(paths.arrow_ipc.name + ".tmp")
    options = pa.ipc.IpcWriteOptions(compression=None)
    with pa.OSFile(str(tmp), "wb") as sink:
        with pa.ipc.new_file(sink, schema, options=options) as writer:
            writer.write_batch(batch)
    os.replace(tmp, paths.arrow_ipc)
    physical_hash = _sha256_file(paths.arrow_ipc)
    logical_hash = _logical_cacc1_hash(rows, risk_ref)
    manifest = {
        "schema": "AS4I_ROUTE_C_CACC1_MANIFEST@1.0.0",
        "accelerator_id": CACC1_ID,
        "format": CACC1_FORMAT,
        "route_c_candidate_hash": ROUTE_C_CANDIDATE_HASH,
        "field_order": list(CACC1_FIELD_ORDER),
        "record_order": "SOURCE_ROW_ORDINAL_ASCENDING",
        "record_batch_count": 1,
        "compression": "NONE",
        "dictionary_encoding": "NONE",
        "arrow_implementation": "pyarrow",
        "arrow_version": str(pa.__version__),
        "determinant_hash": determinants.content_hash,
        "determinants": determinants.as_dict(),
        "row_count": len(rows),
        "q301_common_risk_ref": risk_ref.as_dict(),
        "logical_content_hash": logical_hash,
        "physical_byte_sha256": physical_hash,
    }
    _write_json_atomic(paths.manifest, manifest)
    return Cacc1Bundle(paths, manifest, rows)


def _validate_cacc1_row(row: Mapping[str, Any], expected_ordinal: int) -> None:
    if tuple(row) != CACC1_FIELD_ORDER:
        raise RouteCCorruptAccelerator("CACC1 field order changed")
    if row["row_ordinal"] != expected_ordinal:
        raise RouteCCorruptAccelerator("CACC1 row order/ordinal changed")
    if not isinstance(row["q301_risk_member"], bool):
        raise RouteCCorruptAccelerator("CACC1 risk membership must be Boolean")
    _load_cjson(row["q301_2_raw"])
    _load_cjson(row["q301_7_raw"])
    for name in ("q301_2_state", "q301_7_state"):
        state = _load_cjson(row[name])
        if not isinstance(state, Mapping):
            raise RouteCCorruptAccelerator("CACC1 response state envelope malformed")
        if set(state) != {"physical_missing_state", "projected_response_typed_state"}:
            raise RouteCCorruptAccelerator("CACC1 response state envelope changed")
        try:
            PhysicalMissingState(state["physical_missing_state"])
        except Exception as exc:
            raise RouteCCorruptAccelerator("CACC1 physical missing state invalid") from exc
    for name in CACC1_COORDINATE_NAMES:
        envelope = _load_cjson(row[f"{name}_raw_cjson"])
        if not isinstance(envelope, Mapping) or set(envelope) != {
            "raw_value", "physical_missing_state",
        }:
            raise RouteCCorruptAccelerator("CACC1 coordinate envelope changed")
        try:
            PhysicalMissingState(envelope["physical_missing_state"])
        except Exception as exc:
            raise RouteCCorruptAccelerator("CACC1 coordinate missing state invalid") from exc


def read_cacc1(
    *,
    paths: Cacc1Paths,
    expected_determinants: RouteCDeterminants,
) -> Cacc1Bundle:
    manifest = _load_json_object(paths.manifest)
    if manifest.get("accelerator_id") != CACC1_ID or manifest.get("format") != CACC1_FORMAT:
        raise RouteCCorruptAccelerator("CACC1 identity/format mismatch")
    if manifest.get("route_c_candidate_hash") != ROUTE_C_CANDIDATE_HASH:
        raise RouteCCorruptAccelerator("CACC1 candidate identity mismatch")
    if manifest.get("determinant_hash") != expected_determinants.content_hash:
        raise RouteCDeterminantMismatch("CACC1 stale determinant key")
    if canonicalize(manifest.get("determinants")) != canonicalize(expected_determinants.as_dict()):
        raise RouteCDeterminantMismatch("CACC1 determinant material mismatch")
    if tuple(manifest.get("field_order", ())) != CACC1_FIELD_ORDER:
        raise RouteCCorruptAccelerator("CACC1 frozen field order mismatch")
    if manifest.get("record_batch_count") != 1 or manifest.get("compression") != "NONE":
        raise RouteCCorruptAccelerator("CACC1 batch/compression law mismatch")
    if manifest.get("dictionary_encoding") != "NONE":
        raise RouteCCorruptAccelerator("CACC1 dictionary encoding forbidden")
    if manifest.get("arrow_implementation") != "pyarrow":
        raise RouteCDeterminantMismatch("CACC1 Arrow implementation mismatch")
    if manifest.get("arrow_version") != PINNED_PYARROW_VERSION:
        raise RouteCDeterminantMismatch("CACC1 Arrow implementation/version mismatch")
    if not paths.arrow_ipc.is_file():
        raise RouteCCorruptAccelerator("CACC1 Arrow IPC bytes missing")
    if _sha256_file(paths.arrow_ipc) != manifest.get("physical_byte_sha256"):
        raise RouteCCorruptAccelerator("CACC1 physical byte SHA mismatch")
    pa = _pa()
    with pa.memory_map(str(paths.arrow_ipc), "r") as source:
        reader = pa.ipc.open_file(source)
        if reader.num_record_batches != 1:
            raise RouteCCorruptAccelerator("CACC1 must contain exactly one record batch")
        batch = reader.get_batch(0)
        if not batch.schema.equals(_cacc1_schema(pa), check_metadata=True):
            raise RouteCCorruptAccelerator("CACC1 Arrow schema changed")
        data = batch.to_pydict()
        row_count = batch.num_rows
    rows = []
    for index in range(row_count):
        row = {name: data[name][index] for name in CACC1_FIELD_ORDER}
        _validate_cacc1_row(row, index + 1)
        rows.append(row)
    risk_ref = _ref_from_dict(manifest.get("q301_common_risk_ref"))
    logical_hash = _logical_cacc1_hash(rows, risk_ref)
    if logical_hash != manifest.get("logical_content_hash"):
        raise RouteCCorruptAccelerator("CACC1 logical content hash mismatch")
    if manifest.get("row_count") != row_count:
        raise RouteCCorruptAccelerator("CACC1 row count mismatch")
    return Cacc1Bundle(paths, manifest, tuple(rows))


def _projection_slot_ordinals(projection: GovernedC11Projection) -> Mapping[str, int]:
    response, coordinate = _slot_maps(projection)
    return {
        **{name: response[name].slot.ordinal for name in CACC1_RESPONSE_NAMES},
        **{name: coordinate[name].slot.ordinal for name in CACC1_COORDINATE_NAMES},
    }


def _row_to_cells(row: Mapping[str, Any], projection: GovernedC11Projection) -> tuple[PhysicalCell, ...]:
    ordinals = _projection_slot_ordinals(projection)
    response, _ = _slot_maps(projection)
    result = []
    for name in CACC1_RESPONSE_NAMES:
        raw = _load_cjson(row[f"{name}_raw"])
        state = _load_cjson(row[f"{name}_state"])
        physical_state = PhysicalMissingState(state["physical_missing_state"])
        cell = PhysicalCell(
            row["row_ordinal"], ordinals[name], name, raw, physical_state, None, None
        )
        projected = _projected_response_state(cell, response[name])
        if projected != state["projected_response_typed_state"]:
            raise RouteCDeterminantMismatch(
                f"CACC1 governed projected state stale for {name}@{row['row_ordinal']}"
            )
        result.append(cell)
    for name in CACC1_COORDINATE_NAMES:
        envelope = _load_cjson(row[f"{name}_raw_cjson"])
        result.append(PhysicalCell(
            row["row_ordinal"], ordinals[name], name, envelope["raw_value"],
            PhysicalMissingState(envelope["physical_missing_state"]),
            None, None,
        ))
    return tuple(result)


def cacc1_to_exact_physical_stream(
    bundle: Cacc1Bundle,
    projection: GovernedC11Projection,
) -> ExactPhysicalCellStream:
    source_sha = str(bundle.manifest.get("determinants", {}).get("source_sha256", ""))
    _require_sha(source_sha, "CACC1 manifest source_sha256")
    if source_sha != projection.expected_source_sha256:
        raise RouteCDeterminantMismatch("CACC1/projection source SHA mismatch")
    rows = bundle.rows

    def factory():
        for row in rows:
            yield from _row_to_cells(row, projection)

    return ExactPhysicalCellStream(
        source_sha256=source_sha,
        row_count=len(rows),
        cell_iter_factory=factory,
        transport_identity="AS3_ROUTE_C_CACC1_EXACT_REPLAY_EQUIVALENT_PHYSICAL_CELL_STREAM",
    )


def delete_cacc1(paths: Cacc1Paths) -> None:
    for path in (paths.arrow_ipc, paths.manifest):
        try:
            path.unlink()
        except FileNotFoundError:
            pass


def _pack_mask(row_count: int, members: Iterable[int]) -> bytes:
    if not isinstance(row_count, int) or isinstance(row_count, bool) or row_count < 1:
        raise RouteCAcceleratorError("row_count must be positive integer")
    data = bytearray((row_count + 7) // 8)
    seen = set()
    for row in members:
        if not isinstance(row, int) or isinstance(row, bool) or not 1 <= row <= row_count:
            raise RouteCAcceleratorError("mask row ordinal outside exact source universe")
        if row in seen:
            raise RouteCAcceleratorError("duplicate mask row ordinal")
        seen.add(row)
        index = row - 1
        data[index // 8] |= 1 << (index % 8)
    return bytes(data)


def _validate_mask_bytes(data: bytes, row_count: int) -> None:
    expected = (row_count + 7) // 8
    if len(data) != expected:
        raise RouteCCorruptAccelerator("CACC2 mask byte length mismatch")
    unused = expected * 8 - row_count
    if unused:
        allowed = (1 << (8 - unused)) - 1
        if data[-1] & ~allowed:
            raise RouteCCorruptAccelerator("CACC2 trailing unused bits must be zero")


def mask_member(data: bytes, row_ordinal: int, row_count: int) -> bool:
    _validate_mask_bytes(data, row_count)
    if not 1 <= row_ordinal <= row_count:
        raise RouteCAcceleratorError("row ordinal outside mask universe")
    index = row_ordinal - 1
    return bool(data[index // 8] & (1 << (index % 8)))


def mask_member_count(data: bytes, row_count: int) -> int:
    _validate_mask_bytes(data, row_count)
    return sum(byte.bit_count() for byte in data)


def _role_members(rows: Sequence[Mapping[str, Any]], role_id: str) -> tuple[int, ...]:
    result = []
    for row in rows:
        ordinal = row["row_ordinal"]
        risk = bool(row["q301_risk_member"])
        if role_id in {"A000", "A1RAPP", "A2RAPP"}:
            matched = risk
        else:
            side = "q301_2" if role_id.startswith("A1") else "q301_7"
            state = _load_cjson(row[f"{side}_state"])["projected_response_typed_state"]
            raw = _load_cjson(row[f"{side}_raw"])
            if role_id.endswith("SSUB"):
                matched = state == "SUBSTANTIVE_RESPONSE"
            elif role_id.endswith("SSPS"):
                matched = state == "SOURCE_SPECIFIC_SPECIAL"
            elif role_id.endswith("SMIS"):
                matched = state == "MISSING"
            elif "V" in role_id:
                try:
                    exact_value = int(role_id.split("V", 1)[1])
                except ValueError as exc:
                    raise RouteCAcceleratorError("invalid frozen value atom role") from exc
                matched = state == "SUBSTANTIVE_RESPONSE" and raw == exact_value
            else:
                raise RouteCAcceleratorError(f"unimplemented frozen atom role {role_id}")
        if matched:
            result.append(ordinal)
    return tuple(result)


def build_cacc2(
    *,
    directory: Path,
    cacc1: Cacc1Bundle,
    determinants: Cacc2Determinants,
    atom_bindings: Iterable[Cacc2AtomBinding],
    require_successor_frozen_scope: bool = False,
) -> Mapping[str, Any]:
    if require_successor_frozen_scope:
        determinants.require_successor_frozen_scope()
    bindings = tuple(atom_bindings)
    if {b.role_id for b in bindings} != set(CACC2_FROZEN_ROLE_ORDER):
        raise RouteCDeterminantMismatch("CACC2 requires exactly all 19 frozen semantic atom roles")
    if len(bindings) != len(CACC2_FROZEN_ROLE_ORDER):
        raise RouteCDeterminantMismatch("duplicate CACC2 atom role binding")
    if determinants.cacc1_determinant_hash != cacc1.manifest.get("determinant_hash"):
        raise RouteCDeterminantMismatch("CACC2/CACC1 determinant linkage mismatch")
    rows = cacc1.rows
    row_count = len(rows)
    directory.mkdir(parents=True, exist_ok=True)
    risk_members = tuple(row["row_ordinal"] for row in rows if row["q301_risk_member"])
    risk_bytes = _pack_mask(row_count, risk_members)
    risk_name = "risk_q301_common.mask"
    _write_atomic(directory / risk_name, risk_bytes)
    risk_entry = {
        "entry_kind": "COMMON_RISK_SET",
        "file": risk_name,
        "sha256": _sha256_bytes(risk_bytes),
        "member_count": len(risk_members),
        "risk_ref": canonicalize(cacc1.manifest.get("q301_common_risk_ref")),
    }
    entries = []
    for binding in sorted(bindings, key=lambda item: item.semantic_atom_content_hash):
        members = _role_members(rows, binding.role_id)
        data = _pack_mask(row_count, members)
        file_name = f"atom_{binding.semantic_atom_content_hash}.mask"
        _write_atomic(directory / file_name, data)
        entries.append({
            "entry_kind": "FROZEN_ATOM",
            "role_id": binding.role_id,
            "semantic_atom_content_hash": binding.semantic_atom_content_hash,
            "runtime_predicate_ref": binding.runtime_predicate_ref.as_dict(),
            "file": file_name,
            "sha256": _sha256_bytes(data),
            "member_count": len(members),
        })
    logical_material = {
        "format": CACC2_FORMAT,
        "row_count": row_count,
        "risk_entry": risk_entry,
        "atom_entries": entries,
    }
    manifest = {
        "schema": "AS4I_ROUTE_C_CACC2_MANIFEST@1.0.0",
        "accelerator_id": CACC2_ID,
        "format": CACC2_FORMAT,
        "route_c_candidate_hash": ROUTE_C_CANDIDATE_HASH,
        "determinant_hash": determinants.content_hash,
        "determinants": determinants.as_dict(),
        "row_count": row_count,
        "mask_byte_length": len(risk_bytes),
        "bit_index": "ROW_ORDINAL_MINUS_1",
        "bit_order_within_byte": "LSB_FIRST",
        "trailing_unused_bits": "ZERO",
        "entry_order": "SEMANTIC_ATOM_CONTENT_HASH_ASCENDING",
        "risk_entry": risk_entry,
        "atom_entries": entries,
        "logical_content_hash": semantic_hash(logical_material),
    }
    _write_json_atomic(directory / "manifest.json", manifest)
    return manifest


def read_cacc2(
    *,
    directory: Path,
    expected_determinants: Cacc2Determinants,
) -> Mapping[str, Any]:
    manifest = _load_json_object(directory / "manifest.json")
    if set(manifest) != _ALLOWED_CACC2_MANIFEST_KEYS:
        raise RouteCCorruptAccelerator("CACC2 manifest schema/extra contents changed")
    if manifest.get("accelerator_id") != CACC2_ID or manifest.get("format") != CACC2_FORMAT:
        raise RouteCCorruptAccelerator("CACC2 identity/format mismatch")
    if manifest.get("route_c_candidate_hash") != ROUTE_C_CANDIDATE_HASH:
        raise RouteCCorruptAccelerator("CACC2 candidate identity mismatch")
    if manifest.get("determinant_hash") != expected_determinants.content_hash:
        raise RouteCDeterminantMismatch("CACC2 stale determinant key")
    if canonicalize(manifest.get("determinants")) != canonicalize(expected_determinants.as_dict()):
        raise RouteCDeterminantMismatch("CACC2 determinant material mismatch")
    if manifest.get("bit_index") != "ROW_ORDINAL_MINUS_1":
        raise RouteCCorruptAccelerator("CACC2 bit-index law changed")
    if manifest.get("bit_order_within_byte") != "LSB_FIRST":
        raise RouteCCorruptAccelerator("CACC2 bit order changed")
    if manifest.get("trailing_unused_bits") != "ZERO":
        raise RouteCCorruptAccelerator("CACC2 trailing-bit law changed")
    if manifest.get("entry_order") != "SEMANTIC_ATOM_CONTENT_HASH_ASCENDING":
        raise RouteCCorruptAccelerator("CACC2 atom order law changed")
    row_count = manifest.get("row_count")
    if not isinstance(row_count, int) or isinstance(row_count, bool) or row_count < 1:
        raise RouteCCorruptAccelerator("CACC2 row count invalid")
    risk = manifest.get("risk_entry")
    entries = manifest.get("atom_entries")
    if not isinstance(risk, Mapping) or not isinstance(entries, Sequence):
        raise RouteCCorruptAccelerator("CACC2 entries malformed")
    if len(entries) != 19:
        raise RouteCCorruptAccelerator("CACC2 must contain exactly 19 semantic atom masks")
    if {entry.get("role_id") for entry in entries} != set(CACC2_FROZEN_ROLE_ORDER):
        raise RouteCCorruptAccelerator("CACC2 frozen atom role coverage changed")
    hashes = [entry.get("semantic_atom_content_hash") for entry in entries]
    if hashes != sorted(hashes) or len(set(hashes)) != 19:
        raise RouteCCorruptAccelerator("CACC2 semantic atom order/hash uniqueness violated")
    files = {"manifest.json", str(risk.get("file"))}
    for entry in entries:
        files.add(str(entry.get("file")))
    actual = {p.name for p in directory.iterdir() if p.is_file()}
    if actual != files:
        raise RouteCCorruptAccelerator("CACC2 directory contains missing or unauthorized extra cache material")
    for entry in (risk, *entries):
        path = directory / str(entry.get("file"))
        data = path.read_bytes()
        _validate_mask_bytes(data, row_count)
        if _sha256_bytes(data) != entry.get("sha256"):
            raise RouteCCorruptAccelerator("CACC2 per-mask SHA mismatch")
        if mask_member_count(data, row_count) != entry.get("member_count"):
            raise RouteCCorruptAccelerator("CACC2 mask member count mismatch")
        if len(data) != manifest.get("mask_byte_length"):
            raise RouteCCorruptAccelerator("CACC2 mask length differs across entries")
        if entry is not risk:
            _ref_from_dict(entry.get("runtime_predicate_ref"))
    logical_material = {
        "format": CACC2_FORMAT,
        "row_count": row_count,
        "risk_entry": risk,
        "atom_entries": list(entries),
    }
    if semantic_hash(logical_material) != manifest.get("logical_content_hash"):
        raise RouteCCorruptAccelerator("CACC2 logical content hash mismatch")
    return manifest


def cacc2_mask_for_role(directory: Path, manifest: Mapping[str, Any], role_id: str) -> bytes:
    matches = [entry for entry in manifest.get("atom_entries", ()) if entry.get("role_id") == role_id]
    if len(matches) != 1:
        raise RouteCCorruptAccelerator("CACC2 role mask missing/duplicate")
    return (directory / matches[0]["file"]).read_bytes()


def delete_cacc2(directory: Path) -> None:
    if directory.exists():
        shutil.rmtree(directory)


def _identity_projection_fact(fact: Any) -> Mapping[str, Any]:
    return {
        "ref": fact.ref.as_dict(),
        "typed_state": fact.typed_state,
        "authority_snapshot_refs": [canonicalize(x) for x in fact.authority_snapshot_refs],
        "dependency_refs": [canonicalize(x) for x in fact.dependency_refs],
        "condition_predicate_ref": canonicalize(fact.condition_predicate_ref),
        "risk_set_ref": canonicalize(fact.risk_set_ref),
        "raw_numerator_support": fact.raw_numerator_support,
        "raw_denominator_support": fact.raw_denominator_support,
        "source_empirical_provenance_refs": [
            canonicalize(x) for x in fact.source_empirical_provenance_refs
        ],
        "replay_ref": canonicalize(fact.replay_ref),
    }


def query_identity_projection(result: Any) -> Mapping[str, Any]:
    return {
        "query_ref": canonicalize(result.query_ref),
        "source_scope_mode": result.source_scope_mode,
        "release_refs": [canonicalize(x) for x in result.release_refs],
        "facts": [_identity_projection_fact(f) for f in result.facts],
    }


def discovery_identity_projection(result: Any) -> Mapping[str, Any]:
    return {
        "contract_id": result.contract_id,
        "discovery_authority_ref": canonicalize(result.discovery_authority_ref),
        "candidate_grammar_ref": canonicalize(result.candidate_grammar_ref),
        "evaluated_frontier_ref": canonicalize(result.evaluated_frontier_ref),
        "candidate_count": result.candidate_count,
        "covered_candidate_count": result.covered_candidate_count,
        "empirical_fact_refs": [canonicalize(x) for x in result.empirical_fact_refs],
        "replay_ref": canonicalize(result.replay_ref),
        "receipts": [{
            "ref": receipt.ref.as_dict(),
            "typed_state": receipt.typed_state,
            "authority_snapshot_refs": [canonicalize(x) for x in receipt.authority_snapshot_refs],
            "dependency_refs": [canonicalize(x) for x in receipt.dependency_refs],
            "winning_predicate_ref": canonicalize(receipt.winning_predicate_ref),
            "empirical_fact_refs": [canonicalize(x) for x in receipt.empirical_fact_refs],
            "validation_fact_refs": [canonicalize(x) for x in receipt.validation_fact_refs],
            "evaluated_frontier_ref": canonicalize(receipt.evaluated_frontier_ref),
            "replay_ref": canonicalize(receipt.replay_ref),
        } for receipt in result.receipts],
    }


def assert_exact_query_identity_parity(left: Any, right: Any) -> None:
    if query_identity_projection(left) != query_identity_projection(right):
        raise RouteCAcceleratorError("Route-C query parity failed at exact identity/evidence grain")


def assert_exact_discovery_identity_parity(left: Any, right: Any) -> None:
    if discovery_identity_projection(left) != discovery_identity_projection(right):
        raise RouteCAcceleratorError("Route-C discovery parity failed at exact identity/receipt grain")


def build_route_c_repository(
    *,
    cacc1: Cacc1Bundle,
    projection: GovernedC11Projection,
):
    stream = cacc1_to_exact_physical_stream(cacc1, projection)
    return build_source_backed_c11_repository(stream, projection, cache=None)


def execute_route_c_empirical_query(
    *,
    cacc1: Cacc1Bundle,
    projection: GovernedC11Projection,
    query: Any,
    predicate: Any,
    authority_registry: Any,
    cacc2_directory: Path | None = None,
    cacc2_manifest: Mapping[str, Any] | None = None,
    required_atom_roles: Iterable[str] = (),
):
    # CACC2 is a coverage/preflight accelerator only here.  The unmodified exact
    # I03 engine remains the sole semantic oracle and returns the identity-bearing
    # EmpiricalFact objects.
    if cacc2_directory is not None or cacc2_manifest is not None:
        if cacc2_directory is None or cacc2_manifest is None:
            raise RouteCAcceleratorError("CACC2 directory/manifest must be supplied together")
        available = {entry["role_id"] for entry in cacc2_manifest.get("atom_entries", ())}
        required = set(required_atom_roles)
        if not required <= available:
            raise RouteCAcceleratorError("CACC2 lacks a required frozen atom role")
        for role in required:
            data = cacc2_mask_for_role(cacc2_directory, cacc2_manifest, role)
            _validate_mask_bytes(data, len(cacc1.rows))
    repository, release = build_route_c_repository(cacc1=cacc1, projection=projection)
    from rawlsing_next.pre553_empirical_query import execute_empirical_query
    return execute_empirical_query(
        repository=repository,
        query=query,
        predicate=predicate,
        authority_registry=authority_registry,
        release_refs=(release.release_ref,),
    )


def execute_route_c_exact_bounded_discovery(
    *,
    cacc1: Cacc1Bundle,
    projection: GovernedC11Projection,
    discovery_authority: Any,
    authority_registry: Any,
    predicate_catalog: Iterable[Any],
    query_template_catalog: Iterable[Any],
    cacc2_directory: Path,
    cacc2_manifest: Mapping[str, Any],
):
    # Require complete frozen atom-mask coverage before entering I05, but never
    # allow a mask or its cache identity to replace exact engine truth.
    available_refs = {
        _ref_from_dict(entry["runtime_predicate_ref"])
        for entry in cacc2_manifest.get("atom_entries", ())
    }
    predicates = tuple(predicate_catalog)
    if not {predicate.ref for predicate in predicates} <= available_refs:
        raise RouteCAcceleratorError("CACC2 runtime predicate coverage does not close")
    for entry in cacc2_manifest.get("atom_entries", ()):
        data = (cacc2_directory / entry["file"]).read_bytes()
        _validate_mask_bytes(data, len(cacc1.rows))
    repository, release = build_route_c_repository(cacc1=cacc1, projection=projection)
    from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
    return execute_exact_bounded_discovery(
        repository=repository,
        discovery_authority=discovery_authority,
        authority_registry=authority_registry,
        release_refs=(release.release_ref,),
        predicate_catalog=predicates,
        query_template_catalog=tuple(query_template_catalog),
    )


__all__ = [
    "ROUTE_C_CANDIDATE_HASH", "ROUTE_C_DELETE_REBUILD_LAW_HASH", "PINNED_PYARROW_VERSION",
    "FROZEN_LITS1_SOURCE_SHA256", "FROZEN_LITS1_C11_RELEASE_HASH",
    "FROZEN_PREDICATE_SEMANTIC_CATALOG_HASH", "FROZEN_RISK_TOPOLOGY_PARTITION_HASH",
    "SUCCESSOR_DISCOVERY_AUTHORITY_HASH", "SUCCESSOR_OFFICIAL_FRONTIER_HASH",
    "PRODUCTION_DISCOVERY_OPERATION", "CACC1_ID", "CACC1_FORMAT", "CACC2_ID", "CACC2_FORMAT",
    "CACC1_FIELD_ORDER", "CACC2_FROZEN_ROLE_ORDER",
    "RouteCAcceleratorError", "RouteCDeterminantMismatch", "RouteCCorruptAccelerator",
    "RouteCUnsupportedEnvironment", "RouteCDeterminants", "Cacc1Paths", "Cacc1Bundle",
    "Cacc2AtomBinding", "Cacc2Determinants", "materialize_cacc1_rows", "build_cacc1",
    "read_cacc1", "cacc1_to_exact_physical_stream", "delete_cacc1", "build_cacc2",
    "read_cacc2", "cacc2_mask_for_role", "delete_cacc2", "mask_member", "mask_member_count",
    "query_identity_projection", "discovery_identity_projection", "assert_exact_query_identity_parity",
    "assert_exact_discovery_identity_parity", "build_route_c_repository",
    "execute_route_c_empirical_query", "execute_route_c_exact_bounded_discovery",
]
