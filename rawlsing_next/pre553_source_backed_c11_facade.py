"""Explicit governed physical/native -> validated C11 -> frozen I03 facade.

Physical carriers remain nonsemantic. Every semantic projection decision is an
exact caller-owned input; the module never reads labels/frequencies to infer
meaning and never bypasses C11 validation.
"""
from __future__ import annotations

from dataclasses import dataclass, replace, fields, is_dataclass
from fractions import Fraction
from types import MappingProxyType
from threading import RLock
import hashlib
import math
import json
import struct
from array import array
from bisect import bisect_right
from functools import lru_cache
from collections.abc import Sequence
from typing import Any, Callable, Iterable, Mapping

from rawlsing_next._pre553_c11_execution_view import _compact_public_objects
from rawlsing_next.pre553_c11_ingest import (
    INGEST_CONTRACT_VERSION, C11SourceReleaseCandidate, SourceReleaseManifest,
    build_candidate_replay_manifest, validate_c11_source_release, _validate_country_produced_release,
)
from rawlsing_next.pre553_c11_integrity import (
    C11InternalRecord, QuestionVariableBinding, RespondentIdentity, TypedAbsence,
)
from rawlsing_next.pre553_c11_repository import C11LogicalRelease, C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, AuthoritySnapshot, CanonicalSemanticObject, EmpiricalCoordinateFact, EmpiricalPredicate,
    EmpiricalQuerySpec, EmpiricalUniverse, ExactRef, RespondentEvent,
    RoutingEligibilityFact, SourceUniverseRelation, WeightMeasureFact,
    authority_ref, canonicalize, canonical_json, exact_ref, semantic_hash,
)
from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_physical_c11_bridge import (
    PhysicalSourceAuthorityProjection, build_validated_c11_release,
)
from rawlsing_next.pre553_physical_decoder import (
    DecoderError, PhysicalCell, PhysicalMissingState, PhysicalSourceIncidence,
)
from rawlsing_next.pre553_r5_codec import (
    CODEC_VERSION as R5_CODEC_VERSION,
    R5TypedValueCodec,
    canonical_bytes as r5_canonical_bytes,
)

CONTRACT_ID = "PRE553_SOURCE_BACKED_C11_FACADE@1.0.0"
SLOT_OWNER_SET_CONTRACT_ID = "PRE553_C11_PHYSICAL_SLOT_OWNER_SET@1.0.0"
RESPONSE_OWNER_FAMILY = "RespondentEvent@1.0.0"
COORDINATE_OWNER_FAMILY = "EmpiricalCoordinateFact@1.0.0"
WEIGHT_OWNER_FAMILY = "WeightMeasureFact@1.0.0"
_SUPPORTED_OWNER_FAMILIES = frozenset((RESPONSE_OWNER_FAMILY, COORDINATE_OWNER_FAMILY, WEIGHT_OWNER_FAMILY))

PHYSICAL_VALUE_MATERIAL_SCHEMA = "PRE553_EXACT_PHYSICAL_VALUE_MATERIAL@1.0.0"
PHYSICAL_BINDING_SCHEMA = "PRE553_PHYSICAL_VALUE_BINDING@2.0.0"
RAW_WITNESS_SCHEMA = "PRE553_RAW_PHYSICAL_VALUE_WITNESS@1.0.0"
_PHYSICAL_CODEC = R5TypedValueCodec()


class SourceBackedC11FacadeError(ValueError):
    pass


