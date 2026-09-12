#!/usr/bin/env python3
"""Validate the audit packet only. Does not execute or certify Rawlsing runtime."""
from pathlib import Path
import hashlib,json,re,sys
from collections import deque
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/name).read_text())
def require(ok,msg):
 if not ok:raise AssertionError(msg)
def fields(rows,names,label):
 for r in rows:require(set(names)<=set(r),(label,r.get('id') or r.get('gap_id') or r.get('commission_id'),set(names)-set(r)))
c=read('machine/capability_register.json');g=read('machine/gap_register.json');e=read('machine/dependency_edges.json');w=read('machine/proposed_commissions.json');a=read('machine/authority_dispositions.json');gates=read('machine/gates.json');sources=read('evidence/source_index.json');claims=read('evidence/claim_index.json')
fields(c,'id name semantic_owner authority_status implementation_status real_data_status replay_status qualification_status upstream_composition downstream_composition breadth maturity evidence_refs'.split(),'capabilities')
fields(g,'gap_id title type severity owner dependencies blocked_successors parallel_with requires_authority requires_code requires_real_data requires_hostile_review pass_condition evidence_refs'.split(),'gaps')
fields(e,'from to dependency_type reason required_identity_or_evidence'.split(),'edges')
fields(w,'commission_id role exact_grain ready_now blocking_gate dependencies parallel_with pass_condition blocker_return successor_wake'.split(),'commissions')
fields(a,'identity description status semantic_scope current_authority historical_value quarantined reason required_future_disposition'.split(),'dispositions')
require(len(c)==34 and len(g)==34,'Expected 34 distinct capability and material gap rows')
require(sum(x['ready_now'] for x in w)==8,'Expected exactly eight ready-now bounded commissions')
require(sum(x['severity']=='STRICT_BLOCKER' for x in g)==7,'Expected seven scoped strict completion blockers')
for rows,key in [(c,'id'),(g,'gap_id'),(w,'commission_id'),(gates,'gate_id'),(sources,'evidence_id'),(claims,'claim_id')]:require(len({x[key] for x in rows})==len(rows),'Duplicate '+key)
sourceids={s['evidence_id'] for s in sources};gapids={x['gap_id'] for x in g};workerids={x['commission_id'] for x in w};gateids={x['gate_id'] for x in gates};nodes=gapids|workerids|gateids
for x in c:
 require(x['maturity'] in list('ABCDEFGH'),'Invalid maturity');require(x['maturity'] not in ['G','H'],'Unsupported completion-grade claim')
 require(x['breadth'] in ['NONE','TOY','CANARY_ONLY','NARROW_REAL','MULTI_DOMAIN_REAL','BROAD_BUT_INCOMPLETE','PRODUCTION_SUFFICIENT'],'Invalid breadth')
for x in c+g+a+claims:require(set(x['evidence_refs'])<=sourceids,'Unknown evidence ref')
for x in g:
 require(set(x['dependencies']+x['blocked_successors']+x['parallel_with'])<=gapids,'Unknown gap reference')
 for d in x['dependencies']:require(any(y['from']==d and y['to']==x['gap_id'] for y in e),'Missing gap edge')
for x in w:
 require(set(x['read_set'])<=sourceids,'Unknown commission read set')
 require(set(x['target_gap_ids'])<=gapids,'Unknown target gap')
 require(set(x['parallel_with'])<=workerids,'Unknown parallel commission')
 require(set(x['blocking_gate']+x['successor_wake'])<=gateids,'Unknown commission gate')
 if x['ready_now']:require(not x['blocking_gate'] and not x['dependencies'],'Ready-now commission has unresolved gate')
 else:require(bool(x['blocking_gate']),'Waiting commission lacks a named gate')
 require((ROOT/'commissions'/(x['commission_id']+'.md')).exists(),'Missing dispatch card')
require(set().union(*(set(x['target_gap_ids']) for x in w))==gapids,'Unowned/unaddressable gap missing commission target')
types={'STRICT_DEPENDENCY','SEMANTIC_DEPENDENCY','IDENTITY_DEPENDENCY','EVIDENCE_DEPENDENCY','QUALIFICATION_DEPENDENCY','INTEGRATION_DEPENDENCY'}
indegree={n:0 for n in nodes};out={n:[] for n in nodes};seen=set()
for x in e:
 require(x['from'] in nodes and x['to'] in nodes,'Unknown edge node');require(x['dependency_type'] in types,'Invalid dependency type')
 require(x['reason'] and x['required_identity_or_evidence'],'Empty dependency rationale')
 pair=(x['from'],x['to']);require(pair not in seen,'Duplicate edge');seen.add(pair)
 indegree[x['to']]+=1;out[x['from']].append(x['to'])
