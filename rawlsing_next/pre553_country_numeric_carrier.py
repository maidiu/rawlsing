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
from .pre553_source_backed_c11_facade import ExactPhysicalCellStream

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
        row_id = None
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
        for cell in incidence.iter_country_cells(country_variable,country_value):
            if type(cell) is not PhysicalCell:
                raise CountryCarrierError("foreign physical cell")
            if cell.row_ordinal != row_id:
                if row_id is not None:
                    if cell.row_ordinal<=row_id or not cells:
                        raise CountryCarrierError("selected source rows out of order")
                    accept_row()
                    cells.clear()
                if not 1<=cell.row_ordinal<=incidence.row_count:
                    raise CountryCarrierError("selected source row outside original census")
                row_id=cell.row_ordinal
            cells.append(cell)
            if len(cells) > len(variables):
                raise CountryCarrierError("duplicate source row slot")
        if cells:
            accept_row()
        # The incumbent selected decoder itself verifies complete source scan.
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
        self._closed = False
        self._certified_identity = None
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
        if not self._closed:
            self._closed = True
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
        return _CountryPhysicalStream(self.receipt.source_sha256,self.receipt.country_rows,
                 self.iter_cells,transport_identity="COUNTRY_NUMERIC_PHYSICAL@1:"+self.receipt.sha256,
                 decoder_metadata_digest=self.receipt.metadata_digest,reader=self)
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

@dataclass(frozen=True)
class _CountryPhysicalStream(ExactPhysicalCellStream):
    """Recognized only by the incumbent facade; no generic user-supplied body factory."""
    reader: CountryReader | None = None

    def event_bodies(self, release, events, projection):
        if type(self.reader) is not CountryReader or self.reader._closed:
            raise CountryCarrierError("country body resolver requires its live reader")
        self.reader._verify()
        if self.transport_identity != "COUNTRY_NUMERIC_PHYSICAL@1:"+self.reader.receipt.sha256:
            raise CountryCarrierError("country transport pin mismatch")
        from .pre553_durable_empirical_closure import ReleaseIdentity
        self.reader._certified_identity = ReleaseIdentity(
            release.release_ref,release.replay_manifest.ref,release.source_artifact_ref,
            release.source_release_manifest_hash,release.semantic_release_hash)
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
    __slots__=("reader","projection","rows","slots","owners","respondents","locators","cache")
    def __init__(self,reader,projection,events):
        from .pre553_empirical_objects import exact_ref
        self.reader,self.projection=reader,projection
        self.rows={row:(block,rows,i) for block,rows in reader._blocks() for i,row in enumerate(rows)}
        self.respondents={r.ref.key:r for r in projection.respondents}
        by_respondent={}
        for b in projection.row_bindings:
            by_respondent.setdefault(b.respondent_ref.key,[]).append(b.row_ordinal)
        self.slots={}
        for slot in projection.response_slots:
            self.slots.setdefault(slot.question_binding.ref.key,[]).append(slot)
        self.owners={x.slot.key:x for x in projection.slot_owner_sets}
        locators=[]
        for event in events:
            respondent=exact_ref(event.scoped_respondent_ref).key
            bindings=[r.key for r in event.dependency_refs if r.key in self.slots]
            if respondent not in by_respondent or len(bindings)!=1:
                raise CountryCarrierError("sealed event lacks original country row/slot binding")
            locators.append((tuple(by_respondent[respondent]),respondent,bindings[0],event.ref))
        self.locators=tuple(locators)
        self.cache=OrderedDict()

    def __len__(self):
        return len(self.locators)

    def __getitem__(self,index):
        from .pre553_source_backed_c11_facade import _cell_key,_event,RESPONSE_OWNER_FAMILY
        reader=self.reader
        if reader._closed:
            raise CountryCarrierError("country event resolver closed")
        _live(reader.require_current)
        source_rows,respondent,question,expected=self.locators[index]
        matches=[]
        for row in source_rows:
            block,rows,offset=self.rows[row]
            for slot in self.slots[question]:
                key=(block,slot.slot.ordinal)
                lane=self.cache.get(key)
                if lane is None:
                    lane=reader._column(block,rows,slot.slot.ordinal)
                    self.cache[key]=lane
                    if len(self.cache)>32:
                        self.cache.popitem(last=False)
                else:
                    self.cache.move_to_end(key)
                cell=_decode_cell(row,slot.slot.ordinal,slot.slot.name,lane.dictionary[lane.codes[offset]])
                physical=_cell_key(cell)
                rules=[r for r in slot.values if r.physical_key==physical]
                if len(rules)!=1:
                    raise CountryCarrierError("country event physical value lacks exact governed rule")
                owner=self.owners.get(slot.slot.key)
                auths=owner.authority_refs_for(RESPONSE_OWNER_FAMILY) if owner else ()
                value=rules[0]
                for occ in value.occurrences:
                    event=_event(reader.receipt.source_sha256,row,self.respondents[respondent],
                                 slot,cell,value,occ,self.projection,auths)
                    if event.ref==expected:
                        matches.append(event)
        if len(matches)!=1:
            raise CountryCarrierError("country event reconstruction differs from sealed ref")
        _live(reader.require_current)
        from .pre553_empirical_objects import canonical_json as semantic_json
        return _BodyScalar(semantic_json(matches[0].semantic_projection()).encode("utf-8"))

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

