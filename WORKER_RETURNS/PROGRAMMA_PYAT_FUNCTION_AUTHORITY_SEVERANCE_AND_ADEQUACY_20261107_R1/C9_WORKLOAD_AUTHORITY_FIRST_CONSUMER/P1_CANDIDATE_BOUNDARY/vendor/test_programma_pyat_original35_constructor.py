from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.programma_pyat_original35_constructor import (
    MEASURE_DIRECT,
    MEASURE_PROXY,
    OPERATION_CONDITIONAL,
    OPERATION_DISTRIBUTION,
    OPERATION_HETEROGENEITY,
    OPERATION_JOINT,
    OPERATION_RECURSIVE,
    SCOPE_TEST_ONLY,
    STATUS_ABSTAIN,
    STATUS_COMPILED,
    STATUS_HOLD,
    ConditionerBinding,
    EligibleItem,
    JointBinding,
    Original35ConstructorError,
    Original35Input,
    ScientificMethodInput,
    SourceGrant,
    WaveAdmission,
    WaveIdentity,
    construct_original35_epre,
)


def _h(tag: str) -> str:
    return semantic_hash({"test": tag})


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:programma:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _method(kind: str = MEASURE_DIRECT, *, owner: bool = True) -> ScientificMethodInput:
    return ScientificMethodInput(
        method_ref=_ref("ScientificMethod", kind.lower()),
        method_kind=kind,
        owner_ref=_ref("MethodOwner", "owner") if owner else None,
        authority_ref=_ref("MethodAuthority", "authority") if owner else None,
    )


def _grant(tag: str, sha: str, *, operations=(
    OPERATION_DISTRIBUTION,
    OPERATION_CONDITIONAL,
    OPERATION_JOINT,
    OPERATION_HETEROGENEITY,
    OPERATION_RECURSIVE,
    MEASURE_DIRECT,
), currentness: str = "CURRENT") -> SourceGrant:
    return SourceGrant(
        grant_ref=_ref("SourceGrant", tag),
        source_sha256=sha,
        scope=SCOPE_TEST_ONLY,
        operations=operations,
        host="local-sourcefree",
        purpose="TEST_ONLY_SOURCEFREE",
        currentness=currentness,
        item_registry_ref=_ref("ItemRegistry", tag),
        eligible_population_ref=_ref("EligiblePopulation", tag),
        target_use_permission_ref=_ref("TargetUsePermission", tag),
    )


def _item(
    tag: str,
    code: str,
    *,
    grant: SourceGrant,
    refs: dict[str, ExactRef],
    operation_kinds=(OPERATION_DISTRIBUTION,),
    measure_kind: str = MEASURE_DIRECT,
    conditioner_bindings=(),
    joint_bindings=(),
    stratum_refs=(),
    recursive_authority_ref=None,
) -> EligibleItem:
    return EligibleItem(
        item_ref=_ref("SourceItem", tag),
        source_variable_code=code,
        response_values=("1", "2", "3"),
        route_ref=refs["route"],
        weight_ref=refs["weight"],
        eligibility_ref=grant.eligible_population_ref,
        semantic_ref=refs["semantic"],
        role_ref=refs["role"],
        use_permission_ref=grant.target_use_permission_ref,
        operation_kinds=operation_kinds,
        measure_kind=measure_kind,
        measure_authority_ref=_ref("MeasureAuthority", tag),
        conditioner_bindings=conditioner_bindings,
        joint_bindings=joint_bindings,
        stratum_refs=stratum_refs,
        recursive_authority_ref=recursive_authority_ref,
    )


