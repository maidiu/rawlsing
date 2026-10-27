"""Deterministic R157 LITS lane source-configuration and fixture builder.

This helper is confined to the LITS lane write terrain.  It reads only the
frozen portable R157 evidence package and writes the four source configs, their
field-to-evidence ledgers, exact-name correspondence records, and explicitly
nonrespondent fixtures/oracles under SRC27..SRC30.

It does not read original respondent files, does not create original empirical
workloads, and does not modify the shared runtime, schema, validator or factory.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import EmpiricalUniverse, semantic_hash
from rawlsing_next.source_configuration import evidence
from rawlsing_next.source_configuration.fixture import fixture_document_sha256
from rawlsing_next.source_configuration.schema import canonical_config_hash

ROOT = Path(__file__).resolve().parents[4]
DATA_ROOT = ROOT / "rawlsing_next" / "source_configuration" / "data"
VALIDATION_ROOT = ROOT / "source_pre553_validation"
MANIFEST = evidence.load_manifest()
MANIFEST_FILES = MANIFEST["files"]

SCHEMA_ID = "PYAT_R157_SOURCE_CONFIGURATION@1.0.0"
FIXTURE_SCHEMA_ID = "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0"
P0_DEPENDENCY_COMMIT = "d8d7087a8e56c24042bf5945fea1c97eb0d6c710"
PLAN_SEAL = "4c0c619eac747afee1d8e65e1418bf2d472da4c3"
BASE_HEAD = "91441c34ee58c4c3b13dae37db70a23bb4d4c2b8"

READER_DECODER = "rawlsing_next.pre553_physical_decoder.decode_dta"
RUNTIME = {
    "projection_builder": "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
    "release_builder": "rawlsing_next.source_configuration.factory.build_validated_c11_release_from_config",
    "repository_builder": "rawlsing_next.source_configuration.factory.build_source_backed_c11_repository_from_config",
    "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
    "native_validator_stream": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
    "native_validator_incidence": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release",
    "source_read_owner": "rawlsing_next.pre553_source_read_admission.decode_with_source_read_permission",
}

FAMILIES = {
    "universe": "EmpiricalUniverse@1.0.0",
    "event": "RespondentEvent@1.0.0",
    "coordinate": "EmpiricalCoordinateFact@1.0.0",
    "routing": "RoutingEligibilityFact@1.0.0",
    "replay": "ReplayReceipt@1.0.0",
}

# Source-specific, evidence-grounded recipes.  No values here are respondent
# observations: targets are selected from exact H48/P2/full-relation rows and
# fixture cells are explicitly nonrespondent.
RECIPES: dict[str, dict[str, Any]] = {
    "SRC27": {
        "family": "LiTS",
        "wave": "2006",
        "artifact": "LiTS_I.dta",
        "release_id": "LiTS_WAVE_2006",
        "country_slot": "country",
        "country_kind": "NUMERIC_SOURCE_COUNTRY_CODE",
        "country_geography": (
            "MULTI_COUNTRY_LITS_2006__SOURCE_COUNTRY_SLOT_ORDINAL_98__"
            "SAMPLED_COUNTRY_SET_NOT_ENUMERATED_IN_RETAINED_METADATA"
        ),
        "sampling_geography": (
            "MULTI_COUNTRY_HOUSEHOLD_SAMPLE__REGION_AND_CITY_SLOTS_PRESENT__"
            "SAMPLE_FRAME_NOT_ENUMERATED"
        ),
        "target_population": (
            "HOUSEHOLDS_IN_PARTICIPATING_LITS_2006_COUNTRIES__FRAME_DETAIL_NOT_RETAINED"
        ),
        "design": "COMPLEX_HOUSEHOLD_SAMPLE__WEIGHTS_PRESENT_WITHOUT_DESIGN_AUTHORITY",
        "subject_unit": "HOUSEHOLD",
        "unit_notes": (
            "Rows are household interviews; q101/q102/q103/q104/q105 form a positional "
            "household roster. Supported q103_1/q102_1 are non-directional position-1 "
            "context responses, not forced person-level measurements."
        ),
        "form_slice": (
            "LiTS_2006_SINGLE_INSTRUMENT__ADMINISTRATION_FORM_NOT_RETAINED__"
            "NO_DEFAULT_FORM_ASSERTED"
        ),
        "targets": [
            {
                "var": "q303_3",
                "question_id": "SRC27_Q303_3_TRUST_PARLIAMENT",
                "role": "response",
                "topology_kind": "scalar",
                "occurrence_key": "source_scalar",
                "occurrence_fields": {
                    "kind": "scalar",
                    "source_topology": "scalar",
                    "position": 1,
                },
                "canonical_substantive": True,
                "semantic_role": "RELATION_EVIDENCE",
                "notes": (
                    "Source-native trust scale, signed direction certified by the exact "
                    "QSMV2 relation row; source code preserved as canonical value, no "
                    "linear normalization applied."
                ),
            },
            {
                "var": "q103_1",
                "question_id": "SRC27_Q103_1_HH_MEMBER_1_RELATION",
                "role": "repeated_response",
                "topology_kind": "REPEATED_EVENT",
                "occurrence_key": "household_member_position_1_relation",
                "occurrence_fields": {
                    "kind": "REPEATED_EVENT",
                    "source_topology": "nominal_choice",
                    "repeat_axis": "household_roster",
                    "member_position": 1,
                    "source_slot": "q103_1",
                },
                "canonical_substantive": True,
                "semantic_role": "POSITION_COORDINATE",
                "notes": (
                    "Position-1 household-roster relationship, non-directional nominal "
                    "context; repeated roster layout is explicit and not collapsed into a "
                    "single person measure."
                ),
            },
            {
                "var": "q102_1",
                "question_id": "SRC27_Q102_1_HH_MEMBER_1_GENDER",
                "role": "repeated_response",
                "topology_kind": "REPEATED_EVENT",
                "occurrence_key": "household_member_position_1_gender",
                "occurrence_fields": {
                    "kind": "REPEATED_EVENT",
                    "source_topology": "nominal_choice",
                    "repeat_axis": "household_roster",
                    "member_position": 1,
                    "source_slot": "q102_1",
                },
                "canonical_substantive": True,
                "semantic_role": "POSITION_COORDINATE",
                "notes": (
                    "Position-1 household-roster gender, non-directional nominal context; "
                    "the source code 0=female, 1=male is preserved exactly."
                ),
            },
            {
                "var": "country",
                "question_id": None,
                "role": "coordinate",
                "coordinate_kind": "SOURCE_COUNTRY_CODE",
                "unit_taxonomy": "SOURCE_COUNTRY_CODE_DOMAIN",
                "canonical_substantive": False,
                "notes": (
                    "Source country coordinate copied only as observed raw; no country "
                    "crosswalk, no population frame and no default ZZ universe."
                ),
            },
        ],
        "fixture": {
            "fixture_id": "R157-LITS-SRC27-NONRESPONDENT",
            "country_values": [1.0, 2.0, 3.0, 4.0, 5.0],
            "cells": {
                "q303_3": [4.0, 5.0, 6.0, None, 1.0],
                "q103_1": [1.0, 2.0, 4.0, None, 98.0],
                "q102_1": [0.0, 1.0, 0.0, None, 1.0],
            },
            "shape_coverage": [
                "DTA scalar trust item with exact source codes 1..5, DK code 6 and system-missing cell",
                "DTA positional household-roster relationship repeated item (position 1) with nominal source codes",
                "DTA positional household-roster gender repeated item (position 1) with source codes 0/1",
                "source numeric country coordinate copied raw; fixture codes are nonrespondent fixture values",
            ],
        },
    },
    "SRC28": {
        "family": "LiTS",
        "wave": "II",
        "artifact": "LiTS_II.dta",
        "release_id": "LiTS_WAVE_II",
        "country_slot": "country",
        "country_kind": "NUMERIC_SOURCE_COUNTRY_CODE",
        "country_geography": (
            "MULTI_COUNTRY_LITS_II__SOURCE_COUNTRY_SLOT_ORDINAL_2__"
            "CODEBOOK_DOMAIN_194_COUNTRIES__SAMPLED_COUNTRY_SET_NOT_ENUMERATED"
        ),
        "sampling_geography": (
            "MULTI_COUNTRY_HOUSEHOLD_SAMPLE__PSU_SLOT_ORDINAL_4__HH_SLOT_ORDINAL_5"
        ),
        "target_population": (
            "HOUSEHOLDS_IN_PARTICIPATING_LITS_II_COUNTRIES__FRAME_DETAIL_NOT_RETAINED"
        ),
        "design": (
            "COMPLEX_HOUSEHOLD_SAMPLE__WEIGHT_SLOT_626_DEMOCRATIC_WEIGHT__"
            "DESIGN_AUTHORITY_NOT_RETAINED"
        ),
        "subject_unit": "HOUSEHOLD",
        "unit_notes": (
            "Rows are household interviews; select/select2/oneper and the q102/q103 "
            "roster positions retain the source administration structure. Supported "
            "q303f/q708 are respondent-level scalar/binary items; roster repeats remain "
            "held where routing is unresolved or conditional."
        ),
        "form_slice": (
            "LiTS_II_SINGLE_INSTRUMENT__ONE_OR_TWO_RESPONDENT_ADMINISTRATION_INDICATORS_PRESENT__"
            "EXACT_FORM_ASSIGNMENT_NOT_RETAINED"
        ),
        "targets": [
            {
                "var": "q303f",
                "question_id": "SRC28_Q303F_TRUST_COURTS",
                "role": "response",
                "topology_kind": "scalar",
                "occurrence_key": "source_scalar",
                "occurrence_fields": {
                    "kind": "scalar",
                    "source_topology": "scalar",
                    "position": 1,
                },
                "canonical_substantive": True,
                "semantic_role": "RELATION_EVIDENCE",
                "notes": (
                    "Source-native institutional trust scale; negative special codes "
                    "preserve Not stated/Filtered/Don't know/Not applicable/Refused."
                ),
            },
            {
                "var": "q708",
                "question_id": "SRC28_Q708_MOVE_ABROAD_INTENTION",
                "role": "response",
                "topology_kind": "binary_contrast",
                "occurrence_key": "source_binary_contrast",
                "occurrence_fields": {
                    "kind": "binary_contrast",
                    "source_topology": "binary_contrast",
                    "position": 1,
                },
                "canonical_substantive": True,
                "semantic_role": "RELATION_EVIDENCE",
                "notes": (
                    "Source-native binary intention item with exact Yes/No and special "
                    "codes; no scalar/person default."
                ),
            },
            {
                "var": "country",
                "question_id": None,
                "role": "coordinate",
                "coordinate_kind": "SOURCE_COUNTRY_CODE",
                "unit_taxonomy": "SOURCE_COUNTRY_CODE_DOMAIN",
                "canonical_substantive": False,
                "notes": (
                    "Source country coordinate copied only as observed raw; the 194-label "
                    "codebook domain is not a claim that all countries were sampled."
                ),
            },
        ],
        "fixture": {
            "fixture_id": "R157-LITS-SRC28-NONRESPONDENT",
            "country_values": [1.0, 2.0, 3.0, 4.0, 5.0],
            "cells": {
                "q303f": [4.0, -97.0, -99.0, -98.0, None],
                "q708": [1.0, 2.0, -1.0, -90.0, None],
            },
            "shape_coverage": [
                "DTA scalar trust item with substantive, Don't know, Refused, Not applicable and system-missing cells",
                "DTA binary-contrast intention item with Yes, No, Not stated and Filtered cells",
                "negative source special codes preserved as observed storage values and mapped to exact response states",
                "source numeric country coordinate copied raw; fixture codes are nonrespondent fixture values",
            ],
        },
    },
    "SRC29": {
        "family": "LiTS",
        "wave": "III",
        "artifact": "LiTS_III.dta",
        "release_id": "LiTS_WAVE_III",
        "country_slot": "country",
        "country_kind": "STRING_SOURCE_COUNTRY_VALUE",
        "country_geography": (
            "MULTI_COUNTRY_LITS_III__SOURCE_COUNTRY_SLOT_ORDINAL_1_STRING__"
            "SAMPLED_COUNTRY_SET_NOT_ENUMERATED_IN_RETAINED_METADATA"
        ),
        "sampling_geography": (
            "MULTI_COUNTRY_HOUSEHOLD_SAMPLE__PSU_NUMBER_SLOT_4__PSU_NAME_SLOT_5__"
            "REGION_NAME_SLOT_8"
        ),
        "target_population": (
            "HOUSEHOLDS_IN_PARTICIPATING_LITS_III_COUNTRIES__PRIMARY_AND_SECONDARY_"
            "RESPONDENT_BLOCKS__FRAME_DETAIL_NOT_RETAINED"
        ),
        "design": (
            "COMPLEX_HOUSEHOLD_SAMPLE__WEIGHT_POPULATION_SAMPLE_ONE_SLOTS_PRESENT__"
            "DESIGN_AUTHORITY_NOT_RETAINED"
        ),
        "subject_unit": "HOUSEHOLD_WITH_PRIMARY_AND_SECONDARY_RESPONDENT_BLOCKS",
        "unit_notes": (
            "Rows are household interviews containing explicit primary-respondent (PRq*) "
            "and secondary-respondent (SRq*) blocks. The supported PRq315/SRq315 pair is "
            "kept as two distinct repeated measurements on the same household row; rows "
            "are not reinterpreted as persons."
        ),
        "form_slice": (
            "LiTS_III_SINGLE_INSTRUMENT__PRIMARY_AND_SECONDARY_RESPONDENT_BLOCKS__"
            "SECTION_ORDER_AND_FORM_ASSIGNMENT_NOT_RETAINED"
        ),
        "targets": [
            {
                "var": "PRq306",
                "question_id": "SRC29_PRQ306_PRIMARY_LAND_OWNERSHIP",
                "role": "response",
                "topology_kind": "ordinal_context",
                "occurrence_key": "primary_respondent_land_ownership",
                "occurrence_fields": {
                    "kind": "ordinal_context",
                    "source_topology": "ordinal_context",
                    "respondent_block": "PRIMARY",
                    "position": 1,
                },
                "canonical_substantive": True,
                "semantic_role": "STRUCTURAL_CONTEXT",
                "notes": (
                    "Primary-respondent land-ownership context response, non-directional; "
                    "source code labels are preserved without inventing a yes/no collapse."
                ),
            },
            {
                "var": "PRq315",
                "question_id": "SRC29_PRQ315_PRIMARY_WEALTH_LADDER",
                "role": "repeated_response",
                "topology_kind": "REPEATED_MEASUREMENT",
                "occurrence_key": "primary_respondent_wealth_ladder",
                "occurrence_fields": {
                    "kind": "REPEATED_MEASUREMENT",
                    "source_topology": "ordinal_context",
                    "respondent_block": "PRIMARY",
                    "position": 1,
                },
                "canonical_substantive": True,
                "semantic_role": "POSITION_COORDINATE",
                "notes": (
                    "Primary-respondent 1..10 wealth-ladder position with Don't know/Refusal "
                    "specials; unsigned source context, no direction claim."
                ),
            },
            {
                "var": "SRq315",
                "question_id": "SRC29_SRQ315_SECONDARY_WEALTH_LADDER",
                "role": "repeated_response",
                "topology_kind": "REPEATED_MEASUREMENT",
                "occurrence_key": "secondary_respondent_wealth_ladder",
                "occurrence_fields": {
                    "kind": "REPEATED_MEASUREMENT",
                    "source_topology": "ordinal_context",
                    "respondent_block": "SECONDARY",
                    "position": 2,
                },
                "canonical_substantive": True,
                "semantic_role": "POSITION_COORDINATE",
                "notes": (
                    "Secondary-respondent 1..10 wealth-ladder position, a distinct repeated "
                    "measurement from PRq315; same household row, distinct occurrence key."
                ),
            },
            {
                "var": "country",
                "question_id": None,
                "role": "coordinate",
                "coordinate_kind": "SOURCE_COUNTRY_STRING",
                "unit_taxonomy": "SOURCE_COUNTRY_STRING_DOMAIN",
                "canonical_substantive": False,
                "notes": (
                    "Source string country coordinate copied only as observed raw; the "
                    "retained metadata does not enumerate the sampled country set."
                ),
            },
        ],
        "fixture": {
            "fixture_id": "R157-LITS-SRC29-NONRESPONDENT",
            "country_values": [
                "NONRESPONDENT_FIXTURE_COUNTRY_A",
                "NONRESPONDENT_FIXTURE_COUNTRY_B",
                "NONRESPONDENT_FIXTURE_COUNTRY_C",
                "NONRESPONDENT_FIXTURE_COUNTRY_D",
                "NONRESPONDENT_FIXTURE_COUNTRY_E",
            ],
            "cells": {
                "PRq306": [1, 2, 3, 1, 2],
                "PRq315": [5, -97, -99, 10, 1],
                "SRq315": [6, -97, -99, 9, 2],
            },
            "shape_coverage": [
                "DTA primary-respondent nominal/context response with exact source categories",
                "DTA primary-respondent 1..10 wealth-ladder repeated measurement with Don't know and Refusal specials",
                "DTA secondary-respondent 1..10 wealth-ladder repeated measurement, distinct occurrence from the primary block",
                "DTA string country coordinate copied raw from explicit fixture-only strings",
            ],
        },
    },
    "SRC30": {
        "family": "LiTS",
        "wave": "IV",
        "artifact": "LiTS_IV.dta",
        "release_id": "LiTS_WAVE_IV",
        "country_slot": "country",
        "country_kind": "NUMERIC_SOURCE_COUNTRY_CODE",
        "country_geography": (
            "MULTI_COUNTRY_LITS_IV__SOURCE_COUNTRY_SLOT_ORDINAL_2__"
            "CODEBOOK_DOMAIN_37_COUNTRIES__SAMPLED_COUNTRY_SET_NOT_ENUMERATED"
        ),
        "sampling_geography": (
            "MULTI_COUNTRY_HOUSEHOLD_SAMPLE__PSU_SLOT_ORDINAL_1315__REGION_SLOT_ORDINAL_60"
        ),
        "target_population": (
            "HOUSEHOLDS_IN_PARTICIPATING_LITS_IV_COUNTRIES__PRIMARY_AND_RANDOM_"
            "RESPONDENT_BLOCKS__FRAME_DETAIL_NOT_RETAINED"
        ),
        "design": (
            "COMPLEX_HOUSEHOLD_SAMPLE__WEIGHT_WEIGHT_POP_WEIGHT_TRT_WEIGHT_POP_TRT_"
            "SLOTS_PRESENT__DESIGN_AUTHORITY_NOT_RETAINED"
        ),
        "subject_unit": "HOUSEHOLD",
        "unit_notes": (
            "Rows are household interviews; q1031/q1032 are positional household-roster "
            "gender items for members 1 and 2, kept as distinct repeated occurrences. "
            "The sections-order and knowledgeable/random respondent codes are retained as "
            "administration evidence but no exact form default is asserted."
        ),
        "form_slice": (
            "LiTS_IV_SINGLE_INSTRUMENT__SECTIONS_ORDER_AND_RANDOM_RESPONDENT_INDICATORS_PRESENT__"
            "EXACT_FORM_ASSIGNMENT_NOT_RETAINED"
        ),
        "targets": [
            {
                "var": "q403g",
                "question_id": "SRC30_Q403G_TRUST_POLITICAL_PARTIES",
                "role": "response",
                "topology_kind": "scalar",
                "occurrence_key": "source_scalar",
                "occurrence_fields": {
                    "kind": "scalar",
                    "source_topology": "scalar",
                    "position": 1,
                },
                "canonical_substantive": True,
                "semantic_role": "RELATION_EVIDENCE",
                "notes": (
                    "Source-native institutional trust scale with Don't know and Not "
                    "applicable specials; source code preserved, no default."
                ),
            },
            {
                "var": "q1031",
                "question_id": "SRC30_Q1031_HH_MEMBER_1_GENDER",
                "role": "repeated_response",
                "topology_kind": "REPEATED_EVENT",
                "occurrence_key": "household_member_position_1_gender",
                "occurrence_fields": {
                    "kind": "REPEATED_EVENT",
                    "source_topology": "nominal_choice",
                    "repeat_axis": "household_roster",
                    "member_position": 1,
                    "source_slot": "q1031",
                },
                "canonical_substantive": True,
                "semantic_role": "POSITION_COORDINATE",
                "notes": (
                    "Position-1 household-roster gender; Don't know and Refused specials "
                    "are source-declared and preserved."
                ),
            },
            {
                "var": "q1032",
                "question_id": "SRC30_Q1032_HH_MEMBER_2_GENDER",
                "role": "repeated_response",
                "topology_kind": "REPEATED_EVENT",
                "occurrence_key": "household_member_position_2_gender",
                "occurrence_fields": {
                    "kind": "REPEATED_EVENT",
                    "source_topology": "nominal_choice",
                    "repeat_axis": "household_roster",
                    "member_position": 2,
                    "source_slot": "q1032",
                },
                "canonical_substantive": True,
                "semantic_role": "POSITION_COORDINATE",
                "notes": (
                    "Position-2 household-roster gender, distinct from q1031; no collapse "
                    "to one roster scalar."
                ),
            },
            {
                "var": "country",
                "question_id": None,
                "role": "coordinate",
                "coordinate_kind": "SOURCE_COUNTRY_CODE",
                "unit_taxonomy": "SOURCE_COUNTRY_CODE_DOMAIN",
                "canonical_substantive": False,
                "notes": (
                    "Source country coordinate copied raw; 37-label codebook domain is "
                    "not a sampled-country claim."
                ),
            },
        ],
        "fixture": {
            "fixture_id": "R157-LITS-SRC30-NONRESPONDENT",
            "country_values": [1, 2, 3, 4, 5],
            "cells": {
                "q403g": [4, -97, -98, 5, None],
                "q1031": [1, 2, -97, -99, None],
                "q1032": [2, 1, -99, -97, None],
            },
            "shape_coverage": [
                "DTA scalar trust item with substantive, Don't know, Not applicable and system-missing cells",
                "DTA household-roster gender position 1 with substantive, Don't know, Refused and system-missing cells",
                "DTA household-roster gender position 2, distinct repeated occurrence from position 1",
                "source numeric country coordinate copied raw; fixture codes are nonrespondent fixture values",
            ],
        },
    },
}


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _file_ref(kind: str, path: str, sha256: str) -> dict[str, Any]:
    return {"kind": kind, "object_id": f"urn:rawlsing:r157:evidence:{path}", "content_hash": sha256}


def _exact_ref(kind: str, object_id: str, material: Any) -> dict[str, Any]:
    return {"kind": kind, "object_id": object_id, "content_hash": semantic_hash(material)}


def _authority_ref(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "authority_id": snapshot["authority_id"],
        "authority_version": snapshot["authority_version"],
        "authority_content_hash": snapshot["authority_content_hash"],
    }


def _authority_snapshot(
    *,
    source_id: str,
    tag: str,
    authority_kind: str,
    state: str,
    families: Sequence[str],
    operations: Sequence[str],
    scope: Mapping[str, Any],
    effective_time: str,
    fixture: bool,
) -> dict[str, Any]:
    identity_material = {
        "source_id": source_id,
        "tag": tag,
        "authority_kind": authority_kind,
        "state": state,
        "scope": scope,
    }
    content_hash = semantic_hash(identity_material)
    replay_ref = _exact_ref(
        "REPLAY_PROTOCOL",
        f"urn:rawlsing:r157:authority:replay:{source_id}:{tag}",
        {"source_id": source_id, "tag": tag, "kind": "R157_SOURCE_CONFIGURATION_REPLAY"},
    )
    return {
        "typed_state": state,
        "authority_snapshot_refs": [],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": _exact_ref(
            "REPLAY_ROOT",
            f"urn:rawlsing:r157:authority:root:{source_id}:{tag}",
            {"source_id": source_id, "tag": tag},
        ),
        "authority_id": f"R157_{'FIXTURE' if fixture else 'PREP'}_{tag}_{source_id}",
        "authority_version": "1.0.0",
        "authority_content_hash": content_hash,
        "authority_kind": authority_kind,
        "decision_state": state,
        "governed_operations": list(operations),
        "governed_object_families": list(families),
        "scope_envelope": dict(scope),
        "effective_time_or_interval": effective_time,
        "parent_authority_refs": [],
        "negative_limit_refs": [],
        "supersession_refs": [],
        "interpretation_semantics_fingerprint": semantic_hash(
            {"source_id": source_id, "tag": tag, "scope": scope}
        ),
        "replay_protocol_ref": replay_ref,
    }


def _authority_set(
    *,
    source_id: str,
    source_sha: str,
    original_source_sha: str,
    wave: str,
    fixture: bool,
    fixture_id: str | None,
    fixture_sha: str | None,
    selected_vars: Sequence[str],
) -> dict[str, Any]:
    if fixture:
        base_scope = {
            "fixture_only": True,
            "grade": "NONRESPONDENT_FIXTURE_ONLY",
            "fixture_id": fixture_id,
            "source_id": source_id,
            "source_sha256": original_source_sha,
            "original_source_sha256": original_source_sha,
            "fixture_source_sha256": fixture_sha,
            "wave": wave,
            "selected_variables": list(selected_vars),
            "execution_authority": "NONRESPONDENT_FIXTURE_VALIDATION_ONLY",
        }
        state = "ALLOW"
        prefix = "FIXTURE"
        effective = "R157_NONRESPONDENT_FIXTURE"
    else:
        base_scope = {
            "grade": "SOURCE_REVIEWED_SOURCE_LOCAL_EVIDENCE__PREPARATION_ONLY",
            "source_id": source_id,
            "source_sha256": source_sha,
            "original_source_sha256": source_sha,
            "wave": wave,
            "selected_variables": list(selected_vars),
            "execution_authority": "NOT_GRANTED_UNDER_R157",
            "r157_use": "PORTABLE_CONFIGURATION_AND_NATIVE_RECIPE_ONLY",
        }
        state = "DEFER"
        prefix = "PREP"
        effective = wave

    def snap(tag, kind, families, ops, extra=None):
        scope = dict(base_scope)
        if extra:
            scope.update(extra)
        return _authority_snapshot(
            source_id=source_id,
            tag=tag,
            authority_kind=kind,
            state=state,
            families=families,
            operations=ops,
            scope=scope,
            effective_time=effective,
            fixture=fixture,
        )

    snapshots = [
        snap(
            "PROJECTION",
            "SOURCE_SEMANTICS_TOPOLOGY",
            [FAMILIES["universe"], FAMILIES["event"], FAMILIES["coordinate"], FAMILIES["routing"]],
            [f"R157_{prefix}_OP_{source_id}_PROJECTION"],
            {"projection_scope": "SOURCE_BACKED_C11_PROJECTION"},
        ),
        snap(
            "SEMANTIC",
            "SOURCE_SEMANTICS_TOPOLOGY",
            [FAMILIES["event"], FAMILIES["universe"]],
            [f"R157_{prefix}_OP_{source_id}_SEMANTIC"],
            {"semantic_scope": "QUESTION_VARIABLE_BINDING_AND_RESPONSE_EVENT"},
        ),
        snap(
            "MAPPING",
            "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
            [FAMILIES["event"]],
            [f"R157_{prefix}_OP_{source_id}_MAPPING"],
            {"mapping_scope": "IDENTITY_SOURCE_CODE_MAPPING__NO_LINEAR_NORMALIZATION"},
        ),
        snap(
            "TOPOLOGY",
            "SOURCE_SEMANTICS_TOPOLOGY",
            [FAMILIES["event"]],
            [f"R157_{prefix}_OP_{source_id}_TOPOLOGY"],
            {"topology_scope": "SCALAR_AND_REPEATED_OCCURRENCE_TOPOLOGY"},
        ),
        snap(
            "COORDINATE",
            "COORDINATE_SEMANTICS",
            [FAMILIES["coordinate"]],
            [f"R157_{prefix}_OP_{source_id}_COORDINATE"],
            {"coordinate_scope": "SOURCE_COUNTRY_COORDINATE_RAW_COPY"},
        ),
        snap(
            "ROUTING",
            "ROUTING_RISK_SET",
            [FAMILIES["routing"]],
            [f"R157_{prefix}_OP_{source_id}_ROUTING"],
            {"routing_scope": "SOURCE_PROVEN_UNCONDITIONAL_TARGETS_ONLY"},
        ),
        snap(
            "REPLAY",
            "REPLAY_PROTOCOL",
            [FAMILIES["replay"]],
            [f"R157_{prefix}_OP_{source_id}_REPLAY"],
            {"replay_scope": "R157_DETERMINISTIC_CONFIGURATION_REPLAY"},
        ),
    ]
    by_tag = {snapshot["authority_id"].split("_")[2]: snapshot for snapshot in snapshots}
    # Robust tag recovery independent of source-id underscores.
    by_tag = {}
    for snapshot in snapshots:
        for tag in ("PROJECTION", "SEMANTIC", "MAPPING", "TOPOLOGY", "COORDINATE", "ROUTING", "REPLAY"):
            if f"_{tag}_" in snapshot["authority_id"]:
                by_tag[tag] = snapshot
                break
    required = [_authority_ref(snapshot) for snapshot in snapshots]
    return {
        "snapshots": snapshots,
        "by_tag": by_tag,
        "required_refs": required,
        "projection_authority_ref": _authority_ref(by_tag["PROJECTION"]),
        "replay_authority_ref": _authority_ref(by_tag["REPLAY"]),
    }


def _classify_label(label: str) -> str:
    text = (label or "").strip().lower()
    if any(token in text for token in ("refusal", "refused")):
        return "REFUSAL"
    if any(token in text for token in ("don't know", "dont know", "difficult to say")):
        return "DK"
    if any(token in text for token in ("not applicable", "filtered", "inapplicable")):
        return "INAPPLICABLE"
    if any(token in text for token in ("not stated", "missing", "no answer")):
        return "MISSING"
    return "SUBSTANTIVE_RESPONSE"


def _raw_code(code: str, readstat_type: str) -> int | float:
    if readstat_type.startswith("int"):
        return int(code)
    return float(code)


def _canonical_code(code: str, readstat_type: str) -> str:
    if readstat_type.startswith("int"):
        return str(int(code))
    value = float(code)
    if value.is_integer():
        return str(int(value))
    return repr(value)


def _ordered_codes(slot: Mapping[str, Any]) -> list[tuple[int | float, str, str]]:
    labels = slot.get("value_labels") or {}
    readstat_type = slot.get("readstat_type") or "float"
    result = []
    for code, label in labels.items():
        raw = _raw_code(str(code), readstat_type)
        result.append((raw, str(label), _canonical_code(str(code), readstat_type)))
    result.sort(key=lambda item: float(item[0]))
    return result


def _value_rule(
    *,
    raw_value: Any,
    missing_state: str,
    response_state: str,
    canonical_value: str | None,
    occurrence: Mapping[str, Any],
    mapping_ref: Mapping[str, Any] | None,
    source_missing_declaration: Any = None,
) -> dict[str, Any]:
    return {
        "raw_value": raw_value,
        "missing_state": missing_state,
        "source_missing_declaration": source_missing_declaration,
        "canonical_value": canonical_value,
        "transform_authority_ref": mapping_ref if canonical_value is not None else None,
        "response_state": response_state,
        "occurrences": [dict(occurrence)],
    }


def _occurrence(
    *,
    source_id: str,
    target: Mapping[str, Any],
) -> dict[str, Any]:
    var = target["var"]
    topology_kind = target["topology_kind"]
    if topology_kind == "scalar":
        topology_ref = _exact_ref(
            "RESPONSE_TOPOLOGY",
            f"urn:rawlsing:r157:{source_id}:topology:scalar:{var}",
            {"source_id": source_id, "var": var, "kind": "scalar"},
        )
    elif topology_kind == "binary_contrast":
        topology_ref = _exact_ref(
            "RESPONSE_TOPOLOGY",
            f"urn:rawlsing:r157:{source_id}:topology:binary_contrast:{var}",
            {"source_id": source_id, "var": var, "kind": "binary_contrast"},
        )
    elif topology_kind == "ordinal_context":
        topology_ref = _exact_ref(
            "RESPONSE_TOPOLOGY",
            f"urn:rawlsing:r157:{source_id}:topology:ordinal_context:{var}",
            {"source_id": source_id, "var": var, "kind": "ordinal_context"},
        )
    else:
        topology_ref = _exact_ref(
            "RESPONSE_TOPOLOGY",
            f"urn:rawlsing:r157:{source_id}:topology:{topology_kind}:{var}",
            {"source_id": source_id, "var": var, "kind": topology_kind},
        )
    return {
        "key": target["occurrence_key"],
        "topology_ref": topology_ref,
        "multiplicity_order_rank_fields": dict(target["occurrence_fields"]),
    }


def _reader_ref(source_id: str) -> dict[str, Any]:
    return _exact_ref(
        "READER_CONFIGURATION",
        f"urn:rawlsing:r157:reader:{source_id}:readstat_dta_default",
        {
            "source_id": source_id,
            "decoder_owner": READER_DECODER,
            "encoding_override": None,
            "encoding_authority": "COMPATIBILITY_ONLY_UNLESS_EXACT_ALLOWLIST_OVERRIDE_REQUIRED",
        },
    )


def _selected_targets(recipe: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [target for target in recipe["targets"] if target["role"] != "coordinate"]


def _included_slots(recipe: Mapping[str, Any]) -> set[str]:
    return {target["var"] for target in recipe["targets"]}


def _universe_payload(
    *,
    source_id: str,
    recipe: Mapping[str, Any],
    roster: Mapping[str, Any],
    authority: Mapping[str, Any],
    fixture: bool,
    fixture_sha: str | None,
) -> tuple[dict[str, Any], Any]:
    metadata = roster["metadata_witness"]
    if fixture:
        country_geography = "NONRESPONDENT_FIXTURE__DECLARED_COUNTRY_CELLS_ONLY__NOT_ORIGINAL_SAMPLE"
        sampling_geography = "NONRESPONDENT_FIXTURE__SYNTHETIC_ROW_POSITIONS"
        target_population = "NONRESPONDENT_FIXTURE__NO_POPULATION_FRAME"
        design = "NONRESPONDENT_FIXTURE__NO_DESIGN"
        raw_identity = f"NONRESPONDENT_FIXTURE {recipe['fixture']['fixture_id']} sha256={fixture_sha}"
        study_release = f"R157 NONRESPONDENT FIXTURE for LiTS {recipe['wave']} ({recipe['artifact']})"
        namespace = f"R157_FIXTURE/{source_id}"
    else:
        country_geography = recipe["country_geography"]
        sampling_geography = recipe["sampling_geography"]
        target_population = recipe["target_population"]
        design = recipe["design"]
        raw_identity = (
            f"{recipe['artifact']} sha256={roster['source_sha256']} "
            f"rows={roster['rows']} cols={roster['physical_columns']}"
        )
        study_release = f"LiTS {recipe['wave']} ({recipe['artifact']})"
        namespace = f"LiTS/{recipe['wave']}/household"
    metadata_ref = {
        "kind": "R154_PHYSICAL_METADATA",
        "object_id": f"urn:rawlsing:r157:metadata:{metadata['path']}",
        "content_hash": metadata["sha256"],
    }
    universe_payload = {
        "typed_state": "UNIVERSE_IDENTIFIED",
        "authority_snapshot_refs": [
            _authority_ref(authority["by_tag"]["PROJECTION"]),
            _authority_ref(authority["by_tag"]["SEMANTIC"]),
        ],
        "dependency_refs": [metadata_ref],
        "producer_replay_locator_or_reference_root": _exact_ref(
            "UNIVERSE_REPLAY_ROOT",
            f"urn:rawlsing:r157:universe:{source_id}:{'fixture' if fixture else 'source'}",
            {"source_id": source_id, "fixture": fixture, "wave": recipe["wave"]},
        ),
        "raw_source_identity": raw_identity,
        "source_family": recipe["family"],
        "study_product_release": study_release,
        "instrument_release": f"{source_id}_METADATA_WITNESS_SHA256:{metadata['sha256']}",
        "country_geography": country_geography,
        "sampling_geography": sampling_geography,
        "raw_wave": recipe["wave"],
        "canonical_wave_if_governed": recipe["wave"],
        "field_or_reference_time": recipe["wave"],
        "target_population_and_sample_frame": target_population,
        "sampling_design_regime": design,
        "respondent_namespace": namespace,
        "source_artifact_import_lineage": (
            f"R154_PHYSICAL_METADATA_SHA256:{metadata['sha256']};"
            "R48_H48_ITEM_INDEX;P2_PHASE0;FULL_RELATION_AUTHORITY;"
            f"R157_PORTABLE_EVIDENCE_SHA256:{MANIFEST_FILES['ITEM_EVIDENCE.jsonl.gz']['sha256']}"
        ),
        "harmonization_authority_ref": _authority_ref(authority["by_tag"]["MAPPING"]),
        "source_relation_refs": [],
    }
    universe = EmpiricalUniverse(**universe_payload)
    return universe_payload, universe


def _question_payload(
    *,
    source_id: str,
    recipe: Mapping[str, Any],
    target: Mapping[str, Any],
    roster: Mapping[str, Any],
    item: Mapping[str, Any],
    slot: Mapping[str, Any],
    universe: Any,
    authority: Mapping[str, Any],
    fixture: bool,
) -> dict[str, Any]:
    impl_id = item["implementation_id"]
    exact_identity = item["exact_identity_sha256"]
    relation = item.get("relation") or {}
    routing = _routing_status(item)
    return {
        "question_id": target["question_id"],
        "empirical_universe_ref": universe.ref.as_dict(),
        "native_question_ref": _exact_ref(
            "SOURCE_QUESTION",
            f"urn:rawlsing:r157:{source_id}:question:{target['var']}",
            {
                "source_id": source_id,
                "var": target["var"],
                "implementation_id": impl_id,
                "exact_identity_sha256": exact_identity,
            },
        ),
        "instrument_question_version": (
            f"{recipe['artifact']}::{target['var']}::P2:{exact_identity}"
        ),
        "canonical_question_ref_or_typed_absence": {
            "typed_absence_state": "UNKNOWN",
            "detail": (
                "No cross-source canonical question identity is adopted by this source "
                "slice; the P2/relation identity is retained as source-local evidence."
            ),
        },
        "component_subitem_ref_or_typed_absence": {
            "typed_absence_state": "NOT_APPLICABLE",
            "detail": (
                "Scalar physical slot with its own source-native question identity; no "
                "component/subitem collapse is asserted."
            ),
        },
        "semantic_authority_ref": _authority_ref(authority["by_tag"]["SEMANTIC"]),
        "topology_authority_ref": _authority_ref(authority["by_tag"]["TOPOLOGY"]),
        "item_evidence": {
            "implementation_id": impl_id,
            "source_variable_code": target["var"],
            "exact_identity_sha256": exact_identity,
            "physical_ordinal": slot["ordinal"],
            "physical_name": slot["name"],
            "p2_question_id": (item.get("p2") or {}).get("question_id"),
            "p2_canonical_disposition": (item.get("p2") or {}).get("canonical_disposition"),
            "p2_response_binding_status": (item.get("p2") or {}).get("response_binding_status"),
            "relation_authority_status": relation.get("authority_status_final_or_current"),
            "relation_mapping_status": relation.get("mapping_status"),
            "manual_response_topology": relation.get("manual_response_topology"),
            "manual_signed_polarity_status": relation.get("manual_signed_polarity_status"),
            "routing_status": routing,
            "governed_row_payload_hash": relation.get("governed_row_payload_hash"),
            "p2_exact_identity_sha256": relation.get("p2_exact_identity_sha256"),
            "fixture_identity_class": "NONRESPONDENT_FIXTURE" if fixture else "ORIGINAL_SOURCE",
        },
    }


def _routing_status(item: Mapping[str, Any]) -> str:
    for binding in (item.get("h48") or {}).get("candidate_bindings", ()):
        if binding.get("family") == "O06_IMPLEMENTATION_ROUTING_CENTRAL.jsonl":
            return ((binding.get("status") or {}).get("routing_status")) or "NOT_STATED"
    return "NOT_STATED"


def _response_values_for_original(
    *,
    slot: Mapping[str, Any],
    target: Mapping[str, Any],
    authority: Mapping[str, Any],
    occurrence: Mapping[str, Any],
) -> list[dict[str, Any]]:
    mapping_ref = _authority_ref(authority["by_tag"]["MAPPING"])
    values = []
    for raw, label, canonical in _ordered_codes(slot):
        state = _classify_label(label)
        values.append(
            _value_rule(
                raw_value=raw,
                missing_state="OBSERVED_STORAGE_VALUE",
                response_state=state,
                canonical_value=canonical if state == "SUBSTANTIVE_RESPONSE" and target["canonical_substantive"] else None,
                occurrence=occurrence,
                mapping_ref=mapping_ref,
            )
        )
    values.append(
        _value_rule(
            raw_value=None,
            missing_state="SYSTEM_MISSING",
            response_state="MISSING",
            canonical_value=None,
            occurrence=occurrence,
            mapping_ref=None,
        )
    )
    return values


def _response_values_for_fixture(
    *,
    slot: Mapping[str, Any],
    target: Mapping[str, Any],
    authority: Mapping[str, Any],
    occurrence: Mapping[str, Any],
    fixture_values: Sequence[Any],
) -> list[dict[str, Any]]:
    mapping_ref = _authority_ref(authority["by_tag"]["MAPPING"])
    labels = slot.get("value_labels") or {}
    by_raw: dict[Any, tuple[str, str]] = {}
    for raw, label, canonical in _ordered_codes(slot):
        by_raw[raw] = (label, canonical)
    seen: set[Any] = set()
    values = []
    for raw in fixture_values:
        if raw in seen:
            continue
        seen.add(raw)
        if raw is None:
            values.append(
                _value_rule(
                    raw_value=None,
                    missing_state="SYSTEM_MISSING",
                    response_state="MISSING",
                    canonical_value=None,
                    occurrence=occurrence,
                    mapping_ref=None,
                )
            )
            continue
        if raw not in by_raw:
            raise ValueError(
                f"{target['var']}: fixture value {raw!r} is not a declared source code"
            )
        label, canonical = by_raw[raw]
        state = _classify_label(label)
        values.append(
            _value_rule(
                raw_value=raw,
                missing_state="OBSERVED_STORAGE_VALUE",
                response_state=state,
                canonical_value=canonical if state == "SUBSTANTIVE_RESPONSE" and target["canonical_substantive"] else None,
                occurrence=occurrence,
                mapping_ref=mapping_ref,
            )
        )
    return values


def _coordinate_slot(
    *,
    source_id: str,
    recipe: Mapping[str, Any],
    slot: Mapping[str, Any],
    authority: Mapping[str, Any],
    fixture: bool,
) -> dict[str, Any]:
    return {
        "slot": {"ordinal": slot["ordinal"], "name": slot["name"]},
        "native_coordinate_ref": _exact_ref(
            "SOURCE_COORDINATE",
            f"urn:rawlsing:r157:{source_id}:coordinate:{slot['name']}",
            {
                "source_id": source_id,
                "slot": slot["name"],
                "kind": recipe["country_kind"],
                "fixture": fixture,
            },
        ),
        "unit_taxonomy_ref": _exact_ref(
            "COORDINATE_UNIT_TAXONOMY",
            f"urn:rawlsing:r157:{source_id}:coordinate-unit:{slot['name']}",
            {"source_id": source_id, "unit": recipe["country_kind"]},
        ),
        "effective_time": recipe["wave"],
        "source_semantic_authority_ref": _authority_ref(authority["by_tag"]["COORDINATE"]),
        "canonical_coordinate_ref": None,
        "normalization_ref": {
            "typed_absence_state": "NOT_APPLICABLE",
            "detail": (
                "No country crosswalk, default country, or canonical geography is asserted; "
                "the raw source coordinate is copied only when observed."
            ),
        },
        "values": [],
        "copy_observed_raw": True,
    }


def _routing_rules(
    *,
    source_id: str,
    targets: Sequence[Mapping[str, Any]],
    authority: Mapping[str, Any],
    fixture: bool,
) -> list[dict[str, Any]]:
    rules = []
    for target in targets:
        var = target["var"]
        rules.append(
            {
                "question_id": target["question_id"],
                "row_selector": "ALL",
                "typed_state": "ELIGIBLE_APPLICABLE",
                "risk_set_ref": _exact_ref(
                    "RISK_SET",
                    f"urn:rawlsing:r157:{source_id}:risk-set:{var}",
                    {"source_id": source_id, "var": var, "scope": "unconditional_source_proven"},
                ),
                "routing_rule_ref": _exact_ref(
                    "ROUTING_RULE",
                    f"urn:rawlsing:r157:{source_id}:routing-rule:{var}",
                    {"source_id": source_id, "var": var, "routing_status": "UNCONDITIONAL_SOURCE_PROVEN"},
                ),
                "member_set_replay_ref": _exact_ref(
                    "MEMBER_SET_REPLAY",
                    f"urn:rawlsing:r157:{source_id}:member-set:{var}:{'fixture' if fixture else 'source'}",
                    {"source_id": source_id, "var": var, "fixture": fixture},
                ),
                "authority_ref": _authority_ref(authority["by_tag"]["ROUTING"]),
                "replay_root": _exact_ref(
                    "ROUTING_REPLAY_ROOT",
                    f"urn:rawlsing:r157:{source_id}:routing-replay:{var}:{'fixture' if fixture else 'source'}",
                    {"source_id": source_id, "var": var, "fixture": fixture},
                ),
            }
        )
    return rules


def _physical_slot_payload(
    *,
    slot: Mapping[str, Any],
    item: Mapping[str, Any],
    included: bool,
    target: Mapping[str, Any] | None,
) -> dict[str, Any]:
    if included and target is not None:
        if target["role"] == "coordinate":
            disposition = "INCLUDED_COORDINATE_SLOT"
        elif target["role"] == "repeated_response":
            disposition = "INCLUDED_REPEATED_RESPONSE_SLOT"
        else:
            disposition = "INCLUDED_RESPONSE_SLOT"
        disposition_reason = None
    else:
        p2_disp = (item.get("p2") or {}).get("canonical_disposition") or "UNCLASSIFIED"
        disposition = {
            "ADMINISTRATIVE_METADATA": "EXCLUDED_ADMINISTRATIVE_ACCOUNTED",
            "STRUCTURAL_CONTEXT": "EXCLUDED_STRUCTURAL_CONTEXT_ACCOUNTED",
            "POSITION_COORDINATE": "EXCLUDED_POSITION_COORDINATE_ACCOUNTED",
            "RELATION_EVIDENCE": "EXCLUDED_RELATION_EVIDENCE_ACCOUNTED",
        }.get(p2_disp, "EXCLUDED_INVENTORY_ACCOUNTED")
        disposition_reason = (
            f"Not in declared native slice; exact {p2_disp} item and physical slot are "
            "inventory-accounted with codebook/P2/H48/relation evidence retained."
        )
    payload = {
        "ordinal": slot["ordinal"],
        "name": slot["name"],
        "label": slot.get("label"),
        "storage_type": slot.get("readstat_type"),
        "original_type": slot.get("original_type"),
        "storage_width": slot.get("storage_width"),
        "measure": slot.get("measure"),
        "value_labels": slot.get("value_labels"),
        "missing_declarations": {
            "missing_ranges": slot.get("missing_ranges"),
            "missing_user_values": slot.get("missing_user_values"),
        },
        "mr_declarations": None,
        "codebook_mapping": {
            "var_name": slot["name"],
            "row_hash": (slot.get("codebook_mapping") or {}).get("row_hash"),
            "status": (slot.get("codebook_mapping") or {}).get("status", "UNKNOWN"),
        },
        "disposition": disposition,
    }
    if disposition_reason is not None:
        payload["disposition_reason"] = disposition_reason
    return payload


def _item_payload(
    *,
    slot: Mapping[str, Any],
    item: Mapping[str, Any],
    codebook: Mapping[str, Any],
    included: bool,
    target: Mapping[str, Any] | None,
    source_id: str,
    metadata_sha: str,
) -> dict[str, Any]:
    relation = item.get("relation") or {}
    p2 = item.get("p2") or {}
    routing = _routing_status(item)
    if included and target is not None:
        if target["role"] == "coordinate":
            disposition = "INCLUDED_COORDINATE_SLOT"
        elif target["role"] == "repeated_response":
            disposition = "INCLUDED_REPEATED_RESPONSE_SLOT"
        else:
            disposition = "INCLUDED_RESPONSE_SLOT"
    else:
        p2_disp = p2.get("canonical_disposition") or "UNCLASSIFIED"
        disposition = {
            "ADMINISTRATIVE_METADATA": "EXCLUDED_ADMINISTRATIVE_ACCOUNTED",
            "STRUCTURAL_CONTEXT": "EXCLUDED_STRUCTURAL_CONTEXT_ACCOUNTED",
            "POSITION_COORDINATE": "EXCLUDED_POSITION_COORDINATE_ACCOUNTED",
            "RELATION_EVIDENCE": "EXCLUDED_RELATION_EVIDENCE_ACCOUNTED",
        }.get(p2_disp, "EXCLUDED_INVENTORY_ACCOUNTED")
    evidence_refs = _item_evidence_refs(
        source_id=source_id,
        slot=slot,
        item=item,
        codebook=codebook,
        metadata_sha=metadata_sha,
    )
    limits = _item_limits(item)
    payload = {
        "implementation_id": item["implementation_id"],
        "source_variable_code": item["source_variable_code"],
        "exact_identity_sha256": item["exact_identity_sha256"],
        "question_text": _nonempty_text(
            p2.get("question_text") or codebook.get("question_text") or slot.get("label") or slot["name"]
        ),
        "disposition": disposition,
        "response_classes": _nonempty_text(p2.get("response_classes") or "NOT_DECLARED"),
        "mapping_status": _nonempty_text(relation.get("mapping_status") or p2.get("canonical_disposition") or "NOT_MAPPED"),
        "authority_status": _nonempty_text(
            relation.get("authority_status_final_or_current") or p2.get("authority_status") or "NOT_STATED"
        ),
        "evidence_refs": evidence_refs,
        "limits": limits,
    }
    if included and target is not None:
        payload["relation"] = {
            "status": _nonempty_text(
                relation.get("authority_status_final_or_current")
                or relation.get("relation_use_status_final")
                or "NOT_STATED"
            ),
            "question_id": _nonempty_text(relation.get("question_id") or target["question_id"]),
            "mapping_status": _nonempty_text(relation.get("mapping_status") or "NOT_MAPPED"),
            "manual_response_topology": _nonempty_text(
                relation.get("manual_response_topology") or "NOT_STATED"
            ),
            "manual_response_normalization_rule": _nonempty_text(
                relation.get("manual_response_normalization_rule") or "NOT_STATED"
            ),
            "manual_position_conditioning": _nonempty_text(
                relation.get("manual_position_conditioning") or "NOT_STATED"
            ),
            "manual_semantic_role": _nonempty_text(
                relation.get("manual_semantic_role") or p2.get("canonical_disposition") or "NOT_STATED"
            ),
            "manual_signed_polarity_status": _nonempty_text(
                relation.get("manual_signed_polarity_status") or "NOT_STATED"
            ),
            "forbidden_inference": _nonempty_text(
                relation.get("forbidden_inference") or "NONE_STATED__EMPTY_IN_RELATION_ROW"
            ),
            "does_not_measure": _nonempty_text(
                relation.get("does_not_measure") or "NONE_STATED__EMPTY_IN_RELATION_ROW"
            ),
            "governed_row_payload_hash": relation.get("governed_row_payload_hash"),
            "p2_exact_identity_sha256": relation.get("p2_exact_identity_sha256"),
        }
    return payload


def _nonempty_text(value: Any) -> str:
    text = str(value).strip() if value is not None else ""
    return text if text else "NOT_STATED"


def _item_evidence_refs(
    *,
    source_id: str,
    slot: Mapping[str, Any],
    item: Mapping[str, Any],
    codebook: Mapping[str, Any],
    metadata_sha: str,
) -> list[dict[str, Any]]:
    relation = item.get("relation") or {}
    refs = [
        {
            "kind": "H48_ITEM_AUTHORITY_CANDIDATE",
            "object_id": f"urn:rawlsing:r48:item:{item['implementation_id']}",
            "content_hash": item["exact_identity_sha256"],
        },
        {
            "kind": "P2_IMPLEMENTATION_IDENTITY",
            "object_id": f"urn:rawlsing:p2:{item['implementation_id']}",
            "content_hash": item["exact_identity_sha256"],
        },
        {
            "kind": "FULL_QUESTION_RELATION_AUTHORITY",
            "object_id": f"urn:rawlsing:qra35:{relation.get('authority_rule_id') or item['implementation_id']}",
            "content_hash": relation.get("governed_row_payload_hash")
            or relation.get("p2_exact_identity_sha256")
            or item["exact_identity_sha256"],
        },
        {
            "kind": "CODEBOOK_ROW",
            "object_id": f"urn:rawlsing:r154:codebook:{source_id}:{slot['name']}",
            "content_hash": codebook.get("row_hash") or item["exact_identity_sha256"],
        },
        {
            "kind": "R154_PHYSICAL_METADATA",
            "object_id": f"urn:rawlsing:r157:metadata:{source_id}:{slot['name']}",
            "content_hash": metadata_sha,
        },
    ]
    routing = _routing_status(item)
    if routing != "NOT_STATED":
        refs.append(
            {
                "kind": "O06_IMPLEMENTATION_ROUTING_CENTRAL",
                "object_id": f"urn:rawlsing:h48:routing:{item['implementation_id']}",
                "content_hash": item["exact_identity_sha256"],
            }
        )
    return refs


def _item_limits(item: Mapping[str, Any]) -> list[str]:
    relation = item.get("relation") or {}
    h48 = item.get("h48") or {}
    p2 = item.get("p2") or {}
    limits = [
        f"P2_CANONICAL_DISPOSITION:{p2.get('canonical_disposition') or 'NOT_STATED'}",
        f"P2_RESPONSE_BINDING_STATUS:{p2.get('response_binding_status') or 'NOT_STATED'}",
        f"H48_BINDING_GRADE:{h48.get('binding_grade') or 'NOT_STATED'}",
        f"RELATION_AUTHORITY_STATUS:{relation.get('authority_status_final_or_current') or 'NOT_STATED'}",
        f"RELATION_MAPPING_STATUS:{relation.get('mapping_status') or 'NOT_STATED'}",
        f"ROUTING_STATUS:{_routing_status(item)}",
        f"DIRECTIONAL_CERTIFICATION:{relation.get('manual_directional_certification_status') or 'NOT_STATED'}",
        f"COUNTRY_CODE_SCOPE:{relation.get('country_code_scope') or 'NOT_ENUMERATED'}",
        f"P2_EXACT_IDENTITY_SHA256:{relation.get('p2_exact_identity_sha256') or item['exact_identity_sha256']}",
        f"GOVERNED_ROW_PAYLOAD_HASH:{relation.get('governed_row_payload_hash') or 'NOT_STATED'}",
    ]
    if relation.get("forbidden_inference"):
        limits.append(f"FORBIDDEN_INFERENCE:{relation['forbidden_inference']}")
    if relation.get("does_not_measure"):
        limits.append(f"DOES_NOT_MEASURE:{relation['does_not_measure']}")
    if relation.get("review_notes"):
        limits.append(f"RELATION_REVIEW_NOTES:{relation['review_notes']}")
    return limits


def _residuals(
    *,
    source_id: str,
    recipe: Mapping[str, Any],
    included_count: int,
    item_count: int,
    slot_count: int,
    conditional_vars: Sequence[str],
    country_enumerated: bool,
) -> list[dict[str, Any]]:
    residuals = []
    if conditional_vars:
        residuals.append(
            {
                "residual_id": f"{source_id}-ROUTING-CONDITIONAL-HELD",
                "scope": f"{source_id}:{'/'.join(conditional_vars)}",
                "field": "routing_expression",
                "status": "HELD",
                "reason": (
                    "H48 routing_status is conditional or unresolved for these items and the "
                    "materialized evidence retains no exact O06 route clause; storage "
                    "missingness alone is not evidence of asked/not-asked."
                ),
                "dependent_operation": "native response-event projection for the held conditional items",
                "unaffected_scope": (
                    f"the declared {included_count}-slot supported slice and all "
                    "inventory-accounted items"
                ),
                "owner": "R157 LITS lane author; H48 route-clause acquisition",
                "next_step": (
                    "Read the exact O06_ROUTING_CLAUSES_NAMESPACED row for each implementation "
                    "ID, or the official source questionnaire routing, then serialize exact "
                    "parent_predicate_refs/row_selector before claiming these items."
                ),
            }
        )
    residuals.append(
        {
            "residual_id": f"{source_id}-WEIGHTS-DESIGN-AUTHORITY",
            "scope": f"{source_id}:weight_slots",
            "field": "weight_basis_design_and_estimand_authority",
            "status": "SCOPED_UNKNOWN",
            "reason": (
                "Source weight slots and labels are present, but the exact design basis, "
                "normalization, population/estimand and authorization for weighted use are "
                "not retained in the materialized evidence."
            ),
            "dependent_operation": "weighted native projection or population claim",
            "unaffected_scope": "declared unweighted raw-sample slice",
            "owner": "R157 LITS lane author; source design documentation acquisition",
            "next_step": (
                "Acquire the exact LiTS design/weight documentation and an authority record, "
                "then declare a separate weighted scope; do not default a weight or population."
            ),
        }
    )
    residuals.append(
        {
            "residual_id": f"{source_id}-ADMINISTRATION-FORM",
            "scope": f"{source_id}:form_and_administration",
            "field": "form_ballot_administration_mapping",
            "status": "SCOPED_UNKNOWN",
            "reason": (
                "Administration indicators and respondent-block variables are present, but "
                "the exact form/ballot assignment or section-order semantics are not retained; "
                "no DEFAULT_FORM or administered=True is asserted."
            ),
            "dependent_operation": "form-conditioned or administration-stratified native projection",
            "unaffected_scope": recipe["form_slice"],
            "owner": "R157 LITS lane author; source questionnaire/codebook acquisition",
            "next_step": (
                "Recover the exact source form/administration mapping and encode it as an "
                "explicit form slice before using it for conditioning."
            ),
        }
    )
    residuals.append(
        {
            "residual_id": f"{source_id}-NATIVE-ROW-KEY",
            "scope": f"{source_id}:respondents.source_native_key_slot",
            "field": "source_native_respondent_key_witness",
            "status": "HELD",
            "reason": (
                "The source-native key slots are identified in the physical metadata, but no "
                "permitted decoded row witness exists in this preparation grant. The corrected "
                "P0 factory refuses a configured source_native_key_slot without exact row keys."
            ),
            "dependent_operation": "source-native respondent key binding",
            "unaffected_scope": (
                "row-ordinal replay identity, exact physical slot identity, all declared "
                "response/coordinate slots"
            ),
            "owner": "R157 LITS lane author; P3 integration/decode owner",
            "next_step": (
                "After a separately authorized decode, supply exact ExactRef/TypedAbsence "
                "row_native_keys and set source_native_key_slot; never synthesize row IDs."
            ),
        }
    )
    if not country_enumerated:
        residuals.append(
            {
                "residual_id": f"{source_id}-COUNTRY-SET",
                "scope": f"{source_id}:{recipe['country_slot']}",
                "field": "country_geography/sampled_country_set",
                "status": "SCOPED_UNKNOWN",
                "reason": (
                    "The source country slot is present and its raw code/string coordinate can "
                    "be copied, but retained metadata does not enumerate the sampled country "
                    "set or the population frame."
                ),
                "dependent_operation": "country-stratified query, population claim or cross-wave composition",
                "unaffected_scope": "raw country coordinate copy and the declared scalar/repeated slice",
                "owner": "R157 LITS lane author; source frame/country-list acquisition",
                "next_step": (
                    "Recover the exact sampled-country list and frame from the source manual or "
                    "fieldwork documentation; keep the raw coordinate untouched."
                ),
            }
        )
    residuals.append(
        {
            "residual_id": f"{source_id}-READER-ENCODING-TRANSPORT",
            "scope": f"{source_id}:identity.reader.encoding",
            "field": "qualified_reader_encoding_transport",
            "status": "COMPATIBILITY_ONLY",
            "reason": (
                "The roster records decoder_allowlist_encoding=latin1 with authority status "
                "COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY and "
                "required_encoding=null; no encoding override is configured or guessed."
            ),
            "dependent_operation": "any future text-field decode requiring exact encoding",
            "unaffected_scope": "numeric DTA decode and all declared numeric/string-code slot identities",
            "owner": "P3 integration owner; existing source-read/decoder owner",
            "next_step": (
                "Carry the exact-SHA qualified reader configuration through the existing "
                "source-read transport only when the separately authorized read requires it."
            ),
        }
    )
    residuals.append(
        {
            "residual_id": f"{source_id}-SLICE-OUTSIDE-DECLARED",
            "scope": f"{source_id}:{item_count} original items / {slot_count} physical slots",
            "field": "native response/coordinate binding",
            "status": "EXCLUDED_ACCOUNTED",
            "reason": (
                f"The declared native slice covers {included_count} physical slots. Every "
                "remaining original item and physical slot is serialized with exact "
                "codebook/P2/H48/relation identity and an explicit excluded disposition; no "
                "slot, item or administrative/context field is dropped, and no generic "
                "semantics-pending gate is asserted."
            ),
            "dependent_operation": "native event/coordinate projection for items outside the declared slice",
            "unaffected_scope": "the declared supported slice and all inventory accounting",
            "owner": "R157 LITS lane author",
            "next_step": (
                "When a further item is needed, declare a new per-item supported slice with its "
                "own evidence-backed value, missing-state, topology and routing rules."
            ),
        }
    )
    return residuals


def _item_accounting_row(
    *,
    source_id: str,
    slot: Mapping[str, Any],
    item: Mapping[str, Any],
    codebook: Mapping[str, Any],
    selected: bool,
    target: Mapping[str, Any] | None,
) -> dict[str, Any]:
    relation = item.get("relation") or {}
    h48 = item.get("h48") or {}
    p2 = item.get("p2") or {}
    return {
        "source_id": source_id,
        "physical_ordinal": slot["ordinal"],
        "physical_name": slot["name"],
        "physical_label": slot.get("label"),
        "storage_type": slot.get("readstat_type"),
        "original_type": slot.get("original_type"),
        "storage_width": slot.get("storage_width"),
        "measure": slot.get("measure"),
        "value_labels": slot.get("value_labels"),
        "missing_ranges": slot.get("missing_ranges"),
        "missing_user_values": slot.get("missing_user_values"),
        "codebook_row_hash": codebook.get("row_hash"),
        "codebook_question_text": codebook.get("question_text"),
        "codebook_response_options_all": codebook.get("response_options_all"),
        "implementation_id": item["implementation_id"],
        "exact_identity_sha256": item["exact_identity_sha256"],
        "p2": {
            "question_id": p2.get("question_id"),
            "question_implementation_id": p2.get("question_implementation_id"),
            "canonical_disposition": p2.get("canonical_disposition"),
            "response_binding_status": p2.get("response_binding_status"),
            "response_classes": p2.get("response_classes"),
            "module_guess": p2.get("module_guess"),
            "authority_status": p2.get("authority_status"),
            "question_text": p2.get("question_text"),
        },
        "h48": {
            "binding_grade": h48.get("binding_grade"),
            "disposition": h48.get("disposition"),
            "p2_row": h48.get("p2_row"),
            "p2_evidence_id": h48.get("p2_evidence_id"),
        },
        "relation": {
            "authority_rule_id": relation.get("authority_rule_id"),
            "authority_status_final_or_current": relation.get("authority_status_final_or_current"),
            "relation_use_status_final": relation.get("relation_use_status_final"),
            "question_id": relation.get("question_id"),
            "mapping_status": relation.get("mapping_status"),
            "manual_response_topology": relation.get("manual_response_topology"),
            "manual_response_normalization_rule": relation.get("manual_response_normalization_rule"),
            "manual_position_conditioning": relation.get("manual_position_conditioning"),
            "manual_semantic_role": relation.get("manual_semantic_role"),
            "manual_semantic_subrole": relation.get("manual_semantic_subrole"),
            "manual_signed_polarity_status": relation.get("manual_signed_polarity_status"),
            "manual_directional_certification_status": relation.get("manual_directional_certification_status"),
            "manual_evidence_disposition": relation.get("manual_evidence_disposition"),
            "forbidden_inference": relation.get("forbidden_inference"),
            "does_not_measure": relation.get("does_not_measure"),
            "country_code_scope": relation.get("country_code_scope"),
            "structural_domain_id": relation.get("structural_domain_id"),
            "target_entity_id": relation.get("target_entity_id"),
            "governed_row_payload_hash": relation.get("governed_row_payload_hash"),
            "p2_exact_identity_sha256": relation.get("p2_exact_identity_sha256"),
            "review_notes": relation.get("review_notes"),
        },
        "routing_status": _routing_status(item),
        "selected_native_slice": selected,
        "selected_question_id": target["question_id"] if selected and target else None,
        "selected_role": target["role"] if selected and target else None,
        "evidence_refs": _item_evidence_refs(
            source_id=source_id,
            slot=slot,
            item=item,
            codebook=codebook,
            metadata_sha="",
        ),
        "limits": _item_limits(item),
    }


def _source_data(source_id: str) -> tuple[Mapping[str, Any], list[Mapping[str, Any]], dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]], list[Mapping[str, Any]]]:
    roster = evidence.source_roster_entry(source_id)
    slots = list(evidence.iter_physical_slots(source_id))
    items_raw = list(evidence.iter_item_evidence(source_id))
    codebook = {row["var_name"]: row for row in evidence.iter_codebook_rows(source_id)}
    items = {row["source_variable_code"]: row for row in items_raw}
    if len(slots) != roster["physical_columns"]:
        raise ValueError(f"{source_id}: physical slot count mismatch")
    if len(items) != roster["original_items"]:
        raise ValueError(f"{source_id}: item count mismatch")
    if {slot["name"] for slot in slots} != set(items):
        raise ValueError(f"{source_id}: physical/codebook name sets differ")
    return roster, slots, items, codebook, items_raw


def build_source(source_id: str) -> dict[str, Any]:
    recipe = RECIPES[source_id]
    roster, slots, items, codebook, items_raw = _source_data(source_id)
    selected = {target["var"]: target for target in recipe["targets"]}
    included = _included_slots(recipe)
    if not included.issubset(set(items)):
        raise ValueError(f"{source_id}: selected slot missing from item evidence")
    metadata_sha = roster["metadata_witness"]["sha256"]
    source_sha = roster["source_sha256"]

    # Fixture document and identity first: the fixture config binds its exact hash.
    fixture = _build_fixture_document(source_id, recipe, slots, items, roster)
    fixture_sha = fixture["fixture_source_sha256"]

    original_authority = _authority_set(
        source_id=source_id,
        source_sha=source_sha,
        original_source_sha=source_sha,
        wave=recipe["wave"],
        fixture=False,
        fixture_id=None,
        fixture_sha=None,
        selected_vars=sorted(included),
    )
    fixture_authority = _authority_set(
        source_id=source_id,
        source_sha=fixture_sha,
        original_source_sha=source_sha,
        wave=recipe["wave"],
        fixture=True,
        fixture_id=recipe["fixture"]["fixture_id"],
        fixture_sha=fixture_sha,
        selected_vars=sorted(included),
    )

    original = _build_config(
        source_id=source_id,
        recipe=recipe,
        roster=roster,
        slots=slots,
        items=items,
        codebook=codebook,
        selected=selected,
        included=included,
        authority=original_authority,
        fixture=False,
        fixture_doc=fixture,
        fixture_sha=fixture_sha,
    )
    fixture_config = _build_config(
        source_id=source_id,
        recipe=recipe,
        roster=roster,
        slots=slots,
        items=items,
        codebook=codebook,
        selected=selected,
        included=included,
        authority=fixture_authority,
        fixture=True,
        fixture_doc=fixture,
        fixture_sha=fixture_sha,
    )

    expected = _expected_results(source_id, recipe, original, fixture_config, fixture, fixture_sha)
    accounting = [
        _item_accounting_row(
            source_id=source_id,
            slot=slot,
            item=items[slot["name"]],
            codebook=codebook[slot["name"]],
            selected=slot["name"] in included,
            target=selected.get(slot["name"]),
        )
        for slot in slots
    ]
    correspondence = _correspondence(source_id, roster, slots, items, selected)

    data_dir = DATA_ROOT / source_id
    validation_dir = VALIDATION_ROOT / source_id
    data_dir.mkdir(parents=True, exist_ok=True)
    validation_dir.mkdir(parents=True, exist_ok=True)

    original_path = data_dir / f"{source_id.lower()}.config.json"
    accounting_path = data_dir / f"{source_id.lower()}.item_accounting.jsonl"
    correspondence_path = data_dir / f"{source_id.lower()}.correspondence.json"
    fixture_path = validation_dir / "fixture.json"
    fixture_config_path = validation_dir / "fixture.config.json"
    expected_path = validation_dir / "expected_results.json"

    _write_json(original_path, original)
    _write_jsonl(accounting_path, accounting)
    _write_json(correspondence_path, correspondence)
    _write_json(fixture_path, fixture)
    _write_json(fixture_config_path, fixture_config)
    _write_json(expected_path, expected)

    return {
        "source_id": source_id,
        "original_path": original_path,
        "original_sha256": _file_sha(original_path),
        "original_canonical_hash": canonical_config_hash(original),
        "fixture_path": fixture_path,
        "fixture_sha256": _file_sha(fixture_path),
        "fixture_source_sha256": fixture_sha,
        "fixture_config_path": fixture_config_path,
        "fixture_config_sha256": _file_sha(fixture_config_path),
        "fixture_config_canonical_hash": canonical_config_hash(fixture_config),
        "expected_path": expected_path,
        "expected_sha256": _file_sha(expected_path),
        "accounting_path": accounting_path,
        "accounting_sha256": _file_sha(accounting_path),
        "correspondence_path": correspondence_path,
        "correspondence_sha256": _file_sha(correspondence_path),
        "roster": roster,
        "included_slots": sorted(included),
        "included_items": sorted(
            items[var]["implementation_id"] for var in included
        ),
        "physical_slots": len(slots),
        "items": len(items),
        "conditional_vars": _conditional_vars(source_id, recipe),
    }


def _conditional_vars(source_id: str, recipe: Mapping[str, Any]) -> list[str]:
    # Exact held conditional/unresolved items that are plausible next slices.
    held = {
        "SRC27": ["q103_2", "q315_2", "q511"],
        "SRC28": ["q102_1", "q102_2", "q816c"],
        "SRC29": ["q403"],
        "SRC30": [],
    }[source_id]
    return [var for var in held if var not in _included_slots(recipe)]


def _build_fixture_document(
    source_id: str,
    recipe: Mapping[str, Any],
    slots: Sequence[Mapping[str, Any]],
    items: Mapping[str, Mapping[str, Any]],
    roster: Mapping[str, Any],
) -> dict[str, Any]:
    slot_by_name = {slot["name"]: slot for slot in slots}
    fixture = recipe["fixture"]
    rows = len(fixture["country_values"])
    if any(len(values) != rows for values in fixture["cells"].values()):
        raise ValueError(f"{source_id}: fixture cell arrays must match row count")
    cells = []
    for index in range(rows):
        row = index + 1
        country_slot = slot_by_name[recipe["country_slot"]]
        cells.append(
            {
                "row_ordinal": row,
                "variable_ordinal": country_slot["ordinal"],
                "variable_name": country_slot["name"],
                "raw_value": fixture["country_values"][index],
                "missing_state": "OBSERVED_STORAGE_VALUE",
                "source_missing_declaration": None,
            }
        )
        for var, values in fixture["cells"].items():
            slot = slot_by_name[var]
            raw = values[index]
            missing_state = "SYSTEM_MISSING" if raw is None else "OBSERVED_STORAGE_VALUE"
            cells.append(
                {
                    "row_ordinal": row,
                    "variable_ordinal": slot["ordinal"],
                    "variable_name": slot["name"],
                    "raw_value": raw,
                    "missing_state": missing_state,
                    "source_missing_declaration": None,
                }
            )
    document = {
        "schema": FIXTURE_SCHEMA_ID,
        "fixture_id": fixture["fixture_id"],
        "identity_class": "NONRESPONDENT_FIXTURE",
        "nonrespondent": True,
        "original_source_id": source_id,
        "original_source_sha256": roster["source_sha256"],
        "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "row_count": rows,
        "cells": cells,
        "shape_coverage": fixture["shape_coverage"],
        "expected_results_pending_oracle": True,
        "oracle_basis": (
            "Expected results are declared from the fixture cells and the serialized "
            "source-code/state rules before the factory/native-validator call; they are "
            "not copied from the native result."
        ),
        "limits": [
            "The fixture is repository-generated nonrespondent input, not original respondent data.",
            "Fixture authority is explicitly fixture-only and cannot be used for original-source construction.",
            "Native validation of this fixture does not establish original-source scientific results or execution permission.",
        ],
    }
    document["fixture_source_sha256"] = fixture_document_sha256(document)
    return document


def _build_config(
    *,
    source_id: str,
    recipe: Mapping[str, Any],
    roster: Mapping[str, Any],
    slots: Sequence[Mapping[str, Any]],
    items: Mapping[str, Mapping[str, Any]],
    codebook: Mapping[str, Mapping[str, Any]],
    selected: Mapping[str, Mapping[str, Any]],
    included: set[str],
    authority: Mapping[str, Any],
    fixture: bool,
    fixture_doc: Mapping[str, Any],
    fixture_sha: str,
) -> dict[str, Any]:
    source_sha = roster["source_sha256"]
    metadata_sha = roster["metadata_witness"]["sha256"]
    metadata = roster["metadata_witness"]
    active_sha = fixture_sha if fixture else source_sha
    active_rows = fixture_doc["row_count"] if fixture else roster["rows"]
    universe_payload, universe = _universe_payload(
        source_id=source_id,
        recipe=recipe,
        roster=roster,
        authority=authority,
        fixture=fixture,
        fixture_sha=fixture_sha if fixture else None,
    )

    questions = []
    response_slots = []
    coordinate_slots = []
    for var in sorted(included, key=lambda name: next(s["ordinal"] for s in slots if s["name"] == name)):
        target = selected[var]
        slot = next(s for s in slots if s["name"] == var)
        item = items[var]
        if target["role"] == "coordinate":
            coordinate_slots.append(
                _coordinate_slot(
                    source_id=source_id,
                    recipe=recipe,
                    slot=slot,
                    authority=authority,
                    fixture=fixture,
                )
            )
            continue
        occurrence = _occurrence(source_id=source_id, target=target)
        question = _question_payload(
            source_id=source_id,
            recipe=recipe,
            target=target,
            roster=roster,
            item=item,
            slot=slot,
            universe=universe,
            authority=authority,
            fixture=fixture,
        )
        questions.append(question)
        if fixture:
            fixture_values = recipe["fixture"]["cells"][var]
            values = _response_values_for_fixture(
                slot=slot,
                target=target,
                authority=authority,
                occurrence=occurrence,
                fixture_values=fixture_values,
            )
        else:
            values = _response_values_for_original(
                slot=slot,
                target=target,
                authority=authority,
                occurrence=occurrence,
            )
        response_slots.append(
            {
                "slot": {"ordinal": slot["ordinal"], "name": slot["name"]},
                "question_id": target["question_id"],
                "values": values,
            }
        )

    physical_payload = [
        _physical_slot_payload(
            slot=slot,
            item=items[slot["name"]],
            included=slot["name"] in included,
            target=selected.get(slot["name"]),
        )
        for slot in slots
    ]
    item_payload = [
        _item_payload(
            slot=slot,
            item=items[slot["name"]],
            codebook=codebook[slot["name"]],
            included=slot["name"] in included,
            target=selected.get(slot["name"]),
            source_id=source_id,
            metadata_sha=metadata_sha,
        )
        for slot in slots
    ]

    included_ordinals = sorted(slot["ordinal"] for slot in slots if slot["name"] in included)
    excluded_slots = [
        {
            "ordinal": slot["ordinal"],
            "name": slot["name"],
            "reason": _excluded_reason(
                (items[slot["name"]].get("p2") or {}).get("canonical_disposition")
            ),
        }
        for slot in slots
        if slot["name"] not in included
    ]
    included_ids = sorted(items[var]["implementation_id"] for var in included)
    excluded_items = [
        {
            "implementation_id": items[slot["name"]]["implementation_id"],
            "reason": _excluded_reason(
                (items[slot["name"]].get("p2") or {}).get("canonical_disposition")
            ),
        }
        for slot in slots
        if slot["name"] not in included
    ]
    if fixture:
        coverage = {
            "physical_slots_total": roster["physical_columns"],
            "items_total": roster["original_items"],
            "partial_scope_reason": (
                "Nonrespondent fixture exercises only the declared fixture slots; fixture "
                "cells are not original respondents and do not complete the original config."
            ),
            "not_a_lane_config": True,
        }
    else:
        coverage = {
            "physical_slots_total": roster["physical_columns"],
            "items_total": roster["original_items"],
            "physical_slots_included": included_ordinals,
            "physical_slots_excluded": excluded_slots,
            "items_included": included_ids,
            "items_excluded": excluded_items,
            "partial_scope_reason": (
                f"Declared supported native slice covers {len(included_ordinals)} physical "
                "slots; every remaining slot/item is serialized and inventory-accounted."
            ),
        }

    conditional_vars = _conditional_vars(source_id, recipe)
    residuals = _residuals(
        source_id=source_id,
        recipe=recipe,
        included_count=len(included_ordinals),
        item_count=len(items),
        slot_count=len(slots),
        conditional_vars=conditional_vars,
        country_enumerated=not (
            source_id in {"SRC27", "SRC29"}
        ),
    )
    if fixture:
        residuals = [
            {
                "residual_id": f"{source_id}-FIXTURE-ONLY-IDENTITY",
                "scope": f"{source_id}:{fixture_doc['fixture_id']}",
                "field": "identity_class_and_authority",
                "status": "FIXTURE_ONLY",
                "reason": (
                    "This config deliberately binds a distinct nonrespondent fixture SHA and "
                    "fixture-only authority; it is not an original-source config and cannot "
                    "be promoted to original identity."
                ),
                "dependent_operation": "original-source execution or original authority claims",
                "unaffected_scope": "the nonrespondent fixture native-validation slice",
                "owner": "R157 LITS lane author",
                "next_step": (
                    "Use the separate ORIGINAL_SOURCE config for preparation; original execution "
                    "remains a separate permission/issuance boundary."
                ),
            }
        ]

    config = {
        "schema": SCHEMA_ID,
        "config_id": (
            f"R157-LITS-{source_id}-{'NONRESPONDENT-FIXTURE' if fixture else 'SOURCE-PREPARATION'}"
        ),
        "config_revision": 1,
        "config_purpose": "NONRESPONDENT_FIXTURE" if fixture else "SOURCE_PREPARATION",
        "identity": {
            "source_id": source_id,
            "family": recipe["family"],
            "wave": recipe["wave"],
            "source_family_id": recipe["family"],
            "study_product_id": "LiTS",
            "release_id": recipe["release_id"],
            "instrument_release_id": f"{source_id}_METADATA_WITNESS_SHA256:{metadata_sha}",
            "source_artifact_id": recipe["artifact"],
            "expected_source_sha256": source_sha,
            "source_format": "DTA",
            "source_row_count": roster["rows"],
            "source_column_count": roster["physical_columns"],
            "source_bytes": roster["bytes"],
            "codebook_rows": roster["codebook_rows"],
            "original_item_count": roster["original_items"],
            "source_snapshot_retention_ref": {
                "kind": "SOURCE_SNAPSHOT",
                "object_id": f"urn:rawlsing:r157:source-snapshot:{source_id}",
                "content_hash": source_sha,
            },
            "metadata_witness_ref": {
                "kind": "R154_PHYSICAL_METADATA",
                "object_id": f"urn:rawlsing:r157:metadata:{metadata['path']}",
                "content_hash": metadata_sha,
            },
            "locator": {
                "root": "EXTERNAL_LOCATOR_ID",
                "locator_id": f"{source_id}_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING",
            },
            "reader": {
                "decoder_owner": READER_DECODER,
                "configuration_ref": _reader_ref(source_id),
                "encoding": None,
            },
        },
        "binding": {
            "identity_class": "NONRESPONDENT_FIXTURE" if fixture else "ORIGINAL_SOURCE",
            "source_sha256": active_sha,
            "row_count": active_rows,
            "source_snapshot_ref": {
                "kind": "FIXTURE_SNAPSHOT" if fixture else "SOURCE_SNAPSHOT",
                "object_id": (
                    f"urn:rawlsing:r157:fixture:{fixture_doc['fixture_id']}"
                    if fixture else f"urn:rawlsing:r157:source-snapshot:{source_id}"
                ),
                "content_hash": active_sha,
            },
            "fixture_provenance": (
                {
                    "fixture_id": fixture_doc["fixture_id"],
                    "provenance": (
                        "Repository-generated nonrespondent fixture for the R157 LITS lane; "
                        "fixture values are declared source codes or explicit fixture-only "
                        "strings; no original respondents represented."
                    ),
                    "authority_grade": "NONRESPONDENT_FIXTURE_ONLY",
                    "original_source_id": source_id,
                    "original_source_sha256": source_sha,
                    "no_original_respondents": True,
                    "fixture_study_product_id": f"R157_FIXTURE/LiTS/{source_id}",
                    "fixture_release_id": f"R157_FIXTURE_RELEASE/{source_id}",
                    "fixture_instrument_release_id": f"R157_FIXTURE_INSTRUMENT/{source_id}",
                }
                if fixture else None
            ),
        },
        "authority": {
            "snapshots": authority["snapshots"],
            "required_refs": authority["required_refs"],
            "projection_authority_ref": authority["projection_authority_ref"],
            "replay_authority_ref": authority["replay_authority_ref"],
            "projection_identity_ref": _exact_ref(
                "PROJECTION_IDENTITY",
                f"urn:rawlsing:r157:projection:{source_id}:{'fixture' if fixture else 'source'}",
                {
                    "source_id": source_id,
                    "fixture": fixture,
                    "source_sha256": active_sha,
                    "selected_vars": sorted(included),
                },
            ),
            "tie_order_ref": _exact_ref(
                "DETERMINISTIC_TIE_ORDER",
                f"urn:rawlsing:r157:tie-order:{source_id}:{'fixture' if fixture else 'source'}",
                {"source_id": source_id, "fixture": fixture, "order": "exact_ref_key"},
            ),
            "replay_protocol_version": "R157_SOURCE_CONFIGURATION@1.0.0",
        },
        "universe": {"universes": [universe_payload]},
        "respondents": {
            "subject_unit": (
                "NONRESPONDENT_FIXTURE_ROW" if fixture else recipe["subject_unit"]
            ),
            "respondent_namespace": universe_payload["respondent_namespace"],
            "respondent_key_pattern": (
                f"r157:fixture:{source_id}:row:{{row_ordinal}}"
                if fixture else f"lits:{recipe['wave']}:household_row:{{row_ordinal}}"
            ),
            "row_identity_grade": (
                "FIXTURE_ROW_IDENTITY_ONLY"
                if fixture else
                "ROW_ORDINAL_REPLAY_KEY__SOURCE_NATIVE_KEY_SLOT_HELD_UNTIL_DECODE"
            ),
        },
        "questions": questions,
        "physical_slots": physical_payload,
        "items": item_payload,
        "response_slots": response_slots,
        "coordinate_slots": coordinate_slots,
        "weight_slots": [],
        "routing": _routing_rules(
            source_id=source_id,
            targets=[selected[var] for var in sorted(included) if selected[var]["role"] != "coordinate"],
            authority=authority,
            fixture=fixture,
        ),
        "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
        "replay": {
            "predicate": {
                "typed_absence_state": "NOT_APPLICABLE",
                "detail": "No empirical predicate payload is prepared or claimed by this source config.",
            },
            "comparator": {
                "typed_absence_state": "DEFERRED",
                "detail": "No comparator payload is prepared; execution remains separate.",
            },
            "discovery": {
                "typed_absence_state": "DEFERRED",
                "detail": "No discovery frontier is prepared; execution remains separate.",
            },
            "structural": {
                "typed_absence_state": "NOT_APPLICABLE",
                "detail": "No structural admission replay payload is prepared by this source config.",
            },
        },
        "supported_scope": {
            "scope_id": (
                f"{source_id}_NONRESPONDENT_FIXTURE__"
                + "_".join(sorted(included))
                if fixture else
                f"{source_id}_SOURCE_PREPARATION__" + "_".join(sorted(included))
            ),
            "purpose": (
                "NONRESPONDENT_FIXTURE_VALIDATION" if fixture else "SOURCE_PREPARATION"
            ),
            "declared_supported": True,
            "supported_question_ids": [target["question_id"] for target in selected_targets_value(selected, included)],
            "native_validation_expectation": "POSITIVE_RELEASE" if fixture else "NOT_RUN",
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "supported_unit_slice": (
                "NONRESPONDENT_FIXTURE_HOUSEHOLD_ROW" if fixture else recipe["subject_unit"]
            ),
            "supported_form_slice": (
                "NONRESPONDENT_FIXTURE_DECLARED_CELLS" if fixture else recipe["form_slice"]
            ),
            "notes": [
                recipe["unit_notes"],
                (
                    "The native release is exercised only with the separate nonrespondent "
                    "fixture config and stream; original source execution is not performed."
                    if not fixture else
                    "Fixture-only authority is not original-source authority and cannot be promoted."
                ),
            ],
        },
        "coverage": coverage,
        "residuals": residuals,
        "evidence": _evidence_section(
            source_id=source_id,
            roster=roster,
            fixture=fixture,
            fixture_doc=fixture_doc,
            fixture_sha=fixture_sha,
        ),
        "runtime": {
            **RUNTIME,
            "transport": ["ExactPhysicalCellStream"],
            "reader_encoding_transport": (
                "P3_QUALIFIED_EXACT_SHA_READER_TRANSPORT__NOT_CONSUMED_BY_LANE_CONFIG"
            ),
        },
        "notes": [
            (
                "ORIGINAL_SOURCE preparation config; original respondent execution and "
                "original workload issuance are NOT performed under R157."
                if not fixture else
                "NONRESPONDENT_FIXTURE config; distinct fixture byte identity and fixture-only authority."
            ),
            (
                "All original items and physical slots are retained; included/excluded "
                "partition is explicit and no slot or item is dropped."
            ),
            (
                "No ALLOW original-source authority, default person/scalar, default form, "
                "implicit weight or synthetic universe is asserted."
            ),
        ],
    }
    return config


def selected_targets_value(
    selected: Mapping[str, Mapping[str, Any]], included: Iterable[str]
) -> list[Mapping[str, Any]]:
    result = []
    for var in included:
        target = selected[var]
        if target["role"] != "coordinate":
            result.append(target)
    return result


def _excluded_reason(disposition: Any) -> str:
    mapping = {
        "ADMINISTRATIVE_METADATA": "administrative/metadata",
        "STRUCTURAL_CONTEXT": "structural/context",
        "POSITION_COORDINATE": "position-coordinate",
        "RELATION_EVIDENCE": "relation/measurement",
    }
    category = mapping.get(str(disposition), "inventory")
    return (
        f"Not in declared native slice: {category} item is serialized and accounted "
        "with exact codebook/P2/H48/relation identity; no native response/coordinate "
        "slot, default meaning or generic pending gate is claimed."
    )


def _evidence_section(
    *,
    source_id: str,
    roster: Mapping[str, Any],
    fixture: bool,
    fixture_doc: Mapping[str, Any],
    fixture_sha: str,
) -> dict[str, Any]:
    item_file = MANIFEST_FILES["ITEM_EVIDENCE.jsonl.gz"]
    p2_file = MANIFEST_FILES["P2_PHASE0.csv.gz"]
    slots_file = MANIFEST_FILES["PHYSICAL_SLOTS.jsonl.gz"]
    roster_file = MANIFEST_FILES["SOURCE_ROSTER.json"]
    codebook_file = MANIFEST_FILES["CODEBOOK_ROWS.jsonl.gz"]
    metadata = roster["metadata_witness"]
    metadata_ref = {
        "kind": "R154_PHYSICAL_METADATA",
        "object_id": f"urn:rawlsing:r157:metadata:{metadata['path']}",
        "content_hash": metadata["sha256"],
    }
    pinned = [
        {"kind": "R157_PLAN_SEAL", "commit": PLAN_SEAL},
        {
            "kind": "R154_METADATA_SNAPSHOT",
            "commit": "a02adc896264e1b46afd143cba9426182ec14802",
            "path": "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/store/r154_all35.sqlite",
            "sha256": "7d6421e6e50f7d249cf09e7ecf964757d6afa4a7926d7a31eb1aad3407a12a16",
            "bytes": 30912512,
        },
        {
            "kind": "H48_ITEM_INDEX",
            "commit": "359ddabc89d78ceb4c8fa45561588ee4cad7dd11",
            "path": "WORKER_RETURNS/PYAT-R48-H48-AUTHORITY-AND-CODE-ATLAS-R1/evidence/original_item_authority_candidates.json.gz",
            "sha256": "35818e2cdd2b7e16e60788bef094eb117ef78fc63df3dc068ecb8b8948f728f5",
            "bytes": 3107463,
        },
        {"kind": "P2_PHASE0", "sha256": "d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6", "bytes": 7709908},
        {
            "kind": "FULL_RELATION_AUTHORITY",
            "commit": "9561723cfe0932869e781f2be27e9c80b050ad7a",
            "path": "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv",
            "sha256": "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13",
            "bytes": 47874248,
        },
        {
            "kind": "SOURCE_METADATA_WITNESS",
            "commit": metadata["commit"],
            "path": metadata["path"],
            "sha256": metadata["sha256"],
            "bytes": metadata["bytes"],
        },
        {"kind": "PORTABLE_ITEM_EVIDENCE", "sha256": item_file["sha256"], "bytes": item_file["bytes"]},
        {"kind": "PORTABLE_P2_PHASE0", "sha256": p2_file["sha256"], "bytes": p2_file["bytes"]},
        {"kind": "PORTABLE_PHYSICAL_SLOTS", "sha256": slots_file["sha256"], "bytes": slots_file["bytes"]},
        {"kind": "PORTABLE_CODEBOOK_ROWS", "sha256": codebook_file["sha256"], "bytes": codebook_file["bytes"]},
        {"kind": "PORTABLE_SOURCE_ROSTER", "sha256": roster_file["sha256"], "bytes": roster_file["bytes"]},
    ]
    field_evidence = [
        {
            "field": "identity.source_artifact_and_metadata_witness",
            "refs": [metadata_ref, _file_ref("SOURCE_ROSTER", "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json", roster_file["sha256"])],
        },
        {
            "field": "physical_slots_and_codebook_mapping",
            "refs": [
                _file_ref("PHYSICAL_SLOTS", "rawlsing_next/source_configuration/evidence/PHYSICAL_SLOTS.jsonl.gz", slots_file["sha256"]),
                _file_ref("CODEBOOK_ROWS", "rawlsing_next/source_configuration/evidence/CODEBOOK_ROWS.jsonl.gz", codebook_file["sha256"]),
                metadata_ref,
            ],
        },
        {
            "field": "original_item_identity_and_relation",
            "refs": [
                _file_ref("ITEM_EVIDENCE", "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz", item_file["sha256"]),
                _file_ref("P2_PHASE0", "rawlsing_next/source_configuration/evidence/P2_PHASE0.csv.gz", p2_file["sha256"]),
            ],
        },
        {
            "field": "routing_and_relation_authority",
            "refs": [
                _file_ref("ITEM_EVIDENCE_ROUTING_STATUS", "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz", item_file["sha256"]),
            ],
        },
        {
            "field": "reader_configuration",
            "refs": [_reader_ref(source_id)],
        },
    ]
    limits = [
        "Prior H48/P2/relation evidence is reused with its original grade and limits; it is not current execution permission.",
        "No original respondent rows were read; fixture cells are explicitly nonrespondent.",
        "The 26 exact relation nonmatches are outside this lane's four exact-join sources and remain preserved globally.",
        "Storage missingness alone does not establish asked/not-asked; conditional routing is held.",
        "No population, causal, transport or temporal claim is made from the raw source sample.",
    ]
    if fixture:
        field_evidence.append(
            {
                "field": "nonrespondent_fixture_identity",
                "refs": [
                    _exact_ref(
                        "NONRESPONDENT_FIXTURE",
                        f"urn:rawlsing:r157:fixture:{fixture_doc['fixture_id']}",
                        {
                            "fixture_id": fixture_doc["fixture_id"],
                            "fixture_source_sha256": fixture_sha,
                            "original_source_sha256": roster["source_sha256"],
                        },
                    )
                ],
            }
        )
        limits.append("Fixture authority is NONRESPONDENT_FIXTURE_ONLY and cannot establish original-source authority.")
    return {
        "source_roster_path": "rawlsing_next/source_configuration/evidence/SOURCE_ROSTER.json",
        "item_index_path": "rawlsing_next/source_configuration/evidence/ITEM_EVIDENCE.jsonl.gz",
        "evidence_manifest_path": "rawlsing_next/source_configuration/evidence/EVIDENCE_MANIFEST.json",
        "pinned_inputs": pinned,
        "field_evidence": field_evidence,
        "limits": limits,
    }


def _correspondence(
    source_id: str,
    roster: Mapping[str, Any],
    slots: Sequence[Mapping[str, Any]],
    items: Mapping[str, Mapping[str, Any]],
    selected: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    slot_by_name = {slot["name"]: slot for slot in slots}
    mappings = []
    for var in sorted(selected):
        slot = slot_by_name[var]
        item = items[var]
        relation = item.get("relation") or {}
        mappings.append(
            {
                "physical_ordinal": slot["ordinal"],
                "physical_name": slot["name"],
                "codebook_var_name": slot["name"],
                "codebook_row_hash": (slot.get("codebook_mapping") or {}).get("row_hash"),
                "implementation_id": item["implementation_id"],
                "exact_identity_sha256": item["exact_identity_sha256"],
                "relation_question_id": relation.get("question_id"),
                "relation_status": relation.get("authority_status_final_or_current"),
                "manual_response_topology": relation.get("manual_response_topology"),
                "routing_status": _routing_status(item),
                "correspondence": "EXACT_LITERAL_NAME_MATCH",
                "alias_used": False,
            }
        )
    return {
        "schema": "PYAT_R157_LITS_EXACT_NAME_CORRESPONDENCE@1.0.0",
        "source_id": source_id,
        "source_family": roster["family"],
        "wave": roster["wave"],
        "physical_columns": roster["physical_columns"],
        "codebook_rows": roster["codebook_rows"],
        "original_items": roster["original_items"],
        "physical_only": roster["physical_only"],
        "codebook_only": roster["codebook_only"],
        "exact_relation_matches": roster["exact_relation_matches"],
        "name_set_relation": "EXACT_LITERAL_NAME_SET_MATCH__NO_ALIAS_REQUIRED",
        "normalization_used": "NONE",
        "selected_native_slice": mappings,
        "notes": (
            "The four LITS sources already have exact literal physical/codebook name sets; "
            "this record reuses those exact names. No casefold, punctuation replacement, "
            "P<->Q prefix assumption, copied-edition mapping, nearest-label substitution or "
            "dynamic alias is applied. Only SRC25/SRC26 require exact correspondence work."
        ),
    }


def _expected_results(
    source_id: str,
    recipe: Mapping[str, Any],
    original: Mapping[str, Any],
    fixture_config: Mapping[str, Any],
    fixture: Mapping[str, Any],
    fixture_sha: str,
) -> dict[str, Any]:
    by_question: dict[str, list[str]] = {}
    canonical_by_question: dict[str, list[Any]] = {}
    for slot in fixture_config["response_slots"]:
        qid = slot["question_id"]
        by_question[qid] = []
        canonical_by_question[qid] = []
        values_by_raw = {
            _raw_key(value["raw_value"], value["missing_state"]): value
            for value in slot["values"]
        }
        for cell in fixture["cells"]:
            if cell["variable_ordinal"] != slot["slot"]["ordinal"]:
                continue
            key = _raw_key(cell["raw_value"], cell["missing_state"])
            rule = values_by_raw.get(key)
            if rule is None:
                raise ValueError(
                    f"{source_id}: no fixture value rule for {slot['slot']['name']} {key!r}"
                )
            by_question[qid].append(rule["response_state"])
            canonical_by_question[qid].append(rule["canonical_value"])
    response_events = sum(len(values) for values in by_question.values())
    coordinate_facts = fixture["row_count"] * len(fixture_config["coordinate_slots"])
    routing_facts = fixture["row_count"] * len(fixture_config["routing"])
    return {
        "schema": "PYAT_R157_LITS_NONRESPONDENT_ORACLE@1.0.0",
        "source_id": source_id,
        "fixture_id": fixture["fixture_id"],
        "fixture_path": f"source_pre553_validation/{source_id}/fixture.json",
        "fixture_sha256": fixture_sha,
        "fixture_config_path": f"source_pre553_validation/{source_id}/fixture.config.json",
        "fixture_config_canonical_hash": canonical_config_hash(fixture_config),
        "original_config_path": f"rawlsing_next/source_configuration/data/{source_id}/{source_id.lower()}.config.json",
        "original_source_id": source_id,
        "original_source_sha256": fixture["original_source_sha256"],
        "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "fixture_only": True,
        "row_count": fixture["row_count"],
        "question_count": len(fixture_config["questions"]),
        "response_slot_count": len(fixture_config["response_slots"]),
        "coordinate_slot_count": len(fixture_config["coordinate_slots"]),
        "routing_question_count": len(fixture_config["routing"]),
        "authority_snapshot_count": len(fixture_config["authority"]["snapshots"]),
        "respondent_count": fixture["row_count"],
        "response_event_count": response_events,
        "coordinate_fact_count": coordinate_facts,
        "routing_fact_count": routing_facts,
        "response_states_by_question": by_question,
        "canonical_values_by_question": canonical_by_question,
        "weight_section": "NOT_APPLICABLE",
        "source_relation_section": "DISTINCT_BY_DEFAULT",
        "oracle_basis": (
            "Declared from the fixture cells and serialized source-code/state rules before "
            "the factory/native-validator call; not copied from the native result."
        ),
        "limits": [
            "Nonrespondent fixture validation does not establish original-source scientific results.",
            "Fixture authority is separate from original-source authority.",
            "Original source execution is not performed or claimed.",
        ],
    }


def _raw_key(raw_value: Any, missing_state: str) -> tuple[Any, str]:
    if isinstance(raw_value, bool):
        raise ValueError("boolean physical value is not a source code")
    if raw_value is None:
        return (None, missing_state)
    if isinstance(raw_value, float) and raw_value.is_integer():
        return (int(raw_value), missing_state)
    return (raw_value, missing_state)


def _write_json(path: Path, document: Any) -> None:
    path.write_text(
        json.dumps(document, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n")


def main() -> int:
    results = []
    for source_id in ("SRC27", "SRC28", "SRC29", "SRC30"):
        result = build_source(source_id)
        results.append(
            {
                "source_id": source_id,
                "original_path": str(result["original_path"].relative_to(ROOT)),
                "original_sha256": result["original_sha256"],
                "original_canonical_hash": result["original_canonical_hash"],
                "fixture_path": str(result["fixture_path"].relative_to(ROOT)),
                "fixture_sha256": result["fixture_sha256"],
                "fixture_source_sha256": result["fixture_source_sha256"],
                "fixture_config_path": str(result["fixture_config_path"].relative_to(ROOT)),
                "fixture_config_sha256": result["fixture_config_sha256"],
                "fixture_config_canonical_hash": result["fixture_config_canonical_hash"],
                "expected_path": str(result["expected_path"].relative_to(ROOT)),
                "expected_sha256": result["expected_sha256"],
                "accounting_path": str(result["accounting_path"].relative_to(ROOT)),
                "accounting_sha256": result["accounting_sha256"],
                "correspondence_path": str(result["correspondence_path"].relative_to(ROOT)),
                "correspondence_sha256": result["correspondence_sha256"],
                "physical_slots": result["physical_slots"],
                "items": result["items"],
                "included_slots": result["included_slots"],
                "included_items": result["included_items"],
                "conditional_vars": result["conditional_vars"],
            }
        )
    manifest_path = VALIDATION_ROOT / "SRC27" / "generated_manifest.json"
    _write_json(
        manifest_path,
        {
            "schema": "PYAT_R157_LITS_GENERATED_MANIFEST@1.0.0",
            "lane_id": "LITS",
            "plan_seal": PLAN_SEAL,
            "p0_dependency_commit": P0_DEPENDENCY_COMMIT,
            "lane_base_head": BASE_HEAD,
            "generated_by": "rawlsing_next/source_configuration/data/SRC27/lits_lane_build.py",
            "sources": results,
        },
    )
    print(json.dumps({"ok": True, "manifest": str(manifest_path.relative_to(ROOT)), "sources": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
