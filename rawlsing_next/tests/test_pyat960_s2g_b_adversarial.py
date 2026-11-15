"""S2-G Role-B adversarial repairs and same-chain evidence.

These tests were written after reproducing three material failures in the first
artifact:

1. an artifact could be published with an M1 disposition/fact chain that was not
   drawn from the declared accepted S2-F closure, and the real world consumer
   still returned ``LEARNED_CONSUMER_EXACT_SUPPORTED``;
2. ``resolve_as_of_checkpoint`` accepted an unpinned foreign checkpoint and
   returned a release that was not in the artifact's retained history;
3. a coherently rewritten B5 replay receipt was accepted at open.

The tests also prove the frozen G2 change/restore property with an actual native
fact change in the same source/release chain, not merely a different family-rule
label or a different fixture tag.
"""
from __future__ import annotations

import dataclasses
from pathlib import Path
import json
import shutil
import tempfile
import zlib

import pytest

import rawlsing_next.pre553_learned_empirical_adjudication as m1
import rawlsing_next.pre553_learned_world_composition as i4
import rawlsing_next.pre553_durable_learned_lifecycle as durable
from rawlsing_next.pre553_analytical_composition import (
    _validate_discovery_consumption,
    compose_positioned_subject_possibility,
)
from rawlsing_next.pre553_durable_empirical_closure import (
    NativeEmpiricalOutput,
    publish_empirical_closure,
)
from rawlsing_next.pre553_durable_learned_lifecycle import (
    DurableLearnedLifecycleError,
    DurableLearnedLifecycleRefusal,
    DurableLearnedLifecycleUntrusted,
    LearnedConsumerDeterminants,
    open_learned_lifecycle,
    publish_learned_lifecycle,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import ExactRef, canonical_json, semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleExecutor
from rawlsing_next.pre553_learned_product_release import M2Repository
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import (
    _binding,
    _bundle,
    _clone_fact,
    _m1_authority,
    _receipt_with_fact,
    _registry,
)
from rawlsing_next.tests.test_pre553_learned_world_composition import (
    _contract,
    _disposition,
)
from rawlsing_next.tests.test_pre553_route_b_production import _execute, _fixture
from rawlsing_next.tests.test_pyat960_s2g_durable_lifecycle import (
    _artifact_case,
    _copy_artifact,
    _load_core,
    _rewrite_artifact,
)


def _changed_native_case(tmp_path: Path, base: dict) -> dict:
    """Build the same native M01 chain with one real physical cell changed.

    R1/X is changed 1→0 and R2/X is changed 0→1.  The producer query,
    predicate, source universe and discovery rule remain the same, but the
    native X1/ALL facts, the M1 disposition, M2 release, B5 selection and world
    consumer result all change.
    """

    original_fixture = _fixture()
    cells = list(original_fixture["stream"].cell_iter_factory())
    changed_cells = []
    for cell in cells:
        if cell.row_ordinal == 1 and cell.variable_name == "X" and cell.raw_value == "1":
            cell = dataclasses.replace(cell, raw_value="0")
        elif cell.row_ordinal == 2 and cell.variable_name == "X" and cell.raw_value == "0":
            cell = dataclasses.replace(cell, raw_value="1")
        changed_cells.append(cell)
    changed_fixture = {
        **original_fixture,
        "stream": ExactPhysicalCellStream(
            source_sha256=original_fixture["stream"].source_sha256,
            row_count=original_fixture["stream"].row_count,
            cell_iter_factory=lambda: iter(tuple(changed_cells)),
        ),
    }
    changed_result = _execute(changed_fixture)
    changed_release = changed_result.c11_release.release_ref
    assert changed_release != base["case"]["release"]
    assert changed_result.i05_result.receipts[0].typed_state == "DISCOVERED_RESULT_SUPPORTED"

    changed_s2f = publish_empirical_closure(
        NativeEmpiricalOutput.from_route_b_result(changed_result),
        tmp_path / "s2f-changed",
    )
    changed_auth = _m1_authority("s2g-b-changed-native")
    changed_binding = _binding(changed_auth)
    changed_bundle = m1.build_m1_adjudication_input_bundle(
        requested_claim_family_id=base["m1_bundle"].requested_claim_family_id,
        requested_claim_rule_id=base["m1_bundle"].requested_claim_rule_id,
        selected_discovery_receipts=changed_result.i05_result.receipts,
        discovery_authority_catalog=changed_result.object_graph.discovery_authorities,
        empirical_fact_catalog=changed_result.object_graph.empirical_facts,
        empirical_query_catalog=changed_result.object_graph.executed_queries,
        empirical_predicate_catalog=changed_result.object_graph.executed_predicates,
        authority_snapshots=tuple(changed_result.object_graph.authority_snapshots)
        + (changed_auth,),
        requested_scope=base["m1_bundle"].requested_scope,
        prerequisite_channels=(),
        additional_dependency_refs=(changed_release,),
    )
    changed_disposition = m1.adjudicate_learned_empirical(
        changed_bundle, changed_binding, validator_registry=_registry(changed_binding)
    )
    assert changed_disposition.adjudication_outcome == "RULE_SATISFIED"
    assert changed_disposition.ref != base["disposition"].ref

    changed_contract = _contract(
        route="M1_M2_B5",
        binding=None,
        actions=("REGISTER", "PUBLISH", "SELECT_CURRENT"),
        tag="s2g",
        m1_family_rule_binding_ref=changed_binding.ref,
    )
    changed_executor = LearnedProductLifecycleExecutor()
    changed_learned = i4.compose_learned_world(
        changed_contract,
        m2_repository=M2Repository(),
        lifecycle_executor=changed_executor,
        m1_disposition=changed_disposition,
    )
    assert changed_learned.receipt.terminal_state == "RULE_SATISFIED"
    assert changed_learned.m2_artifacts.release.ref != base["learned"].m2_artifacts.release.ref
    assert changed_learned.b5_selection_receipt.ref != base["learned"].b5_selection_receipt.ref

    conditioner = base["consumer"].conditioner_bindings[0]
    changed_conditioner = dataclasses.replace(
        conditioner, release_ref=changed_release
    )
    changed_consumer = dataclasses.replace(
        base["consumer"],
        release_ref=changed_release,
        conditioner_bindings=(changed_conditioner,),
    )
    fact, predicate, query = _validate_discovery_consumption(
        discovery_result=changed_result.i05_result,
        consumer_query=changed_consumer,
        receipt_ref=changed_result.i05_result.receipts[0].ref,
    )
    registry = AuthorityRegistry(
        (*changed_result.object_graph.authority_snapshots, changed_fixture["qauth"])
    )
    changed_witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:s2g:b:changed-witness",
        consumer_query=changed_consumer,
        producer_query=query,
        producer_predicate=predicate,
        bindings=[changed_conditioner],
        coordinate_value_pairs=[(changed_fixture["qrefs"]["X"], 1)],
        pairing_authority=changed_conditioner.comparability_authority_ref,
        source_universe_ref=changed_fixture["projection"].universes[0].ref,
        release_ref=changed_release,
    )
    changed_composition = compose_positioned_subject_possibility(
        repository=None,
        empirical_query=query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(changed_release,),
        consumer_query=changed_consumer,
        model_rule=base["model"],
        condition_binding_witness=changed_witness,
        discovery_result=changed_result.i05_result,
        discovery_receipt_ref=changed_result.i05_result.receipts[0].ref,
    )
    assert changed_composition.analytical_state == "SUPPORTED"
    changed_determinants = LearnedConsumerDeterminants(
        s2f_root_identity=changed_s2f.root_identity,
        discovery_receipt_ref=changed_result.i05_result.receipts[0].ref,
        producer_query_ref=query.ref,
        producer_predicate_ref=predicate.ref,
        release_ref=changed_release,
        consumer_query=changed_consumer,
        model_rule=base["model"],
        condition_binding_witness=changed_witness,
        expected_composition_identity=changed_composition.composed_result_identity_hash,
        expected_consumer_result_hash=(
            changed_composition.consumer_result_or_null.result_hash
        ),
        purpose_ref=changed_contract.consumer_product_purpose_ref,
    )
    changed_published = publish_learned_lifecycle(
        tmp_path / "learned-changed",
        learned=changed_learned,
        executor=changed_executor,
        determinants=changed_determinants,
        m1_input_bundle=changed_bundle.as_dict(),
        m1_family_rule_binding=changed_binding.as_dict(),
    )
    changed_artifact = open_learned_lifecycle(
        changed_published.artifact_path,
        expected_root=changed_published.root_identity,
    ).require_trusted()
    changed_consumed = changed_artifact.consume(changed_s2f.root_path)
    assert changed_consumed.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    return {
        "fixture": changed_fixture,
        "result": changed_result,
        "release": changed_release,
        "s2f": changed_s2f,
        "bundle": changed_bundle,
        "binding": changed_binding,
        "disposition": changed_disposition,
        "learned": changed_learned,
        "determinants": changed_determinants,
        "published": changed_published,
        "artifact": changed_artifact,
        "consumer_hash": changed_consumed.consumer_result_hash,
        "composition_identity": changed_consumed.composition_identity,
    }


