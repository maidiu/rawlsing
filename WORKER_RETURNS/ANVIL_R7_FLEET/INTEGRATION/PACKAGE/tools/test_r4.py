#!/usr/bin/env python3
"""R4-to-R5 regressions recreated from hostile reviews. Original interrupted R4 test bytes unavailable."""
from test_r5 import fixture
from anvil import validate
import copy,json
s=fixture();assert not validate(s)
errors={}
def attack(name,mut,marker):
    x=copy.deepcopy(s);mut(x);e=validate(x)
    assert any(marker in t for t in e),(name,e[:8]);errors[name]=marker
attack('forged_claim_upgrade',lambda x:x['architecture']['edges'][1].update(transition_class='AUTOMATIC_PERSON_IDENTITY'),'UNAUTHORIZED_OR_UNMODELED_TRANSITION')
attack('actor_immaterial_source_backflow',lambda x:(x['architecture']['nodes'][0]['input_types'].append('next_world'),x['architecture']['edges'].append({**x['architecture']['edges'][0],'id':'BACKFLOW','from':'WORLD_NEXT','to':'SRC','data_type':'next_world'})),'UNAUTHORIZED_OR_UNMODELED_TRANSITION')
attack('redundant_authority_field',lambda x:x['architecture']['edges'][0].update(grade='RELEASED_ORIGINAL'),'CONFLICTING_SECOND_AUTHORITY_VOCABULARY')
attack('missing_temporal_guard',lambda x:x['architecture']['edges'][-1].update(strict_time_guard=''),'UNPROVED_FUTURE_TIME_GUARD')
attack('unimplemented_FF_grade',lambda x:(x.update(outcome='DESIGN_READY_SCOPED'),x['operational_boundary'].update(selected_tranche='FF_FIRST_EFFECT_DESIGN',effect_grade='SOURCE_STATIC_INTERFACE_ONLY')),'PREMATURE_FF_FIRST_EFFECT_CLAIM')
attack('wrong_scope_boundary',lambda x:x['operational_boundary'].update(selected_tranche='FULL_LIFELONG_ACTOR_ENGINE'),'UNBOUNDED_DESIGN_READY_SCOPE')
print(json.dumps({'status':'PASS_RECONSTRUCTED_R4_TO_R5_SYNTHETIC','count':len(errors),'cases':errors},indent=2))
