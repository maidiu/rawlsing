"""Explicit TEST_ONLY source/model for S46 workshop interval participation."""
from __future__ import annotations

from copy import deepcopy

from .bootstrap import install

install()

from candidate import digest, seal  # noqa: E402

from .errors import S46Refusal  # noqa: E402

MODEL_SCHEMA = "S46_TEST_ONLY_INTERVAL_MODEL@1"
DOMAIN_SCHEMA = "S46_INTERVAL_DOMAIN@1"
GRADE = "TEST_ONLY_S46_SYNTHETIC_OBJECTIVE_INTERVAL_MODEL_NOT_NATIVE"
ACTOR_OWNER = "TEST_ONLY_S46_ACTOR_ATTEMPT_OWNER"
WORLD_OWNER = "TEST_ONLY_S46_WORLD_PERFORMER_OWNER"
ACTOR_OWNER_VERSION = "1"
WORLD_OWNER_VERSION = "1"
POLICY_ID = "TEST_ONLY_S46_MATERIAL_ATTEMPT_POLICY"
POLICY_VERSION = "1"
POLICY_MODE = "RESOURCE_CONSTRAINED_ATTEMPT"
MODEL_ID = "TEST_ONLY_S46_MATERIAL_PREP_MODEL"
MODEL_VERSION = "1"
ACTIVITY_ID = "TEST_ONLY_S46_MATERIAL_INSPECT"
SCOPE_ID = "TEST_ONLY_S46_WORKSHOP_MATERIAL_PREP"
SOURCE_RULE_REF = "TEST_ONLY_S46_WORKSHOP_INTERVAL_SOURCE@1"
MODES = frozenset({
    "ACTUAL", "SCHEDULED_ONLY", "DECLINED", "CONSTRAINED", "BLOCKED",
    "UNKNOWN",
})


def _model_body() -> dict:
    return {
        "schema": MODEL_SCHEMA,
        "grade": GRADE,
        "native": False,
        "psychology_claim": False,
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "policy": {
            "policy_id": POLICY_ID,
            "version": POLICY_VERSION,
            "mode": POLICY_MODE,
            "interpretation": "RESOURCE_CONSTRAINED_ATTEMPT_NOT_CONSENT_OR_WILLINGNESS",
        },
        "owners": {
            "actor": {"owner_id": ACTOR_OWNER, "version": ACTOR_OWNER_VERSION},
            "world": {"owner_id": WORLD_OWNER, "version": WORLD_OWNER_VERSION},
        },
        "activity": {
            "activity_id": ACTIVITY_ID,
            "scope_id": SCOPE_ID,
            "source_rule_ref": SOURCE_RULE_REF,
            "resolution": "BOUNDED_PERIOD_STATE_NOT_DAILY_EVENTS",
            "material_inspection": True,
            "counterpart_required": False,
        },
        "source_bindings": {
            "s45_base": "f26a138e20d53c809d611cf8d834ec647b0804bf",
            "sdtf_r4": "79659b352035f095b325181d4f35c259da6b79d0",
            "grade": "TEST_ONLY_SOURCEFREE_OPERATOR_MODEL",
        },
    }


MODEL_HASH = digest(_model_body())
OWNER_REGISTRY_HASH = digest({
    "actor": ACTOR_OWNER, "actor_version": ACTOR_OWNER_VERSION,
    "world": WORLD_OWNER, "world_version": WORLD_OWNER_VERSION,
})


def model_document() -> dict:
    body = _model_body()
    body["model_hash"] = MODEL_HASH
    body["owner_registry_hash"] = OWNER_REGISTRY_HASH
    return seal(body)


