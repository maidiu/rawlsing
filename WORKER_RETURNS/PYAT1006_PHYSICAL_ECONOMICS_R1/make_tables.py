from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
summary = json.loads((ROOT / "evidence" / "baseline_summary.json").read_text())

lines = []
lines.append("# PYAT #1006 measured physical/query baseline\n")
lines.append("ALL ROWS ARE SOURCEFREE SYNTHETIC TEST_ONLY. NOT ORIGINAL35, NOT #1001, NOT PRODUCTION CURRENT. TRUE SOURCE SNAPSHOT/DECODE IS NOT_RUN_PENDING_997.\n")
lines.append("## Host and software\n")
lines.append("- host: `oldMac.lan`, Darwin x86_64, macOS 13.7.8 (22H730), 16 GiB RAM, 16 vCPU, disk 408 GiB with ~16-17 GiB free at dispatch.\n")
lines.append("- Python 3.11.3; pyarrow 26.0.1; pandas 3.1.1; pyreadstat 1.3.7; pytest 9.2.0; psutil 7.2.2; task-local `.venv` inside the return directory.\n")
lines.append("- process-tree ceiling: 6,442,450,944 B (6 GiB), sampled every 20 ms; disk reserve 3 GiB. No shape hit the RSS ceiling.\n")
lines.append("- exact tested heads: assigned branch `codex/pyat1006-physical-baseline-20261113-r1` at `9d96a9cac7d10f59f2c30d8045dd1696fa3ab969`; accepted S2-C `b7b697b69f0acea12174937ee824c19ac34ac284`; accepted S2-D G5 `ba8d760cd8e31a9baff9b45698bd4117f4baa456`.\n")
lines.append("## Shape table\n")
columns = [
    "shape", "status", "resp", "events", "ev/resp", "write s", "I02 proof s",
    "reread/reencode s", "row proj s", "root hash s", "Parquet B",
    "rowgroups", "stage peak B", "proof SQLite B", "cold admit s",
    "session build s", "temp SQLite B", "selected s", "same p50/p95 (n)",
    "fresh p50/p95 (n)", "F2 rev s", "F4 3 s", "I05 s", "batch s",
    "whole-worker tree RSS B", "query phase tree RSS B",
]
lines.append("| " + " | ".join(columns) + " |")
lines.append("|" + "---|" * len(columns))
for item in summary["shapes"]:
    q = item["queries"]
    same = item["same_process"]
    fresh = item.get("fresh", {})
    fresh_stats = fresh.get("query_stats") or {}
    cold = item["cold"]
    monitored = item.get("query_probe_monitored") or {}
    query_tree = (monitored.get("process_tree") or {}).get("tree_peak_rss_bytes")
    lines.append("| " + " | ".join([
        item["shape"],
        item["status"],
        str(item["respondents"]),
        str(item["events"]),
        f"{item['events_per_respondent']:.4f}",
        f"{item['write']['total_seconds']:.3f}",
        f"{item['write']['direct_i02_proof_seconds']:.3f}",
        f"{item['write']['physical_reread_reencode_seconds']:.3f}",
        f"{item['write']['row_projection_seconds']:.3f}",
        f"{item['write']['root_hash_seconds']:.3f}",
        str(item["physical"]["parquet_bytes"]),
        str(item["physical"]["parquet_row_groups"]),
        str(item["physical"]["stage_peak_bytes"]),
        str(item["physical"]["proof_sqlite_peak_bytes"]),
        f"{cold['admission_seconds']:.3f}" if cold.get("admission_seconds") is not None else "NOT_RUN",
        f"{cold['session_build_seconds']:.3f}" if cold.get("session_build_seconds") is not None else (f"{cold['session_build_seconds_total']:.3f} total/{cold['session_build_calls']}" if cold.get("session_build_seconds_total") else "NOT_RUN"),
        str(cold.get("temporary_bytes_during_session", "NOT_RUN")),
        f"{q.get('selected',{}).get('seconds'):.3f}" if q.get("selected",{}).get("seconds") is not None else "NOT_RUN",
        f"{same['p50']:.3f}/{same['p95']:.3f} ({same['n']})" if same else "NOT_RUN",
        f"{fresh_stats.get('p50'):.3f}/{fresh_stats.get('p95'):.3f} ({fresh_stats.get('n')})" if fresh_stats else "NOT_RUN",
        f"{q.get('f2_reverse',{}).get('seconds'):.3f}" if q.get("f2_reverse",{}).get("seconds") is not None else "NOT_RUN",
        f"{q.get('f4_three',{}).get('seconds'):.3f}" if q.get("f4_three",{}).get("seconds") is not None else "NOT_RUN",
        f"{item['i05']['seconds']:.3f}" if item["i05"].get("seconds") is not None else "NOT_RUN",
        f"{item['batch']['seconds']:.3f}" if item["batch"].get("seconds") is not None else "NOT_RUN",
        str(item["process_tree"].get("tree_peak_rss_bytes")),
        str(query_tree) if query_tree else "NOT_RUN",
    ]) + " |")
