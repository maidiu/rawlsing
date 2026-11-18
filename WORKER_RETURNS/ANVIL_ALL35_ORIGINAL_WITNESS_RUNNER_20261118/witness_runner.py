#!/usr/bin/env python3
"""Generic all-wave witness caller for the construction-only candidate.

SRC04 is the witness.  The default path is metadata-only preflight; it never
opens, stats, hashes, or decodes the original source path.  The future producer
is deliberately a separate process and must exit before the reopen process.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import inspect
import json
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
DEFAULT_BINDING_DIR = HERE.parent / "ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118"
DEFAULT_CONFIG_PIN = HERE / "SRC04_WITNESS_SCOPE.json"
PINNED_BINDING_SHA = "d1283b6ebb660f333efd083f479a16f65ce00b432d2956ac596a62c4f81befb0"
PINNED_CANDIDATE_PATCH = "9da2a3689dc7c4da92474b5c1ae00b7067301d2904354594282d785f3a2c53b5"
MEASURED_512K_PARTIAL_BYTES = 1951192968
DISK_FLOOR = 2 * MEASURED_512K_PARTIAL_BYTES + 1024**3
RAM_CAP = 6 * 1024**3
ACCEPTED = {
    "release_hash": "9ddec98561a0fc54668136cc13e64573edcadcbfb12cd3f79cbfc05606f97ae1",
    "public_objects": 2619317,
    "internal_records": 7514,
    "response_events": 1298649,
    "coordinate_facts": 22011,
    "response_positions": 1298649,
    "q217_unbound": 38,
    "q217_release_events": 0,
}


class PreflightRefusal(RuntimeError):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(code + (f": {detail}" if detail else ""))
        self.code = code
        self.detail = detail


def sha_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _slot_ordinal(section: Mapping[str, Any]) -> int:
    return int(section["slot"]["ordinal"])


def _strip_scope(document: Mapping[str, Any], selection: Mapping[str, Any]) -> dict[str, Any]:
    """Existing accepted SRC04 selection, expressed as a metadata-only slice."""
    doc = copy.deepcopy(dict(document))
    selected = set(map(int, selection["selected_response_slots"]))
    selected_coords = set(map(int, selection["selected_coordinate_slots"]))
    doc["response_slots"] = [x for x in doc.get("response_slots", [])
                             if _slot_ordinal(x) in selected]
    doc["coordinate_slots"] = [x for x in doc.get("coordinate_slots", [])
                               if _slot_ordinal(x) in selected_coords]
    qids = {x["question_id"] for x in doc["response_slots"]}
    doc["questions"] = [x for x in doc.get("questions", []) if x["question_id"] in qids]
    doc["routing"] = [x for x in doc.get("routing", []) if x["question_id"] in qids]
    if isinstance(doc.get("supported_scope"), dict):
        supported = doc["supported_scope"].get("supported_question_ids")
        if isinstance(supported, list):
            doc["supported_scope"]["supported_question_ids"] = [
                q for q in supported if q in qids]
    # The accepted construction did not issue canonical adoption.
    for section in doc["response_slots"]:
        for value in section.get("values", []):
            value["canonical_value"] = None
            value["transform_authority_ref"] = None
            value["extra_authority_refs"] = []
    for question in doc["questions"]:
        field = question.get("canonical_question_ref_or_typed_absence")
        if not isinstance(field, dict) or "typed_absence_state" not in field:
            question["canonical_question_ref_or_typed_absence"] = {
                "typed_absence_state": "NOT_AUTHORIZED", "detail": None}
    return doc


def _q217_guard(config: Mapping[str, Any], selection: Mapping[str, Any]) -> dict[str, Any]:
    slots = [x for x in config.get("response_slots", [])
             if x.get("slot", {}).get("name") == "q217" or x.get("question_id") == "q217"]
    if len(slots) != 1:
        raise PreflightRefusal("Q217_CONFIG_SLOT_AMBIGUOUS", str(len(slots)))
    slot = slots[0]
    ordinal = _slot_ordinal(slot)
    if ordinal != 27:
        raise PreflightRefusal("Q217_ORDINAL_MISMATCH", str(ordinal))
    residuals = [r for r in config.get("residuals", [])
                 if r.get("residual_id") == "SRC04-FIELD-REPAIR-q217"]
    if len(residuals) != 1:
        raise PreflightRefusal("Q217_RESIDUAL_MISSING")
    residual = residuals[0]
    if residual.get("status") != "UNRESOLVED_EXACT_UNLABELED_CODES":
        raise PreflightRefusal("Q217_RESIDUAL_NOT_HELD", str(residual.get("status")))
    if "38 observed q217 cells" not in residual.get("reason", ""):
        raise PreflightRefusal("Q217_UNBOUND_COUNT_NOT_PINNED")
    if int(selection["held_q217_unbound_cells"]) != 38:
        raise PreflightRefusal("Q217_ACCEPTED_COUNT_MISMATCH")
    if int(selection["q217_release_events"]) != 0:
        raise PreflightRefusal("Q217_ACCEPTED_RELEASE_EVENTS_MISMATCH")
    if ordinal in set(map(int, selection["selected_response_slots"])):
        raise PreflightRefusal("Q217_SELECTED_AS_RELEASE_EVENT")
    return {
        "status": "HELD_EXACT_BY_SCOPED_CONFIG",
        "slot_ordinal": ordinal,
        "slot_name": "q217",
        "unbound_cells": 38,
        "release_events": 0,
        "residual_id": residual["residual_id"],
        "residual_status": residual["status"],
        "selected_in_release": False,
    }


def _candidate_api(candidate_tree: Path):
    sys.path.insert(0, str(candidate_tree))
    try:
        from rawlsing_next.pre553_source_i02_handoff import (
            build_source_i02_construction_only,
        )
        from rawlsing_next.pre553_r157_projection_adapter import SourceConfig
    except Exception as exc:
        raise PreflightRefusal("CANDIDATE_IMPORT_FAILED", type(exc).__name__) from exc
    signature = inspect.signature(build_source_i02_construction_only)
    q2 = {"census", "inventory", "policy", "frontier"} & set(signature.parameters)
    if q2:
        raise PreflightRefusal("CANDIDATE_LEAKS_Q2_INPUTS", ",".join(sorted(q2)))
    if "resolver" not in signature.parameters:
        raise PreflightRefusal("CANDIDATE_MISSING_RESOLVER")
    return build_source_i02_construction_only, SourceConfig, str(signature)


def _grant_binding(binding_dir: Path):
    sys.path.insert(0, str(binding_dir))
    try:
        import existing_grant_binding as gb
    except Exception as exc:
        raise PreflightRefusal("GRANT_BINDING_IMPORT_FAILED", type(exc).__name__) from exc
    binding_path = binding_dir / "SRC04_BINDING.json"
    if sha_bytes(binding_path) != PINNED_BINDING_SHA:
        raise PreflightRefusal("GRANT_BINDING_EVIDENCE_DRIFT")
    cfg_raw = load_json(binding_dir / "fixtures/SRC04_CONFIG_BINDING.json")
    cfg = gb.ConfigBinding(**cfg_raw)
    raw = load_json(binding_dir / "TRUST_POLICY.json")
    trust = gb.ExternalTrust(**{k: raw[k] for k in (
        "grant_sha256", "grant_path", "config_file_sha256",
        "config_canonical_sha256", "config_binding_sha256")})
    grant_path = binding_dir / "fixtures/SRC04_FULL_SOURCE_GRANT.json"
    result = gb.bind_existing_grant(grant_path=grant_path, config=cfg, trust=trust)
    if result.status != "REQUEST_ONLY_ALLOWED" or result.decision is None:
        raise PreflightRefusal("GRANT_NOT_REQUEST_ONLY_ALLOWED", result.status)
    resolver = gb.ExistingGrantResolver(grant_path, trust, result.request)
    if resolver.resolve_current(result.request) != resolver.resolve_current(result.request):
        raise PreflightRefusal("GRANT_PRE_POST_DECISION_CHANGED")
    return result, resolver


def _load_config(config_path: Path, index_row: Mapping[str, Any], SourceConfig):
    if sha_bytes(config_path) != index_row["source_config"]["file_sha256"]:
        raise PreflightRefusal("CONFIG_FILE_SHA_MISMATCH")
    document = load_json(config_path)
    cfg = SourceConfig(document)
    if cfg.source_id != "SRC04":
        raise PreflightRefusal("CONFIG_SOURCE_MISMATCH")
    if cfg.active_source_sha256 != index_row["identity"]["source_sha256"]:
        raise PreflightRefusal("CONFIG_SOURCE_SHA_MISMATCH")
    return cfg, document


def preflight(*, candidate_tree: Path, config_path: Path, config_pin: Path,
              binding_dir: Path, outdir: Path, source_id: str = "SRC04") -> dict[str, Any]:
    if source_id != "SRC04":
        raise PreflightRefusal("WITNESS_ONLY_SRC04_IMPLEMENTED")
    pin = load_json(config_pin)
    if pin.get("source_id") != "SRC04":
        raise PreflightRefusal("CONFIG_INDEX_SOURCE_MISMATCH")
    if pin.get("held_q217_unbound_cells") != 38:
        raise PreflightRefusal("Q217_PIN_MISMATCH")
    build, SourceConfig, signature = _candidate_api(candidate_tree)
    cfg, document = _load_config(config_path, pin["config_index_row"], SourceConfig)
    q217 = _q217_guard(document, pin)
    scoped_doc = _strip_scope(document, pin)
    scoped = SourceConfig(scoped_doc)
    if _slot_ordinal(next(x for x in document["response_slots"]
                          if x["slot"]["name"] == "q217")) != 27:
        raise PreflightRefusal("Q217_ORDINAL_MISMATCH")
    if any(x["slot"]["name"] == "q217" for x in scoped_doc["response_slots"]):
        raise PreflightRefusal("Q217_NOT_EXCLUDED")
    if len(scoped_doc["response_slots"]) != 177 or len(scoped_doc["coordinate_slots"]) != 3:
        raise PreflightRefusal("SCOPED_SHAPE_MISMATCH",
                               f"{len(scoped_doc['response_slots'])}/{len(scoped_doc['coordinate_slots'])}")
    if len(scoped_doc["physical_slots"]) != 181:
        raise PreflightRefusal("PHYSICAL_SLOT_ACCOUNTING_LOST")
    grant, resolver = _grant_binding(binding_dir)
    free = shutil.disk_usage(outdir).free
    if free < DISK_FLOOR:
        raise PreflightRefusal("DISK_GATE", f"{free} < {DISK_FLOOR}")
    plan = {
        "schema": "ANVIL_ALL35_WITNESS_PLAN@1",
        "source_id": "SRC04",
        "candidate_api": signature,
        "config_path": str(config_path),
        "config_file_sha256": sha_bytes(config_path),
        "config_index_sha256": sha_bytes(config_pin),
        "grant_binding_sha256": PINNED_BINDING_SHA,
        "grant_ref": grant.grant_ref.as_dict(),
        "decision_ref": grant.decision.decision_ref.as_dict(),
        "q217": q217,
        "scoped_counts": {
            "response_slots": len(scoped_doc["response_slots"]),
            "coordinate_slots": len(scoped_doc["coordinate_slots"]),
            "physical_slots": len(scoped_doc["physical_slots"]),
        },
        "accepted_accounting": ACCEPTED,
        "process_isolation": {
            "producer": "separate subprocess; wait for exact nonzero exit",
            "reopen": "fresh subprocess only after producer pid reaped",
            "source_launch": "NOT_PERFORMED",
        },
        "resources": {
            "ram_cap_bytes": RAM_CAP,
            "measured_512x600_partial_bytes": MEASURED_512K_PARTIAL_BYTES,
            "disk_floor_bytes": DISK_FLOOR,
            "available_bytes": free,
            "wall_cutoff": None,
        },
        "no_source_open_stat_hash_decode": True,
        "status": "DRY_PREFLIGHT_OK__Q217_HELD__SCOPED_CONFIG_READY",
    }
    (outdir / "WITNESS_PLAN.json").write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n")
    return plan


def verify_roots(actual, expected, *, label: str = "reopen") -> None:
    """Exact root comparison used by the fresh reopen; wrong roots fail closed."""
    if actual != expected:
        raise PreflightRefusal("WRONG_ROOT_" + label.upper())


def verify_accounting(counts: Mapping[str, int], stats: Any) -> None:
    expected = {
        "RespondentEvent": ACCEPTED["response_events"],
        "EmpiricalCoordinateFact": ACCEPTED["coordinate_facts"],
    }
    for family, value in expected.items():
        if int(counts.get(family, -1)) != value:
            raise PreflightRefusal("ACCOUNTING_MISMATCH_" + family)
    if int(getattr(stats, "source_rows", -1)) != 7337:
        raise PreflightRefusal("ACCOUNTING_ROWS_MISMATCH")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate-tree", type=Path, required=True)
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--config-pin", type=Path, default=DEFAULT_CONFIG_PIN)
    ap.add_argument("--binding-dir", type=Path, default=DEFAULT_BINDING_DIR)
    ap.add_argument("--outdir", type=Path, default=HERE / "DRY_RUN")
    ap.add_argument("--source-id", default="SRC04")
    a = ap.parse_args()
    a.outdir.mkdir(parents=True, exist_ok=True)
    try:
        plan = preflight(candidate_tree=a.candidate_tree, config_path=a.config,
                         config_pin=a.config_pin, binding_dir=a.binding_dir,
                         outdir=a.outdir, source_id=a.source_id)
    except PreflightRefusal as exc:
        result = {"schema": "ANVIL_ALL35_WITNESS_PREFLIGHT@1",
                  "status": "REFUSED", "code": exc.code, "detail": exc.detail,
                  "source_read_performed": False}
        (a.outdir / "WITNESS_PLAN.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result))
        return 2
    print(json.dumps({"status": plan["status"], "q217": plan["q217"],
                      "grant": plan["grant_ref"], "free": plan["resources"]["available_bytes"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
