import sys, csv, json, re
from pathlib import Path
sys.path.insert(0,'/Users/matthewsmith/Desktop/FIELD_FORGE_EXTERNAL_ESTATE_RETURN_R1/scripts')
from lib import *

T=[]; V=[]; VC=[]; C=[]; D=[]
def add_table(**kw): T.append(kw)
def add_var(**kw): V.append(kw)
def add_code(**kw): VC.append(kw)
def add_cov(**kw): C.append(kw)
def add_dim(**kw): D.append(kw)

def csv_rows(p):
 with open(p,encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def csv_header(p):
 with open(p,encoding='utf-8-sig',newline='') as f: return next(csv.reader(f))
def years_from_intervals(rows):
 ys=set()
 for r in rows:
  try:
   a=int(float(r['from'])); b=int(float(r['to']))
   if b-a>500: continue
   ys.update(range(a,b+1))
  except Exception: pass
 return ys

core21=ROOT/'EPR_DATASET_FAMILY/2021/core/EPR-2021.csv'
core23=ROOT/'EPR_DATASET_FAMILY/2023_beta/core/EPR-2023.csv'
geo21=ROOT/'EPR_DATASET_FAMILY/2021/geoepr/GeoEPR-2021.geojson'
geo23=ROOT/'EPR_DATASET_FAMILY/2023_beta/geoepr/GeoEPR-2023.geojson'
ed21=ROOT/'EPR_DATASET_FAMILY/2021/ed/ED-2021.csv'
ed23=ROOT/'EPR_DATASET_FAMILY/2023_beta/ed/ED-2023.csv'
tek21=ROOT/'EPR_DATASET_FAMILY/2021/tek/TEK-2021.csv'
tek23=ROOT/'EPR_DATASET_FAMILY/2023_beta/tek/TEK-2023.csv'

core_labels={'gwid':'Gleditsch-Ward country id','statename':'State name','from':'First year of group period','to':'Last year of group period','group':'Politically relevant group name','groupid':'EPR group id within country','gwgroupid':'Gleditsch-Ward group id','umbrella':'Umbrella group flag','size':'Group population share of country population','status':'Executive-level political status','reg_aut':'Regional autonomy coding'}
core_types={k:'integer' if k in ('gwid','from','to','groupid','gwgroupid') else ('numeric_fraction' if k=='size' else 'string') for k in core_labels}
geo_labels={'gwid':'Gleditsch-Ward country id','statename':'State name','from':'First year of settlement period','to':'Last year of settlement period','group':'Group name','groupid':'EPR group id','gwgroupid':'Gleditsch-Ward group id','umbrella':'Umbrella group flag','sqkm':'Group settlement area in square kilometres','type':'Settlement pattern category','the_geom':'WKT geometry (SRID 4326) in CSV; GeoJSON geometry in GeoJSON'}
ed_labels={'gwid':'Gleditsch-Ward country id','gwgroupid':'Gleditsch-Ward group id','religion1':'Largest religion category','rel1_size':'Share of group in religion1','religion2':'Second religion category','rel2_size':'Share of group in religion2','religion3':'Third religion category','rel3_size':'Share of group in religion3','language1':'Largest language category','lang1_size':'Share of group in language1','language2':'Second language category','lang2_size':'Share of group in language2','language3':'Third language category','lang3_size':'Share of group in language3','phenotype1':'Largest racial/phenotype category','pheno1_size':'Share of group in phenotype1','phenotype2':'Second racial/phenotype category','pheno2_size':'Share of group in phenotype2','phenotype3':'Third racial/phenotype category','pheno3_size':'Share of group in phenotype3'}
tek_labels={'tekid':'Transborder ethnic kin group id','gwid':'Gleditsch-Ward country id','statename':'State name','gwgroupid':'Gleditsch-Ward group id','groupname':'Group name'}

for rel,tag,rows in [('2021','2021',core21),('2023_beta','2023 beta',core23)]:
 hdr=csv_header(rows); rr=csv_rows(rows)
 add_table(source='EPR',es_id='ES01',release=rel,table_or_object='EPR Core country-year group table',relative_path=str(rows.relative_to(ROOT)),format='csv',rows=len(rr),columns=len(hdr),grain='country-group-period (interval from/to); one row per group period',key_columns='gwid + gwgroupid + from + to',units='size is population share; dates are years',universe='politically relevant ethnic groups, not all ethnic categories',dates=f"{min(int(x['from']) for x in rr)}-{max(int(x['to']) for x in rr)}",geography=f"{len(set(x['statename'] for x in rr))} state names",docs='EPR_2021_Codebook_EPR.pdf; EPR 2023 beta page (codebook 404)',read_status='INSPECTED',notes='')
 for v,lab in core_labels.items():
  add_var(source='EPR',es_id='ES01',release=rel,table_or_object='EPR Core',variable=v,label_or_definition=lab,storage_type=core_types[v],role='selected_dimension' if v in ('size','status','umbrella','reg_aut','from','to') else ('key' if v in ('gwid','gwgroupid','groupid') else 'metadata'),value_label_present='yes' if v in ('status','umbrella','reg_aut') else 'no',unit_or_scale='fraction' if v=='size' else ('year' if v in ('from','to') else ('category' if v=='status' else 'identifier or text')),classification_or_denominator='country population' if v=='size' else '',missing_or_special_states='empty string observed in CSV; codebook must be consulted for structural absence',docs_ref='EPR Core codebook / EPR pages',availability='observed',profile_scope='complete_metadata_census',notes='')
 for v in ('status','umbrella','reg_aut'):
  vals=sorted(set(x[v] for x in rr if x[v]!=''))
  for x in vals:
   add_code(source='EPR',es_id='ES01',release=rel,table_or_object='EPR Core',variable=v,code=x,label=x,missing_or_special='no',docs_ref='EPR Core codebook',used_in_selected_dimension='yes')
 # coverage core
 for var in ('size','status','reg_aut','umbrella'):
  for country,g in __import__('itertools').groupby(sorted(rr,key=lambda r:r['statename']),key=lambda r:r['statename']):
   g=list(g); vals=[x[var] for x in g]; valid=sum(1 for x in vals if x!=''); iso=iso3(country)
   ys=years_from_intervals(g)
   add_cov(es_id='ES01',source='EPR',release=rel,table_or_object='EPR Core',variable_or_indicator=var,source_geo_id=country,source_geo_label=country,year_or_interval=ranges(ys),valid_count=valid,missing_count=len(vals)-valid,native_status_flags='interval rows',country_grain='state',match_basis='name_to_iso3',roster_iso3=iso or '',roster_match='exact' if iso in ROSTER else ('unmatched' if not iso else 'not_in_roster'),notes=f'group_period_rows={len(g)}')
 # DIMENSION_MAP
 add_dim(es_id='ES01',requested_dimension='Group population fraction, executive access/status and exclusion, entry/exit and changes',source='EPR Core',release=rel,table_or_object='EPR Core',variables_or_selector='size; status; umbrella; reg_aut; from; to; gwgroupid',definition='size = group population share; status = executive-level political status; from/to = inclusive year interval; reg_aut = regional autonomy',units_or_universe='group share of country population; politically relevant groups',date_semantics='inclusive year interval, not observation/publication date',geography_semantics='EPR state name and GW id; historical states included',coverage_ref='COVERAGE.tsv ES01',direct_proxy_absent='direct',known_limitation='politically relevant group universe, not census all ethnicity; power status not individual beliefs; 2021 and 2023 beta separate',evidence_ref='EPR Core codebook and CSV header; actual file inspected')

for rel,tag,path in [('2021','2021',geo21),('2023_beta','2023 beta',geo23)]:
 d=json.load(open(path)); feats=d['features']
 y=('2021' if rel=='2021' else '2023')
 hdr=csv_header(ROOT/f'EPR_DATASET_FAMILY/{rel}/geoepr/GeoEPR-{y}.csv')
 add_table(source='EPR',es_id='ES02',release=rel,table_or_object='GeoEPR feature collection',relative_path=str(path.relative_to(ROOT)),format='geojson',rows=len(feats),columns=len(feats[0]['properties'])+1,grain='group settlement period',key_columns='gwid + gwgroupid + from + to',units='sqkm; geometry WGS84',universe='GeoEPR polygons for politically relevant groups',dates=f"{min(int(f['properties']['from']) for f in feats)}-{max(int(f['properties']['to']) for f in feats)}",geography=f"{len(set(f['properties']['statename'] for f in feats))} state names",docs='EPR_2021_Codebook_GeoEPR.pdf; GeoEPR-2023 page (codebook 404)',read_status='INSPECTED',notes='GeoJSON has no explicit crs member; coordinates are longitude/latitude WGS84 per dataset documentation; geometry validity not computed because no geometry engine is installed')
 for v,lab in geo_labels.items():
  add_var(source='EPR',es_id='ES02',release=rel,table_or_object='GeoEPR',variable=v,label_or_definition=lab,storage_type='geometry' if v=='the_geom' else ('numeric' if v=='sqkm' else 'string'),role='selected_dimension' if v in ('type','sqkm','from','to','the_geom') else ('key' if v in ('gwid','gwgroupid','groupid') else 'metadata'),value_label_present='no',unit_or_scale='sqkm' if v=='sqkm' else ('year' if v in ('from','to') else ('WGS84 geometry' if v=='the_geom' else 'identifier or text')),classification_or_denominator='',missing_or_special_states='the_geom may be absent for non-polygon settlement patterns; null geometry counted below',docs_ref='GeoEPR codebook / official GeoEPR page',availability='observed',profile_scope='complete_metadata_census',notes='')
 # value codes for settlement type
 for x in sorted(set(f['properties']['type'] for f in feats)):
  add_code(source='EPR',es_id='ES02',release=rel,table_or_object='GeoEPR',variable='type',code=x,label=x,missing_or_special='no',docs_ref='GeoEPR codebook',used_in_selected_dimension='yes')
 geom_types={}; null=0
 for f in feats:
  g=f.get('geometry')
  if g is None: null+=1
  else: geom_types[g.get('type')]=geom_types.get(g.get('type'),0)+1
 for country,g in __import__('itertools').groupby(sorted(feats,key=lambda f:f['properties']['statename']),key=lambda f:f['properties']['statename']):
  g=list(g); iso=iso3(country); ys=set()
  for f in g:
   try: ys.update(range(int(f['properties']['from']),int(f['properties']['to'])+1))
   except Exception: pass
  metrics={
   'feature': (len(g),0),
   'geometry': (sum(1 for f in g if f.get('geometry') is not None), sum(1 for f in g if f.get('geometry') is None)),
   'sqkm': (sum(1 for f in g if str(f['properties'].get('sqkm','')) not in ('','None')), sum(1 for f in g if str(f['properties'].get('sqkm','')) in ('','None'))),
   'type': (sum(1 for f in g if str(f['properties'].get('type','')) not in ('','None')), sum(1 for f in g if str(f['properties'].get('type','')) in ('','None'))),
  }
  for var,(valid,missing) in metrics.items():
   add_cov(es_id='ES02',source='EPR',release=rel,table_or_object='GeoEPR',variable_or_indicator=var,source_geo_id=country,source_geo_label=country,year_or_interval=ranges(ys),valid_count=valid,missing_count=missing,native_status_flags=f'geometry_types={geom_types}; null_geometry={null}',country_grain='state',match_basis='name_to_iso3',roster_iso3=iso or '',roster_match='exact' if iso in ROSTER else ('unmatched' if not iso else 'not_in_roster'),notes='')
 add_dim(es_id='ES02',requested_dimension='Group settlement geometry, settlement type, spatial relation and period',source='GeoEPR',release=rel,table_or_object='GeoEPR',variables_or_selector='type; sqkm; the_geom/GeoJSON geometry; from; to; gwgroupid',definition='settlement pattern category and polygon/multipolygon geometry in WGS84',units_or_universe='sqkm; politically relevant group polygons',date_semantics='inclusive settlement period; geometry is one static feature per period',geography_semantics='state name and group id; changing borders retained as source features',coverage_ref='COVERAGE.tsv ES02',direct_proxy_absent='direct geometry, not population counts or local dominance',known_limitation='geometry not population; no density, no overlays; overlaps and missing geometry remain source-native; CRS not explicitly declared in GeoJSON',evidence_ref='GeoJSON feature inspection')

core_map={}
for r in csv_rows(core21): core_map.setdefault(r['gwid'],r['statename'])
for rel,path in [('2021',ed21),('2023_beta',ed23)]:
 hdr=csv_header(path); rr=csv_rows(path)
 add_table(source='EPR',es_id='ES03',release=rel,table_or_object='EPR-ED group dimensions',relative_path=str(path.relative_to(ROOT)),format='csv',rows=len(rr),columns=len(hdr),grain='country-group (time-invariant within EPR group)',key_columns='gwid + gwgroupid',units='share of group in category',universe='politically relevant groups',dates='no year field in this table',geography=f"{len(set(x['gwid'] for x in rr))} gwid values",docs='EPR_2021_Codebook_ED.pdf',read_status='INSPECTED',notes='ED-2021 and ED-2023 CSV are byte-identical in local custody; 2023 beta did not change ED content')
 for v,lab in ed_labels.items():
  add_var(source='EPR',es_id='ES03',release=rel,table_or_object='EPR-ED',variable=v,label_or_definition=lab,storage_type='numeric_share' if v.endswith('_size') else 'string',role='selected_dimension' if v.endswith('_size') or v in ('religion1','language1','phenotype1') else 'metadata',value_label_present='no',unit_or_scale='share of group' if v.endswith('_size') else 'category code',classification_or_denominator='group population where share is recorded',missing_or_special_states='empty category and 0 share observed; no explicit missing code',docs_ref='ED codebook',availability='observed',profile_scope='complete_metadata_census',notes='')
 for v in ['rel1_size','rel2_size','rel3_size','lang1_size','lang2_size','lang3_size','pheno1_size','pheno2_size','pheno3_size']:
  for country,g in __import__('itertools').groupby(sorted(rr,key=lambda r:r['gwid']),key=lambda r:r['gwid']):
   g=list(g); vals=[x[v] for x in g]; valid=sum(1 for x in vals if x!='')
   cname=core_map.get(country,'')
   iso=iso3(cname) if cname else None
   add_cov(es_id='ES03',source='EPR',release=rel,table_or_object='EPR-ED',variable_or_indicator=v,source_geo_id=country,source_geo_label=cname,year_or_interval='no year field',valid_count=valid,missing_count=len(vals)-valid,native_status_flags='empty string treated as absent; valid zero preserved',country_grain='state',match_basis='gwid_to_core_state',roster_iso3=iso or '',roster_match='exact' if iso in ROSTER else ('unmatched' if not iso else 'not_in_roster'),notes='')
 add_dim(es_id='ES03',requested_dimension='Linguistic, religious and racial group composition and segment shares',source='EPR-ED',release=rel,table_or_object='EPR-ED',variables_or_selector='religion1-3; rel1_size-rel3_size; language1-3; lang1_size-lang3_size; phenotype1-3; pheno1_size-pheno3_size',definition='group-level categorical dimensions and shares where recorded',units_or_universe='share of group; politically relevant groups',date_semantics='no time field; time is inherited from EPR group identity',geography_semantics='gwid/gwgroupid; no separate country name',coverage_ref='COVERAGE.tsv ES03',direct_proxy_absent='direct categorical composition, not individual identity',known_limitation='dimensions not interchangeable; name/code crosswalk to EPR/TEK required; 2023 ED identical to 2021',evidence_ref='ED CSV header and codebook')

for rel,path in [('2021',tek21),('2023_beta',tek23)]:
 hdr=csv_header(path); rr=csv_rows(path)
 add_table(source='EPR',es_id='ES04',release=rel,table_or_object='EPR-TEK link table',relative_path=str(path.relative_to(ROOT)),format='csv',rows=len(rr),columns=len(hdr),grain='TEK-group to country-group link',key_columns='tekid + gwid + gwgroupid',units='link identifiers',universe='transborder ethnic kin groups',dates='no year field in this table',geography=f"{len(set(x['statename'] for x in rr))} state names",docs='EPR_2021_Codebook_TEK.pdf; TEK_Atlas_2021.pdf; 2023 codebook/atlas 404',read_status='INSPECTED',notes='')
 for v,lab in tek_labels.items():
  add_var(source='EPR',es_id='ES04',release=rel,table_or_object='EPR-TEK',variable=v,label_or_definition=lab,storage_type='integer' if v in ('tekid','gwid','gwgroupid') else 'string',role='selected_dimension' if v in ('tekid','gwgroupid','groupname') else 'key',value_label_present='no',unit_or_scale='identifier',classification_or_denominator='',missing_or_special_states='no explicit missing code',docs_ref='TEK codebook',availability='observed',profile_scope='complete_metadata_census',notes='')
 for country,g in __import__('itertools').groupby(sorted(rr,key=lambda r:r['statename']),key=lambda r:r['statename']):
  g=list(g); iso=iso3(country)
  for var in ('tekid','gwgroupid','groupname'):
   add_cov(es_id='ES04',source='EPR',release=rel,table_or_object='EPR-TEK',variable_or_indicator=var,source_geo_id=country,source_geo_label=country,year_or_interval='no year field',valid_count=sum(1 for x in g if str(x.get(var,'')) not in ('','None')),missing_count=sum(1 for x in g if str(x.get(var,'')) in ('','None')),native_status_flags='',country_grain='state',match_basis='name_to_iso3',roster_iso3=iso or '',roster_match='exact' if iso in ROSTER else ('unmatched' if not iso else 'not_in_roster'),notes='')
 add_dim(es_id='ES04',requested_dimension='Transborder ethnic kin links and kin sets',source='EPR-TEK',release=rel,table_or_object='EPR-TEK',variables_or_selector='tekid; gwid; gwgroupid; groupname; statename',definition='nominal link between groups sharing an ethnographic name across states',units_or_universe='group link, not population flow',date_semantics='no year field in table; TEK Atlas provides group descriptions',geography_semantics='state and group identifiers',coverage_ref='COVERAGE.tsv ES04',direct_proxy_absent='direct link, not migration/flow/alliance/contact',known_limitation='kin link not migration, money flow, alliance, contact or solidarity; TEK 2023 Atlas unavailable',evidence_ref='TEK CSV and 2021 Atlas')

# reserve shallow tables
for rel,sub in [('2021','2021'),('2023_beta','2023_beta')]:
 for fam,esid in [('acd2epr','RESERVE_ACD2EPR'),('er','RESERVE_EPR_ER')]:
  for p in sorted((ROOT/'EPR_DATASET_FAMILY'/rel/sub).glob('*.csv')):
   rr=csv_rows(p); hdr=csv_header(p)
   add_table(source='EPR',es_id=esid,release=rel,table_or_object=p.stem,relative_path=str(p.relative_to(ROOT)),format='csv',rows=len(rr),columns=len(hdr),grain='reserve; not profiled',key_columns='',units='reserve',universe='reserve',dates='reserve',geography='reserve',docs='reserve',read_status='INSPECTED_SCHEMA_ONLY',notes='Reserve family; only file presence and shape inspected, no deep profiling')
for p in sorted((ROOT/'EPR_DATASET_FAMILY/AG').glob('*')):
 if p.suffix in ('.csv','.geojson'):
  if p.suffix=='.csv':
   rr=csv_rows(p); n=len(rr); cols=len(csv_header(p)); fmt='csv'
  else:
   d=json.load(open(p)); n=len(d.get('features',[])); cols=len(d['features'][0]['properties']) if d.get('features') else 0; fmt='geojson'
  add_table(source='EPR',es_id='RESERVE_EPR_AG',release='AG',table_or_object=p.name,relative_path=str(p.relative_to(ROOT)),format=fmt,rows=n,columns=cols,grain='reserve; not profiled',key_columns='',units='reserve',universe='reserve',dates='reserve',geography='reserve',docs='AG page',read_status='INSPECTED_SCHEMA_ONLY',notes='Aggregate Group extension; reserve')

write_tsv('TABLES_EPR.tsv',['source','es_id','release','table_or_object','relative_path','format','rows','columns','grain','key_columns','units','universe','dates','geography','docs','read_status','notes'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','relative_path','format','rows','columns','grain','key_columns','units','universe','dates','geography','docs','read_status','notes']] for x in T])
write_tsv('VARIABLES_EPR.tsv',['source','es_id','release','table_or_object','variable','label_or_definition','storage_type','role','value_label_present','unit_or_scale','classification_or_denominator','missing_or_special_states','docs_ref','availability','profile_scope','notes'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','variable','label_or_definition','storage_type','role','value_label_present','unit_or_scale','classification_or_denominator','missing_or_special_states','docs_ref','availability','profile_scope','notes']] for x in V])
write_tsv('VALUE_CODES_EPR.tsv',['source','es_id','release','table_or_object','variable','code','label','missing_or_special','docs_ref','used_in_selected_dimension'],[[x.get(k,'') for k in ['source','es_id','release','table_or_object','variable','code','label','missing_or_special','docs_ref','used_in_selected_dimension']] for x in VC])
write_tsv('COVERAGE_EPR.tsv',['es_id','source','release','table_or_object','variable_or_indicator','source_geo_id','source_geo_label','year_or_interval','valid_count','missing_count','native_status_flags','country_grain','match_basis','roster_iso3','roster_match','notes'],[[x.get(k,'') for k in ['es_id','source','release','table_or_object','variable_or_indicator','source_geo_id','source_geo_label','year_or_interval','valid_count','missing_count','native_status_flags','country_grain','match_basis','roster_iso3','roster_match','notes']] for x in C])
write_tsv('DIMENSION_MAP_EPR.tsv',['es_id','requested_dimension','source','release','table_or_object','variables_or_selector','definition','units_or_universe','date_semantics','geography_semantics','coverage_ref','direct_proxy_absent','known_limitation','evidence_ref'],[[x.get(k,'') for k in ['es_id','requested_dimension','source','release','table_or_object','variables_or_selector','definition','units_or_universe','date_semantics','geography_semantics','coverage_ref','direct_proxy_absent','known_limitation','evidence_ref']] for x in D])
