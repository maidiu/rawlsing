"""Historical-materialization state in the existing Sorok world checkpoint."""

from copy import deepcopy
from dataclasses import asdict, dataclass
from hashlib import sha256
import json


RESOURCE = "sorok.historical_materialization.v1"
DOMAINS = frozenset({"item", "artifact", "collection", "place", "resource", "social_form"})
DIMENSIONS = frozenset({"physical", "provenance", "participation", "dependencies"})


class HistoryRefusal(ValueError):
    """A typed refusal at the historical world boundary."""


def digest(document):
    data = json.dumps(document, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)
    return sha256(data.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SurfaceParticular:
    """Typed objective assertion supplied by the foreground world adapter."""

    occurrence_id: str
    referent_key: str
    domain: str
    location: str
    physical: dict[str, str | int | bool]
    unresolved: tuple[str, ...]


class HistoricalWorld:
    """Use the same branch store, clock and checkpoint as the foreground owner."""

    def __init__(self, session):
        self.session = session

    def scope(self):
        return self.session.read_root()["root_hash"], self.session.branch_id

    def _state(self, world):
        root, branch = self.scope()
        state = world.resources.get(RESOURCE)
        if state is None:
            return {"root": root, "branch": branch, "targets": {}, "outbox": {}}
        if (state["root"], state["branch"]) != (root, branch):
            raise HistoryRefusal("WORLD_HISTORY_SCOPE_MISMATCH")
        return state

    def admit_surface(self, particular: SurfaceParticular):
        """Commit existence and the first historical demand in one checkpoint."""
        if not isinstance(particular, SurfaceParticular):
            raise HistoryRefusal("OBJECTIVE_SURFACE_REQUIRED")
        if (
            not particular.referent_key or not particular.location
            or particular.domain not in DOMAINS
            or not isinstance(particular.physical, dict)
            or any(
                not isinstance(key, str) or not key or type(value) not in (str, int, bool)
                for key, value in particular.physical.items()
            )
            or not set(particular.unresolved) <= DIMENSIONS
        ):
            raise HistoryRefusal("INVALID_SURFACE_PARTICULAR")

        session = self.session
        db = session.product.store.db
        db.execute("BEGIN IMMEDIATE")
        try:
            world = session.world()
            state = self._state(world)
            root, branch = self.scope()
            target_id = "history-target:" + digest([root, branch, particular.referent_key])
            material = asdict(particular)
            dimensions = sorted(set(particular.unresolved))
            material["unresolved"] = dimensions
            previous = state["targets"].get(target_id)
            if previous is not None:
                if previous["surface"] != material:
                    raise HistoryRefusal("BOUND_SURFACE_CONFLICT")
                db.commit()
                return deepcopy(previous)

            event = session.event(particular.occurrence_id)
            if (
                event is None or event.get("kind") not in {"ARRIVAL", "MOVE", "REPAIR", "OFFSCREEN_REPAIR"}
                or event.get("location") != particular.location
                or event.get("clock") != world.clock
                or not event.get("hash")
            ):
                raise HistoryRefusal("CURRENT_OBJECTIVE_OCCURRENCE_REQUIRED")

            target = {
                "id": target_id, "root": root, "branch": branch,
                "surface": material, "parent_hash": event["hash"],
                "admitted_at": world.clock, "version": 1,
            }
            if dimensions:
                job_id = "history-job:" + digest([target_id, dimensions, target["version"]])
                state["outbox"][job_id] = {
                    "id": job_id, "target_id": target_id, "status": "ENQUEUED",
                    "trigger": "NEW_WORLD_PARTICULAR", "dimensions": dimensions,
                    "target_version": target["version"], "parent_hash": event["hash"],
                    "root": root, "branch": branch,
                }
                target["job_id"] = job_id
            state["targets"][target_id] = target
            world.resources[RESOURCE] = state
            session.product._checkpoint(branch, world.clock, world)
            db.commit()
            return deepcopy(target)
        except BaseException:
            db.rollback()
            raise

    def target(self, target_id):
        state = self._state(self.session.world())
        return deepcopy(state["targets"].get(target_id))

    def pending(self):
        state = self._state(self.session.world())
        return tuple(deepcopy(job) for job in state["outbox"].values()
                     if job["status"] == "ENQUEUED")
