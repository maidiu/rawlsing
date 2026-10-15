"""Reviewer-origin falsifiers; predictions frozen before execution, no author tests imported."""

from review_bootstrap import *
from copy import deepcopy
from dataclasses import replace, asdict
import itertools, json, inspect, hashlib
import pytest

FROZEN = json.loads((R / "01_INDEPENDENT_EXPECTATIONS.json").read_text())
OUT = R / "evidence/independent/observations"


def save(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / (name + ".json")).write_text(json.dumps(data, indent=2, default=str) + "\n")


def prepared(m="CERTAIN", e="BELIEF", h="STORED"):
    c = Cell()
    first = c.prepare(memory=m, epistemic=e, history=h)
    assert (
        first["status"] == "FIRST_EVENT_COMMITTED"
        and c.ctx.verify()
        and c.reg.verify_event(c.e1)
    )
    return c


@pytest.mark.parametrize(
    "arm",
    FROZEN["arms"],
    ids=lambda a: a["memory"] + "_" + a["epistemic"] + "_" + a["history"],
)
def test_independent_36_arm_actual_state_to_response(arm):
    c = prepared(arm["memory"], arm["epistemic"], arm["history"])
    pre = c.export()
    expected_hash = c.ctx.state_hash
    result = c.later(expected_hash, history_access=arm["history"] != "WITHHELD")
    assert result["streams"] == arm["expected_streams"]
    assert result["read"]["actual_state"] == pre["owner_state"] == c.ctx.data()
    assert result["read"]["state_hash"] == expected_hash == pre["owner_hash"]
    assert c.reg.verify_event(c.e2)
    assert len(c.reads) == 1 and c.reads[0] == result["read"]
    assert result["receipt"]["kind"] == "M01_CAN008_CURRENT_RESPONSE_GRAPH"
    assert result["receipt"]["payload"]["read"] == result["read"]
    assert bool(result["history_stored"]) == arm["history_stored"]
    assert bool(result["history_delivered"]) == arm["history_delivered"]
    for mid, m in pre["owner_state"]["memories"].items():
        t = pre["owner_state"]["memory_transitions"][m["last_transition_id"]]
        assert t["memory_id"] == mid == m["memory_id"]
        assert (
            t["post_state_hash"]
            == m["current_state_hash"]
            == owner.memory_semantic_hash(m)
        )
        assert t["causal_parent_event_refs"] == [c.e1.event_id]
        assert m["objective_source_event_refs"] == (
            c.e1.event_id + ":" + c.e1.event_hash,
        )
        assert t["effective_causal_time"] == c.e1.effective_causal_time
    for stance in pre["owner_state"]["stances"].values():
        assert stance["stance_kind"] == "BELIEF" and not stance["memory_basis_refs"]
        assert stance["claim_ref"] == c.claim_id and stance["causal_parent_refs"] == (
            c.e1.event_id,
        )
    assert result["receipt"]["payload"]["production_owner"].startswith(
        "MECHANISM_IDENTIFICATION_HOLD"
    )
    save(
        "factorial_" + arm["memory"] + "_" + arm["epistemic"] + "_" + arm["history"],
        {
            "arm": arm,
            "first_admitted_event": asdict(c.e1),
            "pre": pre,
            "actual_result": result,
            "post": c.export(),
        },
    )


