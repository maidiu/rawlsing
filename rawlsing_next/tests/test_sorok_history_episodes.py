"""Experimental sourcefree H1 insertion through the existing objective owner.

The test source explicitly initializes a bounded world policy. Normal sessions
do not have it; none of these proofs issues native world or actor authority.
"""

from copy import deepcopy
from pathlib import Path
import json

import pytest

from rawlsing_next.sorok_history.owner import HistoricalWorld, HistoryRefusal, SurfaceParticular, digest

ENGINE = Path(__file__).resolve().parents[2] / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"


def exact(kind, object_id, body):
    return {"kind": kind, "object_id": object_id, "content_hash": digest(body)}


def source_world(tmp_path, monkeypatch, *, grant=True):
    monkeypatch.syspath_prepend(str(ENGINE))
    from developmental_recursion.p2_owner import load_p2
    fanin = load_p2().start(tmp_path / "world")
    session = fanin.session
    old_parent = session.events()[0]
    here = session.world().positions[session.meta["user_actor"]]
    session.travel("market" if here == "workshop" else "workshop")
    event = session.events()[-1]
    history = HistoricalWorld(session)
    book = history.admit_surface(SurfaceParticular(
        event["event_id"], "source:field-ledger-copy-71", "artifact", event["location"],
        {"condition": "worn"}, ("physical", "provenance", "dependencies")))
    tool = history.admit_surface(SurfaceParticular(
        event["event_id"], "source:measuring-instrument-29", "resource", event["location"],
        {"condition": "used"}, ("physical", "provenance")))
    source_ref = {"kind": "WORLD_EVENT", "object_id": old_parent["event_id"],
                  "content_hash": old_parent["hash"]}
    entities = []
    for kind, identity, details in [
        ("INSTITUTION", "synthetic:cooperative-17", {"name": "Local instrument cooperative"}),
        ("MATERIAL_ACTIVITY", "synthetic:recordkeeping-17", {"operation": "maintenance recordkeeping"}),
        ("PLACE", "synthetic:source-place", {"location": old_parent["location"]}),
        ("PLACE", "synthetic:current-place", {"location": event["location"]}),
    ]:
        record = {"kind": kind, "object_id": identity, "evidence_class": "SOURCEFREE_SYNTHETIC",
                  "source_event_ref": source_ref, **details}
        entities.append({"ref": exact(kind, identity, record), "record": record})
    if grant:
        history.configure_experimental_history(
            source_event_ref=source_ref, target_ids=[book["id"], tool["id"]],
            entities=entities, earliest=old_parent["clock"])
    return fanin, history, book, tool, entities, source_ref


def candidate(leased, book, tool, entities, source_ref):
    packet = leased["packet"]
    actor = packet["actor_refs"][-1]  # Actual rooted other-person identity, not the B alias.
    occurrence = {
        "dependency_group": "z_episode", "asserted_H_class": "H1",
        "effective_time": packet["chronology"]["window"][0] + 1,
        "target_ids": [book["id"], tool["id"]], "action": "USE", "effects": [],
        "actor_refs": [actor], "place_ref": entities[2]["ref"],
        "causal_parents": [source_ref], "source_refs": [source_ref],
        "participants": [{"role": "LABOR_PARTICIPANT", "ref": actor},
                         {"role": "INSTITUTION", "ref": entities[0]["ref"]},
                         {"role": "MATERIAL_ACTIVITY", "ref": entities[1]["ref"]}],
    }
    occurrence["ref"] = exact("OCCURRENCE", "candidate:shared-material-episode", occurrence)
    fact = {"dependency_group": "a_physical", "asserted_H_class": "H0",
            "target_id": book["id"], "predicate": "texture", "value": "fibrous",
            "effective_time": packet["time"]}
    fact["ref"] = exact("FACT", "candidate:book-texture", fact)
    return {"schema": "SOROK_HISTORY_ADMISSION_CANDIDATE@1", "request_id": packet["request_id"],
            "facts": [fact], "occurrences": [occurrence], "links": [],
            "dependencies": [
                {"group_id": "z_episode", "parent_refs": [source_ref], "parent_groups": [],
                 "asserted_H_class": "H1"},
                {"group_id": "a_physical", "parent_refs": [occurrence["ref"]],
                 "parent_groups": ["z_episode"], "asserted_H_class": "H0"}]}


