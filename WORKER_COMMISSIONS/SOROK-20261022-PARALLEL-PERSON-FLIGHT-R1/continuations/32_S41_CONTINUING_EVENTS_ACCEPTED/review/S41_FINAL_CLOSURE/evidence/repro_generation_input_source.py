import json
import os
import sys
import tempfile
from pathlib import Path

RETURN = Path(os.environ["S41_RETURN"]).resolve()
sys.path.insert(0, str(RETURN))

from s41.bootstrap import install

install()

from c8_readonly_consumer import C8ReadOnlyConsumer
from s39.sources import context_records, make_source
from s41.bindings import (
    append_event_binding,
    binding_episodes,
    make_continuation_binding,
)
from s41.event import (
    ContinuationProducer,
    build_second_occurrence,
    history_record_from_prior,
    world_prerequisites,
)
from s41.performer import perform_continuation_attempt
from s41.session import S41Session
from s37.harness import case_for, source_for


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="s41-generation-input-source-"))
    session = S41Session.start(
        root / "state", case=case_for(True), source=source_for(case_for(True))
    )
    producer = None
    try:
        first_binding = binding_episodes(session)[0]
        c8_event = C8ReadOnlyConsumer(
            first_binding["c8"]["journal_path"]
        ).load().get(first_binding["c8"]["occurrence_id"])
        second_case = case_for(False)
        second_source = source_for(second_case)
        occurrence, _ = build_second_occurrence(
            session,
            first_binding=first_binding,
            first_payload=c8_event["payload"],
            second_source=second_source,
            event_time=session.clock() + 1,
        )
        producer = ContinuationProducer(
            session.state_root / "source",
            case=second_case,
            source=second_source,
            occurrence=occurrence,
            current_tools=session.world().actor_state["A"]["tools_remaining"],
        )
        producer.commit_incoming()
        as_of = occurrence.event_time + 5
        history = history_record_from_prior(
            session, first_binding=first_binding, as_of=as_of
        )
        contexts = context_records(
            actor_id=session.meta["source_actor_map"]["TEST_ONLY_R31J_A"],
            branch_id=session.branch_id,
            as_of=as_of,
            repair_urgent=True,
            avoid_debt=True,
        )
        receipt = producer.generate(
            source_records=contexts + [history],
            branch_id=session.branch_id,
            world=world_prerequisites(session),
        )
        world = session.world()
        world.advance(occurrence.event_time)
        session.product._checkpoint(session.branch_id, world.clock, world)
        attempt = perform_continuation_attempt(
            session,
            receipt["attempt_request"],
            generation_receipt=receipt,
            e1_identity={
                "event_id": producer.e1_event["event_id"],
                "event_hash": producer.e1_event["hash"],
                "c8_occurrence_id": producer.out9.occurrence_id,
                "c8_state_digest": producer.out9.readset["state_digest"],
            },
        )
        producer.finalize_s36(attempt_result=attempt)
        replacement = make_source(
            source_ref=history["source_ref"],
            source_class=history["source_class"],
            actor_id=history["actor_id"],
            branch_id=history["branch_id"],
            as_of=history["as_of"],
            predicate=history["predicate"],
            value=history["value"],
            content={
                "mapping_premise": "REPLACED_ACTUAL_INPUT",
                "prior_b_event_hash": "0" * 64,
            },
        )
        binding = make_continuation_binding(
            session,
            producer=producer,
            generation=receipt,
            attempt=attempt,
            s36=producer.s36_binding,
            source=second_source,
            first_binding=first_binding,
            history_source=history,
            world_before=session.world().snapshot(),
            world_after=session.world().snapshot(),
            status=attempt["attempt_status"],
            generation_sources=contexts + [replacement],
        )
        append_event_binding(session, binding)
        first = session.read_event(first_binding["e1_event_id"])
        second = session.read_event(binding["e1_event_id"])
        report = {
            "schema": "SOROK_S41_GENERATION_INPUT_SOURCE_REPRO@1",
            "canonical_history_source": history["source_ref"],
            "history_source_hash": history["source_hash"],
            "replacement_source_hash": replacement["source_hash"],
            "generation_source_refs": second.get("generation_source_refs"),
            "warm_first_status": first["status"],
            "warm_second_status": second["status"],
            "warm_performed": second.get("performed"),
            "warm_verify_ok": session.verify()["ok"],
        }
    finally:
        if producer is not None:
            producer.close()
        session.close()

    cold = S41Session.open(root / "state")
    try:
        cold_first, cold_second = cold.read_events()
        report.update(
            {
                "cold_first_status": cold_first["status"],
                "cold_second_status": cold_second["status"],
                "cold_verify_ok": cold.verify()["ok"],
            }
        )
    finally:
        cold.close()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
