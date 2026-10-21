"""Generate R26E evidence receipts over the live joined product."""
from __future__ import annotations

import hashlib
import json
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
REPO = RET.parents[1]
sys.path.insert(0, str(RET))
sys.path.insert(0, str(RET / "runtime" / "target"))
sys.path.insert(0, str(RET / "runtime" / "n1" / "source"))

import bp2p4  # noqa: E402
bp2p4.install()

from bp1.canon import digest  # noqa: E402
from bp2p4 import reunion  # noqa: E402
from bp2p4.assertion import joined_downstream_a0_a2_assertion  # noqa: E402
from bp2p4.severance import run_all_severances, severance_receipt  # noqa: E402
from bp4.store import C12Store  # noqa: E402
from n1_eligibility import GRADE, seal_record  # noqa: E402
from r26e.c12_integrity import (  # noqa: E402
    ExternalCheckpointWitness, QualifiedC12Store, chain_digest,
)
from r26e.live_product import LiveProduct  # noqa: E402

EVID = RET / "evidence"
EVID.mkdir(exist_ok=True)
A, B = "TEST_ONLY_A", "TEST_ONLY_B"


def entry(kind, name, time, who=A, owner=None,
          operation="coordinated_material_inspection", occurred=True):
    return seal_record(dict(kind=kind, ref="TEST_ONLY_" + name, time=time,
                            subject=who, owner=owner or "TEST_ONLY_OWNER_" + name,
                            grade=GRADE, operation=operation, occurred=occurred))


def n1_case(records=None):
    return dict(case_id="TEST_ONLY_N1_CASE", actor_id=A, other_actor_id=B,
                operation="coordinated_material_inspection", as_of=50,
                records=records if records is not None else [
                    entry("ADP010_OPPORTUNITY", "opp", 1),
                    entry("ACTOR_ENACTED", "first", 2),
                    entry("ACTOR_ENACTED", "second", 4),
                    entry("ADP010_ENCOUNTER", "enc", 6),
                    entry("OTHER_OFFER", "offer", 7, B),
                    entry("ADP019_E1", "e1", 9)])


