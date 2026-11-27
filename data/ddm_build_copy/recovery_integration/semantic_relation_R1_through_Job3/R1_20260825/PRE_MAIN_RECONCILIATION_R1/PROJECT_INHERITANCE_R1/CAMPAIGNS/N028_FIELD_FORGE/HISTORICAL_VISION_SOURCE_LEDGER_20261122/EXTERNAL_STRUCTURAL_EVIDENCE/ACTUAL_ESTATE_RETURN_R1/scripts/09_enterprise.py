import sys, zipfile, io, pathlib, collections
from pathlib import Path
sys.path.insert(0,'/Users/matthewsmith/Desktop/FIELD_FORGE_EXTERNAL_ESTATE_RETURN_R1/scripts')
from lib import *
import pyreadstat, warnings
warnings.filterwarnings('ignore')
T=[]; V=[]; VC=[]; C=[]; D=[]
root=ROOT/'Enterprise'
def ensure_inner(outer_name):
    z=zipfile.ZipFile(root/outer_name); inner=z.namelist()[0]; data=z.read(inner); iz=zipfile.ZipFile(io.BytesIO(data))
    out=[]
    for m in iz.infolist():
        if m.filename.endswith('.dta') or m.filename.lower().endswith('.pdf'):
            p=pathlib.Path('/tmp')/m.filename
            if not p.exists():
                with open(p,'wb') as f: f.write(iz.read(m.filename))
            out.append((m.filename,str(p),m.file_size))
    return inner,out
specs=[
 ('Indicators Database - Global Methodology.zip','ES13','aggregate global-methodology indicator database','WBES enterprise indicator database, global methodology'),
 ('Indicators Database - Not Global Methodology.zip','ES13','historical non-global-methodology indicator database','WBES enterprise indicator database, not-global methodology'),
 ('Informal Sector Enterprise Surveys-Indicators-Database.zip','ES13','informal-sector enterprise indicator database','Informal Sector Enterprise Surveys indicator database'),
]
for outer,es,rel,label in specs:
    inner,files=ensure_inner(outer)
    for fn,path,size in files:
        if fn.endswith('.dta'):
            m=pyreadstat.read_dta(path,metadataonly=True)[1]
            T.append(dict(source='ENTERPRISE',es_id=es,release=rel,table_or_object=label,relative_path=str((root/outer).relative_to(ROOT)),format='stata_dta (nested zip member)',rows=m.number_rows,columns=m.number_columns,grain='establishment/firm-level indicator row (raw values not exported)',key_columns='idstd; wbcode/country; year; size; ownership; exporter; sector_3 (global/non-global); idstd/country/city (informal)',units='mixed percentages, counts, local currency, days, indices',universe='enterprise survey establishments; global vs historical non-global vs informal-city universes distinct',dates='survey year where present',geography='economy code/name; informal data city-level',docs='Indicator-Description.pdf / methodology PDFs',read_status='INSPECTED_SCHEMA_AND_COUNTS_ONLY',notes=f'nested member {fn}; {size} bytes; no raw firm rows or identifiers exported'))
            for c in m.column_names:
                lab=m.column_names_to_labels.get(c) or ''
                vl=m.variable_value_labels.get(c,{})
                role='selected_dimension' if c in ('size','ownership','exporter','sector_3','fin14','fin34','fin16','wk14','wk21','gend2','gend6','in16','in10','reg1','bus2','tax1','corr11','disp3','wk9','obst1','obst4','obst8','obst10','obst13','perf1','perf2','sec1','sec2','sec3','wf1','wf5','ge1') else 'metadata'
                V.append(dict(source='ENTERPRISE',es_id=es,release=rel,table_or_object=label,variable=c,label_or_definition=lab or c,storage_type=str(m.readstat_variable_types.get(c,'')),role=role,value_label_present='yes' if vl else 'no',unit_or_scale=('percentage/count/currency/days/index as label' if c not in ('idstd','wbcode','country','year','cityx') else ''),classification_or_denominator=('firm size/ownership/exporter/sector categories' if c in ('size','ownership','exporter','sector_3') else ''),missing_or_special_states=('value labels present' if vl else ''),docs_ref='Indicator-Description.pdf / methodology PDF',availability='observed',profile_scope='complete_metadata_census' if 'global-methodology indicator database' in rel else 'schema_and_selected_dimensions',notes='Enterprise aggregate indicator file; raw firm rows not exported'))
                for code,labelv in vl.items():
                    VC.append(dict(source='ENTERPRISE',es_id=es,release=rel,table_or_object=label,variable=c,code=str(code),label=str(labelv),missing_or_special='',docs_ref='Indicator-Description.pdf',used_in_selected_dimension='yes' if role=='selected_dimension' else 'no'))
        elif fn.lower().endswith('.pdf'):
            T.append(dict(source='ENTERPRISE',es_id=es,release=rel,table_or_object=label+' documentation',relative_path=str((root/outer).relative_to(ROOT)),format='pdf (nested zip member)',rows='',columns='',grain='documentation',key_columns='',units='',universe='',dates='',geography='',docs=fn,read_status='INSPECTED_HEADER_ONLY',notes='PDF text extractor unavailable; header and presence verified'))
