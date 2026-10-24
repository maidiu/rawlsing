"""Read the S40 generated native-speech/plan/projection/C9 binding."""
from __future__ import annotations

from typing import Any

from .bootstrap import install

install()

from candidate import valid  # noqa: E402
from s39.model import PROVENANCE  # noqa: E402

from .performer import SPEAKING_OPTIONS  # noqa: E402

GRADE = "TEST_ONLY_S40_GENERATED_INTENT_LANGUAGE_MODEL_PREMISE_NOT_GENERAL_TRANSLATION"


class S40ReadRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def _episode_by_id(session, episode_id: str) -> dict | None:
    for row in session.product.store.episodes(session.branch_id):
        if row.get("episode_id") == episode_id:
            return dict(row.get("body") or {})
    return None


def read_s40(session) -> dict:
    generation = session.read_generation()
    attempt = generation["attempt"]
    receipt = generation["generation"]
    option = generation["selected_option"]
    performed = bool(generation["performed"])
    s36 = generation["s36"]
    if s36["target_branch"] != "NO_CHANGE" or s36["target_reason"] != "NO_PROPOSAL":
        raise S40ReadRefusal("S40_S36_TARGET_NOT_NO_CHANGE")
    if s36["target_proposals"] != [] or s36["target_state_rows"] != 0:
        raise S40ReadRefusal("S40_S36_TARGET_PRESENT")

    language = attempt.get("language")
    if option in SPEAKING_OPTIONS and performed:
        if not isinstance(language, dict) or not valid(dict(language)):
            raise S40ReadRefusal("S40_GENERATED_LANGUAGE_BINDING_MISSING")
        language = dict(language)
        if language.get("schema") != "S40_GENERATED_LANGUAGE_BINDING@1":
            raise S40ReadRefusal("S40_LANGUAGE_SCHEMA_MISMATCH")
        if language.get("grade") != GRADE:
            raise S40ReadRefusal("S40_LANGUAGE_GRADE_MISMATCH")
        if language.get("provenance") != "TEST_ONLY_CONSTRUCTIVE_GENERATION_NOT_EXTERNALLY_OBSERVED":
            raise S40ReadRefusal("S40_LANGUAGE_PROVENANCE_MISMATCH")
        if language.get("private_generation_sources_in_plan") is not False:
            raise S40ReadRefusal("S40_PRIVATE_SOURCES_IN_PLAN")
        if language.get("target_proposals") != []:
            raise S40ReadRefusal("S40_LANGUAGE_TARGET_PRESENT")
        if language.get("equivalence_status") != "ACCEPTED":
            raise S40ReadRefusal("S40_EQUIVALENCE_NOT_ACCEPTED")

        event_id = generation["event_id"]
        event = session.event(event_id)
        if not event:
            raise S40ReadRefusal("S40_SPEECH_EVENT_ABSENT")
        if event.get("kind") != "SPEECH" or event.get("actor_id") != "A":
            raise S40ReadRefusal("S40_SPEECH_EVENT_INVALID")
        if event.get("hash") != language.get("speech_event_hash"):
            raise S40ReadRefusal("S40_SPEECH_EVENT_HASH_MISMATCH")
        body = event.get("body") or {}
        if body.get("text") != language.get("native_text"):
            raise S40ReadRefusal("S40_NATIVE_TEXT_MISMATCH")
        spans = body.get("spans") or []
        if not spans or spans[0].get("language_tag") != language.get("language_tag"):
            raise S40ReadRefusal("S40_NATIVE_LANGUAGE_TAG_MISMATCH")
        lme = body.get("lme") or {}
        if lme.get("plan_hash") != language.get("plan_hash"):
            raise S40ReadRefusal("S40_PLAN_HASH_MISMATCH")
        if lme.get("native_artifact_hash") != language.get("native_artifact_hash"):
            raise S40ReadRefusal("S40_NATIVE_ARTIFACT_MISMATCH")
        if lme.get("translation_artifact_hash") != language.get(
            "translation_artifact_hash"
        ):
            raise S40ReadRefusal("S40_TRANSLATION_ARTIFACT_MISMATCH")
        if lme.get("equivalence_receipt_hash") != language.get(
            "equivalence_receipt_hash"
        ):
            raise S40ReadRefusal("S40_EQUIVALENCE_HASH_MISMATCH")
        source_refs = lme.get("source_event_refs") or []
        if not any(
            row.get("event_id") == language.get("source_event_id")
            and row.get("event_hash") == language.get("source_event_hash")
            for row in source_refs
        ):
            raise S40ReadRefusal("S40_LANGUAGE_SOURCE_EVENT_MISMATCH")
        if language.get("access_receipt_id") not in (lme.get("access_receipt_ids") or []):
            raise S40ReadRefusal("S40_LANGUAGE_ACCESS_RECEIPT_MISMATCH")
        if set(receipt.get("source_refs") or []).intersection(
            {row.get("event_id", "") for row in source_refs}
        ):
            raise S40ReadRefusal("S40_PRIVATE_GENERATION_SOURCE_EXPOSED")

        view = session.language_view(event_id, locale="en")
        if view.get("status") != "OK" or view.get("display_mode") != "LABELED_ENGLISH":
            raise S40ReadRefusal("S40_LABELED_ENGLISH_VIEW_UNAVAILABLE", str(view))
        if view.get("translation_text") != language.get("translation_text"):
            raise S40ReadRefusal("S40_TRANSLATION_TEXT_MISMATCH")
        if view.get("plan_hash") != language.get("plan_hash"):
            raise S40ReadRefusal("S40_VIEW_PLAN_MISMATCH")
        if view.get("native_artifact_hash") != language.get("native_artifact_hash"):
            raise S40ReadRefusal("S40_VIEW_NATIVE_MISMATCH")
        if view.get("translation_artifact_hash") != language.get(
            "translation_artifact_hash"
        ):
            raise S40ReadRefusal("S40_VIEW_TRANSLATION_MISMATCH")
        equivalence = view.get("equivalence") or {}
        if equivalence.get("receipt_hash") != language.get("equivalence_receipt_hash"):
            raise S40ReadRefusal("S40_VIEW_EQUIVALENCE_MISMATCH")
        if equivalence.get("status") != "ACCEPTED":
            raise S40ReadRefusal("S40_VIEW_EQUIVALENCE_STATUS_MISMATCH")

        projection = session._projection(event_id)
        if not projection:
            raise S40ReadRefusal("S40_PROJECTION_MISSING")
        if projection.get("plan_hash") != language.get("plan_hash"):
            raise S40ReadRefusal("S40_PROJECTION_PLAN_MISMATCH")
        if projection.get("native_artifact_hash") != language.get("native_artifact_hash"):
            raise S40ReadRefusal("S40_PROJECTION_NATIVE_MISMATCH")
        if projection.get("translation_artifact_hash") != language.get(
            "translation_artifact_hash"
        ):
            raise S40ReadRefusal("S40_PROJECTION_TRANSLATION_MISMATCH")
        projection_body = _episode_by_id(session, language.get("projection_episode_id", ""))
        if projection_body is None or projection_body.get("source_speech_event_id") != event_id:
            raise S40ReadRefusal("S40_PROJECTION_EPISODE_MISMATCH")
        admission = session._admission_for(language.get("plan_hash", ""), event_id)
        if not admission or admission.get("admission_id") != language.get("admission_id"):
            raise S40ReadRefusal("S40_ADMISSION_BINDING_MISMATCH")
        if admission.get("native_artifact", {}).get("artifact_hash") != language.get(
            "native_artifact_hash"
        ):
            raise S40ReadRefusal("S40_ADMISSION_NATIVE_MISMATCH")
        if admission.get("translation_artifact", {}).get("artifact_hash") != language.get(
            "translation_artifact_hash"
        ):
            raise S40ReadRefusal("S40_ADMISSION_TRANSLATION_MISMATCH")
        if admission.get("equivalence", {}).get("receipt_hash") != language.get(
            "equivalence_receipt_hash"
        ):
            raise S40ReadRefusal("S40_ADMISSION_EQUIVALENCE_MISMATCH")
        if s36["outcome"] not in {
            "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
            "OBSERVED_CURRENT_REFUSAL",
        }:
            raise S40ReadRefusal("S40_PERFORMED_S36_NOT_OBSERVED")
        if s36["response_kind"] != attempt.get("s36_response_kind"):
            raise S40ReadRefusal("S40_PERFORMED_S36_KIND_MISMATCH")
        return {
            "schema": "SOROK_S40_GENERATED_NATIVE_SPEECH_READ@1",
            "grade": GRADE,
            "provenance": PROVENANCE,
            "native": False,
            "status": "OK",
            "language_status": "ACCEPTED",
            "selected_option": option,
            "attempt_status": generation["attempt_status"],
            "performed": True,
            "speech_event_id": event_id,
            "speech_event_hash": event.get("hash", ""),
            "native_text": language.get("native_text"),
            "translation_text": language.get("translation_text"),
            "language_tag": language.get("language_tag"),
            "target_language_tag": language.get("target_language_tag"),
            "plan_hash": language.get("plan_hash"),
            "native_artifact_hash": language.get("native_artifact_hash"),
            "translation_artifact_hash": language.get("translation_artifact_hash"),
            "equivalence_receipt_hash": language.get("equivalence_receipt_hash"),
            "access_receipt_id": language.get("access_receipt_id"),
            "source_event_id": language.get("source_event_id"),
            "source_event_hash": language.get("source_event_hash"),
            "projection_episode_id": language.get("projection_episode_id"),
            "admission_id": language.get("admission_id"),
            "s36": s36,
            "generation_hash": generation["generation_hash"],
            "attempt_hash": generation["attempt_hash"],
            "target_proposals": [],
        }

    if option in SPEAKING_OPTIONS and not performed:
        if language:
            raise S40ReadRefusal("S40_DENIED_ATTEMPT_HAS_LANGUAGE")
        if attempt.get("event_id") or attempt.get("event_hash"):
            raise S40ReadRefusal("S40_DENIED_ATTEMPT_HAS_EVENT")
        if s36["outcome"] != "RECEIVABLE_NO_OBSERVED_UPTAKE":
            raise S40ReadRefusal("S40_DENIED_S36_NOT_EMPTY")
        return {
            "schema": "SOROK_S40_GENERATED_NATIVE_SPEECH_READ@1",
            "grade": GRADE,
            "provenance": PROVENANCE,
            "native": False,
            "status": "OK",
            "language_status": "NONE",
            "selected_option": option,
            "attempt_status": "DENIED",
            "performed": False,
            "speech_event_id": "",
            "speech_event_hash": "",
            "native_text": "",
            "translation_text": "",
            "language_tag": "",
            "target_language_tag": "",
            "plan_hash": "",
            "native_artifact_hash": "",
            "translation_artifact_hash": "",
            "equivalence_receipt_hash": "",
            "s36": s36,
            "generation_hash": generation["generation_hash"],
            "attempt_hash": generation["attempt_hash"],
            "target_proposals": [],
        }

    if option == "ATTEND_OBJECT" and performed:
        if language:
            raise S40ReadRefusal("S40_NONVERBAL_HAS_LANGUAGE_BINDING")
        event = session.event(generation["event_id"])
        if not event or event.get("kind") != "INSPECT":
            raise S40ReadRefusal("S40_NONVERBAL_EVENT_INVALID")
        return {
            "schema": "SOROK_S40_GENERATED_NATIVE_SPEECH_READ@1",
            "grade": GRADE,
            "provenance": PROVENANCE,
            "native": False,
            "status": "OK",
            "language_status": "NONVERBAL",
            "selected_option": option,
            "attempt_status": "ADMITTED",
            "performed": True,
            "speech_event_id": "",
            "speech_event_hash": "",
            "native_text": "",
            "translation_text": "",
            "language_tag": "",
            "target_language_tag": "",
            "plan_hash": "",
            "native_artifact_hash": "",
            "translation_artifact_hash": "",
            "equivalence_receipt_hash": "",
            "action_event_id": event.get("event_id", ""),
            "action_event_hash": event.get("hash", ""),
            "s36": s36,
            "generation_hash": generation["generation_hash"],
            "attempt_hash": generation["attempt_hash"],
            "target_proposals": [],
        }

    raise S40ReadRefusal("S40_UNSUPPORTED_GENERATION_STATE", option)


__all__ = ["GRADE", "S40ReadRefusal", "read_s40"]
