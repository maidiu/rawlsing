#!/usr/bin/env python3
import argparse, pandas as pd, json, zipfile, hashlib, tempfile, pathlib, sys, os

ENUM={'WORKER_RECOMMEND_ACCEPT','WORKER_RECOMMEND_PARTIAL_ACCEPT','WORKER_RECOMMEND_REJECT','WORKER_RETAIN_EXISTING_GOVERNED_AUTHORITY','WORKER_BLOCKED_NEEDS_VOZHD'}
CONF={'HIGH','MEDIUM','LOW'}
MUTABLE=['worker_recommendation','proposed_relation_objects_json','authorized_member_implementation_ids_json','rejected_member_implementation_ids_json','relation_role_structure','decisive_rationale','evidence_refs_json','routing_or_composability_note','blocker_reason','confidence','worker_notes']
IDENT=['worker_id','decision_atom_id','r13_packet_id','r12_child_packet_id','packet_class','source_family','wave','raw_origin_id','rule_scope','decision_atom_kind','r13_member_implementation_ids_json','r13_member_semantic_unit_ids_json','known_r6_relation_ids_fully_contained_json']
TYPE={'T03':'GENERAL_PRINCIPLE_SPECIFIC_APPLICATION','T04':'GOAL_MEANS','T05':'COMMITMENT_PERSONAL_COST','T06':'NORM_EXPECTED_CONDUCT','T08':'INSTITUTION_CLASS_DIFFERENTIATION','T09':'RECIPROCAL_ROLE_REVERSAL','T10':'TARGET_CONDITION_MATRIX','T11':'COMPLEMENTARY_ROLE_CONVERGENCE'}
RESERVED={'W03':'R15ATOM-4a035c650a59ffe2f186'}
PACK_SHA={'W01':'316de216ae953d253124a59c7a9d8367602078f4906c7f916e90fedef4dc14db','W02':'c41c4054043ff15cbde7fd05023e1e9194f34ce91929059fa2c1213ee68957d3','W03':'3d0b3abd702376661cdfa25380af556825e8059dee9528b307433386938f8b8f','W04':'94cfef84e67e29ad36d89e6b24a59adf57a3b9f3401043ee703f7c622aabb574','W05':'ffbba6ffc801060976420feb4e971ac190b59da896aefc92c003d007ae188032','W06':'7a34521209e790dec9763d167cf288395fb9ad8aa6ff7126ebf8cbc5b1465e6f'}
ASSIGNED={'W01':19060,'W02':15156,'W03':13339,'W04':13331,'W05':12732,'W06':12274}
T07N={'W01':42,'W02':105,'W03':123,'W04':136,'W05':112,'W06':152}

def file_sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def js(x,typ):
    try: v=json.loads(x)
    except Exception as e: return None
    return v if isinstance(v,typ) else None

