from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception:
    yaml = None

REPO_ROOT = Path(__file__).resolve().parent.parent
FACTBOOK_COUNTRY_PATH = REPO_ROOT / "factbook-out" / "country_cdf1.json"

def _load_joshua_project_codes() -> dict[str, str]:
    path = Path(__file__).resolve().parent / "joshua_project_codes.yaml"
    if yaml and path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                return {str(k): str(v) for k, v in (yaml.safe_load(f) or {}).items()}
        except Exception:
            pass
    return {}

_JOSHUA_PROJECT_CODES: dict[str, str] = _load_joshua_project_codes()

try:
    import pycountry
except Exception:  # pragma: no cover - optional fallback
    pycountry = None  # type: ignore


def _extract_raw_country(country_ref: Any) -> str:
    if isinstance(country_ref, dict):
        for key in (
            "iso2",
            "country_code",
            "country",
            "code",
            "iso3",
            "name",
            "canonical_name",
        ):
            value = country_ref.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return ""
    if country_ref is None:
        return ""
    return str(country_ref).strip()


def _country_input_kind(raw: str) -> str:
    if not raw:
        return "empty"
    compact = raw.strip()
    if len(compact) == 2 and compact.isalpha():
        return "iso2"
    if len(compact) == 3 and compact.isalpha():
        return "iso3"
    return "name"


@lru_cache(maxsize=1)
def _factbook_index() -> dict[str, Any]:
    records = []
    try:
        records = json.loads(FACTBOOK_COUNTRY_PATH.read_text(encoding="utf-8"))
    except Exception:
        records = []

    by_iso2: dict[str, dict[str, Any]] = {}
    by_iso3: dict[str, dict[str, Any]] = {}
    by_name: dict[str, dict[str, Any]] = {}

    for record in records:
        if not isinstance(record, dict):
            continue
        iso2 = str(record.get("code") or "").strip().upper()
        name = str(record.get("name") or "").strip()
        survey = record.get("survey") if isinstance(record.get("survey"), dict) else {}
        if iso2 and len(iso2) == 2:
            # Preserve the first record we see for a code so accidental duplicate
            # rows do not silently overwrite the earlier canonical mapping.
            by_iso2.setdefault(iso2, record)
        if name:
            by_name.setdefault(name.casefold(), record)
        if pycountry and iso2 and len(iso2) == 2:
            try:
                country = pycountry.countries.get(alpha_2=iso2)
            except Exception:
                country = None
            if country:
                by_iso3.setdefault(country.alpha_3.upper(), record)
                for alias in {
                    getattr(country, "name", "") or "",
                    getattr(country, "official_name", "") or "",
                    getattr(country, "common_name", "") or "",
                }:
                    alias = alias.strip()
                    if alias:
                        by_name.setdefault(alias.casefold(), record)
    return {
        "by_iso2": by_iso2,
        "by_iso3": by_iso3,
        "by_name": by_name,
    }


def _pycountry_lookup(raw: str):
    if not raw or not pycountry:
        return None
    try:
        return pycountry.countries.lookup(raw)
    except Exception:
        return None


