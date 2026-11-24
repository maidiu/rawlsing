"""Translate frozen inputs only; expected/group/history_label never enter the engine."""
from copy import deepcopy
from pathlib import Path
import tempfile
from integration import Integration
from fixture_authority import FixtureAuthority

def inputs(case):
 frame=deepcopy(dict(case_id=case['id'],actor={k:v for k,v in case['actor'].items() if k not in ('history_label','SES','sect','age')},
  event=case['world']['event'],actors=case['world']['actors'],evidence=case['world']['evidence'],utterances=case['world']['utterances'],
  ledger=case['world']['ledger'],readset=case['readset'],capability=case['capability'],as_of=case['as_of'],
  proposals=case['proposals'],lineage=case['lineage']))
 frame['exposures']=[]
 observed={x['id']:x for x in frame['evidence']}
 for s in frame['utterances']:
  s['event_ref']=frame['event']['id']
  if 'child' in s['heard_by'] and s['witness'] in observed:
   x=observed[s['witness']]
   frame['exposures'].append(dict(id='heard:'+s['id'],speech_id=s['id'],listener='child',time=x['time'],observer='child',speech_witness=x['id'],source_hash=x['hash'],issuer='B3_TEST_ONLY_EXPOSURE_REGISTRY'))
 return frame
def run_case(case):
 with tempfile.TemporaryDirectory() as d:
  frame=inputs(case);authority=FixtureAuthority();authority.register_observed(frame)
  engine=Integration(Path(d)/'case.sqlite',authority)
  try:
   exact=any(x['event_id']==frame['event']['id'] and x['content_hash']==frame['event']['content_hash'] and x['owner']==frame['event']['owner'] for x in frame['ledger'])
   if exact:
    setup=deepcopy(frame);setup['ledger']=[]
    seeded=engine.run(setup)
    assert seeded['status']=='ELIGIBLE_NONCAUSAL'
   result=engine.run(frame)
   if exact:result['replay_setup']='SEPARATE_TEST_ONLY_PINNED_FIXTURE_RECONSTRUCTION'
   return result
  finally:engine.close()
