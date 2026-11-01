#!/usr/bin/env python3
"""Join the frozen 3,135 variant index to current PRE-MAIN and frozen branch tips."""
from __future__ import annotations
import json, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path

PREMAIN = "8e44ca9c751049d65e6def47600b5c073ee04b29"
DATA = Path("/tmp/rrif_custody")
OUT = Path("WORKER_RETURNS/PYAT_RRIF_CUSTODY_A_SOURCE_LOCATION_R1")


def git(*args: str, check: bool = True) -> str:
    p = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and p.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.strip()}")
    return p.stdout


def load_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def code_type(path: str) -> str:
    name = Path(path).name
    if path.endswith(".py") and ("/tests/" in path or name.startswith("test_")):
        return "PYTHON_TEST"
    if path.endswith(".py"):
        return "PYTHON_IMPLEMENTATION"
    if path.endswith((".json", ".jsonl")):
        return "JSON_DEFINITION_OR_EVIDENCE"
    if path.endswith(".md"):
        return "DOCUMENT"
    return "OTHER"


def main() -> int:
    functions = load_jsonl(DATA / "e8_functions.jsonl")
    families = {x["family_id"]: x for x in load_jsonl(DATA / "e8_families.jsonl")}
    s7 = json.loads((DATA / "s7fix.json").read_text())
    s7families = {x["family_id"]: x for x in s7["corrected_families"]}
    roster = []
    for i in range(1, 6):
        roster += json.loads((DATA / f"pr515_s{i}.json").read_text())["branch_heads"]
    name_to_tip = {x["branch"]: x["tip_sha"] for x in roster}
    tip_to_names = defaultdict(list)
    for x in roster:
        tip_to_names[x["tip_sha"]].append(x["branch"])
    tree = {}
    for line in git("ls-tree", "-r", "--full-tree", PREMAIN).splitlines():
        meta, path = line.split("\t", 1)
        tree[path] = meta.split()[2]
    current_paths = set()
    for fam in families.values():
        current_paths.update(fam["current"].get("current_paths", []))
    last_touch = {}
    for path in sorted(current_paths):
        out = git("log", "-1", "--format=%H|%cI|%s", PREMAIN, "--", path, check=False).strip()
        last_touch[path] = out or None
    # The six corrected boundaries were repaired after the frozen 845 roster.
    boundary_extra = {
        fid: [
            ("agent/pyat-s7-six-boundary-function-family-repair-20261031-r1", "80bc5d9bf6624c2ea04027322947a41c347330aa"),
            ("review/pyat-s7fix-boundary-source-abi-hostile-20261031-r1", "1b89fd49c330e4a2c976e6af8d6c1a5e6dbfb088"),
            ("agent/pyat-s7fix-current-owner-map-correction-20261031-r1", "77a04fff750fd6fa491f3daa9f46fe6a22315010"),
        ]
        for fid in ["S7FAM-41da3f505673271b", "S7FAM-0869c56ad5e0c899", "S7FAM-3ced5b9ab5b98431", "S7FAM-82686a98a4281425", "S7FAM-0808b82fba697141", "S7FAM-5823124c837704c1", "S7FAM-739724b429c79765", "S7FAM-6054813ba02c8e44", "S7FAM-dabfb5ad4dc9f0a4", "S7FAM-a7fe27d3f45643c3", "S7FAM-c7246db42c0322e0"]
    }
    # branch tips for each family
    family_branches = {}
    boundary_extra_tips = {}
    pair_set = set()
    for fid, sf in s7families.items():
        pg = sf.get("preserved_group_fields")
        pg = pg if isinstance(pg, dict) else {}
        branches = [b for b in (pg.get("inherited_branches") or []) if b in name_to_tip]
        if fid in boundary_extra:
            for b, tip in boundary_extra[fid]:
                if b not in branches:
                    branches.append(b)
                boundary_extra_tips.setdefault(fid, []).append({"branch": b, "tip": tip})
        family_branches[fid] = branches
        for b in branches:
            tip = name_to_tip.get(b)
            if not tip:
                continue
            for m in families[fid]["original"]["variants"]:
                path = m.get("path")
                if path:
                    pair_set.add((tip, path))
    # batch-check all frozen tip:path pairs
    lines = [f"{tip}:{path}" for tip, path in sorted(pair_set)]
    batch = subprocess.run(["git", "cat-file", "--batch-check=%(objectname) %(objecttype)"], input="\n".join(lines) + "\n", capture_output=True, text=True)
    if batch.returncode:
        raise RuntimeError(batch.stderr)
    pair_result = {}
    for key, line in zip(sorted(pair_set), batch.stdout.splitlines()):
        pair_result[key] = line.strip()
    branch_stats = {}
    for row in roster:
        b = row["branch"]
        tip = row["tip_sha"]
        cand = []
        for key, val in pair_result.items():
            if key[0] == tip:
                cand.append(val)
        branch_stats[b] = {"tip": tip, "objects": cand}
    ledger = []
    counts = Counter()
    for m in functions:
        fid = m["family_id"]
        fam = families[fid]
        path = m.get("path")
        original_blob = m.get("source_blob")
        fam_current_paths = fam["current"].get("current_paths", [])
        current_blobs = {x["path"]: x["blob"] for x in fam["current"].get("current_path_blobs", [])}
        same_path_exact = bool(path in current_blobs and current_blobs[path] == original_blob)
        other_exact = sorted(p for p, blob in current_blobs.items() if blob == original_blob and p != path)
        same_path_present = path in current_blobs
        same_path_modified = bool(same_path_present and not same_path_exact)
        branches = family_branches.get(fid, [])
        exact_branches = []
        modified_branches = []
        absent_branches = []
        for b in branches:
            tip = name_to_tip.get(b)
            if not tip:
                continue
            result = pair_result.get((tip, path), "missing")
            if result.startswith("missing"):
                absent_branches.append(b)
            else:
                parts = result.split()
                if len(parts) >= 2 and parts[0] == original_blob:
                    exact_branches.append(b)
                else:
                    modified_branches.append(b)
        if same_path_exact:
            loc = "PREMAIN_EXACT_SAME_PATH"
            integration = "CURRENT_PREMAIN_SAME_PATH"
            current_path = path
            current_blob = original_blob
        elif other_exact:
            loc = "PREMAIN_EXACT_OTHER_PATH"
            integration = "CURRENT_PREMAIN_OTHER_PATH_COPY_OR_MOVE_UNVERIFIED"
            current_path = other_exact[0]
            current_blob = original_blob
        elif same_path_modified:
            loc = "PREMAIN_MODIFIED_SAME_PATH"
            integration = "CURRENT_PREMAIN_MODIFIED_SAME_PATH"
            current_path = path
            current_blob = current_blobs.get(path)
        elif exact_branches:
            loc = "BRANCH_TIP_EXACT"
            integration = "FROZEN_BRANCH_TIP_ONLY"
            current_path = path
            current_blob = None
        elif modified_branches:
            loc = "BRANCH_TIP_MODIFIED_OR_UNRELATED"
            integration = "FROZEN_BRANCH_TIP_PRESENT_NOT_EXACT"
            current_path = path
            current_blob = None
        else:
            loc = "NOT_LOCATED"
            integration = "NO_CURRENT_OR_FROZEN_BRANCH_PATH"
            current_path = None
            current_blob = None
        ctype = code_type(path or "")
        if ctype != "PYTHON_IMPLEMENTATION":
            module_class = "EVIDENCE_OR_TEST_OR_DOCUMENT"
        elif loc in ("PREMAIN_EXACT_SAME_PATH", "PREMAIN_EXACT_OTHER_PATH"):
            module_class = "IMPLEMENTATION_CURRENT_EXACT"
        elif loc == "PREMAIN_MODIFIED_SAME_PATH":
            module_class = "IMPLEMENTATION_CURRENT_MODIFIED"
        elif loc == "BRANCH_TIP_EXACT":
            module_class = "IMPLEMENTATION_BRANCH_ONLY_EXACT"
        elif loc == "BRANCH_TIP_MODIFIED_OR_UNRELATED":
            module_class = "IMPLEMENTATION_BRANCH_ONLY_MODIFIED"
        else:
            module_class = "IMPLEMENTATION_NOT_LOCATED"
        counts[loc] += 1
        ledger.append({
            "schema": "RRIF_CUSTODY_CODE_LOCATION@1",
            "function_id": m["function_id"],
            "family_id": fid,
            "family_name": fam.get("family_name"),
            "shard": m.get("shard"),
            "source_path": path,
            "source_symbol": m.get("symbol"),
            "source_blob": original_blob,
            "source_ast_sha1": m.get("ast_sha1"),
            "original_label": m.get("original_label"),
            "corrected_disposition": m.get("corrected_disposition"),
            "code_type": ctype,
            "implementation_class": module_class,
            "branch_names": branches,
            "branch_tips": [{"branch": b, "tip": name_to_tip[b]} for b in branches if b in name_to_tip] + boundary_extra_tips.get(fid, []),
            "branch_attribution": "SPECIAL_BOUNDARY_REPAIR_BRANCHES" if fid in boundary_extra else "FAMILY_INHERITED_BRANCH_SET__EXACT_VARIANT_BRANCH_UNVERIFIED",
            "branch_tip_exact_count": len(exact_branches),
            "branch_tip_exact_branches": [{"branch": b, "tip": name_to_tip[b]} for b in exact_branches],
            "branch_tip_modified_count": len(modified_branches),
            "branch_tip_absent_count": len(absent_branches),
            "current_family_paths": fam_current_paths,
            "current_path": current_path,
            "current_blob": current_blob,
            "current_location": loc,
            "integration_path": integration,
            "receiving_last_path_touch": last_touch.get(current_path) if current_path else None,
            "receiving_commit_scope": "LAST_PATH_TOUCH_NOT_IMPORT_UNLESS_ANCESTRY_VERIFIED",
            "source_grade": "EXACT_SOURCE_BLOB_IDENTITY__SEMANTIC_EQUIVALENCE_NOT_CLAIMED",
            "limitations": [
                "Exact blob identity is not semantic or behavioral equivalence.",
                "Family inherited branches are not proof of exact variant branch attribution.",
                "Current path last-touch is not a merge/cherry-pick proof by itself.",
            ],
        })
    (OUT / "CODE_LOCATION_LEDGER.jsonl").write_text("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in ledger))
    subtraction = [r for r in ledger if r["current_location"] in ("PREMAIN_EXACT_SAME_PATH", "PREMAIN_EXACT_OTHER_PATH", "BRANCH_TIP_EXACT") or r["code_type"] != "PYTHON_IMPLEMENTATION"]
    uncertain = [r for r in ledger if r["implementation_class"] in ("IMPLEMENTATION_CURRENT_MODIFIED", "IMPLEMENTATION_BRANCH_ONLY_MODIFIED", "IMPLEMENTATION_NOT_LOCATED")]
    (OUT / "EXACT_CURRENT_SUBTRACTION.json").write_text(json.dumps({
        "schema": "RRIF_CUSTODY_EXACT_CURRENT_SUBTRACTION@1",
        "premain": PREMAIN,
        "count": len(subtraction),
        "rule": "Exact current blob, exact frozen branch blob, or non-implementation evidence/test/document. No semantic equivalence or integration is claimed.",
        "limitations": ["Branch-tip exact means source exists on a frozen branch, not that it is merged.", "Exact current blob means source identity only, not behavioral equivalence or adoption."],
        "functions": [{"function_id": r["function_id"], "family_id": r["family_id"], "current_location": r["current_location"], "current_path": r["current_path"], "current_blob": r["current_blob"]} for r in subtraction],
    }, indent=2) + "\n")
    (OUT / "UNCERTAIN_OR_MISSING_CODE.jsonl").write_text("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in uncertain))
    summary = {
        "schema": "RRIF_CUSTODY_VARIANT_COUNTS@1",
        "functions": len(ledger), "families_with_variants": len({r["family_id"] for r in ledger}), "e8_families": len(families), "external_zero_member_families": 2, "branch_names": len(roster),
        "current_location_counts": dict(sorted(counts.items())),
        "implementation_class_counts": dict(sorted(Counter(r["implementation_class"] for r in ledger).items())),
        "exact_current_subtraction": len(subtraction),
        "uncertain_or_missing_code": len(uncertain),
        "branch_tip_exact_functions": sum(1 for r in ledger if r["current_location"] == "BRANCH_TIP_EXACT"),
        "premain_same_path_exact": sum(1 for r in ledger if r["current_location"] == "PREMAIN_EXACT_SAME_PATH"),
        "premain_other_path_exact": sum(1 for r in ledger if r["current_location"] == "PREMAIN_EXACT_OTHER_PATH"),
        "premain_modified_same_path": sum(1 for r in ledger if r["current_location"] == "PREMAIN_MODIFIED_SAME_PATH"),
        "not_located": sum(1 for r in ledger if r["current_location"] == "NOT_LOCATED"),
    }
    (OUT / "CODE_LOCATION_COUNTS.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
