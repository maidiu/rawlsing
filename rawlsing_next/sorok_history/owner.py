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
VISIBLE_PHYSICAL = frozenset({"color", "condition", "marking", "texture"})
PHYSICAL_TYPES = {
    "color": str, "material": str, "condition": str, "marking": str, "texture": str,
    "length_mm": int, "width_mm": int, "height_mm": int, "mass_grams": int,
}


def _valid_physical_value(predicate, value):
    if type(value) is not PHYSICAL_TYPES[predicate]:
        return False
    if isinstance(value, int):
        return 0 < value <= 100_000_000
    return bool(value.strip()) and len(value) <= 160


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

    def root_tool_baseline(self, location):
        """Read a tool affordance from the existing sealed pre-contact world."""
        store = self.session.product.store
        if not self.session.product.c12_verify("root").get("ok"):
            raise HistoryRefusal("HISTORICAL_ROOT_BASELINE_UNVERIFIED")
        checkpoint = store.checkpoints("root")[0]
        world = checkpoint["state"]["world"]
        resource = world["resources"].get(location, {})
        available = resource.get("tool_available")
        if type(available) is not bool:
            return None
        root, _ = self.scope()
        return {
            "root": root, "root_checkpoint_hash": checkpoint["hash"],
            "clock": world["clock"], "location": location,
            "tool_available": available,
        }

    def _state(self, world):
        root, branch = self.scope()
        state = world.resources.get(RESOURCE)
        empty = {"root": root, "branch": branch, "targets": {}, "outbox": {}}
        if state is None:
            return empty
        if (state["root"], state["branch"]) == (root, branch):
            return state
        store = self.session.product.store
        if (state["root"] == root
                and store.inherits_verified_prefix(branch, state["branch"])):
            # This resource contains only branch-local admissions. The BP4 fork
            # copies checkpoint bytes, but their targets and leases stay parent-owned.
            return empty
        raise HistoryRefusal("WORLD_HISTORY_SCOPE_MISMATCH")

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

    @staticmethod
    def _parent_index(state):
        if "targets_by_parent" in state:
            return state["targets_by_parent"]
        index = {}
        for target in state["targets"].values():
            index.setdefault(target["surface"]["occurrence_id"], []).append(target["id"])
        return index

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
        index = self._parent_index(state)
        index.setdefault(event["event_id"], []).append(target_id)
        state["targets_by_parent"] = index
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

    @staticmethod
    def _completed_unit_event(event):
        body = event.get("body", {})
        return (event.get("kind") == "REPAIR" and body.get("source_owned") is True
                and type(body.get("completed_delta")) is int and body["completed_delta"] == 1
                and bool(event.get("location")))

    def _repair_link(self, world, target, event):
        if (target["surface"]["referent_key"] != f'completed-unit:{event["event_id"]}'
                or event["hash"] != target["parent_hash"]
                or not self._completed_unit_event(event)):
            return None
        actor_id = world.actor_state.get(event["actor_id"], {}).get("actor_id")
        if actor_id not in self.session.read_root()["actor_ids"]:
            return None
        root = target["root"]
        actor = {"kind": "ACTOR", "object_id": actor_id,
                 "content_hash": digest({"root": root, "actor_id": actor_id})}
        link = {
            "target_id": target["id"], "relation": "PERFORMED_REPAIR",
            "actor_ref": actor, "event_id": event["event_id"], "event_hash": event["hash"],
            "clock": event["clock"], "root": root, "branch": target["branch"],
        }
        return {"edge_id": "history-link:" + digest(link), **link}

    def _register_completed_unit(self, state, event, world):
        event_id = event["event_id"]
        particular = SurfaceParticular(
            event_id, f"completed-unit:{event_id}", "artifact", event["location"],
            {"completed_units": 1}, ("physical", "provenance"),
        )
        target = self._register(state, particular, event, world.clock)
        link = self._repair_link(world, target, event)
        if link is not None:
            actor_id = link["actor_ref"]["object_id"]
            state.setdefault("repair_links_by_actor", {}).setdefault(actor_id, {})[
                target["id"]
            ] = link
        return target["id"]

    def repair_links_for_actor(self, actor_id):
        """Return branch-owned objective participation to a trusted world consumer."""
        world = self.session.world()
        state = self._state(world)
        return self._repair_links_for_actor(world, state, actor_id)

    def _repair_links_for_actor(self, world, state, actor_id):
        indexed = state.get("repair_links_by_actor", {}).get(actor_id, {})
        links = []
        for target_id, link in sorted(indexed.items()):
            target = state["targets"].get(target_id)
            event = self.session.event(link["event_id"])
            if target is not None and event is not None:
                actual = self._repair_link(world, target, event)
                if actual == link:
                    links.append(actual)
        return tuple(links)

    def _local_events(self, branch_id):
        branch = self.session.product.store.branch(branch_id)
        inherited = branch["root_counts"].get("world_event", 0) if branch["parent_branch_id"] else 0
        return self.session.events()[inherited:]

    def capture_completed_unit(self, event_id, event_hash):
        """Bind one completed output at the resolution of an actual repair event."""
        with self._write() as (world, state):
            event = self.session.event(event_id)
            if (event is None or event.get("hash") != event_hash
                    or event.get("kind") != "REPAIR" or event["clock"] > world.clock
                    or event not in world.events
                    or event not in self._local_events(state["branch"])):
                raise HistoryRefusal("HISTORICAL_REPAIR_PARENT_REQUIRED")
            if not self._completed_unit_event(event):
                raise HistoryRefusal("HISTORICAL_COMPLETED_UNIT_REQUIRED")
            return self._register_completed_unit(state, event, world)

    def recover_completed_units(self):
        """Recover repair obligations from this branch's committed world events."""
        with self._write() as (world, state):
            checkpoint_events = {event["event_id"]: event["hash"] for event in world.events}
            for event in self._local_events(state["branch"]):
                if (self._completed_unit_event(event)
                        and checkpoint_events.get(event["event_id"]) == event["hash"]):
                    self._register_completed_unit(state, event, world)

    def target(self, target_id):
        state = self._state(self.session.world())
        return deepcopy(state["targets"].get(target_id))

    def target_for_referent(self, referent_key, *, location=None):
        """Resolve exactly one committed target from the owner index."""
        state = self._state(self.session.world())
        matches = [
            target for target in state["targets"].values()
            if target["surface"].get("referent_key") == referent_key
            and (location is None or target["surface"].get("location") == location)
        ]
        if len(matches) != 1:
            return None
        return deepcopy(matches[0])

    def hold_activity_requirement(self, requirement):
        """Persist an exact dispatch requirement before any physical interval."""
        if not isinstance(requirement, dict) or not isinstance(requirement.get("id"), str):
            raise HistoryRefusal("INVALID_ACTIVITY_REQUIREMENT")
        if not requirement["id"] or not requirement.get("target_id"):
            raise HistoryRefusal("INVALID_ACTIVITY_REQUIREMENT")
        with self._write() as (_, state):
            requirements = state.setdefault("activity_requirements", {})
            previous = requirements.get(requirement["id"])
            if previous is not None:
                stable = {"world_readset", "dispatch_receipt", "status", "target_version"}
                if any(
                    previous.get(key) != requirement.get(key)
                    for key in (set(previous) | set(requirement)) - stable
                ):
                    raise HistoryRefusal("ACTIVITY_REQUIREMENT_CONFLICT")
                return deepcopy(previous)
            requirements[requirement["id"]] = deepcopy(requirement)
            return deepcopy(requirement)

    def activity_requirement(self, requirement_id):
        state = self._state(self.session.world())
        return deepcopy(state.get("activity_requirements", {}).get(requirement_id))

    def activity_requirements(self, status=None):
        state = self._state(self.session.world())
        rows = state.get("activity_requirements", {}).values()
        return tuple(
            deepcopy(row) for row in sorted(rows, key=lambda row: row["id"])
            if status is None or row.get("status") == status
        )

    def mark_activity_requirement(self, requirement_id, status, *, receipt=None):
        if status not in {"DISPATCHING", "AMBIGUOUS", "HELD", "CONSUMED", "INVALIDATED"}:
            raise HistoryRefusal("INVALID_ACTIVITY_REQUIREMENT_STATUS")
        with self._write() as (_, state):
            requirement = state.get("activity_requirements", {}).get(requirement_id)
            if requirement is None:
                raise HistoryRefusal("ACTIVITY_REQUIREMENT_NOT_FOUND")
            if requirement.get("status") == "CONSUMED":
                return deepcopy(requirement)
            requirement["status"] = status
            if receipt is not None:
                requirement["dispatch_receipt"] = deepcopy(receipt)
            return deepcopy(requirement)

    # Explicit negative-test interfaces. These are not ordinary dispatch writes.
    def test_detach_physical_depth(self, target_id, predicate):
        """Detach one committed depth fact for a durable severance test."""
        with self._write() as (_, state):
            target = state["targets"].get(target_id)
            if target is None or predicate not in target.get("physical_depth", {}):
                raise HistoryRefusal("HISTORICAL_DEPTH_NOT_FOUND")
            fact = target["physical_depth"].pop(predicate)
            target["version"] += 1
            return deepcopy(fact)

    def test_restore_physical_depth(self, target_id, fact):
        """Restore the exact detached fact for the matching negative test."""
        if not isinstance(fact, dict) or not fact.get("predicate"):
            raise HistoryRefusal("INVALID_HISTORICAL_DEPTH_FACT")
        with self._write() as (_, state):
            target = state["targets"].get(target_id)
            if target is None:
                raise HistoryRefusal("HISTORICAL_TARGET_UNKNOWN")
            target.setdefault("physical_depth", {})[fact["predicate"]] = deepcopy(fact)
            target["version"] += 1
            return deepcopy(target["physical_depth"][fact["predicate"]])

    def test_set_actor_position(self, actor_id, location):
        """Set an actor position for wrong-place dispatch tests only."""
        with self._write() as (world, state):
            if actor_id not in world.positions or not isinstance(location, str):
                raise HistoryRefusal("INVALID_ACTIVITY_PLACE_TEST")
            world.positions[actor_id] = location
            state["test_mutation"] = state.get("test_mutation", 0) + 1

    def test_set_resource_property(self, location, predicate, value):
        """Set a world resource property for contradiction tests only."""
        with self._write() as (world, state):
            world.resources.setdefault(location, {})[predicate] = value
            state["test_mutation"] = state.get("test_mutation", 0) + 1

    def visible_surfaces(self):
        """Project admitted surface facts available to the current observer."""
        world = self.session.world()
        if RESOURCE not in world.resources:
            return ()
        state = self._state(world)
        actor = self.session.meta["user_actor"]
        location = world.positions.get(actor)
        index = self._parent_index(state)
        ids = {target_id for event_id in self.session.user_perceived_ids()
               for target_id in index.get(event_id, ())}
        result = []
        for target_id in sorted(ids):
            target = state["targets"][target_id]
            surface = target["surface"]
            if surface["location"] == location:
                result.append({"id": target_id, "domain": surface["domain"],
                               "physical": deepcopy(surface["physical"])})
        return tuple(result)

    def pending(self):
        state = self._state(self.session.world())
        return tuple(deepcopy(job) for job in state["outbox"].values()
                     if job["status"] == "ENQUEUED")


    def ready_candidate_id(self):
        state = self._state(self.session.world())
        return next((job_id for job_id, job in state["outbox"].items()
                     if job["status"] == "CANDIDATE_READY"), None)

    def _prior_repair_context(self, world, state, target):
        event = self.session.event(target["surface"]["occurrence_id"])
        link = self._repair_link(world, target, event) if event is not None else None
        if link is None:
            return []
        actor_id = link["actor_ref"]["object_id"]
        prior = [row for row in self._repair_links_for_actor(world, state, actor_id)
                 if row["clock"] < link["clock"]]
        return sorted(prior, key=lambda row: (row["clock"], row["event_id"]))[-2:]

    def _constraint_packet(self, world, target, job):
        """Assemble a bounded packet exclusively from owner-bound material."""
        surface = target["surface"]
        event = self.session.event(surface["occurrence_id"])
        if event is None or event.get("hash") != target["parent_hash"]:
            raise HistoryRefusal("HISTORICAL_PARENT_MISSING")

        def ref(kind, object_id, content_hash):
            return {"kind": kind, "object_id": object_id, "content_hash": content_hash}

        root, branch = target["root"], target["branch"]
        target_id = target["id"]
        authority = {
            "policy": "SOROK_HISTORY_SOURCEFREE_PHYSICAL_V1",
            "root": root, "branch": branch, "target": target_id,
            "grade": "SOURCEFREE_TEST_ONLY", "allowed_H_classes": ["H0"],
        }
        facts = []
        for predicate, value in sorted(surface["physical"].items()):
            body = {"target_id": target_id, "predicate": predicate, "value": value,
                    "state": "KNOWN"}
            checksum = digest(body)
            facts.append({**body, "ref": ref("KNOWN_FACT", "surface:" + checksum, checksum)})
        requested = job.get("requested_predicate")
        if requested is not None:
            for predicate, row in sorted(target.get("physical_depth", {}).items()):
                facts.append({
                    "target_id": target_id, "predicate": predicate, "value": row["value"],
                    "state": "KNOWN", "ref": ref("FACT", row["id"], digest(row)),
                })
        known_refs = [fact["ref"] for fact in facts]
        occurrence = ref("WORLD_EVENT", event["event_id"], event["hash"])
        target_ref = ref("WORLD_TARGET", target_id, digest(target))
        chronology = {"time": world.clock, "window": [target["admitted_at"], world.clock]}
        # Reconstruct previously persisted packets with their original schema.
        if job.get("chronology_bound"):
            chronology["window"][0] = min(target["admitted_at"], event["clock"])
            chronology["records"] = [{
                "ref": occurrence, "time": event["clock"], "targets": [target_id],
            }]
        actor_refs = []
        link = self._repair_link(world, target, event) if job.get("repair_actor_bound") else None
        if link is not None:
            identity = link["actor_ref"]
            actor_refs.append(identity)
            chronology["records"][0]["participants"] = [
                {"role": link["relation"], "actor_ref": identity},
            ]
        return {
            "schema": "SOROK_HISTORY_ADMISSION_PACKET@1",
            "request_id": job["id"], "root": root, "branch": branch, "time": world.clock,
            "target_ids": [target_id],
            "surface": {target_id: {
                "domain": surface["domain"], "location": surface["location"],
                "physical": deepcopy(surface["physical"]),
                "allowed_physical_predicates": {
                    name: value_type.__name__ for name, value_type in PHYSICAL_TYPES.items()
                },
                "known_fact_refs": known_refs, "unresolved": list(job["dimensions"]),
                **({"requested_predicate": requested} if requested is not None else {}),
                **({"prior_actor_repairs": job["prior_actor_repairs"]}
                   if job.get("prior_actor_repairs") else {}),
                **({"root_tool_baseline": job["root_tool_baseline"]}
                   if job.get("root_tool_baseline") else {}),
            }},
            "known_facts": facts,
            "world_refs": [target_ref],
            "actor_refs": actor_refs,
            "event_refs": [occurrence],
            "authority": {
                **authority,
                "ref": ref("AUTHORITY", authority["policy"], digest(authority)),
                "valid_from": target["admitted_at"], "valid_to": world.clock,
            },
            "chronology": chronology,
            "causal_closure": {"allowed_slack_refs": []},
            "world_readset": job["world_readset"],
            "source_limits": ["ACTOR_HISTORY_NOT_ISSUED", "PAST_EVENT_ADMISSION_NOT_ISSUED"],
        }

    def lease(self, *, seconds=60, now=None):
        """Acquire one durable attempt, recovering expired attempts on reopen."""
        if type(seconds) is not int or not 1 <= seconds <= 600:
            raise HistoryRefusal("INVALID_LEASE_DURATION")
        now = time.time() if now is None else now
        with self._write() as (world, state):
            jobs = sorted(
                state["outbox"].values(),
                key=lambda job: ("inspection_priority_event" not in job, job["status"] == "STALE"),
            )
            for job in jobs:
                if job["status"] == "RUNNING" and job["expires_at"] <= now:
                    job["status"] = ("FAILED_RETRYABLE" if job["attempt"] < 3
                                     else "FAILED_TERMINAL")
                if job["status"] not in {"ENQUEUED", "FAILED_RETRYABLE", "STALE"}:
                    continue
                if job.get("attempt", 0) >= 3:
                    continue
                target = state["targets"][job["target_id"]]
                if target["version"] != job["target_version"]:
                    predicate = job.get("requested_predicate")
                    if predicate is None:
                        job["status"] = "STALE"
                        continue
                    if (predicate in target["surface"]["physical"]
                            or predicate in target.get("physical_depth", {})):
                        job["status"] = "NO_WORK"
                        continue
                    job["target_version"] = target["version"]
                if job["status"] == "STALE":
                    job.setdefault("stale_attempts", []).append({
                        "attempt": job["attempt"], "packet_hash": job["packet_hash"],
                        "provider_receipt": job.pop("provider_receipt", None),
                    })
                    job.pop("candidate", None)
                    job.pop("admission", None)
                job.update(status="RUNNING", attempt=job.get("attempt", 0) + 1,
                           lease_token=uuid4().hex, expires_at=now + seconds,
                           world_readset=self._world_readset(world), chronology_bound=True,
                           repair_actor_bound=True)
                job["prior_actor_repairs"] = self._prior_repair_context(world, state, target)
                surface = target["surface"]
                location = surface["location"]
                if surface["referent_key"] == f"world-resource:{location}:tool":
                    job["root_tool_baseline"] = self.root_tool_baseline(location)
                try:
                    packet = self._constraint_packet(world, target, job)
                except HistoryRefusal as exc:
                    if str(exc) != "HISTORICAL_PARENT_MISSING":
                        raise
                    self._hold_missing_parent(job)
                    continue
                job["packet_hash"] = digest(packet)
                return deepcopy({"job": job, "target": target, "world_clock": world.clock,
                                 "packet": packet})
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
                job.update(status="STALE", provider_receipt=deepcopy(receipt))
            else:
                job.update(status="CANDIDATE_READY", candidate=deepcopy(candidate),
                           provider_receipt=deepcopy(receipt))
            return job["status"]

    def record_failure(self, job_id, token, code, *, retryable=False, receipt=None, now=None):
        if not isinstance(code, str) or not code or len(code) > 100:
            raise HistoryRefusal("INVALID_HISTORICAL_FAILURE_CODE")
        now = time.time() if now is None else now
        with self._write() as (_, state):
            job = self._active_attempt(state, job_id, token, now)
            if receipt is not None:
                job["provider_receipt"] = deepcopy(receipt)
            job.update(failure_code=code, status=(
                "FAILED_RETRYABLE" if retryable and job["attempt"] < 3 else "FAILED_TERMINAL"
            ))
            return job["status"]

    def job(self, job_id):
        return deepcopy(self._state(self.session.world())["outbox"].get(job_id))

    @staticmethod
    def _hold_missing_parent(job):
        job.update(status="SOURCE_HELD", admission={
            "status": "SOURCE_HELD", "job_id": job["id"],
            "reason": "HISTORICAL_PARENT_MISSING",
        })
        return deepcopy(job["admission"])

    def commit_candidate(self, job_id):
        """Evaluate a current candidate and bind accepted physical facts atomically."""
        from rawlsing_next.sorok_history.admission import evaluate

        with self._write() as (world, state):
            job = state["outbox"].get(job_id)
            if job is None:
                raise HistoryRefusal("HISTORICAL_JOB_NOT_FOUND")
            if "admission" in job:
                return deepcopy(job["admission"])
            if job["status"] != "CANDIDATE_READY":
                raise HistoryRefusal("HISTORICAL_CANDIDATE_NOT_READY")
            target = state["targets"][job["target_id"]]
            if (job["world_readset"] != self._world_readset(world)
                    or target["version"] != job["target_version"]):
                job["status"] = "STALE"
                job["admission"] = {"status": "STALE", "job_id": job_id}
                return deepcopy(job["admission"])
            try:
                packet = self._constraint_packet(world, target, job)
            except HistoryRefusal as exc:
                if str(exc) != "HISTORICAL_PARENT_MISSING":
                    raise
                return self._hold_missing_parent(job)
            if digest(packet) != job["packet_hash"]:
                job.update(status="STALE", admission={
                    "status": "STALE", "job_id": job_id,
                    "reason": "HISTORICAL_PACKET_READSET_MISMATCH",
                })
                return deepcopy(job["admission"])

            result = evaluate(packet, job["candidate"])
            accepted = []
            held = list(result["held"])
            rejected = list(result["rejected"])
            physical = target.get("physical_depth", {}).copy()
            owner_refs = {
                digest(ref)
                for ref in (packet["event_refs"] + packet["world_refs"]
                            + [packet["authority"]["ref"]]
                            + [fact["ref"] for fact in packet["known_facts"]])
            }
            admitted_groups = {}
            for group in result["accepted_groups"]:
                group_id = group["group_id"]
                claims = group["claims"]
                parent_groups = group["parent_groups"]
                parent_refs = group["parent_refs"]
                if (any(digest(ref) not in owner_refs
                        for claim in claims for ref in (claim.get("source_refs") or ()))
                        or any(parent not in admitted_groups for parent in parent_groups)
                        or any(digest(ref) not in owner_refs for ref in parent_refs)):
                    held.append({"group_id": group_id, "reason": "HISTORICAL_PARENT_GROUP_NOT_ADMITTED"})
                    continue
                if not claims or any(
                    claim["kind"] != "facts" or claim.get("predicate") not in PHYSICAL_TYPES
                    or "physical" not in job["dimensions"]
                    or (job.get("requested_predicate") is not None
                        and claim.get("predicate") != job["requested_predicate"])
                    for claim in claims
                ):
                    held.append({"group_id": group_id, "reason": "HISTORICAL_OWNER_SCOPE_HELD"})
                    continue
                if group.get("asserted_H_class") != "H0":
                    held.append({"group_id": group_id, "reason": "HISTORICAL_OWNER_SCOPE_HELD"})
                    continue
                proposed = physical.copy()
                group_facts = []
                for claim in claims:
                    predicate, value = claim["predicate"], claim["value"]
                    if not _valid_physical_value(predicate, value):
                        break
                    existing = proposed.get(predicate)
                    if existing is not None:
                        if type(existing["value"]) is not type(value) or existing["value"] != value:
                            break
                        group_facts.append(existing["id"])
                        continue
                    effective_time = claim.get("effective_time")
                    body = {
                        "target_id": target["id"], "predicate": predicate,
                        "value": value, "effective_time": (
                            world.clock if effective_time is None else effective_time
                        ),
                        "asserted_at": world.clock, "parent_hash": target["parent_hash"],
                        "parent_event_ref": packet["event_refs"][0],
                        "claim_ref": claim.get("ref"),
                        "owner_dependency_refs": parent_refs,
                        "owner_source_refs": claim.get("source_refs") or [],
                        "dependency_fact_ids": sorted({
                            fact_id for parent in parent_groups
                            for fact_id in admitted_groups[parent]
                        }),
                        "job_id": job_id, "group_id": group_id,
                        "evidence_class": "SOURCEFREE_SYNTHETIC_PHYSICAL",
                    }
                    fact_id = "history-fact:" + digest(body)
                    proposed[predicate] = {"id": fact_id, **body}
                    group_facts.append(fact_id)
                else:
                    physical = proposed
                    accepted.append({"group_id": group_id, "fact_ids": group_facts})
                    admitted_groups[group_id] = group_facts
                    continue
                rejected.append({"group_id": group_id, "reason": "PHYSICAL_FACT_CONFLICT_OR_TYPE"})

            if physical != target.get("physical_depth", {}):
                target["physical_depth"] = physical
                target["version"] += 1
            status = ("PARTIAL_HELD" if held or rejected else "INDEX_READY") if accepted else (
                "SOURCE_HELD" if held else "REJECTED" if rejected else "NO_WORK"
            )
            job.update(status=status, admission={
                "job_id": job_id, "status": status, "accepted": accepted,
                "held": held, "rejected": rejected,
                "world_readset": job["world_readset"], "target_version": target["version"],
            })
            return deepcopy(job["admission"])

    def inspect(self, target_id, *, predicate=None):
        """Perform a local inspection through the existing world event owner."""
        from bp4.world import make_event

        if predicate is not None and predicate not in VISIBLE_PHYSICAL:
            raise HistoryRefusal("HISTORICAL_INSPECTION_PREDICATE_UNAVAILABLE")
        session = self.session
        with self._write() as (world, state):
            target = state["targets"].get(target_id)
            actor = session.meta["user_actor"]
            location = world.positions.get(actor)
            if (target is None or not session.scene_open()
                    or target["surface"]["location"] != location
                    or target["surface"]["occurrence_id"] not in session.user_perceived_ids()):
                raise HistoryRefusal("HISTORICAL_TARGET_UNAVAILABLE")
            visible = {
                predicate: row["id"]
                for predicate, row in target.get("physical_depth", {}).items()
                if predicate in VISIBLE_PHYSICAL
            }
            job = state["outbox"].get(target.get("job_id"), {})
            job_status = job.get("status")
            active = {"ENQUEUED", "RUNNING", "CANDIDATE_READY", "FAILED_RETRYABLE"}
            next_job = None
            known = set(visible) | set(target["surface"]["physical"])
            if (predicate is not None and predicate not in known
                    and "physical" in target["surface"]["unresolved"]
                    and job_status not in active):
                next_job = "history-job:" + digest([target_id, "INSPECT_PHYSICAL", predicate])
                job = state["outbox"].get(next_job)
                if job is None:
                    job = {
                        "id": next_job, "target_id": target_id, "status": "ENQUEUED",
                        "trigger": "INSPECT_PHYSICAL", "dimensions": ["physical"],
                        "requested_predicate": predicate, "target_version": target["version"],
                        "root": target["root"], "branch": target["branch"],
                        "parent_hash": target["parent_hash"],
                    }
                job_status = job["status"]
            if (predicate in known if predicate is not None else bool(visible)):
                depth_status = "OBSERVED"
            elif ("physical" in job.get("dimensions", ())
                  and job_status in active):
                depth_status = "PENDING"
            elif "physical" in job.get("dimensions", ()) and job_status == "SOURCE_HELD":
                depth_status = "HELD"
            else:
                depth_status = "UNKNOWN"
            event = make_event(
                clock=world.clock, kind="INSPECT", actor_id=actor, location=location,
                summary="You inspect the particular.", sequence=len(world.events),
                body={"target": target_id, "physical_fact_ids": visible,
                      "physical_depth_status": depth_status, "changed": False,
                      **({"requested_predicate": predicate} if predicate is not None else {})},
            )
            world.add_event(event)
            session._append_event(event, perceive=(actor,))
            session._perceive_if_present(event, "A", "B")
            session.product._append_episode(
                session.branch_id, actor, "DO", world.clock,
                {"action": "inspect", "admitted": True, "event_id": event["event_id"],
                 "changed": False, "action_seq": session._action_seq()},
            )
            state.setdefault("inspections", {})[event["event_id"]] = event["hash"]
            if depth_status == "PENDING":
                job.setdefault("inspection_priority_event", event["event_id"])
                if next_job is not None:
                    state["outbox"].setdefault(next_job, job)
            return deepcopy(event)

    def read_inspection(self, event_id):
        """Read only the physical evidence bound to an actual perceived inspection."""
        session = self.session
        world = session.world()
        state = self._state(world)
        event = session.event(event_id)
        if (event is None or state.get("inspections", {}).get(event_id) != event["hash"]
                or event["kind"] != "INSPECT"
                or event["actor_id"] != session.meta["user_actor"]
                or event_id not in session.user_perceived_ids()):
            raise HistoryRefusal("HISTORICAL_INSPECTION_NOT_PERCEIVED")
        body = event["body"]
        target = state["targets"][body["target"]]
        facts = target.get("physical_depth", {})
        observed = []
        for predicate, fact_id in body["physical_fact_ids"].items():
            fact = facts.get(predicate)
            if fact is None or fact["id"] != fact_id:
                raise HistoryRefusal("HISTORICAL_INSPECTION_READSET_MISMATCH")
            parent_ref = fact.get("parent_event_ref")
            if parent_ref is not None:
                parent = session.event(parent_ref["object_id"])
                if parent is None or parent["hash"] != parent_ref["content_hash"]:
                    raise HistoryRefusal("HISTORICAL_INSPECTION_PARENT_MISMATCH")
            observed.append({"predicate": predicate, "value": fact["value"], "fact_id": fact_id})
        result = {"target_id": target["id"], "observation_id": event_id, "physical": observed}
        if "physical_depth_status" in body:
            result["physical_depth_status"] = body["physical_depth_status"]
        return result
