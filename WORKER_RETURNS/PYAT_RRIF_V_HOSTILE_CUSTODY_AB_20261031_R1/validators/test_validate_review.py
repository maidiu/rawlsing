from __future__ import annotations
import json,shutil,tempfile,unittest
from pathlib import Path
from validate_review import ValidationError,validate
ROOT=Path(__file__).resolve().parent.parent
FILES=['HOSTILE_COUNTS.json','FALSE_SUBTRACTION_CASES.jsonl','DECISION_ATTRIBUTION_DEFECTS.jsonl','A_EXACT_AUDIT.json','HOSTILE_FINDINGS.md','ADMISSIBLE_REDUCED_SCOPE.md']
class T(unittest.TestCase):
 def test_baseline(self):
  r=validate(ROOT); self.assertEqual(r['result'],'PASS')
 def _copy(self):
  t=tempfile.TemporaryDirectory(); d=Path(t.name)
  for f in FILES: shutil.copy2(ROOT/f,d/f)
  return t,d
 def _j(self,d,n): return json.loads((d/n).read_text())
 def _jl(self,d,n): return [json.loads(x) for x in (d/n).read_text().splitlines() if x]
 def _w(self,d,n,x): (d/n).write_text(json.dumps(x,indent=2)+'\n')
 def test_drop_false_case(self):
  t,d=self._copy()
  try:
   rows=self._jl(d,'FALSE_SUBTRACTION_CASES.jsonl'); rows.pop(); (d/'FALSE_SUBTRACTION_CASES.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows))
   with self.assertRaises(ValidationError): validate(d)
  finally: t.cleanup()
 def test_branch_count_wrong(self):
  t,d=self._copy()
  try:
   c=self._j(d,'HOSTILE_COUNTS.json'); c['A']['branch_only_exact_impl']=1332; self._w(d,'HOSTILE_COUNTS.json',c)
   with self.assertRaises(ValidationError): validate(d)
  finally: t.cleanup()
 def test_unique_id_wrong(self):
  t,d=self._copy()
  try:
   c=self._j(d,'HOSTILE_COUNTS.json'); c['B']['unique_primary_ids']=155; self._w(d,'HOSTILE_COUNTS.json',c)
   with self.assertRaises(ValidationError): validate(d)
  finally: t.cleanup()
 def test_checkpoint_defect_removed(self):
  t,d=self._copy()
  try:
   rows=self._jl(d,'DECISION_ATTRIBUTION_DEFECTS.jsonl'); rows=[x for x in rows if x['defect_id']!='DAD-006']; (d/'DECISION_ATTRIBUTION_DEFECTS.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows))
   with self.assertRaises(ValidationError): validate(d)
  finally: t.cleanup()
 def test_semantic_claim(self):
  t,d=self._copy()
  try:
   rows=self._jl(d,'FALSE_SUBTRACTION_CASES.jsonl'); rows[0]['semantic_equivalence']=True; (d/'FALSE_SUBTRACTION_CASES.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows))
   # no semantic field is checked as truth; ensure an explicit accepted-current inflation is rejected by counts via source flag
   c=self._j(d,'HOSTILE_COUNTS.json'); c['A']['declared_subtraction']=2268; self._w(d,'HOSTILE_COUNTS.json',c)
   with self.assertRaises(ValidationError): validate(d)
  finally: t.cleanup()
if __name__=='__main__': unittest.main()
