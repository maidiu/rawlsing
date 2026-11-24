"""Build the existing ANVIL stream input to S3 from a governed source config.

The private provider supplies the binding and resolver. It must export
construction_inputs(config), returning (source_path, request, resolver)
for an authenticated, current construction-only or broader decision.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import socket

from rawlsing_next.pre553_r157_projection_adapter import (
    _assert_current,
    canonical_config_hash,
    load_source_config,
    source_read_request_from_config,
)

from .runner import load_file_module
from .sqlite_free_single_pass import build_single_pass, resume_single_pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--config-sha256", required=True)
    parser.add_argument("--canonical-config-sha256", required=True)
    parser.add_argument("--authority-provider", type=Path, required=True)
    parser.add_argument("--private-root", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--execute", action="store_true")
    mode.add_argument("--resume", type=Path)
    args = parser.parse_args()

    config = load_source_config(args.config)
    if (
        hashlib.sha256(args.config.read_bytes()).hexdigest() != args.config_sha256
        or canonical_config_hash(config) != args.canonical_config_sha256
    ):
        parser.error("source configuration pin mismatch")
    provider = load_file_module(args.authority_provider, "anvil_construction_provider")
    source_path, request, resolver = provider.construction_inputs(config)
    if request.host.casefold().split(".")[0] != socket.gethostname().casefold().split(".")[0]:
        parser.error("construction decision host does not match the execution host")
    scope = dict(
        host=request.host,
        purpose=request.purpose,
        consumer_use=request.consumer_use,
        semantic_use_scope=request.semantic_use_scope,
    )
    if request != source_read_request_from_config(config, **scope):
        parser.error("construction request does not match the pinned source configuration")
    decision = resolver.resolve_current(request)
    _assert_current(decision, request)
    if len(decision.source_permission_refs) != 1:
        parser.error("construction requires one exact grant for checkpoint binding")
    if not (args.execute or args.resume):
        print(json.dumps({"status": "CONSTRUCTION_ADMISSION_PASS", "source_id": request.source_id}))
        return 0

    root = args.private_root.absolute()
    if not root.is_dir() or root.is_symlink() or root.stat().st_mode & 0o077:
        parser.error("private root must be an existing mode-0700 directory")

    def progress(event):
        print(json.dumps({
            key: event[key]
            for key in ("phase", "family", "processed", "expected", "rows", "records")
            if key in event
        }), flush=True)

    bindings = dict(
        config=config, request=request, resolver=resolver,
        grant_ref=decision.source_permission_refs[0], decision_ref=decision.decision_ref,
        progress=progress,
    )
    if args.resume:
        receipt = resume_single_pass(checkpoint=args.resume, root=root, **bindings)
    else:
        receipt = build_single_pass(source_path=source_path, private_root=root, **scope, **bindings)

    # Retain candidate pins privately. S3 still needs independently held pins
    # and its own currentness provider.
    candidate = {
        "path": receipt.path, "manifest_sha256": receipt.manifest_sha256,
        "source_id": request.source_id, "source_sha256": request.source_sha256,
        "roots": vars(receipt.roots), "family_counts": dict(receipt.family_counts),
    }
    candidate_path = Path(receipt.path).with_suffix(".candidate.json")
    with os.fdopen(os.open(candidate_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "w") as out:
        json.dump(candidate, out, sort_keys=True)
    print(json.dumps({"status": "STREAM_CONSTRUCTED", "source_id": request.source_id}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
