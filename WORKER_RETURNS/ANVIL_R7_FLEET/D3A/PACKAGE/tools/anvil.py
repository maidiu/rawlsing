#!/usr/bin/env python3
"""ANVIL source-graded campaign integrity verifier.
Not a substitute for independent scientific, source, performance, or architecture review.
Author cannot certify its own evidence via this script. Final acceptance requires distinct C.
"""
import argparse, copy, csv, hashlib, io, json, pathlib, re, sys, tempfile, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
MAN=json.loads((ROOT/'03_FROZEN_SOURCE_CUTS.json').read_text())
BC=json.loads((ROOT/'02_BOUNDARY_CONTRACTS.json').read_text())
BOUND={x['id']:x for x in BC['boundaries']}
REQUIRED=MAN['mandatory']
DIMS={'build','cold_open','distinct_1_10_100','retained_scratch','cross_world_reuse','process_tree_rss'}
NECESSITY={'BUILD_NOW','MUST_PRESERVE_NOW','MUST_ALLOW_FUTURE','OWNER_SCIENCE_HELD','HISTORICAL_NOT_ADOPTED','HISTORICAL_PROOF_HELD'}
STATUS={'REUSE_PROVEN','ADAPT_EXISTING','REQUIRES_TEST','PRESERVE_WITHOUT_BUILD','NO_ARCH_CHANGE_PROVEN','UNKNOWN_HELD'}
OUTCOMES={'DESIGN_READY_SCOPED','CONDITIONAL_CANDIDATE','DECISION_BLOCKED_EXACT','INCUMBENT_REJECTED_SCOPED'}
GRADES={'DOCUMENTARY','CODE_STATIC','EXECUTED_SOURCEFREE','EXECUTED_NATIVE'}
ALTS={'SELECTED','ELIMINATED','VIABLE_CONTESTED'}
KINDS={'EXTERNAL_OBSERVED','OBSERVED','DESCRIPTIVE_MODELED','STRUCTURAL_QUALIFIED','FICTIONAL_WORLD','ACTOR_STATE','HISTORY_EVENT','RIGHTS_METADATA'}
FIRST3={'T1','T2','T3'}
STATES={'MEASURED','MODELED','NOT_RUN'}
KEYS={'PRESERVE','PHYSICAL','FUTURE_NONPRECLUSION'}
PIN=re.compile(r'[0-9a-f]{40}')
HEX=re.compile(r'[0-9a-f]{64}')


def nonempty(x,n=10):return isinstance(x,str) and len(x.strip())>=n and x.strip().upper() not in {'UNKNOWN','TBD','TODO','N/A','NONE','SEE ABOVE'}
def err(e,what):e.append(what)
def required(o,names,where,e):
    if not isinstance(o,dict):err(e,where+':NOT_OBJECT');return
    for n in names:
        if n not in o or o[n] is None or o[n]=='' or (o[n]==[] and n not in {'input_types','output_types','dependencies'}):err(e,where+':MISSING:'+n)

