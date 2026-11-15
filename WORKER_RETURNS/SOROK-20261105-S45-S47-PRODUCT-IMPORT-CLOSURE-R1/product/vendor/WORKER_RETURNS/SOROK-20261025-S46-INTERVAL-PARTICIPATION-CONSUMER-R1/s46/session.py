"""S46 interval participation over the actual S45 generated-root person."""
from __future__ import annotations

from .bootstrap import install

install()

from s41.event import world_prerequisites  # noqa: E402
from s45.session import S45Session  # noqa: E402

from .errors import S46Refusal  # noqa: E402

from .producer import (
    STATE_GRADE,
    STATE_KIND,
    STATE_SCHEMA,
    produce_interval as _produce_interval,
    read_interval_states as _read_interval_states,
    validate_interval_state as _validate_interval_state,
)

S46_SCHEMA = "SOROK_S46_INTERVAL_PARTICIPATION_SESSION@1"
CONDITION_REVOKED_KIND = "S46_INTERVAL_CONDITION_REVOKED"
CONDITION_RESTORED_KIND = "S46_INTERVAL_CONDITION_RESTORED"


class S46Session(S45Session):
    """Same S45/S44 person with actual bounded interval participation."""

    def produce_interval(self, domain: dict) -> dict:
        return _produce_interval(self, domain)

    def read_interval_states(self) -> list[dict]:
        return _read_interval_states(self)

    def validate_interval_state(self, state: dict) -> dict:
        return _validate_interval_state(self, state)

    def current_interval_state(self, scope_id: str | None = None) -> dict | None:
        rows = [
            row for row in self.read_interval_states()
            if (scope_id is None or row.get("scope_id") == scope_id)
            and row.get("currentness") == "CURRENT"
        ]
        return rows[-1] if rows else None

    def _condition_revoked(self, state_id: str) -> bool:
        rows = [
            row for row in self.product.store.episodes(self.branch_id)
            if row.get("kind") in {
                CONDITION_REVOKED_KIND, CONDITION_RESTORED_KIND,
            }
            and (row.get("body") or {}).get("state_id") == state_id
        ]
        if not rows:
            return False
        return rows[-1].get("kind") == CONDITION_REVOKED_KIND

    def revoke_interval_condition(self, state_id: str, *,
                                  reason: str = "TEST_ONLY_REVOCATION") -> dict:
        state = self.read_interval_states()
        if not any(row.get("state_id") == state_id for row in state):
            raise S46Refusal("S46_INTERVAL_STATE_UNKNOWN", state_id)
        body = {
            "schema": "S46_INTERVAL_CONDITION_CHANGE@1",
            "state_id": state_id,
            "branch_id": self.branch_id,
            "reason": reason,
            "clock": self.clock(),
            "product_model_calls": 0,
        }
        episode = self.product._append_episode(
            self.branch_id, "A", CONDITION_REVOKED_KIND,
            self.clock(), body,
        )
        self.product._checkpoint(self.branch_id, self.clock(), self.world())
        return {**body, "episode_id": episode["episode_id"]}

    def restore_interval_condition(self, state_id: str, *,
                                   reason: str = "TEST_ONLY_RESTORE") -> dict:
        body = {
            "schema": "S46_INTERVAL_CONDITION_CHANGE@1",
            "state_id": state_id,
            "branch_id": self.branch_id,
            "reason": reason,
            "clock": self.clock(),
            "product_model_calls": 0,
        }
        episode = self.product._append_episode(
            self.branch_id, "A", CONDITION_RESTORED_KIND,
            self.clock(), body,
        )
        self.product._checkpoint(self.branch_id, self.clock(), self.world())
        return {**body, "episode_id": episode["episode_id"]}

    def _world_prerequisites(self) -> dict:
        base = world_prerequisites(self)
        states = self.read_interval_states()
        current = [
            row for row in states if row.get("currentness") == "CURRENT"
        ]
        if not current:
            return base
        state = current[-1]
        if self._condition_revoked(state["state_id"]):
            raise S46Refusal("S46_INTERVAL_CONDITION_REVOKED", state["state_id"])
        latest_segment = state.get("segments", [])[-1] if state.get("segments") else {}
        after = (latest_segment.get("world") or {}).get("state_after") or {}
        return {
            **base,
            "s46_interval": {
                "state_id": state["state_id"],
                "status": state["status"],
                "coverage": state["coverage"],
                "currentness": state["currentness"],
                "receipt_hash": state["receipt_hash"],
                "condition_revoked": False,
                "material_after_interval": bool(after.get("material_remaining", 0)),
                "free_hours_after_interval": bool(after.get("free_hours", 0)),
                "tools_after_interval": int(after.get("tools_remaining", 0)),
            },
        }

    def world_prerequisites(self) -> dict:
        return self._world_prerequisites()

    def verify(self) -> dict:
        result = super().verify()
        try:
            states = self.read_interval_states()
            result["s46_intervals"] = {
                "status": "OK",
                "count": len(states),
                "states": [
                    {
                        "state_id": row.get("state_id"),
                        "status": row.get("status"),
                        "coverage": row.get("coverage"),
                        "scope_id": row.get("scope_id"),
                        "currentness": row.get("currentness"),
                        "superseded_by": row.get("superseded_by"),
                    }
                    for row in states
                ],
            }
            intervals_ok = True
        except Exception as exc:
            result["s46_intervals"] = {
                "status": "REFUSED",
                "code": getattr(exc, "code", type(exc).__name__),
            }
            intervals_ok = False
        result["ok"] = bool(result.get("ok")) and intervals_ok
        return result


__all__ = [
    "S46Session", "S46_SCHEMA", "STATE_KIND", "STATE_SCHEMA", "STATE_GRADE",
]
