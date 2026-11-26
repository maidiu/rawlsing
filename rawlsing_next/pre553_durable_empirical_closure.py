"""S2-F durable complete empirical result closure adapter.

This module owns an isolated, versioned, content-addressed durability seam for
already-produced native PRE553 I03/I05 output.  It is deliberately *not* a new
scientific engine, authority issuer, C11 release, or statistical model.

Contract (frozen S2-F v1):
``2d7517456846d41c06b5bf0355b79626142b5608db90a546e7252831ae3e2716``

What it does
------------
* Publishes the *complete* exact native output closure: EmpiricalFact (including
  every typed negative/held fact), I05 DiscoveryResultReceipt, the constitutive
  query/predicate objects, exact authority snapshots, source/release/replay refs
  and the fact/receipt/frontier replay preimages.
* Factors repeated large preimages with the sourcefree FIABC canonical fragment
  primitives in ``pre553_durable_empirical_fragments``.
* Publishes once into a versioned content-addressed CAS with an atomic staged
  manifest rename.  A failed publication leaves no visible closure and never
  overwrites an existing closure identity.
* Reconstructs the exact native objects in a fresh process without source
  access, re-materializing each public object under its own constructor identity
  law.
* Hands the reconstructed M01 graph to the *actual existing* M1 composer
  ``pre553_learned_world_composition.build_m1_bundle_from_m01`` and an actual
  descriptive Field Forge consumer
  ``field_forge_conditional_support.produce_exact_conditional_support_profile``.

What it deliberately does not do
--------------------------------
* It never constructs a ``C11LogicalRelease`` (that remains an I02 validation
  monopoly) and never opens original source bytes.
* It never manufactures a ``CURRENT`` authority, a production issuer, or a new
  scientific claim.  The historical authority preimages are replay material
  only.
* It never "repairs" a coherently rewritten closure: trust requires an external
  root pin captured outside the closure directory.  A self-hashed manifest that
  is not externally pinned is reported as ``UNPINNED_SELF_HASH`` and refused by
  every trusted consumer entrypoint.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import shutil
import time
from typing import Any, Iterable, Mapping, Sequence
import uuid
import zlib

from rawlsing_next._pre553_query_common import (
    QUERY_EXECUTION_CONTRACT_ID,
    QueryExecutionResult,
)
from rawlsing_next.pre553_carrier_execution import materialize_public_object
from rawlsing_next.pre553_discovery_exact import (
    I05_CONTRACT_ID,
    ExactBoundedDiscoveryResult,
)
from rawlsing_next.pre553_durable_empirical_fragments import (
    DurableFragmentError,
    FRAGMENT_MARKER,
    fragment_map_from_entries,
    hydrate_canonical_preimage,
    pack_canonical_preimage,
)
from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    CanonicalSemanticObject,
    DiscoveryAuthority,
    DiscoveryResultReceipt,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    STATE_FAMILIES,
    canonicalize,
    canonical_json,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_route_b_production import (
    RouteBEmpiricalObjectGraph,
    RouteBProductionResult,
)


DURABLE_CLOSURE_CONTRACT_ID = (
    "PYAT_S2F_DURABLE_COMPLETE_EMPIRICAL_RESULT_CLOSURE@1.0.0"
)
DURABLE_CLOSURE_SCHEMA = "PYAT_S2F_DURABLE_EMPIRICAL_CLOSURE_MANIFEST@1.0.0"
# Explicit envelope extension inside the existing content-addressed container.
# Legacy one-frontier bytes and roots remain unchanged. A v1-only reader
# cannot parse the null singular field, so it fails closed on the new shape.
NATIVE_DISCOVERY_ENVELOPE_V2 = "PYAT_S2F_NATIVE_DISCOVERY_SET@2"
DURABLE_ROOT_SCHEMA = "PYAT_S2F_DURABLE_EMPIRICAL_CLOSURE_ROOT@1.0.0"
DURABLE_CLOSURE_CONTRACT_SHA = (
    "2d7517456846d41c06b5bf0355b79626142b5608db90a546e7252831ae3e2716"
)
EVIDENCE_GRADE = "S2_SOURCEFREE_ISOLATED_FIXTURE"
RIGHTS_STATE = "HISTORICAL_REPLAY_ONLY__NO_CURRENT_AUTHORITY_MINTED"
SOURCE_ACCESS_STATE = "DISABLED__NO_ORIGINAL_SOURCE_BYTES_RETAINED"
BLOB_FORMAT = "canonical-json+deflate-9"
BLOB_SUFFIX = ".json.z"
MANIFEST_NAME = "manifest.json"
# Optional physical transport for the same canonical manifest and root.
# Legacy readers fail closed; no second copy of the logical manifest.
COMPACT_MANIFEST_NAME = "manifest.v1.json.z"
# Larger legitimate manifests retain the plain transport. This is a
# bounded compressed decoder, not a limit on the analytical query grammar.
MAX_COMPACT_MANIFEST_RAW = 256 * 1024 * 1024
CAS_DIR = "cas"
BLOB_DIR = "blobs"
CLOSURES_DIR = "closures"
STAGING_PREFIX = ".staging-"
_LARGE_FRAGMENT_FIELDS = (
    "risk_set_member_refs",
    "denominator_member_refs",
    "complete_cells",
)

CONSERVED_FACT_STATES = tuple(sorted(STATE_FAMILIES["EMPIRICAL_FACT_STATE"]))
CONSERVED_RECEIPT_STATES = tuple(sorted(STATE_FAMILIES["DISCOVERY_RESULT_STATE"]))
POSITIVE_FACT_STATES = frozenset({"SUPPORTED", "OBSERVED_ZERO"})


class DurableEmpiricalClosureError(Pre553IntegrityError):
    """The durable closure is absent, corrupt, unpinned, or semantically inconsistent."""


class DurableEmpiricalClosureUntrusted(DurableEmpiricalClosureError):
    """A closure that is internally coherent has no independent external pin."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DurableEmpiricalClosureError(f"{name} must be a non-empty string")
    return value.strip()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise DurableEmpiricalClosureError(f"{name} must be an exact mapping")
    return value