@pytest.mark.parametrize(
    "m,e",
    list(
        itertools.product(
            ["NONE", "CERTAIN", "UNCERTAIN", "UNAVAILABLE"],
            ["NONE", "BELIEF", "INACCESSIBLE"],
        )
    ),
)
def test_history_intervention_holds_exact_owner_state_constant(m, e):
    rows = []
    for h in ("STORED", "OMITTED", "WITHHELD"):
        c = prepared(m, e, h)
        before = c.ctx.data()
        out = c.later(c.ctx.state_hash, history_access=h != "WITHHELD")
        rows.append((c, before, out))
    assert rows[0][1] == rows[1][1] == rows[2][1]
    assert rows[0][2]["streams"] == rows[1][2]["streams"] == rows[2][2]["streams"]
    assert (
        rows[0][2]["history_stored"]
        and not rows[1][2]["history_stored"]
        and rows[2][2]["history_stored"]
    )
    assert (
        rows[0][2]["history_delivered"]
        and not rows[1][2]["history_delivered"]
        and not rows[2][2]["history_delivered"]
    )
    save(
        "history_contrast_" + m + "_" + e,
        [{"owner": s, "result": o} for c, s, o in rows],
    )


@pytest.mark.parametrize("e", ["NONE", "BELIEF", "INACCESSIBLE"])
def test_same_memory_id_different_committed_content_changes_only_memory_stream(e):
    left = prepared("NONE", e)
    right = prepared("NONE", e)
    # Native formation after identical epistemic setup holds even its provenance
    # IDs fixed. Natural prepare() forms memory first and legitimately gives the
    # epistemic effect a different prestate-derived ID across memory variants.
    left.ctx.commit_memory(left.form("AVAILABLE_SOURCE_BOUND"))
    right.ctx.commit_memory(right.form("AVAILABLE_UNCERTAIN"))
    assert (
        left.e1 == right.e1
        and left.e2 == right.e2
        and left.history.checkpoint() == right.history.checkpoint()
    )
    assert set(left.ctx.memories) == set(right.ctx.memories)
    a = next(iter(left.ctx.memories.values()))
    b = next(iter(right.ctx.memories.values()))
    assert (
        a["source_feature_bindings"] != b["source_feature_bindings"]
        and a["current_state_hash"] != b["current_state_hash"]
    )
    assert left.ctx.claims == right.ctx.claims and left.ctx.stances == right.ctx.stances
    la = left.later(left.ctx.state_hash)
    rb = right.later(right.ctx.state_hash)
    assert (la["streams"]["memory"], rb["streams"]["memory"]) == ("BUFFER", "DEFLECT")
    assert la["streams"]["epistemic"] == rb["streams"]["epistemic"]
    save("same_id_content_" + e, {"left": la, "right": rb})


@pytest.mark.parametrize("m", ["NONE", "CERTAIN", "UNCERTAIN", "UNAVAILABLE"])
def test_native_belief_commit_and_permission_supersession_without_history_change(m):
    c = prepared(m, "NONE")
    history = c.history.checkpoint()
    memories = deepcopy(c.ctx.memories)
    old_hash = c.ctx.state_hash
    before = c.export()
    applied = owner.adp017_apply_epistemic_effect(**native_epistemic(c))
    assert (
        applied["decision_state"] == "APPLIED_EPISTEMIC_TRANSITION"
        and c.ctx.state_hash != old_hash
    )
    assert c.history.checkpoint() == history and c.ctx.memories == memories
    snapshot = c.checkpoint()
    with pytest.raises(Refusal, match="STALE_OR_CORRUPT_OWNER_STATE"):
        c.later(old_hash)
    assert c.checkpoint() == snapshot
    target = next(iter(c.ctx.stances))
    changed = owner.adp017_apply_epistemic_effect(
        **native_epistemic(c, "CLAIM_INACCESSIBLE", "SUPERSEDE_EXACT_RECORD", target)
    )
    assert changed["decision_state"] == "APPLIED_EPISTEMIC_TRANSITION"
    assert (
        len(c.ctx.stances) == 1
        and next(iter(c.ctx.stances.values()))["stance_kind"] == "BELIEF"
    )
    out = c.later(c.ctx.state_hash)
    assert (
        out["streams"]["epistemic"] == "BLOCK"
        and out["read"]["private_permission"]["first_person_permission"]
        == "DENY_FIRST_PERSON_CLAIM"
    )
    assert c.history.checkpoint() == history and c.ctx.memories == memories
    save(
        "native_permission_supersession_" + m,
        {"before": before, "applied": applied, "superseded": changed, "result": out},
    )


