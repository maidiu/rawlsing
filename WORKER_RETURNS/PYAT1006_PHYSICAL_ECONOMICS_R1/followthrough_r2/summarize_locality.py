from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOCAL = HERE / ".local-data"
OUT = HERE / "evidence"


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def _reads(probe: dict, query: str) -> dict:
    row = probe["queries"][query]
    reads = row["reads"]
    phases = reads.get("by_phase", {})
    families = {}
    for phase in phases.values():
        for family, values in phase.get("families", {}).items():
            families[family] = {
                "reads": values.get("reads"),
                "rows_decoded": values.get("rows_decoded"),
                "unique_gids": values.get("unique_gids"),
                "read_seconds": values.get("seconds"),
                "reads_per_unique_gid": (
                    values.get("reads") / values.get("unique_gids")
                    if values.get("unique_gids") else None
                ),
            }
    return {
        "total_reads": reads.get("total_reads"),
        "total_rows_decoded": sum(
            phase.get("rows_decoded", 0) for phase in phases.values()
        ),
        "families": families,
    }


def main() -> int:
    summary = {
        "schema": "PYAT1006_LOCALITY_CANDIDATE_SUMMARY@1",
        "label": "EXPERIMENT_NOT_IMPLEMENTED",
        "review_g5_commit": "0169fac9f3840800796c664eee462bbb8984bb42",
        "review_g5_verdict": "REVISE_EXACT_DEFECT",
        "cases": {},
    }
    for directory, name in (
        (LOCAL / "matrix-1k10k", "matrix_1k_10k"),
        (LOCAL / "matrix-100k", "matrix_100k"),
    ):
        document = _load(directory / "locality_matrix.json")
        for case, pair in document["cases"].items():
            entry = {
                "queries": pair["queries"],
                "baseline_tree_rss_bytes": pair["runs"]["baseline"]["process_tree"]["tree_peak_rss_bytes"],
                "candidate_tree_rss_bytes": pair["runs"]["candidate"]["process_tree"]["tree_peak_rss_bytes"],
                "capsule": pair["runs"]["baseline"]["capsule"],
                "capsule_sha256": pair["runs"]["baseline"]["capsule_sha256"],
                "comparison": pair["comparison"],
                "queries_detail": {},
            }
            for query in [item for item in pair["queries"].split(",") if item]:
                base_probe = pair["runs"]["baseline"]["probe"]
                cand_probe = pair["runs"]["candidate"]["probe"]
                entry["queries_detail"][query] = {
                    "baseline": {
                        "wall_seconds": base_probe["queries"][query]["wall_seconds"],
                        "cpu_seconds": base_probe["queries"][query]["cpu_seconds"],
                        "temp_sqlite_peak_bytes": base_probe["queries"][query].get(
                            "temp_sqlite_peak_bytes"
                        ),
                        "reads": _reads(base_probe, query),
                    },
                    "candidate": {
                        "wall_seconds": cand_probe["queries"][query]["wall_seconds"],
                        "cpu_seconds": cand_probe["queries"][query]["cpu_seconds"],
                        "temp_sqlite_peak_bytes": cand_probe["queries"][query].get(
                            "temp_sqlite_peak_bytes"
                        ),
                        "reads": _reads(cand_probe, query),
                    },
                    "wall_factor": (
                        base_probe["queries"][query]["wall_seconds"]
                        / cand_probe["queries"][query]["wall_seconds"]
                    ),
                    "read_factor": (
                        base_probe["queries"][query]["reads"]["total_reads"]
                        / cand_probe["queries"][query]["reads"]["total_reads"]
                    ),
                }
            summary["cases"][case] = entry
    (OUT / "locality_candidate_matrix.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    lines = [
        "# Locality candidate — TEST_ONLY runtime experiment",
        "",
        "**EXPERIMENT_NOT_IMPLEMENTED.** Production is unchanged. The probe only",
        "patches the module-global `sorted` lookup in `_pre553_query_eval` so native",
        "respondent traversal follows the session's physical insertion order.",
        "All integrity, routing, predicate, risk, fact and replay owners remain the",
        "accepted code.",
        "",
        "## Matched same-release results",
        "",
        "| case | query | baseline wall s | candidate wall s | factor | baseline RGR | candidate RGR | rows decoded B/C | fact/replay exact |",
        "|---|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for case, entry in summary["cases"].items():
        for query, detail in entry["queries_detail"].items():
            base = detail["baseline"]
            cand = detail["candidate"]
            cmp = entry["comparison"][query]
            lines.append(
                f"| {case} | {query} | {base['wall_seconds']:.3f} | "
                f"{cand['wall_seconds']:.3f} | {detail['wall_factor']:.2f}x | "
                f"{base['reads']['total_reads']} | {cand['reads']['total_reads']} | "
                f"{base['reads']['total_rows_decoded']}/{cand['reads']['total_rows_decoded']} | "
                f"{cmp['fact_refs_equal'] and cmp['projection_sha256_equal'] and cmp['replay_refs_equal'] and cmp['release_refs_equal']} |"
            )
    lines += [
        "",
        "## Interpretation",
        "",
        "- The 100k selected query falls from 580.548 s / 204,125 row-group reads",
        "  to 265.680 s / 5,784 reads with exact fact, projection, replay and",
        "  release refs.  Tree RSS is 2.81 GiB versus 2.95 GiB; temp SQLite is",
        "  1.301 GB in both.",
        "- 10k selected/F2/F4 fall from 49.1/51.8/56.6 s to 21.8/21.1/24.7 s,",
        "  with exact parity; 1k falls from 4.4/4.5/5.0 s to 2.0/2.0/2.5 s.",
        "- Candidate row-group reads per unique gid: at 100k, events 634/634 =",
        "  1.0 and routing 2,513/977 = 2.57; baseline events 100,050/634 = 157.8",
        "  and routing 101,438/977 = 103.8.",
        "- Remaining candidate 100k selected time is native object/predicate",
        "  evaluation (about 247.8 CPU s) and session build; the read churn is",
        "  removed.  This is a candidate for a narrow S2-C/D handoff, not an",
        "  optimized engine acceptance.",
        "",
        "## Limits",
        "",
        "- 100k reverse F2/F4 were NOT_RUN in this follow-through; 10k matched",
        "  F2/F4 exact parity is the scale proxy and the original 100k F2/F4",
        "  remain NOT_INDEPENDENTLY_REPRODUCED.",
        "- Candidate is a runtime override, not a production patch, owner",
        "  acceptance, or G5 acceptance.  #999 native body-truth RED remains.",
        "",
    ]
    (OUT / "locality_candidate_summary.md").write_text("\n".join(lines))
    print(json.dumps({case: {q: {
        "factor": v["wall_factor"], "reads_factor": v["read_factor"],
        "exact": summary["cases"][case]["comparison"][q]["fact_refs_equal"]
                  and summary["cases"][case]["comparison"][q]["projection_sha256_equal"]
    } for q, v in entry["queries_detail"].items()} for case, entry in summary["cases"].items()}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