def commit(history, leased, proposal):
    job = leased["job"]
    assert history.record_candidate(job["id"], job["lease_token"], proposal,
                                    {"grade": "MOCK_NOT_LIVE"}) == "CANDIDATE_READY"
    return history.commit_candidate(job["id"])


def test_source_owned_episode_crosses_domains_and_cold_bidirectional_index(tmp_path, monkeypatch):
    fanin, history, book, tool, entities, source_ref = source_world(tmp_path, monkeypatch)
    root = tmp_path / "world"
    try:
        actor_before = deepcopy(fanin.session.world().actor_state)
        perceived_before = set(fanin.session.user_perceived_ids())
        leased = history.lease()
        result = commit(history, leased, candidate(leased, book, tool, entities, source_ref))
        assert result["status"] == "INDEX_READY"
        assert {row["group_id"] for row in result["accepted"]} == {"z_episode", "a_physical"}
        left, right = history.target(book["id"]), history.target(tool["id"])
        assert left["episode_refs"] == right["episode_refs"]
        episode_id = left["episode_refs"][0]["object_id"]
        event = fanin.session.event(episode_id)
        assert event["owner_receipt"]["owner_ref"] == "TEST_ONLY_BP4_WORLD_OWNER"
        assert event["body"]["actor_access"] == "NOT_GRANTED"
        assert fanin.session.world().actor_state == actor_before
        assert fanin.session.user_perceived_ids() == perceived_before
        graph = history.history_graph()
        assert {edge["relation"] for edge in graph["edges"]} >= {
            "MATERIAL_PARTICIPANT", "OBJECTIVE_PARTICIPANT", "INSTITUTION", "MATERIAL_ACTIVITY"}
        reverse = history.query_relations(entities[0]["ref"]["object_id"])
        assert {book["id"], tool["id"]} <= {
            edge["subject_ref"]["object_id"] for edge in reverse["edges"]}
        assert history.query_relations(book["id"], consumer="USER")["status"] == "HELD"
        assert history.query_relations(book["id"], consumer="ACTOR")["edges"] == []
        assert history.commit_candidate(leased["job"]["id"]) == result
    finally:
        fanin.close()
    from developmental_recursion.p2_owner import load_p2
    cold = load_p2().open(root)
    try:
        owner = HistoricalWorld(cold.session)
        assert owner.history_graph() == graph
        assert owner.query_relations(entities[0]["ref"]["object_id"]) == reverse
    finally:
        cold.close()


def test_missing_h1_owner_holds_without_dropping_unrelated_h0(tmp_path, monkeypatch):
    fanin, history, book, tool, entities, source_ref = source_world(tmp_path, monkeypatch, grant=False)
    try:
        leased = history.lease()
        packet = leased["packet"]
        assert "H1_OWNER_NOT_GRANTED" in packet["source_limits"]
        fact = {"dependency_group": "physical", "asserted_H_class": "H0",
                "target_id": book["id"], "predicate": "texture", "value": "fibrous",
                "effective_time": packet["time"]}
        fact["ref"] = exact("FACT", "unrelated-physical", fact)
        episode = {"dependency_group": "episode", "asserted_H_class": "H1",
                   "target_ids": [book["id"]], "effective_time": packet["time"],
                   "action": "USE", "effects": [], "causal_parents": packet["event_refs"]}
        episode["ref"] = exact("OCCURRENCE", "ungranted-episode", episode)
        result = commit(history, leased, {
            "request_id": packet["request_id"], "facts": [fact], "occurrences": [episode],
            "links": [], "dependencies": []})
        assert result["status"] == "PARTIAL_HELD"
        assert any(row["reason"] == "H1_OWNER_NOT_GRANTED" for row in result["held"])
        assert history.target(book["id"])["physical_depth"]["texture"]["value"] == "fibrous"
        assert not any(e["kind"] == "HISTORICAL_MATERIAL" for e in fanin.session.events())
    finally:
        fanin.close()


@pytest.mark.parametrize("fault", ["actor_effect", "chronology", "institution", "wrong_place",
                                  "closed_actor_event", "role_kind", "owner_suppressed"])
