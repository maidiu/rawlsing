#!/usr/bin/env python3
"""Read-only cross-court source custody: S6 groups, H1 challenge rows, PE/V2K files.
Exact historical Git objects, no candidate execution or semantic grant.
"""
import json,collections,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SHARDS=[("S1","6a658ad347ad0a714f40cbce04b5cd6d1f5b5ab5"),
("S2","3042fca8a2165e07871d408118e1741686020cdc"),
("S3","ebdb51a5c79209b2e552cfce648f7847b19386c2"),
("S4","d93e8c2441dfa394e56fc1f5bcf43a0b4388adcb"),
("S5","32dac59b3741dcc54f507321c7826e65174af372")]
S6="2c5cf86beb12b7dbeda5532614784737ad30d89d"
H1="815edc1bd74094522afb8c9dad1742ecb77ec800"
PE="9647d851a2d9b6e93e6711eec7a65325fb83aaa1"
def git(*args):
 p=subprocess.run(["git",*args],cwd=ROOT,capture_output=True,check=False)
 if p.returncode: raise RuntimeError("MISSING_GIT_OBJECT "+repr(args)+" "+p.stderr.decode(errors="replace")[-350:])
 return p.stdout
def raw(sha,path):return git("show",f"{sha}:{path}")
def jrows(sha,path):return [json.loads(v) for v in raw(sha,path).splitlines() if v.strip()]
def obj(sha,path):return json.loads(raw(sha,path))
def summarize_value(value):
 if isinstance(value,list):return {"type":"list","size":len(value),"sample":summarize_value(value[0]) if value else None}
 if isinstance(value,dict):return {"type":"dict","keys":list(value)[:30]}
 return {"type":type(value).__name__,"sample":str(value)[:125]}
def main():
 expected={}
 for sh,sha in SHARDS:
  p=f"PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/{sh}_EVIDENCE_REPAIR/FUNCTION_GRADE_CORRECTIONS.jsonl"
  r=jrows(sha,p)
  expected[sh]=[x.get("original_function_id") for x in r]
 gp="PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S6/"
 groups=jrows(S6,gp+"CROSS_SHARD_FUNCTION_GROUPS.jsonl")
 hp="PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/H1/"
 challenges=jrows(H1,hp+"H1_S1_S5_GRADE_CHALLENGES.jsonl")
 pe="WORKER_RETURNS/PYAT-R3-PE-V2K-SCOPED-RECOVERY/"
 lineage=jrows(PE,pe+"FUNCTION_ORIGIN_AND_SUCCESSOR_MAP.jsonl")
 matrices={}
 for name,path in [("consumers",gp+"CURRENT_RECEIVER_FIRST_CONSUMER_MAP.json"),("integratability",gp+"INTEGRATABILITY_MATRIX.json"),("h1_custody",hp+"BRANCH_COUNT_AND_FUNCTION_CUSTODY_VERIFICATION.json")]:
  d=obj(S6 if name!="h1_custody" else H1,path)
  matrices[name]=summarize_value(d)
 ident=collections.Counter()
 for g in groups:
  for k,v in g.items():
   if isinstance(v,list) and any(word in k for word in ("member","function","row")):
    ident[k]+=1
 grade=collections.Counter();source=collections.Counter()
 for row in challenges:
  for k in ("verdict","grade","classification","challenged_label","challenge_type","row_type","kind","type"):
   if k in row:grade[(k,str(row[k])[:90])]+=1
 def case(k,rows):return {"n":len(rows),"sample_keys":list(rows[0]) if rows else [],"sample_first":{key:summarize_value(val) for key,val in list((rows[0] or {}).items())[:15]}}
 result={"schema":"PYAT_S6_H1_PE_SOURCE_OBJECT_INTAKE@1","refs":{"S6":S6,"H1":H1,"PE":PE},
 "S6":case("s6",groups),"H1":case("h1",challenges),"PE_V2K":case("pe",lineage),
 "original_corrected_ids_count":{k:len(v) for k,v in expected.items()},
 "S6_member_like_field_counts":dict(ident),
 "H1_grade_fields_top":{f"{k}:{v}":n for (k,v),n in grade.most_common(28)},
 "data_shapes":matrices,
 "H1_SESSION_COLLISION_WITH_S1_DECLARED":True,
 "scope":"EXACT_GIT_DATA_ONLY_NOT_INDEPENDENT_SCIENCE_OR_ADOPTION"}
 Path("pyat-s6-h1-receipts").mkdir(exist_ok=True)
 Path("pyat-s6-h1-receipts/INITIAL_RETURN_INDEX.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
 print(json.dumps(result,indent=2)[:19000])
 if len(groups)!=1881 or len(challenges)!=2146 or len(lineage)==0:
  raise SystemExit(2)
if __name__=="__main__":main()
