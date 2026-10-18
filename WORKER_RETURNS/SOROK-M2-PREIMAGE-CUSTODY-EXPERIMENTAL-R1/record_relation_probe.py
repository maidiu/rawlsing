from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'m2_patch'))
from kernel import eligible
from test_local_hostile import twice,rewrite_history,replace,asdict
scene,state=twice()
out={'state_hash_before':state.hash(),'lineage_source_preimages':[asdict(x)['source_preimages'] for x in state.lineage],
     'original_t9_relevance':[asdict(x) for x in scene.relevance],'controls':[]}
for name in ('observed_history','relevance_deleted','relevance_witness'):
    if name=='observed_history':bad=rewrite_history(scene,'child','later_observed_counterpart',activity='observed_counterpart_action:ALLOW')
    elif name=='relevance_deleted':bad=replace(scene,relevance=())
    else:bad=replace(scene,relevance=(replace(scene.relevance[0],observer='peer'),))
    try:options=eligible(bad,state,'future');r={'result':'NOT_REFUSED','candidate_modes':[x.mode for x in options]}
    except Exception as e:r={'result':'REFUSED','code':str(e)}
    out['controls'].append({'attack':name,**r})
out['state_hash_after']=state.hash()
(ROOT/'evidence/later_relation_probe.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['controls']))
