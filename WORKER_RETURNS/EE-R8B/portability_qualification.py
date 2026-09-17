import datetime
import hashlib
import json
import os
import pathlib
import sys
import types

root = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(root / "runtime_code"))
from rawlsing_next import ee_w4_harness_runtime as runtime


class Usage:
    ru_utime = 1.25
    ru_stime = 0.5
    ru_maxrss = 1234567


def metrics_for(platform):
    original = runtime.sys
    runtime.sys = types.SimpleNamespace(platform=platform)
    try:
        return runtime.rusage_metrics(Usage())
    finally:
        runtime.sys = original


linux = metrics_for("linux")
darwin = metrics_for("darwin")
unsupported = None
try:
    metrics_for("freebsd13")
except RuntimeError as exc:
    unsupported = str(exc)
assert linux == {
    "cpu_user_ns": 1250000000,
    "cpu_system_ns": 500000000,
    "peak_rss_native": 1234567,
    "peak_rss_native_unit": "KiB",
    "peak_rss_bytes": 1234567 * 1024,
}
assert darwin == {
    "cpu_user_ns": 1250000000,
    "cpu_system_ns": 500000000,
    "peak_rss_native": 1234567,
    "peak_rss_native_unit": "bytes",
    "peak_rss_bytes": 1234567,
}
assert unsupported == "unsupported ru_maxrss unit for platform: 'freebsd13'"

receipt = {
    "schema": "RAWLSING_EE_R8B_RUSAGE_METRICS_PORTABILITY_QUALIFICATION@1.0.0",
    "status": "PASS_UNIT_NORMALIZATION_ONLY",
    "executed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "driver_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    "runtime_path": "rawlsing_next/ee_w4_harness_runtime.py",
    "runtime_sha256": hashlib.sha256((root / "runtime_code/rawlsing_next/ee_w4_harness_runtime.py").read_bytes()).hexdigest(),
    "linux_representative_metrics": linux,
    "darwin_representative_metrics": darwin,
    "unsupported_platform_result": {"exception_type": "RuntimeError", "message": unsupported},
    "preserved_telemetry_keys": sorted(darwin),
}
(root / "portability_unit_receipt.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
print("PASS_UNIT_NORMALIZATION_ONLY")
