"""Config-to-source-read transport glue for the existing admission owner.

This module does not grant source rights.  It only turns a validated source
configuration's exact identity/reader fields into the existing request/decision
transport and passes the qualified reader configuration to the unchanged
physical decoder.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_source_read_admission import (
    SourceReadRequest,
    SourceReaderConfiguration,
    decode_with_source_read_permission,
)

from .errors import SourceConfigurationBindingError, SourceConfigurationEvidenceError
from .schema import IDENTITY_CLASS_ORIGINAL, SourceConfig


def _doc(config: SourceConfig | Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(config, SourceConfig):
        return config.document
    if not isinstance(config, Mapping):
        raise SourceConfigurationBindingError("source configuration must be SourceConfig or mapping")
    return config


def _identity(doc: Mapping[str, Any]) -> Mapping[str, Any]:
    identity = doc.get("identity")
    if not isinstance(identity, Mapping):
        raise SourceConfigurationBindingError("source configuration lacks identity")
    return identity


def _require_original_binding(doc: Mapping[str, Any]) -> None:
    binding = doc.get("binding")
    if not isinstance(binding, Mapping):
        raise SourceConfigurationBindingError("source configuration lacks binding")
    if binding.get("identity_class") != IDENTITY_CLASS_ORIGINAL:
        raise SourceConfigurationBindingError(
            "source-read transport applies only to an ORIGINAL_SOURCE config; fixtures are not original reads")


def reader_configuration_from_config(
    config: SourceConfig | Mapping[str, Any],
) -> SourceReaderConfiguration:
    """Extract the exact qualified reader configuration from identity.reader."""
    doc = _doc(config)
    _require_original_binding(doc)
    identity = _identity(doc)
    reader = identity.get("reader")
    if not isinstance(reader, Mapping):
        raise SourceConfigurationBindingError("identity.reader is required")
    config_ref = exact_ref(reader["configuration_ref"], "identity.reader.configuration_ref")
    encoding = reader.get("encoding")
    if encoding is None:
        return SourceReaderConfiguration(
            source_sha256=identity["expected_source_sha256"],
            configuration_ref=config_ref,
        )
    if not isinstance(encoding, Mapping):
        raise SourceConfigurationBindingError("identity.reader.encoding must be object or null")
    return SourceReaderConfiguration(
        source_sha256=identity["expected_source_sha256"],
        encoding=encoding["value"],
        authority_status=encoding["authority_status"],
        configuration_ref=config_ref,
    )


def source_read_request_from_config(
    config: SourceConfig | Mapping[str, Any],
    *,
    host: str,
    purpose: str,
    consumer_use: str,
    semantic_use_scope: Sequence[str],
    metadata_freeze_refs: Sequence[Any] | None = None,
    custody_locator_binding: str | None = None,
) -> SourceReadRequest:
    """Build the existing metadata-only request without opening source bytes."""
    doc = _doc(config)
    _require_original_binding(doc)
    identity = _identity(doc)
    locator = identity.get("locator")
    if not isinstance(locator, Mapping):
        raise SourceConfigurationBindingError("identity.locator is required")
    if custody_locator_binding is None:
        if locator.get("root") == "SOURCE_ROOT":
            custody_locator_binding = locator.get("relative_path")
        elif locator.get("root") == "EXTERNAL_LOCATOR_ID":
            custody_locator_binding = locator.get("locator_id")
    if not isinstance(custody_locator_binding, str) or not custody_locator_binding.strip():
        raise SourceConfigurationBindingError("an exact custody locator binding is required")
    if metadata_freeze_refs is None:
        metadata_freeze_refs = (identity["metadata_witness_ref"],)
    if isinstance(semantic_use_scope, (str, bytes)) or not semantic_use_scope:
        raise SourceConfigurationEvidenceError("semantic_use_scope must be an explicit non-empty scope")
    return SourceReadRequest(
        source_id=identity["source_id"],
        source_sha256=identity["expected_source_sha256"],
        source_format=identity["source_format"],
        custody_locator_binding=custody_locator_binding,
        host=host,
        purpose=purpose,
        consumer_use=consumer_use,
        metadata_freeze_refs=tuple(exact_ref(x, "metadata_freeze_ref") for x in metadata_freeze_refs),
        semantic_use_scope=tuple(semantic_use_scope),
    )


def decode_config_with_source_read_permission(
    config: SourceConfig | Mapping[str, Any],
    *,
    source_path: Any,
    resolver: Any,
    host: str,
    purpose: str,
    consumer_use: str,
    semantic_use_scope: Sequence[str],
    metadata_freeze_refs: Sequence[Any] | None = None,
    custody_locator_binding: str | None = None,
):
    """Decode through the existing source-read owner with config reader facts."""
    request = source_read_request_from_config(
        config,
        host=host,
        purpose=purpose,
        consumer_use=consumer_use,
        semantic_use_scope=semantic_use_scope,
        metadata_freeze_refs=metadata_freeze_refs,
        custody_locator_binding=custody_locator_binding,
    )
    reader = reader_configuration_from_config(config)
    return decode_with_source_read_permission(
        source_path=source_path, request=request, resolver=resolver, reader=reader)


__all__ = [
    "reader_configuration_from_config",
    "source_read_request_from_config",
    "decode_config_with_source_read_permission",
]
