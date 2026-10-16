"""New author counterexamples; these are not independent acceptance review."""

from author_bootstrap import *
from pathlib import Path
from copy import deepcopy
import json, subprocess, os, hashlib, shutil, itertools
import pytest

OUT = R / "evidence/author/observations"


def save(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / (name + ".json")).write_text(json.dumps(data, indent=2, default=str) + "\n")


def ready(m="CERTAIN", e="BELIEF", h="STORED"):
    c = Cell()
    c.prepare(m, e, h)
    return c


def denied(c, name):
    before = c.checkpoint()
    events = deepcopy(c.reg._events)
    with pytest.raises(Refusal) as exc:
        c.later(c.ctx.state_hash)
    assert (
        c.checkpoint() == before
        and c.reg._events == events
        and c.reg.event(c.e2.event_id) is None
    )
    save(
        name,
        {
            "typed_refusal": str(exc.value),
            "before": before,
            "after": c.checkpoint(),
            "rollback_exact": True,
        },
    )
    return str(exc.value)


@pytest.mark.parametrize(
    "m,h",
    list(
        itertools.product(
            ["NONE", "CERTAIN", "UNCERTAIN", "UNAVAILABLE"],
            ["STORED", "OMITTED", "WITHHELD"],
        )
    ),
)
def test_bound_none_is_a_real_positive_arm(m, h):
    c = ready(m, "NONE", h)
    before = c.ctx.data()
    out = c.later(c.ctx.state_hash, history_access=h != "WITHHELD")
    assert (
        out["streams"]["epistemic"] == "AMPLIFY"
        and c.ctx.data() == before
        and c.claim_id in c.ctx.claims
    )
    p = out["read"]["claim_selection_provenance"]
    assert p["disposition"] == "BOUND_CANONICAL_CLAIM_NO_APPLIED_STANCE"
    assert p["selected_claim_ref"] == c.claim_id and p["actual_effect_provenance"] == []
    assert (
        p["verified_binding"]["basis"]["source_event"]["event_hash"] == c.e1.event_hash
    )
    save("none_" + m + "_" + h, {"owner": before, "result": out})


@pytest.mark.parametrize(
    "value", [None, "", "UNRESOLVED", 123, {"unhashable": "selector"}]
)
def test_unknown_live_selector_never_becomes_no_stance(value):
    c = ready()
    c.claim_id = value
    denied(c, "unknown_" + hashlib.sha256(str(value).encode()).hexdigest()[:8])


@pytest.mark.parametrize("at", ["1998-09-01T10:00:00Z", "1999-01-20T10:00:00Z"])
def test_actual_native_other_claim_is_not_selected_by_outer_hint(at):
    c = ready("CERTAIN", "NONE")
    e, ref, t = alternative(c, at)
    c.claim_id = ref
    code = denied(c, "other_claim_" + at[:10])
    assert code == (
        "CLAIM_SELECTION_AFTER_RESPONSE"
        if at > "1998-11-20T09:00:00Z"
        else "CLAIM_SELECTION_SOURCE_SCOPE"
    )


def test_irrelevant_future_claim_does_not_ban_legitimate_none():
    c = ready("CERTAIN", "NONE")
    selected = c.claim_id
    alternative(c, "1999-01-20T10:00:00Z")
    assert c.claim_id == selected
    out = c.later(c.ctx.state_hash)
    assert out["streams"] == {"memory": "BUFFER", "epistemic": "AMPLIFY"}
    save("future_not_selected", out)


FIELDS = [
    "actor",
    "world_ref",
    "world_as_of",
    "canonical_claim_ref",
    "canonical_claim_hash",
    "owning_rule_id",
    "owning_rule_version",
    "owning_rule_hash",
    "response_rule_id",
    "response_rule_version",
    "response_source_hash",
    "first_response_receipt_hash",
    "source_event",
]


@pytest.mark.parametrize("field", FIELDS)
def test_checkpoint_binding_fields_cannot_be_reissued(field):
    c = ready()
    before = c.checkpoint()
    packet = deepcopy(before)
    binding = json.loads(packet["claim_selection_binding"])
    binding["basis"][field] = "M03_FORGED"
    packet["claim_selection_binding"] = canon(binding)
    with pytest.raises(Refusal):
        c.restore(packet)
    assert c.checkpoint() == before
    assert c.later(c.ctx.state_hash)["streams"] == {
        "memory": "BUFFER",
        "epistemic": "REROUTE",
    }


@pytest.mark.parametrize(
    "field", ["first_event_entry_hash", "first_owner_state_hash", "schema"]
)
def test_actual_first_commit_identity_is_bound(field):
    c = ready()
    before = c.checkpoint()
    packet = deepcopy(before)
    binding = json.loads(packet["claim_selection_binding"])
    binding[field] = "M03_FORGED"
    packet["claim_selection_binding"] = canon(binding)
    with pytest.raises(Refusal):
        c.restore(packet)
    assert c.checkpoint() == before


