"""Typed S44 no-draw and root refusals."""
from __future__ import annotations


class S44Refusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


__all__ = ["S44Refusal"]
