from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from rawlsing_next.gt12_c_to_d_relation_bridge import GT12CToDBridgeError, admit_gt12_c_relation, bridge_gt12_c_relation_to_d_evidence, make_gt12_c_to_d_admission_rule
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.wave1_ff_prev3_relation_admission import (
    AdmissionDecision,
    RelationAdmissionRequest,
    evaluate_gt2_relation_admission,
)
from rawlsing_next.field_forge_conditional_support import (
    FieldForgeConditionalSupportError,
    produce_exact_conditional_support_profile,
)
from rawlsing_next.tests.test_field_forge_conditional_support import _fixture as ff_fixture, _h as ff_h
from rawlsing_next.tests.test_gt12_closure_b_c_to_d_bridge import _fixture as closure_fixture, _h as closure_h
from rawlsing_next.wave1_r5_q86_c11_projection import question_ref

HERE = Path(__file__).resolve().parent
TRACE = HERE / "R8_PROOF_TRACE.json"


def relation_record(relation):
    return {
        "typed_state": relation.typed_state,
        "producer_state_blocking": relation.producer_state_blocking,
        "conditioner_ref": relation.conditioner_ref.as_dict(),
        "target_ref": relation.target_ref.as_dict(),
        "relation_ref": relation.ref.as_dict(),
        "count_profile_hash": semantic_hash(relation.conditional_count_profile),
        "producer_fact_ref": relation.producer_fact_ref.as_dict(),
        "producer_query_ref": relation.producer_query_ref.as_dict(),
        "risk_set_ref": relation.risk_set_ref.as_dict(),
        "producer_permission_ceiling": list(relation.producer_permission_ceiling),
        "relation_permission_ceiling": list(relation.relation_permission_ceiling),
        "roles": relation.semantic_projection()["roles"],
    }


def admission_record(result):
    return {
        "decision": result.admission.decision.value,
        "reason_code": result.admission.reason_code,
        "relation_ref": result.admission.relation_ref.as_dict(),
        "target_use_permissions": list(result.admission.target_use_permissions),
        "evidence_participants": [
            {"role": p.role, "native_variable": p.native_variable, "participant_ref": p.participant_ref.as_dict()}
            for p in result.evidence.participants
        ],
        "relation_typed_state": result.admission.relation_typed_state,
    }


def expect_error(name, fn):
    try:
        fn()
    except Exception as exc:
        return {"name": name, "refused": True, "error_type": type(exc).__name__, "error": str(exc)[:800]}
    return {"name": name, "refused": False, "error_type": None, "error": None}


def main():
    q86b = question_ref("Q86B")
    q86a = question_ref("Q86A")
    q99b = ExactRef("QUESTION_IMPLEMENTATION", "question_impl.phase0.99999999999999999999", ff_h("q99b"))
    q99a = ExactRef("QUESTION_IMPLEMENTATION", "question_impl.phase0.88888888888888888888", ff_h("q99a"))

    baseline_relation, _ = closure_fixture()
    baseline_admission = admit_gt12_c_relation(baseline_relation)

    q99_query, q99_fact, q99_c, q99_t = ff_fixture(conditioner_ref=q99b, target_ref=q99a)
    unlike = expect_error(
        "unlike_Q99B_Q99A",
        lambda: produce_exact_conditional_support_profile(
            joint_fact=q99_fact,
            joint_query=q99_query,
            conditioner_ref=q99_c,
            target_ref=q99_t,
            producer_permission_ceiling=("FIELD_FORGE_RELATION_PRODUCTION",),
        ),
    )

    wrong_kind = ExactRef("QUESTION", q86b.object_id, q86b.content_hash)
    qkind, fkind, ckind, tkind = ff_fixture(conditioner_ref=wrong_kind, target_ref=q86a)
    wrong_kind_result = expect_error(
        "forged_Q86_object_id_wrong_kind",
        lambda: produce_exact_conditional_support_profile(
            joint_fact=fkind,
            joint_query=qkind,
            conditioner_ref=ckind,
            target_ref=tkind,
            producer_permission_ceiling=("FIELD_FORGE_RELATION_PRODUCTION",),
        ),
    )

    wrong_hash = ExactRef("QUESTION_IMPLEMENTATION", q86a.object_id, ff_h("wrong-q86a-identity"))
    qhash, fhash, chash, thash = ff_fixture(conditioner_ref=q86b, target_ref=wrong_hash)
    wrong_hash_result = expect_error(
        "forged_Q86_wrong_identity_hash",
        lambda: produce_exact_conditional_support_profile(
            joint_fact=fhash,
            joint_query=qhash,
            conditioner_ref=chash,
            target_ref=thash,
            producer_permission_ceiling=("FIELD_FORGE_RELATION_PRODUCTION",),
        ),
    )

    qswap, fswap, cswap, tswap = ff_fixture(reverse_targets=True)
    swapped = expect_error(
        "swapped_Q86_roles",
        lambda: produce_exact_conditional_support_profile(
            joint_fact=fswap,
            joint_query=qswap,
            conditioner_ref=cswap,
            target_ref=tswap,
            producer_permission_ceiling=("FIELD_FORGE_RELATION_PRODUCTION",),
        ),
    )

    wrong_risk = ExactRef("RISK_SET", "WRONG_RISK", closure_h("wrong-risk"))
    wrong_risk_relation, _ = closure_fixture(risk_ref=wrong_risk)
    wrong_risk_result = expect_error("wrong_risk", lambda: admit_gt12_c_relation(wrong_risk_relation))

    narrow_relation, _ = closure_fixture(relation_permissions=("FIELD_FORGE_RELATION_PRODUCTION",))
    narrow_admission = admit_gt12_c_relation(narrow_relation)

    zero_relation, _ = closure_fixture(fact_state="OBSERVED_ZERO")
    zero_admission = admit_gt12_c_relation(zero_relation)

    evidence = bridge_gt12_c_relation_to_d_evidence(baseline_relation)
    rule = make_gt12_c_to_d_admission_rule(baseline_relation)
    source_family_receipts = []
    for label, mutated in (
        ("wrong_source_family", replace(evidence, source_family="OtherSource")),
        ("wrong_source_wave", replace(evidence, source_wave="R4")),
        ("wrong_source_artifact", replace(evidence, source_artifact_ref=ExactRef("SOURCE_ARTIFACT", "wrong", closure_h("wrong-source")))),
    ):
        receipt = evaluate_gt2_relation_admission(RelationAdmissionRequest(mutated), rule)
        source_family_receipts.append({
            "name": label,
            "decision": receipt.decision.value,
            "reason_code": receipt.reason_code,
            "target_use_permissions": list(receipt.target_use_permissions),
        })

    restored_relation, _ = closure_fixture()
    restored_admission = admit_gt12_c_relation(restored_relation)

    trace = {
        "baseline": {
            "relation": relation_record(baseline_relation),
            "admission": admission_record(baseline_admission),
        },
        "negatives": {
            "unlike_pair": unlike,
            "forged_wrong_kind": wrong_kind_result,
            "forged_wrong_hash": wrong_hash_result,
            "swapped_roles": swapped,
            "wrong_risk": wrong_risk_result,
            "wrong_permission": admission_record(narrow_admission),
            "nonpositive_observed_zero": admission_record(zero_admission),
            "source_wave_family_artifact": source_family_receipts,
        },
        "cold_restore": {
            "relation_ref": restored_relation.ref.as_dict(),
            "matches_baseline": restored_relation.ref == baseline_relation.ref,
            "admission": admission_record(restored_admission),
        },
    }
    TRACE.write_text(json.dumps(trace, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    print(json.dumps(trace, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
