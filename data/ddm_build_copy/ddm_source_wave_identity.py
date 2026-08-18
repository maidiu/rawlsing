#!/usr/bin/env python3
"""Governed source/wave identity kernel.

This module separates four things that historical callers often collapsed:

* raw/native labels supplied by an artifact or caller;
* canonical display labels used by governed authority;
* compatibility keys used by existing Rawlsing joins and identifiers;
* stable UID identity plus explicit production-membership state.

The UID registry is additive.  It does not rewrite historical shard IDs,
checkpoint names, cache keys, path tokens, or hash payloads.
"""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_IDENTITY_REGISTRY_PATH = (
    ROOT / "data" / "ddm_build_copy" / "bindings"
    / "source_wave_identity_registry_35wave_v1.json"
)

CLOSED_35 = "CLOSED_35"
RECOGNIZED_EXCLUDED = "RECOGNIZED_EXCLUDED"


class SourceWaveIdentityError(ValueError):
    """Base class for governed source/wave identity failures."""


class UnknownSourceFamilyError(SourceWaveIdentityError):
    """Raised when a source family is not present in governed identity authority."""


class UnknownSourceWaveError(SourceWaveIdentityError):
    """Raised when a wave alias is not governed for the resolved source family."""


class GlobalWaveResolutionError(SourceWaveIdentityError):
    """Raised when a wave is presented without an exact source-family context."""


class ProductionMembershipError(SourceWaveIdentityError):
    """Raised when a recognized identity is not authorized for CLOSED_35 production."""


def _raw_text(value: Any) -> str:
    return str(value or "").strip()


def _nfc(value: Any) -> str:
    return unicodedata.normalize("NFC", _raw_text(value))


def _ascii_fold(value: Any) -> str:
    text = unicodedata.normalize("NFKD", _nfc(value))
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _identity_token(value: Any) -> str:
    text = _ascii_fold(value).casefold().strip()
    if text in {"", "nan", "none", "null", "unknown", "unresolved"}:
        return ""
    return re.sub(r"[^a-z0-9]+", "", text)


def _compat_token(value: Any) -> str:
    text = _ascii_fold(value).lower().strip()
    if text in {"", "nan", "none", "null", "unknown", "unresolved"}:
        return ""
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


@dataclass(frozen=True)
class SourceFamilyIdentity:
    raw_source: str
    canonical_display_source: str
    compatibility_key: str
    source_family_uid: str


@dataclass(frozen=True)
class SourceWaveIdentity:
    raw_source: str
    raw_wave: str
    canonical_display_source: str
    canonical_display_wave: str
    compatibility_source_key: str
    compatibility_wave_key: str
    source_family_uid: str
    wave_uid: str
    governance_state: str
    closed_35_member: bool
    physical_token_version: str

    @property
    def compatibility_key(self) -> str:
        return f"{self.compatibility_source_key}|{self.compatibility_wave_key}"

    @property
    def uid_key(self) -> str:
        return f"{self.source_family_uid}|{self.wave_uid}"

    @property
    def uid_native_physical_token(self) -> str:
        return (
            f"{self.physical_token_version}"
            f"__{self.source_family_uid}__{self.wave_uid}"
        )

    @property
    def production_authorized(self) -> bool:
        return self.closed_35_member and self.governance_state == CLOSED_35

    def as_dict(self) -> dict[str, Any]:
        return {
            "raw_source": self.raw_source,
            "raw_wave": self.raw_wave,
            "canonical_display_source": self.canonical_display_source,
            "canonical_display_wave": self.canonical_display_wave,
            "compatibility_source_key": self.compatibility_source_key,
            "compatibility_wave_key": self.compatibility_wave_key,
            "compatibility_key": self.compatibility_key,
            "source_family_uid": self.source_family_uid,
            "wave_uid": self.wave_uid,
            "uid_key": self.uid_key,
            "governance_state": self.governance_state,
            "closed_35_member": self.closed_35_member,
            "production_authorized": self.production_authorized,
            "physical_token_version": self.physical_token_version,
            "uid_native_physical_token": self.uid_native_physical_token,
        }


@dataclass(frozen=True)
class _IdentityRegistry:
    registry_id: str
    schema_version: str
    uid_namespace_version: str
    physical_token_version: str
    source_alias_index: dict[str, dict[str, Any]]
    source_uid_index: dict[str, dict[str, Any]]
    wave_alias_index: dict[str, dict[str, dict[str, Any]]]
    wave_uid_index: dict[str, dict[str, Any]]
    closed_35_pairs: frozenset[tuple[str, str]]


