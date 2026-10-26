"""S50 recovered V3 source identity, execution, tests and evidence."""
from __future__ import annotations
import hashlib, json, os, shutil, subprocess, sys, tempfile, xml.etree.ElementTree as ET
from pathlib import Path
RET=Path(__file__).resolve().parent; EVID=RET/"evidence"; JUNIT=RET/"junit"; LOGS=RET/"logs"
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",PYTHONPATH=str(RET))
S49=Path("/Users/matthewsmith/.codex/worktrees/10f2/Rawlsing/.local-logs/sorok-s36/worker/WORKER_RETURNS/SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1")
for p in (str(RET),str(RET/"tests")):
    if p not in sys.path: sys.path.insert(0,p)
from s50.bootstrap import CUTS, install, roots
install()
from s50.recovery import verify_source
S50_FILES=["00_RETURN.md","run_s50.py","run_s50_evidence.py","s50/__init__.py","s50/bootstrap.py","s50/yaml_compat.py","s50/recovery.py","s50/session.py","tests/conftest.py","tests/test_s50.py"]
S49_FILES=["s49/__init__.py","s49/bootstrap.py","s49/errors.py","s49/actor.py","s49/session.py","tests/test_s49.py"]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(*a): return subprocess.run(["git",*a],cwd=str(RET),capture_output=True,text=True,check=True).stdout.strip()
def write(p,v): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n")
def counts(x):
 r=ET.parse(x).getroot(); suites=[r] if r.tag=="testsuite" else list(r)
 t=sum(int(s.attrib.get("tests",0)) for s in suites); f=sum(int(s.attrib.get("failures",0)) for s in suites); e=sum(int(s.attrib.get("errors",0)) for s in suites); sk=sum(int(s.attrib.get("skipped",0)) for s in suites)
 return {"tests":t,"PASS":t-f-e-sk,"RED":f,"ERROR":e,"SKIP":sk}
def manifest(entry):
 src=verify_source(); reused=[]
 for rel in S49_FILES:
  local=S49/rel
  pinned=git("rev-parse",f"{CUTS['s49']}:WORKER_RETURNS/SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1/{rel}")
  blob=git("hash-object",str(local)); reused.append({"path":rel,"pinned":pinned,"local":blob,"exact":pinned==blob,"sha256":sha(local)})
 local=[{"path":rel,"sha256":sha(RET/rel),"git_blob_sha1":git("hash-object",str(RET/rel))} for rel in S50_FILES if (RET/rel).exists()]
 return {"schema":"SOROK_S50_SOURCE_MANIFEST@1","roots":roots(),"cuts":dict(CUTS),"source_identity":src,"s49_reused":{"rows":reused,"all_exact":all(r["exact"] for r in reused)},"s50_local":local,"dependency_runtime":{"yaml":"system Ruby Psych -> yaml.safe_load JSON bridge","packages_installed":False,"network":False},"native_grants":{"actor":False,"rule":False,"source":False,"human":False,"c8":False,"c9":False,"c12":False}}
def main():
 EVID.mkdir(exist_ok=True); JUNIT.mkdir(exist_ok=True); LOGS.mkdir(exist_ok=True)
 entry=subprocess.run([sys.executable,"-B","run_s50.py"],cwd=str(RET),env=ENV,capture_output=True,text=True)
 (LOGS/"entrypoint.log").write_text(entry.stdout+entry.stderr)
 if entry.returncode!=0: raise RuntimeError("S50_ENTRYPOINT_FAILED:"+entry.stderr)
 (EVID/"entrypoint.json").write_text(entry.stdout)
 xml=JUNIT/"s50_full.xml"; tmp=LOGS/"tmp"; tmp.mkdir(exist_ok=True)
 proc=subprocess.run([sys.executable,"-B","-m","pytest","-q","-p","no:cacheprovider",f"--junitxml={xml}","tests"],cwd=str(RET),env=dict(ENV,TMPDIR=str(tmp)),capture_output=True,text=True)
 (LOGS/"s50_full.log").write_text(proc.stdout+proc.stderr); c=counts(xml); shutil.rmtree(tmp,ignore_errors=True)
 write(EVID/"test_run.json",{"schema":"SOROK_S50_TEST_RUN@1","s50":{"exit":proc.returncode,"junit":str(xml.relative_to(RET)),"counts":c}})
 write(EVID/"source_manifest.json",manifest(entry))
 print(json.dumps({"entrypoint":entry.returncode,"tests":c},sort_keys=True))
 return 0 if proc.returncode==0 else 1
if __name__=="__main__": raise SystemExit(main())