def test_native_exact_withdrawal_changes_response_at_fixed_memory_and_history():
    c = prepared()
    mem = deepcopy(c.ctx.memories)
    h = c.history.checkpoint()
    target = next(iter(c.ctx.stances))
    changed = owner.adp017_apply_epistemic_effect(
        **native_epistemic(c, operation="WITHDRAW", target=target)
    )
    assert (
        changed["decision_state"] == "APPLIED_EPISTEMIC_TRANSITION"
        and not c.ctx.stances
    )
    out = c.later(c.ctx.state_hash)
    assert out["streams"] == {"memory": "BUFFER", "epistemic": "AMPLIFY"}
    assert c.ctx.memories == mem and c.history.checkpoint() == h
    save("native_withdrawal", {"transition": changed, "result": out})


def test_valid_alternate_memory_identity_is_not_the_transfer_function():
    rows = []
    for tag in ("M02_ALTERNATE_A", "M02_ALTERNATE_B"):
        c = prepared("NONE", "NONE")
        proposal = c.form(memory_id_override=tag)
        commit = c.ctx.commit_memory(proposal)
        assert commit["status"] == "ADP016_TRACE_COMMITTED_IN_FIXTURE"
        rows.append((c, c.later(c.ctx.state_hash)))
    assert set(rows[0][0].ctx.memories) != set(rows[1][0].ctx.memories)
    assert rows[0][0].history.checkpoint() == rows[1][0].history.checkpoint()
    assert (
        rows[0][1]["streams"]
        == rows[1][1]["streams"]
        == {"memory": "BUFFER", "epistemic": "AMPLIFY"}
    )
    save(
        "alternate_memory_identity",
        [{"state": c.export(), "result": r} for c, r in rows],
    )


@pytest.mark.parametrize(
    "field",
    [
        "memory_id",
        "actor_id",
        "source_feature_bindings",
        "objective_source_event_refs",
        "last_transition_effective_time",
        "transition_rule_hash",
        "transition_id",
        "transition_time",
    ],
)
def test_changed_proposal_cannot_commit_without_native_validation(field):
    c = prepared("NONE", "NONE")
    p = c.form()
    before = c.ctx.checkpoint()
    bad = deepcopy(p)
    if field == "transition_rule_hash":
        bad["transition"]["authority_or_rule_hash"] = "f" * 64
    elif field == "transition_id":
        bad["transition"]["memory_transition_id"] = "f" * 64
    elif field == "transition_time":
        bad["transition"]["effective_causal_time"] = c.e2.effective_causal_time
    elif field == "source_feature_bindings":
        bad["memory"][field] = ("forged",)
    elif field == "objective_source_event_refs":
        bad["memory"][field] = ("M02_FOREIGN_EVENT:forged",)
    else:
        bad["memory"][field] = "M02_FORGED"
    with pytest.raises(owner.OwnerTransitionError):
        c.ctx.commit_memory(bad)
    assert c.ctx.checkpoint() == before
    assert c.ctx.commit_memory(p)["status"] == "ADP016_TRACE_COMMITTED_IN_FIXTURE"


@pytest.mark.parametrize(
    "field,value",
    [
        ("subject_scope", "OTHER_ACTOR"),
        ("subject_ref", "OTHER_ACTOR"),
        ("temporal_scope", "2000-12-01T00:00:00Z"),
        ("object_or_value", "DISRESPECTED"),
        ("predicate_ref", "FOREIGN_PREDICATE"),
        ("polarity", "NEGATIVE"),
        ("referent_refs", ["FOREIGN_EVENT"]),
    ],
)
def test_valid_canonical_foreign_claim_does_not_acquire_finite_rule_authority(
    field, value
):
    c = prepared("NONE", "NONE")
    original = c.ctx.claims[c.claim_id]
    args = {
        k: original[k]
        for k in (
            "subject_ref",
            "predicate_ref",
            "object_or_value",
            "temporal_scope",
            "subject_scope",
            "referent_refs",
            "polarity",
        )
    }
    args[field] = value
    foreign = owner.canonical_claim(**args)
    assert owner.verify_claim(foreign)
    before = c.ctx.checkpoint()
    with pytest.raises(owner.OwnerTransitionError):
        c.ctx.bind_claim(foreign, c.e1)
    assert c.ctx.checkpoint() == before


