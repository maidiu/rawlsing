#!/usr/bin/env python3
"""Rehydrate pinned authorized closure from the existing Git store and reproduce.

Run from any checkout containing the pinned Git objects. No fetch, credentials,
model SDK or provider transport is used. Only this return directory is written.
Independent contract REDs are retained and make this script return 1.
"""
import collections
import gzip
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

R = Path(__file__).resolve().parent
REPO = R.parents[1]
LAB1 = 'd7cc7ebf0c06303ffe5637aa4d14c3c1fc228e09'
LAB2 = 'bf5fda102f4bced41a0f18f71c4c380d5d099462'
START = '24173c46b4130bc080955087082cb4e864bcb70c'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def h(data):
    return hashlib.sha256(data).hexdigest()


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()


def write(name, obj):
    p = R / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True)+'\n')


def compressed(name, obj):
    (R / name).write_bytes(gzip.compress(canon(obj), mtime=0))


def sanitize_xml(path):
    tree = ET.parse(path)
    for el in tree.iter():
        el.attrib.pop('hostname', None)
        for k,v in list(el.attrib.items()):
            el.set(k,v.replace(str(REPO), '<WORKTREE>'))
        if el.text:
            el.text = el.text.replace(str(REPO), '<WORKTREE>')
    tree.write(path, encoding='unicode')


def command(name, args, cwd):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    output = (result.stdout+result.stderr).replace(str(REPO), '<WORKTREE>')
    (R/'receipts'/f'{name}.txt').write_text(
        f'cwd: {cwd.relative_to(R)}\ncommand: {" ".join(args)}\nexit_code: {result.returncode}\n'+output)
    print(name, 'exit', result.returncode, output[-350:])
    return result.returncode


