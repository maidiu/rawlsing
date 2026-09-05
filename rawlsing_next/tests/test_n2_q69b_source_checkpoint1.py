from __future__ import annotations

import hashlib
import importlib
import json
import pathlib
import subprocess
import sys
import tempfile
import urllib.request
import warnings

OFFICIAL_URL = (
    "https://www.afrobarometer.org/wp-content/uploads/2022/02/"
    "merged-round-5-data-34-countries-2011-2013-last-update-july-2015.sav"
)
EXPECTED_SHA256 = "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651"
EXPECTED_BYTES = 49_689_458
EXPECTED_ROWS = 51_587
REQUIRED_VARIABLES = ("COUNTRY", "RESPNO", "Q69B", "DATEINTR")
PYREADSTAT_VERSION = "1.3.6"


def _ensure_pyreadstat():
    try:
        module = importlib.import_module("pyreadstat")
    except ModuleNotFoundError:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                f"pyreadstat=={PYREADSTAT_VERSION}",
            ]
        )
        module = importlib.import_module("pyreadstat")
    assert module.__version__ == PYREADSTAT_VERSION
    return module


def _download_exact(path: pathlib.Path) -> tuple[int, str]:
    request = urllib.request.Request(
        OFFICIAL_URL,
        headers={"User-Agent": "Rawlsing-N2-exact-byte-recovery/1.0"},
    )
    digest = hashlib.sha256()
    total = 0
    with urllib.request.urlopen(request, timeout=120) as response, path.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
            digest.update(chunk)
            total += len(chunk)
    return total, digest.hexdigest()


def test_n2_checkpoint1_exact_source_bytes_and_inventory() -> None:
    with tempfile.TemporaryDirectory(prefix="rawlsing_n2_") as tmp:
        source = pathlib.Path(tmp) / "afrobarometer_r5_accepted.sav"
        byte_count, source_sha256 = _download_exact(source)

        assert byte_count == EXPECTED_BYTES, (
            f"N2_SOURCE_SIZE_MISMATCH expected={EXPECTED_BYTES} got={byte_count}"
        )
        assert source_sha256 == EXPECTED_SHA256, (
            "N2_SOURCE_SHA_MISMATCH "
            f"expected={EXPECTED_SHA256} got={source_sha256}"
        )

        pyreadstat = _ensure_pyreadstat()
        _, metadata = pyreadstat.read_sav(
            str(source),
            metadataonly=True,
            disable_datetime_conversion=True,
        )
        names = tuple(metadata.column_names)
        missing = tuple(name for name in REQUIRED_VARIABLES if name not in names)
        assert not missing, f"N2_REQUIRED_VARIABLES_MISSING {missing!r}"
        assert metadata.number_rows == EXPECTED_ROWS, (
            f"N2_METADATA_ROW_COUNT_MISMATCH expected={EXPECTED_ROWS} "
            f"got={metadata.number_rows}"
        )

        checkpoint = {
            "schema_id": "GT34_N2_Q69B_SOURCE_CHECKPOINT1@1.0.0",
            "source_route": "OFFICIAL_AFROBAROMETER_EXACT_BYTE_REACQUISITION",
            "official_url": OFFICIAL_URL,
            "source_byte_count": byte_count,
            "source_sha256": source_sha256,
            "expected_rows": EXPECTED_ROWS,
            "metadata_rows": metadata.number_rows,
            "metadata_columns": metadata.number_columns,
            "required_variable_inventory": {
                name: names.index(name) for name in REQUIRED_VARIABLES
            },
            "python_version": sys.version.split()[0],
            "parser": "pyreadstat",
            "parser_version": pyreadstat.__version__,
            "row_values_read": False,
            "row_values_committed": False,
        }
        warnings.warn(
            "N2_CHECKPOINT1_JSON="
            + json.dumps(checkpoint, sort_keys=True, separators=(",", ":")),
            RuntimeWarning,
            stacklevel=1,
        )
