"""Portable custody for the explicitly versioned candidate, independent of path suffix."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()
def candidate_blob():return json.loads((ROOT/'custody/candidate.json').read_text())['producer_git_blob']
def verify_import(module):
 p=Path(module.__file__).resolve()
 return (p.is_file() and blob(p.read_bytes())==candidate_blob()
         and module.IMPLEMENTATION_VERSION=='F6M_NATIVE_DECISION_ADMISSION_REPAIR@1'
         and module.ORIGINAL_PRODUCER_BLOB=='fc5e37fa5b2f0eb689593b42d95479d1327cb94c')
