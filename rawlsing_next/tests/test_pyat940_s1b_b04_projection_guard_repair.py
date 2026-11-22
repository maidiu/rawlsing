"""B04 repair: a caller-owned projection must match the config-derived rows.

The first consumer consumes respondents, row bindings, routing facts, the source
snapshot retention reference and authority snapshots directly from the supplied
projection.  Identity/version equality alone is insufficient: each of those
surfaces can be replaced while keeping the same source SHA, row count and
declared authority ref.  These are the exact bypasses the repaired binding guard
must refuse.
"""
from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    RoutingEligibilityFact,
)
from rawlsing_next.pre553_r157_projection_adapter import (
    SourceConfigurationBindingError,
    project_c11_candidate_from_config,
    verify_config_projection_binding,
)
from rawlsing_next.pre553_source_backed_c11_facade import RowRespondentBinding
from rawlsing_next.tests.test_pyat940_s1b_support import build_scenario


def _routing_with_state(projection, state: str):
    facts = list(projection.routing)
    original = facts[0]
    fields = dict(original.semantic_fields)
    fields["applicability_state"] = state
    fields["routing_state"] = state
    facts[0] = RoutingEligibilityFact(
        typed_state=state,
        authority_snapshot_refs=original.authority_snapshot_refs,
        dependency_refs=original.dependency_refs,
        producer_replay_locator_or_reference_root=(
            original.producer_replay_locator_or_reference_root
        ),
        **fields,
    )
    return tuple(facts)


def test_b04_config_derived_projection_still_passes(tmp_path):
    scenario = build_scenario(tmp_path / "positive", source_format="SAV")
    incidence = scenario["incidence"]
    try:
        verify_config_projection_binding(
            scenario["config"],
            scenario["projection"],
            source_sha256=incidence.source_sha256,
            row_count=incidence.row_count,
            row_native_keys=scenario["keys"],
        )
    finally:
        incidence.close()


def test_b04_projection_row_binding_swap_is_refused(tmp_path):
    scenario = build_scenario(tmp_path / "row-swap", source_format="SAV")
    incidence = scenario["incidence"]
    try:
        projection = scenario["projection"]
        by_row = {binding.row_ordinal: binding.respondent_ref
                  for binding in projection.row_bindings}
        swapped = tuple(
            RowRespondentBinding(
                binding.row_ordinal,
                by_row[{1: 2, 2: 1}.get(binding.row_ordinal, binding.row_ordinal)],
            )
            for binding in projection.row_bindings
        )
        tampered = replace(projection, row_bindings=swapped)
        with pytest.raises(SourceConfigurationBindingError, match="row/respondent"):
            project_c11_candidate_from_config(
                scenario["config"],
                tampered,
                cells=tuple(incidence.iter_cells(4)),
                row_native_keys=scenario["keys"],
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
    finally:
        incidence.close()


def test_b04_projection_routing_change_is_refused(tmp_path):
    scenario = build_scenario(tmp_path / "routing", source_format="SAV")
    incidence = scenario["incidence"]
    try:
        tampered = replace(
            scenario["projection"],
            routing=_routing_with_state(scenario["projection"], "ROUTING_UNKNOWN"),
        )
        with pytest.raises(SourceConfigurationBindingError, match="routing"):
            project_c11_candidate_from_config(
                scenario["config"],
                tampered,
                cells=tuple(incidence.iter_cells(4)),
                row_native_keys=scenario["keys"],
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
    finally:
        incidence.close()


def test_b04_projection_authority_snapshot_payload_change_is_refused(tmp_path):
    scenario = build_scenario(tmp_path / "authority", source_format="SAV")
    incidence = scenario["incidence"]
    try:
        projection = scenario["projection"]
        snapshots = list(projection.authority_snapshots)
        original = snapshots[0]
        fields = dict(original.semantic_fields)
        fields["governed_operations"] = tuple(
            fields["governed_operations"]) + ("SMUGGLED-OPERATION",)
        # Same declared authority_ref key, different snapshot content.
        payload_changed = AuthoritySnapshot(
            typed_state=original.typed_state,
            authority_snapshot_refs=original.authority_snapshot_refs,
            dependency_refs=original.dependency_refs,
            producer_replay_locator_or_reference_root=(
                original.producer_replay_locator_or_reference_root
            ),
            **fields,
        )
        assert payload_changed.authority_ref == original.authority_ref
        assert payload_changed.object_id != original.object_id
        snapshots[0] = payload_changed
        tampered = replace(projection, authority_snapshots=tuple(snapshots))
        with pytest.raises(
            SourceConfigurationBindingError, match="authority snapshots"
        ):
            project_c11_candidate_from_config(
                scenario["config"],
                tampered,
                cells=tuple(incidence.iter_cells(4)),
                row_native_keys=scenario["keys"],
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
    finally:
        incidence.close()


def test_b04_projection_snapshot_retention_change_is_refused(tmp_path):
    scenario = build_scenario(tmp_path / "snapshot", source_format="SAV")
    incidence = scenario["incidence"]
    try:
        projection = scenario["projection"]
        changed = replace(
            projection.source_snapshot_retention_ref,
            object_id="urn:rawlsing:s1b:other-retained-snapshot",
        )
        tampered = replace(projection, source_snapshot_retention_ref=changed)
        with pytest.raises(
            SourceConfigurationBindingError, match="snapshot retention"
        ):
            project_c11_candidate_from_config(
                scenario["config"],
                tampered,
                cells=tuple(incidence.iter_cells(4)),
                row_native_keys=scenario["keys"],
                source_sha256=incidence.source_sha256,
                row_count=incidence.row_count,
            )
    finally:
        incidence.close()
