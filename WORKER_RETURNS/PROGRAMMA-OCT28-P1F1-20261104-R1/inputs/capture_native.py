"""Compare full synthetic native outputs and externally pinned checkpoint bytes."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys
from unittest.mock import patch

from rawlsing_next import pre553_issued_workload as workload
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.tests import test_universal_world_binding as joined

source, destination = map(Path, sys.argv[1:])
route_results = []
checkpoint_bytes = []
mutation = []
route_original = workload.execute_route_b_production
restore_original = workload.restore_joined_checkpoint


def record_route(*args, **kwargs):
    result = route_original(*args, **kwargs)
    release = result.c11_release
    route_results.append({
        "source": result.source_identity,
        "projection": result.projection_binding_receipt,
        "release_ref": release.release_ref.as_dict(),
        "source_artifact_ref": release.source_artifact_ref.as_dict(),
        "source_release_manifest_hash": release.source_release_manifest_hash,
        "c11_objects": [obj.as_dict() for obj in release.public_objects],
        "c11_internal": [obj.as_dict() for obj in release.internal_records],
        "route_objects": [obj.as_dict() for obj in result.object_graph.public_objects()],
        "route_refs": [obj.ref.as_dict() for obj in result.object_graph.public_objects()],
        "fact_replay_refs": [obj.replay_ref for obj in result.object_graph.empirical_facts],
        "learned_execution_receipt": result.learned_empirical_execution_receipt,
        "route_replay": result.replay_receipt,
    })
    return result


def record_restore(material, *, expected_checkpoint_ref):
    wire = workload.canonical(material)
    if wire not in checkpoint_bytes:
        checkpoint_bytes.append(wire)
    if not mutation:
        changed = deepcopy(json.loads(wire))
        before = changed["entries"][0]["source_sha256"]
        assert before == sha256(source.read_bytes()).hexdigest()
        changed["entries"][0]["source_sha256"] = "b" * 64
        entry = changed["entries"][0]
        entry["entry_hash"] = semantic_hash({k: v for k, v in entry.items() if k != "entry_hash"})
        changed["checkpoint_hash"] = semantic_hash(
            {k: v for k, v in changed.items() if k != "checkpoint_hash"})
        try:
            restore_original(changed, expected_checkpoint_ref=expected_checkpoint_ref)
        except workload.WorkloadAdmissionError as exc:
            assert str(exc) == "JOINED_CHECKPOINT_PIN_MISMATCH", str(exc)
        else:
            raise AssertionError("changed authoritative source determinant was admitted")
        mutation.append({
            "original_source_sha256": before,
            "mutated_source_sha256": entry["source_sha256"],
            "original_checkpoint_pin": expected_checkpoint_ref,
            "rehashed_mutation": changed["checkpoint_hash"],
            "refusal": "JOINED_CHECKPOINT_PIN_MISMATCH",
        })
    return restore_original(material, expected_checkpoint_ref=expected_checkpoint_ref)


runtime, scratch = joined._materialize_p41_runtime()
try:
    with patch.object(workload, "execute_route_b_production", record_route), \
         patch.object(workload, "restore_joined_checkpoint", record_restore):
        result = joined._same_source_connected(str(runtime), source)
finally:
    shutil.rmtree(scratch)
assert route_results and checkpoint_bytes and mutation
assert result["view"].state == "R05_WORLD_SELECTED_VIEW"
for number, wire in enumerate(checkpoint_bytes):
    (destination / f"checkpoint-{number}.json").write_bytes(wire)
(destination / "native.json").write_bytes(workload.canonical({
    "routes": route_results,
    "consumer": result["view"].consumer_values_read,
    "identities": result["hashes"],
    "mutations": mutation,
}))
