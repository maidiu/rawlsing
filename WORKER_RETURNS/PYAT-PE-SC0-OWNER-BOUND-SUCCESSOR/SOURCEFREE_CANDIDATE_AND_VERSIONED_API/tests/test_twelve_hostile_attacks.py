from __future__ import annotations

import copy
import os
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.tests.n10e_empirical_slice_fixture import build_provider_case

from fixtures import build_success_fixture
from n10e_adapter import N10EProducer
from owner_bound_successor import (
    ExactIssuerRegistry,
    OwnerBoundRefusal,
    OwnerBoundReplayError,
    RECEIPT_SCHEMA,
    ROLE_FORWARD,
    ROLE_REVERSE,
    serve,
    verify_replay,
    verify_result_integrity,
)
from sourcefree_world import SourceFreeWorldProvider, make_test_grant

CANDIDATE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]


def _serve(fixture):
    return serve(
        producer=fixture["producer"],
        world_provider=fixture["world_provider"],
        issuer_registry=fixture["issuer_registry"],
        consumer=fixture["consumer"],
        request=fixture["request"],
    )


def _assert_refusal(result, state):
    assert result.result_state == "TYPED_REFUSAL"
    assert result.refusal_state == state
    assert result.receipt is None


def _provider_from_base(base, **changes):
    provider = base["world_provider"]
    kwargs = {
        "world_owner": provider.world_owner,
        "revision": provider.revision,
        "risk_set_ref": provider.risk_set_ref,
        "routing_ref": provider.routing_ref,
        "values": copy.deepcopy(provider.values),
        "clocks": copy.deepcopy(provider.clocks),
        "negative_status_rows": tuple(
            copy.deepcopy(row) for row in provider.negative_status_rows
        ),
        "generated_binding_echo": copy.deepcopy(provider.generated_binding_echo),
        "native_sampling_unit": provider.native_sampling_unit,
        "values_read_receipt": copy.deepcopy(provider.values_read_receipt),
        "grade": provider.grade,
    }
    kwargs.update(changes)
    return SourceFreeWorldProvider(**kwargs)


def _bundle_with_provider(base, provider, **request_changes):
    request = replace(
        base["request"],
        selected_world_owner=provider.world_owner,
        selected_world_digest=provider.selection_digest,
        world_revision=provider.revision,
        **request_changes,
    )
    return {**base, "world_provider": provider, "request": request}


class _TamperedWorldProvider:
    def __init__(self, base, snapshot):
        self.base = base
        self._snapshot = snapshot

    def snapshot(self):
        return self._snapshot

    def refresh_invocation_counts(self):
        return self.base.refresh_invocation_counts()

    def refresh_publication(self, *, invocation_token):
        return self.base.refresh_publication(invocation_token=invocation_token)

    def refresh_binding(self, *, invocation_token):
        return self.base.refresh_binding(invocation_token=invocation_token)


class _TamperedProducer:
    def __init__(self, base):
        self.base = base

    def produce(self):
        evidence = self.base.produce()
        cells = []
        for cell in evidence.cells:
            altered = copy.deepcopy(cell)
            altered["raw_numerator_support"] = 1
            altered["raw_probability_exact_fraction"] = {"$exact_fraction": [1, 100]}
            cells.append(altered)
        return replace(evidence, cells=tuple(cells), denominator=100)


class _ZeroCellProducer:
    def __init__(self, base, zero_cell):
        self.base = base
        self.zero_cell = zero_cell

    def produce(self):
        evidence = self.base.produce()
        cells = []
        for cell in evidence.cells:
            altered = copy.deepcopy(cell)
            if altered["cell"] == self.zero_cell:
                altered["raw_numerator_support"] = 0
                altered["raw_probability_exact_fraction"] = {"$exact_fraction": [0, evidence.denominator]}
            else:
                altered["raw_numerator_support"] = evidence.denominator
                altered["raw_probability_exact_fraction"] = {"$exact_fraction": [1, 1]}
            cells.append(altered)
        return replace(evidence, cells=tuple(cells))


class _NullNumeratorProducer:
    def __init__(self, base):
        self.base = base

    def produce(self):
        evidence = self.base.produce()
        cells = [copy.deepcopy(cell) for cell in evidence.cells]
        cells[0]["raw_numerator_support"] = None
        return replace(evidence, cells=tuple(cells))


