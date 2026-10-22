"""Independent fresh-process cold replay probe (SAV and DTA).

baseline old-digest decode -> replaced bytes under old digest must fail ->
restore exact original bytes -> identical fact payload.
Uses the real decoder + unchanged C11/I03 consumer via the author module helpers.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path.cwd()
sys.path.insert(0, str(REPO))

from rawlsing_next.tests.test_universal_source_byte_custody import (  # noqa: E402
    _ALTERNATE_ROWS,
    _write_source,
)

SCRIPT = (
    "import json, sys\n"
    "from rawlsing_next.tests.test_universal_source_byte_custody import _cold_observation\n"
    "print(json.dumps(_cold_observation(sys.argv[1], sys.argv[2], sys.argv[3]), sort_keys=True))\n"
)


def run_cold(path: Path, source_format: str, digest: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-c", SCRIPT, str(path), source_format, digest],
        cwd=REPO, capture_output=True, text=True, timeout=180,
    )


def main() -> int:
    receipt = {}
    for source_format in ("sav", "dta"):
        tmp = Path(tempfile.mkdtemp(prefix=f"r04bytev-cold-{source_format}-"))
        path = _write_source(tmp / f"cold.{source_format}", source_format)
        original_bytes = path.read_bytes()
        original_sha = hashlib.sha256(original_bytes).hexdigest()

        baseline = run_cold(path, source_format, original_sha)
        baseline_facts = json.loads(baseline.stdout) if baseline.returncode == 0 else None

        _write_source(path, source_format, _ALTERNATE_ROWS)
        changed_sha = hashlib.sha256(path.read_bytes()).hexdigest()
        fault = run_cold(path, source_format, original_sha)

        path.write_bytes(original_bytes)
        restored = run_cold(path, source_format, original_sha)
        restored_facts = json.loads(restored.stdout) if restored.returncode == 0 else None

        receipt[source_format] = {
            "original_sha256": original_sha,
            "changed_bytes_sha256": changed_sha,
            "baseline_returncode": baseline.returncode,
            "baseline_fact_ref": (baseline_facts or {}).get("i03_fact_ref"),
            "baseline_y_cells": (baseline_facts or {}).get("i03_y_cells"),
            "fault_returncode": fault.returncode,
            "fault_stdout_empty": fault.stdout == "",
            "fault_error": fault.stderr.strip().splitlines()[-1] if fault.stderr.strip() else None,
            "restored_returncode": restored.returncode,
            "restored_fact_ref": (restored_facts or {}).get("i03_fact_ref"),
            "restored_y_cells": (restored_facts or {}).get("i03_y_cells"),
            "restored_payload_equals_baseline": restored_facts == baseline_facts,
        }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
