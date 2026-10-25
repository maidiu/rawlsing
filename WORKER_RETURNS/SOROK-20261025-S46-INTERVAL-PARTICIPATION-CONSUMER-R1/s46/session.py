"""S46 interval participation over the actual S45 generated-root person."""
from __future__ import annotations

from .bootstrap import install

install()

from s41.event import world_prerequisites  # noqa: E402
from s45.session import S45Session  # noqa: E402

from .producer import (
    STATE_GRADE,
    STATE_KIND,
    STATE_SCHEMA,
    produce_interval as _produce_interval,
    read_interval_states as _read_interval_states,
    validate_interval_state as _validate_interval_state,
)

S46_SCHEMA = "SOROK_S46_INTERVAL_PARTICIPATION_SESSION@1"


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

    def world_prerequisites(self) -> dict:
        return world_prerequisites(self)

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
