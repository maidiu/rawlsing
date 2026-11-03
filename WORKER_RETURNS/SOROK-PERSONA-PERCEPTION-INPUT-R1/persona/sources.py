"""Pinned JOIN-E extraction and real session probe for persona input."""
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
JOIN_E_ROOT = RUNTIME / "join-e" / JOIN_E_RETURN
JOIN_E_PATHS = (
    JOIN_E_RETURN + "/joined",
    JOIN_E_RETURN + "/vendor/j",
    JOIN_E_RETURN + "/vendor/e",
    JOIN_E_RETURN + "/SOURCE_MANIFEST.json",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_join_e_source() -> Path:
    marker = JOIN_E_ROOT / "joined" / "session.py"
    if marker.exists():
        return JOIN_E_ROOT
    archive = subprocess.run(
        ["git", "archive", JOIN_E_COMMIT, *JOIN_E_PATHS],
        cwd=str(REPO),
        capture_output=True,
        check=True,
    )
    destination = RUNTIME / "join-e"
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as bundle:
        bundle.extractall(destination)
    if not marker.exists():
        raise RuntimeError("PERSONA_JOIN_E_SOURCE_EXTRACTION_INCOMPLETE")
    return JOIN_E_ROOT


def run_probe(
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
    out = state_root / "persona_join_e_bundle.json"
    command = [
        sys.executable,
        "-B",
        str(RETURN / "persona" / "join_e_probe.py"),
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
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        command,
        cwd=str(RETURN),
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )
    if completed.returncode != 0:
        raise RuntimeError("PERSONA_JOIN_E_PROBE_FAILED:" + completed.stderr[-4000:])
    return json.loads(out.read_text(encoding="utf8"))


def store_hash(bundle: dict) -> str:
    path = Path(bundle["c12_path"])
    return _sha256(path) if path.exists() else ""


__all__ = [
    "JOIN_E_COMMIT",
    "JOIN_E_ROOT",
    "RUNTIME",
    "ensure_join_e_source",
    "run_probe",
    "store_hash",
]