def test_b_real_native_fact_change_m1_m2_b5_then_exact_restore(tmp_path):
    base = _artifact_case(tmp_path / "base")
    base_consumer = base["artifact"].consume(base["s2f_receipt"].root_path)
    assert base_consumer.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"

    changed = _changed_native_case(tmp_path, base)
    assert changed["s2f"].root_identity != base["s2f_receipt"].root_identity
    assert changed["disposition"].ref != base["disposition"].ref
    assert changed["learned"].m2_artifacts.release.ref != base["learned"].m2_artifacts.release.ref
    assert changed["learned"].b5_selection_receipt.ref != base["learned"].b5_selection_receipt.ref
    assert changed["composition_identity"] != base_consumer.composition_identity
    assert changed["consumer_hash"] != base_consumer.consumer_result_hash

    restored = publish_learned_lifecycle(
        tmp_path / "base" / "learned",
        learned=base["learned"],
        executor=base["executor"],
        determinants=base["determinants"],
        m1_input_bundle=base["m1_bundle"].as_dict(),
        m1_family_rule_binding=base["binding"].as_dict(),
    )
    assert restored.published is False
    assert restored.root_identity == base["published"].root_identity
    restored_artifact = open_learned_lifecycle(
        restored.artifact_path, expected_root=restored.root_identity
    ).require_trusted()
    restored_consumer = restored_artifact.consume(base["s2f_receipt"].root_path)
    assert restored_consumer.consumer_result_hash == base_consumer.consumer_result_hash
    assert restored_consumer.composition_identity == base_consumer.composition_identity


