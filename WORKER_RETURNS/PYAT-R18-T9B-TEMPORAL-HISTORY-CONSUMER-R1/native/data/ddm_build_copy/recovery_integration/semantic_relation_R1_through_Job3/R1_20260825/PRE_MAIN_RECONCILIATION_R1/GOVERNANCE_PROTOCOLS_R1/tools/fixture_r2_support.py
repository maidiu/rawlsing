from __future__ import annotations
import copy, csv, hashlib, json, re, subprocess
from pathlib import Path

PREMAIN=Path(__file__).resolve().parents[2]; GOV=PREMAIN/'GOVERNANCE_PROTOCOLS_R1'; FX=GOV/'fixtures_r2'; CASES=FX/'cases'; PARENTS=FX/'parents'
def _live():
 return subprocess.check_output(['git','-C',str(PREMAIN),'rev-parse','--verify','refs/heads/integration/pre-main-reconciliation-r1'],text=True).strip()
def _gv():
 m=re.search(r'\*\*Ground version:\*\*\s*`([^`]+)`',(PREMAIN/'00_RAWLSING_GROUND.md').read_text(encoding='utf-8'));
 if not m: raise RuntimeError('Ground version parse failure')
 return m.group(1)
LIVE=_live(); GV=_gv()
PROHIB=['NO_NEW_PROJECT_DECISIONS','NO_AUTHORITY_REINTERPRETATION','NO_OPEN_OBLIGATION_CLOSURE','NO_SUBSTITUTION','NO_FROZEN_ADJUDICATION_REINTERPRETATION']
ALL_AR=[f'AR{i:02d}' for i in range(1,21)]
CONTRACT='GOVERNANCE_PROTOCOLS_R1/GOVERNANCE_PACKET_R2_CONTRACT.md'

def dump(path,obj): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def receipt(mode='GROUNDED_PROJECT_DECISION',domain='GENERAL_PROJECT_DECISION',states=None,obls=None,bind=None,must=None,ceiling='HQ_BANKED_AUTHORITY',rd='N022',anti=None):
 return {'grounding_receipt_id':'R2-'+mode+'-'+domain,'agent_role':'W56A regression fixture','agent_mode':mode,'canonical_project_head':LIVE,'ground_version':GV,'task_scope':domain,'relevant_state_ids':states or [],'relevant_obligation_ids':obls or [],'binding_authority_surfaces_read':bind or ['00_RAWLSING_GROUND.md','CENTRAL_PROJECT_STATE_R1/00_STATE_NOW.md'],'must_factor_surfaces_read':must or ['CENTRAL_PROJECT_STATE_R1/PROJECT_STATE.tsv'],'anti_resurrection_constraints':anti or ['AR04'],'authority_ceiling':ceiling,'may_decide':['DECIDE_AT_DECLARED_GRAIN'] if mode=='GROUNDED_PROJECT_DECISION' else [],'may_not_decide':PROHIB[:] if mode=='GROUNDED_BOUNDED_EXECUTION' else [],'dependencies':[],'required_return_destination':rd,'central_state_head_match':'PASS','grounding_complete_for_declared_scope':'PASS'}

def packet(g,effect='PROJECT_ADOPTION',domain='GENERAL_PROJECT_DECISION',reint='CANONICALLY_INHERITED',local='PASS',touched=None,disps=None,scope_ex=None,successors=None,paths=None,auth_effects=None,closure=None,bp=None,authority_obtained=None):
 touched=touched or []; disps=disps or {}; successors=successors or []; paths=paths or []; auth_effects=auth_effects or []; closure=closure or []; authority_obtained=authority_obtained or []
 w={'work_unit_id':'W56A-FIXTURE','canonical_launch_head':LIVE,'agent_mode':g['agent_mode'],'local_status':local,'result_ref':CONTRACT,'accomplished':['fixture execution'],'not_accomplished':[],'remaining_open':[],'touched_obligation_dispositions':[{'obligation_id':x,'disposition':disps[x]} for x in touched],'new_obligations':[],'spawned_successors':successors,'return_to_ids':[g['required_return_destination']]+[x['return_to'] for x in paths if x.get('return_to')!=g['required_return_destination']],'authority_obtained':authority_obtained,'authority_not_obtained':[],'central_state_changed':[],'central_state_unchanged':['project authority outside declared grain'],'reintegration_status':reint,'required_next_reintegration_action':'Return to governing authority'}
 parent_states=sorted({OBL_PARENT[x] for x in touched if x in OBL_PARENT})
 u={'canonical_project_head':LIVE,'ground_version':GV,'grounding_receipt_id':g['grounding_receipt_id'],'authority_ceiling':g['authority_ceiling'],'return_destination':g['required_return_destination'],'touched_state_ids':parent_states,'touched_obligation_ids':touched,'obligation_dispositions':[{'obligation_id':x,'status':disps[x]} for x in touched],'new_obligations':[],'successor_return_paths':paths,'reintegration_status':reint,'anti_resurrection_acknowledged':True}
 return {'packet_version':'RAWLSING_GOVERNANCE_PACKET_R2','requested_effect':effect,'decision_domain':domain,'grounding_receipt':g,'work_return':w,'central_state_update':u,'scope_exclusions':scope_ex or [],'bounded_parent':bp or {},'authority_effects':auth_effects,'closure_claims':closure}

