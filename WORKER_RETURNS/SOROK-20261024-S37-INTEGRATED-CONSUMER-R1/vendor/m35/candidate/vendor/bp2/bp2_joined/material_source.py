"""First-class B material-source intake for the BP2 pre-C8 occurrence.

The original joined producer only accepts the BP1 composed life. R31J supplied
the GM01 B source through an external producer subclass. This module makes the
source an owned, typed input of the BP2 occurrence builder itself: the owner,
performed operation, quantity, A recipient, clock and source event identity are
validated before the C8 candidate is built, and A's material tool state is
derived from that performed operation rather than from a caller boolean.
"""
from __future__ import annotations

import re
from typing import Any, Mapping

SCHEMA = "BP2_FIRSTCLASS_B_MATERIAL_SOURCE@1"
SOURCE_GRADE = "TEST_ONLY_SOURCEFREE"
SHARE_TOOL = "SHARE_TOOL"
REFUSE_TOOL = "REFUSE_TOOL"
OPERATIONS = (SHARE_TOOL, REFUSE_TOOL)
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_FORBIDDEN_KEYS = frozenset({
    "material_feasible_after",
    "a_performed",
    "a_tool_available",
    "a_tools_remaining",
    "a_inspection",
})
_REQUIRED = (
    "schema", "b_actor", "b_owner", "b_event_ref", "b_event_hash",
    "b_performed", "b_operation", "b_quantity", "b_to_actor", "b_clock",
    "a_e1_ref", "a_e1_hash", "a_e1_clock", "source_grade", "native",
    "psychology_claim",
)


class MaterialSourceRefusal(ValueError):
    """The B material source is not a lawful first-class BP2 input."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise MaterialSourceRefusal("MATERIAL_SOURCE_FIELD_MISSING", name)
    return value


def _integer(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise MaterialSourceRefusal("MATERIAL_SOURCE_FIELD_INVALID", name)
    if value < 0:
        raise MaterialSourceRefusal("MATERIAL_SOURCE_FIELD_NEGATIVE", name)
    return value


def validate_material_source(source: Mapping[str, Any] | None) -> dict:
    """Validate and normalize one owner-bound B material source.

    The envelope describes an independently performed B operation only. An A
    intention, attempt or performed inspection is refused here; A action is
    admitted later by the independent C9/E2 path.
    """
    if not isinstance(source, Mapping):
        raise MaterialSourceRefusal("MATERIAL_SOURCE_MISSING")
    unexpected = _FORBIDDEN_KEYS.intersection(source)
    if unexpected:
        raise MaterialSourceRefusal(
            "MATERIAL_SOURCE_CONFLATES_A_STATE",
            ",".join(sorted(unexpected)),
        )
    missing = [name for name in _REQUIRED if name not in source]
    if missing:
        raise MaterialSourceRefusal(
            "MATERIAL_SOURCE_FIELD_MISSING", ",".join(missing))

    if source["schema"] != SCHEMA:
        raise MaterialSourceRefusal("MATERIAL_SOURCE_SCHEMA_INVALID",
                                    str(source["schema"]))
    actor = _text(source["b_actor"], "b_actor")
    owner = _text(source["b_owner"], "b_owner")
    event_ref = _text(source["b_event_ref"], "b_event_ref")
    event_hash = _text(source["b_event_hash"], "b_event_hash")
    if not _SHA256.match(event_hash):
        raise MaterialSourceRefusal("MATERIAL_SOURCE_EVENT_HASH_INVALID")
    if source["b_performed"] is not True:
        raise MaterialSourceRefusal("MATERIAL_SOURCE_NOT_PERFORMED")
    operation = _text(source["b_operation"], "b_operation")
    if operation not in OPERATIONS:
        raise MaterialSourceRefusal("MATERIAL_SOURCE_OPERATION_INVALID", operation)
    quantity = _integer(source["b_quantity"], "b_quantity")
    if operation == SHARE_TOOL and quantity < 1:
        raise MaterialSourceRefusal("MATERIAL_SOURCE_SHARE_QUANTITY_INVALID")
    if operation == REFUSE_TOOL and quantity != 0:
        raise MaterialSourceRefusal("MATERIAL_SOURCE_REFUSAL_QUANTITY_INVALID")
    recipient = _text(source["b_to_actor"], "b_to_actor")
    clock = _integer(source["b_clock"], "b_clock")
    a_e1_ref = _text(source["a_e1_ref"], "a_e1_ref")
    a_e1_hash = _text(source["a_e1_hash"], "a_e1_hash")
    if not _SHA256.match(a_e1_hash):
        raise MaterialSourceRefusal("MATERIAL_SOURCE_E1_HASH_INVALID")
    a_e1_clock = _integer(source["a_e1_clock"], "a_e1_clock")
    if source["source_grade"] != SOURCE_GRADE:
        raise MaterialSourceRefusal("MATERIAL_SOURCE_GRADE_INVALID")
    if source["native"] is not False:
        raise MaterialSourceRefusal("MATERIAL_SOURCE_NATIVE_CLAIM")
    if source["psychology_claim"] is not False:
        raise MaterialSourceRefusal("MATERIAL_SOURCE_PSYCHOLOGY_CLAIM")

    return {
        "schema": SCHEMA,
        "b_actor": actor,
        "b_owner": owner,
        "b_event_ref": event_ref,
        "b_event_hash": event_hash,
        "b_performed": True,
        "b_operation": operation,
        "b_quantity": quantity,
        "b_to_actor": recipient,
        "b_clock": clock,
        "a_e1_ref": a_e1_ref,
        "a_e1_hash": a_e1_hash,
        "a_e1_clock": a_e1_clock,
        "source_grade": SOURCE_GRADE,
        "native": False,
        "psychology_claim": False,
    }


def material_access(source: Mapping[str, Any] | None) -> str:
    """Derive A's material access from the performed B operation and quantity."""
    if source is None:
        return "granted"
    normalized = validate_material_source(source)
    return "granted" if normalized["b_operation"] == SHARE_TOOL else "denied"


__all__ = [
    "MaterialSourceRefusal",
    "OPERATIONS",
    "REFUSE_TOOL",
    "SCHEMA",
    "SHARE_TOOL",
    "SOURCE_GRADE",
    "material_access",
    "validate_material_source",
]
