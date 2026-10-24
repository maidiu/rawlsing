"""Persistent S39 generated-response session over the S37 consumer."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .bootstrap import CUTS, install

install()

from r30a.first_session import SessionRefusal  # noqa: E402
from s37.product import EPISODE_KIND, S37TargetlessProduct  # noqa: E402
from s37.session import (  # noqa: E402
    GRADE as S37_GRADE,
    SCHEMA as S37_SCHEMA,
    S37IntegratedSession,
)

from .model import FULL_RULE, PROVENANCE, S39GenerationRefusal  # noqa: E402
from .performer import perform_attempt  # noqa: E402
from .producer import GeneratedProducer  # noqa: E402
from .reader import S39ReadRefusal, read_generation  # noqa: E402
from .sources import context_records  # noqa: E402

S39_SCHEMA = "SOROK_S39_GENERATED_RESPONSE_SESSION@1"


class S39GeneratedSession(S37IntegratedSession):
    """One persistent generated-action chain using the S37 session/product."""

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
    ) -> "S39GeneratedSession":
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
            world = session.world()
            if world.clock < producer.event_time:
                world.advance(producer.event_time)
                product._checkpoint(session.branch_id, world.clock, world)

            attempt = perform_attempt(
                session, attempt_request,
                generation_receipt_hash=receipt["hash"],
            )
            pipeline = producer.finalize_s36(attempt_result=attempt)
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
                session.branch_id,
                "A",
                "S39_CONSTRUCTIVE_GENERATION",
                world.clock,
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
                session.branch_id,
                "A",
                "S39_GENERATED_ATTEMPT",
                world.clock,
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
                session.branch_id,
                "A",
                EPISODE_KIND,
                world.clock,
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
                r29p_source_ref="TEST_ONLY_S39_M35_FIRSTCLASS_B",
                expression_port="R31E_EXPRESSION_PORT@1",
                actor_model="LIVE_ACTOR_MODEL_NOT_RUN",
                s39_schema=S39_SCHEMA,
                s39_generation=receipt,
                s39_attempt=attempt,
                s39_generation_hash=receipt["hash"],
                s39_attempt_hash=attempt["hash"],
                s39_selected_option=receipt["selected_option"],
                s39_generation_status=receipt["selection_status"],
                s39_provenance=PROVENANCE,
                s39_attempt_status=attempt["attempt_status"],
                s39_performed=attempt["performed"],
            )
            session._save_join_meta()
            verification = session.verify()
            if not verification.get("ok"):
                raise SessionRefusal(
                    "S39_VERIFY_FAILED", json.dumps(verification, sort_keys=True)
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

    def read_generation(self) -> dict:
        return read_generation(self)

    def verify(self) -> dict:
        result = super().verify()
        try:
            generation = self.read_generation()
            summary = {
                "status": "OK",
                "generation_hash": generation["generation_hash"],
                "attempt_hash": generation["attempt_hash"],
                "selected_option": generation["selected_option"],
                "attempt_status": generation["attempt_status"],
                "performed": generation["performed"],
                "event_id": generation["event_id"],
                "event_hash": generation["event_hash"],
                "s36": generation["s36"],
                "provenance": generation["provenance"],
            }
            generation_ok = True
        except (S39ReadRefusal, KeyError, OSError, ValueError) as exc:
            summary = {"status": "REFUSED", "code": str(exc)}
            generation_ok = False
        result["s39_generation"] = summary
        result["ok"] = bool(result.get("ok")) and generation_ok
        return result

    def status(self) -> dict:
        result = super().status()
        try:
            generation = self.read_generation()
            summary = {
                "status": "OK",
                "selected_option": generation["selected_option"],
                "attempt_status": generation["attempt_status"],
                "performed": generation["performed"],
                "event_id": generation["event_id"],
                "event_hash": generation["event_hash"],
                "generation_hash": generation["generation_hash"],
                "attempt_hash": generation["attempt_hash"],
                "s36": generation["s36"],
                "provenance": generation["provenance"],
            }
        except (S39ReadRefusal, KeyError, OSError, ValueError) as exc:
            summary = {"status": "REFUSED", "code": str(exc)}
        result.update(
            {
                "schema": S39_SCHEMA,
                "s37_schema": S37_SCHEMA,
                "s39_generation": summary,
            }
        )
        return result


__all__ = ["S39_SCHEMA", "S39GeneratedSession"]
