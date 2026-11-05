"""S45 user encounter over the actual generated S44 root."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .bootstrap import install

install()

import s40.session as s40_session  # noqa: E402
from bp1.canon import digest  # noqa: E402
from bp4.world import WorldRefusal, owner_receipt, repair_event  # noqa: E402
from candidate import seal  # noqa: E402
from r31e import expression  # noqa: E402
from s40.session import S40GeneratedSession  # noqa: E402
from s42.reader import S42ReadRefusal  # noqa: E402
from s44.session import S44Session  # noqa: E402

from .errors import S45Refusal  # noqa: E402
from .language import ATOMS, PAIRS, compile_help_plan  # noqa: E402

S45_SCHEMA = "SOROK_S45_GENERATED_ROOT_ENCOUNTER@1"
ENCOUNTER_KIND = "S45_USER_ENCOUNTER"
BINDING_SCHEMA = "S40_GENERATED_LANGUAGE_BINDING@1"
S45_BINDING_SCHEMA = "S45_HELP_LANGUAGE_BINDING@1"
GRADE = "TEST_ONLY_SOURCEBOUND_GENERATED_ROOT_ENCOUNTER_NOT_NATIVE"


class S45ReadRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


class S45Session(S44Session):
    """S44 root plus user SAY/DO/ATTEND through the same person runtime."""

    _S45_ACTIVE_START = False

    @classmethod
    def start(cls, state_root, *, bundle=None, language_context=None,
              attention: str = "focused", **kwargs) -> "S45Session":
        if bundle is None:
            from .fixtures import root_bundle
            bundle = root_bundle()
        session = super().start(
            state_root, bundle=bundle,
            language_context=language_context or {"milieu_id": "workshop"},
            attention=attention, **kwargs,
        )
        session._last_language = None
        session.meta.update({"s45_schema": S45_SCHEMA})
        session._save_join_meta()
        return session

    @classmethod
    def open(cls, state_root, **kwargs) -> "S45Session":
        session = super().open(state_root, **kwargs)
        session._last_language = None
        return session

    # ------------------------------------------------------------------
    # existing user-owned semantic entry points
    # ------------------------------------------------------------------
    def say(self, text: str) -> dict:
        self._last_language = None
        try:
            result = super().say(text)
        except S45Refusal as exc:
            result = {
                "status": "UNSUPPORTED",
                "reason": exc.code,
                "user_event": self._latest_user_event("SPEECH"),
                "strategy": None,
                "candidate": None,
                "admission": None,
                "surface": self._surface(
                    [self._latest_user_event("SPEECH")["event_id"]]
                ),
            }
        except WorldRefusal:
            raise
        self._record_encounter("SAY", result)
        return result

    def do_help(self) -> dict:
        self._last_language = None
        try:
            result = super().do_help()
        except S45Refusal as exc:
            result = {
                "status": "UNSUPPORTED",
                "accepted": False,
                "reason": exc.code,
                "strategy": None,
                "candidate": None,
                "admission": None,
                "surface": [],
                "language": None,
            }
        result["language"] = result.get("language") or self._last_language
        self._record_encounter("DO_HELP", result)
        return result

    def attend(self) -> dict:
        self._last_language = None
        result = super().attend()
        self._record_encounter("ATTEND", result)
        return result

    # ------------------------------------------------------------------
    # semantic admission + source-bound language before speech commit
    # ------------------------------------------------------------------
    def _respond(self, kind: str, text: str = "", event_id: str = "") -> dict:
        if kind not in {"SAY", "DO_HELP"}:
            return super()._respond(kind, text=text, event_id=event_id)
        contract = expression.compile_contract(
            self, trigger_kind=kind, trigger_text=text,
            trigger_event_id=event_id,
        )
        candidates = expression.propose(contract)
        chosen = None
        validation = None
        for candidate in candidates:
            check = expression.validate(candidate, contract, self)
            if not check["ok"]:
                continue
            if candidate.speech is None or candidate.action not in {"NONE", "REPAIR"}:
                continue
            chosen = candidate
            validation = check
            break
        if chosen is None:
            raise S45Refusal("S45_UNSUPPORTED_INPUT", kind)
        candidate = chosen.public()
        plan, index = compile_help_plan(self, candidate, contract)
        from language_mediation.artifacts import (
            build_native_artifact,
            build_translation_artifact,
        )
        from language_mediation.equivalence import evaluate_pair

        native = build_native_artifact(plan)
        translation = build_translation_artifact(plan, native)
        receipt = evaluate_pair(
            plan, native, translation, pairs=PAIRS, atom_universe=ATOMS
        )
        if receipt.get("status") != "ACCEPTED":
            raise S45Refusal(
                "S45_EQUIVALENCE_REJECTED",
                ",".join(receipt.get("codes", [])),
            )

        world = self.world()
        action_event = None
        if chosen.action == "REPAIR":
            action_receipt = owner_receipt(
                act="REPAIR", actor_id="A", clock=world.clock,
                location=world.positions["A"],
            )
            action_event = repair_event(
                world, actor_id="A", receipt=action_receipt
            )
            self._append_event(action_event, perceive=("A",))
            self._perceive_if_present(action_event, "U", "B")
            self.product._append_episode(
                self.branch_id, "A", "DO", world.clock,
                {"action": "repair", "attempted": True, "admitted": True,
                 "event_id": action_event["event_id"],
                 "user_proposal": True,
                 "strategy": chosen.strategy,
                 "contract_hash": contract["contract_hash"]},
            )
            self.product._checkpoint(self.branch_id, world.clock, world)

        candidate_public = chosen.public()
        candidate_public["speech"] = native["text"]
        candidate_public["speech_english"] = chosen.speech
        candidate_public["language_tag"] = native["language_tag"]
        candidate_public["s45_language"] = {
            "plan_hash": plan.plan_hash,
            "native_text": native["text"],
            "translation_text": translation["text"],
            "equivalence_status": receipt["status"],
        }
        admission_id = digest({
            "candidate": candidate_public,
            "contract_hash": contract["contract_hash"],
            "plan_hash": plan.plan_hash,
            "native_artifact_hash": native["artifact_hash"],
            "translation_artifact_hash": translation["artifact_hash"],
            "clock": world.clock,
            "action_event_id": action_event["event_id"] if action_event else "",
        })
        event = self._write_speech_event(
            plan, native, translation, receipt, contract,
            candidate_public, admission_id,
        )
        admission = self._admission(
            plan, native, translation, receipt, contract, event,
            candidate_public, admission_id, index,
        )
        admission.update({
            "schema": "S45_USER_EXPRESSION_ADMISSION@1",
            "r31e_strategy": chosen.strategy,
            "r31e_template_id": chosen.template_id,
            "r31e_validation": validation,
            "action_event_id": action_event["event_id"] if action_event else "",
            "contact_outcome": chosen.contact,
            "user_trigger_kind": kind,
            "user_trigger_event_id": event_id,
            "s45_boundary": True,
        })
        self.product._append_episode(
            self.branch_id, "A", "SAY", world.clock,
            {"event_id": event["event_id"], "text": native["text"],
             "gesture": candidate_public["gesture"],
             "tone": candidate_public["tone"],
             "strategy": chosen.strategy,
             "contract_hash": contract["contract_hash"],
             "admission_id": admission_id,
             "plan_hash": plan.plan_hash,
             "spans": event["body"]["spans"],
             "s45_boundary": True},
        )
        self.product._append_episode(
            self.branch_id, "A", "EXPRESSION_ADMISSION", world.clock,
            {"admission": admission, "candidate": candidate_public,
             "plan": plan.public(),
             "contract_hash": contract["contract_hash"],
             "multilingual_port": {
                 "schema": "S45_HELP_LANGUAGE_PORT@1", "version": 1,
             }},
        )
        projection = self._write_translation_projection(
            event, plan, native, translation, receipt
        )
        self.product._checkpoint(self.branch_id, world.clock, world)
        source_refs = list(plan.readset.get("source_event_refs") or [])
        access_ids = list(plan.readset.get("access_receipt_ids") or [])
        binding = seal({
            "schema": BINDING_SCHEMA,
            "s43_schema": S45_BINDING_SCHEMA,
            "grade": GRADE,
            "provenance": "TEST_ONLY_SOURCEBOUND_GENERATED_ROOT_ENCOUNTER",
            "native": False,
            "intent": chosen.strategy,
            "template_id": chosen.template_id,
            "language_tag": native["language_tag"],
            "target_language_tag": translation["target_language_tag"],
            "native_text": native["text"],
            "translation_text": translation["text"],
            "plan_hash": plan.plan_hash,
            "contract_hash": contract["contract_hash"],
            "native_artifact_hash": native["artifact_hash"],
            "translation_artifact_hash": translation["artifact_hash"],
            "equivalence_receipt_hash": receipt["receipt_hash"],
            "equivalence_status": receipt["status"],
            "equivalence_codes": list(receipt.get("codes", [])),
            "source_event_id": source_refs[0]["event_id"] if source_refs else "",
            "source_event_hash": source_refs[0]["event_hash"] if source_refs else "",
            "access_receipt_id": access_ids[0] if access_ids else "",
            "source_event_refs": source_refs,
            "access_receipt_ids": access_ids,
            "speech_event_id": event["event_id"],
            "speech_event_hash": event["hash"],
            "action_event_id": admission["action_event_id"],
            "admission_id": admission_id,
            "projection_episode_id": projection["episode_id"],
            "private_generation_sources_in_plan": False,
            "target_proposals": [],
            "s45_strategy": chosen.strategy,
            "s45_template_id": chosen.template_id,
            "s45_boundary": True,
        })
        self._last_language = binding
        event_ids = []
        if action_event:
            event_ids.append(action_event["event_id"])
        event_ids.append(event["event_id"])
        return {
            "admission": admission,
            "candidate": candidate_public,
            "event_ids": event_ids,
            "contact": chosen.contact,
            "contract": contract,
            "language": binding,
        }

    # ------------------------------------------------------------------
    # encounter binding / readers
    # ------------------------------------------------------------------
    def _latest_user_event(self, kind: str) -> dict:
        rows = [
            event for event in self.events()
            if event.get("actor_id") == "U" and event.get("kind") == kind
        ]
        if not rows:
            raise S45Refusal("S45_USER_EVENT_MISSING")
        return rows[-1]

    def _record_encounter(self, kind: str, result: Mapping[str, Any]) -> dict:
        user_event = result.get("user_event")
        user_episode = None
        if not user_event:
            wanted = "SPEECH" if kind == "SAY" else (
                "DO" if kind == "DO_HELP" else "ATTEND"
            )
            user_episodes = [
                row for row in self.episodes("U")
                if row.get("kind") == wanted
            ]
            if user_episodes:
                user_episode = user_episodes[-1]
        admission = result.get("admission") or {}
        language = result.get("language") if kind in {"SAY", "DO_HELP"} else None
        if kind in {"SAY", "DO_HELP"} and not language:
            language = self._last_language or {}
        candidate = result.get("candidate") or {}
        action_id = admission.get("action_event_id", "")
        action_event = self.event(action_id) if action_id else None
        speech_id = (language or {}).get("speech_event_id", "")
        speech_event = self.event(speech_id) if speech_id else None
        root = self.read_root()
        body = {
            "schema": S45_SCHEMA,
            "grade": GRADE,
            "native": False,
            "kind": kind,
            "status": result.get("status"),
            "reason": result.get("reason", ""),
            "branch_id": self.branch_id,
            "root_hash": root["root_hash"],
            "root_id": root["root_id"],
            "user_event_id": (user_event or {}).get("event_id", ""),
            "user_event_hash": (user_event or {}).get("hash", ""),
            "user_event_kind": (user_event or {}).get("kind", ""),
            "user_text": (user_event or {}).get("body", {}).get("text", ""),
            "user_episode_id": (user_episode or {}).get("episode_id", ""),
            "user_episode_body": dict((user_episode or {}).get("body") or {}),
            "user_episode_hash": (
                digest((user_episode or {}).get("body") or {})
                if user_episode else ""
            ),
            "strategy": candidate.get("strategy", result.get("strategy")),
            "template_id": candidate.get("template_id", ""),
            "speech_event_id": speech_id,
            "speech_event_hash": (speech_event or {}).get("hash", ""),
            "speech_event_kind": (speech_event or {}).get("kind", ""),
            "action_event_id": action_id,
            "action_event_hash": (action_event or {}).get("hash", ""),
            "action_event_kind": (action_event or {}).get("kind", ""),
            "admission_id": admission.get("admission_id", ""),
            "plan_hash": (language or {}).get("plan_hash", ""),
            "native_text": (language or {}).get("native_text", ""),
            "translation_text": (language or {}).get("translation_text", ""),
            "source_event_refs": list((language or {}).get("source_event_refs") or []),
            "access_receipt_ids": list((language or {}).get("access_receipt_ids") or []),
            "language": dict(language) if language else None,
            "clock": self.clock(),
            "product_model_calls": 0,
            "target_proposals": [],
            "s45_boundary": True,
        }
        body["encounter_hash"] = digest(body)
        episode = self.product._append_episode(
            self.branch_id, "A", ENCOUNTER_KIND, self.clock(), body
        )
        self.product._checkpoint(self.branch_id, self.clock(), self.world())
        return {**body, "encounter_id": episode["episode_id"]}

    def _c9_lineage(self) -> dict | None:
        base = list(super().read_events())
        if not base:
            return None
        row = base[-1]
        c9 = row.get("c9")
        if not isinstance(c9, dict):
            return None
        return {
            "lineage_only": True,
            "source_event_ordinal": row.get("event_ordinal"),
            "source_e1_event_id": row.get("e1_event_id", ""),
            "source_e1_event_hash": row.get("e1_event_hash", ""),
            **dict(c9),
        }

    def _root_evidence(self) -> dict:
        root = self.read_root()
        source_ids = {}
        access_ids = {}
        for row in root.get("language_evidence", []):
            source_ids[row.get("source_event_id", "")] = row
            access_ids[row.get("access_receipt_id", "")] = row
        return {"root": root, "sources": source_ids, "access": access_ids}

    def _current_access(self, access_ids: list[str]) -> dict:
        try:
            from language_mediation.index import build_index
            index = build_index(self, actor_id="A")
            invalid_access = set()
            for row in index.get("invalidated_relations", []):
                receipt = (row.get("access_receipt") or {}).get("receipt_id", "")
                if receipt:
                    invalid_access.add(receipt)
            return {
                receipt: ("REVOKED" if receipt in invalid_access else "GRANTED")
                for receipt in access_ids
            }
        except Exception as exc:
            return {receipt: "UNKNOWN:" + type(exc).__name__
                    for receipt in access_ids}

    def _validate_encounter(self, body: dict) -> dict:
        if body.get("schema") != S45_SCHEMA:
            raise S45ReadRefusal("S45_ENCOUNTER_SCHEMA_MISMATCH")
        kind = body.get("kind")
        if kind not in {"SAY", "DO_HELP", "ATTEND"}:
            raise S45ReadRefusal("S45_ENCOUNTER_KIND_INVALID", str(kind))
        evidence = self._root_evidence()
        root = evidence["root"]
        if body.get("branch_id") != self.branch_id:
            raise S45ReadRefusal("S45_ENCOUNTER_BRANCH_MISMATCH")
        if body.get("root_hash") != root["root_hash"]:
            raise S45ReadRefusal("S45_ENCOUNTER_ROOT_MISMATCH")
        stored_hash = body.get("encounter_hash", "")
        hash_body = {k: v for k, v in body.items()
                     if k not in {"encounter_id", "encounter_hash"}}
        if not stored_hash or stored_hash != digest(hash_body):
            raise S45ReadRefusal("S45_ENCOUNTER_HASH_MISMATCH")
        if kind == "SAY":
            user = self.event(body.get("user_event_id", ""))
            if not user or user.get("hash") != body.get("user_event_hash"):
                raise S45ReadRefusal("S45_USER_EVENT_MISSING")
            if user.get("actor_id") != "U" or user.get("kind") != "SPEECH":
                raise S45ReadRefusal("S45_USER_EVENT_NOT_SPEECH")
            if user.get("body", {}).get("text", "") != body.get("user_text", ""):
                raise S45ReadRefusal("S45_USER_EVENT_TEXT_MISMATCH")
        else:
            episode = next(
                (row for row in self.episodes("U")
                 if row.get("episode_id") == body.get("user_episode_id")),
                None,
            )
            wanted = "DO" if kind == "DO_HELP" else "ATTEND"
            if not episode or episode.get("kind") != wanted:
                raise S45ReadRefusal("S45_USER_EPISODE_MISSING")
            if digest(episode.get("body") or {}) != body.get("user_episode_hash"):
                raise S45ReadRefusal("S45_USER_EPISODE_HASH_MISMATCH")
            if episode.get("body") != body.get("user_episode_body"):
                raise S45ReadRefusal("S45_USER_EPISODE_BODY_MISMATCH")

        speech_id = body.get("speech_event_id", "")
        action_id = body.get("action_event_id", "")
        admission_id = body.get("admission_id", "")
        status = body.get("status")
        if kind == "ATTEND":
            if status != "NO_CHANGE":
                raise S45ReadRefusal("S45_ATTEND_STATUS_INVALID", str(status))
            if (speech_id or action_id or body.get("language")
                    or admission_id or body.get("strategy")
                    or body.get("template_id")):
                raise S45ReadRefusal("S45_ATTEND_HAS_ACTOR_EFFECT")
        elif status == "UNSUPPORTED":
            if speech_id or action_id or body.get("language") or admission_id:
                raise S45ReadRefusal("S45_UNSUPPORTED_HAS_EFFECT")
            if body.get("strategy") or body.get("template_id"):
                raise S45ReadRefusal("S45_UNSUPPORTED_HAS_STRATEGY")
        elif status == "OK":
            if not speech_id:
                raise S45ReadRefusal("S45_OK_REQUIRES_SPEECH")
            if not admission_id:
                raise S45ReadRefusal("S45_ADMISSION_REQUIRED")
            admission_episode = next(
                (row for row in self.episodes("A")
                 if row.get("kind") == "EXPRESSION_ADMISSION"
                 and (row.get("body", {}).get("admission") or {}).get(
                     "admission_id") == admission_id),
                None,
            )
            if not admission_episode:
                raise S45ReadRefusal("S45_ADMISSION_MISSING")
            admission = admission_episode["body"]["admission"]
            candidate_episode = admission_episode["body"].get("candidate") or {}
            plan = admission.get("plan") or {}
            readset = plan.get("readset") or {}
            s45_plan = readset.get("s45") or {}
            if admission.get("schema") != "S45_USER_EXPRESSION_ADMISSION@1":
                raise S45ReadRefusal("S45_ADMISSION_SCHEMA_MISMATCH")
            if admission.get("s45_boundary") is not True:
                raise S45ReadRefusal("S45_ADMISSION_BOUNDARY_MISSING")
            if admission.get("r31e_strategy") != body.get("strategy"):
                raise S45ReadRefusal("S45_STRATEGY_ADMISSION_MISMATCH")
            if admission.get("r31e_template_id") != body.get("template_id"):
                raise S45ReadRefusal("S45_TEMPLATE_ADMISSION_MISMATCH")
            if plan.get("intent") != body.get("strategy"):
                raise S45ReadRefusal("S45_PLAN_INTENT_MISMATCH")
            if plan.get("plan_hash") != body.get("plan_hash"):
                raise S45ReadRefusal("S45_ADMISSION_PLAN_MISMATCH")
            if s45_plan.get("strategy") != body.get("strategy"):
                raise S45ReadRefusal("S45_PLAN_STRATEGY_MISMATCH")
            if s45_plan.get("template_id") != body.get("template_id"):
                raise S45ReadRefusal("S45_PLAN_TEMPLATE_MISMATCH")
            if candidate_episode.get("strategy") != body.get("strategy"):
                raise S45ReadRefusal("S45_CANDIDATE_STRATEGY_MISMATCH")
            if candidate_episode.get("template_id") != body.get("template_id"):
                raise S45ReadRefusal("S45_CANDIDATE_TEMPLATE_MISMATCH")
            if candidate_episode.get("speech") != body.get("native_text"):
                raise S45ReadRefusal("S45_CANDIDATE_TEXT_MISMATCH")
            if admission.get("speech_event_id") != speech_id:
                raise S45ReadRefusal("S45_ADMISSION_SPEECH_MISMATCH")
            if admission.get("action_event_id") != action_id:
                raise S45ReadRefusal("S45_ADMISSION_ACTION_MISMATCH")
            if admission.get("native_artifact", {}).get("text") != body.get("native_text"):
                raise S45ReadRefusal("S45_ADMISSION_NATIVE_MISMATCH")
            if admission.get("translation_artifact", {}).get("text") != body.get(
                    "translation_text"):
                raise S45ReadRefusal("S45_ADMISSION_TRANSLATION_MISMATCH")
            if (plan.get("unit") or {}).get("native_text") != body.get("native_text"):
                raise S45ReadRefusal("S45_PLAN_NATIVE_MISMATCH")
            event = self.event(speech_id)
            if not event or event.get("hash") != body.get("speech_event_hash"):
                raise S45ReadRefusal("S45_SPEECH_EVENT_MISSING")
            if event.get("actor_id") != "A" or event.get("kind") != "SPEECH":
                raise S45ReadRefusal("S45_SPEECH_EVENT_INVALID")
            if body.get("speech_event_kind") != "SPEECH":
                raise S45ReadRefusal("S45_SPEECH_KIND_MISMATCH")
            if event.get("body", {}).get("text", "") != body.get("native_text"):
                raise S45ReadRefusal("S45_SPEECH_TEXT_MISMATCH")
            lme = event.get("body", {}).get("lme") or {}
            if lme.get("plan_hash") != body.get("plan_hash"):
                raise S45ReadRefusal("S45_SPEECH_PLAN_MISMATCH")
            language = body.get("language") or {}
            if language.get("plan_hash") != body.get("plan_hash"):
                raise S45ReadRefusal("S45_LANGUAGE_PLAN_MISMATCH")
            if language.get("native_text") != body.get("native_text"):
                raise S45ReadRefusal("S45_LANGUAGE_NATIVE_MISMATCH")
            if language.get("translation_text") != body.get("translation_text"):
                raise S45ReadRefusal("S45_LANGUAGE_TRANSLATION_MISMATCH")
            if language.get("equivalence_status") != "ACCEPTED":
                raise S45ReadRefusal("S45_EQUIVALENCE_NOT_ACCEPTED")
            if language.get("s45_strategy") not in (None, body.get("strategy")):
                raise S45ReadRefusal("S45_LANGUAGE_STRATEGY_MISMATCH")
            if language.get("s45_template_id") not in (None, body.get("template_id")):
                raise S45ReadRefusal("S45_LANGUAGE_TEMPLATE_MISMATCH")
            source_refs = body.get("source_event_refs") or []
            access_ids = body.get("access_receipt_ids") or []
            if not source_refs or not access_ids:
                raise S45ReadRefusal("S45_SOURCE_OR_ACCESS_MISSING")
            for ref in source_refs:
                source = self.event(ref.get("event_id", ""))
                if not source or source.get("hash") != ref.get("event_hash"):
                    raise S45ReadRefusal("S45_SOURCE_EVENT_MISSING")
                if source.get("actor_id") != "B" or source.get("kind") != "SPEECH":
                    raise S45ReadRefusal("S45_SOURCE_EVENT_INVALID")
                if ref.get("branch_id") != self.branch_id:
                    raise S45ReadRefusal("S45_SOURCE_BRANCH_MISMATCH")
                if ref.get("event_id") not in evidence["sources"]:
                    raise S45ReadRefusal("S45_SOURCE_NOT_ROOT_EVIDENCE")
            for receipt in access_ids:
                if receipt not in evidence["access"]:
                    raise S45ReadRefusal("S45_ACCESS_NOT_ROOT_EVIDENCE")
            view = self.language_view(speech_id, locale="en")
            if view.get("status") != "OK" or view.get("display_mode") != "LABELED_ENGLISH":
                raise S45ReadRefusal("S45_LANGUAGE_VIEW_MISSING")
            if view.get("translation_text") != body.get("translation_text"):
                raise S45ReadRefusal("S45_LANGUAGE_VIEW_TEXT_MISMATCH")
            if action_id:
                action = self.event(action_id)
                if not action or action.get("hash") != body.get("action_event_hash"):
                    raise S45ReadRefusal("S45_ACTION_EVENT_MISSING")
                if action.get("actor_id") != "A":
                    raise S45ReadRefusal("S45_ACTION_ACTOR_MISMATCH")
                if action.get("kind") != body.get("action_event_kind"):
                    raise S45ReadRefusal("S45_ACTION_KIND_MISMATCH")
        else:
            raise S45ReadRefusal("S45_STATUS_INVALID", str(status))
        c9 = self._c9_lineage()
        if not c9 or c9.get("target_branch") != "NO_CHANGE":
            raise S45ReadRefusal("S45_C9_LINEAGE_MISSING")
        return body

    def read_encounters(self) -> list[dict]:
        rows = []
        for row in self.product.store.episodes(self.branch_id):
            if row.get("kind") != ENCOUNTER_KIND:
                continue
            body = dict(row.get("body") or {})
            body["encounter_id"] = row.get("episode_id", "")
            body["clock"] = row.get("clock", body.get("clock", 0))
            body = self._validate_encounter(body)
            body["current_access"] = self._current_access(
                list(body.get("access_receipt_ids") or [])
            )
            body["c9_lineage"] = self._c9_lineage()
            rows.append(body)
        return rows

    def _encounter_summary(self, body: dict, index: int) -> dict:
        return {
            "schema": "SOROK_S45_USER_ENCOUNTER_EVENT@1",
            "status": body.get("status"),
            "event_ordinal": 1_000_000 + index,
            "e1_event_id": body.get("encounter_id") or body.get("user_event_id", ""),
            "e1_event_hash": body.get("encounter_hash") or body.get("user_event_hash", ""),
            "source_operation": "USER_" + str(body.get("kind", "")),
            "selected_option": body.get("strategy"),
            "attempt_status": body.get("status"),
            "performed": False,
            "action_event_kind": "",
            "target_proposals": [],
            "s45": body,
            "c9": body.get("c9_lineage"),
        }

    def read_events(self) -> list[dict]:
        events = list(super().read_events())
        encounters = self.read_encounters()
        events.extend(
            self._encounter_summary(body, index)
            for index, body in enumerate(encounters, start=1)
        )
        return events

    def read_event(self, event_ref: str) -> dict:
        encounters = self.read_encounters()
        for body in encounters:
            if event_ref in {
                body.get("encounter_id"), body.get("user_event_id"),
                body.get("speech_event_id"), body.get("action_event_id"),
            }:
                return self._encounter_summary(body, 1)
        return super().read_event(event_ref)

    def read_latest(self) -> dict:
        base = super().read_latest()
        encounters = self.read_encounters()
        if encounters:
            last = encounters[-1]
            if int(last.get("clock", 0)) >= int(base.get("event_time", 0)):
                return self._encounter_summary(last, len(encounters))
        return base

    def _surface(self, event_ids):
        lines = super()._surface(event_ids)
        binding = self._last_language or {}
        for event_id in event_ids:
            event = self.event(event_id)
            if not event or binding.get("speech_event_id") != event_id:
                continue
            view = self.language_view(event_id, locale="en")
            if view.get("translation_status") == "AVAILABLE":
                lines.append(
                    '[labeled English view, not actor speech: "'
                    + view.get("translation_text", "") + '"]'
                )
        return lines

    def _projection_verification(self, event, lme, projection):
        original_pairs, original_atoms = (
            s40_session.S40_PAIRS, s40_session.S40_ATOMS
        )
        s40_session.S40_PAIRS = {**original_pairs, **PAIRS}
        s40_session.S40_ATOMS = set(original_atoms) | set(ATOMS)
        try:
            return S40GeneratedSession._projection_verification(
                self, event, lme, projection
            )
        finally:
            s40_session.S40_PAIRS = original_pairs
            s40_session.S40_ATOMS = original_atoms

    def verify(self) -> dict:
        try:
            result = super().verify()
        except Exception as exc:
            result = {"ok": False, "error": type(exc).__name__ + ":" + str(exc)}
        try:
            encounters = self.read_encounters()
            result["s45_encounters"] = {
                "status": "OK",
                "count": len(encounters),
                "kinds": [row.get("kind") for row in encounters],
                "current_access": {
                    row.get("encounter_id"): row.get("current_access", {})
                    for row in encounters
                },
            }
            s45_ok = True
        except (S45ReadRefusal, S45Refusal, KeyError, OSError, ValueError) as exc:
            result["s45_encounters"] = {
                "status": "REFUSED", "code": getattr(exc, "code", str(exc)),
            }
            s45_ok = False
        result["ok"] = bool(result.get("ok")) and s45_ok
        return result


__all__ = [
    "S45_SCHEMA", "S45Session", "S45ReadRefusal", "ENCOUNTER_KIND",
    "S45_BINDING_SCHEMA",
]
