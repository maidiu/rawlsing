from pathlib import Path
import csv
import hashlib
import json
import subprocess
import sys


ROOT = Path(sys.argv[1]).resolve()
SEC = ROOT / "58_P3A_V7_RELEASE_LINEAGE_TYPED_SCHEMA_FIXTURES_AND_GOVERNED_PILOT"
fail = []


def need(rel):
    p = SEC / rel
    if not p.exists():
        fail.append(f"missing {rel}")
    return p


def j(rel):
    p = need(rel)
    return json.loads(p.read_text()) if p.exists() else {}


def rows(rel):
    p = need(rel)
    return list(csv.DictReader(p.open())) if p.exists() else []


required = [
    "P3A_V36_CANDIDATE_IDENTITY_MIGRATION.csv",
    "P3A_V36_PACKET_IDENTITY_RECONCILIATION.csv",
    "P3A_V36_COMPONENT_IDENTITY_RECONCILIATION.csv",
    "P3A_V36_ALL_CANDIDATE_HASH_RECONCILIATION.csv",
    "P3A_V36_DIRECT_PAIR_CLOSURE_RECONCILIATION.csv",
    "P3A_V36_TYPED_CONSTRAINT_CONVERGENCE.csv",
    "P3A_V36_RANKING_DERIVATION.csv",
    "P3A_V36_PILOT_STRATA_ELIGIBILITY.csv",
    "P3A_V36_PILOT_CANDIDATE_INDEX.csv",
    "P3A_V36_PILOT_SUBSTITUTION_LEDGER.csv",
    "P3A_V36_QUERY_MATRIX.csv",
    "P3A_V36_OBJECT_COUNTS.json",
    "outputs/p3a_v36_fixture_lifecycle_return.json",
    "outputs/p3a_v36_candidates_final_return.json",
    "postgres/v36_historical_current_boundary_regression_stdout.txt",
    "postgres/blocker_evidence/v36_candidate_origin_blocker_preservation.json",
]
for rel in required:
    need(rel)

for p in ROOT.rglob("*"):
    if p.name == "__pycache__" or p.suffix == ".pyc":
        fail.append(f"python cache present {p.relative_to(ROOT)}")

candidate_return = j("outputs/p3a_v36_candidates_final_return.json")
if candidate_return.get("historical_candidate_revisions_fabricated") != 0:
    fail.append("historical revisions were fabricated")
if candidate_return.get("frozen_historical_identities") != 564:
    fail.append("frozen historical identity count is not 564")
if candidate_return.get("candidate_revisions") != 141:
    fail.append("R36 candidate revision count is not 141")

reg = need("postgres/v36_historical_current_boundary_regression_stdout.txt").read_text()
for token in [
    "frozen_identity_count|564",
    "fabricated_historical_revisions|0",
    "bad_current_base_candidates|0",
    "historical_runtime_addressable|0",
    "frozen_identity_mutation_rejected|PASS",
    "malformed_r36_base_candidate_rejected|PASS",
    "valid_r36_base_candidate_commits_in_rollback_fixture|PASS",
    "regression_fixture_rows_persisted|0",
]:
    if token not in reg:
        fail.append(f"missing regression token {token}")

pkt_rows = rows("P3A_V36_PACKET_IDENTITY_RECONCILIATION.csv")
if len(pkt_rows) != 11:
    fail.append("packet reconciliation not 11 rows")
for r in pkt_rows:
    recomputed = "P3PKT-" + hashlib.sha256("|".join([r["candidate_revision_id"], r["evidence_bundle_hash"], r["schema_version"]]).encode()).hexdigest()[:16]
    if r["packet_id"] != recomputed or r["status"] != "PASS":
        fail.append(f"packet id mismatch {r.get('candidate_revision_id')}")

for rel in [
    "P3A_V36_COMPONENT_IDENTITY_RECONCILIATION.csv",
    "P3A_V36_ALL_CANDIDATE_HASH_RECONCILIATION.csv",
    "P3A_V36_DIRECT_PAIR_CLOSURE_RECONCILIATION.csv",
    "P3A_V36_TYPED_CONSTRAINT_CONVERGENCE.csv",
    "P3A_V36_RANKING_DERIVATION.csv",
]:
    rs = rows(rel)
    if not rs:
        fail.append(f"{rel} empty")
    for r in rs:
        if r.get("status") != "PASS":
            fail.append(f"{rel} status not PASS")

counts = j("P3A_V36_OBJECT_COUNTS.json")
if counts.get("status") != "PASS":
    fail.append("object counts not PASS")
if counts.get("candidate_revisions") != 141:
    fail.append("object counts candidate revision total not 141")
if counts.get("typed_constraints", {}).get("hard_collisions") != 1:
    fail.append("redirect counted as hard collision")

strata = rows("P3A_V36_PILOT_STRATA_ELIGIBILITY.csv")
if len(strata) != 11:
    fail.append("pilot strata count not 11")
for r in strata:
    if r["status"] not in {"PASS", "SHORTFALL_RECORDED"}:
        fail.append("bad stratum status")

packets = list((SEC / "candidate_packets").glob("*.json"))
drafts = list((SEC / "draft_decisions").glob("*.json"))
if len(packets) != 11 or len(drafts) != 11:
    fail.append("packet/draft count not 11")
draft_by_cand = {p.name.split("_")[1]: p for p in drafts}
for pp in packets:
    cand = pp.stem.split("_")[-1]
    dp = draft_by_cand.get(cand)
    if not dp:
        fail.append(f"missing draft for {pp.name}")
        continue
    proc = subprocess.run([sys.executable, str(SEC / "validation/validate_p3_candidate_packet_v32.py"), str(pp), str(dp)], text=True, capture_output=True)
    if proc.returncode != 0:
        fail.append(f"packet validator failed {pp.name}: {proc.stdout[:200]}")

fix = j("outputs/p3a_v36_fixture_lifecycle_return.json")
if fix.get("status") != "PASS":
    fail.append("fixture lifecycle did not PASS")
for r in fix.get("results", []):
    if r.get("expect_pass") and r.get("status") != "PASS":
        fail.append(f"positive fixture failed {r.get('case')}")
    if not r.get("expect_pass") and r.get("status") != "EXPECTED_FAIL":
        fail.append(f"negative fixture did not fail {r.get('case')}")

q = rows("P3A_V36_QUERY_MATRIX.csv")
fails = [r["query_or_gate"] for r in q if r["status"] == "FAIL"]
if sorted(fails) != ["q01b_postpromotion_pointer", "q15b_no_unadjudicated_at_p3_close"]:
    fail.append(f"unexpected q failures {fails}")

print(json.dumps({"status": "FAIL" if fail else "PASS", "failures": fail}, indent=2))
sys.exit(1 if fail else 0)
