"""Actual P2-output compatibility; not the pending durable P3 vertical slice."""
from pathlib import Path
import json
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from p3 import test_rules
from p3.projections import activate, project_views
from developmental_recursion.contracts import EventProposal, detached, digest
from developmental_recursion.p2_owner import P2Owner, load_p2


def seal(body):
    return dict(detached(body), hash=digest(body))


def test_actual_p2_actor_and_public_views_and_rule_records_are_compatible(tmp_path):
    fanin = load_p2().start(tmp_path / "actual-p2")
    case = fanin.deps["case_for"](True)
    owner = P2Owner(fanin, case=case, source=fanin.deps["source_for"](case),
                    participants=tuple(fanin.session.read_root()["actor_ids"]))
    try:
        initial = owner.snapshot()
        proposal = EventProposal("projection-receiving", initial.clock + 6,
                                 "ADMIT_EVENT", (owner.source_ref,), owner.participants, {})
        realized = owner.realize("projection-receiving", proposal, initial).document()
        identity = owner.snapshot().document()
        native_event = realized["objective"]["event"]
        source_hash = digest({"grade": test_rules.GRADE,
                              "purpose": "controlled sourcefree prior-participation hypothesis",
                              "identity": {k: identity[k] for k in ("root", "actor", "branch")}})
        registry = test_rules.make_registry(source_hash)
        plan = {k: identity[k] for k in ("root", "actor", "branch")}
        plan.update(grade=test_rules.GRADE, source_hash=source_hash,
                    registry_hash=registry["hash"], proposal_hash=digest(proposal.document()),
                    event_id=proposal.event_id, permitted_rules=test_rules.rule_descriptors(),
                    phase="FORMATION", project="sourcefree-plan-comparison",
                    counterpart=owner.participants[-1], activation_roles=["peer"],
                    relation_refs=["sourcefree-collaboration"], obligation_refs=[])
        history = []
        for i, outcome in enumerate(("recognized_plan", "imposed_plan")):
            h = {k: identity[k] for k in ("root", "actor", "branch")}
            h.update(grade=test_rules.GRADE, source_hash=source_hash,
                     episode_id="controlled-history-" + str(i), project=plan["project"],
                     counterpart=plan["counterpart"], time=initial.clock - 2 + i,
                     activity="compare_plans_in_task", outcome=outcome,
                     parent_refs=[history[-1]["hash"]] if history else [])
            history.append(seal(h))
        candidate = test_rules.evaluate_event(
            identity=identity, proposal=proposal.document(), realized=realized,
            history=history, records=[], plan=seal(plan), source_hash=source_hash,
            registry=registry)
        records = candidate["records"]
        assert len(records) == 2
        context = {k: identity[k] for k in ("root", "actor", "branch", "clock")}
        context.update(project=plan["project"], counterpart=plan["counterpart"],
                       interlocutor_role="peer", relation_ref="sourcefree-collaboration",
                       obligation_refs=[], actor_observed=True,
                       material_eligible=realized["consequences"]["immediate_response"][
                           "objective_material_eligible"],
                       source_refs=[source_hash], grade=test_rules.GRADE)
        context = seal(context)
        before_read = owner.snapshot()
        activation = activate(records, identity=identity, context=context, registry=registry)
        assert activation["status"] == "CONTRADICTION"
        assert len(activation["entries"]) == 2
        assert all(x["activation"] == "ELIGIBLE" for x in activation["entries"])
        other_context = {k: v for k, v in context.items() if k != "hash"}
        other_context["interlocutor_role"] = "institutional_observer"
        inhibited = activate(records, identity=identity, context=seal(other_context), registry=registry)
        assert all(x["activation"] == "INHIBITED" for x in inhibited["entries"])
        assert inhibited["contradictions"] == activation["contradictions"]

        experience = realized["accessible"]
        public = fanin.view()
        assert public["visible_speech"], "The actual receiving fixture must offer visible dialogue"
        eb = {k: identity[k] for k in ("root", "actor", "branch", "clock")}
        pb = dict(eb, view_hash=digest(public))
        eb["experience_hash"] = digest(experience)
        surfaces = {}
        for name, permissions in (("silent_observer", ["OBSERVE_PUBLIC_ACTION"]),
                                  ("dialogue_partner", ["OBSERVE_PUBLIC_ACTION", "READ_PUBLIC_DIALOGUE"])):
            stand = {k: identity[k] for k in ("root", "actor", "branch", "clock")}
            stand.update(interlocutor_ref="sourcefree-" + name, role=name,
                         permissions=permissions, source_refs=[source_hash], grade=test_rules.GRADE)
            surfaces[name] = project_views(identity=identity, actor_experience=experience,
                                          experience_binding=eb, public_view=public,
                                          public_binding=pb, standpoint=seal(stand))
        assert surfaces["silent_observer"]["actor"] == surfaces["dialogue_partner"]["actor"]
        assert surfaces["silent_observer"]["user"]["visible_speech"] == []
        assert surfaces["dialogue_partner"]["user"]["visible_speech"]
        for view in surfaces.values():
            assert view["actor"]["status"] == "OBSERVED"
            assert view["claims_status"] == "DEFER_MISSING_AUTHORITY"
            serialized = json.dumps(view)
            for secret in (records[0]["hash"], records[1]["hash"], "joint_check", "private_check"):
                assert secret not in serialized
            assert {x["event_id"] for x in view["user"]["visible_actions"]} <= {
                x["event_id"] for x in public["visible_actions"]}
        assert owner.snapshot() == before_read
        receipt = {
            "grade": "HQ_ACTUAL_P2_OUTPUT_COMPATIBILITY_NOT_DURABLE_P3",
            "native_event_ref": native_event["e1_event_id"],
            "actual_actor_perceived_action_ref": native_event["action_event_id"],
            "identity": identity, "activation": activation, "inhibited": inhibited,
            "view_permissions_change_surface_only": True,
            "owner_snapshot_unchanged_by_readers": True,
            "actor_observed": experience["status"],
            "public_dialogue_count": len(public["visible_speech"]),
            "user_dialogue_counts": {k: len(v["user"]["visible_speech"]) for k, v in surfaces.items()},
            "no_causal_ledger_exposure": True, "native_claims": "DEFER_MISSING_AUTHORITY",
            "not_proved": ["durable psychological store", "P3Owner", "later-state first consumer",
                           "two P3 batches", "independent runtime acceptance", "native science"],
        }
        if os.environ.get("P3_PROJECTION_RECEIPT"):
            Path(os.environ["P3_PROJECTION_RECEIPT"]).write_text(json.dumps(receipt, indent=2) + "\n")
    finally:
        owner.close()