@pytest.mark.parametrize("value", [None, {}, 1, "not-json", "[]"])
def test_missing_or_malformed_binding_does_not_create_authority(value):
    c = ready(e="NONE")
    before = c.checkpoint()
    packet = deepcopy(before)
    packet["claim_selection_binding"] = value
    with pytest.raises(Refusal):
        c.restore(packet)
    assert c.checkpoint() == before
    assert c.later(c.ctx.state_hash)["streams"]["epistemic"] == "AMPLIFY"


def test_cross_cell_selection_binding_mix_refuses_atomically():
    a = ready("CERTAIN")
    b = ready("UNCERTAIN")
    before = a.checkpoint()
    packet = deepcopy(before)
    packet["claim_selection_binding"] = b.checkpoint()["claim_selection_binding"]
    with pytest.raises(Refusal):
        a.restore(packet)
    assert a.checkpoint() == before


def test_valid_full_checkpoint_replay_still_works():
    a = ready()
    b = Cell()
    b.restore(a.checkpoint())
    assert a.ctx.data() == b.ctx.data()
    assert a.later(a.ctx.state_hash) == b.later(b.ctx.state_hash)


def test_outer_unknown_checkpoint_is_quarantined_not_trusted():
    c = ready()
    packet = c.checkpoint()
    binding = packet["claim_selection_binding"]
    packet["claim_id"] = "UNKNOWN_OUTER"
    c.restore(packet)
    assert c.checkpoint()["claim_selection_binding"] == binding
    assert denied(c, "quarantined_checkpoint") == "CLAIM_SELECTION_UNKNOWN"


def test_coherent_reissued_binding_cannot_replace_first_source_commit():
    c = ready("CERTAIN", "NONE")
    e, ref, t = alternative(c, "1999-01-20T10:00:00Z")
    before = c.checkpoint()
    packet = deepcopy(before)
    b = json.loads(packet["claim_selection_binding"])
    b["basis"]["canonical_claim_ref"] = ref
    b["basis"]["canonical_claim_hash"] = c.ctx.claims[ref]["canonical_content_hash"]
    b["basis"]["source_event"]["event_id"] = e.event_id
    packet["claim_selection_binding"] = canon(b)
    packet["claim_id"] = ref
    with pytest.raises(Refusal):
        c.restore(packet)
    assert c.checkpoint() == before


def test_missing_actual_first_commit_cannot_be_patched_by_hashing():
    c = ready()
    before = c.checkpoint()
    packet = deepcopy(before)
    entries = packet["journal"][0][:-1]
    packet["journal"] = (entries, digest(entries))
    with pytest.raises(Refusal):
        c.restore(packet)
    assert c.checkpoint() == before


@pytest.mark.parametrize(
    "field",
    ["actor_id", "claim_id", "epistemic_state_hash", "basis_refs", "permission"],
)
def test_current_permission_must_match_actual_snapshot_and_source(field):
    c = ready()
    packet = c.ctx.checkpoint()
    record = packet["state"]["permissions"][c.claim_id]
    record[field] = ["FORGED"] if field == "basis_refs" else "FORGED"
    c.ctx.restore(packet)
    denied(c, "stale_permission_" + field)


def test_native_permission_revision_invalidates_old_record():
    c = ready()
    oldpermission = deepcopy(c.ctx.permissions[c.claim_id])
    target = next(iter(c.ctx.stances))
    assert (
        apply(c, "CLAIM_INACCESSIBLE", "SUPERSEDE_EXACT_RECORD", target)[
            "decision_state"
        ]
        == "APPLIED_EPISTEMIC_TRANSITION"
    )
    packet = c.ctx.checkpoint()
    packet["state"]["permissions"][c.claim_id] = oldpermission
    c.ctx.restore(packet)
    denied(c, "old_current_permission")


def test_duplicate_effect_is_not_silently_collapsed():
    c = ready()
    assert apply(c)["decision_state"] == "APPLIED_EPISTEMIC_TRANSITION"
    assert len(c.ctx.stances) == 2
    denied(c, "duplicate_effect")


@pytest.mark.parametrize(
    "field",
    [
        "effective_causal_time",
        "actor_id",
        "claim_ref",
        "owning_rule_hash",
        "actor_facing_basis_refs",
    ],
)
def test_coherently_rehashed_active_effect_still_needs_actual_provenance(field):
    c = ready()
    packet = c.ctx.checkpoint()
    state = packet["state"]
    key = next(iter(state["stances"]))
    effect = state["stances"][key]
    effect[field] = (
        "1999-01-20T10:00:00Z"
        if field == "effective_causal_time"
        else ("FORGED",) if field == "actor_facing_basis_refs" else "FORGED"
    )
    snap = state["state_sets"][c.claim_id]
    snap["active_stance_records"] = [deepcopy(effect)]
    snap["current_state_hash"] = digest(
        {k: v for k, v in snap.items() if k != "current_state_hash"}
    )
    state["permissions"][c.claim_id]["epistemic_state_hash"] = snap[
        "current_state_hash"
    ]
    c.ctx.restore(packet)
    denied(c, "effect_" + field)