def test_h1_negative_group_preserves_independent_physical_fact(tmp_path, monkeypatch, fault):
    fanin, history, book, tool, entities, source_ref = source_world(tmp_path, monkeypatch)
    try:
        actors = deepcopy(fanin.session.world().actor_state)
        leased = history.lease()
        proposal = candidate(leased, book, tool, entities, source_ref)
        physical = proposal["dependencies"][1]
        physical["parent_refs"] = leased["packet"]["event_refs"]
        physical["parent_groups"] = []
        episode = proposal["occurrences"][0]
        if fault == "actor_effect":
            episode["effects"] = {"actor_state": {"memory": "invented"}}
        elif fault == "chronology":
            episode["effective_time"] = source_ref["content_hash"]  # Not an integer time.
        elif fault == "institution":
            episode["participants"][1]["ref"] = exact("INSTITUTION", "unadmitted", {})
        elif fault == "role_kind":
            episode["participants"][1]["ref"] = episode["actor_refs"][0]
        elif fault == "wrong_place":
            episode["place_ref"] = entities[3]["ref"]
        elif fault == "closed_actor_event":
            episode["effective_time"] = leased["packet"]["chronology"]["window"][0]
        else:
            from bp4.world import WorldRefusal
            def deny(*args, **kwargs):
                raise WorldRefusal("H1_OWNER_NOT_GRANTED")
            monkeypatch.setattr(type(fanin.session.world()), "admit_material_history", deny)
        result = commit(history, leased, proposal)
        assert result["status"] == "PARTIAL_HELD"
        assert history.qualified_physical_fact(book["id"], "texture")["value"] == "fibrous"
        assert not history.target(book["id"]).get("episode_refs")
        assert fanin.session.world().actor_state == actors
        assert not any(e["kind"] == "HISTORICAL_MATERIAL" for e in fanin.session.events())
    finally:
        fanin.close()


@pytest.mark.parametrize("pending_first", [False, True])
def test_h1_material_parent_is_consumed_by_normal_p4_work_not_inspection(tmp_path, monkeypatch, pending_first):
    from rawlsing_next.tests.test_sorok_history_activity import _work_cli
    from rawlsing_next.sorok_history.provider import HistoricalModelProvider
    p4 = ENGINE.parent / "SOROK-P4-FIRST-FULL-MPC-R1"
    monkeypatch.syspath_prepend(str(p4))
    from run_p4 import new, open_owner, run_history_worker, check_boundary, advance_dispatched
    captured = {}

    def establish(session):
        # Trusted, explicitly TEST_ONLY source setup before publishing the opening.
        here = session.world().positions[session.meta["user_actor"]]
        session.travel("market" if here == "workshop" else "workshop")
        session.travel(here)
        h = HistoricalWorld(session)
        first = h.target(h.capture_visible_tool_resource())
        event = session.events()[-1]
        second = h.admit_surface(SurfaceParticular(
            event["event_id"], "source:maintenance-record-copy-4", "artifact", here,
            {"condition": "worn"}, ("provenance",)))
        parent = session.events()[0]
        parent_ref = {"kind": "WORLD_EVENT", "object_id": parent["event_id"],
                      "content_hash": parent["hash"]}
        entities = []
        for kind, identity, details in [
            ("INSTITUTION", "synthetic:maintenance-cooperative", {"name": "Maintenance cooperative"}),
            ("MATERIAL_ACTIVITY", "synthetic:equipment-use", {"operation": "equipment maintenance"}),
            ("PLACE", "synthetic:activity-place", {"location": here}),
        ]:
            record = {"kind": kind, "object_id": identity, "evidence_class": "SOURCEFREE_SYNTHETIC",
                      "source_event_ref": parent_ref, **details}
            entities.append({"ref": exact(kind, identity, record), "record": record})
        h.configure_experimental_history(source_event_ref=parent_ref,
            target_ids=[first["id"], second["id"]], entities=entities, earliest=parent["clock"])
        captured.update(first=first, second=second, entities=entities, parent=parent_ref)

    state = tmp_path / "encounter"
    state.mkdir()
    new(state, state / "p4_receipts.json", "recognized_plan", establish=establish)
    initial = open_owner(state / "actual-p2")
    try:
        initial_material = initial.base_owner.fanin.session.world().actor_state["A"]["material_remaining"]
    finally:
        initial.close()
    if pending_first:
        assert _work_cli(state, monkeypatch)["status"] == "HELD"
    async def transport(request):
        packet = json.loads(request["prompt"].split("Packet:\n", 1)[1])
        proposal = candidate({"packet": packet}, captured["first"], captured["second"],
                             captured["entities"], captured["parent"])
        proposal["facts"][0].update(predicate="condition", value="serviceable")
        body = {key: value for key, value in proposal["facts"][0].items() if key != "ref"}
        proposal["facts"][0]["ref"] = exact("FACT", "candidate:serviceability", body)
        return {"text": json.dumps(proposal), "model": "mock-experimental-history"}
    admitted = run_history_worker(state, provider=HistoricalModelProvider(transport=transport))
    assert admitted["status"] == "INDEX_READY"
    if pending_first:
        assert admitted["activity"][0]["activity"]["status"] == "ADVANCED"
        cold = open_owner(state / "actual-p2")
        try:
            current = cold.base_owner.fanin.session
            assert current.world().actor_state["A"]["material_remaining"] == initial_material - 1
            assert not any(e["kind"] == "INSPECT" for e in current.events())
        finally:
            cold.close()
        return
    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        history = HistoricalWorld(session)
        ledger = json.loads((state / "p4_receipts.json").read_text())
        check_boundary(owner, ledger)  # A valid hidden episode does not break the viewer ABI.
        before = session.world().actor_state["A"]["material_remaining"]
        original_event = session.event
        with monkeypatch.context() as patch:
            patch.setattr(session, "event", lambda ref: (
                None if ref == captured["parent"]["object_id"] else original_event(ref)))
            held = advance_dispatched(owner.base_owner.fanin)
            assert held["status"] == "HELD"
            assert held["activity"]["refusal_code"] == "HISTORICAL_PARENT_MISSING"
            assert session.world().actor_state["A"]["material_remaining"] == before
        qualified = history.query_depth(captured["first"]["id"])
        assert qualified["episodes"]
    finally:
        owner.close()
    used = _work_cli(state, monkeypatch)
    assert used["activity"]["status"] == "ADVANCED"
    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        assert session.world().actor_state["A"]["material_remaining"] == before - 1
        assert not any(e["kind"] == "INSPECT" for e in session.events())
    finally:
        owner.close()


