"""Governed runtime proof for ASTRA-D02-R2.

This test does not materialize the LiTS carrier and does not add compatibility
semantics. It proves that the already accepted exact PRE553 DTA decoder can
execute against a real DTA file through the required pyreadstat backend on the
repo-native governed court surface.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import pandas as pd
import pyreadstat

import rawlsing_next.pre553_physical_decoder as decoder


EXPECTED_DECODER_GIT_BLOB = "13aa733b511dc23e00bfcdf288c5b920e3f09983"
EXPECTED_PYREADSTAT_VERSION = "1.3.6"
RUNTIME_RECEIPT = Path(".rabochii/astra_d02_r2_runtime_receipt.json")


def _git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    payload = f"blob {len(data)}\0".encode("ascii") + data
    return hashlib.sha1(payload).hexdigest()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_exact_dta_decoder_executes_with_required_pyreadstat_backend(tmp_path: Path) -> None:
    decoder_path = Path("rawlsing_next/pre553_physical_decoder.py")
    observed_blob = _git_blob_sha1(decoder_path)
    assert observed_blob == EXPECTED_DECODER_GIT_BLOB
    assert pyreadstat.__version__ == EXPECTED_PYREADSTAT_VERSION

    # This is a tiny generated transport fixture only. It is not the LiTS
    # carrier, and no encoding override is supplied, so the decoder's frozen
    # compatibility allowlist is not extended or exercised.
    fixture = tmp_path / "astra_d02_r2_runtime_probe.dta"
    pyreadstat.write_dta(
        pd.DataFrame({"runtime_probe": [1.0, 2.0], "second_probe": [10.0, 20.0]}),
        str(fixture),
    )

    incidence = decoder.decode_dta(fixture)
    cells = list(incidence.iter_cells(batch_size=2))

    assert incidence.source_format == "DTA"
    assert incidence.row_count == 2
    assert len(incidence.variables) == 2
    assert len(cells) == 4
    assert incidence.reader_configuration["reader"] == "pyreadstat"
    assert incidence.reader_configuration["reader_version"] == EXPECTED_PYREADSTAT_VERSION
    assert incidence.reader_configuration["user_missing"] is True
    assert incidence.reader_configuration["apply_value_formats"] is False
    assert incidence.reader_configuration["encoding"] is None
    assert incidence.reader_configuration["authority_status"] is None
    assert [cell.raw_value for cell in cells if cell.variable_name == "runtime_probe"] == [1.0, 2.0]

    receipt = {
        "schema_id": "ASTRA_D02_R2_GOVERNED_RUNTIME_RECEIPT@1.0.0",
        "result": "PASS",
        "commission_id": "ASTRA-D02-R2",
        "accepted_decoder_path": str(decoder_path),
        "accepted_decoder_git_blob_expected": EXPECTED_DECODER_GIT_BLOB,
        "accepted_decoder_git_blob_observed": observed_blob,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "pyreadstat_version": pyreadstat.__version__,
        "reader_configuration": dict(incidence.reader_configuration),
        "transport_fixture": {
            "kind": "SYNTHETIC_DTA_RUNTIME_PROBE_ONLY",
            "sha256": _sha256(fixture),
            "rows": incidence.row_count,
            "variables": len(incidence.variables),
            "cells_observed": len(cells),
        },
        "lits_carrier_materialized": False,
        "compatibility_allowlist_modified": False,
        "compatibility_encoding_exercised": False,
        "decoder_substitution_used": False,
        "alternate_reader_used": False,
        "scope": "EXECUTION_CAPABILITY_ONLY__NO_LITS_LEARNED_RESULT__NO_SEMANTIC_AUTHORITY",
    }
    RUNTIME_RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME_RECEIPT.write_text(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
