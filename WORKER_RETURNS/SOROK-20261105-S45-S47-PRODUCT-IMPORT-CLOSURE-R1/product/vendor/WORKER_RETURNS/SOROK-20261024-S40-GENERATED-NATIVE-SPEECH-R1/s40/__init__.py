"""S40 generated native-speech and labeled English view over S39/S37."""
from __future__ import annotations

from .bootstrap import CUTS, install, roots
from .language import (
    S40_ATOMS,
    S40_PAIRS,
    S40_REGISTRY_HASH,
    S40LanguageRefusal,
    realize_speaking,
)
from .performer import perform_generated_attempt
from .reader import S40ReadRefusal, read_s40
from .session import S40_SCHEMA, S40GeneratedSession

__all__ = [
    "CUTS",
    "S40_ATOMS",
    "S40_PAIRS",
    "S40_REGISTRY_HASH",
    "S40LanguageRefusal",
    "S40ReadRefusal",
    "S40GeneratedSession",
    "S40_SCHEMA",
    "install",
    "perform_generated_attempt",
    "read_s40",
    "realize_speaking",
    "roots",
]