def _validate(s,evidence_root=None,strict_repo=None):
    e=[]
    if s.get('schema') not in {'ANVIL_SPINE_R5','ANVIL_SPINE_R6'}:e.append('INVALID_SCHEMA')
    if s.get('baseline_sha')!=MAN['snapshot_sha']:e.append('BAD_BASELINE_PIN')
    if s.get('outcome') not in OUTCOMES:e.append('BAD_OUTCOME')
    if not nonempty(s.get('verdict_reason'),30):e.append('VAGUE_VERDICT')
    if s.get('decision_constitution_sha256')!=hashlib.sha256((ROOT/'01_DECISION_CONSTITUTION.md').read_bytes()).hexdigest():e.append('DECISION_RULE_MUTATED')
    if s.get('boundary_contract_sha256')!=hashlib.sha256((ROOT/'02_BOUNDARY_CONTRACTS.json').read_bytes()).hexdigest():e.append('BOUNDARY_RULE_MUTATED')
    isready=s.get('outcome')=='DESIGN_READY_SCOPED'
    ev=s.get('evidence',[])
    evid={}
    if not isinstance(ev,list):e.append('EVIDENCE_NOT_LIST');ev=[]
    for a in ev:
        if not isinstance(a,dict):e.append('BAD_EVIDENCE');continue
        required(a,['id','grade','locator','claim','verification_status'],f'EVIDENCE:{a.get("id")}',e)
        eid=a.get('id');
        if eid in evid:e.append('DUPLICATE_EVIDENCE:'+str(eid))
        evid[eid]=a
        if a.get('grade') not in GRADES:e.append('BAD_EVIDENCE_GRADE:'+str(eid))
        if a.get('verification_status') not in {'SOURCE_PINNED','EXECUTED_FILE_VERIFIED','UNVERIFIED_HELD'}:e.append('BAD_EVIDENCE_VERIFICATION:'+str(eid))
        if a.get('grade','').startswith('EXECUTED') or a.get('verification_status')=='EXECUTED_FILE_VERIFIED':
            required(a,['command','runner','receipt_path','receipt_sha256','positive_case','negative_case','restore_case'],str(eid),e)
            if not HEX.fullmatch(str(a.get('receipt_sha256',''))):e.append('INVALID_EVIDENCE_HASH:'+str(eid))
            if evidence_root is None:
                if isready:e.append('READY_NEEDS_ACTUAL_EVIDENCE_DIRECTORY:'+str(eid))
            else:
                path=(pathlib.Path(evidence_root)/str(a.get('receipt_path',''))).resolve();root=pathlib.Path(evidence_root).resolve()
                if not path.is_relative_to(root) or not path.is_file():e.append('MISSING_EXECUTED_RECEIPT:'+str(eid))
                elif hashlib.sha256(path.read_bytes()).hexdigest()!=a.get('receipt_sha256'):e.append('BAD_EXECUTED_RECEIPT_HASH:'+str(eid))
        if isready and a.get('verification_status')=='UNVERIFIED_HELD':e.append('READY_WITH_UNVERIFIED_EVIDENCE:'+str(eid))
    def evidence_ids(ids,ctx):
        if not isinstance(ids,list) or not ids:e.append('NO_EVIDENCE_FOR:'+ctx);return
        for eid in ids:
            if eid not in evid:e.append('ORPHAN_EVIDENCE:'+ctx+':'+str(eid))
    def executed(ids):return any(x in evid and evid[x].get('grade','').startswith('EXECUTED') and evid[x].get('verification_status')=='EXECUTED_FILE_VERIFIED' for x in ids)
    # Historical and prospective identities: all present in the canonical spine and ALL exported.
    cov=s.get('coverage',{});cov=cov if isinstance(cov,dict) else {}
    for group,keys in REQUIRED.items():
        m=cov.get(group,{})
        if not isinstance(m,dict):e.append('INVALID_COVERAGE_MAP:'+group);continue
        for missing in sorted(set(keys)-set(m)):e.append('MISSING_COVERAGE:'+group+':'+missing)
        for extra in sorted(set(m)-set(keys)):e.append('EXTRA_COVERAGE:'+group+':'+extra)
        for ident,rec in m.items():
            ctx=f'COVERAGE:{group}:{ident}'
            required(rec,['necessity','status','source_anchor','source_semantics','consumer_or_hold','negative_meaning','architecture_effect','evidence_ids','why','decision_ids'],ctx,e)
            if not isinstance(rec,dict):continue
            if rec.get('necessity') not in NECESSITY:e.append('BAD_NECESSITY:'+ctx)
            if rec.get('status') not in STATUS:e.append('BAD_DISPOSITION:'+ctx)
            evidence_ids(rec.get('evidence_ids'),ctx)
            if group=='PYAT_PC' and (rec.get('adopted') is not False or rec.get('necessity')!='HISTORICAL_NOT_ADOPTED'):e.append('UNAUTHORIZED_PROPOSAL_ADOPTION:'+ident)
            if group=='P4R' and (rec.get('closed') is not False or rec.get('necessity')!='HISTORICAL_PROOF_HELD'):e.append('FALSE_P4R_CLOSURE:'+ident)
            if group in {'K1_CAP','PYAT_PC','P4R'}:
                if rec.get('original_source_blob')!=MAN['k3_files'][group]['blob']:e.append('K3_SOURCE_BLOB_MISMATCH:'+ident)
                if not HEX.fullmatch(str(rec.get('row_sha256',''))):e.append('NO_SOURCE_ROW_HASH:'+ident)
            if rec.get('status')=='NO_ARCH_CHANGE_PROVEN' and (not rec.get('decision_ids') or not nonempty(rec.get('why'),65) or not nonempty(rec.get('consumer_or_hold'),20)):
                e.append('NO_ARCH_CHANGE_UNPROVEN:'+ctx)
            if isready and rec.get('status')=='UNKNOWN_HELD' and rec.get('necessity') in {'BUILD_NOW','MUST_PRESERVE_NOW'}:e.append('READY_WITH_UNKNOWN_REQUIRED:'+ctx)
    # SOURCE ROWS: do not let 118 invented/boilerplate hashes claim exact K3 conservation.
    if isready and strict_repo is None:e.append('READY_REQUIRES_EXACT_GIT_SOURCE_RECHECK')
    if strict_repo is not None:
        root=pathlib.Path(strict_repo)
        for group in ('K1_CAP','PYAT_PC','P4R'):
            item=MAN['k3_files'][group];src=MAN['k3_source_root']+'/'+item['file']
            rev=subprocess.run(['git','-C',str(root),'rev-parse',MAN['snapshot_sha']+':'+src],capture_output=True,text=True)
            if rev.returncode or rev.stdout.strip()!=item['blob']:
                e.append('K3_PINNED_FILE_MISMATCH:'+group);continue
            cp=subprocess.run(['git','-C',str(root),'show',MAN['snapshot_sha']+':'+src],capture_output=True,text=True)
            if cp.returncode:e.append('K3_FILE_UNREADABLE:'+group);continue
            rows=cp.stdout.splitlines();actual={}
            for row in rows[1:]:
                if row.strip():
                    actual[row.split('\t',1)[0]]=hashlib.sha256(row.encode()).hexdigest()
            if set(actual)!=set(REQUIRED[group]):e.append('K3_SOURCE_ID_CENSUS_CHANGED:'+group)
            for rid in REQUIRED[group]:
                v=cov.get(group,{}).get(rid,{})
                if v.get('row_sha256')!=actual.get(rid):e.append('K3_ROW_SEMANTIC_HASH_MISMATCH:'+rid)
    # Frozen boundary definitions: exact meaning, not seven arbitrary labels.
    bds=s.get('boundaries',{});bds=bds if isinstance(bds,dict) else {}
    if set(bds)!=set(BOUND):e.append('INCOMPLETE_BOUNDARY_UNIVERSE')
    for ident,base in BOUND.items():
        x=bds.get(ident,{})
        required(x,['contract_name','first_consumer','positive','negative','restore','graph_edge_ids','status','owner','evidence_ids'],ident,e)
        if not isinstance(x,dict):continue
        if x.get('contract_name')!=base['name']:e.append('REDEFINED_BOUNDARY:'+ident)
        evidence_ids(x.get('evidence_ids'),ident)
        if isready and ident in FIRST3 and x.get('status') not in {'ACTUAL_PROVED_AT_SCOPE','SOURCE_STATIC_CONSERVED'}:e.append('READY_WITH_INOPERABLE_P0_BOUNDARY:'+ident)
    # One decision per material choice, not one arbitrary universal candidate. B rival must be real.
    ds=s.get('decisions',[]);ds=ds if isinstance(ds,list) else [];decision_ids=set();dmap={}
    kinds=set()
    for d in ds:
        if not isinstance(d,dict):e.append('DECISION_NOT_OBJECT');continue
        did=d.get('id');ctx='DECISION:'+str(did)
        required(d,['id','class','question','first_consumer','criterion','alternatives','selected','discriminators','invariants','evidence_ids','global_node_ids','comparison_summary'],ctx,e)
        if did in decision_ids:e.append('DUPLICATE_DECISION:'+str(did))
        decision_ids.add(did);dmap[did]=d;kinds.add(d.get('class'))
        evidence_ids(d.get('evidence_ids'),ctx)
        alts=d.get('alternatives',[]);alts=alts if isinstance(alts,list) else []
        if len(alts)<(2 if d.get('class')=='PHYSICAL' else 1):e.append('DECISION_NO_GENUINE_COMPETITOR:'+ctx)
        if d.get('class')!='PHYSICAL' and len(alts)==1 and not nonempty(d.get('no_material_rival_reason'),50):e.append('UNJUSTIFIED_SINGLE_OPTION_NONPHYSICAL:'+ctx)
        aids=[];b_rivals=0;selected=[]
        for a in alts:
            if not isinstance(a,dict):e.append('BAD_ALTERNATIVE:'+ctx);continue
            required(a,['id','origin','status','physical_arrangement','source_preservation','preparation_reuse','first_consumer','future_interfaces','cost_risks','evidence_ids','elimination_or_selection_reason'],ctx+'.ALT',e)
            aids.append(a.get('id'))
            if a.get('origin')=='B_INDEPENDENT':b_rivals+=1
            if a.get('status') not in ALTS:e.append('BAD_ALT_STATUS:'+ctx)
            if a.get('status')=='SELECTED':selected.append(a.get('id'))
            evidence_ids(a.get('evidence_ids'),ctx+'.ALT')
            if a.get('status')=='ELIMINATED' and not nonempty(a.get('elimination_or_selection_reason'),45):e.append('UNPROVEN_ELIMINATION:'+ctx)
        if len(aids)!=len(set(aids)):e.append('DUPLICATE_ALTERNATIVE:'+ctx)
        if d.get('class')=='PHYSICAL' and not b_rivals:e.append('NO_INDEPENDENT_B_ALTERNATIVE:'+ctx)
        if isready and (len(selected)!=1 or d.get('selected')!=selected[0] or any(a.get('status')=='VIABLE_CONTESTED' for a in alts if isinstance(a,dict))):e.append('NO_COMPARATIVE_WINNER:'+ctx)
        discr=d.get('discriminators',[])
        if not isinstance(discr,list) or not discr:e.append('NO_DISCRIMINATORS:'+ctx)
        else:
            for j,z in enumerate(discr):
                zctx=ctx+f'.DISCR[{j}]'
                required(z,['id','raised_by','outcome_if_a','outcome_if_b','status','smallest_test','evidence_ids','competent_owner','physical_or_semantic'],zctx,e)
                if not isinstance(z,dict):continue
                if z.get('raised_by') not in {'A_P0','B_P0','P1_SHARED','C_CHALLENGE'}:e.append('INVALID_DISCRIMINATOR_PROVENANCE:'+zctx)
                if z.get('status') not in {'RESOLVED','PENDING'}:e.append('INVALID_DISCRIMINATOR_STATUS:'+zctx)
                evidence_ids(z.get('evidence_ids'),zctx)
                if isready and z.get('status')=='PENDING':e.append('SELF_DECLARED_NONBLOCKING_REJECTED:'+zctx)
        for label in ('lossless_source','scientific_claims','rights_and_fail_closed','true_joint','global_composition','rss_budget'):
            if d.get('invariants',{}).get(label) not in {'PASS_AT_SCOPE','NOT_APPLICABLE_REASONED','UNPROVED_HELD','FAIL'}:e.append('MISSING_INVARIANT:'+ctx+':'+label)
            if isready and d.get('class') in {'PRESERVE','PHYSICAL'} and d.get('invariants',{}).get(label) in {'UNPROVED_HELD','FAIL'}:e.append('READY_WITH_UNPROVED_CURRENT_VETO:'+ctx+':'+label)
            if isready and d.get('class')=='FUTURE_NONPRECLUSION' and d.get('invariants',{}).get(label)=='FAIL':e.append('READY_WITH_PROVEN_FUTURE_LOSS:'+ctx+':'+label)
    if not KEYS.issubset(kinds):e.append('MISSING_DECISION_CLASS:'+repr(KEYS-kinds))
    for group,m in cov.items():
        if not isinstance(m,dict):continue
        for key,rec in m.items():
            if isinstance(rec,dict) and (not isinstance(rec.get('decision_ids'),list) or any(x not in decision_ids for x in rec.get('decision_ids',[]))):e.append('BAD_COVERAGE_DECISION_LINK:'+group+':'+key)
    # Global composition: selected local alternatives must be used in one typed, connected pipeline.
    arch=s.get('architecture',{})
    required(arch,['nodes','edges','invariants','version_lifecycle','first_consumer_path','future_reference_path'], 'ARCHITECTURE',e)
    nodes=arch.get('nodes',[]) if isinstance(arch,dict) else [];edges=arch.get('edges',[]) if isinstance(arch,dict) else []
    nmap={x.get('id'):x for x in nodes if isinstance(x,dict)};emap={x.get('id'):x for x in edges if isinstance(x,dict)}
    if len(nmap)!=len(nodes):e.append('DUPLICATE_GRAPH_NODE')
    if len(emap)!=len(edges):e.append('DUPLICATE_GRAPH_EDGE')
    for n in nodes:
        if not isinstance(n,dict):continue
        required(n,['id','owner','domain','input_types','output_types','implementation','decision_id','alternative_id'], 'NODE',e)
        if n.get('domain') not in KINDS:e.append('INVALID_NODE_DOMAIN:'+str(n.get('id')))
        d=dmap.get(n.get('decision_id'))
        if not d or n.get('alternative_id')!=d.get('selected'):e.append('GLOBAL_LOCAL_ALTERNATIVE_MISMATCH:'+str(n.get('id')))
    for edge in edges:
        if not isinstance(edge,dict):continue
        required(edge,['id','from','to','data_type','boundary','transition_class','authority_grade','temporal_mode','negative','invalidation_rule'], 'EDGE',e)
        a=nmap.get(edge.get('from'));b=nmap.get(edge.get('to'))
        if not a or not b:e.append('GRAPH_ORPHAN:'+str(edge.get('id')));continue
        if edge.get('data_type') not in a.get('output_types',[]) or edge.get('data_type') not in b.get('input_types',[]):e.append('GLOBAL_TYPE_MISMATCH:'+str(edge.get('id')))
        if edge.get('boundary') not in BOUND:e.append('BAD_BOUNDARY_EDGE:'+str(edge.get('id')))
        if a.get('domain') in {'FICTIONAL_WORLD','ACTOR_STATE','HISTORY_EVENT'} and b.get('domain')=='OBSERVED':e.append('FICTIONAL_BACKFLOW_INTO_OBSERVED:'+str(edge.get('id')))
        if any(x in edge for x in ('grade','authority','clock')):e.append('REDUNDANT_CONTRADICTORY_EDGE_AUTHORITY:'+str(edge.get('id')))
    for ident,record in bds.items():
        if not isinstance(record,dict):continue
        for ed in record.get('graph_edge_ids',[]):
            if ed not in emap or emap[ed].get('boundary')!=ident:e.append('BOUNDARY_GRAPH_NOT_PROVEN:'+str(ident)+':'+str(ed))
    for d in ds:
        if not isinstance(d,dict):continue
        for n in d.get('global_node_ids',[]):
            if n not in nmap or nmap[n].get('decision_id')!=d.get('id'):e.append('DECISION_GLOBAL_ORPHAN:'+str(d.get('id'))+':'+str(n))
    path=arch.get('first_consumer_path',[]) if isinstance(arch,dict) else []
    if not isinstance(path,list) or len(path)<3 or any(x not in nmap for x in path):e.append('INVALID_GLOBAL_FIRST_CONSUMER_PATH')
    elif any(not any(q.get('from')==a and q.get('to')==b for q in edges if isinstance(q,dict)) for a,b in zip(path,path[1:])):e.append('UNCONNECTED_GLOBAL_FIRST_CONSUMER_PATH')
    future=arch.get('future_reference_path',[]) if isinstance(arch,dict) else []
    if not isinstance(future,list) or len(future)<2 or any(x not in nmap for x in future):
        e.append('MISSING_GLOBAL_SOURCE_TO_ACTOR_REFERENCE_PATH')
    else:
        used=[]
        for a,b in zip(future,future[1:]):
            hit=[q for q in edges if isinstance(q,dict) and q.get('from')==a and q.get('to')==b]
            if not hit:e.append('GLOBAL_PATH_DISCONNECTED:'+str(a)+'->'+str(b))
            else:used.append(hit[0].get('boundary'))
        # T1-T7 are interrogations not a compulsory physical linear pipeline. Actual paths are checked in R5 contract.
    if isready and not any(x.get('domain')=='OBSERVED' for x in nodes if isinstance(x,dict)):e.append('READY_WITHOUT_OBSERVED_SOURCE_NODE')
    # Meaning test has to span every boundary, preserving unobservability and grades.
    obs=s.get('epistemic_case',{})
    required(obs,['fixture_description','instrument_A_ancestry','instrument_B_ancestry','true_three_way_joint','material_evidence_independent','steps','test_grade','negative_observability_result','restore_result','source_vs_fictional_separation'], 'EPISTEMIC_CASE',e)
    if obs.get('instrument_A_ancestry') not in {'NOT_ASKED','NOT_RELEASED'}:e.append('WRONG_SYNTHETIC_UNOBSERVED_INSTRUMENT')
    if obs.get('instrument_B_ancestry') not in {'OBSERVED_DIFFERENT_CATEGORY','NOT_COMPARABLE','OBSERVED_COMPARABLE_SCIENCE_ISSUED'}:e.append('UNCONTROLLED_WAVE_COMPARABILITY')
    if obs.get('true_three_way_joint') is not True:e.append('MISSING_TRUE_HIGH_ORDER_JOINT')
    if obs.get('material_evidence_independent') is not True:e.append('STRUCTURAL_EVIDENCE_NOT_INDEPENDENT')
    steps=obs.get('steps',[]);smap={x.get('boundary'):x for x in steps if isinstance(x,dict)}
    if set(smap)!=set(BOUND):e.append('INCOMPLETE_EPISTEMIC_WALK')
    for k,v in smap.items():
        required(v,['boundary','input','output','ancestry_A_status','positive','negative','restore','real_consumer_or_hold','evidence_ids','grade'], 'EPISTEMIC:'+k,e)
        if v.get('ancestry_A_status') not in {'NOT_OBSERVED','MODELED_NOT_OBSERVED','FICTIONAL_NOT_SURVEYED','NOT_APPLICABLE'}:e.append('FABRICATED_ANCESTRY_OBSERVATION:'+k)
        evidence_ids(v.get('evidence_ids'),'EPISTEMIC:'+k)
    if isready and obs.get('test_grade') not in {'EXECUTED_SOURCEFREE_COMPOSED','EXECUTED_NATIVE_COMPOSED'}:e.append('READY_WITHOUT_MEANING_CONSERVATION_TEST')
    # Physical outcome: author cannot declare potentially reversing benchmark unimportant by itself.
    workload=s.get('workload',{})
    required(workload,['locked_scenario','respondents','question_opportunities','cold_distinct_operations','rss_ceiling_bytes','source_width_grade','measures','comparison_preference'], 'WORKLOAD',e)
    if workload.get('rss_ceiling_bytes')!=6442450944:e.append('RSS_BUDGET_CHANGED')
    if workload.get('cold_distinct_operations')!=[1,10,100]:e.append('QUERY_VECTOR_CHANGED')
    if workload.get('respondents')!=100000:e.append('RESPONDENT_VECTOR_CHANGED')
    if int(workload.get('question_opportunities',0))<600:e.append('WIDTH_VECTOR_TOO_SMALL')
    dims={x.get('dimension'):x for x in workload.get('measures',[]) if isinstance(x,dict)}
    if set(dims)!=DIMS:e.append('INCOMPLETE_PHYSICAL_VECTOR')
    for name,x in dims.items():
        required(x,['dimension','kind','candidate_values','evidence_ids','discriminator_effect'], 'COST:'+name,e)
        if x.get('kind') not in STATES:e.append('INVALID_COST_GRADE:'+name)
        evidence_ids(x.get('evidence_ids'),'COST:'+name)
        if isready and name in {'build','cold_open','distinct_1_10_100','retained_scratch','process_tree_rss'} and x.get('kind')!='MEASURED':e.append('READY_WITH_UNMEASURED_PHYSICAL_CHOICE:'+name)
        if x.get('kind')=='MEASURED' and not executed(x.get('evidence_ids',[])):e.append('UNVERIFIED_MEASURED_COST:'+name)
        if name=='process_tree_rss' and x.get('kind')=='MEASURED':
            peak=x.get('selected_peak_bytes')
            if not isinstance(peak,int) or peak<1:e.append('MEASURED_RSS_NO_NUMERIC_PEAK')
            elif peak>6442450944:e.append('MEASURED_RSS_HARD_VETO_FAIL')
    if isready and workload.get('source_width_grade') not in {'EXECUTED_SOURCEFREE_WIDE','EXECUTED_NATIVE_SOURCE_WIDE'}:e.append('READY_WITH_UNPROVEN_REALISTIC_WIDTH')
    # Builder handback: handoff must be grounded and at least one real cold-start sample.
    h=s.get('handoffs',[]);h=h if isinstance(h,list) else [];hids=[]
    for x in h:
        if not isinstance(x,dict):e.append('BAD_HANDOFF');continue
        required(x,['id','boundary','recipient_owner','producer_symbol','producer_cut','consumer_symbol','consumer_status','input_abi','output_abi','transformation','negative','restore','test_command','expected_first_effect','source_authority','implementation_status','required_now_or_future','dependencies','evidence_ids'], 'HANDOFF',e)
        hids.append(x.get('id'))
        if x.get('boundary') not in BOUND:e.append('HANDOFF_INVALID_BOUNDARY:'+str(x.get('id')))
        if x.get('consumer_status') not in {'ACTUAL','PLANNED','HELD'}:e.append('HANDOFF_BAD_CONSUMER_STATUS:'+str(x.get('id')))
        if x.get('implementation_status') not in {'READY_FOR_IMPLEMENTER','SPECIFIED_OWNER_HELD','ALREADY_ACCEPTED_SCOPED'}:e.append('HANDOFF_BAD_BUILD_STATUS:'+str(x.get('id')))
        if x.get('required_now_or_future') not in NECESSITY:e.append('HANDOFF_NO_MATURITY_GRADE:'+str(x.get('id')))
        evidence_ids(x.get('evidence_ids'),'HANDOFF:'+str(x.get('id')))
        if x.get('implementation_status')=='READY_FOR_IMPLEMENTER' and x.get('consumer_status')!='ACTUAL':e.append('BUILDER_READY_WITH_NO_REAL_READER:'+str(x.get('id')))
    if len(hids)!=len(set(hids)):e.append('DUPLICATE_HANDOFF')
    valid_deps=set(hids)|decision_ids|set(nmap)
    for x in h:
        if isinstance(x,dict) and (not isinstance(x.get('dependencies'),list) or any(d not in valid_deps for d in x.get('dependencies',[]))):e.append('HANDOFF_DEPENDENCY_ORPHAN:'+str(x.get('id')))
    if set(x.get('boundary') for x in h if isinstance(x,dict))!=set(BOUND):e.append('INCOMPLETE_DOWNSTREAM_HANDOFF_BOUNDARIES')
    cold=s.get('builder_cold_start',{})
    required(cold,['selected_handoff_id','independent_reader','cold_start_result','instruction_without_new_archaeology','test_positive','test_denied','test_restore','missing_information','evidence_ids'], 'COLD_BUILDER',e)
    if cold.get('selected_handoff_id') not in hids:e.append('COLD_BUILDER_HANDOFF_ORPHAN')
    if cold.get('cold_start_result')!='PENDING_INDEPENDENT_C':e.append('AUTHOR_PRETENDS_C_REVIEW_COMPLETE')
    evidence_ids(cold.get('evidence_ids'),'COLD_BUILDER')
    # At P2 author can propose design readiness but C cold builder has not run.
    # Output: no fake author S3, no unreviewed owner accreditation.
    auth=s.get('authority',{})
    required(auth,['author_scope','independent_review','engineering_accepted','scientific_granted','source_rights_granted','actor_granted','protected_received'], 'AUTHORITY',e)
    if auth.get('author_scope') not in {'S0_S1_DOCUMENTARY','S2_SOURCEFREE_SCOPED','S2_NATIVE_SCOPED'}:e.append('INVALID_AUTHOR_SCOPE')
    if auth.get('independent_review')!='PENDING_C':e.append('AUTHOR_MINTED_INDEPENDENT_RECEIVING')
    if any(auth.get(k) is True for k in ('engineering_accepted','scientific_granted','source_rights_granted','actor_granted','protected_received')):e.append('AUTHOR_MINTED_DOWNSTREAM_AUTHORITY')
    if isready and not evidence_root:e.append('DESIGN_READY_REQUIRES_EXECUTION_RECEIPTS_FOR_AUDIT')
    if s.get('outcome') in {'DECISION_BLOCKED_EXACT','CONDITIONAL_CANDIDATE','INCUMBENT_REJECTED_SCOPED'}:
        blocks=s.get('blockers',[])
        if not isinstance(blocks,list) or not blocks:e.append('MISSING_EXACT_BLOCKER_OR_CONDITION')
        else:
            for i,block in enumerate(blocks):
                required(block,['decision_id','unproved_fact','if_positive','if_negative','smallest_proof','owner','what_can_proceed','decision_impact'], 'BLOCKER:'+str(i),e)
    from r5_contract import check_spine
    e.extend(check_spine(s,evidence_root=evidence_root,strict_repo=strict_repo))
    return sorted(set(e))


