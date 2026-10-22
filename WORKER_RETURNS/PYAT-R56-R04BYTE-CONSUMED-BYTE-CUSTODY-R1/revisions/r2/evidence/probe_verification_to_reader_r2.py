"""R04BYTE r2 probe: replace the unlinked private snapshot pathname between verification and reader open.

Runs against the repaired decoder through the unchanged C11/I03 consumer.
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
    tmp = Path(tempfile.mkdtemp(prefix="r04byte-r2-probe-"))
    path = _write_source(tmp / f"source.{source_format}", source_format)
    alternate = _write_source(tmp / f"alternate.{source_format}", source_format, _ALTERNATE_ROWS)
    expected_sha = _sha(path)

    incidence = _decode(path, source_format, expected_sha)
    snapshot = incidence._source_snapshot
    baseline = _facts_from_incidence(incidence, source_format)
    snapshot_path = snapshot.path
    assert not snapshot_path.exists()
    calls = {"n": 0}

    def replace_once():
        if calls["n"] == 0:
            os.replace(alternate, snapshot_path)
        calls["n"] += 1

    observed = None
    if source_format == "sav":
        original_chunks = pyreadstat.read_file_in_chunks

        def hostile_chunks(reader, source, *args, **kwargs):
            replace_once()
            return original_chunks(reader, source, *args, **kwargs)

        pyreadstat.read_file_in_chunks = hostile_chunks
        try:
            observed = _facts_from_incidence(incidence, source_format)
        finally:
            pyreadstat.read_file_in_chunks = original_chunks
    else:
        original_read = pyreadstat.read_dta

        def hostile_read(source, *args, **kwargs):
            if not kwargs.get("metadataonly", False):
                replace_once()
            return original_read(source, *args, **kwargs)

        pyreadstat.read_dta = hostile_read
        try:
            observed = _facts_from_incidence(incidence, source_format)
        finally:
            pyreadstat.read_dta = original_read

    try:
        verify_after = incidence.verify_source_identity()
    except Exception as exc:  # noqa: BLE001
        verify_after = f"{type(exc).__name__}: {exc}"

    result = {
        "format": source_format,
        "expected_source_sha256": expected_sha,
        "reader_path_binding": incidence._source_snapshot.reader_path,
        "private_snapshot_path_exists_after_attack": snapshot_path.exists(),
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
    try:
        snapshot_path.unlink()
    except OSError:
        pass
    try:
        snapshot.directory.rmdir()
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
