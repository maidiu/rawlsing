import csv, json
from pathlib import Path
R=Path(__file__).resolve().parent.parent
m=json.loads((R/"estate_acceptance_manifest.json").read_text())
with (R/"cell_report_1890.csv").open("w",newline="") as f:
    w=csv.writer(f); w.writerow(["cell_id","source_id","axis_id","axis_family","expected_u_e_pre_status","consumed_grade","cell_status","missing_owner"])
    for c in m["cells"]:
        w.writerow([c["cell_id"],c["source_id"],c["axis_id"],c["axis_family"],c["expected_u_e_pre"]["expected_u_e_pre_status"],c["consumed_grade"] or "",c["cell_status"],(c["missing_obligation"] or {}).get("owner","")])
with (R/"wave_report_35.csv").open("w",newline="") as f:
    w=csv.writer(f); w.writerow(["source_id","source_name","expected_u_e_pre_status","wave_occupancy_state","occupied_or_accounted_cells","missing_cells"])
    for r in m["waves"]:
        w.writerow([r["source_id"],r["source_name"],r["expected_u_e_pre"]["expected_u_e_pre_status"],r["wave_occupancy_state"],r["occupied_or_accounted_cells"],r["missing_cells"]])
print("reports written")
