"""Actual refusal/effect observations; not extra pytest or scientific passes."""
import json,pathlib,tempfile,os,sys
from rawlsing_next.tests import test_hq297_v2r_role_query_binding as T
RET=T.RET;R=T.R;K=T.K
rows=[]
for kind in ['role','form','unit','held','subset','raw_denominator','profile']:
 root=pathlib.Path(tempfile.mkdtemp(prefix='hq297-refusal-'))
 records,expected,plans,calls,register=T.fixture(root)
 if kind in ['role','form','unit','held','subset']:
  changed,plans=T.changed_case(records,expected,plans,kind);expected=K.FrozenOriginalExpected.from_records(changed,input_origin=K.ORIGIN)
 else:
  raw=json.loads(register.payload_json);row=next(r for r in raw['records'] if r['record']['legacy']['slot']=='PAIR')
  if kind=='raw_denominator':row['binding'][kind]=3
  else:row['binding'][kind]['1']['denominator']=3
  register=R.FrozenSourceNativeRegister.from_payload(raw)
 try:R.run_sourcefree(expected=expected,selected_scopes=plans,register=register)
 except R.RoleBindingError as e:
  rows.append(dict(case=kind,diagnostic=str(e),durable_calls=[len(c) for c in calls],ledger_root=str(root),qualified_product_returned=False))
 else:raise AssertionError('FALSE_GREEN_'+kind)
(RET/'repro/actual_refusal_effects.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
