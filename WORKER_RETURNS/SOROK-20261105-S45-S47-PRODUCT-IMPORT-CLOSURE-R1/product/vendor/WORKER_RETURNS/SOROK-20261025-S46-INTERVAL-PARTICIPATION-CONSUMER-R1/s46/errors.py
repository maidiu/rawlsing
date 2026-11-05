"""Typed S46 interval source/model refusals."""
from __future__ import annotations


class S46Refusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


__all__ = ["S46Refusal"]
