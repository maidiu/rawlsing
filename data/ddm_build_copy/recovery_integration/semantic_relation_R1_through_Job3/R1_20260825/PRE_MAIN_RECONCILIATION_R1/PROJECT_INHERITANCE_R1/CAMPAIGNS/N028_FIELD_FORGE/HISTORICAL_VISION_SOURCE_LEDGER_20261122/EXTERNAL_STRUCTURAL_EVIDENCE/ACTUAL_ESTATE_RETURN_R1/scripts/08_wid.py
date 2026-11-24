import sys, zipfile, io, csv, collections
from pathlib import Path
sys.path.insert(0,'/Users/matthewsmith/Desktop/FIELD_FORGE_EXTERNAL_ESTATE_RETURN_R1/scripts')
from lib import *
import pycountry
T=[]; V=[]; VC=[]; C=[]; D=[]
arc=ROOT/'WORLD_INEQUALITY_DATABASE/archive/wid_all_data.zip'
z=zipfile.ZipFile(arc)
names=z.namelist()
data_members=sorted(n for n in names if n.startswith('WID_data_') and n.endswith('.csv'))
meta_members=sorted(n for n in names if n.startswith('WID_metadata_') and n.endswith('.csv'))
countries_txt=z.read('WID_countries.csv').decode('utf-8-sig')
countries=list(csv.DictReader(io.StringIO(countries_txt),delimiter=';'))
cmap={r['alpha2']:r for r in countries}
# archive table
T.append(dict(source='WID',es_id='ES11',release='WID bulk 2026-11-20',table_or_object='wid_all_data.zip',relative_path=str(arc.relative_to(ROOT)),format='zip',rows=len(names),columns='',grain='archive of country-level data and metadata CSV files',key_columns='country alpha2 in filename; country+variable+percentile+year in data',units='mixed; see metadata unit',universe='347 country/region data files plus 347 metadata files, WID_countries, README',dates='data-dependent; metadata source/method fields',geography='WID country/region alpha2 codes; includes historical, subnational and regional aggregates',docs='WID_bulk_README.md; WID_codes_dictionary.html; DINA_Guidelines_2025.pdf',read_status='INSPECTED_ARCHIVE_STREAM',notes='Archive was inspected member-by-member without permanent extraction. 696 members; 347 data + 347 metadata + WID_countries + README.'))
T.append(dict(source='WID',es_id='ES11',release='WID bulk 2026-11-20',table_or_object='WID_countries.csv',relative_path=str(arc.relative_to(ROOT)),format='csv (zip member)',rows=len(countries),columns=len(countries[0]),grain='country/region code',key_columns='alpha2',units='codes and labels',universe=f'{len(countries)} WID codes',dates='not applicable',geography='global with historical/subnational/regional additions',docs='WID_bulk_README.md',read_status='INSPECTED',notes='Semicolon delimiter; alpha2, titlename, shortname, region, region2.'))
# variable schema
data_schema=[('country','WID country/region code'),('variable','WID variable code'),('percentile','percentile or group code'),('year','year'),('value','value in unit named by metadata'),('age','age-group code'),('pop','population-unit code'),('data_quality','data-quality flag as recorded')]
meta_schema=[('country','WID country/region code'),('variable','WID variable code'),('age','age-group code'),('pop','population-unit code'),('countryname','country/region name'),('shortname','series short name'),('simpledes','plain-language description'),('technicaldes','technical/accounting description'),('shorttype','series type short label'),('longtype','series type long label'),('shortpop','population-unit short label'),('longpop','population-unit long label'),('shortage','age-group short label'),('longage','age-group long label'),('unit','unit of value'),('source','source references'),('method','estimation method text'),('avg_quality','average quality flag')]
for c,l in data_schema: V.append(dict(source='WID',es_id='ES11',release='WID bulk 2026-11-20',table_or_object='WID_data_XX.csv',variable=c,label_or_definition=l,storage_type='text/numeric',role='key' if c in ('country','variable','percentile','year') else 'selected_dimension',value_label_present='no',unit_or_scale=('percentile/pop/age code' if c in ('percentile','pop','age') else ''),classification_or_denominator='',missing_or_special_states='empty value or absent row; data_quality flag where present',docs_ref='WID_bulk_README.md',availability='observed',profile_scope='complete_metadata_census',notes=''))
for c,l in meta_schema: V.append(dict(source='WID',es_id='ES11',release='WID bulk 2026-11-20',table_or_object='WID_metadata_XX.csv',variable=c,label_or_definition=l,storage_type='text',role='selected_dimension' if c in ('variable','percentile','pop','age','unit','source','method','avg_quality') else 'metadata',value_label_present='no',unit_or_scale='',classification_or_denominator='',missing_or_special_states='empty metadata field',docs_ref='WID_bulk_README.md',availability='observed',profile_scope='complete_metadata_census',notes=''))
# selected series
sel={
 ('sptinc992j','p90p100'):('Pre-tax national income top 10% share','share'),
 ('sptinc992j','p99p100'):('Pre-tax national income top 1% share','share'),
 ('shweal992j','p90p100'):('Net personal wealth top 10% share','share'),
 ('shweal992j','p99p100'):('Net personal wealth top 1% share','share'),
 ('aptinc992j','p0p100'):('Average pre-tax national income, all adults','average local currency'),
 ('ahweal992j','p0p100'):('Average net personal wealth, all adults','average local currency'),
 ('spllin992j','p90p100'):('Pre-tax labor income top 10% share','share'),
 ('spkkin992j','p90p100'):('Pre-tax capital income top 10% share','share'),
 ('tptinc992j','p99p100'):('Pre-tax national income top 1% threshold','threshold local currency'),
}
for (var,perc),(lab,unit) in sel.items():
    V.append(dict(source='WID',es_id='ES11',release='WID bulk 2026-11-20',table_or_object='selected series',variable=var,label_or_definition=f'{lab}; percentile={perc}',storage_type='numeric',role='selected_dimension',value_label_present='no',unit_or_scale=unit,classification_or_denominator='adults, equal-split where pop=j; see metadata',missing_or_special_states='row absent or empty; data_quality flag',docs_ref='WID metadata; DINA guidelines',availability='observed' if var in ('sptinc992j','shweal992j','aptinc992j','ahweal992j') else 'partial',profile_scope='selected_dimensions',notes=''))
    VC.append(dict(source='WID',es_id='ES11',release='WID bulk 2026-11-20',table_or_object='selected series',variable=var,code=perc,label=lab,missing_or_special='',docs_ref='WID_bulk_README.md; WID codes dictionary',used_in_selected_dimension='yes'))
