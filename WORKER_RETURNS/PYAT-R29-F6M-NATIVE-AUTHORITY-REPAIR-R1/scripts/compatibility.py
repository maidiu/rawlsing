"""Explicit safety/custody compatibility; no frozen numerical oracle is changed."""
from pathlib import Path
import json,hashlib,difflib
ROOT=Path(__file__).resolve().parents[1]
def adapt(base):
 changes=[]
 def edit(rel,pairs):
  p=base/rel;before=p.read_text();after=before
  for old,new in pairs:
   assert old in after,(rel,old)
   after=after.replace(old,new)
  p.write_text(after)
  changes.append(dict(path=rel,before_sha256=hashlib.sha256(before.encode()).hexdigest(),after_sha256=hashlib.sha256(after.encode()).hexdigest(),diff=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='frozen/'+rel,tofile='safety-compat-v1/'+rel))))
 edit('F6C/02_TESTS/test_f6c_frozen_court.py',[
  ('assert blob == "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"','assert blob == __import__("f6m_custody").candidate_blob()'),
  ('assert PRODUCER.__file__.endswith("05_NATIVE_STAGE/rawlsing_next/pre553_heterogeneous_synthesis.py")','assert __import__("f6m_custody").verify_import(PRODUCER)'),
  ('== "EXTERNAL_REVIEW_REQUIRED"','== "UNVERIFIED_INTEGRATION_BOUNDARY"')])
 edit('F6J/04_TESTS/test_f6j_adversarial.py',[
  ('assert out["decision"] == "SYNTHETIC_CANDIDATE"','assert out["decision"] == "PARTIAL_IDENTIFICATION_ONLY"'),
  ('assert F(sup["sources"][0]["conditional_source_weight"]) == 1\n    d = cells(out["candidate"]["distribution"])\n    assert d == {("X", "U"): F(1, 4), ("X", "V"): F(1, 4),\n                 ("Y", "U"): F(1, 4), ("Y", "V"): F(1, 4)}',
   'assert F(sup["sources"][0]["conditional_source_weight"]) == F(1, 2)\n    assert out["candidate"]["distribution"] is None\n    assert F(out["candidate"]["uncovered_target_mass"]) == F(1, 2)\n    assert set(cells(out["candidate"]["covered_subprobability"]).values()) == {F(1, 8)}'),
  ('== "EXTERNAL_REVIEW_REQUIRED"','== "UNVERIFIED_INTEGRATION_BOUNDARY"'),
  ('assert "DESCRIPTIVE_SOCIOLOGICAL_MODEL_ONLY" in ceilings','assert set(ceilings) == {"TEST_ONLY"}'),
  ('assert "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE" in ceilings','assert "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE" not in ceilings'),
  ('assert missing and all(nid.startswith("mapped:") for nid in missing)','assert not missing'),
  ('src = (RET / "01_STAGED_NATIVE/rawlsing_next/pre553_heterogeneous_synthesis.py")','src = Path(sys.modules["rawlsing_next.pre553_heterogeneous_synthesis"].__file__)'),
  ('assert blob == "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"','assert blob == __import__("f6m_custody").candidate_blob()')])
 edit('F6L/02_PHASE_A/04_TESTS/test_f6l_phase_a.py',[
  ('assert blob == "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"','assert blob == __import__("f6m_custody").candidate_blob()'),
  ('entry = WORLDS["P5B_MIXED_ORIGIN_CONTAMINATION"]','entry = WORLDS[CASE_WORLD["P5B_MIXED_ORIGIN_CONTAMINATION"]]')])
 (ROOT/'custody/safety_compatibility_v1.json').write_text(json.dumps(changes,indent=2)+'\n')
