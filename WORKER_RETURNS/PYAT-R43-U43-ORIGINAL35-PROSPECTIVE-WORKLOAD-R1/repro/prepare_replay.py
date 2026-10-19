"""Reconstruct exact inherited test programs and a separate U43 repaired candidate.

Only sourcefree code/metadata are selected. No original microdata are fetched.
The repair is confined to the candidate harness. Existing native owners and
frozen reviewer assertions are byte-preserved. Git is needed for preparation,
not for relocated execution of the staged closure.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

R = Path(__file__).resolve().parents[1]
WT = R.parents[1]
P4 = "WORKER_RETURNS/PYAT-USERDIRECT-20261015-R9-WG0P4-EXACT-FRONTIER-COLD-REPAIR-R1/"
L = "WORKER_RETURNS/PYAT-USERDIRECT-20261015-R10-WG0L-INDEPENDENT-FULL-ENGINE-COURT-R1/"
P4_SHA = "20d781c8502662bf788b60b828e46df55898d687"
L_SHA = "bec9a128922e4e431ce2ed862aa7802c902813ed"


def git(*args):
    return subprocess.check_output(["git", "-c", "gc.auto=0", "-C", str(WT), *args])


def extract(sha, prefix, dest, select):
    result = []
    for line in git("ls-tree", "-r", sha, prefix).decode().splitlines():
        meta, path = line.split("\t"); mode, kind, blob = meta.split()
        rel = path[len(prefix):]
        if kind != "blob" or mode == "120000" or not select(rel):
            continue
        data = git("cat-file", "blob", blob)
        if hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() != blob:
            raise ValueError("GIT_BLOB_MISMATCH")
        target = dest / rel; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
        result.append(dict(commit=sha, path=path, blob=blob, sha256=hashlib.sha256(data).hexdigest(),
            staged_path=str(target.relative_to(dest))))
    return result


def repair(text):
    # Bind every execution-consumed BoundSpec field at qualified compilation,
    # not only the query/predicate. Existing external owner journal anchors the
    # resulting contract; caller recomputation cannot register a new plan.
    before = "dict(unit=u.semantic_projection(),query=specs[k].query.semantic_projection(),predicate=specs[k].predicate.semantic_projection())"
    after = "dict(unit=u.semantic_projection(),query=specs[k].query.semantic_projection(),predicate=specs[k].predicate.semantic_projection(),descriptor=_plain(vars(specs[k])))"
    before_check = "dict(unit=u.semantic_projection(),query=plan.op_specs[k].query.semantic_projection(),predicate=plan.op_specs[k].predicate.semantic_projection())"
    after_check = "dict(unit=u.semantic_projection(),query=plan.op_specs[k].query.semantic_projection(),predicate=plan.op_specs[k].predicate.semantic_projection(),descriptor=_plain(vars(plan.op_specs[k])))"
    if text.count(before) != 1 or text.count(before_check) != 1:
        raise ValueError("EXACT_P4_REPAIR_PREIMAGE_MISSING")
    text = text.replace(before, after).replace(before_check, after_check)
    preimage = "def _check_plan(plan):\n    plan.fixture_owner.assert_plan_issued(plan)"
    replacement = "def _check_plan(plan):\n    if set(plan.op_specs)!=set(plan.units_by_op):raise IdentityError('COMPLETE_DESCRIPTOR_UNIT_KEYSET_MISMATCH')\n    plan.fixture_owner.assert_plan_issued(plan)"
    if text.count(preimage) != 1:
        raise ValueError("EXACT_CHECK_PLAN_PREIMAGE_MISSING")
    return text.replace(preimage, replacement)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "repaired"
    if mode not in {"baseline", "repaired", "current-p10"}:
        raise ValueError("mode baseline|repaired|current-p10")
    dest = WT / "LOCAL_COURTS" / ("u43-" + mode)
    if dest.exists():
        raise ValueError("REFUSE_OVERWRITE_REPLAY:" + str(dest))
    p4 = dest / "runtime_phase_b/candidate"
    source_rows = extract(P4_SHA, P4, p4, lambda p: not p.startswith("observations/"))
    extract(L_SHA, L, dest, lambda p: p.startswith(("repro/", "tests/")) or p in {
        "01_FROZEN_EXPECTATIONS_BEFORE_WG0P4.json",
        "observations/phase_b/reviewer_second_frontier_register.json"})
    (p4 / "observations").mkdir(exist_ok=True)
    (dest / "observations/phase_b").mkdir(parents=True, exist_ok=True)
    if mode in {"repaired", "current-p10"}:
        path = p4 / "repro/wg0p4_workload.py"
        original = (R / "inputs/wg0x/sources/WG0P10_repaired_workload.py").read_bytes() if mode == "current-p10" else path.read_bytes()
        path.write_text(repair(original.decode()))
        import difflib
        (R / ("evidence/current_p10_descriptor_repair.diff" if mode == "current-p10" else "evidence/wg0p4_descriptor_repair.diff")).write_text("".join(difflib.unified_diff(
            original.decode().splitlines(True), path.read_text().splitlines(True),
            fromfile="WG0P4@20d781c8/repro/wg0p4_workload.py", tofile="U43/repro/wg0p4_workload.py")))
    # The original reviewer source check remains active for exact native owners.
    for row in source_rows:
        path = p4 / row["staged_path"]
        row["staged_path"] = str(path.relative_to(dest))
        row["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    (dest / "observations/phase_b/candidate_read_cut.json").write_text(json.dumps(dict(source_rows=source_rows), indent=2)+"\n")
    # A new transport changes only how pre-execution commitment is observed in a
    # relocated copy: immutable frozen input hash instead of ambient git HEAD.
    adapter = (dest / "repro/phase_b_adapter_v1.py").read_text()
    start = adapter.index(" def register_committed(self):")
    end = adapter.index(" def ensure_cold(self):", start)
    expected = hashlib.sha256((dest / "observations/phase_b/reviewer_second_frontier_register.json").read_bytes()).hexdigest()
    adapted = adapter[:start] + " def register_committed(self):\n  return hashlib.sha256((R/'observations/phase_b/reviewer_second_frontier_register.json').read_bytes()).hexdigest()==" + repr(expected) + "\n" + adapter[end:]
    (dest / "repro/u43_reviewer_transport.py").write_text(adapted)
    print(json.dumps(dict(mode=mode, staged=str(dest), files=len(source_rows),
        original65_assertions="BYTE_IDENTICAL", transport="u43_reviewer_transport",
        repair_sha256=hashlib.sha256((p4/"repro/wg0p4_workload.py").read_bytes()).hexdigest())))


if __name__ == "__main__":
    main()
