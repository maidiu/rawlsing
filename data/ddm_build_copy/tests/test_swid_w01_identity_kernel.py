from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import pytest

from data.ddm_build_copy.ddm_source_wave_identity import (
    CLOSED_35,
    RECOGNIZED_EXCLUDED,
    GlobalWaveResolutionError,
    ProductionMembershipError,
    UnknownSourceWaveError,
    closed_35_identities,
    resolve_source_family_identity,
    resolve_source_wave_identity,
    resolve_wave_identity,
)
from data.ddm_build_copy.ddm_survey_identity import (
    canonical_family_key,
    canonical_family_label,
    canonical_wave_key,
    wave_aliases,
    wave_ordinal,
)


# QRA may delegate identity resolution, but question/relationship authority stays QRA-owned.
from data.ddm_build_copy.ddm_v550_question_relation_authority import (
    canonical_country_code as qra_canonical_country_code,
    canonical_source_family as qra_canonical_source_family,
    canonical_wave as qra_canonical_wave,
)

ROOT = Path(__file__).resolve().parents[3]
REGISTRY = (
    ROOT / "data" / "ddm_build_copy" / "bindings"
    / "source_wave_identity_registry_35wave_v1.json"
)

KNOWN_SOURCE_ALIASES = {
    "Afrobarometer": ["Afrobarometer", "Afro Barometer"],
    "Arab Barometer": ["Arab Barometer", "ArabBarometer"],
    "Asian Barometer": ["Asian Barometer", "AsianBarometer", "Asian Barometer Survey"],
    "EVS": ["EVS", "European Values Study", "European Values Survey"],
    "GSS": ["GSS", "General Social Survey"],
    "Latinobarómetro": ["Latinobarómetro", "Latinobarometro"],
    "LiTS": ["LiTS", "Life in Transition Survey", "Life Transition Survey"],
    "South Asia": ["South Asia", "SouthAsia", "South Asia Barometer"],
    "WVS": ["WVS", "WV", "World Values Survey"],
}

KNOWN_WAVE_ALIASES = {
    ("Afrobarometer", "R1"): ["R1", "ROUND1", "Round 1", "W1", "Wave 1", "1"],
    ("Afrobarometer", "R5"): ["R5", "ROUND5", "Round 5", "W5", "Wave 5", "5"],
    ("Afrobarometer", "R9"): ["R9", "ROUND9", "Round 9", "W9", "Wave 9", "9"],
    ("Arab Barometer", "I"): ["I", "W1", "Wave 1", "1"],
    ("Arab Barometer", "II"): ["II", "W2", "Wave 2", "2"],
    ("Arab Barometer", "V"): ["V", "W5", "Wave 5", "5"],
    ("Arab Barometer", "VIII"): ["VIII", "W8", "Wave 8", "8"],
    ("Asian Barometer", "W1"): ["W1", "Wave 1", "1"],
    ("Asian Barometer", "W4"): ["W4", "Wave 4", "4"],
    ("Asian Barometer", "W5"): ["W5", "Wave 5", "5"],
    ("Asian Barometer", "W6"): ["W6", "Wave 6", "6"],
    ("EVS", "1981"): ["1981", "W1", "Wave 1", "1"],
    ("EVS", "1990"): ["1990", "W2", "Wave 2", "2"],
    ("EVS", "1999"): ["1999", "W3", "Wave 3", "3"],
    ("EVS", "2008"): ["2008", "W4", "Wave 4", "4"],
    ("EVS", "2017"): ["2017", "W5", "Wave 5", "5"],
    ("GSS", "1972"): ["1972"], ("GSS", "1973"): ["1973"],
    ("GSS", "1984"): ["1984"], ("GSS", "1993"): ["1993"],
    ("GSS", "2002"): ["2002"], ("GSS", "2010"): ["2010"],
    ("GSS", "2016"): ["2016"], ("GSS", "2024"): ["2024"],
    ("Latinobarómetro", "1995"): ["1995"],
    ("Latinobarómetro", "2011"): ["2011"],
    ("Latinobarómetro", "2024"): ["2024"],
    ("LiTS", "2006"): ["2006", "I", "W1", "Wave 1", "1"],
    ("LiTS", "II"): ["II", "W2", "Wave 2", "2"],
    ("LiTS", "III"): ["III", "W3", "Wave 3", "3"],
    ("LiTS", "IV"): ["IV", "W4", "Wave 4", "4"],
    ("South Asia", "W1"): ["W1", "Wave 1", "1"],
    ("South Asia", "W2"): ["W2", "Wave 2", "2"],
    ("WVS", "W1"): ["W1", "Wave 1", "1"],
    ("WVS", "W4"): ["W4", "Wave 4", "4"],
    ("WVS", "W7"): ["W7", "Wave 7", "7"],
}

