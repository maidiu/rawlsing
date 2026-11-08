#!/usr/bin/env python3
"""Build C9 workload-authority cases, trace, dependencies and estate scope."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer")
BASE = "WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1"
OUT = ROOT / BASE / "C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER"
C5 = ROOT / BASE / "C5_SOURCE_ESTATE_PRODUCER_CONSUMER"
PROBE = json.loads((OUT / "probes/workload_probe.json").read_text())
BASE_CUT = "451f8d1e094800d523589cdd4db5159a338db836"
PROTECTED = "7a5429ffbc48efd25e28c912da80c822e66bc182"
P1_CANDIDATE = "d1278613e9e1a5d986ccce15782a697f19cbd722"
P1_BLOB = "c8352c5ab0fbc1a817c38d8ef99d64beef628230"

CASES = {
    "O08": "C9-O08-QUERY-TARGET-USE",
    "O12": "C9-O12-ISSUED-WORKLOAD",
    "O13": "C9-O13-BATCH-RECEIVING",
}
VERDICT = "FUNCTION_CURRENT_BUT_AUTHORITY_PROVENANCE_UNPROVED"


def clean(value, limit=12000):
    return str(value if value is not None else "").replace("\t", " ").replace("\r", " ").replace("\n", " ").strip()[:limit]


def write_tsv(name, cols, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({c: clean(row.get(c, "")) for c in cols})


def make_case(oid, scope, legacy):
    cid = CASES[oid]
    if oid == "O08":
        a = ("No original shared35 selected document/row is demanded by the observed sourcefree witness. "
             "Candidate AR-0005/0006 QSM relation metadata and AR-0047/48/49/50 question-use/overlay inputs are not selected; "
             "no original QUC target-use or source row/version is proved. Negative: sourcefree test-only query authority, no TARGET_USE_PERMISSION.")
        b = ("Existing non-test API path: pre553_universal_workload.compile_universal_workload:143 -> "
             "pre553_native_workload_binding.build_test_only_workload:299 -> execute_universal_workload:229 -> "
             "execute_test_only_workload:423 -> pre553_issued_workload.admit:219 -> execute_issued_workload:280 -> "
             "CarrierNeutralResearchExecutor.execute_i03:430 -> pre553_empirical_query.execute_empirical_query:685.")
        c = ("Actual sourcefree witness: 4 operations, 4 SUPPORTED RAW facts, no-drop 4/4; authority "
             "B49-TEST-ONLY-QUERY-AUTH; scope TEST_ONLY_SOURCEFREE; query risk type WHOLE_QUESTION_RISK_SET; "
             "target_use_permission_ids empty. The first reader consumed the sourcefree typed authority; no selected target-use authority crossed.")
        d = ("The current sourcefree test-only query authority plus C11/I03 is a legitimate sourcefree witness, "
             "but it is not an original/current QUC target-use issuer. No accepted equivalent or original selected authority is proved.")
        e = ("First break: no selected TARGET_USE_PERMISSION/current source+science issuer and no actual shared35 source_question/target-use selector. "
             "The current query authority is TEST_ONLY_SOURCEFREE; the producer has no selected original row. This is a provenance/issuer seam, not a missing I03 reader.")
        f = ("Sourcefree synthetic DTA witness: 4 SUPPORTED RAW facts with denominators 3/3, 3/3, 4/4, 2/2; "
             "no shared35 source/wave effect, no original respondent or science.")
        g = ("Positive 4/4 no-drop; wrong source SHA gives 0/4 executed and 4 failed; wrong host/purpose gives WorkloadAdmissionError SOURCE_HOST_PURPOSE_MISMATCH; "
             "restoration fact refs match. No selected original target-use test is possible from this fixture.")
        j = ("Name one actual selected shared35 source/wave/question and target use, or retain the sourcefree witness only. "
             "If selected, bind the exact current target-use permission at the existing query/authority owner; no new engine, no forced QUC packet.")
    elif oid == "O12":
        a = ("No original current decision record is present. The observed operation uses TEST_ONLY_SOURCEFREE source/scientific permission refs; "
             "original CURRENT_GRANTED/ORIGINAL_SOURCE_GRANTED, host/purpose issuer, source SHA and native wave identity are not selected. Negative: no original issuer.")

        b = ("Pre553_native_workload_binding.build_test_only_workload:299 emits NativeWorkload/IssuedWorkloadRecord; "
             "TestOnlyDecisionResolver returns the exact test-only record; pre553_issued_workload.admit:219 enforces scope/currentness/host/purpose/envelope/jobs; "
             "execute_issued_workload:280 calls the existing C11/I03/Batch path.")
        c = ("Observed record scope TEST_ONLY_SOURCEFREE and currentness CURRENT_GRANTED (test-only), not an original issuer grant. "
             "4/4 operations admitted/executed; 4 receipts and 4 facts returned; no source/native/science authority promoted.")
        d = ("Sourcefree test-only decision resolver is the only observed authority representation. No external current issuer record, original wave identity or native grant is present.")
        e = ("First break: test-only scope/currentness is not an original or selected current source/science decision. The existing gate is functioning; "
             "the missing input is an external competent issuer record for a selected operation, not a new admission engine.")
        f = ("4 sourcefree operations executed, 4 receipts/facts; RAW/whole-question risk; no original native source or science effect.")
        g = ("Wrong source SHA refused 0/4; wrong host/purpose typed refusal; restoration matches fact refs. Positive sourcefree witness only; no original grant test.")
        j = ("If a real selected operation exists, source/science owner supplies the exact current decision record; otherwise retain sourcefree witness. No forged grant, no production patch.")
    else:
        a = ("No original shared35 Batch input is present. The observed Batch units are the four sourcefree operations from the synthetic DTA fixture; "
             "no original source/wave release, P1 EpreOperation or shared35 frontier is selected. Negative: no original Batch provenance.")
        b = ("execute_issued_workload:280 builds BatchManifest/units; CarrierNeutralResearchExecutor.execute_i03:430 calls pre553_empirical_query.execute_empirical_query:685; "
             "Batch receipts and facts are returned. The existing current C11/I03/Batch owners are installed.")
        c = ("Actual sourcefree witness returns 4 receipts and 4 SUPPORTED facts with no-drop 4/4. The Batch/C11/I03 path is real; "
             "the authority is TEST_ONLY_SOURCEFREE and the input is a synthetic nonrespondent DTA, not a shared35 source.")
        d = ("Current Batch/C11/I03 is an installed current path. The missing alternative is an actual shared35 P1/R157 selector/frontier, not a new Batch engine.")
        e = ("First break: no P1 original35 constructor/frontier, no exact EpreOperation->catalog/request/Batch binding, and no selected shared35 operation. "
             "compile_governed_frontier:473 is unexercised; this is a receiving/selection seam, not a missing I03 or Batch function.")
        f = ("4 sourcefree receipts/facts from synthetic DTA; RAW, whole-question risk, 3/3,3/3,4/4,2/2 support; no original shared35 native effect.")
        g = ("Positive sourcefree 4/4; wrong source SHA 0/4; wrong host/purpose typed refusal; restoration exact. Actual shared35/P1 frontier NOT_RUN.")
        j = ("Inspect existing P1/R157 candidate constructor and provide the exact EpreOperation->NativePreimageBundle/Frontier selector at the current owner; "
             "do not rebuild the C11/I03/Batch path or claim shared35 demand without an actual selected input.")
    return {
        "CASE_ID": cid,
        "VERDICT": VERDICT,
        "CASE_SCOPE": scope,
        "STABLE_LEGACY_FUNCTION_IDS": legacy,
        "CURRENT_OPERATION_IDS": f"B5:{oid};C9_SOURCEFREE_WORKLOAD_WITNESS",
        "REGISTER_IDS": f"B5:{oid};" + ";".join("F1:" + x for x in legacy.split(";") if x) + ";C5:O01-O07;P1:" + P1_CANDIDATE,
        "A_HISTORICAL_SELECTED_DOCUMENT_VERSION_ROW_OPERATION_SCOPE_NEGATIVE": a,
        "B_MODERN_OWNER_AND_FIRST_CONSUMER_PROOF_SHA": b,
        "C_CURRENT_POSITIVE_TRACE_ACTUAL_SELECTED_AUTHORITY": c,
        "D_ALTERNATIVE_AUTHORITY_REPRESENTATION_AND_ISSUER": d,
        "E_EXACT_FIRST_BREAK": e,
        "F_ACTUAL_FUNCTION_EFFECT_AND_EMPIRICAL_GRAIN": f,
        "G_EQUIVALENCE_PROOF_AND_NEGATIVES": g,
        "H_CURRENT_STAGE": "PRE_FORGE_UNIVERSAL_WORKLOAD_TO_C11_I03_BATCH; no FF/post-FF/actor.",
        "I_CURRENT_NATIVE_SOURCE_SCIENCE_AUTHORITY_GRADE": "S0/S1 source/API records + S2 SOURCEFREE test-only witness; original native/science/actor NOT_RUN.",
        "J_LEAST_INVASIVE_OWNER_NEXT_MOVE": j,
        "FORWARD_OLD_ROW_VERSION_SCOPE_EFFECT_NEGATIVE": a,
        "REVERSE_CURRENT_PRODUCER_SELECTOR_FIRST_CONSUMER_AUTHORITY_NEED": b + " Authority need: " + d,
        "CURRENT_EFFECT": f,
        "GRAIN": "sourcefree RAW whole-question risk query; one target, whole-question risk set; no shared35 source/wave claim.",
        "STAGE": "PRE_FORGE_UNIVERSAL_WORKLOAD_TO_C11_I03_BATCH",
        "RIGHTS": "S0/S1 + S2 sourcefree test-only; no original source/respondent/native/actor rights.",
        "PROOF": "C9 probe: 4 operations, 4 SUPPORTED facts, 4 receipts, no-drop 4/4; wrong source 0/4; wrong host/purpose typed refusal; restoration exact.",
        "REFUSAL": "Wrong source SHA and wrong host/purpose refused; actual shared35/P1 frontier NOT_RUN.",
        "OWNER_ACTION": j,
        "EVIDENCE_PATHS": "probes/workload_probe.py; probes/workload_probe.json; logs/workload_probe.log; C5 06_ALL35_SOURCE_DISPOSITIONS.tsv",
    }


cases = [
    make_case("O08", "O08 query/target-use selection in the existing universal workload API; sourcefree nonrespondent witness only.", "F03_QREL;F08_Q_USE"),
    make_case("O12", "O12 issued-workload authority/admission in the existing universal workload API; sourcefree test-only record.", "F28_EXEC_GRANT"),
    make_case("O13", "O13 Batch/C11/I03 receiving for the shared workload plan; sourcefree witness only, actual shared35 input unproved.", "F18_J_PREPARED;F26_CACHE"),
]
(OUT / "01_CASES.jsonl").write_text("\n".join(json.dumps(c, sort_keys=True) for c in cases) + "\n", encoding="utf-8")
write_tsv("02_CASES.tsv", list(cases[0].keys()), cases)

trace = [
    {"TRACE_ID":"C9-T01","CASE_ID":CASES["O08"],"STAGE_ORDER":"1","PRODUCER_SELECTOR":"pre553_universal_workload.compile_universal_workload:143","SOURCE_REQUEST_OR_SCOPE":"NativePreimageBundle from synthetic nonrespondent DTA; 4 administered operations","AUTHORITY_SELECTED":"B49-TEST-ONLY-QUERY-AUTH; TEST_ONLY_SOURCEFREE; target_use_permission_ids empty","FIRST_READER":"execute_universal_workload:229 -> execute_test_only_workload:423","OBSERVED_RESULT":"4 compiled / 4 executed; 4 SUPPORTED RAW facts; no-drop 4/4","SCOPE_LIMIT":"SOURCEFREE_TEST_ONLY__NOT_SHARED35","EVIDENCE":"probes/workload_probe.json","STATUS":"OBSERVED"},
    {"TRACE_ID":"C9-T02","CASE_ID":CASES["O08"],"STAGE_ORDER":"2","PRODUCER_SELECTOR":"build_projection_catalog / EmpiricalQuerySpec target+risk","SOURCE_REQUEST_OR_SCOPE":"one target; WHOLE_QUESTION_RISK_SET; RAW; UNCERTAINTY_UNQUANTIFIED","AUTHORITY_SELECTED":"B49-TEST-ONLY-QUERY-AUTH; no selected TARGET_USE_PERMISSION","FIRST_READER":"CarrierNeutralResearchExecutor.execute_i03:430 -> execute_empirical_query:685","OBSERVED_RESULT":"SUPPORTED facts 3/3,3/3,4/4,2/2","SCOPE_LIMIT":"NO_SELECTED_ORIGINAL_TARGET_USE__SOURCEFREE_ONLY","EVIDENCE":"probes/workload_probe.json","STATUS":"OBSERVED"},
    {"TRACE_ID":"C9-T03","CASE_ID":CASES["O12"],"STAGE_ORDER":"3","PRODUCER_SELECTOR":"TestOnlyDecisionResolver / pre553_issued_workload.admit:219","SOURCE_REQUEST_OR_SCOPE":"TEST_ONLY_SOURCEFREE record; synthetic DTA source; host/purpose C9","AUTHORITY_SELECTED":"TEST_ONLY_SOURCEFREE; CURRENT_GRANTED test-only; no ORIGINAL_SOURCE_GRANTED","FIRST_READER":"execute_issued_workload:280","OBSERVED_RESULT":"4 operations admitted; 4 receipts/facts","SCOPE_LIMIT":"NO_ORIGINAL/SOURCE-SCIENCE DECISION","EVIDENCE":"probes/workload_probe.json","STATUS":"OBSERVED"},
    {"TRACE_ID":"C9-T04","CASE_ID":CASES["O13"],"STAGE_ORDER":"4","PRODUCER_SELECTOR":"execute_issued_workload:280 / BatchManifest","SOURCE_REQUEST_OR_SCOPE":"4 QUERY units over sourcefree synthetic nonrespondent DTA","AUTHORITY_SELECTED":"TEST_ONLY_SOURCEFREE","FIRST_READER":"CarrierNeutralResearchExecutor.execute_i03:430 -> execute_empirical_query:685","OBSERVED_RESULT":"4 Batch receipts; 4 SUPPORTED facts; no-drop 4/4","SCOPE_LIMIT":"NO_SHARED35_P1_INPUT","EVIDENCE":"probes/workload_probe.json","STATUS":"OBSERVED"},
    {"TRACE_ID":"C9-T05","CASE_ID":CASES["O13"],"STAGE_ORDER":"5","PRODUCER_SELECTOR":"P1 original35 constructor candidate d127... / pre553_universal_workload.compile_governed_frontier:473","SOURCE_REQUEST_OR_SCOPE":"caller-frozen ScientificFrontier + NativePreimageBundle; no P1 EpreOperation selector observed","AUTHORITY_SELECTED":"NOT_RUN; no selected shared35 frontier/issuer","FIRST_READER":"NOT_RUN; no exact EpreOperation->catalog/request/Batch binding","OBSERVED_RESULT":"NOT_RUN","SCOPE_LIMIT":"P1 candidate blob d127/c835... absent in inherited object store; no shared35 P1 input; do not rebuild","EVIDENCE":"P1 contract/roadmap records; no source read","STATUS":"NOT_RUN"},
]
write_tsv("02_PRODUCER_SELECTOR_CONSUMER_TRACE.tsv", list(trace[0]), trace)

actions = [
    {"ACTION_ID":"C9-A01","CASE_ID":CASES["O08"],"VERDICT":VERDICT,"OWNER":"Current C11/I03 query/target-use owner + source semantic owner","FIRST_BREAK":"No selected TARGET_USE_PERMISSION/current shared35 target-use authority; test-only query authority only","ACTION":"Name one actual selected shared35 source/wave/question/target use, or keep the sourcefree library witness. If selected, bind exact current target-use permission at existing owner; no new engine/QUC packet.","ABI":"EmpiricalQuerySpec.target_use_ref / TARGET_USE_PERMISSION; B49-TEST-ONLY-QUERY-AUTH is test-only","DEPENDENCY":"C9-D01","GATE":"No original issuer invented; no production patch from C9"},
    {"ACTION_ID":"C9-A02","CASE_ID":CASES["O12"],"VERDICT":VERDICT,"OWNER":"Current source/science decision issuer; pre553_issued_workload owner","FIRST_BREAK":"Test-only sourcefree scope; no original CURRENT_GRANTED/ORIGINAL_SOURCE_GRANTED record","ACTION":"If a real selected operation exists, supply exact external current decision record; otherwise retain sourcefree witness. No forged grant or new admission gate.","ABI":"NativeWorkload/IssuedWorkloadRecord; source/science permission refs; host/purpose/source SHA","DEPENDENCY":"C9-D02","GATE":"External competent issuer only"},
    {"ACTION_ID":"C9-A03","CASE_ID":CASES["O13"],"VERDICT":VERDICT,"OWNER":"P1/R157 selector owner + current C11/I03/Batch owner","FIRST_BREAK":"No actual shared35 P1 EpreOperation->NativePreimageBundle/Frontier selector; compile_governed_frontier NOT_RUN","ACTION":"Inspect existing P1 candidate constructor and produce exact selector/receiving seam at true owner; do not rebuild C11/I03/Batch or claim shared35 demand without input.","ABI":"EpreOperation/NativePreimageBundle -> compile_universal_workload:143 / compile_governed_frontier:473","DEPENDENCY":"C9-D03/C9-D04","GATE":"No new engine; no original native/science claim"},
]
write_tsv("04_MINIMAL_OWNER_ACTIONS.tsv", list(actions[0]), actions)

deps = [
    {"DEPENDENCY_ID":"C9-D01","CASE_ID":CASES["O08"],"OWNER":"Current C11/I03 query-target-use owner + source semantic owner","MISSING_ABI_OR_PROVENANCE":"selected TARGET_USE_PERMISSION/current target-use row; current B49-TEST-ONLY-QUERY-AUTH is test-only","SMALLEST_LEGITIMATE_OPERATION":"Name one actual shared35 source/wave/question/target use and bind exact current permission at existing query owner","STATUS":"UNPROVED"},
    {"DEPENDENCY_ID":"C9-D02","CASE_ID":CASES["O12"],"OWNER":"External source/science current issuer; pre553_issued_workload owner","MISSING_ABI_OR_PROVENANCE":"ORIGINAL_SOURCE_GRANTED/CURRENT_GRANTED decision record, source/science permission refs, original wave identity","SMALLEST_LEGITIMATE_OPERATION":"Supply an external current decision record for one selected operation; no new admission engine","STATUS":"BLOCKED_ISSUER"},
    {"DEPENDENCY_ID":"C9-D03","CASE_ID":CASES["O13"],"OWNER":"P1/R157 candidate selector owner + current C11/I03/Batch owner","MISSING_ABI_OR_PROVENANCE":"exact EpreOperation/Operation ID -> NativePreimageBundle/Frontier -> catalog/request/Batch envelope binding","SMALLEST_LEGITIMATE_OPERATION":"Inspect candidate P1 module; produce one exact shared35 selector/receiving seam without new engine","STATUS":"UNPROVED_NOT_REBUILD"},
    {"DEPENDENCY_ID":"C9-D04","CASE_ID":CASES["O13"],"OWNER":"P1 candidate source custodian","MISSING_ABI_OR_PROVENANCE":"P1 candidate d127 program; blob c835... absent in inherited object store; no current shared35 constructor/frontier","SMALLEST_LEGITIMATE_OPERATION":"Obtain exact candidate read-only or identify existing current successor; do not assume absence means missing function","STATUS":"PRECISE_UNKNOWN"},
]
write_tsv("04_INDISPENSABLE_DEPENDENCIES.tsv", list(deps[0]), deps)

with (C5 / "06_ALL35_SOURCE_DISPOSITIONS.tsv").open(encoding="utf-8") as fh:
    c5 = list(csv.DictReader(fh, delimiter="\t"))
estate = []
for r in c5:
    estate.append({
        "SOURCE_ID": r["SOURCE_ID"],
        "FAMILY": r["SOURCE_FAMILY"],
        "WAVE": r["WAVE"],
        "FORMAT": r["FORMAT"],
        "ORIGINAL_EXECUTION_STATUS": r["ORIGINAL_EXECUTION_STATUS"],
        "SHARED_PLANNER_COVERAGE": "NOT_RUN__NO_P1_SHARED35_WORKLOAD_INPUT",
        "C9_EVIDENCE": "SOURCEFREE_LIBRARY_WITNESS_ONLY__NOT_SHARED35",
        "C5_DISPOSITION": r["DISPOSITION"],
        "EXCEPTION_OR_OWNER": r["EXCEPTION_OR_OWNER"],
    })
write_tsv("05_DECLARED_ESTATE_SCOPE.tsv", list(estate[0]), estate)
print(json.dumps({"cases":len(cases),"trace":len(trace),"actions":len(actions),"deps":len(deps),"sources":len(estate),"verdict":VERDICT},indent=2,sort_keys=True))