@lru_cache(maxsize=4)
def load_identity_registry(path: str | Path | None = None) -> _IdentityRegistry:
    registry_path = Path(path).expanduser().resolve() if path else DEFAULT_IDENTITY_REGISTRY_PATH
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    families = payload.get("source_families") or []
    if not isinstance(families, list) or not families:
        raise SourceWaveIdentityError(f"identity registry has no source_families: {registry_path}")

    source_alias_index: dict[str, dict[str, Any]] = {}
    source_uid_index: dict[str, dict[str, Any]] = {}
    wave_alias_index: dict[str, dict[str, dict[str, Any]]] = {}
    wave_uid_index: dict[str, dict[str, Any]] = {}
    closed_pairs: set[tuple[str, str]] = set()

    for family in families:
        source_uid = _raw_text(family.get("source_family_uid"))
        source_key = _raw_text(family.get("compatibility_key"))
        display_source = _raw_text(family.get("canonical_display_source"))
        if not source_uid or not source_key or not display_source:
            raise SourceWaveIdentityError("identity registry contains incomplete source family")
        if source_uid in source_uid_index:
            raise SourceWaveIdentityError(f"duplicate source_family_uid: {source_uid}")
        source_uid_index[source_uid] = family
        aliases = list(family.get("aliases") or []) + [display_source, source_key]
        for alias in aliases:
            token = _identity_token(alias)
            if not token:
                continue
            existing = source_alias_index.get(token)
            if existing is not None and existing.get("source_family_uid") != source_uid:
                raise SourceWaveIdentityError(f"ambiguous source alias: {alias!r}")
            source_alias_index[token] = family

        family_wave_index: dict[str, dict[str, Any]] = {}
        for wave in family.get("waves") or []:
            wave_uid = _raw_text(wave.get("wave_uid"))
            display_wave = _raw_text(wave.get("canonical_display_wave"))
            compatibility_wave = _raw_text(wave.get("compatibility_key"))
            state = _raw_text(wave.get("governance_state"))
            member = bool(wave.get("closed_35_member"))
            if not wave_uid or not display_wave or not compatibility_wave or not state:
                raise SourceWaveIdentityError(
                    f"identity registry contains incomplete wave for {display_source}"
                )
            if wave_uid in wave_uid_index:
                raise SourceWaveIdentityError(f"duplicate wave_uid: {wave_uid}")
            if member and state != CLOSED_35:
                raise SourceWaveIdentityError(
                    f"CLOSED_35 member {display_source}/{display_wave} has state={state}"
                )
            if state == CLOSED_35 and not member:
                raise SourceWaveIdentityError(
                    f"CLOSED_35 state without membership: {display_source}/{display_wave}"
                )
            record = dict(wave)
            record["_family"] = family
            wave_uid_index[wave_uid] = record
            aliases = list(wave.get("aliases") or []) + [display_wave, compatibility_wave]
            for alias in aliases:
                token = _identity_token(alias)
                if not token:
                    continue
                existing = family_wave_index.get(token)
                if existing is not None and existing.get("wave_uid") != wave_uid:
                    raise SourceWaveIdentityError(
                        f"ambiguous wave alias within {display_source}: {alias!r}"
                    )
                family_wave_index[token] = record
            if member:
                closed_pairs.add((source_uid, wave_uid))
        wave_alias_index[source_uid] = family_wave_index

    expected_count = int(payload.get("production_member_count") or 0)
    if expected_count != 35 or len(closed_pairs) != expected_count:
        raise SourceWaveIdentityError(
            f"CLOSED_35 registry count mismatch: declared={expected_count} actual={len(closed_pairs)}"
        )

    return _IdentityRegistry(
        registry_id=_raw_text(payload.get("registry_id")),
        schema_version=_raw_text(payload.get("schema_version")),
        uid_namespace_version=_raw_text(payload.get("uid_namespace_version")),
        physical_token_version=_raw_text(payload.get("physical_token_version")),
        source_alias_index=source_alias_index,
        source_uid_index=source_uid_index,
        wave_alias_index=wave_alias_index,
        wave_uid_index=wave_uid_index,
        closed_35_pairs=frozenset(closed_pairs),
    )


def resolve_source_family_identity(
    source: Any,
    *,
    registry_path: str | Path | None = None,
) -> SourceFamilyIdentity:
    raw = _raw_text(source)
    registry = load_identity_registry(registry_path)
    family = registry.source_alias_index.get(_identity_token(raw))
    if family is None:
        raise UnknownSourceFamilyError(f"unrecognized source family: {raw!r}")
    return SourceFamilyIdentity(
        raw_source=raw,
        canonical_display_source=_raw_text(family["canonical_display_source"]),
        compatibility_key=_raw_text(family["compatibility_key"]),
        source_family_uid=_raw_text(family["source_family_uid"]),
    )


