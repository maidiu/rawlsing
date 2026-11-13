"""PYAT1007 EARLY SOURCEFREE FIXTURE PREP harness (TEST_ONLY).

One generic, config-driven path:

    compact R157 metadata witness -> closed R157 NONRESPONDENT_FIXTURE config
    -> real SAV/DTA synthetic bytes -> existing S1-B decoder/projection/factory
    -> existing S2-B direct I02 + accepted S2-C physical estate
    -> accepted S2-D cold I03/I05/Batch admission.

No original respondent bytes, original source hash, translation, rights or
scientific comparability are manufactured.  The three fixture shapes exist only
to exercise accepted interfaces.  Arab/WVS labels and missing/state rules are
copied from the exact R157 Git metadata blobs; fixture topology/routing overrides
are explicitly marked TEST_ONLY and are not claims about administered surveys.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd
import pyreadstat

from rawlsing_next._pre553_direct_i02_sourcefree import (
    SourcefreeDirectI02Sections,
    direct_sections_from_candidate,
)
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_c11_ingest import (
    build_candidate_replay_manifest,
    validate_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import RespondentIdentity
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalQuerySpec,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    exact_ref,
    make_empirical_predicate,
)
from rawlsing_next.pre553_r157_projection_adapter import (
    SourceConfig,
    build_governed_c11_projection,
    decode_fixture_config,
    project_c11_candidate_from_config,
    row_native_keys_from_transport,
)
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_source_direct_parquet_estate import (
    EstateReceipt,
    write_direct_estate,
)

RETURN_ROOT = Path(__file__).resolve().parent
METADATA_PATH = RETURN_ROOT / "metadata" / "R157_METADATA_GROUNDING.json"
R157_COMMIT = "1924499ef52403a0f331b8aff9b7c7eff99bf1e2"
TEST_ONLY = "PYAT1007_TEST_ONLY_NONRESPONDENT_FIXTURE"


def sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def ref(kind: str, object_id: str, material: Any | None = None) -> ExactRef:
    digest = sha256_text(
        json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
        if material is not None
        else f"{kind}:{object_id}"
    )
    return ExactRef(kind, object_id, digest)


def authority_ref(authority_id: str, version: str = "1.0.0") -> dict[str, str]:
    return {
        "authority_id": authority_id,
        "authority_version": version,
        "authority_content_hash": sha256_text(f"authority:{authority_id}:{version}"),
    }


def _authority_snapshot(
    authority_id: str,
    kind: str,
    families: Sequence[str],
    *,
    fixture_id: str,
    operation: str | None = None,
) -> dict[str, Any]:
    name = authority_id
    return {
        "typed_state": "ALLOW",
        "authority_snapshot_refs": [],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": ref(
            "REPLAY_ROOT", f"urn:rawlsing:pyat1007:test:authority:{name}:root"
        ).as_dict(),
        "authority_id": authority_id,
        "authority_version": "1.0.0",
        "authority_content_hash": sha256_text(f"authority:{authority_id}:1.0.0"),
        "authority_kind": kind,
        "decision_state": "ALLOW",
        "governed_operations": [operation or f"PYAT1007-TEST-{name}"],
        "governed_object_families": list(families),
        "scope_envelope": {
            "fixture_only": True,
            "grade": "NONRESPONDENT_FIXTURE_ONLY",
            "fixture_id": fixture_id,
        },
        "effective_time_or_interval": "PYAT1007_TEST_ONLY_FIXTURE",
        "parent_authority_refs": [],
        "negative_limit_refs": [],
        "supersession_refs": [],
        "interpretation_semantics_fingerprint": sha256_text(f"fp:{authority_id}"),
        "replay_protocol_ref": ref(
            "REPLAY_PROTOCOL", f"urn:rawlsing:pyat1007:test:authority:{name}:replay"
        ).as_dict(),
    }


def _typed_absence(state: str, detail: str | None = None) -> dict[str, Any]:
    return {"typed_absence_state": state, "detail": detail}


@dataclass(frozen=True)
class SeriesFixtureSpec:
    series_key: str
    fixture_id: str
    positive_questions: tuple[str, ...]
    route_unknown_questions: tuple[str, ...]
    rank_question: str | None
    rows: Mapping[str, tuple[Any, ...]]
    routing_overrides: Mapping[str, str]
    occurrence_overrides: Mapping[str, tuple[str, int]]
    carrier_kinds: Mapping[str, str]
    coordinate_variables: tuple[str, ...]
    key_variable: str | None
    scalar_domains: Mapping[str, tuple[str, ...]]


SERIES_SPECS: Mapping[str, SeriesFixtureSpec] = MappingProxyType({
    "ARAB_SRC07": SeriesFixtureSpec(
        series_key="ARAB_SRC07",
        fixture_id="PYAT1007_ARAB_SRC07_NONRESPONDENT_TEST",
        positive_questions=("Q508",),
        route_unknown_questions=("Q509",),
        rank_question="Q104A_2_1",
        rows={
            "COUNTRY": (8.0, 10.0, 13.0, 15.0, 21.0, 7.0),
            "Q508": (0.0, 5.0, 10.0, 98.0, 99.0, 3.0),
            "Q509": (1.0, 2.0, 98.0, 4.0, 5.0, 6.0),
            "Q104A_2_1": (1.0, 0.0, 1.0, 0.0, 1.0, 0.0),
        },
        routing_overrides={"Q508": "ELIGIBLE_APPLICABLE", "Q104A_2_1": "ELIGIBLE_APPLICABLE"},
        occurrence_overrides={"Q104A_2_1": ("MULTISELECT", 2)},
        carrier_kinds={"Q508": "SCALAR_SINGULAR", "Q509": "SCALAR_SINGULAR", "Q104A_2_1": "MULTISELECT"},
        coordinate_variables=("COUNTRY",),
        key_variable=None,
        scalar_domains={
            "Q508": tuple(f"{value}.0" for value in range(0, 11)),
            "Q509": tuple(f"{value}.0" for value in range(0, 11)),
            "Q104A_2_1": ("0.0", "1.0"),
        },
    ),
    "WVS_SRC35": SeriesFixtureSpec(
        series_key="WVS_SRC35",
        fixture_id="PYAT1007_WVS_SRC35_NONRESPONDENT_TEST",
        positive_questions=("Q1", "Q2", "Q3"),
        route_unknown_questions=("Q4",),
        rank_question=None,
        rows={
            "S007": (9001.0, 9002.0, 9003.0, 9004.0, 9005.0, 9006.0),
            "A_YEAR": (2020.0, 2021.0, 2022.0, 2023.0, 2017.0, 2018.0),
            "Q1": (1.0, 2.0, 3.0, 4.0, -1.0, 2.0),
            "Q2": (1.0, 2.0, 4.0, 3.0, -2.0, 1.0),
            "Q3": (4.0, 3.0, 2.0, 1.0, 1.0, -4.0),
            "Q4": (1.0, 2.0, 1.0, 2.0, -5.0, 3.0),
        },
        routing_overrides={"Q1": "ELIGIBLE_APPLICABLE", "Q2": "ELIGIBLE_APPLICABLE", "Q3": "ELIGIBLE_APPLICABLE"},
        occurrence_overrides={},
        carrier_kinds={"Q1": "SCALAR_SINGULAR", "Q2": "SCALAR_SINGULAR", "Q3": "SCALAR_SINGULAR", "Q4": "SCALAR_SINGULAR"},
        coordinate_variables=("A_YEAR",),
        key_variable="S007",
        scalar_domains={
            "Q1": ("1.0", "2.0", "3.0", "4.0"),
            "Q2": ("1.0", "2.0", "3.0", "4.0"),
            "Q3": ("1.0", "2.0", "3.0", "4.0"),
            "Q4": ("1.0", "2.0", "3.0", "4.0"),
        },
    ),
    "LITS_SRC28_HOSTILE": SeriesFixtureSpec(
        series_key="LITS_SRC28_HOSTILE",
        fixture_id="PYAT1007_LITS_SRC28_NONRESPONDENT_HOSTILE",
        positive_questions=("q201",),
        route_unknown_questions=("q102_1",),
        rank_question=None,
        rows={
            "psu": (101.0, 102.0, 103.0, 104.0, 105.0, 106.0),
            "q201": (1.0, 2.0, 3.0, -97.0, -98.0, 7.0),
            "q102_1": (1.0, 2.0, None, 1.0, 2.0, 1.0),
        },
        routing_overrides={},
        occurrence_overrides={},
        carrier_kinds={"q201": "SCALAR_SINGULAR", "q102_1": "REPEATED_EVENT"},
        coordinate_variables=("psu",),
        key_variable=None,
        scalar_domains={
            "q201": tuple(f"{value}.0" for value in range(1, 8)),
            "q102_1": ("1.0", "2.0"),
        },
    ),
})


def load_metadata(path: str | Path = METADATA_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _variable_metadata(metadata: Mapping[str, Any], series_key: str, name: str) -> Mapping[str, Any]:
    return metadata["series"][series_key]["selected_variables"][name]


def _slot_payload(
    ordinal: int,
    variable: Mapping[str, Any],
    *,
    name: str,
    disposition: str,
    measure: str | None = None,
) -> dict[str, Any]:
    return {
        "ordinal": ordinal,
        "name": name,
        "label": variable.get("label"),
        "storage_type": variable.get("storage_type"),
        "original_type": variable.get("original_type"),
        "storage_width": variable.get("storage_width"),
        "measure": measure if measure is not None else variable.get("measure"),
        "value_labels": variable.get("value_labels"),
        "missing_declarations": variable.get("missing_declarations"),
        "mr_declarations": variable.get("mr_declarations"),
        "codebook_mapping": variable.get("codebook_mapping")
        or {
            "var_name": name,
            "row_hash": sha256_text(f"pyat1007:test:{name}"),
            "status": "TEST_ONLY_SYNTHETIC",
        },
        "disposition": disposition,
        "disposition_reason": "PYAT1007 TEST_ONLY nonrespondent fixture metadata binding.",
    }


def _occurrence_rules(
    name: str,
    variable: Mapping[str, Any],
    spec: SeriesFixtureSpec,
) -> tuple[list[dict[str, Any]], str]:
    override = spec.occurrence_overrides.get(name)
    if override is not None:
        kind, count = override
        return (
            [
                {
                    "key": str(index),
                    "topology_ref": ref(
                        "RESPONSE_TOPOLOGY",
                        f"urn:rawlsing:pyat1007:test:{spec.series_key}:topology:{name}:{kind}:{index}",
                    ).as_dict(),
                    "multiplicity_order_rank_fields": {"kind": kind, "index": index},
                }
                for index in range(count)
            ],
            kind,
        )
    kind = spec.carrier_kinds[name]
    return (
        [
            {
                "key": "0",
                "topology_ref": ref(
                    "RESPONSE_TOPOLOGY",
                    f"urn:rawlsing:pyat1007:test:{spec.series_key}:topology:{name}:{kind}:0",
                ).as_dict(),
                "multiplicity_order_rank_fields": {"kind": kind, "index": 0},
            }
        ],
        kind,
    )


def _response_values(
    name: str,
    variable: Mapping[str, Any],
    spec: SeriesFixtureSpec,
) -> list[dict[str, Any]]:
    occurrences, kind = _occurrence_rules(name, variable, spec)
    values = []
    for state in variable.get("r157_value_states", ()):
        raw = state["raw_value"]
        if raw is not None:
            try:
                raw = float(raw)
            except (TypeError, ValueError):
                pass
        occurrences_payload = []
        for index, occurrence in enumerate(occurrences):
            item = dict(occurrence)
            item["key"] = str(index)
            item["multiplicity_order_rank_fields"] = {
                **dict(occurrence["multiplicity_order_rank_fields"]),
                "index": index,
            }
            occurrences_payload.append(item)
        values.append({
            "raw_value": raw,
            "missing_state": state["missing_state"],
            "source_missing_declaration": state.get("source_missing_declaration"),
            "response_state": state["response_state"],
            "occurrences": occurrences_payload,
            "canonical_value": (
                str(raw)
                if raw is not None and state["response_state"] == "SUBSTANTIVE_RESPONSE"
                else None
            ),
            "transform_authority_ref": (
                None
                if state["response_state"] != "SUBSTANTIVE_RESPONSE"
                else authority_ref(f"PYAT1007-{spec.series_key}-MAPPING")
            ),
            "extra_authority_refs": [],
        })
    return values


def build_fixture_config(
    metadata: Mapping[str, Any],
    spec: SeriesFixtureSpec,
    *,
    active_source_sha256: str,
    row_count: int,
    source_bytes: int,
    source_format: str,
    config_id: str,
    fixture_release_id: str,
) -> dict[str, Any]:
    series = metadata["series"][spec.series_key]
    variables = series["selected_variables"]
    if source_format != series["source_format"]:
        raise ValueError("fixture format differs from the exact R157 metadata format")
    fixture_id = spec.fixture_id
    original_identity_sha = sha256_text(
        f"PYAT1007_TEST_ONLY_ORIGINAL_IDENTITY_NOT_READ:{series['source_id']}"
    )
    if active_source_sha256 == original_identity_sha:
        raise ValueError("fixture bytes may not reuse the synthetic original identity")
    if series["weight_slots_count"]:
        raise ValueError("this prep only covers the R157 no-weight fixture shape")
    source_auth = authority_ref(f"PYAT1007-{spec.series_key}-SOURCE")
    mapping_auth = authority_ref(f"PYAT1007-{spec.series_key}-MAPPING")
    topology_auth = authority_ref(f"PYAT1007-{spec.series_key}-TOPOLOGY")
    coord_auth = authority_ref(f"PYAT1007-{spec.series_key}-COORD")
    routing_auth = authority_ref(f"PYAT1007-{spec.series_key}-ROUTING")
    replay_auth = authority_ref(f"PYAT1007-{spec.series_key}-REPLAY")
    projection_auth = authority_ref(f"PYAT1007-{spec.series_key}-PROJECTION")
    snapshots = [
        _authority_snapshot(
            f"PYAT1007-{spec.series_key}-SOURCE", "SOURCE_SEMANTICS_TOPOLOGY",
            ("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"), fixture_id=fixture_id,
        ),
        _authority_snapshot(
            f"PYAT1007-{spec.series_key}-MAPPING",
            "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
            ("RespondentEvent@1.0.0",), fixture_id=fixture_id,
        ),
        _authority_snapshot(
            f"PYAT1007-{spec.series_key}-TOPOLOGY", "SOURCE_SEMANTICS_TOPOLOGY",
            ("RespondentEvent@1.0.0",), fixture_id=fixture_id,
        ),
        _authority_snapshot(
            f"PYAT1007-{spec.series_key}-COORD", "COORDINATE_SEMANTICS",
            ("EmpiricalCoordinateFact@1.0.0",), fixture_id=fixture_id,
        ),
        _authority_snapshot(
            f"PYAT1007-{spec.series_key}-ROUTING", "ROUTING_RISK_SET",
            ("RoutingEligibilityFact@1.0.0",), fixture_id=fixture_id,
        ),
        _authority_snapshot(
            f"PYAT1007-{spec.series_key}-REPLAY", "REPLAY_PROTOCOL",
            ("ReplayReceipt@1.0.0",), fixture_id=fixture_id,
        ),
        _authority_snapshot(
            f"PYAT1007-{spec.series_key}-PROJECTION", "SOURCE_SEMANTICS_TOPOLOGY",
            ("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0"), fixture_id=fixture_id,
        ),
    ]
    universe_payload = {
        "typed_state": "UNIVERSE_IDENTIFIED",
        "authority_snapshot_refs": [source_auth],
        "dependency_refs": [],
        "producer_replay_locator_or_reference_root": ref(
            "REPLAY_ROOT", f"urn:rawlsing:pyat1007:test:{spec.series_key}:universe:root"
        ).as_dict(),
        "raw_source_identity": f"{TEST_ONLY}:{series['source_id']}",
        "source_family": f"NONRESPONDENT_FIXTURE_{series['family']}",
        "study_product_release": f"{TEST_ONLY}:{series['source_id']}:study/release",
        "instrument_release": f"{TEST_ONLY}:{series['source_id']}:instrument",
        "country_geography": "NONRESPONDENT_FIXTURE",
        "sampling_geography": "NONRESPONDENT_FIXTURE",
        "raw_wave": series["wave"],
        "canonical_wave_if_governed": None,
        "field_or_reference_time": "PYAT1007_TEST_ONLY_FIXTURE",
        "target_population_and_sample_frame": "NONRESPONDENT_FIXTURE",
        "sampling_design_regime": "NONRESPONDENT_FIXTURE",
        "respondent_namespace": f"urn:rawlsing:pyat1007:test:{spec.series_key}:rows",
        "source_artifact_import_lineage": TEST_ONLY,
        "harmonization_authority_ref": None,
        "source_relation_refs": [],
    }
    universe_ref = EmpiricalUniverse(**universe_payload).ref.as_dict()

    response_variables = [
        name for name in variables
        if name not in spec.coordinate_variables and name != spec.key_variable
    ]
    ordered_physical = list(spec.coordinate_variables)
    if spec.key_variable is not None:
        ordered_physical.append(spec.key_variable)
    ordered_physical.extend(response_variables)

    physical_slots = []
    slot_ordinal: dict[str, int] = {}
    for ordinal, name in enumerate(ordered_physical, 1):
        slot_ordinal[name] = ordinal
        variable = variables[name]
        if name in spec.coordinate_variables:
            disposition = "SUPPORTED_COORDINATE"
        elif name == spec.key_variable:
            disposition = "SOURCE_NATIVE_RESPONDENT_KEY"
        else:
            disposition = "SUPPORTED_RESPONSE"
        physical_slots.append(
            _slot_payload(ordinal, variable, name=name, disposition=disposition)
        )

    questions = []
    for name in response_variables:
        variable = variables[name]
        questions.append({
            "question_id": name,
            "empirical_universe_ref": universe_ref,
            "native_question_ref": ref(
                "QUESTION_NATIVE", f"urn:rawlsing:pyat1007:test:{spec.series_key}:question:{name}"
            ).as_dict(),
            "instrument_question_version": f"PYAT1007_TEST_ONLY_R157_{series['wave']}",
            "canonical_question_ref_or_typed_absence": _typed_absence(
                "NOT_AUTHORIZED",
                "No canonical adoption or directional certification is issued by this sourcefree fixture.",
            ),
            "component_subitem_ref_or_typed_absence": _typed_absence("NOT_APPLICABLE"),
            "semantic_authority_ref": mapping_auth,
            "topology_authority_ref": topology_auth,
        })

    items = []
    for name in response_variables:
        variable = variables[name]
        row_hash = (variable.get("codebook_mapping") or {}).get("row_hash")
        if not isinstance(row_hash, str) or len(row_hash) != 64:
            row_hash = sha256_text(f"pyat1007:item:{spec.series_key}:{name}")
        items.append({
            "implementation_id": f"pyat1007.test.{spec.series_key}.{name}",
            "source_variable_code": name,
            "exact_identity_sha256": row_hash,
            "question_text": variable.get("label") or name,
            "disposition": "SUPPORTED_RESPONSE",
            "response_classes": (
                "RANKED_OCCURRENCE_TEST_ONLY"
                if name == spec.rank_question
                else "SCALAR"
            ),
            "mapping_status": "TEST_ONLY_FIXTURE_EXACT_R157_METADATA",
            "authority_status": "NONRESPONDENT_FIXTURE_ONLY",
            "evidence_refs": [
                ref(
                    "S1B_EVIDENCE",
                    f"urn:rawlsing:pyat1007:test:{spec.series_key}:item:{name}",
                ).as_dict()
            ],
            "limits": [
                "TEST_ONLY nonrespondent fixture; not original survey administration or rights."
            ],
        })

    response_slots = []
    for name in response_variables:
        response_slots.append({
            "slot": {"ordinal": slot_ordinal[name], "name": name},
            "question_id": name,
            "values": _response_values(name, variables[name], spec),
        })

    coordinate_slots = []
    for name in spec.coordinate_variables:
        coordinate_slots.append({
            "slot": {"ordinal": slot_ordinal[name], "name": name},
            "native_coordinate_ref": ref(
                "COORDINATE_NATIVE", f"urn:rawlsing:pyat1007:test:{spec.series_key}:coordinate:{name}"
            ).as_dict(),
            "unit_taxonomy_ref": ref(
                "UNIT_TAXONOMY", f"urn:rawlsing:pyat1007:test:{spec.series_key}:unit:{name}"
            ).as_dict(),
            "effective_time": "PYAT1007_TEST_ONLY_FIXTURE",
            "source_semantic_authority_ref": coord_auth,
            "canonical_coordinate_ref": None,
            "normalization_ref": None,
            "values": [],
            "copy_observed_raw": True,
        })

    risk_groups = {
        name: (
            "positive"
            if name in spec.positive_questions
            or spec.routing_overrides.get(name) == "ELIGIBLE_APPLICABLE"
            else "unknown"
        )
        for name in response_variables
    }
    risk_refs = {
        group: ref(
            "RISK_SET", f"urn:rawlsing:pyat1007:test:{spec.series_key}:risk:{group}"
        ).as_dict()
        for group in ("positive", "unknown")
    }
    routing = []
    for name in response_variables:
        series_state = variables[name].get("r157_routing_state") or "ROUTING_UNKNOWN"
        state = spec.routing_overrides.get(name, series_state)
        routing.append({
            "question_id": name,
            "row_selector": "ALL",
            "typed_state": state,
            "risk_set_ref": risk_refs[risk_groups[name]],
            "routing_rule_ref": ref(
                "ROUTING_RULE", f"urn:rawlsing:pyat1007:test:{spec.series_key}:routing:{name}"
            ).as_dict(),
            "member_set_replay_ref": ref(
                "MEMBER_SET_REPLAY", f"urn:rawlsing:pyat1007:test:{spec.series_key}:members:{name}"
            ).as_dict(),
            "authority_ref": routing_auth,
            "parent_predicate_refs": [],
            "dependency_refs": [],
        })

    respondents = {
        "subject_unit": "NONRESPONDENT_FIXTURE_ROW",
        "respondent_namespace": f"urn:rawlsing:pyat1007:test:{spec.series_key}:rows",
        "respondent_key_pattern": f"PYAT1007-{series['source_id']}-ROW-{{row_ordinal:04d}}",
        "source_native_key_slot": (
            {"ordinal": slot_ordinal[spec.key_variable], "name": spec.key_variable}
            if spec.key_variable is not None
            else None
        ),
        "row_identity_grade": (
            "NONRESPONDENT_FIXTURE_KEY_WITNESS"
            if spec.key_variable is not None
            else "NONRESPONDENT_FIXTURE_ROW_ORDINAL"
        ),
    }

    document = {
        "schema": "PYAT_R157_SOURCE_CONFIGURATION@1.0.0",
        "config_id": config_id,
        "config_revision": 1,
        "config_purpose": "NONRESPONDENT_FIXTURE",
        "identity": {
            "source_id": series["source_id"],
            "family": series["family"],
            "wave": series["wave"],
            "source_family_id": f"PYAT1007_TEST_ONLY_{series['source_family_id']}",
            "study_product_id": f"{TEST_ONLY}:{series['source_id']}:study",
            "release_id": fixture_release_id,
            "instrument_release_id": f"{TEST_ONLY}:{series['source_id']}:instrument",
            "source_artifact_id": f"{TEST_ONLY}_{series['source_id']}_CELLS.{source_format}",
            "expected_source_sha256": original_identity_sha,
            "source_format": source_format,
            "source_row_count": row_count,
            "source_column_count": len(physical_slots),
            "source_bytes": source_bytes,
            "codebook_rows": len(items),
            "original_item_count": len(items),
            "source_snapshot_retention_ref": {
                "kind": "SOURCE_SNAPSHOT",
                "object_id": f"urn:rawlsing:pyat1007:test:{spec.series_key}:original-identity-not-read",
                "content_hash": original_identity_sha,
            },
            "metadata_witness_ref": {
                "kind": "R154_PHYSICAL_METADATA",
                "object_id": (
                    f"urn:rawlsing:pyat1007:test:{spec.series_key}:r157-metadata:"
                    f"{series['config_blob_sha256']}"
                ),
                "content_hash": series["config_blob_sha256"],
            },
            "locator": {
                "root": "EXTERNAL_LOCATOR_ID",
                "locator_id": f"PYAT1007_TEST_ONLY_{series['source_id']}_NO_ORIGINAL_LOCATOR",
            },
            "reader": {
                "decoder_owner": (
                    "rawlsing_next.pre553_physical_decoder.decode_sav"
                    if source_format == "SAV"
                    else "rawlsing_next.pre553_physical_decoder.decode_dta"
                ),
                "configuration_ref": ref(
                    "READER_CONFIGURATION",
                    f"urn:rawlsing:pyat1007:test:{spec.series_key}:reader",
                ).as_dict(),
                "encoding": None,
            },
        },
        "binding": {
            "identity_class": "NONRESPONDENT_FIXTURE",
            "source_sha256": active_source_sha256,
            "row_count": row_count,
            "source_snapshot_ref": {
                "kind": "FIXTURE_SNAPSHOT",
                "object_id": (
                    f"urn:rawlsing:pyat1007:test:{spec.series_key}:fixture-snapshot:"
                    f"{active_source_sha256}"
                ),
                "content_hash": active_source_sha256,
            },
            "fixture_provenance": {
                "fixture_id": fixture_id,
                "provenance": (
                    "PYAT1007 repository-generated nonrespondent TEST_ONLY cells; "
                    "R157 semantic metadata only, no original respondent bytes or rights."
                ),
                "authority_grade": "NONRESPONDENT_FIXTURE_ONLY",
                "original_source_id": series["source_id"],
                "original_source_sha256": original_identity_sha,
                "no_original_respondents": True,
                "fixture_study_product_id": f"{TEST_ONLY}:{series['source_id']}:study",
                "fixture_release_id": fixture_release_id,
                "fixture_instrument_release_id": f"{TEST_ONLY}:{series['source_id']}:instrument",
            },
        },
        "authority": {
            "snapshots": snapshots,
            "required_refs": [
                source_auth, mapping_auth, topology_auth, coord_auth,
                routing_auth, replay_auth, projection_auth,
            ],
            "projection_authority_ref": projection_auth,
            "replay_authority_ref": replay_auth,
            "projection_identity_ref": ref(
                "C11_PROJECTION", f"urn:rawlsing:pyat1007:test:{spec.series_key}:projection"
            ).as_dict(),
            "tie_order_ref": ref(
                "TIE_ORDER", f"urn:rawlsing:pyat1007:test:{spec.series_key}:tie-order"
            ).as_dict(),
            "replay_protocol_version": "PYAT1007_REPLAY_TEST@1",
        },
        "universe": {"universes": [universe_payload]},
        "respondents": respondents,
        "questions": questions,
        "physical_slots": physical_slots,
        "items": items,
        "response_slots": response_slots,
        "coordinate_slots": coordinate_slots,
        "weight_slots": [],
        "routing": routing,
        "source_relations": {"typed_absence_state": "DISTINCT_BY_DEFAULT"},
        "replay": {
            "predicate": _typed_absence("NOT_APPLICABLE"),
            "comparator": _typed_absence("DEFERRED"),
            "discovery": _typed_absence("DEFERRED"),
            "structural": _typed_absence("NOT_APPLICABLE"),
        },
        "supported_scope": {
            "scope_id": f"PYAT1007-{spec.series_key}-TEST-SCOPE",
            "purpose": "NONRESPONDENT_FIXTURE_VALIDATION",
            "declared_supported": True,
            "supported_question_ids": list(response_variables),
            "native_validation_expectation": "POSITIVE_RELEASE",
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "notes": [
                "TEST_ONLY fixture; not original respondent execution.",
                "Routing eligibility is fixture semantics, not R157 administration.",
            ],
        },
        "coverage": {
            "physical_slots_total": len(physical_slots),
            "items_total": len(items),
            "partial_scope_reason": "Compact nonrespondent TEST_ONLY witness of selected R157 metadata.",
            "not_a_lane_config": True,
        },
        "residuals": [],
        "evidence": {
            "source_roster_path": "WORKER_RETURNS/PYAT1007_DUAL_SERIES_PREP_R1/metadata/R157_METADATA_GROUNDING.json",
            "item_index_path": "WORKER_RETURNS/PYAT1007_DUAL_SERIES_PREP_R1/metadata/R157_METADATA_GROUNDING.json",
            "evidence_manifest_path": "WORKER_RETURNS/PYAT1007_DUAL_SERIES_PREP_R1/metadata/R157_METADATA_GROUNDING.json",
            "pinned_inputs": [
                {
                    "kind": "R157_SOURCE_CONFIG_METADATA_BLOB",
                    "sha256": series["config_blob_sha256"],
                    "commit": R157_COMMIT,
                    "path": series["config_path"],
                    "bytes": series["config_blob_bytes"],
                }
            ],
            "field_evidence": [
                {
                    "field": name,
                    "refs": [
                        ref(
                            "R157_PHYSICAL_METADATA",
                            f"urn:rawlsing:r157:{series['config_path']}#{name}",
                            {"name": name, "config_sha256": series["config_blob_sha256"]},
                        ).as_dict()
                    ],
                }
                for name in ordered_physical
            ],
            "limits": [
                "No original respondent bytes, original source hash, wave translation, or rights.",
                "No scientific comparability, design issuer, weight authority, or population inference.",
            ],
        },
        "runtime": {
            "projection_builder": "rawlsing_next.pre553_r157_projection_adapter.build_governed_c11_projection",
            "release_builder": "rawlsing_next.pre553_r157_projection_adapter.build_validated_c11_release_from_config",
            "repository_builder": "rawlsing_next.pre553_r157_projection_adapter.build_source_backed_c11_repository_from_config",
            "native_owner": "rawlsing_next.pre553_source_backed_c11_facade.GovernedC11Projection",
            "native_validator_stream": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release_from_stream",
            "native_validator_incidence": "rawlsing_next.pre553_source_backed_c11_facade.build_validated_source_backed_c11_release",
            "source_read_owner": "rawlsing_next.pre553_r157_projection_adapter.decode_with_source_read_permission",
            "transport": ["ExactPhysicalCellStream", "PhysicalSourceIncidence"],
            "reader_encoding_transport": "PYAT1007_TEST_ONLY_FIXTURE_TRANSPORT",
        },
        "notes": [
            "TEST_ONLY nonrespondent fixture. Do not promote to original-source, scientific, rights, design, weight, or comparability acceptance.",
            f"Semantic metadata witness: R157 {R157_COMMIT} {series['config_path']} sha256={series['config_blob_sha256']}.",
            "Local physical ordinals compact selected variables; exact R157 ordinals are retained in the metadata witness.",
            "Routing eligibility/ranked occurrence overrides are typed fixture semantics, not R157 administration.",
            "Original respondent bytes/current permission are SOURCE_BYTES_UNAVAILABLE/SOURCE_PERMISSION_HELD.",
        ],
    }
    SourceConfig(document)
    return document


def fixture_rows(spec: SeriesFixtureSpec, metadata: Mapping[str, Any]) -> dict[str, list[Any]]:
    series = metadata["series"][spec.series_key]
    variables = series["selected_variables"]
    order = list(spec.coordinate_variables)
    if spec.key_variable is not None:
        order.append(spec.key_variable)
    order.extend(
        name for name in variables
        if name not in spec.coordinate_variables and name != spec.key_variable
    )
    row_count = len(next(iter(spec.rows.values())))
    for name, values in spec.rows.items():
        if len(values) != row_count:
            raise ValueError(f"{spec.series_key}: {name} row count mismatch")
    return {name: list(spec.rows[name]) for name in order}


def write_fixture_file(
    directory: Path,
    spec: SeriesFixtureSpec,
    metadata: Mapping[str, Any],
    *,
    source_format: str | None = None,
    values_override: Mapping[str, Sequence[Any]] | None = None,
) -> tuple[Path, str, int]:
    directory.mkdir(parents=True, exist_ok=True)
    series = metadata["series"][spec.series_key]
    source_format = source_format or series["source_format"]
    rows = fixture_rows(spec, metadata)
    if values_override:
        rows.update({name: list(values) for name, values in values_override.items()})
    frame = pd.DataFrame(rows)
    path = directory / f"{spec.series_key.lower()}_{source_format.lower()}_test_only.{source_format.lower()}"
    labels: dict[str, dict[Any, Any]] = {}
    for name in rows:
        variable = series["selected_variables"].get(name)
        if not variable:
            continue
        raw_labels = variable.get("value_labels")
        if not raw_labels:
            continue
        converted: dict[Any, Any] = {}
        for key, label in raw_labels.items():
            try:
                converted[float(key)] = label
            except (TypeError, ValueError):
                converted[key] = label
        labels[name] = converted
    if source_format == "SAV":
        pyreadstat.write_sav(frame, str(path), variable_value_labels=labels)
    elif source_format == "DTA":
        pyreadstat.write_dta(frame, str(path), variable_value_labels=labels)
    else:
        raise ValueError("source_format must be SAV or DTA")
    return path, sha256(path.read_bytes()).hexdigest(), len(frame)


@dataclass(frozen=True)
class PipelineResult:
    spec: SeriesFixtureSpec
    config: SourceConfig
    fixture_path: Path
    source_sha256: str
    incidence: Any
    projection: Any
    candidate: Any
    release: Any
    receipt: EstateReceipt
    root: Path
    row_native_keys: Mapping[int, Any] | None


def build_pipeline(
    directory: Path,
    spec: SeriesFixtureSpec,
    metadata: Mapping[str, Any],
    *,
    values_override: Mapping[str, Sequence[Any]] | None = None,
    estate_name: str | None = None,
) -> PipelineResult:
    directory = Path(directory).resolve()
    path, source_sha, row_count = write_fixture_file(
        directory, spec, metadata, values_override=values_override
    )
    series = metadata["series"][spec.series_key]
    config_document = build_fixture_config(
        metadata, spec,
        active_source_sha256=source_sha,
        row_count=row_count,
        source_bytes=path.stat().st_size,
        source_format=series["source_format"],
        config_id=f"PYAT1007-{spec.series_key}-TEST-{source_sha[:12]}",
        fixture_release_id=f"PYAT1007_{spec.series_key}_TEST_RELEASE",
    )
    config = SourceConfig(config_document)
    incidence = decode_fixture_config(config, path)
    keys = None
    if config_document["respondents"].get("source_native_key_slot") is not None:
        keys = row_native_keys_from_transport(config, incidence=incidence, batch_size=8)
    projection = build_governed_c11_projection(config, row_native_keys=keys)
    cells = tuple(incidence.iter_cells(8))
    candidate = project_c11_candidate_from_config(
        config,
        projection,
        cells=cells,
        row_native_keys=keys,
        source_sha256=incidence.source_sha256,
        row_count=incidence.row_count,
    )
    release = validate_c11_source_release(candidate)
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=projection.replay_authority_ref,
        deterministic_tie_order_rules_ref=projection.tie_order_ref,
        replay_protocol_version=projection.replay_protocol_version,
    )
    candidate = replace(candidate, candidate_replay_manifest=replay)
    sections = direct_sections_from_candidate(
        candidate,
        replay_protocol_authority_ref=projection.replay_authority_ref,
        replay_protocol_version=projection.replay_protocol_version,
        deterministic_tie_order_rules_ref=projection.tie_order_ref,
    )
    root = directory / (estate_name or f"estate_{spec.series_key.lower()}_{source_sha[:12]}")
    root.mkdir(mode=0o700, exist_ok=True)
    receipt = write_direct_estate(
        sections, projection.universes[0].ref, root, chunk_rows=2,
    )
    return PipelineResult(
        spec=spec,
        config=config,
        fixture_path=path,
        source_sha256=source_sha,
        incidence=incidence,
        projection=projection,
        candidate=candidate,
        release=release,
        receipt=receipt,
        root=root,
        row_native_keys=keys,
    )


def decoded_cell_manifest_sha256(result: PipelineResult) -> str:
    """Deterministic digest of decoded synthetic cells (independent of writer timestamps)."""
    rows = []
    for cell in result.incidence.iter_cells(64):
        rows.append({
            "row": cell.row_ordinal,
            "ordinal": cell.variable_ordinal,
            "name": cell.variable_name,
            "raw": repr(cell.raw_value),
            "missing_state": cell.missing_state.value,
            "declaration": repr(cell.source_missing_declaration),
        })
    rows.sort(key=lambda item: (item["row"], item["ordinal"], item["name"]))
    return sha256_text(json.dumps(rows, sort_keys=True, separators=(",", ":")))


def source_view(result: PipelineResult) -> dict[str, Any]:
    candidate = result.candidate
    qrefs = {
        binding.native_question_ref.object_id.rsplit(":", 1)[-1]: binding.native_question_ref
        for binding in candidate.question_variable_bindings
    }
    crefs = {
        exact_ref(fact.native_coordinate_ref).object_id.rsplit(":", 1)[-1]: exact_ref(
            fact.native_coordinate_ref
        )
        for fact in candidate.empirical_coordinate_facts
    }
    set_qrefs = {
        variable: qref for variable, qref in qrefs.items()
    }
    auth_by = {snapshot.authority_ref.authority_id: snapshot for snapshot in candidate.authority_snapshots}
    routing_by_target = {
        exact_ref(fact.question_or_target_ref).object_id.rsplit(":", 1)[-1]: fact
        for fact in candidate.routing_eligibility_facts_or_exact_rules
    }
    question_by_variable = {
        binding.native_question_ref.object_id.rsplit(":", 1)[-1]: binding
        for binding in candidate.question_variable_bindings
    }
    return {
        "universe": candidate.empirical_universes[0],
        "qrefs": set_qrefs,
        "crefs": crefs,
        "source_auth": auth_by[question_by_variable[
            result.spec.positive_questions[0]
            if result.spec.positive_questions else result.spec.route_unknown_questions[0]
        ].semantic_authority_ref.authority_id],
        "coord_auth": auth_by[
            candidate.empirical_coordinate_facts[0].source_semantic_authority_ref["authority_id"]
        ],
        "authorities": candidate.authority_snapshots,
        "respondents": {
            identity.respondent_key: identity for identity in candidate.respondent_identities
        },
        "risk_refs": {
            variable: exact_ref(fact.risk_set_ref)
            for variable, fact in routing_by_target.items()
        },
        "routing_by_target": routing_by_target,
        "question_by_variable": question_by_variable,
    }


def query_authority(series_key: str) -> AuthoritySnapshot:
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=ref(
            "REPLAY_ROOT", f"urn:rawlsing:pyat1007:test:{series_key}:query-authority:root"
        ),
        authority_id=f"PYAT1007-{series_key}-QUERY",
        authority_version="1.0.0",
        authority_content_hash=sha256_text(f"authority:PYAT1007-{series_key}-QUERY"),
        authority_kind="PREDICATE_GRAMMAR",
        decision_state="ALLOW",
        governed_operations=(f"PYAT1007-{series_key}-QUERY-OP",),
        governed_object_families=(
            "EmpiricalPredicate@1.0.0",
            "EmpiricalQuerySpec@1.0.0",
            "EmpiricalFact@1.0.0",
        ),
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="PYAT1007_TEST_ONLY",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=sha256_text(f"fp:PYAT1007-{series_key}-QUERY"),
        replay_protocol_ref=ref(
            "REPLAY_PROTOCOL", f"urn:rawlsing:pyat1007:test:{series_key}:query-authority:replay"
        ),
    )


def respondent_keys(result: PipelineResult, rows: Iterable[int]) -> tuple[str, ...]:
    return tuple(
        result.projection.respondents[row - 1].respondent_key
        for row in rows
    )


def build_branch_predicate(
    result: PipelineResult,
    view: Mapping[str, Any],
    qauth: AuthoritySnapshot,
    *,
    tag: str,
    member_keys: Iterable[str] | None = None,
) -> Any:
    if member_keys is None:
        members = tuple(view["respondents"].values())
    else:
        members = tuple(view["respondents"][key] for key in member_keys)
    refs = tuple(sorted((member.ref for member in members), key=lambda item: item.key))
    membership = ref(
        "BRANCH_MEMBERSHIP",
        f"urn:rawlsing:pyat1007:test:{result.spec.series_key}:branch:{tag}",
        [member.key for member in refs],
    )
    ast = {
        "op": "LEAF",
        "leaf_type": "DERIVED_BRANCH_COHORT",
        "branch_definition_id": f"PYAT1007-{result.spec.series_key}-{tag}",
        "resolved_predicate_hash_or_exact_membership_ref": membership.as_dict(),
        "parent_ancestry_ref": ref(
            "BRANCH_PARENT", f"urn:rawlsing:pyat1007:test:{result.spec.series_key}:branch-parent:{tag}"
        ).as_dict(),
        "branch_algorithm_authority_ref": qauth.authority_ref.as_dict(),
        "branch_membership_replay_ref": ref(
            "BRANCH_REPLAY", f"urn:rawlsing:pyat1007:test:{result.spec.series_key}:branch-replay:{tag}"
        ).as_dict(),
        "branch_source_scope_ref": view["universe"].ref.as_dict(),
        "exact_member_respondent_refs": [member.as_dict() for member in refs],
    }
    return make_empirical_predicate(
        predicate_ast=ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(qauth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=ref(
            "REPLAY_ROOT", f"urn:rawlsing:pyat1007:test:{result.spec.series_key}:predicate:{tag}"
        ),
        grammar_authority_ref=qauth.authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=tuple(view["risk_refs"].values()),
        scope_refs=(view["universe"].ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )


def build_query(
    result: PipelineResult,
    view: Mapping[str, Any],
    qauth: AuthoritySnapshot,
    predicate: Any,
    targets: Sequence[str],
    *,
    domains: Mapping[str, Sequence[str]],
    measure: str = "RAW",
    tag: str,
    universe_refs: Sequence[ExactRef] | None = None,
) -> EmpiricalQuerySpec:
    if universe_refs is None:
        universe_refs = (view["universe"].ref,)
    risk_sets = {view["risk_refs"][target].key: view["risk_refs"][target] for target in targets}
    if len(risk_sets) != 1:
        raise ValueError("joint query targets do not share one exact risk set")
    risk_set_ref = next(iter(risk_sets.values()))
    components = []
    for target in targets:
        binding = view["question_by_variable"][target]
        components.append({
            "target_ref": view["qrefs"][target].as_dict(),
            "topology": "SCALAR_SINGULAR",
            "domain": list(domains[target]),
            "target_domain_replay_ref": ref(
                "TARGET_DOMAIN",
                f"urn:rawlsing:pyat1007:test:{result.spec.series_key}:domain:{target}",
                list(domains[target]),
            ).as_dict(),
            "topology_authority_refs": [binding.topology_authority_ref.as_dict()],
            "response_semantic_authority_refs": [binding.semantic_authority_ref.as_dict()],
            "included_states": ["SUBSTANTIVE_RESPONSE"],
        })
    grain = {
        "source_scope_mode": "SINGLE_UNIVERSE",
        "measure_kind": measure,
        "risk_set_type": (
            "COMMON_ELIGIBLE_RISK_SET" if len(targets) > 1
            else "WHOLE_QUESTION_RISK_SET"
        ),
        "response_state_semantics_ref": ref(
            "RESPONSE_STATE_SEMANTICS", "SUBSTANTIVE"
        ).as_dict(),
        "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
        "query_operation": f"PYAT1007-{result.spec.series_key}-QUERY-OP",
    }
    if measure == "GOVERNED_WEIGHTED":
        grain["weight_basis_id"] = "W"
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(qauth.authority_ref,),
        dependency_refs=(predicate.ref,),
        producer_replay_locator_or_reference_root=ref(
            "REPLAY_ROOT", f"urn:rawlsing:pyat1007:test:{result.spec.series_key}:query:{tag}"
        ),
        target_refs=tuple(view["qrefs"][target] for target in targets),
        target_arity_and_topology={
            "arity": len(targets),
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": components,
        },
        condition_predicate_ref=predicate.ref,
        risk_set_ref=risk_set_ref,
        empirical_universe_refs=tuple(universe_refs),
        scope_refs=tuple(universe_refs),
        measure_basis_ref=ref("MEASURE_BASIS", measure),
        requested_output_grain=grain,
        query_authority_refs=(qauth.authority_ref,),
    )


def catalog(
    result: PipelineResult,
    qauth: AuthoritySnapshot,
    predicates: Sequence[Any],
    queries: Sequence[Any],
    discovery_authorities: Sequence[Any] = (),
    extra_authorities: Sequence[Any] = (),
) -> RuntimeObjectCatalog:
    return RuntimeObjectCatalog(
        authorities=(
            tuple(result.candidate.authority_snapshots)
            + (qauth,)
            + tuple(extra_authorities)
        ),
        predicates=tuple(predicates),
        queries=tuple(queries),
        discovery_authorities=tuple(discovery_authorities),
    )


def admission(
    result: PipelineResult,
    runtime_catalog: RuntimeObjectCatalog,
    *,
    allow: bool = True,
    current_authorizer: Any | None = None,
) -> SavedC11Admission:
    return SavedC11Admission.open(
        root=result.root,
        exact_path=result.receipt.path,
        independently_held_manifest_sha256=result.receipt.manifest_sha256,
        independently_held_i02=result.receipt.i02,
        release_ref=result.receipt.reconstructed_v1_release_ref,
        runtime_catalog=runtime_catalog,
        current_authorizer=(
            current_authorizer
            if current_authorizer is not None
            else (lambda _roots: allow)
        ),
    )


def release_ref(result: PipelineResult) -> ExactRef:
    return result.receipt.reconstructed_v1_release_ref


def hold_result(spec: SeriesFixtureSpec, metadata: Mapping[str, Any]) -> dict[str, Any]:
    series = metadata["series"][spec.series_key]
    return {
        "series_key": spec.series_key,
        "source_id": series["source_id"],
        "family": series["family"],
        "wave": series["wave"],
        "source_format": series["source_format"],
        "fixture_id": spec.fixture_id,
        "original_source_bytes": "SOURCE_BYTES_UNAVAILABLE",
        "current_source_permission": "SOURCE_PERMISSION_HELD",
        "actual_source_native_pilot": "HOLD_DEPENDENCY",
        "fixture_grade": "NONRESPONDENT_FIXTURE_ONLY",
        "commercial_or_scientific_comparability": "NOT_CLAIMED",
        "design_issuer": "NOT_ISSUED",
        "weight_authority": "NOT_ISSUED",
    }


def duplicate_occurrence_sections(
    candidate: Any,
    projection: Any,
) -> SourcefreeDirectI02Sections:
    sections = direct_sections_from_candidate(
        candidate,
        replay_protocol_authority_ref=projection.replay_authority_ref,
        replay_protocol_version=projection.replay_protocol_version,
        deterministic_tie_order_rules_ref=projection.tie_order_ref,
    )
    events = tuple(candidate.respondent_events)
    if not events:
        raise ValueError("candidate has no events")
    first = events[0]
    fields = dict(first.semantic_fields)
    fields["response_topology_ref"] = ref(
        "RESPONSE_TOPOLOGY",
        "urn:rawlsing:pyat1007:test:duplicate-occurrence-witness",
    ).as_dict()
    duplicate = RespondentEvent(
        typed_state=first.typed_state,
        authority_snapshot_refs=first.authority_snapshot_refs,
        dependency_refs=first.dependency_refs,
        producer_replay_locator_or_reference_root=(
            first.producer_replay_locator_or_reference_root
        ),
        **fields,
    )
    replacement = {
        family: iter(values) for family, values in sections.sections.items()
    }
    replacement["RespondentEvent"] = iter((*events, duplicate))
    return SourcefreeDirectI02Sections(
        manifest=sections.manifest,
        sections=MappingProxyType(replacement),
        typed_absences=sections.typed_absences,
        replay_protocol_authority_ref=sections.replay_protocol_authority_ref,
        replay_protocol_version=sections.replay_protocol_version,
        deterministic_tie_order_rules_ref=sections.deterministic_tie_order_rules_ref,
    )


__all__ = [
    "METADATA_PATH",
    "PipelineResult",
    "SERIES_SPECS",
    "SeriesFixtureSpec",
    "TEST_ONLY",
    "admission",
    "build_branch_predicate",
    "build_fixture_config",
    "build_pipeline",
    "build_query",
    "catalog",
    "decoded_cell_manifest_sha256",
    "duplicate_occurrence_sections",
    "fixture_rows",
    "hold_result",
    "load_metadata",
    "query_authority",
    "release_ref",
    "source_view",
    "write_fixture_file",
]
