from types import SimpleNamespace

import pytest

from rawlsing_next.closed35_evs1999_realization import (
    APPLICABLE_EDGE_CLASSES,
    CANONICAL_SHA256,
    CandidateSemanticBinding,
    DOCUMENTARY_ALIGNMENT_UNKNOWN,
    DocumentaryRoutingRule,
    DocumentaryVariableEntry,
    EVS1999RealizationError,
    R35_HOOK_BINDING,
    R35_REQUIRED_PHYSICAL_DIMENSIONS,
    ROUTING_RULES,
    SOURCE_SPECIFIC_REALIZATION_IDENTITY,
    admit_physical_incidence,
    align_documentary_semantics,
    require_common_abc_semantic_law,
    resolve_documentary_routing,
)
from rawlsing_next.pre553_physical_decoder import COMPATIBILITY_ONLY


def _variable_entry(label="Official producer label"):
    return DocumentaryVariableEntry(
        variable_name="v49_filt",
        authority_id="ZA3811_V3_0_0_VARIABLE_REPORT",
        producer_label=label,
        value_labels={"-3": "Not applicable", "1": "Often"},
        question_or_construct_ref="Q6B",
    )


def _synthetic_incidence(source_sha=CANONICAL_SHA256, **overrides):
    reader = {
        "reader": "pyreadstat",
        "reader_version": "1.3.6",
        "user_missing": True,
        "apply_value_formats": False,
        "encoding": "latin1",
        "authority_status": COMPATIBILITY_ONLY,
    }
    reader.update(overrides)
    return SimpleNamespace(source_sha256=source_sha, reader_configuration=reader)


def test_malformed_label_does_not_become_semantic_authority():
    result = align_documentary_semantics(
        "unknown_var",
        entries=(),
        compatibility_rendered_text="apparently readable but nonauthoritative latin1 text",
    )
    assert result.status == DOCUMENTARY_ALIGNMENT_UNKNOWN
    assert result.semantic_label is None
    assert result.semantic_authority_present is False


def test_official_documentary_mapping_overrides_readable_compatibility_garbage():
    result = align_documentary_semantics(
        "v49_filt",
        entries=(_variable_entry(),),
        raw_value=-3,
        compatibility_rendered_text="garbage-but-readable compatibility rendering",
    )
    assert result.status == "DOCUMENTARY_ALIGNMENT_RESOLVED"
    assert result.authority_id == "ZA3811_V3_0_0_VARIABLE_REPORT"
    assert result.semantic_label == "Official producer label"
    assert result.value_status == "DOCUMENTARY_VALUE_ALIGNMENT_RESOLVED"
    assert result.documentary_value_label == "Not applicable"


def test_unresolved_label_remains_documentary_alignment_unknown():
    unresolved = DocumentaryVariableEntry(
        variable_name="v999_unknown",
        authority_id="ZA3811_V3_0_0_VARIABLE_REPORT",
        producer_label=None,
        value_labels={},
    )
    result = align_documentary_semantics(
        "v999_unknown",
        entries=(unresolved,),
        compatibility_rendered_text="temptingly coherent compatibility text",
    )
    assert result.status == DOCUMENTARY_ALIGNMENT_UNKNOWN
    assert result.semantic_label is None


def test_exact_variable_identifier_is_required_no_fuzzy_or_neighbor_join():
    result = align_documentary_semantics(
        "v49",
        entries=(_variable_entry(),),
        compatibility_rendered_text="looks like v49_filt",
    )
    assert result.status == DOCUMENTARY_ALIGNMENT_UNKNOWN


def test_routing_comes_from_documentary_authority_not_missingness():
    absent = resolve_documentary_routing(
        "no_documented_route",
        rules=(),
        observed_missing_state="FORMAT_USER_MISSING_VALUE",
    )
    assert absent.status == DOCUMENTARY_ALIGNMENT_UNKNOWN
    assert absent.route_id is None

    resolved = resolve_documentary_routing(
        "v49_filt",
        rules=ROUTING_RULES,
        observed_missing_state="OBSERVED_STORAGE_VALUE",
    )
    assert resolved.status == "DOCUMENTARY_ROUTING_RESOLVED"
    assert resolved.route_id == "RT002"
    assert resolved.authority_id == "ZA3811_V3_0_0_VARIABLE_REPORT"


def test_release_specific_routing_precedes_master_default_for_same_exact_field():
    master = DocumentaryRoutingRule(
        "T-MASTER",
        "v49_filt",
        "EVS1999_MASTER_QUESTIONNAIRE",
        "generic master flow",
    )
    result = resolve_documentary_routing(
        "v49_filt",
        rules=(master, ROUTING_RULES[0]),
    )
    assert result.route_id == "RT002"


def test_physical_compatibility_mode_does_not_change_source_root():
    admission = admit_physical_incidence(_synthetic_incidence())
    assert admission.source_sha256 == CANONICAL_SHA256
    assert admission.compatibility_semantic_authority is False

    with pytest.raises(EVS1999RealizationError, match="source root mismatch"):
        admit_physical_incidence(_synthetic_incidence(source_sha="0" * 64))


def test_reader_config_drift_fails_closed():
    with pytest.raises(EVS1999RealizationError, match="reader/config drift"):
        admit_physical_incidence(_synthetic_incidence(reader_version="9.9.9"))
    with pytest.raises(EVS1999RealizationError, match="reader/config drift"):
        admit_physical_incidence(_synthetic_incidence(encoding="utf-8"))
    with pytest.raises(EVS1999RealizationError, match="reader/config drift"):
        admit_physical_incidence(_synthetic_incidence(apply_value_formats=True))


def test_abc_candidates_share_one_source_specific_semantic_realization_law():
    bindings = tuple(CandidateSemanticBinding(candidate) for candidate in ("A", "B", "C"))
    identity = require_common_abc_semantic_law(bindings)
    assert identity == SOURCE_SPECIFIC_REALIZATION_IDENTITY
    assert len({binding.source_specific_realization_identity for binding in bindings}) == 1

    divergent = (
        bindings[0],
        bindings[1],
        SimpleNamespace(
            candidate_id="C",
            source_sha256=CANONICAL_SHA256,
            source_specific_realization_identity="f" * 64,
        ),
    )
    with pytest.raises(EVS1999RealizationError, match="semantic realization divergence"):
        require_common_abc_semantic_law(divergent)


def test_evs1999_edge_scope_and_r35_hooks_are_frozen():
    assert APPLICABLE_EDGE_CLASSES == ("EC01", "EC02", "EC03", "EC10", "EC14")
    assert R35_HOOK_BINDING["i01_physical_metadata"]["required"] is True
    assert R35_HOOK_BINDING["i02_derivative_parentage"]["required_for_non_direct_raw"] is True
    assert tuple(R35_HOOK_BINDING["i03_source_scope"]["applicable_edge_classes"]) == APPLICABLE_EDGE_CLASSES
    assert set(R35_REQUIRED_PHYSICAL_DIMENSIONS) >= {
        "physical_metadata",
        "reader_configuration_digest",
        "compatibility_decode_evidence",
        "form_module_skip_routing_carriers",
    }
    assert R35_HOOK_BINDING["i03_source_scope"]["semantic_authority"] is False
