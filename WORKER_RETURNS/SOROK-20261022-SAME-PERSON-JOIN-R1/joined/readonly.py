"""Cold-reopen wrapper that never rewrites the immutable J product root."""
from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import historical_actor_producer as H
from bp2p4 import reunion as R
from r29p.product import JOIN_STATE
from r31j.product import R31JProduct as _R31JProduct


class ReadOnlyR31JProduct(_R31JProduct):
    """R31J product reopened for reading; constructor persistence is disabled.

    The pinned ``R31JProduct.__init__`` rewrites ``bp2_join.json`` through
    ``_persist_r31j_binding`` and ``_persist_variant`` even during a cold read.
    Both methods are dynamic-dispatch seams, so this wrapper suppresses them
    only for the read-only reopen.  The vendor file itself stays immutable.
    """

    def __init__(self, root, *, artifacts, source=None, c8_state_digest="",
                 e1_event_hash="", target_id="", branch_id="root",
                 variant="A_REPAIR_LONG", bind_source=True, readonly=True,
                 **kwargs):
        self._readonly = bool(readonly)
        super().__init__(
            root, artifacts=artifacts, source=source,
            c8_state_digest=c8_state_digest, e1_event_hash=e1_event_hash,
            target_id=target_id, branch_id=branch_id, variant=variant,
            bind_source=bind_source, **kwargs)

    def _persist_variant(self):
        if getattr(self, "_readonly", False):
            return
        return super()._persist_variant()

    def _persist_r31j_binding(self, artifacts, c8_state_digest, e1_event_hash,
                              target_id):
        if getattr(self, "_readonly", False):
            return
        return super()._persist_r31j_binding(
            artifacts, c8_state_digest, e1_event_hash, target_id)

    @classmethod
    def reopen(cls, root, *, branch_id="root"):
        root = Path(root)
        if not (root / JOIN_STATE).exists():
            raise ValueError("R31J_TIME_COORDINATE_HOLD")
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
        life = H.build_life(variant)
        snapshot = document.get("r31j_actor_snapshot")
        if snapshot is not None:
            life = replace(life, a_snapshot=snapshot)
        artifacts = R._assemble(
            mode="RECOVERED", root=Path(recorded["root"]),
            life=life, persisted=persisted, paths=paths,
            receipt={"persisted": persisted}, e2=None)
        return cls(
            root, artifacts=artifacts, source=document.get("r31j_source"),
            c8_state_digest=document.get("r31j_c8_state_digest", ""),
            e1_event_hash=document.get("r31j_e1_event_hash", ""),
            target_id=document.get("r31j_target_id", ""),
            branch_id=branch_id, variant=variant, bind_source=False,
            readonly=True)


__all__ = ["ReadOnlyR31JProduct"]
