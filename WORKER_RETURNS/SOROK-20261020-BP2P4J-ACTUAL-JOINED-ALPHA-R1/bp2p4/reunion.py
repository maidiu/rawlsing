"""Produce or recover the ACTUAL BP2 joined artifacts consumed by BP4.

Two lawful modes:

``FRESH``
    Run BP2's real ``bp2_joined.producer.JoinedProducer`` in this return's own
    runtime root. The C8 keyed journal, external anchor, C9 SQLite store and the
    independently performed E2 receipt are all produced by BP2 code, not by this
    adapter. The BP2 named downstream assertion is executed on the result.

``ORIGIN_LITERAL``
    Consume the exact surviving BP2 evidence runtime when it is present on this
    machine (the run that produced target ``950a4c79…`` / consumed ``4907a662…``).
    That runtime contains a random TEST_ONLY key and a path-bound journal, so it
    is not reproducible from the committed return; this mode is therefore a
    local literal-origin cross-check, not a portable test dependency.

Every mode re-verifies the physical artifacts: journal keyed proof and external
anchor, OUT9 readset, the sealed target row and its digest, the CAN008 response
row, the separate CAN011 authorization row, the target commit receipt, the BP2
E1 occurrence binding and the performed E2 admission. A shape-valid statement is
never accepted in place of the artifacts.
"""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402
from bp1.composer import build_two_actor_life  # noqa: E402
from bp1.ledger import verify_snapshot  # noqa: E402
from candidate import CandidateStore, admit_performed_action  # noqa: E402

BP2_COMMIT = "5065e2e6934e9d5bca800cbf88c79e461bcf2393"
BP2_RETURN = "WORKER_RETURNS/SOROK-20261020-BP2-JOINED-ACTOR-EVENT-RULE-ACTION-R1"

# Path/key independent identities: these MUST reproduce exactly.
EXPECTED_INVARIANT = {
    "c8_occurrence_id": "OCC-0001",
    "c8_state_digest": "058d006c1ce79d2783b02a3bb4e2f92d0672aec9b406b5f3312453f9c5608b4b",
    "c8_content_hash": "8675e3aacd340d66ee977cb1fc6aa995799ed7a6d6fe277816b34ff3781776e2",
    "c8_identity_digest": "f4227419cbc64e6eb198b3802b044af7472a667e32d6013a0d70ac031dc37ef2",
    "c8_writer_version": 1,
    "actor_id": "TEST_ONLY_BP1_ACTOR_A",
    "other_actor_id": "TEST_ONLY_BP1_ACTOR_B",
    "actor_source_hash": "bf80ce4a1cddafa2eadab57fdda43942c70cca999bd49c864a34e9c1e33f82e2",
    "other_source_hash": "ba1266db1726ce17c426df62ec7e4a028b47ee09f7388b243e2ae47dc3ab0fcb",
    "actor_snapshot_hash": "6b65980d0fbb2ecc8dca657e0f6f12daf98a6d4789d2d35a0e129ed23de80bb6",
    "rule_a_content_hash": "aa5033ca2b5f6321203652bf32537618fefbde4836ada572404702bef1869574",
    "rule_t_content_hash": "457894cf45902c8a4db1077bb1d043feef1b9c7bba67ad1e231e19978d1da3cb",
    "event_time": 202,
}

# Derived from the committed target row and the performed E2 receipt, not from
# the persisted identity block.
EXPECTED_DERIVED = {
    "practice_label": "coordinated_material_inspection",
    "e2_act": "inspect_with_tool",
    "e2_actuator_ref": "TEST_ONLY_ACTUATOR_BP2_INDEPENDENT",
    "e2_occurrence_ref": "TEST_ONLY_OCCURRENCE_BP2_E2",
    "target_commit_time": 202,
    "e2_action_time": 217,
}

# Identities that bind the random TEST_ONLY key and the absolute journal path.
# They reproduce only at the exact origin path/key; recorded here for the
# origin-change reconciliation, never asserted against a fresh run.
LITERAL_ORIGIN = {
    "c8_commit_receipt_id": "95ac61ff1bbb8af04278d2e7ce321f56189e1f526f167b079de55c0194306e93",
    "e1_event_id": "TEST_ONLY_BP2_E1_OCC-0001",
    "e1_event_hash": "f043e3b3d264e93abb0a7abeafe971ca5d524bab2c6101b63af29649995f6197",
    "response_hash": "757eecb20ad793d556daa08e2cb31cf2a59406901dfe6de888da98d32990fda0",
    "grant_hash": "3236a56072294efecd81b7817b6b54ec4afa31be33ec5886ad8852a9172bd970",
    "target_id": "950a4c7903cbe832c72d234a0095946720910c23c8235a28c3118afd8fc1b9f8",
    "target_record_hash": "8d784d48096f4d32d0df3d7c659a23b501681877a948580e0c0150ac60efcd3e",
    "consumed_state_hash": "4907a662d2494d9f7949d1f809195264e001f90d39021feb73e5a75cc31c656d",
    "e2_receipt_hash": "19349fd6fded91f222d50ef5774deab1203619c390fb554e2bd4970e9c7f05aa",
    "c9_commit_receipt_hash": "b4d518ed47d32a01bc1d59156dfdce23275c0b6d149f4665f36cd311983de280",
    "c9_authorization_hash": "18c85828af145307f37430f05761693757419088cd191147cf143c26dbffa2b5",
}

