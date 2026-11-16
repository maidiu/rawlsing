"""Explicitly sourced synthetic actor-context/history records for S39."""
from __future__ import annotations

from typing import Any, Mapping

from .bootstrap import install

install()

from candidate import digest, seal, valid  # noqa: E402

SCHEMA = "S39_ACTOR_CONTEXT_SOURCE@1"
GRADE = "TEST_ONLY_SYNTHETIC_ACTOR_CONTEXT_MODEL_PREMISE_NOT_OBSERVED"
CONTEXT_KINDS = frozenset({"CURRENT_PROJECT", "ACTOR_PRIORITY", "HISTORICAL_EPISODE"})
IGNORED_LABEL_KINDS = frozenset({"DEMOGRAPHIC_LABEL", "TYPE_LABEL", "LABEL_ONLY"})
FORBIDDEN_KEYS = frozenset({
    "selected_action", "desired_action", "response_witness",
    "performed_response", "action_witness", "preferred_action", "answer",
    "requested_option", "chosen_action",
})
_SOURCE_KEYS = (
    "schema", "source_ref", "source_class", "actor_id", "branch_id",
    "as_of", "predicate", "value", "content", "source_grade", "native",
    "psychology_claim", "model_premise", "recruitment_mode",
)


def _forbidden(value: Any) -> str | None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str) and key.lower() in FORBIDDEN_KEYS:
                return key
            found = _forbidden(item)
            if found:
                return found
    elif isinstance(value, (list, tuple)):
        for item in value:
            found = _forbidden(item)
            if found:
                return found
    return None


def source_digest(record: Mapping[str, Any]) -> str:
    return digest({key: record.get(key) for key in _SOURCE_KEYS})


def make_source(
    *,
    source_ref: str,
    source_class: str,
    actor_id: str,
    branch_id: str,
    as_of: int,
    predicate: str,
    value: int,
    content: Mapping[str, Any] | None = None,
    recruitment_mode: str = "CAUSAL_NOT_CONSCIOUS_RECALL",
) -> dict:
    body = {
        "schema": SCHEMA,
        "source_ref": source_ref,
        "source_class": source_class,
        "actor_id": actor_id,
        "branch_id": branch_id,
        "as_of": as_of,
        "predicate": predicate,
        "value": int(value),
        "content": dict(content or {}),
        "source_grade": GRADE,
        "native": False,
        "psychology_claim": False,
        "model_premise": True,
        "recruitment_mode": recruitment_mode,
    }
    bad = _forbidden(body)
    if bad:
        raise ValueError("S39_FORBIDDEN_INPUT_KEY:" + bad)
    return seal(dict(body, source_hash=digest(body)))


def validate_source(record: Mapping[str, Any], *, actor_id: str,
                    branch_id: str, as_of: int) -> dict:
    if not isinstance(record, Mapping) or not valid(dict(record)):
        raise ValueError("S39_SOURCE_INTEGRITY_FAILURE")
    if record.get("schema") != SCHEMA:
        raise ValueError("S39_SOURCE_SCHEMA_MISMATCH")
    if record.get("source_hash") != source_digest(record):
        raise ValueError("S39_SOURCE_HASH_MISMATCH")
    if record.get("actor_id") != actor_id:
        raise ValueError("S39_SOURCE_ACTOR_MISMATCH")
    if record.get("branch_id") != branch_id:
        raise ValueError("S39_SOURCE_BRANCH_MISMATCH")
    if not isinstance(record.get("as_of"), int) or record["as_of"] > as_of:
        raise ValueError("S39_SOURCE_TIME_INVALID")
    if record.get("source_grade") != GRADE:
        raise ValueError("S39_SOURCE_GRADE_INVALID")
    if record.get("native") is not False or record.get("psychology_claim") is not False:
        raise ValueError("S39_SOURCE_NATIVE_OR_PSYCHOLOGY_CLAIM")
    if record.get("model_premise") is not True:
        raise ValueError("S39_SOURCE_NOT_MODEL_PREMISE")
    if record.get("source_class") not in CONTEXT_KINDS | IGNORED_LABEL_KINDS:
        raise ValueError("S39_SOURCE_CLASS_INVALID")
    if record.get("source_class") in IGNORED_LABEL_KINDS:
        return dict(record)
    bad = _forbidden(record)
    if bad:
        raise ValueError("S39_FORBIDDEN_INPUT_KEY:" + bad)
    return dict(record)


def context_records(*, actor_id: str, branch_id: str, as_of: int,
                    repair_urgent: bool = False,
                    avoid_debt: bool = False,
                    prefer_independent: bool = False,
                    prior_b_share: bool = False,
                    prior_b_refusal: bool = False,
                    labels: Mapping[str, Any] | None = None) -> list[dict]:
    records = []
    if repair_urgent:
        records.append(make_source(
            source_ref="TEST_ONLY_S39_CTX_REPAIR_URGENT",
            source_class="CURRENT_PROJECT", actor_id=actor_id,
            branch_id=branch_id, as_of=as_of,
            predicate="REPAIR_URGENT", value=1,
            content={"project": "repair_seam_urgent"}))
    if avoid_debt:
        records.append(make_source(
            source_ref="TEST_ONLY_S39_CTX_AVOID_DEBT",
            source_class="ACTOR_PRIORITY", actor_id=actor_id,
            branch_id=branch_id, as_of=as_of,
            predicate="AVOID_DEBT", value=1,
            content={"priority": "avoid_new_debt"}))
    if prefer_independent:
        records.append(make_source(
            source_ref="TEST_ONLY_S39_CTX_PREFER_INDEPENDENT",
            source_class="ACTOR_PRIORITY", actor_id=actor_id,
            branch_id=branch_id, as_of=as_of,
            predicate="PREFER_INDEPENDENT", value=1,
            content={"priority": "independent_inspection_preferred"}))
    if prior_b_share:
        records.append(make_source(
            source_ref="TEST_ONLY_S39_HIST_B_PRIOR_SHARE",
            source_class="HISTORICAL_EPISODE", actor_id=actor_id,
            branch_id=branch_id, as_of=as_of,
            predicate="PRIOR_B_SHARE", value=1,
            content={"episode": "other_party_shared_before"}))
    if prior_b_refusal:
        records.append(make_source(
            source_ref="TEST_ONLY_S39_HIST_B_PRIOR_REFUSAL",
            source_class="HISTORICAL_EPISODE", actor_id=actor_id,
            branch_id=branch_id, as_of=as_of,
            predicate="PRIOR_B_REFUSAL", value=1,
            content={"episode": "other_party_refused_before"}))
    if labels:
        for key, value in labels.items():
            records.append(make_source(
                source_ref="TEST_ONLY_S39_LABEL_" + str(key).upper(),
                source_class="LABEL_ONLY", actor_id=actor_id,
                branch_id=branch_id, as_of=as_of,
                predicate=str(key), value=0,
                content={"label": str(value)}))
    return records


__all__ = [
    "CONTEXT_KINDS",
    "GRADE",
    "IGNORED_LABEL_KINDS",
    "SCHEMA",
    "context_records",
    "make_source",
    "source_digest",
    "validate_source",
]
