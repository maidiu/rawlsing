"""Issuer-custodied request transport into the existing selected Route B owners.

This module has no issuer, grant writer, statistical compiler, or source reader.
Deployment supplies a competent current-decision resolver and an exact source
factory. Both are trusted infrastructure, outside caller/checkpoint custody.
The resolver must authenticate competence and current source/host/purpose rights;
matching a hash alone does not establish those rights.
"""
from __future__ import annotations

from collections import Counter
from contextlib import ExitStack
from collections.abc import Mapping
from dataclasses import dataclass, fields, is_dataclass
import json
import hashlib
import sys
from types import MappingProxyType
from typing import Any, Callable, Protocol

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec, ExecutionOutcome,
    ExecutorBinding, UnitExecutionReceipt,
)
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor, I03GroupedExecutionScope, RuntimeObjectCatalog,
)
from rawlsing_next.pre553_saved_c11_admission import (
    SavedBindingReceipt,
    SavedC11Admission,
)
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from rawlsing_next.pre553_discovery_exact import COVERAGE_CLAIM, I05_CONTRACT_ID
from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from types import SimpleNamespace
from rawlsing_next.pre553_empirical_objects import (
    DiscoveryResultReceipt, EmpiricalFact, EmpiricalPredicate,
    EmpiricalQuerySpec, ExactRef, AuthorityRef, RoutingEligibilityFact,
    canonical_json, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest, execute_route_b_production
from rawlsing_next.pre553_source_backed_c11_facade import (
    GovernedC11Projection, _PackedRoutingFacts, build_source_backed_c11_repository,
)


class WorkloadAdmissionError(ValueError):
    pass


class NativeWorkloadExecutionError(RuntimeError):
    pass


def material(value: Any) -> Any:
    """Complete dataclass preimages, including fields omitted by count receipts."""
    # Exact builtin fast paths. The full issued envelope is still rebuilt and
    # hashed at every admission boundary. No identity-only or stale hash cache.
    typ = type(value)
    if value is None or typ in (str, bool, int, float, bytes):
        return value
    if typ is dict:
        return {str(k): material(v) for k, v in value.items()}
    if typ is _PackedRoutingFacts:
        return [json.loads(row) for row in value.canonical_rows()]
    if typ is list or typ is tuple:
        return [material(v) for v in value]
    if hasattr(value, "as_dict"):
        return material(value.as_dict())
    if is_dataclass(value):
        return {f.name: material(getattr(value, f.name)) for f in fields(value)}
    if isinstance(value, Mapping):
        return {str(k): material(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [material(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((material(v) for v in value), key=lambda x: json.dumps(x, sort_keys=True))
    return value


def canonical(value: Any) -> bytes:
    return json.dumps(material(value), sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def operation_jobs(requests, discoveries):
    return tuple(sorted(
        [("QUERY", r.query_ref.key, r.predicate_ref.key) for r in requests]
        + [("DISCOVERY", d.key, "") for d in discoveries]
    ))


@dataclass(frozen=True)
class OriginalWaveIdentity:
    """Canonical roster identity; native aliases require the issuer's own binding."""
    atlas_id: str
    dataset_id: str
    source_family: str
    wave: str

    def __post_init__(self):
        if any(not isinstance(value, str) or not value.strip() for value in (
            self.atlas_id, self.dataset_id, self.source_family, self.wave
        )):
            raise WorkloadAdmissionError("COMPLETE_ORIGINAL_WAVE_IDENTITY_REQUIRED")


@dataclass(frozen=True)
class IssuedWorkloadRecord:
    """Read result from external competent custody; never created by this worker."""
    decision_ref: ExactRef
    source_permission_ref: ExactRef
    scientific_permission_refs: tuple[ExactRef, ...]
    host: str
    purpose: str
    source_sha256: str
    envelope_sha256: str
    original_u_root: str
    expected_frontier_root: str
    expected_jobs: tuple[tuple[str, str, str], ...]
    currentness: str
    scope: str
    original_wave_identity: OriginalWaveIdentity | None = None
    native_universe_refs: tuple[ExactRef, ...] = ()


class CurrentDecisionResolver(Protocol):
    def resolve_current(self, decision_ref: ExactRef) -> IssuedWorkloadRecord:
        """Authenticate issuer, scope, source/host/purpose and revocation externally.

        The read must be repeatable: this module rechecks the same decision at
        the source-read, restore and pre-publication boundaries. A resolver must
        not consume a single-use authorization token on the first read.
        """
        ...


def _require_current_resolver(resolver: Any) -> CurrentDecisionResolver:
    """Refuse an absent or non-independent current-decision resolver."""
    if resolver is None or not callable(getattr(resolver, "resolve_current", None)):
        raise WorkloadAdmissionError("INDEPENDENT_CURRENT_DECISION_RESOLVER_REQUIRED")
    return resolver


@dataclass(frozen=True)
class ExpectedWorkloadBinding:
    original_wave_identity: OriginalWaveIdentity
    decision_ref: ExactRef
    envelope_sha256: str


@dataclass(frozen=True)
class IssuedEstateFrontier:
    """Authenticated scheduling read, composed from separately competent issuers.

    This is a permitted-packet census for the current phase, not an issuer of
    original source rights, administered U, or scientific E_pre. Its custody is
    independent of the submitted workload mapping, just like expected_jobs.
    """
    frontier_ref: ExactRef
    host: str
    purpose: str
    roster_identity: str
    expected_workloads: tuple[ExpectedWorkloadBinding, ...]
    currentness: str
    scope: str


def original35_roster(waves) -> tuple[OriginalWaveIdentity, ...]:
    roster = tuple(sorted((OriginalWaveIdentity(
        w["atlas_id"], w["original_manifest_identity"]["dataset_id"], w["family"], w["wave"]
    ) for w in waves), key=lambda w: w.atlas_id))
    if len(roster) != 35 or len({w.atlas_id for w in roster}) != 35:
        raise WorkloadAdmissionError("INDEPENDENT_ORIGINAL35_ROSTER_REQUIRED")
    return roster


def reconcile_estate_workloads(waves, workloads, frontier: IssuedEstateFrontier):
    """No-drop transport for all independently expected permitted native packets.

    A wave can have multiple country/shard/purpose packets. No source is opened
    and no empirical/scientific candidate is generated during reconciliation.
    """
    roster = original35_roster(waves)
    by_atlas = {w.atlas_id: w for w in roster}
    if semantic_hash(material(roster)) != frontier.roster_identity:
        raise WorkloadAdmissionError("ISSUED_ESTATE_ROSTER_IDENTITY_MISMATCH")
    if not set(workloads) <= set(by_atlas):
        raise WorkloadAdmissionError("UNEXPECTED_WAVE_OUTSIDE_ORIGINAL35")
    expected = []
    for entry in frontier.expected_workloads:
        wave = entry.original_wave_identity
        if by_atlas.get(wave.atlas_id) != wave:
            raise WorkloadAdmissionError("ISSUER_FRONTIER_WAVE_NOT_IN_FROZEN_ROSTER")
        expected.append((wave.atlas_id, entry.decision_ref.key, entry.envelope_sha256))
    if len(expected) != len(set(expected)):
        raise WorkloadAdmissionError("ISSUER_FRONTIER_DUPLICATE_NATIVE_PACKET")
    submitted = []
    prepared = []
    for atlas_id, values in workloads.items():
        packets = (values,) if isinstance(values, NativeWorkload) else tuple(values)
        for packet in packets:
            if not isinstance(packet, NativeWorkload):
                raise WorkloadAdmissionError("EXACT_NATIVE_WORKLOAD_REQUIRED")
            if packet.original_wave_identity != by_atlas[atlas_id]:
                raise WorkloadAdmissionError("ORIGINAL35_ROSTER_TO_NATIVE_PACKET_MISMATCH")
            submitted.append((atlas_id, packet.decision_ref.key, semantic_hash(packet.envelope())))
            prepared.append((by_atlas[atlas_id], packet))
    if Counter(submitted) != Counter(expected):
        raise WorkloadAdmissionError("EXPECTED_NATIVE_PACKET_IDENTITY_MULTISET_MISMATCH")
    return tuple(sorted(prepared, key=lambda pair: (
        pair[0].atlas_id, pair[1].decision_ref.key, semantic_hash(pair[1].envelope())
    )))


DESCRIPTOR_FIELDS = frozenset({
    "source_edition", "native_item_ids", "release_tag", "routing_and_risk",
    "carrier", "country_and_population", "weight_design_estimand",
    "missing_and_occurrence_policy", "target_conditioner_roles",
})


@dataclass(frozen=True)
class NativeWorkload:
    decision_ref: ExactRef
    source_factory_ref: ExactRef
    descriptor: bytes
    projection: GovernedC11Projection
    catalog: RuntimeObjectCatalog
    requests: tuple[I03ExecutionRequest, ...]
    discoveries: tuple[ExactRef, ...]
    original_u_root: str
    expected_frontier_root: str
    original_wave_identity: OriginalWaveIdentity | None = None

    def envelope(self):
        return self._envelope()

    def _envelope(self, *, omit_routing=False):
        descriptor = json.loads(self.descriptor)
        if set(descriptor) != DESCRIPTOR_FIELDS or canonical(descriptor) != self.descriptor:
            raise WorkloadAdmissionError("CLOSED_CANONICAL_COMPLETE_DESCRIPTOR_REQUIRED")
        if any(v is None or v == "UNBOUND" for v in descriptor.values()):
            raise WorkloadAdmissionError("ISSUED_DESCRIPTOR_HAS_UNBOUND_REQUIRED_FIELD")
        projection = (
            {f.name: material(getattr(self.projection, f.name))
             for f in fields(self.projection) if f.name != "routing"}
            if omit_routing else material(self.projection)
        )
        envelope = dict(
            descriptor=descriptor, projection=projection,
            catalog=material(self.catalog), source_factory_ref=self.source_factory_ref.as_dict(),
            requests=[r.as_dict() for r in self.requests],
            discoveries=[r.as_dict() for r in self.discoveries],
            original_u_root=self.original_u_root, expected_frontier_root=self.expected_frontier_root,
        )
        if self.original_wave_identity is not None:
            envelope["original_wave_identity"] = material(self.original_wave_identity)
        return envelope


def _routing_pin(obj):
    """Pin the existing deeply immutable canonical object, not a caller ref.

    CanonicalSemanticObject owns its detached mapping-proxy descendants.
    Recheck the public scalar and ref fields (including ref preimages), and
    retain the original semantic-fields mapping by identity. This is the
    same in-process immutable-data boundary as I03 index attestation, not
    security against arbitrary Python-memory modification.
    """
    if type(obj) is not RoutingEligibilityFact or obj._frozen is not True:
        return None
    if type(obj.semantic_fields) is not MappingProxyType:
        return None
    scalar=(obj.schema_id,obj.schema_version,obj.typed_state,obj.object_id,obj.content_hash)
    if any(type(v) is not str for v in scalar):
        return None
    auth=obj.authority_snapshot_refs
    deps=obj.dependency_refs
    if (type(auth) is not tuple or type(deps) is not tuple
        or any(type(v) is not AuthorityRef for v in auth)
        or any(type(v) is not ExactRef for v in deps)):
        return None
    auth_material=tuple((v.authority_id,v.authority_version,v.authority_content_hash) for v in auth)
    dep_material=tuple((v.kind,v.object_id,v.content_hash) for v in deps)
    replay=obj.producer_replay_locator_or_reference_root
    if type(replay) is ExactRef:
        replay=(replay.kind,replay.object_id,replay.content_hash)
    elif type(replay) is not str:
        return None
    return scalar,auth_material,dep_material,replay


def _routing_envelope_parts(workload):
    """Stream the canonical prefix and suffix around the sole routing array."""
    envelope=workload._envelope(omit_routing=True)
    def pieces(values, projection=False):
        yield b"{"
        keys=sorted((*values.keys(),"routing")) if projection else sorted(values)
        for i,key in enumerate(keys):
            if i:
                yield b","
            yield canonical_json(key).encode("utf-8")
            yield b":"
            if projection and key=="routing":
                yield None
            elif not projection and key=="projection":
                yield from pieces(values[key],True)
            else:
                yield canonical_json(values[key]).encode("utf-8")
        yield b"}"
    return pieces(envelope)


def _stream_workload_digest(workload):
    """Same complete canonical U43 hash, without retaining routing JSON."""
    digest=hashlib.sha256()
    for part in _routing_envelope_parts(workload):
        if part is not None:
            digest.update(part)
            continue
        digest.update(b"[")
        routing=workload.projection.routing
        rows=(routing.canonical_rows() if type(routing) is _PackedRoutingFacts
              else (canonical_json(material(obj)).encode("utf-8") for obj in routing))
        for i,row in enumerate(rows):
            if i:
                digest.update(b",")
            digest.update(row)
        digest.update(b"]")
    return digest.hexdigest()


def _update_routing_pin(digest,pin):
    # Pin material consists solely of exact strings and nested tuples. Python
    # repr of these primitives is unambiguous, including embedded controls.
    # This is private in-process mutation detection, not the U43 wire hash.
    def valid(value):
        return type(value) is str or (type(value) is tuple and all(valid(v) for v in value))
    if not valid(pin):
        return False
    digest.update(repr(pin).encode("utf-8"))
    digest.update(b"\n")
    return True


def _fast_routing_row(obj):
    """Keep immutable leaf identities and shared link objects, not their JSON.

    Strong references pin all old leaves, including equal-but-distinct strings.
    The tuple's members cannot be replaced. Ref contents are verified separately
    once per *actual reference object*, not once per route that uses it.
    """
    return (obj.schema_id, obj.schema_version, obj.typed_state,
            obj.object_id, obj.content_hash, obj.authority_snapshot_refs,
            obj.dependency_refs, obj.producer_replay_locator_or_reference_root)


def _fast_routing_row_matches(obj, mapping, row):
    # Identity, not user-defined equality: all original scalar leaves were
    # exact builtins, all original link tuples were exact tuples, and the
    # original semantic mapping is detached and deeply frozen.
    return (type(obj) is RoutingEligibilityFact and obj._frozen is True
            and obj.semantic_fields is mapping
            and obj.schema_id is row[0] and obj.schema_version is row[1]
            and obj.typed_state is row[2] and obj.object_id is row[3]
            and obj.content_hash is row[4] and obj.authority_snapshot_refs is row[5]
            and obj.dependency_refs is row[6]
            and obj.producer_replay_locator_or_reference_root is row[7])


def _fast_ref_pin(ref):
    if type(ref) is AuthorityRef:
        values=(ref.authority_id,ref.authority_version,ref.authority_content_hash)
    elif type(ref) is ExactRef:
        values=(ref.kind,ref.object_id,ref.content_hash)
    else:
        raise TypeError("noncanonical routing reference")
    if any(type(v) is not str for v in values):
        raise TypeError("noncanonical routing reference preimage")
    return (ref,*values)


def _fast_ref_matches(row):
    ref=row[0]
    if type(ref) is AuthorityRef:
        return (ref.authority_id is row[1] and ref.authority_version is row[2]
                and ref.authority_content_hash is row[3])
    if type(ref) is ExactRef:
        return (ref.kind is row[1] and ref.object_id is row[2]
                and ref.content_hash is row[3])
    return False


@dataclass(frozen=True,slots=True)
class _NonRoutingEnvelopePin:
    """Bounded structural witness over the rest of the exact issued preimage.

    Never replaces the independent current resolver, initial canonical SHA,
    job/catalog checks, or packed routing storage pin. Reuse only known
    incumbent representations; unsupported dynamic/custom inputs fall back
    to full canonical serialization. No caller-mutable mapping is assumed
    immutable: check every mapping entry, and every actual ref instance.
    """
    attrs: tuple
    mappings: tuple
    retained_bytes: int

    @classmethod
    def capture(cls,workload,max_bytes):
        from rawlsing_next.pre553_empirical_objects import (
            CanonicalSemanticObject,_FrozenSemanticList,PUBLIC_OBJECT_FAMILIES)
        from rawlsing_next.pre553_c11_integrity import C11InternalRecord,TypedAbsence
        seen=set()
        attrs=[]
        mappings=[]
        used=256
        known_dataclasses={
            "rawlsing_next.pre553_source_backed_c11_facade",
            "rawlsing_next.pre553_carrier_execution",
            "rawlsing_next.pre553_route_b_production",
            "rawlsing_next.pre553_issued_workload",
            "rawlsing_next.pre553_c11_integrity",
            "rawlsing_next.pre553_empirical_objects",
        }
        class Unsupported(Exception):
            pass
        def budget(n):
            nonlocal used
            used+=n
            if used>max_bytes:
                raise Unsupported
        def attr(obj,names):
            if cls._has_serialization_override(obj):
                raise Unsupported
            vals=tuple(getattr(obj,n) for n in names)
            attrs.append((obj,type(obj),names,vals))
            budget(128+16*len(names))
            for v in vals:
                visit(v)
        def visit(obj):
            typ=type(obj)
            if obj is None or typ in (str,bool,int,float,bytes):
                return
            ident=id(obj)
            if ident in seen:
                return
            seen.add(ident)
            budget(72)
            if typ in (tuple,_FrozenSemanticList):
                for v in obj:
                    visit(v)
            elif typ in (dict,MappingProxyType):
                items=tuple(obj.items())
                if any(type(k) is not str for k,v in items):
                    raise Unsupported
                mappings.append((obj,items))
                budget(128+80*len(items))
                for k,v in items:
                    visit(v)
            elif typ is GovernedC11Projection:
                attr(obj,tuple(f.name for f in fields(obj) if f.name!="routing"))
            elif isinstance(obj,CanonicalSemanticObject):
                if (typ.__module__!="rawlsing_next.pre553_empirical_objects"
                        or obj.FAMILY not in PUBLIC_OBJECT_FAMILIES
                        or typ.as_dict is not CanonicalSemanticObject.as_dict
                        or obj._frozen is not True):
                    raise Unsupported
                attr(obj,("schema_id","schema_version","typed_state","object_id","content_hash",
                          "authority_snapshot_refs","dependency_refs",
                          "producer_replay_locator_or_reference_root","_semantic_fields","_frozen"))
            elif isinstance(obj,C11InternalRecord):
                if (typ.__module__!="rawlsing_next.pre553_c11_integrity"
                        or typ.as_dict is not C11InternalRecord.as_dict):
                    raise Unsupported
                attr(obj,tuple(f.name for f in fields(obj))+("content_hash","object_id","ref"))
            elif typ in (ExactRef,AuthorityRef,TypedAbsence,I03ExecutionRequest,NativeWorkload,RuntimeObjectCatalog):
                attr(obj,tuple(f.name for f in fields(obj)))
            elif (typ.__module__ in known_dataclasses and is_dataclass(obj)
                  and not hasattr(obj,"as_dict")):
                attr(obj,tuple(f.name for f in fields(obj)))
            else:
                raise Unsupported
        try:
            visit(workload)
        except (Unsupported,TypeError,ValueError,AttributeError,RecursionError):
            return None
        return cls(tuple(attrs),tuple(mappings),used)

    @staticmethod
    def _has_serialization_override(obj):
        # The pin covers known incumbent field representations, not
        # instance-overridden serialization behavior.
        own=getattr(obj,"__dict__",{})
        return any(k in own for k in ("as_dict","semantic_projection","envelope",
                                      "_envelope","request_identity"))

    def matches(self):
        missing=object()
        for obj,typ,names,vals in self.attrs:
            if (type(obj) is not typ or self._has_serialization_override(obj)
                    or any(getattr(obj,n,missing) is not v for n,v in zip(names,vals))):
                return False
        for obj,items in self.mappings:
            if len(obj)!=len(items) or any(k not in obj or obj[k] is not v for k,v in items):
                return False
        return True


@dataclass(frozen=True)
class _PreparedRoutingEnvelope:
    """Reuse an exact SHA continuation, not a second serialized routing graph.

    Admission still compares the exact externally issued complete envelope
    digest. The canonical prefix is freshly hashed, and only if it equals the
    prepared prefix do we copy the SHA state *after* the routing list. All
    suffix bytes are freshly hashed. Routing public objects' detached
    immutable mappings remain pinned by identity and their public scalar/ref
    fields are checked with a streaming private pin digest. No routing JSON
    retained, no original-source opt-in, no arbitrary Python memory defense.
    """
    workload: NativeWorkload
    routing: tuple
    mappings: tuple
    pin_digest: bytes
    prefix_digest: bytes
    after_routing: Any
    encoded_routing_bytes: int
    retained_pin_bytes: int
    fast_pins: tuple | None = None
    fast_ref_pins: tuple | None = None
    packed_storage: tuple | None = None
    nonrouting_pin: _NonRoutingEnvelopePin | None = None
    complete_digest: str | None = None

    @classmethod
    def prepare(cls, workload, expected_hash, *, max_bytes=32*1024*1024,
                max_records=4_000_000):
        if (type(workload) is not NativeWorkload
                or type(workload.projection) is not GovernedC11Projection):
            return None
        routing=workload.projection.routing
        if type(routing) is _PackedRoutingFacts:
            if max_bytes<1024:
                return None
            # Full exact envelope independently matched at initial admission.
            # No caller-supplied digest or prepared hash is trusted. The
            # actual routing bytes are detached immutable builtin leaves.
            storage=routing.immutable_storage()
            nonrouting=_NonRoutingEnvelopePin.capture(workload,min(max_bytes-512,8*1024*1024))
            digest=hashlib.sha256()
            pieces=_routing_envelope_parts(workload)
            for part in pieces:
                if part is None:
                    break
                digest.update(part)
            else:
                return None
            prefix=digest.copy().digest()
            digest.update(b"[")
            encoded_bytes=2
            for i,row in enumerate(routing.canonical_rows()):
                if i:
                    digest.update(b",")
                    encoded_bytes+=1
                digest.update(row)
                encoded_bytes+=len(row)
            digest.update(b"]")
            after=digest.copy()
            for part in pieces:
                if part is None:
                    return None
                digest.update(part)
            if digest.hexdigest()!=expected_hash or routing._storage is not storage:
                return None
            if nonrouting is not None and not nonrouting.matches():
                return None
            return cls(workload,routing,(),b"",prefix,after,encoded_bytes,
                       sys.getsizeof(after)+256+(nonrouting.retained_bytes if nonrouting else 0),
                       packed_storage=storage,nonrouting_pin=nonrouting,
                       complete_digest=expected_hash if nonrouting else None)
        if type(routing) is not tuple or len(routing)>max_records:
            return None
        # Bound the temporary list + retained tuple of mapping references,
        # with conservative pointer/container allowance. No encoded-size cap:
        # large routing arrays are hashed in a stream, never held as JSON.
        if 256+24*len(routing)>max_bytes:
            return None
        digest=hashlib.sha256()
        pieces=_routing_envelope_parts(workload)
        for part in pieces:
            if part is None:
                break
            digest.update(part)
        else:
            return None
        prefix=digest.copy().digest()
        pins=hashlib.sha256()
        mappings=[]
        # The fast layout holds one shallow row per route, plus one leaf
        # pin per distinct *actual* reference object. Never deduplicate
        # mutable reference instances merely because their values agree.
        # Limit estimated additional pointer/tuple/dict capacity; the old
        # streaming layout remains the bounded fallback at larger scales.
        fast=[] if 128*len(routing)+256<=max_bytes//2 else None
        ref_pins={} if fast is not None else None
        fast_bytes=0
        digest.update(b"[")
        encoded_bytes=2
        for i,obj in enumerate(routing):
            pin=_routing_pin(obj)
            if pin is None or not _update_routing_pin(pins,pin):
                return None
            encoded=canonical_json(material(obj)).encode("utf-8")
            if i:
                digest.update(b",")
                encoded_bytes+=1
            digest.update(encoded)
            encoded_bytes+=len(encoded)
            mappings.append(obj.semantic_fields)
            if fast is not None:
                row=_fast_routing_row(obj)
                fast.append(row)
                fast_bytes+=sys.getsizeof(row)+24
                for ref in (*row[5],*row[6],*((row[7],) if type(row[7]) is ExactRef else ())):
                    key=id(ref)
                    if key not in ref_pins:
                        ref_pin=_fast_ref_pin(ref)
                        ref_pins[key]=ref_pin
                        # Include conservative allowance for temporary dict,
                        # final tuple pointers, and key integer.
                        fast_bytes+=sys.getsizeof(ref_pin)+128
                if fast_bytes+24*len(routing)>max_bytes//2:
                    fast=None
                    ref_pins=None
                    fast_bytes=0
        digest.update(b"]")
        after=digest.copy()
        for part in pieces:
            if part is None:
                return None
            digest.update(part)
        if digest.hexdigest()!=expected_hash:
            return None
        held=tuple(mappings)
        return cls(workload,routing,held,pins.digest(),prefix,after,encoded_bytes,
                   sys.getsizeof(held)+sys.getsizeof(after)+128+fast_bytes,
                   tuple(fast) if fast is not None else None,
                   tuple(ref_pins.values()) if ref_pins is not None else None)

    def digest(self):
        workload=self.workload
        if (type(workload.projection) is not GovernedC11Projection
                or workload.projection.routing is not self.routing):
            return None
        if self.packed_storage is not None:
            if type(self.routing) is not _PackedRoutingFacts or self.routing._storage is not self.packed_storage:
                return None
            if self.nonrouting_pin is not None:
                return self.complete_digest if self.nonrouting_pin.matches() else None
        elif len(self.mappings)!=len(self.routing):
            return None
        elif self.fast_pins is not None:
            if (self.fast_ref_pins is None
                    or len(self.fast_pins)!=len(self.routing)):
                return None
            for obj,mapping,row in zip(self.routing,self.mappings,self.fast_pins):
                if not _fast_routing_row_matches(obj,mapping,row):
                    return None
            for row in self.fast_ref_pins:
                if not _fast_ref_matches(row):
                    return None
        else:
            pins=hashlib.sha256()
            for obj,mapping in zip(self.routing,self.mappings):
                if obj.semantic_fields is not mapping:
                    return None
                pin=_routing_pin(obj)
                if pin is None or not _update_routing_pin(pins,pin):
                    return None
            if pins.digest()!=self.pin_digest:
                return None
        digest=hashlib.sha256()
        pieces=_routing_envelope_parts(workload)
        for part in pieces:
            if part is None:
                if digest.digest()!=self.prefix_digest:
                    return None
                digest=self.after_routing.copy()
                break
            digest.update(part)
        else:
            return None
        for part in pieces:
            if part is None:
                return None
            digest.update(part)
        return digest.hexdigest()


def admit(workload: NativeWorkload, resolver: CurrentDecisionResolver, *, host: str,
          purpose: str, allow_test_only: bool = False,
          expected_wave: OriginalWaveIdentity | None = None) -> IssuedWorkloadRecord:
    """Public admission always validates the complete ordinary envelope."""
    return _admit(workload,resolver,host=host,purpose=purpose,
                  allow_test_only=allow_test_only,expected_wave=expected_wave)


def _admit(workload: NativeWorkload, resolver: CurrentDecisionResolver, *, host: str,
           purpose: str, allow_test_only: bool = False,
           expected_wave: OriginalWaveIdentity | None = None,
           prepared: _PreparedRoutingEnvelope | None = None,
           _capture_prepared: list | None = None) -> IssuedWorkloadRecord:
    """Refuse copied/rehash descriptors and no-drop violations before source open.

    ``resolver`` is an independent external reader, never the historical
    ``item.record`` supplied with a checkpoint. Every failure here happens
    before this module can open source or restore a retained result.
    """
    resolver = _require_current_resolver(resolver)
    if not isinstance(host, str) or not host.strip():
        raise WorkloadAdmissionError("NONEMPTY_HOST_REQUIRED")
    if not isinstance(purpose, str) or not purpose.strip():
        raise WorkloadAdmissionError("NONEMPTY_PURPOSE_REQUIRED")
    try:
        record = resolver.resolve_current(workload.decision_ref)
    except WorkloadAdmissionError:
        raise
    except Exception as exc:
        raise WorkloadAdmissionError("CURRENT_DECISION_RESOLVER_REFUSED") from exc
    if not isinstance(record, IssuedWorkloadRecord) or record.decision_ref != workload.decision_ref:
        raise WorkloadAdmissionError("CURRENT_AUTHENTICATED_ISSUER_RECORD_REQUIRED")
    scopes = {"ORIGINAL_SOURCE_GRANTED"}
    if allow_test_only:
        scopes.add("TEST_ONLY_SOURCEFREE")
    if record.scope not in scopes or record.currentness != "CURRENT_GRANTED":
        raise WorkloadAdmissionError("CURRENT_COMPETENT_SOURCE_AND_SCIENCE_DECISION_REQUIRED")
    if (record.host, record.purpose) != (host, purpose):
        raise WorkloadAdmissionError("SOURCE_HOST_PURPOSE_MISMATCH")
    if record.scope == "ORIGINAL_SOURCE_GRANTED" or expected_wave is not None:
        identity = workload.original_wave_identity
        if not isinstance(identity, OriginalWaveIdentity) or record.original_wave_identity != identity:
            raise WorkloadAdmissionError("ISSUED_ORIGINAL_WAVE_BINDING_REQUIRED")
        if expected_wave is not None and identity != expected_wave:
            raise WorkloadAdmissionError("ORIGINAL35_ROSTER_TO_NATIVE_PACKET_MISMATCH")
        if (not isinstance(record.native_universe_refs, tuple)
                or any(not isinstance(ref, ExactRef) for ref in record.native_universe_refs)
                or Counter(record.native_universe_refs) != Counter(
                    u.ref for u in workload.projection.universes
                )):
            raise WorkloadAdmissionError("ISSUED_NATIVE_UNIVERSE_TO_ORIGINAL_WAVE_MISMATCH")
    if (not isinstance(record.scientific_permission_refs, tuple)
            or not record.scientific_permission_refs
            or any(not isinstance(ref, ExactRef) for ref in record.scientific_permission_refs)
            or not isinstance(record.source_permission_ref, ExactRef)):
        raise WorkloadAdmissionError("SEPARATE_SOURCE_AND_SCIENTIFIC_PERMISSIONS_REQUIRED")
    if (record.original_u_root, record.expected_frontier_root) != (
        workload.original_u_root, workload.expected_frontier_root
    ):
        raise WorkloadAdmissionError("INDEPENDENT_PROSPECTIVE_U_E_PRE_ROOT_MISMATCH")
    if (not isinstance(record.expected_jobs, tuple) or any(
        not isinstance(job, tuple) or len(job) != 3
        or not all(isinstance(part, str) for part in job)
        for job in record.expected_jobs
    )):
        raise WorkloadAdmissionError("EXPECTED_EXECUTED_OPERATION_IDENTITY_MULTISET_MISMATCH")
    jobs = operation_jobs(workload.requests, workload.discoveries)
    if Counter(jobs) != Counter(record.expected_jobs) or len(jobs) != len(set(jobs)) or not jobs:
        raise WorkloadAdmissionError("EXPECTED_EXECUTED_OPERATION_IDENTITY_MULTISET_MISMATCH")
    if record.source_sha256 != workload.projection.expected_source_sha256:
        raise WorkloadAdmissionError("ISSUED_SOURCE_EDITION_MISMATCH")
    new_prepared = None
    try:
        envelope_sha256 = None
        if type(prepared) is _PreparedRoutingEnvelope and prepared.workload is workload:
            envelope_sha256 = prepared.digest()
        if (envelope_sha256 is None and _capture_prepared is not None
                and record.scope=="TEST_ONLY_SOURCEFREE"):
            # The initial full exact envelope pass can also prepare its
            # reusable routing witness. Do not repeat that pass after source
            # open. A preparation refusal retains the ordinary full path.
            new_prepared = _PreparedRoutingEnvelope.prepare(workload,record.envelope_sha256)
            if new_prepared is not None:
                envelope_sha256 = record.envelope_sha256
        if envelope_sha256 is None:
            if (record.scope=="TEST_ONLY_SOURCEFREE"
                    and type(workload) is NativeWorkload
                    and type(workload.projection) is GovernedC11Projection
                    and type(workload.projection.routing) in (tuple,_PackedRoutingFacts)):
                envelope_sha256=_stream_workload_digest(workload)
            else:
                envelope_sha256 = semantic_hash(workload.envelope())
    except WorkloadAdmissionError:
        raise
    except (TypeError, ValueError) as exc:
        raise WorkloadAdmissionError("CLOSED_CANONICAL_COMPLETE_DESCRIPTOR_REQUIRED") from exc
    if envelope_sha256 != record.envelope_sha256:
        raise WorkloadAdmissionError("ENTIRE_EXECUTION_DESCRIPTOR_NOT_THE_ISSUED_ENVELOPE")
    # One exact local lookup per validated envelope, not repeated full
    # catalog scans for every job. Duplicate/custom inputs use old resolver.
    cat=workload.catalog
    query_map=predicate_map=discovery_map=None
    if type(cat) is RuntimeObjectCatalog:
        query_map={obj.ref:obj for obj in cat.queries}
        predicate_map={obj.ref:obj for obj in cat.predicates}
        discovery_map={obj.ref:obj for obj in cat.discovery_authorities}
        if (len(query_map)!=len(cat.queries) or len(predicate_map)!=len(cat.predicates)
                or len(discovery_map)!=len(cat.discovery_authorities)):
            query_map=predicate_map=discovery_map=None
    for r in workload.requests:
        q=(query_map.get(r.query_ref) if query_map is not None else None)
        if q is None:
            q=cat.resolve_query_exact(r.query_ref)
        if material(q.condition_predicate_ref) != r.predicate_ref.as_dict():
            raise WorkloadAdmissionError("QUERY_TARGET_CONDITION_DIRECTION_MISMATCH")
        if predicate_map is None or r.predicate_ref not in predicate_map:
            cat.resolve_predicate_exact(r.predicate_ref)
    for ref in workload.discoveries:
        if discovery_map is None or ref not in discovery_map:
            cat.resolve_discovery_authority_exact(ref)
    if _capture_prepared is not None:
        _capture_prepared.append(new_prepared)
    return record


class _CountryAdmissionScope:
    """One privately constructed proof for an existing country transaction.

    Every former full admission still calls the independent resolver and
    checks the exact descriptor, jobs, catalog and routing witness. The
    canonical record pin is detached so in-place mutation of a returned
    resolver object is not mistaken for the same issued record. No grant is
    cached. Only sourcefree exact envelopes use the prepared optimization.
    """
    def __init__(self,workload,resolver,*,host,purpose,allow_test_only,expected_wave=None):
        self.workload=workload
        self.resolver=resolver
        self.host=host
        self.purpose=purpose
        self.allow_test_only=allow_test_only
        self.expected_wave=expected_wave
        captured=[]
        self.record=_admit(workload,resolver,host=host,purpose=purpose,
                           allow_test_only=allow_test_only,expected_wave=expected_wave,
                           _capture_prepared=captured)
        self._prepared=captured[0]
        self._record_pin=canonical(self.record)
        r=self.record.decision_ref
        self._decision=ExactRef(r.kind,r.object_id,r.content_hash)

    def check(self):
        current=_admit(self.workload,self.resolver,host=self.host,purpose=self.purpose,
                       allow_test_only=self.allow_test_only,expected_wave=self.expected_wave,
                       prepared=self._prepared)
        if canonical(current)!=self._record_pin:
            raise WorkloadAdmissionError("ISSUER_SNAPSHOT_CHANGED_DURING_EXECUTION")
        return current

    def current_only(self):
        # Physical lane access and retained-product item reads already have
        # full content-admission brackets; retain their independent live
        # record boundary and compare against detached exact material.
        current=self.resolver.resolve_current(self._decision)
        if type(current) is not IssuedWorkloadRecord or canonical(current)!=self._record_pin:
            raise WorkloadAdmissionError("ISSUER_SNAPSHOT_CHANGED_DURING_EXECUTION")
        return current


@dataclass(frozen=True)
class NativeWorkloadResult:
    route_results: tuple[Any, ...]
    native_outputs: tuple[Any, ...]
    manifest: BatchManifest
    receipts: tuple[Any, ...]
    output_refs: tuple[ExactRef, ...]
    envelope_sha256: str
    decision_ref: ExactRef
    scope: str
    summary: Any
    original_wave_identity: OriginalWaveIdentity | None = None
    source_sha256: str | None = None
    outputs_by_unit: Mapping[str, Any] | None = None

    def exact_s2e_output_census(self, *, require_complete: bool = True,
                                runtime_catalog: RuntimeObjectCatalog | None = None):
        """Audit full native I03/I05 and Batch first-reader output preimages.

        This read-only S2-E proof surface is intentionally optional and
        cannot mint native/source/scientific authority or a completed Batch
        claim for an intentionally partial execution. No second evaluator.
        """
        from rawlsing_next.pre553_s2e_exact_conservation import census_native_batch

        return census_native_batch(
            self.manifest, self.receipts, self.outputs_by_unit or {},
            require_complete=require_complete, runtime_catalog=runtime_catalog,
        )


def execute_issued_workload(workload: NativeWorkload, resolver: CurrentDecisionResolver, *,
                            source_factory: Callable[[ExactRef], Any] | None = None,
                            saved_admission_factory: Callable[[], SavedC11Admission] | None = None,
                            host: str, purpose: str,
                            allow_test_only: bool = False, prior_receipts=(),
                            prior_outputs=None, max_units=None,
                            expected_wave: OriginalWaveIdentity | None = None,
                            group_scope: I03GroupedExecutionScope | None = None,
                            reuse_prepared_saved_session: bool = False,
                            checkpoint_every: int | None = None,
                            checkpoint_observer: Callable[[NativeWorkloadResult], None] | None = None):
    """Public issued execution: no caller-supplied admission witness."""
    return _execute_issued_workload(
        workload,resolver,source_factory=source_factory,
        saved_admission_factory=saved_admission_factory,host=host,purpose=purpose,
        allow_test_only=allow_test_only,prior_receipts=prior_receipts,
        prior_outputs=prior_outputs,max_units=max_units,expected_wave=expected_wave,
        group_scope=group_scope,reuse_prepared_saved_session=reuse_prepared_saved_session,
        checkpoint_every=checkpoint_every,checkpoint_observer=checkpoint_observer)


def _execute_issued_workload(workload: NativeWorkload, resolver: CurrentDecisionResolver, *,
                            source_factory: Callable[[ExactRef], Any] | None = None,
                            saved_admission_factory: Callable[[], SavedC11Admission] | None = None,
                            host: str, purpose: str,
                            allow_test_only: bool = False, prior_receipts=(),
                            prior_outputs=None, max_units=None,
                            expected_wave: OriginalWaveIdentity | None = None,
                            group_scope: I03GroupedExecutionScope | None = None,
                            reuse_prepared_saved_session: bool = False,
                            checkpoint_every: int | None = None,
                            checkpoint_observer: Callable[[NativeWorkloadResult], None] | None = None, _country_scope=None,
                            _expected_country_identity=None,_country_session=None):
    """Reuse C11, Route B, I03, I05 and Batch; eligibility comes from external U/E_pre.

    A factory is called only after admission. Source bytes stay inside the native
    owner. The return contains native results/receipts, with no authority promotion.
    Exact receipt persistence and preimages remain the existing Batch/C11 custody
    responsibility; prior receipts must resolve in the rebuilt native repository.

    The external decision is re-read at every boundary where source can be read,
    restored or served. A revoked/replaced decision cannot open source or
    publish a positive result.
    """
    if max_units is not None and (
        not isinstance(max_units, int) or isinstance(max_units, bool) or max_units < 1
    ):
        raise WorkloadAdmissionError("POSITIVE_MAX_UNITS_REQUIRED")
    if (checkpoint_every is None) != (checkpoint_observer is None):
        raise WorkloadAdmissionError("CHECKPOINT_INTERVAL_AND_OBSERVER_REQUIRED_TOGETHER")
    if checkpoint_every is not None and (
        type(checkpoint_every) is not int or checkpoint_every < 1
        or not callable(checkpoint_observer)
        or (saved_admission_factory is None and _country_scope is None)
    ):
        raise WorkloadAdmissionError("EXACT_SAVED_CHECKPOINT_OBSERVER_REQUIRED")
    if (_expected_country_identity is not None or _country_session is not None) and _country_scope is None:
        raise WorkloadAdmissionError("COUNTRY_RESUME_REQUIRES_PRIVATE_ADMISSION_SCOPE")
    if type(reuse_prepared_saved_session) is not bool:
        raise WorkloadAdmissionError("EXACT_PREPARED_SAVED_OPT_IN_REQUIRED")
    if reuse_prepared_saved_session and saved_admission_factory is None:
        raise WorkloadAdmissionError("PREPARED_SAVED_REQUIRES_SAVED_ADMISSION")
    if _country_scope is not None:
        if (type(_country_scope) is not _CountryAdmissionScope
                or _country_scope.workload is not workload
                or _country_scope.resolver is not resolver
                or (_country_scope.host,_country_scope.purpose,
                    _country_scope.allow_test_only,_country_scope.expected_wave)
                   != (host,purpose,allow_test_only,expected_wave)
                or saved_admission_factory is not None):
            raise WorkloadAdmissionError("COUNTRY_ADMISSION_SCOPE_MISMATCH")
        record=_country_scope.check()
        if ((checkpoint_observer is not None or _expected_country_identity is not None)
                and record.scope!="TEST_ONLY_SOURCEFREE"):
            raise WorkloadAdmissionError("COUNTRY_CHECKPOINT_ORIGINAL_RETENTION_HELD")
    else:
        record = admit(workload, resolver, host=host, purpose=purpose, allow_test_only=allow_test_only,
                       expected_wave=expected_wave)
    # The native Batch owner verifies receipt structure, not external issuance.
    # Do not accept caller-rehashed historical receipts through this new ingress.
    # P4's separately authenticated fact/receipt custody is the proven cold path.
    prior_receipts = tuple(prior_receipts)
    prior_outputs = dict(prior_outputs or {})

    prepared = None

    def check_current():
        if _country_scope is not None:
            current=_country_scope.check()
        elif prepared is None:
            current = admit(workload, resolver, host=host, purpose=purpose,
                            allow_test_only=allow_test_only,expected_wave=expected_wave)
        else:
            current = _admit(workload,resolver,host=host,purpose=purpose,
                             allow_test_only=allow_test_only,expected_wave=expected_wave,
                             prepared=prepared)
        if current != record:
            raise WorkloadAdmissionError("ISSUER_SNAPSHOT_CHANGED_DURING_EXECUTION")

    # Admit and recheck immediately before the source/saved-estate boundary.
    # The saved admission factory is called only after the fresh external
    # CURRENT admission above; no estate bytes are opened by this function
    # before that admission.
    check_current()
    saved = None
    if saved_admission_factory is not None:
        # The source factory is deliberately not called on the saved path. A
        # caller may retain its tripwire/factory for legacy compatibility.
        if group_scope is not None:
            raise WorkloadAdmissionError(
                "SAVED_GROUPED_SCOPE_UNSUPPORTED"
            )
        if not callable(saved_admission_factory):
            raise WorkloadAdmissionError("SAVED_ADMISSION_FACTORY_INVALID")
        check_current()
        saved = saved_admission_factory()
        if type(saved) is not SavedC11Admission:
            raise WorkloadAdmissionError("EXACT_SAVED_C11_ADMISSION_REQUIRED")
        if saved.source_ref.content_hash != record.source_sha256:
            raise WorkloadAdmissionError("SAVED_SOURCE_DOES_NOT_MATCH_CURRENT_SOURCE")
        if saved.release_ref.object_id != workload.projection.release_id:
            raise WorkloadAdmissionError("SAVED_RELEASE_DOES_NOT_MATCH_WORKLOAD")
        check_current()
        release_ref = saved.release_ref
        replay_ref = saved.replay_ref
        routes = ()
        repository = saved
        executor = None
        owned_group_scope = None
    else:
        if not callable(source_factory):
            raise WorkloadAdmissionError("SOURCE_FACTORY_REQUIRED")
        source = source_factory(workload.source_factory_ref)
        if source.source_sha256 != record.source_sha256:
            raise WorkloadAdmissionError("SOURCE_FACTORY_RETURNED_WRONG_EDITION")
        check_current()
        # Bounded sourcefree country opt-in only. Original sources and other
        # carriers retain the incumbent admission path until qualified.
        from rawlsing_next.pre553_country_numeric_carrier import _CountryPhysicalStream,CountryWorkloadSession
        if _country_session is not None and (type(_country_session) is not CountryWorkloadSession
                or record.scope!="TEST_ONLY_SOURCEFREE"):
            raise WorkloadAdmissionError("EXACT_SOURCEFREE_COUNTRY_SESSION_REQUIRED")
        if _country_scope is not None and type(source) is not _CountryPhysicalStream:
            raise WorkloadAdmissionError("COUNTRY_ADMISSION_REQUIRES_LIVE_COUNTRY_STREAM")
        if (_country_scope is None and type(source) is _CountryPhysicalStream
                and record.scope=="TEST_ONLY_SOURCEFREE"):
            prepared = _PreparedRoutingEnvelope.prepare(workload,record.envelope_sha256)
        # No invented empty DiscoveryAuthority: query-only scopes use actual C11/I03.
        routes_list = []
        if max_units is None:
            for n, ref in enumerate(workload.discoveries):
                check_current()
                routes_list.append(execute_route_b_production(
                    source=source, projection=workload.projection, runtime_catalog=workload.catalog,
                    i03_requests=workload.requests if n == 0 else (), discovery_authority_ref=ref,
                ))
                check_current()
        routes = tuple(routes_list)
        check_current()
        if _country_session is None:
            repo, release = build_source_backed_c11_repository(
                source, workload.projection, current_authorities=workload.catalog.authorities,
            )
        else:
            repo, release = _country_session._repository(source,workload.projection,workload.catalog.authorities)
        check_current()
        # The authenticated prior product binds the complete release, not
        # merely its source hash or a caller-supplied release id. Verify before
        # any pending unit can consume the newly certified country.
        if _expected_country_identity is not None:
            source._verify_binding()
            if source.reader._certified_identity!=_expected_country_identity:
                raise WorkloadAdmissionError("RESUME_COUNTRY_RELEASE_OR_REPLAY_DRIFT")
        executor = CarrierNeutralResearchExecutor(repo, (release.release_ref,), workload.catalog)
        owned_group_scope = None
        if group_scope is None and _country_session is not None:
            group_scope=_country_session._query_scope_for(repo)
        if group_scope is None and len(workload.requests) + len(workload.discoveries) > 1:
            group_scope = I03GroupedExecutionScope()
            owned_group_scope = group_scope
        release_ref = release.release_ref
        replay_ref = release.replay_manifest.ref
        repository = repo

    units = tuple(BatchUnitSpec("QUERY", r.query_ref, (release_ref,),
                               (r.predicate_ref, workload.decision_ref)) for r in workload.requests)
    units += tuple(BatchUnitSpec("DISCOVERY", d, (release_ref,),
                                (workload.decision_ref,)) for d in workload.discoveries)
    manifest = BatchManifest(units)
    _validate_prior_cache(manifest, prior_receipts, prior_outputs)
    outputs = dict(prior_outputs)
    requests_by_query = {r.query_ref.key: r for r in workload.requests}
    # Reuse the existing prepared saved reader *inside* the original issuer
    # owner. Its exact decision, source/current and output-receipt guards
    # remain mandatory; no second Batch, estimator or issuer is created.
    prepared_session = None

    def execute(unit):
        check_current()
        if saved is not None:
            saved_reader = prepared_session if prepared_session is not None else saved
            if unit.job_kind == "QUERY":
                result = saved_reader.execute_i03(
                    query_ref=unit.job_ref,
                    predicate_ref=requests_by_query[unit.job_ref.key].predicate_ref,
                )
                refs = tuple(f.ref for f in result.facts)
            else:
                result = saved_reader.execute_i05(
                    discovery_authority_ref=unit.job_ref,
                )
                refs = tuple(r.ref for r in result.receipts)
        elif unit.job_kind == "QUERY":
            result = executor.execute_i03(query_ref=unit.job_ref,
                predicate_ref=requests_by_query[unit.job_ref.key].predicate_ref,
                group_scope=group_scope)
            refs = tuple(f.ref for f in result.facts)
        else:
            result = executor.execute_i05(discovery_authority_ref=unit.job_ref,
                group_scope=group_scope)
            refs = tuple(r.ref for r in result.receipts)
        check_current()
        outputs[unit.unit_hash] = result
        return ExecutionOutcome(refs, (replay_ref, workload.decision_ref))

    def executor_ref(kind):
        h = semantic_hash({"module": __name__, "kind": kind, "envelope": record.envelope_sha256})
        return ExactRef("U43_ISSUED_NATIVE_TRANSPORT", "urn:rawlsing:u43:" + h, h)

    runner = BatchExecutionRunner(
        manifest=manifest, repository=repository, prior_receipts=prior_receipts,
        saved_mode=saved is not None,
    )
    def snapshot():
        return NativeWorkloadResult(
            routes, tuple(outputs[k] for k in sorted(outputs)), manifest, runner.receipts,
            tuple(ref for r in runner.receipts for ref in r.result_refs),
            record.envelope_sha256, record.decision_ref, record.scope, runner.summary(),
            record.original_wave_identity, record.source_sha256, dict(outputs))

    attempts_since_checkpoint = 0

    def checkpoint():
        nonlocal attempts_since_checkpoint
        check_current()
        if saved is not None:
            saved.check_current()
        else:
            source._verify_binding()
        checkpoint_observer(snapshot())
        if saved is not None:
            saved.check_current()
        else:
            source._verify_binding()
        check_current()
        attempts_since_checkpoint = 0

    def after_attempt(_receipt):
        nonlocal attempts_since_checkpoint
        attempts_since_checkpoint += 1
        if attempts_since_checkpoint == checkpoint_every:
            checkpoint()

    try:
        check_current()
        # One original DirectEstateI03Session is opened only for the explicit
        # saved-estate opt-in. ExitStack closes it even on failed/deferred
        # units or CURRENT refusal; legacy default behavior is unchanged.
        with ExitStack() as stack:
            if reuse_prepared_saved_session:
                check_current()
                prepared_admission = PreparedSavedC11Admission.from_verified_admission(saved)
                prepared_session = stack.enter_context(prepared_admission.prepared_i03())
                check_current()
            runner.run(executors={k: ExecutorBinding(executor_ref(k), execute) for k in ("QUERY", "DISCOVERY")},
                       max_units=max_units,
                       after_attempt=after_attempt if checkpoint_observer is not None else None)
            # Publish the final attempted prefix even if some units failed.
            # The unbounded run still refuses incomplete success below.
            if checkpoint_observer is not None and attempts_since_checkpoint:
                checkpoint()
            check_current()
        # Coverage is determined by the incumbent Batch owner's latest attempt
        # per unit, not by the cardinality or state of the immutable history.
        # A successful retry must preserve FAILED/DEFERRED attempts.
        summary = runner.summary()
        if max_units is None and not summary.full_coverage:
            raise NativeWorkloadExecutionError("NATIVE_EXECUTION_INCOMPLETE_SEE_RECEIPTS")
        result = snapshot()
    finally:
        if owned_group_scope is not None:
            owned_group_scope.close()
    return result


JOINED_CUSTODY_SCHEMA = "PRE553_R04_JOINED_WORKLOAD_CUSTODY@2.0.0"


@dataclass(frozen=True)
class WorkloadCustodyEntry:
    decision_ref: ExactRef
    envelope_sha256: str
    source_sha256: str
    manifest_hash: str
    kind: str
    state: str
    unit_materials: tuple[Mapping[str, Any], ...]
    completed_outputs: Mapping[str, Mapping[str, Any]]
    receipt_materials: tuple[Mapping[str, Any], ...]
    output_refs: tuple[ExactRef, ...]
    entry_hash: str

    def material(self) -> dict[str, Any]:
        return {
            "decision_ref": self.decision_ref.as_dict(),
            "envelope_sha256": self.envelope_sha256,
            "source_sha256": self.source_sha256,
            "manifest_hash": self.manifest_hash,
            "kind": self.kind, "state": self.state,
            "unit_materials": [material(row) for row in self.unit_materials],
            "completed_outputs": {
                key: material(row) for key, row in self.completed_outputs.items()
            },
            "receipt_materials": [material(row) for row in self.receipt_materials],
            "output_refs": [ref.as_dict() for ref in self.output_refs],
            "entry_hash": self.entry_hash,
        }


@dataclass(frozen=True)
class JoinedWorkloadCheckpoint:
    schema: str
    entries: tuple[WorkloadCustodyEntry, ...]
    checkpoint_hash: str
    # Optional exact saved-estate binding.  It is omitted from material() and
    # the content hash for legacy source-based checkpoints, preserving their
    # existing schema/hash semantics.
    saved_binding: SavedBindingReceipt | None = None

    def material(self) -> dict[str, Any]:
        material_payload = {
            "schema": self.schema,
            "entries": [entry.material() for entry in self.entries],
            "checkpoint_hash": self.checkpoint_hash,
        }
        if self.saved_binding is not None:
            material_payload["saved_binding"] = self.saved_binding.as_dict()
        return material_payload

    @property
    def completed_decision_refs(self) -> tuple[ExactRef, ...]:
        return tuple(entry.decision_ref for entry in self.entries)


@dataclass(frozen=True)
class JoinedWorkloadResumeResult:
    checkpoint: JoinedWorkloadCheckpoint
    completed_results: tuple[Any, ...]
    resumed_results: tuple[Any, ...]
    output_refs: tuple[ExactRef, ...]
    receipt_materials: tuple[Mapping[str, Any], ...]

    @property
    def all_results(self) -> tuple[Any, ...]:
        return (*self.completed_results, *self.resumed_results)


def _unit_material(unit: BatchUnitSpec) -> dict[str, Any]:
    return {
        "job_kind": unit.job_kind, "job_ref": unit.job_ref.as_dict(),
        "release_refs": [ref.as_dict() for ref in unit.release_refs],
        "semantic_input_refs": [ref.as_dict() for ref in unit.semantic_input_refs],
    }


def _restore_manifest(rows: Sequence[Mapping[str, Any]]) -> BatchManifest:
    return BatchManifest(tuple(
        BatchUnitSpec(
            row["job_kind"], exact_ref(row["job_ref"]),
            tuple(exact_ref(ref) for ref in row["release_refs"]),
            tuple(exact_ref(ref) for ref in row.get("semantic_input_refs", ())),
        ) for row in rows
    ))


def _restore_receipt(row: Mapping[str, Any]) -> UnitExecutionReceipt:
    return UnitExecutionReceipt(
        manifest_hash=row["manifest_hash"], unit_ref=exact_ref(row["unit_ref"]),
        attempt_index=row["attempt_index"], state=row["state"],
        execution_performed=row["execution_performed"],
        executor_ref=None if row["executor_ref"] is None else exact_ref(row["executor_ref"]),
        result_refs=tuple(exact_ref(ref) for ref in row["result_refs"]),
        provenance_refs=tuple(exact_ref(ref) for ref in row["provenance_refs"]),
        failure_code=row["failure_code"], detail_hash=row["detail_hash"],
    )


def _restore_fact(row: Mapping[str, Any]) -> EmpiricalFact:
    semantic = dict(row["semantic_fields"])
    return EmpiricalFact(
        typed_state=row["typed_state"],
        authority_snapshot_refs=tuple(row["authority_snapshot_refs"]),
        dependency_refs=tuple(row["dependency_refs"]),
        producer_replay_locator_or_reference_root=row["producer_replay_locator_or_reference_root"],
        object_id=row["object_id"], content_hash=row["content_hash"],
        schema_id=row["schema_id"], schema_version=row["schema_version"],
        **semantic,
    )


@dataclass(frozen=True)
class RetainedDiscoveryResultView:
    contract_id: str
    discovery_authority_ref: ExactRef
    candidate_grammar_ref: ExactRef
    evaluated_frontier_ref: ExactRef
    coverage_claim: str
    candidate_count: int
    covered_candidate_count: int
    receipts: tuple[DiscoveryResultReceipt, ...]
    empirical_fact_refs: tuple[ExactRef, ...]
    empirical_facts: tuple[EmpiricalFact, ...]
    executed_predicate_refs: tuple[ExactRef, ...]
    executed_query_refs: tuple[ExactRef, ...]
    valid_empty: bool
    replay_ref: ExactRef

    def __post_init__(self) -> None:
        if tuple(sorted(self.receipts, key=lambda row: row.ref.key)) != self.receipts:
            raise WorkloadAdmissionError("RETAINED_DISCOVERY_RECEIPT_ORDER_INVALID")
        if tuple(sorted(self.empirical_fact_refs, key=lambda ref: ref.key)) != self.empirical_fact_refs:
            raise WorkloadAdmissionError("RETAINED_DISCOVERY_FACT_REF_ORDER_INVALID")
        if tuple(f.ref for f in self.empirical_facts) != self.empirical_fact_refs:
            raise WorkloadAdmissionError("RETAINED_DISCOVERY_FACT_CLOSURE_INVALID")
        if tuple(sorted(self.executed_predicate_refs, key=lambda ref: ref.key)) != self.executed_predicate_refs:
            raise WorkloadAdmissionError("RETAINED_DISCOVERY_PREDICATE_ORDER_INVALID")
        if tuple(sorted(self.executed_query_refs, key=lambda ref: ref.key)) != self.executed_query_refs:
            raise WorkloadAdmissionError("RETAINED_DISCOVERY_QUERY_ORDER_INVALID")


def _restore_discovery_receipt(row: Mapping[str, Any]) -> DiscoveryResultReceipt:
    semantic = dict(row["semantic_fields"])
    return DiscoveryResultReceipt(
        typed_state=row["typed_state"],
        authority_snapshot_refs=tuple(row["authority_snapshot_refs"]),
        dependency_refs=tuple(row["dependency_refs"]),
        producer_replay_locator_or_reference_root=row["producer_replay_locator_or_reference_root"],
        object_id=row["object_id"], content_hash=row["content_hash"],
        schema_id=row["schema_id"], schema_version=row["schema_version"],
        **semantic,
    )


def _restore_output_material(row: Mapping[str, Any]) -> Any:
    if row["kind"] == "QUERY":
        facts = tuple(sorted(
            (_restore_fact(fact) for fact in row["facts"]),
            key=lambda fact: fact.ref.key,
        ))
        return QueryExecutionResult(
            query_ref=exact_ref(row["query_ref"]), facts=facts,
            source_scope_mode=row["source_scope_mode"],
            release_refs=tuple(sorted(
                (exact_ref(ref) for ref in row["release_refs"]),
                key=lambda ref: ref.key,
            )),
        )
    if row["kind"] == "DISCOVERY":
        facts = tuple(sorted(
            (_restore_fact(fact) for fact in row["empirical_facts"]),
            key=lambda fact: fact.ref.key,
        ))
        receipts = tuple(sorted(
            (_restore_discovery_receipt(receipt) for receipt in row["receipts"]),
            key=lambda receipt: receipt.ref.key,
        ))
        return RetainedDiscoveryResultView(
            contract_id=row["contract_id"],
            discovery_authority_ref=exact_ref(row["discovery_authority_ref"]),
            candidate_grammar_ref=exact_ref(row["candidate_grammar_ref"]),
            evaluated_frontier_ref=exact_ref(row["evaluated_frontier_ref"]),
            coverage_claim=row["coverage_claim"],
            candidate_count=row["candidate_count"],
            covered_candidate_count=row["covered_candidate_count"],
            receipts=receipts,
            empirical_fact_refs=tuple(sorted(
                (exact_ref(ref) for ref in row["empirical_fact_refs"]),
                key=lambda ref: ref.key,
            )),
            empirical_facts=facts,
            executed_predicate_refs=tuple(sorted(
                (exact_ref(ref) for ref in row.get("executed_predicate_refs", ())),
                key=lambda ref: ref.key,
            )),
            executed_query_refs=tuple(sorted(
                (exact_ref(ref) for ref in row.get("executed_query_refs", ())),
                key=lambda ref: ref.key,
            )),
            valid_empty=row["valid_empty"],
            replay_ref=exact_ref(row["replay_ref"]),
        )
    raise WorkloadAdmissionError("UNKNOWN_RETAINED_OUTPUT_KIND")


def _discovery_result_material(result: Any) -> dict[str, Any]:
    return {
        "kind": "DISCOVERY",
        "contract_id": result.contract_id,
        "discovery_authority_ref": result.discovery_authority_ref.as_dict(),
        "candidate_grammar_ref": result.candidate_grammar_ref.as_dict(),
        "evaluated_frontier_ref": result.evaluated_frontier_ref.as_dict(),
        "coverage_claim": result.coverage_claim,
        "candidate_count": result.candidate_count,
        "covered_candidate_count": result.covered_candidate_count,
        "receipts": [receipt.as_dict() for receipt in result.receipts],
        "empirical_fact_refs": [ref.as_dict() for ref in result.empirical_fact_refs],
        "empirical_facts": [fact.as_dict() for fact in result.empirical_facts],
        "executed_predicate_refs": [p.ref.as_dict() for p in result.executed_predicates],
        "executed_query_refs": [q.ref.as_dict() for q in result.executed_queries],
        "valid_empty": result.valid_empty,
        "replay_ref": result.replay_ref.as_dict(),
    }


def _result_output_material(result: Any) -> dict[str, Mapping[str, Any]]:
    if getattr(result, "native_result", None) is not None:
        unit_hash = result.manifest.units[0].unit_hash
        return {unit_hash: _discovery_result_material(result.native_result)}
    outputs = getattr(result, "outputs_by_unit", None) or {}
    mapped = {}
    for unit_hash, output in outputs.items():
        if hasattr(output, "query_ref") and hasattr(output, "facts"):
            mapped[unit_hash] = {
                "kind": "QUERY",
                "query_ref": output.query_ref.as_dict(),
                "facts": [fact.as_dict() for fact in output.facts],
                "source_scope_mode": output.source_scope_mode,
                "release_refs": [ref.as_dict() for ref in output.release_refs],
            }
        elif hasattr(output, "receipts") and hasattr(output, "executed_queries"):
            mapped[unit_hash] = _discovery_result_material(output)
        else:
            raise WorkloadAdmissionError("UNKNOWN_NATIVE_OUTPUT_KIND")
    return mapped


def _validate_prior_cache(manifest: BatchManifest, prior_receipts, prior_outputs) -> None:
    """Refuse caller/checkpoint prior outputs that do not match their receipts.

    The native Batch owner verifies receipt structure. This closes the cache
    content boundary: a completed prior unit may be skipped only when the
    supplied native output has exactly the receipt's result refs. A different
    value cannot be injected under a valid receipt.
    """
    unit_by_hash = {unit.unit_hash: unit for unit in manifest.units}
    unit_by_ref = {unit.unit_ref.key: unit for unit in manifest.units}
    if not set(prior_outputs) <= set(unit_by_hash):
        raise WorkloadAdmissionError("PRIOR_OUTPUT_UNKNOWN_UNIT")
    completed_by_unit = {}
    for receipt in prior_receipts:
        unit = unit_by_ref.get(receipt.unit_ref.key)
        if unit is not None and receipt.state == "COMPLETED":
            completed_by_unit[unit.unit_hash] = receipt
    if any(
        unit_hash not in completed_by_unit for unit_hash in prior_outputs
    ):
        raise WorkloadAdmissionError("PRIOR_OUTPUT_WITHOUT_COMPLETED_RECEIPT")
    for receipt in prior_receipts:
        unit = unit_by_ref.get(receipt.unit_ref.key)
        if unit is None:
            raise WorkloadAdmissionError("PRIOR_RECEIPT_UNKNOWN_UNIT")
        if receipt.manifest_hash != manifest.manifest_hash:
            raise WorkloadAdmissionError("PRIOR_RECEIPT_MANIFEST_MISMATCH")
        if receipt.state != "COMPLETED":
            continue
        output = prior_outputs.get(unit.unit_hash)
        if output is None:
            raise WorkloadAdmissionError("PRIOR_OUTPUT_MISSING")
        if unit.job_kind == "QUERY":
            facts = getattr(output, "facts", None)
            if facts is None:
                raise WorkloadAdmissionError("PRIOR_OUTPUT_KIND_MISMATCH")
            expected = tuple(fact.ref for fact in facts)
        elif unit.job_kind == "DISCOVERY":
            receipts = getattr(output, "receipts", None)
            if receipts is None:
                raise WorkloadAdmissionError("PRIOR_OUTPUT_KIND_MISMATCH")
            expected = tuple(item.ref for item in receipts)
        else:
            raise WorkloadAdmissionError("PRIOR_OUTPUT_KIND_MISMATCH")
        if Counter(expected) != Counter(receipt.result_refs):
            raise WorkloadAdmissionError("PRIOR_OUTPUT_RECEIPT_MISMATCH")


def _entry_payload(entry: WorkloadCustodyEntry) -> dict[str, Any]:
    """Exact content-addressed entry preimage (excludes the entry hash itself)."""
    return {
        "decision_ref": entry.decision_ref.as_dict(),
        "envelope_sha256": entry.envelope_sha256,
        "source_sha256": entry.source_sha256,
        "manifest_hash": entry.manifest_hash,
        "kind": entry.kind, "state": entry.state,
        "unit_materials": [material(row) for row in entry.unit_materials],
        "completed_outputs": {
            key: material(row) for key, row in entry.completed_outputs.items()
        },
        "receipt_materials": [material(row) for row in entry.receipt_materials],
        "output_refs": [ref.as_dict() for ref in entry.output_refs],
    }


def _checkpoint_content_hash(checkpoint: JoinedWorkloadCheckpoint) -> str:
    """Content address of the complete checkpoint, independent of the claimed pin."""
    payload = {
        "schema": checkpoint.schema,
        "entries": [entry.material() for entry in checkpoint.entries],
    }
    if checkpoint.saved_binding is not None:
        payload["saved_binding"] = checkpoint.saved_binding.as_dict()
    return semantic_hash(payload)


def _validate_entry_material(entry: WorkloadCustodyEntry) -> None:
    """Refuse a corrupt, orphaned or internally inconsistent checkpoint entry.

    This is a material/structure check only. It deliberately does not
    reconstruct native empirical outputs; ``_validate_entry_outputs`` performs
    that parse only after the caller has established current authority. It
    never treats a stored permission field as current authority.
    """
    if not isinstance(entry, WorkloadCustodyEntry):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_REQUIRED")
    if entry.kind not in {"WORKLOAD", "DISCOVERY"}:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_KIND_INVALID")
    if entry.state not in {"COMPLETED", "PARTIAL"}:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_STATE_INVALID")
    if entry.kind == "DISCOVERY" and entry.state != "COMPLETED":
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_DISCOVERY_STATE_INVALID")
    for value in (entry.envelope_sha256, entry.source_sha256, entry.manifest_hash):
        if (not isinstance(value, str) or len(value) != 64
                or any(char not in "0123456789abcdef" for char in value.lower())):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_HASH_INVALID")
    try:
        if entry.entry_hash != semantic_hash(_entry_payload(entry)):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_HASH_MISMATCH")
        manifest = _restore_manifest(entry.unit_materials)
        receipts = tuple(_restore_receipt(row) for row in entry.receipt_materials)
        if manifest.manifest_hash != entry.manifest_hash:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_MANIFEST_MISMATCH")
        if entry.kind == "DISCOVERY" and any(
            unit.job_kind != "DISCOVERY" for unit in manifest.units
        ):
            raise WorkloadAdmissionError(
                "JOINED_CHECKPOINT_DISCOVERY_MANIFEST_MISMATCH"
            )
        if any(receipt.manifest_hash != manifest.manifest_hash for receipt in receipts):
            raise WorkloadAdmissionError(
                "JOINED_CHECKPOINT_RECEIPT_MANIFEST_MISMATCH"
            )
        unit_keys = {unit.unit_ref.key for unit in manifest.units}
        receipt_keys = [receipt.unit_ref.key for receipt in receipts]
        if len(receipt_keys) != len(set(receipt_keys)) or not set(receipt_keys) <= unit_keys:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_RECEIPT_UNIT_MISMATCH")
        completed_keys = {
            receipt.unit_ref.key for receipt in receipts
            if receipt.state == "COMPLETED"
        }
        expected_outputs = {
            unit.unit_hash for unit in manifest.units
            if unit.unit_ref.key in completed_keys
        }
        if set(entry.completed_outputs) != expected_outputs:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_OUTPUT_CLOSURE_MISMATCH")
        if entry.state == "COMPLETED" and (
            set(receipt_keys) != unit_keys or completed_keys != unit_keys
        ):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_COMPLETED_PREFIX_INCOMPLETE")
        if entry.state == "PARTIAL" and not completed_keys:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_EMPTY_PREFIX")
        expected_refs = tuple(sorted(
            (ref for receipt in receipts for ref in receipt.result_refs),
            key=lambda ref: ref.key,
        ))
        if entry.output_refs != expected_refs:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_OUTPUT_REF_MISMATCH")
    except WorkloadAdmissionError:
        raise
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_MATERIAL_INVALID") from exc


def _canonical_refs(values) -> tuple[ExactRef, ...]:
    refs = [
        value if isinstance(value, ExactRef) else exact_ref(value)
        for value in values
    ]
    return tuple(sorted(refs, key=lambda ref: ref.key))


def _discovery_frontier_replay(output: Any) -> ExactRef:
    """Recompute the I05 frontier replay ref from the retained view fields.

    This mirrors the existing I05 derivation; it is a consistency check, not a
    new receipt issuer or authority root.
    """
    digest = semantic_hash({
        "contract": output.contract_id,
        "frontier_ref": output.evaluated_frontier_ref.as_dict(),
        "receipt_refs": [receipt.ref.as_dict() for receipt in output.receipts],
        "fact_refs": [ref.as_dict() for ref in output.empirical_fact_refs],
        "valid_empty": output.valid_empty,
    })
    return ExactRef(
        "PRE553_I05_FRONTIER_REPLAY",
        "urn:rawlsing:pre553:i05:frontier-replay:sha256:" + digest,
        digest,
    )


def _validate_entry_outputs(
    entry: WorkloadCustodyEntry, *, workload: NativeWorkload | None = None,
) -> None:
    """Reconstruct retained native outputs and bind them to their native units.

    This is the protected-payload parse. Callers invoke it only after current
    authority has been established, so a revoked/replaced decision cannot
    cause a retained empirical output to be reconstructed or served. It binds
    the whole retained output identity, not only the fact/receipt refs:
    query_ref, release refs, source-scope mode, fact query/predicate refs,
    discovery authority/frontier/grammar/release/executed-ref closure and the
    I05 frontier replay ref. A different native value or a different per-unit
    identity cannot ride under a valid unit receipt.
    """
    if not isinstance(entry, WorkloadCustodyEntry):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_REQUIRED")
    try:
        manifest = _restore_manifest(entry.unit_materials)
        receipts = tuple(_restore_receipt(row) for row in entry.receipt_materials)
        if workload is not None:
            expected_queries = {
                request.query_ref.key: request for request in workload.requests
            }
            expected_discoveries = {ref.key for ref in workload.discoveries}
            for unit in manifest.units:
                input_keys = {ref.key for ref in unit.semantic_input_refs}
                if workload.decision_ref.key not in input_keys:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DECISION_MISMATCH"
                    )
                if unit.job_kind == "QUERY":
                    request = expected_queries.get(unit.job_ref.key)
                    if request is None:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_UNIT_MISMATCH"
                        )
                    if request.predicate_ref.key not in input_keys:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_PREDICATE_MISMATCH"
                        )
                elif unit.job_kind == "DISCOVERY":
                    if unit.job_ref.key not in expected_discoveries:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_UNIT_MISMATCH"
                        )
                else:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_KIND_MISMATCH"
                    )
            if entry.state == "COMPLETED" and len(manifest.units) != (
                len(expected_queries) + len(expected_discoveries)
            ):
                raise WorkloadAdmissionError(
                    "JOINED_CHECKPOINT_OUTPUT_UNIT_CLOSURE_MISMATCH"
                )
        unit_by_hash = {unit.unit_hash: unit for unit in manifest.units}
        receipt_by_unit = {receipt.unit_ref.key: receipt for receipt in receipts}
        for unit_hash, row in entry.completed_outputs.items():
            unit = unit_by_hash.get(unit_hash)
            if unit is None:
                raise WorkloadAdmissionError("JOINED_CHECKPOINT_OUTPUT_UNIT_MISMATCH")
            receipt = receipt_by_unit.get(unit.unit_ref.key)
            if receipt is None or receipt.state != "COMPLETED":
                raise WorkloadAdmissionError(
                    "JOINED_CHECKPOINT_OUTPUT_RECEIPT_MISMATCH"
                )
            output = _restore_output_material(row)
            if unit.job_kind == "QUERY":
                if row.get("kind") != "QUERY" or not hasattr(output, "facts"):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_KIND_MISMATCH"
                    )
                if output.query_ref != unit.job_ref:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_QUERY_MISMATCH"
                    )
                if _canonical_refs(output.release_refs) != _canonical_refs(unit.release_refs):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_RELEASE_MISMATCH"
                    )
                if workload is not None:
                    query = workload.catalog.resolve_query_exact(unit.job_ref)
                    grain = query.requested_output_grain
                    expected_mode = (
                        grain.get("source_scope_mode")
                        if isinstance(grain, Mapping) else None
                    )
                    if (expected_mode is not None
                            and output.source_scope_mode != expected_mode):
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_SCOPE_MODE_MISMATCH"
                        )
                request = (
                    expected_queries.get(unit.job_ref.key)
                    if workload is not None else None
                )
                unit_input_keys = {
                    ref.key for ref in unit.semantic_input_refs
                }
                for fact in output.facts:
                    if exact_ref(
                        fact.empirical_query_spec_ref, "empirical_query_spec_ref"
                    ) != unit.job_ref:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_QUERY_MISMATCH"
                        )
                    fact_predicate = exact_ref(
                        fact.condition_predicate_ref, "condition_predicate_ref"
                    )
                    if request is not None:
                        if fact_predicate != request.predicate_ref:
                            raise WorkloadAdmissionError(
                                "JOINED_CHECKPOINT_OUTPUT_PREDICATE_MISMATCH"
                            )
                    elif fact_predicate.key not in unit_input_keys:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_PREDICATE_MISMATCH"
                        )
                refs = tuple(fact.ref for fact in output.facts)
            elif unit.job_kind == "DISCOVERY":
                if row.get("kind") != "DISCOVERY" or not hasattr(output, "receipts"):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_KIND_MISMATCH"
                    )
                if output.discovery_authority_ref != unit.job_ref:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_AUTHORITY_MISMATCH"
                    )
                if (output.contract_id != I05_CONTRACT_ID
                        or output.coverage_claim != COVERAGE_CLAIM):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_CONTRACT_MISMATCH"
                    )
                if (output.candidate_count != output.covered_candidate_count
                        or output.candidate_count != len(output.receipts)):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_COUNT_MISMATCH"
                    )
                if output.valid_empty != (
                    not output.receipts
                    or all(item.typed_state == "VALID_EMPTY"
                           for item in output.receipts)
                ):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_EMPTY_MISMATCH"
                    )
                if output.replay_ref != _discovery_frontier_replay(output):
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_REPLAY_MISMATCH"
                    )
                if workload is not None:
                    authority = workload.catalog.resolve_discovery_authority_exact(
                        unit.job_ref
                    )
                    if output.candidate_grammar_ref != exact_ref(
                        authority.candidate_grammar_ref
                    ):
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_GRAMMAR_MISMATCH"
                        )
                fact_union = set()
                query_union = set()
                predicate_union = set()
                for item in output.receipts:
                    if exact_ref(
                        item.discovery_authority_ref, "discovery_authority_ref"
                    ) != unit.job_ref:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_AUTHORITY_MISMATCH"
                        )
                    if exact_ref(
                        item.evaluated_frontier_ref, "evaluated_frontier_ref"
                    ) != output.evaluated_frontier_ref:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_FRONTIER_MISMATCH"
                        )
                    if output.candidate_grammar_ref.key not in {
                        exact_ref(ref).key for ref in item.dependency_refs
                    }:
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_GRAMMAR_MISMATCH"
                        )
                    if _canonical_refs(item.source_release_refs) != _canonical_refs(
                        unit.release_refs
                    ):
                        raise WorkloadAdmissionError(
                            "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_RELEASE_MISMATCH"
                        )
                    fact_union.update(
                        exact_ref(ref).key for ref in item.empirical_fact_refs
                    )
                    for role in item.candidate_identity.get("query_roles", ()):
                        query_union.add(exact_ref(role["query_ref"], "query_ref").key)
                        predicate_union.add(
                            exact_ref(role["predicate_ref"], "predicate_ref").key
                        )
                if fact_union != {ref.key for ref in output.empirical_fact_refs}:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_FACT_MISMATCH"
                    )
                if query_union != {ref.key for ref in output.executed_query_refs}:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_QUERY_MISMATCH"
                    )
                if predicate_union != {
                    ref.key for ref in output.executed_predicate_refs
                }:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_PREDICATE_MISMATCH"
                    )
                refs = tuple(item.ref for item in output.receipts)
            else:
                raise WorkloadAdmissionError(
                    "JOINED_CHECKPOINT_OUTPUT_KIND_MISMATCH"
                )
            if Counter(refs) != Counter(receipt.result_refs):
                raise WorkloadAdmissionError(
                    "JOINED_CHECKPOINT_OUTPUT_RECEIPT_MISMATCH"
                )
    except WorkloadAdmissionError:
        raise
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_MATERIAL_INVALID") from exc