def make_domain(*, mode: str, start: int, end: int,
                segments: tuple[tuple[int, int], ...] | None = None,
                actor_id: str = "TEST_ONLY_BP1_R26V_ACTOR_A",
                branch_id: str = "first_session") -> dict:
    if mode not in MODES:
        raise S46Refusal("S46_MODE_INVALID", mode)
    if not (isinstance(start, int) and isinstance(end, int) and start < end):
        raise S46Refusal("S46_DOMAIN_TIME_INVALID")
    if segments is None:
        midpoint = start + (end - start) // 2
        segments = ((start, midpoint), (midpoint, end))
    normalized = tuple((int(a), int(b)) for a, b in segments)
    if (
        not normalized
        or normalized[0][0] != start
        or normalized[-1][1] != end
        or any(a >= b for a, b in normalized)
        or any(normalized[i][1] != normalized[i + 1][0]
               for i in range(len(normalized) - 1))
    ):
        raise S46Refusal("S46_SEGMENTS_INVALID")
    body = {
        "schema": DOMAIN_SCHEMA,
        "grade": GRADE,
        "native": False,
        "psychology_claim": False,
        "domain_id": "S46_DOMAIN_" + mode,
        "actor_id": actor_id,
        "branch_id": branch_id,
        "scope_id": SCOPE_ID,
        "activity_id": ACTIVITY_ID,
        "mode": mode,
        "start": int(start),
        "end": int(end),
        "segments": normalized,
        "model_hash": MODEL_HASH,
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "owner_registry_hash": OWNER_REGISTRY_HASH,
        "actor_owner": ACTOR_OWNER,
        "actor_owner_version": ACTOR_OWNER_VERSION,
        "world_owner": WORLD_OWNER,
        "world_owner_version": WORLD_OWNER_VERSION,
        "policy_id": POLICY_ID,
        "policy_version": POLICY_VERSION,
        "source_rule_ref": SOURCE_RULE_REF,
        "resolution": "BOUNDED_PERIOD_STATE",
        "coverage_rule": "ONE_INSTANTANEOUS_ACTION_COVERS_ONE_TIME_UNIT_ACTION_SPAN",
        "action_span_units": 1,
    }
    return seal({**body, "domain_hash": digest(body)})


def validate_domain(domain: dict) -> dict:
    if not isinstance(domain, dict):
        raise S46Refusal("S46_DOMAIN_NOT_OBJECT")
    if domain.get("schema") != DOMAIN_SCHEMA:
        raise S46Refusal("S46_DOMAIN_SCHEMA_MISMATCH")
    if domain.get("model_hash") != MODEL_HASH:
        raise S46Refusal("S46_MODEL_HASH_MISMATCH")
    if domain.get("owner_registry_hash") != OWNER_REGISTRY_HASH:
        raise S46Refusal("S46_OWNER_REGISTRY_MISMATCH")
    if domain.get("actor_owner") != ACTOR_OWNER or domain.get("world_owner") != WORLD_OWNER:
        raise S46Refusal("S46_OWNER_ID_MISMATCH")
    if domain.get("policy_id") != POLICY_ID or domain.get("source_rule_ref") != SOURCE_RULE_REF:
        raise S46Refusal("S46_POLICY_OR_RULE_MISMATCH")
    if domain.get("mode") not in MODES:
        raise S46Refusal("S46_MODE_INVALID")
    if domain.get("domain_id") != "S46_DOMAIN_" + str(domain.get("mode")):
        raise S46Refusal("S46_DOMAIN_ID_MISMATCH")
    if domain.get("source_rule_ref") != SOURCE_RULE_REF:
        raise S46Refusal("S46_DOMAIN_SOURCE_RULE_MISMATCH")
    if domain.get("coverage_rule") != (
        "ONE_INSTANTANEOUS_ACTION_COVERS_ONE_TIME_UNIT_ACTION_SPAN"
    ) or domain.get("action_span_units") != 1:
        raise S46Refusal("S46_COVERAGE_RULE_MISMATCH")
    stored_hash = domain.get("domain_hash", "")
    body = {
        key: value for key, value in domain.items()
        if key not in {"domain_hash", "hash"}
    }
    if not stored_hash or digest(body) != stored_hash:
        raise S46Refusal("S46_DOMAIN_HASH_MISMATCH")
    if not domain.get("actor_id") or not domain.get("branch_id"):
        raise S46Refusal("S46_ACTOR_OR_BRANCH_MISSING")
    if not isinstance(domain.get("segments"), (list, tuple)) or not domain["segments"]:
        raise S46Refusal("S46_SEGMENTS_INVALID")
    return dict(domain)


__all__ = [
    "MODEL_SCHEMA", "DOMAIN_SCHEMA", "GRADE", "MODEL_HASH",
    "OWNER_REGISTRY_HASH", "ACTOR_OWNER", "WORLD_OWNER", "MODES",
    "model_document", "make_domain", "validate_domain",
]
