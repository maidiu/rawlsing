#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable

from rawlsing_next.f07_second_canary_prev3_admission import (
    SecondCanaryIntegrity,
    execute_current_second_canary,
    instantiate_second_canary_admission,
    load_current_governed_inputs,
    prepare_second_canary_m1,
)
from rawlsing_next.m1_admitted_field_forge_relation_v554_ingress import RelationPreparationState

EXPECTED = {
    "claim_id": "FFR2_R5_Q73A_Q86A_EXACT_JOINT_CONDITIONED_DIRECTIONAL_HETEROGENEITY_CANARY@1",
    "relation_identity_sha256": "1a3b1d28cecdb5b06c7b8ac927848249693324da733d1ee9649a94e50d4322ee",
    "authority_key_sha256": "33c6f8b2e33758ef91d57d3eb3fa8bab7c65dfb7a6498495fb08d5261dc3a5fd",
    "replay_key_sha256": "0615a8668d87c5641c8a7bba4b144011d297c653a5369d6db2bd979e824fd19d",
    "source_sha256": "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651",
    "risk_set_id": "FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1",
    "risk_set_rows": 19210,
    "risk_set_member_set_sha256": "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b",
    "roster_artifact_sha256": "1cc810979eb80d52d1e5efcd1a916e309be1b60e8d5cc4eed1575bce30f38814",
    "admission_hash": "05456f3d21ab3426af6a6c924843fecb8417c11620dce7213a36c8a819e8dd2c",
    "m1_replay_sha256": "5d6e26ef30210ad7766c95d660c99cb6b91e38ebc291dd025e154201fdeec25b",
    "basis_id": "urn:rawlsing:v554:basis:sha256:a34deb4ba5d52990b966ac67cb1e0e51ab76ba05fbfae4c3f8db996d26b1d81b",
    "f1_id": "urn:rawlsing:v554:f1:sha256:06f96892b9d7cad5a2d506345203b3634509d2492997326031a98b44d83973f8",
    "permission": "STRUCTURAL_MEDIATION_INPUT",
}
EXPECTED_TYPED = {
    "observed_joint_states": 812,
    "support_admitted": 441,
    "zero_denominator_abstentions": 371,
    "directional_persistence": 185,
    "directional_reversal": 130,
    "exact_zero_difference": 126,
}


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "rawlsing_next").is_dir():
            return p
    raise RuntimeError("repository root not found")


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def json_normalized(value: Any) -> Any:
    return json.loads(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    )


ROOT = repo_root()
F07_RETURN = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/HQ_THIRD_WAVE_FANIN_AND_FOURTH_WAVE_DISPATCH_R1/FOURTH_WAVE_WORKER_RETURNS/F07"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        value = json.load(fh)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not an object")
    return value


def expect_integrity_failure(mutator: Callable[[dict[str, dict[str, Any]]], None]) -> None:
    inputs = copy.deepcopy(load_current_governed_inputs())
    mutator(inputs)
    try:
        instantiate_second_canary_admission(inputs)
    except (SecondCanaryIntegrity, KeyError, TypeError, ValueError):
        return
    raise AssertionError("mutation did not fail closed")


def expect_receipt_integrity_failure(mutator: Callable[[dict[str, Any]], None]) -> None:
    inputs = load_current_governed_inputs()
    receipt = instantiate_second_canary_admission(inputs)
    changed = copy.deepcopy(receipt)
    mutator(changed)
    prep = prepare_second_canary_m1(changed, inputs)
    if prep.state is not RelationPreparationState.INTEGRITY_FAILURE:
        raise AssertionError(f"mutated receipt did not fail closed: {prep.state}")


results: list[dict[str, str]] = []


def run(case_id: str, description: str, fn: Callable[[], None]) -> None:
    try:
        fn()
    except Exception as exc:
        results.append({"id": case_id, "description": description, "status": "FAIL", "detail": f"{type(exc).__name__}: {exc}"})
        return
    results.append({"id": case_id, "description": description, "status": "PASS", "detail": "exact assertion satisfied"})


