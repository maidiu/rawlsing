#!/usr/bin/env python3
"""Mechanically materialize the accepted LiTS-I Candidate-C binding inputs.

No source bytes or outcomes are opened. Every value is taken from immutable
accepted authority artifacts or from the frozen Route-C owner constants.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from rawlsing_next.pre553_empirical_objects import semantic_hash

R10L_COMMIT = "1d01bd7a1763bea642947557b924a7cfc6d15db6"
R10L_RECOVERY = "WORKER_RETURNS/EE-R10L/01_BANKED_PROJECTION_RECOVERY.json"
BANKED_COMMIT = "3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f"
AUTHORITY_PACKAGE = "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/banked_as2a/04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json"
B13_COMMIT = "46acf0b162bdcac5f47ce9cce0d9bb1d039fae2d"
B13_BASE = "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/WORKERS/B13_AS3R3_SUCCESSOR_DISCOVERY_FRONTIER_REPLAY_SEAL_R1"
B13_RUNTIME = B13_BASE + "/02_SUCCESSOR_RUNTIME_CATALOG_BINDING.json"
B13_DISCOVERY = B13_BASE + "/03_SUCCESSOR_DISCOVERY_AUTHORITY.json"
B13_FRONTIER = B13_BASE + "/06_SUCCESSOR_82_CANDIDATE_FRONTIER_MANIFEST.json"

FROZEN_SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
FROZEN_C11_RELEASE_HASH = "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
FROZEN_PREDICATE_SEMANTIC_CATALOG_HASH = "8c559917640242e017b03e206d5a0a950cb2973c36a90e0be43d3c0fe7cc9293"
FROZEN_RISK_TOPOLOGY_PARTITION_HASH = "ed3b76242a588a5e2d4dacbb76f17ceef6185cd27a4080a2e8fb436056abfabf"
SUCCESSOR_DISCOVERY_AUTHORITY_HASH = "2e153a153c59bd0b920f8db376478ad1b07000710e79a158471490c11b610cea"
SUCCESSOR_OFFICIAL_FRONTIER_HASH = "7aca4dbe1ccd36c48444d6858d378084e41aa30b3197662b6225753d5fc82e24"
PRODUCTION_DISCOVERY_OPERATION = "PRE553_PRODUCTION_EXACT_BOUNDED_AUTONOMOUS_DISCOVERY@1.0.0"
ROLE_ORDER = ("A000","A1V1","A1V2","A1V3","A1V4","A1V5","A1SSUB","A1SSPS","A1SMIS","A1RAPP","A2V1","A2V2","A2V3","A2V4","A2V5","A2SSUB","A2SSPS","A2SMIS","A2RAPP")

def _ensure(commit: str) -> None:
    probe = subprocess.run(["git","cat-file","-e",commit+"^{commit}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if probe.returncode == 0:
        return
    subprocess.run(["git","fetch","--no-tags","origin",commit], check=True, stdout=subprocess.DEVNULL)

def _git_bytes(commit: str, path: str) -> bytes:
    _ensure(commit)
    p = subprocess.run(["git","show",f"{commit}:{path}"], check=True, stdout=subprocess.PIPE)
    return p.stdout

def _git_json(commit: str, path: str) -> Any:
    return json.loads(_git_bytes(commit,path).decode("utf-8"))

def materialize() -> dict[str, Any]:
    recovery = _git_json(R10L_COMMIT, R10L_RECOVERY)
    package_bytes = _git_bytes(BANKED_COMMIT, AUTHORITY_PACKAGE)
    package_sha = hashlib.sha256(package_bytes).hexdigest()
    expected_package_sha = recovery["authority_package"]["bytes_sha256"]
    if package_sha != expected_package_sha:
        raise RuntimeError("accepted LiTS projection authority package byte identity drift")
    package = json.loads(package_bytes.decode("utf-8"))
    ids = recovery["accepted_identities"]
    if ids["source_sha256"] != FROZEN_SOURCE_SHA256 or ids["c11_logical_release_hash"] != FROZEN_C11_RELEASE_HASH:
        raise RuntimeError("R10L accepted LiTS identity drift")
    if package["projection_authority_ref"]["content_hash"] != ids["projection_authority_hash"]:
        raise RuntimeError("projection authority ref mismatch")
    if package["projection_material"]["slot_ledger_sha256"] != recovery["slot_ledger"]["sha256"]:
        raise RuntimeError("slot-ledger identity mismatch")

    route_c = {
        "source_sha256": ids["source_sha256"],
        "decoder_identity": package["projection_material"]["decoder"],
        "projection_authority_hash": ids["projection_authority_hash"],
        "slot_ledger_hash": recovery["slot_ledger"]["sha256"],
        "governed_projection_hash": ids["projection_cache_identity"],
        "c11_logical_release_hash": ids["c11_logical_release_hash"],
        "replay_manifest_hash": ids["as2b_replay_manifest_hash"],
        "semantic_authority_closure_hash": package_sha,
    }
    cacc1_determinant_hash = semantic_hash(route_c)

    runtime = _git_json(B13_COMMIT, B13_RUNTIME)
    discovery = _git_json(B13_COMMIT, B13_DISCOVERY)
    frontier = _git_json(B13_COMMIT, B13_FRONTIER)
    if discovery["content_hash"] != SUCCESSOR_DISCOVERY_AUTHORITY_HASH:
        raise RuntimeError("successor DiscoveryAuthority identity drift")
    if frontier["official_frontier_ref"]["content_hash"] != SUCCESSOR_OFFICIAL_FRONTIER_HASH:
        raise RuntimeError("successor frontier identity drift")
    mappings = runtime["predicate_role_mappings"]
    if [m["as3_id"] for m in mappings] != list(ROLE_ORDER):
        raise RuntimeError("B13 frozen 19-role order drift")
    atom_bindings = []
    for m in mappings:
        ref = {
            "kind": m["successor_kind"],
            "object_id": m["successor_object_id"],
            "content_hash": m["successor_content_hash"],
        }
        if "urn:test:" in ref["object_id"]:
            raise RuntimeError("synthetic runtime predicate ref forbidden")
        atom_bindings.append({
            "role_id": m["as3_id"],
            "semantic_atom_content_hash": m["source_content_hash"],
            "runtime_predicate_ref": ref,
        })

    cacc2 = {
        "cacc1_determinant_hash": cacc1_determinant_hash,
        "discovery_authority_ref": discovery["exact_ref"],
        "predicate_catalog_hash": FROZEN_PREDICATE_SEMANTIC_CATALOG_HASH,
        "risk_partition_hash": FROZEN_RISK_TOPOLOGY_PARTITION_HASH,
        "production_operation_identity": PRODUCTION_DISCOVERY_OPERATION,
        "candidate_frontier_ref": frontier["official_frontier_ref"],
    }
    material = {
        "schema": "EE_P2R1_LITS_C_REAL_BINDING@1.0.0",
        "status": "PASS__REAL_ACCEPTED_ROUTE_C_CACC1_CACC2_BINDINGS_MATERIALIZED",
        "source_access": False,
        "outcome_access": False,
        "synthetic_substitution": False,
        "route_c_determinants": route_c,
        "route_c_determinant_hash": cacc1_determinant_hash,
        "cacc2_determinants": cacc2,
        "atom_bindings": atom_bindings,
        "role_count": len(atom_bindings),
        "distinct_runtime_predicate_count": len({x["runtime_predicate_ref"]["content_hash"] for x in atom_bindings}),
        "sole_alias": runtime["sole_alias"],
        "authority_inputs": {
            "r10l_projection_recovery_commit": R10L_COMMIT,
            "banked_projection_commit": BANKED_COMMIT,
            "b13_runtime_binding_commit": B13_COMMIT,
            "authority_package_sha256": package_sha,
        },
    }
    return {**material, "binding_identity": semantic_hash(material)}

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=Path); args=ap.parse_args()
    result=materialize(); rendered=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(rendered,encoding="utf-8")
    print(rendered,end=""); return 0

if __name__ == "__main__":
    raise SystemExit(main())