def _sequence(value: Any, name: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise DurableEmpiricalClosureError(f"{name} must be a sequence")
    return value


def _exact(value: Any, name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Pre553IntegrityError as exc:
        raise DurableEmpiricalClosureError(str(exc)) from exc


def _refs(values: Iterable[Any], name: str) -> tuple[ExactRef, ...]:
    return tuple(sorted({_exact(value, name) for value in values}, key=lambda r: r.key))


def _canonical_bytes(value: Any) -> bytes:
    return canonical_json(value).encode("utf-8")


def _compress(value: Any) -> tuple[bytes, bytes]:
    raw = _canonical_bytes(value)
    return raw, zlib.compress(raw, 9)


def _decompress(blob: bytes) -> Any:
    import json

    return json.loads(zlib.decompress(blob).decode("utf-8"))


def _fsync_dir(path: Path) -> None:
    if not path.is_dir():
        return
    try:
        fd = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _cleanup_stale_publish_artifacts(root: Path) -> None:
    """Remove staging/tmp leftovers from dead publishers only.

    Content-addressed final blobs are never removed.  A live concurrent
    publisher keeps its own staging/tmp names because the embedded pid resolves
    as alive.  Legacy UUID-only blob temp names (``.tmp-<uuid>`` from the
    pre-repair publisher) carry no liveness marker and are deliberately left
    untouched rather than guessed at; only publisher-generated
    ``.tmp-<pid>-<uuid>`` names are attributable and cleanable.
    """

    blob_dir = root / CAS_DIR / BLOB_DIR
    closures_dir = root / CLOSURES_DIR
    for path in blob_dir.glob(".*.tmp-*"):
        tail = path.name.rsplit(".tmp-", 1)
        if len(tail) != 2:
            continue
        try:
            pid = int(tail[1].split("-", 1)[0])
        except ValueError:
            continue
        if not _pid_alive(pid):
            try:
                path.unlink()
            except OSError:
                pass
    for path in closures_dir.glob(f"{STAGING_PREFIX}*"):
        tail = path.name[len(STAGING_PREFIX):]
        try:
            pid = int(tail.split("-", 1)[0])
        except ValueError:
            continue
        if not _pid_alive(pid):
            shutil.rmtree(path, ignore_errors=True)


@dataclass(frozen=True)
class ReleaseIdentity:
    """Exact source-release identity retained by the closure (never raw rows)."""

    release_ref: ExactRef
    replay_ref: ExactRef
    source_artifact_ref: ExactRef | None = None
    source_release_manifest_hash: str | None = None
    semantic_release_hash: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "release_ref", _exact(self.release_ref, "release_ref"))
        object.__setattr__(self, "replay_ref", _exact(self.replay_ref, "replay_ref"))
        if self.source_artifact_ref is not None:
            object.__setattr__(
                self,
                "source_artifact_ref",
                _exact(self.source_artifact_ref, "source_artifact_ref"),
            )
        for name in ("source_release_manifest_hash", "semantic_release_hash"):
            value = getattr(self, name)
            if value is not None:
                _text(value, name)
                if len(value) != 64:
                    raise DurableEmpiricalClosureError(f"{name} must be sha256")

    def as_dict(self) -> dict[str, Any]:
        return {
            "release_ref": self.release_ref.as_dict(),
            "replay_ref": self.replay_ref.as_dict(),
            "source_artifact_ref": (
                None
                if self.source_artifact_ref is None
                else self.source_artifact_ref.as_dict()
            ),
            "source_release_manifest_hash": self.source_release_manifest_hash,
            "semantic_release_hash": self.semantic_release_hash,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ReleaseIdentity":
        item = _mapping(value, "release identity")
        return cls(
            release_ref=item.get("release_ref"),
            replay_ref=item.get("replay_ref"),
            source_artifact_ref=item.get("source_artifact_ref"),
            source_release_manifest_hash=item.get("source_release_manifest_hash"),
            semantic_release_hash=item.get("semantic_release_hash"),
        )


@dataclass(frozen=True)
class DurableReleaseRefView:
    """A non-authoritative release ref view.

    It deliberately is not a ``C11LogicalRelease``: constructing that type is an
    I02 validation monopoly.  The existing M1 adapter only dereferences
    ``c11_release.release_ref``, and no source access is available through this
    object.
    """

    release_ref: ExactRef

    def __post_init__(self) -> None:
        object.__setattr__(self, "release_ref", _exact(self.release_ref, "release_ref"))


@dataclass(frozen=True)
class DurableM01ReplayView:
    """The exact reconstructed M1 graph plus a release-ref-only C11 view."""

    object_graph: RouteBEmpiricalObjectGraph
    c11_release: DurableReleaseRefView
    rights_state: str = RIGHTS_STATE


@dataclass(frozen=True)
class NativeEmpiricalOutput:
    """Complete native output handed to the closure publisher.

    This is a *view* over already-produced native I03/I05 output.  It contains no
    source bytes and no repository handle.  ``from_route_b_result`` intentionally
    drops the live executor binding.
    """

    source_identity: Mapping[str, Any]
    release_identities: tuple[ReleaseIdentity, ...]
    i03_results: tuple[QueryExecutionResult, ...]
    i05_result: ExactBoundedDiscoveryResult | None
    object_graph: RouteBEmpiricalObjectGraph
    typed_states: Mapping[str, Any] | None = None
    learned_empirical_execution_receipt: Mapping[str, Any] | None = None
    replay_receipt_identity: str | None = None
    replay_receipt_header: Mapping[str, Any] | None = None
    native_result_identity: str | None = None
    i05_results: tuple[ExactBoundedDiscoveryResult, ...] = ()

    @property
    def discovery_results(self) -> tuple[ExactBoundedDiscoveryResult, ...]:
        return (self.i05_result,) if self.i05_result is not None else self.i05_results

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "source_identity", canonicalize(_mapping(self.source_identity, "source_identity"))
        )
        releases = tuple(self.release_identities)
        if not releases:
            raise DurableEmpiricalClosureError(
                "at least one exact release identity is required"
            )
        if not all(isinstance(item, ReleaseIdentity) for item in releases):
            raise DurableEmpiricalClosureError("release identities must be exact")
        object.__setattr__(
            self,
            "release_identities",
            tuple(sorted(releases, key=lambda item: item.release_ref.key)),
        )
        if self.i05_result is not None and (
            not isinstance(self.i05_result, ExactBoundedDiscoveryResult)
            or self.i05_results
        ):
            raise DurableEmpiricalClosureError("ambiguous singular/plural I05 envelope")
        if type(self.i05_results) is not tuple or not all(
            type(item) is ExactBoundedDiscoveryResult for item in self.i05_results
        ):
            raise DurableEmpiricalClosureError("exact native I05 tuple required")
        ordered = tuple(sorted(self.i05_results, key=lambda item: item.discovery_authority_ref.key))
        if len({item.discovery_authority_ref for item in ordered}) != len(ordered):
            raise DurableEmpiricalClosureError("duplicate native discovery authority")
        object.__setattr__(self, "i05_results", ordered)
        if not isinstance(self.object_graph, RouteBEmpiricalObjectGraph):
            raise DurableEmpiricalClosureError(
                "exact RouteBEmpiricalObjectGraph is required"
            )
        results = tuple(self.i03_results)
        if not all(isinstance(item, QueryExecutionResult) for item in results):
            raise DurableEmpiricalClosureError("i03_results must be exact query results")
        object.__setattr__(self, "i03_results", results)
        if self.typed_states is not None:
            object.__setattr__(self, "typed_states", canonicalize(self.typed_states))
        if self.learned_empirical_execution_receipt is not None:
            object.__setattr__(
                self,
                "learned_empirical_execution_receipt",
                canonicalize(self.learned_empirical_execution_receipt),
            )
        if self.replay_receipt_header is not None:
            object.__setattr__(
                self,
                "replay_receipt_header",
                canonicalize(self.replay_receipt_header),
            )
        for name in ("replay_receipt_identity", "native_result_identity"):
            value = getattr(self, name)
            if value is not None:
                _text(value, name)
                if len(value) != 64:
                    raise DurableEmpiricalClosureError(f"{name} must be sha256")

    @classmethod
    def from_route_b_result(cls, result: RouteBProductionResult) -> "NativeEmpiricalOutput":
        if not isinstance(result, RouteBProductionResult):
            raise DurableEmpiricalClosureError(
                "exact RouteBProductionResult is required"
            )
        release = result.c11_release
        identity = ReleaseIdentity(
            release_ref=release.release_ref,
            replay_ref=release.replay_manifest.ref,
            source_artifact_ref=release.source_artifact_ref,
            source_release_manifest_hash=release.source_release_manifest_hash,
            semantic_release_hash=release.semantic_release_hash,
        )
        header = {
            key: value
            for key, value in result.replay_receipt.items()
            if key not in {"object_preimages", "receipt_identity"}
        }
        return cls(
            source_identity=result.source_identity,
            release_identities=(identity,),
            i03_results=result.i03_results,
            i05_result=result.i05_result,
            object_graph=result.object_graph,
            typed_states=result.replay_receipt.get("typed_states"),
            learned_empirical_execution_receipt=(
                result.learned_empirical_execution_receipt
            ),
            replay_receipt_identity=result.replay_receipt.get("receipt_identity"),
            replay_receipt_header=header,
            native_result_identity=result.replay_receipt.get("dependency_root"),
        )

    def release_by_ref(self) -> Mapping[str, ReleaseIdentity]:
        return {item.release_ref.key: item for item in self.release_identities}


@dataclass(frozen=True)
class PublishReceipt:
    root_path: str
    closure_identity: str
    root_identity: str
    published: bool
    object_count: int
    fragment_count: int
    blob_count: int
    fact_count: int
    receipt_count: int
    rows: Mapping[str, int]
    logical_evidence_bytes: int
    referenced_physical_bytes: int
    referenced_blob_bytes: int
    compressed_fragment_bytes: int
    manifest_bytes: int
    peak_scratch_bytes: int
    cas_new_bytes: int
    source_open_count: int
    dedup_ratio: float
    evidence_grade: str = EVIDENCE_GRADE
    rights_state: str = RIGHTS_STATE

    def as_dict(self) -> dict[str, Any]:
        return {
            "root_path": self.root_path,
            "closure_identity": self.closure_identity,
            "root_identity": self.root_identity,
            "published": self.published,
            "object_count": self.object_count,
            "fragment_count": self.fragment_count,
            "blob_count": self.blob_count,
            "fact_count": self.fact_count,
            "receipt_count": self.receipt_count,
            "rows": dict(self.rows),
            "logical_evidence_bytes": self.logical_evidence_bytes,
            "referenced_physical_bytes": self.referenced_physical_bytes,
            "referenced_blob_bytes": self.referenced_blob_bytes,
            "compressed_fragment_bytes": self.compressed_fragment_bytes,
            "manifest_bytes": self.manifest_bytes,
            "peak_scratch_bytes": self.peak_scratch_bytes,
            "cas_new_bytes": self.cas_new_bytes,
            "source_open_count": self.source_open_count,
            "dedup_ratio": self.dedup_ratio,
            "evidence_grade": self.evidence_grade,
            "rights_state": self.rights_state,
        }


def _domain_identity(query: EmpiricalQuerySpec) -> tuple[str, dict[str, Any]]:
    """Recompute the exact ``_TargetPlan.domain_identity`` without executing I03."""

    spec = _mapping(query.target_arity_and_topology, "target_arity_and_topology")
    target_refs = tuple(_exact(value, "target_ref") for value in query.target_refs)
    arity = spec.get("arity")
    if not isinstance(arity, int) or isinstance(arity, bool) or arity != len(target_refs):
        raise DurableEmpiricalClosureError("target arity/ref mismatch")
    order_semantics = spec.get("joint_order_semantics")
    components_raw = _sequence(spec.get("components"), "target components")
    if len(components_raw) != arity:
        raise DurableEmpiricalClosureError("target component count mismatch")
    components: list[dict[str, Any]] = []
    domains: list[tuple[Any, ...]] = []
    for raw, target_ref in zip(components_raw, target_refs):
        item = _mapping(raw, "target component")
        if _exact(item.get("target_ref"), "target component ref") != target_ref:
            raise DurableEmpiricalClosureError("target component exact ref mismatch")
        domain = tuple(canonicalize(value) for value in _sequence(item.get("domain", ()), "domain"))
        domains.append(domain)
        components.append(
            {
                "target_ref": target_ref.as_dict(),
                "topology": item.get("topology"),
                "domain": list(domain),
                "target_domain_replay_ref": _exact(
                    item.get("target_domain_replay_ref"), "target_domain_replay_ref"
                ).as_dict(),
            }
        )
    if any(not domain for domain in domains):
        full_domain: tuple[Any, ...] = ()
    elif arity == 1:
        full_domain = tuple(domains[0])
    else:
        explicit_joint = spec.get("joint_domain")
        if explicit_joint is not None:
            full_domain = tuple(canonicalize(v) for v in _sequence(explicit_joint, "joint_domain"))
        else:
            from itertools import product

            full_domain = tuple(
                canonicalize(list(values)) for values in product(*domains)
            )
    material = {
        "components": components,
        "joint_order_semantics": order_semantics,
        "full_domain": list(full_domain),
    }
    return semantic_hash(material), material


def _fact_release_refs(fact: EmpiricalFact) -> tuple[ExactRef, ...]:
    release_refs = _refs(
        (
            _exact(value, "fact provenance")
            for value in fact.source_empirical_provenance_refs
            if _exact(value, "fact provenance").kind == "C11LogicalRelease"
        ),
        "fact release refs",
    )
    if not release_refs:
        raise DurableEmpiricalClosureError("fact provenance omits its C11 release ref")
    return release_refs


def _positive_fact_replay_material(
    fact: EmpiricalFact,
    releases: Mapping[str, ReleaseIdentity],
) -> Mapping[str, Any] | None:
    """Exact replay preimage shape built by ``_build_fact``.

    Native I03 has two lawful fact shapes.  The positive/executed shape carries
    the complete target-cell projection and member refs; the typed-negated shape
    built by ``_build_negative_fact`` carries the requested topology and failure
    detail instead.  Both are native output and both must be conserved.
    """

    topology = _mapping(fact.target_topology, "fact.target_topology")
    cells = topology.get("complete_cell_semantic_projection")
    if cells is None:
        return None
    domain_identity = getattr(fact, "target_domain_identity", None)
    if domain_identity is None:
        return None
    release_refs = _fact_release_refs(fact)
    missing = [ref.key for ref in release_refs if ref.key not in releases]
    if missing:
        raise DurableEmpiricalClosureError(
            "fact provenance references a release outside the native output registry"
        )
    return {
        "contract": QUERY_EXECUTION_CONTRACT_ID,
        "query_ref": _exact(fact.empirical_query_spec_ref, "fact query").as_dict(),
        "predicate_ref": _exact(
            fact.condition_predicate_ref, "fact predicate"
        ).as_dict(),
        "release_refs": [ref.as_dict() for ref in release_refs],
        "release_replay_refs": [
            releases[ref.key].replay_ref.as_dict() for ref in release_refs
        ],
        "source_scope_mode": fact.source_scope_mode,
        "measure_kind": fact.measure_kind,
        "risk_set_type": fact.risk_set_type,
        "target_domain_identity": domain_identity,
        "risk_member_refs": [dict(value) for value in fact.risk_set_member_refs],
        "denominator_member_refs": [
            dict(value) for value in fact.denominator_member_refs
        ],
        "complete_cells": [dict(value) for value in cells],
    }


def _negative_fact_replay_material(
    fact: EmpiricalFact,
    releases: Mapping[str, ReleaseIdentity],
) -> Mapping[str, Any] | None:
    """Exact replay preimage shape built by ``_build_negative_fact``.

    The negative shape records the requested topology and the deterministic
    failure detail instead of a computed cell projection.  It is not a
    counts-only or result-only substitute: the exact universe/release refs,
    query/predicate identity, typed state and failure code are all retained.
    """

    topology = _mapping(fact.target_topology, "fact.target_topology")
    if "complete_cell_semantic_projection" in topology:
        return None
    p02_failure_state = getattr(fact, "p02_failure_state", None)
    detail = getattr(fact, "execution_detail", None)
    if not isinstance(p02_failure_state, str) or not isinstance(detail, str):
        return None
    release_refs = _fact_release_refs(fact)
    missing = [ref.key for ref in release_refs if ref.key not in releases]
    if missing:
        raise DurableEmpiricalClosureError(
            "fact provenance references a release outside the native output registry"
        )
    return {
        "contract": QUERY_EXECUTION_CONTRACT_ID,
        "query_ref": _exact(fact.empirical_query_spec_ref, "fact query").as_dict(),
        "predicate_ref": _exact(
            fact.condition_predicate_ref, "fact predicate"
        ).as_dict(),
        "source_scope_mode": fact.source_scope_mode,
        "universe_refs": [
            ref.as_dict()
            for ref in _refs(fact.empirical_universe_refs, "fact universe")
        ],
        "release_refs": [ref.as_dict() for ref in release_refs],
        "p01_state": fact.typed_state,
        "p02_failure_state": p02_failure_state,
        "detail": detail,
    }


def _fact_replay_material(
    fact: EmpiricalFact,
    releases: Mapping[str, ReleaseIdentity],
) -> Mapping[str, Any]:
    """Reconstruct the exact native replay preimage for either fact shape.

    Selection is by the native ``replay_ref`` identity, never by a guess.  If
    neither known native shape reproduces the fact's own replay hash the closure
    fails closed instead of storing an invented or approximate preimage.
    """

    replay_hash = _exact(fact.replay_ref, "fact replay").content_hash
    candidates: list[Mapping[str, Any]] = []
    for builder in (
        _positive_fact_replay_material,
        _negative_fact_replay_material,
    ):
        try:
            candidate = builder(fact, releases)
        except DurableEmpiricalClosureError:
            raise
        except Exception:
            candidate = None
        if candidate is not None:
            candidates.append(candidate)
    matches = [
        candidate for candidate in candidates if semantic_hash(candidate) == replay_hash
    ]
    if len(matches) != 1:
        raise DurableEmpiricalClosureError(
            "fact replay preimage cannot be reconstructed exactly from its retained fields"
        )
    return matches[0]


def _receipt_replay_material(
    receipt: DiscoveryResultReceipt,
    release_refs: Iterable[ExactRef],
) -> Mapping[str, Any]:
    identity = _mapping(receipt.candidate_identity, "receipt candidate_identity")
    fact_refs = _refs(receipt.empirical_fact_refs, "receipt empirical_fact_refs")
    receipts_release_refs = _refs(
        getattr(receipt, "source_release_refs", ()), "receipt source_release_refs"
    )
    declared = _refs(release_refs, "closure release refs")
    if receipts_release_refs:
        declared_keys = {ref.key for ref in declared}
        missing = [
            ref.key for ref in receipts_release_refs if ref.key not in declared_keys
        ]
        if missing:
            raise DurableEmpiricalClosureError(
                "receipt source release refs reference a release outside the closure"
            )
    else:
        receipts_release_refs = declared
    return {
        "contract": I05_CONTRACT_ID,
        "authority_ref": _exact(
            receipt.discovery_authority_ref, "receipt discovery authority"
        ).as_dict(),
        "frontier_ref": _exact(
            receipt.evaluated_frontier_ref, "receipt frontier"
        ).as_dict(),
        "candidate_id": _text(identity.get("candidate_id"), "candidate_id"),
        "candidate_hash": _text(identity.get("candidate_hash"), "candidate_hash"),
        "coverage_state": _text(receipt.coverage_state, "coverage_state"),
        "fact_refs": [ref.as_dict() for ref in fact_refs],
        "release_refs": [ref.as_dict() for ref in receipts_release_refs],
        "query_execution_contract": QUERY_EXECUTION_CONTRACT_ID,
    }


def _frontier_replay_material(
    receipts: Iterable[DiscoveryResultReceipt],
    i05: ExactBoundedDiscoveryResult,
) -> Mapping[str, Any]:
    identities = []
    for receipt in receipts:
        identity = _mapping(receipt.candidate_identity, "receipt candidate_identity")
        identities.append(
            {
                "candidate_id": _text(identity.get("candidate_id"), "candidate_id"),
                "candidate_hash": _text(identity.get("candidate_hash"), "candidate_hash"),
            }
        )
    identities.sort(key=lambda item: item["candidate_hash"])
    return {
        "contract": I05_CONTRACT_ID,
        "discovery_authority_ref": i05.discovery_authority_ref.as_dict(),
        "candidate_grammar_ref": i05.candidate_grammar_ref.as_dict(),
        "query_execution_contract": QUERY_EXECUTION_CONTRACT_ID,
        "candidate_identities": identities,
        "coverage_claim": i05.coverage_claim,
    }


def _final_replay_material(i05: ExactBoundedDiscoveryResult) -> Mapping[str, Any]:
    return {
        "contract": I05_CONTRACT_ID,
        "frontier_ref": i05.evaluated_frontier_ref.as_dict(),
        "receipt_refs": [receipt.ref.as_dict() for receipt in i05.receipts],
        "fact_refs": [ref.as_dict() for ref in i05.empirical_fact_refs],
        "valid_empty": i05.valid_empty,
    }


def _pack_replay_material(
    material: Mapping[str, Any],
    fragments: dict[str, Any],
) -> Mapping[str, Any]:
    """Deduplicate the large replay arrays against the same fragment map."""

    packed = dict(canonicalize(material))
    for name in _LARGE_FRAGMENT_FIELDS:
        if name in packed:
            from rawlsing_next.pre553_durable_empirical_fragments import store_fragment

            packed[name] = store_fragment(packed[name], fragments)
    return canonicalize(packed)


def _object_families(graph: RouteBEmpiricalObjectGraph) -> Mapping[str, tuple[CanonicalSemanticObject, ...]]:
    return {
        "authority_snapshots": graph.authority_snapshots,
        "executed_predicates": graph.executed_predicates,
        "executed_queries": graph.executed_queries,
        "empirical_facts": graph.empirical_facts,
        "discovery_authorities": graph.discovery_authorities,
        "discovery_receipts": graph.discovery_receipts,
    }


_EXPECTED_FAMILY_CLASS = {
    "authority_snapshots": AuthoritySnapshot,
    "executed_predicates": EmpiricalPredicate,
    "executed_queries": EmpiricalQuerySpec,
    "empirical_facts": EmpiricalFact,
    "discovery_authorities": DiscoveryAuthority,
    "discovery_receipts": DiscoveryResultReceipt,
}

_FAMILY_OBJECT_NAME = {
    "authority_snapshots": "AuthoritySnapshot@1.0.0",
    "executed_predicates": "EmpiricalPredicate@1.0.0",
    "executed_queries": "EmpiricalQuerySpec@1.0.0",
    "empirical_facts": "EmpiricalFact@1.0.0",
    "discovery_authorities": "DiscoveryAuthority@1.0.0",
    "discovery_receipts": "DiscoveryResultReceipt@1.0.0",
}


def _family_sort_key(family: str, obj: CanonicalSemanticObject) -> str:
    if family == "authority_snapshots":
        return obj.authority_ref.key
    return obj.ref.key


def _verify_output_graph(output: NativeEmpiricalOutput) -> None:
    graph = output.object_graph
    for family, objects in _object_families(graph).items():
        expected = _EXPECTED_FAMILY_CLASS[family]
        if not all(isinstance(obj, expected) for obj in objects):
            raise DurableEmpiricalClosureError(f"{family} contains a wrong object family")
        keys = [_family_sort_key(family, obj) for obj in objects]
        if keys != sorted(set(keys)):
            raise DurableEmpiricalClosureError(f"{family} is not canonical exact-ref sorted")
        for obj in objects:
            if semantic_hash(obj.semantic_projection()) != obj.content_hash:
                raise DurableEmpiricalClosureError(f"{family} contains identity-drifted object")
            if obj.ref.object_id != obj.object_id or obj.ref.content_hash != obj.content_hash:
                raise DurableEmpiricalClosureError(f"{family} contains ExactRef drift")

    authorities = {obj.authority_ref.key: obj for obj in graph.authority_snapshots}
    registry = AuthorityRegistry(graph.authority_snapshots)
    for family, objects in _object_families(graph).items():
        if family == "authority_snapshots":
            continue
        for obj in objects:
            try:
                validate_object_authority_closure(obj, registry)
            except Exception as exc:
                raise DurableEmpiricalClosureError(
                    f"{family} object authority closure cannot be satisfied: {exc}"
                ) from exc

    graph_keys = {
        family: {obj.ref.key for obj in objects}
        for family, objects in _object_families(graph).items()
    }

    # I03 result closure.
    for result in output.i03_results:
        if result.query_ref.key not in graph_keys["executed_queries"]:
            raise DurableEmpiricalClosureError("i03 result query is absent from the object graph")
        for fact in result.facts:
            if fact.ref.key not in graph_keys["empirical_facts"]:
                raise DurableEmpiricalClosureError("i03 result fact is absent from the object graph")

    # Each actual native I05 result retains its own frontier and replay.
    # In v2 neither absent discovery nor distinct frontiers are synthesized.
    referenced = {result.query_ref.key for result in output.i03_results} | {
        fact.ref.key for result in output.i03_results for fact in result.facts
    }
    actual_receipts = set()
    actual_discoveries = set()
    for i05 in output.discovery_results:
        if i05.discovery_authority_ref.key not in graph_keys["discovery_authorities"]:
            raise DurableEmpiricalClosureError("i05 discovery authority is absent")
        actual_discoveries.add(i05.discovery_authority_ref.key)
        for receipt in i05.receipts:
            if (receipt.ref.key not in graph_keys["discovery_receipts"]
                or receipt.ref.key in actual_receipts):
                raise DurableEmpiricalClosureError("i05 receipt absent or shared across frontiers")
            if (_exact(receipt.discovery_authority_ref, "receipt authority") != i05.discovery_authority_ref
                or _exact(receipt.evaluated_frontier_ref, "receipt frontier") != i05.evaluated_frontier_ref):
                raise DurableEmpiricalClosureError("i05 receipt frontier/authority mismatch")
            actual_receipts.add(receipt.ref.key)
        if tuple(f.ref for f in i05.empirical_facts) != i05.empirical_fact_refs:
            raise DurableEmpiricalClosureError("i05 fact envelope mismatch")
        for fact_ref in i05.empirical_fact_refs:
            if fact_ref.key not in graph_keys["empirical_facts"]:
                raise DurableEmpiricalClosureError("i05 fact is absent")
        for predicate in i05.executed_predicates:
            if predicate.ref.key not in graph_keys["executed_predicates"]:
                raise DurableEmpiricalClosureError("i05 predicate is absent")
        for query in i05.executed_queries:
            if query.ref.key not in graph_keys["executed_queries"]:
                raise DurableEmpiricalClosureError("i05 query is absent")
        if type(i05.valid_empty) is not bool or i05.valid_empty != all(
            receipt.typed_state == "VALID_EMPTY" for receipt in i05.receipts
        ):
            raise DurableEmpiricalClosureError("i05 valid_empty contradicts its receipt states")
        if i05.candidate_count != i05.covered_candidate_count or i05.candidate_count != len(i05.receipts):
            raise DurableEmpiricalClosureError("i05 candidate/receipt cardinality mismatch")
        referenced |= ({i05.discovery_authority_ref.key}
            | {r.ref.key for r in i05.receipts}
            | {r.key for r in i05.empirical_fact_refs}
            | {obj.ref.key for obj in i05.executed_predicates}
            | {obj.ref.key for obj in i05.executed_queries})
    if actual_receipts != graph_keys["discovery_receipts"] or actual_discoveries != graph_keys["discovery_authorities"]:
        raise DurableEmpiricalClosureError("unowned discovery object in closure")
    if not referenced.issubset(set().union(*graph_keys.values())):
        raise DurableEmpiricalClosureError("referenced native objects are not declared in the graph")


def _fact_rows(
    fact: EmpiricalFact,
    queries: Mapping[str, EmpiricalQuerySpec],
    predicates: Mapping[str, EmpiricalPredicate],
) -> dict[str, Any]:
    query = queries.get(_exact(fact.empirical_query_spec_ref, "fact query").key)
    if query is None:
        raise DurableEmpiricalClosureError("fact constitutive query preimage is absent")
    predicate = predicates.get(_exact(fact.condition_predicate_ref, "fact predicate").key)
    if predicate is None:
        raise DurableEmpiricalClosureError("fact constitutive predicate preimage is absent")
    if _exact(fact.condition_predicate_ref, "fact predicate") != _exact(
        query.condition_predicate_ref, "query predicate"
    ):
        raise DurableEmpiricalClosureError("fact/query condition predicate mismatch")
    fact_universes = _refs(fact.empirical_universe_refs, "fact universe")
    query_universes = _refs(query.empirical_universe_refs, "query universe")
    if not fact_universes or not set(fact_universes).issubset(set(query_universes)):
        raise DurableEmpiricalClosureError("fact/query source universe mismatch")
    provenance_universes = {
        ref.key
        for ref in _refs(
            fact.source_empirical_provenance_refs,
            "fact source provenance",
        )
        if ref.kind == "EmpiricalUniverse@1.0.0"
    }
    if any(ref.key not in provenance_universes for ref in fact_universes):
        raise DurableEmpiricalClosureError(
            "fact source universe is not retained in its exact provenance"
        )
    if _exact(fact.risk_set_ref, "fact risk") != _exact(query.risk_set_ref, "query risk"):
        raise DurableEmpiricalClosureError("fact/query risk identity mismatch")
    if _exact(fact.measure_basis_ref, "fact measure") != _exact(
        query.measure_basis_ref, "query measure"
    ):
        raise DurableEmpiricalClosureError("fact/query measure identity mismatch")

    topology = _mapping(fact.target_topology, "fact.target_topology")
    risk_members = _refs(
        getattr(fact, "risk_set_member_refs", ()), "risk members"
    )
    denominator_members = _refs(
        getattr(fact, "denominator_member_refs", ()), "denominator members"
    )
    if not set(denominator_members).issubset(set(risk_members)) and denominator_members:
        raise DurableEmpiricalClosureError("denominator members are not a subset of risk members")
    if len(denominator_members) != fact.raw_denominator_support:
        raise DurableEmpiricalClosureError(
            "raw denominator support disagrees with the retained exact member count"
        )
    cells = tuple(topology.get("complete_cell_semantic_projection", ()))
    has_positive_topology = (
        "complete_cell_semantic_projection" in topology
        and topology.get("target_domain_identity") is not None
        and getattr(fact, "target_domain_identity", None) is not None
    )
    if not has_positive_topology:
        # Native typed-negative facts are built by ``_build_negative_fact`` with
        # no risk/denominator member refs and exact zero support.  Requiring that
        # invariant prevents a re-hashed negative fact from silently carrying a
        # substituted count while retaining its nonpositive typed state.  A lawful
        # empty target domain is a *positive* topology with an empty cell
        # projection and is deliberately not treated as a negative fact.
        if risk_members or denominator_members:
            raise DurableEmpiricalClosureError(
                "typed negative fact cannot carry risk or denominator member refs"
            )
        if fact.raw_numerator_support != 0 or fact.raw_denominator_support != 0:
            raise DurableEmpiricalClosureError(
                "typed negative fact cannot carry nonzero support"
            )
    if _exact(
        fact.producer_replay_locator_or_reference_root, "fact replay root"
    ) != _exact(fact.replay_ref, "fact replay"):
        raise DurableEmpiricalClosureError(
            "fact producer replay root differs from its exact replay identity"
        )
    cell_raw = []
    for cell in cells:
        value = _mapping(cell, "fact target cell").get("raw_numerator_support")
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise DurableEmpiricalClosureError("cell raw support is not a nonnegative integer")
        cell_raw.append(value)
    if cells or has_positive_topology or fact.typed_state in POSITIVE_FACT_STATES:
        if sum(cell_raw) != fact.raw_numerator_support:
            raise DurableEmpiricalClosureError(
                "raw numerator support disagrees with the retained exact cell sum"
            )
        if fact.typed_state in POSITIVE_FACT_STATES and fact.raw_denominator_support <= 0:
            raise DurableEmpiricalClosureError("positive fact requires positive exact denominator")
        domain_identity, domain_material = _domain_identity(query)
        if getattr(fact, "target_domain_identity", None) != domain_identity:
            raise DurableEmpiricalClosureError(
                "fact target-domain identity does not match its constitutive query"
            )
        if topology.get("target_domain_identity") != domain_identity:
            raise DurableEmpiricalClosureError("fact target topology domain identity drift")
        if canonicalize(topology.get("joint_order_semantics")) != canonicalize(
            domain_material["joint_order_semantics"]
        ):
            raise DurableEmpiricalClosureError("fact joint order semantics drift")
        if len(cells) != len(domain_material["full_domain"]):
            raise DurableEmpiricalClosureError(
                "fact complete cell count disagrees with the constitutive query domain"
            )
    target_arity_raw = topology.get("arity")
    if (
        isinstance(target_arity_raw, int)
        and not isinstance(target_arity_raw, bool)
        and target_arity_raw >= 0
    ):
        target_arity = target_arity_raw
    else:
        requested = topology.get("requested_target_arity_and_topology")
        requested_arity = (
            requested.get("arity") if isinstance(requested, Mapping) else None
        )
        target_arity = (
            int(requested_arity)
            if isinstance(requested_arity, int)
            and not isinstance(requested_arity, bool)
            and requested_arity >= 0
            else 0
        )
    return {
        "ref": fact.ref.as_dict(),
        "typed_state": fact.typed_state,
        "measure_kind": fact.measure_kind,
        "source_scope_mode": fact.source_scope_mode,
        "risk_set_type": fact.risk_set_type,
        "target_arity": target_arity,
        "same_respondent_binding_semantics": predicate.same_respondent_binding_semantics,
        "raw_numerator_support": fact.raw_numerator_support,
        "raw_denominator_support": fact.raw_denominator_support,
        "risk_member_count": len(risk_members),
        "denominator_member_count": len(denominator_members),
        "cell_count": len(cells),
        "replay_ref": _exact(fact.replay_ref, "fact replay").as_dict(),
    }


def _receipt_rows(
    receipt: DiscoveryResultReceipt,
    facts: Mapping[str, EmpiricalFact],
    predicates: Mapping[str, EmpiricalPredicate],
    queries: Mapping[str, EmpiricalQuerySpec],
    discoveries: Mapping[str, DiscoveryAuthority],
    closure_release_refs: Iterable[ExactRef],
) -> dict[str, Any]:
    identity = _mapping(receipt.candidate_identity, "receipt candidate identity")
    discovery_ref = _exact(receipt.discovery_authority_ref, "receipt discovery authority")
    discovery = discoveries.get(discovery_ref.key)
    if discovery is None:
        raise DurableEmpiricalClosureError("receipt discovery authority preimage is absent")
    winning_ref = _exact(receipt.winning_predicate_ref, "receipt winning predicate")
    if winning_ref.key not in predicates:
        raise DurableEmpiricalClosureError("receipt winning predicate preimage is absent")
    role_rows = []
    for role in _sequence(identity.get("query_roles", ()), "receipt query roles"):
        role_item = _mapping(role, "receipt query role")
        predicate_ref = _exact(role_item.get("predicate_ref"), "role predicate")
        query_ref = _exact(role_item.get("query_ref"), "role query")
        predicate = predicates.get(predicate_ref.key)
        query = queries.get(query_ref.key)
        if predicate is None or query is None:
            raise DurableEmpiricalClosureError("receipt role preimage is absent")
        if _exact(query.condition_predicate_ref, "role query predicate") != predicate_ref:
            raise DurableEmpiricalClosureError("receipt role query/predicate binding mismatch")
        role_rows.append(
            {
                "role": _text(role_item.get("role"), "query role"),
                "predicate_ref": predicate_ref.as_dict(),
                "query_ref": query_ref.as_dict(),
                "predicate_hash": predicate.predicate_hash,
                "target_arity": int(query.target_arity_and_topology.get("arity", 0)),
            }
        )
    receipt_fact_refs = _refs(
        (
            *receipt.empirical_fact_refs,
            *getattr(receipt, "validation_fact_refs", ()),
        ),
        "receipt fact refs",
    )
    for fact_ref in receipt_fact_refs:
        if fact_ref.key not in facts:
            raise DurableEmpiricalClosureError("receipt empirical fact preimage is absent")
    declared_receipt_releases = _refs(
        getattr(receipt, "source_release_refs", ()),
        "receipt source release refs",
    )
    if not declared_receipt_releases:
        declared_receipt_releases = _refs(
            closure_release_refs, "closure release refs"
        )
    declared_keys = {ref.key for ref in declared_receipt_releases}
    for fact_ref in receipt_fact_refs:
        fact = facts[fact_ref.key]
        fact_release_keys = {
            ref.key
            for ref in _refs(
                fact.source_empirical_provenance_refs,
                "receipt fact source provenance",
            )
            if ref.kind == "C11LogicalRelease"
        }
        if not fact_release_keys.issubset(declared_keys):
            raise DurableEmpiricalClosureError(
                "receipt source release refs do not cover its owned facts"
            )
    required = {
        discovery_ref.key,
        _exact(receipt.evaluated_frontier_ref, "receipt frontier").key,
        winning_ref.key,
        *(ref.key for ref in _refs(receipt.empirical_fact_refs, "receipt fact refs")),
    }
    actual = {_exact(ref, "receipt dependency").key for ref in receipt.dependency_refs}
    if not required.issubset(actual):
        raise DurableEmpiricalClosureError("receipt dependency closure omits constitutive refs")
    grammar_ref = _exact(discovery.candidate_grammar_ref, "candidate grammar ref")
    if grammar_ref.key not in actual:
        raise DurableEmpiricalClosureError("receipt dependency closure omits the candidate grammar")
    return {
        "ref": receipt.ref.as_dict(),
        "typed_state": receipt.typed_state,
        "coverage_state": receipt.coverage_state,
        "family": _text(identity.get("family"), "receipt family"),
        "rule_id": _text(identity.get("rule_id"), "receipt rule id"),
        "validation_kind": _text(
            _mapping(identity.get("validation"), "receipt validation").get("kind"),
            "receipt validation kind",
        ),
        "winning_predicate_ref": winning_ref.as_dict(),
        "empirical_fact_refs": [ref.as_dict() for ref in _refs(receipt.empirical_fact_refs, "receipt facts")],
        "coverage_claim": discovery.coverage_claim,
        "role_rows": sorted(role_rows, key=lambda item: item["role"]),
        "ancestry_refs": [ref.as_dict() for ref in _refs(receipt.branch_or_parent_ancestry_refs, "receipt ancestry")],
        "replay_ref": _exact(receipt.replay_ref, "receipt replay").as_dict(),
    }


def _build_census(output: NativeEmpiricalOutput) -> Mapping[str, Any]:
    graph = output.object_graph
    facts = {obj.ref.key: obj for obj in graph.empirical_facts}
    predicates = {obj.ref.key: obj for obj in graph.executed_predicates}
    queries = {obj.ref.key: obj for obj in graph.executed_queries}
    discoveries = {obj.ref.key: obj for obj in graph.discovery_authorities}

    fact_rows = [_fact_rows(fact, queries, predicates) for fact in graph.empirical_facts]
    closure_release_refs = tuple(
        item.release_ref for item in output.release_identities
    )
    receipt_rows = [
        _receipt_rows(
            receipt,
            facts,
            predicates,
            queries,
            discoveries,
            closure_release_refs,
        )
        for receipt in graph.discovery_receipts
    ]
    fact_state_counts: dict[str, int] = {}
    for row in fact_rows:
        fact_state_counts[row["typed_state"]] = fact_state_counts.get(row["typed_state"], 0) + 1
    receipt_state_counts: dict[str, int] = {}
    coverage_state_counts: dict[str, int] = {}
    for row in receipt_rows:
        receipt_state_counts[row["typed_state"]] = receipt_state_counts.get(row["typed_state"], 0) + 1
        coverage_state_counts[row["coverage_state"]] = coverage_state_counts.get(row["coverage_state"], 0) + 1

    negative_or_held = []
    for row in fact_rows:
        if row["typed_state"] not in POSITIVE_FACT_STATES:
            negative_or_held.append(
                {"family": "EmpiricalFact@1.0.0", "ref": row["ref"], "typed_state": row["typed_state"]}
            )
    for row in receipt_rows:
        if row["typed_state"] != "DISCOVERED_RESULT_SUPPORTED" or row["coverage_state"] != "EVALUATED_SUPPORTED":
            negative_or_held.append(
                {
                    "family": "DiscoveryResultReceipt@1.0.0",
                    "ref": row["ref"],
                    "typed_state": row["typed_state"],
                    "coverage_state": row["coverage_state"],
                }
            )
    negative_or_held.sort(key=lambda item: canonical_json(item))

    unvisited = [
        row["ref"]
        for row in receipt_rows
        if row["typed_state"] == "UNEVALUATED"
    ]
    ancestry = sorted(
        {
            ref["kind"] + "|" + ref["object_id"] + "|" + ref["content_hash"]
            for row in receipt_rows
            for ref in row["ancestry_refs"]
        }
    )

    i03_fact_keys = {
        fact.ref.key for result in output.i03_results for fact in result.facts
    }
    for row in fact_rows:
        row["is_i03_result"] = exact_ref(row["ref"], "census fact ref").key in i03_fact_keys
    f1_refs = [
        row["ref"]
        for row in fact_rows
        if row["target_arity"] == 1
    ]
    f2_refs = [
        row["ref"]
        for row in receipt_rows
        if row["validation_kind"] == "CONDITIONAL_REVERSAL"
        and {role["role"] for role in row["role_rows"]} >= {"POOLED_POS", "POOLED_NEG"}
        and any(
            role["role"].startswith("STRATUM:") and role["role"].endswith(":POS")
            for role in row["role_rows"]
        )
        and any(
            role["role"].startswith("STRATUM:") and role["role"].endswith(":NEG")
            for role in row["role_rows"]
        )
    ]
    f3_refs = [
        row["ref"]
        for row in receipt_rows
        if row["family"] == "MINORITY_OR_NONMODAL_DEPARTURE"
    ]
    f4_refs = [
        row["ref"]
        for row in fact_rows
        if row["target_arity"] >= 3
        and row["source_scope_mode"] == "SINGLE_UNIVERSE"
        and row["same_respondent_binding_semantics"] == "EXACT_SCOPED_RESPONDENT"
    ]

    return {
        "declared": {
            "object_family_counts": {
                family: len(objects) for family, objects in _object_families(graph).items()
            },
            "fact_state_counts": dict(sorted(fact_state_counts.items())),
            "receipt_state_counts": dict(sorted(receipt_state_counts.items())),
            "coverage_state_counts": dict(sorted(coverage_state_counts.items())),
            "fact_rows": sorted(fact_rows, key=lambda row: canonical_json(row["ref"])),
            "receipt_rows": sorted(receipt_rows, key=lambda row: canonical_json(row["ref"])),
            "negative_or_held": negative_or_held,
            "unvisited_refs": sorted(unvisited, key=canonical_json),
            "ancestry_refs": ancestry,
            "absent_fact_states_in_this_output": sorted(
                set(CONSERVED_FACT_STATES) - set(fact_state_counts)
            ),
            "absent_receipt_states_in_this_output": sorted(
                set(CONSERVED_RECEIPT_STATES) - set(receipt_state_counts)
            ),
            "unvisited_state": (
                "NO_NATIVE_DISCOVERY_EXECUTED" if not output.discovery_results else
                "NONE__EXACT_FRONTIER_EVALUATES_ALL_CANDIDATES"
                if not unvisited
                else "DECLARED_UNVISITED_RECEIPTS"
            ),
            "original_source_objects_materialized": 0,
            "source_objects_retained": 0,
        },
        "f1_f4": {
            "F1_marginal_fact_refs": sorted(f1_refs, key=canonical_json),
            "F2_reversal_receipt_refs": sorted(f2_refs, key=canonical_json),
            "F3_minority_receipt_refs": sorted(f3_refs, key=canonical_json),
            "F4_same_respondent_joint_fact_refs": sorted(f4_refs, key=canonical_json),
        },
    }


def _i05_envelope(i05: ExactBoundedDiscoveryResult) -> Mapping[str, Any]:
    return {
        "contract_id": i05.contract_id,
        "discovery_authority_ref": i05.discovery_authority_ref.as_dict(),
        "candidate_grammar_ref": i05.candidate_grammar_ref.as_dict(),
        "evaluated_frontier_ref": i05.evaluated_frontier_ref.as_dict(),
        "coverage_claim": i05.coverage_claim,
        "candidate_count": i05.candidate_count,
        "covered_candidate_count": i05.covered_candidate_count,
        "valid_empty": i05.valid_empty,
        "replay_ref": i05.replay_ref.as_dict(),
        "receipt_refs": [receipt.ref.as_dict() for receipt in i05.receipts],
        "empirical_fact_refs": [ref.as_dict() for ref in i05.empirical_fact_refs],
        "executed_predicate_refs": [
            obj.ref.as_dict() for obj in i05.executed_predicates
        ],
        "executed_query_refs": [obj.ref.as_dict() for obj in i05.executed_queries],
    }


def _native_envelope(output: NativeEmpiricalOutput) -> Mapping[str, Any]:
    i05 = output.i05_result
    return {
        "source_identity": canonicalize(output.source_identity),
        "release_identities": [item.as_dict() for item in output.release_identities],
        "i03_results": [
            {
                "query_ref": result.query_ref.as_dict(),
                "source_scope_mode": result.source_scope_mode,
                "release_refs": [ref.as_dict() for ref in result.release_refs],
                "fact_refs": [fact.ref.as_dict() for fact in result.facts],
            }
            for result in output.i03_results
        ],
        "i05": _i05_envelope(i05) if i05 is not None else None,
        **({} if i05 is not None else {
            "discovery_envelope_schema": NATIVE_DISCOVERY_ENVELOPE_V2,
            "i05_results": [_i05_envelope(item) for item in output.discovery_results],
        }),
        "typed_states": canonicalize(output.typed_states) if output.typed_states is not None else None,
        "learned_empirical_execution_receipt": (
            canonicalize(output.learned_empirical_execution_receipt)
            if output.learned_empirical_execution_receipt is not None
            else None
        ),
        "replay_receipt_identity": output.replay_receipt_identity,
        "replay_receipt_header": (
            canonicalize(output.replay_receipt_header)
            if output.replay_receipt_header is not None
            else None
        ),
        "native_result_identity": output.native_result_identity,
    }


def _replay_documents(
    output: NativeEmpiricalOutput,
    fragments: dict[str, Any],
) -> tuple[Mapping[str, Any], dict[str, int]]:
    releases = output.release_by_ref()
    release_refs = tuple(item.release_ref for item in output.release_identities)
    fact_materials = []
    for fact in output.object_graph.empirical_facts:
        material = _fact_replay_material(fact, releases)
        digest = semantic_hash(material)
        if digest != _exact(fact.replay_ref, "fact replay").content_hash:
            raise DurableEmpiricalClosureError(
                "fact replay preimage does not reproduce the native replay identity"
            )
        fact_materials.append(
            {
                "fact_ref": fact.ref.as_dict(),
                "material_hash": digest,
                "material": _pack_replay_material(material, fragments),
            }
        )
    receipt_materials = []
    for receipt in output.object_graph.discovery_receipts:
        material = _receipt_replay_material(receipt, release_refs)
        digest = semantic_hash(material)
        if digest != _exact(receipt.replay_ref, "receipt replay").content_hash:
            raise DurableEmpiricalClosureError(
                "receipt replay preimage does not reproduce the native replay identity"
            )
        receipt_materials.append(
            {
                "receipt_ref": receipt.ref.as_dict(),
                "material_hash": digest,
                "material": canonicalize(material),
            }
        )
    def discovery_replay(i05):
        frontier = _frontier_replay_material(i05.receipts, i05)
        frontier_digest = semantic_hash(frontier)
        if frontier_digest != _exact(i05.evaluated_frontier_ref, "frontier").content_hash:
            raise DurableEmpiricalClosureError("reconstructed frontier preimage does not reproduce the native frontier identity")
        final = _final_replay_material(i05)
        final_digest = semantic_hash(final)
        if final_digest != _exact(i05.replay_ref, "i05 replay").content_hash:
            raise DurableEmpiricalClosureError("reconstructed final replay preimage does not reproduce the native replay identity")
        return {
            "frontier": {"material": canonicalize(frontier), "material_hash": frontier_digest},
            "i05_final": {"material": canonicalize(final), "material_hash": final_digest},
        }
    discovery_docs = (discovery_replay(output.i05_result)
        if output.i05_result is not None else {
            "discovery_replays": [
                {"discovery_authority_ref": item.discovery_authority_ref.as_dict(),
                 **discovery_replay(item)} for item in output.discovery_results
            ]})
    return ({"facts": fact_materials, "receipts": receipt_materials, **discovery_docs}, {})


def _object_entries(
    output: NativeEmpiricalOutput,
    fragments: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, bytes]]:
    entries: list[dict[str, Any]] = []
    blobs: dict[str, bytes] = {}
    for family, objects in _object_families(output.object_graph).items():
        for obj in objects:
            document = obj.as_dict()
            logical_raw = _canonical_bytes(document)
            packed = pack_canonical_preimage(document, fragments)
            # semantic_hash uses these same canonical UTF-8 bytes. Hash the
            # actual compressed preimage instead of serializing it a second time.
            raw, compressed = _compress(packed)
            document_hash = hashlib.sha256(raw).hexdigest()
            blobs[document_hash] = compressed
            entries.append(
                {
                    "family": _FAMILY_OBJECT_NAME[family],
                    "ref": obj.ref.as_dict(),
                    "document_hash": document_hash,
                    "document_uncompressed_bytes": len(raw),
                    "document_compressed_bytes": len(compressed),
                    "logical_document_bytes": len(logical_raw),
                    "fragment_refs": sorted(_markers(packed)),
                }
            )
    entries.sort(key=lambda item: canonical_json(item["ref"]))
    return entries, blobs


