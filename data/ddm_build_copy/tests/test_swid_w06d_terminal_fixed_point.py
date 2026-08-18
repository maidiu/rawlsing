from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pytest

from data.ddm_build_copy.build_source_structure_validator import canonical_wave_label
from data.ddm_build_copy.ddm_source_wave_identity import (
    ProductionMembershipError,
    closed_35_identities,
    load_identity_registry,
    resolve_source_wave_identity,
)
from data.ddm_build_copy.run_20var_allwaves_v550_552j_smoke import (
    ALL_WAVES,
    COMPILER_SPECS,
    DEFAULT_CONFIG,
    runtime_compiler_paths,
    validate_explicit_scope,
)


EXPECTED_CLOSED_35 = {
    ("Afrobarometer", "R1"),
    ("Afrobarometer", "R5"),
    ("Afrobarometer", "R9"),
    ("Arab Barometer", "I"),
    ("Arab Barometer", "II"),
    ("Arab Barometer", "V"),
    ("Arab Barometer", "VIII"),
    ("Asian Barometer", "W1"),
    ("Asian Barometer", "W4"),
    ("Asian Barometer", "W5"),
    ("EVS", "1981"),
    ("EVS", "1990"),
    ("EVS", "1999"),
    ("EVS", "2008"),
    ("EVS", "2017"),
    ("GSS", "1972"),
    ("GSS", "1973"),
    ("GSS", "1984"),
    ("GSS", "1993"),
    ("GSS", "2002"),
    ("GSS", "2010"),
    ("GSS", "2016"),
    ("GSS", "2024"),
    ("Latinobarómetro", "1995"),
    ("Latinobarómetro", "2011"),
    ("Latinobarómetro", "2024"),
    ("LiTS", "2006"),
    ("LiTS", "II"),
    ("LiTS", "III"),
    ("LiTS", "IV"),
    ("South Asia", "W1"),
    ("South Asia", "W2"),
    ("WVS", "W1"),
    ("WVS", "W4"),
    ("WVS", "W7"),
}

EXPECTED_CANARY_SCOPE = {
    ("Arab Barometer", "I"),
    ("EVS", "1981"),
    ("EVS", "1999"),
    ("Afrobarometer", "R1"),
    ("Latinobarómetro", "1995"),
}

EXPECTED_COMPILERS = {
    "v550": "data/ddm_build_copy/build_determinicity_wave_shard_v550.py",
    "v550j": "data/ddm_build_copy/compile_v550j_joint_response_patterns.py",
    "v551": "data/ddm_build_copy/compile_v551_relation_evidence_atoms.py",
    "v551j": "data/ddm_build_copy/compile_v551j_joint_evidence_packets.py",
    "v552": "data/ddm_build_copy/compile_v552_structural_ddm.py",
    "v552j": "data/ddm_build_copy/compile_v552j_structural_handoff.py",
}


def _registry_family_by_uid() -> dict[str, dict]:
    registry = load_identity_registry()
    return registry.source_uid_index


def test_closed_35_catalog_is_exact_unique_and_production_authorized() -> None:
    identities = closed_35_identities()
    pairs = {(i.canonical_display_source, i.canonical_display_wave) for i in identities}
    uid_pairs = {(i.source_family_uid, i.wave_uid) for i in identities}
    assert pairs == EXPECTED_CLOSED_35
    assert len(identities) == 35
    assert len(uid_pairs) == 35
    assert all(i.production_authorized for i in identities)


def test_every_declared_alias_for_all_35_resolves_to_the_same_governed_uid() -> None:
    families = _registry_family_by_uid()
    seen = 0
    for canonical in closed_35_identities():
        family = families[canonical.source_family_uid]
        wave = next(row for row in family["waves"] if row["wave_uid"] == canonical.wave_uid)
        family_aliases = set(family.get("aliases") or []) | {family["canonical_display_source"]}
        wave_aliases = set(wave.get("aliases") or []) | {
            wave["canonical_display_wave"],
            wave["compatibility_key"],
        }
        for source_alias in family_aliases:
            for wave_alias in wave_aliases:
                resolved = resolve_source_wave_identity(source_alias, wave_alias, require_closed_35=True)
                assert (resolved.source_family_uid, resolved.wave_uid) == (
                    canonical.source_family_uid,
                    canonical.wave_uid,
                )
                seen += 1
    assert seen > 35

    latin = "Latinobarómetro"
    latin_nfd = unicodedata.normalize("NFD", latin)
    for source_alias in (latin, latin_nfd, "Latinobarometro"):
        resolved = resolve_source_wave_identity(source_alias, "1995", require_closed_35=True)
        assert resolved.wave_uid == "wv_latinobarometro_1995_v1"


def test_uid_native_physical_tokens_are_unique_ascii_and_versioned_for_all_35() -> None:
    tokens = [identity.uid_native_physical_token for identity in closed_35_identities()]
    assert len(set(tokens)) == 35
    for token in tokens:
        assert token.isascii()
        assert re.fullmatch(r"[A-Za-z0-9_.-]+", token), token
        assert token.startswith("swidp1__")


def test_asian_barometer_w6_is_recognized_but_cannot_enter_closed_35() -> None:
    identity = resolve_source_wave_identity("Asian Barometer", "W6")
    assert identity.canonical_display_wave == "W6"
    assert not identity.closed_35_member
    assert not identity.production_authorized
    with pytest.raises(ProductionMembershipError):
        resolve_source_wave_identity("Asian Barometer", "W6", require_closed_35=True)
    assert ("Asian Barometer", "W6") not in EXPECTED_CLOSED_35


def test_supported_smoke_catalog_is_exactly_closed_35_and_uid_clean() -> None:
    assert len(ALL_WAVES) == 35
    assert {(source, wave) for source, wave, _country in ALL_WAVES} == EXPECTED_CLOSED_35
    assert all(country for _source, _wave, country in ALL_WAVES)
    assert validate_explicit_scope(ALL_WAVES) == []


def test_required_respondent_canary_scopes_have_exact_governed_identity() -> None:
    smoke_pairs = {(source, wave) for source, wave, _country in ALL_WAVES}
    assert EXPECTED_CANARY_SCOPE <= smoke_pairs
    for source, wave in EXPECTED_CANARY_SCOPE:
        identity = resolve_source_wave_identity(source, wave, require_closed_35=True)
        assert identity.production_authorized
        assert identity.source_family_uid
        assert identity.wave_uid


def test_supported_runtime_compiler_entrypoints_are_exact_and_present() -> None:
    assert COMPILER_SPECS == EXPECTED_COMPILERS
    actual = runtime_compiler_paths(DEFAULT_CONFIG)
    assert set(actual) == set(EXPECTED_COMPILERS)
    for stage, path in actual.items():
        assert path == DEFAULT_CONFIG.repo_root / EXPECTED_COMPILERS[stage]
        assert path.is_file(), f"missing active compiler: {stage}: {path}"


def test_v550_legacy_compatibility_wave_is_separate_from_display_and_uid_identity() -> None:
    evs = resolve_source_wave_identity("EVS", "1981", require_closed_35=True)
    assert evs.raw_wave == "1981"
    assert canonical_wave_label(evs.raw_source, evs.raw_wave) == "W1"
    assert evs.canonical_display_wave == "1981"
    assert evs.wave_uid == "wv_evs_1981_v1"
    assert len({canonical_wave_label(evs.raw_source, evs.raw_wave), evs.canonical_display_wave, evs.wave_uid}) == 3
