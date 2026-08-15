#!/usr/bin/env python3
"""Rawlsing V5 thin end-to-end implementation.

This module is deliberately narrow: it creates real layer artifacts from V552J
through V558, but those artifacts are boundary packets, readiness reports, and
forbidden-inference audits. They are not semantic/runtime/persona compilers.

The purpose is to make the future path executable before making it vivid.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
import shutil

try:
    from data.ddm_build_copy.ddm_v550_manifest import utc_now
except ModuleNotFoundError:  # pragma: no cover - keeps patch tests runnable outside the full repo
    from datetime import datetime, timezone

    def utc_now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

from data.ddm_build_copy.ddm_v5_build_standard import build_layer_build_record, build_thin_build_ledger
from data.ddm_build_copy.ddm_v554_seed_contract import build_v554_seed_contract
from data.ddm_build_copy.ddm_v555_life_course_mediation import build_v555_life_course_mediation
from data.ddm_build_copy.ddm_v556_pressureflow import build_v556_pressureflow_attractor
from data.ddm_build_copy.ddm_v557_renderer_contract import build_v557_renderer_contract
from data.ddm_build_copy.ddm_v558_runtime_input_gate import build_v558_runtime_input_gate
from data.ddm_build_copy.ddm_v558_runtime_graft_readiness import build_v558_numeric_runtime_graft_readiness
from data.ddm_build_copy.ddm_path_utils import repo_relative_path_text
from data.ddm_build_copy.ddm_survey_identity import require_survey_identity

ROOT = Path(__file__).resolve().parents[2]

THIN_SCHEMA_VERSION = "v5_thin_end_to_end_0.1"
THIN_COMPILER_VERSION = "v5_thin_end_to_end_0.1"


@dataclass(frozen=True)
class ThinLayerSpec:
    layer: str
    title: str
    artifact_slug: str
    consumes_layer: str
    consumes_artifact: str
    runtime_use_class: str
    allowed_inputs: tuple[str, ...]
    forbidden_inputs: tuple[str, ...]
    allowed_outputs: tuple[str, ...]
    forbidden_outputs: tuple[str, ...]
    required_input_files: tuple[str, ...]
    stop_if_missing: tuple[str, ...]
    payload_builder: str


LAYER_SPECS: tuple[ThinLayerSpec, ...] = (
    ThinLayerSpec(
        layer="v552j",
        title="Runtime-safe structural handoff adapter",
        artifact_slug="v552j_structural_handoff_packet",
        consumes_layer="v551j",
        consumes_artifact="v551j_certified_packet_index + v551j_reviewable_evidence_sidecar",
        runtime_use_class="structural_context_only_not_runtime_safe",
        allowed_inputs=(
            "v551j_certified_packet_index",
            "v551j_reviewable_evidence_sidecar",
            "v551j_certification_readiness_report",
            "v551j_review_readiness_report",
            "v551j_input_provenance_manifest",
        ),
        forbidden_inputs=(
            "raw_v551_relation_evidence_atoms",
            "raw_v550j_association_review_surface",
            "raw_microdata_rows",
            "v2_runtime_identity",
            "v3_backbone_state",
            "persona_or_chat_memory",
        ),
        allowed_outputs=(
            "structural_evidence_envelope",
            "known_absence_register",
            "reviewable_context_index",
            "handoff_stop_reasons",
        ),
        forbidden_outputs=(
            "person_belief",
            "parent_trait",
            "household_biography",
            "carrier_ideology",
            "actor_orientation",
            "runtime_psyche",
            "enneagram_type",
            "chat_voice",
        ),
        required_input_files=(
            "manifest/v551j_certification_readiness_report.json",
            "manifest/v551j_review_readiness_report.json",
        ),
        stop_if_missing=("manifest/v551j_certification_readiness_report.json",),
        payload_builder="_payload_v552j",
    ),
    ThinLayerSpec(
        layer="v553",
        title="Temporal structural pressure field adapter",
        artifact_slug="v553_temporal_pressure_field_packet",
        consumes_layer="v552j",
        consumes_artifact="v552j_structural_handoff_packet",
        runtime_use_class="temporal_structural_context_only_not_runtime_safe",
        allowed_inputs=("v552j_structural_handoff_packet", "v552j_readiness_report"),
        forbidden_inputs=(
            "raw_v551j_packets",
            "raw_survey_rows",
            "review_only_context_without_v552j_adapter",
            "bounded_seed_affordance",
            "life_event_story",
        ),
        allowed_outputs=(
            "temporal_pressure_slots",
            "temporalization_requirements",
            "pressure_absence_register",
            "time_axis_stop_reasons",
        ),
        forbidden_outputs=(
            "generated_life_event",
            "person_memory",
            "parent_orientation",
            "pressureflow_route",
            "enneagram_type",
            "autobiography",
        ),
        required_input_files=("packets/v552j_structural_handoff_packet.json",),
        stop_if_missing=("packets/v552j_structural_handoff_packet.json",),
        payload_builder="_payload_v553",
    ),
    ThinLayerSpec(
        layer="v554",
        title="Persona-seed contract adapter",
        artifact_slug="v554_bounded_seed_affordance_contract_packet",
        consumes_layer="v553",
        consumes_artifact="v553_temporal_pressure_field_packet",
        runtime_use_class="bounded_seed_affordance_only_not_persona",
        allowed_inputs=(
            "v553_temporal_pressure_field_packet",
            "v553_year_indexed_pressure_over_time",
            "v553_interpolated_pressure_over_time",
            "v553_readiness_report",
        ),
        forbidden_inputs=(
            "raw_survey_rows",
            "raw_v551j_packets",
            "unmediated_structural_pressure",
            "household_story",
            "parent_biography",
        ),
        allowed_outputs=(
            "bounded_seed_affordance_envelope",
            "bounded_seed_affordance_absence_register",
            "required_mediation_slots",
            "seed_contract_stop_reasons",
        ),
        forbidden_outputs=(
            "full_person",
            "chat_voice",
            "autobiography",
            "parent_story",
            "household_story",
            "enneagram_type",
            "belief_as_fact",
        ),
        required_input_files=(
            "manifest/v553_temporal_readiness_report.json",
            "manifest/v553_wave_harmonization_report.json",
            "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet",
            "packets/v553_year_indexed_pressure_over_time.parquet",
            "packets/v553_interpolated_pressure_over_time.parquet",
        ),
        stop_if_missing=(
            "manifest/v553_temporal_readiness_report.json",
            "manifest/v553_wave_harmonization_report.json",
            "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet",
            "packets/v553_year_indexed_pressure_over_time.parquet",
            "packets/v553_interpolated_pressure_over_time.parquet",
        ),
        payload_builder="_payload_v554",
    ),
    ThinLayerSpec(
        layer="v555",
        title="Life-course mediation bridge adapter",
        artifact_slug="v555_life_course_mediation_packet",
        consumes_layer="v554",
        consumes_artifact="v554_bounded_seed_affordance_contract_packet",
        runtime_use_class="generated_mediation_slots_only_not_biography",
        allowed_inputs=(
            "v554_bounded_seed_affordance_contract_packet",
            "v554_readiness_report",
            "v553_year_indexed_pressure_over_time",
            "v553_interpolated_pressure_over_time",
        ),
        forbidden_inputs=(
            "raw_v551j_packets",
            "raw_survey_rows",
            "survey_answer_as_person_fact",
            "unbounded_biographical_generation",
        ),
        allowed_outputs=(
            "mediation_slot_contracts",
            "household_mediation_required_unresolved",
            "carrier_mediation_required_unresolved",
            "life_course_stop_reasons",
        ),
        forbidden_outputs=(
            "completed_biography",
            "source_claim_as_memory",
            "named_parent_psychology",
            "household_event_story",
            "carrier_membership_as_fact",
        ),
	    required_input_files=(
	        "manifest/v554_readiness_report.json",
	        "packets/v554_bounded_seed_affordance_contract_packet.json",
	        "packets/v553_year_indexed_pressure_over_time.parquet",
	        "packets/v553_interpolated_pressure_over_time.parquet",
	        "manifest/v553_wave_harmonization_report.json",
	        "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet",
	    ),
	    stop_if_missing=(
	        "manifest/v554_readiness_report.json",
	        "packets/v554_bounded_seed_affordance_contract_packet.json",
	        "packets/v553_year_indexed_pressure_over_time.parquet",
	        "packets/v553_interpolated_pressure_over_time.parquet",
	        "manifest/v553_wave_harmonization_report.json",
	        "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet",
	    ),
        payload_builder="_payload_v555",
    ),
    ThinLayerSpec(
        layer="v556",
        title="Pressure-flow / attractor formation adapter",
        artifact_slug="v556_pressureflow_attractor_packet",
        consumes_layer="v555",
        consumes_artifact="v555_life_course_mediation_packet",
        runtime_use_class="generated_psyche_dynamics_contract_only",
	        allowed_inputs=(
	            "v555_life_course_mediation_packet",
	            "v555_readiness_report",
	            "v553_year_indexed_pressure_over_time",
	            "v553_interpolated_pressure_over_time",
	            "v553_wave_harmonization_report",
	        ),
        forbidden_inputs=(
            "raw_survey_rows",
            "raw_v551j_packets",
            "countrywide_personality",
            "enneagram_from_country",
            "enneagram_from_survey",
        ),
        allowed_outputs=(
            "pressureflow_contract_slots",
            "attractor_generation_requirements",
            "psyche_generation_absence_register",
            "pressureflow_stop_reasons",
        ),
        forbidden_outputs=(
            "static_trait_assignment",
            "enneagram_type",
            "enneagram_from_survey",
            "finished_psyche_profile",
            "chat_personality",
        ),
	        required_input_files=(
	            "manifest/v555_readiness_report.json",
	            "packets/v555_life_course_mediation_packet.json",
	            "packets/v553_year_indexed_pressure_over_time.parquet",
	            "packets/v553_interpolated_pressure_over_time.parquet",
	            "manifest/v553_wave_harmonization_report.json",
	            "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet",
	        ),
	        stop_if_missing=(
	            "manifest/v555_readiness_report.json",
	            "packets/v555_life_course_mediation_packet.json",
	            "packets/v553_year_indexed_pressure_over_time.parquet",
	            "packets/v553_interpolated_pressure_over_time.parquet",
	            "manifest/v553_wave_harmonization_report.json",
	            "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet",
	        ),
        payload_builder="_payload_v556",
    ),
    ThinLayerSpec(
        layer="v557",
        title="Phenomenological renderer packet adapter",
        artifact_slug="v557_renderer_contract_packet",
        consumes_layer="v556",
        consumes_artifact="v556_pressureflow_attractor_packet",
        runtime_use_class="renderer_contract_only_no_dialogue",
	        allowed_inputs=("v556_pressureflow_attractor_packet", "v556_readiness_report", "v553_wave_harmonization_report"),
        forbidden_inputs=(
            "raw_survey_rows",
            "raw_v551j_packets",
            "unmediated_structural_pressure",
            "evidence_as_dialogue",
            "source_claim_as_autobiography",
        ),
        allowed_outputs=(
            "renderer_input_contract",
            "render_blockers",
            "audit_requirements_for_future_app_wiring",
            "renderer_stop_reasons",
        ),
        forbidden_outputs=(
            "unaudited_persona",
            "chat_dialogue",
            "voice_sample",
            "source_claim_as_autobiography",
            "upstream_evidence_as_dialogue",
        ),
	        required_input_files=(
	            "manifest/v556_readiness_report.json",
	            "packets/v556_pressureflow_attractor_packet.json",
	            "manifest/v553_wave_harmonization_report.json",
	            "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet",
	        ),
	        stop_if_missing=(
	            "manifest/v556_readiness_report.json",
	            "packets/v556_pressureflow_attractor_packet.json",
	            "manifest/v553_wave_harmonization_report.json",
	            "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet",
        ),
        payload_builder="_payload_v557",
    ),
    ThinLayerSpec(
        layer="v558",
        title="Runtime input gate / graft readiness adapter",
        artifact_slug="v558_runtime_boundary_packet",
        consumes_layer="v557",
        consumes_artifact="v557_renderer_contract_packet",
        runtime_use_class="review_boundary_only_not_runtime_graft",
        allowed_inputs=(
            "v557_renderer_contract_packet",
            "v557_readiness_report",
            "v557_prompt_shape_audit",
            "v557_forbidden_inference_audit",
            "v557_source_to_generation_separation_ledger",
        ),
        forbidden_inputs=(
            "raw_survey_rows",
            "raw_v551j_packets",
            "unmediated_structural_pressure",
            "dialogue",
            "voice",
        ),
        allowed_outputs=(
            "v558_runtime_input_gate_report",
            "v558_runtime_graft_readiness_report",
            "normalized_runtime_input",
            "runtime_graft_blockers",
        ),
        forbidden_outputs=(
            "runtime_graft",
            "app_wiring",
            "dialogue",
            "voice",
            "persona",
        ),
        required_input_files=(
            "manifest/v557_readiness_report.json",
            "packets/v557_renderer_contract_packet.json",
            "audits/v557_prompt_shape_audit.json",
            "audits/v557_forbidden_inference_audit.json",
        ),
        stop_if_missing=(
            "manifest/v557_readiness_report.json",
            "packets/v557_renderer_contract_packet.json",
        ),
        payload_builder="_payload_v558",
    ),
)

SPEC_BY_LAYER = {spec.layer: spec for spec in LAYER_SPECS}
LAYER_REQUIREMENTS: dict[str, dict[str, Any]] = {
    "v552j": {
        "required_upstream_artifacts": [
            "packets/v551j_certified_packet_index.parquet",
            "packets/v551j_reviewable_evidence_sidecar.parquet",
            "manifest/v551j_certification_readiness_report.json",
            "manifest/v551j_review_readiness_report.json",
            "manifest/v551j_input_provenance_manifest.json",
        ],
        "required_upstream_authority": [
            "v551j certified spine",
            "v551j reviewable sidecar",
            "no runtime-safe claims",
        ],
        "downstream_outputs_expected": [
            "packets/v552j_structural_handoff_packet.json",
            "manifest/v552j_runtime_handoff_manifest.json",
            "manifest/v552j_readiness_report.json",
        ],
    },
    "v553": {
        "required_upstream_artifacts": [
            "packets/v552j_structural_handoff_packet.json",
            "manifest/v552j_readiness_report.json",
            "manifest/v552j_runtime_handoff_manifest.json",
        ],
        "required_upstream_authority": [
            "structural adapter boundary",
            "known absences preserved",
            "multiple-wave harmonization report present",
            "shared semantic/directionality/position authority preserved",
        ],
        "downstream_outputs_expected": [
            "packets/v553_temporal_pressure_field_packet.json",
            "packets/v553_year_indexed_pressure_over_time.parquet",
            "packets/v553_interpolated_pressure_over_time.parquet",
            "manifest/v553_wave_harmonization_report.json",
            "manifest/v553_temporal_readiness_report.json",
        ],
    },
    "v554": {
        "required_upstream_artifacts": [
            "packets/v553_temporal_pressure_field_packet.json",
            "packets/v553_year_indexed_pressure_over_time.parquet",
            "packets/v553_interpolated_pressure_over_time.parquet",
            "manifest/v553_temporal_readiness_report.json",
            "manifest/v553_wave_harmonization_report.json",
        ],
        "required_upstream_authority": [
            "temporal pressure field exists",
            "temporalization still thin",
            "multi-wave harmonization authority preserved",
            "no persona/runtime generation",
        ],
        "downstream_outputs_expected": [
            "packets/v554_bounded_seed_affordance_contract_packet.json",
            "packets/v554_seed_affordance_index.parquet",
            "packets/v554_demographic_slice_contract.parquet",
            "packets/v554_regional_slice_contract.parquet",
            "packets/v554_required_mediation_slot_index.parquet",
            "packets/v554_seed_absence_register.parquet",
            "packets/v554_seed_blocker_ledger.parquet",
            "packets/v554_seed_prohibition_ledger.parquet",
            "packets/v554_v555_handoff_index.parquet",
            "manifest/v554_readiness_report.json",
            "manifest/v554_input_manifest.json",
            "manifest/v554_seed_contract_manifest.json",
            "manifest/v554_v555_handoff_manifest.json",
        ],
    },
    "v555": {
        "required_upstream_artifacts": [
            "packets/v554_bounded_seed_affordance_contract_packet.json",
            "manifest/v554_readiness_report.json",
            "packets/v553_year_indexed_pressure_over_time.parquet",
            "manifest/v553_wave_harmonization_report.json",
            "v553_wave_harmonization/v553_wave_harmonization_evidence.parquet",
        ],
        "required_upstream_authority": [
            "bounded seed only",
            "seed mediated through family and household channels",
            "no biography or household story",
        ],
        "downstream_outputs_expected": [
            "packets/v555_life_course_mediation_packet.json",
            "manifest/v555_readiness_report.json",
        ],
    },
    "v556": {
        "required_upstream_artifacts": [
            "packets/v555_life_course_mediation_packet.json",
            "manifest/v555_readiness_report.json",
            "packets/v553_year_indexed_pressure_over_time.parquet",
        ],
        "required_upstream_authority": [
            "mediation slots only",
            "no Enneagram assignment",
            "no finished psyche profile",
        ],
        "downstream_outputs_expected": [
            "packets/v556_pressureflow_attractor_packet.json",
            "manifest/v556_readiness_report.json",
        ],
    },
    "v557": {
        "required_upstream_artifacts": [
            "packets/v556_pressureflow_attractor_packet.json",
            "manifest/v556_readiness_report.json",
        ],
        "required_upstream_authority": [
            "pressure-flow contract only",
            "no dialogue",
            "no voice",
            "no app-facing persona",
        ],
        "downstream_outputs_expected": [
            "packets/v557_renderer_contract_packet.json",
            "manifest/v557_readiness_report.json",
        ],
    },
    "v558": {
        "required_upstream_artifacts": [
            "packets/v557_renderer_contract_packet.json",
            "manifest/v557_readiness_report.json",
            "audits/v557_prompt_shape_audit.json",
            "audits/v557_forbidden_inference_audit.json",
        ],
        "required_upstream_authority": [
            "renderer contract boundary",
            "prompt shape audited",
            "no runtime graft yet",
        ],
        "downstream_outputs_expected": [
            "packets/v558_runtime_boundary_packet.json",
            "manifest/v558_runtime_input_gate_report.json",
            "manifest/v558_runtime_graft_readiness_report.json",
        ],
    },
}
DEPENDENCY_CHAIN = [
    {"from": "v550j", "to": "v551j", "handoff": "joint morphology -> joint evidence packets"},
    {"from": "v551", "to": "v551j", "handoff": "relation evidence atoms -> joint evidence packets"},
    {"from": "v551", "to": "v552", "handoff": "relation evidence atoms -> structural handoff"},
    {"from": "v551j", "to": "v552j", "handoff": "certified spine/reviewable sidecar -> structural adapter"},
    {"from": "v552", "to": "v552j", "handoff": "structural outputs -> adapter inputs"},
    {"from": "v552j", "to": "v553", "handoff": "structural adapter -> temporal pressure fields"},
    {"from": "v553", "to": "v554", "handoff": "temporal pressure fields -> seed contract"},
    {"from": "v554", "to": "v555", "handoff": "seed contract -> mediation bridge"},
    {"from": "v555", "to": "v556", "handoff": "mediation bridge -> pressure-flow"},
    {"from": "v556", "to": "v557", "handoff": "pressure-flow -> renderer contract"},
    {"from": "v557", "to": "v558", "handoff": "renderer contract -> runtime boundary gate"},
]


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    tmp.replace(path)


def _carry_forward_thin_context(input_root: Path, output_root: Path) -> None:
    carry_forward_paths = [
        Path("packets/v553_temporal_pressure_field_packet.json"),
        Path("packets/v553_temporal_pressure_field.parquet"),
        Path("packets/v553_year_indexed_pressure_over_time.parquet"),
        Path("packets/v553_interpolated_pressure_over_time.parquet"),
        Path("manifest/v553_temporal_readiness_report.json"),
        Path("manifest/v553_temporal_input_manifest.json"),
        Path("manifest/v553_wave_harmonization_report.json"),
        Path("v553_wave_harmonization/v553_wave_harmonization_evidence.parquet"),
        Path("manifest/v553_wave_harmonization_table.csv"),
        Path("manifest/v553_wave_harmonization_differences.csv"),
        Path("manifest/v553_wave_harmonization_build_ledger.json"),
        Path("manifest/v553_repo_discovery_report.json"),
    ]
    for rel_path in carry_forward_paths:
        source_candidates = [input_root / rel_path, input_root / rel_path.name]
        source = next((candidate for candidate in source_candidates if candidate.exists()), None)
        if source is None:
            continue
        target = output_root / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _carry_forward_layer_contract(input_root: Path, output_root: Path, spec: ThinLayerSpec) -> dict[str, Any]:
    """Copy the immediately prior layer's own contract artifacts into the next layer root.

    The thin builder keeps the chain inspectable by preserving the consumed upstream
    packet and readiness report alongside the new layer's outputs.
    """
    carried: list[str] = []
    if not spec.consumes_layer or not spec.consumes_artifact:
        return {"status": "not_applicable", "carried": carried}

    carry_forward_paths = [
        Path("packets") / f"{spec.consumes_artifact}.json",
        Path("manifest") / f"{spec.consumes_layer}_readiness_report.json",
    ]
    for rel_path in carry_forward_paths:
        source = input_root / rel_path
        if not source.exists():
            continue
        target = output_root / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        carried.append(str(rel_path))

    return {
        "status": "injected" if carried else "missing_upstream_layer_contract_artifacts",
        "carried": carried,
    }


def _inject_v553_temporal_context(
    output_root: Path,
    context_root: str | Path | None,
) -> dict[str, Any]:
    latest_root = Path(context_root) if context_root else None
    injected: list[str] = []
    if latest_root is None:
        return {
            "latest_root": "",
            "injected": injected,
            "status": "missing_explicit_v553_temporal_context_root",
        }
    if not latest_root.exists() or not latest_root.is_dir():
        return {
            "latest_root": str(latest_root),
            "injected": injected,
            "status": "explicit_v553_temporal_context_root_not_found",
        }
    if not (latest_root / "manifest" / "v553_temporal_readiness_report.json").exists():
        candidates = sorted(
            (
                path
                for path in latest_root.iterdir()
                if path.is_dir() and (path / "manifest" / "v553_temporal_readiness_report.json").exists()
            ),
            key=lambda path: path.name,
        )
        if candidates:
            latest_root = candidates[-1]

    carry_forward_paths = [
        Path("packets/v553_temporal_pressure_field_packet.json"),
        Path("packets/v553_temporal_pressure_field.parquet"),
        Path("packets/v553_year_indexed_pressure_over_time.parquet"),
        Path("packets/v553_interpolated_pressure_over_time.parquet"),
        Path("manifest/v553_temporal_readiness_report.json"),
        Path("manifest/v553_temporal_input_manifest.json"),
        Path("v553_wave_harmonization/v553_wave_harmonization_evidence.parquet"),
    ]
    for rel_path in carry_forward_paths:
        source = latest_root / rel_path
        if not source.exists():
            continue
        target = output_root / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        injected.append(str(rel_path))

    return {
        "latest_root": str(latest_root),
        "injected": injected,
        "status": "injected" if injected else "missing_v553_temporal_artifacts",
    }


def _inject_v553_wave_harmonization_context(
    output_root: Path,
    context_root: str | Path | None,
) -> dict[str, Any]:
    latest_root = Path(context_root) if context_root else None
    injected: list[str] = []
    if latest_root is None:
        return {
            "latest_root": "",
            "injected": injected,
            "status": "missing_explicit_v553_wave_harmonization_root",
        }
    if not latest_root.exists() or not latest_root.is_dir():
        return {
            "latest_root": str(latest_root),
            "injected": injected,
            "status": "explicit_v553_wave_harmonization_root_not_found",
        }

    carry_forward_paths = [
        Path("manifest/v553_wave_harmonization_report.json"),
        Path("manifest/v553_wave_harmonization_table.csv"),
        Path("manifest/v553_wave_harmonization_differences.csv"),
        Path("manifest/v553_wave_harmonization_build_ledger.json"),
        Path("manifest/v553_repo_discovery_report.json"),
        Path("v553_wave_harmonization/v553_wave_harmonization_evidence.parquet"),
    ]
    for rel_path in carry_forward_paths:
        source_candidates = [latest_root / rel_path, latest_root / rel_path.name]
        source = next((candidate for candidate in source_candidates if candidate.exists()), None)
        if source is None:
            continue
        target = output_root / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        injected.append(str(rel_path))

    return {
        "latest_root": str(latest_root),
        "injected": injected,
        "status": "injected" if injected else "missing_v553_wave_harmonization_artifacts",
    }


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if isinstance(value, float) and value != value:
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "null"} else text


def _bounded_score(value: float, default: float = 0.0) -> float:
    try:
        score = float(value)
    except Exception:
        score = default
    if score != score:
        score = default
    return max(0.0, min(1.0, score))


def _input_status_score(input_status: str) -> float:
    if input_status == "ready":
        return 1.0
    if input_status == "ready_with_input_gaps":
        return 0.65
    if input_status == "blocked_missing_required_input":
        return 0.0
    return 0.25


def _report_score(report: dict[str, Any], key: str) -> float:
    if not isinstance(report, dict):
        return 0.0
    return _bounded_score(report.get(key, 0.0))


def _report_has_actual_input_gap(report: dict[str, Any]) -> bool:
    if not isinstance(report, dict):
        return False
    for key in ("missing_required_inputs", "blocked_required_inputs", "gap_required_inputs", "stop_missing_inputs"):
        value = report.get(key)
        if isinstance(value, list) and value:
            return True
        if isinstance(value, dict) and value:
            return True
    return False


def _readiness_report_status(report: dict[str, Any]) -> tuple[str, bool | None, bool | None]:
    candidates = [
        _clean_text(report.get("status")),
        _clean_text(report.get("final_status")),
        _clean_text(report.get("input_status")),
    ]
    build_record = report.get("build_record") if isinstance(report.get("build_record"), dict) else {}
    build_status = _clean_text(build_record.get("status")) if isinstance(build_record, dict) else ""
    implementation_kind = _clean_text(report.get("implementation_kind"))
    status = next((value for value in candidates if value), "")
    lower = status.lower()
    build_lower = build_status.lower()
    ready_semantic = report.get("ready_for_semantic_deepening") if "ready_for_semantic_deepening" in report else None
    ready_runtime = report.get("ready_for_runtime_consumption") if "ready_for_runtime_consumption" in report else None
    if isinstance(ready_semantic, str):
        ready_semantic = ready_semantic.strip().lower() in {"true", "1", "yes", "y"}
    if isinstance(ready_runtime, str):
        ready_runtime = ready_runtime.strip().lower() in {"true", "1", "yes", "y"}
    if build_lower.startswith("thin_") and (not lower or lower.startswith("thin_")):
        if "blocked" in build_lower:
            return "blocked", False, False
        if "with_input_gaps" in build_lower:
            if _report_has_actual_input_gap(report):
                return "gapped", False, False
            return "ready", ready_semantic, ready_runtime
        return "ready", ready_semantic, ready_runtime
    if lower.startswith("thin_"):
        if "blocked" in lower:
            return "blocked", False, False
        if "with_input_gaps" in lower:
            if _report_has_actual_input_gap(report):
                return "gapped", False, False
            return "ready", ready_semantic, ready_runtime
        return "ready", ready_semantic, ready_runtime
    if any(token in lower for token in ("blocked", "not_ready", "missing_required_input", "missing")):
        return "blocked", False, False
    if implementation_kind in {"thin_scaffold", "boundary", "reviewable"} and ready_runtime is False and ready_semantic is not False:
        if not _report_has_actual_input_gap(report):
            return "ready", ready_semantic if isinstance(ready_semantic, bool) else True, False
    if ready_semantic is False or ready_runtime is False:
        return "gapped", bool(ready_semantic), bool(ready_runtime)
    if any(token in lower for token in ("gap", "provisional", "degraded", "partial")):
        return "gapped", ready_semantic if isinstance(ready_semantic, bool) else False, ready_runtime if isinstance(ready_runtime, bool) else False
    if status:
        return "ready", ready_semantic if isinstance(ready_semantic, bool) else True, ready_runtime if isinstance(ready_runtime, bool) else True
    return "", ready_semantic if isinstance(ready_semantic, bool) else None, ready_runtime if isinstance(ready_runtime, bool) else None


def _is_v553_temporal_boundary_input(report: dict[str, Any]) -> bool:
    if not isinstance(report, dict) or not report:
        return False
    status = _clean_text(report.get("status"))
    if status != "BLOCKED_V553_TEMPORAL_PRESSURE_FIELD":
        return False
    if _report_has_actual_input_gap(report):
        return False
    required_paths = (
        "packet_path",
        "year_indexed_pressure_path",
        "interpolated_pressure_path",
        "v553_wave_harmonization_table_path",
    )
    return all(_clean_text(report.get(key)) for key in required_paths)


def _summarize_readiness_report(report: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(report, dict) or not report:
        return {}
    summary = {
        "status": _clean_text(report.get("status")),
        "final_status": _clean_text(report.get("final_status")),
        "input_status": _clean_text(report.get("input_status")),
        "ready_for_semantic_deepening": report.get("ready_for_semantic_deepening"),
        "ready_for_runtime_consumption": report.get("ready_for_runtime_consumption"),
        "blocker_context_count": report.get("blocker_context_count"),
        "blocker_context_breakdown_json": _clean_text(report.get("blocker_context_breakdown_json")),
        "blocker_contexts_json": _clean_text(report.get("blocker_contexts_json")),
        "structural_handoff_status": _clean_text(report.get("structural_handoff_status")),
        "ready_for_v553": report.get("ready_for_v553"),
    }
    for key, value in report.items():
        if key.endswith("_score") or key in {
            "wave_coverage_score",
            "shared_semantic_score",
            "shared_directionality_score",
            "shared_position_score",
            "overlay_presence_score",
            "harmonization_score",
            "readiness_score",
        }:
            summary[key] = value
    return summary


def _exists_any(root: Path, rel_without_ext: str) -> bool:
    base = root / rel_without_ext
    if base.exists():
        return True
    for suffix in (".json", ".parquet", ".csv"):
        if Path(str(base) + suffix).exists():
            return True
    return False


def _inspect_input_root(input_root: Path, spec: ThinLayerSpec) -> dict[str, Any]:
    files = []
    missing = []
    gap_required = []
    blocked_required = []
    readiness_report_statuses: dict[str, str] = {}
    readiness_reports: dict[str, dict[str, Any]] = {}
    for rel in spec.required_input_files:
        path = input_root / rel
        exists = path.exists()
        if not exists:
            missing.append(rel)
            files.append({"relative_path": rel, "exists": exists, "report_status": "", "ready_for_semantic_deepening": None, "ready_for_runtime_consumption": None})
            continue

        report_status = ""
        ready_semantic = None
        ready_runtime = None
        if rel.endswith(".json") and "report" in rel:
            report = _read_json(path)
            readiness_reports[rel] = report
            if rel.endswith("readiness_report.json"):
                report_status, ready_semantic, ready_runtime = _readiness_report_status(report)
                if rel == "manifest/v553_temporal_readiness_report.json" and _is_v553_temporal_boundary_input(report):
                    report_status = "ready_boundary_input"
                    ready_semantic = True
                    ready_runtime = False
                readiness_report_statuses[rel] = report_status or "unknown"
                if report_status == "blocked":
                    blocked_required.append(rel)
                elif report_status == "gapped":
                    gap_required.append(rel)
            else:
                report_status = _clean_text(report.get("status")) or _clean_text(report.get("final_status"))
                readiness_report_statuses[rel] = report_status or "unknown"
        files.append(
            {
                "relative_path": rel,
                "exists": exists,
                "report_status": report_status,
                "ready_for_semantic_deepening": ready_semantic,
                "ready_for_runtime_consumption": ready_runtime,
            }
        )

    stop_missing = []
    for rel in spec.stop_if_missing:
        path = input_root / rel
        exists = path.exists()
        if not exists:
            stop_missing.append(rel)

    stop_missing.extend([rel for rel in blocked_required if rel not in stop_missing])

    input_status = "ready"
    if stop_missing or blocked_required:
        input_status = "blocked_missing_required_input"
    elif missing or gap_required:
        input_status = "ready_with_input_gaps"

    return {
        "input_root": str(input_root),
        "files": files,
        "missing_required_inputs": missing,
        "gap_required_inputs": gap_required,
        "blocked_required_inputs": blocked_required,
        "stop_missing_inputs": stop_missing,
        "readiness_report_statuses": readiness_report_statuses,
        "readiness_reports": readiness_reports,
        "input_status": input_status,
    }


def _schema_for(spec: ThinLayerSpec) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": spec.artifact_slug,
        "type": "object",
        "required": [
            "run_id",
            "layer",
            "artifact_type",
            "runtime_use_class",
            "status",
            "forbidden_outputs_written",
            "runtime_packets_written",
            "persona_fields_written",
            "payload",
        ],
        "properties": {
            "run_id": {"type": "string"},
            "layer": {"const": spec.layer},
            "artifact_type": {"const": spec.artifact_slug},
            "runtime_use_class": {"const": spec.runtime_use_class},
            "status": {"type": "string"},
            "forbidden_outputs_written": {"const": False},
            "runtime_packets_written": {"const": False},
            "persona_fields_written": {"const": False},
            "payload": {"type": "object"},
        },
        "additionalProperties": True,
    }


def _forbidden_audit(spec: ThinLayerSpec, run_id: str) -> dict[str, Any]:
    rows = []
    for value in spec.forbidden_inputs:
        rows.append(
            {
                "run_id": run_id,
                "layer": spec.layer,
                "audit_type": "forbidden_input",
                "item": value,
                "audit_status": "blocked_by_contract",
                "reason": f"{value} would bypass the {spec.layer} adapter boundary.",
            }
        )
    for value in spec.forbidden_outputs:
        rows.append(
            {
                "run_id": run_id,
                "layer": spec.layer,
                "audit_type": "forbidden_output",
                "item": value,
                "audit_status": "not_written_by_thin_compiler",
                "reason": f"{value} is outside {spec.layer}'s thin implementation authority.",
            }
        )
    return {
        "run_id": run_id,
        "layer": spec.layer,
        "row_count": len(rows),
        "rows": rows,
        "created_at": utc_now(),
        "schema_version": THIN_SCHEMA_VERSION,
        "compiler_version": THIN_COMPILER_VERSION,
    }


def _prompt_shape_audit(run_id: str, packet: dict[str, Any]) -> dict[str, Any]:
    forbidden_terms = [
        "chat_prompt",
        "system_prompt",
        "persona_sheet",
        "voice_sample",
        "I am ",
        "I feel ",
        "I remember ",
        "my mother",
        "my father",
        "I grew up",
        "as a child",
        "Enneagram type",
        "conversation_style",
        "speaking_style",
        "memory_seed",
    ]
    payload = packet.get("payload", {})
    inspected_payload = {
        "renderer_input_contract": payload.get("renderer_input_contract"),
        "runtime_wiring_contract": payload.get("runtime_wiring_contract"),
        "future_consumer_notes": payload.get("future_consumer_notes"),
        "app_wiring_boundaries": payload.get("app_wiring_boundaries"),
        "render_blockers": payload.get("render_blockers"),
        "dialogue_generated": payload.get("dialogue_generated"),
        "voice_generated": payload.get("voice_generated"),
        "prompt_shape_audit_status": payload.get("prompt_shape_audit_status"),
    }
    serialized = json.dumps(inspected_payload, sort_keys=True, ensure_ascii=False).lower()
    violations = [term for term in forbidden_terms if term.lower() in serialized]
    return {
        "run_id": run_id,
        "layer": "v557",
        "status": "prompt_shaped" if violations else "prompt_shape_clear",
        "forbidden_terms": forbidden_terms,
        "violations": violations,
        "violation_count": len(violations),
        "prompt_shape_detected": bool(violations),
        "prompt_shape_violation_count": len(violations),
        "prompt_shape_clear": not violations,
        "prompt_shape_allowed": False,
        "created_at": utc_now(),
        "schema_version": THIN_SCHEMA_VERSION,
        "compiler_version": THIN_COMPILER_VERSION,
    }


def _status_for(input_status: str) -> str:
    if input_status == "blocked_missing_required_input":
        return "THIN_BLOCKED_MISSING_REQUIRED_INPUT"
    if input_status == "ready_with_input_gaps":
        return "THIN_READY_WITH_INPUT_GAPS"
    return "THIN_READY"


def _common_payload(spec: ThinLayerSpec, input_inspection: dict[str, Any]) -> dict[str, Any]:
    readiness_reports = input_inspection.get("readiness_reports", {}) if isinstance(input_inspection.get("readiness_reports", {}), dict) else {}
    report_score_values = [
        _report_score(report, "readiness_score")
        for report in readiness_reports.values()
        if isinstance(report, dict)
    ]
    upstream_readiness_score = _bounded_score(sum(report_score_values) / len(report_score_values)) if report_score_values else 0.0
    input_readiness_score = _input_status_score(str(input_inspection.get("input_status", "")))
    boundary_only_limitations = spec.layer in {"v554", "v555", "v556", "v557"}
    limitations_kind = "boundary_only_not_runtime" if boundary_only_limitations else ""
    limitations_reason = [
        f"{spec.layer} is a boundary contract, not runtime generation",
        "ready_for_runtime_consumption is false",
    ] if boundary_only_limitations else []
    return {
        "thin_semantic_depth": "boundary_contract_only",
        "consumes_layer": spec.consumes_layer,
        "consumes_artifact": spec.consumes_artifact,
        "allowed_inputs": list(spec.allowed_inputs),
        "allowed_outputs": list(spec.allowed_outputs),
        "forbidden_inputs": list(spec.forbidden_inputs),
        "forbidden_outputs": list(spec.forbidden_outputs),
        "input_status": input_inspection["input_status"],
        "missing_required_inputs": input_inspection["missing_required_inputs"],
        "gap_required_inputs": input_inspection.get("gap_required_inputs", []),
        "blocked_required_inputs": input_inspection.get("blocked_required_inputs", []),
        "readiness_report_statuses": dict(input_inspection.get("readiness_report_statuses", {})),
        "input_readiness_score": input_readiness_score,
        "upstream_readiness_score": upstream_readiness_score,
        "boundary_readiness_score": _bounded_score((0.6 * input_readiness_score) + (0.4 * upstream_readiness_score)),
        "boundary_only_limitations": boundary_only_limitations,
        "limitations_kind": limitations_kind,
        "limitations_reason": limitations_reason,
        "upstream_authority_context": {
            "consumes_layer": spec.consumes_layer,
            "consumes_artifact": spec.consumes_artifact,
            "input_status": input_inspection["input_status"],
            "missing_required_inputs": list(input_inspection["missing_required_inputs"]),
            "gap_required_inputs": list(input_inspection.get("gap_required_inputs", [])),
            "blocked_required_inputs": list(input_inspection.get("blocked_required_inputs", [])),
            "readiness_report_statuses": dict(input_inspection.get("readiness_report_statuses", {})),
        },
        "upstream_readiness_context": {
            rel: _summarize_readiness_report(report)
            for rel, report in readiness_reports.items()
        },
        "known_absences_are_preserved": True,
        "generated_runtime_content": False,
        "source_claims_converted_to_person_facts": False,
        "upstream_requirements": LAYER_REQUIREMENTS.get(spec.layer, {}),
    }


def _layer_authority_summary(spec: ThinLayerSpec, readiness: dict[str, Any]) -> dict[str, Any]:
    packet = _read_json(Path(readiness.get("packet_path", ""))) if readiness.get("packet_path") else {}
    payload = packet.get("payload", {}) if isinstance(packet, dict) else {}
    summary = {
        "layer": spec.layer,
        "consumes_layer": spec.consumes_layer,
        "input_status": readiness.get("input_status", ""),
        "missing_required_inputs": list(readiness.get("missing_required_inputs", [])),
        "blocked_required_inputs": list(readiness.get("input_inspection", {}).get("blocked_required_inputs", []))
        if isinstance(readiness.get("input_inspection"), dict)
        else list(readiness.get("blocked_required_inputs", [])),
        "gap_required_inputs": list(readiness.get("input_inspection", {}).get("gap_required_inputs", []))
        if isinstance(readiness.get("input_inspection"), dict)
        else list(readiness.get("gap_required_inputs", [])),
        "readiness_report_statuses": dict(readiness.get("input_inspection", {}).get("readiness_report_statuses", {}))
        if isinstance(readiness.get("input_inspection"), dict)
        else dict(readiness.get("readiness_report_statuses", {})),
        "upstream_authority_context": payload.get("upstream_authority_context", {}),
        "upstream_readiness_context_keys": sorted(list(payload.get("upstream_readiness_context", {}).keys()))
        if isinstance(payload.get("upstream_readiness_context", {}), dict)
        else [],
    }
    for key in (
        "v552j_readiness_context",
        "v553_authority_context",
        "v554_authority_context",
        "v555_authority_context",
        "v556_authority_context",
    ):
        if key in payload:
            summary[key] = payload.get(key)
    return summary


def _payload_v552j(spec: ThinLayerSpec, input_inspection: dict[str, Any]) -> dict[str, Any]:
    payload = _common_payload(spec, input_inspection)
    readiness_reports = input_inspection.get("readiness_reports", {}) if isinstance(input_inspection.get("readiness_reports", {}), dict) else {}
    v552j_readiness_context = readiness_reports.get("manifest/v552j_readiness_report.json", {}) if isinstance(readiness_reports, dict) else {}
    payload.update(
        {
            "structural_evidence_envelope": {
                "certified_evidence_may_flow": True,
                "reviewable_evidence_may_flow_as_context_only": True,
                "diagnostic_or_blocked_evidence_may_flow": False,
                "runtime_safe": False,
            },
            "v552j_readiness_context": {
                "status": _clean_text(v552j_readiness_context.get("status")),
                "structural_handoff_status": _clean_text(v552j_readiness_context.get("structural_handoff_status")),
                "ready_for_v553": bool(v552j_readiness_context.get("ready_for_v553", False)),
                "blocker_contexts_json": _clean_text(v552j_readiness_context.get("blocker_contexts_json")),
                "blocker_context_breakdown_json": _clean_text(v552j_readiness_context.get("blocker_context_breakdown_json")),
                "blocker_context_count": int(v552j_readiness_context.get("blocker_context_count", 0) or 0),
            },
            "handoff_constraints": [
                "Do not treat V551J evidence certification as runtime safety.",
                "Do not collapse reviewable evidence into rejection or certification.",
                "Do not infer household/carrier/orientation/personhood here.",
            ],
        }
    )
    return payload


def _payload_v553(spec: ThinLayerSpec, input_inspection: dict[str, Any]) -> dict[str, Any]:
    payload = _common_payload(spec, input_inspection)
    payload.update(
        {
            "harmonization_contract": {
                "status": "multi_wave_authority_required",
                "scope": "cross_wave_only",
                "required_authority_kinds": ["semantic", "directionality", "position"],
                "shared_structure_required": [
                    "shared semantic columns",
                    "shared directionality columns",
                    "shared position columns",
                ],
                "forbidden_shortcuts": [
                    "single-wave temporalization",
                    "persona generation",
                    "life event narration",
                    "carrier or parent inference",
                ],
            },
            "wave_harmonization_requirements": [
                "multiple waves must be present before temporal pressure deepens",
                "wave-to-wave authority overlays must be preserved",
                "shared semantic/directionality/position structure must be explicit",
            ],
            "wave_harmonization_outputs": [
                "v553_wave_harmonization_report",
                "v553_wave_harmonization_table",
                "v553_wave_harmonization_differences",
            ],
            "temporal_pressure_slots": [
                {
                    "slot": "historical_periodization",
                    "status": "thin_contract_requires_multi_wave_harmonization",
                },
                {
                    "slot": "pressure_duration",
                    "status": "thin_contract_requires_wave_alignment",
                },
                {
                    "slot": "contradiction_sequence",
                    "status": "thin_contract_requires_authority_overlay_preservation",
                },
            ],
            "events_generated": False,
            "life_course_claims_written": False,
        }
    )
    return payload


def _payload_v554(spec: ThinLayerSpec, input_inspection: dict[str, Any]) -> dict[str, Any]:
    payload = _common_payload(spec, input_inspection)
    v553_temporal_report = input_inspection.get("readiness_reports", {}).get("manifest/v553_temporal_readiness_report.json", {})
    v553_harmonization_report = input_inspection.get("readiness_reports", {}).get("manifest/v553_wave_harmonization_report.json", {})
    v553_harmonization_evidence_path = _clean_text(v553_harmonization_report.get("wave_pair_evidence_path"))
    v553_harmonization_evidence_row_count = v553_harmonization_report.get("wave_pair_evidence_row_count")
    v553_temporal_score = _report_score(v553_temporal_report, "readiness_score")
    v553_harmonization_score = _report_score(v553_harmonization_report, "readiness_score")
    seed_readiness_score = _bounded_score(
        (0.35 if input_inspection.get("input_status") == "ready" else 0.15)
        + (0.25 if _clean_text(v553_temporal_report.get("status")) else 0.0)
        + (0.20 if _clean_text(v553_harmonization_report.get("status")) else 0.0)
        + (0.10 * v553_temporal_score)
        + (0.10 * v553_harmonization_score)
    )
    payload.update(
        {
            "v553_authority_context": {
                "temporal_readiness_report": _summarize_readiness_report(v553_temporal_report),
                "wave_harmonization_report": _summarize_readiness_report(v553_harmonization_report),
                "wave_harmonization_evidence": {
                    "path": v553_harmonization_evidence_path,
                    "row_count": v553_harmonization_evidence_row_count,
                    "exists": bool(v553_harmonization_evidence_path) and Path(v553_harmonization_evidence_path).exists(),
                },
                "authority_requires_multi_wave_harmonization": True,
                "authority_preserves_cross_wave_differences": True,
                "authority_requires_harmonization_evidence_parquet": True,
            },
            "seed_contract": {
                "status": "bounded_seed_only",
                "depends_on": [
                    "v553 temporal pressure field",
                    "v553 wave harmonization report",
                    "v553 harmonization evidence parquet",
                ],
                "runtime_positioning": [
                    "demographic slice",
                    "regional slice",
                    "national slice",
                    "subnational slice where available",
                    "ruling-class slice where available",
                    "majority-group slice where available",
                ],
                "blocked_inferences": [
                    "full persona",
                    "voice",
                    "autobiography",
                    "household story",
                    "parent psychology",
                    "carrier ideology",
                ],
            },
            "seed_blocker_ledger": [
                "missing v553 temporal pressure field",
                "missing v553 wave harmonization report",
                "no runtime personhood",
            ],
            "seed_prohibition_ledger": [
                "no voice",
                "no autobiography",
                "no finished psyche",
                "no household story",
                "no parent psychology",
                "no carrier ideology",
            ],
            "bounded_seed_affordance_envelope": {
                "seed_can_constrain_generation_later": True,
                "seed_is_not_persona": True,
                "seed_is_not_autobiography": True,
            },
            "demographic_slice_requirements": [
                "age",
                "sex",
                "race_ethnicity",
                "class_status",
                "education",
                "religious_affiliation",
                "region",
                "country",
            ],
            "regional_prior_requirements": [
                "national consensus slice",
                "subnational/regional slice",
                "ruling-class slice where available",
                "majority-group slice where available",
            ],
            "temporal_pressure_surfaces": [
                "v553_year_indexed_pressure_over_time",
                "v553_interpolated_pressure_over_time",
            ],
            "prior_authority_requirements": [
                "wave harmonization report present",
                "wave harmonization evidence parquet present",
                "cross-wave differences preserved",
                "directionality and position overlays retained",
            ],
            "required_mediation_slots": [
                "temporal_pressure_field",
                "household_or_caregiver_mediation_if_evidenced",
                "carrier_mediation_if_evidenced",
                "orientation_resolution",
                "pressureflow_mediation",
            ],
            "seed_absence_register": [
                "no full person",
                "no voice",
                "no autobiography",
                "no finished psyche",
            ],
            "seed_readiness_score": seed_readiness_score,
            "v553_temporal_score": v553_temporal_score,
            "v553_harmonization_score": v553_harmonization_score,
        }
    )
    return payload


def _payload_v555(spec: ThinLayerSpec, input_inspection: dict[str, Any]) -> dict[str, Any]:
    payload = _common_payload(spec, input_inspection)
    v554_readiness_report = input_inspection.get("readiness_reports", {}).get("manifest/v554_readiness_report.json", {})
    v553_harmonization_report = input_inspection.get("readiness_reports", {}).get("manifest/v553_wave_harmonization_report.json", {})
    v554_readiness_score = _report_score(v554_readiness_report, "boundary_readiness_score")
    v553_harmonization_evidence_path = _clean_text(v553_harmonization_report.get("wave_pair_evidence_path"))
    v553_harmonization_evidence_row_count = v553_harmonization_report.get("wave_pair_evidence_row_count")
    mediation_readiness_score = _bounded_score(
        (0.30 if input_inspection.get("input_status") == "ready" else 0.10)
        + (0.25 if _clean_text(v554_readiness_report.get("status")) else 0.0)
        + (0.25 if _clean_text(v554_readiness_report.get("seed_contract", {}).get("status") if isinstance(v554_readiness_report.get("seed_contract"), dict) else "") else 0.0)
        + (0.20 * v554_readiness_score)
    )
    payload.update(
        {
            "v554_authority_context": {
                "readiness_report": _summarize_readiness_report(v554_readiness_report),
                "mediation_requires_generated_history": True,
                "mediation_is_not_biography": True,
            },
            "v553_authority_context": {
                "wave_harmonization_report": _summarize_readiness_report(v553_harmonization_report),
                "wave_harmonization_evidence": {
                    "path": v553_harmonization_evidence_path,
                    "row_count": v553_harmonization_evidence_row_count,
                    "exists": bool(v553_harmonization_evidence_path) and Path(v553_harmonization_evidence_path).exists(),
                },
                "authority_requires_harmonization_evidence_parquet": True,
                "authority_requires_cross_wave_preservation": True,
            },
            "mediation_contract": {
                "status": "channelized_and_generated_not_factual",
                "channels": [
                    "parent",
                    "co_parent",
                    "child",
                    "household",
                    "carrier",
                ],
                "channel_separation_rules": [
                    "parent transmission is not co_parent transmission",
                    "household mediation is not parent psychology",
                    "child absorption is not biography",
                    "carrier mediation is not carrier membership as fact",
                ],
                "blocked_shortcuts": [
                    "skip family mediation and jump to psyche",
                    "convert generated mediation into survey fact",
                    "collapse co_parent and parent into one slot",
                ],
            },
            "generated_evidenced_ledger": {
                "generated": [
                    "mediation_slot_contracts",
                    "channel separation rules",
                    "required mediation channels",
                ],
                "evidenced": [
                    "upstream pressure field",
                    "upstream seed affordance constraints",
                    "authority-preserved channel routes",
                ],
                "not_evidenced": [
                    "parent biography",
                    "household event story",
                    "carrier membership as fact",
                    "child psyche",
                ],
            },
            "mediation_slot_contracts": [
                {"slot": "household_mediation", "status": "unresolved_not_story", "channel": "household", "requires": ["local surveillance", "kin density", "domestic economy"]},
                {"slot": "parent_transmission", "status": "unresolved_not_parent_psychology", "channel": "parent", "requires": ["intergenerational authority", "discipline or warmth", "obligation"]},
                {"slot": "co_parent_transmission", "status": "unresolved_not_co_parent_psychology", "channel": "co_parent", "requires": ["shared care context", "conflict or coordination", "household route"]},
                {"slot": "child_absorption_resistance", "status": "unresolved_not_psyche", "channel": "child", "requires": ["developmental stage", "absorption/resistance balance", "future recursion"]},
                {"slot": "institutional_carrier_mediation", "status": "unresolved_not_carrier_membership", "channel": "carrier", "requires": ["school/church/work exposure", "institutional pressure", "authority mediation"]},
            ],
            "mediation_channel_requirements": [
                "parent",
                "co_parent",
                "child",
                "household",
                "carrier",
            ],
            "mediation_authority_requirements": [
                "generated mediation must stay generated",
                "no asserted parent psychology",
                "no asserted household history",
                "no carrier membership as fact",
                "cross-wave harmonization evidence present",
            ],
            "transmission_distinctions": [
                "identity_with_vs.identity_from",
                "explicit_authority_vs.implicit_absorption",
                "household_channel_vs.institutional_channel",
            ],
            "mediation_stop_reasons": [
                "no completed biography",
                "no carrier membership as fact",
                "no named parent psychology",
                "no household event story",
            ],
            "biography_generated": False,
            "household_story_generated": False,
            "mediation_readiness_score": mediation_readiness_score,
            "v554_readiness_score": v554_readiness_score,
        }
    )
    return payload


def _payload_v556(spec: ThinLayerSpec, input_inspection: dict[str, Any]) -> dict[str, Any]:
    payload = _common_payload(spec, input_inspection)
    v555_readiness_report = input_inspection.get("readiness_reports", {}).get("manifest/v555_readiness_report.json", {})
    v553_harmonization_report = input_inspection.get("readiness_reports", {}).get("manifest/v553_wave_harmonization_report.json", {})
    v555_readiness_score = _report_score(v555_readiness_report, "boundary_readiness_score")
    v553_harmonization_evidence_path = _clean_text(v553_harmonization_report.get("wave_pair_evidence_path"))
    v553_harmonization_evidence_row_count = v553_harmonization_report.get("wave_pair_evidence_row_count")
    pressureflow_readiness_score = _bounded_score(
        (0.30 if input_inspection.get("input_status") == "ready" else 0.10)
        + (0.25 if _clean_text(v555_readiness_report.get("status")) else 0.0)
        + (0.25 if _clean_text(v555_readiness_report.get("mediation_contract", {}).get("status") if isinstance(v555_readiness_report.get("mediation_contract"), dict) else "") else 0.0)
        + (0.20 * v555_readiness_score)
    )
    payload.update(
        {
            "v555_authority_context": {
                "readiness_report": _summarize_readiness_report(v555_readiness_report),
                "pressureflow_requires_mediated_history": True,
                "pressureflow_is_candidate_only": True,
            },
            "v553_authority_context": {
                "wave_harmonization_report": _summarize_readiness_report(v553_harmonization_report),
                "wave_harmonization_evidence": {
                    "path": v553_harmonization_evidence_path,
                    "row_count": v553_harmonization_evidence_row_count,
                    "exists": bool(v553_harmonization_evidence_path) and Path(v553_harmonization_evidence_path).exists(),
                },
                "authority_requires_harmonization_evidence_parquet": True,
                "authority_requires_cross_wave_preservation": True,
            },
            "pressureflow_contract": {
                "status": "candidate_dynamics_only",
                "preconditions": [
                    "v555 mediated history present",
                    "v553 temporal pressure present",
                    "no finished psyche profile",
                ],
                "candidate_dynamics": [
                    "defiance",
                    "collapse",
                    "compassion",
                    "domination",
                    "withdrawal",
                    "transformation",
                ],
                "blocked_shortcuts": [
                    "direct survey-to-Enneagram assignment",
                    "static trait inference",
                    "render attractor as final identity",
                ],
            },
            "pressureflow_absence_ledger": [
                "no finished psyche profile",
                "no static trait assignment",
                "no chat personality",
                "no final identity claim",
            ],
            "pressureflow_contract_slots": [
                {"slot": "expectation_baseline", "status": "requires_v555_mediated_history", "source": "mediated history"},
                {"slot": "striving_objects", "status": "requires_v555_mediated_history", "source": "mediated history"},
                {"slot": "wound_vector", "status": "requires_v555_mediated_history", "source": "mediated history"},
                {"slot": "attractor_formation", "status": "requires_pressureflow_history_not_survey_direct", "source": "pressure-flow recurrence"},
            ],
            "evidence_requirements": [
                "mediated life-course history",
                "pressure-flow history",
                "cross-wave harmonization evidence",
                "no direct survey-to-psyche shortcut",
                "no static trait assignment",
            ],
            "route_guard_conditions": [
                "v555 mediation present",
                "v553 temporal pressure present",
                "no finished psyche profile",
                "no enneagram assignment from survey alone",
                "no direct render of candidate as identity",
            ],
            "psyche_blockers": [
                "finished_psyche_profile",
                "static_trait_assignment",
                "chat_personality",
                "survey_direct_identity_claim",
            ],
            "enneagram_assigned": False,
            "psyche_profile_generated": False,
            "pressureflow_readiness_score": pressureflow_readiness_score,
            "v555_readiness_score": v555_readiness_score,
        }
    )
    return payload


def _payload_v557(spec: ThinLayerSpec, input_inspection: dict[str, Any]) -> dict[str, Any]:
    payload = _common_payload(spec, input_inspection)
    v556_readiness_report = input_inspection.get("readiness_reports", {}).get("manifest/v556_readiness_report.json", {})
    v553_harmonization_report = input_inspection.get("readiness_reports", {}).get("manifest/v553_wave_harmonization_report.json", {})
    v556_readiness_score = _report_score(v556_readiness_report, "boundary_readiness_score")
    v553_harmonization_evidence_path = _clean_text(v553_harmonization_report.get("wave_pair_evidence_path"))
    v553_harmonization_evidence_row_count = v553_harmonization_report.get("wave_pair_evidence_row_count")
    renderer_readiness_score = _bounded_score(
        (0.35 if input_inspection.get("input_status") == "ready" else 0.10)
        + (0.25 if _clean_text(v556_readiness_report.get("status")) else 0.0)
        + (0.20 if _clean_text(v556_readiness_report.get("pressureflow_contract", {}).get("status") if isinstance(v556_readiness_report.get("pressureflow_contract"), dict) else "") else 0.0)
        + (0.20 * v556_readiness_score)
    )
    payload.update(
        {
            "v556_authority_context": {
                "readiness_report": _summarize_readiness_report(v556_readiness_report),
                "renderer_requires_pressureflow_audit": True,
                "renderer_is_boundary_only": True,
            },
            "v553_authority_context": {
                "wave_harmonization_report": _summarize_readiness_report(v553_harmonization_report),
                "wave_harmonization_evidence": {
                    "path": v553_harmonization_evidence_path,
                    "row_count": v553_harmonization_evidence_row_count,
                    "exists": bool(v553_harmonization_evidence_path) and Path(v553_harmonization_evidence_path).exists(),
                },
                "authority_requires_harmonization_evidence_parquet": True,
                "authority_requires_cross_wave_preservation": True,
            },
            "renderer_input_contract": {
                "may_render_only_after_generation_audit": True,
                "may_not_quote_or_paraphrase_upstream_evidence_as_autobiography": True,
                "may_not_speak_raw_structure_as_dialogue": True,
            },
            "runtime_wiring_contract": [
                "consume pressure-flow contract only",
                "respect upstream evidence/routing boundaries",
                "do not invent dialogue or voice from structural packets",
                "defer persona synthesis to later runtime stages",
            ],
            "future_consumer_notes": [
                "app-facing runtime must use audited downstream packets only",
                "renderer may not backfill missing persona facts",
                "any voice generation requires a separate runtime authority layer",
            ],
            "source_to_generation_separation_ledger": [
                "structure is not dialogue",
                "evidence is not autobiography",
                "rendering is not origin",
                "audited packets only",
                "cross-wave harmonization evidence preserved",
            ],
            "app_wiring_boundaries": [
                "no dialogue",
                "no voice",
                "no autobiography",
                "no unaudited persona",
            ],
            "render_blockers": [
                "missing audited V556 psyche dynamics",
                "missing source-to-generation separation ledger",
                "missing app/runtime consumption contract",
            ],
            "dialogue_generated": False,
            "voice_generated": False,
            "renderer_readiness_score": renderer_readiness_score,
            "v556_readiness_score": v556_readiness_score,
        }
    )
    return payload


def _payload_v558(spec: ThinLayerSpec, input_inspection: dict[str, Any]) -> dict[str, Any]:
    payload = _common_payload(spec, input_inspection)
    v557_readiness_report = input_inspection.get("readiness_reports", {}).get("manifest/v557_readiness_report.json", {})
    v557_prompt_audit = input_inspection.get("readiness_reports", {}).get("audits/v557_prompt_shape_audit.json", {})
    gate_readiness_score = _bounded_score(
        (0.40 if input_inspection.get("input_status") != "blocked_missing_required_input" else 0.10)
        + (0.25 if _clean_text(v557_readiness_report.get("status")) else 0.0)
        + (0.20 if bool(v557_prompt_audit.get("prompt_shape_clear", False)) else 0.0)
        + (0.15 * _report_score(v557_readiness_report, "boundary_readiness_score"))
    )
    payload.update(
        {
            "v557_authority_context": {
                "readiness_report": _summarize_readiness_report(v557_readiness_report),
                "prompt_shape_audit": v557_prompt_audit,
                "renderer_boundary_only": True,
            },
            "v558_boundary_contract": {
                "status": "runtime_input_gate_only",
                "runtime_graft_allowed": False,
                "governance_required": True,
                "prompt_shape_audit_required": True,
                "no_runtime_graft": True,
            },
            "runtime_input_gate_requirements": [
                "v557 renderer contract packet",
                "prompt shape audit",
                "forbidden inference audit",
                "governance pack review",
            ],
            "runtime_graft_requirements": [
                "normalized runtime input",
                "governance evidence",
                "no runtime leak",
                "no prompt violation",
            ],
            "runtime_graft_blockers": [
                "missing governance pack",
                "prompt shape violation",
                "runtime material leakage",
                "missing authority documents",
            ],
            "v558_handoff_ready": False,
            "v558_handoff_requirements_present": False,
            "normalized_runtime_input_status": "pending_gate_execution",
            "gate_readiness_score": gate_readiness_score,
            "v557_readiness_score": _report_score(v557_readiness_report, "boundary_readiness_score"),
        }
    )
    return payload


_PAYLOAD_BUILDERS: dict[str, Callable[[ThinLayerSpec, dict[str, Any]], dict[str, Any]]] = {
    "_payload_v552j": _payload_v552j,
    "_payload_v553": _payload_v553,
    "_payload_v554": _payload_v554,
    "_payload_v555": _payload_v555,
    "_payload_v556": _payload_v556,
    "_payload_v557": _payload_v557,
    "_payload_v558": _payload_v558,
}


def build_thin_layer(
    *,
    layer: str,
    run_id: str,
    input_root: str | Path,
    output_root: str | Path,
    survey_family: str = "",
    country_code: str = "",
    v553_temporal_context_root: str | Path | None = None,
    v553_wave_harmonization_root: str | Path | None = None,
) -> dict[str, Any]:
    if layer not in SPEC_BY_LAYER:
        raise ValueError(f"Unknown thin layer: {layer}")
    identity = None
    if layer == "v553":
        identity = require_survey_identity(
            survey_family,
            "cross_wave",
            country_code,
            require_country=True,
        )
    spec = SPEC_BY_LAYER[layer]
    root = Path(output_root) / run_id
    input_root_path = Path(input_root)
    input_inspection = _inspect_input_root(input_root_path, spec)
    status = _status_for(input_inspection["input_status"])
    builder = _PAYLOAD_BUILDERS[spec.payload_builder]
    payload = builder(spec, input_inspection)

    packet = {
        "run_id": run_id,
        "layer": spec.layer,
        "title": spec.title,
        "artifact_type": spec.artifact_slug,
        "schema_version": THIN_SCHEMA_VERSION,
        "compiler_version": THIN_COMPILER_VERSION,
        "created_at": utc_now(),
        "status": status,
        "runtime_use_class": spec.runtime_use_class,
        "input_root": str(input_root_path),
        "input_inspection": input_inspection,
        "payload": payload,
        "forbidden_outputs_written": False,
        "runtime_packets_written": False,
        "persona_fields_written": False,
        "person_level_allowed": False,
        "household_level_allowed": False,
        "carrier_level_allowed": False,
        "structural_level_only": spec.layer in {"v552j", "v553"},
        "stop_reasons": input_inspection["stop_missing_inputs"],
        "v553_temporal_context": {"status": "not_applicable", "latest_root": "", "injected": []},
        "upstream_requirements": LAYER_REQUIREMENTS.get(spec.layer, {}),
        "downstream_expectations": LAYER_REQUIREMENTS.get(spec.layer, {}).get("downstream_outputs_expected", []),
        "input_readiness_score": payload.get("input_readiness_score", 0.0),
        "upstream_readiness_score": payload.get("upstream_readiness_score", 0.0),
        "boundary_readiness_score": payload.get("boundary_readiness_score", 0.0),
        "boundary_only_limitations": payload.get("boundary_only_limitations", False),
        "limitations_kind": payload.get("limitations_kind", ""),
        "limitations_reason": payload.get("limitations_reason", []),
        "source": identity.source if identity else "",
        "source_family": identity.source_key if identity else "",
        "country_code": identity.country_code if identity else "",
    }
    packet_path = root / "packets" / f"{spec.artifact_slug}.json"
    schema_path = root / "schemas" / f"{spec.artifact_slug}.schema.json"
    audit_path = root / "audits" / f"{spec.layer}_forbidden_inference_audit.json"
    readiness_path = root / "manifest" / f"{spec.layer}_readiness_report.json"
    input_manifest_path = root / "manifest" / f"{spec.layer}_input_manifest.json"
    prompt_shape_audit_path = ""
    if spec.layer == "v557":
        prompt_shape_audit = _prompt_shape_audit(run_id, packet)
        payload["prompt_shape_audit"] = prompt_shape_audit
        payload["prompt_shape_audit_status"] = prompt_shape_audit["status"]
        payload["prompt_shape_audit_detected"] = prompt_shape_audit["prompt_shape_detected"]
        payload["prompt_shape_audit_clear"] = prompt_shape_audit["prompt_shape_clear"]
        payload["prompt_shape_audit_allowed"] = prompt_shape_audit["prompt_shape_allowed"]
        payload["prompt_shape_violation_count"] = prompt_shape_audit["prompt_shape_violation_count"]
        packet["payload"] = payload
        prompt_shape_audit_path = str(root / "audits" / "v557_prompt_shape_audit.json")
    if spec.layer == "v558":
        governance_root = ROOT / "rawlsing_v5_locked_build_pack_v1" / "04_REVIEW_AND_CI"
        v558_input_gate_bundle = build_v558_runtime_input_gate(
            run_id=run_id,
            v557_run_root=input_root_path,
            output_root=root,
            governance_root=governance_root,
        )
        v558_graft_bundle = build_v558_numeric_runtime_graft_readiness(
            run_id=run_id,
            v557_run_root=input_root_path,
            output_root=root,
            governance_root=governance_root,
        )
        payload["v558_runtime_input_gate"] = v558_input_gate_bundle
        payload["v558_runtime_graft_readiness"] = v558_graft_bundle
        payload["v558_authority_context"] = {
            "v557_readiness_report": _summarize_readiness_report(input_inspection.get("readiness_reports", {}).get("manifest/v557_readiness_report.json", {})),
            "input_gate": {
                "status": v558_input_gate_bundle.get("status"),
                "ready_for_runtime_graft_review": v558_input_gate_bundle.get("ready_for_runtime_graft_review"),
                "blocker_count": v558_input_gate_bundle.get("blocker_count"),
            },
            "graft_readiness": {
                "status": v558_graft_bundle.get("status"),
                "ready_for_runtime_graft_review": v558_graft_bundle.get("ready_for_runtime_graft_review"),
                "blocker_count": v558_graft_bundle.get("blocker_count"),
            },
            "governance_root": str(governance_root),
            "authority_documents": v558_graft_bundle.get("authority_documents", []),
        }
        packet["payload"] = payload
        packet["v558_runtime_input_gate"] = v558_input_gate_bundle
        packet["v558_runtime_graft_readiness"] = v558_graft_bundle
        packet["v558_governance_root"] = str(governance_root)
        packet["status"] = v558_graft_bundle.get("status", status)
        packet["ready_for_runtime_consumption"] = False

    _write_json(packet_path, packet)
    _write_json(schema_path, _schema_for(spec))
    _write_json(audit_path, _forbidden_audit(spec, run_id))
    if spec.layer == "v557":
        _write_json(Path(prompt_shape_audit_path), packet["payload"]["prompt_shape_audit"])
    _write_json(input_manifest_path, input_inspection)
    _carry_forward_thin_context(input_root_path, root)
    upstream_layer_context = _carry_forward_layer_contract(input_root_path, root, spec)
    v554_bundle: dict[str, Any] | None = None
    v555_bundle: dict[str, Any] | None = None
    v556_bundle: dict[str, Any] | None = None
    v557_bundle: dict[str, Any] | None = None
    v558_input_gate_bundle: dict[str, Any] | None = None
    v558_graft_bundle: dict[str, Any] | None = None
    if spec.layer == "v554" and input_inspection["input_status"] == "ready":
        v554_bundle = build_v554_seed_contract(
            run_id=run_id,
            input_root=input_root_path,
            output_root=root.parent,
            input_inspection=input_inspection,
            write_csv=False,
            write_parquet=True,
        )
    if spec.layer == "v555" and input_inspection["input_status"] == "ready":
        v555_bundle = build_v555_life_course_mediation(
            run_id=run_id,
            input_root=input_root_path,
            output_root=root.parent,
            input_inspection=input_inspection,
            write_csv=False,
            write_parquet=True,
        )
    if spec.layer == "v556" and input_inspection["input_status"] == "ready":
        v556_bundle = build_v556_pressureflow_attractor(
            run_id=run_id,
            input_root=input_root_path,
            output_root=root.parent,
            input_inspection=input_inspection,
            write_csv=False,
            write_parquet=True,
        )
    if spec.layer == "v557" and input_inspection["input_status"] == "ready":
        v557_bundle = build_v557_renderer_contract(
            run_id=run_id,
            input_root=input_root_path,
            output_root=root.parent,
            input_inspection=input_inspection,
            write_csv=False,
            write_parquet=True,
        )
    if spec.layer == "v553":
        packet["v553_wave_harmonization_context"] = _inject_v553_wave_harmonization_context(
            root,
            v553_wave_harmonization_root,
        )
        packet["v553_temporal_context"] = _inject_v553_temporal_context(
            root,
            v553_temporal_context_root,
        )
        _write_json(packet_path, packet)

    build_record = build_layer_build_record(
        spec=spec,
        input_inspection=input_inspection,
        status=status,
        packet_path=str(packet_path),
        schema_path=str(schema_path),
        audit_path=str(audit_path),
        readiness_path=str(readiness_path),
        input_manifest_path=str(input_manifest_path),
        run_id=run_id,
    )

    readiness = {
        "run_id": run_id,
        "layer": spec.layer,
        "status": status,
        "implementation_kind": build_record["implementation_kind"],
        "provisionality": build_record["provisionality"],
        "scaffold_level": build_record["scaffold_level"],
        "ready_for_semantic_deepening": status == "THIN_READY" or spec.layer == "v557",
        "ready_for_runtime_consumption": False,
        "packet_path": str(packet_path),
        "schema_path": str(schema_path),
        "audit_path": str(audit_path),
        "prompt_shape_audit_path": prompt_shape_audit_path,
        "input_manifest_path": str(input_manifest_path),
        "upstream_requirements": LAYER_REQUIREMENTS.get(spec.layer, {}),
        "downstream_expectations": LAYER_REQUIREMENTS.get(spec.layer, {}).get("downstream_outputs_expected", []),
        "input_status": input_inspection["input_status"],
        "missing_required_inputs": input_inspection["missing_required_inputs"],
        "stop_reasons": input_inspection["stop_missing_inputs"],
        "input_readiness_score": payload.get("input_readiness_score", 0.0),
        "upstream_readiness_score": payload.get("upstream_readiness_score", 0.0),
        "boundary_readiness_score": payload.get("boundary_readiness_score", 0.0),
        "boundary_only_limitations": payload.get("boundary_only_limitations", False),
        "limitations_kind": payload.get("limitations_kind", ""),
        "limitations_reason": payload.get("limitations_reason", []),
        "v553_wave_harmonization_context": packet.get("v553_wave_harmonization_context", {}),
        "v553_temporal_context": packet.get("v553_temporal_context", {}),
        "upstream_layer_context": upstream_layer_context,
        "runtime_packets_written": False,
        "persona_fields_written": False,
        "forbidden_outputs_written": False,
        "continuity_checked_full": build_record["continuity_checked_full"],
        "upstream_continuity_scope": build_record["upstream_continuity_scope"],
        "upstream_continuity_result": build_record["upstream_continuity_result"],
        "downstream_continuity_scope": build_record["downstream_continuity_scope"],
        "downstream_continuity_result": build_record["downstream_continuity_result"],
        "full_upstream_and_downstream_continuity_checked": build_record["full_upstream_and_downstream_continuity_checked"],
        "how_built": build_record["how_built"],
        "continuity_notes": build_record["continuity_notes"],
        "created_at": utc_now(),
        "schema_version": THIN_SCHEMA_VERSION,
        "compiler_version": THIN_COMPILER_VERSION,
    }
    if v554_bundle is not None:
        readiness.update(v554_bundle["readiness"])
        readiness["v554_seed_contract_artifacts"] = v554_bundle.get("artifact_paths", {})
        readiness["v554_seed_contract_artifact_infos"] = v554_bundle.get("artifact_infos", {})
        readiness["status"] = v554_bundle["readiness"]["status"]
        readiness["seed_contract_status"] = v554_bundle["readiness"]["status"]
        v554_packet_updates = v554_bundle.get("packet_updates", {}) if isinstance(v554_bundle, dict) else {}
        packet["seed_contract"] = v554_packet_updates.get("seed_contract", packet.get("seed_contract", {}))
        if isinstance(packet.get("payload"), dict):
            packet["payload"]["seed_contract"] = v554_packet_updates.get("seed_contract", packet.get("payload", {}).get("seed_contract", {}))
        status = readiness["status"]
    if v555_bundle is not None:
        readiness.update(v555_bundle["readiness"])
        readiness["v555_life_course_mediation_artifacts"] = v555_bundle.get("artifact_paths", {})
        readiness["v555_life_course_mediation_artifact_infos"] = v555_bundle.get("artifact_infos", {})
        readiness["status"] = v555_bundle["readiness"]["status"]
        readiness["life_course_mediation_status"] = v555_bundle["readiness"]["status"]
        status = readiness["status"]
    if v556_bundle is not None:
        readiness.update(v556_bundle["readiness"])
        readiness["v556_pressureflow_attractor_artifacts"] = v556_bundle.get("artifact_paths", {})
        readiness["v556_pressureflow_attractor_artifact_infos"] = v556_bundle.get("artifact_infos", {})
        readiness["status"] = v556_bundle["readiness"]["status"]
        readiness["pressureflow_status"] = v556_bundle["readiness"]["status"]
        status = readiness["status"]
    if v557_bundle is not None:
        readiness.update(v557_bundle["readiness"])
        readiness["v557_renderer_contract_artifacts"] = v557_bundle.get("artifact_paths", {})
        readiness["v557_renderer_contract_artifact_infos"] = v557_bundle.get("artifact_infos", {})
        readiness["status"] = v557_bundle["readiness"]["status"]
        readiness["renderer_contract_status"] = v557_bundle["readiness"]["status"]
        status = readiness["status"]
    if spec.layer == "v558":
        if v558_input_gate_bundle is not None and v558_graft_bundle is not None:
            readiness.update(v558_input_gate_bundle)
            readiness.update(v558_graft_bundle)
            readiness["v558_runtime_input_gate_artifacts"] = {
                "report_path": v558_input_gate_bundle.get("report_path"),
                "gate_packet_path": v558_input_gate_bundle.get("gate_packet_path"),
                "audit_path": v558_input_gate_bundle.get("audit_path"),
                "validation_path": v558_input_gate_bundle.get("validation_path"),
                "build_ledger_path": v558_input_gate_bundle.get("build_ledger_path"),
            }
            readiness["v558_runtime_graft_readiness_artifacts"] = {
                "report_path": v558_graft_bundle.get("report_path"),
                "blockers_path": v558_graft_bundle.get("blockers_path"),
                "audit_path": v558_graft_bundle.get("audit_path"),
                "build_ledger_path": v558_graft_bundle.get("build_ledger_path"),
            }
            readiness["status"] = v558_graft_bundle.get("status", readiness["status"])
            readiness["runtime_input_gate_status"] = v558_input_gate_bundle.get("status", "")
            readiness["runtime_graft_status"] = v558_graft_bundle.get("status", "")
            status = readiness["status"]
    readiness["packet_path"] = repo_relative_path_text(packet_path)
    readiness["schema_path"] = repo_relative_path_text(schema_path)
    readiness["audit_path"] = repo_relative_path_text(audit_path)
    packet["ready_for_runtime_consumption"] = False
    packet["voice_fields_written"] = False
    packet["biography_fields_written"] = False
    _write_json(packet_path, packet)
    _write_json(readiness_path, readiness)
    _write_json(root / "manifest" / f"{spec.layer}_build_record.json", build_record)
    return readiness


def build_v5_thin_end_to_end(
    *,
    run_id: str,
    v551j_run_root: str | Path,
    output_root: str | Path,
    survey_family: str,
    country_code: str,
    v553_temporal_context_root: str | Path | None = None,
    v553_wave_harmonization_root: str | Path | None = None,
) -> dict[str, Any]:
    identity = require_survey_identity(
        survey_family,
        "cross_wave",
        country_code,
        require_country=True,
    )
    root = Path(output_root) / run_id
    previous_root = Path(v551j_run_root)
    layer_reports: list[dict[str, Any]] = []

    for spec in LAYER_SPECS:
        layer_output_root = root / "layers" / spec.layer
        readiness = build_thin_layer(
            layer=spec.layer,
            run_id=run_id,
            input_root=previous_root,
            output_root=layer_output_root,
            survey_family=identity.source,
            country_code=identity.country_code,
            v553_temporal_context_root=v553_temporal_context_root,
            v553_wave_harmonization_root=v553_wave_harmonization_root,
        )
        readiness["layer_output_root"] = str(layer_output_root / run_id)
        layer_reports.append(readiness)
        previous_root = layer_output_root / run_id

    layer_authority_summaries = {
        report["layer"]: _layer_authority_summary(next(spec for spec in LAYER_SPECS if spec.layer == report["layer"]), report)
        for report in layer_reports
    }

    status_counts: dict[str, int] = {}
    for report in layer_reports:
        status_counts[report["status"]] = status_counts.get(report["status"], 0) + 1

    final_status = "READY_V5_THIN_END_TO_END"
    if any(report["status"] == "THIN_BLOCKED_MISSING_REQUIRED_INPUT" for report in layer_reports):
        final_status = "READY_V5_THIN_END_TO_END_WITH_BLOCKED_THIN_LAYERS"
    elif any(bool(report.get("boundary_only_limitations", False)) for report in layer_reports):
        final_status = "READY_V5_THIN_END_TO_END_WITH_BOUNDARY_LIMITATIONS"
    elif any(report["status"] == "THIN_READY_WITH_INPUT_GAPS" for report in layer_reports):
        final_status = "READY_V5_THIN_END_TO_END_WITH_INPUT_GAPS"

    ledger = build_thin_build_ledger(run_id=run_id, records=[report for report in layer_reports], final_status=final_status)
    ledger["created_at"] = utc_now()

    summary = {
        "run_id": run_id,
        "final_status": final_status,
        "layer_count": len(layer_reports),
        "boundary_only_layer_count": sum(1 for report in layer_reports if bool(report.get("boundary_only_limitations", False))),
        "layer_status_counts": status_counts,
        "dependency_chain": DEPENDENCY_CHAIN,
        "layer_requirements": LAYER_REQUIREMENTS,
        "layer_reports": layer_reports,
        "layer_authority_summaries": layer_authority_summaries,
        "implementation_ledger": ledger,
        "ready_for_runtime_consumption": False,
        "runtime_packets_written": False,
        "persona_fields_written": False,
        "forbidden_outputs_written": False,
        "created_at": utc_now(),
        "schema_version": THIN_SCHEMA_VERSION,
        "compiler_version": THIN_COMPILER_VERSION,
        "source": identity.source,
        "source_family": identity.source_key,
        "country_code": identity.country_code,
    }
    _write_json(root / "manifest" / "v5_thin_end_to_end_readiness_report.json", summary)
    _write_json(root / "manifest" / "v5_thin_build_ledger.json", ledger)
    _write_json(
        root / "contracts" / "v5_thin_end_to_end_layer_specs.json",
        {
            "layers": [spec.__dict__ for spec in LAYER_SPECS],
            "dependency_chain": DEPENDENCY_CHAIN,
        },
    )
    return summary


def validate_thin_end_to_end(summary: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if summary.get("runtime_packets_written"):
        errors.append("thin end-to-end must not write runtime packets")
    if summary.get("persona_fields_written"):
        errors.append("thin end-to-end must not write persona fields")
    if summary.get("forbidden_outputs_written"):
        errors.append("thin end-to-end must not write forbidden outputs")
    if int(summary.get("layer_count", 0) or 0) != len(LAYER_SPECS):
        errors.append("thin end-to-end layer count mismatch")
    for report in summary.get("layer_reports", []):
        if report.get("ready_for_runtime_consumption"):
            errors.append(f"{report.get('layer')} incorrectly marked runtime-ready")
        for key in ("packet_path", "schema_path", "audit_path"):
            value = report.get(key)
            if not value or not Path(value).exists():
                errors.append(f"{report.get('layer')} missing {key}")
        if report.get("layer") == "v557":
            prompt_value = report.get("prompt_shape_audit_path")
            if not prompt_value or not Path(prompt_value).exists():
                errors.append("v557 missing prompt_shape_audit_path")
    return errors


__all__ = [
    "THIN_SCHEMA_VERSION",
    "THIN_COMPILER_VERSION",
    "LAYER_SPECS",
    "SPEC_BY_LAYER",
    "build_thin_layer",
    "build_v5_thin_end_to_end",
    "validate_thin_end_to_end",
]