def validate(s,evidence_root=None,strict_repo=None):
    if not isinstance(s,dict):return ['MALFORMED_SPINE_NOT_OBJECT']
    try:return _validate(s,evidence_root=evidence_root,strict_repo=strict_repo)
    except (AttributeError,TypeError,KeyError,ValueError,IndexError,OverflowError) as ex:return ['MALFORMED_SPINE_REJECTED:'+type(ex).__name__+':'+str(ex)[:160]]


def rendered(s):
    lines=['# ANVIL — architected decision and construction inheritance','',f"**Author-proposed grade:** {s['outcome']} (independent C and owner receiving separate)",f"**Pinned starting baseline:** {s['baseline_sha']}",'',s['verdict_reason'],'','## The integrated whole-machine graph']
    for n in s.get('architecture',{}).get('nodes',[]):lines.append(f"- {n['id']} [{n['domain']}] {n['implementation']} ({n['decision_id']}/{n['alternative_id']})")
    for edge in s.get('architecture',{}).get('edges',[]):lines.append(f"- {edge['id']}: {edge['from']} -> {edge['to']} : {edge['data_type']} [{edge['boundary']}] ({edge['transition_class']}/{edge['temporal_mode']})")
    lines+=['','## Decisions']
    for d in s['decisions']:
        lines+=['',f"### {d['id']} — {d['question']}",f"- First real/planned consumer: {d['first_consumer']}",f"- Selected: {d['selected']}",f"- Comparison: {d['comparison_summary']}"]
        for a in d['alternatives']:lines.append(f"  - {a['id']} [{a['origin']}]: {a['status']}; {a['elimination_or_selection_reason']}")
        for x in d['discriminators']:lines.append(f"  - Discriminator {x['id']}: {x['status']}; positive {x['outcome_if_a']}; negative {x['outcome_if_b']}; smallest test {x['smallest_test']}")
    lines+=['','## Fixed seven boundary contracts']
    for k in BOUND:
        d=s['boundaries'][k];lines.append(f"- {k}: **{d['contract_name']}**; consumer {d['first_consumer']}; status {d['status']}; deny {d['negative']}")
    lines+=['','## Honest physical evidence']
    for x in s['workload']['measures']:lines.append(f"- {x['dimension']}: {x['kind']}; {x['discriminator_effect']}")
    lines+=['','## Material blockers / conditional next tests']
    for b in s.get('blockers',[]):lines.append(f"- {b['decision_id']}: {b['unproved_fact']}; {b['smallest_proof']}; owner {b['owner']}")
    lines+=['','## Proof boundary','This document is generated from SPINE.json and is neither source-native acceptance nor independently certified scientific/actor authority.']
    return '\n'.join(lines)+'\n'


