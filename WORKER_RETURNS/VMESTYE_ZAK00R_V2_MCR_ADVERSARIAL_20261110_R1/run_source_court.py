#!/usr/bin/env python3
"""ZAK00R source-pinned hostile MCR probe. Source-extracted/stubbed only; never native35."""
from __future__ import annotations

import ast
import copy
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from types import SimpleNamespace

BASE = Path(__file__).resolve().parents[2]
FLIGHTS = BASE / "WORKER_COMMISSIONS/VMESTYE_ZAKONCHILOS_ZAK00_V2_MCR/FLIGHT_LAUNCHES"
REPORTS = []
SOURCE_PINS = {
    "V549b": ("data/ddm_build_copy/build_question_response_attitude_cloud_summary_v549b.py", "bf874a95ea5172817b0d1bdf21b43600aac5cbfe"),
    "F03": ("data/ddm_build_copy/ddm_v550_question_relation_authority.py", "62084cbed10a5975f79bd504bf4fb99025e4e64e"),
    "F08": ("data/ddm_build_copy/ddm_v550_question_use.py", "8d90a5116fd05b5db17e9b4645638a3aa6fc1131"),
    "V552": ("data/ddm_build_copy/ddm_v552_structural.py", "0df56d70cb3880dee723df00aea2207acd525260"),
    "CURRENT_AUTH": ("rawlsing_next/pre553_empirical_authority.py", "ca65a7fd4d52f0c44447434559b1d09412e7aa39"),
    "CURRENT_QUERY": ("rawlsing_next/pre553_empirical_query.py", "b72b469e6646b88e4e2ed4dbbf0f3c209557fd69"),
}
SOURCES = {}
def assert_case(name, truth, evidence):
    if not truth:
        raise AssertionError(name + ": " + str(evidence))
    REPORTS.append({"id": name, "result": "PASS", "evidence": evidence})

def exact_func(src, name):
    tree = ast.parse(src)
    matches = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name]
    if len(matches) != 1:
        raise AssertionError("EXPECTED_EXACT_FUNCTION " + name)
    return matches[0]

def extracted_exec(fn, globals_dict):
    # Compiles actual immutable function AST, not a handwritten implementation.
    node = ast.Module(body=[
        ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0),
        copy.deepcopy(fn)
    ], type_ignores=[])
    exec(compile(ast.fix_missing_locations(node), "<EXACT_SOURCE_EXTRACT>", "exec"), globals_dict)
    return globals_dict[fn.name]

def read_and_pin():
    for key, (p, sha) in SOURCE_PINS.items():
        path = BASE / p
        actual = subprocess.check_output(["git", "hash-object", p], cwd=BASE, text=True).strip()
        assert_case("PIN_" + key, path.is_file() and actual == sha, {"path":p, "git_blob":actual, "expected":sha})
        SOURCES[key] = path.read_text(encoding="utf-8")
    # The author candidate and prompts must remain physically unchanged under review.
    all_files = [FLIGHTS / ("ZAK_%02d_FULL_COPY_PASTE_MCR.md" % i) for i in range(1, 12)]
    assert_case("ELEVEN_PRESENT", all(p.is_file() for p in all_files), 11)
    return all_files

