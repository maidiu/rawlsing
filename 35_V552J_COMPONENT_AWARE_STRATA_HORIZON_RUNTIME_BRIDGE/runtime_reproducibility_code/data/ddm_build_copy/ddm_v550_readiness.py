#!/usr/bin/env python3
"""Readiness and scope computation for V550."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os, time
from typing import Any, Iterable

import pandas as pd

from data.ddm_build_copy.ddm_v550_io import clean_text
from data.ddm_build_copy.ddm_v550_metrics import dominant_response
from data.ddm_build_copy.ddm_v550_shared_cache import cached_query_frame, shared_cache_root


POSITION_FIELDS = [
    "sex",
    "age",
    "age_group",
    "education_level",
    "income_level",
    "religion_label",
    "urban_rural",
    "region",
    "ethnicity",
    "language",
    "employment",
    "marital",
    "household_size",
]


def _query_df(conn, sql: str, params: tuple[Any, ...] | None = None) -> pd.DataFrame:
    return pd.read_sql_query(sql, conn, params=params)


def _readiness_log(progress_started: float | None, message: str) -> None:
    if progress_started is None:
        return
    print(f"[v550b +{time.monotonic() - progress_started:0.0f}s] {message}", flush=True)


def _sql_filter_clause(
    source_filters: list[str] | None = None,
    wave_filters: list[str] | None = None,
    country_filters: list[str] | None = None,
    var_filters: list[str] | None = None,
    *,
    source_col: str = "source",
    wave_col: str = "wave",
    country_col: str = "country_code",
) -> tuple[str, dict[str, Any]]:
    clauses = ["TRUE"]
    params: dict[str, Any] = {}
    if source_filters:
        clauses.append(f"{source_col} = ANY(%(sources)s)")
        params["sources"] = source_filters
    if wave_filters:
        clauses.append(f"{wave_col} = ANY(%(waves)s)")
        params["waves"] = wave_filters
    if country_filters:
        clauses.append(f"{country_col} = ANY(%(countries)s)")
        params["countries"] = country_filters
    return " AND ".join(clauses), params


def load_scope_manifest(
    conn,
    source_filters: list[str] | None = None,
    wave_filters: list[str] | None = None,
    country_filters: list[str] | None = None,
    *,
    progress_started: float | None = None,
    log_prefix: str = "load_scope_manifest",
) -> pd.DataFrame:
    if progress_started is not None:
        print(
            f"[v550b +0s] {log_prefix}: filters source={source_filters or []} wave={wave_filters or []} country={country_filters or []}",
            flush=True,
        )
    where_clause, params = _sql_filter_clause(source_filters, wave_filters, country_filters)
    if progress_started is not None:
        print(f"[v550b +0s] {log_prefix}: executing survey_microdata_respondents aggregation", flush=True)
    sql = """
        SELECT source, wave, country_code, COUNT(*) AS respondents
        FROM survey_microdata_respondents
        WHERE {where_clause}
        GROUP BY source, wave, country_code
        ORDER BY source, wave, country_code
    """.format(where_clause=where_clause)

    def _query() -> pd.DataFrame:
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description] if cur.description else ["source", "wave", "country_code", "respondents"]
        finally:
            cur.close()
        if progress_started is not None:
            print(f"[v550b +0s] {log_prefix}: materializing dataframe from {len(rows)} rows", flush=True)
        return pd.DataFrame(rows, columns=columns)

    df = cached_query_frame(
        "scope",
        {
            "query": "survey_microdata_respondents_scope_manifest",
            "source_filters": sorted({str(value) for value in source_filters or [] if str(value).strip()}),
            "wave_filters": sorted({str(value) for value in wave_filters or [] if str(value).strip()}),
            "country_filters": sorted({str(value) for value in country_filters or [] if str(value).strip()}),
        },
        _query,
        cache_root=shared_cache_root(),
        metadata={
            "source_table": "survey_microdata_respondents",
            "source_filters": sorted({str(value) for value in source_filters or [] if str(value).strip()}),
            "wave_filters": sorted({str(value) for value in wave_filters or [] if str(value).strip()}),
            "country_filters": sorted({str(value) for value in country_filters or [] if str(value).strip()}),
        },
    )
    if progress_started is not None:
        print(f"[v550b +0s] {log_prefix}: dataframe materialized", flush=True)
        print(f"[v550b +0s] {log_prefix}: fetched {len(df)} rows", flush=True)
        print(f"[v550b +0s] {log_prefix}: resetting index", flush=True)
    df = df.reset_index(drop=True)
    if progress_started is not None:
        print(f"[v550b +0s] {log_prefix}: returning scope dataframe", flush=True)
    return df


def ensure_live_substrate(conn) -> None:
    # This is a hard gate: the rest of readiness assumes the live substrate exists.
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM respondent_position_fact")
    row = cur.fetchone()
    if row is None or int(row[0] or 0) <= 0:
        raise RuntimeError("[V550_MISSING_RESPONDENT_POSITION_FACT] respondent_position_fact is missing or empty. Run data/ddm_build_copy/apply_postgres_facet_ready_substrate.py before V550.")
    cur.close()


def respondent_position_coverage(conn, scope_df: pd.DataFrame, source_filters: list[str] | None = None, wave_filters: list[str] | None = None, country_filters: list[str] | None = None) -> pd.DataFrame:
    where_clause, params = _sql_filter_clause(source_filters, wave_filters, country_filters, source_col="source_family")
    sql = f"""
        SELECT source_family AS source, wave, country_code,
               {", ".join([f"COUNT(*) FILTER (WHERE {field} IS NOT NULL AND {field}::TEXT <> '') AS {field}_n" for field in POSITION_FIELDS])}
        FROM respondent_position_fact
        WHERE {where_clause}
        GROUP BY source_family, wave, country_code
        ORDER BY source_family, wave, country_code
    """
    df = _query_df(conn, sql, params=params)
    return df


def weight_coverage(conn, source_filters: list[str] | None = None, wave_filters: list[str] | None = None) -> pd.DataFrame:
    where_clause, params = _sql_filter_clause(source_filters, wave_filters, None)
    sql = """
        SELECT source, wave, COUNT(*) AS weight_rows,
               COUNT(*) FILTER (WHERE is_primary) AS primary_weight_rows,
               COUNT(DISTINCT respondent_id) AS respondents_with_weights,
               COUNT(DISTINCT weight_name) AS distinct_weight_names
        FROM survey_weight_fact
        WHERE {where_clause}
        GROUP BY source, wave
        ORDER BY source, wave
    """.format(where_clause=where_clause)
    return _query_df(conn, sql, params=params)


def mapping_status_coverage(conn, source_filters: list[str] | None = None, wave_filters: list[str] | None = None) -> pd.DataFrame:
    from data.ddm_build_copy.ddm_v550_family_overlay import wave_aliases, waves_equivalent
    from data.ddm_build_copy.ddm_v550_shared_cache import question_structural_mapping_select_columns

    requested_sources = [str(value) for value in source_filters or [] if str(value).strip()]
    requested_waves = [str(value) for value in wave_filters or [] if str(value).strip()]
    query_waves = list(requested_waves)
    if len(requested_sources) == 1:
        for wave in requested_waves:
            query_waves.extend(wave_aliases(requested_sources[0], wave))
    query_waves = list(dict.fromkeys(value for value in query_waves if str(value).strip()))

    where_clause, params = _sql_filter_clause(source_filters, query_waves, None)
    select_columns = question_structural_mapping_select_columns(conn)

    def _query() -> pd.DataFrame:
        qsm_relation = os.getenv("DDM_QSM_RELATION", "question_structural_mapping")
        sql = """
            SELECT {columns}
            FROM {qsm_relation}
            WHERE {where_clause}
            ORDER BY source, wave, var_code, loaded_at DESC
        """.format(qsm_relation=qsm_relation, columns=", ".join(select_columns), where_clause=where_clause)
        return _query_df(conn, sql, params=params)

    raw = cached_query_frame(
        "mapping",
        {
            "query": "question_structural_mapping_slice",
            "source_filters": sorted({str(value) for value in source_filters or [] if str(value).strip()}),
            "wave_filters": sorted({str(value) for value in query_waves if str(value).strip()}),
            "requested_wave_filters": sorted({str(value) for value in requested_waves if str(value).strip()}),
            "select_columns": select_columns,
        },
        _query,
        cache_root=shared_cache_root(),
        metadata={
            "source_table": "question_structural_mapping",
            "source_filters": sorted({str(value) for value in source_filters or [] if str(value).strip()}),
            "wave_filters": sorted({str(value) for value in query_waves if str(value).strip()}),
            "requested_wave_filters": sorted({str(value) for value in requested_waves if str(value).strip()}),
            "select_columns": select_columns,
        },
    )
    if raw.empty:
        return pd.DataFrame(columns=["source", "wave", "mapping_rows", "mapped_rows", "facet_rows", "legacy_leak_rows"])
    enriched = raw.assign(
        mapping_status_nonempty=raw["mapping_status"].fillna("").astype(str).str.strip().ne(""),
        driver_facet_nonempty=raw["driver_facet_id"].fillna("").astype(str).str.strip().ne(""),
        legacy_leak_nonempty=raw["legacy_final_driver_id"].fillna("").astype(str).str.strip().ne(""),
        driver_facet_blank=raw["driver_facet_id"].fillna("").astype(str).str.strip().eq(""),
    )
    grouped = (
        enriched.groupby(["source", "wave"], dropna=False)
        .agg(
            mapping_rows=("source", "size"),
            mapped_rows=("mapping_status_nonempty", "sum"),
            facet_rows=("driver_facet_nonempty", "sum"),
            legacy_leak_rows=("legacy_leak_nonempty", lambda s: int((s & enriched.loc[s.index, "driver_facet_blank"]).sum())),
        )
        .reset_index()
    )
    if len(requested_sources) == 1 and len(requested_waves) == 1:
        source = requested_sources[0]
        requested_wave = requested_waves[0]
        equivalent = grouped["wave"].map(lambda value: waves_equivalent(source, value, requested_wave))
        grouped.loc[equivalent, "wave"] = requested_wave
        grouped = (
            grouped.groupby(["source", "wave"], dropna=False, as_index=False)[
                ["mapping_rows", "mapped_rows", "facet_rows", "legacy_leak_rows"]
            ]
            .sum()
        )
    return grouped.sort_values(["source", "wave"]).reset_index(drop=True)


def response_coverage(
    conn,
    filters: dict[str, list[str]] | None = None,
    *,
    progress_started: float | None = None,
    log_prefix: str = "response_coverage",
) -> pd.DataFrame:
    source_filters = (filters or {}).get("source", [])
    wave_filters = (filters or {}).get("canonical_wave", [])
    country_filters = (filters or {}).get("country_code", [])
    var_filters = (filters or {}).get("var_code", [])

    where_parts = ["TRUE"]
    params: dict[str, Any] = {}
    if source_filters:
        where_parts.append("source = ANY(%(sources)s)")
        params["sources"] = source_filters
    if wave_filters:
        where_parts.append("canonical_wave = ANY(%(waves)s)")
        params["waves"] = wave_filters
    if country_filters:
        where_parts.append("country_code = ANY(%(countries)s)")
        params["countries"] = country_filters
    if var_filters:
        where_parts.append("var_code = ANY(%(var_codes)s)")
        params["var_codes"] = var_filters
    where_clause = " AND ".join(where_parts)
    resp_relation = os.getenv("DDM_RESPONSE_LONG_RELATION", "v_ddm_response_long_facet_ready")
    sql = """
        SELECT
            source,
            canonical_wave AS wave,
            country_code,
            COUNT(DISTINCT respondent_id)::bigint AS respondents_with_responses,
            COUNT(*)::bigint AS response_rows
        FROM {resp_relation}
        WHERE {where_clause}
        GROUP BY source, canonical_wave, country_code
        ORDER BY source, canonical_wave, country_code
    """.format(resp_relation=resp_relation, where_clause=where_clause)
    _readiness_log(
        progress_started,
        f"{log_prefix}: executing aggregate SQL countries={len(country_filters)} vars={len(var_filters)}",
    )
    started = time.monotonic()
    frame = cached_query_frame(
        "response_coverage_aggregate",
        {
            "query": "v_ddm_response_long_facet_ready_aggregate",
            "source_filters": sorted({str(value) for value in source_filters if str(value).strip()}),
            "wave_filters": sorted({str(value) for value in wave_filters if str(value).strip()}),
            "country_filters": sorted({str(value) for value in country_filters if str(value).strip()}),
            "var_filters": sorted({str(value) for value in var_filters if str(value).strip()}),
        },
        lambda: _query_df(conn, sql, params=params).reset_index(drop=True),
        cache_root=shared_cache_root(),
        metadata={
            "source_table": resp_relation,
            "aggregation": "source_canonical_wave_country",
            "source_filters": sorted({str(value) for value in source_filters if str(value).strip()}),
            "wave_filters": sorted({str(value) for value in wave_filters if str(value).strip()}),
            "country_filters": sorted({str(value) for value in country_filters if str(value).strip()}),
            "var_filters": sorted({str(value) for value in var_filters if str(value).strip()}),
        },
    )
    expected = ["source", "wave", "country_code", "respondents_with_responses", "response_rows"]
    if frame.empty:
        return pd.DataFrame(columns=expected)
    for column in expected:
        if column not in frame.columns:
            frame[column] = pd.NA
    frame = frame[expected].copy()
    frame["source"] = frame["source"].fillna("").astype(str)
    frame["wave"] = frame["wave"].fillna("").astype(str)
    frame["country_code"] = frame["country_code"].fillna("").astype(str)
    _readiness_log(
        progress_started,
        f"{log_prefix}: aggregate rows={len(frame)} in {time.monotonic() - started:0.1f}s",
    )
    return frame.reset_index(drop=True)


def build_readiness(
    conn,
    scope_df: pd.DataFrame,
    min_cell_n: int,
    source_filters: list[str] | None = None,
    wave_filters: list[str] | None = None,
    country_filters: list[str] | None = None,
    var_filters: list[str] | None = None,
    *,
    progress_started: float | None = None,
    log_prefix: str = "build_readiness",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    total_steps = 6
    step = 1
    _readiness_log(progress_started, f"{log_prefix}: {step}/{total_steps} checking live substrate")
    ensure_live_substrate(conn)
    step += 1
    pos_started = time.monotonic()
    _readiness_log(progress_started, f"{log_prefix}: {step}/{total_steps} building respondent position coverage")
    pos = respondent_position_coverage(conn, scope_df, source_filters, wave_filters, country_filters)
    _readiness_log(progress_started, f"{log_prefix}: {step}/{total_steps} respondent position coverage rows={len(pos)} in {time.monotonic() - pos_started:0.1f}s")
    step += 1
    weight_started = time.monotonic()
    _readiness_log(progress_started, f"{log_prefix}: {step}/{total_steps} building weight coverage")
    weight = weight_coverage(conn, source_filters, wave_filters)
    _readiness_log(progress_started, f"{log_prefix}: {step}/{total_steps} weight coverage rows={len(weight)} in {time.monotonic() - weight_started:0.1f}s")
    step += 1
    mapping_started = time.monotonic()
    _readiness_log(progress_started, f"{log_prefix}: {step}/{total_steps} building mapping status coverage")
    mapping = mapping_status_coverage(conn, source_filters, wave_filters)
    _readiness_log(progress_started, f"{log_prefix}: {step}/{total_steps} mapping coverage rows={len(mapping)} in {time.monotonic() - mapping_started:0.1f}s")
    step += 1
    response_started = time.monotonic()
    _readiness_log(progress_started, f"{log_prefix}: {step}/{total_steps} building response coverage")
    response = response_coverage(
        conn,
        {"source": source_filters or [], "canonical_wave": wave_filters or [], "country_code": country_filters or [], "var_code": var_filters or []},
        progress_started=progress_started,
        log_prefix=f"{log_prefix}: response coverage",
    )
    _readiness_log(progress_started, f"{log_prefix}: {step}/{total_steps} response coverage rows={len(response)} in {time.monotonic() - response_started:0.1f}s")
    scope = scope_df.rename(columns={"source": "source", "wave": "wave"}).copy()
    scope["wave"] = scope["wave"].astype(str)
    scope["source"] = scope["source"].astype(str)
    scope["country_code"] = scope["country_code"].astype(str)

    merged = scope.merge(response, on=["source", "wave", "country_code"], how="left")
    merged = merged.merge(pos, on=["source", "wave", "country_code"], how="left")
    merged = merged.merge(weight, on=["source", "wave"], how="left")
    merged = merged.merge(mapping, on=["source", "wave"], how="left")
    step += 1
    merge_started = time.monotonic()
    _readiness_log(progress_started, f"{log_prefix}: {step}/{total_steps} merging coverage frames")

    pos_cols = [f"{field}_n" for field in POSITION_FIELDS if f"{field}_n" in merged.columns]
    merged["position_nonnull_sum"] = merged[pos_cols].fillna(0).sum(axis=1) if pos_cols else 0
    merged["has_positions"] = merged["position_nonnull_sum"] > 0
    merged["has_weights"] = merged.get("weight_rows", 0).fillna(0) > 0 if "weight_rows" in merged else False
    merged["has_mapped_rows"] = merged.get("mapped_rows", 0).fillna(0) > 0 if "mapped_rows" in merged else False
    merged["readiness_status"] = "partial"
    merged.loc[(merged["respondents"].fillna(0) >= min_cell_n) & merged["has_mapped_rows"] & merged["has_positions"], "readiness_status"] = "ready"
    merged.loc[(merged["respondents"].fillna(0) >= min_cell_n) & merged["has_mapped_rows"] & ~merged["has_positions"], "readiness_status"] = "distribution_only"
    merged.loc[merged["respondents"].fillna(0) < min_cell_n, "readiness_status"] = "underpowered"
    merged.loc[merged["mapped_rows"].fillna(0) <= 0, "readiness_status"] = "mapping_insufficient"
    merged.loc[~merged["has_weights"], "weight_status"] = "unweighted_only"
    merged.loc[merged["has_weights"], "weight_status"] = "weighted"
    merged.loc[~merged["has_positions"], "position_status"] = "missing_positions"
    merged.loc[merged["has_positions"], "position_status"] = "positions_present"
    merged["legacy_leak_flag"] = merged.get("legacy_leak_rows", 0).fillna(0) > 0
    merged["country_code"] = merged["country_code"].fillna("").astype(str)
    merged["source"] = merged["source"].fillna("").astype(str)
    merged["wave"] = merged["wave"].fillna("").astype(str)
    merged["country_code"] = merged["country_code"].replace({"nan": ""})
    underpowered = merged[merged["readiness_status"].eq("underpowered")].copy()
    legacy = merged[merged["legacy_leak_flag"]].copy()
    _readiness_log(
        progress_started,
        f"{log_prefix}: {step}/{total_steps} classified readiness ready={int((merged['readiness_status'] == 'ready').sum())} distribution_only={int((merged['readiness_status'] == 'distribution_only').sum())} underpowered={len(underpowered)} mapping_insufficient={int((merged['readiness_status'] == 'mapping_insufficient').sum())} in {time.monotonic() - merge_started:0.1f}s",
    )
    return merged.reset_index(drop=True), pos.reset_index(drop=True), weight.reset_index(drop=True), mapping.reset_index(drop=True), legacy.reset_index(drop=True), underpowered.reset_index(drop=True)


def discover_shardable_source_waves(
    conn,
    static_paths: Any | None = None,
    filters: dict[str, list[str]] | None = None,
) -> pd.DataFrame:
    source_filters = (filters or {}).get("source", [])
    wave_filters = (filters or {}).get("wave", [])
    country_filters = (filters or {}).get("country", [])
    scope = load_scope_manifest(conn, source_filters or None, wave_filters or None, country_filters or None)
    if scope.empty:
        return pd.DataFrame(columns=[
            "source",
            "source_family",
            "wave",
            "canonical_wave",
            "countries",
            "country_count",
            "respondent_count",
            "response_row_count",
            "mapped_row_count",
            "facet_row_count",
            "position_field_count",
            "weight_status",
            "readiness_status",
            "skip_by_default",
            "skip_reason",
            "estimated_question_count",
        ])
    readiness_df, pos_df, weight_df, mapping_df, _, underpowered_df = build_readiness(
        conn,
        scope,
        min_cell_n=50,
        source_filters=source_filters or None,
        wave_filters=wave_filters or None,
        country_filters=country_filters or None,
    )
    response_df = response_coverage(
        conn,
        {"source": source_filters or [], "canonical_wave": wave_filters or [], "country_code": country_filters or [], "var_code": var_filters or []},
    )
    rows = []
    for (source, wave), group in scope.groupby(["source", "wave"], sort=False):
        countries = sorted({str(c) for c in group["country_code"].dropna().astype(str) if str(c).strip()})
        resp = readiness_df[(readiness_df["source"].eq(source)) & (readiness_df["wave"].eq(wave))]
        resp_counts = response_df[(response_df["source"].eq(source)) & (response_df["wave"].eq(wave))]
        pos_counts = pos_df[(pos_df["source"].eq(source)) & (pos_df["wave"].eq(wave))]
        weight_counts = weight_df[(weight_df["source"].eq(source)) & (weight_df["wave"].eq(wave))]
        map_counts = mapping_df[(mapping_df["source"].eq(source)) & (mapping_df["wave"].eq(wave))]
        readiness_status = str(resp["readiness_status"].iloc[0]) if not resp.empty and "readiness_status" in resp.columns else "unknown"
        skip_reason = None if readiness_status in {"ready", "distribution_only", "partial"} else readiness_status
        position_field_count = 0
        if not pos_counts.empty:
            position_field_count = int(sum(int(pos_counts.iloc[0].get(f"{field}_n", 0) or 0) > 0 for field in POSITION_FIELDS))
        rows.append(
            {
                "source": source,
                "source_family": source,
                "wave": wave,
                "canonical_wave": wave,
                "countries": countries,
                "country_count": len(countries),
                "respondent_count": int(group["respondents"].sum()),
                "response_row_count": int(resp_counts["response_rows"].sum()) if not resp_counts.empty and "response_rows" in resp_counts.columns else 0,
                "mapped_row_count": int(map_counts["mapped_rows"].sum()) if not map_counts.empty and "mapped_rows" in map_counts.columns else 0,
                "facet_row_count": int(map_counts["facet_rows"].sum()) if not map_counts.empty and "facet_rows" in map_counts.columns else 0,
                "position_field_count": position_field_count,
                "weight_status": "weighted" if not weight_counts.empty and int(weight_counts["weight_rows"].sum()) > 0 else "unweighted_only",
                "readiness_status": readiness_status,
                "skip_by_default": readiness_status in {"underpowered", "mapping_insufficient"},
                "skip_reason": skip_reason,
                "estimated_question_count": max(0, int(map_counts["mapped_rows"].sum()) // max(len(countries), 1)) if not map_counts.empty else 0,
            }
        )
    return pd.DataFrame(rows).sort_values(["source", "wave"]).reset_index(drop=True)
