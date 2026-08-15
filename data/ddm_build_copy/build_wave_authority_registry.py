#!/usr/bin/env python3
"""Compile the closed 35-wave authority registry from installed files."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from data.ddm_build_copy.ddm_v550_family_overlay import (
    canonical_family_key,
    canonical_wave_key,
    load_family_overlay,
    wave_aliases,
)
from data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke import ALL_WAVES

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "data" / "ddm_build_copy" / "reports"
OUTPUT = ROOT / "data" / "ddm_build_copy" / "bindings" / "wave_authority_registry_35wave_v1.json"
STAGES = ("first_pass_authority", "semantic_authority", "position_conditioning", "directionality")
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII"}
WVS_YEARS = {"W1": "1981", "W4": "2000", "W7": "2017"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    entries = []
    for family, wave, _country in ALL_WAVES:
        stages = {}
        for stage in STAGES:
            loaded = load_family_overlay(family, wave, stage, required=True, search_roots=[REPORTS], use_registry=False)
            if loaded.status != "FOUND" or not loaded.path:
                raise RuntimeError(f"{family}/{wave}/{stage}: {loaded.status}: {loaded.message}")
            path = Path(loaded.path).resolve()
            stages[stage] = {
                "relative_path": str(path.relative_to(ROOT)),
                "sha256": sha256(path),
                "row_count": int(loaded.row_count),
                "columns": list(loaded.columns),
            }
        aliases = set(wave_aliases(family, wave)) | {wave}
        if family == "WVS" and wave in WVS_YEARS:
            number = int(wave[1:])
            aliases.update({WVS_YEARS[wave], ROMAN[number], f"W{ROMAN[number]}", f"WV{ROMAN[number]}"})
        entries.append({
            "source_family": family,
            "source_family_key": canonical_family_key(family),
            "canonical_wave": wave,
            "canonical_wave_key": canonical_wave_key(family, wave),
            "incoming_aliases": sorted(aliases),
            "stages": stages,
        })
    payload = {
        "registry_version": "wave_authority_registry_35wave_v1",
        "scope_status": "CLOSED_35_WAVES",
        "source": "run_20var_allwaves_v550_552j_smoke.ALL_WAVES",
        "entry_count": len(entries),
        "stage_names": list(STAGES),
        "entries": entries,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT} ({len(entries)} waves)")


if __name__ == "__main__":
    main()
