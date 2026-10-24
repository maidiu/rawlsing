"""Small adapter over the real JoinedSession.

Existing exact-template expression remains the default.  Only an explicitly
bound branch+actor uses the separately versioned multilingual path.  The
adapter inherits ``JoinedSession.start/open/say`` and the existing C12
event/episode/checkpoint writer.  It never creates a second actor root, a
parallel ledger or psychological memory.
"""
from __future__ import annotations

import json

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402
from bp4.world import make_event  # noqa: E402
from joined.session import JoinedSession  # noqa: E402
from r30a.first_session import SessionRefusal  # noqa: E402
from r31e import expression  # noqa: E402

from .artifacts import (  # noqa: E402
    build_native_artifact,
    build_translation_artifact,
)
from .atoms import pair_for_unit  # noqa: E402
from .equivalence import evaluate_pair  # noqa: E402
from .index import (  # noqa: E402
    ENCOUNTER_SCHEMA,
    LanguageRefusal,
    build_index,
    invalidate_index,
    persist_index_cache,
)
from .plan import COMPETENCE_SCHEMA, compile_plan  # noqa: E402

PORT_SCHEMA = "LME_JOINED_MULTILINGUAL_PORT@1"
PORT_VERSION = 1
ADMISSION_SCHEMA = "LME_MULTILINGUAL_EXPRESSION_ADMISSION@1"
CANDIDATE_SCHEMA = "LME_MULTILINGUAL_EXPRESSION_CANDIDATE@1"
BINDING_SCHEMA = "LME_MEDIATION_BINDING@1"
PROJECTION_SCHEMA = "LME_TRANSLATION_PROJECTION@1"
SAY_RECEIPT_SCHEMA = "LME_MEDIATED_SAY_RECEIPT@1"
GRADE = "TEST_ONLY_SOURCEFREE_LANGUAGE_MEDIATION_NOT_NATIVE"


