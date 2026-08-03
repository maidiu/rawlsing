"""Shared executable-registry contract for V550J registry consumers."""

from __future__ import annotations

from typing import Any

EXECUTABLE_JOINT_REGISTRY_STATUSES = frozenset({"active", "approved", "certified", "governed"})
NONEXECUTABLE_JOINT_REGISTRY_STATUSES = frozenset({"draft", "review_only"})

REQUIRED_P3_AUTHORITY_RELEASE_ID = "P3-AUTHORITY-2026-08-02-R184"
SECTION85_JOINT_CONFIGURATION_AUTHORITY_RELEASE_ID = "V550J-BOUNDED-AUTHORITY-2026-08-02-R1"
LAYER1_JOINT_CONFIGURATION_AUTHORITY_RELEASE_ID = "V550J-LAYER1-AUDIT-AUTHORITY-2026-08-03-R1"
ACCEPTED_JOINT_CONFIGURATION_AUTHORITY_RELEASE_IDS = frozenset(
    {
        SECTION85_JOINT_CONFIGURATION_AUTHORITY_RELEASE_ID,
        LAYER1_JOINT_CONFIGURATION_AUTHORITY_RELEASE_ID,
    }
)


def clean_registry_value(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def registry_status_is_executable(value: Any) -> bool:
    return clean_registry_value(value).lower() in EXECUTABLE_JOINT_REGISTRY_STATUSES


def require_executable_registry_status(value: Any) -> str:
    status = clean_registry_value(value).lower()
    if status not in EXECUTABLE_JOINT_REGISTRY_STATUSES:
        raise RuntimeError(f"joint registry is not executable: status={status or 'missing'}")
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
