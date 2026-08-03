#!/usr/bin/env python3
import csv,json,hashlib,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'outputs/P3C_EVIDENCE_FIRST_INVENTORY_RETURN.json').read_text())
expected={'status':'PASS','original_candidate_revisions':141,'candidate_membership_occurrences':496,'unique_member_lineages':397,'shared_member_components':112,'cross_component_merges':2,'final_proposition_families':111,'multi_family_original_candidates':2,'open_closure_obligations':345}
errors=[]
for k,v in expected.items():
    if d.get(k)!=v: errors.append(f'{k}: {d.get(k)!r} != {v!r}')
inv=list(csv.DictReader((root/'outputs/P3C_EVIDENCE_FIRST_CANDIDATE_INVENTORY.csv').open()))
fams=list(csv.DictReader((root/'outputs/P3C_FINAL_PROPOSITION_FAMILY_MAP.csv').open()))
mem=list(csv.DictReader((root/'outputs/P3C_EVIDENCE_FIRST_MEMBER_MAP.csv').open()))
if len(inv)!=141: errors.append(f'inventory rows={len(inv)}')
if len(fams)!=111: errors.append(f'family rows={len(fams)}')
if len(mem)!=496: errors.append(f'member rows={len(mem)}')
bycand={r['candidate_revision_id']:r for r in inv}
if bycand['P3CANDREV-000273-R0002']['primary_family_id']!='JFAM-000219': errors.append('candidate273 not mapped to JFAM-000219')
if bycand['P3CANDREV-000252-R0002']['planned_decision']!='SPLIT_REQUIRED_TO_SUCCESSORS_424_425': errors.append('candidate252 split plan absent')
if bycand['P3CANDREV-000264-R0002']['planned_decision']!='DIRECT_FAMILY_CONFIRMATION_WITH_DERIVED_NAMED_EXCLUSION': errors.append('candidate264 boundary plan absent')
print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors,'checked_candidates':len(inv),'checked_families':len(fams),'checked_memberships':len(mem)},indent=2))
raise SystemExit(1 if errors else 0)
