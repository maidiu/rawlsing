#!/usr/bin/env python3
import os, sys, csv, hashlib, zipfile, io, json, time
from pathlib import Path
ROOT=Path('/Users/matthewsmith/Desktop/Rawlsing/source_files')
OUT=Path('/Users/matthewsmith/Desktop/FIELD_FORGE_EXTERNAL_ESTATE_RETURN_R1')

def sha256_file(p):
    h=hashlib.sha256(); n=0
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20), b''):
            h.update(b); n+=len(b)
    return h.hexdigest(), n

def magic(p):
    try:
        with open(p,'rb') as f: b=f.read(16)
    except Exception: return 'UNREADABLE'
    if b.startswith(b'%PDF-'): return 'PDF'
    if b.startswith(b'PK\x03\x04'): return 'ZIP'
    if b.startswith(b'\x1f\x8b'): return 'GZIP'
    if b.startswith(b'$FL2') or b.startswith(b'$FL3'): return 'SPSS_SAV'
    if b.startswith(b'<stata_dta>'): return 'STATA_DTA'
    if b[:1] in (b'{',b'['): return 'JSON_TEXT'
    if b.startswith(b'<!DOCTYPE') or b.startswith(b'<html'): return 'HTML_TEXT'
    if b.startswith(b'---') or b.startswith(b'#') or b.startswith(b'source;'): return 'TEXT'
    # heuristic text
    if all((x in b'\t\r\n' or 32<=x<127) for x in b[:16]): return 'TEXT'
    return 'BINARY'

def fmt_for(p, mg):
    s=p.suffix.lower()
    if s=='.pdf' or mg=='PDF': return 'pdf'
    if s in ('.xlsx','.xlsm'): return 'xlsx'
    if s=='.xls': return 'xls'
    if s=='.dta': return 'stata_dta'
    if s=='.sav': return 'spss_sav'
    if s in ('.rds',): return 'r_rds_gzip'
    if s in ('.rdata','.rda'): return 'r_rdata_gzip'
    if s in ('.zip',): return 'zip'
    if s=='.csv': return 'csv'
    if s=='.tsv': return 'tsv'
    if s=='.txt': return 'txt'
    if s=='.json': return 'json'
    if s=='.geojson': return 'geojson'
    if s=='.html': return 'html'
    if s=='.md': return 'markdown'
    if s=='.do': return 'stata_do'
    if s=='.pdf': return 'pdf'
    if mg=='GZIP': return 'gzip_unknown'
    if mg=='ZIP': return 'zip_unknown'
    return s.lstrip('.') or mg.lower()

def reader_for(fmt):
    return {'csv':'python csv','tsv':'python csv','txt':'text','json':'json','geojson':'json','xlsx':'openpyxl','xls':'unavailable_legacy_xls','dta':'pyreadstat','spss_sav':'pyreadstat','r_rds_gzip':'pyreadr','r_rdata_gzip':'pyreadr','zip':'zipfile','pdf':'header/mdls only (no PDF text extractor)','html':'text','markdown':'text','stata_do':'text'}.get(fmt,'unavailable')

