"""Record actual native producer and downstream outputs in a fresh interpreter."""
from pathlib import Path
import sys,json,copy
ROOT=Path(__file__).resolve().parents[1]
mode=sys.argv[1]
sys.path.insert(0,str(ROOT/('candidate' if mode=='repaired' else 'inherited/F6J/01_STAGED_NATIVE')))
sys.path.insert(0,str(ROOT/'inherited/F6C/02_TESTS'))
import f6c_worlds as C
import rawlsing_next.pre553_heterogeneous_synthesis as M
from rawlsing_next.pre553_empirical_objects import semantic_hash
worlds={w['case']:w for w in json.loads((ROOT/'inherited/F6L/02_PHASE_A/01_WORLDS_AND_EXACT_EXPECTATIONS.json').read_text())['worlds']}
cases={
 'world_a':C.world_a(), 'world_b':C.world_b(),
 'forged_owner':None, 'mixed_origin':None,
 'novel_2x2_no_positivity':None, 'novel_3category_no_positivity':None,
 'minority_cell_threshold5':None, 'minority_source_exclusion150':None}
for name,case in [('forged_owner','P11_GENUINE_COMPLETE_TARGET_POSITIVE'),('mixed_origin','P11_GENUINE_COMPLETE_TARGET_POSITIVE'),('novel_2x2_no_positivity','P2_NOVEL_2X2_NO_POSITIVITY'),('novel_3category_no_positivity','P3_NOVEL_3_CATEGORY_NO_POSITIVITY'),('minority_cell_threshold5','P8_DISTRIBUTED_SUPPORT_MIN_5_CELL_NOT_GATE'),('minority_source_exclusion150','P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED')]:
 w=copy.deepcopy(worlds[case]);cases[name]=(w['target'],w['sources'],w['policy'])
for s in cases['forged_owner'][1]:s['test_origin']=False
cases['mixed_origin'][1][0]['test_origin']=False
cases['mixed_origin'][1][1]['test_origin']=True
rows=[]
for name,(t,s,p) in cases.items():
 calls=[]
 def callback(source,target,operation):calls.append({'source_id':source['source_id'],'operation':operation});return True
 out=M.synthesize(t,s,p,admit=callback)
 c=out['candidate'];axis=c['construct_topology']
 # The real native value-reading conditional, plus a deliberately decision-only gate.
 cond=M.conditional(out,{axis[0]:c['ordered_categories'][0][0]},axis[1])
 real=M.conditional(out,{},axis[-1],use='REAL_USE') if mode=='repaired' else {'state':'NO_AUTHENTICATED_USE_INTERFACE_IN_ORIGINAL'}
 rows.append(dict(case=name,input_hash=semantic_hash([t,s,p]),callback_calls=calls,
                  producer_output=out,native_conditional=cond,real_use_consumer=real,
                  decision_only_consumer=('COMPLETE_DECISION_ACCEPTED' if out['decision']=='SYNTHETIC_CANDIDATE' else 'REFUSED')))
path=ROOT/'evidence'/mode/'consumer_outputs.json';path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n')
print(mode,len(rows),'actual producer/consumer receipts')
