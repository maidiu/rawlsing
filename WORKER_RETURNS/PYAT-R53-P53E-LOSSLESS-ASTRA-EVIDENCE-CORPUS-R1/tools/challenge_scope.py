#!/usr/bin/env python3
"""Independent challenge of U53F's tree/ref/row/roster claims.

This is a mechanical, source-free re-derivation. It does not adopt U53F's
causal claims and does not read respondent data or execute production code.
"""
from __future__ import annotations

import csv
import io
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus_common as C

SEALED = C.FALLBACK_SEALED_REF
U = C.U53F_RETURN
MATERIAL_PATTERNS = re.compile(
    r"(rawlsing_next|pre553|i05|i03|g50|b49|i51|f43|j42|w41|e41|p41|f6|f7|world|"
    r"selected|learned|source|workload|n9|n10|consumer|universal|closed35|all35|"
    r"temporal|field.?forge|ff-|r4[3-9]|r5[0-3]|lits|q301|carrier|route.?b|c11|"
    r"e04|e05|n9j|t35|ee1|o35b|r39i|s03fo|f6m|f6p)",
    re.I,
)
BROAD_CANDIDATE = re.compile(
    r"(source|workload|universal|world|consumer|temporal|learned|carrier|i03|i05|"
    r"f6|f7|n9|n10|e04|lits|q301|35|closed|ff|field.?forge|route.?b|c11|j42|p41|"
    r"e41|f43|w41|b49|g50|i51|u43|commission|acceptance|drift|seal|stop)",
    re.I,
)
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


def show_json(path: str):
    return json.loads(C.read_blob(C.tree_map()[U + "/" + path]["blob"]).decode("utf-8"))


def show_bytes(path: str):
    return C.read_blob(C.tree_map()[U + "/" + path]["blob"])


def show_tsv(path: str):
    text = show_bytes(path).decode("utf-8", "replace")
    lines = text.splitlines()
    header = lines[0].split("\t")
    rows = [dict(zip(header, line.split("\t"))) for line in lines[1:]]
    return header, rows


def parse_commits(heads):
    """Return head -> (date_iso, subject, type) using one cat-file process."""
    unique = sorted(set(heads))
    payload = "".join(head + "\n" for head in unique).encode()
    proc = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=str(C.ROOT),
        input=payload,
        capture_output=True,
        check=True,
    )
    raw = proc.stdout
    out = {}
    pos = 0
    while pos < len(raw):
        end = raw.index(b"\n", pos)
        header = raw[pos:end].decode("utf-8", "replace").split()
        pos = end + 1
        if len(header) != 3:
            out[header[0]] = ("", "", "missing")
            continue
        sha, kind, size = header[0], header[1], int(header[2])
        data = raw[pos : pos + size]
        pos += size + 1
        if kind != "commit":
            out[sha] = ("", "", kind)
            continue
        text = data.decode("utf-8", "replace")
        lines = text.split("\n")
        blank = lines.index("") if "" in lines else len(lines)
        headers = lines[:blank]
        message = "\n".join(lines[blank + 1 :])
        subject = message.splitlines()[0] if message.splitlines() else ""
        date_iso = ""
        for line in headers:
            if line.startswith("committer "):
                match = re.search(r" (\d+) ([+-]\d{4})$", line)
                if match:
                    ts = int(match.group(1))
                    date_iso = datetime.fromtimestamp(ts, timezone.utc).isoformat()
                break
        out[sha] = (date_iso, subject, "commit")
    return out


def check(name, passed, actual, expected, source, note="", **extra):
    return {
        "check": name,
        "pass": bool(passed),
        "actual": actual,
        "expected": expected,
        "source": source,
        "note": note,
        **extra,
    }