def tsv(header,rows):
    buf=io.StringIO();out=csv.writer(buf,delimiter='\t',lineterminator='\n');out.writerow(header);out.writerows(rows);return buf.getvalue().encode()

def outputs(s):
    out={'DESIGN_DECISION.md':rendered(s).encode()}
    cov=[]
    for group in REQUIRED:
        for ident in REQUIRED[group]:
            v=s['coverage'][group][ident]
            cov.append([group,ident,v['necessity'],v['status'],','.join(v['decision_ids']),v['source_anchor'],v['source_semantics'],v['consumer_or_hold'],v['negative_meaning'],v['architecture_effect'],','.join(v['evidence_ids']),v['why']])
    out['COVERAGE_TO_DECISION.tsv']=tsv(['group','id','necessity','status','decision_ids','source_anchor','source_semantics','consumer_or_hold','negative_meaning','architecture_effect','evidence_ids','why'],cov)
    out['DOWNSTREAM_BUILD_HANDOFF.jsonl']=(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in s['handoffs'])).encode()
    out['EVIDENCE_AND_FALSIFIER_INDEX.jsonl']=(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in s['evidence'])).encode()
    out['GLOBAL_ARCHITECTURE.json']=json.dumps(s['architecture'],sort_keys=True,ensure_ascii=False,indent=2).encode()
    out['BOUNDARY_TRACE.json']=json.dumps({'boundaries':s['boundaries'],'integrated_epistemic_case':s['epistemic_case'],'provenance':s.get('observability_provenance',{})},sort_keys=True,ensure_ascii=False,indent=2).encode()
    return out

