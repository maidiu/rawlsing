"""Successor focused recheck for the two repaired SRC04 carrier defects.

Review-owned; labelled nonrespondent fixture only.  The prior actual_review
RED files are imported read-only for their bundle helper and are not edited.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import pickle
import tempfile

import pytest

from campaign_src04_completion.consumers.consumer import _plain
from campaign_src04_completion.empirical.actual_carrier import ActualCarrierRefusal
from campaign_src04_completion.empirical.authorized_execution import (
    AuthorizedExecutionRefusal,
    _topology_valid_targets,
    authenticate_fixture_grant,
    authenticate_grant,
    execute_issued,
    issue_authorized_execution,
    issue_fixture_execution,
)
from campaign_src04_completion.empirical.consumer_bridge import consume_with_lane_d
from campaign_src04_completion.empirical.native_workload import WorkloadPolicy
from campaign_src04_completion.empirical.actual_review import test_actual_carrier_review as prior
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.source_configuration.factory import build_validated_c11_release_from_config
from rawlsing_next.source_configuration.fixture import load_fixture_stream
from rawlsing_next.source_configuration.schema import load_source_config
from rawlsing_next.tests.test_observed_response import _Context

ROOT = Path(__file__).resolve().parents[3]
FIXTURE_CONFIG = ROOT / "source_pre553_validation/SRC04/fixture.config.json"
FIXTURE = ROOT / "source_pre553_validation/SRC04/fixture.json"
GRANT_PATH = ROOT / "campaign_src04_completion/empirical/USER_EMPIRICAL_GRANT.json"
FIXTURE_GRANT_PATH = ROOT / "campaign_src04_completion/empirical/FIXTURE_EMPIRICAL_GRANT.json"
SCOPE_PATH = ROOT / "campaign_src04_completion/empirical/SCOPE_LEDGER_V2.json"


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _fixture_release():
    config = load_source_config(FIXTURE_CONFIG)
    stream = load_fixture_stream(FIXTURE)
    return build_validated_c11_release_from_config(config, stream=stream), stream


def _bundle(tmp_path: Path, release, stream):
    local, release_receipt, primary, public, internal = prior._write_bundle(
        tmp_path, release, stream.source_sha256
    )
    # The actual receipt carries the source artifact shape; the prior review
    # helper omitted it, so bind it here for the fixture issuer path.
    document = json.loads(local.read_text(encoding="utf-8"))
    document["source_artifact_ref"] = release.source_artifact_ref.as_dict()
    local.write_text(json.dumps(document), encoding="utf-8")
    return local, release_receipt, primary, public, internal


def _reopen(tmp_path: Path, release, stream):
    local, release_receipt, primary, _, _ = _bundle(tmp_path, release, stream)
    return prior._load(
        local, release_receipt, primary, tmp_path,
        expected_source_sha256=stream.source_sha256,
        local_receipt_sha256=_sha(local),
        release_receipt_sha256=_sha(release_receipt),
        primary_run_sha256=_sha(primary),
    ), local, release_receipt, primary


def test_fixture_adapter_issuer_executor_and_lane_d_exact(tmp_path):
    release, stream = _fixture_release()
    reopened, _, _, _ = _reopen(tmp_path, release, stream)
    context = _Context()
    fixture_grant = authenticate_fixture_grant(FIXTURE_GRANT_PATH)
    policy = WorkloadPolicy.from_mapping(
        json.loads(SCOPE_PATH.read_text(encoding="utf-8"))["workload_policy"]
    )
    issued = issue_fixture_execution(
        fixture_grant=fixture_grant,
        release=reopened,
        pending_contract=context.contract,
        policy=policy,
    )
    workload = execute_issued(issued)
    bridge = consume_with_lane_d(
        grant=fixture_grant, issued=issued, workload=workload
    )
    product = bridge.product

    assert issued.fixture_only is True
    assert issued.contract.authority_grade == "NONRESPONDENT_FIXTURE_ONLY"
    assert issued.contract.source_sha256 == stream.source_sha256
    assert workload.accounting["operations_total"] == 44
    assert workload.accounting["executed_operations"] == 44
    assert workload.accounting["refused_operations"] == 0
    assert workload.accounting["operations_by_family"] == {
        "UNARY_OBSERVED_DISTRIBUTION": 3,
        "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION": 38,
        "SAME_RESPONDENT_JOINT_DISTRIBUTION": 3,
    }
    unary = [
        op for op in workload.operations
        if op.family == "UNARY_OBSERVED_DISTRIBUTION"
    ]
    assert len(unary) == 3
    assert all(
        op.fact_state == "SUPPORTED"
        and (op.raw_numerator, op.raw_denominator) == (7, 7)
        and op.observed_ledger["denominator_policy"] == "PER_TARGET_OBSERVED"
        and op.observed_ledger["not_eligible_population_estimate"] is True
        and op.observed_ledger["scoped_respondents"] == 8
        and op.observed_ledger["target_observed"] == 7
        and op.observed_ledger["target_unobserved"] == 1
        for op in unary
    )

    joint = [
        op for op in workload.operations
        if op.family == "SAME_RESPONDENT_JOINT_DISTRIBUTION"
    ]
    assert len(joint) == 3
    assert sorted(op.raw_denominator for op in joint) == [6, 6, 7]
    assert all(
        op.fact_state == "SUPPORTED"
        and op.observed_ledger["denominator_policy"] == "CO_OBSERVED_TARGETS"
        and op.observed_ledger["not_eligible_population_estimate"] is True
        for op in joint
    )

    conditional = [
        op for op in workload.operations
        if op.family == "BIDIRECTIONAL_CONDITIONAL_DISTRIBUTION"
    ]
    assert len(conditional) == 38
    directions = {
        (op.target_refs[0].object_id, op.condition_ref.object_id)
        for op in conditional
    }
    assert len(directions) == 6
    targets = sorted({op.target_refs[0].object_id for op in conditional})
    assert len(targets) == 3
    for i, left in enumerate(targets):
        for right in targets[i + 1:]:
            assert (left, right) in directions
            assert (right, left) in directions
    assert all(
        op.condition_counts is not None
        and op.observed_ledger is not None
        and op.observed_ledger["condition_unobserved"]
        == op.condition_counts["condition_unobserved"]
        and op.observed_ledger["condition_false"]
        == op.condition_counts["condition_false"]
        and op.observed_ledger["denominator_policy"] == "PER_TARGET_OBSERVED"
        for op in conditional
    )

    assert product["status"] == "FIXTURE_ONLY_NATIVE_ENGINEERING_POSITIVE"
    assert product["fixture_only"] is True
    assert product["source_local_claim"] is False
    assert product["downstream_value_effect"] == "SUBSTANTIVE_DISCOVERY_RESULT_SUPPORTED"
    assert product["observed_response"]["status"] == "OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION"
    assert product["observed_response"]["not_eligible_population_estimate"] is True
    assert product["observed_response"]["ledger"]["denominator_policy"] == "PER_TARGET_OBSERVED"
    assert product["downstream_discovery"]["empirical_facts"]
    assert all(
        item["observed_response"]["status"] == "OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION"
        and item["observed_response"]["not_eligible_population_estimate"] is True
        and item["observed_response"]["ledger"]["not_eligible_population_estimate"] is True
        for item in product["downstream_discovery"]["empirical_facts"]
    )

    base = next(op for op in unary if op.fact_ref.as_dict() == product["fact_ref"])
    source_result = execute_empirical_query(
        repository=issued.repository,
        query=base.query,
        predicate=base.predicate,
        authority_registry=issued.registry,
        release_refs=(issued.release.release_ref,),
    )
    source_fact = source_result.facts[0]
    assert product["observed_response"] == _plain(
        source_fact.target_topology["observed_response"]
    )


def test_fixture_mode_does_not_bypass_original_or_fixture_authority_gates(tmp_path):
    release, stream = _fixture_release()
    reopened, _, _, _ = _reopen(tmp_path, release, stream)
    context = _Context()
    fixture_grant = authenticate_fixture_grant(FIXTURE_GRANT_PATH)
    original_grant = authenticate_grant(GRANT_PATH)
    policy = WorkloadPolicy.from_mapping(
        json.loads(SCOPE_PATH.read_text(encoding="utf-8"))["workload_policy"]
    )
    with pytest.raises(AuthorizedExecutionRefusal) as exc:
        issue_fixture_execution(
            fixture_grant=original_grant,
            release=reopened,
            pending_contract=context.contract,
            policy=policy,
        )
    assert exc.value.code == "FIXTURE_GRANT_REQUIRED"
    with pytest.raises(AuthorizedExecutionRefusal) as exc:
        issue_authorized_execution(
            grant=original_grant,
            release=reopened,
            pending_contract=context.contract,
            policy=policy,
        )
    assert exc.value.code == "RELEASE_SOURCE_IDENTITY_MISMATCH"
    with pytest.raises(AuthorizedExecutionRefusal) as exc:
        issue_authorized_execution(
            grant=fixture_grant,
            release=reopened,
            pending_contract=context.contract,
            policy=policy,
            fixture_mode=False,
        )
    assert exc.value.code == "NO_SOURCE_QUALIFIED_TARGETS"
    with pytest.raises(AuthorizedExecutionRefusal) as exc:
        authenticate_fixture_grant(FIXTURE_GRANT_PATH, "0" * 64)
    assert exc.value.code == "FIXTURE_GRANT_SHA256_MISMATCH"


def test_carrier_malformed_truncated_missing_are_typed(tmp_path):
    release, stream = _fixture_release()
    local, release_receipt, primary, public, _ = _bundle(tmp_path, release, stream)
    with pytest.raises(ActualCarrierRefusal) as exc:
        prior._load(
            tmp_path / "missing_receipt.json",
            release_receipt,
            primary,
            tmp_path,
            expected_source_sha256=stream.source_sha256,
            local_receipt_sha256="0" * 64,
        )
    assert exc.value.code == "CARRIER_FILE_UNREADABLE"

    for name, payload in (
        ("malformed.pkl", b"not-a-pickle"),
        ("truncated.pkl", public.read_bytes()[:8]),
    ):
        bad = tmp_path / name
        bad.write_bytes(payload)
        document = json.loads(local.read_text(encoding="utf-8"))
        document["public_objects"].update({
            "file": bad.name,
            "lines": 1,
            "bytes": bad.stat().st_size,
            "sha256": _sha(bad),
        })
        local.write_text(json.dumps(document), encoding="utf-8")
        with pytest.raises(ActualCarrierRefusal) as exc:
            prior._load(
                local, release_receipt, primary, tmp_path,
                expected_source_sha256=stream.source_sha256,
            )
        assert exc.value.code in {
            "CARRIER_STREAM_UNREADABLE",
            "CARRIER_STREAM_FILE_UNREADABLE",
        }

    local, release_receipt, primary, public, _ = _bundle(tmp_path, release, stream)
    with pytest.raises(ActualCarrierRefusal) as exc:
        prior._load(
            local, release_receipt, primary, tmp_path,
            expected_source_sha256=stream.source_sha256,
            local_receipt_sha256="0" * 64,
        )
    assert exc.value.code == "LOCAL_RECEIPT_SHA256_MISMATCH"
    with pytest.raises(ActualCarrierRefusal) as exc:
        prior._load(
            local, release_receipt, primary, tmp_path,
            expected_source_sha256="2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18",
        )
    assert exc.value.code == "LOCAL_SOURCE_MISMATCH"


def test_fixture_topology_validation_rejects_wrong_event_binding():
    release, _ = _fixture_release()
    context = _Context()
    bad_binding = replace(
        context.contract.topology_bindings[0],
        source_native_topology_ref=ExactRef(
            "RESPONSE_TOPOLOGY", "urn:review:wrong-topology", "f" * 64
        ),
    )
    bad_contract = replace(
        context.contract,
        topology_bindings=(
            bad_binding,
            *context.contract.topology_bindings[1:],
        ),
    )
    valid, held, _ = _topology_valid_targets(
        release,
        bad_contract,
        allow_fixture_canonical=True,
        extend_release_targets=False,
    )
    assert len(valid) == 2
    assert any(item.get("code") == "TOPOLOGY_REF_MISMATCH" for item in held)


def test_frozen_prior_red_artifact_is_preserved():
    assert _sha(Path(prior.__file__)) == (
        "97278b24a8378674c7312b4d4f66972eedd18bb9ecec749ade797fdade69de67"
    )
    assert _sha(ROOT / "campaign_src04_completion/empirical/actual_review/REVIEW.json") == (
        "a9e8bd8756e81f05001249322b96dfeec0cb6e0b9abfbd70597e0c01bba53ce0"
    )
    assert _sha(ROOT / "campaign_src04_completion/empirical/actual_review/MEASUREMENTS.json") == (
        "85af81c7ce6de31f474a9d409edc058d5ff33cb9a3b7d2d9159307712b9e8c4a"
    )
    assert _sha(ROOT / "campaign_src04_completion/empirical/actual_review/TEST_RUN.txt") == (
        "9314078b109ec98a1e2a10e1323b928acacf6a1de85e77f6dcd220f8b47429a4"
    )