@pytest.mark.parametrize(
    "field,value",
    [
        ("actor_id", "OTHER_ACTOR"),
        ("claim_ref", "FOREIGN_CLAIM"),
        ("effective_causal_time", "2000-12-01T00:00:00Z"),
        ("actor_facing_basis_refs", ["M02_SOURCE_ONLY"]),
        ("causal_parent_refs", ["FOREIGN_EVENT"]),
        ("owning_rule_version", "FOREIGN_VERSION"),
        ("memory_basis_refs", ["UNSTORED_MEMORY"]),
        ("stance_kind", "KNOWLEDGE"),
    ],
)
def test_native_epistemic_actor_basis_time_rule_and_permission_fail_closed(
    field, value
):
    c = prepared("CERTAIN", "NONE")
    before = c.ctx.checkpoint()
    args = native_epistemic(c)
    args[field] = value
    result = owner.adp017_apply_epistemic_effect(**args)
    assert (
        result["decision_state"] != "APPLIED_EPISTEMIC_TRANSITION"
        and c.ctx.checkpoint() == before
    )


@pytest.mark.parametrize("point", ["later_admission", "later_read", "later_emission"])
def test_later_transaction_rollback_covers_actual_all_owner_and_journal_state(point):
    c = prepared()
    before = c.checkpoint()
    with pytest.raises(Refusal):
        c.later(c.ctx.state_hash, failure=point)
    assert c.checkpoint() == before and c.reg.event(c.e2.event_id) is None
    assert c.later(c.ctx.state_hash)["status"] == "COMMITTED_TEST_ONLY"


@pytest.mark.parametrize("m", ["NONE", "CERTAIN", "UNCERTAIN", "UNAVAILABLE"])
def test_unknown_access_not_nonknowledge_and_no_later_publication(m):
    c = prepared(m, "UNKNOWN")
    before = c.checkpoint()
    with pytest.raises(Refusal, match="MECHANISM_IDENTIFICATION_HOLD_ACCESS_UNKNOWN"):
        c.later(c.ctx.state_hash)
    assert c.checkpoint() == before and c.reg.event(c.e2.event_id) is None
    assert all(v["stance_kind"] == "BELIEF" for v in c.ctx.stances.values())


@pytest.mark.parametrize(
    "target", ["memory", "stance", "permission", "memory_transition"]
)
def test_unprovenanced_actual_store_changes_never_become_productive(target):
    c = prepared()
    if target == "memory":
        next(iter(c.ctx.memories.values()))["memory_id"] = "M02_FORGED_ID"
    elif target == "stance":
        next(iter(c.ctx.stances.values()))["claim_ref"] = "M02_FORGED_CLAIM"
    elif target == "permission":
        c.ctx.permissions[c.claim_id]["permission"] = "PERMIT_FIRST_PERSON_KNOWLEDGE"
    else:
        next(iter(c.ctx.memory_transitions.values()))[
            "authority_or_rule_hash"
        ] = "M02_FORGED_RULE"
    before = deepcopy(c.reg._events)
    with pytest.raises((Refusal, owner.OwnerTransitionError, LedgerIntegrityError)):
        c.later(c.ctx.state_hash)
    assert c.reg._events == before


