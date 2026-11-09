"""P4 consumer of P2 speech and previously committed P3 mediators."""

from developmental_recursion.contracts import RecursionRefusal, digest
from p3 import projections, test_rules

from speech import developing_actor

OPENING_FORMATION_ID = "p4-formation"
SEMANTIC_GRADE = "SOURCEFREE_TEST_ONLY"
NATIVE_PLAN_HOLD = "BLOCKED_NAMED_AUTHORITY_REQUIRED"
SPEECH_MOVES = frozenset({
    "QUESTION", "ASSERTION", "REQUEST", "OFFER", "REFUSAL", "JOKE",
    "OBJECTION", "DISCLOSURE", "REDIRECTION", "UNKNOWN",
})

EXPRESSIONS = {
    "joint_check": "Come look at this edge with me.",
    "private_check": "Give me a moment to check this edge myself.",
    "inspect_alone": "I'll check the edge first.",
}


def check_source(owner):
    owner._check_config()
    test_rules._check_sources(owner.registry, owner.source_hash)


def semantic_encounter(event, transduce):
    """Validate a sourcefree meaning proposal without admitting its claims."""
    text = event["body"]["text"]
    proposal = transduce(event_id=event["event_id"], event_hash=event["hash"], text=text)
    if (type(proposal) is not dict
            or set(proposal) != {"event_id", "event_hash", "hypotheses"}
            or proposal["event_id"] != event["event_id"]
            or proposal["event_hash"] != event["hash"]):
        return None
    hypotheses = proposal["hypotheses"]
    if type(hypotheses) is not list or not 1 <= len(hypotheses) <= 8:
        return None
    for item in hypotheses:
        if (type(item) is not dict
                or set(item) != {"move", "referent", "span", "uncertain"}
                or type(item["move"]) is not str or item["move"] not in SPEECH_MOVES
                or item["referent"] not in (None, "CURRENT_EDGE")
                or type(item["uncertain"]) is not bool):
            return None
        span = item["span"]
        if (type(span) is not list or len(span) != 2
                or any(type(value) is not int for value in span)
                or not 0 <= span[0] < span[1] <= len(text)):
            return None
    return {**proposal, "grade": SEMANTIC_GRADE, "native_plan": NATIVE_PLAN_HOLD,
            "hash": digest(proposal)}


def read_response(owner, admission, scope, *, transduce=None):
    """Read uptake using the actor's actual speech perception and P3 readset."""
    check_source(owner)
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
    semantic = not event["body"]["request_edge"]
    if semantic:
        if transduce is None:
            return dict(result, status="PERCEIVED_NO_INSPECTION_REQUEST")
        person = owner.snapshot()
        try:
            encounter = semantic_encounter(event, transduce)
        except TimeoutError:
            encounter = None
            unavailable = True
        else:
            unavailable = False
        if owner.snapshot() != person:
            raise RecursionRefusal("P4_SEMANTIC_PERSON_SNAPSHOT_STALE")
        if unavailable:
            return dict(result, status="SEMANTIC_PROPOSAL_UNAVAILABLE")
        if encounter is None:
            return dict(result, status="SEMANTIC_PROPOSAL_REFUSED")
        result["semantic_encounter"] = encounter
        result["person_snapshot"] = person.document()
        result["readset"].append(encounter["hash"])
        # The received P3 fixture authorizes only the current edge practice.
        # Mixed or uncertain proposals have no issued selection rule.
        hypotheses = encounter["hypotheses"]
        if len(hypotheses) != 1 or hypotheses[0]["uncertain"]:
            return dict(result, status="SEMANTIC_AMBIGUITY_HELD")
        move = hypotheses[0]
        if move["move"] == "UNKNOWN" or (
                move["move"] == "REQUEST" and move["referent"] is None):
            return dict(result, status="SEMANTIC_UNRESOLVED_HELD")
        if move["move"] != "REQUEST":
            return dict(result, status="SEMANTIC_VALID_EMPTY")

    if semantic:
        fields = ("project", "counterpart", "interlocutor_role")
        formation = owner.store.get_operation(OPENING_FORMATION_ID)
        scope_plan = formation["plan"] if formation and formation["phase"] == "COMPLETE" else None
        if (scope_plan is None or scope_plan["phase"] != "FORMATION"
                or any(scope.get(key) != scope_plan[key] for key in fields)
                or scope.get("relation_ref") not in scope_plan["relation_refs"]):
            return dict(result, status="SEMANTIC_SCOPE_REFUSED")
        result["readset"].append(scope_plan["hash"])

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
    if semantic:
        context["source_refs"].extend((event["hash"], digest(access), encounter["hash"],
                                       scope_plan["hash"]))
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
    if semantic:
        result["recruitment"] = activation
        if activation["status"] == "CONTRADICTION" or len(eligible) > 1:
            return dict(result, status="SEMANTIC_CONFLICT_HELD")
    elif not records:
        eligible.add("inspect_alone")
    # Conflicting eligible modes do not license an invented resolution.
    mode = next(iter(eligible)) if len(eligible) == 1 else None
    return dict(result, status="UPTAKE" if mode else "NO_EXPRESSION", mode=mode,
                actor_alias=actor)


def express(session, *, mode, actor_alias=None):
    """Realize the bounded outward expression through the P2 world writer."""
    from s45_projection.projection import project_event

    if mode is None:
        return None, None
    event = session._actor_say(actor_alias, EXPRESSIONS[mode])
    observed = (project_event(event)
                if event["event_id"] in session.user_perceived_ids() else None)
    return event, observed
