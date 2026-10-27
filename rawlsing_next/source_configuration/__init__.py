"""R157 source-configuration foundation.

The package is deliberately a thin, data-driven configuration layer over the
existing ``GovernedC11Projection`` / source-backed C11 owner.  It does not
replace the native engine, infer missing source semantics, or turn a metadata
identity into an empirical claim.
"""
from __future__ import annotations

from .errors import (
    SourceConfigurationBindingError,
    SourceConfigurationError,
    SourceConfigurationEvidenceError,
    SourceConfigurationFactoryError,
    SourceConfigurationSchemaError,
)
from .schema import (
    SCHEMA_ID,
    SourceConfig,
    canonical_config_hash,
    config_file_sha256,
    load_source_config,
    validate_source_config,
)
from .factory import (
    build_governed_c11_projection,
    build_source_backed_c11_repository_from_config,
    build_validated_c11_release_from_config,
    construct_governed_c11_projection,
)
from .fixture import (
    FIXTURE_SCHEMA_ID,
    fixture_document_sha256,
    fixture_stream_from_document,
    load_fixture_stream,
)

__all__ = [
    "SCHEMA_ID", "SourceConfig", "SourceConfigurationError",
    "SourceConfigurationSchemaError", "SourceConfigurationBindingError",
    "SourceConfigurationFactoryError", "SourceConfigurationEvidenceError",
    "canonical_config_hash", "config_file_sha256", "load_source_config",
    "validate_source_config", "build_governed_c11_projection",
    "construct_governed_c11_projection", "build_validated_c11_release_from_config",
    "build_source_backed_c11_repository_from_config", "FIXTURE_SCHEMA_ID",
    "fixture_document_sha256", "fixture_stream_from_document", "load_fixture_stream",
]
