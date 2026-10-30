#!/usr/bin/env python3
"""First code-level evidence for five disjoint Pyat S1-S5 branch cohorts.

Does not run/import candidate code, infer science, select a successor, or merge.
Exact code-symbol equivalence is a narrow machine observation, not human merit.
"""
from __future__ import annotations

import argparse
import ast
import collections
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location("pyat_s0", HERE / "12_s0_exact_tree_blob_index.py")
s0 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = s0
spec.loader.exec_module(s0)
CODE_SUFFIXES = (".py", ".js", ".ts", ".jsx", ".tsx")
CODE_DIRS = ("rawlsing_next/", "src/", "scripts/", "data/ddm_build_copy/")
MAX_BLOB = 4_000_000


def hashlib_text(t):
    return hashlib.sha256(t.encode("utf-8", errors="replace")).hexdigest()


def shape(node, rename=False, strip_docs=False):
    n = copy.deepcopy(node)
    if rename and hasattr(n, "name"):
        n.name = "_symbol_"
    if strip_docs and hasattr(n, "body") and n.body and isinstance(n.body[0], ast.Expr):
        first = n.body[0].value
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            n.body.pop(0)
    return ast.dump(n, annotate_fields=True, include_attributes=False)


def read_symbols(blob_id, path, cache, problems):
    if not blob_id:
        return {"state": "NO_BLOB", "symbols": []}
    if blob_id in cache:
        return cache[blob_id]
    raw = s0.git("cat-file", "blob", blob_id, check=False)
    if raw is None:
        result = {"state": "BLOB_UNAVAILABLE", "symbols": []}
        problems.append({"blob": blob_id, "path": path, "reason": "CAT_FILE_FAIL"})
    elif len(raw) > MAX_BLOB:
        result = {"state": "OVERSIZE_SKIP", "size": len(raw), "symbols": []}
        problems.append({"blob": blob_id, "path": path, "reason": "OVERSIZE"})
    elif path.endswith(".py"):
        try:
            tree = ast.parse(raw.decode("utf-8-sig"))
            found = []
            def walk(items, prefix=""):
                for node in items:
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        q = prefix + node.name
                        found.append({
                            "symbol": q, "kind": type(node).__name__,
                            "line": node.lineno,
                            "ast_exact_sha256": hashlib_text(shape(node)),
                            "ast_no_identifier_or_doc_sha256": hashlib_text(
                                shape(node, rename=True, strip_docs=True)),
                        })
                        if isinstance(node, ast.ClassDef):
                            walk(node.body, q + ".")
            walk(tree.body)
            result = {"state": "PARSED_PYTHON_AST", "symbols": found,
                      "sha256": hashlib.sha256(raw).hexdigest()}
        except (SyntaxError, UnicodeDecodeError, ValueError) as exc:
            result = {"state": "PYTHON_PARSE_FAILURE", "symbols": [], "detail": str(exc)[:240]}
            problems.append({"blob": blob_id, "path": path, "reason": str(exc)[:200]})
    else:
        result = {"state": "NON_PYTHON_SOURCE_UNPARSED", "symbols": [],
                  "sha256": hashlib.sha256(raw).hexdigest()}
    cache[blob_id] = result
    return result


