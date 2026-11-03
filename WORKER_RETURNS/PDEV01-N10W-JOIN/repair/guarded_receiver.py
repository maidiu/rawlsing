"""Exact J42 provider/version/currentness guard for the existing joined receiver.

This is an isolated candidate overlay. It does not edit production. The exact
provider identities are the existing constants in the actual J42 joined service
(``j42_join.py:J42P41Service.progressive``), not a new trust rule. The N9
selected clock is the actual ``j42_bindings.w41_clock`` carried by the receipt.
"""
from __future__ import annotations

from copy import deepcopy
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


def _refusal(code: str, request: JoinedWorldSelectionRequest) -> JoinedWorldSelectedView:
    field_ids = tuple(field.field_id for field in request.fields)
    material = {
        "state": "REFUSED",
        "reason_code": code,
        "view_key": request.view_key,
        "field_ids": list(field_ids),
        "guard": "PDEV01_J42_EXACT_IDENTITY_GUARD@1",
        "provider_source": J42_PROVIDER_SOURCE,
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
    binding = p41.get("j42_bindings") or {}
    clock = binding.get("w41_clock") or {}
    selection = n9.get("selection") or {}
    if any(selection.get(key) != clock.get(key) for key in N9_SELECTION_FIELDS):
        return "JOINED_N9_SELECTION_MISMATCH"
    if "test_now" in selection and selection.get("test_now") != clock.get("test_now"):
        return "JOINED_N9_SELECTION_MISMATCH"
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
    """Reject any J42 identity/currentness/clock/hash bypass, then use the real receiver."""
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
    "guarded_select_joined_world_view",
]