def test_cold_withheld_source_restores_exact_readset_index_and_public_read(tmp_path, monkeypatch):
    fanin, history, book, tool, entities, source_ref = source_world(tmp_path, monkeypatch)
    root = tmp_path / "world"
    try:
        leased = history.lease()
        result = commit(history, leased, candidate(leased, book, tool, entities, source_ref))
        assert result["status"] == "INDEX_READY"
        event = history.inspect(book["id"])
        observed = history.read_inspection(event["event_id"])
        assert "episodes" not in observed
        depth = history.query_depth(book["id"])
        graph = history.history_graph()
        # The index is a disposable projection, not a second canonical history.
        with history._write() as (_, state):
            del state["graph_index"]
        assert history.rebuild_history_index() == graph
        withheld = history.test_withhold_event_source(source_ref["object_id"])
    finally:
        fanin.close()
    from developmental_recursion.p2_owner import load_p2
    cold = load_p2().open(root)
    try:
        history = HistoricalWorld(cold.session)
        with pytest.raises(HistoryRefusal, match="HISTORICAL_PARENT_MISSING"):
            history.query_depth(book["id"])
        with pytest.raises(HistoryRefusal, match="HISTORICAL_PARENT_MISSING"):
            history.read_inspection(event["event_id"])
        # Canonical occurrence remains; source unavailable is not event absence.
        assert cold.session.event(source_ref["object_id"])["hash"] == source_ref["content_hash"]
        history.test_restore_event_source(withheld)
    finally:
        cold.close()
    restored = load_p2().open(root)
    try:
        history = HistoricalWorld(restored.session)
        assert history.query_depth(book["id"]) == depth
        assert history.history_graph() == graph
        assert history.read_inspection(event["event_id"]) == observed
    finally:
        restored.close()


