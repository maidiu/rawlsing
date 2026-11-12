"""Read the existing P3 actor-bound sourcefree state from a P6 situated decision.

This does not write a world or psychological record, issue a CAN/ADP rule,
confer actor memory, or authorize a native action.  It binds the *existing*
P3 owner to the *existing* P6 session and permits a provisional sourcefree
interpreter to consider admitted, earlier B1 mediator candidates.

Material home conditions must continue to come from the P2/P6 world owner.
"""
from __future__ import annotations

from developmental_recursion.contracts import RecursionRefusal


def qualified_p3_read(owner, session, *, project, counterpart, as_of):
    """Return prior, actor-qualified P3 mediator identities; never world facts."""
    if owner is None or not all(hasattr(owner, name) for name in (
            "snapshot", "store", "registry", "source_hash", "mode")):
        raise RecursionRefusal("P6_P3_OWNER_UNAVAILABLE")
    if owner.mode != "TEST_ONLY":
        raise RecursionRefusal("P6_P3_SOURCEFREE_MODE_ONLY")
    if not isinstance(project, str) or not project or not isinstance(counterpart, str) or not counterpart:
        raise RecursionRefusal("P6_P3_SCOPE_INVALID")
    world = session.world()
    actor = world.actor_state["A"]["actor_id"]
    root = session.read_root()["root_hash"]
    branch = session.branch_id
    ident = owner.snapshot()
    if (ident.root, ident.actor, ident.branch) != (root, actor, branch):
        raise RecursionRefusal("P6_P3_ACTOR_ROOT_BRANCH_MISMATCH")
    if type(as_of) is not int or as_of != world.clock or as_of != ident.clock:
        raise RecursionRefusal("P6_P3_CLOCK_MISMATCH")
    registry = owner.registry
    store = owner.store
    if (type(registry) is not dict or registry.get("hash") != store.registry_hash
            or owner.source_hash != store.source_hash
            or len(registry.get("rules", ())) < 1):
        raise RecursionRefusal("P6_P3_SOURCE_REGISTRY_MISMATCH")
    formation = registry["rules"][0]
    rows = store.query(project=project, counterpart=counterpart, as_of=as_of)
    admitted = []
    for record in rows:
        if (record.get("kind") != "V3MS_MEDIATOR"
                or record.get("grade") != "SOURCEFREE_TEST_ONLY"
                or any(record.get(k) != v for k, v in (
                    ("root", root), ("actor", actor), ("branch", branch),
                    ("source_hash", owner.source_hash),
                    ("registry_hash", registry["hash"]),
                    ("rule_id", formation["rule_id"]),
                    ("rule_version", formation["rule_version"]),
                    ("rule_hash", formation["rule_hash"]),
                ))
                or type(record.get("effective_from")) is not int
                or record["effective_from"] >= as_of
                or not isinstance(record.get("hash"), str)
                or not isinstance(record.get("payload"), dict)
                or record["payload"].get("origin_access") != "NOT_GRANTED_AS_MEMORY"
                or record["payload"].get("mode") not in ("joint_check", "private_check")):
            raise RecursionRefusal("P6_P3_RECORD_NOT_QUALIFIED")
        admitted.append({
            "record_hash": record["hash"],
            "mode": record["payload"]["mode"],
            "effective_from": record["effective_from"],
        })
    return {
        "grade": "SOURCEFREE_TEST_ONLY",
        "status": "PRIOR_P3_CANDIDATES" if admitted else "NO_PRIOR_P3_CANDIDATES",
        "root": root, "actor": actor, "branch": branch, "as_of": as_of,
        "project": project, "counterpart": counterpart,
        "source_hash": owner.source_hash,
        "registry_hash": registry["hash"],
        "records": admitted,
        "readset": [row["record_hash"] for row in admitted],
        "native_memory": "MISSING_RULE",
        "native_action": "NOT_ISSUED_BY_P3_RULE",
    }
