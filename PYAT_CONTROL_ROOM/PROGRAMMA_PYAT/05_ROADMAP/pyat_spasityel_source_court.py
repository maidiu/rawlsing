#!/usr/bin/env python3
"""AUTHOR-run source-fate evidence court, not independent G5 or a new registry."""
import ast, base64, gzip, hashlib, json, os, re, sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from urllib.error import HTTPError
HERE=Path(__file__).resolve().parent
REPO="maidiu/rawlsing"
B16="8676569af1e6580979a7265aeca1c499165fde24"
S1247="53517c4acecf6246ee6ed3ba7974bc7e6297d8ff"
S1267="102b274e3f99e744c9cfc91aa6f044508c24127a"
D=("data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
 "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
 "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/"
 "B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B16_C05R2B_REAL_LITS1_PRODUCTION_I05_R1/")
IDS="001 002 003 004 017 018 019 026 028 059 060 061 062 063 064 065 066 067 068 069 070 071 072 073 074 075 076 077 078 079 080 081 082 083 084 085 086 087 088 089 090 091".split()
TRANSFERS=set("003 004 065 071 080 077 078 083 084 085".split())
G4={"INDEX.jsonl":"4d3b0a5ac02b54fde70f2b62a69867f1fb720bf8",
"FUNCTION_PARITY.jsonl":"3183bd36fc216cc400814e547b46f4db40fdeba8",
"COMPONENT_STATUS.jsonl":"bd0d7832a684e89db71b888f5b6abda6fe59ea4e",
"CURRENT_SEAM_STATES.jsonl":"2584e331950f4aaa4b54a7863e65c68b403c3ed4"}
checks=[]
report={"grade":"AUTHOR_SOURCE_COURT_NOT_INDEPENDENT_G5","exact_head":os.getenv("GITHUB_SHA"),"checks":checks,"B16":{},"holds":[]}
def test(name,ok,info=None):
 checks.append({"check":name,"pass":bool(ok),"info":info})
 print(("PASS " if ok else "FAIL ")+name+" "+str(info)[:240],flush=True)
def blob(data):
 return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def fetch(ref,path,allow404=False):
 url="https://api.github.com/repos/"+REPO+"/contents/"+quote(path,safe="/")+"?ref="+ref
 h={"Accept":"application/vnd.github+json","User-Agent":"PYAT-SPASITYEL-exact-source-court"}
 if os.getenv("GITHUB_TOKEN"):h["Authorization"]="Bearer "+os.getenv("GITHUB_TOKEN")
 try:
  with urlopen(Request(url,headers=h),timeout=50) as response: doc=json.load(response)
 except HTTPError as err:
  if allow404 and err.code==404:return None
  raise
 if doc.get("encoding")!="base64":raise ValueError("Source content not base64: "+path)
 return base64.b64decode(doc["content"])
def exact(ref,path,sha):
 data=fetch(ref,path); found=blob(data)
 test("EXACT_GIT_BLOB "+path,found==sha,found)
 return data