DEFAULT_ORIGIN_RUNTIME = (
    "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/bp2/WORKER_RETURNS/"
    "SOROK-20261020-BP2-JOINED-ACTOR-EVENT-RULE-ACTION-R1/evidence/runtime/positive"
)


class ReunionRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


@dataclass
class BP2Artifacts:
    mode: str
    root: Path
    life: Any
    journal_path: Path
    key_path: Path
    key_id: str
    anchor_log: Path
    anchor_watermark: Path
    c9_path: Path
    occurrence_id: str
    c8_state_digest: str
    c8_content_hash: str
    c8_identity_digest: str
    c8_ledger_prefix_digest: str
    c8_writer_version: int
    c8_commit_receipt_id: str
    c8_canonical_bytes_sha256: str
    e1_event_id: str
    e1_event_hash: str
    target_id: str
    target_record_hash: str
    consumed_state_hash: str
    target: dict
    rule_a_hash: str
    rule_t_hash: str
    rule_t_dependency: str
    response_hash: str
    grant_hash: str
    e2_receipt: dict | None
    e2_receipt_hash: str
    event_time: int
    as_of: int
    later_as_of: int
    practice_label: str
    receipt: dict
    emission_order: tuple[str, ...] = ("BP2_C8_COMMIT", "BP2_C9_TARGET_COMMIT",
                                       "BP2_E2_ADMISSION")

    def public(self) -> dict:
        return {
            "schema": "BP2P4J_BP2_ARTIFACT_BINDING@1",
            "mode": self.mode,
            "root": str(self.root),
            "journal_path": str(self.journal_path),
            "key_path": str(self.key_path),
            "key_id": self.key_id,
            "anchor_log": str(self.anchor_log),
            "anchor_watermark": str(self.anchor_watermark),
            "c9_path": str(self.c9_path),
            "occurrence_id": self.occurrence_id,
            "c8_state_digest": self.c8_state_digest,
            "c8_content_hash": self.c8_content_hash,
            "c8_identity_digest": self.c8_identity_digest,
            "c8_ledger_prefix_digest": self.c8_ledger_prefix_digest,
            "c8_writer_version": self.c8_writer_version,
            "c8_commit_receipt_id": self.c8_commit_receipt_id,
            "c8_canonical_bytes_sha256": self.c8_canonical_bytes_sha256,
            "e1_event_id": self.e1_event_id,
            "e1_event_hash": self.e1_event_hash,
            "target_id": self.target_id,
            "target_record_hash": self.target_record_hash,
            "consumed_state_hash": self.consumed_state_hash,
            "c9_commit_receipt_hash": self.receipt.get("persisted", {}).get(
                "c9_commit_receipt_hash", ""),
            "c9_authorization_hash": self.receipt.get("persisted", {}).get(
                "c9_authorization_hash", ""),
            "rule_a_content_hash": self.rule_a_hash,
            "rule_t_content_hash": self.rule_t_hash,
            "rule_t_dependency_hash": self.rule_t_dependency,
            "response_hash": self.response_hash,
            "grant_hash": self.grant_hash,
            "e2_receipt_hash": self.e2_receipt_hash,
            "event_time": self.event_time,
            "as_of": self.as_of,
            "later_as_of": self.later_as_of,
            "practice_label": self.practice_label,
            "emission_order": list(self.emission_order),
            "native_grant": "NOT_GRANTED",
        }


