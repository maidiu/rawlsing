#!/usr/bin/env python3
"""Legacy specialist R7 stage receiving: actual evidence-byte reads, external grade ceilings.

This local checker cannot authenticate distinct reviewers, live GitHub, original-source
science, or protected CAS. Unlike R5/R6, it never returns local H1 accreditation.
"""
from __future__ import annotations
import argparse,ast,hashlib,json,pathlib,subprocess,sys
from r7_decision import compare,check_decision_dag,digest,load_bytes,_read_json,sha,ishash,H40

SCHEMA='ANVIL_R7_STAGE'

def check_priority_C(packet, result, frozen):
    """Require a concrete C assessment whenever H0 owner priorities broke a tradeoff.

    External independence and competent owner consent are NOT authenticated locally.
    """
    e=[]
    if not str(result.get('status','')).endswith('_PRIORITY_WIN_PENDING_INDEPENDENT_C'):
        return e
    p=packet.get('priority_adjudication')
    if not isinstance(p,dict):return ['R7_C_PRIORITY_WIN_WITHOUT_CHALLENGED_PRIORITY_REVIEW']
    if p.get('priority_source_sha256')!=frozen.get('priority_rule',{}).get('owner_source_sha256'):
        e.append('R7_C_PRIORITY_NOT_BOUND_TO_OWNER_SOURCE')
    if p.get('selected_candidate')!=result.get('winner'):
        e.append('R7_C_PRIORITY_REVIEW_CHANGED_WINNER')
    if p.get('independent_external_review_pending') is not True:
        e.append('R7_C_PRIORITY_CANNOT_SELF_ACCREDIT_REVIEW')
    for k in ('first_consumer_priority_justification','B_strongest_concrete_objection',
              'why_every_regression_is_acceptable','what_would_reverse_selection'):
        if not isinstance(p.get(k),str) or len(p[k].strip())<60:
            e.append('R7_C_PRIORITY_MISSING_SUBSTANTIVE_'+k)
    return e


def _loc(packet,key,root,errors,code):
    item=packet.get(key)
    if not isinstance(item,dict):errors.append(code+'_MISSING_POINTER');return None
    return _read_json(root,item.get('path'),item.get('sha256'),errors,code)

def check_symbol(root,ref):
    if not isinstance(ref,str) or ref.count('::')!=1:return False
    rel,sym=ref.split('::')
    if rel.startswith('/') or '..' in pathlib.PurePosixPath(rel).parts or not sym.isidentifier():return False
    r=pathlib.Path(root).resolve();p=(r/rel).resolve()
    if not p.is_relative_to(r) or not p.is_file() or p.suffix!='.py':return False
    try:tree=ast.parse(p.read_text())
    except (SyntaxError,UnicodeDecodeError):return False
    return any(isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and node.name==sym for node in tree.body)

