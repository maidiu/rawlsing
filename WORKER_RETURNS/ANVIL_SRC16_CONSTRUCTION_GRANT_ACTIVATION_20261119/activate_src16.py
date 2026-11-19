#!/usr/bin/env python3
"""Activate the exact SRC16 local C11 construction decision.

Private operatives stay outside Git. Public return contains only safe aggregate
metadata, hashes and refusal codes. No source file is opened, statted, hashed or
decoded.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path("/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117")
OWNER = ROOT / "OWNER"
PRIOR = OWNER / "WORKER_RETURNS/ANVIL_ALL35_CONSTRUCTION_GRANT_REPAIR_20261119"
OUT = OWNER / "WORKER_RETURNS/ANVIL_SRC16_CONSTRUCTION_GRANT_ACTIVATION_20261119"
PRIVATE = Path("/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/anvil_src16_construction_grant_20261119")
CAND = ROOT / "MEASUREMENT_PREP/private-runtime/SRC04_OVERLAY_REPLAY_1795040438/tree"
SOURCE_DRAFT = Path("/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/anvil_all35_construction_grant_drafts_20261119/SRC16.full-source-read-grant.draft.json")

sys.path[:0] = [str(CAND)]

from rawlsing_next.pre553_r157_projection_adapter import (
    IssuedSourceReadDecision, SourceReadRequest,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash


def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PRIVATE.mkdir(parents=True, mode=0o700, exist_ok=True)
    draft = load(SOURCE_DRAFT)
    if (draft["source_id"] != "SRC16"
            or draft["expected_source_sha256"] != "e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204"
            or draft["source_rows"] != 1613
            or draft["source_columns"] != 216
            or draft["source_bytes"] != 1647241):
        raise SystemExit("SRC16_DRAFT_IDENTITY_MISMATCH")
    source_config = load(CAND / "rawlsing_next/source_configuration/data/SRC16/SRC16.source.config.json")
    metadata_ref = ExactRef(**source_config["identity"]["metadata_witness_ref"])
    locator_id = source_config["identity"]["locator"]["locator_id"]
    grant = dict(draft)
    grant.update({
        "currentness": "CURRENT_GRANTED",
        "revocation": "NONE_RECORDED",
        "authorization": "for GSS 1972, yes",
        "issuer": "HUMAN_USER_VIA_EXISTING_PYAT_HQ",
        "thread": "HQ_THIS_THREAD",
        "draft": False,
        "operative": True,
        "limits": [
            "Construction-only local C11; no Q2, analysis, science or eligibility.",
            "No source bytes in Git, no respondent rows in Git, no export.",
            "Exact local source read only for C11 estate construction.",
        ],
    })
    grant_raw = (json.dumps(grant, indent=2, sort_keys=True) + "\n").encode()
    grant_path = PRIVATE / "SRC16.construction.grant.json"
    grant_path.write_bytes(grant_raw)
    os.chmod(grant_path, 0o600)
    grant_sha = sha_bytes(grant_raw)

    request = SourceReadRequest(
        source_id="SRC16",
        source_sha256=grant["expected_source_sha256"],
        source_format="SAV",
        custody_locator_binding=locator_id,
        host="USER_LOCAL_MAC",
        purpose="FULL_SRC16_ORIGINAL_C11_CONSTRUCTION_ONLY",
        consumer_use="EXISTING_PRE553_SOURCE_BACKED_C11",
        read_operation="SOURCE_RESPONSE_DECODE",
        physical_read_extent="EXACT_FILE",
        metadata_freeze_refs=(metadata_ref,),
        semantic_use_scope=(
            "C11_CONSTRUCTION_ONLY", "NO_Q2", "NO_SEMANTIC_ADOPTION", "SRC16",
        ),
    )
    decision_basis = {
        "grant_sha256": grant_sha,
        "source_id": request.source_id,
        "source_sha256": request.source_sha256,
        "host": request.host,
        "purpose": request.purpose,
        "consumer_use": request.consumer_use,
        "scope": grant["scope"],
        "read_operation": request.read_operation,
        "physical_read_extent": request.physical_read_extent,
        "user_decision": "for GSS 1972, yes",
        "thread": "HQ_THIS_THREAD",
    }
    decision_ref = ExactRef(
        "USER_SOURCE_READ_DECISION",
        f"urn:rawlsing:src16:construction-decision:{grant_sha}",
        semantic_hash(decision_basis),
    )
    grant_ref = ExactRef(
        "FULL_SOURCE_READ_GRANT",
        f"urn:rawlsing:src16:construction-grant:{grant_sha}",
        grant_sha,
    )
    decision = IssuedSourceReadDecision(
        decision_ref=decision_ref,
        source_permission_refs=(grant_ref,),
        source_id=request.source_id,
        source_sha256=request.source_sha256,
        source_format=request.source_format,
        custody_locator_binding=request.custody_locator_binding,
        host=request.host,
        purpose=request.purpose,
        consumer_use=request.consumer_use,
        read_operation=request.read_operation,
        physical_read_extent=request.physical_read_extent,
        metadata_freeze_refs=request.metadata_freeze_refs,
        semantic_use_scope=request.semantic_use_scope,
        effective_interval="2026-11-19/HQ_THIS_THREAD",
        currentness="CURRENT_GRANTED",
        revocation_ref=None,
        retention_export_limits={
            "retention": "LOCAL_RUNTIME_ONLY",
            "export": "DENY",
            "rowwise_response_artifacts": "DENY",
            "source_bytes_in_git": "DENY",
        },
    )
    binding = {
        "schema": "ANVIL_SRC16_EXACT_CONSTRUCTION_BINDING@1",
        "grant_sha256": grant_sha,
        "grant_private_filename": grant_path.name,
        "request": {
            "source_id": request.source_id,
            "source_sha256": request.source_sha256,
            "source_format": request.source_format,
            "custody_locator_binding": request.custody_locator_binding,
            "host": request.host,
            "purpose": request.purpose,
            "consumer_use": request.consumer_use,
            "read_operation": request.read_operation,
            "physical_read_extent": request.physical_read_extent,
            "metadata_freeze_refs": [metadata_ref.as_dict()],
            "semantic_use_scope": list(request.semantic_use_scope),
        },
        "decision": {
            "decision_ref": decision.decision_ref.as_dict(),
            "source_permission_refs": [ref.as_dict() for ref in decision.source_permission_refs],
            "currentness": decision.currentness,
            "revocation_ref": None,
            "effective_interval": decision.effective_interval,
            "retention_export_limits": dict(decision.retention_export_limits),
        },
        "user_decision": {
            "quote": "for GSS 1972, yes",
            "question": "Authorize local read of the exact files in the decision packet solely to build C11 estates?",
            "thread": "HQ_THIS_THREAD",
            "issuer": "HUMAN_USER_VIA_EXISTING_PYAT_HQ",
        },
        "source_config": grant["source_config"],
    }
    binding_raw = (json.dumps(binding, indent=2, sort_keys=True) + "\n").encode()
    binding_path = PRIVATE / "SRC16.construction.binding.json"
    binding_path.write_bytes(binding_raw)
    os.chmod(binding_path, 0o600)
    binding_sha = sha_bytes(binding_raw)

    resolver_path = PRIVATE / "SRC16.exact_resolver.py"
    resolver_source = '''"""Private exact SRC16 construction resolver; no source I/O."""
from __future__ import annotations
import json
from pathlib import Path
from rawlsing_next.pre553_r157_projection_adapter import SourceReadRequest, IssuedSourceReadDecision
from rawlsing_next.pre553_empirical_objects import ExactRef

class BindingRefusal(RuntimeError):
    pass

class ExactSrc16Resolver:
    def __init__(self, binding_path):
        d=json.loads(Path(binding_path).read_text())
        self.grant_sha256=d["grant_sha256"]
        self.request=SourceReadRequest(
            source_id=d["request"]["source_id"], source_sha256=d["request"]["source_sha256"],
            source_format=d["request"]["source_format"], custody_locator_binding=d["request"]["custody_locator_binding"],
            host=d["request"]["host"], purpose=d["request"]["purpose"], consumer_use=d["request"]["consumer_use"],
            read_operation=d["request"]["read_operation"], physical_read_extent=d["request"]["physical_read_extent"],
            metadata_freeze_refs=tuple(ExactRef(**x) for x in d["request"]["metadata_freeze_refs"]),
            semantic_use_scope=tuple(d["request"]["semantic_use_scope"]))
        dd=d["decision"]; refs=tuple(ExactRef(**x) for x in dd["source_permission_refs"])
        self.decision=IssuedSourceReadDecision(
            decision_ref=ExactRef(**dd["decision_ref"]), source_permission_refs=refs,
            source_id=self.request.source_id, source_sha256=self.request.source_sha256,
            source_format=self.request.source_format, custody_locator_binding=self.request.custody_locator_binding,
            host=self.request.host, purpose=self.request.purpose, consumer_use=self.request.consumer_use,
            read_operation=self.request.read_operation, physical_read_extent=self.request.physical_read_extent,
            metadata_freeze_refs=self.request.metadata_freeze_refs, semantic_use_scope=self.request.semantic_use_scope,
            effective_interval=dd["effective_interval"], currentness=dd["currentness"],
            revocation_ref=None, retention_export_limits=dd["retention_export_limits"])
    def resolve_current(self, request):
        if request != self.request:
            raise BindingRefusal("EXACT_REQUEST_MISMATCH")
        return self.decision
'''
    resolver_path.write_text(resolver_source)
    os.chmod(resolver_path, 0o600)

    # Import the private resolver by path and exercise exact/representative negatives.
    import importlib.util
    spec = importlib.util.spec_from_file_location("src16_exact_resolver", resolver_path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    resolver = mod.ExactSrc16Resolver(binding_path)
    admitted = resolver.resolve_current(request)
    cases = []
    for name, other in [
        ("other_source", replace(request, source_id="SRC15", source_sha256="c43d0e1821c51398817d7dfdfad2c0a4a5bb0d492f6a58096670e623bb6130e9")),
        ("analysis_purpose", replace(request, purpose="PRE553_OBSERVED_RESPONSE_EMPIRICAL_OPERATIONS@1.0.0")),
        ("incorrect_scope", replace(request, semantic_use_scope=("ANALYSIS_ONLY",))),
    ]:
        try:
            resolver.resolve_current(other)
        except mod.BindingRefusal as exc:
            cases.append({"case": name, "refused": True, "code": str(exc), "source_read_performed": False})
        else:
            cases.append({"case": name, "refused": False, "code": "NOT_REFUSED", "source_read_performed": False})
    public = {
        "schema": "ANVIL_SRC16_CONSTRUCTION_GRANT_ACTIVATION@1",
        "status": "ACTIVE_PRIVATE_OPERATIVE_BINDING",
        "source_id": "SRC16",
        "source_artifact_id": "GSS1972.sav",
        "source_sha256": grant["expected_source_sha256"],
        "source_rows": 1613,
        "source_columns": 216,
        "source_bytes": 1647241,
        "host": "USER_LOCAL_MAC",
        "purpose": "FULL_SRC16_ORIGINAL_C11_CONSTRUCTION_ONLY",
        "consumer": "EXISTING_PRE553_SOURCE_BACKED_C11",
        "scope": grant["scope"],
        "extent": "EXACT_FILE",
        "retention": "LOCAL_RUNTIME_ONLY",
        "currentness": "CURRENT_GRANTED",
        "revocation": "NONE_RECORDED",
        "user_decision": {
            "quote": "for GSS 1972, yes",
            "thread": "HQ_THIS_THREAD",
            "issuer": "HUMAN_USER_VIA_EXISTING_PYAT_HQ",
        },
        "grant_sha256": grant_sha,
        "binding_sha256": binding_sha,
        "decision_ref": decision_ref.as_dict(),
        "request": {
            "source_id": request.source_id,
            "source_sha256": request.source_sha256,
            "source_format": request.source_format,
            "custody_locator_binding": request.custody_locator_binding,
            "host": request.host,
            "purpose": request.purpose,
            "consumer_use": request.consumer_use,
            "read_operation": request.read_operation,
            "physical_read_extent": request.physical_read_extent,
            "metadata_freeze_refs": [metadata_ref.as_dict()],
            "semantic_use_scope": list(request.semantic_use_scope),
        },
        "resolver_results": {
            "exact_request": {"admitted": admitted == resolver.decision, "currentness": admitted.currentness, "source_read_performed": False},
            "negative_cases": cases,
        },
        "private_operative": {
            "root": str(PRIVATE),
            "grant_file": grant_path.name,
            "binding_file": binding_path.name,
            "resolver_file": resolver_path.name,
            "mode": "0700/0600",
            "in_git": False,
        },
        "public_source_path": False,
        "source_read_performed": False,
        "analysis_or_q2_issued": False,
    }
    (OUT / "ACTIVATION.json").write_text(json.dumps(public, indent=2, sort_keys=True) + "\n")
    prior = load(PRIOR / "DRAFT_INDEX.json")
    pending = [d["source_id"] for d in prior["drafts"] if d["source_id"] != "SRC16"]
    (OUT / "PENDING_32.json").write_text(json.dumps({
        "schema": "ANVIL_ALL35_CONSTRUCTION_GRANT_PENDING_AFTER_SRC16@1",
        "active_existing": ["SRC04", "SRC17"],
        "newly_active": ["SRC16"],
        "pending": pending,
        "pending_count": len(pending),
        "existing_scope_unchanged": True,
        "private_drafts_index": str(PRIOR / "DRAFT_INDEX.json"),
        "private_drafts_index_sha256": sha_bytes((PRIOR / "DRAFT_INDEX.json").read_bytes()),
    }, indent=2, sort_keys=True) + "\n")
    (OUT / "SUMMARY.json").write_text(json.dumps({
        "schema": "ANVIL_SRC16_ACTIVATION_SUMMARY@1",
        "active_existing": 2,
        "newly_active": 1,
        "drafts_pending": len(pending),
        "total_sources": 35,
        "source_read_performed": False,
        "actual_run_started": False,
        "q2_or_analysis_issued": False,
        "private_operative_files_in_git": False,
    }, indent=2, sort_keys=True) + "\n")
    (OUT / "SHARED_RUNNER_GAP.json").write_text(json.dumps({
        "schema": "ANVIL_SRC16_SHARED_RUNNER_GAP@1",
        "shared_runner": "/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_SRC04_SQLITE_FREE_OPERATOR_INTEGRATION_20261118/sqlite_free_witness.py",
        "can_execute_src16": False,
        "reason": "The shared SQLite-free witness hardcodes SRC04 config/trust/q217/runtime overlay and its producer path; it has no SRC16 source/grant/config entry. The exact SRC16 binding is materialized privately but cannot be injected into that runner without a generic binding/config adapter.",
        "smallest_gap": "Add a generic source-specific binding injection to the existing sqlite_free_single_pass/sqlite_free_witness path; no per-wave writer or new administrative system is needed.",
        "metadata_preflight_available": False,
        "authorized_launch_inputs_available": False,
        "source_read_performed": False,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "grant_sha256": grant_sha, "binding_sha256": binding_sha,
        "exact_admitted": public["resolver_results"]["exact_request"]["admitted"],
        "negatives": cases, "pending": len(pending),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