# ---------------------------------------------------------------------------
# physical artifact verification (shared by every mode)
# ---------------------------------------------------------------------------
def _load_c8(journal_path, key_path, key_id, anchor_log, anchor_watermark,
             expected: dict) -> dict:
    import c8_exclusive_writer as bp3
    import c9_event_ingress as ingress

    store = bp3.WriterKeyStore.load(key_path, key_id)
    anchor = bp3.KeyedMonotonicAnchor(log_path=anchor_log,
                                      watermark_path=anchor_watermark,
                                      store=store)
    journal = bp3.ExclusiveJournal(journal_path, store=store, anchor=anchor)
    try:
        journal.verify_journal()
    except Exception as error:  # noqa: BLE001 - typed source refusal
        raise ReunionRefusal("BP2_C8_PROOF_INVALID", type(error).__name__ + ":" + str(error))
    try:
        read = ingress.receive_event(journal_path, proof_verifier=journal.verify_journal)
    except Exception as error:  # noqa: BLE001
        raise ReunionRefusal("BP2_C8_INGRESS_REFUSED", type(error).__name__ + ":" + str(error))
    if read["state_digest"] != expected["c8_state_digest"]:
        raise ReunionRefusal("BP2_C8_STATE_DIGEST_MISMATCH", read["state_digest"])
    if list(read["occurrence_ids"]) != [expected["c8_occurrence_id"]]:
        raise ReunionRefusal("BP2_C8_OCCURRENCE_SET_MISMATCH", str(read["occurrence_ids"]))
    if read["writer_version"] != expected["c8_writer_version"]:
        raise ReunionRefusal("BP2_C8_WRITER_VERSION_MISMATCH", str(read["writer_version"]))
    from c8_readonly_consumer import C8ReadOnlyConsumer

    view = C8ReadOnlyConsumer(journal_path).load()
    event = view.get(expected["c8_occurrence_id"])
    if event is None:
        raise ReunionRefusal("BP2_C8_OCCURRENCE_ABSENT")
    if event.get("content_hash") != expected["c8_content_hash"]:
        raise ReunionRefusal("BP2_C8_CONTENT_HASH_MISMATCH")
    identity = event.get("identity_preimage") or {}
    if event.get("identity_digest") != digest(dict(identity)):
        raise ReunionRefusal("BP2_C8_IDENTITY_DIGEST_INVALID")
    if event.get("identity_digest") != expected["c8_identity_digest"]:
        raise ReunionRefusal("BP2_C8_IDENTITY_DIGEST_MISMATCH")
    if read["commit_receipt_id"] != expected.get("c8_commit_receipt_id",
                                                 read["commit_receipt_id"]):
        raise ReunionRefusal("BP2_C8_COMMIT_RECEIPT_MISMATCH")
    return {"ingress": read, "event": event, "readset": view.readset.to_json(),
            "journal_id": journal.journal_id}


def _verify_c9_rows(c9_path: Path, expected: dict) -> dict:
    with CandidateStore(c9_path) as store:
        target = store.read_target_state(expected["target_id"])
        if target is None:
            raise ReunionRefusal("BP2_C9_TARGET_ABSENT", expected["target_id"])
        if digest(dict(target)) != expected["consumed_state_hash"]:
            raise ReunionRefusal("BP2_C9_CONSUMED_HASH_MISMATCH")
        preimage = target.get("record_preimage")
        if not isinstance(preimage, dict):
            raise ReunionRefusal("BP2_C9_TARGET_PREIMAGE_MISSING")
        if preimage.get("hash") != target.get("record_hash"):
            raise ReunionRefusal("BP2_C9_PREIMAGE_HASH_MISMATCH")
        if digest({k: v for k, v in preimage.items() if k != "hash"}) != target.get("record_hash"):
            raise ReunionRefusal("BP2_C9_PREIMAGE_DIGEST_MISMATCH")
        if target.get("record_hash") != expected["target_record_hash"]:
            raise ReunionRefusal("BP2_C9_TARGET_RECORD_HASH_MISMATCH")
        if target.get("actor_id") != expected["actor_id"]:
            raise ReunionRefusal("BP2_C9_TARGET_ACTOR_MISMATCH", str(target.get("actor_id")))
        if target.get("state_kind_id") != "V3MS_PRACTICE":
            raise ReunionRefusal("BP2_C9_TARGET_STATE_KIND_MISMATCH")
        if target.get("semantic_object_ref") != "c9p:coordinated_material_inspection":
            raise ReunionRefusal("BP2_C9_TARGET_SEMANTIC_OBJECT_MISMATCH")
        if target.get("creation_rule_ref") != expected["rule_a_content_hash"]:
            raise ReunionRefusal("BP2_RULE_A_BINDING_MISMATCH")
        if target.get("permission_ref") != "TEST_ONLY_BP2_TARGET_GRANT":
            raise ReunionRefusal("BP2_RULE_T_GRANT_REF_MISMATCH")
        payload = preimage.get("governed_payload") or {}
        if payload.get("practice_label") != EXPECTED_DERIVED["practice_label"]:
            raise ReunionRefusal("BP2_PRACTICE_LABEL_MISMATCH",
                                 str(payload.get("practice_label")))
        parents = preimage.get("causal_parent_refs") or []
        if expected.get("e1_event_hash") and parents[:1] != [expected["e1_event_hash"]]:
            raise ReunionRefusal("BP2_E1_CAUSAL_PARENT_MISMATCH")
        response = _find_response(store, target)
        if response is None:
            raise ReunionRefusal("BP2_RULE_A_RESPONSE_ABSENT", expected["response_hash"])
        if response.get("status") != "RESPONSE_COMMITTED":
            raise ReunionRefusal("BP2_RULE_A_RESPONSE_NOT_COMMITTED", str(response.get("status")))
        if response.get("rule_content_hash") != expected["rule_a_content_hash"]:
            raise ReunionRefusal("BP2_RULE_A_RESPONSE_RULE_MISMATCH")
        if parents and response.get("event_ref") != parents[0]:
            raise ReunionRefusal("BP2_RULE_A_RESPONSE_EVENT_MISMATCH")
        journal_row = _find_target_journal(store, target)
        if journal_row is None:
            raise ReunionRefusal("BP2_RULE_T_AUTHORIZATION_ABSENT", expected["target_record_hash"])
        if journal_row.get("authorization_hash") != expected["c9_authorization_hash"]:
            raise ReunionRefusal("BP2_RULE_T_AUTHORIZATION_MISMATCH")
        if journal_row.get("branch") != "CREATE":
            raise ReunionRefusal("BP2_RULE_T_BRANCH_MISMATCH")
        if journal_row.get("permission_ref") != target.get("permission_ref"):
            raise ReunionRefusal("BP2_RULE_T_PERMISSION_MISMATCH")
        commit_receipt = _find_commit_receipt(store, target)
        if commit_receipt is None:
            raise ReunionRefusal("BP2_COMMIT_RECEIPT_ABSENT")
        if commit_receipt.get("record_hash") != target.get("record_hash"):
            raise ReunionRefusal("BP2_COMMIT_RECEIPT_RECORD_MISMATCH")
        if commit_receipt.get("authorization_hash") != expected["c9_authorization_hash"]:
            raise ReunionRefusal("BP2_COMMIT_RECEIPT_AUTH_MISMATCH")
        if commit_receipt.get("target_branch") != "CREATE":
            raise ReunionRefusal("BP2_COMMIT_BRANCH_MISMATCH")
        occurrence = _find_occurrence(store, expected.get("e1_event_hash", ""))
        if occurrence is None:
            raise ReunionRefusal("BP2_E1_OCCURRENCE_ROW_ABSENT")
    return {
        "target": dict(target),
        "response": dict(response),
        "target_journal": dict(journal_row),
        "commit_receipt": dict(commit_receipt),
        "occurrence": dict(occurrence),
    }


