"""Bounded actual-root probes for the S48-S52 current-B seam."""
from __future__ import annotations

import importlib
from pathlib import Path

SEED = "01" * 32


def _start(pkg: str, state: Path):
    from s37.harness import case_for, source_for
    from s45.fixtures import root_bundle

    module = importlib.import_module(pkg + ".session")
    cls = getattr(module, pkg.upper() + "Session")
    case = case_for(True)
    return cls.start(
        state, bundle=root_bundle(SEED), case=case, source=source_for(case),
        language_context={"milieu_id": "workshop"},
    )


def _identity(session) -> dict:
    world = session.world()
    return {
        "root_hash": session.read_root()["root_hash"],
        "root_id": session.read_root()["root_id"],
        "branch_id": session.branch_id,
        "b_actor": dict(world.actor_state.get("B") or {}),
        "b_position": (world.positions or {}).get("B"),
        "world_events": len(world.events),
        "clock": session.clock(),
        "read_events": len(session.read_events()),
    }


def probe_s49(stage: Path, work: Path) -> dict:
    from s49.bootstrap import install
    install()
    from s48.errors import S48Refusal
    from s48.sources import candidate_specs, eligible_candidate_ids, issue_current_source
    from s49.actor import MISSING_B_CONTEXT, _b_access, record_b_observation, root_b_sources
    from s49.session import S49Session

    state = work / "actual"
    session = _start("s49", state)
    try:
        before = _identity(session)
        record_b_observation(session)
        event = session.read_events()[-1]
        access = _b_access(session, event)
        sources = root_b_sources(session)
        candidates = candidate_specs(session)
        eligible = eligible_candidate_ids(session)
        try:
            issue_current_source(session, "ANY")
            issue_hold = {"raised": False}
        except S48Refusal as exc:
            issue_hold = {"raised": True, "code": exc.code, "detail": str(exc)}
        before_turn = _identity(session)
        turn = session.produce_b_turn(controlled=False)
        after_turn = _identity(session)
        verify_ok = session.verify().get("ok")
        normal = [
            dict(row.get("body") or {})
            for row in session.product.store.episodes(session.branch_id)
            if (row.get("body") or {}).get("stage") == "NORMAL_CONSUMER"
        ]
    finally:
        session.close()
    return {
        "schema": "SOROK_CURRENT_B_S49_PROBE@1",
        "before": before,
        "access": access,
        "root_b_sources": sources,
        "s48_candidate_specs": candidates,
        "s48_eligible_candidate_ids": eligible,
        "s48_issue_current_source": issue_hold,
        "b_turn": {key: turn.get(key) for key in
                   ("stage", "status", "reason", "event_ref", "missing_context")},
        "missing_context": MISSING_B_CONTEXT,
        "identity_before_turn": before_turn,
        "identity_after_turn": after_turn,
        "world_or_clock_changed": (
            before_turn["world_events"] != after_turn["world_events"]
            or before_turn["clock"] != after_turn["clock"]
        ),
        "normal_s42_consumer_rows": len(normal),
        "normal_s42_reached": bool(turn.get("event_ref")),
        "c8_created": bool(normal),
        "verify_ok": verify_ok,
        "actual_source_grade": "UNAVAILABLE_CURRENT_B_ACTOR_OWNED_CONTEXT",
    }


def probe_s50(stage: Path, work: Path) -> dict:
    from s50.bootstrap import install
    install()
    from s50.recovery import verify_source
    from s50.session import S50Session

    state = work / "actual"
    session = _start("s50", state)
    try:
        identity = _identity(session)
        missing = session.actual_root_missing()
        verify_ok = session.verify().get("ok")
    finally:
        session.close()
    source = verify_source()
    return {
        "schema": "SOROK_CURRENT_B_S50_PROBE@1",
        "identity": identity,
        "actual_root_missing": missing,
        "source_identity": {
            "count": source.get("count"),
            "all_exact": source.get("all_exact"),
            "archive_identity": source.get("archive_identity"),
            "fixture_sha256": source.get("fixture_sha256"),
        },
        "verify_ok": verify_ok,
    }


