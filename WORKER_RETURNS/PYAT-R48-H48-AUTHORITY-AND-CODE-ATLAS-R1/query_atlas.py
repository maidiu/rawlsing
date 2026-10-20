"""Read the H48 indexes without opening original sources or granting authority."""
import argparse,csv,gzip,json,pathlib

ROOT=pathlib.Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--input',help='Exact or partial current input ID')
p.add_argument('--wave',help='Exact canonical family|wave, e.g. LiTS|2006')
p.add_argument('--item',help='Exact source variable (case preserved); use with --wave')
p.add_argument('--evidence',help='Exact E evidence ID')
a=p.parse_args()
if a.evidence:
 print(json.dumps(json.load(open(ROOT/'EVIDENCE_MANIFEST.json'))['evidence'][a.evidence],indent=2,ensure_ascii=False))
elif a.item:
 if not a.wave:p.error('--item requires --wave')
 family,wave=a.wave.split('|',1)
 with gzip.open(ROOT/'evidence/original_item_authority_candidates.json.gz','rt') as f:rows=json.load(f)
 print(json.dumps([r for r in rows if (r['source_family'],r['wave'],r['source_variable_code'])==(family,wave,a.item)],indent=2,ensure_ascii=False))
elif a.input:
 rows=list(csv.DictReader(open(ROOT/'01_CURRENT_CONSUMER_INPUT_AND_PROVIDER_INDEX.csv')))
 selected=[r for r in rows if a.input in r['input_id']]
 if a.wave:
  family,wave=a.wave.split('|',1)
  prefixes={p for r in selected for p in json.loads(r['authority_locator_family_prefixes'])}
  locators=list(csv.DictReader(open(ROOT/'02_ACCEPTED_AND_ARCHIVAL_AUTHORITY_LOCATOR.csv')))
  routes=[r for r in locators if (r['source_family'],r['wave'])==(family,wave) and any(r['authority_family'].startswith(p) for p in prefixes)]
  selected={'inputs':selected,'source_authority_routes':routes,'grade':'Routes and source assertions are scoped evidence; current selection/permission remain separate.'}
 print(json.dumps(selected,indent=2,ensure_ascii=False))
elif a.wave:
 family,wave=a.wave.split('|',1)
 rows=list(csv.DictReader(open(ROOT/'02_ACCEPTED_AND_ARCHIVAL_AUTHORITY_LOCATOR.csv')))
 print(json.dumps([r for r in rows if (r['source_family'],r['wave'])==(family,wave)],indent=2,ensure_ascii=False))
else:p.print_help()
