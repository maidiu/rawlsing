from __future__ import annotations

import hashlib
import inspect

import pytest

from rawlsing_next.wsc_gt0_prev3_bridge import (
    GT0_F0_SOURCE_STRUCTURE_ID,
    GT0Prev3BridgeError,
    STAGE_ID,
    ZERO_V556_MARKER,
    run_gt0_prev3,
)
from rawlsing_next.wsc_gt0_protocol import (
    GT0ConservationEnvelope,
    GT0ExactRef,
    GT0PermissionError,
    GT0StageReceipt,
    GT0StageStatus,
)


def _sha(seed: str) -> str:
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()


def _ref(kind: str, value: str, seed: str | None = None) -> GT0ExactRef:
    return GT0ExactRef(
        kind=kind,
        value=value,
        content_hash=_sha(seed) if seed is not None else None,
    )


def _upstream(status: GT0StageStatus = GT0StageStatus.PASS):
    owner = _ref("SEMANTIC_OWNER", "urn:test:owner:field-forge")
    f0 = _ref("SOURCE_STRUCTURE", GT0_F0_SOURCE_STRUCTURE_ID)
    ff_ref = _ref(
        "FIELD_FORGE_REFERENCE_RECEIPT",
        "urn:test:field-forge:reference",
        "ff-reference",
    )
    authority = _ref("AUTHORITY", "urn:test:authority:field-forge", "authority")
    scope = _ref("SCOPE", "urn:test:scope:afro-r1")
    query = _ref("RELATION_QUERY", "urn:test:query:gt0-f0")
    replay = _ref("REPLAY", "urn:test:replay:field-forge", "replay")

    envelope = GT0ConservationEnvelope(
        semantic_owner_ref=owner,
        object_refs=(f0, ff_ref),
        authority_refs=(authority,),
        current_selection_refs=(),
        scope_refs=(scope,),
        relation_query_refs=(query,),
        permission_ceiling=("GT0_REFERENCE", "READ"),
        status=status,
        dependency_refs=(f0,),
        provenance_refs=(f0,),
        replay_refs=(replay,),
        information_loss="NONE__REFERENCE_PRESERVING",
    )
    receipt = GT0StageReceipt(
        stage_id="GT0_PREFF_TO_FIELD_FORGE",
        status=status,
        input_envelope_hashes=(_sha("prior-input-envelope"),),
        output_envelope=envelope,
        upstream_refs=(f0,),
        authority_refs=(authority,),
        replay_refs=(replay,),
        detail_code="REFERENCE_PRESERVED",
    )
    return receipt, f0


def test_baseline_is_undefined_without_i04_or_m1_promotion():
    upstream, f0 = _upstream()

    result = run_gt0_prev3(upstream, f0_ref=f0)

    assert result.stage_id == STAGE_ID
    assert result.status is GT0StageStatus.UNDEFINED_FOR_OBJECT
    assert result.input_envelope_hashes == (upstream.output_envelope.content_hash,)
    assert result.output_envelope.semantic_owner_ref == upstream.output_envelope.semantic_owner_ref
    assert result.output_envelope.object_refs == upstream.output_envelope.object_refs
    assert result.output_envelope.permission_ceiling == upstream.output_envelope.permission_ceiling
    assert result.output_envelope.information_loss == "NONE__REFERENCE_PRESERVING"
    assert "NO_I04_COERCION" in result.detail_code
    assert "NO_M1_DIRECT_BASIS" in result.detail_code
    assert "NO_V555_ROUTE" in result.detail_code
    assert ZERO_V556_MARKER in result.detail_code


def test_named_structural_request_blocks_instead_of_coercing_to_empirical_admission():
    upstream, f0 = _upstream()

    result = run_gt0_prev3(
        upstream,
        f0_ref=f0,
        requested_structural_meaning="STRUCTURAL_PRESSURE",
    )

    assert result.status is GT0StageStatus.BLOCKED_EXPLICIT_AUTHORITY
    assert (
        "FF_RELATION_TO_PREV3_ADMISSION_SURFACE_NOT_CURRENTLY_BOUND"
        in result.detail_code
    )
    assert result.output_envelope.object_refs == upstream.output_envelope.object_refs


def test_api_has_no_empirical_admission_escape_hatch():
    params = inspect.signature(run_gt0_prev3).parameters
    assert "structural_admission_evaluation" not in params
    assert "empirical_fact" not in params
    assert "m1_basis" not in params


def test_permission_may_narrow_but_not_widen():
    upstream, f0 = _upstream()

    narrowed = run_gt0_prev3(
        upstream,
        f0_ref=f0,
        consumer_permissions=("READ",),
    )
    assert narrowed.output_envelope.permission_ceiling == ("READ",)

    with pytest.raises(GT0PermissionError):
        run_gt0_prev3(
            upstream,
            f0_ref=f0,
            consumer_permissions=("READ", "WRITE"),
        )


def test_exact_f0_must_be_preserved_by_upstream_receipt():
    upstream, _f0 = _upstream()
    wrong = _ref("SOURCE_STRUCTURE", "cssu.r1.afrobarometer.r1.wrong")

    with pytest.raises(GT0Prev3BridgeError, match="bound GT0 source-structure seed"):
        run_gt0_prev3(upstream, f0_ref=wrong)

    exact_but_absent = _ref("SOURCE_STRUCTURE", GT0_F0_SOURCE_STRUCTURE_ID, "different")
    with pytest.raises(GT0Prev3BridgeError, match="does not preserve the exact F0"):
        run_gt0_prev3(upstream, f0_ref=exact_but_absent)


def test_upstream_nonpositive_state_is_preserved_without_promotion():
    upstream, f0 = _upstream(GT0StageStatus.DENIED)

    result = run_gt0_prev3(upstream, f0_ref=f0)

    assert result.status is GT0StageStatus.DENIED
    assert result.output_envelope.status is GT0StageStatus.DENIED
    assert "UPSTREAM_NONPOSITIVE_PRESERVED" in result.detail_code


def test_replay_identity_is_deterministic():
    upstream, f0 = _upstream()

    left = run_gt0_prev3(upstream, f0_ref=f0)
    right = run_gt0_prev3(upstream, f0_ref=f0)

    assert left.content_hash == right.content_hash
    assert left.output_envelope.content_hash == right.output_envelope.content_hash
