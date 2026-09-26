"""Collapse per-process zero-execution guards into the return telemetry receipt."""
from __future__ import annotations

import json
from pathlib import Path
import sys


directory = Path(sys.argv[1])
output = Path(sys.argv[2])
processes = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(directory.glob("process-*.json"))]
keys = (
    "raw_source_open_attempts",
    "raw_source_hash_sha_attempts",
    "decoder_calls",
    "candidate_process_launch_attempts",
    "synthetic_process_envelope_probe_launches",
    "measured_p2x_launch_attempts",
)
totals = {key: sum(item["counts"][key] for item in processes) for key in keys}
violations = [
    {"pid": item["pid"], "events": item["violations"]}
    for item in processes
    if item["violations"]
]
receipt = {
    "schema": "RAWLSING_FIABC_SOURCE_SPLIT_R2_ZERO_EXECUTION_TELEMETRY@1.0.0",
    "scope": "source-free integrated fan-in, adjacent, and protected joined-successor hostile suites",
    "instrumentation": {
        "python_audit_open_guard": "blocks survey-format source paths before open",
        "survey_decoder_guard": "blocks pyreadstat and pandas survey decoder calls",
        "candidate_process_guard": "blocks production A/B/C envelope launches and counts only SIMPLE_TEST_ONLY process probes separately",
        "measurement_guard": "blocks split/joined driver --run process launches",
        "python_processes_instrumented": len(processes),
    },
    "raw_source_opens": totals["raw_source_open_attempts"],
    "raw_source_hash_sha_passes": totals["raw_source_hash_sha_attempts"],
    "decoder_calls": totals["decoder_calls"],
    "candidate_abc_process_launch_attempts": totals["candidate_process_launch_attempts"],
    "synthetic_process_envelope_probe_launches": totals["synthetic_process_envelope_probe_launches"],
    "candidate_outputs": 0,
    "measured_p2x_executions": totals["measured_p2x_launch_attempts"],
    "violations": violations,
    "status": (
        "PASS__ZERO_SOURCE_AND_CANDIDATE_EXECUTION"
        if not any(
            totals[key]
            for key in (
                "raw_source_open_attempts",
                "raw_source_hash_sha_attempts",
                "decoder_calls",
                "candidate_process_launch_attempts",
                "measured_p2x_launch_attempts",
            )
        )
        and not violations
        else "BLOCKED__ZERO_EXECUTION_GUARD_TRIGGERED"
    ),
    "per_process_counts": [
        {"pid": item["pid"], **item["counts"]} for item in processes
    ],
}
output.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8")
if receipt["status"] != "PASS__ZERO_SOURCE_AND_CANDIDATE_EXECUTION":
    raise SystemExit(1)
