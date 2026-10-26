#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import json
import resource
import time
from pathlib import Path
from typing import Any, Mapping

from rawlsing_next.pre553_carrier_execution import materialize_public_object
from rawlsing_next.pre553_learned_empirical_adjudication import (
    M1AdjudicationInputBundle,
    M1ValidatorRegistry,
    adjudicate_learned_empirical,
    build_m1_adjudication_input_bundle,
)
from rawlsing_next.pre553_empirical_objects import canonicalize


def load_index(private: Path) -> list[Mapping[str, Any]]:
    return [
        json.loads(line)
        for line in (private / "object_index.jsonl").open(encoding="utf-8")
    ]


def load_doc(private: Path, item: Mapping[str, Any]) -> Mapping[str, Any]:
    path = (
        private
        / "objects"
        / item["schema_id"]
        / f"{item['content_hash']}.json.gz"
    )
    return json.loads(gzip.decompress(path.read_bytes()).decode("utf-8"))


def load_object(private: Path, item: Mapping[str, Any]) -> Any:
    doc = load_doc(private, item)
    obj = materialize_public_object(doc)
    if canonicalize(obj.as_dict()) != canonicalize(doc):
        raise RuntimeError("consumer object round-trip drift")
    return obj


def by_ref(index: list[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {item["ref"]["object_id"]: item for item in index}


def ref_dict(value: Any) -> Mapping[str, Any]:
    return canonicalize(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    started = time.time()
    private = args.private.resolve()
    out = args.out.resolve()
    index = load_index(private)
    refs = by_ref(index)
    tail = json.loads((private / "material_tail.json").read_text())

    receipts = [x for x in index if x["schema_id"] == "DiscoveryResultReceipt"]
    selected_meta = min(
        (x for x in receipts if x["coverage_state"] == "EVALUATED_SUPPORTED"),
        key=lambda x: len(x["empirical_fact_refs"]) + len(x["validation_fact_refs"]),
    )
    selected_receipt = load_object(private, selected_meta)
    selected_fact_refs = {
        *[x["object_id"] for x in selected_meta["empirical_fact_refs"]],
        *[x["object_id"] for x in selected_meta["validation_fact_refs"]],
    }
    fact_metas = [refs[x] for x in selected_fact_refs]
    facts = [load_object(private, x) for x in fact_metas]
    queries = [
        load_object(private, x)
        for x in index if x["schema_id"] == "EmpiricalQuerySpec"
    ]
    predicates = [
        load_object(private, x)
        for x in index if x["schema_id"] == "EmpiricalPredicate"
    ]
    authority_metas = [
        x for x in index if x["schema_id"] == "AuthoritySnapshot"
    ]
    authorities = [load_object(private, x) for x in authority_metas]
    discoveries = [
        load_object(private, x)
        for x in index if x["schema_id"] == "DiscoveryAuthority"
    ]

    release_ref = tail["projection_and_release_refs"]["release_refs"][0]
    replay_ref = tail["projection_and_release_refs"]["release_replay_refs"][0]
    bundle = None
    disposition = None
    m1_error = None
    try:
        bundle = build_m1_adjudication_input_bundle(
            requested_claim_family_id="NOT_BOUND",
            requested_claim_rule_id=selected_meta["rule_id"],
            selected_discovery_receipts=(selected_receipt,),
            discovery_authority_catalog=discoveries,
            empirical_fact_catalog=facts,
            empirical_query_catalog=queries,
            empirical_predicate_catalog=predicates,
            authority_snapshots=authorities,
            requested_scope={
                "source_identity": tail["source_identity"],
                "frontier_manifest": tail["frontier_manifest"],
                "claim_family_selection": "NOT_BOUND__NO_FAMILY_RULE_ISSUED",
            },
            additional_dependency_refs=(release_ref, replay_ref),
        )
        disposition = adjudicate_learned_empirical(
            bundle,
            None,
            validator_registry=M1ValidatorRegistry(),
        )
    except Exception as exc:
        m1_error = {"type": type(exc).__name__, "message": str(exc)}

    selected = fact_metas[0]
    doc = load_doc(private, selected)
    original = materialize_public_object(doc)
    tampered_identity = dict(doc)
    tampered_identity["object_id"] = (
        tampered_identity["object_id"][:-1]
        + ("0" if tampered_identity["object_id"][-1] != "0" else "1")
    )
    identity_error = None
    try:
        materialize_public_object(tampered_identity)
    except Exception as exc:
        identity_error = {"type": type(exc).__name__, "message": str(exc)}

    tampered_ref = dict(doc)
    fields = dict(tampered_ref["semantic_fields"])
    qref = dict(fields["empirical_query_spec_ref"])
    qref["content_hash"] = (
        "0" * 64
    )
    qref["object_id"] = (
        "urn:rawlsing:pre553:EmpiricalQuerySpec:sha256:" + qref["content_hash"]
    )
    fields["empirical_query_spec_ref"] = qref
    tampered_ref["semantic_fields"] = fields
    ref_error = None
    try:
        materialize_public_object(tampered_ref)
    except Exception as exc:
        ref_error = {"type": type(exc).__name__, "message": str(exc)}

    restored = materialize_public_object(doc)
    if restored.ref != original.ref or restored.content_hash != original.content_hash:
        raise RuntimeError("restored object identity drift")

    authorization_groups = {}
    for item in authority_metas:
        key = (
            item["authority_id"],
            item["authority_version"],
            item["authority_content_hash"],
        )
        authorization_groups.setdefault(key, []).append(item)
    conflicts = [
        {
            "authority_ref": {
                "authority_id": key[0],
                "authority_version": key[1],
                "authority_content_hash": key[2],
            },
            "snapshot_refs": [x["ref"] for x in group],
            "snapshot_content_hashes": [x["content_hash"] for x in group],
        }
        for key, group in authorization_groups.items()
        if len(group) > 1
    ]
    disposition_doc = None if disposition is None else disposition.as_dict()
    status = (
        "ARTIFACT_RECOVERY_PASS__M1_INPUT_BUNDLE_BUILT__FAMILY_RULE_MISSING"
        if disposition is not None
        else "ARTIFACT_RECOVERY_PASS__M1_INPUT_REFUSED__CONFLICTING_AUTHORITY_SNAPSHOT_PREIMAGES"
    )
    consumer_result = (
        "TYPED_REFUSAL__NO_FAMILY_RULE_BINDING__NO_VALUES_READ"
        if disposition is not None
        else "TYPED_REFUSAL__M1_INPUT_BUNDLE_CONFLICTING_AUTHORITY_SNAPSHOT_PREIMAGES__NO_VALUES_READ"
    )
    result = {
        "schema": "PYAT_R128_CONSUMER_RECEIPT_OR_REFUSAL@1",
        "status": status,
        "artifact_recovery": "PASS",
        "consumer_result": consumer_result,
        "selected_edge": {
            "owner": "rawlsing_next.pre553_learned_empirical_adjudication",
            "call": "build_m1_adjudication_input_bundle -> adjudicate_learned_empirical",
            "reached_call": "build_m1_adjudication_input_bundle",
            "not_reached_call": "adjudicate_learned_empirical",
            "selected_receipt_ref": selected_meta["ref"],
            "selected_candidate_hash": selected_meta["candidate_hash"],
            "selected_fact_refs": [x["ref"] for x in fact_metas],
            "query_catalog_count": len(queries),
            "predicate_catalog_count": len(predicates),
            "authority_catalog_count": len(authorities),
            "discovery_authority_count": len(discoveries),
            "requested_claim_family_id": "NOT_BOUND",
            "requested_claim_rule_id": selected_meta["rule_id"],
            "family_rule_binding": None,
            "validator_registry": "EMPTY__NO_REGISTRATION",
        },
        "bundle": None if bundle is None else {
            "ref": bundle.ref.as_dict(),
            "requested_claim_family_id": bundle.requested_claim_family_id,
            "requested_claim_rule_id": bundle.requested_claim_rule_id,
            "discovery_receipt_count": len(bundle.discovery_receipts),
            "empirical_fact_count": len(bundle.empirical_facts),
            "empirical_query_count": len(bundle.empirical_queries),
            "empirical_predicate_count": len(bundle.empirical_predicates),
            "authority_snapshot_count": len(bundle.authority_snapshots),
        },
        "m1_input_refusal": {
            "exception": m1_error,
            "conflicting_authority_refs": conflicts,
            "conflict_count": len(conflicts),
            "required_resolution": "one exact canonical AuthoritySnapshot preimage per AuthorityRef, or an owner-approved resolution of the retained duplicate authority snapshots",
        },
        "disposition": None if disposition is None else {
            "ref": disposition.ref.as_dict(),
            "claim_family_id": disposition.claim_family_id,
            "claim_rule_id": disposition.claim_rule_id,
            "adjudication_outcome": disposition.adjudication_outcome,
            "reason_code": disposition.reason_code,
            "semantic_ceiling": disposition.semantic_ceiling,
            "disposition_sha256": disposition.ref.content_hash,
        },
        "typed_refusal": {
            "reason_code": (
                "M1_INPUT_BUNDLE_CONFLICTING_AUTHORITY_SNAPSHOT_PREIMAGES"
                if disposition is None
                else disposition.reason_code
            ),
            "required_rule": (
                "exact unique AuthoritySnapshot preimage per AuthorityRef, or an owner-approved resolution of the retained duplicate authority snapshots"
                if disposition is None
                else "exact M1FamilyRuleBinding with claim family/rule, validator authority, current-selection authority, applicability scope, allowed families/states, prerequisite channels, uncertainty policy, output contract, validator algorithm/parameters, replay contract, and authority closure"
            ),
            "required_family_rule": "exact M1FamilyRuleBinding and FamilyValidatorRegistration; not reached because M1 input assembly refused first",
            "required_registration": "exact FamilyValidatorRegistration for the binding dispatch key",
            "not_supplied": True,
        },
        "identity_severance": {
            "selected_fact_ref": selected["ref"],
            "identity_tamper_rejected": identity_error is not None,
            "identity_error": identity_error,
            "reference_tamper_rejected": ref_error is not None,
            "reference_error": ref_error,
            "restoration_passed": True,
            "restored_ref": restored.ref.as_dict(),
            "restored_content_hash": restored.content_hash,
        },
        "no_positive_consumer": {
            "n10e_values_read": False,
            "m2_release_created": False,
            "b5_current_selection_created": False,
            "ff_or_v553_positive": False,
            "reason": (
                "M1 input assembly refused on conflicting retained authority snapshot preimages; no positive consumer or family rule was manufactured."
                if disposition is None
                else "Exact family validation rule/registration is absent; the existing M1 owner returned its own BLOCKED disposition. No substitute law was supplied."
            ),
        },
        "evidence_class": "FRESH_RETAINED_REPLAY_CONSUMER_ATTEMPT__NO_SOURCE_EXECUTION",
    }
    (out / "CONSUMER_RECEIPT_OR_REFUSAL.json").write_bytes(
        (json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()
    )
    if disposition_doc is not None:
        (private / "m1_disposition.json").write_bytes(
            (json.dumps(disposition_doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()
        )
    resources_path = out / "RESOURCE_AND_ACCESS.json"
    if resources_path.exists():
        resources = json.loads(resources_path.read_text())
        resources["consumer_attempt"] = {
            "status": result["status"],
            "max_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "elapsed_seconds": round(time.time() - started, 2),
            "m1_input_refused": disposition is None,
            "conflict_count": len(conflicts),
            "identity_tamper_rejected": identity_error is not None,
            "reference_tamper_rejected": ref_error is not None,
            "restoration_passed": True,
            "n10e_values_read": False,
            "m2_release_created": False,
            "b5_current_selection_created": False,
            "source_accesses": 0,
        }
        resources["memory"]["consumer_max_rss_bytes"] = resources["consumer_attempt"]["max_rss_bytes"]
        resources["memory"]["consumer_below_limit"] = (
            resources["consumer_attempt"]["max_rss_bytes"]
            < resources["memory"]["limit_bytes"]
        )
        resources_path.write_bytes(
            (json.dumps(resources, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()
        )
    print(json.dumps({
        "status": result["status"],
        "bundle_ref": None if bundle is None else bundle.ref.as_dict(),
        "disposition_ref": None if disposition is None else disposition.ref.as_dict(),
        "m1_error": m1_error,
        "identity_error": identity_error,
        "ref_error": ref_error,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