lines.append("")
lines.append("## Native-reader subtable (1k/10k/skew only)\n")
lines.append("| shape | normal s | completed s | partial s | absent s | batch units | batch states |")
lines.append("|---|---|---|---|---|---|---|")
for item in summary["shapes"]:
    native = item.get("native_readers") or {}
    batch = item.get("batch") or {}
    if not native:
        continue
    lines.append("| " + " | ".join([
        item["shape"],
        f"{native.get('normal_seconds'):.3f}" if native.get("normal_seconds") is not None else "NOT_RUN",
        f"{native.get('resume_completed_seconds'):.3f}" if native.get("resume_completed_seconds") is not None else "NOT_RUN",
        f"{native.get('resume_partial_seconds'):.3f}" if native.get("resume_partial_seconds") is not None else "NOT_RUN",
        f"{native.get('resume_absent_seconds'):.3f}" if native.get("resume_absent_seconds") is not None else "NOT_RUN",
        ",".join(batch.get("units", ())) or "NOT_RUN",
        ",".join(batch.get("states", ())) or "NOT_RUN",
    ]) + " |")
lines.append("")
lines.append("## 100k physical family ledger\n")
lines.append("| member | bytes | rows | row groups |")
lines.append("|---|---|---|---|")
hundred = next(item for item in summary["shapes"] if item["shape"] == "hist-100k")
for member, row in sorted(hundred["physical"]["members"].items()):
    lines.append(f"| {member} | {row['bytes']} | {row['rows']} | {row['row_groups']} |")
