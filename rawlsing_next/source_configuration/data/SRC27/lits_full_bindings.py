"""Full LITS source-binding expansion for SRC27..SRC30.

The first pass (``lits_lane_build.py``) produced the source configs and
nonrespondent fixtures for a small canary slice.  HQ correctly rejected a
canary-only declaration: all response-bound source items must be bound with
their exact value/topology rules, while genuinely unavailable items carry an
exact native field + source-fact premise rather than an "outside slice" label.

This generator consumes the same frozen portable evidence and the baseline
helpers.  It:
  * binds every response-bound item with finite source value labels;
  * binds source geographic/administrative coordinates by raw copy;
  * serializes every response-bound item's routing explicitly (ELIGIBLE,
    NOT_ASKED for administrative routes, or ROUTING_UNKNOWN where the exact
    O06 clause is absent);
  * keeps response-authority-gap items, weights and native keys as exact
    field-level holds;
  * accounts every original item and physical slot in coverage;
  * derives the separate nonrespondent fixture config from the selected
    source rules, preserving fixture-only identity and the P3 keyed path.
"""
from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

import lits_lane_build as base

ROOT = base.ROOT
DATA_ROOT = base.DATA_ROOT
VALIDATION_ROOT = base.VALIDATION_ROOT

COORDINATE_KINDS = {
    "country": "SOURCE_COUNTRY_COORDINATE__RAW_CODE_OR_STRING",
    "region": "SOURCE_REGION_COORDINATE__RAW_CODE",
    "region_name": "SOURCE_REGION_COORDINATE__RAW_NAME",
    "city": "SOURCE_CITY_COORDINATE__RAW_CODE",
    "psu": "SOURCE_PSU_COORDINATE__RAW_CODE",
    "PSU_number": "SOURCE_PSU_COORDINATE__RAW_CODE",
    "urban": "SOURCE_URBANITY_COORDINATE__RAW_CODE",
}


def _coordinate_kind(recipe: Mapping[str, Any], var: str) -> str:
    if var == recipe["country_slot"]:
        return COORDINATE_KINDS["country"]
    return COORDINATE_KINDS.get(var, "SOURCE_ADMIN_COORDINATE__RAW_VALUE")


def _coordinate_unit(recipe: Mapping[str, Any], var: str) -> str:
    if var == recipe["country_slot"]:
        return recipe["country_kind"]
    if var in {"urban"}:
        return "SOURCE_URBANITY_CODE_DOMAIN"
    if var in {"psu", "PSU_number"}:
        return "SOURCE_PSU_CODE__UNIT_NOT_RETAINED"
    if var in {"region", "region_name"}:
        return "SOURCE_REGION_CODE_OR_NAME__UNIT_NOT_RETAINED"
    if var in {"city"}:
        return "SOURCE_CITY_CODE__UNIT_NOT_RETAINED"
    return "SOURCE_NATIVE_ADMIN_CODE__UNIT_NOT_RETAINED"


def _plan(
    source_id: str,
    recipe: Mapping[str, Any],
    slots: Sequence[Mapping[str, Any]],
    items: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    response_targets: list[dict[str, Any]] = []
    coordinate_targets: list[dict[str, Any]] = []
    blocked_vars: list[str] = []
    weight_vars: list[str] = []
    key_var = recipe["key_slot"]
    coordinate_vars = set(recipe.get("coordinate_vars") or [recipe["country_slot"]])
    weight_set = set(recipe.get("weight_vars") or [])
    for slot in slots:
        var = slot["name"]
        item = items[var]
        if var == key_var:
            continue
        if var in weight_set:
            weight_vars.append(var)
            continue
        if var in coordinate_vars:
            coordinate_targets.append(
                {
                    "var": var,
                    "question_id": None,
                    "role": "coordinate",
                    "coordinate_kind": _coordinate_kind(recipe, var),
                    "unit_taxonomy": _coordinate_unit(recipe, var),
                }
            )
            continue
        if item["p2"].get("response_binding_status") == "bound" and slot.get("value_labels"):
            response_targets.append(base._target_for_item(source_id, slot, item))
            continue
        blocked_vars.append(var)
    return {
        "response_targets": response_targets,
        "coordinate_targets": coordinate_targets,
        "blocked_vars": blocked_vars,
        "weight_vars": weight_vars,
        "key_var": key_var,
    }


def _dispositions(
    plan: Mapping[str, Any],
    items: Mapping[str, Mapping[str, Any]],
) -> dict[str, tuple[str, str | None]]:
    response_vars = {target["var"] for target in plan["response_targets"]}
    coordinate_vars = {target["var"] for target in plan["coordinate_targets"]}
    weight_vars = set(plan["weight_vars"])
    blocked_vars = set(plan["blocked_vars"])
    key_var = plan["key_var"]
    result: dict[str, tuple[str, str | None]] = {}
    for var in items:
        if var in response_vars:
            target = next(t for t in plan["response_targets"] if t["var"] == var)
            disposition = (
                "INCLUDED_REPEATED_RESPONSE_SLOT"
                if target["role"] == "repeated_response"
                else "INCLUDED_RESPONSE_SLOT"
            )
            result[var] = (disposition, None)
        elif var in coordinate_vars:
            result[var] = ("INCLUDED_COORDINATE_SLOT", None)
        elif var == key_var:
            result[var] = (
                "SOURCE_NATIVE_KEY_SLOT_HELD_UNTIL_DECODE",
                "Identified source-native key slot; no permitted decoded row witness exists "
                "under R157 preparation, and the corrected P0 factory refuses a configured "
                "source_native_key_slot without exact row keys. The fixture config exercises "
                "the P3 keyed path only with fixture-scoped key cells.",
            )
        elif var in weight_vars:
            result[var] = (
                "WEIGHT_HELD_NO_DESIGN_AUTHORITY",
                "Source weight slot/label is present, but exact design basis, normalization, "
                "population/estimand and weighted-use authority are not retained; no implicit "
                "unit weight or population claim is configured.",
            )
        elif var in blocked_vars:
            result[var] = (
                "HELD_RESPONSE_AUTHORITY_GAP",
                "P2 response_binding_status=blocked_response_authority_gap for this item; "
                "the exact P2/H48/full-relation evidence is retained but no response value "
                "or semantic authority is invented.",
            )
        else:
            result[var] = (
                "HELD_UNCLASSIFIED_ACCOUNTED",
                "Item is serialized and accounted but no native binding path is asserted.",
            )
    return result


def _routing_state(target: Mapping[str, Any]) -> str:
    status = target.get("routing_status") or "NOT_STATED"
    if status == "UNCONDITIONAL_SOURCE_PROVEN":
        return "ELIGIBLE_APPLICABLE"
    if status == "ADMIN_OR_NONRESPONDENT":
        return "NOT_ASKED"
    return "ROUTING_UNKNOWN"


def _routing_counts(targets: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(t["routing_status"] for t in targets).items()))


