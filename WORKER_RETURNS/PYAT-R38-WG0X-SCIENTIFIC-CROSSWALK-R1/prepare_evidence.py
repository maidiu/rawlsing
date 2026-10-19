"""Read pinned source-free Git objects, retain exact row projections and custody."""
import csv, hashlib, io, json, subprocess
from pathlib import Path
R = Path(__file__).resolve().parent
BASE = '68873526efe5a39a0849aa401666ac997870f156'
O35 = '30a2ef61230cea4583945493a1ad489f5ab213c5'
REVIEW = '44eac9021db23267448a6fc151e6bbe8374a868f'
WG0R = '86c13ea6c'
QRA_PIN = 'eede2b8bdb9fcdcc1d4187912f8e00773869c22c'
RP = 'WORKER_RETURNS/PYAT-R37-WG0R-CURRENT35-FRONTIER-SUCCESSION-R1/'
IP = 'WORKER_RETURNS/PYAT-R37-WG0I-CURRENT35-FRONTIER-INDEPENDENT-R1/'
OP = 'WORKER_RETURNS/PYAT-R28-O35E-ORIGINAL-35-ELIGIBILITY-NATIVE-R1/'
QRA = 'data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv'
manifest = []
def read(ref, path, save=None):
    commit = subprocess.check_output(['git','rev-parse',ref+'^{commit}'], text=True).strip()
    blob = subprocess.check_output(['git','rev-parse',commit+':'+path], text=True).strip()
    raw = subprocess.check_output(['git','cat-file','blob',blob])
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == blob
    row = dict(commit=commit, path=path, git_blob_sha1=blob, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
    if save:
        dest=R/save; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(raw); row['retained_path']=save
    manifest.append(row)
    return raw

def dump(path, obj):
    p=R/path; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2)+'\n')

def main():
    p2raw=read(WG0R,RP+'sources/local_archive/Rawlsing_P2_Phase0_Question_Node_Skeleton_v1.csv')
    qraw=read(QRA_PIN,QRA)
    p2=list(csv.DictReader(io.StringIO(p2raw.decode('utf-8-sig'))))
    qra=list(csv.DictReader(io.StringIO(qraw.decode('utf-8-sig'))))
    oracle=json.loads(read(REVIEW,IP+'phase_a/01_PHASE_A_FROZEN_ORACLE.json','sources/inherited_oracle.json'))
    read(REVIEW,IP+'00_INDEPENDENT_VERDICT.md','sources/WG0I_historical_verdict.md')
    read(REVIEW,IP+'phase_b/WG0R_COMPARISON.json','sources/WG0I_historical_comparison.json')
    # Bind O35E origin and direct original QRA, not the WG0R repaired carrier.
    matrix=json.loads(read(O35,OP+'01_35_WAVE_ELIGIBLE_ITEM_OPERATION_MATRIX.json'))
    active=[r for r in qra if r['authority_status']!='EXCLUDED_INACTIVE_WAVE']
    assert len(active)==18259 and len(p2)==18276
    mh={it['question_id']:it for w in matrix['waves'] for it in w['items']}
    assert len(mh)==len(active)
    for q in active:
        m=mh[q['question_id']]
        assert m['governed_row_payload_hash']==q['governed_row_payload_hash']
        assert m['p2_exact_identity_sha256']==(q['p2_exact_identity_sha256'] or None)
    pby={r['exact_identity_sha256']:r for r in p2}
    qby={r['p2_exact_identity_sha256']:r for r in active if r['p2_exact_identity_sha256']}
    assert len(pby)==len(p2) and len(qby)==18250 and set(qby)<=set(pby)
    delta=[dict(csv_record=i,row=r) for i,r in enumerate(p2,1) if r['exact_identity_sha256'] not in qby]
    blocked=[dict(csv_record=i,row=r) for i,r in enumerate(qra,1) if r['authority_status']=='BLOCKED_IDENTITY_OR_AUTHORITY_JOIN']
    dump('sources/p2_only_exact_rows.json',delta)
    dump('sources/qra_blocked_exact_rows.json',blocked)
    # Full source projections retain no host locators. Full preimages stay in shared Git.
    pfields=['question_implementation_id','source_family','wave','source_variable_code','question_id','exact_identity_sha256','canonical_disposition','authority_semantic_role','response_binding_status']
    qfields=['canonical_source','canonical_wave','question_id','var_code','country_code_scope','p2_exact_identity_sha256','governed_row_payload_hash','qsmv2_final_payload_hash','authority_status','relation_use_status_final','manual_response_topology','p2_response_topology','p2_response_binding_status']
    with (R/'sources/p2_identity_projection.jsonl').open('w') as f:
        for i,r in enumerate(p2,1):f.write(json.dumps(dict(csv_record=i,**{k:r[k] for k in pfields}),ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
    with (R/'sources/qra_identity_projection.jsonl').open('w') as f:
        for i,r in enumerate(qra,1):f.write(json.dumps(dict(csv_record=i,**{k:r[k] for k in qfields}),ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n')
    context=[dict(csv_record=i,row={k:r[k] for k in ['question_id','var_code','display_text','country_code_scope','p2_exact_identity_sha256','authority_status','manual_response_topology','p2_response_topology']})
        for i,r in enumerate(qra,1) if (r['canonical_source'],r['canonical_wave']) in {('Afrobarometer','R1'),('Latinobarómetro','1995'),('Latinobarómetro','2024')}]
    dump('sources/three_wave_qra_context.json',context)
    # Small source-free native closure already pinned by WG0R; import provenance
    # binds originals at BASE, never adopts WG0R repair or carrier conclusions.
    tree=subprocess.check_output(['git','ls-tree','-r','--name-only',WG0R,RP+'sources/native/'],text=True).splitlines()
    for path in tree:
        dest=path.split('/sources/native/',1)[1]
        read(BASE,dest,'native/'+dest)
    for path,name in [('data/ddm_build_copy/build_determinicity_repository_v550.py','v550_worklist.py'),('data/ddm_build_copy/compile_v550j_joint_response_patterns.py','v550j_patterns.py')]:
        read(BASE,path,'sources/'+name)
    read(BASE,'PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/AUTOMATED_WORKLOAD_CONSTRUCTION_CRITICAL_GATE.md','sources/AUTOMATED_WORKLOAD_CONSTRUCTION_CRITICAL_GATE.md')
    dump('sources/o35e_scope.json',dict(census=matrix['census'],operation_requirements=matrix['operation_requirements'],waves=[{k:w[k] for k in ['atlas_id','canonical_source_family','canonical_wave','qra_row_count','dataset_manifest_identity']} for w in matrix['waves']]))
    dump('evidence/source_manifest.json',manifest)
    projection_files=sorted((R/'sources').glob('*projection.jsonl'))+sorted((R/'sources').glob('*exact_rows.json'))+[R/'sources/o35e_scope.json']
    dump('evidence/projection_digests.json',{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in projection_files})
    print(json.dumps(dict(p2=len(p2),qra=len(qra),active=len(active),common=len(qby),p2_only=len(delta),blocked=len(blocked),native_files=len(tree),source_objects=len(manifest))))
if __name__=='__main__': main()
