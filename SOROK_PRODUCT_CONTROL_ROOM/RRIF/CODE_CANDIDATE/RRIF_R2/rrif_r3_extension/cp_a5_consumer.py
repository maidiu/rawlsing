"""RRIF-R3 actual CP-A5 read-only encounter consumer.

This module is the new sourcefree consumer beyond the unchanged RRIF-R2 JOIN-E
root. It executes the recovered CP-A5-R2 `build_cp_life` and
`EncounterReader.ask` over a CP-A5 sourcefree continued-person product.

It does not attach the CP-A5 product to the R2 same-root C9/C12 store because
that exact source cut is incompatible (actor/c8 origin mismatch). See
03_C9_R3B_C9C12_R2_JOIN_VERSION_NEGATIVE_COURT.json.
"""
from __future__ import annotations

import importlib
from pathlib import Path
import sys
from typing import Any

RUNTIME = Path(__file__).resolve().parent / "cp_a5_runtime"
_runtime = str(RUNTIME)
if _runtime not in sys.path:
    sys.path.insert(0, _runtime)


def _install() -> None:
    if _runtime in sys.path:
        sys.path.remove(_runtime)
    sys.path.insert(0, _runtime)
    import bp2p4

    expected = (RUNTIME / "bp2p4").resolve()
    if Path(bp2p4.__file__).resolve().parent != expected:
        for name in [name for name in sys.modules
                     if name == "bp2p4" or name.startswith("bp2p4.")]:
            del sys.modules[name]
        importlib.invalidate_caches()
        import bp2p4
    bp2p4.install()


def run_cp_a5_consumer(
    root: str | Path,
    *,
    include_b_activity: bool = True,
    grant_a_access: bool = True,
    custody_rule: bool = True,
    context_profile: str = "cross_context",
) -> dict[str, Any]:
    """Build the sourcefree CP-A5 life and exercise the actual read-only consumer."""
    _install()
    from bp2p4 import reunion
    from cp_a5.assertion import run_a5_assertion
    from cp_a5.scenario import build_cp_life

    root = Path(root)
    artifacts = reunion.build_fresh(root / "joined")
    build_cp_life(
        root,
        artifacts,
        include_b_activity=include_b_activity,
        grant_a_access=grant_a_access,
        custody_rule=custody_rule,
        context_profile=context_profile,
    )
    return run_a5_assertion(root)


def ask_cp_a5(root: str | Path, question: str, *, branch_id: str = "root") -> dict[str, Any]:
    """Use the recovered CP-A5 EncounterReader.ask directly."""
    _install()
    from cp_a5.encounter import EncounterReader

    with EncounterReader(root, branch_id=branch_id) as reader:
        return reader.ask(question)


def view_cp_a5(root: str | Path, *, branch_id: str = "root") -> dict[str, Any]:
    _install()
    from cp_a5.encounter import EncounterReader

    with EncounterReader(root, branch_id=branch_id) as reader:
        return reader.view()


__all__ = ["ask_cp_a5", "run_cp_a5_consumer", "view_cp_a5"]