def _sha(value: str, name: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or value.lower() != value or any(c not in "0123456789abcdef" for c in value):
        raise SourceBackedC11FacadeError(f"{name} must be lowercase sha256")
    return value


def _dref(kind: str, ns: str, material: Any) -> ExactRef:
    h = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:pre553:c05r2a:{ns}:sha256:{h}", h)


def _auths(values: Iterable[AuthorityRef]) -> tuple[AuthorityRef, ...]:
    return tuple(sorted(set(values), key=lambda x: x.key))


def _refs(values: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    return tuple(sorted(set(values), key=lambda x: x.key))


def _opt_ref(value: Any, name: str) -> ExactRef | None:
    return None if value is None or isinstance(value, TypedAbsence) else exact_ref(value, name)


def exact_physical_value_material(value: Any) -> dict[str, Any]:
    """Return exact candidate-neutral physical material, never semantic material."""
    return {
        "schema": PHYSICAL_VALUE_MATERIAL_SCHEMA,
        "codec": R5_CODEC_VERSION,
        "token": _PHYSICAL_CODEC.encode(value),
    }


def raw_physical_value_witness(value: Any) -> dict[str, Any]:
    """Carry an observed physical value as an opaque C11 witness."""
    return {"$raw_physical_value": exact_physical_value_material(value)}


def physical_value_binding_key(raw_value: Any, missing_state: PhysicalMissingState | str,
                               declaration: Mapping[str, Any] | None = None) -> str:
    state = missing_state.value if isinstance(missing_state, PhysicalMissingState) else missing_state
    if state not in {x.value for x in PhysicalMissingState}:
        raise SourceBackedC11FacadeError("unknown physical missing state")
    material = {
        "schema": PHYSICAL_BINDING_SCHEMA,
        "codec": R5_CODEC_VERSION,
        "raw_value": _PHYSICAL_CODEC.encode(raw_value),
        "physical_state": state,
        "source_missing_declaration": _PHYSICAL_CODEC.encode(declaration),
    }
    return hashlib.sha256(r5_canonical_bytes(material)).hexdigest()


def _cell_key(cell: PhysicalCell) -> str:
    return physical_value_binding_key(cell.raw_value, cell.missing_state, cell.source_missing_declaration)


@dataclass(frozen=True, order=True)
class PhysicalSlot:
    ordinal: int
    name: str

    def __post_init__(self):
        if not isinstance(self.ordinal, int) or isinstance(self.ordinal, bool) or self.ordinal < 1 or not isinstance(self.name, str) or not self.name:
            raise SourceBackedC11FacadeError("invalid exact physical slot")

    @property
    def key(self):
        return (self.ordinal, self.name)


@dataclass(frozen=True)
class PhysicalSlotOwnerAuthorization:
    owner_family: str
    authority_refs: tuple[AuthorityRef, ...]

    def __post_init__(self):
        if self.owner_family not in _SUPPORTED_OWNER_FAMILIES:
            raise SourceBackedC11FacadeError("unsupported physical-slot semantic owner family")
        normalized = _auths(authority_ref(x, "physical-slot owner authority") for x in self.authority_refs)
        if not normalized:
            raise SourceBackedC11FacadeError("physical-slot semantic owner lacks explicit authority")
        if len(normalized) != len(self.authority_refs):
            raise SourceBackedC11FacadeError("duplicate physical-slot owner authority")
        object.__setattr__(self, "authority_refs", normalized)


@dataclass(frozen=True)
class PhysicalSlotOwnerSet:
    slot: PhysicalSlot
    owners: tuple[PhysicalSlotOwnerAuthorization, ...]
    contract_id: str = SLOT_OWNER_SET_CONTRACT_ID

    def __post_init__(self):
        if self.contract_id != SLOT_OWNER_SET_CONTRACT_ID:
            raise SourceBackedC11FacadeError("unsupported physical-slot owner-set contract")
        if not self.owners:
            raise SourceBackedC11FacadeError("physical-slot owner set cannot be empty")
        families = tuple(x.owner_family for x in self.owners)
        if len(families) != len(set(families)):
            raise SourceBackedC11FacadeError("conflicting duplicate physical-slot semantic owners")
        object.__setattr__(self, "owners", tuple(sorted(self.owners, key=lambda x: x.owner_family)))

    @property
    def owner_families(self) -> tuple[str, ...]:
        return tuple(x.owner_family for x in self.owners)

    def authority_refs_for(self, owner_family: str) -> tuple[AuthorityRef, ...]:
        for owner in self.owners:
            if owner.owner_family == owner_family:
                return owner.authority_refs
        return ()


@dataclass(frozen=True)
class RowRespondentBinding:
    row_ordinal: int
    respondent_ref: ExactRef


@dataclass(frozen=True)
class OccurrenceRule:
    key: str
    topology_ref: ExactRef
    multiplicity_order_rank_fields: Mapping[str, Any]
    component_ref: ExactRef | None = None


@dataclass(frozen=True)
class ResponseValueRule:
    physical_key: str
    response_state: str
    occurrences: tuple[OccurrenceRule, ...]
    canonical_value: Any = None
    transform_authority_ref: AuthorityRef | None = None
    extra_authority_refs: tuple[AuthorityRef, ...] = ()


@dataclass(frozen=True)
class ResponseSlotRule:
    slot: PhysicalSlot
    question_binding: QuestionVariableBinding
    values: tuple[ResponseValueRule, ...]


@dataclass(frozen=True)
class CoordinateValueRule:
    physical_key: str
    coordinate_state: str
    canonical_value: Any = None
    extra_authority_refs: tuple[AuthorityRef, ...] = ()


@dataclass(frozen=True)
class CoordinateSlotRule:
    slot: PhysicalSlot
    native_coordinate_ref: ExactRef
    unit_taxonomy_ref: ExactRef
    effective_time: Any
    source_semantic_authority_ref: AuthorityRef
    canonical_coordinate_ref: ExactRef | None = None
    normalization_ref: AuthorityRef | ExactRef | None = None
    values: tuple[CoordinateValueRule, ...] = ()
    copy_observed_raw: bool = False


@dataclass(frozen=True)
class WeightValueRule:
    physical_key: str
    exact_value: Any
    state: str = "WEIGHT_VALID_AUTHORIZED"


@dataclass(frozen=True)
class WeightSlotRule:
    slot: PhysicalSlot
    weight_basis_id: str
    weight_source_ref: ExactRef
    design_authority_ref: AuthorityRef
    estimand_authority_ref: AuthorityRef
    effective_scope_ref: ExactRef
    normalization_ref: AuthorityRef | ExactRef | None = None
    values: tuple[WeightValueRule, ...] = ()
    copy_observed_numeric: bool = False
    extra_authority_refs: tuple[AuthorityRef, ...] = ()


@dataclass(frozen=True)
class ExactPhysicalCellStream:
    source_sha256: str
    row_count: int
    cell_iter_factory: Callable[[], Iterable[PhysicalCell]]
    transport_identity: str = "EXACT_REPLAY_EQUIVALENT_PHYSICAL_CELL_STREAM"
    decoder_metadata_digest: str | None = None

    def __post_init__(self):
        _sha(self.source_sha256, "source_sha256")
        if self.decoder_metadata_digest is not None:
            _sha(self.decoder_metadata_digest, "decoder_metadata_digest")
        if not isinstance(self.row_count, int) or isinstance(self.row_count, bool) or self.row_count < 0 or not callable(self.cell_iter_factory):
            raise SourceBackedC11FacadeError("invalid exact physical-cell stream")

    def iter_cells(self):
        return self.cell_iter_factory()


class _RoutingColumnBuilder:
    """Bounded dictionary for genuinely repeated fields, direct bytes otherwise."""
    __slots__=("dictionary","values","codes","blob","offsets")
    def __init__(self):
        self.dictionary={}
        self.values=[]
        self.codes=array("I")
        self.blob=bytearray()
        self.offsets=array("Q",[0])

    def _direct(self,value):
        self.blob.extend(value)
        self.offsets.append(len(self.blob))

    def add(self,value):
        if self.dictionary is None:
            self._direct(value)
            return
        code=self.dictionary.get(value)
        if code is None:
            if len(self.values)>=4096:
                # Do not retain a high-cardinality hash table or duplicate
                # dictionary in addition to its direct lane.
                for old in self.codes:
                    self._direct(self.values[old])
                self.dictionary=self.values=self.codes=None
                self._direct(value)
                return
            code=len(self.values)
            self.dictionary[value]=code
            self.values.append(value)
        self.codes.append(code)

    def finish(self):
        if self.dictionary is None:
            return (bytes(self.blob),_routing_le(self.offsets),b"")
        direct_cost=sum(len(self.values[code])+8 for code in self.codes)
        dict_cost=sum(len(v)+8 for v in self.values)+4*len(self.codes)
        if dict_cost<direct_cost:
            for value in self.values:
                self._direct(value)
            return (bytes(self.blob),_routing_le(self.offsets),_routing_le(self.codes))
        for code in self.codes:
            self._direct(self.values[code])
        return (bytes(self.blob),_routing_le(self.offsets),b"")


def _routing_le(values):
    import sys
    if sys.byteorder!="little":
        values.byteswap()
    return values.tobytes()


def _routing_column_value(column,row):
    blob,offsets,codes=column
    if codes:
        row=struct.unpack_from("<I",codes,4*row)[0]
    lo,hi=struct.unpack_from("<QQ",offsets,8*row)
    return blob[lo:hi]


@lru_cache(maxsize=256)
def _routing_field_key_bytes(key):
    return canonical_json(key).encode("utf-8")+b":"


class _PackedRoutingFacts(Sequence):
    """Detached, lossless private governed routing input at field grain.

    Only exact immutable builtin tuples, bytes, ints and strings are held.
    One digest per exact identity; repeated authority/risk/rule/respondent
    fields have bounded dictionaries, unique fields have direct byte lanes.
    The public semantic constructor and original ordered envelope are unchanged.
    No inference of eligibility or compression of away any exception.
    """
    __slots__=("_storage",)
    _top=("authority_snapshot_refs","dependency_refs",
          "producer_replay_locator_or_reference_root","schema_id","schema_version","typed_state")
    _prefix="urn:rawlsing:pre553:RoutingEligibilityFact:sha256:"

    def __setattr__(self,name,value):
        raise AttributeError("packed routing is immutable")

    def __init__(self,records):
        runs,ends=[],[]
        keys=None
        builders=[]
        digests=bytearray()
        count=0
        def flush():
            if keys is not None:
                runs.append((keys,tuple(b.finish() for b in builders),bytes(digests)))
                ends.append(count)
                digests.clear()
        for obj in records:
            if type(obj) is not RoutingEligibilityFact:
                raise SourceBackedC11FacadeError("packed routing requires exact routing facts")
            doc=obj.as_dict()
            h=obj.content_hash
            digest=bytes.fromhex(h)
            if len(digest)!=32 or digest.hex()!=h or obj.object_id!=self._prefix+h:
                raise SourceBackedC11FacadeError("packed routing identity drift")
            # Never silently repair a stale/forged supplied semantic preimage.
            if semantic_hash(obj.semantic_projection())!=h:
                raise SourceBackedC11FacadeError("packed routing semantic hash drift")
            fields=doc["semantic_fields"]
            shape=tuple(sorted(fields))
            if shape!=keys:
                flush()
                keys=shape
                builders=[_RoutingColumnBuilder() for _ in (*self._top,*keys)]
            for builder,value in zip(builders,(
                    *(doc[k] for k in self._top),*(fields[k] for k in keys))):
                builder.add(canonical_json(value).encode("utf-8"))
            digests.extend(digest)
            count+=1
        flush()
        object.__setattr__(self,"_storage",(tuple(runs),tuple(ends)))

    def immutable_storage(self):
        # Validate the actual builtin storage and its complete row geometry.
        # Canonical iteration, random access and sorted replay must describe
        # exactly the same rows, including after a malformed caller-side swap.
        def refuse():
            raise SourceBackedC11FacadeError("packed routing storage/row geometry drift")
        storage=self._storage
        if type(storage) is not tuple or len(storage)!=2:
            refuse()
        runs,ends=storage
        if type(runs) is not tuple or type(ends) is not tuple or len(runs)!=len(ends):
            refuse()
        count=0
        for run,end in zip(runs,ends):
            if type(run) is not tuple or len(run)!=3 or type(end) is not int:
                refuse()
            keys,columns,digests=run
            if (type(keys) is not tuple or any(type(k) is not str for k in keys)
                    or keys!=tuple(sorted(set(keys)))
                    or not RoutingEligibilityFact.REQUIRED_FIELDS.issubset(keys)
                    or type(columns) is not tuple or len(columns)!=len(self._top)+len(keys)
                    or type(digests) is not bytes or not digests or len(digests)%32):
                refuse()
            rows=len(digests)//32
            count+=rows
            if end!=count:
                refuse()
            for col in columns:
                if type(col) is not tuple or len(col)!=3 or any(type(x) is not bytes for x in col):
                    refuse()
                blob,offsets,codes=col
                if len(offsets)<16 or len(offsets)%8 or len(codes)%4:
                    refuse()
                entries=len(offsets)//8-1
                if (codes and len(codes)!=4*rows) or (not codes and entries!=rows):
                    refuse()
                prior=-1
                for offset, in struct.iter_unpack("<Q",offsets):
                    if (prior<0 and offset!=0) or offset<=prior or offset>len(blob):
                        refuse()
                    prior=offset
                if prior!=len(blob):
                    refuse()
                if codes and any(code>=entries for code, in struct.iter_unpack("<I",codes)):
                    refuse()
        return storage

    def __len__(self):
        ends=self._storage[1]
        return ends[-1] if ends else 0

    @classmethod
    def _row_bytes(cls,run,row):
        keys,columns,digests=run
        h=digests[32*row:32*(row+1)].hex().encode("ascii")
        def pair(k,v):
            return _routing_field_key_bytes(k)+v
        values={key:_routing_column_value(col,row) for key,col in zip(cls._top,columns)}
        values["content_hash"]=b'"'+h+b'"'
        values["object_id"]=b'"'+cls._prefix.encode("ascii")+h+b'"'
        values["semantic_fields"]=b"{"+b",".join(pair(key,_routing_column_value(col,row))
              for key,col in zip(keys,columns[len(cls._top):]))+b"}"
        return b"{"+b",".join(pair(key,values[key]) for key in sorted(values))+b"}"

    def canonical_rows(self):
        runs,ends=self._storage
        start=0
        for run,end in zip(runs,ends):
            for row in range(end-start):
                yield self._row_bytes(run,row)
            start=end

    def _location(self,index):
        runs,ends=self._storage
        if index<0:
            index+=len(self)
        if not 0<=index<len(self):
            raise IndexError(index)
        run=bisect_right(ends,index)
        return runs[run],index-(ends[run-1] if run else 0)

    def digest_at(self,index):
        run,row=self._location(index)
        return run[2][32*row:32*(row+1)]

    def row_ref(self,index):
        h=self.digest_at(index).hex()
        return ExactRef(RoutingEligibilityFact.FAMILY,self._prefix+h,h)

    def field_bytes(self,index,name):
        run,row=self._location(index)
        keys,columns,_=run
        return _routing_column_value(columns[len(self._top)+keys.index(name)],row)

    def _selector(self,index):
        from rawlsing_next._pre553_c11_execution_view import _RoutingRead,_ref_identity
        run,row=self._location(index)
        keys,columns,_=run
        def value(name):
            return json.loads(_routing_column_value(columns[len(self._top)+keys.index(name)],row))
        def top(name):
            return json.loads(_routing_column_value(columns[self._top.index(name)],row))
        routing,applicability=value("routing_state"),value("applicability_state")
        if type(routing) is not str or type(applicability) is not str:
            # Preserve incumbent behavior for unusual admissible preimages.
            return self[index]
        auths=tuple(authority_ref(a) for a in top("authority_snapshot_refs"))
        return _RoutingRead(_ref_identity(self.row_ref(index)),top("typed_state"),routing,applicability,
            _ref_identity(exact_ref(value("question_or_target_ref"))),
            _ref_identity(exact_ref(value("risk_set_ref"))),
            _ref_identity(exact_ref(value("member_set_replay_ref"))),
            tuple((a.authority_id,a.authority_version,a.authority_content_hash) for a in auths))

    def __getitem__(self,index):
        if isinstance(index,slice):
            return tuple(self[i] for i in range(*index.indices(len(self))))
        runs,ends=self._storage
        if index<0:
            index+=len(self)
        if not 0<=index<len(self):
            raise IndexError(index)
        run=bisect_right(ends,index)
        row=index-(ends[run-1] if run else 0)
        from rawlsing_next.pre553_carrier_execution import materialize_public_object
        return materialize_public_object(json.loads(self._row_bytes(runs[run],row)))

    def __iter__(self):
        from rawlsing_next.pre553_carrier_execution import materialize_public_object
        for row in self.canonical_rows():
            yield materialize_public_object(json.loads(row))

    @property
    def payload_bytes(self):
        return sum(len(digests)+sum(sum(len(v) for v in col) for col in cols)
                   for _,cols,digests in self._storage[0])


@dataclass(frozen=True,slots=True)
class _SortedPackedRoutingFacts(Sequence):
    """I02's canonical ordering over the same detached routing field lanes."""
    source: _PackedRoutingFacts
    storage: tuple
    order: bytes
    _order_pin: bytes

    @classmethod
    def build(cls,source):
        storage=source.immutable_storage()
        detached=object.__new__(_PackedRoutingFacts)
        object.__setattr__(detached,"_storage",storage)
        order=_routing_le(array("Q",sorted(range(len(detached)),key=detached.digest_at)))
        return cls(detached,storage,order,order)

    def __len__(self):
        return len(self.order)//8

    def _ordinal(self,i):
        if (self.source._storage is not self.storage or self.order is not self._order_pin
                or type(self.order) is not bytes):
            raise SourceBackedC11FacadeError("sealed routing backing/order replaced")
        if i<0:
            i+=len(self)
        if not 0<=i<len(self):
            raise IndexError(i)
        return struct.unpack_from("<Q",self.order,8*i)[0]

    def __getitem__(self,i):
        if isinstance(i,slice):
            return tuple(self[n] for n in range(*i.indices(len(self))))
        return self.source[self._ordinal(i)]

    def row_ref(self,i):
        return self.source.row_ref(self._ordinal(i))

    def field_bytes(self,i,name):
        return self.source.field_bytes(self._ordinal(i),name)

    def _selector(self,i):
        return self.source._selector(self._ordinal(i))

    def find(self,ref):
        if ref.kind!=RoutingEligibilityFact.FAMILY:
            return None
        h=bytes.fromhex(ref.content_hash)
        if ref.object_id!=_PackedRoutingFacts._prefix+ref.content_hash:
            return None
        lo,hi=0,len(self)
        while lo<hi:
            mid=(lo+hi)//2
            if self.source.digest_at(self._ordinal(mid))<h:
                lo=mid+1
            else:
                hi=mid
        if lo<len(self) and self.row_ref(lo)==ref:
            return lo
        return None

    def scoped_rows(self,universe_ref,respondent_keys):
        # Build ordinals by exact respondent/universe. Decode shared dimension
        # values once per distinct byte string; no expanded per-route objects.
        universe=canonical_json(universe_ref.as_dict()).encode("utf-8")
        grouped={key:array("Q") for key in respondent_keys}
        keys={}
        for i in range(len(self)):
            if self.field_bytes(i,"empirical_universe_ref")!=universe:
                continue
            raw=self.field_bytes(i,"scoped_respondent_ref")
            key=keys.get(raw)
            if key is None:
                key=exact_ref(json.loads(raw)).key
                keys[raw]=key
            if key not in grouped:
                raise SourceBackedC11FacadeError("sealed routing respondent outside selected universe")
            grouped[key].append(i)
        return {key:_PackedRoutingRows(self,_routing_le(rows)) for key,rows in grouped.items()}


@dataclass(frozen=True,slots=True)
class _PackedRoutingRows(Sequence):
    lane: _SortedPackedRoutingFacts
    ordinals: bytes

    def __len__(self):
        return len(self.ordinals)//8

    def _ordinal(self,i):
        if i<0:
            i+=len(self)
        if not 0<=i<len(self):
            raise IndexError(i)
        return struct.unpack_from("<Q",self.ordinals,8*i)[0]

    def __getitem__(self,i):
        if isinstance(i,slice):
            return tuple(self[n] for n in range(*i.indices(len(self))))
        return self.lane[self._ordinal(i)]

    def _selector(self,i):
        return self.lane._selector(self._ordinal(i))

    def dimension_bytes(self,i):
        row=self._ordinal(i)
        return (self.lane.field_bytes(row,"question_or_target_ref"),
                self.lane.field_bytes(row,"risk_set_ref"))


def _freeze_governed_input(value: Any) -> Any:
    """Detach mutable rule data once, before any physical-stream callback.

    Frozen dataclasses are shallow. A mutable response/occurrence/weight or
    coordinate subvalue must not change *during* the physical-cell iterator
    and then be restored before the entry/exit cache-key comparison. Canonical
    semantic and internal C11 records already own immutable identities and
    remain under their original validators, not a duplicated representation.
    This private snapshot does not issue scientific or source permission.
    """
    if type(value) is _PackedRoutingFacts:
        value.immutable_storage()
        return value
    if isinstance(value, (ExactRef, AuthorityRef, TypedAbsence,
                          CanonicalSemanticObject, C11InternalRecord)):
        return value
    if isinstance(value, Mapping):
        return MappingProxyType({
            key: _freeze_governed_input(item)
            for key, item in value.items()
        })
    if isinstance(value, (tuple, list)):
        items = tuple(_freeze_governed_input(item) for item in value)
        if isinstance(value, tuple) and all(a is b for a, b in zip(items, value)):
            return value
        return items
    if isinstance(value, (set, frozenset)):
        # Sets have no lawful mutable descendants as members. Make the
        # container immutable without reinterpreting its semantic elements.
        return frozenset(value)
    if is_dataclass(value):
        transformed = {
            field.name: _freeze_governed_input(getattr(value, field.name))
            for field in fields(value)
        }
        if all(transformed[field.name] is getattr(value, field.name)
               for field in fields(value)):
            return value
        return replace(value, **transformed)
    return value


def _cache_projection_preimage(value: Any) -> Any:
    """Lossless cache identity for the governed input (not a new authority).

    Semantic objects supply their content-addressed full preimages via refs or
    as_dict; dataclass rule carriers are recursively expanded so a changed
    source/row/response/occurrence/routing/weight rule cannot alias its old
    value under the same nominal projection ref.
    """
    if type(value) is _PackedRoutingFacts:
        return [json.loads(row) for row in value.canonical_rows()]
    if isinstance(value, (ExactRef, AuthorityRef, TypedAbsence)):
        return value.as_dict()
    if is_dataclass(value):
        return {
            field.name: _cache_projection_preimage(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, Mapping):
        return {key: _cache_projection_preimage(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_cache_projection_preimage(item) for item in value]
    if hasattr(value, "as_dict"):
        return value.as_dict()
    return value


@dataclass(frozen=True)
class GovernedC11Projection:
    projection_identity_ref: ExactRef
    source_artifact_id: str
    expected_source_sha256: str
    source_family_id: str
    study_product_id: str
    release_id: str
    instrument_release_id: str
    source_snapshot_retention_ref: ExactRef
    universes: tuple[EmpiricalUniverse, ...]
    respondents: tuple[RespondentIdentity, ...]
    row_bindings: tuple[RowRespondentBinding, ...]
    questions: tuple[QuestionVariableBinding, ...]
    response_slots: tuple[ResponseSlotRule, ...]
    coordinate_slots: tuple[CoordinateSlotRule, ...]
    routing: Sequence[RoutingEligibilityFact]
    weight_slots: tuple[WeightSlotRule, ...]
    authority_snapshots: tuple[AuthoritySnapshot, ...]
    source_relations: tuple[SourceUniverseRelation, ...] | TypedAbsence
    predicate_replay: tuple[C11InternalRecord, ...] | TypedAbsence
    comparator_replay: tuple[C11InternalRecord, ...] | TypedAbsence
    discovery_replay: tuple[C11InternalRecord, ...] | TypedAbsence
    structural_replay: tuple[C11InternalRecord, ...] | TypedAbsence
    required_authority_refs: tuple[AuthorityRef, ...]
    projection_authority_ref: AuthorityRef
    replay_authority_ref: AuthorityRef
    tie_order_ref: ExactRef
    replay_protocol_version: str
    slot_owner_sets: tuple[PhysicalSlotOwnerSet, ...] = ()

    def __post_init__(self):
        # Copy and deeply freeze rule-carrier descendants at the source-side
        # boundary. A caller may mutate its own mapping after construction;
        # that mutation must never alter the issued projection consumed by I02.
        for field in fields(self):
            original = getattr(self, field.name)
            frozen = _freeze_governed_input(original)
            if frozen is not original:
                object.__setattr__(self, field.name, frozen)
        exact_ref(self.projection_identity_ref, "projection_identity_ref")
        _sha(self.expected_source_sha256, "expected_source_sha256")
        if self.source_snapshot_retention_ref.content_hash != self.expected_source_sha256:
            raise SourceBackedC11FacadeError("snapshot ref does not bind expected source SHA")
        if not all((self.universes, self.respondents, self.row_bindings, self.questions,
                    self.response_slots, self.coordinate_slots, self.routing,
                    self.authority_snapshots, self.required_authority_refs)):
            raise SourceBackedC11FacadeError("projection omits mandatory governed semantic input")
        mandatory = {self.projection_authority_ref, self.replay_authority_ref}
        if not mandatory.issubset(set(self.required_authority_refs)):
            raise SourceBackedC11FacadeError("projection/replay authorities must be explicitly required")
        packaged = {a.authority_ref for a in self.authority_snapshots}
        if not set(self.required_authority_refs).issubset(packaged):
            raise SourceBackedC11FacadeError("required authority absent from projection closure")
        if len({x.row_ordinal for x in self.row_bindings}) != len(self.row_bindings):
            raise SourceBackedC11FacadeError("duplicate row replay coordinate")
        respondent_refs = {r.ref for r in self.respondents}
        if any(x.respondent_ref not in respondent_refs for x in self.row_bindings):
            raise SourceBackedC11FacadeError("row binding references absent respondent")

        family_rules = (
            (RESPONSE_OWNER_FAMILY, self.response_slots),
            (COORDINATE_OWNER_FAMILY, self.coordinate_slots),
            (WEIGHT_OWNER_FAMILY, self.weight_slots),
        )
        actual: dict[tuple[int, str], set[str]] = {}
        for family, rules in family_rules:
            keys = [x.slot.key for x in rules]
            if len(keys) != len(set(keys)):
                raise SourceBackedC11FacadeError("conflicting duplicate physical-slot semantic owners")
            for key in keys:
                actual.setdefault(key, set()).add(family)

        owner_sets: dict[tuple[int, str], PhysicalSlotOwnerSet] = {}
        for owner_set in self.slot_owner_sets:
            if owner_set.slot.key in owner_sets:
                raise SourceBackedC11FacadeError("duplicate physical-slot owner set")
            owner_sets[owner_set.slot.key] = owner_set

        for key, families in actual.items():
            declared = owner_sets.get(key)
            if len(families) > 1 and declared is None:
                raise SourceBackedC11FacadeError("implicit/unapproved second physical-slot owner")
            if declared is not None and set(declared.owner_families) != families:
                raise SourceBackedC11FacadeError("physical-slot owner set does not exactly match emitted semantic owners")
        if set(owner_sets) - set(actual):
            raise SourceBackedC11FacadeError("physical-slot owner set references a slot with no emitted semantic owner")

        owner_authorities = {ref for owner_set in owner_sets.values() for owner in owner_set.owners for ref in owner.authority_refs}
        if not owner_authorities.issubset(set(self.required_authority_refs)):
            raise SourceBackedC11FacadeError("physical-slot owner authority must be explicitly required")
        if not owner_authorities.issubset(packaged):
            raise SourceBackedC11FacadeError("physical-slot owner authority absent from projection closure")
        owner_registry = AuthorityRegistry(self.authority_snapshots)
        for owner_set in owner_sets.values():
            for owner in owner_set.owners:
                for ref in owner.authority_refs:
                    owner_registry.require(ref, object_family=owner.owner_family)

    @property
    def cache_identity(self) -> str:
        """Exact full governed-projection preimage, not just its asserted name.

        Caller-provided projection_identity_ref and authority refs do not
        establish equivalence when row/response/routing/weight/occurrence rules
        differ. Hash the actual entire producer input, preserving typed
        absence and canonical semantic references. This is cache isolation,
        not original-source/science/current-use authorization.
        """
        # Same canonical projection hash, stream one sequence member
        # at a time rather than expanding every routing preimage in RAM.
        h=hashlib.sha256()
        def emit(value):
            h.update(canonical_json(value).encode("utf-8"))
        h.update(b'{"contract":')
        emit(CONTRACT_ID)
        h.update(b',"projection":{')
        for i,f in enumerate(sorted(fields(self),key=lambda f:f.name)):
            if i:
                h.update(b",")
            emit(f.name)
            h.update(b":")
            value=getattr(self,f.name)
            if type(value) is _PackedRoutingFacts:
                h.update(b"[")
                for j,row in enumerate(value.canonical_rows()):
                    if j:
                        h.update(b",")
                    h.update(row)
                h.update(b"]")
            elif type(value) in (tuple,list):
                h.update(b"[")
                for j,item in enumerate(value):
                    if j:
                        h.update(b",")
                    emit(_cache_projection_preimage(item))
                h.update(b"]")
            else:
                emit(_cache_projection_preimage(value))
        h.update(b"}}")
        return h.hexdigest()


def _owner_material(owner_authority_refs: Iterable[AuthorityRef]) -> tuple[AuthorityRef, ...]:
    return _auths(owner_authority_refs)


def _event(source_sha, row, respondent, slot, cell, value, occ, p, owner_authority_refs=()):
    q = slot.question_binding
    owner_authority_refs = _owner_material(owner_authority_refs)
    material = {"contract": CONTRACT_ID, "projection": p.projection_identity_ref.as_dict(), "source_sha": source_sha,
                "row": row, "respondent": respondent.ref.as_dict(), "question": q.ref.as_dict(),
                "slot": slot.slot.key, "physical_value_key": value.physical_key, "occurrence": occ.key}
    if owner_authority_refs:
        material["slot_owner_authority_refs"] = [x.as_dict() for x in owner_authority_refs]
    group = semantic_hash({**material, "role": "GROUP"})
    eid = semantic_hash({**material, "role": "EVENT"})
    auths = [p.projection_authority_ref, authority_ref(q.semantic_authority_ref, "question semantic authority"),
             authority_ref(q.topology_authority_ref, "question topology authority"), *value.extra_authority_refs,
             *owner_authority_refs]
    if value.transform_authority_ref is not None:
        auths.append(value.transform_authority_ref)
    component = occ.component_ref or _opt_ref(q.component_subitem_ref_or_typed_absence, "component")
    return RespondentEvent(
        typed_state=value.response_state, authority_snapshot_refs=_auths(auths), dependency_refs=_refs((respondent.ref, q.ref)),
        producer_replay_locator_or_reference_root=_dref("PRE553_C05R2A_EVENT_REPLAY_ROOT", "event", material),
        empirical_universe_ref=respondent.empirical_universe_ref, scoped_respondent_ref=respondent.ref,
        native_question_ref=q.native_question_ref,
        canonical_question_ref_if_authorized=_opt_ref(q.canonical_question_ref_or_typed_absence, "canonical question"),
        component_or_subitem_ref=component,
        event_group_id=f"urn:rawlsing:pre553:c05r2a:event-group:sha256:{group}",
        response_event_id_or_deterministic_index=f"urn:rawlsing:pre553:c05r2a:event:sha256:{eid}",
        raw_response_value=raw_physical_value_witness(cell.raw_value), canonical_response_value_if_authorized=canonicalize(value.canonical_value),
        value_transform_authority_ref=value.transform_authority_ref, response_topology_ref=occ.topology_ref,
        multiplicity_order_rank_fields=canonicalize(occ.multiplicity_order_rank_fields), response_state=value.response_state)


def _coordinate(source_sha, row, respondent, slot, cell, rule, p, owner_authority_refs=()):
    owner_authority_refs = _owner_material(owner_authority_refs)
    if rule is None:
        if not slot.copy_observed_raw or cell.missing_state is not PhysicalMissingState.OBSERVED_STORAGE_VALUE:
            raise SourceBackedC11FacadeError("unbound/missing coordinate cannot acquire semantics")
        state = "OBSERVED_COORDINATE"
        canonical = None
        extras = ()
    else:
        state = rule.coordinate_state
        canonical = rule.canonical_value
        extras = rule.extra_authority_refs
    material = {"contract": CONTRACT_ID, "projection": p.projection_identity_ref.as_dict(), "source_sha": source_sha, "row": row,
                "respondent": respondent.ref.as_dict(), "slot": slot.slot.key, "physical_value_key": _cell_key(cell)}
    if owner_authority_refs:
        material["slot_owner_authority_refs"] = [x.as_dict() for x in owner_authority_refs]
    auths = [p.projection_authority_ref, slot.source_semantic_authority_ref, *extras, *owner_authority_refs]
    if isinstance(slot.normalization_ref, AuthorityRef):
        auths.append(slot.normalization_ref)
    return EmpiricalCoordinateFact(
        typed_state=state, authority_snapshot_refs=_auths(auths), dependency_refs=(respondent.ref,),
        producer_replay_locator_or_reference_root=_dref("PRE553_C05R2A_COORDINATE_REPLAY_ROOT", "coordinate", material),
        empirical_universe_ref=respondent.empirical_universe_ref, scoped_respondent_ref=respondent.ref,
        native_coordinate_ref=slot.native_coordinate_ref, canonical_coordinate_ref_if_authorized=slot.canonical_coordinate_ref,
        raw_coordinate_value=raw_physical_value_witness(cell.raw_value), canonical_coordinate_value_if_authorized=canonicalize(canonical),
        unit_category_taxonomy_ref=slot.unit_taxonomy_ref, effective_or_reference_time=canonicalize(slot.effective_time),
        coordinate_state=state, normalization_crosswalk_authority_ref=slot.normalization_ref,
        source_semantic_authority_ref=slot.source_semantic_authority_ref)


def _numeric(value):
    if isinstance(value, bool) or value is None:
        raise SourceBackedC11FacadeError("weight raw copy requires numeric")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise SourceBackedC11FacadeError("weight cannot be NaN/inf")
        text = repr(value)
        Fraction(text)
        return text
    if isinstance(value, str):
        text = value.strip()
        Fraction(text)
        return text
    raise SourceBackedC11FacadeError("weight raw copy requires exact numeric representation")


def _weight(source_sha, row, respondent, slot, cell, rule, p, owner_authority_refs=()):
    owner_authority_refs = _owner_material(owner_authority_refs)
    if rule is None:
        if not slot.copy_observed_numeric or cell.missing_state is not PhysicalMissingState.OBSERVED_STORAGE_VALUE:
            raise SourceBackedC11FacadeError("unbound/missing weight cannot default or fall back")
        state = "WEIGHT_VALID_AUTHORIZED"
        value = _numeric(cell.raw_value)
    else:
        state = rule.state
        value = rule.exact_value
    material = {"contract": CONTRACT_ID, "projection": p.projection_identity_ref.as_dict(), "source_sha": source_sha, "row": row,
                "respondent": respondent.ref.as_dict(), "slot": slot.slot.key, "physical_value_key": _cell_key(cell), "basis": slot.weight_basis_id}
    if owner_authority_refs:
        material["slot_owner_authority_refs"] = [x.as_dict() for x in owner_authority_refs]
    return WeightMeasureFact(
        typed_state=state, authority_snapshot_refs=_auths((p.projection_authority_ref, slot.design_authority_ref,
                                                           slot.estimand_authority_ref, *slot.extra_authority_refs,
                                                           *owner_authority_refs)),
        dependency_refs=(respondent.ref,), producer_replay_locator_or_reference_root=_dref("PRE553_C05R2A_WEIGHT_REPLAY_ROOT", "weight", material),
        empirical_universe_ref=respondent.empirical_universe_ref, scoped_respondent_ref=respondent.ref,
        weight_basis_id=slot.weight_basis_id, exact_weight_value_representation=canonicalize(value), weight_state=state,
        weight_source_ref=slot.weight_source_ref, design_authority_ref=slot.design_authority_ref,
        estimand_authority_ref=slot.estimand_authority_ref, normalization_or_recalibration_rule_ref=slot.normalization_ref,
        effective_scope_ref=slot.effective_scope_ref)


def _count(x):
    return 0 if isinstance(x, TypedAbsence) else len(x)


def _counts(p, events, coords, weights):
    return {"EmpiricalUniverse": len(p.universes), "RespondentIdentity": len(p.respondents), "QuestionVariableBinding": len(p.questions),
            "RespondentEvent": len(events), "RoutingEligibilityFact": len(p.routing), "EmpiricalCoordinateFact": len(coords),
            "WeightMeasureFact": _count(weights), "AuthoritySnapshot": len(p.authority_snapshots), "SourceUniverseRelation": _count(p.source_relations),
            "EmpiricalPredicateReplayBinding": _count(p.predicate_replay), "ComparatorReplayBinding": _count(p.comparator_replay),
            "DiscoveryBranchReplayBinding": _count(p.discovery_replay), "StructuralAdmissionReplayBinding": _count(p.structural_replay), "ReplayManifest": 1}


def project_c11_candidate_from_physical_cells(*, source_sha256: str, row_count: int,
                                               cells: Iterable[PhysicalCell], projection: GovernedC11Projection | None,
                                               _event_collector=None):
    if not isinstance(projection, GovernedC11Projection):
        raise SourceBackedC11FacadeError("explicit governed projection required; no semantic inference permitted")
    _sha(source_sha256, "source_sha256")
    if source_sha256 != projection.expected_source_sha256:
        raise SourceBackedC11FacadeError("source SHA mismatch")
    respondent_by_ref = {r.ref: r for r in projection.respondents}
    rows = {x.row_ordinal: (i,respondent_by_ref[x.respondent_ref])
            for i,x in enumerate(projection.row_bindings)}
    if len(rows) != row_count:
        raise SourceBackedC11FacadeError("row/respondent replay map cardinality differs from exact physical stream")
    restored=(_event_collector is not None and _event_collector.finished is not None)
    rs = {} if restored else {x.slot.key: x for x in projection.response_slots}
    cs = {x.slot.key: x for x in projection.coordinate_slots}
    ws = {x.slot.key: x for x in projection.weight_slots}
    owner_sets = {x.slot.key: x for x in projection.slot_owner_sets}
    projected = set(rs) | set(cs) | set(ws)
    # One bit of coverage per required row/slot, not a Python set per
    # variable retaining one integer object for every response.
    seen={s:bytearray((row_count+7)//8) for s in projected}
    counts={s:0 for s in projected}
    response_values={key:{x.physical_key:x for x in slot.values} for key,slot in rs.items()}
    coordinate_values={key:{x.physical_key:x for x in slot.values} for key,slot in cs.items()}
    weight_values={key:{x.physical_key:x for x in slot.values} for key,slot in ws.items()}
    events = []
    coords = []
    weights = []
    for cell in cells:
        if not isinstance(cell, PhysicalCell):
            raise SourceBackedC11FacadeError("non-PhysicalCell transport member")
        key = (cell.variable_ordinal, cell.variable_name)
        if key not in projected:
            continue
        if cell.row_ordinal not in rows:
            raise SourceBackedC11FacadeError("cell row outside replay map")
        position,respondent=rows[cell.row_ordinal]
        byte,bit=divmod(position,8)
        mask=1<<bit
        if seen[key][byte]&mask:
            raise SourceBackedC11FacadeError("duplicate physical row/slot")
        seen[key][byte]|=mask
        counts[key]+=1
        pv = _cell_key(cell)
        owner_set = owner_sets.get(key)
        if key in rs:
            slot = rs[key]
            value = response_values[key].get(pv)
            if value is None:
                raise SourceBackedC11FacadeError("unbound response value/state; no label/frequency/missingness inference")
            auths = owner_set.authority_refs_for(RESPONSE_OWNER_FAMILY) if owner_set else ()
            for occurrence_index, occurrence in enumerate(value.occurrences):
                event=_event(source_sha256,cell.row_ordinal,respondent,slot,cell,value,occurrence,projection,auths)
                if _event_collector is None:
                    events.append(event)
                else:
                    _event_collector.add(event, source_coordinates=(cell.row_ordinal, cell.variable_ordinal, occurrence_index))
        if key in cs:
            slot = cs[key]
            rule = coordinate_values[key].get(pv)
            auths = owner_set.authority_refs_for(COORDINATE_OWNER_FAMILY) if owner_set else ()
            coords.append(_coordinate(source_sha256, cell.row_ordinal, respondent, slot, cell, rule, projection, auths))
        if key in ws:
            slot = ws[key]
            rule = weight_values[key].get(pv)
            auths = owner_set.authority_refs_for(WEIGHT_OWNER_FAMILY) if owner_set else ()
            weights.append(_weight(source_sha256, cell.row_ordinal, respondent, slot, cell, rule, projection, auths))
    if any(v!=row_count for v in counts.values()):
        raise SourceBackedC11FacadeError("projected slot incomplete; absent physical cell is not semantic absence")
    events = (tuple(sorted(events,key=lambda x:x.ref.key))
              if _event_collector is None else
              _event_collector.finished if restored else _event_collector.finish())
    coords = tuple(sorted(coords, key=lambda x: x.ref.key))
    weight_section = tuple(sorted(weights, key=lambda x: x.ref.key)) if projection.weight_slots else TypedAbsence("NOT_APPLICABLE")
    manifest = SourceReleaseManifest(
        source_artifact_id=projection.source_artifact_id, source_artifact_content_hash=source_sha256, source_family_id=projection.source_family_id,
        study_product_id=projection.study_product_id, release_id=projection.release_id, instrument_release_id=projection.instrument_release_id,
        ingest_contract_version=INGEST_CONTRACT_VERSION, declared_universe_refs=tuple(sorted((x.ref for x in projection.universes), key=lambda r: r.key)),
        declared_authority_snapshot_refs=tuple(sorted((x.authority_ref for x in projection.authority_snapshots), key=lambda r: r.key)),
        declared_record_counts_by_logical_family=_counts(projection, events, coords, weight_section), source_snapshot_retention_ref=projection.source_snapshot_retention_ref)
    candidate = C11SourceReleaseCandidate(
        source_release_manifest=manifest, empirical_universes=tuple(sorted(projection.universes, key=lambda x: x.ref.key)),
        respondent_identities=tuple(sorted(projection.respondents, key=lambda x: x.ref.key)), question_variable_bindings=tuple(sorted(projection.questions, key=lambda x: x.ref.key)),
        respondent_events=events, routing_eligibility_facts_or_exact_rules=(
            _SortedPackedRoutingFacts.build(projection.routing)
            if _event_collector is not None and type(projection.routing) is _PackedRoutingFacts
            else tuple(sorted(projection.routing,key=lambda x:x.ref.key))), empirical_coordinate_facts=coords,
        weight_measure_facts_or_typed_absence=weight_section, authority_snapshots=tuple(sorted(projection.authority_snapshots, key=lambda x: x.authority_ref.key)),
        source_universe_relations_or_explicit_distinct_default=projection.source_relations, predicate_replay_bindings_when_retained_objects_require_them=projection.predicate_replay,
        comparator_replay_bindings_or_typed_deferred_state=projection.comparator_replay, discovery_branch_replay_bindings_or_typed_deferred_state=projection.discovery_replay,
        structural_admission_replay_bindings_or_typed_not_applicable_state=projection.structural_replay, candidate_replay_manifest=None)
    replay = build_candidate_replay_manifest(candidate, replay_protocol_authority_ref=projection.replay_authority_ref,
                                             deterministic_tie_order_rules_ref=projection.tie_order_ref, replay_protocol_version=projection.replay_protocol_version,
                                             _country_events=events if _event_collector is not None else None)
    return replace(candidate, candidate_replay_manifest=replay)


def _verify(candidate, p, sha):
    m = candidate.source_release_manifest
    if m.source_artifact_content_hash != sha or m.source_snapshot_retention_ref.content_hash != sha:
        raise SourceBackedC11FacadeError("candidate/source SHA mismatch")
    required = set(p.required_authority_refs)
    packaged = {x.authority_ref for x in candidate.authority_snapshots}
    declared = set(m.declared_authority_snapshot_refs)
    if not required.issubset(packaged) or not required.issubset(declared):
        raise SourceBackedC11FacadeError("required authority absent from C11 candidate closure")


def build_validated_source_backed_c11_release(incidence: PhysicalSourceIncidence, projection: GovernedC11Projection | None, *, batch_size: int = 10_000):
    if not isinstance(projection, GovernedC11Projection):
        raise SourceBackedC11FacadeError("explicit governed projection required")
    bridge = PhysicalSourceAuthorityProjection(required_authority_refs=projection.required_authority_refs,
        candidate_builder=lambda source, cells, _: project_c11_candidate_from_physical_cells(source_sha256=source.source_sha256,
                                                                                             row_count=source.row_count,
                                                                                             cells=cells, projection=projection))
    return build_validated_c11_release(incidence, bridge, batch_size=batch_size)


def build_validated_source_backed_c11_release_from_stream(stream: ExactPhysicalCellStream, projection: GovernedC11Projection | None):
    if not isinstance(projection, GovernedC11Projection):
        raise SourceBackedC11FacadeError("explicit governed projection required")
    candidate = project_c11_candidate_from_physical_cells(source_sha256=stream.source_sha256, row_count=stream.row_count,
                                                           cells=stream.iter_cells(), projection=projection)
    _verify(candidate, projection, stream.source_sha256)
    return validate_c11_source_release(candidate)


@dataclass(frozen=True)
class SourceBackedFacadeKey:
    source_sha256: str
    projection_identity: str
    physical_binding_identity: str | None = None


class SourceBackedC11SessionCache:
    def __init__(self):
        self._entries = {}
        # Sourcefree session cache; serialize only its small lookup/admission/
        # eviction metadata, never the I02 source read or I03 computation.
        self._lock = RLock()

    @staticmethod
    def _require_same_binding(key, release, entry):
        stored_key, prior = entry
        if (stored_key != key or not isinstance(prior, C11LogicalRelease)
                or prior.source_artifact_ref.content_hash != key.source_sha256
                or prior.release_ref != release.release_ref
                or prior.source_release_manifest_hash != release.source_release_manifest_hash
                or prior.replay_manifest.ref != release.replay_manifest.ref):
            raise SourceBackedC11FacadeError("conflicting cache rebind")

    @staticmethod
    def _require_source(key, release):
        if (not isinstance(release, C11LogicalRelease)
                or release.source_artifact_ref.content_hash != key.source_sha256):
            raise SourceBackedC11FacadeError("cache/source mismatch")

    def get(self, key):
        with self._lock:
            entry = self._entries.get(key)
            if entry is None:
                return None
            stored_key, release = entry
            if (stored_key != key or not isinstance(release, C11LogicalRelease)
                    or release.source_artifact_ref.content_hash != key.source_sha256):
                raise SourceBackedC11FacadeError("stale/tampered cache")
            return release

    def put(self, key, release):
        """Public replay is idempotent only; no unowned first cache admission."""
        self._require_source(key, release)
        with self._lock:
            existing = self._entries.get(key)
            if existing is None:
                raise SourceBackedC11FacadeError("producer-only cache admission")
            self._require_same_binding(key, release, existing)
            # Preserve first-admitted original object; never replace with a
            # second caller-supplied object sharing its exact identities.

    def _admit_from_source_backed_producer(self, key, release):
        """Single, atomic producer admission after I02 + full coherence checks.

        The prior contains() -> public put() split could refuse a legitimate
        validated producer when another thread cleared the session cache in
        between. Holding the cache metadata lock prevents that false denial
        and retains A's producer-only first insertion + B's rebind refusal.
        This is local synchronization, not external source/issuer authority.
        """
        self._require_source(key, release)
        with self._lock:
            existing = self._entries.get(key)
            if existing is None:
                self._entries[key] = (key, release)
            else:
                self._require_same_binding(key, release, existing)

    def clear(self):
        with self._lock:
            self._entries.clear()

    @property
    def entry_count(self):
        with self._lock:
            return len(self._entries)


def source_backed_facade_key(source, p, *, current_authorities=()):
    """Cache only under the same full semantics AND physical-read context."""
    binding = {
        "row_count": source.row_count,
        "decoder_metadata_digest": _accelerator_decoder_digest(source),
        "transport_identity": getattr(source, "transport_identity", None),
        "current_authority_refs": sorted(a.ref.key for a in current_authorities),
    }
    return SourceBackedFacadeKey(
        source.source_sha256, p.cache_identity, semantic_hash(binding),
    )


def _accelerator_decoder_digest(source: PhysicalSourceIncidence | ExactPhysicalCellStream) -> str | None:
    if isinstance(source, ExactPhysicalCellStream):
        return source.decoder_metadata_digest
    try:
        return source.physical_metadata_digest
    except DecoderError:
        # Legacy in-memory incidence can be valid for I02 without a file decoder receipt.
        return None


def build_source_backed_c11_repository(
    source, projection, *, cache=None, batch_size=10_000, current_authorities=(),
    _country_preparation=None,
):
    # One-shot iterables must not disappear between cache admission and the
    # compact physical-binding witness. Both must see identical authorities.
    current_authorities = tuple(current_authorities)
    if cache is not None and not isinstance(cache, SourceBackedC11SessionCache):
        raise SourceBackedC11FacadeError("source-backed cache must be producer-owned session cache")
    from .pre553_country_numeric_carrier import _CountryPhysicalStream
    country = type(source) is _CountryPhysicalStream
    if country and cache is not None:
        raise SourceBackedC11FacadeError("country repository has live reader; no detached session cache")
    if _country_preparation is not None and not country:
        raise SourceBackedC11FacadeError("country preparation requires live country transport")
    key = source_backed_facade_key(source, projection, current_authorities=current_authorities)
    if country:
        # Rebind to the live reader's own selected decoder, not a caller's
        # replacement cell_iter_factory on a copied country transport.
        source._verify_binding()
        trusted=source.reader._native_stream(projection)
        if source_backed_facade_key(trusted,projection,current_authorities=current_authorities)!=key:
            raise SourceBackedC11FacadeError("country source transport differs from live reader")
        source=trusted
        # The I02 owner validates each actual event as the physical producer
        # emits it, then seals the same logical package from exact headers.
        # No complete event-object graph or second body archive is retained.
        restored_headers=None
        captured=None
        if _country_preparation is not None:
            from ._pre553_country_preparation import _CountryPreparation
            if type(_country_preparation) is not _CountryPreparation:
                raise SourceBackedC11FacadeError("private country preparation required")
            source.reader.verify_full()
            restored_headers=_country_preparation.load(key)
        def produce(collector):
            nonlocal captured
            if restored_headers is None:
                cells=source.iter_cells()
            else:
                # Only coordinate/weight bodies need physical re-production.
                # Response bodies remain in the authenticated numeric carrier.
                selected={rule.slot.key for rules in
                          (projection.coordinate_slots,projection.weight_slots)
                          for rule in rules}
                cells=source.reader._iter_slots(tuple(sorted(selected)))
            candidate=project_c11_candidate_from_physical_cells(
                source_sha256=source.source_sha256,row_count=source.row_count,
                cells=cells,projection=projection,_event_collector=collector)
            _verify(candidate,projection,source.source_sha256)
            if _country_preparation is not None and restored_headers is None:
                captured=collector.finished
            return candidate
        release=_validate_country_produced_release(produce=produce,
            authority_snapshots=projection.authority_snapshots,
            compact_builder=lambda ref,replay,non_events,headers,closure_refs,routing:
                source.compact_events(ref,replay,non_events,headers,projection,closure_refs,routing),
            _restored_headers=restored_headers)
        if source_backed_facade_key(source,projection,current_authorities=current_authorities)!=key:
            raise SourceBackedC11FacadeError("cache input changed during C11 build")
        repo=C11Repository((release,))
        if _country_preparation is not None:
            source.reader.verify_full()
            _country_preparation.finish(key,release,captured)
            source.reader._verify()
        source.certify_release(release,facade_key=key)
        return repo,release
    release = cache.get(key) if cache else None
    if release is None:
        release = (build_validated_source_backed_c11_release(source, projection, batch_size=batch_size)
                   if isinstance(source, PhysicalSourceIncidence)
                   else build_validated_source_backed_c11_release_from_stream(source, projection)
                   if isinstance(source, ExactPhysicalCellStream)
                   else (_ for _ in ()).throw(SourceBackedC11FacadeError("unsupported physical transport")))
        def physical_binding():
            decoder_digest = _accelerator_decoder_digest(source)
            if isinstance(source, PhysicalSourceIncidence) and decoder_digest is None:
                return None
            return {
                "decoder_metadata": decoder_digest,
                "transport": getattr(source, "transport_identity", None),
                "facade_contract": CONTRACT_ID,
                "value_codec": R5_CODEC_VERSION,
                "current_authorities": sorted(snapshot.ref.key for snapshot in current_authorities),
            }

        public = _compact_public_objects(
            release, physical_binding=physical_binding, projection_binding=key.projection_identity,
            country_body_factory=(lambda rel, events: source.event_bodies(rel, events, projection)) if country else None,
        )
        if public is not None:
            release = replace(release, public_objects=public)
        elif country:
            raise SourceBackedC11FacadeError("country compact native selector unavailable")
        # Frozen dataclasses can still enclose caller-owned mutable mappings.
        # The physical iterator (or a sidecar callback) may mutate them after
        # input admission but before I02 finishes. A valid release computed
        # under changed source/semantic/authority context is not an issued
        # release under the original context, whether or not a cache exists.
        if source_backed_facade_key(
            source, projection, current_authorities=current_authorities
        ) != key:
            raise SourceBackedC11FacadeError("cache input changed during C11 build")
        if cache:
            cache._admit_from_source_backed_producer(key, release)
    elif cache and source_backed_facade_key(
        source, projection, current_authorities=current_authorities
    ) != key:
        # Covers mutation during a cache.get callback (or concurrent owner
        # changes) on a hit, not only the fresh-build path.
        raise SourceBackedC11FacadeError("cache input changed during C11 build")
    return C11Repository((release,)), release


def execute_source_backed_empirical_query(*, source, projection, query: EmpiricalQuerySpec, predicate: EmpiricalPredicate,
                                          authority_registry: AuthorityRegistry, cache=None, batch_size=10_000) -> QueryExecutionResult:
    repo, release = build_source_backed_c11_repository(source, projection, cache=cache, batch_size=batch_size)
    return execute_empirical_query(repository=repo, query=query, predicate=predicate, authority_registry=authority_registry,
                                   release_refs=(release.release_ref,))


__all__ = [
    "CONTRACT_ID", "SLOT_OWNER_SET_CONTRACT_ID", "RESPONSE_OWNER_FAMILY", "COORDINATE_OWNER_FAMILY", "WEIGHT_OWNER_FAMILY",
    "SourceBackedC11FacadeError", "PHYSICAL_VALUE_MATERIAL_SCHEMA", "PHYSICAL_BINDING_SCHEMA", "RAW_WITNESS_SCHEMA",
    "exact_physical_value_material", "raw_physical_value_witness", "PhysicalSlot", "PhysicalSlotOwnerAuthorization", "PhysicalSlotOwnerSet",
    "RowRespondentBinding", "OccurrenceRule", "ResponseValueRule", "ResponseSlotRule", "CoordinateValueRule",
    "CoordinateSlotRule", "WeightValueRule", "WeightSlotRule", "ExactPhysicalCellStream", "GovernedC11Projection",
    "SourceBackedFacadeKey", "SourceBackedC11SessionCache", "physical_value_binding_key",
    "project_c11_candidate_from_physical_cells", "build_validated_source_backed_c11_release",
    "build_validated_source_backed_c11_release_from_stream", "source_backed_facade_key",
    "build_source_backed_c11_repository", "execute_source_backed_empirical_query",
]
