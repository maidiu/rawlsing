from rawlsing_next.wsc_gt0_end_to_end import TERMINAL, run_gt0_end_to_end
from rawlsing_next.wsc_gt0_protocol import GT0StageStatus
from rawlsing_next.wsc_gt0_source_preff import F0_SOURCE_STRUCTURE_ID, bind_gt0_f0, run_gt0_preff
from rawlsing_next.wsc_gt0_field_forge_ingress import run_gt0_field_forge_ingress
from rawlsing_next.wsc_gt0_prev3_bridge import run_gt0_prev3
from rawlsing_next.wsc_gt0_v3_runtime import run_gt0_prev3_v3
from rawlsing_next.wsc_gt0_v2_mediation import run_gt0_v3_v2


def test_integrated_gt0_reaches_expected_terminal_without_semantic_inflation():
    result = run_gt0_end_to_end()
    assert result.terminal == TERMINAL
    assert result.receipts[-1].status is GT0StageStatus.BLOCKED_NAMED_AUTHORITY_REQUIRED


def test_f0_ceiling_is_preserved_through_prev3():
    bound = bind_gt0_f0()
    assert bound.f0_ref.value == F0_SOURCE_STRUCTURE_ID
    preff = run_gt0_preff(bound)
    ff = run_gt0_field_forge_ingress(preff)
    prev3 = run_gt0_prev3(ff, f0_ref=bound.f0_ref)
    assert prev3.status is GT0StageStatus.UNDEFINED_FOR_OBJECT
    assert "NO_I04_COERCION" in prev3.detail_code
    assert "NO_M1_DIRECT_BASIS" in prev3.detail_code
    assert "ZERO_V556_OBJECTS" in prev3.detail_code


def test_named_structural_request_blocks_without_ff_to_prev3_admission_authority():
    bound = bind_gt0_f0()
    ff = run_gt0_field_forge_ingress(run_gt0_preff(bound))
    prev3 = run_gt0_prev3(ff, f0_ref=bound.f0_ref, requested_structural_meaning="STRUCTURAL_PRESSURE")
    assert prev3.status is GT0StageStatus.BLOCKED_EXPLICIT_AUTHORITY


def test_v3_and_v2_remain_zero_effect_and_nonrendering():
    bound = bind_gt0_f0()
    ff = run_gt0_field_forge_ingress(run_gt0_preff(bound))
    prev3 = run_gt0_prev3(ff, f0_ref=bound.f0_ref)
    v3 = run_gt0_prev3_v3(prev3)
    v2 = run_gt0_v3_v2(v3)
    assert v3.before == v3.after
    assert v2.actor_claim_created is False
    assert v2.rendered_text is None
    assert v2.v3_mutated is False


def test_integrated_gt0_is_deterministic_and_never_widens_permission_or_owner():
    left = run_gt0_end_to_end()
    right = run_gt0_end_to_end()
    assert left.full_thread_hash == right.full_thread_hash
    owners = {receipt.output_envelope.semantic_owner_ref for receipt in left.receipts}
    assert len(owners) == 1
    baseline_permissions = set(left.receipts[0].output_envelope.permission_ceiling)
    for receipt in left.receipts[1:]:
        assert set(receipt.output_envelope.permission_ceiling).issubset(baseline_permissions)
