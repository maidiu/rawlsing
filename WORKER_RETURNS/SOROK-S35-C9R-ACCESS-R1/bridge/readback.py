"""Cold readback of the committed C9 rows and the C12 root/branch binding."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Mapping

from install import install

install()

from bp4.store import C12Store
from candidate import digest, valid

from .access import public_privacy_error


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf8"))


def _body_rows(
    connection: sqlite3.Connection, table: str, key_column: str
) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for key, body in connection.execute(
        f'SELECT "{key_column}", body FROM "{table}" ORDER BY "{key_column}"'
    ):
        result[str(key)] = json.loads(body)
    return result


def read_c9(path: str | Path) -> dict:
    path = Path(path)
    connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        occurrence = _body_rows(connection, "occurrence", "hash")
        response = _body_rows(connection, "response", "hash")
        receipt = _body_rows(connection, "receipt", "hash")
        target_state = _body_rows(connection, "target_state", "id")
        target_journal = _body_rows(connection, "target_journal", "id")
        event_identity_rows = [
            (str(row[0]), str(row[1]))
            for row in connection.execute(
                "SELECT event_id, hash FROM event_identity ORDER BY event_id"
            )
        ]
        clocks = [
            int(row[0])
            for row in connection.execute("SELECT clock FROM clock ORDER BY clock")
        ]
    finally:
        connection.close()
    return {
        "occurrence": occurrence,
        "event_identity": event_identity_rows,
        "response": response,
        "receipt": receipt,
        "target_state": target_state,
        "target_journal": target_journal,
        "clocks": clocks,
    }


def _sealed(rows: Mapping[str, Mapping[str, Any]], key: str) -> bool:
    body = rows.get(key)
    return isinstance(body, Mapping) and digest(dict(body)) == key


def _valid_episode(episode: Mapping[str, Any]) -> bool:
    body = {
        key: value
        for key, value in episode.items()
        if key not in {"hash", "episode_id"}
    }
    return episode.get("hash") == digest(body)


def cold_verify(world_root: str | Path, label: str) -> dict:
    world_root = Path(world_root)
    run_dir = world_root / "runs" / str(label)
    world = _load(world_root / "world.json")
    run = _load(run_dir / "run.json")
    checks: dict[str, bool] = {}
    observed: dict[str, Any] = {
        "label": str(label),
        "world_schema": world.get("schema"),
        "run_schema": run.get("schema"),
        "refused": bool(run.get("refused")),
    }
    if run.get("refused"):
        checks["refusal_has_no_c9"] = not (run_dir / "c9.sqlite").exists()
        checks["refusal_committed_false"] = run.get("committed") is False
        checks["refusal_zero_targets"] = run.get("target_state_rows") == 0
        checks["refusal_status_typed"] = run.get("response_status") in {
            "REFUSED",
            "HELD",
        }
        checks["refusal_public_privacy"] = not public_privacy_error(run)
        return {"ok": all(checks.values()), "checks": checks, "observed": observed}

    receipt_path = run_dir / "s35_receipt.json"
    s35_receipt = _load(receipt_path)
    checks["s35_receipt_sealed"] = valid(dict(s35_receipt))
    checks["s35_receipt_hash_matches_run"] = (
        s35_receipt.get("hash") == run.get("s35_receipt_hash")
    )
    c9 = read_c9(run_dir / "c9.sqlite")
    response_key = str(run.get("response_row_hash", ""))
    receipt_key = str(run.get("c9_receipt_hash", ""))
    response_body = c9["response"].get(response_key, {})
    receipt_body = c9["receipt"].get(receipt_key, {})
    checks["response_row_present"] = bool(response_body)
    checks["response_row_sealed"] = _sealed(c9["response"], response_key)
    checks["receipt_row_present"] = bool(receipt_body)
    checks["receipt_row_sealed"] = _sealed(c9["receipt"], receipt_key)
    checks["response_status_matches"] = (
        response_body.get("status") == run.get("response_status")
    )
    checks["response_route_matches"] = (
        response_body.get("candidate_route") == s35_receipt.get("candidate_route")
    )
    checks["response_receipt_binding"] = (
        response_body.get("receipt_hash") == s35_receipt.get("hash")
    )
    checks["response_event_binding"] = (
        response_body.get("event_ref") == world["context"]["event_ref"]
    )
    checks["c9_receipt_event_binding"] = (
        receipt_body.get("event_ref") == world["context"]["event_ref"]
    )
    checks["c9_receipt_response_binding"] = (
        receipt_body.get("response_ref") == response_key
    )
    checks["target_branch_no_change"] = receipt_body.get("target_branch") == "NO_CHANGE"
    checks["target_reason_no_proposal"] = (
        receipt_body.get("target_reason") == "NO_PROPOSAL"
    )
    checks["target_id_absent"] = receipt_body.get("target_id") == ""
    checks["target_state_empty"] = len(c9["target_state"]) == 0
    checks["target_journal_empty"] = len(c9["target_journal"]) == 0
    checks["occurrence_present"] = len(c9["occurrence"]) == 1
    checks["event_identity_present"] = len(c9["event_identity"]) == 1
    checks["clock_present"] = world["context"]["event_time"] in c9["clocks"]
    checks["receipt_target_proposals_zero"] = s35_receipt.get("target_proposals") == []
    checks["receipt_objective_separate"] = (
        s35_receipt.get("objective_material_implies_uptake") is False
    )
    checks["receipt_claim_ceiling"] = (
        s35_receipt.get("claim_ceiling")
        == "OBSERVED_PRESENT_ACTION_ONLY_NOT_PSYCHOLOGICAL_RULE_A"
    )
    checks["receipt_public_privacy"] = not public_privacy_error(s35_receipt)
    checks["run_public_privacy"] = not public_privacy_error(run)
    checks["response_row_public_privacy"] = not public_privacy_error(response_body)
    checks["c9_receipt_public_privacy"] = not public_privacy_error(receipt_body)
    grade = s35_receipt.get("evidence_grade")
    actual = s35_receipt.get("actual_actor_input")
    checks["evidence_grade_typed"] = grade in {
        "TEST_ONLY_CONTROLLED_FIXTURE",
        "QUALIFIED_ACTUAL_A_INPUT",
        "ACTUAL_A_INPUT_UNAVAILABLE",
    }
    checks["actual_input_graded"] = (
        (grade == "TEST_ONLY_CONTROLLED_FIXTURE" and actual is False)
        or (grade == "QUALIFIED_ACTUAL_A_INPUT" and actual is True)
        or (grade == "ACTUAL_A_INPUT_UNAVAILABLE" and actual is False)
    )
    outcome = str(s35_receipt.get("outcome", ""))
    hold_reason = str(s35_receipt.get("hold_reason", ""))
    checks["hold_reason_consistent"] = (
        (outcome in {"A_LOCAL_PERCEPTION_HOLD", "A_OWNED_ACTION_HOLD"})
        == bool(hold_reason)
    )
    if outcome not in {"A_LOCAL_PERCEPTION_HOLD", "A_OWNED_ACTION_HOLD"}:
        checks["perception_ref_present"] = bool(s35_receipt.get("perception_ref"))
    if outcome in {
        "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
        "OBSERVED_CURRENT_REFUSAL",
        "RECEIVABLE_NO_OBSERVED_UPTAKE",
    }:
        checks["action_ref_present"] = bool(s35_receipt.get("action_ref"))

    c12 = C12Store(world_root / "c12.sqlite")
    try:
        root_branch = c12.branch("root")
        branch = c12.branch("s35")
        root_state = c12.checkpoints("root")[-1]
        checks["c12_root_hash_matches"] = (
            digest(root_branch) == world["context"]["root_branch_hash"]
        )
        checks["c12_branch_hash_matches"] = (
            digest(branch) == world["context"]["branch_hash"]
        )
        checks["c12_root_state_matches"] = (
            root_state.get("hash") == world["context"]["root_state_hash"]
        )
        checks["c12_branch_parent_matches"] = (
            branch.get("parent_branch_id") == world["context"]["branch_parent_id"]
        )
        checks["c12_branch_fork_clock_matches"] = (
            branch.get("fork_clock") == world["context"]["branch_fork_clock"]
        )
        checks["c12_clock_matches"] = (
            c12.last_clock("s35") == world["context"]["clock"]
        )
        episodes = c12.episodes("s35")
        matching = [
            episode
            for episode in episodes
            if (episode.get("body") or {}).get("s35_receipt_hash")
            == s35_receipt.get("hash")
            and (episode.get("body") or {}).get("label") == str(label)
        ]
        observed_episode = matching[0] if matching else {}
        observed_body = observed_episode.get("body") or {}
        checks["c12_episode_present"] = len(matching) == 1
        checks["c12_episode_sealed"] = bool(matching) and _valid_episode(
            matching[0]
        )
        checks["c12_episode_receipt_matches"] = (
            bool(matching) and observed_body.get("s35_receipt") == s35_receipt
        )
        checks["c12_episode_targetless"] = (
            bool(matching)
            and observed_body.get("target_id") == ""
            and observed_body.get("target_branch") == "NO_CHANGE"
            and observed_body.get("target_reason") == "NO_PROPOSAL"
        )
        checks["c12_episode_public_privacy"] = not public_privacy_error(
            observed_body
        )
        observed.update(
            {
                "outcome": s35_receipt.get("outcome"),
                "response_status": response_body.get("status"),
                "response_row_hash": response_key,
                "c9_receipt_hash": receipt_key,
                "s35_receipt_hash": s35_receipt.get("hash"),
                "evidence_grade": s35_receipt.get("evidence_grade"),
                "actual_actor_input": s35_receipt.get("actual_actor_input"),
                "qualification": s35_receipt.get("qualification"),
                "hold_reason": s35_receipt.get("hold_reason"),
                "target_branch": receipt_body.get("target_branch"),
                "target_reason": receipt_body.get("target_reason"),
                "target_state_rows": len(c9["target_state"]),
                "c12_episode_hash": observed_episode.get("hash", ""),
            }
        )
    finally:
        c12.close()
    return {"ok": all(checks.values()), "checks": checks, "observed": observed}


__all__ = ["cold_verify", "read_c9"]
