#!/usr/bin/env python3
import csv,json,sys,collections
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
def rc(n):
 with open(root/n,encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def j(s):
 try:return json.loads(s)
 except:return []
c=rc('O12_JOB3_CANDIDATE_DENOMINATOR_T15_SUCCESSOR_R3.csv');e=rc('O12_EXISTING_GOVERNED_RELATION_TOPOLOGY_R3.csv');cov=rc('O12_RULE_WAVE_COVERAGE_R3.csv');aj=rc('O12_GOVERNED_POSITIVE_SUBSET_ANTI_JOIN_R3.csv')
errs=[]
want={'S14-T01':544,'S14-T02':29,'S14-T05':59,'S14-T06':4,'S14-T11':477,'S14-T12':72,'S14-T13':65,'S14-T15':14}
if len(c)!=1264:errs.append('candidate_count')
if len({r['candidate_id'] for r in c})!=1264:errs.append('candidate_id_unique')
if dict(collections.Counter(r['rule_id'] for r in c))!=want:errs.append('candidate_histogram')
if len(e)!=638:errs.append('existing_count')
if len(cov)!=525:errs.append('coverage_count')
if len(aj)!=86 or collections.Counter(r['rule_id'] for r in aj)!=collections.Counter({'S14-T01':84,'S14-T02':2}):errs.append('subset_antijoin_count')
# prove no final candidate remains subset of governed same-rule/source-wave positive
idx=collections.defaultdict(list)
for x in e:idx[(x['source_family'],x['wave'],x['rule_id'])].append(set(j(x['member_implementation_ids_json'])))
for r in c:
 s=set(j(r['implementation_ids']))
 if any(s.issubset(ps) for ps in idx[(r['source_family'],str(r['active_wave']),r['rule_id'])]):errs.append('candidate_covered_by_governed_positive:'+r['candidate_id']);break
for n in ['O12_COMPLETENESS_VALIDATION_R3.json','O12_HOSTILE_QA_R3.json','INDEPENDENT_EXPECTED_UNIVERSE_VALIDATION_R3.json','VALIDATION_R3.json']:
 if json.load(open(root/n))['status']!='PASS':errs.append(n)
print(json.dumps({'status':'PASS' if not errs else 'FAIL','errors':errs,'candidate_count':len(c),'existing_count':len(e),'visible_topology':len(c)+len(e),'candidate_by_rule':dict(collections.Counter(r['rule_id'] for r in c))},indent=2,sort_keys=True))
sys.exit(1 if errs else 0)
