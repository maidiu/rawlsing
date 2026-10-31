from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import (
    access,
    binding,
    event,
    post_snapshot,
    projection,
    response,
    snapshot,
    year_input,
)

from v3core_adapter.contracts import Status
from v3core_adapter.derived_scope import material_capacity_index
from v3core_adapter.ledger import HistoricalProjection
from v3core_adapter.quarantine import forbidden_default_reasons
from v3core_adapter.scheduler import run_year

ROOT = Path(__file__).resolve().parents[1]


def test_cold_process_reloads_identical_material_projection(tmp_path: Path) -> None:
    ledger = tmp_path / "projection.json"
    proj = projection()
    result = run_year(proj, year_input(prior=proj.prior_snapshot), ledger_path=str(ledger))
    assert result.committed is True
    assert proj.state.capacity.money == 56.0
    assert material_capacity_index(proj.state) == pytest.approx(11.6)
    env = dict(os.environ)
    env["PYTHONPATH"] = f"{ROOT}:{ROOT / 'vendor'}:{ROOT / 'vendor' / 'py3deps'}"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    probe = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "cold_probe.py"), str(ledger)],
        env=env,
        capture_output=True,
        text=True,
    )
    assert probe.returncode == 0, probe.stderr
    payload = json.loads(probe.stdout)
    assert payload["state_hash"] == proj.state_hash()
    assert payload["cash"] == 56.0
    assert payload["years"] == 1
    assert payload["applied_event_ids"] == ["EV_MARKET_WORK"]
    assert payload["forbidden_default_reasons"] == []
    assert payload["canonical_c9_claimed"] is False
    assert payload["rival_store_created"] is False
    loaded = HistoricalProjection.load(ledger)
    assert loaded.state_hash() == proj.state_hash()
    assert forbidden_default_reasons(loaded.state) == []


def test_failed_commit_leaves_existing_ledger_unchanged(tmp_path: Path, monkeypatch) -> None:
    ledger = tmp_path / "projection.json"
    proj = projection()
    run_year(proj, year_input(prior=proj.prior_snapshot), ledger_path=str(ledger))
    original = hashlib.sha256(ledger.read_bytes()).hexdigest()
    second = projection()
    second.state = proj.state
    second.prior_snapshot = proj.prior_snapshot
    second.years = list(proj.years)
    second.applied_event_ids = list(proj.applied_event_ids)
    second.material_facts = dict(proj.material_facts)

    def fail_save(self, *args, **kwargs):
        raise OSError("simulated save failure")

    monkeypatch.setattr(HistoricalProjection, "save", fail_save)
    request = year_input(
        annual_year=2,
        events=(event(event_id="EV2"),),
        accesses=(access(event_id="EV2"),),
        responses=(response(event_id="EV2"),),
        bindings=(binding(event_id="EV2", annual_year=2),),
        prior=snapshot(cash=56.0, completed_units=4.0),
        post=post_snapshot(cash=58.0, completed_units=5.0),
    )
    result = run_year(second, request, ledger_path=str(ledger))
    assert result.status == Status.HELD_TRANSACTION_ABORTED
    assert result.committed is False
    assert hashlib.sha256(ledger.read_bytes()).hexdigest() == original
    assert second.state.capacity.money == 56.0


def test_source_event_removal_then_restored_positive() -> None:
    proj = projection()
    before = proj.state_hash()
    removed = run_year(
        proj,
        year_input(events=(), accesses=(), responses=(), bindings=(binding("EV_MARKET_WORK"),)),
    )
    assert removed.status == Status.HELD_SOURCE_EVENT_WITHDRAWN
    assert proj.state_hash() == before
    restored = run_year(proj, year_input(prior=proj.prior_snapshot))
    assert restored.status == Status.APPLIED_TEST_ONLY_SOURCEFREE
    assert restored.committed is True
    assert restored.material_index_after - restored.material_index_before == pytest.approx(0.3)
    assert proj.state.capacity.money == 56.0


def test_second_actual_event_continues_durable_history(tmp_path: Path) -> None:
    ledger = tmp_path / "projection.json"
    proj = projection()
    first = run_year(proj, year_input(prior=proj.prior_snapshot), ledger_path=str(ledger))
    assert first.committed is True
    second = run_year(
        proj,
        year_input(
            annual_year=2,
            events=(event(event_id="EV2"),),
            accesses=(access(event_id="EV2"),),
            responses=(response(event_id="EV2"),),
            bindings=(binding(event_id="EV2", annual_year=2),),
            prior=snapshot(cash=56.0, completed_units=4.0),
            post=post_snapshot(cash=58.0, completed_units=5.0),
        ),
        ledger_path=str(ledger),
    )
    assert second.status == Status.APPLIED_TEST_ONLY_SOURCEFREE
    assert second.committed is True
    assert proj.state.capacity.money == 58.0
    loaded = HistoricalProjection.load(ledger)
    assert loaded.state_hash() == proj.state_hash()
    assert len(loaded.years) == 2
    assert loaded.applied_event_ids == ["EV_MARKET_WORK", "EV2"]
