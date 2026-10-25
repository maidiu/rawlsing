"""S49 evidence: actual root hold, controlled B producer, tests and manifest."""
from __future__ import annotations
import hashlib, json, os, shutil, subprocess, sys, xml.etree.ElementTree as ET
from pathlib import Path
RET=Path(__file__).resolve().parent; EVID=RET/"evidence"; JUNIT=RET/"junit"; LOGS=RET/"logs"
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE="1",PYTHONPATH=str(RET))
for p in (str(RET),str(RET/"tests")):
    if p not in sys.path: sys.path.insert(0,p)
from s49.bootstrap import CUTS, install, roots
install()
S48_RETURN=Path(roots()["s48_return"])
S49_FILES=[".gitignore","00_RETURN.md","run_s49.py","run_s49_evidence.py","s49/__init__.py","s49/bootstrap.py","s49/errors.py","s49/actor.py","s49/session.py","tests/conftest.py","tests/test_s49.py"]
S48_FILES=["s48/__init__.py","s48/bootstrap.py","s48/errors.py","s48/product.py","s48/session.py","s48/sources.py","tests/conftest.py","tests/test_s48_one_call.py"]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(*a): return subprocess.run(["git",*a],cwd=str(RET),capture_output=True,text=True,check=True).stdout.strip()
def write(p,v): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n")
def counts(x):
    r=ET.parse(x).getroot(); suites=[r] if r.tag=="testsuite" else list(r)
    t=sum(int(s.attrib.get("tests",0)) for s in suites); f=sum(int(s.attrib.get("failures",0)) for s in suites); e=sum(int(s.attrib.get("errors",0)) for s in suites); sk=sum(int(s.attrib.get("skipped",0)) for s in suites)
    return {"tests":t,"PASS":t-f-e-sk,"RED":f,"ERROR":e,"SKIP":sk}
def manifest():
    reused=[]
    for rel in S48_FILES:
        local=S48_RETURN/rel; pinned=git("rev-parse",f"{CUTS['s48']}:WORKER_RETURNS/SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1/{rel}"); blob=git("hash-object",str(local))
        reused.append({"path":rel,"pinned":pinned,"local":blob,"exact":pinned==blob,"sha256":sha(local)})
    local=[{"path":rel,"sha256":sha(RET/rel),"git_blob_sha1":git("hash-object",str(RET/rel))} for rel in S49_FILES if (RET/rel).exists()]
    s42 = Path(roots()["s42_return"]) / "s42/session.py"
    return {"schema":"SOROK_S49_SOURCE_MANIFEST@1","roots":roots(),"cuts":dict(CUTS),"s48_reused":{"rows":reused,"all_exact":all(r["exact"] for r in reused)},"s49_local":local,"s42_normal_consumer_seam":{"path":"WORKER_RETURNS/SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1/s42/session.py","sha256":sha(s42),"git_blob_sha1":git("hash-object",str(s42)),"reason":"minimal normal admit hook preserves S49 chain before C8"},"native_grants":{"actor":False,"rule":False,"source":False,"human":False,"c8":False,"c9":False,"c12":False}}
def main():
    EVID.mkdir(exist_ok=True); JUNIT.mkdir(exist_ok=True); LOGS.mkdir(exist_ok=True)
    entry=subprocess.run([sys.executable,"-B","run_s49.py"],cwd=str(RET),env=ENV,capture_output=True,text=True)
    (LOGS/"entrypoint.log").write_text(entry.stdout+entry.stderr)
    if entry.returncode!=0: raise RuntimeError("S49_ENTRYPOINT_FAILED:"+entry.stderr)
    (EVID/"entrypoint.json").write_text(entry.stdout)
    xml=JUNIT/"s49_full.xml"; tmp=LOGS/"tmp"; tmp.mkdir(exist_ok=True)
    proc=subprocess.run([sys.executable,"-B","-m","pytest","-q","-p","no:cacheprovider",f"--junitxml={xml}","tests"],cwd=str(RET),env=dict(ENV,TMPDIR=str(tmp)),capture_output=True,text=True)
    (LOGS/"s49_full.log").write_text(proc.stdout+proc.stderr); c=counts(xml); shutil.rmtree(tmp,ignore_errors=True)
    write(EVID/"test_run.json",{"schema":"SOROK_S49_TEST_RUN@1","s49":{"exit":proc.returncode,"junit":str(xml.relative_to(RET)),"counts":c}})
    write(EVID/"source_manifest.json",manifest())
    print(json.dumps({"entrypoint":entry.returncode,"tests":c},sort_keys=True))
    return 0 if proc.returncode==0 else 1
if __name__=="__main__": raise SystemExit(main())
