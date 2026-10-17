"""Prospective P6 source-view integrity regressions against actual pinned code."""
import copy,json,sys
from dataclasses import replace
from pathlib import Path
import pytest
from phase_b_support_v1 import w,plan,execute,profile_calls,OP

R=Path(__file__).resolve().parents[1]
EVENTS=[]
@pytest.fixture(scope='session',autouse=True)
def save():
 yield
 (R/'observations/fresh_source_binding_events.json').write_text(json.dumps(EVENTS,indent=2,default=str)+'\n')

def bad_pointer(p,kind):
 valid=p.releases['REL-A-W1'].source_artifact_ref
 foreign=p.releases['REL-A-W2'].source_artifact_ref
 values={'other_release':foreign,
         'same_hash_foreign_id':w.ExactRef('SOURCE_SNAPSHOT',foreign.object_id,valid.content_hash),
         'same_id_wrong_hash':w.ExactRef('SOURCE_SNAPSHOT',valid.object_id,foreign.content_hash),
         'wrong_kind':w.ExactRef('SOURCE_ARTIFACT',valid.object_id,valid.content_hash),
         'actual_artifact':p.repository.resolve_release_exact(p.releases['REL-A-W1'].release_ref).source_artifact_ref,
         'missing':None}
 return values[kind]

def changed_plan(p,pointer):
 releases=dict(p.releases);releases['REL-A-W1']=replace(releases['REL-A-W1'],source_artifact_ref=pointer)
 return replace(p,releases=releases)

@pytest.mark.parametrize('tag',['REL-A-W1','REL-A-W2','REL-B-W2'])
def test_exact_reconstructed_view_matches_owner_qualified_c11_snapshot(tag):
 p=plan();r=p.releases[tag];fresh=replace(r,source_artifact_ref=w.ExactRef(**r.source_artifact_ref.as_dict()))
 actual=r.repo.resolve_release_exact(r.release_ref);material=w._release_material(fresh)
 assert fresh.source_artifact_ref in actual.replay_manifest.closure_refs
 assert w.digest(material)==p.fixture_owner._issued()['native_sources'][r.release_ref.key]
 assert material['source_view_binding']['view_source_snapshot']==fresh.source_artifact_ref.as_dict()
 assert material['source_view_binding']['source_artifact']==actual.source_artifact_ref.as_dict()
 assert material['source_view_binding']['release']==r.release_ref.as_dict()
 EVENTS.append(dict(positive=tag,binding=material['source_view_binding']))

@pytest.mark.parametrize('stage',['precompile','callback','run','consumer','restore'])
@pytest.mark.parametrize('kind',['other_release','same_hash_foreign_id','same_id_wrong_hash','wrong_kind','actual_artifact','missing'])
def test_source_pointer_refuses_at_every_boundary_before_new_i03(stage,kind):
 p=plan();receipts=None;checkpoint=None
 if stage in ('consumer','restore'):
  _,receipts,_=execute(p)
  if stage=='restore':checkpoint=w.create_checkpoint(p,receipts)
 bad=changed_plan(p,bad_pointer(p,kind))
 if stage=='restore':bad=replace(bad,fact_custody=w.FactCustody(),prior_receipts=())
 prior=p.fact_custody.snapshot();bad_prior=bad.fact_custody.snapshot()
 journal=copy.deepcopy(p.fixture_owner._issued());calls=[]
 sys.setprofile(profile_calls(calls))
 try:
  with pytest.raises(w.IdentityError) as exc:
   if stage=='precompile':
    releases=w.Releases(bad.releases);releases.fixture_owner=p.fixture_owner;plan(releases=releases)
   elif stage=='callback':w.make_executor(bad)(p.units_by_op[OP])
   elif stage=='run':w.run_plan(bad,w.make_executor(bad))
   elif stage=='consumer':w.consumer_effects(bad,receipts)
   else:w.restore_from_checkpoint(checkpoint,bad)
 finally:sys.setprofile(None)
 assert not any(c['name']=='execute_empirical_query' for c in calls)
 assert p.fact_custody.snapshot()==prior and bad.fact_custody.snapshot()==bad_prior
 assert p.fixture_owner._issued()==journal
 assert bad.prior_receipts==(() if stage=='restore' else p.prior_receipts)
 EVENTS.append(dict(stage=stage,kind=kind,error=type(exc.value).__name__,reason=str(exc.value),new_i03_calls=0,
                    owner_journal_unchanged=True,fact_custody_unchanged=True,callbacks=calls))

@pytest.mark.parametrize('part',['source_material','contract','both'])
def test_caller_rehashing_does_not_register_foreign_snapshot(part):
 p=plan();bad=changed_plan(p,bad_pointer(p,'other_release'))
 source=json.loads(p.source_material);source['REL-A-W1']['source_view_binding']['view_source_snapshot']=bad.releases['REL-A-W1'].source_artifact_ref.as_dict()
 contract=json.loads(p.contract);contract['caller_source_view']=source
 if part in ('source_material','both'):bad=replace(bad,source_material=w.canonical(source))
 if part in ('contract','both'):bad=replace(bad,contract=w.canonical(contract))
 journal=copy.deepcopy(p.fixture_owner._issued());calls=[];sys.setprofile(profile_calls(calls))
 try:
  with pytest.raises(w.IdentityError):w.make_executor(bad)(p.units_by_op[OP])
 finally:sys.setprofile(None)
 assert not any(c['name']=='execute_empirical_query' for c in calls)
 assert p.fixture_owner._issued()==journal

def test_native_ingest_registration_cannot_requalify_a_foreign_view():
 p=plan();bad=changed_plan(p,bad_pointer(p,'other_release'));before=copy.deepcopy(p.fixture_owner._issued())
 with pytest.raises(w.IdentityError):p.fixture_owner._register_native_sources(bad.releases)
 assert p.fixture_owner._issued()==before

@pytest.mark.parametrize('field,value',[('release_tag','REL-A-W2'),('source_edition','FOREIGN_EDITION'),('member_ids',('R11','R12','R13','R14','R15','R16'))])
def test_original_descriptor_repairs_remain_closed_with_same_counts(field,value):
 p=plan();specs=dict(p.op_specs);specs[OP]=replace(specs[OP],**{field:value});bad=replace(p,op_specs=specs)
 calls=[];sys.setprofile(profile_calls(calls))
 try:
  with pytest.raises(w.IdentityError):w.make_executor(bad)(p.units_by_op[OP])
 finally:sys.setprofile(None)
 assert not any(c['name']=='execute_empirical_query' for c in calls)

@pytest.mark.parametrize('attack',['revoke','source_drift'])
def test_source_binding_does_not_resurrect_current_rights_or_old_source(attack):
 p=plan()
 if attack=='revoke':p.fixture_owner.revoke('REL-A-W1')
 else:
  state=p.fixture_owner.state();state['source_digests']['REL-A-W1']='0'*64
  w.atomic_write(p.fixture_owner.directory/'current.json',w.canonical(state))
 calls=[];sys.setprofile(profile_calls(calls))
 try:
  with pytest.raises((w.RevocationError,w.IdentityError)):w.make_executor(p)(p.units_by_op[OP])
 finally:sys.setprofile(None)
 assert not any(c['name']=='execute_empirical_query' for c in calls)