class _ZeroDenominatorProducer:
    def __init__(self, base):
        self.base = base

    def produce(self):
        evidence = self.base.produce()
        return replace(evidence, denominator=0)


class _RaisingProducer:
    def produce(self):
        raise RuntimeError("producer unavailable")


class _RaisingConsumer:
    def consume(self, **_kwargs):
        raise RuntimeError("consumer severed")


class _FaultyRefreshProvider:
    def __init__(self, base):
        self.base = base

    def snapshot(self):
        return self.base.snapshot()

    def refresh_invocation_counts(self):
        return self.base.refresh_invocation_counts()

    def refresh_publication(self, *, invocation_token):
        raise RuntimeError("publication refresh failed")

    def refresh_binding(self, *, invocation_token):
        raise RuntimeError("binding refresh failed")


class _NonAuditedRefreshProvider:
    def __init__(self, base):
        self.base = base

    def snapshot(self):
        return self.base.snapshot()

    def refresh_invocation_counts(self):
        return self.base.refresh_invocation_counts()

    def _receipt(self, channel, invocation_token, snapshot):
        return {
            "channel": channel,
            "executed": True,
            "world_owner": snapshot.world_owner,
            "base_revision": snapshot.revision,
            "world_result_ref": snapshot.selection_digest,
            "invocation_token": invocation_token,
            "generation": snapshot.revision + 1,
            "successor_digest": semantic_hash(
                {
                    "channel": channel,
                    "world_owner": snapshot.world_owner,
                    "base_revision": snapshot.revision,
                    "world_result_ref": snapshot.selection_digest,
                    "invocation_token": invocation_token,
                }
            ),
        }

    def refresh_publication(self, *, invocation_token):
        snapshot = self.base.snapshot()
        return self._receipt("H2_PUBLICATION_BOUNDARY_REFRESH", invocation_token, snapshot)

    def refresh_binding(self, *, invocation_token):
        snapshot = self.base.snapshot()
        return self._receipt("H2_GENERATED_BINDING_REFRESH", invocation_token, snapshot)


def test_hostile_01_altered_horizon_and_sanctions_with_unchanged_digest():
    base = build_success_fixture()
    snapshot = base["world_provider"].snapshot()
    values = copy.deepcopy(snapshot.values)
    values["absolute_horizon"] = "fx:ATTACKER_AH"
    values["public_sanctions"] = ["fx:sanction:attacker"]
    provider = _TamperedWorldProvider(
        base["world_provider"], replace(snapshot, values=values)
    )
    result = _serve({**base, "world_provider": provider})
    _assert_refusal(result, "WORLD_VALUES_TAMPERED_REFUSED")
    assert "fx:ATTACKER_AH" not in str(result.material())


def test_hostile_02_cells_sum_two_with_denominator_one_hundred():
    base = build_success_fixture()
    result = _serve({**base, "producer": _TamperedProducer(base["producer"])})
    _assert_refusal(result, "GEOMETRY_CELL_SUM_MISMATCH_REFUSED")


def test_geometry_zero_cell_is_exact_and_zero_or_null_is_refused():
    base = build_success_fixture()
    zero_cell = _serve(
        {**base, "producer": _ZeroCellProducer(base["producer"], "P2")}
    )
    assert zero_cell.result_state == "EXACT_SUPPORTED"
    zero_entry = next(c for c in zero_cell.receipt.geometry["cells"] if c["cell"] == "P2")
    assert zero_entry["raw_numerator_support"] == 0
    assert zero_entry["raw_probability_exact_fraction"] == {"$exact_fraction": [0, 62]}
    assert sum(c["raw_numerator_support"] for c in zero_cell.receipt.geometry["cells"]) == 62
    null_numerator = _serve(
        {**base, "producer": _NullNumeratorProducer(base["producer"])}
    )
    _assert_refusal(null_numerator, "GEOMETRY_REFUSED")
    zero_denominator = _serve(
        {**base, "producer": _ZeroDenominatorProducer(base["producer"])}
    )
    _assert_refusal(zero_denominator, "GEOMETRY_ZERO_DENOMINATOR_REFUSED")


