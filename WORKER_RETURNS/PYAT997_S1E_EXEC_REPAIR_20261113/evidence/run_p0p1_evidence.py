"""PYAT #997 S1-E: executable P0/P1 runtime evidence on the frozen source tree.

This is a witness producer, not a new authority. It reuses the exact accepted
Q2/S2-C/S2-D owners and the repository's own TEST_ONLY fixtures. Every number
below is measured from an actual run on this host; the five-row fixture is not
production-size evidence.
"""
from __future__ import annotations

import json
import os
import platform
import resource
import subprocess
import sys
import tempfile
import time
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pyarrow
import duckdb
import pyreadstat

from rawlsing_next.pre553_batch_runner import BatchExecutionRunner
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_batch, execute_saved_i05,
)
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
from rawlsing_next.tests.test_pyat997_s1e_saved_native_first_consumer import (
    _issued_manifest, _native_i03, _prepare_fixture, _run,
)
from rawlsing_next.tests.test_pyat997_s1e_saved_source_bridge import (
    _build_saved, _estate as _bridge_estate, _native_i03 as _bridge_native_i03,
)

def _git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], cwd=HERE, check=True, text=True,
            capture_output=True,
        ).stdout.strip()
    except Exception as exc:  # evidence script must not hide a bad checkout
        return f"GIT_ERROR: {exc}"


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_plain(v) for v in value),
                      key=lambda item: json.dumps(item, sort_keys=True))
    if hasattr(value, "as_dict"):
        return _plain(value.as_dict())
    if hasattr(value, "key") and not isinstance(value, (str, bytes)):
        return value.key
    return value


def _peak_rss_bytes() -> int:
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return raw if sys.platform == "darwin" else raw * 1024


def _root_bytes(path: Path) -> int:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def _parquet_files(path: Path) -> list[dict[str, Any]]:
    return [
        {"name": p.name, "bytes": p.stat().st_size}
        for p in sorted(path.glob("*.parquet"))
    ]


def _family_table(handoff, estate_receipt, private: Path) -> dict[str, Any]:
    from rawlsing_next.pre553_source_direct_parquet_estate import (
        VerifiedDirectEstate,
    )
    transport = handoff.body_transport or {}
    yields = dict(transport.get("families", {}))
    cold = VerifiedDirectEstate(
        private, exact_path=estate_receipt.path,
        independently_held_manifest_sha256=estate_receipt.manifest_sha256,
        independently_held_i02=estate_receipt.i02,
        current_authorizer=lambda _roots: True,
    )
    families: dict[str, Any] = {}
    for family in ALL_FAMILIES:
        cold_rows = tuple(cold.iter_family(family, batch_size=2))
        families[family] = {
            "declared": handoff.counts.get(family),
            "sink_yield": yields.get(family),
            "estate_declared": estate_receipt.family_counts.get(family),
            "cold_rows": len(cold_rows),
            "cold_refs": [o.ref.key for o in cold_rows],
        }
    return {
        "families": families,
        "family_total": len(ALL_FAMILIES),
        "body_objects": sum(yields.values()),
        "typed_absences": _plain(transport.get("absences", {})),
        "replay_manifest_declared": handoff.counts.get("ReplayManifest"),
    }