def test_official_validator_mutants(files):
    vpath = BASE / "CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py"
    spec = importlib.util.spec_from_file_location("mcr_format", vpath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    n_format_false_positive = 0
    n_structural_red = 0
    for i, file in enumerate(files, 1):
        t = file.read_text(encoding="utf-8")
        base = module.validate(t)
        assert_case("CLI_STRUCTURE_%02d" % i, base["status"] == "PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH", base["status"])
        # Deliberately counterfeit an entire source/meaning oracle while preserving
        # every mandatory header and syntax field. This mutation is not a new source fact.
        fake = ("FROZEN_ORACLE_AND_COUNTEREXAMPLE: "
                "POS=all 182 inherited reference identities prove selected live native consumer application; "
                "NEG=the mere existence of matching historical Git blobs constitutes source semantic and actor issuance")
        mutated, n = re.subn(r"(?m)^FROZEN_ORACLE_AND_COUNTEREXAMPLE:.*$", fake, t, count=1)
        assert n == 1
        result = module.validate(mutated)
        assert result["status"] == "PASS_FORMAT_ONLY_NOT_AUTHORITY_OR_LAUNCH", (i, result)
        n_format_false_positive += 1
        # Mutate the structural pilot field: an honest parser must reject this.
        pilot_bad = re.sub(r"(PILOT=)CALIBRATION_NONTERMINAL", r"\1TERMINAL", t, count=1)
        assert pilot_bad != t
        red = module.validate(pilot_bad)
        assert red["status"] == "RED_INVALID_FOR_DISPATCH", (i, red)
        n_structural_red += 1
    assert_case("FORMAT_ONLY_FALSE_POSITIVE_CONTROL", n_format_false_positive == 11,
                {"semantic_false_promotions_accepted_by_actual_validator":n_format_false_positive,
                 "meaning":"FORMAT_ONLY; human/source MCR court must reject all 11"})
    assert_case("PILOT_STRUCTURAL_NEGATIVE_CONTROL", n_structural_red == 11,
                {"terminal_pilot_mutants_rejected_by_actual_validator":n_structural_red})

def test_version_and_output_defects(files):
    texts = [f.read_text(encoding="utf-8") for f in files]
    bad = "315251451a6d112fb312a6e80b096d345c5de6"
    correct = "315251451a6d112fb312a6a2e80b096d345c5de6"
    bad_ids = [i + 1 for i, x in enumerate(texts) if bad in x]
    assert_case("SOURCE_REF_NONHEX_LENGTH", len(bad)==38 and len(correct)==40 and bad_ids == [3,4],
                {"flights":bad_ids, "malformed":bad, "actual":correct})
    invisible = [i+1 for i,x in enumerate(texts) if "\u00ad" in x]
    assert_case("OUTPUT_PATH_INVISIBLE_BYTE", invisible == [11] and
                "EPIS\u00adTEMIC_GRADE_MATRIX.tsv" in texts[10], {"flights":invisible, "char":"U+00AD"})
    courts = [x[x.index("\nENGINEERING COURT"):x.index("\nSTOP AND RETURN")] for x in texts]
    assert_case("ALL_THREE_COURTS_PRESENT", all(all(label in x for label in
                ("ENGINEERING COURT", "SCIENTIFIC COURT", "AUTHORITY COURT",
                 "ACCEPT_IF:", "FAIL_RED_IF:", "HOLD_IF:", "EVIDENCE:", "OWNER_OF_DECISION:")) for x in courts), "11/11")

def test_v549b_source_extracted_progress():
    src = SOURCES["V549b"]
    tree = ast.parse(src)
    stores = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id=="answer_type" and isinstance(n.ctx, ast.Store)]
    assert_case("V549B_ANSWER_TYPE_UNBOUND", len(stores)==0 and src.count("answer_type")==1,
                "Only use is reporter format at old source line 607; no assignment exists")
    target = [n for n in ast.walk(tree) if isinstance(n, ast.If) and n.lineno==605]
    assert len(target)==1
    snippet = ast.Module(body=[copy.deepcopy(target[0])],type_ignores=[])
    class Reporter:
        def maybe_emit(self, message):
            raise AssertionError("should fail constructing message before emitter")
    ns={"reporter":Reporter(),"other_index":50,"PROGRESS_ITEM_STEP":50,
        "source":"GSS","wave":"1973","country":"us",
        "var_name":"war","cand_item_id":"prior_item","candidate_items":list(range(50)),
        "rows":[],"exclusions":[]}
    caught = None
    try:
        exec(compile(ast.fix_missing_locations(snippet), "<V549B_EXACT_AST_REPORTER>", "exec"),ns)
    except NameError as exc:
        caught = str(exc)
    assert_case("V549B_REPORTER_BRANCH_EXECUTED_RED", caught is not None and "answer_type" in caught,
                {"actual_exception":caught,"source_line":605,"scope":"SOURCE_EXTRACT_AST_STUBBED; NOT_FULL_PANDAS_RUN"})
    # The earlier progress message is evaluated BEFORE rebinding the current item_id.
    outer = [n for n in ast.walk(tree) if isinstance(n, ast.For) and n.lineno==564]
    assert len(outer)==1
    f=outer[0]; reporter_line = next(n.lineno for n in ast.walk(f) if isinstance(n, ast.If) and n.lineno==565)
    rebind = next(n.lineno for n in f.body if isinstance(n, ast.Assign) and any(isinstance(t,ast.Name) and t.id=="item_id" for t in n.targets))
    assert_case("V549B_PROGRESS_STALE_LABEL", reporter_line < rebind,
                {"reporter_line":reporter_line,"current_item_rebind_line":rebind})

