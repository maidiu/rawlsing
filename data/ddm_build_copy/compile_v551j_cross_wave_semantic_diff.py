#!/usr/bin/env python3
"""Compile the provisional V551J-D cross-wave semantic diff."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from time import monotonic

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs, write_frame_artifact, write_json_artifact
from data.ddm_build_copy.ddm_v551j_semantic_diff import (
    build_v551j_cross_wave_semantic_diff,
    validate_v551j_cross_wave_semantic_diff,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile the provisional V551J-D cross-wave semantic diff.")
    parser.add_argument("--comparison-id", required=True)
    parser.add_argument("--left-run-root", required=True)
    parser.add_argument("--right-run-root", required=True)
    parser.add_argument("--output-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v551j" / "comparisons"))
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--strict", action="store_true", default=True)
    parser.add_argument("--no-strict", dest="strict", action="store_false")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def _log_stage(enabled: bool, label: str, detail: str = "") -> None:
    if not enabled:
        return
    message = f"[V551J-D] {label}"
    if detail:
        message = f"{message}: {detail}"
    print(message, flush=True)


def main() -> int:
    args = parse_args()
    started = monotonic()
    output_dirs = ensure_output_dirs(args.output_root, args.comparison_id)

    _log_stage(args.verbose, "stage 1/5", "loading V551J runs")
    summary = build_v551j_cross_wave_semantic_diff(
        comparison_id=args.comparison_id,
        left_run_root=args.left_run_root,
        right_run_root=args.right_run_root,
    )
    _log_stage(
        args.verbose,
        "stage 1/5 complete",
        f"left_packets={summary['readiness_summary']['packet_count_left']} right_packets={summary['readiness_summary']['packet_count_right']}",
    )

    errors = validate_v551j_cross_wave_semantic_diff(summary)
    _log_stage(args.verbose, "stage 2/5", "validating provisional diff")
    _log_stage(args.verbose, "stage 2/5 complete", "validation_passed" if not errors else f"validation_errors={len(errors)}")
    if args.strict and errors:
        raise RuntimeError("V551J_CROSS_WAVE_SEMANTIC_DIFF_VALIDATION_FAILED: " + "; ".join(errors))

    _log_stage(args.verbose, "stage 3/5", "writing diff artifacts")
    write_frame_artifact(
        summary["packet_diff"],
        path=output_dirs["root"] / "v551j_cross_wave_packet_diff.parquet",
        schema_path=output_dirs["schemas"] / "v551j_cross_wave_packet_diff.schema.json",
        name="v551j_cross_wave_packet_diff",
        run_id=args.comparison_id,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
    )
    write_frame_artifact(
        summary["authority_diff"],
        path=output_dirs["root"] / "v551j_cross_wave_authority_diff.parquet",
        schema_path=output_dirs["schemas"] / "v551j_cross_wave_authority_diff.schema.json",
        name="v551j_cross_wave_authority_diff",
        run_id=args.comparison_id,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
    )
    write_frame_artifact(
        summary["affordance_diff"],
        path=output_dirs["root"] / "v551j_cross_wave_affordance_diff.parquet",
        schema_path=output_dirs["schemas"] / "v551j_cross_wave_affordance_diff.schema.json",
        name="v551j_cross_wave_affordance_diff",
        run_id=args.comparison_id,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
    )
    write_frame_artifact(
        summary["known_absence_diff"],
        path=output_dirs["root"] / "v551j_cross_wave_known_absence_diff.parquet",
        schema_path=output_dirs["schemas"] / "v551j_cross_wave_known_absence_diff.schema.json",
        name="v551j_cross_wave_known_absence_diff",
        run_id=args.comparison_id,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
    )
    _log_stage(args.verbose, "stage 3/5 complete", f"packet_diff_rows={len(summary['packet_diff'])}")

    _log_stage(args.verbose, "stage 4/5", "writing readiness and comparability reports")
    write_json_artifact(output_dirs["manifest"] / "v551j_cross_wave_readiness_summary.json", summary["readiness_summary"])
    write_json_artifact(output_dirs["manifest"] / "v551j_cross_wave_comparability_report.json", summary["comparability_report"])
    _log_stage(args.verbose, "stage 4/5 complete", f"status={summary['readiness_summary']['status']}")

    _log_stage(args.verbose, "stage 5/5", "done")
    if args.verbose:
        elapsed = monotonic() - started
        print(f"[V551J-D] completed in {elapsed:.1f}s -> {output_dirs['root']}", flush=True)
    print(summary["readiness_summary"]["status"])
    print(str(output_dirs["manifest"] / "v551j_cross_wave_readiness_summary.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
