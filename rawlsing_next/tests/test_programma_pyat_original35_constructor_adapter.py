"""Recovered P1 constructor keeps no-drop and no longer blanket-holds RAW on weight."""
from __future__ import annotations

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.programma_pyat_original35_constructor import (
    MEASURE_DIRECT, OPERATION_DISTRIBUTION, SCOPE_TEST_ONLY, STATUS_COMPILED,
    EligibleItem, Original35Input, ScientificMethodInput, SourceGrant,
    WaveAdmission, WaveIdentity, construct_original35_epre,
)


def _ref(kind: str, tag: str) -> ExactRef:
    digest = semantic_hash({"kind": kind, "tag": tag})
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", digest)


def _wave(index: int) -> WaveAdmission:
    sha = semantic_hash({"source": index})
    grant = SourceGrant(
        grant_ref=_ref("SourceGrant", str(index)), source_sha256=sha,
        scope=SCOPE_TEST_ONLY, operations=(OPERATION_DISTRIBUTION, MEASURE_DIRECT),
        currentness="CURRENT",
        item_registry_ref=_ref("ItemRegistry", str(index)),
        eligible_population_ref=_ref("EligiblePopulation", str(index)),
        target_use_permission_ref=_ref("TargetUsePermission", str(index)))
    def item(tag: str):
        return EligibleItem(
            item_ref=_ref("SourceItem", tag), source_variable_code=tag,
            response_values=("0", "1"), route_ref=_ref("Route", str(index)),
            weight_ref=None, eligibility_ref=grant.eligible_population_ref,
            semantic_ref=_ref("Semantic", str(index)),
            role_ref=_ref("Role", str(index)),
            use_permission_ref=grant.target_use_permission_ref,
            operation_kinds=(OPERATION_DISTRIBUTION,),
            measure_authority_ref=_ref("MeasureAuthority", str(index)))
    return WaveAdmission(
        identity=WaveIdentity(
            f"ATLAS-{index:02d}", f"DATASET-{index:02d}", "FAMILY",
            f"W{index:02d}", sha),
        release_ref=_ref("C11LogicalRelease", str(index)),
        source_grant=grant, items=(item(f"Q{index:02d}A"), item(f"Q{index:02d}B")))


def test_p1_missing_optional_weight_is_not_a_raw_hold_and_no_drop_is_deterministic():
    method = ScientificMethodInput(
        method_ref=_ref("ScientificMethod", "direct"),
        method_kind=MEASURE_DIRECT,
        owner_ref=_ref("MethodOwner", "owner"),
        authority_ref=_ref("MethodAuthority", "authority"))
    plan = construct_original35_epre(Original35Input(
        waves=tuple(_wave(index) for index in range(35)),
        scientific_method=method))
    assert plan.no_drop_ok is True
    assert len(plan.operations) == 35 * 2 * 2
    assert len(plan.batch_units) == 140
    assert not plan.holds
    assert all(op.status == STATUS_COMPILED for op in plan.operations)
    assert plan.plan_ref == construct_original35_epre(Original35Input(
        waves=tuple(_wave(index) for index in range(35)),
        scientific_method=method)).plan_ref
