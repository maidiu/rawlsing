import sys, glob, csv, re
from pathlib import Path
sys.path.insert(0,'/Users/matthewsmith/Desktop/FIELD_FORGE_EXTERNAL_ESTATE_RETURN_R1/scripts')
from lib import *
import pyreadr, pandas as pd
T=[]; V=[]; VC=[]; C=[]; D=[]
# catalogs/dictionaries
toc=pd.read_csv(ROOT/'ILOSTAT/catalog/indicator_toc_en.csv',encoding='utf-8-sig')
toc_by_id={r['id']:r for _,r in toc.iterrows()}
def read_dict(name):
    d=pyreadr.read_r(ROOT/f'ILOSTAT/dictionaries/{name}_en.rds'); return list(d.values())[0]
ind=read_dict('indicator'); ref=read_dict('ref_area'); sex=read_dict('sex'); src=read_dict('source'); obs=read_dict('obs_status'); c1=read_dict('classif1'); c2=read_dict('classif2')
ind_map=dict(zip(ind['indicator'],ind['indicator.label'])) if 'indicator' in ind else {}
ref_map=dict(zip(ref['ref_area'],ref['ref_area.label'])) if 'ref_area' in ref else {}
sex_map=dict(zip(sex['sex'],sex['sex.label'])) if 'sex' in sex else {}
src_map=dict(zip(src['source'],src['source.label'])) if 'source' in src else {}
obs_map=dict(zip(obs['obs_status'],obs['obs_status.label'])); c1_map=dict(zip(c1['classif1'],c1['classif1.label'])); c2_map=dict(zip(c2['classif2'],c2['classif2.label']))
# value codes static dictionaries
for _,r in sex.iterrows(): VC.append(dict(source='ILOSTAT',es_id='ES09',release='annual selected',table_or_object='dictionary',variable='sex',code=str(r['sex']),label=str(r['sex.label']),missing_or_special='',docs_ref='sex_en.rds',used_in_selected_dimension='yes'))
for _,r in ref.iterrows(): VC.append(dict(source='ILOSTAT',es_id='ES09',release='annual selected',table_or_object='dictionary',variable='ref_area',code=str(r['ref_area']),label=str(r['ref_area.label']),missing_or_special='',docs_ref='ref_area_en.rds',used_in_selected_dimension='yes'))
for _,r in obs.iterrows(): VC.append(dict(source='ILOSTAT',es_id='ES09',release='annual selected',table_or_object='dictionary',variable='obs_status',code=str(r['obs_status']),label=str(r['obs_status.label']),missing_or_special='',docs_ref='obs_status_en.rds',used_in_selected_dimension='yes'))
for _,r in c1.iterrows(): VC.append(dict(source='ILOSTAT',es_id='ES09',release='annual selected',table_or_object='dictionary',variable='classif1',code=str(r['classif1']),label=str(r['classif1.label']),missing_or_special='',docs_ref='classif1_en.rds',used_in_selected_dimension='yes'))
for _,r in c2.iterrows(): VC.append(dict(source='ILOSTAT',es_id='ES09',release='annual selected',table_or_object='dictionary',variable='classif2',code=str(r['classif2']),label=str(r['classif2.label']),missing_or_special='',docs_ref='classif2_en.rds',used_in_selected_dimension='yes'))
# per file
files=sorted((ROOT/'ILOSTAT/indicator').glob('*.rds'))
for p in files:
    iid=p.stem
    try:
        d=pyreadr.read_r(str(p)); df=list(d.values())[0]
        if 'time' in df.columns: df['time']=pd.to_numeric(df['time'],errors='coerce')
    except Exception as e:
        T.append(dict(source='ILOSTAT',es_id='ES09',release='annual selected',table_or_object=iid,relative_path=str(p.relative_to(ROOT)),format='r_rds_gzip',rows='',columns='',grain='',key_columns='',units='',universe='',dates='',geography='',docs='',read_status='UNREADABLE',notes=repr(e))); continue
    t=toc_by_id.get(iid,{})
    T.append(dict(source='ILOSTAT',es_id='ES09',release='annual selected',table_or_object=iid,relative_path=str(p.relative_to(ROOT)),format='r_rds_gzip',rows=len(df),columns=len(df.columns),grain='reference-area × time × indicator × sex (long table)',key_columns='ref_area + time + indicator + sex; source',units=str(t.get('unit_measure.label','')),universe=str(t.get('indicator.label','')),dates=f"{int(t.get('data.start',df['time'].min()))}-{int(t.get('data.end',df['time'].max()))}" if 'time' in df and df['time'].notna().any() else '',geography=f"{df['ref_area'].nunique()} reference-area codes",docs='ILOSTAT indicator TOC and dictionaries; BulkDownload Guidelines',read_status='INSPECTED',notes=f"subject={t.get('subject.label','')}; classification={t.get('classification','')}; database={t.get('database.label','')}"))
    for c in df.columns:
        V.append(dict(source='ILOSTAT',es_id='ES09',release='annual selected',table_or_object=iid,variable=c,label_or_definition={'ref_area':'ILO reference area code','source':'source identifier','indicator':'indicator code','sex':'sex code','time':'year','obs_value':'observation value','best_source':'best-source flag (1/NA)','obs_status':'observation status code','classif1':'classification 1 code (sex/age/status/etc.)','classif2':'classification 2 code','note_indicator':'indicator-specific methodological note','note_source':'source-specific note','note_classif':'classification-specific note'}.get(c,c),storage_type=str(df[c].dtype),role='selected_dimension' if c in ('ref_area','time','indicator','sex','obs_value') else 'metadata',value_label_present='yes' if c in ('ref_area','sex','indicator') else 'no',unit_or_scale=('percentage/number/currency as named by indicator' if c=='obs_value' else ''),classification_or_denominator='',missing_or_special_states='schema varies by indicator: obs_status in 83/93 files; classif1 76/93; classif2 17/93; note columns present in subsets; best_source is a source-selection flag',docs_ref='indicator TOC; dictionaries',availability='observed',profile_scope='complete_metadata_census',notes=''))
    if iid in toc_by_id:
        VC.append(dict(source='ILOSTAT',es_id='ES09',release='annual selected',table_or_object=iid,variable='indicator',code=str(df['indicator'].iloc[0]) if len(df) else iid,label=str(t.get('indicator.label','')),missing_or_special='',docs_ref='indicator TOC',used_in_selected_dimension='yes'))
    # coverage by ref_area
    if 'ref_area' in df.columns and 'time' in df.columns:
        for area,g in df.groupby('ref_area',dropna=False):
            area=str(area); iso=area if valid_iso(area) else None
            ys=pd.to_numeric(g['time'],errors='coerce').dropna().astype(int).tolist(); valid=g['obs_value'].notna().sum() if 'obs_value' in g else 0
            bsrc=[]
            if 'best_source' in g: bsrc.append('best_source='+','.join(sorted(set(str(x) for x in g['best_source'].dropna().unique()))))
            if 'obs_status' in g: bsrc.append('obs_status='+','.join(sorted(set(str(x) for x in g['obs_status'].dropna().unique()))))
            bsrc=';'.join(bsrc)
            C.append(dict(es_id='ES09',source='ILOSTAT',release='annual selected',table_or_object=iid,variable_or_indicator=iid,source_geo_id=area,source_geo_label=ref_map.get(area,''),year_or_interval=ranges(ys),valid_count=int(valid),missing_count=int(g['obs_value'].isna().sum()) if 'obs_value' in g else 0,native_status_flags=bsrc,country_grain='reference-area-year',match_basis='iso3_ref_area' if iso else 'aggregate_or_non_iso',roster_iso3=iso or '',roster_match=('exact' if iso in ROSTER else 'not_in_roster') if iso else 'aggregate',notes=''))