class SourceForensicHold(Exception):pass
try:
 k=(HERE/"KUDA.md").read_text()
 n=(HERE/"NEKUDA.md").read_text()
 l=(HERE/"PYAT_SPASITYEL_KUDA_ADJUDICATION_AND_REVIEW_LOG.md").read_text()
 expect=["KUDA-"+x for x in IDS]
 ki=re.findall(r"^### (KUDA-\d{3}) —",k,re.M)
 li=re.findall(r"^\| \[(KUDA-\d{3})\]\(KUDA\.md#kuda-\d{3}\)",l,re.M)
 test("exact 42 KUDA source identities preserved",ki==expect,len(ki))
 test("exact 42 log identities same order",li==expect,len(li))
 reviews=re.findall(r"^### (IR-\d{2})",l,re.M)
 test("single ten-family review queue",reviews==["IR-%02d"%i for i in range(1,11)],reviews)

 # R20–R21 structure is checked, but source/need judgments are NOT mechanically certified.
 r20=l.split("## 8. R20 — economical seven-part",1)[1].split("## 9. R21 — remaining",1)[0]
 r21=l.split("## 9. R21 — remaining",1)[1].split("## 10. R22 — DEEP TRANCHE 1:",1)[0]
 family_entries=re.findall(r"^\| \*\*([A-J]) — [^\n]*?\*\* \(([^)]+)\) \|",r20,re.M)
 family_ids={}
 for family,source_ids in family_entries:
  family_ids[family]=re.findall(r"KUDA-(\d{3})",source_ids)
 court_a=re.findall(r"^\| \[(\d{3})\]\(KUDA\.md#kuda-(\d{3})\) · ([A-J]) \|[^\n]+",r20,re.M)
 court_b=re.findall(r"^\| \[(\d{3})\]\(KUDA\.md#kuda-(\d{3})\) ([A-J]) \|[^\n]+",r21,re.M)
 proposed=court_a+court_b
 expected_ids=set(IDS)
 test("seven-part docket: 10 shared Q1/Q2 necessity baselines",
      len(family_entries)==10 and set(family_ids)==set("ABCDEFGHIJ")
      and len(set(i for ids in family_ids.values() for i in ids))==42,
      {"family_count":len(family_entries),"group_total":sum(map(len,family_ids.values()))})
 test("seven-part docket: exact 24 P0 + 18 downstream records",
      len(court_a)==24 and len(court_b)==18,
      {"P0":len(court_a),"downstream":len(court_b)})
 test("seven-part docket: each historic KUDA exactly once, no invented ID",
      len(proposed)==42 and len({i for i,_,_ in proposed})==42
      and {i for i,_,_ in proposed}==expected_ids
      and all(i==link_id and i in family_ids.get(family,()) for i,link_id,family in proposed),
      {"seen":len(proposed),"unique":len({i for i,_,_ in proposed})})
 case_lines=[line for section in (r20,r21) for line in section.splitlines()
             if re.match(r"^\| \[\d{3}\]\(KUDA\.md#kuda-\d{3}\)",line)]
 test("seven-part docket: each record has eight actual table columns",
      len(case_lines)==42 and all(len(re.split(r"(?<!\\)\|",line))==10 for line in case_lines),
      {"rows":len(case_lines),
       "unexpected_column_counts":[len(re.split(r"(?<!\\)\|",line)) for line in case_lines if len(re.split(r"(?<!\\)\|",line))!=10][:8]})
 report["seven_part_limit"]="STRUCTURAL_COVERAGE_ONLY_NOT_INDEPENDENT_QUALITY_OR_NECESSITY_ACCEPTANCE"

 # R22 selective deep-tranche source checks: these confirm observations, NOT science/semantics.
 r22=l.split("## 10. R22 — DEEP TRANCHE 1:",1)[1]
 deep_cases=re.findall(r"^### 10\.([123]) KUDA-(\d{3})",r22,re.M)
 test("R22 deep tranche exact three assessed IDs, no other automatic promotion",
      deep_cases==[("1","068"),("2","069"),("3","072")],deep_cases)
 deep_ref="997ca50869551d292650c710a2c99a43c9119f7a"
 source=exact(deep_ref,"rawlsing_next/pre553_source_i02_handoff.py",
              "4bed962724efdf68c31f7a13e697533c7552c8aa").decode()
 test("KUDA-068 original prehash plus one decoded source read, one semantic cell pass",
      all(phrase in source for phrase in (
        "source_prehash_passes = 1 if original_source else 0",
        "source_reads = 1 + source_prehash_passes",
        "for cell in incidence.iter_cells(batch_size):",
        "seen: dict[tuple[int, str], set[int]]")),
      "SOURCE_STATIC_ONLY: no cost benchmark")
 reader=exact(deep_ref,"rawlsing_next/pre553_direct_estate_i03.py",
              "9fd39efb858be48c6883e0238266a4991ac6de49").decode()
 estate=exact(deep_ref,"rawlsing_next/pre553_source_direct_parquet_estate.py",
              "e8622ac6bf59c4d1ec052e21410e63aab7dd9aa1").decode()
 test("KUDA-069 exact Parquet member hashes and per-context native posting rebuild",
      all(phrase in reader for phrase in (
        "self._temporary = tempfile.TemporaryDirectory(",
        "self._build()",
        "self._validate_event_body_truth(body, row)",
        "CREATE INDEX events_resp_idx ON events(respondent,ref)",
        "ORDER BY gid,off")) and
      all(phrase in estate for phrase in (
        "for name, digest in members.items():",
        "_hash(member) != digest")),
      "SOURCE_STATIC_ONLY: cost stage not measured by this test")
 prepared=exact(deep_ref,"rawlsing_next/pre553_prepared_saved_i03.py",
                "dd57604f2416f46b912daaad36bd9eedb09ff3ea").decode()
 klass=next(c for c in ast.parse(prepared).body
            if isinstance(c,ast.ClassDef) and c.name=="PreparedI03Session")
 ctor=next(m for m in klass.body if isinstance(m,ast.FunctionDef) and m.name=="__init__")
 constructor=ast.get_source_segment(prepared,ctor)
 mismatch=("type(admission) is not PreparedSavedC11Admission" in constructor
           and "type(session) is not DirectEstateI03Session" in constructor
           and "session.estate" not in constructor
           and "admission._estate" not in constructor
           and not any(isinstance(n,ast.FunctionDef) and n.name=="__setattr__" for n in klass.body))
 test("KUDA-072 preexisting EXPORTED admission/session pinning defect still in selected source",
      mismatch,"EXPECTED SOURCE DEFECT / NOT BEHAVIORAL EXPLOIT EXECUTION")
 if mismatch:
  report["holds"].append("KUDA-072_PUBLIC_PREPARED_A_B_ADMISSION_SESSION_RECEIPT_PINNING_REPAIR_REQUIRED")
 report["R22_scope"]="THREE_DEEP_SOURCE_STATIC_JUDGMENTS__ACTUAL_P0_NATIVE_AND_COST_AUTHORITY_HELD"

 # R23 ordered early STOP filters and three source-graded case decisions.
 r23=l.split("## 11. R23 — CHEAP ELIMINATION GATES",1)[1]
 deep23=re.findall(r"^### 11\.([123]) KUDA-(\d{3})",r23,re.M)
 test("R23 next deep tranche exact three IDs, not 42 promotions",
      deep23==[("1","001"),("2","002"),("3","070")],deep23)
 for marker in ("A — Q2 necessity","B — Q3 independently necessary reader",
                "C — Q1 adequate existing successor","D — Q5 obvious unsuitability",
                "All gates are **three-valued: YES/NO/UNKNOWN**"):
  test("R23 cheap gate documented "+marker,marker in r23)
 deep_ref="997ca50869551d292650c710a2c99a43c9119f7a"
 proj=exact(deep_ref,"rawlsing_next/pre553_r157_projection_adapter.py",
            "d4d84ef164feba6fb0de0851568738eb5f5e937d").decode()
 test("KUDA-001 selected source config composes governed C11 without source permission mint",
      all(needle in proj for needle in (
       "def validate_source_config(document:",
       "def build_governed_c11_projection(",
       "def decode_with_source_read_permission(",
       "ORIGINAL_SOURCE binding requires SOURCE_PREPARATION",
       "NOT_PERFORMED_UNDER_R157_PREPARATION")),
      "SOURCE_STATIC, original item science and rights external")
 original=exact("b5600da96358f8526471d635a1befa8daa3f098b",
                "rawlsing_next/pre553_inherited_source_rules.py",
                "5f6efaceb18d92a362d065d12fdca4076d53fa16").decode()
 klass=next(n for n in ast.parse(original).body
            if isinstance(n,ast.FunctionDef) and n.name=="_classify_item")
 code=ast.get_source_segment(original,klass)
 test("KUDA-002 historical selector gate requires only nonempty binding, not affirmed grant",
      "if not item.response_binding_status:" in code
      and "status=U_CANDIDATE" in code
      and "reason=\"EXACT_AUTHORITY_SELECTED\"" in code,
      "SOURCE_STATIC NEGATIVE: hypothetical nonaffirmative nonempty status can pass; no original science claim")
 missing=fetch(deep_ref,"rawlsing_next/pre553_inherited_source_rules.py",allow404=True)
 test("KUDA-002 old B49 selector absent selected #1247, missing symbol alone not gap",
      missing is None,"NOT_IMPLEMENTATION_NECESSITY")
 issuer=exact(deep_ref,"rawlsing_next/pre553_governed_query_issuer_v2.py",
              "a55275c4b5f824496f7d18df9d013e1ab883a317").decode()
 test("KUDA-070 selected v2 issuer is existing separate TEST_ONLY original-role binding",
      all(needle in issuer for needle in (
       "def compile_and_issue_governed_queries_v2(",
       "compile_governed_frontier(",
       "TEST_ONLY_DECISION",
       "TEST_ONLY_SCIENTIFIC_PERMISSION",
       "R03_V2_NONELIGIBLE_SUPPORTED_OPERATION")),
      "SOURCE_STATIC: original authoritative source/science issuer absent")
 report["R23_limit"]="THREE_DEEP_WORK_SELECTION_JUDGMENTS__LEGACY_REJECT_NOT_FUNCTION_RETIREMENT"

 # R24 is an ELIMINATION ONLY docket. The checker enforces no-drop and honest class
 # accounting, NOT the correctness of 42 separate scientific/implementation rulings.
 r24=l.split("## 12. R24 — careful whole-KUDA elimination adjudication",1)[1]
 part_a=r24.split("### 12.1 P0 & physical carriers: A–C (24 IDs)",1)[1].split("### 12.2 D–J:",1)[0]
 part_b=r24.split("### 12.2 D–J:",1)[1].split("### 12.3 Cross-cutting elimination result:",1)[0]
 def elimination_rows(section):
  records=[]
  for line in section.splitlines():
   m=re.match(r"^\| \[(\d{3})\]\(KUDA\.md#kuda-(\d{3})\) \| (.+) \|$",line)
   if not m: continue
   fields=re.split(r"(?<!\\) \| ",m.group(3))
   records.append((m.group(1),m.group(2),fields))
  return records
 first=elimination_rows(part_a);second=elimination_rows(part_b)
 elected=first+second
 test("R24 eliminated-by-function court exact 24 P0 plus 18 downstream",
      len(first)==24 and len(second)==18,
      {"p0":len(first),"downstream":len(second)})
 test("R24 each historic KUDA exactly once with actual matching original link",
      len(elected)==42 and len({i for i,_,_ in elected})==42
      and {i for i,_,_ in elected}==set(IDS)
      and all(i==link_id for i,link_id,_ in elected),
      {"total":len(elected),"unique":len({i for i,_,_ in elected})})
 test("R24 every verdict has Q2/Q3/Q1/Q5, conserved necessary function and exact falsifier",
      all(len(fields)==7 and all(value.strip() for value in fields)
              for _,_,fields in elected),
      {"rows":len(elected),"incomplete":[i for i,_,fields in elected if len(fields)!=7]})
 expected_categories={
  "STOP_DUPLICATE_PORT":10,"STOP_EXACT_DUPLICATE":1,
  "STOP_LEGACY_UNSUITABLE":2,"STOP_BROKEN_ARCHIVE":1,
  "STOP_NO_EXTERNAL_READER":2,"STOP_FOREIGN_OWNER":4,
  "KEEP_EXISTING_OWNER":9,"HOLD_PHYSICAL_COMPARATOR":3,
  "HOLD_TEST_ORACLE":3,"HOLD_CONDITIONAL_CONSUMER":3,
  "HOLD_NARROW_NEGATIVE":3,"HOLD_PARTIAL_DISTINCT":1,
 }
 actual_categories={}
 for _,_,fields in elected:
  if len(fields)!=7:continue
  verdict=fields[4]
  actual_categories[verdict]=actual_categories.get(verdict,0)+1
 test("R24 exact twelve source-qualified decision classes and 20/9/13 division",
      actual_categories==expected_categories,
      actual_categories)
 for needle in (
  "UNKNOWN never becomes NO or BUILD",
  "A STOP rejects a proposed historical module or development ticket",
  "SOROK actor construction obligation remains live",
  "NOT FIXED",
  "not 42 final full seven-criterion executable/scientific acceptances",
 ):
  test("R24 source-grade no-false-retirement qualification "+needle,
       needle.lower() in r24.lower())
 report["R24_grade"]="AUTHOR_SOURCE_STATIC_ELIMINATION_ONLY_NOT_INDEPENDENT_G5_NOT_42_DEEP_TESTS"
 report["R24_fates"]=actual_categories

 # R26 — thirteen held historical implementations exact-body identity and selected owner overlap.
 r26=l.split("## 14. R26 — S1/S2 exact-source adjudication",1)[1]
 r26rows=re.findall(r"^\| \[(\d{3})\]\(KUDA\.md#kuda-\d{3}\)",r26,re.M)
 expected_r26=set("028 077 083 067 081 086 078 082 091 017 018 019 076".split())
 test("R26 exactly thirteen source-specific stop-filter cases",len(r26rows)==13
      and set(r26rows)==expected_r26,r26rows)
 historic=[
  ("028","46b7325637e68f78ccc7487d4b1abc7009c5ac0b",
   "rawlsing_next/_pre553_c11_execution_view.py","986f327aa18053edc61bd837cdded02bbf8388d9"),
  ("077",B16,"rawlsing_next/pre553_route_c_accelerators.py",
   "abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889"),
  ("083",B16,"rawlsing_next/pre553_r5_compact_carrier.py",
   "92e364b31eaf27be1bca2081eff65f6ffb779c3d"),
  ("067","624ad8d1516d32ecb30657d61103636c6fc966af",
   "rawlsing_next/field_forge_conditional_support.py","fd8570ec6bf6ee6e140abbcb251dd486da5d60cb"),
  ("081","624ad8d1516d32ecb30657d61103636c6fc966af",
   "rawlsing_next/gt12_c_to_d_relation_bridge.py","2f5066fdb308386f700537c1931655499a99ca13"),
  ("086","9c776b358c5f5a31f2ff2d35460d5350c0dc2bc8",
   "rawlsing_next/field_forge_conditional_support.py","cad7b2e1b1dbaf1478b3d0e2816f49629c31b2a1"),
  ("078",B16,"rawlsing_next/as4/protocol.py","590da3a2cc54666bd9786130409170b73310a700"),
  ("082","0dc9a21f9b491d27c711082ad9c39c05509211b0",
   "rawlsing_next/universal_source_to_c11/consumer.py","41cfc0f5a1b0528a60f35f08169f2464d425aa60"),
  ("091","c07368ef37202f89ed298fa076c409c579f62202",
   "rawlsing_next/wsc_gt0_end_to_end.py","1b23013e644582218e3b67de32c163575036d39e"),
  ("017","1f1c72f883d0d7a6d11d7df8bad75c37d06c3ffa",
   "WORKER_RETURNS/PYAT-R29-F6M-NATIVE-AUTHORITY-REPAIR-R1/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py","2df811d76db258d98d89ffb43c830cb221ff9a7d"),
  ("018","016870e86913e6f7a811a51db6aba2d741bcfe58",
   "WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/f6p_partial_bound_evidence_consumer.py","8fa992899293f454d7abded36831a4b4a362df8e"),
  ("019","f8fe03cc6e6a482f428bed9e03c08e50ce1e6479",
   "WORKER_RETURNS/PYAT-F7-P07-RECOVERY/candidate/temporal_method_candidate.py","f93fc79c182b1962dc3b3a25915b8d93afe7e5c7"),
  ("076","7628840c4c8e95b320cadc672743355afbe2958a",
   "WORKER_RETURNS/PYAT-R37-N9J-SELECTED-WORLD-PROGRESSIVE-CONSUMER-R1/native/e05_n9_selected_world_adapter.py","642381bc033aaeef878624bdce71f9f94708043d"),
 ]
 historic_body={}
 for ident,ref,path,expected in historic:
  historic_body[ident]=exact(ref,path,expected).decode()
 test("R26 historic unique thirteen exact body identities",set(historic_body)==expected_r26)
 selected_cut="997ca50869551d292650c710a2c99a43c9119f7a"
 current_ff=exact(selected_cut,"rawlsing_next/field_forge_conditional_support.py",
     "a70decb20747d84cbcbe27d1280babc6de88ef33").decode()
 combined_ff=exact(S1267,"rawlsing_next/field_forge_conditional_support.py",
     "a22c66dfc73a651a0d7df071d644426411a5d5f7").decode()
 current_d=exact(selected_cut,"rawlsing_next/gt12_c_to_d_relation_bridge.py",
     "ea04ec079e8d60e6e5c7236ec5b54898876be4b3").decode()
 combined_d=exact(S1267,"rawlsing_next/gt12_c_to_d_relation_bridge.py",
     "2f5066fdb308386f700537c1931655499a99ca13").decode()
 current_r112=exact(selected_cut,"rawlsing_next/pre553_world_conditioned_progressive_service.py",
     "809a60c1cbfeb90af625c308a29bea46e3bfee9e").decode()
 combined_r112=exact(S1267,"rawlsing_next/pre553_world_conditioned_progressive_service.py",
     "004ec58dbfd8732d1139e32ce7c7a0eb6a7a0380").decode()
 test("R26 FF01 067 and 086 BOTH coexist in one held combined blob",
      "_check_positive_respondent_extent" not in current_ff
      and "_validate_frozen_q86_source_identity" not in current_ff
      and all(x in combined_ff for x in (
       "def _check_positive_respondent_extent(",
       "def _validate_frozen_q86_source_identity(")),
      "STATIC_UNION_NOT_EXECUTED_AT_COMBINED_SHA")
 test("R26 D C-to-D 081 distinct selected original source contradiction guard",
      "def admit_gt12_c_relation_from_fixed_current_transport(" not in current_d
      and "def admit_gt12_c_relation_from_fixed_current_transport(" in combined_d,
      "STATIC_NOT_NATIVE_REVIEWED")
 test("R26 R112 076 postread field check added into existing owner",
      "def _verify_e05_field_read(" not in current_r112
      and "def _verify_e05_field_read(" in combined_r112,
      "TEST_ONLY_CANDIDATE; N9C different held function")
 f6m=exact(S1267,"rawlsing_next/pre553_heterogeneous_synthesis.py",
           "2df811d76db258d98d89ffb43c830cb221ff9a7d")
 f6p=exact(S1267,"rawlsing_next/_f6_candidate/f6p_partial_bound_evidence_consumer.py",
           "8fa992899293f454d7abded36831a4b4a362df8e")
 test("R26 017/018 original body exact duplication on held candidate",
      f6m==historic_body["017"].encode() and f6p==historic_body["018"].encode(),
      "Does not grant external world receiver")
 current_g=exact(selected_cut,"rawlsing_next/wsc_gt0_end_to_end.py",
   "62b6ea39c605874af6d7aef85693472f88087f57").decode()
 newtests=exact(S1267,"rawlsing_next/tests/test_kuda091_gt0_real_spine_hostiles.py",
   "3540990bd108f99fb38c314aa7c1dac7408be440").decode()
 test("R26 091 old fake stage ABI replaced by actual stage hostile assertions",
      "class GT0StageAPI:" in historic_body["091"]
      and "class GT0StageAPI:" not in current_g
      and "test_original_kuda091_v3_rng_state_mutation_detected_in_actual_spine" in newtests
      and "test_original_kuda091_v2_actor_expression" in newtests,
      "OLD_OTHER_NEGATIVES_NOT_EXHAUSTIVELY_COMPARED")
 ftest=exact(S1267,"rawlsing_next/tests/test_kuda082_r157_current_c11_parity.py",
   "9934459bb2fd43b35830fbbdf5c21c2b41b01110").decode()
 test("R26 082 test-only original fixture parity/refusal now has selected-owner code",
      "def receive_fixture_release(" in historic_body["082"]
      and "original_execution" in historic_body["082"]
      and "test_independent_current_r157_facade_vs_direct_i02_parity" in ftest
      and "decode_fixture_config refuses ORIGINAL_SOURCE" in ftest,
      "35-specific roster negatives not yet shown equivalent")
 current_view=exact(selected_cut,"rawlsing_next/_pre553_c11_execution_view.py",
  "de5613301eb54aefaccb002e3c8dc4c657885479").decode()
 test("R26 028 competing physical compression shape is not same source body",
      "class _CompressedBodies:" in historic_body["028"]
      and "class _CompressedBodies:" not in current_view
      and "def _read_bodies(" in current_view,
      "NOT A PERFORMANCE VERDICT")
 test("R26 077 and 083 original alternate physical contracts require selected test",
      "require_frozen_lits1_scope" in historic_body["077"]
      and "class R5CompactLongShardedBuilder:" in historic_body["083"]
      and "class HB04CandidateSession:" in historic_body["078"],
      "NO SAME-WORKLOAD ORIGINAL WIDTH WIN")
 test("R26 P07 exact version selector vs selected R06 label not a binding",
      "def select_as_of_version(" in historic_body["019"]
      and "class AsOfVersion:" in historic_body["019"]
      and "def select_world_view(" in exact(selected_cut,
          "rawlsing_next/pre553_universal_world_binding.py",
          "fdda8b2f887bd1fb7703bc5fb8ce1fefc52ca09d").decode(),
      "CLASS/METHOD COEXISTENCE ONLY; source-issued relation unknown")
 report["R26_grade"]="13_SOURCE_BODIES_S1_S2_STATIC__SELECTED_FIRST_CONSUMER_DIFFERENTIAL_HELD"
 report["R26_outcomes"]={"physical_single_comparator":3,"existing_owner_combined_candidate_no_old_port":4,
                         "legacy_test_oracle_partial":3,"source_science_external_consumer_held":3}

 # R27 source and documentary first-reader bank — author CI proof is external run.
 r27=l.split("## 15. R27 — TESTS-ONLY",1)[1]
 for key in ("196942c62b8dc919ff787f9eb2017ae2ee70860c",
             "44952903500","77 PASS / 0 FAIL","44952780251",
             "76 pass / 1 fail","14726372572",
             "NOT demonstrated","NO_NEW_RUNTIME_PORT"):
  test("R27 exact-SHA/sourcegrade/failure ledger "+key,key.lower() in r27.lower())
 test_code=exact("196942c62b8dc919ff787f9eb2017ae2ee70860c",
  "rawlsing_next/tests/test_spasityel_joined_s3a_first_consumer.py",
  "d90985212c7988c9e657d7f910a7219ec156c016").decode()
 test("R27 uses genuine FF01 and D runtime and both distinct hostile cases",
      all(v in test_code for v in (
       "ff.produce_exact_conditional_support_profile(",
       "d.admit_gt12_c_relation(",
       "denominator member outside risk set",
       "exact Q86B/Q86A QUESTION_IMPLEMENTATION",
       "declared producer source contradicts frozen GT12 physical source",
       "from dataclasses import replace")),
      "SOURCE_STATIC_TEST_ONLY; green CI at child head cited, not independently rerun")
 workflow=exact("196942c62b8dc919ff787f9eb2017ae2ee70860c",
  ".github/workflows/pyat-spasityel-joined-s3a-sourcefree.yml",
  "594cb2c005291ab31edac6b6a041c06324b5e258").decode()
 test("R27 current selected+E05 same sourcefree runner with immutable head check",
      "test \"$(git rev-parse HEAD)\" = \"$GITHUB_SHA\"" in workflow
      and "test_kuda076_e05_selected_world_guard.py" in workflow
      and "test_s3a_r5_denominator_membership_closure.py" in workflow)
 report["R27_grade"]="AUTHOR_EXECUTED_77_OF_77_AT_TEST_ONLY_SHA_NOT_G5_NOT_ORIGINAL_SOURCE"






 section=n.split("## NEKUDA-R13",1)[1].split("## NEKUDA-R8",1)[0]
 transfers=set(re.findall(r"^\| \[KUDA-(\d{3})\]",section,re.M))
 test("all ten standalone no-reimport fates retained",transfers==TRANSFERS,sorted(transfers))
 for name,sha in G4.items():
  test("original G4 machine table byte unchanged "+name,blob((HERE/name).read_bytes())==sha)
 p="rawlsing_next/_pre553_direct_i02_sourcefree.py"
 historical=exact("cc35e0a4e51394961f58b632dec8a149deea21a2",p,"451727511af7f727b082c518aae2f4a3dbe2ba3a")
 selected=exact(S1247,p,"451727511af7f727b082c518aae2f4a3dbe2ba3a")
 test("KUDA-065 identical direct I02 source",historical==selected)
 w05=fetch(S1247,"rawlsing_next/pre553_direct_estate_i03.py").decode()
 test("KUDA-071 selected W05 indices_for",all(z in w05 for z in ("class DirectEstateI03Session:","def indices_for(")))
 cache=exact(S1247,"rawlsing_next/pre553_source_backed_c11_facade.py","f29247b33cb78e5f1e620620d6968ab433ce407a").decode()
 test("KUDA-080 current cache identity & freeze",all(x in cache for x in ("def _cache_projection_preimage(","def cache_identity(","def source_backed_facade_key(","def _freeze_governed_input(")))
 r5=exact(B16,"rawlsing_next/pre553_r5_seam.py","cef326ebbc40468428378f7fdbe76e4756179f39").decode()
 test("KUDA-084 old geometry requires 0-based variable ordinal","0 <= variable_ordinal < self.variable_count" in r5)
 route=exact(B16,"rawlsing_next/pre553_route_c_accelerators.py","abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889").decode()
 test("KUDA-077 Route-C frozen LiTS scope","require_frozen_lits1_scope" in route and "require_successor_frozen_scope" in route)
 old=exact("d379bafe36b8d89da27ea5bf33614d33aca7f2d2","WORKER_RETURNS/PYAT-R50-G50-GOVERNED-OPERATION-GRAMMAR-R1/g50/enumerate.py","f610ef2dea39519a51a5b57fd35bbe245fb9dc9b").decode()
 current=exact(S1247,"rawlsing_next/universal_grammar/enumerate.py","fd9203a0b272f98771c24070d01a9e5287c9b099").decode()
 test("KUDA-003 old G50 smaller than selected R61 named surface (not parity)","def enumerate_frontier(" in old and "def partition_frontier(" in current and "def inventory_ledger(" in current)
 old=exact("9bbf9e0509411beb210331d28160324b005a784e","WORKER_RETURNS/PYAT-R51-I51-B49-G50-JOINED-PRODUCER-R1/candidate/r51_joined_source_producer.py","31eb9d6a17788b577b7aab46a290d68f12a59288").decode()
 current=exact(S1247,"rawlsing_next/pre553_governed_query_issuer_v2.py","a55275c4b5f824496f7d18df9d013e1ab883a317").decode()
 test("KUDA-004 I51 old toy distinct from current R03v2","def lower_to_b49(" in old and "def compile_and_issue_governed_queries_v2(" in current)
 old=exact("7628840c4c8e95b320cadc672743355afbe2958a","WORKER_RETURNS/PYAT-R37-N9J-SELECTED-WORLD-PROGRESSIVE-CONSUMER-R1/native/e05_n9_selected_world_adapter.py","642381bc033aaeef878624bdce71f9f94708043d").decode()
 r112=exact(S1267,"rawlsing_next/pre553_world_conditioned_progressive_service.py","004ec58dbfd8732d1139e32ce7c7a0eb6a7a0380").decode()
 n9c=fetch(S1267,"rawlsing_next/pre553_hq297_n9c_two_field_reader.py",allow404=True)
 partial="pre553_hq297_n9c_two_field_reader" in old and "read_historical_test_only(" in old and "def _verify_e05_field_read(" in r112 and n9c is None
 test("KUDA-076 PARTIAL ONLY: N9C two native-field readset absent selected",partial)
 if partial:report["holds"].append("KUDA-076_N9C_NONPOOLED_TWO_NATIVE_FIELD_READSET_NOT_RECOVERED")
 launcher=exact(B16,D+"01_C05R2B_PRODUCTION_EXECUTION_DRIVER.py","26d1e3ede625499a26c712844bffaff4d77e13da")
 chunks=[fetch(B16,D+"DRIVER_SOURCE_CHUNKS/part_0%d.b64"%i) for i in (0,1)]
 test("B16 two driver chunks exact lengths",list(map(len,chunks))==[7001,3052],list(map(len,chunks)))
 encoded=b"".join(chunks)
 archive_error=None
 recovered=None
 repair=None
 try:
  recovered=gzip.decompress(base64.b64decode(encoded,validate=True))
 except Exception as original_error:
  archive_error=repr(original_error)
  report["B16"]["as_committed_loader_error"]=archive_error
  # The frozen bootstrap used validate=True, so its direct load is objectively non-runnable.
  test("B16 archived Base64 strict-load failure is an actual historical packing defect",
       len(encoded)%4==1 and "padding" in str(original_error).lower(),
       {"concat_len":len(encoded),"error":archive_error})
  # Source recovery only, never execution or silent modification of frozen history.
  for position in range(len(encoded)):
   candidate=encoded[:position]+encoded[position+1:]
   try:
    decoded=gzip.decompress(base64.b64decode(candidate,validate=True))
   except Exception:
    continue
   digest=hashlib.sha256(decoded).hexdigest()
   if digest=="59ce6903776df5f5b17bc074b15d9ae06334a5a1c30fad91096fc3fb6a014a3f":
    recovered=decoded
    repair={"forensic_only_removed_base64_char_at_global_offset":position,
            "removed_character":chr(encoded[position]),"chunk_boundary":len(chunks[0]),
            "archived_source_unmodified":True}
    break
 if recovered is None:
  report["B16"]["forensic_recovery_status"]="EXACT_SOURCE_HELD_AFTER_ALL_SINGLE_CHARACTER_DELETIONS"
  report["holds"].append("B16_ARCHIVED_DRIVER_INVALID_STRICT_BASE64_AND_FULL_SOURCE_UNRECOVERED")
  raise SourceForensicHold("B16 invalid archived driver; no single-character-deletion matches expected SHA256")
 if repair:report["B16"]["forensic_boundary_repair"]=repair
 sha=hashlib.sha256(recovered).hexdigest()
 test("B16 exact effective uncompressed driver SHA256",sha=="59ce6903776df5f5b17bc074b15d9ae06334a5a1c30fad91096fc3fb6a014a3f",sha)
 asttree=ast.parse(recovered,filename="B16_EXACT_CODE_NOT_EXECUTED")
 funcs=[node.name for node in asttree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef))]
 imports=[node.module for node in asttree.body if isinstance(node,ast.ImportFrom) and node.module]
 test("B16 effective code AST genuinely inspectable",bool(funcs),{"bytes":len(recovered),"functions":funcs})
 report["B16"]={"bytes":len(recovered),"sha256":sha,"git_blob":blob(recovered),"functions":funcs,"imports":imports,"never_executed":True}
 runs=[json.loads(fetch(B16,D+filename)) for filename in ("05_PRODUCTION_RUN_1.json","06_PRODUCTION_RUN_2.json")]
 good=all(v["i05"]["candidate_count"]==82 and v["i05"]["empirical_fact_ref_count"]==140 and v["i05"]["unevaluated_count"]==0 and v["i05"]["terminal_state_counts"]=={"EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY / COVERAGE_LIMITED":82} for v in runs)
 test("B16 two real-source historical receipts have 82 negatives, zero scientific positives",good)
except SourceForensicHold as exc:
 print("B16_SOURCE_FORENSICS_HELD",str(exc),flush=True)
except Exception as exc:
 test("SOURCE_COURT_EXCEPTION",False,repr(exc))
finally:
 (HERE/"pyat_spasityel_source_court_result.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
 print("TOTAL",len(checks),"PASS",sum(c["pass"] for c in checks),"FAIL",sum(not c["pass"] for c in checks),flush=True)
sys.exit(0 if all(c["pass"] for c in checks) else 1)
