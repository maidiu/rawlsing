"""Load only exact materialized source bytes; no mutable branch imports."""
from pathlib import Path
import hashlib,importlib.util,json,sys
ROOT=Path(__file__).resolve().parent
RUNTIME=ROOT/'.runtime'
def load(name,path):
 rows=json.loads((ROOT/'source_manifest.json').read_text())
 rel=str(path.relative_to(ROOT));row=next(x for x in rows if x.get('local')==rel)
 assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],rel
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec)
 sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
sys.path.insert(0,str(RUNTIME/'b2'))
b2=load('b3_fixed_b2',RUNTIME/'b2/bridge.py')
m2=load('b3_frozen_m2',RUNTIME/'m2/kernel.py')
def identities():
 return [dict(module=m.__name__,relative_file=str(Path(m.__file__).relative_to(ROOT)),sha256=hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()) for m in (b2,b2.b1,b2.p1,m2)]
