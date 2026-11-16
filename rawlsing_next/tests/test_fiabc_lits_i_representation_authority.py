from __future__ import annotations

from decimal import Decimal
from pathlib import Path
import types

import pytest

import rawlsing_next.ee_p2x_darwin_stage_backend as backend
from rawlsing_next.fiabc_final_oracle_freeze_producers import (
    LITS_BASE_CANDIDATE_PROJECTION,
    LITS_R5B_BLOBS,
    LITS_R5B_COMMIT,
    LITS_R5B_DRIVER,
    _lits_accepted_legacy_base_candidate,
    _lits_accepted_legacy_projection,
)
from rawlsing_next.fiabc_lits_i_representation_authority import (
    ACCEPTED_C11_RELEASE_IDENTITY,
    AUTHORITY_KIND,
    AUTHORIZED_BANKED_R5_TOKENS,
    AUTHORIZED_DECODER_R5_TOKENS,
    CURRENT_TYPED_FACADE_BLOB,
    LEGACY_FACADE_BLOB,
    LEGACY_FACADE_COMMIT,
    LEGACY_FACADE_PATH,
    NATIVE_CODES,
    NEGATIVE_LIMITS,
    OPERATION,
    REPRESENTATION_AUTHORITY_REF,
    SOURCE_SHA256,
    TARGET_VARIABLES,
    authorized_banked_raw_value,
    authorized_replay_cell,
    representation_authority_snapshot,
)
from rawlsing_next.pre553_empirical_authority import (
    Pre553AuthorityError,
    require_positive_authority,
    validate_authority_snapshot,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key


REPO = Path(__file__).resolve().parents[2]
CODEC = R5TypedValueCodec()
FLOATS = {
    1: 1.0,
    2: 2.0,
    3: 3.0,
    4: 4.0,
    5: 5.0,
    6: 6.0,
    7: 7.0,
}


def _value(**overrides):
    values = {
        "source_sha256": SOURCE_SHA256,
        "variable_name": "q301_2",
        "ordinal": 194,
        "raw_value": 1.0,
        "missing_state": PhysicalMissingState.OBSERVED_STORAGE_VALUE,
        "source_missing_declaration": None,
    }
    values.update(overrides)
    return authorized_banked_raw_value(**values)


def _cell(**overrides):
    values = {
        "row_ordinal": 1,
        "variable_ordinal": 194,
        "variable_name": "q301_2",
        "raw_value": 1.0,
        "missing_state": PhysicalMissingState.OBSERVED_STORAGE_VALUE,
        "source_missing_declaration": None,
        "raw_value_label": "UNUSED_LABEL_WITNESS",
    }
    values.update(overrides)
    return PhysicalCell(**values)


def test_exact_decoder_tokens_map_only_to_exact_banked_tokens():
    for name, ordinal in TARGET_VARIABLES.items():
        for code in NATIVE_CODES:
            value = authorized_banked_raw_value(
                source_sha256=SOURCE_SHA256,
                variable_name=name,
                ordinal=ordinal,
                raw_value=FLOATS[code],
                missing_state=PhysicalMissingState.OBSERVED_STORAGE_VALUE,
                source_missing_declaration=None,
            )
            assert type(value) is Decimal
            assert CODEC.encode(FLOATS[code]) == AUTHORIZED_DECODER_R5_TOKENS[code]
            assert CODEC.encode(value) == AUTHORIZED_BANKED_R5_TOKENS[code]


def test_representation_bridge_is_source_variable_state_type_and_token_bounded():
    hostile = (
        {"source_sha256": "0" * 64},
        {"variable_name": "q301_3"},
        {"ordinal": 199},
        {"raw_value": 1},
        {"raw_value": Decimal("1.0")},
        {"raw_value": "1"},
        {"raw_value": True},
        {"raw_value": 0.0},
        {"raw_value": 8.0},
        {"missing_state": PhysicalMissingState.FORMAT_USER_MISSING_VALUE},
        {"source_missing_declaration": {"kind": "value", "value": 1.0}},
    )
    for overrides in hostile:
        with pytest.raises(ValueError):
            _value(**overrides)


def test_system_missing_is_exact_and_not_reinterpreted():
    assert _value(
        raw_value=None,
        missing_state=PhysicalMissingState.SYSTEM_MISSING,
    ) is None
    with pytest.raises(ValueError):
        _value(raw_value=1.0, missing_state=PhysicalMissingState.SYSTEM_MISSING)
    with pytest.raises(ValueError):
        _value(
            raw_value=None,
            missing_state=PhysicalMissingState.SYSTEM_MISSING,
            source_missing_declaration={"kind": "value", "value": 7},
        )


def test_non_target_cells_are_byte_semantically_untouched_and_labels_are_not_used():
    other = _cell(variable_name="country", variable_ordinal=98, raw_value="BY")
    assert authorized_replay_cell(source_sha256=SOURCE_SHA256, cell=other) is other
    first = authorized_replay_cell(source_sha256=SOURCE_SHA256, cell=_cell())
    second = authorized_replay_cell(
        source_sha256=SOURCE_SHA256,
        cell=_cell(raw_value_label="DIFFERENT_UNUSED_LABEL"),
    )
    assert first.raw_value == second.raw_value == Decimal("1.0")
    assert first.raw_value_label != second.raw_value_label


def test_current_typed_key_law_remains_distinct_and_unmodified():
    state = PhysicalMissingState.OBSERVED_STORAGE_VALUE
    assert physical_value_binding_key(1.0, state) != physical_value_binding_key(Decimal("1.0"), state)
    assert physical_value_binding_key(Decimal("1.0"), state) != physical_value_binding_key(Decimal(1), state)
    assert backend._blob((REPO / "rawlsing_next/pre553_source_backed_c11_facade.py").read_bytes()) == CURRENT_TYPED_FACADE_BLOB


def test_legacy_facade_is_loaded_only_from_exact_commit_and_blob(tmp_path):
    deployed = backend._deploy(
        REPO,
        tmp_path,
        LEGACY_FACADE_COMMIT,
        LEGACY_FACADE_PATH,
        LEGACY_FACADE_BLOB,
    )
    assert backend._blob(deployed.read_bytes()) == LEGACY_FACADE_BLOB
    legacy = backend._load(deployed, "_fiabc_lits_i_test_legacy_facade")
    state = PhysicalMissingState.OBSERVED_STORAGE_VALUE
    assert legacy.physical_value_binding_key(Decimal("1.0"), state) == legacy.physical_value_binding_key(Decimal(1), state)
    assert legacy.physical_value_binding_key(Decimal("1.0"), state) != physical_value_binding_key(Decimal("1.0"), state)


def test_actual_banked_projection_converts_to_exact_accepted_legacy_owner(tmp_path):
    ctx = types.SimpleNamespace(work_root=tmp_path / "banked")
    services = types.SimpleNamespace(repo_root=REPO)
    projection, _context, banked = backend._lits_projection(ctx, services, {}, None)
    legacy, converted = _lits_accepted_legacy_projection(
        projection=projection,
        repo_root=REPO,
        neutral_root=tmp_path / "legacy",
        backend=backend,
    )
    assert converted.cache_identity == projection.cache_identity
    assert len(converted.response_slots) == 2
    assert len(converted.coordinate_slots) == 5
    assert len(converted.routing) == 58004
    assert legacy.physical_value_binding_key(
        Decimal("1.0"), PhysicalMissingState.OBSERVED_STORAGE_VALUE
    ) == legacy.physical_value_binding_key(
        Decimal(1), PhysicalMissingState.OBSERVED_STORAGE_VALUE
    )
    legacy_response_keys = {
        legacy.physical_value_binding_key(
            Decimal(code), PhysicalMissingState.OBSERVED_STORAGE_VALUE
        )
        for code in NATIVE_CODES
    }
    legacy_missing_key = legacy.physical_value_binding_key(
        None, PhysicalMissingState.SYSTEM_MISSING
    )
    for slot in converted.response_slots:
        assert {rule.physical_key for rule in slot.values} == (
            legacy_response_keys | {legacy_missing_key}
        )
    for slot in converted.coordinate_slots:
        assert {rule.physical_key for rule in slot.values} == {legacy_missing_key}
    assert physical_value_binding_key(
        Decimal(1), PhysicalMissingState.OBSERVED_STORAGE_VALUE
    ) not in legacy_response_keys
    coordinate = _cell(
        variable_name="country",
        variable_ordinal=98,
        raw_value=112.0,
    )
    assert banked.exact_cell(coordinate).raw_value == Decimal("112.0")


def test_authority_snapshot_is_positive_narrow_and_candidate_neutral():
    snapshot = representation_authority_snapshot()
    assert validate_authority_snapshot(snapshot) == snapshot
    assert require_positive_authority(
        snapshot,
        authority_kind=AUTHORITY_KIND,
        operation=OPERATION,
        object_family="RespondentEvent",
    ) == snapshot
    with pytest.raises(Pre553AuthorityError, match="authority kind mismatch"):
        require_positive_authority(snapshot, authority_kind="SOURCE_SEMANTICS_TOPOLOGY")
    assert snapshot.authority_ref == REPRESENTATION_AUTHORITY_REF
    for limit in (
        "NO_GLOBAL_INT_FLOAT_DECIMAL_COERCION",
        "NO_OTHER_VARIABLES",
        "NO_OTHER_SOURCES",
        "NO_CURRENT_TYPED_KEY_EQUIVALENCE",
        "NO_LABEL_OR_FREQUENCY_AUTHORITY",
        "NO_MISSINGNESS_INFERENCE",
        "NO_RESPONSE_SEMANTIC_REMAP",
        "NO_CANDIDATE_OUTPUT_PARENTAGE",
        "NO_SYSTEM_MISSING_REINTERPRETATION",
    ):
        assert limit in NEGATIVE_LIMITS


def test_producer_helper_pins_accepted_base_candidate_before_returning(monkeypatch, tmp_path):
    class LegacyProjection:
        cache_identity = "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872"

    class LegacyStream:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def iter_cells(self):
            return self.kwargs["cell_iter_factory"]()

    good_release = types.SimpleNamespace(
        release_ref=types.SimpleNamespace(content_hash=ACCEPTED_C11_RELEASE_IDENTITY),
        replay_manifest=types.SimpleNamespace(
            ref=types.SimpleNamespace(
                content_hash="6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd"
            )
        ),
    )
    replayed = []

    good_candidate = types.SimpleNamespace(
        candidate_replay_manifest=types.SimpleNamespace(
            semantic_projection_hash=LITS_BASE_CANDIDATE_PROJECTION
        )
    )

    def project_candidate(*, cells, **_kwargs):
        replayed.extend(cells)
        return good_candidate

    legacy = types.SimpleNamespace(
        GovernedC11Projection=lambda **kwargs: LegacyProjection(),
        ExactPhysicalCellStream=LegacyStream,
        project_c11_candidate_from_physical_cells=project_candidate,
        validate_c11_source_release=lambda candidate: (
            good_release if candidate is good_candidate else None
        ),
    )
    fake_backend = types.SimpleNamespace(
        _deploy=lambda *args: tmp_path / "legacy.py",
        _load=lambda *args: legacy,
    )
    incidence = types.SimpleNamespace(
        source_sha256=SOURCE_SHA256,
        row_count=29002,
        iter_cells=lambda **kwargs: iter((
            _cell(raw_value=1.0),
            _cell(variable_name="country", variable_ordinal=98, raw_value=112.0),
        )),
    )
    banked = types.SimpleNamespace(
        exact_cell=lambda cell: PhysicalCell(
            row_ordinal=cell.row_ordinal,
            variable_ordinal=cell.variable_ordinal,
            variable_name=cell.variable_name,
            raw_value=Decimal(str(cell.raw_value)) if type(cell.raw_value) is float else cell.raw_value,
            missing_state=cell.missing_state,
            source_missing_declaration=cell.source_missing_declaration,
            raw_value_label=cell.raw_value_label,
        )
    )
    projection = types.SimpleNamespace()
    monkeypatch.setattr(
        "rawlsing_next.fiabc_final_oracle_freeze_producers._lits_accepted_legacy_projection",
        lambda **kwargs: (legacy, LegacyProjection()),
    )
    observed_legacy, observed_projection, candidate = _lits_accepted_legacy_base_candidate(
        incidence=incidence,
        projection=projection,
        repo_root=REPO,
        neutral_root=tmp_path,
        backend=fake_backend,
        banked=banked,
    )
    assert observed_legacy is legacy
    assert isinstance(observed_projection, LegacyProjection)
    assert candidate is good_candidate
    assert [cell.raw_value for cell in replayed] == [Decimal("1.0"), Decimal("112.0")]


def test_exact_adopted_r5b_successor_driver_and_support_are_source_free_pinned(tmp_path):
    deployed = {
        path: backend._deploy(REPO, tmp_path, LITS_R5B_COMMIT, path, blob)
        for path, blob in LITS_R5B_BLOBS.items()
    }
    for path, blob in LITS_R5B_BLOBS.items():
        assert backend._blob(deployed[path].read_bytes()) == blob
    r5b = backend._load(deployed[LITS_R5B_DRIVER], "_fiabc_test_exact_r5b_successor")
    assert r5b.verify_frozen_support()