# reserve archive rows
for p in sorted(root.glob('*.zip')):
    if p.name in [s[0] for s in specs]: continue
    T.append(dict(source='ENTERPRISE',es_id='RESERVE_ENTERPRISE',release='reserve',table_or_object=p.name,relative_path=str(p.relative_to(ROOT)),format='zip',rows='',columns='',grain='reserve archive; not profiled',key_columns='',units='',universe='reserve raw/other enterprise database',dates='',geography='',docs='reserve',read_status='RESERVE_NOT_PROFILED',notes='Not deeply profiled per commission; archive membership is in FILE_MANIFEST.tsv'))
# coverage reads
coverage_specs=[
 ('/tmp/WBES-Indicators-Database-Global-Methodology_November_11_2026.dta','ES13','aggregate global-methodology indicator database','wbcode',['size','ownership','exporter','sector_3','fin14','fin34','fin16','wk14','in16','reg1','corr11','perf1'],'country-year'),
 ('/tmp/ES-Indicators-Database-Not-Global-Methodology_October_26_2026.dta','ES13','historical non-global-methodology indicator database','wbcode',['size','ownership','exporter','sector_3','fin14','fin34','fin16','wk14','in16','reg1','corr11','perf1'],'country-year'),
 ('/tmp/Informal-Sector-Enterprise-Surveys-Indicators-Database_November_20_2026.dta','ES13','informal-sector enterprise indicator database','country_abr',['sec1','sec2','sec3','wf1','wf5','ge1'],'country-city'),
]
for path,es,rel,idcol,vars_,grain in coverage_specs:
    if not pathlib.Path(path).exists(): continue
    m=pyreadstat.read_dta(path,metadataonly=True)[1]
    cols=[c for c in [idcol,'country','year','cityx']+vars_ if c in m.column_names]
    df,_=pyreadstat.read_dta(path,usecols=cols)
    if 'year' not in df.columns: df['year']=None
    if 'cityx' not in df.columns: df['cityx']=''
    for keys,g in df.groupby([idcol]+(['cityx'] if 'cityx' in df.columns and df['cityx'].astype(str).str.len().max()>0 else []),dropna=False):
        if not isinstance(keys,tuple): keys=(keys,)
        iso=str(keys[0]); city=keys[1] if len(keys)>1 else ''
        ys=[int(y) for y in g['year'].dropna().unique()] if 'year' in g else []
        for var in vars_:
            if var not in g.columns: continue
            C.append(dict(es_id=es,source='ENTERPRISE',release=rel,table_or_object=rel,variable_or_indicator=var,source_geo_id=iso,source_geo_label=str(g['country'].iloc[0]) if 'country' in g.columns else '',year_or_interval=ranges(ys),valid_count=int(g[var].notna().sum()),missing_count=int(g[var].isna().sum()),native_status_flags=f'city={city}' if city else '',country_grain=grain,match_basis='iso3_code' if valid_iso(iso) else 'country_abbreviation_or_name',roster_iso3=iso if valid_iso(iso) else '',roster_match=('exact' if iso in ROSTER else 'not_in_roster') if valid_iso(iso) else 'unresolved',notes=f'establishment_rows={len(g)}; no raw firm values exported'))
