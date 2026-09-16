#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import io
import json
import pathlib
import subprocess

THIS = pathlib.Path(__file__).resolve()
ROOT = THIS.parents[2]

EE_R2D_COMMIT = "ec1d5dc11a13290853632d7ab967b6094f2b9955"
EE_R2D_REGISTRY = "WORKER_RETURNS/EE-R2D/02_SOURCE_RULE_BATCH_REGISTRY.json"
B03_COMMIT = "3d1cdd242fe10f544bdcbb5bb91cf042c56ef787"
B03_ROOT = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/RESIDUAL_ZERO_LOSS_EXECUTION_WAVE_R2/B03_ROUTING_GSS_WVS_EVS"
)
NATIVE = f"{B03_ROOT}/NATIVE_CURRENT_REBIND_06.csv"
DERIVATIVE = f"{B03_ROOT}/DERIVATIVE_ONLY_CURRENT_REBIND.csv"
RULINGS = THIS.parent / "01_EXACT_19_WVS_ROUTING_RULINGS.csv"
EXPECTED_SORTED_ID_SHA256 = "fd10aa916e0c7a58d008d2194dbe20083f1d85f9da66958fa5bb34ef0951daec"
EXPECTED_RULINGS_SHA256 = "d5b4e5bad9e53675691574246f7a32473572ff831f08d4425250c80614bb0c61"
EXPECTED_SOURCE_RETURN_SHA256 = "d23abc9e786b4d6093bbf7bd9be9f15c7a3ca1384ba47723d532a082141359cc"

def git_show(ref: str, path: str) -> bytes:
    p = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if p.returncode:
        raise AssertionError(p.stderr.decode(errors="replace"))
    return p.stdout

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

registry = json.loads(git_show(EE_R2D_COMMIT, EE_R2D_REGISTRY))
unit = next(x for x in registry["units"] if x["unit_id"] == "EE-R2D-B02-WVS-B03-W07")
selected = unit["question_implementation_ids"]
assert len(selected) == 19 == len(set(selected))
assert unit["source_family"] == "WVS"
assert unit["coverage_basis"]["owner_resolution_mode"] == "EXACT_QID_LOOKUP_WITHIN_PINNED_W07_ONLY"
assert unit["coverage_basis"]["shared_rule_asserted"] is False
assert unit["source_rule_owner_refs"] == [{
    "authority_code": "B03-W07",
    "commit": B03_COMMIT,
    "source_path": "RETURN_U1/O06_IMPLEMENTATION_ROUTING.jsonl",
    "source_return_sha256": EXPECTED_SOURCE_RETURN_SHA256
}]
assert sha256(("".join(q + "\n" for q in sorted(selected))).encode()) == EXPECTED_SORTED_ID_SHA256

native_rows = list(csv.DictReader(io.StringIO(git_show(B03_COMMIT, NATIVE).decode("utf-8-sig"))))
w07_native = {r["qid"] for r in native_rows if r["worker"] == "W07"}
assert len(w07_native) == 36
assert not (set(selected) & w07_native)

derivative_rows = list(csv.DictReader(io.StringIO(git_show(B03_COMMIT, DERIVATIVE).decode("utf-8-sig"))))
w07_derivative = {r["qid"] for r in derivative_rows if r["worker"] == "W07"}
assert len(w07_derivative) == 0
assert not (set(selected) & w07_derivative)

ruling_bytes = RULINGS.read_bytes()
assert sha256(ruling_bytes) == EXPECTED_RULINGS_SHA256
rulings = list(csv.DictReader(io.StringIO(ruling_bytes.decode("utf-8"))))
assert len(rulings) == 19
assert [x["question_implementation_id"] for x in rulings] == selected
assert all(x["source_family"] == "WVS" for x in rulings)
assert all(x["source_owner"] == "B03-W07" for x in rulings)
assert all(x["predecessor_state"] == "UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY" for x in rulings)
assert all(x["court_disposition"] == "UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY" for x in rulings)
assert all(x["objectizer_ready"] == "false" for x in rulings)

summary = {
    "status": "PASS",
    "selected": len(selected),
    "w07_affirmative_native_qids": len(w07_native),
    "selected_affirmative_intersection": len(set(selected) & w07_native),
    "w07_derivative_qids": len(w07_derivative),
    "selected_derivative_intersection": len(set(selected) & w07_derivative),
    "unresolved_preserved": sum(
        x["court_disposition"] == "UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY" for x in rulings
    ),
    "objectizer_ready": sum(x["objectizer_ready"] == "true" for x in rulings),
    "rulings_sha256": sha256(ruling_bytes),
}
print(json.dumps(summary, sort_keys=True, indent=2))
