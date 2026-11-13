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

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor,
    RuntimeObjectCatalog,
)
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
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
        }


class SavedC11Admission:
    """One exact accepted S2-C estate with bounded native I03/I05 consumers."""

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
        if release_ref != estate.reconstructed_v1_release_ref:
            raise SavedC11AdmissionError(
                "saved release ref differs from the estate's reconstructed v1 identity"
            )
        self.estate = estate
        self.release_ref = release_ref
        self.runtime_catalog = runtime_catalog
        # Constructing the existing carrier performs the exact type, release,
        # current and catalog checks without asking for a C11 repository.
        self._executor = CarrierNeutralResearchExecutor(
            repository=estate,
            release_refs=(release_ref,),
            runtime_catalog=runtime_catalog,
        )
        self.estate._live()

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
        return cls(
            estate=estate,
            release_ref=release_ref,
            runtime_catalog=runtime_catalog,
        )

    @property
    def manifest_sha256(self) -> str:
        return self.estate.held_manifest_sha256

    @property
    def i02(self) -> ExternalI02Roots:
        return self.estate.i02

    @property
    def estate_path(self) -> str:
        return self.estate.directory.as_posix()

    def binding_receipt(self) -> SavedBindingReceipt:
        return SavedBindingReceipt(
            schema="PYAT991_S2D_SAVED_C11_ADMISSION@1",
            manifest_sha256=self.manifest_sha256,
            i02=self.i02,
            release_ref=self.release_ref,
            estate_path=self.estate_path,
            runtime_catalog=self.runtime_catalog.receipt(),
        )

    def resolve_release_exact(self, ref: ExactRef) -> SavedReleaseIdentity:
        """Identity-only exact release resolution for a future Batch handoff."""

        exact = exact_ref(ref, "saved_batch_release_ref")
        if exact != self.release_ref:
            raise SavedC11AdmissionError(
                "saved Batch release ref is not the exact admitted release"
            )
        return SavedReleaseIdentity(self.release_ref)

    def execute_i03(
        self,
        *,
        query_ref: ExactRef | Mapping[str, Any],
        predicate_ref: ExactRef | Mapping[str, Any],
    ) -> Any:
        """Run the existing native I03 owner against the bounded saved estate."""

        self.estate._live()
        result = self._executor.execute_i03(
            query_ref=query_ref,
            predicate_ref=predicate_ref,
            group_scope=None,
        )
        # Never serve a result after a revocation that happened mid-query.
        self.estate._live()
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

        self.estate._live()
        authority = self.runtime_catalog.resolve_discovery_authority_exact(
            discovery_authority_ref
        )
        with DirectEstateI03Session(self.estate) as session:
            result = execute_exact_bounded_discovery(
                repository=session,
                discovery_authority=authority,
                authority_registry=self.runtime_catalog.authority_registry,
                release_refs=(self.release_ref,),
                predicate_catalog=self.runtime_catalog.predicates,
                query_template_catalog=self.runtime_catalog.queries,
                group_scope=None,
            )
        # The session checked current at every materialization; this final
        # check prevents release/serve after a mid-result revocation.
        self.estate._live()
        return result


__all__ = [
    "SavedBindingReceipt",
    "SavedC11Admission",
    "SavedC11AdmissionError",
    "SavedReleaseIdentity",
    "SavedWorkloadOwnerHandoffRequired",
]