EXPECTED_CLOSED_35 = {
    ("Afrobarometer", "R1"), ("Afrobarometer", "R5"), ("Afrobarometer", "R9"),
    ("Arab Barometer", "I"), ("Arab Barometer", "II"), ("Arab Barometer", "V"), ("Arab Barometer", "VIII"),
    ("Asian Barometer", "W1"), ("Asian Barometer", "W4"), ("Asian Barometer", "W5"),
    ("EVS", "1981"), ("EVS", "1990"), ("EVS", "1999"), ("EVS", "2008"), ("EVS", "2017"),
    ("GSS", "1972"), ("GSS", "1973"), ("GSS", "1984"), ("GSS", "1993"),
    ("GSS", "2002"), ("GSS", "2010"), ("GSS", "2016"), ("GSS", "2024"),
    ("Latinobarómetro", "1995"), ("Latinobarómetro", "2011"), ("Latinobarómetro", "2024"),
    ("LiTS", "2006"), ("LiTS", "II"), ("LiTS", "III"), ("LiTS", "IV"),
    ("South Asia", "W1"), ("South Asia", "W2"),
    ("WVS", "W1"), ("WVS", "W4"), ("WVS", "W7"),
}


def _registry_payload() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_closed_35_is_explicit_and_exact():
    identities = closed_35_identities()
    actual = {
        (item.canonical_display_source, item.canonical_display_wave)
        for item in identities
    }
    assert len(identities) == 35
    assert actual == EXPECTED_CLOSED_35
    assert all(item.governance_state == CLOSED_35 for item in identities)
    assert all(item.production_authorized for item in identities)


def test_every_governed_source_and_wave_alias_resolves_within_family():
    payload = _registry_payload()
    for family in payload["source_families"]:
        canonical_source = family["canonical_display_source"]
        source_uid = family["source_family_uid"]
        for source_alias in family["aliases"]:
            resolved_source = resolve_source_family_identity(source_alias)
            assert resolved_source.source_family_uid == source_uid
            assert resolved_source.canonical_display_source == canonical_source

        for wave in family["waves"]:
            for wave_alias in wave["aliases"]:
                resolved = resolve_source_wave_identity(canonical_source, wave_alias)
                assert resolved.source_family_uid == source_uid
                assert resolved.wave_uid == wave["wave_uid"]
                assert resolved.canonical_display_wave == wave["canonical_display_wave"]


def test_audited_alias_matrix_resolves_to_declared_display_identity():
    for display_source, aliases in KNOWN_SOURCE_ALIASES.items():
        expected_uid = resolve_source_family_identity(display_source).source_family_uid
        for alias in aliases:
            resolved = resolve_source_family_identity(alias)
            assert resolved.canonical_display_source == display_source
            assert resolved.source_family_uid == expected_uid

    for (source, display_wave), aliases in KNOWN_WAVE_ALIASES.items():
        expected_uid = resolve_source_wave_identity(source, display_wave).wave_uid
        for alias in aliases:
            resolved = resolve_source_wave_identity(source, alias)
            assert resolved.canonical_display_wave == display_wave
            assert resolved.wave_uid == expected_uid


@pytest.mark.parametrize("alias", ["I", "W1", "Wave 1", "1"])
def test_arab_barometer_wave_one_aliases(alias: str):
    assert resolve_source_wave_identity("Arab Barometer", alias).canonical_display_wave == "I"


@pytest.mark.parametrize(
    ("alias", "expected"),
    [("1981", "1981"), ("W1", "1981"), ("1999", "1999"), ("W3", "1999")],
)
def test_evs_year_and_wave_aliases(alias: str, expected: str):
    assert resolve_source_wave_identity("EVS", alias).canonical_display_wave == expected


@pytest.mark.parametrize("alias", ["R1", "ROUND1", "Round 1"])
def test_afrobarometer_round_aliases(alias: str):
    assert resolve_source_wave_identity("Afrobarometer", alias).canonical_display_wave == "R1"


def test_latinobarometro_nfc_nfd_and_unaccented_source_aliases_share_uid():
    nfc = "Latinobarómetro"
    nfd = unicodedata.normalize("NFD", nfc)
    forms = [nfc, nfd, "Latinobarometro"]
    identities = [resolve_source_wave_identity(form, "1995") for form in forms]
    assert {item.source_family_uid for item in identities} == {"sf_latinobarometro_v1"}
    assert {item.wave_uid for item in identities} == {"wv_latinobarometro_1995_v1"}
    assert {item.canonical_display_source for item in identities} == {nfc}
    assert identities[1].raw_source == nfd


def test_global_bare_wave_resolution_is_forbidden_even_for_known_alias():
    with pytest.raises(GlobalWaveResolutionError):
        resolve_wave_identity("W1")


