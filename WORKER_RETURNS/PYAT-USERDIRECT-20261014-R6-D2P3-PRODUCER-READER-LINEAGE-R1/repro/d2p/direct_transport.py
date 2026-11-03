"""D2P sourcefree handoff into the existing direct-producer transport.

Imports the REAL accepted `compose_direct_producer` (and its contract/ingress
types) from rawlsing_next.pre553_learned_world_composition (pinned blob
4a8e27a226a9c06606f5ba493d2cc7356d491a7b) and records actual module __file__,
function calls and receipt terminal states. The contract presented here is
explicitly TEST_ONLY: TEST_ONLY route authority and TEST_ONLY consumer
acceptance. A test-only contract cannot constitute N5/N6 issuance, EE13,
N7, N9 or OC05; the transport receipt itself enforces that ceiling.
"""
from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Mapping

TRANSPORT_IMPORT_ERROR: str | None = None

try:
    import rawlsing_next.pre553_learned_world_composition as _lwc
    from rawlsing_next.pre553_learned_world_composition import (
        compose_direct_producer,
        DirectProducerIngress,
        LearnedWorldProductContractBinding,
    )
    TRANSPORT_MODULE_FILE = _lwc.__file__
    TRANSPORT_AVAILABLE = True
except Exception as exc:  # pragma: no cover - import failure recorded, not raised
    TRANSPORT_IMPORT_ERROR = f"{type(exc).__name__}: {exc}"
    TRANSPORT_AVAILABLE = False
    TRANSPORT_MODULE_FILE = None


def _sha256(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _tref(kind: str, ident: str) -> Any:
    from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
    material = {"schema": "D2P_TEST_ONLY_TRANSPORT_REF@1", "kind": kind, "id": ident}
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:test:d2p:{kind.lower()}:{ident}:sha256:{digest}", digest)


def handoff_two_fields(
    fields: Mapping[str, Mapping[str, Any]],
    *,
    subject_kind: str = "SOURCEFREE_HISTORICAL_CONTEXT",
) -> dict[str, Any]:
    """Hand the two produced fields into the real direct-producer transport.

    Returns a call trace with actual module paths/function names and the
    transport receipt's terminal state and reason, or an exact NOT_EXECUTED
    blocker if the accepted owner cannot be imported under current rights/runtime.
    """
    trace: dict[str, Any] = {
        "transport_module": "rawlsing_next.pre553_learned_world_composition",
        "transport_module_file": TRANSPORT_MODULE_FILE,
        "transport_function": "compose_direct_producer",
        "executed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "calls": [],
    }
    if not TRANSPORT_AVAILABLE:
        trace["status"] = "NOT_EXECUTED"
        trace["blocker"] = TRANSPORT_IMPORT_ERROR
        trace["blocker_class"] = "MISSING_OWNER_IMPORT"
        return trace

    determinant_refs = []
    for role in ("GSS_RURAL_LIGHTING", "NCA_NATIONAL_MOBILE_DATA"):
        determinant_refs.append(_tref("FIELD_DETERMINANT", fields[role]["field_ref"]))

    contract = LearnedWorldProductContractBinding(
        route="DIRECT_PRODUCER",
        product_family_ref=_tref("PRODUCT_FAMILY", "D2P_TEST_ONLY_TWO_FIELDS"),
        producer_owner_ref=_tref("PRODUCER_OWNER", "D2P_SOURCEFREE_TEST_ONLY_FIELD_PRODUCER"),
        producer_contract_ref=_tref("PRODUCER_CONTRACT", "D2P_TEST_ONLY_TWO_FIELD_CONTRACT"),
        release_subject_kind="TEST_ONLY_EXTERNAL_PUBLISHED_AGGREGATE",
        selection_scope_ref=_tref("SELECTION_SCOPE", "HISTORICAL_PUBLICATION_AWARE_2022"),
        producer_permission_ceiling_ref=_tref("PERMISSION_CEILING", "TEST_ONLY_NO_EXTERNAL_USE_GRANT"),
        consumer_product_purpose_ref=_tref("CONSUMER_PURPOSE", "SOURCEFREE_HISTORICAL_CONTEXT"),
        direct_producer_route_authority_ref=_tref(
            "ROUTE_AUTHORITY", "TEST_ONLY_DIRECT_PRODUCER_ROUTE_NOT_N5N6_N7_N9_OC05"),
        direct_consumer_acceptance_ref=_tref(
            "CONSUMER_ACCEPTANCE", "TEST_ONLY_CONSUMER_ACCEPTANCE_NOT_ADOPTED"),
    )
    ingress = DirectProducerIngress(
        subject_ref=_tref("SUBJECT", subject_kind),
        producer_owner_ref=_tref("PRODUCER_OWNER", "D2P_SOURCEFREE_TEST_ONLY_FIELD_PRODUCER"),
        producer_contract_ref=_tref("PRODUCER_CONTRACT", "D2P_TEST_ONLY_TWO_FIELD_CONTRACT"),
        typed_state="SOURCEFREE_TEST_ONLY_TWO_FIELDS_BOUND",
        determinant_refs=tuple(determinant_refs),
        replay_ref=_tref("REPLAY", "D2P_TEST_ONLY_REPLAY"),
        explanation_ref=_tref("EXPLANATION", "D2P_TEST_ONLY_EXPLANATION"),
        semantic_ceiling="TEST_ONLY_NO_ISSUANCE",
    )
    trace["calls"].append({
        "function": "compose_direct_producer",
        "module_file": TRANSPORT_MODULE_FILE,
        "contract_route": "DIRECT_PRODUCER",
        "determinant_count": len(determinant_refs),
    })
    result = compose_direct_producer(contract=contract, ingress=ingress)
    receipt = result.receipt
    trace["calls"].append({
        "function": "compose_direct_producer.result",
        "terminal_state": receipt.terminal_state,
        "reason_code": receipt.reason_code,
        "route_taken": receipt.route_taken,
    })
    trace["status"] = "EXECUTED"
    trace["receipt_terminal_state"] = receipt.terminal_state
    trace["receipt_reason_code"] = receipt.reason_code
    trace["receipt_route_taken"] = receipt.route_taken
    return trace