# dimension map by subject groups
subject_to_dim={
 'EAP':'Labour force participation by sex and age','EMP':'Employment and employment-to-population ratios; status, occupation and economic activity','EES':'Employees/status-in-employment dimensions','IFL':'Informal employment by sex, age, status and sector','LUU':'Unemployment, underemployment and labour underutilization','EAR':'Earnings and wages','HOW':'Working hours','POV':'Working poverty','SOC':'Social protection coverage and benefit categories','ILR':'Trade-union density and collective bargaining','CLD':'Child labour','CAR':'Parental leave / paid care workers (maternity-protection proxy)'
}
for subj,dim in subject_to_dim.items():
    rows=toc[toc['subject']==subj]
    ids=sorted(set(p.stem for p in files if p.stem in toc_by_id and toc_by_id[p.stem].get('subject')==subj))
    if not ids: continue
    D.append(dict(es_id='ES09',requested_dimension=dim,source='ILOSTAT',release='annual selected',table_or_object='indicator/*.rds',variables_or_selector='; '.join(ids[:20])+('; ...' if len(ids)>20 else ''),definition=f'{len(ids)} annual selected indicator files; subject={subj}',units_or_universe='long RDS tables by reference area, time, indicator and sex',date_semantics='annual time field; projections may extend beyond current year',geography_semantics='ref_area codes; ISO3 countries plus regional/aggregate codes',coverage_ref='COVERAGE_ILOSTAT.tsv',direct_proxy_absent=('proxy only' if subj=='CAR' else 'direct'),known_limitation=('no dedicated maternity-protection indicator; parental leave retained as closest proxy' if subj=='CAR' else 'observed, 19th-ICLS and modelled series are separate indicator IDs; obs_status/classif/notes are present only in subsets of RDS files'),evidence_ref='ILOSTAT RDS files and TOC inspected'))
