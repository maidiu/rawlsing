#!/usr/bin/env python3
"""Independent focused verification of the C10 Q3 F03 replay.

Reads the exact historical module/authority bytes from the pinned Git cut
9ba4764 into this review lease's tmp directory, then exercises the actual
historical entrypoints used by C10. It does not read respondents, SAV/DTA/DB,
production modules, or current engines. It writes only this review lease.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pandas as pd

REPO = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer")
LEASE = Path(
    "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-c6-historical-independent-review/"
    "WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/"
    "C10_Q3_F03_INDEPENDENT_REVIEW"
)
AUTHOR = Path(
    "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-joint-consumer/"
    "WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/"
    "C10_Q3_F03_FIRST_CONSUMER_EFFECT"
)
TMP = LEASE / "tmp" / "verify_replay_root"
RESTORE = LEASE / "tmp" / "verify_restore_root"

HIST = "9ba4764bef551b1ce498e5772d60b73d69337d4b"
AUTHOR_CUT = "0d548b033a0a20c9738fa4a3412ba5acd01217c5"

MODULE_PATH = "data/ddm_build_copy/ddm_v550_question_relation_authority.py"
FULL_PATH = (
    "data/ddm_build_copy/authority/full_question_relation_authority/"
    "R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv"
)
REG_PATH = "data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv"

EXPECT = {
    MODULE_PATH: "2fb0851d8bac6f3d381fdf11749f7e04e676de914d643e5be1ad4603cc39f63c",
    FULL_PATH: "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13",
    REG_PATH: "a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b",
}
EXPECT_BYTES = {
    MODULE_PATH: 38858,
    FULL_PATH: 47874248,
    REG_PATH: 1119028,
}
EXPECT_ROWS = {FULL_PATH: 18518, REG_PATH: 700}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_hash(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode()
    ).hexdigest()


def git_bytes(path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(REPO), "show", f"{HIST}:{path}"],
        check=True, stdout=subprocess.PIPE,
    ).stdout


def materialize(git_path: str, dest: Path) -> None:
    data = git_bytes(git_path)
    actual = sha256_bytes(data)
    if actual != EXPECT[git_path]:
        raise SystemExit(f"pin mismatch {git_path}: {actual}")
    if len(data) != EXPECT_BYTES[git_path]:
        raise SystemExit(f"byte mismatch {git_path}: {len(data)}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    if sha256_file(dest) != EXPECT[git_path]:
        raise SystemExit(f"materialized hash mismatch {dest}")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def bridge_from_audit_row(row: pd.Series) -> dict[str, str]:
    return {
        "source_family": str(row["source_family"]),
        "canonical_wave": str(row["canonical_wave"]),
        "country_code": str(row["input_country_code"]),
        "question_id": str(row["question_id"]),
        "var_code": str(row["var_code"]),
    }


def selected_row(row: pd.Series) -> dict[str, str]:
    return {
        "source_family": str(row["source_family"]),
        "canonical_wave": str(row["canonical_wave"]),
        "country_code": str(row["input_country_code"]),
        "question_id": str(row["question_id"]),
        "var_code": str(row["var_code"]),
        "authority_rule_id": str(row["authority_rule_id"]),
        "authority_row_payload_hash": str(row["authority_row_payload_hash"]),
        "resolver_status": str(row["resolver_status"]),
        "relation_use_status": str(row["relation_use_status"]),
    }


def main() -> int:
    if TMP.exists():
        shutil.rmtree(TMP)
    if RESTORE.exists():
        shutil.rmtree(RESTORE)
    TMP.mkdir(parents=True, exist_ok=True)
    RESTORE.mkdir(parents=True, exist_ok=True)

    module_path = TMP / MODULE_PATH
    full_path = TMP / FULL_PATH
    reg_path = TMP / REG_PATH
    for git_path, dest in ((MODULE_PATH, module_path), (FULL_PATH, full_path), (REG_PATH, reg_path)):
        materialize(git_path, dest)

    mod = load_module(module_path, "c10_review_qra")
    checks: dict[str, Any] = {}

    checks["module_root_matches_replay_root"] = mod.ROOT.resolve() == TMP.resolve()
    checks["module_sha256"] = sha256_file(module_path)
    checks["full_authority_sha256"] = sha256_file(full_path)
    checks["registry_sha256"] = sha256_file(reg_path)
    checks["full_authority_bytes"] = full_path.stat().st_size
    checks["registry_bytes"] = reg_path.stat().st_size

    index = mod.load_question_relation_authority()
    checks["index_rows"] = len(index.rows)
    checks["index_keys"] = len(index.by_key)
    checks["index_file_sha256"] = index.file_sha256

    closed35 = mod.active_closed_35_waves()
    checks["closed35_count"] = len(closed35)
    checks["closed35_excludes_w6"] = ("Asian Barometer", "W6", "") not in closed35
    checks["closed35_first_last"] = [list(closed35[0]), list(closed35[-1])]

    full_frame = pd.read_csv(full_path, dtype=str, keep_default_na=False)
    checks["full_frame_rows"] = len(full_frame)
    audit = mod.validate_active_universe(full_frame)
    checks["audit_rows"] = len(audit)
    status_counts = {str(k): int(v) for k, v in audit["resolver_status"].value_counts().items()}
    relation_counts = {str(k): int(v) for k, v in audit["relation_use_status"].value_counts().items()}
    checks["resolver_status_counts"] = status_counts
    checks["relation_use_status_counts"] = relation_counts
    checks["status_sum"] = sum(status_counts.values())
    checks["relation_sum"] = sum(relation_counts.values())
    checks["directional_coordinates_complete"] = int(audit["directional_coordinates_complete"].sum())
    checks["current_directional_atom_eligible"] = int(audit["current_directional_atom_eligible"].sum())

    sw = (
        audit.groupby(["source_family", "canonical_wave"], dropna=False)
        .size().reset_index(name="rows")
    )
    pairs = [(str(r.source_family), str(r.canonical_wave), int(r.rows)) for r in sw.itertuples(index=False)]
    active = [p for p in pairs if not (p[0] == "Asian Barometer" and p[1] == "W6")]
    checks["source_wave_pair_count_including_w6"] = len(pairs)
    checks["active_source_wave_count"] = len(active)
    checks["w6_rows"] = sum(p[2] for p in pairs if p[0] == "Asian Barometer" and p[1] == "W6")
    checks["active_rows"] = sum(p[2] for p in active)
    checks["full_audit_digest"] = canonical_hash(
        {"status": status_counts, "relation": relation_counts, "active_source_waves": active}
    )

    # Nine positive family witnesses, reproducing the C10 selection law.
    candidates = audit[
        (audit["resolver_status"] == "RESOLVED_DIRECTIONAL_AUTHORITY")
        & (audit["directional_coordinates_complete"])
        & (audit["current_directional_atom_eligible"])
    ]
    positives = []
    for source in candidates["source_family"].drop_duplicates().tolist():
        row = candidates[candidates["source_family"] == source].iloc[0]
        bridge = bridge_from_audit_row(row)
        out = mod.apply_question_relation_authority(bridge)
        positives.append({
            "source_family": source,
            "selected_row": selected_row(row),
            "bridge_input": bridge,
            "resolver_status": out.get("question_relation_authority_resolution_status"),
            "relation_use_status": out.get("relation_use_status"),
            "semantic_role": out.get("semantic_role"),
            "current_directional_atom_eligible": bool(out.get("current_directional_atom_eligible")),
            "question_relation_coverage_eligible": bool(out.get("question_relation_coverage_eligible")),
            "authority_artifact_sha256": out.get("authority_artifact_sha256"),
            "structural_coordinate_count": sum(
                1 for key in (
                    "driver_id", "driver_facet_id", "question_block_id",
                    "structural_domain_id", "relation_axis_id", "target_entity_id",
                ) if str(out.get(key, "")) != ""
            ),
            "output_hash": canonical_hash(out),
        })
    checks["positive_family_count"] = len(positives)
    checks["positive_families"] = [p["source_family"] for p in positives]

    first = positives[0]
    first_bridge = first["bridge_input"]

    # Actual explicit block.
    block_row = audit[audit["resolver_status"] == "RESOLVED_EXPLICIT_BLOCK"].iloc[0]
    block_out = mod.apply_question_relation_authority(bridge_from_audit_row(block_row))
    block = {
        "selected_row": selected_row(block_row),
        "resolver_status": block_out.get("question_relation_authority_resolution_status"),
        "semantic_role": block_out.get("semantic_role"),
        "structural_coordinates_cleared": all(
            str(block_out.get(k, "")) == ""
            for k in ("driver_id", "driver_facet_id", "question_block_id",
                      "structural_domain_id", "relation_axis_id", "target_entity_id")
        ),
        "current_directional_atom_eligible": bool(block_out.get("current_directional_atom_eligible")),
        "question_relation_coverage_eligible": bool(block_out.get("question_relation_coverage_eligible")),
        "output_hash": canonical_hash(block_out),
    }
    checks["explicit_block"] = block

    # Actual ambiguous row.
    amb_rows = audit[audit["resolver_status"] == "BLOCKED_AMBIGUOUS_AUTHORITY"]
    amb = None
    if not amb_rows.empty:
        amb_row = amb_rows.iloc[0]
        amb_out = mod.apply_question_relation_authority(bridge_from_audit_row(amb_row))
        amb = {
            "selected_row": selected_row(amb_row),
            "resolver_status": amb_out.get("question_relation_authority_resolution_status"),
            "semantic_role": amb_out.get("semantic_role"),
            "current_directional_atom_eligible": bool(amb_out.get("current_directional_atom_eligible")),
            "output_hash": canonical_hash(amb_out),
        }
    checks["ambiguous"] = amb

    # Suffix-derived missing-row negative fixture only.
    missing_bridge = dict(first_bridge)
    missing_bridge["var_code"] = "__C10_MISSING__" + str(first_bridge["var_code"])
    missing_bridge["question_id"] = "__C10_MISSING__" + str(first_bridge["question_id"])
    missing_out = mod.apply_question_relation_authority(missing_bridge)
    checks["missing_row"] = {
        "bridge_input": missing_bridge,
        "resolver_status": missing_out.get("question_relation_authority_resolution_status"),
        "semantic_role": missing_out.get("semantic_role"),
        "structural_coordinates_cleared": all(
            str(missing_out.get(k, "")) == ""
            for k in ("driver_id", "driver_facet_id", "question_block_id",
                      "structural_domain_id", "relation_axis_id", "target_entity_id")
        ),
        "current_directional_atom_eligible": bool(missing_out.get("current_directional_atom_eligible")),
        "question_relation_coverage_eligible": bool(missing_out.get("question_relation_coverage_eligible")),
        "output_hash": canonical_hash(missing_out),
    }

    # Limited/wrong authority: the AR-0006 700-row registry supplied for the
    # first full-AR-0005 positive row.
    wrong_out = mod.apply_question_relation_authority(first_bridge, authority_path=reg_path)
    checks["limited_registry"] = {
        "wrong_authority_sha256": sha256_file(reg_path),
        "resolver_status": wrong_out.get("question_relation_authority_resolution_status"),
        "semantic_role": wrong_out.get("semantic_role"),
        "current_directional_atom_eligible": bool(wrong_out.get("current_directional_atom_eligible")),
        "authority_artifact_sha256": wrong_out.get("authority_artifact_sha256"),
        "output_hash": canonical_hash(wrong_out),
    }

    # Missing authority file.
    missing_file = LEASE / "tmp" / "missing_authority.csv"
    try:
        mod.apply_question_relation_authority(first_bridge, authority_path=missing_file)
        checks["missing_file"] = {"status": "NO_ERROR"}
    except Exception as exc:  # noqa: BLE001 - exact exception type is the evidence
        checks["missing_file"] = {"status": "EXCEPTION", "type": type(exc).__name__, "message": str(exc)}

    # Cold restore to a second disposable root with identical bytes.
    restore_module_path = RESTORE / MODULE_PATH
    restore_full_path = RESTORE / FULL_PATH
    restore_reg_path = RESTORE / REG_PATH
    for src, dest in ((module_path, restore_module_path), (full_path, restore_full_path), (reg_path, restore_reg_path)):
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
    restore_mod = load_module(restore_module_path, "c10_review_restore_qra")
    restore_out = restore_mod.apply_question_relation_authority(first_bridge)
    checks["cold_restore"] = {
        "restore_root_matches": restore_mod.ROOT.resolve() == RESTORE.resolve(),
        "authority_copy_sha256": sha256_file(restore_full_path),
        "module_copy_sha256": sha256_file(restore_module_path),
        "output_hash": canonical_hash(restore_out),
        "matches_first_positive": canonical_hash(restore_out) == first["output_hash"],
    }

    # AR-0006 residual consumer: 20-row Latinobarometro 1995 slice.
    residual = mod.derive_legacy_latinobarometro_1995_residual(full_frame)
    residual_csv = residual.to_csv(index=False)
    checks["residual_ar0006"] = {
        "rows": len(residual),
        "source_families": sorted({str(x) for x in residual["source_family"].tolist()}),
        "canonical_waves": sorted({str(x) for x in residual["canonical_wave"].tolist()}),
        "csv_sha256": sha256_bytes(residual_csv.encode()),
        "registry_index_rows": len(mod.load_question_relation_authority(reg_path).rows),
        "registry_index_sha256": mod.load_question_relation_authority(reg_path).file_sha256,
    }

    # Compare to the author's results.
    author = json.loads((AUTHOR / "logs/replay_results.json").read_text())
    apos = {x["source_family"]: x for x in author["positive_rows"]}
    pos_compare = []
    for p in positives:
        a = apos.get(p["source_family"])
        pos_compare.append({
            "source_family": p["source_family"],
            "selected_row_match": bool(a) and p["selected_row"] == a["selected_row"],
            "output_hash_match": bool(a) and p["output_hash"] == a["output_hash"],
            "resolver_match": bool(a) and p["resolver_status"] == a["resolver_status"],
            "semantic_role_match": bool(a) and p["semantic_role"] == a["semantic_role"],
            "structural_coordinate_count": p["structural_coordinate_count"],
        })
    checks["positive_compare"] = pos_compare
    checks["full_audit_matches_author"] = {
        "resolver_counts": status_counts == author["full_audit"]["resolver_status_counts"],
        "relation_counts": relation_counts == author["full_audit"]["relation_use_status_counts"],
        "active_closed_35": len(closed35) == author["full_audit"]["active_closed_35_count"],
        "active_source_wave_count": len(active) == author["full_audit"]["active_source_wave_count"],
        "full_audit_digest": checks["full_audit_digest"] == author["full_audit"]["full_audit_digest"],
        "directional_coordinates_complete": int(audit["directional_coordinates_complete"].sum())
        == author["full_audit"]["directional_coordinates_complete"],
        "current_directional_atom_eligible": int(audit["current_directional_atom_eligible"].sum())
        == author["full_audit"]["current_directional_atom_eligible"],
    }
    checks["negative_matches_author"] = {
        "explicit_block": block["resolver_status"] == author["negative"]["explicit_block"]["resolver_status"]
        and block["output_hash"] == author["negative"]["explicit_block"]["output_hash"],
        "ambiguous": bool(amb) and amb["resolver_status"] == author["negative"]["ambiguous"]["resolver_status"]
        and amb["output_hash"] == author["negative"]["ambiguous"]["output_hash"],
        "missing": checks["missing_row"]["resolver_status"] == author["negative"]["missing"]["resolver_status"]
        and checks["missing_row"]["output_hash"] == author["negative"]["missing"]["output_hash"],
        "limited": checks["limited_registry"]["resolver_status"] == author["negative"]["wrong_or_limited"]["resolver_status"]
        and checks["limited_registry"]["output_hash"] == author["negative"]["wrong_or_limited"]["output_hash"],
        "missing_file": checks["missing_file"]["type"] == author["negative"]["missing_file"]["type"],
    }
    checks["residual_matches_author"] = {
        "rows": checks["residual_ar0006"]["rows"] == author["residual_ar0006"]["rows"],
        "csv_sha256": checks["residual_ar0006"]["csv_sha256"] == author["residual_ar0006"]["csv_sha256"],
        "registry_rows": checks["residual_ar0006"]["registry_index_rows"] == author["residual_ar0006"]["registry_rows"],
    }

    # Author script inspection: no substantive reader monkeypatch / no downstream calls.
    script_text = (AUTHOR / "scripts/replay_f03.py").read_text()
    checks["replay_script_scan"] = {
        "contains_mock_or_monkeypatch_token": any(t in script_text for t in ("monkeypatch", "unittest.mock", "MagicMock")),
        "contains_setattr": "setattr(" in script_text,
        "imports_ddm_v550_bridge": "ddm_v550_bridge" in script_text.split("def main")[0],
        "imports_compile_v551_relation_evidence_atoms": "compile_v551_relation_evidence_atoms" in script_text.split("def main")[0],
        "mentions_downstream_only_in_boundary": "V550 bridge/compile_v551_relation_evidence_atoms downstream not run" in script_text,
        "module_loaded_by_exact_path": "spec_from_file_location" in script_text,
        "authority_path_is_public_keyword": "authority_path" in script_text,
    }

    # Q4 current pins at the author cut, verified from git (not filename-only).
    q4_paths = {
        "generic_projection": "rawlsing_next/pre553_source_backed_c11_facade.py",
        "generic_query": "rawlsing_next/pre553_empirical_query.py",
        "generic_authority_validation": "rawlsing_next/pre553_empirical_authority.py",
        "bounded_fqra_materializer": "rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py",
    }
    q4 = {}
    for key, path in q4_paths.items():
        data = subprocess.run(
            ["git", "-C", str(REPO), "show", f"{AUTHOR_CUT}:{path}"],
            check=True, stdout=subprocess.PIPE,
        ).stdout
        q4[key] = {"path": path, "sha256": sha256_bytes(data), "bytes": len(data)}
    c6_candidate = subprocess.run(
        ["git", "-C", str(REPO), "cat-file", "-e", f"{AUTHOR_CUT}:rawlsing_next/pre553_historical_authority.py"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    q4["c6_candidate_absent"] = c6_candidate.returncode != 0
    mat_text = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{AUTHOR_CUT}:rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py"],
        check=True, stdout=subprocess.PIPE,
    ).stdout.decode()
    q4["bounded_fqra"] = {
        "fqra_sha256_constant": "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13" in mat_text,
        "coordinate_rule": "QRA35V1::WVS::W7::B_COUNTRY" in mat_text,
        "routing_only_scope": "FROZEN_P2_ROUTING_ONLY" in mat_text,
        "substantive_evidence_false": '"substantive_evidence_use": False' in mat_text or "'substantive_evidence_use': False" in mat_text,
        "r6s_authorities": "def r6s_authorities" in mat_text,
    }
    checks["q4_current_pins"] = q4

    # Author evidence hashes.
    checks["author_trace_sha256"] = sha256_file(AUTHOR / "TRACE.jsonl")
    checks["author_results_trace_sha256_match"] = checks["author_trace_sha256"] == author.get("trace_sha256")
    checks["author_results_schema"] = author.get("schema")

    print(json.dumps(checks, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
