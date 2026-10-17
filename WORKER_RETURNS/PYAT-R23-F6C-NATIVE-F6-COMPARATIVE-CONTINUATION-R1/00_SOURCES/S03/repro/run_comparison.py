"""Replay the one synthetic comparison and contribution/value receipts."""
from pathlib import Path
import sys
import json
from fractions import Fraction as F
from copy import deepcopy
import time
import resource

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from rawlsing_next.pre553_heterogeneous_synthesis import synthesize, conditional
from rawlsing_next.pre553_empirical_objects import semantic_hash
from fixtures import fixtures, CELLS

RETURN = Path(__file__).resolve().parents[1]


def distribution(b):
    return {tuple(c["categories"]): F(c["probability"]) for c in b["candidate"]["distribution"]}


def native(source):
    totals = dict.fromkeys(CELLS, F(0))
    for z in source["strata"].values():
        for c in z["cells"]:
            k = tuple(a["category_map"][v] for a,v in zip(source["axes"], c["categories"]))
            totals[k] += F(c["mass"])
    n = sum(totals.values())
    return {k:v/n for k,v in totals.items()}


def tv(p,q):
    return sum(abs(p.get(k,0)-q.get(k,0)) for k in set(p)|set(q))/2


def write(name, value):
    if '--write' in sys.argv:
        (RETURN / name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')
    elif name != 'COMPARISON_RESOURCE_RECEIPT.json':
        assert json.loads((RETURN / name).read_text()) == value, f'replay mismatch: {name}'


def main():
    started=time.perf_counter()
    t,s,p=fixtures()
    protocol=json.loads((RETURN/'repro/HELDOUT_PROTOCOL.json').read_text())
    equal=synthesize(t,s,p)
    write('SYNTHETIC_WORLD_BUNDLE.json',equal)
    scenarios={}
    for label, weights in [('A_only', {'A':1}),('A_B_equal',{'A':1,'B':1}),('A_triple_B',{'A':3,'B':1}),('B_only',{'B':1})]:
        selected=[x for x in s if x['source_id'] in weights]
        policy=deepcopy(p);policy['source_weights']=weights
        b=synthesize(t,selected,policy)
        scenarios[label]={'distribution':b['candidate']['distribution'],
                          'consumer_receipt':conditional(b,{'material_security':'secure'},'employment_position'),
                          'bundle_hash':b['content_hash'], 'contribution_graph':b['candidate']['support']}
    write('CONTRIBUTION_VALUE_RECEIPTS.json',scenarios)
    target_counts=protocol['same_target_validation_counts']
    validation=dict(zip(CELLS,(F(x,sum(target_counts)) for x in target_counts)))
    adverse_counts=protocol['adverse_target_counts']
    adverse=dict(zip(CELLS,(F(x,sum(adverse_counts)) for x in adverse_counts)))
    # Strict no-pooling baseline: score each source separately, never collapse
    # those tables into an allegedly observed population distribution.
    results={'schema':'S03_COMPARISON@1','test_origin':True,
             'protocol_hash':semantic_hash(protocol),'method':'one candidate: target-stratum joint standardization',
             'baseline':'separate native mapped source joints; scores at same declared validation target',
             'idealized_target_validation':{'origin':'fixed synthetic holdout counts, not survey calibration',
                 'baseline_TV_by_source':{x['source_id']:str(tv(native(x),validation)) for x in s},
                 'candidate_TV':str(tv(distribution(equal),validation))},
             'unmeasured_source_shift_adversary':{
                 'baseline_TV_by_source':{x['source_id']:str(tv(native(x),adverse)) for x in s},
                 'candidate_TV':str(tv(distribution(equal),adverse)),
                 'implication':'Target share adjustment cannot repair noninvariant conditional joint laws.'}}
    # Leave B entirely out of fitting. Its known synthetic stratum shares define
    # the transfer target. B's joint cells are used only for validation below.
    heldout_t=deepcopy(t);heldout_t['target_id']='SYNTHETIC_B_SAMPLE_TRANSFER'
    heldout_t['strata']={'majority':'1/5','minority':'4/5'}
    heldout_p=deepcopy(p);heldout_p['source_weights']={'A':1}
    fit=synthesize(heldout_t,s[:1],heldout_p)
    heldout=dict(zip(CELLS,(F(x,100) for x in protocol['source_B_heldout_counts'])))
    subgroup={}
    for z in t['strata']:
        def stratum(source):
            totals={tuple(a['category_map'][v] for a,v in zip(source['axes'],c['categories'])):F(c['mass']) for c in source['strata'][z]['cells']}
            n=sum(totals.values());return {k:v/n for k,v in totals.items()}
        subgroup[z]={'TV_before_and_after':str(tv(stratum(s[0]),stratum(s[1]))),
                     'interpretation':'No within-stratum model improvement is claimed.'}
    results['leave_B_out_transfer']={'fitted_sources':['A'],'heldout_source':'B',
                                     'native_A_TV':str(tv(native(s[0]),heldout)),
                                     'standardized_A_TV':str(tv(distribution(fit),heldout)),
                                     'subgroups':subgroup,'real_source_validation':False}
    results['decision']={'synthetic':'Candidate improves composition-shift behavior, fails unmeasured law shift; retain native baseline alongside any candidate.',
                         'real':'NO_REPLACEMENT; no S00/rights/metadata qualification or empirical comparison',
                         'full_F6':'NOT_ESTABLISHED', 'independent_review':'PENDING'}
    # Acceptance thresholds were declared before comparison, not inferred from a
    # production output. These are explicit writer-controlled synthetic oracles.
    assert results['idealized_target_validation']['candidate_TV']=='0'
    assert F(results['leave_B_out_transfer']['standardized_A_TV']) < F(results['leave_B_out_transfer']['native_A_TV'])
    assert F(results['unmeasured_source_shift_adversary']['candidate_TV']) > F(results['unmeasured_source_shift_adversary']['baseline_TV_by_source']['B'])
    write('CANDIDATE_VERSUS_BASELINE_RESULTS.json',results)
    write('COMPARISON_RESOURCE_RECEIPT.json',{'elapsed_seconds':format(time.perf_counter()-started,'.6f'),
          'process_peak_rss_platform_units':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'rss_units':'bytes on macOS; KiB on Linux','interpreter':sys.executable,
          'code_sha256':__import__('hashlib').sha256((ROOT/'rawlsing_next/pre553_heterogeneous_synthesis.py').read_bytes()).hexdigest(),
          'dependencies':'Python standard library and existing semantic_hash owner',
          'paid_or_external_execution':False})
    print(json.dumps(results,indent=2))


if __name__=='__main__': main()
