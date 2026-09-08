from __future__ import annotations

from datetime import datetime, timezone

import rawlsing_next.rabochii_return_beacon_sweep as sweep


class FakeClient:
    repo = "maidiu/rawlsing"

    def __init__(self, pages):
        self.pages = list(pages)
        self.calls = []

    def _request(self, method, path, *, body=None):
        self.calls.append((method, path, body))
        return self.pages.pop(0)


def _page(nodes, *, more=False, cursor=None):
    return {
        "data": {
            "repository": {
                "refs": {
                    "nodes": nodes,
                    "pageInfo": {
                        "hasNextPage": more,
                        "endCursor": cursor,
                    },
                }
            }
        }
    }


def test_branch_node_accepts_full_agent_name_from_heads_namespace():
    node = {
        "name": "agent/rabochii-example-r1",
        "target": {
            "committedDate": "2099-01-01T00:00:00Z",
            "messageHeadline": "Return example to SUB-VOZHD",
        },
    }
    cutoff = datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert sweep._branch_from_node(node, cutoff=cutoff) == "agent/rabochii-example-r1"


def test_branch_node_rejects_non_agent_and_non_return():
    cutoff = datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert sweep._branch_from_node(
        {
            "name": "main",
            "target": {
                "committedDate": "2099-01-01T00:00:00Z",
                "messageHeadline": "Return something",
            },
        },
        cutoff=cutoff,
    ) is None
    assert sweep._branch_from_node(
        {
            "name": "agent/example",
            "target": {
                "committedDate": "2099-01-01T00:00:00Z",
                "messageHeadline": "work in progress",
            },
        },
        cutoff=cutoff,
    ) is None


def test_discovery_queries_full_heads_namespace_and_paginates():
    client = FakeClient(
        [
            _page(
                [
                    {
                        "name": "agent/first",
                        "target": {
                            "committedDate": "2099-01-01T00:00:00Z",
                            "messageHeadline": "Return first",
                        },
                    }
                ],
                more=True,
                cursor="next",
            ),
            _page(
                [
                    {
                        "name": "agent/second",
                        "target": {
                            "committedDate": "2099-01-01T00:00:00Z",
                            "messageHeadline": "Return second",
                        },
                    },
                    {
                        "name": "feature/not-agent",
                        "target": {
                            "committedDate": "2099-01-01T00:00:00Z",
                            "messageHeadline": "Return ignored",
                        },
                    },
                ]
            ),
        ]
    )
    assert sweep.discover_recent_return_branches(client) == ["agent/first", "agent/second"]
    assert len(client.calls) == 2
    query = client.calls[0][2]["query"]
    assert 'refPrefix: "refs/heads/"' in query
    assert 'refPrefix: "refs/heads/agent/"' not in query
    assert client.calls[1][2]["variables"]["after"] == "next"


def test_direct_mode_checks_only_moved_branch(monkeypatch):
    seen = []

    def fake_notify(client, *, branch, issue_number, allow_legacy):
        seen.append((branch, issue_number, allow_legacy))
        return True

    monkeypatch.setattr(sweep, "notify_if_certified", fake_notify)
    client = FakeClient([])
    assert sweep.run(client, issue_number=304, branch="agent/direct") == 0
    assert seen == [("agent/direct", 304, True)]
    assert client.calls == []
