"""Scoped source/API custody adjudication, not duplication of Pyat review courts."""
from stage import R,git,blob
from pathlib import Path
import json,hashlib,subprocess,sys,os,xml.etree.ElementTree as E,shutil,importlib.util
out=R/'evidence/pyat';out.mkdir(parents=True,exist_ok=True);rows=[]
def fetch(sha,path,alias):
 b=git('show',sha+':'+path);assert blob(b)==git('rev-parse',sha+':'+path).decode().strip();p=R/'staging/pyat_evidence'/alias;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);rows.append(dict(commit=sha,path=path,local=str(p.relative_to(R)),blob_sha1=blob(b),sha256=hashlib.sha256(b).hexdigest()));return p,b
r22='ecb5de4f5f90015e5f10b9f3b12e76ee145fee58'
fetch(r22,'PYAT_CONTROL_ROOM/PYAT_HQ_ACCESSION_CANDIDATE_20261016_R1/07_R22_SIX_WORKER_FANIN_AND_SCIENTIFIC_DECISIONS_20261016.md','R22.md')
primary={
'E06I':('b3ebd8a0ce49ba2b96e1adae5cff3f65a90b17a1','WORKER_RETURNS/PYAT-R18-E06I-INDEPENDENT-FULL-BRIDGE-R1',['00_INDEPENDENT_VERDICT.md','04_METHOD_RIGHTS_HQ_NEXT_EDGE.md','observations/author40_regression.xml','observations/e06i_independent_court.xml','observations/source_closure_proof.json','02_EXECUTED_ORIGINAL_OWNER_AND_BOTH_CLIENTS.json']),
'GF1I':('c6a55f0dd5b327c40d64f96e0705ab5485559e90','WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1',['00_INDEPENDENT_SCIENTIFIC_VERDICT.md','04_FIELD_FORGE_SEMANTIC_OWNER_SCOPE_AND_HQ_NEXT_EDGE.md','junit/gf1i_independent.xml','02_ACTUAL_NATIVE_RELATION_CONSUMER_AND_INTERVENTIONS.json','logs/gf1i_pytest_stdout.txt'])}
summaries=[]
for label,(sha,prefix,names) in primary.items():
 for name in names:
  p,b=fetch(sha,prefix+'/'+name,label+'/'+name)
  if name.endswith('.xml'):
   root=E.fromstring(b);cases=list(root.iter('testcase'));summaries.append(dict(source=label,commit=sha,path=prefix+'/'+name,tests=len(cases),failures=sum(x.find('failure') is not None for x in cases),errors=sum(x.find('error') is not None for x in cases),fresh_C0I_execution=False))
# Exact missing aliases are source-manifested, not orphan modules.
s='f524f60781e2e7e72278d04d6377fb1da877698a';p='WORKER_RETURNS/PYAT-USERDIRECT-20261016-R14-E05S-INDEPENDENT-SELECTED-WORLD-R1/source_manifest.json';_,b=fetch(s,p,'E05S_source_manifest.json');manifest=json.loads(b)
aliases=[]
for x in manifest:
 if x['local'] in ['e05_n9_selected_world_adapter.py','rawlsing_next/pre553_hq297_n9c_two_field_reader.py']:
  pp,bb=fetch(x['commit'],x['path'],'alias_source/'+x['local']);assert blob(bb)==x['git_blob'];aliases.append(dict(alias=x['local'],**rows[-1]))
