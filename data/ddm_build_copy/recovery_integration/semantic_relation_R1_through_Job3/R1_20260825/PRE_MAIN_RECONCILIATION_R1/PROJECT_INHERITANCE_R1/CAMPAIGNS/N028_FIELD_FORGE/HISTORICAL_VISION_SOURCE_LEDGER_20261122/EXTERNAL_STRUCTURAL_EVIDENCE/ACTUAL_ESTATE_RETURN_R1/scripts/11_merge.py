import csv, glob, re, collections
from pathlib import Path
OUT=Path('/Users/matthewsmith/Desktop/FIELD_FORGE_EXTERNAL_ESTATE_RETURN_R1')
def merge(prefix, out, pattern):
    files=sorted(f for f in OUT.glob(pattern) if f.name not in (out,'COVERAGE_SUMMARY.tsv'))
    header=None; rows=[]
    for f in files:
        with open(f,newline='') as fh:
            r=csv.reader(fh,delimiter='\t')
            try: h=next(r)
            except StopIteration: continue
            if header is None: header=h
            elif h!=header: print('HEADER MISMATCH',f)
            rows.extend(r)
    with open(OUT/out,'w',newline='') as fh:
        w=csv.writer(fh,delimiter='\t'); w.writerow(header); w.writerows(rows)
    print(out,len(rows))
merge('TABLES','TABLES.tsv','TABLES_*.tsv')
merge('VARIABLES','VARIABLES.tsv','VARIABLES_*.tsv')
merge('VALUE_CODES','VALUE_CODES.tsv','VALUE_CODES_*.tsv')
merge('COVERAGE','COVERAGE.tsv','COVERAGE_*.tsv')
merge('DIMENSION_MAP','DIMENSION_MAP.tsv','DIMENSION_MAP_*.tsv')

# summary and matrix
rows=list(csv.DictReader(open(OUT/'COVERAGE.tsv'),delimiter='\t'))
def years(s):
    out=set()
    for part in re.split(r'[;,]\s*',s):
        m=re.match(r'(\d{4})(?:-(\d{4}))?$',part.strip())
        if m:
            a=int(m.group(1)); b=int(m.group(2) or a); out.update(range(a,b+1))
    return out
summ=collections.OrderedDict()
matrix=collections.defaultdict(set)
for r in rows:
    k=(r['es_id'],r['source'],r['release'])
    d=summ.setdefault(k,{'indicators':set(),'geos':set(),'match':set(),'unmatched':set(),'native_only':set(),'years':set(),'valid':0,'missing':0})
    d['indicators'].add(r['variable_or_indicator']); d['geos'].add(r['source_geo_id']); d['valid']+=int(r['valid_count'] or 0); d['missing']+=int(r['missing_count'] or 0); d['years'] |= years(r['year_or_interval'])
    if r['roster_match']=='exact' and r['roster_iso3']: d['match'].add(r['roster_iso3']); matrix[r['es_id']].add(r['roster_iso3'])
    elif r['roster_match'] in ('not_in_roster','not_iso3','aggregate'): d['native_only'].add(r['source_geo_id'])
    elif r['roster_match']=='unmatched': d['unmatched'].add(r['source_geo_id'])
with open(OUT/'COVERAGE_SUMMARY.tsv','w',newline='') as f:
    w=csv.writer(f,delimiter='\t'); w.writerow(['es_id','source','release','distinct_indicators','distinct_source_geos','roster_geos_matched','native_only_geos','unmatched_geos','year_min','year_max','total_valid','total_missing','notes'])
    for (es,src,rel),d in summ.items():
        ys=d['years']; w.writerow([es,src,rel,len(d['indicators']),len(d['geos']),len(d['match']),len(d['native_only']),len(d['unmatched']),min(ys) if ys else '',max(ys) if ys else '',d['valid'],d['missing'],''])
roster=[x.strip() for x in (Path('/Users/matthewsmith/Desktop/Rawlsing/source_files/COUNTRY_ROSTER_35_WAVES.txt')).read_text().splitlines() if x.strip()]
esids=[f'ES{i:02d}' for i in range(1,15)]
with open(OUT/'ROSTER_COVERAGE_MATRIX.tsv','w',newline='') as f:
    w=csv.writer(f,delimiter='\t'); w.writerow(['roster_iso3']+esids)
    for iso in roster: w.writerow([iso]+['1' if iso in matrix.get(es,set()) else '0' for es in esids])
print('summary',len(summ),'matrix',len(roster),'x',len(esids))