def p01() -> None:
    inputs = load_current_governed_inputs()
    authority = inputs["e10_authority"]
    ledger = inputs["e10_replay_ledger"]
    assert canonical_hash(authority["relation_identity_key"]) == EXPECTED["relation_identity_sha256"] == authority["relation_identity_sha256"]
    assert canonical_hash(authority["authority_key"]) == EXPECTED["authority_key_sha256"] == authority["authority_key_sha256"]
    assert canonical_hash(ledger["replay_key"]) == EXPECTED["replay_key_sha256"] == ledger["replay_key_sha256"]


def p02() -> None:
    relation = load_current_governed_inputs()["e10_authority"]["relation_identity_key"]
    assert relation["claim_id"] == EXPECTED["claim_id"]
    assert relation["source_sha256"] == EXPECTED["source_sha256"]
    assert relation["risk_set"] == {
        "id": EXPECTED["risk_set_id"],
        "rows": EXPECTED["risk_set_rows"],
        "member_set_sha256": EXPECTED["risk_set_member_set_sha256"],
    }
    assert [p["source_variable"] for p in relation["participants"]] == ["Q73A", "Q86A", "Q70B", "Q70C", "Q84"]
    assert [p["ordinal"] for p in relation["participants"]] == [0, 1, 2, 3, 4]


def p03() -> None:
    committed = load_json(F07_RETURN / "01_SECOND_CANARY_ADMISSION_RECEIPT.json")
    fresh = instantiate_second_canary_admission(load_current_governed_inputs())
    assert fresh == committed
    material = {k: v for k, v in committed.items() if k not in {"field_forge_relation_admission_id", "field_forge_relation_admission_content_hash"}}
    digest = canonical_hash(material)
    assert digest == EXPECTED["admission_hash"] == committed["field_forge_relation_admission_content_hash"]
    assert committed["field_forge_relation_admission_id"] == f"urn:rawlsing:prev3:f07:second-canary-admission:sha256:{digest}"


def p04() -> None:
    receipt = load_json(F07_RETURN / "01_SECOND_CANARY_ADMISSION_RECEIPT.json")
    typed = receipt["f07_instantiation"]["typed_state_summary"]
    assert typed == EXPECTED_TYPED
    assert typed["observed_joint_states"] == typed["support_admitted"] + typed["zero_denominator_abstentions"]
    assert typed["support_admitted"] == typed["directional_persistence"] + typed["directional_reversal"] + typed["exact_zero_difference"]
    roster = receipt["applicable_negative_denial_noncomparability_refs"][0]["full_roster_artifact"]
    assert roster["sha256"] == EXPECTED["roster_artifact_sha256"] and roster["observed_states"] == 812


def p05() -> None:
    receipt = load_json(F07_RETURN / "01_SECOND_CANARY_ADMISSION_RECEIPT.json")
    assert receipt["target_use_permission_refs"] == [f"permission:{EXPECTED['permission']}"]
    inst = receipt["f07_instantiation"]
    assert inst["permission_ceiling"] == [EXPECTED["permission"]]
    assert inst["gt2_rule_reuse"] == "DENIED"
    assert inst["m3_promotion"] == "DENIED"
    assert inst["person_state_promotion"] == "DENIED"
    assert inst["publication_authority"] == "NONE"


def p06() -> None:
    committed = load_json(F07_RETURN / "02_M1_V554_INGRESS_AND_REPLAY_RECEIPT.json")
    out = execute_current_second_canary()
    ev = out["m1_evaluation"]
    assert ev["decision_state"] == "ELIGIBLE"
    assert ev["canonical_basis_semantic_id"] == EXPECTED["basis_id"]
    assert ev["f1"]["f1_id"] == EXPECTED["f1_id"]
    assert ev["direct_v557_handoff"] is None
    assert out["m1_replay_sha256"] == EXPECTED["m1_replay_sha256"]
    assert committed["m1_evaluation"] == json_normalized(ev)
    assert committed["m1_replay_sha256"] == EXPECTED["m1_replay_sha256"]
    assert committed["same_input_replay"] == "EXACT_MATCH"


def p07() -> None:
    a = execute_current_second_canary()
    b = execute_current_second_canary()
    assert a == b
    assert canonical_hash(a["m1_evaluation"]) == EXPECTED["m1_replay_sha256"]


