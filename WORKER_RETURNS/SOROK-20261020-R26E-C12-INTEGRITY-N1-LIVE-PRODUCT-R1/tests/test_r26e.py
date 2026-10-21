"""R26E qualified C12, N1 port integration and product court."""
from __future__ import annotations

import json
import sqlite3

import pytest

from bp2p4.assertion import joined_downstream_a0_a2_assertion
from bp2p4.severance import run_all_severances, severance_receipt
from bp4.store import C12Store
from n1_eligibility import GRADE, seal_record, screen

from r26e.c12_integrity import (
    EXTERNAL_WITNESS_GRADE,
    TRUST_CUSTODY_HOLD,
    ExternalCheckpointWitness,
    QualifiedC12Store,
    chain_digest,
)
from r26e.live_product import LiveProduct

A = "TEST_ONLY_A"
B = "TEST_ONLY_B"


def entry(kind, name, time, who=A, owner=None,
          operation="coordinated_material_inspection", occurred=True):
    return seal_record(dict(
        kind=kind, ref="TEST_ONLY_" + name, time=time, subject=who,
        owner=owner or "TEST_ONLY_OWNER_" + name, grade=GRADE,
        operation=operation, occurred=occurred))


def n1_fixture():
    return dict(case_id="TEST_ONLY_N1_CASE", actor_id=A, other_actor_id=B,
                operation="coordinated_material_inspection", as_of=50,
                records=[
                    entry("ADP010_OPPORTUNITY", "opp", 1),
                    entry("ACTOR_ENACTED", "first", 2),
                    entry("ACTOR_ENACTED", "second", 4),
                    entry("ADP010_ENCOUNTER", "enc", 6),
                    entry("OTHER_OFFER", "offer", 7, B),
                    entry("ADP019_E1", "e1", 9),
                ])


def test_c12_valid_populated_episode_verifies_and_cold_reopens(tmp_path, artifacts):
    p = LiveProduct(tmp_path / "p", artifacts=artifacts)
    try:
        p.say("a real episode")
        report = p.c12_verify()
        assert report["ok"] is True, report
        assert report["counts"]["episode"] == 1
        row = p.store.db.execute(
            "SELECT body,hash FROM episode WHERE branch_id='root'").fetchone()
        body = json.loads(row[0])
        from bp1.canon import digest
        assert digest({k: v for k, v in body.items()
                        if k not in ("hash", "episode_id")}) == body["hash"]
        assert body["hash"] == row[1]
        assert C12Store(p.store.path).verify("root")["ok"] is False  # upstream defect
        path = p.store.path
    finally:
        p.close()
    q = QualifiedC12Store(path)
    try:
        cold = q.verify("root")
        assert cold["ok"] is True, cold
        assert cold["counts"]["episode"] == 1
    finally:
        q.close()


def test_c12_all_row_types_after_lifecycle_and_chain_digest(tmp_path, artifacts):
    p = LiveProduct(tmp_path / "p", artifacts=artifacts)
    try:
        p.say("hello")
        p.wait(30)
        p.travel("market")
        p.attend()
        report = p.c12_verify()
        assert report["ok"] is True, report
        assert report["counts"]["episode"] >= 1
        assert report["counts"]["world_event"] >= 2
        assert report["counts"]["checkpoint"] >= 2
        d1 = chain_digest(p.store, "root")
        p.say("second episode")
        d2 = chain_digest(p.store, "root")
        assert d1 != d2
        assert p.c12_verify()["ok"] is True
    finally:
        p.close()


def test_n1_screen_alternatives_never_create_durable_state(tmp_path, artifacts):
    p = LiveProduct(tmp_path / "p", artifacts=artifacts)
    try:
        before = p.store.latest_state("root")
        before_targets = p.store.db.execute(
            "SELECT count(*) FROM target_state").fetchone()[0] if False else None
        before_projects = p.observe()["self"]["state"]["projects"]
        cases = {
            "positive": n1_fixture(),
            "no_e1": {**n1_fixture(), "records": [
                r for r in n1_fixture()["records"] if r["kind"] != "ADP019_E1"]},
            "no_enacted": {**n1_fixture(), "records": [
                r for r in n1_fixture()["records"] if r["kind"] != "ACTOR_ENACTED"]},
            "contrary": {**n1_fixture(), "records": n1_fixture()["records"] + [
                entry("CONTRARY_ACTION", "contrary", 8)]},
            "self_report": {**n1_fixture(), "records": [
                r for r in n1_fixture()["records"] if r["kind"] != "ACTOR_ENACTED"] + [
                entry("ACTOR_SELF_REPORT", "speech", 3)]},
            "same_actor": {**n1_fixture(), "other_actor_id": A},
        }
        statuses = {name: p.n1_screen(case)["status"] for name, case in cases.items()}
        assert statuses["positive"] == "OWNER_REVIEW_CANDIDATE"
        assert statuses["no_e1"] == "REQUEST_EVIDENCE"
        assert statuses["no_enacted"] == "NO_CHANGE"
        assert statuses["contrary"] == "COMPETING"
        assert statuses["self_report"] == "NO_CHANGE"
        assert statuses["same_actor"] == "DENY"
        compiled = p.n1_compile(cases["positive"], now=50)
        assert compiled["status"] == "TEST_ONLY_PORTS_BOUND_NOT_ISSUED"
        assert compiled["grant"] is None
        assert compiled["rule_a"].test_only and compiled["rule_t"].test_only
        assert compiled["native_registry_mutation"] is False
        assert compiled["downstream_state_change"] is False
        assert p.production_registries()["response_rule_count"] == 0
        assert p.production_registries()["target_rule_count"] == 0
        after = p.store.latest_state("root")
        assert after == before
        assert p.observe()["self"]["state"]["projects"] == before_projects
    finally:
        p.close()


