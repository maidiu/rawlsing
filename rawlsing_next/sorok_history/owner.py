"""Historical-materialization state in the existing Sorok world checkpoint."""

from contextlib import contextmanager
from copy import deepcopy
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import time
from uuid import uuid4


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

    @contextmanager
    def _write(self):
        session = self.session
        db = session.product.store.db
        db.execute("BEGIN IMMEDIATE")
        try:
            world = session.world()
            state = self._state(world)
            before = digest(state)
            yield world, state
            if digest(state) != before:
                world.resources[RESOURCE] = state
                session.product._checkpoint(session.branch_id, world.clock, world)
            db.commit()
        except BaseException:
            db.rollback()
            raise

    @staticmethod
    def _world_readset(world):
        material = world.snapshot()
        material.pop("hash", None)
        material["resources"].pop(RESOURCE, None)
        return digest(material)

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

        with self._write() as (world, state):
            event = self.session.event(particular.occurrence_id)
            already_bound = self._target_id(state, particular.referent_key) in state["targets"]
            if (
                event is None
                or event.get("kind") not in {"ARRIVAL", "MOVE", "REPAIR", "OFFSCREEN_REPAIR"}
                or event.get("location") != particular.location
                or (not already_bound and event.get("clock") != world.clock)
                or not event.get("hash")
            ):
                raise HistoryRefusal("CURRENT_OBJECTIVE_OCCURRENCE_REQUIRED")
            return deepcopy(self._register(state, particular, event, world.clock))

    @staticmethod
    def _target_id(state, key):
        return "history-target:" + digest([state["root"], state["branch"], key])

    def _register(self, state, particular, event, clock):
        target_id = self._target_id(state, particular.referent_key)
        material = asdict(particular)
        dimensions = sorted(set(particular.unresolved))
        material["unresolved"] = dimensions
        previous = state["targets"].get(target_id)
        if previous is not None:
            if previous["surface"] != material:
                raise HistoryRefusal("BOUND_SURFACE_CONFLICT")
            return previous
        target = {
            "id": target_id, "root": state["root"], "branch": state["branch"],
            "surface": material, "parent_hash": event["hash"],
            "admitted_at": clock, "version": 1,
        }
        if dimensions:
            job_id = "history-job:" + digest([target_id, dimensions, target["version"]])
            state["outbox"][job_id] = {
                "id": job_id, "target_id": target_id, "status": "ENQUEUED",
                "trigger": "NEW_WORLD_PARTICULAR", "dimensions": dimensions,
                "target_version": target["version"], "parent_hash": event["hash"],
                "root": state["root"], "branch": state["branch"],
            }
            target["job_id"] = job_id
        state["targets"][target_id] = target
        return target

    def capture_visible_tool_resource(self):
        """Bind the P4 owner's public tool affordance to its place and arrival.

        The owner exposes availability of a local tool resource without an
        individual tool identifier. Preserve that resolution here.
        """
        session = self.session
        with self._write() as (world, state):
            location = world.positions.get(session.meta["user_actor"])
            if not location or world.resources.get(location, {}).get("tool_available") is not True:
                return None
            key = f"world-resource:{location}:tool"
            target_id = self._target_id(state, key)
            if target_id in state["targets"]:
                return target_id
            perceived = session.user_perceived_ids()
            occurrence = next((
                event for event in reversed(session.events())
                if event.get("kind") in {"ARRIVAL", "MOVE"}
                and event.get("location") == location
                and event["event_id"] in perceived
            ), None)
            if occurrence is None:
                return None
            particular = SurfaceParticular(
                occurrence["event_id"], key, "resource", location,
                {"tool_available": True}, ("physical", "provenance"),
            )
            return self._register(state, particular, occurrence, world.clock)["id"]

    def target(self, target_id):
        state = self._state(self.session.world())
        return deepcopy(state["targets"].get(target_id))

    def visible_surfaces(self):
        """Project admitted surface facts available to the current observer."""
        world = self.session.world()
        if RESOURCE not in world.resources:
            return ()
        state = self._state(world)
        actor = self.session.meta["user_actor"]
        location = world.positions.get(actor)
        perceived = self.session.user_perceived_ids()
        return tuple(
            {"id": target["id"], "domain": target["surface"]["domain"],
             "physical": deepcopy(target["surface"]["physical"])}
            for target in state["targets"].values()
            if target["surface"]["location"] == location
            and target["surface"]["occurrence_id"] in perceived
        )

    def pending(self):
        state = self._state(self.session.world())
        return tuple(deepcopy(job) for job in state["outbox"].values()
                     if job["status"] == "ENQUEUED")


    def lease(self, *, seconds=60, now=None):
        """Acquire one durable attempt, recovering expired attempts on reopen."""
        if type(seconds) is not int or not 1 <= seconds <= 600:
            raise HistoryRefusal("INVALID_LEASE_DURATION")
        now = time.time() if now is None else now
        with self._write() as (world, state):
            for job in state["outbox"].values():
                if job["status"] == "RUNNING" and job["expires_at"] <= now:
                    job["status"] = ("FAILED_RETRYABLE" if job["attempt"] < 3
                                     else "FAILED_TERMINAL")
                if job["status"] not in {"ENQUEUED", "FAILED_RETRYABLE"}:
                    continue
                target = state["targets"][job["target_id"]]
                if target["version"] != job["target_version"]:
                    job["status"] = "STALE"
                    continue
                job.update(status="RUNNING", attempt=job.get("attempt", 0) + 1,
                           lease_token=uuid4().hex, expires_at=now + seconds,
                           world_readset=self._world_readset(world))
                return deepcopy({"job": job, "target": target, "world_clock": world.clock})
        return None

    @staticmethod
    def _active_attempt(state, job_id, token, now):
        job = state["outbox"].get(job_id)
        if (job is None or job["status"] != "RUNNING" or job["lease_token"] != token
                or job["expires_at"] <= now):
            raise HistoryRefusal("HISTORICAL_ATTEMPT_NOT_CURRENT")
        return job

    def record_candidate(self, job_id, token, candidate, receipt, *, now=None):
        """Persist provider output in the outbox. Admission remains a separate write."""
        if not isinstance(candidate, dict) or candidate.get("request_id") != job_id:
            raise HistoryRefusal("HISTORICAL_REQUEST_MISMATCH")
        if not isinstance(receipt, dict):
            raise HistoryRefusal("HISTORICAL_RECEIPT_REQUIRED")
        material = json.dumps([candidate, receipt], ensure_ascii=False, allow_nan=False)
        if len(material.encode("utf-8")) > 128_000:
            raise HistoryRefusal("HISTORICAL_RESULT_TOO_LARGE")
        now = time.time() if now is None else now
        with self._write() as (world, state):
            job = self._active_attempt(state, job_id, token, now)
            target = state["targets"][job["target_id"]]
            if (job["world_readset"] != self._world_readset(world)
                    or target["version"] != job["target_version"]):
                job["status"] = "STALE"
            else:
                job.update(status="CANDIDATE_READY", candidate=deepcopy(candidate),
                           provider_receipt=deepcopy(receipt))
            return job["status"]

    def record_failure(self, job_id, token, code, *, retryable=False, now=None):
        if not isinstance(code, str) or not code or len(code) > 100:
            raise HistoryRefusal("INVALID_HISTORICAL_FAILURE_CODE")
        now = time.time() if now is None else now
        with self._write() as (_, state):
            job = self._active_attempt(state, job_id, token, now)
            job.update(failure_code=code, status=(
                "FAILED_RETRYABLE" if retryable and job["attempt"] < 3 else "FAILED_TERMINAL"
            ))
            return job["status"]

    def job(self, job_id):
        return deepcopy(self._state(self.session.world())["outbox"].get(job_id))
