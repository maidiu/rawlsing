"""Generate BP4 machine-readable evidence: product, cold replay, forks, severances."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
REPO = RET.parents[1]
EVID = RET / "evidence"
EVID.mkdir(exist_ok=True)
sys.path.insert(0, str(RET))

from bp4.c10 import C10Refusal, _verify_world, receive  # noqa: E402
from bp4.canon import digest  # noqa: E402
from bp4.perception import render_requested_event  # noqa: E402
from bp4.product import BP4Product  # noqa: E402


def blob(path: Path) -> dict:
    raw = path.read_bytes()
    try:
        rel = str(path.resolve().relative_to(REPO.resolve()))
    except ValueError:
        rel = str(path.relative_to(RET))
    return {"path": rel, "git_blob": subprocess.run(
        ["git", "hash-object", str(path)], cwd=str(REPO), capture_output=True,
        text=True, check=True).stdout.strip(),
        "sha256": hashlib.sha256(raw).hexdigest()}


def product_evidence() -> dict:
    root = Path(tempfile.mkdtemp(prefix="bp4-positive-", dir=str(RET / "runtime")))
    p = BP4Product(root)
    try:
        steps = {}
        steps["A0"] = p.observe()
        steps["A1_SAY"] = p.say("I am here about the bench.")
        steps["A1_INSPECT"] = p.inspect()
        steps["A1_REPAIR"] = p.repair()
        steps["A2_WAIT"] = p.wait(30)
        steps["A3_OTHER"] = p.other()
        steps["A2_TRAVEL"] = p.travel("market")
        steps["A2_ATTEND"] = p.attend()
        steps["A2_REENTRY"] = p.reenter()
        steps["DENY_REPAIR"] = p.repair()
        steps["ADDRESS_OTHER_PRESENT"] = p.address_other("Are you there?")
        evidence = {
            "schema": "SOROK_BP4_PRODUCT_EVIDENCE@1",
            "grade": "TEST_ONLY_SOURCEFREE_TECHNICAL_ALPHA",
            "native_claims": steps["A0"]["native_claims"],
            "c9": steps["A0"]["c9"],
            "c8": steps["A0"]["c8"],
            "steps": {k: {"status": v.get("status"), "clock": v.get("clock"),
                          "admitted": v.get("admitted"),
                          "claims": [c["kind"] for c in v.get("claims", [])],
                          "code": v.get("code"),
                          "completed_units": v.get("public", {}).get("completed_units")}
                      for k, v in steps.items()},
            "full_steps": steps,
            "first_actual_downstream_consumer": (
                "Cold-reopened C12 actor history produces a changed A0/A2 claim "
                "because a source-owned offscreen E2/repair event occurred without "
                "user instruction and was later lawfully perceived."),
            "root": str(root),
        }
        (EVID / "product_positive.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
        return evidence
    finally:
        p.close()


def cold_replay() -> dict:
    root = Path(tempfile.mkdtemp(prefix="bp4-cold-", dir=str(RET / "runtime")))
    worker = RET / "repro" / "cold_worker.py"
    build = subprocess.run([sys.executable, "-B", str(worker), "build", str(root)],
                           capture_output=True, text=True, check=True)
    observe = subprocess.run([sys.executable, "-B", str(worker), "observe", str(root)],
                             capture_output=True, text=True, check=True)
    built = json.loads(build.stdout.strip().splitlines()[-1])
    reopened = json.loads(observe.stdout.strip().splitlines()[-1])
    evidence = {
        "schema": "SOROK_BP4_COLD_REPLAY@1",
        "build_pid_mode": "fresh interpreter", "observe_pid_mode": "fresh interpreter",
        "build_status": built.get("status"), "observe_status": reopened.get("status"),
        "clock_equal": built.get("clock") == reopened.get("clock"),
        "claims_equal": [c["event_id"] for c in built.get("claims", [])]
        == [c["event_id"] for c in reopened.get("claims", [])],
        "branch_equal": built.get("branch_id") == reopened.get("branch_id"),
        "c9_equal": built.get("c9") == reopened.get("c9"),
        "c8_equal": built.get("c8") == reopened.get("c8"),
        "built_clock": built.get("clock"), "reopened_clock": reopened.get("clock"),
        "claim_kinds": [c["kind"] for c in reopened.get("claims", [])],
    }
    (EVID / "cold_replay.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    return evidence


def fork_evidence() -> dict:
    root = Path(tempfile.mkdtemp(prefix="bp4-fork-", dir=str(RET / "runtime")))
    p = BP4Product(root)
    try:
        p.say("fork point")
        fork = p.fork("branch_leave")
        shared_before = p.store.shared_root_equal("root", "branch_leave")
        p.use("branch_leave")
        p.leave_tool()
        p.wait(30)
        leave = p.other()
        p.use("root")
        p.take_tool()
        p.wait(30)
        take = p.other()
        shared_after = p.store.shared_root_equal("root", "branch_leave")
        evidence = {
            "schema": "SOROK_BP4_FORK_DIVERGENCE@1",
            "fork": fork,
            "shared_root_equal": shared_before["equal"] and shared_after["equal"],
            "shared_before": shared_before, "shared_after": shared_after,
            "leave_branch": leave["public"],
            "take_branch": take["public"],
            "diverged": leave["public"]["completed_units"] != take["public"]["completed_units"],
            "branch_private_work_events": (
                leave["public"]["public_work_events"]
                != take["public"]["public_work_events"]),
        }
        (EVID / "fork_divergence.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
        return evidence
    finally:
        p.close()


def severance_evidence() -> dict:
    root = Path(tempfile.mkdtemp(prefix="bp4-sev-", dir=str(RET / "runtime")))
    p = BP4Product(root)
    trials = []
    try:
        # 1 C9 target
        baseline = p.observe()
        copy = root / "c9_missing.sqlite"
        shutil.copy(p.seed.c9_path, copy)
        with sqlite3.connect(copy) as db:
            db.execute("DELETE FROM target_state")
            db.commit()
        original = p.seed.c9_path
        p.seed.c9_path = copy
        try:
            fault = p.observe()
        finally:
            p.seed.c9_path = original
        restored = p.observe()
        trials.append({
            "edge": "C9_TARGET_E2_READ",
            "baseline": baseline.get("status"), "fault": fault.get("status"),
            "fault_code": fault.get("code"), "restored": restored.get("status"),
            "same_observation": "product.observe c9.target_id/state_hash",
            "pass": baseline.get("status") == "OK" and fault.get("status") == "HELD"
            and restored.get("status") == "OK",
        })
        # 2 BP1 source
        baseline = receive(p.seed, p.store, "root", actor_id="A")
        try:
            receive(p.seed, p.store, "root", actor_id="A", expected_a_hash="0" * 64)
            fault = "NO_REFUSAL"
        except C10Refusal as exc:
            fault = exc.code
        restored = receive(p.seed, p.store, "root", actor_id="A")
        trials.append({
            "edge": "BP1_ACTOR_HISTORICAL_SOURCE",
            "baseline": "OK" if baseline.receipt["c9_target_id"] else "HELD",
            "fault": fault, "restored": "OK" if restored.receipt["c9_target_id"] else "HELD",
            "same_observation": "C10 receive actor snapshot authentication",
            "pass": fault == "BP1_ACTOR_SOURCE_NOT_AUTHENTICATED",
        })
        # 3 BP3 receipt
        def bad_verifier():
            raise RuntimeError("substituted proof")
        baseline = receive(p.seed, p.store, "root", actor_id="A")
        try:
            receive(p.seed, p.store, "root", actor_id="A", proof_verifier=bad_verifier)
            fault = "NO_REFUSAL"
        except C10Refusal as exc:
            fault = exc.code
        restored = receive(p.seed, p.store, "root", actor_id="A")
        trials.append({
            "edge": "BP3_VERIFIED_C8_RECEIPT",
            "baseline": "OK" if baseline.c8_ingress["occurrence_ids"] else "HELD",
            "fault": fault, "restored": "OK" if restored.c8_ingress["occurrence_ids"] else "HELD",
            "same_observation": "C10 receive BP3 proof/anchor verification",
            "pass": fault == "BP3_PROOF_INVALID",
        })
        # 4 actor perception boundary: lawful READY -> denied access -> restored READY
        p.wait(30)
        p.travel("market")
        p.attend()
        state = p._runtime_state("root")
        events = p.store.world_events("root")
        offscreen = next(e for e in events if e["kind"] == "OFFSCREEN_REPAIR")
        visible = render_requested_event("A", 40, state, events, offscreen["event_id"])
        without = dict(state)
        without["knowledge"] = dict(state["knowledge"])
        without["knowledge"]["A"] = [i for i in state["knowledge"]["A"]
                                     if i != offscreen["event_id"]]
        hidden = render_requested_event("A", 40, without, events, offscreen["event_id"])
        restored_visible = render_requested_event("A", 40, state, events, offscreen["event_id"])
        trials.append({
            "edge": "ACTOR_KNOWLEDGE_PERCEPTION_BOUNDARY",
            "baseline": visible["state"], "fault": hidden["state"],
            "restored": restored_visible["state"],
            "same_observation": "render_requested_event",
            "pass": visible["state"] == "READY" and hidden["state"] == "NONRENDERABLE"
            and restored_visible["state"] == "READY",
        })
        # 5 offscreen owner receipt
        state = p._runtime_state("root")
        baseline_world = _verify_world(state)
        tampered = {"world": dict(state["world"]), "actors": state["actors"]}
        tampered["world"]["events"] = [dict(e) for e in state["world"]["events"]]
        target = next(e for e in tampered["world"]["events"]
                      if e["kind"] == "OFFSCREEN_REPAIR")
        target["owner_receipt"] = dict(target["owner_receipt"])
        target["owner_receipt"]["owner_ref"] = "SELF"
        target["hash"] = digest({k: v for k, v in target.items() if k != "hash"})
        tampered["world"]["hash"] = digest({k: v for k, v in tampered["world"].items()
                                            if k != "hash"})
        try:
            _verify_world(tampered)
            fault = "NO_REFUSAL"
        except C10Refusal as exc:
            fault = exc.code
        restored_world = _verify_world(state)
        trials.append({
            "edge": "INDEPENDENT_OFFSCREEN_PERFORMER",
            "baseline": f"OK:{baseline_world.clock}", "fault": fault,
            "restored": f"OK:{restored_world.clock}",
            "same_observation": "C10 _verify_world owner receipt",
            "pass": fault == "WORLD_OWNER_RECEIPT_INVALID",
        })
        evidence = {"schema": "SOROK_BP4_SEVERANCE_TRIALS@1", "trials": trials,
                    "all_pass": all(t["pass"] for t in trials)}
        (EVID / "severance_trials.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
        return evidence
    finally:
        p.close()


def provenance() -> dict:
    rows = [blob(path) for path in sorted(
        list((RET / "bp4").glob("*.py")) + list((RET / "tests").glob("*.py"))
        + list((RET / "vendor" / "bp1").glob("*.py"))
        + list((RET / "vendor" / "c9r" / "candidate").glob("*.py"))
        + [RET / "vendor" / "bp3" / "c8_exclusive_writer.py",
           RET / "vendor" / "bp3" / "c9_event_ingress.py",
           REPO / "rawlsing_next" / "m6_actor_safe_expression.py",
           REPO / "rawlsing_next" / "m5_runtime_rsc_peer_prior.py"]
    )]
    pins = {
        "bp1_source": "b4e07ef515e9464c7bc8177e394ac29f4a4af72a",
        "bp1_documentation": "be9f3a9e1bb4c61a8c3ec89a9a5d18b4a10762a2",
        "bp3_source": "7faaa0722336231335d974bebc70c1282c79ce3e",
        "c9r_source": "6fa2939972ce5a2c0cc4f2b033946b276f1c2934",
        "c9ri_acceptance": "5753d9b4f8fad9f2175b1e285733f95bb8387888",
        "pa0_atlas": "3b39c86b376efff8c11833b8451c1791adddb9bc",
        "bp4_startup": "e699fed59925a3d7b3f02805f85771ae2df32be8",
        "bp2_commission": "19503a3ea09bdf840a5ce98a9697650c387787fa",
    }
    evidence = {"schema": "SOROK_BP4_SOURCE_PROVENANCE@1", "pins": pins, "rows": rows}
    (EVID / "source_provenance.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    return evidence


def main() -> int:
    (RET / "runtime").mkdir(exist_ok=True)
    product = product_evidence()
    cold = cold_replay()
    fork = fork_evidence()
    sev = severance_evidence()
    prov = provenance()
    print(json.dumps({
        "product": product["steps"],
        "cold_clock_equal": cold["clock_equal"],
        "cold_claims_equal": cold["claims_equal"],
        "fork_shared": fork["shared_root_equal"],
        "fork_diverged": fork["diverged"],
        "severance_all_pass": sev["all_pass"],
        "source_rows": len(prov["rows"]),
    }, indent=2))
    return 0 if sev["all_pass"] and cold["clock_equal"] and cold["claims_equal"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
