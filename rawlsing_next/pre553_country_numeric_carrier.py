"""Country-at-a-time compact physical survey carrier (S03 candidate).

Uses the incumbent PhysicalSourceIncidence and R5 codec. No source permission,
semantic mapping, population estimate or new analytical evaluator is issued.
Original source row ordinals survive. Ordinary cells are small dictionary codes,
not serialized C11 objects. A country-scoped governed projection is still
required for native C11/I03; a country shard must never impersonate a full wave.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from pathlib import Path
from typing import Callable, Iterator
import json
import os
import sqlite3
import struct
import tempfile
import zlib

from .pre553_physical_decoder import PhysicalCell, PhysicalMissingState, PhysicalSourceIncidence
from .pre553_r5_codec import R5TypedValueCodec, canonical_json

SCHEMA = "PYAT_COUNTRY_NUMERIC_PHYSICAL@1"
_CODEC = R5TypedValueCodec()
MAX_ROWS = 4096
MAX_BYTES = 64 * 1024 * 1024

class CountryCarrierError(ValueError):
    pass

def _hash(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _live(check: Callable[[], None]) -> None:
    if not callable(check):
        raise CountryCarrierError("explicit currentness owner callback required")
    # A caller must implement the existing source authorization check.
    # False is a denial, not a successful callback.
    if check() is False:
        raise CountryCarrierError("source/retention currentness refused")

def _pack(values, width):
    tag = {1:"B", 2:"H", 4:"I", 8:"Q"}[width]
    return zlib.compress(struct.pack("<" + tag * len(values), *values))

def _unpack(payload, width, n):
    if not 0 <= n <= MAX_ROWS or width not in (1, 2, 4, 8):
        raise CountryCarrierError("invalid packed lane dimensions")
    d = zlib.decompressobj()
    data = d.decompress(payload, n * width + 1)
    if len(data) != n * width or not d.eof or d.unused_data or d.unconsumed_tail:
        raise CountryCarrierError("invalid packed lane")
    tag = {1:"B", 2:"H", 4:"I", 8:"Q"}[width]
    return struct.unpack("<" + tag * n, data)

def _encode_cell(cell: PhysicalCell) -> str:
    return canonical_json(_CODEC.encode((cell.raw_value, cell.missing_state.value,
                                        cell.source_missing_declaration, cell.raw_value_label)))

def _decode_cell(row, ordinal, name, token):
    raw, state, declaration, label = _CODEC.decode(json.loads(token))
    return PhysicalCell(row, ordinal, name, raw, PhysicalMissingState(state), declaration, label)

@dataclass(frozen=True)
class CountryReceipt:
    source_sha256: str
    metadata_digest: str
    source_rows: int
    country_variable: str
    country_key: str
    country_rows: int
    sha256: str
    bytes: int

@dataclass(frozen=True)
class NumericColumn:
    """Codes and exact R5 value/state dictionary, in original respondent order."""
    row_ordinals: tuple[int, ...]
    codes: tuple[int, ...]
    dictionary: tuple[str, ...]

    def cells(self, ordinal, name):
        for row, code in zip(self.row_ordinals, self.codes):
            yield _decode_cell(row, ordinal, name, self.dictionary[code])

    def observed_codes_for(self, value):
        target = _CODEC.typed_key(value)
        result = set()
        for i, token in enumerate(self.dictionary):
            raw, state, _, _ = _CODEC.decode(json.loads(token))
            if state == PhysicalMissingState.OBSERVED_STORAGE_VALUE.value and _CODEC.typed_key(raw) == target:
                result.add(i)
        return frozenset(result)

def build_country(incidence: PhysicalSourceIncidence, *, country_variable: str,
                  country_value, output: str | Path, require_current: Callable[[], None],
                  block_rows: int = 1024) -> CountryReceipt:
    """Scan the content-bound source; retain only ONE explicit country.

    Each block stores row ordinals once and one compressed integer code lane
    per native variable. Country values and labels are not inferred. Repeated
    source scans are possible; no full-wave C11 staging or per-cell JSON archive.
    """
    if type(incidence) is not PhysicalSourceIncidence:
        raise CountryCarrierError("incumbent physical decoder incidence required")
    if type(block_rows) is not int or not 1 <= block_rows <= MAX_ROWS:
        raise CountryCarrierError("invalid country block size")
    variables = tuple((v.ordinal, v.name) for v in incidence.variables)
    if not variables or len(set(variables)) != len(variables) or len({v[1] for v in variables}) != len(variables):
        raise CountryCarrierError("invalid source variable inventory")
    if country_variable not in {name for _, name in variables}:
        raise CountryCarrierError("explicit source-native country variable required")
    key = canonical_json(_CODEC.encode(country_value))
    _live(require_current)
    source = incidence.verify_source_identity()
    metadata = incidence.physical_metadata_digest
    dest = Path(output).resolve()
    if not dest.parent.is_dir() or dest.exists():
        raise CountryCarrierError("existing private output directory and new output required")
    fd, tmp = tempfile.mkstemp(prefix=".country-", suffix=".sqlite", dir=dest.parent)
    os.close(fd)
    stage = Path(tmp)
    db = None
    try:
        db = sqlite3.connect(stage)
        db.executescript("""
          PRAGMA journal_mode=DELETE;
          PRAGMA synchronous=FULL;
          CREATE TABLE meta(k TEXT PRIMARY KEY,v TEXT NOT NULL);
          CREATE TABLE vars(ordinal INTEGER PRIMARY KEY,name TEXT NOT NULL UNIQUE);
          CREATE TABLE blocks(id INTEGER PRIMARY KEY,n INTEGER NOT NULL,rows BLOB NOT NULL);
          CREATE TABLE lanes(block INTEGER NOT NULL REFERENCES blocks(id),ordinal INTEGER NOT NULL REFERENCES vars(ordinal),
             width INTEGER NOT NULL,dict BLOB NOT NULL,codes BLOB NOT NULL,PRIMARY KEY(block,ordinal)) WITHOUT ROWID;
        """)
        db.execute("PRAGMA foreign_keys=ON")
        db.executemany("INSERT INTO vars VALUES(?,?)", variables)
        pending = []
        country_rows = 0
        block = 0
        def flush():
            nonlocal block
            if not pending:
                return
            _live(require_current)
            n = len(pending)
            db.execute("INSERT INTO blocks VALUES(?,?,?)",
                       (block,n,_pack([row[0] for row in pending],8)))
            for i,(ordinal,_) in enumerate(variables):
                dictionary, index, codes = [], {}, []
                for _,tokens in pending:
                    token = tokens[i]
                    if token not in index:
                        index[token] = len(dictionary)
                        dictionary.append(token)
                    codes.append(index[token])
                width = 1 if len(dictionary) <= 256 else 2 if len(dictionary) <= 65536 else 4
                raw = canonical_json(dictionary).encode("ascii")
                if len(raw) > MAX_BYTES:
                    raise CountryCarrierError("dictionary block too large")
                db.execute("INSERT INTO lanes VALUES(?,?,?,?,?)",
                           (block,ordinal,width,zlib.compress(raw),_pack(codes,width)))
            pending.clear()
            block += 1
            db.commit()
        row_id = 1
        cells = []
        def accept_row():
            nonlocal country_rows
            if tuple((c.variable_ordinal,c.variable_name) for c in cells) != variables:
                raise CountryCarrierError("missing, duplicated or reordered physical cell")
            country = next(c for c in cells if c.variable_name == country_variable)
            if (country.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE
                    and canonical_json(_CODEC.encode(country.raw_value)) == key):
                pending.append((row_id,tuple(_encode_cell(c) for c in cells)))
                country_rows += 1
                if len(pending) == block_rows:
                    flush()
        for cell in incidence.iter_cells():
            if type(cell) is not PhysicalCell:
                raise CountryCarrierError("foreign physical cell")
            if cell.row_ordinal != row_id:
                if cell.row_ordinal != row_id + 1 or not cells:
                    raise CountryCarrierError("source row discontinuity")
                accept_row()
                cells.clear()
                row_id += 1
            cells.append(cell)
            if len(cells) > len(variables):
                raise CountryCarrierError("duplicate source row slot")
        if cells:
            accept_row()
        if (row_id if cells else 0) != incidence.row_count:
            raise CountryCarrierError("incomplete original source scan")
        flush()
        if not country_rows:
            raise CountryCarrierError("country has no observed exact-code respondents")
        if incidence.verify_source_identity() != source or incidence.physical_metadata_digest != metadata:
            raise CountryCarrierError("source changed during country build")
        _live(require_current)
        info = dict(schema=SCHEMA,source_sha256=source,metadata_digest=metadata,
                    source_rows=incidence.row_count,country_variable=country_variable,
                    country_key=key,country_rows=country_rows)
        db.executemany("INSERT INTO meta VALUES(?,?)",[(k,canonical_json(v)) for k,v in info.items()])
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok" or db.execute("PRAGMA foreign_key_check").fetchone():
            raise CountryCarrierError("country SQLite integrity failed")
        db.commit()
        db.close()
        db = None
        _live(require_current)
        receipt = CountryReceipt(**{k:v for k,v in info.items() if k!="schema"},
                                 sha256=_hash(stage), bytes=stage.stat().st_size)
        # Publish only a complete committed file; link refuses overwrites.
        _live(require_current)
        os.link(stage,dest)
        try:
            _live(require_current)
        except BaseException:
            dest.unlink()
            raise
        return receipt
    finally:
        if db is not None:
            db.close()
        stage.unlink(missing_ok=True)
        Path(str(stage)+"-journal").unlink(missing_ok=True)

class CountryReader:
    """Cold reader requiring externally retained build receipt and currentness."""
    def __init__(self, path, receipt: CountryReceipt, *, require_current):
        if type(receipt) is not CountryReceipt:
            raise CountryCarrierError("external country receipt required")
        self.path, self.receipt, self.require_current = Path(path).resolve(), receipt, require_current
        self._verify()
        self.db = sqlite3.connect(self.path.as_uri()+"?mode=ro",uri=True)
        try:
            self.db.execute("PRAGMA query_only=ON")
            info = {k:json.loads(v) for k,v in self.db.execute("SELECT k,v FROM meta")}
            expected = {k:v for k,v in asdict(receipt).items() if k not in ("sha256","bytes")}
            if info != dict(schema=SCHEMA,**expected):
                raise CountryCarrierError("country receipt/metadata mismatch")
            self.variables = dict(self.db.execute("SELECT ordinal,name FROM vars ORDER BY ordinal"))
        except BaseException:
            self.db.close()
            raise
    def _verify(self):
        _live(self.require_current)
        if self.path.stat().st_size != self.receipt.bytes or _hash(self.path) != self.receipt.sha256:
            raise CountryCarrierError("country file differs from held receipt")
    def close(self):
        self.db.close()
    def __enter__(self):
        return self
    def __exit__(self,*args):
        self.close()
    def _blocks(self):
        previous, total = 0, 0
        for block,n,payload in self.db.execute("SELECT id,n,rows FROM blocks ORDER BY id"):
            _live(self.require_current)
            rows = _unpack(payload,8,n)
            if not rows or rows[0]<=previous or any(a>=b for a,b in zip(rows,rows[1:])) or rows[-1]>self.receipt.source_rows:
                raise CountryCarrierError("invalid source ordinal lane")
            previous, total = rows[-1],total+n
            yield block,rows
        if total != self.receipt.country_rows:
            raise CountryCarrierError("country row census mismatch")
    def _column(self, block, rows, ordinal):
        lane = self.db.execute("SELECT width,dict,codes FROM lanes WHERE block=? AND ordinal=?",(block,ordinal)).fetchone()
        if lane is None:
            raise CountryCarrierError("country variable lane missing")
        width,payload,codes = lane
        d = zlib.decompressobj()
        raw = d.decompress(payload,MAX_BYTES+1)
        if len(raw)>MAX_BYTES or not d.eof or d.unused_data or d.unconsumed_tail:
            raise CountryCarrierError("invalid dictionary compression")
        dictionary = tuple(json.loads(raw))
        ids = _unpack(codes,width,len(rows))
        if not dictionary or any(i>=len(dictionary) for i in ids):
            raise CountryCarrierError("invalid column dictionary codes")
        return NumericColumn(rows,ids,dictionary)
    def iter_columns(self, *names: str) -> Iterator[dict[str,NumericColumn]]:
        """One aligned block of actual numeric codes for requested variables."""
        by_name = {v:k for k,v in self.variables.items()}
        if not names or len(set(names))!=len(names) or any(n not in by_name for n in names):
            raise CountryCarrierError("distinct source-native variable names required")
        self._verify()
        for block,rows in self._blocks():
            yield {n:self._column(block,rows,by_name[n]) for n in names}
        self._verify()
    def matching_rows(self, conditions: dict) -> Iterator[int]:
        """Direct physical code intersections; NOT an issued I03 fact."""
        if not conditions:
            raise CountryCarrierError("explicit physical conditions required")
        for columns in self.iter_columns(*conditions):
            accepted = {n:col.observed_codes_for(conditions[n]) for n,col in columns.items()}
            rows = next(iter(columns.values())).row_ordinals
            for i,row in enumerate(rows):
                if all(col.codes[i] in accepted[n] for n,col in columns.items()):
                    yield row
    def row_ordinals(self):
        self._verify()
        for _,rows in self._blocks():
            yield from rows
        self._verify()
    def iter_cells(self):
        """Replay exact incumbent PhysicalCell values, without renumbering."""
        self._verify()
        for block,rows in self._blocks():
            columns = [self._column(block,rows,i).cells(i,n) for i,n in self.variables.items()]
            for record in zip(*columns):
                yield from record
        self._verify()
    def _native_stream(self, projection):
        from .pre553_source_backed_c11_facade import ExactPhysicalCellStream, GovernedC11Projection
        if type(projection) is not GovernedC11Projection:
            raise CountryCarrierError("explicit country-scoped governed projection required")
        selected = set(self.row_ordinals())
        bindings = [r.row_ordinal for r in projection.row_bindings]
        if len(bindings)!=len(selected) or set(bindings)!=selected:
            raise CountryCarrierError("projection must bind exact original country rows, not full wave")
        return ExactPhysicalCellStream(self.receipt.source_sha256,self.receipt.country_rows,
                 self.iter_cells,transport_identity="COUNTRY_NUMERIC_PHYSICAL@1:"+self.receipt.sha256,
                 decoder_metadata_digest=self.receipt.metadata_digest)
    def native_release(self, projection):
        """Use actual incumbent C11 owner, only with an explicitly scoped projection."""
        from .pre553_source_backed_c11_facade import build_validated_source_backed_c11_release_from_stream
        release = build_validated_source_backed_c11_release_from_stream(self._native_stream(projection),projection)
        self._verify()
        return release
    def native_repository(self, projection, *, cache=None, current_authorities=()):
        """Use incumbent compact event selector and shared I03 repository.

        Country logical projection is currently materialized once to certify it;
        existing compact selectors serve subsequent queries. This is not an
        independent grant to use a returned repository after source revocation.
        """
        from .pre553_source_backed_c11_facade import build_source_backed_c11_repository
        repo, release = build_source_backed_c11_repository(
            self._native_stream(projection),projection,cache=cache,
            current_authorities=current_authorities)
        self._verify()
        return repo, release