@pytest.mark.parametrize("memory", ["CERTAIN", "UNCERTAIN"])
def test_k3_hidden_origin_remains_inaccessible_despite_real_causal_effect(memory):
    c = prepared(memory)
    out = c.later(c.ctx.state_hash)
    assert (
        out["read"]["memory_first_person"]["first_person_permission"]
        == "DENY_FIRST_PERSON_CLAIM"
    )
    assert (
        out["read"]["memory_first_person"]["self_explanation_of_hidden_origin"]
        == "BLOCKED"
    )
    assert (
        out["read"]["private_permission"]["first_person_permission"]
        == "PERMIT_FIRST_PERSON_BELIEF"
    )
    assert (
        out["receipt"]["payload"]["public_standing"]
        == "HOLD_NO_PUBLIC_RATIFICATION_OWNER"
    )


@pytest.mark.parametrize(
    "label", ["OBJECTIVE_SUPPORTED", "OBJECTIVE_CONTRADICTED", "OBJECTIVE_UNRESOLVED"]
)
def test_k5_private_public_objective_remain_distinct(label):
    c = prepared("CERTAIN", "NONE")
    args = native_epistemic(c)
    args["claim_objective_relation"] = label
    applied = owner.adp017_apply_epistemic_effect(**args)
    assert applied["decision_state"] == "APPLIED_EPISTEMIC_TRANSITION"
    assert applied["public_ratification"] == "HOLD_NO_PUBLIC_STANDING_OWNER"
    assert c.ctx.state_sets[c.claim_id]["analyst_relation"] == "OBJECTIVE_UNRESOLVED"
    assert c.later(c.ctx.state_hash)["streams"] == {
        "memory": "BUFFER",
        "epistemic": "REROUTE",
    }


def test_original_can3_history_comparator_and_owner_state_equality():
    a = run_positive_chain(_comparison=False)
    b = run_positive_chain(
        _comparison=False,
        omit_first_effect=True,
        later_event_requires_prior_effect=False,
    )
    assert (
        a["later_event_response"]["effect_kind"] == "DEFLECT"
        and b["later_event_response"]["effect_kind"] == "AMPLIFY"
    )
    assert a["state"] == b["state"]
    save("independent_CAN3_comparator", {"stored": a, "omitted": b})


def test_serial_reference_attachment_is_not_content_sensitive_mediation():
    outputs = []
    for m in ("CERTAIN", "UNCERTAIN"):
        c = prepared(m, "NONE")
        args = native_epistemic(c)
        args["memory_basis_refs"] = list(c.ctx.memories)
        applied = owner.adp017_apply_epistemic_effect(**args)
        assert applied["decision_state"] == "APPLIED_EPISTEMIC_TRANSITION"
        permission = owner.adp017_first_person_check(
            "BELIEF",
            "CLAIM_ACCESSIBLE",
            context=c.ctx,
            claim_ref=c.claim_id,
            state_hash=c.ctx.state_sets[c.claim_id]["current_state_hash"],
        )
        before = c.checkpoint()
        with pytest.raises(Refusal, match="UNAUTHORIZED_EPISTEMIC_MECHANISM"):
            c.later(c.ctx.state_hash)
        assert c.checkpoint() == before
        outputs.append({"memory": m, "transition": applied, "permission": permission})
    assert outputs[0]["permission"] == outputs[1]["permission"]
    save(
        "serial_content_identification_hold",
        {"actual": outputs, "verdict": "MECHANISM_IDENTIFICATION_HOLD"},
    )


