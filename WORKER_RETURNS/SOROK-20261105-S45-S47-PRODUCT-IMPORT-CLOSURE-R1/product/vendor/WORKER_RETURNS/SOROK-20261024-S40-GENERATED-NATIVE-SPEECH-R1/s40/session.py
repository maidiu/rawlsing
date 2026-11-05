"""Persistent S40 generated-native-speech session over accepted S39/S37."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .bootstrap import CUTS, install

install()

from r30a.first_session import SessionRefusal  # noqa: E402
from language_mediation.equivalence import evaluate_pair  # noqa: E402
from language_mediation.session import PROJECTION_SCHEMA  # noqa: E402
from s37.product import EPISODE_KIND, S37TargetlessProduct  # noqa: E402
from s37.session import GRADE as S37_GRADE, SCHEMA as S37_SCHEMA  # noqa: E402
from s39.model import FULL_RULE, PROVENANCE, S39GenerationRefusal  # noqa: E402
from s39.producer import GeneratedProducer  # noqa: E402
from s39.session import S39GeneratedSession  # noqa: E402
from s39.sources import context_records  # noqa: E402

from .language import S40_ATOMS, S40_PAIRS  # noqa: E402
from .performer import perform_generated_attempt  # noqa: E402
from .reader import S40ReadRefusal, read_s40  # noqa: E402

S40_SCHEMA = "SOROK_S40_GENERATED_NATIVE_SPEECH_SESSION@1"


class S40GeneratedSession(S39GeneratedSession):
    """S39 generated choice plus authorized source-language outward speech."""

    @classmethod
    def start(
        cls,
        state_root,
        *,
        case: Mapping[str, Any],
        source: Mapping[str, Any] | None = None,
        variant: str = "A_REPAIR_LONG",
        attention: str = "focused",
        source_records: list[Mapping[str, Any]] | None = None,
        rule=FULL_RULE,
        labels: Mapping[str, Any] | None = None,
        language_competence: bool = True,
    ) -> "S40GeneratedSession":
        state_root = Path(state_root).resolve()
        state_root.mkdir(parents=True, exist_ok=True)
        if (state_root / "session.json").exists():
            raise SessionRefusal("SESSION_EXISTS__NO_AUTOMATIC_REROLL")
        if (state_root / "product").exists() or (state_root / "source").exists():
            raise SessionRefusal("ORPHAN_PRODUCT_ROOT")

        producer = GeneratedProducer(
            state_root / "source", case=case, source=source, variant=variant
        )
        product = None
        try:
            producer.stage_m35()
            records = list(source_records) if source_records is not None else context_records(
                actor_id=producer.occurrence.actor_id,
                branch_id="first_session",
                as_of=producer.as_of,
                repair_urgent=True,
                avoid_debt=True,
                prior_b_share=True,
                labels=labels,
            )
            receipt = producer.generate(source_records=records, rule=rule)
            if receipt.get("selection_status") != "UNIQUE_SELECTED":
                raise S39GenerationRefusal(
                    "S39_GENERATION_UNRESOLVED",
                    str(receipt.get("unresolved_reason", "")),
                )
            attempt_request = receipt["attempt_request"]
            c8 = producer.c8_binding()
            typed_source = dict(producer.source)
            source_map = producer.source_map()
            life = producer.historical_life

            product = S37TargetlessProduct(
                state_root / "product",
                life=life,
                source=typed_source,
                c8_binding=c8,
                variant=variant,
                s36_binding={},
                write_sidecar=True,
            )
            session = cls._attach_new(
                product,
                state_root,
                scenario="available",
                attention=attention,
                variant=variant,
            )
            session.meta["s40_language_competence_allowed"] = bool(language_competence)
            world = session.world()
            if world.clock < producer.event_time:
                world.advance(producer.event_time)
                product._checkpoint(session.branch_id, world.clock, world)

            e1_identity = {
                "event_id": producer.e1_event["event_id"],
                "event_hash": producer.e1_event["hash"],
                "c8_occurrence_id": producer.out9.occurrence_id,
                "c8_state_digest": producer.out9.readset["state_digest"],
            }
            attempt = perform_generated_attempt(
                session, attempt_request, generation_receipt=receipt,
                e1_identity=e1_identity,
            )
            producer.finalize_s36(attempt_result=attempt)
            s36 = dict(producer.s36_binding or {})
            rel = s36.get("c9_db_relpath", "")
            if rel and not Path(rel).is_absolute():
                s36["c9_db_relpath"] = str(Path("source") / rel)
            producer.s36_binding = s36
            producer.close()

            product.s36_binding = s36
            product.sidecar["s36"] = s36
            product.sidecar["source_operation"] = typed_source["b_operation"]
            product.sidecar["material_access"] = (
                "granted" if typed_source["b_operation"] == "SHARE_TOOL" else "denied"
            )
            product.sidecar_path.write_text(
                json.dumps(product.sidecar, indent=2, sort_keys=True) + "\n",
                encoding="utf8",
            )

            world = session.world()
            product._append_episode(
                session.branch_id, "A", "S39_CONSTRUCTIVE_GENERATION", world.clock,
                {
                    "schema": "SOROK_S39_GENERATION_EPISODE@1",
                    "grade": PROVENANCE,
                    "generation": receipt,
                    "generation_hash": receipt["hash"],
                    "source": typed_source,
                    "c8": c8,
                    "s36": s36,
                    "native": False,
                },
            )
            product._append_episode(
                session.branch_id, "A", "S39_GENERATED_ATTEMPT", world.clock,
                {
                    "schema": "SOROK_S39_ATTEMPT_EPISODE@1",
                    "grade": PROVENANCE,
                    "attempt": attempt,
                    "attempt_hash": attempt["hash"],
                    "generation_hash": receipt["hash"],
                    "native": False,
                },
            )
            product._append_episode(
                session.branch_id, "A", EPISODE_KIND, world.clock,
                {
                    "schema": "SOROK_S37_C12_S36_BINDING@1",
                    "grade": S37_GRADE,
                    "source": typed_source,
                    "c8": c8,
                    "s36": s36,
                    "target_id": "",
                    "native": False,
                },
            )
            product._checkpoint(session.branch_id, world.clock, world)

            language = attempt.get("language")
            session.meta.update(
                schema=S37_SCHEMA,
                grade=S37_GRADE,
                case=typed_source["b_operation"],
                source=typed_source,
                c8=c8,
                s36=s36,
                target_id="",
                targetless=True,
                j_target_id="",
                root_branch_id="root",
                branch_lineage=None,
                material_performance=(
                    "generated_share"
                    if typed_source["b_operation"] == "SHARE_TOOL"
                    else "generated_refusal"
                ),
                source_actor_map=source_map,
                c9_db_path=s36["c9_db_path"],
                c9_db_relpath=s36["c9_db_relpath"],
                j_source_ref=CUTS["m35"],
                e_source_ref=CUTS["join_e"],
                language_source_ref=CUTS["language"],
                s36_source_ref=CUTS["s37"],
                s39_source_ref=CUTS["s39"],
                r29p_source_ref="TEST_ONLY_S40_M35_FIRSTCLASS_B",
                expression_port="R31E_EXPRESSION_PORT@1",
                actor_model="LIVE_ACTOR_MODEL_NOT_RUN",
                s39_schema="SOROK_S39_GENERATED_RESPONSE_SESSION@1",
                s39_generation=receipt,
                s39_attempt=attempt,
                s39_generation_hash=receipt["hash"],
                s39_attempt_hash=attempt["hash"],
                s39_selected_option=receipt["selected_option"],
                s39_generation_status=receipt["selection_status"],
                s39_provenance=PROVENANCE,
                s39_attempt_status=attempt["attempt_status"],
                s39_performed=attempt["performed"],
                s40_schema=S40_SCHEMA,
                s40_language=language,
                s40_language_status="ACCEPTED" if language else "NONE",
                s40_selected_option=receipt["selected_option"],
                s40_attempt_status=attempt["attempt_status"],
                s40_performed=attempt["performed"],
            )
            session._save_join_meta()
            verification = session.verify()
            if not verification.get("ok"):
                raise SessionRefusal(
                    "S40_VERIFY_FAILED", json.dumps(verification, sort_keys=True)
                )
            return session
        except Exception:
            if product is not None:
                product.close()
            try:
                producer.close()
            except Exception:
                pass
            raise

    def read_s40(self) -> dict:
        return read_s40(self)

    def _projection_verification(self, event: dict, lme: dict,
                                 projection: dict) -> dict:
        event_id = event.get("event_id", "")
        if projection.get("schema") != PROJECTION_SCHEMA:
            return {"ok": False, "reason": "PROJECTION_SCHEMA_MISMATCH"}
        if projection.get("source_speech_event_id") != event_id:
            return {"ok": False, "reason": "PROJECTION_SOURCE_EVENT_MISMATCH"}
        if projection.get("source_event_hash") != event.get("hash", ""):
            return {"ok": False, "reason": "PROJECTION_SOURCE_HASH_MISMATCH"}
        if projection.get("plan_hash") != lme.get("plan_hash", ""):
            return {"ok": False, "reason": "PROJECTION_PLAN_HASH_MISMATCH"}
        if projection.get("native_artifact_hash") != lme.get("native_artifact_hash", ""):
            return {"ok": False, "reason": "PROJECTION_NATIVE_HASH_MISMATCH"}
        if projection.get("translation_artifact_hash") != lme.get(
            "translation_artifact_hash", ""
        ):
            return {"ok": False, "reason": "PROJECTION_TRANSLATION_HASH_MISMATCH"}
        receipt = projection.get("equivalence_receipt") or {}
        if receipt.get("status") != "ACCEPTED":
            return {"ok": False, "reason": "EQUIVALENCE_" + str(receipt.get("status"))}
        if receipt.get("receipt_hash") != lme.get("equivalence_receipt_hash", ""):
            return {"ok": False, "reason": "PROJECTION_EQUIVALENCE_HASH_MISMATCH"}
        admission = self._admission_for(lme.get("plan_hash", ""), event_id)
        if not admission:
            return {"ok": False, "reason": "PROJECTION_ADMISSION_MISSING"}
        native = admission.get("native_artifact") or {}
        translation = admission.get("translation_artifact") or {}
        if native.get("artifact_hash") != projection.get("native_artifact_hash"):
            return {"ok": False, "reason": "PROJECTION_NATIVE_ARTIFACT_MISMATCH"}
        if translation.get("artifact_hash") != projection.get(
            "translation_artifact_hash"
        ):
            return {"ok": False, "reason": "PROJECTION_TRANSLATION_ARTIFACT_MISMATCH"}
        if translation.get("text") != projection.get("text"):
            return {"ok": False, "reason": "PROJECTION_TEXT_MISMATCH"}
        recheck = evaluate_pair(
            admission.get("plan") or {}, native, translation,
            pairs=S40_PAIRS, atom_universe=S40_ATOMS,
        )
        if recheck.get("status") != "ACCEPTED":
            return {"ok": False, "reason": "PROJECTION_EQUIVALENCE_"
                    + str(recheck.get("status"))}
        if recheck.get("receipt_hash") != receipt.get("receipt_hash"):
            return {"ok": False, "reason": "PROJECTION_EQUIVALENCE_RECEIPT_MISMATCH"}
        return {"ok": True}

    def verify(self) -> dict:
        result = super().verify()
        try:
            s40 = self.read_s40()
            summary = {
                "status": "OK",
                "selected_option": s40["selected_option"],
                "attempt_status": s40["attempt_status"],
                "performed": s40["performed"],
                "language_status": s40["language_status"],
                "speech_event_id": s40["speech_event_id"],
                "speech_event_hash": s40["speech_event_hash"],
                "native_text": s40["native_text"],
                "translation_text": s40["translation_text"],
                "plan_hash": s40["plan_hash"],
                "equivalence_receipt_hash": s40["equivalence_receipt_hash"],
                "s36": s40["s36"],
            }
            s40_ok = True
        except (S40ReadRefusal, KeyError, OSError, ValueError) as exc:
            summary = {"status": "REFUSED", "code": str(exc)}
            s40_ok = False
        result["s40_language"] = summary
        result["ok"] = bool(result.get("ok")) and s40_ok
        return result

    def status(self) -> dict:
        result = super().status()
        try:
            s40 = self.read_s40()
            summary = {
                "status": "OK",
                "selected_option": s40["selected_option"],
                "attempt_status": s40["attempt_status"],
                "performed": s40["performed"],
                "language_status": s40["language_status"],
                "speech_event_id": s40["speech_event_id"],
                "speech_event_hash": s40["speech_event_hash"],
                "native_text": s40["native_text"],
                "translation_text": s40["translation_text"],
                "plan_hash": s40["plan_hash"],
                "equivalence_receipt_hash": s40["equivalence_receipt_hash"],
                "s36": s40["s36"],
            }
        except (S40ReadRefusal, KeyError, OSError, ValueError) as exc:
            summary = {"status": "REFUSED", "code": str(exc)}
        result.update({
            "schema": S40_SCHEMA,
            "s37_schema": S37_SCHEMA,
            "s39_schema": "SOROK_S39_GENERATED_RESPONSE_SESSION@1",
            "s40_language": summary,
        })
        return result


__all__ = ["S40_SCHEMA", "S40GeneratedSession"]