def _mutant_m1_artifact(tmp_path: Path, base: dict) -> tuple[object, dict]:
    """Publish an internally valid artifact whose M1 fact chain is foreign."""

    receipt = base["receipt"]
    old_ref = ExactRef(**dict(receipt.empirical_fact_refs[0]))
    old_fact = next(
        fact for fact in base["result"].object_graph.empirical_facts
        if fact.ref == old_ref
    )
    mutant_fact = _clone_fact(
        old_fact,
        state="OBSERVED_ZERO",
        numerator=0,
        denominator=old_fact.raw_denominator_support,
        tag="s2g-b-cross-chain",
    )
    mutant_receipt = _receipt_with_fact(
        receipt, old_fact, mutant_fact, tag="s2g-b-cross-chain-receipt"
    )
    mutant_auth = _m1_authority("s2g-b-cross-chain")
    mutant_binding = _binding(mutant_auth)
    facts = tuple(
        mutant_fact if fact.ref == old_fact.ref else fact
        for fact in base["result"].object_graph.empirical_facts
    )
    receipts = tuple(
        mutant_receipt if item.ref == receipt.ref else item
        for item in base["result"].i05_result.receipts
    )
    mutant_bundle = m1.build_m1_adjudication_input_bundle(
        requested_claim_family_id=base["m1_bundle"].requested_claim_family_id,
        requested_claim_rule_id=base["m1_bundle"].requested_claim_rule_id,
        selected_discovery_receipts=receipts,
        discovery_authority_catalog=base["result"].object_graph.discovery_authorities,
        empirical_fact_catalog=facts,
        empirical_query_catalog=base["result"].object_graph.executed_queries,
        empirical_predicate_catalog=base["result"].object_graph.executed_predicates,
        authority_snapshots=tuple(base["m1_bundle"].authority_snapshots) + (mutant_auth,),
        requested_scope=base["m1_bundle"].requested_scope,
        prerequisite_channels=(),
        additional_dependency_refs=base["m1_bundle"].additional_dependency_refs,
    )
    mutant_disposition = m1.adjudicate_learned_empirical(
        mutant_bundle, mutant_binding, validator_registry=_registry(mutant_binding)
    )
    assert mutant_disposition.adjudication_outcome == "RULE_SATISFIED"
    contract = _contract(
        route="M1_M2_B5",
        binding=None,
        actions=("REGISTER", "PUBLISH", "SELECT_CURRENT"),
        tag="s2g",
        m1_family_rule_binding_ref=mutant_binding.ref,
    )
    executor = LearnedProductLifecycleExecutor()
    learned = i4.compose_learned_world(
        contract,
        m2_repository=M2Repository(),
        lifecycle_executor=executor,
        m1_disposition=mutant_disposition,
    )
    assert learned.receipt.terminal_state == "RULE_SATISFIED"
    published = publish_learned_lifecycle(
        tmp_path / "learned-mutant",
        learned=learned,
        executor=executor,
        determinants=base["determinants"],
        m1_input_bundle=mutant_bundle.as_dict(),
        m1_family_rule_binding=mutant_binding.as_dict(),
    )
    artifact = open_learned_lifecycle(
        published.artifact_path, expected_root=published.root_identity
    ).require_trusted()
    return artifact, {
        "bundle": mutant_bundle,
        "binding": mutant_binding,
        "disposition": mutant_disposition,
        "learned": learned,
        "published": published,
    }


