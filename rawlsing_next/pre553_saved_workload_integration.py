"""S2-D saved-workload integration surface.

Only the I03 and I05 readers can be integrated lawfully in the new S2-D files
without changing a shared owner file.  The remaining original readers need an
exact owner acknowledgement for the existing Batch, issued-workload and joined
resume owners.  Those dependencies are exposed as typed refusals here rather
than faked with a C11Repository subclass, guard monkeypatch, synthetic receipt
or in-memory compatibility estate.

The actual accepted S2-C physical reader and the actual existing I03/I05
scientific owners remain in their original modules.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission,
    SavedC11AdmissionError,
    SavedWorkloadOwnerHandoffRequired,
)


def execute_saved_i03(
    admission: SavedC11Admission,
    *,
    query_ref: Any,
    predicate_ref: Any,
) -> Any:
    """Execute one exact normal I03 request on the admitted saved estate."""

    if type(admission) is not SavedC11Admission:
        raise SavedC11AdmissionError("exact SavedC11Admission required")
    return admission.execute_i03(query_ref=query_ref, predicate_ref=predicate_ref)


def execute_saved_i05(
    admission: SavedC11Admission,
    *,
    discovery_authority_ref: Any,
) -> Any:
    """Execute one exact I05 frontier on the admitted saved estate."""

    if type(admission) is not SavedC11Admission:
        raise SavedC11AdmissionError("exact SavedC11Admission required")
    return admission.execute_i05(discovery_authority_ref=discovery_authority_ref)


def require_batch_owner_ack() -> None:
    """Raise the exact Batch integration dependency, never a fake pass."""

    raise SavedWorkloadOwnerHandoffRequired(
        code="S2D_BATCH_OWNER_ACK_REQUIRED",
        owner="BatchExecutionRunner owner",
        path="rawlsing_next/pre553_batch_runner.py",
        function="BatchExecutionRunner.__init__",
        minimum_edit=(
            "accept the exact SavedC11Admission union (or a narrow owner-approved "
            "saved repository surface) at the line-402 C11Repository guard and "
            "resolve only its exact SavedReleaseIdentity; never construct or "
            "accept a full C11LogicalRelease/repository graph"
        ),
        detail=(
            "The existing runner only calls repository.resolve_release_exact in "
            "__init__. The saved admission already exposes exact identity-only "
            "resolution, but the shared guard is READONLY pending owner ACK."
        ),
    )


def execute_saved_batch(*_args: Any, **_kwargs: Any) -> Any:
    require_batch_owner_ack()


def require_normal_owner_ack() -> None:
    """Raise the exact normal issued-workload integration dependency."""

    raise SavedWorkloadOwnerHandoffRequired(
        code="S2D_NORMAL_OWNER_ACK_REQUIRED",
        owner="S1-D/issued-workload owner",
        path="rawlsing_next/pre553_issued_workload.py",
        function="execute_issued_workload",
        minimum_edit=(
            "add an optional exact saved_admission parameter; when supplied, "
            "skip source_factory, build_source_backed_c11_repository and the "
            "legacy route/C11 rebuild, and drive the existing Batch/I03/I05 "
            "owners on the admitted estate while retaining current and fate checks"
        ),
        detail=(
            "The startup function unconditionally calls source_factory -> "
            "build_source_backed_c11_repository -> BatchExecutionRunner. A new "
            "orchestrator would duplicate the existing issued-workload owner."
        ),
    )


def execute_saved_normal(*_args: Any, **_kwargs: Any) -> Any:
    require_normal_owner_ack()


def require_resume_owner_ack() -> None:
    """Raise the exact joined-resume/checkpoint integration dependency."""

    raise SavedWorkloadOwnerHandoffRequired(
        code="S2D_RESUME_OWNER_ACK_REQUIRED",
        owner="S1-D/issued-workload checkpoint owner",
        path="rawlsing_next/pre553_issued_workload.py",
        function="resume_joined_workloads / JoinedWorkloadCheckpoint / capture_joined_checkpoint",
        minimum_edit=(
            "bind the exact saved-estate manifest, ExternalI02Roots and "
            "reconstructed v1 release to completed/partial/absent entries, and "
            "use the optional saved_admission path on resume while preserving "
            "current, prior receipts/outputs and no-drop receipts. Add an "
            "owner-approved schema field or exact external custody envelope."
        ),
        detail=(
            "JoinedWorkloadCheckpoint v2 contains decision/envelope/source/manifest/"
            "unit/output/receipt material but no saved-estate identity. Absent and "
            "partial branches re-enter execute_issued_workload and currently rebuild "
            "source/full C11."
        ),
    )


def execute_saved_completed(*_args: Any, **_kwargs: Any) -> Any:
    require_resume_owner_ack()


def execute_saved_partial(*_args: Any, **_kwargs: Any) -> Any:
    require_resume_owner_ack()


def execute_saved_absent(*_args: Any, **_kwargs: Any) -> Any:
    require_resume_owner_ack()


def saved_reader_capabilities() -> Mapping[str, Any]:
    """Expose the honest new-module capability boundary, not a fake seven-pass."""

    return {
        "schema": "PYAT991_S2D_SAVED_WORKLOAD_CAPABILITIES@1",
        "implemented_here": ["I03", "I05"],
        "blocked_owner_ack": {
            "Batch": "rawlsing_next/pre553_batch_runner.py::BatchExecutionRunner.__init__",
            "NORMAL": "rawlsing_next/pre553_issued_workload.py::execute_issued_workload",
            "COMPLETED": "rawlsing_next/pre553_issued_workload.py::resume_joined_workloads",
            "PARTIAL": "rawlsing_next/pre553_issued_workload.py::resume_joined_workloads",
            "ABSENT": "rawlsing_next/pre553_issued_workload.py::resume_joined_workloads",
        },
        "preserved": [
            "accepted S2-C VerifiedDirectEstate/DirectEstateI03Session",
            "existing execute_empirical_query I03 semantics",
            "existing execute_exact_bounded_discovery I05 semantics",
            "external manifest/I02 roots and live current callback",
            "no C11Repository/C11LogicalRelease/full replay closure requirement",
            "no source reopen or second persistent body corpus",
        ],
    }


__all__ = [
    "execute_saved_absent",
    "execute_saved_batch",
    "execute_saved_completed",
    "execute_saved_i03",
    "execute_saved_i05",
    "execute_saved_normal",
    "execute_saved_partial",
    "require_batch_owner_ack",
    "require_normal_owner_ack",
    "require_resume_owner_ack",
    "saved_reader_capabilities",
]
