#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
from typing import Any


def load_env(path: Path | None) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path or not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def connect(dsn: str):
    try:
        import psycopg  # type: ignore
        return psycopg.connect(dsn)
    except ImportError:
        import psycopg2  # type: ignore
        return psycopg2.connect(dsn)


def query_rows(conn, sql: str, params: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return list(cur.fetchall())


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the live respondent-level database contract for the bounded nine-source V550J canary.")
    parser.add_argument("--section", type=Path, required=True)
    parser.add_argument("--db-url", default="")
    parser.add_argument("--env-file", type=Path, default=None)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    env = load_env(args.env_file)
    dsn = args.db_url or os.environ.get("DATABASE_URL", "") or env.get("DATABASE_URL", "")
    if not dsn:
        raise RuntimeError("DATABASE_URL is required")

    section = args.section.resolve()
    with (section / "authority" / "bounded_nine_scope_manifest.csv").open(encoding="utf-8", newline="") as handle:
        scopes = list(csv.DictReader(handle))
    with (section / "authority" / "bounded_joint_configuration_item_crosswalk.csv").open(encoding="utf-8", newline="") as handle:
        items = list(csv.DictReader(handle))
    by_config: dict[str, list[str]] = {}
    for row in items:
        by_config.setdefault(row["joint_configuration_id"], []).append(row["var_code"].upper())

    conn = connect(dsn)
    try:
        available = {row[0] for row in query_rows(conn, "SELECT table_name FROM information_schema.views WHERE table_schema='public' AND table_name IN ('v_ddm_response_long_facet_ready_authority','v_ddm_response_long_facet_ready')")}
        view = "v_ddm_response_long_facet_ready_authority" if "v_ddm_response_long_facet_ready_authority" in available else "v_ddm_response_long_facet_ready" if "v_ddm_response_long_facet_ready" in available else ""
        if not view:
            raise RuntimeError("Neither required facet-ready respondent view exists")
        columns = {row[0] for row in query_rows(conn, "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name=%s", (view,))}
        required = {"source", "canonical_wave", "country_code", "var_code", "respondent_id"}
        missing = sorted(required - columns)
        if missing:
            raise RuntimeError(f"{view} is missing required columns: {missing}")

        results = []
        failures = []
        for scope in scopes:
            variables = by_config[scope["joint_configuration_id"]]
            rows = query_rows(conn, f'''SELECT count(*)::bigint, count(DISTINCT respondent_id)::bigint, count(DISTINCT upper(var_code))::bigint
                FROM public.{view}
                WHERE source=%s AND canonical_wave=%s AND country_code=%s AND upper(var_code)=ANY(%s)''',
                (scope["source_family"], scope["wave"], scope["country_code"], variables))
            row_count, respondent_count, variable_count = map(int, rows[0])
            passed = row_count > 0 and respondent_count > 0 and variable_count == len(set(variables))
            if not passed:
                failures.append(scope["scope_dir"])
            results.append({
                "scope_dir": scope["scope_dir"],
                "source_family": scope["source_family"],
                "wave": scope["wave"],
                "country_code": scope["country_code"],
                "expected_variable_count": len(set(variables)),
                "observed_variable_count": variable_count,
                "response_row_count": row_count,
                "respondent_count": respondent_count,
                "status": "PASS" if passed else "FAIL",
            })
        result = {
            "status": "PASS_LIVE_RESPONDENT_DATABASE_CONTRACT" if not failures else "FAIL_LIVE_RESPONDENT_DATABASE_CONTRACT",
            "resolved_view": f"public.{view}",
            "scope_count": len(scopes),
            "passed_scope_count": len(scopes) - len(failures),
            "failed_scopes": failures,
            "scope_results": results,
        }
    finally:
        conn.close()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
