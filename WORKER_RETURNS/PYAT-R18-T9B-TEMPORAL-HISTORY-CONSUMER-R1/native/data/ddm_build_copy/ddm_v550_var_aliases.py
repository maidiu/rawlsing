#!/usr/bin/env python3
"""Explicit canonical-to-physical variable aliases for V550.

These are narrow, source-authority-backed mappings for cases where the
canonical packet variable name differs from the physical microdata column
name, or where a canonical multiselect parent is represented by physical
child columns.
"""

from __future__ import annotations

import re
from typing import Any

from data.ddm_build_copy.ddm_v550_family_overlay import canonical_family_key, canonical_wave_key

LATINOBAROMETRO_PHYSICAL_ALIASES: dict[tuple[str, str], list[str]] = {
    ("2011", "P3ST_A"): ["P3ST.A"],
    ("2011", "P11ST_A"): ["P11ST.A"],
    ("2024", "Q1ST"): ["P1ST"],
    ("2024", "Q12STGBSA"): ["P12STGBS.A"],
    ("2024", "Q2NCV"): [f"P2NCV.{idx}" for idx in range(1, 13)],
    ("2024", "Q9NCV"): [f"P9NCV.{idx}" for idx in range(1, 9)],
}


def _clean(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return "" if text.lower() in {"", "nan", "none"} else text


def _alias_key(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", _clean(value).lower())


_REVERSE_LATINOBAROMETRO_ALIAS_LOOKUP: dict[tuple[str, str, str], str] = {}
for (wave_key, canonical_var_name), physical_names in LATINOBAROMETRO_PHYSICAL_ALIASES.items():
    for physical_name in physical_names:
        _REVERSE_LATINOBAROMETRO_ALIAS_LOOKUP[(canonical_family_key("Latinobarómetro"), wave_key, _alias_key(physical_name))] = canonical_var_name


def resolve_question_var_aliases(source: Any, wave: Any, canonical_var_code: Any) -> dict[str, Any]:
    """Return explicit alias metadata for a canonical question variable.

    The returned payload always includes the canonical variable name and a
    list of physical/source variable names that should be queried or matched.
    """
    source_key = canonical_family_key(source)
    wave_key = canonical_wave_key(source_key or source, wave)
    requested_var_name = _clean(canonical_var_code).upper()
    canonical_var_name = requested_var_name
    physical_names: list[str] = []
    mapping_type = "identity"

    if source_key == "latinobarometro":
        canonical_match = (wave_key, requested_var_name)
        if canonical_match in LATINOBAROMETRO_PHYSICAL_ALIASES:
            canonical_var_name = requested_var_name
            physical_names = [alias for alias in LATINOBAROMETRO_PHYSICAL_ALIASES[canonical_match] if _clean(alias)]
            mapping_type = "explicit_multiselect_children" if len(physical_names) > 1 else "explicit_alias"
        else:
            reverse_key = (source_key, wave_key, _alias_key(requested_var_name))
            reverse_canonical = _REVERSE_LATINOBAROMETRO_ALIAS_LOOKUP.get(reverse_key)
            if reverse_canonical:
                canonical_var_name = reverse_canonical
                physical_names = [alias for alias in LATINOBAROMETRO_PHYSICAL_ALIASES.get((wave_key, canonical_var_name), []) if _clean(alias)]
                mapping_type = "explicit_multiselect_children" if len(physical_names) > 1 else "explicit_alias"

    if physical_names:
        source_var_name = " | ".join(physical_names)
    else:
        source_var_name = canonical_var_name
        physical_names = [canonical_var_name] if canonical_var_name else []

    query_var_codes: list[str] = []
    for candidate in [canonical_var_name, *physical_names]:
        candidate = _clean(candidate).upper()
        if candidate and candidate not in query_var_codes:
            query_var_codes.append(candidate)

    return {
        "source_family": source_key or _clean(source),
        "canonical_wave": wave_key or _clean(wave),
        "canonical_var_name": canonical_var_name,
        "source_var_name": source_var_name,
        "source_var_names": physical_names,
        "source_mapping_type": mapping_type,
        "source_mapping_authority": "question_structural_mapping",
        "query_var_codes": query_var_codes,
        "alias_key_variants": [_alias_key(value) for value in query_var_codes if _clean(value)],
    }


def question_var_code_variants(source: Any, wave: Any, canonical_var_code: Any) -> list[str]:
    """Return canonical and physical variable codes for row lookup."""
    resolved = resolve_question_var_aliases(source, wave, canonical_var_code)
    out: list[str] = []
    for value in [resolved["canonical_var_name"], *resolved["source_var_names"]]:
        text = _clean(value).upper()
        if text and text not in out:
            out.append(text)
    return out
