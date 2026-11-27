import csv, json, re, hashlib, functools
from pathlib import Path
import pycountry, country_converter as coco
ROOT=Path('/Users/matthewsmith/Desktop/Rawlsing/source_files')
OUT=Path('/Users/matthewsmith/Desktop/FIELD_FORGE_EXTERNAL_ESTATE_RETURN_R1')
ROSTER=set(x.strip() for x in (ROOT/'COUNTRY_ROSTER_35_WAVES.txt').read_text().splitlines() if x.strip())
ALIASES={
 'hongkong':'HKG','mainland china':'CHN','srilanka':'LKA','slovak rep.':'SVK','czech rep.':'CZE',
 'kyrgyz rep.':'KGZ','russia':'RUS','moldova':'MDA','bosnia':'BIH','fyrom':'MKD','czechrep':'CZE',
 'turkey':'TUR','vietnam':'VNM','bolivia':'BOL','tanzania':'TZA','iran':'IRN','syria':'SYR',
 'egypt':'EGY','cape verde':'CPV','cote d’ivoire':"CIV","cote d'ivoire":"CIV",'ivory coast':'CIV',
 'palestine':'PSE','taiwan':'TWN','kosovo':'XKX','north macedonia':'MKD','macedonia':'MKD',
 'united states':'USA','usa':'USA','great britain':'GBR','uk':'GBR','south korea':'KOR','korea':'KOR',
 'german federal republic':'DEU','german democratic republic':'DDR','yugoslavia':'SRB','zanzibar':'TZA',
 'uae':'ARE','venezuala':'VEN','timor':'TLS','vietnam, democratic republic of':'VNM','vietnam, republic of':'VNM',
 'central afican rep.':'CAF','central afican rep':'CAF','central african republic':'CAF','ethipoia':'ETH','myanamar':'MMR','nambia':'NAM','congo-brazzaville':'COG','congo, rep.':'COG','dr congo':'COD','cote d ivoire':'CIV',
}
def norm(x):
 s=str(x).strip(); s=re.sub(r'^\{cnt=\d+\}','',s); s=re.sub(r'^\d+\.\s*','',s)
 return s.replace('\u00a0',' ').strip()
@functools.lru_cache(maxsize=None)
def iso3(x):
 if x is None: return None
 s=norm(x); k=s.lower().strip('. ')
 if k in ALIASES: return ALIASES[k]
 try:
  out=coco.convert(names=[s],to='ISO3',not_found=None)
  v=out[0] if isinstance(out,(list,tuple)) else out
  if v and v!='not found' and len(str(v))==3: return str(v)
 except Exception: pass
 try: return pycountry.countries.lookup(s).alpha_3
 except Exception: return None
def valid_iso(x): return bool(x and len(x)==3 and pycountry.countries.get(alpha_3=x))
def ranges(years):
 ys=sorted(set(int(y) for y in years if str(y).strip()!=''))
 if not ys: return ''
 out=[]; a=b=ys[0]
 for y in ys[1:]:
  if y==b+1: b=y
  else: out.append(f'{a}' if a==b else f'{a}-{b}'); a=b=y
 out.append(f'{a}' if a==b else f'{a}-{b}')
 return ','.join(out)
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def write_tsv(name, header, rows):
 p=OUT/name
 with open(p,'w',newline='') as f:
  w=csv.writer(f,delimiter='\t'); w.writerow(header); w.writerows(rows)
 print(name,len(rows))
def read_manifest():
 return list(csv.DictReader(open(OUT/'FILE_MANIFEST.tsv'),delimiter='\t'))