def check_builder(card,source_root,receipt_root):
    e=[];grade=card.get('grade')
    if grade not in {'SPECIFICATION_CONSTRUCTION_READY','EXECUTED_FIRST_READER_PROOF','EXACT_BUILDER_HOLD'}:
        return ['R7_BUILDER_INVALID_GRADE']
    if grade=='EXACT_BUILDER_HOLD':
        if not isinstance(card.get('exact_hold'),str) or len(card['exact_hold'])<30:e.append('R7_BUILDER_HOLD_NOT_EXACT')
        return e
    if source_root is None:e.append('R7_BUILDER_NO_SOURCE_SNAPSHOT_FOR_READY');return e
    for field in ('producer_symbol','consumer_symbol'):
        if not check_symbol(source_root,card.get(field)):e.append('R7_BUILDER_NONEXISTENT_'+field)
    if not ishash(card.get('source_head'),H40):e.append('R7_BUILDER_UNPINNED_SOURCE_HEAD')
    for field,hashfield in (('producer_symbol','producer_sha256'),('consumer_symbol','consumer_sha256')):
        ref=card.get(field)
        if isinstance(ref,str) and ref.count('::')==1:
            rel=ref.split('::')[0];r=pathlib.Path(source_root).resolve();q=(r/rel).resolve()
            if not q.is_relative_to(r) or not q.is_file() or sha(q.read_bytes())!=card.get(hashfield):
                e.append('R7_BUILDER_SOURCE_BYTES_NOT_PINNED:'+field)
    if grade=='SPECIFICATION_CONSTRUCTION_READY':
        repo=pathlib.Path(source_root)
        if not (repo/'.git').exists():
            e.append('R7_BUILDER_CANNOT_DECLARE_REAL_GIT_READINESS_FROM_NON_GIT_SNAPSHOT')
        else:
            try:
                actual=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],stderr=subprocess.DEVNULL,text=True,timeout=6).strip()
                if actual!=card.get('source_head'):e.append('R7_BUILDER_SOURCE_HEAD_NOT_THE_CHECKED_OUT_COMMIT')
                for field in ('producer_symbol','consumer_symbol'):
                    ref=card.get(field)
                    if isinstance(ref,str) and ref.count('::')==1:
                        rel=ref.split('::')[0]
                        committed=subprocess.check_output(['git','-C',str(repo),'show','HEAD:'+rel],stderr=subprocess.DEVNULL,timeout=6)
                        if sha(committed)!=sha((repo/rel).read_bytes()):
                            e.append('R7_BUILDER_SOURCE_FILE_NOT_AT_PINNED_GIT_HEAD:'+field)
            except (OSError,subprocess.SubprocessError):e.append('R7_BUILDER_CANNOT_AUTHENTICATE_LOCAL_GIT_HEAD_OR_COMMITTED_SYMBOL')
    if not isinstance(card.get('test_command'),str) or not card['test_command'].startswith(('python -m unittest ','python3 -m unittest ','python tools/','python3 tools/')):
        e.append('R7_BUILDER_UNSAFE_OR_UNDEFINED_TEST_COMMAND')
    if not isinstance(card.get('first_consumer'),str) or len(card['first_consumer'])<12:e.append('R7_BUILDER_NO_FIRST_CONSUMER')
    if grade=='EXECUTED_FIRST_READER_PROOF':
        proof=_loc(card,'executed_test_receipt',receipt_root,e,'R7_BUILDER_EXECUTED_RECEIPT')
        if proof is not None:
            if proof.get('schema')!='ANVIL_R7_EXECUTION_TEST_RECEIPT' or proof.get('command')!=card.get('test_command') or proof.get('exit_code')!=0 or proof.get('execution_kind')=='SYNTHETIC_TEST':
                e.append('R7_BUILDER_EXECUTION_NOT_PROVED_BY_RECEIPT_CONTENT')
            for field in ('first_consumer_effect','negative_refusal','restore_replay','runner_code_head','source_or_fixture_sha256'):
                if not proof.get(field):e.append('R7_BUILDER_EXECUTION_RECEIPT_MISSING_'+field)
    return e

