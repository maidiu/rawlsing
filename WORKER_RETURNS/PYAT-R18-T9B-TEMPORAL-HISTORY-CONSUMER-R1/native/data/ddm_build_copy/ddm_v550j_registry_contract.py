"""Shared executable-registry contract for V550J registry consumers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

EXECUTABLE_JOINT_REGISTRY_STATUSES = frozenset({"active", "approved", "certified", "governed"})
NONEXECUTABLE_JOINT_REGISTRY_STATUSES = frozenset({"draft", "review_only"})

REGISTRY_AUTHORITY_EXECUTABLE = "executable"
REGISTRY_AUTHORITY_NOT_APPLICABLE = "not_applicable"
REGISTRY_AUTHORITY_MISSING = "authority_missing"
REGISTRY_AUTHORITY_NON_EXECUTABLE = "authority_non_executable"

REQUIRED_P3_AUTHORITY_RELEASE_ID = "P3-AUTHORITY-2026-08-02-R184"
SECTION85_JOINT_CONFIGURATION_AUTHORITY_RELEASE_ID = "V550J-BOUNDED-AUTHORITY-2026-08-02-R1"
LAYER1_JOINT_CONFIGURATION_AUTHORITY_RELEASE_ID = "V550J-LAYER1-AUDIT-AUTHORITY-2026-08-03-R1"
ACCEPTED_JOINT_CONFIGURATION_AUTHORITY_RELEASE_IDS = frozenset(
    {
        SECTION85_JOINT_CONFIGURATION_AUTHORITY_RELEASE_ID,
        LAYER1_JOINT_CONFIGURATION_AUTHORITY_RELEASE_ID,
    }
)


class RegistryAuthorityError(RuntimeError):
    """Typed fail-closed error for unavailable or non-executable registry authority."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        authority_name: str = "",
        path: str | Path | None = None,
        status: Any = None,
    ) -> None:
        self.code = str(code).strip()
        self.authority_name = str(authority_name).strip()
        self.path = "" if path is None else str(path)
        self.status = clean_registry_value(status).lower()
        super().__init__(message)


def clean_registry_value(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def registry_status_is_executable(value: Any) -> bool:
    return clean_registry_value(value).lower() in EXECUTABLE_JOINT_REGISTRY_STATUSES


def registry_authority_state(value: Any, *, applicable: bool = True) -> str:
    """Return a typed execution state without weakening status semantics."""
    if not applicable:
        return REGISTRY_AUTHORITY_NOT_APPLICABLE
    status = clean_registry_value(value).lower()
    if not status:
        return REGISTRY_AUTHORITY_MISSING
    if status in EXECUTABLE_JOINT_REGISTRY_STATUSES:
        return REGISTRY_AUTHORITY_EXECUTABLE
    return REGISTRY_AUTHORITY_NON_EXECUTABLE


def require_executable_registry_status(
    value: Any,
    *,
    authority_name: str = "joint registry",
    path: str | Path | None = None,
) -> str:
    status = clean_registry_value(value).lower()
    state = registry_authority_state(status, applicable=True)
    if state == REGISTRY_AUTHORITY_MISSING:
        raise RegistryAuthorityError(
            "registry_authority_missing",
            f"{authority_name} authority is missing an executable status",
            authority_name=authority_name,
            path=path,
            status=status,
        )
    if state != REGISTRY_AUTHORITY_EXECUTABLE:
        raise RegistryAuthorityError(
            "registry_status_not_executable",
            f"{authority_name} is not executable: status={status}",
            authority_name=authority_name,
            path=path,
            status=status,
        )
    return status


def require_p3_authority_release(value: Any) -> str:
    release_id = clean_registry_value(value)
    if release_id != REQUIRED_P3_AUTHORITY_RELEASE_ID:
        raise RuntimeError(f"unexpected P3 authority release: {release_id}")
    return release_id


def require_joint_configuration_authority_release(value: Any) -> str:
    release_id = clean_registry_value(value)
    if release_id not in ACCEPTED_JOINT_CONFIGURATION_AUTHORITY_RELEASE_IDS:
        raise RuntimeError(f"unexpected joint-configuration authority release: {release_id}")
    return release_id
