"""R91 R04V independent joined custody probes (TEST_ONLY)."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_issued_workload import (
    capture_joined_checkpoint, restore_joined_checkpoint, resume_joined_workloads,
)
from rawlsing_next.pre553_native_workload_binding import execute_test_only_discovery_workload
from rawlsing_next.pre553_universal_workload import compile_governed_frontier
from rawlsing_next.tests.test_universal_workload import (
    AS_OF as GOV_AS_OF, HOST as GOV_HOST, PURPOSE as GOV_PURPOSE,
    _frontier_bundle, _frontier_fixture,
)
from rawlsing_next.tests.test_universal_workload_custody import (
    AS_OF, HOST, PURPOSE, _execute_all, _issued_workloads,
)


def _first_result(issued, bundle):
    from rawlsing_next.pre553_native_workload_binding import execute_test_only_workload
    return execute_test_only_workload(
        issued=issued[0], source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE,
    )


def _forge_checkpoint(checkpoint):
    material = deepcopy(checkpoint.material())
    entry = material["entries"][0]
    forged = ExactRef(
        "EmpiricalFact@1.0.0", "urn:forged:r04v-fact", "f" * 64
    ).as_dict()
    entry["output_refs"] = [forged]
    for receipt in entry["receipt_materials"]:
        receipt["result_refs"] = [forged]
    entry_payload = {
        "decision_ref": entry["decision_ref"],
        "envelope_sha256": entry["envelope_sha256"],
        "source_sha256": entry["source_sha256"],
        "manifest_hash": entry["manifest_hash"],
        "receipt_materials": entry["receipt_materials"],
        "output_refs": entry["output_refs"],
    }
    entry["entry_hash"] = semantic_hash(entry_payload)
    material["checkpoint_hash"] = semantic_hash({
        "schema": material["schema"], "entries": material["entries"],
    })
    return restore_joined_checkpoint(material)


def test_H1_actual_governed_r03_result_is_consumable(tmp_path):
    bundle, _ = _frontier_bundle(tmp_path / "r04v_governed.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=GOV_AS_OF, host=GOV_HOST, purpose=GOV_PURPOSE,
    )
    discovery = execute_test_only_discovery_workload(
        issued=compilation.issued,
        source_factory=lambda _ref: bundle.physical_stream,
        host=GOV_HOST, purpose=GOV_PURPOSE,
    )
    # The authorized joined custody interface must consume the actual R03
    # governed-issued discovery result, not only unary NativeWorkloadResults.
    capture_joined_checkpoint((discovery,))


def test_H2_self_hashed_checkpoint_forgery_must_refuse(tmp_path):
    bundle, issued = _issued_workloads(tmp_path)
    first = _first_result(issued, bundle)
    checkpoint = capture_joined_checkpoint((first,))
    forged = _forge_checkpoint(checkpoint)
    # Only the candidate-controlled checkpoint was rewritten and rehashed;
    # there is no separately provisioned original pin.
    with pytest.raises(Exception):
        resume_joined_workloads(
            workloads=issued,
            source_factory=lambda _ref: bundle.physical_stream,
            host=HOST, purpose=PURPOSE, checkpoint=forged,
        )


def test_H3_completed_resume_preserves_native_outputs_and_manifest(tmp_path):
    bundle, issued = _issued_workloads(tmp_path)
    first = _first_result(issued, bundle)
    assert first.native_outputs
    checkpoint = capture_joined_checkpoint((first,))
    resumed = resume_joined_workloads(
        workloads=issued,
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
    )
    completed = resumed.completed_results[0]
    assert completed.native_outputs == first.native_outputs, (
        "completed resume lost the retained native output/fact objects"
    )
    assert completed.manifest == first.manifest, (
        "completed resume substituted a synthetic manifest instead of the original"
    )