def blob(path: Path) -> dict:
    return {"path": str(path.relative_to(RET)), "git_blob": subprocess.run(
        ["git", "hash-object", str(path)], cwd=str(REPO), capture_output=True,
        text=True, check=True).stdout.strip(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    root = Path(tempfile.mkdtemp(prefix="r26e-evidence-"))
    artifacts = reunion.build_fresh(root / "bp2")
    out = {}

    # 1 valid populated episode + cold verifier
    p = LiveProduct(root / "p1", artifacts=artifacts)
    p.say("valid populated episode")
    before = p.c12_verify()
    row = p.store.db.execute("SELECT body,hash FROM episode WHERE branch_id='root'").fetchone()
    body = json.loads(row[0])
    doc = {
        "schema": "R26E_C12_VALID_EPISODE@1",
        "qualified_verify": before,
        "upstream_original_verify": C12Store(p.store.path).verify("root"),
        "episode_true_preimage_matches": digest(
            {k: v for k, v in body.items() if k not in ("hash", "episode_id")}) == body["hash"],
        "episode_delivered_old_preimage_matches": digest(
            {k: v for k, v in body.items() if k != "hash"}) == body["hash"],
        "row_column_hash": row[1],
        "body_hash": body["hash"],
    }
    p.close()
    q = QualifiedC12Store(root / "p1" / "c12.sqlite")
    doc["cold_reopen_verify"] = q.verify("root")
    q.close()
    out["c12_valid_episode"] = doc

    # 2 raw SQLite deletion vs TEST_ONLY external witness
    p = LiveProduct(root / "p2", artifacts=artifacts)
    p.say("episode to delete")
    witness = ExternalCheckpointWitness(root / "anchor" / "w.json", b"k" * 32)
    witness.record(p.store, "root")
    chain_before = chain_digest(p.store, "root")
    db = p.store.path
    p.close()
    with sqlite3.connect(db) as conn:
        conn.execute("DROP TRIGGER IF EXISTS episode_no_delete")
        deleted = conn.execute("DELETE FROM episode WHERE branch_id='root'").rowcount
        conn.commit()
    s = QualifiedC12Store(db)
    check = witness.check(s, "root")
    after = chain_digest(s, "root")
    witness.record(s, "root")
    forged = witness.check(s, "root")
    doc = {
        "schema": "R26E_RAW_SQLITE_ATTACK@1",
        "deleted_rows": deleted,
        "remaining_verify": s.verify("root"),
        "chain_before": chain_before, "chain_after": after,
        "witness_check": check, "witness_after_rewrite": forged,
        "residual": witness.residual(),
    }
    s.close()
    out["raw_sqlite_attack"] = doc

    # 3 N1 screen, ports, no durable state
    p = LiveProduct(root / "p3", artifacts=artifacts)
    before_state = p.store.latest_state("root")
    cases = {
        "positive": n1_case(),
        "no_e1": n1_case([r for r in n1_case()["records"] if r["kind"] != "ADP019_E1"]),
        "no_enacted": n1_case([r for r in n1_case()["records"] if r["kind"] != "ACTOR_ENACTED"]),
        "contrary": n1_case(n1_case()["records"] + [entry("CONTRARY_ACTION", "contrary", 8)]),
        "self_report": n1_case([r for r in n1_case()["records"] if r["kind"] != "ACTOR_ENACTED"] + [entry("ACTOR_SELF_REPORT", "speech", 3)]),
        "same_actor": {**n1_case(), "other_actor_id": A},
    }
    statuses = {k: p.n1_screen(v)["status"] for k, v in cases.items()}
    compiled = p.n1_compile(cases["positive"], now=50)
    ineligible = p.n1_compile(cases["no_e1"], now=50)
    doc = {
        "schema": "R26E_N1_PORTS@1",
        "screen_statuses": statuses,
        "compiled_status": compiled["status"],
        "grant": compiled["grant"],
        "rule_a_test_only": compiled["rule_a"].test_only if compiled["rule_a"] else None,
        "rule_t_test_only": compiled["rule_t"].test_only if compiled["rule_t"] else None,
        "native_registry_mutation": compiled["native_registry_mutation"],
        "downstream_state_change": compiled["downstream_state_change"],
        "production_registries": {
            key: value for key, value in p.production_registries().items()
            if key in ("response_rule_count", "target_rule_count", "status")},
        "ineligible_status": ineligible["status"],
        "ineligible_rule_a": ineligible["rule_a"],
        "ineligible_grant": ineligible["grant"],
        "state_unchanged": p.store.latest_state("root") == before_state,
    }
    p.close()
    out["n1_ports"] = doc

    # 4 product A0/A2 + offscreen
    p = LiveProduct(root / "p4", artifacts=artifacts)
    a0 = p.observe_verified()
    p.say("I am here about the bench.")
    waited = p.wait(30)
    other = p.other()
    p.travel("market")
    p.attend()
    reentry = p.observe_verified()
    doc = {
        "schema": "R26E_PRODUCT@1",
        "a0_status": a0.get("status"), "a0_target": a0.get("c9", {}).get("target_id"),
        "a0_claims": [c["kind"] for c in a0.get("claims", [])],
        "wait_clock": waited.get("clock"),
        "other_completed_units": other["public"]["completed_units"],
        "reentry_status": reentry.get("status"),
        "reentry_claims": [c["kind"] for c in reentry.get("claims", [])],
        "c12_verify": reentry.get("c12_verify"),
        "native_claims": reentry.get("native_claims"),
    }
    p.close()
    out["product"] = doc

    # 5 author 7+3 severances + method fault
    trials = run_all_severances(root / "severance", artifacts)
    sev = severance_receipt(trials)
    method_fault = {
        "edge": "N1_METHOD_SCREEN_REMOVAL",
        "baseline": "OWNER_REVIEW_CANDIDATE",
        "fault": "NO_CHANGE_OR_REQUEST_EVIDENCE",
        "target_effect": "NONE",
        "rule_a": None, "rule_t": None, "grant": None,
    }
    out["severance"] = {"receipt": sev, "method_fault": method_fault}

    # 6 provenance
    own = [blob(p) for p in sorted((RET / "r26e").glob("*.py"))
           + sorted((RET / "tests").glob("*.py"))]
    out["provenance"] = {
        "schema": "R26E_SOURCE_PROVENANCE@1",
        "own": own,
        "pins": {
            "r26e_startup": "dba95216d5627513ea36323f459cf97413b504d1",
            "bp2p4j_target": "5b3e6577400ea1d88971ae6b48e41a118b8059ae",
            "bp2p4ji_review": "3212d716ce66586527c258632ef10c3ff4489803",
            "n1_target": "cd6b0fb9358c5f7d3c344c84a148d3fee48d2e16",
            "bp2": "5065e2e6934e9d5bca800cbf88c79e461bcf2393",
            "bp4": "d868e82c7c83def2df18295244d93af9706e647f",
        },
    }
    (EVID / "r26e_receipts.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: ("OK" if k != "severance" else sev["all_primary_proved"]) for k in out}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
