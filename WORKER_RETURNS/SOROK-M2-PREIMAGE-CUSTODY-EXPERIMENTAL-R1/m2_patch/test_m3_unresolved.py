"""M3 strict RED-exposing source preimage continuation tests; immutable original M2 candidate."""
from dataclasses import replace,asdict
import pytest
from kernel import seed_scene,State,eligible,propose,fixture_grant,append_test_only,Refusal,digest

def admitted():
 s=seed_scene(); st=State('child',procedure_refs=('old_watchful_habit',))
 c=next(x for x in eligible(s,st,'discussion') if x.source=='parent_said' and x.stance=='REJECT')
 p=propose(s,st,'discussion',c.id,affect_ref='first_distress',public_action_ref='public_lock_check')
 st=append_test_only(s,st,p,fixture_grant(p,'child'))
 return s,st

def test_R3_01_past_heard_words_cannot_change_without_current_lineage_source_collision():
 s,st=admitted(); edited=replace(s.speech[0], words='It was definitely the children of group Z.')
 after=replace(s,speech=(edited,)+s.speech[1:],
     speech_actions=(replace(s.speech_actions[0],speech_hash=digest(asdict(edited))),)+s.speech_actions[1:],
     exposures=(replace(s.exposures[0],speech_hash=digest(asdict(edited))),)+s.exposures[1:])
 with pytest.raises(Refusal,match='SOURCE_PREIMAGE|SOURCE_IDENTITY_COLLISION'):
     eligible(after,st,'later')

def test_R3_02_prior_practical_orientation_cannot_change_unnoticed_after_lineage_append():
 s,st=admitted();child=s.actors[0]
 h=replace(child.history[1],activity='fully different old practical orientation')
 witnesses=tuple(replace(w,history_hash=digest(asdict(h))) if w.actor=='child' and w.history_id==h.id else w for w in s.history_witnesses)
 after=replace(s,actors=(replace(child,history=child.history[:1]+(h,)+child.history[2:]),)+s.actors[1:],history_witnesses=witnesses)
 with pytest.raises(Refusal,match='SOURCE_PREIMAGE|SOURCE_IDENTITY_COLLISION'):
     eligible(after,st,'later')

def test_R3_03_earlier_affective_witness_rewrite_cannot_change_historical_lineage_source():
 s,st=admitted();child=s.actors[0]
 h=replace(child.history[2],activity='happy delight instead of distress')
 witnesses=tuple(replace(w,history_hash=digest(asdict(h))) if w.actor=='child' and w.history_id==h.id else w for w in s.history_witnesses)
 after=replace(s,actors=(replace(child,history=child.history[:2]+(h,)+child.history[3:]),)+s.actors[1:],history_witnesses=witnesses)
 with pytest.raises(Refusal,match='SOURCE_PREIMAGE|SOURCE_IDENTITY_COLLISION'):
     eligible(after,st,'later')
