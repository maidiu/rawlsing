"""S48 one-call continuing-turn product orchestration."""
from .bootstrap import install
from .errors import ProductCallError, S48Refusal
from .product import (
    CANDIDATES,
    PRODUCT_CONFIG,
    PRODUCT_MODEL,
    PRODUCT_SCHEMA,
    PRODUCT_VARIANT,
    build_payload,
    build_prompt,
    parse_envelope,
    run_product_cli,
)
from .session import PRODUCT_TURN_KIND, S48_SCHEMA, S48Session, SCI05_REASON

install()

__all__ = [
    "CANDIDATES", "PRODUCT_CONFIG", "PRODUCT_MODEL", "PRODUCT_SCHEMA",
    "PRODUCT_TURN_KIND", "PRODUCT_VARIANT", "ProductCallError", "S48Refusal",
    "S48Session", "S48_SCHEMA", "SCI05_REASON", "build_payload", "build_prompt",
    "parse_envelope", "run_product_cli",
]
