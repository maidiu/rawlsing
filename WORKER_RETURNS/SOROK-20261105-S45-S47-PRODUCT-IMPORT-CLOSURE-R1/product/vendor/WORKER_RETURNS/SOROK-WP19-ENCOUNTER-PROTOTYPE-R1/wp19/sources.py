"""Exact read-side source materialization for WP-19.

JOIN-E and CP-A5 are extracted from their pinned Git commits at runtime. The
extracted trees and generated encounter roots are gitignored and never staged.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
RUNTIME = RETURN / ".runtime"
JOIN_E_COMMIT = "5e63672543973ce2533129e1ca3224d82af0dffc"
JOIN_E_RETURN = "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1"
CP_A5_COMMIT = "913765328e4fab12b150ea01421ed6b445158184"
CP_A5_RETURN = "WORKER_RETURNS/SOROK-CP-A5-R2"
JOIN_E_PATHS = (
    JOIN_E_RETURN + "/joined",
    JOIN_E_RETURN + "/vendor/j",
    JOIN_E_RETURN + "/vendor/e",
    JOIN_E_RETURN + "/SOURCE_MANIFEST.json",
)
CP_A5_PATHS = (CP_A5_RETURN + "/candidate",)
JOIN_E_ROOT = RUNTIME / "join-e" / JOIN_E_RETURN
CP_A5_ROOT = RUNTIME / "cp-a5" / CP_A5_RETURN / "candidate"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _extract(
    commit: str, paths: tuple[str, ...], marker: Path, destination: Path
) -> None:
    if marker.exists():
        return
    archive = subprocess.run(
        ["git", "archive", commit, *paths],
        cwd=str(REPO),
        capture_output=True,
        check=True,
    )
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as bundle:
        bundle.extractall(destination)
    if not marker.exists():
        raise RuntimeError("WP19_SOURCE_EXTRACTION_INCOMPLETE:" + str(marker))


def ensure_join_e_source() -> Path:
    _extract(
        JOIN_E_COMMIT,
        JOIN_E_PATHS,
        JOIN_E_ROOT / "joined" / "session.py",
        RUNTIME / "join-e",
    )
    return JOIN_E_ROOT


def ensure_cp_a5_source() -> Path:
    _extract(
        CP_A5_COMMIT,
        CP_A5_PATHS,
        CP_A5_ROOT / "run_cp_a5.py",
        RUNTIME / "cp-a5",
    )
    return CP_A5_ROOT


def _env() -> dict:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_join_e_probe(
    *,
    state_root: str | Path,
    disposition: str = "PERFORMED",
    perform: str = "omit",
    mode: str = "start",
    do_help: bool = True,
) -> dict:
    join_e_root = ensure_join_e_source()
    state_root = Path(state_root).resolve()
    state_root.mkdir(parents=True, exist_ok=True)
    out = state_root / "wp19_join_e_bundle.json"
    command = [
        sys.executable,
        "-B",
        str(RETURN / "wp19" / "join_e_probe.py"),
        "--join-e-root",
        str(join_e_root),
        "--state",
        str(state_root),
        "--disposition",
        disposition,
        "--perform",
        perform,
        "--mode",
        mode,
        "--out",
        str(out),
    ]
    if do_help:
        command.append("--do-help")
    completed = subprocess.run(
        command,
        cwd=str(RETURN),
        env=_env(),
        capture_output=True,
        text=True,
        timeout=180,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "WP19_JOIN_E_PROBE_FAILED:" + completed.stderr[-4000:]
        )
    return json.loads(out.read_text(encoding="utf8"))


def run_cp_a5_command(root: str | Path, *args: str) -> dict:
    candidate = ensure_cp_a5_source()
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(candidate / "run_cp_a5.py"),
            "--root",
            str(root),
            *args,
        ],
        cwd=str(candidate),
        env=_env(),
        capture_output=True,
        text=True,
        timeout=240,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "WP19_CP_A5_COMMAND_FAILED:"
            + " ".join(args)
            + ":"
            + completed.stderr[-4000:]
        )
    return json.loads(completed.stdout)


def materialize_cp_a5(root: str | Path) -> Path:
    root = Path(root).resolve()
    if not (root / "life").exists():
        run_cp_a5_command(root, "scenario")
    return root


def cp_a5_store_path(root: str | Path) -> Path:
    return Path(root).resolve() / "life" / "c12.sqlite"


def join_e_store_path(bundle: dict) -> Path:
    return Path(bundle["c12_path"]).resolve()


def store_hashes(hashes: dict) -> dict:
    return {
        name: _sha256(Path(path)) if Path(path).exists() else ""
        for name, path in hashes.items()
    }


__all__ = [
    "CP_A5_COMMIT",
    "CP_A5_ROOT",
    "JOIN_E_COMMIT",
    "JOIN_E_ROOT",
    "RUNTIME",
    "cp_a5_store_path",
    "ensure_cp_a5_source",
    "ensure_join_e_source",
    "join_e_store_path",
    "materialize_cp_a5",
    "run_cp_a5_command",
    "run_join_e_probe",
    "store_hashes",
]
