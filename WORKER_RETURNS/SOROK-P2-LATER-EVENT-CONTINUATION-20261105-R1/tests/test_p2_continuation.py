from __future__ import annotations

import json
from pathlib import Path

from p2_continuation import cli
from p2_continuation.continuation import SCHEMA, cold_read


def test_positive_later_event_chain_and_projected_refusal(positive_report):
    report = positive_report
    assert report["schema"] == SCHEMA
    assert report["ok"] is True, report["checks"]
    assert all(report["checks"].values()), report["checks"]
    assert report["interval"]["status"] == "PARTIAL"
    assert report["material_after_interval"] == 0
    assert report["later_event_2"]["status"] == "OK"
    assert report["later_event_2"]["performed"] is True
    assert report["later_event_2"]["c9"]["s47_source_in_readset"] is True
    assert report["later_event_2"]["c9"]["s47_source_hash"] == (
        report["interval_source_hash"]
    )
    assert report["later_event_2"]["s43"]["language_status"] == "ACCEPTED"
    assert report["later_event_2"]["s43"]["repertoire_hash"]
    assert report["later_event_3"]["status"] == "OK"
    assert report["later_event_2"]["event_ref"] in report["later_event_3"][
        "history_refs"
    ]
    assert report["earlier_event_after_later"]["event_hash"] == report[
        "later_event_2"
    ]["event_hash"]
    assert report["do_help"]["status"] == "REFUSED"
    assert report["do_help"]["attempted"] is True
    assert report["do_help"]["performed"] is False
    assert report["do_help"]["refusal"] is True
    assert report["attend"]["status"] == "NO_CHANGE"
    assert report["attend"]["world_event_created"] is False
    assert report["attend"]["clock_changed"] is False
    assert report["cold"]["verify_ok"] is True
    assert report["cold"]["root_hash"] == report["root_hash"]


def test_producer_and_first_consumers_are_named_callables(positive_report):
    callables = positive_report["callables"]
    assert callables["later_event_producer"].endswith("S43Session.admit_event")
    assert callables["later_event_reader"].endswith("S45Session.read_event")
    assert callables["later_event_reader_delegate"] == "s42.reader.read_event"
    assert callables["source_bound_expression_reader"].endswith(
        "S43Session.read_s43_event"
    )
    assert callables["event_local_c9_reader"].endswith(
        "S47Session.read_c9_conditioning"
    )
    assert callables["projected_say"].endswith("S45Projection.say")
    assert callables["projected_do_help"].endswith("S45Projection.do_help")
    assert callables["projected_attend"].endswith("S45Projection.attend")
    assert callables["s41_continuation_producer"] == (
        "s41.event.ContinuationProducer.generate"
    )


def test_scheduled_control_same_root_accepts_help(
    positive_report, scheduled_report
):
    report = scheduled_report
    assert report["ok"] is True, report["checks"]
    assert all(report["checks"].values()), report["checks"]
    assert report["root_hash"] == positive_report["root_hash"]
    assert report["material_after_interval"] == 1
    assert report["interval"]["status"] == "NOT_PERFORMED"
    assert report["do_help"]["status"] == "OK"
    assert report["do_help"]["refusal"] is False
    assert report["do_help"]["attempted"] is True
    assert report["do_help"]["performed"] is False
    assert report["do_help"]["actor_response"]["strategy"] == "HELP_ACCEPT"
    assert report["do_help"]["actor_response"]["performed"] is True


def test_interval_condition_cut_refuses_then_restores(cut_report):
    report = cut_report
    assert report["ok"] is True, report["checks"]
    assert all(report["checks"].values()), report["checks"]
    assert report["cut_code"] == "S46_INTERVAL_CONDITION_REVOKED"
    assert report["events_after_cut"] == report["events_before_cut"]
    assert report["restored_source"]["source_hash"] == report["before_source"][
        "source_hash"
    ]
    assert report["admitted"]["status"] == "OK"
    assert report["admitted"]["c9"]["s47_source_in_readset"] is True
    assert report["cold"]["verify_ok"] is True
    assert report["cold"]["root_hash"] == report["root_hash"]


def test_cli_reads_existing_positive_chain(positive_report, capsys):
    state = positive_report["state_root"]
    e2 = positive_report["later_event_2"]["event_ref"]
    e3 = positive_report["later_event_3"]["event_ref"]

    code = cli.main(["verify", "--state", state])
    captured = capsys.readouterr()
    assert code == 0, captured.err
    verify = json.loads(captured.out)
    assert verify["ok"] is True
    assert len(verify["s42_events"]) >= 3

    code = cli.main([
        "cold", "--state", state,
        "--event-ref", e2, "--event-ref", e3,
    ])
    captured = capsys.readouterr()
    assert code == 0, captured.err
    cold = json.loads(captured.out)
    assert cold["verify_ok"] is True
    assert cold["root_hash"] == positive_report["root_hash"]
    assert cold["events"][e2]["c9"]["s47_source_hash"] == (
        positive_report["later_event_2"]["c9"]["s47_source_hash"]
    )
