from __future__ import annotations

import json
from pathlib import Path

from p2_continuation import cli
from p2_continuation.continuation import (
    SCHEMA,
    cold_read,
    privacy_hits,
    public_cut_restore_report,
    public_report,
)


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
    assert report["encounter_count_before_action"] == 0
    assert report["encounter_count_after_action"] == 3
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
    assert report["encounter_count_before_action"] == 0
    assert report["encounter_count_after_action"] == 3


def test_observation_does_not_manufacture_user_attempt(
    positive_observation, scheduled_observation
):
    for report in (positive_observation, scheduled_observation):
        assert report["ok"] is True, report["checks"]
        assert report["say"] is None
        assert report["do_help"] is None
        assert report["attend"] is None
        assert report["say_executed"] is False
        assert report["do_help_executed"] is False
        assert report["attend_executed"] is False
        assert report["encounter_count_before_action"] == 0
        assert report["encounter_count_after_action"] == 0
        public = public_report(report)
        assert privacy_hits(public) == []
        assert public["checks"]["privacy_clean"] is True
        assert public["do_help"] is None
        assert public["do_help_executed"] is False
        assert public["encounter_count_before_action"] == 0
        assert public["encounter_count_after_action"] == 0


def test_public_action_reports_privacy_and_explicit_counts(
    positive_report, scheduled_report
):
    for report in (positive_report, scheduled_report):
        public = public_report(report)
        assert privacy_hits(public) == []
        assert public["checks"]["privacy_clean"] is True
        assert public["do_help_executed"] is True
        assert public["do_help"] is not None
        assert public["encounter_count_before_action"] == 0
        assert public["encounter_count_after_action"] == 3
        assert public["checks"]["do_help_explicit"] is True


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
    public = public_cut_restore_report(report)
    assert privacy_hits(public) == []
    assert public["checks"]["privacy_clean"] is True
    assert public["checks"]["source_intact"] is True
    assert public["checks"]["cold_continuity"] is True


def test_source_intact_cold_engineering_read(cut_report):
    report = cut_report
    admitted = report["admitted"]
    cold = cold_read(report["state_root"], (admitted["event_ref"],))
    cold_event = cold["events"][admitted["event_ref"]]
    assert cold["verify_ok"] is True
    assert cold_event["c9"]["s47_source_hash"] == report["before_source"][
        "source_hash"
    ]
    assert cold_event["c9"]["s47_source_in_readset"] is True


def test_cli_public_default_and_explicit_action(tmp_path, capsys):
    state = tmp_path / "cli-default" / "state"
    code = cli.main(["positive", "--state", str(state)])
    captured = capsys.readouterr()
    assert code == 0, captured.err
    public = json.loads(captured.out)
    assert privacy_hits(public) == []
    assert public["do_help"] is None
    assert public["do_help_executed"] is False
    assert public["encounter_count_before_action"] == 0
    assert public["encounter_count_after_action"] == 0

    state_action = tmp_path / "cli-action" / "state"
    code = cli.main([
        "positive", "--state", str(state_action), "--do-help",
    ])
    captured = capsys.readouterr()
    assert code == 0, captured.err
    public_action = json.loads(captured.out)
    assert privacy_hits(public_action) == []
    assert public_action["do_help_executed"] is True
    assert public_action["do_help"]["status"] == "REFUSED"
    assert public_action["encounter_count_before_action"] == 0
    assert public_action["encounter_count_after_action"] == 1
