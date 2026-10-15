"""Exact paired joins, equal case/family weights and explicit assumption limits."""
import math
from collections import defaultdict
from assay.scoring import score
from .data import IntegrityError
def evaluate(rows,captures,key,require_complete=True):
 ids=[r['id'] for r in rows]
 if len(ids)!=len(set(ids)):raise IntegrityError('DUPLICATE_PLANNED_ID')
 if set(captures)-set(ids):raise IntegrityError('UNPLANNED_CAPTURE')
 if require_complete and set(captures)!=set(ids):raise IntegrityError('MISSING_CAPTURE')
 return score(rows,captures,key)
def paired(records,rows,case_ids=None,metric='correct'):
 planned={r['id']:r for r in rows};byblock=defaultdict(dict)
 if len({r['id'] for r in records})!=len(records):raise IntegrityError('DUPLICATE_CAPTURE')
 if {r['id'] for r in records}!=set(planned):raise IntegrityError('MISSING_OR_EXTRA_CAPTURE')
 for r in records:
  row=planned[r['id']]
  if any(r[k]!=row[k] for k in ['block','case','family','k','arm']):raise IntegrityError('JOIN_CONTEXT')
  if case_ids is not None and r['case'] not in case_ids:continue
  if r['arm'] in byblock[r['block']]:raise IntegrityError('DUPLICATE_PAIR_MEMBER')
  byblock[r['block']][r['arm']]=r
 differences={'B':defaultdict(list),'C':defaultdict(list)}
 def value(r):return int(r['correct']) if metric=='correct' else int(r['coded']['action']=='POLICING_CANDIDATE')
 for block,g in byblock.items():
  if set(g)!=set('ABC'):raise IntegrityError('INCOMPLETE_PAIR')
  if len({(x['case'],x['family'],x['k']) for x in g.values()})!=1:raise IntegrityError('PAIR_CONTEXT')
  for arm in 'BC':differences[arm][(g['A']['family'],g['A']['case'])].append(value(g[arm])-value(g['A']))
 result={}
 for arm,case_values in differences.items():
  families=defaultdict(list)
  for (family,case),values in case_values.items():families[family].append(sum(values)/len(values))
  means={f:sum(x)/len(x) for f,x in sorted(families.items())}
  if not means:raise IntegrityError('EMPTY_ANALYSIS')
  delta=sum(means.values())/len(means);radius=math.sqrt(2*math.log(2*12/.05)/len(means))
  result[arm]=dict(delta=delta,family_differences=means,n_constructed_families=len(means),n_matched_blocks=len(byblock),conditional_bounded_interval=[max(-1,delta-radius),min(1,delta+radius)],inference='DESCRIPTIVE_SYNTHETIC_ONLY; INDEPENDENT_FAMILY_SAMPLING_NOT_ESTABLISHED',powered=False)
 return result
def conditional_power_table():
 alpha=.05;m=12;beta=.2
 def precision(e):return math.ceil(2*math.log(2*m/alpha)/e**2)
 def superiority(g):return math.ceil(2*(math.sqrt(math.log(2*m/alpha))+math.sqrt(math.log(1/beta)))**2/g**2)
 def equivalence(e):return math.ceil(2*(math.sqrt(math.log(2*m/alpha))+math.sqrt(math.log(2/beta)))**2/e**2)
 return dict(alpha=alpha,comparisons=m,beta=beta,assumption='Independent sampled family paired means in[-1,1]; no independence established for current convenience fixtures',simultaneous_precision_families={str(e):precision(e) for e in [.05,.1]},conservative_80percent_power_superiority_families={str(g):superiority(g) for g in [.05,.1,.2]},conservative_80percent_power_equivalence_at_true_zero_families={str(e):equivalence(e) for e in [.05,.1]},current_power_claim=False,ICC_variance_model_response_cost='UNKNOWN; independent prospective pilot required before cheaper variance-based design')
