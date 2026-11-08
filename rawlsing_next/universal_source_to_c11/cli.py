"""Command-line delivery surface for universal source-to-C11."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from .cold_restore import cold_restore
from .consumer import receive_all, receive_fixture_release
from .ledger import build_ledger
from .negative import run_negative_suite
from .provenance import current_owner_abi, imported_cut_manifest, verify_imported_cut
from .registry import UniversalSourceRegistry


def _print(value: Any, output: str | None) -> None:
    text = json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True)
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text + "\n", encoding="utf-8")
    print(text)


def _registry(args) -> UniversalSourceRegistry:
    return UniversalSourceRegistry(index_path=args.index) if args.index else UniversalSourceRegistry()


def cmd_status(args) -> int:
    registry = _registry(args)
    ledger = build_ledger(registry)
    _print({
        "source_scope": ledger["source_scope"],
        "sources": ledger["totals"]["sources"],
        "physical_slots": ledger["totals"]["physical_slots"],
        "original_items": ledger["totals"]["original_items"],
        "exact_relation_joins": ledger["totals"]["exact_relation_joins"],
        "unmatched_relation_ids": ledger["totals"]["unmatched_relation_ids"],
        "held_slots": ledger["totals"]["held_slots"],
        "fixture_releases": ledger["totals"]["fixture_releases"],
        "not_run": ledger["totals"]["not_run"],
        "fixture_only": ledger["totals"]["fixture_only"],
        "original_source_execution": ledger["original_source_execution"],
        "goal_complete": ledger["goal_complete"],
    }, args.output)
    return 0


def cmd_ledger(args) -> int:
    _print(build_ledger(_registry(args)), args.output)
    return 0


def cmd_prove(args) -> int:
    receipt = receive_fixture_release(_registry(args), args.source_id)
    _print(receipt.as_dict(), args.output)
    return 0


def cmd_prove_all(args) -> int:
    registry = _registry(args)
    receipts = receive_all(registry)
    payload = {
        "schema": "PYAT_777_UNIVERSAL_SOURCE_TO_C11_RECEIPTS@1.0.0",
        "source_count": len(receipts),
        "all_accepted": all(receipt.ingest_accepted for receipt in receipts),
        "all_match_recorded_receipt": all(
            receipt.release_ref["content_hash"]
            == (registry.slot(receipt.source_id).index_row.get("release_ref") or {}).get("content_hash")
            for receipt in receipts
        ),
        "original_source_execution": "NOT_RUN",
        "source_read_performed": False,
        "receipts": [receipt.as_dict() for receipt in receipts],
    }
    _print(payload, args.output)
    return 0 if payload["all_accepted"] and payload["all_match_recorded_receipt"] else 1


def cmd_cold_restore(args) -> int:
    result = cold_restore(args.source_id)
    _print(result, args.output)
    return 0 if result["ok"] else 1


def cmd_negative(args) -> int:
    result = run_negative_suite(_registry(args))
    _print(result, args.output)
    return 0 if result["passed"] else 1


def cmd_owner_abi(args) -> int:
    _print(current_owner_abi(), args.output)
    return 0


def cmd_provenance(args) -> int:
    manifest = imported_cut_manifest()
    verification = verify_imported_cut(manifest)
    _print({
        "manifest": manifest,
        "verification": verification,
    }, args.output)
    return 0 if verification["ok"] else 1


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m rawlsing_next.universal_source_to_c11.cli",
        description="Universal 35-source configuration-to-current-C11 receive surface",
    )
    p.add_argument("--index", default=None, help="portable index JSON path")
    p.add_argument("--output", default=None, help="write the JSON payload to this path")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("status", help="show all-35 disposition and no-drop totals")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("ledger", help="emit the full 35-source configuration ledger")
    s.set_defaults(func=cmd_ledger)

    s = sub.add_parser("prove", help="receive one declared fixture release through current C11")
    s.add_argument("source_id")
    s.set_defaults(func=cmd_prove)

    s = sub.add_parser("prove-all", help="receive all 35 declared fixture releases through current C11")
    s.set_defaults(func=cmd_prove_all)

    s = sub.add_parser("cold-restore", help="cold load/rebuild from an empty cwd and receive one release")
    s.add_argument("source_id", nargs="?", default="SRC26")
    s.set_defaults(func=cmd_cold_restore)

    s = sub.add_parser("negative", help="run negative/refusal evidence")
    s.set_defaults(func=cmd_negative)

    s = sub.add_parser("owner-abi", help="record the current installed C11 owner/ABI")
    s.set_defaults(func=cmd_owner_abi)

    s = sub.add_parser("provenance", help="record and verify the exact R157 import cut")
    s.set_defaults(func=cmd_provenance)
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as exc:  # noqa: BLE001 - CLI must return a typed refusal
        print(json.dumps({"error": type(exc).__name__, "message": str(exc)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
