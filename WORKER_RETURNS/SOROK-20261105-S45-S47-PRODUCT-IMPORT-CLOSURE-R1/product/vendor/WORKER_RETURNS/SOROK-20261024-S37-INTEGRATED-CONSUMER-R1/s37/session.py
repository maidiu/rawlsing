"""One persistent targetless session class for both lawful B histories.

The same class, C12 product and public `read_s36` reader are used for SHARE_TOOL
and REFUSE_TOOL. The language methods are the accepted MediatedJoinedSession
methods over the existing C12/world writer; language source histories remain
separate TEST_ONLY sources and are never generated from the S36 orientation.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .bootstrap import CUTS, install

install()

import firstclass  # noqa: E402
from language_mediation import MediatedJoinedSession  # noqa: E402
from r30a.first_session import SessionRefusal  # noqa: E402
from joined.lineage import validate as validate_lineage  # noqa: E402

from .product import (  # noqa: E402
    EPISODE_KIND,
    S37TargetlessProduct,
    validate_s37_product,
)
from .producer import IntegratedProducer  # noqa: E402
from .reader import S37ReadRefusal, read_committed_s36  # noqa: E402

SCHEMA = "SOROK_S37_INTEGRATED_TARGETLESS_SESSION@1"
GRADE = "TEST_ONLY_SOURCEFREE_NOT_NATIVE"


class S37IntegratedSession(MediatedJoinedSession):
    """Persistent targetless C12/language session over one M35 source."""

    @classmethod
    def start(
        cls,
        state_root,
        *,
        case: Mapping[str, Any],
        source: Mapping[str, Any] | None = None,
        variant: str = "A_REPAIR_LONG",
        attention: str = "focused",
    ) -> "S37IntegratedSession":
        state_root = Path(state_root).resolve()
        state_root.mkdir(parents=True, exist_ok=True)
        if (state_root / "session.json").exists():
            raise SessionRefusal("SESSION_EXISTS__NO_AUTOMATIC_REROLL")
        if (state_root / "product").exists() or (state_root / "source").exists():
            raise SessionRefusal("ORPHAN_PRODUCT_ROOT")

        producer = IntegratedProducer(
            state_root / "source",
            case=case,
            source=source,
            variant=variant,
        )
        product = None
        try:
            producer.stage_m35().stage_s36()
            c8 = producer.c8_binding()
            s36 = dict(producer.s36_binding or {})
            rel = s36.get("c9_db_relpath", "")
            if rel and not Path(rel).is_absolute():
                s36["c9_db_relpath"] = str(Path("source") / rel)
            typed_source = dict(producer.source)
            source_map = producer.source_map()
            life = producer.historical_life
            producer.close()

            product = S37TargetlessProduct(
                state_root / "product",
                life=life,
                source=typed_source,
                c8_binding=c8,
                variant=variant,
                s36_binding=s36,
                write_sidecar=True,
            )
            world = product._world("root")
            product._append_episode(
                "root",
                "A",
                EPISODE_KIND,
                world.clock,
                {
                    "schema": "SOROK_S37_C12_S36_BINDING@1",
                    "grade": GRADE,
                    "source": typed_source,
                    "c8": c8,
                    "s36": s36,
                    "target_id": "",
                    "native": False,
                },
            )
            product._checkpoint("root", world.clock, world)

            session = cls._attach_new(
                product,
                state_root,
                scenario="available",
                attention=attention,
                variant=variant,
            )
            session.meta.update(
                schema=SCHEMA,
                grade=GRADE,
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
                    "observed_share"
                    if typed_source["b_operation"] == "SHARE_TOOL"
                    else "observed_refusal"
                ),
                source_actor_map=source_map,
                c9_db_path=s36["c9_db_path"],
                c9_db_relpath=s36["c9_db_relpath"],
                j_source_ref=CUTS["m35"],
                e_source_ref=CUTS["join_e"],
                language_source_ref=CUTS["language"],
                s36_source_ref=CUTS["s36"],
                r29p_source_ref="TEST_ONLY_S37_M35_FIRSTCLASS_B",
                expression_port="R31E_EXPRESSION_PORT@1",
                actor_model="LIVE_ACTOR_MODEL_NOT_RUN",
            )
            session._save_join_meta()
            verification = session.verify()
            if not verification.get("ok"):
                raise SessionRefusal(
                    "S37_VERIFY_FAILED",
                    json.dumps(verification, sort_keys=True),
                )
            return session
        except Exception:
            if product is not None:
                product.close()
            else:
                try:
                    producer.close()
                except Exception:
                    pass
            raise

    @classmethod
    def open(cls, state_root, *, attention: str | None = None) -> "S37IntegratedSession":
        state_root = Path(state_root).resolve()
        path = state_root / "session.json"
        if not path.is_file():
            raise SessionRefusal("SESSION_NOT_FOUND", str(path))
        meta = json.loads(path.read_text(encoding="utf8"))
        if meta.get("schema") != SCHEMA:
            raise SessionRefusal("WRONG_PRODUCT_LINEAGE")
        if Path(meta.get("state_root", "")).resolve() != state_root:
            raise SessionRefusal("SESSION_ROOT_MOVED")
        product_root = state_root / "product"
        if Path(meta.get("product_root", "")).resolve() != product_root:
            raise SessionRefusal("FOREIGN_PRODUCT_ROOT")
        sidecar_path = product_root / "targetless.json"
        if not sidecar_path.is_file():
            raise SessionRefusal("J_BINDING_MISSING", str(sidecar_path))
        sidecar = json.loads(sidecar_path.read_text(encoding="utf8"))
        life = firstclass.prepare_life(meta["source"], meta.get("variant", "A_REPAIR_LONG"))
        product = S37TargetlessProduct(
            product_root,
            life=life,
            source=meta["source"],
            c8_binding=meta["c8"],
            variant=meta.get("variant", "A_REPAIR_LONG"),
            s36_binding=meta["s36"],
            write_sidecar=False,
            branch_id=meta.get("branch_id", "first_session"),
            sidecar_document=sidecar,
        )
        try:
            if product.source != meta["source"]:
                raise SessionRefusal("J_SOURCE_IDENTITY_CHANGED")
            lineage = validate_lineage(meta, product.branch_id, product.store)
            if not lineage.get("ok"):
                raise SessionRefusal(
                    "BRANCH_LINEAGE_MISMATCH",
                    json.dumps(lineage.get("checks", {}), sort_keys=True),
                )
            provenance = validate_s37_product(
                product, meta, sidecar, product.branch_id
            )
            if not provenance.get("ok"):
                raise SessionRefusal(
                    "S37_PROVENANCE_MISMATCH",
                    json.dumps(provenance.get("checks", {}), sort_keys=True),
                )
            if not product.c12_verify("root").get("ok"):
                raise SessionRefusal("C12_ROOT_VERIFY_FAILED")
            if not product.c12_verify(product.branch_id).get("ok"):
                raise SessionRefusal("C12_BRANCH_VERIFY_FAILED")
            session = cls(product, state_root, meta)
            if attention and attention != session.meta.get("attention"):
                session.meta["attention"] = attention
                session._save_join_meta()
            verification = session.verify()
            if not verification.get("ok"):
                raise SessionRefusal(
                    "S37_VERIFY_FAILED",
                    json.dumps(verification, sort_keys=True),
                )
            return session
        except Exception:
            product.close()
            raise

    def _save_join_meta(self) -> None:
        (self.state_root / "session.json").write_text(
            json.dumps(self.meta, indent=2, sort_keys=True) + "\n",
            encoding="utf8",
        )

    def _lineage_result(self) -> dict:
        return validate_lineage(self.meta, self.branch_id, self.product.store)

    def _c9_path(self) -> Path:
        rel = (self.meta.get("s36") or {}).get("c9_db_relpath")
        if rel:
            return self.state_root / rel
        return Path((self.meta.get("s36") or {}).get("c9_db_path", ""))

    def read_s36(self) -> dict:
        """Read the actual committed C9 response/receipt for this session."""
        return read_committed_s36(
            c9_path=self._c9_path(),
            s36_binding=self.meta["s36"],
            c8_binding=self.meta["c8"],
            source=self.meta["source"],
            product=self.product,
            branch_id=self.branch_id,
            meta=self.meta,
            sidecar=self.product.sidecar,
        )

    def verify(self) -> dict:
        result = super().verify()
        root = self.product.c12_verify("root")
        lineage = self._lineage_result()
        provenance = validate_s37_product(
            self.product, self.meta, self.product.sidecar, self.branch_id
        )
        try:
            s36 = self.read_s36()
            s36_ok = True
            s36_summary = {
                "response_ref": s36["response_ref"],
                "c9_receipt_hash": s36["c9_receipt_hash"],
                "outcome": s36["outcome"],
                "target_branch": s36["target_branch"],
                "target_reason": s36["target_reason"],
                "target_proposals": s36["target_proposals"],
            }
        except (S37ReadRefusal, KeyError, OSError, ValueError) as exc:
            s36_ok = False
            s36_summary = {"status": "REFUSED", "code": str(exc)}
        result["root"] = root
        result["lineage"] = lineage
        result["provenance"] = provenance
        result["targetless"] = True
        result["s36"] = s36_summary
        result["ok"] = (
            bool(result.get("ok"))
            and bool(root.get("ok"))
            and bool(lineage.get("ok"))
            and bool(provenance.get("ok"))
            and s36_ok
        )
        return result

    def status(self) -> dict:
        result = super().status()
        try:
            s36 = self.read_s36()
            s36_summary = {
                "status": "OK",
                "response_ref": s36["response_ref"],
                "response_receipt_hash": s36["response_receipt_hash"],
                "c9_receipt_hash": s36["c9_receipt_hash"],
                "outcome": s36["outcome"],
                "target_branch": s36["target_branch"],
                "target_reason": s36["target_reason"],
                "target_id": s36["target_id"],
                "target_proposals": s36["target_proposals"],
                "e1_event_hash": s36["e1_event_hash"],
                "c8_state_digest": s36["c8_state_digest"],
                "source_operation": s36["source_operation"],
                "material_access": s36["material_access"],
                "target_state_rows": s36["target_state_rows"],
            }
        except (S37ReadRefusal, KeyError, OSError, ValueError) as exc:
            s36_summary = {"status": "REFUSED", "code": str(exc)}
        result.update(
            {
                "schema": SCHEMA,
                "grade": GRADE,
                "targetless": True,
                "target_id": "",
                "case": self.meta.get("case"),
                "source_operation": (self.meta.get("source") or {}).get("b_operation"),
                "source_actor_map": self.meta.get("source_actor_map"),
                "s36": s36_summary,
            }
        )
        return result


__all__ = ["GRADE", "SCHEMA", "S37IntegratedSession"]