def test_f03_source_extracted_quc_no_match():
    fn = exact_func(SOURCES["F03"], "apply_question_relation_authority")
    resolution=SimpleNamespace(authority_row=None, status="NO_MATCH",reason="no governing registry row",normalized_country_code="")
    def clear_coords(out):
        for key in ("relation_axis_id","target_entity_id","driver_facet_id"):
            out[key] = ""
    ns={
        "load_question_relation_authority":lambda path=None:SimpleNamespace(path="fake_exact_source"),
        "resolve_question_relation_authority":lambda **kw:resolution,
        "_authority_metadata":lambda out,r,index:None,
        "_clear_structural_coordinates":clear_coords,
        "_bool":lambda v,default=False: v if isinstance(v,bool) else str(v).lower() in ("true","yes","1"),
        "STRUCTURAL_COORDINATE_FIELDS":("relation_axis_id","target_entity_id","driver_facet_id"),
        "DIRECTIONAL_STATUS":"GOVERNED_DIRECTIONAL",
        "NEUTRAL_COVERAGE_STATUS":"NEUTRAL_COVERAGE",
    }
    apply = extracted_exec(fn,ns)
    inbound={"source":"GSS","wave":"1973","var_code":"uswar",
             "relation_axis_id":"UNVERIFIED_PREEXISTING_COORDINATE",
             "semantic_role_authority_status":"CERTIFIED","semantic_role":"RELATION_EVIDENCE",
             "current_directional_atom_eligible":True,
             "allowed_as_v551_relation_evidence":True,
             "structural_mapping_status":"COMPLETE"}
    keep=apply(inbound)
    assert_case("F03_Q_U_C_PRESERVES_WITHOUT_REGISTRY_ROW",
                keep["relation_axis_id"]=="UNVERIFIED_PREEXISTING_COORDINATE" and
                keep["question_relation_registry_match"] is False and
                keep["question_relation_authority_resolution"]=="QUC_AUTHORITY_PRESERVED_ACTIVE_REGISTRY_NO_MATCH",
                {"scope":"EXACT_SOURCE_FUNCTION_WITH_STUBBED_INDEX",
                 "proof":"inbound field flags suffice for historic no-match preservation; no independent issuer checked in this branch"})
    deny=apply({**inbound,"allowed_as_v551_relation_evidence":False})
    assert_case("F03_Q_U_C_FAIL_CLOSED_ON_FALSE_ALLOWED",
                deny["relation_axis_id"]=="" and deny["semantic_role"]=="UNKNOWN" and
                deny["manual_review_flag"] is True, {"scope":"EXACT_SOURCE_FUNCTION_WITH_STUBBED_INDEX"})
    deny_partial=apply({**inbound,"structural_mapping_status":"PARTIAL"})
    assert_case("F03_Q_U_C_FAIL_CLOSED_ON_PARTIAL", deny_partial["relation_axis_id"]=="" and
                deny_partial["allowed_as_v551_relation_evidence"] is False,
                {"scope":"EXACT_SOURCE_FUNCTION_WITH_STUBBED_INDEX"})

