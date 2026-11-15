"""Native and auxiliary English artifacts, both bound to one admitted plan."""
from __future__ import annotations

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402

NATIVE_SCHEMA = "LME_NATIVE_SPEECH_ARTIFACT@1"
TRANSLATION_SCHEMA = "LME_LABELED_ENGLISH_ARTIFACT@1"
GRADE = "TEST_ONLY_SOURCEFREE_LANGUAGE_ARTIFACT_NOT_NATIVE"


def seal_artifact(body: dict) -> dict:
    value = dict(body)
    value["artifact_hash"] = digest(value)
    return value


def artifact_valid(artifact: dict) -> bool:
    if not isinstance(artifact, dict):
        return False
    stored = artifact.get("artifact_hash")
    if not stored:
        return False
    body = {key: value for key, value in artifact.items()
            if key != "artifact_hash"}
    return digest(body) == stored


def build_native_artifact(plan, *, atoms=None, text=None,
                          plan_hash=None) -> dict:
    pair = plan.pair
    body = {
        "schema": NATIVE_SCHEMA,
        "grade": GRADE,
        "native": False,
        "plan_hash": plan_hash or plan.plan_hash,
        "unit_id": plan.unit["unit_id"],
        "language_tag": pair["native_language"],
        "text": text if text is not None else pair["native_text"],
        "atoms": sorted(atoms if atoms is not None else pair["atoms"]),
        "source_relation_ids": sorted(plan.relation_ids),
        "source_event_refs": list(plan.readset["source_event_refs"]),
        "render_role": "ACTOR_SPEECH_CANDIDATE",
        "product_model_calls": 0,
    }
    return seal_artifact(body)


def build_translation_artifact(plan, native_artifact, *, atoms=None,
                               text=None, plan_hash=None,
                               source_artifact_hash=None) -> dict:
    pair = plan.pair
    body = {
        "schema": TRANSLATION_SCHEMA,
        "grade": GRADE,
        "native": False,
        "plan_hash": plan_hash or plan.plan_hash,
        "source_artifact_hash": (source_artifact_hash
                                 if source_artifact_hash is not None
                                 else native_artifact["artifact_hash"]),
        "source_language_tag": pair["native_language"],
        "target_language_tag": pair["target_language"],
        "text": text if text is not None else pair["target_text"],
        "atoms": sorted(atoms if atoms is not None else pair["atoms"]),
        "render_mode": "LABELED_ENGLISH_AUXILIARY_VIEW",
        "not_actor_speech": True,
        "product_model_calls": 0,
    }
    return seal_artifact(body)


__all__ = [
    "NATIVE_SCHEMA",
    "TRANSLATION_SCHEMA",
    "seal_artifact",
    "artifact_valid",
    "build_native_artifact",
    "build_translation_artifact",
]
