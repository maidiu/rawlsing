"""Typed S47 interval-to-C9 conditioning refusals."""
from __future__ import annotations


class S47Refusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


__all__ = ["S47Refusal"]
