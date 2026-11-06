"""Errors raised by the R157 source-configuration foundation."""
from __future__ import annotations


class SourceConfigurationError(ValueError):
    """Base configuration error."""


class SourceConfigurationSchemaError(SourceConfigurationError):
    """The serialized configuration is not closed/valid."""


class SourceConfigurationBindingError(SourceConfigurationError):
    """The active source/fixture binding is inconsistent with the config."""


class SourceConfigurationFactoryError(SourceConfigurationError):
    """The validated config cannot be mapped to the native owner."""


class SourceConfigurationEvidenceError(SourceConfigurationError):
    """Pinned evidence is missing, malformed, or inconsistent."""
