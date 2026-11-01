#!/usr/bin/env python3
from __future__ import annotations

import ast
from dataclasses import asdict
import inspect
import json
import pathlib
import subprocess

import rawlsing_next.pre553_issued_workload as issued
import rawlsing_next.pre553_universal_workload as universal

ROOT = pathlib.Path(__file__).resolve().parents[3]
MODULES = (
    "pre553_batch_runner",
    "pre553_issued_workload",
    "pre553_native_workload_binding",
    "pre553_universal_workload",
    "pre553_source_native_preimage_adapter",
    "pre553_learned_world_composition",
    "pre553_learned_product_lifecycle",
    "universal_grammar.native_map",
    "universal_grammar.enumerate",
    "universal_grammar.types",
)
ABSENT = (
    "pre553_production_binding",
    "pre553_source_read_admission",
    "pre553_universal_evidence_binding",
    "pre553_universal_empirical_extension",
    "s06_trusted_release_replay",
    "pre553_batch_durable_checkpoint_candidate",
    "pre553_governed_batch_checkpoint_integration_candidate",
    "pre553_v2_durable_consumer_integration_candidate",
    "pre553_original_workload_binder_candidate",
    "pre553_original_workload_contract_v2_candidate",
    "pre553_original_workload_v2_verifier_candidate",
)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args], check=True, text=True,
        capture_output=True).stdout.strip()


def _importers(module: str) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    module_path = "rawlsing_next/" + module.replace(".", "/") + ".py"
    for path in (ROOT / "rawlsing_next").rglob("*.py"):
        rel = str(path.relative_to(ROOT))
        if rel == module_path:
            continue
        try:
            tree = ast.parse(path.read_text(), filename=rel)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.ImportFrom) and node.module:
                names.append(node.module)
            elif isinstance(node, ast.Import):
                names.extend(alias.name for alias in node.names)
            if any(name == f"rawlsing_next.{module}" or name.startswith(
                    f"rawlsing_next.{module}.") for name in names):
                hits.append({
                    "path": rel,
                    "kind": "TEST" if "/tests/" in rel else "PRODUCTION_OR_WORKER",
                })
                break
    return sorted(hits, key=lambda item: (item["path"], item["kind"]))



def _callers(function_name: str, defining_module: str) -> list[str]:
    hits: list[str] = []
    defining_path = "rawlsing_next/" + defining_module.replace(".", "/") + ".py"
    for path in (ROOT / "rawlsing_next").rglob("*.py"):
        rel = str(path.relative_to(ROOT))
        if rel == defining_path:
            continue
        try:
            tree = ast.parse(path.read_text(), filename=rel)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if isinstance(func, ast.Name) and func.id == function_name:
                hits.append(rel)
                break
            if isinstance(func, ast.Attribute) and func.attr == function_name:
                hits.append(rel)
                break
    return sorted(set(hits))

def _wave(index: int) -> dict:
    return {
        "atlas_id": f"ATLAS-{index:02d}",
        "original_manifest_identity": {"dataset_id": f"DATASET-{index:02d}"},
        "family": "ORIGINAL35",
        "wave": f"WAVE-{index:02d}",
    }


waves = [_wave(i) for i in range(35)]
roster = issued.original35_roster(waves)
short_roster = None
try:
    issued.original35_roster(waves[:34])
except Exception as exc:
    short_roster = type(exc).__name__ + ":" + str(exc)

result = {
    "schema": "PYAT_RRIF_D3_LINEAGE_PROBE@1",
    "head": _git("rev-parse", "HEAD"),
    "head_subject": _git("log", "-1", "--format=%s"),
    "current_modules": {},
    "absent_paths": {},
    "all35": {
        "roster_size": len(roster),
        "roster_is_identity_only": all(set(asdict(w)) == {"atlas_id", "dataset_id", "source_family", "wave"} for w in roster),
        "short_roster_refusal": short_roster,
        "reconcile_signature": str(inspect.signature(issued.reconcile_estate_workloads)),
        "compile_signature": str(inspect.signature(universal.compile_universal_workload)),
        "issued_module_callers": _importers("pre553_issued_workload"),
        "universal_module_callers": _importers("pre553_universal_workload"),
        "original35_roster_callers_outside_module": _callers(
            "original35_roster", "pre553_issued_workload"),
        "reconcile_estate_workloads_callers_outside_module": _callers(
            "reconcile_estate_workloads", "pre553_issued_workload"),
        "compile_universal_workload_callers_outside_module": _callers(
            "compile_universal_workload", "pre553_universal_workload"),
        "interpretation": (
            "original35_roster validates caller-supplied wave dictionaries; "
            "reconcile_estate_workloads validates caller-supplied workloads and "
            "IssuedEstateFrontier; compile_universal_workload takes one NativePreimageBundle. "
            "No current function constructs requests for all 35 waves."
        ),
    },
}
for module in MODULES:
    path = ROOT / ("rawlsing_next/" + module.replace(".", "/") + ".py")
    rel = str(path.relative_to(ROOT))
    result["current_modules"][module] = {
        "path": rel,
        "exists": path.exists(),
        "git_blob": _git("rev-parse", f"HEAD:{rel}") if path.exists() else None,
        "lines": len(path.read_text().splitlines()) if path.exists() else 0,
        "importers": _importers(module),
    }
for module in ABSENT:
    path = ROOT / ("rawlsing_next/" + module.replace(".", "/") + ".py")
    result["absent_paths"][module] = {"path": str(path.relative_to(ROOT)), "exists": path.exists()}
print(json.dumps(result, indent=2, sort_keys=True))