def test_lawful_future_claim_cannot_condition_an_earlier_response():
    # Actual owner admission/commit; only Cell's selected claim pointer is then
    # rebound adversarially. This is not a lawful mediator treatment, and must not
    # count as a positive causal arm. The read must enforce temporal/claim custody.
    c = prepared("CERTAIN", "NONE")
    future = seal_event(
        event_id="M02_FUTURE_FEEDBACK",
        issuer_authority_id="ISSUER_AUTH_WORLD_SCHED",
        issuer_authority_version="1",
        event_kind="EXTERNAL_RUNTIME_EVENT",
        actor_scope=c.e1.actor_scope,
        world_ref=c.e1.world_ref,
        world_as_of=c.e1.world_as_of,
        admission_state="ADMITTED",
        effective_causal_time="1999-01-20T10:00:00Z",
        public_features=c.e1.public_features,
        causal_parent_event_ids=(c.e1.event_id,),
    )
    admitted = c.reg.admit_event(future)
    assert admitted["status"] == "EVENT_IDENTITY_ADMITTED_IN_FIXTURE"
    claim = owner.canonical_claim(
        c.ctx.actor_id,
        "FIXTURE_PRIVATE_FEEDBACK_APPRAISAL",
        "RESPECTED",
        future.effective_causal_time,
        c.ctx.actor_id,
        [future.event_id],
    )
    foreign = c.ctx.bind_claim(claim, future)
    args = native_epistemic(c)
    args.update(
        claim_ref=foreign,
        causal_parent_refs=[future.event_id],
        actor_facing_basis_refs=[future.event_id + ":" + future.event_hash],
        effective_causal_time=future.effective_causal_time,
    )
    applied = owner.adp017_apply_epistemic_effect(**args)
    assert applied["decision_state"] == "APPLIED_EPISTEMIC_TRANSITION"
    c.claim_id = foreign
    before = c.checkpoint()
    observed = None
    refused = None
    try:
        observed = c.later(c.ctx.state_hash)
    except (Refusal, owner.OwnerTransitionError, LedgerIntegrityError) as e:
        refused = str(e)
    save(
        "future_claim_provenance_probe",
        {
            "future_event": asdict(future),
            "actual_admission": admitted,
            "actual_owner_transition": applied,
            "first_event": asdict(c.e1),
            "later_event": asdict(c.e2),
            "before": before["ctx"],
            "actual_result": observed,
            "refused": refused,
            "scope": "adversarial Cell metadata rebinding after legitimate owner operations; not a lawful treatment or an arbitrary monkeypatch",
        },
    )
    assert (
        refused is not None
    ), "Earlier response consumed future claim/epistemic state after Cell metadata rebinding"
    assert c.checkpoint() == before


def test_checkpoint_claim_selector_cannot_downgrade_existing_belief_to_absence():
    # Follow-up to the predeclared claim/provenance falsifier. The supported
    # rollback/restore method accepts a modified outer Cell selector while the
    # complete owner state/hash and actual response history are unchanged.
    control = prepared()
    changed = prepared()
    same_owner = control.ctx.data()
    same_hash = control.ctx.state_hash
    assert changed.ctx.data() == same_owner and changed.ctx.state_hash == same_hash
    assert changed.history.checkpoint() == control.history.checkpoint()
    packet = changed.checkpoint()
    original_claim = packet["claim_id"]
    packet["claim_id"] = "M02_UNKNOWN_SELECTED_CLAIM"
    changed.restore(packet)
    assert (
        changed.ctx.data() == same_owner
        and changed.ctx.state_hash == same_hash
        and changed.ctx.verify()
    )
    expected = control.later(same_hash)
    refused = None
    observed = None
    try:
        observed = changed.later(same_hash)
    except (Refusal, owner.OwnerTransitionError, LedgerIntegrityError) as e:
        refused = str(e)
    save(
        "checkpoint_claim_selector_probe",
        {
            "original_claim": original_claim,
            "altered_selector": packet["claim_id"],
            "actual_owner_state_identical": changed.ctx.data() == same_owner,
            "owner_hash": same_hash,
            "control": expected,
            "actual_result": observed,
            "refused": refused,
            "scope": "adversarial outer Cell checkpoint metadata; no code patch, no forged owner transition, not a lawful intervention",
        },
    )
    assert (
        refused is not None
    ), "Unresolved selected claim silently converted an actually stored accessible BELIEF into no stance"
