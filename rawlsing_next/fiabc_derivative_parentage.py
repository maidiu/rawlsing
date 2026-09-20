"""Generic immutable derivative-parentage receipts for FIABC CLOSED_35.

The contract is intentionally physical/provenance-only. It does not certify
survey semantics, weights, population claims, or documentary authority.

A derivative is admissible only through an external chain:

    derivative identity
      -> governed producer / operation / reader-config
      -> immutable parent receipt identity
      -> exact canonical source SHA

An asserted source_sha256 inside the derivative payload is never parentage.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

SOURCE_RECEIPT_SCHEMA = "FIABC_CANONICAL_SOURCE_VERIFICATION_RECEIPT@1.0.0"
DERIVATIVE_RECEIPT_SCHEMA = "FIABC_DERIVATIVE_PARENTAGE_RECEIPT@1.0.0"
BUNDLE_SCHEMA = "FIABC_DERIVATIVE_PARENTAGE_BUNDLE@1.0.0"


class ParentageError(ValueError):
    """Raised when an immutable parentage chain is absent or does not close."""


def canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ParentageError("parentage material must be canonical JSON") from exc


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _sha256(value: Any, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or value != value.lower()
        or any(ch not in "0123456789abcdef" for ch in value)
    ):
        raise ParentageError(f"{label} must be lowercase sha256")
    return value


def _nonempty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ParentageError(f"{label} must be nonempty string")
    return value


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ParentageError(f"{label} must be mapping")
    return value


def _exact(actual: Any, expected: Any, label: str) -> None:
    if canonical_bytes(actual) != canonical_bytes(expected):
        raise ParentageError(f"{label} mismatch")


def _validate_producer(producer: Mapping[str, Any], label: str) -> None:
    _nonempty(producer.get("identity"), f"{label}.identity")
    _nonempty(producer.get("code_blob"), f"{label}.code_blob")
    _nonempty(producer.get("version"), f"{label}.version")


def _sealed(unsigned: Mapping[str, Any], identity_key: str) -> dict[str, Any]:
    return {**unsigned, identity_key: canonical_digest(unsigned)}


def mint_source_verification_receipt(
    *,
    source_id: str,
    canonical_source_sha256: str,
    observed_source_sha256: str,
    producer: Mapping[str, Any],
    operation: str,
    reader_config: Mapping[str, Any],
    scope_determinants: Mapping[str, Any],
    currentness_determinants: Mapping[str, Any],
    ownership: Mapping[str, Any],
) -> dict[str, Any]:
    canonical = _sha256(canonical_source_sha256, "canonical source sha")
    observed = _sha256(observed_source_sha256, "observed source sha")
    if observed != canonical:
        raise ParentageError("observed raw source does not equal canonical source SHA")
    producer = dict(_mapping(producer, "producer"))
    _validate_producer(producer, "producer")
    unsigned = {
        "schema": SOURCE_RECEIPT_SCHEMA,
        "canonical_source": {
            "source_id": _nonempty(source_id, "source_id"),
            "sha256": canonical,
        },
        "observation": {
            "observed_sha256": observed,
            "operation": _nonempty(operation, "operation"),
        },
        "producer": producer,
        "reader_config": dict(_mapping(reader_config, "reader_config")),
        "scope_determinants": dict(_mapping(scope_determinants, "scope_determinants")),
        "currentness_determinants": dict(_mapping(currentness_determinants, "currentness_determinants")),
        "ownership": dict(_mapping(ownership, "ownership")),
    }
    return _sealed(unsigned, "receipt_identity")


def verify_source_verification_receipt(
    receipt: Mapping[str, Any] | None,
    *,
    expected_source_id: str | None = None,
    expected_source_sha256: str | None = None,
    expected_receipt_identity: str | None = None,
    expected_operation: str | None = None,
    expected_producer: Mapping[str, Any] | None = None,
    expected_reader_config: Mapping[str, Any] | None = None,
    expected_scope_determinants: Mapping[str, Any] | None = None,
    expected_currentness_determinants: Mapping[str, Any] | None = None,
    expected_ownership: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    if receipt is None:
        raise ParentageError("canonical source verification receipt absent")
    receipt = _mapping(receipt, "source receipt")
    if receipt.get("schema") != SOURCE_RECEIPT_SCHEMA:
        raise ParentageError("source verification receipt schema mismatch")
    identity = _sha256(receipt.get("receipt_identity"), "source receipt identity")
    unsigned = {k: v for k, v in receipt.items() if k != "receipt_identity"}
    if canonical_digest(unsigned) != identity:
        raise ParentageError("source verification receipt identity mismatch")

    canonical = _mapping(receipt.get("canonical_source"), "canonical_source")
    source_id = _nonempty(canonical.get("source_id"), "canonical_source.source_id")
    source_sha = _sha256(canonical.get("sha256"), "canonical_source.sha256")
    observation = _mapping(receipt.get("observation"), "observation")
    if _sha256(observation.get("observed_sha256"), "observed_source_sha256") != source_sha:
        raise ParentageError("source receipt observed SHA does not close to canonical SHA")
    _nonempty(observation.get("operation"), "source verification operation")

    producer = _mapping(receipt.get("producer"), "source producer")
    _validate_producer(producer, "source producer")
    _mapping(receipt.get("reader_config"), "source reader_config")
    _mapping(receipt.get("scope_determinants"), "source scope_determinants")
    _mapping(receipt.get("currentness_determinants"), "source currentness_determinants")
    _mapping(receipt.get("ownership"), "source ownership")

    if expected_source_id is not None and source_id != expected_source_id:
        raise ParentageError("source receipt source_id mismatch")
    if expected_source_sha256 is not None and source_sha != _sha256(expected_source_sha256, "expected source sha"):
        raise ParentageError("source receipt canonical SHA mismatch")
    if expected_receipt_identity is not None and identity != _sha256(expected_receipt_identity, "expected source receipt identity"):
        raise ParentageError("source receipt identity mismatch")
    if expected_operation is not None and observation["operation"] != expected_operation:
        raise ParentageError("source verification operation mismatch")
    if expected_producer is not None:
        _exact(producer, expected_producer, "source producer")
    if expected_reader_config is not None:
        _exact(receipt["reader_config"], expected_reader_config, "source reader config")
    if expected_scope_determinants is not None:
        _exact(receipt["scope_determinants"], expected_scope_determinants, "source scope determinants")
    if expected_currentness_determinants is not None:
        _exact(receipt["currentness_determinants"], expected_currentness_determinants, "source currentness determinants")
    if expected_ownership is not None:
        _exact(receipt["ownership"], expected_ownership, "source ownership")
    return receipt


def mint_derivative_parentage_receipt(
    *,
    source_receipt: Mapping[str, Any],
    derivative_class: str,
    derivative_identity: str,
    derivative_hash: str,
    derivative_metadata: Mapping[str, Any],
    producer: Mapping[str, Any],
    derivation_operation: str,
    reader_config: Mapping[str, Any],
    scope_determinants: Mapping[str, Any],
    currentness_determinants: Mapping[str, Any],
    ownership: Mapping[str, Any],
    replay_parent_receipt_identity: str | None = None,
) -> dict[str, Any]:
    source_receipt = verify_source_verification_receipt(source_receipt)
    canonical_source = dict(source_receipt["canonical_source"])
    producer = dict(_mapping(producer, "producer"))
    _validate_producer(producer, "producer")
    replay = None
    if replay_parent_receipt_identity is not None:
        replay = _sha256(replay_parent_receipt_identity, "replay parent receipt identity")
    unsigned = {
        "schema": DERIVATIVE_RECEIPT_SCHEMA,
        "canonical_source": canonical_source,
        "derivative": {
            "class": _nonempty(derivative_class, "derivative_class"),
            "identity": _nonempty(derivative_identity, "derivative_identity"),
            "hash": _sha256(derivative_hash, "derivative_hash"),
            "metadata": dict(_mapping(derivative_metadata, "derivative_metadata")),
        },
        "producer": producer,
        "derivation_operation": _nonempty(derivation_operation, "derivation_operation"),
        "reader_config": dict(_mapping(reader_config, "reader_config")),
        "scope_determinants": dict(_mapping(scope_determinants, "scope_determinants")),
        "currentness_determinants": dict(_mapping(currentness_determinants, "currentness_determinants")),
        "ownership": dict(_mapping(ownership, "ownership")),
        "parent_receipt_identity": source_receipt["receipt_identity"],
        "replay_parent_receipt_identity": replay,
    }
    return _sealed(unsigned, "receipt_identity")


def verify_derivative_parentage_receipt(
    receipt: Mapping[str, Any] | None,
    *,
    source_receipt: Mapping[str, Any],
    expected_source_id: str,
    expected_source_sha256: str,
    expected_derivative_class: str,
    expected_derivative_identity: str,
    expected_receipt_identity: str | None = None,
    expected_derivative_hash: str,
    expected_derivative_metadata: Mapping[str, Any],
    expected_producer: Mapping[str, Any],
    expected_derivation_operation: str,
    expected_reader_config: Mapping[str, Any],
    expected_scope_determinants: Mapping[str, Any],
    expected_currentness_determinants: Mapping[str, Any],
    expected_ownership: Mapping[str, Any],
    expected_replay_parent_receipt_identity: str | None = None,
) -> Mapping[str, Any]:
    source_receipt = verify_source_verification_receipt(
        source_receipt,
        expected_source_id=expected_source_id,
        expected_source_sha256=expected_source_sha256,
    )
    if receipt is None:
        raise ParentageError("derivative parentage receipt absent")
    receipt = _mapping(receipt, "derivative receipt")
    if receipt.get("schema") != DERIVATIVE_RECEIPT_SCHEMA:
        raise ParentageError("derivative parentage receipt schema mismatch")
    identity = _sha256(receipt.get("receipt_identity"), "derivative receipt identity")
    unsigned = {k: v for k, v in receipt.items() if k != "receipt_identity"}
    if canonical_digest(unsigned) != identity:
        raise ParentageError("derivative parentage receipt identity mismatch")
    if expected_receipt_identity is not None and identity != _sha256(expected_receipt_identity, "expected derivative receipt identity"):
        raise ParentageError("derivative receipt identity mismatch")
    if receipt.get("parent_receipt_identity") != source_receipt["receipt_identity"]:
        raise ParentageError("derivative parent receipt does not close to supplied source receipt")
    _exact(receipt.get("canonical_source"), source_receipt["canonical_source"], "derivative canonical source")

    derivative = _mapping(receipt.get("derivative"), "derivative")
    _nonempty(derivative.get("class"), "derivative.class")
    _nonempty(derivative.get("identity"), "derivative.identity")
    _sha256(derivative.get("hash"), "derivative.hash")
    _mapping(derivative.get("metadata"), "derivative.metadata")
    producer = _mapping(receipt.get("producer"), "derivative producer")
    _validate_producer(producer, "derivative producer")
    _nonempty(receipt.get("derivation_operation"), "derivation_operation")

    _exact(derivative["class"], expected_derivative_class, "derivative class")
    _exact(derivative["identity"], expected_derivative_identity, "derivative identity")
    _exact(derivative["hash"], _sha256(expected_derivative_hash, "expected derivative hash"), "derivative hash")
    _exact(derivative["metadata"], expected_derivative_metadata, "derivative metadata")
    _exact(producer, expected_producer, "derivative producer")
    _exact(receipt["derivation_operation"], expected_derivation_operation, "derivation operation")
    _exact(receipt.get("reader_config"), expected_reader_config, "derivative reader config")
    _exact(receipt.get("scope_determinants"), expected_scope_determinants, "derivative scope determinants")
    _exact(receipt.get("currentness_determinants"), expected_currentness_determinants, "derivative currentness determinants")
    _exact(receipt.get("ownership"), expected_ownership, "derivative ownership")
    expected_replay = expected_replay_parent_receipt_identity
    if expected_replay is not None:
        expected_replay = _sha256(expected_replay, "expected replay parent receipt identity")
    _exact(receipt.get("replay_parent_receipt_identity"), expected_replay, "replay parent receipt identity")
    return receipt


def mint_parentage_bundle(
    *,
    source_receipt: Mapping[str, Any],
    derivative_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    source_receipt = verify_source_verification_receipt(source_receipt)
    if not isinstance(derivative_receipt, Mapping):
        raise ParentageError("derivative receipt must be mapping")
    if derivative_receipt.get("parent_receipt_identity") != source_receipt["receipt_identity"]:
        raise ParentageError("cannot bundle detached derivative receipt")
    unsigned = {
        "schema": BUNDLE_SCHEMA,
        "source_receipt": dict(source_receipt),
        "derivative_receipt": dict(derivative_receipt),
    }
    return _sealed(unsigned, "bundle_identity")


def verify_parentage_bundle(
    bundle: Mapping[str, Any] | None,
    *,
    expected_source_id: str,
    expected_source_sha256: str,
    expected_derivative_class: str,
    expected_derivative_identity: str,
    expected_derivative_receipt_identity: str | None = None,
    expected_derivative_hash: str,
    expected_derivative_metadata: Mapping[str, Any],
    expected_producer: Mapping[str, Any],
    expected_derivation_operation: str,
    expected_reader_config: Mapping[str, Any],
    expected_scope_determinants: Mapping[str, Any],
    expected_currentness_determinants: Mapping[str, Any],
    expected_ownership: Mapping[str, Any],
    expected_source_receipt_identity: str | None = None,
    expected_source_operation: str | None = None,
    expected_source_producer: Mapping[str, Any] | None = None,
    expected_source_reader_config: Mapping[str, Any] | None = None,
    expected_source_scope_determinants: Mapping[str, Any] | None = None,
    expected_source_currentness_determinants: Mapping[str, Any] | None = None,
    expected_source_ownership: Mapping[str, Any] | None = None,
    expected_replay_parent_receipt_identity: str | None = None,
) -> Mapping[str, Any]:
    if bundle is None:
        raise ParentageError("external derivative parentage bundle absent")
    bundle = _mapping(bundle, "parentage bundle")
    if bundle.get("schema") != BUNDLE_SCHEMA:
        raise ParentageError("parentage bundle schema mismatch")
    identity = _sha256(bundle.get("bundle_identity"), "parentage bundle identity")
    unsigned = {k: v for k, v in bundle.items() if k != "bundle_identity"}
    if canonical_digest(unsigned) != identity:
        raise ParentageError("parentage bundle identity mismatch")
    source = verify_source_verification_receipt(
        bundle.get("source_receipt"),
        expected_source_id=expected_source_id,
        expected_source_sha256=expected_source_sha256,
        expected_receipt_identity=expected_source_receipt_identity,
        expected_operation=expected_source_operation,
        expected_producer=expected_source_producer,
        expected_reader_config=expected_source_reader_config,
        expected_scope_determinants=expected_source_scope_determinants,
        expected_currentness_determinants=expected_source_currentness_determinants,
        expected_ownership=expected_source_ownership,
    )
    verify_derivative_parentage_receipt(
        bundle.get("derivative_receipt"),
        source_receipt=source,
        expected_source_id=expected_source_id,
        expected_source_sha256=expected_source_sha256,
        expected_derivative_class=expected_derivative_class,
        expected_derivative_identity=expected_derivative_identity,
        expected_receipt_identity=expected_derivative_receipt_identity,
        expected_derivative_hash=expected_derivative_hash,
        expected_derivative_metadata=expected_derivative_metadata,
        expected_producer=expected_producer,
        expected_derivation_operation=expected_derivation_operation,
        expected_reader_config=expected_reader_config,
        expected_scope_determinants=expected_scope_determinants,
        expected_currentness_determinants=expected_currentness_determinants,
        expected_ownership=expected_ownership,
        expected_replay_parent_receipt_identity=expected_replay_parent_receipt_identity,
    )
    return bundle


def wvs_structural_metadata(doc: Mapping[str, Any]) -> dict[str, Any]:
    doc = _mapping(doc, "WVS structural preimage")
    return {
        "schema": doc.get("schema"),
        "rows": doc.get("rows"),
        "variables": doc.get("variables"),
    }


def r5_root_metadata(root: Mapping[str, Any]) -> dict[str, Any]:
    root = _mapping(root, "R5 root")
    source_ref = _mapping(
        _mapping(root.get("release_identity"), "R5 release_identity").get("source_artifact_ref"),
        "R5 source_artifact_ref",
    )
    return {
        "carrier_id": root.get("carrier_id"),
        "carrier_schema_version": root.get("carrier_schema_version"),
        "typed_codec_version": root.get("typed_codec_version"),
        "logical_stream_digest": root.get("logical_stream_digest"),
        "canonical_row_count": root.get("canonical_row_count"),
        "member_inventory": root.get("member_inventory"),
        "build_config": root.get("build_config"),
        "release_identity": root.get("release_identity"),
        "source_artifact_ref": dict(source_ref),
    }


def assert_r5_root_parent(root: Mapping[str, Any], *, expected_source_sha256: str) -> None:
    source_ref = _mapping(
        _mapping(root.get("release_identity"), "R5 release_identity").get("source_artifact_ref"),
        "R5 source_artifact_ref",
    )
    if _sha256(source_ref.get("content_hash"), "R5 embedded source SHA") != _sha256(
        expected_source_sha256, "expected R5 source SHA"
    ):
        raise ParentageError("R5 embedded source SHA differs from canonical parent")


__all__ = [
    "SOURCE_RECEIPT_SCHEMA",
    "DERIVATIVE_RECEIPT_SCHEMA",
    "BUNDLE_SCHEMA",
    "ParentageError",
    "canonical_bytes",
    "canonical_digest",
    "mint_source_verification_receipt",
    "verify_source_verification_receipt",
    "mint_derivative_parentage_receipt",
    "verify_derivative_parentage_receipt",
    "mint_parentage_bundle",
    "verify_parentage_bundle",
    "wvs_structural_metadata",
    "r5_root_metadata",
    "assert_r5_root_parent",
]
