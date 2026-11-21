#!/usr/bin/env python3
"""Reusable SRC16 recorded-only operator preparation and preflight.

This module does not issue authority and does not open a saved estate.  It
materializes an operation document from a separately supplied owner decision
and validates the exact SRC16 owner/use/successor/raw-domain shape that a
private driver must satisfy before the cold stream index is opened.

The actual owner decision, current-use successor, historical closure and
operation are private inputs.  Only sourcefree fixtures are used by the tests.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import argparse
import json
import os
from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from typing import Any, Mapping

from rawlsing_next.pre553_anvil_stream_recorded import (
    SUPPORTED_HISTORICAL_SCOPE_GRADES,
)
from rawlsing_next.pre553_carrier_execution import materialize_public_object
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    ExactRef,
    exact_ref,
    semantic_hash,
)


SOURCE_ID = "SRC16"
QUESTION_ID = "GSS:1972:racpres"
HISTORICAL_GRADE = "EXACT_COORDINATE_CANDIDATES_ONLY_NOT_ADOPTION"
OPERATION = "SRC16-RACPRES-RECORDED-RESPONSE-ONLY"
SUPPORTED_INTERPRETATION_STATES = frozenset({
    "SUBSTANTIVE_RESPONSE",
    "DK",
    "REFUSAL",
    "MISSING",
    "INAPPLICABLE",
    "NOT_ASKED",
    "SOURCE_SPECIFIC_SPECIAL",
    "INVALID_UNRESOLVED",
})
SCOPE_KIND = "OBSERVED_STORED_CODE_FREQUENCIES"
ASKED_ELIGIBILITY = "HELD_NOT_PROVEN"


class Src16OperatorError(ValueError):
    """The exact SRC16 operator contract is absent, stale or incomplete."""

    def __init__(self, code: str, detail: str | None = None) -> None:
        self.code = code
        self.detail = detail
        super().__init__(code if detail is None else code + ": " + detail)


class Src16Dependency(Src16OperatorError):
    """An exact external classification/authority dependency remains."""


def _ref(value: Any, label: str) -> ExactRef:
    if isinstance(value, str):
        parts = value.split("|")
        if len(parts) == 3 and all(parts):
            value = {"kind": parts[0], "object_id": parts[1], "content_hash": parts[2]}
    try:
        return exact_ref(value, label)
    except Exception as exc:
        raise Src16OperatorError("SRC16_EXACT_REF_INVALID", label) from exc


def _authority_ref(value: Any, label: str) -> AuthorityRef:
    if isinstance(value, AuthorityRef):
        return value
    try:
        return AuthorityRef(
            value["authority_id"], value["authority_version"],
            value["authority_content_hash"],
        )
    except Exception as exc:
        raise Src16OperatorError("SRC16_AUTHORITY_REF_INVALID", label) from exc


def _owner_codes(owner: Mapping[str, Any]) -> tuple[str, ...]:
    denominator = owner.get("denominator")
    values = (
        denominator.get("recorded_raw_codes")
        if isinstance(denominator, Mapping)
        else owner.get("recorded_raw_codes")
    )
    if not isinstance(values, (list, tuple)) or not values:
        raise Src16OperatorError("SRC16_RAW_DOMAIN_MISSING")
    codes = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (str, int)):
            raise Src16OperatorError("SRC16_RAW_DOMAIN_NOT_EXACT_LABELS")
        codes.append(str(value))
    if len(set(codes)) != len(codes):
        raise Src16OperatorError("SRC16_RAW_DOMAIN_DUPLICATE_CODE")
    return tuple(codes)


def _owner_interpretation(
    owner: Mapping[str, Any], codes: tuple[str, ...],
) -> tuple[tuple[str, str], ...]:
    raw = owner.get("interpretation")
    if not isinstance(raw, Mapping):
        raise Src16OperatorError("SRC16_INTERPRETATION_MISSING")
    result = []
    for code in codes:
        value = raw.get(code)
        if value is None:
            value = raw.get(int(code)) if code.lstrip("-").isdigit() else None
        if isinstance(value, (list, tuple)):
            if len(value) != 1:
                raise Src16OperatorError(
                    "SRC16_INTERPRETATION_NOT_SINGLE_STATE", code
                )
            value = value[0]
        if not isinstance(value, str) or not value:
            raise Src16OperatorError("SRC16_INTERPRETATION_NOT_EXACT", code)
        state = value.strip()
        if state not in SUPPORTED_INTERPRETATION_STATES:
            raise Src16Dependency(
                "SRC16_CODE_STATE_CLASSIFICATION_REQUIRED",
                f"code={code} state={state} is not an exact recorded state",
            )
        result.append((code, state))
    if set(str(x) for x in raw) != set(codes):
        raise Src16OperatorError("SRC16_INTERPRETATION_DOMAIN_MISMATCH")
    non_substantive = {}
    for code, state in result:
        if state == "SUBSTANTIVE_RESPONSE":
            continue
        if state in non_substantive:
            raise Src16OperatorError(
                "SRC16_STORED_CODE_BIN_COLLISION",
                f"state={state} has both {non_substantive[state]} and {code}",
            )
        non_substantive[state] = code
    return tuple(result)


def _owner_scope(owner: Mapping[str, Any]) -> Mapping[str, Any]:
    raw = owner.get("scope")
    if isinstance(raw, Mapping):
        scope = dict(raw)
        required = {
            "host", "scope", "question_id", "questionnaire_sha256",
            "denominator",
        }
        if set(scope) != required:
            raise Src16OperatorError("SRC16_STRUCTURED_SCOPE_SHAPE_MISMATCH")
        return scope
    if not isinstance(raw, str) or not raw:
        raise Src16OperatorError("SRC16_OWNER_SCOPE_MISSING")
    required = ("host", "question_id", "questionnaire_sha256", "denominator")
    if any(name not in owner for name in required):
        raise Src16OperatorError("SRC16_OWNER_SCOPE_FIELDS_MISSING")
    return {
        "host": owner["host"],
        "scope": raw,
        "question_id": owner["question_id"],
        "questionnaire_sha256": owner["questionnaire_sha256"],
        "denominator": owner["denominator"],
    }


def _validate_structured_scope(scope: Mapping[str, Any], codes: tuple[str, ...]) -> None:
    if scope.get("question_id") != QUESTION_ID:
        raise Src16OperatorError("SRC16_SCOPE_QUESTION_MISMATCH")
    if not isinstance(scope.get("scope"), str) or not scope["scope"]:
        raise Src16OperatorError("SRC16_SCOPE_GRADE_MISSING")
    if not isinstance(scope.get("host"), str) or not scope["host"]:
        raise Src16OperatorError("SRC16_SCOPE_HOST_MISSING")
    denominator = scope.get("denominator")
    if not isinstance(denominator, Mapping):
        raise Src16OperatorError("SRC16_SCOPE_DENOMINATOR_MISSING")
    raw = denominator.get("recorded_raw_codes")
    if not isinstance(raw, (list, tuple)) or tuple(str(x) for x in raw) != codes:
        raise Src16OperatorError("SRC16_SCOPE_RAW_DOMAIN_MISMATCH")


def _owner_question(owner: Mapping[str, Any], question_ref: Any | None) -> ExactRef:
    value = question_ref or owner.get("native_question_ref") or owner.get("question_ref")
    question = _ref(value, "SRC16 native question")
    return question


def _state_bearing(interpretation: tuple[tuple[str, str], ...]) -> bool:
    return any(state != "SUBSTANTIVE_RESPONSE" for _, state in interpretation)


def _approved_states(
    owner: Mapping[str, Any], interpretation: tuple[tuple[str, str], ...],
) -> tuple[str, ...]:
    raw = owner.get("approved_nonanswer_states", ())
    if not isinstance(raw, (list, tuple)):
        raise Src16OperatorError("SRC16_APPROVED_STATE_DOMAIN_INVALID")
    approved = tuple(str(x) for x in raw)
    if len(set(approved)) != len(approved):
        raise Src16OperatorError("SRC16_APPROVED_STATE_DOMAIN_DUPLICATE")
    required = {
        state for _, state in interpretation
        if state != "SUBSTANTIVE_RESPONSE"
    }
    if not required.issubset(set(approved)):
        raise Src16OperatorError(
            "SRC16_APPROVED_STATE_DOMAIN_MISMATCH",
            f"missing={sorted(required - set(approved))}",
        )
    return approved


def _owner_historical(
    owner: Mapping[str, Any], historical_scope_grade: str | None,
) -> tuple[str, ExactRef]:
    grade = historical_scope_grade or owner.get("historical_scope_grade")
    if grade != HISTORICAL_GRADE:
        raise Src16OperatorError(
            "SRC16_HISTORICAL_GRADE_MISMATCH",
            f"expected {HISTORICAL_GRADE!r}",
        )
    if grade not in SUPPORTED_HISTORICAL_SCOPE_GRADES:
        raise Src16OperatorError("SRC16_HISTORICAL_GRADE_UNSUPPORTED")
    historical_ref = _ref(
        owner.get("historical_snapshot_ref"),
        "SRC16 historical snapshot",
    )
    return grade, historical_ref


def _authority(
    *, owner_sha: str, role: str, operation: str,
    scope: Mapping[str, Any], roots: Mapping[str, str],
    codes: tuple[str, ...], kind: str, families: tuple[str, ...],
    state_bearing: bool,
    historical_scope_grade: str, historical_ref: ExactRef,
) -> AuthoritySnapshot:
    material = {
        "owner_decision_sha256": owner_sha,
        "role": role,
        "operation": operation,
        "scope": scope,
        "roots": roots,
        "codes": list(codes),
        "historical_scope_grade": historical_scope_grade,
        "historical_snapshot_ref": historical_ref.as_dict(),
    }
    digest = semantic_hash(material)
    universe = _ref(roots["universe"], "SRC16 universe")
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(ExactRef(
            "OWNER_DECISION", "q006-src16-" + owner_sha, owner_sha,
        ),),
        producer_replay_locator_or_reference_root=ExactRef(
            "REPLAY_ROOT", "q006-src16-" + role + "-" + owner_sha, digest,
        ),
        authority_id="Q006-SRC16-" + role,
        authority_version="1.0.0",
        authority_content_hash=digest,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=(operation,),
        governed_object_families=tuple(families),
        scope_envelope={
            "source_universe_refs": [universe.as_dict()],
            "source_sha256": roots["source"],
            "release": roots["release"],
            "replay_root": roots["replay"],
            "scope": dict(scope),
            "recorded_raw_codes": list(codes),
            "scope_kind": SCOPE_KIND,
            "asked_eligibility": ASKED_ELIGIBILITY,
            "substantive_vote_denominator": False,
            "state_bearing_raw_codes": state_bearing,
            "historical_scope_grade": historical_scope_grade,
            "historical_snapshot_ref": historical_ref.as_dict(),
        },
        effective_time_or_interval="OWNER_DECISION_CURRENT",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash(material),
        replay_protocol_ref=ExactRef(
            "REPLAY_PROTOCOL", "q006-src16-" + role, digest,
        ),
    )


def _r2_binding(r2: Mapping[str, Any]) -> Mapping[str, Any]:
    waves = r2.get("waves")
    if not isinstance(waves, Mapping) or not isinstance(waves.get(SOURCE_ID), Mapping):
        raise Src16OperatorError("SRC16_R2_WAVE_MISSING")
    return waves[SOURCE_ID]


def materialize(
    *, owner_path: Path, r2_path: Path, output: Path,
    question_ref: Any | None = None,
) -> tuple[Path, str]:
    """Build a private SRC16 operation document from an exact owner decision."""
    owner_bytes = owner_path.read_bytes()
    owner_sha = sha256(owner_bytes).hexdigest()
    owner = json.loads(owner_bytes)
    if not isinstance(owner, Mapping) or owner.get("source_id") != SOURCE_ID:
        raise Src16OperatorError("SRC16_OWNER_SOURCE_MISMATCH")
    if owner.get("question_id") != QUESTION_ID:
        raise Src16OperatorError("SRC16_OWNER_QUESTION_MISMATCH")
    r2 = json.loads(r2_path.read_bytes())
    source = _r2_binding(r2)
    binding = owner.get("source_binding")
    expected_keys = (
        "custody_estate_path", "decision_ref", "manifest_sha256",
        "saved_i02", "source_sha256",
    )
    if not isinstance(binding, Mapping) or any(
        binding.get(key) != source.get(key) for key in expected_keys
    ):
        raise Src16OperatorError("SRC16_R2_SOURCE_BINDING_MISMATCH")
    roots = binding.get("saved_i02")
    if not isinstance(roots, Mapping):
        raise Src16OperatorError("SRC16_SAVED_ROOTS_MISSING")
    for name in ("source", "release", "universe", "replay"):
        if not isinstance(roots.get(name), str) or not roots[name]:
            raise Src16OperatorError("SRC16_SAVED_ROOT_MISSING", name)
    codes = _owner_codes(owner)
    interpretation = _owner_interpretation(owner, codes)
    scope = _owner_scope(owner)
    _validate_structured_scope(scope, codes)
    question = _owner_question(owner, question_ref)
    operation = owner.get("authorized_operation") or OPERATION
    if operation != OPERATION:
        raise Src16OperatorError("SRC16_OPERATION_MISMATCH", str(operation))
    grade, historical_ref = _owner_historical(owner, None)
    source_auth = _authority(
        owner_sha=owner_sha, role="SOURCE", operation=operation, scope=scope,
        roots=roots, codes=codes, kind="SOURCE_SEMANTICS_TOPOLOGY",
        families=(
            "EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0",
            "RoutingEligibilityFact@1.0.0",
        ),
        state_bearing=_state_bearing(interpretation),
        historical_scope_grade=grade, historical_ref=historical_ref,
    )
    routing_auth = _authority(
        owner_sha=owner_sha, role="ROUTING", operation=operation, scope=scope,
        roots=roots, codes=codes, kind="ROUTING_RISK_SET",
        families=("RoutingEligibilityFact@1.0.0",),
        state_bearing=_state_bearing(interpretation),
        historical_scope_grade=grade, historical_ref=historical_ref,
    )
    query_auth = _authority(
        owner_sha=owner_sha, role="QUERY", operation=operation, scope=scope,
        roots=roots, codes=codes, kind="PREDICATE_GRAMMAR",
        families=(
            "EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0",
            "EmpiricalFact@1.0.0",
        ),
        state_bearing=_state_bearing(interpretation),
        historical_scope_grade=grade, historical_ref=historical_ref,
    )
    suffix = semantic_hash({"owner": owner_sha, "codes": codes, "question": question.as_dict()})
    approved_nonanswer = _approved_states(owner, interpretation)
    doc = {
        "schema": "ANVIL_Q006_SRC16_RACPRES_OPERATION@1",
        "owner_decision_sha256": owner_sha,
        "source_id": SOURCE_ID,
        "source_root": roots["source"],
        "release_root": roots["release"],
        "universe_root": roots["universe"],
        "replay_root": roots["replay"],
        "question_ref": question.as_dict(),
        "authorized_operation": operation,
        "allowed_raw_codes": list(codes),
        "interpretation": [list(x) for x in interpretation],
        "state_bearing_raw_codes": _state_bearing(interpretation),
        "scope_kind": SCOPE_KIND,
        "asked_eligibility": ASKED_ELIGIBILITY,
        "substantive_vote_denominator": False,
        "historical_scope_grade": grade,
        "historical_snapshot_ref": historical_ref.as_dict(),
        "approved_nonanswer_states": list(approved_nonanswer),
        "authorities": [x.as_dict() for x in (
            source_auth, routing_auth, query_auth,
        )],
        "query_authority_ref": query_auth.authority_ref.as_dict(),
        "routing_authority_ref": routing_auth.authority_ref.as_dict(),
        "source_authority_ref": source_auth.authority_ref.as_dict(),
        "recorded_risk_ref": {
            "kind": "RISK_SET",
            "object_id": "urn:rawlsing:q006:src16:racpres:recorded:" + suffix,
            "content_hash": suffix,
        },
        "routing_rule_ref": {
            "kind": "ROUTING_RULE",
            "object_id": "urn:rawlsing:q006:src16:racpres:recorded-only:" + suffix,
            "content_hash": suffix,
        },
        "member_set_replay_ref": {
            "kind": "MEMBER_SET",
            "object_id": "urn:rawlsing:q006:src16:racpres:members:" + suffix,
            "content_hash": suffix,
        },
        "measure_basis_ref": {
            "kind": "MEASURE_BASIS",
            "object_id": "urn:rawlsing:q006:src16:racpres:RAW:" + suffix,
            "content_hash": semantic_hash({"measure": "RAW", "owner": owner_sha}),
        },
        "response_state_semantics_ref": {
            "kind": "RESPONSE_STATE_SEMANTICS",
            "object_id": "urn:rawlsing:q006:src16:racpres:recorded-only:" + suffix,
            "content_hash": semantic_hash({
                "interpretation": interpretation, "owner": owner_sha,
            }),
        },
        "target_domain_replay_ref": {
            "kind": "TARGET_DOMAIN",
            "object_id": "urn:rawlsing:q006:src16:racpres:domain:" + suffix,
            "content_hash": semantic_hash({
                "question": question.as_dict(), "codes": list(codes),
            }),
        },
        "predicate_replay_root": {
            "kind": "REPLAY_ROOT",
            "object_id": "urn:rawlsing:q006:src16:racpres:predicate:" + suffix,
            "content_hash": semantic_hash({"kind": "predicate", "owner": owner_sha}),
        },
        "query_replay_root": {
            "kind": "REPLAY_ROOT",
            "object_id": "urn:rawlsing:q006:src16:racpres:query:" + suffix,
            "content_hash": semantic_hash({"kind": "query", "owner": owner_sha}),
        },
        "transform_ref": {
            "kind": "RECORDED_VALUE_TRANSFORM",
            "object_id": "urn:rawlsing:q006:src16:racpres:transform:" + suffix,
            "content_hash": semantic_hash({
                "transform": "R5_RAW_TO_RECORDED_OWNER_INTERPRETATION",
                "owner": owner_sha,
            }),
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(doc, stream, indent=2, sort_keys=True)
        stream.write("\n")
    os.chmod(output, 0o600)
    return output, sha256(output.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Src16Preflight:
    owner_sha256: str
    expected_scope: Mapping[str, Any]
    codes: tuple[str, ...]
    interpretation: tuple[tuple[str, str], ...]
    historical_ref: ExactRef
    historical_scope_grade: str
    state_bearing_raw_codes: bool
    positive: AuthoritySnapshot
    authorities: tuple[AuthoritySnapshot, ...]


def validate_preflight(
    *, owner_bytes: bytes, r2: Mapping[str, Any], operation_bytes: bytes,
    use_bytes: bytes, closure_bytes: bytes,
) -> Src16Preflight:
    """Validate exact current owner/use/raw-domain shape before any estate open."""
    owner_sha = sha256(owner_bytes).hexdigest()
    owner = json.loads(owner_bytes)
    if not isinstance(owner, Mapping) or owner.get("source_id") != SOURCE_ID:
        raise Src16OperatorError("SRC16_OWNER_SOURCE_MISMATCH")
    if owner.get("question_id") != QUESTION_ID:
        raise Src16OperatorError("SRC16_OWNER_QUESTION_MISMATCH")
    source = _r2_binding(r2)
    binding = owner.get("source_binding")
    expected_keys = (
        "custody_estate_path", "decision_ref", "manifest_sha256",
        "saved_i02", "source_sha256",
    )
    if not isinstance(binding, Mapping) or any(
        binding.get(key) != source.get(key) for key in expected_keys
    ):
        raise Src16OperatorError("SRC16_R2_SOURCE_BINDING_MISMATCH")
    operation = json.loads(operation_bytes)
    if not isinstance(operation, Mapping):
        raise Src16OperatorError("SRC16_OPERATION_NOT_MAPPING")
    if operation.get("source_id") != SOURCE_ID:
        raise Src16OperatorError("SRC16_OPERATION_SOURCE_MISMATCH")
    if operation.get("owner_decision_sha256") != owner_sha:
        raise Src16OperatorError("SRC16_OPERATION_OWNER_STALE")
    codes = _owner_codes(owner)
    interpretation = _owner_interpretation(owner, codes)
    if tuple(str(x) for x in operation.get("allowed_raw_codes", ())) != codes:
        raise Src16OperatorError("SRC16_OPERATION_RAW_DOMAIN_MISMATCH")
    if tuple(tuple(str(x) for x in pair) for pair in operation.get("interpretation", ())) != interpretation:
        raise Src16OperatorError("SRC16_OPERATION_INTERPRETATION_MISMATCH")
    if operation.get("state_bearing_raw_codes") is not _state_bearing(interpretation):
        raise Src16OperatorError("SRC16_OPERATION_STATE_BEARING_MISMATCH")
    if operation.get("scope_kind") != SCOPE_KIND:
        raise Src16OperatorError("SRC16_OPERATION_SCOPE_KIND_MISMATCH")
    if operation.get("asked_eligibility") != ASKED_ELIGIBILITY:
        raise Src16OperatorError("SRC16_OPERATION_ASKED_ELIGIBILITY_MISMATCH")
    if operation.get("substantive_vote_denominator") is not False:
        raise Src16OperatorError("SRC16_OPERATION_SUBSTANTIVE_DENOMINATOR_CLAIM")
    approved_states = _approved_states(owner, interpretation)
    if tuple(
        str(x) for x in operation.get("approved_nonanswer_states", ())
    ) != approved_states:
        raise Src16OperatorError("SRC16_OPERATION_APPROVED_STATE_DOMAIN_MISMATCH")
    expected_scope = _owner_scope(owner)
    _validate_structured_scope(expected_scope, codes)
    question = _owner_question(owner, None)
    if _ref(operation.get("question_ref"), "operation question") != question:
        raise Src16OperatorError("SRC16_OPERATION_QUESTION_MISMATCH")
    operation_name = operation.get("authorized_operation")
    if operation_name != OPERATION:
        raise Src16OperatorError("SRC16_OPERATION_NAME_MISMATCH")
    historical_ref = _ref(
        operation.get("historical_snapshot_ref"),
        "operation historical snapshot",
    )
    grade = operation.get("historical_scope_grade")
    if grade != HISTORICAL_GRADE:
        raise Src16OperatorError("SRC16_OPERATION_HISTORICAL_GRADE_MISMATCH")
    if grade not in SUPPORTED_HISTORICAL_SCOPE_GRADES:
        raise Src16OperatorError("SRC16_HISTORICAL_GRADE_UNSUPPORTED")
    try:
        authorities = tuple(
            materialize_public_object(item)
            for item in operation.get("authorities", ())
        )
    except Exception as exc:
        raise Src16OperatorError("SRC16_OPERATION_AUTHORITY_INVALID") from exc
    if not authorities or any(type(x) is not AuthoritySnapshot for x in authorities):
        raise Src16OperatorError("SRC16_OPERATION_AUTHORITY_FAMILY_MISMATCH")
    positive = next(
        (x for x in authorities
         if x.authority_ref == _authority_ref(
             operation.get("source_authority_ref"), "source authority"
         )), None,
    )
    if positive is None:
        raise Src16OperatorError("SRC16_POSITIVE_SOURCE_AUTHORITY_MISSING")
    if positive.decision_state != "ALLOW":
        raise Src16OperatorError("SRC16_POSITIVE_SOURCE_AUTHORITY_NOT_CURRENT")
    if operation_name not in positive.governed_operations:
        raise Src16OperatorError("SRC16_POSITIVE_OPERATION_MISMATCH")
    if positive.authority_kind != "SOURCE_SEMANTICS_TOPOLOGY":
        raise Src16OperatorError("SRC16_POSITIVE_SOURCE_FAMILY_MISMATCH")
    positive_scope = positive.scope_envelope
    if not isinstance(positive_scope, Mapping):
        raise Src16OperatorError("SRC16_POSITIVE_SCOPE_MISSING")
    if positive_scope.get("scope") != expected_scope:
        raise Src16OperatorError("SRC16_POSITIVE_SCOPE_SHAPE_MISMATCH")
    if tuple(str(x) for x in positive_scope.get("recorded_raw_codes", ())) != codes:
        raise Src16OperatorError("SRC16_POSITIVE_RAW_DOMAIN_MISMATCH")
    if positive_scope.get("historical_scope_grade") != grade:
        raise Src16OperatorError("SRC16_POSITIVE_HISTORICAL_GRADE_MISMATCH")
    if positive_scope.get("scope_kind") != SCOPE_KIND:
        raise Src16OperatorError("SRC16_POSITIVE_SCOPE_KIND_MISMATCH")
    if positive_scope.get("asked_eligibility") != ASKED_ELIGIBILITY:
        raise Src16OperatorError("SRC16_POSITIVE_ASKED_ELIGIBILITY_MISMATCH")
    if positive_scope.get("substantive_vote_denominator") is not False:
        raise Src16OperatorError("SRC16_POSITIVE_SUBSTANTIVE_DENOMINATOR_CLAIM")
    if _ref(
        positive_scope.get("historical_snapshot_ref"),
        "positive historical snapshot",
    ) != historical_ref:
        raise Src16OperatorError("SRC16_POSITIVE_HISTORICAL_REF_MISMATCH")
    for key, expected in (
        ("source_sha256", operation.get("source_root")),
        ("release", operation.get("release_root")),
        ("replay_root", operation.get("replay_root")),
    ):
        if positive_scope.get(key) != expected:
            raise Src16OperatorError("SRC16_POSITIVE_ROOT_MISMATCH", key)
    try:
        use = json.loads(use_bytes)
    except Exception as exc:
        raise Src16OperatorError("SRC16_USE_DECISION_INVALID") from exc
    if not isinstance(use, Mapping):
        raise Src16OperatorError("SRC16_USE_DECISION_NOT_MAPPING")
    if use.get("owner_decision_sha256") != owner_sha:
        raise Src16OperatorError("SRC16_USE_OWNER_STALE")
    if use.get("operation_document_sha256") != sha256(operation_bytes).hexdigest():
        raise Src16OperatorError("SRC16_USE_OPERATION_STALE")
    if use.get("historical_scope_grade") != grade:
        raise Src16OperatorError("SRC16_USE_HISTORICAL_GRADE_MISMATCH")
    if _ref(use.get("historical_snapshot_ref"), "use historical") != historical_ref:
        raise Src16OperatorError("SRC16_USE_HISTORICAL_REF_MISMATCH")
    if use.get("scope") != expected_scope:
        raise Src16OperatorError("SRC16_USE_SCOPE_SHAPE_MISMATCH")
    if use.get("operation") != operation_name:
        raise Src16OperatorError("SRC16_USE_OPERATION_MISMATCH")
    if tuple(str(x) for x in use.get("recorded_raw_codes", ())) != codes:
        raise Src16OperatorError("SRC16_USE_RAW_DOMAIN_MISMATCH")
    try:
        closure = json.loads(closure_bytes)
    except Exception as exc:
        raise Src16OperatorError("SRC16_HISTORICAL_CLOSURE_INVALID") from exc
    if not isinstance(closure, list) or len(closure) != 1:
        raise Src16OperatorError("SRC16_HISTORICAL_CLOSURE_NOT_EXACT")
    item = closure[0]
    if not isinstance(item, Mapping) or item.get("state") != "DEFER":
        raise Src16OperatorError("SRC16_HISTORICAL_CLOSURE_NOT_DEFER")
    if _ref(item.get("ref"), "closure historical") != historical_ref:
        raise Src16OperatorError("SRC16_HISTORICAL_CLOSURE_REF_MISMATCH")
    if "semantic_scope" in item and item["semantic_scope"] != grade:
        raise Src16OperatorError("SRC16_HISTORICAL_CLOSURE_GRADE_MISMATCH")
    return Src16Preflight(
        owner_sha256=owner_sha,
        expected_scope=expected_scope,
        codes=codes,
        interpretation=interpretation,
        historical_ref=historical_ref,
        historical_scope_grade=grade,
        state_bearing_raw_codes=_state_bearing(interpretation),
        positive=positive,
        authorities=authorities,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner-decision", type=Path, required=True)
    ap.add_argument("--r2-decision", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--question-ref", default=None)
    args = ap.parse_args()
    try:
        output, digest = materialize(
            owner_path=args.owner_decision, r2_path=args.r2_decision,
            output=args.output, question_ref=args.question_ref,
        )
    except Src16Dependency as exc:
        print(json.dumps({
            "schema": "ANVIL_Q006_SRC16_MATERIALIZE_EXACT_HOLD@1",
            "status": "EXACT_HOLD", "dependency": exc.code,
            "detail": exc.detail,
        }, sort_keys=True))
        return 2
    except Src16OperatorError as exc:
        print(json.dumps({
            "schema": "ANVIL_Q006_SRC16_MATERIALIZE_REFUSAL@1",
            "status": "REFUSED", "code": exc.code, "detail": exc.detail,
        }, sort_keys=True))
        return 1
    print(json.dumps({
        "schema": "ANVIL_Q006_SRC16_OPERATION_MATERIALIZED@1",
        "output": str(output), "sha256": digest,
        "mode": oct(output.stat().st_mode & 0o777),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "HISTORICAL_GRADE",
    "OPERATION",
    "QUESTION_ID",
    "SOURCE_ID",
    "Src16Dependency",
    "Src16OperatorError",
    "Src16Preflight",
    "materialize",
    "validate_preflight",
]