def _run_bundle(tmp_path: Path, label: str, values, fixture=None) -> dict[str, Any]:
    started = time.perf_counter()
    result = _run(tmp_path / label, values, fixture=fixture)
    elapsed = time.perf_counter() - started
    (handoff, estate, admission, compilation, resolver, batch, joined,
     fact_refs, discovery_refs, sink) = result
    workload = compilation.issued.workload
    original_fates = Counter(row["disposition"] for row in handoff.operation_fates)
    issued_fates = Counter(compilation.operation_dispositions.values())
    postconsumer_states = Counter(
        row["postconsumer_state"] for row in joined.rows
    )
    receipted = [row for row in joined.rows if row["postconsumer_receipt_refs"]]
    noneligible = [row for row in joined.rows if row["disposition"] != "ELIGIBLE"]
    return {
        "label": label,
        "values": list(values),
        "wall_seconds": elapsed,
        "source_sha256": handoff.source_sha256,
        "source_rows": handoff.row_count,
        "source_stats": _plain(asdict(handoff.stats)),
        "roots": _plain(asdict(handoff.roots)),
        "manifest_sha256": estate.manifest_sha256,
        "estate_i02": _plain(asdict(estate.i02)),
        "estate_path": str(estate.path),
        "retained_bytes": estate.retained_bytes,
        "family_counts": _plain(estate.family_counts),
        "census_audit": _plain(handoff.census_audit),
        "body_transport": _plain(handoff.body_transport),
        "journal_bytes": sink.stats.get("journal_bytes"),
        "sink_stats": _plain(dict(sink.stats)),
        "original_fate_counts": dict(sorted(original_fates.items())),
        "issued_fate_counts": dict(sorted(issued_fates.items())),
        "postconsumer_state_counts": dict(sorted(postconsumer_states.items())),
        "fact_refs": list(fact_refs),
        "discovery_refs": list(discovery_refs),
        "batch_receipts": [
            {
                "unit": receipt.unit_ref.key,
                "state": receipt.state,
                "attempt_index": receipt.attempt_index,
                "execution_performed": receipt.execution_performed,
                "receipt_ref": receipt.receipt_ref.key,
                "result_refs": [ref.key for ref in receipt.result_refs],
            }
            for receipt in batch.receipts
        ],
        "joined": {
            "schema": joined.schema,
            "result_hash": joined.result_hash,
            "issued_decision_ref": joined.issued_decision_ref.key,
            "issuer_envelope_sha256": joined.issued_envelope_sha256,
            "release_ref": joined.release_ref.key,
            "estate_manifest_sha256": joined.estate_manifest_sha256,
            "audit": _plain(joined.audit),
            "operation_count": len(joined.rows),
            "receipted_operation_count": len(receipted),
            "noneligible_operation_count": len(noneligible),
            "noneligible_with_receipts": [
                row["operation_id"] for row in noneligible
                if row["postconsumer_receipt_refs"]
            ],
            "rows": _plain(joined.rows),
        },
        "compilation": {
            "frontier_hash": compilation.frontier_hash,
            "source_sha256": compilation.source_sha256,
            "plan_records": len(compilation.plan.records),
            "supported_records": sum(
                1 for entry in compilation.plan.records
                if entry.status == "SUPPORTED"
            ),
            "expected_candidates": len(compilation.plan.expected_candidates),
            "operation_dispositions": _plain(compilation.operation_dispositions),
            "operation_claim_classes": _plain(compilation.operation_claim_classes),
        },
        "workload": {
            "requests": len(workload.requests),
            "discoveries": len(workload.discoveries),
            "decision_ref": workload.decision_ref.key,
        },
        "_objects": result,
    }


def _sink_stats(handoff) -> Mapping[str, Any]:
    transport = handoff.body_transport or {}
    return {
        "complete": transport.get("complete"),
        "families": transport.get("families"),
        "journal_bytes": transport.get("journal_bytes"),
        "absences": transport.get("absences"),
    }


def _timed_cold_first_reader(tmp_path: Path) -> dict[str, Any]:
    fixture = _prepare_fixture(tmp_path / "fixture", (0., 1., 0., 1., 0.))
    handoff, estate, admission, compilation, resolver, _sink = _full_bundle(
        tmp_path / "cold", fixture)
    started = time.perf_counter()
    operation_id, result = _native_i03(admission, compilation)
    elapsed = time.perf_counter() - started
    fact = result.facts[0]
    return {
        "seconds": elapsed,
        "operation_id": operation_id,
        "fact_ref": fact.ref.key,
        "typed_state": fact.typed_state,
        "raw_numerator_support": fact.raw_numerator_support,
        "raw_denominator_support": fact.raw_denominator_support,
        "cells": _plain(fact.target_topology.get(
            "complete_cell_semantic_projection")),
        "source_open_count": handoff.stats.source_reads,
        "decode_calls": handoff.stats.decode_calls,
    }


def _full_bundle(tmp_path: Path, fixture):
    from rawlsing_next.tests.test_pyat997_s1e_saved_native_first_consumer import (
        _full,
    )
    return _full(tmp_path, fixture=fixture)


