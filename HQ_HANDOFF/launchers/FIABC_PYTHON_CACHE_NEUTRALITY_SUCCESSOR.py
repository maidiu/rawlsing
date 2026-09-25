#!/usr/bin/env python3
"""Successor-only FIABC Python bytecode-cache neutrality control.

This module does not authorize current protected execution.  It defines the
source-free C0 environment and receipts required if HQ adopts a future law that
normalizes Python bytecode-cache participation for BOTH joined and split
candidate execution.

It never imports candidate owners, opens survey sources, decodes data, or
launches candidate processes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any, Mapping

SCHEMA = "RAWLSING_FIABC_PYTHON_CACHE_NEUTRALITY_SUCCESSOR@1.0.0"
EXPECTED_CURRENT_PROTECTED_HEAD = "3d8f2ad62600b6777dcb23a28404a067502e77a0"
PREFIX_REL = Path("court") / "_python_cache_neutral_prefix"
DONT_WRITE_ENV = "PYTHONDONTWRITEBYTECODE"
PYCACHE_PREFIX_ENV = "PYTHONPYCACHEPREFIX"
ADOPTION_ENV = "RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR"


class CacheNeutralityError(RuntimeError):
    pass


def _canon(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
    ).encode("utf-8")


def _hash(value: Any) -> str:
    return hashlib.sha256(_canon(value)).hexdigest()


def _entries(root: Path) -> tuple[str, ...]:
    if not root.exists():
        return ()
    return tuple(p.relative_to(root).as_posix() for p in sorted(root.rglob("*")))


def cache_prefix(work_root: Path) -> Path:
    return (Path(work_root).resolve() / PREFIX_REL).resolve()


def prepare_environment(work_root: Path) -> Mapping[str, str]:
    """Prepare an empty redirected cache namespace without importing any project code."""
    prefix = cache_prefix(work_root)
    if _entries(prefix):
        raise CacheNeutralityError(
            f"cache-neutral prefix is not empty before candidate entry: {_entries(prefix)!r}"
        )
    prefix.mkdir(parents=True, exist_ok=True)
    return {
        DONT_WRITE_ENV: "1",
        PYCACHE_PREFIX_ENV: str(prefix),
        ADOPTION_ENV: "1",
    }


def assert_prefix_empty(work_root: Path) -> None:
    prefix = cache_prefix(work_root)
    entries = _entries(prefix)
    if entries:
        raise CacheNeutralityError(
            f"cache-neutral prefix acquired filesystem entries during candidate execution: {entries!r}"
        )


def assert_runtime_configuration(work_root: Path) -> Mapping[str, Any]:
    """Verify the interpreter is actually running under the successor cache law."""
    prefix = cache_prefix(work_root)
    observed_prefix = None if sys.pycache_prefix is None else str(Path(sys.pycache_prefix).resolve())
    if sys.dont_write_bytecode is not True:
        raise CacheNeutralityError("sys.dont_write_bytecode is not true")
    if observed_prefix != str(prefix):
        raise CacheNeutralityError(
            f"sys.pycache_prefix drift: expected {prefix}, got {observed_prefix}"
        )
    if os.environ.get(DONT_WRITE_ENV) != "1":
        raise CacheNeutralityError("PYTHONDONTWRITEBYTECODE environment binding absent")
    if os.environ.get(PYCACHE_PREFIX_ENV) != str(prefix):
        raise CacheNeutralityError("PYTHONPYCACHEPREFIX environment binding drift")
    if os.environ.get(ADOPTION_ENV) != "1":
        raise CacheNeutralityError("cache-neutral successor adoption marker absent")
    assert_prefix_empty(work_root)
    return {
        "dont_write_bytecode": True,
        "pycache_prefix": str(prefix),
        "prefix_entry_inventory": [],
    }


def build_receipt(
    *,
    work_root: Path,
    scope: str,
    protected_head: str,
    joined_successor_identity: str | None,
) -> Mapping[str, Any]:
    if scope not in {"JOINED_SIX_CELL", "SPLIT_SOURCE_LOCAL"}:
        raise CacheNeutralityError(f"unknown cache-neutrality scope: {scope}")
    runtime = assert_runtime_configuration(work_root)
    payload = {
        "schema": SCHEMA,
        "status": "PASS__CACHE_NEUTRAL_RUNTIME_BOUND__NOT_BY_ITSELF_A_PARITY_ADMISSION",
        "scope": scope,
        "protected_execution_head": protected_head,
        "current_protected_reference_head": EXPECTED_CURRENT_PROTECTED_HEAD,
        "joined_successor_identity": joined_successor_identity,
        "joined_successor_adopted": joined_successor_identity is not None,
        "runtime": runtime,
        "law": {
            "ordinary_source_tree_pycache_must_be_ignored": True,
            "bytecode_cache_writes_disabled": True,
            "redirected_prefix_empty_before_candidate_entry": True,
            "redirected_prefix_must_remain_file_empty": True,
            "candidate_main_processes_covered": True,
            "candidate_descendant_processes_must_inherit_environment": True,
            "same_law_required_for_joined_and_split": True,
            "compileall_or_precompiled_cache_substitution_authorized": False,
        },
        "source_free": True,
        "raw_source_opened": False,
        "raw_source_hashed": False,
        "decoder_called": False,
        "candidate_process_launched_by_this_control": False,
        "candidate_output_created": False,
        "measurement_performed": False,
    }
    payload["receipt_identity"] = _hash(payload)
    return payload


def verify_receipt(
    document: Mapping[str, Any],
    *,
    expected_scope: str,
    require_joined_successor: bool,
) -> None:
    if document.get("schema") != SCHEMA:
        raise CacheNeutralityError("cache-neutrality receipt schema drift")
    identity = document.get("receipt_identity")
    material = {k: v for k, v in document.items() if k != "receipt_identity"}
    if identity != _hash(material):
        raise CacheNeutralityError("cache-neutrality receipt identity drift")
    if document.get("status") != "PASS__CACHE_NEUTRAL_RUNTIME_BOUND__NOT_BY_ITSELF_A_PARITY_ADMISSION":
        raise CacheNeutralityError("cache-neutrality receipt status drift")
    if document.get("scope") != expected_scope:
        raise CacheNeutralityError("cache-neutrality receipt scope drift")
    law = document.get("law")
    if not isinstance(law, Mapping) or any(
        law.get(key) is not True
        for key in (
            "ordinary_source_tree_pycache_must_be_ignored",
            "bytecode_cache_writes_disabled",
            "redirected_prefix_empty_before_candidate_entry",
            "redirected_prefix_must_remain_file_empty",
            "candidate_main_processes_covered",
            "candidate_descendant_processes_must_inherit_environment",
            "same_law_required_for_joined_and_split",
        )
    ):
        raise CacheNeutralityError("cache-neutrality law is incomplete")
    if law.get("compileall_or_precompiled_cache_substitution_authorized") is not False:
        raise CacheNeutralityError("precompiled-cache substitution was incorrectly authorized")
    if require_joined_successor and document.get("joined_successor_adopted") is not True:
        raise CacheNeutralityError(
            "split cache neutrality cannot admit parity before joined successor adoption"
        )


def _write(path: Path, doc: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("--work-root", type=Path, required=True)
    check = sub.add_parser("runtime-check")
    check.add_argument("--work-root", type=Path, required=True)
    receipt = sub.add_parser("receipt")
    receipt.add_argument("--work-root", type=Path, required=True)
    receipt.add_argument("--scope", choices=("JOINED_SIX_CELL", "SPLIT_SOURCE_LOCAL"), required=True)
    receipt.add_argument("--protected-head", required=True)
    receipt.add_argument("--joined-successor-identity")
    receipt.add_argument("--output", type=Path, required=True)
    return p


def main() -> int:
    args = _parser().parse_args()
    if args.command == "prepare":
        print(json.dumps(prepare_environment(args.work_root), sort_keys=True))
        return 0
    if args.command == "runtime-check":
        print(json.dumps(assert_runtime_configuration(args.work_root), sort_keys=True))
        return 0
    doc = build_receipt(
        work_root=args.work_root,
        scope=args.scope,
        protected_head=args.protected_head,
        joined_successor_identity=args.joined_successor_identity,
    )
    _write(args.output, doc)
    print(json.dumps(doc, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
