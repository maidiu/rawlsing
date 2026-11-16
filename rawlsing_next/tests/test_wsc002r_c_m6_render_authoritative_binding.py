import pytest

import rawlsing_next.wsc_gt0_v2_mediation as gt0_f
from rawlsing_next.wsc_gt0_field_forge_ingress import run_gt0_field_forge_ingress
from rawlsing_next.wsc_gt0_prev3_bridge import run_gt0_prev3
from rawlsing_next.wsc_gt0_source_preff import bind_gt0_f0, run_gt0_preff
from rawlsing_next.wsc_gt0_v3_runtime import run_gt0_prev3_v3
from rawlsing_next.wsc_gt0_protocol import GT0StageStatus


def _v3_result():
    bound = bind_gt0_f0()
    preff = run_gt0_preff(bound)
    field_forge = run_gt0_field_forge_ingress(preff)
    prev3 = run_gt0_prev3(field_forge, f0_ref=bound.f0_ref)
    return run_gt0_prev3_v3(prev3)


def test_gt0_f_binds_exact_current_m6_and_render_negative_surfaces():
    result = gt0_f.run_gt0_v3_v2(_v3_result())

    assert result.receipt.status is GT0StageStatus.BLOCKED_NAMED_AUTHORITY_REQUIRED
    assert result.actor_claim_created is False
    assert result.rendered_text is None
    assert result.model_invocation_count == 0
    assert result.v3_mutated is False

    assert result.m6_contract_id == gt0_f.m6.M6_CONTRACT_ID
    assert (
        result.m6_negative_status
        == gt0_f.m6.BLOCKED_NAMED_AUTHORITY_REQUIRED
        == gt0_f.m6.situated_expression_behavior_status()
    )
    assert result.render_contract_id == gt0_f.bounded_render.IG_RENDER_CONTRACT_ID
    assert (
        result.render_plan_authority_status
        == gt0_f.m6.BLOCKED_NAMED_AUTHORITY_REQUIRED
        == gt0_f.bounded_render.current_positive_plan_authority_status()
    )
    assert gt0_f.bounded_render.BOUND_M6_CONTRACT_ID == gt0_f.m6.M6_CONTRACT_ID

    bound_values = {
        ref.value for ref in result.receipt.output_envelope.provenance_refs
    }
    assert gt0_f.m6.M6_CONTRACT_ID in bound_values
    assert gt0_f.bounded_render.IG_RENDER_CONTRACT_ID in bound_values
    assert gt0_f.m6.BLOCKED_NAMED_AUTHORITY_REQUIRED in bound_values
    assert "M6ForbiddenBehavioralSource" in bound_values
    assert "M6NamedAuthorityRequired" in bound_values

    detail = result.receipt.detail_code
    assert "AUTHORITATIVE_M6_RENDER_NEGATIVE_BINDING" in detail
    assert f"M6_CONTRACT={gt0_f.m6.M6_CONTRACT_ID}" in detail
    assert f"RENDER_CONTRACT={gt0_f.bounded_render.IG_RENDER_CONTRACT_ID}" in detail
    assert "MODEL_CALLS=0" in detail
    assert "NO_ACTOR_SAFE_CLAIM_ENTRY" in detail
    assert "NO_RENDERED_ARTIFACT" in detail
    assert "NO_CAUSAL_RETURN" in detail


def test_gt0_f_calls_authoritative_negative_surfaces_and_never_positive_render_api(monkeypatch):
    calls = {
        "source_firewall": 0,
        "situated_status": 0,
        "owner_required": 0,
        "render_status": 0,
        "positive_render": 0,
        "claim_entry": 0,
    }

    source_firewall = gt0_f.m6.assert_behavioral_source_rejected
    situated_status = gt0_f.m6.situated_expression_behavior_status
    owner_required = gt0_f.m6.require_situated_expression_owner
    render_status = gt0_f.bounded_render.current_positive_plan_authority_status

    def counted_source(*args, **kwargs):
        calls["source_firewall"] += 1
        return source_firewall(*args, **kwargs)

    def counted_situated():
        calls["situated_status"] += 1
        return situated_status()

    def counted_owner():
        calls["owner_required"] += 1
        return owner_required()

    def counted_render_status():
        calls["render_status"] += 1
        return render_status()

    def forbidden_positive_render(*args, **kwargs):
        calls["positive_render"] += 1
        raise AssertionError("GT0 baseline must not enter positive render realization")

    def forbidden_claim_entry(*args, **kwargs):
        calls["claim_entry"] += 1
        raise AssertionError("GT0 baseline must not fabricate ActorSafeClaimEntry")

    monkeypatch.setattr(gt0_f.m6, "assert_behavioral_source_rejected", counted_source)
    monkeypatch.setattr(gt0_f.m6, "situated_expression_behavior_status", counted_situated)
    monkeypatch.setattr(gt0_f.m6, "require_situated_expression_owner", counted_owner)
    monkeypatch.setattr(
        gt0_f.bounded_render,
        "current_positive_plan_authority_status",
        counted_render_status,
    )
    monkeypatch.setattr(
        gt0_f.bounded_render,
        "realize_bounded_expression",
        forbidden_positive_render,
    )
    monkeypatch.setattr(
        gt0_f.m6,
        "make_actor_safe_claim_entry",
        forbidden_claim_entry,
    )

    result = gt0_f.run_gt0_v3_v2(_v3_result())

    assert result.receipt.status is GT0StageStatus.BLOCKED_NAMED_AUTHORITY_REQUIRED
    assert calls == {
        "source_firewall": 1,
        "situated_status": 1,
        "owner_required": 1,
        "render_status": 1,
        "positive_render": 0,
        "claim_entry": 0,
    }


@pytest.mark.parametrize("surface", ["m6_status", "render_status", "source_firewall"])
def test_gt0_f_fails_if_authoritative_negative_contract_diverges(monkeypatch, surface):
    if surface == "m6_status":
        monkeypatch.setattr(
            gt0_f.m6,
            "situated_expression_behavior_status",
            lambda: "PASS",
        )
    elif surface == "render_status":
        monkeypatch.setattr(
            gt0_f.bounded_render,
            "current_positive_plan_authority_status",
            lambda: "PASS",
        )
    else:
        monkeypatch.setattr(
            gt0_f.m6,
            "assert_behavioral_source_rejected",
            lambda *args, **kwargs: None,
        )

    with pytest.raises(AssertionError):
        gt0_f.run_gt0_v3_v2(_v3_result())
