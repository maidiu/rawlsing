"""Focused S50 recovered V3 actor-state tests."""
from __future__ import annotations
import shutil
from pathlib import Path
import pytest
from s50.bootstrap import install
install()
from s45.fixtures import root_bundle
from s37.harness import case_for, source_for
from s50.recovery import verify_source, run_legacy_fixture
from s50.session import S50Session


def _start(state):
    c=case_for(True)
    return S50Session.start(state,bundle=root_bundle("01"*32),case=c,source=source_for(c),language_context={"milieu_id":"workshop"})


def test_source_identities_all_31_exact():
    v=verify_source(); assert v["count"]==31; assert v["all_exact"] is True; assert v["fixture_sha256"]


def test_legacy_v3_roundtrip_pressure_flow_and_projection():
    r=run_legacy_fixture(years=1)
    assert r["roundtrip_exact"] is True
    assert r["year"]==2001 and r["age"]==31
    assert r["pressure_flow_history_count"]>=1
    assert r["expectation_baseline"]
    assert r["projection"]["read_only"] is True
    assert r["projection"]["second_mind"] is False
    assert r["actual_person_commit"] is False
    assert "ACTUAL_ROOT_MISSING_BACKBONE_STATE" in r["projection"]["unknowns"]


def test_actual_root_missing_state_hold_and_projection_is_isolated(tmp_path):
    s=_start(tmp_path/"actual")
    try:
        before=(len(s.world().events),len(s.read_events()),s.clock())
        missing=s.actual_root_missing()
        assert missing["status"]=="SOURCE_OWNER_HOLD"
        assert "backbone_state" in missing["missing_fields"]
        made=s.materialize_legacy_projection(years=1)
        assert made["actual_person_commit"] is False
        assert made["source_all_exact"] is True
        assert made["fixture_sha256"]
        after=(len(s.world().events),len(s.read_events()),s.clock())
        assert after==before
        p=s.read_projection()
        assert p["fixture_only"] is True and p["read_only"] is True
        assert p["actual_person_commit"] is False
        assert s.verify()["ok"] is True
    finally: s.close()


def test_projection_cold_reopen_same_canonical_store(tmp_path):
    state=tmp_path/"cold"; s=_start(state)
    try:
        made=s.materialize_legacy_projection(years=1)
        h=made["projection_hash"]
    finally: s.close()
    c=S50Session.open(state)
    try:
        p=c.read_projection()
        assert p is not None and p["projection"]["state_sha256"]==h
        assert p["actual_person_commit"] is False
        assert c.verify()["ok"] is True
    finally: c.close()


def test_projection_source_identity_mismatch_fails_closed(tmp_path):
    s=_start(tmp_path/"mismatch")
    try:
        from s50 import session as mod
        orig=mod.verify_source
        mod.verify_source=lambda: {"all_exact":False,"count":0,"rows":[]}
        try:
            with pytest.raises(Exception):
                s.materialize_legacy_projection(years=1)
        finally:
            mod.verify_source=orig
    finally: s.close()
