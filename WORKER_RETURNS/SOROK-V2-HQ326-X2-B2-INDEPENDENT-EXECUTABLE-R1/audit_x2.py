"""Independently verify B2 and all imported preimages against Git objects."""
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

B2 = Path(os.environ["B2_REVIEW_ROOT"]).resolve()
GIT = Path(os.environ["X2_GIT_CWD"]).resolve()
OUT = Path(__file__).resolve().parent
PREFIX = "WORKER_RETURNS/SOROK-V2-HQ325-B2-FOUR_RETURN_INTEGRATION-R1/"
PIN = "950ecf0b3816ea7d0dd3ab48b62c92cedfe0e883"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=GIT)


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


assert git("cat-file", "-t", PIN).strip() == b"commit"
tree = git("ls-tree", "-r", PIN, PREFIX).decode().splitlines()
b2_rows = []
regenerated = []
for row in tree:
    metadata, path = row.split("\t")
    expected_blob = metadata.split()[2]
    expected = git("show", PIN + ":" + path)
    local = (B2 / path.removeprefix(PREFIX)).read_bytes()
    assert blob(expected) == expected_blob, path
    if expected != local:
        assert path.removeprefix(PREFIX).startswith("evidence/") or path.removeprefix(PREFIX) in ("execution_receipt.json", "imported_sources.json"), path
        regenerated.append(path.removeprefix(PREFIX))
    else:
        assert expected == local
    if path.endswith((".py", ".js", ".json")) and "/evidence/" not in path:
        b2_rows.append({"path": path.removeprefix(PREFIX), "blob_sha1": expected_blob, "sha256": sha256(local)})

manifest = json.loads((B2 / "imported_sources.json").read_text())
import_rows = []
for row in manifest:
    local = (B2 / row["materialized_path"]).read_bytes()
    assert sha256(local) == row["sha256"]
    if row["component"] != "F1_ARCHIVE_MEMBER":
        assert git("cat-file", "-t", row["commit"]).strip() == b"commit"
        expected = git("show", row["commit"] + ":" + row["source_path"])
        assert expected == local
        assert blob(expected) == row["git_blob_sha1"]
    import_rows.append({k: row[k] for k in ("component", "materialized_path", "sha256")})

sys.path.insert(0, str(B2))
bridge = importlib.import_module("bridge")
f1 = importlib.import_module("f1_adapter")
modules = {name: {"relative_path": str(Path(module.__file__).resolve().relative_to(B2)),
                  "sha256": sha256(Path(module.__file__).read_bytes())}
           for name, module in (("B2 bridge", bridge), ("B1", bridge.b1), ("P1", bridge.p1), ("F1 adapter", f1))}
assert modules["B1"]["relative_path"] == "imports/B1/bfirst.py"
assert modules["P1"]["relative_path"] == "imports/P1/p1_contract.py"
assert bridge.D1_SOURCE.relative_to(B2).as_posix().startswith("imports/D1/")

totals = {}
for label in ("b1", "p1", "f1", "integration"):
    suite = ET.parse(B2 / "evidence" / (label + ".xml")).find("testsuite")
    totals[label] = {key: int(suite.attrib[key]) for key in ("tests", "failures", "errors", "skipped")}
native = json.loads((B2 / "evidence/f1_native_gate.log").read_text())
applicability = json.loads((B2 / "evidence/f1_applicability.json").read_text())
positive = json.loads((B2 / "evidence/vertical/positive/trace.json").read_text())
control = json.loads((B2 / "evidence/vertical/journal_only/trace.json").read_text())
cold = json.loads((B2 / "evidence/cold_replay.log").read_text())
assert cold["final_hash"] == positive["final_hash"]
assert cold["receipts"] == [ep["receipt"] for ep in positive["episodes"]]
assert positive["episodes"][1]["receipt"]["response"]["practical_activity"] == ["joint_check:caretaker"]
assert control["episodes"][1]["receipt"]["response"]["practical_activity"] == ["inspect_alone:caretaker"]
author_receipt = json.loads(git("show", PIN + ":" + PREFIX + "execution_receipt.json"))
independent_receipt = json.loads((B2 / "execution_receipt.json").read_text())
assert author_receipt["totals"] == independent_receipt["totals"]
assert author_receipt["f1"] == independent_receipt["f1"]
assert len(native["failures"]) == 17
assert sum(r["result"] == "PASS_BOUNDARY_ONLY" for r in applicability) == 19
assert sum(r["result"] == "NOT_APPLICABLE_TO_THIS_LAB" for r in applicability) == 17
assert {r["case_id"] for r in applicability if r["result"] == "NOT_APPLICABLE_TO_THIS_LAB"} == {r["case_id"] for r in native["failures"]}
result = {"sealed_start": git("rev-parse", "HEAD").decode().strip(),
          "b2_pin": PIN, "b2_tracked_files_verified": len(tree), "b2_source_hashes": b2_rows,
          "regenerated_b2_evidence_files": regenerated,
          "imported_files_and_archive_members_verified": len(import_rows),
          "imported_files": import_rows, "modules": modules,
          "d1_source": str(bridge.D1_SOURCE.relative_to(B2)),
          "junit_totals": totals, "f1_native_failures": len(native["failures"]),
          "author_vs_independent_counts_exact": True,
          "cold_replay_receipts_and_final_hash_exact": True,
          "positive_final_hash": positive["final_hash"],
          "journal_only_final_hash": control["final_hash"],
          "f1_native_failure_ids": [r["case_id"] for r in native["failures"]],
          "f1_boundary_pass": 19, "f1_not_applicable": 17}
(OUT / "source_and_execution_audit.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ("sealed_start", "b2_pin", "b2_tracked_files_verified", "imported_files_and_archive_members_verified", "modules", "junit_totals", "f1_native_failures")}, indent=2))
