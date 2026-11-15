"""S39 source-bound generated response over the accepted S37 consumer."""
from __future__ import annotations

from .bootstrap import CUTS, install, roots
from .model import (
    ComparisonRule,
    FULL_RULE,
    GRADE,
    OPTIONS,
    PROVENANCE,
    S39GenerationRefusal,
    generate_choice,
)
from .performer import perform_attempt
from .producer import GeneratedProducer
from .reader import S39ReadRefusal, read_generation
from .session import S39_SCHEMA, S39GeneratedSession
from .sources import context_records, make_source

__all__ = [
    "CUTS",
    "ComparisonRule",
    "FULL_RULE",
    "GRADE",
    "GeneratedProducer",
    "OPTIONS",
    "PROVENANCE",
    "S39GenerationRefusal",
    "S39ReadRefusal",
    "S39GeneratedSession",
    "S39_SCHEMA",
    "context_records",
    "generate_choice",
    "install",
    "make_source",
    "perform_attempt",
    "read_generation",
    "roots",
]
