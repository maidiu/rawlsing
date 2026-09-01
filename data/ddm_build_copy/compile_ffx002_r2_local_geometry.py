#!/usr/bin/env python3
"""CLI for the bounded FFX002-R2 Core-B LOCAL_GEOMETRIC producer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from data.ddm_build_copy.ffx002_r2_local_geometry import (
    LocalGeometryContractError,
    compile_local_geometric_view,
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_canonical_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    path.write_text(rendered + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compile the bounded FFX002-R2 Core-B LOCAL_GEOMETRIC view over "
            "already-frozen position/disposition semantic inputs."
        )
    )
    parser.add_argument("--input-json", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args()

    try:
        payload = _load_json(args.input_json)
        result = compile_local_geometric_view(payload)
    except (OSError, json.JSONDecodeError, LocalGeometryContractError) as exc:
        parser.exit(2, f"LOCAL_GEOMETRIC_FAIL_CLOSED: {exc}\n")

    _write_canonical_json(args.output_json, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
