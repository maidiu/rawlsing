#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
MODULE_BLOB = "6f6b462b1cdef54d7989f15452473383c1661594"
TEST_BLOB = "8a82bd5905d266c1d500b1bf2bdcb01ea948efd6"
SOURCE_RELATIONS_BLOB = "8053d30d306a3654ebf563043088311ff390bb2b"
CUT = "c86ae335eaf70e82b5764c46754b16ca7e1587ce"


def _git_show(blob: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-p", blob],
        check=True, capture_output=True).stdout


def _counts(raw: bytes) -> dict[str, int]:
    tree = ast.parse(raw.decode("utf-8"))
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    tests = [node for node in functions if node.name.startswith("test_")]
    return {
        "function_defs": len(functions),
        "class_defs": len(classes),
        "test_functions": len(tests),
    }


module = _git_show(MODULE_BLOB)
test = _git_show(TEST_BLOB)
source_relations = _git_show(SOURCE_RELATIONS_BLOB)
result = {
    "schema": "PYAT_F7_P07_HISTORICAL_PROBE@1",
    "cut": CUT,
    "f7_module_blob": MODULE_BLOB,
    "f7_module_sha256": hashlib.sha256(module).hexdigest(),
    "f7_module_bytes": len(module),
    "f7_module_counts": _counts(module),
    "f7_tests_blob": TEST_BLOB,
    "f7_tests_sha256": hashlib.sha256(test).hexdigest(),
    "f7_tests_bytes": len(test),
    "f7_tests_counts": _counts(test),
    "source_relations_blob_at_cut": SOURCE_RELATIONS_BLOB,
    "source_relations_sha256": hashlib.sha256(source_relations).hexdigest(),
    "source_relations_bytes": len(source_relations),
    "source_relations_nested_sealed_owner_present": (
        b"_make_sealed_source_relation_owner" in source_relations),
    "source_relations_authenticated_entrypoint_present": (
        b"authenticated_source_relation_decision" in source_relations),
    "f7_requires_temporal_comparability_kind": (
        b"TEMPORAL_COMPARABILITY" in module),
    "f7_imports_native_extension": any(
        token in module for token in (b"import p07", b"PyInit_", b"ctypes", b"cffi")),
    "f7_uses_intervals_overlap_boolean": b"intervals_overlap" in module,
    "f7_has_timestamp_or_asof_selector": any(
        token in module for token in (b"as_of", b"timestamp", b"version_selector")),
}
print(json.dumps(result, indent=2, sort_keys=True))
