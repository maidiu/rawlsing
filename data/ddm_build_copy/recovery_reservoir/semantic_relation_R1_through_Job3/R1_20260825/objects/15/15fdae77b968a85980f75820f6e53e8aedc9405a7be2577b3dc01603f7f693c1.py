#!/usr/bin/env python3
import csv,json,sys,os
from collections import Counter
root=os.path.dirname(os.path.abspath(__file__))
def rows(name):
    with open(os.path.join(root,name),newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
checks=[]
def ck(name,ok,detail=''):
    checks.append({'check':name,'pass':bool(ok),'detail':str(detail)})
pos=rows('CENTRAL_T15_POSITIVE_RELATION_AUTHORITY_R1.csv')
t06=rows('CENTRAL_STRICT_T06_SOURCE_FIRST_AUTHORITY_R1.csv')
wave=rows('T15_35WAVE_COMPLETENESS_ATTESTATION_R1.csv')
fb=rows('T06_T15_BOUNDARY_ADJUDICATION_R1.csv')
cov=rows('MERGED_T15_SOURCE_COVERAGE_DEFECTS_R1.csv')
ck('positive_188',len(pos)==188,len(pos))
ck('strict_t06_64',len(t06)==64,len(t06))
ck('waves_35',len(wave)==35,len(wave))
ck('implementation_denominator_18276',sum(int(float(r['implementation_denominator'])) for r in wave)==18276,sum(int(float(r['implementation_denominator'])) for r in wave))
ck('boundary_86',len(fb)==86,len(fb))
post=Counter(r['final_central_posture'] for r in fb)
ck('boundary_64_21_1',post==Counter({'RETAIN_STRICT_T06':64,'MIGRATE_TO_T15':21,'REJECT_BOTH':1}),dict(post))
ids=[r['central_relation_id'] for r in pos]
ck('central_t15_ids_unique',len(ids)==len(set(ids)),len(set(ids)))
allowed={'DIRECT_ENACTMENT','RIGHT_OR_PERMISSION_EXERCISE','PRACTICAL_VIOLATION','INSTITUTIONAL_OR_SOCIAL_REALIZATION','INSTRUMENTAL_ENACTMENT'}
ck('subtypes_allowed',set(r['manifestation_subtype'] for r in pos)<=allowed,sorted(set(r['manifestation_subtype'] for r in pos)))
inst=[r for r in pos if r['manifestation_subtype']=='INSTRUMENTAL_ENACTMENT']
allowed_bridge={'SOURCE_EXPLICIT_MEANS','GOVERNED_T04_BRIDGE','SOURCE_NATIVE_BATTERY_BRIDGE'}
ck('instrumental_bridge_law',set(r['bridge_basis_type'] for r in inst)<=allowed_bridge,sorted(set(r['bridge_basis_type'] for r in inst)))
ck('coverage_defects_withheld',all(r['runtime_relation_withheld'].upper()=='YES' for r in cov),Counter(r['runtime_relation_withheld'] for r in cov))
def members(s):
    try:return tuple(sorted(json.loads(s)))
    except:return (s,)
t15keys={(r['source_family'],r['wave'],members(r['member_implementation_ids_json'])) for r in pos}
t06keys={(r['source_family'],r['wave'],members(r['member_implementation_ids_json'])) for r in t06}
ck('t06_t15_antijoin',not (t15keys&t06keys),len(t15keys&t06keys))
for r in pos:
    for c in ['active_source_wave_set_json','member_semantic_unit_ids_json','member_implementation_ids_json','role_assignments_json','bridge_basis_ids_json','source_provenance_json','overlap_with_existing_s14_rule_json']:
        try:json.loads(r[c])
        except Exception:ck('json_valid_'+c,False,r['central_relation_id']);break
else:
    ck('positive_json_fields_parse',True,'all')
status='PASS' if all(x['pass'] for x in checks) else 'FAIL'
print(json.dumps({'status':status,'checks':checks},indent=2))
sys.exit(0 if status=='PASS' else 1)
