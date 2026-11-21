"""A-counter: full retained-output identity binding under native receipts.

B's cache repair bound fact/receipt refs but not the per-unit query identity or
the retained discovery view metadata. These tests poison those identities while
recomputing the entry/checkpoint content hashes and preserving the original
unit receipt. The first reader must refuse before any source open.
"""
from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path
import tempfile

import pytest

import rawlsing_next.pre553_issued_workload as issued_module
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_issued_workload import (
    WorkloadAdmissionError, capture_joined_checkpoint, execute_issued_workload,
    resume_joined_workloads,
)
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_universal_workload import (
    compile_governed_frontier, execute_governed_frontier,
)
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import (
    CurrentIssuer, HOST, PURPOSE, _build_multi_unit_issued,
)
from rawlsing_next.tests.test_universal_source_projection import build_s3, s3_rows
from rawlsing_next.tests.test_universal_workload import (
    _frontier_bundle, _frontier_fixture,
)
from rawlsing_next.tests.test_universal_workload_custody import AS_OF


def _entry_hash(entry):
    return semantic_hash({
        key: value for key, value in entry.material().items()
        if key != "entry_hash"
    })


def _checkpoint_hash(checkpoint):
    return semantic_hash({
        "schema": checkpoint.schema,
        "entries": [entry.material() for entry in checkpoint.entries],
    })


def _rehashed_checkpoint(checkpoint, row, unit_hash):
    entry = checkpoint.entries[0]
    outputs = dict(entry.completed_outputs)
    outputs[unit_hash] = row
    entry = replace(entry, completed_outputs=outputs)
    entry = replace(entry, entry_hash=_entry_hash(entry))
    poisoned = replace(checkpoint, entries=(entry,))
    return replace(poisoned, checkpoint_hash=_checkpoint_hash(poisoned))


def _poisoned_row(entry, mutate):
    unit_hash, row = next(iter(entry.completed_outputs.items()))
    poisoned = copy.deepcopy(row)
    mutate(poisoned)
    return unit_hash, poisoned


def _rehash_entry(checkpoint, entry):
    entry = replace(entry, entry_hash=_entry_hash(entry))
    poisoned = replace(checkpoint, entries=(entry,))
    return replace(poisoned, checkpoint_hash=_checkpoint_hash(poisoned))


