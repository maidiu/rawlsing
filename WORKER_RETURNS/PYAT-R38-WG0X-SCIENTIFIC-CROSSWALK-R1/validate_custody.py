"""Verify retained code bytes and exact projected rows against pinned Git objects."""
import csv,hashlib,io,json,subprocess,sys
from pathlib import Path
csv.field_size_limit(sys.maxsize)
R=Path(__file__).resolve().parent

def git_blob(row):
    b=subprocess.check_output(['git','cat-file','blob',row['git_blob_sha1']])
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
    assert hashlib.sha256(b).hexdigest()==row['sha256'] and len(b)==row['bytes']
    return b

def main():
    manifest=json.loads((R/'evidence/source_manifest.json').read_text())
    for r in manifest:
        if r.get('retained_path'):
            b=(R/r['retained_path']).read_bytes()
            assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['retained_path']
    p2m=next(r for r in manifest if r['path'].endswith('Rawlsing_P2_Phase0_Question_Node_Skeleton_v1.csv'))
    qm=next(r for r in manifest if r['path'].endswith('QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv'))
    assert p2m['sha256']=='d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6'
    full={}
    for name,meta in [('p2',p2m),('qra',qm)]:
        rows=list(csv.DictReader(io.StringIO(git_blob(meta).decode('utf-8-sig'))));full[name]=rows
        projection=[json.loads(x) for x in (R/f'sources/{name}_identity_projection.jsonl').read_text().splitlines()]
        assert len(rows)==len(projection)
        for p in projection:
            i=p['csv_record'];assert {k:v for k,v in p.items() if k!='csv_record'}=={k:rows[i-1][k] for k in p if k!='csv_record'}
    for name in ['p2','qra']:
        fname='p2_only_exact_rows.json' if name=='p2' else 'qra_blocked_exact_rows.json'
        for p in json.loads((R/'sources'/fname).read_text()):assert p['row']==full[name][p['csv_record']-1]
    owners=json.loads((R/'sources/owner_row_projections.json').read_text())
    matched={}
    for label,match in [('register_A','/REGISTER_A/'),('register_B','/REGISTER_B/'),('v525b_semantic','/v525b/questions_master_semantic'),('v525b_drivers','/v525b/questions_master_drivers'),('d62_driver_provenance_only','/d62/questions_master_drivers')]:
        meta=next(r for r in manifest if match in r['path'])
        rows=list(csv.DictReader(io.StringIO(git_blob(meta).decode('utf-8-sig'))))
        assert len(rows)==owners[label]['total_rows']
        for p in owners[label]['selected_records']:
            row=rows[p['csv_record']-1]
            assert hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':')).encode()).hexdigest()==p['row_sha256']
            assert p['row']=={k:row[k] for k in p['row']}
        matched[label]=len(owners[label]['selected_records'])
    out=dict(status='PINNED_PREIMAGES_AND_EXACT_PROJECTION_ROWS_VERIFIED',source_objects=len(manifest),retained_preimages=sum(bool(x.get('retained_path')) for x in manifest),p2_projection=len(full['p2']),qra_projection=len(full['qra']),owner_row_records=matched,grade='MECHANICAL_CUSTODY_NOT_SEMANTIC_OR_REPAIR_ACCEPTANCE')
    (R/'evidence/custody_verification.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
