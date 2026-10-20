"""01/02 — sealed tree census, path classification, environment and refs."""
from __future__ import annotations

import json
import platform
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C


def refs_snapshot():
    raw = C.git("for-each-ref", "--format=%(refname)\t%(objectname)\t%(objecttype)")
    heads, remotes, tags, other = [], [], [], []
    for line in raw.splitlines():
        name, sha, kind = line.split("\t")
        row = dict(ref=name, head=sha, type=kind)
        if name.startswith("refs/heads/"):
            heads.append(row)
        elif name.startswith("refs/remotes/"):
            remotes.append(row)
        elif name.startswith("refs/tags/"):
            tags.append(row)
        else:
            other.append(row)
    return dict(heads=heads, remotes=remotes, tags=tags, other=other)


def worktrees():
    raw = C.git("worktree", "list", "--porcelain")
    out, cur = [], {}
    for line in raw.splitlines():
        if not line:
            if cur:
                out.append(cur)
                cur = {}
            continue
        key, _, value = line.partition(" ")
        cur[key] = value or True
    if cur:
        out.append(cur)
    return out


def main():
    C.OUT.mkdir(parents=True, exist_ok=True)
    C.EVID.mkdir(parents=True, exist_ok=True)
    status = C.git("status", "--porcelain")
    tree = C.ls_tree()
    sizes = C.blob_sizes([row["blob"] for row in tree])
    rows = []
    for row in tree:
        category = C.classify_path(row["path"])
        rows.append((row["mode"], row["kind"], row["blob"], sizes.get(row["blob"], -1),
                     category, C.parent_top(row["path"]), row["path"]))
    rows.sort(key=lambda r: r[-1])
    tsv = C.write_tsv(C.OUT / "02_ALL_PINNED_TREE_FILES.tsv",
                      ("mode", "kind", "blob", "size", "category", "parent_top", "path"),
                      rows)
    categories = Counter(r[4] for r in rows)
    parents = {}
    for r in rows:
        p = parents.setdefault(r[5], Counter())
        p[r[4]] += 1
    parents_out = {k: dict(sorted(v.items())) for k, v in sorted(parents.items())}
    refs = refs_snapshot()
    lfs = C.run(["git", "lfs", "ls-files"], check=False)
    lfs_count = len(lfs.stdout.splitlines()) if lfs.returncode == 0 else None
    sub = C.run(["git", "config", "--file", ".gitmodules", "--get-regexp", "path"], check=False)
    submodules = sub.stdout.splitlines() if sub.returncode == 0 else []
    partial = C.run(["git", "config", "--get", "remote.origin.partialclonefilter"], check=False)
    counts = C.git("count-objects", "-vH")
    payload = dict(
        schema="R53_U53F_REPOSITORY_SCOPE_AND_COMPLETENESS@1",
        sealed_startup=C.SEALED,
        observed_head=C.git("rev-parse", "HEAD").strip(),
        branch=C.git("rev-parse", "--abbrev-ref", "HEAD").strip(),
        generated_from_sealed_commit=C.git("show", "-s", "--format=%cI", C.SEALED).strip(),
        environment=dict(
            os=platform.platform(), machine=platform.machine(),
            python=sys.version.split()[0], git=C.git("--version").strip(),
            cwd=str(C.ROOT)),
        worktree_status_porcelain=status.splitlines(),
        worktree_status_count=len(status.splitlines()),
        refs=dict(
            counts=dict(heads=len(refs["heads"]), remotes=len(refs["remotes"]),
                        tags=len(refs["tags"]), other=len(refs["other"])),
            heads=refs["heads"], remotes=refs["remotes"], tags=refs["tags"],
            other=refs["other"],
            remote_freshness="not re-fetched for this forensic run; local refs frozen at run time"),
        worktrees=worktrees(),
        submodules=submodules,
        lfs_file_count=lfs_count,
        partial_clone_filter=(partial.stdout.strip() if partial.returncode == 0 else None),
        object_availability=counts.splitlines(),
        census=dict(
            tracked_file_count=len(rows),
            category_counts=dict(sorted(categories.items())),
            per_parent_category_counts=parents_out,
            tsv_manifest_sha256=tsv,
            blob_kind_counts=dict(sorted(Counter(r[1] for r in rows).items())),
            total_blob_bytes=sum(max(0, r[3]) for r in rows),
        ),
        completeness_limitations=[
            "Only paths tracked in the sealed Git tree are provably covered; untracked working files elsewhere are UNKNOWN.",
            "Refs not selected by the material branch algorithm are counted but their diffs are not scanned.",
            "No raw respondent SAV/DTA or source secret was opened; archive/source binaries are classified, not read.",
            "Remote ref freshness was not re-fetched during this run.",
            "Repository-wide absence claims are bounded by this census and the material-ref scan.",
        ])
    C.write_json(C.OUT / "01_REPOSITORY_SCOPE_AND_COMPLETENESS.json", payload)
    C.write_json(C.EVID / "index_tree_receipt.json",
                 dict(census_manifest=tsv, tracked=len(rows),
                      category_counts=dict(sorted(categories.items()))))
    print(json.dumps(dict(tracked=len(rows), categories=dict(sorted(categories.items())),
                          refs=payload["refs"]["counts"], tsv=tsv), indent=1))


if __name__ == "__main__":
    main()
