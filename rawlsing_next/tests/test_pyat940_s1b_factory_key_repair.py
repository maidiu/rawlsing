from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess

import pytest

from rawlsing_next.pre553_r157_projection_adapter import (
    R157_HISTORICAL_COMMIT,
    SourceConfigurationBindingError,
    _effective_row_native_keys,
    build_source_backed_c11_repository_from_config,
    build_validated_c11_release_from_config,
    load_fixture_stream,
    load_source_config,
    row_native_keys_from_transport,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.tests.test_pyat940_s1b_support import build_scenario

ROOT = Path(__file__).resolve().parents[2]
SRC09_RELEASE = "15f65920ec025a02a67b1572c3ce43f343186322f7dd2c381f18733c2d58194b"


def _git_blob(relative: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{R157_HISTORICAL_COMMIT}:{relative}"],
        capture_output=True,
        check=True,
    ).stdout


def _historical_src09(tmp_path: Path):
    config_path = tmp_path / "SRC09.full.fixture.config.json"
    fixture_path = tmp_path / "SRC09.full.fixture.json"
    config_path.write_bytes(_git_blob(
        "rawlsing_next/source_configuration/data/SRC09/SRC09.full.fixture.config.json"
    ))
    fixture_path.write_bytes(_git_blob(
        "source_pre553_validation/SRC09/SRC09.full.fixture.json"
    ))
    return load_source_config(config_path), load_fixture_stream(fixture_path)


def _swapped(keys):
    swapped = dict(keys)
    swapped[1], swapped[2] = keys[2], keys[1]
    return swapped


def test_factory_and_repository_refuse_swapped_keys_on_historical_stream(tmp_path):
    config, stream = _historical_src09(tmp_path)
    keys = row_native_keys_from_transport(config, stream=stream)
    baseline = build_validated_c11_release_from_config(config, stream=stream)
    assert baseline.release_ref.content_hash == SRC09_RELEASE
    assert build_validated_c11_release_from_config(
        config, stream=stream, row_native_keys=keys
    ).release_ref.content_hash == SRC09_RELEASE

    swapped = _swapped(keys)
    with pytest.raises(
        SourceConfigurationBindingError,
        match="supplied row-native keys differ from the physical cell key witnesses",
    ):
        build_validated_c11_release_from_config(
            config, stream=stream, row_native_keys=swapped
        )
    with pytest.raises(
        SourceConfigurationBindingError,
        match="supplied row-native keys differ from the physical cell key witnesses",
    ):
        build_source_backed_c11_repository_from_config(
            config, stream, row_native_keys=swapped
        )

    repository, release = build_source_backed_c11_repository_from_config(
        config, stream, row_native_keys=keys
    )
    assert release.release_ref.content_hash == SRC09_RELEASE
    assert repository is not None


@pytest.mark.parametrize("source_format", ("SAV", "DTA"))
def test_factory_refuses_swapped_keys_on_incidence_and_stream(tmp_path, source_format):
    scenario = build_scenario(tmp_path / source_format, source_format=source_format)
    incidence = scenario["incidence"]
    try:
        keys = scenario["keys"]
        swapped = _swapped(keys)
        baseline = build_validated_c11_release_from_config(
            scenario["config"], incidence=incidence, batch_size=4
        )
        assert baseline.release_ref.content_hash == scenario["release"].release_ref.content_hash
        matching = build_validated_c11_release_from_config(
            scenario["config"], incidence=incidence, row_native_keys=keys, batch_size=4
        )
        assert matching.release_ref.content_hash == baseline.release_ref.content_hash
        with pytest.raises(
            SourceConfigurationBindingError,
            match="supplied row-native keys differ from the physical cell key witnesses",
        ):
            build_validated_c11_release_from_config(
                scenario["config"], incidence=incidence, row_native_keys=swapped,
                batch_size=4,
            )
        with pytest.raises(
            SourceConfigurationBindingError,
            match="supplied row-native keys differ from the physical cell key witnesses",
        ):
            build_source_backed_c11_repository_from_config(
                scenario["config"], incidence, row_native_keys=swapped, batch_size=4
            )

        stream = ExactPhysicalCellStream(
            source_sha256=scenario["source_sha"],
            row_count=scenario["rows"],
            cell_iter_factory=lambda: tuple(scenario["cells"]),
        )
        assert build_validated_c11_release_from_config(
            scenario["config"], stream=stream, row_native_keys=keys
        ).release_ref.content_hash == baseline.release_ref.content_hash
        with pytest.raises(
            SourceConfigurationBindingError,
            match="supplied row-native keys differ from the physical cell key witnesses",
        ):
            build_validated_c11_release_from_config(
                scenario["config"], stream=stream, row_native_keys=swapped
            )
        with pytest.raises(
            SourceConfigurationBindingError,
            match="supplied row-native keys differ from the physical cell key witnesses",
        ):
            build_source_backed_c11_repository_from_config(
                scenario["config"], stream, row_native_keys=swapped
            )
    finally:
        incidence.close()


def test_unkeyed_and_typed_absence_key_states(tmp_path):
    unkeyed = build_scenario(
        tmp_path / "unkeyed", source_format="SAV", config_kwargs={"keyed": False}
    )
    try:
        baseline = build_validated_c11_release_from_config(
            unkeyed["config"], incidence=unkeyed["incidence"], batch_size=4
        )
        assert baseline.release_ref.content_hash == unkeyed["release"].release_ref.content_hash
        with pytest.raises(
            SourceConfigurationBindingError,
            match="row_native_keys supplied without a configured source_native_key_slot",
        ):
            build_validated_c11_release_from_config(
                unkeyed["config"], incidence=unkeyed["incidence"],
                row_native_keys={1: unkeyed["keys"][1] if unkeyed["keys"] else None},
                batch_size=4,
            )
    finally:
        unkeyed["incidence"].close()

    scenario = build_scenario(tmp_path / "typed-absence", source_format="SAV")
    try:
        cells = []
        for cell in scenario["cells"]:
            if cell.row_ordinal == 1 and cell.variable_name == "country":
                cells.append(PhysicalCell(
                    cell.row_ordinal, cell.variable_ordinal, cell.variable_name,
                    None, PhysicalMissingState.SYSTEM_MISSING, None,
                ))
            else:
                cells.append(cell)
        stream = ExactPhysicalCellStream(
            source_sha256=scenario["source_sha"],
            row_count=scenario["rows"],
            cell_iter_factory=lambda: tuple(cells),
        )
        keys = _effective_row_native_keys(
            scenario["config"], stream=stream, incidence=None, explicit=None, batch_size=4
        )
        assert keys[1].state == "UNKNOWN"
        assert _effective_row_native_keys(
            scenario["config"], stream=stream, incidence=None, explicit=keys, batch_size=4
        ) == keys
        fabricated = dict(keys)
        fabricated[1] = keys[2]
        with pytest.raises(
            SourceConfigurationBindingError,
            match="supplied row-native keys differ from the physical cell key witnesses",
        ):
            _effective_row_native_keys(
                scenario["config"], stream=stream, incidence=None,
                explicit=fabricated, batch_size=4,
            )
    finally:
        scenario["incidence"].close()
