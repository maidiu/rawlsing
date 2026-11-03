"""Focused independent recheck of N10W clock repair c75b464ab4."""
from __future__ import annotations
import copy, json, sys, hashlib, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
REPO = REVIEW.parents[1]
OLD = REVIEW / 'evidence'
CANDIDATE = Path('/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join')
REPAIR = CANDIDATE / 'WORKER_RETURNS/PDEV01-N10W-JOIN/repair'
KEY = 'base/TEST_CURRENT/budget5'
sys.dont_write_bytecode = True
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPAIR))
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_universal_world_binding import JoinedWorldField, select_joined_world_view
from rawlsing_next.tests.test_universal_world_binding import _joined_request
from guarded_receiver import (
    W41_ARTIFACT_PATH, W41_ARTIFACT_SHA256, W41_COMMIT, _load_w41_worlds,
    guarded_select_joined_world_view,
)


def sha(b): return hashlib.sha256(b).hexdigest()
def load(n): return json.loads((OLD/n).read_text())
def fields(rec,key):
    rules=rec['p41_joined_receipts'][key]['n9_world']['rules']
    return (JoinedWorldField('training_access',rules['training_access']['value']),
            JoinedWorldField('civil_sanction',rules['civil_sanction']['value']))
def guard(rec,key=KEY,fields_=None,**changes):
    v=guarded_select_joined_world_view(_joined_request(rec,key,fields=fields(rec,key) if fields_ is None else fields_,**changes))
    return {'state':v.state,'reason_code':v.reason_code,'view_key':v.view_key,'view_hash':v.view_hash,
            'families':None if v.consumer_values_read is None else v.consumer_values_read.get('families'),
            'n9_clock':None if v.consumer_values_read is None else v.consumer_values_read.get('n9_clock'),
            'n9_currentness':None if v.consumer_values_read is None else v.consumer_values_read.get('n9_currentness')}
def p41(rec): return rec['p41_joined_receipts'][KEY]
def mutate(rec,fn):
    d=copy.deepcopy(rec); p=p41(d); fn(p); p.pop('content_hash',None); p['content_hash']=semantic_hash(p); return d
def unmutated(rec,fn):
    d=copy.deepcopy(rec); fn(p41(d)); return d

def main():
    a=load('J42_RECEIPTS_actual_1.json'); b=load('J42_RECEIPTS_actual_2.json')
    assert a==b
    assert sha((OLD/'J42_RECEIPTS_actual_1.json').read_bytes()) == 'c54b215bb03bba391571b4c51357831b14f256b7c4c6eec98d85dd9bda30eebf'
    views={k:guard(a,k) for k in sorted(a['p41_joined_receipts'])}
    cold={k:guard(b,k) for k in sorted(b['p41_joined_receipts'])}
    positive=sum(v['state']=='SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER' for v in views.values())
    # artifact identity and exact lookup
    worlds=_load_w41_worlds()
    artifact=subprocess.check_output(['git','-C',str(REPO),'show',f'{W41_COMMIT}:{W41_ARTIFACT_PATH}'],timeout=180)
    assert sha(artifact)==W41_ARTIFACT_SHA256
    trusted=worlds[KEY]
    # paired caller-clock mutation + P41 rehash
    forged={'mode':'AS_OF','published_asof':'2099-01-01','valid_at':'2099-01-01'}
    def pair(p):
        p['n9_world']['selection']=dict(forged)
        p['j42_bindings']['w41_clock']=dict(forged,test_now=None)
    paired=mutate(a,pair)
    # selection-only and binding-only caller mutations
    only=mutate(a,lambda p:p['n9_world'].__setitem__('selection',dict(forged)))
    binding=mutate(a,lambda p:p['j42_bindings'].__setitem__('w41_clock',dict(forged,test_now=None)))
    # snapshot/view caller mutation with rehash
    snap=mutate(a,lambda p:p['j42_bindings'].__setitem__('w41_snapshot_hash','f'*64))
    view=mutate(a,lambda p:p['j42_bindings'].__setitem__('w41_view_hash','f'*64))
    # missing exact W41 lookup key control
    missing=copy.deepcopy(a)
    # leave all caller data, request an absent key; guard should refuse before delegate
    absent_key='base/DOES_NOT_EXIST/budget5'
    try:
        absent=guard(missing,absent_key)
    except Exception as exc:
        absent={'exception':type(exc).__name__,'detail':str(exc)}
    # Stale hash unchanged control
    stale=unmutated(a,lambda p:p['n9_world'].__setitem__('guard_probe','stale'))
    doc={
      'schema':'PDEV01_N10W_CLOCK_RECHECK_EVIDENCE@1.0.0',
      'candidate':'c75b464ab4dbba15c6a89db42aaf5d101ba13d55',
      'reused_evidence':'e79be4a3d8cd2cbe57c4a25361acc5e4dd9a8e1c',
      'actual_j42':{'receipt_sha256':sha((OLD/'J42_RECEIPTS_actual_1.json').read_bytes()),'receipt_2_sha256':sha((OLD/'J42_RECEIPTS_actual_2.json').read_bytes()),'cold_byte_equal':a==b,'views':len(views),'positive':positive,'first_refusals':{k:v for k,v in views.items() if v['state']!='SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER'},'cold_all_view_hashes_equal':views==cold,'base':views[KEY]},
      'w41_artifact':{'commit':W41_COMMIT,'path':W41_ARTIFACT_PATH,'sha256':W41_ARTIFACT_SHA256,'verified_sha256':sha(artifact),'trusted_world':{'clock':trusted.get('clock'),'snapshot_hash':trusted.get('snapshot_hash'),'view_hash':trusted.get('content_hash')},'caller_independent':True,'exact_lookup_key':KEY},
      'paired_clock_mutation':{'forged_clock':forged,'guard':guard(paired)},
      'selection_only_mutation':{'guard':guard(only)},
      'binding_only_mutation':{'guard':guard(binding)},
      'snapshot_mutation':{'guard':guard(snap)},
      'view_mutation':{'guard':guard(view)},
      'absent_lookup_key':absent,
      'stale_hash':guard(stale),
      'limits':['TEST_ONLY sourcefree; no original data','candidate readonly; no production edit','no authority/science/adoption'],
    }
    (HERE/'evidence/recheck_evidence.json').write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'views':len(views),'positive':positive,'cold_equal':views==cold,'paired':doc['paired_clock_mutation']['guard'],'selection_only':doc['selection_only_mutation']['guard'],'binding_only':doc['binding_only_mutation']['guard'],'snapshot':doc['snapshot_mutation']['guard'],'view':doc['view_mutation']['guard'],'absent':absent,'stale':doc['stale_hash']},indent=2))

if __name__=='__main__': main()
