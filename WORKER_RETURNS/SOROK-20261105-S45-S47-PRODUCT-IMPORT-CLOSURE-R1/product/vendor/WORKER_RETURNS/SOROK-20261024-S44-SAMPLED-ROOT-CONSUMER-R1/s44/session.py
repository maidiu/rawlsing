"""S44 generated-root substitution into the actual S43/S42 person consumer."""
from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Mapping

from .bootstrap import install

install()

import firstclass  # noqa: E402
import s40.language as s40_language  # noqa: E402
from s43.session import S43Session  # noqa: E402

from .bundle import default_bundle  # noqa: E402
from .errors import S44Refusal  # noqa: E402
from .root import ROOT_GRADE, ROOT_SCHEMA, SampledRoot, generate_root  # noqa: E402

S44_SCHEMA = "SOROK_S44_SAMPLED_ROOT_SESSION@1"
ROOT_FILE = "s44_root.json"
ROOT_BINDING_KIND = "S44_SAMPLED_ROOT_BINDING"


@contextmanager
def _root_life(life):
    original = firstclass.prepare_life

    def prepare(source, variant="A_REPAIR_LONG", *args, **kwargs):
        return life

    firstclass.prepare_life = prepare
    try:
        yield
    finally:
        firstclass.prepare_life = original


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf8"))


