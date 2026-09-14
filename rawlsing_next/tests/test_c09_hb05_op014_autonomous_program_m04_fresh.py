from __future__ import annotations

from types import SimpleNamespace

import pytest

from rawlsing_next import c09_hb05_op014_autonomous_program as op
from rawlsing_next import pre553_discovery_exact as engine_mod


def _ref(seed: str):
    return {
        "kind": "TEST_EXACT_REF",
        "object_id": f"urn:rawlsing:m04:test:{seed}",
        "content_hash": (seed[0] if seed else "a") * 64,
    }


class _CatalogObject:
    def __init__(self, seed: str):
        self.ref = _ref(seed)


class _CoverageReceipt:
    def __init__(self, seed: str, state: str = "EVALUATED_SUPPORTED"):
        self.ref = _ref(seed)
        self.coverage_state = state


def _authority(**overrides):
    values = {
        "typed_state": "EXACT_BOUNDED_AUTHORIZED",
        "coverage_claim": op.COVERAGE_CLAIM,
        "algorithm_identity_if_semantically_required": op.ENGINE_CONTRACT_ID,
        "tie_order_rules": "CANONICAL_CANDIDATE_HASH_ORDER",
        "pruning_contract": {"kind": "NONE_EXACT_EVALUATE_ALL"},
        "rng_policy_if_any": None,
        "semantic_fields": {"mode": "EXACT_BOUNDED"},
        "ref": _ref("a"),
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def _inputs():
    return {
        "repository": object(),
        "discovery_authority": _authority(),
        "authority_registry": object(),
        "release_refs": (_ref("b"), _ref("c")),
        "predicate_catalog": (_CatalogObject("d"), _CatalogObject("e")),
        "query_template_catalog": (_CatalogObject("f"), _CatalogObject("1")),
    }


def _result(*, count=2, covered=2, states=None, contract=None):
    if states is None:
        states = ("EVALUATED_SUPPORTED", "EVALUATED_VALID_EMPTY")
    receipts = tuple(_CoverageReceipt(str(i + 2), state) for i, state in enumerate(states))
    return SimpleNamespace(
        contract_id=contract or op.ENGINE_CONTRACT_ID,
        coverage_claim=op.COVERAGE_CLAIM,
        candidate_count=count,
        covered_candidate_count=covered,
        receipts=receipts,
        empirical_fact_refs=(_ref("8"),),
        replay_ref=_ref("9"),
    )


def _fake_engine(result):
    def run(**kwargs):
        return result
    return run


def test_m04_exact_frozen_program_and_engine_identity():
    assert op.PROGRAM_ID == "C09_HB05_OP014_EXACT_BOUNDED_AUTONOMOUS_DISCOVERY_PROGRAM_R1"
    assert op.semantic_hash(op.FROZEN_PROGRAM_PAYLOAD) == op.FROZEN_PROGRAM_PAYLOAD_SHA256
    assert op.FROZEN_PROGRAM_PAYLOAD_SHA256 == "5ccdde46139acbc94b07afd23db62450b997deffbc094617e5a61010b3e853c8"
    loaded = op._load_engine()
    assert loaded is engine_mod.execute_exact_bounded_discovery


def test_m04_public_contract_has_no_architecture_or_verdict_controls():
    assert op.public_input_names() == (
        "repository",
        "discovery_authority",
        "authority_registry",
        "release_refs",
        "predicate_catalog",
        "query_template_catalog",
    )
    forbidden_words = ("architecture", "winner", "rank", "score", "performance", "primitive")
    assert not any(any(word in name.lower() for word in forbidden_words) for name in op.public_input_names())
    assert op.FROZEN_PROGRAM_PAYLOAD["replay"]["architecture_identity"] is False
    assert "C09_COMPARISON_VERDICT" in op.FROZEN_PROGRAM_PAYLOAD["forbidden"]


def test_m04_accepted_engine_result_schema_cannot_emit_c09_verdict():
    fields = set(engine_mod.ExactBoundedDiscoveryResult.__dataclass_fields__)
    for forbidden in ("winner", "ranking", "architecture", "performance", "c09_verdict", "verdict"):
        assert forbidden not in fields


def test_m04_preexecution_identity_is_canonical_order_invariant():
    data = _inputs()
    h1, m1 = op.build_search_input_identity(
        discovery_authority=data["discovery_authority"],
        release_refs=data["release_refs"],
        predicate_catalog=data["predicate_catalog"],
        query_template_catalog=data["query_template_catalog"],
    )
    h2, m2 = op.build_search_input_identity(
        discovery_authority=data["discovery_authority"],
        release_refs=tuple(reversed(data["release_refs"])),
        predicate_catalog=tuple(reversed(data["predicate_catalog"])),
        query_template_catalog=tuple(reversed(data["query_template_catalog"])),
    )
    assert h1 == h2
    assert m1 == m2
    assert m1["result_independent_frontier"] is True


def test_m04_exact_input_identity_changes_when_catalog_identity_changes():
    data = _inputs()
    h1, _ = op.build_search_input_identity(
        discovery_authority=data["discovery_authority"],
        release_refs=data["release_refs"],
        predicate_catalog=data["predicate_catalog"],
        query_template_catalog=data["query_template_catalog"],
    )
    changed = (_CatalogObject("7"),) + data["predicate_catalog"][1:]
    h2, _ = op.build_search_input_identity(
        discovery_authority=data["discovery_authority"],
        release_refs=data["release_refs"],
        predicate_catalog=changed,
        query_template_catalog=data["query_template_catalog"],
    )
    assert h1 != h2


def test_m04_rng_pruning_and_adaptive_frontier_fail_closed():
    base = _inputs()
    cases = (
        _authority(rng_policy_if_any={"kind": "SEEDED", "seed": 1}),
        _authority(pruning_contract={"kind": "TOP_K"}),
        _authority(semantic_fields={"mode": "EXACT_BOUNDED", "candidate_scoring_or_ranking_rule_if_any": {"controls_frontier": True}}),
    )
    for authority in cases:
        with pytest.raises(op.Op014ProgramBlocked) as exc:
            op.build_search_input_identity(
                discovery_authority=authority,
                release_refs=base["release_refs"],
                predicate_catalog=base["predicate_catalog"],
                query_template_catalog=base["query_template_catalog"],
            )
        assert exc.value.blocker_state == op.B_AUTH


def test_m04_duplicate_and_nonexact_inputs_fail_closed():
    data = _inputs()
    with pytest.raises(op.Op014ProgramBlocked) as exc:
        op.build_search_input_identity(
            discovery_authority=data["discovery_authority"],
            release_refs=(data["release_refs"][0], data["release_refs"][0]),
            predicate_catalog=data["predicate_catalog"],
            query_template_catalog=data["query_template_catalog"],
        )
    assert exc.value.blocker_state == op.B_INPUT
    bad_query = SimpleNamespace(ref={"kind": "x", "object_id": "y", "content_hash": "not-a-hash"})
    with pytest.raises(op.Op014ProgramBlocked) as exc2:
        op.build_search_input_identity(
            discovery_authority=data["discovery_authority"],
            release_refs=data["release_refs"],
            predicate_catalog=data["predicate_catalog"],
            query_template_catalog=(bad_query,),
        )
    assert exc2.value.blocker_state == op.B_INPUT


def test_m04_complete_frontier_yields_deterministic_program_receipt():
    data = _inputs()
    result = _result()
    _, r1 = op._execute_with_engine(_fake_engine(result), **data)
    _, r2 = op._execute_with_engine(_fake_engine(result), **data)
    assert r1 == r2
    assert r1.typed_state == "OP014_EXECUTED_COMPLETE_EXACT_FRONTIER"
    assert r1.candidate_count == r1.covered_candidate_count == 2
    assert r1.terminal_reason == op.TERMINATION_REASON
    assert len(r1.program_replay_sha256) == 64
    assert len(r1.receipt_sha256) == 64


def test_m04_incomplete_or_nonterminal_frontier_cannot_close():
    data = _inputs()
    incomplete = _result(count=2, covered=1)
    with pytest.raises(op.Op014ProgramBlocked) as exc:
        op._execute_with_engine(_fake_engine(incomplete), **data)
    assert exc.value.blocker_state == op.B_FRONTIER
    nonterminal = _result(states=("EVALUATED_SUPPORTED", "RUNNING"))
    with pytest.raises(op.Op014ProgramBlocked) as exc2:
        op._execute_with_engine(_fake_engine(nonterminal), **data)
    assert exc2.value.blocker_state == op.B_FRONTIER


def test_m04_engine_contract_mismatch_fails_closed():
    data = _inputs()
    bad = _result(contract="SOME_OTHER_ENGINE@9")
    with pytest.raises(op.Op014ProgramBlocked) as exc:
        op._execute_with_engine(_fake_engine(bad), **data)
    assert exc.value.blocker_state == op.B_ENGINE


def test_m04_engine_failure_is_typed_and_never_becomes_verdict():
    data = _inputs()
    def boom(**kwargs):
        raise ValueError("hostile failure")
    with pytest.raises(op.Op014ProgramBlocked) as exc:
        op._execute_with_engine(boom, **data)
    assert exc.value.blocker_state == op.B_EXEC
    assert "ValueError" in exc.value.detail


def test_m04_program_hash_tamper_fails_before_search(monkeypatch):
    data = _inputs()
    monkeypatch.setattr(op, "FROZEN_PROGRAM_PAYLOAD_SHA256", "0" * 64)
    with pytest.raises(op.Op014ProgramBlocked) as exc:
        op.build_search_input_identity(
            discovery_authority=data["discovery_authority"],
            release_refs=data["release_refs"],
            predicate_catalog=data["predicate_catalog"],
            query_template_catalog=data["query_template_catalog"],
        )
    assert exc.value.blocker_state == op.B_PROGRAM
