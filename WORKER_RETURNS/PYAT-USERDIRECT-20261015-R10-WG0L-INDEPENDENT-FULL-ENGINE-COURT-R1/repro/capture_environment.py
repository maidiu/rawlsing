from pathlib import Path
import json,sys,os,platform,hashlib,subprocess,importlib,datetime,xml.etree.ElementTree as ET
import pytest
import wg0p2_workload as w
import wg0p3_workload
R=Path(__file__).resolve().parents[1];RT=R/'runtime_root';calls=[];query_returns=[]
def trace(frame,event,arg):
 fn=frame.f_code.co_filename;name=frame.f_code.co_name
 if event=='call' and (name in ('ingest_c11_source_release','execute_empirical_query','_commit_validated') or name=='run' and fn.endswith('pre553_batch_runner.py')):
  if '/rawlsing_next/' in fn:calls.append({'function':name,'file':fn,'line':frame.f_code.co_firstlineno})
 if event=='return' and name=='execute_empirical_query' and fn.endswith('pre553_empirical_query.py') and arg is not None:
  query_returns.append({'query':frame.f_locals['query'].ref.as_dict(),'releases':[r.as_dict() for r in frame.f_locals['release_refs']],'facts':[{'ref':f.ref.as_dict(),'canonical':f.semantic_projection()} for f in arg.facts]})
 return trace
b=w.WorkloadBuilder();items=w.independent_oracle_items()
for item in items:assert b.add_item(item)=='OK'
sys.settrace(trace);rels=w.build_all_releases();p=w.build_executable_plan(b.enumerate(),rels,freeze_hash=b.freeze(),items_by_id={i.item_id:i for i in items});runner,rs=w.run_plan(p,w.make_executor(p));effects=w.consumer_effects(p,rs);sys.settrace(None)
mods=[]
for n,m in sorted(sys.modules.items()):
 if n.startswith('rawlsing_next.') or n in ('wg0p2_workload','wg0p3_workload'):
  physical=Path(m.__file__);data=physical.read_bytes();blob=subprocess.check_output(['git','hash-object',str(physical)]).decode().strip();mods.append({'module':n,'physical_file':str(physical),'git_hash_object':blob,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
sel=json.loads((R/'source_selector_phase_a.json').read_text())
for row in sel['files']:assert hashlib.sha256((RT/row['staged_path']).read_bytes()).hexdigest()==row['sha256']
for m in mods:
 rel=str(Path(m['physical_file']).relative_to(RT));assert next(r for r in sel['files'] if r['staged_path']==rel)['git_blob_sha1']==m['git_hash_object']
suites={}
for name in ('author29','author36','phase_a','wg0k_full_historical'):
 tree=ET.parse(R/f'observations/{name}.xml');suites[name]={'suites':[s.attrib for s in tree.findall('testsuite')],'terminal':json.loads((R/f'observations/{name}.terminal.json').read_text())}
report={'phase':'A','status':'PHASE_A_OWNER_ENVIRONMENT_EXECUTED_NOT_WG0P4_ADJUDICATED','WG0P4_candidate_imported':False,'no_candidate_sha_invented':True,'versions':{'python':sys.version,'pytest':pytest.__version__,'git':subprocess.check_output(['git','version']).decode().strip(),'platform':platform.platform()},'imports':mods,'all_staged_files_unchanged':len(sel['files']),'actual_owner_calls_on_historical_P2':calls,'actual_query_returns':query_returns,'actual_historical_consumer':effects,'three_validated_releases_one_repository':len({id(r.repo) for r in rels.values()})==1 and all(type(r.repo.resolve_release_exact(r.release_ref)).__name__=='C11LogicalRelease' for r in rels.values()),'batch_summary':{'state':runner.summary().batch_state,'coverage':runner.summary().coverage_state,'populated_data_execution_claim':runner.summary().populated_data_execution_claim},'historical_and_environment_test_runs':suites,'new_65_hostiles':'COLLECTED_ONLY; WG0P4 runtime adapter deliberately pending physical candidate, not skipped or passed','environment_hold':None,'candidate_verdict':None,'authority_limit':'Synthetic-only; real source issuer/model-use/all35/N11/N12/V3 remain unissued; actual historical ALLOW snapshots not external source trust.'}
(R/'02_ACTUAL_FULL_OWNER_EXECUTION_OR_PRECISE_ENV_HOLD.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
print('PHYSICAL_IMPORTS',len(mods),'OWNER_CALLS',len(calls),'STAGED_UNCHANGED',len(sel['files']))