def _wave(index: int) -> WaveAdmission:
    sha = _h(f"source-{index:02d}")
    identity = WaveIdentity(
        atlas_id=f"ATLAS-{index:02d}",
        dataset_id=f"DATASET-{index:02d}",
        source_family="ORIGINAL35",
        wave=f"WAVE-{index:02d}",
        source_sha256=sha,
    )
    grant = _grant(f"g{index:02d}", sha)
    refs = {
        "route": _ref("Route", f"r{index:02d}"),
        "weight": _ref("WeightDesign", f"w{index:02d}"),
        "semantic": _ref("Semantic", f"s{index:02d}"),
        "role": _ref("Role", f"ro{index:02d}"),
        "stratum": _ref("Stratum", f"st{index:02d}"),
        "recursive": _ref("RecursiveAuthority", f"ra{index:02d}"),
        "joint": _ref("JointAuthority", f"ja{index:02d}"),
    }
    first = _item(
        f"i{index:02d}a", f"Q{index:02d}A", grant=grant, refs=refs,
        operation_kinds=(OPERATION_DISTRIBUTION,))
    conditioner = ConditionerBinding(
        conditioner_ref=first.item_ref,
        conditioner_code=first.source_variable_code,
        values=("0", "1"),
        eligibility_ref=grant.eligible_population_ref,
    )
    joint = JointBinding(
        other_item_ref=first.item_ref,
        other_code=first.source_variable_code,
        values=("0", "1"),
        joint_authority_ref=refs["joint"],
        eligibility_ref=grant.eligible_population_ref,
    )
    second = _item(
        f"i{index:02d}b", f"Q{index:02d}B", grant=grant, refs=refs,
        operation_kinds=(
            OPERATION_DISTRIBUTION,
            OPERATION_CONDITIONAL,
            OPERATION_JOINT,
            OPERATION_HETEROGENEITY,
            OPERATION_RECURSIVE,
        ),
        conditioner_bindings=(conditioner,),
        joint_bindings=(joint,),
        stratum_refs=(refs["stratum"],),
        recursive_authority_ref=refs["recursive"],
    )
    return WaveAdmission(
        identity=identity,
        release_ref=_ref("C11LogicalRelease", f"release{index:02d}"),
        source_grant=grant,
        items=(first, second),
    )


def _input(*, waves=None, method=None) -> Original35Input:
    return Original35Input(
        waves=tuple(waves if waves is not None else (_wave(i) for i in range(35))),
        scientific_method=method or _method(),
    )


def _replace_wave(waves, index: int, **changes) -> tuple[WaveAdmission, ...]:
    out = list(waves)
    out[index] = replace(out[index], **changes)
    return tuple(out)


def _replace_item(wave: WaveAdmission, index: int, **changes) -> WaveAdmission:
    items = list(wave.items)
    items[index] = replace(items[index], **changes)
    return replace(wave, items=tuple(items))


def test_positive_original35_enumeration_and_no_drop():
    plan = construct_original35_epre(_input())
    assert plan.no_drop_ok is True
    assert len(plan.roster) == 35
    assert len(plan.waves) == 35
    assert len(plan.operations) == 840
    assert len(plan.batch_units) == 840
    assert len(plan.holds) == 0
    assert len(plan.abstentions) == 0
    assert isinstance(plan.batch_manifest, BatchManifest)
    assert all(isinstance(unit, BatchUnitSpec) for unit in plan.batch_units)
    assert plan.batch_manifest.units == plan.batch_units
    assert plan.source_qualification == SCOPE_TEST_ONLY
    assert plan.all35_populated_claim is False
    assert plan.sourced_results_claim is False
    assert plan.no_drop_manifest["expected_item_count"] == 70
    assert plan.no_drop_manifest["processed_item_count"] == 70
    assert plan.no_drop_manifest["compiled_operations"] == 840


def test_constructor_is_deterministic():
    first = construct_original35_epre(_input())
    second = construct_original35_epre(_input())
    assert first.plan_ref == second.plan_ref
    assert first.batch_manifest.manifest_ref == second.batch_manifest.manifest_ref


def test_thirty_four_waves_are_refused():
    waves = tuple(_wave(i) for i in range(34))
    with pytest.raises(Original35ConstructorError, match="INDEPENDENT_ORIGINAL35_ROSTER_REQUIRED"):
        construct_original35_epre(_input(waves=waves))


def test_duplicate_wave_is_refused():
    waves = tuple(_wave(i) for i in range(35))
    duplicate = replace(waves[1], identity=replace(waves[1].identity, atlas_id=waves[0].identity.atlas_id))
    bad = (waves[0], duplicate) + waves[2:]
    with pytest.raises(Original35ConstructorError, match="INDEPENDENT_ORIGINAL35_ROSTER_REQUIRED"):
        construct_original35_epre(_input(waves=bad))


