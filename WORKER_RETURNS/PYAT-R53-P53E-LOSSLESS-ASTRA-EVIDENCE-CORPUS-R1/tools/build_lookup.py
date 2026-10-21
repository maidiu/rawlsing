#!/usr/bin/env python3
"""Build Astra's topic/file navigation layer and the unexamined-ref denominator.

The lookup is navigation convenience. It never replaces or truncates the
lossless shards; every count is a pointer into the preserved original bytes.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus_common as C

U = C.U53F_RETURN
TOPICS = [
    (
        "T1_SOURCE_NATIVE_AUTHORITY_ROLE_WORKLOAD",
        re.compile(
            r"(source|authority|registr|roster|role|workload|u_epre|universe|"
            r"admission|permission|eligib|question_relation|closed35|all35)",
            re.I,
        ),
        "source-native inventory / authority / role / workload",
    ),
    (
        "T2_B49_G50_I51_U43",
        re.compile(r"(b49|g50|i51|u43)", re.I),
        "B49, G50, I51 and U43 lanes",
    ),
    (
        "T3_C11_ROUTEB_I03_I05_BATCH",
        re.compile(
            r"(c11|route.?b|i03|i05|batch|carrier|empirical_query|empirical_possib)",
            re.I,
        ),
        "canonical C11 / Route B / I03 / I05 / Batch",
    ),
    (
        "T4_E41_J42_P41_LEARNED_M1_M2_B5_FF_F5_F8_N9_N10_E04",
        re.compile(
            r"(e41|j42|p41|learned|m1|m2|b5|field.?forge|ff[-_]|f5|f6|f7|f8|"
            r"n9|n10|e04|e05|temporal|world|consumer|joint)",
            re.I,
        ),
        "E41/J42/P41, learned M1/M2/B5, FF/F5-F8, N9/N10E/N10W, E04",
    ),
    (
        "T5_HQ_COMMISSION_ACCEPTANCE_DRIFT_HISTORY",
        re.compile(
            r"(WORKER_COMMISSIONS|PYAT_CONTROL_ROOM|HQ_HANDOFF|CROSS_HQ|"
            r"commission|acceptance|drift|STOP|dispatch|seal)",
            re.I,
        ),
        "HQ commission / acceptance / drift history",
    ),
]
HIGH_RISK_PATHS = [
    "rawlsing_next/pre553_candidate_c_production_binding.py",
    "rawlsing_next/ee_p2x_darwin_stage_backend.py",
    "rawlsing_next/pre553_independent_parity_oracle.py",
    "rawlsing_next/fiabc_final_oracle_freeze_producers.py",
    "g50/native_i05.py",
    "r51_joined_source_producer.py",
    "candidate/r51_joined_source_producer.py",
]


def show_json(path: str):
    return json.loads(C.read_blob(C.tree_map()[U + "/" + path]["blob"]).decode("utf-8"))


def show_bytes(path: str):
    return C.read_blob(C.tree_map()[U + "/" + path]["blob"])


def show_tsv(path: str):
    text = show_bytes(path).decode("utf-8", "replace")
    lines = text.splitlines()
    header = lines[0].split("\t")
    return header, [dict(zip(header, line.split("\t"))) for line in lines[1:]]


def clean(text: str, limit=300):
    text = text.replace("\t", " | ").replace("\r", " ").replace("\n", " ")
    return text[:limit]


def main():
    corpus = json.loads((C.P53E_ROOT / "02_LOSSLESS_ORDERED_SHARD_MANIFEST.json").read_text(encoding="utf-8"))
    challenge = json.loads((C.P53E_ROOT / "receipts/scope_challenge.json").read_text(encoding="utf-8"))
    by_path = {o["path"]: o for o in corpus["originals"]}

    def locate(path, row):
        record = by_path.get(path)
        if not record:
            return None
        if record["storage"] == "direct":
            return {
                "shard_id": "DIRECT",
                "shard_path": record["full_path"],
                "part": "DIRECT",
                "row": row,
            }
        for chunk in record["chunks"]:
            if chunk["row_start"] <= row <= chunk["row_end"]:
                return {
                    "shard_id": record["shard_id"],
                    "shard_path": chunk["path"],
                    "part": chunk["part"],
                    "row": row - chunk["row_start"] + 1,
                }
        return None

    lookup_rows = []
    # Complete file map: every one of the 36 originals.
    for record in corpus["originals"]:
        if record["storage"] == "sharded":
            lookup_rows.append(
                (
                    "FILE_MAP",
                    "ALL",
                    record["path"],
                    record["git_blob"],
                    record["line_count"],
                    record["shard_id"],
                    record["shard_dir"],
                    f"0000-{record['chunk_count'] - 1:04d}",
                    1,
                    record["line_count"],
                    0,
                    record["actual_bytes"],
                    record["line_count"],
                    1,
                    record["line_count"],
                    "",
                    clean(record["first_line"]),
                    f"SHARDED; chunks={record['chunk_count']}; sha256={record['actual_sha256']}; "
                    f"byte-exact reconstruction={record['reconstruction_equal']}",
                )
            )
        else:
            lookup_rows.append(
                (
                    "FILE_MAP",
                    "ALL",
                    record["path"],
                    record["git_blob"],
                    record["line_count"],
                    "DIRECT",
                    record["full_path"],
                    "DIRECT",
                    1,
                    record["line_count"],
                    0,
                    record["actual_bytes"],
                    record["line_count"],
                    1,
                    record["line_count"],
                    "",
                    clean(record["first_line"]),
                    "DIRECT at the pinned U53F ref; byte/size/SHA256 verified; no shard needed.",
                )
            )

    # Per-topic chunk-level coverage and samples.
    topic_file_counts = defaultdict(Counter)
    topic_first = {}
    topic_first_by_path = defaultdict(dict)
    topic_samples = defaultdict(list)
    high_signal_rows = []
    for topic, regex, description in TOPICS:
        for path, record in by_path.items():
            if record["storage"] != "sharded":
                continue
            if record["shard_id"] in ("S01_01_REPOSITORY_SCOPE", "S07_EVIDENCE_REF_INVENTORY", "S08_NESTED_01_REPOSITORY_SCOPE"):
                continue
            for chunk in record["chunks"]:
                data = (C.P53E_ROOT / chunk["path"]).read_bytes()
                lines = data.split(b"\n")
                if lines and lines[-1] == b"":
                    lines = lines[:-1]
                for offset, raw_line in enumerate(lines):
                    line = raw_line.decode("utf-8", "replace")
                    if "\t" not in line and not line.strip():
                        continue
                    fields = line.split("\t")
                    if record["shard_id"].startswith("S02"):
                        match_text = fields[6] if len(fields) > 6 else line
                    elif record["shard_id"].startswith("S03") or record["shard_id"].startswith("S04"):
                        match_text = "\t".join(
                            [
                                fields[0] if len(fields) > 0 else "",
                                fields[3] if len(fields) > 3 else "",
                                fields[8] if len(fields) > 8 else "",
                                fields[11] if len(fields) > 11 else "",
                            ]
                        )
                    elif record["shard_id"].startswith("S05"):
                        match_text = "\t".join(fields[:9]) + "\t" + (fields[9] if len(fields) > 9 else "")
                    elif record["shard_id"].startswith("S06"):
                        match_text = "\t".join(fields[:2])
                    else:
                        match_text = line
                    if record["shard_id"].startswith("S02"):
                        source_path = fields[6] if len(fields) > 6 else line
                        source_blob = fields[2] if len(fields) > 2 else ""
                    elif record["shard_id"].startswith("S03") or record["shard_id"].startswith("S04"):
                        source_path = fields[8] if len(fields) > 8 else line
                        source_blob = fields[9] if len(fields) > 9 else ""
                    else:
                        source_path = fields[0] if fields else line
                        source_blob = fields[1] if len(fields) > 1 else ""
                    if regex.search(match_text):
                        absolute_row = chunk["row_start"] + offset
                        topic_file_counts[topic][source_path] += 1
                        topic_first.setdefault(topic, (source_path, absolute_row, chunk, line))
                        topic_first_by_path[topic].setdefault(
                            source_path, (source_blob, path, absolute_row, chunk, line)
                        )
                        if len(topic_samples[topic]) < 20:
                            topic_samples[topic].append(
                                (source_path, source_blob, path, absolute_row, chunk, line)
                            )
                    if record["shard_id"].startswith("S05") and len(fields) > 8:
                        severity = fields[7] if len(fields) > 7 else ""
                        confidence = fields[8] if len(fields) > 8 else ""
                        if (severity == "HIGH" or confidence == "HIGH") and len(high_signal_rows) < 20000:
                            high_signal_rows.append(
                                (source_path, source_blob, path, absolute_row, chunk, line, fields)
                            )
        # chunk-level counts
        for path, record in by_path.items():
            if record["storage"] != "sharded":
                continue
            if record["shard_id"] in ("S01_01_REPOSITORY_SCOPE", "S07_EVIDENCE_REF_INVENTORY", "S08_NESTED_01_REPOSITORY_SCOPE"):
                continue
            for chunk in record["chunks"]:
                data = (C.P53E_ROOT / chunk["path"]).read_bytes()
                lines = data.split(b"\n")
                if lines and lines[-1] == b"":
                    lines = lines[:-1]
                count = 0
                first_row = None
                last_row = None
                sample = ""
                for offset, raw_line in enumerate(lines):
                    line = raw_line.decode("utf-8", "replace")
                    fields = line.split("\t")
                    if record["shard_id"].startswith("S02"):
                        match_text = fields[6] if len(fields) > 6 else line
                    elif record["shard_id"].startswith("S03") or record["shard_id"].startswith("S04"):
                        match_text = "\t".join(
                            [
                                fields[0] if len(fields) > 0 else "",
                                fields[3] if len(fields) > 3 else "",
                                fields[8] if len(fields) > 8 else "",
                                fields[11] if len(fields) > 11 else "",
                            ]
                        )
                    elif record["shard_id"].startswith("S05"):
                        match_text = "\t".join(fields[:9]) + "\t" + (fields[9] if len(fields) > 9 else "")
                    elif record["shard_id"].startswith("S06"):
                        match_text = "\t".join(fields[:2])
                    else:
                        match_text = line
                    if regex.search(match_text):
                        count += 1
                        absolute_row = chunk["row_start"] + offset
                        if first_row is None:
                            first_row = absolute_row
                            sample = line
                        last_row = absolute_row
                if count:
                    lookup_rows.append(
                        (
                            "TOPIC_CHUNK",
                            topic,
                            path,
                            record["git_blob"],
                            record["line_count"],
                            record["shard_id"],
                            chunk["path"],
                            chunk["part"],
                            chunk["row_start"],
                            chunk["row_end"],
                            chunk["byte_start"],
                            chunk["byte_end"],
                            count,
                            first_row,
                            last_row,
                            first_row,
                            clean(sample),
                            f"SAMPLE_ONLY at chunk granularity; {description}; "
                            f"full chunk preserved; {count} matching physical lines in this chunk.",
                        )
                    )
        # per-file top 50
        for source_path, count in topic_file_counts[topic].most_common(50):
            first = topic_first_by_path[topic].get(source_path)
            if first:
                source_blob, container_path, row, chunk, line = first
                record = by_path[container_path]
                loc = locate(container_path, row)
                lookup_rows.append(
                    (
                        "TOPIC_FILE_TOP",
                        topic,
                        source_path,
                        source_blob,
                        0,
                        loc["shard_id"],
                        loc["shard_path"],
                        loc["part"],
                        row,
                        row,
                        chunk["byte_start"],
                        chunk["byte_end"],
                        count,
                        row,
                        row,
                        row,
                        clean(line),
                        f"TOP_50_BY_MATCH_COUNT; source-path matches={count}; "
                        f"container={container_path}; container_lines={record['line_count']}; "
                        f"retrieval sample, not the complete match universe.",
                    )
                )
        # 20 samples with exact rows
        for source_path, source_blob, container_path, row, chunk, line in topic_samples[topic]:
            loc = locate(container_path, row)
            lookup_rows.append(
                (
                    "TOPIC_SAMPLE",
                    topic,
                    source_path,
                    source_blob,
                    0,
                    loc["shard_id"],
                    loc["shard_path"],
                    loc["part"],
                    row,
                    row,
                    chunk["byte_start"],
                    chunk["byte_end"],
                    1,
                    row,
                    row,
                    row,
                    clean(line),
                    f"HIGH_SIGNAL_SAMPLE; {description}; exact physical row in "
                    f"container={container_path}.",
                )
            )

    # High-signal leakage convenience sample (U53F classifications; not adopted).
    for source_path, source_blob, container_path, row, chunk, line, fields in high_signal_rows[:120]:
        loc = locate(container_path, row)
        lookup_rows.append(
            (
                "TOPIC_SAMPLE",
                "T6_HIGH_SIGNAL_CANDIDATE_LEAKAGE",
                source_path,
                source_blob,
                0,
                loc["shard_id"],
                loc["shard_path"],
                loc["part"],
                row,
                row,
                chunk["byte_start"],
                chunk["byte_end"],
                1,
                row,
                row,
                row,
                clean(line),
                f"U53F-authored candidate classification; severity={fields[7]}; "
                f"confidence={fields[8]}; container={container_path}; not adopted by this return.",
            )
        )
    named_high_signal_count = 0
    for source_path, source_blob, container_path, row, chunk, line, fields in high_signal_rows:
        if named_high_signal_count >= 200:
            break
        if any(hr in source_path for hr in HIGH_RISK_PATHS):
            named_high_signal_count += 1
            loc = locate(container_path, row)
            lookup_rows.append(
                (
                    "TOPIC_SAMPLE",
                    "T7_NAMED_HIGH_RISK_FILES",
                    source_path,
                    source_blob,
                    0,
                    loc["shard_id"],
                    loc["shard_path"],
                    loc["part"],
                    row,
                    row,
                    chunk["byte_start"],
                    chunk["byte_end"],
                    1,
                    row,
                    row,
                    row,
                    clean(line),
                    f"Named high-risk file from U53F 09; container={container_path}; "
                    "exact row pointer; not an adjudication.",
                )
            )

    # Null/unknown/dynamic-unresolved pointers.
    _, unresolved = show_tsv("05_UNRESOLVED_DYNAMIC_AND_MISSING_EDGES.tsv")
    for index, row in enumerate(unresolved, start=2):
        lookup_rows.append(
            (
                "NULL_UNRESOLVED",
                "T8_NULL_UNKNOWN_INACCESSIBLE_DYNAMIC_UNRESOLVED",
                "05_UNRESOLVED_DYNAMIC_AND_MISSING_EDGES.tsv",
                C.tree_map()[U + "/05_UNRESOLVED_DYNAMIC_AND_MISSING_EDGES.tsv"]["blob"],
                10,
                "DIRECT",
                U + "/05_UNRESOLVED_DYNAMIC_AND_MISSING_EDGES.tsv",
                "DIRECT",
                index,
                index,
                0,
                0,
                1,
                index,
                index,
                index,
                clean("\t".join(row.values())),
                f"U53F unresolved edge status={row.get('status')}; reason={row.get('reason')}",
            )
        )
    for index, line in enumerate(
        show_bytes("01_REPOSITORY_SCOPE_AND_COMPLETENESS.json").decode("utf-8").splitlines(), start=1
    ):
        if '"completeness_limitations"' in line or line.strip().startswith('"Only paths') or line.strip().startswith('"Refs not') or line.strip().startswith('"No raw') or line.strip().startswith('"Remote ref') or line.strip().startswith('"Repository-wide'):
            lookup_rows.append(
                (
                    "NULL_UNRESOLVED",
                    "T8_NULL_UNKNOWN_INACCESSIBLE_DYNAMIC_UNRESOLVED",
                    "01_REPOSITORY_SCOPE_AND_COMPLETENESS.json",
                    by_path["01_REPOSITORY_SCOPE_AND_COMPLETENESS.json"]["git_blob"],
                    by_path["01_REPOSITORY_SCOPE_AND_COMPLETENESS.json"]["line_count"],
                    "S01_01_REPOSITORY_SCOPE",
                    next(c["path"] for c in by_path["01_REPOSITORY_SCOPE_AND_COMPLETENESS.json"]["chunks"] if c["row_start"] <= index <= c["row_end"]),
                    next(c["part"] for c in by_path["01_REPOSITORY_SCOPE_AND_COMPLETENESS.json"]["chunks"] if c["row_start"] <= index <= c["row_end"]),
                    index,
                    index,
                    0,
                    0,
                    1,
                    index,
                    index,
                    index,
                    clean(line),
                    "U53F bounded limitation; preserve as UNKNOWN, not as absence.",
                )
            )

    header = (
        "record_type",
        "topic",
        "original_path",
        "original_blob",
        "original_lines",
        "shard_id",
        "shard_path",
        "shard_part",
        "shard_row_start",
        "shard_row_end",
        "byte_start",
        "byte_end",
        "match_count",
        "first_match_row",
        "last_match_row",
        "sample_row",
        "sample_text",
        "note",
    )
    C.write_tsv(C.P53E_ROOT / "04_TOPIC_TO_SHARD_LOOKUP.tsv", header, lookup_rows)

    # ---------- 05 denominator ----------
    rows05 = []
    counts = challenge["counts"]
    current_only = (
        counts["remote_added"]
        + counts["remote_pull_refs"]
        + counts["remote_head_refs"]
        + counts["remote_tag_refs"]
    )
    summary = [
        ("TREE_TRACKED_FILES", counts["tree_rows"], "git ls-tree -r f148f9ba; exact equality verified"),
        ("TREE_BYTES", counts["tree_bytes"], "sum of 02 sizes; git object sizes verified"),
        ("U53F_REFS_TOTAL", counts["refs_snapshot"], "2,613 observed refs + 2 mandated pseudo-refs"),
        ("U53F_MATERIAL_REFS", counts["material_refs"], "recomputed with U53F rule; exact set equality"),
        ("U53F_CONTRIBUTING_REFS", counts["contributing_refs"], "selected refs with changed_paths>0"),
        ("U53F_ZERO_DIFF_REFS", counts["zero_diff_refs"], "selected refs with changed_paths=0"),
        ("DIFF_ROWS", counts["diff_rows"], "03 part00=50,000 + part01=29,487"),
        ("SCAN_HITS", counts["scan_hits"], "06 physical data rows"),
        ("SCAN_UNIQUE_BLOBS", counts["scan_unique_blobs"], "unique blob ids in 06; all present locally"),
        ("SCAN_PYTHON_COVERAGE", 11305, "U53F-authored; not re-derived by this access mission"),
        ("GRAPH_NODES", counts["graph_nodes"], "04 record_type=node"),
        ("GRAPH_EDGES", counts["graph_edges"], "04 record_type=edge"),
        ("UNRESOLVED_EDGES", counts["unresolved_edges"], "05 data rows"),
        ("TIMELINE_ROWS", counts["timeline_rows"], "07 data rows"),
        ("ROSTER_ROWS", counts["roster_rows"], "08 data rows; 700 registry rows -> 35 pairs"),
        ("U53F_UNEXAMINED_REFS", 1649, "1,648 non-material + 1 same-as-sealed"),
        ("CURRENT_REMOTE_ONLY_REFS", current_only, "new heads + pull refs + HEAD at the frozen live snapshot"),
        ("TOTAL_UNEXAMINED_REFS", 1649 + current_only, "U53F exclusions plus current remote-only refs"),
        ("CANDIDATE_FLAGGED_REFS", sum(1 for r in challenge["ref_denominator"] if r.get("candidate_flag")), "broad material-name history flag; not a relevance verdict"),
        ("SHARDED_ORIGINALS", counts["tree_rows"] and 8, "eight originals >192 KiB"),
        ("SHARD_CHUNKS", corpus["summary"]["chunk_count"], "byte-exact chunks"),
        ("SHARDED_BYTES", corpus["summary"]["sharded_original_bytes"], "lossless chunk bytes"),
        ("DIRECT_ORIGINALS", corpus["summary"]["direct_original_files"], "small originals remain at exact U53F ref"),
        ("BROWSER_CONNECTOR_READBACK", "UNKNOWN", "no Browser connector in this harness; see 00_RETURN"),
    ]
    header05 = (
        "record_type",
        "key_or_ref",
        "head",
        "ref_type",
        "snapshot_source",
        "in_u53f_snapshot",
        "u53f_material",
        "u53f_reason",
        "contributes_diff_rows",
        "zero_diff",
        "date",
        "subject",
        "candidate_flag",
        "candidate_reason",
        "excluded_changed_paths",
        "excluded_notable_paths",
        "value_or_note",
    )
    # Rebuild summary rows to the 17-column 05 schema.
    rows05 = []
    for key, value, note in summary:
        rows05.append(
            ("SCOPE_DENOMINATOR", key)
            + ("",) * 14
            + (f"{key}={value} | {note}",)
        )
    for r in challenge["ref_denominator"]:
        if r["source"].startswith("U53F"):
            record_type = (
                "EXCLUDED_MATERIAL_CANDIDATE" if r.get("candidate_flag") else "U53F_REF"
            )
            note = ""
            if r.get("reason") == "SAME_AS_SEALED":
                note = "U53F branch at the sealed SHA; excluded as SAME_AS_SEALED."
            elif r.get("reason") == "MANDATED_PSEUDO_REF":
                note = "Mandated return commit added as a pseudo-ref because no snapshot ref named it."
            elif r.get("zero_diff"):
                note = "Selected by U53F but changed_paths=0; contributes no 03 row."
            elif r.get("candidate_flag"):
                note = (
                    "Excluded by U53F's rule but matches a broader universal/source/history name or subject. "
                    "Listed as a denominator candidate, not as proof of relevance."
                )
            rows05.append(
                (
                    record_type,
                    r["ref"],
                    r["head"],
                    r["ref_type"],
                    r["source"],
                    "Y",
                    "Y" if r.get("included") else "N",
                    r.get("reason", ""),
                    "Y" if r.get("contributes_rows") else "N",
                    "Y" if r.get("zero_diff") else "N",
                    r.get("date", ""),
                    r.get("subject", ""),
                    "Y" if r.get("candidate_flag") else "N",
                    r.get("candidate_reason", ""),
                    r.get("excluded_changed_paths"),
                    "; ".join(r.get("excluded_notable_paths", [])),
                    note,
                )
            )
        else:
            record_type = (
                "CURRENT_REMOTE_MATERIAL_CANDIDATE"
                if r.get("candidate_flag")
                else "CURRENT_REMOTE_ONLY"
            )
            note = "Remote ref appeared after the U53F snapshot and was not examined by U53F."
            if r["ref"].startswith("refs/pull/"):
                note = "Pull-request ref; not a branch head; not examined by U53F."
            elif r["ref"] == "HEAD":
                note = "Remote default-branch HEAD pointer; not a branch head."
            elif r.get("candidate_flag"):
                note += " Matches a broad material-name pattern; subject may be UNKNOWN if not local."
            rows05.append(
                (
                    record_type,
                    r["ref"],
                    r["head"],
                    r["ref_type"],
                    r["source"],
                    "N",
                    "N",
                    "NOT_IN_U53F_SNAPSHOT",
                    "N",
                    "N",
                    r.get("date", ""),
                    r.get("subject", ""),
                    "Y" if r.get("candidate_flag") else "N",
                    r.get("candidate_reason", ""),
                    r.get("excluded_changed_paths"),
                    "; ".join(r.get("excluded_notable_paths", [])),
                    note,
                )
            )
    C.write_tsv(C.P53E_ROOT / "05_UNEXAMINED_REF_AND_SCOPE_DENOMINATOR.tsv", header05, rows05)

    # ---------- readback targets ----------
    targets = []
    for record in corpus["originals"]:
        if record["storage"] != "sharded":
            continue
        chunks = record["chunks"]
        for label, chunk in (
            ("FIRST", chunks[0]),
            ("MIDDLE", chunks[len(chunks) // 2]),
            ("LAST", chunks[-1]),
        ):
            targets.append(
                {
                    "label": f"{record['shard_id']}_{label}",
                    "original_path": record["path"],
                    "shard_id": record["shard_id"],
                    "shard_path": chunk["path"],
                    "part": chunk["part"],
                    "bytes": chunk["bytes"],
                    "sha256": chunk["sha256"],
                }
            )
    named_patterns = {
        "B49": re.compile(r"b49", re.I),
        "G50": re.compile(r"g50", re.I),
        "I51": re.compile(r"i51", re.I),
        "J42": re.compile(r"j42", re.I),
        "E41": re.compile(r"e41", re.I),
        "P41": re.compile(r"p41", re.I),
        "U43": re.compile(r"u43", re.I),
    }
    for label, regex in named_patterns.items():
        found = None
        # Prefer a high-signal 06 row whose source path names the lane.
        for source_path, source_blob, container_path, row, chunk, line, fields in high_signal_rows:
            if not regex.search(source_path):
                continue
            record = by_path[container_path]
            found = {
                "label": f"NAMED_{label}",
                "original_path": source_path,
                "shard_id": record["shard_id"],
                "shard_path": chunk["path"],
                "part": chunk["part"],
                "bytes": chunk["bytes"],
                "sha256": chunk["sha256"],
                "sample_row": row,
                "sample_text": clean(line, 240),
            }
            break
        # Fallback: the first occurrence anywhere in a sharded evidence file.
        if not found:
            for path, record in by_path.items():
                if record["storage"] != "sharded":
                    continue
                if record["shard_id"] in ("S01_01_REPOSITORY_SCOPE", "S07_EVIDENCE_REF_INVENTORY", "S08_NESTED_01_REPOSITORY_SCOPE"):
                    continue
                for chunk in record["chunks"]:
                    data = (C.P53E_ROOT / chunk["path"]).read_bytes()
                    for offset, raw_line in enumerate(data.split(b"\n")):
                        line = raw_line.decode("utf-8", "replace")
                        if regex.search(line):
                            found = {
                                "label": f"NAMED_{label}",
                                "original_path": path,
                                "shard_id": record["shard_id"],
                                "shard_path": chunk["path"],
                                "part": chunk["part"],
                                "bytes": chunk["bytes"],
                                "sha256": chunk["sha256"],
                                "sample_row": chunk["row_start"] + offset,
                                "sample_text": clean(line, 240),
                            }
                            break
                    if found:
                        break
                if found:
                    break
        if found:
            targets.append(found)
    # high-signal named files: use the already-built T7 pointers into 06 rows.
    for needle in HIGH_RISK_PATHS:
        found = None
        for row in lookup_rows:
            if row[0] != "TOPIC_SAMPLE" or row[1] != "T7_NAMED_HIGH_RISK_FILES":
                continue
            if needle not in row[2]:
                continue
            chunk_meta = next(
                c
                for o in corpus["originals"]
                for c in o.get("chunks", [])
                if c["path"] == row[6]
            )
            found = {
                "label": "HIGH_SIGNAL_" + Path(needle).name,
                "original_path": row[2],
                "shard_id": row[5],
                "shard_path": row[6],
                "part": row[7],
                "bytes": chunk_meta["bytes"],
                "sha256": chunk_meta["sha256"],
                "sample_row": row[15],
                "sample_text": row[16],
            }
            break
        if found:
            targets.append(found)
    C.write_json(
        C.RECEIPTS / "readback_targets.json",
        {
            "schema": "R53_P53E_READBACK_TARGETS@1",
            "branch": "agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1",
            "targets": targets,
            "count": len(targets),
        },
    )
    print(
        json.dumps(
            {
                "lookup_rows": len(lookup_rows),
                "denominator_rows": len(rows05),
                "readback_targets": len(targets),
            },
            indent=1,
        )
    )


if __name__ == "__main__":
    main()
