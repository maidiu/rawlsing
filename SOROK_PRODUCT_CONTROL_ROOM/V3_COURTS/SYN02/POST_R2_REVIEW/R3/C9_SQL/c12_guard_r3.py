"""C9-R3 test-only C12 fork guard policy over the actual imported C12 source.

This wrapper does not edit BP4/r26e. It makes the owner guard decision
executable: if a perception lies beyond the last non-perception clock, or the
exact perception cut cannot be qualified, return FORK_HELD rather than CLEAN.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


class C12ForkHeld(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def load_c12():
    join = Path(os.environ.get("JOIN_E_RETURN", "")).expanduser()
    if not join.is_absolute() or not join.is_dir():
        raise RuntimeError("JOIN_E_RETURN_MISSING")
    for rel in ("vendor/j", "vendor/j/candidate", "vendor/j/candidate/vendor/bp4"):
        path = str(join / rel)
        if path not in sys.path:
            sys.path.insert(0, path)
    from bp4.store import C12Store
    from r26e.c12_integrity import QualifiedC12Store
    return C12Store, QualifiedC12Store


def guard_fork(store, parent_branch_id: str, new_branch_id: str) -> dict:
    """Create a fork only if the complete perception cut is qualifiable."""
    parent = store.branch(parent_branch_id)
    nonperception = int(store.last_clock(parent_branch_id))
    perceptions = list(store.perceptions(parent_branch_id))
    max_perception = max((int(row["clock"]) for row in perceptions), default=nonperception)
    if max_perception > nonperception:
        raise C12ForkHeld(
            "C12_PERCEPTION_ONLY_SUFFIX",
            f"parent={parent_branch_id} nonperception={nonperception} perception={max_perception}",
        )
    if not parent.get("actor_ids"):
        raise C12ForkHeld("C12_PARENT_ACTOR_SET_MISSING", parent_branch_id)
    return store.fork(parent_branch_id, new_branch_id)


__all__ = ["C12ForkHeld", "guard_fork", "load_c12"]
