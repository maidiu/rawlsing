"""N1 independent TEST_ONLY source-neutral scientific evidence screen.

NOT a CAN008/CAN011 rule, an issuer, a person generator, or an ADP019 admission.
An evidence-method positive means ONLY that a competent owner may evaluate a
finite proposed acquisition hypothesis. No source-free event produces psychology.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

GRADE = "TEST_ONLY_SOURCEFREE_METHODOLOGY"
SCHEMA = "N1_PRACTICE_EVIDENCE_SCREEN@1"
ACTIONS = {"ACTOR_ENACTED", "OTHER_OFFER", "ADP010_OPPORTUNITY", "ADP010_ENCOUNTER",
           "ADP019_E1", "ACTOR_E2", "CONTRARY_ACTION", "ACTOR_SELF_REPORT", "ROLE_PRIOR"}


def digest(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True).encode("utf-8")).hexdigest()


def seal_record(body: Mapping[str, Any]) -> dict:
    result = dict(body)
    result["hash"] = digest(result)
    return result


def _reply(status: str, reason: str, case: Mapping[str, Any], refs=(), rivals=None) -> dict:
    result = {"schema": SCHEMA, "grade": GRADE, "status": status, "reason": reason,
              "case_id": case.get("case_id", ""), "actor_id": case.get("actor_id", ""),
              "readset": sorted(set(refs)), "rivals": rivals or {},
              "native_rule_issued": False, "target_write_permitted": False,
              "native_actor_fact": False}
    result["screen_hash"] = digest(result)
    return result


def screen(case: Mapping[str, Any]) -> dict:
    """Adversarial method screen, not a developmental transition.

    DENY means source integrity/clock violation, REQUEST_EVIDENCE means a
    missing required issuer observation, NO_CHANGE means no material basis
    for a practice-target petition, COMPETING means rivals not discriminated.
    Only OWNER_REVIEW_CANDIDATE can request a competent scientific decision.
    """
    if not isinstance(case, Mapping):
        return _reply("DENY", "INVALID_CASE", {})
    actor, other = case.get("actor_id"), case.get("other_actor_id")
    now, entries = case.get("as_of"), case.get("records")
    if not all(isinstance(x, str) and x.startswith("TEST_ONLY_") for x in (actor, other)) or actor == other:
        return _reply("DENY", "ACTOR_OTHER_IDENTITY_INVALID", case)
    if not isinstance(now, int) or isinstance(now, bool) or not isinstance(entries, list):
        return _reply("DENY", "CLOCK_OR_RECORDS_INVALID", case)
    seen, groups = set(), {kind: [] for kind in ACTIONS}
    for rec in entries:
        if not isinstance(rec, dict) or rec.get("kind") not in ACTIONS:
            return _reply("DENY", "RECORD_KIND_INVALID", case)
        h = rec.get("hash")
        body = {k: v for k, v in rec.items() if k != "hash"}
        if not isinstance(h, str) or h != digest(body):
            return _reply("DENY", "SOURCE_CONTENT_HASH_INVALID", case)
        ref, owner, subject, when = [rec.get(k) for k in ("ref", "owner", "subject", "time")]
        if not isinstance(ref, str) or not ref.startswith("TEST_ONLY_") or ref in seen:
            return _reply("DENY", "DUPLICATE_OR_UNQUALIFIED_SOURCE_REF", case)
        seen.add(ref)
        if rec.get("grade") != GRADE or not isinstance(owner, str) or not owner.startswith("TEST_ONLY_"):
            return _reply("DENY", "SOURCE_OWNER_GRADE_INVALID", case)
        if subject not in (actor, other) or owner in (actor, other):
            return _reply("DENY", "SELF_AUTHORED_OR_FOREIGN_SOURCE", case)
        if not isinstance(when, int) or isinstance(when, bool) or when > now or when < 0:
            return _reply("DENY", "EVENT_CLOCK_INVALID", case)
        if rec["kind"] in {"ACTOR_ENACTED", "ACTOR_E2", "CONTRARY_ACTION"} and subject != actor:
            return _reply("DENY", "FOCAL_ENACTMENT_WRONG_ACTOR", case)
        if rec["kind"] == "OTHER_OFFER" and subject != other:
            return _reply("DENY", "OTHER_OFFER_WRONG_ACTOR", case)
        groups[rec["kind"]].append(rec)
    refs = tuple(seen)
    opp, enc, e1 = (groups[k] for k in ("ADP010_OPPORTUNITY", "ADP010_ENCOUNTER", "ADP019_E1"))
    if not opp or not enc or not e1:
        return _reply("REQUEST_EVIDENCE", "ADP010_OR_ADP019_OWNER_WITNESS_MISSING", case, refs)
    if not (min(r["time"] for r in opp) <= min(r["time"] for r in enc)
            <= min(r["time"] for r in e1)):
        return _reply("DENY", "OPPORTUNITY_ENCOUNTER_E1_TIME_REVERSED", case, refs)
    if not all(r.get("occurred") is True for r in enc + e1):
        return _reply("REQUEST_EVIDENCE", "ENCOUNTER_OR_E1_NOT_OCCURRED", case, refs)
    acts = sorted(groups["ACTOR_ENACTED"], key=lambda x: (x["time"], x["ref"]))
    independent = [x for x in acts if x.get("occurred") is True and x.get("operation") == case.get("operation")]
    offers = [x for x in groups["OTHER_OFFER"] if x.get("occurred") is True]
    contrary = groups["CONTRARY_ACTION"]
    rivals = {
        "H1_enacted_material_practice": "MATERIAL_EPISODES_PRESENT" if independent else "UNOBSERVED",
        "H2_other_person_participation": "INDEPENDENT_OTHER_OFFER_PRESENT" if offers else "UNOBSERVED",
        "H3_contradictory_commitments": "CONTRARY_ENACTED_EVIDENCE_PRESENT" if contrary else "NOT_OBSERVED_NOT_ABSENT",
        "H0_role_or_fixture_only": "NOT_EXCLUDED_BY_TEST_ONLY_EVIDENCE",
        "actor_self_knowledge": "UNKNOWN_WITHOUT_ADP017"}
    if contrary:
        return _reply("COMPETING", "CONTRARY_PRACTICE_EVIDENCE_UNRESOLVED", case, refs, rivals)
    if not independent or not offers:
        return _reply("NO_CHANGE", "NO_ENACTED_AND_OTHER_PARTICIPATION_BASIS", case, refs, rivals)
    if len({(x["ref"], x["time"]) for x in independent}) < 2:
        return _reply("REQUEST_EVIDENCE", "NO_DISTINCT_LONGITUDINAL_OBSERVATIONS", case, refs, rivals)
    if len({x["owner"] for x in independent}) < 2:
        return _reply("REQUEST_EVIDENCE", "SINGLE_METHOD_OR_SOURCE_OWNER", case, refs, rivals)
    if not (max(x["time"] for x in independent) < min(x["time"] for x in e1)):
        return _reply("DENY", "RETROCAUSAL_PRACTICE_EVIDENCE", case, refs, rivals)
    return _reply("OWNER_REVIEW_CANDIDATE", "FINITE_EVIDENCE_ONLY_NOT_PSYCHOGENESIS", case, refs, rivals)


def compile_test_only_bp2_resources(case: Mapping[str, Any], ports: Any, *, now: int) -> dict:
    """Bind two *separate TEST_ONLY* candidate resources through actual BP2 ports.

    Caller supplies the actual vendor/bp2/bp2_joined/ports.py. This function
    does NOT compile an issued rule or target grant, does NOT touch production
    registries, and refuses unless method screen is review-eligible.
    """
    result = screen(case)
    if result["status"] != "OWNER_REVIEW_CANDIDATE":
        return {"status": result["status"], "screen": result,
                "rule_a": None, "rule_t": None, "grant": None}
    if ports is None:
        raise ValueError("ACTUAL_BP2_PORTS_REQUIRED")
    actor = case["actor_id"]
    semantics_a = {"rule_id": "TEST_ONLY_N1_RULE_A", "rule_version": "1",
                   "authority_id": "TEST_ONLY_CAN008", "authority_version": "1",
                   "allowed_subjects": [actor],
                   "permitted_readset_classes": ["ResolvedStructuralContext"],
                   "predicates": ["OWNER_REVIEW_ONLY_NOT_CAUSAL_SCIENCE"], "native": False}
    hash_a = digest(semantics_a)
    body_a = {"schema": "BP2_CAN008_RULE_A@1", "issuer_ref": "TEST_ONLY_N1_CAN008_ISSUER",
              "issuer_verified": True, "grade": ports.TEST_ONLY_GRADE,
              "rule_content_hash": hash_a, "rule_semantics": semantics_a,
              "native_claim": False}
    ra = ports.test_only_rule_resource(
        resource_id="TEST_ONLY_N1_A_RESOURCE", version="1", body=body_a,
        issuer_ref="TEST_ONLY_N1_CAN008_ISSUER", source_owner="TEST_ONLY_N1_CAN008_OWNER",
        permission_ref="TEST_ONLY_N1_A_SCOPE", effective_from=0,
        readset_refs=("ResolvedStructuralContext",), currentness_as_of=0)
    ports.CAN008RulePort().bind(rule=ra, subject=actor,
                               conditioning_class="ResolvedStructuralContext", now=now)
    semantics_t = {"rule_id": "TEST_ONLY_N1_RULE_T", "rule_version": "1",
                   "authority_id": "TEST_ONLY_CAN011", "authority_version": "1",
                   "response_rule_content_hash": hash_a, "state_kind_id": "V3MS_PRACTICE",
                   "allowed_operations": ["CREATE"],
                   "accepted_semantic_objects": ["c9p:coordinated_material_inspection"],
                   "native": False}
    body_t = {"schema": "BP2_CAN011_RULE_T@1", "issuer_ref": "TEST_ONLY_N1_CAN011_ISSUER",
              "grade": ports.TEST_ONLY_GRADE, "rule_content_hash": hash_a,
              "rule_t_content_hash": digest(semantics_t),
              "rule_semantics": semantics_t, "native_claim": False}
    rt = ports.test_only_rule_resource(
        resource_id="TEST_ONLY_N1_T_RESOURCE", version="1", body=body_t,
        issuer_ref="TEST_ONLY_N1_CAN011_ISSUER", source_owner="TEST_ONLY_N1_CAN011_OWNER",
        permission_ref="TEST_ONLY_N1_T_SCOPE", effective_from=0,
        readset_refs=("ResolvedStructuralContext",), currentness_as_of=0)
    ports.CAN011TargetPort(response_owner="TEST_ONLY_N1_CAN008_OWNER").bind_rule(rule=rt, now=now)
    return {"status": "TEST_ONLY_PORTS_BOUND_NOT_ISSUED", "screen": result,
            "rule_a": ra, "rule_t": rt, "grant": None,
            "native_registry_mutation": False,
            "downstream_state_change": False}