def compare_one(path, candidate_blob, current_blob, cache, problems):
    cand = read_symbols(candidate_blob, path, cache, problems)
    curr = read_symbols(current_blob, path, cache, problems) if current_blob else {"state": "NO_CURRENT_PATH", "symbols": []}
    by_name = {s["symbol"]: s for s in curr["symbols"]}
    symbols = []
    for sym in cand["symbols"]:
        sibling = by_name.get(sym["symbol"])
        grade = (
            "SYMBOL_CURRENT_PATH_ABSENT" if not current_blob else
            "SYMBOL_NOT_PRESENT_AT_CURRENT_PATH" if sibling is None else
            "SAME_EXACT_AST_AT_CURRENT_PATH" if sibling["ast_exact_sha256"] == sym["ast_exact_sha256"] else
            "SAME_AST_IGNORING_NAME_AND_DOCSTRING" if sibling["ast_no_identifier_or_doc_sha256"] == sym["ast_no_identifier_or_doc_sha256"] else
            "DIFFERENT_AST__ADJUDICATE"
        )
        symbols.append({**sym, "same_path_grade": grade,
                        "current_ast_exact_sha256": sibling["ast_exact_sha256"] if sibling else None})
    return {"candidate": cand, "current": curr, "symbols": symbols}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", choices=s0.GROUPS, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    manifest = s0.json_file(s0.SCOPE / "11_00_SCOPED_HEAD_ROSTER_MANIFEST.json")
    entry = next(v for v in manifest["rosters"] if v["worker"] == args.shard)
    roster_path = ROOT / entry["path"]
    if s0.git("hash-object", str(roster_path)).decode().strip() != entry["git_blob_sha"]:
        raise RuntimeError("ROSTER_CUSTODY_FAILURE")
    roster = s0.json_file(roster_path)["branch_heads"]
    if len(roster) != entry["branches"]:
        raise RuntimeError("ROSTER_COUNT_FAILURE")
    receiving = s0.sha_ref(s0.BASE)
    current = s0.blobs_at(receiving)
    missing = set(s0.fetch_sha_batch(sorted({x["tip_sha"] for x in roster})))
    cache, variants, errors = {}, {}, []
    counts = collections.Counter()
    branch_rows = []
    for original in roster:
        tip = original["tip_sha"]
        item = {"branch": original["branch"], "tip": tip,
                "tip_date_not_creation_date": original["committer_time_utc"],
                "current_receiving_sha": receiving, "cohort": original["cohort_date_status"],
                "changed_source_paths": [], "changed_test_paths": [], "changed_return_roots": [],
                "historical_merit": "NOT_JUDGED", "reviewer_verdict": "NOT_JUDGED",
                "functional_equivalence_or_successor": "NOT_JUDGED",
                "whole_codebase_integratability": "NOT_JUDGED",
                "no_code_execution": True}
        try:
            if tip in missing:
                raise RuntimeError("PINNED_TIP_MISSING")
            tree = s0.git("rev-parse", tip + "^{tree}").decode().strip()
            if tree != original["tree_sha"]:
                raise RuntimeError("TREE_CUSTODY_FAILURE")
            merge_base = s0.git("merge-base", receiving, tip)
            if not merge_base or not merge_base.strip():
                raise RuntimeError("NO_MERGE_BASE")
            mb = merge_base.decode().strip()
            item["merge_base"] = mb
            delta = s0.read_diff(mb, tip, current)
            return_roots = set()
            for f in delta:
                path = f["path"]
                if path.startswith("WORKER_RETURNS/"):
                    parts = path.split("/")
                    if len(parts) > 2:
                        return_roots.add("/".join(parts[:2]))
                if not path.startswith(CODE_DIRS) or not path.endswith(CODE_SUFFIXES):
                    continue
                if f["status"] == "D":
                    # A deleted source can still be an important negative/supersession.
                    target = {"path": path, "status": "DELETED_IN_BRANCH",
                              "blob": None, "current_blob": f["current_blob"]}
                else:
                    blob = f["candidate_blob"]
                    target = {"path": path, "status": f["path_blob_grain"],
                              "blob": blob, "current_blob": f["current_blob"]}
                    key = blob + "|" + path
                    if key not in variants:
                        variants[key] = {"variant_key": key, "path": path,
                                         "historical_blob": blob, "current_blob": f["current_blob"],
                                         **compare_one(path, blob, f["current_blob"], cache, errors)}
                    target["variant_key"] = key
                if "/tests/" in path or path.split("/")[-1].startswith("test_"):
                    item["changed_test_paths"].append(target)
                else:
                    item["changed_source_paths"].append(target)
                counts[f["path_blob_grain"]] += 1
            item["changed_return_roots"] = sorted(return_roots)
            item["state"] = "CODE_AND_RETURN_PATHS_INDEXED__NOT_MERIT_ASSESSED"
        except Exception as exc:
            item["state"] = "INCOMPLETE"
            item["error"] = str(exc)[:650]
            errors.append({"branch": item["branch"], "reason": item["error"]})
        branch_rows.append(item)
    args.out.mkdir(parents=True, exist_ok=True)
    prefix = args.shard
    bp = args.out / (prefix + "_branch_code_return_index.jsonl")
    vp = args.out / (prefix + "_function_variant_index.jsonl")
    for path, values in [(bp, branch_rows), (vp, sorted(variants.values(), key=lambda x: x["variant_key"]))]:
        with path.open("w", encoding="utf-8") as fd:
            for row in values:
                fd.write(json.dumps(row, sort_keys=True, ensure_ascii=True) + "\n")
    summary = {"schema": "PYAT_S1_S5_MACHINE_SOURCE_FUNCTION_CANDIDATES@1",
               "shard": prefix, "receiving_sha": receiving, "roster_blob": entry["git_blob_sha"],
               "branch_total": len(branch_rows), "branch_indexed": sum(x["state"] != "INCOMPLETE" for x in branch_rows),
               "branch_errors": len([x for x in branch_rows if x["state"] == "INCOMPLETE"]),
               "changed_code_path_occurrences": sum(len(x["changed_source_paths"]) + len(x["changed_test_paths"]) for x in branch_rows),
               "unique_code_variants": len(variants),
               "candidate_python_symbols": sum(len(x["symbols"]) for x in variants.values()),
               "path_grades": dict(counts), "symbol_parse_errors": len(errors),
               "branch_index_sha256": hashlib.sha256(bp.read_bytes()).hexdigest(),
               "variant_index_sha256": hashlib.sha256(vp.read_bytes()).hexdigest(),
               "limitations": [
                   "NO branch execution, source-native data, original scientific issuance or semantic authority",
                   "All diff entries are merge-base..tip; shared ancestral/retained changes may repeat",
                   "Exact AST equality is code identity at one path, not provenance or adoption",
                   "No cross-filename or callgraph functional equivalence adjudication",
                   "Review and return root names are evidence locators, NOT reviewer acceptance",
                   "No trash/replaced/recover/integrate decision without qualified independent investigation",
                   "Tip date is not original branch creation date"
               ]}
    (args.out / (prefix + "_coverage.json")).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if summary["branch_errors"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
