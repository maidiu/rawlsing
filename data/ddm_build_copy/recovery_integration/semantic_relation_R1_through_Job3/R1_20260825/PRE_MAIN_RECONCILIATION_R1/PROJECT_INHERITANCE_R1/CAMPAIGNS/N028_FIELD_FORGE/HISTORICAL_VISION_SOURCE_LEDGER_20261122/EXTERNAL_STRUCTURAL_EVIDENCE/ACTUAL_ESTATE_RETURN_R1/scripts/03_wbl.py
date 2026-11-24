import sys, csv, json
from pathlib import Path
sys.path.insert(0,'/Users/matthewsmith/Desktop/FIELD_FORGE_EXTERNAL_ESTATE_RETURN_R1/scripts')
from lib import *
import pyreadstat, warnings
warnings.filterwarnings('ignore')

T=[]; V=[]; VC=[]; C=[]; D=[]
def add_table(**kw): T.append(kw)
def add_var(**kw): V.append(kw)
def add_code(**kw): VC.append(kw)
def add_cov(**kw): C.append(kw)
def add_dim(**kw): D.append(kw)
root=ROOT/'WOMEN_BUSINESS_AND_LAW'

def profile_dta(rel, es, release, table, path, grain, units, universe, docs, selected_prefixes=None, coverage_vars=None, year_col=None, id_col='economycode'):
    df,m=pyreadstat.read_dta(str(path))
    cols=m.column_names
    add_table(source='WBL',es_id=es,release=release,table_or_object=table,relative_path=str(path.relative_to(ROOT)),format='stata_dta',rows=m.number_rows,columns=m.number_columns,grain=grain,key_columns=id_col+(' + '+year_col if year_col else ''),units=units,universe=universe,dates=('year field '+year_col if year_col else 'single report-year cross-section'),geography=f"{df[id_col].nunique()} economy codes",docs=docs,read_status='INSPECTED',notes='')
    for c in cols:
        lab=m.column_names_to_labels.get(c) or ''
        vl=m.variable_value_labels.get(c,{})
        role='selected_dimension' if (selected_prefixes and any(c.startswith(p) for p in selected_prefixes)) else ('key' if c in (id_col,year_col,'Economy','ISOcode') else 'metadata')
        add_var(source='WBL',es_id=es,release=release,table_or_object=table,variable=c,label_or_definition=lab or c,storage_type=str(df[c].dtype),role=role,value_label_present='yes' if vl else 'no',unit_or_scale=('index/score or question response' if 'index' in c.lower() or c.endswith('_ts') or c.endswith('_qs') or c.endswith('_is') else ''),classification_or_denominator='',missing_or_special_states=('value labels: '+str(sorted(set(vl.values()))[:5]) if vl else ''),docs_ref=docs,availability='observed',profile_scope='complete_metadata_census' if table in ('WBL 2026 full 3-pillar','WBL 1.0 historical panel','WBL 2024 legal frameworks','WBL 2024 supportive frameworks','WBL 2024 expert opinions by economy') else 'selected_dimensions',notes='')
        for code,label in vl.items():
            add_code(source='WBL',es_id=es,release=release,table_or_object=table,variable=c,code=str(code),label=str(label),missing_or_special='',docs_ref=docs,used_in_selected_dimension='yes' if role=='selected_dimension' else 'no')
    # coverage
    if coverage_vars:
        for var in coverage_vars:
            if var not in df.columns: continue
            for eco,g in df.groupby(id_col,dropna=False):
                iso=str(eco)
                valid=g[var].notna().sum(); miss=g[var].isna().sum()
                if year_col and year_col in g.columns: ys=g[year_col].dropna().astype(int).tolist()
                else: ys=[]
                add_cov(es_id=es,source='WBL',release=release,table_or_object=table,variable_or_indicator=var,source_geo_id=iso,source_geo_label=str(g['Economy'].iloc[0]) if 'Economy' in g.columns else '',year_or_interval=ranges(ys) if ys else ('single cross-section' if not year_col else ''),valid_count=int(valid),missing_count=int(miss),native_status_flags='',country_grain='economy',match_basis='iso3_code',roster_iso3=iso,roster_match='exact' if iso in ROSTER else 'not_in_roster',notes='')
    return df,m

# WBL 1.0
df10,m10=profile_dta('ES08','ES08','WBL 1.0 1971-2024','WBL 1.0 historical panel',root/'data/WBL1-0-1971-2024.dta',
 'economy-year (report year)', 'index 0-100; year', '190 economies; WBL 1.0 eight-topic legal index', 'WBL2024-Data-Notes.pdf; WBL-Full-report-2024.pdf; WBL methodology page',
 selected_prefixes=['WBL_index','GR'], coverage_vars=['WBL_index','GR1_mobility','GR2_workplace','GR3_pay','GR4_marriage','GR5_parenthood','GR6_entrprnshp','GR7_assets','GR8_pension'], year_col='year')