class S44Session(S43Session):
    """S43 consumer whose actual root is the sampled antecedent history."""

    _S44_ACTIVE_START = False

    @classmethod
    def start(
        cls,
        state_root,
        *,
        bundle: Mapping[str, Any] | None = None,
        language_context: Mapping[str, Any] | None = None,
        **kwargs,
    ) -> "S44Session":
        state_root = Path(state_root).resolve()
        state_root.mkdir(parents=True, exist_ok=True)
        root_path = state_root / ROOT_FILE
        if root_path.exists():
            raise S44Refusal("S44_ROOT_ALREADY_FROZEN", str(root_path))
        root = generate_root(bundle or default_bundle(root_seed="00" * 32))
        root_path.write_text(
            json.dumps({
                "schema": "S44_FROZEN_ROOT_FILE@1",
                "bundle": root.bundle,
                "receipt": root.receipt,
            }, indent=2, sort_keys=True) + "\n",
            encoding="utf8",
        )
        admissions = []

        def admit_root_language(session):
            for evidence in root.bundle.get("language_evidence") or []:
                admitted = session.admit_language_encounter(
                    text=evidence["text"],
                    concept_id=evidence["concept_id"],
                    milieu_id=evidence["milieu_id"],
                    sense_id=evidence["sense_id"],
                    relation_label=evidence["relation_label"],
                    atoms=list(evidence["atoms"]),
                    language_tag=evidence.get("language_tag", "es-MX"),
                    speaker_actor=evidence.get("speaker_actor", "B"),
                    counterexample_event_ids=tuple(
                        evidence.get("counterexample_event_ids") or ()
                    ),
                )
                admissions.append({
                    "evidence_id": evidence.get("evidence_id", ""),
                    "source_event_id": admitted["event"]["event_id"],
                    "source_event_hash": admitted["event"]["hash"],
                    "relation_id": admitted["encounter"]["encounter_id"],
                    "access_receipt_id": admitted["encounter"]["access_receipt_id"],
                    "milieu_id": admitted["encounter"]["milieu_id"],
                    "sense_id": admitted["encounter"]["sense_id"],
                    "source_grade": admitted["event"]["body"].get("source_grade", ""),
                    "text": evidence["text"],
                    "language_tag": evidence.get("language_tag", "es-MX"),
                })

        original_source_for_intent = s40_language._source_for_intent

        def source_for_intent(session, intent):
            if not admissions:
                admit_root_language(session)
            target = (
                (session.s43_context() or language_context or {}).get("milieu_id", "")
            )
            candidates = list(zip(
                root.bundle.get("language_evidence") or [], admissions
            ))
            matching = [
                (evidence, admitted) for evidence, admitted in candidates
                if (not target or evidence.get("milieu_id") == target)
                and evidence.get("intent", intent) == intent
            ] or [
                (evidence, admitted) for evidence, admitted in candidates
                if evidence.get("intent", intent) == intent
            ]
            if matching:
                evidence, admitted = matching[0]
                if intent in {"REQUEST_TOOL", "EXPLICIT_REFUSAL"}:
                    return {
                        "event": session.event(admitted["source_event_id"]),
                        "access": {
                            "receipt": {
                                "receipt_id": admitted["access_receipt_id"],
                            }
                        },
                        "receipt": {
                            "receipt_id": admitted["access_receipt_id"],
                        },
                    }
            raise S44Refusal(
                "S44_INITIAL_LANGUAGE_EVIDENCE_MISSING", str(intent)
            )

        s40_language._source_for_intent = source_for_intent
        try:
            cls._S44_ACTIVE_START = True
            with _root_life(root.life):
                session = super().start(
                    state_root, language_context=language_context, **kwargs
                )
            if not admissions:
                admit_root_language(session)
            root.receipt["language_evidence_admissions"] = admissions
            root_path.write_text(
                json.dumps({
                    "schema": "S44_FROZEN_ROOT_FILE@1",
                    "bundle": root.bundle,
                    "receipt": root.receipt,
                }, indent=2, sort_keys=True) + "\n",
                encoding="utf8",
            )
            session.meta.update({
                "s44_schema": S44_SCHEMA,
                "s44_root_hash": root.root_hash,
                "s44_root_id": root.receipt["root_id"],
                "s44_root_bundle_hash": root.bundle["bundle_hash"],
                "s44_root_selected_finished_life": False,
                "s44_language_evidence": admissions,
            })
            session._save_join_meta()
            body = {
                "schema": "SOROK_S44_SAMPLED_ROOT_BINDING@1",
                "grade": ROOT_GRADE,
                "native": False,
                "root_hash": root.root_hash,
                "root_id": root.receipt["root_id"],
                "bundle_hash": root.bundle["bundle_hash"],
                "root_seed_sha256": root.receipt["root_seed_sha256"],
                "actor_ids": root.receipt["actor_ids"],
                "source_hashes": root.receipt["source_hashes"],
                "source_refs": root.receipt["source_refs"],
                "event_refs": root.receipt["event_refs"],
                "g18_history_refs": root.receipt["g18_history_refs"],
                "g18_history_hashes": root.receipt["g18_history_hashes"],
                "snapshot_hashes": root.receipt["snapshot_hashes"],
                "draw_receipt_hashes": [
                    row["decision_replay_identity_hash"]
                    for row in root.receipt["draw_receipts"]
                ],
                "language_evidence": admissions,
                "selected_finished_life": False,
                "psychology_claim": False,
                "product_model_calls": 0,
            }
            session.product._append_episode(
                session.branch_id, "A", ROOT_BINDING_KIND,
                session.clock(), body,
            )
            session.product._checkpoint(
                session.branch_id, session.clock(), session.world()
            )
        except Exception:
            try:
                session.close()
            except UnboundLocalError:
                pass
            if root_path.exists():
                root_path.unlink()
            raise
        finally:
            s40_language._source_for_intent = original_source_for_intent
            cls._S44_ACTIVE_START = False
        return session

    @classmethod
    def open(cls, state_root, **kwargs) -> "S44Session":
        state_root = Path(state_root).resolve()
        root_path = state_root / ROOT_FILE
        if not root_path.is_file():
            raise S44Refusal("S44_ROOT_MISSING", str(root_path))
        document = _read_json(root_path)
        root = generate_root(document["bundle"])
        if root.root_hash != document["receipt"]["root_hash"]:
            raise S44Refusal(
                "S44_ROOT_REPLAY_MISMATCH",
                f'{root.root_hash} != {document["receipt"]["root_hash"]}',
            )
        with _root_life(root.life):
            return super().open(state_root, **kwargs)

    def read_root(self) -> dict:
        root_path = self.state_root / ROOT_FILE
        if not root_path.is_file():
            raise S44Refusal("S44_ROOT_MISSING", str(root_path))
        document = _read_json(root_path)
        receipt = document.get("receipt") or {}
        calculated = generate_root(document["bundle"]).receipt
        if calculated["root_hash"] != receipt.get("root_hash"):
            raise S44Refusal("S44_ROOT_REPLAY_MISMATCH")
        bindings = [
            row for row in self.product.store.episodes(self.branch_id)
            if row.get("kind") == ROOT_BINDING_KIND
        ]
        if len(bindings) != 1:
            raise S44Refusal("S44_ROOT_BINDING_COUNT", str(len(bindings)))
        binding = dict(bindings[0].get("body") or {})
        if binding.get("root_hash") != receipt["root_hash"]:
            raise S44Refusal("S44_ROOT_BINDING_HASH_MISMATCH")
        if binding.get("event_refs") != receipt["event_refs"]:
            raise S44Refusal("S44_ROOT_EVENT_REFS_MISMATCH")
        if binding.get("g18_history_refs") != receipt["g18_history_refs"]:
            raise S44Refusal("S44_ROOT_G18_REFS_MISMATCH")
        language = receipt.get("language_evidence_admissions", [])
        if binding.get("language_evidence") != language:
            raise S44Refusal("S44_ROOT_LANGUAGE_BINDING_MISMATCH")
        for admission in language:
            event = self.event(admission.get("source_event_id", ""))
            if not event or event.get("hash") != admission.get("source_event_hash"):
                raise S44Refusal("S44_ROOT_LANGUAGE_EVENT_MISMATCH")
            if event.get("body", {}).get("text") != admission.get("text"):
                raise S44Refusal("S44_ROOT_LANGUAGE_TEXT_MISMATCH")
        return {
            "schema": "SOROK_S44_ROOT_READ@1",
            "status": "OK",
            "root_hash": receipt["root_hash"],
            "root_id": receipt["root_id"],
            "bundle_hash": document["bundle"]["bundle_hash"],
            "root_seed_sha256": receipt["root_seed_sha256"],
            "actor_ids": receipt["actor_ids"],
            "source_hashes": receipt["source_hashes"],
            "source_refs": receipt["source_refs"],
            "event_refs": receipt["event_refs"],
            "g18_history_refs": receipt["g18_history_refs"],
            "g18_history_hashes": receipt["g18_history_hashes"],
            "snapshot_hashes": receipt["snapshot_hashes"],
            "state": receipt["state"],
            "selected_branches": receipt["selected_branches"],
            "draw_receipts": receipt["draw_receipts"],
            "language_evidence": receipt.get("language_evidence_admissions", []),
            "selected_finished_life": False,
            "psychology_claim": False,
        }

    def verify(self) -> dict:
        result = super().verify()
        if type(self)._S44_ACTIVE_START:
            result["s44_root"] = {"status": "INITIALIZING"}
            return result
        try:
            root = self.read_root()
            result["s44_root"] = {
                "status": "OK", "root_hash": root["root_hash"],
                "actor_ids": root["actor_ids"],
                "event_ref_count": sum(len(v) for v in root["event_refs"].values()),
            }
            root_ok = True
        except (S44Refusal, KeyError, OSError, ValueError) as exc:
            result["s44_root"] = {"status": "REFUSED", "code": str(exc)}
            root_ok = False
        result["ok"] = bool(result.get("ok")) and root_ok
        return result

    def status(self) -> dict:
        result = super().status()
        try:
            root = self.read_root()
            result["s44_root"] = {
                "status": "OK", "root_hash": root["root_hash"],
                "root_id": root["root_id"], "actor_ids": root["actor_ids"],
                "bundle_hash": root["bundle_hash"],
            }
        except (S44Refusal, KeyError, OSError, ValueError) as exc:
            result["s44_root"] = {"status": "REFUSED", "code": str(exc)}
        return result


__all__ = ["S44_SCHEMA", "S44Session", "ROOT_FILE", "ROOT_BINDING_KIND"]
