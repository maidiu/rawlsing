"""PRE-FF C0: mapping-independent, single-pass physical observation custody.

This OPTIONAL sourcefree physical journal is a companion to the existing
thirteen semantic C11 families. It is not a fourteenth semantic family,
not a new interpretive issuer, and not permission to persist original waves.

Every decoder-visible cell is stored at its PHYSICAL grain, including fields
with no known question/mapping/occurrence. Scientific interpretation may be
recomputed from this evidence later, without rereading the SAV/DTA, but a
mapping is never inferred from the value. The existing issued semantic
releases remain separately immutable.

The storage is a bounded streaming gzip JSONL using the existing exact
R5 typed-value codec. An independently held receipt must accompany reads.
"""
from __future__ import annotations

from dataclasses import dataclass
import gzip
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from typing import Iterator

from rawlsing_next.pre553_physical_decoder import (
    PhysicalCell, PhysicalMissingState, PhysicalSourceIncidence,
)
from rawlsing_next.pre553_r5_codec import (
    R5TypedValueCodec, canonical_json as r5_canonical_json,
)

SCHEMA = "PREFF_C0_SOURCEFREE_PHYSICAL_CELL_JOURNAL@1"
_CODEC = R5TypedValueCodec()


class PhysicalCellJournalError(ValueError):
    """Physical custody/integrity, not an analysis result."""


def _sha(value: str) -> str:
    if (type(value) is not str or len(value) != 64
            or any(x not in "0123456789abcdef" for x in value)):
        raise PhysicalCellJournalError("lowercase SHA-256 required")
    return value


def _root(path: str | Path) -> Path:
    root = Path(path).absolute()
    if root.is_symlink() or not root.is_dir():
        raise PhysicalCellJournalError("explicit existing private retention directory required")
    status = root.stat()
    mode = status.st_mode
    if status.st_uid != os.geteuid() or not stat.S_ISDIR(mode) or mode & 0o077:
        raise PhysicalCellJournalError("physical journal requires private 0700 retention root")
    return root


def _cell_payload(cell: PhysicalCell) -> dict:
    if type(cell) is not PhysicalCell or type(cell.missing_state) is not PhysicalMissingState:
        raise PhysicalCellJournalError("exact decoder physical-cell type required")
    return {
        "row": cell.row_ordinal,
        "ordinal": cell.variable_ordinal,
        "name": cell.variable_name,
        "raw_value": _CODEC.encode(cell.raw_value),
        "missing_state": cell.missing_state.value,
        "missing_declaration": _CODEC.encode(cell.source_missing_declaration),
        "source_value_label": _CODEC.encode(cell.raw_value_label),
    }


@dataclass(frozen=True)
class PhysicalCellJournalReceipt:
    schema: str
    source_sha256: str
    source_metadata_digest: str
    row_count: int
    variables: tuple[tuple[int, str], ...]
    cell_count: int
    physical_cells_sha256: str
    gzip_sha256: str
    gzip_bytes: int
    path: str

    def material(self) -> dict:
        return {
            "schema": self.schema, "source_sha256": self.source_sha256,
            "source_metadata_digest": self.source_metadata_digest,
            "row_count": self.row_count,
            "variables": [list(x) for x in self.variables],
            "cell_count": self.cell_count,
            "physical_cells_sha256": self.physical_cells_sha256,
            "gzip_sha256": self.gzip_sha256,
            "gzip_bytes": self.gzip_bytes,
            "path": self.path,
            "grade": "SOURCEFREE_PHYSICAL_CUSTODY_ONLY__NO_MAPPING_OR_ORIGINAL_SOURCE_PERMISSION",
        }


