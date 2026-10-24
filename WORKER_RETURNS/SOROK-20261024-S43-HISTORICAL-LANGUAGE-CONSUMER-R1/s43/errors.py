"""Typed S43 refusals before unsupported historical language use."""
from __future__ import annotations


class S43Refusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


__all__ = ["S43Refusal"]
