"""Bounded LiTS-I physical representation bridge for the exact accepted owner.

This module adapts only the authority-enumerated q301_2/q301_7 decoder
representations.  It does not infer response meaning or change the current
physical-key law; it creates the accepted frozen owner's exact projection and
stream types before that owner performs C11 lookup.
"""
from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any, Iterable

from rawlsing_next.fiabc_lits_i_representation_authority import (
    REPRESENTATION_AUTHORITY_REF,
    SOURCE_SHA256,
    TARGET_VARIABLES,
    authorized_replay_cell,
    representation_authority_snapshot,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell


class LiTSRepresentationBridgeError(ValueError):
    pass


_LOCAL_OWNER_DATACLASSES = frozenset({
    "PhysicalSlot",
    "RowRespondentBinding",
    "OccurrenceRule",
    "ResponseValueRule",
    "ResponseSlotRule",
    "CoordinateValueRule",
    "CoordinateSlotRule",
    "WeightValueRule",
    "WeightSlotRule",
})


def validate_lits_projection_scope(projection: Any) -> None:
    expected = {
        "source_artifact_id": f"urn:rawlsing:source:lits1:sha256:{SOURCE_SHA256}",
        "expected_source_sha256": SOURCE_SHA256,
        "source_family_id": "LiTS",
        "study_product_id": "Life in Transition Survey 2006",
        "instrument_release_id": "LiTS-I Final questionnaire 2006",
    }
    observed = {name: getattr(projection, name, None) for name in expected}
    if observed != expected:
        raise LiTSRepresentationBridgeError(
            f"LiTS representation authority source/wave scope mismatch: {observed!r}"
        )
    response_slots = {
        (slot.slot.ordinal, slot.slot.name) for slot in getattr(projection, "response_slots", ())
    }
    target_slots = {(ordinal, name) for name, ordinal in TARGET_VARIABLES.items()}
    if response_slots != target_slots:
        raise LiTSRepresentationBridgeError("LiTS response projection differs from exact authority slots")
    if getattr(projection, "weight_slots", ()):
        raise LiTSRepresentationBridgeError("LiTS accepted representation projection unexpectedly has weights")


def authorized_lits_cell(*, source_sha256: str, cell: PhysicalCell) -> PhysicalCell:
    """Transform exact targets; reject partial target-coordinate matches."""
    if source_sha256 != SOURCE_SHA256:
        raise LiTSRepresentationBridgeError("LiTS representation authority source SHA mismatch")
    if not isinstance(cell, PhysicalCell):
        raise LiTSRepresentationBridgeError("LiTS representation bridge requires an exact PhysicalCell")
    target_ordinals = frozenset(TARGET_VARIABLES.values())
    target_name = cell.variable_name in TARGET_VARIABLES
    target_ordinal = cell.variable_ordinal in target_ordinals
    if not target_name and not target_ordinal:
        return cell
    if TARGET_VARIABLES.get(cell.variable_name) != cell.variable_ordinal:
        raise LiTSRepresentationBridgeError("LiTS representation target name/slot pair mismatch")
    try:
        return authorized_replay_cell(source_sha256=source_sha256, cell=cell)
    except (TypeError, ValueError) as exc:
        raise LiTSRepresentationBridgeError(str(exc)) from exc


def _owner_dataclass(value: Any, owner_module: Any) -> Any:
    name = type(value).__name__
    if name in _LOCAL_OWNER_DATACLASSES:
        owner_type = getattr(owner_module, name, None)
        if owner_type is None or not is_dataclass(owner_type):
            raise LiTSRepresentationBridgeError(f"exact owner type {name} is unavailable")
        try:
            return owner_type(**{
                field.name: _owner_dataclass(getattr(value, field.name), owner_module)
                for field in fields(value)
            })
        except Exception as exc:
            raise LiTSRepresentationBridgeError(f"exact owner rejected reconstructed {name}") from exc
    if isinstance(value, tuple):
        return tuple(_owner_dataclass(item, owner_module) for item in value)
    if isinstance(value, list):
        return [_owner_dataclass(item, owner_module) for item in value]
    return value


def reconstruct_exact_owner_projection(
    *, current_projection: Any, adapted_projection: Any, owner_module: Any
) -> tuple[Any, dict[str, Any]]:
    """Rebuild every frozen-owner-local dataclass without dropping fields."""
    validate_lits_projection_scope(current_projection)
    current_fields = {field.name for field in fields(adapted_projection)}
    owner_type = getattr(owner_module, "GovernedC11Projection", None)
    if owner_type is None or not is_dataclass(owner_type):
        raise LiTSRepresentationBridgeError("exact B owner projection class is unavailable")
    owner_fields = {field.name for field in fields(owner_type)}
    unsupported = current_fields - owner_fields
    missing = owner_fields - current_fields
    if missing:
        raise LiTSRepresentationBridgeError(
            f"exact B owner requires projection fields absent from the current projection: {sorted(missing)!r}"
        )
    if not unsupported <= {"slot_owner_sets"} or tuple(getattr(current_projection, "slot_owner_sets", ())) != ():
        raise LiTSRepresentationBridgeError(
            f"exact B owner cannot represent current projection fields without loss: {sorted(unsupported)!r}"
        )
    try:
        values = {
            field.name: _owner_dataclass(getattr(adapted_projection, field.name), owner_module)
            for field in fields(owner_type)
        }
        rebuilt = owner_type(**values)
    except LiTSRepresentationBridgeError:
        raise
    except Exception as exc:
        raise LiTSRepresentationBridgeError("exact B owner rejected reconstructed projection") from exc
    if not isinstance(rebuilt, owner_type):
        raise LiTSRepresentationBridgeError("projection is outside the exact B type universe")
    nested_counts = {}
    for name in sorted(_LOCAL_OWNER_DATACLASSES):
        nested_counts[name] = sum(
            1 for item in _walk_dataclasses(rebuilt) if type(item) is getattr(owner_module, name, None)
        )
    if any(type(item).__name__ in _LOCAL_OWNER_DATACLASSES and type(item).__module__ != owner_module.__name__
           for item in _walk_dataclasses(rebuilt)):
        raise LiTSRepresentationBridgeError("projection retained a foreign nested owner type")
    if rebuilt.cache_identity != adapted_projection.cache_identity:
        raise LiTSRepresentationBridgeError("exact B projection cache identity drift")
    return rebuilt, {
        "schema": "FIABC_LITS_EXACT_B_OWNER_PROJECTION_RECONSTRUCTION@1.0.0",
        "projection_cache_identity": rebuilt.cache_identity,
        "owner_module": owner_module.__name__,
        "top_level_type": f"{type(rebuilt).__module__}.{type(rebuilt).__qualname__}",
        "nested_owner_type_counts": nested_counts,
        "unsupported_empty_fields_omitted": sorted(unsupported),
        "field_loss": False,
        "semantic_inference": False,
    }


def _walk_dataclasses(value: Any) -> Iterable[Any]:
    if is_dataclass(value) and not isinstance(value, type):
        yield value
        for field in fields(value):
            yield from _walk_dataclasses(getattr(value, field.name))
    elif isinstance(value, (tuple, list)):
        for item in value:
            yield from _walk_dataclasses(item)


def representation_authority_receipt(*, projection: Any, transformed_counts: dict[str, int]) -> dict[str, Any]:
    validate_lits_projection_scope(projection)
    snapshot = representation_authority_snapshot()
    return {
        "schema": "FIABC_LITS_BOUNDED_REPRESENTATION_BINDING_RECEIPT@1.0.0",
        "authority_ref": REPRESENTATION_AUTHORITY_REF.as_dict(),
        "authority_snapshot": snapshot.as_dict(),
        "source_artifact_id": projection.source_artifact_id,
        "source_sha256": projection.expected_source_sha256,
        "source_family_id": projection.source_family_id,
        "instrument_release_id": projection.instrument_release_id,
        "target_slots": [
            {"ordinal": ordinal, "name": name}
            for name, ordinal in TARGET_VARIABLES.items()
        ],
        "transformed_cell_counts": dict(sorted(transformed_counts.items())),
        "generic_numeric_coercion": False,
        "labels_or_frequencies_used": False,
        "missingness_inferred": False,
        "authority_snapshot_identity": REPRESENTATION_AUTHORITY_REF.authority_content_hash,
    }
