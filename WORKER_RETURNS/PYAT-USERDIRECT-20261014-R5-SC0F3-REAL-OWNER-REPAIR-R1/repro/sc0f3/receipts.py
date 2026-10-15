"""Reuse the frozen two-contract language, with readable bound carriers."""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator
from sc0f.strict_receipts import build_world_receipt, build_possibility_receipt
from .common import digest, require, semantic_selection


def schema():
    path=Path(__file__).resolve().parents[1]/'inputs/port/oracles/01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json'
    return json.loads(path.read_text())


def refs(x):
    if isinstance(x,dict):
        if set(x)=={'kind','id','hash'}:
            yield x
        else:
            for v in x.values():yield from refs(v)
    elif isinstance(x,list):
        for v in x:yield from refs(v)


def refkey(ref):return ref['kind']+'|'+ref['id']+'|'+ref['hash']


def build(selection, native, effects, possibility):
    carriers={}
    def bind(kind,ident,value):
        r=dict(kind=kind,id=ident,hash=digest(value));carriers[refkey(r)]=copy.deepcopy(value);return r
    w=selection['world']
    value_refs=[]
    for cid,effect in effects.items():
        effect['values_read_refs']=[bind('VALUE_READ',cid+':'+k,v) for k,v in sorted(effect['values_read'].items())]
        effect['empirical_read_ref']=bind('EMPIRICAL_READ',cid,native['geometry'])
        effect['consumer_digest']=bind('CONSUMER_EFFECT',cid,effect['output'])
        value_refs.extend(effect['values_read_refs']+[effect['empirical_read_ref']])
    wr=build_world_receipt(request_id='sc0f3:'+digest(selection['demand'])[:16],selection=selection,values_read_refs=value_refs)
    wr['snapshot_ref']=bind('SNAPSHOT','selected-world',semantic_selection(selection))
    wr['demand_ref']=bind('DEMAND','actual-demand',selection['demand'])
    all_values={**w['values'],**w['routes']}
    for row in wr['selection']:
        key=row['demand_key']
        if key in all_values:
            row['object_ref']=bind('WORLD_OBJECT',key,all_values[key])
            row['dependency_refs']=[row['object_ref']]
    for row in wr['payloads']:
        key=row['object_ref']['id']
        row['object_ref']=bind('WORLD_OBJECT',key,all_values[key])
        row['payload_ref']=bind('PAYLOAD',key,all_values[key])
    # Full world carrier preserves every semantic extension, 12 scoped negative
    # payloads, F1/F2, clocks, categories, H3 and independent structural support.
    extra=copy.deepcopy(wr['payloads'][0])
    extra.update(object_ref=bind('WORLD_OBJECT','complete-world',w),
                 payload_ref=bind('PAYLOAD','complete-world',w),object_family='OTHER_PRODUCER_OWNED')
    wr['payloads'].append(extra)
    closure=dict(world=w,demand=selection['demand'],source_complete=True)
    wr['dependency_closure']['closure_ref']=bind('CLOSURE','actual-native-closure',closure)
    wr['refresh']['binding_fingerprint']=digest(w['generated_binding_echo'])
    pr=build_possibility_receipt(receipt_id='sc0f3:poss',world_snapshot_ref=wr['snapshot_ref'],
                               possibility=possibility,values_read_refs=value_refs)
    # N10E computes empirical geometry independently of structural world values.
    # Joining their inputs to proposal consumers does not issue an N10W model.
    pr['world_binding_requirement']='N10E_ALONE'
    pr['target_ref']=bind('TARGET','native-target',native['query']['target_ref'])
    pr['source_universe_ref']=bind('SOURCE_UNIVERSE','native-universe',native['query']['source_universe_ref'])
    pr['release_ref']=bind('RELEASE','native-release',native['query']['release_ref'])
    pr['same_respondent_joint_ref']=bind('SAME_RESPONDENT_JOINT','native-geometry',native['geometry'])
    pr['response_routing_ref']=bind('RESPONSE_ROUTING','native-denominator',native['geometry']['denominator'])
    for option,cell in zip(pr['options'],native['geometry']['cells']):
        option['value_ref']=bind('VALUE',str(cell['cell']),cell)
    for step in pr['ordered_steps']:
        step['evidence_ref']=bind('EVIDENCE','native-evidence',native['native_result'])
        step['denominator_ref']=bind('DENOMINATOR','native-denominator',native['geometry']['denominator'])
        step['empirical_query_ref']=bind('EMPIRICAL_QUERY','native-query',native['query'])
    pr['replay_ref']=bind('REPLAY','native-executed-replay',native['native_result'])
    wr['receipt_ref']=bind('WORLD_RECEIPT','sc0f3-world',{k:v for k,v in wr.items() if k!='receipt_ref'})
    pr['receipt_ref']=bind('POSSIBILITY_RECEIPT','sc0f3-possibility',{k:v for k,v in pr.items() if k!='receipt_ref'})
    # All remaining refs are declared TEST_ONLY identifier carriers inherited
    # from the existing serializer, never fictional independent evidence.
    for r in list(refs([wr,pr,effects])):
        if refkey(r) not in carriers:
            require(r['hash']==digest(r['id']), 'INTEGRITY_FAILURE','Unresolved serializer ref')
            carriers[refkey(r)]=r['id']
    result=dict(world_receipt=wr,possibility_receipt=pr,consumer_effects=effects,
                carriers=carriers,native_computation=native,
                grade='SOURCEFREE_INTERFACE_CANDIDATE',person_generation='NONE')
    result['carrier_digest']=digest(result)
    verify(result)
    return result


def verify(bundle):
    validator=Draft202012Validator(schema())
    for key in ('world_receipt','possibility_receipt'):
        validator.validate(bundle[key])
        receipt=bundle[key]
        require(receipt['receipt_ref']['hash']==digest({k:v for k,v in receipt.items() if k!='receipt_ref'}),
                'INTEGRITY_FAILURE','Stale receipt identity')
    require(bundle['carrier_digest']==digest({k:v for k,v in bundle.items() if k!='carrier_digest'}),
            'INTEGRITY_FAILURE','Carrier/effects tampered')
    require(set(bundle['consumer_effects'])=={'CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY','NONPARENT_APPRENTICESHIP_ENTRY'},
            'INTEGRITY_FAILURE','Complete two-consumer carrier required')
    for r in refs([bundle['world_receipt'],bundle['possibility_receipt'],bundle['consumer_effects']]):
        require(refkey(r) in bundle['carriers'] and digest(bundle['carriers'][refkey(r)])==r['hash'],
                'INTEGRITY_FAILURE','Absent or altered reference carrier')
    for effect in bundle['consumer_effects'].values():
        require(effect['consumer_digest']['hash']==digest(effect['output']), 'INTEGRITY_FAILURE','Consumer effect changed')
    return True