@pytest.mark.parametrize(
    "at", ["1998-10-03T15:59:59Z", "1998-10-03T16:00:00Z", "not-time", None]
)
def test_consumption_rejects_earlier_or_invalid_cuts(at):
    c = ready()
    before = c.checkpoint()
    with pytest.raises(Refusal):
        c.read_owner(c.ctx.state_hash, at)
    assert c.checkpoint() == before


@pytest.mark.parametrize(
    "at", ["1998-10-03T16:00:01Z", "1998-11-20T09:00:00Z", "2000-12-31T23:59:59Z"]
)
def test_consumption_checks_actual_cut_each_read(at):
    c = ready()
    out = c.read_owner(c.ctx.state_hash, at)
    assert out["streams"] == {"memory": "BUFFER", "epistemic": "REROUTE"}
    assert out["claim_selection_provenance"]["response_as_of"] == at


def test_public_first_receipt_corruption_does_not_poison_rollback():
    c = ready()
    c.first_receipt["receipt_hash"] = "FORGED"
    denied(c, "precorrupt_first_receipt")


def test_native_withdrawal_and_unchanged_none_claim_remain_lawful():
    c = ready()
    mem = deepcopy(c.ctx.memories)
    history = c.history.checkpoint()
    target = next(iter(c.ctx.stances))
    assert (
        apply(c, operation="WITHDRAW", target=target)["decision_state"]
        == "APPLIED_EPISTEMIC_TRANSITION"
    )
    out = c.later(c.ctx.state_hash)
    assert (
        out["streams"] == {"memory": "BUFFER", "epistemic": "AMPLIFY"}
        and c.ctx.memories == mem
        and c.history.checkpoint() == history
    )
    save("withdrawal", out)


@pytest.mark.parametrize("stage", ["later_admission", "later_read", "later_emission"])
def test_rollback_preserves_binding_and_all_native_state(stage):
    c = ready()
    before = c.checkpoint()
    with pytest.raises(Refusal):
        c.later(c.ctx.state_hash, failure=stage)
    assert c.checkpoint() == before
    assert c.later(c.ctx.state_hash)["status"] == "COMMITTED_TEST_ONLY"


@pytest.mark.parametrize("at", ["2001-01-01T00:00:00Z", "2099-01-01T00:00:00Z"])
def test_direct_read_cannot_escape_finite_rule_scope(at):
    c = Cell()
    c.prepare("CERTAIN", "BELIEF")
    before = c.checkpoint()
    with pytest.raises(Refusal, match="CLAIM_RESPONSE_OUTSIDE_RULE_SCOPE"):
        c.read_owner(c.ctx.state_hash, at)
    assert c.checkpoint() == before


def test_provenance_helper_body_is_inside_actual_source_grant(tmp_path):
    target = tmp_path / "source_probe"
    target.mkdir()
    for name in ("cell.py", "claim_provenance.py"):
        shutil.copyfile(M / "repro" / name, target / name)
    script = """
import bootstrap,sys,json,hashlib
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import cell,claim_provenance
c=cell.Cell();c.prepare();before=c.checkpoint()
assert Path(claim_provenance.__file__).parent==Path(sys.argv[1])
p=Path(claim_provenance.__file__);original=hashlib.sha256(p.read_bytes()).hexdigest()
p.write_bytes(p.read_bytes()+b'\\n# actual provenance body mutation\\n')
try:c.later(c.ctx.state_hash)
except cell.Refusal as e:assert e.code=='UNAUTHORIZED_RULE_OR_SOURCE'
else:raise AssertionError('mutated helper accepted under existing grant')
assert c.checkpoint()==before
print(json.dumps({'actual_import':str(p),'before_sha256':original,'after_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'old_grant_refused':True,'rollback_exact':True}))
"""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=str(M / "repro"))
    p = subprocess.run(
        [sys.executable, "-c", script, str(target)],
        cwd=M / "repro",
        env=env,
        capture_output=True,
        text=True,
    )
    save(
        "provenance_source_body_mutation",
        {
            "returncode": p.returncode,
            "stdout": p.stdout.replace(str(R), "[RETURN]"),
            "stderr": p.stderr.replace(str(R), "[RETURN]"),
        },
    )
    assert p.returncode == 0, p.stderr


def test_actual_import_and_grant_receipt():
    import cell, claim_provenance
    from dataclasses import asdict

    c = ready()
    out = c.later(c.ctx.state_hash)
    files = {}
    for module in (cell, claim_provenance, bootstrap, old, owner):
        p = Path(module.__file__).resolve()
        b = p.read_bytes()
        files[module.__name__] = {
            "file": str(p.relative_to(R)),
            "sha256": hashlib.sha256(b).hexdigest(),
            "blob_sha1": hashlib.sha1(
                b"blob " + str(len(b)).encode() + b"\0" + b
            ).hexdigest(),
        }
    assert Path(cell.__file__).resolve() == (M / "repro/cell.py").resolve()
    assert (
        Path(claim_provenance.__file__).resolve()
        == (M / "repro/claim_provenance.py").resolve()
    )
    assert c.grant == cell.source_hash()
    save(
        "actual_imports",
        {
            "files": files,
            "source_hash": c.grant,
            "first_event": asdict(c.e1),
            "later_event": asdict(c.e2),
            "read": out["read"],
        },
    )