run("G07-P01", "independent E10 relation/authority/replay hash binding", p01)
run("G07-P02", "exact claim/source/risk/operand identity", p02)
run("G07-P03", "fresh admission equals committed receipt and independent content hash", p03)
run("G07-P04", "full typed-state roster and both partitions preserved", p04)
run("G07-P05", "singleton structural permission ceiling with broader promotions denied", p05)
run("G07-P06", "M1/V554 exact ELIGIBLE result and frozen basis/F1/replay identities", p06)
run("G07-P07", "same-input end-to-end replay deterministic", p07)

run("G07-N01", "authority current-status mutation fails closed", lambda: expect_integrity_failure(lambda x: x["e10_authority"].__setitem__("status", "STALE")))
run("G07-N02", "authority decision mutation fails closed", lambda: expect_integrity_failure(lambda x: x["e10_authority"]["authority_key"].__setitem__("decision_state", "DENY")))
run("G07-N03", "relation source identity mutation fails closed", lambda: expect_integrity_failure(lambda x: x["e10_authority"]["relation_identity_key"].__setitem__("source_sha256", "0" * 64)))
run("G07-N04", "risk-set member identity mutation fails closed", lambda: expect_integrity_failure(lambda x: x["e10_authority"]["relation_identity_key"]["risk_set"].__setitem__("member_set_sha256", "0" * 64)))
run("G07-N05", "claim identity mutation fails closed", lambda: expect_integrity_failure(lambda x: x["e10_authority"]["relation_identity_key"].__setitem__("claim_id", "OTHER_CLAIM")))
run("G07-N06", "operand coordinate mutation fails closed", lambda: expect_integrity_failure(lambda x: x["e10_authority"]["relation_identity_key"]["participants"][2].__setitem__("source_variable", "Q999")))
run("G07-N07", "typed roster support count mutation fails closed", lambda: expect_integrity_failure(lambda x: x["e10_replay_ledger"]["typed_state_preservation"].__setitem__("support_admitted", 440)))
run("G07-N08", "permission widening fails closed", lambda: expect_integrity_failure(lambda x: x["e10_authority"]["authority_key"]["allowed_permission_subset"].append("M3_HIGHER_ORDER_POSITIVE_PRODUCTION")))
run("G07-N09", "D09 evidence source provenance mutation fails closed", lambda: expect_integrity_failure(lambda x: x["d09_evidence_receipt"]["source"].__setitem__("sha256", "0" * 64)))
run("G07-N10", "replay provenance/full-roster artifact mutation fails closed", lambda: expect_integrity_failure(lambda x: x["e10_replay_ledger"]["replay_key"]["source_execution_artifacts"].__setitem__("03_JOINT_STATE_ROSTER_SUPPORT.tsv.gz", "0" * 64)))
run("G07-N11", "instantiated receipt relation identity mutation becomes integrity failure", lambda: expect_receipt_integrity_failure(lambda r: r["field_forge_relation_ref"].__setitem__("content_hash", "0" * 64)))
run("G07-N12", "instantiated receipt permission mutation becomes integrity failure", lambda: expect_receipt_integrity_failure(lambda r: r["target_use_permission_refs"].append("permission:M3_HIGHER_ORDER_POSITIVE_PRODUCTION")))
run("G07-N13", "instantiated receipt provenance mutation becomes integrity failure", lambda: expect_receipt_integrity_failure(lambda r: r["authority_current_selection_dependency_provenance_refs"].append("unbound:mutation")))

failed = [x for x in results if x["status"] != "PASS"]
out = {
    "schema_id": "PREV3_G07_SECOND_CANARY_INDEPENDENT_QUALIFICATION_RESULTS@1.0.0",
    "grain": "PREV3_SECOND_CANARY_ADMISSION_AND_M1_V554_INDEPENDENT_QUALIFICATION_R1_ONLY",
    "result": "PASS" if not failed else "FAIL",
    "case_count": len(results),
    "pass_count": len(results) - len(failed),
    "fail_count": len(failed),
    "expected_exact_identities": EXPECTED,
    "typed_state_summary": EXPECTED_TYPED,
    "partition_checks": {
        "812_eq_441_plus_371": True,
        "441_eq_185_plus_130_plus_126": True,
    },
    "cases": results,
}
text = json.dumps(out, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
print(text, end="")
results_path = os.environ.get("G07_RESULTS_PATH")
if results_path:
    Path(results_path).write_text(text, encoding="utf-8")
if failed:
    raise SystemExit(1)
