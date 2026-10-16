from pathlib import Path
import subprocess,hashlib,json
R=Path(__file__).resolve().parents[1];root=R.parents[1];RT=R/'runtime_root';c='3f91dc22d2eb863bc1d2facccfd33e6c05349503';p='WORKER_RETURNS/PYAT-HQ280-PV3-A04T-V2-VERIFIED-INDEPENDENT-JOIN-R1/repro/a04t_join_worker.py'
source_path='WORKER_RETURNS/PYAT-HQ282-P01-V2-DURABLE-CONSUMER-INTEGRATION-R1/repro/a04t_join_worker.py'
data=subprocess.check_output(['git','-c','gc.auto=0','-C',str(root),'show',c+':'+source_path]);blob=subprocess.check_output(['git','-C',str(root),'rev-parse',c+':'+source_path]).decode().strip();assert subprocess.check_output(['git','hash-object','--stdin'],input=data).decode().strip()==blob
out=RT/p;out.parent.mkdir(parents=True,exist_ok=True);assert not out.exists();out.write_bytes(data)
s=json.loads((R/'source_selector.json').read_text());s['files'].append(dict(commit=c,source_path=source_path,staged_path=p,compatibility_alias='Exact retained worker bytes at historical test-selected path; no test or worker code changed',git_blob_sha1=blob,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)));(R/'source_selector.json').write_text(json.dumps(s,indent=2)+'\n');print('EXACT_RETAINED_WORKER',blob)