class PhysicalCellJournal:
    """Explicit private, streaming and fail-closed sourcefree physical sink.

    The caller holds the sourcefree retention decision. Merely constructing
    this object cannot issue original-source permission; the source-I02
    builder rejects this sink for ORIGINAL identity classes.
    """

    def __init__(self, authorized_private_root: str | Path):
        self.root = _root(authorized_private_root)
        self._stage: Path | None = None
        self._raw_stream = None
        self._gzip = None
        self._expected_sha: str | None = None
        self._metadata_digest: str | None = None
        self._rows = 0
        self._variables: tuple[tuple[int, str], ...] = ()
        self._seen = 0
        self._digest = sha256()
        self._published: Path | None = None
        self._receipt: PhysicalCellJournalReceipt | None = None
        self.state = "new"

    def begin(self, incidence: PhysicalSourceIncidence) -> None:
        if self.state != "new" or type(incidence) is not PhysicalSourceIncidence:
            raise PhysicalCellJournalError("NEW exact physical-source incidence required")
        self._expected_sha = _sha(incidence.source_sha256)
        self._metadata_digest = _sha(incidence.physical_metadata_digest)
        self._rows = incidence.row_count
        self._variables = tuple((v.ordinal, v.name) for v in incidence.variables)
        if (type(self._rows) is not int or self._rows < 1
                or not self._variables
                or any(x != (i, x[1]) or not x[1]
                       for i, x in enumerate(self._variables, 1))):
            raise PhysicalCellJournalError("invalid rectangular decoder source dimensions")
        self._stage = Path(tempfile.mkdtemp(prefix=".preff-physical-stage-", dir=self.root))
        self._stage.chmod(0o700)
        try:
            path = self._stage / "physical_cells.jsonl.gz"
            self._raw_stream = path.open("xb")
            os.chmod(path, 0o600)
            self._gzip = gzip.GzipFile(
                filename="", mode="wb", fileobj=self._raw_stream, mtime=0,
                compresslevel=6,
            )
            self.state = "writing"
        except BaseException:
            self.abort()
            raise

    def accept(self, cell: PhysicalCell) -> None:
        if self.state != "writing" or self._gzip is None:
            raise PhysicalCellJournalError("journal is not receiving source cells")
        expected_ordinal = self._seen % len(self._variables) + 1
        expected_row = self._seen // len(self._variables) + 1
        if (cell.row_ordinal != expected_row
                or cell.variable_ordinal != expected_ordinal
                or (cell.variable_ordinal, cell.variable_name)
                != self._variables[expected_ordinal - 1]
                or expected_row > self._rows):
            raise PhysicalCellJournalError(
                "physical rectangular source order/identity incomplete or duplicated"
            )
        payload = _cell_payload(cell)
        line = (r5_canonical_json(payload) + "\n").encode("ascii")
        self._gzip.write(line)
        self._digest.update(line)
        self._seen += 1

    def finish(self) -> PhysicalCellJournalReceipt:
        if self.state != "writing" or self._stage is None or self._gzip is None:
            raise PhysicalCellJournalError("journal not ready for commit")
        if self._seen != self._rows * len(self._variables):
            raise PhysicalCellJournalError(
                "physical source truncated or omitted cells; cannot seal"
            )
        self._gzip.close()
        self._gzip = None
        self._raw_stream.flush()
        os.fsync(self._raw_stream.fileno())
        self._raw_stream.close()
        self._raw_stream = None
        file = self._stage / "physical_cells.jsonl.gz"
        digest = sha256()
        with file.open("rb") as stream:
            for block in iter(lambda: stream.read(1 << 20), b""):
                digest.update(block)
        gzip_sha = digest.hexdigest()
        content_sha = self._digest.hexdigest()
        releases = self.root / "releases"
        if releases.is_symlink():
            raise PhysicalCellJournalError("physical releases directory may not be symlink")
        releases.mkdir(mode=0o700, exist_ok=True)
        if releases.stat().st_mode & 0o077:
            raise PhysicalCellJournalError("physical releases root not private")
        target = releases / ("physical-" + self._expected_sha + "-" + content_sha)
        if target.exists() or target.is_symlink():
            raise PhysicalCellJournalError(
                "physical journal content-addressed target occupied; no overwrite"
            )
        receipt = PhysicalCellJournalReceipt(
            SCHEMA, self._expected_sha, self._metadata_digest,
            self._rows, self._variables, self._seen, content_sha,
            gzip_sha, file.stat().st_size, str(target),
        )
        meta = (r5_canonical_json(receipt.material()) + "\n").encode("ascii")
        manifest = self._stage / "manifest.json"
        with manifest.open("xb") as f:
            os.chmod(manifest, 0o600)
            f.write(meta)
            f.flush()
            os.fsync(f.fileno())
        # Claim a fresh name without replacing an existing publication.
        # Each caller can use a distinct private root for the same source.
        self._stage.rename(target)
        self._stage = None
        self._published = target
        self._receipt = receipt
        self.state = "committed"
        fd = os.open(releases, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
        return receipt

    def abort(self) -> None:
        if self.state == "aborted":
            return
        if self._gzip is not None:
            self._gzip.close()
            self._gzip = None
        if self._raw_stream is not None:
            self._raw_stream.close()
            self._raw_stream = None
        if self._stage is not None:
            shutil.rmtree(self._stage)
            self._stage = None
        # Roll back only a publication this exact object exclusively created,
        # and only during the enclosing source-I02 transaction's failure.
        if self._published is not None:
            shutil.rmtree(self._published)
            self._published = None
        self._receipt = None
        self.state = "aborted"


def read_physical_cells(
    receipt: PhysicalCellJournalReceipt, *, authorized_private_root: str | Path,
) -> Iterator[PhysicalCell]:
    """Cold exact read of the independent physical source, NOT a C11 fact.

    Requires independently retained exact receipt. Neither this read nor its
    successful checksum issues a semantic mapping, source rights or weights.
    """
    if type(receipt) is not PhysicalCellJournalReceipt or receipt.schema != SCHEMA:
        raise PhysicalCellJournalError("independently held exact physical receipt required")
    root = _root(authorized_private_root)
    target = Path(receipt.path).absolute()
    if (target != root / "releases" / ("physical-" + _sha(receipt.source_sha256)
                                      + "-" + _sha(receipt.physical_cells_sha256))
            or target.is_symlink()
            or not target.is_dir()):
        raise PhysicalCellJournalError("physical journal path outside exact retention scope")
    file = target / "physical_cells.jsonl.gz"
    manifest = target / "manifest.json"
    if (file.is_symlink() or manifest.is_symlink()
            or not file.is_file() or not manifest.is_file()):
        raise PhysicalCellJournalError("physical journal body/manifest missing or linked")
    if json.loads(manifest.read_text("ascii")) != receipt.material():
        raise PhysicalCellJournalError("physical journal manifest differs from independent receipt")
    if file.stat().st_size != receipt.gzip_bytes:
        raise PhysicalCellJournalError("physical journal compressed length differs from receipt")
    compressed_digest = sha256()
    with file.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            compressed_digest.update(block)
    if compressed_digest.hexdigest() != _sha(receipt.gzip_sha256):
        raise PhysicalCellJournalError("physical journal compressed hash differs from receipt")
    # Complete uncompressed verification BEFORE offering the first value.
    # A checksum failure at EOF may not expose earlier corrupt values to
    # a consumer that could start making semantic facts while streaming.
    seen = 0
    stream_digest = sha256()
    with gzip.open(file, "rb") as handle:
        for line in handle:
            stream_digest.update(line)
            data = json.loads(line)
            ordinal = seen % len(receipt.variables) + 1
            row = seen // len(receipt.variables) + 1
            if (data["row"] != row or data["ordinal"] != ordinal
                    or (data["ordinal"], data["name"])
                    != receipt.variables[ordinal - 1]):
                raise PhysicalCellJournalError("physical cell order/slot changed")
            # Reject invalid typed payloads as well as invalid bytes.
            _CODEC.decode(data["raw_value"])
            PhysicalMissingState(data["missing_state"])
            _CODEC.decode(data["missing_declaration"])
            _CODEC.decode(data["source_value_label"])
            seen += 1
    if (seen != receipt.cell_count
            or seen != receipt.row_count * len(receipt.variables)
            or stream_digest.hexdigest() != _sha(receipt.physical_cells_sha256)):
        raise PhysicalCellJournalError("physical journal uncompressed bytes/count differ")
    # The original SAV/DTA is NOT reopened. This second bounded pass is
    # exclusively over independently authenticated retained physical bytes.
    # A future original-source reader must also pin host rights/currentness.
    with gzip.open(file, "rb") as handle:
        for line in handle:
            data = json.loads(line)
            yield PhysicalCell(
                data["row"], data["ordinal"], data["name"],
                _CODEC.decode(data["raw_value"]),
                PhysicalMissingState(data["missing_state"]),
                _CODEC.decode(data["missing_declaration"]),
                _CODEC.decode(data["source_value_label"]),
            )


__all__ = [
    "SCHEMA", "PhysicalCellJournal", "PhysicalCellJournalReceipt",
    "PhysicalCellJournalError", "read_physical_cells",
]