def _find_response(store: CandidateStore, target: dict) -> dict | None:
    wanted = target.get("response_hash")
    for (body,) in store.db.execute("SELECT body FROM response"):
        record = json.loads(body)
        if record.get("receipt_hash") == wanted:
            return record
    return None


def _find_target_journal(store: CandidateStore, target: dict) -> dict | None:
    row = store.db.execute("SELECT body FROM target_journal WHERE id=?",
                           (target.get("record_hash"),)).fetchone()
    return json.loads(row[0]) if row else None


def _find_commit_receipt(store: CandidateStore, target: dict) -> dict | None:
    for body in store.db.execute("SELECT body FROM receipt"):
        record = json.loads(body[0])
        if record.get("target_id") == target.get("middle_state_id"):
            return record
    return None


def _find_occurrence(store: CandidateStore, event_hash: str) -> dict | None:
    if not event_hash:
        return None
    row = store.db.execute("SELECT body FROM occurrence WHERE hash=?",
                           (event_hash,)).fetchone()
    return json.loads(row[0]) if row else None


def _verify_e2(receipt: dict | None, *, expected: dict, target: dict) -> dict | None:
    if receipt is None:
        return None
    if not isinstance(receipt, dict):
        raise ReunionRefusal("BP2_E2_RECEIPT_NOT_OBJECT")
    if receipt.get("actor_id") != expected["actor_id"]:
        raise ReunionRefusal("BP2_E2_ACTOR_MISMATCH")
    if receipt.get("act") != expected["e2_act"]:
        raise ReunionRefusal("BP2_E2_ACT_MISMATCH")
    if receipt.get("actuator_ref") == expected["actor_id"]:
        raise ReunionRefusal("BP2_E2_SELF_PERFORMED")
    if receipt.get("occurrence_ref") == expected["actor_id"]:
        raise ReunionRefusal("BP2_E2_OCCURRENCE_NOT_INDEPENDENT")
    admission = admit_performed_action(
        owner_receipt=receipt,
        expected_actor_id=expected["actor_id"],
        expected_act=expected["e2_act"],
        consumed_state_hash=digest(dict(target)),
        as_of=int(receipt.get("action_time", -1)),
        target_commit_time=int(receipt.get("target_commit_time", -1)),
    )
    if not getattr(admission, "admitted", False):
        raise ReunionRefusal("BP2_E2_NOT_ADMITTED",
                             getattr(getattr(admission, "reason", None), "value", str(admission)))
    return {
        "admitted": True,
        "act": admission.act,
        "actuator_ref": admission.actuator_ref,
        "occurrence_ref": admission.occurrence_ref,
        "consumed_state_hash": admission.consumed_state_hash,
        "action_time": admission.action_time,
        "target_commit_time": admission.target_commit_time,
        "receipt_hash": admission.receipt_hash,
    }


