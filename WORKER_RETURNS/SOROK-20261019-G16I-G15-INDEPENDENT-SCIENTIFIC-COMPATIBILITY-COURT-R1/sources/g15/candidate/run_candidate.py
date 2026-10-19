"""Run or cold-replay the complete research candidate; no external services."""
from pathlib import Path
import argparse,json,sys
sys.dont_write_bytecode=True
from lab_sgi1.research import inputs,run
from lab_sgi1.proposal import ProposalRecord
from lab_sgi1.core import h_obj


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--replay',type=Path);a=p.parse_args()
 if a.replay:
  old=json.loads(a.replay.read_text());data=json.loads(json.dumps(old['frozen_inputs']));data['proposal_record']=ProposalRecord(**data['proposal_record']);result=run(data)
  equal=result['causal_replay_record']==old['result']['causal_replay_record']
  out=dict(result=result,complete_causal_record_equal=equal,source_packet_hash=h_obj(old['frozen_inputs']))
 else:
  data=inputs();result=run(data);frozen=dict(data);frozen['proposal_record']=data['proposal_record'].as_dict()
  out=dict(frozen_inputs=frozen,result=result)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps(dict(terminal=result['terminal']['status'],causal_replay_hash=result['causal_replay_hash'],complete_causal_record_equal=out.get('complete_causal_record_equal')),sort_keys=True))
 if a.replay and not out['complete_causal_record_equal']:return 1
 return 0
if __name__=='__main__':raise SystemExit(main())
