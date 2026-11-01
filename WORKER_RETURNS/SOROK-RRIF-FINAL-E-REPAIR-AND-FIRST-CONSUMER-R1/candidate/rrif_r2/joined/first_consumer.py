"""The RRIF-E executed sourcefree first consumer.

Same-root path: R2 JOIN-E actor source -> material event -> C9 target -> C12
continuation -> cold/fork -> read-only encounter. The C9/C12-R3 composite is
kept as a typed incompatible owner hold; CP-A5 is consumed on its own sourcefree
root and is not welded by relabeling.
"""
from __future__ import annotations

from pathlib import Path
import json
import os
import subprocess
import sys
from typing import Any

from .c12_custody import coordinated_guard_report
import sys
from .c12_verify_repair import upstream_defect_is_reproducible, verify_branch_chain_repaired
from .c9c12_compat import read_c9c12_compatibility
from .session import JoinedSession

R2 = Path(__file__).resolve().parents[1]
EXT = R2 / "rrif_r3_extension"
from r26e.c12_integrity import QualifiedC12Store

_EXT = Path(__file__).resolve().parents[1] / "rrif_r3_extension"
if str(_EXT) not in sys.path:
    sys.path.insert(0, str(_EXT))


def _same_root(root: str | Path) -> dict[str, Any]:
    state = Path(root) / "same-root"
    session = JoinedSession.start(state, perform="omit", attention="focused")
    try:
        said = session.say("Hello. I just moved in.")
        helped = session.do_help()
        attended = session.attend()
        waited = session.wait(30)
        fork = session.fork_alt("alt")
        product_root = session.product.root
        root_verify = session.product.c12_verify("root")
        alt_verify = session.product.c12_verify("alt")
        source = dict(session.product.source)
        c8_state_digest = session.meta.get("j_c8_state_digest")
        target_id = session.meta.get("j_target_id")
    finally:
        session.close()

    cold = JoinedSession.open(state)
    try:
        cold_verify = cold.verify()
        returned = cold.return_session()
        cold_branch = cold.branch_id
    finally:
        cold.close()

    db_path = product_root / "c12.sqlite"
    qualified = QualifiedC12Store(db_path)
    try:
        verifier = upstream_defect_is_reproducible(qualified, "root")
        repaired_root = verify_branch_chain_repaired(qualified, "root")
        repaired_alt = verify_branch_chain_repaired(qualified, "alt")
        qualified_root = qualified.verify("root")
    finally:
        qualified.close()
    custody = coordinated_guard_report(db_path, branch_id="root")
    compatibility = read_c9c12_compatibility(product_root)
    return {
        "state_root": str(state),
        "product_root": str(product_root),
        "c12_path": str(db_path),
        "material_event": {
            "source_operation": source.get("b_operation"),
            "b_performed": source.get("b_performed"),
            "c8_state_digest": c8_state_digest,
            "target_id": target_id,
        },
        "encounter": {
            "say_strategy": said.get("strategy"),
            "help_accepted": helped.get("accepted"),
            "help_strategy": helped.get("strategy"),
            "attend_status": attended.get("status"),
            "wait_clock": waited.get("clock"),
            "scene_open_after_wait": waited.get("scene_open"),
            "return_scene_open": returned.get("scene_open"),
        },
        "fork": {"created_branch": "alt", "receipt": fork.get("branch", {}).get("branch_id"), "cold_branch": cold_branch},
        "c12": {
            "root_verify": root_verify,
            "alt_verify": alt_verify,
            "qualified_root": qualified_root,
            "repaired_root": repaired_root,
            "repaired_alt": repaired_alt,
            "upstream_defect_reproduced": verifier,
            "custody": custody,
        },
        "cold_verify_ok": cold_verify.get("ok") is True,
        "same_root_c9_c12": {
            "status": "SAME_ROOT_C9_C12_SOURCEFREE_GREEN",
            "c9_actor_projection": "HELD_NOT_PRESENT",
            "target_id": target_id,
            "native": False,
        },
        "c9c12_compatibility": compatibility,
    }


def _cp_a5_probe(root: Path) -> dict[str, Any]:
    """Run the separate CP-A5 consumer in a clean process (no import pollution)."""
    repo = Path(__file__).resolve().parents[5]
    env = {
        **os.environ,
        "PYTHONPATH": f"{R2}{os.pathsep}{EXT}{os.pathsep}{repo}",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
    }
    code = (
        "import json\n"
        "from cp_a5_consumer import ask_cp_a5, run_cp_a5_consumer\n"
        f"root = {str(root)!r}\n"
        "receipt = run_cp_a5_consumer(root)\n"
        "answer = ask_cp_a5(root, 'What did B do at the market?')\n"
        "print(json.dumps({'assertion_status': receipt.get('status'),\n"
        " 'decision': receipt.get('decision'),\n"
        " 'market_status': (receipt.get('encounter') or {}).get('market', {}).get('status'),\n"
        " 'ask_status': answer.get('status'), 'read_only': answer.get('read_only')}))\n"
    )
    run = subprocess.run(
        [sys.executable, "-B", "-c", code], cwd=str(repo), env=env,
        text=True, capture_output=True, timeout=120)
    if run.returncode != 0:
        return {"status": "ERROR", "reason": run.stderr[-2000:], "same_root_with_r2": False}
    return json.loads(run.stdout)


def run_first_consumer(root: str | Path) -> dict[str, Any]:
    """Execute same-root C9/C12/JOIN and separate CP-A5 consumers."""
    root = Path(root)
    same_root = _same_root(root)
    cp_a5 = _cp_a5_probe(root / "cp-a5")
    return {
        "schema": "RRIF_E_FIRST_CONSUMER_RECEIPT@1",
        "status": "PASS_PARTIAL_SAME_ROOT_C9_C12__C9_ACTOR_OWNER_HELD__CP_A5_SEPARATE_ROOT",
        "same_root": same_root,
        "cp_a5": {
            **cp_a5,
            "same_root_with_r2": False,
        },
        "authority": {
            "native_person": False,
            "native_c8_c9_c12": False,
            "native_cp_a5": False,
            "owner_adoption": False,
            "external_anchor": "OWNER_ANCHOR_REQUIRED",
        },
    }


__all__ = ["run_first_consumer"]
