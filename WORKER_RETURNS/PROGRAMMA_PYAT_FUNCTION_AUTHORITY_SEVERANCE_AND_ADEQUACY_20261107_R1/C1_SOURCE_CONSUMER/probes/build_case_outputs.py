#!/usr/bin/env python3
"""Build the C1 single-case return and anti-join from immutable existing registers."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer")
OUT = ROOT / "WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C1_SOURCE_CONSUMER"
REG = "WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1"
PINS = {
    "protected": "7a5429ffbc48efd25e28c912da80c822e66bc182",
    "startup": "03d054f1c693524e781767d96a287ca9e937e3ff",
    "f1": "c3fe75371136c5e7c9eba83ac5ffa66c3f4922ae",
    "r2_748": "9307ffafa5bec45e5f4800e555b2b30ce5b467ff",
    "b5": "33fb9159be9b83ca2577ea004ffb71cfc7862b1e",
    "r4": "0c5b385d858033306c6221bcd344b2f69616ff29",
}
CASE_ID = "C1-Q86-R5-RAW-001"


def git_show(ref: str, path: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{ref}:{path}"], capture_output=True, check=True).stdout.decode()


def read_tsv_git(ref: str, path: str):
    return list(csv.DictReader(git_show(ref, path).splitlines(), delimiter="\t"))


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(value, limit=500):
    text = str(value if value is not None else "").replace("\t", " ").replace("\r", " ").replace("\n", " ").strip()
    return text[:limit]


q86 = json.loads((OUT / "probes/q86_source_semantics_probe.json").read_text())
neg = json.loads((OUT / "probes/q86_negative_probe.json").read_text())
t01 = json.loads((OUT / "probes/r7_t01_trace.json").read_text())

# Register anti-join sources: preserve every ID and do not use this sample as a
# universal completeness claim.
registers = []
b5 = read_tsv_git(PINS["b5"], "WORKER_RETURNS/PROGRAMMA-PYAT-WHOLE-PIPELINE-AUTHORITY-AUDIT-20261107-R1/B5_AUTHORITY_DOCUMENT_INVOCATION_GAPS/03_CURRENT_OPERATION_TO_AUTHORITY_REQUIRED_SELECTED_INVOKED_ENFORCED.tsv")
for r in b5:
    registers.append(("B5_CURRENT_OPERATIONS", PINS["b5"], "WORKER_RETURNS/PROGRAMMA-PYAT-WHOLE-PIPELINE-AUTHORITY-AUDIT-20261107-R1/B5_AUTHORITY_DOCUMENT_INVOCATION_GAPS/03_CURRENT_OPERATION_TO_AUTHORITY_REQUIRED_SELECTED_INVOKED_ENFORCED.tsv", r["operation_id"], r["real_current_operation"]))
f1 = [json.loads(x) for x in git_show(PINS["f1"], "WORKER_RETURNS/PROGRAMMA_PYAT_HQ_ACCESSION_20261107_R1/05_ALL_29_HISTORICAL_FUNCTION_TO_CURRENT_OWNER_CANDIDATES.jsonl").splitlines() if x.strip()]
for r in f1:
    registers.append(("F1_29_HISTORICAL_FUNCTIONS", PINS["f1"], "WORKER_RETURNS/PROGRAMMA_PYAT_HQ_ACCESSION_20261107_R1/05_ALL_29_HISTORICAL_FUNCTION_TO_CURRENT_OWNER_CANDIDATES.jsonl", r["stable_function_id"], r["historic_function"]))
r2 = read_tsv_git(PINS["r2_748"], "WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/MAINMAC_COMPOUND_RECLOSURE/R2_QUALIFIED_FUNCTION_RESOURCE_JOIN/02_QUALIFIED_FUNCTION_JOIN.tsv")
for r in r2:
    registers.append(("748_30_RESPONSIBILITIES", PINS["r2_748"], "WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/MAINMAC_COMPOUND_RECLOSURE/R2_QUALIFIED_FUNCTION_RESOURCE_JOIN/02_QUALIFIED_FUNCTION_JOIN.tsv", r["FUNCTION_ID"], r["FUNCTION_NAME"]))
for fname, register in [
    ("FIELD_FORGE_R2_FUNCTION_ASSET_REGISTER_20261104_R1.jsonl", "FFR2_FUNCTION_ASSET_26"),
    ("FIELD_FORGE_R2_DEPENDENCY_COURT_20261104_R1.jsonl", "FFR2_DEPENDENCY_16"),
    ("POST_FF_R2_SOURCE_MECHANISM_RECEIVING_20261104_R1.jsonl", "POSTFF_SOURCE_MECHANISM_15"),
    ("POST_FF_R2_SEAM_STARVATION_MATRIX_20261104_R1.jsonl", "POSTFF_SEAM_11"),
]:
    rows = read_jsonl(ROOT / "PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP" / fname)
    for r in rows:
        rid = r.get("stable_id") or r.get("id")
        title = r.get("title") or r.get("requirement_and_human_purpose") or r.get("demand") or r.get("anchor") or ""
        registers.append((register, PINS["protected"], str(Path("PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP") / fname), rid, title))
ar = read_tsv_git(PINS["r4"], "WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/MAINMAC_COMPOUND_RECLOSURE/R4_HISTORICAL_VERSION/01_ALL_58_HISTORICAL_RELEASE_LEDGER.tsv")
for r in ar:
    registers.append(("R4_HISTORICAL_RELEASES_58", PINS["r4"], "WORKER_RETURNS/PROGRAMMA-PYAT-AUTHORITY-RECLOSURE-20261106-R1/MAINMAC_COMPOUND_RECLOSURE/R4_HISTORICAL_VERSION/01_ALL_58_HISTORICAL_RELEASE_LEDGER.tsv", r["asset_release_id"], r["historical_operation_grain"]))

primary_matches = {
    ("B5_CURRENT_OPERATIONS", "O02"): "UPSTREAM_C11_PROJECTOR_OPERATION",
    ("B5_CURRENT_OPERATIONS", "O04"): "CONTEXT_RESPONSE_SEMANTIC_BINDING_OPERATION",
    ("B5_CURRENT_OPERATIONS", "O08"): "UPSTREAM_I03_QUERY_OPERATION",
    ("B5_CURRENT_OPERATIONS", "O17"): "PRIMARY_FF_Q86_CONDITIONAL_OPERATION",
    ("F1_29_HISTORICAL_FUNCTIONS", "F05_RESP_OPTION"): "LEGACY_RESPONSE_OPTION_FUNCTION",
    ("F1_29_HISTORICAL_FUNCTIONS", "F06_RESP_CONTRACT"): "LEGACY_RESPONSE_CONTRACT_FUNCTION",
    ("748_30_RESPONSIBILITIES", "F05_RESP_OPTION"): "LEGACY_RESPONSE_OPTION_FUNCTION",
    ("748_30_RESPONSIBILITIES", "F06_RESP_CONTRACT"): "LEGACY_RESPONSE_CONTRACT_FUNCTION",
    ("FFR2_FUNCTION_ASSET_26", "FFR1:A12"): "FROZEN_Q86_GT2_SPECIALIZED_PRODUCER",
    ("FFR2_FUNCTION_ASSET_26", "FFR1:A13"): "GT12_C_TO_D_TYPED_BRIDGE",
    ("FFR2_FUNCTION_ASSET_26", "FFR1:A16"): "GENERIC_I03_N_TARGET_QUERY",
    ("FFR2_FUNCTION_ASSET_26", "FFR1:A25"): "Q86_SELECTED_TREE_IDENTITY_CENSUS",
    ("FFR2_DEPENDENCY_16", "FFR1:E07"): "Q86_I03_JOINT_TO_FF_GT12_DEPENDENCY",
    ("FFR2_DEPENDENCY_16", "FFR1:E08"): "Q86_PRODUCER_OUTSIDE_CANARY_CONTAMINATION",
    ("POSTFF_SOURCE_MECHANISM_15", "PSR1:P04"): "Q86B_CONDITIONER_Q86A_TARGET_PROFILE",
    ("POSTFF_SOURCE_MECHANISM_15", "PSR1:P05"): "SOURCE_SPECIFIC_CANARY_SEPARATION",
    ("R4_HISTORICAL_RELEASES_58", "AR-0033"): "SELECTED_AFROBAROMETER_RESPONSE_OPTION_AUTHORITY",
}
anti_rows = []
matched = 0
for register, cut, path, rid, title in registers:
    role = primary_matches.get((register, str(rid)))
    if role:
        matched += 1
        match = "MATCHED"
        disposition = "PRESERVED_AND_JOINED_TO_CASE"
    else:
        match = "UNMATCHED"
        disposition = "PRESERVED_UNMATCHED__NO_SAMPLE_COMPLETENESS_CLAIM"
    anti_rows.append({
        "REGISTER": register,
        "REGISTER_SOURCE_CUT": cut,
        "REGISTER_PATH": path,
        "REGISTER_ROW_ID": rid,
        "TITLE": clean(title, 240),
        "CASE_ID": CASE_ID,
        "MATCH": match,
        "MATCH_ROLE": role or "",
        "DISPOSITION": disposition,
        "NOTE": "rows are anti-joined by stable ID; sample case does not claim whole-register completeness",
    })

# Case fields. A-J are deliberately separable prose fields; forward/reverse
# columns preserve the actual selected row and current first reader.
case = {
    "CASE_ID": CASE_ID,
    "VERDICT": "FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED",
    "CASE_SCOPE": "One bounded R5 Q86 current operation: GT1 raw unary Q86A and GT2 raw joint Q86B->Q86A I03 canary, plus the existing FF conditional-support consumer; no structural/actor/science promotion.",
    "STABLE_LEGACY_FUNCTION_IDS": "F05_RESP_OPTION;F06_RESP_CONTRACT",
    "CURRENT_OPERATION_IDS": "B5:O17;B5:O08;B5:O02;GT1_R5_Q86A_RAW_UNARY_EXACT_RISK_SET@1;GT2_R5_Q86A_X_Q86B_RAW_JOINT_EXACT_RISK_SET@1",
    "REGISTER_IDS": "B5:O02;O04;O08;O17;F1:F05;F06;748:F05;F06;FFR2:A12;A13;A16;A25;E07;E08;PSR1:P04;P05;AR-0033",
    "MATCHED_REGISTER_IDS": ";".join(f"{k[0]}:{k[1]}" for k in primary_matches),
    "UNMATCHED_REGISTER_COUNT": len(registers) - matched,
    "UNMATCHED_REGISTER_IDS": f"SEE_05_REGISTER_ANTIJOIN__{len(registers) - matched}_PRESERVED_UNMATCHED",
    "A_HISTORICAL_SELECTED_DOCUMENT_VERSION_ROW_OPERATION_SCOPE_NEGATIVE": (
        "AR-0033 selected Afrobarometer response-option authority: 15,498,257 bytes, sha256 305cb215485bc95ebecee395e578c52739311bc2fc15faed27318bd922f47332; "
        "Afrobarometer R5 Q86A and Q86B, 6 rows each (0/1 substantive; special codes retained); handling_rule=context_only; recommended_computation=none; "
        "response_family=context_only; question_type=ordinal_context; source_structure_classification=demographic_material_or_identity_context; "
        "Q86A contract 198f189adafd2f4b9e459184a897c8257fa4631f5f940686cd77736cccd38082; Q86B contract 01ceeb78b8b4788c0732afeaab07374140b974fc1e330f79eb9f948e4c1eaa13; "
        "issuer grade A02_RECORDED_HISTORICAL_DECISION_NOT_ORIGINAL_SIGNER; no current release proved. Negative: no certified polarity/direction/weight, no signed-atom or structural promotion; 6-row source-option sets per variable."
    ),
    "B_MODERN_OWNER_AND_FIRST_CONSUMER_PROOF_SHA": (
        "Owner rawlsing_next/wave1_gt12_i03_positive_facts.py sha256 ab14f87d25a05c8b3463fceb47763d977aea6470798422ec3058f73a71ad5635; "
        "I03 first semantic reader build_gt1_q86a_i03_plan/build_gt2_q86a_q86b_i03_plan at :646/:670 -> execute_empirical_query pre553_empirical_query.py:685; "
        "C11 projector pre553_source_backed_c11_facade.py:502-553; downstream FF consumer field_forge_conditional_support.py:467-529. "
        "Proof: 8/8 Q86 tests and 97/97 inherited focused suite at startup 03d054f1; source SHA c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651; frozen risk set 19,210."
    ),
    "C_CURRENT_POSITIVE_TRACE_ACTUAL_SELECTED_AUTHORITY": (
        "C11 source SHA, QIMPL IDs, current source-structure IDs, common risk count, query authority and target-use authority are enforced. "
        "The actual AR-0033 Q86 response-contract hashes 198f.../01cee... are NOT referenced anywhere in current rawlsing_next; Q86 target response_semantic_authority_refs are caller-supplied. "
        "The positive tests use a synthetic SOURCE_SEMANTICS_TOPOLOGY fixture, not the selected Q86 row. Thus the chain is source SHA -> generic C11/I03; the selected response semantic authority does not cross the boundary."
    ),
    "D_ALTERNATIVE_AUTHORITY_REPRESENTATION_AND_ISSUER": (
        "SOURCEFREE_COMPARE_ONLY: a synthetic generic SOURCE_SEMANTICS_TOPOLOGY snapshot can carry I03, but it is not an issuer-attested Q86 semantic equivalent. "
        "The actual selected AR-0033 rows are context_only/recommended none and may permit raw context counting only if the source semantic owner says so. No competent current issuer or accepted equivalent proves that."
    ),
    "E_EXACT_FIRST_BREAK": (
        "Source/projector handoff: pre553_source_backed_c11_facade.py:502-553 and pre553_c11_ingest.py:644-659 never bind AR-0033 Q86 contract hashes to QuestionVariableBinding/target semantics. "
        "I03 later checks only ref presence at _pre553_query_eval.py:184-190. The Q86 operation pins source SHA/QIMPL/source structure but not the selected response semantics. Not a missing-asset-directory claim."
    ),
    "F_ACTUAL_FUNCTION_EFFECT_AND_EMPIRICAL_GRAIN": (
        "The current operation runs and emits a SUPPORTED RAW EmpiricalFact in the sourcefree fixture (GT1 3/3; GT2 3/3; production constants 19,210). "
        "Grain is SINGLE_UNIVERSE raw unary/joint counts, exact common risk set, no ratio, no signed direction, no weight/design, no structural admission, no actor/V3/V2 promotion. "
        "Function effect present; selected Q86 response authority effect not proven."
    ),
    "G_EQUIVALENCE_PROOF_AND_NEGATIVES": (
        "No equivalence. Positive proof is sourcefree only. Current Q86 negative controls all typed-refuse: wrong source SHA, wrong QIMPL, wrong source-structure/wave grain, wrong risk count, wrong target-use operation, widened permission ceiling; restoration PASS. "
        "R7 T01 separately shows wrong-kind/wrong-operation/wrong-scope generic C11 ALLOW can reach SUPPORTED 2/2 (inherited named falsifier rerun at current protected); that is not a Q86-specific historical-authority proof. "
        "Selected-version/shadow/withdrawal/cold-restore for actual Q86 row: NOT_RUN because no actual selected Q86 version fixture/issuer is supplied. UNPROVED, not equivalent."
    ),
    "H_CURRENT_STAGE": "Pre-Forge C11/I03 -> Field Forge Q86 conditional canary; no post-FF or actor stage.",
    "I_CURRENT_NATIVE_SOURCE_SCIENCE_AUTHORITY_GRADE": (
        "S0/S1 selected historical metadata + S2 sourcefree execution. No original issuer/native rights, no respondent/SAV/DB read, no scientific issuance, no C11/runtime patch."
    ),
    "J_LEAST_INVASIVE_OWNER_NEXT_MOVE": (
        "Source-semantic owner plus current C11/projector owner: state whether AR-0033 Q86 context_only rows authorize RAW unary/joint counting. If yes, bind the exact selected row/contract hashes (198f.../01cee...) to the existing QuestionVariableBinding/target semantics at pre553_source_backed_c11_facade.py:502-553; if no, retire the Q86 raw operation. "
        "Add exact positive plus wrong-version/source/wave and cold-restore tests; independent review; no new engine and no patch from this lease."
    ),
    "FORWARD_OLD_ROW_VERSION_SCOPE_EFFECT_NEGATIVE": (
        "AR-0033 selected bytes: Afrobarometer R5 Q86A/Q86B, Q86A row-set sha256 e3750a7d6f9431c53e222604d729e3aff0bab5fc6f06c230136bc5c768efaf22; Q86B row-set sha256 d16ff201d6d05777b2d41885e254caf669d025944982320f15e0969685562581. "
        "Historical governing meaning: response-option metadata context_only, no recommended computation, no polarity; special/nonresponse states remain distinct."
    ),
    "REVERSE_CURRENT_PRODUCER_SELECTOR_FIRST_CONSUMER_AUTHORITY_NEED": (
        "Current producer: C11/GovernedC11Projection -> pre553_source_backed_c11_facade.py:502-553. Selector: caller-supplied source/topology snapshots and Q86 binding; first consumer: I03 execute_empirical_query -> FF conditional support. "
        "Authority needed: selected Q86 response semantics/row/contract hash and a competent source semantic issuer decision; current actual authority absent. Equivalent: UNPROVED."
    ),
    "FIRST_BREAK": "AR-0033 selected Q86 response semantics -> C11 QuestionVariableBinding/target semantics; no exact binding edge.",
    "CURRENT_EFFECT": "Present sourcefree RAW Q86 unary/joint fact; no selected semantic provenance.",
    "GRAIN": "SINGLE_UNIVERSE; common exact risk set 19,210 in production constants; RAW counts; no ratio or structural/actor promotion.",
    "STAGE": "PRE_FORGE_C11_I03_TO_FIELD_FORGE_CANARY",
    "RIGHTS": "S0/S1 selected historical metadata; S2 sourcefree tests only; no native/original rights.",
    "PROOF": "97/97 inherited focused suite; 8/8 Q86 tests; 6/6 Q86 typed negatives + restoration PASS; R7 T01 wrong-kind/op/scope 2/2 SUPPORTED (named generic control).",
    "REFUSAL": "Wrong source SHA/QIMPL/source-structure/risk count/target-use/ceiling typed-refused; actual selected Q86 version test NOT_RUN.",
    "OWNER_ACTION": "Bind or retire AR-0033 Q86 response semantics at existing C11 producer; no new engine.",
    "EVIDENCE_PATHS": "probes/q86_source_semantics_probe.json; probes/q86_negative_probe.json; probes/r7_t01_trace.json; logs/97_suite.log; logs/q86_i03_tests.log; logs/r7_t01_runner.log",
}
assert case["VERDICT"] == "FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED"
assert matched >= 10
assert len(registers) == 212, len(registers)

# 01/02
(OUT / "01_CASES.jsonl").write_text(json.dumps(case, sort_keys=True) + "\n", encoding="utf-8")
tsv_cols = list(case.keys())
with (OUT / "02_CASES.tsv").open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=tsv_cols, delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerow({k: clean(v, 12000) for k, v in case.items()})

# 04 owner action: one exact action, no production patch authorized here.
actions = [{
    "ACTION_ID": "C1-Q86-ACT-001",
    "CASE_ID": CASE_ID,
    "VERDICT": case["VERDICT"],
    "OWNER": "Current C11/projector source-semantic owner; AR-0033 source semantical authority; FF Q86 owner advisory",
    "FIRST_MISSING_EDGE": "AR-0033 selected Q86 response semantics/contract hash -> C11 QuestionVariableBinding/target semantics",
    "ACTION": "Decide whether context_only Q86A/Q86B rows authorize RAW unary/joint counting. If yes, bind exact selected row/contract hashes to the existing C11 producer; if no, retire the Q86 raw operation.",
    "EXISTING_FILES": "pre553_source_backed_c11_facade.py:502-553; pre553_c11_ingest.py:644-659; wave1_gt12_i03_positive_facts.py:646-738; field_forge_conditional_support.py:467-529",
    "REQUIRED_TESTS": "Actual selected Q86 positive; wrong source/wave/operation/version; shadow/withdrawal; cold restore; preserve RAW vs weight/routing/status",
    "PRIORITY": "HIGH_AFTER_SOURCE_DECISION",
    "GATE": "Competent source semantic issuer decision + independent nonauthor review; no production patch from C1 lease",
    "NO_GO": "No new engine, no C11/runtime patch, no source copy, no native/science/actor claim",
}]
with (OUT / "04_MINIMAL_OWNER_ACTIONS.tsv").open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(actions[0]), delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(actions)

# 05 anti-join
anti_cols = ["REGISTER", "REGISTER_SOURCE_CUT", "REGISTER_PATH", "REGISTER_ROW_ID", "TITLE", "CASE_ID", "MATCH", "MATCH_ROLE", "DISPOSITION", "NOTE"]
with (OUT / "05_REGISTER_ANTIJOIN.tsv").open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=anti_cols, delimiter="\t", lineterminator="\n")
    w.writeheader()
    for row in anti_rows:
        w.writerow({k: clean(row.get(k, "")) for k in anti_cols})

print(json.dumps({
    "case_id": CASE_ID,
    "verdict": case["VERDICT"],
    "register_rows": len(registers),
    "matched": matched,
    "unmatched": len(registers) - matched,
    "sourcefree_positive": neg["baseline"],
    "negative_cases": len(neg["cases"]),
    "restoration_pass": neg["restoration_pass"],
    "t01_wrong_kind": t01["T01"]["variants"]["b_wrong_kind_allow"]["bad_reference_query"]["fact"]["typed_state"],
    "t01_raw_support": [t01["T01"]["variants"]["b_wrong_kind_allow"]["bad_reference_query"]["fact"]["raw_numerator_support"], t01["T01"]["variants"]["b_wrong_kind_allow"]["bad_reference_query"]["fact"]["raw_denominator_support"]],
}, indent=2, sort_keys=True))
