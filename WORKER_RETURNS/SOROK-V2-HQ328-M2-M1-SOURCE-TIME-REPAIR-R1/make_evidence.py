import json, subprocess, sys, hashlib, tarfile
from pathlib import Path
from dataclasses import asdict
from kernel import *
p=Path(__file__).parent
scene=seed_scene(other_action='REFUSE'); st=State('child',procedure_refs=('old_watchful_habit',))
start_hash=objective_event_hash(scene.events[0])
loss=eligible(scene,st,'loss');processing=eligible(scene,st,'discussion')
selected=next(x for x in processing if x.source=='parent_said' and x.stance=='REJECT')
pr=propose(scene,st,'discussion',selected.id,affect_ref='first_distress',public_action_ref='public_lock_check')
first=append_test_only(scene,st,pr,fixture_grant(pr,'child'))
future=eligible(scene,first,'later')
selected2=next(x for x in future if x.mode=='DIFFERENTIATE')
pr2=propose(scene,first,'later',selected2.id)
second=append_test_only(scene,first,pr2,fixture_grant(pr2,'child'))
no_change=next(x for x in future if x.mode=='NO_CHANGE');nc=propose(scene,first,'later',no_change.id);ng=fixture_grant(nc,'child')
audit=audit_no_change(scene,first,nc,ng);unchanged=append_test_only(scene,first,nc,ng)
receipt={
 'schema':'M2_SOURCEFREE_TWO_EVENT_RECEIPT_R1','grade':GRADE,
 'objective_loss_hash_before_after':{'before':start_hash,'after':objective_event_hash(scene.events[0])},
 'loss_t3_eligible_modes':[(x.mode,x.source) for x in loss],
 'processing_t6_eligible_count':len(processing),'processing_t6_accounts':sorted({x.source for x in processing if x.mode=='RECONSIDER'}),
 'first_lineage':asdict(first.lineage[0]),'later_t9_eligible_modes':[x.mode for x in future],
 'second_lineage':asdict(second.lineage[-1]),'lineage_length_after_t9':len(second.lineage),
 'no_effect_state_identical':unchanged==first,'no_effect_audit':asdict(audit),
 'counterpart_action':'REFUSE','no_automatic_belief_or_psyche':True,
 'real_owner_grants':'NOT_ISSUED','native_actor':'NOT_RUN'}
(p/'sample_receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print('sample',len(processing),'candidate alternatives; lineage versions',len(second.lineage),'objective identical',receipt['objective_loss_hash_before_after']['before']==receipt['objective_loss_hash_before_after']['after'])
