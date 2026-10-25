"""Typed S48 one-call product-turn refusals."""
from __future__ import annotations


class S48Refusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


class ProductCallError(RuntimeError):
    def __init__(self, code: str, detail: str = "", receipt: dict | None = None):
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.receipt = dict(receipt or {})


__all__ = ["ProductCallError", "S48Refusal"]