def family_release_role(p):
    rel=p.relative_to(ROOT); parts=rel.parts; top=parts[0]
    if top=='EPR_DATASET_FAMILY.zip': return 'EPR_DATASET_FAMILY','archive mirror','archive','SUPPORT','EPR CC BY-NC-SA 4.0; see family README'
    if top=='Rawlsing 35 waves of savs & dtas.zip': return 'RAWLSING_35_WAVES','archive mirror','archive','ORIGINAL35_RESERVE','restricted/respondent-source terms; not exported'
    if top=='MICS_Datasets.zip': return 'MICS','reserve archive','reserve','RESERVE_MICS','restricted/respondent-source terms; not exported'
    if top=='EPR_DATASET_FAMILY': 
        fam='EPR_DATASET_FAMILY'
        if len(parts)>2 and parts[1] in ('2021','2023_beta'):
            reln=parts[1]
            sub=parts[2] if len(parts)>2 else ''
            if sub in ('core','geoepr','ed','tek','acd2epr','er'):
                es={'core':'ES01','geoepr':'ES02','ed':'ES03','tek':'ES04','acd2epr':'RESERVE_ACD2EPR','er':'RESERVE_EPR_ER'}[sub]
                role='selected_source' if es.startswith('ES') else 'reserve'
                return fam, f'{reln}/{sub}', role, es, 'EPR CC BY-NC-SA 4.0; see family README'
        if len(parts)>1 and parts[1]=='AG': return fam,'AG','reserve','RESERVE_EPR_AG','EPR-AG CC BY-NC-SA 4.0; see family README'
        return fam,'metadata','metadata','SUPPORT','see family README'
    if top=='RELIGION_AND_STATE':
        if len(parts)>1 and parts[1]=='data':
            name=parts[-1]
            if 'RAS3_COMPLETE' in name: return 'RAS','RAS3 1990-2014','selected_source','ES05','no explicit license; research-use/ARDA; see README'
            if 'RASM3_COMPLETE' in name: return 'RAS','RASM3','selected_source','ES06','no explicit license; research-use/ARDA; see README'
            if 'RAS_Constitutions' in name: return 'RAS','RAS Constitutions v1.02','selected_source','ES07','no explicit license; research-use/ARDA; see README'
            if 'RMAR' in name: return 'RAS','RMAR 2000-2014','reserve','RESERVE_RMAR','no explicit license; research-use/ARDA; see README'
            if 'SOR' in name: return 'RAS','SOR specialized dataset','reserve','RESERVE_RAS_SOR','no explicit license; research-use/ARDA; see README'
        return 'RAS','RAS documentation','documentation','SUPPORT','no explicit license; see README'
    if top=='WOMEN_BUSINESS_AND_LAW': return 'WBL','multiple WBL releases','selected_source' if len(parts)>1 and parts[1]=='data' else 'documentation','ES08','World Bank CC BY 4.0; 2024 report CC BY 3.0 IGO'
    if top=='GLOBAL_JOBS_INDICATORS_JOIN': return 'JOIN','JOIN v10','selected_source' if parts[-1].endswith('.xlsx') else 'documentation','ES10','World Bank CC BY 4.0'
    if top=='ILOSTAT':
        if len(parts)>1 and parts[1]=='indicator' and p.suffix=='.rds': return 'ILOSTAT','annual selected indicator','selected_source','ES09','ILO CC BY 4.0'
        return 'ILOSTAT','catalogs/dictionaries/docs','documentation','SUPPORT','ILO CC BY 4.0'
    if top=='WORLD_INEQUALITY_DATABASE':
        if len(parts)>1 and parts[1]=='archive': return 'WID','bulk archive','selected_source','ES11','license ambiguous; see README'
        return 'WID','documentation','documentation','SUPPORT','license ambiguous; see README'
    if top=='Global Findex': return 'FINDEX','Global Findex 2025 aggregate + docs','selected_source' if p.suffix=='.dta' else 'documentation','ES12','World Bank CC BY 4.0'
    if top=='V_DEM':
        if len(parts)>1 and parts[1]=='data': return 'VDEM','v16 Full+Others','selected_source','ES14','CC BY-SA 4.0'
        return 'VDEM','v16 docs/release','documentation','SUPPORT','CC BY-SA 4.0'
    if top=='Enterprise':
        name=p.name
        if 'Indicators Database - Global Methodology' in name or 'Indicators Database - Not Global Methodology' in name or 'Informal Sector Enterprise Surveys-Indicators-Database' in name:
            return 'ENTERPRISE','enterprise aggregate/indicator database','selected_source','ES13','World Bank Enterprise Surveys; license not separately captured'
        return 'ENTERPRISE','enterprise reserve/raw database','reserve','RESERVE_ENTERPRISE','World Bank Enterprise Surveys; license not separately captured'
    if top in ('Rawlsing 35 waves of savs & dtas','EVS','WVS','BarAfro','BarArab','BarAsian','BarLatino','LiTS','SS','SouthAsia','Final Codebooks','ArabBarometer_WaveIX_English_Datasets_NOV_2026'):
        return 'RAWLSING_35_WAVES','local respondent source estate','reserve','ORIGINAL35_RESERVE','restricted/respondent-source terms; not exported'
    if top=='MICS_Datasets.zip': return 'MICS','reserve archive','reserve','RESERVE_MICS','restricted/respondent-source terms; not exported'
    if top in ('COUNTRY_ROSTER_35_WAVES.csv','COUNTRY_ROSTER_35_WAVES.txt','SOURCE_ESTATE_OVERLAP.md','SOURCE_ESTATE_OVERLAP.tsv','_coverage_sets.json','ACQUISITION_STATUS.md'):
        return 'FIELD_FORGE_EVIDENCE',top,'metadata','SUPPORT','internal metadata'
    return top or 'UNKNOWN','unknown','unknown','UNKNOWN','unknown'

