"""03 — material worker ref inventory and branch-diff file blobs."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

MATERIAL_PATTERNS = re.compile(
    r"(rawlsing_next|pre553|i05|i03|g50|b49|i51|f43|j42|w41|e41|p41|f6|f7|world|"
    r"selected|learned|source|workload|n9|n10|consumer|universal|closed35|all35|"
    r"temporal|field.?forge|ff-|r4[3-9]|r5[0-3]|lits|q301|carrier|route.?b|c11|"
    r"e04|e05|n9j|t35|ee1|o35b|r39i|s03fo|f6m|f6p)", re.I)
MANDATED = {
    "b5600da96358f8526471d635a1befa8daa3f098b": "B49_return",
    "d379bafe36b8d89da27ea5bf33614d33aca7f2d2": "G50_return",
    "9bbf9e0509411beb210331d28160324b005a784e": "I51_return",
    "100ae7832ddc2c5edb7abdbd7e2cb94b5f9e8733": "F43_return",
    "f53cb0d2bce52640268c844c398bbd8007d28edc": "J42_return",
    "b0a68e4ff5d5e2ca62b080376fda6b5f5431a6c2": "W41_return",
    "6e123bafe749d6997c764ae117fb5e68e0139ed7": "E41_return",
    "f27d1101048638bba395143a48efb7ef00bfcda4": "P41_return",
}
SHARD = 50000


def refs():
    raw = C.git("for-each-ref", "--format=%(refname)\t%(objectname)\t%(objecttype)")
    rows = []
    for line in raw.splitlines():
        name, sha, kind = line.split("\t")
        rows.append(dict(ref=name, head=sha, type=kind))
    for sha, label in MANDATED.items():
        if not any(r["head"] == sha for r in rows):
            rows.append(dict(ref=f"mandated:{label}", head=sha, type="commit"))
    return rows


def subject(sha):
    out = C.git("show", "-s", "--format=%H%x09%ci%x09%s", sha)
    return out.split("\t", 2)


def parse_raw_diff(base, head):
    raw = C.git_bytes("diff", "--no-renames", "--raw", "--no-abbrev", "-z", base, head)
    parts = raw.split(b"\0")
    rows = []
    i = 0
    while i + 1 < len(parts):
        meta = parts[i]
        if not meta:
            i += 1
            continue
        if meta.startswith(b":"):
            fields = meta[1:].decode().split()
            path = parts[i + 1].decode("utf-8", "surrogateescape")
            rows.append(dict(path=path, status=fields[4],
                             blob=(fields[3] if set(fields[3]) != {"0"} else fields[2]),
                             old_blob=fields[2], new_blob=fields[3]))
            i += 2
        else:
            i += 1
    return rows


def relevance(path):
    if path.startswith("rawlsing_next/") or path.startswith("data/"):
        return "RELEVANT_CODE_OR_DATA"
    if path.startswith("WORKER_RETURNS/") or path.startswith("WORKER_COMMISSIONS/"):
        return "RELEVANT_WORKER_EVIDENCE"
    if path.startswith("PYAT_CONTROL_ROOM/") or path.startswith("HQ_HANDOFF/"):
        return "RELEVANT_CONTROL_DOC"
    if path.startswith("tests/"):
        return "RELEVANT_TEST"
    return "OTHER_CHANGED_PATH"


def main():
    C.OUT.mkdir(parents=True, exist_ok=True)
    rows = refs()
    ledger = []
    shard_rows = []
    material = 0
    for row in rows:
        name, head = row["ref"], row["head"]
        try:
            sha, date, subj = subject(head)
        except Exception:
            ledger.append(dict(ref=name, head=head, included=False,
                               reason="HEAD_UNREADABLE"))
            continue
        base = C.run(["git", "merge-base", C.SEALED, head], check=False)
        base_sha = base.stdout.strip() if base.returncode == 0 else ""
        by_name = bool(MATERIAL_PATTERNS.search(name)) or name.startswith("mandated:")
        by_subject = bool(MATERIAL_PATTERNS.search(subj))
        if head == C.SEALED:
            ledger.append(dict(ref=name, head=head, subject=subj, included=False,
                               reason="SAME_AS_SEALED"))
            continue
        if not (by_name or by_subject):
            ledger.append(dict(ref=name, head=head, subject=subj, included=False,
                               reason="NON_MATERIAL_SCOPE_RULE"))
            continue
        material += 1
        if base_sha:
            changed = parse_raw_diff(base_sha, head)
            relation = "MERGE_BASE"
        else:
            tree = C.ls_tree(head)
            changed = [dict(path=e["path"], status="A", blob=e["blob"],
                            old_blob="", new_blob=e["blob"]) for e in tree]
            relation = "UNRELATED_BASE_MISSING__FULL_TREE"
        ledger.append(dict(ref=name, head=head, subject=subj, date=date,
                           included=True, reason="MATERIAL_NAME" if by_name else "MATERIAL_SUBJECT",
                           merge_base=base_sha, relation=relation,
                           changed_paths=len(changed)))
        for item in changed:
            shard_rows.append((name, row["type"], head, subj, date, base_sha,
                               relation, item["status"], item["path"],
                               item["new_blob"] or item["old_blob"],
                               relevance(item["path"])))
    # sizes
    sizes = C.blob_sizes([r[9] for r in shard_rows if r[9]])
    final = [(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9],
              sizes.get(r[9], -1), r[10]) for r in shard_rows]
    header = ("ref", "ref_type", "head", "subject", "date", "merge_base", "relation",
              "status", "path", "blob", "size", "relevance")
    shard_manifest = []
    if len(final) <= SHARD:
        digest = C.write_tsv(C.OUT / "03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.tsv",
                             header, final)
        shard_manifest.append(dict(file="03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.tsv",
                                   rows=len(final), sha256=digest))
    else:
        for index in range(0, len(final), SHARD):
            name = f"03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part{index // SHARD:02d}.tsv"
            digest = C.write_tsv(C.OUT / name, header, final[index:index + SHARD])
            shard_manifest.append(dict(file=name,
                                       rows=len(final[index:index + SHARD]),
                                       sha256=digest))
        C.write_json(C.OUT / "03_MATERIAL_BRANCH_DIFF_INDEX.json",
                     dict(schema="R53_U53F_MATERIAL_BRANCH_DIFF_INDEX@1",
                          total_rows=len(final), shards=shard_manifest,
                          material_refs=material, all_refs=len(rows)))
    payload = dict(
        schema="R53_U53F_REF_INVENTORY@1",
        sealed=C.SEALED,
        total_refs=len(rows),
        material_refs=material,
        excluded_refs=len(rows) - material,
        included=[r for r in ledger if r.get("included")],
        excluded_summary=dict(Counter(r.get("reason") for r in ledger
                                      if not r.get("included"))),
        mandate_note="Material selection: name/subject regex over universal/source/I03/I05/F6/F7/"
                     "world/consumer lanes plus mandated return commits; exclusions and bases recorded "
                     "per ref. Non-material refs are counted, not diff-scanned.",
        diff_rows=len(final),
        shard_manifest=shard_manifest)
    C.write_json(C.EVID / "ref_inventory.json", payload)
    print(json.dumps(dict(refs=len(rows), material=material,
                          diff_rows=len(final), shards=shard_manifest), indent=1))


if __name__ == "__main__":
    main()
