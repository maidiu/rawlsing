import sys, re, collections
from pathlib import Path
sys.path.insert(0,'/Users/matthewsmith/Desktop/FIELD_FORGE_EXTERNAL_ESTATE_RETURN_R1/scripts')
from lib import *
import pyreadstat, warnings
warnings.filterwarnings('ignore')
T=[]; V=[]; VC=[]; C=[]; D=[]
root=ROOT/'RELIGION_AND_STATE/data'
def selected_ras3():
    out=[]
    for y in [1990,2000,2010,2014]:
        for pref in ['SAX','SBX','NX01X','MX01X','LX01X','VFUNDINGX','VOFFICE01X']:
            out.append(f'{pref}{y}')
    for pref in ['SAX','SBX','NX01X','MX01X','LX01X','VFUNDINGX','VOFFICE01X']:
        out.append(f'{pref}2014X')
    return out
def selected_rasm3():
    out=[]
    for y in [1990,2000,2014]:
        for pref in ['MMX01X','MMX02X','WZSOCDIS01X','WZMIN2MAJ01X','WZGENERALX']:
            out.append(f'{pref}{y}')
    for pref in ['MMX01X','MMX02X','WZSOCDIS01X','WZMIN2MAJ01X','WZGENERALX']:
        out.append(f'{pref}2014X')
    return out
def selected_const():
    out=[]
    for y in [1990,2000,2022]:
        for pref in ['coff','coffestab','csras01x','creldis01x','cfree01x','claws01x']:
            out.append(f'{pref}{y}')
    return out
def profile(path,es,release,table,selected,idcol,yearlogic,universe,grain,country_col=None):
    df,m=pyreadstat.read_sav(str(path))
    T.append(dict(source='RAS',es_id=es,release=release,table_or_object=table,relative_path=str(path.relative_to(ROOT)),format='spss_sav',rows=m.number_rows,columns=m.number_columns,grain=grain,key_columns=idcol,units='ordinal/binary expert codes; shares only where named',universe=universe,dates=yearlogic,geography=f'{df[idcol].nunique()} country values',docs='RAS3_Codebook.pdf; RASM3_Codebook.pdf; RAS_Constitutions_Codebook.pdf; online codebook snapshots',read_status='INSPECTED',notes='RAS wide country-level arrays; year is encoded in variable names, not a row year field'))
    for c in m.column_names:
        lab=m.column_names_to_labels.get(c) or ''
        vl=m.variable_value_labels.get(c,{})
        V.append(dict(source='RAS',es_id=es,release=release,table_or_object=table,variable=c,label_or_definition=lab or c,storage_type=str(df[c].dtype),role='selected_dimension' if c in selected else 'metadata',value_label_present='yes' if vl else 'no',unit_or_scale=('ordinal/binary expert code' if vl else 'administrative'),classification_or_denominator='',missing_or_special_states=('value labels may include missing/NA codes' if vl else ''),docs_ref='RAS codebook',availability='observed',profile_scope='complete_metadata_census',notes=''))
    for c in selected:
        if c not in df.columns: continue
        vl=m.variable_value_labels.get(c,{})
        for code,label in vl.items():
            special='yes' if any(k in str(label).lower() for k in ['missing','don\'t know','not applicable','not asked','no answer']) else 'no'
            VC.append(dict(source='RAS',es_id=es,release=release,table_or_object=table,variable=c,code=str(code),label=str(label),missing_or_special=special,docs_ref='RAS codebook',used_in_selected_dimension='yes'))
        # coverage by country
        cc=country_col or idcol
        for country,g in df.groupby(cc,dropna=False):
            if idcol=='ISO3' and 'ISO3' in g.columns:
                iso=str(g['ISO3'].iloc[0]) if str(g['ISO3'].iloc[0]) not in ('','nan') else iso3(country)
            else: iso=iso3(country)
            if not country or str(country)=='nan': continue
            vals=g[c]
            valid=vals.notna().sum()
            add=C.append
            yr=re.search(r'(\d{4})',c).group(1) if re.search(r'(\d{4})',c) else ''
            add(dict(es_id=es,source='RAS',release=release,table_or_object=table,variable_or_indicator=c,source_geo_id=(iso or str(country)),source_geo_label=str(country),year_or_interval=yr,valid_count=int(valid),missing_count=int(vals.isna().sum()),native_status_flags=('year_encoded_in_variable_name='+yr),country_grain=('country' if es!='ES06' else 'country-minority'),match_basis=('iso3_column' if idcol=='ISO3' else 'name_to_iso3'),roster_iso3=iso or '',roster_match=('exact' if iso in ROSTER else 'not_in_roster') if iso else 'unmatched',notes=f'groups_or_rows={len(g)}'))
    return df,m
