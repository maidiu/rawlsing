import argparse
import hashlib
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import c9_actor_r3 as c9

S36_ROOT = Path(
    "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/"
    "syn02-s36-r2-wt/WORKER_RETURNS/"
    "SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1"
)
JOIN_E = Path(
    "/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/"
    "SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/j"
)


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def s36_probe(work):
    sys.path.insert(0, str(S36_ROOT))
    sys.path.insert(0, str(S36_ROOT / "runtime" / "native"))
    from candidate.canon import digest
    from candidate.transaction import CandidateStore
    from s36_harness import run_s35_case

    store = CandidateStore(work / "s36-targetless.db")
    legacy, _ = run_s35_case(store)
    assert legacy.committed and legacy.receipt.committed
    before_readset = store._logical_readset()
    before_hash = digest(before_readset)
    tables = sorted(before_readset["tables"])

    actor = c9.ActorAuthority(work / "actor-s36.db", actor_id="S36-ISOLATION")
    actor.add_world_receipt(
        world_receipt_hash="world-s36",
        world_event_id="event-s36",
        c8_branch_id="c8-s36",
        c8_root_hash="c8-root-s36",
        c8_head_hash="c8-head-s36",
        effective_us=1,
    )
    actor.add_rule(
        rule_hash="T-S36",
        rule_kind="T",
        issuer_ref="sourcefree-test",
        source_cut_hash=actor.source_cut_hash,
    )
    actor.publish(
        c9.PublishRequest(
            event_key="s36-event",
            idempotency_key="s36-key",
            decision_kind="COMMITTED_CHANGE",
            source_cut_hash=actor.source_cut_hash,
            source_scope_hash="s36-source-scope",
            settled_scope_hash="s36-settled-scope",
            world_receipt_hash="world-s36",
            rule_t_hash="T-S36",
            rule_t_status="COMMITTED_CHANGE",
            evaluation_basis="ISSUED_RULE_T_EVALUATED",
            evaluated_readset_hash="s36-readset",
            semantic_payload={"s36": True},
        )
    )
    after_hash = digest(store._logical_readset())
    old_receipt = {
        "receipt_hash": legacy.receipt.receipt_hash,
        "before_hash": legacy.receipt.before_hash,
        "after_hash": legacy.receipt.after_hash,
        "target_branch": legacy.receipt.target_branch,
        "target_reason": legacy.receipt.target_reason,
        "committed": legacy.receipt.committed,
    }
    store.close()
    return {
        "source": str(S36_ROOT),
        "source_sha256": file_hash(S36_ROOT / "candidate" / "transaction.py"),
        "tables": tables,
        "old_receipt": old_receipt,
        "before_readset_hash": before_hash,
        "after_readset_hash": after_hash,
        "unchanged": before_hash == after_hash,
        "table_count": len(tables),
    }


def c12_imports():
    sys.path.insert(0, str(JOIN_E))
    sys.path.insert(0, str(JOIN_E / "candidate" / "vendor" / "bp4"))
    sys.path.insert(0, str(JOIN_E / "candidate" / "vendor" / "bp4" / "vendor" / "bp1"))
    from bp4.canon import seal
    from bp4.store import C12Store, GRADE
    from r26e.c12_integrity import QualifiedC12Store

    return seal, C12Store, GRADE, QualifiedC12Store


def c12_probe(work):
    seal, C12Store, GRADE, QualifiedC12Store = c12_imports()
    path = work / "c12-defect.db"
    store = QualifiedC12Store(path)
    store.create_root("root", clock=10, actor_ids=["A"], state={"world": 1})
    event = seal(
        {
            "schema": "BP4_C12_WORLD_EVENT@1",
            "branch_id": "root",
            "event_id": "ev1",
            "clock": 10,
            "body": {},
            "grade": GRADE,
            "native": False,
        }
    )
    store.append_world_event("root", event)
    store.record_perception("root", actor_id="A", event_id="ev1", clock=11, channel="test")
    verify = store.verify("root")
    last_clock = store.last_clock("root")
    parent_guard = c9.c12_fork_guard(path, "root")
    wrong_root = c9.c12_fork_guard(
        path, "root", expected_base_root_hash="wrong-root"
    )
    store.close()

    same_count_path = work / "c12-same-count.db"
    same = QualifiedC12Store(same_count_path)
    same.create_root("root", clock=10, actor_ids=["A"], state={"world": 1})
    first = seal(
        {
            "schema": "BP4_C12_WORLD_EVENT@1",
            "branch_id": "root",
            "event_id": "ev1",
            "clock": 10,
            "body": {},
            "grade": GRADE,
            "native": False,
        }
    )
    second = seal(
        {
            "schema": "BP4_C12_WORLD_EVENT@1",
            "branch_id": "root",
            "event_id": "ev2",
            "clock": 10,
            "body": {},
            "grade": GRADE,
            "native": False,
        }
    )
    same.append_world_event("root", first)
    same.append_world_event("root", second)
    same.record_perception("root", actor_id="A", event_id="ev1", clock=10, channel="test")
    same.record_perception("root", actor_id="A", event_id="ev2", clock=11, channel="test")
    parent = c9.c12_fork_guard(same_count_path, "root")
    same.fork("root", "child")
    third = seal(
        {
            "schema": "BP4_C12_WORLD_EVENT@1",
            "branch_id": "child",
            "event_id": "ev3",
            "clock": 10,
            "body": {},
            "grade": GRADE,
            "native": False,
        }
    )
    same.append_world_event("child", third)
    same.record_perception("child", actor_id="A", event_id="ev3", clock=10, channel="test")
    same_count = {
        "parent_verify": same.verify("root"),
        "child_verify": same.verify("child"),
        "parent_perceptions": same.perceptions("root"),
        "child_perceptions": same.perceptions("child"),
        "parent_guard": parent,
        "child_guard": c9.c12_fork_guard(
            same_count_path,
            "child",
            expected_base_perception_hash=parent["base_perception_hash"],
        ),
    }
    same.close()
    return {
        "source": str(JOIN_E),
        "store_sha256": file_hash(JOIN_E / "candidate" / "vendor" / "bp4" / "bp4" / "store.py"),
        "verifier_sha256": file_hash(JOIN_E / "r26e" / "c12_integrity.py"),
        "parent_verify": verify,
        "parent_last_clock": last_clock,
        "parent_guard": parent_guard,
        "wrong_base_root_guard": wrong_root,
        "same_count": same_count,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as temporary:
        work = Path(temporary)
        evidence = {
            "schema_hashes": c9.schema_hashes(),
            "s36": s36_probe(work),
            "c12": c12_probe(work),
        }
    text = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        Path(args.json_out).write_text(text, encoding="utf8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
