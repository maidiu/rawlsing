"""Import closure for the BP2P4J joined product.

Puts the two exact staged upstream returns on ``sys.path`` in a fixed order and
then verifies, after import, that every loaded upstream module is byte-identical
to a file recorded in the staged source manifest (or, for the two live
``rawlsing_next`` modules, to the exact Git blob pinned by the upstream returns).

No upstream module is patched. The only new code is in this return's
``bp2p4`` package.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
REPO = next(p for p in RETURN.parents if (p / ".git").exists())
VENDOR = RETURN / "vendor"
MANIFEST = VENDOR / "source_manifest.json"
BP2_DIR = VENDOR / "bp2"
BP4_DIR = VENDOR / "bp4"

# The two live namespace modules are part of the checkout, not of either return.
PINNED_LIVE_BLOBS = {
    "rawlsing_next/m6_actor_safe_expression.py":
        "74d9701cdc7dabccf61eb5089498db290c1efd9c",
    "rawlsing_next/v3_psepf_zero_positive_guard.py":
        "e0528d65215cb431196570c38bac4eae94217a1b",
}

UPSTREAM_MODULES = (
    "bp1", "bp1.canon", "bp1.source", "bp1.ledger", "bp1.composer", "bp1.c9_bridge",
    "candidate", "candidate.identity", "candidate.events", "candidate.conditioning",
    "candidate.response_rules", "candidate.target_rules", "candidate.transaction",
    "candidate.pipeline", "candidate.action_admission", "candidate.later_action",
    "lab_sgi1", "lab_sgi1.core", "lab_sgi1.history", "lab_sgi1.joint",
    "lab_sgi1.proposal",
    "c8_exclusive_writer", "c9_event_ingress", "outbox_prototype",
    "c8o_trusted_outbox", "c8_readonly_consumer",
    "rawlsing_next.m6_actor_safe_expression",
    "rawlsing_next.v3_psepf_zero_positive_guard",
)
JOINED_MODULES = (
    "bp2_joined", "bp2_joined.producer", "bp2_joined.binding", "bp2_joined.ports",
    "bp2_joined.bootstrap",
    "bp4", "bp4.c10", "bp4.store", "bp4.world", "bp4.product", "bp4.perception",
    "bp4.bp2_compat",
)


class SourceClosureDrift(RuntimeError):
    pass


def _manifest_hashes() -> dict[str, str]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf8"))
    return {row["sha256"]: row["staged_path"] for row in manifest["files"]}


def install() -> None:
    # Real repo root first: provides the live pinned ``rawlsing_next`` modules and
    # lets BP4's own bootstrap resolve them in a staged location.
    for path in (str(REPO), str(BP4_DIR), str(BP2_DIR)):
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)
    # BP2's own bootstrap installs its exact vendor closure (bp1, c9r, g18, bp3,
    # native guard).
    import bp2_joined  # noqa: F401

    bp2_joined.install()
    # BP4 imports its package-level path setup on first import.
    import bp4  # noqa: F401


def _blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources() -> dict:
    """Re-read every staged file from its origin and compare bytes."""
    import importlib.util

    stage_path = RETURN / "tools" / "stage_sources.py"
    spec = importlib.util.spec_from_file_location("bp2p4j_stage_sources", stage_path)
    stage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stage)  # type: ignore[union-attr]
    ok, problems = stage.verify()
    if not ok:
        raise SourceClosureDrift(";".join(problems))
    return json.loads(MANIFEST.read_text(encoding="utf8"))


def verify_loaded_modules(strict: bool = True) -> dict:
    """Verify every imported upstream and joined module against pinned bytes."""
    manifest_paths = _manifest_hashes()
    rows = []
    problems = []
    for name in UPSTREAM_MODULES + JOINED_MODULES:
        module = sys.modules.get(name)
        if module is None:
            if strict:
                problems.append("NOT_IMPORTED:" + name)
            continue
        path = Path(getattr(module, "__file__", "")).resolve()
        if not path.exists():
            problems.append("NO_FILE:" + name)
            continue
        digest = _sha256(path)
        relative_repo = None
        try:
            relative_repo = str(path.relative_to(REPO))
        except ValueError:
            relative_repo = None
        pinned_live = (
            relative_repo is not None
            and relative_repo in PINNED_LIVE_BLOBS
        )
        if pinned_live:
            expected = PINNED_LIVE_BLOBS[relative_repo]
            actual = _blob_sha1(path)
            ok = actual == expected
            origin = "LIVE_REPO_PINNED"
            detail = expected
        else:
            ok = digest in manifest_paths
            origin = "STAGED_RETURN"
            detail = manifest_paths.get(digest, "")
        if not ok:
            problems.append("HASH_NOT_PINNED:" + name + ":" + str(path))
        rows.append({
            "module": name,
            "path": str(path),
            "origin": origin,
            "pinned": detail,
            "sha256": digest,
            "ok": ok,
        })
    if problems and strict:
        raise SourceClosureDrift(";".join(problems))
    return {"ok": not problems, "problems": problems, "modules": rows}


def module_origins(*names: str) -> list[dict]:
    rows = []
    for name in names:
        module = sys.modules.get(name)
        path = Path(getattr(module, "__file__", "")).resolve() if module else None
        rows.append({"module": name, "path": str(path) if path else "",
                     "sha256": _sha256(path) if path and path.exists() else ""})
    return rows


__all__ = [
    "BP2_DIR", "BP4_DIR", "JOINED_MODULES", "MANIFEST", "PINNED_LIVE_BLOBS",
    "REPO", "RETURN", "SourceClosureDrift", "UPSTREAM_MODULES", "VENDOR",
    "install", "module_origins", "verify_loaded_modules", "verify_sources",
]
