#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping

from rawlsing_next.pre553_carrier_execution import materialize_public_object
from rawlsing_next.pre553_empirical_objects import canonicalize
from rawlsing_next.pre553_learned_empirical_adjudication import (
    M1ValidatorRegistry,
    adjudicate_learned_empirical,
    build_m1_adjudication_input_bundle,
)

PRODUCER_COMMIT = "6286c15bea78758a91686d60e036680bb26c6674"
PRODUCER_PATH = (
    "WORKER_RETURNS/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1/"
    "source_retry_evidence/zero_source_resume_receipt.json"
)
SELECTED_RECEIPT = (
    "urn:rawlsing:pre553:DiscoveryResultReceipt:sha256:"
    "006df79b240d7314d113a86d37ab28c02325af642681c40460977a69d70547b8"
)


class CatalogRepairError(RuntimeError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            canonicalize(value),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


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
        raise CatalogRepairError("object round-trip drift")
    return obj


def authority_key(snapshot: Any) -> tuple[str, str, str]:
    return (
        snapshot.authority_id,
        snapshot.authority_version,
        snapshot.authority_content_hash,
    )


def ref_key(ref: Any) -> tuple[str, str, str]:
    value = canonicalize(ref)
    return (value["kind"], value["object_id"], value["content_hash"])


def authority_ref_for(key: tuple[str, str, str]) -> Mapping[str, str]:
    return {
        "authority_id": key[0],
        "authority_version": key[1],
        "authority_content_hash": key[2],
    }


def producer_catalog() -> Mapping[str, Any]:
    raw = subprocess.check_output(
        ["git", "show", f"{PRODUCER_COMMIT}:{PRODUCER_PATH}"],
        cwd=Path.cwd(),
    )
    doc = json.loads(raw)
    return doc["audit"]["common_execution_binding"]["runtime_catalog"]


def select_receipt_objects(private: Path, index: list[Mapping[str, Any]]) -> Mapping[str, Any]:
    by_id = {item["ref"]["object_id"]: item for item in index}
    receipt = load_object(private, by_id[SELECTED_RECEIPT])
    facts: dict[str, Any] = {}
    queries: dict[str, Any] = {}
    predicates: dict[str, Any] = {}
    fact_refs = [canonicalize(ref) for ref in receipt.empirical_fact_refs]
    fact_refs += [canonicalize(ref) for ref in receipt.validation_fact_refs]
    for ref in fact_refs:
        facts[ref["object_id"]] = load_object(private, by_id[ref["object_id"]])
    for fact in facts.values():
        for name in ("empirical_query_spec_ref", "condition_predicate_ref"):
            ref = canonicalize(getattr(fact, name))
            if name == "empirical_query_spec_ref":
                queries[ref["object_id"]] = load_object(private, by_id[ref["object_id"]])
            else:
                predicates[ref["object_id"]] = load_object(private, by_id[ref["object_id"]])
    identity = receipt.candidate_identity
    for role in identity["query_roles"]:
        qref = role["query_ref"]["object_id"]
        pref = role["predicate_ref"]["object_id"]
        queries[qref] = load_object(private, by_id[qref])
        predicates[pref] = load_object(private, by_id[pref])
    for ref in (
        canonicalize(receipt.winning_predicate_ref),
        canonicalize(receipt.discovery_authority_ref),
    ):
        if ref["kind"].startswith("EmpiricalPredicate"):
            predicates[ref["object_id"]] = load_object(private, by_id[ref["object_id"]])
    discovery = load_object(
        private, by_id[canonicalize(receipt.discovery_authority_ref)["object_id"]]
    )
    required_keys: set[tuple[str, str, str]] = set()
    for obj in (
        receipt,
        *facts.values(),
        *queries.values(),
        *predicates.values(),
        discovery,
    ):
        for auth in obj.authority_snapshot_refs:
            required_keys.add(
                (auth.authority_id, auth.authority_version, auth.authority_content_hash)
            )
    return {
        "receipt": receipt,
        "facts": tuple(facts.values()),
        "queries": tuple(queries.values()),
        "predicates": tuple(predicates.values()),
        "discovery": discovery,
        "required_authority_keys": required_keys,
        "query_roles": identity["query_roles"],
    }


def make_bundle(
    catalog: tuple[Any, ...],
    selection: Mapping[str, Any],
    tail: Mapping[str, Any],
) -> Any:
    release_ref = tail["projection_and_release_refs"]["release_refs"][0]
    replay_ref = tail["projection_and_release_refs"]["release_replay_refs"][0]
    return build_m1_adjudication_input_bundle(
        requested_claim_family_id="NOT_BOUND",
        requested_claim_rule_id=selection["receipt"].candidate_identity["rule_id"],
        selected_discovery_receipts=(selection["receipt"],),
        discovery_authority_catalog=(selection["discovery"],),
        empirical_fact_catalog=selection["facts"],
        empirical_query_catalog=selection["queries"],
        empirical_predicate_catalog=selection["predicates"],
        authority_snapshots=catalog,
        requested_scope={
            "source_identity": tail["source_identity"],
            "frontier_manifest": tail["frontier_manifest"],
            "claim_family_selection": "NOT_BOUND__NO_FAMILY_RULE_ISSUED",
        },
        additional_dependency_refs=(release_ref, replay_ref),
    )


def call_adjudication(bundle: Any) -> Mapping[str, Any]:
    disposition = adjudicate_learned_empirical(
        bundle,
        None,
        validator_registry=M1ValidatorRegistry(),
    )
    return {
        "disposition_ref": disposition.ref.as_dict(),
        "adjudication_outcome": disposition.adjudication_outcome,
        "reason_code": disposition.reason_code,
        "claim_family_id": disposition.claim_family_id,
        "claim_rule_id": disposition.claim_rule_id,
        "semantic_ceiling": disposition.semantic_ceiling,
    }


def exception_record(exc: BaseException) -> Mapping[str, Any]:
    return {"type": type(exc).__name__, "message": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    private = args.private.resolve()
    out = args.out.resolve()
    index = load_index(private)
    by_id = {item["ref"]["object_id"]: item for item in index}
    authority_metas = [x for x in index if x["schema_id"] == "AuthoritySnapshot"]
    authority_objects = [load_object(private, x) for x in authority_metas]
    authority_by_key: dict[tuple[str, str, str], list[Any]] = defaultdict(list)
    for obj in authority_objects:
        authority_by_key[authority_key(obj)].append(obj)

    tail = json.loads((private / "material_tail.json").read_text())
    producer = producer_catalog()
    producer_objects = [
        load_object(private, by_id[ref["object_id"]])
        for ref in producer["authorities"]
    ]
    producer_by_key = {authority_key(obj): obj for obj in producer_objects}
    if len(producer_by_key) != len(producer_objects):
        raise CatalogRepairError("producer authority catalog is not unique by AuthorityRef")

    selection = select_receipt_objects(private, index)
    producer_refs = [obj.ref.as_dict() for obj in producer_objects]
    selected_refs: list[Any] = list(producer_objects)
    support_refs = []
    missing = []
    ambiguous = []
    for key in sorted(selection["required_authority_keys"]):
        if key in producer_by_key:
            continue
        candidates = authority_by_key.get(key, [])
        if len(candidates) == 1:
            selected_refs.append(candidates[0])
            support_refs.append({
                "authority_ref": authority_ref_for(key),
                "snapshot_ref": candidates[0].ref.as_dict(),
                "basis": "UNIQUE_REQUIRED_FULL_CUSTODY_PREIMAGE__ABSENT_FROM_PRODUCER_CATALOG",
            })
        elif not candidates:
            missing.append(authority_ref_for(key))
        else:
            ambiguous.append({
                "authority_ref": authority_ref_for(key),
                "candidate_refs": [x.ref.as_dict() for x in candidates],
            })
    if missing or ambiguous:
        result = {
            "schema": "PYAT_R129_CATALOG_BINDING_REFUSAL@1",
            "status": "REFUSED__PRODUCER_CATALOG_DOES_NOT_UNIQUELY_BIND_REQUIRED_SNAPSHOTS",
            "missing": missing,
            "ambiguous": ambiguous,
        }
        (out / "CATALOG_BINDINGS.json").write_bytes(canonical_bytes(result))
        return 2

    selected_by_key = {authority_key(obj): obj for obj in selected_refs}
    duplicate_keys = sorted(
        key for key, objects in authority_by_key.items() if len(objects) > 1
    )
    all24 = tuple(authority_objects)
    baseline = None
    try:
        baseline_bundle = make_bundle(all24, selection, tail)
        baseline = {"unexpected_success_bundle_ref": baseline_bundle.ref.as_dict()}
    except Exception as exc:
        baseline = exception_record(exc)

    selected_catalog = tuple(selected_refs)
    bundle = make_bundle(selected_catalog, selection, tail)
    disposition = call_adjudication(bundle)

    sever_key = sorted(selection["required_authority_keys"])[0]
    sever_catalog = tuple(
        obj for obj in selected_catalog if authority_key(obj) != sever_key
    )
    sever = None
    try:
        sever_bundle = make_bundle(sever_catalog, selection, tail)
        sever = call_adjudication(sever_bundle)
    except Exception as exc:
        sever = {"exception": exception_record(exc)}

    restore_bundle = make_bundle(selected_catalog, selection, tail)
    restored = call_adjudication(restore_bundle)
    if restored["disposition_ref"] != disposition["disposition_ref"]:
        raise CatalogRepairError("restored disposition does not match original")

    bindings = {
        "schema": "PYAT_R129_CATALOG_BINDINGS@1",
        "status": "BOUND__PRODUCER_CATALOG_PLUS_UNIQUE_REQUIRED_SUPPORT",
        "producer_evidence": {
            "commit": PRODUCER_COMMIT,
            "path": PRODUCER_PATH,
            "binding_identity": json.loads(
                subprocess.check_output(
                    ["git", "show", f"{PRODUCER_COMMIT}:{PRODUCER_PATH}"],
                    cwd=Path.cwd(),
                )
            )["audit"]["common_execution_binding"]["binding_identity"],
            "catalog_identity": producer["catalog_identity"],
        },
        "producer_catalog_authorities": [
            {
                "authority_ref": authority_ref_for(authority_key(obj)),
                "snapshot_ref": obj.ref.as_dict(),
            }
            for obj in producer_objects
        ],
        "required_authority_refs": [
            authority_ref_for(key)
            for key in sorted(selection["required_authority_keys"])
        ],
        "selected_catalog_authorities": [
            {
                "authority_ref": authority_ref_for(authority_key(obj)),
                "snapshot_ref": obj.ref.as_dict(),
                "source": (
                    "PRODUCER_RUNTIME_CATALOG"
                    if authority_key(obj) in producer_by_key
                    else "UNIQUE_REQUIRED_FULL_CUSTODY_SUPPORT"
                ),
            }
            for obj in selected_catalog
        ],
        "support_bindings": support_refs,
        "producer_duplicate_keys": [
            {
                "authority_ref": authority_ref_for(key),
                "full_custody_snapshot_refs": [
                    obj.ref.as_dict() for obj in authority_by_key[key]
                ],
                "selected_snapshot_ref": producer_by_key[key].ref.as_dict(),
                "selection_basis": "EXACT_OBJECT_REF_FROM_PRODUCER_RUNTIME_CATALOG",
            }
            for key in duplicate_keys
            if key in producer_by_key
        ],
        "unselected_full_custody_authorities": [
            obj.ref.as_dict()
            for obj in authority_objects
            if obj.ref.object_id not in {
                selected.ref.object_id for selected in selected_catalog
            }
        ],
        "rules": {
            "arbitrary_dedup": False,
            "hash_sorted_winner": False,
            "snapshot_merge_or_rewrite": False,
            "new_authority": False,
            "producer_catalog_unchanged": True,
            "support_only_if_required_and_unique": True,
        },
    }
    (out / "CATALOG_BINDINGS.json").write_bytes(canonical_bytes(bindings))

    receipt = {
        "schema": "PYAT_R129_EXACT_NATIVE_CALL_RECEIPT@1",
        "status": "M1_INPUT_BUILT__NEXT_TYPED_REFUSAL__FAMILY_RULE_UNBOUND",
        "evidence_class": "FRESH_RETAINED_M1_INPUT_COMPOSITION__NO_SOURCE_EXECUTION",
        "selected_receipt_ref": selection["receipt"].ref.as_dict(),
        "selected_fact_refs": [obj.ref.as_dict() for obj in selection["facts"]],
        "selected_query_refs": [obj.ref.as_dict() for obj in selection["queries"]],
        "selected_predicate_refs": [obj.ref.as_dict() for obj in selection["predicates"]],
        "selected_discovery_authority_ref": selection["discovery"].ref.as_dict(),
        "selected_snapshot_refs": [obj.ref.as_dict() for obj in selected_catalog],
        "producer_catalog_ref_count": len(producer_objects),
        "selected_snapshot_count": len(selected_catalog),
        "required_snapshot_count": len(selection["required_authority_keys"]),
        "r128_conflicting_all24_replay": baseline,
        "m1_build": {
            "bundle_ref": bundle.ref.as_dict(),
            "authority_snapshot_count": len(bundle.authority_snapshots),
            "family_rule_binding": None,
            "validator_registry": "EMPTY",
        },
        "next_native_disposition": disposition,
        "sever_one_required_snapshot": {
            "removed_authority_ref": authority_ref_for(sever_key),
            "result": sever,
        },
        "restoration": {
            "restored_disposition_matches": True,
            "disposition": restored,
        },
        "no_positive_consumer": {
            "m2_release_created": False,
            "b5_current_selection_created": False,
            "n10e_values_read": False,
            "ff_or_v553_positive": False,
            "reason": "Exact family rule/validator is unbound; existing M1 owner returned its own typed refusal.",
        },
    }
    (out / "exactNATIVE_CALL_RECEIPT.json").write_bytes(canonical_bytes(receipt))
    print(json.dumps({
        "status": receipt["status"],
        "bundle_ref": bundle.ref.as_dict(),
        "next_reason_code": disposition["reason_code"],
        "selected_snapshot_count": len(selected_catalog),
        "sever_result": sever,
        "restored_reason_code": restored["reason_code"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
