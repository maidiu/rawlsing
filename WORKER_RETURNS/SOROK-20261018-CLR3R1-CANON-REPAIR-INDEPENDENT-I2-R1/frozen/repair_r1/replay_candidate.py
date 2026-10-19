"""Verify candidate binding, frozen imports and unchanged valid trajectories."""
import gzip,hashlib,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REVIEW=ROOT.parent
sys.path.insert(0,str(ROOT/'candidate'))
import recursive_court as c
assert Path(c.__file__).resolve()==ROOT/'candidate/recursive_court.py'

traces={w:c.run_trajectory(w) for w in ('HOURS_CUT','ROUTINE','RAISE_WITH_OVERTIME')}
traces['alternate_canon']=c.run_trajectory('ROUTINE',location='garage_shelf',variant='alternate')
raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
baseline=json.loads(gzip.decompress((REVIEW/'reconstructed/clr3/evidence/full_trajectories.json.gz').read_bytes()))
assert json.loads(raw)==baseline,'Valid trajectory changed'
inv={r['path']:r for r in json.loads((REVIEW/'reconstructed/clr3/sources/legacy_source_inventory.json').read_text())['files']}
modules=[]
for name,module in sorted(sys.modules.items()):
    if name=='v3' or name.startswith('v3.') or name=='r1_world':
        path=Path(module.__file__).resolve()
        assert path.is_relative_to(REVIEW/'reconstructed/clr3/sources'),('IMPORT_MISMATCH',name)
        data=path.read_bytes()
        if name=='r1_world':
            assert hashlib.sha256(data).hexdigest()=='3b6d0995930664cb03969a0108214b95e67f3cb4ab04391cfdf27aa5059ad4aa'
        else:
            rel=str(path.relative_to(REVIEW/'reconstructed/clr3/sources/legacy'))
            assert hashlib.sha256(data).hexdigest()==inv[rel]['sha256']
        modules.append(dict(module=name,verified_import_path='<I2_RETURN>/'+str(path.relative_to(REVIEW)),sha256=hashlib.sha256(data).hexdigest()))
payload=gzip.compress(raw,mtime=0)
(ROOT/'evidence/valid_trajectories.json.gz').write_bytes(payload)
(ROOT/'evidence/replay_and_imports.json').write_text(json.dumps(dict(candidate_sha256=hashlib.sha256(Path(c.__file__).read_bytes()).hexdigest(),full_record_equality=True,records=len(traces),trace_hashes={k:v['trace_hash'] for k,v in traces.items()},frozen_imports=modules,legacy_modules=sum(m['module']=='v3' or m['module'].startswith('v3.') for m in modules),trajectories_sha256=hashlib.sha256(payload).hexdigest()),indent=2)+'\n')
print(json.dumps({k:v['trace_hash'] for k,v in traces.items()},sort_keys=True))