def check(stage,packet,receipt_root,source_root=None):
    e=[]
    if not isinstance(packet,dict) or packet.get('schema')!=SCHEMA or packet.get('stage')!=stage:return {'status':'RED','errors':['R7_STAGE_SCHEMA_OR_NAME_MISMATCH']}
    if receipt_root is None:return {'status':'RED','errors':['R7_STAGE_MISSING_EVIDENCE_ROOT']}
    if stage=='ANALYTICAL':
        frozen=_loc(packet,'frozen_plan',receipt_root,e,'R7_ANALYTICAL_FROZEN')
        proof=_loc(packet,'analytical_proof',receipt_root,e,'R7_ANALYTICAL_PROOF')
        if packet.get('verdict')!='ANALYTICAL_PROOF_SUBMITTED_FOR_C':
            e.append('R7_ANALYTICAL_FALSE_REVIEW_GRADE')
        if frozen is not None and proof is not None:
            from r7_analytical_elimination import check as check_elimination
            result=check_elimination(proof,frozen,receipt_root,source_root)
            if result['status']=='RED':e.extend('R7_ANALYTICAL:'+x for x in result['errors'])
            if result['winner'] is not None:e.append('R7_ANALYTICAL_AUTOMATIC_ARCHITECTURE_SELECTION')
        return {'status':'RED' if e else 'PASS_LOCAL_ANALYTICAL_EVIDENCE_ONLY__C_AND_OWNER_PENDING',
                'errors':sorted(set(e))}
    if stage=='P15':
        data=_loc(packet,'comparison_input',receipt_root,e,'R7_P15_COMPARISON_INPUT')
        frozen=_loc(packet,'frozen_plan',receipt_root,e,'R7_P15_FROZEN_PLAN')
        if data is not None and frozen is not None:
            res=compare(data,frozen,receipt_root)
            if res.get('winner') is None or res['status']=='RED':e.append('R7_P15_NO_RECEIPT_BOUND_DECISIVE_COMPARISON:'+res['status'])
            if packet.get('comparison_verdict')!=res['status'] or packet.get('provisional_winner')!=res['winner']:
                e.append('R7_P15_RESULT_MISMATCH')
            if packet.get('frozen_digest')!=digest(frozen):e.append('R7_P15_FROZEN_DIGEST_NOT_RECONCILED')
            if packet.get('material_cell_ids')!=sorted(c['id'] for c in frozen['cells']):e.append('R7_P15_INCOMPLETE_MATERIAL_CELL_SET')
            if packet.get('verdict')!='P15_MATCHED_DECISIVE_WITNESS_PROVISIONAL':e.append('R7_P15_FALSE_RECEIVING_GRADE')
            if not isinstance(packet.get('first_consumer'),str) or len(packet['first_consumer'])<12:e.append('R7_P15_NO_REAL_FIRST_CONSUMER')
            # A P15 comparator acceptance has no self-issued independent scientific or
            # source-rights authority. The stage must say so regardless of JSON flags.
            if packet.get('independent_science_or_runner_accredited') is not False:e.append('R7_P15_SELF_AUTHENTICATION_PROHIBITED')
        return {'status':'RED' if e else 'PASS_LOCAL_RECEIPT_CONTENT_ONLY_P15_PROVISIONAL','errors':sorted(set(e))}
    if stage=='C':
        p15=_loc(packet,'P15_receipt',receipt_root,e,'R7_C_P15')
        p2=_loc(packet,'P2_spine',receipt_root,e,'R7_C_P2')
        frozen=_loc(packet,'frozen_plan',receipt_root,e,'R7_C_FROZEN')
        data=_loc(packet,'comparison_input',receipt_root,e,'R7_C_COMPARISON')
        ledger=_loc(packet,'decision_ledger',receipt_root,e,'R7_C_DECISION_LEDGER')
        typed=_loc(packet,'typed_boundaries',receipt_root,e,'R7_C_TYPED_BOUNDARIES')
        if all(x is not None for x in (p15,p2,frozen,data,ledger)):
            if p15.get('schema')!=SCHEMA or p15.get('stage')!='P15':e.append('R7_C_NOT_AN_ACTUAL_P15_PACKET')
            checkp=check('P15',p15,receipt_root,source_root)
            if checkp['status'].startswith('RED'):e.append('R7_C_P15_FAILED:'+repr(checkp['errors']))
            cmp=compare(data,frozen,receipt_root)
            if cmp.get('winner') not in ('A','B'):e.append('R7_C_NO_DECISIVE_COMPARISON')
            e.extend(check_decision_dag(ledger,cmp,frozen,p2))
            e.extend(check_priority_C(packet,cmp,frozen))
            # The original R5/R6 complete meaning/consumer SPINE must be passed
            # through its source-validating machine, not replaced by a small roster.
            from r5_contract import check_spine
            if p2.get('schema')!='ANVIL_SPINE_R6':e.append('R7_C_MISSING_FULL_R5_R6_SPINE')
            else:e.extend('R7_C_BASE_SPINE:'+x for x in check_spine(p2,receipt_root))
            if packet.get('verdict')=='C_ACCEPT_SCOPED' and p2.get('outcome')!='DESIGN_READY_SCOPED':
                e.append('R7_C_ACCEPT_WITHOUT_FULL_SPINE_DESIGN_READY')
            if typed is not None:
                from r7_typed import validate as typed_validate
                e.extend(typed_validate(typed,p2))
            if packet.get('selected_candidate')!=cmp.get('winner'):e.append('R7_C_SELECTED_OTHER_CANDIDATE')
            if p2.get('comparison_receipt',{}).get('declared_winner')!=cmp.get('winner'):
                e.append('R7_C_LEGACY_SPINE_WINNER_DISAGREES_WITH_R7')
            for d in p2.get('decisions',[]):
                if isinstance(d,dict) and d.get('class')=='PHYSICAL':
                    alts={a.get('id'):a for a in d.get('alternatives',[]) if isinstance(a,dict)}
                    selected=alts.get(d.get('selected'),{})
                    expected_origin='A_INCUMBENT' if cmp.get('winner')=='A' else 'B_INDEPENDENT'
                    if selected.get('origin')!=expected_origin:
                        e.append('R7_C_LEGACY_PHYSICAL_ALTERNATIVE_DISAGREES_WITH_R7')
            for m in p2.get('physical_decision_evidence',[]):
                if isinstance(m,dict) and m.get('selected_candidate')!=cmp.get('winner'):
                    e.append('R7_C_LEGACY_PHYSICAL_EVIDENCE_DISAGREES_WITH_R7')
        builder_cards=packet.get('builder_cards',[])
        if not isinstance(builder_cards,list) or len(builder_cards)!=2 or len({c.get('id') for c in builder_cards if isinstance(c,dict)})!=2:
            e.append('R7_C_NEEDS_DISTINCT_PRESENT_AND_FUTURE_BUILDER');builder_cards=[]
        if builder_cards:
            if {c.get('domain') for c in builder_cards}!={'CURRENT_FIRST_CONSUMER','FUTURE_NONPRECLUSION'}:
                e.append('R7_C_BUILDER_DOMAIN_MISMATCH')
            for card in builder_cards:e.extend(check_builder(card,source_root,receipt_root))
            current=next((card for card in builder_cards if card.get('domain')=='CURRENT_FIRST_CONSUMER'),{})
            if all(x is not None for x in (p15,p2,frozen,data,ledger)):
                expected=frozen.get('candidate_code_heads',{}).get(packet.get('selected_candidate'))
                if current.get('candidate_code_head')!=expected:
                    e.append('R7_C_BUILDER_NOT_BOUND_TO_SELECTED_CANDIDATE_HEAD')
                elif current.get('source_head')!=expected and current.get('grade')!='EXACT_BUILDER_HOLD':
                    bridge=_loc(current,'first_consumer_compatibility_receipt',receipt_root,e,'R7_C_BUILDER_ABI_BRIDGE')
                    if bridge is not None:
                        if (bridge.get('schema')!='ANVIL_R7_FIRST_CONSUMER_ABI_BRIDGE'
                                or bridge.get('candidate_code_head')!=expected
                                or bridge.get('builder_source_head')!=current.get('source_head')
                                or bridge.get('first_consumer')!=current.get('first_consumer')
                                or any(not isinstance(bridge.get(x),str) or len(bridge[x])<20
                                       for x in ('input_abi','output_abi','negative_restore_test'))):
                            e.append('R7_C_BUILDER_ABI_BRIDGE_NOT_BINDING_TO_SELECTED_SYSTEM')
        objection=packet.get('strongest_surviving_objection')
        if not isinstance(objection,dict) or objection.get('could_change_choice') not in {'YES','NO'}:
            e.append('R7_C_NO_INDEPENDENT_STRONGEST_OBJECTION')
        elif objection.get('could_change_choice')=='YES':e.append('R7_C_CHOICE_REVERSING_OBJECTION_SURVIVES')
        elif not isinstance(objection.get('reason_and_evidence'),str) or len(objection['reason_and_evidence'])<40:e.append('R7_C_OBJECTION_NONREVERSAL_UNPROVED')
        if packet.get('reviewer_relationship')!='DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION':
            e.append('R7_C_FALSE_INDEPENDENCE_CERTIFICATION')
        if packet.get('verdict')=='C_ACCEPT_SCOPED' and builder_cards and builder_cards[0].get('grade')=='EXACT_BUILDER_HOLD':
            e.append('R7_C_ACCEPTS_HELD_FIRST_BUILDER')
        if packet.get('verdict') not in {'C_ACCEPT_SCOPED','C_ACCEPT_DOCUMENTARY_HOLD'}:e.append('R7_C_BAD_VERDICT')
        return {'status':'RED' if e else 'PASS_LOCAL_STRUCTURE_AND_RECEIPT_CONTENT_ONLY_C_PENDING_INDEPENDENT_REVIEW','errors':sorted(set(e))}
    if stage=='H1':
        # No local JSON field can grant real protected receiving. Actual GitHub
        # currentness, competent owner, protected CAS and paired progress are an
        # external check, even if their claimed evidence files are hash-consistent.
        _loc(packet,'C_receipt',receipt_root,e,'R7_H1_C_RECEIPT')
        _loc(packet,'P2_receipt',receipt_root,e,'R7_H1_P2_RECEIPT')
        if packet.get('verdict') in {'H1_RECEIVED_SCOPED','H1_RECEIVED_CONDITIONAL'}:
            e.append('R7_H1_PROTECTED_RECEIVING_REQUIRES_LIVE_AUTHORIZED_EXTERNAL_CAS')
        elif packet.get('verdict') not in {'HQ_CURRENTNESS_HOLD','H1_READY_FOR_EXTERNAL_OWNER_RECEIVING'}:
            e.append('R7_H1_INVALID_LOCAL_VERDICT')
        if packet.get('scientific_granted_YN')=='YES' or packet.get('source_rights_granted_YN')=='YES' or packet.get('actor_granted_YN')=='YES':
            e.append('R7_H1_UNSUPPORTED_SCIENCE_SOURCE_OR_ACTOR_PROMOTION')
        return {'status':'RED' if e else 'PASS_LOCAL_PRE_RECEIVING_ONLY_EXTERNAL_CAS_PENDING','errors':sorted(set(e))}
    return {'status':'RED','errors':['R7_STAGE_NOT_SUPPORTED']}

