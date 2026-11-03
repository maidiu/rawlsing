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

from bridge import access, occurrence_consumer, s39_source
from bridge.join_e_compat import store_hashes
from bridge.join_e_source import JOIN_E_COMMIT, ensure_source

GRADE = "TEST_ONLY_SOURCEFREE_NOT_NATIVE"
PROGRAMMA_COMMIT = "6fdebcdae4e524ebda929c613da13ccc0fde097a"
BASE = "eb489dcaac4fb6362b8a3ed1d78d1f1654950563"


def _run_encounter(
    *,
    join_e_root: Path,
    state: Path,
    disposition: str,
    mode: str,
    perform: str,
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
        "--perform",
        perform,
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
            "ACTUAL_A_ENCOUNTER_FAILED:"
            + disposition
            + ":"
            + mode
            + ":"
            + completed.stderr[-2000:]
        )
    return json.loads(out.read_text(encoding="utf8"))


def _a_analysis(bundle: dict, occurrence: dict) -> dict:
    a = bundle.get("a_evidence") or {}
    episodes = a.get("a_action_episodes") or []
    perceptions = a.get("a_perceptions") or []
    world_events = a.get("world_events") or []
    action_rows = [
        row
        for row in episodes
        if (row.get("body") or {}).get("action") == "material_inspect"
    ]
    performed_rows = [
        row for row in action_rows
        if (row.get("body") or {}).get("attempted") is True
        and (row.get("body") or {}).get("admitted") is True
    ]
    omission_rows = [
        row for row in action_rows
        if (row.get("body") or {}).get("attempted") is False
    ]
    action_event_ids = [
        (row.get("body") or {}).get("event_id")
        for row in performed_rows
        if (row.get("body") or {}).get("event_id")
    ]
    action_world_events = [
        row for row in world_events if row.get("event_id") in action_event_ids
    ]
    action_clocks = [int(row.get("clock", 0)) for row in action_world_events]
    own_action_perceptions = [
        row for row in perceptions
        if row.get("channel") == "own_action"
        and row.get("event_id") in action_event_ids
    ]
    e1_hash = bundle["e1_event_hash"]
    e1_id = bundle["event_id"]
    action_bound_to_e1 = any(
        (row.get("body") or {}).get("e1_event_hash") == e1_hash
        or (row.get("body") or {}).get("e1_event_id") == e1_id
        for row in action_rows
    )
    a_local_observation_of_e1 = any(
        row.get("event_id") in {e1_hash, e1_id} for row in perceptions
    )
    gm01 = a.get("gm01_source") or {}
    return {
        "a_action_rows": len(action_rows),
        "a_action_performed_rows": len(performed_rows),
        "a_omission_rows": len(omission_rows),
        "a_action_event_ids": action_event_ids,
        "a_action_event_clocks": action_clocks,
        "a_own_action_perceptions": own_action_perceptions,
        "a_perception_event_ids": [row.get("event_id") for row in perceptions],
        "a_perception_clocks": [row.get("clock") for row in perceptions],
        "e1_event_id": e1_id,
        "e1_event_hash": e1_hash,
        "event_clock": int(occurrence["event_clock"]),
        "branch_clock": int(occurrence["branch_clock"]),
        "action_bound_to_e1": action_bound_to_e1,
        "a_local_observation_of_e1": a_local_observation_of_e1,
        "action_clock_matches_e1": bool(action_clocks)
        and all(clock == int(occurrence["event_clock"]) for clock in action_clocks),
        "action_order_persisted": False,
        "action_event_clock_lt_e1": bool(action_clocks)
        and all(clock < int(occurrence["event_clock"]) for clock in action_clocks),
        "gm01_a_e1_ref": gm01.get("a_e1_ref"),
        "gm01_a_e1_hash": gm01.get("a_e1_hash"),
        "gm01_a_e1_clock": gm01.get("a_e1_clock"),
        "gm01_a_e2_ref": gm01.get("a_e2_ref"),
        "gm01_a_e2_hash": gm01.get("a_e2_hash"),
        "gm01_a_e2_performed": gm01.get("a_e2_performed"),
        "gm01_b_event_ref": gm01.get("b_event_ref"),
        "gm01_b_event_hash": gm01.get("b_event_hash"),
        "gm01_b_performed": gm01.get("b_performed"),
        "fixture_grade": "TEST_ONLY_SOURCEFREE_R31J_A_FIXTURE_NOT_ACTUAL",
        "actual_a": False,
    }


