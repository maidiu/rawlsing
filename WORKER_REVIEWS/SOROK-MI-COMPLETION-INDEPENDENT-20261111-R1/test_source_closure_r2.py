"""Independent source-time/cache probes for MI closure head 0b0eb94c7."""

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rawlsing_next.sorok_history.owner import HistoryRefusal
from rawlsing_next.tests.test_sorok_history_episodes import (
    candidate, commit, source_world,
)


def test_graph_lookup_does_not_reuse_revoked_source_across_reads(tmp_path, monkeypatch):
    fanin, history, book, tool, entities, source_ref = source_world(tmp_path, monkeypatch)
    try:
        leased = history.lease()
        admitted = commit(history, leased,
                          candidate(leased, book, tool, entities, source_ref))
        assert admitted["status"] == "INDEX_READY"
        before = history.query_relations(book["id"])
        assert before["status"] == "QUALIFIED"
        withheld = history.test_withhold_event_source(source_ref["object_id"])
        with pytest.raises(HistoryRefusal, match="HISTORICAL_(EPISODE_)?PARENT_MISSING"):
            history.query_relations(book["id"])
        history.test_restore_event_source(withheld)
        assert history.query_relations(book["id"]) == before
    finally:
        fanin.close()
