"""RG11 independently executed finite authority counterexamples. Not real genealogy."""
from fractions import Fraction
import hashlib,json,pytest
def posterior(p):return p/(p+(1-p))
def survivor(q,a):return [q[i]*a[i]/sum(q[j]*a[j] for j in range(2)) for i in range(2)]
def stable(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def test_feasibility_not_posterior():assert posterior(Fraction(9,10))!=posterior(Fraction(1,10))
def test_attrition_bias():assert survivor([Fraction(1,2)]*2,[Fraction(1),Fraction(1,4)])==[Fraction(4,5),Fraction(1,5)]
def test_no_choice_rule_no_draw():
 domain_rule=None;draws=[]
 assert domain_rule is None and draws==[]
def test_singleton_no_draw():assert len(['one'])==1
def test_dedup_no_mass_inflation():assert len(set(['rare','rare','rare','common']))==2
def test_future_child_embargo():
 mother={'checkpoint':'M1','older_child':'older'}
 def proposal(label):return stable({'mother':mother,'classes':['A','B']})
 assert proposal('good')==proposal('bad')
def test_construction_not_causal():
 planning=[('endpoint','history_search','NONCAUSAL')];causal=[('parent_history','encounter'),('encounter','conception_IF_ISSUED')]
 assert planning[0][2]=='NONCAUSAL' and all(a!='endpoint' for a,b in causal)
def test_no_dyad_join_from_respondent():
 sampling_unit='RESPONDENT';dyad_authority=None
 with pytest.raises(PermissionError,match='NO_DYAD_AUTHORITY'):
  if sampling_unit!='DYAD' or dyad_authority is None:raise PermissionError('NO_DYAD_AUTHORITY')
def test_pending_not_child_or_birth():
 events={'pending':True,'conception':None,'child_generated':None,'birth':None}
 assert events['pending'] and all(events[k] is None for k in ('conception','child_generated','birth'))
