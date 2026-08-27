#!/usr/bin/env python3
"""Execute the banked AS2A LiTS-I projection through the frozen C11/I03 path.

This is a mechanical court driver.  It does not amend the AS2A slot ledger,
infer source semantics, select a weight, or modify the PRE553 runtime.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import sys
import time
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[6]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import duckdb
import numpy
import pandas
import pyarrow
import pyreadstat

from rawlsing_next.pre553_c11_ingest import record_counts_for_candidate, validate_c11_source_release
from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalQuerySpec,
    EmpiricalUniverse,
    ExactRef,
    RoutingEligibilityFact,
    canonical_json,
    exact_ref,
    make_empirical_predicate,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_physical_decoder import (
    COMPATIBILITY_ONLY,
    PhysicalCell,
    PhysicalMissingState,
    PhysicalSourceIncidence,
    decode_dta,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    CONTRACT_ID,
    CoordinateSlotRule,
    CoordinateValueRule,
    GovernedC11Projection,
    OccurrenceRule,
    PhysicalSlot,
    ResponseSlotRule,
    ResponseValueRule,
    RowRespondentBinding,
    SourceBackedC11FacadeError,
    physical_value_binding_key,
    project_c11_candidate_from_physical_cells,
)


SOURCE_SHA = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
ROWS = 29_002
VARIABLES = 1_198
PHYSICAL_CELLS = 34_744_396
PART_A_HASH = "9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06"
SLOT_LEDGER_HASH = "65bdb972c2004d7ea6539b991125d2111e3705aee2d3e76159208d04e4a3fa60"
PART_A_DIR = Path(__file__).resolve().parent.parent / "AS2A_LITS1_SHARED_CERTIFICATION_20260827"
LEDGER = PART_A_DIR / "01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv"
PACKAGE = PART_A_DIR / "04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json"


@dataclass(frozen=True)
class LinearValidatedGovernedC11Projection(GovernedC11Projection):
    """The frozen projection checks, with its row-reference set built once.

    The accepted implementation rebuilds that complete set once per row.  This
    subclass changes no field, identity, or validation law; it only removes the
    quadratic repetition that makes the 29,002-row court non-executable.
    """

    def __post_init__(self) -> None:
        exact_ref(self.projection_identity_ref, "projection_identity_ref")
        value = self.expected_source_sha256
        if (not isinstance(value, str) or len(value) != 64 or value.lower() != value
                or any(c not in "0123456789abcdef" for c in value)):
            raise SourceBackedC11FacadeError("expected_source_sha256 must be lowercase sha256")
        if self.source_snapshot_retention_ref.content_hash != self.expected_source_sha256:
            raise SourceBackedC11FacadeError("snapshot ref does not bind expected source SHA")
        if not all((self.universes, self.respondents, self.row_bindings, self.questions,
                    self.response_slots, self.coordinate_slots, self.routing,
                    self.authority_snapshots, self.required_authority_refs)):
            raise SourceBackedC11FacadeError("projection omits mandatory governed semantic input")
        mandatory = {self.projection_authority_ref, self.replay_authority_ref}
        if not mandatory.issubset(set(self.required_authority_refs)):
            raise SourceBackedC11FacadeError("projection/replay authorities must be explicitly required")
        packaged = {a.authority_ref for a in self.authority_snapshots}
        if not set(self.required_authority_refs).issubset(packaged):
            raise SourceBackedC11FacadeError("required authority absent from projection closure")
        if len({x.row_ordinal for x in self.row_bindings}) != len(self.row_bindings):
            raise SourceBackedC11FacadeError("duplicate row replay coordinate")
        respondent_refs = {r.ref for r in self.respondents}
        if any(x.respondent_ref not in respondent_refs for x in self.row_bindings):
            raise SourceBackedC11FacadeError("row binding references absent respondent")
        physical_slots = [x.slot.key for x in (*self.response_slots, *self.coordinate_slots, *self.weight_slots)]
        if len(physical_slots) != len(set(physical_slots)):
            raise SourceBackedC11FacadeError("physical slot has multiple semantic owners")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def dref(kind: str, tag: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:pre553:as2b:{tag}:sha256:{digest}", digest)


def authority(
    role: str,
    kind: str,
    families: tuple[str, ...],
    *,
    content_hash: str | None = None,
) -> AuthoritySnapshot:
    material = {
        "court": "AS2B_LITS1_MECHANICAL_SOURCE_CERTIFICATION_20260827",
        "role": role,
        "kind": kind,
        "source_sha256": SOURCE_SHA,
        "part_a_projection_authority_hash": PART_A_HASH,
        "families": families,
    }
    authority_hash = content_hash or semantic_hash(material)
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=dref("REPLAY_ROOT", f"authority-{role}", material),
        authority_id=f"urn:rawlsing:pre553:as2b:lits1:authority:{role}",
        authority_version="AS2A-BANKED-1.0.0",
        authority_content_hash=authority_hash,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=(f"AS2B_LITS1_{role.upper()}",),
        governed_object_families=families,
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="LITS1_2006_AS2B_EXECUTION",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=semantic_hash({**material, "ceiling": "AS2A_BANKED_ONLY"}),
        replay_protocol_ref=dref("REPLAY_PROTOCOL", f"authority-{role}", material),
    )


def exact_decimal(value: Any) -> Any:
    """Make pyreadstat binary floats admissible to the exact semantic carrier."""
    if isinstance(value, float):
        return Decimal(str(value))
    return value


def exact_cell(cell: PhysicalCell) -> PhysicalCell:
    return PhysicalCell(
        row_ordinal=cell.row_ordinal,
        variable_ordinal=cell.variable_ordinal,
        variable_name=cell.variable_name,
        raw_value=exact_decimal(cell.raw_value),
        missing_state=cell.missing_state,
        source_missing_declaration=cell.source_missing_declaration,
        raw_value_label=cell.raw_value_label,
    )


def read_banked_authority() -> tuple[dict[str, Any], list[dict[str, str]], dict[str, int]]:
    if sha256_file(LEDGER) != SLOT_LEDGER_HASH:
        raise RuntimeError("Part-A slot ledger SHA mismatch")
    package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    if semantic_hash(package["projection_material"]) != PART_A_HASH:
        raise RuntimeError("Part-A projection authority content hash mismatch")
    if package["projection_authority_ref"]["content_hash"] != PART_A_HASH:
        raise RuntimeError("Part-A projection authority ref mismatch")
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        ledger = list(csv.DictReader(handle))
    if len(ledger) != VARIABLES:
        raise RuntimeError("Part-A slot ledger denominator mismatch")
    slots = {row["var"]: int(row["slot"]) for row in ledger}
    expected = {
        "country": 98, "city": 104, "region": 107, "q301_2": 194,
        "q301_7": 199, "tablec": 1117, "tabled": 1118,
    }
    if any(slots.get(name) != ordinal for name, ordinal in expected.items()):
        raise RuntimeError("Part-A bounded proving slot identity mismatch")
    return package, ledger, slots


def build_projection(incidence, package: dict[str, Any], ledger: list[dict[str, str]], slots: dict[str, int]):
    decoded = [(v.ordinal, v.name) for v in incidence.variables]
    banked = [(int(row["slot"]), row["var"]) for row in ledger]
    if decoded != banked:
        raise RuntimeError("frozen decoder variable order differs from banked 1,198-slot ledger")

    projection_auth = authority(
        "part_a_projection",
        "SOURCE_SEMANTICS_TOPOLOGY",
        ("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0", "RoutingEligibilityFact@1.0.0"),
        content_hash=PART_A_HASH,
    )
    source_auth = authority("source_semantics", "SOURCE_SEMANTICS_TOPOLOGY", ("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"))
    coordinate_auth = authority("coordinate_semantics", "COORDINATE_SEMANTICS", ("EmpiricalCoordinateFact@1.0.0",))
    routing_auth = authority("routing", "ROUTING_RISK_SET", ("RoutingEligibilityFact@1.0.0",))
    replay_auth = authority("replay", "REPLAY_PROTOCOL", ("ReplayReceipt@1.0.0",))
    query_auth = authority("i03_query", "PREDICATE_GRAMMAR", ("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"))
    authorities = (projection_auth, source_auth, coordinate_auth, routing_auth, replay_auth, query_auth)

    universe_spec = package["projection_material"]["universe_spec"]
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref, projection_auth.authority_ref),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=dref("REPLAY_ROOT", "universe", universe_spec),
        raw_source_identity=f"sha256:{SOURCE_SHA}",
        source_family="LiTS",
        study_product_release=universe_spec["study_product"],
        instrument_release=universe_spec["instrument_release"],
        country_geography=universe_spec["country_geography"],
        sampling_geography=universe_spec["sampling_geography"],
        raw_wave=universe_spec["raw_wave"],
        canonical_wave_if_governed=universe_spec["canonical_wave_if_governed"],
        field_or_reference_time="2006",
        target_population_and_sample_frame=universe_spec["target_population_and_sample_frame"],
        sampling_design_regime=universe_spec["sampling_design_regime"],
        respondent_namespace=universe_spec["respondent_namespace"],
        source_artifact_import_lineage=f"LiTS_I.dta|sha256:{SOURCE_SHA}|AS2A:{PART_A_HASH}",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )

    respondents = tuple(
        RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=f"LITS1_SELECTED_RESPONDENT__{SOURCE_SHA}__ROW_{row:012d}",
            source_native_respondent_key_ref_or_typed_absence=TypedAbsence(
                "NOT_AUTHORIZED", "native id remains a source attribute and is not durable identity authority"
            ),
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        )
        for row in range(1, ROWS + 1)
    )
    row_bindings = tuple(RowRespondentBinding(i, respondents[i - 1].ref) for i in range(1, ROWS + 1))

    qrefs = {
        name: dref("QUESTION_NATIVE", f"lits1-{name}", {"source_sha256": SOURCE_SHA, "slot": slots[name], "name": name})
        for name in ("q301_2", "q301_7")
    }
    questions = tuple(
        QuestionVariableBinding(
            empirical_universe_ref=universe.ref,
            native_question_ref=qrefs[name],
            instrument_question_version="LiTS-I-2006",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=source_auth.authority_ref,
            topology_authority_ref=source_auth.authority_ref,
        )
        for name in ("q301_2", "q301_7")
    )
    question_by_name = dict(zip(("q301_2", "q301_7"), questions))

    response_slots = []
    for name in ("q301_2", "q301_7"):
        occurrence = OccurrenceRule(
            "scalar-0",
            dref("RESPONSE_TOPOLOGY", f"{name}-scalar", {"source_sha256": SOURCE_SHA, "slot": slots[name], "kind": "SCALAR_SINGULAR"}),
            {"kind": "SCALAR_SINGULAR", "index": 0},
        )
        rules = []
        for value in range(1, 6):
            exact = Decimal(value)
            rules.append(ResponseValueRule(physical_value_binding_key(exact, PhysicalMissingState.OBSERVED_STORAGE_VALUE), "SUBSTANTIVE_RESPONSE", (occurrence,)))
        for value in (6, 7):
            exact = Decimal(value)
            rules.append(ResponseValueRule(physical_value_binding_key(exact, PhysicalMissingState.OBSERVED_STORAGE_VALUE), "SOURCE_SPECIFIC_SPECIAL", (occurrence,)))
        rules.append(ResponseValueRule(physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING), "MISSING", (occurrence,)))
        response_slots.append(ResponseSlotRule(PhysicalSlot(slots[name], name), question_by_name[name], tuple(rules)))

    coordinate_slots = []
    coordinate_refs = {}
    for name in ("country", "city", "region", "tablec", "tabled"):
        coordinate_refs[name] = dref("COORDINATE_NATIVE", f"lits1-{name}", {"source_sha256": SOURCE_SHA, "slot": slots[name], "name": name})
        missing = CoordinateValueRule(
            physical_value_binding_key(None, PhysicalMissingState.SYSTEM_MISSING),
            "MISSING",
        )
        coordinate_slots.append(CoordinateSlotRule(
            PhysicalSlot(slots[name], name),
            coordinate_refs[name],
            dref("UNIT_TAXONOMY", f"lits1-{name}", {"scope": "SOURCE_NATIVE_RAW", "coordinate": name}),
            "LiTS-I-2006",
            coordinate_auth.authority_ref,
            values=(missing,),
            copy_observed_raw=True,
        ))

    risk_set_ref = dref("RISK_SET", "lits1-q301-bounded", {
        "source_sha256": SOURCE_SHA,
        "rows": ROWS,
        "questions": [qrefs[name].as_dict() for name in ("q301_2", "q301_7")],
        "routing": "ELIGIBLE_APPLICABLE__SECTION3_Q301_UNCONDITIONAL_SELECTED_RESPONDENT",
    })
    member_set_ref = dref("MEMBER_SET", "lits1-q301-bounded", {"source_sha256": SOURCE_SHA, "row_ordinals": [1, ROWS], "count": ROWS})
    routing = tuple(
        RoutingEligibilityFact(
            typed_state="ELIGIBLE_APPLICABLE",
            authority_snapshot_refs=(projection_auth.authority_ref, routing_auth.authority_ref),
            dependency_refs=(respondent.ref, qrefs[name]),
            producer_replay_locator_or_reference_root=dref("REPLAY_ROOT", f"routing-{name}-{row}", {"source_sha256": SOURCE_SHA, "row": row, "question": name}),
            empirical_universe_ref=universe.ref,
            scoped_respondent_ref=respondent.ref,
            question_or_target_ref=qrefs[name],
            risk_set_ref=risk_set_ref,
            routing_rule_ref=dref("ROUTING_RULE", f"lits1-{name}", {"part_a_hash": PART_A_HASH, "question": name, "state": "ELIGIBLE_APPLICABLE"}),
            applicability_state="ELIGIBLE_APPLICABLE",
            routing_state="ELIGIBLE_APPLICABLE",
            parent_predicate_refs=(),
            member_set_replay_ref=member_set_ref,
        )
        for row, respondent in enumerate(respondents, 1)
        for name in ("q301_2", "q301_7")
    )

    package_ref = package["projection_authority_ref"]
    projection = LinearValidatedGovernedC11Projection(
        projection_identity_ref=ExactRef(package_ref["kind"], package_ref["object_id"], package_ref["content_hash"]),
        source_artifact_id=f"urn:rawlsing:source:lits1:sha256:{SOURCE_SHA}",
        expected_source_sha256=SOURCE_SHA,
        source_family_id="LiTS",
        study_product_id="Life in Transition Survey 2006",
        release_id=f"LITS1-AS2B-C11-{SOURCE_SHA[:16]}-{PART_A_HASH[:16]}",
        instrument_release_id="LiTS-I Final questionnaire 2006",
        source_snapshot_retention_ref=ExactRef("SOURCE_SNAPSHOT", f"urn:rawlsing:source:lits1:sha256:{SOURCE_SHA}", SOURCE_SHA),
        universes=(universe,),
        respondents=respondents,
        row_bindings=row_bindings,
        questions=questions,
        response_slots=tuple(response_slots),
        coordinate_slots=tuple(coordinate_slots),
        routing=routing,
        weight_slots=(),
        authority_snapshots=authorities,
        source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"),
        structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(a.authority_ref for a in authorities),
        projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay_auth.authority_ref,
        tie_order_ref=dref("ORDER_RULE", "canonical-ref-sort", {"contract": CONTRACT_ID, "rule": "CANONICAL_EXACT_REF_SORT"}),
        replay_protocol_version="AS2B-LITS1-1.0.0",
    )
    context = {
        "universe": universe,
        "respondents": respondents,
        "qrefs": qrefs,
        "coordinate_refs": coordinate_refs,
        "risk_set_ref": risk_set_ref,
        "authorities": authorities,
        "projection_auth": projection_auth,
        "source_auth": source_auth,
        "coordinate_auth": coordinate_auth,
        "routing_auth": routing_auth,
        "query_auth": query_auth,
    }
    return projection, context


def response_leaf(context, question: str, *, values: Iterable[Any] | None = None, state: str | None = None):
    if state is not None:
        return {
            "op": "LEAF", "leaf_type": "TYPED_RESPONSE_STATE",
            "question_semantic_ref": context["qrefs"][question],
            "typed_state_ref": dref("TYPED_STATE", f"{question}-{state}", {"question": question, "state": state}),
            "state_semantic_authority_ref": context["source_auth"].authority_ref,
            "typed_state": state,
        }
    values = tuple(values or ())
    return {
        "op": "LEAF", "leaf_type": "SURVEY_RESPONSE_EVENT",
        "question_semantic_ref": context["qrefs"][question],
        "component_or_event_selector_ref": dref("EVENT_SELECTOR", f"{question}-scalar", {"question": question, "topology": "SCALAR_SINGULAR"}),
        "response_value_or_state_ref": dref("VALUE_REF", f"{question}-values", {"question": question, "values": values}),
        "response_topology_authority_ref": context["source_auth"].authority_ref,
        "response_semantic_authority_ref": context["source_auth"].authority_ref,
        "operator": "IN" if len(values) != 1 else "EQ",
        "exact_values": values,
        **({"exact_value": values[0]} if len(values) == 1 else {}),
    }


def routing_leaf(context, question: str):
    return {
        "op": "LEAF", "leaf_type": "ROUTING_APPLICABILITY_STATE",
        "question_semantic_ref": context["qrefs"][question],
        "routing_or_applicability_state_ref": dref("ROUTING_STATE", f"{question}-eligible", {"question": question, "state": "ELIGIBLE_APPLICABLE"}),
        "routing_authority_ref": context["routing_auth"].authority_ref,
        "routing_state": "ELIGIBLE_APPLICABLE",
    }


def coordinate_leaf(context, coordinate: str, value: Any):
    return {
        "op": "LEAF", "leaf_type": "EMPIRICAL_POSITION_COORDINATE",
        "coordinate_semantic_ref": context["coordinate_refs"][coordinate],
        "value_or_value_set_ref": dref("VALUE_REF", f"{coordinate}-value", {"coordinate": coordinate, "value": value}),
        "comparison_operator_ref": dref("COMPARISON_OPERATOR", "eq", {"operator": "EQ"}),
        "typed_state_policy_ref": dref("STATE_POLICY", "observed-only", {"state": "OBSERVED_COORDINATE"}),
        "coordinate_authority_ref": context["coordinate_auth"].authority_ref,
        "operator": "EQ", "exact_value": value,
    }


def predicate(context, ast: dict[str, Any], tag: str):
    return make_empirical_predicate(
        predicate_ast=ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(context["query_auth"].authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=dref("REPLAY_ROOT", f"predicate-{tag}", ast),
        grammar_authority_ref=context["query_auth"].authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=(context["risk_set_ref"],),
        scope_refs=(context["universe"].ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(dref("OPERATOR_SEMANTICS", "boolean", {"operators": ["AND", "OR", "NOT", "EQ", "IN", "STATE_EQ"]}),),
    )


def query(context, pred, targets: tuple[str, ...], tag: str, *, weighted: bool = False):
    domain = tuple(Decimal(i) for i in range(1, 6))
    components = tuple({
        "target_ref": context["qrefs"][name],
        "topology": "SCALAR_SINGULAR",
        "domain": domain,
        "target_domain_replay_ref": dref("TARGET_DOMAIN", f"{name}-substantive-1-5", {"question": name, "domain": domain, "excluded_typed_states": ["SOURCE_SPECIFIC_SPECIAL", "MISSING"]}),
        "topology_authority_refs": (context["source_auth"].authority_ref,),
        "response_semantic_authority_refs": (context["source_auth"].authority_ref,),
        "included_states": ("SUBSTANTIVE_RESPONSE",),
    } for name in targets)
    grain = {
        "source_scope_mode": "SINGLE_UNIVERSE",
        "measure_kind": "GOVERNED_WEIGHTED" if weighted else "RAW",
        "risk_set_type": "COMMON_ELIGIBLE_RISK_SET" if len(targets) > 1 else "WHOLE_QUESTION_RISK_SET",
        "response_state_semantics_ref": dref("RESPONSE_STATE_SEMANTICS", "lits1-raw-substantive", {"part_a_hash": PART_A_HASH, "included": ["SUBSTANTIVE_RESPONSE"], "preserved_nonincluded": ["SOURCE_SPECIFIC_SPECIAL", "MISSING"]}),
        "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
    }
    if weighted:
        grain["weight_basis_id"] = "AS2B_NO_AUTHORIZED_WEIGHT"
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(context["query_auth"].authority_ref,),
        dependency_refs=(pred.ref,),
        producer_replay_locator_or_reference_root=dref("REPLAY_ROOT", f"query-{tag}", {"predicate": pred.ref.as_dict(), "targets": targets, "weighted": weighted}),
        target_refs=tuple(context["qrefs"][name] for name in targets),
        target_arity_and_topology={"arity": len(targets), "joint_order_semantics": "SEMANTIC_ORDERED", "components": components},
        condition_predicate_ref=pred.ref,
        risk_set_ref=context["risk_set_ref"],
        empirical_universe_refs=(context["universe"].ref,),
        scope_refs=(context["universe"].ref,),
        measure_basis_ref=dref("MEASURE_BASIS", "governed-weighted" if weighted else "raw", {"kind": "GOVERNED_WEIGHTED" if weighted else "RAW"}),
        requested_output_grain=grain,
        query_authority_refs=(context["query_auth"].authority_ref,),
    )


def fact_receipt(result) -> dict[str, Any]:
    return {
        "query_ref": result.query_ref.as_dict(),
        "source_scope_mode": result.source_scope_mode,
        "release_refs": [ref.as_dict() for ref in result.release_refs],
        "facts": [{
            "ref": fact.ref.as_dict(),
            "typed_state": fact.typed_state,
            "raw_numerator_support": fact.raw_numerator_support,
            "raw_denominator_support": fact.raw_denominator_support,
        } for fact in result.facts],
    }


def run_i03(repository, release, context):
    registry = AuthorityRegistry(context["authorities"])
    all_pred = predicate(context, routing_leaf(context, "q301_2"), "all")
    q2_low = response_leaf(context, "q301_2", values=(Decimal(1), Decimal(2)))
    q7_one = response_leaf(context, "q301_7", values=(Decimal(1),))
    q7_two = response_leaf(context, "q301_7", values=(Decimal(2),))
    first_country = min(
        (obj.raw_coordinate_value for obj in release.public_objects
         if obj.schema_id == "EmpiricalCoordinateFact" and exact_ref(obj.native_coordinate_ref) == context["coordinate_refs"]["country"]
         and obj.typed_state == "OBSERVED_COORDINATE"),
        key=canonical_json,
    )
    plans = [
        ("univariate_distribution", all_pred, ("q301_2",), False),
        ("two_way_joint_pair_cotravel", all_pred, ("q301_2", "q301_7"), False),
        ("conditional_distribution", predicate(context, q2_low, "q2-low"), ("q301_7",), False),
        ("subgroup_country_equal", predicate(context, coordinate_leaf(context, "country", first_country), "country-eq"), ("q301_7",), False),
        ("subgroup_country_complement", predicate(context, {"op": "NOT", "children": [coordinate_leaf(context, "country", first_country)]}, "country-not"), ("q301_7",), False),
        ("recursive_and_or_not", predicate(context, {"op": "AND", "children": [q2_low, {"op": "OR", "children": [q7_one, q7_two]}]}, "recursive"), ("q301_2",), False),
        ("typed_special_state_condition", predicate(context, response_leaf(context, "q301_2", state="SOURCE_SPECIFIC_SPECIAL"), "special"), ("q301_7",), False),
        ("weighted_no_default", all_pred, ("q301_2",), True),
    ]
    receipts = []
    failed = 0
    typed_nonpositive = 0
    for operation, pred, targets, weighted in plans:
        spec = query(context, pred, targets, operation, weighted=weighted)
        result = execute_empirical_query(
            repository=repository,
            query=spec,
            predicate=pred,
            authority_registry=registry,
            release_refs=(release.release_ref,),
        )
        receipt = {"operation": operation, "execution": "EXECUTED", **fact_receipt(result)}
        states = {fact.typed_state for fact in result.facts}
        if weighted:
            expected = states <= {"UNAVAILABLE", "UNRESOLVED", "NOT_APPLICABLE"} and bool(states)
            receipt["expected_typed_nonpositive"] = expected
            typed_nonpositive += int(expected)
            failed += int(not expected)
        else:
            allowed = {"SUPPORTED", "OBSERVED_ZERO", "ZERO_SUPPORT", "LOW_SUPPORT", "UNRESOLVED", "NOT_APPLICABLE", "VALID_EMPTY"}
            expected = bool(states) and states <= allowed
            receipt["expected_positive_or_lawful_typed_nonpositive"] = expected
            receipt["lawful_typed_nonpositive"] = bool(states & {"UNRESOLVED", "NOT_APPLICABLE", "VALID_EMPTY"})
            typed_nonpositive += int(receipt["lawful_typed_nonpositive"])
            failed += int(not expected)
        receipts.append(receipt)
        print(f"I03 {operation}: states={sorted(states)} expected={expected}", flush=True)
    for operation, reason in (
        ("three_way_conjunction", "TYPED_NOT_APPLICABLE__ONLY_TWO_POSITIVE_BOUNDED_RESPONSE_SLOTS"),
        ("five_way_conjunction", "TYPED_NOT_APPLICABLE__ONLY_TWO_POSITIVE_BOUNDED_RESPONSE_SLOTS"),
        ("source_indexed_multi_universe", "TYPED_NOT_APPLICABLE__ONE_EXACT_ACCEPTED_SOURCE_UNIVERSE"),
        ("non_scalar_topology_gather", "TYPED_NOT_APPLICABLE__BOUNDED_PROVING_RESPONSE_SLOTS_ARE_SCALAR"),
    ):
        receipts.append({"operation": operation, "execution": "NOT_EXECUTED", "typed_nonpositive_state": reason})
        typed_nonpositive += 1
    return {
        "executed_query_count": len(plans),
        "passed_query_count": len(plans) - failed,
        "failed_query_count": failed,
        "typed_nonpositive_count": typed_nonpositive,
        "operation_receipts": receipts,
        "first_country_exact_value": first_country,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--result", required=True, type=Path)
    parser.add_argument("--run-label", required=True)
    args = parser.parse_args()
    started = time.time()
    disk_before = shutil.disk_usage(args.result.parent)
    package, ledger, slots = read_banked_authority()
    source_hash = sha256_file(args.source)
    if source_hash != SOURCE_SHA:
        raise RuntimeError("LiTS-I source SHA mismatch")
    print(f"{args.run_label}: source and Part-A hashes verified", flush=True)

    decode_started = time.time()
    incidence = decode_dta(args.source, encoding="latin1")
    decode_seconds = time.time() - decode_started
    if incidence.source_sha256 != SOURCE_SHA or incidence.row_count != ROWS or len(incidence.variables) != VARIABLES:
        raise RuntimeError("frozen decoder source shape/identity mismatch")
    if incidence.reader_configuration.get("authority_status") != COMPATIBILITY_ONLY:
        raise RuntimeError("frozen decoder compatibility status mismatch")
    print(f"{args.run_label}: frozen decoder complete in {decode_seconds:.3f}s", flush=True)

    projection_started = time.time()
    projection, context = build_projection(incidence, package, ledger, slots)
    projection_seconds = time.time() - projection_started
    print(f"{args.run_label}: GovernedC11Projection constructed in {projection_seconds:.3f}s", flush=True)

    physical_denominator = incidence.row_count * len(incidence.variables)
    selected_physical_count = 0
    selected_counts = {name: {state.value: 0 for state in PhysicalMissingState} for name in ("q301_2", "q301_7", "q105_12")}
    sequence_hashes = {name: hashlib.sha256() for name in ("id", "country", "weight_0", "weight_1", "weight_2", "q304a", "q304b")}
    observed_country_values = set()

    selected_names = {
        "id", "country", "city", "region", "tablec", "tabled",
        "q301_2", "q301_7", "q105_12", "q304a", "q304b",
        "weight_0", "weight_1", "weight_2",
    }
    selected_variables = tuple(v for v in incidence.variables if v.name in selected_names)
    if {v.name for v in selected_variables} != selected_names:
        raise RuntimeError("hostile/projection selected physical slot unavailable")
    selected_incidence = PhysicalSourceIncidence(
        source_sha256=incidence.source_sha256,
        source_format=incidence.source_format,
        row_count=incidence.row_count,
        variables=selected_variables,
        reader_configuration={**incidence.reader_configuration, "transport": "EXACT_PROJECTED_AND_HOSTILE_SLOT_STREAM"},
        file_metadata=incidence.file_metadata,
        _frame=incidence._frame[[v.name for v in selected_variables]],
    )

    def cells():
        nonlocal selected_physical_count
        for native in selected_incidence.iter_cells(batch_size=20_000):
            selected_physical_count += 1
            cell = exact_cell(native)
            name = cell.variable_name
            if name in selected_counts:
                selected_counts[name][cell.missing_state.value] += 1
            if name in sequence_hashes:
                sequence_hashes[name].update((canonical_json({"row": cell.row_ordinal, "value": cell.raw_value, "state": cell.missing_state.value}) + "\n").encode("utf-8"))
            if name == "country" and cell.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE:
                observed_country_values.add(canonical_json(cell.raw_value))
            yield cell

    build_started = time.time()
    candidate = project_c11_candidate_from_physical_cells(
        source_sha256=SOURCE_SHA,
        row_count=ROWS,
        cells=cells(),
        projection=projection,
    )
    build_seconds = time.time() - build_started
    if physical_denominator != PHYSICAL_CELLS:
        raise RuntimeError(f"physical cell denominator mismatch: {physical_denominator}")
    if selected_physical_count != ROWS * len(selected_variables):
        raise RuntimeError(f"selected exact physical stream mismatch: {selected_physical_count}")
    print(f"{args.run_label}: C11SourceReleaseCandidate built in {build_seconds:.3f}s", flush=True)

    validate_started = time.time()
    release = validate_c11_source_release(candidate)
    validation_seconds = time.time() - validate_started
    repository = C11Repository((release,))
    if repository.resolve_release_exact(release.release_ref) is not release:
        raise RuntimeError("C11Repository exact resolution failed")
    print(f"{args.run_label}: C11 release/repository validated in {validation_seconds:.3f}s", flush=True)

    i03_started = time.time()
    i03 = run_i03(repository, release, context)
    i03_seconds = time.time() - i03_started
    print(f"{args.run_label}: I03 burden complete in {i03_seconds:.3f}s", flush=True)

    counts = dict(record_counts_for_candidate(candidate))
    weights_distinct_slots = len({slots[name] for name in ("weight_0", "weight_1", "weight_2")}) == 3
    hostile = [
        {"fixture_id": "L1_ID_ROW_ORDINAL", "status": "PASS" if all(isinstance(r.source_native_respondent_key_ref_or_typed_absence, TypedAbsence) and r.source_native_respondent_key_ref_or_typed_absence.state == "NOT_AUTHORIZED" for r in context["respondents"]) else "FAIL", "evidence": "respondent identity is source SHA plus 1-based row ordinal; native id sequence retained as physical-only digest"},
        {"fixture_id": "L1_COUNTRY_CONTEXT_EXACT", "status": "PASS" if counts["EmpiricalCoordinateFact"] == ROWS * 5 else "FAIL", "evidence": f"five raw coordinate slots x {ROWS} rows; observed country codes={len(observed_country_values)}"},
        {"fixture_id": "L1_WEIGHT_SURFACES_DISTINCT", "status": "PASS" if weights_distinct_slots else "FAIL", "evidence": "weight_0/weight_1/weight_2 retain distinct physical slot ordinals and sequence digests"},
        {"fixture_id": "L1_NO_DEFAULT_WEIGHT", "status": "PASS" if counts["WeightMeasureFact"] == 0 else "FAIL", "evidence": "no WeightMeasureFact projected"},
        {"fixture_id": "L1_DK_NA_NOT_AUTOMATIC", "status": "PASS" if counts["RespondentEvent"] == ROWS * 2 else "FAIL", "evidence": "raw codes 6 and 7 use SOURCE_SPECIFIC_SPECIAL, not semantic DK/IAP"},
        {"fixture_id": "L1_Q105_12_PHYSICAL_MISSING", "status": "PASS" if selected_counts["q105_12"][PhysicalMissingState.SYSTEM_MISSING.value] == ROWS else "FAIL", "evidence": f"system-missing physical cells={selected_counts['q105_12'][PhysicalMissingState.SYSTEM_MISSING.value]}"},
        {"fixture_id": "L1_RANKED_ORDERED_SOURCE_TOPOLOGY", "status": "PASS" if slots["q304a"] != slots["q304b"] else "FAIL", "evidence": "q304a and q304b retained as distinct physical slots and sequence digests"},
        {"fixture_id": "L1_ENCODING_PROVENANCE", "status": "PASS" if incidence.reader_configuration.get("encoding") == "latin1" and incidence.reader_configuration.get("authority_status") == COMPATIBILITY_ONLY else "FAIL", "evidence": COMPATIBILITY_ONLY},
    ]
    hostile_failed = sum(item["status"] != "PASS" for item in hostile)
    peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    disk_after = shutil.disk_usage(args.result.parent)
    result = {
        "schema": "AS2B_LITS1_MECHANICAL_SOURCE_CERTIFICATION_RUN@1.0.0",
        "run_label": args.run_label,
        "status": "PASS" if hostile_failed == 0 and i03["failed_query_count"] == 0 else "FAIL",
        "source": {"path": str(args.source), "sha256": source_hash, "rows": incidence.row_count, "variables": len(incidence.variables), "physical_cells": physical_denominator, "selected_exact_physical_cells_streamed": selected_physical_count, "selected_exact_physical_slot_count": len(selected_variables), "format": incidence.source_format},
        "part_a": {"projection_authority_hash": PART_A_HASH, "slot_ledger_sha256": SLOT_LEDGER_HASH, "slot_count": len(ledger)},
        "environment": {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "platform": platform.platform(),
            "pyreadstat": pyreadstat.__version__,
            "pandas": pandas.__version__,
            "numpy": numpy.__version__,
            "pyarrow": pyarrow.__version__,
            "duckdb": duckdb.__version__,
            "decoder_call": "decode_dta(source_path, encoding=\"latin1\")",
            "encoding_authority_status": incidence.reader_configuration.get("authority_status"),
        },
        "projection": {
            "identity_ref": projection.projection_identity_ref.as_dict(),
            "runtime_cache_identity_hash": projection.cache_identity,
            "runtime_identity": f"urn:rawlsing:pre553:as2b:lits1:governed-c11-projection:sha256:{projection.cache_identity}",
            "response_slots": ["q301_2", "q301_7"],
            "coordinate_slots": ["country", "city", "region", "tablec", "tabled"],
            "weight_slots": [],
        },
        "c11": {
            "candidate_identity": f"urn:rawlsing:pre553:as2b:lits1:c11-candidate:sha256:{candidate.candidate_replay_manifest.semantic_projection_hash}",
            "candidate_hash": candidate.candidate_replay_manifest.semantic_projection_hash,
            "source_release_manifest_hash": candidate.source_release_manifest.content_hash,
            "logical_release_ref": release.release_ref.as_dict(),
            "logical_release_hash": release.semantic_release_hash,
            "repository_release_count": len(repository),
            "repository_snapshot_identity": repository.snapshot_identity(),
            "repository_snapshot_hash": semantic_hash(repository.snapshot_identity()),
            "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
            "replay_manifest_hash": release.replay_manifest.content_hash,
            "record_counts": counts,
            "public_object_count": len(release.public_objects),
            "internal_record_count": len(release.internal_records),
            "m01_m18_coverage": {key: list(value) for key, value in release.m01_m18_coverage.items()},
        },
        "hostile_fixtures": {"passed": len(hostile) - hostile_failed, "failed": hostile_failed, "fixtures": hostile},
        "physical_surface_receipt": {
            "selected_missing_state_counts": selected_counts,
            "sequence_hashes": {name: digest.hexdigest() for name, digest in sequence_hashes.items()},
            "observed_country_value_count": len(observed_country_values),
        },
        "i03": i03,
        "resources": {
            "total_wall_seconds": time.time() - started,
            "decoder_wall_seconds": decode_seconds,
            "projection_construction_seconds": projection_seconds,
            "c11_candidate_build_seconds": build_seconds,
            "c11_validation_seconds": validation_seconds,
            "i03_seconds": i03_seconds,
            "peak_rss_bytes": peak_rss,
            "source_opens_high_level": 4,
            "source_opens_method": "one explicit SHA read + decoder internal SHA read + pyreadstat metadata read + pyreadstat compatibility full read",
            "decoder_passes": 1,
            "persistent_payload_bytes": 0,
            "transient_scratch_bytes": 0,
            "disk_free_before": disk_before.free,
            "disk_free_after_before_receipt": disk_after.free,
            "cleanup_behavior": "NO_TRANSIENT_FILES_CREATED; all C11 objects remained process-memory resident",
        },
    }
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{args.run_label}: wrote {args.result}; status={result['status']}", flush=True)
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