def main():
    tree = C.tree_map()
    sealed_tree = C.tree_map(SEALED)
    checks = []
    anomalies = []

    # ---------- 01 / 02 tree ledger ----------
    scope01 = show_json("01_REPOSITORY_SCOPE_AND_COMPLETENESS.json")
    header02, rows02 = show_tsv("02_ALL_PINNED_TREE_FILES.tsv")
    ledger = {}
    for row in rows02:
        ledger[row["path"]] = (row["mode"], row["kind"], row["blob"])
    sealed_ledger = {
        path: (entry["mode"], entry["kind"], entry["blob"])
        for path, entry in sealed_tree.items()
    }
    missing = sorted(set(sealed_ledger) - set(ledger))
    extra = sorted(set(ledger) - set(sealed_ledger))
    mismatch = sorted(
        path
        for path in set(ledger) & set(sealed_ledger)
        if ledger[path] != sealed_ledger[path]
    )
    checks.append(
        check(
            "tree_ledger_equality_at_f148f9ba",
            not missing and not extra and not mismatch,
            {"paths": len(ledger), "missing": len(missing), "extra": len(extra), "mismatch": len(mismatch)},
            {"paths": len(sealed_ledger), "missing": 0, "extra": 0, "mismatch": 0},
            "git ls-tree -r -z f148f9ba... vs 02_ALL_PINNED_TREE_FILES.tsv",
            "modes, kinds, blobs and paths compared; sizes checked separately",
        )
    )
    if missing or extra or mismatch:
        anomalies.append(
            {
                "kind": "TREE_LEDGER_DIFF",
                "missing": missing[:50],
                "extra": extra[:50],
                "mismatch": mismatch[:50],
            }
        )
    # sizes
    sizes = C.blob_sizes([row["blob"] for row in rows02])
    size_bad = [
        {"path": row["path"], "tsv": int(row["size"]), "git": sizes.get(row["blob"])}
        for row in rows02
        if int(row["size"]) != sizes.get(row["blob"])
    ]
    checks.append(
        check(
            "tree_ledger_sizes",
            not size_bad,
            {"checked": len(rows02), "bad": len(size_bad)},
            {"checked": 7615, "bad": 0},
            "git cat-file --batch-check on every 02 blob",
        )
    )
    census = scope01["census"]
    checks.append(
        check(
            "tree_census_counts",
            (
                len(rows02) == census["tracked_file_count"] == 7615
                and sum(int(r["size"]) for r in rows02) == census["total_blob_bytes"]
                and Counter(r["category"] for r in rows02) == Counter(census["category_counts"])
            ),
            {
                "rows": len(rows02),
                "total_bytes": sum(int(r["size"]) for r in rows02),
                "categories": len(Counter(r["category"] for r in rows02)),
            },
            {
                "rows": census["tracked_file_count"],
                "total_bytes": census["total_blob_bytes"],
                "categories": len(census["category_counts"]),
            },
            "02 TSV vs 01 census",
        )
    )

    # ---------- refs snapshot and 966 selection ----------
    snap_refs = (
        scope01["refs"]["heads"]
        + scope01["refs"]["remotes"]
        + scope01["refs"]["tags"]
        + scope01["refs"]["other"]
    )
    commit_meta = parse_commits([r["head"] for r in snap_refs])
    refs_all = []
    for r in snap_refs:
        meta = commit_meta.get(r["head"], ("", "", "missing"))
        refs_all.append(
            {
                "ref": r["ref"],
                "head": r["head"],
                "ref_type": r.get("type", "commit"),
                "date": meta[0],
                "subject": meta[1],
                "source": "U53F_SNAPSHOT",
                "head_readable": meta[2] == "commit",
            }
        )
    present_heads = {r["head"] for r in refs_all}
    for sha, label in MANDATED.items():
        if sha not in present_heads:
            meta = commit_meta.get(sha)
            if meta is None:
                meta = parse_commits([sha]).get(sha, ("", "", "missing"))
            refs_all.append(
                {
                    "ref": f"mandated:{label}",
                    "head": sha,
                    "ref_type": "commit",
                    "date": meta[0],
                    "subject": meta[1],
                    "source": "U53F_MANDATED_PSEUDO_REF",
                    "head_readable": meta[2] == "commit",
                }
            )
    for r in refs_all:
        name = r["ref"]
        subj = r["subject"]
        if r["head"] == SEALED and not name.startswith("mandated:"):
            r["included"] = False
            r["reason"] = "SAME_AS_SEALED"
        elif name.startswith("mandated:"):
            r["included"] = True
            r["reason"] = "MANDATED_PSEUDO_REF"
        elif MATERIAL_PATTERNS.search(name):
            r["included"] = True
            r["reason"] = "MATERIAL_NAME"
        elif MATERIAL_PATTERNS.search(subj):
            r["included"] = True
            r["reason"] = "MATERIAL_SUBJECT"
        else:
            r["included"] = False
            r["reason"] = "NON_MATERIAL_SCOPE_RULE"
    included = [r for r in refs_all if r["included"]]
    excluded = [r for r in refs_all if not r["included"]]
    inventory = show_json("evidence/ref_inventory.json")
    inv_inc = {r["ref"]: r for r in inventory["included"]}
    recomp_names = {r["ref"] for r in included}
    checks.append(
        check(
            "ref_snapshot_and_material_selection",
            (
                len(refs_all) == 2615
                and len(included) == 966
                and len(excluded) == 1649
                and recomp_names == set(inv_inc)
            ),
            {
                "refs": len(refs_all),
                "included": len(included),
                "excluded": len(excluded),
                "selection_set_equal": recomp_names == set(inv_inc),
            },
            {"refs": 2615, "included": 966, "excluded": 1649, "selection_set_equal": True},
            "01 refs snapshot + U53F MATERIAL_PATTERNS rule vs evidence/ref_inventory.json",
            "Two mandated commits are pseudo-refs; the U53F branch at the sealed SHA is SAME_AS_SEALED.",
        )
    )
    # attach inventory changed_paths
    for r in refs_all:
        inv = inv_inc.get(r["ref"], {})
        r["changed_paths"] = inv.get("changed_paths")
        r["merge_base"] = inv.get("merge_base")
        r["zero_diff"] = inv.get("changed_paths") == 0
        r["contributes_rows"] = bool(inv.get("changed_paths", 0))

    # ---------- 03 material diff rows ----------
    part_rows = {}
    all03 = []
    for part in (
        "03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part00.tsv",
        "03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part01.tsv",
    ):
        _, rows = show_tsv(part)
        part_rows[part] = rows
        all03.extend(rows)
    ref_counts = Counter(row["ref"] for row in all03)
    idx03 = show_json("03_MATERIAL_BRANCH_DIFF_INDEX.json")
    quality = show_json("QUALITY_CHECKS.json")
    inv_sum = sum(r.get("changed_paths", 0) for r in inventory["included"])
    per_ref_equal = all(
        ref_counts.get(r["ref"], 0) == r.get("changed_paths", 0)
        for r in inventory["included"]
    )
    checks.append(
        check(
            "diff_rows_79487",
            (
                len(all03) == 79487
                and len(part_rows["03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part00.tsv"]) == 50000
                and len(part_rows["03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part01.tsv"]) == 29487
                and idx03["total_rows"] == 79487
                and inv_sum == 79487
                and per_ref_equal
            ),
            {
                "rows": len(all03),
                "part00": len(part_rows["03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part00.tsv"]),
                "part01": len(part_rows["03_MATERIAL_BRANCH_DIFF_FILE_BLOBS.part01.tsv"]),
                "inventory_sum": inv_sum,
                "per_ref_equal": per_ref_equal,
            },
            {
                "rows": 79487,
                "part00": 50000,
                "part01": 29487,
                "inventory_sum": 79487,
                "per_ref_equal": True,
            },
            "03 TSV rows, 03 index, evidence/ref_inventory.json changed_paths",
        )
    )
    contributing = {r["ref"] for r in included if r.get("changed_paths", 0)}
    zero = {r["ref"] for r in included if r.get("changed_paths", 0) == 0}
    checks.append(
        check(
            "material_refs_contributing_rows",
            (
                len(included) == 966
                and len(contributing) == 847
                and len(zero) == 119
                and set(ref_counts) == contributing
            ),
            {
                "selected": len(included),
                "contributing_847": len(contributing),
                "zero_diff_119": len(zero),
                "row_refs": len(ref_counts),
                "row_ref_set_equal": set(ref_counts) == contributing,
            },
            {
                "selected": 966,
                "contributing_847": 847,
                "zero_diff_119": 119,
                "row_refs": 847,
                "row_ref_set_equal": True,
            },
            "recomputation from evidence/ref_inventory.json and 03 refs",
            "The 966 selected refs include 119 with changed_paths=0; only 847 contribute the 79,487 rows. "
            "This is a material clarification, not a row-count error.",
        )
    )

    # ---------- 06 scan hits ----------
    header06, rows06 = show_tsv("06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv")
    leak_receipt = show_json("evidence/leak_scan_receipt.json")
    class_counts = Counter(r["candidate_classification"] for r in rows06)
    sealed_hits = [r for r in rows06 if r["refs"] == "SEALED"]
    sealed_bad = [
        r for r in sealed_hits
        if r["path"] not in sealed_ledger or sealed_ledger[r["path"]][2] != r["blob"]
    ]
    ref_hits = [r for r in rows06 if r["refs"].startswith("refs/")]
    snapshot_ref_names = {r["ref"] for r in refs_all}
    unknown_ref_hits = [r for r in ref_hits if r["refs"] not in snapshot_ref_names]
    blob_ids = sorted({r["blob"] for r in rows06})
    present, missing_blob = C.blob_presence(blob_ids) if hasattr(C, "blob_presence") else (None, None)
    if present is None:
        payload = "".join(blob + "\n" for blob in blob_ids).encode()
        proc = subprocess.run(
            ["git", "cat-file", "--batch-check"],
            cwd=str(C.ROOT),
            input=payload,
            capture_output=True,
            check=True,
        )
        present = 0
        missing_blob = []
        for line in proc.stdout.decode().splitlines():
            fields = line.split()
            if len(fields) == 3:
                present += 1
            else:
                missing_blob.append(fields[0])
    checks.append(
        check(
            "scan_hits_45431",
            (
                len(rows06) == 45431
                and leak_receipt["total_hits"] == 45431
                and class_counts == Counter(leak_receipt["classification_counts"])
                and not sealed_bad
                and not unknown_ref_hits
            ),
            {
                "rows": len(rows06),
                "receipt_total_hits": leak_receipt["total_hits"],
                "classification_equal": class_counts == Counter(leak_receipt["classification_counts"]),
                "sealed_rows": len(sealed_hits),
                "sealed_bad": len(sealed_bad),
                "branch_ref_rows": len(ref_hits),
                "unknown_ref_rows": len(unknown_ref_hits),
                "unique_blobs": len(blob_ids),
                "blobs_present": present,
                "blobs_missing": len(missing_blob),
            },
            {
                "rows": 45431,
                "receipt_total_hits": 45431,
                "classification_equal": True,
                "sealed_bad": 0,
                "unknown_ref_rows": 0,
            },
            "06 TSV row/classification parse; SEALED path+blob check; ref-name check; blob presence check",
            "The 11,305 scanned-Python-blob coverage figure is U53F-authored and is not re-derived by this "
            "access mission; row-level 45,431 hits are independently counted.",
        )
    )
    if missing_blob:
        anomalies.append(
            {
                "kind": "SCAN_BLOBS_NOT_PRESENT_LOCALLY",
                "count": len(missing_blob),
                "sample": missing_blob[:20],
                "note": "These branch-only blobs are not locally materialized; no fetch was attempted. "
                        "The 45,431 rows remain present in the shard, but their blob content cannot be "
                        "independently opened in this workspace.",
            }
        )

    # ---------- 04/05 graph and unresolved edges ----------
    graph_lines = show_bytes("04_UNIVERSAL_PRODUCER_CONSUMER_GRAPH.jsonl").decode("utf-8").splitlines()
    graph = [json.loads(line) for line in graph_lines if line.strip()]
    nodes = [g for g in graph if g.get("record_type") == "node"]
    edges = [g for g in graph if g.get("record_type") == "edge"]
    edge_bad = [
        e for e in edges
        if not all(k in e for k in ("caller_path", "caller_blob", "line", "status"))
    ]
    _, unresolved = show_tsv("05_UNRESOLVED_DYNAMIC_AND_MISSING_EDGES.tsv")
    checks.append(
        check(
            "graph_22_nodes_51_edges",
            len(nodes) == 22 and len(edges) == 51 and not edge_bad,
            {"nodes": len(nodes), "edges": len(edges), "bad_edges": len(edge_bad)},
            {"nodes": 22, "edges": 51, "bad_edges": 0},
            "04 JSONL parse",
        )
    )
    checks.append(
        check(
            "unresolved_edges_9",
            len(unresolved) == 9,
            len(unresolved),
            9,
            "05 TSV data rows",
        )
    )

    # ---------- 07 timeline ----------
    _, timeline = show_tsv("07_HISTORIC_REQUIREMENT_TO_ACCEPTANCE_PROPAGATION.tsv")
    checks.append(
        check(
            "timeline_19_rows",
            len(timeline) == 19,
            len(timeline),
            19,
            "07 TSV data rows",
        )
    )

    # ---------- 08 roster vs frozen registry ----------
    registry_path = "data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv"
    registry_bytes = C.read_blob(C.tree_map(SEALED)[registry_path]["blob"])
    registry = list(csv.DictReader(io.StringIO(registry_bytes.decode("utf-8"))))
    active = [r for r in registry if (r.get("authority_status") or "").strip() != "EXCLUDED_INACTIVE_WAVE"]
    pairs = defaultdict(list)
    for row in active:
        pairs[(row["source_family"].strip(), row["canonical_wave"].strip())].append(row)
    _, roster08 = show_tsv("08_CLOSED35_UNIVERSAL_EXECUTION_COVERAGE.tsv")
    roster_pairs = {(r["source_family"], r["canonical_wave"]): r for r in roster08}
    roster_errors = []
    for key, members in sorted(pairs.items()):
        if key not in roster_pairs:
            roster_errors.append({"pair": key, "error": "missing from 08"})
            continue
        row = roster_pairs[key]
        countries = sorted({m.get("country_code_scope", "") for m in members if m.get("country_code_scope")})
        statuses = sorted({m.get("authority_status", "") for m in members})
        reviews = sorted({m.get("review_status", "") for m in members})
        directional = sum(1 for m in members if (m.get("relation_use_status") or "") == "GOVERNED_DIRECTIONAL")
        expected_country = ",".join(countries) or "UNKNOWN"
        expected_status = statuses[0] if len(statuses) == 1 else "|".join(statuses)
        expected_review = reviews[0] if len(reviews) == 1 else "|".join(reviews)
        expected_sem = f"{len(members)} authority rows; directional={directional}; question/var fields present"
        for field, expected in (
            ("country_scope", expected_country),
            ("authority_status", expected_status),
            ("review_status", expected_review),
            ("semantics_routing_role_weight_evidence", expected_sem),
            ("source_permission_runtime", "UNKNOWN_NOT_GRANTED_IN_THIS_FORENSIC_RUN"),
            ("known_original_U_E_pre_scope", "NOT_ISSUED / NULL"),
            ("format", "UNKNOWN_IN_AUTHORITY_ROW"),
        ):
            if row[field] != expected:
                roster_errors.append(
                    {"pair": key, "field": field, "08": row[field], "registry": expected}
                )
    extra_roster = sorted(set(roster_pairs) - set(pairs))
    checks.append(
        check(
            "closed35_roster_identity_and_nulls",
            (
                len(registry) == 700
                and len(active) == 700
                and len(pairs) == 35
                and all(len(v) == 20 for v in pairs.values())
                and ("Asian Barometer", "W6") not in pairs
                and set(roster_pairs) == set(pairs)
                and not roster_errors
                and not extra_roster
                and len(roster08) == 35
                and all(r["source_permission_runtime"] == "UNKNOWN_NOT_GRANTED_IN_THIS_FORENSIC_RUN" for r in roster08)
                and all(r["known_original_U_E_pre_scope"] == "NOT_ISSUED / NULL" for r in roster08)
            ),
            {
                "registry_rows": len(registry),
                "active_rows": len(active),
                "unique_pairs": len(pairs),
                "rows_per_pair": sorted(set(len(v) for v in pairs.values())),
                "asian_w6": ("Asian Barometer", "W6") in pairs,
                "roster_rows": len(roster08),
                "roster_errors": len(roster_errors),
                "extra_roster": extra_roster,
            },
            {
                "registry_rows": 700,
                "active_rows": 700,
                "unique_pairs": 35,
                "rows_per_pair": [20],
                "asian_w6": False,
                "roster_rows": 35,
                "roster_errors": 0,
                "extra_roster": [],
            },
            "frozen registry CSV at f148f9ba vs 08 TSV",
            "Not a name search: 08 is recomputed from source_family/canonical_wave groups and compared field-by-field.",
        )
    )

    # ---------- 06B document counts ----------
    _, docs = show_tsv("06B_DOCUMENT_REFERENCE_COUNTS.tsv")
    doc_bad = [
        r for r in docs
        if r["path"] not in sealed_ledger or sealed_ledger[r["path"]][2] != r["blob"]
    ]
    checks.append(
        check(
            "document_reference_counts_1398",
            len(docs) == 1398 and not doc_bad,
            {"rows": len(docs), "bad": len(doc_bad)},
            {"rows": 1398, "bad": 0},
            "06B TSV rows and sealed path/blob identity",
        )
    )

    # ---------- current remote snapshot ----------
    proc = subprocess.run(
        ["git", "ls-remote", "origin"],
        cwd=str(C.ROOT),
        capture_output=True,
        check=True,
        timeout=120,
    )
    remote_raw = proc.stdout
    remote_refs = []
    for line in remote_raw.decode("utf-8", "replace").splitlines():
        sha, ref = line.split("\t", 1)
        remote_refs.append({"ref": ref, "head": sha})
    remote_snapshot_path = C.RECEIPTS / "remote_refs_snapshot.tsv"
    C.RECEIPTS.mkdir(parents=True, exist_ok=True)
    remote_lines = ["ref\thead"] + [f"{r['ref']}\t{r['head']}" for r in sorted(remote_refs, key=lambda x: x["ref"])]
    remote_snapshot_path.write_text("\n".join(remote_lines) + "\n", encoding="utf-8")
    remote_sha = C.sha256(remote_raw)
    snap_names = {}
    for r in refs_all:
        name = r["ref"]
        if name.startswith("refs/remotes/origin/"):
            snap_names[name[len("refs/remotes/origin/"):]] = r["head"]
        elif name.startswith("refs/remotes/"):
            snap_names[name[len("refs/remotes/"):]] = r["head"]
    cur_names = {}
    for r in remote_refs:
        if r["ref"].startswith("refs/heads/"):
            cur_names[r["ref"][len("refs/heads/"):]] = r["head"]
    added = sorted(set(cur_names) - set(snap_names))
    removed = sorted(set(snap_names) - set(cur_names))
    moved = sorted(k for k in set(snap_names) & set(cur_names) if snap_names[k] != cur_names[k])
    pull_refs = [r for r in remote_refs if r["ref"].startswith("refs/pull/")]
    head_refs = [r for r in remote_refs if r["ref"] == "HEAD"]
    tag_refs = [r for r in remote_refs if r["ref"].startswith("refs/tags/")]
    checks.append(
        check(
            "current_remote_ref_snapshot",
            True,
            {
                "remote_refs": len(remote_refs),
                "u53f_snapshot_names": len(snap_names),
                "added_since_u53f_snapshot": len(added),
                "removed_since_u53f_snapshot": len(removed),
                "moved_since_u53f_snapshot": len(moved),
                "pull_refs": len(pull_refs),
                "head_refs": len(head_refs),
                "tag_refs": len(tag_refs),
                "raw_sha256": remote_sha,
            },
            {
                "remote_refs": "live",
                "raw_sha256": remote_sha,
            },
            f"git ls-remote origin at {datetime.now(timezone.utc).isoformat()}",
            "This is an independent live ref enumeration, frozen to receipts/remote_refs_snapshot.tsv. "
            "It is not a re-fetch of every branch's blobs.",
        )
    )

    # ---------- manifest / head self-reference anomalies ----------
    manifest = show_json("EVIDENCE_MANIFEST.json")
    remote_verification = show_json("evidence/remote_verification.json")
    head_anomalies = [
        {
            "kind": "HEAD_METADATA_INCONSISTENT",
            "01_observed_head": scope01.get("observed_head"),
            "manifest_observed_head": manifest.get("observed_head"),
            "remote_verification": remote_verification.get("verified_remote_ref"),
            "pinned_final_u53f_head": C.SOURCE_REF,
            "note": "All 36 file hashes match, but 01/manifest/remote_verification name earlier heads "
                    "(f148f9ba/872aaee) while the manifest blob and branch now sit at fdc4d... .",
        }
    ]
    anomalies.extend(head_anomalies)
    checks.append(
        check(
            "manifest_head_self_reference",
            False,
            head_anomalies[0],
            {"consistent_final_head": C.SOURCE_REF},
            "01 observed_head, EVIDENCE_MANIFEST observed_head, remote_verification vs pinned fdc4d...",
            "APPARENT DEFECT: content hashes pass; head receipts do not name the final commit.",
        )
    )

    # ---------- per-ref denominator data for 05 ----------
    # Broader candidate flags for excluded refs.
    excluded_candidates = [
        r for r in excluded
        if BROAD_CANDIDATE.search(r["ref"]) or BROAD_CANDIDATE.search(r["subject"])
    ]
    candidate_path_evidence = {}
    for r in excluded_candidates:
        try:
            base = C.git("merge-base", SEALED, r["head"]).strip()
        except Exception:
            base = ""
        try:
            if base:
                raw = C.git_bytes("diff", "--no-renames", "--name-only", "-z", base, r["head"])
            else:
                raw = C.git_bytes("ls-tree", "-r", "-z", "--name-only", r["head"])
            paths = [p.decode("utf-8", "replace") for p in raw.split(b"\0") if p]
        except Exception as exc:
            paths = []
            r["diff_unreadable"] = str(exc)
        r["excluded_changed_paths"] = len(paths)
        notable = sorted(
            p for p in paths if BROAD_CANDIDATE.search(p)
        )[:12]
        candidate_path_evidence[r["ref"]] = {
            "changed_paths": len(paths),
            "notable_paths": notable,
        }
        r["excluded_notable_paths"] = notable

    # Current remote additions: attach commit metadata where locally available.
    added_heads = [cur_names[name] for name in added]
    added_meta = parse_commits(added_heads) if added_heads else {}
    current_added_records = []
    for name in added:
        head = cur_names[name]
        meta = added_meta.get(head, ("", "", "missing"))
        current_added_records.append(
            {
                "ref": "refs/heads/" + name,
                "head": head,
                "ref_type": "commit",
                "date": meta[0],
                "subject": meta[1] if meta[2] == "commit" else "SUBJECT_UNKNOWN_NOT_FETCHED",
                "source": "CURRENT_REMOTE_ONLY",
                "included": False,
                "reason": "NOT_IN_U53F_SNAPSHOT",
                "head_readable": meta[2] == "commit",
                "changed_paths": None,
                "zero_diff": None,
                "contributes_rows": None,
                "candidate_flag": bool(BROAD_CANDIDATE.search(name)),
                "candidate_reason": "CURRENT_REMOTE_NAME_MATCH" if BROAD_CANDIDATE.search(name) else "",
            }
        )

    ref_records = []
    for r in refs_all:
        cand = bool(BROAD_CANDIDATE.search(r["ref"]) or BROAD_CANDIDATE.search(r["subject"]))
        ref_records.append(
            {
                **r,
                "source": r["source"],
                "candidate_flag": cand and not r["included"],
                "candidate_reason": "EXCLUDED_BROAD_MATERIAL_NAME" if cand and not r["included"] else "",
                "excluded_changed_paths": r.get("excluded_changed_paths"),
                "excluded_notable_paths": r.get("excluded_notable_paths", []),
            }
        )
    ref_records.extend(current_added_records)
    current_extra_records = []
    for r in pull_refs + head_refs + tag_refs:
        current_extra_records.append(
            {
                "ref": r["ref"],
                "head": r["head"],
                "ref_type": "pull_ref"
                if r["ref"].startswith("refs/pull/")
                else ("head_ref" if r["ref"] == "HEAD" else "tag"),
                "date": "",
                "subject": "SUBJECT_UNKNOWN_NOT_FETCHED",
                "source": "CURRENT_REMOTE_ONLY_NON_BRANCH_REF",
                "included": False,
                "reason": "NOT_IN_U53F_SNAPSHOT",
                "head_readable": False,
                "changed_paths": None,
                "zero_diff": None,
                "contributes_rows": None,
                "candidate_flag": False,
                "candidate_reason": "",
                "excluded_changed_paths": None,
                "excluded_notable_paths": [],
            }
        )
    ref_records.extend(current_extra_records)

    payload = {
        "schema": "R53_P53E_SCOPE_CHALLENGE@1",
        "source_ref": C.SOURCE_REF,
        "u53f_sealed_ref": SEALED,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "anomalies": anomalies,
        "counts": {
            "tree_rows": len(ledger),
            "tree_bytes": sum(int(r["size"]) for r in rows02),
            "refs_snapshot": len(refs_all),
            "material_refs": len(included),
            "contributing_refs": len(contributing),
            "zero_diff_refs": len(zero),
            "diff_rows": len(all03),
            "scan_hits": len(rows06),
            "scan_unique_blobs": len(blob_ids),
            "scan_blobs_missing_locally": len(missing_blob),
            "graph_nodes": len(nodes),
            "graph_edges": len(edges),
            "unresolved_edges": len(unresolved),
            "timeline_rows": len(timeline),
            "roster_rows": len(roster08),
            "registry_rows": len(registry),
            "remote_refs_current": len(remote_refs),
            "remote_added": len(added),
            "remote_removed": len(removed),
            "remote_moved": len(moved),
            "remote_pull_refs": len(pull_refs),
            "remote_head_refs": len(head_refs),
            "remote_tag_refs": len(tag_refs),
        },
        "remote_snapshot": {
            "command": "git ls-remote origin",
            "raw_sha256": remote_sha,
            "receipt_path": str(remote_snapshot_path.relative_to(C.P53E_ROOT)),
            "refs": len(remote_refs),
            "added": added,
            "removed": removed,
            "moved": moved,
            "pull_refs": len(pull_refs),
            "head_refs": len(head_refs),
            "tag_refs": len(tag_refs),
            "note": "Added/removed/moved are branch-name comparisons against the U53F 01 snapshot; "
                    "remote-only subjects are UNKNOWN unless the commit object was already local. "
                    "Pull refs and HEAD are enumerated separately and are not branch heads.",
        },
        "ref_denominator": ref_records,
        "excluded_candidate_path_evidence": candidate_path_evidence,
        "limitations": [
            "No branch blobs were fetched for this challenge; locally absent blobs are reported missing.",
            "The 11,305 scanned-Python-blob coverage figure is not re-derived; the 45,431 hit rows are.",
            "U53F's causal/architectural hypotheses are not evaluated here.",
            "No respondent data, production execution, source grant or scientific adoption is used.",
        ],
    }
    C.write_json(C.P53E_ROOT / "receipts/scope_challenge.json", payload)
    print(
        json.dumps(
            {
                "checks": {c["check"]: c["pass"] for c in checks},
                "counts": payload["counts"],
                "anomalies": len(anomalies),
            },
            indent=1,
        )
    )


if __name__ == "__main__":
    main()
