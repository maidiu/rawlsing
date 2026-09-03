from dataclasses import replace

import pytest

import rawlsing_next.wave1_gt12_a2_real_gt1 as a2
import rawlsing_next.wave1_gt12_i03_positive_facts as gt12b
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_validated_source_backed_c11_release_from_stream,
)
from rawlsing_next.tests.test_wave1_r5_q86_c11_projection import (
    _build,
    _rows,
    _tiny_contract,
)


def _tiny_a2(monkeypatch):
    contract = replace(
        _tiny_contract(),
        source_structure_id="cssu.r1.afrobarometer.r5.fixture",
    )
    package = _build(_rows(), contract)
    release = build_validated_source_backed_c11_release_from_stream(
        package.stream, package.projection
    )
    monkeypatch.setattr(a2, "A1_RELEASE_HASH", release.release_ref.content_hash)
    monkeypatch.setattr(a2, "A1_REPLAY_HASH", release.replay_manifest.ref.content_hash)
    monkeypatch.setattr(a2, "FROZEN_BINDINGS", contract)
    monkeypatch.setattr(a2, "FROZEN_RISK_SET_ID", contract.risk_set_id)
    monkeypatch.setattr(a2, "FROZEN_RISK_SET_MEMBER_COUNT", contract.risk_set_row_count)
    monkeypatch.setattr(
        a2, "FROZEN_RISK_MEMBER_SET_SHA256", contract.risk_set_member_set_sha256
    )
    monkeypatch.setattr(gt12b, "FROZEN_R5_SOURCE_SHA256", contract.source_sha256)
    monkeypatch.setattr(gt12b, "FROZEN_RISK_SET_ID", contract.risk_set_id)
    monkeypatch.setattr(
        gt12b, "FROZEN_RISK_SET_MEMBER_COUNT", contract.risk_set_row_count
    )
    monkeypatch.setattr(
        gt12b, "FROZEN_RISK_MEMBER_SET_SHA256", contract.risk_set_member_set_sha256
    )
    return release


def test_a2_claim_scoped_authorities_bind_actual_release_universe_and_replay(monkeypatch):
    release = _tiny_a2(monkeypatch)
    result = a2.execute_and_replay_a2_gt1(release)

    context = result.context
    fact = result.execution.fact
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 1
    assert result.replay_result == result.execution.result
    assert context.query_authority.authority_kind == "PREDICATE_GRAMMAR"
    assert context.target_use_authority.authority_kind == "TARGET_USE_PERMISSION"
    assert context.binding.empirical_universe_ref == context.empirical_universe.ref
    assert context.target_use_authority.authority_ref in fact.authority_snapshot_refs
    assert context.query_authority.authority_ref in fact.authority_snapshot_refs
    assert context.target_use_authority.scope_envelope["source_universe_refs"] == [
        context.empirical_universe.ref.as_dict()
    ]


def test_a2_wrong_terminal_a1_release_hash_fails_closed(monkeypatch):
    release = _tiny_a2(monkeypatch)
    monkeypatch.setattr(a2, "A1_RELEASE_HASH", "0" * 64)
    with pytest.raises(gt12b.GT12BI03BindingError, match="terminal A1"):
        a2.build_a2_gt1_context(release)
