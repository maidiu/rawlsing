from pathlib import Path
import pandas as pd,json,sys
root=Path(__file__).resolve().parent
s14=pd.read_csv(root/'S14_EXECUTABLE_GENERATION_GRAMMAR_R10K_T15.csv',dtype=str).fillna('')
s15=pd.read_csv(root/'S15_DERIVED_INDICATOR_DEFINITION_RELEASE_R10K_T15.csv',dtype=str).fillna('')
cons=pd.read_csv(root/'PARENT_ROW_CONSERVATION_R1.csv',dtype=str).fillna('')
checks={
 's14_15':len(s14)==15 and s14.rule_id.nunique()==15,
 's15_17':len(s15)==17 and s15.requirement_id.nunique()==17,
 't15_present':'S14-T15' in set(s14.rule_id),
 'je17_present':'JE-17_NORM_PRACTICAL_REALIZATION' in set(s15.requirement_id),
 'parent_rows_preserved':all(cons.preserved.str.lower()=='true'),
 't14_recall_only':s14.loc[s14.rule_id=='S14-T14','enumeration_status'].iloc[0]=='RECALL_ONLY__CANNOT_DIRECTLY_EMIT_CANDIDATE',
 'enumeration_gated':all(s14.current_permission.str.contains('FORBIDDEN_UNTIL_O11_S16_AND_O12')),
 'no_job3_authority':all(s14.job3_relation_authority_created.str.lower()=='false'),
 'no_s15_values':all(s15.runtime_values_created.str.lower()=='false')
}
print(json.dumps({'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks},indent=2))
sys.exit(0 if all(checks.values()) else 1)