write_tsv('TABLES_ILOSTAT.tsv',['source','es_id','release','table_or_object','relative_path','format','rows','columns','grain','key_columns','units','universe','dates','geography','docs','read_status','notes'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','relative_path','format','rows','columns','grain','key_columns','units','universe','dates','geography','docs','read_status','notes']] for x in T])
write_tsv('VARIABLES_ILOSTAT.tsv',['source','es_id','release','table_or_object','variable','label_or_definition','storage_type','role','value_label_present','unit_or_scale','classification_or_denominator','missing_or_special_states','docs_ref','availability','profile_scope','notes'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','variable','label_or_definition','storage_type','role','value_label_present','unit_or_scale','classification_or_denominator','missing_or_special_states','docs_ref','availability','profile_scope','notes']] for x in V])
write_tsv('VALUE_CODES_ILOSTAT.tsv',['source','es_id','release','table_or_object','variable','code','label','missing_or_special','docs_ref','used_in_selected_dimension'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','variable','code','label','missing_or_special','docs_ref','used_in_selected_dimension']] for x in VC])
write_tsv('COVERAGE_ILOSTAT.tsv',['es_id','source','release','table_or_object','variable_or_indicator','source_geo_id','source_geo_label','year_or_interval','valid_count','missing_count','native_status_flags','country_grain','match_basis','roster_iso3','roster_match','notes'],[[x.get(k,'') for k in ['es_id','source','release','table_or_object','variable_or_indicator','source_geo_id','source_geo_label','year_or_interval','valid_count','missing_count','native_status_flags','country_grain','match_basis','roster_iso3','roster_match','notes']] for x in C])
write_tsv('DIMENSION_MAP_ILOSTAT.tsv',['es_id','requested_dimension','source','release','table_or_object','variables_or_selector','definition','units_or_universe','date_semantics','geography_semantics','coverage_ref','direct_proxy_absent','known_limitation','evidence_ref'],[[x.get(k,'') for k in ['es_id','requested_dimension','source','release','table_or_object','variables_or_selector','definition','units_or_universe','date_semantics','geography_semantics','coverage_ref','direct_proxy_absent','known_limitation','evidence_ref']] for x in D])
