#!/usr/bin/env python3
"""Active ANVIL R7 integral investigation and decision gates.

A/B *duel* is OPTIONAL, and then only for a named question with shared evidence.
The obsolete full-architecture A/B comparator remains a read-only historical
specialist, not the active selection authority. All positives are LOCAL and do
not authenticate source rights, independent reviews, runner results, or HQ.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re, subprocess, sys, zipfile
from anvil import REQUIRED
from r7_inventory import check_inventory, ORIGINAL_ZIP_SHA

SCHEMA='ANVIL_R7_INTEGRATED'
HEX40=re.compile(r'^[a-f0-9]{40}$')
HEX64=re.compile(r'^[a-f0-9]{64}$')
DOMAINS=('SOURCE_SEMANTICS','C11_PERSISTENCE','CURRENT_I03_I05',
         'HISTORICAL_DDM_FUNCTIONS','F1_F4_ANALYTICS','FIELD_FORGE',
         'SEAM_WORLD_ACTOR','AUTHORITY_AND_RECOVERY','RESOURCE_ECONOMICS')
BINDS={'PRESENT_HARD','FUTURE_NONPRECLUSION','EXTERNAL_OWNER_HELD'}
DISPOS={'PRESENT_PRESERVED','FUTURE_NONPRECLUDED','EXACT_OWNER_HOLD','BLOCKING_LOSS','REFUSED_AUTHORITY'}
IDENTITY_STATES={'PRESENT_PRESERVED','FUTURE_NONPRECLUDED','EXACT_OWNER_HOLD','BLOCKING_LOSS','REFUSED_AUTHORITY','RETAINED_HISTORICAL_NONADOPTED'}
GRAPH_TIME={'OBSERVED','HISTORICAL_AS_OF','MODELED','FICTIONAL','MIXED_TYPED'}
BOUND_IDS=('T1','T2','T3','T4','T5','T6','T7')
# Exact decision-requirement roster: nine whole-machine domains plus seven
# cross-cutting obligations that the 118 identity dispositions alone do not
# spell out.  The roster is code-fixed so deleting a free-form requirement is
# no longer a silent no-loss path (D4A/A6).
REQUIREMENT_ROSTER=(
 'REQ-SOURCE-SEMANTICS','REQ-C11-PERSISTENCE','REQ-CURRENT-I03-I05',
 'REQ-HISTORICAL-DDM','REQ-F1-F4','REQ-FIELD-FORGE','REQ-SEAM-WORLD-ACTOR',
 'REQ-AUTHORITY-RECOVERY','REQ-RESOURCE-ECONOMICS',
 'REQ-MULTIWAY-JOINT','REQ-DENOMINATOR-MISSING-ROUTING',
 'REQ-PHYSICAL-WORKLOAD-1-10-100','REQ-SOURCE-I02-REVOCATION',
 'REQ-FF01-FF02-WORLD-ACTOR-FIREWALL','REQ-TERMINAL-F5-F8-N11-N12',
 'REQ-HISTORICAL-NOADOPTION-CONSERVATION')
REQUIREMENT_DOMAIN={
 'REQ-SOURCE-SEMANTICS':'SOURCE_SEMANTICS','REQ-C11-PERSISTENCE':'C11_PERSISTENCE',
 'REQ-CURRENT-I03-I05':'CURRENT_I03_I05','REQ-HISTORICAL-DDM':'HISTORICAL_DDM_FUNCTIONS',
 'REQ-F1-F4':'F1_F4_ANALYTICS','REQ-FIELD-FORGE':'FIELD_FORGE',
 'REQ-SEAM-WORLD-ACTOR':'SEAM_WORLD_ACTOR','REQ-AUTHORITY-RECOVERY':'AUTHORITY_AND_RECOVERY',
 'REQ-RESOURCE-ECONOMICS':'RESOURCE_ECONOMICS',
 'REQ-MULTIWAY-JOINT':'F1_F4_ANALYTICS','REQ-DENOMINATOR-MISSING-ROUTING':'SOURCE_SEMANTICS',
 'REQ-PHYSICAL-WORKLOAD-1-10-100':'RESOURCE_ECONOMICS','REQ-SOURCE-I02-REVOCATION':'AUTHORITY_AND_RECOVERY',
 'REQ-FF01-FF02-WORLD-ACTOR-FIREWALL':'SEAM_WORLD_ACTOR','REQ-TERMINAL-F5-F8-N11-N12':'HISTORICAL_DDM_FUNCTIONS',
 'REQ-HISTORICAL-NOADOPTION-CONSERVATION':'AUTHORITY_AND_RECOVERY'}

TERMINAL_IDS=('F1','F2','F3','F4','F5','F6','F7','F8','N9','N10E','N10W','N11','N12','PRE-V3','SEAM','SOROK')
# Specific, mechanically encoded obligations.  This is not a universal truth
# scanner: it freezes the choice-changing distinctions already stated in the
# source court and refuses a coherent rewrite that erases them.  Semantic truth
# of the authored summary remains an external C/source-owner hold.
REQUIREMENT_SEMANTICS={
 'REQ-SOURCE-SEMANTICS':{'typed_obligation':'NATIVE_SOURCE_SEMANTICS','required_phrases':['native question','option','routing','missing'],'forbidden_phrases':['stratum implies sect','impute individual ancestry','normalization may replace']},
 'REQ-C11-PERSISTENCE':{'typed_obligation':'C11_BODY_LOCATOR','required_phrases':['body','locator','CURRENT','cold restore'],'forbidden_phrases':['body hash alone proves source']},
 'REQ-CURRENT-I03-I05':{'typed_obligation':'I03_I05_FIRST_READER','required_phrases':['I03','I05','sourcefree','source-native'],'forbidden_phrases':['sourcefree is native']},
 'REQ-HISTORICAL-DDM':{'typed_obligation':'HISTORICAL_FUNCTION_SEMANTICS','required_phrases':['V549','V550','V550J','F26'],'forbidden_phrases':['guard is the numeric','guard determines all','postgres is universal','f26 caller is proved']},
 'REQ-F1-F4':{'typed_obligation':'F1_F4_JOINT_DENOMINATOR','required_phrases':['same-person','k>=3','denominator','branch'],'forbidden_phrases':['marginal equality is sufficient']},
 'REQ-FIELD-FORGE':{'typed_obligation':'FF_DESCRIPTIVE_VS_STRUCTURAL','required_phrases':['FF01','FF02','descriptive','structural'],'forbidden_phrases':['ff01 is ff02']},
 'REQ-SEAM-WORLD-ACTOR':{'typed_obligation':'SEAM_ACTOR_BOUNDARY','required_phrases':['Other','encounter','access','SOROK'],'forbidden_phrases':['survey gives actor private knowledge']},
 'REQ-AUTHORITY-RECOVERY':{'typed_obligation':'I02_TRUST_REVOCATION','required_phrases':['I02','trust root','revocation','cold restore'],'forbidden_phrases':['producer hash is source truth']},
 'REQ-RESOURCE-ECONOMICS':{'typed_obligation':'RESOURCE_ECONOMICS','required_phrases':['100k','6 GiB','1/10/100','NOT_RUN'],'forbidden_phrases':['synthetic green benchmark']},
 'REQ-MULTIWAY-JOINT':{'typed_obligation':'SAME_PERSON_K3_JOINT','required_phrases':['three-way','same-person','joint','pairwise'],'forbidden_phrases':['pairwise marginal is sufficient','pairwise-only','no three-way','pairwise marginals are sufficient']},
 'REQ-DENOMINATOR-MISSING-ROUTING':{'typed_obligation':'DENOMINATOR_TYPED_MISSING','required_phrases':['forward','reverse','denominator','routing'],'forbidden_phrases':['one denominator for both']},
 'REQ-PHYSICAL-WORKLOAD-1-10-100':{'typed_obligation':'PHYSICAL_WORKLOAD','required_phrases':['600','1,300','process-tree','distinct'],'forbidden_phrases':['3.245 events is representative']},
 'REQ-SOURCE-I02-REVOCATION':{'typed_obligation':'SOURCE_I02_REVOCATION','required_phrases':['independent','source comparison','revoked','prepared'],'forbidden_phrases':['shared wrong hash is proof']},
 'REQ-FF01-FF02-WORLD-ACTOR-FIREWALL':{'typed_obligation':'FF_ACTOR_WORLD_FIREWALL','required_phrases':['survey','actor','knowledge','fictional'],'forbidden_phrases':['survey opinion is institutional power','survey answers give actor','fictional action edits observed']},
 'REQ-TERMINAL-F5-F8-N11-N12':{'typed_obligation':'TERMINAL_HOLD_DISCIPLINE','required_phrases':['F5','F8','N11','N12'],'forbidden_phrases':['seven stages','serial pipeline']},
 'REQ-HISTORICAL-NOADOPTION-CONSERVATION':{'typed_obligation':'HISTORICAL_NONADOPTION','required_phrases':['26','14','NOT_ADOPTED','HELD'],'forbidden_phrases':['adopt all','close all']},
}
IDENTITY_GUARDS={
 'K1-CAP-11':{'required':['three-way','joint','same-person'],'forbidden':['pairwise marginal is sufficient','pairwise-only','no three-way']},
 'K1-CAP-17':{'required':['F6','numeric'],'forbidden':['guard is the numeric','guard determines all','guard supplies the numeric']},
 'K1-CAP-24':{'required':['F26','hold'],'forbidden':['F26 caller proved','F26 equivalence proved']},
 'P4R-R02':{'required':['F26','hold'],'forbidden':['F26 caller proved','F26 equivalence proved']},
 'PYAT-PC-R11-21':{'required':['F26','hold'],'forbidden':['F26 caller proved','F26 equivalence proved']},
}
C_FORBIDDEN=('survey opinion is institutional power','survey answers give actor private knowledge','survey response gives actor knowledge','fictional action edits observed source','fictional action overwrites observed','no independent structural producer','respondent answers give the actor private')
GRADES={'CODE_STATIC','DOCUMENTARY','EXECUTED_SOURCEFREE','EXECUTED_NATIVE','UNVERIFIED_HELD'}
INVALID=('todo','tbd','placeholder','to be determined','see above','n/a','not applicable')

def good(x,n=24):
    return isinstance(x,str) and len(x.strip())>=n and not any(x.strip().lower()==s for s in INVALID)

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def sha(x):return hashlib.sha256(x).hexdigest()

def load(root,ptr,errors,code):
    if not isinstance(ptr,dict):errors.append(code+':NO_POINTER');return None
    rel=ptr.get('path');expected=ptr.get('sha256')
    if not isinstance(rel,str) or not rel or rel.startswith('/') or '\\' in rel or '..' in pathlib.PurePosixPath(rel).parts or not isinstance(expected,str) or not HEX64.fullmatch(expected):
        errors.append(code+':INVALID_LOCATOR');return None
    base=pathlib.Path(root).resolve() if root else None
    if base is None:errors.append(code+':NO_ROOT');return None
    path=(base/rel).resolve()
    if not path.is_relative_to(base) or not path.is_file() or path.is_symlink():errors.append(code+':UNSAFE_OR_ABSENT');return None
    data=path.read_bytes()
    if sha(data)!=expected:errors.append(code+':BYTES_CHANGED');return None
    try:return json.loads(data)
    except (UnicodeDecodeError,ValueError):errors.append(code+':MALFORMED_JSON');return None

def _git_blob_bytes(repo,commit,git_path,errors,code):
    if not isinstance(repo,str) or not repo:
        errors.append(code+':REPO_REQUIRED_FOR_GIT_ANCHOR');return None
    try:
        top=subprocess.run(['git','-C',repo,'rev-parse','--show-toplevel'],capture_output=True,text=True,timeout=30)
        if top.returncode!=0:errors.append(code+':REPO_NOT_A_GIT_OBJECT_STORE');return None
        obj=subprocess.run(['git','-C',repo,'rev-parse',commit+':'+git_path],capture_output=True,text=True,timeout=30)
        if obj.returncode!=0:errors.append(code+':GIT_PATH_NOT_IN_COMMIT');return None
        data=subprocess.run(['git','-C',repo,'cat-file','blob',obj.stdout.strip()],capture_output=True,timeout=30)
        if data.returncode!=0:errors.append(code+':GIT_BLOB_UNREADABLE');return None
        return data.stdout
    except (OSError,subprocess.SubprocessError):
        errors.append(code+':GIT_ANCHOR_UNREADABLE');return None

def source_ref(item,root,errors,code,repo=None,zip_path=None,strict=False):
    """Content pin plus exact quote, and in strict mode a real Git/ZIP anchor.

    A caller-controlled local file with a matching SHA-256 is NOT a source
    anchor (D4A/A4).  Strict evidence must name either an immutable Git
    commit:path:blob or the original supplied ZIP member.  This still proves
    retrieved bytes, never issuer competence, source rights or scientific truth.
    """
    if not isinstance(item,dict):errors.append(code+':NO_SOURCE');return
    rel=item.get('path');wanted=item.get('sha256');quote=item.get('exact_excerpt')
    if (not isinstance(rel,str) or not rel or rel.startswith('/') or '\\' in rel or '..' in pathlib.PurePosixPath(rel).parts
        or not isinstance(wanted,str) or not HEX64.fullmatch(wanted) or not good(quote,20)):
        errors.append(code+':INVALID_SOURCE_PIN');return
    if root is None:errors.append(code+':NO_SOURCE_ROOT');return
    base=pathlib.Path(root).resolve();p=(base/rel).resolve()
    if not p.is_relative_to(base) or not p.is_file() or p.is_symlink():errors.append(code+':SOURCE_NOT_FOUND');return
    body=p.read_bytes()
    if sha(body)!=wanted or quote.encode() not in body:errors.append(code+':SOURCE_HASH_OR_QUOTE_DISAGREES')
    # Strict anchor authentication.
    if strict:
        if item.get('commit') or item.get('git_path') or item.get('git_blob'):
            commit=item.get('commit');git_path=item.get('git_path');blob=item.get('git_blob')
            if not (isinstance(commit,str) and HEX40.fullmatch(commit) and isinstance(git_path,str) and git_path
                    and isinstance(blob,str) and re.fullmatch(r'^[a-f0-9]{40}$',blob)):
                errors.append(code+':MALFORMED_GIT_ANCHOR');return
            data=_git_blob_bytes(repo,commit,git_path,errors,code)
            if data is None:return
            actual='sha1:'+hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            if actual!='sha1:'+blob:errors.append(code+':GIT_BLOB_ID_DISAGREES')
            if sha(data)!=wanted or quote.encode() not in data:errors.append(code+':GIT_ANCHOR_BYTES_OR_QUOTE_DISAGREE')
        elif item.get('zip_sha256') or item.get('zip_member'):
            zsha=item.get('zip_sha256');member=item.get('zip_member')
            if zsha!=ORIGINAL_ZIP_SHA:errors.append(code+':NOT_THE_ORIGINAL_ZIP')
            if not isinstance(member,str) or not member or member.startswith('/') or '..' in pathlib.PurePosixPath(member).parts:
                errors.append(code+':INVALID_ZIP_MEMBER');return
            if not isinstance(zip_path,str) or not zip_path:
                errors.append(code+':ZIP_REQUIRED_FOR_ZIP_ANCHOR');return
            try:
                with zipfile.ZipFile(zip_path) as z:
                    data=z.read(member)
            except (OSError,KeyError,zipfile.BadZipFile):
                errors.append(code+':ZIP_MEMBER_ABSENT');return
            if sha(data)!=wanted or quote.encode() not in data:errors.append(code+':ZIP_MEMBER_BYTES_OR_QUOTE_DISAGREE')
        else:
            errors.append(code+':SOURCE_ANCHOR_MISSING')

def _check_release_register(frame,evidence_root,errors):
    rel=load(evidence_root,frame.get('release_register'),errors,'FRAME:RELEASE')
    if rel is None:return set()
    if rel.get('schema')!='ANVIL_R7_SOURCE_RELEASE_REGISTER':errors.append('FRAME:RELEASE_BAD_SCHEMA')
    current=rel.get('current');revoked=rel.get('revoked')
    if not isinstance(current,list) or not current:errors.append('FRAME:RELEASE_NO_CURRENT_PIN')
    if not isinstance(revoked,list):errors.append('FRAME:RELEASE_REVOKED_NOT_LIST');return set()
    revoked_shas=set()
    for x in revoked:
        if not isinstance(x,dict) or not isinstance(x.get('sha256'),str) or not HEX64.fullmatch(x['sha256']):
            errors.append('FRAME:RELEASE_BAD_REVOCATION_ENTRY')
        else:revoked_shas.add(x['sha256'])
    if not any(isinstance(x,dict) and x.get('sha256')==ORIGINAL_ZIP_SHA for x in current):
        errors.append('FRAME:RELEASE_ORIGINAL_ZIP_NOT_CURRENT')
    if ORIGINAL_ZIP_SHA in revoked_shas:errors.append('FRAME:RELEASE_ORIGINAL_ZIP_REVOKED')
    return revoked_shas

def _check_actor_world_boundary(decision,errors):
    aw=decision.get('actor_world_boundary')
    if not isinstance(aw,dict):
        errors.append('DECISION:NO_ACTOR_WORLD_BOUNDARY');return
    for flag in ('survey_implies_actor_knowledge','fictional_mutates_source','source_implies_material_power','actor_private_state_from_source'):
        if aw.get(flag) is not False:errors.append('DECISION:ACTOR_WORLD_FIREWALL_BREACH:'+flag)
    text=(decision.get('entire_source_to_actor_dataflow') or '')+' '+(decision.get('scientific_boundary_and_nonpreclusion') or '')
    low=text.lower()
    for phrase in ('survey answers directly determine','survey response directly gives actor','respondent answers give the actor private','fictional actor edits the observed source','opinion frequency is institutional power'):
        if phrase in low:errors.append('DECISION:ACTOR_WORLD_FIREWALL_BREACH:forbidden_text')

def _check_builder_receipt(card,evidence_root,source_root,errors):
    grade=card.get('grade')
    if grade=='EXACT_BUILDER_HOLD':
        if not good(card.get('exact_hold'),30):errors.append('C:BUILDER_HOLD_NOT_EXACT')
        return
    receipt=card.get('receipt')
    if not isinstance(receipt,dict):errors.append('C:BUILDER_RECEIPT_MISSING');return
    for k in ('argv','raw_log','host','time','runner_head','stdout_sha256','test_command'):
        if not receipt.get(k):errors.append('C:BUILDER_RECEIPT_FIELD:'+k)
    cmd=receipt.get('test_command')
    if isinstance(cmd,str):
        import shlex
        toks=shlex.split(cmd)
        # python3 from PATH is an interpreter, not a source script file.
        script=None
        for tok in toks:
            if pathlib.PurePath(tok).name.lower() in ('python','python3','python3.11','bash','sh','node','rscript'):
                continue
            if tok.startswith('-'):continue
            script=tok;break
        if not script:
            errors.append('C:BUILDER_NO_SCRIPT_AFTER_INTERPRETER')
        else:
            roots=[pathlib.Path(source_root),pathlib.Path(evidence_root),pathlib.Path(__file__).resolve().parent,pathlib.Path(__file__).resolve().parents[1]]
            if not any((r/script).is_file() for r in roots if r is not None):
                errors.append('C:BUILDER_NONEXISTENT_TEST_COMMAND:'+script)
    log=receipt.get('raw_log')
    if isinstance(log,dict):
        rel=log.get('path'); want=log.get('sha256')
        if not isinstance(rel,str) or not isinstance(want,str):errors.append('C:BUILDER_RAW_LOG_NOT_POINTER')
        else:
            pth=pathlib.Path(evidence_root)/rel
            if not pth.is_file():errors.append('C:BUILDER_RAW_LOG_MISSING')
            else:
                data=pth.read_bytes()
                if sha(data)!=want or receipt.get('stdout_sha256')!=want:errors.append('C:BUILDER_STDOUT_HASH_MISMATCH')
    else:
        errors.append('C:BUILDER_RAW_LOG_NOT_POINTER')
    custody=receipt.get('execution_custody')
    if grade=='EXECUTED_FIRST_READER_PROOF' and custody not in ('EXTERNAL_RUNNER_VERIFIED','OWNER_CUSTODY_VERIFIED'):
        errors.append('C:BUILDER_LOCAL_RECEIPT_CANNOT_SUPPORT_C_GRADE')

def check_history(obj,errors):
    if not isinstance(obj,dict) or obj.get('schema')!='ANVIL_R7_INHERITED_CONSERVATION':
        errors.append('HISTORY:WRONG_SCHEMA');return
    coverage=obj.get('coverage',{})
    if not isinstance(coverage,dict) or set(coverage)!=set(REQUIRED):
        errors.append('HISTORY:GROUPS_NOT_INHERITED');return
    count=0
    for group,ids in REQUIRED.items():
        rows=coverage.get(group,{})
        if not isinstance(rows,dict) or set(rows)!=set(ids):errors.append('HISTORY:ID_SET_DRIFT:'+group);continue
        for rid,entry in rows.items():
            count+=1
            if not isinstance(entry,dict):errors.append('HISTORY:NO_RECORD:'+rid);continue
            for key in ('source_anchor','source_semantics','consumer_or_hold','negative_meaning','architecture_effect','why'):
                if not good(entry.get(key),12):errors.append('HISTORY:SEMANTIC_OR_CONSUMER_LOSS:'+rid+':'+key)
            if not isinstance(entry.get('evidence_ids'),list) or not entry['evidence_ids']:
                errors.append('HISTORY:NO_EVIDENCE:'+rid)
            if group=='PYAT_PC' and (entry.get('adopted') is not False or entry.get('necessity')!='HISTORICAL_NOT_ADOPTED'):
                errors.append('HISTORY:FALSE_PROSPECTIVE_ADOPTION:'+rid)
            if group=='P4R' and (entry.get('closed') is not False or entry.get('necessity')!='HISTORICAL_PROOF_HELD'):
                errors.append('HISTORY:FALSE_PROOF_CLOSURE:'+rid)
    if count!=sum(map(len,REQUIRED.values())):errors.append('HISTORY:COUNT_DRIFT')
    if obj.get('source_authentication')!='NOT_AUTHENTICATED_BY_LOCAL_CHECK':errors.append('HISTORY:FALSE_SOURCE_AUTHENTICATION')

def check_graph(graph,errors,code='GRAPH'):
    """Typed whole-machine graph: producer, authority, time and consumer are explicit.

    This is a structural contract check, not proof that any edge executed.
    """
    if not isinstance(graph,dict):errors.append(code+':NOT_OBJECT');return
    nodes=graph.get('nodes');edges=graph.get('edges')
    if not isinstance(nodes,list) or not nodes:errors.append(code+':NO_NODES');nodes=[]
    if not isinstance(edges,list) or not edges:errors.append(code+':NO_EDGES');edges=[]
    nmap={};emap={}
    for n in nodes:
        if not isinstance(n,dict):errors.append(code+':BAD_NODE');continue
        rid=n.get('id')
        if not isinstance(rid,str) or not rid or rid in nmap:errors.append(code+':DUPLICATE_OR_MISSING_NODE')
        nmap[rid]=n
        for k in ('producer','producer_authority','input_types','output_types','time_mode','first_consumer','decision_id','alternative_id'):
            if k in ('input_types','output_types'):
                if not isinstance(n.get(k),list) or not n[k]:errors.append(code+':NODE_FIELD:'+str(rid)+':'+k)
            elif not good(n.get(k),2 if k in ('first_consumer','decision_id','alternative_id','time_mode') else 8):errors.append(code+':NODE_FIELD:'+str(rid)+':'+k)
        if n.get('time_mode') not in GRAPH_TIME:errors.append(code+':BAD_TIME_MODE:'+str(rid))
    for edge in edges:
        if not isinstance(edge,dict):errors.append(code+':BAD_EDGE');continue
        rid=edge.get('id')
        if not isinstance(rid,str) or not rid or rid in emap:errors.append(code+':DUPLICATE_OR_MISSING_EDGE')
        emap[rid]=edge
        for k in ('from','to','data_type','authority_grade','temporal_mode','negative_or_refusal','invalidation_rule','boundary'):
            if not good(edge.get(k),2 if k in ('from','to','boundary') else 6):errors.append(code+':EDGE_FIELD:'+str(rid)+':'+k)
        a=nmap.get(edge.get('from'));b=nmap.get(edge.get('to'))
        if not a or not b:errors.append(code+':ORPHAN_EDGE:'+str(rid));continue
        if edge.get('data_type') not in a.get('output_types',[]) or edge.get('data_type') not in b.get('input_types',[]):
            errors.append(code+':TYPE_MISMATCH:'+str(rid))
        if edge.get('boundary') not in BOUND_IDS:errors.append(code+':BAD_BOUNDARY:'+str(rid))
        observed_core={'SURVEY_RELEASE','INSTRUMENT','SEMANTIC_RULE','SOURCE_RIGHT','DESIGN_SCOPE','S01_PROJECT','I02_PROOF','C11_ESTATE','C11_ROOT','COLD_READ','I03','I05'}
        if a.get('time_mode') in ('FICTIONAL','MODELED') and b.get('time_mode')=='OBSERVED' and edge.get('to') in observed_core:
            errors.append(code+':FICTIONAL_BACKFLOW:'+str(rid))
    for t in BOUND_IDS:
        if not any(e.get('boundary')==t for e in edges if isinstance(e,dict)):errors.append(code+':BOUNDARY_EDGE_MISSING:'+t)
    if len(nodes)<30 or len(edges)<40:errors.append(code+':GRAPH_NOT_WHOLE_MACHINE')
    aliases={'F5':'F5_LEARNED','F8':'F8_POSITIONED','N11':'N11_ACCEPTANCE','N12':'N12_WAKE','PRE-V3':'PREV3','SEAM':'SEAM_HANDOFF','SOROK':'SOROK_CONTINUITY'}
    for tid in TERMINAL_IDS:
        n=nmap.get(tid) or nmap.get(aliases.get(tid,''))
        if not n:errors.append(code+':TERMINAL_NODE_MISSING:'+tid);continue
        if n.get('time_mode') not in GRAPH_TIME:errors.append(code+':TERMINAL_TIME_MODE:'+tid)
        held=(n.get('first_consumer')=='EXACT_HOLD') or bool(n.get('exact_hold'))
        if held and not good(n.get('exact_hold'),25):errors.append(code+':TERMINAL_HOLD_NOT_EXACT:'+tid)
        if not held and not good(n.get('first_consumer'),3):errors.append(code+':TERMINAL_NO_CONSUMER_OR_HOLD:'+tid)

def check_identity_dispositions(decision,inventory,source_root,errors,evidence_root=None,repo=None,zip_path=None):
    """Every one of the 118 identities must have a candidate-specific disposition.

    Presence of an ID is not preservation.  The origin must match the verified
    inventory row; 26 proposals cannot be adopted and 14 proofs cannot be closed.
    """
    if inventory is None:errors.append('DECISION:NO_VERIFIED_INVENTORY');return
    rows=decision.get('identity_dispositions')
    if not isinstance(rows,list):errors.append('DECISION:NO_IDENTITY_DISPOSITIONS');return
    inv={e['id']:e for e in inventory.get('entries',[]) if isinstance(e,dict)}
    dmap={}
    for x in rows:
        if not isinstance(x,dict):errors.append('DECISION:BAD_IDENTITY_DISPOSITION');continue
        rid=x.get('identity_id')
        if rid in dmap:errors.append('DECISION:DUPLICATE_IDENTITY_DISPOSITION:'+str(rid))
        dmap[rid]=x
    if set(dmap)!=set(inv) or len(rows)!=len(inv):errors.append('DECISION:INCOMPLETE_118_IDENTITY_RECONCILIATION')
    for rid,row in dmap.items():
        base=inv.get(rid)
        if base is None:errors.append('DECISION:UNKNOWN_IDENTITY:'+str(rid));continue
        state=row.get('disposition')
        if state not in IDENTITY_STATES:errors.append('DECISION:BAD_IDENTITY_DISPOSITION:'+str(rid))
        if state=='RETAINED_HISTORICAL_NONADOPTED' and base.get('group') not in ('PYAT_PC','P4R'):
            errors.append('DECISION:HISTORICAL_NONADOPTION_OVERUSED:'+str(rid))
        if base.get('group')=='PYAT_PC' and row.get('adopted_by_this_decision') is not False:errors.append('DECISION:PROSPECTIVE_ADOPTION:'+str(rid))
        if base.get('group')=='P4R' and row.get('closed_by_this_decision') is not False:errors.append('DECISION:FALSE_PROOF_CLOSURE:'+str(rid))
        if row.get('status_assertion') in ('ADOPTED','CLOSED') and base.get('group') in ('PYAT_PC','P4R'):
            errors.append('DECISION:SILENT_HISTORICAL_PROMOTION:'+str(rid))
        for k in ('design_effect','first_consumer_path','conservation_or_refusal_witness'):
            if not good(row.get(k),38):errors.append('DECISION:VACUOUS_IDENTITY_EFFECT:'+str(rid)+':'+k)
        for k,mn in (('source_meaning',20),('source_negative',20),('typed_obligation',8),('first_consumer_or_hold',8),('interpretation_grade',20)):
            if not good(row.get(k),mn):errors.append('DECISION:NO_IDENTITY_SEMANTIC_FIELD:'+str(rid)+':'+k)
        if row.get('source_meaning_sha256')!=sha((base.get('source_semantics') or '').encode()):
            errors.append('DECISION:SOURCE_MEANING_NOT_BOUND_TO_INVENTORY:'+str(rid))
        if row.get('interpretation_grade') not in ('AUTHORED_SOURCE_BOUNDED_PENDING_C','EXTERNAL_C_SOURCE_OWNER_HOLD'):
            errors.append('DECISION:FALSE_SEMANTIC_AUTHENTICATION:'+str(rid))
        guard=IDENTITY_GUARDS.get(rid)
        if guard:
            blob=(row.get('source_meaning','')+' '+row.get('source_negative','')+' '+row.get('design_effect','')+' '+row.get('conservation_or_refusal_witness','')).lower()
            for ph in guard['required']:
                if ph.lower() not in blob:errors.append('DECISION:REQUIRED_DISTINCTION_MISSING:'+rid+':'+ph)
            for ph in guard['forbidden']:
                if ph.lower() in blob:errors.append('DECISION:FORBIDDEN_DISTINCTION_REWRITE:'+rid+':'+ph)
        if row.get('evidence_grade') not in GRADES:errors.append('DECISION:BAD_IDENTITY_EVIDENCE_GRADE:'+str(rid))
        source_ref(row.get('evidence'),source_root,errors,'DECISION:IDENTITY_EVIDENCE:'+str(rid),repo,zip_path,strict=True)
        if row.get('origin_sha256')!=base.get('origin_sha256'):errors.append('DECISION:IDENTITY_ORIGIN_DRIFT:'+str(rid))
        if state in ('PRESENT_PRESERVED','FUTURE_NONPRECLUDED') and not row.get('evidence'):
            errors.append('DECISION:UNPROVED_IDENTITY_PRESERVATION:'+str(rid))
    if len({x.get('design_effect') for x in dmap.values() if isinstance(x,dict)})<100:
        errors.append('DECISION:GENERIC_IDENTITY_DESIGN_EFFECTS')
    if len({x.get('first_consumer_path') for x in dmap.values() if isinstance(x,dict)})<80:
        errors.append('DECISION:GENERIC_IDENTITY_CONSUMERS')
    if len({x.get('conservation_or_refusal_witness') for x in dmap.values() if isinstance(x,dict)})<100:
        errors.append('DECISION:GENERIC_IDENTITY_WITNESSES')

def check_frame(frame,evidence_root,source_root,repo=None,zip_path=None):
    e=[]
    if not isinstance(frame,dict) or frame.get('schema')!=SCHEMA or frame.get('stage')!='COMMON_FRAME':
        return {'status':'RED','errors':['FRAME:BAD_SCHEMA']}
    if frame.get('workflow')!='ONE_INTEGRATED_INVESTIGATION_OPTIONAL_TARGETED_DUELS':e.append('FRAME:DIVIDED_ARCHITECT_WORKFLOW_FORBIDDEN')
    if frame.get('phase')!='BEFORE_ARCHITECTURE_SELECTION':e.append('FRAME:WRONG_CHRONOLOGY')
    if frame.get('architecture_selected') is not False:e.append('FRAME:ARCHITECTURE_PRESELECTED')
    if frame.get('mandatory_rival_architecture') is not False:e.append('FRAME:RIVAL_NOT_OPTIONAL')
    if frame.get('A_B_method')!='OPTIONAL_SAME_QUESTION_SAME_EVIDENCE':e.append('FRAME:DUEL_METHOD_DISTORTED')
    if frame.get('scope') not in ('C11_QUERY_DESIGN','F1_F4_CONSUMER_DESIGN','FF_FIRST_EFFECT_DESIGN'):e.append('FRAME:INVALID_SCOPE')
    for name in ('source_cut','protected_head'):
        if not isinstance(frame.get(name),str) or not HEX40.fullmatch(frame[name]):e.append('FRAME:UNPINNED_'+name)
    for name in ('user_priority_source','first_real_consumer','currentness_gap_or_exact_verified_state','science_authority_boundary','whole_program_mission'):
        if not good(frame.get(name),35):e.append('FRAME:UNDERDEFINED_'+name)
    if frame.get('source_grades_authentic_by_local_test') is not False:e.append('FRAME:FALSE_SOURCE_AUTHORITY')
    revoked=_check_release_register(frame,evidence_root,e)
    # Exact seven typed boundary contracts from the supplied ZIP (D4B/H08).
    bc=load(evidence_root,frame.get('boundary_contract'),e,'FRAME:BOUNDARY')
    if bc is not None:
        if bc.get('schema')!='ANVIL_BOUNDARIES_R3' or len(bc.get('boundaries',[]))!=7:
            e.append('FRAME:BOUNDARY_SET_NOT_EXACT')
        supplied={b.get('id'):b for b in bc.get('boundaries',[]) if isinstance(b,dict)}
        claimed=frame.get('boundary_contracts')
        if not isinstance(claimed,list) or {b.get('id') for b in claimed if isinstance(b,dict)}!=set(BOUND_IDS):
            e.append('FRAME:T_BOUNDARIES_MISSING_OR_EXTRA')
        if isinstance(claimed,list):
            for b in claimed:
                if not isinstance(b,dict):continue
                src=supplied.get(b.get('id'),{})
                pairs=(('producer','producers'),('receiver','receivers'),('must_preserve','must_preserve'),
                       ('expected_first_effect','first_effect'),('veto','veto'),('time_class','time_class'),('owner','owners'))
                for k,sk in pairs:
                    if b.get(k)!=src.get(sk):e.append('FRAME:T_BOUNDARY_REWRITTEN:'+str(b.get('id'))+':'+k)
    # S1 identity source: a source-authenticated inventory, never an R5/R6 SPINE.
    inventory=None
    if not isinstance(frame.get('source_inventory'),dict):
        e.append('FRAME:NO_SOURCE_IDENTITY_INVENTORY')
    else:
        inventory=load(evidence_root,frame.get('source_inventory'),e,'FRAME:SOURCE_INVENTORY')
        if inventory is not None:
            res=check_inventory(inventory,source_root,repo,zip_path)
            if res['status']=='RED':e.extend('FRAME:INVENTORY:'+x for x in res['errors'])
    # A legacy R5/R6 transfer is optional historical evidence only.  It cannot
    # supply identity truth; a synthetic self-consistent spine is not a source.
    if frame.get('historical_source_spine') is not None or frame.get('historical_conservation') is not None:
        if not isinstance(frame.get('historical_conservation'),dict):
            e.append('FRAME:LEGACY_TRANSFER_WITHOUT_CONSERVATION')
        else:
            hist=load(evidence_root,frame.get('historical_conservation'),e,'FRAME:HISTORY')
            if hist is not None:check_history(hist,e)
        if inventory is None:e.append('FRAME:LEGACY_SPINE_CANNOT_SUBSTITUTE_FOR_SOURCE_INVENTORY')
    rows=frame.get('requirements')
    if not isinstance(rows,list):rows=[];e.append('FRAME:REQUIREMENTS_NOT_LIST')
    seen=set();have=set()
    for row in rows:
        if not isinstance(row,dict):e.append('FRAME:BAD_REQUIREMENT');continue
        key=row.get('id');domain=row.get('domain');have.add(domain)
        if not isinstance(key,str) or not key or key in seen:e.append('FRAME:DUPLICATE_OR_MISSING_ID')
        seen.add(key)
        if domain not in DOMAINS:e.append('FRAME:UNRECOGNIZED_DOMAIN:'+str(domain))
        if row.get('binding') not in BINDS:e.append('FRAME:BAD_BINDING:'+str(key))
        for k in ('substantive_requirement','why_needed','loss_if_missing','first_consumer','architectural_consequence','proof_or_owner_hold'):
            if not good(row.get(k),28):e.append('FRAME:VACUOUS_'+str(key)+':'+k)
        spec=REQUIREMENT_SEMANTICS.get(key)
        if spec:
            if row.get('typed_obligation')!=spec['typed_obligation']:e.append('FRAME:TYPED_OBLIGATION_MISMATCH:'+str(key))
            text=' '.join(str(row.get(k,'')) for k in ('substantive_requirement','why_needed','loss_if_missing','first_consumer','architectural_consequence','proof_or_owner_hold')).lower()
            for ph in spec['required_phrases']:
                if ph.lower() not in text:e.append('FRAME:REQUIRED_DISTINCTION_MISSING:'+str(key)+':'+ph)
            for ph in spec['forbidden_phrases']:
                if ph.lower() in text:e.append('FRAME:FORBIDDEN_OBLIGATION_REWRITE:'+str(key)+':'+ph)
            for pk in ('positive_probe','negative_probe'):
                if not good(row.get(pk),40):e.append('FRAME:NO_'+pk.upper()+':'+str(key))
        source_ref(row.get('evidence'),source_root,e,'FRAME:EVIDENCE:'+str(key),repo,zip_path,strict=True)
        ev=row.get('evidence') or {}
        if ev.get('sha256') in revoked or ev.get('zip_sha256') in revoked:e.append('FRAME:REVOKED_EVIDENCE_USED:'+str(key))
        if row.get('binding')=='EXTERNAL_OWNER_HELD' and not good(row.get('authority_owner'),10):e.append('FRAME:OWNER_NOT_NAMED:'+str(key))
    for domain in DOMAINS:
        if domain not in have:e.append('FRAME:WHOLE_MISSION_DOMAIN_MISSING:'+domain)
    if set(seen)!=set(REQUIREMENT_ROSTER) or len(rows)!=len(REQUIREMENT_ROSTER):
        e.append('FRAME:REQUIREMENT_ROSTER_DRIFT')
    for rid in REQUIREMENT_ROSTER:
        for row in rows:
            if isinstance(row,dict) and row.get('id')==rid and row.get('domain')!=REQUIREMENT_DOMAIN.get(rid):
                e.append('FRAME:REQUIREMENT_DOMAIN_MISMATCH:'+rid)
    if frame.get('duel_required') is not False:e.append('FRAME:UNNECESSARY_DUEL_REQUIRED')
    return {'status':'RED' if e else 'PASS_LOCAL_COMMON_REQUIREMENTS_SOURCE_IDENTITY_NOT_NATIVE_AUTHENTICATED','errors':sorted(set(e)),
            'requirements':len(rows),'domains':len(have&set(DOMAINS)),
            'identity_inventory_total':len(inventory.get('entries',[])) if inventory else 0}

def check_duel(duel,frame_sha,errors):
    if not isinstance(duel,dict) or duel.get('schema')!='ANVIL_R7_TARGETED_DUEL':errors.append('DECISION:DUEL_BAD_SCHEMA');return
    if duel.get('shared_frame_sha256')!=frame_sha:errors.append('DECISION:DUEL_DIFFERENT_PREMISES')
    if not good(duel.get('single_decision_question'),40):errors.append('DECISION:DUEL_NOT_SINGLE_QUESTION')
    if not good(duel.get('why_independence_is_needed'),40):errors.append('DECISION:DUEL_NO_JUSTIFICATION')
    if not good(duel.get('shared_evidence_description'),40):errors.append('DECISION:DUEL_MISSING_SHARED_EVIDENCE')
    investigators=duel.get('investigators')
    if not isinstance(investigators,list) or len(investigators)!=2 or len({i.get('id') for i in investigators if isinstance(i,dict)})!=2:
        errors.append('DECISION:DUEL_NOT_TWO_DISTINCT_PEERS');return
    if any(i.get('shared_frame_sha256')!=frame_sha or i.get('evidence_access')!='SAME_FULL_EVIDENCE' or not good(i.get('analysis'),40) for i in investigators):
        errors.append('DECISION:DUEL_DIVIDED_EVIDENCE_OR_NO_ANALYSIS')
    if any(i.get('assignment') not in ('SAME_EXACT_QUESTION_INDEPENDENT_ANALYSIS',) for i in investigators):
        errors.append('DECISION:DUEL_SPLIT_ASSIGNMENTS_FORBIDDEN')
    if not good(duel.get('integrated_adjudication'),50):errors.append('DECISION:DUEL_NOT_INTEGRATED')
    if duel.get('independence_proven_by_local_check') is not False:errors.append('DECISION:DUEL_SELF_CERTIFIES_INDEPENDENCE')

def check_decision(decision,evidence_root,source_root,repo=None,zip_path=None):
    e=[]
    if not isinstance(decision,dict) or decision.get('schema')!=SCHEMA or decision.get('stage')!='INTEGRATED_DECISION':
        return {'status':'RED','errors':['DECISION:BAD_SCHEMA']}
    frame=load(evidence_root,decision.get('common_frame'),e,'DECISION:FRAME')
    if frame is None:return {'status':'RED','errors':sorted(set(e))}
    fr=check_frame(frame,evidence_root,source_root,repo,zip_path)
    if fr['status']=='RED':e.extend('DECISION:INVALID_FRAME:'+v for v in fr['errors'])
    frozen_sha=digest(frame)
    if decision.get('frame_sha256')!=frozen_sha:e.append('DECISION:FRAME_NOT_FROZEN')
    if decision.get('first_real_consumer')!=frame.get('first_real_consumer'):e.append('DECISION:FIRST_CONSUMER_DRIFT')
    if decision.get('decision_process')!='ONE_SYNTHESIS_NO_MANDATORY_RIVAL':e.append('DECISION:WRONG_PROCESS')
    if decision.get('basis') not in ('ANALYTICAL_SOURCE_GROUNDED','EXECUTED_EXISTING_CODE','BOUNDED_DISCRIMINATOR','TARGETED_DUEL'):
        e.append('DECISION:UNKNOWN_BASIS')
    if decision.get('grade') not in ('AUTHOR_PROPOSED_PENDING_C','CONDITIONAL_DIRECTION','EXACT_HOLD'):
        e.append('DECISION:FALSE_AUTHORITY_GRADE')
    for k in ('architecture_description','entire_source_to_actor_dataflow','algorithm_and_data_structures','resource_cost_reasoning',
              'historical_function_conservation','scientific_boundary_and_nonpreclusion','strongest_surviving_objection',
              'why_selected_over_feasible_alternatives','next_actual_engineering_operation'):
        if not good(decision.get(k),55):e.append('DECISION:UNDERARGUED_'+k)
    if not good(decision.get('single_selected_strategy'),10) and decision.get('grade')!='EXACT_HOLD':
        e.append('DECISION:NO_PROPOSED_STRATEGY')
    alternatives=decision.get('alternatives_considered')
    if not isinstance(alternatives,list) or not alternatives:e.append('DECISION:ALTERNATIVES_NOT_ANALYTICALLY_CONSIDERED')
    else:
        for j,a in enumerate(alternatives):
            if not isinstance(a,dict) or not good(a.get('technical_approach'),20) or not good(a.get('why_not_selected_or_held'),45) or a.get('state') not in ('RULED_OUT_BY_REASON','VIABLE_NOT_SELECTED','UNRESOLVED_HOLD'):
                e.append('DECISION:ALTERNATIVE_UNREASONED:'+str(j))
    reversers=decision.get('choice_reversers')
    if not isinstance(reversers,list):e.append('DECISION:NO_REVERSER_ACCOUNTING')
    elif decision.get('grade')=='AUTHOR_PROPOSED_PENDING_C' and any(isinstance(r,dict) and r.get('status')=='UNRESOLVED_CHOICE_CHANGING' for r in reversers):
        e.append('DECISION:CHOICE_CHANGING_UNCERTAINTY_HIDDEN')
    if decision.get('requires_full_A_B_comparison') is not False:e.append('DECISION:COMPETITION_REQUIRED')
    if decision.get('architecture_claims_independent_acceptance') is not False:e.append('DECISION:UNAUTHORIZED_ACCEPTANCE')
    # All 118 identities: candidate-specific, non-vacuous and source-origin-bound.
    inv=load(evidence_root,frame.get('source_inventory'),e,'DECISION:INVENTORY') if isinstance(frame.get('source_inventory'),dict) else None
    check_identity_dispositions(decision,inv,source_root,e,evidence_root,repo,zip_path)
    # Typed whole-machine graph: producer / authority / time / consumer.
    check_graph(decision.get('whole_machine_graph'),e,'DECISION:GRAPH')
    # No local H1 or protected receiving.
    if decision.get('h1_received_by_local_check') is not False:e.append('DECISION:LOCAL_H1_CLAIM')
    if decision.get('protected_received_by_local_check') is not False:e.append('DECISION:LOCAL_PROTECTED_RECEIVING')
    if decision.get('codex_53_used_as_118') is True:e.append('DECISION:PARTIAL_53_CROSSWALK_SUBSTITUTES_FOR_118')
    _check_actor_world_boundary(decision,e)
    reqs=frame.get('requirements',[])
    covers=decision.get('requirement_dispositions',[])
    if not isinstance(covers,list):covers=[];e.append('DECISION:NO_REQUIREMENT_DISPOSITIONS')
    rids={r['id'] for r in reqs if isinstance(r,dict) and isinstance(r.get('id'),str)}
    if rids!=set(REQUIREMENT_ROSTER):e.append('DECISION:REQUIREMENT_ROSTER_DRIFT')
    dmap={x.get('requirement_id'):x for x in covers if isinstance(x,dict)}
    if set(dmap)!=rids or len(covers)!=len(rids):e.append('DECISION:INCOMPLETE_REQUIREMENT_RECONCILIATION')
    for row in reqs:
        if not isinstance(row,dict):continue
        rid=row.get('id');x=dmap.get(rid,{})
        state=x.get('disposition')
        if state not in DISPOS:e.append('DECISION:BAD_DISPOSITION:'+str(rid))
        if row.get('binding')=='PRESENT_HARD' and state not in ('PRESENT_PRESERVED','BLOCKING_LOSS'):
            e.append('DECISION:HARD_PRESENT_RELABELED_FUTURE:'+str(rid))
        if row.get('binding')=='EXTERNAL_OWNER_HELD' and state=='PRESENT_PRESERVED' and x.get('evidence_grade') not in ('EXECUTED_SOURCEFREE','EXECUTED_NATIVE'):
            e.append('DECISION:HELD_SCIENCE_PROMOTED:'+str(rid))
        for k in ('actual_design_effect','specific_first_consumer_path','conservation_or_refusal_witness'):
            if not good(x.get(k),38):e.append('DECISION:VACUOUS_DISPOSITION:'+str(rid)+':'+k)
        spec=REQUIREMENT_SEMANTICS.get(rid)
        if spec:
            if x.get('typed_obligation')!=spec['typed_obligation']:e.append('DECISION:TYPED_OBLIGATION_MISMATCH:'+str(rid))
            blob=' '.join(str(x.get(k,'')) for k in ('actual_design_effect','specific_first_consumer_path')).lower()
            for ph in spec['forbidden_phrases']:
                if ph.lower() in blob:e.append('DECISION:FORBIDDEN_OBLIGATION_REWRITE:'+str(rid)+':'+ph)
        if x.get('evidence_grade') not in GRADES:e.append('DECISION:BAD_EVIDENCE_GRADE:'+str(rid))
        if state in ('PRESENT_PRESERVED','FUTURE_NONPRECLUDED'):
            source_ref(x.get('evidence'),source_root,e,'DECISION:UNPROVED_PRESERVATION:'+str(rid),repo,zip_path,strict=True)
    if decision.get('grade')=='AUTHOR_PROPOSED_PENDING_C' and any(x.get('disposition')=='BLOCKING_LOSS' for x in covers if isinstance(x,dict)):
        e.append('DECISION:READY_WHILE_LOSING_REQUIRED_FUNCTION')
    if decision.get('grade')=='AUTHOR_PROPOSED_PENDING_C' and any(x.get('disposition')=='BLOCKING_LOSS' for x in decision.get('identity_dispositions',[]) if isinstance(x,dict)):
        e.append('DECISION:READY_WHILE_LOSING_IDENTITY')
    if decision.get('grade')=='AUTHOR_PROPOSED_PENDING_C' and any(x.get('disposition')=='EXACT_OWNER_HOLD' for x in covers if isinstance(x,dict)
              and any(r.get('id')==x.get('requirement_id') and r.get('binding')=='PRESENT_HARD' for r in reqs)):
        e.append('DECISION:READY_WITH_PRESENT_HARD_HOLD')
    if decision.get('basis')=='TARGETED_DUEL':
        duel=load(evidence_root,decision.get('targeted_duel'),e,'DECISION:OPTIONAL_DUEL')
        if duel is not None:check_duel(duel,frozen_sha,e)
    elif decision.get('targeted_duel') is not None:e.append('DECISION:DUEL_PRESENT_WITHOUT_GROUNDED_NEED')
    # A/B comparison is a specialist input, never a globally mandatory decision oracle.
    if decision.get('competing_implementations_mandatory') is not False:e.append('DECISION:MANDATORY_BACKEND_BAKEOFF')
    return {'status':'RED' if e else 'PASS_LOCAL_INTEGRATED_DECISION_PENDING_C','errors':sorted(set(e)),
            'covered':len(covers),'requirement_total':len(rids),
            'identity_dispositions':len(decision.get('identity_dispositions',[])) if isinstance(decision.get('identity_dispositions'),list) else 0}

def check_boundary_court(court,evidence_root,source_root,errors,admit):
    if not isinstance(court,dict) or set(court)!=set(BOUND_IDS):
        errors.append('C:INCOMPLETE_BOUNDARY_COURT');return
    for t in BOUND_IDS:
        x=court.get(t)
        if not isinstance(x,dict):errors.append('C:BAD_BOUNDARY_COURT:'+t);continue
        for k in ('positive','negative','restore'):
            if not good(x.get(k),30):errors.append('C:BOUNDARY_MISSING_'+k.upper()+':'+t)
        if x.get('grade') not in ('EXECUTED_AT_SCOPE','SOURCE_STATIC_CONSERVED','NOT_RUN'):
            errors.append('C:BOUNDARY_BAD_GRADE:'+t)
        if admit and x.get('grade')=='NOT_RUN':errors.append('C:ADMIT_WITH_UNRUN_BOUNDARY:'+t)
        if x.get('grade')!='NOT_RUN':
            source_ref(x.get('evidence'),source_root,errors,'C:BOUNDARY_EVIDENCE:'+t)
        else:
            if not good(x.get('exact_hold'),30):errors.append('C:BOUNDARY_NOT_RUN_WITHOUT_EXACT_HOLD:'+t)
        if not good(x.get('first_consumer_or_hold'),20):errors.append('C:BOUNDARY_NO_CONSUMER_OR_HOLD:'+t)
        grade=x.get('claim_grade')
        if grade not in ('SOURCE_STATIC_CONSERVED','EXACT_HOLD','ACTUAL_PROVED'):
            errors.append('C:BOUNDARY_FALSE_CLAIM_GRADE:'+t)
        if grade=='ACTUAL_PROVED' and x.get('actual_first_reader_verified') is not True:
            errors.append('C:BOUNDARY_ACTUAL_PROVED_WITHOUT_READER:'+t)
        if not good(x.get('authority_owner'),8):errors.append('C:BOUNDARY_NO_AUTHORITY_OWNER:'+t)
        fp=x.get('forbidden_promotions')
        if not isinstance(fp,list):errors.append('C:BOUNDARY_FORBIDDEN_PROMOTIONS_NOT_LIST:'+t)
        elif fp:errors.append('C:BOUNDARY_FORBIDDEN_PROMOTION_PRESENT:'+t)
        blob=' '.join(str(x.get(k,'')) for k in ('positive','negative','restore','first_consumer_or_hold')).lower()
        for ph in C_FORBIDDEN:
            if ph in blob:errors.append('C:BOUNDARY_FALSE_SCIENCE_CLAIM:'+t+':'+ph)

def check_C(packet,evidence_root,source_root,repo=None,zip_path=None):
    e=[]
    if not isinstance(packet,dict) or packet.get('schema')!=SCHEMA or packet.get('stage')!='INDEPENDENT_C':
        return {'status':'RED','errors':['C:BAD_SCHEMA']}
    decision=load(evidence_root,packet.get('integrated_decision'),e,'C:DECISION')
    if decision is not None:
        verdict=check_decision(decision,evidence_root,source_root,repo,zip_path)
        if verdict['status']=='RED':e.extend('C:DEFECTIVE_DECISION:'+x for x in verdict['errors'])
        if packet.get('integrated_decision_sha256')!=digest(decision):e.append('C:DECISION_NOT_PINNED')
        if packet.get('first_consumer')!=decision.get('first_real_consumer'):
            e.append('C:CONSUMER_CHANGED')
    for k in ('independent_reverse_walk_of_whole_frame','strongest_choice_reversing_objection',
              'scientific_and_owner_boundary','actual_first_consumer_assessment','historical_no_loss_assessment'):
        if not good(packet.get(k),60):e.append('C:INSUFFICIENT_'+k)
    admit=packet.get('verdict')=='C_CONDITIONALLY_ADMIT_DESIGN'
    check_boundary_court(packet.get('boundary_court'),evidence_root,source_root,e,admit)
    audit=packet.get('graph_audit')
    if not isinstance(audit,dict):e.append('C:NO_TYPED_GRAPH_AUDIT')
    else:
        if audit.get('producer_authority_time_consumer_checked') is not True:e.append('C:GRAPH_AUDIT_NOT_TYPED')
        holes=audit.get('holes')
        if not isinstance(holes,list):e.append('C:GRAPH_HOLES_NOT_LIST')
        elif holes:e.append('C:TYPED_GRAPH_HOLE')
        if set(audit.get('boundary_edges_checked',[]))!=set(BOUND_IDS):e.append('C:GRAPH_BOUNDARY_COVERAGE_MISSING')
    if not good(packet.get('builder_handoff_review'),60):e.append('C:NO_ACTUAL_BUILDER_HANDOFF_REVIEW')
    ctext=' '.join(str(packet.get(k,'')) for k in ('independent_reverse_walk_of_whole_frame','strongest_choice_reversing_objection','scientific_and_owner_boundary','actual_first_consumer_assessment','historical_no_loss_assessment','builder_handoff_review')).lower()
    for ph in C_FORBIDDEN:
        if ph in ctext:e.append('C:PROSE_FALSE_SCIENCE_CLAIM:'+ph)
    ta=packet.get('terminal_audit')
    if not isinstance(ta,dict):e.append('C:NO_TERMINAL_AUDIT')
    else:
        if set(ta.get('terminal_ids_present',[]))!=set(TERMINAL_IDS):e.append('C:TERMINAL_IDS_NOT_PRESENT_IN_GRAPH')
        holds=ta.get('terminal_holds')
        if not isinstance(holds,dict):e.append('C:NO_TERMINAL_HOLDS')
        else:
            for tid in ('F5','F8','N11','N12','SEAM','SOROK'):
                if not good(holds.get(tid),20):e.append('C:TERMINAL_HOLD_MISSING:'+tid)
    if admit and packet.get('actual_first_reader_verified') is not True:e.append('C:ADMIT_WITHOUT_ACTUAL_FIRST_READER')
    cards=packet.get('builder_cards')
    if not isinstance(cards,list) or len(cards)!=2 or {c.get('domain') for c in cards if isinstance(c,dict)}!={'CURRENT_FIRST_CONSUMER','FUTURE_NONPRECLUSION'}:
        e.append('C:REQUIRES_PRESENT_AND_FUTURE_BUILDER_CARDS')
    else:
        from r7_stage import check_builder
        for card in cards:
            e.extend('C:BUILDER:'+v for v in check_builder(card,source_root,evidence_root))
            _check_builder_receipt(card,evidence_root,source_root,e)
        present=next(c for c in cards if c['domain']=='CURRENT_FIRST_CONSUMER')
        if admit and present.get('grade')=='EXACT_BUILDER_HOLD':
            e.append('C:ADMIT_WITHOUT_CURRENT_BUILDER')
        if admit and present.get('grade')=='EXECUTED_FIRST_READER_PROOF':
            if (present.get('receipt') or {}).get('execution_custody') not in ('EXTERNAL_RUNNER_VERIFIED','OWNER_CUSTODY_VERIFIED'):
                e.append('C:ADMIT_ON_LOCAL_RECEIPT_WITHOUT_EXTERNAL_CUSTODY')
    if packet.get('reviewer_relationship')!='DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION':
        e.append('C:SELF_CERTIFIED_INDEPENDENCE')
    if packet.get('choice_reversing_objection_survives') is not False and admit:
        e.append('C:ACCEPTS_SURVIVING_REVERSER')
    if packet.get('verdict') not in ('C_CONDITIONALLY_ADMIT_DESIGN','C_HOLD_EXACT'):
        e.append('C:FALSE_C_GRADE')
    if packet.get('original_source_granted_by_local_check') is not False or packet.get('owner_granted_by_local_check') is not False:
        e.append('C:FALSE_AUTHORITY')
    if packet.get('local_h1_claim') is not False or packet.get('protected_received_locally') is not False:
        e.append('C:LOCAL_H1_OR_PROTECTED_CLAIM')
    if packet.get('h1_grade')=='ACCEPTED':e.append('C:LOCAL_H1_ACCEPTED')
    return {'status':'RED' if e else 'PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED','errors':sorted(set(e))}

def check(stage,packet,evidence_root,source_root=None,repo=None,zip_path=None):
    if stage=='FRAME':return check_frame(packet,evidence_root,source_root,repo,zip_path)
    if stage=='DECISION':return check_decision(packet,evidence_root,source_root,repo,zip_path)
    if stage=='C_INTEGRATED':return check_C(packet,evidence_root,source_root,repo,zip_path)
    return {'status':'RED','errors':['ACTIVE_STAGE_UNKNOWN']}

def main():
    ap=argparse.ArgumentParser(description='Active ANVIL integral workflow, NOT autonomous accreditation')
    ap.add_argument('stage',choices=['FRAME','DECISION','C_INTEGRATED'])
    ap.add_argument('packet');ap.add_argument('--evidence-root',required=True);ap.add_argument('--source-root',required=True)
    ap.add_argument('--repo',help='Git object store: REQUIRED to authenticate Git-origin families')
    ap.add_argument('--zip',help='original supplied ZIP: REQUIRED to authenticate ZIP-origin families')
    arg=ap.parse_args()
    try:out=check(arg.stage,json.loads(pathlib.Path(arg.packet).read_text()),arg.evidence_root,arg.source_root,arg.repo,arg.zip)
    except (OSError,ValueError,TypeError,KeyError) as exc:out={'status':'RED','errors':['UNHANDLED_MALFORMED_PACKET:'+repr(exc)]}
    print(json.dumps(out,indent=2));return 2 if out['status']=='RED' else 0
if __name__=='__main__':sys.exit(main())
