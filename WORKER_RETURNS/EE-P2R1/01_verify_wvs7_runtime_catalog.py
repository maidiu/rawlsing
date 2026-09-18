#!/usr/bin/env python3
"""Fresh-process qualification for EE-P2R1 runtime-catalog materialization.

This verifier consumes the exact adopted EE-P2F2 WVS7 objectization by immutable
commit with `git show`.  It opens no empirical source carrier and computes no
outcome.  The burden is only to prove that the carrier-neutral seam can recover
complete PRE553 object preimages, enforce their exact hashes, and compile the
same frozen 46-candidate I05 frontier without source- or candidate-specific code.
"""
from __future__ import annotations

import argparse
import copy
import json
import subprocess
from pathlib import Path

from rawlsing_next.pre553_carrier_execution import (
    CarrierExecutionBindingError,
    RuntimeObjectCatalog,
)
from rawlsing_next.pre553_discovery_exact import (
    _catalog_atoms,
    _catalog_templates,
    _compile_frontier,
    _validate_catalog_scope,
    _verify_discovery_authority,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, semantic_hash


F2_COMMIT = "22667bd395e7293f99b285daddad36fe3a4377ef"
P_AUTH = "WORKER_RETURNS/EE-P2F2/01_WVS7_PRE553_ISSUED_AUTHORITY_SNAPSHOTS.json"
P_PRED = "WORKER_RETURNS/EE-P2F2/03_WVS7_RESPONSE_ATOM_AND_PREDICATE_BINDINGS.json"
P_QUERY = "WORKER_RETURNS/EE-P2F2/04_WVS7_QUERY_TEMPLATE_BINDINGS.json"
P_DISC = "WORKER_RETURNS/EE-P2F2/05_WVS7_DISCOVERY_AUTHORITY_AND_FRONTIER_BINDING.json"

EXPECTED = {
    "authority_count": 6,
    "predicate_count": 11,
    "query_count": 3,
    "discovery_authority_count": 1,
    "candidate_count": 46,
    "discovery_authority_hash":
        "24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab",
    "candidate_grammar_hash":
        "a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6",
}


def _ensure_commit(commit: str) -> None:
    probe = subprocess.run(["git", "cat-file", "-e", commit + "^{commit}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if probe.returncode == 0:
        return
    subprocess.run(["git", "fetch", "--no-tags", "origin", commit],
        check=True, stdout=subprocess.DEVNULL)

def git_json(commit: str, path: str):
    _ensure_commit(commit)
    completed = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"exact governed artifact unavailable from {commit}:{path}: "
            f"{completed.stderr.strip()}"
        )
    return json.loads(completed.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-receipt", type=Path)
    args = parser.parse_args()

    auth = git_json(F2_COMMIT, P_AUTH)
    pred = git_json(F2_COMMIT, P_PRED)
    query = git_json(F2_COMMIT, P_QUERY)
    disc = git_json(F2_COMMIT, P_DISC)

    authority_documents = tuple(auth["snapshots"])
    predicate_documents = (
        pred["baseline_risk_predicate"],
        *(item["predicate"] for item in pred["atoms"]),
    )
    query_documents = tuple(item["query"] for item in query["templates"])
    discovery_documents = (disc["discovery_authority"],)

    catalog = RuntimeObjectCatalog.from_documents(
        authority_documents=authority_documents,
        predicate_documents=predicate_documents,
        query_documents=query_documents,
        discovery_authority_documents=discovery_documents,
    )

    counts = {
        "authority_count": len(catalog.authorities),
        "predicate_count": len(catalog.predicates),
        "query_count": len(catalog.queries),
        "discovery_authority_count": len(catalog.discovery_authorities),
    }
    for key, value in counts.items():
        if value != EXPECTED[key]:
            raise RuntimeError(f"{key} mismatch: expected {EXPECTED[key]}, got {value}")

    discovery = catalog.discovery_authorities[0]
    if discovery.content_hash != EXPECTED["discovery_authority_hash"]:
        raise RuntimeError("DiscoveryAuthority identity mismatch")
    if discovery.candidate_grammar_ref["content_hash"] != EXPECTED["candidate_grammar_hash"]:
        raise RuntimeError("candidate grammar identity mismatch")

    definition = _verify_discovery_authority(
        discovery, catalog.authority_registry
    )
    atom_catalog = _catalog_atoms(definition, catalog.predicates)
    template_catalog = _catalog_templates(definition, catalog.queries)
    _validate_catalog_scope(discovery, atom_catalog, template_catalog)
    candidates = _compile_frontier(definition, atom_catalog, template_catalog)
    candidate_hashes = [candidate.candidate_hash for candidate in candidates]
    if len(candidate_hashes) != EXPECTED["candidate_count"]:
        raise RuntimeError("compiled candidate count mismatch")
    if candidate_hashes != disc["candidate_hashes"]:
        raise RuntimeError("compiled candidate hashes diverge from adopted F2 Lock2")
    if candidate_hashes != sorted(candidate_hashes):
        raise RuntimeError("compiled candidate order is not canonical candidate-hash order")

    # Hostile 1: exact object hashes are not suggestions.
    mutated = copy.deepcopy(predicate_documents[0])
    mutated["content_hash"] = "0" * 64
    try:
        RuntimeObjectCatalog.from_documents(
            authority_documents=authority_documents,
            predicate_documents=(mutated, *predicate_documents[1:]),
            query_documents=query_documents,
            discovery_authority_documents=discovery_documents,
        )
    except CarrierExecutionBindingError:
        mutated_hash_rejected = True
    else:
        mutated_hash_rejected = False
    if not mutated_hash_rejected:
        raise RuntimeError("mutated canonical object hash was not rejected")

    # Hostile 2: no ref-only/hash-inversion fallback exists.
    unavailable = ExactRef(
        "EmpiricalPredicate@1.0.0",
        "urn:rawlsing:pre553:EmpiricalPredicate:sha256:" + "f" * 64,
        "f" * 64,
    )
    try:
        catalog.resolve_predicate_exact(unavailable)
    except CarrierExecutionBindingError:
        missing_preimage_rejected = True
    else:
        missing_preimage_rejected = False
    if not missing_preimage_rejected:
        raise RuntimeError("missing predicate preimage did not fail closed")

    material = {
        "schema": "EE_P2R1_WVS7_RUNTIME_CATALOG_QUALIFICATION@1.0.0",
        "status": "PASS__EXACT_F2_PREIMAGES_MATERIALIZED__LOCK2_FRONTIER_RECOMPILED",
        "source_commit": F2_COMMIT,
        "source_paths": [P_AUTH, P_PRED, P_QUERY, P_DISC],
        "source_access": False,
        "empirical_outcomes_computed": False,
        "candidate_specific_execution": False,
        "counts": counts,
        "catalog_receipt": catalog.receipt(),
        "discovery_authority_ref": discovery.ref.as_dict(),
        "candidate_grammar_ref": discovery.candidate_grammar_ref,
        "candidate_count": len(candidate_hashes),
        "candidate_hashes": candidate_hashes,
        "mutated_hash_rejected": mutated_hash_rejected,
        "missing_preimage_rejected": missing_preimage_rejected,
        "law": "NO_HASH_INVERSION__EXACT_CANONICAL_PREIMAGE_REQUIRED",
    }
    receipt = {**material, "receipt_identity": semantic_hash(material)}
    rendered = json.dumps(canonicalize(receipt), sort_keys=True, indent=2) + "\n"
    if args.write_receipt:
        args.write_receipt.parent.mkdir(parents=True, exist_ok=True)
        args.write_receipt.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
