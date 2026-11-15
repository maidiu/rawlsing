"""Focused source/API identity check for the preflight registry.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B \
      WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-CONTEXT-RECHECK-R1/reproductions/repro_context_modules.py

Confirms the s43.registry imported by the preflight is the same module used by
the S43Session in the actual S47 inheritance chain, and prints the actual
registry milieus and native default context.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

REPO = next(
    path for path in Path(__file__).resolve().parents if (path / "WORKER_RETURNS").is_dir()
)
sys.path.insert(0, str(REPO / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"))
os.chdir(REPO)

from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-context-modules-"))
    fanin = load_p2().start(root)
    case = fanin.deps["case_for"](True)
    owner = P2Owner(
        fanin,
        case=case,
        source=fanin.deps["source_for"](case),
        participants=tuple(fanin.session.read_root()["actor_ids"]),
    )
    try:
        import s43
        import s43.registry
        import s43.session

        print("s43 package", s43.__file__)
        print("s43.registry", s43.registry.__file__)
        print("s43.session", s43.session.__file__)
        print("session class", type(fanin.session))
        for cls in type(fanin.session).__mro__:
            if cls.__module__.startswith("s43"):
                print("mro s43 class", cls, sys.modules[cls.__module__].__file__)
        print("registry hash", s43.registry.REGISTRY_HASH)
        print("registry schema", s43.registry.registry_document()["schema"])
        print(
            "unit library milieus",
            sorted(
                {
                    unit["milieu_id"]
                    for unit in s43.registry.registry_document()["unit_library"].values()
                }
            ),
        )
        print("native context", fanin.session.s43_context())
        return 0
    finally:
        owner.close()


if __name__ == "__main__":
    raise SystemExit(main())
