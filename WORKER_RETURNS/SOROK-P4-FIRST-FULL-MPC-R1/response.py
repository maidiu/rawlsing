"""P4 consumer of P2 speech and previously committed P3 mediators."""

from developmental_recursion.contracts import RecursionRefusal, digest
from p3 import projections, test_rules

from speech import developing_actor

EXPRESSIONS = {
    "joint_check": "Come look at this edge with me.",
    "private_check": "Give me a moment to check this edge myself.",
    "inspect_alone": "I'll check the edge first.",
}


def check_source(owner):
    owner._check_config()
    test_rules._check_sources(owner.registry, owner.source_hash)


def qualified_scope(owner, scope, *, exact_keys=False,
                    code="P4_SCOPE_NOT_SOURCE_BOUND"):
    """Return the exact foreground scope owned by the single source formation."""
    required = ("project", "counterpart", "interlocutor_role", "relation_ref")
    if type(scope) is not dict:
        raise RecursionRefusal(code)
    if exact_keys:
        if set(scope) != set(required):
            raise RecursionRefusal(code)
    elif any(key not in scope for key in required):
        raise RecursionRefusal(code)
    plans = getattr(owner, "plans", None)
    if not isinstance(plans, (list, tuple)):
        raise RecursionRefusal(code)
    formations = [
        row for row in plans
        if type(row) is dict and row.get("phase") == "FORMATION"
    ]
    if len(formations) != 1:
        raise RecursionRefusal(code)
    formation = formations[0]
    relations = formation.get("relation_refs")
    if not isinstance(relations, (list, tuple)) or len(relations) != 1:
        raise RecursionRefusal(code)
    expected = {
        "project": formation.get("project"),
        "counterpart": formation.get("counterpart"),
        "interlocutor_role": formation.get("interlocutor_role"),
        "relation_ref": relations[0],
    }
    if (any(type(value) is not str or not value for value in expected.values())
            or any(scope.get(key) != value for key, value in expected.items())):
        raise RecursionRefusal(code)
    registry = getattr(owner, "registry", None)
    if (type(registry) is not dict
            or formation.get("hash") != digest({
                key: value for key, value in formation.items() if key != "hash"
            })
            or formation.get("source_hash") != getattr(owner, "source_hash", None)
            or formation.get("registry_hash") != registry.get("hash")):
        raise RecursionRefusal(code)
    return dict(expected)


def read_response(owner, admission, scope):
    """Read uptake using the actor's actual speech perception and P3 readset."""
    check_source(owner)
    scope = qualified_scope(owner, scope)
    identity = owner.base_owner.snapshot().document()
    session = owner.base_owner.fanin.session
    attempt = admission["attempt"]
    if any(attempt[key] != identity[key] for key in ("root", "branch", "clock")):
        raise RecursionRefusal("P4_SPEECH_IDENTITY_MISMATCH")
    if attempt["hash"] != digest({k: v for k, v in attempt.items() if k != "hash"}):
        raise RecursionRefusal("P4_SPEECH_ATTEMPT_HASH_MISMATCH")
    result = {"status": "NOT_PERCEIVED", "mode": None, "readset": []}
    event = admission["performed"]
    if event is None:
        return dict(result, status="NOT_PERFORMED")
    user = session.meta["user_actor"]
    stored = session.event(event["event_id"])
    if (stored != event or event["kind"] != "SPEECH" or event["actor_id"] != user
            or event["clock"] != identity["clock"]
            or event["body"].get("attempt_hash") != attempt["hash"]
            or event["body"].get("text") != attempt["text"]
            or event["body"].get("request_edge") is not attempt["request_edge"]):
        raise RecursionRefusal("P4_SPEECH_EVENT_BINDING_MISMATCH")

    actor = developing_actor(session, identity["actor"])
    receipts = session.product.store.perceptions(session.branch_id, actor)
    access = next((row for row in receipts if row["event_id"] == event["event_id"]
                   and row["clock"] == event["clock"]), None)
    if access != admission["actor_access"]:
        raise RecursionRefusal("P4_SPEECH_PERCEPTION_MISMATCH")
    result["readset"] = [event["hash"]]
    if access is None:
        return result

    result["readset"].append(digest(access))
    if not event["body"]["request_edge"]:
        return dict(result, status="PERCEIVED_NO_INSPECTION_REQUEST")

    result["readset"].extend([owner.registry["hash"],
                              test_rules.B1_SHA256, owner.source_hash])
    context = {
        **{key: identity[key] for key in ("root", "actor", "branch", "clock")},
        "project": scope["project"],
        "counterpart": scope["counterpart"],
        "interlocutor_role": scope["interlocutor_role"],
        "relation_ref": scope["relation_ref"],
        "obligation_refs": [],
        "actor_observed": True,
        "material_eligible": None,
        "source_refs": [owner.source_hash],
        "grade": test_rules.GRADE,
    }
    context["hash"] = digest(context)
    records = owner.store.query(project=context["project"], counterpart=context["counterpart"],
                                as_of=identity["clock"] - 1)
    activation = projections.activate(records, identity=identity, context=context,
                                      registry=owner.registry)
    result["readset"].append(activation["context_hash"])
    eligible = set()
    for entry in activation["entries"]:
        result["readset"].append(entry["record_hash"])
        if entry["activation"] == "ELIGIBLE":
            eligible.add(entry["mode"])
    if not records:
        eligible.add("inspect_alone")
    # Conflicting eligible modes do not license an invented resolution.
    mode = next(iter(eligible)) if len(eligible) == 1 else None
    return dict(result, status="UPTAKE" if mode else "NO_EXPRESSION", mode=mode,
                actor_alias=actor)


def express(session, uptake):
    """Realize the bounded outward expression through the P2 world writer."""
    from s45_projection.projection import project_event

    mode = uptake["mode"]
    if mode is None:
        return None, None
    event = session._actor_say(uptake["actor_alias"], EXPRESSIONS[mode])
    observed = (project_event(event)
                if event["event_id"] in session.user_perceived_ids() else None)
    return event, observed
