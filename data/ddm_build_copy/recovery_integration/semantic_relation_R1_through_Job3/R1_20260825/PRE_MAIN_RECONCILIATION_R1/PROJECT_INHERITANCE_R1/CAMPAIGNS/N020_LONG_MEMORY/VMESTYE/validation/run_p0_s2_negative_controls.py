#!/usr/bin/env python3
"""Run the eight deliberately broken P0 fixtures against the stage-aware validator."""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CONTROLS = [
    ("N01_SR01_MISSING_KEY", "A_SOURCE_KEYS:PYAT_SR01_2416"),
    ("N02_RM_ALIAS_CORRUPTION", "B_RM_SELECTOR:AJ-RM01"),
    ("N03_G4_PREDICATE_CORRUPTION", "D_G4_FIELD:ASTRA:IF:N0:N4:0:original_predicate"),
    ("N04_IF_TO_MUST", "D_G4_FIELD:ASTRA:IF:N1:N4:1:original_requiredness"),
    ("N05_D02_DANGLING_SOURCE", "C_D02_D07_SELECTOR:AJ-D02_SOURCE_PACKAGE__CURRENT_PROOF_REFS.csv"),
    ("N06_RM_NEGATIVE_LOSS", "B_RM_ANTI_JOIN:AJ-RM01"),
    ("N07_FORGED_ACCEPTANCE", "E_STAGE_ACCEPTANCE:ZL00"),
    ("N08_P1_SCHEMA_CORRUPTION", "F_P1_HEADER:OPERATION_TRACES.tsv"),
    ("N09_D05_RAW_HASH_TAMPER", "C_D05_QUALIFICATION_HASH:D05-F01"),
]