def test_n1_ineligible_case_compiles_no_rule_or_target(tmp_path, artifacts):
    p = LiveProduct(tmp_path / "p", artifacts=artifacts)
    try:
        before = p.store.latest_state("root")
        case = {**n1_fixture(), "records": [
            r for r in n1_fixture()["records"] if r["kind"] != "ADP019_E1"]}
        result = p.n1_compile(case, now=50)
        assert result["status"] == "REQUEST_EVIDENCE"
        assert result["rule_a"] is None and result["rule_t"] is None
        assert result["grant"] is None
        assert p.store.latest_state("root") == before
    finally:
        p.close()


def test_n1_method_screen_removal_leaves_product_target_untouched(tmp_path, artifacts):
    p = LiveProduct(tmp_path / "p", artifacts=artifacts)
    try:
        target_before = p.observe()["c9"]["target_id"]
        projects_before = p.observe()["self"]["state"]["projects"]
        case = {**n1_fixture(), "records": [
            r for r in n1_fixture()["records"] if r["kind"] != "ACTOR_ENACTED"]}
        assert p.n1_screen(case)["status"] == "NO_CHANGE"
        assert p.n1_compile(case, now=50)["grant"] is None
        assert p.observe()["c9"]["target_id"] == target_before
        assert p.observe()["self"]["state"]["projects"] == projects_before
        assert p.c12_verify()["ok"] is True
    finally:
        p.close()


def test_raw_sqlite_delete_and_test_only_external_witness(tmp_path, artifacts):
    p = LiveProduct(tmp_path / "p", artifacts=artifacts)
    try:
        p.say("episode to delete")
        witness = ExternalCheckpointWitness(tmp_path / "anchor" / "w.json", b"k" * 32)
        witness.record(p.store, "root")
        db = p.store.path
        before = chain_digest(p.store, "root")
    finally:
        p.close()
    with sqlite3.connect(db) as conn:
        conn.execute("DROP TRIGGER IF EXISTS episode_no_delete")
        deleted = conn.execute("DELETE FROM episode WHERE branch_id='root'").rowcount
        conn.commit()
    store = QualifiedC12Store(db)
    try:
        remaining = store.verify("root")
        assert remaining["ok"] is True
        assert remaining["counts"]["episode"] == 0
        check = witness.check(store, "root")
        assert check["ok"] is False and check["code"] == "CHAIN_DIGEST_MISMATCH"
        assert check["security_boundary"] is False
        after = chain_digest(store, "root")
        assert before != after
        # Same-trust-domain attacker can rewrite the witness; no KMS claim.
        witness.record(store, "root")
        forged = witness.check(store, "root")
        assert forged["ok"] is True
        assert witness.residual()["code"] == TRUST_CUSTODY_HOLD
        assert witness.residual()["production_kms_claim"] is False
        assert witness.trust_grade == EXTERNAL_WITNESS_GRADE
    finally:
        store.close()


def test_joined_assertion_and_live_product_agree(tmp_path, artifacts):
    receipt = joined_downstream_a0_a2_assertion(tmp_path / "assertion", artifacts)
    assert receipt["assertion"] == "bp2p4.assertion.joined_downstream_a0_a2_assertion"
    assert receipt["status"] == "PASS"
    assert receipt["target_id"] == artifacts.target_id
    p = LiveProduct(tmp_path / "live", artifacts=artifacts)
    try:
        observed = p.observe_verified()
        assert observed["status"] == "OK"
        assert observed["c9"]["target_id"] == artifacts.target_id
        assert observed["c12_verify"]["ok"] is True
        p.wait(30)
        p.travel("market")
        p.attend()
        after = p.observe_verified()
        assert after["status"] == "OK"
        assert any(c["kind"] == "OFFSCREEN_REPAIR" for c in after["claims"])
        assert p.c12_verify()["ok"] is True
    finally:
        p.close()


def test_author_seven_primary_and_three_supplementary_faults(tmp_path, artifacts):
    trials = run_all_severances(tmp_path / "severance", artifacts)
    receipt = severance_receipt(trials)
    assert receipt["edge_count"] == 7
    assert receipt["supplementary_count"] == 3
    assert receipt["all_primary_proved"] is True
    assert receipt["all_supplementary_proved"] is True
    assert all("JOINED" in t.assertion or "bp2p4.assertion" in t.assertion
               for t in trials)
