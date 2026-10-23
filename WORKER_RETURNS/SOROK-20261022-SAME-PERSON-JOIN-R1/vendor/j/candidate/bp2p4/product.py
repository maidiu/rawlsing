"""Joined A0-A3 product: BP4's real product over the real BP2 joined seed.

The class subclasses BP4's actual ``BP4Product`` and only replaces seed
construction. Every user-facing behavior - C10 read, C12 append-only store,
objective world, M6 actor-safe perception, SAY/DO/ATTEND, offscreen life, fork,
cold reentry - is the inherited BP4 implementation.

The BP2 join changes three real things in that product:

1. ``C10.receive`` re-verifies the actual BP2 keyed C8 journal, the sealed C9
   target row (``950a4c79…``-equivalent) and the actor snapshots before any
   A0 observation.
2. The committed BP2 ``V3MS_PRACTICE`` target plus its independently performed
   E2 act are materialized into actor A's ``projects``/``tools_remaining`` and
   into the workshop tool resource.
3. The BP2->BP4 envelope and the two clock domains are recorded explicitly; no
   numeric cross-domain ordering is ever used.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402
from bp4.product import BP4Product  # noqa: E402
from bp4.store import C12Store  # noqa: E402

from .reunion import ReunionRefusal, recover  # noqa: E402
from .seed import JoinedSeed, SeedRefusal, build_seed  # noqa: E402

JOIN_STATE = "bp4_join_state.json"
PRODUCT_GRADE = "TEST_ONLY_SOURCEFREE_JOINED_PRODUCT_ALPHA_NOT_NATIVE"


class JoinedProductRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


class JoinedProduct(BP4Product):
    """BP4's A0-A3 product bound to the BP2 joined source."""

    def __init__(self, root, *, artifacts, branch_id: str = "root",
                 e2: Any = "default", world=None, materialize: bool = True) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.artifacts = artifacts
        self.seed: JoinedSeed = build_seed(artifacts, e2=e2, world=world,
                                           materialize=materialize)
        self.store = C12Store(self.root / "c12.sqlite")
        self.branch_id = branch_id
        existing = self.store._branch("root")
        self._check_binding_source()
        if existing is not None and not self._world_root_after_bind():
            self.store.close()
            raise JoinedProductRefusal(
                "TIME_COORDINATE_HOLD",
                "existing C12 root has no recorded post-BP2 world-root marker; "
                "refusing to assert a chronological relation")
        self._ensure_root()
        if existing is None:
            self._record_world_root()

    def _check_binding_source(self) -> None:
        """Refuse to attach an existing product root to a different BP2 run."""
        path = self.root / "bp2_join.json"
        if not path.exists():
            return
        document = json.loads(path.read_text(encoding="utf8"))
        recorded = document.get("artifacts", {})
        if recorded.get("target_id") and recorded["target_id"] != self.artifacts.target_id:
            self.store.close()
            raise JoinedProductRefusal(
                "JOIN_BINDING_SOURCE_MISMATCH",
                recorded["target_id"] + " != " + self.artifacts.target_id)

    def _world_root_after_bind(self) -> bool:
        path = self.root / JOIN_STATE
        if not path.exists():
            return False
        try:
            document = json.loads(path.read_text(encoding="utf8"))
        except (OSError, ValueError):
            return False
        return bool(document.get("created_after_bp2_bind"))

    def _record_world_root(self) -> None:
        from .reunion import _persist_binding

        _persist_binding(self.root, self.artifacts)
        document = {
            "schema": "BP2P4J_BP4_JOIN_STATE@1",
            "world_root_created": True,
            "created_after_bp2_bind": True,
            "branch_id": self.branch_id,
            "world_hash": self.store.latest_state(self.branch_id)["world"]["hash"],
            "world_clock": self.store.last_clock(self.branch_id),
            "process_order": list(self.seed.clock.process_order),
            "join_receipt_hash": digest(self.seed.custody()),
        }
        (self.root / JOIN_STATE).write_text(
            json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf8")

    @classmethod
    def reopen(cls, root, *, branch_id: str = "root") -> "JoinedProduct":
        """Fresh-process construction from the persisted BP2 join binding."""
        root = Path(root)
        if not (root / JOIN_STATE).exists():
            raise JoinedProductRefusal(
                "TIME_COORDINATE_HOLD", "missing BP4 world-root join state")
        return cls(root, artifacts=recover(root), branch_id=branch_id)

    # ------------------------------------------------------------------
    def joined_source(self) -> dict:
        """The full source identity the user-facing product is bound to."""
        state = self.store.latest_state(self.branch_id)
        return {
            "schema": "BP2P4J_JOINED_SOURCE@1",
            "grade": PRODUCT_GRADE,
            "native": False,
            "artifacts": self.artifacts.public(),
            "custody": self.seed.custody(),
            "practice": self.seed.practice.as_dict(),
            "clock": self.seed.clock.as_dict(),
            "envelope": {
                "schema": self.seed.envelope["schema"],
                "producer": self.seed.envelope["producer"],
                "validation": self.seed.envelope_validation,
                "hash": digest(self.seed.envelope),
            },
            "world": {
                "hash": state["world"]["hash"],
                "clock": state["world"]["clock"],
                "tool_available": state["world"]["resources"]["workshop"]["tool_available"],
            },
            "c12": {
                "branch_id": self.branch_id,
                "last_clock": self.store.last_clock(self.branch_id),
            },
            "native_grants": self.seed.custody()["native_grants"],
        }

    def verify_join(self) -> dict:
        """Independent re-check of every joined source edge at read time."""
        source = self.joined_source()
        custody = source["custody"]
        if custody["target_id"] != self.artifacts.target_id:
            raise JoinedProductRefusal("JOIN_TARGET_ID_MISMATCH")
        if custody["consumed_state_hash"] != self.artifacts.consumed_state_hash:
            raise JoinedProductRefusal("JOIN_CONSUMED_HASH_MISMATCH")
        if custody["c8_state_digest"] != self.artifacts.c8_state_digest:
            raise JoinedProductRefusal("JOIN_C8_DIGEST_MISMATCH")
        if custody["clock"]["numeric_ordering_used"] is not False:
            raise JoinedProductRefusal("JOIN_NUMERIC_CLOCK_ORDERING")
        if not self.seed.envelope_validation.get("recomputed_from_artifacts"):
            raise JoinedProductRefusal("JOIN_ENVELOPE_NOT_RECOMPUTED")
        return source


__all__ = [
    "JOIN_STATE",
    "JoinedProduct",
    "JoinedProductRefusal",
    "PRODUCT_GRADE",
]