q=deque(n for n in nodes if not indegree[n]);order=[]
while q:
 n=q.popleft();order.append(n)
 for v in out[n]:
  indegree[v]-=1
  if not indegree[v]:q.append(v)
require(len(order)==len(nodes),'Dependency graph has a cycle')
# Ensure there is no fake all-producer gate before V1.
require({x['from'] for x in e if x['to']=='GATE-V1'}=={'ASTRA-W02'},'V1 artificially serialized behind unrelated producers')
for s in sources:
 if s.get('url'):
  require(s.get('commit') and len(s['commit'])==40,'Unpinned repository source')
  require(s.get('blob') and len(s['blob'])==40,'Missing exact blob identity')
 else:
  p=ROOT/s['source_path'];require(p.exists(),'Missing local evidence')
  require(hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'],'Evidence hash mismatch '+s['evidence_id'])
# Verify mirrors expose every operational row, edge and disputed identity in Markdown.
capdoc=(ROOT/'03_CAPABILITY_MATURITY_MATRIX.md').read_text();gapdoc=(ROOT/'05_GAP_AND_BLOCKER_REGISTER.md').read_text();edgedoc=(ROOT/'06_DEPENDENCY_AND_PARALLELISM_DAG.md').read_text();adoc=(ROOT/'04_PERSON_CREATION_LEAKAGE_COURT.md').read_text();claimdoc=(ROOT/'12_EVIDENCE_AND_AUTHORITY_INDEX.md').read_text()
for x in c:require(x['id'] in capdoc and x['name'] in capdoc,'Capability mirror missing')
for x in g:require(x['gap_id'] in gapdoc and x['pass_condition'] in gapdoc,'Gap mirror missing')
for x in e:require(x['from'] in edgedoc and x['to'] in edgedoc and x['required_identity_or_evidence'].replace('|',' / ') in edgedoc,'Edge mirror missing')
for x in a:require(x['identity'] in adoc and x['required_future_disposition'] in adoc,'Authority mirror missing')
for x in claims:require(x['claim_id'] in claimdoc,'Claim mirror missing')
required=['00_EXECUTIVE_VERDICT.md','01_PREV3_CONSTITUTIONAL_BOUNDARY.md','02_CURRENT_SYSTEM_MAP.md','03_CAPABILITY_MATURITY_MATRIX.md','04_PERSON_CREATION_LEAKAGE_COURT.md','05_GAP_AND_BLOCKER_REGISTER.md','06_DEPENDENCY_AND_PARALLELISM_DAG.md','07_TARGET_COMPLETION_ARCHITECTURE.md','08_PHASED_ATTACK_PLAN.md','09_FIRST_WAVE_COMMISSIONS.md','10_COMPLETION_AND_FREEZE_CRITERIA.md','11_FINAL_SCHEMATIC.md','12_EVIDENCE_AND_AUTHORITY_INDEX.md','99_RETURN_TO_VOZHD_HQ.md']
for n in required:require((ROOT/n).is_file(),'Missing required document '+n)
# Markdown links resolve within packet or to immutable external evidence.
for p in ROOT.rglob('*.md'):
 if p.name=='ORIGINAL_AUDIT_REPORT.md' or p.name.startswith('user-'):continue
 s=p.read_text();require(s.count('```')%2==0,'Unclosed fence '+str(p))
 for dest in re.findall(r'\]\(([^)]+)\)',s):
  if dest.startswith(('http:','https:','#')):continue
  require((p.parent/dest.split('#')[0]).exists(),'Broken local link '+str(p)+' -> '+dest)
for p in ROOT.rglob('*.json'):
 if p.name=='packet_manifest.json':continue
 json.loads(p.read_text())
manifest=read('packet_manifest.json')
for item in manifest['files']:
 p=ROOT/item['path'];require(p.is_file(),'Manifest path missing')
 require(hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],'Manifest hash mismatch '+item['path'])
actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='packet_manifest.json'}
require(actual=={i['path'] for i in manifest['files']},'Manifest file set differs')
print(json.dumps({'result':'PASS_PACKET_CONSISTENCY_ONLY','capabilities':len(c),'gaps':len(g),'scoped_strict_blockers':7,'ready_now_commissions':8,'waiting_commissions':len(w)-8,'dependency_edges':len(e),'dag_nodes':len(nodes),'evidence_sources':len(sources),'typed_claims':len(claims),'manifest_files':len(manifest['files']),'runtime_reexecution':False},indent=2))