def _build_result(
    *,
    raw_input: str,
    input_kind: str,
    canonical_name: str,
    iso2: str = "",
    iso3: str = "",
    resolved_via: str,
    factbook_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    survey = {}
    external_codes: dict[str, Any] = {}
    if isinstance(factbook_record, dict):
        survey = dict(factbook_record.get("survey") or {})
        canonical = str(factbook_record.get("code") or "").strip().upper()
        cia = str(factbook_record.get("cia") or "").strip().lower()
        survey_countries = survey.get("countries") if isinstance(survey, dict) else []
        proxy_targets = [
            str(code or "").strip().upper()
            for code in (survey_countries or [])
            if str(code or "").strip().upper() and str(code or "").strip().upper() != canonical
        ]
        external_codes = {
            "geonames": iso2 or canonical,
            "survey": iso2 or canonical,
            "history": canonical_name or raw_input,
            "factbook": cia or (iso2 or canonical).lower(),
            "survey_pool": [iso2 or canonical] if (iso2 or canonical) else [],
            "survey_proxy_targets": proxy_targets,
        }
        if iso3 or iso2:
            external_codes["epr"] = iso3 or iso2
    return {
        "input": raw_input,
        "input_kind": input_kind,
        "iso2": iso2,
        "iso3": iso3,
        "canonical_name": canonical_name,
        "resolved_via": resolved_via,
        "fallback_used": resolved_via not in ("factbook", "pycountry->factbook"),
        "survey": survey,
        "external_codes": external_codes,
        "factbook_record": factbook_record or {},
    }


def normalize_country_ref(country_ref: Any) -> dict[str, Any]:
    """
    Normalize an ISO2 code, ISO3 code, or display name to a canonical country reference.

    The factbook country file is the primary naming authority. pycountry is used only as a
    deterministic conversion helper when the factbook index cannot resolve the input directly.
    """
    raw = _extract_raw_country(country_ref)
    input_kind = _country_input_kind(raw)
    if not raw:
        return _build_result(
            raw_input="",
            input_kind="empty",
            canonical_name="",
            resolved_via="original",
        )

    index = _factbook_index()
    by_iso2 = index["by_iso2"]
    by_iso3 = index["by_iso3"]
    by_name = index["by_name"]
    raw_upper = raw.upper()
    raw_name_key = raw.casefold()

    record = None
    if input_kind == "iso2":
        record = by_iso2.get(raw_upper)
    elif input_kind == "iso3":
        record = by_iso3.get(raw_upper)
        if not record:
            pc = _pycountry_lookup(raw_upper)
            if pc:
                record = by_iso2.get(getattr(pc, "alpha_2", "").upper())
    else:
        record = by_name.get(raw_name_key)

    if record:
        iso2 = str(record.get("code") or "").strip().upper()
        canonical_name = str(record.get("name") or "").strip() or raw
        iso3 = ""
        if pycountry and iso2:
            try:
                pc = pycountry.countries.get(alpha_2=iso2)
            except Exception:
                pc = None
            if pc:
                iso3 = getattr(pc, "alpha_3", "") or ""
        return _build_result(
            raw_input=raw,
            input_kind=input_kind,
            canonical_name=canonical_name,
            iso2=iso2,
            iso3=iso3,
            resolved_via="factbook",
            factbook_record=record,
        )

    pc = _pycountry_lookup(raw)
    if pc:
        iso2 = getattr(pc, "alpha_2", "") or ""
        iso3 = getattr(pc, "alpha_3", "") or ""
        if iso2 and iso2.upper() in by_iso2:
            record = by_iso2[iso2.upper()]
            canonical_name = str(record.get("name") or "").strip() or getattr(pc, "name", raw)
            return _build_result(
                raw_input=raw,
                input_kind=input_kind,
                canonical_name=canonical_name,
                iso2=iso2.upper(),
                iso3=iso3.upper(),
                resolved_via="pycountry->factbook",
                factbook_record=record,
            )
        canonical_name = getattr(pc, "name", raw)
        return _build_result(
            raw_input=raw,
            input_kind=input_kind,
            canonical_name=canonical_name,
            iso2=iso2.upper(),
            iso3=iso3.upper(),
            resolved_via="pycountry",
        )

    # Deterministic fallback: preserve the original token.
    return _build_result(
        raw_input=raw,
        input_kind=input_kind,
        canonical_name=raw,
        resolved_via="original",
    )


class UnresolvedCountryError(ValueError):
    """Raised when a country reference cannot be resolved to a canonical authority."""


def require_country_ref(country_ref: Any, *, allow_subnational: bool = False) -> dict[str, Any]:
    result = normalize_country_ref(country_ref)
    if result.get("resolved_via") == "original" and not result.get("canonical_name"):
        raise UnresolvedCountryError(f"Cannot resolve country: {country_ref!r}")
    if not allow_subnational:
        raw = _extract_raw_country(country_ref).upper()
        if raw == "NIR":
            raise UnresolvedCountryError("Cannot generate identity for subnational unit: 'NIR'")
    return result


def code_for_system(country_ref: Any, system: str) -> str:
    """
    Return the code/identifier used by a downstream system.

    system: 'geonames' | 'joshua_project' | 'factbook' | 'epr' | 'survey' | 'history' | 'iso2' | 'iso3'
    """
    result = normalize_country_ref(country_ref)
    iso2 = str(result.get("iso2") or "").strip().upper()
    iso3 = str(result.get("iso3") or "").strip().upper()
    canonical_name = str(result.get("canonical_name") or "").strip()
    external = dict(result.get("external_codes") or {})
    system_key = (system or "").strip().lower()

    if system_key == "iso2":
        return iso2
    if system_key == "iso3":
        return iso3 or iso2
    if system_key in {"geonames", "survey"}:
        return str(external.get(system_key) or iso2)
    if system_key == "history":
        return str(external.get("history") or canonical_name or iso3 or iso2)
    if system_key == "factbook":
        return str(external.get("factbook") or iso2.lower())
    if system_key == "epr":
        return str(external.get("epr") or iso3 or iso2)
    if system_key == "joshua_project":
        return str(external.get("joshua_project") or _JOSHUA_PROJECT_CODES.get(iso3 or iso2 or "", iso2))
    return str(external.get(system_key) or iso2 or iso3 or canonical_name)