def _candidate_receipts(bundle: dict, occurrence: dict, analysis: dict) -> dict:
    context = occurrence_consumer.build_context(occurrence)["context"]
    perception = None
    action = None
    if analysis["a_own_action_perceptions"]:
        row = analysis["a_own_action_perceptions"][0]
        perception = access.make_a_local_perception_receipt(
            context=context,
            source_ref="TEST_ONLY_ADP017_ACCESS_S35_A_LOCAL_PERCEPTION_R31J",
            perception_ref="TEST_ONLY_R31J_A_OWN_ACTION_PERCEPTION",
            access_status="ACCESSIBLE",
            perceived_at=int(row["clock"]),
            scene=context.scene,
            content={
                "producer": "R31J_A_OWN_ACTION_PERCEPTION",
                "action_event_id": row["event_id"],
                "fixture_not_actual": True,
                "e1_event_hash": analysis["e1_event_hash"],
            },
            evidence_grade=access.S35_GRADE_CONTROLLED,
            actual_actor_input=False,
            qualification=access.S35_QUALIFICATION_CONTROLLED,
        )
    if analysis["a_action_event_ids"]:
        action = access.make_a_owned_action_receipt(
            context=context,
            source_ref="TEST_ONLY_A_ACTION_S35_A_OWNED_R31J_FIXTURE",
            action_ref=analysis["a_action_event_ids"][0],
            action_kind="ATTEND_OBJECT",
            performed=True,
            action_time=int(analysis["a_action_event_clocks"][0]),
            content={
                "producer": "R31J_MATERIAL_INSPECT_DO",
                "action_event_id": analysis["a_action_event_ids"][0],
                "fixture_not_actual": True,
                "e1_event_hash": analysis["e1_event_hash"],
            },
            evidence_grade=access.S35_GRADE_CONTROLLED,
            actual_actor_input=False,
            qualification=access.S35_QUALIFICATION_CONTROLLED,
        )
    return {"perception": perception, "action": action}


def _evaluate(occurrence, *, perception=None, action=None) -> dict:
    result = occurrence_consumer.evaluate_occurrence(
        occurrence,
        perception_receipt=perception,
        action_receipt=action,
    )
    return occurrence_consumer.summary(result)