def _assert_invariants(persisted: dict, *, mode: str) -> dict:
    mismatches = []
    for key, value in EXPECTED_INVARIANT.items():
        actual = persisted.get(key)
        if actual != value:
            mismatches.append({"field": key, "expected": value, "actual": actual})
    if mismatches:
        raise ReunionRefusal("BP2_ORIGIN_INVARIANT_MISMATCH", json.dumps(mismatches[:4]))
    return {"mode": mode, "checked": len(EXPECTED_INVARIANT), "mismatches": []}


def _assert_derived(artifacts: "BP2Artifacts") -> None:
    mismatches = []
    derived = {
        "practice_label": artifacts.practice_label,
        "e2_act": (artifacts.e2_receipt or {}).get("act", ""),
        "e2_actuator_ref": (artifacts.e2_receipt or {}).get("actuator_ref", ""),
        "e2_occurrence_ref": (artifacts.e2_receipt or {}).get("occurrence_ref", ""),
        "target_commit_time": (artifacts.e2_receipt or {}).get("target_commit_time"),
        "e2_action_time": (artifacts.e2_receipt or {}).get("action_time"),
    }
    for key, value in EXPECTED_DERIVED.items():
        if derived.get(key) != value:
            mismatches.append({"field": key, "expected": value, "actual": derived.get(key)})
    if mismatches:
        raise ReunionRefusal("BP2_DERIVED_IDENTITY_MISMATCH", json.dumps(mismatches[:4]))


def reconciliation(persisted: dict, artifacts: "BP2Artifacts | None" = None) -> dict:
    """Exact vs recomputed identity reconciliation with explicit origin change."""
    rows = []
    for key, value in EXPECTED_INVARIANT.items():
        rows.append({"field": key, "expected": value, "actual": persisted.get(key),
                     "class": "EXACT" if persisted.get(key) == value else "MISMATCH"})
    for key, value in LITERAL_ORIGIN.items():
        rows.append({"field": key, "literal_origin": value,
                     "actual": persisted.get(key),
                     "class": ("LITERAL_ORIGIN_MATCHED" if persisted.get(key) == value
                               else "RECOMPUTED")})
    if artifacts is not None:
        for key, value in EXPECTED_DERIVED.items():
            actual = {
                "practice_label": artifacts.practice_label,
                "e2_act": (artifacts.e2_receipt or {}).get("act", ""),
                "e2_actuator_ref": (artifacts.e2_receipt or {}).get("actuator_ref", ""),
                "e2_occurrence_ref": (artifacts.e2_receipt or {}).get("occurrence_ref", ""),
                "target_commit_time": (artifacts.e2_receipt or {}).get("target_commit_time"),
                "e2_action_time": (artifacts.e2_receipt or {}).get("action_time"),
            }.get(key)
            rows.append({"field": key, "expected": value, "actual": actual,
                         "class": "EXACT" if actual == value else "MISMATCH"})
    return {
        "schema": "BP2P4J_ORIGIN_RECONCILIATION@1",
        "rows": rows,
        "exact_count": sum(1 for row in rows if row["class"] in
                           ("EXACT", "LITERAL_ORIGIN_MATCHED")),
        "recomputed_count": sum(1 for row in rows if row["class"] == "RECOMPUTED"),
        "explanation": (
            "BP2's C8 commit receipt identity binds a random TEST_ONLY HMAC key "
            "and the absolute journal path (capability nonce = f(journal_id), "
            "issuer_ref carries journal_id). The key is generated per run and "
            "excluded from the committed return, so the literal commit receipt, "
            "E1 hash, response/grant hashes, target id, record hash and consumed "
            "hash cannot be reproduced at another root. Every value that does "
            "not depend on the key or path - occurrence id, C8 state/content/"
            "identity digests, writer version, both actor source/snapshot hashes, "
            "RULE_A/RULE_T semantic hashes, practice label, E2 act/actuator/"
            "occurrence and the logical clocks - MUST and does match exactly."),
    }