def test_committed_history_link_activates_coalesced_t2_without_inspection(tmp_path, monkeypatch):
    from rawlsing_next.sorok_history.provider import HistoricalModelProvider
    from rawlsing_next.sorok_history.runtime import run_once
    import asyncio
    fanin, history, book, tool, entities, source_ref = source_world(tmp_path, monkeypatch)
    try:
        leased = history.lease()
        before_jobs = len(history._state(fanin.session.world())["outbox"])
        admitted = commit(history, leased, candidate(leased, book, tool, entities, source_ref))
        assert admitted["status"] == "INDEX_READY"
        assert len(history._state(fanin.session.world())["outbox"]) == before_jobs
        [followup_id] = admitted["followup_jobs"]
        followup = history.job(followup_id)
        assert followup["target_id"] == tool["id"]
        assert followup["trigger"] == "HISTORY_DEPENDENCY"
        assert followup["original_trigger"] == "NEW_WORLD_PARTICULAR"
        assert followup["generation_depth"] == 1
        assert followup["history_dependency_refs"] == history.target(tool["id"])["episode_refs"]
        assert not any(e["kind"] == "INSPECT" for e in fanin.session.events())
        calls = []
        async def transport(request):
            packet = json.loads(request["prompt"].split("Packet:\n", 1)[1])
            calls.append(packet)
            assert packet["authority"]["allowed_H_classes"] == ["H0"]
            assert packet["surface"][tool["id"]]["history_dependency_refs"]
            fact = {"dependency_group": "detail", "asserted_H_class": "H0",
                    "target_id": tool["id"], "predicate": "texture", "value": "brushed",
                    "effective_time": packet["time"]}
            fact["ref"] = exact("FACT", "linked-instrument-texture", fact)
            return {"model": "mock-t2-history", "text": json.dumps({
                "request_id": packet["request_id"], "facts": [fact], "occurrences": [],
                "links": [], "dependencies": [{"group_id": "detail", "asserted_H_class": "H0",
                    "parent_refs": followup["history_dependency_refs"], "parent_groups": []}]})}
        completed = asyncio.run(run_once(history, HistoricalModelProvider(transport=transport)))
        assert completed["status"] == "INDEX_READY" and len(calls) == 1
        assert history.qualified_physical_fact(tool["id"], "texture")["value"] == "brushed"
        for target in [book, tool]:
            event = history.inspect(target["id"])
            assert history.read_inspection(event["event_id"])["physical"]
        assert history.target(book["id"])["episode_refs"] == history.target(tool["id"])["episode_refs"]
    finally:
        fanin.close()


def test_cold_source_restoration_reuses_bound_candidate_without_a_provider(tmp_path, monkeypatch):
    import asyncio
    from rawlsing_next.sorok_history.runtime import run_once
    fanin, history, book, tool, entities, source_ref = source_world(tmp_path, monkeypatch)
    root = tmp_path / "world"
    try:
        leased = history.lease()
        job = leased["job"]
        proposal = candidate(leased, book, tool, entities, source_ref)
        assert history.record_candidate(job["id"], job["lease_token"], proposal,
                                        {"grade": "MOCK_NOT_LIVE"}) == "CANDIDATE_READY"
        withheld = history.test_withhold_event_source(source_ref["object_id"])
        held = history.commit_candidate(job["id"])
        assert held["status"] == "SOURCE_HELD"
        assert not any(e["kind"] == "HISTORICAL_MATERIAL" for e in fanin.session.events())
        history.test_restore_event_source(withheld)
    finally:
        fanin.close()
    from developmental_recursion.p2_owner import load_p2
    cold = load_p2().open(root)
    try:
        history = HistoricalWorld(cold.session)
        recovered = asyncio.run(run_once(history, None))
        assert recovered["status"] == "INDEX_READY"
        assert history.job(job["id"])["attempt"] == 1
        assert history.job(job["id"])["source_holds"] == [held]
        assert history.commit_candidate(job["id"]) == recovered
        assert len([e for e in cold.session.events() if e["kind"] == "HISTORICAL_MATERIAL"]) == 1
    finally:
        cold.close()