def duplicate_basis(p):
    s=p.stem.lower()
    return ''  # filled for obvious sibling serializations below

def main():
    rows=[]; members=[]; failures=[]
    allfiles=[p for p in ROOT.rglob('*') if p.is_file()]
    for p in sorted(allfiles):
        rel=str(p.relative_to(ROOT))
        if p.name=='.DS_Store':
            continue
        fam,release,role,es,rights=family_release_role(p)
        mg=magic(p); fmt=fmt_for(p,mg)
        try:
            sha,n=sha256_file(p)
            shaval=sha
        except Exception as e:
            shaval=f'UNREADABLE:{e}'; n=p.stat().st_size if p.exists() else ''
        status='INSPECTED' if role in ('selected_source','documentation','metadata') else 'RESERVE_NOT_PROFILED'
        if role=='reserve': status='RESERVE_NOT_PROFILED'
        rows.append([rel,'',fam,release,role,n,shaval,fmt,reader_for(fmt),status,'',rights,es])
        if p.suffix.lower()=='.zip':
            try:
                z=zipfile.ZipFile(p)
                bad=z.testzip()
                if bad: failures.append((rel,'zip_member_crc_failure',bad))
                for i in z.infolist():
                    if i.is_dir(): continue
                    rows.append([rel,i.filename,fam,release,'archive_member',i.file_size,f'zip_crc32:{i.CRC:08x}',fmt_for(Path(i.filename),magic_bytes=None) if False else (Path(i.filename).suffix.lower().lstrip('.') or 'unknown'),reader_for(Path(i.filename).suffix.lower().lstrip('.')),'INSPECTED_METADATA_ONLY','','',es])
                    # nested zip one level for Enterprise indicators
                    if i.filename.lower().endswith('.zip') and p.parent.name=='Enterprise':
                        try:
                            data=z.read(i.filename)
                            iz=zipfile.ZipFile(io.BytesIO(data))
                            for j in iz.infolist():
                                if j.is_dir(): continue
                                rows.append([rel,i.filename+'::'+j.filename,fam,release,'archive_member_nested',j.file_size,f'zip_crc32:{j.CRC:08x}',Path(j.filename).suffix.lower().lstrip('.') or 'unknown',reader_for(Path(j.filename).suffix.lower().lstrip('.')),'INSPECTED_METADATA_ONLY','','',es])
                        except Exception as e:
                            failures.append((rel,i.filename,'nested_zip_unreadable',str(e)))
            except Exception as e:
                failures.append((rel,'zip_open_failure',str(e)))
    # mark obvious alternative serializations by same stem in same dir
    from collections import defaultdict
    groups=defaultdict(list)
    for idx,r in enumerate(rows):
        if r[1]=='' and r[4]=='selected_source':
            p=ROOT/r[0]; groups[(str(p.parent),p.stem)].append(idx)
    for key,idxs in groups.items():
        if len(idxs)>1:
            for i in idxs:
                others=[rows[j][0] for j in idxs if j!=i]
                rows[i][10]='alternative_serialization_same_stem; not byte-verified: '+';'.join(others)
    with open(OUT/'FILE_MANIFEST.tsv','w',newline='') as f:
        w=csv.writer(f,delimiter='\t')
        w.writerow(['relative_path','archive_member','family','release','role','bytes','sha256_or_reason','format','reader','status','duplicate_basis','rights_status','es_id'])
        w.writerows(rows)
    with open(OUT/'_inventory_failures.tsv','w',newline='') as f:
        w=csv.writer(f,delimiter='\t'); w.writerow(['path','member','failure','detail']); w.writerows(failures)
    print('files',len(allfiles),'manifest_rows',len(rows),'failures',len(failures))
if __name__=='__main__': main()