def test_duplicate_item_ref_is_refused():
    waves = tuple(_wave(i) for i in range(35))
    bad_wave = replace(
        waves[0],
        items=(waves[0].items[0], replace(waves[0].items[1], item_ref=waves[0].items[0].item_ref)),
    )
    with pytest.raises(Original35ConstructorError, match="DUPLICATE_ITEM_REF"):
        construct_original35_epre(_input(waves=(bad_wave,) + waves[1:]))


def test_missing_source_grant_is_typed_hold_and_still_no_drop():
    waves = tuple(_wave(i) for i in range(35))
    bad = _replace_wave(waves, 0, source_grant=None)
    plan = construct_original35_epre(_input(waves=bad))
    assert plan.no_drop_ok is True
    assert len(plan.holds) == 24
    assert len(plan.abstentions) == 0
    assert all(op.reason == "SOURCE_GRANT_ABSENT" for op in plan.holds)
    assert len(plan.batch_units) == 816
    assert len(plan.operations) == 840
    assert plan.source_qualification == "NONISSUING_MIXED_OR_ABSENT"


def test_wrong_source_sha_abstains_only_that_wave_and_restores():
    base_waves = tuple(_wave(i) for i in range(35))
    bad_grant = replace(base_waves[0].source_grant, source_sha256=_h("wrong-sha"))
    bad = _replace_wave(base_waves, 0, source_grant=bad_grant)
    bad_plan = construct_original35_epre(_input(waves=bad))
    assert bad_plan.no_drop_ok is True
    assert len(bad_plan.abstentions) == 24
    assert all(op.reason == "SOURCE_SHA_MISMATCH" for op in bad_plan.abstentions)
    assert len(bad_plan.batch_units) == 816
    restored = construct_original35_epre(_input(waves=base_waves))
    assert restored.plan_ref != bad_plan.plan_ref
    assert len(restored.batch_units) == 840


def test_missing_route_is_typed_hold_and_restores():
    waves = tuple(_wave(i) for i in range(35))
    bad_wave = _replace_item(waves[0], 0, route_ref=None)
    plan = construct_original35_epre(_input(waves=(bad_wave,) + waves[1:]))
    assert plan.no_drop_ok is True
    assert len(plan.holds) == 3
    assert all(op.reason == "ROUTE_REF_ABSENT" for op in plan.holds)
    assert len(plan.batch_units) == 837
    assert construct_original35_epre(_input(waves=waves)).plan_ref != plan.plan_ref


def test_missing_weight_is_typed_hold():
    waves = tuple(_wave(i) for i in range(35))
    bad_wave = _replace_item(waves[0], 0, weight_ref=None)
    plan = construct_original35_epre(_input(waves=(bad_wave,) + waves[1:]))
    assert len(plan.holds) == 3
    assert all(op.reason == "WEIGHT_REF_ABSENT" for op in plan.holds)


def test_respondent_eligibility_mismatch_is_typed_abstain():
    waves = tuple(_wave(i) for i in range(35))
    bad_wave = _replace_item(waves[0], 1, eligibility_ref=_ref("EligiblePopulation", "foreign"))
    plan = construct_original35_epre(_input(waves=(bad_wave,) + waves[1:]))
    assert plan.no_drop_ok is True
    assert len(plan.abstentions) == 21
    assert all(op.reason == "RESPONDENT_ELIGIBILITY_MISMATCH" for op in plan.abstentions)


def test_missing_item_registry_is_typed_hold():
    waves = tuple(_wave(i) for i in range(35))
    bad_grant = replace(waves[0].source_grant, item_registry_ref=None)
    bad = _replace_wave(waves, 0, source_grant=bad_grant)
    plan = construct_original35_epre(_input(waves=bad))
    assert len(plan.holds) == 24
    assert all(op.reason == "ITEM_REGISTRY_REF_ABSENT" for op in plan.holds)


