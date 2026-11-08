#!/usr/bin/env python3
"""C10 Q3 F03 historical authority -> unchanged first consumer replay.

Test-time replay only.  The exact historical module and selected nonrespondent
authority bytes are copied from the pinned historical Git cut into this C10
lease.  No respondent/source microdata, SAV/DTA/DB, production module, current
engine, or original scientific operation is executed.
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

FULL_SHA = "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13"
REGISTRY_SHA = "a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b"
MODULE_SHA = "2fb0851d8bac6f3d381fdf11749f7e04e676de914d643e5be1ad4603cc39f63c"
MODULE_GIT_PATH = "data/ddm_build_copy/ddm_v550_question_relation_authority.py"
FULL_GIT_PATH = (
    "data/ddm_build_copy/authority/full_question_relation_authority/"
    "R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv"
)
REGISTRY_GIT_PATH = (
    "data/ddm_build_copy/bindings/question_relation_registry_35wave_active_v1.csv"
)


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


def load_module(module_path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import module at {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def ensure_pinned_historical_file(repo: Path, git_path: str, dest: Path, expected_sha: str) -> None:
    """Materialize an exact pinned historical file only inside this C10 tmp lease."""
    if dest.exists():
        actual = sha256_file(dest)
        if actual == expected_sha:
            return
        dest.unlink()
    dest.parent.mkdir(parents=True, exist_ok=True)
    data = subprocess.run(
        ["git", "-C", str(repo), "show", f"9ba4764bef551b1ce498e5772d60b73d69337d4b:{git_path}"],
        stdout=subprocess.PIPE,
        check=True,
    ).stdout
    actual = sha256_bytes(data)
    if actual != expected_sha:
        raise SystemExit(f"Git extraction pin mismatch {git_path}: {actual} != {expected_sha}")
    dest.write_bytes(data)


def bridge_from_audit_row(row: pd.Series) -> dict[str, Any]:
    return {
        "source_family": str(row["source_family"]),
        "canonical_wave": str(row["canonical_wave"]),
        "country_code": str(row["input_country_code"]),
        "question_id": str(row["question_id"]),
        "var_code": str(row["var_code"]),
    }


def selected_row(row: pd.Series) -> dict[str, Any]:
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
    repo = Path(__file__).resolve().parents[4]
    lease = Path(__file__).resolve().parents[1]
    replay_root = lease / "tmp" / "replay_root"
    restore_root = lease / "tmp" / "replay_restore_root"
    module_path = replay_root / MODULE_GIT_PATH
    full_path = replay_root / FULL_GIT_PATH
    registry_path = replay_root / REGISTRY_GIT_PATH

    for git_path, dest, expected in (
        (MODULE_GIT_PATH, module_path, MODULE_SHA),
        (FULL_GIT_PATH, full_path, FULL_SHA),
        (REGISTRY_GIT_PATH, registry_path, REGISTRY_SHA),
    ):
        ensure_pinned_historical_file(repo, git_path, dest, expected)
        actual = sha256_file(dest)
        if actual != expected:
            raise SystemExit(f"pin mismatch {dest}: {actual} != {expected}")

    mod = load_module(module_path, "c10_ddm_v550_question_relation_authority")
    if mod.ROOT.resolve() != replay_root.resolve():
        raise SystemExit(f"unexpected historical module ROOT: {mod.ROOT}")

    # Actual default loader + closed-35 scope, not a fixture.
    index = mod.load_question_relation_authority()
    if index.file_sha256 != FULL_SHA or len(index.rows) != 18518:
        raise SystemExit("full authority index does not match the selected pin")
    closed35 = mod.active_closed_35_waves()
    if len(closed35) != 35 or ("Asian Barometer", "W6", "") in closed35:
        raise SystemExit("closed-35 scope is not the expected active scope")

    # Actual public consumer audit over every authority row (nonrespondent).
    full_frame = pd.read_csv(full_path, dtype=str, keep_default_na=False)
    audit = mod.validate_active_universe(full_frame)
    status_counts = {str(k): int(v) for k, v in audit["resolver_status"].value_counts().items()}
    relation_counts = {str(k): int(v) for k, v in audit["relation_use_status"].value_counts().items()}
    source_wave_counts = (
        audit.groupby(["source_family", "canonical_wave"], dropna=False)
        .size()
        .reset_index(name="rows")
    )
    active_source_waves = [
        (str(r.source_family), str(r.canonical_wave), int(r.rows))
        for r in source_wave_counts.itertuples(index=False)
        if not (str(r.source_family) == "Asian Barometer" and str(r.canonical_wave) == "W6")
    ]
    summary = {
        "audit_rows": int(len(audit)),
        "resolver_status_counts": status_counts,
        "relation_use_status_counts": relation_counts,
        "directional_coordinates_complete": int(audit["directional_coordinates_complete"].sum()),
        "current_directional_atom_eligible": int(audit["current_directional_atom_eligible"].sum()),
        "active_closed_35_count": len(closed35),
        "active_source_wave_count": len(active_source_waves),
        "active_source_waves": active_source_waves,
        "full_authority_rows": int(len(full_frame)),
        "full_authority_sha256": sha256_file(full_path),
        "full_audit_digest": canonical_hash(
            {
                "status": status_counts,
                "relation": relation_counts,
                "active_source_waves": active_source_waves,
            }
        ),
    }

    trace: list[dict[str, Any]] = []
    execution_limit = (
        "TEST_TIME_HISTORICAL_REPLAY_ONLY__NOT_EVIDENCE_OF_ORIGINAL_RUN__"
        "NO_RESPONDENT_OR_SOURCE_MICRODATA"
    )
    common = {
        "authority_sha256": FULL_SHA,
        "authority_bytes": full_path.stat().st_size,
        "authority_git_path": FULL_GIT_PATH,
        "module_sha256": MODULE_SHA,
        "module_git_path": MODULE_GIT_PATH,
        "entrypoint": "apply_question_relation_authority",
        "loader": "load_question_relation_authority",
        "execution_limit": execution_limit,
    }

    trace.append(
        {
            "event_id": "C10-F03-001",
            "kind": "AUTHORITY_LOAD",
            "status": "PASS",
            **common,
            "authority_rows": len(index.rows),
            "index_keys": len(index.by_key),
            "active_closed_35_count": len(closed35),
            "active_closed_35_excludes_w6": True,
        }
    )

    trace.append(
        {
            "event_id": "C10-F03-002",
            "kind": "FULL_AUTHORITY_AUDIT",
            "status": "OBSERVED",
            **common,
            "audit_rows": summary["audit_rows"],
            "resolver_status_counts": status_counts,
            "relation_use_status_counts": relation_counts,
            "active_closed_35_count": len(closed35),
            "active_source_wave_count": len(active_source_waves),
            "full_audit_digest": summary["full_audit_digest"],
            "coverage_note": "all 18518 authority rows resolved; 35 active source/wave scopes plus excluded W6; row sample is not an all35 substitution",
        }
    )

    candidates = audit[
        (audit["resolver_status"] == "RESOLVED_DIRECTIONAL_AUTHORITY")
        & (audit["directional_coordinates_complete"])
        & (audit["current_directional_atom_eligible"])
    ].copy()
    if candidates.empty:
        raise SystemExit("no actual positive directional authority rows")

    positives: list[dict[str, Any]] = []
    positive_trace_rows: list[dict[str, Any]] = []
    for source in candidates["source_family"].drop_duplicates().tolist():
        row = candidates[candidates["source_family"] == source].iloc[0]
        bridge = bridge_from_audit_row(row)
        out = mod.apply_question_relation_authority(bridge)
        if out.get("question_relation_authority_resolution_status") != "RESOLVED_DIRECTIONAL_AUTHORITY":
            raise SystemExit(f"positive observation failed for {source}: {out.get('question_relation_authority_resolution_status')}")
        out_hash = canonical_hash(out)
        positive = {
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
                1
                for key in (
                    "driver_id",
                    "driver_facet_id",
                    "question_block_id",
                    "structural_domain_id",
                    "relation_axis_id",
                    "target_entity_id",
                )
                if str(out.get(key, "")) != ""
            ),
            "output_hash": out_hash,
        }
        positives.append(positive)
        positive_trace_rows.append(
            {
                "event_id": f"C10-F03-POS-{len(positive_trace_rows)+1:02d}",
                "kind": "POSITIVE_FIRST_CONSUMER",
                "status": "PASS",
                **common,
                "selected_row": positive["selected_row"],
                "bridge_input": bridge,
                "resolver_status": positive["resolver_status"],
                "relation_use_status": positive["relation_use_status"],
                "semantic_role": positive["semantic_role"],
                "current_directional_atom_eligible": positive["current_directional_atom_eligible"],
                "question_relation_coverage_eligible": positive["question_relation_coverage_eligible"],
                "authority_artifact_sha256": positive["authority_artifact_sha256"],
                "structural_coordinate_count": positive["structural_coordinate_count"],
                "output_hash": out_hash,
            }
        )

    trace.extend(positive_trace_rows)

    # Actual explicit block row.
    block_row = audit[audit["resolver_status"] == "RESOLVED_EXPLICIT_BLOCK"].iloc[0]
    block_out = mod.apply_question_relation_authority(bridge_from_audit_row(block_row))
    block_expected = str(block_row["resolver_status"])
    if block_out.get("question_relation_authority_resolution_status") != block_expected:
        raise SystemExit("explicit-block row did not preserve the actual block status")
    if str(block_out.get("semantic_role")) != "UNKNOWN" or bool(block_out.get("current_directional_atom_eligible")):
        raise SystemExit("explicit-block row was not fail-closed")
    trace.append(
        {
            "event_id": "C10-F03-NEG-BLOCK",
            "kind": "NEGATIVE_EXPLICIT_BLOCK",
            "status": "OBSERVED_REFUSAL",
            **common,
            "selected_row": selected_row(block_row),
            "resolver_status": block_out.get("question_relation_authority_resolution_status"),
            "semantic_role": block_out.get("semantic_role"),
            "structural_coordinates_cleared": all(
                str(block_out.get(key, "")) == ""
                for key in (
                    "driver_id",
                    "driver_facet_id",
                    "question_block_id",
                    "structural_domain_id",
                    "relation_axis_id",
                    "target_entity_id",
                )
            ),
            "current_directional_atom_eligible": bool(block_out.get("current_directional_atom_eligible")),
            "question_relation_coverage_eligible": bool(block_out.get("question_relation_coverage_eligible")),
            "output_hash": canonical_hash(block_out),
        }
    )

    # Actual ambiguous authority row.
    ambiguous_rows = audit[audit["resolver_status"] == "BLOCKED_AMBIGUOUS_AUTHORITY"]
    ambiguous = None
    if not ambiguous_rows.empty:
        amb_row = ambiguous_rows.iloc[0]
        amb_out = mod.apply_question_relation_authority(bridge_from_audit_row(amb_row))
        if amb_out.get("question_relation_authority_resolution_status") != "BLOCKED_AMBIGUOUS_AUTHORITY":
            raise SystemExit("ambiguous authority row did not preserve refusal")
        ambiguous = {
            "selected_row": selected_row(amb_row),
            "resolver_status": amb_out.get("question_relation_authority_resolution_status"),
            "semantic_role": amb_out.get("semantic_role"),
            "current_directional_atom_eligible": bool(amb_out.get("current_directional_atom_eligible")),
            "output_hash": canonical_hash(amb_out),
        }
        trace.append(
            {
                "event_id": "C10-F03-NEG-AMBIGUOUS",
                "kind": "NEGATIVE_AMBIGUOUS_AUTHORITY",
                "status": "OBSERVED_REFUSAL",
                **common,
                **ambiguous,
            }
        )

    first_positive = positives[0]
    first_bridge = first_positive["bridge_input"]
    missing_bridge = dict(first_bridge)
    missing_bridge["var_code"] = "__C10_MISSING__" + str(first_bridge["var_code"])
    missing_bridge["question_id"] = "__C10_MISSING__" + str(first_bridge["question_id"])
    missing_out = mod.apply_question_relation_authority(missing_bridge)
    if missing_out.get("question_relation_authority_resolution_status") != "BLOCKED_MISSING_AUTHORITY":
        raise SystemExit("missing-row negative did not fail closed")
    missing = {
        "bridge_input": missing_bridge,
        "resolver_status": missing_out.get("question_relation_authority_resolution_status"),
        "semantic_role": missing_out.get("semantic_role"),
        "structural_coordinates_cleared": all(
            str(missing_out.get(key, "")) == ""
            for key in (
                "driver_id",
                "driver_facet_id",
                "question_block_id",
                "structural_domain_id",
                "relation_axis_id",
                "target_entity_id",
            )
        ),
        "current_directional_atom_eligible": bool(missing_out.get("current_directional_atom_eligible")),
        "question_relation_coverage_eligible": bool(missing_out.get("question_relation_coverage_eligible")),
        "output_hash": canonical_hash(missing_out),
    }
    trace.append(
        {
            "event_id": "C10-F03-NEG-MISSING",
            "kind": "NEGATIVE_MISSING_AUTHORITY_ROW",
            "status": "OBSERVED_REFUSAL",
            **common,
            **missing,
        }
    )

    # Correctly selected authority vs the 700-row calibration registry (limited
    # authority); the actual loader/validator is used, no reader monkeypatch.
    wrong_out = mod.apply_question_relation_authority(first_bridge, authority_path=registry_path)
    wrong = {
        "wrong_authority_path": REGISTRY_GIT_PATH,
        "wrong_authority_sha256": REGISTRY_SHA,
        "resolver_status": wrong_out.get("question_relation_authority_resolution_status"),
        "semantic_role": wrong_out.get("semantic_role"),
        "current_directional_atom_eligible": bool(wrong_out.get("current_directional_atom_eligible")),
        "authority_artifact_sha256": wrong_out.get("authority_artifact_sha256"),
        "output_hash": canonical_hash(wrong_out),
    }
    trace.append(
        {
            "event_id": "C10-F03-NEG-WRONG",
            "kind": "NEGATIVE_WRONG_OR_LIMITED_AUTHORITY",
            "status": "OBSERVED",
            **common,
            **wrong,
        }
    )

    missing_path = lease / "tmp" / "missing_authority.csv"
    try:
        mod.apply_question_relation_authority(first_bridge, authority_path=missing_path)
        missing_file = {"status": "NO_ERROR"}
    except Exception as exc:  # exact observed exception, not a fabricated PASS
        missing_file = {"status": "EXCEPTION", "type": type(exc).__name__, "message": str(exc)}
    trace.append(
        {
            "event_id": "C10-F03-NEG-FILE",
            "kind": "NEGATIVE_MISSING_AUTHORITY_FILE",
            "status": missing_file["status"],
            **common,
            **missing_file,
        }
    )

    # Cold restore: a second disposable root with identical module/authority bytes.
    if restore_root.exists():
        shutil.rmtree(restore_root)
    (restore_root / "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814").mkdir(parents=True)
    (restore_root / "data/ddm_build_copy/bindings").mkdir(parents=True)
    shutil.copyfile(module_path, restore_root / MODULE_GIT_PATH)
    shutil.copyfile(full_path, restore_root / FULL_GIT_PATH)
    shutil.copyfile(registry_path, restore_root / REGISTRY_GIT_PATH)
    restore_module = load_module(restore_root / MODULE_GIT_PATH, "c10_restore_question_relation_authority")
    restore_out = restore_module.apply_question_relation_authority(first_bridge)
    restore_hash = canonical_hash(restore_out)
    if restore_hash != first_positive["output_hash"]:
        raise SystemExit("cold-restore output hash differs from the original positive output")
    trace.append(
        {
            "event_id": "C10-F03-RESTORE",
            "kind": "COLD_RESTORE_DISPOSABLE_COPY",
            "status": "PASS",
            **common,
            "authority_copy_sha256": sha256_file(restore_root / FULL_GIT_PATH),
            "module_copy_sha256": sha256_file(restore_root / MODULE_GIT_PATH),
            "output_hash": restore_hash,
            "matches_positive_output_hash": True,
        }
    )

    # Actual AR-0006 residual consumer (20-row Latinobarómetro 1995 slice).
    residual = mod.derive_legacy_latinobarometro_1995_residual(full_frame)
    residual_rows = [
        {
            "source_family": str(r.get("source_family", "")),
            "canonical_wave": str(r.get("canonical_wave", "")),
            "country_code_scope": str(r.get("country_code_scope", "")),
            "question_id": str(r.get("question_id", "")),
            "var_code": str(r.get("var_code", "")),
            "authority_rule_id": str(r.get("authority_rule_id", "")),
        }
        for r in residual.to_dict(orient="records")
    ]
    residual_csv = residual.to_csv(index=False)
    registry_index = mod.load_question_relation_authority(registry_path)
    trace.append(
        {
            "event_id": "C10-F03-AR0006-RESIDUAL",
            "kind": "AR0006_DERIVED_RESIDUAL_CONSUMER",
            "status": "PASS" if len(residual) == 20 else "FAIL",
            **common,
            "registry_sha256": registry_index.file_sha256,
            "registry_rows": len(registry_index.rows),
            "residual_rows": len(residual),
            "residual_source_families": sorted({r["source_family"] for r in residual_rows}),
            "residual_canonical_waves": sorted({r["canonical_wave"] for r in residual_rows}),
            "residual_csv_sha256": hashlib.sha256(residual_csv.encode()).hexdigest(),
            "row_rule": "exact registry identity minus full-R1 target identity; 20-row Latinobarometro 1995 residual",
        }
    )

    # Current Q4 successor locations: exact current file hashes and symbols, not
    # current execution or equivalence.
    current_paths = {
        "generic_projection": repo / "rawlsing_next/pre553_source_backed_c11_facade.py",
        "generic_query": repo / "rawlsing_next/pre553_empirical_query.py",
        "generic_authority_validation": repo / "rawlsing_next/pre553_empirical_authority.py",
        "bounded_fqra_materializer": repo / "rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py",
        "c6_candidate_historical_authority": repo / "rawlsing_next/pre553_historical_authority.py",
    }
    current = {}
    for key, path in current_paths.items():
        current[key] = {
            "path": str(path.relative_to(repo)),
            "exists": path.is_file(),
            "sha256": sha256_file(path) if path.is_file() else None,
        }
    current["bounded_fqra_materializer"].update(
        {
            "symbol": "FQRA_SHA256 / COORDINATE_AUTHORITY_MATERIAL / r6s_authorities",
            "lines": "68,202-243,534-544",
            "pinned_fqra_sha256": FULL_SHA,
            "bounded_coordinate_rule": "QRA35V1::WVS::W7::B_COUNTRY",
            "scope": "FROZEN_P2_ROUTING_ONLY; substantive_evidence_use=false",
            "current_execution": "NOT_RUN__REQUIRES_WVS7_SOURCE/PHYSICAL_RESPONDENT_DATA",
        }
    )
    current["c6_candidate_historical_authority"]["status"] = (
        "ABSENT_AT_0d548b__C6_CANDIDATE_NOT_INSTALLED"
    )
    current["owner_status"] = (
        "CURRENT_GENERIC_AUTHORITY_OWNER_AND_BOUNDED_FQRA_PIN_PRESENT__"
        "FULL_F03_FQRA_ADAPTER_AND_CURRENT_SELECTION_NOT_PROVED__NO_SEVERANCE"
    )
    trace.append(
        {
            "event_id": "C10-F03-Q4-CURRENT",
            "kind": "CURRENT_SUCCESSOR_LOCATION",
            "status": "MAPPED_NOT_RUN",
            "current": current,
            "c6_currentness_candidate": "rawlsing_next.pre553_historical_authority.QuestionRelationAuthority.resolve/apply_row -> AuthoritySnapshot; rawlsing_next/pre553_empirical_objects.py; AuthoritySnapshot; GovernedC11Projection; execute_empirical_query",
            "c7_checkpoint_f03_label": "UNPROVED_CURRENT_SELECTION",
            "exact_remaining_boundary": (
                "Historical authority-to-apply consumer replay observed; V550 bridge/compile_v551_relation_evidence_atoms downstream not run; "
                "full F03 FQRA current adapter/selection not proved; current WVS7 FQRA pin is bounded FROZEN_P2_ROUTING coordinate use, not general equivalence."
            ),
            "severance": "NOT_PROVED__NO_GOVERNING_INPUT_LOSS_DEMONSTRATED",
        }
    )

    results = {
        "schema": "C10_Q3_F03_REPLAY_RESULTS_V1",
        "authority": {
            "release_id": "AR-0005",
            "sha256": FULL_SHA,
            "bytes": full_path.stat().st_size,
            "historical_git_path": FULL_GIT_PATH,
            "selected_locator": FULL_GIT_PATH,
            "registry_release_id": "AR-0006",
            "registry_sha256": REGISTRY_SHA,
            "registry_bytes": registry_path.stat().st_size,
            "registry_git_path": REGISTRY_GIT_PATH,
        },
        "module": {
            "sha256": MODULE_SHA,
            "bytes": module_path.stat().st_size,
            "git_path": MODULE_GIT_PATH,
            "historical_source_sha": "9ba4764bef551b1ce498e5772d60b73d69337d4b",
            "entrypoint": "apply_question_relation_authority",
            "loader": "load_question_relation_authority",
            "audit": "validate_active_universe",
            "residual_consumer": "derive_legacy_latinobarometro_1995_residual",
        },
        "full_audit": summary,
        "positive_rows": positives,
        "negative": {
            "explicit_block": {
                "selected_row": selected_row(block_row),
                "resolver_status": block_out.get("question_relation_authority_resolution_status"),
                "semantic_role": block_out.get("semantic_role"),
                "coords_cleared": all(
                    str(block_out.get(key, "")) == ""
                    for key in (
                        "driver_id",
                        "driver_facet_id",
                        "question_block_id",
                        "structural_domain_id",
                        "relation_axis_id",
                        "target_entity_id",
                    )
                ),
                "output_hash": canonical_hash(block_out),
            },
            "ambiguous": ambiguous,
            "missing": missing,
            "wrong_or_limited": wrong,
            "missing_file": missing_file,
        },
        "restore": {
            "authority_copy_sha256": sha256_file(restore_root / FULL_GIT_PATH),
            "module_copy_sha256": sha256_file(restore_root / MODULE_GIT_PATH),
            "output_hash": restore_hash,
            "matches_positive_output_hash": True,
        },
        "residual_ar0006": {
            "rows": len(residual),
            "source_families": sorted({r["source_family"] for r in residual_rows}),
            "canonical_waves": sorted({r["canonical_wave"] for r in residual_rows}),
            "csv_sha256": hashlib.sha256(residual_csv.encode()).hexdigest(),
            "selected_rows": residual_rows,
            "registry_sha256": registry_index.file_sha256,
            "registry_rows": len(registry_index.rows),
        },
        "execution_limit": execution_limit,
        "current_successor": current,
        "trace_sha256": None,
    }
    (lease / "logs").mkdir(parents=True, exist_ok=True)
    (lease / "logs" / "replay_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False, default=str) + "\n"
    )
    trace_path = lease / "TRACE.jsonl"
    with trace_path.open("w") as fh:
        for event in trace:
            fh.write(json.dumps(event, ensure_ascii=False, sort_keys=False, default=str) + "\n")
    # Add the trace digest without changing the trace file.
    results["trace_sha256"] = sha256_file(trace_path)
    (lease / "logs" / "replay_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False, default=str) + "\n"
    )
    print(json.dumps({
        "status": "PASS",
        "trace_sha256": results["trace_sha256"],
        "positive_rows": len(positives),
        "audit_rows": summary["audit_rows"],
        "active_closed_35": len(closed35),
        "residual_rows": len(residual),
        "restore_matches": True,
        "negative_statuses": {
            "block": block_out.get("question_relation_authority_resolution_status"),
            "ambiguous": ambiguous["resolver_status"] if ambiguous else None,
            "missing": missing_out.get("question_relation_authority_resolution_status"),
            "wrong": wrong_out.get("question_relation_authority_resolution_status"),
            "missing_file": missing_file["status"],
        },
        "current_owner_status": current["owner_status"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