def probe_s51(stage: Path, work: Path) -> dict:
    from s51.bootstrap import install
    install()
    from s51.session import S51Session

    state = work / "actual"
    session = _start("s51", state)
    try:
        root_hash = session.read_root()["root_hash"]
        experiment = session.run_experiment()
        verify_ok = session.verify().get("ok")
    finally:
        session.close()
    cold = S51Session.open(state)
    try:
        cold_verify = cold.verify().get("ok")
        cold_eps = [
            row for row in cold.product.store.episodes(cold.branch_id)
            if row.get("kind") == "S51_OBJECT_RELEVANCE"
        ]
        target = experiment["relevance"]["episode_id"]
        cold_hash = next(
            (row["body"]["result"]["relevance_hash"] for row in cold_eps
             if row.get("episode_id") == target), "",
        )
    finally:
        cold.close()
    rel = experiment["relevance"]
    gen = experiment["generation"] or {}
    obj = experiment["object"]
    return {
        "schema": "SOROK_CURRENT_B_S51_PROBE@1",
        "identity": {
            "root_hash": root_hash,
            "b_actor": rel.get("actor_id"),
        },
        "object": {key: obj.get(key) for key in
                   ("object_event_id", "object_hash", "actor_id", "striving",
                    "effective_index", "work_parent_event_id",
                    "project_parent_event_id", "source_grade")},
        "relevance": {key: rel.get(key) for key in
                      ("status", "relation", "actor_free_hours",
                       "actual_current_purpose_proved", "relevance_hash")},
        "generation": {key: gen.get(key) for key in
                       ("selection_status", "selected_option",
                        "missing_option_relation", "s49_status",
                        "source_ref", "target_proposals")},
        "actual_root_current_purpose_proved": experiment.get(
            "actual_root_current_purpose_proved"),
        "verify_ok": verify_ok,
        "cold": {"same_relevance_hash": cold_hash == rel.get("relevance_hash"),
                 "verify_ok": cold_verify},
        "native": False,
    }


def probe_s52(stage: Path, work: Path) -> dict:
    from s52.bootstrap import install
    install()
    from s52.session import S52Session

    state = work / "actual"
    session = _start("s52", state)
    try:
        experiment = session.run_experiment()
        candidate = experiment["candidate"]
        generation = experiment["generation"]
        receipt = generation.get("generation_receipt") or {}
        before = _identity(session)
        normal = session.perform_paid_participation(
            candidate, generation=generation, counterpart_performed=False
        )
        after = _identity(session)
        verify_ok = session.verify().get("ok")
    finally:
        session.close()
    cold = S52Session.open(state)
    try:
        cold_verify = cold.verify().get("ok")
        cold_candidates = [
            row for row in cold.product.store.episodes(cold.branch_id)
            if row.get("kind") == "S52_PAID_CANDIDATE"
        ]
        cold_match = bool(
            cold_candidates
            and cold_candidates[-1]["body"].get("candidate_hash")
            == candidate["candidate_hash"]
        )
    finally:
        cold.close()
    return {
        "schema": "SOROK_CURRENT_B_S52_PROBE@1",
        "candidate": {key: candidate.get(key) for key in
                      ("candidate_hash", "status", "reason", "recruited",
                       "objective_feasibility", "counterpart_status",
                       "prospective_payment", "earned_payment",
                       "actual_current_purpose_proved")},
        "generation": {
            "selection_status": receipt.get("selection_status"),
            "selected_option": receipt.get("selected_option"),
            "eligible_options": receipt.get("eligible_options"),
            "options": [row.get("option_id") for row in receipt.get("options", [])],
            "paid_reasons": [
                row for row in receipt.get("reasons", [])
                if row.get("option_id") == "PAID_PARTICIPATION"
            ],
        },
        "normal_paid_perform_without_counterpart": {
            key: normal.get(key) for key in
            ("status", "performed", "reason", "world_event_id", "payment_earned")
        },
        "identity_before_normal": before,
        "identity_after_normal": after,
        "normal_no_world_or_state_change": (
            before["world_events"] == after["world_events"]
            and before["b_actor"] == after["b_actor"]
            and before["clock"] == after["clock"]
        ),
        "controlled_counterpart_not_executed": True,
        "verify_ok": verify_ok,
        "cold": {"candidate_match": cold_match, "verify_ok": cold_verify},
        "native": False,
    }


PROBES = {
    "s49": probe_s49,
    "s50": probe_s50,
    "s51": probe_s51,
    "s52": probe_s52,
}


__all__ = ["PROBES"]