def test_sealed_root_is_not_replaced_by_fork_private_history(tmp_path, monkeypatch):
    fanin, history, book, tool, entities, source_ref = source_world(tmp_path, monkeypatch)
    root = tmp_path / "world"
    try:
        leased = history.lease()
        assert commit(history, leased, candidate(leased, book, tool, entities, source_ref))["status"] == "INDEX_READY"
        sealed = history.root_tool_baseline("workshop")
        root_checkpoints = deepcopy(fanin.session.product.store.checkpoints("root"))
        held = history.request_shared_precontact("artifact:shared-acquisition", ["provenance"])
        assert held["reason"] == "ROOT_HISTORY_WRITE_NOT_GRANTED"
        original_jobs = deepcopy(history._state(fanin.session.world())["outbox"])
        assert history.request_shared_precontact("artifact:different-order", ["provenance"])["status"] == "HELD"
        assert history._state(fanin.session.world())["outbox"] == original_jobs
        fanin.session.fork_alt("experimental-h1-child")
        assert history.root_tool_baseline("workshop") == sealed
        assert history.target(book["id"]) is None
        assert history.query_relations(book["id"])["status"] == "UNKNOWN"
        assert history.request_shared_precontact("artifact:shared-acquisition", ["provenance"]) == held
        assert fanin.session.product.store.checkpoints("root") == root_checkpoints
        fanin.session.fork_alt("experimental-h1-nested")
        assert history.target(tool["id"]) is None
        assert history.query_relations(entities[0]["ref"]["object_id"])["edges"] == []
    finally:
        fanin.close()
    from developmental_recursion.p2_owner import load_p2
    cold = load_p2().open(root)
    try:
        history = HistoricalWorld(cold.session)
        assert history.root_tool_baseline("workshop") == sealed
        assert history.request_shared_precontact("artifact:shared-acquisition", ["provenance"]) == held
        assert history.lease() is None
    finally:
        cold.close()


def test_cold_deleted_canonical_episode_is_rejected_then_exact_bytes_restore(tmp_path, monkeypatch):
    """Privileged corruption of this disposable fixture, not a runtime write API.

    The append-only trigger is removed only on the closed test database to
    simulate a hostile owner bypass. Normal runtime triggers remain unchanged.
    """
    import sqlite3
    fanin, history, book, tool, entities, source_ref = source_world(tmp_path, monkeypatch)
    root = tmp_path / "world"
    try:
        leased = history.lease()
        assert commit(history, leased, candidate(leased, book, tool, entities, source_ref))["status"] == "INDEX_READY"
        episode_id = history.target(book["id"])["episode_refs"][0]["object_id"]
        inspected = history.inspect(book["id"])
        public = history.read_inspection(inspected["event_id"])
        depth = history.query_depth(book["id"])
        graph = history.history_graph()
        database = Path(fanin.session.product.store.path)
        assert tmp_path.resolve() in database.resolve().parents
    finally:
        fanin.close()
    original = database.read_bytes()
    from developmental_recursion.p2_owner import load_p2
    try:
        with sqlite3.connect(database) as connection:
            connection.execute("DROP TRIGGER world_event_no_delete")
            removed = connection.execute("DELETE FROM world_event WHERE event_id=?", (episode_id,))
            assert removed.rowcount == 1
        with pytest.raises(ValueError, match="S37_PROVENANCE_MISMATCH") as refused:
            load_p2().open(root)
        assert '"c12_branch_ok": false' in str(refused.value)
    finally:
        database.write_bytes(original)
    restored = load_p2().open(root)
    try:
        history = HistoricalWorld(restored.session)
        assert history.query_depth(book["id"]) == depth
        assert history.history_graph() == graph
        assert history.read_inspection(inspected["event_id"]) == public
        assert restored.session.product.c12_verify(restored.session.branch_id)["ok"]
    finally:
        restored.close()


def test_actor_testimony_is_not_a_world_history_policy_source(tmp_path, monkeypatch):
    fanin, history, book, tool, entities, _ = source_world(tmp_path, monkeypatch, grant=False)
    try:
        speech = next(event for event in fanin.session.events() if event["kind"] == "SPEECH")
        ref = {"kind": "WORLD_EVENT", "object_id": speech["event_id"], "content_hash": speech["hash"]}
        with pytest.raises(HistoryRefusal, match="H1_SOURCE_POLICY_INVALID"):
            history.configure_experimental_history(source_event_ref=ref,
                target_ids=[book["id"], tool["id"]], entities=[], earliest=speech["clock"])
        assert "H1_OWNER_NOT_GRANTED" in history.lease()["packet"]["source_limits"]
    finally:
        fanin.close()