def capture_joined_checkpoint(
    results: Sequence[Any], *,
    source_sha256_by_decision: Mapping[str, str] | None = None,
    saved_binding: SavedBindingReceipt | None = None,
) -> JoinedWorkloadCheckpoint:
    """Capture completed or real partial prefix with native output facts retained."""
    entries = []
    for result in results:
        is_discovery = getattr(result, "native_result", None) is not None
        manifest = getattr(result, "manifest", None)
        receipts = tuple(getattr(result, "receipts", ()))
        if manifest is None or not receipts:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_NATIVE_RESULT_REQUIRED")
        by_unit = {}
        for receipt in receipts:
            if receipt.unit_ref.key in by_unit:
                raise WorkloadAdmissionError("JOINED_CHECKPOINT_DUPLICATE_UNIT")
            by_unit[receipt.unit_ref.key] = receipt
        completed = {unit.unit_ref.key: by_unit.get(unit.unit_ref.key)
                     for unit in manifest.units}
        if is_discovery:
            state = "COMPLETED"
        else:
            if not completed or not any(receipt is not None for receipt in completed.values()):
                raise WorkloadAdmissionError("JOINED_CHECKPOINT_EMPTY_PREFIX")
            state = ("COMPLETED" if all(
                receipt is not None and receipt.state == "COMPLETED"
                for receipt in completed.values()) else "PARTIAL")
        output_refs = tuple(sorted(
            (ref for receipt in receipts for ref in receipt.result_refs),
            key=lambda ref: ref.key,
        ))
        entry_payload = {
            "decision_ref": result.decision_ref.as_dict(),
            "envelope_sha256": result.envelope_sha256,
            "source_sha256": (
                getattr(result, "source_sha256", None)
                or (source_sha256_by_decision or {}).get(result.decision_ref.key, "")
            ),
            "manifest_hash": manifest.manifest_hash,
            "kind": "DISCOVERY" if is_discovery else "WORKLOAD",
            "state": state,
            "unit_materials": [_unit_material(unit) for unit in manifest.units],
            "completed_outputs": _result_output_material(result),
            "receipt_materials": [material(receipt) for receipt in receipts],
            "output_refs": [ref.as_dict() for ref in output_refs],
        }
        entry = WorkloadCustodyEntry(
            decision_ref=result.decision_ref,
            envelope_sha256=result.envelope_sha256,
            source_sha256=(
                getattr(result, "source_sha256", None)
                or (source_sha256_by_decision or {}).get(result.decision_ref.key, "")
            ),
            manifest_hash=manifest.manifest_hash,
            kind=entry_payload["kind"], state=state,
            unit_materials=tuple(entry_payload["unit_materials"]),
            completed_outputs=entry_payload["completed_outputs"],
            receipt_materials=tuple(entry_payload["receipt_materials"]),
            output_refs=output_refs,
            entry_hash=semantic_hash(entry_payload),
        )
        _validate_entry_material(entry)
        _validate_entry_outputs(entry)
        entries.append(entry)
    ordered = tuple(sorted(entries, key=lambda entry: entry.decision_ref.key))
    if len({entry.decision_ref.key for entry in ordered}) != len(ordered):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_DUPLICATE_DECISION")
    if saved_binding is not None and type(saved_binding) is not SavedBindingReceipt:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_SAVED_BINDING_INVALID")
    payload = {"schema": JOINED_CUSTODY_SCHEMA,
               "entries": [entry.material() for entry in ordered]}
    if saved_binding is not None:
        payload["saved_binding"] = saved_binding.as_dict()
    return JoinedWorkloadCheckpoint(
        schema=JOINED_CUSTODY_SCHEMA, entries=ordered,
        checkpoint_hash=semantic_hash(payload), saved_binding=saved_binding,
    )