class MediatedJoinedSession(JoinedSession):
    """One same-person JOIN-E session with an optional multilingual adapter."""

    # ------------------------------------------------------------------
    # explicit TEST_ONLY declarations / encounters
    # ------------------------------------------------------------------
    def declare_language_competence(self, actor_id: str, language_tag: str,
                                    *, basis: str = "EXPLICIT_TEST_ONLY_DECLARATION"):
        if basis != "EXPLICIT_TEST_ONLY_DECLARATION":
            raise LanguageRefusal("COMPETENCE_BASIS_NOT_TEST_ONLY", basis)
        branch = self.product.store.branch(self.branch_id)
        if actor_id not in branch["actor_ids"]:
            raise LanguageRefusal("COMPETENCE_ACTOR_NOT_IN_BRANCH", actor_id)
        body = {
            "schema": COMPETENCE_SCHEMA,
            "grade": GRADE,
            "native": False,
            "actor_id": actor_id,
            "language_tag": language_tag,
            "basis": basis,
            "inferred_from_demographics": False,
            "product_model_calls": 0,
        }
        episode = self.product._append_episode(
            self.branch_id, "A", "LANGUAGE_COMPETENCE", self.clock(), body)
        self.product._checkpoint(self.branch_id, self.clock(), self.world())
        return episode

    def append_test_only_access_receipt(self, source_event_id: str, *,
                                        actor_id: str = "A",
                                        declared_hash: str | None = None,
                                        declared_branch: str | None = None,
                                        access: str = "OBSERVED_HEARING",
                                        record_perception: bool = True):
        event = self.event(source_event_id)
        if not event:
            raise LanguageRefusal("SOURCE_EVENT_MISSING", source_event_id)
        receipt = {
            "schema": "LME_SOURCE_ACCESS@1",
            "grade": GRADE,
            "native": False,
            "source_event_id": source_event_id,
            "source_event_hash": declared_hash or event["hash"],
            "branch_id": declared_branch or self.branch_id,
            "actor_id": actor_id,
            "access": access,
            "clock": self.clock(),
            "product_model_calls": 0,
        }
        receipt["receipt_id"] = "LME_ACCESS_" + digest(receipt)
        if record_perception:
            self.product.store.record_perception(
                self.branch_id, actor_id=actor_id, event_id=source_event_id,
                clock=self.clock(), channel=access.lower())
        episode = self.product._append_episode(
            self.branch_id, "A", "LANGUAGE_ACCESS", self.clock(),
            {"receipt": receipt})
        return {"receipt": receipt, "episode": episode}

    def admit_language_event(self, text: str, *, speaker_actor: str = "B",
                             language_tag: str = "es-MX",
                             access_declared_hash: str | None = None,
                             access_declared_branch: str | None = None,
                             record_access: bool = True):
        if not text.strip():
            raise LanguageRefusal("EMPTY_SOURCE_SPEECH")
        branch = self.product.store.branch(self.branch_id)
        if speaker_actor not in branch["actor_ids"]:
            raise LanguageRefusal("SOURCE_SPEAKER_NOT_IN_BRANCH", speaker_actor)
        world = self.world()
        event = make_event(
            clock=world.clock, kind="SPEECH", actor_id=speaker_actor,
            location=world.positions.get(speaker_actor, "workshop"),
            summary=f"{speaker_actor} says: {text.strip()}",
            body={
                "text": text.strip(),
                "language_tag": language_tag,
                "observable": True,
                "source_grade": "TEST_ONLY_INVENTED_LANGUAGE_EVENT",
            },
            sequence=len(world.events),
        )
        world.add_event(event)
        self._append_event(event, perceive=(speaker_actor,))
        self._perceive_if_present(event, "A", "U")
        self.product._append_episode(
            self.branch_id, speaker_actor, "SAY", world.clock,
            {"event_id": event["event_id"], "text": text.strip(),
             "language_tag": language_tag,
             "source_grade": "TEST_ONLY_INVENTED_LANGUAGE_EVENT",
             "action_seq": self._action_seq()})
        access = self.append_test_only_access_receipt(
            event["event_id"], declared_hash=access_declared_hash,
            declared_branch=access_declared_branch,
            record_perception=record_access)
        self.product._checkpoint(self.branch_id, world.clock, world)
        return {"event": event, "access": access}

    def admit_language_encounter(self, *, text: str, concept_id: str,
                                 milieu_id: str, sense_id: str,
                                 relation_label: str, atoms: list[str],
                                 language_tag: str = "es-MX",
                                 speaker_actor: str = "B",
                                 counterexample_event_ids: tuple[str, ...] = (),
                                 access_declared_hash: str | None = None,
                                 access_declared_branch: str | None = None,
                                 record_access: bool = True):
        source = self.admit_language_event(
            text, speaker_actor=speaker_actor, language_tag=language_tag,
            access_declared_hash=access_declared_hash,
            access_declared_branch=access_declared_branch,
            record_access=record_access)
        event = source["event"]
        refs = []
        for ref in counterexample_event_ids:
            counter = self.event(ref)
            if not counter:
                raise LanguageRefusal("COUNTEREXAMPLE_EVENT_MISSING", ref)
            refs.append({"event_id": ref, "event_hash": counter["hash"]})
        body = {
            "schema": ENCOUNTER_SCHEMA,
            "grade": GRADE,
            "native": False,
            "actor_id": "A",
            "branch_id": self.branch_id,
            "concept_id": concept_id,
            "milieu_id": milieu_id,
            "sense_id": sense_id,
            "relation_label": relation_label,
            "atoms": sorted(set(atoms)),
            "language_tag": language_tag,
            "source_event_id": event["event_id"],
            "source_event_hash": event["hash"],
            "access_receipt_id": source["access"]["receipt"]["receipt_id"],
            "counterexample_event_refs": refs,
            "product_model_calls": 0,
        }
        body["encounter_id"] = "LME_ENC_" + digest(body)
        episode = self.product._append_episode(
            self.branch_id, "A", "LANGUAGE_ENCOUNTER", self.clock(), body)
        self.product._checkpoint(self.branch_id, self.clock(), self.world())
        return {"encounter": body, "episode": episode,
                "event": event, "access": source["access"]}

    def _access_receipt_ids(self) -> set[str]:
        ids: set[str] = set()
        for episode in self.episodes():
            if episode.get("kind") != "LANGUAGE_ACCESS":
                continue
            body = episode.get("body", {})
            receipt = body.get("receipt") or body
            if receipt.get("receipt_id"):
                ids.add(receipt["receipt_id"])
        return ids

    def revoke_language_access(self, receipt_id: str, *,
                               reason: str = "TEST_ONLY_SEVERANCE"):
        if receipt_id not in self._access_receipt_ids():
            raise LanguageRefusal("ACCESS_RECEIPT_UNKNOWN", receipt_id)
        body = {
            "schema": "LME_SOURCE_ACCESS_REVOCATION@1",
            "receipt_id": receipt_id,
            "reason": reason,
            "branch_id": self.branch_id,
            "clock": self.clock(),
            "product_model_calls": 0,
        }
        episode = self.product._append_episode(
            self.branch_id, "A", "LANGUAGE_ACCESS_REVOKED", self.clock(), body)
        invalidate_index(self, reason=reason, changed_ref=receipt_id)
        self.product._checkpoint(self.branch_id, self.clock(), self.world())
        return episode

    def restore_language_access(self, receipt_id: str, *,
                                reason: str = "TEST_ONLY_RESTORE"):
        if receipt_id not in self._access_receipt_ids():
            raise LanguageRefusal("ACCESS_RECEIPT_UNKNOWN", receipt_id)
        body = {
            "schema": "LME_SOURCE_ACCESS_RESTORATION@1",
            "receipt_id": receipt_id,
            "reason": reason,
            "branch_id": self.branch_id,
            "clock": self.clock(),
            "product_model_calls": 0,
        }
        episode = self.product._append_episode(
            self.branch_id, "A", "LANGUAGE_ACCESS_RESTORED", self.clock(), body)
        self.product._checkpoint(self.branch_id, self.clock(), self.world())
        return episode

    # ------------------------------------------------------------------
    # binding / index / plan
    # ------------------------------------------------------------------
    def enable_mediation(self, *, trigger_kinds=("SAY",),
                         display_locale: str = "en"):
        index = build_index(self, actor_id="A")
        persist_index_cache(self, index)
        body = {
            "schema": BINDING_SCHEMA,
            "grade": GRADE,
            "native": False,
            "port": {"schema": PORT_SCHEMA, "version": PORT_VERSION},
            "baseline_port": expression.PORT_SCHEMA,
            "actor_id": "A",
            "branch_id": self.branch_id,
            "trigger_kinds": list(trigger_kinds),
            "display_policy": "SOURCE_PLUS_LABELED_AUXILIARY",
            "index_hash": index["index_hash"],
            "index_readset_hash": index["readset_hash"],
            "product_model_calls": 0,
        }
        episode = self.product._append_episode(
            self.branch_id, "A", "LANGUAGE_MEDIATION_BINDING",
            self.clock(), body)
        self.meta["display_locale"] = display_locale
        self._save_join_meta()
        self.product._checkpoint(self.branch_id, self.clock(), self.world())
        return {"binding": body, "episode": episode, "index": index}

    def mediation_binding(self) -> dict | None:
        for episode in reversed(self.episodes()):
            if episode.get("kind") != "LANGUAGE_MEDIATION_BINDING":
                continue
            body = episode.get("body", {})
            if body.get("branch_id") != self.branch_id:
                return None
            if body.get("actor_id") != "A":
                continue
            return body
        return None

    def language_index(self) -> dict:
        return build_index(self, actor_id="A")

    def expression_plan(self, *, trigger_kind: str = "SAY",
                        text: str = ""):
        contract = expression.compile_contract(
            self, trigger_kind=trigger_kind, trigger_text=text)
        index = build_index(self, actor_id="A")
        plan = compile_plan(self, index, contract,
                            trigger_kind=trigger_kind, trigger_text=text)
        return plan

    def display_locale(self) -> str:
        return self.meta.get("display_locale", "en")

    def set_display_locale(self, locale: str) -> None:
        self.meta["display_locale"] = locale
        self._save_join_meta()

    # ------------------------------------------------------------------
    # inherited say/open flow plus the separately versioned path
    # ------------------------------------------------------------------
    def say(self, text: str) -> dict:
        self._last_language = None
        result = super().say(text)
        result["language"] = self._last_language
        result["product_model_calls"] = 0
        return result

    def _respond(self, kind: str, text: str = "", event_id: str = "") -> dict:
        self._last_language = None
        binding = self.mediation_binding()
        if not binding or kind not in binding.get("trigger_kinds", []):
            return super()._respond(kind, text=text, event_id=event_id)

        contract = expression.compile_contract(
            self, trigger_kind=kind, trigger_text=text,
            trigger_event_id=event_id)
        index = build_index(self, actor_id="A")
        plan = compile_plan(self, index, contract,
                            trigger_kind=kind, trigger_text=text)
        native = build_native_artifact(plan)
        translation = build_translation_artifact(plan, native)
        receipt = evaluate_pair(plan, native, translation)
        if receipt.get("status") != "ACCEPTED":
            raise SessionRefusal(
                "LANGUAGE_EQUIVALENCE_" + str(receipt.get("status")),
                json.dumps({"codes": receipt.get("codes", []),
                            "plan_hash": plan.plan_hash}, sort_keys=True))

        world = self.world()
        candidate = self._candidate(plan, native)
        admission_id = digest({
            "candidate": candidate,
            "contract_hash": contract.get("contract_hash", ""),
            "plan_hash": plan.plan_hash,
            "native_artifact_hash": native["artifact_hash"],
            "translation_artifact_hash": translation["artifact_hash"],
            "clock": world.clock,
        })
        event = self._write_speech_event(
            plan, native, translation, receipt, contract,
            candidate, admission_id)
        admission = self._admission(
            plan, native, translation, receipt, contract, event,
            candidate, admission_id, index)
        self.product._append_episode(
            self.branch_id, "A", "SAY", world.clock,
            {"event_id": event["event_id"], "text": native["text"],
             "language_tag": native["language_tag"],
             "gesture": candidate["gesture"], "tone": candidate["tone"],
             "strategy": candidate["strategy"],
             "contract_hash": contract.get("contract_hash", ""),
             "admission_id": admission_id,
             "plan_hash": plan.plan_hash,
             "spans": event["body"]["spans"]})
        self.product._append_episode(
            self.branch_id, "A", "EXPRESSION_ADMISSION", world.clock,
            {"admission": admission, "candidate": candidate,
             "plan": plan.public(),
             "contract_hash": contract.get("contract_hash", ""),
             "multilingual_port": {"schema": PORT_SCHEMA,
                                   "version": PORT_VERSION}})
        projection = self._write_translation_projection(
            event, plan, native, translation, receipt)
        self.product._checkpoint(self.branch_id, world.clock, world)

        self._last_language = {
            "schema": SAY_RECEIPT_SCHEMA,
            "grade": GRADE,
            "native": False,
            "plan": plan.public(),
            "index_hash": index["index_hash"],
            "index_readset_hash": index["readset_hash"],
            "index_cache_status": index["cache_status"],
            "cache_invalidated": index["cache_status"] == "CACHE_INVALID",
            "native_artifact": native,
            "translation_artifact": translation,
            "equivalence": receipt,
            "source_event_id": event["event_id"],
            "source_event_hash": event["hash"],
            "source_dependent": bool(plan.unit["source_dependent"]),
            "source_dependent_refused": bool(plan.fallback),
            "fallback": bool(plan.fallback),
            "fallback_reason": plan.fallback_reason,
            "projection_episode_id": projection["episode_id"],
            "product_model_calls": 0,
        }
        return {
            "admission": admission,
            "candidate": candidate,
            "event_ids": [event["event_id"]],
            "contact": "",
            "contract": contract,
        }

    def _candidate(self, plan, native: dict) -> dict:
        return {
            "schema": CANDIDATE_SCHEMA,
            "grade": GRADE,
            "native": False,
            "strategy": plan.intent,
            "template_id": "lme:" + plan.unit["unit_id"],
            "slots": {},
            "speech": native["text"],
            "language_tag": native["language_tag"],
            "gesture": plan.unit["gesture"],
            "tone": plan.unit["tone"],
            "action": "NONE",
            "facts": [{
                "kind": "LANGUAGE_SOURCE_RELATION",
                "relation_ids": list(plan.supporting_relation_ids),
            }],
            "contact": "",
            "knowledge_refs": [],
            "variant": 0,
            "plan_hash": plan.plan_hash,
            "fallback": bool(plan.fallback),
            "fallback_reason": plan.fallback_reason,
        }

    def _write_speech_event(self, plan, native: dict, translation: dict,
                            receipt: dict, contract: dict, candidate: dict,
                            admission_id: str) -> dict:
        world = self.world()
        event = make_event(
            clock=world.clock, kind="SPEECH", actor_id="A",
            location=world.positions.get("A", "workshop"),
            summary=f"A says: {native['text']}",
            body={
                "text": native["text"],
                "language_tag": native["language_tag"],
                "spans": [{
                    "language_tag": native["language_tag"],
                    "text": native["text"],
                    "span_role": "SPOKEN",
                }],
                "gesture": candidate["gesture"],
                "tone": candidate["tone"],
                "strategy": candidate["strategy"],
                "contract_hash": contract.get("contract_hash", ""),
                "admission_id": admission_id,
                "lme": {
                    "schema": "LME_ADMITTED_SPEECH_OCCURRENCE@1",
                    "grade": GRADE,
                    "native": False,
                    "plan_hash": plan.plan_hash,
                    "native_artifact_hash": native["artifact_hash"],
                    "translation_artifact_hash": translation["artifact_hash"],
                    "equivalence_receipt_hash": receipt.get("receipt_hash", ""),
                    "equivalence_status": receipt.get("status"),
                    "source_event_refs": plan.readset["source_event_refs"],
                    "access_receipt_ids": plan.readset["access_receipt_ids"],
                    "product_model_calls": 0,
                },
            },
            sequence=len(world.events),
        )
        world.add_event(event)
        self._append_event(event, perceive=("A",))
        self._perceive_if_present(event, "U", "B")
        return event

    def _admission(self, plan, native: dict, translation: dict, receipt: dict,
                   contract: dict, event: dict, candidate: dict,
                   admission_id: str, index: dict) -> dict:
        return {
            "schema": ADMISSION_SCHEMA,
            "grade": GRADE,
            "native": False,
            "port": {"schema": PORT_SCHEMA, "version": PORT_VERSION,
                     "baseline_port": expression.PORT_SCHEMA,
                     "live_actor_model": "LIVE_ACTOR_MODEL_NOT_RUN"},
            "admission_id": admission_id,
            "strategy": candidate["strategy"],
            "template_id": candidate["template_id"],
            "contract_hash": contract.get("contract_hash", ""),
            "source_ref": contract.get("source_ref"),
            "target_id": contract.get("source", {}).get("target_id", ""),
            "consumed_state_hash": contract.get("source", {}).get(
                "consumed_state_hash", ""),
            "branch_id": self.branch_id,
            "clock": self.clock(),
            "speech_event_id": event["event_id"],
            "speech_event_hash": event["hash"],
            "action_event_id": "",
            "contact_outcome": "",
            "plan": plan.public(),
            "native_artifact": native,
            "translation_artifact": translation,
            "equivalence": receipt,
            "custody": {
                "contract_hash": contract.get("contract_hash", ""),
                "source_ref": contract.get("source_ref"),
                "target_id": contract.get("source", {}).get("target_id", ""),
                "consumed_state_hash": contract.get("source", {}).get(
                    "consumed_state_hash", ""),
                "branch_id": self.branch_id,
                "index_hash": index["index_hash"],
                "index_readset_hash": index["readset_hash"],
            },
            "validation": {
                "branch_match": plan.branch_id == self.branch_id,
                "index_cache_status": index["cache_status"],
                "plan_before_wording": True,
                "equivalence_status": receipt.get("status"),
                "source_dependent_unit_authorized": not plan.fallback,
                "user_access_preserved": True,
                "locale_or_attention_changed_actor": False,
                "product_model_calls": 0,
            },
            "source_dependent": bool(plan.unit["source_dependent"]),
            "source_dependent_refused": bool(plan.fallback),
            "fallback": bool(plan.fallback),
            "fallback_reason": plan.fallback_reason,
            "attention_excluded": True,
            "motive_status": "MOTIVE_UNDERDETERMINED",
            "product_model_calls": 0,
        }

    def _write_translation_projection(self, event: dict, plan, native: dict,
                                      translation: dict, receipt: dict) -> dict:
        body = {
            "schema": PROJECTION_SCHEMA,
            "grade": GRADE,
            "native": False,
            "status": "DERIVED_CACHE",
            "source_speech_event_id": event["event_id"],
            "source_event_hash": event["hash"],
            "source_event_ref": event["event_id"],
            "source_utterance_hash": event["hash"],
            "plan_hash": plan.plan_hash,
            "native_artifact_hash": native["artifact_hash"],
            "translation_artifact_hash": translation["artifact_hash"],
            "equivalence_receipt": receipt,
            "target_language_tag": translation["target_language_tag"],
            "text": translation["text"],
            "render_mode": "LABELED_ENGLISH_AUXILIARY",
            "not_actor_speech": True,
            "product_model_calls": 0,
        }
        return self.product._append_episode(
            self.branch_id, "A", "LANGUAGE_TRANSLATION_PROJECTION",
            self.clock(), body)

    # ------------------------------------------------------------------
    # read-only auxiliary view after actual admission
    # ------------------------------------------------------------------
    def _projection(self, event_id: str) -> dict | None:
        for episode in reversed(self.episodes()):
            if episode.get("kind") != "LANGUAGE_TRANSLATION_PROJECTION":
                continue
            body = episode.get("body", {})
            if body.get("source_speech_event_id") == event_id:
                return body
        return None

    def _admission_for(self, plan_hash: str, event_id: str) -> dict | None:
        for episode in reversed(self.episodes()):
            if episode.get("kind") != "EXPRESSION_ADMISSION":
                continue
            body = episode.get("body", {})
            admission = body.get("admission") or {}
            if (admission.get("speech_event_id") == event_id
                    and (admission.get("plan") or {}).get("plan_hash")
                    == plan_hash):
                return admission
        return None

    def _projection_verification(self, event: dict, lme: dict,
                                 projection: dict) -> dict:
        """Re-bind a cached projection to its admitted event and artifacts."""
        event_id = event.get("event_id", "")
        if projection.get("schema") != PROJECTION_SCHEMA:
            return {"ok": False, "reason": "PROJECTION_SCHEMA_MISMATCH"}
        if projection.get("source_speech_event_id") != event_id:
            return {"ok": False, "reason": "PROJECTION_SOURCE_EVENT_MISMATCH"}
        if projection.get("source_event_hash") != event.get("hash", ""):
            return {"ok": False, "reason": "PROJECTION_SOURCE_HASH_MISMATCH"}
        if projection.get("plan_hash") != lme.get("plan_hash", ""):
            return {"ok": False, "reason": "PROJECTION_PLAN_HASH_MISMATCH"}
        if (projection.get("native_artifact_hash")
                != lme.get("native_artifact_hash", "")):
            return {"ok": False, "reason": "PROJECTION_NATIVE_HASH_MISMATCH"}
        if (projection.get("translation_artifact_hash")
                != lme.get("translation_artifact_hash", "")):
            return {"ok": False,
                    "reason": "PROJECTION_TRANSLATION_HASH_MISMATCH"}
        receipt = projection.get("equivalence_receipt") or {}
        if receipt.get("status") != "ACCEPTED":
            return {"ok": False,
                    "reason": "EQUIVALENCE_" + str(receipt.get("status"))}
        if receipt.get("receipt_hash") != lme.get("equivalence_receipt_hash", ""):
            return {"ok": False,
                    "reason": "PROJECTION_EQUIVALENCE_HASH_MISMATCH"}
        admission = self._admission_for(lme.get("plan_hash", ""), event_id)
        if not admission:
            return {"ok": False, "reason": "PROJECTION_ADMISSION_MISSING"}
        native = admission.get("native_artifact") or {}
        translation = admission.get("translation_artifact") or {}
        if native.get("artifact_hash") != projection.get("native_artifact_hash"):
            return {"ok": False, "reason": "PROJECTION_NATIVE_ARTIFACT_MISMATCH"}
        if (translation.get("artifact_hash")
                != projection.get("translation_artifact_hash")):
            return {"ok": False,
                    "reason": "PROJECTION_TRANSLATION_ARTIFACT_MISMATCH"}
        if translation.get("text") != projection.get("text"):
            return {"ok": False, "reason": "PROJECTION_TEXT_MISMATCH"}
        recheck = evaluate_pair(admission.get("plan") or {}, native, translation)
        if recheck.get("status") != "ACCEPTED":
            return {"ok": False,
                    "reason": "PROJECTION_EQUIVALENCE_"
                              + str(recheck.get("status"))}
        if recheck.get("receipt_hash") != receipt.get("receipt_hash"):
            return {"ok": False,
                    "reason": "PROJECTION_EQUIVALENCE_RECEIPT_MISMATCH"}
        return {"ok": True}

    def language_view(self, event_id: str, *, locale: str | None = None,
                      attention: str | None = None,
                      fail_translation: bool = False) -> dict:
        event = self.event(event_id)
        if not event:
            return {"status": "EVENT_NOT_FOUND", "source_event_id": event_id,
                    "source_preserved": True, "product_model_calls": 0}
        if event_id not in self.user_perceived_ids():
            return {"status": "NOT_PERCEIVED", "source_event_id": event_id,
                    "source_event_hash": event.get("hash", ""),
                    "source_preserved": True,
                    "display_mode": "SOURCE_ORIGINAL",
                    "product_model_calls": 0}
        body = event.get("body", {})
        lme = body.get("lme")
        if not lme:
            return {"status": "NOT_MEDIATED", "source_event_id": event_id,
                    "source_event_hash": event.get("hash", ""),
                    "source_text": body.get("text", ""),
                    "source_preserved": True,
                    "display_mode": "SOURCE_ORIGINAL",
                    "product_model_calls": 0}
        locale = locale or self.display_locale()
        attention = attention or self.meta.get("attention", "focused")
        base = {
            "schema": "LME_LANGUAGE_VIEW@1",
            "grade": GRADE,
            "native": False,
            "source_event_id": event_id,
            "source_event_hash": event.get("hash", ""),
            "source_text": body.get("text", ""),
            "source_language_tags": [span.get("language_tag", "")
                                     for span in body.get("spans", [])],
            "plan_hash": lme.get("plan_hash", ""),
            "attention": attention,
            "locale": locale,
            "attention_changed_actor": False,
            "locale_changed_actor": False,
            "product_model_calls": 0,
        }
        if locale in {"es", "source", "SOURCE_ORIGINAL"}:
            return {**base, "status": "OK", "display_mode": "SOURCE_ORIGINAL",
                    "translation_status": "NOT_REQUESTED"}
        if locale not in {"en", "english", "ENGLISH_TRANSLATION",
                          "dual", "DUAL"}:
            return {**base, "status": "UNRESOLVED",
                    "display_mode": "TRANSLATION_UNAVAILABLE",
                    "translation_status": "UNRESOLVED_TARGET_LOCALE",
                    "source_preserved": True}
        if fail_translation:
            return {**base, "status": "OK",
                    "display_mode": "TRANSLATION_UNAVAILABLE",
                    "translation_status": "TRANSLATION_UNAVAILABLE",
                    "translation_failure": "EXPLICIT_DISPLAY_FAILURE",
                    "source_preserved": True}
        projection = self._projection(event_id)
        if not projection:
            return {**base, "status": "OK",
                    "display_mode": "TRANSLATION_UNAVAILABLE",
                    "translation_status": "PROJECTION_MISSING",
                    "source_preserved": True}
        verification = self._projection_verification(event, lme, projection)
        if not verification["ok"]:
            return {**base, "status": "UNRESOLVED",
                    "display_mode": "TRANSLATION_UNAVAILABLE",
                    "translation_status": verification["reason"],
                    "source_preserved": True}
        receipt = projection.get("equivalence_receipt", {})
        return {
            **base,
            "status": "OK",
            "display_mode": ("DUAL" if locale in {"dual", "DUAL"}
                             else "LABELED_ENGLISH"),
            "translation_status": "AVAILABLE",
            "translation_text": projection.get("text", ""),
            "translation_label": "labeled English auxiliary view; not actor speech",
            "native_artifact_hash": projection.get("native_artifact_hash", ""),
            "translation_artifact_hash": projection.get(
                "translation_artifact_hash", ""),
            "equivalence": receipt,
            "source_preserved": True,
        }

    def _surface(self, event_ids):
        lines = super()._surface(event_ids)
        if not self.mediation_binding():
            return lines
        for event_id in event_ids:
            event = self.event(event_id)
            if not event or event.get("kind") != "SPEECH":
                continue
            if event.get("actor_id") != "A":
                continue
            if "lme" not in event.get("body", {}):
                continue
            view = self.language_view(event_id)
            if view.get("display_mode") == "SOURCE_ORIGINAL":
                continue
            if view.get("translation_status") == "AVAILABLE":
                lines.append(
                    '[labeled English view, not actor speech: "'
                    + view.get("translation_text", "") + '"]')
            else:
                lines.append(
                    "[labeled English view unavailable; source original preserved.]")
        return lines

    # ------------------------------------------------------------------
    # public status
    # ------------------------------------------------------------------
    def status(self) -> dict:
        result = super().status()
        binding = self.mediation_binding()
        index = None
        if binding:
            try:
                index = build_index(self, actor_id="A")
            except LanguageRefusal:
                index = None
        result["multilingual_port"] = {
            "schema": PORT_SCHEMA,
            "version": PORT_VERSION,
            "baseline_port": expression.PORT_SCHEMA,
            "bound": bool(binding),
            "display_locale": self.display_locale(),
            "index_cache_status": index["cache_status"] if index else "",
            "product_model_calls": 0,
        }
        return result


__all__ = [
    "MediatedJoinedSession",
    "PORT_SCHEMA",
    "PORT_VERSION",
    "ADMISSION_SCHEMA",
    "CANDIDATE_SCHEMA",
    "PROJECTION_SCHEMA",
    "BINDING_SCHEMA",
    "GRADE",
]
