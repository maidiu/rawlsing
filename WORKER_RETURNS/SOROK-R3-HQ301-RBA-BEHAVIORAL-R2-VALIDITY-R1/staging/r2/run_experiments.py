"""Execute complete frozen mock assay plus adversaries; never real models."""
from pathlib import Path
import argparse,gzip,json,socket,time,re
from assay.experiment import run_mock
R=Path(__file__).resolve().parent

def main(run_id):
 if not re.fullmatch('[a-zA-Z0-9_-]{1,64}',run_id):raise ValueError('Run ID must be a single safe name')
 def deny(*a,**k):raise RuntimeError('ZERO_REAL_MODEL_NETWORK_GUARD')
 socket.socket.connect=deny;socket.socket.connect_ex=deny;socket.getaddrinfo=deny
 out=R/'receipts'/run_id
 out.mkdir(parents=True,exist_ok=False)
 freeze=R/(R/'CURRENT_FREEZE').read_text().strip()
 suites=[('complete_lawful','lawful',None),('all_first_option','first',{'primary'}),
         ('metadata_attack','metadata',{'N5_TRACE_FIREWALL'}),
         ('budget_falsifier','budget_fragile',{'N7_BUDGET'}),
         ('origin_falsifier','origin_leak',{'N5_TRACE_FIREWALL'}),
         ('belief_falsifier','belief_overwrite',{'N5_TRACE_FIREWALL'})]
 summaries={}
 for name,policy,phases in suites:
  t=time.monotonic();print('START',name,flush=True)
  summary,records=run_mock(R,freeze,out/name,policy,phases)
  summary['wall_seconds']=round(time.monotonic()-t,3)
  (out/name/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
  summaries[name]=summary
  for p in [out/name/'ledger.jsonl',out/name/'coded_captures.json',out/name/'intervention_receipts.json']:
   p.with_name(p.name+'.gz').write_bytes(gzip.compress(p.read_bytes(),mtime=0));p.unlink()
  print('DONE',name,'planned',summary['n_planned'],'dispatches',summary['mock_dispatches'],'fraction',summary['correctness_fraction_plumbing_only'],'seconds',summary['wall_seconds'],flush=True)
 assert summaries['complete_lawful']['n_planned']==10800
 assert summaries['complete_lawful']['correctness_fraction_plumbing_only']==1
 assert all(v['pass_mock_null'] for v in summaries['complete_lawful']['nulls'].values())
 for k,comparisons in summaries['all_first_option']['paired_primary'].items():
  assert all(c['delta']==0 for c in comparisons.values()),k
 assert summaries['metadata_attack']['correctness_fraction_plumbing_only']<1
 assert not summaries['budget_falsifier']['nulls']['N7_BUDGET']['pass_mock_null']
 assert summaries['origin_falsifier']['correctness_fraction_plumbing_only']==0
 assert summaries['belief_falsifier']['correctness_fraction_plumbing_only']<1
 (out/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
 print('ALL MOCK COURTS VERIFIED; ZERO REAL MODEL/ACTOR CALLS',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('run_id');main(p.parse_args().run_id)