# ---------------------------------------------------------------------------
# FRESH mode
# ---------------------------------------------------------------------------
def build_fresh(root, *, actor: str = "A") -> BP2Artifacts:
    from bp2_joined.producer import JoinedProducer, joined_consumer_assertion

    root = Path(root)
    bp2_root = root / "bp2"
    bp2_root.mkdir(parents=True, exist_ok=True)
    producer = JoinedProducer(bp2_root, actor=actor)
    outcome = producer.run()
    if not outcome.ok:
        producer.close()
        raise ReunionRefusal("BP2_PRODUCER_REFUSED",
                             outcome.stage_reached + ":" + outcome.failure_code)
    joined_consumer_assertion(outcome)
    receipt = outcome.receipt()
    persisted = receipt["persisted"]
    invariants = _assert_invariants(persisted, mode="FRESH")
    life = producer.life
    env = producer.env
    producer.close()
    paths = {
        "journal_path": Path(persisted["journal_path"]),
        "key_path": env.key_path,
        "key_id": env.key_store.key_id,
        "anchor_log": env.anchor.log_path,
        "anchor_watermark": env.anchor.watermark_path,
        "c9_path": Path(persisted["c9_db_path"]),
    }
    artifacts = _assemble(mode="FRESH", root=bp2_root, life=life, persisted=persisted,
                          paths=paths, receipt=receipt, e2=None)
    _assert_derived(artifacts)
    artifacts.invariants = invariants  # type: ignore[attr-defined]
    _persist_binding(root, artifacts)
    return artifacts


def _assemble(*, mode: str, root: Path, life, persisted: dict, paths: dict,
              receipt: dict, e2: dict | None) -> BP2Artifacts:
    e2_receipt = e2 if e2 is not None else persisted.get("e2_owner_receipt")
    expected = {
        "c8_occurrence_id": persisted["c8_occurrence_id"],
        "c8_state_digest": persisted["c8_state_digest"],
        "c8_content_hash": persisted["c8_content_hash"],
        "c8_identity_digest": persisted["c8_identity_digest"],
        "c8_writer_version": persisted["c8_writer_version"],
        "c8_commit_receipt_id": persisted["c8_commit_receipt_id"],
        "actor_id": persisted["actor_id"],
        "rule_a_content_hash": persisted["rule_a_content_hash"],
        "response_hash": persisted["response_hash"],
        "c9_authorization_hash": persisted["c9_authorization_hash"],
        "target_id": persisted["target_id"],
        "target_record_hash": persisted["target_record_hash"],
        "consumed_state_hash": persisted["consumed_state_hash"],
        "e2_act": persisted["expected_act"],
        "e2_actuator_ref": (e2_receipt or {}).get("actuator_ref", ""),
        "e2_occurrence_ref": (e2_receipt or {}).get("occurrence_ref", ""),
        "event_time": persisted["event_time"],
        "target_commit_time": (e2_receipt or {}).get("target_commit_time",
                                                      persisted["event_time"]),
        "e2_action_time": (e2_receipt or {}).get("action_time", persisted["later_as_of"]),
        "e1_event_hash": persisted["e1_event_hash"],
    }
    c8 = _load_c8(paths["journal_path"], paths["key_path"], paths["key_id"],
                  paths["anchor_log"], paths["anchor_watermark"], expected)
    c9 = _verify_c9_rows(Path(paths["c9_path"]), expected)
    e2_admission = _verify_e2(e2_receipt, expected=expected, target=c9["target"])
    if e2_admission is not None and e2_admission["receipt_hash"] != persisted["e2_receipt_hash"]:
        raise ReunionRefusal("BP2_E2_RECEIPT_HASH_MISMATCH")
    snapshot_a = life.a_snapshot
    ok, reason = verify_snapshot(snapshot_a, expected_hash=persisted["actor_snapshot_hash"])
    if not ok:
        raise ReunionRefusal("BP2_ACTOR_SNAPSHOT_NOT_AUTHENTICATED", str(reason))
    payload = c8["event"].get("payload") or {}
    actor_block = payload.get("actor") or {}
    other_block = payload.get("other_actor") or {}
    if life.a_source.source_hash != actor_block.get("source_hash"):
        raise ReunionRefusal("BP1_ACTOR_SOURCE_NOT_MATCHING_BP2_C8",
                             life.a_source.source_hash)
    if life.b_source.source_hash != other_block.get("source_hash"):
        raise ReunionRefusal("BP1_OTHER_SOURCE_NOT_MATCHING_BP2_C8")
    if life.a_snapshot["hash"] != actor_block.get("snapshot_hash"):
        raise ReunionRefusal("BP1_ACTOR_SNAPSHOT_NOT_MATCHING_BP2_C8")
    if life.b_snapshot["hash"] != other_block.get("snapshot_hash"):
        raise ReunionRefusal("BP1_OTHER_SNAPSHOT_NOT_MATCHING_BP2_C8")
    if actor_block.get("source_hash") != persisted["actor_source_hash"]:
        raise ReunionRefusal("BP2_ACTOR_SOURCE_NOT_MATCHING_C8")
    if other_block.get("source_hash") != persisted["other_source_hash"]:
        raise ReunionRefusal("BP2_OTHER_SOURCE_NOT_MATCHING_C8")
    if actor_block.get("snapshot_hash") != persisted["actor_snapshot_hash"]:
        raise ReunionRefusal("BP2_ACTOR_SNAPSHOT_NOT_MATCHING_C8")
    if other_block.get("snapshot_hash") != persisted["other_snapshot_hash"] \
            if "other_snapshot_hash" in persisted else False:
        raise ReunionRefusal("BP2_OTHER_SNAPSHOT_NOT_MATCHING_C8")
    if "other_snapshot_hash" not in persisted:
        other_snap = life.b_snapshot["hash"]
        if other_block.get("snapshot_hash") != other_snap:
            raise ReunionRefusal("BP2_OTHER_SNAPSHOT_NOT_MATCHING_C8")
    if actor_block.get("actor_id") == other_block.get("actor_id"):
        raise ReunionRefusal("BP2_OTHER_ACTOR_ALIASED")
    return BP2Artifacts(
        mode=mode,
        root=Path(root),
        life=life,
        journal_path=Path(paths["journal_path"]),
        key_path=Path(paths["key_path"]),
        key_id=str(paths["key_id"]),
        anchor_log=Path(paths["anchor_log"]),
        anchor_watermark=Path(paths["anchor_watermark"]),
        c9_path=Path(paths["c9_path"]),
        occurrence_id=persisted["c8_occurrence_id"],
        c8_state_digest=persisted["c8_state_digest"],
        c8_content_hash=persisted["c8_content_hash"],
        c8_identity_digest=persisted["c8_identity_digest"],
        c8_ledger_prefix_digest=c8["readset"]["ledger_prefix_digest"],
        c8_writer_version=int(persisted["c8_writer_version"]),
        c8_commit_receipt_id=persisted["c8_commit_receipt_id"],
        c8_canonical_bytes_sha256=c8["readset"]["canonical_bytes_sha256"],
        e1_event_id=persisted["e1_event_id"],
        e1_event_hash=persisted["e1_event_hash"],
        target_id=persisted["target_id"],
        target_record_hash=persisted["target_record_hash"],
        consumed_state_hash=persisted["consumed_state_hash"],
        target=c9["target"],
        rule_a_hash=persisted["rule_a_content_hash"],
        rule_t_hash=persisted["rule_t_content_hash"],
        rule_t_dependency=persisted["rule_t_dependency_hash"],
        response_hash=persisted["response_hash"],
        grant_hash=persisted["grant_hash"],
        e2_receipt=e2_receipt,
        e2_receipt_hash=persisted["e2_receipt_hash"] if e2_admission else "",
        event_time=int(persisted["event_time"]),
        as_of=int(persisted["as_of"]),
        later_as_of=int(persisted["later_as_of"]),
        practice_label=c9["target"]["record_preimage"]["governed_payload"]["practice_label"],
        receipt=receipt,
    )