def test_issuer_version_time_and_operation_are_narrow():
    base = build_success_fixture()
    request = base["request"]
    grant = base["grant"]
    wrong_version = replace(request, issuer_ref=replace(grant.authority_ref, authority_version="999.0.0"))
    _assert_refusal(
        _serve({**base, "request": wrong_version}), "ISSUER_MISSING_OR_INCOMPETENT_REFUSED"
    )
    fake = replace(grant.authority_ref, authority_content_hash="f" * 64)
    _assert_refusal(
        _serve({**base, "request": replace(request, issuer_ref=fake)}),
        "ISSUER_MISSING_OR_INCOMPETENT_REFUSED",
    )
    future = make_test_grant(
        target_ref=request.target_ref,
        risk_set_ref=request.risk_set_ref,
        world_owner=request.selected_world_owner,
        operations={ROLE_REVERSE},
        valid_from="2030-01-01",
        valid_until=None,
    )
    _assert_refusal(
        _serve(
            {
                **base,
                "issuer_registry": ExactIssuerRegistry([future]),
                "request": replace(request, issuer_ref=future.authority_ref),
            }
        ),
        "ISSUER_TIME_SCOPE_REFUSED",
    )
    expired = make_test_grant(
        target_ref=request.target_ref,
        risk_set_ref=request.risk_set_ref,
        world_owner=request.selected_world_owner,
        operations={ROLE_REVERSE},
        valid_from="2020-01-01",
        valid_until="2021-01-01",
    )
    _assert_refusal(
        _serve(
            {
                **base,
                "issuer_registry": ExactIssuerRegistry([expired]),
                "request": replace(request, issuer_ref=expired.authority_ref),
            }
        ),
        "ISSUER_TIME_SCOPE_REFUSED",
    )
    wrong_operation = make_test_grant(
        target_ref=request.target_ref,
        risk_set_ref=request.risk_set_ref,
        world_owner=request.selected_world_owner,
        operations={ROLE_FORWARD},
        valid_until=None,
    )
    _assert_refusal(
        _serve(
            {
                **base,
                "issuer_registry": ExactIssuerRegistry([wrong_operation]),
                "request": replace(request, issuer_ref=wrong_operation.authority_ref),
            }
        ),
        "ISSUER_OPERATION_REFUSED",
    )


def test_hostile_03_fake_refresh_receipts_from_failing_provider():
    base = build_success_fixture()
    result = _serve({**base, "world_provider": _FaultyRefreshProvider(base["world_provider"])})
    _assert_refusal(result, "REFRESH_CHANNEL_FAULT_REFUSED")
    result = _serve(
        {**base, "world_provider": _NonAuditedRefreshProvider(base["world_provider"])}
    )
    _assert_refusal(result, "REFRESH_AUDIT_MISSING_REFUSED")


def test_hostile_04_enriched_receipt_mutation_changes_result_identity():
    result = _serve(build_success_fixture())
    verify_result_integrity(result)
    formula = semantic_hash(
        {
            "schema": "PYAT_PE_SC0_OWNER_BOUND_RESULT@1",
            "contract": result.material()["contract"],
            "request_ref": result.request_ref.as_dict(),
            "result_state": result.result_state,
            "receipt_ref": result.receipt.ref.as_dict(),
            "receipt_hash": result.receipt.receipt_hash,
            "refusal_state": None,
            "refusal_reason": None,
        }
    )
    assert formula == result.result_hash
    material = copy.deepcopy(result.receipt.material())
    material["world"]["values"]["absolute_horizon"] = "fx:MUTATED_AFTER_SIGNING"
    mutated_receipt_hash = semantic_hash(material)
    assert mutated_receipt_hash != result.receipt.receipt_hash
    mutated_ref = {
        "kind": RECEIPT_SCHEMA,
        "object_id": f"urn:rawlsing:pyat:pe-sc0:owner-bound-receipt:sha256:{mutated_receipt_hash}",
        "content_hash": mutated_receipt_hash,
    }
    mutated_result_hash = semantic_hash(
        {
            "schema": "PYAT_PE_SC0_OWNER_BOUND_RESULT@1",
            "contract": result.material()["contract"],
            "request_ref": result.request_ref.as_dict(),
            "result_state": result.result_state,
            "receipt_ref": mutated_ref,
            "receipt_hash": mutated_receipt_hash,
            "refusal_state": None,
            "refusal_reason": None,
        }
    )
    assert mutated_result_hash != result.result_hash


