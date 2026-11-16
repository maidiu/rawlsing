"""Sourcefree fixture actor sources: NOT native ADP007 actor issuance.

A BP1 actor source is a declared TEST_ONLY fixture origin. It carries an actor
id, a source reference, a role, a birth clock, sparsity/unknowns and no
psychology. The source hash is a content identity; it is not a native issuer
signature. A native actor/ADP007 source must be supplied by the competent owner
and is explicitly out of scope here.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from .canon import digest, seal, valid

BP1_ACTOR_SOURCE_SCHEMA = "BP1_SOURCEFREE_ACTOR_SOURCE@1"
BP1_ACTOR_SOURCE_GRADE = "SOURCEFREE_FIXTURE_ACTOR_NOT_NATIVE"
BP1_NATIVE_GRANT = "NOT_GRANTED"
TEST_ONLY_PREFIX = "TEST_ONLY_BP1_"
ALLOWED_ROLES = frozenset({"repair", "finishing"})
ALLOWED_EVENT_PERMISSIONS = frozenset({
    "PRIOR_HISTORY",
    "SHARED_OBJECTIVE",
    "PERFORMED_ACTION",
    "OTHER_ACTION",
    "RELATION_VIEW",
    "NO_CHANGE",
    "DENY",
})
PSYCHOLOGY_KEYS = frozenset({
    "beliefs", "affect", "emotions", "traits", "personality", "motives",
    "desires", "intentions", "knowledge", "memories", "competence_estimate",
    "propensity", "attachment", "wound",
})
FUTURE_CHILD_KEYS = frozenset({
    "future_child", "future_child_personality", "future_child_outcome",
    "future_child_desired_adversity_tag", "future_child_health_outcome",
    "future_child_education_outcome", "any_field_derived_from_future_child",
})


class SourceRefusal(ValueError):
    """A source is not a declared sourcefree fixture actor source."""


@dataclass(frozen=True)
class ActorSource:
    actor_id: str
    source_ref: str
    role: str
    seed: str
    birth_clock: int
    initial_cash: int
    initial_free_hours: int
    material_units: int
    event_permissions: tuple[str, ...]
    known_unknowns: tuple[str, ...]
    other_actor_id: str
    schema: str = BP1_ACTOR_SOURCE_SCHEMA
    source_grade: str = BP1_ACTOR_SOURCE_GRADE
    native_grant: str = BP1_NATIVE_GRANT

    def body(self) -> dict:
        return {
            "schema": self.schema,
            "actor_id": self.actor_id,
            "source_ref": self.source_ref,
            "role": self.role,
            "seed": self.seed,
            "birth_clock": self.birth_clock,
            "initial_cash": self.initial_cash,
            "initial_free_hours": self.initial_free_hours,
            "material_units": self.material_units,
            "event_permissions": list(self.event_permissions),
            "known_unknowns": list(self.known_unknowns),
            "other_actor_id": self.other_actor_id,
            "source_grade": self.source_grade,
            "native_grant": self.native_grant,
        }

    def sealed(self) -> dict:
        return seal(self.body())

    @property
    def source_hash(self) -> str:
        return digest(self.body())


def _has_forbidden_key(value: Any, keys: frozenset[str]) -> str | None:
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str) and key.lower() in keys:
                return key
            found = _has_forbidden_key(item, keys)
            if found:
                return found
    elif isinstance(value, (list, tuple)):
        for item in value:
            found = _has_forbidden_key(item, keys)
            if found:
                return found
    return None


def issue_actor_source(
    *,
    actor_id: str,
    role: str,
    seed: str,
    birth_clock: int = 0,
    initial_cash: int = 30,
    initial_free_hours: int = 30,
    material_units: int = 5,
    event_permissions: tuple[str, ...] = tuple(sorted(ALLOWED_EVENT_PERMISSIONS)),
    known_unknowns: tuple[str, ...] = (
        "PSYCHOLOGICAL_LAW_UNISSUED",
        "NATIVE_ACTOR_SOURCE_NOT_GRANTED",
    ),
    other_actor_id: str = "",
) -> ActorSource:
    """Issue one explicit sourcefree fixture actor source.

    The name ``issue`` is fixture construction, not native actor generation.
    """
    if not isinstance(actor_id, str) or not actor_id.startswith(TEST_ONLY_PREFIX):
        raise SourceRefusal("ACTOR_ID_NOT_TEST_ONLY_BP1")
    if role not in ALLOWED_ROLES:
        raise SourceRefusal("ACTOR_ROLE_NOT_DECLARED")
    if not isinstance(seed, str) or not seed:
        raise SourceRefusal("ACTOR_SEED_MISSING")
    if type(birth_clock) is not int or birth_clock < 0:
        raise SourceRefusal("ACTOR_BIRTH_CLOCK_INVALID")
    for name, value in (("initial_cash", initial_cash),
                        ("initial_free_hours", initial_free_hours),
                        ("material_units", material_units)):
        if type(value) is not int or value < 0:
            raise SourceRefusal("ACTOR_SOURCE_BUDGET_INVALID:" + name)
    permissions = tuple(event_permissions)
    if not permissions or any(p not in ALLOWED_EVENT_PERMISSIONS for p in permissions):
        raise SourceRefusal("ACTOR_EVENT_PERMISSION_UNKNOWN")
    if len(set(permissions)) != len(permissions):
        raise SourceRefusal("ACTOR_EVENT_PERMISSION_DUPLICATE")
    if other_actor_id and not other_actor_id.startswith(TEST_ONLY_PREFIX):
        raise SourceRefusal("OTHER_ACTOR_NOT_TEST_ONLY_BP1")
    source = ActorSource(
        actor_id=actor_id,
        source_ref=TEST_ONLY_PREFIX + "SOURCE_" + actor_id[len(TEST_ONLY_PREFIX):],
        role=role,
        seed=seed,
        birth_clock=birth_clock,
        initial_cash=initial_cash,
        initial_free_hours=initial_free_hours,
        material_units=material_units,
        event_permissions=permissions,
        known_unknowns=tuple(known_unknowns),
        other_actor_id=other_actor_id,
    )
    verify_actor_source(source)
    return source


def _source_problem(source: ActorSource) -> str | None:
    if not isinstance(source, ActorSource):
        return "ACTOR_SOURCE_NOT_OBJECT"
    body = source.body()
    if body["schema"] != BP1_ACTOR_SOURCE_SCHEMA:
        return "ACTOR_SOURCE_SCHEMA_UNKNOWN"
    if body["source_grade"] != BP1_ACTOR_SOURCE_GRADE:
        return "ACTOR_SOURCE_GRADE_NOT_DECLARED"
    if body["native_grant"] != BP1_NATIVE_GRANT:
        return "ACTOR_SOURCE_CANNOT_CARRY_NATIVE_GRANT"
    if not body["actor_id"].startswith(TEST_ONLY_PREFIX):
        return "ACTOR_ID_NOT_TEST_ONLY_BP1"
    if not body["source_ref"].startswith(TEST_ONLY_PREFIX):
        return "ACTOR_SOURCE_REF_NOT_TEST_ONLY_BP1"
    if body["role"] not in ALLOWED_ROLES:
        return "ACTOR_ROLE_NOT_DECLARED"
    if not body["seed"]:
        return "ACTOR_SEED_MISSING"
    for key in ("birth_clock", "initial_cash", "initial_free_hours",
                "material_units"):
        if type(body[key]) is not int or body[key] < 0:
            return "ACTOR_SOURCE_BUDGET_INVALID:" + key
    if not body["event_permissions"]:
        return "ACTOR_EVENT_PERMISSION_EMPTY"
    if any(p not in ALLOWED_EVENT_PERMISSIONS for p in body["event_permissions"]):
        return "ACTOR_EVENT_PERMISSION_UNKNOWN"
    forbidden = _has_forbidden_key(body, PSYCHOLOGY_KEYS | FUTURE_CHILD_KEYS)
    if forbidden:
        return "ACTOR_SOURCE_FORBIDDEN_FIELD:" + forbidden
    return None


def verify_actor_source(source: ActorSource) -> tuple[bool, str | None]:
    """Return ``(accepted, reason)`` for a sourcefree fixture actor source."""
    problem = _source_problem(source)
    if problem is not None:
        return False, problem
    return True, None


def require_actor_source(source: ActorSource) -> ActorSource:
    accepted, reason = verify_actor_source(source)
    if not accepted:
        raise SourceRefusal(reason)
    return source


def reseal_with_changed_source_ref(source: ActorSource, source_ref: str) -> ActorSource:
    """Test helper: produce a rehashed source with a changed source reference."""
    return replace(source, source_ref=source_ref)
