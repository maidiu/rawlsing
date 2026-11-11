#!/usr/bin/env python3
"""Resolve the governed respondent-long relation used by V550.

The live host can expose both a historical facet-ready view and a later
authority-enriched view.  The bounded nine-source database contract already
prefers the authority view, but the V550 shard launcher historically defaulted
to the older view.  This module makes the selection explicit, validated, and
shared by the launcher and its tests.
"""
from __future__ import annotations

import re
from typing import Any, Iterable

import pandas as pd

from data.ddm_build_copy.ddm_survey_identity import family_keys_equal, waves_equivalent

RELATION_IDENTIFIER_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?$"
)
AUTO_RESPONSE_RELATION = "auto"
DEFAULT_RESPONSE_RELATION_CANDIDATES = (
    "public.v_ddm_response_long_facet_ready_authority",
    "public.v_ddm_response_long_facet_ready",
)
REQUIRED_RESPONSE_RELATION_COLUMNS = {
    "respondent_id",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "var_code",
}


def validate_relation_identifier(value: str) -> str:
    relation = str(value or "").strip()
    if not RELATION_IDENTIFIER_RE.fullmatch(relation):
        raise ValueError(f"invalid respondent relation identifier: {value!r}")
    return relation


def choose_response_relation(
    available_relations: Iterable[str],
    requested: str | None = AUTO_RESPONSE_RELATION,
) -> str:
    """Choose one relation deterministically from a discovered relation set."""
    available = {str(value).strip() for value in available_relations if str(value).strip()}
    requested_text = str(requested or AUTO_RESPONSE_RELATION).strip()
    if requested_text and requested_text.lower() != AUTO_RESPONSE_RELATION:
        explicit = validate_relation_identifier(requested_text)
        explicit_variants = {explicit, explicit.removeprefix("public."), f"public.{explicit}" if "." not in explicit else explicit}
        matches = sorted(available & explicit_variants)
        if not matches:
            raise RuntimeError(
                f"[V550_RESPONSE_RELATION_MISSING] Explicit respondent relation {explicit!r} does not exist; "
                f"available={sorted(available)}"
            )
        chosen = matches[0]
        return chosen if "." in chosen else f"public.{chosen}"

    for candidate in DEFAULT_RESPONSE_RELATION_CANDIDATES:
        variants = {candidate, candidate.removeprefix("public.")}
        matches = sorted(available & variants)
        if matches:
            chosen = matches[0]
            return chosen if "." in chosen else f"public.{chosen}"
    raise RuntimeError(
        "[V550_RESPONSE_RELATION_MISSING] Neither authority-enriched nor historical facet-ready respondent relation exists"
    )


def _relation_parts(relation: str) -> tuple[str, str]:
    validated = validate_relation_identifier(relation)
    if "." in validated:
        return tuple(validated.split(".", 1))  # type: ignore[return-value]
    return "public", validated


def discover_response_relations(conn: Any) -> set[str]:
    rows = pd.read_sql_query(
        """
        SELECT table_schema, table_name
        FROM information_schema.views
        WHERE table_name IN (
            'v_ddm_response_long_facet_ready_authority',
            'v_ddm_response_long_facet_ready'
        )
        ORDER BY table_schema, table_name
        """,
        conn,
    )
    if rows.empty:
        return set()
    return {
        f"{str(row.table_schema)}.{str(row.table_name)}"
        for row in rows.itertuples(index=False)
    }


def relation_columns(conn: Any, relation: str) -> set[str]:
    schema, table = _relation_parts(relation)
    rows = pd.read_sql_query(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = %(schema)s
          AND table_name = %(table)s
        ORDER BY ordinal_position
        """,
        conn,
        params={"schema": schema, "table": table},
    )
    return set(rows["column_name"].astype(str).tolist()) if not rows.empty else set()


def resolve_response_relation(conn: Any, requested: str | None = AUTO_RESPONSE_RELATION) -> dict[str, Any]:
    available = discover_response_relations(conn)
    relation = choose_response_relation(available, requested)
    columns = relation_columns(conn, relation)
    missing = sorted(REQUIRED_RESPONSE_RELATION_COLUMNS - columns)
    if missing:
        raise RuntimeError(
            f"[V550_RESPONSE_RELATION_CONTRACT] {relation} is missing required columns: {missing}"
        )
    return {
        "relation": relation,
        "requested": str(requested or AUTO_RESPONSE_RELATION),
        "available_relations": sorted(available),
        "columns": sorted(columns),
        "missing_columns": missing,
        "selection_mode": "explicit" if str(requested or "").strip().lower() not in {"", AUTO_RESPONSE_RELATION} else "auto_prefer_authority",
    }


def scope_manifest_from_response_rows(
    rows: pd.DataFrame,
    *,
    requested_source: str,
    requested_wave: str,
    countries: Iterable[str] = (),
) -> pd.DataFrame:
    """Normalize a response-relation scope probe to the requested identity."""
    expected = ["source", "wave", "country_code", "respondents"]
    if rows is None or rows.empty:
        return pd.DataFrame(columns=expected)
    frame = rows.copy()
    for column in ("source", "wave", "canonical_wave", "country_code"):
        if column not in frame.columns:
            frame[column] = ""
        frame[column] = frame[column].fillna("").astype(str)
    country_set = {str(value).strip().upper() for value in countries if str(value).strip()}
    mask = frame["source"].map(lambda value: family_keys_equal(value, requested_source))
    mask &= frame.apply(
        lambda row: waves_equivalent(requested_source, row.get("wave"), requested_wave)
        or waves_equivalent(requested_source, row.get("canonical_wave"), requested_wave),
        axis=1,
    )
    if country_set:
        mask &= frame["country_code"].str.upper().isin(country_set)
    scoped = frame.loc[mask].copy()
    if scoped.empty:
        return pd.DataFrame(columns=expected)
    respondent_column = "respondents" if "respondents" in scoped.columns else "respondent_count"
    if respondent_column not in scoped.columns:
        scoped[respondent_column] = 0
    scoped["respondents"] = pd.to_numeric(scoped[respondent_column], errors="coerce").fillna(0).astype("int64")
    scoped["source"] = str(requested_source)
    scoped["wave"] = str(requested_wave)
    return (
        scoped[expected]
        .groupby(["source", "wave", "country_code"], as_index=False, dropna=False)["respondents"]
        .sum()
        .sort_values(["source", "wave", "country_code"], kind="mergesort")
        .reset_index(drop=True)
    )


def load_scope_manifest_from_response_relation(
    conn: Any,
    relation: str,
    *,
    requested_source: str,
    requested_wave: str,
    countries: Iterable[str] = (),
) -> pd.DataFrame:
    validated = validate_relation_identifier(relation)
    country_values = [str(value).strip() for value in countries if str(value).strip()]
    where = ""
    params: dict[str, Any] = {}
    if country_values:
        where = "WHERE country_code = ANY(%(countries)s)"
        params["countries"] = country_values
    rows = pd.read_sql_query(
        f"""
        SELECT
            source,
            wave,
            canonical_wave,
            country_code,
            COUNT(DISTINCT respondent_id)::bigint AS respondents
        FROM {validated}
        {where}
        GROUP BY source, wave, canonical_wave, country_code
        ORDER BY source, wave, canonical_wave, country_code
        """,
        conn,
        params=params or None,
    )
    return scope_manifest_from_response_rows(
        rows,
        requested_source=requested_source,
        requested_wave=requested_wave,
        countries=country_values,
    )
