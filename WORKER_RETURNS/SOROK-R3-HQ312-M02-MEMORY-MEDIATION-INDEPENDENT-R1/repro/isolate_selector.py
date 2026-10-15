"""Post-RED paired isolation, using only native owner APIs and Cell checkpoints."""

from review_bootstrap import *
from pathlib import Path
from dataclasses import asdict
import json, hashlib, os

c = Cell()
c.prepare("CERTAIN", "NONE")
original_claim = c.claim_id
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
assert c.reg.admit_event(future)["status"] == "EVENT_IDENTITY_ADMITTED_IN_FIXTURE"
claim = owner.canonical_claim(
    c.ctx.actor_id,
    "FIXTURE_PRIVATE_FEEDBACK_APPRAISAL",
    "RESPECTED",
    future.effective_causal_time,
    c.ctx.actor_id,
    [future.event_id],
)
selected = c.ctx.bind_claim(claim, future)
args = native_epistemic(c)
args.update(
    claim_ref=selected,
    causal_parent_refs=[future.event_id],
    actor_facing_basis_refs=[future.event_id + ":" + future.event_hash],
    effective_causal_time=future.effective_causal_time,
)
transition = owner.adp017_apply_epistemic_effect(**args)
assert transition["decision_state"] == "APPLIED_EPISTEMIC_TRANSITION"
packet = c.checkpoint()
other = Cell()
other.restore(packet)
changed = other.checkpoint()
changed["claim_id"] = selected
other.restore(changed)
assert c.ctx.data() == other.ctx.data() and c.ctx.state_hash == other.ctx.state_hash
assert (
    c.history.checkpoint() == other.history.checkpoint()
    and c.e1 == other.e1
    and c.e2 == other.e2
)
method = Cell.later
left = c.later(c.ctx.state_hash)
right = other.later(other.ctx.state_hash)
assert Cell.later is method
assert left["read"]["actual_state"] == right["read"]["actual_state"]
assert left["streams"] == {"memory": "BUFFER", "epistemic": "AMPLIFY"}
assert right["streams"] == {"memory": "BUFFER", "epistemic": "REROUTE"}


def source(fn):
    p = Path(fn.__code__.co_filename).resolve()
    b = p.read_bytes()
    return {
        "file": str(p.relative_to(R)),
        "git_blob_sha1": hashlib.sha1(
            b"blob " + str(len(b)).encode() + b"\0" + b
        ).hexdigest(),
        "sha256": hashlib.sha256(b).hexdigest(),
    }


out = {
    "pid": os.getpid(),
    "scope": "post-RED adversarial selector isolation, not a lawful treatment or psychological experiment",
    "same_full_owner_state": True,
    "same_owner_hash": c.ctx.state_hash,
    "same_history_events_and_times": True,
    "original_selector": original_claim,
    "future_selector": selected,
    "future_event": asdict(future),
    "actual_owner_transition": transition,
    "control": left,
    "changed_selector": right,
    "actual_native_sources": {
        "Cell.later": source(Cell.later),
        "Cell.read_owner": source(Cell.read_owner),
        "epistemic": source(owner.adp017_apply_epistemic_effect),
    },
    "no_response_monkeypatch": True,
}
(R / "evidence/selector_isolation.json").write_text(json.dumps(out, indent=2) + "\n")
print("ACTUAL_PAIRED_SELECTOR_ISOLATION", left["streams"], right["streams"])
