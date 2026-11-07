from copy import deepcopy

from gaze import attend, orientation, render, visible_events


def occurrence(ref, kind, *, perceived=True, speaker="A", text=""):
    return {
        "event_id": ref, "kind": kind, "perceived_by_user": perceived,
        "actor_visible_id": speaker, "summary": f"Observable {ref}.",
        "body_public": {"text": text},
    }


def test_distinct_practices_select_distinct_facts_without_changing_world():
    surface = {"observations": [
        occurrence("arrive", "ARRIVAL"), occurrence("move", "MOVE"),
        occurrence("repair", "REPAIR"), occurrence("inspect", "INSPECT"),
        occurrence("question", "SPEECH", text="Could you hold this?"),
        occurrence("private", "SPEECH", perceived=False, text="hidden"),
    ]}
    before = deepcopy(surface)
    work = attend(surface, attend(surface, [], "repair"), "inspect")
    movement = attend(surface, attend(surface, [], "arrive"), "move")
    assert attend(surface, work, "private") is None
    assert attend(surface, work, "repair") == work
    left = render(surface, work, boundary="question")
    right = render(surface, movement, boundary="question")
    assert [r["event_id"] for r in left] == ["repair", "inspect", "question"]
    assert [r["event_id"] for r in right] == ["arrive", "move", "question"]
    assert left[-1] == right[-1] == {
        "event_id": "question", "text": "Nadia says, “Could you hold this?”",
    }
    assert render(surface, work, candidates=["private"], boundary="private") == []
    assert surface == before


def test_sparse_or_tied_evidence_does_not_assert_a_preference():
    surface = {"observations": [
        occurrence("arrive", "ARRIVAL"), occurrence("move", "MOVE"),
        occurrence("repair", "REPAIR"), occurrence("inspect", "INSPECT"),
    ]}
    visible = visible_events(surface)
    assert orientation(visible, ["repair", "repair", "repair"]) is None
    assert orientation(visible, list(visible)) is None
    assert orientation(visible, ["repair", "inspect"]) == "work"


def test_a_reserved_reply_keeps_its_place_before_later_work():
    surface = {"observations": [
        occurrence("reply", "SPEECH", text="I'll check it first."),
        occurrence("repair", "REPAIR"),
    ]}
    narration = render(surface, [], candidates=["repair"], boundary="reply")
    assert [row["event_id"] for row in narration] == ["reply", "repair"]