t='79cb8244a5291218bde17142b93fc2419eade396';p='WORKER_RETURNS/PYAT-USERDIRECT-20261016-R15-E04T-NATIVE-CURRENT-GRANT-REPAIR-R1/product/empirical.py';pp,bb=fetch(t,p,'alias_source/e04t_empirical.py');aliases.append(dict(alias='runtime/owners/e04t_empirical.py',**rows[-1]));assert bb==(R/'staging/runtime/product/empirical.py').read_bytes()
# Confirm C0P frozen earlier bridge is byte-identical to final E06 bridge.
e06='f9c52113de38caececc450f0e54c980f64ed3981';ep='WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-E06-E04E05-NATIVE-BRIDGE-R1'
bridge,b=fetch(e06,ep+'/bridge.py','E06_final_bridge.py');assert b==(R/'staging/oracles/pyat_e06/bridge.py').read_bytes()
fetch(e06,ep+'/repro/stage_sources.py','E06_stage_sources.py')
# Reproduce only the C0P closure import failure, with explicit environment.
probe="import importlib.util,sys;sys.path.insert(0,sys.argv[1]);s=importlib.util.spec_from_file_location('e06_exact',sys.argv[2]);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)"
cmd=[sys.executable,'-c',probe,str(R/'staging/runtime'),str(bridge)];p=subprocess.run(cmd,cwd=R,env=dict(os.environ,PYTHONPATH=str(R/'staging/runtime'),PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
(out/'E06_C0P_closure_import.stdout.log').write_text(p.stdout+p.stderr);assert p.returncode!=0 and "No module named 'e04t_empirical'" in p.stderr
# GF1: check complete candidate tree for absent named consumer; probe that exact missing name.
gf='9f4a23cef1482e0a81afb1e7a65df90879931465';gp='WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1'
paths=git('ls-tree','-r','--full-tree','--name-only',gf).decode().splitlines();missing=[x for x in paths if 'gf1_pair_support_consumer' in x];assert not missing
for name in ['court/repro/gf1_native.py','court/repro/test_gf1_generic_pair.py']:
 fetch(gf,gp+'/'+name,'GF1_original/'+name)
code="import gf1_pair_support_consumer";q=subprocess.run([sys.executable,'-I','-c',code],cwd=R,capture_output=True,text=True);(out/'GF1_named_consumer_import.stdout.log').write_text(q.stdout+q.stderr);assert q.returncode!=0 and 'gf1_pair_support_consumer' in q.stderr
# E03 actual Git preimage proof, and actual timeout availability (not an empty search).
e03='0e0ed50dbce2dd1434d3a3c84b937b9a956adba9';path='rawlsing_next/pre553_n9_n10w_progressive_candidate.py';b=git('show',e03+':'+path);assert blob(b)=='84d404147547767be8ecd4b6e1541f5fa3a8c8a2'
result=dict(schema='C0I_PYAT_SOURCE_API_AUDIT@1',source_files=rows,upstream_junit=summaries,E06=dict(c0p_closure_import_exit=p.returncode,first_missing='e04t_empirical',bridge_matches_final_candidate=True,source_aliases_reachable=aliases,correction='Absent from the C0P 29-module staging, not absent from exact reachable Pyat source/manifests',r22='R22-E06I-05 ACCEPT_SOURCEFREE_NONINSTALLING_JOINED_BRIDGE_METHOD_ONLY',independently_accepted_by_Pyat=True,installed_N9=False,C0I_did_not_rerun_402_module_or_88_case_E06I_mission=True,residuals=['same-ref integrity ValueError labeling','warm/cold refusal label variation','ambient current_runtime_authorities fallback untested by E06I','nondurable synthetic revocation']),GF1=dict(candidate=gf,full_tree_paths_examined=len(paths),named_consumer_paths=[],actual_isolated_missing_import_exit=q.returncode,full_44_collection_reproduced_by_C0I=False,why_not='Do not restage/repeat Pyat full74 closure assignment; exact missing artifact and references independently checked; GF1I full collection failure retained as external evidence',r22='R22-GF1I-06 CONFIRM_RED_MISSING_DOWNSTREAM_CONSUMER_ARTIFACT',consumer_reconstructed=False,method_accepted=False,relation19_pass_upstream_only=True,oracle_correction='GF1I changed expected changed-relations2 to3 after observation; not immutable precommit proof'),E03=dict(commit=e03,path=path,blob_sha1=blob(b),reachable_commit_object=True,timeout_executable=shutil.which('timeout'),false_negative_correction='A missing shell timeout tool is ENV error, not a negative Git reachability result'),XSP='R22 standalone19 method is interface expectation; no native seam; not duplicated',sourcefree_only=True)
(out/'source_api_audit.json').write_text(json.dumps(result,indent=2)+'\n');print('E06 closure discrepancy reproduced; three exact alias source preimages proved; R22 primary evidence audited; GF1 absent consumer confirmed')
