import pytest

from rawlsing_next.wsc_gt0_field_forge_ingress import run_gt0_field_forge_ingress
from rawlsing_next.wsc_gt0_protocol import (
    GT0ConservationEnvelope,
    GT0StageReceipt,
    GT0StageStatus,
)
from rawlsing_next.wsc_gt0_source_preff import GT0SourcePreFFResult, bind_gt0_f0


NEGATIVE_STATES = (
    GT0StageStatus.DENIED,
    GT0StageStatus.UNRESOLVED,
    GT0StageStatus.NONCOMPARABLE,
    GT0StageStatus.INTEGRITY_FAILURE,
)


def _preff_with_status(status: GT0StageStatus) -> GT0SourcePreFFResult:
    baseline = bind_gt0_f0()
    source = baseline.receipt.output_envelope
    negative = GT0ConservationEnvelope(
        semantic_owner_ref=source.semantic_owner_ref,
        object_refs=source.object_refs,
        authority_refs=source.authority_refs,
        current_selection_refs=source.current_selection_refs,
        scope_refs=source.scope_refs,
        relation_query_refs=source.relation_query_refs,
        permission_ceiling=source.permission_ceiling,
        status=status,
        dependency_refs=source.dependency_refs,
        provenance_refs=source.provenance_refs,
        replay_refs=source.replay_refs,
        information_loss=source.information_loss,
    )
    receipt = GT0StageReceipt(
        stage_id="GT0_PREFF_HOSTILE_TYPED_NEGATIVE_FIXTURE",
        status=status,
        input_envelope_hashes=(source.content_hash,),
        output_envelope=negative,
        upstream_refs=baseline.receipt.upstream_refs,
        authority_refs=baseline.receipt.authority_refs,
        replay_refs=baseline.receipt.replay_refs,
        detail_code="HOSTILE_TYPED_NEGATIVE_FIXTURE__NO_PROMOTION",
    )
    return GT0SourcePreFFResult(receipt=receipt, f0_ref=baseline.f0_ref)


@pytest.mark.parametrize("status", NEGATIVE_STATES)
def test_field_forge_ingress_conserves_typed_negative_without_promotion(status):
    preff = _preff_with_status(status)
    source = preff.receipt.output_envelope

    receipt = run_gt0_field_forge_ingress(preff)
    output = receipt.output_envelope

    assert receipt.status is status
    assert output.status is status
    assert receipt.status is not GT0StageStatus.PASS
    assert output.content_hash == source.content_hash

    assert output.semantic_owner_ref == source.semantic_owner_ref
    assert output.object_refs == source.object_refs
    assert output.authority_refs == source.authority_refs
    assert output.current_selection_refs == source.current_selection_refs
    assert output.scope_refs == source.scope_refs
    assert output.relation_query_refs == source.relation_query_refs
    assert output.permission_ceiling == source.permission_ceiling
    assert output.dependency_refs == source.dependency_refs
    assert output.provenance_refs == source.provenance_refs
    assert output.replay_refs == source.replay_refs
    assert output.information_loss == source.information_loss

    assert receipt.input_envelope_hashes == (source.content_hash,)
    assert receipt.upstream_refs == preff.receipt.upstream_refs
    assert receipt.authority_refs == preff.receipt.authority_refs
    assert receipt.replay_refs == preff.receipt.replay_refs
