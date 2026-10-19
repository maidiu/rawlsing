"""Trace comparison, observed imports/reads, and independent cold-interpreter replay."""
from pathlib import Path
import gzip,hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parent;F=R/'frozen';C=F/'reconstructed/clr3'
sys.path.insert(0,str(F/'repair_r1/candidate'))
reads=set()
def hook(name,args):
    if name=='open' and isinstance(args[0],(str,bytes)):
        p=Path(os.fsdecode(args[0]))
        if p.suffix in ('.yaml','.yml') and p.exists():reads.add(p.resolve())
sys.addaudithook(hook)
import recursive_court as c
assert Path(c.__file__).resolve()==F/'repair_r1/candidate/recursive_court.py'
traces={w:c.run_trajectory(w) for w in c.r1_world.WORK_OUTCOMES}
traces['alternate_canon']=c.run_trajectory('ROUTINE',location='garage_shelf',variant='alternate')
raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
expected=json.loads(gzip.decompress((C/'evidence/full_trajectories.json.gz').read_bytes()))
assert json.loads(raw)==expected,'Whole trajectory differs'
inventory={x['path']:x for x in json.loads((C/'sources/legacy_source_inventory.json').read_text())['files']}
def record(path):
    b=path.read_bytes()
    return dict(module_file=str(path.relative_to(R)),sha256=hashlib.sha256(b).hexdigest(),blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest())
modules=[]
for name,module in sorted(sys.modules.items()):
    if name=='recursive_court' or name=='r1_world' or name=='v3' or name.startswith('v3.'):
        p=Path(module.__file__).resolve();row=record(p)
        if name=='v3' or name.startswith('v3.'):
            assert p.is_relative_to(C/'sources/legacy')
            assert row['sha256']==inventory[str(p.relative_to(C/'sources/legacy'))]['sha256']
        elif name=='r1_world':assert p==C/'sources/r1_world.py'
        modules.append(dict(module=name,**row))
yaml=[]
for p in sorted(reads):
    assert p.is_relative_to(C/'sources/legacy')
    row=record(p);assert row['sha256']==inventory[str(p.relative_to(C/'sources/legacy'))]['sha256'];yaml.append(row)
cold=[]
code="import json,recursive_court as c; print(json.dumps({'module_file':c.__file__, 'hashes':{w:c.run_trajectory(w)['trace_hash'] for w in c.r1_world.WORK_OUTCOMES}},sort_keys=True))"
for seed in (0,1,71,123):
    cmd=[sys.executable,'-c',code]
    p=subprocess.run(cmd,cwd=F/'repair_r1/candidate',env={**os.environ,'PYTHONHASHSEED':str(seed),'PYTHONDONTWRITEBYTECODE':'1'},text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    assert p.returncode==0,p.stdout
    output=json.loads(p.stdout);assert output['module_file']==str(Path(c.__file__).resolve())
    assert output['hashes']=={w:traces[w]['trace_hash'] for w in c.r1_world.WORK_OUTCOMES}
    output['module_file']=str(Path(output['module_file']).relative_to(R))
    cold.append(dict(hashseed=seed,exit_code=p.returncode,command=['RETURN/.venv/bin/python','-c',code],cwd='frozen/repair_r1/candidate',**output))
payload=gzip.compress(raw,mtime=0);(R/'evidence/trajectories.json.gz').write_bytes(payload)
summary=dict(records=4,full_record_equality=True,trace_hashes={w:v['trace_hash'] for w,v in traces.items()},modules=modules,yaml_reads=yaml,cold=cold,trajectories_sha256=hashlib.sha256(payload).hexdigest(),legacy_modules=sum(x['module']=='v3' or x['module'].startswith('v3.') for x in modules))
(R/'evidence/replay_imports.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ('records','full_record_equality','trace_hashes','legacy_modules')}));print('YAML reads',len(yaml),'cold processes',len(cold))
