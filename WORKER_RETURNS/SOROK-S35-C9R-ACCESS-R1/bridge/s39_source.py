"""Read-only audit of the S39 A performer at its pinned Git cut."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
S39_COMMIT = "6604f2d9"
S39_RETURN = "WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1"
FILES = {
    "performer": S39_RETURN + "/s39/performer.py",
    "sources": S39_RETURN + "/s39/sources.py",
    "session": S39_RETURN + "/s39/session.py",
}


def _git_show(path: str) -> tuple[str, str, str]:
    blob = subprocess.run(
        ["git", "rev-parse", f"{S39_COMMIT}:{path}"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    text = subprocess.run(
        ["git", "show", f"{S39_COMMIT}:{path}"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    sha256 = hashlib.sha256(text.encode("utf8")).hexdigest()
    return blob, sha256, text


def audit() -> dict:
    files = {}
    texts = {}
    for name, path in FILES.items():
        blob, sha256, text = _git_show(path)
        texts[name] = text
        files[name] = {"path": path, "git_blob": blob, "sha256": sha256}
    performer = texts["performer"]
    sources = texts["sources"]
    return {
        "schema": "S35_S39_A_PERFORMER_AUDIT@1",
        "commit": S39_COMMIT,
        "native": False,
        "files": files,
        "performer_options": [
            option
            for option in ("ATTEND_OBJECT", "REQUEST_TOOL", "EXPLICIT_REFUSAL")
            if option in performer
        ],
        "requires_s37_product_inspect": "product.inspect" in performer,
        "requires_generated_attempt": "attempt_request" in performer,
        "sources_are_synthetic_premises": (
            "TEST_ONLY_SYNTHETIC_ACTOR_CONTEXT_MODEL_PREMISE_NOT_OBSERVED"
            in sources
        ),
        "join_e_root_compatible": False,
        "actual_a_performer": False,
        "reason": (
            "S39 performer executes A options over the S37 targetless product "
            "and a generated attempt; it is not wired to the JOIN-E R31J "
            "product and its selection sources are TEST_ONLY synthetic model "
            "premises, not actual A observations."
        ),
    }


__all__ = ["FILES", "S39_COMMIT", "S39_RETURN", "audit"]