def _markers(value: Any) -> set[str]:
    markers: set[str] = set()
    if isinstance(value, Mapping):
        if set(value) == {FRAGMENT_MARKER}:
            markers.add(str(value[FRAGMENT_MARKER]))
            return markers
        for item in value.values():
            markers.update(_markers(item))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            markers.update(_markers(item))
    return markers


def _fragment_blobs(fragments: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, bytes]]:
    entries: list[dict[str, Any]] = []
    blobs: dict[str, bytes] = {}
    for digest in sorted(fragments):
        material = canonicalize(fragments[digest])
        raw, compressed = _compress(material)
        if hashlib.sha256(raw).hexdigest() != digest:
            raise DurableEmpiricalClosureError("fragment blob hash drift")
        blobs[digest] = compressed
        entries.append(
            {
                "fragment_hash": digest,
                "uncompressed_bytes": len(raw),
                "compressed_bytes": len(compressed),
            }
        )
    return entries, blobs


def _blob_manifest(
    object_entries: Iterable[Mapping[str, Any]],
    fragment_entries: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    blobs: dict[str, dict[str, Any]] = {}
    for entry in object_entries:
        blobs[entry["document_hash"]] = {
            "blob": f"{entry['document_hash']}{BLOB_SUFFIX}",
            "content_hash": entry["document_hash"],
            "uncompressed_bytes": entry["document_uncompressed_bytes"],
            "compressed_bytes": entry["document_compressed_bytes"],
        }
    for entry in fragment_entries:
        blobs[entry["fragment_hash"]] = {
            "blob": f"{entry['fragment_hash']}{BLOB_SUFFIX}",
            "content_hash": entry["fragment_hash"],
            "uncompressed_bytes": entry["uncompressed_bytes"],
            "compressed_bytes": entry["compressed_bytes"],
        }
    return [blobs[key] for key in sorted(blobs)]


def _root_identity(closure_identity: str, blobs: Iterable[Mapping[str, Any]]) -> str:
    return semantic_hash(
        {
            "schema": DURABLE_ROOT_SCHEMA,
            "closure_identity": closure_identity,
            "blobs": [
                {
                    "content_hash": item["content_hash"],
                    "uncompressed_bytes": item["uncompressed_bytes"],
                    "compressed_bytes": item["compressed_bytes"],
                }
                for item in sorted(blobs, key=lambda item: item["content_hash"])
            ],
        }
    )


class _ScratchCounter:
    def __init__(self) -> None:
        self.current = 0
        self.peak = 0

    def add(self, amount: int) -> None:
        self.current += int(amount)
        self.peak = max(self.peak, self.current)

    def remove(self, amount: int) -> None:
        self.current = max(0, self.current - int(amount))


def publish_empirical_closure(
    output: NativeEmpiricalOutput,
    root_dir: str | Path,
    *,
    consumer_binding: Mapping[str, Any] | None = None,
    descriptive_consumer: Mapping[str, Any] | None = None,
    expected_root: str | None = None,
    failpoint: Any | None = None,
    compact_manifest: bool = False,
) -> PublishReceipt:
    """Publish one complete native output closure exactly once.

    ``expected_root`` is an external pin.  Supplying it makes publication
    idempotent only for that exact root.  It is never inferred from the closure.
    """

    if type(compact_manifest) is not bool:
        raise DurableEmpiricalClosureError("explicit compact manifest selection required")
    started = time.monotonic()
    root = Path(root_dir)
    root.mkdir(parents=True, exist_ok=True)
    blob_dir = root / CAS_DIR / BLOB_DIR
    closures_dir = root / CLOSURES_DIR
    blob_dir.mkdir(parents=True, exist_ok=True)
    closures_dir.mkdir(parents=True, exist_ok=True)
    _cleanup_stale_publish_artifacts(root)

    _verify_output_graph(output)
    fragments: dict[str, Any] = {}
    replay_documents, _ = _replay_documents(output, fragments)
    object_entries, object_blobs = _object_entries(output, fragments)
    fragment_entries, fragment_blobs = _fragment_blobs(fragments)
    blobs = _blob_manifest(object_entries, fragment_entries)
    blob_specs = {item["content_hash"]: item for item in blobs}
    if set(object_blobs) & set(fragment_blobs):
        raise DurableEmpiricalClosureError("object and fragment blob hash collision")

    census = _build_census(output)
    # Logical evidence is the full preimage estate a naive result store would
    # retain (complete object documents plus the separate replay preimages).
    # Physical retention is only the compressed content-addressed blobs plus the
    # manifest; the same fact fragment is never stored twice.
    logical_bytes = (
        sum(entry["logical_document_bytes"] for entry in object_entries)
        + len(_canonical_bytes(replay_documents))
    )
    core: dict[str, Any] = {
        "schema": DURABLE_CLOSURE_SCHEMA,
        "contract": DURABLE_CLOSURE_CONTRACT_ID,
        "contract_sha": DURABLE_CLOSURE_CONTRACT_SHA,
        "evidence_grade": EVIDENCE_GRADE,
        "rights_state": RIGHTS_STATE,
        "source_access_state": SOURCE_ACCESS_STATE,
        "native_result": _native_envelope(output),
        "objects": object_entries,
        "fragments": fragment_entries,
        "replays": replay_documents,
        "census": census,
        "consumer_binding": (
            None if consumer_binding is None else canonicalize(consumer_binding)
        ),
        "descriptive_consumer": (
            None if descriptive_consumer is None else canonicalize(descriptive_consumer)
        ),
        "ab_contract": {
            "packet": "S2-F",
            "old_obligations": ["P2-07"],
            "evidence_grade": EVIDENCE_GRADE,
            "incoming_s2e_accepted": False,
            "full_integrated_s2f": "HOLD_DEPENDENCY",
            "scientific_authority": "SEPARATE_OWNER_NOT_MINTED",
        },
        "resource_shape": {
            "object_count": len(object_entries),
            "fragment_count": len(fragment_entries),
            "blob_count": len(blobs),
            "fact_count": len(output.object_graph.empirical_facts),
            "receipt_count": len(output.object_graph.discovery_receipts),
            "logical_evidence_bytes": int(logical_bytes),
            "compressed_blob_bytes": int(sum(item["compressed_bytes"] for item in blobs)),
            "rows": _row_counts(output, census),
        },
    }
    closure_identity = semantic_hash(core)
    root_identity = _root_identity(closure_identity, blobs)
    if expected_root is not None and expected_root != root_identity:
        raise DurableEmpiricalClosureError(
            "external root pin does not match the exact publication root"
        )
    manifest = {
        "schema": DURABLE_CLOSURE_SCHEMA,
        "contract": DURABLE_CLOSURE_CONTRACT_ID,
        "contract_sha": DURABLE_CLOSURE_CONTRACT_SHA,
        "publication": {
            "closure_identity": closure_identity,
            "root_identity": root_identity,
            "evidence_grade": EVIDENCE_GRADE,
        },
        "core": core,
    }
    manifest_bytes = _canonical_bytes(manifest)
    manifest_name = MANIFEST_NAME
    if compact_manifest and len(manifest_bytes) <= MAX_COMPACT_MANIFEST_RAW:
        packed = len(manifest_bytes).to_bytes(8,"big") + zlib.compress(manifest_bytes,6)
        if len(packed) < len(manifest_bytes):
            manifest_name = COMPACT_MANIFEST_NAME
            manifest_bytes = packed
    final_dir = closures_dir / f"closure-{closure_identity}"
    receipt_kwargs = dict(
        root_path=str(final_dir),
        closure_identity=closure_identity,
        root_identity=root_identity,
        object_count=len(object_entries),
        fragment_count=len(fragment_entries),
        blob_count=len(blobs),
        fact_count=len(output.object_graph.empirical_facts),
        receipt_count=len(output.object_graph.discovery_receipts),
        rows=_row_counts(output, census),
        logical_evidence_bytes=int(logical_bytes),
        compressed_fragment_bytes=int(
            sum(entry["compressed_bytes"] for entry in fragment_entries)
        ),
        manifest_bytes=len(manifest_bytes),
        source_open_count=0,
        dedup_ratio=0.0,
    )
    if final_dir.exists():
        existing_path = _manifest_file(final_dir)
        existing = _read_json_file(existing_path)
        existing_root = _mapping(existing.get("publication"), "publication").get(
            "root_identity"
        )
        if existing_root != root_identity:
            raise DurableEmpiricalClosureError(
                "one closure identity already exists with a different root"
            )
        # "Publish once" means the existing closure must still be exactly
        # readable under its own external root, not merely that a directory name
        # matches.
        open_empirical_closure(final_dir, expected_root=root_identity).require_trusted()
        referenced_blobs = sum(item["compressed_bytes"] for item in blobs)
        actual_manifest_bytes = existing_path.stat().st_size
        referenced_total = referenced_blobs + actual_manifest_bytes
        return PublishReceipt(
            **{
                **receipt_kwargs,
                "manifest_bytes": actual_manifest_bytes,
                "published": False,
                "referenced_physical_bytes": int(referenced_total),
                "referenced_blob_bytes": int(referenced_blobs),
                "peak_scratch_bytes": 0,
                "cas_new_bytes": 0,
                "dedup_ratio": (
                    float(referenced_total / logical_bytes) if logical_bytes else 0.0
                ),
            }
        )

    scratch = _ScratchCounter()
    staged_dir = closures_dir / f"{STAGING_PREFIX}{os.getpid()}-{uuid.uuid4().hex}"
    staged_dir.mkdir(parents=False, exist_ok=False)
    cas_new = 0
    published = True
    try:
        for digest in sorted(set(object_blobs) | set(fragment_blobs)):
            data = object_blobs.get(digest, fragment_blobs.get(digest))
            path = blob_dir / f"{digest}{BLOB_SUFFIX}"
            if path.exists():
                # A pre-existing content-addressed blob must reproduce its own
                # hash; a poisoned/partial CAS slot is never adopted silently.
                _verify_existing_blob(path, data, digest, blob_specs[digest])
                continue
            scratch.add(len(data))
            tmp = path.with_name(
                f".{path.name}.tmp-{os.getpid()}-{uuid.uuid4().hex}"
            )
            try:
                with open(tmp, "wb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(tmp, path)
                cas_new += len(data)
            finally:
                if tmp.exists():
                    tmp.unlink()
        _fsync_dir(blob_dir)
        if failpoint is not None:
            failpoint("after_blob_write")
        manifest_path = staged_dir / manifest_name
        scratch.add(len(manifest_bytes))
        with open(manifest_path, "wb") as handle:
            handle.write(manifest_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        _fsync_dir(staged_dir)
        if failpoint is not None:
            failpoint("before_manifest_replace")
        try:
            os.replace(staged_dir, final_dir)
        except OSError:
            if not final_dir.exists():
                raise
            existing = _read_json_file(_manifest_file(final_dir))
            if _mapping(existing.get("publication"), "publication").get(
                "root_identity"
            ) != root_identity:
                raise DurableEmpiricalClosureError(
                    "concurrent publication produced a different closure root"
                )
            open_empirical_closure(final_dir,expected_root=root_identity).require_trusted()
            published = False
        _fsync_dir(closures_dir)
        if failpoint is not None:
            failpoint("after_manifest_replace")
    except Exception:
        if staged_dir.exists():
            shutil.rmtree(staged_dir, ignore_errors=True)
        raise
    finally:
        if staged_dir.exists():
            shutil.rmtree(staged_dir, ignore_errors=True)

    referenced_blobs = sum(item["compressed_bytes"] for item in blobs)
    actual_manifest_bytes = _manifest_file(final_dir).stat().st_size
    referenced_total = referenced_blobs + actual_manifest_bytes
    return PublishReceipt(
        **{
            **receipt_kwargs,
            "manifest_bytes": actual_manifest_bytes,
            "published": published,
            "referenced_physical_bytes": int(referenced_total),
            "referenced_blob_bytes": int(referenced_blobs),
            "peak_scratch_bytes": int(scratch.peak),
            "cas_new_bytes": int(cas_new),
            "dedup_ratio": (
                float(referenced_total / logical_bytes) if logical_bytes else 0.0
            ),
        }
    )


def _row_counts(output: NativeEmpiricalOutput, census: Mapping[str, Any]) -> dict[str, int]:
    facts = census["declared"]["fact_rows"]
    receipts = census["declared"]["receipt_rows"]
    return {
        "native_facts": len(facts),
        "native_receipts": len(receipts),
        "native_objects": len(output.object_graph.public_objects()),
        "native_i03_results": len(output.i03_results),
        "risk_member_rows": sum(row["risk_member_count"] for row in facts),
        "denominator_member_rows": sum(row["denominator_member_count"] for row in facts),
        "target_cell_rows": sum(row["cell_count"] for row in facts),
        "receipt_role_rows": sum(len(row["role_rows"]) for row in receipts),
    }


def _manifest_file(directory: Path) -> Path:
    choices = tuple(directory / name for name in (MANIFEST_NAME,COMPACT_MANIFEST_NAME)
                    if (directory / name).exists())
    if len(choices) != 1 or not choices[0].is_file():
        raise DurableEmpiricalClosureError("exactly one closure manifest transport required")
    return choices[0]


def _read_json_file(path: Path) -> Mapping[str, Any]:
    try:
        with open(path, "rb") as handle:
            value = handle.read()
    except OSError as exc:
        raise DurableEmpiricalClosureError(f"closure file cannot be read: {path}") from exc
    import json

    try:
        if path.name == COMPACT_MANIFEST_NAME:
            if len(value) <= 8:
                raise ValueError("truncated compact manifest")
            size = int.from_bytes(value[:8],"big")
            if not 0 < size <= MAX_COMPACT_MANIFEST_RAW:
                raise ValueError("compact manifest expansion outside transport bound")
            decoder = zlib.decompressobj()
            raw = decoder.decompress(value[8:],size+1)
            if (len(raw) != size or not decoder.eof or decoder.unconsumed_tail
                    or decoder.unused_data):
                raise ValueError("compact manifest length or framing drift")
            value = raw
        document = json.loads(value.decode("utf-8"))
    except (UnicodeDecodeError, ValueError, zlib.error) as exc:
        raise DurableEmpiricalClosureError(f"closure file is not canonical JSON: {path}") from exc
    if not isinstance(document, Mapping):
        raise DurableEmpiricalClosureError(f"closure file is not a mapping: {path}")
    return document


@dataclass(frozen=True)
class DurableEmpiricalClosure:
    """A verified, cold-reconstructible native output closure."""

    root_path: Path
    root_identity: str
    closure_identity: str
    trust_state: str
    manifest: Mapping[str, Any]
    object_graph: RouteBEmpiricalObjectGraph
    i03_results: tuple[QueryExecutionResult, ...]
    i05_result: ExactBoundedDiscoveryResult | None
    release_identities: tuple[ReleaseIdentity, ...]
    consumer_binding: Mapping[str, Any] | None
    descriptive_consumer: Mapping[str, Any] | None
    census: Mapping[str, Any]
    i05_results: tuple[ExactBoundedDiscoveryResult, ...] = ()

    @property
    def discovery_results(self) -> tuple[ExactBoundedDiscoveryResult, ...]:
        return (self.i05_result,) if self.i05_result is not None else self.i05_results

    def discovery_by_receipt(self, receipt_ref: ExactRef) -> ExactBoundedDiscoveryResult:
        ref = _exact(receipt_ref, "discovery receipt")
        matches = [item for item in self.discovery_results
                   if any(r.ref == ref for r in item.receipts)]
        if len(matches) != 1:
            raise DurableEmpiricalClosureError("discovery receipt not uniquely retained")
        return matches[0]

    @property
    def exact_ref(self) -> ExactRef:
        return ExactRef(
            "PYAT_S2F_DURABLE_EMPIRICAL_CLOSURE@1.0.0",
            f"urn:rawlsing:s2f:closure:sha256:{self.root_identity}",
            self.root_identity,
        )

    def require_trusted(self) -> "DurableEmpiricalClosure":
        if self.trust_state != "EXTERNALLY_PINNED":
            raise DurableEmpiricalClosureUntrusted(
                "coherent self-hashed closure has no independent external root pin"
            )
        return self

    def assert_no_current_authority(self) -> None:
        """Fail closed if anyone claims the closure minted current rights."""

        if self.manifest["core"].get("rights_state") != RIGHTS_STATE:
            raise DurableEmpiricalClosureError("closure does not declare historical-only rights")
        if self.manifest["core"].get("source_access_state") != SOURCE_ACCESS_STATE:
            raise DurableEmpiricalClosureError("closure does not declare disabled source access")
        ab = _mapping(self.manifest["core"].get("ab_contract"), "ab_contract")
        if ab.get("scientific_authority") != "SEPARATE_OWNER_NOT_MINTED":
            raise DurableEmpiricalClosureError("closure improperly claims scientific authority")

    def historical_authority_registry(self) -> AuthorityRegistry:
        """Resolve the retained *historical* snapshots; this mints nothing."""

        return AuthorityRegistry(self.object_graph.authority_snapshots)

    def fact_by_ref(self, ref: ExactRef | Mapping[str, Any]) -> EmpiricalFact:
        exact = _exact(ref, "fact ref")
        for fact in self.object_graph.empirical_facts:
            if fact.ref == exact:
                return fact
        raise DurableEmpiricalClosureError("requested exact fact preimage is absent")

    def query_by_ref(self, ref: ExactRef | Mapping[str, Any]) -> EmpiricalQuerySpec:
        exact = _exact(ref, "query ref")
        for query in self.object_graph.executed_queries:
            if query.ref == exact:
                return query
        raise DurableEmpiricalClosureError("requested exact query preimage is absent")

    def m01_replay_view(self) -> DurableM01ReplayView:
        if len(self.release_identities) != 1:
            raise DurableEmpiricalClosureError(
                "M1 replay view requires one exact release identity"
            )
        return DurableM01ReplayView(
            object_graph=self.object_graph,
            c11_release=DurableReleaseRefView(self.release_identities[0].release_ref),
        )

    def m1_bundle_from_declared_binding(self) -> Any:
        """Run the actual existing M1 composer from the persisted consumer binding."""

        self.require_trusted()
        from rawlsing_next.pre553_learned_world_composition import (
            LearnedWorldProductContractBinding,
            build_m1_bundle_from_m01,
        )
        from rawlsing_next.pre553_learned_empirical_adjudication import (
            M1FamilyRuleBinding,
            M1PrerequisiteChannel,
        )

        binding = _mapping(self.consumer_binding, "consumer_binding")
        if binding.get("kind") != "M1_BUNDLE_COMPOSER":
            raise DurableEmpiricalClosureError("no declared M1 bundle composer binding")
        contract = LearnedWorldProductContractBinding(
            **_constructor_kwargs(binding.get("contract_kwargs"), "contract_kwargs")
        )
        family_rule = M1FamilyRuleBinding(
            **_constructor_kwargs(binding.get("binding_kwargs"), "binding_kwargs")
        )
        if contract.m1_family_rule_binding_ref != family_rule.ref:
            raise DurableEmpiricalClosureError(
                "declared M1 contract does not pin the reconstructed family rule"
            )
        additional_refs = _refs(
            binding.get("additional_authority_refs", ()), "additional authority refs"
        )
        additional = []
        authority_by_key = {
            obj.authority_ref.key: obj for obj in self.object_graph.authority_snapshots
        }
        for ref in additional_refs:
            obj = authority_by_key.get(ref.key)
            if obj is None:
                raise DurableEmpiricalClosureError(
                    "declared additional M1 authority preimage is absent"
                )
            additional.append(obj)
        channels = [
            M1PrerequisiteChannel(**_constructor_kwargs(document, "prerequisite channel"))
            for document in _sequence(
                binding.get("prerequisite_channel_documents", ()),
                "prerequisite_channel_documents",
            )
        ]
        return build_m1_bundle_from_m01(
            self.m01_replay_view(),
            contract=contract,
            family_rule_binding=family_rule,
            selected_discovery_receipt_refs=_refs(
                binding.get("selected_discovery_receipt_refs", ()),
                "selected discovery receipt refs",
            ),
            requested_scope=_mapping(binding.get("requested_scope"), "requested_scope"),
            additional_authority_snapshots=tuple(additional),
            prerequisite_channels=tuple(channels),
            additional_dependency_refs=_refs(
                binding.get("additional_dependency_refs", ()),
                "additional dependency refs",
            ),
        )

    def field_forge_profile_from_declared_consumer(self) -> Any:
        """Run the actual existing descriptive Field Forge fact consumer."""

        self.require_trusted()
        from rawlsing_next.field_forge_conditional_support import (
            produce_exact_conditional_support_profile,
        )

        config = _mapping(self.descriptive_consumer, "descriptive_consumer")
        if config.get("kind") != "FIELD_FORGE_EXACT_CONDITIONAL_SUPPORT":
            raise DurableEmpiricalClosureError("no declared Field Forge consumer")
        fact = self.fact_by_ref(config.get("joint_fact_ref"))
        query = self.query_by_ref(config.get("joint_query_ref"))
        if _exact(fact.empirical_query_spec_ref, "fact query") != query.ref:
            raise DurableEmpiricalClosureError("declared Field Forge fact/query mismatch")
        return produce_exact_conditional_support_profile(
            joint_fact=fact,
            joint_query=query,
            conditioner_ref=config.get("conditioner_ref"),
            target_ref=config.get("target_ref"),
            producer_permission_ceiling=tuple(
                _sequence(config.get("producer_permission_ceiling"), "producer_permission_ceiling")
            ),
            relation_permission_ceiling=(
                None
                if config.get("relation_permission_ceiling") is None
                else tuple(
                    _sequence(
                        config.get("relation_permission_ceiling"),
                        "relation_permission_ceiling",
                    )
                )
            ),
        )


def _constructor_kwargs(value: Any, name: str) -> dict[str, Any]:
    item = _mapping(value, name)
    return {str(key): _thaw(item[key]) for key in item}


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_thaw(item) for item in value]
    return value


def _freeze_config(value: Any) -> Any:
    from types import MappingProxyType

    if isinstance(value, Mapping):
        return MappingProxyType(
            {str(key): _freeze_config(item) for key, item in value.items()}
        )
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return tuple(_freeze_config(item) for item in value)
    return value


def _read_verified_manifest(closure_path,*,expected_root,allow_unpinned=False):
    """Shared exact root verification, deliberately not a complete blob audit."""
    path = Path(closure_path)
    if path.is_file():
        path = path.parent
    manifest = _read_json_file(_manifest_file(path))
    if manifest.get("schema") != DURABLE_CLOSURE_SCHEMA:
        raise DurableEmpiricalClosureError("closure manifest schema mismatch")
    if manifest.get("contract") != DURABLE_CLOSURE_CONTRACT_ID:
        raise DurableEmpiricalClosureError("closure manifest contract mismatch")
    if manifest.get("contract_sha") != DURABLE_CLOSURE_CONTRACT_SHA:
        raise DurableEmpiricalClosureError("closure manifest contract SHA mismatch")
    core = _mapping(manifest.get("core"), "closure core")
    publication = _mapping(manifest.get("publication"), "closure publication")
    closure_identity = semantic_hash(core)
    if publication.get("closure_identity") != closure_identity:
        raise DurableEmpiricalClosureError("closure identity self-hash mismatch")
    blobs = _sequence(core.get("blobs", ()), "closure blobs") if "blobs" in core else None
    object_entries = _sequence(core.get("objects"), "closure objects")
    fragment_entries = _sequence(core.get("fragments"), "closure fragments")
    if blobs is not None and blobs:
        raise DurableEmpiricalClosureError("closure core must not inline a second blob archive")
    blob_manifest = _blob_manifest(object_entries, fragment_entries)
    root_identity = _root_identity(closure_identity, blob_manifest)
    if publication.get("root_identity") != root_identity:
        raise DurableEmpiricalClosureError("closure root identity self-hash mismatch")
    trust_state = "UNPINNED_SELF_HASH"
    if expected_root is not None:
        if expected_root != root_identity:
            raise DurableEmpiricalClosureError(
                "closure root does not match the independent external pin"
            )
        trust_state = "EXTERNALLY_PINNED"
    elif not allow_unpinned:
        raise DurableEmpiricalClosureUntrusted(
            "closure has no independent external root pin; self-hash is not trust"
        )

    return (path,manifest,core,closure_identity,root_identity,trust_state,
            object_entries,fragment_entries)


def _load_exact_closure_object(blob_dir,item,fragments):
    ref=_exact(item.get("ref"),"object ref")
    digest=_text(item.get("document_hash"),"document_hash")
    if len(digest)!=64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise DurableEmpiricalClosureError("malformed exact document digest")
    packed=_load_blob(blob_dir/f"{digest}{BLOB_SUFFIX}",digest,item)
    if sorted(_markers(packed))!=list(item.get("fragment_refs",())):
        raise DurableEmpiricalClosureError("closure object fragment inventory drift")
    document=_mapping(hydrate_canonical_preimage(packed,fragments),"hydrated object")
    try:
        obj=materialize_public_object(document)
    except Exception as exc:
        raise DurableEmpiricalClosureError(
            f"closure object cannot be re-materialized exactly: {exc}") from exc
    if obj.ref!=ref or obj.family!=item.get("family"):
        raise DurableEmpiricalClosureError("closure object ref/family does not match identity")
    if canonical_json(obj.as_dict())!=canonical_json(document):
        raise DurableEmpiricalClosureError("closure object preimage is not byte-exact")
    if canonicalize(obj.semantic_projection())!=canonicalize({
        key:document[key] for key in ("schema_id","schema_version","typed_state",
            "authority_snapshot_refs","dependency_refs","producer_replay_locator_or_reference_root",
            "semantic_fields")}):
        raise DurableEmpiricalClosureError("closure object semantic projection drift")
    return obj


def _unique_archive_index(rows,key,description):
    result={}
    for row in rows:
        key_value=key(row)
        if key_value in result:
            raise DurableEmpiricalClosureError(f"duplicate {description} in closure")
        result[key_value]=row
    return result


class _SelectedI03Archive:
    """Private root-pinned selected-unit reader, NOT a DurableEmpiricalClosure.

    Full manifest authentication is retained. Only selected object/replay
    fragments are loaded. Unvisited objects and discovery frontiers are NOT
    audited by this view, and it cannot issue a complete-closure or authority
    claim. Full open_empirical_closure remains the audit operation.
    """
    def __init__(self,closure_path,*,expected_root):
        (path,manifest,core,_,root,trust,objects,fragments)=_read_verified_manifest(
            closure_path,expected_root=expected_root)
        if trust!="EXTERNALLY_PINNED":
            raise DurableEmpiricalClosureUntrusted("selected archive requires external root")
        if (core.get("rights_state")!=RIGHTS_STATE or core.get("source_access_state")!=SOURCE_ACCESS_STATE
                or _mapping(core.get("ab_contract"),"ab_contract").get("scientific_authority")!="SEPARATE_OWNER_NOT_MINTED"):
            raise DurableEmpiricalClosureError("selected archive rights boundary drift")
        self.root=root
        self.core=core
        self.native=_mapping(core.get("native_result"),"native_result")
        # Aggregate native receipt audit requires the full graph. Do not
        # pretend selected material can reproduce it. Country S2-F has none.
        if any(self.native.get(k) is not None for k in (
            "replay_receipt_identity","replay_receipt_header","native_result_identity")):
            raise DurableEmpiricalClosureError("selected read requires nonaggregate country closure")
        self.release_identities=tuple(ReleaseIdentity.from_dict(item) for item in
            _sequence(self.native.get("release_identities"),"release identities"))
        self.releases={r.release_ref.key:r for r in self.release_identities}
        self.objects=_unique_archive_index(objects,lambda x:_exact(x.get("ref"),"object ref").key,"object ref")
        self.fragment_entries=_unique_archive_index(fragments,lambda x:_text(x.get("fragment_hash"),"fragment hash"),"fragment")
        self.direct=_unique_archive_index(_sequence(self.native.get("i03_results"),"i03 results"),
                    lambda x:_exact(x.get("query_ref"),"query ref").key,"direct query")
        self.fact_replays=_unique_archive_index(_sequence(_mapping(core.get("replays"),"replays").get("facts"),"fact replays"),
                    lambda x:_exact(x.get("fact_ref"),"fact ref").key,"fact replay")
        self.fact_rows=_unique_archive_index(_sequence(_mapping(_mapping(core.get("census"),"census").get("declared"),"declared census").get("fact_rows"),"fact rows"),
                    lambda x:_exact(x.get("ref"),"fact census ref").key,"fact census")
        self.blob_dir=path.parent.parent/CAS_DIR/BLOB_DIR
        self._fragments={}
        self._objects={}
        self.blobs_read=0

    def _fragment(self,digest):
        if digest not in self._fragments:
            entry=self.fragment_entries.get(digest)
            if entry is None or len(digest)!=64 or any(ch not in "0123456789abcdef" for ch in digest):
                raise DurableEmpiricalClosureError("selected fragment absent or malformed")
            self._fragments[digest]=_load_blob(self.blob_dir/f"{digest}{BLOB_SUFFIX}",digest,entry)
            self.blobs_read+=1
        return self._fragments[digest]

    def object(self,ref,expected_type):
        ref=_exact(ref,"selected object ref")
        obj=self._objects.get(ref.key)
        if obj is None:
            entry=self.objects.get(ref.key)
            if entry is None:
                raise DurableEmpiricalClosureError("selected object preimage absent")
            # Load only declared references; shared helper independently
            # compares that inventory to the actual authenticated packed body.
            fragments={digest:self._fragment(digest) for digest in
                       _sequence(entry.get("fragment_refs"),"object fragments")}
            obj=_load_exact_closure_object(self.blob_dir,entry,fragments)
            self._objects[ref.key]=obj
            self.blobs_read+=1
        if type(obj) is not expected_type or obj.ref!=ref:
            raise DurableEmpiricalClosureError("selected exact object family/ref mismatch")
        return obj

    def authorities(self):
        return tuple(sorted((self.object(_exact(entry["ref"],"authority ref"),AuthoritySnapshot)
              for entry in self.objects.values() if entry["family"]=="AuthoritySnapshot@1.0.0"),
              key=lambda x:x.authority_ref.key))

    def query(self,ref,authorities):
        ref=_exact(ref,"selected query ref")
        entry=self.direct.get(ref.key)
        if entry is None:
            raise DurableEmpiricalClosureError("query not retained as direct I03 output")
        query=self.object(ref,EmpiricalQuerySpec)
        predicate=self.object(query.condition_predicate_ref,EmpiricalPredicate)
        facts=tuple(self.object(v,EmpiricalFact) for v in _sequence(entry.get("fact_refs"),"selected fact refs"))
        ex=QueryExecutionResult(ref,facts,_text(entry.get("source_scope_mode"),"source scope"),
                                _refs(entry.get("release_refs"),"selected release refs"))
        expected_entry={"query_ref":ref.as_dict(),"source_scope_mode":ex.source_scope_mode,
                        "release_refs":[x.as_dict() for x in ex.release_refs],
                        "fact_refs":[x.ref.as_dict() for x in facts]}
        if canonical_json(entry)!=canonical_json(expected_entry):
            raise DurableEmpiricalClosureError("selected I03 envelope drift")
        graph=RouteBEmpiricalObjectGraph(authorities,(predicate,),(query,),facts,(),())
        _verify_output_graph(NativeEmpiricalOutput(
            source_identity=self.native["source_identity"],release_identities=self.release_identities,
            i03_results=(ex,),i05_result=None,object_graph=graph))
        for fact in facts:
            row=_fact_rows(fact,{query.ref.key:query},{predicate.ref.key:predicate})
            row["is_i03_result"]=True
            if canonical_json(row)!=canonical_json(self.fact_rows.get(fact.ref.key)):
                raise DurableEmpiricalClosureError("selected fact census drift")
            replay=self.fact_replays.get(fact.ref.key)
            if replay is None:
                raise DurableEmpiricalClosureError("mandatory selected fact replay absent")
            fragments={digest:self._fragment(digest) for digest in _markers(replay.get("material"))}
            _verify_fact_replay_document(fact,replay,self.releases,fragments)
        return query,predicate,ex


def open_empirical_closure(
    closure_path: str | Path,
    *,
    expected_root: str | None,
    allow_unpinned: bool = False,
) -> DurableEmpiricalClosure:
    """Open and verify one closure without source access.

    ``expected_root`` is mandatory for a trusted read.  If it is absent the
    closure is still structurally verified but is marked ``UNPINNED_SELF_HASH``
    and refused unless the caller explicitly asks for an untrusted replay.
    """

    (path,manifest,core,closure_identity,root_identity,trust_state,
     object_entries,fragment_entries)=_read_verified_manifest(
        closure_path,expected_root=expected_root,allow_unpinned=allow_unpinned)

    root = path.parent.parent
    blob_dir = root / CAS_DIR / BLOB_DIR
    fragments: dict[str, Any] = {}
    for entry in fragment_entries:
        item = _mapping(entry, "fragment entry")
        digest = _text(item.get("fragment_hash"), "fragment_hash")
        blob_path = blob_dir / f"{digest}{BLOB_SUFFIX}"
        value = _load_blob(blob_path, digest, item)
        fragments[digest] = value
    fragments = fragment_map_from_entries(
        [
            {"fragment_hash": digest, "value": value}
            for digest, value in sorted(fragments.items())
        ]
    )

    objects_by_family: dict[str, list[CanonicalSemanticObject]] = {
        family: [] for family in _EXPECTED_FAMILY_CLASS
    }
    for entry in object_entries:
        item = _mapping(entry, "object entry")
        ref = _exact(item.get("ref"), "object ref")
        family = _text(item.get("family"), "object family")
        if family not in _FAMILY_OBJECT_NAME.values():
            raise DurableEmpiricalClosureError("unknown object family in closure")
        family_key = next(
            key for key, value in _FAMILY_OBJECT_NAME.items() if value == family
        )
        obj=_load_exact_closure_object(blob_dir,item,fragments)
        objects_by_family[family_key].append(obj)

    for family, objects in objects_by_family.items():
        expected = _EXPECTED_FAMILY_CLASS[family]
        if not all(isinstance(obj, expected) for obj in objects):
            raise DurableEmpiricalClosureError(f"{family} materialized with a wrong type")
        objects.sort(key=lambda obj: _family_sort_key(family, obj))
        if len({_family_sort_key(family, obj) for obj in objects}) != len(objects):
            raise DurableEmpiricalClosureError(f"{family} contains duplicate exact refs")
    object_graph = RouteBEmpiricalObjectGraph(
        authority_snapshots=tuple(objects_by_family["authority_snapshots"]),
        executed_predicates=tuple(objects_by_family["executed_predicates"]),
        executed_queries=tuple(objects_by_family["executed_queries"]),
        empirical_facts=tuple(objects_by_family["empirical_facts"]),
        discovery_authorities=tuple(objects_by_family["discovery_authorities"]),
        discovery_receipts=tuple(objects_by_family["discovery_receipts"]),
    )
    native = _mapping(core.get("native_result"), "native_result")
    release_identities = tuple(
        ReleaseIdentity.from_dict(item)
        for item in _sequence(native.get("release_identities"), "release identities")
    )
    if not release_identities:
        raise DurableEmpiricalClosureError("closure has no release identities")
    releases = {item.release_ref.key: item for item in release_identities}

    fact_by_key = {obj.ref.key: obj for obj in object_graph.empirical_facts}
    query_by_key = {obj.ref.key: obj for obj in object_graph.executed_queries}
    predicate_by_key = {obj.ref.key: obj for obj in object_graph.executed_predicates}
    receipt_by_key = {obj.ref.key: obj for obj in object_graph.discovery_receipts}

    i03_results = []
    for item in _sequence(native.get("i03_results"), "i03 results"):
        entry = _mapping(item, "i03 result")
        query_ref = _exact(entry.get("query_ref"), "i03 query ref")
        facts = []
        for raw in _sequence(entry.get("fact_refs"), "i03 fact refs"):
            ref = _exact(raw, "i03 fact ref")
            fact = fact_by_key.get(ref.key)
            if fact is None:
                raise DurableEmpiricalClosureError("i03 fact preimage is absent")
            facts.append(fact)
        i03_results.append(
            QueryExecutionResult(
                query_ref=query_ref,
                facts=tuple(sorted(facts, key=lambda fact: fact.ref.key)),
                source_scope_mode=_text(
                    entry.get("source_scope_mode"), "i03 source_scope_mode"
                ),
                release_refs=_refs(entry.get("release_refs"), "i03 release refs"),
            )
        )

    def parse_discovery(i05_entry):
        i05_entry = _mapping(i05_entry, "i05 envelope")
        receipts = []
        for raw in _sequence(i05_entry.get("receipt_refs"), "i05 receipt refs"):
            ref = _exact(raw, "i05 receipt ref")
            receipt = receipt_by_key.get(ref.key)
            if receipt is None:
                raise DurableEmpiricalClosureError("i05 receipt preimage is absent")
            receipts.append(receipt)
        i05_fact_refs = tuple(
            _exact(raw, "i05 fact ref")
            for raw in _sequence(i05_entry.get("empirical_fact_refs"), "i05 fact refs")
        )
        i05_facts = []
        for ref in i05_fact_refs:
            fact = fact_by_key.get(ref.key)
            if fact is None:
                raise DurableEmpiricalClosureError("i05 fact preimage is absent")
            i05_facts.append(fact)
        i05_predicates = []
        for raw in _sequence(i05_entry.get("executed_predicate_refs"), "i05 predicate refs"):
            ref = _exact(raw, "i05 predicate ref")
            predicate = predicate_by_key.get(ref.key)
            if predicate is None:
                raise DurableEmpiricalClosureError("i05 predicate preimage is absent")
            i05_predicates.append(predicate)
        i05_queries = []
        for raw in _sequence(i05_entry.get("executed_query_refs"), "i05 query refs"):
            ref = _exact(raw, "i05 query ref")
            query = query_by_key.get(ref.key)
            if query is None:
                raise DurableEmpiricalClosureError("i05 query preimage is absent")
            i05_queries.append(query)
        i05 = ExactBoundedDiscoveryResult(
            contract_id=_text(i05_entry.get("contract_id"), "i05 contract"),
            discovery_authority_ref=_exact(
                i05_entry.get("discovery_authority_ref"), "i05 discovery authority"
            ),
            candidate_grammar_ref=_exact(
                i05_entry.get("candidate_grammar_ref"), "i05 candidate grammar"
            ),
            evaluated_frontier_ref=_exact(
                i05_entry.get("evaluated_frontier_ref"), "i05 frontier"
            ),
            coverage_claim=_text(i05_entry.get("coverage_claim"), "i05 coverage claim"),
            candidate_count=int(i05_entry.get("candidate_count")),
            covered_candidate_count=int(i05_entry.get("covered_candidate_count")),
            receipts=tuple(sorted(receipts, key=lambda receipt: receipt.ref.key)),
            empirical_fact_refs=tuple(sorted(i05_fact_refs, key=lambda ref: ref.key)),
            empirical_facts=tuple(sorted(i05_facts, key=lambda fact: fact.ref.key)),
            executed_predicates=tuple(sorted(i05_predicates, key=lambda obj: obj.ref.key)),
            executed_queries=tuple(sorted(i05_queries, key=lambda obj: obj.ref.key)),
            valid_empty=bool(i05_entry.get("valid_empty")),
            replay_ref=_exact(i05_entry.get("replay_ref"), "i05 replay"),
        )

        if i05.candidate_count != len(i05.receipts) or i05.covered_candidate_count != len(i05.receipts):
            raise DurableEmpiricalClosureError("i05 candidate/receipt cardinality mismatch")
        if i05.valid_empty != all(
            receipt.typed_state == "VALID_EMPTY" for receipt in i05.receipts
        ):
            raise DurableEmpiricalClosureError("i05 valid_empty contradicts its receipt states")
        # Do not coerce an internally rehashed string count/bool, reorder
        # a frontier, or silently discard undeclared fields on cold read.
        if canonical_json(i05_entry) != canonical_json(_i05_envelope(i05)):
            raise DurableEmpiricalClosureError("native I05 envelope is not exact")
        return i05

    if "discovery_envelope_schema" in native:
        if (native["discovery_envelope_schema"] != NATIVE_DISCOVERY_ENVELOPE_V2
                or native.get("i05") is not None):
            raise DurableEmpiricalClosureError("invalid plural native discovery envelope")
        i05 = None
        i05_results = tuple(parse_discovery(row) for row in _sequence(
            native.get("i05_results"), "plural native I05 envelopes"))
        if tuple(sorted(i05_results, key=lambda item: item.discovery_authority_ref.key)) != i05_results:
            raise DurableEmpiricalClosureError("plural discovery envelopes not canonical")
    else:
        if "i05_results" in native:
            raise DurableEmpiricalClosureError("unversioned plural native discovery envelope")
        i05 = parse_discovery(native.get("i05"))
        i05_results = ()

    census = _mapping(core.get("census"), "census")
    if canonical_json(census) != canonical_json(
        _build_census(
            NativeEmpiricalOutput(
                source_identity=_mapping(native.get("source_identity"), "source_identity"),
                release_identities=release_identities,
                i03_results=tuple(i03_results),
                i05_result=i05,
                i05_results=i05_results,
                object_graph=object_graph,
            )
        )
    ):
        raise DurableEmpiricalClosureError("closure census does not reproduce the native output")

    _verify_replay_documents(core, object_graph, i05, releases, fragments, i05_results=i05_results)
    _verify_authority_closure(object_graph)
    _verify_native_replay_receipt(native, object_graph)
    _verify_output_graph(
        NativeEmpiricalOutput(
            source_identity=_mapping(native.get("source_identity"), "source_identity"),
            release_identities=release_identities,
            i03_results=tuple(i03_results),
            i05_result=i05,
            i05_results=i05_results,
            object_graph=object_graph,
        )
    )

    return DurableEmpiricalClosure(
        root_path=path,
        root_identity=root_identity,
        closure_identity=closure_identity,
        trust_state=trust_state,
        manifest=_freeze_config(manifest),
        object_graph=object_graph,
        i03_results=tuple(i03_results),
        i05_result=i05,
        i05_results=i05_results,
        release_identities=release_identities,
        consumer_binding=(
            None
            if core.get("consumer_binding") is None
            else _freeze_config(_mapping(core.get("consumer_binding"), "consumer_binding"))
        ),
        descriptive_consumer=(
            None
            if core.get("descriptive_consumer") is None
            else _freeze_config(_mapping(core.get("descriptive_consumer"), "descriptive_consumer"))
        ),
        census=_freeze_config(census),
    )


def _verify_existing_blob(path: Path, generated: bytes, digest: str, entry: Mapping[str, Any]) -> None:
    """Verify actual CAS bytes against this publication's exact preimage.

    Generated bytes have already been produced from canonical material and
    their content digest and lengths established by the existing publisher.
    Equality is a stronger witness than another parse/canonicalize/hash of
    those same bytes. It is not an mtime, path or cached-permission shortcut.
    Different encodings must pass the SAME size and semantic checks as a
    cold reader; semantic hash alone cannot license a different extent.
    """
    actual = path.read_bytes()
    if actual == generated:
        return
    _decode_verified_blob(actual, digest, entry)


def _load_blob(path: Path, expected_hash: str, entry: Mapping[str, Any]) -> Any:
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        raise DurableEmpiricalClosureError(
            f"mandatory closure blob is missing: {path.name}"
        ) from exc
    return _decode_verified_blob(data, expected_hash, entry)


def _decode_verified_blob(data: bytes, expected_hash: str, entry: Mapping[str, Any]) -> Any:
    try:
        value = _decompress(data)
    except Exception as exc:
        raise DurableEmpiricalClosureError(
            f"closure blob is not decodable: {path.name}"
        ) from exc
    from rawlsing_next.pre553_empirical_objects import canonical_json

    raw = canonical_json(value).encode("utf-8")
    if hashlib.sha256(raw).hexdigest() != expected_hash:
        raise DurableEmpiricalClosureError("closure blob content hash drift")
    expected_compressed = entry.get("compressed_bytes", entry.get("document_compressed_bytes"))
    if expected_compressed is not None and int(expected_compressed) != len(data):
        raise DurableEmpiricalClosureError("closure blob compressed size drift")
    expected_uncompressed = entry.get("uncompressed_bytes", entry.get("document_uncompressed_bytes"))
    if expected_uncompressed is not None and int(expected_uncompressed) != len(raw):
        raise DurableEmpiricalClosureError("closure blob uncompressed size drift")
    return value


def _verify_fact_replay_document(fact,item,releases,fragments):
    material = _fact_replay_material(fact, releases)
    digest = semantic_hash(material)
    if digest != _text(item.get("material_hash"), "fact material hash"):
        raise DurableEmpiricalClosureError("fact replay material hash drift")
    if digest != _exact(fact.replay_ref, "fact replay").content_hash:
        raise DurableEmpiricalClosureError("fact replay preimage does not match its exact ref")
    stored = hydrate_canonical_preimage(item.get("material"), fragments)
    if canonical_json(stored) != canonical_json(material):
        raise DurableEmpiricalClosureError("fact replay stored preimage is not exact")


def _verify_replay_documents(
    core: Mapping[str, Any],
    graph: RouteBEmpiricalObjectGraph,
    i05: ExactBoundedDiscoveryResult | None,
    releases: Mapping[str, ReleaseIdentity],
    fragments: Mapping[str, Any],
    *,
    i05_results: tuple[ExactBoundedDiscoveryResult, ...] = (),
) -> None:
    replays = _mapping(core.get("replays"), "replays")
    fact_docs = {
        _exact(item.get("fact_ref"), "replay fact ref").key: item
        for item in _sequence(replays.get("facts"), "fact replays")
    }
    for fact in graph.empirical_facts:
        item = fact_docs.get(fact.ref.key)
        if item is None:
            raise DurableEmpiricalClosureError("mandatory fact replay preimage is absent")
        _verify_fact_replay_document(fact,item,releases,fragments)
    receipt_docs = {
        _exact(item.get("receipt_ref"), "replay receipt ref").key: item
        for item in _sequence(replays.get("receipts"), "receipt replays")
    }
    for receipt in graph.discovery_receipts:
        item = receipt_docs.get(receipt.ref.key)
        if item is None:
            raise DurableEmpiricalClosureError("mandatory receipt replay preimage is absent")
        material = _receipt_replay_material(
            receipt, (entry.release_ref for entry in releases.values())
        )
        digest = semantic_hash(material)
        if digest != _text(item.get("material_hash"), "receipt material hash"):
            raise DurableEmpiricalClosureError("receipt replay material hash drift")
        if digest != _exact(receipt.replay_ref, "receipt replay").content_hash:
            raise DurableEmpiricalClosureError("receipt replay preimage does not match its exact ref")
        if canonical_json(item.get("material")) != canonical_json(material):
            raise DurableEmpiricalClosureError("receipt replay stored preimage is not exact")
    def verify_discovery(i05, doc):
        frontier_item = _mapping(doc.get("frontier"), "frontier replay")
        frontier = _frontier_replay_material(i05.receipts, i05)
        if semantic_hash(frontier) != _text(
            frontier_item.get("material_hash"), "frontier material hash"
        ):
            raise DurableEmpiricalClosureError("frontier replay material hash drift")
        if semantic_hash(frontier) != _exact(
            i05.evaluated_frontier_ref, "i05 frontier"
        ).content_hash:
            raise DurableEmpiricalClosureError("frontier replay does not match the exact frontier ref")
        if canonical_json(frontier_item.get("material")) != canonical_json(frontier):
            raise DurableEmpiricalClosureError("frontier replay stored preimage is not exact")
        final_item = _mapping(doc.get("i05_final"), "final replay")
        final = _final_replay_material(i05)
        if semantic_hash(final) != _text(
            final_item.get("material_hash"), "final material hash"
        ):
            raise DurableEmpiricalClosureError("final replay material hash drift")
        if semantic_hash(final) != _exact(i05.replay_ref, "i05 replay").content_hash:
            raise DurableEmpiricalClosureError("final replay does not match the exact i05 replay ref")
        if canonical_json(final_item.get("material")) != canonical_json(final):
            raise DurableEmpiricalClosureError("final replay stored preimage is not exact")


    if i05 is not None:
        if "discovery_replays" in replays:
            raise DurableEmpiricalClosureError("ambiguous singular/plural discovery replay")
        verify_discovery(i05, replays)
    else:
        if "frontier" in replays or "i05_final" in replays:
            raise DurableEmpiricalClosureError("singular replay in plural archive")
        docs = _sequence(replays.get("discovery_replays"), "discovery replays")
        if len(docs) != len(i05_results):
            raise DurableEmpiricalClosureError("discovery replay census mismatch")
        for item, doc in zip(i05_results, docs):
            doc = _mapping(doc, "discovery replay")
            if _exact(doc.get("discovery_authority_ref"), "discovery replay authority") != item.discovery_authority_ref:
                raise DurableEmpiricalClosureError("discovery replay identity mismatch")
            verify_discovery(item, doc)


def _verify_authority_closure(graph: RouteBEmpiricalObjectGraph) -> None:
    registry = AuthorityRegistry(graph.authority_snapshots)
    for family, objects in _object_families(graph).items():
        if family == "authority_snapshots":
            continue
        for obj in objects:
            try:
                validate_object_authority_closure(obj, registry)
            except Exception as exc:
                raise DurableEmpiricalClosureError(
                    f"retained object authority closure cannot be satisfied: {exc}"
                ) from exc


def _verify_native_replay_receipt(
    native: Mapping[str, Any],
    graph: RouteBEmpiricalObjectGraph,
) -> None:
    """Reconstruct the M01 aggregate replay receipt without a second archive.

    The closure stores only the non-preimage header and the exact receipt
    identity.  The public-object preimages are the same exact objects already
    stored in the closure, so the full receipt identity is recomputable.
    """

    identity = native.get("replay_receipt_identity")
    header = native.get("replay_receipt_header")
    if identity is None and header is None:
        return
    if not isinstance(identity, str) or len(identity) != 64:
        raise DurableEmpiricalClosureError("native replay receipt identity is malformed")
    header = _mapping(header, "replay_receipt_header")
    dependency_material = _mapping(
        header.get("dependency_material"), "replay dependency_material"
    )
    if semantic_hash(dependency_material) != _text(
        header.get("dependency_root"), "replay dependency_root"
    ):
        raise DurableEmpiricalClosureError("native replay dependency root mismatch")
    if native.get("native_result_identity") not in (None, header.get("dependency_root")):
        raise DurableEmpiricalClosureError("native result identity/root mismatch")
    material = dict(header)
    material["object_preimages"] = {
        "authority_snapshots": [obj.as_dict() for obj in graph.authority_snapshots],
        "executed_predicates": [obj.as_dict() for obj in graph.executed_predicates],
        "executed_queries": [obj.as_dict() for obj in graph.executed_queries],
        "empirical_facts": [obj.as_dict() for obj in graph.empirical_facts],
        "discovery_authorities": [obj.as_dict() for obj in graph.discovery_authorities],
        "discovery_receipts": [obj.as_dict() for obj in graph.discovery_receipts],
    }
    if semantic_hash(material) != identity:
        raise DurableEmpiricalClosureError(
            "native aggregate replay receipt preimage is not reconstructible"
        )


__all__ = [
    "DURABLE_CLOSURE_CONTRACT_ID",
    "DURABLE_CLOSURE_SCHEMA",
    "DURABLE_CLOSURE_CONTRACT_SHA",
    "EVIDENCE_GRADE",
    "RIGHTS_STATE",
    "SOURCE_ACCESS_STATE",
    "DurableEmpiricalClosureError",
    "DurableEmpiricalClosureUntrusted",
    "ReleaseIdentity",
    "NativeEmpiricalOutput",
    "PublishReceipt",
    "DurableEmpiricalClosure",
    "DurableReleaseRefView",
    "DurableM01ReplayView",
    "publish_empirical_closure",
    "open_empirical_closure",
]
