#!/usr/bin/env python3
"""Refresh-verify the frozen O-INDEX source manifest against real Git objects.

Offline validation checks registry/manifest consistency only. This command is
the qualified S2 check: it resolves every commit:path through Git, verifies the
object type and object id, and compares the manifest timestamp with the actual
commit time. It never imports or executes the indexed source.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout.strip()


def _derive_source_kind(object_type: str, path: str) -> str:
    if object_type == "tree":
        return "source_tree"
    extension = path.rsplit(".", 1)[-1].lower() if "." in path.rsplit("/", 1)[-1] else ""
    if extension == "py":
        return "executable_source"
    if extension == "md":
        return "documentary_definition"
    if extension in ("json", "jsonl"):
        return "json_definition_or_evidence"
    return "opaque_blob"


def _same_time(left: str, right: str) -> bool:
    try:
        return (datetime.fromisoformat(left.replace("Z", "+00:00"))
                == datetime.fromisoformat(right.replace("Z", "+00:00")))
    except (TypeError, ValueError):
        return False


def verify(root: Path, repo: Path) -> dict[str, Any]:
    manifest = json.loads((root / "source_manifest.json").read_text(encoding="utf-8"))
    rows = manifest.get("rows", [])
    references = manifest.get("reference_sources", [])
    errors: list[str] = []
    expected_digest = hashlib.sha256(json.dumps(
        rows + references, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if manifest.get("manifest_digest") != expected_digest:
        errors.append("manifest_digest_mismatch")
    if len(rows) != 167:
        errors.append(f"row_count:{len(rows)}")
    policy = manifest.get("consumer_evidence_policy", {})
    if policy.get("actual_consumer_admissible") is not False:
        errors.append("actual_consumer_policy_not_forbidden")
    expected_counts = policy.get("expected_counts", {})
    if expected_counts.get("TOTAL_NONE_PROVEN_AT_PREMAIN") != 135 or expected_counts.get("ACTUAL") != 0:
        errors.append("consumer_evidence_denominator_policy_mismatch")
    none_proven = sum(1 for row in rows if row.get("actual_consumer_state") == "NONE_PROVEN_AT_PREMAIN")
    actual = sum(1 for row in rows if row.get("actual_consumer_state") == "ACTUAL")
    if none_proven != 135:
        errors.append(f"none_proven_count:{none_proven}")
    if actual != 0:
        errors.append(f"actual_consumer_count:{actual}")
    for item in rows + references:
        label = item.get("namespace", "REF") + ":" + str(item.get("id", item.get("label")))
        commit = item.get("commit", "")
        path = item.get("path", "")
        object_type = item.get("object_type", "")
        object_id = item.get("object_id", "")
        timestamp = item.get("source_timestamp", "")
        try:
            actual_type = _git(repo, "cat-file", "-t", f"{commit}:{path}")
            actual_id = _git(repo, "rev-parse", f"{commit}:{path}")
            actual_time = _git(repo, "show", "-s", "--format=%cI", commit)
        except RuntimeError as error:
            errors.append(f"{label}:git_object_missing:{error}")
            continue
        if actual_type != object_type:
            errors.append(f"{label}:object_type:{actual_type}!={object_type}")
        if actual_id != object_id:
            errors.append(f"{label}:object_id:{actual_id}!={object_id}")
        if not _same_time(actual_time, timestamp):
            errors.append(f"{label}:timestamp:{actual_time}!={timestamp}")
        if item.get("source_kind") != _derive_source_kind(object_type, path):
            errors.append(f"{label}:source_kind_not_derived")
        if item.get("actual_consumer_evidence") is not None:
            errors.append(f"{label}:forbidden_actual_consumer_evidence")
        if item.get("actual_consumer_state") == "ACTUAL":
            errors.append(f"{label}:actual_consumer_forbidden")
        if object_type == "tree":
            tree_files = item.get("tree_files", [])
            actual_files = _git(repo, "ls-tree", "-r", "--name-only", f"{commit}:{path}").splitlines()
            if tree_files != actual_files:
                errors.append(f"{label}:tree_files")
    return {
        "schema": "SOROK_OINDEX_SOURCE_MANIFEST_REFRESH@1",
        "result": "PASS" if not errors else "FAIL",
        "rows": len(rows),
        "references": len(references),
        "manifest_digest": expected_digest,
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parent)
    parser.add_argument("--repo", type=Path,
                        default=Path(__file__).resolve().parents[3])
    args = parser.parse_args(argv)
    report = verify(args.root, args.repo)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