def execute_country_workload(workload,resolver,*,country_path,country_receipt,host,purpose,
                             require_country_current,allow_test_only=False,expected_wave=None):
    """Execute an already issued workload from one retained numeric country.

    The separate country custody/currentness callback is mandatory; it is not
    replaced by U43's source/science decision. Original execution may proceed
    only through the incumbent independent resolver and actual country grant.
    This function does not publish original empirical outputs to S2-F.
    """
    from .pre553_issued_workload import admit,execute_issued_workload
    record=admit(workload,resolver,host=host,purpose=purpose,
                 allow_test_only=allow_test_only,expected_wave=expected_wave)
    if type(country_receipt) is not CountryReceipt or record.source_sha256!=country_receipt.source_sha256:
        raise CountryCarrierError("issued source and external country receipt differ")
    def current():
        _live(require_country_current)
        if admit(workload,resolver,host=host,purpose=purpose,
                 allow_test_only=allow_test_only,expected_wave=expected_wave)!=record:
            raise CountryCarrierError("country workload decision changed")
    current()
    count=len(workload.requests)+len(workload.discoveries)
    if count<1:
        raise CountryCarrierError("empty country workload")
    with CountryReader(country_path,country_receipt,require_current=current) as reader:
        def factory(ref):
            current()
            if ref!=workload.source_factory_ref:
                raise CountryCarrierError("country source factory identity mismatch")
            return reader._native_stream(workload.projection)
        # The original bounded path runs the declared units once, avoiding
        # the historical preliminary Route B/discovery pass. Require all units.
        result=execute_issued_workload(workload,resolver,source_factory=factory,
            host=host,purpose=purpose,allow_test_only=allow_test_only,
            expected_wave=expected_wave,max_units=count)
        identity=reader._certified_identity
        if identity is None or not result.summary.full_coverage:
            raise CountryCarrierError("country native workload not fully executed")
        result.exact_s2e_output_census(require_complete=True,runtime_catalog=workload.catalog)
        reader._verify()
        current()
        return CountryExecution(result,identity)

def build_country_set(incidence,*,country_variable,root,require_current,
                      country_keys=None,retained_receipts=(),block_rows=1024):
    """Sequential, resumable country construction; no full-wave expanded estate.

    country_keys are exact R5 strings from country_census, or None for every
    observed code. Only externally supplied receipts may authorize reuse.
    Missing/unknown country rows are explicitly reported in the census.
    Yields (path,receipt) after each completed country so an operator can bank
    the independent receipt before proceeding. A failure leaves earlier
    completed countries intact.
    """
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
    for key in keys:
        _live(require_current)
        path=root/("country-"+sha256(key.encode("ascii")).hexdigest()+".sqlite")
        if key in retained:
            receipt=retained[key]
            with CountryReader(path,receipt,require_current=require_current) as reader:
                if len(tuple(reader.row_ordinals()))!=receipt.country_rows:
                    raise CountryCarrierError("retained country census mismatch")
        else:
            receipt=build_country(incidence,country_variable=country_variable,
                country_value=_CODEC.decode(json.loads(key)),output=path,
                require_current=require_current,block_rows=block_rows)
            if receipt.country_rows!=inventory["observed"][key]:
                raise CountryCarrierError("country build census mismatch")
        yield path,receipt
