"""Prepared cold saved-I03/I05 session over one admitted S2-C estate.

Versioned TEST_ONLY reader surface.  It reuses the existing
``DirectEstateI03Session`` posting index and the existing native I03/I05
evaluators across many operations.  It does not create a second evaluator,
store, C11 repository, authority system or scientific issuer.

The prepared session is additive: ``SavedC11Admission.execute_i03`` and
``execute_i05`` keep their one-operation behavior.  This module is a candidate
for owner-qualified receiving, not a production grant.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator

from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission, SavedC11AdmissionError,
)

PREPARED_SAVED_I03_SCHEMA = "PYAT_PREP_SAVED_I03@1.0.0"


class PreparedSavedI03Error(SavedC11AdmissionError):
    """The prepared session is closed, retargeted or outside exact scope."""


@dataclass(frozen=True)
class PreparedSessionReceipt:
    schema: str
    manifest_sha256: str
    release_ref: ExactRef
    estate_path: str
    operations: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "manifest_sha256": self.manifest_sha256,
            "release_ref": self.release_ref.as_dict(),
            "estate_path": self.estate_path,
            "operations": self.operations,
        }


class PreparedI03Session:
    """One exact saved posting index reused by many I03/I05 operations."""

    __slots__ = ("_admission", "_session", "_operations", "_closed")

    def __init__(
        self, admission: SavedC11Admission, session: DirectEstateI03Session,
    ) -> None:
        if type(admission) is not PreparedSavedC11Admission:
            raise PreparedSavedI03Error("exact prepared saved admission required")
        if type(session) is not DirectEstateI03Session:
            raise PreparedSavedI03Error("exact DirectEstateI03Session required")
        self._admission = admission
        self._session = session
        self._operations = 0
        self._closed = False

    def _require_open(self) -> None:
        if self._closed:
            raise PreparedSavedI03Error("prepared saved I03 session is closed")
        self._admission.check_current()

    def _copy_query(self, query_ref: ExactRef | Any):
        catalog = self._admission._runtime_catalog
        query = catalog.resolve_query_exact(query_ref)
        self._admission._require_query_scope(query)
        return query

    def _copy_predicate(self, predicate_ref: ExactRef | Any):
        catalog = self._admission._runtime_catalog
        predicate = catalog.resolve_predicate_exact(predicate_ref)
        self._admission._require_predicate_scope(predicate)
        return predicate

    def execute_i03(self, *, query_ref: Any, predicate_ref: Any) -> Any:
        """Execute one exact I03 operation on the shared prepared index."""

        self._require_open()
        query = self._copy_query(query_ref)
        predicate = self._copy_predicate(predicate_ref)
        condition = exact_ref(
            query.condition_predicate_ref, "query.condition_predicate_ref",
        )
        if condition != predicate.ref:
            raise PreparedSavedI03Error(
                "prepared I03 predicate is not the exact query condition"
            )
        result = execute_empirical_query(
            repository=self._session,
            query=query,
            predicate=predicate,
            authority_registry=self._admission._runtime_catalog.authority_registry,
            release_refs=(self._admission._release_ref,),
        )
        self._admission.check_current()
        self._operations += 1
        return result

    def execute_i05(self, *, discovery_authority_ref: Any) -> Any:
        """Execute one exact I05 discovery on the shared prepared index."""

        self._require_open()
        catalog = self._admission._runtime_catalog
        authority = catalog.resolve_discovery_authority_exact(
            discovery_authority_ref
        )
        self._admission._require_discovery_scope(authority)
        result = execute_exact_bounded_discovery(
            repository=self._session,
            discovery_authority=authority,
            authority_registry=catalog.authority_registry,
            release_refs=(self._admission._release_ref,),
            predicate_catalog=catalog.predicates,
            query_template_catalog=catalog.queries,
            group_scope=None,
        )
        self._admission.check_current()
        self._operations += 1
        return result

    def receipt(self) -> PreparedSessionReceipt:
        return PreparedSessionReceipt(
            schema=PREPARED_SAVED_I03_SCHEMA,
            manifest_sha256=self._admission.manifest_sha256,
            release_ref=self._admission.release_ref,
            estate_path=self._admission.estate_path,
            operations=self._operations,
        )

    def close(self) -> None:
        if not self._closed:
            self._session.__exit__(None, None, None)
            self._closed = True

    def __enter__(self) -> "PreparedI03Session":
        self._require_open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


class PreparedSavedC11Admission(SavedC11Admission):
    """A SavedC11Admission that can expose one prepared exact session.

    The inherited admission construction, pins, catalog snapshot and current
    checks are unchanged.  Only the explicit prepared context is added.
    """

    __slots__ = ()

    @classmethod
    def from_verified_admission(
        cls, admitted: SavedC11Admission,
    ) -> "PreparedSavedC11Admission":
        """Upgrade ONE already authenticated saved estate to prepared reading.

        Reuse the original independently pinned private estate and exact frozen
        catalog, not a new caller-supplied root, an inferred release, or an
        extra whole-estate hash pass. The existing _initialize path rechecks
        release/catalog/current and snapshots its catalog. This is only an
        execution-local reuse capability, not a source/science permission.
        """
        if type(admitted) is not SavedC11Admission:
            raise PreparedSavedI03Error(
                "EXACT_EXISTING_SAVED_ADMISSION_REQUIRED"
            )
        admitted.check_current()
        return cls._from_verified_estate(
            admitted._estate,
            admitted.release_ref,
            admitted._runtime_catalog,
        )

    @contextmanager
    def prepared_i03(self) -> Iterator[PreparedI03Session]:
        self.check_current()
        session = DirectEstateI03Session(self._estate)
        session.__enter__()
        prepared = PreparedI03Session(self, session)
        try:
            yield prepared
        finally:
            prepared.close()


__all__ = [
    "PREPARED_SAVED_I03_SCHEMA",
    "PreparedI03Session",
    "PreparedSavedC11Admission",
    "PreparedSavedI03Error",
    "PreparedSessionReceipt",
]
