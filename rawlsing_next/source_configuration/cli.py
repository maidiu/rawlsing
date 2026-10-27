"""Command-line delivery surface for the R157 source-configuration library."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from .library import (
    INDEX_PATH,
    ROOT,
    SQLITE_PATH,
    SourceConfigLibrary,
    SourceLibraryError,
    SourceNotPrepared,
    build_index,
)


def _print(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def _library(args) -> SourceConfigLibrary:
    index = Path(args.index) if args.index else INDEX_PATH
    return SourceConfigLibrary(index_path=index, root=Path(args.root))


def _display_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def cmd_build_index(args) -> int:
    index = build_index(
        index_path=Path(args.index) if args.index else INDEX_PATH,
        sqlite_path=Path(args.sqlite) if args.sqlite else SQLITE_PATH,
    )
    root = Path(args.root)
    _print({
        "index": _display_path(Path(args.index) if args.index else INDEX_PATH, root),
        "sqlite": _display_path(Path(args.sqlite) if args.sqlite else SQLITE_PATH, root),
        "counts": index["counts"],
        "pending_source_ids": index["pending_source_ids"],
    })
    return 0


def cmd_status(args) -> int:
    library = _library(args)
    _print({
        "index": _display_path(library.index_path, library.root),
        "plan_seal": library.document["plan_seal"],
        "baseline": library.document["baseline"],
        "counts": library.document["counts"],
        "pending_source_ids": library.pending_source_ids(),
    })
    return 0


def cmd_list(args) -> int:
    library = _library(args)
    rows = []
    for source_id in library.source_ids():
        row = library.records[source_id]
        rows.append({
            "source_id": source_id,
            "family": row["family"],
            "wave": row["wave"],
            "lane": row["lane"],
            "status": row["status"],
            "available": row["status"] == "AVAILABLE_NATIVE_RECEIPT",
            "release_hash": (row.get("release_ref") or {}).get("content_hash"),
        })
    _print(rows)
    return 0


def cmd_show(args) -> int:
    library = _library(args)
    row = library.records.get(args.source_id)
    if row is None:
        raise SourceLibraryError(f"unknown source {args.source_id}")
    _print(row)
    return 0


def cmd_validate(args) -> int:
    library = _library(args)
    result = library.validate_source(args.source_id)
    if args.native:
        release = library.build_fixture_release(args.source_id)
        result["native_call"] = {
            "callable": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
            "release_ref": release.release_ref.as_dict(),
            "semantic_release_hash": release.semantic_release_hash,
        }
    _print(result)
    return 0 if result["passed"] else 1


def cmd_fixture_call(args) -> int:
    library = _library(args)
    release = library.build_fixture_release(args.source_id)
    row = library.record(args.source_id)
    _print({
        "source_id": args.source_id,
        "callable": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
        "original_config_path": row["original_config_path"],
        "original_config_file_sha256": row["original_config_file_sha256"],
        "fixture_config_path": row["fixture_config_path"],
        "fixture_path": row["fixture_path"],
        "fixture_source_sha256": row["fixture_source_sha256"],
        "native_results_path": row["native_results_path"],
        "release_ref": release.release_ref.as_dict(),
        "semantic_release_hash": release.semantic_release_hash,
        "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
        "public_object_count": len(release.public_objects),
        "m01_m18_coverage": {key: list(value) for key, value in release.m01_m18_coverage.items()},
        "source_read_performed": False,
        "original_workload_issued": False,
    })
    return 0


def cmd_native_results(args) -> int:
    library = _library(args)
    row = library.record(args.source_id)
    _print({
        "source_id": args.source_id,
        "native_results_path": row["native_results_path"],
        "native_results_file_sha256": row["native_results_file_sha256"],
        "release_ref": row["release_ref"],
    })
    return 0


def cmd_original_plan(args) -> int:
    library = _library(args)
    plan = library.original_plan(
        args.source_id,
        source_path=args.source_path,
        host=args.host,
        purpose=args.purpose,
        consumer_use=args.consumer_use,
        semantic_use_scope=args.semantic_scope,
        custody_locator_binding=args.custody_locator_binding,
    )
    _print(plan)
    return 0


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m rawlsing_next.source_configuration.cli",
                                description="R157 portable source-configuration registry and delivery commands")
    p.add_argument("--index", default=None, help="index JSON path (default: source_pre553_validation/integration/SOURCE_LIBRARY_INDEX.json)")
    p.add_argument("--root", default=str(ROOT), help="repository root (default: package root)")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("build-index", help="rebuild the portable index and SQLite lookup")
    s.add_argument("--sqlite", default=None)
    s.set_defaults(func=cmd_build_index)

    s = sub.add_parser("status", help="show current availability against the 35-source baseline")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("list", help="list all 35 source slots and readiness")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("show", help="show one source record")
    s.add_argument("source_id")
    s.set_defaults(func=cmd_show)

    s = sub.add_parser("validate", help="validate original/fixture identity and coverage")
    s.add_argument("source_id")
    s.add_argument("--native", action="store_true", help="also run the actual fixture native validator")
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser("fixture-call", help="run the actual existing native C11 validator on the configured fixture")
    s.add_argument("source_id")
    s.set_defaults(func=cmd_fixture_call)

    s = sub.add_parser("native-results", help="show the recorded native receipt provenance")
    s.add_argument("source_id")
    s.set_defaults(func=cmd_native_results)

    s = sub.add_parser("original-plan", help="emit a separately authorized original-read plan without opening source bytes")
    s.add_argument("source_id")
    s.add_argument("--source-path", required=True)
    s.add_argument("--host", required=True)
    s.add_argument("--purpose", required=True)
    s.add_argument("--consumer-use", required=True)
    s.add_argument("--semantic-scope", action="append", required=True)
    s.add_argument("--custody-locator-binding", default=None)
    s.set_defaults(func=cmd_original_plan)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (SourceLibraryError, SourceNotPrepared, FileNotFoundError, ValueError) as exc:
        print(json.dumps({"error": type(exc).__name__, "message": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
