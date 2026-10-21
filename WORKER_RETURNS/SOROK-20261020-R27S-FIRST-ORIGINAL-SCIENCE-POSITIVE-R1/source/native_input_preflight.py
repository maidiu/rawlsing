"""Fail-closed preflight for one native original A/B practice pathway.

This verifier is a receiving court, not an issuer. It never creates an actor,
encounter, rule, grant, occurrence or performed action. A passing result means
only that the presented input has the exact shape and internal currentness
required for a competent owner to decide whether to receive it.

The native target is deliberately one bounded object:
``c9p:coordinated_material_inspection`` as ``V3MS_PRACTICE``. No trait,
demographic, role or type-derived psychology is accepted.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Protocol

SCHEMA = "R27S_NATIVE_INPUT_BUNDLE@1"
RECEIPT_SCHEMA = "R27S_NATIVE_INPUT_PREFLIGHT_RECEIPT@1"
PREFLIGHT_VERSION = "1.0.0"

TEST_ONLY_GRADE = "TEST_ONLY_SOURCEFREE_TECHNICAL"
NATIVE_GRADE = "NATIVE_ORIGINAL_SOURCE"
UNISSUED_GRADE = "UNISSUED"
PRACTICE_OBJECT = "c9p:coordinated_material_inspection"
TARGET_KIND = "V3MS_PRACTICE"
SELF_KNOWLEDGE = "UNKNOWN_WITHOUT_ADP017"

STATUS_REFUSED = "REFUSED"
STATUS_TECHNICAL_PASS = "TECHNICAL_PREFLIGHT_PASS__NATIVE_FALSE__PRODUCTION_EMPTY"
STATUS_NATIVE_ELIGIBLE = (
    "NATIVE_INPUT_ELIGIBLE_FOR_COMPETENT_RECEIPT__NO_GRANT_ISSUED"
)

FORBIDDEN_PSYCHOGENESIS_FIELDS = frozenset(
    {
        "demographic",
        "demographics",
        "ethnicity",
        "race",
        "gender",
        "sex",
        "class",
        "caste",
        "religion",
        "occupation_psyche",
        "role_psyche",
        "personality",
        "trait",
        "traits",
        "enneagram",
        "attractor",
        "temperament",
        "psychological_type",
        "psychotype",
    }
)


class SignatureVerifier(Protocol):
    """A separately supplied native signature verifier."""

    def verify(self, signature: Mapping[str, Any]) -> bool:
        """Return True only when the signature is authentic."""


def canonical(value: Any) -> str:
    """Return the canonical JSON text used for every digest in this court."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    """Return the SHA-256 hex digest of canonical JSON."""
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def _fail(reasons: list[str], code: str) -> None:
    if code not in reasons:
        reasons.append(code)


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _string(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _integer(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    return value


def _test_only(value: str) -> bool:
    return value.startswith("TEST_ONLY_")


def _current(content: Mapping[str, Any], at: int) -> bool:
    effective_from = _integer(content.get("effective_from"))
    expires_at = content.get("expires_at")
    if effective_from is None or effective_from > at:
        return False
    if content.get("revoked") is True:
        return False
    if expires_at is not None:
        expires = _integer(expires_at)
        if expires is None or at >= expires:
            return False
    return True


def _artifact(
    bundle: Mapping[str, Any],
    ref: Any,
    grade: str,
    reasons: list[str],
) -> Mapping[str, Any] | None:
    artifacts = _mapping(bundle.get("source_artifacts"))
    if artifacts is None:
        _fail(reasons, "SOURCE_ARTIFACTS_MISSING")
        return None
    if not isinstance(ref, str) or not ref:
        _fail(reasons, "SOURCE_REFERENCE_MISSING")
        return None
    wrapper = _mapping(artifacts.get(ref))
    if wrapper is None:
        _fail(reasons, "SOURCE_ARTIFACT_ABSENT:" + ref)
        return None
    if wrapper.get("grade") != grade:
        _fail(reasons, "SOURCE_ARTIFACT_GRADE_MISMATCH:" + ref)
    content = _mapping(wrapper.get("content"))
    if content is None:
        _fail(reasons, "SOURCE_ARTIFACT_CONTENT_MISSING:" + ref)
        return None
    if wrapper.get("content_hash") != digest(content):
        _fail(reasons, "SOURCE_CONTENT_HASH_INVALID:" + ref)
    if "grade" in content and content.get("grade") != grade:
        _fail(reasons, "SOURCE_CONTENT_GRADE_MISMATCH:" + ref)
    if not _string(wrapper.get("owner_ref")):
        _fail(reasons, "SOURCE_ARTIFACT_OWNER_MISSING:" + ref)
    return content


def _forbidden_fields(value: Mapping[str, Any], reasons: list[str], where: str) -> None:
    for field in FORBIDDEN_PSYCHOGENESIS_FIELDS:
        if field in value:
            _fail(reasons, "DEMOGRAPHIC_OR_ROLE_PSYCHOGENESIS_FORBIDDEN:" + where + ":" + field)


def _require_current(
    content: Mapping[str, Any],
    at: int | None,
    reasons: list[str],
    code: str,
) -> None:
    if at is None or not _current(content, at):
        _fail(reasons, code)


def evaluate(
    bundle: Mapping[str, Any],
    *,
    signature_verifier: SignatureVerifier | None = None,
) -> dict[str, Any]:
    """Evaluate one claimed original A/B practice bundle.

    A technical fixture can pass structural and currentness checks, but its
    result always carries ``native=False`` and no production registry entry.
    A native candidate additionally requires a separately supplied verifier;
    even then the result never issues a rule, grant or target.
    """
    reasons: list[str] = []
    checks: dict[str, bool] = {}

    if not isinstance(bundle, Mapping):
        _fail(reasons, "BUNDLE_NOT_MAPPING")
        return _receipt(bundle, reasons, checks, "", "", "", "")

    if bundle.get("schema") != SCHEMA:
        _fail(reasons, "SCHEMA_UNSUPPORTED")
    mode = _string(bundle.get("mode"))
    if mode not in {"TEST_ONLY_TECHNICAL", "NATIVE_CANDIDATE"}:
        _fail(reasons, "MODE_UNSUPPORTED")
    grade = _string(bundle.get("grade"))
    if grade not in {TEST_ONLY_GRADE, NATIVE_GRADE}:
        _fail(reasons, "GRADE_UNSUPPORTED")
    if mode == "TEST_ONLY_TECHNICAL" and grade != TEST_ONLY_GRADE:
        _fail(reasons, "TEST_ONLY_MODE_REQUIRES_TEST_ONLY_GRADE")
    if mode == "NATIVE_CANDIDATE" and grade != NATIVE_GRADE:
        _fail(reasons, "NATIVE_GRADE_REQUIRED")
    checks["schema_and_mode"] = not reasons

    as_of = _integer(bundle.get("as_of"))
    if as_of is None or as_of < 0:
        _fail(reasons, "AS_OF_INVALID")

    production = _mapping(bundle.get("production")) or {}
    if production.get("production_registry_entries") != 0:
        _fail(reasons, "PRODUCTION_REGISTRY_NOT_EMPTY")
    if production.get("grant_written") is not False:
        _fail(reasons, "PRODUCTION_GRANT_WRITE_FORBIDDEN")
    if production.get("native_issued") is not False:
        _fail(reasons, "PREFLIGHT_CANNOT_ISSUE_NATIVE")
    checks["production_empty"] = not any(
        code.startswith("PRODUCTION_") or code.startswith("PREFLIGHT_CANNOT")
        for code in reasons
    )

    source_grant_ref = bundle.get("source_grant_ref")
    source_grant = _artifact(bundle, source_grant_ref, grade, reasons) or {}
    _forbidden_fields(source_grant, reasons, "source_grant")
    if not _string(source_grant.get("source_id")):
        _fail(reasons, "SOURCE_ID_MISSING")
    if not _string(source_grant.get("edition")):
        _fail(reasons, "SOURCE_EDITION_MISSING")
    if not _string(source_grant.get("host_ref")):
        _fail(reasons, "SOURCE_HOST_MISSING")
    if not _string(source_grant.get("purpose_ref")):
        _fail(reasons, "SOURCE_PURPOSE_MISSING")
    if not _string(source_grant.get("permission_ref")):
        _fail(reasons, "SOURCE_PERMISSION_REF_MISSING")
    if not _string(source_grant.get("source_content_hash")):
        _fail(reasons, "SOURCE_CONTENT_IDENTITY_MISSING")
    if as_of is not None:
        _require_current(source_grant, as_of, reasons, "SOURCE_GRANT_STALE")
    checks["source_grant_current"] = "SOURCE_GRANT_STALE" not in reasons

    actor_a = _mapping(bundle.get("actor_a")) or {}
    actor_b = _mapping(bundle.get("actor_b")) or {}
    actor_a_id = _string(actor_a.get("actor_id"))
    actor_b_id = _string(actor_b.get("actor_id"))
    if not actor_a_id or not actor_b_id:
        _fail(reasons, "ACTOR_ID_MISSING")
    if actor_a_id == actor_b_id:
        _fail(reasons, "ACTOR_OTHER_NOT_DISTINCT")
    _forbidden_fields(actor_a, reasons, "actor_a")
    _forbidden_fields(actor_b, reasons, "actor_b")
    if actor_a.get("self_knowledge") != SELF_KNOWLEDGE:
        _fail(reasons, "ACTOR_SELF_KNOWLEDGE_MUST_REMAIN_UNKNOWN")
    if actor_a.get("demographic_or_role_derived") not in (None, [], ()):
        _fail(reasons, "DEMOGRAPHIC_OR_ROLE_PSYCHOGENESIS_FORBIDDEN:actor_a:derived")
    checks["actors_distinct_and_nonpsychogenic"] = not any(
        code.startswith("ACTOR_") or code.startswith("DEMOGRAPHIC_")
        for code in reasons
    )

    history_refs = actor_a.get("history_refs")
    if not isinstance(history_refs, list):
        history_refs = []
        _fail(reasons, "ACTOR_A_HISTORY_REFS_MISSING")
    contrary_refs = actor_a.get("contrary_refs")
    if not isinstance(contrary_refs, list):
        contrary_refs = []
        _fail(reasons, "ACTOR_A_CONTRARY_REFS_MISSING")
    nonperformance_refs = actor_a.get("nonperformance_refs")
    if not isinstance(nonperformance_refs, list):
        nonperformance_refs = []
        _fail(reasons, "ACTOR_A_NONPERFORMANCE_REFS_MISSING")

    enacted_times: list[int] = []
    enacted_owners: set[str] = set()
    for ref in history_refs:
        content = _artifact(bundle, ref, grade, reasons)
        if content is None:
            continue
        if content.get("kind") != "ACTOR_ENACTED":
            _fail(reasons, "ACTOR_HISTORY_KIND_INVALID:" + _string(ref))
            continue
        if content.get("subject") != actor_a_id:
            _fail(reasons, "ACTOR_HISTORY_WRONG_SUBJECT:" + _string(ref))
        if content.get("operation") != PRACTICE_OBJECT:
            _fail(reasons, "ACTOR_HISTORY_WRONG_OPERATION:" + _string(ref))
        if content.get("occurred") is not True:
            _fail(reasons, "ACTOR_HISTORY_NOT_PERFORMED:" + _string(ref))
        if content.get("independent") is not True:
            _fail(reasons, "ACTOR_HISTORY_NOT_INDEPENDENT:" + _string(ref))
        owner = _string(content.get("owner_ref"))
        if not owner or owner in {actor_a_id, actor_b_id}:
            _fail(reasons, "ACTOR_HISTORY_SELF_OR_ACTOR_OWNED:" + _string(ref))
        if owner:
            enacted_owners.add(owner)
        when = _integer(content.get("time"))
        if when is None or as_of is None or when > as_of or when < 0:
            _fail(reasons, "ACTOR_HISTORY_CLOCK_INVALID:" + _string(ref))
        else:
            enacted_times.append(when)

    if len(history_refs) < 2:
        _fail(reasons, "ACTOR_HISTORY_INSUFFICIENT_LONGITUDINAL_OBSERVATIONS")
    if len(enacted_owners) < 2:
        _fail(reasons, "ACTOR_HISTORY_SINGLE_SOURCE_OWNER")
    if len(set(enacted_times)) < 2:
        _fail(reasons, "ACTOR_HISTORY_NO_DISTINCT_TIMES")
    checks["actor_history"] = not any(
        code.startswith("ACTOR_HISTORY_") for code in reasons
    )

    contrary_found = False
    contrary_times: list[int] = []
    for ref in contrary_refs:
        content = _artifact(bundle, ref, grade, reasons)
        if content is None:
            continue
        if content.get("kind") not in {"CONTRARY_ACTION", "CONTRARY_ENACTED"}:
            _fail(reasons, "CONTRARY_KIND_INVALID:" + _string(ref))
            continue
        if content.get("subject") != actor_a_id or content.get("occurred") is not True:
            _fail(reasons, "CONTRARY_RECORD_INVALID:" + _string(ref))
            continue
        when = _integer(content.get("time"))
        if when is None or as_of is None or when > as_of or when < 0:
            _fail(reasons, "CONTRARY_CLOCK_INVALID:" + _string(ref))
            continue
        contrary_found = True
        contrary_times.append(when)
    if not contrary_found:
        _fail(reasons, "CONTRARY_COMMITMENT_EVIDENCE_MISSING")

    nonperformance_found = False
    nonperformance_times: list[int] = []
    for ref in nonperformance_refs:
        content = _artifact(bundle, ref, grade, reasons)
        if content is None:
            continue
        if content.get("kind") != "ACTOR_NONPERFORMANCE":
            _fail(reasons, "NONPERFORMANCE_KIND_INVALID:" + _string(ref))
            continue
        if content.get("subject") != actor_a_id or content.get("occurred") is not False:
            _fail(reasons, "NONPERFORMANCE_RECORD_INVALID:" + _string(ref))
            continue
        if content.get("operation") != PRACTICE_OBJECT:
            _fail(reasons, "NONPERFORMANCE_WRONG_OPERATION:" + _string(ref))
            continue
        when = _integer(content.get("time"))
        if when is None or as_of is None or when > as_of or when < 0:
            _fail(reasons, "NONPERFORMANCE_CLOCK_INVALID:" + _string(ref))
            continue
        nonperformance_found = True
        nonperformance_times.append(when)
    if not nonperformance_found:
        _fail(reasons, "MATCHED_NONPERFORMANCE_EVIDENCE_MISSING")
    checks["rivals_discriminable"] = not any(
        code.startswith("CONTRARY_")
        or code.startswith("NONPERFORMANCE_")
        or code == "MATCHED_NONPERFORMANCE_EVIDENCE_MISSING"
        for code in reasons
    )

    performed_refs = actor_b.get("performed_refs")
    if not isinstance(performed_refs, list):
        performed_refs = []
        _fail(reasons, "ACTOR_B_PERFORMED_REFS_MISSING")
    performed = 0
    for ref in performed_refs:
        content = _artifact(bundle, ref, grade, reasons)
        if content is None:
            continue
        if content.get("kind") not in {"OTHER_OFFER", "OTHER_REFUSAL", "OTHER_ACT"}:
            _fail(reasons, "OTHER_ACT_KIND_INVALID:" + _string(ref))
            continue
        if content.get("subject") != actor_b_id:
            _fail(reasons, "OTHER_ACT_WRONG_SUBJECT:" + _string(ref))
        if content.get("occurred") is not True:
            _fail(reasons, "OTHER_ACT_NOT_PERFORMED:" + _string(ref))
        if content.get("independent") is not True:
            _fail(reasons, "OTHER_ACT_NOT_INDEPENDENT:" + _string(ref))
        owner = _string(content.get("owner_ref"))
        if not owner or owner in {actor_a_id, actor_b_id}:
            _fail(reasons, "OTHER_ACT_SELF_OWNED:" + _string(ref))
        when = _integer(content.get("time"))
        if when is None or as_of is None or when > as_of or when < 0:
            _fail(reasons, "OTHER_ACT_CLOCK_INVALID:" + _string(ref))
        performed += 1
    if performed < 1:
        _fail(reasons, "OTHER_ACT_INSUFFICIENT")
    checks["independent_other"] = not any(
        code.startswith("OTHER_ACT_") for code in reasons
    )

    encounter = _mapping(bundle.get("encounter")) or {}
    opportunity_ref = encounter.get("opportunity_ref")
    encounter_ref = encounter.get("encounter_ref")
    contact_ref = encounter.get("contact_ref")
    opportunity = _artifact(bundle, opportunity_ref, grade, reasons) or {}
    contact = _artifact(bundle, contact_ref, grade, reasons) or {}
    encounter_content = _artifact(bundle, encounter_ref, grade, reasons) or {}
    if opportunity.get("kind") != "ADP010_OPPORTUNITY" or opportunity.get("subject") != actor_a_id:
        _fail(reasons, "ADP010_OPPORTUNITY_INVALID")
    if encounter_content.get("kind") != "ADP010_ENCOUNTER" or encounter_content.get("subject") != actor_a_id:
        _fail(reasons, "ADP010_ENCOUNTER_INVALID")
    if encounter_content.get("parent_ref") != opportunity_ref:
        _fail(reasons, "ADP010_CHAIN_NOT_OPPORTUNITY_TO_ENCOUNTER")
    if contact.get("kind") != "CONTACT_OCCURRENCE":
        _fail(reasons, "ADP010_CONTACT_WITNESS_INVALID")
    if contact.get("co_location_only") is not False:
        _fail(reasons, "ADP010_COLOCATION_IS_NOT_CONTACT")
    if actor_a_id not in (contact.get("participants") or ()) or actor_b_id not in (
        contact.get("participants") or ()
    ):
        _fail(reasons, "ADP010_CONTACT_PARTICIPANTS_INVALID")
    if _string(contact.get("owner_ref")) in {actor_a_id, actor_b_id, ""}:
        _fail(reasons, "ADP010_CONTACT_WITNESS_NOT_INDEPENDENT")
    opportunity_time = _integer(opportunity.get("time"))
    encounter_time = _integer(encounter_content.get("time"))
    if opportunity_time is None or encounter_time is None or opportunity_time > encounter_time:
        _fail(reasons, "ADP010_OPPORTUNITY_ENCOUNTER_CLOCK_INVALID")
    if opportunity_time is not None and as_of is not None and opportunity_time > as_of:
        _fail(reasons, "ADP010_OPPORTUNITY_IN_FUTURE")
    if encounter_time is not None and as_of is not None and encounter_time > as_of:
        _fail(reasons, "ADP010_ENCOUNTER_IN_FUTURE")
    checks["adp010_contact"] = not any(
        code.startswith("ADP010_") for code in reasons
    )

    e1 = _artifact(bundle, bundle.get("e1_ref"), grade, reasons) or {}
    e1_time = _integer(e1.get("time"))
    if e1.get("kind") != "ADP019_ADMISSION":
        _fail(reasons, "ADP019_E1_KIND_INVALID")
    if e1.get("admission_status") != "ADMIT":
        _fail(reasons, "ADP019_E1_NOT_ADMITTED")
    if not _string(e1.get("receipt_id")):
        _fail(reasons, "ADP019_E1_RECEIPT_MISSING")
    if not _string(e1.get("event_id")):
        _fail(reasons, "ADP019_E1_EVENT_ID_MISSING")
    if not _string(e1.get("event_hash")):
        _fail(reasons, "ADP019_E1_EVENT_HASH_MISSING")
    if e1.get("parent_ref") != encounter_ref:
        _fail(reasons, "ADP019_E1_PARENT_NOT_ADP010_ENCOUNTER")
    if _string(e1.get("source_owner_ref")) in {actor_a_id, actor_b_id, ""}:
        _fail(reasons, "ADP019_E1_SOURCE_OWNER_NOT_INDEPENDENT")
    if e1_time is None or encounter_time is None or e1_time < encounter_time:
        _fail(reasons, "ADP019_E1_BEFORE_ENCOUNTER")
    if e1_time is not None and as_of is not None and e1_time > as_of:
        _fail(reasons, "ADP019_E1_IN_FUTURE")
    if e1_time is not None and enacted_times and max(enacted_times) >= e1_time:
        _fail(reasons, "ACTOR_HISTORY_NOT_BEFORE_E1")
    if e1_time is not None and contrary_times and max(contrary_times) >= e1_time:
        _fail(reasons, "ACTOR_CONTRARY_NOT_BEFORE_E1")
    if e1_time is not None and nonperformance_times and max(nonperformance_times) >= e1_time:
        _fail(reasons, "ACTOR_NONPERFORMANCE_NOT_BEFORE_E1")
    checks["adp019_e1"] = not any(
        code.startswith("ADP019_") for code in reasons
    )

    c8 = _artifact(bundle, bundle.get("c8_ref"), grade, reasons) or {}
    if c8.get("kind") != "C8_PROTECTED_WRITER":
        _fail(reasons, "C8_TRUST_KIND_INVALID")
    if c8.get("proof_verified") is not True:
        _fail(reasons, "C8_PROOF_UNVERIFIED")
    if c8.get("monotonic_anchor") is not True:
        _fail(reasons, "C8_EXTERNAL_ANCHOR_NOT_MONOTONIC")
    if not _string(c8.get("writer_ref")) or not _string(c8.get("anchor_ref")):
        _fail(reasons, "C8_WRITER_OR_ANCHOR_MISSING")
    if grade == NATIVE_GRADE:
        if c8.get("protected_writer") is not True:
            _fail(reasons, "C8_PROTECTED_WRITER_REQUIRED")
        if c8.get("key_custody") != "NATIVE_PROTECTED_KMS":
            _fail(reasons, "C8_PROTECTED_KEY_CUSTODY_REQUIRED")
    checks["c8_trust"] = not any(code.startswith("C8_") for code in reasons)

    rule_a_ref = bundle.get("rule_a_ref")
    rule_t_ref = bundle.get("rule_t_ref")
    grant_ref = bundle.get("grant_ref")
    target_ref = bundle.get("target_ref")
    e2_ref = bundle.get("e2_ref")

    rule_a = _artifact(bundle, rule_a_ref, grade, reasons) or {}
    if rule_a.get("kind") != "CAN008_RULE_A":
        _fail(reasons, "CAN008_RULE_A_KIND_INVALID")
    if rule_a.get("authority_id") != "CAN008_R2":
        _fail(reasons, "CAN008_RULE_A_AUTHORITY_INVALID")
    if rule_a.get("semantic_object") != PRACTICE_OBJECT:
        _fail(reasons, "CAN008_RULE_A_OBJECT_INVALID")
    if actor_a_id not in (rule_a.get("subject_refs") or ()):
        _fail(reasons, "CAN008_RULE_A_SUBJECT_MISSING")
    if _string(rule_a.get("issuer_ref")) in {actor_a_id, actor_b_id, ""}:
        _fail(reasons, "CAN008_RULE_A_SELF_ISSUED")
    if _string(rule_a.get("source_owner_ref")) in {actor_a_id, actor_b_id, ""}:
        _fail(reasons, "CAN008_RULE_A_ACTOR_OWNED")
    required_a = {"ACTOR_HISTORY", "ADP010_ENCOUNTER", "ADP019_E1"}
    if not required_a.issubset(set(rule_a.get("readset_classes") or ())):
        _fail(reasons, "CAN008_RULE_A_READSET_INCOMPLETE")
    if e1_time is not None:
        _require_current(rule_a, e1_time, reasons, "CAN008_RULE_A_NOT_CURRENT_AT_E1")
    if as_of is not None:
        _require_current(rule_a, as_of, reasons, "CAN008_RULE_A_STALE_OR_REVOKED")
    checks["can008_rule_a"] = not any(
        code.startswith("CAN008_") for code in reasons
    )

    rule_t = _artifact(bundle, rule_t_ref, grade, reasons) or {}
    if rule_t.get("kind") != "CAN011_RULE_T":
        _fail(reasons, "CAN011_RULE_T_KIND_INVALID")
    if rule_t.get("authority_id") != "CAN011":
        _fail(reasons, "CAN011_RULE_T_AUTHORITY_INVALID")
    if rule_t.get("target_kind") != TARGET_KIND:
        _fail(reasons, "CAN011_TARGET_KIND_INVALID")
    if rule_t.get("semantic_object") != PRACTICE_OBJECT:
        _fail(reasons, "CAN011_TARGET_OBJECT_INVALID")
    if rule_t.get("response_rule_ref") != rule_a_ref:
        _fail(reasons, "CAN011_RULE_T_RESPONSE_DEPENDENCY_MISMATCH")
    if _string(rule_t.get("source_owner_ref")) in {
        _string(rule_a.get("source_owner_ref")),
        _string(rule_a.get("issuer_ref")),
        actor_a_id,
        actor_b_id,
        "",
    }:
        _fail(reasons, "CAN011_TARGET_OWNER_NOT_SEPARATE")
    if _string(rule_t.get("issuer_ref")) in {
        _string(rule_a.get("issuer_ref")),
        _string(rule_a.get("source_owner_ref")),
        actor_a_id,
        actor_b_id,
        "",
    }:
        _fail(reasons, "CAN011_TARGET_ISSUER_NOT_SEPARATE")
    if as_of is not None:
        _require_current(rule_t, as_of, reasons, "CAN011_RULE_T_STALE_OR_REVOKED")
    checks["can011_rule_t"] = not any(
        code.startswith("CAN011_RULE_T_") or code == "CAN011_TARGET_OWNER_NOT_SEPARATE"
        or code == "CAN011_TARGET_ISSUER_NOT_SEPARATE"
        for code in reasons
    )

    grant = _artifact(bundle, grant_ref, grade, reasons) or {}
    if grant.get("kind") != "CAN011_GRANT":
        _fail(reasons, "CAN011_GRANT_KIND_INVALID")
    if grant.get("actor_id") != actor_a_id:
        _fail(reasons, "CAN011_GRANT_ACTOR_MISMATCH")
    if grant.get("rule_a_ref") != rule_a_ref:
        _fail(reasons, "CAN011_GRANT_RULE_A_MISMATCH")
    if grant.get("rule_t_ref") != rule_t_ref:
        _fail(reasons, "CAN011_GRANT_RULE_T_MISMATCH")
    if grant.get("response_ref") != rule_a_ref:
        _fail(reasons, "CAN011_GRANT_RESPONSE_MISMATCH")
    if grant.get("decision") != "CREATE":
        _fail(reasons, "CAN011_GRANT_DECISION_INVALID")
    if _string(grant.get("source_owner_ref")) in {
        _string(rule_a.get("source_owner_ref")),
        _string(rule_a.get("issuer_ref")),
        actor_a_id,
        actor_b_id,
        "",
    }:
        _fail(reasons, "CAN011_GRANT_OWNER_NOT_SEPARATE")
    if not _string(grant.get("before_state_hash")):
        _fail(reasons, "CAN011_GRANT_PRESTATE_MISSING")
    if as_of is not None:
        _require_current(grant, as_of, reasons, "CAN011_GRANT_STALE_OR_REVOKED")
    checks["can011_grant"] = not any(
        code.startswith("CAN011_GRANT_") for code in reasons
    )

    target = _artifact(bundle, target_ref, grade, reasons) or {}
    target_time = _integer(target.get("commit_time"))
    target_state = _string(target.get("state_hash"))
    if target.get("kind") != "TARGET_COMMIT" or target.get("committed") is not True:
        _fail(reasons, "TARGET_COMMIT_NOT_ADMITTED")
    if target.get("e1_ref") != bundle.get("e1_ref"):
        _fail(reasons, "TARGET_E1_BINDING_MISMATCH")
    if target.get("rule_a_ref") != rule_a_ref or target.get("rule_t_ref") != rule_t_ref:
        _fail(reasons, "TARGET_RULE_BINDING_MISMATCH")
    if target.get("grant_ref") != grant_ref:
        _fail(reasons, "TARGET_GRANT_BINDING_MISMATCH")
    if not target_state:
        _fail(reasons, "TARGET_STATE_HASH_MISSING")
    if target_time is None or e1_time is None or target_time < e1_time:
        _fail(reasons, "TARGET_COMMIT_BEFORE_E1")
    if target_time is not None and as_of is not None and target_time > as_of:
        _fail(reasons, "TARGET_COMMIT_IN_FUTURE")
    grant_effective = _integer(grant.get("effective_from"))
    if target_time is None or grant_effective is None or target_time < grant_effective:
        _fail(reasons, "TARGET_COMMIT_BEFORE_GRANT_EFFECTIVE")
    checks["target_commit"] = not any(
        code.startswith("TARGET_") for code in reasons
    )

    e2 = _artifact(bundle, e2_ref, grade, reasons) or {}
    e2_time = _integer(e2.get("action_time"))
    if e2.get("kind") != "E2_PERFORMED" or e2.get("performed") is not True:
        _fail(reasons, "E2_NOT_PERFORMED")
    if e2.get("actor_id") != actor_a_id:
        _fail(reasons, "E2_ACTOR_MISMATCH")
    if e2.get("act") != "inspect_with_tool":
        _fail(reasons, "E2_ACT_MISMATCH")
    if e2.get("consumed_state_hash") != target_state or not target_state:
        _fail(reasons, "E2_CONSUMED_STATE_MISMATCH")
    if _string(e2.get("actuator_ref")) in {actor_a_id, ""}:
        _fail(reasons, "E2_SELF_ACTUATOR")
    if _string(e2.get("occurrence_ref")) in {actor_a_id, ""}:
        _fail(reasons, "E2_OCCURRENCE_SELF_BOUND")
    if _string(e2.get("source_owner_ref")) in {actor_a_id, actor_b_id, ""}:
        _fail(reasons, "E2_SOURCE_OWNER_NOT_INDEPENDENT")
    if e2_time is None or target_time is None or e2_time < target_time:
        _fail(reasons, "E2_ACTION_BEFORE_TARGET_COMMIT")
    if e2_time is not None and as_of is not None and e2_time > as_of:
        _fail(reasons, "E2_ACTION_IN_FUTURE")
    if e2_time is not None:
        _require_current(source_grant, e2_time, reasons, "SOURCE_GRANT_NOT_CURRENT_AT_E2")
    checks["source_grant_current"] = not any(
        code.startswith("SOURCE_GRANT_") for code in reasons
    )
    checks["performed_e2"] = not any(
        code.startswith("E2_") for code in reasons
    )

    required_readset = sorted(
        {
            str(bundle.get("source_grant_ref", "")),
            *(str(ref) for ref in history_refs),
            *(str(ref) for ref in contrary_refs),
            *(str(ref) for ref in nonperformance_refs),
            *(str(ref) for ref in performed_refs),
            str(opportunity_ref or ""),
            str(contact_ref or ""),
            str(encounter_ref or ""),
            str(bundle.get("e1_ref", "")),
            str(bundle.get("c8_ref", "")),
            str(rule_a_ref or ""),
            str(rule_t_ref or ""),
            str(grant_ref or ""),
            str(target_ref or ""),
            str(e2_ref or ""),
        }
    )
    required_readset = [ref for ref in required_readset if ref]
    readset = _mapping(bundle.get("readset")) or {}
    declared = readset.get("declared_refs")
    declared_readset = sorted(declared) if isinstance(declared, list) else []
    if declared_readset != required_readset:
        _fail(reasons, "READSET_DECLARED_REFS_MISMATCH")
    declared_hashes = _mapping(readset.get("content_hashes")) or {}
    for ref in required_readset:
        wrapper = _mapping((_mapping(bundle.get("source_artifacts")) or {}).get(ref)) or {}
        if declared_hashes.get(ref) != wrapper.get("content_hash"):
            _fail(reasons, "READSET_CONTENT_HASH_MISMATCH:" + ref)
    checks["readset_exact"] = not any(
        code.startswith("READSET_") for code in reasons
    )

    if grade == NATIVE_GRADE:
        if signature_verifier is None:
            _fail(reasons, "NATIVE_SIGNATURE_VERIFIER_UNAVAILABLE")
        else:
            artifacts = _mapping(bundle.get("source_artifacts")) or {}
            for ref in required_readset:
                wrapper = _mapping(artifacts.get(ref)) or {}
                signature = _mapping(wrapper.get("signature"))
                if signature is None:
                    _fail(reasons, "NATIVE_SIGNATURE_MISSING:" + ref)
                    continue
                try:
                    ok = signature_verifier.verify(signature)
                except Exception:
                    ok = False
                if ok is not True:
                    _fail(reasons, "NATIVE_SIGNATURE_INVALID:" + ref)
        checks["native_signatures"] = not any(
            code.startswith("NATIVE_SIGNATURE") for code in reasons
        )

    if reasons:
        return _receipt(
            bundle,
            reasons,
            checks,
            mode,
            grade,
            required_readset,
            declared_readset,
        )
    if mode == "TEST_ONLY_TECHNICAL":
        status = STATUS_TECHNICAL_PASS
    else:
        status = STATUS_NATIVE_ELIGIBLE
    return _receipt(
        bundle,
        reasons,
        checks,
        mode,
        grade,
        required_readset,
        declared_readset,
        status=status,
        native_eligible=mode == "NATIVE_CANDIDATE",
    )


def _receipt(
    bundle: Any,
    reasons: list[str],
    checks: Mapping[str, bool],
    mode: str,
    grade: str,
    required_readset: list[str],
    declared_readset: list[str],
    *,
    status: str = STATUS_REFUSED,
    native_eligible: bool = False,
) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "schema": RECEIPT_SCHEMA,
        "preflight_version": PREFLIGHT_VERSION,
        "status": status,
        "mode": mode,
        "grade": grade,
        "native": False,
        "native_eligible": native_eligible,
        "native_issued": False,
        "production_registries": "EMPTY",
        "grant_written": False,
        "reasons": list(reasons),
        "checks": dict(checks),
        "required_readset": list(required_readset),
        "declared_readset": list(declared_readset),
        "input_digest": digest(bundle) if isinstance(bundle, Mapping) else "",
    }
    receipt["receipt_hash"] = digest(receipt)
    return receipt


__all__ = [
    "NATIVE_GRADE",
    "PRACTICE_OBJECT",
    "PREFLIGHT_VERSION",
    "RECEIPT_SCHEMA",
    "SCHEMA",
    "STATUS_NATIVE_ELIGIBLE",
    "STATUS_REFUSED",
    "STATUS_TECHNICAL_PASS",
    "TEST_ONLY_GRADE",
    "canonical",
    "digest",
    "evaluate",
]
