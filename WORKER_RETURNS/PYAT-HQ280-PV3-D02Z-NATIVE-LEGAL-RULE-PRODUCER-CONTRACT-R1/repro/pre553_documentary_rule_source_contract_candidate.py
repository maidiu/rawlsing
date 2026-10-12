"""D02Z candidate, deliberately NONISSUING documentary rule preimage checker.

This module does NOT read a statute, authenticate an issuer, establish source
bytes, issue RULE_TEXT_DOCUMENTED, mint a StructuralObject, or serve N9.
A passing shape check is *only* an inspectable source-science preimage.
It is outside accepted PRE-V3 runtime and must not be wired into production.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Mapping

CONTRACT_ID = "PREV3_ORIGINAL_DOCUMENTARY_LEGAL_RULE_SOURCE@0.1.0-CANDIDATE"
SOURCE_URL = "https://www.brr.gov.gh/acc/registry/docs/Citizenship%20Act%20-%20ACT%20591.pdf"
NO_AUTHORITY_GRANT = "NO_LEGAL_SOURCE_ISSUER__NO_NATIVE_PRODUCER_ADOPTION"

# Deliberately one document-and-clause-specific specimen. An existing immutable
# input can be shape-checked without converting the caller's testimony into law.
EXACT_FIELDS = {
    "contract_id": CONTRACT_ID,
    "documentary_assertion": "SOURCE_TEXT_PREIMAGE_CANDIDATE_ONLY",
    "jurisdiction": "GH",
    "issuing_body": "PARLIAMENT_OF_GHANA",
    "legal_document_id": "ACT_591_2000",
    "clause_id": "PART_I_SECTION_7",
    "legal_text_version": "AS_ENACTED_2000_12_29_RECONSTRUCTION__NOT_CERTIFIED_GAZETTE",
    "assent_date": "2000-12-29",
    "source_url": SOURCE_URL,
    "source_format": "GHANA_GOVERNMENT_HOSTED_DATACENTA_REPRODUCTION",
    "original_pdf_byte_custody": "NOT_CUSTODIED",
    "birth_cohort_operator": "ON_OR_AFTER",
    "birth_cohort_date": "1993-01-07",
    "birthplace_domain": "BORN_IN_OR_OUTSIDE_GHANA",
    "qualifying_ancestor_roles": ["PARENT", "GRANDPARENT"],
    "ancestor_status_original_verb": "WAS_OR_IS",
    "ancestor_status_temporal_context": "AT_DATE_OF_BIRTH_AS_S7_WORDED__NO_INDIVIDUAL_INFERENCE",
    "constitutional_crossref": "ARTICLE_6_2_AFTER_COMMENCEMENT_WORDING__NOT_IDENTICAL_BOUNDARY",
    "constitution_in_force_date": "1993-01-07",
    "gazette_notification_printed": "2001-01-05",
    "BRR_registry_date_labeled_gazette": "2000-12-29",
    "amendment_version_chain": "NOT_CERTIFIED",
    "requested_use": "INSPECT_UNISSUED_DOCUMENTARY_PREIMAGE",
}
MUST_BE_NULL = frozenset({
    "original_pdf_sha256",
    "act_commencement_date",
    "operative_world_asof",
    "legal_individual_status",
    "administrative_observation",
    "observed_service_access",
    "causal_effect",
    "producer_issuer_ref",
    "accepted_source_grant_ref",
    "v557_publication_ref",
    "n9_current_ref",
})
ALLOWED_KEYS = frozenset(EXACT_FIELDS) | MUST_BE_NULL

# No operation below issues an accepted native source fact. This is a
# normative refusal table, not a generalized current-world service.
HELD_OPERATIONS = {
    "ISSUE_RULE_TEXT_DOCUMENTED": "HELD_COMPETENT_ORIGINAL_SOURCE_ISSUER_AND_PRODUCER_ADOPTION",
    "RULE_IN_FORCE_AT_TIME": "HELD_ACT_COMMENCEMENT_AND_AMENDMENT_ASOF_AUTHORITY",
    "INTERPRET_PERSON_CITIZENSHIP": "REFUSED_NO_PERSON_CASE_FACTS_OR_LEGAL_ADJUDICATION",
    "ASSERT_ENFORCEMENT": "REFUSED_NO_OFFICIAL_ADMINISTRATIVE_OBSERVATION",
    "ASSERT_SERVICE_ACCESS": "REFUSED_NO_ACCESS_MEASUREMENT",
    "ASSERT_CAUSAL_MECHANISM": "REFUSED_NO_CAUSAL_MECHANISM_AUTHORITY",
    "EMIT_EMPIRICAL_FACT": "REFUSED_WRONG_EMPIRICAL_OBJECT_FAMILY",
    "EMIT_V554_ROOT": "REFUSED_FORGED_STRUCTURAL_PRODUCER_FAMILY",
    "BIND_V557_V558": "HELD_UNAPPROVED_DOCUMENTARY_ROOT_AND_PUBLICATION_AUTHORITY",
    "SERVE_N9_HISTORICAL": "HELD_NO_ISSUED_RULE_SOURCE_ROOT_OR_N9_CONSUMER",
    "SERVE_N9_CURRENT": "HELD_NO_CURRENT_LEGAL_VERSION_OR_SELECTED_WORLD",
    "G0B_OR_ACTOR_V3": "REFUSED_NO_MODEL_OR_ACTOR_USE_GRANT",
}

@dataclass(frozen=True)
class SourcePreimageDecision:
    state: str
    reasons: tuple[str, ...]
    canonical_input_sha256: str | None
    source_document_pdf_sha256: None
    issued_fact_ref: None
    competent_issuer_ref: None
    permitted_externally_active_uses: tuple[str, ...]
    proposed_rule_class: str = "RULE_TEXT_DOCUMENTED"
    candidate_only: bool = True

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "contract_id": CONTRACT_ID,
            "state": self.state,
            "reasons": list(self.reasons),
            "canonical_input_sha256": self.canonical_input_sha256,
            "source_document_pdf_sha256": self.source_document_pdf_sha256,
            "issued_fact_ref": self.issued_fact_ref,
            "competent_issuer_ref": self.competent_issuer_ref,
            "permitted_externally_active_uses": list(self.permitted_externally_active_uses),
            "proposed_rule_class": self.proposed_rule_class,
            "candidate_only": self.candidate_only,
        }

def _canonical_sha(value: Mapping[str, Any]) -> str:
    blob = json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False)
    return sha256(blob.encode("utf-8")).hexdigest()

def inspect_source_preimage(value: Any) -> SourcePreimageDecision:
    reasons: list[str] = []
    if type(value) is not dict:
        reasons.append("INVALID_TOP_LEVEL_TYPE")
        return SourcePreimageDecision("REFUSED_LOCAL_PREIMAGE", tuple(reasons),
                                      None, None, None, None, ())
    missing = sorted(ALLOWED_KEYS - value.keys())
    extra = sorted(value.keys() - ALLOWED_KEYS)
    if missing:
        reasons.append("MISSING_REQUIRED_KEYS:" + ",".join(missing))
    if extra:
        reasons.append("UNAUTHORIZED_EXTRA_KEYS:" + ",".join(extra))
    for k, expected in EXACT_FIELDS.items():
        if k in value and (type(value[k]) is not type(expected) or value[k] != expected):
            reasons.append("CLAUSE_OR_SOURCE_SEMANTIC_MISMATCH:" + k)
    for k in sorted(MUST_BE_NULL):
        if k in value and value[k] is not None:
            reasons.append("FORBIDDEN_UNPROVED_AUTHORITY_OR_OUTCOME:" + k)
    try:
        digest = _canonical_sha(value)
    except (TypeError, ValueError, OverflowError):
        reasons.append("INVALID_CANONICAL_JSON")
        digest = None
    return SourcePreimageDecision(
        "REFUSED_LOCAL_PREIMAGE" if reasons else "LOCAL_PREIMAGE_SHAPE_POSITIVE__NOT_ISSUED",
        tuple(reasons) if reasons else (NO_AUTHORITY_GRANT,),
        digest, None, None, None, ())

def evaluate_requested_operation(value: Any, operation: str) -> dict[str, Any]:
    pre = inspect_source_preimage(value)
    if pre.state != "LOCAL_PREIMAGE_SHAPE_POSITIVE__NOT_ISSUED":
        return {"operation": operation, "state": "REFUSED_INVALID_SOURCE_PREIMAGE",
                "preimage": pre.to_jsonable(), "issued_fact_ref": None}
    if operation == "INSPECT_UNISSUED_DOCUMENTARY_PREIMAGE":
        return {"operation": operation, "state": pre.state,
                "preimage": pre.to_jsonable(), "issued_fact_ref": None}
    return {"operation": operation,
            "state": HELD_OPERATIONS.get(operation, "REFUSED_UNKNOWN_OPERATION"),
            "preimage": pre.to_jsonable(), "issued_fact_ref": None}
