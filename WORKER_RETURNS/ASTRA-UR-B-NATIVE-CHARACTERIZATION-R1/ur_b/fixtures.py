"""Generate the frozen S1/S2/S3 TEST_ONLY native fixtures."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pyreadstat


def write_s1(path: Path) -> None:
    rows = []
    for i in range(16):
        a = i % 2
        b = (i // 2) % 2
        rows.append({
            "A": float(a),
            "B": float(b),
            "Y": float(a ^ b),
            "G": float((i // 4) % 2),
            "WEIGHT": float(1 + i // 8),
            "Z": float("nan"),
        })
    df = pd.DataFrame(rows, columns=("A", "B", "Y", "G", "WEIGHT", "Z"))
    pyreadstat.write_sav(
        df, str(path),
        column_labels=["A condition", "B condition", "Y outcome",
                       "G coordinate", "Synthetic weight", "All-missing Z"],
    )


def write_s2_person(path: Path) -> None:
    rows = []
    for h in range(8):
        for p in range(2):
            rows.append({
                "HID": float(h),
                "PID": float(p),
                "OUTCOME": float((h + p) % 3),
                "HMEAS": float(h % 2),
                "PWEIGHT": float(h + 1),
                "PITEM": float((h + 1) % 3) if p == 1 else None,
                "PITEM_B": float((h + 2) % 3) if p == 1 else None,
            })
    df = pd.DataFrame(rows, columns=("HID", "PID", "OUTCOME", "HMEAS",
                                     "PWEIGHT", "PITEM", "PITEM_B"))
    pyreadstat.write_dta(
        df, str(path),
        column_labels=["household id", "person id", "person outcome",
                       "household measurement", "person weight",
                       "Person item form A", "Person item form B"],
    )


def write_s2_household(path: Path) -> None:
    rows = [{"HID": float(h), "HMEAS": float(h % 2)} for h in range(8)]
    df = pd.DataFrame(rows, columns=("HID", "HMEAS"))
    pyreadstat.write_dta(
        df, str(path),
        column_labels=["household id", "household measurement"],
    )


def write_s3(path: Path) -> None:
    rows = []
    for r in range(12):
        for t in range(2):
            rows.append({
                "PID": float(r),
                "OCCASION": float(t),
                "SCORE": float((r + t) % 3),
                "MR1": float(r % 2) if t == 0 else None,
                "MR2": float((r // 2) % 2) if t == 1 else None,
                "RANK1": float(r % 3) if t == 0 else None,
                "RANK2": float((r + 1) % 3) if t == 1 else None,
                "FORM": float(r % 2),
            })
    df = pd.DataFrame(rows, columns=("PID", "OCCASION", "SCORE", "MR1",
                                     "MR2", "RANK1", "RANK2", "FORM"))
    pyreadstat.write_sav(
        df, str(path),
        column_labels=["person id", "occasion", "score",
                       "multi-response option A", "multi-response option B",
                       "rank option A", "rank option B", "form"],
    )


def generate(directory) -> dict[str, Path]:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    paths = {
        "S1": directory / "ur_b_s1_xor.sav",
        "S2_person": directory / "ur_b_s2_person.dta",
        "S2_household": directory / "ur_b_s2_household.dta",
        "S3": directory / "ur_b_s3_repeated.sav",
    }
    write_s1(paths["S1"])
    write_s2_person(paths["S2_person"])
    write_s2_household(paths["S2_household"])
    write_s3(paths["S3"])
    return paths
