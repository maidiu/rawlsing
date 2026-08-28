#!/usr/bin/env python3
"""Exact lower-level replay verifier for the historical 18,792-row QSR.

This verifier never treats the reference QSR as a producer. It verifies an
exact dependency manifest, stages only the declared canonical audit producers,
runs the exact historical builder in a fresh tree, and opens the reference
carrier only after generation for parity comparison.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Mapping

import pandas as pd

CONTRACT_ID = "QSR_LOWER_LEVEL_REPLAY@1.0.0"


class QSRReplayError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise QSRReplayError(f"missing producer: {label}: {path}")


def _verify_hash(path: Path, expected: str, label: str) -> None:
    _require_file(path, label)
    observed = sha256_file(path)
    if observed != expected:
        raise QSRReplayError(
            f"producer hash mismatch: {label}: expected={expected} observed={observed} path={path}"
        )


def _load_spec(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("contract") != "QSR_LOWER_LEVEL_REPLAY_DEPENDENCIES@1.0.0":
        raise QSRReplayError("unsupported dependency manifest contract")
    audits = data.get("audit_producers")
    if not isinstance(audits, list) or len(audits) != data.get("expected_scope_count"):
        raise QSRReplayError("audit producer census is incomplete")
    dataset_ids = [str(x.get("dataset_id") or "") for x in audits]
    if len(dataset_ids) != len(set(dataset_ids)) or any(not x for x in dataset_ids):
        raise QSRReplayError("audit producer dataset identities must be complete and unique")
    if any("asian_barometer_wave_6" in x.lower() for x in dataset_ids):
        raise QSRReplayError("Asian Barometer W6 is excluded from CLOSED_35")
    return data


def _canonical_manifest_rows(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, dtype=str, keep_default_na=False, low_memory=False)
    if "canonical_intended" not in frame.columns or "dataset_id" not in frame.columns:
        raise QSRReplayError("validation manifest lacks canonical scope identity")
    mask = frame["canonical_intended"].str.strip().str.lower().isin({"1", "true", "yes", "y"})
    return frame.loc[mask].copy()


def _rewrite_transport_manifest(source: Path, target: Path, audit_stage: Path) -> dict[str, Any]:
    original = pd.read_csv(source, dtype=str, keep_default_na=False, low_memory=False)
    replay = original.copy()
    changes = []
    for idx, row in replay.iterrows():
        for col in ("audit_csv", "audit_yaml"):
            value = str(row.get(col) or "")
            if not value:
                continue
            basename = Path(value).name
            replay.at[idx, col] = str(Path("data") / "ddm_build_copy" / "reports" / "source_structure_audits" / basename)
            changes.append({"row": int(idx), "column": col, "basename": basename})
    for col in original.columns:
        if col not in {"audit_csv", "audit_yaml"} and original[col].tolist() != replay[col].tolist():
            raise QSRReplayError(f"transport rewrite altered semantic manifest column {col}")
    target.parent.mkdir(parents=True, exist_ok=True)
    replay.to_csv(target, index=False)
    return {
        "source_manifest_sha256": sha256_file(source),
        "replay_transport_manifest_sha256": sha256_file(target),
        "path_rewrite_count": len(changes),
        "non_path_cells_identical": True,
    }


def _row_identity_root(frame: pd.DataFrame) -> tuple[str, int]:
    hashes = []
    for ordinal, (_, row) in enumerate(frame.iterrows(), start=1):
        payload = json.dumps(row.to_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        hashes.append(f"{ordinal}:{hashlib.sha256(payload.encode('utf-8')).hexdigest()}")
    root = hashlib.sha256((("\n".join(hashes) + "\n") if hashes else "").encode("utf-8")).hexdigest()
    return root, len(set(x.split(":", 1)[1] for x in hashes))


def compare_qsr(generated: Path, reference: Path, expected: Mapping[str, Any]) -> dict[str, Any]:
    # Called only after the fresh builder finishes.
    _require_file(generated, "generated_qsr")
    _require_file(reference, "reference_qsr")
    gsha = sha256_file(generated)
    rsha = sha256_file(reference)
    g = pd.read_csv(generated, dtype=str, keep_default_na=False, low_memory=False)
    r = pd.read_csv(reference, dtype=str, keep_default_na=False, low_memory=False)
    columns_equal = list(g.columns) == list(r.columns)
    shape_equal = g.shape == r.shape
    if columns_equal and shape_equal:
        neq = g.ne(r)
        diff_cells = int(neq.to_numpy().sum())
        diff_rows = int(neq.any(axis=1).sum())
    else:
        diff_cells = -1
        diff_rows = -1
    root, unique_row_hashes = _row_identity_root(g)
    result = {
        "generated_sha256": gsha,
        "reference_sha256": rsha,
        "raw_bytes_equal": generated.read_bytes() == reference.read_bytes(),
        "generated_rows": int(g.shape[0]),
        "generated_columns": int(g.shape[1]),
        "reference_rows": int(r.shape[0]),
        "reference_columns": int(r.shape[1]),
        "columns_equal": columns_equal,
        "shape_equal": shape_equal,
        "differing_rows": diff_rows,
        "differing_cells": diff_cells,
        "ordered_row_identity_root": root,
        "unique_row_content_hashes": unique_row_hashes,
        "manual_review_yes_count": int((g.get("needs_manual_review", pd.Series(dtype=str)).str.lower() == "yes").sum()),
        "source_structure_review_required_count": int((g.get("source_structure_review_required", pd.Series(dtype=str)).str.lower() == "true").sum()),
        "unknown_classification_count": int((g.get("source_structure_classification", pd.Series(dtype=str)) == "unknown").sum()),
    }
    checks = {
        "rows": result["generated_rows"] == int(expected["rows"]),
        "columns": result["generated_columns"] == int(expected["columns"]),
        "expected_sha": gsha == expected["sha256"],
        "reference_sha": rsha == expected["sha256"],
        "row_identity_root": root == expected["ordered_row_identity_root"],
        "raw_parity": result["raw_bytes_equal"],
        "row_cell_parity": columns_equal and shape_equal and diff_rows == 0 and diff_cells == 0,
        "manual_review": result["manual_review_yes_count"] == int(expected["manual_review_yes_count"]),
        "source_structure_review": result["source_structure_review_required_count"] == int(expected["source_structure_review_required_count"]),
        "unknown_classification": result["unknown_classification_count"] == int(expected["unknown_classification_count"]),
    }
    result["checks"] = checks
    result["pass"] = all(checks.values())
    return result


def replay_qsr(
    *, dependency_manifest: Path, builder: Path, source_structure_rule: Path,
    survey_identity_helper: Path, validation_manifest: Path, taxonomy: Path,
    semantic_driver_master: Path, audit_root: Path, reference_qsr: Path,
    workdir: Path | None = None,
) -> dict[str, Any]:
    spec = _load_spec(dependency_manifest)
    core = spec["core_producers"]
    exacts = [
        (builder, core["builder"]["sha256"], "builder"),
        (source_structure_rule, core["source_structure_rule"]["sha256"], "source_structure_rule"),
        (survey_identity_helper, core["survey_identity_helper"]["sha256"], "survey_identity_helper"),
        (validation_manifest, core["validation_manifest"]["sha256"], "validation_manifest"),
        (taxonomy, core["question_type_taxonomy"]["sha256"], "question_type_taxonomy"),
        (semantic_driver_master, core["semantic_driver_master"]["sha256"], "semantic_driver_master"),
    ]
    for path, expected, label in exacts:
        _verify_hash(path, expected, label)

    canonical = _canonical_manifest_rows(validation_manifest)
    expected_ids = {x["dataset_id"] for x in spec["audit_producers"]}
    canonical_ids = set(canonical["dataset_id"].tolist())
    if canonical_ids != expected_ids:
        raise QSRReplayError(
            f"CLOSED_35 manifest census mismatch: missing={sorted(expected_ids-canonical_ids)} extra={sorted(canonical_ids-expected_ids)}"
        )

    producer_paths: dict[str, Path] = {}
    for item in spec["audit_producers"]:
        source = audit_root / item["recovered_audit_basename"]
        _verify_hash(source, item["audit_sha256"], f"audit:{item['dataset_id']}")
        producer_paths[item["dataset_id"]] = source

    if workdir is None:
        td = tempfile.TemporaryDirectory(prefix="qsr_replay_")
        root = Path(td.name)
    else:
        td = None
        root = workdir
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)

    try:
        ddm = root / "data" / "ddm_build_copy"
        manifests = ddm / "manifests"
        audits = ddm / "reports" / "source_structure_audits"
        final_codebooks = root / "data" / "final_codebooks"
        manifests.mkdir(parents=True, exist_ok=True)
        audits.mkdir(parents=True, exist_ok=True)
        final_codebooks.mkdir(parents=True, exist_ok=True)
        (root / "data" / "__init__.py").write_text("", encoding="utf-8")
        (ddm / "__init__.py").write_text("", encoding="utf-8")
        shutil.copy2(builder, ddm / "build_question_structure_register.py")
        shutil.copy2(source_structure_rule, ddm / "ddm_v550_source_structure.py")
        shutil.copy2(survey_identity_helper, ddm / "ddm_survey_identity.py")
        shutil.copy2(taxonomy, manifests / "question_type_taxonomy.yaml")
        shutil.copy2(semantic_driver_master, final_codebooks / "questions_master_drivers.csv")

        by_id = {x["dataset_id"]: x for x in spec["audit_producers"]}
        for _, row in canonical.iterrows():
            item = by_id[row["dataset_id"]]
            shutil.copy2(producer_paths[row["dataset_id"]], audits / item["manifest_audit_basename"])

        transport = _rewrite_transport_manifest(
            validation_manifest, manifests / "source_structure_validation_manifest.csv", audits
        )
        generated = manifests / "question_structure_register.csv"
        if generated.exists():
            raise QSRReplayError("fresh replay tree unexpectedly contains a QSR before execution")
        env = dict(os.environ)
        env["PYTHONPATH"] = str(root)
        proc = subprocess.run(
            [sys.executable, str(ddm / "build_question_structure_register.py")],
            cwd=root, env=env, text=True, capture_output=True,
        )
        if proc.returncode != 0:
            raise QSRReplayError(
                f"QSR builder failed rc={proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}"
            )
        if not generated.is_file():
            raise QSRReplayError("builder returned success without generated QSR")

        parity = compare_qsr(generated, reference_qsr, spec["expected_output"])
        receipt = {
            "contract": CONTRACT_ID,
            "status": "PASS" if parity["pass"] else "FAIL",
            "dependency_manifest_sha256": sha256_file(dependency_manifest),
            "producer_census": {
                "core_producer_count": len(exacts),
                "audit_producer_count": len(spec["audit_producers"]),
                "audit_row_count": sum(int(x["audit_row_count"]) for x in spec["audit_producers"]),
                "scope": spec["scope"],
            },
            "transport_manifest": transport,
            "builder": {
                "returncode": proc.returncode,
                "stdout": proc.stdout.replace(str(root), "<REPLAY_ROOT>"),
                "stderr": proc.stderr.replace(str(root), "<REPLAY_ROOT>"),
            },
            "parity": parity,
            "negative_ceiling": spec["negative_ceiling"],
        }
        if not parity["pass"]:
            raise QSRReplayError("fresh QSR does not match expected/reference carrier: " + json.dumps(parity, sort_keys=True))
        return receipt
    finally:
        if td is not None:
            td.cleanup()


def _main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dependency-manifest", type=Path, required=True)
    ap.add_argument("--builder", type=Path, required=True)
    ap.add_argument("--source-structure-rule", type=Path, required=True)
    ap.add_argument("--survey-identity-helper", type=Path, required=True)
    ap.add_argument("--validation-manifest", type=Path, required=True)
    ap.add_argument("--taxonomy", type=Path, required=True)
    ap.add_argument("--semantic-driver-master", type=Path, required=True)
    ap.add_argument("--audit-root", type=Path, required=True)
    ap.add_argument("--reference-qsr", type=Path, required=True)
    ap.add_argument("--workdir", type=Path)
    ap.add_argument("--receipt", type=Path, required=True)
    ns = ap.parse_args()
    receipt = replay_qsr(
        dependency_manifest=ns.dependency_manifest,
        builder=ns.builder,
        source_structure_rule=ns.source_structure_rule,
        survey_identity_helper=ns.survey_identity_helper,
        validation_manifest=ns.validation_manifest,
        taxonomy=ns.taxonomy,
        semantic_driver_master=ns.semantic_driver_master,
        audit_root=ns.audit_root,
        reference_qsr=ns.reference_qsr,
        workdir=ns.workdir,
    )
    ns.receipt.parent.mkdir(parents=True, exist_ok=True)
    ns.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "receipt": str(ns.receipt)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
