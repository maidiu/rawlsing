"""Independent MI H1 chronology/source probe for frozen head 634b75d6."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rawlsing_next.tests.test_sorok_history_episodes import (
    candidate, commit, exact, source_world,
)


def test_h1_source_ref_cannot_postdate_effective_time(tmp_path, monkeypatch):
    fanin, history, book, tool, entities, source_ref = source_world(tmp_path, monkeypatch)
    try:
        leased = history.lease()
        proposal = candidate(leased, book, tool, entities, source_ref)
        occurrence = proposal["occurrences"][0]
        packet = leased["packet"]
        effective = occurrence["effective_time"]
        future = next(
            ref for ref in packet["event_refs"]
            if fanin.session.event(ref["object_id"])["clock"] > effective
        )
        occurrence["source_refs"] = [future]
        occurrence["ref"] = exact("OCCURRENCE", "candidate:postdating-source", occurrence)
        proposal["dependencies"][1]["parent_refs"] = [occurrence["ref"]]
        result = commit(history, leased, proposal)
        assert result["status"] != "INDEX_READY"
        assert not any(event["kind"] == "HISTORICAL_MATERIAL"
                       for event in fanin.session.events())
    finally:
        fanin.close()
