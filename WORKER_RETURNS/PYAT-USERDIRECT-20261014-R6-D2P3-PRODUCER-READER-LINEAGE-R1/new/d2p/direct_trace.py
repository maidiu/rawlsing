"""Trace the accepted direct-producer transport with exact field determinants."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_learned_world_composition import (
    DirectProducerIngress,
    LearnedWorldProductContractBinding,
    compose_direct_producer,
)
from new.d2p.single_registry import GSS, NCA, produce_registry


def _tref(kind: str, ident: str) -> ExactRef:
    digest = semantic_hash({"schema": "D2P3_TRANSPORT_REF@1", "kind": kind, "id": ident})
    return ExactRef(kind, f"urn:test:d2p3:{kind.lower()}:{ident}:sha256:{digest}", digest)


def _field_exact_ref(field_ref: str) -> ExactRef:
    if not field_ref.startswith("D2P_TESTONLY_FIELD:"):
        raise ValueError("D2P3 field ref required")
    digest = field_ref.split(":", 1)[1]
    return ExactRef("D2P_TESTONLY_FIELD", field_ref, digest)


def trace(rows: list[dict[str, Any]]) -> dict[str, Any]:
    registry = produce_registry(rows)
    refs = registry.refs_by_role()
    determinant_refs = tuple(_field_exact_ref(refs[role]) for role in (GSS, NCA))
    contract = LearnedWorldProductContractBinding(
        route="DIRECT_PRODUCER",
        product_family_ref=_tref("PRODUCT_FAMILY", "D2P3_TEST_ONLY_TWO_FIELDS"),
        producer_owner_ref=_tref("PRODUCER_OWNER", "D2P3_SOURCEFREE_TEST_ONLY_FIELD_PRODUCER"),
        producer_contract_ref=_tref("PRODUCER_CONTRACT", "D2P3_TEST_ONLY_TWO_FIELD_CONTRACT"),
        release_subject_kind="TEST_ONLY_EXTERNAL_PUBLISHED_AGGREGATE",
        selection_scope_ref=_tref("SELECTION_SCOPE", "HISTORICAL_PUBLICATION_AWARE_2022"),
        producer_permission_ceiling_ref=_tref("PERMISSION_CEILING", "TEST_ONLY_NO_EXTERNAL_USE_GRANT"),
        consumer_product_purpose_ref=_tref("CONSUMER_PURPOSE", "SOURCEFREE_HISTORICAL_CONTEXT"),
        direct_producer_route_authority_ref=_tref(
            "ROUTE_AUTHORITY", "TEST_ONLY_DIRECT_PRODUCER_ROUTE_NOT_N5N6_N7_N9_OC05"
        ),
        direct_consumer_acceptance_ref=_tref(
            "CONSUMER_ACCEPTANCE", "TEST_ONLY_CONSUMER_ACCEPTANCE_NOT_ADOPTED"
        ),
    )
    ingress = DirectProducerIngress(
        subject_ref=_tref("SUBJECT", "SOURCEFREE_HISTORICAL_CONTEXT"),
        producer_owner_ref=contract.producer_owner_ref,
        producer_contract_ref=contract.producer_contract_ref,
        typed_state="SOURCEFREE_TEST_ONLY_TWO_FIELDS_BOUND",
        determinant_refs=determinant_refs,
        replay_ref=_tref("REPLAY", "D2P3_TEST_ONLY_REPLAY"),
        explanation_ref=_tref("EXPLANATION", "D2P3_TEST_ONLY_EXPLANATION"),
        semantic_ceiling="TEST_ONLY_NO_ISSUANCE",
    )
    result = compose_direct_producer(contract=contract, ingress=ingress)
    receipt = result.receipt
    return {
        "schema": "D2P3_DIRECT_TRANSPORT_TRACE@1",
        "transport_module": "rawlsing_next.pre553_learned_world_composition",
        "transport_module_file": __import__("rawlsing_next.pre553_learned_world_composition", fromlist=["__file__"]).__file__,
        "status": "EXECUTED",
        "producer_refs": refs,
        "determinant_refs": [ref.as_dict() for ref in determinant_refs],
        "determinant_content_hashes_match": all(
            ref.content_hash == registry.dereference(ref.object_id)["field_ref"].split(":", 1)[1]
            for ref in determinant_refs
        ),
        "receipt_terminal_state": receipt.terminal_state,
        "receipt_reason_code": receipt.reason_code,
        "receipt_route_taken": receipt.route_taken,
        "issued_N5N6": False,
        "issued_EE13": False,
        "operative_OC05": False,
        "semantic_ceiling": receipt.semantic_ceiling,
    }


if __name__ == "__main__":
    import sys
    rows = json.loads(Path(sys.argv[1]).read_text())["fields"]
    print(json.dumps(trace(rows), indent=2, sort_keys=True))
