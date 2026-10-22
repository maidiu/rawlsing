"""Independent probe: private snapshot-path replacement between verify() and reader open.

Runs against candidate c1b0abec decoder through the unchanged C11/I03 consumer.
Prints actual facts and source identity before/after the attack.
"""
import json
import os
import sys
import tempfile
from pathlib import Path

REPO = Path.cwd()
sys.path.insert(0, str(REPO))

import pyreadstat  # noqa: E402

from rawlsing_next.tests.test_universal_source_byte_custody import (  # noqa: E402
    _ALTERNATE_ROWS,
    _decode,
    _facts_from_incidence,
    _sha,
    _write_source,
)


def main(source_format: str) -> int:
    tmp = Path(tempfile.mkdtemp(prefix="r04bytev-probe-"))
    path = _write_source(tmp / f"source.{source_format}", source_format)
    alternate = _write_source(tmp / f"alternate.{source_format}", source_format, _ALTERNATE_ROWS)
    expected_sha = _sha(path)

    incidence = _decode(path, source_format, expected_sha)
    baseline = _facts_from_incidence(incidence, source_format)
    baseline_snapshot = incidence._source_snapshot
    snapshot_path = Path(baseline_snapshot.reader_path)

    calls = {"n": 0}
    original_chunks = pyreadstat.read_file_in_chunks

    def hostile_chunks(reader, source, *args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            os.replace(alternate, snapshot_path)
        return original_chunks(reader, source, *args, **kwargs)

    pyreadstat.read_file_in_chunks = hostile_chunks
    try:
        observed = _facts_from_incidence(incidence, source_format)
    finally:
        pyreadstat.read_file_in_chunks = original_chunks

    verify_after = None
    try:
        verify_after = incidence.verify_source_identity()
    except Exception as exc:  # noqa: BLE001
        verify_after = f"{type(exc).__name__}: {exc}"

    result = {
        "format": source_format,
        "expected_source_sha256": expected_sha,
        "alternate_sha256": _sha(alternate) if alternate.exists() else "moved-onto-snapshot",
        "baseline_source_sha256": baseline["source_sha256"],
        "baseline_snapshot_sha256": baseline["snapshot_sha256"],
        "baseline_i03_y_cells": baseline["i03_y_cells"],
        "baseline_i03_fact_ref": baseline["i03_fact_ref"],
        "observed_source_sha256": observed["source_sha256"],
        "observed_snapshot_sha256": observed["snapshot_sha256"],
        "observed_i03_y_cells": observed["i03_y_cells"],
        "observed_i03_fact_ref": observed["i03_fact_ref"],
        "observed_equals_baseline": observed == baseline,
        "verify_source_identity_after_attack": verify_after,
        "reader_calls": calls["n"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    incidence.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
