"""Frozen GM01 cases for R31J pre-C9 source admission."""
from __future__ import annotations

from generative_resource import CASE, candidate_resource, evaluate, observation

A = "TEST_ONLY_R31J_A"
B = "TEST_ONLY_R31J_B"
RESOURCE = candidate_resource()


def _event(kind, subject, name, when, performed=True, **payload):
    return observation(kind, subject, "TEST_ONLY_OWNER_" + name, when,
                       ref="TEST_ONLY_EVENT_" + name, performed=performed,
                       **payload)


def case(*, share: bool, e2: bool, contrary: bool = False) -> dict:
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
        records.append(_event("A_E2_PERFORMED", A, "e2", 9,
                              operation="INSPECT_WITH_TOOL"))
    return {"schema": CASE, "case_id": "TEST_ONLY_R31J_PREC9",
            "actor": A, "other": B, "as_of": 10,
            "social_role": "repair_worker", "demographic_label": "TEST_ONLY",
            "records": records}


def evaluated(*, share: bool, e2: bool, **kwargs) -> dict:
    case_obj = case(share=share, e2=e2, **kwargs)
    return {"case": case_obj, "gm01": evaluate(case_obj, RESOURCE),
            "resource_hash": RESOURCE["content_hash"]}
