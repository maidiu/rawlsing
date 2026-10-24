"""R91-R04V R2 independent successor probes (TEST_ONLY)."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import os
import subprocess
import sys

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_issued_workload import (
    WorkloadAdmissionError, capture_joined_checkpoint, execute_issued_workload,
    restore_joined_checkpoint, resume_joined_workloads,
)
from rawlsing_next.pre553_native_workload_binding import execute_test_only_workload
from rawlsing_next.tests.test_universal_workload import (
    AS_OF as GOV_AS_OF, HOST as GOV_HOST, PURPOSE as GOV_PURPOSE,
    _frontier_bundle, _frontier_fixture,
)
from rawlsing_next.tests.test_universal_workload_custody import (
    AS_OF, HOST, PURPOSE, _issued_workloads,
)
from r04v_r3_helper import build_multi

REPO_ROOT = Path(__file__).resolve().parents[5]
PROBE_DIR = Path(__file__).resolve().parent


def _first(issued, bundle):
    return execute_test_only_workload(
        issued=issued[0], source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE,
    )


def _forge_checkpoint(checkpoint):
    material = deepcopy(checkpoint.material())
    entry = material["entries"][0]
    forged = ExactRef("EmpiricalFact@1.0.0", "urn:forged:r04v:r2", "f" * 64).as_dict()
    entry["output_refs"] = [forged]
    for receipt in entry["receipt_materials"]:
        receipt["result_refs"] = [forged]
    entry_payload = {
        "decision_ref": entry["decision_ref"],
        "envelope_sha256": entry["envelope_sha256"],
        "source_sha256": entry["source_sha256"],
        "manifest_hash": entry["manifest_hash"],
        "kind": entry["kind"], "state": entry["state"],
        "unit_materials": entry["unit_materials"],
        "completed_outputs": entry["completed_outputs"],
        "receipt_materials": entry["receipt_materials"],
        "output_refs": entry["output_refs"],
    }
    entry["entry_hash"] = semantic_hash(entry_payload)
    material["checkpoint_hash"] = semantic_hash({
        "schema": material["schema"], "entries": material["entries"],
    })
    return restore_joined_checkpoint(
        material, expected_checkpoint_ref=material["checkpoint_hash"])


def test_H1_actual_governed_capture_retained_facts(tmp_path):
    from rawlsing_next.pre553_universal_workload import (
        compile_governed_frontier, execute_governed_frontier,
    )
    bundle, _ = _frontier_bundle(tmp_path / "r04v_r2_governed.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=GOV_AS_OF, host=GOV_HOST, purpose=GOV_PURPOSE,
    )
    governed = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    native = governed.native_execution
    checkpoint = capture_joined_checkpoint(
        (native,), source_sha256_by_decision={
            native.decision_ref.key: compilation.issued.record.source_sha256,
        })
    pin = checkpoint.checkpoint_hash
    restored = restore_joined_checkpoint(
        checkpoint.material(), expected_checkpoint_ref=pin)
    resumed = resume_joined_workloads(
        workloads=(compilation.issued,),
        source_factory=lambda _ref: bundle.physical_stream,
        host=GOV_HOST, purpose=GOV_PURPOSE, checkpoint=restored,
        expected_checkpoint_ref=pin,
    )
    completed = resumed.completed_results[0]
    assert tuple(fact.ref for fact in completed.native_result.empirical_facts) == tuple(
        fact.ref for fact in native.native_result.empirical_facts)
    assert completed.manifest.manifest_hash == native.manifest.manifest_hash


def test_H2_external_pin_rejects_rehashed_checkpoint(tmp_path):
    bundle, issued = _issued_workloads(tmp_path)
    first = _first(issued, bundle)
    checkpoint = capture_joined_checkpoint((first,))
    pin = checkpoint.checkpoint_hash
    forged = _forge_checkpoint(checkpoint)
    assert forged.checkpoint_hash != pin
    with pytest.raises(Exception):
        resume_joined_workloads(
            workloads=issued,
            source_factory=lambda _ref: bundle.physical_stream,
            host=HOST, purpose=PURPOSE, checkpoint=forged,
            expected_checkpoint_ref=pin,
        )


def test_H3_completed_resume_preserves_native_outputs_manifest(tmp_path):
    bundle, issued = _issued_workloads(tmp_path)
    first = _first(issued, bundle)
    checkpoint = capture_joined_checkpoint((first,))
    resumed = resume_joined_workloads(
        workloads=issued,
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
        expected_checkpoint_ref=checkpoint.checkpoint_hash,
    )
    completed = resumed.completed_results[0]
    assert completed.manifest == first.manifest
    assert completed.native_outputs
    original_output = first.native_outputs[0]
    retained_output = completed.native_outputs[0]
    assert retained_output.query_ref == original_output.query_ref, (
        "completed output view lost the native query identity"
    )
    assert tuple(fact.ref.key for fact in retained_output.facts) == tuple(
        fact.ref.key for fact in original_output.facts
    )


def test_H4_real_partial_multiunit_fresh_process(tmp_path):
    bundle, issued = _issued_workloads(tmp_path)
    multi, resolver = build_multi(
        bundle, issued, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    partial = execute_issued_workload(
        multi.workload, resolver,
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True, max_units=1,
    )
    assert len(partial.receipts) == 1 and len(partial.manifest.units) == 2
    checkpoint = capture_joined_checkpoint((partial,))
    pin = checkpoint.checkpoint_hash
    uninterrupted = execute_issued_workload(
        multi.workload, resolver,
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    checkpoint_path = tmp_path / "r04v_r2_partial_checkpoint.json"
    checkpoint_path.write_text(json.dumps(checkpoint.material(), sort_keys=True))
    source_path = tmp_path / "r91_r04.sav"
    code = """