def _restore_saved_binding(value: Any) -> SavedBindingReceipt:
    """Restore the exact saved-estate binding from checkpoint material."""
    if not isinstance(value, Mapping):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_SAVED_BINDING_REQUIRED")
    try:
        i02_raw = value["i02"]
        if not isinstance(i02_raw, Mapping):
            raise TypeError("i02 not mapping")
        i02 = ExternalI02Roots(**dict(i02_raw))
        binding = SavedBindingReceipt(
            schema=value["schema"],
            manifest_sha256=value["manifest_sha256"],
            i02=i02,
            release_ref=exact_ref(value["release_ref"], "saved_binding.release_ref"),
            estate_path=value["estate_path"],
            runtime_catalog=dict(value["runtime_catalog"]),
            source_opens=value.get("source_opens", 0),
            full_c11_repository_builds=value.get("full_c11_repository_builds", 0),
            full_c11_logical_release_builds=value.get(
                "full_c11_logical_release_builds", 0
            ),
            persistent_body_corpora=value.get("persistent_body_corpora", 0),
            counter_status=value.get(
                "counter_status", "DECLARED_ZERO__NOT_A_MEASUREMENT"
            ),
        )
    except WorkloadAdmissionError:
        raise
    except Exception as exc:
        raise WorkloadAdmissionError(
            "JOINED_CHECKPOINT_SAVED_BINDING_INVALID"
        ) from exc
    return binding


