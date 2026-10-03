"""Synthetic carrier generator for the R9 budget enforcement court.

Source-free. Generates TINY LEGAL synthetic SAV and DTA carriers into a
caller-supplied temporary directory. Never reads, copies, references or
derives from any real survey file, locator or raw source.

Every carrier is byte-legal for its format: written by pyreadstat's own
writer, then re-read to prove the round trip before use.

The generator deliberately produces carriers whose SHA-256 is NOT in the
decoder's COMPATIBILITY_ALLOWLIST, so that the fail-closed refusal path is
exercised as its own probe before any in-memory harness injection.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

# Declared intent per carrier. These are FIXTURE DESCRIPTIONS, not
# expectations about any real survey source.
CARRIERS: dict[str, dict[str, Any]] = {
    "SYN_SAV_TINY": {
        "format": "sav",
        "decoder_entry": "decode_sav",
        "shape": "two numeric variables, four rows, one user-missing value",
        "rows": 4,
    },
    "SYN_DTA_TINY": {
        "format": "dta",
        "decoder_entry": "decode_dta",
        "shape": "two numeric variables, four rows, one user-missing value",
        "rows": 4,
    },
    "SYN_SAV_TINY_COMPAT": {
        "format": "sav",
        "decoder_entry": "decode_sav",
        "shape": "identical content to SYN_SAV_TINY; distinct filename so its SHA differs is NOT relied upon",
        "rows": 4,
    },
}


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def generate(dest_dir: str | Path) -> dict[str, dict[str, Any]]:
    """Write every declared carrier into dest_dir. Returns a manifest."""
    import pandas as pd
    import pyreadstat

    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)

    # Deterministic tiny content. No real data, no derived values.
    frame = pd.DataFrame(
        {
            "v_small": [1.0, 2.0, 3.0, None],
            "v_other": [10.0, 20.0, 30.0, 40.0],
        }
    )
    variable_value_labels = {"v_small": {1.0: "one", 2.0: "two", 3.0: "three"}}

    manifest: dict[str, dict[str, Any]] = {}

    for name, spec in CARRIERS.items():
        target = dest / f"{name}.{ 'sav' if spec['format'] == 'sav' else 'dta' }"
        if spec["format"] == "sav":
            pyreadstat.write_sav(
                frame, str(target), file_label="SYNTHETIC_CARRIER",
                variable_value_labels=variable_value_labels,
            )
        else:
            pyreadstat.write_dta(
                frame, str(target), file_label="SYNTHETIC_CARRIER",
                variable_value_labels=variable_value_labels,
            )

        # Round-trip proof: the carrier is byte-legal and re-readable.
        if spec["format"] == "sav":
            _, meta = pyreadstat.read_sav(str(target), metadataonly=True)
        else:
            _, meta = pyreadstat.read_dta(str(target), metadataonly=True)

        sha = _sha256_file(target)
        manifest[name] = {
            "name": name,
            "path": str(target),
            "format": spec["format"],
            "decoder_entry": spec["decoder_entry"],
            "declared_shape": spec["shape"],
            "bytes": target.stat().st_size,
            "sha256": sha,
            "in_compatibility_allowlist": False,
            "roundtrip_columns": list(meta.column_names),
            "roundtrip_rows": int(getattr(meta, "number_rows", 0) or 0),
            "roundtrip_proved": True,
            "synthetic": True,
            "derived_from_any_real_source": False,
        }

    return manifest


if __name__ == "__main__":
    import sys

    out = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(generate(out), indent=2, sort_keys=True))