OBL_PARENT={'OBL001':'N012','OBL005':'N028','OBL006':'N028','OBL007':'N016','OBL008':'N024','OBL009':'N027','OBL010':'N012','OBL013':'N025','OBL017':'N025','OBL018':'N025','OBL020':'N028','OBL024':'N010','OBL026':'N036','OBL027':'N004','OBL028':'N004','OBL029':'N006','OBL030':'N006','OBL031':'N006','OBL035':'N010','OBL036':'N010','OBL037':'N012','OBL040':'N028','OBL041':'N028','OBL042':'N028','OBL043':'N028','OBL045':'N026'}

def ex(*ids): return [{'obligation_id':x,'reason':'Explicitly outside fixture decision grain; preserved open','preserved_open':True} for x in ids]

def physical(valid=True):
 bind=['00_RAWLSING_GROUND.md','CENTRAL_PROJECT_STATE_R1/00_STATE_NOW.md','CANONICAL_GOVERNANCE_R1/AUTHORITY_LEVELS.tsv']; must=['PROJECT_INHERITANCE_R1/CAMPAIGNS/N004_DVA_DEVELOPMENTAL_ARCHITECTURE','PROJECT_INHERITANCE_R1/CAMPAIGNS/N006_TRII_EMPIRICAL_SUBSTRATE','PROJECT_INHERITANCE_R1/CAMPAIGNS/N010_CHETIRI_SOURCE_BACKED_ARCHITECTURE','PROJECT_INHERITANCE_R1/CAMPAIGNS/N012_PREV3_NO_WINNER_ARCHITECTURE']
 if not valid: must.remove('PROJECT_INHERITANCE_R1/CAMPAIGNS/N010_CHETIRI_SOURCE_BACKED_ARCHITECTURE')
 g=receipt(domain='PHYSICAL_ARCHITECTURE',states=['N004','N006','N010','N012','S037'],obls=['OBL001','OBL037'],bind=bind,must=must,rd='N012')
 return packet(g,domain='PHYSICAL_ARCHITECTURE',scope_ex=ex('OBL027','OBL028','OBL029','OBL030','OBL031','OBL024','OBL035','OBL036','OBL010'))

def ff(valid=True):
 must=['PROJECT_INHERITANCE_R1/FIELD_FORGE_REINDUCTION_BRIDGE.md','PROJECT_INHERITANCE_R1/CAMPAIGNS/N028_FIELD_FORGE'];
 if not valid: must=must[1:]
 g=receipt(domain='FIELD_FORGE',states=['N028','N016','N026'],obls=['OBL005','OBL006','OBL040','OBL041','OBL042','OBL043'],bind=['00_RAWLSING_GROUND.md','CANONICAL_GOVERNANCE_R1/CURRENT_AUTHORITY_INDEX.tsv','CANONICAL_GOVERNANCE_R1/CURRENT_SEMANTIC_LAW_INDEX.tsv'],must=must,rd='N028')
 return packet(g,domain='FIELD_FORGE',scope_ex=ex('OBL020','OBL007','OBL045'))

def j01b(valid=True):
 must=['PROJECT_INHERITANCE_R1/CAMPAIGNS/N025_SOURCE_PREPARATION_CURRENT_ADMISSION','PROJECT_INHERITANCE_R1/CAMPAIGNS/N026_CURRENT_JOINT_C06_ROUTING','PROJECT_INHERITANCE_R1/CAMPAIGNS/N027_J01B_CURRENT_JOINT_AUTHORITY'];
 if not valid: must.remove('PROJECT_INHERITANCE_R1/CAMPAIGNS/N026_CURRENT_JOINT_C06_ROUTING')
 g=receipt(domain='J01B',states=['N025','N026','N027'],obls=['OBL009'],bind=['00_RAWLSING_GROUND.md','CANONICAL_GOVERNANCE_R1/DELEGATED_AUTHORITY_INDEX.tsv'],must=must,rd='N027')
 return packet(g,domain='J01B',scope_ex=ex('OBL013','OBL017','OBL018','OBL045'))

def dva(valid=True):
 states=['N004','S037'] if valid else ['N004']; bind=['00_RAWLSING_GROUND.md','00_CANONICAL_ENTRYPOINT.md'] if valid else ['00_RAWLSING_GROUND.md']
 g=receipt(domain='DVA_IMPLEMENTATION',states=states,obls=['OBL027','OBL028'],bind=bind,must=['PROJECT_INHERITANCE_R1/CAMPAIGNS/N004_DVA_DEVELOPMENTAL_ARCHITECTURE'],rd='N004')
 return packet(g,domain='DVA_IMPLEMENTATION')