def _timed_i05_and_batch(bundle: dict[str, Any]) -> dict[str, Any]:
    (handoff, estate, admission, compilation, resolver, _batch, joined,
     _f, _d, _sink) = bundle["_objects"]
    workload = compilation.issued.workload
    discovery_ref = workload.discoveries[0]
    started = time.perf_counter()
    discovery = execute_saved_i05(
        admission, discovery_authority_ref=discovery_ref,
    )
    i05_seconds = time.perf_counter() - started
    manifest, predicates = _issued_manifest(workload, admission)
    started = time.perf_counter()
    batch = execute_saved_batch(
        admission, manifest=manifest, predicate_ref_by_query=predicates,
    )
    batch_seconds = time.perf_counter() - started
    # execute_saved_batch returns the completed runner; its exact receipts are
    # the only evidence the join accepts.
    from rawlsing_next.pre553_source_postconsumer_receipts import (
        join_saved_source_operation_fates,
    )
    from rawlsing_next.tests.test_pyat960_s1e_native_fact import (
        _NATIVE_HOST, _NATIVE_PURPOSE,
    )
    started = time.perf_counter()
    joined_timed = join_saved_source_operation_fates(
        handoff=handoff, estate_receipt=estate, admission=admission,
        compilation=compilation, workload=workload, resolver=resolver,
        host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, runner=batch,
    )
    join_seconds = time.perf_counter() - started
    return {
        "i05_seconds": i05_seconds,
        "i05_receipts": [r.ref.key for r in discovery.receipts],
        "batch_seconds": batch_seconds,
        "batch_units": len(batch.receipts),
        "batch_states": dict(sorted(Counter(
            r.state for r in batch.receipts).items())),
        "join_seconds": join_seconds,
        "join_result_hash": joined_timed.result_hash,
        "join_matches_first": joined_timed.result_hash == joined.result_hash,
        "join_positive_linked": joined_timed.audit[
            "positive_native_linked_operations"],
        "join_pending_eligible": joined_timed.audit[
            "pending_eligible_operations"],
    }


def _bridge_native_cells(tmp_path: Path) -> dict[str, Any]:
    baseline = _build_saved(
        tmp_path, name="bridge-baseline", native_fixture=True,
        values=(0., 1., 2., 0., 1.),
    )
    changed = _build_saved(
        tmp_path, name="bridge-changed", native_fixture=True,
        values=(0., 1., 1., 0., 1.),
    )
    restored = _build_saved(
        tmp_path, name="bridge-restored", fixture=baseline[0],
    )
    out = {}
    for label, bundle in (("baseline", baseline), ("changed", changed),
                          ("restored", restored)):
        _, handoff, sink, private = bundle
        estate = _bridge_estate(handoff, sink, private)
        started = time.perf_counter()
        result, raw_domain = _bridge_native_i03(estate, tag="PYAT997-EVIDENCE")
        elapsed = time.perf_counter() - started
        fact = result.facts[0]
        out[label] = {
            "source_sha256": handoff.source_sha256,
            "roots": _plain(asdict(handoff.roots)),
            "native_i03_seconds": elapsed,
            "fact_ref": fact.ref.key,
            "typed_state": fact.typed_state,
            "denominator": fact.raw_denominator_support,
            "cells": [
                [str(cell["cell"]), cell["raw_numerator_support"]]
                for cell in fact.target_topology[
                    "complete_cell_semantic_projection"]
            ],
            "raw_domain": sorted(raw_domain),
        }
    out["baseline_roots_equal_restored"] = (
        baseline[1].roots.logical == restored[1].roots.logical
        and baseline[1].roots.physical == restored[1].roots.physical
    )
    out["changed_roots_differ"] = (
        baseline[1].roots.logical != changed[1].roots.logical
    )
    out["baseline_fact_equal_restored"] = (
        out["baseline"]["fact_ref"] == out["restored"]["fact_ref"]
        and out["baseline"]["cells"] == out["restored"]["cells"]
    )
    out["changed_fact_differs"] = (
        out["baseline"]["fact_ref"] != out["changed"]["fact_ref"]
        and out["baseline"]["cells"] != out["changed"]["cells"]
    )
    return out