add_dim(es_id='ES08',requested_dimension='WBL 1.0 historical legal index and eight-topic legal scores by economy and report year',source='WBL',release='WBL 1.0 1971-2024',table_or_object='WBL 1.0 historical panel',variables_or_selector='WBL_index; GR1_mobility; GR2_workplace; GR3_pay; GR4_marriage; GR5_parenthood; GR6_entrprnshp; GR7_assets; GR8_pension; year; reportyr',definition='legal-framework index and topic scores constructed from binary legal questions',units_or_universe='0-100 index; 190 economies; report years 1971-2024',date_semantics='internal year field 1970-2023; reportyr 1971-2024',geography_semantics='economycode ISO3',coverage_ref='COVERAGE.tsv ES08',direct_proxy_absent='direct legal coding, not enforcement or practice',known_limitation='composite index; legal scope and exceptions not identical to practical access; WBL 1.0 vs 2.0 not silently combine',evidence_ref='DTA metadata and WBL 2024 data notes')

# WBL 2026 3-pillar full
df26,m26=profile_dta('ES08','ES08','WBL 2026','WBL 2026 full 3-pillar',root/'data/WBL26-3Pillar-Scores-Published.dta',
 'economy cross-section (ReportYear 2026)', 'index/score 0-100; binary/categorical question responses', '190 economies; 10 topics; legal, supportive, enforcement perceptions', 'WBL-Methodology-Handbook-2026-FINAL.pdf; WBL 2026 data page',
 selected_prefixes=['LF_','SF_','EP_','Saf_','Mob_','Wrk_','Pay_','Mar_','Par_','Chd_','Ent_','Ast_','Pen_'], coverage_vars=['LF_econ_index','SF_econ_index','EP_econ_index'], year_col='ReportYear', id_col='EconomyCode')
add_dim(es_id='ES08',requested_dimension='Differentiated legal capacity, institutional availability and perceived enforcement across ten WBL topics',source='WBL',release='WBL 2026',table_or_object='WBL 2026 full 3-pillar',variables_or_selector='LF_econ_index; SF_econ_index; EP_econ_index; *_ts topic scores; *_qs question variables; *_is indicator summaries',definition='separate legal-framework, supportive-framework and enforcement-perception measures',units_or_universe='0-100 scores and binary/categorical question responses; 190 economies; 10 topics',date_semantics='ReportYear 2026; data current as of October 1, 2026 per source',geography_semantics='EconomyCode ISO3',coverage_ref='COVERAGE.tsv ES08',direct_proxy_absent='direct legal/supportive coding; perception is expert-opinion product, not observed enforcement',known_limitation='do not substitute composite ranking for provision; legal scope/exceptions and actual enforcement separate; WBL versions not silently combined',evidence_ref='3-pillar DTA metadata and 2026 methodology handbook')

# 2024 legal/supportive/EP
for f,table,esname,prefixes,cov in [
 ('WBL2024_LEGAL_EconLevel_ToPublish.dta','WBL 2024 legal frameworks','WBL 2024 legal','WBL2024_LEGAL_EconLevel_ToPublish.dta',['OVERALL','SAFETY','MOBILITY','WORKPLACE','PAY','MARRIAGE','PARENTHOOD','CHILDCARE','ENTREPRENEURSHIP','ASSETS','PENSION']),
 ('WBL2024_SUPPORTIVE_EconLevel_ToPublish.dta','WBL 2024 supportive frameworks','WBL 2024 supportive','WBL2024_SUPPORTIVE_EconLevel_ToPublish.dta',['OVERALL','SAFETY','MOBILITY','WORKPLACE','PAY','MARRIAGE','PARENTHOOD','CHILDCARE','ENTREPRENEURSHIP','ASSETS','PENSION']),
 ('WBL2024_ExpertOpinion_EconLevel_ToPublish2.dta','WBL 2024 expert opinions by economy','WBL 2024 expert opinions','WBL2024_ExpertOpinion_EconLevel_ToPublish2.dta',['OVERALL','SAFETY','MOBILITY','WORKPLACE','PAY','MARRIAGE','PARENTHOOD','CHILDCARE','ENTREPRENEURSHIP','ASSETS','PENSION','TotalSubmissions'])]:
    p=root/'data'/f
    profile_dta('ES08','ES08',esname,table,p,'economy cross-section','0-100 score; binary/categorical responses','190 economies (164 for expert opinions)','WBL-Full-report-2024.pdf; WBL2024-Data-Notes.pdf; WBL 2024 download page',selected_prefixes=None,coverage_vars=cov,id_col=('EconomyCode' if f.startswith('WBL2024_ExpertOpinion') else 'economycode'))