def locate_pack(root,w):
    p=root/w/'RETURN/WORKER_RETURN_TEMPLATE.csv'
    if p.exists(): return root/w
    p=root/'RETURN/WORKER_RETURN_TEMPLATE.csv'
    if p.exists(): return root
    raise FileNotFoundError('Could not locate worker pack root')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--worker',required=True,choices=[f'W0{i}' for i in range(1,7)]); ap.add_argument('--pack',required=True); ap.add_argument('--return-csv'); ap.add_argument('--preflight',action='store_true'); ap.add_argument('--output-json'); a=ap.parse_args()
    w=a.worker; temp=None
    pp=pathlib.Path(a.pack)
    observed_pack_sha=''
    if pp.suffix=='.zip':
        observed_pack_sha=file_sha(pp)
        temp=tempfile.TemporaryDirectory(); z=zipfile.ZipFile(pp); z.extractall(temp.name); roots=list(pathlib.Path(temp.name).iterdir()); root=roots[0] if len(roots)==1 and roots[0].is_dir() else pathlib.Path(temp.name)
    else: root=pp
    pr=locate_pack(root,w)
    template=pd.read_csv(pr/'RETURN/WORKER_RETURN_TEMPLATE.csv',dtype=str,keep_default_na=False)
    wb=pd.read_csv(pr/'WORKBENCH/DECISION_ATOM_WORKBENCH.csv',dtype=str,keep_default_na=False)
    checks=[]
    def ck(name,ok,detail=''): checks.append({'check':name,'pass':bool(ok),'detail':str(detail)})
    if observed_pack_sha: ck('exact_pack_sha256',observed_pack_sha==PACK_SHA[w],observed_pack_sha)
    ck('assigned_atom_count_exact',len(wb)==ASSIGNED[w],f'{len(wb)}/{ASSIGNED[w]}')
    ck('t07_reserved_count_exact',int((wb.rule_scope=='T07').sum())==T07N[w],int((wb.rule_scope=='T07').sum()))
    ck('workbench_template_same_rows',len(template)==len(wb) and template.decision_atom_id.tolist()==wb.decision_atom_id.tolist(),f'{len(template)}/{len(wb)}')
    ck('decision_atom_ids_unique',template.decision_atom_id.is_unique,template.decision_atom_id.duplicated().sum())
    ck('identity_columns_present',all(x in template.columns for x in IDENT),len(template.columns))
    ck('mutable_fields_blank_in_template',all((template[c]=='').all() for c in MUTABLE), '')
    ck('job3_not_in_worker_task',True,'validator has no Job3 operation')
    if a.preflight:
        result={'worker':w,'mode':'preflight','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checks':checks}
    else:
        if not a.return_csv: raise SystemExit('--return-csv required unless --preflight')
        ret=pd.read_csv(a.return_csv,dtype=str,keep_default_na=False)
        ck('return_columns_exact',ret.columns.tolist()==template.columns.tolist(),len(ret.columns))
        ck('return_row_count_exact',len(ret)==len(template),f'{len(ret)}/{len(template)}')
        ck('return_atom_order_exact',ret.decision_atom_id.tolist()==template.decision_atom_id.tolist(),'')
        for c in IDENT: ck('immutable_'+c,(ret[c]==template[c]).all(),int((ret[c]!=template[c]).sum()))
        ck('no_blank_mutable_cells',all((ret[c]!='').all() for c in MUTABLE),sum(int((ret[c]=='').sum()) for c in MUTABLE))
        ck('recommendation_enum',set(ret.worker_recommendation)<=ENUM,sorted(set(ret.worker_recommendation)-ENUM))
        ck('confidence_enum',set(ret.confidence)<=CONF,sorted(set(ret.confidence)-CONF))
        json_errors=[]; semantic_errors=[]
        for idx,r in ret.iterrows():
            prop=js(r.proposed_relation_objects_json,list); auth=js(r.authorized_member_implementation_ids_json,list); rej=js(r.rejected_member_implementation_ids_json,list); struct=js(r.relation_role_structure,dict); ev=js(r.evidence_refs_json,list); frozen=js(r.r13_member_implementation_ids_json,list); known=js(r.known_r6_relation_ids_fully_contained_json,list)
            if None in (prop,auth,rej,struct,ev,frozen,known): json_errors.append(r.decision_atom_id); continue
            rec=r.worker_recommendation
            if r.rule_scope=='T07':
                if not (rec=='WORKER_BLOCKED_NEEDS_VOZHD' and r.blocker_reason=='T07_RESERVED_CENTRAL'): semantic_errors.append((r.decision_atom_id,'T07_NOT_RESERVED'))
            if w=='W03' and r.decision_atom_id==RESERVED['W03']:
                if not (rec=='WORKER_BLOCKED_NEEDS_VOZHD' and r.blocker_reason=='CENTRAL_C4_DUPLICATE_RESERVED'): semantic_errors.append((r.decision_atom_id,'CENTRAL_DUPLICATE_NOT_RESERVED'))
            if rec in {'WORKER_RECOMMEND_ACCEPT','WORKER_RECOMMEND_PARTIAL_ACCEPT'}:
                if not prop: semantic_errors.append((r.decision_atom_id,'ACCEPT_WITHOUT_PROPOSED_OBJECT'))
                if not auth: semantic_errors.append((r.decision_atom_id,'ACCEPT_WITHOUT_AUTHORIZED_MEMBERS'))
                if not set(auth)<=set(frozen) or not set(rej)<=set(frozen) or set(auth)&set(rej): semantic_errors.append((r.decision_atom_id,'MEMBER_PARTITION_INVALID'))
                allowed=set()
                for rs in r.rule_scope.split(';'):
                    if rs in TYPE: allowed.add(TYPE[rs])
                for o in prop:
                    if not isinstance(o,dict) or not {'relation_type','member_implementation_ids','member_roles','common_identity','evidence_basis'}<=set(o): semantic_errors.append((r.decision_atom_id,'PROPOSED_OBJECT_SCHEMA')) ; continue
                    if o.get('relation_type') not in allowed: semantic_errors.append((r.decision_atom_id,'RELATION_TYPE_WRONG_FOR_RULE'))
                    if not set(o.get('member_implementation_ids',[]))<=set(frozen): semantic_errors.append((r.decision_atom_id,'PROPOSED_MEMBERS_OUTSIDE_FROZEN'))
            elif rec=='WORKER_RETAIN_EXISTING_GOVERNED_AUTHORITY':
                if not known: semantic_errors.append((r.decision_atom_id,'RETAIN_WITHOUT_KNOWN_R6'))
            elif rec=='WORKER_BLOCKED_NEEDS_VOZHD':
                if r.blocker_reason in {'','NONE'}: semantic_errors.append((r.decision_atom_id,'BLOCKED_WITHOUT_REASON'))
                if prop: semantic_errors.append((r.decision_atom_id,'BLOCKED_WITH_PROPOSED_OBJECT'))
            elif rec=='WORKER_RECOMMEND_REJECT':
                if prop: semantic_errors.append((r.decision_atom_id,'REJECT_WITH_PROPOSED_OBJECT'))
            if r.rule_scope=='T06':
                if not isinstance(struct,dict) or struct.get('rule')!='T06' or not {'rr_norm','endpoint_or_conduct','link'}<=set(struct): semantic_errors.append((r.decision_atom_id,'T06_STRUCTURE_SCHEMA'))
            if r.evidence_refs_json=='[]': semantic_errors.append((r.decision_atom_id,'NO_EVIDENCE_REF'))
            if r.decisive_rationale in {'','NONE'}: semantic_errors.append((r.decision_atom_id,'NO_DECISIVE_RATIONALE'))
        ck('all_json_fields_parse',len(json_errors)==0,json_errors[:20])
        ck('semantic_return_contract',len(semantic_errors)==0,semantic_errors[:40])
        result={'worker':w,'mode':'return','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checks':checks,'recommendation_counts':ret.worker_recommendation.value_counts().to_dict()}
    if a.output_json: pathlib.Path(a.output_json).write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2)); sys.exit(0 if result['status']=='PASS' else 2)
if __name__=='__main__': main()