for code,label in [('p0p100','all'),('p90p100','top 10%'),('p99p100','top 1%')]:
    VC.append(dict(source='WID',es_id='ES11',release='WID bulk 2026-11-20',table_or_object='selected series',variable='percentile',code=code,label=label,missing_or_special='',docs_ref='WID_bulk_README.md',used_in_selected_dimension='yes'))
for code,label in [('992','adults'),('999','all ages')]: VC.append(dict(source='WID',es_id='ES11',release='WID bulk 2026-11-20',table_or_object='selected series',variable='age',code=code,label=label,missing_or_special='',docs_ref='WID_bulk_README.md',used_in_selected_dimension='yes'))
for code,label in [('j','equal-split adults'),('i','individuals')]: VC.append(dict(source='WID',es_id='ES11',release='WID bulk 2026-11-20',table_or_object='selected series',variable='pop',code=code,label=label,missing_or_special='',docs_ref='WID_bulk_README.md',used_in_selected_dimension='yes'))
# scan data
obs=collections.defaultdict(list); meta=collections.defaultdict(dict)
for n in data_members:
    code=n[len('WID_data_'):-4]
    with z.open(n) as f:
        r=csv.DictReader(io.TextIOWrapper(f,encoding='utf-8'),delimiter=';')
        for row in r:
            key=(row.get('variable'),row.get('percentile'))
            if key in sel and row.get('value','')!='':
                try: yr=int(float(row.get('year')))
                except Exception: continue
                obs[(code,)+key].append((yr,row.get('value'),row.get('data_quality',''),row.get('age',''),row.get('pop','')))
for n in meta_members:
    code=n[len('WID_metadata_'):-4]
    with z.open(n) as f:
        r=csv.DictReader(io.TextIOWrapper(f,encoding='utf-8'),delimiter=';')
        for row in r:
            key=(row.get('variable'),)
            if row.get('variable') in {v for v,p in sel}:
                meta[(code,row.get('variable'))]=row
