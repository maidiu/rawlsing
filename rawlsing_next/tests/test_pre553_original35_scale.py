from dataclasses import replace

import pytest

from rawlsing_next import pre553_source_backed_c11_facade as facade
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState, decode_sav
from rawlsing_next.pre553_source_backed_c11_facade import (
    CoordinateValueRule,
    build_source_backed_c11_repository,
    physical_value_binding_key,
)
from rawlsing_next.pre553_source_native_preimage_adapter import (
    NativePreimageRefusal,
    NativeSourceRule,
    materialize_native_preimages,
)
from rawlsing_next.tests.test_universal_source_projection import (
    build_s3,
    package,
    s3_rows,
    write_rows,
)

AS_OF = "2026-11-06"


def test_materialize_prebuilt_release_is_reused_by_repository(tmp_path, monkeypatch):
    path = tmp_path / "reuse.sav"
    bundle = build_s3(path, s3_rows(respondents=3, occasions=2))
    stream = bundle.physical_stream
    assert stream.prebuilt_release is not None
    assert stream.prebuilt_projection_identity == bundle.projection.cache_identity

    def unexpected(*_args, **_kwargs):
        pytest.fail("validated C11 release was rebuilt instead of reusing the prebuilt release")

    with monkeypatch.context() as patch:
        patch.setattr(facade, "build_validated_source_backed_c11_release_from_stream", unexpected)
        repository, release = build_source_backed_c11_repository(stream, bundle.projection)
    assert len(repository) == 1
    assert release.release_ref == bundle.release.release_ref
    assert release.replay_manifest.ref == bundle.release.replay_manifest.ref


def test_materialize_consumes_exact_caller_coordinate_rules(tmp_path):
    path = tmp_path / "coordinate.sav"
    rows = s3_rows(respondents=3, occasions=2)
    write_rows(path, rows)
    pkg = package(path, len(rows), (NativeSourceRule("impl.score", "SCORE"),), coordinate="OCCASION")
    incidence = decode_sav(path)
    try:
        legacy = materialize_native_preimages(package=pkg, incidence=incidence)
        base_rule = legacy.projection.coordinate_slots[0]
        values = tuple(
            CoordinateValueRule(
                physical_value_binding_key(value, PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
                "UNKNOWN",
                None,
            )
            for value in (0.0, 1.0)
        )
        rule = replace(base_rule, values=values, copy_observed_raw=False)
        assert rule.copy_observed_raw is False
        explicit = materialize_native_preimages(
            package=pkg, incidence=incidence, coordinate_rules=(rule,),
        )
        assert explicit.projection.coordinate_slots == (rule,)
        coordinate_states = {
            obj.typed_state for obj in explicit.release.public_objects
            if obj.schema_id == "EmpiricalCoordinateFact"
        }
        assert coordinate_states == {"UNKNOWN"}
        with pytest.raises(NativePreimageRefusal, match="COORDINATE_SLOT_RULE_MATCH_REQUIRED"):
            materialize_native_preimages(package=pkg, incidence=incidence, coordinate_rules=())
    finally:
        incidence.close()
