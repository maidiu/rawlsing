#!/usr/bin/env python3
"""Independent sourcefree probe for PR #774 Q86 guard.

Run with PYTHONPATH=<pinned 9c776b sparse worktree> and python3 -P.
Uses unchanged pinned source/test fixture builders; no monkeypatch.
Writes only C18 lease output.
"""
from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from rawlsing_next.field_forge_conditional_support import (
    FieldForgeConditionalSupportError,
    produce_exact_conditional_support_profile,
)
from rawlsing_next.gt12_c_to_d_relation_bridge import (
    GT12CToDBridgeError,
    admit_gt12_c_relation,
    bridge_gt12_c_relation_to_d_evidence,
    make_gt12_c_to_d_admission_rule,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.wave1_ff_prev3_relation_admission import (
    AdmissionDecision,
    RelationAdmissionRequest,
    evaluate_gt2_relation_admission,
    GT2_TARGET_USE,
)
from rawlsing_next.wave1_r5_q86_c11_projection import question_ref
from rawlsing_next.pre553_repo_native_current_payload import (
    load_current_gt2_query_fact_from_committed_transport,
)
from rawlsing_next.tests.test_field_forge_conditional_support import _fixture as ff_fixture, _h as ff_h
from rawlsing_next.tests.test_gt12_closure_b_c_to_d_bridge import _fixture as closure_fixture

HERE = Path(__file__).resolve().parent
OUT = HERE / "independent_probe.json"


def expect_error(label, fn):
    try:
        value = fn()
    except Exception as exc:  # expected for negatives
        return {"label": label, "refused": True, "error_type": type(exc).__name__, "error": str(exc)[:600], "returned": None}
    return {"label": label, "refused": False, "error_type": None, "error": None, "returned": type(value).__name__}


def main() -> int:
    results = {}
    q86b = question_ref("Q86B")
    q86a = question_ref("Q86A")
    results["q86_refs"] = {"conditioner": q86b.as_dict(), "target": q86a.as_dict()}

    # Retained valid Q86 sourcefree transport -> exact frozen relation/count profile.
    retained_query, retained_fact = load_current_gt2_query_fact_from_committed_transport()
    retained_relation = produce_exact_conditional_support_profile(
        joint_fact=retained_fact,
        joint_query=retained_query,
        conditioner_ref=retained_query.target_refs[0],
        target_ref=retained_query.target_refs[1],
        producer_permission_ceiling=(GT2_TARGET_USE,),
        relation_permission_ceiling=(GT2_TARGET_USE,),
    )
    retained_admission = admit_gt12_c_relation(retained_relation)
    retained_count_hash = semantic_hash(retained_relation.conditional_count_profile)
    results["retained"] = {
        "typed_state": retained_relation.typed_state,
        "conditioner_ref": retained_relation.conditioner_ref.as_dict(),
        "target_ref": retained_relation.target_ref.as_dict(),
        "relation_ref": retained_relation.ref.as_dict(),
        "count_profile_hash": retained_count_hash,
        "condition_rows": len(retained_relation.conditional_count_profile),
        "admission_decision": retained_admission.admission.decision.value,
        "admission_reason": retained_admission.admission.reason_code,
        "target_use_permissions": list(retained_admission.admission.target_use_permissions),
        "matches_declared_relation_hash": retained_relation.ref.content_hash == "1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19",
        "matches_declared_count_hash": retained_count_hash == "49bf14eb4a2b7fbf8e79ea4c72d10f4027819381564f582242ef6e24fc14fb59",
    }

    # Identity negatives: must refuse before profile minting.
    q99b = ExactRef("QUESTION_IMPLEMENTATION", "question_impl.phase0.99999999999999999999", ff_h("q99b"))
    q99a = ExactRef("QUESTION_IMPLEMENTATION", "question_impl.phase0.88888888888888888888", ff_h("q99a"))
    q99_query, q99_fact, q99_c, q99_t = ff_fixture(conditioner_ref=q99b, target_ref=q99a)
    results["unlike_q99_pair"] = expect_error(
        "unlike_q99_pair",
        lambda: produce_exact_conditional_support_profile(
            joint_fact=q99_fact, joint_query=q99_query, conditioner_ref=q99_c, target_ref=q99_t,
            producer_permission_ceiling=("FIELD_FORGE_RELATION_PRODUCTION",),
        ),
    )

    wrong_kind = ExactRef("QUESTION", q86b.object_id, q86b.content_hash)
    kind_query, kind_fact, kind_c, kind_t = ff_fixture(conditioner_ref=wrong_kind, target_ref=q86a)
    results["forged_wrong_kind"] = expect_error(
        "forged_wrong_kind",
        lambda: produce_exact_conditional_support_profile(
            joint_fact=kind_fact, joint_query=kind_query, conditioner_ref=kind_c, target_ref=kind_t,
            producer_permission_ceiling=("FIELD_FORGE_RELATION_PRODUCTION",),
        ),
    )

    wrong_hash = ExactRef("QUESTION_IMPLEMENTATION", q86a.object_id, ff_h("wrong-q86a-identity"))
    hash_query, hash_fact, hash_c, hash_t = ff_fixture(conditioner_ref=q86b, target_ref=wrong_hash)
    results["forged_wrong_hash"] = expect_error(
        "forged_wrong_hash",
        lambda: produce_exact_conditional_support_profile(
            joint_fact=hash_fact, joint_query=hash_query, conditioner_ref=hash_c, target_ref=hash_t,
            producer_permission_ceiling=("FIELD_FORGE_RELATION_PRODUCTION",),
        ),
    )

    swap_query, swap_fact, swap_c, swap_t = ff_fixture(reverse_targets=True)
    results["swapped_roles"] = expect_error(
        "swapped_roles",
        lambda: produce_exact_conditional_support_profile(
            joint_fact=swap_fact, joint_query=swap_query, conditioner_ref=swap_c, target_ref=swap_t,
            producer_permission_ceiling=("FIELD_FORGE_RELATION_PRODUCTION",),
        ),
    )

    # Downstream closure negatives: none may produce positive/ADMITTED relation.
    wrong_risk = ExactRef("RISK_SET", "WRONG_RISK", ff_h("wrong-risk"))
    wrong_risk_relation, _ = closure_fixture(risk_ref=wrong_risk)
    results["wrong_risk"] = expect_error("wrong_risk", lambda: admit_gt12_c_relation(wrong_risk_relation))

    narrow_relation, _ = closure_fixture(relation_permissions=("FIELD_FORGE_RELATION_PRODUCTION",))
    narrow_admission = admit_gt12_c_relation(narrow_relation)
    results["wrong_permission"] = {
        "decision": narrow_admission.admission.decision.value,
        "reason_code": narrow_admission.admission.reason_code,
        "target_use_permissions": list(narrow_admission.admission.target_use_permissions),
    }

    zero_relation, _ = closure_fixture(fact_state="OBSERVED_ZERO")
    zero_admission = admit_gt12_c_relation(zero_relation)
    results["nonpositive_observed_zero"] = {
        "relation_typed_state": zero_relation.typed_state,
        "decision": zero_admission.admission.decision.value,
        "reason_code": zero_admission.admission.reason_code,
        "target_use_permissions": list(zero_admission.admission.target_use_permissions),
    }

    baseline_relation, _ = closure_fixture()
    evidence = bridge_gt12_c_relation_to_d_evidence(baseline_relation)
    rule = make_gt12_c_to_d_admission_rule(baseline_relation)
    source_receipts = []
    for label, mutated in (
        ("wrong_source_family", replace(evidence, source_family="OtherSource")),
        ("wrong_source_wave", replace(evidence, source_wave="R4")),
        ("wrong_source_artifact", replace(evidence, source_artifact_ref=ExactRef("SOURCE_ARTIFACT", "wrong", ff_h("wrong-source")))),
    ):
        receipt = evaluate_gt2_relation_admission(RelationAdmissionRequest(mutated), rule)
        source_receipts.append({
            "label": label,
            "decision": receipt.decision.value,
            "reason_code": receipt.reason_code,
            "target_use_permissions": list(receipt.target_use_permissions),
        })
    results["source_family_wave_artifact"] = source_receipts

    restored_relation, _ = closure_fixture()
    results["cold_restore"] = {
        "relation_ref": restored_relation.ref.as_dict(),
        "matches_baseline": restored_relation.ref == baseline_relation.ref,
        "admission_decision": admit_gt12_c_relation(restored_relation).admission.decision.value,
    }

    # Compact expected-outcome assertions for the independent review.
    assert results["retained"]["typed_state"] == "SUPPORTED"
    assert results["retained"]["condition_rows"] == 6
    assert results["retained"]["admission_decision"] == "ADMITTED"
    assert results["unlike_q99_pair"]["refused"] is True
    assert results["forged_wrong_kind"]["refused"] is True
    assert results["forged_wrong_hash"]["refused"] is True
    assert results["swapped_roles"]["refused"] is True
    assert results["wrong_risk"]["refused"] is True
    assert results["wrong_permission"]["decision"] == "DENIED"
    assert results["wrong_permission"]["target_use_permissions"] == []
    assert results["nonpositive_observed_zero"]["decision"] == "UNRESOLVED"
    assert results["nonpositive_observed_zero"]["target_use_permissions"] == []
    assert results["source_family_wave_artifact"][0]["decision"] == "OUT_OF_SCOPE"
    assert results["source_family_wave_artifact"][1]["decision"] == "OUT_OF_SCOPE"
    assert results["source_family_wave_artifact"][2]["decision"] == "INTEGRITY_FAILURE"
    assert results["cold_restore"]["matches_baseline"] is True
    assert results["cold_restore"]["admission_decision"] == "ADMITTED"

    OUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