def persistence(valid=True):
 states=['N006','N010','N012'] if valid else ['N006','N012']; must=['PROJECT_INHERITANCE_R1/CAMPAIGNS/N006_TRII_EMPIRICAL_SUBSTRATE','PROJECT_INHERITANCE_R1/CAMPAIGNS/N010_CHETIRI_SOURCE_BACKED_ARCHITECTURE','PROJECT_INHERITANCE_R1/CAMPAIGNS/N012_PREV3_NO_WINNER_ARCHITECTURE'];
 if not valid: must.remove('PROJECT_INHERITANCE_R1/CAMPAIGNS/N010_CHETIRI_SOURCE_BACKED_ARCHITECTURE')
 g=receipt(domain='PHYSICAL_PERSISTENCE',states=states,obls=['OBL001','OBL037'],bind=['00_RAWLSING_GROUND.md','CANONICAL_GOVERNANCE_R1/AUTHORITY_LEVELS.tsv'],must=must,rd='N012')
 exclusions=ex('OBL029','OBL030','OBL031','OBL024','OBL035','OBL036','OBL010')
 return packet(g,domain='PHYSICAL_PERSISTENCE',scope_ex=exclusions)

def parent_files():
 p=receipt(states=['N017'],obls=[],rd='N022'); p['grounding_receipt_id']='PARENT-GENERAL-R2'; dump(PARENTS/'PARENT_GENERAL.json',p)
 pd=receipt(domain='DVA_IMPLEMENTATION',states=['N004','S037'],obls=['OBL027','OBL028'],bind=['00_RAWLSING_GROUND.md','00_CANONICAL_ENTRYPOINT.md'],must=['PROJECT_INHERITANCE_R1/CAMPAIGNS/N004_DVA_DEVELOPMENTAL_ARCHITECTURE'],rd='N004'); pd['grounding_receipt_id']='PARENT-DVA-R2'; dump(PARENTS/'PARENT_DVA.json',pd)
 ps=copy.deepcopy(p); ps['grounding_receipt_id']='PARENT-STALE-R2'; ps['canonical_project_head']='0'*40; dump(PARENTS/'PARENT_STALE.json',ps)
 return p,pd,ps

def bounded(parent_name='PARENT_GENERAL.json',domain='GENERAL_PROJECT_DECISION',states=None,obls=None,scope_ex=None,rd='N022',touched=None,disps=None,reint='LOCAL_COMPLETE_UNRECONCILED'):
 parent=json.loads((PARENTS/parent_name).read_text()); g=receipt(mode='GROUNDED_BOUNDED_EXECUTION',domain=domain,states=states if states is not None else parent['relevant_state_ids'],obls=obls if obls is not None else parent['relevant_obligation_ids'],bind=parent['binding_authority_surfaces_read'],must=parent['must_factor_surfaces_read'],ceiling='WORKER_LOCAL_RESULT',rd=rd); g['grounding_receipt_id']='CHILD-'+parent['grounding_receipt_id']
 bp={'parent_receipt_path':f'GOVERNANCE_PROTOCOLS_R1/fixtures_r2/parents/{parent_name}','parent_receipt_sha256':sha(PARENTS/parent_name),'parent_grounding_receipt_id':parent['grounding_receipt_id'],'governing_adjudication_ref':CONTRACT,'forbidden_reinterpretation':PROHIB[:]}
 return packet(g,effect='BOUNDED_EXECUTION_RETURN',domain=domain,reint=reint,touched=touched,disps=disps,scope_ex=scope_ex,bp=bp)

def closure_packet(reint='CANONICALLY_INHERITED'):
 g=receipt(domain='GENERAL_PROJECT_DECISION',states=['N012'],obls=['OBL010'],ceiling='PROJECT_CURRENT_AUTHORITY',rd='N012')
 cl=[{'obligation_id':'OBL010','closure_authority':'VOZHD/HQ architecture authority','supporting_evidence_ref':CONTRACT,'closure_condition_addressed':'Competent exact architecture-selection ruling supplied for fixture'}]
 return packet(g,effect='PROJECT_CLOSURE_AT_GRAIN',domain='GENERAL_PROJECT_DECISION',reint=reint,local='PROJECT_CLOSED',touched=['OBL010'],disps={'OBL010':'CLOSED'},scope_ex=ex('OBL001','OBL037'),closure=cl)

def resurrection(target,effect,gates):
 g=receipt(states=['N017'],anti=gates or ['AR04'])
 ae=[{'target_id':target,'requested_effect':effect,'supporting_authority_ref':CONTRACT,'applicable_gate_ids':gates}]
 return packet(g,auth_effects=ae,authority_obtained=[f'{target}:{effect}'])
