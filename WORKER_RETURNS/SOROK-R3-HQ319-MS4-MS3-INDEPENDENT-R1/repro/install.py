"""Select pinned wrapper only; native modules and original tests are immutable."""
from stage import R,git,blob
import sys,json
RT=R/'staging/ms3/staging/ms2/staging/ms1/runtime'
mode=sys.argv[1];assert mode in ('old','ms3')
sha='d40cc32ecec8f681dcced6a482b6438a86080899' if mode=='old' else '48200cf0b8e9b69ce27bf0151cb43fde5133322f'
prefix='WORKER_RETURNS/SOROK-R3-HQ316-MS1-SERIAL-MEMORY-BELIEF-FEASIBILITY-R1/runtime' if mode=='old' else 'WORKER_RETURNS/SOROK-R3-HQ318-MS3-MS2-PROVENANCE-REPAIR-R1/candidate'
rows=[]
for name in (['ms1_serial.py'] if mode=='old' else ['ms1_serial.py','ms3_native_custody.py']):
    path=prefix+'/'+name;b=git('show',sha+':'+path);assert blob(b)==git('rev-parse',sha+':'+path).decode().strip();(RT/name).write_bytes(b)
    rows.append(dict(commit=sha,path=path,local=str((RT/name).relative_to(R)),blob_sha1=blob(b)))
(R/'evidence').mkdir(exist_ok=True);(R/'evidence'/('installation_'+mode+'.json')).write_text(json.dumps(rows,indent=2)+'\n')
print(mode,'pinned wrapper installed; original native modules unchanged')
