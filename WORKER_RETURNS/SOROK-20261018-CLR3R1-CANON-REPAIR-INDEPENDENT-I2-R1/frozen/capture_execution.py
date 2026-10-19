"""Instrument exact code reads/imports, without changing candidate bytes."""
import builtins,gzip,hashlib,io,json,sys
from pathlib import Path
from reconstruct import ROOT

CLR=ROOT/'reconstructed/clr3'
sys.path.insert(0,str(CLR))
reads=set()
orig_open=builtins.open
orig_io_open=io.open
def record(file):
    if isinstance(file,(str,bytes,Path)):
        p=Path(file).resolve()
        if p.is_relative_to(CLR/'sources/legacy'):reads.add(str(p.relative_to(CLR/'sources/legacy')))
def watched_open(file,*a,**k):record(file);return orig_open(file,*a,**k)
def watched_io_open(file,*a,**k):record(file);return orig_io_open(file,*a,**k)
builtins.open=watched_open
io.open=watched_io_open
import recursive_court as c
traces={w:c.run_trajectory(w) for w in ('HOURS_CUT','ROUTINE','RAISE_WITH_OVERTIME')}
traces['alternate_canon']=c.run_trajectory('ROUTINE',location='garage_shelf',variant='alternate')
builtins.open=orig_open
io.open=orig_io_open
inv={r['path']:r for r in json.loads((CLR/'sources/legacy_source_inventory.json').read_text())['files']}
modules=[]
for name,module in sorted(sys.modules.items()):
    if name=='v3' or name.startswith('v3.') or name in {'recursive_court','r1_world'}:
        path=Path(module.__file__).resolve()
        assert path.is_relative_to(CLR),('IMPORT_MISMATCH',name)
        data=path.read_bytes()
        legacy_path=str(path.relative_to(CLR/'sources/legacy')) if path.is_relative_to(CLR/'sources/legacy') else None
        if legacy_path:
            assert legacy_path in inv and hashlib.sha256(data).hexdigest()==inv[legacy_path]['sha256']
        modules.append(dict(module=name,verified_module_file='<I2_RETURN>/'+str(path.relative_to(ROOT)),local_path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(data).hexdigest(),legacy_inventory_path=legacy_path))
for path in reads:assert path in inv,('UNPINNED_FILE_READ',path)
raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
compressed=gzip.compress(raw,mtime=0)
(ROOT/'evidence/reproduced_trajectories.json.gz').write_bytes(compressed)
author=json.loads(gzip.decompress((CLR/'evidence/full_trajectories.json.gz').read_bytes()))
roundtripped=json.loads(raw)
comparison={label:dict(reproduced_trace_hash=t['trace_hash'],author_trace_hash=author[label]['trace_hash'],full_record_equal=roundtripped[label]==author[label],final_age=t['final_state']['age'],final_social_support=t['final_state']['capacity']['social_support'],father_minutes=t['resolved']['father_response']['available_minutes'],later_target=t['later']['target_location']) for label,t in traces.items()}
assert all(r['full_record_equal'] for r in comparison.values())
report=dict(modules=modules,legacy_modules_count=sum(r['legacy_inventory_path'] is not None for r in modules),opened_legacy_files=sorted(reads),unopened_inventory_files=sorted(set(inv)-reads-{r['legacy_inventory_path'] for r in modules}),source_closure_grade='ALL_OBSERVED_V3_IMPORTS_AND_CONFIG_READS_MATCH_65_FILE_PUBLISHED_CLOSURE; not all 65 files are imported',trajectory_comparison=comparison,uncompressed_bytes=len(raw),sha256=hashlib.sha256(compressed).hexdigest())
(ROOT/'evidence/import_and_replay_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(legacy_modules=report['legacy_modules_count'],config_reads=len(reads),trajectory_comparison=comparison)))