def _world(bundle: dict) -> dict:
    read = occurrence_consumer.read_occurrence(bundle)
    if not read.ok:
        return {
            "occurrence_ok": False,
            "missing_contract": read.missing_contract,
        }
    occurrence = read.occurrence
    analysis = _a_analysis(bundle, occurrence)
    candidates = _candidate_receipts(bundle, occurrence, analysis)
    controlled_perception = access.make_a_local_perception_receipt(
        context=occurrence_consumer.build_context(occurrence)["context"],
        source_ref="TEST_ONLY_ADP017_ACCESS_S35_A_LOCAL_PERCEPTION",
        perception_ref="TEST_ONLY_ACTUAL_A_CONTROLLED_PERCEPTION",
        access_status="ACCESSIBLE",
        perceived_at=int(occurrence["event_clock"]),
        scene=str((occurrence["event"].get("content") or {}).get("scene", "")),
        content={"controlled": True},
        evidence_grade=access.S35_GRADE_CONTROLLED,
        actual_actor_input=False,
        qualification=access.S35_QUALIFICATION_CONTROLLED,
    )
    controlled_action = access.make_a_owned_action_receipt(
        context=occurrence_consumer.build_context(occurrence)["context"],
        source_ref="TEST_ONLY_A_ACTION_S35_A_OWNED",
        action_ref="TEST_ONLY_ACTUAL_A_CONTROLLED_ACTION",
        action_kind="ATTEND_OBJECT",
        performed=True,
        action_time=int(occurrence["event_clock"]),
        content={"controlled": True},
        evidence_grade=access.S35_GRADE_CONTROLLED,
        actual_actor_input=False,
        qualification=access.S35_QUALIFICATION_CONTROLLED,
    )
    return {
        "occurrence_ok": True,
        "occurrence": {
            "event_hash": occurrence["event_hash"],
            "event_id": occurrence["event_id"],
            "event_clock": occurrence["event_clock"],
            "branch_clock": occurrence["branch_clock"],
            "clock_binding_hash": occurrence["clock_binding_hash"],
            "root_branch_hash": occurrence["root_branch_hash"],
            "branch_hash": occurrence["branch_hash"],
            "checks": dict(read.checks),
        },
        "a_analysis": analysis,
        "candidate_receipts": {
            "perception_present": candidates["perception"] is not None,
            "action_present": candidates["action"] is not None,
            "perception_hash": (candidates["perception"] or {}).get("hash", ""),
            "action_hash": (candidates["action"] or {}).get("hash", ""),
        },
        "wired_actual_a_candidate": {
            "perception_only": _evaluate(
                occurrence, perception=candidates["perception"]
            ),
            "action_only_with_controlled_perception": _evaluate(
                occurrence,
                perception=controlled_perception,
                action=candidates["action"],
            ),
            "both_candidate": _evaluate(
                occurrence,
                perception=candidates["perception"],
                action=candidates["action"],
            ),
        },
        "controlled_integration": {
            "intact": _evaluate(
                occurrence,
                perception=controlled_perception,
                action=controlled_action,
            ),
            "perception_severed": _evaluate(
                occurrence,
                perception=None,
                action=controlled_action,
            ),
            "action_severed": _evaluate(
                occurrence,
                perception=controlled_perception,
                action=None,
            ),
            "restored": _evaluate(
                occurrence,
                perception=controlled_perception,
                action=controlled_action,
            ),
        },
        "missing_source_owner_contract": occurrence_consumer.missing_source_owner_contract(
            event_hash=occurrence["event_hash"],
            event_id=str(occurrence["event_id"]),
            event_clock=occurrence["event_clock"],
            branch_clock=occurrence["branch_clock"],
            root_id="root",
            branch_id=occurrence["branch_id"],
            missing_fields=(
                "A_LOCAL_OBSERVATION_RECEIPT_OF_E1",
                "A_ACTION_OR_OMISSION_RECEIPT_BOUND_TO_E1_CLOCK_AND_ORDER",
                "QUALIFIED_A_SOURCE_OWNER_RECEIPT",
            ),
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--evidence-out",
        default=str(RETURN / "evidence" / "actual_a_evidence.json"),
    )
    parser.add_argument("--base-dir", default="")
    args = parser.parse_args()
    source_runtime = ensure_source()
    join_e_root = Path(source_runtime["return_path"])
    base = (
        Path(args.base_dir).resolve()
        if args.base_dir
        else Path(tempfile.mkdtemp(prefix="sorok-s35-actual-a-"))
    )
    base.mkdir(parents=True, exist_ok=True)
    worlds = {}
    bundles = {}
    for disposition, perform in (
        ("PERFORMED", "e2"),
        ("PERFORMED", "omit"),
        ("REFUSED", "omit"),
    ):
        key = disposition.lower() + "-" + perform
        state = base / key
        start = _run_encounter(
            join_e_root=join_e_root,
            state=state,
            disposition=disposition,
            mode="start",
            perform=perform,
            do_help=True,
            out=base / (key + "-start.json"),
        )
        bundles[key] = start
        before = store_hashes(start)
        world = _world(start)
        after = store_hashes(start)
        cold = _run_encounter(
            join_e_root=join_e_root,
            state=state,
            disposition=disposition,
            mode="open",
            perform=perform,
            do_help=True,
            out=base / (key + "-cold.json"),
        )
        cold_world = _world(cold)
        worlds[key] = {
            "state_root": str(state),
            "source_binding": {
                "b_operation": start["source"].get("b_operation"),
                "b_performed": start["source"].get("b_performed"),
                "b_quantity": start["source"].get("b_quantity"),
                "material_feasible_after": start["source"].get(
                    "material_feasible_after"
                ),
            },
            "join_e": {
                "help": start["help"],
                "tools_remaining": start["tools_remaining"],
                "verify_ok": start["verify_ok"],
                "j_b_disposition": start["j_b_disposition"],
                "event_time": start["event_time"],
                "branch_clock": start["c12"]["branch_clock"],
            },
            "live": world,
            "store_mutation": {
                "before": before,
                "after": after,
                "mutated_by_s35": before != after,
            },
            "cold": {
                "help": cold["help"],
                "tools_remaining": cold["tools_remaining"],
                "verify_ok": cold["verify_ok"],
                "world": cold_world,
            },
        }
    s39 = s39_source.audit()
    summary = {
        "base": BASE,
        "join_e_commit": JOIN_E_COMMIT,
        "programma_commit": PROGRAMMA_COMMIT,
        "s39_commit": s39["commit"],
        "actual_a_producer": "NONE_VERIFIED",
        "performed_e2_a_action_present": worlds["performed-e2"]["live"][
            "a_analysis"
        ]["a_action_performed_rows"]
        > 0,
        "performed_omit_a_omission_present": worlds["performed-omit"]["live"][
            "a_analysis"
        ]["a_omission_rows"]
        > 0,
        "a_action_bound_to_e1": any(
            worlds[key]["live"]["a_analysis"]["action_bound_to_e1"]
            for key in worlds
        ),
        "a_local_observation_of_e1": any(
            worlds[key]["live"]["a_analysis"]["a_local_observation_of_e1"]
            for key in worlds
        ),
        "action_clock_matches_e1": any(
            worlds[key]["live"]["a_analysis"]["action_clock_matches_e1"]
            for key in worlds
        ),
        "action_order_persisted": any(
            worlds[key]["live"]["a_analysis"]["action_order_persisted"]
            for key in worlds
        ),
        "actual_a_wiring_outcomes": {
            key: {
                "perception_only": worlds[key]["live"]["wired_actual_a_candidate"][
                    "perception_only"
                ]["outcome"],
                "action_only_with_controlled_perception": worlds[key]["live"][
                    "wired_actual_a_candidate"
                ]["action_only_with_controlled_perception"]["outcome"],
                "both_candidate": worlds[key]["live"]["wired_actual_a_candidate"][
                    "both_candidate"
                ]["outcome"],
            }
            for key in worlds
        },
        "controlled_integration_preserved": all(
            worlds[key]["live"]["controlled_integration"]["intact"]["outcome"]
            in {
                "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
                "OBSERVED_CURRENT_REFUSAL",
            }
            for key in worlds
        ),
        "cold_verify_all": all(
            worlds[key]["cold"]["verify_ok"] for key in worlds
        ),
        "store_unmutated_by_s35": all(
            not worlds[key]["store_mutation"]["mutated_by_s35"]
            for key in worlds
        ),
        "s39_actual_a": s39["actual_a_performer"],
        "s39_join_e_root_compatible": s39["join_e_root_compatible"],
        "s39_synthetic_premises": s39["sources_are_synthetic_premises"],
        "missing_source_owner_contract_present": all(
            worlds[key]["live"]["missing_source_owner_contract"]["schema"]
            == "S35_MISSING_SOURCE_OWNER_CONTRACT@1"
            for key in worlds
        ),
        "new_store_created": False,
    }
    evidence = {
        "schema": "SOROK_S35_ACTUAL_A_EVIDENCE@1",
        "grade": GRADE,
        "native": False,
        "base": BASE,
        "join_e_commit": JOIN_E_COMMIT,
        "programma_commit": PROGRAMMA_COMMIT,
        "source_runtime": source_runtime,
        "s39_audit": s39,
        "worlds": worlds,
        "summary": summary,
        "limits": [
            "existing R31J A action/omission is TEST_ONLY sourcefree fixture, not actual A",
            "no persisted A-local observation of E1",
            "no A action/omission receipt bound to E1 clock/root/branch/order",
            "no qualified A source-owner receipt",
            "S39 A performer is synthetic-premise and requires the S37 product interface",
            "no new store, native law or provider call",
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
