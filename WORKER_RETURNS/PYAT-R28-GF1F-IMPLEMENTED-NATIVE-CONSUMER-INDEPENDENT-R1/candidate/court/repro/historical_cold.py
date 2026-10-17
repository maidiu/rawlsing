"""Fresh physical predecessor reproduction, separately retained from PV3 repair."""

from pathlib import Path
from collections import Counter
import os, sys, subprocess, json, hashlib, shutil

R = Path(__file__).resolve().parents[1]
RT = R / "runtime_root"
root = RT / "historical_final_cold"
H = R / "historical/observations"
H.mkdir(parents=True, exist_ok=True)


def call(mode, path=root, tag=None):
    tag = "historical_" + (tag or mode)
    cmd = [sys.executable, str(R / "repro/cold_child.py"), str(path), mode, tag]
    p = subprocess.run(
        cmd,
        env=dict(os.environ, PV3_COLD_MODE="HISTORICAL"),
        capture_output=True,
        text=True,
    )
    (H / (tag + ".stdout")).write_text(p.stdout + p.stderr)
    return {"argv": cmd, "exit": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def ledger_hashes():
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (root / "ledger").rglob("*")
        if p.is_file()
    }


a = call("first")
assert a["exit"] == 0, a
before = ledger_hashes()
b = call("replay")
assert b["exit"] == 0, b
after = ledger_hashes()
f = json.loads((root / "observations/first.json").read_text())
r = json.loads((root / "observations/replay.json").read_text())
read = call("current_read", tag="forged_current_grant")
assert read["exit"] == 0, read
(H / "cold_forged_current_grant.json").write_bytes(
    (R / "observations/historical_forged_current_grant.json").read_bytes()
)
missing = call("missing_source")
edition = call("changed_edition")
first_audit = json.loads((R / "observations/historical_first.audit.json").read_text())
replay_audit = json.loads((R / "observations/historical_replay.audit.json").read_text())
(H / "cold_court.json").write_text(
    json.dumps(
        {
            "first": a,
            "replay": b,
            "distinct_pids": first_audit["pid"] != replay_audit["pid"],
            "same_ledger_bytes": before == after,
            "links_exact": f["links"] == r["links"],
            "held_exact": f["nonrunnable"] == r["nonrunnable"],
            "register_exact": f["pv2_register"] == r["pv2_register"],
            "no_new_durable_units": all(
                x["run"]["executed"] == [] for x in r["owner_reports"]
            ),
            "missing_source": missing,
            "changed_edition": edition,
            "actual_owner_calls_replay": dict(
                Counter(x["function"] for x in replay_audit["calls"])
            ),
        },
        indent=2,
    )
    + "\n"
)
for kind in ("journal", "checkpoint"):
    dest = RT / ("historical_" + kind + "_attack")
    shutil.copytree(root, dest)
    if kind == "journal":
        p = next((dest / "ledger").rglob("b01e_side_effects.jsonl"))
        lines = p.read_text().splitlines()
        row = json.loads(lines[0])
        row["result_refs"][0]["content_hash"] = "f" * 64
        row["result_refs"][0]["object_id"] = (
            "urn:rawlsing:pre553:EmpiricalFact:sha256:" + "f" * 64
        )
        lines[0] = json.dumps(row)
        p.write_text("\n".join(lines) + "\n")
    else:
        p = next((dest / "ledger").rglob("b01e_checkpoint.json"))
        d = json.loads(p.read_text())
        d["records"][0]["receipt_projection"]["result_refs"][0]["content_hash"] = (
            "a" * 64
        )
        p.write_text(json.dumps(d))
    result = call("replay", dest, kind + "_attack")
    (
        H
        / (
            "cold_actual_result_ref_tamper.json"
            if kind == "journal"
            else "cold_checkpoint_payload_tamper.json"
        )
    ).write_text(json.dumps(result, indent=2) + "\n")
    assert result["exit"] == (0 if kind == "journal" else 1)
print("PREDECESSOR_PHYSICAL_COLD_AND_ACCEPTED_FORGED_JOURNAL_REPRODUCED")
