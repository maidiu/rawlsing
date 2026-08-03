from __future__ import annotations

import csv, hashlib, json, sys
from pathlib import Path

CONTROL={"PACKAGE_INDEX.csv","SHA256SUMS.csv","VALIDATION.json"}

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    if rows and any(v == "SET" for v in rows[0].values()):
        raise ValueError(f"SET preamble in {path}")
    return rows

def all_pass(path: Path) -> bool:
    rows=read_csv(path)
    return bool(rows) and all(r.get("status") == "PASS" for r in rows)

def main() -> int:
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
    sec=root/"55_P3A_V7_DIRECT_CONSTRAINT_CLOSURE_AND_RISK_STRATIFIED_PILOT"
    expected={r["relative_path"]:r for r in csv.DictReader((root/"PACKAGE_INDEX.csv").open(newline="",encoding="utf-8"))}
    actual={}
    debris=[]
    csv_set=[]
    for p in root.rglob("*"):
        if p.is_dir() and p.name == "__pycache__": debris.append(p.relative_to(root).as_posix())
        if not p.is_file(): continue
        rel=p.relative_to(root).as_posix()
        if p.suffix == ".pyc": debris.append(rel)
        if p.suffix.lower() in {".csv", ".tsv"}:
            try:
                first=p.read_text(errors="ignore").splitlines()[0]
                if first == "SET": csv_set.append(rel)
            except IndexError:
                pass
        if rel in CONTROL or p.name==".DS_Store" or "/.DS_Store" in rel: continue
        actual[rel]=p
    missing=sorted(set(expected)-set(actual)); unexpected=sorted(set(actual)-set(expected)); mismatches=[]
    for rel,row in expected.items():
        p=actual.get(rel)
        if p and (str(p.stat().st_size)!=row["bytes"] or sha256(p)!=row["sha256"]): mismatches.append(rel)
    validation=json.loads((root/"VALIDATION.json").read_text())
    query=json.loads((sec/"outputs/v33_populated_validation_matrix_summary.json").read_text())
    pilot=json.loads((sec/"P3A_V33_PILOT_STRATA_RETURN.json").read_text())
    fixture=json.loads((sec/"P3A_V33_FIXTURE_ISOLATION_RETURN.json").read_text())
    objects=json.loads((sec/"P3A_V33_OBJECT_COUNTS.json").read_text())
    checks={
      "direct_constraints": all_pass(sec/"P3A_V33_DIRECT_CONSTRAINT_RECONCILIATION.csv") and len(read_csv(sec/"P3A_V33_DIRECT_CONSTRAINT_RECONCILIATION.csv"))==10,
      "attachment_bridges": all_pass(sec/"P3A_V33_ATTACHMENT_ORIGIN_RECONCILIATION.csv") and len(read_csv(sec/"P3A_V33_ATTACHMENT_ORIGIN_RECONCILIATION.csv"))==41,
      "signature_blockers": all_pass(sec/"P3A_V33_SIGNATURE_BLOCKER_RECONCILIATION.csv"),
      "pilot_packets": pilot.get("status")=="PASS" and pilot.get("packet_count")==40 and all_pass(sec/"P3A_V33_DATABASE_PACKET_CONVERGENCE.csv"),
      "fixture_isolation": fixture.get("status")=="PASS" and fixture.get("main_canonical_families")==0 and fixture.get("main_final_adjudications")==0,
      "q_matrix": query.get("failures")==["q01b_postpromotion_pointer","q15b_no_unadjudicated_at_p3_close"],
      "counts": objects["metrics"].get("pair_projections_total")==667 and objects["metrics"].get("candidate_000136_attachment_projections")==47 and objects["metrics"].get("clean_candidates")==0,
    }
    ok=not missing and not unexpected and not mismatches and not debris and not csv_set and validation.get("handoff_version")=="v33" and all(checks.values())
    result={"status":"PASS" if ok else "FAIL","manifested_payload_files":len(expected),"actual_payload_files":len(actual),"missing":missing,"unexpected":unexpected,"mismatches":mismatches,"debris":debris,"csv_set_preambles":csv_set,"checks":checks}
    print(json.dumps(result,indent=2))
    return 0 if ok else 1

if __name__=="__main__":
    raise SystemExit(main())
