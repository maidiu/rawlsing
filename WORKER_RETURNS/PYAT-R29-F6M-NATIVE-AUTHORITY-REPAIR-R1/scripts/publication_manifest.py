"""List and stage only the authorized return, preserving ignored inherited evidence."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
EXCLUDE={'.environment-marker'}
def eligible(p):
 rel=p.relative_to(ROOT)
 return (p.is_file() and not p.is_symlink() and not any(x in ('runtime','__pycache__','.pytest_cache') for x in rel.parts)
         and p.name not in EXCLUDE and p.suffix!='.pyc')
def main():
 paths=sorted(p for p in ROOT.rglob('*') if eligible(p))
 manifest=ROOT/'custody/publication_manifest.json'
 entries=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size=p.stat().st_size) for p in paths if p!=manifest]
 manifest.write_text(json.dumps(dict(schema='F6M_PUBLICATION_MANIFEST@1',self_excluded=True,files=entries),indent=2)+'\n')
 paths=sorted(p for p in ROOT.rglob('*') if eligible(p))
 if '--stage' in sys.argv:
  repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip())
  names=b''.join(str(p.relative_to(repo)).encode()+bytes([0]) for p in paths)
  subprocess.run(['git','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=names,cwd=repo,check=True)
 print('Publication files:',len(paths),'manifest entries:',len(entries))
if __name__=='__main__':main()
