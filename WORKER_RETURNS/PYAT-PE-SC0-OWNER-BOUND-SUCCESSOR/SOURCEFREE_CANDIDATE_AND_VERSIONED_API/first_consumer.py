"""In-candidate TEST_ONLY_SOURCEFREE receiving consumer.

This is a receiving exercise for the owner-bound receipt, not an operative N9
consumer, not an actor/person generator and not a scientific adoption.
"""
from __future__ import annotations

from typing import Any, Mapping

from owner_bound_successor import SERVICE_GRADE

CONSUMER_ID = "TEST_ONLY_SOURCEFREE_WORLD_ROUTE_CONSUMER@1"


class SourceFreeWorldRouteConsumer:
    def __init__(self, *, consumer_id: str = CONSUMER_ID) -> None:
        self.consumer_id = consumer_id

    def consume(
        self,
        *,
        request: Any,
        world: Mapping[str, Any],
        target_cell: str,
        target_fraction: Any,
    ) -> Mapping[str, Any]:
        values = world.get("values")
        if not isinstance(values, Mapping):
            raise ValueError("consumer requires world values")
        sanctions = values.get("public_sanctions")
        horizon = values.get("absolute_horizon")
        routes = [
            {
                "route": "ROUTE_RECORDED_SANCTIONS_CONSTRAINED",
                "sanctions_ref": "world:public_sanctions",
                "horizon_ref": "world:absolute_horizon",
                "horizon": horizon,
                "sanction_count": len(sanctions) if isinstance(sanctions, list) else 0,
            }
        ]
        return {
            "consumer_id": self.consumer_id,
            "consumer_grade": (
                f"{SERVICE_GRADE}__IN_CANDIDATE_FIRST_CONSUMER_ONLY"
            ),
            "world_owner": world.get("world_owner"),
            "world_revision": world.get("revision"),
            "world_selection_digest": world.get("selection_digest"),
            "target_cell": target_cell,
            "target_fraction": target_fraction,
            "route_constraints": routes,
            "no_person_generation": True,
            "no_actor_state": True,
            "scientific_claim": "NONE__TEST_ONLY_SOURCEFREE_ROUTE_READ",
        }


__all__ = ["CONSUMER_ID", "SourceFreeWorldRouteConsumer"]
