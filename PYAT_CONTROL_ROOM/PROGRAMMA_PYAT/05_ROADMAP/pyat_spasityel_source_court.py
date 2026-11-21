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
  for position in range(max(0,len(chunks[0])-16),min(len(encoded),len(chunks[0])+17)):
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
  raise RuntimeError("B16 packed driver is invalid and cannot be recovered by one-character boundary deletion")
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
except Exception as exc:
 test("SOURCE_COURT_EXCEPTION",False,repr(exc))
finally:
 (HERE/"pyat_spasityel_source_court_result.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
 print("TOTAL",len(checks),"PASS",sum(c["pass"] for c in checks),"FAIL",sum(not c["pass"] for c in checks),flush=True)
sys.exit(0 if all(c["pass"] for c in checks) else 1)