def test_idle_is_bounded_coalesces_inspection_and_yields_to_new_causal_work(tmp_path, monkeypatch):
    import asyncio
    from rawlsing_next.sorok_history.provider import HistoricalModelProvider
    from rawlsing_next.sorok_history.runtime import run_once
    fanin, history, book, tool, entities, source_ref = source_world(tmp_path, monkeypatch, grant=False)
    calls = []
    async def transport(request):
        packet = json.loads(request["prompt"].split("Packet:\n", 1)[1])
        calls.append(packet)
        [target_id] = packet["target_ids"]
        predicate = packet["surface"][target_id].get("requested_predicate", "texture")
        value = {"texture": "matte", "color": "grey", "marking": "unmarked", "condition": "used"}[predicate]
        fact = {"dependency_group": "detail", "asserted_H_class": "H0",
                "target_id": target_id, "predicate": predicate, "value": value,
                "effective_time": packet["time"]}
        return {"model": "mock-idle", "text": json.dumps({
            "request_id": packet["request_id"] , "facts": [fact], "occurrences": [], "links": [],
            "dependencies": [{"group_id": "detail", "parent_refs": packet["event_refs"],
                              "parent_groups": [], "asserted_H_class": "H0"}]})}
    provider = HistoricalModelProvider(transport=transport)
    try:
        assert history.enqueue_idle()["reason"] == "CAUSAL_BACKLOG_FIRST"
        for _ in range(2):
            assert asyncio.run(run_once(history, provider))["status"] == "INDEX_READY"
        [idle_id] = history.enqueue_idle()["jobs"]
        idle = history.job(idle_id)
        count = len(history._state(fanin.session.world())["outbox"])
        history.inspect(idle["target_id"], predicate=idle["requested_predicate"])
        assert len(history._state(fanin.session.world())["outbox"]) == count
        assert history.job(idle_id)["inspection_priority_event"]
        # An actively requested inspection is now urgent, and keeps the same job.
        assert asyncio.run(run_once(history, provider))["job_id"] == idle_id
        [idle_id] = history.enqueue_idle()["jobs"]
        existing_surface = history.target(book["id"])["surface"]
        new_target = history.admit_surface(SurfaceParticular(
            existing_surface["occurrence_id"], "source:spare-measuring-piece", "item",
            existing_surface["location"], {"condition": "used"}, ("physical",)))
        urgent = history.lease()
        assert urgent["target"]["id"] == new_target["id"]
        assert urgent["job"]["trigger"] == "NEW_WORLD_PARTICULAR"
        history.record_failure(urgent["job"]["id"], urgent["job"]["lease_token"],
                               "TEST_SOURCE_WORK_CANCELED", retryable=False)
        assert asyncio.run(run_once(history, provider))["job_id"] == idle_id
        for _ in range(8):
            queued = history.enqueue_idle()
            if queued["status"] == "NO_WORK":
                break
            assert asyncio.run(run_once(history, provider))["status"] == "INDEX_READY"
        else:
            pytest.fail("idle overhang did not reach its finite budget")
        counts = history._state(fanin.session.world())["idle_generations"]
        assert max(counts.values()) == 2
        assert len(calls) <= 2 + 2 * 3
        assert history.enqueue_idle()["status"] == "NO_WORK"
    finally:
        fanin.close()


def test_provider_timeout_is_durable_instead_of_expiring_its_own_lease(tmp_path, monkeypatch):
    import asyncio
    from types import SimpleNamespace
    from rawlsing_next.sorok_history.provider import ProviderTimeout
    from rawlsing_next.sorok_history.runtime import run_once
    from rawlsing_next.sorok_history import owner as owner_module
    fanin, history, *_ = source_world(tmp_path, monkeypatch)
    clock = [1000.0]
    monkeypatch.setattr(owner_module.time, 'time', lambda: clock[0])

    class Provider:
        config = SimpleNamespace(timeout_s=120, max_attempts=1, retry_delay_s=0)

        async def propose(self, packet):
            clock[0] += 120
            raise ProviderTimeout('bounded endpoint timeout', code='TIMEOUT')

    try:
        result = asyncio.run(run_once(history, Provider()))
        assert result['status'] == 'FAILED_RETRYABLE'
        job = history.job(result['job_id'])
        assert job['failure_code'] == 'TIMEOUT'
        assert job['provider_receipt']['failure_grade'] == 'TRANSIENT'
        assert job['expires_at'] > clock[0]
    finally:
        fanin.close()
