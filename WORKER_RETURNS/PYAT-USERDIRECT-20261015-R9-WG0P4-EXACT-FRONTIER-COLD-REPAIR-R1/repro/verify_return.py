"""Read-only return validation (or explicit --build-manifest before final commit)."""
import collections,hashlib,json,pathlib,subprocess,sys,xml.etree.ElementTree as ET
R=pathlib.Path(__file__).resolve().parents[1];ROOT=R.parents[1];PREFIX=R.relative_to(ROOT).as_posix()+'/';START='c1e88fb26f3ef757f13bad7cf901cd6529a368c8';checks=[]
def git(*a):return subprocess.check_output(['git','-C',str(ROOT),*a])
def good(name,value):
    if not value:raise AssertionError(name)
    checks.append(name)
def blob(p):return hashlib.sha1(b'blob '+str(len(p.read_bytes())).encode()+b'\0'+p.read_bytes()).hexdigest()
ret=json.load(open(R/'RETURN_MANIFEST.json'))
for name,h in [('ORIGINAL_FRONTIER.json','1af4d869c1b63046d0439ef607642f649dd13727394ae796a86399bc9e22023f'),('CONDITIONAL_FRONTIER.json','2f6826e52f46cfecf5c96f0abccd48891e3220ffe0e88f222924f66f15804abe')]:
    good('prospective_oracle:'+name,hashlib.sha256((R/name).read_bytes()).hexdigest()==h and (R/name).read_bytes()==git('show',ret['expectation_freeze_commit']+':'+PREFIX+name))
for row in json.load(open(R/'source_selector.json'))['files']:
    p=R/'pinned'/row['staging_path'];good('pinned_preimage:'+row['staging_path'],blob(p)==row['git_blob_sha1']==git('rev-parse',row['commit']+':'+row['source_path']).decode().strip() and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'])
sha=hashlib.sha256((R/'repro/wg0p4_workload.py').read_bytes()).hexdigest()
expected={'historical_p2':(29,0),'historical_p3':(36,0),'historical_j':(44,20),'historical_k_on_p3':(11,10),'ported_j':(44,0),'ported_k':(11,0),'wg0p4':(69,0)}
for name,(total,fail) in expected.items():
    record=json.load(open(R/'observations'/f'{name}.terminal.json'));tree=ET.parse(R/'observations'/f'{name}.xml')
    good('real_junit:'+name,len(tree.findall('.//testcase'))==total and len(tree.findall('.//failure'))==fail and len(tree.findall('.//error'))==len(tree.findall('.//skipped'))==0 and record['tests']==total and record['failures']==fail and record['exit']==int(fail>0))
    if name.startswith('ported_') or name=='wg0p4':good('tested_final_candidate:'+name,record['candidate_sha256']==sha)
base=json.load(open(R/'observations/baseline.json'));selector=json.load(open(R/'source_selector.json'))
for row in selector['files']:
    if row['source_path'].startswith('rawlsing_next/'):
        module=row['source_path'][:-3].replace('/','.')
        imported=next((x for x in base['imports'] if x['module']==module),None)
        if imported is None:
            good('staged_optional_not_imported:'+module,module in ['rawlsing_next.pre553_discovery_exact','rawlsing_next.pre553_runtime_composition'])
        else:
            good('actual_native_import:'+module,imported['git_blob_sha1']==row['git_blob_sha1'] and imported['file'].endswith('/pinned/'+row['staging_path']))
good('native_call_trace',collections.Counter(c['function'] for c in base['owner_calls'])=={'ingest_c11_source_release':3,'_commit_validated':3,'execute_empirical_query':3,'run':1})
a=json.load(open(R/'observations/native_cold_crash.json'));b=json.load(open(R/'observations/native_cold_resume.json'))
good('actual_cold_process_identity',a['pid']!=b['pid'] and a['exit']==23 and a['unit_count']==b['unit_count']==3 and a['manifest']==b['manifest'] and a['source_frontier_root']==b['source_frontier_root'])
good('actual_one_then_two_query_executions',collections.Counter(x['function'] for x in a['actual_calls'])=={'execute_empirical_query':1,'run':1} and collections.Counter(x['function'] for x in b['actual_calls'])=={'execute_empirical_query':2,'run':1})
good('actual_receipt_preimage_restored',len(a['receipts'])==1 and a['receipts'][0] in b['receipts'] and len(b['receipts'])==3 and all(x['manifest_hash']==a['manifest'] for x in b['receipts']) and b['summary']['coverage_state']=='FULL_MANIFEST_COVERAGE')
conditional=json.load(open(R/'observations/ordinary_conditional.json'));e=conditional['actual_consumer']
good('ordinary_positive_conditional',len(conditional['frontier'])==4 and e['denominator']==2 and {c['cell']:c['n'] for c in e['cells']}=={'yes':1,'no':1} and conditional['summary']['coverage_state']=='FULL_MANIFEST_COVERAGE')
for attack in ['grant','missing_payload','receipt_provenance','source_leaf','revoked_owner','knowledge_clock']:
    d=json.load(open(R/'observations'/f'fresh_process_attack_{attack}.json'));good('actual_fresh_process_denial:'+attack,d['accepted'] is False and d['actual_owner_calls']==[])
changed=git('diff','--name-only',START).decode().splitlines();good('owned_terrain_only',all(p.startswith(PREFIX) for p in changed))
good('startup_ancestor',subprocess.run(['git','-C',str(ROOT),'merge-base','--is-ancestor',START,'HEAD']).returncode==0)
good('review_and_authority_ceiling',ret['new_source_model_semantic_n11_n12_v3_grants'] is False and ret['status']=='RETURNED_SOURCEFREE_IMPLEMENTER_CANDIDATE__WG0L_REVIEW_REQUIRED')
files=sorted(set(git('ls-files','--cached','--others','--exclude-standard','--',PREFIX).decode().splitlines()))
good('no_runtime_keys_in_return',all('/runtime/' not in p and '__pycache__' not in p and not p.endswith('key.bin') for p in files))
for p in files:
    raw=(ROOT/p).read_bytes();good('sanitized:'+p,str(pathlib.Path.home()).encode() not in raw)
if sys.argv[1:]==['--build-manifest']:
    entries={p.removeprefix(PREFIX):{'git_blob_sha1':blob(ROOT/p),'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),'bytes':(ROOT/p).stat().st_size} for p in files if p!=PREFIX+'ARTIFACT_MANIFEST.json'}
    manifest={'schema':'WG0P4_IMMUTABLE_RETURN_FILES@1','sealed_startup':START,'expectation_freeze_commit':ret['expectation_freeze_commit'],'implementation_evidence_commit':ret['implementation_evidence_commit'],'file_root':PREFIX,'self_exclusion':'ARTIFACT_MANIFEST.json cannot bind its own future bytes. The enclosing Git commit supplies publication identity.','files':entries}
    (R/'ARTIFACT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
else:
    manifest=json.load(open(R/'ARTIFACT_MANIFEST.json'))
    for path,e in manifest['files'].items():good('artifact_manifest:'+path,blob(R/path)==e['git_blob_sha1'] and hashlib.sha256((R/path).read_bytes()).hexdigest()==e['sha256'])
print(json.dumps({'status':'RETURN_STRUCTURE_AND_GENUINE_EVIDENCE_VERIFIED','checks':len(checks),'candidate_sha256':sha,'code_commit':ret['implementation_evidence_commit'],'scientific_acceptance':'PENDING_DISTINCT_WG0L_AND_PYAT_HQ','verified':checks},indent=2))
