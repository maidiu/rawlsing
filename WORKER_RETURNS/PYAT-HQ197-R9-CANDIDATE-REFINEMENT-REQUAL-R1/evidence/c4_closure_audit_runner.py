#!/usr/bin/env python3
"""HQ197 — exact C4 closure audit for raw-path reader calls.

Closure source: the accepted C4C3 return's transitive_import_closure
(8ff40d37:WORKER_RETURNS/PYAT-C4C3-DARWIN-ANCHOR-RUNTIME-R1/02_ACTUAL_C4_CALL_PATH.json),
which declares module_count = 21.  The commission referred to a "23-module closure";
the accepted artifact says 21, and the count is stated twice in the freeze
(c4_import_closure_modules = 21 and transitive_import_closure.module_count = 21).
That discrepancy is reported rather than silently reconciled.

The candidate adds rawlsing_next/pre553_source_access_broker.py, which the decoder
now imports, so it is audited as part of the closure.

Audit question, per the commission: does any pyreadstat reader call inside the
closure receive a SOURCE PATH STRING?
"""
from __future__ import annotations

import ast
import json
import os
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = sys.argv[2]

DECLARED = [
    "rawlsing_next/pre553_physical_decoder.py",
    "rawlsing_next/pre553_source_backed_c11_facade.py",
    "rawlsing_next/pre553_empirical_possibility_provider.py",
    "rawlsing_next/pre553_analytical_composition.py",
    "rawlsing_next/source_backed_positioned_subject_possibility.py",
    "rawlsing_next/pre553_r5_codec.py",
    "rawlsing_next/pre553_c11_ingest.py",
    "rawlsing_next/pre553_c11_integrity.py",
    "rawlsing_next/pre553_c11_repository.py",
    "rawlsing_next/pre553_empirical_authority.py",
    "rawlsing_next/pre553_empirical_objects.py",
    "rawlsing_next/_pre553_query_common.py",
    "rawlsing_next/pre553_empirical_query.py",
    "rawlsing_next/pre553_physical_c11_bridge.py",
    "rawlsing_next/pre553_discovery_exact.py",
    "rawlsing_next/pre553_recursive_handoff.py",
    "rawlsing_next/pre553_runtime_context.py",
    "rawlsing_next/_pre553_query_eval.py",
    "rawlsing_next/_pre553_query_predicate.py",
    "rawlsing_next/pre553_runtime_composition.py",
    "rawlsing_next/pre553_runtime_authority.py",
]
CANDIDATE_ADDITION = "rawlsing_next/pre553_source_access_broker.py"
CLOSURE = DECLARED + [CANDIDATE_ADDITION]

READERS = {"read_sav", "read_dta", "read_file_in_chunks"}


