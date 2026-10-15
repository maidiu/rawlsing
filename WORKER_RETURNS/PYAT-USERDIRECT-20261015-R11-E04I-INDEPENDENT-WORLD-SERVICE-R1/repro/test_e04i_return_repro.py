"""Independent E04I sourcefree native 58-row oracle, NOT actual PRE553 owners.

This standalone pytest requires stdlib + pytest, no source issuance.
"""
from collections import Counter
from fractions import Fraction
from copy import deepcopy
import pytest

STRATA={'111':(6,2),'110':(4,4),'101':(5,3),'100':(3,5),
        '011':(4,2),'010':(2,4),'001':(3,3),'000':(2,6)}

def rows():
    return [{**dict(zip('ABC',map(int,code))),'Y':y,'id':f'{code}-{y}-{i}'}
            for code,(yes,no) in STRATA.items() for y,n in ((1,yes),(0,no)) for i in range(n)]

def query(data,target,conditions,permit=None):
    allowed={'Y':('A','B','C'),'A':('Y',)} if permit is None else permit
    if target not in allowed or not conditions or len(set(k for k,v in conditions))!=len(conditions) or any(k not in allowed[target] or type(v)!=int or v not in (0,1) for k,v in conditions):
        raise ValueError('AUTHORITY_OR_RISK_SET_REFUSED')
    matched=[r for r in data if all(r[k]==v for k,v in conditions)]
    counts=Counter(r[target] for r in matched)
    return dict(n=len(matched),yes=counts[1],no=counts[0],p=Fraction(counts[1],len(matched)) if matched else None)

def progressive(data):
    cond=(('A',1),('B',1),('C',1))
    return [query(data,'Y',cond[:n]) for n in range(1,4)]

def changed(data):
    out=deepcopy(data);next(r for r in out if (r['A'],r['B'],r['C'],r['Y'])==(1,1,1,0))['Y']=1;return out

def test_58_rows_eight_independent_strata():
    data=rows();assert len(data)==58 and len(STRATA)==8
    assert Counter(''.join(str(r[k]) for k in 'ABC') for r in data)=={k:sum(v) for k,v in STRATA.items()}

def test_three_progressive_native_exact_fractions():
    results=progressive(rows());assert [(x['yes'],x['no'],x['n'],x['p']) for x in results]==[(18,14,32,Fraction(9,16)),(10,6,16,Fraction(5,8)),(6,2,8,Fraction(3,4))]

def test_independently_authorized_reverse_not_bayes_guess():
    q=query(rows(),'A',[('Y',1)]);assert (q['yes'],q['no'],q['n'],q['p'])==(18,11,29,Fraction(18,29))

def test_reverse_role_cannot_reuse_forward_grant():
    with pytest.raises(ValueError):query(rows(),'A',[('Y',1)],permit={'Y':('A','B','C')})

def test_absent_joint_or_duplicate_binding_is_not_positive():
    for target,conditions in [('B',[('Y',1)]),('Y',[('A',1),('A',1)])]:
        with pytest.raises(ValueError):query(rows(),target,conditions)

def test_real_single_native_row_change_updates_all_three():
    before=rows();after=changed(before)
    assert [(r['yes'],r['no'],r['n'],r['p']) for r in progressive(after)]==[(19,13,32,Fraction(19,32)),(11,5,16,Fraction(11,16)),(7,1,8,Fraction(7,8))]
    assert query(before,'A',[('Y',1)])['n']==29

def test_support_loss_is_zero_support_not_zero_probability():
    data=[r for r in rows() if (r['A'],r['B'],r['C'])!=(1,1,1)]
    r=progressive(data);assert [x['n'] for x in r]==[24,8,0]
    assert r[0]['p']==Fraction(1,2) and r[2]['p'] is None

def test_empirical_vs_structural_independence():
    base={'training_access':True,'training_fee':2,'exit_cost':2,'civil_open':True,'civil_sanction':False}
    closed={**base,'training_access':False,'exit_cost':8}
    assert progressive(rows())==progressive(rows())
    assert closed['training_access'] is False and closed['exit_cost']==8 and closed['civil_open']==base['civil_open']
    assert progressive(changed(rows()))!=progressive(rows())

def test_sanction_is_not_emprical_evidence():
    base={'civil_open':True,'civil_sanction':False};sanction={**base,'civil_sanction':True}
    assert base['civil_open'] and not sanction['civil_sanction'] is False
    assert progressive(rows())==progressive(rows())
