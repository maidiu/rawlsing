"""Representation-neutral bounded-court runner/telemetry for PRE553 R5 shadow."""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import resource
import sys
import time
from typing import Any, Callable, Mapping, Sequence

from rawlsing_next.pre553_r5_codec import canonical_json
from rawlsing_next.pre553_r5_model import R5Error


RUNNER_VERSION = "PRE553_R5_MINIMUM_ONE_RUNNER@1.0.0"


@dataclass(frozen=True)
class R5GateResult:
    gate: str
    passed: bool
    detail: Mapping[str, Any]


class R5BoundedCourtRunner:
    """Runs G0-G8 in fixed order; a gate cannot be waived by a later performance win."""

    ORDER = tuple(f"G{i}" for i in range(9))

    def __init__(self) -> None:
        self.results: list[R5GateResult] = []

    def run(self, gates: Mapping[str, Callable[[], Mapping[str, Any]]]) -> tuple[R5GateResult, ...]:
        self.results = []
        for gate in self.ORDER:
            fn = gates.get(gate)
            if fn is None:
                self.results.append(R5GateResult(gate, False, {"error": "gate callable missing"}))
                break
            try:
                detail = dict(fn())
                passed = bool(detail.pop("passed", True))
            except Exception as exc:
                detail = {"error": f"{type(exc).__name__}: {exc}"}; passed = False
            self.results.append(R5GateResult(gate, passed, detail))
            if not passed:
                break
        return tuple(self.results)

    @property
    def all_passed(self) -> bool:
        return len(self.results) == len(self.ORDER) and all(item.passed for item in self.results)


def current_peak_rss_bytes() -> int:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # Linux reports KiB, macOS reports bytes.
    return int(value if sys.platform == "darwin" else value * 1024)


def deterministic_resource_receipt(*, canonical_bytes: int, scratch_peak_bytes: int,
                                   cache_bytes: int, post_success_retained_bytes: int,
                                   peak_rss_bytes: int, logical_rows: int) -> Mapping[str, int]:
    return {
        "canonical_steady_state_bytes": int(canonical_bytes),
        "scratch_execution_peak_bytes": int(scratch_peak_bytes),
        "nonauthoritative_cache_bytes": int(cache_bytes),
        "post_success_retained_bytes": int(post_success_retained_bytes),
        "peak_rss_bytes": int(peak_rss_bytes),
        "logical_rows": int(logical_rows),
    }


def write_receipt(path: str | Path, payload: Mapping[str, Any]) -> None:
    Path(path).write_text(canonical_json(payload) + "\n", encoding="ascii")


__all__ = [
    "RUNNER_VERSION", "R5GateResult", "R5BoundedCourtRunner", "current_peak_rss_bytes",
    "deterministic_resource_receipt", "write_receipt",
]
