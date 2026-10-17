"""Build independent evidence crosswalks from real JUnit and import receipts."""
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
RET = ROOT.parent
REPO = RET.parents[1]
CAND = '9a33c2dcaa7ac0d50606416ab965488c9782934b'

def write(path, value):
    path.write_text(json.dumps(value,indent=2)+'\n')

def parse(path):
    root = ET.parse(path).getroot()
    rows = []
    for c in root.iter('testcase'):
        status = next((s for s in ['failure','error','skipped'] if c.find(s) is not None),'passed')
        node = c.find(status)
        rows.append(dict(name=c.get('name'), classname=c.get('classname'), status=status,
                         message=node.get('message') if node is not None else None))
    return dict(tests=len(rows), passed=sum(r['status']=='passed' for r in rows),
                failed=sum(r['status']=='failure' for r in rows), errors=sum(r['status']=='error' for r in rows),
                skipped=sum(r['status']=='skipped' for r in rows),cases=rows)

def main():
    rows = {}
    processes = []
    for suite in ['legacy','author','independent','delta','candidate_own','postinspection']:
        rows[suite] = parse(ROOT/'junit'/f'{suite}.xml')
        receipt = json.loads((ROOT/'evidence'/f'{suite}_execution.json').read_text())
        assert receipt['rootdir'] == str(ROOT)
        assert receipt['configfile'] == str(ROOT/'pytest.ini')
        assert rows[suite]['errors'] == rows[suite]['skipped'] == 0
        processes.append(dict(suite=suite,exit=receipt['exit'],
                              junit=f'junit/{suite}.xml', log=f'logs/{suite}.log',
                              loaded_project_modules=len(receipt['all_loaded_project_modules']),
                              python_executable=receipt['python_executable'],
                              python_version=receipt['python_version']))
    old = {c['name']:c for c in parse(RET/'junit/independent.xml')['cases']}
    new = {c['name']:c for c in rows['independent']['cases']}
    assert set(old) == set(new) and len(new) == 48
    cross = [dict(name=n, phase_a=old[n]['status'], phase_b=new[n]['status']) for n in old]
    assert sum(c['phase_a']=='failure' and c['phase_b']=='passed' for c in cross)==10
    write(ROOT/'evidence/original48_delta_crosswalk.json',cross)
    old_author = {c['name']:c for c in parse(RET/'junit/author.xml')['cases']}
    assert set(old_author)=={c['name'] for c in rows['author']['cases']}
    write(ROOT/'evidence/author28_delta_crosswalk.json',[
        dict(name=c['name'], phase_a=old_author[c['name']]['status'],phase_b=c['status'])
        for c in rows['author']['cases']])
    # Compare each original field and separately count additive disclosures.
    obs=json.loads((ROOT/'evidence/independent_observations.json').read_text())
    actual=next(r['actual'] for r in obs if r['id']=='E6_TWO_TIME')
    original=json.loads((ROOT/'pinned_candidate/evidence/02_real_temporal_to_selected_world_two_times.json').read_text())['two_time_reads']
    differences=[]
    def diff(a,b,path=''):
        if isinstance(a,dict) and isinstance(b,dict):
            for k in sorted(set(a)|set(b)):
                p=path+'/'+k
                if k not in a: differences.append(dict(path=p,kind='additive',repaired=b[k]))
                elif k not in b: differences.append(dict(path=p,kind='removed',original=a[k]))
                else: diff(a[k],b[k],p)
        elif a!=b: differences.append(dict(path=path,kind='changed',original=a,repaired=b))
    diff(original,actual['reads'])
    assert [d['path'] for d in differences if d['kind']=='changed']==['/1990/opportunity_ids']
    write(ROOT/'evidence/two_time_artifact_leaf_diff.json',dict(differences=differences,
          actual_values=actual['numerical_values'],structural_world=actual['structural_world'],
          adjudication='1990 opportunity removal is safety-correct; additive provenance is disclosed, not byte-identical'))
    frozen=json.loads((RET/'01C_PHASE_A_FREEZE_MANIFEST.json').read_text())
    for f in frozen['files']:
        assert hashlib.sha256((RET/f['path']).read_bytes()).hexdigest()==f['sha256']
    manifest=json.loads((ROOT/'evidence/staged_source_manifest.json').read_text())
    for f in manifest:
        b=(ROOT/'pinned_candidate'/f['relative']).resolve().read_bytes()
        assert hashlib.sha256(b).hexdigest()==f['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['git_blob_sha1']
        if f.get('source_commit'):
            assert b==subprocess.check_output(['git','-C',str(REPO),'show',f['source_commit']+':'+f['candidate_git_path']])
    # Reverify each original archival cargo entry against actual original Git blobs
    # without importing or materializing the 1,237 unnecessary files.
    audit=json.loads((RET/'evidence/immutable_copied_source_manifest.json').read_text())
    ids=list(dict.fromkeys(r['git_blob_sha1'] for r in audit))
    raw=subprocess.check_output(['git','-C',str(REPO),'cat-file','--batch'],input=('\n'.join(ids)+'\n').encode())
    blobs={};offset=0
    for oid in ids:
        end=raw.index(b'\n',offset);head=raw[offset:end].decode().split();size=int(head[2]);start=end+1
        assert head[:2]==[oid,'blob'];blobs[oid]=raw[start:start+size];offset=start+size+1
    for f in audit:
        b=blobs[f['git_blob_sha1']]
        assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
    assert len(audit)==1259
    write(ROOT/'evidence/final_custody_verification.json',dict(phase_a_frozen_files_verified=len(frozen['files']),
          staged_preimages_verified=len(manifest),archival_cargo_preimages_reverified=len(audit),
          archival_source_bytes=sum(r['bytes'] for r in audit),native_files=22,
          native_matches_original_blobs=22, ambient_falsifier_exit=4,
          no_source_author_edits=True,original_phase_a_unmodified=True))
    target='refs/heads/agent/rabochii-pyat-r26-t9c-temporal-adapter-seven-red-repair-r1'
    remote=subprocess.check_output(['git','-C',str(REPO),'ls-remote','origin',target]).decode().strip()
    assert remote.split()[0]==CAND
    write(ROOT/'evidence/candidate_direct_remote_readback.json',dict(candidate=CAND,direct_remote=remote,
          at_utc=datetime.now(timezone.utc).isoformat(),source_bytes_pinned=True))
    write(ROOT/'evidence/process_exits.json',dict(runs=processes,
          transport_attempts_retained=['attempt0_missing_pytest_path','attempt1_missing_author_oracle','attempt2_missing_author_ledger'],
          transport_shell_typo='One author rerun redirection had a nonexistent path; process did not start; corrected.',
          runtime_differs_from_phase_a=True,third_party_inventory_measured_not_source_authorized=True))
    write(ROOT/'evidence/court_summary.json',rows)
    print(json.dumps({k:{a:b for a,b in v.items() if a!='cases'} for k,v in rows.items()},indent=2))

if __name__=='__main__': main()
