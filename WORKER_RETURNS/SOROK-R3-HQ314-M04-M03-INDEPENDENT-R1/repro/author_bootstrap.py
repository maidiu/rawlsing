"""Use the installed native candidate and the unchanged fixture owners."""

from pathlib import Path
import sys

R = Path(__file__).resolve().parents[1]
M = R / "runtime/m02/runtime/m01"
sys.path.insert(0, str(M / "repro"))
import bootstrap
from cell import Cell, Refusal, owner, old, digest, events
from candidate.positive_chain import seal_event
from candidate.candidate_registry_fixture import canon


def apply(
    c, access="CLAIM_ACCESSIBLE", operation="ADD", target=None, claim=None, event=None
):
    e = event or c.e1
    claim = claim or c.claim_id
    return owner.adp017_apply_epistemic_effect(
        actor_id=c.ctx.actor_id,
        claim_ref=claim,
        stance_kind="BELIEF",
        stance_operation=operation,
        causal_parent_refs=[e.event_id],
        actor_facing_basis_refs=[e.event_id + ":" + e.event_hash],
        memory_basis_refs=[],
        owning_rule_id=c.binding.rule_id,
        owning_rule_version=c.binding.rule_version,
        owning_rule_hash=c.binding.rule_content_hash,
        effective_causal_time=e.effective_causal_time,
        claim_accessibility=access,
        context=c.ctx,
        pre_state_hash=c.ctx.state_hash,
        target_record_ref=target,
    )


def alternative(c, at, tag="M03_ALTERNATIVE"):
    e = seal_event(
        event_id=tag,
        issuer_authority_id="ISSUER_AUTH_WORLD_SCHED",
        issuer_authority_version="1",
        event_kind="EXTERNAL_RUNTIME_EVENT",
        actor_scope=c.e1.actor_scope,
        world_ref=c.e1.world_ref,
        world_as_of=c.e1.world_as_of,
        admission_state="ADMITTED",
        effective_causal_time=at,
        public_features=c.e1.public_features,
        causal_parent_event_ids=(
            (c.e1.event_id,) if at > c.e1.effective_causal_time else ()
        ),
    )
    assert c.reg.admit_event(e)["status"] == "EVENT_IDENTITY_ADMITTED_IN_FIXTURE"
    value = owner.canonical_claim(
        c.ctx.actor_id,
        "FIXTURE_PRIVATE_FEEDBACK_APPRAISAL",
        "RESPECTED",
        at,
        c.ctx.actor_id,
        [e.event_id],
    )
    ref = c.ctx.bind_claim(value, e)
    result = apply(c, claim=ref, event=e)
    assert result["decision_state"] == "APPLIED_EPISTEMIC_TRANSITION"
    return e, ref, result
