"""S2-G mandatory cases: durable M1/M2/B5 custody + actual world consumer.

TEST_ONLY synthetic M1 validator fixtures are used exactly as permitted.  The
adapter never constructs an M1 disposition directly: the native M01 graph is
adjudicated by the existing M1 owner, then M2/B5 use the existing composition
owners.  The cold consumer reruns the existing C1/N10E discovery composition
from the accepted S2-F closure and calls the existing learned/world consumer.
"""
from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import tempfile
import time
import zlib

import pytest

import rawlsing_next.pre553_learned_empirical_adjudication as m1
import rawlsing_next.pre553_learned_world_composition as i4
from rawlsing_next.pre553_analytical_composition import (
    _validate_discovery_consumption,
    compose_positioned_subject_possibility,
)
from rawlsing_next.pre553_durable_empirical_closure import (
    NativeEmpiricalOutput,
    open_empirical_closure,
    publish_empirical_closure,
)
from rawlsing_next.pre553_durable_learned_lifecycle import (
    DURABLE_LEARNED_CONTRACT_SHA,
    DurableLearnedLifecycleError,
    DurableLearnedLifecycleRefusal,
    DurableLearnedLifecycleUntrusted,
    ExternalCurrentAttestation,
    LearnedConsumerDeterminants,
    open_learned_lifecycle,
    publish_learned_lifecycle,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import ExactRef, canonical_json, semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleExecutor
from rawlsing_next.pre553_learned_product_release import M2Repository
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import (
    _binding,
    _bundle,
    _m1_authority,
    _registry,
)
from rawlsing_next.tests.test_pre553_learned_world_composition import (
    _contract,
    _disposition,
)
from rawlsing_next.tests.test_universal_learned_consumer import _build_case


ROOT = Path(__file__).resolve().parents[2]
RUNNER = Path(__file__).with_name("test_pyat960_s2g_fresh_process.py")


def _artifact_case(tmp_path: Path, *, tag: str = "s2g", actions=("REGISTER", "PUBLISH", "SELECT_CURRENT")):
    case = _build_case()
    m01 = case["m01"]
    result = case["m01_result"]
    receipt = result.i05_result.receipts[0]
    consumer = case["consumer_query"]
    model = case["model_rule"]
    release = case["release"]
    universe = m01["projection"].universes[0]
    fact, predicate, query = _validate_discovery_consumption(
        discovery_result=result.i05_result,
        consumer_query=consumer,
        receipt_ref=receipt.ref,
    )
    binding = consumer.conditioner_bindings[0]
    witness = fx.build_witness_for_binding(
        witness_object_id=f"urn:test:s2g:{tag}:witness",
        consumer_query=consumer,
        producer_query=query,
        producer_predicate=predicate,
        bindings=[binding],
        coordinate_value_pairs=[(m01["qrefs"]["X"], 1)],
        pairing_authority=binding.comparability_authority_ref,
        source_universe_ref=universe.ref,
        release_ref=release,
    )
    registry = AuthorityRegistry((*m01["projection"].authority_snapshots, m01["qauth"]))
    composition = compose_positioned_subject_possibility(
        repository=None,
        empirical_query=query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(release,),
        consumer_query=consumer,
        model_rule=model,
        condition_binding_witness=witness,
        discovery_result=result.i05_result,
        discovery_receipt_ref=receipt.ref,
    )
    m1_authority = _m1_authority(f"{tag}-validator")
    binding = _binding(m1_authority)
    _, _m1_result, m1_bundle = _bundle(validator_authorities=(m1_authority,))
    disposition = m1.adjudicate_learned_empirical(
        m1_bundle, binding, validator_registry=_registry(binding)
    )
    assert disposition.adjudication_outcome == "RULE_SATISFIED"
    contract = _contract(
        route="M1_M2_B5",
        binding=None,
        actions=actions,
        tag=tag,
        m1_family_rule_binding_ref=binding.ref,
    )
    executor = LearnedProductLifecycleExecutor()
    repository = M2Repository()
    learned = i4.compose_learned_world(
        contract,
        m2_repository=repository,
        lifecycle_executor=executor,
        m1_disposition=disposition,
    )
    assert learned.receipt.terminal_state == "RULE_SATISFIED"
    s2f_receipt = publish_empirical_closure(
        NativeEmpiricalOutput.from_route_b_result(result), tmp_path / "s2f"
    )
    determinants = LearnedConsumerDeterminants(
        s2f_root_identity=s2f_receipt.root_identity,
        discovery_receipt_ref=receipt.ref,
        producer_query_ref=query.ref,
        producer_predicate_ref=predicate.ref,
        release_ref=release,
        consumer_query=consumer,
        model_rule=model,
        condition_binding_witness=witness,
        expected_composition_identity=composition.composed_result_identity_hash,
        expected_consumer_result_hash=composition.consumer_result_or_null.result_hash,
        purpose_ref=contract.consumer_product_purpose_ref,
    )
    published = publish_learned_lifecycle(
        tmp_path / "learned",
        learned=learned,
        executor=executor,
        determinants=determinants,
        m1_input_bundle=m1_bundle.as_dict(),
        m1_family_rule_binding=binding.as_dict(),
    )
    artifact = open_learned_lifecycle(
        published.artifact_path, expected_root=published.root_identity
    ).require_trusted()
    return {
        "case": case,
        "m01": m01,
        "result": result,
        "receipt": receipt,
        "consumer": consumer,
        "model": model,
        "release": release,
        "query": query,
        "predicate": predicate,
        "composition": composition,
        "learned": learned,
        "disposition": disposition,
        "binding": binding,
        "m1_bundle": m1_bundle,
        "executor": executor,
        "repository": repository,
        "contract": contract,
        "determinants": determinants,
        "s2f_receipt": s2f_receipt,
        "published": published,
        "artifact": artifact,
    }


def _attestation(artifact, *, selection=None, purpose=None, as_of=None, revoked=False, checkpoint_hash=None):
    selection = artifact.b5_selection_receipt if selection is None else selection
    purpose = artifact.determinants.purpose_ref if purpose is None else purpose
    checkpoint_hash = (
        artifact.b5_executor.export_checkpoint()["checkpoint_hash"]
        if checkpoint_hash is None
        else checkpoint_hash
    )
    placeholder = "0" * 64
    temporary = ExternalCurrentAttestation(
        issuer_id="TEST_ONLY_S2G_CURRENT_ISSUER",
        artifact_root=artifact.root_identity,
        selection_key_ref=selection.selection_key_ref,
        selection_receipt_ref=selection.ref,
        checkpoint_hash=checkpoint_hash,
        purpose_ref=purpose,
        as_of_event_ref=as_of,
        revoked=revoked,
        issued_at="2026-11-12T00:00:00Z",
        content_root=placeholder,
    )
    return replace(temporary, content_root=temporary.computed_root)


def _rewrite_artifact(root: Path, artifact_path: Path, core: dict) -> str:
    manifest_path = artifact_path / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    raw = canonical_json(core).encode("utf-8")
    blob_hash = __import__("hashlib").sha256(raw).hexdigest()
    blob_path = root / "blobs" / f"{blob_hash}.json.z"
    blob_path.write_bytes(zlib.compress(raw, 9))
    artifact_identity = semantic_hash(core)
    root_identity = semantic_hash({
        "schema": "PYAT960_S2G_DURABLE_LEARNED_ROOT@1.0.0",
        "artifact_identity": artifact_identity,
        "blob_hash": blob_hash,
    })
    manifest["publication"] = {
        "artifact_identity": artifact_identity,
        "root_identity": root_identity,
        "blob_hash": blob_hash,
        "compressed_bytes": blob_path.stat().st_size,
        "uncompressed_bytes": len(raw),
    }
    manifest_path.write_bytes(canonical_json(manifest).encode("utf-8"))
    return root_identity


def _copy_artifact(root: Path) -> Path:
    destination = Path(tempfile.mkdtemp(prefix="s2g-mutation-"))
    shutil.copytree(root, destination, dirs_exist_ok=True)
    return destination


def _load_core(root: Path, artifact_path: Path) -> tuple[dict, Path]:
    manifest = json.loads((artifact_path / "manifest.json").read_text())
    blob = root / "blobs" / f"{manifest['publication']['blob_hash']}.json.z"
    return json.loads(zlib.decompress(blob.read_bytes()).decode("utf-8")), (
        root / "artifacts" / artifact_path.name
    )


# ---------------------------------------------------------------------------
# G01 real M1/M2/B5 world first reader
# ---------------------------------------------------------------------------


def test_g01_real_m1_m2_b5_first_reader(tmp_path):
    item = _artifact_case(tmp_path)
    artifact = item["artifact"]
    learned = item["learned"]
    assert artifact.m1_disposition.ref == learned.m1_disposition.ref
    assert artifact.m2_artifacts.release.ref == learned.m2_artifacts.release.ref
    assert artifact.b5_selection_receipt.ref == learned.b5_selection_receipt.ref
    assert artifact.learned_receipt.ref == learned.receipt.ref
    consumed = artifact.consume(item["s2f_receipt"].root_path)
    assert consumed.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert consumed.reason_code == "PRODUCTIVE_LEARNED_PRODUCT_WITH_ACTUAL_EMPIRICAL_EVIDENCE"
    assert consumed.consumer_result_hash == item["composition"].consumer_result_or_null.result_hash
    assert consumed.m1_disposition_ref == learned.m1_disposition.ref
    assert consumed.m2_release_ref == learned.m2_artifacts.release.ref
    assert consumed.b5_selection_receipt_ref == learned.b5_selection_receipt.ref
    assert artifact.trust_state == "EXTERNALLY_PINNED"
    assert artifact.core["evidence_grade"] == "S2_SOURCEFREE_ISOLATED_FIXTURE"
    assert artifact.core["contract_sha"] == DURABLE_LEARNED_CONTRACT_SHA
    s2f = open_empirical_closure(
        item["s2f_receipt"].root_path, expected_root=item["s2f_receipt"].root_identity
    ).require_trusted()
    s2f_fact_keys = {fact.ref.key for fact in s2f.object_graph.empirical_facts}
    s2f_receipt_keys = {receipt.ref.key for receipt in s2f.object_graph.discovery_receipts}
    assert {fact.ref.key for fact in item["m1_bundle"].empirical_facts}.issubset(s2f_fact_keys)
    assert {receipt.ref.key for receipt in item["m1_bundle"].discovery_receipts}.issubset(s2f_receipt_keys)


# ---------------------------------------------------------------------------
# G02 fresh process, changed input + exact restoration
# ---------------------------------------------------------------------------


def test_g02b_fresh_process_cold_learner(tmp_path):
    item = _artifact_case(tmp_path)
    expected = item["composition"].consumer_result_or_null.result_hash
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            str(item["published"].artifact_path),
            item["published"].root_identity,
            str(item["s2f_receipt"].root_path),
            expected,
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
    assert observed["consumer_result_hash"] == expected
    assert observed["source_opens"] == []
    assert observed["matches_expected"] is True


def test_g02_changed_input_and_exact_restoration(tmp_path):
    item = _artifact_case(tmp_path)
    original = item["published"]
    assert original.published is True
    # Changed M1 input: a different actual M1 adjudication/fact fixture, same
    # product family/scope and selection purpose.
    changed_disposition, changed_binding, changed_auth = _disposition("s2g-changed")
    _, _, changed_bundle = _bundle(validator_authorities=(changed_auth,))
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
    changed = publish_learned_lifecycle(
        tmp_path / "learned",
        learned=changed_learned,
        executor=changed_executor,
        determinants=item["determinants"],
        m1_input_bundle=changed_bundle.as_dict(),
        m1_family_rule_binding=changed_binding.as_dict(),
    )
    assert changed.root_identity != original.root_identity
    changed_artifact = open_learned_lifecycle(
        changed.artifact_path, expected_root=changed.root_identity
    ).require_trusted()
    assert changed_artifact.consume(item["s2f_receipt"].root_path).state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    # Restoring the original learned product reproduces the exact root.
    restored = publish_learned_lifecycle(
        tmp_path / "learned",
        learned=item["learned"],
        executor=item["executor"],
        determinants=item["determinants"],
        m1_input_bundle=item["m1_bundle"].as_dict(),
        m1_family_rule_binding=item["binding"].as_dict(),
    )
    assert restored.published is False
    assert restored.root_identity == original.root_identity
    restored_artifact = open_learned_lifecycle(
        restored.artifact_path, expected_root=restored.root_identity
    ).require_trusted()
    assert restored_artifact.consume(item["s2f_receipt"].root_path).consumer_result_hash == item[
        "composition"
    ].consumer_result_or_null.result_hash


# ---------------------------------------------------------------------------
# G03 current/as-of/supersession/no-current
# ---------------------------------------------------------------------------


def test_g03_current_asof_supersession_and_no_current(tmp_path):
    item = _artifact_case(tmp_path)
    artifact = item["artifact"]
    selection = artifact.b5_selection_receipt
    attestation = _attestation(artifact, as_of=selection.current_select_event_ref)
    current = artifact.resolve_current(
        attestation, expected_attestation_root=attestation.content_root
    )
    assert current.state == "CURRENT_SELECTED"
    assert current.selected_release_ref == artifact.m2_artifacts.release.ref
    asof = artifact.resolve_as_of(selection.current_select_event_ref)
    assert asof.state == "CURRENT_SELECTED"
    assert asof.selected_release_ref == artifact.m2_artifacts.release.ref

    # No-current artifact: publication without SELECT_CURRENT preserves absence.
    no_current = _artifact_case(tmp_path / "no-current", tag="s2g-no-current", actions=("REGISTER", "PUBLISH"))
    no_current_artifact = no_current["artifact"]
    assert no_current_artifact.b5_selection_receipt is None
    refused = no_current_artifact.consume(
        no_current["s2f_receipt"].root_path, require_current_selection=True
    )
    assert refused.state == "REFUSED"
    assert refused.reason_code == "LEARNED_CURRENT_SELECTION_ABSENT"
    supported = no_current_artifact.consume(
        no_current["s2f_receipt"].root_path, require_current_selection=False
    )
    assert supported.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    with pytest.raises(DurableLearnedLifecycleRefusal):
        no_current_artifact.resolve_as_of(
            ExactRef("NO_CURRENT_EVENT", "urn:test:s2g:no-current", semantic_hash({"no": "current"}))
        )


def test_g03b_supersession_and_asof_history(tmp_path):
    item = _artifact_case(tmp_path)
    first_artifact = item["artifact"]
    first_selection = first_artifact.b5_selection_receipt
    first_checkpoint = item["executor"].export_checkpoint()
    changed_disposition, changed_binding, changed_auth = _disposition("s2g-super")
    _, _, changed_bundle = _bundle(validator_authorities=(changed_auth,))
    contract = _contract(
        route="M1_M2_B5",
        binding=None,
        actions=("REGISTER", "PUBLISH", "SELECT_CURRENT"),
        tag="s2g",
        m1_family_rule_binding_ref=changed_binding.ref,
        expected_previous_selection_receipt_ref=first_selection.ref,
    )
    changed_learned = i4.compose_learned_world(
        contract,
        m2_repository=item["repository"],
        lifecycle_executor=item["executor"],
        m1_disposition=changed_disposition,
    )
    assert changed_learned.receipt.terminal_state == "RULE_SATISFIED"
    second = publish_learned_lifecycle(
        tmp_path / "learned",
        learned=changed_learned,
        executor=item["executor"],
        determinants=item["determinants"],
        m1_input_bundle=changed_bundle.as_dict(),
        m1_family_rule_binding=changed_binding.as_dict(),
    )
    second_artifact = open_learned_lifecycle(
        second.artifact_path, expected_root=second.root_identity
    ).require_trusted()
    second_selection = second_artifact.b5_selection_receipt
    assert second_selection is not None
    assert second_selection.ref != first_selection.ref
    historical_event = ExactRef(
        **second_artifact.core["b5"]["checkpoint"]["checkpoint_payload"]["events"][0]["record_ref"]
    )
    historical = second_artifact.resolve_as_of(historical_event)
    assert historical.state == "UNKNOWN_CURRENTNESS"
    first_asof = second_artifact.resolve_as_of(first_selection.current_select_event_ref)
    assert first_asof.state == "CURRENT_SELECTED"
    assert first_asof.selected_release_ref == first_artifact.m2_artifacts.release.ref
    second_asof = second_artifact.resolve_as_of(second_selection.current_select_event_ref)
    assert second_asof.state == "CURRENT_SELECTED"
    assert second_asof.selected_release_ref == second_artifact.m2_artifacts.release.ref
    checkpoint_asof = second_artifact.resolve_as_of_checkpoint(
        first_checkpoint,
        expected_checkpoint_hash=first_checkpoint["checkpoint_hash"],
    )
    assert checkpoint_asof.state == "CURRENT_SELECTED"
    assert checkpoint_asof.selected_release_ref == first_artifact.m2_artifacts.release.ref
    attestation = _attestation(
        second_artifact,
        selection=second_selection,
        as_of=second_selection.current_select_event_ref,
    )
    current = second_artifact.resolve_current(
        attestation, expected_attestation_root=attestation.content_root
    )
    assert current.selected_release_ref == second_artifact.m2_artifacts.release.ref


# ---------------------------------------------------------------------------
# G04 independent test-only issuer: revoked/stale/wrong purpose
# ---------------------------------------------------------------------------


def test_g04_independent_issuer_refusals(tmp_path):
    item = _artifact_case(tmp_path)
    artifact = item["artifact"]
    good = _attestation(artifact)
    assert artifact.resolve_current(
        good, expected_attestation_root=good.content_root
    ).state == "CURRENT_SELECTED"
    current_view, current_consumer = artifact.consume_current(
        item["s2f_receipt"].root_path,
        attestation=good,
        expected_attestation_root=good.content_root,
    )
    assert current_view.state == "CURRENT_SELECTED"
    assert current_consumer.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    with pytest.raises(DurableLearnedLifecycleUntrusted):
        artifact.resolve_current(good, expected_attestation_root=None)
    with pytest.raises(DurableLearnedLifecycleRefusal):
        artifact.resolve_current(
            _attestation(artifact, revoked=True),
            expected_attestation_root=_attestation(artifact, revoked=True).content_root,
        )
    wrong_purpose_ref = ExactRef(
        "TEST_ONLY_WRONG_PURPOSE",
        "urn:test:s2g:wrong-purpose",
        semantic_hash({"purpose": "wrong"}),
    )
    wrong_purpose = _attestation(artifact, purpose=wrong_purpose_ref)
    with pytest.raises(DurableLearnedLifecycleRefusal):
        artifact.resolve_current(
            wrong_purpose, expected_attestation_root=wrong_purpose.content_root
        )
    stale = _attestation(artifact, checkpoint_hash="0" * 64)
    with pytest.raises(DurableLearnedLifecycleRefusal):
        artifact.resolve_current(stale, expected_attestation_root=stale.content_root)
    wrong_root = _attestation(artifact)
    with pytest.raises(DurableLearnedLifecycleError):
        artifact.resolve_current(
            wrong_root, expected_attestation_root="1" * 64
        )
    historical_event = ExactRef(
        **artifact.core["b5"]["checkpoint"]["checkpoint_payload"]["events"][0]["record_ref"]
    )
    stale_asof = _attestation(artifact, as_of=historical_event)
    with pytest.raises(DurableLearnedLifecycleRefusal):
        artifact.resolve_current(
            stale_asof, expected_attestation_root=stale_asof.content_root
        )
    wrong_selection = replace(
        good,
        selection_receipt_ref=ExactRef(
            "CURRENT_SELECTION",
            "urn:test:s2g:wrong-selection",
            semantic_hash({"wrong": "selection"}),
        ),
    )
    wrong_selection = replace(
        wrong_selection, content_root=wrong_selection.computed_root
    )
    with pytest.raises(DurableLearnedLifecycleRefusal):
        artifact.resolve_current(
            wrong_selection,
            expected_attestation_root=wrong_selection.content_root,
        )
    wrong_key = replace(
        good,
        selection_key_ref=ExactRef(
            "SelectionKey",
            "urn:test:s2g:wrong-key",
            semantic_hash({"wrong": "key"}),
        ),
    )
    wrong_key = replace(wrong_key, content_root=wrong_key.computed_root)
    with pytest.raises(DurableLearnedLifecycleRefusal):
        artifact.resolve_current(
            wrong_key, expected_attestation_root=wrong_key.content_root
        )
    assert not hasattr(artifact, "resolve_latest")
    assert not hasattr(artifact, "resolve_default")


# ---------------------------------------------------------------------------
# G05 forged checkpoint / wrong root / wrong as-of
# ---------------------------------------------------------------------------


def test_g04b_fresh_process_current_attestation(tmp_path):
    item = _artifact_case(tmp_path)
    attestation = _attestation(item["artifact"])
    attestation_path = tmp_path / "current_attestation.json"
    attestation_path.write_text(
        json.dumps(
            {**attestation.material(), "content_root": attestation.content_root},
            sort_keys=True,
        )
    )
    expected = item["composition"].consumer_result_or_null.result_hash
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            str(item["published"].artifact_path),
            item["published"].root_identity,
            str(item["s2f_receipt"].root_path),
            expected,
            str(attestation_path),
            attestation.content_root,
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
    observed = json.loads(completed.stdout)
    assert observed["current_state"] == "CURRENT_SELECTED"
    assert observed["state"] == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert observed["consumer_result_hash"] == expected
    assert observed["source_opens"] == []


def test_g05_self_rehashed_fake_checkpoint_and_wrong_asof(tmp_path):
    item = _artifact_case(tmp_path)
    artifact = item["artifact"]
    root = Path(artifact.artifact_path).parent.parent
    victim = _copy_artifact(root)
    path = victim / "artifacts" / Path(artifact.artifact_path).name
    core, path = _load_core(victim, path)
    core["b5"]["checkpoint"]["checkpoint_payload"]["events"] = []
    core["b5"]["checkpoint"]["checkpoint_hash"] = semantic_hash(
        core["b5"]["checkpoint"]["checkpoint_payload"]
    )
    new_root = _rewrite_artifact(victim, path, core)
    with pytest.raises(DurableLearnedLifecycleError):
        open_learned_lifecycle(path, expected_root=new_root)
    with pytest.raises(DurableLearnedLifecycleError):
        open_learned_lifecycle(path, expected_root=artifact.root_identity)
    with pytest.raises(DurableLearnedLifecycleRefusal):
        artifact.resolve_as_of(
            ExactRef("WRONG_ASOF", "urn:test:s2g:asof", "2" * 64)
        )
    shutil.rmtree(victim)


# ---------------------------------------------------------------------------
# G06 missing family rule/receipt/history/changed M2 dependency
# ---------------------------------------------------------------------------


def test_g06_missing_rule_receipt_history_and_changed_m2_dependency(tmp_path):
    item = _artifact_case(tmp_path)
    artifact = item["artifact"]
    root = Path(artifact.artifact_path).parent.parent
    path = Path(artifact.artifact_path)
    core, _ = _load_core(root, path)
    variants = []
    missing_rule = json.loads(json.dumps(core))
    missing_rule["m1"]["determinant_receipt"] = None
    variants.append(missing_rule)
    missing_binding = json.loads(json.dumps(core))
    missing_binding["m1"]["disposition"]["semantic_fields"][
        "family_rule_binding_ref"
    ] = {"typed_absence_state": "NOT_APPLICABLE", "detail": "removed rule binding"}
    variants.append(missing_binding)
    missing_history = json.loads(json.dumps(core))
    missing_history["b5"]["checkpoint"]["checkpoint_payload"]["events"].pop()
    missing_history["b5"]["checkpoint"]["checkpoint_hash"] = semantic_hash(
        missing_history["b5"]["checkpoint"]["checkpoint_payload"]
    )
    variants.append(missing_history)
    changed_m2 = json.loads(json.dumps(core))
    changed_m2["m2"]["release"]["dependency_closure_ref"] = ExactRef(
        "M2Closure", "urn:test:s2g:forged-dependency", "3" * 64
    ).as_dict()
    variants.append(changed_m2)
    for variant in variants:
        victim = _copy_artifact(root)
        victim_path = victim / "artifacts" / path.name
        new_root = _rewrite_artifact(victim, victim_path, variant)
        with pytest.raises(DurableLearnedLifecycleError):
            open_learned_lifecycle(victim_path, expected_root=new_root)
        shutil.rmtree(victim)


# ---------------------------------------------------------------------------
# G07 crash between publish and current pointer
# ---------------------------------------------------------------------------


def test_g07_publish_pointer_crash_and_recovery(tmp_path):
    item = _artifact_case(tmp_path)
    artifact = item["artifact"]
    # The artifact exists but no external pointer has been issued.
    with pytest.raises(DurableLearnedLifecycleUntrusted):
        artifact.resolve_current(_attestation(artifact), expected_attestation_root=None)
    # A valid independent attestation restores current.
    attestation = _attestation(artifact)
    assert artifact.resolve_current(
        attestation, expected_attestation_root=attestation.content_root
    ).state == "CURRENT_SELECTED"
    # Crash during artifact publication leaves no visible artifact/manifest.
    crash_root = tmp_path / "crash"
    def _fail(name):
        if name == "before_manifest_replace":
            raise RuntimeError("injected crash before manifest")
    with pytest.raises(RuntimeError):
        publish_learned_lifecycle(
            crash_root,
            learned=item["learned"],
            executor=item["executor"],
            determinants=item["determinants"],
            m1_input_bundle=item["m1_bundle"].as_dict(),
            m1_family_rule_binding=item["binding"].as_dict(),
            failpoint=_fail,
        )
    assert not list((crash_root / "artifacts").glob("artifact-*"))


# ---------------------------------------------------------------------------
# G08 native lifecycle regression / exact native objects
# ---------------------------------------------------------------------------


def test_g08_native_lifecycle_objects_unchanged(tmp_path):
    item = _artifact_case(tmp_path)
    assert item["learned"].receipt.terminal_state == "RULE_SATISFIED"
    assert item["learned"].b5_selection_receipt is not None
    assert item["learned"].b5_replay_receipt is not None
    assert item["learned"].b5_replay_receipt.replay_state == "REPLAY_VERIFIED"
    assert item["artifact"].m2_repository.release_exact(
        item["artifact"].m2_artifacts.release.ref
    ).ref == item["learned"].m2_artifacts.release.ref
    assert item["artifact"].b5_executor.export_checkpoint()["checkpoint_hash"] == item[
        "artifact"
    ].b5_executor.export_checkpoint()["checkpoint_hash"]


# ---------------------------------------------------------------------------
# G09 resources / source opens
# ---------------------------------------------------------------------------


def test_g09_resources_and_source_opens(tmp_path):
    item = _artifact_case(tmp_path)
    artifact = item["artifact"]
    root = Path(artifact.artifact_path).parent.parent
    retained = sum(path.stat().st_size for path in root.rglob("*") if path.is_file())
    opens = []

    def _audit(event, args):
        if event == "open" and args:
            text = str(args[0]).lower()
            if text.endswith((".sav", ".dta", ".parquet", ".csv", ".rdata", ".rds")):
                opens.append(text)

    sys.addaudithook(_audit)
    started = time.monotonic()
    consumed = artifact.consume(item["s2f_receipt"].root_path)
    elapsed = time.monotonic() - started
    repeat_started = time.monotonic()
    again = artifact.consume(item["s2f_receipt"].root_path)
    repeat = time.monotonic() - repeat_started
    assert consumed.state == again.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert opens == []
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_bytes = int(rss) if sys.platform == "darwin" else int(rss) * 1024
    assert rss_bytes < 6 * 1024**3
    evidence = {
        "artifact_root_identity": artifact.root_identity,
        "retained_disk_bytes": retained,
        "compressed_blob_bytes": item["published"].compressed_bytes,
        "logical_bytes": item["published"].logical_bytes,
        "cold_seconds": elapsed,
        "repeat_seconds": repeat,
        "process_tree_peak_rss_bytes": rss_bytes,
        "source_opens": len(opens),
        "rows": item["published"].object_counts,
        "cap_bytes": 6 * 1024**3,
        "cap_result": "PASS",
        "integrated_100k": "NOT_RUN",
    }
    (tmp_path / "s2g_resource_evidence.json").write_text(json.dumps(evidence, sort_keys=True))
    assert json.loads((tmp_path / "s2g_resource_evidence.json").read_text())["source_opens"] == 0