def test_asian_barometer_w6_is_recognized_but_not_closed_35():
    identity = resolve_source_wave_identity("Asian Barometer", "W6")
    assert identity.canonical_display_wave == "W6"
    assert identity.governance_state == RECOGNIZED_EXCLUDED
    assert identity.closed_35_member is False
    assert identity.production_authorized is False
    with pytest.raises(ProductionMembershipError):
        resolve_source_wave_identity("Asian Barometer", "W6", require_closed_35=True)


@pytest.mark.parametrize(
    ("source", "wave"),
    [
        ("EVS", "R1"),
        ("Arab Barometer", "W4"),
        ("GSS", "W1"),
        ("Latinobarómetro", "W1"),
        ("Asian Barometer", "VIII"),
    ],
)
def test_invalid_source_family_wave_combinations_fail(source: str, wave: str):
    with pytest.raises(UnknownSourceWaveError):
        resolve_source_wave_identity(source, wave)


def test_uid_identity_and_physical_token_are_alias_stable_ascii_and_versioned():
    aliases = [
        resolve_source_wave_identity("ArabBarometer", "I"),
        resolve_source_wave_identity("Arab Barometer", "W1"),
        resolve_source_wave_identity("Arab Barometer", "Wave 1"),
    ]
    assert len({item.uid_key for item in aliases}) == 1
    assert len({item.uid_native_physical_token for item in aliases}) == 1
    token = aliases[0].uid_native_physical_token
    assert token.startswith("swidp1__")
    assert re.fullmatch(r"[A-Za-z0-9_]+", token)
    assert "Arab Barometer" not in token


def test_legacy_compatibility_representation_remains_unchanged():
    assert canonical_family_key("Latinobarómetro") == "latinobarometro"
    assert canonical_family_label("latinobarometro") == "Latinobarómetro"
    assert canonical_wave_key("Afrobarometer", "R1") == "ROUND1"
    assert canonical_wave_key("Afrobarometer", "1") == "1"
    assert canonical_wave_key("Arab Barometer", "Wave 1") == "I"
    assert canonical_wave_key("EVS", "1981") == "W1"
    assert canonical_wave_key("EVS", "1999") == "W3"
    assert wave_ordinal("Afrobarometer", "R9") == 9
    assert wave_aliases("Afrobarometer", "R1") == ["ROUND1", "R1", "1", "Round 1"]


def test_raw_display_compatibility_uid_and_governance_representations_remain_distinct():
    item = resolve_source_wave_identity("European Values Study", "W3")
    assert item.raw_source == "European Values Study"
    assert item.raw_wave == "W3"
    assert item.canonical_display_source == "EVS"
    assert item.canonical_display_wave == "1999"
    assert item.compatibility_source_key == "evs"
    assert item.compatibility_wave_key == "W3"
    assert item.source_family_uid == "sf_evs_v1"
    assert item.wave_uid == "wv_evs_1999_v1"
    assert item.governance_state == CLOSED_35

def test_qra_source_wave_identity_delegates_to_shared_kernel_without_changing_display_dialect():
    nfc = "Latinobarómetro"
    nfd = unicodedata.normalize("NFD", nfc)
    assert qra_canonical_source_family(nfc) == nfc
    assert qra_canonical_source_family(nfd) == nfc
    assert qra_canonical_source_family("Latinobarometro") == nfc

    for alias in ("R1", "ROUND1", "Round 1"):
        assert qra_canonical_wave("Afrobarometer", alias) == "R1"
    for alias in ("I", "W1", "Wave 1", "1"):
        assert qra_canonical_wave("Arab Barometer", alias) == "I"
    for alias in ("1981", "W1"):
        assert qra_canonical_wave("EVS", alias) == "1981"
    for alias in ("1999", "W3"):
        assert qra_canonical_wave("EVS", alias) == "1999"


def test_qra_non_identity_semantics_are_not_absorbed_into_shared_kernel():
    # Country aliases are QRA-local governed behavior and must not move into the
    # source/wave kernel as a side effect of identity delegation.
    assert qra_canonical_country_code("BF") == "LS"
    assert qra_canonical_country_code("LY") == "YE"
    # A source-family/wave combination outside identity authority remains
    # unresolved rather than being manufactured by generic wave grammar.
    assert qra_canonical_wave("Arab Barometer", "W4") == "W4"
    assert qra_canonical_wave("GSS", "W1") == "W1"


def test_qra_asian_w6_is_recognized_for_identity_but_not_promoted_to_closed_35():
    assert qra_canonical_wave("Asian Barometer", "W6") == "W6"
    identity = resolve_source_wave_identity("Asian Barometer", "W6")
    assert identity.governance_state == RECOGNIZED_EXCLUDED
    assert not identity.production_authorized
