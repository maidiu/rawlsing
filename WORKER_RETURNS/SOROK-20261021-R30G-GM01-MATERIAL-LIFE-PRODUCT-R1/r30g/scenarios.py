"""Frozen GM01 material cases for the R30G product."""
from __future__ import annotations

from generative_resource import CASE, candidate_resource, evaluate, observation

A = "TEST_ONLY_R30G_A"
B = "TEST_ONLY_R30G_B"
RESOURCE = candidate_resource()


def _event(kind, subject, name, when, performed=True, **payload):
    return observation(kind, subject, "TEST_ONLY_OWNER_" + name, when,
                       ref="TEST_ONLY_EVENT_" + name, performed=performed,
                       **payload)


def case(*, share: bool, e2: bool, contrary: bool = False,
         forged_e2: bool = False, revoked: bool = False) -> dict:
    records = [_event("WORLD", A, "world", 1, tools_for_a=0)]
    records.append(_event(
        "OTHER_PERFORMED", B, "share" if share else "refuse", 5,
        operation="SHARE_TOOL" if share else "REFUSE_TOOL",
        to_actor=A, quantity=1 if share else 0))
    records.append(_event("E1_EVENT", A, "e1", 6))
    if contrary:
        records.append(_event("A_CONTRARY_PROJECT", A, "contrary", 7,
                              operation="INCOMPATIBLE_COMMITMENT"))
    if e2:
        records.append(_event("A_E2_PERFORMED", A, "e2",
                              4 if forged_e2 else 9,
                              operation="INSPECT_WITH_TOOL"))
    return {"schema": CASE, "case_id": "TEST_ONLY_R30G_MATERIAL",
            "actor": A, "other": B, "as_of": 10,
            "social_role": "repair_worker", "demographic_label": "TEST_ONLY",
            "records": records}


def evaluated(*, share: bool, e2: bool, **kwargs) -> dict:
    case_obj = case(share=share, e2=e2, **kwargs)
    result = evaluate(case_obj, RESOURCE)
    if kwargs.get("revoked"):
        result = dict(result)
        result["status"] = "DENY_REVOKED"
    return {"case": case_obj, "gm01": result,
            "resource_hash": RESOURCE["content_hash"]}


def share_e2():
    return evaluated(share=True, e2=True)


def refuse_e2():
    return evaluated(share=False, e2=True)


def share_omit():
    return evaluated(share=True, e2=False)


def refuse_omit():
    return evaluated(share=False, e2=False)


def share_contrary_omit():
    return evaluated(share=True, e2=False, contrary=True)


def forged_e2():
    return evaluated(share=True, e2=True, forged_e2=True)