# respondent-level reserve (inventory only, no respondent values)
dfeo,meo=pyreadstat.read_dta(str(root/'data/WBL2024_ExpertOpinion_EOLevel_ToPublish2.dta'))
add_table(source='WBL',es_id='ES08',release='WBL 2024 expert opinions',table_or_object='WBL 2024 expert opinions by respondent',relative_path=str((root/'data/WBL2024_ExpertOpinion_EOLevel_ToPublish2.dta').relative_to(ROOT)),format='stata_dta',rows=meo.number_rows,columns=meo.number_columns,grain='respondent-economy submission (restricted/reserve; not profiled)',key_columns='SubmissionID + EconomyID',units='ordinal opinion responses 1-4/NA',universe='expert respondents, 164 economies',dates='2024 report cross-section',geography=f"{dfeo['EconomyCode'].nunique()} economy codes",docs='WBL 2024 expert opinion data notes',read_status='INSPECTED_SCHEMA_ONLY',notes='Reserve respondent-level product; no raw respondent values exported')
# 2026 separate pillar files
for f,table in [('WBL26-LF-Scores-Published.dta','WBL 2026 legal frameworks'),('WBL26-SF-Scores-Published.dta','WBL 2026 supportive frameworks'),('WBL26-EP-Scores-Published.dta','WBL 2026 enforcement perceptions')]:
    p=root/'data'/f
    profile_dta('ES08','ES08','WBL 2026',table,p,'economy cross-section','0-100 score; binary/categorical responses','190 economies (178 for enforcement perceptions)','WBL 2026 methodology',selected_prefixes=['LF_','SF_','EP_'],coverage_vars=[x for x in ['LF_econ_index','SF_econ_index','EP_econ_index'] if x in pyreadstat.read_dta(str(p),metadataonly=True)[1].column_names],year_col='ReportYear', id_col='EconomyCode')
# xlsx metadata and selected coverage
import openpyxl
def xlsx_table(rel,es,release,table,sheet,header_row,grain,units,universe,coverage_col=None,selected_rows=()):
    p=root/rel
    wb=openpyxl.load_workbook(p,read_only=True,data_only=True)
    ws=wb[sheet]
    add_table(source='WBL',es_id=es,release=release,table_or_object=table+' ['+sheet+']',relative_path=str(p.relative_to(ROOT)),format='xlsx',rows=ws.max_row,columns=ws.max_column,grain=grain,key_columns='Economy / EconomyCode where present',units=units,universe=universe,dates='see About sheet',geography='economy',docs='See workbook About and Methodology sheets',read_status='INSPECTED',notes='Header row '+str(header_row)+'; no image or formula profiling')
    # variables from header row
    hdr=[c.value for c in ws[header_row]]
    for i,h in enumerate(hdr,1):
        if h is None: continue
        add_var(source='WBL',es_id=es,release=release,table_or_object=table+' ['+sheet+']',variable=str(h),label_or_definition=str(h),storage_type='xlsx cell',role='selected_dimension' if any(str(h).lower().startswith(s) for s in selected_rows) else 'metadata',value_label_present='no',unit_or_scale='',classification_or_denominator='',missing_or_special_states='',docs_ref='workbook About/Methodology',availability='observed',profile_scope='complete_metadata_census',notes='Header-derived name; underlying cell types may vary')
    # coverage if economy code column found
    if coverage_col:
        rows=list(ws.iter_rows(min_row=header_row+1,values_only=True))
        hi={str(c.value):i for i,c in enumerate(ws[header_row],1) if c.value}
        if coverage_col in hi and 'EconomyCode' in hi:
            ci=hi[coverage_col]-1; ei=hi['EconomyCode']-1
            for r in rows:
                if r[ei] is None: continue
                iso=str(r[ei]); val=r[ci]
                add_cov(es_id=es,source='WBL',release=release,table_or_object=table+' ['+sheet+']',variable_or_indicator=coverage_col,source_geo_id=iso,source_geo_label=str(r[hi['Economy']-1]) if 'Economy' in hi else '',year_or_interval='single cross-section',valid_count=1 if val not in (None,'') else 0,missing_count=0 if val not in (None,'') else 1,native_status_flags='',country_grain='economy',match_basis='iso3_code',roster_iso3=iso,roster_match='exact' if iso in ROSTER else 'not_in_roster',notes='')
    wb.close()
