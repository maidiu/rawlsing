"""Independent probes: metadata-phase snapshot-path replacement and between-batch in-place alteration.

Runs against candidate c1b0abec decoder. Prints actual observed metadata/cells and identity.
"""
import json
import os
import sys
import tempfile
from pathlib import Path

REPO = Path.cwd()
sys.path.insert(0, str(REPO))

import pandas as pd  # noqa: E402
import pyreadstat  # noqa: E402

from rawlsing_next.pre553_physical_decoder import decode_sav  # noqa: E402
from rawlsing_next.tests.test_universal_source_byte_custody import (  # noqa: E402
    _ALTERNATE_ROWS,
    _ROWS,
    _sha,
    _write_source,
)


def metadata_window() -> dict:
    tmp = Path(tempfile.mkdtemp(prefix="r04bytev-meta-"))
    path = _write_source(tmp / "source.sav", "sav")
    renamed = tmp / "renamed.sav"
    frame = pd.DataFrame({("Z" if name == "W" else name): values for name, values in _ROWS.items()})
    pyreadstat.write_sav(frame, str(renamed))
    expected_sha = _sha(path)

    incidence_ok = decode_sav(path, expected_source_sha256=expected_sha)
    original_names = [v.name for v in incidence_ok.variables]
    incidence_ok.close()

    original_reader = pyreadstat.read_sav
    replaced = {"done": False}

    def hostile_reader(source, *args, **kwargs):
        if not replaced["done"] and kwargs.get("metadataonly"):
            replaced["done"] = True
            os.replace(renamed, source)
        return original_reader(source, *args, **kwargs)

    pyreadstat.read_sav = hostile_reader
    try:
        attacked = decode_sav(path, expected_source_sha256=expected_sha)
        attacked_names = [v.name for v in attacked.variables]
        attacked_sha = attacked.source_sha256
        attacked_custody = dict(attacked.source_custody or {})
        raw_layout = attacked.file_metadata["raw_layout_declarations"]["format_native_header"]
        attacked.close()
    finally:
        pyreadstat.read_sav = original_reader

    return {
        "original_variable_names": original_names,
        "attacked_variable_names": attacked_names,
        "attacked_source_sha256": attacked_sha,
        "expected_source_sha256": expected_sha,
        "attacked_snapshot_sha256": attacked_custody.get("snapshot_sha256"),
        "metadata_consumed_replacement": attacked_names != original_names,
        "raw_header_from_original_snapshot_fd": raw_layout.get("header_prefix_sha256"),
    }


def between_batch_window() -> dict:
    tmp = Path(tempfile.mkdtemp(prefix="r04bytev-batch-"))
    path = _write_source(tmp / "source.sav", "sav")
    alternate = _write_source(tmp / "alternate.sav", "sav", _ALTERNATE_ROWS)
    expected_sha = _sha(path)
    incidence = decode_sav(path, expected_source_sha256=expected_sha)
    snapshot_path = Path(incidence._source_snapshot.reader_path)
    alternate_bytes = alternate.read_bytes()

    observed_batches = []
    altered_after_first = False
    for batch in incidence.iter_batches(4):
        observed_batches.append([
            (cell.row_ordinal, cell.variable_name, cell.raw_value) for cell in batch
        ])
        if not altered_after_first:
            altered_after_first = True
            os.chmod(snapshot_path, 0o600)
            with snapshot_path.open("r+b") as handle:
                handle.write(alternate_bytes)
                handle.truncate()
    result = {
        "expected_source_sha256": expected_sha,
        "observed_batches": observed_batches,
        "row1_y": [c for c in observed_batches[0] if c[1] == "Y"],
        "row2_y": [c for c in observed_batches[1] if c[1] == "Y"] if len(observed_batches) > 1 else None,
        "row3_y": [c for c in observed_batches[2] if c[1] == "Y"] if len(observed_batches) > 2 else None,
        "alternate_row_y": [1, 1, 0],
        "verify_after": None,
    }
    try:
        result["verify_after"] = incidence.verify_source_identity()
    except Exception as exc:  # noqa: BLE001
        result["verify_after"] = f"{type(exc).__name__}: {exc}"
    incidence.close()
    return result


if __name__ == "__main__":
    print(json.dumps({
        "metadata_window": metadata_window(),
        "between_batch_window": between_batch_window(),
    }, indent=2, sort_keys=True, default=str))
