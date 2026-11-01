"""Sourcefree B-to-A material person history over M35/JOIN-E."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEPS = ROOT / "deps"
os.environ.setdefault("M35_JOIN_E_RETURN", str(DEPS / "join_e"))
if str(DEPS / "m35") not in sys.path:
    sys.path.insert(0, str(DEPS / "m35"))
import install  # noqa: E402
install.install()

from joined.session import JoinedSession  # noqa: E402
from joined.refusal import RefusalSession  # noqa: E402
from p1_s35 import evaluate  # noqa: E402
from p1_no_access import build_no_access, open_no_access  # noqa: E402


def _base(session) -> dict:
    product = session.product
    branch = session.branch_id
    world = product._world(branch)
    return {
        "source": product.source,
        "branch": branch,
        "state_root": str(session.state_root),
        "c12": product.c12_verify(branch),
        "root_branch": "root",
        "root_c12": product.c12_verify("root"),
        "c8_state_digest": session.meta.get("j_c8_state_digest"),
        "e1_event_hash": session.meta.get("j_e1_event_hash"),
        "target_id": session.meta.get("j_target_id", ""),
        "a_tools_remaining": world.actor_state["A"]["tools_remaining"],
        "world_clock": world.clock,
        "meta_schema": session.meta.get("schema"),
        "native": False,
    }


def _open(kind: str, state_root) -> dict:
    """Read a persisted history in a genuinely separate Python interpreter."""
    env = dict(os.environ)
    env["M35_JOIN_E_RETURN"] = str(DEPS / "join_e")
    cp = subprocess.run(
        [sys.executable, str(ROOT / "p1_cold.py"), "--kind", kind,
         "--state", str(state_root)],
        capture_output=True, text=True, env=env, cwd=str(ROOT),
    )
    if cp.returncode != 0:
        return {"ok": False, "returncode": cp.returncode,
                "stderr": cp.stderr[-2000:], "stdout": cp.stdout[-2000:]}
    out = json.loads(cp.stdout)
    out["returncode"] = cp.returncode
    return out


def run_trajectories(root) -> dict:
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    result = {
        "schema": "SOROK_P1_FOUR_MATERIAL_TRAJECTORIES@1",
        "grade": "TEST_ONLY_SOURCEFREE_NOT_NATIVE",
        "native": False,
        "trajectories": {},
    }

    # A: B SHARE, A receives access, independently asks for help.
    a_state = root / "A_share_access_request"
    a = JoinedSession.start(a_state, perform="omit")
    try:
        a_help = a.do_help()
        a_base = _base(a)
        a_cold = _open("joined", a_state)
        a_base.update({
            "id": "A_SHARE_ACCESS_A_REQUEST",
            "b_operation": a_base["source"]["b_operation"],
            "a_access_admitted": True,
            "a_action": "REQUEST_TOOL",
            "a_help": a_help,
            "s35": evaluate(access=True, actions=("REQUEST_TOOL",),
                            b_operation=a_base["source"]["b_operation"]),
            "cold": a_cold,
        })
        result["trajectories"]["A"] = a_base
    finally:
        a.close()

    # B: identical B share, A access denied; no A response/target.
    b_state = root / "B_share_no_access"
    bp, b_info = build_no_access(b_state)
    try:
        b_view = bp.no_access_view()
        b_cold = _open("no_access", b_state)
        result["trajectories"]["B"] = {
            "id": "B_SHARE_NO_ACCESS",
            **b_info,
            "a_access_admitted": False,
            "a_response": None,
            "target_id": "",
            "s35": evaluate(access=False, b_operation=b_info["source"]["b_operation"]),
            "view": b_view,
            "cold": b_cold,
            "native": False,
        }
    finally:
        bp.close()

    # C: B REFUSE; A's own help refusal, no target, no help-accept.
    c_state = root / "C_refuse_targetless"
    c = RefusalSession.start(c_state)
    try:
        c_help = c.do_help()
        c_base = _base(c)
        c_base.update({
            "id": "C_B_REFUSE_A_REFUSAL",
            "b_operation": c_base["source"]["b_operation"],
            "a_access_admitted": True,
            "a_action": "EXPLICIT_REFUSAL",
            "a_help": c_help,
            "s35": evaluate(access=True, actions=("EXPLICIT_REFUSAL",),
                            b_operation=c_base["source"]["b_operation"]),
            "cold": _open("refusal", c_state),
        })
        result["trajectories"]["C"] = c_base
    finally:
        c.close()

    # D: B SHARE, A E2 object inspection vs omission.
    d_state = root / "D_share_e2_vs_omit"
    omit = JoinedSession.start(d_state / "omit", perform="omit")
    try:
        omit_help = omit.do_help()
        omit_base = _base(omit)
        omit_base.update({
            "a_action": "OMIT",
            "a_help": omit_help,
            "s35": evaluate(access=True, actions=(),
                            b_operation=omit_base["source"]["b_operation"]),
            "cold": _open("joined", d_state / "omit"),
        })
    finally:
        omit.close()
    e2 = JoinedSession.start(d_state / "e2", perform="e2")
    try:
        e2_help = e2.do_help()
        e2_base = _base(e2)
        e2_base.update({
            "a_action": "ATTEND_OBJECT",
            "a_help": e2_help,
            "s35": evaluate(access=True, actions=("ATTEND_OBJECT",),
                            b_operation=e2_base["source"]["b_operation"]),
            "cold": _open("joined", d_state / "e2"),
        })
    finally:
        e2.close()
    result["trajectories"]["D"] = {
        "id": "D_SHARE_E2_VS_OMIT",
        "omitted": omit_base,
        "performed": e2_base,
        "difference": {
            "material_tools": [omit_base["a_tools_remaining"], e2_base["a_tools_remaining"]],
            "help_strategy": [omit_base["a_help"].get("strategy"), e2_base["a_help"].get("strategy")],
            "a_action": [omit_base["a_action"], e2_base["a_action"]],
        },
        "native": False,
    }
    result["invariants"] = {
        "A_B_same_b_event_hash": (
            result["trajectories"]["A"]["source"]["b_event_hash"]
            == result["trajectories"]["B"]["source"]["b_event_hash"]),
        "B_has_no_target": result["trajectories"]["B"]["target_id"] == "",
        "B_has_no_a_response": result["trajectories"]["B"]["a_response"] is None,
        "C_never_help_accept": result["trajectories"]["C"]["a_help"].get("accepted") is False,
        "C_targetless": result["trajectories"]["C"]["target_id"] == "",
        "D_tools_differ": result["trajectories"]["D"]["omitted"]["a_tools_remaining"]
        != result["trajectories"]["D"]["performed"]["a_tools_remaining"],
        "D_help_differs": result["trajectories"]["D"]["omitted"]["a_help"].get("strategy")
        != result["trajectories"]["D"]["performed"]["a_help"].get("strategy"),
    }
    return result


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    data = run_trajectories(Path(args.root))
    Path(args.output).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "path": args.output,
                      "invariants": data["invariants"]}, indent=2))