def main() -> int:
    started = time.perf_counter()
    peak_before = _peak_rss_bytes()
    tmp = Path(tempfile.mkdtemp(prefix="pyat997-evidence-")).resolve()
    fixture = _prepare_fixture(tmp / "fixture", (0., 1., 0., 1., 0.))

    # Count actual decoder snapshot acquisitions during the baseline chain.
    import rawlsing_next.pre553_physical_decoder as decoder
    original_snapshot = decoder._acquire_source_snapshot
    opens: list[int] = []

    def spy(*args, **kwargs):
        opens.append(1)
        return original_snapshot(*args, **kwargs)

    decoder._acquire_source_snapshot = spy
    try:
        baseline = _run_bundle(
            tmp / "runs", "baseline", (0., 1., 0., 1., 0.), fixture=fixture,
        )
    finally:
        decoder._acquire_source_snapshot = original_snapshot
    changed = _run_bundle(
        tmp / "runs", "changed", (0., 1., 1., 1., 0.),
    )
    restored = _run_bundle(
        tmp / "runs", "restored", (0., 1., 0., 1., 0.), fixture=fixture,
    )
    family_table = _family_table(
        baseline["_objects"][0], baseline["_objects"][1],
        tmp / "runs" / "baseline" / "private",
    )
    cold = _timed_cold_first_reader(tmp)
    timed = _timed_i05_and_batch(baseline)
    bridge = _bridge_native_cells(tmp / "bridge")

    baseline_joined = baseline["joined"]
    restored_joined = restored["joined"]
    changed_joined = changed["joined"]
    p0 = {
        "source_open_count": len(opens),
        "declared_source_reads": baseline["source_stats"]["source_reads"],
        "decode_calls": baseline["source_stats"]["decode_calls"],
        "cell_passes": baseline["source_stats"]["cell_passes"],
        "full_c11_builds": baseline["source_stats"]["full_c11_builds"],
        "legacy_full_c11_builds_expected": 0,
        "source_rows": baseline["source_rows"],
        "family_table": family_table,
        "roots": baseline["roots"],
        "manifest_sha256": baseline["manifest_sha256"],
        "estate_i02": baseline["estate_i02"],
        "retained_bytes": baseline["retained_bytes"],
        "parquet_files": _parquet_files(Path(baseline["estate_path"])),
        "journal_leftovers": [
            p.name for p in (tmp / "runs" / "baseline" / "private").glob(
                ".s1e-body-journal-*")
        ],
        "stage_leftovers": [
            p.name for p in (tmp / "runs" / "baseline" / "private").glob(
                ".s2c-stage-*")
        ],
        "estate_bytes_actual": _root_bytes(Path(baseline["estate_path"])),
        "changed_roots_differ": (
            baseline["roots"]["logical"] != changed["roots"]["logical"]
        ),
        "restored_roots_equal": (
            baseline["roots"]["logical"] == restored["roots"]["logical"]
            and baseline["roots"]["physical"] == restored["roots"]["physical"]
        ),
        "baseline_fact_refs": baseline["fact_refs"],
        "changed_fact_refs": changed["fact_refs"],
        "restored_fact_refs": restored["fact_refs"],
        "baseline_discovery_refs": baseline["discovery_refs"],
        "changed_discovery_refs": changed["discovery_refs"],
        "restored_discovery_refs": restored["discovery_refs"],
        "baseline_joined_result_hash": baseline_joined["result_hash"],
        "restored_joined_result_hash": restored_joined["result_hash"],
        "changed_joined_result_hash": changed_joined["result_hash"],
        "restored_joined_equal": (
            baseline_joined["result_hash"] == restored_joined["result_hash"]
        ),
        "changed_joined_differs": (
            baseline_joined["result_hash"] != changed_joined["result_hash"]
        ),
        "batch_states": timed["batch_states"],
        "batch_units": timed["batch_units"],
        "cold_first_reader": cold,
        "i05_receipts": timed["i05_receipts"],
        "timed_phases": timed,
        "bridge_native": bridge,
    }
    p1 = {
        "original_fate_counts": baseline["original_fate_counts"],
        "issued_fate_counts": baseline["issued_fate_counts"],
        "postconsumer_state_counts": baseline["postconsumer_state_counts"],
        "operation_anti_join": {
            "original_operations": len(
                baseline["original_fate_counts"].values()) and sum(
                    baseline["original_fate_counts"].values()),
            "joined_rows": baseline_joined["operation_count"],
            "issued_dispositions": sum(
                baseline["issued_fate_counts"].values()),
            "missing_from_join": sorted(
                set(baseline["compilation"]["operation_dispositions"])
                - {row["operation_id"] for row in baseline_joined["rows"]}
            ),
            "extra_in_join": sorted(
                {row["operation_id"] for row in baseline_joined["rows"]}
                - set(baseline["compilation"]["operation_dispositions"])
            ),
        },
        "audit": baseline_joined["audit"],
        "issuer_decision_ref": baseline_joined["issued_decision_ref"],
        "issuer_envelope_sha256": baseline_joined["issuer_envelope_sha256"],
        "release_ref": baseline_joined["release_ref"],
        "estate_manifest_sha256": baseline_joined["estate_manifest_sha256"],
        "receipted_operation_count": baseline_joined[
            "receipted_operation_count"],
        "noneligible_operation_count": baseline_joined[
            "noneligible_operation_count"],
        "noneligible_with_receipts": baseline_joined[
            "noneligible_with_receipts"],
        "pending_eligible_operations": baseline_joined["audit"][
            "pending_eligible_operations"],
        "positive_native_linked_operations": baseline_joined["audit"][
            "positive_native_linked_operations"],
        "rows": baseline_joined["rows"],
        "changed_joined": {
            "original_fate_counts": changed["original_fate_counts"],
            "issued_fate_counts": changed["issued_fate_counts"],
            "postconsumer_state_counts": changed["postconsumer_state_counts"],
            "result_hash": changed_joined["result_hash"],
        },
        "restored_joined": {
            "original_fate_counts": restored["original_fate_counts"],
            "issued_fate_counts": restored["issued_fate_counts"],
            "postconsumer_state_counts": restored["postconsumer_state_counts"],
            "result_hash": restored_joined["result_hash"],
        },
    }
    elapsed = time.perf_counter() - started
    peak_after = _peak_rss_bytes()
    environment = {
        "git_head": _git("rev-parse", "HEAD"),
        "git_branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
        "git_status": _git("status", "--short"),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "python": sys.version,
        "python_executable": sys.executable,
        "proc_self_fd": os.path.isdir("/proc/self/fd"),
        "dependencies": {
            "pytest": __import__("pytest").__version__,
            "pyarrow": pyarrow.__version__,
            "duckdb": duckdb.__version__,
            "pyreadstat": pyreadstat.__version__,
            "pandas": __import__("pandas").__version__,
            "numpy": __import__("numpy").__version__,
        },
    }
    evidence = {
        "schema": "PYAT997_S1E_EXEC_RUNTIME_EVIDENCE@1",
        "scope": "TEST_ONLY_SOURCEFREE_TINY_FIXTURE_NOT_PRODUCTION",
        "environment": environment,
        "resource": {
            "wall_seconds_total": elapsed,
            "peak_rss_bytes_before": peak_before,
            "peak_rss_bytes_after": peak_after,
            "peak_rss_mib": round(peak_after / (1024 * 1024), 3),
            "source_rows": baseline["source_rows"],
            "source_rows_per_second_total": round(
                baseline["source_rows"] / elapsed, 3),
            "events": baseline["source_stats"]["event_count"],
            "journal_bytes": baseline["journal_bytes"],
            "spool_bytes": baseline["source_stats"]["spool_bytes"],
            "retained_bytes": baseline["retained_bytes"],
            "estate_bytes_actual": p0["estate_bytes_actual"],
            "cold_i03_seconds": cold["seconds"],
            "i05_seconds": timed["i05_seconds"],
            "batch_seconds": timed["batch_seconds"],
            "join_seconds": timed["join_seconds"],
            "baseline_chain_seconds": baseline["wall_seconds"],
            "changed_chain_seconds": changed["wall_seconds"],
            "restored_chain_seconds": restored["wall_seconds"],
        },
        "p0": p0,
        "p1": p1,
        "honesty": {
            "fixture_rows": baseline["source_rows"],
            "production_100k_or_6gib_claimed": False,
            "original35_rights_claimed": False,
            "independent_g5": "PENDING_INDEPENDENT_RECEIVING",
            "separate_1006_engine_optimization_authority": True,
        },
    }
    target = HERE / (
        "p0p1_runtime_linux.json" if os.path.isdir("/proc/self/fd")
        else "p0p1_runtime_darwin.json"
    )
    target.write_text(
        json.dumps(evidence, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "wrote": str(target),
        "p0_source_opens": p0["source_open_count"],
        "p0_families": family_table["family_total"],
        "p0_cold_state": cold["typed_state"],
        "p0_changed_fact_differs": p0["changed_fact_refs"]
        != p0["baseline_fact_refs"],
        "p0_restore": p0["restored_roots_equal"]
        and p0["restored_joined_equal"],
        "p1_operations": p1["audit"]["operation_count"],
        "p1_positive_linked": p1["positive_native_linked_operations"],
        "p1_pending_eligible": p1["pending_eligible_operations"],
        "p1_noneligible_with_receipts": p1["noneligible_with_receipts"],
        "peak_rss_mib": round(peak_after / (1024 * 1024), 3),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
