#!/usr/bin/env python3
"""Render the <20 KiB Astra handoff page from verified receipts."""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus_common as C

BRANCH = "agent/rabochii-pyat-r53-p53e-u53f-corpus-browser-access-and-proof-r1"
REPO = "https://github.com/maidiu/rawlsing"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--head", default=None)
    args = parser.parse_args()
    head = args.head or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=str(C.ROOT), text=True
    ).strip()
    corpus = json.loads((C.P53E_ROOT / "02_LOSSLESS_ORDERED_SHARD_MANIFEST.json").read_text(encoding="utf-8"))
    challenge = json.loads((C.P53E_ROOT / "receipts/scope_challenge.json").read_text(encoding="utf-8"))
    targets = json.loads((C.P53E_ROOT / "receipts/readback_targets.json").read_text(encoding="utf-8"))
    adversarial_path = C.RECEIPTS / "adversarial_test.json"
    adversarial = json.loads(adversarial_path.read_text(encoding="utf-8")) if adversarial_path.exists() else {}
    readback_path = C.RECEIPTS / "github_api_readback.json"
    readback = json.loads(readback_path.read_text(encoding="utf-8")) if readback_path.exists() else {}
    lookup_path = C.P53E_ROOT / "04_TOPIC_TO_SHARD_LOOKUP.tsv"
    lookup_counts = Counter()
    if lookup_path.exists():
        with lookup_path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                if row["record_type"] == "TOPIC_CHUNK":
                    lookup_counts[row["topic"]] += 1

    def full_path(path):
        return path if path.startswith("WORKER_RETURNS/") else f"{C.P53E_RETURN}/{path}"

    def url(path):
        return f"{REPO}/blob/{BRANCH}/{full_path(path)}"

    def raw(path):
        return f"https://raw.githubusercontent.com/maidiu/rawlsing/{BRANCH}/{full_path(path)}"

    lines = []
    lines.append("# PYAT R53 P53E — Astra minimum index (read this first)\n")
    lines.append(f"**Repository** `maidiu/rawlsing` (private). **Branch** `{BRANCH}`.  ")
    lines.append(f"**This return head** `{head}`. **Original U53F evidence** `{C.SOURCE_REF}`.  ")
    lines.append(f"**Corpus status** `{corpus['summary']['original_files']}/{corpus['summary']['original_files']}` U53F manifest files byte-verified; ")
    lines.append(f"{corpus['summary']['chunk_count']} lossless chunks; {corpus['summary']['total_original_bytes']:,} bytes.  ")
    lines.append(f"**Browser connector readback** `{readback.get('browser_connector_status', 'UNKNOWN_NOT_TESTED_IN_THIS_HARNESS')}`.  ")
    lines.append(f"**GitHub REST/API readback** `{readback.get('api_readback_status', 'NOT_YET_TESTED')}`.\n")
    lines.append("> This is a navigation page, not a substitute for the corpus. Every row below is preserved in a lossless shard. ")
    lines.append("> U53F classifications are quoted as U53F-authored evidence, not adopted by this return.\n")

    lines.append("## 60-second route\n")
    lines.append("1. Read `02_LOSSLESS_ORDERED_SHARD_MANIFEST.json` for every original → chunk → byte/row/SHA mapping.")
    lines.append("2. Use `04_TOPIC_TO_SHARD_LOOKUP.tsv` to jump by topic or source path. `TOPIC_CHUNK` rows are complete at chunk granularity; `TOPIC_SAMPLE`/`TOPIC_FILE_TOP` are explicitly samples.")
    lines.append("3. Read `05_UNEXAMINED_REF_AND_SCOPE_DENOMINATOR.tsv` before making any NO-MISSING claim.")
    lines.append("4. Read the original small files at the U53F ref; read the eight large originals through the shards.")
    lines.append("5. Re-verify with `tools/verify_corpus.py` (see commands below).\n")

    lines.append("## Verified counts\n")
    s = corpus["summary"]
    c = challenge["counts"]
    lines.append("| Item | Value | Source |")
    lines.append("|---|---:|---|")
    lines.append(f"| U53F manifest files rechecked | {s['original_files']}/{s['original_files']} | `01_ORIGINAL_MANIFEST_INDEPENDENT_RECHECK.json` |")
    lines.append(f"| Large originals sharded | {s['sharded_original_files']} | `02_…SHARD_MANIFEST.json` |")
    lines.append(f"| Lossless chunks | {s['chunk_count']} | `02_…SHARD_MANIFEST.json` |")
    lines.append(f"| Sharded original bytes | {s['sharded_original_bytes']:,} | 331-byte-exact chunks |")
    lines.append(f"| All original bytes | {s['total_original_bytes']:,} | 36 manifest files |")
    lines.append(f"| Pinned-tree rows | {c['tree_rows']:,} | `git ls-tree -r f148f9ba` equality |")
    lines.append(f"| Material diff rows | {c['diff_rows']:,} | `03` parts 50,000 + 29,487 |")
    lines.append(f"| Scan hit rows | {c['scan_hits']:,} | `06` physical rows |")
    lines.append(f"| Selected / contributing refs | {c['material_refs']} / {c['contributing_refs']} | `evidence/ref_inventory.json` recomputation |")
    lines.append(f"| Zero-diff selected refs | {c['zero_diff_refs']} | `03` explanation below |")
    lines.append(f"| Closed35 roster rows | {c['roster_rows']} | 700-row frozen registry → 35 pairs |")
    lines.append(f"| Unresolved dynamic edges | {c['unresolved_edges']} | `05_UNRESOLVED…tsv` |")
    lines.append(f"| Current remote refs seen | {c['remote_refs_current']:,} | live `git ls-remote`, frozen receipt |")
    current_only = (
        c["remote_added"] + c["remote_pull_refs"] + c["remote_head_refs"] + c["remote_tag_refs"]
    )
    lines.append(f"| Unexamined refs denominator | {1649 + current_only:,} | 1,649 U53F-excluded + {current_only} current-only |")
    lines.append("")

    lines.append("## Shard map — first / middle / last exact links\n")
    lines.append("| Shard (original) | Chunks | Bytes | First | Middle | Last |")
    lines.append("|---|---:|---:|---|---|---|")
    by_shard = defaultdict(list)
    for target in targets["targets"]:
        if target["label"].endswith(("_FIRST", "_MIDDLE", "_LAST")):
            shard = target["shard_id"]
            by_shard[shard].append(target)
    for record in corpus["originals"]:
        if record["storage"] != "sharded":
            continue
        shard = record["shard_id"]
        entries = {t["label"].rsplit("_", 1)[-1]: t for t in by_shard[shard]}
        links = []
        for key in ("FIRST", "MIDDLE", "LAST"):
            t = entries.get(key)
            links.append(f"[{key.lower()}]({url(t['shard_path'])})" if t else "")
        lines.append(
            f"| `{shard}`<br>`{record['path']}` | {record['chunk_count']} | {record['actual_bytes']:,} | "
            + " | ".join(links)
            + " |"
        )
    lines.append("")

    lines.append("## Topic → primary shards (ordered lookup)\n")
    topic_shards = defaultdict(Counter)
    if lookup_path.exists():
        with lookup_path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                if row["record_type"] == "TOPIC_CHUNK":
                    topic_shards[row["topic"]][row["shard_id"]] += int(row["match_count"])
    lines.append("| Topic | Matching rows (chunk-count sum) | Top shards |")
    lines.append("|---|---:|---|")
    for topic in sorted(topic_shards):
        top = ", ".join(f"`{k}`" for k, _ in topic_shards[topic].most_common(5))
        lines.append(f"| `{topic}` | {sum(topic_shards[topic].values()):,} | {top} |")
    lines.append("\n`04_TOPIC_TO_SHARD_LOOKUP.tsv` has the exact source path, blob, physical row, shard and byte range. ")
    lines.append("`TOPIC_CHUNK` coverage is complete at chunk granularity; samples are labeled as samples.\n")

    lines.append("## Named exact pointers (G50/J42 and high-risk files)\n")
    lines.append("| Label | Source path | Shard | Row | Link |")
    lines.append("|---|---|---|---:|---|")
    seen = set()
    for target in targets["targets"]:
        if not target["label"].startswith(("NAMED_", "HIGH_SIGNAL_")):
            continue
        key = (target["label"], target["shard_path"])
        if key in seen:
            continue
        seen.add(key)
        lines.append(
            f"| `{target['label']}` | `{target['original_path']}` | `{target['shard_path']}` | "
            f"{target.get('sample_row', '')} | [open]({url(target['shard_path'])}) |"
        )
    lines.append("")

    lines.append("## Null, unknown, inaccessible, dynamically unresolved\n")
    lines.append("- **9** U53F unresolved/incompatible edges are preserved in `05_UNRESOLVED_DYNAMIC_AND_MISSING_EDGES.tsv`; they are not resolved by this return.")
    lines.append("- **35/35** roster rows keep `source_permission_runtime=UNKNOWN_NOT_GRANTED_IN_THIS_FORENSIC_RUN` and `known_original_U_E_pre_scope=NOT_ISSUED / NULL`.")
    lines.append(f"- **1,649** U53F-excluded refs (1,648 non-material + 1 same-as-sealed) and **{current_only}** current remote-only refs ({c['remote_added']} new heads + {c['remote_pull_refs']} pull refs + {c['remote_head_refs']} HEAD) are in the denominator. No NO-MISSING claim is made.")
    lines.append("- **119** of the 966 U53F-selected refs have `changed_paths=0`; only **847** contribute the 79,487 rows. This is a clarification, not a row loss.")
    lines.append("- U53F's 11,305 scanned-Python-blob coverage is author-reported; this return independently counts the 45,431 hit rows and confirms all 1,228 unique hit blobs are locally present.")
    lines.append("- The U53F manifest/01/remote receipt name earlier heads (`f148f9ba`/`872aaee`) while the pinned final head is `fdc4d…`. Content hashes pass; the head metadata is an apparent self-reference defect.")
    lines.append("")

    lines.append("## Verify and reassemble\n")
    lines.append("```bash")
    lines.append("cd <worktree root>")
    lines.append("R=WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1")
    lines.append("python3 $R/tools/verify_corpus.py --json-out /tmp/p53e_verify.json")
    lines.append("# reassemble one original exactly (raw byte concatenation):")
    lines.append("python3 - <<'PY'")
    lines.append("import json, pathlib")
    lines.append("R=pathlib.Path('WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1')")
    lines.append("m=json.loads((R/'02_LOSSLESS_ORDERED_SHARD_MANIFEST.json').read_text())")
    lines.append("o=next(x for x in m['originals'] if x['path']=='06_SOURCE_SPECIFICITY_AND_FIXTURE_LEAKAGE.tsv')")
    lines.append("b=b''.join((R/c['path']).read_bytes() for c in o['chunks'])")
    lines.append("assert b == __import__('subprocess').check_output(['git','show','fdc4d03537e649cd56c19a458ebeb3292298ff3f:'+'WORKER_RETURNS/PYAT-R53-U53F-UNIVERSAL-EXECUTION-CODEBASE-FORENSICS-R1/'+o['path']])")
    lines.append("print(len(b), __import__('hashlib').sha256(b).hexdigest())")
    lines.append("PY")
    lines.append("```")
    lines.append("")
    lines.append("## Limits\n")
    lines.append("- No Browser connector is present in this harness. GitHub API readback is reported separately; actual Browser UI readback remains **UNKNOWN** unless a Browser-side worker tests it.")
    lines.append("- No source/respondent data, production code execution, source grant, scientific adoption, architecture verdict, U53A theory, or HQ acceptance is created.")
    lines.append("- The U53F material-ref selection is bounded by its name/subject rule; the denominator above is the explicit frontier, not proof of absence.")
    lines.append("- Remote-only ref subjects are UNKNOWN where the commit object was not already local; this return did not fetch every branch.")
    lines.append("")
    lines.append("## Exact paths\n")
    for name in (
        "00_RETURN_AND_ASTRA_READ_FIRST.md",
        "01_ORIGINAL_MANIFEST_INDEPENDENT_RECHECK.json",
        "02_LOSSLESS_ORDERED_SHARD_MANIFEST.json",
        "03_REPRODUCIBLE_SHARD_READBACK_AND_REASSEMBLY.md",
        "04_TOPIC_TO_SHARD_LOOKUP.tsv",
        "05_UNEXAMINED_REF_AND_SCOPE_DENOMINATOR.tsv",
        "07_NEGATIVE_REASSEMBLY_RESULTS.json",
        "tools/verify_corpus.py",
    ):
        lines.append(f"- [`{name}`]({url(C.P53E_RETURN + '/' + name)})")
    lines.append("")

    text = "\n".join(lines) + "\n"
    if len(text.encode("utf-8")) > 20 * 1024:
        raise SystemExit(f"minimum index is {len(text.encode('utf-8'))} bytes, over 20 KiB")
    (C.P53E_ROOT / "06_ASTRA_MINIMUM_INDEX.md").write_text(text, encoding="utf-8")
    print(
        json.dumps(
            {
                "bytes": len(text.encode("utf-8")),
                "head": head,
                "browser_status": readback.get("browser_connector_status", "UNKNOWN_NOT_TESTED_IN_THIS_HARNESS"),
                "api_status": readback.get("api_readback_status", "NOT_YET_TESTED"),
            },
            indent=1,
        )
    )


if __name__ == "__main__":
    main()