import json, sys
from pathlib import Path
from rawlsing_next.tests.test_universal_source_projection import load_s3
from rawlsing_next.pre553_universal_workload import compile_universal_workload
from rawlsing_next.pre553_issued_workload import (
    execute_issued_workload, restore_joined_checkpoint, resume_joined_workloads,
)
from r04v_r3_helper import build_multi
bundle = load_s3(Path(sys.argv[1]))
compilation = compile_universal_workload(
    bundle=bundle, as_of=sys.argv[3], host=sys.argv[4], purpose=sys.argv[5])
issued = tuple(item.issued for item in compilation.compiled if item.issued is not None)
multi, resolver = build_multi(bundle, issued, as_of=sys.argv[3],
                              host=sys.argv[4], purpose=sys.argv[5])
pin = sys.argv[6]
checkpoint = restore_joined_checkpoint(
    json.loads(open(sys.argv[2], encoding="utf-8").read()),
    expected_checkpoint_ref=pin)
resumed = resume_joined_workloads(
    workloads=(multi,), source_factory=lambda _ref: bundle.physical_stream,
    host=sys.argv[4], purpose=sys.argv[5], checkpoint=checkpoint,
    expected_checkpoint_ref=pin)
final = resumed.resumed_results[0]
print(json.dumps({
    "states": [r.state for r in final.receipts],
    "output_refs": [ref.key for ref in resumed.output_refs],
    "facts": sorted(ref.key for output in final.outputs_by_unit.values()
                    for fact in output.facts for ref in (fact.ref,)),
}, sort_keys=True))
"""
    env = dict(os.environ)
    env["PYTHONPATH"] = (
        str(REPO_ROOT) + os.pathsep + str(PROBE_DIR)
        + os.pathsep + env.get("PYTHONPATH", "")
    )
    proc = subprocess.run(
        [sys.executable, "-c", code, str(source_path), str(checkpoint_path),
         AS_OF, HOST, PURPOSE, pin],
        cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-3000:]
    child = json.loads(proc.stdout)
    assert child["states"] == ["COMPLETED", "COMPLETED"]
    assert child["output_refs"] == sorted(
        ref.key for receipt in uninterrupted.receipts for ref in receipt.result_refs)
    expected_facts = sorted(
        fact.ref.key for output in uninterrupted.outputs_by_unit.values()
        for fact in output.facts)
    assert child["facts"] == expected_facts


def test_H5_governed_discovery_view_identity_and_freeze(tmp_path):
    from dataclasses import FrozenInstanceError
    from rawlsing_next.pre553_issued_workload import RetainedDiscoveryResultView
    from rawlsing_next.pre553_universal_workload import (
        compile_governed_frontier, execute_governed_frontier,
    )
    bundle, _ = _frontier_bundle(tmp_path / "r04v_r3_governed.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=GOV_AS_OF, host=GOV_HOST, purpose=GOV_PURPOSE,
    )
    governed = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    native = governed.native_execution
    checkpoint = capture_joined_checkpoint(
        (native,), source_sha256_by_decision={
            native.decision_ref.key: compilation.issued.record.source_sha256,
        })
    pin = checkpoint.checkpoint_hash
    resumed = resume_joined_workloads(
        workloads=(compilation.issued,),
        source_factory=lambda _ref: bundle.physical_stream,
        host=GOV_HOST, purpose=GOV_PURPOSE, checkpoint=checkpoint,
        expected_checkpoint_ref=pin,
    )
    view = resumed.completed_results[0].native_result
    assert isinstance(view, RetainedDiscoveryResultView)
    assert view.evaluated_frontier_ref == native.native_result.evaluated_frontier_ref
    assert view.replay_ref == native.native_result.replay_ref
    assert view.empirical_fact_refs == native.native_result.empirical_fact_refs
    assert view.receipts == native.native_result.receipts
    assert view.executed_predicate_refs == tuple(
        p.ref for p in native.native_result.executed_predicates)
    assert view.executed_query_refs == tuple(
        q.ref for q in native.native_result.executed_queries)
    with pytest.raises(FrozenInstanceError):
        view.candidate_count = 0