def main():
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['FRAME','DECISION','C_INTEGRATED','ANALYTICAL','P15','C','H1']);p.add_argument('packet');p.add_argument('--evidence-root',required=True);p.add_argument('--source-root');p.add_argument('--legacy-regression',action='store_true',help='Explicit opt-in for obsolete P15/C comparison machinery (NEVER an active ANVIL decision)');a=p.parse_args()
    if a.stage in {'P15','C'} and not a.legacy_regression:
        print(json.dumps({'status':'RED','errors':['R7_LEGACY_A_B_STAGE_NOT_ACTIVE_USE_INTEGRATED_FRAME_DECISION_C']},indent=2));return 2
    if a.stage in {'FRAME','DECISION','C_INTEGRATED'}:
        from r7_integrated import check as check_active
        if a.source_root is None:
            print(json.dumps({'status':'RED','errors':['R7_INTEGRATED_SOURCE_ROOT_REQUIRED']},indent=2));return 2
        try:res=check_active(a.stage,json.loads(pathlib.Path(a.packet).read_text()),a.evidence_root,a.source_root)
        except (OSError,ValueError,TypeError,KeyError) as ex:res={'status':'RED','errors':['R7_INTEGRATED_MALFORMED:'+repr(ex)]}
        print(json.dumps(res,indent=2));return 2 if res['status']=='RED' else 0
    try:res=check(a.stage,json.loads(pathlib.Path(a.packet).read_text()),a.evidence_root,a.source_root)
    except (OSError,ValueError,TypeError,KeyError) as x:res={'status':'RED','errors':['R7_STAGE_MALFORMED:'+type(x).__name__+':'+str(x)]}
    print(json.dumps(res,indent=2));return 2 if res['status']=='RED' else 0
if __name__=='__main__':sys.exit(main())
