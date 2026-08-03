from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Any

import pyreadstat

ROOT = Path(__file__).resolve().parents[2]
CODEBOOK_DIR = ROOT / "data" / "FINAL CODEBOOKS" / "FINAL FINAL CODEBOOKS"

DATASETS = [
    {
        "source_family": "Asian Barometer",
        "wave": "W5",
        "source_path": ROOT / "data" / "Data" / "W5 Merged Data" / "20230505_W5_merge_15.sav",
        "codebook_name": "Asian Barometer Wave 5 codebook.csv",
        "report_dir": ROOT / "data" / "Asian Barometer" / "wave5_reports",
    },
    {
        "source_family": "South Asia",
        "wave": "W1",
        "source_path": ROOT / "data" / "Data" / "SA_Wave1" / "SDSA 2005.sav",
        "codebook_name": "South Asia Wave 1 codebook.csv",
        "report_dir": ROOT / "data" / "South Asia" / "reports",
    },
    {
        "source_family": "South Asia",
        "wave": "W2",
        "source_path": ROOT / "data" / "Data" / "SA_Wave2" / "SDSA 2013.sav",
        "codebook_name": "South Asia Wave 2 codebook.csv",
        "report_dir": ROOT / "data" / "South Asia" / "reports",
    },
]

SPECIAL_MISSING_VALUES = {-5, -4, -3, -2, -1, 7, 8, 9, 97, 98, 99}


def decode(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, bytes):
        return v.decode("utf-8", "replace").strip()
    return str(v).strip()


def format_code(code: Any) -> str:
    if isinstance(code, float) and code.is_integer():
        return str(int(code))
    if isinstance(code, int):
        return str(code)
    try:
        f = float(code)
        if f.is_integer():
            return str(int(f))
    except Exception:
        pass
    return str(code)


def sorted_label_items(labels: dict[Any, Any]):
    def key(item: tuple[Any, Any]):
        code = item[0]
        try:
            return (0, float(code))
        except Exception:
            return (1, decode(code))

    return sorted(labels.items(), key=key)


def split_labels(labels: dict[Any, Any]) -> tuple[str, str, str]:
    substantive: list[str] = []
    special: list[str] = []
    all_opts: list[str] = []
    for code, label in sorted_label_items(labels):
        code_text = format_code(code)
        label_text = decode(label)
        entry = f"{code_text} = {label_text}" if label_text and label_text != code_text else code_text
        all_opts.append(entry)
        try:
            code_num = float(code)
        except Exception:
            code_num = None
        if code_num is not None and int(code_num) in SPECIAL_MISSING_VALUES:
            special.append(entry)
        else:
            substantive.append(entry)
    return " | ".join(substantive), " | ".join(special), " | ".join(all_opts)


def infer_type(var_types: dict[bytes, int], var_name: bytes) -> str:
    return "string" if var_types.get(var_name, 0) > 0 else "numeric"


def infer_note(var_name: str, storage_type: str) -> str:
    low = var_name.lower()
    if low in {
        "id",
        "idnumber",
        "resno",
        "ccode",
        "country",
        "country_code",
        "year",
        "month",
        "region",
        "level",
        "wt",
        "weight",
    }:
        return "administrative metadata"
    if low.startswith(("q", "gb", "gbc", "c", "b", "d", "z", "v", "se", "ir")):
        return "survey question"
    if low.startswith(("w", "i_")):
        return "constructed weight/index"
    if storage_type == "string":
        return "string variable"
    return ""


def write_codebook(dataset: dict[str, Any]) -> dict[str, Any]:
    path = dataset["source_path"]
    if not path.exists():
        return {
            "file": path.name,
            "status": "missing",
            "output": "",
            "rows": 0,
            "columns": 0,
        }
    df, meta = pyreadstat.read_sav(str(path), metadataonly=True)
    columns = list(getattr(meta, "column_names", []) or list(df.columns))
    columns = [decode(c) for c in columns]
    rows = []
    for raw_var in getattr(meta, "column_names", []) or list(df.columns):
        var_name = decode(raw_var)
        sav_label = decode(getattr(meta, "column_names_to_labels", {}).get(var_name, "") if hasattr(meta, "column_names_to_labels") else "")
        storage_type = infer_type(getattr(meta, "variable_types", {}), raw_var)
        measure = decode(getattr(meta, "variable_measure", {}).get(raw_var, "") if hasattr(meta, "variable_measure") else "")
        fmt = decode(getattr(meta, "original_variable_types", {}).get(raw_var, "") if hasattr(meta, "original_variable_types") else "")
        value_labels = getattr(meta, "variable_value_labels", {}).get(raw_var, {}) if hasattr(meta, "variable_value_labels") else {}
        substantive_opts, special_opts, all_opts = split_labels(value_labels or {})
        rows.append(
            {
                "var_name": var_name,
                "question_text": sav_label,
                "storage_type": storage_type,
                "measure": measure,
                "format": fmt,
                "value_labels_count": str(len(value_labels or {})),
                "substantive_value_labels": substantive_opts,
                "special_value_labels": special_opts,
                "all_value_labels": all_opts,
                "note": infer_note(var_name, storage_type),
            }
        )

    CODEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    out_path = CODEBOOK_DIR / dataset["codebook_name"]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "var_name",
                "question_text",
                "storage_type",
                "measure",
                "format",
                "value_labels_count",
                "substantive_value_labels",
                "special_value_labels",
                "all_value_labels",
                "note",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    report_dir = dataset["report_dir"]
    report_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "file": path.name,
        "status": "ok",
        "rows": len(rows),
        "columns": len(columns),
        "source_path": str(path),
        "codebook_path": str(out_path),
        "source_family": dataset["source_family"],
        "wave": dataset["wave"],
    }
    return summary


def main() -> int:
    summaries = [write_codebook(dataset) for dataset in DATASETS]

    by_report_dir: dict[Path, list[dict[str, Any]]] = {}
    for summary, dataset in zip(summaries, DATASETS):
        by_report_dir.setdefault(dataset["report_dir"], []).append(summary)

    for report_dir, rows in by_report_dir.items():
        report_dir.mkdir(parents=True, exist_ok=True)
        with (report_dir / "codebook_summary.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["file", "status"])
            writer.writeheader()
            writer.writerows(rows)

        if len(rows) > 1:
            with (report_dir / "structure_comparison.txt").open("w", encoding="utf-8") as f:
                f.write(f"files: {len(rows)}\n")
                for row in rows:
                    f.write(f"{row['file']}: rows={row['rows']} columns={row['columns']}\n")

    for summary in summaries:
        print(f"{summary['file']}: {summary['status']} -> {summary['codebook_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
