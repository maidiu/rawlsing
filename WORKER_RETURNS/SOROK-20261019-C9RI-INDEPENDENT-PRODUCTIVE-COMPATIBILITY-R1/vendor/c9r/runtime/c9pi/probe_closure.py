from pathlib import Path
import hashlib,importlib,json,sys
R=Path(__file__).resolve().parent;ROOT=R/'runs/runtime';P='WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1'
sys.path[:0]=[str(ROOT),str(ROOT/P)]
import candidate
rows=[]
mods=[importlib.import_module('candidate'+('.'+p.stem if p.stem!='__init__' else '')) for p in sorted((ROOT/P/'candidate').glob('*.py'))]
mods += [importlib.import_module('rawlsing_next.'+p.stem) for p in sorted((ROOT/'rawlsing_next').glob('*.py'))]
for mod in mods:
 p=Path(mod.__file__).resolve();rel=p.relative_to(ROOT).as_posix();b=p.read_bytes()
 expected=(R/'frozen/c9p'/p.relative_to(ROOT/P)) if rel.startswith(P+'/') else (R/'frozen/native'/rel)
 assert b==expected.read_bytes()
 rows.append(dict(module=mod.__name__,runtime_file_relative=rel,observed_absolute_file_sha256=hashlib.sha256(str(p).encode()).hexdigest(),sha256=hashlib.sha256(b).hexdigest(),blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),exact_frozen_preimage=True))
for row in json.loads((R/'custody/source_preimages.json').read_text()):
 if row['staged'].startswith('frozen/c9p/'):
  p=ROOT/P/row['staged'][len('frozen/c9p/'):];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
assert len(rows)==16
(R/'evidence/actual_imports.json').write_text(json.dumps(rows,indent=2)+'\n')
print('16 exact runtime module files verified; 13 candidate (12 operative + __init__), 3 native; unchanged author tests/receipts')