def check_dir(path,**kwargs):
    s=json.loads((path/'SPINE.json').read_text());problems=validate(s,**kwargs)
    if not problems:
        for name,data in outputs(s).items():
            p=path/name
            if not p.is_file() or p.read_bytes()!=data:problems.append('PROJECTION_MISSING_OR_CHANGED:'+name)
    return problems

def main():
    a=argparse.ArgumentParser();a.add_argument('action',choices=['verify','render','selftest']);a.add_argument('directory',nargs='?',default='.');a.add_argument('--evidence-root');a.add_argument('--repo');p=a.parse_args()
    if p.action=='selftest':
        from test_r5 import main as t
        return t()
    root=pathlib.Path(p.directory);s=json.loads((root/'SPINE.json').read_text())
    e=validate(s,evidence_root=p.evidence_root,strict_repo=p.repo)
    if p.action=='render' and not e:
        for name,data in outputs(s).items():(root/name).write_bytes(data)
    if not e:e=check_dir(root,evidence_root=p.evidence_root,strict_repo=p.repo)
    print(json.dumps({'status':'PASS_STRUCTURE_AND_CROSS_CONTRACT_CONSISTENCY_ONLY' if not e else 'RED','errors':e,'counts':{'coverage':sum(len(v) for v in s.get('coverage',{}).values()),'decisions':len(s.get('decisions',[])),'handoffs':len(s.get('handoffs',[]))}},indent=2))
    return 0 if not e else 2
if __name__=='__main__':sys.exit(main())