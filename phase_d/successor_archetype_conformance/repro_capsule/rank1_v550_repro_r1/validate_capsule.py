from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
EXPECTED = json.loads((ROOT / "config/CAPSULE_EXPECTATIONS.json").read_text())
slice_df = pd.read_csv(ROOT / "input/prepared_rank1_slice.csv")
assert len(slice_df) == 1800
assert slice_df["respondent_id_pseudo"].nunique() == 900
assert set(slice_df["var_code"].str.upper()) == {"Q306C", "Q305_1"}
assert all(re.fullmatch(r"r_[0-9a-f]{24}", str(v)) for v in slice_df["respondent_id_pseudo"])
assert not any(c in slice_df.columns for c in {"respondent_id", "respondent_id_norm", "email", "name"})
assert not slice_df["respondent_id_pseudo"].astype(str).str.contains("respondent", case=False, regex=False).any()
for required in [
    "schemas/branch_relation_co_signature.schema.json",
    "schemas/branch_co_signature.schema.json",
    "schemas/question_response_attitude_cloud.schema.json",
]:
    assert (ROOT / required).exists(), required
manifest = json.loads((ROOT / "CAPSULE_MANIFEST.json").read_text())
for entry in manifest["files"]:
    p = ROOT / entry["path"]
    assert p.exists(), entry["path"]
    assert p.stat().st_size == entry["bytes"], entry["path"]
    assert hashlib.sha256(p.read_bytes()).hexdigest() == entry["sha256"], entry["path"]
print("CAPSULE_VALID PASS")
print(json.dumps({"rows": len(slice_df), "respondents": int(slice_df.respondent_id_pseudo.nunique()), "files": len(manifest["files"])}, sort_keys=True))