def test_conditional_binding_absence_is_typed_hold_not_silent_drop():
    waves = tuple(_wave(i) for i in range(35))
    bad_wave = _replace_item(waves[0], 1, conditioner_bindings=())
    plan = construct_original35_epre(_input(waves=(bad_wave,) + waves[1:]))
    assert plan.no_drop_ok is True
    assert len(plan.holds) == 1
    assert plan.holds[0].reason == "CONDITIONER_BINDING_ABSENT"
    assert len(plan.batch_units) == 834
    assert len(plan.operations) == 835


def test_false_native_measurement_is_typed_hold():
    waves = tuple(_wave(i) for i in range(35))
    bad_wave = _replace_item(waves[0], 0, measure_kind=MEASURE_PROXY)
    plan = construct_original35_epre(_input(waves=(bad_wave,) + waves[1:]))
    assert len(plan.holds) == 3
    assert all(op.reason == "MEASURE_NOT_IN_SOURCE_GRANT" for op in plan.holds)


def test_proxy_method_requires_owner_and_authority():
    waves = tuple(_wave(i) for i in range(35))
    proxy_waves = []
    for wave in waves:
        grant = replace(
            wave.source_grant,
            operations=tuple(wave.source_grant.operations) + (MEASURE_PROXY,),
        )
        proxy_waves.append(replace(
            wave,
            source_grant=grant,
            items=tuple(replace(item, measure_kind=MEASURE_PROXY) for item in wave.items),
        ))
    held = construct_original35_epre(_input(
        waves=tuple(proxy_waves), method=_method(MEASURE_PROXY, owner=False)))
    assert len(held.holds) == 840
    assert len(held.batch_units) == 0
    assert all("METHOD_OWNER" in (op.reason or "") or "SCIENTIFIC_METHOD" in (op.reason or "")
               for op in held.holds)
    owned = construct_original35_epre(_input(
        waves=tuple(proxy_waves), method=_method(MEASURE_PROXY)))
    assert len(owned.holds) == 0
    assert len(owned.abstentions) == 0
    assert len(owned.batch_units) == 840


def test_all_held_has_no_batch_manifest_and_no_drop():
    waves = tuple(replace(w, source_grant=None) for w in (_wave(i) for i in range(35)))
    plan = construct_original35_epre(_input(waves=waves))
    assert plan.no_drop_ok is True
    assert plan.batch_manifest is None
    assert len(plan.batch_units) == 0
    assert len(plan.holds) == 840
    assert plan.all35_populated_claim is False


def test_batch_manifest_contains_only_compiled_operations():
    waves = tuple(_wave(i) for i in range(35))
    bad = _replace_item(waves[0], 0, route_ref=None)
    plan = construct_original35_epre(_input(waves=(bad,) + waves[1:]))
    assert plan.batch_manifest is not None
    assert len(plan.batch_manifest.units) == len(plan.batch_units) == 837
    assert all(op.batch_job_ref is None for op in plan.holds)
    assert all(op.status == STATUS_HOLD for op in plan.holds)
    assert all(op.status == STATUS_COMPILED for op in plan.operations if op not in plan.holds)


def test_stale_source_grant_is_typed_hold():
    waves = tuple(_wave(i) for i in range(35))
    stale_grant = replace(waves[0].source_grant, currentness="STALE")
    bad = _replace_wave(waves, 0, source_grant=stale_grant)
    plan = construct_original35_epre(_input(waves=bad))
    assert len(plan.holds) == 24
    assert all(op.reason == "SOURCE_GRANT_NOT_CURRENT" for op in plan.holds)
    assert len(plan.batch_units) == 816


def test_original_scope_input_still_does_not_claim_populated_results():
    waves = tuple(_wave(i) for i in range(35))
    original = tuple(
        replace(wave, source_grant=replace(wave.source_grant, scope="ORIGINAL_SOURCE_ISSUED"))
        for wave in waves
    )
    plan = construct_original35_epre(_input(waves=original))
    assert plan.source_qualification == "ORIGINAL_SOURCE_ISSUED"
    assert plan.all35_populated_claim is False
    assert plan.sourced_results_claim is False
    assert len(plan.batch_units) == 840