def test_b_cross_chain_m1_evidence_is_refused_by_actual_consumer(tmp_path):
    base = _artifact_case(tmp_path / "base")
    mutant, _ = _mutant_m1_artifact(tmp_path, base)
    # The artifact is internally valid and opens under its own external pin.
    assert mutant.trust_state == "EXTERNALLY_PINNED"
    with pytest.raises(DurableLearnedLifecycleError, match="M1 input bundle"):
        mutant.consume(base["s2f_receipt"].root_path)
    # The original chain remains exact.
    assert (
        base["artifact"].consume(base["s2f_receipt"].root_path).consumer_result_hash
        == base["composition"].consumer_result_or_null.result_hash
    )


def test_b_unpinned_and_foreign_asof_checkpoints_refused(tmp_path):
    base = _artifact_case(tmp_path / "base")
    artifact = base["artifact"]
    own = artifact.b5_executor.export_checkpoint()
    own_resolution = artifact.resolve_as_of_checkpoint(
        own, expected_checkpoint_hash=own["checkpoint_hash"]
    )
    assert own_resolution.state == "CURRENT_SELECTED"
    assert own_resolution.selected_release_ref == artifact.m2_artifacts.release.ref

    foreign_disposition, foreign_binding, foreign_auth = _disposition("s2g-b-foreign")
    _, _, foreign_bundle = _bundle(validator_authorities=(foreign_auth,))
    contract = _contract(
        route="M1_M2_B5",
        binding=None,
        actions=("REGISTER", "PUBLISH", "SELECT_CURRENT"),
        tag="s2g",
        m1_family_rule_binding_ref=foreign_binding.ref,
        expected_previous_selection_receipt_ref=artifact.b5_selection_receipt.ref,
    )
    foreign_learned = i4.compose_learned_world(
        contract,
        m2_repository=base["repository"],
        lifecycle_executor=base["executor"],
        m1_disposition=foreign_disposition,
    )
    assert foreign_learned.receipt.terminal_state == "RULE_SATISFIED"
    foreign_checkpoint = base["executor"].export_checkpoint()
    with pytest.raises(DurableLearnedLifecycleUntrusted):
        artifact.resolve_as_of_checkpoint(foreign_checkpoint)
    with pytest.raises(DurableLearnedLifecycleRefusal):
        artifact.resolve_as_of_checkpoint(
            foreign_checkpoint,
            expected_checkpoint_hash=foreign_checkpoint["checkpoint_hash"],
        )