def main():
    (R/'receipts').mkdir(exist_ok=True)
    marker = R/'.runtime_marker'
    if not marker.exists():
        marker.write_text(str(uuid.uuid4())+'\n')
    manifest = json.loads((R/'source_manifest.json').read_text())
    for row in manifest:
        data = git('show', row['commit']+':'+row['path'])
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+bytes([0])+data).hexdigest() == row['git_blob_sha1']
        assert h(data) == row['sha256']
        p = R/row['local_relative_path']
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(data)
    tests = {}
    for label in ('LAB1','LAB2'):
        cwd=R/'imports'/label
        pkg='lab' if label=='LAB1' else 'lab2'
        xml = R/'receipts'/f'{label.lower()}_junit.xml'
        tests[label] = command(label.lower()+'_suite',
            [sys.executable,'-m','pytest',f'{pkg}/test_{pkg}.py','-q',f'--junitxml=../../receipts/{label.lower()}_junit.xml'], cwd)
        sanitize_xml(xml)
        assert tests[label] == 0
        assert command(label.lower()+'_machine' if label=='LAB1' else 'lab2_harness',
                       [sys.executable,f'{pkg}/run_{pkg}.py' if label=='LAB1' else 'lab2/run_lab2.py'],cwd)==0
        profile = '''import sys,json,hashlib,pathlib
sys.path.insert(0, '.')
LABEL = sys.argv[1]
if LABEL == 'LAB1':
 import lab.experiment, lab.runner
else:
 import lab2.packets, lab2.scoring, lab2.behavioral_runner
out=[]
for name,m in sorted(sys.modules.items()):
 if name == 'lab' or name.startswith(('lab.','lab2.')):
  p=pathlib.Path(m.__file__).resolve();b=p.read_bytes()
  out.append(dict(module=name,file=str(p.relative_to(pathlib.Path.cwd().resolve().parents[1])),git_blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()))
print(json.dumps(out))'''
        imported=json.loads(subprocess.check_output([sys.executable,'-c',profile,label],cwd=cwd))
        write(f'receipts/{label.lower()}_imports.json',imported)

    # Actual replay-vs-predecessor comparison; do not trust run_lab2's literals.
    prefix='WORKER_RETURNS/SOROK-S-M-LAB1-WORLD-ORG-RESPONSE-CAUSAL-COURT-R1/'
    old=json.loads(git('show',LAB1+':'+prefix+'outputs/primary_results.json'))
    new=json.loads((R/'imports/LAB1/outputs/primary_results.json').read_text())
    compressed('receipts/lab1_primary_results.json.gz',new)
    section={k:dict(equal=old[k]==new[k],original_sha256=h(canon(old[k])),replay_sha256=h(canon(new[k]))) for k in old}
    rows=[];raw={}
    for p in sorted((R/'imports/LAB1/outputs/runs').glob('*.json')):
        a=git('show',LAB1+':'+prefix+'outputs/runs/'+p.name);b=p.read_bytes()
        oa=json.loads(a);ob=json.loads(b);raw[p.name]=ob
        diffs=[k for k in set(oa)|set(ob) if oa.get(k)!=ob.get(k)]
        rows.append(dict(file=p.name,original_raw_sha256=h(a),replay_raw_sha256=h(b),raw_byte_equal=a==b,different_top_level_fields=diffs,
                         deterministic_equal={k:v for k,v in oa.items() if k!='latency_ms'}=={k:v for k,v in ob.items() if k!='latency_ms'}))
    assert len(rows)==576 and all(x['deterministic_equal'] for x in rows)
    assert all(section[k]['equal'] for k in ('scores','integrity','null_controls','opacity','comparison'))
    compressed('receipts/lab1_all_576_runs.json.gz',raw)
    write('receipts/replication_diff.json',dict(sections=section,trial_count=len(rows),raw_byte_equal_count=sum(x['raw_byte_equal'] for x in rows),deterministic_equal_count=sum(x['deterministic_equal'] for x in rows),runs=rows,
          ceiling='Five declared semantic sections identical; full timed output is NOT byte-identical. Only per-trial latency_ms excluded for deterministic equality.'))

    sys.path.insert(0,str(R/'imports/LAB2'))
    from lab2 import packets, scoring, behavioral_runner
    from lab2.model_gate import evaluate_gate
    m=packets.build_manifest();all_packets=[];pos=collections.defaultdict(lambda:collections.Counter())
    attackers=[];by_arm=collections.defaultdict(list);by_block=collections.defaultdict(list)
    for t in m['trials']:
        f=next(f for f,c in packets.contrast_pairs(t['k_id']) if c==t['prereg_contrast'])
        p=packets.build_trial_packet(t['k_id'],f,t['prereg_contrast'],t['seed'],t['arm'])
        all_packets.append(dict(arm=t['arm'],packet=p))
        by_block[t['trial_id']].append({k:v for k,v in p.items() if k not in ('typed_menu','presentation_code','counterbalance_code')})
        pos[(t['k_id'],t['prereg_contrast'],t['arm'])][p['typed_menu'].index(t['expected_typed_codes'][0])]+=1
        # Adversarial control only: use a frozen label->code table, zero state/history reasoning.
        code=packets.EXPECTED_TYPED_CODES[p['k_id']][p['trial_id'].split('__')[1]][0]
        attackers.append(scoring.ScorerInput(t['trial_id'],t['presentation_code'],code))
        by_arm[t['arm']].append(scoring.ScorerInput(t['trial_id'],t['presentation_code'],p['typed_menu'][0]))
    expected={t['trial_id']:t['expected_typed_codes'] for t in m['trials']}
    oracle=scoring.dual_score(attackers,expected)
    first={a:scoring.scorer_alpha(v,expected) for a,v in by_arm.items()}
    assert len(by_block)==192 and all(len(v)==3 and all(x==v[0] for x in v) for v in by_block.values())
    vendor_matches=[]
    for p in sorted((R/'imports/LAB2/lab2/predecessor_lab1/lab').glob('*.py')):
        original=R/'imports/LAB1/lab'/p.name
        assert p.read_bytes()==original.read_bytes()
        vendor_matches.append(dict(file=p.name,sha256=h(p.read_bytes()),equal=True))
    assert len(vendor_matches)==6
    pre=R/'imports/LAB2/01_PREREGISTRATION_FROZEN.json'
    freeze=json.loads((R/'imports/LAB2/outputs/preregistration_freeze.json').read_text())
    assert h(pre.read_bytes())==freeze['preregistration_sha256']
    retained=json.loads(git('show',LAB2+':WORKER_RETURNS/SOROK-R3-HQ298-SM-LAB2-BEHAVIORAL-R1/outputs/matched_heldout_manifest.json'))
    assert m['manifest_hash']==retained['manifest_hash']
    counts=[dict(k=k,contrast=c,arm=a,expected_position_counts={str(i):v[i] for i in range(len(packets.MENU_ORDER[k]))}) for (k,c,a),v in pos.items()]
    collisions=collections.defaultdict(set)
    for t in m['trials']:
        collisions[t['matched_content_hash']].add((t['k_id'],t['prereg_contrast'],tuple(t['expected_typed_codes'])))
    collision_rows=[dict(matched_content_hash=key,contrasts=[dict(k=k,contrast=c,expected_codes=list(codes)) for k,c,codes in sorted(v)],conflicting_expected_codes=len({codes for k,c,codes in v})>1) for key,v in collisions.items() if len(v)>1]
    compressed('receipts/all_576_packets.json.gz',all_packets)
    write('receipts/packet_and_scorer_audit.json',dict(manifest_hash=m['manifest_hash'],preregistration_sha256=h(pre.read_bytes()),freeze=freeze,
          n_trials=m['n_trials'],unique_trial_ids=len(expected),unique_matched_content_hashes=len({t['matched_content_hash'] for t in m['trials']}),
          matched_ok=m['matched_content_across_arms_ok'],independent_full_core_equal_blocks=len(by_block),content_collisions=collision_rows,vendor_original_equality=vendor_matches,opaque_id_attack_correct=sum(x['correct'] for x in oracle['records']),attack_n=oracle['n_records'],
          attack_label='DETERMINISTIC_METADATA_ONLY_COUNTEREXAMPLE__NOT_BEHAVIORAL_EVIDENCE',
          first_menu_only_comparison=scoring.compare_arms(first),first_menu_only_per_k={k:scoring.compare_arms({a:[x for x in rows if x.trial_id.startswith(k+'__')] for a,rows in first.items()}) for k in packets.EXPECTED_TYPED_CODES},menu_position_counts=counts,packet_nulls=behavioral_runner.run_packet_nulls(),gate=evaluate_gate(None).as_dict(),
          zero_discordance_one_sided_95_upper_at_n12=1-.05**(1/12),minimum_iid_n_for_zero_discordance_upper_below_5pp=59,
          unit_caveat='Binomial illustration assumes IID discordances. Paired +/-1 outcomes and clustered scenario inference require a predeclared actual design; this is not power certification.'))
    tests['independent']=command('independent_contracts',[sys.executable,'-m','pytest','test_independent.py','-q','--tb=short','--junitxml=receipts/independent_junit.xml'],R)
    sanitize_xml(R/'receipts/independent_junit.xml')
    write('receipts/execution_summary.json',dict(observed_at=datetime.now(timezone.utc).isoformat(),startup=START,checkout=git('rev-parse','HEAD').decode().strip(),python=platform.python_version(),pytest=subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),git=git('--version').decode().strip(),source_count=len(manifest),suite_exit_codes=tests,external_model_calls=0,actor_runs=0,source_calls=0,network_guard='Independent pytest socket/DNS guard; candidate suite code inspected; no provider transport implemented',return_status='REVIEW_REVISE'))
    return 1 if tests['independent'] else 0


if __name__=='__main__':
    raise SystemExit(main())
