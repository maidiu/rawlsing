"""Freeze candidate bytes BEFORE any mock. Append-only versions; no execution."""
from pathlib import Path
import argparse,hashlib,json,copy
from datetime import datetime,timezone
from assay.corpus import create_files,opaque,ARMS
from assay.oracle import proposed_key
R=Path(__file__).resolve().parent

def main(version):
 data=R/'data';data.mkdir(exist_ok=True)
 if not (data/'corpus.json').exists():
  cases,rows=create_files(data)
  primary=list(rows)
  for c in cases:
   controls={a:next(r for r in primary if r['case']==c['id'] and r['arm']==a) for a in ARMS}
   for phase in ['N1_PARAPHRASE','N2_LABEL','N3_ORDER','N4_SURFACE','N5_TRACE_FIREWALL','N6_NO_PROSE_SCORING','N7_BUDGET','free_text']:
    block=opaque()
    for arm in ARMS:
     control=controls[arm];row=copy.deepcopy(control);row.update(id=opaque(),block=block,phase=phase,control=control['id'])
     if phase!='free_text':row['variant']=phase
     else:row['response_format']='free_text_fixture'
     if phase=='N7_BUDGET':row['max_tokens']=128
     rows.append(row)
  (data/'schedule.json').write_text(json.dumps(rows,indent=2)+'\n')
  (data/'oracle.json').write_text(json.dumps(proposed_key(cases),indent=2,sort_keys=True)+'\n')
 else:
  cases=json.loads((data/'corpus.json').read_text());rows=json.loads((data/'schedule.json').read_text())
 pre=dict(schema='R2_CANDIDATE_PREREGISTRATION@2',status='FROZEN_CANDIDATE_NOT_INDEPENDENTLY_ACCEPTED',
  design='01_DESIGN.md',r1_freeze_sha256='880fbde407654cf847e72f9cc58f7884470973072e99c0964b8d33e17e0bb330',
  settings=6,constructed_factorial_cells=len(cases),primary_calls=sum(r.get('phase','primary')=='primary' for r in rows),
  null_calls=sum(r.get('phase','primary').startswith('N') for r in rows),free_text_calls=sum(r.get('phase')=='free_text' for r in rows),
  total_unique_mock_calls=len(rows),maximum_attempts_including_one_retry=2*len(rows),
  independent_sampling_units='NONE_CERTIFIED; six convenience setting families only',paired_unit='family means within K; nuisance rotations/orders averaged, not independent units',
  multiplicity=12,alpha=.05,equivalence_margin=.05,minimum_screening_gain=.10,
  power='Hoeffding precision calculation only; no powered generalization or equivalence accepted',
  semantic_status='Proposed lawful sets preserving predecessor possibilities; competent owner and separate I2 review pending',
  oracle_custody='Separate files/code paths; all authored here, NOT independent science acceptance',
  real_model_calls_permitted=0,live_mode='UNCONDITIONAL_DENIAL',review='Subsequent HQ I2 action per routing erratum, unless human user directs otherwise')
 if version not in ('v1','v2','v3'):
  pre['execution_randomization']='Whole matched blocks shuffled using Random(942011), independent of outcomes and arms; all six within-block permutations crossed.'
 if version not in ('v1','v2','v3','v4','v5','v6'):
  pre['active_ledger_continuity']='Verify regular-file inode, size, mtime and exact committed tail before append; no recreation after active removal; preserve charged attempts and deny concurrent writers.'
 if version not in ('v1','v2','v3','v4','v5','v6','v7'):
  pre['unresolved_outcomes']='Reserve marks a trial pending; only a captured response or typed retryable transport error clears it. Unknown response/capture outcomes HOLD without redraw after re-entry. Same-runner calls serialized.'
 prepath=R/('preregistration.json' if version in ('v1','v2','v3') else f'preregistration_{version}.json')
 if prepath.exists():assert json.loads(prepath.read_text())==pre
 else:prepath.write_text(json.dumps(pre,indent=2)+'\n')
 files=[R/'01_DESIGN.md',prepath,R/'freeze_candidate.py',R/'test_r2.py']+list((R/'assay').glob('*.py'))+list(data.glob('*.json'))
 manifest=dict(schema='R2_SOURCE_CORPUS_FREEZE@2',version=version,created_at=datetime.now(timezone.utc).isoformat(),
  corpus_file='data/corpus.json',schedule_file='data/schedule.json',oracle_file='data/oracle.json',preregistration_file=str(prepath.relative_to(R)),
  behavioral_mock_calls_before_initial_freeze=0 if version=='v1' else 'SEE_PRESERVED_PRIOR_VERSION_RECEIPTS',
  files={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)})
 (R/'freezes').mkdir(exist_ok=True);path=R/'freezes'/f'{version}.json'
 with path.open('x') as f:json.dump(manifest,f,indent=2,sort_keys=True);f.write('\n')
 (R/'CURRENT_FREEZE').write_text(str(path.relative_to(R))+'\n')
 print(json.dumps(pre,indent=2));print('Freeze',version,hashlib.sha256(path.read_bytes()).hexdigest())
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('version');main(p.parse_args().version)
