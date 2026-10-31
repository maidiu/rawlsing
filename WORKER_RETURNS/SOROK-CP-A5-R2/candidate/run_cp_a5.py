#!/usr/bin/env python3
"""CLI for the CP-A5 sourcefree multicontact life and read-only encounter."""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from bp2p4 import bootstrap

bootstrap.install()

from bp2p4 import reunion  # noqa: E402
from cp_a5.assertion import run_a5_assertion  # noqa: E402
from cp_a5.encounter import EncounterReader, render_encounter  # noqa: E402
from cp_a5.scenario import build_cp_life  # noqa: E402


def _print(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CP-A5 sourcefree encounter")
    parser.add_argument("--root", default="")
    parser.add_argument("--branch", default="root")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("scenario")
    sub.add_parser("verify")
    sub.add_parser("assert")
    sub.add_parser("view")
    encounter = sub.add_parser("encounter")
    encounter.add_argument("question")
    encounter.add_argument("--renderer", default="json",
                           choices=["json", "plain", "compact"])
    args = parser.parse_args(argv)
    root = Path(args.root) if args.root else Path(tempfile.mkdtemp(prefix="cp-a5-"))
    if args.command == "scenario":
        artifacts = reunion.build_fresh(root / "artifacts")
        _, trace = build_cp_life(root / "life", artifacts)
        _print(trace)
        return 0
    if args.command == "verify":
        with EncounterReader(root / "life", branch_id=args.branch) as reader:
            _print({"view": reader.view(), "c12": reader.c12_report})
        return 0
    if args.command == "assert":
        _print(run_a5_assertion(root / "life", branch_id=args.branch))
        return 0
    if args.command == "view":
        with EncounterReader(root / "life", branch_id=args.branch) as reader:
            _print(reader.view())
        return 0
    with EncounterReader(root / "life", branch_id=args.branch) as reader:
        answer = reader.ask(args.question)
        if args.renderer == "json":
            _print(answer)
        else:
            _print(render_encounter(reader.view(), args.renderer))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
