"""Sourcefree I1 joined product: BP2P4J plus the BP4R C12 guard.

The product keeps the BP2P4J source identity and A0-A3 behavior. It replaces
only the C12 storage object with ``GuardedC12Store`` so every read can verify
content, fork origin, and the pinned writer schema. Authenticity remains
``OWNER_ANCHOR_REQUIRED``; this module never invents an external anchor.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .c12_guard import GuardedC12Store, verify_store
from .product import JoinedProduct


class GuardedJoinedProduct(JoinedProduct):
    """The joined product whose C12 store is the guarded reader."""

    def __init__(self, root: str | Path, *, artifacts: Any,
                 branch_id: str = "root", e2: Any = "default",
                 world: Any = None, materialize: bool = True) -> None:
        super().__init__(root, artifacts=artifacts, branch_id=branch_id,
                         e2=e2, world=world, materialize=materialize)
        self._open_guarded_store()

    def _open_guarded_store(self) -> None:
        old = self.store
        old.close()
        self.store = GuardedC12Store(self.root / "c12.sqlite")

    def reenter(self, actor: str = "A") -> dict:
        """Close and reopen the guarded store, then observe as a cold reader."""
        self.store.close()
        self.store = GuardedC12Store(self.root / "c12.sqlite")
        return self.observe(actor=actor)

    def verify_c12(self, branch_id: str | None = None) -> dict:
        """Verify content and fork integrity for the current branch."""
        return verify_store(self.store, branch_id or self.branch_id)

    def owner_material_readout(self, actor: str = "B") -> dict:
        """Owner-only material history; never exposed through A0-A3 ``other``.

        The readout is derived from the persisted C12 checkpoint and the
        source-owned work event. It is marked owner/test-only so a caller
        cannot mistake it for A's public perception.
        """
        state = self.store.latest_state(self.branch_id)
        actor_state = dict(state["actors"].get(actor, {}).get("state", {}))
        events = [
            event for event in self.store.world_events(self.branch_id)
            if event.get("actor_id") == actor
            and event.get("kind") in {"REPAIR", "OFFSCREEN_REPAIR"}
        ]
        latest = events[-1] if events else None
        return {
            "schema": "SOROK_I1_OWNER_MATERIAL_READOUT@1",
            "visibility": "OWNER_TEST_ONLY",
            "branch_id": self.branch_id,
            "actor": actor,
            "state": {
                "position": state["world"]["positions"].get(actor),
                "cash": actor_state.get("cash"),
                "material_remaining": actor_state.get("material_remaining"),
                "free_hours": actor_state.get("free_hours"),
                "completed_units": actor_state.get("completed_units"),
            },
            "latest_work_event": None if latest is None else {
                "event_id": latest["event_id"],
                "kind": latest["kind"],
                "clock": latest["clock"],
                "location": latest["location"],
                "body": latest.get("body", {}),
            },
        }

    def close(self) -> None:
        self.store.close()


__all__ = ["GuardedJoinedProduct"]
