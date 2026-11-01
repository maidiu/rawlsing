#!/usr/bin/env python3
"""Validate hostile A×B review evidence and its corrected denominators."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path

class ValidationError(AssertionError): pass
def req(c,m):
    if not c: raise ValidationError(m)
def jl(p): return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]

def validate(root: Path):
    counts=json.loads((root/'HOSTILE_COUNTS.json').read_text())
    false=jl(root/'FALSE_SUBTRACTION_CASES.jsonl')
    defects=jl(root/'DECISION_ATTRIBUTION_DEFECTS.jsonl')
    audit=json.loads((root/'A_EXACT_AUDIT.json').read_text())
    for f in ('HOSTILE_FINDINGS.md','ADMISSIBLE_REDUCED_SCOPE.md'):
        req((root/f).is_file(),f'missing {f}')
    A=counts['A']; B=counts['B']
    req(A['branch_rows']==A['unique_names']==845,'A names')
    req(A['unique_tips']==838,'A tips')
    req(A['code_bearing']==321 and A['stranded']==276 and A['exact_present']==45,'A 321/276/45')
    req(A['evidence_only']==458 and A['no_delta']==66,'A 458/66')
    req(A['branch_only_exact_impl']==1333,'A branch-only')
    req(A['other_path_targets']==11 and A['other_path_target_test']==65,'A other path')
    req(A['multi_exact_branch_variants']==851,'A multi-branch exact')
    req(A['declared_subtraction']==2269,'A declared subtraction')
    req(not any(x.get('semantic_equivalence') is True for x in false),'false case semantic equivalence')
    req(B['primary_rows']==155 and B['unique_primary_ids']==122 and B['decision_records']==135,'B 155/122/135')
    req(B['fate_classified']==151 and B['hq_other_unclassified_rows']==4 and B['hq_other_class_rows']==5,'B 151/4/5')
    req(B['multi_branch_decision_records']==32 and B['duplicate_tip_groups']==7,'B multi/alias')
    req(B['crosswalk_records']==135 and B['crosswalk_promoted_ids']==0 and B['crosswalk_max_observed_families']==145,'B crosswalk')
    req(counts['accepted_nine']['premain_ancestors']==0,'accepted ancestors')
    req(len(counts['accepted_nine']['all_exact'])==4 and len(counts['accepted_nine']['partial'])==1 and len(counts['accepted_nine']['nonexact'])==3 and len(counts['accepted_nine']['no_code'])==1,'accepted categories')
    req(len(false)==13,'false case count')
    agg=[x for x in false if x['case_type']=='AGGREGATE_BRANCH_ONLY_EXACT_NOT_CURRENT']
    req(len(agg)==1 and agg[0]['function_count']==1333,'false aggregate')
    others=[x for x in false if x['case_type']=='EXACT_OTHER_PATH_COPY_OR_TEST_TARGET']
    req(len(others)==11 and sum(x['function_count'] for x in others)==291,'false other path count')
    req(sum(x['function_count'] for x in others if x['current_target_is_test'])==65,'false test targets')
    req(all(x.get('subtraction_member') is True for x in false),'false subtraction membership')
    req(len(defects)==7,'defect count')
    req({x['defect_id'] for x in defects}=={f'DAD-{i:03d}' for i in range(1,8)},'defect ids')
    req(all(x.get('claim') and x.get('contradictory_source') and x.get('correction') for x in defects),'defect fields')
    req(audit['exact_present_checked']==45 and audit['exact_present_pass']==45,'A exact audit')
    req(audit['stranded_sample_checked']==10 and audit['stranded_sample_with_bad']==10,'A stranded audit')
    return {'schema':'RRIF_V_VALIDATION@1','result':'PASS','cuts':counts['cuts'],'counts':{'A':A,'B':B,'false_cases':len(false),'defects':len(defects),'accepted_nine':counts['accepted_nine']},'checks':['845/838','321/276/45','1333 branch-only exact excluded from current','291 other-path / 65 test targets','155 branch rows / 122 unique IDs / 135 records / 151 classified / 4 unclassified / 5 HQ_OTHER','45 exact-present independently audited','9 accepted branches categorized']}

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent); ap.add_argument('--output',type=Path)
    a=ap.parse_args()
    try: r=validate(a.root)
    except (ValidationError,KeyError,ValueError,json.JSONDecodeError) as e:
        print(json.dumps({'result':'FAIL','error':str(e)},indent=2)); return 1
    t=json.dumps(r,indent=2)+'\n'
    if a.output: a.output.write_text(t)
    print(t,end=''); return 0
if __name__=='__main__': sys.exit(main())
