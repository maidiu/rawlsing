#!/usr/bin/env python3
"""CLI for FFX002-R2 Core-A EXACT_CONFIGURATION_SET production."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from data.ddm_build_copy.ddm_ffx_exact_configuration import (
    CoreAContractError,
    produce_exact_configuration_set,
    write_outputs,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compile FFX002-R2 Core-A exact configuration surfaces from frozen facts."
    )
    parser.add_argument("--input", required=True, help="FFX_EXACT_CONFIGURATION_INPUT_R1 JSON")
    parser.add_argument("--output-dir", required=True, help="Directory for deterministic Core-A artifacts")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    input_path = Path(args.input)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    try:
        result = produce_exact_configuration_set(payload)
    except CoreAContractError as exc:
        failure = {
            "schema_version": "FFX_CORE_A_FAILURE_RECEIPT_R1",
            "arm_id": "A",
            "view_family": "EXACT_CONFIGURATION_SET",
            "status": exc.status,
            "detail": exc.detail,
        }
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "CORE_A_FAILURE_RECEIPT.json").write_text(
            json.dumps(failure, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return 2

    write_outputs(result, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
