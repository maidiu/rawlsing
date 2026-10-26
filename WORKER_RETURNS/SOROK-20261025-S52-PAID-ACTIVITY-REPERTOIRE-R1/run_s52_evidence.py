"""S52 focused tests, entrypoint and source manifest; no provider call."""
from __future__ import annotations
import hashlib,json,os,shutil,subprocess,sys,xml.etree.ElementTree as ET
from pathlib import Path
RET=Path(__file__).resolve().parent; EVID=RET/"evidence"; JUNIT=RET/"junit"; LOGS=RET/"logs"
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",PYTHONPATH=str(RET))
for p in (str(RET),str(RET/"tests")):
 if p not in sys.path:sys.path.insert(0,p)
from s52.bootstrap import install,roots
install()
FILES=["00_RETURN.md","run_s52.py","run_s52_evidence.py","s52/__init__.py","s52/bootstrap.py","s52/session.py","s52/performer.py","tests/conftest.py","tests/test_s52.py"]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n")
def counts(x):
 r=ET.parse(x).getroot(); su=[r] if r.tag=="testsuite" else list(r); t=sum(int(s.attrib.get("tests",0)) for s in su);f=sum(int(s.attrib.get("failures",0)) for s in su);e=sum(int(s.attrib.get("errors",0)) for s in su);sk=sum(int(s.attrib.get("skipped",0)) for s in su);return {"tests":t,"PASS":t-f-e-sk,"RED":f,"ERROR":e,"SKIP":sk}
def seam(rel):return {"path":rel,"sha256":sha(Path("/Users/matthewsmith/.codex/worktrees/10f2/Rawlsing/.local-logs/sorok-s36/worker")/rel)}
def manifest():
 rows=[]
 for rel in FILES:
  p=RET/rel
  rows.append({"path":rel,"sha256":sha(p),"git_blob_sha1":subprocess.run(["git","hash-object",str(p)],cwd=str(RET),capture_output=True,text=True,check=True).stdout.strip()})
 return {"schema":"SOROK_S52_SOURCE_MANIFEST@1","roots":roots(),"s51_base":"2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65","s49_base":"6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43","source_files":rows,"seams":{"s39_model":seam("WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1/s39/model.py"),"s49_actor":seam("WORKER_RETURNS/SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1/s49/actor.py"),"s49_session":seam("WORKER_RETURNS/SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1/s49/session.py"),"s51_session":seam("WORKER_RETURNS/SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1/s51/session.py")},"native_grants":{"actor":False,"rule":False,"source":False,"human":False,"c8":False,"c9":False,"c12":False}}
def main():
 EVID.mkdir(exist_ok=True);JUNIT.mkdir(exist_ok=True);LOGS.mkdir(exist_ok=True)
 entry=subprocess.run([sys.executable,"-B","run_s52.py"],cwd=str(RET),env=ENV,capture_output=True,text=True);(LOGS/"entrypoint.log").write_text(entry.stdout+entry.stderr)
 if entry.returncode!=0:raise RuntimeError("S52_ENTRYPOINT_FAILED:"+entry.stderr)
 (EVID/"entrypoint.json").write_text(entry.stdout)
 xml=JUNIT/"s52_full.xml";tmp=LOGS/"tmp";tmp.mkdir(exist_ok=True)
 proc=subprocess.run([sys.executable,"-B","-m","pytest","-q","-p","no:cacheprovider",f"--junitxml={xml}","tests"],cwd=str(RET),env=dict(ENV,TMPDIR=str(tmp)),capture_output=True,text=True)
 (LOGS/"s52_full.log").write_text(proc.stdout+proc.stderr);c=counts(xml);shutil.rmtree(tmp,ignore_errors=True)
 write(EVID/"test_run.json",{"schema":"SOROK_S52_TEST_RUN@1","s52":{"exit":proc.returncode,"junit":str(xml.relative_to(RET)),"counts":c}})
 write(EVID/"source_manifest.json",manifest())
 print(json.dumps({"entrypoint":entry.returncode,"tests":c},sort_keys=True));return 0 if proc.returncode==0 else 1
if __name__=="__main__":raise SystemExit(main())
