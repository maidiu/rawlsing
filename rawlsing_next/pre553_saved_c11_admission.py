"""S2-D typed saved C11 admission over the accepted S2-C physical estate.

This module is deliberately a *consumer admission*, not a second physical
writer, scientific evaluator, issuer or C11 graph builder.  It binds one exact
accepted ``VerifiedDirectEstate`` to the existing native I03/I05 owners:

* I03: the existing ``CarrierNeutralResearchExecutor.execute_i03`` path and
  ``execute_empirical_query`` semantics.
* I05: the existing ``execute_exact_bounded_discovery`` owner, with the exact
  S2-C ``DirectEstateI03Session`` as its bounded repository view.

The admitted estate is read through S2-C's independently pinned manifest,
direct-I02 roots and reconstructed historical v1 release identity.  No
``C11LogicalRelease``, ``C11Repository`` object graph, full replay closure,
second persistent body corpus or source reopen is introduced here.

Shared-file integration for Batch, normal issued workloads and joined resume is
intentionally not implemented in this new module.  The exact owner/signature
handoff is exposed as a typed refusal so it cannot be mistaken for a completed
all-reader product.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor,
    RuntimeObjectCatalog,
)
from rawlsing_next.pre553_direct_estate_i03 import (
    DirectEstateI03Session,
    _ref_from_key,
)
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError,
    VerifiedDirectEstate,
)


class SavedC11AdmissionError(ValueError):
    """A saved-store input, identity, current grant or consumer is invalid."""


class SavedWorkloadOwnerHandoffRequired(SavedC11AdmissionError):
    """The remaining reader is lawful but needs an exact shared-file owner ACK."""

    def __init__(
        self,
        *,
        code: str,
        owner: str,
        path: str,
        function: str,
        minimum_edit: str,
        detail: str,
    ) -> None:
        self.code = code
        self.owner = owner
        self.path = path
        self.function = function
        self.minimum_edit = minimum_edit
        self.detail = detail
        super().__init__(
            f"{code}: owner={owner} path={path} function={function} "
            f"minimum_edit={minimum_edit} detail={detail}"
        )


@dataclass(frozen=True)
class SavedReleaseIdentity:
    """Identity-only release object for a future owner-approved Batch adapter.

    This is NOT a C11LogicalRelease and carries no validation seal.  It exists
    only so a narrow Batch guard can establish that the exact release named by a
    saved estate is the one in the manifest without constructing the full C11
    graph.  Batch itself remains a shared owner file and is not edited here.
    """

    release_ref: ExactRef

    def __post_init__(self) -> None:
        if type(self.release_ref) is not ExactRef:
            raise SavedC11AdmissionError(
                "exact release identity required for saved Batch admission"
            )


@dataclass(frozen=True)
class SavedBindingReceipt:
    schema: str
    manifest_sha256: str
    i02: ExternalI02Roots
    release_ref: ExactRef
    estate_path: str
    runtime_catalog: Mapping[str, Any]
    source_opens: int = 0
    full_c11_repository_builds: int = 0
    full_c11_logical_release_builds: int = 0
    persistent_body_corpora: int = 0
    counter_status: str = "DECLARED_ZERO__NOT_A_MEASUREMENT"

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "manifest_sha256": self.manifest_sha256,
            "i02": {
                "logical": self.i02.logical,
                "physical": self.i02.physical,
                "release": self.i02.release,
                "source": self.i02.source,
                "replay": self.i02.replay,
                "universe": self.i02.universe,
                "schema": self.i02.schema,
            },
            "release_ref": self.release_ref.as_dict(),
            "estate_path": self.estate_path,
            "runtime_catalog": dict(self.runtime_catalog),
            "source_opens": self.source_opens,
            "full_c11_repository_builds": self.full_c11_repository_builds,
            "full_c11_logical_release_builds": self.full_c11_logical_release_builds,
            "persistent_body_corpora": self.persistent_body_corpora,
            "counter_status": self.counter_status,
        }


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise SavedC11AdmissionError(f"{name} must be an exact mapping")
    return value


def _sequence(value: Any, name: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise SavedC11AdmissionError(f"{name} must be a sequence")
    return value


class SavedC11Admission:
    """One exact accepted S2-C estate with bounded native I03/I05 consumers.

    The bound estate/release/catalog are private-and-frozen after construction.
    Reassigning any binding field is a refusal, not a silent retarget.  A direct
    constructor also re-verifies the supplied estate into a private reader, so a
    caller mutation of the object it passed cannot retarget an already-open
    admission.
    """

    __slots__ = (
        "_estate",
        "_release_ref",
        "_runtime_catalog",
        "_executor",
        "_universe_ref",
        "_source_ref",
        "_frozen",
    )

    def __init__(
        self,
        *,
        estate: VerifiedDirectEstate,
        release_ref: ExactRef,
        runtime_catalog: RuntimeObjectCatalog,
    ) -> None:
        if type(estate) is not VerifiedDirectEstate:
            raise SavedC11AdmissionError(
                "exact accepted VerifiedDirectEstate required; no duck repository"
            )
        if type(release_ref) is not ExactRef:
            raise SavedC11AdmissionError("exact reconstructed v1 release ref required")
        if type(runtime_catalog) is not RuntimeObjectCatalog:
            raise SavedC11AdmissionError("exact RuntimeObjectCatalog required")
        # Snapshot by re-verifying the exact pins into a private reader object.
        # A caller cannot retarget this admission by mutating the estate it still
        # holds after construction.
        private_estate = VerifiedDirectEstate(
            estate.root,
            exact_path=estate.directory,
            independently_held_manifest_sha256=estate.held_manifest_sha256,
            independently_held_i02=estate.i02,
            current_authorizer=estate._authorize,
        )
        self._initialize(private_estate, release_ref, runtime_catalog)

    @classmethod
    def _from_verified_estate(
        cls,
        estate: VerifiedDirectEstate,
        release_ref: ExactRef,
        runtime_catalog: RuntimeObjectCatalog,
    ) -> "SavedC11Admission":
        """Internal fast path for an estate just verified by ``open``."""

        if type(estate) is not VerifiedDirectEstate:
            raise SavedC11AdmissionError(
                "exact accepted VerifiedDirectEstate required; no duck repository"
            )
        self = cls.__new__(cls)
        self._initialize(estate, release_ref, runtime_catalog)
        return self

    def _initialize(
        self,
        estate: VerifiedDirectEstate,
        release_ref: ExactRef,
        runtime_catalog: RuntimeObjectCatalog,
    ) -> None:
        if type(release_ref) is not ExactRef:
            raise SavedC11AdmissionError("exact reconstructed v1 release ref required")
        if type(runtime_catalog) is not RuntimeObjectCatalog:
            raise SavedC11AdmissionError("exact RuntimeObjectCatalog required")
        if release_ref != estate.reconstructed_v1_release_ref:
            raise SavedC11AdmissionError(
                "saved release ref differs from the estate's reconstructed v1 identity"
            )
        # Private catalog snapshot: later mutation of the caller's catalog object
        # cannot replace the workload bound to this admission.
        private_catalog = RuntimeObjectCatalog(
            authorities=tuple(runtime_catalog.authorities),
            predicates=tuple(runtime_catalog.predicates),
            queries=tuple(runtime_catalog.queries),
            discovery_authorities=tuple(runtime_catalog.discovery_authorities),
        )
        # Constructing the existing carrier performs the exact type, release,
        # current and catalog checks without asking for a C11 repository.
        executor = CarrierNeutralResearchExecutor(
            repository=estate,
            release_refs=(release_ref,),
            runtime_catalog=private_catalog,
        )
        universe_ref = _ref_from_key(
            estate.i02.universe, "EmpiricalUniverse@1.0.0"
        )
        source_kind = estate.i02.source.split("|", 1)[0]
        source_ref = _ref_from_key(estate.i02.source, source_kind)
        object.__setattr__(self, "_estate", estate)
        object.__setattr__(self, "_release_ref", release_ref)
        object.__setattr__(self, "_runtime_catalog", private_catalog)
        object.__setattr__(self, "_executor", executor)
        object.__setattr__(self, "_universe_ref", universe_ref)
        object.__setattr__(self, "_source_ref", source_ref)
        object.__setattr__(self, "_frozen", True)
        estate._live()

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, "_frozen", False):
            raise SavedC11AdmissionError("saved admission binding is immutable")
        object.__setattr__(self, name, value)

    @classmethod
    def open(
        cls,
        *,
        root: str | Any,
        exact_path: str | Any,
        independently_held_manifest_sha256: str,
        independently_held_i02: ExternalI02Roots,
        release_ref: ExactRef,
        runtime_catalog: RuntimeObjectCatalog,
        current_authorizer: Any,
    ) -> "SavedC11Admission":
        """Open one process-exited S2-C estate with independent pins/current."""

        estate = VerifiedDirectEstate(
            root,
            exact_path=exact_path,
            independently_held_manifest_sha256=independently_held_manifest_sha256,
            independently_held_i02=independently_held_i02,
            current_authorizer=current_authorizer,
        )
        return cls._from_verified_estate(estate, release_ref, runtime_catalog)

    @property
    def manifest_sha256(self) -> str:
        return self._estate.held_manifest_sha256

    @property
    def i02(self) -> ExternalI02Roots:
        return self._estate.i02

    @property
    def estate_path(self) -> str:
        return self._estate.directory.as_posix()

    @property
    def release_ref(self) -> ExactRef:
        """Exact reconstructed historical v1 release admitted by this estate."""

        return self._release_ref

    @property
    def source_ref(self) -> ExactRef:
        """Exact admitted source artifact, derived from the estate's I02 root."""

        return self._source_ref

    @property
    def replay_ref(self) -> ExactRef:
        """Exact native replay identity, derived from the estate's I02 root."""

        kind = self._estate.i02.replay.split("|", 1)[0]
        return _ref_from_key(self._estate.i02.replay, kind)

    def check_current(self) -> None:
        """Recheck the external current/rights callback before protected work."""

        self._estate._live()

    def binding_receipt(self) -> SavedBindingReceipt:
        return SavedBindingReceipt(
            schema="PYAT991_S2D_SAVED_C11_ADMISSION@1",
            manifest_sha256=self.manifest_sha256,
            i02=self.i02,
            release_ref=self._release_ref,
            estate_path=self.estate_path,
            runtime_catalog=self._runtime_catalog.receipt(),
        )

    def _require_exact_scope_refs(self, refs: Any, label: str) -> None:
        """Require exact source selectors without narrowing lawful scope metadata.

        The original EmpiricalQuerySpec/EmpiricalPredicate schema permits
        non-universe scope refs (for example the exact admitted C11LogicalRelease
        or a source-scope descriptor).  The native I03 owner accepts those.
        A saved single-universe admission must reject a *foreign universe* or
        *foreign release* in scope, but must not require the entire scope set to
        equal a singleton universe when the owner itself permits additional
        exact scope metadata.
        """

        parsed = tuple(exact_ref(value, label) for value in refs)
        universes = {
            ref.key for ref in parsed if ref.kind == "EmpiricalUniverse@1.0.0"
        }
        releases = {
            ref.key for ref in parsed if ref.kind == "C11LogicalRelease"
        }
        if universes != {self._universe_ref.key}:
            raise SavedC11AdmissionError(
                "saved consumer scope is not the exact admitted estate universe"
            )
        if releases and releases != {self._release_ref.key}:
            raise SavedC11AdmissionError(
                "saved consumer scope names a foreign C11 release"
            )
        allowed = {
            self._universe_ref.key,
            self._release_ref.key,
            self._source_ref.key,
        }
        if any(ref.key not in allowed for ref in parsed):
            raise SavedC11AdmissionError(
                "saved consumer scope contains a foreign scope reference"
            )

    def _require_query_scope(self, query: Any) -> None:
        universes = tuple(
            sorted(
                {
                    exact_ref(value, "query.empirical_universe_refs")
                    for value in query.empirical_universe_refs
                },
                key=lambda ref: ref.key,
            )
        )
        if universes != (self._universe_ref,):
            raise SavedC11AdmissionError(
                "saved consumer query is not the exact admitted estate universe"
            )
        self._require_exact_scope_refs(query.scope_refs, "query.scope_refs")

    def _require_predicate_scope(self, predicate: Any) -> None:
        self._require_exact_scope_refs(
            predicate.scope_refs, "predicate.scope_refs",
        )

    def _require_discovery_scope(self, authority: Any) -> None:
        definition = _mapping(
            authority.candidate_universe_definition,
            "discovery candidate_universe_definition",
        )
        for raw in _sequence(definition.get("atoms", ()), "discovery atoms"):
            atom = _mapping(raw, "discovery atom")
            predicate = self._runtime_catalog.resolve_predicate_exact(
                atom.get("predicate_ref")
            )
            self._require_predicate_scope(predicate)
        for raw in _sequence(
            definition.get("query_templates", ()), "discovery query templates"
        ):
            template = _mapping(raw, "discovery query template")
            query = self._runtime_catalog.resolve_query_exact(
                template.get("query_ref")
            )
            self._require_query_scope(query)
        source_scope = getattr(authority, "source_universe_scope", None)
        if isinstance(source_scope, Mapping):
            allowed = source_scope.get("allowed_universe_refs")
            if isinstance(allowed, (tuple, list, set, frozenset)) and allowed:
                allowed_keys = {
                    exact_ref(value, "discovery allowed universe").key
                    for value in allowed
                }
                if self._universe_ref.key not in allowed_keys:
                    raise SavedC11AdmissionError(
                        "saved discovery authority does not allow the admitted estate universe"
                    )

    def resolve_release_exact(self, ref: ExactRef) -> SavedReleaseIdentity:
        """Identity-only exact release resolution for a future Batch handoff."""

        exact = exact_ref(ref, "saved_batch_release_ref")
        if exact != self._release_ref:
            raise SavedC11AdmissionError(
                "saved Batch release ref is not the exact admitted release"
            )
        return SavedReleaseIdentity(self._release_ref)

    def execute_i03(
        self,
        *,
        query_ref: ExactRef | Mapping[str, Any],
        predicate_ref: ExactRef | Mapping[str, Any],
    ) -> Any:
        """Run the existing native I03 owner against the bounded saved estate."""

        self._estate._live()
        query = self._runtime_catalog.resolve_query_exact(query_ref)
        predicate = self._runtime_catalog.resolve_predicate_exact(predicate_ref)
        self._require_query_scope(query)
        self._require_predicate_scope(predicate)
        result = self._executor.execute_i03(
            query_ref=query.ref,
            predicate_ref=predicate.ref,
            group_scope=None,
        )
        # Never serve a result after a revocation that happened mid-query.
        self._estate._live()
        return result

    def execute_i05(
        self,
        *,
        discovery_authority_ref: ExactRef | Mapping[str, Any],
    ) -> Any:
        """Run the existing I05 owner over the same bounded saved estate.

        The S2-C carrier deliberately refuses saved I05; this admission uses
        the original discovery owner directly, with the accepted S2-C session
        as its exact repository view.  No new discovery/statistics engine is
        introduced.
        """

        self._estate._live()
        authority = self._runtime_catalog.resolve_discovery_authority_exact(
            discovery_authority_ref
        )
        self._require_discovery_scope(authority)
        with DirectEstateI03Session(self._estate) as session:
            result = execute_exact_bounded_discovery(
                repository=session,
                discovery_authority=authority,
                authority_registry=self._runtime_catalog.authority_registry,
                release_refs=(self._release_ref,),
                predicate_catalog=self._runtime_catalog.predicates,
                query_template_catalog=self._runtime_catalog.queries,
                group_scope=None,
            )
        # The session checked current at every materialization; this final
        # check prevents release/serve after a mid-result revocation.
        self._estate._live()
        return result


__all__ = [
    "SavedBindingReceipt",
    "SavedC11Admission",
    "SavedC11AdmissionError",
    "SavedReleaseIdentity",
    "SavedWorkloadOwnerHandoffRequired",
]
