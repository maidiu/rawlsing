#!/usr/bin/env python3
"""Build a per-file accounting manifest for raw survey data and codebooks.

This manifest is meant to support long-running offline loops by making every
raw data file and every canonical codebook file individually explicit.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd
import pyreadstat
import yaml


ROOT = Path(__file__).resolve().parents[2]
DDM_ROOT = ROOT / "data" / "ddm_build_copy"
MANIFEST_OUT = DDM_ROOT / "manifests" / "file_accounting_manifest.csv"
REPORT_OUT = DDM_ROOT / "manifests" / "file_accounting_manifest.yaml"
CODEBOOK_DIR = ROOT / "data" / "FINAL CODEBOOKS" / "FINAL FINAL CODEBOOKS"
RAW_DATA_DIR = ROOT / "data" / "Data"


def _strip_accents(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


def _slugify_identifier(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", _strip_accents(text)).strip("_")
    return slug or "unknown"


def _canonical_source_family(source_family: str) -> str:
    raw = source_family.strip()
    return {
        "Afro Barometer": "Afrobarometer",
        "Afrobarometer": "Afrobarometer",
        "Arab Barometer": "Arab Barometer",
        "Asian Barometer": "Asian Barometer",
        "EVS": "EVS",
        "GSS": "GSS",
        "Latinobarometro": "Latinobarómetro",
        "Latinobarómetro": "Latinobarómetro",
        "LiTS": "LiTS",
        "South Asia": "South Asia",
        "WVS": "WVS",
        "World Values Survey": "WVS",
    }.get(raw, raw)


def canonical_wave_label(source_family: str, raw_wave: str) -> str:
    source_family = _canonical_source_family(source_family)
    raw_wave = str(raw_wave).strip()
    if source_family == "Arab Barometer":
        return {
            "I": "W1",
            "II": "W2",
            "III": "W3",
            "IV": "W4",
            "V": "W5",
            "VI_pt_i": "W6a",
            "VI_pt_ii": "W6b",
            "VI_pt_iii": "W6c",
            "VII": "W7",
            "VIII": "W8",
            "Wave 1": "W1",
            "Wave 2": "W2",
            "Wave 5": "W5",
            "Wave 8": "W8",
        }.get(raw_wave, raw_wave)
    if source_family == "Afrobarometer":
        return {
            "Round 1": "R1",
            "Round 5": "R5",
            "Round 9": "R9",
            "R1": "R1",
            "R5": "R5",
            "R9": "R9",
        }.get(raw_wave, raw_wave)
    if source_family == "Asian Barometer":
        return {
            "Wave 1": "W1",
            "W1": "W1",
            "Wave 4": "W4",
            "W4": "W4",
            "Wave 5": "W5",
            "W5": "W5",
            "Wave 6": "W6",
            "W6": "W6",
        }.get(raw_wave, "W6" if raw_wave.startswith("Wave 6") else raw_wave)
    if source_family == "South Asia":
        return {"Wave 1": "W1", "W1": "W1", "Wave 2": "W2", "W2": "W2"}.get(raw_wave, raw_wave)
    if source_family == "Latinobarómetro":
        return {"1995": "1995", "2011": "2011", "2024": "2024"}.get(raw_wave, raw_wave)
    if source_family == "EVS":
        return {
            "1981": "1981",
            "1990": "1990",
            "1999": "1999",
            "2008": "2008",
            "2017": "2017",
            "TREND": "TREND",
        }.get(raw_wave, raw_wave)
    if source_family == "WVS":
        return {"Wave 1": "W1", "W1": "W1", "Wave 4": "W4", "W4": "W4", "Wave 7": "W7", "W7": "W7"}.get(raw_wave, raw_wave)
    if source_family == "GSS":
        return raw_wave
    if source_family == "LiTS":
        return {"2006": "2006", "I": "2006", "II": "II", "III": "III", "IV": "IV"}.get(raw_wave, raw_wave)
    return raw_wave


def _infer_raw_family_and_wave(path: Path) -> tuple[str, str]:
    name = path.name
    stem = path.stem
    lower = name.lower()

    if lower.startswith("afro barometer round "):
        return "Afrobarometer", stem.replace("Afro Barometer ", "")
    if lower.startswith("arab barometer wave "):
        match = re.search(r"wave\s+(\d+)", lower)
        return "Arab Barometer", f"Wave {match.group(1)}" if match else "Wave unknown"
    if lower.startswith("asian barometer wave 1"):
        return "Asian Barometer", "Wave 1"
    if lower.startswith("asian barometer wave 4"):
        return "Asian Barometer", "Wave 4"
    if lower.startswith("asian barometer wave 5"):
        return "Asian Barometer", "Wave 5"
    if lower.startswith("asian barometer wave 6 "):
        return "Asian Barometer", f"Wave 6 {stem.split('Wave 6 ', 1)[1]}"
    if lower.startswith("evs "):
        match = re.match(r"EVS\s+(\d{4})(?:\b|$)", stem)
        if match:
            return "EVS", match.group(1)
    if lower.startswith("gss") and stem[3:].isdigit():
        return "GSS", stem[3:]
    if lower.startswith("latinobarometro ") and stem.split()[1].isdigit():
        return "Latinobarometro", stem.split()[1]
    if stem.lower() == "lits_i":
        return "LiTS", "2006"
    if stem.lower() == "lits_ii":
        return "LiTS", "II"
    if stem.lower() == "lits_iii":
        return "LiTS", "III"
    if stem.lower() == "lits_iv":
        return "LiTS", "IV"
    if lower.startswith("south asia wave "):
        match = re.search(r"wave\s+(\d+)", lower)
        return "South Asia", f"Wave {match.group(1)}" if match else "Wave unknown"
    if lower.startswith("wvs wave "):
        match = re.search(r"wave\s+(\d+)", lower)
        return "WVS", f"Wave {match.group(1)}" if match else "Wave unknown"
    raise ValueError(f"Unrecognized raw file name: {path.name}")


def _read_raw_metadata(path: Path) -> tuple[str, int | pd.NA, int | pd.NA, str]:
    try:
        if path.suffix.lower() == ".sav":
            try:
                _, meta = pyreadstat.read_sav(str(path), metadataonly=True)
            except Exception:
                _, meta = pyreadstat.read_sav(str(path), metadataonly=True, encoding="latin1")
        elif path.suffix.lower() == ".dta":
            _, meta = pyreadstat.read_dta(str(path), metadataonly=True)
        else:
            return "blocked_read_error", pd.NA, pd.NA, f"unsupported extension: {path.suffix}"
        return "green_metadata_read", int(meta.number_rows), int(meta.number_columns), ""
    except Exception as exc:  # pragma: no cover - defensive for future file formats
        return "blocked_read_error", pd.NA, pd.NA, repr(exc)


def _raw_row_for_path(path: Path) -> dict:
    source_family, wave = _infer_raw_family_and_wave(path)
    source_family = _canonical_source_family(source_family)
    canonical_wave = canonical_wave_label(source_family, wave)
    read_status, row_count, column_count, error = _read_raw_metadata(path)
    return {
        "artifact_kind": "raw_data",
        "source_family": source_family,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "canonical_intended": True,
        "dataset_id": _slugify_identifier(f"{source_family}_{wave}_{path.stem}"),
        "path": str(path),
        "relative_path": str(path.relative_to(RAW_DATA_DIR)),
        "format": path.suffix.lstrip(".").lower(),
        "size_bytes": path.stat().st_size,
        "sha256": "",
        "read_status": read_status,
        "row_count": row_count,
        "column_count": column_count,
        "paired_codebook_name": "",
        "paired_codebook_path": "",
        "paired_codebook_exists": False,
        "paired_raw_path": "",
        "error": error,
    }


def parse_codebook_filename(name: str) -> tuple[str, str, bool]:
    n = name.lower()
    if "arab barometer wave 1" in n:
        return "Arab Barometer", "W1", True
    if "arab barometer wave 2" in n:
        return "Arab Barometer", "W2", True
    if "arab barometer wave 5" in n:
        return "Arab Barometer", "W5", True
    if "arab barometer wave 8" in n or "arabbarometer_abviii" in n:
        return "Arab Barometer", "W8", True
    if "afrobarometer round 1" in n:
        return "Afrobarometer", "R1", True
    if "afrobarometer round 5" in n:
        return "Afrobarometer", "R5", True
    if "afrobarometer round 9" in n:
        return "Afrobarometer", "R9", True
    if "asian barometer wave 1" in n:
        return "Asian Barometer", "W1", True
    if "asian barometer wave 4" in n:
        return "Asian Barometer", "W4", True
    if "asian barometer wave 5" in n or "w5 merged data" in n or "w5 merge" in n:
        return "Asian Barometer", "W5", True
    if "asian barometer wave 6" in n:
        return "Asian Barometer", "W6", True
    if "south asia wave 1" in n or "sa wave1" in n or "sdsa 2005" in n:
        return "South Asia", "W1", True
    if "south asia wave 2" in n or "sa wave2" in n or "sdsa 2013" in n:
        return "South Asia", "W2", True
    if "latinobarometro 1995" in n:
        return "Latinobarómetro", "1995", True
    if "latinobarometro 2011" in n:
        return "Latinobarómetro", "2011", True
    if "latinobarometro 2024" in n:
        return "Latinobarómetro", "2024", True
    if "evs wave 1" in n or "1981" in n:
        return "EVS", "1981", True
    if "evs wave 2" in n or "1990" in n:
        return "EVS", "1990", True
    if "evs wave 3" in n or "1999" in n:
        return "EVS", "1999", True
    if "evs wave 4" in n or "2008" in n:
        return "EVS", "2008", True
    if "evs wave 5" in n or "2017" in n:
        return "EVS", "2017", True
    if "world values survey wave 1" in n or "wvs wave 1" in n:
        return "WVS", "W1", True
    if "world values survey wave 4" in n or "wvs wave 4" in n:
        return "WVS", "W4", True
    if "world values survey wave 7" in n or "wvs wave 7" in n:
        return "WVS", "W7", True
    if "gss1972-codebook" in n:
        return "GSS", "1972", True
    if "gss1973-codebook" in n:
        return "GSS", "1973", True
    if "gss1982-codebook" in n:
        return "GSS", "1982", True
    if "gss1984-codebook" in n:
        return "GSS", "1984", True
    if "gss1993-codebook" in n:
        return "GSS", "1993", True
    if "gss2002-codebook" in n:
        return "GSS", "2002", True
    if "gss2010-codebook" in n:
        return "GSS", "2010", True
    if "gss2016-codebook" in n:
        return "GSS", "2016", True
    if "gss2024-codebook" in n:
        return "GSS", "2024", True
    if "lits-i-codebook" in n or "lits 2006 codebook" in n or "lits-2006-codebook" in n:
        return "LiTS", "2006", True
    if "lits-ii-codebook" in n or "lits ii codebook" in n:
        return "LiTS", "II", True
    if "lits-iii-codebook" in n:
        return "LiTS", "III", True
    if "lits-iv-codebook" in n:
        return "LiTS", "IV", True
    return "unknown", "unknown", False


def load_raw_manifest() -> pd.DataFrame:
    rows = []
    for path in sorted(RAW_DATA_DIR.iterdir()):
        if not path.is_file() or path.name == ".DS_Store":
            continue
        rows.append(_raw_row_for_path(path))
    return pd.DataFrame(rows)


def load_codebook_manifest() -> pd.DataFrame:
    rows = []
    if not CODEBOOK_DIR.exists():
        return pd.DataFrame(rows)
    for path in sorted(CODEBOOK_DIR.glob("*.csv")):
        source_family, wave, canonical_intended = parse_codebook_filename(path.name)
        source_family = _canonical_source_family(source_family)
        rows.append(
            {
                "artifact_kind": "codebook",
                "source_family": source_family,
                "wave": wave,
                "canonical_wave": wave,
                "canonical_intended": canonical_intended,
                "dataset_id": _slugify_identifier(f"{source_family}_{wave}"),
                "path": str(path),
                "relative_path": str(path.relative_to(CODEBOOK_DIR)),
                "format": "csv",
                "size_bytes": path.stat().st_size,
                "sha256": "",
                "read_status": "codebook_present",
                "row_count": pd.NA,
                "column_count": pd.NA,
                "paired_codebook_name": "",
                "error": "",
            }
        )
    return pd.DataFrame(rows)


def main() -> int:
    raw_df = load_raw_manifest()
    codebook_df = load_codebook_manifest()

    codebook_lookup = {
        (str(row.source_family), str(row.canonical_wave)): row.path
        for row in codebook_df.itertuples(index=False)
    }
    raw_df["paired_codebook_path"] = raw_df.apply(
        lambda r: codebook_lookup.get((str(r["source_family"]), str(r["canonical_wave"])), ""),
        axis=1,
    )
    raw_df["paired_codebook_name"] = raw_df["paired_codebook_path"].apply(
        lambda p: Path(str(p)).name if p else ""
    )
    raw_df["paired_codebook_exists"] = raw_df["paired_codebook_path"].astype(str).str.len().gt(0)

    raw_lookup = {
        (str(row.source_family), str(row.canonical_wave)): row.path
        for row in raw_df.itertuples(index=False)
    }
    codebook_df["paired_raw_path"] = codebook_df.apply(
        lambda r: raw_lookup.get((str(r["source_family"]), str(r["canonical_wave"])), ""),
        axis=1,
    )

    manifest = pd.concat([raw_df, codebook_df], ignore_index=True, sort=False)
    manifest = manifest[
        [
            "artifact_kind",
            "source_family",
            "wave",
            "canonical_wave",
            "canonical_intended",
            "dataset_id",
            "path",
            "relative_path",
            "format",
            "size_bytes",
            "sha256",
            "read_status",
            "row_count",
            "column_count",
            "paired_codebook_name",
            "paired_codebook_path",
            "paired_codebook_exists",
            "paired_raw_path",
            "error",
        ]
    ].copy()

    MANIFEST_OUT.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(MANIFEST_OUT, index=False)
    payload = {
        "status": "green_file_accounting_manifest_written",
        "row_count": int(len(manifest)),
        "raw_count": int((manifest["artifact_kind"] == "raw_data").sum()),
        "codebook_count": int((manifest["artifact_kind"] == "codebook").sum()),
        "canonical_intended_raw_count": int(((manifest["artifact_kind"] == "raw_data") & (manifest["canonical_intended"] == True)).sum()),
        "canonical_intended_codebook_count": int(((manifest["artifact_kind"] == "codebook") & (manifest["canonical_intended"] == True)).sum()),
        "blocked_raw_count": int((manifest["read_status"].astype(str).str.contains("blocked")).sum()),
        "output_file": str(MANIFEST_OUT),
        "limitations": [
            "Raw file accounting comes directly from data/Data and only includes files present there now.",
            "Codebook accounting comes directly from FINAL FINAL CODEBOOKS and only includes files present there now.",
            "Counts are enriched from metadata-only reads of the current raw files when possible.",
        ],
    }
    REPORT_OUT.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    print(f"Wrote file accounting manifest to {MANIFEST_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
