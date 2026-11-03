from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

import install

install.install()

from bridge import join_e_compat
from bridge.join_e_source import JOIN_E_COMMIT, ensure_source

GRADE = "TEST_ONLY_SOURCEFREE_NOT_NATIVE"


def _run_encounter(
    *,
    join_e_root: Path,
    state: Path,
    disposition: str,
    mode: str,
    do_help: bool,
    out: Path,
) -> dict:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        sys.executable,
        "-B",
        str(RETURN / "tools" / "join_e_encounter.py"),
        "--join-e-root",
        str(join_e_root),
        "--state",
        str(state),
        "--disposition",
        disposition,
        "--mode",
        mode,
        "--out",
        str(out),
    ]
    if do_help:
        command.append("--do-help")
    completed = subprocess.run(
        command,
        cwd=str(RETURN),
        env=env,
        capture_output=True,
        text=True,
        timeout=180,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "JOIN_E_ENCOUNTER_FAILED:"
            + disposition
            + ":"
            + mode
            + ":"
            + completed.stderr[-2000:]
        )
    return json.loads(out.read_text(encoding="utf8"))


def _world_summary(bundle: dict, result: dict) -> dict:
    return {
        "outcome": join_e_compat.summary(result)["outcome"],
        "response_status": join_e_compat.summary(result)["response_status"],
        "target_proposals": join_e_compat.summary(result)["target_proposals"],
        "target_branch": join_e_compat.summary(result)["target_branch"],
        "target_reason": join_e_compat.summary(result)["target_reason"],
        "target_id": join_e_compat.summary(result)["target_id"],
        "s35_receipt_hash": join_e_compat.summary(result)["s35_receipt_hash"],
        "evidence_grade": join_e_compat.summary(result)["evidence_grade"],
        "actual_actor_input": join_e_compat.summary(result)["actual_actor_input"],
        "qualification": join_e_compat.summary(result)["qualification"],
        "hold_reason": join_e_compat.summary(result)["hold_reason"],
        "event_time": join_e_compat.summary(result)["event_time"],
        "clock": join_e_compat.summary(result)["clock"],
        "material_eligible": join_e_compat.summary(result)["material_eligible"],
        "material_refs": join_e_compat.summary(result)["material_refs"],
        "material_reason": join_e_compat.summary(result)["material_reason"],
        "access_granted": join_e_compat.summary(result)["access_granted"],
        "operation_only_would_grant": join_e_compat.summary(result)[
            "operation_only_material_grant"
        ],
        "public_source": bundle["source"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-out", default=str(
        RETURN / "evidence" / "join_e_s35_compat.json"
    ))
    parser.add_argument("--base-dir", default="")
    args = parser.parse_args()
    source_runtime = ensure_source()
    join_e_root = Path(source_runtime["return_path"])
    base = (
        Path(args.base_dir).resolve()
        if args.base_dir
        else Path(tempfile.mkdtemp(prefix="sorok-s35-joine-compat-"))
    )
    base.mkdir(parents=True, exist_ok=True)
    worlds = {}
    for disposition in ("PERFORMED", "OMITTED", "REFUSED"):
        state = base / disposition.lower()
        start = _run_encounter(
            join_e_root=join_e_root,
            state=state,
            disposition=disposition,
            mode="start",
            do_help=True,
            out=base / (disposition.lower() + "-start.json"),
        )
        action_kind = (
            "REQUEST_TOOL" if disposition == "PERFORMED" else "EXPLICIT_REFUSAL"
        )
        before_s35 = join_e_compat.store_hashes(start)
        baseline = join_e_compat.evaluate(start, controlled=False)
        controlled = join_e_compat.evaluate(
            start,
            controlled=True,
            perception_status="ACCESSIBLE",
            action_kind=action_kind,
            action_present=True,
        )
        perception_severed = join_e_compat.evaluate(
            start,
            controlled=True,
            perception_status="NOT_WITNESSED",
            action_kind=action_kind,
            action_present=True,
        )
        action_severed = join_e_compat.evaluate(
            start,
            controlled=True,
            perception_status="ACCESSIBLE",
            action_kind=action_kind,
            action_present=False,
        )
        after_s35 = join_e_compat.store_hashes(start)
        incompatibility = join_e_compat.full_pipeline_incompatibility(start)
        cold = _run_encounter(
            join_e_root=join_e_root,
            state=state,
            disposition=disposition,
            mode="open",
            do_help=True,
            out=base / (disposition.lower() + "-cold.json"),
        )
        cold_baseline = join_e_compat.evaluate(cold, controlled=False)
        cold_controlled = join_e_compat.evaluate(
            cold,
            controlled=True,
            perception_status="ACCESSIBLE",
            action_kind=action_kind,
            action_present=True,
        )
        worlds[disposition] = {
            "state_root": str(state),
            "source": start["source"],
            "source_binding": {
                "b_operation": start["source"].get("b_operation"),
                "b_performed": start["source"].get("b_performed"),
                "b_quantity": start["source"].get("b_quantity"),
                "material_feasible_after": start["source"].get(
                    "material_feasible_after"
                ),
                "b_event_hash": start["source"].get("b_event_hash"),
                "b_clock": start["source"].get("b_clock"),
            },
            "join_e": {
                "session_schema": start["session_schema"],
                "branch_id": start["branch_id"],
                "event_id": start["event_id"],
                "event_time": start["event_time"],
                "c12_branch_clock": start["c12"]["branch_clock"],
                "c12_root_clock": start["c12"]["root_clock"],
                "help": start["help"],
                "tools_remaining": start["tools_remaining"],
                "verify_ok": start["verify_ok"],
                "j_b_disposition": start["j_b_disposition"],
                "target_id": start["target_id"],
            },
            "material": {
                "performed_aware_access": join_e_compat.source_material_access(
                    start["source"]
                ),
                "operation_only_would_grant": join_e_compat.operation_only_material_grant(
                    start["source"]
                ),
                "eligible_material_at_c12_clock": baseline["built"][
                    "material_eligible"
                ],
                "material_reason": baseline["built"]["material_reason"],
            },
            "s35": {
                "baseline_typed_hold": _world_summary(start, baseline),
                "controlled_at_actual_clock": _world_summary(start, controlled),
                "perception_severed": _world_summary(
                    start, perception_severed
                ),
                "action_severed": _world_summary(start, action_severed),
                "full_pipeline_incompatibility": incompatibility,
            },
            "store_mutation": {
                "before_s35": before_s35,
                "after_s35": after_s35,
                "s35_mutated_store": before_s35 != after_s35,
            },
            "cold": {
                "session_verify_ok": cold["verify_ok"],
                "help": cold["help"],
                "tools_remaining": cold["tools_remaining"],
                "branch_clock": cold["c12"]["branch_clock"],
                "baseline_typed_hold": _world_summary(cold, cold_baseline),
                "controlled_at_actual_clock": _world_summary(
                    cold, cold_controlled
                ),
            },
        }
    operation_only_omitted_grant = bool(
        worlds["OMITTED"]["material"]["operation_only_would_grant"]
        and worlds["OMITTED"]["join_e"]["tools_remaining"]
    )
    summary = {
        "join_e_commit": JOIN_E_COMMIT,
        "source_runtime": source_runtime,
        "worlds": len(worlds),
        "performed_help_accept": worlds["PERFORMED"]["join_e"]["help"][
            "accepted"
        ],
        "omitted_help_accept": worlds["OMITTED"]["join_e"]["help"][
            "accepted"
        ],
        "refused_help_accept": worlds["REFUSED"]["join_e"]["help"][
            "accepted"
        ],
        "omitted_operation_only_grant_observed": operation_only_omitted_grant,
        "omitted_performed_aware_access": worlds["OMITTED"]["material"][
            "performed_aware_access"
        ],
        "same_root_full_pipeline_incompatibility": not worlds["PERFORMED"]["s35"][
            "full_pipeline_incompatibility"
        ]["same_root_c9_reexecution_lawful"],
        "controlled_same_root_outcomes": {
            key: worlds[key]["s35"]["controlled_at_actual_clock"]["outcome"]
            for key in worlds
        },
        "baseline_same_root_outcomes": {
            key: worlds[key]["s35"]["baseline_typed_hold"]["outcome"]
            for key in worlds
        },
        "targetless_all": all(
            worlds[key]["s35"]["baseline_typed_hold"]["target_branch"]
            == "NO_CHANGE"
            and worlds[key]["s35"]["baseline_typed_hold"]["target_reason"]
            == "NO_PROPOSAL"
            and worlds[key]["s35"]["baseline_typed_hold"]["target_proposals"]
            == 0
            for key in worlds
        ),
        "store_unmutated_by_s35": all(
            not worlds[key]["store_mutation"]["s35_mutated_store"]
            for key in worlds
        ),
        "cold_verify_all": all(
            worlds[key]["cold"]["session_verify_ok"] for key in worlds
        ),
        "s35_store_created": False,
    }
    evidence = {
        "schema": "SOROK_JOIN_E_X_S35_COMPAT@1",
        "grade": GRADE,
        "native": False,
        "base": "a6b1f10b37c0748b0b6880e1870a2c4f07844be9",
        "join_e_commit": JOIN_E_COMMIT,
        "source_runtime": source_runtime,
        "worlds": worlds,
        "summary": summary,
        "limits": [
            "no new S35 C9 store",
            "JOIN-E stores opened read-only by the S35 selector",
            "actual qualified A producer unavailable; controlled evidence TEST_ONLY",
            "same-root full C9 pipeline re-execution incompatibility recorded",
            "no native grants, psyche, provider calls or external checkout reads",
        ],
    }
    out = Path(args.evidence_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(evidence, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