lines.append("")
lines.append("## Counts and negative facts\n")
lines.append("- 100k shape: 100,000 distinct respondents, 324,477 RespondentEvent rows (3.24477 events/respondent), 1,448,965 total Parquet rows, 2,841 row groups.\n")
lines.append("- Independent G5 `0169fac9f3840800796c664eee462bbb8984bb42` returned `REVISE_EXACT_DEFECT`; it reproduced the 100k writer/selected cost and corrected this report's old causal claim and test count. The 1k/10k RSS rows below are whole-worker peaks; writer-only 1k is 194,072,576 B and writer-only 10k is 214,261,760 B (independent review). 50k/100k were writer-only because they stopped after write.\n")
lines.append("- `_row`/body_json reconstruction is called twice per object: once at write and once in the post-write reread/re-encode proof. At 100k, row calls: RespondentEvent 649,587; RoutingEligibilityFact 1,000,000; RespondentIdentity 200,000; EmpiricalCoordinateFact 200,000; WeightMeasureFact 200,000. Total `_row` time 492.834 s.\n")
lines.append("- 100k retained Parquet 310,163,264 B; staging peak 5,257,841,984 B; temporary I02 proof SQLite peak 4,385,796,096 B; session temporary SQLite 1,300,910,080 B. These are distinct files/phase costs, not one copy.\n")
lines.append("- 100k writer process-tree peak 295,211,008 B; 100k query process-tree peak 3,690,455,040 B; both below 6 GiB. 50k query peak 1,833,365,504 B.\n")
lines.append("- 100k cold admission 1.520 s; cold all-event posting-index build 33.508 s / 324,477 events / 700,000 member rows; selected query 562.362 s total, so query-time evaluation dominates the session build by ~16x.\n")
lines.append("- 50k cold admission 0.687 s; session build 14.555 s; selected 297.986 s; F2 reverse 295.457 s; F4 3-way 497.799 s.\n")
lines.append("- Source opens on the fixture producer: 0 (synthetic in-process generator). Full C11 repository builds on the saved path: 0 (tripwire). Whole `pq.read_table` calls: 0 (tripwire). Persistent second body corpus: none; each release has 13 family Parquet members + locator + manifest.\n")
lines.append("- Exact small-oracle parity: 48-respondent weighted fixture with A/B/C/D question families, reverse F2, same-respondent 3-way and 4-way joint, repeated occurrence, weighted query and I05; saved fact refs, semantic projections, release refs and I05 receipts equal native oracle. Changed C value changes the fact; old root restores exact old fact. Tests in `test_1006_baseline.py`: 6 passed.\n")
lines.append("- Accepted hostile regression suite reused proportionately: 31 passed (S2-C/S2-D direct estate); 29 passed for the RUNBOOK five-file S2-D group; a separate partial-binding-order suite passed 2; own baseline tests passed 6. The old 36-passed claim is withdrawn and is not a single test selection. See `evidence/`.\n")
lines.append("")
lines.append("## Historical-shape difference\n")
lines.append("The Nov 11 historical W03 shape was 100k rows / 200k events. Preserving F2/F4 with genuine same-respondent 3+ question joints requires at least 3 events for each fully joint respondent; this fixture therefore uses 100k distinct respondents / 324,477 events (A,B,C always; sparse D; repeated MR; typed missing B). This is the closest executable shape under the frozen requirement, not an apples-to-apples W03 rerun. No comparison or improvement claim against the historic W03 777.5 s / 5,923,426,304 B persistence RSS is made.\n")
lines.append("")
lines.append("## Dominant measured cost\n")
lines.append("At 100k the direct I02 proof is 2,249.700 s inclusive (74.2% of write), with 761.224 s reread/re-encode proof (25.1%) and 492.834 s `_row`/body_json overlapping both passes; root hashing is 11.101 s (0.37%). A 2k profiled decomposition shows the direct proof contains first-pass body construction/Parquet flush, object validation/insertion, projection/replay hashing and SQLite work; canonical projection/identity/object validation and body_json reconstruction dominate, while SQLite execute is only about 4.2% of the inflated 2k profile wall. Query economics are dominated by native respondent traversal in ref-key order across physically ordered row groups: at 100k selected there were 204,125 row-group reads / 103,133,313 decoded rows after a 33.508 s session build. A runtime-only physical-order candidate preserves exact facts/replay and reduces 100k selected to 5,784 reads / 265.680 s, but is EXPERIMENT_NOT_IMPLEMENTED pending owner handoff.\n")
lines.append("")
lines.append("## Rejected assumptions\n")
lines.append("- The 6 GiB process-tree cap was not the failure at 100k: writer 295 MB, query 3.69 GB. The material failure is time/query economics and repeated cold evaluation, not RSS.\n")
lines.append("- O(N) session build is real but bounded (33.5 s at 100k, 1.3 GB temp SQLite); it is not the dominant selected-query cost. The dominant query cause is cross-respondent ref-key traversal across physical row groups; per-respondent `(gid,off)` ordering cannot fix it.\n")
lines.append("- The accepted writer does not create a full C11 graph, does not reopen source and does not retain a second body corpus; its cost is exact canonical body/identity proof and JSON/SQLite work.\n")
lines.append("")
lines.append("## NOT_RUN / holds\n")
lines.append("- TRUE source snapshot/decode/projection cost: NOT_RUN_PENDING_997 accepted bridge handoff. The fixture generator is synthetic and in-process.\n")
lines.append("- 100k x 10 same-process and 10 fresh-process repetitions: NOT_RUN_MEASURED_COST. 1k and 10k meet n=10; skew has n=5; 50k/100k have one measured query each because the measured per-query seconds make the 10/10 court impractical in this dispatch. No substitute claim.\n")
lines.append("- Full 100k all-seven native readers (Batch/NORMAL/COMPLETED/PARTIAL/ABSENT plus I05/F2/F4) and #1001 whole-vertical 6 GiB certification: NOT_RUN. The all-seven readers were exercised at 1k/10k/skew against this same physical reader ABI; #1001 remains separate.\n")
lines.append("- #997 source bridge, #998 joined integration, #1001 full 100k/6 GiB, #1007 original-source rights: not owned here.\n")
lines.append("")
(ROOT / "evidence" / "baseline_table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(ROOT / "evidence" / "baseline_table.md")