def resolve_source_wave_identity(
    source: Any,
    wave: Any,
    *,
    require_closed_35: bool = False,
    registry_path: str | Path | None = None,
) -> SourceWaveIdentity:
    source_identity = resolve_source_family_identity(source, registry_path=registry_path)
    raw_wave = _raw_text(wave)
    if not raw_wave:
        raise UnknownSourceWaveError(
            f"wave is blank for source family {source_identity.canonical_display_source}"
        )
    registry = load_identity_registry(registry_path)
    wave_record = registry.wave_alias_index[source_identity.source_family_uid].get(
        _identity_token(raw_wave)
    )
    if wave_record is None:
        raise UnknownSourceWaveError(
            "unrecognized source-family/wave combination: "
            f"{source_identity.canonical_display_source!r}/{raw_wave!r}"
        )
    identity = SourceWaveIdentity(
        raw_source=source_identity.raw_source,
        raw_wave=raw_wave,
        canonical_display_source=source_identity.canonical_display_source,
        canonical_display_wave=_raw_text(wave_record["canonical_display_wave"]),
        compatibility_source_key=source_identity.compatibility_key,
        compatibility_wave_key=_raw_text(wave_record["compatibility_key"]),
        source_family_uid=source_identity.source_family_uid,
        wave_uid=_raw_text(wave_record["wave_uid"]),
        governance_state=_raw_text(wave_record["governance_state"]),
        closed_35_member=bool(wave_record["closed_35_member"]),
        physical_token_version=registry.physical_token_version,
    )
    if require_closed_35 and not identity.production_authorized:
        raise ProductionMembershipError(
            f"recognized identity is not a CLOSED_35 production member: "
            f"{identity.canonical_display_source}/{identity.canonical_display_wave}"
        )
    return identity


def resolve_wave_identity(
    wave: Any,
    *,
    source_family: Any | None = None,
    require_closed_35: bool = False,
    registry_path: str | Path | None = None,
) -> SourceWaveIdentity:
    if source_family is None or not _raw_text(source_family):
        raise GlobalWaveResolutionError(
            f"global bare-wave resolution is forbidden: {_raw_text(wave)!r}; "
            "resolve source family first"
        )
    return resolve_source_wave_identity(
        source_family,
        wave,
        require_closed_35=require_closed_35,
        registry_path=registry_path,
    )


def closed_35_identities(
    *,
    registry_path: str | Path | None = None,
) -> tuple[SourceWaveIdentity, ...]:
    registry = load_identity_registry(registry_path)
    out: list[SourceWaveIdentity] = []
    for family in registry.source_uid_index.values():
        for wave in family.get("waves") or []:
            if not bool(wave.get("closed_35_member")):
                continue
            out.append(
                resolve_source_wave_identity(
                    family["canonical_display_source"],
                    wave["canonical_display_wave"],
                    require_closed_35=True,
                    registry_path=registry_path,
                )
            )
    return tuple(sorted(out, key=lambda item: (item.source_family_uid, item.wave_uid)))


# ---------------------------------------------------------------------------
# Compatibility surface
#
# These functions intentionally preserve the historical ddm_survey_identity
# key grammar.  They are not production-authorization APIs.
# ---------------------------------------------------------------------------

_FAMILY_ALIASES = {
    "gss": "gss",
    "general_social_survey": "gss",
    "wvs": "wvs",
    "world_values_survey": "wvs",
    "evs": "evs",
    "european_values_study": "evs",
    "afrobarometer": "afrobarometer",
    "afro_barometer": "afrobarometer",
    "arabbarometer": "arab_barometer",
    "arab_barometer": "arab_barometer",
    "asianbarometer": "asian_barometer",
    "asian_barometer": "asian_barometer",
    "asian_barometer_survey": "asian_barometer",
    "latinobarometer": "latinobarometro",
    "latinobar_metro": "latinobarometro",
    "latinobarometro": "latinobarometro",
    "lits": "lits",
    "life_in_transition_survey": "lits",
    "southasia": "south_asia",
    "south_asia": "south_asia",
    "south_asia_barometer": "south_asia",
}
_FAMILY_LABELS = {
    "gss": "GSS",
    "wvs": "WVS",
    "evs": "EVS",
    "afrobarometer": "Afrobarometer",
    "arab_barometer": "Arab Barometer",
    "asian_barometer": "Asian Barometer",
    "latinobarometro": "Latinobarómetro",
    "lits": "LiTS",
    "south_asia": "South Asia",
}
_ARAB_ROMAN_BY_NUMBER = {
    "1": "I", "2": "II", "3": "III", "4": "IV", "5": "V", "6": "VI",
    "7": "VII", "8": "VIII", "9": "IX", "10": "X", "11": "XI", "12": "XII",
}
_EVS_WAVE_BY_YEAR = {
    "1981": "W1", "1990": "W2", "1999": "W3", "2008": "W4", "2017": "W5",
}
_EVS_YEAR_BY_WAVE = {wave: year for year, wave in _EVS_WAVE_BY_YEAR.items()}
_ROMAN_VALUES = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6,
    "VII": 7, "VIII": 8, "IX": 9, "X": 10, "XI": 11, "XII": 12,
}


