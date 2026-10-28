"""Capture the existing RM40-R2 named symbols from pinned source without importing it."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path

MATRIX_SHA = "e332787287b92b6efdfdb63eafd2fc68a69327807be310162b6e97f02f2cce0e"
RUN_SHA = "f2c1bbcbbdd39dda37e1334e035383535a8c04bfa6feb2d8253687576805eb60"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def capture(source: Path, matrix: Path) -> dict:
    data = matrix.read_bytes()
    if digest(data) != MATRIX_SHA:
        raise ValueError("RM40_R2_MATRIX_SOURCE_CHANGED")
    old = json.loads(data)
    rows = []
    verified = {}
    for row in old["rows"]:
        symbols = []
        for name in map(str.strip, row["symbols"].split(";")):
            matches = []
            for entry in row["source_files"]:
                path = source / entry["path"]
                if not path.is_file():
                    continue
                raw = path.read_bytes()
                if digest(raw) != entry["sha256"]:
                    raise ValueError("HISTORIC_SOURCE_HASH_CHANGED:" + entry["path"])
                verified[entry["path"]] = entry["sha256"]
                if path.suffix == ".py":
                    for node in ast.walk(ast.parse(raw)):
                        kind = None
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == name:
                            kind = "class" if isinstance(node, ast.ClassDef) else "callable_definition"
                        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name:
                            kind = "annotated_field"
                        elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
                            kind = "assignment"
                        elif isinstance(node, ast.ImportFrom) and any((a.asname or a.name) == name for a in node.names):
                            kind = "import_alias"
                        if kind:
                            matches.append({"name": name, "kind": kind, "path": entry["path"], "line": node.lineno,
                                            "sha256": entry["sha256"], "role": row["retained_invariant"],
                                            "historical_hazard": row["historical_hazard"]})
                elif name == "derived_indices_schedule" and entry["path"] == "v3/v3_yearly_step_order.yaml":
                    for line, text in enumerate(raw.decode().splitlines(), 1):
                        if text == "derived_indices_schedule:":
                            matches.append({"name": name, "kind": "config_key", "path": entry["path"], "line": line,
                                            "sha256": entry["sha256"], "role": "historical derived-index scheduling configuration"})
            if not matches:
                raise ValueError("NAMED_SYMBOL_NOT_LOCATED:" + row["m"] + ":" + name)
            symbols.extend(matches)
        rows.append({"M": row["m"], "symbols": symbols,
                     "current_adapter": "TO_BUILD", "proposed_adapter": row["new_adapter"],
                     "test_id": row["test_id"], "test_status": "TEST_SPEC_ONLY",
                     "source_status": "HISTORICAL_SOURCE_IDENTIFIED_NOT_NATIVE_ISSUANCE"})
    run = source / "v3/run_and_print.py"
    if digest(run.read_bytes()) != RUN_SHA:
        raise ValueError("RUN_AND_PRINT_SOURCE_CHANGED")
    calls = {n.lineno: n for n in ast.walk(ast.parse(run.read_bytes())) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    for mid, line, name in [("M25", 123, "run_one_year"), ("M27", 139, "run_llm_band_year"), ("M37", 152, "render_year")]:
        if calls[line].func.id != name:
            raise ValueError("CALLSITE_CHANGED:" + mid)
        next(r for r in rows if r["M"] == mid)["symbols"].append({"name": name, "kind": "callsite", "path": "v3/run_and_print.py",
            "line": line, "sha256": RUN_SHA, "role": "final present-state render" if mid == "M37" else "historical yearly simulation callsite"})
    assert len(rows) == 40 and len({r["M"] for r in rows}) == 40
    return {"schema": "RM40_R3_LITERAL_SOURCE_SYMBOL_ADDENDUM_V1", "grade": "READ_ONLY_AST_SOURCE_PREPARATION",
            "matrix_sha256": MATRIX_SHA, "source_cut": old["source_cut"], "rows": rows,
            "named_symbols": sum(len(r["symbols"]) for r in rows),
            "source_files_verified_for_this_capture": len(verified) + ("v3/run_and_print.py" not in verified),
            "historical_matrix_unchanged": {"cells": 480, "marks": 124, "unmarked": 356},
            "not_claimed": ["RM40_R3_full_return", "executable_F1_F2_F3_adapters", "current_live_consumers", "native_science", "owner_source_permission"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = capture(args.source_root, args.matrix)
    encoded = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if args.output.read_text() != encoded:
            raise SystemExit("SYMBOL_REGISTRY_MISMATCH")
    else:
        args.output.write_text(encoded)
    print(json.dumps({"rows": len(result["rows"]), "symbols": result["named_symbols"], "source_only": True, "check": "PASS"}))