def read_rows(path: Path, delimiter: str = "\t") -> tuple[list[str], list[list[str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        raw = list(csv.reader(handle, delimiter=delimiter, strict=True))
    return raw[0], raw[1:]


def write_rows(path: Path, header: list[str], rows: list[list[str]], delimiter: str = "\t") -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter=delimiter, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def mutate(control: str, root: Path) -> None:
    if control == "N01_SR01_MISSING_KEY":
        path = root / "CONTROL/P0_RETURN_AND_BRANCH_CENSUS.tsv"
        header, rows = read_rows(path)
        removed = False
        kept = []
        for row in rows:
            if not removed and row[header.index("estate_id")] == "PYAT_SR01_2416":
                removed = True
                continue
            kept.append(row)
        write_rows(path, header, kept)
        return
    if control == "N02_RM_ALIAS_CORRUPTION":
        path = root / "CONTROL/P0_RM_CHECK_ID_BIJECTION_V1.tsv"
        header, rows = read_rows(path)
        rows[0][header.index("authoritative_census_estate_id")] = "RECENT_RM01"
        write_rows(path, header, rows)
        return
    if control in {"N03_G4_PREDICATE_CORRUPTION", "N04_IF_TO_MUST"}:
        path = root / "CONTROL/P0_PROG_SEAM82_PREDICATE_CONTRACT_V1.tsv"
        header, rows = read_rows(path)
        edge_index = header.index("edge_id")
        target = "ASTRA:IF:N0:N4:0" if control == "N03_G4_PREDICATE_CORRUPTION" else "ASTRA:IF:N1:N4:1"
        for row in rows:
            if row[edge_index] == target:
                if control == "N03_G4_PREDICATE_CORRUPTION":
                    row[header.index("original_predicate")] += " TAMPERED"
                else:
                    row[header.index("original_requiredness")] = "MUST"
                break
        write_rows(path, header, rows)
        return
    if control == "N05_D02_DANGLING_SOURCE":
        path = root / "CONTROL/P0_NO_DROP_ANTI_JOINS.tsv"
        header, rows = read_rows(path)
        check_index = header.index("check_id")
        source_index = header.index("source_ref")
        for row in rows:
            if row[check_index] == "AJ-D02_SOURCE_PACKAGE__CURRENT_PROOF_REFS.csv":
                row[source_index] = row[source_index].replace("CURRENT_PROOF_REFS.csv", "MISSING_SOURCE_FILE.csv")
                break
        write_rows(path, header, rows)
        return
    if control == "N06_RM_NEGATIVE_LOSS":
        path = root / "CONTROL/P0_NO_DROP_ANTI_JOINS.tsv"
        header, rows = read_rows(path)
        check_index = header.index("check_id")
        negative_index = header.index("negative_ids")
        for row in rows:
            if row[check_index] == "AJ-RM01":
                row[negative_index] = row[negative_index].replace("estate_id=RECENT_CAMPAIGN30", "estate_id=RECENT_RM01")
                break
        write_rows(path, header, rows)
        return
    if control == "N07_FORGED_ACCEPTANCE":
        path = root / "CONTROL/P0_S2_STAGE_MANIFEST.tsv"
        header, rows = read_rows(path)
        subject_index = header.index("subject_id")
        for row in rows:
            if row[subject_index] == "ZL00":
                row[header.index("stage")] = "ACCEPTED_TO_VMESTYE"
                break
        write_rows(path, header, rows)
        return
    if control == "N09_D05_RAW_HASH_TAMPER":
        path = root / "CONTROL/P0_D05_RAW_SOURCE_QUALIFICATION.tsv"
        header, rows = read_rows(path)
        target_index = header.index("source_exact_id")
        hash_index = header.index("raw_physical_line_sha256")
        for row in rows:
            if row[target_index] == "D05-F01":
                row[hash_index] = "sha256:" + "0" * 64
                break
        write_rows(path, header, rows)
        return
    if control == "N08_P1_SCHEMA_CORRUPTION":
        path = root / "CONTROL/P0_SCHEMA_AND_LEASES.md"
        text = path.read_text(encoding="utf-8")
        header = "\t".join([
            "prong_id", "trace_id", "finding_id", "census_id", "estate_id",
            "source_commit_sha", "source_path", "source_composite_id", "source_grain",
            "input_source_ref", "input_semantics", "selected_rule_ref",
            "transformation_human_language", "output_object", "producer_edge_id",
            "first_consumer_id", "first_consumer_evidence_id", "negative_or_refusal",
            "execution_status", "proof_grade", "missing_next_edge",
        ])
        if header not in text:
            raise RuntimeError("cannot find frozen OPERATION_TRACES header")
        text = text.replace(header, header.replace("prong_id", "prong", 1), 1)
        path.write_text(text, encoding="utf-8")
        return
    raise KeyError(control)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assembly", type=Path, required=True)
    parser.add_argument("--git-repo", type=Path, required=True)
    parser.add_argument("--validator", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    rows = []
    for control, expected in CONTROLS:
        with tempfile.TemporaryDirectory(prefix=f"{control}-", dir=args.out) as tmp:
            root = Path(tmp) / "VMESTYE"
            shutil.copytree(args.assembly, root)
            mutate(control, root)
            command = [
                sys.executable,
                str(args.validator),
                "--root", str(root),
                "--git-repo", str(args.git_repo),
            ]
            proc = subprocess.run(command, capture_output=True, text=True)
            output = proc.stdout + proc.stderr
            (args.out / f"{control}.log").write_text(output, encoding="utf-8")
            actual_error_ids = sorted({
                line.split(maxsplit=2)[1]
                for line in proc.stderr.splitlines()
                if line.startswith("ERROR ") and len(line.split(maxsplit=2)) >= 2
            })
            passed = proc.returncode != 0 and expected in actual_error_ids
            rows.append({
                "control_id": control,
                "mutation": control,
                "expected_error_id": expected,
                "exit_code": str(proc.returncode),
                "actual_error_ids": ",".join(actual_error_ids),
                "status": "PASS" if passed else "FAIL",
                "log_path": f"{control}.log",
            })
            (args.out / f"{control}.json").write_text(
                json.dumps({"expected": expected, "actual_error_ids": actual_error_ids,
                            "exit_code": proc.returncode, "status": rows[-1]["status"],
                            "output": output}, indent=2) + "\n",
                encoding="utf-8",
            )
    with (args.out / "P0_S2_NEGATIVE_CONTROLS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(f"{row['status']}\t{row['control_id']}\t{row['expected_error_id']}\t{row['actual_error_ids']}")
    return 0 if all(row["status"] == "PASS" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
