"""Author fixtures and freeze code/tests before ANY R3 responder execution."""
import copy,datetime,gzip,hashlib,itertools,json,pathlib,random,uuid
RET=pathlib.Path(__file__).resolve().parents[1];R2=RET/'runtime_root/rba/exec/r2'
if (RET/'CURRENT_FREEZE').exists():raise SystemExit('EXISTING_FREEZE_REFUSE_REWRITE')
base=json.loads((R2/'data/corpus.json').read_text());original_key=json.loads((R2/'data/oracle.json').read_text())
heldout=[];key={};provenance={}
for i,setting in enumerate(['municipal instrument repair depot','river ferry scheduling office']):
 for case in base:
  if case['family']!='F0' or case['k'] not in ['K3','K5','K6']:continue
  c=copy.deepcopy(case);old=c['id'];c['id']=uuid.uuid4().hex;c['family']='HELDOUT_SURFACE_'+str(i)
  c['context']=dict(setting=setting,person='Morgan',counterpart='Avery',split='predeclared_visible_heldout_not_independent')
  for e in c['history']:e['id']=uuid.uuid4().hex
  if c['hidden']:c['hidden']={k:'PRIVATE_'+uuid.uuid4().hex for k in c['hidden']}
  heldout.append(c);key[c['id']]=copy.deepcopy(original_key[old]);provenance[c['id']]=old
assert len(heldout)==28
(RET/'fixtures/heldout_cases.json').write_text(json.dumps(heldout,indent=2)+'\n')
(RET/'fixtures/heldout_key.json').write_text(json.dumps(key,indent=2)+'\n')
(RET/'fixtures/heldout_prototype_custody.json').write_text(json.dumps(dict(status='IMPLEMENTATION_VISIBLE_NOT_INDEPENDENT',semantic_template_prototypes=provenance),indent=2)+'\n')
menus={'K1':['REQUEST_FEEDBACK','SILENCE','APPEAL','OTHER_UNSCORABLE'],'K2':['REQUEST_WITH_REPAIR','REQUEST_WITH_CONDITIONAL_CAUTION','OTHER_UNSCORABLE'],'K3':['HEIGHTENED_GUARD','NEUTRAL_RESPONSE','OTHER_UNSCORABLE'],'K4':['NARROWED_CONSULT','REPEATED_QUESTION','NO_ACTION','OTHER_UNSCORABLE'],'K5':['ACCEPT_CERTIFICATE','REMAIN_DOUBTFUL','NO_STANDING_CHANGE_ACTION','OTHER_UNSCORABLE'],'K6':['POLICING_CANDIDATE','NO_SANCTION','OTHER_UNSCORABLE']}
blocks=[]
for case in base+heldout:
 menu=menus[case['k']]
 for rotation in range(len(menu)):
  for order in itertools.permutations('ABC'):
   block=uuid.uuid4().hex;public=uuid.uuid4().hex
   blocks.append([dict(id=uuid.uuid4().hex,block=block,public_response_id=public,case=case['id'],family=case['family'],k=case['k'],dataset='heldout' if case in heldout else 'original',arm=arm,execution_index=i,menu=menu[rotation:]+menu[:rotation]) for i,arm in enumerate(order)])
random.Random(304031).shuffle(blocks);rows=[r for b in blocks for r in b]
raw=json.dumps(rows,separators=(',',':')).encode();(RET/'fixtures/schedule.json.gz').write_bytes(gzip.compress(raw,mtime=0))
files=[p for folder in ['r3','tests','fixtures'] for p in (RET/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files.extend([RET/'01_PREDECLARED_R3_DESIGN.json',pathlib.Path(__file__)])
original=['freezes/v6.json','preregistration_v6.json','original_R1_preregistration.json','data/corpus.json','data/oracle.json','data/schedule.json']
f=dict(schema='BL3_R3_CANDIDATE_FREEZE@1.0.0',frozen_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),generation_only_no_responder_or_scoring_executed=True,files={str(p.relative_to(RET)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)},original_frozen_files={p:hashlib.sha256((R2/p).read_bytes()).hexdigest() for p in original},original_cases=len(base),heldout_cases=len(heldout),trials=len(rows),schedule_uncompressed_sha256=hashlib.sha256(raw).hexdigest(),oracle_independence='NOT_CERTIFIED; distinct custodian required',revision_rule='Any source/test/design/fixture repair after first execution requires append-only new freeze and prior output/source preservation')
(RET/'freezes').mkdir();out=RET/'freezes/r3-v1.json';out.write_text(json.dumps(f,indent=2)+'\n');(RET/'CURRENT_FREEZE').write_text('freezes/r3-v1.json\n');print('R3_FROZEN',hashlib.sha256(out.read_bytes()).hexdigest(),'CASES',len(base)+len(heldout),'TRIALS',len(rows))
