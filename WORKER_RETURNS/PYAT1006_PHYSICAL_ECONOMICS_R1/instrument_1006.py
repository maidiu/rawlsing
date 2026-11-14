"""Independent runtime instrumentation for accepted S2-C/S2-D code.

Nothing in this module changes production semantics.  Wrappers count calls and
elapsed time at already-existing boundaries and always invoke the accepted
implementation.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
import time
from types import MappingProxyType
from typing import Any, Callable, Iterator, Mapping


@dataclass
class TimerBank:
    totals: dict[str, float] = field(default_factory=dict)
    counts: dict[str, int] = field(default_factory=dict)

    @contextmanager
    def measure(self, name: str) -> Iterator[None]:
        start = time.monotonic()
        try:
            yield
        finally:
            self.totals[name] = self.totals.get(name, 0.0) + (
                time.monotonic() - start
            )
            self.counts[name] = self.counts.get(name, 0) + 1

    def add(self, name: str, seconds: float, count: int = 1) -> None:
        self.totals[name] = self.totals.get(name, 0.0) + seconds
        self.counts[name] = self.counts.get(name, 0) + count

    def material(self) -> dict[str, Any]:
        return {
            "seconds": dict(sorted(self.totals.items())),
            "calls": dict(sorted(self.counts.items())),
        }


class TimedSections:
    def __init__(self, sections: Mapping[str, Any], timers: TimerBank):
        self._sections = sections
        self._timers = timers
        self._wrapped = MappingProxyType({
            family: self._wrap(family, stream)
            for family, stream in sections.items()
        })

    def _wrap(self, family: str, stream: Iterator[Any]) -> Iterator[Any]:
        def iterate() -> Iterator[Any]:
            while True:
                start = time.monotonic()
                try:
                    value = next(stream)
                except StopIteration:
                    self._timers.add(f"fixture_yield:{family}", time.monotonic() - start)
                    return
                self._timers.add(f"fixture_yield:{family}", time.monotonic() - start)
                yield value
        return iterate()

    @property
    def sections(self) -> Mapping[str, Iterator[Any]]:
        return self._wrapped


def replace_sections(source: Any, timers: TimerBank) -> Any:
    from dataclasses import replace

    timed = TimedSections(source.sections, timers)
    return replace(source, sections=timed.sections)


def install_estate_instrumentation(
    estate_module: Any, timers: TimerBank,
) -> dict[str, Any]:
    state: dict[str, Any] = {
        "row_calls": {},
        "row_body_bytes": {},
        "row_seconds": 0.0,
        "sink_add_calls": {},
        "sink_flush_calls": {},
        "hash_calls": 0,
        "hash_bytes": 0,
        "verify_row_calls": 0,
        "original": {},
    }
    original_row = estate_module._row
    original_add = estate_module._Sink.add
    original_flush = estate_module._Sink.flush
    original_hash = estate_module._hash
    original_build = estate_module.build_sourcefree_direct_i02
    original_verify = estate_module._verify_emitted_physical_payloads
    original_cert = estate_module._reconstructed_v1_release_from_certificate
    state["original"] = {
        "row": original_row,
        "add": original_add,
        "flush": original_flush,
        "hash": original_hash,
        "build": original_build,
        "verify": original_verify,
        "cert": original_cert,
    }

    def row(family: str, obj: object) -> dict[str, Any]:
        start = time.monotonic()
        result = original_row(family, obj)
        elapsed = time.monotonic() - start
        state["row_seconds"] += elapsed
        state["row_calls"][family] = state["row_calls"].get(family, 0) + 1
        state["row_body_bytes"][family] = state["row_body_bytes"].get(
            family, 0
        ) + len(result["body_json"].encode("utf-8"))
        return result

    def add(self, obj: object) -> tuple[int, int]:
        state["sink_add_calls"][self.family] = state["sink_add_calls"].get(
            self.family, 0
        ) + 1
        return original_add(self, obj)

    def flush(self) -> None:
        state["sink_flush_calls"][self.family] = state["sink_flush_calls"].get(
            self.family, 0
        ) + 1
        with timers.measure(f"sink_flush:{self.family}"):
            return original_flush(self)

    def hash_path(path: Path) -> str:
        state["hash_calls"] += 1
        if path.is_file():
            state["hash_bytes"] += path.stat().st_size
        with timers.measure("root_hash"):
            return original_hash(path)

    def build(*args: Any, **kwargs: Any) -> Any:
        with timers.measure("direct_i02_proof"):
            return original_build(*args, **kwargs)

    def verify(*args: Any, **kwargs: Any) -> Any:
        with timers.measure("physical_reread_reencode_proof"):
            return original_verify(*args, **kwargs)

    def cert(*args: Any, **kwargs: Any) -> Any:
        with timers.measure("reconstructed_v1_header"):
            return original_cert(*args, **kwargs)

    estate_module._row = row
    estate_module._Sink.add = add
    estate_module._Sink.flush = flush
    estate_module._hash = hash_path
    estate_module.build_sourcefree_direct_i02 = build
    estate_module._verify_emitted_physical_payloads = verify
    estate_module._reconstructed_v1_release_from_certificate = cert
    return state


def restore_estate_instrumentation(
    estate_module: Any, state: Mapping[str, Any],
) -> None:
    original = state["original"]
    estate_module._row = original["row"]
    estate_module._Sink.add = original["add"]
    estate_module._Sink.flush = original["flush"]
    estate_module._hash = original["hash"]
    estate_module.build_sourcefree_direct_i02 = original["build"]
    estate_module._verify_emitted_physical_payloads = original["verify"]
    estate_module._reconstructed_v1_release_from_certificate = original["cert"]


def install_session_instrumentation(
    direct_module: Any, timers: TimerBank,
) -> dict[str, Any]:
    state = {
        "enter_calls": 0,
        "build_calls": 0,
        "event_rows": 0,
        "family_rows": {},
        "original_enter": direct_module.DirectEstateI03Session.__enter__,
        "original_build": direct_module.DirectEstateI03Session._build,
        "original_rows": direct_module.DirectEstateI03Session._respondent_family,
    }

    def enter(self: Any) -> Any:
        state["enter_calls"] += 1
        with timers.measure("cold_session_open"):
            return state["original_enter"](self)

    def build(self: Any) -> None:
        state["build_calls"] += 1
        with timers.measure("cold_session_posting_index_build"):
            return state["original_build"](self)

    def family_rows(self: Any, family: str, respondent_key: str) -> Iterator[Any]:
        yield from state["original_rows"](self, family, respondent_key)

    direct_module.DirectEstateI03Session.__enter__ = enter
    direct_module.DirectEstateI03Session._build = build
    direct_module.DirectEstateI03Session._respondent_family = family_rows
    return state


def restore_session_instrumentation(
    direct_module: Any, state: Mapping[str, Any],
) -> None:
    direct_module.DirectEstateI03Session.__enter__ = state["original_enter"]
    direct_module.DirectEstateI03Session._build = state["original_build"]
    direct_module.DirectEstateI03Session._respondent_family = state["original_rows"]


def install_object_materialization_counter(
    direct_module: Any,
) -> dict[str, int]:
    state = {"count": 0}
    original = direct_module._object_from_row

    def count(value: Any) -> Any:
        state["count"] += 1
        return original(value)

    direct_module._object_from_row = count
    state["original"] = original
    return state


def restore_object_materialization_counter(
    direct_module: Any, state: Mapping[str, Any],
) -> None:
    direct_module._object_from_row = state["original"]


def parquet_audit(directory: Path) -> dict[str, Any]:
    import pyarrow.parquet as pq

    families: dict[str, Any] = {}
    total_rows = 0
    total_row_groups = 0
    for path in sorted(directory.glob("*.parquet")):
        pf = pq.ParquetFile(path)
        try:
            metadata = pf.metadata
            groups = [
                {
                    "row_group": gid,
                    "rows": metadata.row_group(gid).num_rows,
                    "bytes": metadata.row_group(gid).total_byte_size,
                }
                for gid in range(pf.num_row_groups)
            ]
            rows = metadata.num_rows
            families[path.name] = {
                "bytes": path.stat().st_size,
                "rows": rows,
                "row_groups": pf.num_row_groups,
                "row_group_detail": groups,
            }
            total_rows += rows
            total_row_groups += pf.num_row_groups
        finally:
            pf.close()
    return {
        "members": families,
        "total_rows": total_rows,
        "total_row_groups": total_row_groups,
        "total_bytes": sum(item["bytes"] for item in families.values()),
    }


def directory_bytes(path: Path) -> int:
    try:
        return sum(
            item.stat().st_size for item in path.rglob("*") if item.is_file()
        )
    except FileNotFoundError:
        return 0


def stats(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"n": 0}
    ordered = sorted(values)
    def pct(percent: float) -> float:
        if len(ordered) == 1:
            return ordered[0]
        position = (len(ordered) - 1) * percent
        low = int(position)
        high = min(low + 1, len(ordered) - 1)
        fraction = position - low
        return ordered[low] * (1 - fraction) + ordered[high] * fraction
    return {
        "n": len(ordered),
        "min": ordered[0],
        "p50": pct(0.50),
        "p95": pct(0.95),
        "max": ordered[-1],
        "mean": sum(ordered) / len(ordered),
    }


__all__ = [
    "TimerBank",
    "TimedSections",
    "directory_bytes",
    "install_estate_instrumentation",
    "install_object_materialization_counter",
    "install_session_instrumentation",
    "parquet_audit",
    "replace_sections",
    "restore_estate_instrumentation",
    "restore_object_materialization_counter",
    "restore_session_instrumentation",
    "stats",
]
