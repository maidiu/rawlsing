#!/usr/bin/env python3
"""ANVIL R7 deterministic first-reader builder.

Restores the six useful R5 projections for the ACTIVE integrated workflow, bound
to the source-qualified 118 inventory instead of an R5 SPINE.  Output is a pure
function of the decision document: identical input bytes => identical output
bytes.  A PASS here is a construction artifact, not science or receiving.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, pathlib, sys

PROJECTIONS=('DESIGN_DECISION.md','COVERAGE_TO_DECISION.tsv','DOWNSTREAM_BUILD_HANDOFF.jsonl',
             'EVIDENCE_AND_FALSIFIER_INDEX.jsonl','GLOBAL_ARCHITECTURE.json','BOUNDARY_TRACE.json')

def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def _j(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()


def render_decision(decision,frame,history):
    L=['# ANVIL — integrated decision (author-proposed, pending independent C)','',
       f"**Grade:** {decision.get('grade')}  ",f"**Basis:** {decision.get('basis')}  ",
       f"**Scope:** {frame.get('scope')}  ",
       f"**Source cut:** {frame.get('source_cut')}  ",
       f"**Inventory:** {decision.get('inventory_sha256')}  ",'',
       '## Selected strategy','',decision.get('single_selected_strategy') or '(none: exact hold)','',
       '## Architecture','',decision.get('architecture_description',''),'',
       '## Source-to-actor dataflow','',decision.get('entire_source_to_actor_dataflow',''),'',
       '## Algorithm and data structures','',decision.get('algorithm_and_data_structurees',decision.get('algorithm_and_data_structures','')),'',
       '## Resource-cost reasoning','',decision.get('resource_cost_reasoning',''),'',
       '## Historical function conservation','',decision.get('historical_function_conservation',''),'',
       '## Scientific boundary and nonpreclusion','',decision.get('scientific_boundary_and_nonpreclusion',''),'',
       '## Strongest surviving objection','',decision.get('strongest_surviving_objection',''),'',
       '## Why selected over feasible alternatives','',decision.get('why_selected_over_feasible_alternatives',''),'',
       '## Next actual engineering operation','',decision.get('next_actual_engineering_operation',''),'',
       '## 118 identity disposition summary','']
    rows=decision.get('identity_dispositions') or []
    counts={}
    for r in rows:counts[r.get('disposition')]=counts.get(r.get('disposition'),0)+1
    for k in sorted(counts):L.append(f'- {k}: {counts[k]}')
    L+=['',f'Total identities reconciled: {len(rows)}','',
        '## Proof boundary','',
        'This document is generated deterministically from an author proposal. It is not independent review, '
        'not protected receiving, not source/science/actor rights and not a native execution receipt.']
    return ('\n'.join(L)+'\n').encode()


def render_coverage(decision,history):
    order={'K1_CAP':0,'PYAT_PC':1,'P4R':2,'SEAM_B':3,'SEAM_S':4,'ANVIL_L':5,'BOUNDARY':6,'TERMINAL':7}
    src={r['id']:r for r in history.get('rows',[]) if isinstance(r,dict)}
    rows=decision.get('identity_dispositions') or []
    buf=io.StringIO();w=csv.writer(buf,delimiter='\t',lineterminator='\n')
    w.writerow(['group','id','disposition','candidate_specific_effect','first_consumer_consequence',
                'conservation_or_refusal_witness','origin_row_sha256','evidence_grade','owner'])
    for r in sorted(rows,key=lambda r:(order.get(src.get(r.get('identity_id'),{}).get('group'),9),r.get('identity_id') or '')):
        s=src.get(r.get('identity_id'),{})
        w.writerow([s.get('group',''),r.get('identity_id'),r.get('disposition'),r.get('candidate_specific_effect'),
                    r.get('first_consumer_consequence'),r.get('conservation_or_refusal_witness'),
                    r.get('origin_row_sha256'),r.get('evidence_grade'),r.get('owner') or ''])
    return buf.getvalue().encode()


def _handoffs(decision,frame):
    out=[]
    for h in decision.get('handoffs') or []:
        if isinstance(h,dict):out.append(h)
    if out:return out
    for b in decision.get('boundary_court') or []:
        if not isinstance(b,dict):continue
        out.append({'id':'HO-'+str(b.get('boundary')),
                    'boundary':b.get('boundary'),
                    'producer':b.get('positive',{}).get('case') if isinstance(b.get('positive'),dict) else None,
                    'receiver':frame.get('first_real_consumer'),
                    'required_now_or_future':('BUILD_OR_HOLD' if b.get('status')=='EXACT_OWNER_HOLD' else 'MUST_ALLOW_FUTURE'),
                    'status':b.get('status'),
                    'owner':b.get('owner'),
                    'negative':b.get('negative'),
                    'restore':b.get('restore'),
                    'graph_edge_ids':b.get('graph_edge_ids')})
    return out


def _evidence(decision):
    out=[]
    for i,e in enumerate(decision.get('evidence_index') or []):
        if isinstance(e,dict):out.append(e)
    for b in decision.get('boundary_court') or []:
        if not isinstance(b,dict):continue
        for kind in ('positive','negative','restore'):
            t=b.get(kind)
            if isinstance(t,dict):
                out.append({'id':f"{b.get('boundary')}:{kind}",'boundary':b.get('boundary'),'kind':kind,
                            'case':t.get('case'),'expected':t.get('expected'),'evidence_grade':t.get('evidence_grade')})
    return out


def build(decision,frame,history):
    out={}
    out['DESIGN_DECISION.md']=render_decision(decision,frame,history)
    out['COVERAGE_TO_DECISION.tsv']=render_coverage(decision,history)
    out['DOWNSTREAM_BUILD_HANDOFF.jsonl']=b''.join(_j(x)+b'\n' for x in _handoffs(decision,frame))
    out['EVIDENCE_AND_FALSIFIER_INDEX.jsonl']=b''.join(_j(x)+b'\n' for x in _evidence(decision))
    out['GLOBAL_ARCHITECTURE.json']=(json.dumps(decision.get('typed_graph') or {},sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    out['BOUNDARY_TRACE.json']=(json.dumps({'boundary_contract_sha256':decision.get('boundary_contract_sha256'),
        'boundary_court':decision.get('boundary_court') or []},sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    return out


def write(decision,frame,history,outdir):
    d=pathlib.Path(outdir);d.mkdir(parents=True,exist_ok=True)
    files=build(decision,frame,history)
    man={}
    for name,data in files.items():
        (d/name).write_bytes(data);man[name]=sha(data)
    manifest={'schema':'ANVIL_R7_BUILDER_PROJECTIONS','files':man,'digest':canon(man),
              'scope':'DETERMINISTIC_CONSTRUCTION_ONLY__NO_SCIENCE__NO_RECEIVING'}
    (d/'PROJECTION_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    return manifest


def main():
    ap=argparse.ArgumentParser();ap.add_argument('decision');ap.add_argument('frame');ap.add_argument('inventory')
    ap.add_argument('--out',required=True);a=ap.parse_args()
    dec=json.loads(pathlib.Path(a.decision).read_text());fr=json.loads(pathlib.Path(a.frame).read_text())
    inv=json.loads(pathlib.Path(a.inventory).read_text())
    print(json.dumps(write(dec,fr,inv,a.out),indent=2));return 0

if __name__=='__main__':sys.exit(main())
