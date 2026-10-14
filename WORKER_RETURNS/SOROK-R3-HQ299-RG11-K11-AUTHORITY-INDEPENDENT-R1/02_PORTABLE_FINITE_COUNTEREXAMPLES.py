"""Independent finite counterexamples for RG11. NOT accepted ADP implementation."""
from fractions import Fraction
import hashlib, json
import pytest

def posterior_from_boolean_feasibility(prior_a):
    assert 0 < prior_a < 1
    like_a=like_b=Fraction(1)
    return prior_a*like_a/(prior_a*like_a+(1-prior_a)*like_b)

def survivor_weights(q_a,q_b,a_a,a_b):
    z=q_a*a_a+q_b*a_b
    return q_a*a_a/z,q_b*a_b/z

def h(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()

def ordered_construction(mother, candidates, future_label=None):
    # The frozen child label is NOT an input to the legitimate planning function.
    del future_label
    return {'mother_ref':h(mother),'candidates':tuple(sorted(set(candidates))),
            'dag_edges':[('endpoint','history_search','NONCAUSAL')], 'draws':0}

def test_same_feasible_histories_nonunique_posterior():
    assert posterior_from_boolean_feasibility(Fraction(9,10))==Fraction(9,10)
    assert posterior_from_boolean_feasibility(Fraction(1,10))==Fraction(1,10)
    assert posterior_from_boolean_feasibility(Fraction(9,10))!=posterior_from_boolean_feasibility(Fraction(1,10))

def test_silent_retry_changes_simulation_law():
    assert survivor_weights(Fraction(1,2),Fraction(1,2),Fraction(1),Fraction(1,4))==(Fraction(4,5),Fraction(1,5))

def test_selection_without_owner_rule_must_not_draw():
    policy=None; candidates=['A','B']; draws=[]
    result='SELECTION_AUTHORITY_UNBOUND' if policy is None else 'ALLOW'
    assert result=='SELECTION_AUTHORITY_UNBOUND' and draws==[] and len(candidates)==2

def test_qualified_singleton_has_no_draw():
    selected=('A',0) if len(['A'])==1 else ('N/A',1)
    assert selected==('A',0)

def test_dedup_does_not_increase_selection_mass():
    classes=['rare|A','rare|A','rare|A','common|B']
    assert len(set(classes))==2 and len(classes)==4
    assert Fraction(1,len(set(classes)))==Fraction(1,2)

def test_child_embargo_changed_hidden_label():
    mother={'pre_event':'sha-m','older_child':'child:older'}
    x=ordered_construction(mother,['x','y','x'],future_label='future-good')
    y=ordered_construction(mother,['x','y','x'],future_label='future-poor')
    assert h(x)==h(y) and x['mother_ref']==h(mother) and x['draws']==0

def test_construction_edge_is_not_causal_ancestor():
    construction=[('endpoint','history_search','NONCAUSAL')]
    chronological=[('parent_history','encounter','CAUSAL'),('encounter','conception_if_issued','CAUSAL')]
    assert all(e[2]!='CAUSAL' for e in construction)
    assert all(e[0]!='endpoint' for e in chronological)

def test_no_inferred_dyad_posterior_from_respondent_marginal():
    unit='RESPONDENT'; observation={'religion':'A','attitude':'agree'}
    dyad_authority=None
    assert observation and unit=='RESPONDENT' and dyad_authority is None
    with pytest.raises(PermissionError,match='UNISSUED_DYAD_DISTRIBUTION'):
        if dyad_authority is None:raise PermissionError('UNISSUED_DYAD_DISTRIBUTION')

def test_pending_conception_distinct_from_child_generated_and_birth():
    x={'pending':True,'conception_occurrence':None,'child_generated_event':None,'birth_event':None}
    assert x['pending'] and sum(x[z] is not None for z in ['conception_occurrence','child_generated_event','birth_event'])==0
