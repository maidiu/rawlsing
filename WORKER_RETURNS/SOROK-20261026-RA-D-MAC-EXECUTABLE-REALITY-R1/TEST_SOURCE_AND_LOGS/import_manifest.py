"""Record actual import roots, module origins and content hashes for the S52 cut."""
from __future__ import annotations
import hashlib, json, sys, platform
from pathlib import Path

RETURN = Path(__file__).resolve().parent
ARCHIVE = RETURN / "isolated_archive_s52c821"
S52 = ARCHIVE / "WORKER_RETURNS" / "SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1"
if str(S52) not in sys.path:
    sys.path.insert(0, str(S52))
from s52.bootstrap import install, roots as s52_roots  # noqa: E402

install()

import s52  # noqa: E402
import s51.bootstrap  # noqa: E402
import s49.bootstrap  # noqa: E402
import s37.bootstrap  # noqa: E402
import lab_sgi1.history  # noqa: E402

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def origin(name: str) -> dict:
    mod = sys.modules.get(name)
    f = getattr(mod, "__file__", None)
    if not f:
        return {"module": name, "file": None}
    p = Path(f).resolve()
    return {"module": name, "file": str(p), "sha256": sha256(p) if p.is_file() else None}

roots = s52_roots()
# s37 roots include the actual external closure and loaded origins
r37 = s37.bootstrap.roots()
# Only imported modules that belong to the source closure or external roots.
interesting = [
    "s39.model", "s39.sources", "s37.bootstrap", "s37.session",
    "s44.root", "s44.session", "s45.session", "s46.producer",
    "s47.conditioning", "s47.session", "s48.session", "s49.actor",
    "s49.session", "s51.session", "s52.session", "s52.performer",
    "lab_sgi1.history", "lab_sgi1.joint", "candidate", "candidate.actor_access_response",
    "language_mediation.session", "joined.session", "bp4.world", "bp1.composer",
]
modules = {name: origin(name) for name in interesting}
report = {
    "schema": "RA_D_IMPORT_MANIFEST@1",
    "python": sys.version,
    "python_executable": sys.executable,
    "platform": platform.platform(),
    "cwd": str(Path.cwd()),
    "archive": str(ARCHIVE),
    "s52_roots": roots,
    "s37_roots": r37,
    "modules": modules,
    "imported_closure": {
        "s52_return": str(S52),
        "s51_return": str(S52.parent / "SOROK-20261025-S51-SITUATED-OBJECT-RELEVANCE-R1"),
        "s49_return": str(S52.parent / "SOROK-20261025-S49-INDEPENDENT-ACTOR-PRODUCER-R1"),
        "s39_model_file": modules["s39.model"].get("file"),
        "s39_model_sha256": modules["s39.model"].get("sha256"),
    },
}
print(json.dumps(report, indent=2, sort_keys=True))
