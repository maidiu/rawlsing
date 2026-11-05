from __future__ import annotations

import io
import os
import subprocess
import sys
import tarfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
RETURN = Path(__file__).resolve().parents[1]
RUNTIME = Path(
    os.environ.get(
        "S45_PROJECTION_RUNTIME",
        str(REPO / ".local-logs" / "s45-projection-runtime"),
    )
)

S45_COMMIT = "f26a138e20d53c809d611cf8d834ec647b0804bf"
WP19_COMMIT = "3c4df43f813cd0727feff04f620aa0bbd9a63026"
S11_COMMIT = "faec7ce909c54664e85320534bdf744b9bc47d37"

S36_RETURN = "WORKER_RETURNS/SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1"
S37_RETURN = "WORKER_RETURNS/SOROK-20261024-S37-INTEGRATED-CONSUMER-R1"
S39_RETURN = "WORKER_RETURNS/SOROK-20261024-S39-GENERATED-RESPONSE-R1"
S40_RETURN = "WORKER_RETURNS/SOROK-20261024-S40-GENERATED-NATIVE-SPEECH-R1"
S41_RETURN = "WORKER_RETURNS/SOROK-20261024-S41-CONTINUING-PERSON-EVENTS-R1"
S42_RETURN = "WORKER_RETURNS/SOROK-20261024-S42-ONGOING-EVENT-CONSUMER-R1"
S43_RETURN = "WORKER_RETURNS/SOROK-20261024-S43-HISTORICAL-LANGUAGE-CONSUMER-R1"
S44_RETURN = "WORKER_RETURNS/SOROK-20261024-S44-SAMPLED-ROOT-CONSUMER-R1"
S45_RETURN = "WORKER_RETURNS/SOROK-20261025-S45-GENERATED-ROOT-ENCOUNTER-R1"
WP19_RETURN = "WORKER_RETURNS/SOROK-WP19-ENCOUNTER-PROTOTYPE-R1"
S11_RETURN = "WORKER_RETURNS/SOROK-S11-ENCOUNTER-EXIT-SPEC-R1"
S11_SPEC = S11_RETURN + "/02_WP19_CONSUMABLE_INTERFACE.json"

CHAIN_PATHS = (
    S36_RETURN,
    S37_RETURN,
    S39_RETURN,
    S40_RETURN,
    S41_RETURN,
    S42_RETURN,
    S43_RETURN,
    S44_RETURN,
    S45_RETURN,
)

_REQUIRED = (
    S36_RETURN + "/candidate/__init__.py",
    S37_RETURN + "/s37/bootstrap.py",
    S39_RETURN + "/s39/__init__.py",
    S40_RETURN + "/s40/session.py",
    S41_RETURN + "/s41/__init__.py",
    S42_RETURN + "/s42/session.py",
    S43_RETURN + "/s43/session.py",
    S44_RETURN + "/s44/session.py",
    S45_RETURN + "/s45/session.py",
    WP19_RETURN + "/wp19/interface.py",
    S11_SPEC,
)


def _extract(commit: str, paths: tuple[str, ...]) -> None:
    archive = subprocess.run(
        ["git", "archive", commit, *paths],
        cwd=str(REPO),
        capture_output=True,
        check=True,
    )
    RUNTIME.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as bundle:
        bundle.extractall(RUNTIME)


def ensure_pinned() -> dict:
    if not all((RUNTIME / relative).is_file() for relative in _REQUIRED):
        _extract(S45_COMMIT, CHAIN_PATHS)
        _extract(WP19_COMMIT, (WP19_RETURN,))
        _extract(S11_COMMIT, (S11_RETURN,))
    missing = [relative for relative in _REQUIRED if not (RUNTIME / relative).is_file()]
    if missing:
        raise RuntimeError("PINNED_SOURCE_INCOMPLETE:" + ",".join(missing))
    return {
        "repo": REPO,
        "return": RETURN,
        "runtime": RUNTIME,
        "s45_commit": S45_COMMIT,
        "wp19_commit": WP19_COMMIT,
        "s11_commit": S11_COMMIT,
        "s45_return": RUNTIME / S45_RETURN,
        "wp19_return": RUNTIME / WP19_RETURN,
        "s11_return": RUNTIME / S11_RETURN,
        "s11_spec": RUNTIME / S11_SPEC,
    }


def ensure_pinned_imports() -> dict:
    info = ensure_pinned()
    for path in (str(info["wp19_return"]), str(info["s45_return"]), str(RETURN)):
        if path in sys.path:
            sys.path.remove(path)
    for path in (str(RETURN), str(info["wp19_return"]), str(info["s45_return"])):
        sys.path.insert(0, path)
    import s45
    import wp19.interface as wp19_interface

    if not Path(s45.__file__).resolve().is_relative_to(info["s45_return"]):
        raise RuntimeError("S45_IMPORT_ORIGIN_MISMATCH:" + str(s45.__file__))
    if not Path(wp19_interface.__file__).resolve().is_relative_to(
        info["wp19_return"]
    ):
        raise RuntimeError(
            "WP19_IMPORT_ORIGIN_MISMATCH:" + str(wp19_interface.__file__)
        )
    info["s45"] = s45
    info["wp19_interface"] = wp19_interface
    return info


def pinned_env() -> dict:
    info = ensure_pinned()
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = os.pathsep.join([
        str(RETURN),
        str(info["s45_return"]),
        env.get("PYTHONPATH", ""),
    ])
    return env