def is_path_expr(node: ast.AST) -> bool:
    """True if the expression is a literal path / str(...) / os.fspath(...)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return True
    if isinstance(node, ast.JoinedStr):
        return True
    if isinstance(node, ast.Call):
        fn = node.func
        name = getattr(fn, "id", None) or getattr(fn, "attr", None)
        if name in ("str", "Path", "fspath"):
            return True
    return False


def _reader_of(expr: ast.AST) -> str | None:
    """Return the reader name if this expression selects a pyreadstat reader.

    Handles the direct attribute, and the ternary the broker actually uses:
        reader = self.pyreadstat.read_sav if kind == "SAV" else self.pyreadstat.read_dta
    which is an ast.IfExp, not an ast.Attribute.
    """
    if isinstance(expr, ast.Attribute) and expr.attr in READERS and _is_pyreadstat_base(expr.value):
        return expr.attr
    if isinstance(expr, ast.IfExp):
        return _reader_of(expr.body) or _reader_of(expr.orelse)
    return None


def _is_pyreadstat_base(node: ast.AST) -> bool:
    """True for `pyreadstat` and for `self.pyreadstat` / `<expr>.pyreadstat`."""
    if getattr(node, "id", None) == "pyreadstat":
        return True
    return getattr(node, "attr", None) == "pyreadstat"


def reader_aliases(tree: ast.AST) -> dict[str, str]:
    """Map local names bound to a pyreadstat reader, so indirect calls are seen.

    A naive scan for ``pyreadstat.read_sav(...)`` reports zero reader calls in a
    module that reaches the reader through a local variable, which would make the
    audit falsely clean. This resolves the aliases first.
    """
    aliases: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            value = node.value
            reader_name = _reader_of(value)
            if reader_name is None:
                continue
            for target in node.targets:
                if isinstance(target, ast.Name):
                    aliases[target.id] = reader_name
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            value = node.value
            reader_name = _reader_of(value) if value is not None else None
            if reader_name is not None:
                aliases[node.target.id] = reader_name
    return aliases


def audit_module(rel: str) -> dict:
    path = ROOT / rel
    entry = {"module": rel, "present": path.is_file(), "reader_calls": [],
             "raw_path_reader_calls": [], "opens_source_path": [],
             "reader_aliases": {}}
    if not entry["present"]:
        return entry
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    aliases = reader_aliases(tree)
    entry["reader_aliases"] = aliases

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            attr = getattr(fn, "attr", None)
            name = getattr(fn, "id", None)
            reader = _reader_of(fn)         # direct pyreadstat.<reader>(...)
            if reader is None and name in aliases:
                reader = aliases[name]       # reached through a local alias
            if reader is not None:
                first = node.args[0] if node.args else None
                raw = first is not None and is_path_expr(first)
                rec = {"line": node.lineno, "reader": reader,
                       "invoked_as": attr or name,
                       "first_arg_is_path_expression": raw,
                       "first_arg_source": ast.unparse(first)[:80] if first is not None else None}
                entry["reader_calls"].append(rec)
                if raw:
                    entry["raw_path_reader_calls"].append(rec)
        # any open(...) of a source path
        if isinstance(node, ast.Call):
            fn = node.func
            if getattr(fn, "id", None) == "open" or getattr(fn, "attr", None) == "open":
                entry["opens_source_path"].append({"line": node.lineno,
                                                   "arg": ast.unparse(node.args[0])[:80] if node.args else None})
    return entry


def main() -> int:
    modules = [audit_module(m) for m in CLOSURE]
    raw_hits = [m for m in modules if m["raw_path_reader_calls"]]
    all_readers = sum(len(m["reader_calls"]) for m in modules)
    missing = [m["module"] for m in modules if not m["present"]]

    # the WVS7 materializer is explicitly out of closure and out of terrain
    wvs = ROOT / "rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py"
    wvs_in_closure = "rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py" in CLOSURE

    report = {
        "schema": "HQ197_C4_CLOSURE_AUDIT@1.0.0",
        "CATEGORY": "C1_historical_expected_counts (closure list) + C2 static audit of current tree",
        "closure_source": "8ff40d37de69db2d8a6053a7c2242f481677f1a4:WORKER_RETURNS/PYAT-C4C3-DARWIN-ANCHOR-RUNTIME-R1/02_ACTUAL_C4_CALL_PATH.json .transitive_import_closure",
        "closure_count_discrepancy": {
            "commission_said": 23,
            "accepted_artifact_says": 21,
            "corroborated_in_freeze": "06_RUNTIME_READER_LANES_AND_RESOURCE_LAW.json declares c4_import_closure_modules = 21",
            "resolution": "the accepted artifact is used; the count 23 is not reproducible from any governed artifact and is reported rather than reconciled by inventing two modules",
            "candidate_addition": CANDIDATE_ADDITION,
            "audited_total": len(CLOSURE),
        },
        "audit_question": "does any pyreadstat reader call inside the C4 closure receive a source path string?",
        "verdict": "NO_RAW_PATH_READER_CALLS_IN_CLOSURE" if not raw_hits else "RAW_PATH_READER_CALLS_PRESENT",
        "modules_audited": len(modules),
        "modules_missing_from_worktree": missing,
        "total_reader_calls_in_closure": all_readers,
        "reader_calls_per_module": {m["module"]: len(m["reader_calls"]) for m in modules if m["reader_calls"]},
        "raw_path_reader_call_count": sum(len(m["raw_path_reader_calls"]) for m in modules),
        "modules_with_raw_path_reader_calls": [m["module"] for m in raw_hits],
        "source_path_open_sites_in_closure": {
            m["module"]: m["opens_source_path"] for m in modules if m["opens_source_path"]
        },
        "wvs7_projection_materializer": {
            "in_c4_closure": wvs_in_closure,
            "exists_in_tree": wvs.is_file(),
            "edited_by_this_lane": False,
            "note": "outside the C4 closure and outside this lane's write terrain; deliberately not audited as closure and not modified",
        },
        "per_module": modules,
    }
    Path(OUT).write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"modules audited          : {len(modules)}")
    print(f"reader calls in closure  : {all_readers}")
    print(f"RAW-PATH reader calls    : {report['raw_path_reader_call_count']}")
    print(f"verdict                  : {report['verdict']}")
    print(f"reader calls by module   : {json.dumps(report['reader_calls_per_module'])}")
    print(f"missing from worktree    : {missing}")
    print(f"wvs7 in closure          : {wvs_in_closure}")
    return 0 if not raw_hits else 1


if __name__ == "__main__":
    raise SystemExit(main())
