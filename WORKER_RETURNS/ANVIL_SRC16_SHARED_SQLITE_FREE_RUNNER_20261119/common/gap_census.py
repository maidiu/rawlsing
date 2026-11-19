#!/usr/bin/env python3
"""Controller-run, one-pass, aggregate mapped-slot gap census.

This is deliberately separate from the worker path.  It is intended to be run
by the owner/controller under the exact existing SRC16 construction grant.  It
uses the pinned config/profile and the existing resolver before decode, performs
one bounded physical pass, and writes only aggregate per-slot unresolved-token
coverage.  It never emits respondent rows, identity keys, source bytes, or a
decoded response table.

The worker does not run this script.  The owner may run it to obtain the exact
native tokens needed to repair the pinned mapping without guessing a range or
category.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from source_adapter import AdapterRefusal, Profile  # noqa: E402
from mapped_slot_precheck import aggregate_mapped_slots  # noqa: E402

CONFIG_FILE_SHA256 = "1106de3e086032f5ac0b26fee0b56a147722399c80ac2841b70f0b851dea93b7"
CONFIG_CANONICAL_SHA256 = "c26e8e71afbc629a9f19708cedb7b38cc2ba3cefb9ac53f11e0608044e64b534"
SOURCE_SHA256 = "e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=512)
    parser.add_argument("--controller-run", action="store_true", required=True)
    args = parser.parse_args()

    try:
        profile = Profile(args.profile)
        if profile.config.source_id != "SRC16":
            raise AdapterRefusal("NOT_SRC16_PROFILE")
        if profile.config.document["binding"]["source_sha256"] != SOURCE_SHA256:
            raise AdapterRefusal("SOURCE_IDENTITY_DRIFT")
        decision = profile.resolve_before_source()
        if decision.currentness != "CURRENT_GRANTED" or decision.revocation_ref is not None:
            raise AdapterRefusal("CURRENT_OR_REVOCATION_REFUSED")

        from rawlsing_next.pre553_r157_projection_adapter import (
            canonical_config_hash,
            decode_config_with_source_read_permission,
        )

        cfg_file = Path(profile.data["config"]).absolute()
        if sha256(cfg_file) != CONFIG_FILE_SHA256:
            raise AdapterRefusal("CONFIG_FILE_DRIFT")
        if canonical_config_hash(profile.config) != CONFIG_CANONICAL_SHA256:
            raise AdapterRefusal("CONFIG_CANONICAL_DRIFT")

        request = profile.request
        incidence = decode_config_with_source_read_permission(
            profile.config,
            source_path=profile.source_path,
            resolver=profile.resolver,
            host=request.host,
            purpose=request.purpose,
            consumer_use=request.consumer_use,
            semantic_use_scope=request.semantic_use_scope,
        )
        try:
            if incidence.source_sha256 != SOURCE_SHA256:
                raise AdapterRefusal("DECODED_SOURCE_SHA_MISMATCH")
            if incidence.row_count != profile.config.document["binding"]["row_count"]:
                raise AdapterRefusal("DECODED_SOURCE_ROWS_MISMATCH")
            report = aggregate_mapped_slots(
                profile.config.document,
                incidence.iter_cells(int(args.batch_size)),
            )
        finally:
            incidence.close()

        output = {
            "schema": "ANVIL_SRC16_AGGREGATE_MAPPED_SLOT_GAP_CENSUS@1",
            "source_id": "SRC16",
            "source_sha256": SOURCE_SHA256,
            "source_config_file_sha256": CONFIG_FILE_SHA256,
            "source_config_canonical_sha256": CONFIG_CANONICAL_SHA256,
            "currentness": decision.currentness,
            "revocation": None,
            "scope": "C11_CONSTRUCTION_ONLY_NO_Q2",
            "one_bounded_pass": True,
            "source_bytes_written_to_git": False,
            "respondent_rows_emitted": False,
            "aggregate_only": True,
            "census": report,
        }
        args.out = args.out.absolute()
        args.out.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        args.out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
        os.chmod(args.out, 0o600)
        summary = {
            "status": "CENSUS_COMPLETE_WITH_GAPS" if not report["precheck_passed"] else "CENSUS_COMPLETE_NO_GAPS",
            "unresolved_slot_count": report["unresolved_slot_count"],
            "unresolved_cell_count": report["unresolved_cell_count"],
            "missing_slot_count": report["missing_slot_count"],
            "duplicate_slot_count": report["duplicate_slot_count"],
            "out": str(args.out),
        }
        print(json.dumps(summary, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "status": "CENSUS_REFUSED",
            "code": getattr(exc, "code", type(exc).__name__),
            "detail": str(exc),
            "source_read_performed": False,
        }, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
