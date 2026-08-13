#!/usr/bin/env python3
"""Build centralized review candidates for legacy GSS directionality files.

Copying or finding an overlay does not certify it. Every generated row is
explicitly review-only until an independent authority action changes its
status.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OVERLAY_DIR = ROOT / "data" / "ddm_build_copy" / "reports"
DEFAULT_AUTHORITY_DIR = ROOT / "data" / "ddm_build_copy" / "directionality_authority"

EXTRA_ROWS_1972 = [
    {
        "source": "GSS",
        "wave": "1972",
        "canonical_wave": "1972",
        "var_name": "pres68",
        "question_text": "vote for humphrey, nixon, or wallace",
        "semantic_role": "relation_evidence",
        "semantic_subrole": "political_choice_coordinate",
        "directionality_policy": "unsigned_identity",
        "signed_polarity_status": "unsigned_identity",
        "response_family_expectation": "nominal_single_choice",
        "positive_anchor_label": "",
        "negative_anchor_label": "",
        "neutral_anchor_label": "",
        "bridge_directionality_action": "force_unsigned",
        "directionality_confidence": "high",
        "directionality_note": "nominal political choice; keep unsigned",
        "manual_review_required": True,
    },
    {
        "source": "GSS",
        "wave": "1972",
        "canonical_wave": "1972",
        "var_name": "other",
        "question_text": "other protestant denominations",
        "semantic_role": "relation_evidence",
        "semantic_subrole": "religious_affiliation_coordinate",
        "directionality_policy": "unsigned_identity",
        "signed_polarity_status": "unsigned_identity",
        "response_family_expectation": "nominal_single_choice",
        "positive_anchor_label": "",
        "negative_anchor_label": "",
        "neutral_anchor_label": "",
        "bridge_directionality_action": "force_unsigned",
        "directionality_confidence": "high",
        "directionality_note": "nominal religious affiliation; keep unsigned",
        "manual_review_required": True,
    },
]


def build_authority_frame(overlay_path: Path) -> pd.DataFrame:
    frame = pd.read_csv(overlay_path, low_memory=False)
    if frame.empty:
        return frame
    out = frame.copy()
    if overlay_path.name.lower() == "gss1972_directionality_overlay.csv":
        for row in EXTRA_ROWS_1972:
            if not out["var_name"].astype(str).str.strip().eq(row["var_name"]).any():
                out = pd.concat([out, pd.DataFrame([row])], ignore_index=True, sort=False)
    out["directionality_authority_status"] = "REVIEW_REQUIRED"
    out["directional_certification_status"] = "NOT_CERTIFIED"
    out["current_directional_atom_eligible"] = False
    out["manual_review_required"] = True
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed the directionality authority folder from the available GSS overlays.")
    parser.add_argument("--overlay-dir", type=Path, default=DEFAULT_OVERLAY_DIR)
    parser.add_argument("--authority-dir", type=Path, default=DEFAULT_AUTHORITY_DIR)
    args = parser.parse_args()

    authority_dir = args.authority_dir.resolve()
    authority_dir.mkdir(parents=True, exist_ok=True)

    overlay_dir = args.overlay_dir.resolve()
    overlay_paths = sorted(overlay_dir.glob("gss*_directionality_overlay.csv"))
    if not overlay_paths:
        raise FileNotFoundError(f"No directionality overlays found in {overlay_dir}")

    index_rows = []
    for overlay_path in overlay_paths:
        wave = overlay_path.stem.replace("gss", "").replace("_directionality_overlay", "")
        authority_path = authority_dir / f"gss{wave}_directionality_authority.csv"
        frame = build_authority_frame(overlay_path)
        frame.to_csv(authority_path, index=False)
        notes = "seeded from legacy directionality overlay"
        if wave == "1972":
            notes = "1972 seed authority: current overlay plus explicit unsigned nominal items."
        index_rows.append(
            {
                "source": "GSS",
                "wave": wave,
                "file_name": authority_path.name,
                "row_count": len(frame),
                "status": "review_only_not_certified",
                "notes": notes,
            }
        )
        print(f"Wrote {authority_path}")

    index_path = authority_dir / "directionality_authority_index.csv"
    index_frame = pd.DataFrame(index_rows)
    index_frame.to_csv(index_path, index=False)

    readme_path = authority_dir / "README.md"
    readme_path.write_text(
        "# Directionality Authority\n\n"
        "This folder contains GSS directionality review candidates.\n\n"
        "Presence is not certification. Generated rows remain `REVIEW_REQUIRED`/"
        "`NOT_CERTIFIED` until independently adjudicated.\n\n"
        "The V550 eligibility contract checks explicit authority status before use.\n",
        encoding="utf-8",
    )

    print(f"Wrote {index_path}")
    print(f"Wrote {readme_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
