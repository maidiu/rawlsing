"""KUDA-082: diagnostic-only test of existing R157 and C11 two-path fidelity.

This test owns NO production reader, issuer, semantic schema, all35 index,
or historical universal_source_to_c11 package. Do not install an alternative
C11 entrypoint to make a historical fixture check pass.
"""
import pytest

from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_r157_projection_adapter import (
    SourceConfig,
    SourceConfigurationBindingError,
    build_governed_c11_projection,
    decode_fixture_config,
    project_c11_candidate_from_config,
    row_native_keys_from_transport,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_validated_source_backed_c11_release,
)
from rawlsing_next.tests.test_pyat940_s1b_support import build_scenario, make_config


@pytest.mark.parametrize("format_name,values", (
    ("SAV", (1.0, 2.0, 0.0, 7.0, 8.0, -1.0, None)),
    ("DTA", (1.0, 1.0, 0.0, None)),
))
def test_independent_current_r157_facade_vs_direct_i02_parity(
    tmp_path, format_name, values,
):
    court = build_scenario(
        tmp_path / format_name, source_format=format_name, values=values,
    )
    try:
        incidence = court["incidence"]
        config = court["config"]
        keys = row_native_keys_from_transport(
            config, incidence=incidence, batch_size=3,
        )
        projection = build_governed_c11_projection(
            config, source_sha256=incidence.source_sha256,
            row_count=incidence.row_count, row_native_keys=keys,
        )
        # Both executions remain inside the CHOSEN current owners.
        facade_release = build_validated_source_backed_c11_release(
            incidence, projection, batch_size=3,
        )
        candidate = project_c11_candidate_from_config(
            config, projection,
            cells_factory=lambda: incidence.iter_cells(3),
            row_native_keys=keys,
            source_sha256=incidence.source_sha256,
            row_count=incidence.row_count,
        )
        repository = C11Repository()
        ingestion = ingest_c11_source_release(candidate, repository)
        assert ingestion.accepted
        assert ingestion.release_ref is not None
        direct = repository.resolve_release_exact(ingestion.release_ref)
        assert direct.release_ref == facade_release.release_ref == court["release"].release_ref
        assert direct.source_artifact_ref == facade_release.source_artifact_ref
        assert direct.semantic_release_hash == facade_release.semantic_release_hash
        assert direct.m01_m18_coverage == facade_release.m01_m18_coverage
        assert repository.release_refs == (direct.release_ref,)
    finally:
        court["incidence"].close()


def test_fixture_reader_must_refuse_closed_original_source_config_before_io(tmp_path):
    # This deliberately constructs source authority SHAPE only, not a grant;
    # the sourcefree decoder must not open any named original source.
    fake_sha = "a" * 64
    config = SourceConfig(make_config(
        source_format="SAV", active_source_sha256=fake_sha,
        row_count=2, values=(1.0, 2.0),
        original=True, purpose="SOURCE_PREPARATION",
    ))
    assert config.identity_class == "ORIGINAL_SOURCE"
    with pytest.raises(
        SourceConfigurationBindingError,
        match="decode_fixture_config refuses ORIGINAL_SOURCE",
    ):
        decode_fixture_config(config, tmp_path / "nonexistent-original.sav")
