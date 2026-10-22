"""R29P product: R27P actor-origin chain with the R26E qualified C12 read path."""
from __future__ import annotations

import json
from pathlib import Path

import historical_actor_producer as H
from bp2p4 import reunion as R
from bp2p4.product import JoinedProduct
from r26e.c12_integrity import QualifiedC12Store

JOIN_STATE = "bp4_join_state.json"
PRODUCT_GRADE = "TEST_ONLY_SOURCEFREE_R29P_GENERATED_ACTOR_PRODUCT_NOT_NATIVE"


class R29PProduct(JoinedProduct):
    """Joined BP2/BP4 product whose C12 reads use the corrected preimage verifier."""

    def __init__(self, root, *, artifacts, branch_id="root",
                 variant="A_REPAIR_LONG", **kwargs):
        self.variant = variant
        super().__init__(root, artifacts=artifacts, branch_id=branch_id, **kwargs)
        self._qualify_store()
        self._persist_variant()

    def _qualify_store(self):
        path = self.store.path
        self.store.close()
        self.store = QualifiedC12Store(path)

    def _persist_variant(self):
        path = self.root / "bp2_join.json"
        if not path.exists():
            return
        document = json.loads(path.read_text(encoding="utf8"))
        document["variant"] = self.variant
        path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n",
                        encoding="utf8")

    @classmethod
    def reopen(cls, root, *, branch_id="root"):
        root = Path(root)
        if not (root / JOIN_STATE).exists():
            raise ValueError("R29P_TIME_COORDINATE_HOLD")
        document = json.loads((root / "bp2_join.json").read_text(encoding="utf8"))
        variant = document.get("variant", "A_REPAIR_LONG")
        persisted = document["persisted"]
        recorded = document["artifacts"]
        paths = {
            "journal_path": Path(recorded["journal_path"]),
            "key_path": Path(recorded["key_path"]),
            "key_id": recorded["key_id"],
            "anchor_log": Path(recorded["anchor_log"]),
            "anchor_watermark": Path(recorded["anchor_watermark"]),
            "c9_path": Path(recorded["c9_path"]),
        }
        artifacts = R._assemble(
            mode="RECOVERED", root=Path(recorded["root"]),
            life=H.build_life(variant), persisted=persisted, paths=paths,
            receipt={"persisted": persisted}, e2=None)
        return cls(root, artifacts=artifacts, branch_id=branch_id, variant=variant)

    def c12_verify(self, branch_id=None):
        return self.store.verify(branch_id or self.branch_id)

    def observe_verified(self, actor="A"):
        verify = self.c12_verify()
        if not verify["ok"]:
            return {
                "schema": "R29P_OBSERVE@1",
                "status": "HELD",
                "code": "C12_CHAIN_INVALID",
                "verify": verify,
                "native": False,
                "grade": PRODUCT_GRADE,
            }
        result = self.observe(actor=actor)
        result["c12_verify"] = verify
        result["r29p_grade"] = PRODUCT_GRADE
        return result

    def reenter_verified(self, actor="A"):
        self.store.close()
        self.store = QualifiedC12Store(self.root / "c12.sqlite")
        return self.observe_verified(actor=actor)

    def close(self):
        self.store.close()