# ---------------------------------------------------------------------------
# persisted binding + RECOVERED mode (cold reentry)
# ---------------------------------------------------------------------------
def _persist_binding(root: Path, artifacts: BP2Artifacts) -> None:
    document = {
        "schema": "BP2P4J_BP2_JOIN_BINDING@1",
        "artifacts": artifacts.public(),
        "persisted": artifacts.receipt["persisted"],
        "reconciliation": reconciliation(artifacts.receipt["persisted"], artifacts),
    }
    (Path(root) / "bp2_join.json").write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf8")


def recover(root) -> BP2Artifacts:
    root = Path(root)
    binding_path = root / "bp2_join.json"
    if not binding_path.exists():
        raise ReunionRefusal("BP2_JOIN_BINDING_ABSENT", str(binding_path))
    document = json.loads(binding_path.read_text(encoding="utf8"))
    persisted = document["persisted"]
    invariants = _assert_invariants(persisted, mode="RECOVERED")
    life = build_two_actor_life()
    recorded = document["artifacts"]
    paths = {
        "journal_path": Path(recorded["journal_path"]),
        "key_path": Path(recorded["key_path"]),
        "key_id": recorded["key_id"],
        "anchor_log": Path(recorded["anchor_log"]),
        "anchor_watermark": Path(recorded["anchor_watermark"]),
        "c9_path": Path(recorded["c9_path"]),
    }
    for name, path in paths.items():
        if name == "key_id":
            continue
        if not Path(path).exists():
            raise ReunionRefusal("BP2_ARTIFACT_MISSING", name + ":" + str(path))
    receipt = {"persisted": persisted}
    bp2_root = Path(recorded["root"])
    if not bp2_root.exists():
        raise ReunionRefusal("BP2_ARTIFACT_ROOT_MISSING", str(bp2_root))
    artifacts = _assemble(mode="RECOVERED", root=bp2_root, life=life,
                          persisted=persisted, paths=paths, receipt=receipt, e2=None)
    _assert_derived(artifacts)
    artifacts.invariants = invariants  # type: ignore[attr-defined]
    return artifacts


