"""Cold-process build/verify probe for the joined BP3 -> BP1 -> C9R positive.

``build`` runs the whole joined chain in this process and writes the hot receipt.
``verify`` runs in a separate process: it re-verifies the staged source closure,
the BP3 keyed journal proof and external anchor, the OUT9 read, the durable
SQLite target record and the later performed E2 admission against the exact
consumed state hash.

Usage:
    python3 tools/cold_probe.py build  <root> <receipt.json>
    python3 tools/cold_probe.py verify <root> <receipt.json>
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

os.environ.setdefault("PYTHONHASHSEED", "0")
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")

import bp2_joined  # noqa: E402
from bp2_joined.producer import (  # noqa: E402
    EXPECTED_ACT,
    JoinedProducer,
    joined_consumer_assertion,
    prepare_journal_env,
)


def _write_json(value, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, default=str) + "\n",
                    encoding="utf8")


def build(root: Path, receipt_path: Path) -> dict:
    manifest = bp2_joined.verify_sources()
    with JoinedProducer(root) as producer:
        outcome = producer.run()
        joined_consumer_assertion(outcome)
        receipt = outcome.receipt()
        document = {
            "schema": "BP2_JOINED_COLD_BUILD@1",
            "root": str(root),
            "manifest_file_count": manifest["file_count"],
            "manifest_sha256": _hash_file(bp2_joined.bootstrap.MANIFEST),
            "receipt": receipt,
            "persisted": receipt["persisted"],
        }
    _write_json(document, receipt_path)
    return {
        "status": "BUILT",
        "receipt_path": str(receipt_path),
        "ok": True,
        "c8_occurrence_id": document["persisted"]["c8_occurrence_id"],
        "target_record_hash": document["persisted"]["target_record_hash"],
        "consumed_state_hash": document["persisted"]["consumed_state_hash"],
    }


def _hash_file(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root: Path, receipt_path: Path) -> dict:
    from candidate import admit_performed_action

    document = json.loads(Path(receipt_path).read_text(encoding="utf8"))
    persisted = document["persisted"]
    manifest = bp2_joined.verify_sources()

    env = prepare_journal_env(Path(root))
    proof = env.journal.verify_journal()
    journal_verified = bool(proof.get("schema"))

    from c8_readonly_consumer import C8ReadOnlyConsumer
    from c9_event_ingress import receive_event

    ingress = receive_event(
        env.journal_path,
        expected_state_digest=persisted["c8_state_digest"],
        proof_verifier=env.journal.verify_journal,
    )
    view = C8ReadOnlyConsumer(env.journal_path).load()
    readset = view.readset.to_json()
    occurrence = view.get(persisted["c8_occurrence_id"])
    out9_equal = (
        readset["state_digest"] == persisted["c8_state_digest"]
        and list(readset["occurrence_ids"]) == [persisted["c8_occurrence_id"]]
        and readset["commit_receipt_id"] == persisted["c8_commit_receipt_id"]
        and readset["writer_version"] == persisted["c8_writer_version"]
        and readset["canonical_bytes_sha256"] == persisted["c8_canonical_bytes_sha256"]
        and occurrence is not None
        and occurrence.get("content_hash") == persisted.get("c8_content_hash",
                                                           occurrence.get("content_hash"))
    )

    from bp1.canon import digest
    from candidate import CandidateStore

    store = CandidateStore(Path(root) / "c9.sqlite")
    try:
        record = store.read_target_state(persisted["target_id"])
        target_record_equal = (
            record is not None
            and digest(dict(record)) == persisted["consumed_state_hash"]
            and record.get("record_hash") == persisted["target_record_hash"]
            and record.get("creation_rule_ref") == persisted["rule_t_dependency_hash"]
            and record.get("actor_id") == persisted["actor_id"]
            and record.get("response_hash") == persisted["response_hash"]
            and record.get("record_preimage", {}).get("causal_parent_refs", [""])[0]
            == persisted["e1_event_hash"]
        )
        journal_row = store.db.execute(
            "SELECT body FROM target_journal WHERE id=?",
            (persisted["target_record_hash"],),
        ).fetchone()
        target_journal_present = journal_row is not None
        receipt_rows = store.db.execute("SELECT body FROM receipt").fetchall()
        receipt_present = any(
            json.loads(row[0]).get("target_id") == persisted["target_id"]
            for row in receipt_rows
        )
        admission = admit_performed_action(
            owner_receipt=persisted["e2_owner_receipt"],
            expected_actor_id=persisted["actor_id"],
            expected_act=persisted["expected_act"],
            consumed_state_hash=persisted["consumed_state_hash"],
            as_of=persisted["later_as_of"],
            target_commit_time=persisted["event_time"],
        )
    finally:
        store.close()

    result = {
        "schema": "BP2_JOINED_COLD_VERIFY@1",
        "status": "VERIFIED" if all((
            journal_verified, out9_equal, target_record_equal,
            target_journal_present, receipt_present, admission.admitted,
        )) else "FAILED",
        "manifest_file_count": manifest["file_count"],
        "manifest_sha256": _hash_file(bp2_joined.bootstrap.MANIFEST),
        "journal_proof_verified": journal_verified,
        "journal_id": env.journal.journal_id,
        "out9_read_equal": out9_equal,
        "out9_state_digest": readset["state_digest"],
        "out9_occurrence_ids": list(readset["occurrence_ids"]),
        "target_record_equal": target_record_equal,
        "target_journal_present": target_journal_present,
        "commit_receipt_present": receipt_present,
        "e2_readmitted": bool(admission.admitted),
        "e2_reason": getattr(admission.reason, "value", str(admission.reason)),
        "e2_consumed_state_hash": getattr(admission, "consumed_state_hash", ""),
        "c8_occurrence_id": persisted["c8_occurrence_id"],
        "c8_state_digest": persisted["c8_state_digest"],
        "c8_commit_receipt_id": persisted["c8_commit_receipt_id"],
        "c8_canonical_bytes_sha256": persisted["c8_canonical_bytes_sha256"],
        "target_record_hash": persisted["target_record_hash"],
        "consumed_state_hash": persisted["consumed_state_hash"],
        "rule_a_content_hash": persisted["rule_a_content_hash"],
        "rule_t_content_hash": persisted["rule_t_content_hash"],
        "rule_t_dependency_hash": persisted["rule_t_dependency_hash"],
        "grant_hash": persisted["grant_hash"],
        "response_hash": persisted["response_hash"],
        "e2_receipt_hash": persisted["e2_receipt_hash"],
        "e1_event_id": persisted["e1_event_id"],
        "e1_event_hash": persisted["e1_event_hash"],
        "target_record_parent": record.get("record_preimage", {}).get(
            "causal_parent_refs", [""])[0] if record else "",
        "adp019_admission_receipt": ingress["adp019_admission_receipt"],
        "e2_performed_by_c8": ingress["e2_performed"],
        "native_actor_admitted": ingress["native_actor_admitted"],
    }
    return result


def main(argv: list[str]) -> int:
    if len(argv) != 4 or argv[1] not in {"build", "verify"}:
        print(__doc__)
        return 2
    root, receipt = Path(argv[2]), Path(argv[3])
    if argv[1] == "build":
        result = build(root, receipt)
        print(json.dumps(result, sort_keys=True, default=str))
        return 0
    result = verify(root, receipt)
    print(json.dumps(result, sort_keys=True, default=str))
    return 0 if result["status"] == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
