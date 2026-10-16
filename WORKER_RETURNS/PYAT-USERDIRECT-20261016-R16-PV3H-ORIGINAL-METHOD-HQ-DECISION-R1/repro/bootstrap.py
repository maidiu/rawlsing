from pathlib import Path
import sys,os,json,hashlib
R=Path(__file__).resolve().parents[1];C=R/'runtime/court';RT=C/'runtime_root'
NATIVE=json.loads((R/'native_74_source_manifest.json').read_text())['files']
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def reattest():
 for row in NATIVE:
  p=RT/row['staged_path']
  if not p.is_file():raise ValueError('MISSING_NATIVE_SOURCE_ATTESTATION:'+row['staged_path'])
  if blob(p.read_bytes())!=row['git_blob_sha1']:raise ValueError('CHANGED_NATIVE_SOURCE_ATTESTATION:'+row['staged_path'])
 return len(NATIVE)
reattest()
sys.path[:0]=[str(C/'repro'),str(RT),str(RT/'candidate/repro'),str(C/'frozen_pv2i/repro')]
os.environ.update(PV2_RUNTIME_ROOT=str(RT),PV_RETURN=str(RT/'prior_PV'))
