#!/usr/bin/env python3
"""Static, non-executing V550 audit of a hash-pinned repository snapshot.

Usage: python rawlsing_scan/scan_v550.py
No historic source bytes are loaded, and no V550 module is imported/executed.
This scanner is intentionally broad: it inventories syntactic calls, leaving
semantic authority and actual runtime path choice for separate qualification.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIR = ROOT / "data" / "ddm_build_copy"
OUT = ROOT / "generated"
HIST = "9ba4764bef551b1ce498e5772d60b73d69337d4b"
CURRENT = "fce43498e16e4709f3c9801e8717f0fdae18126a"
ENTRY = {
    "build_determinicity_wave_shard_v550",
    "build_determinicity_repository_v550",
    "build_response_option_map_v550",
    "build_question_use_contract_v550",
    "build_v550_source_structure_population",
    "build_all_survey_overlays",
    "build_wave_overlays",
    "build_directionality_authority",
    "build_arab_barometer_directionality_authority",
    "check_v550_wave_readiness",
    "plan_v550_wave_shards",
    "run_v550_shards_from_plan",
    "merge_determinicity_shards_v550",
    "rebuild_v550_bridge_from_checkpoints",
}
LOAD_NAMES = {
    "load_family_overlay", "load_question_relation_authority",
    "load_question_structure_register", "load_scope_manifest",
    "build_response_option_map", "load_response_semantics_authority",
    "resolve_question_relation_authority", "read_table_any",
    "load_raw_response_semantics", "load_joint_configuration_registry",
    "_build_authority_receipt", "build_question_use_contract",
    "build_question_use_contract_row", "build_v551_bridge_index_for_table",
    "build_bridge_causal_summary", "build_response_authority_match_audit",
    "assert_response_authority_match_gate", "apply_question_relation_authority",
    "bind_governed_response_semantics_contracts", "response_semantics_contract_hash",
    "build_distribution_tables", "_load_response_option_map",
    "_prefetch_question_rows_by_country", "_prepare_v550_question_row_cache",
    "_harmonize_question_frame", "cached_query_frame", "load_cached_frame",
    "_build_index", "derive_legacy_latinobarometro_1995_residual",
    "match_source_structure_row", "resolve_shared_substrate_requirements",
    "canonicalize_shared_respondent_substrate",
    "write_shared_respondent_substrate_atomic",
}
IO_LEAVES = {
    "open", "read_csv", "read_parquet", "read_json", "read_excel",
    "read_sql", "read_sql_query", "read_sql_table", "read_text",
    "read_bytes", "load", "safe_load", "glob", "rglob", "iterdir",
    "connect", "execute", "executemany", "read_table", "read_dataset",
    "read_feather", "read_pickle", "to_parquet", "to_csv", "to_json",
    "write_text", "write_bytes", "dump", "safe_dump", "getenv",
    "get", "add_argument", "read_table_any", "load_dotenv",
    "read_jsonl", "fetchall", "query", "copy", "load_family_overlay",
}
SOURCE_LEAVES = {"getenv", "add_argument", "get"}
ASSET_RE = re.compile(
    r"(?:\.csv|\.json|\.jsonl|\.parquet|\.yaml|\.yml|\.db|\.duckdb|\.sqlite|\.txt|\.xlsx|\.sha256|\.tsv)$",
    re.I,
)


def name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return name(node.value) + "." + node.attr
    if isinstance(node, ast.Call):
        return name(node.func)
    return type(node).__name__


def unparse(node: ast.AST) -> str:
    try:
        return ast.unparse(node).replace("\n", " ")[:460]
    except Exception:
        return ""


def writes(path: Path, headings: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headings, delimiter="\t" if path.suffix == ".tsv" else ",", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


INDEX = json.loads((ROOT / "blob_index.json").read_text(encoding="utf-8"))
KNOWN = {item["path"]: item for item in INDEX["legacy"] + INDEX["current"]}
files = sorted(DIR.glob("*.py"))
trees = {}
source = {}
imports = defaultdict(set)
outside = defaultdict(set)
for file in files:
    module = file.stem
    text = file.read_text(encoding="utf-8")
    source[module] = text
    trees[module] = ast.parse(text, filename=str(file))
    for node in ast.walk(trees[module]):
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("data.ddm_build_copy."):
                imports[module].add(node.module.split(".")[-1])
            elif node.module and node.module.startswith("rawlsing_next"):
                outside[module].add(node.module)
            elif node.module and node.module.startswith("data."):
                outside[module].add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("data.ddm_build_copy."):
                    imports[module].add(alias.name.split(".")[-1])
                elif alias.name.startswith(("rawlsing_next", "data.")):
                    outside[module].add(alias.name)

seeds = set(ENTRY) | {
    p.stem for p in files if ("v550" in p.stem and "v550j" not in p.stem)
    or p.stem.startswith("ddm_v550")
}
queue = deque(sorted(seeds))
closure = set()
missing_modules = set()
while queue:
    module = queue.popleft()
    if module in closure:
        continue
    if module not in trees:
        missing_modules.add(module)
        continue
    closure.add(module)
    queue.extend(sorted(imports[module] - closure))


def walk_with_context(node: ast.AST, scope: tuple[str, ...] = ()):
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            yield from walk_with_context(child, scope + (child.name,))
        else:
            yield child, scope
            yield from walk_with_context(child, scope)


rows = []
assets = []
envs = []
counts = Counter()
for module in sorted(closure):
    for node, scope in walk_with_context(trees[module]):
        if isinstance(node, ast.Call):
            symbol = name(node.func)
            leaf = symbol.rsplit(".", 1)[-1]
            if leaf not in IO_LEAVES and leaf not in LOAD_NAMES:
                continue
            expr = unparse(node)
            # 'get' is noisy dictionary access: count separately, not legacy I/O.
            if leaf == "get" and not expr.startswith(("os.environ.get(", "environ.get(")):
                continue
            if leaf == "add_argument" and not expr.startswith("parser.add_argument"):
                continue
            typ = (
                "SELECTION" if leaf in SOURCE_LEAVES else
                "POTENTIAL_AUTHORITY_HELPER" if leaf in LOAD_NAMES else
                "IO_SITE"
            )
            if leaf in {"to_parquet", "to_csv", "to_json", "write_text", "write_bytes", "dump", "safe_dump", "copy"}:
                typ = "PERSISTENCE_OR_MUTATION"
            if leaf in {"execute", "executemany", "query", "fetchall"}:
                typ = "SQL_OR_DATA_OPERATION"
            provenance = (
                "ENTRYPOINT_CLI" if leaf == "add_argument" else
                "ENVIRONMENT_SELECTOR" if leaf in {"getenv", "get"} else
                "FILE_OR_DB_READ_CHECK_EXACT_EXPR" if typ in {"IO_SITE", "SQL_OR_DATA_OPERATION"} else
                "FILE_OR_DERIVED_OUTPUT_EXACT_EXPR" if typ == "PERSISTENCE_OR_MUTATION" else
                "AUTHORITY_TRANSFORM_CALL_SITE"
            )
            stage = ("V550_J_SHARED_DEPENDENCY" if "v550j" in module else "V550")
            row = {
                "row_id": f"V550-L1-{len(rows)+1:04d}",
                "version": stage,
                "stage": provenance,
                "producer_entry": module if module in seeds else "TRANSITIVE_IMPORT",
                "historical_module": f"data/ddm_build_copy/{module}.py",
                "symbol": ".".join(scope) or "<module>",
                "line": node.lineno,
                "historical_sha": HIST,
                "call_expression": expr,
                "call_kind": typ,
                "source_authority_path": "DYNAMIC_EXPRESSION:"+expr if typ!="PERSISTENCE_OR_MUTATION" else "NOT_INPUT_OUTPUT_WRITE",
                "source_file_byte_sha256": "UNVERIFIED_RUNTIME_BYTES",
                "grain": "SOURCE_WAVE_COUNTRY_QUESTION_OR_RESPONSE_AS_EXPRESSION",
                "accepted_status": "UNVERIFIED_SOURCE_AUTHORITY_NOT_PROMOTED",
                "cli_env_default_selection": expr if typ=="SELECTION" else "SEE_EXECUTABLE_PARSE_ARGS_AND_HELPER_DEFAULTS",
                "authority_role": "IO_OR_TRANSFORM_POTENTIAL_CHECK" if typ!="PERSISTENCE_OR_MUTATION" else "DERIVED_PERSISTENCE",
                "semantic_transformation": ("DIRECT_EXACT_CALL_EXPRESSION: "+expr if typ=="POTENTIAL_AUTHORITY_HELPER" else "SOURCE_CODE_SITE_NO_RUNTIME_VALUE_PROOF"),
                "typed_negative_semantics": "STATIC_NO_RUNTIME_BRANCH_EXERCISE",
                "output_persist_cache": expr if typ=="PERSISTENCE_OR_MUTATION" else "TRACE_ENCLOSING_SYMBOL_FOR_OUTPUT",
                "later_actual_reader": "NEEDS_FULL_DATAFLOW_TRACE",
                "current_pre553_successor": "UNBOUND / HOLD",
                "current_first_consumer": "UNBOUND / HOLD",
                "preservation_replay_evidence": "S0_STATIC_ONLY",
                "dynamic_or_mutation_test": "NOT_RUN_NO_S2_NATIVE_ACCESS",
            }
            rows.append(row)
            counts[typ] += 1
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
            if ASSET_RE.search(value) and len(value) < 300:
                assets.append({
                    "module": f"data/ddm_build_copy/{module}.py",
                    "line": node.lineno,
                    "literal": value,
                    "owner_symbol": ".".join(scope) or "<module>",
                })
        if isinstance(node, ast.Subscript) and name(node.value) in {"os.environ", "environ"}:
            envs.append((module, node.lineno, unparse(node)))

OUT.mkdir(exist_ok=True)
writes(OUT / "02_LEGACY_CALLSITES.csv", list(rows[0]), rows)
writes(OUT / "ASSET_LITERALS.tsv", ["module", "line", "literal", "owner_symbol"], assets)
scan_rows = []
for file in [*files, *sorted((ROOT/"rawlsing_next").glob("*.py"))]:
    module = file.stem
    is_legacy = file.parent == DIR
    prefix = "data/ddm_build_copy" if is_legacy else "rawlsing_next"
    repo_path = f"{prefix}/{file.name}"
    expected = KNOWN.get(repo_path, {})
    full_bytes = file.read_bytes()
    original_bytes = full_bytes[:expected["size"]] if expected.get("size") is not None else full_bytes
    computed_blob_sha = hashlib.sha1(
        b"blob "+str(len(original_bytes)).encode("ascii")+b"\0"+original_bytes
    ).hexdigest()
    sha_valid = bool(expected.get("blob_sha") == computed_blob_sha and len(original_bytes) == expected.get("size"))
    scan_rows.append({
        "path": repo_path,
        "scan_status": ("AST_SCANNED_CLOSURE" if module in closure else "AST_SCANNED_OUT_OF_CLOSURE") if is_legacy else "CURRENT_PYTHON_LITERAL_AND_SYMBOL_SEARCH",
        "file_bytes": len(original_bytes),
        "git_blob_sha1": expected.get("blob_sha", "NOT_IN_INDEX"),
        "file_byte_sha256": hashlib.sha256(original_bytes).hexdigest(),
        "git_blob_exact_verified": sha_valid,
        "historical_commit": HIST,
        "protected_commit": CURRENT,
        "reachable_from": ("V550_ENTRY_OR_DDM_V550" if module in closure else "NO_STATIC_IMPORT_EDGE_FROM_SEEDS") if is_legacy else "CURRENT_SYMBOL_SEARCH_NOT_PROVEN_FIRST_CONSUMER",
        "direct_ddm_imports": ";".join(sorted(imports[module])) if is_legacy else "NOT_ANALYZED_CURRENT_IMPORT_GRAPH",
        "external_data_imports": ";".join(sorted(outside[module])) if is_legacy else "NOT_ANALYZED_CURRENT_IMPORT_GRAPH",
        "callsite_rows": sum(r["historical_module"].endswith("/"+file.name) for r in rows),
    })
writes(OUT / "01_SCANNED_FILES.tsv", list(scan_rows[0]), scan_rows)
summary = {
    "files_ast_scanned": len(files),
    "closure_modules": len(closure),
    "nonclosure_modules": len(files) - len(closure),
    "missing_import_modules": sorted(missing_modules),
    "external_import_modules": {k: sorted(v) for k, v in outside.items() if k in closure},
    "callsite_rows": len(rows),
    "callsite_types": dict(counts),
    "literal_asset_ref_count": len(assets),
    "env_subscript_count": len(envs),
    "seeds": sorted(seeds),
    "closure": sorted(closure),
    "dynamic_imports_not_resolved": True,
    "foreign_imports_not_ast_scanned": True,
    "native_io_not_executed": True,
    "source_files_git_sha_verified": sum(x["git_blob_exact_verified"] for x in scan_rows),
    "source_files_git_sha_unverified": [x["path"] for x in scan_rows if not x["git_blob_exact_verified"]],
    "source_file_universe_size": len(scan_rows),
    "current_root_python_files_scanned": len(list((ROOT/"rawlsing_next").glob("*.py"))),
}
(OUT / "SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps({k:v for k,v in summary.items() if k not in ("seeds", "closure", "external_import_modules")}, indent=2))
