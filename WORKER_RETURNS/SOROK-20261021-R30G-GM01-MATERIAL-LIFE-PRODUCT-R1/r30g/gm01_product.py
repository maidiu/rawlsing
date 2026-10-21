"""R30G product: R29P cold C12 product with GM01 material feasibility overlay."""
from __future__ import annotations

from pathlib import Path

from bp4.world import WorldState, inspect_event
from r29p.product import R29PProduct


class GM01Product(R29PProduct):
    """R29P product with an explicit GM01 material start and performed E2 method."""

    def __init__(self, root, *, artifacts, branch_id="root",
                 variant="A_REPAIR_LONG", gm01=None, **kwargs):
        self.gm01 = gm01
        super().__init__(root, artifacts=artifacts, branch_id=branch_id,
                         variant=variant, **kwargs)
        if gm01 is not None:
            self.apply_material_start(
                tools=1 if gm01.get("material_feasible_after") else 0,
                gm01_receipt_hash=gm01.get("result_hash", ""))

    def apply_material_start(self, *, tools: int, gm01_receipt_hash: str = ""):
        world = self._world(self.branch_id)
        state = world.actor_state["A"]
        state["tools_remaining"] = int(tools)
        state["material_remaining"] = max(2, int(state.get("material_remaining", 2)))
        world.resources["workshop"] = dict(world.resources.get("workshop", {}))
        world.resources["workshop"]["tool_available"] = bool(tools)
        self._checkpoint(self.branch_id, world.clock, world)
        self.material_start_receipt = {
            "schema": "R30G_GM01_MATERIAL_START@1",
            "tools_for_a": int(tools),
            "gm01_receipt_hash": gm01_receipt_hash,
            "world_clock": world.clock,
            "world_hash": world.snapshot()["hash"],
        }

    def material_inspect(self):
        """A's own later material inspection, or a typed denial without a tool."""
        world = self._world(self.branch_id)
        state = world.actor_state["A"]
        tools = int(state.get("tools_remaining", 0))
        if tools < 1:
            self._append_episode(self.branch_id, "A", "DO", world.clock, {
                "action": "material_inspect", "attempted": True,
                "admitted": False, "reason": "GM01_NO_TOOL",
                "gm01_receipt_hash": getattr(self, "gm01", {}).get("result_hash", ""),
            })
            self._checkpoint(self.branch_id, world.clock, world)
            return {"status": "DENY", "code": "GM01_NO_TOOL",
                    "attempted": True, "admitted": False,
                    "clock": world.clock}
        event = inspect_event(world, actor_id="A")
        state["tools_remaining"] = tools - 1
        state["completed_units"] = int(state.get("completed_units", 0)) + 1
        state["material_remaining"] = max(0, int(state.get("material_remaining", 0)) - 1)
        world.resources["workshop"] = dict(world.resources.get("workshop", {}))
        world.resources["workshop"]["tool_available"] = False
        self.store.append_world_event(self.branch_id, event)
        self._perceive(self.branch_id, "A", event, "own_action")
        self._append_episode(self.branch_id, "A", "DO", world.clock, {
            "action": "material_inspect", "attempted": True, "admitted": True,
            "event_id": event["event_id"],
            "gm01_receipt_hash": getattr(self, "gm01", {}).get("result_hash", ""),
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
            "gm01_receipt_hash": getattr(self, "gm01", {}).get("result_hash", ""),
        })
        self._checkpoint(self.branch_id, world.clock, world)
        return {"status": "NO_CHANGE", "attempted": False, "admitted": False,
                "reason": "GM01_A_OMITTED", "clock": world.clock}
