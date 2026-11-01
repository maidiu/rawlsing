"""Thin, format-neutral source-byte decoders for the PRE553 substrate.

This module deliberately stops at physical incidence.  It never maps a raw
value to a C11 response state or interprets a label.

R35-I01 extends the physical boundary with a generic raw-layout metadata
contract.  Raw header declarations, reader-normalized geometry, display
metadata, and reader/config identity are preserved as independent witnesses.
Conflicting witnesses are never reconciled or promoted to survey semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
try:
    import fcntl
except ImportError:
    fcntl = None
import json
import math
import os
from pathlib import Path
import stat
import tempfile
from typing import Any, Iterator, Mapping

from rawlsing_next.pre553_r5_codec import normalize_decoder_physical_value


COMPATIBILITY_ONLY = "COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY"
SOURCE_DECLARED_ENCODING_ONLY = "SOURCE_DECLARED_EXACT_SHA_ENCODING__PHYSICAL_DECODING_ONLY"
PHYSICAL_METADATA_CONTRACT = "PRE553_PHYSICAL_METADATA@1.0.0"
SOURCE_CUSTODY_CONTRACT = "PRE553_CONTENT_BOUND_SOURCE_SNAPSHOT@1.0.0"
DECODER_IMPLEMENTATION_ID = "rawlsing_next/pre553_physical_decoder.py"
COMPATIBILITY_ALLOWLIST: Mapping[str, str] = {
    "6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8a": "latin1",
    "5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379": "latin1",
    "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09": "latin1",
    "c43d0e1821c51398817d7dfdfad2c0a4a5bb0d492f6a58096670e623bb6130e9": "latin1",
    "368ae5d07a44975a2f0a9ce3b1e564988a966b2632e28075c56a24d60065bcc8": "latin1",
    "14e1032755c4f42d8d3dc61647097ccd7605ba281551e53953c76d22a223cd1c": "latin1",
}

# CLOSED35 D01: exact source-declared encoding admission is a separate physical
# decoder lane from compatibility-only fallback. The map binds only exact source
# SHA -> declared decoder encoding; it authorizes no text semantics and no family-
# or wave-level inheritance.
DECLARED_ENCODING_ALLOWLIST: Mapping[str, str] = {
    "ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2": "BIG5",
    "5b703173845c086382fd93252f1cbc91dfef74007755459adfc73785389172f2": "WINDOWS-1252",
    "66252a92c59bf6759b79a6b35b2be658b98a433373212a70c8ec94755d3e02ec": "WINDOWS-1252",
}


class PhysicalMissingState(str, Enum):
    OBSERVED_STORAGE_VALUE = "OBSERVED_STORAGE_VALUE"
    SYSTEM_MISSING = "SYSTEM_MISSING"
    FORMAT_USER_MISSING_VALUE = "FORMAT_USER_MISSING_VALUE"
    FORMAT_USER_MISSING_RANGE = "FORMAT_USER_MISSING_RANGE"
    FORMAT_EXTENDED_MISSING = "FORMAT_EXTENDED_MISSING"
    SOURCE_CELL_ABSENT_OR_UNREPRESENTED = "SOURCE_CELL_ABSENT_OR_UNREPRESENTED"
    PHYSICAL_STATE_UNKNOWN = "PHYSICAL_STATE_UNKNOWN"


@dataclass(frozen=True)
class PhysicalVariable:
    ordinal: int
    name: str
    storage_type: str | None
    variable_label: str | None
    value_labels: Mapping[str, Any]
    missing_declarations: tuple[Mapping[str, Any], ...]
    display_metadata: Mapping[str, Any]
    topology_metadata: Mapping[str, Any]


@dataclass(frozen=True)
class PhysicalCell:
    row_ordinal: int
    variable_ordinal: int
    variable_name: str
    raw_value: Any
    missing_state: PhysicalMissingState
    source_missing_declaration: Mapping[str, Any] | None
    raw_value_label: Any = None


@dataclass(frozen=True)
class PhysicalSourceIncidence:
    source_sha256: str
    source_format: str
    row_count: int
    variables: tuple[PhysicalVariable, ...]
    reader_configuration: Mapping[str, Any]
    file_metadata: Mapping[str, Any]
    _frame: Any = None
    _variables_by_name: Mapping[str, PhysicalVariable] = None
    _source_path: str | None = None
    _reader_kind: str | None = None
    _encoding: str | None = None
    _source_snapshot: _SourceSnapshot | None = None

    @property
    def source_custody(self) -> Mapping[str, Any] | None:
        if self._source_snapshot is None:
            return None
        return {
            "contract": SOURCE_CUSTODY_CONTRACT,
            "source_sha256": self.source_sha256,
            "snapshot_sha256": self._source_snapshot.sha256,
            "snapshot_size": self._source_snapshot.size,
            "snapshot_path_unlinked": not self._source_snapshot.path.exists(),
            "reader_binding": "OPEN_FD_VIA_POSIX_DEV_FD",
            "reader_access_mode": self._source_snapshot.access_mode,
            "content_bound": True,
        }

    def verify_source_identity(self) -> str:
        if self._source_snapshot is not None:
            self._source_snapshot.verify()
        return self.source_sha256

    def close(self) -> None:
        if self._source_snapshot is not None:
            self._source_snapshot.close()

    def __enter__(self) -> PhysicalSourceIncidence:
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        self.close()

    @property
    def physical_metadata_digest(self) -> str:
        """Candidate-neutral digest of the required physical metadata receipt.

        This digest is deliberately metadata-only.  It does not replace raw-cell
        replay digests, derivative parentage, source certification, or semantic
        parity.  It makes loss of a required physical witness mechanically
        visible to later courts.
        """
        return compute_physical_metadata_digest(
            source_sha256=self.source_sha256,
            source_format=self.source_format,
            reader_configuration=self.reader_configuration,
            file_metadata=self.file_metadata,
            variables=self.variables,
        )

    def require_physical_metadata_digest(self, expected_digest: str) -> None:
        if not isinstance(expected_digest, str) or len(expected_digest) != 64:
            raise DecoderError("expected physical metadata digest must be a SHA-256 hex string")
        actual = self.physical_metadata_digest
        if actual != expected_digest.lower():
            raise DecoderError(
                f"physical metadata digest mismatch: expected {expected_digest.lower()} got {actual}"
            )

    def iter_batches(self, batch_size: int = 10_000) -> Iterator[tuple[PhysicalCell, ...]]:
        """Yield bounded cell batches with stable source row ordinals.

        The decoder retains only the reader frame when a compatibility reader
        requires a full read; it never retains a complete cell-object universe.
        """
        if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size < 1:
            raise ValueError("batch_size must be a positive integer")
        variables = self.variables
        declarations = {v.name: v.missing_declarations for v in variables}
        rows_per_chunk = max(1, batch_size // max(1, len(variables)))

        def emit(frame: Any, row_offset: int) -> Iterator[tuple[PhysicalCell, ...]]:
            batch: list[PhysicalCell] = []
            for local_row, row in enumerate(frame.itertuples(index=False, name=None), 1):
                for variable, value in zip(variables, row):
                    raw = _physical_value(value)
                    state, declaration = classify_physical_value(raw, declarations[variable.name])
                    batch.append(PhysicalCell(row_offset + local_row, variable.ordinal, variable.name, raw, state,
                                              declaration, variable.value_labels.get(str(raw))))
                    if len(batch) >= batch_size:
                        yield tuple(batch)
                        batch.clear()
            if batch:
                yield tuple(batch)

        if self._frame is not None:
            yield from emit(self._frame, 0)
            return
        if self._reader_kind is None or self._source_snapshot is None:
            raise DecoderError("physical source has no content-bound snapshot for lazy byte reads")
        self.verify_source_identity()
        import pyreadstat
        snapshot = self._source_snapshot
        reader = pyreadstat.read_sav if self._reader_kind == "SAV" else pyreadstat.read_dta
        snapshot.rewind()
        if self._reader_kind == "SAV":
            row_offset = 0
            chunks = pyreadstat.read_file_in_chunks(
                reader, snapshot.reader_path, chunksize=rows_per_chunk, encoding=self._encoding,
                apply_value_formats=False, user_missing=True,
            )
            for frame, _metadata in chunks:
                snapshot.check_stable()
                yield from emit(frame, row_offset)
                row_offset += len(frame)
            return
        frame, _metadata = reader(
            snapshot.reader_path, apply_value_formats=False, user_missing=True, encoding=self._encoding
        )
        snapshot.verify()
        yield from emit(frame, 0)

    def iter_cells(self, batch_size: int = 10_000) -> Iterator[PhysicalCell]:
        for batch in self.iter_batches(batch_size):
            yield from batch


class DecoderError(ValueError):
    pass


@dataclass
class _SourceSnapshot:
    sha256: str
    path: Path
    directory: Path
    fd: int
    size: int
    stat_signature: tuple[int, int, int, int, int]
    _closed: bool = False

    def _ensure_read_only(self) -> None:
        if self._closed:
            raise DecoderError("source snapshot is closed")
        if fcntl is None:
            raise DecoderError("read-only descriptor capability requires POSIX fcntl")
        flags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        if flags & os.O_ACCMODE != os.O_RDONLY:
            raise DecoderError("source snapshot reader is not read-only")
        if not stat.S_ISREG(os.fstat(self.fd).st_mode):
            raise DecoderError("source snapshot reader is not a regular file")

    @property
    def access_mode(self) -> str:
        if self._closed:
            return "CLOSED"
        if fcntl is None:
            return "UNKNOWN"
        flags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        return {
            os.O_RDONLY: "O_RDONLY",
            os.O_WRONLY: "O_WRONLY",
            os.O_RDWR: "O_RDWR",
        }.get(flags & os.O_ACCMODE, "UNKNOWN")

    @property
    def reader_path(self) -> str:
        self._ensure_read_only()
        return f"/dev/fd/{self.fd}"

    def read_prefix(self, size: int) -> bytes:
        self._ensure_read_only()
        return os.pread(self.fd, size, 0)

    def rewind(self) -> None:
        self._ensure_read_only()
        os.lseek(self.fd, 0, os.SEEK_SET)

    def _current_signature(self) -> tuple[int, int, int, int, int]:
        st = os.fstat(self.fd)
        return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)

    def check_stable(self) -> None:
        self._ensure_read_only()
        if self._current_signature() != self.stat_signature:
            raise DecoderError("source snapshot changed after identity acquisition")

    def verify(self) -> None:
        self._ensure_read_only()
        self.check_stable()
        if _sha_fd(self.fd) != self.sha256:
            raise DecoderError("source snapshot bytes changed after identity acquisition")

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            st = os.stat(self.path)
            fst = os.fstat(self.fd)
            if (st.st_dev, st.st_ino) == (fst.st_dev, fst.st_ino):
                os.unlink(self.path)
        except OSError:
            pass
        try:
            os.close(self.fd)
        finally:
            try:
                os.rmdir(self.directory)
            except OSError:
                pass

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass


def _sha_fd(fd: int) -> str:
    digest = hashlib.sha256()
    offset = 0
    while True:
        block = os.pread(fd, 1024 * 1024, offset)
        if not block:
            return digest.hexdigest()
        digest.update(block)
        offset += len(block)


def _acquire_source_snapshot(source: Path, expected_source_sha256: str | None = None) -> _SourceSnapshot:
    try:
        source_fd = os.open(source, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0))
    except OSError as exc:
        raise DecoderError(f"source bytes unavailable: {source}") from exc
    directory: Path | None = None
    construction_fd: int | None = None
    reader_fd: int | None = None
    snapshot_identity: tuple[int, int] | None = None
    try:
        if not stat.S_ISREG(os.fstat(source_fd).st_mode):
            raise DecoderError(f"source bytes unavailable: {source}")
        if os.name != "posix" or not Path("/dev/fd").is_dir():
            raise DecoderError("content-bound reader path requires POSIX /dev/fd")
        directory = Path(tempfile.mkdtemp(prefix="rawlsing-source-custody-"))
        snapshot_path = directory / "source.bin"
        construction_fd = os.open(snapshot_path, os.O_RDWR | os.O_CREAT | os.O_EXCL, 0o600)
        construction_stat = os.fstat(construction_fd)
        snapshot_identity = (construction_stat.st_dev, construction_stat.st_ino)
        digest = hashlib.sha256()
        size = 0
        while True:
            block = os.read(source_fd, 1024 * 1024)
            if not block:
                break
            digest.update(block)
            size += len(block)
            view = memoryview(block)
            while view:
                view = view[os.write(construction_fd, view):]
        os.fchmod(construction_fd, 0o400)
        actual = digest.hexdigest()
        if expected_source_sha256 is not None and actual != expected_source_sha256:
            raise DecoderError("source sha256 mismatch before governed decode")
        reader_flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
        reader_fd = os.open(snapshot_path, reader_flags)
        reader_stat = os.fstat(reader_fd)
        construction_stat = os.fstat(construction_fd)
        if (
            (reader_stat.st_dev, reader_stat.st_ino) != (construction_stat.st_dev, construction_stat.st_ino)
            or reader_stat.st_size != size
            or construction_stat.st_size != size
        ):
            raise DecoderError("source snapshot reader does not match the construction inode")
        if fcntl is None:
            raise DecoderError("read-only descriptor capability requires POSIX fcntl")
        if fcntl.fcntl(reader_fd, fcntl.F_GETFL) & os.O_ACCMODE != os.O_RDONLY:
            raise DecoderError("source snapshot reader is not read-only")
        os.close(construction_fd)
        construction_fd = None
        path_stat = os.stat(snapshot_path)
        if (path_stat.st_dev, path_stat.st_ino) != (reader_stat.st_dev, reader_stat.st_ino):
            raise DecoderError("source snapshot pathname was replaced before unlink")
        os.unlink(snapshot_path)
        if os.fstat(reader_fd).st_nlink != 0:
            raise DecoderError("source snapshot inode retains an acquisition link")
        if _sha_fd(reader_fd) != actual:
            raise DecoderError("source snapshot bytes changed before read-only handoff")
        st = os.fstat(reader_fd)
        signature = (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
        return _SourceSnapshot(actual, snapshot_path, directory, reader_fd, size, signature)
    except Exception:
        if reader_fd is not None:
            try:
                os.close(reader_fd)
            except OSError:
                pass
        if construction_fd is not None:
            try:
                os.close(construction_fd)
            except OSError:
                pass
        if directory is not None:
            path = directory / "source.bin"
            if snapshot_identity is not None:
                try:
                    st = os.stat(path)
                    if (st.st_dev, st.st_ino) == snapshot_identity:
                        os.unlink(path)
                except OSError:
                    pass
            try:
                os.rmdir(directory)
            except OSError:
                pass
        raise
    finally:
        os.close(source_fd)


def _jsonable(value: Any) -> Any:
    if None is value or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if math.isnan(value):
            return None
        if math.isinf(value):
            return str(value)
        return value
    if hasattr(value, "item"):
        try:
            return _jsonable(value.item())
        except Exception:
            pass
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    return str(value)


def _physical_value(value: Any) -> Any:
    """Preserve exact decoder-native naive date/time through the opaque R5 seam only."""
    import datetime as _dt
    if type(value) in {_dt.datetime, _dt.date, _dt.time}:
        return normalize_decoder_physical_value(value)
    if hasattr(value, "item"):
        try:
            item = value.item()
        except Exception:
            pass
        else:
            if type(item) in {_dt.datetime, _dt.date, _dt.time}:
                return normalize_decoder_physical_value(item)
    return _jsonable(value)


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        _jsonable(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_file_metadata_contract(file_metadata: Mapping[str, Any]) -> None:
    if not isinstance(file_metadata, Mapping):
        raise DecoderError("file_metadata must be a mapping")
    if file_metadata.get("contract_schema") != PHYSICAL_METADATA_CONTRACT:
        raise DecoderError("file_metadata physical metadata contract schema missing or wrong")
    for key in ("raw_layout_declarations", "normalized_geometry", "display_metadata", "decoder_identity"):
        if key not in file_metadata:
            raise DecoderError(f"file_metadata missing required physical witness: {key}")


def build_physical_metadata_payload(
    *,
    source_sha256: str,
    source_format: str,
    reader_configuration: Mapping[str, Any],
    file_metadata: Mapping[str, Any],
    variables: tuple[PhysicalVariable, ...] | list[PhysicalVariable],
) -> Mapping[str, Any]:
    """Build the canonical metadata-only replay payload.

    Raw header/layout declarations and normalized geometry are intentionally
    separate.  The payload records both even when they disagree.  No field in
    this payload authorizes semantic interpretation of labels, routing, weights,
    missingness, or respondent identity.
    """
    _validate_file_metadata_contract(file_metadata)
    return {
        "schema": PHYSICAL_METADATA_CONTRACT,
        "source_sha256": source_sha256,
        "source_format": source_format,
        "reader_configuration": _jsonable(reader_configuration),
        "file_metadata": _jsonable(file_metadata),
        "variables": [
            {
                "ordinal": variable.ordinal,
                "name": variable.name,
                "storage_type": variable.storage_type,
                "variable_label": variable.variable_label,
                "value_labels": _jsonable(variable.value_labels),
                "missing_declarations": _jsonable(variable.missing_declarations),
                "display_metadata": _jsonable(variable.display_metadata),
                "topology_metadata": _jsonable(variable.topology_metadata),
            }
            for variable in variables
        ],
    }


def compute_physical_metadata_digest(
    *,
    source_sha256: str,
    source_format: str,
    reader_configuration: Mapping[str, Any],
    file_metadata: Mapping[str, Any],
    variables: tuple[PhysicalVariable, ...] | list[PhysicalVariable],
) -> str:
    return _canonical_json_sha256(build_physical_metadata_payload(
        source_sha256=source_sha256,
        source_format=source_format,
        reader_configuration=reader_configuration,
        file_metadata=file_metadata,
        variables=variables,
    ))


def _compatibility_config(source_sha: str, encoding: str | None) -> dict[str, Any]:
    if encoding in ("auto", "guess", "fallback"):
        raise DecoderError("automatic encoding guessing/fallback is forbidden")
    if encoding is None:
        return {"encoding": None, "authority_status": None}
    expected = COMPATIBILITY_ALLOWLIST.get(source_sha)
    if expected == encoding:
        return {"encoding": encoding, "authority_status": COMPATIBILITY_ONLY}
    declared = DECLARED_ENCODING_ALLOWLIST.get(source_sha)
    if declared == encoding:
        return {"encoding": encoding, "authority_status": SOURCE_DECLARED_ENCODING_ONLY}
    raise DecoderError("encoding override is not in an exact SHA/config representation allowlist")


def _missing_declarations(metadata: Any, name: str, source_format: str) -> tuple[Mapping[str, Any], ...]:
    ranges = getattr(metadata, "missing_ranges", {}) or {}
    user = getattr(metadata, "missing_user_values", {}) or {}
    result: list[Mapping[str, Any]] = []
    for item in ranges.get(name, ()):
        if isinstance(item, Mapping) and item.get("lo") == item.get("hi"):
            result.append({"kind": "discrete", "value": _jsonable(item.get("lo"))})
        else:
            result.append({"kind": "range", "lo": _jsonable(item.get("lo")), "hi": _jsonable(item.get("hi"))})
    for value in user.get(name, ()):
        token = _jsonable(value)
        if source_format == "DTA" and isinstance(token, str) and len(token) == 1 and token.lower() in "abcdefghijklmnopqrstuvwxyz":
            result.append({"kind": "extended", "reader_token": token, "stata_token": "." + token.lower()})
        elif source_format == "DTA" and isinstance(token, str) and len(token) == 2 and token[0] == "." and token[1].lower() in "abcdefghijklmnopqrstuvwxyz":
            result.append({"kind": "extended", "reader_token": token[1].lower(), "stata_token": token.lower()})
        else:
            result.append({"kind": "discrete", "value": token})
    return tuple(result)


def classify_physical_value(value: Any, declarations: tuple[Mapping[str, Any], ...]) -> tuple[PhysicalMissingState, Mapping[str, Any] | None]:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return PhysicalMissingState.SYSTEM_MISSING, None
    for declaration in declarations:
        if declaration["kind"] == "extended" and value in (declaration.get("reader_token"), declaration.get("stata_token"), declaration.get("token")):
            return PhysicalMissingState.FORMAT_EXTENDED_MISSING, declaration
        if declaration["kind"] == "discrete" and value == declaration.get("value"):
            return PhysicalMissingState.FORMAT_USER_MISSING_VALUE, declaration
        if declaration["kind"] == "range" and declaration.get("lo") <= value <= declaration.get("hi"):
            return PhysicalMissingState.FORMAT_USER_MISSING_RANGE, declaration
    return PhysicalMissingState.OBSERVED_STORAGE_VALUE, None


def _reader_declared_layout(metadata: Any) -> Mapping[str, Any]:
    return {
        "number_columns": _jsonable(getattr(metadata, "number_columns", None)),
        "number_rows": _jsonable(getattr(metadata, "number_rows", None)),
        "file_format": _jsonable(getattr(metadata, "file_format", None)),
        "file_encoding": _jsonable(getattr(metadata, "file_encoding", None)),
    }


def _sav_header_layout(prefix: bytes) -> Mapping[str, Any]:
    """Parse only fixed physical SAV header declarations.

    SPSS system files place layout_code at byte 64 and nominal_case_size at
    byte 68.  Endianness is selected only when the layout code is the standard
    2/3 witness.  Unknown/truncated headers remain preserved by prefix digest
    and parse status rather than guessed.
    """
    out: dict[str, Any] = {
        "header_prefix_length": len(prefix),
        "header_prefix_sha256": hashlib.sha256(prefix).hexdigest(),
    }
    if len(prefix) < 84:
        out["parse_status"] = "TRUNCATED_FIXED_HEADER"
        return out
    record_type = prefix[0:4]
    out["record_type_hex"] = record_type.hex()
    if record_type not in (b"$FL2", b"$FL3"):
        out["parse_status"] = "UNRECOGNIZED_FIXED_HEADER_SIGNATURE"
        return out

    raw_layout = prefix[64:68]
    little = int.from_bytes(raw_layout, "little", signed=True)
    big = int.from_bytes(raw_layout, "big", signed=True)
    if little in (2, 3):
        byteorder = "little"
        layout_code = little
    elif big in (2, 3):
        byteorder = "big"
        layout_code = big
    else:
        out.update({
            "parse_status": "UNRECOGNIZED_LAYOUT_CODE",
            "layout_code_raw_hex": raw_layout.hex(),
            "layout_code_little": little,
            "layout_code_big": big,
        })
        return out

    def i32(start: int) -> int:
        return int.from_bytes(prefix[start:start + 4], byteorder, signed=True)

    out.update({
        "parse_status": "PARSED_FIXED_HEADER",
        "integer_endianness": byteorder,
        "record_type": record_type.decode("ascii"),
        "layout_code": layout_code,
        "nominal_case_size": i32(68),
        "compression": i32(72),
        "weight_index": i32(76),
        "declared_case_count": i32(80),
    })
    return out


def _raw_layout_declarations(
    source: Path, source_format: str, metadata: Any, *, prefix: bytes | None = None
) -> Mapping[str, Any]:
    """Preserve raw-format layout evidence without interpreting survey meaning."""
    prefix_size = 176 if source_format == "SAV" else 512
    if prefix is None:
        with source.open("rb") as handle:
            prefix = handle.read(prefix_size)

    if source_format == "SAV":
        native = _sav_header_layout(prefix)
    else:
        native = {
            "parse_status": "RAW_HEADER_BYTES_PRESERVED__NO_FORMAT_SEMANTIC_INFERENCE",
            "header_prefix_length": len(prefix),
            "header_prefix_sha256": hashlib.sha256(prefix).hexdigest(),
        }

    return {
        "reader_declared": _reader_declared_layout(metadata),
        "format_native_header": native,
    }


def _file_metadata_contract(
    *,
    source: Path,
    source_format: str,
    metadata: Any,
    variables: tuple[PhysicalVariable, ...],
    row_count: int,
    prefix: bytes | None = None,
) -> Mapping[str, Any]:
    names = [variable.name for variable in variables]
    display = [
        {
            "ordinal": variable.ordinal,
            "name": variable.name,
            "storage_type": variable.storage_type,
            "display_metadata": _jsonable(variable.display_metadata),
        }
        for variable in variables
    ]
    raw_layout = _raw_layout_declarations(source, source_format, metadata, prefix=prefix)
    normalized_geometry = {
        "traversed_dictionary_variable_count": len(variables),
        "traversed_stream_cell_width": len(variables),
        "traversed_row_count": row_count,
        "ordered_variable_inventory": [
            {"ordinal": variable.ordinal, "name": variable.name}
            for variable in variables
        ],
    }
    return {
        "contract_schema": PHYSICAL_METADATA_CONTRACT,
        "file_encoding": _jsonable(getattr(metadata, "file_encoding", None)),
        "file_format": _jsonable(getattr(metadata, "file_format", source_format.lower())),
        # Legacy normalized geometry fields retained for existing consumers.
        "number_columns": len(names),
        "number_rows": row_count,
        # R35-I01 witnesses: do not reconcile these if they disagree.
        "raw_layout_declarations": raw_layout,
        "normalized_geometry": normalized_geometry,
        "display_metadata": display,
        "decoder_identity": {
            "implementation": DECODER_IMPLEMENTATION_ID,
            "contract_version": PHYSICAL_METADATA_CONTRACT,
        },
    }


def _decode(
    path: str | Path,
    *,
    expected_format: str,
    encoding: str | None = None,
    expected_source_sha256: str | None = None,
) -> PhysicalSourceIncidence:
    import pyreadstat

    source = Path(path)
    if not source.is_file():
        raise DecoderError(f"source bytes unavailable: {source}")
    if expected_source_sha256 is not None:
        if (
            not isinstance(expected_source_sha256, str)
            or len(expected_source_sha256) != 64
            or expected_source_sha256.lower() != expected_source_sha256
            or any(char not in "0123456789abcdef" for char in expected_source_sha256)
        ):
            raise DecoderError("expected_source_sha256 must be lowercase sha256")
        if _sha(source) != expected_source_sha256:
            raise DecoderError("source sha256 mismatch before governed decode")
    snapshot = _acquire_source_snapshot(source, expected_source_sha256)
    try:
        snapshot.verify()
        source_sha = snapshot.sha256
        compatibility = _compatibility_config(source_sha, encoding)
        reader = pyreadstat.read_sav if expected_format == "sav" else pyreadstat.read_dta
        reader_source = snapshot.reader_path
        snapshot.rewind()
        _metadata_frame, metadata = reader(reader_source, metadataonly=True, apply_value_formats=False,
                                           user_missing=True, encoding=encoding)
        snapshot.verify()
        source_format = expected_format.upper()
        compatibility_full_read = encoding is not None
        frame = None
        if compatibility_full_read:
            snapshot.rewind()
            frame, metadata = reader(reader_source, apply_value_formats=False, user_missing=True, encoding=encoding)
            snapshot.verify()
        names = list(metadata.column_names)
        variables: list[PhysicalVariable] = []
        declarations: dict[str, tuple[Mapping[str, Any], ...]] = {}
        for ordinal, name in enumerate(names, 1):
            decl = _missing_declarations(metadata, name, source_format)
            declarations[name] = decl
            labels = (getattr(metadata, "variable_value_labels", {}) or {}).get(name, {}) or {}
            display = {
                "storage_width": (getattr(metadata, "variable_storage_width", {}) or {}).get(name),
                "display_width": (getattr(metadata, "variable_display_width", {}) or {}).get(name),
                "alignment": (getattr(metadata, "variable_alignment", {}) or {}).get(name),
                "measure": (getattr(metadata, "variable_measure", {}) or {}).get(name),
                "format": (getattr(metadata, "original_variable_types", {}) or {}).get(name),
            }
            variables.append(PhysicalVariable(
                ordinal, name, (getattr(metadata, "readstat_variable_types", {}) or {}).get(name),
                (getattr(metadata, "column_names_to_labels", {}) or {}).get(name),
                {str(_jsonable(k)): _jsonable(v) for k, v in labels.items()}, decl, display,
                {"multiple_response_sets": _jsonable((getattr(metadata, "mr_sets", {}) or {}))},
            ))
        row_count = int(getattr(metadata, "number_rows", 0) or 0)
        variable_tuple = tuple(variables)
        file_meta = _file_metadata_contract(
            source=source,
            source_format=source_format,
            metadata=metadata,
            variables=variable_tuple,
            row_count=row_count,
            prefix=snapshot.read_prefix(176 if source_format == "SAV" else 512),
        )
        snapshot.verify()
        reader_config = {
            "reader": "pyreadstat",
            "reader_version": getattr(pyreadstat, "__version__", None),
            "decoder_implementation": DECODER_IMPLEMENTATION_ID,
            "physical_metadata_contract": PHYSICAL_METADATA_CONTRACT,
            "user_missing": True,
            "apply_value_formats": False,
            **compatibility,
        }
        return PhysicalSourceIncidence(
            source_sha,
            source_format,
            row_count,
            variable_tuple,
            reader_config,
            file_meta,
            _frame=frame,
            _source_path=str(source),
            _reader_kind=source_format,
            _encoding=encoding,
            _source_snapshot=snapshot,
        )
    except Exception:
        snapshot.close()
        raise


def decode_sav(
    path: str | Path,
    *,
    encoding: str | None = None,
    expected_source_sha256: str | None = None,
) -> PhysicalSourceIncidence:
    return _decode(
        path,
        expected_format="sav",
        encoding=encoding,
        expected_source_sha256=expected_source_sha256,
    )


def decode_dta(
    path: str | Path,
    *,
    encoding: str | None = None,
    expected_source_sha256: str | None = None,
) -> PhysicalSourceIncidence:
    return _decode(
        path,
        expected_format="dta",
        encoding=encoding,
        expected_source_sha256=expected_source_sha256,
    )


__all__ = [
    "COMPATIBILITY_ALLOWLIST",
    "COMPATIBILITY_ONLY",
    "DECLARED_ENCODING_ALLOWLIST",
    "SOURCE_DECLARED_ENCODING_ONLY",
    "DECODER_IMPLEMENTATION_ID",
    "PHYSICAL_METADATA_CONTRACT",
    "SOURCE_CUSTODY_CONTRACT",
    "DecoderError",
    "PhysicalMissingState",
    "PhysicalVariable",
    "PhysicalCell",
    "PhysicalSourceIncidence",
    "build_physical_metadata_payload",
    "compute_physical_metadata_digest",
    "classify_physical_value",
    "_physical_value",
    "decode_sav",
    "decode_dta",
]
