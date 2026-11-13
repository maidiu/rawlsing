"""A bounded read-only P3-to-P6 TEST_ONLY first-consumer candidate adapter.

Do NOT confuse sourcefree B1 mediator candidates with autobiographical
memory, a native psychological disposition, an actor permission, or material
home facts. Reuse the same registered P3 activation logic P4 actually uses:
source identity, time, role, relation, actor-observed access, and contradictory
modes must all be checked *before* a candidate reaches a situated interpreter.
"""
from __future__ import annotations

from developmental_recursion.contracts import RecursionRefusal, digest
from p3 import projections, test_rules

_GRADE = "SOURCEFREE_TEST_ONLY"


def qualified_p4_scope(owner, ledger):
    """Preflight the P4 foreground's test-only P3 scope against its source plan.

    P4's ledger is an action receipt, not an authority for replacing the
    project, counterpart, role or relation chosen at genesis. The existing
    P3Owner source/config is frozen and checked on reopen. This exact P4
    fixture has one source-issued FORMATION plan and one relation. Ambiguous
    or future multiproject arrangements are held, not guessed from a list.
    The check must happen BEFORE P4 writes pending or performs an action.
    """
    scope = ledger.get("scope") if type(ledger) is dict else None
    required = {"project", "counterpart", "interlocutor_role", "relation_ref"}
    if type(scope) is not dict or set(scope) != required:
        raise RecursionRefusal("P6_P3_SCOPE_NOT_SOURCE_BOUND")
    plans = getattr(owner, "plans", None)
    if not isinstance(plans, (list, tuple)):
        raise RecursionRefusal("P6_P3_SCOPE_NOT_SOURCE_BOUND")
    formations = [
        row for row in plans
        if type(row) is dict and row.get("phase") == "FORMATION"
    ]
    if len(formations) != 1:
        raise RecursionRefusal("P6_P3_SCOPE_NOT_SOURCE_BOUND")
    formation = formations[0]
    relations = formation.get("relation_refs")
    if not isinstance(relations, (list, tuple)) or len(relations) != 1:
        raise RecursionRefusal("P6_P3_SCOPE_NOT_SOURCE_BOUND")
    expected = {
        "project": formation.get("project"),
        "counterpart": formation.get("counterpart"),
        "interlocutor_role": formation.get("interlocutor_role"),
        "relation_ref": relations[0],
    }
    if any(type(v) is not str or not v for v in expected.values()) or scope != expected:
        raise RecursionRefusal("P6_P3_SCOPE_NOT_SOURCE_BOUND")
    return dict(expected)


def qualified_p3_read(
    owner, session, *, project, counterpart, as_of,
    interlocutor_role=None, relation_ref=None, obligation_refs=(),
    actor_observed=False,
):
    """Read eligible B1 sourcefree candidate identities; NEVER issue memory/action."""
    if owner is None or not all(hasattr(owner, name) for name in (
            "snapshot", "base_owner", "store", "registry", "source_hash", "mode")):
        raise RecursionRefusal("P6_P3_OWNER_UNAVAILABLE")
    if owner.mode != "TEST_ONLY":
        raise RecursionRefusal("P6_P3_SOURCEFREE_MODE_ONLY")
    if (not isinstance(project, str) or not project
            or not isinstance(counterpart, str) or not counterpart):
        raise RecursionRefusal("P6_P3_SCOPE_INVALID")
    if type(actor_observed) is not bool:
        raise RecursionRefusal("P6_P3_ACTOR_ACCESS_SCHEMA")
    if not isinstance(obligation_refs, (list, tuple)):
        raise RecursionRefusal("P6_P3_OBLIGATION_SCOPE_INVALID")
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
    # The same immutable B1-source gate already used by the P4 consumer.
    test_rules._check_sources(registry, owner.source_hash)
    formation = registry["rules"][0]
    rows = store.query(project=project, counterpart=counterpart, as_of=as_of)
    for record in rows:
        if (record.get("kind") != "V3MS_MEDIATOR"
                or record.get("grade") != _GRADE
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

    # The *actual* current P3 context and activation procedure. The P6 caller
    # derives actor_observed from its admitted actor-local world evidence,
    # never from the provider, portal user gaze or analyst biography.
    identity = owner.base_owner.snapshot().document()
    context = {
        "root": root, "actor": actor, "branch": branch, "clock": as_of,
        "project": project, "counterpart": counterpart,
        "interlocutor_role": interlocutor_role, "relation_ref": relation_ref,
        "obligation_refs": list(obligation_refs), "actor_observed": actor_observed,
        "material_eligible": None, "source_refs": [owner.source_hash],
        "grade": _GRADE,
    }
    context["hash"] = digest(context)
    activated = projections.activate(
        rows, identity=identity, context=context, registry=registry,
    )
    entries = {row["record_hash"]: row for row in activated["entries"]}
    permitted = []
    if activated["status"] == "OK":
        for record in rows:
            entry = entries.get(record["hash"])
            if entry is None:
                raise RecursionRefusal("P6_P3_ACTIVATION_RECORD_MISSING")
            if entry["activation"] == "ELIGIBLE":
                permitted.append({
                    "record_hash": record["hash"],
                    "mode": entry["mode"],
                    "effective_from": record["effective_from"],
                })
    return {
        "grade": _GRADE,
        "status": (
            "CONTRADICTION_HELD" if activated["status"] == "CONTRADICTION"
            else "PRIOR_P3_CANDIDATES" if permitted
            else "NO_QUALIFIED_P3_CANDIDATES"
        ),
        "root": root, "actor": actor, "branch": branch, "as_of": as_of,
        "project": project, "counterpart": counterpart,
        "source_hash": owner.source_hash, "registry_hash": registry["hash"],
        "context_hash": activated["context_hash"],
        "records": permitted,
        "readset": [row["record_hash"] for row in permitted],
        "native_memory": "MISSING_RULE",
        "native_action": "NOT_ISSUED_BY_P3_RULE",
    }
