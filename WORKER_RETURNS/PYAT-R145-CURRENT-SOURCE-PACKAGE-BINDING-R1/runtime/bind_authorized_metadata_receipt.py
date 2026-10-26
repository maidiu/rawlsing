#!/usr/bin/env python3
"""Consume an externally authorized metadata/header receipt; never a source grant."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from source_package_binder import (  # noqa: E402
    PackageBindingRefusal, bind_authorized_metadata_receipt, build_preparation,
    load_metadata_scope,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args(argv)
    specs = {spec.source_id: spec for spec in load_metadata_scope(args.scope)}
    spec = specs.get(args.source_id)
    if spec is None:
        raise PackageBindingRefusal("SOURCE_ID_NOT_IN_METADATA_SCOPE", args.source_id)
    receipt = json.loads(Path(args.receipt).read_text(encoding="utf-8"))
    preparation, _accounts, _freeze = build_preparation(spec)
    _prep, accounts, _freeze = build_preparation(spec)
    binding = bind_authorized_metadata_receipt(
        spec, receipt,
        codebook_variables=[account["var_name"] for account in accounts],
    )
    print(json.dumps(binding, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
