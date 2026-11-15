"""R31J product: pre-C9 GM01 source bound into R29P C12/A0/A2."""
from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import historical_actor_producer as H
from bp2p4 import reunion as R
from bp4.world import inspect_event
from r29p.product import JOIN_STATE, R29PProduct


class R31JProduct(R29PProduct):
    """R29P product initialized from the pre-C9 GM01 actor snapshot."""

    def __init__(self, root, *, artifacts, source: dict | None = None,
                 c8_state_digest: str = "", e1_event_hash: str = "",
                 target_id: str = "", branch_id="root",
                 variant="A_REPAIR_LONG", bind_source: bool = True, **kwargs):
        self.source = source or {}
        super().__init__(root, artifacts=artifacts, branch_id=branch_id,
                         variant=variant, **kwargs)
        self._persist_r31j_binding(artifacts, c8_state_digest, e1_event_hash,
                                   target_id)
        if not bind_source:
            self.pre_c9_binding = {}
            return
        world = self._world(self.branch_id)
        state = world.actor_state["A"]
        state["tools_remaining"] = int(
            artifacts.life.a_snapshot["state"].get("tools_remaining", 0))
        state["material_remaining"] = int(
            artifacts.life.a_snapshot["state"].get("material_remaining", 4))
        world.resources["workshop"] = dict(world.resources.get("workshop", {}))
        world.resources["workshop"]["tool_available"] = bool(state["tools_remaining"])
        self._checkpoint(self.branch_id, world.clock, world)
        self._append_episode(self.branch_id, "A", "GM01_SOURCE", world.clock, {
            "gm01_source": source,
            "c8_state_digest": c8_state_digest,
            "e1_event_hash": e1_event_hash,
            "c9_target_id": target_id,
            "native": False,
        })
        self._checkpoint(self.branch_id, world.clock, world)
        self.pre_c9_binding = {
            "schema": "R31J_PRE_C9_PRODUCT_BINDING@1",
            "gm01_b_event_ref": source.get("b_event_ref"),
            "gm01_b_event_hash": source.get("b_event_hash"),
            "c8_state_digest": c8_state_digest,
            "e1_event_hash": e1_event_hash,
            "c9_target_id": target_id,
            "tools_from_pre_c9": state["tools_remaining"],
            "native": False,
        }

    def _persist_r31j_binding(self, artifacts, c8_state_digest, e1_event_hash,
                              target_id):
        path = self.root / "bp2_join.json"
        if not path.exists():
            return
        document = json.loads(path.read_text(encoding="utf8"))
        document["r31j_actor_snapshot"] = artifacts.life.a_snapshot
        document["r31j_source"] = self.source
        document["r31j_c8_state_digest"] = c8_state_digest
        document["r31j_e1_event_hash"] = e1_event_hash
        document["r31j_target_id"] = target_id
        path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n",
                        encoding="utf8")

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
            branch_id=branch_id, variant=variant, bind_source=False)

    def material_inspect(self):
        world = self._world(self.branch_id)
        state = world.actor_state["A"]
        if int(state.get("tools_remaining", 0)) < 1:
            self._append_episode(self.branch_id, "A", "DO", world.clock, {
                "action": "material_inspect", "attempted": True,
                "admitted": False, "reason": "GM01_NO_TOOL",
                "gm01_source": self.source,
            })
            self._checkpoint(self.branch_id, world.clock, world)
            return {"status": "DENY", "code": "GM01_NO_TOOL",
                    "attempted": True, "admitted": False, "clock": world.clock}
        event = inspect_event(world, actor_id="A")
        state["tools_remaining"] = int(state["tools_remaining"]) - 1
        state["completed_units"] = int(state.get("completed_units", 0)) + 1
        state["material_remaining"] = max(0, int(state.get("material_remaining", 0)) - 1)
        world.resources["workshop"] = dict(world.resources.get("workshop", {}))
        world.resources["workshop"]["tool_available"] = False
        self.store.append_world_event(self.branch_id, event)
        self._perceive(self.branch_id, "A", event, "own_action")
        self._append_episode(self.branch_id, "A", "DO", world.clock, {
            "action": "material_inspect", "attempted": True, "admitted": True,
            "event_id": event["event_id"],
            "gm01_b_event_ref": self.source.get("b_event_ref"),
            "gm01_b_event_hash": self.source.get("b_event_hash"),
        })
        self._checkpoint(self.branch_id, world.clock, world)
        return {"status": "OK", "attempted": True, "admitted": True,
                "event_id": event["event_id"], "clock": world.clock,
                "actor_state": dict(state)}

    def record_omission(self):
        world = self._world(self.branch_id)
        self._append_episode(self.branch_id, "A", "DO", world.clock, {
            "action": "material_inspect", "attempted": False,
            "admitted": False, "reason": "GM01_A_OMITTED",
            "gm01_b_event_ref": self.source.get("b_event_ref"),
            "gm01_b_event_hash": self.source.get("b_event_hash"),
        })
        self._checkpoint(self.branch_id, world.clock, world)
        return {"status": "NO_CHANGE", "attempted": False, "admitted": False,
                "reason": "GM01_A_OMITTED", "clock": world.clock}
