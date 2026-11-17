#!/usr/bin/env python3
"""Deterministic builder for the active ANVIL R7 decision package.

Six first-reader projections, re-derived only from a locally verified FRAME +
DECISION.  They are decision documents, not native science, independent C or H1.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, tempfile, sys
from r7_integrated import check_decision, load, digest
from r7_inventory import check_inventory

NAMES=('DESIGN_DECISION.md','IDENTITY_DISPOSITIONS.tsv','BOUNDARY_CONTRACT_MAP.json',
       'TYPED_GRAPH.json','EVIDENCE_INDEX.jsonl','BUILDER_HANDOFF.json')

def sha(b):return hashlib.sha256(b).hexdigest()
def enc(s):return s.encode('utf-8')
def js(o):return (json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
def jl(rows):return enc(''.join(json.dumps(x,sort_keys=True,ensure_ascii=False)+'\n' for x in rows))

def build(decision,evidence_root,source_root,repo=None):
    err=[]
    frame=load(evidence_root,decision.get('common_frame'),err,'BUILD:FRAME')
    if frame is None:return None,err
    inv=load(evidence_root,frame.get('source_inventory'),err,'BUILD:INVENTORY')
    if inv is None:return None,err
    return _artifacts(decision,frame,inv),err

def _artifacts(decision,frame,inv):
    disps=sorted(decision.get('identity_dispositions',[]),key=lambda x:(x.get('identity_id','')))
    lines=['# ANVIL integrated decision — deterministic first-reader projection','',
           f"**Frame:** {digest(frame)}",f"**Decision grade:** {decision.get('grade')}",
           f"**First real consumer:** {decision.get('first_real_consumer')}","",
           '## Candidate',decision.get('architecture_description',''),'',
           '## Selected strategy',decision.get('single_selected_strategy',''),'',
           '## Resource / cost reasoning',decision.get('resource_cost_reasoning',''),'',
           '## Historical conservation',decision.get('historical_function_conservation',''),'',
           '## Scientific / owner boundary',decision.get('scientific_boundary_and_nonpreclusion',''),'',
           '## Strongest surviving objection',decision.get('strongest_surviving_objection',''),'',
           '## Next actual engineering operation',decision.get('next_actual_engineering_operation',''),'',
           '## Authority ceiling','This is an author proposal pending distinct C and competent H1. No source/science/actor grant, no protected receiving, no architecture adoption.','']
    design=enc('\n'.join(lines))
    head=['identity_id','group','disposition','status_assertion','evidence_grade','design_effect','first_consumer_path','conservation_or_refusal_witness','origin_sha256']
    rows=[head]+[[x.get('identity_id',''),next((e.get('group','') for e in inv.get('entries',[]) if e.get('id')==x.get('identity_id')),''),
                  x.get('disposition',''),x.get('status_assertion',''),x.get('evidence_grade',''),x.get('design_effect',''),
                  x.get('first_consumer_path',''),x.get('conservation_or_refusal_witness',''),x.get('origin_sha256','')] for x in disps]
    # TSV without csv escaping surprises: fields are controlled; strip tabs/newlines.
    tsv=enc('\n'.join('\t'.join(str(c).replace('\t',' ').replace('\n',' ') for c in r) for r in rows)+'\n')
    contracts=js({'schema':'ANVIL_R7_BOUNDARY_CONTRACT_MAP','boundaries':decision.get('boundary_contract_map',{}),
                  'note':'T1-T7 are interrogations, not seven pipeline stages; no science is accredited here.'})
    graph=js({'schema':'ANVIL_R7_TYPED_GRAPH','graph':decision.get('whole_machine_graph',{}),
              'note':'Producer/authority/time/consumer typed contract; local structure only.'})
    ev=[]
    for e in inv.get('entries',[]):
        ev.append({'id':'INV:'+e.get('id',''),'kind':'SOURCE_IDENTITY','group':e.get('group'),'origin_sha256':e.get('origin_sha256'),'source_anchor':e.get('source_anchor')})
    for x in disps:
        ev.append({'id':'DISP:'+x.get('identity_id',''),'kind':'IDENTITY_DISPOSITION','disposition':x.get('disposition'),'origin_sha256':x.get('origin_sha256')})
    ev.extend(decision.get('evidence_index',[]) if isinstance(decision.get('evidence_index'),list) else [])
    evidence=jl(sorted(ev,key=lambda x:(str(x.get('id')),str(x.get('kind')))))
    handoff=js({'schema':'ANVIL_R7_BUILDER_HANDOFF','first_real_consumer':decision.get('first_real_consumer'),
                'handoff':decision.get('builder_handoff',{}),'authority_ceiling':'SPECIFICATION_ONLY_NOT_EXECUTED_OR_PROTECTED'})
    return {'DESIGN_DECISION.md':design,'IDENTITY_DISPOSITIONS.tsv':tsv,'BOUNDARY_CONTRACT_MAP.json':contracts,
            'TYPED_GRAPH.json':graph,'EVIDENCE_INDEX.jsonl':evidence,'BUILDER_HANDOFF.json':handoff}

def write(arts,out):
    out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
    manifest={}
    for n,b in arts.items():
        (out/n).write_bytes(b);manifest[n]=sha(b)
    (out/'MANIFEST.json').write_bytes(js({'schema':'ANVIL_R7_BUILT_MANIFEST','files':manifest,
        'note':'Six deterministic projections; regenerate and byte-compare, do not hand-edit.'}))
    return manifest

def verify(arts,out):
    out=pathlib.Path(out);e=[]
    for n,b in arts.items():
        p=out/n
        if not p.is_file():e.append('MISSING:'+n)
        elif p.read_bytes()!=b:e.append('BYTES_CHANGED:'+n)
    m=out/'MANIFEST.json'
    if not m.is_file():e.append('MISSING:MANIFEST.json')
    else:
        try:
            want={n:sha(b) for n,b in arts.items()}
            if json.loads(m.read_text()).get('files')!=want:e.append('MANIFEST_HASH_MISMATCH')
        except ValueError:e.append('MANIFEST_MALFORMED')
    return sorted(set(e))

def main():
    ap=argparse.ArgumentParser(description='Build/verify the six deterministic ANVIL R7 projections')
    ap.add_argument('action',choices=['build','verify']);ap.add_argument('decision')
    ap.add_argument('--evidence-root',required=True);ap.add_argument('--source-root',required=True)
    ap.add_argument('--repo');ap.add_argument('--out',required=True);a=ap.parse_args()
    d=json.loads(pathlib.Path(a.decision).read_text())
    res=check_decision(d,a.evidence_root,a.source_root,a.repo)
    if res['status']=='RED':print(json.dumps({'status':'RED','gate':res},indent=2));return 2
    arts,err=build(d,a.evidence_root,a.source_root,a.repo)
    if arts is None:print(json.dumps({'status':'RED','errors':err},indent=2));return 2
    if a.action=='build':
        man=write(arts,a.out);print(json.dumps({'status':'BUILT','files':man,'scope':'LOCAL_STRUCTURE_ONLY_NOT_NATIVE_OR_PROTECTED'},indent=2));return 0
    e=verify(arts,a.out);print(json.dumps({'status':'RED' if e else 'PASS_SIX_PROJECTIONS_BYTE_IDENTICAL','errors':e},indent=2));return 2 if e else 0

if __name__=='__main__':sys.exit(main())