def compatibility_family_key(value: Any) -> str:
    token = _compat_token(value)
    return _FAMILY_ALIASES.get(token, token)


def compatibility_family_label(value: Any) -> str:
    key = compatibility_family_key(value)
    return _FAMILY_LABELS.get(key, _raw_text(value))


def compatibility_wave_key(survey_family: Any, value: Any) -> str:
    family = compatibility_family_key(survey_family)
    raw = _raw_text(value)
    if not raw:
        return ""
    compact = re.sub(r"[^A-Za-z0-9]+", "", raw).upper()

    if family == "arab_barometer":
        number = ""
        if compact.startswith("WAVE"):
            number = compact[4:]
        elif compact.startswith("W") and compact[1:].isdigit():
            number = compact[1:]
        elif compact.isdigit():
            number = compact
        elif compact in _ROMAN_VALUES:
            return compact
        if number in _ARAB_ROMAN_BY_NUMBER:
            return _ARAB_ROMAN_BY_NUMBER[number]

    if family == "evs":
        if compact in _EVS_WAVE_BY_YEAR:
            return _EVS_WAVE_BY_YEAR[compact]
        if compact in _EVS_YEAR_BY_WAVE:
            return compact
        if compact.startswith("WAVE") and compact[4:].isdigit():
            return f"W{compact[4:]}"

    if compact.startswith("ROUND") and compact[5:].isdigit():
        return f"ROUND{int(compact[5:])}"
    if compact.startswith("R") and compact[1:].isdigit():
        return f"ROUND{int(compact[1:])}"
    if compact.startswith("WAVE") and compact[4:].isdigit():
        return f"W{int(compact[4:])}"
    if compact.startswith("W") and compact[1:].isdigit():
        return f"W{int(compact[1:])}"
    return compact


def compatibility_wave_aliases(survey_family: Any, value: Any) -> list[str]:
    family = compatibility_family_key(survey_family)
    canonical = compatibility_wave_key(family, value)
    if not canonical:
        return []
    aliases: list[str] = [canonical]
    if family == "arab_barometer":
        reverse = {roman: number for number, roman in _ARAB_ROMAN_BY_NUMBER.items()}
        number = reverse.get(canonical)
        if number:
            aliases.extend([f"W{number}", number, f"WAVE{number}"])
    elif family == "evs":
        year = _EVS_YEAR_BY_WAVE.get(canonical)
        if year:
            aliases.extend([year, canonical.replace("W", "Wave ")])
    elif canonical.startswith("ROUND"):
        number = canonical[5:]
        aliases.extend([f"R{number}", number, f"Round {number}"])
    elif canonical.startswith("W") and canonical[1:].isdigit():
        number = canonical[1:]
        aliases.extend([number, f"Wave {number}"])
    elif canonical in _ROMAN_VALUES:
        aliases.append(str(_ROMAN_VALUES[canonical]))
    else:
        aliases.append(_raw_text(value))

    out: list[str] = []
    seen: set[str] = set()
    for alias in aliases:
        token = _raw_text(alias)
        if token and token.upper() not in seen:
            seen.add(token.upper())
            out.append(token)
    return out


def compatibility_wave_ordinal(survey_family: Any, value: Any) -> int | None:
    canonical = compatibility_wave_key(survey_family, value)
    if not canonical:
        return None
    if canonical.isdigit():
        return int(canonical)
    if canonical.startswith("ROUND") and canonical[5:].isdigit():
        return int(canonical[5:])
    if canonical.startswith("W") and canonical[1:].isdigit():
        return int(canonical[1:])
    return _ROMAN_VALUES.get(canonical)
