#!/usr/bin/env python3
"""S0 Pyat stranded-source tree/blob reconciliation only. Never import or execute branch code."""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCOPE = Path(__file__).resolve().parent / "SCOPED_ROSTER"
BASE = "refs/remotes/origin/integration/pre-main-reconciliation-r1"
SHA = re.compile(r"^[0-9a-f]{40}$")
FUNCTIONAL = ("rawlsing_next/", "src/", "tests/", "scripts/", "data/ddm_build_copy/")
GROUPS = ("S1", "S2", "S3", "S4", "S5")


def git(*args, check=True):
    p = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=False)
    if check and p.returncode:
        raise RuntimeError("git " + " ".join(args[:4]) + " refused: " + p.stderr.decode(errors="replace")[-700:])
    return p.stdout if p.returncode == 0 else None


def json_file(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha_ref(ref):
    value = git("rev-parse", "--verify", ref).decode().strip()
    if not SHA.fullmatch(value):
        raise ValueError("INVALID_COMMIT_REF")
    return value


def blobs_at(ref):
    raw = git("ls-tree", "-r", "-z", "--full-tree", ref)
    result = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        header, name = record.split(b"\t", 1)
        mode, objtype, blob = header.decode().split(" ")
        result[name.decode("utf-8", errors="surrogateescape")] = (objtype, blob)
    return result


def read_diff(merge_base, tip, current):
    raw = git("diff", "--raw", "--no-renames", "--abbrev=40", "-z", merge_base, tip)
    parts = raw.split(b"\0")
    rows = []
    for ix in range(0, len(parts) - 1, 2):
        if not parts[ix]:
            continue
        meta = parts[ix].decode().split(" ")
        name = parts[ix + 1].decode("utf-8", errors="surrogateescape")
        status = meta[-1]
        candidate_blob = meta[-2] if status != "D" else None
        current_blob = current.get(name, (None, None))[1]
        current_type = current.get(name, (None, None))[0]
        if status == "D":
            grade = "DELETED_IN_BRANCH__CURRENT_PRESENT" if current_blob else "DELETED_IN_BRANCH__CURRENT_ABSENT"
        elif current_blob is None:
            grade = "MISSING_CURRENT_PATH"
        elif candidate_blob == current_blob:
            grade = "EXACT_BLOB_PRESENT_CURRENT"
        else:
            grade = "DIFFERENT_BLOB_CURRENT__NEEDS_FUNCTIONAL_COMPARISON"
        rows.append({"path": name, "status": status, "candidate_blob": candidate_blob,
                     "current_blob": current_blob, "current_type": current_type,
                     "path_blob_grain": grade,
                     "relevant_code_path": name.startswith(FUNCTIONAL)})
    return rows


def fetch_sha_batch(shas):
    missing = []
    for off in range(0, len(shas), 20):
        chunk = shas[off:off + 20]
        command = ["fetch", "--no-tags", "--filter=blob:none", "origin", *chunk]
        if git(*command, check=False) is None:
            for sha in chunk:
                if git("fetch", "--no-tags", "--filter=blob:none", "origin", sha, check=False) is None:
                    missing.append(sha)
    return missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", choices=GROUPS, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    spec = json_file(SCOPE / "11_00_SCOPED_HEAD_ROSTER_MANIFEST.json")
    entry = next(v for v in spec["rosters"] if v["worker"] == args.shard)
    roster_path = ROOT / entry["path"]
    if git("hash-object", str(roster_path)).decode().strip() != entry["git_blob_sha"]:
        raise ValueError("FROZEN_ROSTER_BLOB_MISMATCH")
    roster = json_file(roster_path)
    heads = roster["branch_heads"]
    if len(heads) != entry["branches"] or len({x["branch"] for x in heads}) != len(heads):
        raise ValueError("FROZEN_ROSTER_NAMES_MISMATCH")
    if len({x["tip_sha"] for x in heads}) != entry["unique_tip_sha_count"]:
        raise ValueError("FROZEN_ROSTER_TIP_COUNT_MISMATCH")

    canonical = sha_ref(BASE)
    current = blobs_at(canonical)
    unique_heads = sorted({x["tip_sha"] for x in heads})
    missing_fetch = set(fetch_sha_batch(unique_heads))
    args.out.mkdir(parents=True, exist_ok=True)
    source_path = args.out / (args.shard + "_blob_path_index.jsonl")
    errors = []
    states = collections.Counter()
    code_counts = collections.Counter()
    with source_path.open("w", encoding="utf-8") as fd:
        for row in heads:
            name, tip = row["branch"], row["tip_sha"]
            result = {"branch": name, "pinned_tip": tip, "shard": args.shard,
                      "kind_from_roster": row["kind"], "tip_date": row["committer_time_utc"],
                      "receiving_current_sha": canonical, "index_state": "INCOMPLETE",
                      "changed_paths": [], "no_code_ever_executed": True,
                      "no_scientific_or_adoption_grade": True}
            try:
                if tip in missing_fetch:
                    raise RuntimeError("PINNED_HEAD_FETCH_UNAVAILABLE")
                tree = git("rev-parse", tip + "^{tree}").decode().strip()
                if tree != row["tree_sha"]:
                    raise ValueError("PINNED_HEAD_TREE_MISMATCH")
                common = git("merge-base", canonical, tip)
                if common is None or not common.strip():
                    raise RuntimeError("MERGE_BASE_UNRESOLVED")
                result["merge_base"] = common.decode().strip()
                result["verified_tree"] = tree
                changed = read_diff(result["merge_base"], tip, current)
                result["changed_paths"] = changed
                result["index_state"] = "EXACT_PATH_BLOB_INDEX_ONLY"
                result["changed_file_count"] = len(changed)
                result["changed_code_path_count"] = sum(x["relevant_code_path"] for x in changed)
                for item in changed:
                    states[item["path_blob_grain"]] += 1
                    if item["relevant_code_path"]:
                        code_counts[item["path_blob_grain"]] += 1
            except Exception as exc:
                result["error"] = str(exc)[:850]
                errors.append({"branch": name, "tip": tip, "error": result["error"]})
            fd.write(json.dumps(result, ensure_ascii=True, sort_keys=True) + "\n")
    body = source_path.read_bytes()
    coverage = {"schema": "PYAT_S0_EXACT_PATH_AND_BLOB_INDEX@1",
                "shard": args.shard, "pinned_roster_blob": entry["git_blob_sha"],
                "pinned_roster_names": len(heads), "distinct_pinned_tips": len(unique_heads),
                "current_receiving_sha": canonical,
                "indexed_branches": len(heads) - len(errors),
                "unindexed_branches": len(errors), "path_blob_grains": dict(states),
                "functional_path_blob_grains": dict(code_counts),
                "index_file": source_path.name, "index_file_sha256": hashlib.sha256(body).hexdigest(),
                "errors": errors,
                "index_complete": not errors, "function_equivalence_proved": False,
                "test_or_review_grade_proved": False, "original_source_access": False,
                "science_issuer_or_approval": False, "integration_or_merge": False,
                "creation_time_exception_checked": False,
                "note": "Each branch diff is exact merge-base..tip; path/blob match is not functional equivalence. Move/head drift must be independently rechecked."}
    (args.out / (args.shard + "_coverage.json")).write_text(json.dumps(coverage, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in coverage.items() if k != "errors"}, indent=2))
    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
