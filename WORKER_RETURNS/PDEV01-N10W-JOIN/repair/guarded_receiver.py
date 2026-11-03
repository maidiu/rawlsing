"""Exact J42 provider/version/currentness/clock guard for the joined receiver.

This is an isolated candidate overlay. It does not edit production. Provider
identities are the existing constants in the actual J42 joined service
(``j42_join.py:J42P41Service.progressive``). The selected clock is read from
the independently pinned W41 returned artifact, never trusted from the caller
receipt's mutually consistent fields.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_universal_world_binding import (
    JoinedWorldSelectedView,
    JoinedWorldSelectionRequest,
    select_joined_world_view,
)


P41_SCHEMA = "PYAT_R41_P41_GENERIC_POSSIBILITY_RECEIPT@1"
P41_SERVICE = "P41_GENERIC_POSSIBILITY_SERVICE@1"
J42_CONTRACT = "J42_JOINED_E41_W41_P41_PREV3_CONSUMER@1"

# Exact values from actual J42 j42_join.py:J42P41Service.progressive.
EXPECTED_PROVIDERS = {
    "n9_world": "W41_READONLY_SOURCE_QUALIFIED_WORLD@1",
    "n10e_empirical": "E41_N10E_EMPIRICAL_POSSIBILITY_SLICE_PROVIDER_EXT@1.1.0",
    "n10w_progressive": "P41_GENERIC_POSSIBILITY_SERVICE@1",
    "learned_release": "E04L_M1_M2_B5_READTHROUGH@1",
}
N9_CURRENTNESS = "CURRENT_TEST_ONLY_SELECTION"
N9_SELECTION_FIELDS = ("mode", "valid_at", "published_asof")
J42_PROVIDER_SOURCE = (
    "f53cb0d2bce52640268c844c398bbd8007d28edc:"
    "WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-"
    "CONSUMER-R1/runtime/j42_join.py"
)
W41_COMMIT = "b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2"
W41_ARTIFACT_PATH = (
    "WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/"
    "current_historical_asof_world_consumer_receipts.json"
)
W41_ARTIFACT_SHA256 = "09a92d6c00e867a44712b225cadd352b7d41a2038384de26de34f5c10a9185e7"
_REPO = Path(__file__).resolve().parents[2]
_W41_WORLDS: dict[str, Any] | None = None


class W41ClockAuthorityError(ValueError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _load_w41_worlds() -> dict[str, Any]:
    """Load the accepted W41 artifact by exact commit/path and verify its SHA."""
    global _W41_WORLDS
    if _W41_WORLDS is not None:
        return _W41_WORLDS
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(_REPO), "show", f"{W41_COMMIT}:{W41_ARTIFACT_PATH}"],
            stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        raise W41ClockAuthorityError("W41_CLOCK_ARTIFACT_UNAVAILABLE") from exc
    if hashlib.sha256(raw).hexdigest() != W41_ARTIFACT_SHA256:
        raise W41ClockAuthorityError("W41_CLOCK_ARTIFACT_HASH_MISMATCH")
    try:
        worlds = json.loads(raw)["worlds"]
    except Exception as exc:
        raise W41ClockAuthorityError("W41_CLOCK_ARTIFACT_SHAPE_INVALID") from exc
    if not isinstance(worlds, dict):
        raise W41ClockAuthorityError("W41_CLOCK_ARTIFACT_SHAPE_INVALID")
    _W41_WORLDS = worlds
    return worlds


def _refusal(code: str, request: JoinedWorldSelectionRequest) -> JoinedWorldSelectedView:
    field_ids = tuple(field.field_id for field in request.fields)
    material = {
        "state": "REFUSED",
        "reason_code": code,
        "view_key": request.view_key,
        "field_ids": list(field_ids),
        "guard": "PDEV01_J42_EXACT_IDENTITY_GUARD@2",
        "provider_source": J42_PROVIDER_SOURCE,
        "w41_artifact_sha256": W41_ARTIFACT_SHA256,
    }
    return JoinedWorldSelectedView(
        state="REFUSED",
        reason_code=code,
        view_key=request.view_key,
        field_ids=field_ids,
        consumer_values_read=None,
        view_hash=semantic_hash(material),
    )


def _receipts(request: JoinedWorldSelectionRequest) -> tuple[Any, Any]:
    receipts = request.joined_receipts
    if not isinstance(receipts, Mapping):
        return None, None
    return (
        (receipts.get("p41_joined_receipts") or {}).get(request.view_key),
        (receipts.get("joined_consumer_receipts") or {}).get(request.view_key),
    )


def _identity_error(request: JoinedWorldSelectionRequest) -> str | None:
    p41, joined = _receipts(request)
    if not isinstance(p41, Mapping) or not isinstance(joined, Mapping):
        return "JOINED_VIEW_NOT_FOUND"
    if p41.get("schema") != P41_SCHEMA or p41.get("service") != P41_SERVICE:
        return "JOINED_CONSUMER_CONTRACT_MISMATCH"
    providers = p41.get("providers") or {}
    if providers != EXPECTED_PROVIDERS:
        return "JOINED_PROVIDER_IDENTITY_MISMATCH"
    n9 = p41.get("n9_world") or {}
    if n9.get("currentness") != N9_CURRENTNESS:
        return "JOINED_N9_CURRENTNESS_INVALID"

    # Trusted clock: exact W41 world by the J42 lookup key, not caller fields.
    try:
        worlds = _load_w41_worlds()
    except W41ClockAuthorityError as exc:
        return exc.code
    expected_world = worlds.get(request.view_key)
    if not isinstance(expected_world, Mapping):
        return "W41_CLOCK_VIEW_ABSENT"
    trusted_clock = expected_world.get("clock")
    if not isinstance(trusted_clock, Mapping):
        return "W41_CLOCK_ABSENT"

    selection = n9.get("selection") or {}
    if any(selection.get(key) != trusted_clock.get(key) for key in N9_SELECTION_FIELDS):
        return "JOINED_N9_SELECTION_MISMATCH"
    binding = p41.get("j42_bindings") or {}
    binding_clock = binding.get("w41_clock") or {}
    if binding_clock != trusted_clock:
        return "JOINED_W41_CLOCK_BINDING_MISMATCH"

    # Preserve the existing P41 receipt-integrity contract; this is not the
    # authority for the clock.
    expected_hash = p41.get("content_hash")
    if not expected_hash:
        return "JOINED_RECEIPT_CONTENT_HASH_MISMATCH"
    material = {key: value for key, value in p41.items() if key != "content_hash"}
    if semantic_hash(material) != expected_hash:
        return "JOINED_RECEIPT_CONTENT_HASH_MISMATCH"
    return None


def guarded_select_joined_world_view(
    request: JoinedWorldSelectionRequest,
) -> JoinedWorldSelectedView:
    """Reject identity/currentness/trusted-clock/hash bypass, then use the real receiver."""
    problem = _identity_error(request)
    if problem is not None:
        return _refusal(problem, request)
    return select_joined_world_view(request)


__all__ = [
    "EXPECTED_PROVIDERS",
    "N9_CURRENTNESS",
    "N9_SELECTION_FIELDS",
    "J42_CONTRACT",
    "J42_PROVIDER_SOURCE",
    "W41_ARTIFACT_SHA256",
    "W41ClockAuthorityError",
    "guarded_select_joined_world_view",
]
