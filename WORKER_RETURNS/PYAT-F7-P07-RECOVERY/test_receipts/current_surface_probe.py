#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import pathlib
import subprocess

from rawlsing_next.pre553_empirical_authority import AUTHORITY_KINDS

ROOT = pathlib.Path(__file__).resolve().parents[3]
SOURCE_RELATIONS = ROOT / "rawlsing_next" / "pre553_source_relations.py"
F7_PATH = ROOT / "rawlsing_next" / "pre553_temporal_comparability.py"


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True, text=True, capture_output=True).stdout.strip()


def _production_imports(module_name: str) -> list[str]:
    hits: list[str] = []
    for path in (ROOT / "rawlsing_next").rglob("*.py"):
        relative = path.relative_to(ROOT)
        if "tests" in relative.parts or "WORKER_RETURNS" in relative.parts:
            continue
        if path.name == f"{module_name}.py":
            continue
        try:
            tree = ast.parse(path.read_text(), filename=str(path))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.ImportFrom) and node.module:
                names.append(node.module)
            elif isinstance(node, ast.Import):
                names.extend(alias.name for alias in node.names)
            if f"rawlsing_next.{module_name}" in names or module_name in names:
                hits.append(str(relative))
                break
    return sorted(set(hits))


source_text = SOURCE_RELATIONS.read_text()
result = {
    "schema": "PYAT_F7_P07_CURRENT_SURFACE_PROBE@1",
    "head": _git("rev-parse", "HEAD"),
    "head_subject": _git("log", "-1", "--format=%s"),
    "pre553_temporal_comparability_path_exists": F7_PATH.exists(),
    "pre553_source_relations_git_blob": _git(
        "rev-parse", f"HEAD:rawlsing_next/pre553_source_relations.py"),
    "pre553_empirical_authority_git_blob": _git(
        "rev-parse", f"HEAD:rawlsing_next/pre553_empirical_authority.py"),
    "authority_kind_count": len(AUTHORITY_KINDS),
    "temporal_evidence_kind_present": "TEMPORAL_EVIDENCE" in AUTHORITY_KINDS,
    "temporal_comparability_kind_present": "TEMPORAL_COMPARABILITY" in AUTHORITY_KINDS,
    "nested_sealed_owner_string_present": "_make_sealed_source_relation_owner" in source_text,
    "authenticated_source_relation_decision_present": (
        "authenticated_source_relation_decision" in source_text),
    "validate_relation_decision_replay_identity_present": (
        "validate_relation_decision_replay_identity" in source_text),
    "pre553_source_relations_production_importers": _production_imports(
        "pre553_source_relations"),
    "pre553_temporal_comparability_production_importers": _production_imports(
        "pre553_temporal_comparability"),
}
print(json.dumps(result, indent=2, sort_keys=True))
