#!/usr/bin/env python3
"""Alternate source-local FIABC measured-court orchestrator.

This file is deliberately OUTSIDE the protected execution branch.  It imports
all governed candidate, backend, accounting, and semantic machinery from an
exact protected execution checkout and changes only court orchestration:

    one invocation = one source block = A -> B -> C

It never runs the six-cell S17 verifier and never claims six-cell/P2
completeness.  A separate merge/adjudication step is required.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Mapping

EXPECTED_EXECUTION_BRANCH = "agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"
EXPECTED_EXECUTION_HEAD = "3d8f2ad62600b6777dcb23a28404a067502e77a0"
EXPECTED_SOURCES = ("LITS_I", "WVS7")
EXPECTED_CANDIDATES = ("A", "B", "C")
SOURCE_TERMINAL_SCHEMA = "RAWLSING_FIABC_SOURCE_LOCAL_TERMINAL@1.0.0"
SOURCE_PREFLIGHT_SCHEMA = "RAWLSING_FIABC_SOURCE_LOCAL_PREFLIGHT@1.0.0"


class SourceLocalRunnerError(RuntimeError):
    pass


def _canon(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
    ).encode("utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _require_exact_execution_checkout(repo_root: Path) -> tuple[str, str]:
    branch = _git(repo_root, "branch", "--show-current").stdout.strip()
    head = _git(repo_root, "rev-parse", "--verify", "HEAD^{commit}").stdout.strip()
    if branch != EXPECTED_EXECUTION_BRANCH:
        raise SourceLocalRunnerError(
            f"execution checkout branch drift: expected {EXPECTED_EXECUTION_BRANCH}, got {branch}"
        )
    if head != EXPECTED_EXECUTION_HEAD:
        raise SourceLocalRunnerError(
            f"execution checkout head drift: expected {EXPECTED_EXECUTION_HEAD}, got {head}"
        )
    dirty = _git(
        repo_root, "status", "--porcelain", "--untracked-files=all"
    ).stdout.strip()
    if dirty:
        raise SourceLocalRunnerError("protected execution checkout is dirty")
    return branch, head


def _load_base(repo_root: Path):
    repo_root = repo_root.resolve()
    root_text = str(repo_root)
    if root_text in sys.path:
        sys.path.remove(root_text)
    sys.path.insert(0, root_text)

    from rawlsing_next import ee_p2x_darwin_court_driver as base  # type: ignore

    driver_path = Path(base.__file__).resolve()
    if repo_root != driver_path and repo_root not in driver_path.parents:
        raise SourceLocalRunnerError(
            f"governed driver imported outside protected checkout: {driver_path}"
        )
    return base


def _sysctl(name: str) -> str | None:
    proc = subprocess.run(
        ["sysctl", "-n", name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    value = proc.stdout.strip()
    return value or None


def _hardware_fingerprint(base_host: Any) -> Mapping[str, Any]:
    memory = _sysctl("hw.memsize")
    governed_runtime = dataclasses.asdict(base_host)
    dependency_versions = dict(governed_runtime.get("dependency_versions", {}))
    dependency_versions.update({
        "pandas": importlib.metadata.version("pandas"),
        "numpy": importlib.metadata.version("numpy"),
    })
    governed_runtime["dependency_versions"] = dependency_versions
    return {
        "governed_runtime": governed_runtime,
        "macos_version": platform.mac_ver()[0] or None,
        "hardware_model": _sysctl("hw.model"),
        "cpu_brand": _sysctl("machdep.cpu.brand_string"),
        "memory_bytes": int(memory) if memory and memory.isdigit() else None,
    }


def _cells_for_source(machine: Any, source: str) -> list[Mapping[str, Any]]:
    cells = [
        cell
        for cell in machine.document.get("cells", ())
        if isinstance(cell, Mapping) and cell.get("source") == source
    ]
    observed = tuple(cell.get("candidate") for cell in cells)
    if observed != EXPECTED_CANDIDATES:
        raise SourceLocalRunnerError(
            f"source-local candidate order drift for {source}: {observed!r}"
        )
    return cells


def _stage_addresses(base: Any, machine: Any, source: str) -> list[str]:
    out: list[str] = []
    for cell in _cells_for_source(machine, source):
        for stage_id in base._manifest_ordered_stage_ids(machine.document, cell):
            out.append(f"{source}/{cell['candidate']}/{stage_id}")
    if not out:
        raise SourceLocalRunnerError(f"source-local stage set is empty: {source}")
    return out



class SourceLocalManifestProgressPlan:
    """Selected-source progress ordinals over the exact protected manifest.

    The protected ProgressReporter remains the emitter.  Only its administrative
    address universe is replaced so a split source block can represent all 51
    governed rows for that source without admitting the other source or S17.
    """

    def __init__(self, base: Any, machine: Any, source: str):
        self.base = base
        self.machine = machine
        self.source = source
        self.cells = tuple(_cells_for_source(machine, source))
        self.cell_addresses: dict[tuple[str, str], tuple[str, ...]] = {}
        self.cell_meta: dict[tuple[str, str], Mapping[str, Any]] = {}
        flattened: list[str] = []
        sources = (
            machine.document.get("sources", {})
            if isinstance(machine.document.get("sources", {}), Mapping)
            else {}
        )

        for cell_index, cell in enumerate(self.cells, 1):
            candidate = str(cell["candidate"])
            key = (source, candidate)
            stage_ids = base._manifest_ordered_stage_ids(machine.document, cell)
            addresses = tuple(f"{source}/{candidate}/{sid}" for sid in stage_ids)
            for address in addresses:
                stage = machine.get(address)
                if stage.source != source or stage.candidate != candidate:
                    raise SourceLocalRunnerError(
                        f"source-local progress address escaped selected cell: {address}"
                    )
            self.cell_addresses[key] = addresses
            src_doc = (
                sources.get(source, {})
                if isinstance(sources.get(source, {}), Mapping)
                else {}
            )
            self.cell_meta[key] = {
                "cell_index": cell_index,
                "source_name": str(
                    cell.get("source_name")
                    or src_doc.get("display_name")
                    or src_doc.get("name")
                    or src_doc.get("label")
                    or source
                ),
                "candidate_name": str(cell.get("candidate_name") or candidate),
                "stage_ids": stage_ids,
            }
            flattened.extend(addresses)

        if len(flattened) != 51:
            raise SourceLocalRunnerError(
                f"source-local progress universe must contain 51 current rows, got {len(flattened)}"
            )
        if any(not address.startswith(f"{source}/") for address in flattened):
            raise SourceLocalRunnerError("source-local progress universe contains another source")
        if any(address.startswith("COURT/") or "/S17_" in address for address in flattened):
            raise SourceLocalRunnerError("source-local progress universe contains COURT/S17")

        self.governed_addresses = tuple(flattened)
        self.executable_addresses = tuple(
            address
            for address in self.governed_addresses
            if machine.get(address).disposition == "READY__RUN_LOCALLY"
        )
        self._overall = {
            address: index
            for index, address in enumerate(self.governed_addresses, 1)
        }
        self._executable = {
            address: index
            for index, address in enumerate(self.executable_addresses, 1)
        }

    @property
    def overall_total(self) -> int:
        return len(self.governed_addresses)

    @property
    def executable_total(self) -> int:
        return len(self.executable_addresses)

    @property
    def cell_total(self) -> int:
        return len(self.cells)

    def position(self, address: str):
        if address not in self._overall:
            raise SourceLocalRunnerError(
                f"progress address is outside selected source {self.source}: {address}"
            )
        stage = self.machine.get(address)
        key = (stage.source, stage.candidate)
        meta = self.cell_meta[key]
        stage_ids = meta["stage_ids"]
        return self.base.ProgressPosition(
            address=address,
            overall_index=self._overall[address],
            overall_total=self.overall_total,
            executable_index=self._executable.get(address),
            executable_total=self.executable_total,
            cell_index=int(meta["cell_index"]),
            cell_total=self.cell_total,
            source=stage.source,
            candidate=stage.candidate,
            source_name=str(meta["source_name"]),
            candidate_name=str(meta["candidate_name"]),
            stage_id=stage.stage_id,
            stage_index=stage_ids.index(stage.stage_id) + 1,
            stage_total=len(stage_ids),
            is_court_final=False,
        )


def _install_source_local_progress(
    *, base: Any, driver: Any, machine: Any, source: str
) -> SourceLocalManifestProgressPlan:
    """Retain the protected reporter, replacing only its full-court address plan."""
    plan = SourceLocalManifestProgressPlan(base, machine, source)
    driver.progress.plan = plan
    return plan


def _ordered_manifest_addresses(base: Any, machine: Any) -> list[str]:
    ordered: list[str] = []
    for cell in machine.document.get("cells", ()):
        if not isinstance(cell, Mapping):
            continue
        source = cell.get("source")
        candidate = cell.get("candidate")
        if not isinstance(source, str) or not isinstance(candidate, str):
            raise SourceLocalRunnerError("manifest cell source/candidate malformed")
        for stage_id in base._manifest_ordered_stage_ids(machine.document, cell):
            ordered.append(f"{source}/{candidate}/{stage_id}")
    return ordered


def _joined_preflight_prefix(base: Any, machine: Any) -> tuple[str, ...]:
    first = getattr(machine, "first_unfinished", None)
    if not isinstance(first, str):
        return ()
    ordered = _ordered_manifest_addresses(base, machine)
    try:
        index = ordered.index(first)
    except ValueError as exc:
        raise SourceLocalRunnerError(
            "joined first_unfinished is absent from manifest order"
        ) from exc
    return tuple(ordered[:index])


def _joined_all_pass_trace(machine: Any) -> tuple[str, ...]:
    first = getattr(machine, "first_unfinished", None)
    final = getattr(machine, "final_stage_id", None)
    if not isinstance(first, str) or not isinstance(final, str):
        return ()
    address = first
    seen: set[str] = set()
    trace: list[str] = []
    while address != "__COURT_COMPLETE__":
        if address in seen:
            raise SourceLocalRunnerError(f"joined pass graph cycles at {address}")
        seen.add(address)
        trace.append(address)
        if address == final:
            break
        address = machine.get(address).next_stage_on_pass
    return tuple(trace)


def _transition_differential(base: Any, machine: Any, source: str) -> Mapping[str, Any]:
    """Exact protected joined-source segment versus split materialization model."""
    selected = tuple(_stage_addresses(base, machine, source))
    preflight = tuple(
        address
        for address in _joined_preflight_prefix(base, machine)
        if address.startswith(f"{source}/")
    )
    joined_run = tuple(
        address
        for address in _joined_all_pass_trace(machine)
        if address.startswith(f"{source}/")
    )
    split_run = tuple(address for address in selected if address not in preflight)

    joined_backend = tuple(
        address
        for address in joined_run
        if machine.get(address).disposition == "READY__RUN_LOCALLY"
    )
    split_backend = tuple(
        address
        for address in split_run
        if machine.get(address).disposition == "READY__RUN_LOCALLY"
    )
    extras = tuple(address for address in split_run if address not in joined_run)
    missing = tuple(address for address in joined_run if address not in split_run)
    approved_extras: list[str] = []
    for address in extras:
        stage = machine.get(address)
        if (
            source == "WVS7"
            and address == "WVS7/C/S00_SOURCE_PREFLIGHT_IDENTITY"
            and stage.disposition == "DONE__PRESERVE"
            and stage.empirical_source_access_required is False
            and stage.physical_host_measurement_required is False
        ):
            approved_extras.append(address)

    return {
        "source": source,
        "selected_stage_count": len(selected),
        "joined_preflight": list(preflight),
        "joined_run": list(joined_run),
        "split_preflight": list(preflight),
        "split_run": list(split_run),
        "joined_candidate_backend_addresses": list(joined_backend),
        "split_candidate_backend_addresses": list(split_backend),
        "candidate_backend_addresses_identical": joined_backend == split_backend,
        "split_extra_addresses": list(extras),
        "approved_mechanical_extra_addresses": approved_extras,
        "split_missing_addresses": list(missing),
        "other_source_or_s17_in_split": [
            address
            for address in selected
            if not address.startswith(f"{source}/")
            or address.startswith("COURT/")
            or "/S17_" in address
        ],
    }


def _assert_transition_parity(base: Any, machine: Any, source: str) -> Mapping[str, Any]:
    # Synthetic unit fixtures from the first split court predate actual-manifest
    # differential qualification.  Exact runtime machines always expose these.
    if not isinstance(getattr(machine, "first_unfinished", None), str):
        return {"source": source, "synthetic_fixture": True}
    diff = _transition_differential(base, machine, source)
    if diff["selected_stage_count"] != 51:
        raise SourceLocalRunnerError("selected source no longer has exactly 51 governed stages")
    if diff["other_source_or_s17_in_split"]:
        raise SourceLocalRunnerError("source-local traversal escaped selected source or admitted S17")
    if diff["split_missing_addresses"]:
        raise SourceLocalRunnerError(
            f"split traversal drops joined source stages: {diff['split_missing_addresses']}"
        )
    if diff["candidate_backend_addresses_identical"] is not True:
        raise SourceLocalRunnerError("split candidate backend address/order differs from joined source segment")
    extras = tuple(diff["split_extra_addresses"])
    approved = tuple(diff["approved_mechanical_extra_addresses"])
    if extras != approved:
        raise SourceLocalRunnerError(
            f"unapproved split-only stage materialization: {extras}"
        )
    expected_extra = () if source == "LITS_I" else ("WVS7/C/S00_SOURCE_PREFLIGHT_IDENTITY",)
    if approved != expected_extra:
        raise SourceLocalRunnerError(
            f"source-cut mechanical differential drift for {source}: {approved!r}"
        )
    if source == "LITS_I" and tuple(diff["joined_preflight"]) != (
        "LITS_I/A/S00_SOURCE_PREFLIGHT_IDENTITY",
    ):
        raise SourceLocalRunnerError("LiTS/A/S00 joined preflight-prefix law drift")
    if source == "LITS_I" and len(diff["joined_run"]) != 50:
        raise SourceLocalRunnerError("joined LiTS run is no longer exactly 50 stages")
    if source == "WVS7" and len(diff["joined_run"]) != 50:
        raise SourceLocalRunnerError("joined WVS run is no longer exactly 50 stages")
    return diff


def _materialize_source_preflight_prefix(
    *, base: Any, driver: Any, machine: Any, source: str, source_sha: str
) -> tuple[str, ...]:
    """Reproduce joined preflight-prefix mechanics without candidate execution."""
    addresses = tuple(
        address
        for address in _joined_preflight_prefix(base, machine)
        if address.startswith(f"{source}/")
    )
    for address in addresses:
        stage = machine.get(address)
        old = driver.ledger.stage_entry(address)
        if old is not None:
            driver.ledger.revalidate_terminal(address)
            continue
        if stage.disposition == "DONE__PRESERVE":
            base._preserve(
                machine,
                driver.ledger,
                stage,
                driver.repo_root,
                driver.repo.head,
                source_sha,
            )
        elif stage.disposition == "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW":
            base._skip(
                machine,
                driver.ledger,
                stage,
                driver.repo.head,
                source_sha,
            )
        else:
            raise SourceLocalRunnerError(
                f"source preflight prefix contains executable/nonmechanical stage: {address}"
            )
    return addresses


def _source_preflight(
    *,
    base: Any,
    driver: Any,
    machine: Any,
    source: str,
    source_path: Path,
    repo_root: Path,
    court_contract_path: Path,
    succession_manifest: Path,
    succession_lifecycle_context: Path,
    freeze_path: Path,
) -> Mapping[str, Any]:
    driver.verify_static_gates()

    observed_sha = driver.ensure_source_verified(source)
    expected_sha = machine.document["sources"][source]["sha256"]
    if observed_sha != expected_sha:
        raise SourceLocalRunnerError("selected source identity drift")

    transition_diff = _assert_transition_parity(base, machine, source)
    preflight_prefix = _materialize_source_preflight_prefix(
        base=base,
        driver=driver,
        machine=machine,
        source=source,
        source_sha=observed_sha,
    )

    # Bind all three frozen owner blobs exactly, but do not instantiate a
    # candidate process or candidate-owned root.
    owners: dict[str, str] = {}
    for candidate, spec in base.OWNER_SPECS.items():
        data = base._git_show_bytes(repo_root, base.OWNER_COMMIT, spec["path"])
        blob = base._git_blob_sha1(data)
        if blob != spec["blob"]:
            raise SourceLocalRunnerError(f"Candidate-{candidate} owner blob drift")
        owners[candidate] = blob

    from rawlsing_next.fiabc_live_terminal_control import (  # type: ignore
        load_frozen_source_oracle,
        run_live_succession_preflight,
        validate_current_court_contract_file,
    )

    validate_current_court_contract_file(court_contract_path, machine.document)
    base.validate_frozen_upstream_for_machine(machine, freeze_path)
    load_frozen_source_oracle(
        freeze_path=freeze_path, source=source, work_root=driver.work_root
    )

    t5_path = driver.work_root / "court" / "fiabc_t5_succession_preflight.json"
    t5 = run_live_succession_preflight(
        manifest_path=succession_manifest,
        lifecycle_context_path=succession_lifecycle_context,
        repo_root=repo_root,
        repo_head=driver.repo.head,
        court_contract_path=court_contract_path,
        current_manifest=machine.document,
        output_path=t5_path,
    )

    payload = {
        "schema": SOURCE_PREFLIGHT_SCHEMA,
        "status": "PASS",
        "source": source,
        "source_sha256": observed_sha,
        "execution_branch": driver.repo.branch,
        "execution_head": driver.repo.head,
        "current_execution_manifest": dataclasses.asdict(machine.identity),
        "host": _hardware_fingerprint(driver.host),
        "owner_blobs": owners,
        "t5_succession_preflight": t5,
        "t5_succession_preflight_path": str(t5_path),
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "joined_split_transition_differential": transition_diff,
        "mechanical_preflight_prefix": list(preflight_prefix),
        "source_local_only": True,
        "six_cell_s17_authorized": False,
        "p2_synthesis_authorized": False,
    }
    payload["receipt_identity"] = _sha256_bytes(_canon(payload))
    out = driver.work_root / "court" / "source_local_preflight.json"
    base._atomic_write_json(out, payload)
    return payload


def _write_source_terminal(
    *,
    base: Any,
    driver: Any,
    machine: Any,
    source: str,
    status: str,
) -> Mapping[str, Any]:
    cells = _cells_for_source(machine, source)
    candidate_terminals: dict[str, Any] = {}
    candidate_failures: list[str] = []
    common_blockers: list[str] = []
    incomplete_stages: list[str] = []
    allow_incomplete = status == "BLOCKED__COMMON_COURT_AUTHORITY"

    for cell in cells:
        candidate = str(cell["candidate"])
        stage_ids = base._manifest_ordered_stage_ids(machine.document, cell)
        if not stage_ids:
            raise SourceLocalRunnerError(f"cell has no governed stages: {source}/{candidate}")
        for stage_id in stage_ids:
            address = f"{source}/{candidate}/{stage_id}"
            entry = driver.ledger.stage_entry(address)
            if not entry or entry.get("terminal_disposition") not in base.COMPLETE_LEDGER_DISPOSITIONS:
                if allow_incomplete:
                    incomplete_stages.append(address)
                    continue
                raise SourceLocalRunnerError(f"source-local terminal has incomplete stage: {address}")
            entry = driver.ledger.revalidate_terminal(address)
            disposition = entry.get("terminal_disposition")
            if disposition in {
                "BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
                "BLOCKED_BY_COMMON_COURT_AUTHORITY",
            }:
                common_blockers.append(address)
        terminal_address = f"{source}/{candidate}/{stage_ids[-1]}"
        terminal = driver.ledger.stage_entry(terminal_address)
        if terminal and terminal.get("terminal_disposition") in base.COMPLETE_LEDGER_DISPOSITIONS:
            terminal = driver.ledger.revalidate_terminal(terminal_address)
            terminal_disposition = terminal.get("terminal_disposition")
            candidate_terminals[candidate] = {
                "address": terminal_address,
                "terminal_disposition": terminal_disposition,
                "receipt_hash": terminal.get("receipt_hash"),
            }
            if terminal_disposition == "CANDIDATE_LOCAL_FAILURE":
                candidate_failures.append(candidate)
        elif allow_incomplete:
            candidate_terminals[candidate] = {
                "address": terminal_address,
                "terminal_disposition": "INCOMPLETE_DUE_COMMON_COURT_BLOCKER",
                "receipt_hash": None,
            }
        else:
            raise SourceLocalRunnerError(
                f"source-local terminal stage absent: {terminal_address}"
            )

    if common_blockers and not status.startswith("BLOCKED"):
        raise SourceLocalRunnerError(
            "source-local completion cannot ignore common-authority blockers"
        )

    source_identity = driver.ledger.source_identity(source)
    if not isinstance(source_identity, Mapping):
        raise SourceLocalRunnerError("source identity missing from source-local ledger")

    control_head = os.environ.get("RAWLSING_FIABC_SPLIT_CONTROL_HEAD")
    runner_sha = os.environ.get("RAWLSING_FIABC_SPLIT_RUNNER_SHA256")
    driver_sha = _sha256_file(Path(__file__).resolve())

    payload = {
        "schema": SOURCE_TERMINAL_SCHEMA,
        "status": status,
        "source": source,
        "source_sha256": source_identity.get("sha256"),
        "candidate_order": list(EXPECTED_CANDIDATES),
        "candidate_terminals": candidate_terminals,
        "candidate_failure_cells": [f"{source}/{c}" for c in candidate_failures],
        "common_blockers": common_blockers,
        "incomplete_stages": incomplete_stages,
        "stage_ledger_sha256": driver.ledger.hash(),
        "execution_branch": driver.repo.branch,
        "execution_head": driver.repo.head,
        "current_execution_manifest": dataclasses.asdict(machine.identity),
        "host": _hardware_fingerprint(driver.host),
        "control_runner": {
            "control_head": control_head,
            "launcher_sha256": runner_sha,
            "source_local_driver_sha256": driver_sha,
        },
        "source_local_only": True,
        "six_cell_s17_executed": False,
        "six_cell_completion_claimed": False,
        "measured_synthesis_performed": False,
        "p2_synthesis_authorized": False,
        "next_required_action": "MERGE_WITH_OTHER_SOURCE_BLOCK__HQ_ADJUDICATION_REQUIRED",
    }
    payload["receipt_identity"] = _sha256_bytes(_canon(payload))
    out = driver.work_root / "court" / "source_local_terminal.json"
    base._atomic_write_json(out, payload)
    return payload


def _run_source_block(
    *,
    base: Any,
    driver: Any,
    machine: Any,
    source: str,
) -> Mapping[str, Any]:
    driver.verify_static_gates()
    source_sha = driver.ensure_source_verified(source)
    _assert_transition_parity(base, machine, source)

    addresses = _stage_addresses(base, machine, source)
    blocked_status: str | None = None

    for address in addresses:
        stage = machine.get(address)
        old = driver.ledger.stage_entry(address)

        if old and old.get("terminal_disposition") in base.COMPLETE_LEDGER_DISPOSITIONS:
            driver.ledger.revalidate_terminal(address)
            continue
        if old and old.get("state") == "RUNNING":
            raise SourceLocalRunnerError(
                f"partial RUNNING stage exists in a fresh source-local court: {address}"
            )

        start_ns = driver.progress.now_ns()

        if stage.disposition == "DONE__PRESERVE":
            next_stage, _ = base._preserve(
                machine, driver.ledger, stage, driver.repo_root, driver.repo.head, source_sha
            )
            driver.progress.emit_stage(
                stage,
                "PRESERVE",
                next_stage=next_stage,
                elapsed_stage_ns=driver.progress.now_ns() - start_ns,
                terminal_disposition="PRESERVED",
            )
            driver.progress.emit_completed_cells()
            continue

        if stage.disposition == "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW":
            next_stage, _ = base._skip(
                machine, driver.ledger, stage, driver.repo.head, source_sha
            )
            driver.progress.emit_stage(
                stage,
                "SKIP",
                next_stage=next_stage,
                elapsed_stage_ns=driver.progress.now_ns() - start_ns,
                terminal_disposition="SKIPPED_BY_FROZEN_LAW",
            )
            driver.progress.emit_completed_cells()
            continue

        if stage.disposition != "READY__RUN_LOCALLY":
            raise SourceLocalRunnerError(
                f"source-local runner refuses non-current disposition at {address}: "
                f"{stage.disposition}"
            )

        driver.progress.emit_stage(
            stage, "START", next_stage=None, elapsed_stage_ns=None
        )
        roots = base._candidate_roots(
            driver.work_root, stage.source, stage.candidate
        )
        input_identity = base._input_identity(
            machine, stage, source_sha, driver.repo.head
        )
        driver.ledger.begin(stage, input_identity)

        context = base.StageContext(
            base.BACKEND_CONTRACT,
            stage,
            driver.work_root,
            roots,
            driver.source_paths.get(source)
            if stage.empirical_source_access_required
            else None,
            source_sha,
            machine.identity,
            base.P2X_BRANCH,
            driver.repo.head,
            input_identity,
        )

        try:
            result = driver.backend.run_stage(context, driver.services)
        except base.CandidateLocalFailure as exc:
            result = base.BackendResult(
                "CANDIDATE_LOCAL_FAILURE",
                {"error": str(exc), **exc.receipt},
                verifier_complete=True,
            )
        except base.CommonAuthorityBlocker as exc:
            result = base.BackendResult(
                "COMMON_SOURCE_BLOCKER"
                if exc.scope == "SOURCE"
                else "COMMON_COURT_BLOCKER",
                {"error": str(exc), "scope": exc.scope, **exc.receipt},
                verifier_complete=True,
            )
        except Exception as exc:
            raise SourceLocalRunnerError(
                f"untyped backend failure at {address}: {exc}"
            ) from exc

        next_stage, receipt_hash, disposition = base._backend_terminal(
            machine, driver.ledger, stage, driver.repo.head, source_sha, result
        )

        if stage.physical_host_measurement_required:
            print(
                "RAWLSING_LOCAL_SUPERVISOR_ACTION "
                + json.dumps(
                    base._token(
                        stage,
                        receipt_hash,
                        driver.ledger.hash(),
                        driver.repo.head,
                    ),
                    sort_keys=True,
                    separators=(",", ":"),
                ),
                file=sys.stderr,
                flush=True,
            )

        if disposition == "CANDIDATE_LOCAL_FAILURE":
            base._candidate_stop(
                machine,
                driver.ledger,
                source=source,
                candidate=stage.candidate,
                head=driver.repo.head,
                source_sha=source_sha,
                blocker=address,
            )
            progress_state = "CANDIDATE_LOCAL_FAILURE"
        elif disposition == "BLOCKED_BY_COMMON_SOURCE_AUTHORITY":
            inherited_global_next = base._mark_source_blocked(
                machine,
                driver.ledger,
                source=source,
                observed_head=driver.repo.head,
                source_sha256=source_sha,
                blocker_stage=address,
            )
            if isinstance(inherited_global_next, str):
                next_stage = inherited_global_next
            blocked_status = "BLOCKED__COMMON_SOURCE_AUTHORITY"
            progress_state = "BLOCKED"
        elif disposition == "BLOCKED_BY_COMMON_COURT_AUTHORITY":
            blocked_status = "BLOCKED__COMMON_COURT_AUTHORITY"
            progress_state = "BLOCKED"
        else:
            progress_state = "PASS"

        driver.progress.emit_stage(
            stage,
            progress_state,
            next_stage=next_stage,
            elapsed_stage_ns=driver.progress.now_ns() - start_ns,
            terminal_disposition=disposition,
        )
        driver.progress.emit_completed_cells()

        if blocked_status is not None:
            break

    if blocked_status is not None:
        return _write_source_terminal(
            base=base,
            driver=driver,
            machine=machine,
            source=source,
            status=blocked_status,
        )

    return _write_source_terminal(
        base=base,
        driver=driver,
        machine=machine,
        source=source,
        status="SOURCE_BLOCK_SEQUENCE_COMPLETE__ALL_THREE_CELLS_TERMINAL",
    )


def _verify_source_block(*, base: Any, driver: Any, machine: Any, source: str) -> Mapping[str, Any]:
    for address in _stage_addresses(base, machine, source):
        entry = driver.ledger.stage_entry(address)
        if not entry:
            continue
        if entry.get("state") == "RUNNING":
            raise SourceLocalRunnerError(f"partial RUNNING stage remains: {address}")
        if entry.get("terminal_disposition") in base.COMPLETE_LEDGER_DISPOSITIONS:
            driver.ledger.revalidate_terminal(address)
    terminal = driver.work_root / "court" / "source_local_terminal.json"
    return {
        "schema": "RAWLSING_FIABC_SOURCE_LOCAL_VERIFY@1.0.0",
        "status": "PASS",
        "source": source,
        "ledger_sha256": driver.ledger.hash(),
        "source_terminal_present": terminal.is_file(),
        "source_terminal_sha256": _sha256_file(terminal) if terminal.is_file() else None,
        "six_cell_s17_executed": False,
    }


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--run", action="store_true")
    mode.add_argument("--verify-only", action="store_true")

    p.add_argument("--source", choices=EXPECTED_SOURCES, required=True)
    p.add_argument("--continuation-map", type=Path, required=True)
    p.add_argument("--current-court-contract", type=Path, required=True)
    p.add_argument("--work-root", type=Path, required=True)
    p.add_argument("--repo-root", type=Path, required=True)
    p.add_argument("--source-path", type=Path, required=True)
    p.add_argument("--backend-module")
    p.add_argument("--frozen-upstream-receipt", type=Path, required=True)
    p.add_argument("--succession-manifest", type=Path)
    p.add_argument("--succession-lifecycle-context", type=Path)
    p.add_argument("--succession-preflight-receipt", type=Path)
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    repo_root = args.repo_root.resolve()
    work_root = args.work_root.resolve()
    source_path = args.source_path.resolve()

    _require_exact_execution_checkout(repo_root)
    base = _load_base(repo_root)

    machine = base.load_current_execution_manifest(args.continuation_map.resolve())
    if tuple(machine.document.get("source_order", ())) != EXPECTED_SOURCES:
        raise SourceLocalRunnerError("full governed source order drift")
    _cells_for_source(machine, args.source)

    from rawlsing_next.fiabc_live_terminal_control import (  # type: ignore
        load_frozen_source_oracle,
        validate_current_court_contract_file,
        validate_live_succession_preflight_receipt,
    )
    from rawlsing_next.fiabc_live_accounting_binding import (  # type: ignore
        authorized_same_cell_transitions,
    )

    court_contract = args.current_court_contract.resolve()
    freeze_path = args.frozen_upstream_receipt.resolve()
    validate_current_court_contract_file(court_contract, machine.document)
    base.validate_frozen_upstream_for_machine(machine, freeze_path)

    host = base.observe_host()
    repo = base.observe_repo(repo_root)
    base.verify_runtime_gate(host)
    base.verify_repo_gate(repo)

    source_paths = {args.source: source_path}
    backend = base._load_backend(args.backend_module) if args.backend_module else None

    lock_root = repo_root / ".git" if (repo_root / ".git").is_dir() else work_root
    with base.DriverInstanceLock(lock_root):
        driver = base.DarwinCourtDriver(
            machine=machine,
            work_root=work_root,
            repo_root=repo_root,
            source_paths=source_paths,
            host=host,
            repo=repo,
            backend=backend,
        )
        _install_source_local_progress(
            base=base, driver=driver, machine=machine, source=args.source
        )
        _assert_transition_parity(base, machine, args.source)

        if args.preflight:
            if args.succession_manifest is None or args.succession_lifecycle_context is None:
                raise SourceLocalRunnerError(
                    "--preflight requires succession manifest and lifecycle context"
                )
            out = _source_preflight(
                base=base,
                driver=driver,
                machine=machine,
                source=args.source,
                source_path=source_path,
                repo_root=repo_root,
                court_contract_path=court_contract,
                succession_manifest=args.succession_manifest.resolve(),
                succession_lifecycle_context=args.succession_lifecycle_context.resolve(),
                freeze_path=freeze_path,
            )
        elif args.verify_only:
            out = _verify_source_block(
                base=base, driver=driver, machine=machine, source=args.source
            )
        else:
            if backend is None or args.backend_module != base.ISOLATED_BACKEND_MODULE:
                raise SourceLocalRunnerError(
                    "source-local measured execution requires the exact process-isolated backend"
                )
            if args.succession_preflight_receipt is None:
                raise SourceLocalRunnerError(
                    "--run requires the source-local/full-court succession preflight receipt"
                )

            preflight_receipt = args.succession_preflight_receipt.resolve()
            validate_live_succession_preflight_receipt(
                preflight_receipt,
                repo_head=repo.head,
                court_contract_path=court_contract,
                current_manifest=machine.document,
            )
            load_frozen_source_oracle(
                freeze_path=freeze_path, source=args.source, work_root=work_root
            )

            os.environ[base.FROZEN_UPSTREAM_ENV] = str(freeze_path)
            os.environ["RAWLSING_FIABC_T5_CURRENT_COURT_CONTRACT"] = str(court_contract)
            os.environ["RAWLSING_FIABC_T5_CURRENT_EXECUTION_MANIFEST"] = str(
                args.continuation_map.resolve()
            )
            os.environ["RAWLSING_FIABC_T5_SUCCESSION_PREFLIGHT_RECEIPT"] = str(
                preflight_receipt
            )
            os.environ["RAWLSING_EE_P2X_WARM_STATE_TRANSITIONS"] = ",".join(
                authorized_same_cell_transitions(
                    machine.document.get("stage_catalog", ())
                )
            )

            out = _run_source_block(
                base=base, driver=driver, machine=machine, source=args.source
            )

    print(json.dumps(out, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
