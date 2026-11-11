"""Joined MI/MII/MIII causal differential through the existing P6 and work CLI."""

from argparse import Namespace
import shutil
from pathlib import Path

from rawlsing_next.tests.test_sorok_history_activity import _mock_provider, _work_cli

P6 = Path(__file__).resolve().parents[2] / "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1"


def test_private_gaze_changes_view_not_independent_history_activity(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(P6))
    from run_p6 import experience
    from run_p4 import open_owner, run_history_worker
    from rawlsing_next.sorok_history.owner import HistoricalWorld

    def view(state, command="view", **kwargs):
        return experience(state, Namespace(command=command, request_id=None, **kwargs))

    state, frozen = tmp_path / "current", tmp_path / "frozen-bytes"
    view(state, "new")
    owner = open_owner(state / "actual-p2")
    try:
        history = HistoricalWorld(owner.base_owner.fanin.session)
        target = history.target_for_referent("world-resource:workshop:tool")
    finally:
        owner.close()
    admitted = run_history_worker(state, provider=_mock_provider(target["id"], "serviceable"))
    assert admitted["status"] == "INDEX_READY"
    view(state)  # History-only commits must be compatible with the P6 reader.
    shutil.copytree(state, frozen)
    results = []
    for index, focus in enumerate(["bench", "mug"]):
        if index:
            # Preserve the root-bound absolute path. Opening a copied live root
            # at another location is correctly refused by the existing owner.
            shutil.rmtree(state)
            shutil.copytree(frozen, state)
        view(state, "mii-enable-learning")
        view(state, "mii-correct-attention", target=focus, weight=20)
        outcome = _work_cli(state, monkeypatch)
        assert outcome["activity"]["status"] == "ADVANCED"
        # The ordinary viewer must reopen after the independent owner changed
        # history and performed exactly one S46 interval, without an inspection.
        presented = view(state)
        owner = open_owner(state / "actual-p2")
        try:
            session = owner.base_owner.fanin.session
            assert not any(event["kind"] == "INSPECT" for event in session.events())
            history = HistoricalWorld(session)
            actual_target = history.target(target["id"])
            assert actual_target["physical_depth"]["condition"]["value"] == "serviceable"
            results.append((session.world().snapshot(), session.read_events(),
                            session.read_interval_states(), owner.store.head(), presented))
        finally:
            owner.close()
    assert results[0][:4] == results[1][:4]
    assert results[0][4]["mii_surface"]["mandatory"] == results[1][4]["mii_surface"]["mandatory"]
    assert results[0][4]["detail"] != results[1][4]["detail"]


@__import__('pytest').mark.parametrize('reader', ['P5', 'P6'])
def test_existing_situated_reader_consumes_only_actual_inspection_projection(tmp_path, monkeypatch, reader):
    import importlib
    p5 = P6.parent / 'SOROK-P5-CONTINUOUS-EXPERIENCE-R1'
    monkeypatch.syspath_prepend(str(P6 if reader == 'P6' else p5))
    module = importlib.import_module('run_p6' if reader == 'P6' else 'run_p5')
    from run_p4 import open_owner, run_history_worker
    state = tmp_path / 'reader'
    module.experience(state, Namespace(command='new', history='recognized_plan', request_id=None))
    owner = open_owner(state / 'actual-p2')
    try:
        from rawlsing_next.sorok_history.owner import HistoricalWorld
        target = HistoricalWorld(owner.base_owner.fanin.session).visible_surfaces()[0]['id']
    finally:
        owner.close()
    admitted = run_history_worker(state, provider=_mock_provider(target, 'serviceable'))
    assert admitted['status'] == 'INDEX_READY'
    observed = module.experience(state, Namespace(command='inspect-particular',
        target=target, property='condition', request_id='bounded-physical-inspection'))
    assert observed['admission'] == 'ADMITTED'
    assert observed['observation']['physical'][0]['value'] == 'serviceable'
    assert not {'episodes', 'history_graph', 'actor_refs'} & set(observed['observation'])
    refused = module.experience(state, Namespace(command='inspect-particular',
        target='unadmitted-target', property='condition', request_id='unavailable'))
    assert refused['admission'] == 'UNAVAILABLE'
    assert refused['observation'] is None
