#!/usr/bin/env python3
"""Valid sourcefree comparator readback at R6 P2 design scope, then hostile selection mutations.

All synthetic files are newly created test receipts, never real source or runtime results.
The full Git K3 source audit and independently qualified H1 are separate and NOT performed.
"""
import sys,json,hashlib,copy,pathlib,tempfile
from test_r6 import r6_fixture,numeric_fixture
from r5_contract import check_spine

def run():
    s=r6_fixture();s['outcome']='DESIGN_READY_SCOPED'
    s['decisions'][1]['alternatives'][1]['status']='ELIMINATED'
    for d in s['decisions']:
        for x in d['discriminators']:x['status']='RESOLVED'
        if d['class'] in ('PHYSICAL','PRESERVE'):
            d['invariants']={k:'PASS_AT_SCOPE' for k in d['invariants']}
    with tempfile.TemporaryDirectory() as dirname:
        root=pathlib.Path(dirname);data,frozen=numeric_fixture()
        for item in data['measurements']:
            for side in ('A','B'):
                p=root/item[side]['receipt_path']
                payload=json.dumps({'test_only':True,'case':item['cell_id'],'side':side}).encode()
                p.write_bytes(payload);item[side]['receipt_sha256']=hashlib.sha256(payload).hexdigest()
        for v in data['hard_veto_checks']:
            v['receipt_path']='veto_'+v['id'];payload=json.dumps({'synthetic':True,'veto':v['id']}).encode()
            (root/v['receipt_path']).write_bytes(payload);v['receipt_sha256']=hashlib.sha256(payload).hexdigest()
        dpath=root/'comparison.json';fpath=root/'frozen.json'
        dpath.write_text(json.dumps(data));fpath.write_text(json.dumps(frozen))
        s['comparison_receipt']={'input_path':dpath.name,'input_sha256':hashlib.sha256(dpath.read_bytes()).hexdigest(),'frozen_path':fpath.name,'frozen_sha256':hashlib.sha256(fpath.read_bytes()).hexdigest(),'declared_verdict':'A_DOMINATES_FULL_MATERIAL_DIMENSIONS','declared_winner':'A','physical_decision_id':'DK-PHYSICAL'}
        s['physical_decision_evidence']=[{'decision_id':'DK-PHYSICAL','selected_alternative_id':'A-P','selected_candidate':'A','material_cell_ids':[x['id'] for x in frozen['cells']],'first_consumer_effect':'Actual first saved sourcefree I03 output potentially changes with the selected source condition','joint_cost_or_dependency_explanation':'Whole-source writer proof cold query and reuse index costs must be tested as combined dependency','source_integrity_veto_receipt':'Synthetic sourcefree fixture proof only, independent original rights and science remain held'}]
        err=check_spine(s,evidence_root=root)
        assert not err,err
        out=['valid_R6_readback_structural_PASS']
        t=copy.deepcopy(s);t['physical_decision_evidence']=[]
        e=check_spine(t,evidence_root=root);assert 'R6_PHYSICAL_DECISION_TO_EVIDENCE_CLOSURE_INCOMPLETE' in e,e
        out.append('missing_physical_decision_mapping_REJECTED')
        t=copy.deepcopy(s);t['physical_decision_evidence'][0]['selected_candidate']='B'
        e=check_spine(t,evidence_root=root);assert any('BORROWS_OTHER_WINNER' in x for x in e),e
        out.append('borrowed_winner_REJECTED')
        t=copy.deepcopy(s);t['physical_decision_evidence'][0]['material_cell_ids']=['NOT_AN_ACTUAL_CELL']
        e=check_spine(t,evidence_root=root);assert any('WITHOUT_RELEVANT_CELLS' in x for x in e),e
        out.append('invented_selected_cell_REJECTED')
        t=copy.deepcopy(s);t['comparison_receipt']['declared_winner']='B'
        e=check_spine(t,evidence_root=root);assert any('PHYSICAL_CHOICE_CONTRADICTS_MATCHED_RECEIPT' in x for x in e),e
        out.append('wrong_physical_winner_REJECTED')
        t=copy.deepcopy(s);t['decisions'].append(copy.deepcopy(t['decisions'][1]));t['decisions'][-1]['id']='OTHER-PHYSICAL'
        e=check_spine(t,evidence_root=root);assert 'R6_PHYSICAL_DECISION_TO_EVIDENCE_CLOSURE_INCOMPLETE' in e,e
        out.append('unearned_second_physical_decision_REJECTED')
        t=copy.deepcopy(s);t['comparison_receipt']['declared_verdict']='B_DOMINATES_FULL_MATERIAL_DIMENSIONS'
        e=check_spine(t,evidence_root=root);assert any('PHYSICAL_CHOICE_CONTRADICTS_MATCHED_RECEIPT' in x for x in e),e
        out.append('unmatched_numeric_verdict_REJECTED')
        print(json.dumps({'status':'PASS_R6_SCOPED_SOURCEFREE_READBACK_SYNTHETIC_NOT_GIT_OR_SCIENCE','cases':out,'count':len(out)},indent=2))

if __name__=='__main__':run()
