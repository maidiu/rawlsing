"""Independent review of PDEV01 N10W repair 877f974a: actual J42 84 views + guard."""
from __future__ import annotations
import copy, json, os, shutil, subprocess, sys, tarfile, tempfile, hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CANDIDATE = Path('/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-pdev01-n10w-join')
REPAIR = CANDIDATE / 'WORKER_RETURNS/PDEV01-N10W-JOIN/repair'
J42 = 'f53cb0d2bce52640268c844c398bbd8007d28edc'
J42_PACKET = 'WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1'
W41_COMMIT = 'b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2'
W41_PATH = 'WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1/current_historical_asof_world_consumer_receipts.json'
KEY = 'base/TEST_CURRENT/budget5'
J42_ROWS = '4320b3a505478c274fc756ce0e025e36685e0742e940072aae80ce11286e4c02'
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPAIR))
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_universal_world_binding import (
    JoinedWorldField, select_joined_world_view,
)
from rawlsing_next.tests.test_universal_world_binding import _joined_request
from guarded_receiver import guarded_select_joined_world_view


def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_path(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def build(tag):
    base = Path(tempfile.mkdtemp(prefix=f'.n10w-review-{tag}-', dir=tempfile.gettempdir()))
    try:
        archive = base / 'j42.tar'
        subprocess.run(['git','archive',J42,J42_PACKET,'-o',str(archive)], cwd=str(REPO), check=True, capture_output=True, timeout=180)
        with tarfile.open(archive) as h: h.extractall(base)
        packet = base / J42_PACKET
        os.symlink(REPO/'rawlsing_next', base/'rawlsing_next')
        (base/'.git').write_text('gitdir: ' + subprocess.check_output(['git','-C',str(REPO),'rev-parse','--absolute-git-dir'], text=True).strip() + '\n')
        env = dict(os.environ, PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1')
        env['PYTHONPATH'] = str(REPO) + os.pathsep + env.get('PYTHONPATH','')
        out = base/'out'; out.mkdir()
        proc = subprocess.run([sys.executable, str(packet/'runtime/j42_build.py'), '--outdir', str(out)], cwd=str(REPO), env=env, capture_output=True, text=True, timeout=900)
        if proc.returncode != 0:
            raise RuntimeError((proc.stdout[-4000:] + proc.stderr[-4000:]))
        receipt_path = packet/'n9_n10e_n10w_real_joined_consumer_receipts.json'
        receipts = json.loads(receipt_path.read_text())
        raw = receipt_path.read_bytes()
        return receipts, raw, proc.stdout
    finally:
        shutil.rmtree(base, ignore_errors=True)

def fields_for(receipts, key):
    rules = receipts['p41_joined_receipts'][key]['n9_world']['rules']
    return (JoinedWorldField('training_access', rules['training_access']['value']),
            JoinedWorldField('civil_sanction', rules['civil_sanction']['value']))

def run_guard(receipts, key=KEY, fields=None, **changes):
    view = guarded_select_joined_world_view(_joined_request(
        receipts, key, fields=fields_for(receipts,key) if fields is None else fields, **changes))
    return {'state': view.state, 'reason_code': view.reason_code, 'view_key': view.view_key,
            'view_hash': view.view_hash, 'families': None if view.consumer_values_read is None else view.consumer_values_read.get('families'),
            'n9_currentness': None if view.consumer_values_read is None else view.consumer_values_read.get('n9_currentness'),
            'n9_clock': None if view.consumer_values_read is None else view.consumer_values_read.get('n9_clock')}

def run_base(receipts, key=KEY, **changes):
    view = select_joined_world_view(_joined_request(receipts, key, fields=fields_for(receipts,key), **changes))
    return {'state': view.state, 'reason_code': view.reason_code, 'view_hash': view.view_hash}

def p41(receipts): return receipts['p41_joined_receipts'][KEY]

def rehash(p):
    p.pop('content_hash', None); p['content_hash'] = semantic_hash(p)

def mutate(receipts, change, *, rehash_it=True):
    d = copy.deepcopy(receipts); p = p41(d); change(p)
    if rehash_it: rehash(p)
    return d

def without(receipts, section):
    d = copy.deepcopy(receipts); d[section].pop(KEY, None); return d

def main():
    rec1, raw1, out1 = build('one')
    rec2, raw2, out2 = build('two')
    (HERE/'evidence'/'J42_RECEIPTS_actual_1.json').write_bytes(raw1)
    (HERE/'evidence'/'J42_RECEIPTS_actual_2.json').write_bytes(raw2)
    (HERE/'logs'/'j42_build_1.stdout.log').write_text(out1)
    (HERE/'logs'/'j42_build_2.stdout.log').write_text(out2)
    if rec1 != rec2 or raw1 != raw2:
        raise AssertionError('cold receipts differ')
    all1 = {k: run_guard(rec1,k) for k in sorted(rec1['p41_joined_receipts'])}
    all2 = {k: run_guard(rec2,k) for k in sorted(rec2['p41_joined_receipts'])}
    positive = {k:v for k,v in all1.items() if v['state']=='SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER'}
    cold_equal = all2 == all1
    base = all1[KEY]
    # five rehashed mutations
    versions = json.loads((CANDIDATE/'WORKER_RETURNS/PDEV01-N10W-JOIN/VERSION_AND_IDENTITY_NEGATIVES.json').read_text())['defects']
    five = {}
    for name, spec in versions.items():
        if name == 'wrong_n9_provider_version': change=lambda p:p['providers'].__setitem__('n9_world',spec['mutated_value'])
        elif name == 'wrong_n10e_provider_version': change=lambda p:p['providers'].__setitem__('n10e_empirical',spec['mutated_value'])
        elif name == 'wrong_n10w_provider_version': change=lambda p:p['providers'].__setitem__('n10w_progressive',spec['mutated_value'])
        elif name == 'revoked_n9_currentness': change=lambda p:p['n9_world'].__setitem__('currentness',spec['mutated_value'])
        elif name == 'mutated_n9_selection': change=lambda p:p['n9_world'].__setitem__('selection',spec['mutated_value'])
        else: continue
        d=mutate(rec1,change); five[name]={'guard':run_guard(d),'base':run_base(d)}
    # simultaneous self-consistent clock change + rehash
    new_clock={'mode':'AS_OF','published_asof':'2099-01-01','valid_at':'2099-01-01'}
    def both(p):
        p['n9_world']['selection']=dict(new_clock)
        p['j42_bindings']['w41_clock']=dict(new_clock,test_now=None)
    simultaneous=mutate(rec1,both)
    # selection-only rehash for contrast
    only=mutate(rec1,lambda p:p['n9_world'].__setitem__('selection',dict(new_clock)))
    # stale hash control (no rehash)
    stale=mutate(rec1,lambda p:p['n9_world'].__setitem__('guard_probe','stale'),rehash_it=False)
    missing={
      'missing_n9_provider':run_guard(mutate(rec1,lambda p:p['providers'].pop('n9_world',None))),
      'missing_n10e_steps':run_guard(mutate(rec1,lambda p:p.__setitem__('n10e_steps',[]))),
      'missing_p41_receipt':run_guard(without(rec1,'p41_joined_receipts'), fields=fields_for(rec1,KEY)),
      'missing_joined_receipt':run_guard(without(rec1,'joined_consumer_receipts'), fields=fields_for(rec1,KEY)),
      'missing_required_field':run_guard(rec1,fields=(_joined_request(rec1,KEY).fields[0],)),
      'wrong_source_rows':run_guard(rec1,source_rows_hash='f'*64),
      'wrong_as_of':run_guard(rec1,as_of_ref='2099-01-01'),
    }
    r05=json.loads((CANDIDATE/'WORKER_RETURNS/PDEV01-N10W-JOIN/R05_P41_TRACE.json').read_text())
    r05d=mutate(rec1,lambda p:p.__setitem__('providers',dict(r05['p41_providers'])))
    # trusted W41 clock comparison
    w41=json.loads(subprocess.check_output(['git','-C',str(REPO),'show',W41_COMMIT+':'+W41_PATH], timeout=180))
    trusted_clock=w41['worlds'][KEY]['clock']
    doc={
      'schema':'PDEV01_N10W_INDEPENDENT_REVIEW_EVIDENCE@1.0.0',
      'candidate':'877f974a0e70ea591118fd94f558d73f426202dc',
      'review_branch':'review/pyat-pdev01-n10w-identity-r1',
      'j42':{'commit':J42,'packet':J42_PACKET,'build_stdout_sha256':sha_bytes(out1.encode()),'receipt_sha256':sha_bytes(raw1),'receipt_2_sha256':sha_bytes(raw2),'receipts_byte_equal':raw1==raw2,'views':len(all1),'positive':len(positive),'positive_first_refusals':{k:v for k,v in all1.items() if v['state']!='SELECTED_VIEW_FROM_ACTUAL_JOINED_CONSUMER'},'cold_all_view_hashes_equal':cold_equal,'base':base},
      'five_rehashed_mutations':five,
      'clock_trust':{'trusted_w41_clock':trusted_clock,'baseline_j42_clock':p41(rec1)['j42_bindings']['w41_clock'],'guard_accepts_simultaneous_clock_rehash':run_guard(simultaneous),'guard_refuses_selection_only_rehash':run_guard(only),'simultaneous_clock':new_clock,'trusted_input_compared_by_guard':False},
      'stale_hash':run_guard(stale),
      'missing_parents':missing,
      'r05_substitution':run_guard(r05d),
      'limits':['TEST_ONLY sourcefree actual J42/J41/P41; no original data','candidate production receiver unchanged; guard is isolated overlay','no authority/science/adoption'],
    }
    (HERE/'evidence'/'review_evidence.json').write_text(json.dumps(doc,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'j42_views':len(all1),'positive':len(positive),'cold_equal':cold_equal,'five_mutations_refused':all(v['guard']['state']=='REFUSED' for v in five.values()),'simultaneous_clock':doc['clock_trust']['guard_accepts_simultaneous_clock_rehash'],'selection_only':doc['clock_trust']['guard_refuses_selection_only_rehash'],'stale':doc['stale_hash'],'missing':missing},indent=2))

if __name__=='__main__': main()
