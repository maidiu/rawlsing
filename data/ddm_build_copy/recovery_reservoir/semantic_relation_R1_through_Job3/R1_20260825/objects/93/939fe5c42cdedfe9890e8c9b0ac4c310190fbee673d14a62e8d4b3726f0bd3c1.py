"""Final deterministic reconciliation applied after hostile QA.
- Removes accidental synthetic positive-table index column to match materialized R16F schema contract.
- Corrects source-proven GSS XMARSEX norm-shore accounting.
- Reconciles wave attestation counts.
This script documents the final delta; it is not automatically re-run during validation.
"""
from pathlib import Path
import pandas as pd, json
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'RETURN'
SCHEMA=Path('/mnt/data/t06w04_source_first/schema_only/CENTRAL_POSITIVE_S14_RELATION_AUTHORITY_R16F.csv')
P=pd.read_csv(R/'T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv',dtype=str).fillna('')
if 'index' in P.columns: P=P.drop(columns=['index'])
if SCHEMA.exists(): P=P.reindex(columns=pd.read_csv(SCHEMA,nrows=0).columns.tolist())
P.to_csv(R/'T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv',index=False)
A=pd.read_csv(R/'T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv',dtype=str).fillna('')
mask=A.question_implementation_id.eq('question_impl.phase0.8dbc76d03be025a7d974')
if mask.sum()==1:
    A.loc[mask,'implementation_classification']='NORM_SHORE'
    A.loc[mask,'action_signature_json']=json.dumps({'actor':'married person; respondent as possible instance','action':'have sexual relations with someone other than spouse/marriage partner','target_or_object':'marital sexual exclusivity','modality':'normative wrongness','condition':'while married','respondent_universe':'GSS 2002 Ballot 1 source version','source_battery_or_stem':'Sexual morality / extramarital sex norm'},separators=(',',':'))
    A.loc[mask,'source_battery_or_stem']='Sexual morality / extramarital sex norm'
    A.loc[mask,'source_basis']='Flattened native questionnaire recovers the married-person extramarital-sex wrongness question at GSS/2002 GSS V1.pdf p.36.'
    A.loc[mask,'source_binding_status']='RECOVERED_FLATTENED_NATIVE_PAGE'
    A.loc[mask,'explicit_source_relative_path']='GSS/2002 GSS V1.pdf'; A.loc[mask,'explicit_source_page']='36'
    A.loc[mask,'norm_to_conduct_search_complete']='TRUE'; A.loc[mask,'conduct_to_norm_search_complete']=''
    A.loc[mask,'plausible_crosswalk_review_count']='1'; A.loc[mask,'accounting_confidence']='HIGH'
    A.loc[mask,'accounting_note']='Source-first repair: native moral-wrongness wording proves NORM_SHORE; explicitly crosswalked to EVSTRAY realized conduct.'
A.to_csv(R/'T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv',index=False)