profile(root/'RAS3_COMPLETE_ARDA.sav','ES05','RAS3 1990-2014','RAS Round 3 country array',selected_ras3(),'ISO3','1990-2014 encoded in variable names','183 countries; state religion policy','country (one row per country, year-specific columns)',country_col='COUNTRY')
profile(root/'RASM3_COMPLETE_ARDA.sav','ES06','RASM3','RAS Minorities Round 3 group array',selected_rasm3(),'COUNTRY','1990-2014 encoded in variable names','771 minorities in 183 countries','country-minority (one row per minority)',country_col='COUNTRY')
profile(root/'RAS_Constitutions_2022_v1.02.sav','ES07','RAS Constitutions v1.02','RAS Constitutions country array',selected_const(),'country','1990-2022 encoded in variable names','176 countries; constitutional religion provisions','country (one row per country, year-specific columns)',country_col='country')
# reserve RMAR and SOR shallow
for f,label in [('RMAR_2000-2014.dta','RMAR 2000-2014'),('SOR_Article_Data3.sav','Specialized RAS/WVS/ISSP SOR dataset')]:
    p=root/f
    if p.suffix=='.dta':
        m=pyreadstat.read_dta(str(p),metadataonly=True)[1]; fmt='stata_dta'
    else:
        m=pyreadstat.read_sav(str(p),metadataonly=True)[1]; fmt='spss_sav'
    T.append(dict(source='RAS',es_id='RESERVE_RAS',release=label,table_or_object=label,relative_path=str(p.relative_to(ROOT)),format=fmt,rows=m.number_rows,columns=m.number_columns,grain='reserve; not profiled',key_columns='',units='reserve',universe='reserve',dates='reserve',geography='reserve',docs='reserve',read_status='INSPECTED_SCHEMA_ONLY',notes='Reserve family; no deep variable/category profiling'))
D += [
 dict(es_id='ES05',requested_dimension='State treatment and regulation of religion, official support, privilege and restriction',source='RAS3',release='RAS3 1990-2014',table_or_object='RAS Round 3 country array',variables_or_selector='SAX{year}; SBX{year}; NX01X{year}; MX01X{year}; LX01X{year}; VFUNDINGX{year}; VOFFICE01X{year}',definition='country-level ordinal/binary expert codes for official religion, official support, restrictions on religious parties/public observance, religious marriage/divorce, funding and office oaths',units_or_universe='183 countries; 1990-2014',date_semantics='year encoded in variable name; X suffix denotes earliest/latest',geography_semantics='country name/ISO3; state unit',coverage_ref='COVERAGE_RAS.tsv ES05',direct_proxy_absent='direct expert-coded state policy, not law text or private belief',known_limitation='expert codes not law text; coverage endpoint and coding changes explicit',evidence_ref='RAS3 SAV, codebook and online codebook inspected'),
 dict(es_id='ES06',requested_dimension='Group-differentiated religious discrimination and treatment',source='RASM3',release='RASM3',table_or_object='RAS Minorities Round 3 group array',variables_or_selector='MMX01X{year}; MMX02X{year}; WZSOCDIS01X{year}; WZMIN2MAJ01X{year}; WZGENERALX{year}',definition='minority-level governmental and societal discrimination/action codes',units_or_universe='771 minorities in 183 countries',date_semantics='year encoded in variable name',geography_semantics='country-minority; no universal religious census',coverage_ref='COVERAGE_RAS.tsv ES06',direct_proxy_absent='direct minority-level expert code',known_limitation='minority coverage not universal; no name-only match or imputation',evidence_ref='RASM3 SAV and codebook inspected'),
 dict(es_id='ES07',requested_dimension='Constitutional religion provisions: establishment, recognition, guarantees, restriction',source='RAS Constitutions',release='RAS Constitutions v1.02',table_or_object='RAS Constitutions country array',variables_or_selector='coff{year}; coffestab{year}; csras01x{year}; creldis01x{year}; cfree01x{year}; claws01x{year}',definition='presence/absence of specific constitutional clauses by year',units_or_universe='176 countries; 1990-2022',date_semantics='year encoded in variable name; enactment/effective dates not separately supplied',geography_semantics='country',coverage_ref='COVERAGE_RAS.tsv ES07',direct_proxy_absent='direct constitutional clause coding',known_limitation='provision alone not operative sanction or practical access; enactment vs effective date not separate in this array',evidence_ref='Constitutions SAV and codebook inspected')
]
write_tsv('TABLES_RAS.tsv',['source','es_id','release','table_or_object','relative_path','format','rows','columns','grain','key_columns','units','universe','dates','geography','docs','read_status','notes'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','relative_path','format','rows','columns','grain','key_columns','units','universe','dates','geography','docs','read_status','notes']] for x in T])
write_tsv('VARIABLES_RAS.tsv',['source','es_id','release','table_or_object','variable','label_or_definition','storage_type','role','value_label_present','unit_or_scale','classification_or_denominator','missing_or_special_states','docs_ref','availability','profile_scope','notes'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','variable','label_or_definition','storage_type','role','value_label_present','unit_or_scale','classification_or_denominator','missing_or_special_states','docs_ref','availability','profile_scope','notes']] for x in V])
write_tsv('VALUE_CODES_RAS.tsv',['source','es_id','release','table_or_object','variable','code','label','missing_or_special','docs_ref','used_in_selected_dimension'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','variable','code','label','missing_or_special','docs_ref','used_in_selected_dimension']] for x in VC])
write_tsv('COVERAGE_RAS.tsv',['es_id','source','release','table_or_object','variable_or_indicator','source_geo_id','source_geo_label','year_or_interval','valid_count','missing_count','native_status_flags','country_grain','match_basis','roster_iso3','roster_match','notes'],[[x.get(k,'') for k in ['es_id','source','release','table_or_object','variable_or_indicator','source_geo_id','source_geo_label','year_or_interval','valid_count','missing_count','native_status_flags','country_grain','match_basis','roster_iso3','roster_match','notes']] for x in C])
write_tsv('DIMENSION_MAP_RAS.tsv',['es_id','requested_dimension','source','release','table_or_object','variables_or_selector','definition','units_or_universe','date_semantics','geography_semantics','coverage_ref','direct_proxy_absent','known_limitation','evidence_ref'],[[x.get(k,'') for k in ['es_id','requested_dimension','source','release','table_or_object','variables_or_selector','definition','units_or_universe','date_semantics','geography_semantics','coverage_ref','direct_proxy_absent','known_limitation','evidence_ref']] for x in D])
