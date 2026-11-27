"""Country-at-a-time compact physical survey carrier (S03 candidate).

Uses the incumbent PhysicalSourceIncidence and R5 codec. No source permission,
semantic mapping, population estimate or new analytical evaluator is issued.
Original source row ordinals survive. Ordinary cells are small dictionary codes,
not serialized C11 objects. A country-scoped governed projection is still
required for native C11/I03; a country shard must never impersonate a full wave.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from collections import OrderedDict
from collections.abc import Sequence
from copy import deepcopy
from array import array
import shutil
import sys
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
from .pre553_r5_codec import R5OpaqueValue, R5TypedValueCodec, canonical_json
from .pre553_source_backed_c11_facade import ExactPhysicalCellStream
from ._pre553_country_preparation import CountryPreparationPin

LEGACY_SCHEMA = "PYAT_COUNTRY_NUMERIC_PHYSICAL@1"
SCHEMA = "PYAT_COUNTRY_NUMERIC_PHYSICAL@2"
_BINARY_DICTIONARY = b"R5N2"
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

def _bounded_decompress(payload, limit=MAX_BYTES):
    d = zlib.decompressobj()
    raw = d.decompress(payload,limit+1)
    if len(raw)>limit or not d.eof or d.unused_data or d.unconsumed_tail:
        raise CountryCarrierError("invalid bounded dictionary compression")
    return raw

def _shuffle_words(words):
    # Byte planes: exact IEEE bits/int64, not quantization or numeric rounding.
    return bytes(b for i in range(8) for word in words for b in word[i:i+1])

def _unshuffle_words(raw,n):
    if len(raw)!=8*n:
        raise CountryCarrierError("numeric dictionary word census mismatch")
    return tuple(bytes(raw[i*n+j] for i in range(8)) for j in range(n))

def _pack_dictionary(dictionary):
    """Choose smaller of legacy full R5 token and split exact numeric dictionary.

    The R5 owner still defines every typed value. Finite IEEE words and inline
    integer words are stored as bit-exact binary planes. Exceptional R5 values
    remain canonical escapes. State/declaration/label live in a separate
    shared metadata dictionary. No numeric coercion, missing-value collapse,
    reinterpretation of dates, or assumption of unique numeric values.
    """
    legacy=canonical_json(dictionary).encode("ascii")
    if len(legacy)>MAX_BYTES:
        raise CountryCarrierError("dictionary block too large")
    old=zlib.compress(legacy)
    tags=bytearray()
    floats,ints,escapes,meta,meta_codes=[],[],[],[],[]
    meta_index={}
    for token in dictionary:
        obj=json.loads(token)
        if obj.get("t")!="tuple" or len(obj.get("v",()))!=4:
            raise CountryCarrierError("invalid R5 cell token")
        raw,*tail=obj["v"]
        tag=raw["t"]
        if tag=="float64_finite":
            tags.append(0);floats.append(bytes.fromhex(raw["bits"]))
        elif tag=="int":
            tags.append(1);ints.append(struct.pack(">q",int(raw["v"])))
        else:
            tags.append(2);escapes.append(raw)
        key=canonical_json(tail)
        if key not in meta_index:
            meta_index[key]=len(meta);meta.append(tail)
        meta_codes.append(meta_index[key])
    if not floats and not ints:
        return old
    side=canonical_json([escapes,meta]).encode("ascii")
    n=len(dictionary)
    body=(struct.pack("<IIII",n,len(floats),len(ints),len(side))+bytes(tags)
          +_shuffle_words(floats)+_shuffle_words(ints)
          +struct.pack("<"+"H"*n,*meta_codes)+side)
    if len(body)>MAX_BYTES:
        return old
    new=_BINARY_DICTIONARY+zlib.compress(body)
    return new if len(new)<len(old) else old

def _read_dictionary(payload, *, typed=False):
    """Keep the old token export; actual readers request typed R5 entries."""
    if not payload.startswith(_BINARY_DICTIONARY):
        tokens=tuple(json.loads(_bounded_decompress(payload)))
        if not typed:
            return tokens
        return _TypedCellDictionary(
            tuple(_CODEC.decode(json.loads(token)) for token in tokens),
            tokens=tokens)
    body=_bounded_decompress(payload[len(_BINARY_DICTIONARY):])
    if len(body)<16:
        raise CountryCarrierError("truncated binary R5 dictionary")
    n,nf,ni,side_n=struct.unpack_from("<IIII",body)
    if not 1<=n<=MAX_ROWS or nf+ni>n:
        raise CountryCarrierError("invalid binary R5 dictionary census")
    end=16+n+8*(nf+ni)+2*n
    if end+side_n!=len(body):
        raise CountryCarrierError("binary R5 dictionary extent mismatch")
    tags=body[16:16+n]
    if tags.count(0)!=nf or tags.count(1)!=ni or tags.count(2)!=n-nf-ni:
        raise CountryCarrierError("invalid binary R5 dictionary type lanes")
    off=16+n
    floats=iter(_unshuffle_words(body[off:off+8*nf],nf));off+=8*nf
    ints=iter(_unshuffle_words(body[off:off+8*ni],ni));off+=8*ni
    codes=struct.unpack_from("<"+"H"*n,body,off)
    escapes,meta=json.loads(body[end:])
    if len(escapes)!=n-nf-ni or not meta or any(c>=len(meta) for c in codes):
        raise CountryCarrierError("invalid binary R5 exception/metadata census")
    if any(not isinstance(x,list) or len(x)!=3 for x in meta):
        raise CountryCarrierError("invalid R5 cell metadata")
    other=iter(escapes);tokens=[]
    # Metadata is genuinely shared across raw dictionary values. Decode it
    # once; mutable descendants are detached only at the cell export boundary.
    tails=tuple(tuple(_CODEC.decode(part) for part in tail) for tail in meta) if typed else ()
    entries=[]
    for tag,code in zip(tags,codes):
        if tag==0:
            raw={"t":"float64_finite","bits":next(floats).hex()}
        elif tag==1:
            raw={"t":"int","v":str(struct.unpack(">q",next(ints))[0])}
        else:
            raw=next(other)
        if typed:
            entries.append((_CODEC.decode(raw),*tails[code]))
        else:
            tokens.append(canonical_json({"t":"tuple","v":[raw,*meta[code]]}))
    return _TypedCellDictionary(tuple(entries)) if typed else tuple(tokens)


def _needs_detach(value):
    # R5 decoding produces builtin containers, immutable scalars and the
    # frozen opaque escape. Nested tuples can still contain mutable members.
    if type(value) in (dict,list):
        return True
    return type(value) is tuple and any(_needs_detach(x) for x in value)


class _TypedCellDictionary(Sequence):
    """One decoded value/state tuple per distinct R5 cell token.

    No binary->JSON text->JSON parse roundtrip. Shared mutable metadata never
    escapes as an alias. The original canonical-token sequence remains
    available on demand for consumers that explicitly need a wire witness.
    """
    __slots__=("_entries","_detach","_tokens")
    def __init__(self,entries,*,tokens=None):
        for entry in entries:
            if type(entry) is not tuple or len(entry)!=4:
                raise CountryCarrierError("invalid typed R5 cell dictionary entry")
            PhysicalMissingState(entry[1])
        self._entries=entries
        self._detach=bytes(_needs_detach(entry) for entry in entries)
        self._tokens=tokens
    def __len__(self):
        return len(self._entries)
    def __getitem__(self,index):
        if isinstance(index,slice):
            return tuple(self[i] for i in range(*index.indices(len(self))))
        if self._tokens is not None:
            return self._tokens[index]
        return canonical_json(_CODEC.encode(self._entries[index]))
    def decoded(self,index):
        entry=self._entries[index]
        return deepcopy(entry) if self._detach[index] else entry
    def observed_codes_for(self,value):
        target=_CODEC.typed_key(value)
        return frozenset(i for i,(raw,state,_,_) in enumerate(self._entries)
            if state==PhysicalMissingState.OBSERVED_STORAGE_VALUE.value and _CODEC.typed_key(raw)==target)
    def retained_bytes(self):
        # Conservative shallow+recursive accounting of distinct reachable
        # Python objects, not a serialization of each token or process RSS.
        seen=set()
        def size(value):
            identity=id(value)
            if identity in seen:
                return 0
            seen.add(identity)
            total=sys.getsizeof(value)
            if isinstance(value,(tuple,list)):
                total+=sum(size(x) for x in value)
            elif isinstance(value,dict):
                total+=sum(size(k)+size(v) for k,v in value.items())
            elif type(value) is R5OpaqueValue:
                # The frozen wrapper is small; its bytes payload need not be.
                total+=size(vars(value))
            return total
        return sys.getsizeof(self)+size(self._entries)+size(self._detach)+size(self._tokens)

def _digest(kind,coordinates,*payloads):
    """Domain- and coordinate-bound authentication of exact stored bytes."""
    h=sha256(canonical_json([kind,*coordinates]).encode("ascii"))
    for blob in payloads:
        h.update(struct.pack("<Q",len(blob)))
        h.update(blob)
    return h.digest()

def _manifest_root(variables,blocks,lanes):
    """Hash the exact v2 canonical JSON preimage without building its full body.

    Each record is still canonicalized by R5. Array punctuation is identical
    to canonical_json([SCHEMA, list(variables), ..., ...]); no new schema,
    digest algorithm, ordering, scope or receipt identity is introduced.
    """
    from itertools import islice
    h=sha256()
    h.update(b"[")
    h.update(canonical_json(SCHEMA).encode("ascii"))
    for rows in (variables, ([i,n,d.hex()] for i,n,d in blocks),
                 ([i,j,d.hex()] for i,j,d in lanes)):
        h.update(b",[")
        first=True
        records=iter(rows)
        # A bounded chunk preserves B's memory law while amortizing Python
        # encoder calls. Strip only the outer array punctuation; the same
        # canonical encoder owns all members and their escaping.
        while True:
            chunk=tuple(islice(records,256))
            if not chunk:
                break
            if not first:
                h.update(b",")
            encoded=canonical_json(chunk).encode("ascii")
            h.update(memoryview(encoded)[1:-1])
            first=False
        h.update(b"]")
    h.update(b"]")
    return h.hexdigest()

def _stat_signature(path):
    st=path.stat()
    return st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns

def _encode_cell(cell: PhysicalCell) -> str:
    return canonical_json(_CODEC.encode((cell.raw_value, cell.missing_state.value,
                                        cell.source_missing_declaration, cell.raw_value_label)))

def _scalar_memo_key(value):
    """Bounded exact builtin subset of R5; None means use the full codec.

    Type tags prevent bool/int/float equality from collapsing identities.
    IEEE bits preserve signed zero. Nonbuiltin and mutable values never
    enter the shortcut. No alternate persisted encoding is introduced.
    """
    kind=type(value)
    if value is None:
        return (0,None)
    if kind is bool:
        return (1,value)
    if kind is int and -32768<=value<=32767:
        return (2,value)
    if kind is float and -32768<=value<=32767 and value.is_integer():
        return (3,struct.pack(">d",value))
    if kind is str and len(value)<=64:
        return (4,value)
    if kind is bytes and len(value)<=64:
        return (5,value)
    return None


class _CellTokenMemo:
    """Block-scoped, bounded admission of common immutable physical cells.

    Keep at most 256 entries, each with a bounded key and canonical token.
    Cold high-cardinality values use the incumbent encoder. No eviction
    churn, no mutable metadata alias, no authority or schema change.
    """
    __slots__=("entries","limit")
    def __init__(self,limit=256):
        self.entries={}
        self.limit=limit

    def token(self,cell):
        if (not self.limit or cell.source_missing_declaration is not None
                or type(cell.missing_state) is not PhysicalMissingState):
            return _encode_cell(cell)
        raw=_scalar_memo_key(cell.raw_value)
        label=_scalar_memo_key(cell.raw_value_label)
        if raw is None or label is None:
            return _encode_cell(cell)
        key=(raw,cell.missing_state,label)
        hit=self.entries.get(key)
        if hit is not None:
            return hit
        token=_encode_cell(cell)
        if len(self.entries)<self.limit and len(token)<=1024:
            self.entries[key]=token
        return token


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
    # Optional only for backwards reading v1 files. All new builds carry
    # this independently retained authenticated row/column inventory root.
    lane_root: str | None = None

    def __post_init__(self):
        for value in (self.source_sha256,self.metadata_digest,self.sha256):
            if type(value) is not str or len(value)!=64 or any(c not in "0123456789abcdef" for c in value):
                raise CountryCarrierError("country receipt requires exact SHA256 pins")
        if self.lane_root is not None and (type(self.lane_root) is not str
            or len(self.lane_root)!=64 or any(c not in "0123456789abcdef" for c in self.lane_root)):
            raise CountryCarrierError("country receipt requires exact lane inventory root")
        if (type(self.source_rows) is not int or type(self.country_rows) is not int
            or not 0<self.country_rows<=self.source_rows or type(self.bytes) is not int or self.bytes<=0
            or type(self.country_variable) is not str or not self.country_variable
            or type(self.country_key) is not str):
            raise CountryCarrierError("invalid country receipt scope")
        if canonical_json(_CODEC.encode(_CODEC.decode(json.loads(self.country_key))))!=self.country_key:
            raise CountryCarrierError("country receipt code must be canonical R5")


@dataclass(frozen=True)
class NumericColumn:
    """Codes and exact R5 value/state dictionary, in original respondent order."""
    row_ordinals: tuple[int, ...]
    codes: tuple[int, ...]
    dictionary: Sequence[str]

    def cell_at(self, offset, ordinal, name):
        row,code=self.row_ordinals[offset],self.codes[offset]
        if type(self.dictionary) is _TypedCellDictionary:
            raw,state,declaration,label=self.dictionary.decoded(code)
            return PhysicalCell(row,ordinal,name,raw,PhysicalMissingState(state),declaration,label)
        return _decode_cell(row,ordinal,name,self.dictionary[code])

    def cells(self, ordinal, name):
        for offset in range(len(self.row_ordinals)):
            yield self.cell_at(offset,ordinal,name)

    def observed_codes_for(self, value):
        if type(self.dictionary) is _TypedCellDictionary:
            return self.dictionary.observed_codes_for(value)
        target = _CODEC.typed_key(value)
        result = set()
        for i, token in enumerate(self.dictionary):
            raw, state, _, _ = _CODEC.decode(json.loads(token))
            if state == PhysicalMissingState.OBSERVED_STORAGE_VALUE.value and _CODEC.typed_key(raw) == target:
                result.add(i)
        return frozenset(result)

def _check_space(root,min_free_bytes):
    free=shutil.disk_usage(root).free
    if free<min_free_bytes:
        raise CountryCarrierError(f"country build disk reserve: {free} free bytes, "
                                  f"{min_free_bytes} required; completed files retained")


class _CountryWriter:
    """One independent country artifact; bounded column dictionaries during build.

    Never retain a row-by-column grid of repeated serialized tokens. Intern
    each token as it arrives; pending codes use two bytes per cell. For
    high-cardinality data flush early at a conservative container estimate.
    """
    def __init__(self,incidence,country_variable,key,dest,require_current,
                 block_rows,pending_budget,min_free_bytes):
        self.incidence,self.country_variable,self.key=incidence,country_variable,key
        self.dest=Path(dest).resolve()
        self.current=require_current
        self.block_rows,self.budget,self.min_free=block_rows,pending_budget,min_free_bytes
        self.variables=tuple((v.ordinal,v.name) for v in incidence.variables)
        self.country_index=next(i for i,(_,n) in enumerate(self.variables) if n==country_variable)
        if not self.dest.parent.is_dir():
            raise CountryCarrierError("existing private country destination required")
        if self.dest.exists():
            raise CountryCarrierError(f"country file already exists: {self.dest}; "
                                      "resume with externally retained exact receipt; never overwrite")
        _live(self.current)
        _check_space(self.dest.parent,self.min_free)
        self.source=incidence.source_sha256
        self.metadata=incidence.physical_metadata_digest
        self.stage=None
        self.db=None
        self.count=self.block=0
        self.previous=0
        try:
            fd,tmp=tempfile.mkstemp(prefix=".country-",suffix=".sqlite",dir=self.dest.parent)
            os.close(fd)
            self.stage=Path(tmp)
            self.db=sqlite3.connect(self.stage)
            self.db.executescript("""
              PRAGMA journal_mode=DELETE;
              PRAGMA synchronous=FULL;
              PRAGMA cache_size=-1024;
              PRAGMA foreign_keys=ON;
              CREATE TABLE meta(k TEXT PRIMARY KEY,v TEXT NOT NULL);
              CREATE TABLE vars(ordinal INTEGER PRIMARY KEY,name TEXT NOT NULL UNIQUE);
              CREATE TABLE blocks(id INTEGER PRIMARY KEY,n INTEGER NOT NULL,rows BLOB NOT NULL,digest BLOB NOT NULL);
              CREATE TABLE lanes(block INTEGER NOT NULL REFERENCES blocks(id),ordinal INTEGER NOT NULL REFERENCES vars(ordinal),
                 width INTEGER NOT NULL,dict BLOB NOT NULL,codes BLOB NOT NULL,digest BLOB NOT NULL,
                 PRIMARY KEY(block,ordinal));
            """)
            self.db.executemany("INSERT INTO vars VALUES(?,?)",self.variables)
            self._reset()
        except BaseException:
            self.abort()
            raise

    def _reset(self):
        self.rows=array("Q")
        self.columns=[([],{},array("H")) for _ in self.variables]
        self.estimated_bytes=256*len(self.variables)
        # Separate small, bounded acceleration allowance; do not change
        # the incumbent pending-token estimate or physical block geometry.
        # Disable for tight explicit pending budgets.
        self.token_memo=_CellTokenMemo(min(256,max(0,self.budget//65536)))

    def append(self,cells):
        if tuple((c.variable_ordinal,c.variable_name) for c in cells)!=self.variables:
            raise CountryCarrierError("missing, duplicated or reordered physical cell")
        row=cells[0].row_ordinal
        if not self.previous<row<=self.incidence.row_count or any(c.row_ordinal!=row for c in cells):
            raise CountryCarrierError("country row identity/order mismatch")
        country=cells[self.country_index]
        if (country.missing_state is not PhysicalMissingState.OBSERVED_STORAGE_VALUE
            or canonical_json(_CODEC.encode(country.raw_value))!=self.key):
            raise CountryCarrierError("selected row does not belong to country")
        # A single row must fit before any data can be published; estimate
        # unique-token storage and compact code arrays independently.
        tokens=tuple(self.token_memo.token(c) for c in cells)
        def increment():
            return 16+sum(4+(sys.getsizeof(t)+100 if t not in col[1] else 0)
                          for col,t in zip(self.columns,tokens))
        cost=increment()
        if self.rows and self.estimated_bytes+cost>self.budget:
            self.flush()
            cost=increment()
        if self.estimated_bytes+cost>self.budget:
            raise CountryCarrierError("one exact source row exceeds country pending-memory budget; "
                                      "increase explicit budget or reduce selected simultaneous countries")
        self.rows.append(row)
        for (dictionary,index,codes),token in zip(self.columns,tokens):
            code=index.get(token)
            if code is None:
                code=len(dictionary)
                dictionary.append(token)
                index[token]=code
            codes.append(code)
        self.estimated_bytes+=cost
        self.previous=row
        self.count+=1
        if len(self.rows)>=self.block_rows:
            self.flush()

    def flush(self):
        if not self.rows:
            return
        _live(self.current)
        _check_space(self.dest.parent,self.min_free)
        n=len(self.rows)
        row_blob=_pack(self.rows,8)
        self.db.execute("INSERT INTO blocks VALUES(?,?,?,?)",
                        (self.block,n,row_blob,_digest("ROWS",(self.block,n),row_blob)))
        for (ordinal,_),(dictionary,index,codes) in zip(self.variables,self.columns):
            width=1 if len(dictionary)<=256 else 2
            payload=_pack_dictionary(dictionary)
            if len(dictionary)==n and all(i==code for i,code in enumerate(codes)):
                width,packed=0,b""
            else:
                packed=_pack(codes,width)
            self.db.execute("INSERT INTO lanes VALUES(?,?,?,?,?,?)",
                 (self.block,ordinal,width,payload,packed,
                  _digest("LANE",(self.block,ordinal,width),payload,packed)))
        self.db.commit()
        self.block+=1
        self._reset()

    def finish(self,expected_count=None):
        if not self.count or (expected_count is not None and self.count!=expected_count):
            raise CountryCarrierError("country build does not match exact census")
        self.flush()
        _live(self.current)
        lane_root=_manifest_root(self.variables,
            self.db.execute("SELECT id,n,digest FROM blocks ORDER BY id"),
            self.db.execute("SELECT block,ordinal,digest FROM lanes ORDER BY block,ordinal"))
        info=dict(schema=SCHEMA,source_sha256=self.source,metadata_digest=self.metadata,
            source_rows=self.incidence.row_count,country_variable=self.country_variable,
            country_key=self.key,country_rows=self.count,lane_root=lane_root)
        self.db.executemany("INSERT INTO meta VALUES(?,?)",
            [(k,canonical_json(v)) for k,v in info.items()])
        if (self.db.execute("PRAGMA integrity_check").fetchone()[0]!="ok"
                or self.db.execute("PRAGMA foreign_key_check").fetchone()):
            raise CountryCarrierError("country SQLite integrity failed")
        self.db.commit()
        self.db.close()
        self.db=None
        _live(self.current)
        receipt=CountryReceipt(**{k:v for k,v in info.items() if k!="schema"},
            sha256=_hash(self.stage),bytes=self.stage.stat().st_size)
        _live(self.current)
        os.link(self.stage,self.dest)
        try:
            directory_fd=os.open(self.dest.parent,os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
            _live(self.current)
        except BaseException:
            self.dest.unlink()
            raise
        return receipt

    def abort(self):
        if self.db is not None:
            self.db.close()
            self.db=None
        if self.stage is not None:
            self.stage.unlink(missing_ok=True)
            Path(str(self.stage)+"-journal").unlink(missing_ok=True)


def _build_limits(incidence,country_variable,block_rows,pending_budget,min_free):
    if type(incidence) is not PhysicalSourceIncidence:
        raise CountryCarrierError("incumbent physical decoder incidence required")
    if type(block_rows) is not int or not 1<=block_rows<=MAX_ROWS:
        raise CountryCarrierError("invalid country block size")
    variables=tuple((v.ordinal,v.name) for v in incidence.variables)
    if (not variables or len(set(variables))!=len(variables)
            or len({v[1] for v in variables})!=len(variables)):
        raise CountryCarrierError("invalid source variable inventory")
    if country_variable not in {name for _,name in variables}:
        raise CountryCarrierError("explicit source-native country variable required")
    if type(pending_budget) is not int or pending_budget<=256*len(variables):
        raise CountryCarrierError("invalid country pending-memory budget")
    if type(min_free) is not int or min_free<0:
        raise CountryCarrierError("invalid disk reserve")


def _feed_writers(incidence,country_variable,writers,require_current):
    """One content-bound selected source scan; never a full-wave expanded estate."""
    _live(require_current)
    source=incidence.verify_source_identity()
    metadata=incidence.physical_metadata_digest
    values=tuple(_CODEC.decode(json.loads(key)) for key in writers)
    cells=[]
    previous=0
    country_index=next(i for i,v in enumerate(incidence.variables) if v.name==country_variable)
    width=len(incidence.variables)
    def accept():
        if len(cells)!=width:
            raise CountryCarrierError("selected source row incomplete")
        country=cells[country_index]
        key=canonical_json(_CODEC.encode(country.raw_value))
        writer=writers.get(key)
        if writer is None:
            raise CountryCarrierError("selected stream returned unrequested country")
        writer.append(cells)
    stream=(incidence.iter_country_cells(country_variable,values[0]) if len(values)==1
            else incidence.iter_countries_cells(country_variable,values))
    for cell in stream:
        if type(cell) is not PhysicalCell:
            raise CountryCarrierError("foreign physical cell")
        if cell.row_ordinal!=previous:
            if cells:
                accept()
                cells.clear()
            if not previous<cell.row_ordinal<=incidence.row_count:
                raise CountryCarrierError("selected source rows out of order")
            previous=cell.row_ordinal
        cells.append(cell)
        if len(cells)>width:
            raise CountryCarrierError("duplicate source row slot")
    if cells:
        accept()
    if incidence.verify_source_identity()!=source or incidence.physical_metadata_digest!=metadata:
        raise CountryCarrierError("source changed during country build")
    _live(require_current)


def build_country(incidence: PhysicalSourceIncidence, *, country_variable: str,
                  country_value, output: str | Path, require_current: Callable[[], None],
                  block_rows: int=1024, pending_bytes: int=32*1024*1024,
                  min_free_bytes: int=64*1024*1024) -> CountryReceipt:
    """Build one exact country; compact, independent, atomically published."""
    _build_limits(incidence,country_variable,block_rows,pending_bytes,min_free_bytes)
    _live(require_current)
    key=canonical_json(_CODEC.encode(country_value))
    writer=_CountryWriter(incidence,country_variable,key,output,require_current,
                          block_rows,pending_bytes,min_free_bytes)
    try:
        _feed_writers(incidence,country_variable,{key:writer},require_current)
        return writer.finish()
    finally:
        writer.abort()


class _PackedLaneDigests:
    """Exact rectangular lane inventory, in authenticated SQL key order.

    Block ids are dense from zero; variable ordinals need not be dense.
    The only retained per-lane payload is the original 32-byte digest.
    """
    __slots__=("_positions","_width","_digests")
    def __init__(self,ordinals,digests):
        self._positions={ordinal:i for i,ordinal in enumerate(ordinals)}
        self._width=len(ordinals)
        if not self._width or len(self._positions)!=self._width or len(digests)%(32*self._width):
            raise CountryCarrierError("invalid packed lane digest extent")
        self._digests=bytes(digests)

    def __len__(self):
        return len(self._digests)//32

    def get(self,key,default=None):
        block,ordinal=key
        position=self._positions.get(ordinal)
        if position is None or type(block) is not int or block<0:
            return default
        index=block*self._width+position
        if index>=len(self):
            return default
        start=32*index
        return self._digests[start:start+32]


class CountryReader:
    """Cold reader requiring externally retained build receipt and currentness."""
    def __init__(self, path, receipt: CountryReceipt, *, require_current):
        if type(receipt) is not CountryReceipt:
            raise CountryCarrierError("external country receipt required")
        self.path, self.receipt, self.require_current = Path(path).resolve(), receipt, require_current
        self._closed = False
        self._signature = _stat_signature(self.path)
        # Authenticate the complete retained artifact once on cold opening.
        self.verify_full()
        self._block_auth,self._lane_auth=None,None
        self.db = sqlite3.connect(self.path.as_uri()+"?mode=ro"+("&immutable=1" if receipt.lane_root else ""),uri=True)
        self._certified_identity = None
        self._certified_facade_key = None
        try:
            self.db.execute("PRAGMA query_only=ON")
            info = {k:json.loads(v) for k,v in self.db.execute("SELECT k,v FROM meta")}
            expected = {k:v for k,v in asdict(receipt).items() if k not in ("sha256","bytes") and v is not None}
            if info != dict(schema=SCHEMA if receipt.lane_root else LEGACY_SCHEMA,**expected):
                raise CountryCarrierError("country receipt/metadata mismatch")
            variables=tuple(self.db.execute("SELECT ordinal,name FROM vars ORDER BY ordinal"))
            self.variables = dict(variables)
            if receipt.lane_root:
                # Stream the SQL inventory directly into its final lookup
                # maps while hashing the same external canonical preimage.
                # No complete cursor tuple survives alongside those maps.
                self._block_auth={}
                ordinals=tuple(self.variables)
                if not ordinals or len(ordinals)!=len(variables):
                    raise CountryCarrierError("invalid authenticated variable inventory")
                lane_digests=bytearray()
                def blocks():
                    for i,n,d in self.db.execute("SELECT id,n,digest FROM blocks ORDER BY id"):
                        if (i!=len(self._block_auth) or not 1<=n<=MAX_ROWS
                                or type(d) is not bytes or len(d)!=32):
                            raise CountryCarrierError("invalid authenticated row block inventory")
                        self._block_auth[i]=(n,d)
                        yield i,n,d
                def lanes():
                    for i,j,d in self.db.execute("SELECT block,ordinal,digest FROM lanes ORDER BY block,ordinal"):
                        block,position=divmod(len(lane_digests)//32,len(ordinals))
                        # Exact ordered rectangular census: no duplicate, gap,
                        # alien coordinate or reordering can enter the lane.
                        if (i!=block or i not in self._block_auth or j!=ordinals[position]
                                or type(d) is not bytes or len(d)!=32):
                            raise CountryCarrierError("invalid authenticated column lane inventory")
                        lane_digests.extend(d)
                        yield i,j,d
                if _manifest_root(variables,blocks(),lanes())!=receipt.lane_root:
                    raise CountryCarrierError("country lane inventory differs from external receipt")
                if (sum(n for n,_ in self._block_auth.values())!=receipt.country_rows
                    or len(lane_digests)!=32*len(self._block_auth)*len(ordinals)):
                    raise CountryCarrierError("country authenticated lane inventory incomplete")
                self._lane_auth=_PackedLaneDigests(ordinals,lane_digests)
            self._verify()
        except BaseException:
            self.db.close()
            raise
    def _check_live_file(self):
        if self._closed:
            raise CountryCarrierError("country reader closed")
        _live(self.require_current)
        try:
            same=_stat_signature(self.path)==self._signature
        except OSError as exc:
            raise CountryCarrierError("country file no longer available") from exc
        if not same:
            raise CountryCarrierError("country file changed during reader session")

    def verify_full(self):
        self._check_live_file()
        if self._signature[2]!=self.receipt.bytes or _hash(self.path)!=self.receipt.sha256:
            raise CountryCarrierError("country file differs from held receipt")
        self._check_live_file()

    def _verify(self):
        # Stat checks are a mutation alarm, NEVER the v2 authentication
        # proof: the held root authenticates inventory, and each selected
        # row/column blob is authenticated before decoding. Old v1 files
        # have no per-lane pin and therefore keep the old full-hash path.
        if self.receipt.lane_root is None:
            self.verify_full()
        else:
            self._check_live_file()
    def close(self):
        if not self._closed:
            self._closed = True
            self.db.close()
    def __enter__(self):
        return self
    def __exit__(self,*args):
        self.close()
    def _blocks(self):
        previous, total = 0, 0
        seen=[]
        for block,n,payload in self.db.execute("SELECT id,n,rows FROM blocks ORDER BY id"):
            self._check_live_file()
            if self._block_auth is not None and self._block_auth.get(block)!=(n,_digest("ROWS",(block,n),payload)):
                raise CountryCarrierError("row block authentication failed")
            seen.append(block)
            rows = _unpack(payload,8,n)
            if not rows or rows[0]<=previous or any(a>=b for a,b in zip(rows,rows[1:])) or rows[-1]>self.receipt.source_rows:
                raise CountryCarrierError("invalid source ordinal lane")
            previous, total = rows[-1],total+n
            yield block,rows
        if total != self.receipt.country_rows or (self._block_auth is not None and tuple(seen)!=tuple(self._block_auth)):
            raise CountryCarrierError("country row census mismatch")
    def _column(self, block, rows, ordinal):
        lane = self.db.execute("SELECT width,dict,codes FROM lanes WHERE block=? AND ordinal=?",(block,ordinal)).fetchone()
        if lane is None:
            raise CountryCarrierError("country variable lane missing")
        width,payload,codes = lane
        if self._lane_auth is not None and self._lane_auth.get((block,ordinal))!=_digest("LANE",(block,ordinal,width),payload,codes):
            raise CountryCarrierError("column lane authentication failed")
        dictionary = _read_dictionary(payload,typed=True)
        if width==0:
            if self.receipt.lane_root is None or codes!=b"" or len(dictionary)!=len(rows):
                raise CountryCarrierError("invalid implicit identity code lane")
            ids=tuple(range(len(rows)))
        else:
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
        """Replay every native cell, without renumbering."""
        yield from self._iter_slots(tuple(self.variables.items()))

    def _iter_slots(self,slots):
        """Exact authenticated selected slots; full physical API remains available."""
        if not slots or any(self.variables.get(i)!=n for i,n in slots):
            raise CountryCarrierError("governed slot absent from authenticated variable inventory")
        self._verify()
        for block,rows in self._blocks():
            columns=[self._column(block,rows,i).cells(i,n) for i,n in slots]
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
        projected={rule.slot.key for rules in (projection.response_slots,projection.coordinate_slots,
                                                  projection.weight_slots) for rule in rules}
        slots=tuple((i,n) for i,n in self.variables.items() if (i,n) in projected)
        if set(slots)!=projected:
            raise CountryCarrierError("projection slot identity absent from country carrier")
        # The existing facade consumes only projected slots and independently
        # validates every required row/slot. Unowned columns remain stored,
        # queryable via the physical API and available for future projections.
        return _CountryPhysicalStream(self.receipt.source_sha256,self.receipt.country_rows,
                 lambda:self._iter_slots(slots),transport_identity="COUNTRY_NUMERIC_PHYSICAL@1:"+self.receipt.sha256,
                 decoder_metadata_digest=self.receipt.metadata_digest,reader=self)
    def native_release(self, projection):
        """Use actual incumbent C11 owner, only with an explicitly scoped projection."""
        from .pre553_source_backed_c11_facade import build_validated_source_backed_c11_release_from_stream
        release = build_validated_source_backed_c11_release_from_stream(self._native_stream(projection),projection)
        self._verify()
        return release
    def native_repository(self, projection, *, cache=None, current_authorities=()):
        """Use incumbent compact event selector and shared I03 repository.

        I02 validates actual events while emitting compact headers;
        existing compact selectors serve subsequent queries. This is not an
        independent grant to use a returned repository after source revocation.
        """
        from .pre553_source_backed_c11_facade import build_source_backed_c11_repository
        repo, release = build_source_backed_c11_repository(
            self._native_stream(projection),projection,cache=cache,
            current_authorities=current_authorities)
        self._verify()
        return repo, release

@dataclass(frozen=True)
class _CountryPhysicalStream(ExactPhysicalCellStream):
    """Recognized only by the incumbent facade; no generic user-supplied body factory."""
    reader: CountryReader | None = None

    def _verify_binding(self):
        if type(self.reader) is not CountryReader or self.reader._closed:
            raise CountryCarrierError("country body resolver requires its live reader")
        self.reader._verify()
        if self.transport_identity != "COUNTRY_NUMERIC_PHYSICAL@1:"+self.reader.receipt.sha256:
            raise CountryCarrierError("country transport pin mismatch")
    def compact_events(self,release_ref,replay_ref,non_events,headers,projection,closure_refs,routing=None):
        self._verify_binding()
        from ._pre553_c11_execution_view import _compact_country_headers
        bodies=_CountryEventBodies(self.reader,projection,headers,closure_refs=closure_refs)
        return _compact_country_headers(release_ref,replay_ref,non_events,headers,bodies,routing)

    def certify_release(self,release,*,facade_key=None):
        self._verify_binding()
        from .pre553_durable_empirical_closure import ReleaseIdentity
        self.reader._certified_identity = ReleaseIdentity(
            release.release_ref,release.replay_manifest.ref,release.source_artifact_ref,
            release.source_release_manifest_hash,release.semantic_release_hash)
        self.reader._certified_facade_key=facade_key

    def event_bodies(self, release, events, projection):
        self.certify_release(release)
        return _CountryEventBodies(self.reader, projection, events)

class _BodyScalar:
    __slots__ = ("value",)
    def __init__(self,value):
        self.value=value
    def as_py(self):
        return self.value

class _CountryEventBodies:
    """The existing _EventLane's byte-reader ABI, backed by original numeric cells.

    Only original row/slot/expected exact-ref locators are retained for events.
    No serialized event bodies, no duplicate permanent archive. The existing
    _event constructor remains the authority on the event's exact preimage.
    The validated release has already sealed every occurrence. The selected
    reader must remain open, and current-use checks bracket workload delivery.
    """
    __slots__=("reader","projection","rows","slots","owners","respondents","respondent_keys",
               "source_rows","question_keys","respondent_codes","question_codes","hashes",
               "cache","cache_bytes","direct","row_ordinals","row_respondents",
               "slot_occurrences","value_rules")
    def __init__(self,reader,projection,events,*,closure_refs=None):
        from .pre553_empirical_objects import exact_ref, RespondentEvent, URN_PREFIX
        from .pre553_c11_integrity import _PackedClosureRefs
        shared=(closure_refs.digest_lane(RespondentEvent.FAMILY,f"{URN_PREFIX}:RespondentEvent:sha256:")
                if type(closure_refs) is _PackedClosureRefs else None)
        if shared is not None and len(shared)!=32*len(events):
            raise CountryCarrierError("sealed replay event lane cardinality drift")
        self.reader,self.projection=reader,projection
        self.rows={row:(block,rows,i) for block,rows in reader._blocks() for i,row in enumerate(rows)}
        from ._pre553_c11_execution_view import _CountryEventHeader
        self.direct=bool(events) and type(events[0]) is _CountryEventHeader
        self.respondents={r.ref.key:r for r in projection.respondents}
        self.owners={x.slot.key:x for x in projection.slot_owner_sets}
        self.slots={}
        if self.direct:
            # Two uint32 lanes replace (not supplement) respondent/question
            # codes. Sparse original row ordinals are shared once per row.
            self.row_ordinals=tuple(self.rows)
            row_index={row:i for i,row in enumerate(self.row_ordinals)}
            self.row_respondents={b.row_ordinal:self.respondents[b.respondent_ref.key]
                                  for b in projection.row_bindings}
            slots={s.slot.ordinal:s for s in projection.response_slots}
            pairs=[]; pair_index={}
            self.value_rules={s.slot.ordinal:{r.physical_key:r for r in s.values}
                              for s in projection.response_slots}
            # The prior enumerating body reader refused ambiguous physical
            # rules rather than allowing dict collapse. Keep that refusal.
            if any(len(self.value_rules[s.slot.ordinal])!=len(s.values)
                   for s in projection.response_slots):
                raise CountryCarrierError("country response slot has ambiguous physical value rules")
            self.respondent_keys=self.source_rows=self.question_keys=()
        else:
            # Compatibility for the older expanded-event transport only.
            self.row_ordinals=self.slot_occurrences=()
            self.row_respondents=self.value_rules={}
            by_respondent={}
            for b in projection.row_bindings:
                by_respondent.setdefault(b.respondent_ref.key,[]).append(b.row_ordinal)
            for slot in projection.response_slots:
                self.slots.setdefault(slot.question_binding.ref.key,[]).append(slot)
            self.respondent_keys=tuple(by_respondent)
            self.source_rows=tuple(tuple(by_respondent[key]) for key in self.respondent_keys)
            self.question_keys=tuple(self.slots)
            ri={key:i for i,key in enumerate(self.respondent_keys)}
            qi={key:i for i,key in enumerate(self.question_keys)}
        rc,qc=array("I"),array("I")
        hashes=bytearray()
        prior=b""
        for offset,event in enumerate(events):
            respondent=exact_ref(event.scoped_respondent_ref).key
            if self.direct:
                if type(event) is not _CountryEventHeader:
                    raise CountryCarrierError("mixed country event locator representation")
                row,ordinal,occurrence=event.source_coordinates
                slot=slots.get(ordinal)
                bound=self.row_respondents.get(row)
                if (row not in row_index or bound is None or bound.ref.key!=respondent
                        or slot is None or slot.question_binding.ref not in event.dependency_refs
                        or type(occurrence) is not int or occurrence<0):
                    raise CountryCarrierError("sealed event lacks exact emitted physical coordinates")
                pair=(ordinal,occurrence)
                code=pair_index.get(pair)
                if code is None:
                    code=len(pairs)
                    pair_index[pair]=code
                    pairs.append((slot,occurrence))
                rc.append(row_index[row]);qc.append(code)
            else:
                bindings=[r.key for r in event.dependency_refs if r.key in self.slots]
                if respondent not in ri or len(bindings)!=1:
                    raise CountryCarrierError("sealed event lacks original country row/slot binding")
                rc.append(ri[respondent]);qc.append(qi[bindings[0]])
            ref=event.ref
            digest=bytes.fromhex(ref.content_hash)
            if (ref!=self._event_ref(digest) or len(digest)!=32 or digest<=prior):
                raise CountryCarrierError("sealed event canonical identity/order mismatch")
            prior=digest
            if shared is None:
                hashes.extend(digest)
            elif shared[32*offset:32*(offset+1)]!=digest:
                raise CountryCarrierError("sealed replay event lane identity drift")
        if self.direct:
            self.slot_occurrences=tuple(pairs)
        self.respondent_codes=memoryview(rc.tobytes()).cast("I")
        self.question_codes=memoryview(qc.tobytes()).cast("I")
        self.hashes=shared if shared is not None else bytes(hashes)
        self.cache=OrderedDict()
        self.cache_bytes=0

    @staticmethod
    def _event_ref(digest):
        from .pre553_empirical_objects import ExactRef,RespondentEvent,URN_PREFIX
        h=digest.hex()
        return ExactRef(RespondentEvent.FAMILY,f"{URN_PREFIX}:RespondentEvent:sha256:{h}",h)

    def __len__(self):
        return len(self.respondent_codes)

    @property
    def locator_bytes(self):
        return self.respondent_codes.nbytes+self.question_codes.nbytes+len(self.hashes)

    def find_event(self,ref):
        """Exact membership lookup without a per-event Python hash table."""
        from .pre553_empirical_objects import ExactRef,RespondentEvent
        if not isinstance(ref,ExactRef) or ref.kind!=RespondentEvent.FAMILY:
            return None
        digest=bytes.fromhex(ref.content_hash)
        if ref!=self._event_ref(digest):
            return None
        lo,hi=0,len(self)
        while lo<hi:
            mid=(lo+hi)//2
            if self.hashes[32*mid:32*(mid+1)]<digest:
                lo=mid+1
            else:
                hi=mid
        return lo if lo<len(self) and self.hashes[32*lo:32*(lo+1)]==digest else None

    def check_current(self):
        self.reader._verify()

    def check_live(self):
        """Every existing country-backed exact-object reader must remain CURRENT."""
        self.reader._check_live_file()

    def _cell(self,row,slot):
        block,rows,offset=self.rows[row]
        key=(block,slot.slot.ordinal)
        lane=self.cache.get(key)
        if lane is None:
            lane=self.reader._column(block,rows,slot.slot.ordinal)
            size=(sys.getsizeof(lane)+sys.getsizeof(lane.codes)
                  +sum(sys.getsizeof(x) for x in lane.codes)
                  + (lane.dictionary.retained_bytes() if type(lane.dictionary) is _TypedCellDictionary
                     else sys.getsizeof(lane.dictionary)+sum(sys.getsizeof(x) for x in lane.dictionary)))
            if size<=8*1024*1024:
                while self.cache and (len(self.cache)>=32 or self.cache_bytes+size>8*1024*1024):
                    _,(_,old)=self.cache.popitem(last=False)
                    self.cache_bytes-=old
                self.cache[key]=(lane,size)
                self.cache_bytes+=size
        else:
            lane,_=lane
            self.cache.move_to_end(key)
        return lane.cell_at(offset,slot.slot.ordinal,slot.slot.name)

    def materialize(self,index):
        from .pre553_source_backed_c11_facade import _cell_key,_event,RESPONSE_OWNER_FAMILY
        reader=self.reader
        self.check_live()
        if index<0:
            index+=len(self)
        if not 0<=index<len(self):
            raise IndexError(index)
        expected=self._event_ref(self.hashes[32*index:32*(index+1)])
        def reconstruct(row,slot,cell,value,occ,respondent):
            owner=self.owners.get(slot.slot.key)
            auths=owner.authority_refs_for(RESPONSE_OWNER_FAMILY) if owner else ()
            return _event(reader.receipt.source_sha256,row,respondent,slot,cell,value,occ,self.projection,auths)
        if self.direct:
            # Direct addresses are acceleration only. The selected bytes and
            # the fully reconstructed semantic object's exact sealed ref
            # remain mandatory. No mutable locator can authorize another body.
            try:
                row=self.row_ordinals[self.respondent_codes[index]]
                slot,position=self.slot_occurrences[self.question_codes[index]]
                cell=self._cell(row,slot)
                value=self.value_rules[slot.slot.ordinal][_cell_key(cell)]
                occ=value.occurrences[position]
                event=reconstruct(row,slot,cell,value,occ,self.row_respondents[row])
            except (IndexError,KeyError) as exc:
                raise CountryCarrierError("country event physical locator differs from sealed rule") from exc
            if event.ref!=expected:
                raise CountryCarrierError("country event reconstruction differs from sealed ref")
        else:
            code=self.respondent_codes[index]
            respondent=self.respondents[self.respondent_keys[code]]
            question=self.question_keys[self.question_codes[index]]
            matches=[]
            for row in self.source_rows[code]:
                for slot in self.slots[question]:
                    cell=self._cell(row,slot)
                    physical=_cell_key(cell)
                    rules=[r for r in slot.values if r.physical_key==physical]
                    if len(rules)!=1:
                        raise CountryCarrierError("country event physical value lacks exact governed rule")
                    value=rules[0]
                    for occ in value.occurrences:
                        candidate=reconstruct(row,slot,cell,value,occ,respondent)
                        if candidate.ref==expected:
                            matches.append(candidate)
            if len(matches)!=1:
                raise CountryCarrierError("country event reconstruction differs from sealed ref")
            event=matches[0]
        reader._check_live_file()
        return event

    def __getitem__(self,index):
        from .pre553_empirical_objects import canonical_json as semantic_json
        return _BodyScalar(semantic_json(self.materialize(index).semantic_projection()).encode("utf-8"))


def country_census(incidence, *, country_variable, require_current):
    """Exact native typed country-code inventory; missing codes explicitly separate.

    Returns R5 typed keys, not inferred country names or semantic authority.
    Unknown/missing rows are reported, never silently assigned to a country.
    """
    if type(incidence) is not PhysicalSourceIncidence or country_variable not in {v.name for v in incidence.variables}:
        raise CountryCarrierError("explicit native country variable required")
    _live(require_current)
    observed, held, last = {}, {}, 0
    for cell in incidence.iter_native_column(country_variable):
        if cell.variable_name!=country_variable or cell.row_ordinal!=last+1:
            raise CountryCarrierError("country census row discontinuity")
        last=cell.row_ordinal
        if cell.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE:
            bucket,key=observed,canonical_json(_CODEC.encode(cell.raw_value))
        else:
            bucket,key=held,cell.missing_state.value
        bucket[key]=bucket.get(key,0)+1
    if last!=incidence.row_count:
        raise CountryCarrierError("country census incomplete")
    incidence.verify_source_identity()
    _live(require_current)
    return {"source_sha256":incidence.source_sha256,"source_rows":last,
            "country_variable":country_variable,"observed":observed,"held":held}


@dataclass(frozen=True)
class CountryExecution:
    result: object
    release_identity: object

class CountryWorkloadSession:
    """Bounded live country reuse for separately issued TEST_ONLY workloads.

    The existing I02 facade and repository remain the only producers. One
    repository is retained, on the private reader that actually certified it.
    No detached release, cached permission or cached answer. Optional R14
    preparation retains only producer-qualified response headers, requiring
    independent external pin custody and full fresh sourcefree admission.
    A new workload must be independently admitted, reauthenticate the full
    country file, and match the full producer key before reusing preparation.
    Single-threaded, explicit context lifetime; failed execution closes it.
    """
    def __init__(self,path,receipt,*,require_current,preparation_path=None,
                 preparation_pin=None,reuse_query_preparation=False,
                 omit_preparation_group_plane=False):
        if type(reuse_query_preparation) is not bool:
            raise CountryCarrierError("explicit query preparation reuse selection required")
        self._reuse_query_preparation=reuse_query_preparation
        self._query_scope=None
        if type(receipt) is not CountryReceipt or not callable(require_current):
            raise CountryCarrierError("exact country receipt and current callback required")
        self._path=Path(path).resolve()
        self._receipt=receipt
        # All receipt fields are exact immutable primitive values. Keep a
        # detached tuple rather than serializing it on every event read.
        from dataclasses import fields
        self._receipt_fields=tuple(f.name for f in fields(receipt))
        self._receipt_pin=self._receipt_material(receipt)
        self._require_current=require_current
        from ._pre553_country_preparation import _CountryPreparation
        if preparation_path is None and preparation_pin is not None:
            raise CountryCarrierError("preparation path required with external pin")
        self._preparation=(None if preparation_path is None else
                           _CountryPreparation(preparation_path,preparation_pin,omit_groups=omit_preparation_group_plane))
        self._published_preparation_pin=None
        self._reader=None
        self._entry=None
        self._active=None
        self._entered=False
        self._closed=False
        self._busy=False
        self._owner=None

    @property
    def preparation_pin(self):
        """External custody pin; retain separately only after successful execution."""
        return self._published_preparation_pin

    def _receipt_material(self,receipt):
        return tuple(getattr(receipt,name) for name in self._receipt_fields)

    def __enter__(self):
        if self._entered or self._closed:
            raise CountryCarrierError("country workload session cannot be reentered")
        from threading import get_ident
        self._owner=get_ident()
        self._entered=True
        return self

    def close(self):
        from threading import get_ident
        if self._owner is not None and self._owner!=get_ident():
            raise CountryCarrierError("country workload session owner thread required")
        self._closed=True
        self._discard_query_scope()
        self._entry=None
        if self._reader is not None:
            self._reader.close()
            self._reader=None

    def __exit__(self,*args):
        self.close()

    def _require_owner(self):
        from threading import get_ident
        if not self._entered or self._closed or self._owner!=get_ident():
            raise CountryCarrierError("country workload session not open on owner thread")

    def _check_custody(self):
        self._require_owner()
        _live(self._require_current)
        self._require_owner()
        if self._receipt_material(self._receipt)!=self._receipt_pin:
            raise CountryCarrierError("country workload session receipt changed")

    def _current(self):
        self._require_owner()
        if self._active is None:
            raise CountryCarrierError("country workload session has no active issued decision")
        # Active execution callback already checks country custody and its
        # independently current issuer. Do not call the custody owner twice.
        self._active()
        self._require_owner()

    def _bind(self,path,receipt,scope,current):
        from contextlib import contextmanager
        @contextmanager
        def binding():
            self._check_custody()
            if self._active is not None:
                raise CountryCarrierError("country workload session already active")
            if (scope is None or scope.record.scope!="TEST_ONLY_SOURCEFREE"
                    or Path(path).resolve()!=self._path
                    or type(receipt) is not CountryReceipt
                    or self._receipt_material(receipt)!=self._receipt_pin):
                raise CountryCarrierError("country workload session binding mismatch")
            self._active=current
            try:
                self._current()
                if self._reader is None:
                    self._reader=CountryReader(self._path,self._receipt,require_current=self._current)
                else:
                    # Do not mistake stat identity for exact custody. The
                    # entire artifact is authenticated at every new workload.
                    self._reader.verify_full()
                yield self._reader
                self._current()
            except BaseException:
                self.close()
                raise
            finally:
                self._active=None
        return binding()

    def _discard_query_scope(self):
        if self._query_scope is not None:
            self._query_scope.close()
            self._query_scope=None

    def _query_scope_for(self,repository):
        # Existing grouping and condition owner, scoped to this exact live
        # certified repository. Each separate workload is still admitted.
        self._current()
        if not self._reuse_query_preparation:
            return None
        if self._entry is None or self._entry[3] is not repository:
            raise CountryCarrierError("query preparation repository drift")
        if self._query_scope is None:
            from .pre553_empirical_query import I03GroupedExecutionScope
            self._query_scope=I03GroupedExecutionScope(rolling_groups=True)
        return self._query_scope

    def _repository(self,source,projection,authorities):
        from .pre553_source_backed_c11_facade import (
            build_source_backed_c11_repository,source_backed_facade_key,_CountryProjectionPin)
        self._current()
        if type(source) is not _CountryPhysicalStream or source.reader is not self._reader:
            raise CountryCarrierError("country session source reader mismatch")
        source._verify_binding()
        authorities=tuple(authorities)
        if self._entry is not None:
            pin=getattr(self._reader,"_certified_projection_pin",None)
            if type(pin) is _CountryProjectionPin and pin.matches(projection,authorities):
                key=pin.key(source,projection,authorities)
            else:
                key=source_backed_facade_key(source,projection,current_authorities=authorities)
            old_key,old_projection,old_authorities,repo,release,identity,identity_pin=self._entry
            # Strict object ownership avoids reusing a body resolver bound
            # to a different (even equal) projection or authority instance.
            if (key==old_key and projection is old_projection
                    and len(authorities)==len(old_authorities)
                    and all(a is b for a,b in zip(authorities,old_authorities))):
                if (canonical_json(identity.as_dict())!=identity_pin
                        or self._reader._certified_identity!=identity
                        or self._reader._certified_facade_key!=old_key
                        or repo.resolve_release_exact(identity.release_ref) is not release
                        or release.replay_manifest.ref!=identity.replay_ref
                        or release.source_release_manifest_hash!=identity.source_release_manifest_hash
                        or release.semantic_release_hash!=identity.semantic_release_hash):
                    raise CountryCarrierError("country prepared repository identity drift")
                self._current()
                return repo,release
            # Do not keep the old graph alive in destructured local variables
            # across a miss while building its replacement.
            del repo,release,old_projection,old_authorities,identity
        # Release the old prepared graph and query derivatives before
        # constructing another one. Neither crosses a release replacement.
        self._discard_query_scope()
        self._entry=None
        if self._preparation is None:
            repo,release=build_source_backed_c11_repository(source,projection,
                                        current_authorities=authorities)
        else:
            # Private, independently admitted TEST_ONLY session only.
            from .pre553_source_backed_c11_facade import _build_source_backed_c11_repository
            repo,release=_build_source_backed_c11_repository(source,projection,
                current_authorities=authorities,_country_preparation=self._preparation)
        # Facade already computed and rechecked the complete producer key.
        # Do not repeat its projection hashing on this cold admission.
        key=self._reader._certified_facade_key
        identity=self._reader._certified_identity
        if identity is None or key is None:
            raise CountryCarrierError("country prepared release not certified")
        self._entry=(key,projection,authorities,repo,release,identity,
                     canonical_json(identity.as_dict()))
        self._current()
        return repo,release

    def execute(self,workload,resolver,*,host,purpose):
        from .pre553_issued_workload import _CountryAdmissionScope
        self._require_owner()
        if self._busy:
            raise CountryCarrierError("country workload session already active")
        self._busy=True
        try:
            self._check_custody()
            scope=_CountryAdmissionScope(workload,resolver,host=host,purpose=purpose,allow_test_only=True)
            result=_execute_country_workload(workload,resolver,country_path=self._path,
                country_receipt=self._receipt,host=host,purpose=purpose,
                require_country_current=self._check_custody,allow_test_only=True,
                _country_scope=scope,_session=self)
            self._published_preparation_pin=(None if self._preparation is None else self._preparation.pin)
            return result
        except BaseException:
            self.close()
            raise
        finally:
            self._busy=False

    def publish(self,workload,resolver,*,host,purpose,root_dir,**options):
        from .pre553_saved_durable_delivery import execute_publish_country
        self._require_owner()
        if self._busy:
            raise CountryCarrierError("country workload session already active")
        self._busy=True
        try:
            self._check_custody()
            result=execute_publish_country(workload,resolver,host=host,purpose=purpose,
                country_path=self._path,country_receipt=self._receipt,root_dir=root_dir,
                _country_session=self,**options)
            self._published_preparation_pin=(None if self._preparation is None else self._preparation.pin)
            return result
        except BaseException:
            self.close()
            raise
        finally:
            self._busy=False


def execute_country_workload(workload,resolver,*,country_path,country_receipt,host,purpose,
                             require_country_current,allow_test_only=False,expected_wave=None):
    """Public country entry: own the admission scope, never take one from a caller."""
    from .pre553_issued_workload import _CountryAdmissionScope
    scope=(_CountryAdmissionScope(workload,resolver,host=host,purpose=purpose,
                                  allow_test_only=allow_test_only,expected_wave=expected_wave)
           if allow_test_only else None)
    return _execute_country_workload(workload,resolver,country_path=country_path,
        country_receipt=country_receipt,host=host,purpose=purpose,
        require_country_current=require_country_current,allow_test_only=allow_test_only,
        expected_wave=expected_wave,_country_scope=scope)


def _execute_country_workload(workload,resolver,*,country_path,country_receipt,host,purpose,
                             require_country_current,allow_test_only=False,expected_wave=None,_country_scope=None,
                             _max_units=None,_prior_product=None,_checkpoint_every=None,
                             _checkpoint_observer=None,_session=None,_final_observer=None):
    """Execute an already issued workload from one retained numeric country.

    The separate country custody/currentness callback is mandatory; it is not
    replaced by U43's source/science decision. Original execution may proceed
    only through the incumbent independent resolver and actual country grant.
    This function does not publish original empirical outputs to S2-F.
    """
    from .pre553_issued_workload import admit,execute_issued_workload,_execute_issued_workload
    record=(_country_scope.check() if _country_scope is not None else
            admit(workload,resolver,host=host,purpose=purpose,
                  allow_test_only=allow_test_only,expected_wave=expected_wave))
    if type(country_receipt) is not CountryReceipt or record.source_sha256!=country_receipt.source_sha256:
        raise CountryCarrierError("issued source and external country receipt differ")
    bounded=_max_units is not None
    if bounded and (type(_max_units) is not int or _max_units<1):
        raise CountryCarrierError("positive exact country max_units required")
    if (_checkpoint_every is None)!=(_checkpoint_observer is None):
        raise CountryCarrierError("country checkpoint interval and observer required together")
    if _checkpoint_every is not None and (type(_checkpoint_every) is not int
            or _checkpoint_every<1 or not callable(_checkpoint_observer)):
        raise CountryCarrierError("exact country checkpoint observer required")
    if _final_observer is not None and not callable(_final_observer):
        raise CountryCarrierError("exact final country observer required")
    if (bounded or _prior_product is not None or _checkpoint_observer is not None
            or _final_observer is not None):
        if _country_scope is None or record.scope!="TEST_ONLY_SOURCEFREE":
            raise CountryCarrierError("country continuation requires private sourcefree delivery scope")
    prior_receipts=()
    prior_outputs=None
    expected_identity=None
    if _prior_product is not None:
        from .pre553_saved_durable_delivery import ColdSavedProduct
        if type(_prior_product) is not ColdSavedProduct or _prior_product.complete:
            raise CountryCarrierError("exact incomplete country product required")
        _prior_product._live()
        prior_receipts=_prior_product._receipts
        prior_outputs=_prior_product._outputs
        expected_identity,=_prior_product._closure.release_identities
    def current():
        _live(require_country_current)
        # Full immutable workload admission occurs before opening, inside
        # the incumbent U43 executor, and again after execution. Frequent
        # physical reads compare the independently returned exact decision,
        # rather than reserializing the entire projection per event.
        if _country_scope is not None:
            _country_scope.current_only()
        elif resolver.resolve_current(workload.decision_ref)!=record:
            raise CountryCarrierError("country workload decision changed")
    current()
    count=len(workload.requests)+len(workload.discoveries)
    if count<1:
        raise CountryCarrierError("empty country workload")
    if _session is not None and type(_session) is not CountryWorkloadSession:
        raise CountryCarrierError("exact live country workload session required")
    binding=(CountryReader(country_path,country_receipt,require_current=current)
             if _session is None else _session._bind(country_path,country_receipt,_country_scope,current))
    with binding as reader:
        def checkpoint(result):
            reader._verify()
            current()
            identity=reader._certified_identity
            if identity is None:
                raise CountryCarrierError("country checkpoint lacks certified release")
            _checkpoint_observer(CountryExecution(result,identity),reader)
            reader._verify()
            current()
        def factory(ref):
            current()
            if ref!=workload.source_factory_ref:
                raise CountryCarrierError("country source factory identity mismatch")
            return reader._native_stream(workload.projection)
        # The original bounded path runs the declared units once, avoiding
        # the historical preliminary Route B/discovery pass. Require all units.
        if _country_scope is None:
            result=execute_issued_workload(workload,resolver,source_factory=factory,
                host=host,purpose=purpose,allow_test_only=allow_test_only,
                expected_wave=expected_wave,max_units=count)
        else:
            result=_execute_issued_workload(workload,resolver,source_factory=factory,
                host=host,purpose=purpose,allow_test_only=allow_test_only,
                expected_wave=expected_wave,max_units=_max_units if bounded else count,
                _country_scope=_country_scope,prior_receipts=prior_receipts,
                prior_outputs=prior_outputs,_expected_country_identity=expected_identity,
                checkpoint_every=_checkpoint_every,
                checkpoint_observer=checkpoint if _checkpoint_observer is not None else None,
                _country_session=_session)
        identity=reader._certified_identity
        if identity is None or (not bounded and not result.summary.full_coverage):
            # Retain typed failure codes without disclosing respondent data.
            codes=tuple((r.state,r.failure_code) for r in result.receipts if r.state!="COMPLETED")
            raise CountryCarrierError("country native workload not fully executed: "+repr(codes))
        # Ordinary execution keeps its post-proof full admission. Delivery's
        # synchronous observer owns the one final proof AFTER this carrier's
        # external admission callbacks, not a census made before those calls.
        if _final_observer is None:
            result.exact_s2e_output_census(require_complete=not bounded,
                                          runtime_catalog=workload.catalog)
        reader._verify()
        current()
        if (_country_scope.check() if _country_scope is not None else
                admit(workload,resolver,host=host,purpose=purpose,
                      allow_test_only=allow_test_only,expected_wave=expected_wave))!=record:
            raise CountryCarrierError("country workload decision changed before serving")
        executed=CountryExecution(result,identity)
        if _final_observer is not None:
            _final_observer(executed,reader)
            reader._verify()
            current()
        return executed

def build_country_set(incidence,*,country_variable,root,require_current,
                      country_keys=None,retained_receipts=(),block_rows=1024,
                      max_open_countries=4,pending_bytes=64*1024*1024,
                      min_free_bytes=64*1024*1024,on_progress=None):
    """Resumable independent countries; amortize scans over bounded groups.

    Retain only externally receipted completed countries. Missing country
    rows are reported in the census; no silent assignment. Each completed
    file/receipt is yielded independently. Unreceipted final files are
    refused, not adopted or overwritten. max_open_countries=1 retains
    strictly sequential source scans for constrained hosts.
    """
    if type(max_open_countries) is not int or not 1<=max_open_countries<=64:
        raise CountryCarrierError("max_open_countries must be in 1..64")
    if on_progress is not None and not callable(on_progress):
        raise CountryCarrierError("progress callback must be callable")
    _build_limits(incidence,country_variable,block_rows,pending_bytes,min_free_bytes)
    inventory=country_census(incidence,country_variable=country_variable,
                             require_current=require_current)
    keys=tuple(sorted(inventory["observed"])) if country_keys is None else tuple(country_keys)
    if len(set(keys))!=len(keys) or any(k not in inventory["observed"] for k in keys):
        raise CountryCarrierError("country selection must use distinct exact observed codes")
    retained={}
    for receipt in retained_receipts:
        if (type(receipt) is not CountryReceipt or receipt.country_key in retained
            or receipt.source_sha256!=inventory["source_sha256"]
            or receipt.country_variable!=country_variable
            or receipt.metadata_digest!=incidence.physical_metadata_digest
            or receipt.country_rows!=inventory["observed"].get(receipt.country_key)):
            raise CountryCarrierError("retained country receipt mismatch")
        retained[receipt.country_key]=receipt
    root=Path(root).resolve()
    if not root.is_dir():
        raise CountryCarrierError("existing private country root required")
    def progress(**state):
        if on_progress is not None:
            on_progress(state)
    def path_for(key):
        return root/("country-"+sha256(key.encode("ascii")).hexdigest()+".sqlite")
    # Retain requested ordering, but coalesce contiguous not-yet-built codes.
    # Bounded per-country estimates, not a hard process RSS guarantee.
    width=len(incidence.variables)
    group_limit=max(1,min(max_open_countries,pending_bytes//max(1,1024*width)))
    progress(phase="CENSUS",source_rows=inventory["source_rows"],
             selected_countries=len(keys),held_rows=sum(inventory["held"].values()),
             max_open_countries=group_limit)
    offset=0
    while offset<len(keys):
        key=keys[offset]
        _live(require_current)
        if key in retained:
            receipt=retained[key];path=path_for(key)
            with CountryReader(path,receipt,require_current=require_current) as reader:
                if sum(1 for _ in reader.row_ordinals())!=receipt.country_rows:
                    raise CountryCarrierError("retained country census mismatch")
            progress(phase="REUSED",country_key=key,rows=receipt.country_rows,bytes=receipt.bytes)
            yield path,receipt
            offset+=1
            continue
        batch=[]
        while offset<len(keys) and keys[offset] not in retained and len(batch)<group_limit:
            batch.append(keys[offset]);offset+=1
        writers={}
        try:
            budget=pending_bytes//len(batch)
            for item in batch:
                writers[item]=_CountryWriter(incidence,country_variable,item,path_for(item),
                    require_current,block_rows,budget,min_free_bytes)
            progress(phase="SOURCE_SCAN",countries=len(batch))
            _feed_writers(incidence,country_variable,writers,require_current)
            # No country is published before the bounded source scan has
            # completed and all selected row counts are known exact.
            if any(w.count!=inventory["observed"][k] for k,w in writers.items()):
                raise CountryCarrierError("country group census mismatch")
            for item,w in writers.items():
                receipt=w.finish(inventory["observed"][item])
                w.abort()
                progress(phase="BUILT",country_key=item,rows=receipt.country_rows,bytes=receipt.bytes)
                yield path_for(item),receipt
        finally:
            for w in writers.values():
                w.abort()


def country_workspace_status(root,*,retained_receipts=()):
    """Non-mutating operator inventory. Never turn a local hash into authority."""
    root=Path(root).resolve()
    if not root.is_dir():
        raise CountryCarrierError("existing country root required")
    pinned={}
    for receipt in retained_receipts:
        if type(receipt) is not CountryReceipt:
            raise CountryCarrierError("external receipt required")
        name="country-"+sha256(receipt.country_key.encode("ascii")).hexdigest()+".sqlite"
        if name in pinned:
            raise CountryCarrierError("duplicate external country receipt")
        pinned[name]=receipt
    files={p.name:p for p in root.glob("country-*.sqlite")}
    return {"pinned_present":sorted(set(files)&set(pinned)),
            "missing_pinned":sorted(set(pinned)-set(files)),
            "unreceipted_final":sorted(set(files)-set(pinned)),
            "uncommitted_stage":[p.name for p in sorted(root.glob(".country-*"))],
            "free_bytes":shutil.disk_usage(root).free,
            "note":"Inventory only. Reopen with external receipts and live permission; "
                   "unreceipted files require owner disposition, not automatic adoption/deletion."}
