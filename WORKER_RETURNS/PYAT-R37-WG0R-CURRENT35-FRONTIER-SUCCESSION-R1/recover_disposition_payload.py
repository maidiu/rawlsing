"""Reproduce exact frozen bytes. Recall projections have no issuance authority.

The sole acceptance gate is the original payload SHA plus exact P2 identity.
No candidate, diagnostic projection or aggregate count can replace that gate.
"""
import csv
import hashlib
import io
import json
from pathlib import Path
from account_current35 import ROOT, P2_SHA, PACK_SHA


def recover():
    custody=json.loads((ROOT/'evidence/disposition_recovery_input_custody.json').read_text())
    for row in custody:
        if hashlib.sha256((ROOT/row['projection_path']).read_bytes()).hexdigest()!=row['projection_sha256']:
            raise ValueError('RECOVERY_INPUT_CUSTODY_MISMATCH')
    p2data=(ROOT/'sources/local_archive/Rawlsing_P2_Phase0_Question_Node_Skeleton_v1.csv').read_bytes()
    if hashlib.sha256(p2data).hexdigest()!=P2_SHA:raise ValueError('P2_IDENTITY_MISMATCH')
    p2=list(csv.DictReader(io.StringIO(p2data.decode('utf-8-sig'))))
    ids={r['question_implementation_id'] for r in p2}
    if len(ids)!=18276 or len(p2)!=18276:raise ValueError('P2_CARDINALITY_MISMATCH')
    floor=ROOT/'sources/recovered_disposition'
    def keyed(name,full=True):
        rows=list(csv.DictReader((floor/name).open()));result={r['question_implementation_id']:r for r in rows}
        if len(result)!=len(rows) or (full and set(result)!=ids):raise ValueError('RECOVERY_IDENTITY_ANTI_JOIN')
        return result
    s00=keyed('s00_workstreams.csv');routing=keyed('o06_routing.csv')
    o07=keyed('o07_recall_projection.csv');o9=keyed('o08_o09_conditioners.csv')
    work=keyed('o04_worker_states.csv',False)
    accepted=set(json.loads((floor/'o04_accepted_ids.json').read_text()))
    codes={'S1_RELATIONAL_SEMANTIC_RECONCILIATION':0,'S1A_GOVERNED_ANCHOR_RECONCILIATION':0,
           'S2_STRUCTURAL_CHOICE_ADJUDICATION':1,'S2_SOURCE_TOPOLOGY_REVIEW':1,
           'R1_P5_RESPONDENT_POSITION_GOVERNANCE':2,'R1_P5_CONTEXT_GOVERNANCE':4,
           'R1_P5_STRUCTURAL_CONTEXT_GOVERNANCE':5,'S00_TERMINAL_ADMINISTRATIVE_NONRELATION_USE':6,
           'R1_P5_CONTEXT_POSITION_GOVERNANCE':8,'S00_BLOCKED_SOURCE_REVIEW_REQUIRED':9}
    conditional={'RESPONDENT_ANSWER_CONDITIONAL','COUNTRY_CONDITIONAL','MULTI_CONDITION',
                 'SPLIT_SAMPLE_CONDITIONAL','DEMOGRAPHIC_OR_ELIGIBILITY_CONDITIONAL','MODULE_OR_BALLOT_CONDITIONAL'}
    payload=[]
    for row in p2:
        q=row['question_implementation_id'];stream=s00[q]['s0_next_workstream']
        if stream=='S2B_BEHAVIOR_EXPOSURE_ENDPOINT_REVIEW':
            # Existing central report explicitly extends the feelevel block to
            # earlier-wave instances; accepted set is retained central ancestry.
            code=3 if q in accepted else 9 if ('BLOCK' in work[q]['s2b_terminal_disposition'] or row['source_variable_code']=='feelevel') else 7
        else:code=codes[stream]
        route=routing[q]['routing_status']
        held=(code==9 or route=='SOURCE_ROUTING_UNRESOLVED'
              or o07[q]['current_o07_measurement_use_class_DIAGNOSTIC_ONLY']=='UNRESOLVED'
              or o9[q]['o08_position_lane']=='POSITION_SEMANTICS_UNRESOLVED'
              or o9[q]['p5_conditioner_disposition']=='P5_CONDITIONER_SEMANTICS_UNRESOLVED')
        payload.append(code+16*held+32*(route in conditional))
    data=bytes(payload)
    if len(data)!=18276 or hashlib.sha256(data).hexdigest()!=PACK_SHA:
        raise ValueError('RECOVERY_NOT_THE_FROZEN_ORIGINAL_PAYLOAD')
    return data


if __name__=='__main__':
    data=recover()
    print(json.dumps({'state':'EXACT_FROZEN_PAYLOAD_RECOVERED','bytes':len(data),
                      'sha256':hashlib.sha256(data).hexdigest(),'p2_sha256':P2_SHA}))