def test_b_tampered_b5_replay_and_receipt_history_refused(tmp_path):
    base = _artifact_case(tmp_path / "base")
    artifact = base["artifact"]
    root = Path(artifact.artifact_path).parent.parent
    path = Path(artifact.artifact_path)

    # Tamper the stored replay receipt's event list but keep a self-consistent
    # artifact root and new external pin.
    core, _ = _load_core(root, path)
    core["b5"]["replay"]["event_refs"] = core["b5"]["replay"]["event_refs"][:-1]
    victim = _copy_artifact(root)
    victim_path = victim / "artifacts" / path.name
    new_root = _rewrite_artifact(victim, victim_path, core)
    with pytest.raises(DurableLearnedLifecycleError):
        open_learned_lifecycle(victim_path, expected_root=new_root)
    shutil.rmtree(victim)

    # Tamper the learned receipt's claimed history; the checkpoint is intact.
    core, _ = _load_core(root, path)
    core["learned_receipt"]["b5_event_refs"] = core["learned_receipt"]["b5_event_refs"][:-1]
    victim = _copy_artifact(root)
    victim_path = victim / "artifacts" / path.name
    new_root = _rewrite_artifact(victim, victim_path, core)
    with pytest.raises(DurableLearnedLifecycleError):
        open_learned_lifecycle(victim_path, expected_root=new_root)
    shutil.rmtree(victim)

    # Tamper the stored B5 protocol view while keeping the M2/B5 objects intact.
    core, _ = _load_core(root, path)
    core["b5"]["protocol_view"]["product_family_ref"] = {
        "kind": "ProductFamily",
        "object_id": "urn:test:s2g:b:forged-family",
        "content_hash": "5" * 64,
    }
    victim = _copy_artifact(root)
    victim_path = victim / "artifacts" / path.name
    new_root = _rewrite_artifact(victim, victim_path, core)
    with pytest.raises(DurableLearnedLifecycleError):
        open_learned_lifecycle(victim_path, expected_root=new_root)
    shutil.rmtree(victim)

    # Tamper the learned receipt's M2 closure provenance; the M2 objects remain
    # the authority and must disagree with the receipt.
    core, _ = _load_core(root, path)
    core["learned_receipt"]["m2_authority_closure_ref"] = {
        "kind": "M2Closure",
        "object_id": "urn:test:s2g:b:forged-closure",
        "content_hash": "6" * 64,
    }
    victim = _copy_artifact(root)
    victim_path = victim / "artifacts" / path.name
    new_root = _rewrite_artifact(victim, victim_path, core)
    with pytest.raises(DurableLearnedLifecycleError):
        open_learned_lifecycle(victim_path, expected_root=new_root)
    shutil.rmtree(victim)

    # The unmodified artifact still opens and serves the exact result.
    restored = open_learned_lifecycle(
        path, expected_root=artifact.root_identity
    ).require_trusted()
    assert restored.consume(base["s2f_receipt"].root_path).state == (
        "LEARNED_CONSUMER_EXACT_SUPPORTED"
    )


def test_b_fresh_process_cold_resource_envelope(tmp_path):
    import os
    import subprocess
    import sys

    base = _artifact_case(tmp_path / "base")
    runner = Path(__file__).with_name("test_pyat960_s2g_fresh_process.py")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2])
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            str(runner),
            str(base["published"].artifact_path),
            base["published"].root_identity,
            str(base["s2f_receipt"].root_path),
            base["composition"].consumer_result_or_null.result_hash,
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout)
    assert observed["state"] == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert observed["matches_expected"] is True
    assert observed["source_opens"] == []
    assert observed["process_tree_peak_rss_bytes"] < 6 * 1024**3
    retained = sum(
        item.stat().st_size
        for item in Path(base["published"].artifact_path).parent.parent.rglob("*")
        if item.is_file()
    )
    assert retained > 0
    assert base["published"].compressed_bytes > 0
    assert base["published"].manifest_bytes > 0
    assert base["published"].peak_scratch_bytes > 0