# coverage rows
for code in sorted(set([k[0] for k in obs]+list(cmap.keys()))):
    c=cmap.get(code,{})
    iso=None
    if len(code)==2:
        cc=pycountry.countries.get(alpha_2=code); iso=cc.alpha_3 if cc else None
    for (var,perc),(lab,unit) in sel.items():
        vals=obs.get((code,var,perc),[])
        if not vals: continue
        ys=[v[0] for v in vals]; qualities=sorted(set(v[2] for v in vals if v[2]!=''))
        C.append(dict(es_id='ES11',source='WID',release='WID bulk 2026-11-20',table_or_object=f'WID_data_{code}.csv',variable_or_indicator=f'{var}:{perc}',source_geo_id=code,source_geo_label=c.get('shortname',''),year_or_interval=ranges(ys),valid_count=len(vals),missing_count=0,native_status_flags='data_quality='+','.join(qualities),country_grain='country/region-year',match_basis='iso2_to_iso3' if iso else 'non_iso_or_subnational',roster_iso3=iso or '',roster_match=('exact' if iso in ROSTER else 'not_in_roster') if iso else 'not_iso3',notes=f'age_values={sorted(set(v[3] for v in vals))}; pop_values={sorted(set(v[4] for v in vals))}; unit={unit}'))
D.append(dict(es_id='ES11',requested_dimension='Income and wealth distribution, top shares, labor vs capital income, levels and material position gradients',source='WID',release='WID bulk 2026-11-20',table_or_object='WID_data_XX.csv + WID_metadata_XX.csv',variables_or_selector='sptinc992j p90p100; sptinc992j p99p100; shweal992j p90p100; shweal992j p99p100; aptinc992j p0p100; ahweal992j p0p100; spllin992j p90p100; spkkin992j p90p100; tptinc992j p99p100',definition='country/region-year distributional national accounts series by variable, percentile, age and population unit',units_or_universe='shares, local-currency averages/thresholds, metadata unit per country; adults/equal-split where specified',date_semantics='year field; historical and current estimates mixed; metadata source/method per series',geography_semantics='WID alpha2 codes; historical, subnational and regional aggregates retained separately',coverage_ref='COVERAGE_WID.tsv',direct_proxy_absent='direct distributional estimate, not individual income or class membership',known_limitation='no top percentile=ruling class; no invented precise income from self-reported bracket; avoid mixing unit/age/price/PPP/definition; estimate quality explicit',evidence_ref='WID archive data and metadata streamed and inspected'))
write_tsv('TABLES_WID.tsv',['source','es_id','release','table_or_object','relative_path','format','rows','columns','grain','key_columns','units','universe','dates','geography','docs','read_status','notes'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','relative_path','format','rows','columns','grain','key_columns','units','universe','dates','geography','docs','read_status','notes']] for x in T])
write_tsv('VARIABLES_WID.tsv',['source','es_id','release','table_or_object','variable','label_or_definition','storage_type','role','value_label_present','unit_or_scale','classification_or_denominator','missing_or_special_states','docs_ref','availability','profile_scope','notes'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','variable','label_or_definition','storage_type','role','value_label_present','unit_or_scale','classification_or_denominator','missing_or_special_states','docs_ref','availability','profile_scope','notes']] for x in V])
write_tsv('VALUE_CODES_WID.tsv',['source','es_id','release','table_or_object','variable','code','label','missing_or_special','docs_ref','used_in_selected_dimension'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','variable','code','label','missing_or_special','docs_ref','used_in_selected_dimension']] for x in VC])
write_tsv('COVERAGE_WID.tsv',['es_id','source','release','table_or_object','variable_or_indicator','source_geo_id','source_geo_label','year_or_interval','valid_count','missing_count','native_status_flags','country_grain','match_basis','roster_iso3','roster_match','notes'],[[x.get(k,'') for k in ['es_id','source','release','table_or_object','variable_or_indicator','source_geo_id','source_geo_label','year_or_interval','valid_count','missing_count','native_status_flags','country_grain','match_basis','roster_iso3','roster_match','notes']] for x in C])
write_tsv('DIMENSION_MAP_WID.tsv',['es_id','requested_dimension','source','release','table_or_object','variables_or_selector','definition','units_or_universe','date_semantics','geography_semantics','coverage_ref','direct_proxy_absent','known_limitation','evidence_ref'],[[x.get(k,'') for k in ['es_id','requested_dimension','source','release','table_or_object','variables_or_selector','definition','units_or_universe','date_semantics','geography_semantics','coverage_ref','direct_proxy_absent','known_limitation','evidence_ref']] for x in D])
print('WID data members scanned',len(data_members),'coverage rows',len(C))
