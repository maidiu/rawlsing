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

from bridge import join_e_compat, occurrence_consumer
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
            "OCCURRENCE_ENCOUNTER_FAILED:"
            + disposition
            + ":"
            + mode
            + ":"
            + completed.stderr[-2000:]
        )
    return json.loads(out.read_text(encoding="utf8"))


def _summary(result: dict) -> dict:
    return occurrence_consumer.summary(result)


def _evaluate_set(occurrence, *, action_kind: str, omitted: bool) -> dict:
    if omitted:
        intact = occurrence_consumer.evaluate_occurrence(
            occurrence, controlled=False
        )
        intact_controlled = occurrence_consumer.evaluate_occurrence(
            occurrence,
            controlled=True,
            perception_status="ACCESSIBLE",
            action_kind=action_kind,
            action_present=False,
        )
    else:
        intact = occurrence_consumer.evaluate_occurrence(
            occurrence,
            controlled=True,
            perception_status="ACCESSIBLE",
            action_kind=action_kind,
            action_present=True,
        )
        intact_controlled = intact
    perception_severed = occurrence_consumer.evaluate_occurrence(
        occurrence,
        controlled=True,
        perception_status="NOT_WITNESSED",
        action_kind=action_kind,
        action_present=not omitted,
    )
    action_severed = occurrence_consumer.evaluate_occurrence(
        occurrence,
        controlled=True,
        perception_status="ACCESSIBLE",
        action_kind=action_kind,
        action_present=False,
    )
    restored = occurrence_consumer.evaluate_occurrence(
        occurrence, controlled=False
    ) if omitted else occurrence_consumer.evaluate_occurrence(
        occurrence,
        controlled=True,
        perception_status="ACCESSIBLE",
        action_kind=action_kind,
        action_present=True,
    )
    return {
        "intact": _summary(intact),
        "intact_controlled": _summary(intact_controlled),
        "perception_severed": _summary(perception_severed),
        "action_severed": _summary(action_severed),
        "restored": _summary(restored),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--evidence-out",
        default=str(RETURN / "evidence" / "occurrence_consumer.json"),
    )
    parser.add_argument("--base-dir", default="")
    args = parser.parse_args()
    source_runtime = ensure_source()
    join_e_root = Path(source_runtime["return_path"])
    base = (
        Path(args.base_dir).resolve()
        if args.base_dir
        else Path(tempfile.mkdtemp(prefix="sorok-s35-occurrence-"))
    )
    base.mkdir(parents=True, exist_ok=True)
    worlds = {}
    start_bundles = {}
    cold_bundles = {}
    for disposition in ("PERFORMED", "OMITTED", "REFUSED"):
        state = base / disposition.lower()
        start = _run_encounter(
            join_e_root=join_e_root,
            state=state,
            disposition=disposition,
            mode="start",
            do_help=True,
            out=base / (disposition.lower() + "-occurrence-start.json"),
        )
        start_bundles[disposition] = start
        read_start = occurrence_consumer.read_occurrence(start)
        if not read_start.ok:
            raise RuntimeError(
                "OCCURRENCE_READ_REFUSED:"
                + disposition
                + ":"
                + json.dumps(read_start.missing_contract, sort_keys=True)
            )
        occurrence = read_start.occurrence
        before = join_e_compat.store_hashes(start)
        action_kind = (
            "REQUEST_TOOL" if disposition == "PERFORMED" else "EXPLICIT_REFUSAL"
        )
        omitted = disposition == "OMITTED"
        evaluated = _evaluate_set(
            occurrence, action_kind=action_kind, omitted=omitted
        )
        equalized = occurrence_consumer.make_clock_binding(
            occurrence["event_clock"],
            occurrence["event_clock"],
            substitution=True,
            equality_claimed=True,
        )
        clock_fault = occurrence_consumer.read_occurrence(
            start, clock_binding_override=equalized
        )
        after = join_e_compat.store_hashes(start)
        cold = _run_encounter(
            join_e_root=join_e_root,
            state=state,
            disposition=disposition,
            mode="open",
            do_help=True,
            out=base / (disposition.lower() + "-occurrence-cold.json"),
        )
        cold_bundles[disposition] = cold
        read_cold = occurrence_consumer.read_occurrence(cold)
        if not read_cold.ok:
            raise RuntimeError(
                "OCCURRENCE_COLD_READ_REFUSED:"
                + disposition
                + ":"
                + json.dumps(read_cold.missing_contract, sort_keys=True)
            )
        cold_evaluated = _evaluate_set(
            read_cold.occurrence, action_kind=action_kind, omitted=omitted
        )
        missing_contract = occurrence_consumer.missing_source_owner_contract(
            event_hash=occurrence["event_hash"],
            event_id=str(occurrence["event_id"]),
            event_clock=occurrence["event_clock"],
            branch_clock=occurrence["branch_clock"],
            root_id="root",
            branch_id=occurrence["branch_id"],
            missing_fields=(
                "qualified_a_perception_receipt",
                "qualified_a_action_receipt",
                "clock_domain_binding",
            ),
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
                "event_id": start["event_id"],
                "event_time": start["event_time"],
                "c12_branch_clock": start["c12"]["branch_clock"],
                "help": start["help"],
                "tools_remaining": start["tools_remaining"],
                "verify_ok": start["verify_ok"],
                "j_b_disposition": start["j_b_disposition"],
                "target_id": start["target_id"],
            },
            "occurrence": {
                "schema": occurrence["schema"],
                "event_hash": occurrence["event_hash"],
                "event_id": occurrence["event_id"],
                "event_clock": occurrence["event_clock"],
                "branch_clock": occurrence["branch_clock"],
                "clock_binding": occurrence["clock_binding"],
                "clock_binding_hash": occurrence["clock_binding_hash"],
                "root_branch_hash": occurrence["root_branch_hash"],
                "branch_hash": occurrence["branch_hash"],
                "branch_fork_clock": occurrence["branch_fork_clock"],
                "source_material_access": occurrence["source_material_access"],
                "duplicate_admission": False,
                "new_store_created": False,
                "c9_read_only": True,
                "checks": dict(read_start.checks),
            },
            "s35": evaluated,
            "clock_substitution_fault": {
                "ok": clock_fault.ok,
                "missing_contract": clock_fault.missing_contract,
                "refused": not clock_fault.ok,
            },
            "store_mutation": {
                "before": before,
                "after": after,
                "s35_mutated_store": before != after,
            },
            "cold": {
                "session_verify_ok": cold["verify_ok"],
                "help": cold["help"],
                "tools_remaining": cold["tools_remaining"],
                "branch_clock": cold["c12"]["branch_clock"],
                "occurrence_ok": read_cold.ok,
                "clock_binding_hash": read_cold.occurrence[
                    "clock_binding_hash"
                ],
                "s35": cold_evaluated,
            },
            "missing_source_owner_contract": missing_contract,
        }
    def _mix(base_bundle: dict, other_bundle: dict, fields: tuple[str, ...]) -> dict:
        mixed = dict(base_bundle)
        for field in fields:
            mixed[field] = other_bundle.get(field)
        return mixed

    def _substitution(name: str, bundle: dict) -> dict:
        read = occurrence_consumer.read_occurrence(bundle)
        return {
            "name": name,
            "ok": read.ok,
            "refused": not read.ok,
            "missing_fields": list(
                (read.missing_contract or {}).get("missing_fields", [])
            ),
        }

    performed_live = start_bundles["PERFORMED"]
    refused_live = start_bundles["REFUSED"]
    performed_cold = cold_bundles["PERFORMED"]
    refused_cold = cold_bundles["REFUSED"]
    mutation_bundle = dict(performed_live)
    mutated_actor = dict(performed_live["actor_snapshot"])
    mutated_state = dict(mutated_actor.get("state") or {})
    mutated_state["actor_id"] = "TEST_ONLY_FOREIGN_ACTOR"
    mutated_actor["state"] = mutated_state
    mutated_actor["source_ref"] = "TEST_ONLY_FOREIGN_ACTOR_SOURCE"
    mutation_bundle["actor_snapshot"] = mutated_actor
    substitution_tests = {
        "live": [
            _substitution(
                "performed_c9_refused_source",
                _mix(performed_live, refused_live, ("source",)),
            ),
            _substitution(
                "performed_c9_refused_c12",
                _mix(performed_live, refused_live, ("c12_path",)),
            ),
            _substitution(
                "performed_c9_refused_source_and_c12",
                _mix(
                    performed_live,
                    refused_live,
                    (
                        "source",
                        "c12_path",
                        "branch_id",
                        "source_actor_map",
                        "actor_snapshot",
                    ),
                ),
            ),
            _substitution(
                "performed_c9_refused_c9_path",
                _mix(performed_live, refused_live, ("c9_path", "e1_event_hash")),
            ),
            _substitution(
                "refused_c9_performed_source",
                _mix(refused_live, performed_live, ("source",)),
            ),
            _substitution(
                "mutated_actor_snapshot",
                mutation_bundle,
            ),
        ],
        "cold": [
            _substitution(
                "cold_performed_c9_refused_source_and_c12",
                _mix(
                    performed_cold,
                    refused_cold,
                    (
                        "source",
                        "c12_path",
                        "branch_id",
                        "source_actor_map",
                        "actor_snapshot",
                    ),
                ),
            ),
            _substitution(
                "cold_source_only_substitution",
                _mix(performed_cold, refused_cold, ("source",)),
            ),
        ],
    }
    summary = {
        "join_e_commit": JOIN_E_COMMIT,
        "source_runtime": source_runtime,
        "first_consumer": (
            "bridge/occurrence_consumer.py:read_occurrence->"
            "evaluate_occurrence"
        ),
        "worlds": len(worlds),
        "reader_ok_all": all(
            worlds[key]["occurrence"]["checks"]
            and all(worlds[key]["occurrence"]["checks"].values())
            for key in worlds
        ),
        "intact_outcomes": {
            key: worlds[key]["s35"]["intact"]["outcome"] for key in worlds
        },
        "intact_controlled_outcomes": {
            key: worlds[key]["s35"]["intact_controlled"]["outcome"]
            for key in worlds
        },
        "perception_severed_outcomes": {
            key: worlds[key]["s35"]["perception_severed"]["outcome"]
            for key in worlds
        },
        "action_severed_outcomes": {
            key: worlds[key]["s35"]["action_severed"]["outcome"]
            for key in worlds
        },
        "restored_outcomes": {
            key: worlds[key]["s35"]["restored"]["outcome"] for key in worlds
        },
        "clock_substitution_refused_all": all(
            worlds[key]["clock_substitution_fault"]["refused"] for key in worlds
        ),
        "cold_outcomes_match": all(
            worlds[key]["cold"]["s35"]["intact"]["outcome"]
            == worlds[key]["s35"]["intact"]["outcome"]
            for key in worlds
        ),
        "cold_verify_all": all(
            worlds[key]["cold"]["session_verify_ok"] for key in worlds
        ),
        "performed_help_accept": worlds["PERFORMED"]["join_e"]["help"][
            "accepted"
        ],
        "omitted_help_accept": worlds["OMITTED"]["join_e"]["help"][
            "accepted"
        ],
        "refused_help_accept": worlds["REFUSED"]["join_e"]["help"][
            "accepted"
        ],
        "omitted_material_access": worlds["OMITTED"]["occurrence"][
            "source_material_access"
        ],
        "store_unmutated_by_s35": all(
            not worlds[key]["store_mutation"]["s35_mutated_store"]
            for key in worlds
        ),
        "duplicate_admission": False,
        "new_store_created": False,
        "actual_a_producer": "NONE_VERIFIED",
        "missing_source_owner_contract_present": all(
            worlds[key]["missing_source_owner_contract"]["schema"]
            == "S35_MISSING_SOURCE_OWNER_CONTRACT@1"
            for key in worlds
        ),
        "targetless_all": all(
            worlds[key]["s35"]["intact"]["target_branch"] == "NO_CHANGE"
            and worlds[key]["s35"]["intact"]["target_reason"] == "NO_PROPOSAL"
            and worlds[key]["s35"]["intact"]["target_proposals"] == 0
            for key in worlds
        ),
        "substitution_refused_all": all(
            row["refused"] for row in substitution_tests["live"]
        ),
        "cold_substitution_refused_all": all(
            row["refused"] for row in substitution_tests["cold"]
        ),
        "controlled_evidence": "TEST_ONLY",
    }
    evidence = {
        "schema": "SOROK_SAME_ROOT_ADMITTED_OCCURRENCE_CONSUMER@1",
        "grade": GRADE,
        "native": False,
        "base": "c5602ec87ba6e951540b89a49404db76c128eb50",
        "join_e_commit": JOIN_E_COMMIT,
        "programma_disposition": "29aa0f9e81fe1f371f2773d4750e1838bdd63daf",
        "source_runtime": source_runtime,
        "worlds": worlds,
        "substitution_tests": substitution_tests,
        "summary": summary,
        "limits": [
            "no duplicate admission",
            "no second store",
            "no clock substitution",
            "no fabricated actual A producer",
            "controlled A inputs are TEST_ONLY",
            "no new native law, provider call or external checkout read",
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
