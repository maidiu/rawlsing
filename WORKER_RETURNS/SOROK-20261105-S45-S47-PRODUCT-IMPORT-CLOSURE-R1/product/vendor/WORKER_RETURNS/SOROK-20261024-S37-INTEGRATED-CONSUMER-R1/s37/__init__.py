"""S37 integrated TEST_ONLY consumer over M35, S36, JOIN-E and language."""
from __future__ import annotations

from .bootstrap import CUTS, install, origins, roots
from .producer import IntegratedProducer, S37Refusal
from .product import S37TargetlessProduct, validate_s37_product
from .reader import S37ReadRefusal, read_committed_s36
from .session import S37IntegratedSession

__all__ = [
    "CUTS",
    "IntegratedProducer",
    "S37IntegratedSession",
    "S37ReadRefusal",
    "S37Refusal",
    "S37TargetlessProduct",
    "install",
    "origins",
    "read_committed_s36",
    "roots",
    "validate_s37_product",
]
