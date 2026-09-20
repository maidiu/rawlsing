from types import SimpleNamespace

import pytest

from rawlsing_next.closed35_evs2008_realization import (
    APPLICABLE_EDGE_CLASSES,
    BOUNDED_UNKNOWN,
    CANONICAL_SHA256,
    CandidateSemanticBinding,
    COMPATIBILITY_SEMANTIC_SCOPE,
    DocumentaryVariableEntry,
    EVS2008RealizationError,
    EVS_NEGATIVE_MISSING_DOMAIN,
    FLAG_RELATIONS,
    MR_SETS,
    MR_SET_BY_NAME,
    MR_TOPOLOGY_IDENTITY,
    PHYSICAL_COMPATIBILITY_MODE,
    R35_HOOK_BINDING,
    R35_REQUIRED_PHYSICAL_DIMENSIONS,
    SOURCE_SPECIFIC_REALIZATION_IDENTITY,
    UNKNOWN_PRODUCER_TEXT,
    V372_MISSING_DETAIL,
    V372_MISSING_STATE,
    V372_RENDERED_SENTINEL,
    admit_physical_incidence,
    align_documentary_semantics,
    assert_no_producer_checksum_claim,
    realize_mr_item_code,
    realize_v372_rendered_missing,
    require_common_abc_semantic_law,
    require_exact_mr_topology,
    resolve_mr_routing,
)
from rawlsing_next.pre553_physical_decoder import COMPATIBILITY_ONLY


def _synthetic_incidence(source_sha=CANONICAL_SHA256, **overrides):
    reader = {
        "reader": "pyreadstat",
        "reader_version": "1.3.6",
        "user_missing": True,
        "apply_value_formats": False,
        "encoding": "latin1",
        "authority_status": COMPATIBILITY_ONLY,
        "compatibility_mode": PHYSICAL_COMPATIBILITY_MODE,
        "compatibility_semantic_scope": COMPATIBILITY_SEMANTIC_SCOPE,
        "semantic_authority": False,
    }
    reader.update(overrides)
    return SimpleNamespace(source_sha256=source_sha, source_format="SAV", reader_configuration=reader)


def _exact_topology():
    return {rule.set_name: rule.members for rule in MR_SETS}


def test_compatibility_rendered_text_cannot_be_semantic_authority():
    result = align_documentary_semantics(
        "v10",
        entries=(),
        compatibility_rendered_text="readable latin1 output that is still nonauthoritative",
    )
    assert result.status == UNKNOWN_PRODUCER_TEXT
    assert result.semantic_label is None

    producer = DocumentaryVariableEntry(
        variable_name="v10",
        authority_id="ZA4800_V5_VARIABLE_REPORT",
        producer_label="Official producer semantic label",
        value_labels={"1": "Mentioned", "0": "Not mentioned"},
        question_or_construct_ref="Q5a",
    )
    resolved = align_documentary_semantics(
        "v10",
        entries=(producer,),
        raw_value=1,
        compatibility_rendered_text="contradictory compatibility rendering",
    )
    assert resolved.semantic_label == "Official producer semantic label"
    assert resolved.documentary_value_label == "Mentioned"


def test_all_13_native_mr_sets_are_explicit_and_exact():
    assert len(MR_SETS) == 13
    assert len(MR_SET_BY_NAME) == 13
    assert require_exact_mr_topology(_exact_topology()) == MR_TOPOLOGY_IDENTITY

    assert MR_SET_BY_NAME["q5a"].members == MR_SET_BY_NAME["evs_q5a"].members
    assert MR_SET_BY_NAME["q5a"].set_name != MR_SET_BY_NAME["evs_q5a"].set_name
    assert MR_SET_BY_NAME["vv25"].members == MR_SET_BY_NAME["q5a"].members[:-1]
    assert MR_SET_BY_NAME["vv25"].omitted_members == ("v25",)
    assert MR_SET_BY_NAME["vv43"].members == MR_SET_BY_NAME["q5b"].members[:-1]
    assert MR_SET_BY_NAME["vv43"].omitted_members == ("v43",)


def test_mr_flattening_is_rejected():
    flattened = _exact_topology()
    del flattened["evs_q5a"]
    with pytest.raises(EVS2008RealizationError, match="identity collapse"):
        require_exact_mr_topology(flattened)


def test_mr_overlap_collapse_or_member_drift_is_rejected():
    collapsed = _exact_topology()
    collapsed["vv25"] = collapsed["q5a"]
    with pytest.raises(EVS2008RealizationError, match="membership/order drift"):
        require_exact_mr_topology(collapsed)

    collapsed = _exact_topology()
    collapsed["evs_q107"] = collapsed["evs_q107"] + ("v324b",)
    with pytest.raises(EVS2008RealizationError, match="membership/order drift"):
        require_exact_mr_topology(collapsed)