def test_v552_overcount_and_allow_independence():
    src=SOURCES["V552"]
    class Series:
        def __init__(self, values):self.values=values
        def dropna(self):return Series([v for v in self.values if v is not None])
        def astype(self, dtype):return Series([dtype(v) for v in self.values])
        def fillna(self, value):return Series([value if v is None else v for v in self.values])
        def sum(self):return sum(self.values)
        def __iter__(self):return iter(self.values)
    class Frame:
        empty=False
        def __init__(self, values):self.n_unweighted=Series(values)
        def get(self, key, default):return Series([2,2]) if key=="n_respondents" else default
    pd=SimpleNamespace(to_numeric=lambda s,errors="coerce":s, Series=lambda dtype:Series([]))
    fn=extracted_exec(exact_func(src,"_surface"), {"pd":pd,"V552_EPSILON":1e-12})
    ordinary=fn(Frame([1,1])); over=fn(Frame([2,2]))
    assert_case("V552_COVERAGE_ORIGINAL_FUNCTION",
                ordinary[0]=="COMPLETE_SELECTED_RESPONSE_CATEGORY_COVERAGE" and
                over[0]=="BLOCKED_RESPONSE_CATEGORY_COUNT_EXCEEDS_DENOMINATOR" and
                over[1]==2.0,
                {"ordinary":ordinary,"overcount":over,"scope":"EXACT_SOURCE_FUNCTION_WITH_STUBBED_SERIES"})
    main = ast.get_source_segment(src, exact_func(src,"build_v552_pressure_observation_index"))
    start=main.index("if debt:status=evidence")
    end=main.index("\n        signed=pd.to_numeric(c.get(",start)
    computation_branch=main[start:end]
    assert_case("V552_OVERCOUNT_DIAGNOSTIC_NOT_SCORE_GATE",
                "perm=\"ALLOW\"" in computation_branch and
                re.search(r"\bsel\b",computation_branch) is None,
                {"scope":"EXACT_SOURCE_AST_CONTROL_DEPENDENCY; NOT_FULL_DATAFRAME_CONSUMER",
                 "observed":"selected surface status does not guard nondebt score/ALLOW path"})

def test_current_authority_and_optional_target():
    auth=SOURCES["CURRENT_AUTH"];query=SOURCES["CURRENT_QUERY"]
    assert_case("CURRENT_EXACT_POSITIVE_SCOPE_GUARD",
                all(x in auth for x in ("snapshot.decision_state != POSITIVE_AUTHORITY_STATE",
                  "snapshot.authority_kind != authority_kind",
                  "operation not in snapshot.governed_operations",
                  "object family not named by exact authority",
                  "exact authority scope does not include")),
                "Current snapshot checks decision, kind, operation, family, and scope; not proof source selection")
    assert_case("CURRENT_TARGET_USE_TRIPLE_CONDITIONAL",
                all(x in query for x in ("if not declared_target_keys:\n        return",
                      "I03 target-use permission must bind ref, authority, and operation together",
                      'authority_kind="TARGET_USE_PERMISSION"')),
                "Target-use triple required if declared; no triple => this check returns; no implication every query lacks other guards")

def main():
    files=read_and_pin()
    test_official_validator_mutants(files)
    test_version_and_output_defects(files)
    test_v549b_source_extracted_progress()
    test_f03_source_extracted_quc_no_match()
    test_v552_overcount_and_allow_independence()
    test_current_authority_and_optional_target()
    out={"schema":"ZAK00R_V2_SOURCE_PINNED_MCR_HOSTILE_PROBE_R1",
         "candidate_head":"9d24323494cc852ada078010f09bfcf9ceb911d9",
         "grade":"S1_CODE_PIN_PLUS_SOURCE_EXTRACTED_S2_STUB_BRANCH; NOT_ORIGINAL35_OR_NATIVE",
         "source_pin_checks":len(SOURCE_PINS),"assertions":len(REPORTS),
         "candidate_decision":"REVISE_EXACT_DEFECT__NO_AUTHORITY_ACCEPTANCE",
         "tests":REPORTS}
    print(json.dumps(out,indent=2))
if __name__=="__main__":main()