@pytest.fixture(scope="module")
def court(tmp_path_factory):
    path = tmp_path_factory.mktemp("s1d-a-counter") / "counter.sav"
    bundle = build_s3(path, s3_rows(respondents=6, occasions=2))
    issued = _build_multi_unit_issued(bundle)
    full = execute_issued_workload(
        issued.workload, TestOnlyDecisionResolver(issued.record),
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    checkpoint = capture_joined_checkpoint((full,))
    return type("Court", (), {
        "bundle": bundle, "issued": issued, "full": full,
        "checkpoint": checkpoint,
        "checkpoint_material": copy.deepcopy(checkpoint.material()),
        "full_output_refs": tuple(ref.key for ref in full.output_refs),
        "full_manifest_hash": full.manifest.manifest_hash,
    })()


def _resume_refuses(court, checkpoint, expected_code):
    source_calls = {"n": 0}

    def factory(_ref):
        source_calls["n"] += 1
        return court.bundle.physical_stream

    with pytest.raises(WorkloadAdmissionError, match=expected_code):
        resume_joined_workloads(
            workloads=(court.issued,), resolver=CurrentIssuer((court.issued.record,)),
            source_factory=factory, host=HOST, purpose=PURPOSE,
            checkpoint=checkpoint, expected_checkpoint_ref=checkpoint.checkpoint_hash,
            allow_test_only=True,
        )
    assert source_calls["n"] == 0


def test_query_ref_identity_poison_refused(court):
    unit_hash, row = _poisoned_row(
        court.checkpoint.entries[0],
        lambda row: row.__setitem__("query_ref", ExactRef(
            "EmpiricalQuerySpec@1.0.0",
            "urn:rawlsing:pre553:EmpiricalQuerySpec:sha256:" + "d" * 64,
            "d" * 64,
        ).as_dict()),
    )
    poisoned = _rehashed_checkpoint(court.checkpoint, row, unit_hash)
    assert poisoned.checkpoint_hash != court.checkpoint.checkpoint_hash
    _resume_refuses(court, poisoned, "JOINED_CHECKPOINT_OUTPUT_QUERY_MISMATCH")


def test_query_release_identity_poison_refused(court):
    unit_hash, row = _poisoned_row(
        court.checkpoint.entries[0],
        lambda row: row.__setitem__("release_refs", [ExactRef(
            "C11LogicalRelease", "urn:rawlsing:fake:release", "e" * 64,
        ).as_dict()]),
    )
    poisoned = _rehashed_checkpoint(court.checkpoint, row, unit_hash)
    _resume_refuses(court, poisoned, "JOINED_CHECKPOINT_OUTPUT_RELEASE_MISMATCH")


def test_query_scope_mode_poison_refused(court):
    unit_hash, row = _poisoned_row(
        court.checkpoint.entries[0],
        lambda row: row.__setitem__("source_scope_mode", "AUTHORIZED_COMPOSITE"),
    )
    poisoned = _rehashed_checkpoint(court.checkpoint, row, unit_hash)
    _resume_refuses(court, poisoned, "JOINED_CHECKPOINT_OUTPUT_SCOPE_MODE_MISMATCH")


def _rebind_unit(court, mutate_unit, *, base=None):
    assert court.checkpoint.material() == court.checkpoint_material
    assert tuple(ref.key for ref in court.full.output_refs) == court.full_output_refs
    assert court.full.manifest.manifest_hash == court.full_manifest_hash
    checkpoint = base if base is not None else court.checkpoint
    entry = checkpoint.entries[0]
    unit_materials = copy.deepcopy(list(entry.unit_materials))
    index = next(
        i for i, row in enumerate(unit_materials) if row["job_kind"] == "QUERY"
    )
    mutate_unit(unit_materials[index])
    old_manifest = issued_module._restore_manifest(entry.unit_materials)
    new_manifest = issued_module._restore_manifest(unit_materials)
    # BatchManifest canonicalizes unit order; locate the exact mutated unit by
    # rebuilding a one-unit manifest rather than assuming it stays at index.
    old_unit = issued_module._restore_manifest(
        (entry.unit_materials[index],)
    ).units[0]
    new_unit = issued_module._restore_manifest((unit_materials[index],)).units[0]
    outputs = dict(entry.completed_outputs)
    outputs[new_unit.unit_hash] = outputs.pop(old_unit.unit_hash)
    receipt_materials = []
    for row in entry.receipt_materials:
        row = dict(row)
        row["manifest_hash"] = new_manifest.manifest_hash
        if issued_module.exact_ref(row["unit_ref"]).key == old_unit.unit_ref.key:
            row["unit_ref"] = new_unit.unit_ref.as_dict()
        receipt_materials.append(row)
    entry = replace(
        entry, unit_materials=tuple(unit_materials),
        completed_outputs=outputs, receipt_materials=tuple(receipt_materials),
        manifest_hash=new_manifest.manifest_hash,
    )
    return _rehash_entry(checkpoint, entry)


def test_unit_decision_ref_poison_refused(court):
    def mutate(unit):
        refs = list(unit["semantic_input_refs"])
        refs[1] = ExactRef(
            "TEST_ONLY_DECISION", "urn:fake:s1d:decision", "1" * 64,
        ).as_dict()
        unit["semantic_input_refs"] = refs

    poisoned = _rebind_unit(
        court, mutate, base=capture_joined_checkpoint((court.full,))
    )
    _resume_refuses(
        court, poisoned, "JOINED_CHECKPOINT_OUTPUT_DECISION_MISMATCH"
    )


def test_unit_query_ref_poison_refused(court):
    fake = ExactRef(
        "EmpiricalQuerySpec@1.0.0",
        "urn:rawlsing:pre553:EmpiricalQuerySpec:sha256:" + "2" * 64,
        "2" * 64,
    )
    def mutate(unit):
        unit["job_ref"] = fake.as_dict()

    poisoned = _rebind_unit(
        court, mutate, base=capture_joined_checkpoint((court.full,))
    )
    _resume_refuses(court, poisoned, "JOINED_CHECKPOINT_OUTPUT_UNIT_MISMATCH")


def _governed_discovery(tmp_path):
    bundle, _ = _frontier_bundle(tmp_path / "discovery.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    governed = execute_governed_frontier(
        compilation=compilation, source_factory=lambda _ref: bundle.physical_stream,
    )
    native = governed.native_execution
    checkpoint = capture_joined_checkpoint(
        (native,),
        source_sha256_by_decision={
            native.decision_ref.key: compilation.issued.record.source_sha256
        },
    )
    return compilation.issued, checkpoint, bundle


def test_valid_discovery_view_resumes(tmp_path):
    issued, checkpoint, bundle = _governed_discovery(tmp_path)
    result = resume_joined_workloads(
        workloads=(issued,), resolver=CurrentIssuer((issued.record,)),
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
        expected_checkpoint_ref=checkpoint.checkpoint_hash, allow_test_only=True,
    )
    assert len(result.completed_results) == 1
    assert result.resumed_results == ()
    assert result.completed_results[0].native_result.replay_ref


def test_discovery_view_metadata_poisons_refused(tmp_path):
    issued, checkpoint, bundle = _governed_discovery(tmp_path)
    entry = checkpoint.entries[0]
    unit_hash, row = next(iter(entry.completed_outputs.items()))
    assert row["kind"] == "DISCOVERY"

    def attempt(mutate, expected_code):
        poisoned_row = copy.deepcopy(row)
        mutate(poisoned_row)
        poisoned = _rehashed_checkpoint(checkpoint, poisoned_row, unit_hash)
        with pytest.raises(WorkloadAdmissionError, match=expected_code):
            resume_joined_workloads(
                workloads=(issued,), resolver=CurrentIssuer((issued.record,)),
                source_factory=lambda _ref: bundle.physical_stream,
                host=HOST, purpose=PURPOSE, checkpoint=poisoned,
                expected_checkpoint_ref=poisoned.checkpoint_hash,
                allow_test_only=True,
            )

    attempt(
        lambda r: r.__setitem__("evaluated_frontier_ref", ExactRef(
            "PRE553_I05_EVALUATED_FRONTIER", "urn:fake:frontier", "f" * 64,
        ).as_dict()),
        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_REPLAY_MISMATCH",
    )
    attempt(
        lambda r: r.__setitem__("replay_ref", ExactRef(
            "PRE553_I05_FRONTIER_REPLAY", "urn:fake:replay", "a" * 64,
        ).as_dict()),
        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_REPLAY_MISMATCH",
    )
    attempt(
        lambda r: r.__setitem__("candidate_grammar_ref", ExactRef(
            "PRE553_I05_CANDIDATE_GRAMMAR", "urn:fake:grammar", "b" * 64,
        ).as_dict()),
        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_GRAMMAR_MISMATCH",
    )
    attempt(
        lambda r: r.__setitem__("executed_query_refs", []),
        "JOINED_CHECKPOINT_OUTPUT_DISCOVERY_QUERY_MISMATCH",
    )