def restore_joined_checkpoint(
    material_payload: Mapping[str, Any], *, expected_checkpoint_ref: str | None = None,
    current_guard: Callable[[tuple[ExactRef, ...]], None] | None = None,
) -> JoinedWorkloadCheckpoint:
    """Rehydrate a joined checkpoint and require the original external pin.

    This helper restores custody material, not native empirical outputs when
    no current guard is supplied: ``_validate_entry_material`` validates
    hashes/manifest/receipt structure but deliberately does not call
    ``_restore_output_material``. The protected payload parse then happens in
    ``resume_joined_workloads`` only after it has admitted the current decision.
    ``current_guard`` remains an optional early-refusal hook for callers that
    own an independent resolver; it runs after the pin/hash checks and before
    any entry material is parsed. When it is supplied and succeeds, the helper
    also performs the full output/receipt binding check. It is not a permission
    cache, and omitting it cannot cause a protected output restore because this
    function does not perform one without it.
    """
    if not isinstance(expected_checkpoint_ref, str) or not expected_checkpoint_ref:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_EXPECTED_PIN_REQUIRED")
    if not isinstance(material_payload, Mapping):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_MATERIAL_REQUIRED")
    payload = dict(material_payload)
    if payload.get("schema") != JOINED_CUSTODY_SCHEMA:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_SCHEMA_MISMATCH")
    claimed = payload.get("checkpoint_hash")
    entries_material = payload.get("entries", ())
    if not isinstance(entries_material, (list, tuple)):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRIES_INVALID")
    if any(not isinstance(row, Mapping) for row in entries_material):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRIES_INVALID")
    computed_payload = {
        "schema": payload.get("schema"),
        "entries": [dict(row) for row in entries_material],
    }
    saved_binding_material = payload.get("saved_binding")
    saved_binding = (
        _restore_saved_binding(saved_binding_material)
        if saved_binding_material is not None else None
    )
    if saved_binding_material is not None:
        computed_payload["saved_binding"] = dict(saved_binding_material)
    if claimed != semantic_hash(computed_payload):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_HASH_MISMATCH")
    if claimed != expected_checkpoint_ref:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_PIN_MISMATCH")
    if current_guard is not None:
        if not callable(current_guard):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_CURRENT_GUARD_INVALID")
        try:
            decision_refs = tuple(
                exact_ref(row["decision_ref"]) for row in entries_material
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_MATERIAL_INVALID") from exc
        try:
            current_guard(decision_refs)
        except WorkloadAdmissionError:
            raise
        except Exception as exc:
            raise WorkloadAdmissionError(
                "JOINED_CHECKPOINT_CURRENT_GUARD_REFUSED"
            ) from exc
    entries = []
    try:
        for row in entries_material:
            entry_payload = {
                "decision_ref": row["decision_ref"],
                "envelope_sha256": row["envelope_sha256"],
                "source_sha256": row["source_sha256"],
                "manifest_hash": row["manifest_hash"],
                "kind": row["kind"], "state": row["state"],
                "unit_materials": row["unit_materials"],
                "completed_outputs": row["completed_outputs"],
                "receipt_materials": row["receipt_materials"],
                "output_refs": row["output_refs"],
            }
            if row.get("entry_hash") != semantic_hash(entry_payload):
                raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_HASH_MISMATCH")
            restored_units = _restore_manifest(row["unit_materials"])
            if restored_units.manifest_hash != row["manifest_hash"]:
                raise WorkloadAdmissionError("JOINED_CHECKPOINT_MANIFEST_MISMATCH")
            entry = WorkloadCustodyEntry(
                decision_ref=exact_ref(row["decision_ref"]),
                envelope_sha256=row["envelope_sha256"],
                source_sha256=row["source_sha256"],
                manifest_hash=row["manifest_hash"],
                kind=row["kind"], state=row["state"],
                unit_materials=tuple(dict(item) for item in row["unit_materials"]),
                completed_outputs={
                    key: dict(item) for key, item in row["completed_outputs"].items()
                },
                receipt_materials=tuple(dict(item) for item in row["receipt_materials"]),
                output_refs=tuple(exact_ref(ref) for ref in row["output_refs"]),
                entry_hash=row["entry_hash"],
            )
            _validate_entry_material(entry)
            if current_guard is not None:
                # The guard has already established current authority above;
                # only now may a guarded cold restore parse protected output.
                _validate_entry_outputs(entry)
            entries.append(entry)
    except WorkloadAdmissionError:
        raise
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_MATERIAL_INVALID") from exc
    return JoinedWorkloadCheckpoint(
        schema=payload["schema"], entries=tuple(entries),
        checkpoint_hash=claimed, saved_binding=saved_binding,
    )


def _completed_entry_view(entry: WorkloadCustodyEntry, scope: str) -> Any:
    manifest = _restore_manifest(entry.unit_materials)
    receipts = tuple(_restore_receipt(row) for row in entry.receipt_materials)
    outputs = {
        unit_hash: _restore_output_material(row)
        for unit_hash, row in entry.completed_outputs.items()
    }
    if entry.kind == "DISCOVERY":
        if len(outputs) != 1:
            raise WorkloadAdmissionError("RETAINED_DISCOVERY_OUTPUT_COUNT_INVALID")
        native_result = next(iter(outputs.values()))
        return SimpleNamespace(
            native_result=native_result, manifest=manifest, receipts=receipts,
            envelope_sha256=entry.envelope_sha256,
            decision_ref=entry.decision_ref, scope=scope,
            source_sha256=entry.source_sha256,
        )
    return NativeWorkloadResult(
        route_results=(), native_outputs=tuple(outputs[key] for key in sorted(outputs)),
        manifest=manifest, receipts=receipts, output_refs=entry.output_refs,
        envelope_sha256=entry.envelope_sha256, decision_ref=entry.decision_ref,
        scope=scope, summary=None, source_sha256=entry.source_sha256,
        outputs_by_unit=outputs,
    )


def resume_joined_workloads(
    *,
    workloads: Sequence[Any],
    resolver: CurrentDecisionResolver,
    source_factory: Callable[[ExactRef], Any] | None = None,
    saved_admission_factory: Callable[[], SavedC11Admission] | None = None,
    host: str,
    purpose: str,
    checkpoint: JoinedWorkloadCheckpoint,
    expected_checkpoint_ref: str | None = None,
    allow_test_only: bool = False,
) -> JoinedWorkloadResumeResult:
    """Resume actual R03-issued workloads under one independent current issuer.

    The resolver is required for every fate. No historical ``item.record``,
    checkpoint field or retained permission is used as current authority. The
    first admission happens before entry branching, protected result
    restoration, ``source_factory`` or native execution. Completed results are
    rechecked twice: before restore and immediately before serve.
    """
    resolver = _require_current_resolver(resolver)
    if not isinstance(checkpoint, JoinedWorkloadCheckpoint):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_REQUIRED")
    if checkpoint.schema != JOINED_CUSTODY_SCHEMA:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_SCHEMA_MISMATCH")
    if saved_admission_factory is not None:
        if not callable(saved_admission_factory):
            raise WorkloadAdmissionError("SAVED_ADMISSION_FACTORY_INVALID")
        if checkpoint.saved_binding is None:
            raise WorkloadAdmissionError(
                "SAVED_CHECKPOINT_BINDING_REQUIRED"
            )
    elif checkpoint.saved_binding is not None:
        raise WorkloadAdmissionError(
            "SAVED_CHECKPOINT_REQUIRES_SAVED_ADMISSION"
        )
    if source_factory is None and saved_admission_factory is None:
        raise WorkloadAdmissionError("SOURCE_OR_SAVED_ADMISSION_REQUIRED")
    if not isinstance(checkpoint.entries, tuple) or any(
        not isinstance(entry, WorkloadCustodyEntry) for entry in checkpoint.entries
    ):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_REQUIRED")
    # Recompute the content address from the entries before trusting the
    # claimed hash or the caller-supplied pin. A mutated in-memory checkpoint
    # that retained its old hash is refused before any resolver/source read.
    try:
        computed_checkpoint_hash = _checkpoint_content_hash(checkpoint)
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_MATERIAL_INVALID") from exc
    if computed_checkpoint_hash != checkpoint.checkpoint_hash:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_HASH_MISMATCH")
    if expected_checkpoint_ref is None or checkpoint.checkpoint_hash != expected_checkpoint_ref:
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_PIN_MISMATCH")
    items = tuple(workloads)
    by_decision: dict[str, Any] = {}
    for item in items:
        workload = getattr(item, "workload", None)
        historical = getattr(item, "record", None)
        if not isinstance(workload, NativeWorkload):
            raise WorkloadAdmissionError("EXACT_NATIVE_WORKLOAD_REQUIRED")
        if not isinstance(historical, IssuedWorkloadRecord):
            raise WorkloadAdmissionError("HISTORICAL_ISSUED_RECORD_REQUIRED")
        if historical.decision_ref != workload.decision_ref:
            raise WorkloadAdmissionError("JOINED_WORKLOAD_RECORD_DECISION_MISMATCH")
        if historical.envelope_sha256 != semantic_hash(workload.envelope()):
            raise WorkloadAdmissionError("JOINED_WORKLOAD_HISTORICAL_ENVELOPE_MISMATCH")
        if historical.source_sha256 != workload.projection.expected_source_sha256:
            raise WorkloadAdmissionError("JOINED_WORKLOAD_HISTORICAL_SOURCE_MISMATCH")
        key = workload.decision_ref.key
        if key in by_decision:
            raise WorkloadAdmissionError("JOINED_WORKLOAD_DUPLICATE_DECISION")
        by_decision[key] = item
    completed_entries = {entry.decision_ref.key: entry for entry in checkpoint.entries}
    if len(completed_entries) != len(checkpoint.entries):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_DUPLICATE_DECISION")
    if not set(completed_entries) <= set(by_decision):
        raise WorkloadAdmissionError("JOINED_CHECKPOINT_UNKNOWN_WORKLOAD")
    # Metadata-only shape check before the first external read. Full native
    # material validation happens after current admission, so a revoked
    # decision cannot cause a protected payload restore.
    for entry in checkpoint.entries:
        if not isinstance(entry, WorkloadCustodyEntry):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_ENTRY_REQUIRED")
        if entry.kind not in {"WORKLOAD", "DISCOVERY"}:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_KIND_INVALID")
        if entry.state not in {"COMPLETED", "PARTIAL"}:
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_STATE_INVALID")

    def current_for(item: Any) -> IssuedWorkloadRecord:
        return admit(
            item.workload, resolver, host=host, purpose=purpose,
            allow_test_only=allow_test_only,
            expected_wave=item.workload.original_wave_identity,
        )

    def require_unchanged(item: Any, expected: IssuedWorkloadRecord, code: str) -> None:
        if current_for(item) != expected:
            raise WorkloadAdmissionError(code)

    completed_results: list[Any] = []
    resumed_results: list[Any] = []
    current_by_key: dict[str, IssuedWorkloadRecord] = {}
    for item in items:
        workload = item.workload
        # Required for every fate, including COMPLETED and ABSENT, before any
        # checkpoint material is restored or a source factory can be called.
        current_record = current_for(item)
        key = workload.decision_ref.key
        current_by_key[key] = current_record
        entry = completed_entries.get(key)
        if entry is None:
            if saved_admission_factory is not None:
                saved = saved_admission_factory()
                if type(saved) is not SavedC11Admission:
                    raise WorkloadAdmissionError("EXACT_SAVED_C11_ADMISSION_REQUIRED")
                if saved.binding_receipt() != checkpoint.saved_binding:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_SAVED_BINDING_MISMATCH"
                    )
                if saved.source_ref.content_hash != current_record.source_sha256:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_SAVED_SOURCE_MISMATCH"
                    )
                saved_factory = lambda saved=saved: saved
                resumed_results.append(execute_issued_workload(
                    workload, resolver, source_factory=None,
                    saved_admission_factory=saved_factory,
                    host=host, purpose=purpose, allow_test_only=allow_test_only,
                    expected_wave=workload.original_wave_identity,
                ))
            else:
                resumed_results.append(execute_issued_workload(
                    workload, resolver, source_factory=source_factory,
                    host=host, purpose=purpose, allow_test_only=allow_test_only,
                    expected_wave=workload.original_wave_identity,
                ))
            continue
        if (entry.envelope_sha256 != current_record.envelope_sha256
                or entry.source_sha256 != current_record.source_sha256
                or entry.decision_ref != current_record.decision_ref):
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_WORKLOAD_IDENTITY_MISMATCH")
        if entry.state == "COMPLETED":
            require_unchanged(
                item, current_record, "ISSUER_SNAPSHOT_CHANGED_BEFORE_RESTORE"
            )
            if saved_admission_factory is not None:
                saved = saved_admission_factory()
                if type(saved) is not SavedC11Admission:
                    raise WorkloadAdmissionError("EXACT_SAVED_C11_ADMISSION_REQUIRED")
                if saved.binding_receipt() != checkpoint.saved_binding:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_SAVED_BINDING_MISMATCH"
                    )
                if saved.source_ref.content_hash != current_record.source_sha256:
                    raise WorkloadAdmissionError(
                        "JOINED_CHECKPOINT_SAVED_SOURCE_MISMATCH"
                    )
            # Current authority is established immediately above. Only now may
            # the checkpoint's native material be parsed and validated.
            _validate_entry_material(entry)
            _validate_entry_outputs(entry, workload=workload)
            view = _completed_entry_view(entry, current_record.scope)
            require_unchanged(
                item, current_record, "ISSUER_SNAPSHOT_CHANGED_BEFORE_SERVE"
            )
            completed_results.append(view)
            continue
        if entry.state != "PARTIAL":
            raise WorkloadAdmissionError("JOINED_CHECKPOINT_STATE_INVALID")
        require_unchanged(
            item, current_record, "ISSUER_SNAPSHOT_CHANGED_BEFORE_RESTORE"
        )
        # The exact saved binding/type/source check MUST precede any protected
        # entry/output parse or restore in the PARTIAL branch.  This mirrors the
        # COMPLETED branch and prevents a coherently rehashed forged checkpoint
        # from causing retained-output restoration before refusal.
        saved = None
        if saved_admission_factory is not None:
            saved = saved_admission_factory()
            if type(saved) is not SavedC11Admission:
                raise WorkloadAdmissionError("EXACT_SAVED_C11_ADMISSION_REQUIRED")
            if saved.binding_receipt() != checkpoint.saved_binding:
                raise WorkloadAdmissionError(
                    "JOINED_CHECKPOINT_SAVED_BINDING_MISMATCH"
                )
            if saved.source_ref.content_hash != current_record.source_sha256:
                raise WorkloadAdmissionError(
                    "JOINED_CHECKPOINT_SAVED_SOURCE_MISMATCH"
                )
            # The estate open/current callback must not invalidate the exact
            # CURRENT record established before the protected parse.
            require_unchanged(
                item, current_record,
                "ISSUER_SNAPSHOT_CHANGED_AFTER_SAVED_BINDING",
            )
        _validate_entry_material(entry)
        _validate_entry_outputs(entry, workload=workload)
        prior_receipts = tuple(_restore_receipt(row) for row in entry.receipt_materials)
        prior_outputs = {
            unit_hash: _restore_output_material(row)
            for unit_hash, row in entry.completed_outputs.items()
        }
        if saved is not None:
            saved_factory = lambda saved=saved: saved
            resumed_results.append(execute_issued_workload(
                workload, resolver, source_factory=None,
                saved_admission_factory=saved_factory,
                host=host, purpose=purpose, allow_test_only=allow_test_only,
                prior_receipts=prior_receipts, prior_outputs=prior_outputs,
                expected_wave=workload.original_wave_identity,
            ))
        else:
            resumed_results.append(execute_issued_workload(
                workload, resolver, source_factory=source_factory,
                host=host, purpose=purpose, allow_test_only=allow_test_only,
                prior_receipts=prior_receipts, prior_outputs=prior_outputs,
                expected_wave=workload.original_wave_identity,
            ))
    # One final read for every item, after all native work and immediately
    # before publication. A change affecting an earlier completed result
    # still aborts the whole return.
    for item in items:
        require_unchanged(
            item, current_by_key[item.workload.decision_ref.key],
            "ISSUER_SNAPSHOT_CHANGED_BEFORE_PUBLICATION",
        )
    all_results = tuple(completed_results + resumed_results)
    output_refs = tuple(sorted(
        {ref for result in all_results for receipt in result.receipts
         for ref in receipt.result_refs},
        key=lambda ref: ref.key,
    ))
    receipt_materials = tuple(
        material(receipt) for result in all_results for receipt in result.receipts
    )
    return JoinedWorkloadResumeResult(
        checkpoint=checkpoint, completed_results=tuple(completed_results),
        resumed_results=tuple(resumed_results), output_refs=output_refs,
        receipt_materials=receipt_materials,
    )