def test_hostile_05_source_promotion_from_faulty_producer_is_refused():
    base = build_success_fixture()
    echo = copy.deepcopy(base["world_provider"].generated_binding_echo)
    echo["may_use_as_source_observation"] = True
    provider = _provider_from_base(base, generated_binding_echo=echo)
    result = _serve(_bundle_with_provider(base, provider))
    _assert_refusal(result, "SOURCE_PROMOTION_REFUSED")
    echo = copy.deepcopy(base["world_provider"].generated_binding_echo)
    echo["upstream_authorship"] = True
    provider = _provider_from_base(base, generated_binding_echo=echo)
    result = _serve(_bundle_with_provider(base, provider))
    _assert_refusal(result, "SOURCE_PROMOTION_REFUSED")
    promotion_grant = make_test_grant(
        target_ref=base["request"].target_ref,
        risk_set_ref=base["request"].risk_set_ref,
        world_owner=base["request"].selected_world_owner,
        operations={ROLE_REVERSE, "SOURCE_PROMOTION"},
        source_promotion_authority=True,
    )
    with pytest.raises(OwnerBoundRefusal) as excinfo:
        ExactIssuerRegistry([promotion_grant]).require_source_promotion(
            promotion_grant.authority_ref
        )
    assert excinfo.value.state == "TEST_AUTHORITY_NOT_COMPETENT_FOR_SOURCE_PROMOTION"


def test_hostile_06_held_authority_missing_scope_is_refused():
    base = build_success_fixture()
    rows = [copy.deepcopy(row) for row in base["world_provider"].negative_status_rows]
    for row in rows:
        if row["state"] == "HELD_AUTHORITY":
            row["scope"] = None
    provider = _provider_from_base(base, negative_status_rows=tuple(rows))
    result = _serve(_bundle_with_provider(base, provider))
    _assert_refusal(result, "NEGATIVE_STATUS_SCOPE_REFUSED")
    rows = [copy.deepcopy(row) for row in base["world_provider"].negative_status_rows]
    for row in rows:
        if row["state"] == "HELD_AUTHORITY":
            row.pop("risk_set_ref", None)
    provider = _provider_from_base(base, negative_status_rows=tuple(rows))
    result = _serve(_bundle_with_provider(base, provider))
    _assert_refusal(result, "NEGATIVE_STATUS_SCOPE_REFUSED")


def test_hostile_07_all_time_grant_does_not_erase_target_or_risk_scope():
    base = build_success_fixture()
    request = base["request"]
    bad_target = make_test_grant(
        target_ref=request.target_ref,
        risk_set_ref=request.risk_set_ref,
        world_owner=request.selected_world_owner,
        operations={ROLE_REVERSE},
        target_refs={"urn:test:attacker:unauthorized-target"},
        valid_until=None,
    )
    bundle = {
        **base,
        "issuer_registry": ExactIssuerRegistry([bad_target]),
        "request": replace(request, issuer_ref=bad_target.authority_ref),
    }
    _assert_refusal(_serve(bundle), "ISSUER_TARGET_REFUSED")
    bad_risk = make_test_grant(
        target_ref=request.target_ref,
        risk_set_ref=request.risk_set_ref,
        world_owner=request.selected_world_owner,
        operations={ROLE_REVERSE},
        target_refs={request.target_ref.key},
        risk_set_refs={"urn:test:attacker:unauthorized-risk"},
        valid_until=None,
    )
    bundle = {
        **base,
        "issuer_registry": ExactIssuerRegistry([bad_risk]),
        "request": replace(request, issuer_ref=bad_risk.authority_ref),
    }
    _assert_refusal(_serve(bundle), "ISSUER_RISK_REFUSED")


def test_hostile_08_no_sitecustomize_or_pythonpath_monkeypatch():
    assert not (CANDIDATE_DIR / "sitecustomize.py").exists()
    from rawlsing_next.pre553_empirical_possibility_provider import (
        provide_empirical_possibility_slice,
    )

    before = provide_empirical_possibility_slice
    import fixtures as _fixtures  # noqa: F401
    import first_consumer as _first_consumer  # noqa: F401
    import n10e_adapter as _n10e_adapter  # noqa: F401
    import owner_bound_successor as _owner_bound_successor  # noqa: F401
    import sourcefree_world as _sourcefree_world  # noqa: F401

    assert provide_empirical_possibility_slice is before
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([str(CANDIDATE_DIR), str(REPO_ROOT)])
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; print('sitecustomize' in sys.modules); "
            "import rawlsing_next.pre553_empirical_possibility_provider as p; "
            "print(p.provide_empirical_possibility_slice.__module__)",
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    assert completed.stdout.splitlines() == [
        "False",
        "rawlsing_next.pre553_empirical_possibility_provider",
    ]


