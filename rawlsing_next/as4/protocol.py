"""Candidate-neutral HB04 A/B/C session protocol.

The protocol owns transport/session lifecycle only.  Shared I03/I05 remain the
semantic oracle.  Descriptive resource observations never enter semantic refs.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import os
from pathlib import Path
import resource
import shutil
import time
from typing import Any, Iterable, Mapping

from rawlsing_next.as4.loader import (
    HB04FreezeError,
    LITS1_SOURCE_SHA256,
    LoadedHB04Manifest,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
from rawlsing_next.pre553_r5_source_backed_adapter import build_r5_source_backed_c11_repository
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
from rawlsing_next.pre553_route_c_accelerators import (
    Cacc1Paths,
    build_cacc1,
    read_cacc1,
    build_cacc2,
    read_cacc2,
    delete_cacc1,
    delete_cacc2,
    execute_route_c_empirical_query,
    execute_route_c_exact_bounded_discovery,
)


@dataclass(frozen=True)
class HB04Workload:
    authority_registry: Any
    i03_query: Any
    i03_predicate: Any
    discovery_authority: Any
    predicate_catalog: tuple[Any, ...]
    query_template_catalog: tuple[Any, ...]
    required_cacc2_roles_for_i03: tuple[str, ...] = ("A000",)


@dataclass
class HB04PreparedSource:
    source_sha256: str
    projection: Any
    transport: Any
    workload: HB04Workload
    mode: str
    r5_reader: Any | None = None
    route_c_determinants: Any | None = None
    route_c_cacc2_determinants: Any | None = None
    route_c_atom_bindings: tuple[Any, ...] = ()
    cleanup_paths: tuple[Path, ...] = ()
    source_identity_receipt: Mapping[str, Any] = field(default_factory=dict)

    def validate(self, manifest: LoadedHB04Manifest, *, allow_bounded_fixture: bool) -> None:
        if self.mode == "PRODUCTION_LITS1":
            if self.source_sha256 != LITS1_SOURCE_SHA256:
                raise HB04FreezeError("production HB04 source SHA does not match frozen LiTS-I")
        elif self.mode == "BOUNDED_GOVERNED_FIXTURE":
            if not allow_bounded_fixture:
                raise HB04FreezeError("bounded fixture requires explicit implementation-court authorization")
        else:
            raise HB04FreezeError(f"unknown HB04 source mode {self.mode!r}")
        if not self.source_sha256 or len(self.source_sha256) != 64:
            raise HB04FreezeError("source bundle lacks exact source SHA-256")
        if self.workload is None:
            raise HB04FreezeError("source bundle lacks exact semantic workload")
        if self.projection is None or self.transport is None:
            raise HB04FreezeError("source bundle lacks projection/transport")


def _rss_bytes() -> int | None:
    try:
        value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except Exception:
        return None
    # Linux reports KiB; macOS reports bytes. B21 authoritative court is Linux.
    return int(value) * 1024 if os.uname().sysname == "Linux" else int(value)


def _tree_stats(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    count = 0
    size = 0
    for item in path.rglob("*"):
        try:
            if item.is_file():
                count += 1
                size += item.stat().st_size
        except OSError:
            continue
    return count, size


class HB04CandidateSession:
    """One candidate, one source bundle, one exact semantic workload."""

    def __init__(
        self,
        *,
        candidate: str,
        source: HB04PreparedSource,
        manifest: LoadedHB04Manifest,
        workdir: Path,
        allow_bounded_fixture: bool = False,
    ) -> None:
        if candidate not in {"A", "B", "C"}:
            raise HB04FreezeError("candidate must be exactly A, B, or C")
        source.validate(manifest, allow_bounded_fixture=allow_bounded_fixture)
        self.candidate = candidate
        self.source = source
        self.manifest = manifest
        self.workdir = Path(workdir)
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.scratch = self.workdir / "scratch"
        self.scratch.mkdir(parents=True, exist_ok=False)
        self.repository = None
        self.release = None
        self._closed = False
        self._cacc1 = None
        self._cacc1_paths = None
        self._cacc2_manifest = None
        self._cacc2_dir = None
        self._measurements: dict[str, Any] = {
            "schema": "HB04_RESOURCE_OBSERVATION@1.0.0",
            "candidate": candidate,
            "semantic_identity_effect": "NONE_DESCRIPTIVE_ONLY",
            "rss_start_bytes": _rss_bytes(),
            "prepare_elapsed_ns": None,
            "i03_elapsed_ns": None,
            "i05_elapsed_ns": None,
            "rss_end_bytes": None,
            "scratch_peak_bytes": 0,
            "scratch_peak_file_count": 0,
            "persistent_transformed_payload_bytes": 0,
            "persistent_transformed_payload_file_count": 0,
        }
        started = time.perf_counter_ns()
        try:
            self._prepare()
        except Exception:
            self.close()
            raise
        self._measurements["prepare_elapsed_ns"] = time.perf_counter_ns() - started
        self._observe_scratch()

    def _observe_scratch(self) -> None:
        count, size = _tree_stats(self.scratch)
        self._measurements["scratch_peak_bytes"] = max(
            int(self._measurements["scratch_peak_bytes"]), size
        )
        self._measurements["scratch_peak_file_count"] = max(
            int(self._measurements["scratch_peak_file_count"]), count
        )

    def _prepare(self) -> None:
        if self.candidate == "A":
            if self.source.r5_reader is None:
                raise HB04FreezeError("Route A requires an exact frozen R5 reader")
            repo, release, descriptor = build_r5_source_backed_c11_repository(
                self.source.r5_reader, self.source.projection
            )
            if descriptor.source_sha256 != self.source.source_sha256:
                raise HB04FreezeError("Route A descriptor lost source SHA binding")
            self.repository, self.release = repo, release
            return

        if self.candidate == "B":
            repo, release = build_source_backed_c11_repository(
                self.source.transport, self.source.projection, cache=None
            )
            if release.source_artifact_ref.content_hash != self.source.source_sha256:
                raise HB04FreezeError("Route B release lost source SHA binding")
            self.repository, self.release = repo, release
            return

        if self.source.route_c_determinants is None or self.source.route_c_cacc2_determinants is None:
            raise HB04FreezeError("Route C requires exact CACC1/CACC2 determinants")
        if len(self.source.route_c_atom_bindings) != 19:
            raise HB04FreezeError("Route C requires exactly 19 frozen role-mask bindings")
        paths = Cacc1Paths(self.scratch / "cacc1.arrow", self.scratch / "cacc1.manifest.json")
        cacc1 = build_cacc1(
            stream=self.source.transport,
            projection=self.source.projection,
            determinants=self.source.route_c_determinants,
            paths=paths,
        )
        cacc1 = read_cacc1(paths=paths, expected_determinants=self.source.route_c_determinants)
        c2dir = self.scratch / "cacc2"
        build_cacc2(
            directory=c2dir,
            cacc1=cacc1,
            determinants=self.source.route_c_cacc2_determinants,
            atom_bindings=self.source.route_c_atom_bindings,
        )
        c2 = read_cacc2(
            directory=c2dir,
            expected_determinants=self.source.route_c_cacc2_determinants,
        )
        self._cacc1, self._cacc1_paths = cacc1, paths
        self._cacc2_dir, self._cacc2_manifest = c2dir, c2
        repo, release = build_source_backed_c11_repository(
            self.source.transport, self.source.projection, cache=None
        )
        self.repository, self.release = repo, release

    def run_i03(self):
        if self._closed:
            raise HB04FreezeError("candidate session is closed")
        w = self.source.workload
        started = time.perf_counter_ns()
        if self.candidate == "C":
            result = execute_route_c_empirical_query(
                cacc1=self._cacc1,
                projection=self.source.projection,
                query=w.i03_query,
                predicate=w.i03_predicate,
                authority_registry=w.authority_registry,
                cacc2_directory=self._cacc2_dir,
                cacc2_manifest=self._cacc2_manifest,
                required_atom_roles=w.required_cacc2_roles_for_i03,
            )
        else:
            result = execute_empirical_query(
                repository=self.repository,
                query=w.i03_query,
                predicate=w.i03_predicate,
                authority_registry=w.authority_registry,
                release_refs=(self.release.release_ref,),
            )
        self._measurements["i03_elapsed_ns"] = time.perf_counter_ns() - started
        self._observe_scratch()
        return result

    def run_i05(self):
        if self._closed:
            raise HB04FreezeError("candidate session is closed")
        w = self.source.workload
        started = time.perf_counter_ns()
        if self.candidate == "C":
            result = execute_route_c_exact_bounded_discovery(
                cacc1=self._cacc1,
                projection=self.source.projection,
                discovery_authority=w.discovery_authority,
                authority_registry=w.authority_registry,
                predicate_catalog=w.predicate_catalog,
                query_template_catalog=w.query_template_catalog,
                cacc2_directory=self._cacc2_dir,
                cacc2_manifest=self._cacc2_manifest,
            )
        else:
            result = execute_exact_bounded_discovery(
                repository=self.repository,
                discovery_authority=w.discovery_authority,
                authority_registry=w.authority_registry,
                release_refs=(self.release.release_ref,),
                predicate_catalog=w.predicate_catalog,
                query_template_catalog=w.query_template_catalog,
            )
        self._measurements["i05_elapsed_ns"] = time.perf_counter_ns() - started
        self._observe_scratch()
        return result

    @property
    def measurements(self) -> Mapping[str, Any]:
        return dict(self._measurements)

    @property
    def closed(self) -> bool:
        return self._closed

    def close(self) -> Mapping[str, Any]:
        if self._closed:
            return {
                "schema": "HB04_CLEANUP_RECEIPT@1.0.0",
                "candidate": self.candidate,
                "status": "ALREADY_CLOSED",
                "scratch_exists": self.scratch.exists(),
                "persistent_transformed_payload_file_count": 0,
            }
        self._observe_scratch()
        try:
            if self._cacc1_paths is not None:
                delete_cacc1(self._cacc1_paths)
            if self._cacc2_dir is not None and self._cacc2_dir.exists():
                delete_cacc2(self._cacc2_dir)
            close_reader = getattr(self.source.r5_reader, "close", None)
            if callable(close_reader):
                close_reader()
        finally:
            self.repository = None
            self.release = None
            for path in self.source.cleanup_paths:
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                    elif path.exists():
                        path.unlink()
                except OSError:
                    pass
            if self.scratch.exists():
                shutil.rmtree(self.scratch)
            self._closed = True
            self._measurements["rss_end_bytes"] = _rss_bytes()
        count, size = _tree_stats(self.scratch)
        return {
            "schema": "HB04_CLEANUP_RECEIPT@1.0.0",
            "candidate": self.candidate,
            "status": "PASS_CLOSED_AND_SCRATCH_REMOVED" if not self.scratch.exists() else "FAIL",
            "scratch_exists": self.scratch.exists(),
            "scratch_residual_file_count": count,
            "scratch_residual_bytes": size,
            "persistent_transformed_payload_file_count": 0,
            "persistent_transformed_payload_bytes": 0,
            "result_cache_present": False,
        }


def prepare(
    candidate: str,
    source: HB04PreparedSource,
    sealed_manifest: LoadedHB04Manifest,
    workdir: Path,
    *,
    allow_bounded_fixture: bool = False,
) -> HB04CandidateSession:
    return HB04CandidateSession(
        candidate=candidate,
        source=source,
        manifest=sealed_manifest,
        workdir=Path(workdir),
        allow_bounded_fixture=allow_bounded_fixture,
    )


def result_identity_receipt(candidate: str, i03_result: Any, i05_result: Any) -> Mapping[str, Any]:
    return {
        "schema": "HB04_CANDIDATE_SEMANTIC_IDENTITY_RECEIPT@1.0.0",
        "candidate": candidate,
        "i03_fact_refs": [fact.ref.as_dict() for fact in i03_result.facts],
        "i05_evaluated_frontier_ref": i05_result.evaluated_frontier_ref.as_dict(),
        "i05_receipt_refs": [receipt.ref.as_dict() for receipt in i05_result.receipts],
        "candidate_count": i05_result.candidate_count,
        "covered_candidate_count": i05_result.covered_candidate_count,
        "ranking_fields_present": False,
        "selection_fields_present": False,
    }


__all__ = [
    "HB04Workload",
    "HB04PreparedSource",
    "HB04CandidateSession",
    "prepare",
    "result_identity_receipt",
]
