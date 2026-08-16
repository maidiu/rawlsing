#!/usr/bin/env python3
"""Storage contract helpers for V550."""

from __future__ import annotations

import json
import errno
import os
import shutil
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from data.ddm_build_copy.ddm_v550_schema import QUESTION_USE_CONTRACT_SCHEMA, write_schema_json


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_run_id(stage: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stage}_{stamp}"


def load_env_database_url(env_file: Path | None, explicit_url: str | None) -> str | None:
    if explicit_url:
        return explicit_url
    if env_file is not None and env_file.exists():
        from dotenv import load_dotenv

        load_dotenv(env_file)
    return os.environ.get("DATABASE_URL")


def try_connect_database(db_url: str | None) -> tuple[Any | None, str | None]:
    if not db_url:
        return None, "DATABASE_URL is missing."
    try:
        import psycopg2

        return psycopg2.connect(db_url), None
    except Exception as exc:  # pragma: no cover - connection failure handled by callers
        return None, str(exc)


def atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f".{path.name}.tmp")
    tmp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp_path.replace(path)


def _robust_rmtree(path: Path, *, retries: int = 3, delay_seconds: float = 0.2) -> None:
    if not path.exists():
        return

    def _onerror(func, target_path, exc_info):  # type: ignore[no-untyped-def]
        exc = exc_info[1]
        if isinstance(exc, OSError) and exc.errno in {errno.ENOTEMPTY, errno.EBUSY, errno.ENOENT}:
            try:
                if Path(target_path).is_dir():
                    time.sleep(delay_seconds)
                    return
            except Exception:
                pass
        raise exc

    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            shutil.rmtree(path, onerror=_onerror)
            return
        except FileNotFoundError:
            return
        except OSError as exc:
            last_exc = exc
            if exc.errno in {errno.ENOTEMPTY, errno.EBUSY} and attempt < retries - 1:
                time.sleep(delay_seconds * (attempt + 1))
                continue
            raise
    if last_exc is not None:
        raise last_exc


def atomic_promote_latest(output_root: Path, run_id: str, manifest: dict) -> None:
    latest_link = output_root / "latest"
    latest_json = output_root / "LATEST.json"
    run_path = output_root / "runs" / run_id
    if latest_link.exists() or latest_link.is_symlink():
        try:
            latest_link.unlink()
        except OSError:
            pass
    try:
        latest_link.symlink_to(run_path)
    except OSError:
        pass
    atomic_write_json(
        latest_json,
        {
            "latest_successful_run_id": run_id,
            "latest_successful_run_path": str(run_path),
            "updated_at": utc_now(),
            "manifest": manifest,
        },
    )