def test_mr_rank_and_missing_state_law_is_preserved():
    q52 = MR_SET_BY_NAME["q52"]
    assert q52.selection_cap == 5
    assert q52.rank_law == "SELECTION_CAP_5__NO_RANK_SIGNIFICANCE"

    q107 = MR_SET_BY_NAME["evs_q107"]
    assert "v324b" not in q107.members
    assert "v324b" in q107.distinct_nonmember_roles

    assert realize_mr_item_code(1).is_missing is False
    assert realize_mr_item_code(0).is_missing is False
    for code, state in EVS_NEGATIVE_MISSING_DOMAIN.items():
        realized = realize_mr_item_code(code)
        assert realized.is_missing is True
        assert realized.semantic_state == state

    unknown = realize_mr_item_code(997)
    assert unknown.semantic_state == BOUNDED_UNKNOWN
    assert unknown.is_missing is None


def test_routing_is_documentary_and_never_inferred_from_missingness():
    unresolved = resolve_mr_routing(
        "q5b",
        country="SE",
        observed_missing_state="SYSTEM_MISSING",
    )
    assert unresolved.status == BOUNDED_UNKNOWN
    assert unresolved.rule_id is None

    denmark = resolve_mr_routing(
        "q5b",
        country="DK",
        observed_missing_state="OBSERVED_STORAGE_VALUE",
    )
    assert denmark.status == "DOCUMENTARY_ROUTING_RESOLVED"
    assert denmark.rule_id == "MRR_Q5B_DK"

    finland = resolve_mr_routing(
        "evs_q108",
        country="Finland",
        observed_missing_state="SYSTEM_MISSING",
    )
    assert finland.status == "DOCUMENTARY_ROUTING_RESOLVED"
    assert finland.rule_id == "MRR_Q108_FI"


def test_v372_missing_state_preserves_unknown_negative_subreason():
    realized = realize_v372_rendered_missing(V372_RENDERED_SENTINEL)
    assert realized.semantic_state == V372_MISSING_STATE
    assert realized.semantic_reason_detail == V372_MISSING_DETAIL
    assert realized.producer_missing_domain == (-1, -2, -3, -4, -5)

    with pytest.raises(EVS2008RealizationError, match="not recoverable"):
        realize_v372_rendered_missing(
            V372_RENDERED_SENTINEL,
            claimed_negative_subcode=-4,
        )


def test_documentary_alignment_cannot_mint_producer_checksum_claim():
    assert_no_producer_checksum_claim(None)
    with pytest.raises(EVS2008RealizationError, match="producer checksum"):
        assert_no_producer_checksum_claim(CANONICAL_SHA256)


def test_source_sha_and_compatibility_mode_fail_closed():
    admitted = admit_physical_incidence(_synthetic_incidence())
    assert admitted.source_sha256 == CANONICAL_SHA256
    assert admitted.compatibility_semantic_authority is False

    with pytest.raises(EVS2008RealizationError, match="source root mismatch"):
        admit_physical_incidence(_synthetic_incidence(source_sha="0" * 64))
    wrong_format = _synthetic_incidence()
    wrong_format.source_format = "DTA"
    with pytest.raises(EVS2008RealizationError, match="source format mismatch"):
        admit_physical_incidence(wrong_format)
    with pytest.raises(EVS2008RealizationError, match="reader/config drift"):
        admit_physical_incidence(_synthetic_incidence(encoding="utf-8"))
    with pytest.raises(EVS2008RealizationError, match="reader/config drift"):
        admit_physical_incidence(_synthetic_incidence(apply_value_formats=True))
    with pytest.raises(EVS2008RealizationError, match="reader/config drift"):
        admit_physical_incidence(_synthetic_incidence(semantic_authority=True))


def test_flag_relations_preserve_producer_documentary_scope():
    assert FLAG_RELATIONS["f201"]["scope"] == ("v201", "v202")
    assert FLAG_RELATIONS["f201"]["values"] == {0: "consistent", 1: "inconsistent"}
    assert FLAG_RELATIONS["f180"]["scope"] == tuple(f"v{i}" for i in range(170, 181))


def test_abc_share_one_source_specific_semantic_owner():
    bindings = tuple(CandidateSemanticBinding(candidate) for candidate in ("A", "B", "C"))
    assert require_common_abc_semantic_law(bindings) == SOURCE_SPECIFIC_REALIZATION_IDENTITY

    divergent = (
        bindings[0],
        bindings[1],
        SimpleNamespace(
            candidate_id="C",
            source_sha256=CANONICAL_SHA256,
            source_specific_realization_identity="f" * 64,
        ),
    )
    with pytest.raises(EVS2008RealizationError, match="semantic realization divergence"):
        require_common_abc_semantic_law(divergent)


def test_evs2008_edge_scope_and_r35_hooks_are_frozen():
    assert APPLICABLE_EDGE_CLASSES == ("EC01", "EC02", "EC03", "EC08", "EC14")
    assert R35_HOOK_BINDING["i01_physical_metadata"]["required"] is True
    assert R35_HOOK_BINDING["i02_derivative_parentage"]["required_for_non_direct_raw"] is True
    i03 = R35_HOOK_BINDING["i03_whole_source_physical_equivalence"]
    assert tuple(i03["applicable_edge_classes"]) == APPLICABLE_EDGE_CLASSES
    assert i03["semantic_authority"] is False
    assert set(R35_REQUIRED_PHYSICAL_DIMENSIONS) >= {
        "physical_metadata",
        "raw_storage_values",
        "typed_missingness",
        "row_replay_identity",
        "reader_configuration_digest",
        "compatibility_decode_evidence",
        "mr_topology",
    }
