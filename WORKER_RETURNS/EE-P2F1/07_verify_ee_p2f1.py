#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
A = "A__SATISFIED_AS_IS_PRE553_READY"
B = "B__SEMANTIC_AUTHORITY_EXISTS__PRE553_ISSUANCE_OR_BINDING_ONLY"
C = "C__SOURCE_EVIDENCE_SUFFICIENT__NEW_ADOPTED_AUTHORITY_REQUIRED"
D = "D__GENUINELY_MISSING_SEMANTIC_OR_ROUTING_AUTHORITY"
E = "E__NOT_REQUIRED_FOR_FROZEN_P2_WVS_PROGRAM"

matrix = json.loads((ROOT / "01_REQUIRED_PRE553_AUTHORITY_MATRIX.json").read_text())
cross = json.loads((ROOT / "03_REQUIREMENT_TO_AUTHORITY_CROSSWALK.json").read_text())
wake = json.loads((ROOT / "06_LOCK2_WAKE_DECISION.json").read_text())
rows = matrix["rows"]
ids = [r["requirement_id"] for r in rows]
required = {"R01","R02","R03","R04","R05","R06","R07","R08","R09","R10","R10W","R11","R12","R13","R14","R15A","R15B"}
assert set(ids) == required and len(ids) == len(set(ids))
assert all(r["classification"] in {A,B,C,D,E} for r in rows)
counts = {k: sum(r["classification"] == v for r in rows) for k,v in {"A":A,"B":B,"C":C,"D":D,"E":E}.items()}
assert counts == {"A":0,"B":14,"C":0,"D":0,"E":3}, counts
assert matrix["summary"]["semantic_or_routing_gap_count"] == 0
assert matrix["summary"]["new_adoption_required_count"] == 0
assert all(r["owner_category"] is not None for r in rows if r["classification"] in {B,C,D})
assert all(r["owner_category"] is None for r in rows if r["classification"] == E)
assert len(cross["crosswalk"]) == len(rows)
assert {r["requirement_id"] for r in cross["crosswalk"]} == required
assert wake["decision"] == "WAKE_MECHANICAL_PRE553_ISSUER__THEN_REWAKE_LOCK2_HASH_MATERIALIZER"
assert wake["next_worker_may"]["open_wvs_source"] is False
assert wake["next_worker_may"]["inspect_outcomes"] is False
assert wake["next_worker_may"]["change_semantics"] is False
assert wake["next_worker_may"]["change_routing"] is False
assert wake["candidate_execution"].startswith("FORBIDDEN")
text = (ROOT / "00_RETURN.md").read_text()
assert "EE_P2F1_PASS__ALL_WVS_P2_REQUIREMENTS_CLASSIFIED__MECHANICAL_PRE553_ISSUANCE_ONLY" in text
assert "Raw WVS source opened: **NO**" in text
assert "Candidate execution / measurement: **NO**" in text
plan = (ROOT / "04_MINIMUM_PRE553_ISSUANCE_ENGINEERING_PLAN.md").read_text()
assert "Zero new semantic propositions" in plan
assert "pre553_discovery_exact_execute" in plan
new = (ROOT / "05_MINIMUM_NEW_AUTHORITY_PLAN.md").read_text()
assert "**No C rows. No D rows.**" in new
print(json.dumps({"status":"PASS","rows":len(rows),"counts":counts,"terminal":"EE_P2F1_PASS__ALL_WVS_P2_REQUIREMENTS_CLASSIFIED__MECHANICAL_PRE553_ISSUANCE_ONLY"}, sort_keys=True))