def _full_residuals(
    *,
    source_id: str,
    recipe: Mapping[str, Any],
    plan: Mapping[str, Any],
    item_count: int,
    slot_count: int,
) -> list[dict[str, Any]]:
    response_targets = plan["response_targets"]
    blocked_vars = plan["blocked_vars"]
    coordinate_targets = plan["coordinate_targets"]
    routing_counts = _routing_counts(response_targets)
    unknown_targets = [
        t for t in response_targets
        if t["routing_status"] not in {"UNCONDITIONAL_SOURCE_PROVEN", "ADMIN_OR_NONRESPONDENT"}
    ]
    admin_targets = [
        t for t in response_targets
        if t["routing_status"] == "ADMIN_OR_NONRESPONDENT"
    ]
    residuals: list[dict[str, Any]] = []
    if unknown_targets:
        residuals.append(
            {
                "residual_id": f"{source_id}-ROUTING-UNKNOWN-GROUP",
                "scope": (
                    f"{source_id}:{len(unknown_targets)} response-bound items; "
                    f"status_counts={json.dumps(_routing_counts(unknown_targets), sort_keys=True)}"
                ),
                "field": "routing.typed_state",
                "status": "SCOPED_UNKNOWN",
                "reason": (
                    "The exact O06_ROUTING_CLAUSES_NAMESPACED route expression is not retained "
                    "in the materialized evidence for these bound items. Their routing facts are "
                    "serialized with typed ROUTING_UNKNOWN and row_selector ALL, not as a false "
                    "unconditional eligibility claim. Full implementation IDs and statuses are "
                    "in the source item_accounting ledger."
                ),
                "dependent_operation": (
                    "native respondent eligibility / risk-set projection for these items"
                ),
                "unaffected_scope": (
                    f"{len(response_targets) - len(unknown_targets)} fully unconditional or "
                    "administrative-routed response bindings and the representative nonrespondent "
                    "native fixture"
                ),
                "owner": "R157 LITS lane author; H48 route-clause acquisition",
                "next_step": (
                    "Read the exact O06 routing-clause row for each implementation ID, or the "
                    "official source questionnaire route, and replace ROUTING_UNKNOWN with the "
                    "exact predicate/row selector before claiming original eligibility."
                ),
            }
        )
    if admin_targets:
        residuals.append(
            {
                "residual_id": f"{source_id}-ADMIN-ROUTE-GROUP",
                "scope": (
                    f"{source_id}:{len(admin_targets)} response-bound items with "
                    "routing_status=ADMIN_OR_NONRESPONDENT"
                ),
                "field": "routing.typed_state",
                "status": "SCOPED_BOUND",
                "reason": (
                    "The H48 routing row identifies an administrative/nonrespondent route rather "
                    "than a respondent-asked route. The observed categorical values are bound as "
                    "response events with routing typed NOT_ASKED; this is not a claim that a "
                    "respondent was eligible or asked."
                ),
                "dependent_operation": "respondent eligibility or administration-conditioned inference",
                "unaffected_scope": "observed administrative/context value witnesses",
                "owner": "R157 LITS lane author",
                "next_step": (
                    "If an administration-conditioned operation is needed, recover the exact "
                    "administrative route and represent it as a separate explicit administration "
                    "slice; do not reinterpret NOT_ASKED as a respondent answer route."
                ),
            }
        )
    if blocked_vars:
        residuals.append(
            {
                "residual_id": f"{source_id}-RESPONSE-AUTHORITY-GAP-GROUP",
                "scope": (
                    f"{source_id}:{len(blocked_vars)} items with exact "
                    "P2 response_binding_status=blocked_response_authority_gap"
                ),
                "field": "question.semantic_authority_ref and response_slot.value_rule",
                "status": "HELD",
                "reason": (
                    "The P2 implementation identity records an explicit response-authority gap "
                    "for these items; the physical/codebook identity is retained, but no "
                    "response value rule or semantic authority is invented. Full implementation "
                    "IDs and exact P2/H48/relation evidence are in the item_accounting ledger."
                ),
                "dependent_operation": "native response-event projection for these items",
                "unaffected_scope": (
                    f"{len(response_targets)} response-bound items, {len(coordinate_targets)} "
                    "raw coordinates and all inventory accounting"
                ),
                "owner": "R157 LITS lane author; P2/source authority owner",
                "next_step": (
                    "Resolve the exact response authority gap for each implementation ID, then "
                    "declare its value/state/topology rules; do not infer a value domain from "
                    "labels or frequencies."
                ),
            }
        )
    residuals.append(
        {
            "residual_id": f"{source_id}-WEIGHTS-DESIGN-AUTHORITY",
            "scope": f"{source_id}:weight_slots {plan['weight_vars']}",
            "field": "weight_basis_design_and_estimand_authority",
            "status": "SCOPED_UNKNOWN",
            "reason": (
                "Source weight slots and labels are present, but the exact design basis, "
                "normalization, population/estimand and authorization for weighted use are not "
                "retained in the materialized evidence."
            ),
            "dependent_operation": "weighted native projection or population claim",
            "unaffected_scope": "declared unweighted raw-sample bindings",
            "owner": "R157 LITS lane author; source design documentation acquisition",
            "next_step": (
                "Acquire the exact LiTS design/weight documentation and an authority record, then "
                "declare a separate weighted scope; do not default a weight or population."
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
                "Administration indicators and respondent-block variables are present, but the "
                "exact form/ballot assignment or section-order semantics are not retained; no "
                "DEFAULT_FORM or administered=True is asserted."
            ),
            "dependent_operation": "form-conditioned or administration-stratified native projection",
            "unaffected_scope": recipe["form_slice"],
            "owner": "R157 LITS lane author; source questionnaire/codebook acquisition",
            "next_step": (
                "Recover the exact source form/administration mapping and encode it as an explicit "
                "form slice before using it for conditioning."
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
                "P0/P3 factory refuses a configured source_native_key_slot without exact row "
                "keys; the nonrespondent fixture config demonstrates the keyed path separately."
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
    residuals.append(
        {
            "residual_id": f"{source_id}-COUNTRY-SET",
            "scope": f"{source_id}:{recipe['country_slot']}",
            "field": "country_geography/sampled_country_set",
            "status": "SCOPED_UNKNOWN",
            "reason": (
                "The source country slot is bound as a raw coordinate, but retained metadata does "
                "not enumerate the sampled country set or the population frame for this wave."
            ),
            "dependent_operation": "country-stratified query, population claim or cross-wave composition",
            "unaffected_scope": "raw country coordinate copy and all response bindings",
            "owner": "R157 LITS lane author; source frame/country-list acquisition",
            "next_step": (
                "Recover the exact sampled-country list and frame from the source manual or "
                "fieldwork documentation; keep the raw coordinate untouched."
            ),
        }
    )
    if len(coordinate_targets) > 1:
        residuals.append(
            {
                "residual_id": f"{source_id}-COORDINATE-UNIT-DEFINITIONS",
                "scope": (
                    f"{source_id}:{len(coordinate_targets)} raw source coordinates "
                    "[country/region/city/PSU/urban as present]"
                ),
                "field": "coordinate.unit_taxonomy",
                "status": "SCOPED_UNKNOWN",
                "reason": (
                    "Administrative/geographic coordinates are copied only as observed raw source "
                    "codes or names. The retained metadata does not fully define region/city/PSU "
                    "boundaries, comparability, or the unit hierarchy; no crosswalk or geographic "
                    "aggregation is asserted."
                ),
                "dependent_operation": "geographic aggregation, population claim or cross-wave geography",
                "unaffected_scope": "raw coordinate value witnesses and all response bindings",
                "owner": "R157 LITS lane author; source geography documentation acquisition",
                "next_step": (
                    "Recover the exact geographic unit definitions and frame before aggregation; "
                    "do not infer boundaries from labels."
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
    supported_count = sum(
        1 for t in response_targets
        if t["routing_status"] in {"UNCONDITIONAL_SOURCE_PROVEN", "ADMIN_OR_NONRESPONDENT"}
    )
    residuals.append(
        {
            "residual_id": f"{source_id}-FIXTURE-FULL-SUPPORTED-SCOPE",
            "scope": (
                f"{source_id}: full declared supported scope; {supported_count} supported "
                f"questions and all declared coordinate shapes; source config has {item_count} "
                f"items and {slot_count} physical slots"
            ),
            "field": "native_validation.harness_scope",
            "status": "SCOPED_HARNESS",
            "reason": (
                "The full supported nonrespondent fixture covers every declared supported "
                "question and coordinate shape. Prepared routing-unknown and response-authority-"
                "gap items remain outside the declared supported scope with their exact source "
                "premises; they are not a generic representative remainder and are not claimed "
                "as fixture-validated. The full source config still serializes and accounts them."
            ),
            "dependent_operation": "adding routing-unknown or response-gap items to supported scope",
            "unaffected_scope": "the full declared supported nonrespondent scope and all accounting",
            "owner": "R157 integration owner / final all35 validation",
            "next_step": (
                "Resolve the exact O06 routing clause or P2 response authority for a prepared item "
                "before adding it to the supported scope; do not alter source rules or invent "
                "fixture-only authority."
            ),
        }
    )
    return residuals


def _build_original_with_codebook(
    *,
    source_id: str,
    recipe: Mapping[str, Any],
    roster: Mapping[str, Any],
    slots: Sequence[Mapping[str, Any]],
    items: Mapping[str, Mapping[str, Any]],
    codebook: Mapping[str, Mapping[str, Any]],
    plan: Mapping[str, Any],
    dispositions: Mapping[str, tuple[str, str | None]],
    authority: Mapping[str, Any],
) -> dict[str, Any]:
    universe_payload, universe = base._universe_payload(
        source_id=source_id,
        recipe=recipe,
        roster=roster,
        authority=authority,
        fixture=False,
        fixture_sha=None,
    )
    response_targets = plan["response_targets"]
    coordinate_targets = plan["coordinate_targets"]
    questions: list[dict[str, Any]] = []
    response_slots: list[dict[str, Any]] = []
    for target in response_targets:
        slot = next(s for s in slots if s["name"] == target["var"])
        item = items[target["var"]]
        occurrence = base._occurrence(source_id=source_id, target=target)
        questions.append(
            base._question_payload(
                source_id=source_id,
                recipe=recipe,
                target=target,
                roster=roster,
                item=item,
                slot=slot,
                universe=universe,
                authority=authority,
                fixture=False,
            )
        )
        response_slots.append(
            {
                "slot": {"ordinal": slot["ordinal"], "name": slot["name"]},
                "question_id": target["question_id"],
                "values": base._response_values_for_original(
                    slot=slot,
                    target=target,
                    authority=authority,
                    occurrence=occurrence,
                ),
            }
        )
    coordinate_slots = []
    for target in coordinate_targets:
        slot = next(s for s in slots if s["name"] == target["var"])
        coordinate_slots.append(
            base._coordinate_slot(
                source_id=source_id,
                recipe=recipe,
                slot=slot,
                authority=authority,
                fixture=False,
                coordinate_kind=target["coordinate_kind"],
                unit_taxonomy=target["unit_taxonomy"],
            )
        )
    physical_payload = [
        base._physical_slot_payload(
            slot=slot,
            item=items[slot["name"]],
            included=True,
            target=None,
            disposition_override=dispositions[slot["name"]][0],
            disposition_reason_override=dispositions[slot["name"]][1],
        )
        for slot in slots
    ]
    response_var_set = {target["var"] for target in response_targets}
    item_payload = []
    for slot in slots:
        var = slot["name"]
        target = next((t for t in response_targets if t["var"] == var), None)
        item_payload.append(
            base._item_payload(
                slot=slot,
                item=items[var],
                codebook=codebook[var],
                included=True,
                target=target,
                source_id=source_id,
                metadata_sha=roster["metadata_witness"]["sha256"],
                disposition_override=dispositions[var][0],
                include_relation=(var in response_var_set),
            )
        )
    routing = base._routing_rules(
        source_id=source_id,
        targets=response_targets,
        authority=authority,
        fixture=False,
    )
    residuals = _full_residuals(
        source_id=source_id,
        recipe=recipe,
        plan=plan,
        item_count=len(slots),
        slot_count=len(slots),
    )
    included_ordinals = [slot["ordinal"] for slot in slots]
    included_ids = [items[slot["name"]]["implementation_id"] for slot in slots]
    config = {
        "schema": base.SCHEMA_ID,
        "config_id": f"R157-LITS-{source_id}-SOURCE-PREPARATION",
        "config_revision": 1,
        "config_purpose": "SOURCE_PREPARATION",
        "identity": {
            "source_id": source_id,
            "family": recipe["family"],
            "wave": recipe["wave"],
            "source_family_id": recipe["family"],
            "study_product_id": "LiTS",
            "release_id": recipe["release_id"],
            "instrument_release_id": (
                f"{source_id}_METADATA_WITNESS_SHA256:{roster['metadata_witness']['sha256']}"
            ),
            "source_artifact_id": recipe["artifact"],
            "expected_source_sha256": roster["source_sha256"],
            "source_format": "DTA",
            "source_row_count": roster["rows"],
            "source_column_count": roster["physical_columns"],
            "source_bytes": roster["bytes"],
            "codebook_rows": roster["codebook_rows"],
            "original_item_count": roster["original_items"],
            "source_snapshot_retention_ref": {
                "kind": "SOURCE_SNAPSHOT",
                "object_id": f"urn:rawlsing:r157:source-snapshot:{source_id}",
                "content_hash": roster["source_sha256"],
            },
            "metadata_witness_ref": {
                "kind": "R154_PHYSICAL_METADATA",
                "object_id": f"urn:rawlsing:r157:metadata:{roster['metadata_witness']['path']}",
                "content_hash": roster["metadata_witness"]["sha256"],
            },
            "locator": {
                "root": "EXTERNAL_LOCATOR_ID",
                "locator_id": f"{source_id}_ORIGINAL_SOURCE_EXTERNAL_RUNTIME_BINDING",
            },
            "reader": {
                "decoder_owner": base.READER_DECODER,
                "configuration_ref": base._reader_ref(source_id),
                "encoding": None,
            },
        },
        "binding": {
            "identity_class": "ORIGINAL_SOURCE",
            "source_sha256": roster["source_sha256"],
            "row_count": roster["rows"],
            "source_snapshot_ref": {
                "kind": "SOURCE_SNAPSHOT",
                "object_id": f"urn:rawlsing:r157:source-snapshot:{source_id}",
                "content_hash": roster["source_sha256"],
            },
        },
        "authority": {
            "snapshots": authority["snapshots"],
            "required_refs": authority["required_refs"],
            "projection_authority_ref": authority["projection_authority_ref"],
            "replay_authority_ref": authority["replay_authority_ref"],
            "projection_identity_ref": base._exact_ref(
                "PROJECTION_IDENTITY",
                f"urn:rawlsing:r157:projection:{source_id}:source:full",
                {
                    "source_id": source_id,
                    "source_sha256": roster["source_sha256"],
                    "response_items": len(response_targets),
                    "coordinates": len(coordinate_targets),
                },
            ),
            "tie_order_ref": base._exact_ref(
                "DETERMINISTIC_TIE_ORDER",
                f"urn:rawlsing:r157:tie-order:{source_id}:source:full",
                {"source_id": source_id, "order": "exact_ref_key"},
            ),
            "replay_protocol_version": "R157_SOURCE_CONFIGURATION@1.0.0",
        },
        "universe": {"universes": [universe_payload]},
        "respondents": base._respondents_section(
            source_id=source_id,
            recipe=recipe,
            slots=slots,
            universe_payload=universe_payload,
            fixture=False,
            key_slot_name=None,
        ),
        "questions": questions,
        "physical_slots": physical_payload,
        "items": item_payload,
        "response_slots": response_slots,
        "coordinate_slots": coordinate_slots,
        "weight_slots": [],
        "routing": routing,
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
            "scope_id": f"{source_id}_FULL_SOURCE_PREPARATION__KNOWN_ROUTING_SUPPORTED",
            "purpose": "SOURCE_PREPARATION",
            "declared_supported": True,
            "supported_question_ids": [
                t["question_id"] for t in response_targets
                if t["routing_status"] in {
                    "UNCONDITIONAL_SOURCE_PROVEN", "ADMIN_OR_NONRESPONDENT"
                }
            ],
            "native_validation_expectation": "NOT_RUN",
            "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
            "supported_unit_slice": recipe["subject_unit"],
            "supported_form_slice": recipe["form_slice"],
            "notes": [
                recipe["unit_notes"],
                (
                    f"All {len(response_targets)} response-bound items are serialized with "
                    "their exact source value, missing/special, topology and routing states. "
                    f"{sum(1 for t in response_targets if t['routing_status'] in {'UNCONDITIONAL_SOURCE_PROVEN','ADMIN_OR_NONRESPONDENT'})} "
                    "of them have a known unconditional or administrative routing state and are "
                    "declared supported; the remaining routing-unknown items are prepared bindings "
                    "outside the declared eligibility scope, not unselected items. Routing is "
                    "ROUTING_UNKNOWN where the exact O06 clause is absent and NOT_ASKED for "
                    "administrative/nonrespondent routes; neither is a false unconditional "
                    "eligibility claim."
                ),
                (
                    f"{len(plan['blocked_vars'])} items remain held only because P2 records an "
                    "exact response_binding_status=blocked_response_authority_gap; their full "
                    "identity/evidence is retained and they are not called unselected."
                ),
                (
                    "The full supported nonrespondent fixture config covers every declared "
                    "supported question and coordinate shape with the same source rules; "
                    "routing-unknown/response-gap prepared bindings remain outside supported "
                    "scope with exact residuals. Original source execution is not performed."
                ),
            ],
        },
        "coverage": {
            "physical_slots_total": roster["physical_columns"],
            "items_total": roster["original_items"],
            "physical_slots_included": included_ordinals,
            "physical_slots_excluded": [],
            "items_included": included_ids,
            "items_excluded": [],
            "partial_scope_reason": (
                "All original items and physical slots are serialized and accounted. Included "
                "means accounted in this source config; each item's disposition states whether "
                "it is a bound response/coordinate, a response-authority-gap hold, a native-key "
                "hold or a weight-design hold. Every item in the declared supported-question "
                "set and every declared coordinate shape is covered by the full supported "
                "nonrespondent fixture; routing-unknown/response-gap prepared bindings remain "
                "outside supported scope with exact residuals."
            ),
        },
        "residuals": residuals,
        "evidence": base._evidence_section(
            source_id=source_id,
            roster=roster,
            fixture=False,
            fixture_doc={},
            fixture_sha="",
        ),
        "runtime": {
            **base.RUNTIME,
            "transport": ["ExactPhysicalCellStream"],
            "reader_encoding_transport": (
                "P3_QUALIFIED_EXACT_SHA_READER_TRANSPORT__CONFIG_FACTS_AVAILABLE__NO_ORIGINAL_READ"
            ),
        },
        "notes": [
            (
                "ORIGINAL_SOURCE preparation config; original respondent execution and original "
                "workload issuance are NOT performed under R157."
            ),
            (
                "Every original item and physical slot is retained. Response-bound items carry "
                "exact value/state/topology/routing serialization; blocked items carry an exact "
                "P2 response-authority-gap premise, not an outside-slice label."
            ),
            (
                "No ALLOW original-source authority, default person/scalar, default form, "
                "implicit weight or synthetic universe is asserted."
            ),
            (
                "Coordinate normalization_ref is null because the frozen native canonicalizer "
                "does not accept a TypedAbsence there; no country/region/PSU crosswalk or "
                "canonical geography is asserted."
            ),
            (
                "The source-native key slot is inventoried but not configured because no "
                "permitted decoded row witness exists; row identity remains a replay ordinal. "
                "The nonrespondent fixture config exercises the P3 keyed path separately."
            ),
        ],
    }
    return config


def _replace_fixture_authorities(
    config: dict[str, Any],
    *,
    fixture_universe: Any,
    authority: Mapping[str, Any],
) -> None:
    semantic = base._authority_ref(authority["by_tag"]["SEMANTIC"])
    topology = base._authority_ref(authority["by_tag"]["TOPOLOGY"])
    mapping = base._authority_ref(authority["by_tag"]["MAPPING"])
    coordinate = base._authority_ref(authority["by_tag"]["COORDINATE"])
    routing = base._authority_ref(authority["by_tag"]["ROUTING"])
    for question in config["questions"]:
        question["empirical_universe_ref"] = fixture_universe.ref.as_dict()
        question["semantic_authority_ref"] = semantic
        question["topology_authority_ref"] = topology
        if isinstance(question.get("item_evidence"), dict):
            question["item_evidence"]["fixture_identity_class"] = "NONRESPONDENT_FIXTURE"
    for slot in config["response_slots"]:
        for value in slot["values"]:
            if value.get("transform_authority_ref") is not None:
                value["transform_authority_ref"] = mapping
    for slot in config["coordinate_slots"]:
        slot["source_semantic_authority_ref"] = coordinate
    for rule in config["routing"]:
        rule["authority_ref"] = routing


def _build_fixture_config(
    *,
    source_id: str,
    recipe: Mapping[str, Any],
    roster: Mapping[str, Any],
    slots: Sequence[Mapping[str, Any]],
    original: Mapping[str, Any],
    fixture_doc: Mapping[str, Any],
    fixture_sha: str,
    fixture_authority: Mapping[str, Any],
) -> dict[str, Any]:
    fixture_universe_payload, fixture_universe = base._universe_payload(
        source_id=source_id,
        recipe=recipe,
        roster=roster,
        authority=fixture_authority,
        fixture=True,
        fixture_sha=fixture_sha,
    )
    fixture_vars = {
        target["var"] for target in recipe["targets"] if target["role"] != "coordinate"
    } | {recipe["country_slot"]}
    config = copy.deepcopy(dict(original))
    config["config_id"] = f"R157-LITS-{source_id}-NONRESPONDENT-FIXTURE"
    config["config_purpose"] = "NONRESPONDENT_FIXTURE"
    config["binding"] = {
        "identity_class": "NONRESPONDENT_FIXTURE",
        "source_sha256": fixture_sha,
        "row_count": fixture_doc["row_count"],
        "source_snapshot_ref": {
            "kind": "FIXTURE_SNAPSHOT",
            "object_id": f"urn:rawlsing:r157:fixture:{fixture_doc['fixture_id']}",
            "content_hash": fixture_sha,
        },
        "fixture_provenance": {
            "fixture_id": fixture_doc["fixture_id"],
            "provenance": (
                "Repository-generated nonrespondent fixture for the R157 LITS lane; fixture "
                "values are declared source codes or explicit fixture-only strings; no original "
                "respondents represented."
            ),
            "authority_grade": "NONRESPONDENT_FIXTURE_ONLY",
            "original_source_id": source_id,
            "original_source_sha256": roster["source_sha256"],
            "no_original_respondents": True,
            "fixture_study_product_id": f"R157_FIXTURE/LiTS/{source_id}",
            "fixture_release_id": f"R157_FIXTURE_RELEASE/{source_id}",
            "fixture_instrument_release_id": f"R157_FIXTURE_INSTRUMENT/{source_id}",
        },
    }
    config["authority"] = {
        "snapshots": fixture_authority["snapshots"],
        "required_refs": fixture_authority["required_refs"],
        "projection_authority_ref": fixture_authority["projection_authority_ref"],
        "replay_authority_ref": fixture_authority["replay_authority_ref"],
        "projection_identity_ref": base._exact_ref(
            "PROJECTION_IDENTITY",
            f"urn:rawlsing:r157:projection:{source_id}:fixture",
            {
                "source_id": source_id,
                "fixture_id": fixture_doc["fixture_id"],
                "fixture_sha": fixture_sha,
                "selected_vars": sorted(fixture_vars),
            },
        ),
        "tie_order_ref": base._exact_ref(
            "DETERMINISTIC_TIE_ORDER",
            f"urn:rawlsing:r157:tie-order:{source_id}:fixture",
            {"source_id": source_id, "fixture": True, "order": "exact_ref_key"},
        ),
        "replay_protocol_version": "R157_SOURCE_CONFIGURATION@1.0.0",
    }
    config["universe"] = {"universes": [fixture_universe_payload]}
    config["respondents"] = base._respondents_section(
        source_id=source_id,
        recipe=recipe,
        slots=slots,
        universe_payload=fixture_universe_payload,
        fixture=True,
        key_slot_name=recipe["key_slot"],
    )
    config["questions"] = [
        q for q in config["questions"]
        if (q.get("item_evidence") or {}).get("source_variable_code") in fixture_vars
    ]
    fixture_qids = {q["question_id"] for q in config["questions"]}
    config["response_slots"] = [
        s for s in config["response_slots"] if s["slot"]["name"] in fixture_vars
    ]
    config["coordinate_slots"] = [
        s for s in config["coordinate_slots"] if s["slot"]["name"] == recipe["country_slot"]
    ]
    config["routing"] = [
        r for r in config["routing"] if r["question_id"] in fixture_qids
    ]
    _replace_fixture_authorities(
        config, fixture_universe=fixture_universe, authority=fixture_authority
    )
    # Mark the fixture key slot explicitly; all other item dispositions remain the
    # source inventory's exact dispositions.
    for slot in config["physical_slots"]:
        if slot["name"] == recipe["key_slot"]:
            slot["disposition"] = "INCLUDED_FIXTURE_KEY_SLOT"
            slot.pop("disposition_reason", None)
    for item in config["items"]:
        if item["source_variable_code"] == recipe["key_slot"]:
            item["disposition"] = "INCLUDED_FIXTURE_KEY_SLOT"
    config["weight_slots"] = []
    config["supported_scope"] = {
        "scope_id": f"{source_id}_NONRESPONDENT_FIXTURE_REPRESENTATIVE_SHAPES",
        "purpose": "NONRESPONDENT_FIXTURE_VALIDATION",
        "declared_supported": True,
        "supported_question_ids": sorted(fixture_qids),
        "native_validation_expectation": "POSITIVE_RELEASE",
        "original_source_execution": "NOT_PERFORMED_UNDER_R157_PREPARATION",
        "supported_unit_slice": "NONRESPONDENT_FIXTURE_HOUSEHOLD_ROW",
        "supported_form_slice": "NONRESPONDENT_FIXTURE_DECLARED_CELLS",
        "notes": [
            (
                "The fixture exercises representative LITS shapes (scalar/binary, "
                "repeated roster/respondent occurrences, raw country coordinate and the P3 "
                "fixture-scoped exact row key path)."
            ),
            (
                "Fixture-only authority is not original-source authority. The original config "
                "retains the full prepared binding scope and its exact residuals."
            ),
        ],
    }
    config["coverage"] = {
        "physical_slots_total": roster["physical_columns"],
        "items_total": roster["original_items"],
        "partial_scope_reason": (
            "Nonrespondent fixture exercises only the declared fixture slots and questions; "
            "all other source items remain serialized in this fixture config with their exact "
            "source dispositions. Fixture cells are not original respondents and do not "
            "complete the original config."
        ),
        "not_a_lane_config": True,
    }
    config["residuals"] = [
        {
            "residual_id": f"{source_id}-FIXTURE-ONLY-IDENTITY",
            "scope": f"{source_id}:{fixture_doc['fixture_id']}",
            "field": "identity_class_and_authority",
            "status": "FIXTURE_ONLY",
            "reason": (
                "This config deliberately binds a distinct nonrespondent fixture SHA and "
                "fixture-only authority; it is not an original-source config and cannot be "
                "promoted to original identity."
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
    config["evidence"] = base._evidence_section(
        source_id=source_id,
        roster=roster,
        fixture=True,
        fixture_doc=fixture_doc,
        fixture_sha=fixture_sha,
    )
    config["notes"] = [
        "NONRESPONDENT_FIXTURE config; distinct fixture byte identity and fixture-only authority.",
        (
            "The fixture config is a representative native-validation view of the same source "
            "rules; it does not replace the original source configuration."
        ),
        (
            "Fixture-scoped exact row keys are derived only from fixture key cells; they are "
            "not original respondent keys."
        ),
    ]
    return config


def build(source_id: str) -> dict[str, Any]:
    recipe = base.RECIPES[source_id]
    roster, slots, items, codebook, _ = base._source_data(source_id)
    plan = _plan(source_id, recipe, slots, items)
    dispositions = _dispositions(plan, items)
    metadata_sha = roster["metadata_witness"]["sha256"]

    fixture_doc = base._build_fixture_document(source_id, recipe, slots, items, roster)
    fixture_sha = fixture_doc["fixture_source_sha256"]
    original_authority = base._authority_set(
        source_id=source_id,
        source_sha=roster["source_sha256"],
        original_source_sha=roster["source_sha256"],
        wave=recipe["wave"],
        fixture=False,
        fixture_id=None,
        fixture_sha=None,
        selected_vars=sorted(
            {t["var"] for t in plan["response_targets"]}
            | {t["var"] for t in plan["coordinate_targets"]}
        ),
    )
    fixture_authority = base._authority_set(
        source_id=source_id,
        source_sha=fixture_sha,
        original_source_sha=roster["source_sha256"],
        wave=recipe["wave"],
        fixture=True,
        fixture_id=recipe["fixture"]["fixture_id"],
        fixture_sha=fixture_sha,
        selected_vars=sorted(
            {t["var"] for t in recipe["targets"] if t["role"] != "coordinate"}
            | {recipe["country_slot"]}
        ),
    )
    original = _build_original_with_codebook(
        source_id=source_id,
        recipe=recipe,
        roster=roster,
        slots=slots,
        items=items,
        codebook=codebook,
        plan=plan,
        dispositions=dispositions,
        authority=original_authority,
    )
    fixture_config = _build_fixture_config(
        source_id=source_id,
        recipe=recipe,
        roster=roster,
        slots=slots,
        original=original,
        fixture_doc=fixture_doc,
        fixture_sha=fixture_sha,
        fixture_authority=fixture_authority,
    )
    expected = base._expected_results(
        source_id, recipe, original, fixture_config, fixture_doc, fixture_sha
    )
    accounting = []
    response_vars = {t["var"] for t in plan["response_targets"]}
    coordinate_vars = {t["var"] for t in plan["coordinate_targets"]}
    for slot in slots:
        var = slot["name"]
        target = next((t for t in plan["response_targets"] if t["var"] == var), None)
        row = base._item_accounting_row(
            source_id=source_id,
            slot=slot,
            item=items[var],
            codebook=codebook[var],
            selected=(var in response_vars or var in coordinate_vars),
            target=target,
            metadata_sha=metadata_sha,
        )
        row["binding_disposition"] = dispositions[var][0]
        row["binding_reason"] = dispositions[var][1]
        row["response_bound"] = var in response_vars
        row["coordinate_bound"] = var in coordinate_vars
        row["key_slot_held"] = var == plan["key_var"]
        row["weight_held"] = var in set(plan["weight_vars"])
        row["routing_binding_state"] = (
            _routing_state(target) if target is not None else None
        )
        row["routing_status"] = (
            target["routing_status"] if target is not None else base._routing_status(items[var])
        )
        accounting.append(row)
    correspondence = base._correspondence(
        source_id,
        roster,
        slots,
        items,
        {t["var"]: t for t in plan["response_targets"] + plan["coordinate_targets"]},
    )
    correspondence.update(
        {
            "response_bound_items": len(plan["response_targets"]),
            "response_authority_gap_items": len(plan["blocked_vars"]),
            "coordinate_items": len(plan["coordinate_targets"]),
            "key_slot_held": plan["key_var"],
            "weight_held_items": len(plan["weight_vars"]),
            "routing_state_counts": _routing_counts(plan["response_targets"]),
            "all_items_serialized": True,
            "all_items_name_set_exact": True,
        }
    )
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
    base._write_json(original_path, original)
    base._write_jsonl(accounting_path, accounting)
    base._write_json(correspondence_path, correspondence)
    base._write_json(fixture_path, fixture_doc)
    base._write_json(fixture_config_path, fixture_config)
    base._write_json(expected_path, expected)
    return {
        "source_id": source_id,
        "original_path": original_path,
        "original_sha256": base._file_sha(original_path),
        "original_canonical_hash": base.canonical_config_hash(original),
        "fixture_path": fixture_path,
        "fixture_sha256": base._file_sha(fixture_path),
        "fixture_source_sha256": fixture_sha,
        "fixture_config_path": fixture_config_path,
        "fixture_config_sha256": base._file_sha(fixture_config_path),
        "fixture_config_canonical_hash": base.canonical_config_hash(fixture_config),
        "expected_path": expected_path,
        "expected_sha256": base._file_sha(expected_path),
        "accounting_path": accounting_path,
        "accounting_sha256": base._file_sha(accounting_path),
        "correspondence_path": correspondence_path,
        "correspondence_sha256": base._file_sha(correspondence_path),
        "response_bound": len(plan["response_targets"]),
        "response_authority_gap": len(plan["blocked_vars"]),
        "coordinate_bound": len(plan["coordinate_targets"]),
        "weight_held": len(plan["weight_vars"]),
        "routing_counts": _routing_counts(plan["response_targets"]),
        "physical_slots": len(slots),
        "items": len(items),
        "residuals": [r["residual_id"] for r in original["residuals"]],
    }


def main() -> int:
    results = [build(sid) for sid in ("SRC27", "SRC28", "SRC29", "SRC30")]
    manifest = {
        "schema": "PYAT_R157_LITS_FULL_BINDINGS_MANIFEST@1.0.0",
        "lane_id": "LITS",
        "plan_seal": base.PLAN_SEAL,
        "p0_dependency_commit": base.P0_DEPENDENCY_COMMIT,
        "p3_dependency_commit": "519355ec2215409b40d566ef13c3b21f611e0726",
        "lane_base_head": base.BASE_HEAD,
        "generated_by": (
            "rawlsing_next/source_configuration/data/SRC27/lits_full_bindings.py"
        ),
        "sources": [
            {
                **result,
                "original_path": str(result["original_path"].relative_to(ROOT)),
                "fixture_path": str(result["fixture_path"].relative_to(ROOT)),
                "fixture_config_path": str(result["fixture_config_path"].relative_to(ROOT)),
                "expected_path": str(result["expected_path"].relative_to(ROOT)),
                "accounting_path": str(result["accounting_path"].relative_to(ROOT)),
                "correspondence_path": str(result["correspondence_path"].relative_to(ROOT)),
            }
            for result in results
        ],
    }
    manifest_path = VALIDATION_ROOT / "SRC27" / "generated_manifest.json"
    base._write_json(manifest_path, manifest)
    print(json.dumps({"ok": True, "manifest": str(manifest_path.relative_to(ROOT)), "sources": manifest["sources"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
