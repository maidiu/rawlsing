"""Reverify only the nonrespondent metadata/code preimages in the H48 manifest.

Missing roots/objects are reported, never fetched or replaced. Survey data,
databases and respondent carriers are refused even if added to a manifest.
"""
import argparse,hashlib,json,pathlib,subprocess,zipfile
ROOT=pathlib.Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',required=True)
p.add_argument('--local-root',required=True)
p.add_argument('--trawlsing-root',required=True)
p.add_argument('--harvest-root',required=True)
a=p.parse_args()
roots={'$RAWLSING_LOCAL':pathlib.Path(a.local_root),'$AUTHORITY_ARCHIVE':pathlib.Path(a.local_root)/'Rawlsing_Authority_Document_Archive_2026-08-24','$TRAWLSING_LOCAL':pathlib.Path(a.trawlsing_root),'$HARVEST':pathlib.Path(a.harvest_root),'$H48':pathlib.Path(a.repo)}
forbidden={'.sav','.dta','.parquet','.arrow','.db','.sqlite','.sqlite3'}
result=[]
for eid,x in json.load(open(ROOT/'EVIDENCE_MANIFEST.json'))['evidence'].items():
 try:
  if x['kind']=='GIT':
   assert pathlib.Path(x['path']).suffix.lower() not in forbidden
   b=subprocess.check_output(['git','-C',a.repo,'show',x['commit']+':'+x['path']],stderr=subprocess.PIPE)
   oid=subprocess.check_output(['git','-C',a.repo,'rev-parse',x['commit']+':'+x['path']],stderr=subprocess.PIPE).decode().strip()
   assert oid==x['blob_oid']
  else:
   locator=x['locator'];prefix,rel=locator.split('/',1);base=roots[prefix]
   if '!' in rel:
    archive,member=rel.split('!',1);ap=(base/archive).resolve();assert ap.is_relative_to(base.resolve())
    with zipfile.ZipFile(ap) as z:
     if member=='CENTRAL_DIRECTORY':b=json.dumps(z.namelist()).encode()
     else:
      assert pathlib.Path(member).suffix.lower() not in forbidden
      b=z.read(member)
   else:
    fp=(base/rel).resolve();assert fp.is_relative_to(base.resolve()) and fp.suffix.lower() not in forbidden;b=fp.read_bytes()
  assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
  result.append({'evidence_id':eid,'state':'PASS'})
 except (OSError,KeyError,AssertionError,ValueError,subprocess.CalledProcessError,zipfile.BadZipFile) as ex:
  result.append({'evidence_id':eid,'state':'UNAVAILABLE_OR_MISMATCH','error_type':type(ex).__name__})
counts={state:sum(r['state']==state for r in result) for state in ['PASS','UNAVAILABLE_OR_MISMATCH']}
print(json.dumps({'counts':counts,'results':result},indent=2))
raise SystemExit(bool(counts['UNAVAILABLE_OR_MISMATCH']))