xlsx_table('data/WBL2024-2-0.xlsx','ES08','WBL 2024','WBL 2024 all-pillars','Legal2.0',1,'economy cross-section','0-100 and binary/categorical','190 economies','OVERALL',('overall','safety'))
xlsx_table('data/WBL2024-2-0.xlsx','ES08','WBL 2024','WBL 2024 all-pillars','SF2.0',1,'economy cross-section','0-100 and binary/categorical','190 economies','OVERALL',('overall','safety'))
xlsx_table('data/WBL2024-2-0.xlsx','ES08','WBL 2024','WBL 2024 all-pillars','EO_ByEconomy',2,'economy cross-section','0-100 and ordinal','164 economies','WBL 2024 EO 2.0 index',('wbl','safety'))
xlsx_table('data/WBL2024-2-0.xlsx','ES08','WBL 2024','WBL 2024 all-pillars','EO_ByRespondent',2,'respondent submission','ordinal','1,224 submissions','')
xlsx_table('data/2026-02-26-WBL-2026-1-0-Scores-Values_F.xlsx','ES08','WBL 2026 1.0','WBL 2026 recalculated under WBL 1.0','WBL 2026 1.0',1,'economy cross-section','0-100 and binary','190 economies','WBL 1.0 INDEX',('wbl 1.0 index','mobility'))
xlsx_table('data/2026.02.19_WBL26_FINAL Data for Download.xlsx','ES08','WBL 2026','WBL 2024-2025 under 2026 methodology','I. Legal Frameworks',4,'economy cross-section','0-100 and binary','190 economies','WBL26 Economy LF Index',('wbl26 economy lf index',))
xlsx_table('data/WBL_Financial_Inclusion_Data.xlsx','ES08','NFIS 2022','National Financial Inclusion Strategies','Financial Inclusion Data Set',1,'economy cross-section','binary/current strategy','190 economies',None,('does the economy have','are banks'))
xlsx_table('data/WBL_2022_Women_with_Disabilities_Final_Data.xlsx','ES08','WBL 2022 disabilities','Rights of Women with Disabilities','Women with Disabilities Data',1,'economy cross-section','binary','190 economies',None,('is there a gender equality','is there a law on persons'))
xlsx_table('data/WBL-1971-2024-Reforms_Database.xlsx','ES08','WBL 2024 reforms','Historical reforms database 1971-2024','Reform database (1971-2024)_web',1,'reform event','date/text/category','2,329 reform rows','Name of the Law',('name of the law','date of enactment'))
xlsx_table('data/Reforms-Database-WBL-2025-2026.xlsx','ES08','WBL 2025-2026 reforms','Reforms database 2025-2026','Reforms Database (2025-2026)',1,'reform event','date/text/category','123 reform rows','Name of the Law',('name of the law','date of enactment'))

write_tsv('TABLES_WBL.tsv',['source','es_id','release','table_or_object','relative_path','format','rows','columns','grain','key_columns','units','universe','dates','geography','docs','read_status','notes'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','relative_path','format','rows','columns','grain','key_columns','units','universe','dates','geography','docs','read_status','notes']] for x in T])
write_tsv('VARIABLES_WBL.tsv',['source','es_id','release','table_or_object','variable','label_or_definition','storage_type','role','value_label_present','unit_or_scale','classification_or_denominator','missing_or_special_states','docs_ref','availability','profile_scope','notes'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','variable','label_or_definition','storage_type','role','value_label_present','unit_or_scale','classification_or_denominator','missing_or_special_states','docs_ref','availability','profile_scope','notes']] for x in V])
write_tsv('VALUE_CODES_WBL.tsv',['source','es_id','release','table_or_object','variable','code','label','missing_or_special','docs_ref','used_in_selected_dimension'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','variable','code','label','missing_or_special','docs_ref','used_in_selected_dimension']] for x in VC])
write_tsv('COVERAGE_WBL.tsv',['es_id','source','release','table_or_object','variable_or_indicator','source_geo_id','source_geo_label','year_or_interval','valid_count','missing_count','native_status_flags','country_grain','match_basis','roster_iso3','roster_match','notes'],[[x.get(k,'') for k in ['es_id','source','release','table_or_object','variable_or_indicator','source_geo_id','source_geo_label','year_or_interval','valid_count','missing_count','native_status_flags','country_grain','match_basis','roster_iso3','roster_match','notes']] for x in C])
write_tsv('DIMENSION_MAP_WBL.tsv',['es_id','requested_dimension','source','release','table_or_object','variables_or_selector','definition','units_or_universe','date_semantics','geography_semantics','coverage_ref','direct_proxy_absent','known_limitation','evidence_ref'],[[x.get(k,'') for k in ['es_id','requested_dimension','source','release','table_or_object','variables_or_selector','definition','units_or_universe','date_semantics','geography_semantics','coverage_ref','direct_proxy_absent','known_limitation','evidence_ref']] for x in D])