D.append(dict(es_id='ES13',requested_dimension='Employer-context distributions and barriers: enterprise size, ownership, employment composition, financing, infrastructure and institutional constraints',source='Enterprise Surveys',release='ES13 selected aggregate indicator databases',table_or_object='global-methodology; not-global-methodology; informal-sector indicator databases',variables_or_selector='size; ownership; exporter; sector_3; fin14; fin34; fin16; wk14; wk21; gend2; gend6; in16; in10; reg1; bus2; tax1; corr11; disp3; wk9; obst1; obst4; obst8; obst10; obst13; perf1; perf2; informal sec1-3, wf1-7, ge1-2, fin1-17, op1-12',definition='establishment-level indicator databases with survey weights and firm characteristics; not raw firm analysis',units_or_universe='firm universes: formal global, historical non-global, informal-city; distinct and not nation-representative where city-only',date_semantics='survey year; non-global and informal historical universes separate',geography_semantics='economy codes/names; informal city-level only',coverage_ref='COVERAGE_ENTERPRISE.tsv',direct_proxy_absent='direct establishment indicators; not worker outcomes',known_limitation='firm is not worker; formal/historical/informal universes distinct; no nation inference from city sample; raw firm microdata not ingested',evidence_ref='DTA metadata and country-year/city counts inspected'))
write_tsv('TABLES_ENTERPRISE.tsv',['source','es_id','release','table_or_object','relative_path','format','rows','columns','grain','key_columns','units','universe','dates','geography','docs','read_status','notes'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','relative_path','format','rows','columns','grain','key_columns','units','universe','dates','geography','docs','read_status','notes']] for x in T])
write_tsv('VARIABLES_ENTERPRISE.tsv',['source','es_id','release','table_or_object','variable','label_or_definition','storage_type','role','value_label_present','unit_or_scale','classification_or_denominator','missing_or_special_states','docs_ref','availability','profile_scope','notes'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','variable','label_or_definition','storage_type','role','value_label_present','unit_or_scale','classification_or_denominator','missing_or_special_states','docs_ref','availability','profile_scope','notes']] for x in V])
write_tsv('VALUE_CODES_ENTERPRISE.tsv',['source','es_id','release','table_or_object','variable','code','label','missing_or_special','docs_ref','used_in_selected_dimension'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','variable','code','label','missing_or_special','docs_ref','used_in_selected_dimension']] for x in VC])
write_tsv('COVERAGE_ENTERPRISE.tsv',['es_id','source','release','table_or_object','variable_or_indicator','source_geo_id','source_geo_label','year_or_interval','valid_count','missing_count','native_status_flags','country_grain','match_basis','roster_iso3','roster_match','notes'],[[x.get(k,'') for k in ['es_id','source','release','table_or_object','variable_or_indicator','source_geo_id','source_geo_label','year_or_interval','valid_count','missing_count','native_status_flags','country_grain','match_basis','roster_iso3','roster_match','notes']] for x in C])
write_tsv('DIMENSION_MAP_ENTERPRISE.tsv',['es_id','requested_dimension','source','release','table_or_object','variables_or_selector','definition','units_or_universe','date_semantics','geography_semantics','coverage_ref','direct_proxy_absent','known_limitation','evidence_ref'],[[x.get(k,'') for k in ['es_id','requested_dimension','source','release','table_or_object','variables_or_selector','definition','units_or_universe','date_semantics','geography_semantics','coverage_ref','direct_proxy_absent','known_limitation','evidence_ref']] for x in D])