def test_hostile_09_stale_clock_revision_and_invalidated_current():
    base = build_success_fixture()
    bundle = {**base, "request": replace(base["request"], world_revision=999)}
    _assert_refusal(_serve(bundle), "WORLD_REVISION_MISMATCH_REFUSED")
    clocks = copy.deepcopy(base["world_provider"].clocks)
    clocks["publication_knowledge"] = "2030"
    provider = _provider_from_base(base, clocks=clocks)
    _assert_refusal(_serve(_bundle_with_provider(base, provider)), "STALE_CURRENT_REFUSED")
    clocks = copy.deepcopy(base["world_provider"].clocks)
    clocks["request_currentness"] = "2025-01-01"
    provider = _provider_from_base(base, clocks=clocks)
    _assert_refusal(_serve(_bundle_with_provider(base, provider)), "STALE_CURRENT_REFUSED")
    bundle = {
        **base,
        "request": replace(base["request"], n9_snapshot_state="INVALIDATED"),
    }
    _assert_refusal(_serve(bundle), "INVALIDATED_CURRENT_REFUSED")


def test_hostile_10_wrong_target_condition_role_direction():
    base = build_success_fixture(role_direction=ROLE_REVERSE)
    bundle = {
        **base,
        "producer": N10EProducer(case=build_provider_case("forward")),
    }
    _assert_refusal(_serve(bundle), "ROLE_DIRECTION_REFUSED")
    swapped = replace(
        base["request"],
        target_ref=base["request"].conditioner_coordinate_ref,
        conditioner_coordinate_ref=base["request"].target_ref,
    )
    swapped_result = _serve({**base, "request": swapped})
    assert swapped_result.result_state == "TYPED_REFUSAL"
    assert swapped_result.refusal_state in {
        "ISSUER_TARGET_REFUSED",
        "ROLE_DIRECTION_REFUSED",
    }
    assert swapped_result.receipt is None
    base = build_success_fixture(role_direction=ROLE_FORWARD)
    bundle = {
        **base,
        "producer": N10EProducer(case=build_provider_case("reverse")),
    }
    _assert_refusal(_serve(bundle), "ROLE_DIRECTION_REFUSED")


def test_hostile_11_missing_producer_or_severed_consumer():
    base = build_success_fixture()
    _assert_refusal(_serve({**base, "producer": None}), "PRODUCER_MISSING_REFUSED")
    _assert_refusal(_serve({**base, "producer": _RaisingProducer()}), "PRODUCER_FAULT_REFUSED")
    _assert_refusal(_serve({**base, "consumer": None}), "CONSUMER_SEVERED_REFUSED")
    _assert_refusal(_serve({**base, "consumer": _RaisingConsumer()}), "CONSUMER_SEVERED_REFUSED")
    _assert_refusal(
        _serve({**base, "world_provider": None}), "WORLD_PROVIDER_MISSING_REFUSED"
    )


def test_hostile_12_wrong_replay_asof_or_changed_world_owner():
    base = build_success_fixture()
    result = _serve(base)
    verify_result_integrity(result)
    replayed = verify_replay(
        result,
        producer=base["producer"],
        world_provider=base["world_provider"],
        issuer_registry=base["issuer_registry"],
        consumer=base["consumer"],
        request=base["request"],
    )
    assert replayed.result_hash == result.result_hash
    changed_asof = replace(base["request"], n9_asof_time="2020-01-01")
    with pytest.raises(OwnerBoundReplayError):
        verify_replay(
            result,
            producer=base["producer"],
            world_provider=base["world_provider"],
            issuer_registry=base["issuer_registry"],
            consumer=base["consumer"],
            request=changed_asof,
        )
    changed_result = _serve({**base, "request": changed_asof})
    assert changed_result.result_hash != result.result_hash
    provider = _provider_from_base(base, world_owner="urn:test:attacker:world-owner")
    mismatch = _serve(
        {
            **base,
            "world_provider": provider,
            "request": replace(
                base["request"], selected_world_digest=provider.selection_digest
            ),
        }
    )
    _assert_refusal(mismatch, "WORLD_OWNER_MISMATCH_REFUSED")
    bundle = {**base, "request": replace(base["request"], world_revision=999)}
    _assert_refusal(_serve(bundle), "WORLD_REVISION_MISMATCH_REFUSED")
