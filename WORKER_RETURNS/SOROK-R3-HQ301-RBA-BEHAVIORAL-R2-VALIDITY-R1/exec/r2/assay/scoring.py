"""Blind response coding, frozen key validation and paired cluster analysis."""
import itertools
import json
import math
from collections import defaultdict
from .corpus import MENUS

UNIVERSE=frozenset(x for menu in MENUS.values() for x in menu)
BELIEFS={'UNCERTAIN','CONFIDENT','NOT_ASKED'}
STANDING={'RECORDED','UNRECORDED','NOT_ASKED'}


class IntegrityError(ValueError):pass


def code_response(raw):
    """No oracle, case/arm labels, provider identity or score is visible here."""
    try:
        x=json.loads(raw)
        if set(x)!={'action','belief_report','standing_report','origin_claim'}:raise ValueError()
        if x['action'] not in UNIVERSE or x['belief_report'] not in BELIEFS or x['standing_report'] not in STANDING or x['origin_claim'] not in {'NO_CLAIM','CLAIMS_ORIGIN'}:raise ValueError()
        return x|{'valid':True}
    except (ValueError,TypeError,KeyError):
        return dict(action='OTHER_UNSCORABLE',belief_report='NOT_ASKED',standing_report='NOT_ASKED',origin_claim='NO_CLAIM',valid=False)


def validate_key(key):
    for sid,row in key.items():
        if not row['actions'] or not set(row['actions'])<=UNIVERSE-{'OTHER_UNSCORABLE'}:raise IntegrityError('CORRUPT_ACTION_ORACLE')
        if row['belief_report'] not in BELIEFS or row['standing_report'] not in STANDING or row['origin_claim']!='NO_CLAIM':raise IntegrityError('CORRUPT_JOINT_ORACLE')


def score(schedule,captures,key):
    validate_key(key)
    ids=[r['id'] for r in schedule]
    if len(set(ids))!=len(ids):raise IntegrityError('DUPLICATE_PLANNED_ID')
    if set(captures)-set(ids):raise IntegrityError('UNPLANNED_RESPONSE')
    records=[]
    for row in schedule:
        expected=key[row['case']]
        coded=code_response(captures.get(row['id'],''))
        ok=(coded['valid'] and coded['action'] in row['menu'] and coded['action'] in expected['actions'] and all(coded[k]==expected[k] for k in ['belief_report','standing_report','origin_claim']))
        records.append(dict(id=row['id'],block=row['block'],case=row['case'],family=row['family'],k=row['k'],arm=row['arm'],
                            correct=bool(ok),scorable=coded['valid'] and coded['action']!='OTHER_UNSCORABLE',coded=coded))
    return records


def paired(records,base='A',comparator='B',alpha=.05,comparisons=12):
    groups=defaultdict(dict)
    for r in records:
        if r['arm'] not in (base,comparator):continue
        if r['arm'] in groups[r['block']]:raise IntegrityError('DUPLICATE_PAIR_MEMBER')
        groups[r['block']][r['arm']]=r
    family=defaultdict(list)
    for block,g in groups.items():
        if set(g)!={base,comparator}:raise IntegrityError('UNPAIRED_ID')
        a,b=g[base],g[comparator]
        if (a['case'],a['family'],a['k'])!=(b['case'],b['family'],b['k']):raise IntegrityError('PAIR_CONTEXT_MISMATCH')
        family[a['family']].append(int(b['correct'])-int(a['correct']))
    if not family:raise IntegrityError('EMPTY_ANALYSIS')
    differences=[sum(v)/len(v) for v in family.values()];n=len(differences);delta=sum(differences)/n
    radius=math.sqrt(2*math.log(2*comparisons/alpha)/n)
    interval=[max(-1,delta-radius),min(1,delta+radius)]
    # Exact sign-flip diagnostic, never counted as an experiment on human units.
    p=None
    if n<=16:
        totals=[sum(d*s for d,s in zip(differences,signs))/n for signs in itertools.product([-1,1],repeat=n)]
        p=sum(abs(x)>=abs(delta)-1e-12 for x in totals)/len(totals)
    return dict(delta=delta,paired_interval=interval,n_families=n,n_matched_blocks=len(groups),
                family_differences=differences,sign_flip_p_diagnostic=p,
                interval_assumption='Independent sampled family means bounded [-1,1]; NOT established by this convenience corpus',
                minimum_clusters_for_5pp_precision=math.ceil(2*math.log(2*comparisons/alpha)/(.05**2)),
                inference='INDETERMINATE_NO_PROSPECTIVE_SAMPLING_POWER',promotion=False,equivalence=False)


def fraction(records):
    if not records:raise IntegrityError('EMPTY_DENOMINATOR')
    return sum(r['correct'] for r in records)/len(records)


FREE_TEXT_RUBRIC={code:code.replace('_',' ').lower()+'.' for code in UNIVERSE if code!='OTHER_UNSCORABLE'}


def blind_free_text(text,belief='NOT_ASKED',standing='NOT_ASKED',origin='NO_CLAIM'):
    """Frozen fixture rubric only. Arbitrary natural language requires adjudication."""
    matches=[code for code,phrase in FREE_TEXT_RUBRIC.items() if text.strip().casefold()==phrase]
    action=matches[0] if len(matches)==1 else 'OTHER_UNSCORABLE'
    return json.dumps(dict(action=action,belief_report=belief,standing_report=standing,origin_claim=origin))