# ---------------------------------------------------------------------------
# ORIGIN_LITERAL mode
# ---------------------------------------------------------------------------
def origin_runtime_available(path: str | Path | None = None) -> Path | None:
    candidate = Path(path or DEFAULT_ORIGIN_RUNTIME)
    required = (candidate / "c9.sqlite", candidate / "journal" / "journal.json",
                candidate / "keys" / "writer_keys.json",
                candidate / "anchor" / "rows.json",
                candidate / "anchor" / "watermark.json")
    return candidate if all(p.exists() for p in required) else None


def load_origin_literal(origin_root, *, evidence_path, workspace=None) -> BP2Artifacts:
    """Read the exact surviving BP2 origin runtime (literal target 950a4c79…)."""
    origin = Path(origin_root)
    evidence = json.loads(Path(evidence_path).read_text(encoding="utf8"))
    persisted = evidence["persisted"]
    invariants = _assert_invariants(persisted, mode="ORIGIN_LITERAL")
    for key, value in LITERAL_ORIGIN.items():
        if persisted.get(key) != value:
            raise ReunionRefusal("ORIGIN_LITERAL_IDENTITY_MISMATCH", key)
    with CandidateStore(origin / "c9.sqlite") as store:
        target = store.read_target_state(LITERAL_ORIGIN["target_id"])
    if target is None:
        raise ReunionRefusal("ORIGIN_LITERAL_TARGET_ABSENT")
    if digest(dict(target)) != LITERAL_ORIGIN["consumed_state_hash"]:
        raise ReunionRefusal("ORIGIN_LITERAL_CONSUMED_HASH_MISMATCH")
    life = build_two_actor_life()
    paths = {
        "journal_path": origin / "journal" / "journal.json",
        "key_path": origin / "keys" / "writer_keys.json",
        "key_id": "BP2-TEST-KEY",
        "anchor_log": origin / "anchor" / "rows.json",
        "anchor_watermark": origin / "anchor" / "watermark.json",
        "c9_path": origin / "c9.sqlite",
    }
    artifacts = _assemble(mode="ORIGIN_LITERAL", root=origin, life=life,
                          persisted=persisted, paths=paths,
                          receipt={"persisted": persisted},
                          e2=persisted.get("e2_owner_receipt"))
    _assert_derived(artifacts)
    artifacts.invariants = invariants  # type: ignore[attr-defined]
    if workspace is not None:
        _persist_binding(Path(workspace), artifacts)
    return artifacts


def verify_artifacts(artifacts: BP2Artifacts) -> BP2Artifacts:
    """Re-run every physical source check against the on-disk artifacts."""
    persisted = artifacts.receipt["persisted"]
    paths = {
        "journal_path": artifacts.journal_path,
        "key_path": artifacts.key_path,
        "key_id": artifacts.key_id,
        "anchor_log": artifacts.anchor_log,
        "anchor_watermark": artifacts.anchor_watermark,
        "c9_path": artifacts.c9_path,
    }
    return _assemble(mode=artifacts.mode, root=artifacts.root, life=artifacts.life,
                     persisted=persisted, paths=paths, receipt=artifacts.receipt,
                     e2=artifacts.e2_receipt)


def clone_artifacts(artifacts: BP2Artifacts, destination) -> BP2Artifacts:
    """Copy the physical artifacts to a fault-injection workspace and re-verify."""
    destination = Path(destination)
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    shutil.copytree(artifacts.root, destination / "bp2")
    clone = load_clone(destination / "bp2", artifacts)
    _persist_binding(destination, clone)
    return clone


def load_clone(bp2_root: Path, original: BP2Artifacts) -> BP2Artifacts:
    """Re-verify a copied BP2 runtime without re-running the producer."""
    persisted = original.receipt["persisted"]
    invariants = _assert_invariants(persisted, mode="CLONE")
    life = build_two_actor_life()
    paths = {
        "journal_path": bp2_root / "journal" / "journal.json",
        "key_path": bp2_root / "keys" / "writer_keys.json",
        "key_id": original.key_id,
        "anchor_log": bp2_root / "anchor" / "rows.json",
        "anchor_watermark": bp2_root / "anchor" / "watermark.json",
        "c9_path": bp2_root / "c9.sqlite",
    }
    artifacts = _assemble(mode="CLONE", root=bp2_root, life=life,
                          persisted=persisted, paths=paths,
                          receipt={"persisted": persisted}, e2=None)
    _assert_derived(artifacts)
    artifacts.invariants = invariants  # type: ignore[attr-defined]
    return artifacts


__all__ = [
    "BP2Artifacts",
    "BP2_COMMIT",
    "DEFAULT_ORIGIN_RUNTIME",
    "EXPECTED_INVARIANT",
    "LITERAL_ORIGIN",
    "ReunionRefusal",
    "build_fresh",
    "clone_artifacts",
    "load_clone",
    "load_origin_literal",
    "origin_runtime_available",
    "reconciliation",
    "recover",
]
