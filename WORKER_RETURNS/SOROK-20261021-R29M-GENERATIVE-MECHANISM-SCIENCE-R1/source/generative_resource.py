"""R29M source-neutral conditional material/other-mediated actor action mechanism.

CANDIDATE_SOURCEFREE_NOT_NATIVE. This module neither generates real source
receipts nor issues CAN008/CAN011, ADP, C8, Pyat or C11 permissions. It keeps
actual action, an opportunity, and learned disposition separate.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

SCHEMA = "GENERATIVE_SCIENCE_RESOURCE_CANDIDATE@1"
CASE = "R29M_CONDITIONAL_ACTIVITY_INPUT@1"
GRADE = "TEST_ONLY_SOURCE_NEUTRAL_CANDIDATE"
A_OWNER = "TEST_ONLY_R29M_CAN008_SCIENCE_PROPOSAL_NOT_ISSUER"
T_OWNER = "TEST_ONLY_R29M_CAN011_SCIENCE_PROPOSAL_NOT_ISSUER"
KINDS = {"WORLD", "OTHER_PERFORMED", "E1_EVENT", "A_PAST_ENACTED", "A_E2_PERFORMED", "A_CONTRARY_PROJECT"}


def sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
                                     separators=(",", ":")).encode()).hexdigest()


def sealed(body: Mapping[str, Any]) -> dict:
    result = dict(body)
    result["content_hash"] = sha(result)
    return result


def observation(kind: str, subject: str, owner: str, when: int, *,
                ref: str, performed: bool = True, **payload: Any) -> dict:
    """TEST_ONLY fixture factory; source identifiers have no custody authority."""
    return sealed(dict(kind=kind, subject=subject, owner=owner, at=when,
                       ref=ref, performed=performed, payload=payload,
                       grade=GRADE))


def candidate_resource() -> dict:
    # Each content hash is a *proposal fingerprint*, not an issued signature.
    a = dict(rule_id="TEST_ONLY_R29M_A1", owner=A_OWNER,
             operation="PERSON_X_E1_RECEIVABILITY_CONDITIONED_BY_EXTERNAL_MATERIAL_OPTION",
             event_role="E1_SOURCE_EVENT_NOT_MERE_EXPOSURE",
             alternatives=["OPPORTUNITY_NEWLY_FEASIBLE", "OPPORTUNITY_UNCHANGED",
                           "UNKNOWN", "NO_CHANGE", "DENY"],
             actor_response_policy="NO_UNWITNESSED_UPTAKE_OR_AUTOMATIC_ACTION",
             native=False)
    t = dict(rule_id="TEST_ONLY_R29M_T1", owner=T_OWNER,
             state_kind="V3MS_PRACTICE", semantic_object="c9p:coordinated_material_inspection",
             operation="NO_CHANGE", response_rule_content_hash=sha(a),
             explanation="NO_DOMAIN_SPECIFIC_ACQUISITION_RULE_EMPIRICALLY_ISSUED",
             native=False)
    body = dict(schema=SCHEMA, resource_version="1", status="PROPOSAL_NOT_ISSUED",
                science_tier="MATERIAL_OPPORTUNITY_AND_PERFORMED_ACTION_ONLY",
                science_grade="THEORY_PLUS_BROAD_LONGITUDINAL_ANALOGY__NO_DOMAIN_TRANSFER_WARRANT",
                source_evidence=[dict(kind="EMPIRICAL_PUBLISHED_LONGITUDINAL",
                     doi="10.1086/227593", authors="Kohn and Schooler", year=1982,
                     scope="work conditions reciprocal with orientations, not an inspection-practice rule",
                     full_content_sha256="NOT_VERIFIED_FOR_NATIVE_SOURCE_REGISTRY",
                     source_rights="BIBLIOGRAPHIC_SCIENTIFIC_REFERENCE_ONLY")],
                transport_grade="NOT_ESTABLISHED_FOR_SYNTHETIC_ACTOR_PSYCHOGENESIS",
                actor_source_grade=GRADE, original_actor_observed=False,
                original_identical_real_dyad_required=False,
                actual_source_permission="NOT_GRANTED",
                effective_from=0, expires_at=None, revoked=False,
                currentness_scope="TEST_ONLY_AS_OF_INTEGER_CLOCK",
                uncertainty="H0_REMAINS_UNEXCLUDED__DURABLE_PRACTICE_NOT_WARRANTED",
                hypotheses=["H1_ENACTED_PRACTICE", "H2_INDEPENDENT_B_MEDIATION",
                            "H3_CONTRADICTORY_PROJECTS_SCARCITY", "H0_ROLE_TASK_FIXTURE_SELECTION"],
                candidate_rule_a=a, candidate_rule_a_hash=sha(a),
                candidate_rule_t=t, candidate_rule_t_hash=sha(t),
                native_grant=None, source_grant=None,
                production_registries={"CAN008": [], "CAN011": []},
                scientific_issuer_decision="REQUEST_EVIDENCE_FOR_CAN011_PRACTICE",
                legal_issuance=False)
    body["content_hash"] = sha(body)
    return body


def _out(code: str, *, case: Mapping[str, Any], evidence=(),
         available_before=None, available_after=None, b_effect=False,
         e2=False, practical_result="NO_CHANGE", rivals=None) -> dict:
    # An engine may know the event; actor uptake/actor knowledge remain unknown.
    result = dict(schema="R29M_CONDITIONAL_MECHANISM_RESULT@1", grade=GRADE,
        case_id=case.get("case_id"), actor=case.get("actor"), other=case.get("other"),
        status=code, readset=sorted(evidence),
        material_feasible_before=available_before,
        material_feasible_after=available_after,
        independent_other_changes_options=b_effect,
        actor_e2_performed=e2, world_effect=practical_result,
        rule_a_result="CANDIDATE_CONDITIONING_EVIDENCE_ONLY__RECEIVABILITY_NOT_INFERRED" if available_after is not None else "VALID_EMPTY",
        rule_t_result="NO_CHANGE", rule_t_grant=None, v3ms_created=0,
        psyche_delta={}, belief_delta={}, self_account_delta={},
        actor_receivability="UNKNOWN_ADP010_CAN008_NATIVE_NOT_ISSUED",
        hypotheses=rivals or {"H1":"NOT_VALIDATED", "H2":"NOT_VALIDATED", "H3":"UNRESOLVED", "H0":"LIVE"},
        native_actor=False, native_rules_issued=False, native_source_grant=False)
    result["result_hash"] = sha(result)
    return result


def evaluate(case: Mapping[str, Any], resource: Mapping[str, Any]) -> dict:
    """Return material choice/actual act without creating a psyche or choosing for A.

    World actor/action sources must be owner-authenticated elsewhere; this
    TEST_ONLY screen can detect invalid fixture preimages but cannot sign them.
    Two events or two distinct source IDs never automatically acquire a trait.
    """
    if not isinstance(case, Mapping) or not isinstance(resource, Mapping):
        return _out("DENY_BAD_INPUT", case={})
    content = {k: v for k, v in resource.items() if k != "content_hash"}
    if (resource.get("schema") != SCHEMA or resource.get("status") != "PROPOSAL_NOT_ISSUED"
        or resource.get("content_hash") != sha(content)
        or resource.get("native_grant") is not None
        or resource.get("source_grant") is not None
        or resource.get("legal_issuance") is not False
        or resource.get("production_registries") != {"CAN008": [], "CAN011": []}):
        return _out("DENY_RESOURCE_TAMPER_OR_NATIVE_AUTHORITY", case=case)
    if resource.get("revoked"):
        return _out("DENY_REVOKED", case=case)
    a, b, asof = case.get("actor"), case.get("other"), case.get("as_of")
    if (case.get("schema") != CASE or not isinstance(a, str) or not a.startswith("TEST_ONLY_")
        or not isinstance(b, str) or not b.startswith("TEST_ONLY_") or a == b
        or type(asof) is not int or asof < resource.get("effective_from", 0)
        or (resource.get("expires_at") is not None and asof >= resource["expires_at"])):
        return _out("DENY_CASE_IDENTITY_OR_TIME", case=case)
    records = case.get("records")
    if not isinstance(records, list):
        return _out("DENY_RECORDS", case=case)
    kinds = {k: [] for k in KINDS}
    refs = []
    for record in records:
        if not isinstance(record, Mapping):
            return _out("DENY_RECORD_SHAPE", case=case, evidence=refs)
        body = {k: v for k, v in record.items() if k != "content_hash"}
        kind, person, owner = record.get("kind"), record.get("subject"), record.get("owner")
        ref, time = record.get("ref"), record.get("at")
        if (kind not in KINDS or record.get("content_hash") != sha(body)
            or record.get("grade") != GRADE or not isinstance(ref, str)
            or not ref.startswith("TEST_ONLY_") or ref in refs
            or not isinstance(owner, str) or not owner.startswith("TEST_ONLY_OWNER_")
            or owner in (a,b) or person not in (a,b)
            or type(time) is not int or time < 0 or time > asof
            or type(record.get("performed")) is not bool or not isinstance(record.get("payload"), dict)):
            return _out("DENY_SOURCE_INTEGRITY_OWNER_CLOCK", case=case, evidence=refs)
        if kind in ("WORLD", "A_PAST_ENACTED", "A_E2_PERFORMED", "A_CONTRARY_PROJECT") and person != a:
            return _out("DENY_WRONG_ACTOR", case=case, evidence=refs)
        if kind == "OTHER_PERFORMED" and person != b:
            return _out("DENY_B_NOT_INDEPENDENT_ACTOR", case=case, evidence=refs)
        if kind == "E1_EVENT" and person != a:
            return _out("DENY_E1_OTHER_ACTOR", case=case, evidence=refs)
        refs.append(ref)
        kinds[kind].append(record)
    worlds = kinds["WORLD"]
    if len(worlds) != 1 or not worlds[0]["performed"]:
        return _out("HOLD_WORLD_SOURCE_MISSING", case=case, evidence=refs)
    w = worlds[0]
    count = w["payload"].get("tools_for_a")
    if type(count) is not int or count < 0:
        return _out("DENY_WORLD_MATERIAL", case=case, evidence=refs)
    if len(kinds["E1_EVENT"]) != 1 or not kinds["E1_EVENT"][0]["performed"]:
        return _out("HOLD_E1_NOT_ADMITTED_TEST_ONLY", case=case, evidence=refs)
    e1 = kinds["E1_EVENT"][0]
    if w["at"] > e1["at"]:
        return _out("DENY_WORLD_AFTER_E1", case=case, evidence=refs)
    b_events = [x for x in kinds["OTHER_PERFORMED"] if x["performed"] and
                x["payload"].get("operation") == "SHARE_TOOL" and
                x["payload"].get("to_actor") == a and w["at"] <= x["at"] <= e1["at"]]
    # B must be free to decline. Only performed material transfer alters options.
    transfer = sum(int(x["payload"].get("quantity", 0)) for x in b_events
                   if type(x["payload"].get("quantity")) is int and x["payload"]["quantity"] > 0)
    options_before = count > 0
    options_after = count + transfer > 0
    past = [x for x in kinds["A_PAST_ENACTED"] if x["performed"] and
            x["payload"].get("operation") == "INSPECT_WITH_TOOL" and x["at"] < e1["at"]]
    contrary = any(x["performed"] for x in kinds["A_CONTRARY_PROJECT"])
    next_actions = [x for x in kinds["A_E2_PERFORMED"] if x["performed"]]
    if any(x["at"] <= e1["at"] for x in next_actions):
        return _out("DENY_E2_NOT_LATER", case=case, evidence=refs)
    e2_inspect = [x for x in next_actions if x["payload"].get("operation") == "INSPECT_WITH_TOOL"]
    if e2_inspect and not options_after:
        return _out("DENY_ACTION_WITHOUT_MATERIAL", case=case, evidence=refs,
                    available_before=options_before,available_after=options_after)
    status = ("UNCERTAIN_CONTRADICTORY_PROJECTS" if contrary and not next_actions else
              "OPPORTUNITY_CHANGED_BY_INDEPENDENT_B" if not options_before and options_after else
              "OPPORTUNITY_UNCHANGED")
    result = "INSPECTION_OCCURRED" if e2_inspect else "NO_CHANGE"
    return _out(status, case=case, evidence=refs,
                available_before=options_before, available_after=options_after,
                b_effect=not options_before and options_after,
                e2=bool(e2_inspect), practical_result=result,
                rivals=dict(H1="PAST_ACTION_PRESENT_NO_ACQUISITION_LAW" if past else "PAST_ACTION_ABSENT",
                            H2="ACTUAL_INDEPENDENT_B_CHANGED_OPTIONS" if transfer else "B_NO_RELEVANT_TRANSFER",
                            H3="CONTRARY_PROJECT_PRESENT_NOT_RESOLVED" if contrary else "NOT_OBSERVED_NOT_ABSENT",
                            H0="STILL_LIVE_SELECTION_AND_ROLE_ONLY_NO_PSYCHIC_LEARNING_TEST"))


def bp2_test_only_resources(ports: Any, resource: Mapping[str, Any], subject: str, now: int) -> dict:
    """Adapt candidate to the actual BP2/C9R *receiving ports*, never issue.

    A is a strictly TEST_ONLY response resource. T is an independent owner
    no-change resource; grant remains None and neither registry is populated.
    """
    if evaluate({"schema": CASE,"actor": subject,"other": "TEST_ONLY_NO_OTHER",
                 "as_of": now,"records": []}, resource)["status"] == "DENY_RESOURCE_TAMPER_OR_NATIVE_AUTHORITY":
        raise ValueError("INVALID_CANDIDATE_RESOURCE")
    sem_a = {"rule_id":"TEST_ONLY_R29M_CAN008_A", "rule_version":"1", "authority_id":"TEST_ONLY_CAN008",
             "authority_version":"1", "allowed_subjects":[subject],
             "permitted_readset_classes":["ResolvedStructuralContext"],
             "predicates":["MATERIAL_FEASIBILITY_ONLY_NO_PSYCHIC_WARRANT"], "native":False}
    hash_a = sha(sem_a)
    body_a = {"schema":"BP2_CAN008_RULE_A@1", "issuer_ref":A_OWNER,
              "issuer_verified":False,"grade":ports.TEST_ONLY_GRADE,
              "rule_content_hash":hash_a,"rule_semantics":sem_a,"native_claim":False}
    ra = ports.test_only_rule_resource(resource_id="TEST_ONLY_R29M_A_RESOURCE", version="1",
        body=body_a, issuer_ref=A_OWNER, source_owner="TEST_ONLY_R29M_CAN008_OWNER",
        permission_ref="TEST_ONLY_SCIENCE_CANDIDATE_NOT_NATIVE_PERMISSION",effective_from=0,
        readset_refs=("ResolvedStructuralContext",),currentness_as_of=0)
    ports.CAN008RulePort().bind(rule=ra,subject=subject,conditioning_class="ResolvedStructuralContext",now=now)
    sem_t = {"rule_id":"TEST_ONLY_R29M_CAN011_T", "rule_version":"1", "authority_id":"TEST_ONLY_CAN011",
             "authority_version":"1", "response_rule_content_hash":hash_a,
             "state_kind_id":"V3MS_PRACTICE", "allowed_operations":["NO_CHANGE"],
             "accepted_semantic_objects":["c9p:coordinated_material_inspection"],"native":False}
    body_t = {"schema":"BP2_CAN011_RULE_T@1", "issuer_ref":T_OWNER, "grade":ports.TEST_ONLY_GRADE,
              "rule_content_hash":hash_a,"rule_t_content_hash":sha(sem_t),
              "rule_semantics":sem_t,"native_claim":False}
    rt = ports.test_only_rule_resource(resource_id="TEST_ONLY_R29M_T_RESOURCE",version="1",
        body=body_t,issuer_ref=T_OWNER,source_owner="TEST_ONLY_R29M_CAN011_OWNER",
        permission_ref="TEST_ONLY_CANDIDATE_NO_GRANT",effective_from=0,
        readset_refs=("ResolvedStructuralContext",),currentness_as_of=0)
    ports.CAN011TargetPort(response_owner="TEST_ONLY_R29M_CAN008_OWNER").bind_rule(rule=rt, now=now)
    return {"grade":GRADE,"rule_a":ra,"rule_t":rt,"grant":None,
            "actual_target_mutations":0,"native_issuer":None,"production_registry_writes":0,
            "scope":"TEST_ONLY_BP2_PORT_CONTENT_COMPATIBILITY_ONLY"}