def write_parquet_with_schema(df: pd.DataFrame, path: Path, schema_path: Path | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    if schema_path is not None:
        schema_path.parent.mkdir(parents=True, exist_ok=True)
        write_schema_json(schema_path, df, name=path.stem, run_id=path.parent.parent.name if path.parent.parent else "", extra=None)


def read_table_any(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    if path.suffix.lower() in {".csv", ".txt"}:
        return pd.read_csv(path, low_memory=False)
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return pd.DataFrame(payload)
        if isinstance(payload, dict):
            return pd.DataFrame([payload])
    raise ValueError(f"Unsupported table format: {path}")


@dataclass
class V550Paths:
    root: Path
    run_id: str
    run_path: Path = field(init=False)
    failed_root: Path = field(init=False)
    schemas: Path = field(init=False)
    core: Path = field(init=False)
    distributions: Path = field(init=False)
    determinicity: Path = field(init=False)
    clouds: Path = field(init=False)
    audit: Path = field(init=False)
    csv_mirrors: Path = field(init=False)
    latest_link: Path = field(init=False)
    latest_json: Path = field(init=False)
    failed_run_path: Path = field(init=False)

    def __post_init__(self) -> None:
        self.run_path = self.root / "runs" / self.run_id
        self.failed_root = self.root / "failed"
        self.schemas = self.run_path / "schemas"
        self.core = self.run_path / "core"
        self.distributions = self.run_path / "distributions"
        self.determinicity = self.run_path / "determinicity"
        self.clouds = self.run_path / "clouds"
        self.audit = self.run_path / "audit"
        self.csv_mirrors = self.run_path / "csv_mirrors"
        self.latest_link = self.root / "latest"
        self.latest_json = self.root / "LATEST.json"
        self.failed_run_path = self.failed_root / self.run_id

    def ensure(self) -> None:
        for path in [self.root, self.failed_root, self.run_path, self.schemas, self.core, self.distributions, self.determinicity, self.clouds, self.audit, self.csv_mirrors]:
            path.mkdir(parents=True, exist_ok=True)

    def mark_failed(self) -> None:
        self.failed_run_path.mkdir(parents=True, exist_ok=True)

    def promote_latest(self) -> None:
        atomic_promote_latest(self.root, self.run_id, {"success": True})


@dataclass
class V550ShardPaths:
    root: Path
    run_id: str
    shard_id: str
    run_path: Path = field(init=False)
    shard_path: Path = field(init=False)
    manifest_path: Path = field(init=False)
    status_path: Path = field(init=False)
    warnings_path: Path = field(init=False)
    schemas: Path = field(init=False)
    checkpoints: Path = field(init=False)
    questions_checkpoints: Path = field(init=False)
    tables_checkpoints: Path = field(init=False)
    respondent_substrate: Path = field(init=False)
    core: Path = field(init=False)
    distributions: Path = field(init=False)
    determinicity: Path = field(init=False)
    clouds: Path = field(init=False)
    audit: Path = field(init=False)
    csv_mirrors: Path = field(init=False)
    bridge: Path = field(init=False)
    run_root: Path = field(init=False)

    def __post_init__(self) -> None:
        self.run_root = self.root / "shard_runs" / self.run_id
        self.shard_path = self.run_root / self.shard_id
        self.run_path = self.shard_path
        self.manifest_path = self.shard_path / "shard_manifest.json"
        self.status_path = self.shard_path / "shard_status.json"
        self.warnings_path = self.shard_path / "shard_warnings.json"
        self.schemas = self.shard_path / "schemas"
        self.checkpoints = self.shard_path / "checkpoints"
        self.questions_checkpoints = self.checkpoints / "questions"
        self.tables_checkpoints = self.checkpoints / "tables"
        self.respondent_substrate = self.checkpoints / "respondent_substrate"
        self.core = self.shard_path / "core"
        self.distributions = self.shard_path / "distributions"
        self.determinicity = self.shard_path / "determinicity"
        self.clouds = self.shard_path / "clouds"
        self.audit = self.shard_path / "audit"
        self.csv_mirrors = self.shard_path / "csv_mirrors"
        self.bridge = self.shard_path / "bridge"

    def ensure(self) -> None:
        for path in [
            self.root,
            self.run_root,
            self.shard_path,
            self.schemas,
            self.checkpoints,
            self.questions_checkpoints,
            self.tables_checkpoints,
            self.respondent_substrate,
            self.core,
            self.distributions,
            self.determinicity,
            self.clouds,
            self.audit,
            self.csv_mirrors,
            self.bridge,
        ]:
            path.mkdir(parents=True, exist_ok=True)

    def clean(self) -> None:
        if self.shard_path.exists():
            _robust_rmtree(self.shard_path)
        self.ensure()


def connect_from_env(db_url: str | None = None, env_file: Path | None = None):
    url = load_env_database_url(env_file, db_url)
    if not url:
        raise RuntimeError("DATABASE_URL is missing.")
    conn, error = try_connect_database(url)
    if conn is None:
        raise RuntimeError(error or "Could not connect to Postgres.")
    return conn


def ensure_directories(root: Path, run_id: str) -> V550Paths:
    paths = V550Paths(root=root, run_id=run_id)
    paths.ensure()
    return paths


def _canonicalize_empty_table_schema(df: pd.DataFrame, table_name: str) -> pd.DataFrame:
    """Widen valid-empty QUC output to its canonical required schema before serialization."""
    if not df.empty or table_name != "question_use_contract":
        return df
    columns = list(dict.fromkeys([
        *df.columns,
        *QUESTION_USE_CONTRACT_SCHEMA["required_columns"],
    ]))
    return df.reindex(columns=columns)


def write_table(
    df: pd.DataFrame,
    *,
    paths: V550Paths,
    table_name: str,
    layer: str,
    write_csv: bool = True,
    write_parquet: bool = True,
    report_name: str | None = None,
    reports_dir: Path | None = None,
    extra_schema: dict[str, Any] | None = None,
    arrow_schema: Any = None,
) -> dict[str, Any]:
    df = _canonicalize_empty_table_schema(df, table_name)
    layer_dir = {
        "core": paths.core,
        "distributions": paths.distributions,
        "determinicity": paths.determinicity,
        "clouds": paths.clouds,
        "audit": paths.audit,
        "schemas": paths.schemas,
    }.get(layer, paths.core)
    layer_dir.mkdir(parents=True, exist_ok=True)

    parquet_path = layer_dir / f"{table_name}.parquet"
    csv_name = report_name or f"{table_name}.csv"
    csv_path = paths.csv_mirrors / csv_name
    schema_path = paths.schemas / f"{table_name}.schema.json"

    if write_parquet:
        if arrow_schema is not None:
            import pyarrow as pa, pyarrow.parquet as pq
            frame = df.reindex(columns=arrow_schema.names)
            table = pa.Table.from_pandas(frame, schema=arrow_schema, preserve_index=False)
            pq.write_table(table, parquet_path)
            _write_schema_json_from_arrow(schema_path, arrow_schema, row_count=len(df), name=table_name, run_id=paths.run_id, extra=extra_schema)
        else:
            df.to_parquet(parquet_path, index=False)
    if write_csv:
        df.to_csv(csv_path, index=False)
    if arrow_schema is None:
        write_schema_json(schema_path, df, name=table_name, run_id=paths.run_id, extra=extra_schema)

    if reports_dir is not None and write_csv:
        reports_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(reports_dir / csv_name, index=False)

    return {
        "table_name": table_name,
        "layer": layer,
        "parquet_path": str(parquet_path) if write_parquet else "",
        "csv_path": str(csv_path) if write_csv else "",
        "schema_path": str(schema_path),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
    }


def _write_schema_json_from_arrow(
    path: Path,
    arrow_schema: Any,
    *,
    row_count: int,
    name: str,
    run_id: str,
    extra: dict[str, Any] | None = None,
) -> None:
    """Write schema JSON from an explicit Arrow schema (not pandas-inferred)."""
    payload = {
        "name": name,
        "run_id": run_id,
        "row_count": row_count,
        "column_count": len(arrow_schema),
        "columns": [{"name": f.name, "dtype": str(f.type)} for f in arrow_schema],
    }
    if extra:
        payload.update(extra)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_manifest(paths: V550Paths, payload: dict[str, Any]) -> Path:
    manifest_path = paths.run_path / "manifest.json"
    manifest_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest_path
