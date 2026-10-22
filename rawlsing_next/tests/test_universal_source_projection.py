from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next.pre553_c11_integrity import (
    QuestionVariableBinding,
    RespondentIdentity,
    TypedAbsence,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    canonical_json,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_physical_decoder import (
    PhysicalCell,
    PhysicalMissingState,
    decode_sav,
)
from rawlsing_next.pre553_source_backed_c11_facade import (
    CONTRACT_ID,
    ExactPhysicalCellStream,
    build_source_backed_c11_repository,
    physical_value_binding_key,
)
from rawlsing_next.pre553_source_native_preimage_adapter import (
    OCCURRENCE_BINDING_SCHEMA,
    GovernedRowOccurrencePlan,
    NativePreimageRefusal,
    NativeSourceIdentity,
    NativeSourcePackage,
    NativeSourceRule,
    OccurrenceBinding,
    VariableOccurrencePlan,
    build_authority_set,
    materialize_native_preimages,
    token,
)
from rawlsing_next.tests.pre553_query_frontier_fixtures import _custom_query
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _query_authority,
)

REPO = Path(__file__).resolve().parents[2]
SOURCE_ID = "R56R02"


def source_identity(path: Path, rows: int, source_format: str = "SAV") -> NativeSourceIdentity:
    return NativeSourceIdentity(
        source_id=SOURCE_ID, family="SYNTHETIC", wave="W1",
        canonical_filename=path.name,
        declared_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        source_format=source_format, expected_rows=rows)


def package(path: Path, rows: int, rules, *, coordinate="OCCASION",
            units=None, source_format="SAV") -> NativeSourcePackage:
    if units is None:
        units = {rule.source_variable_code: rule.unit for rule in rules}
    expanded = []
    for rule in rules:
        if rule.unit == "person":
            expanded.append(NativeSourceRule(
                rule.implementation_id, rule.source_variable_code,
                unit=units[rule.source_variable_code],
                administered=rule.administered,
                semantic_direction=rule.semantic_direction,
                value_aliases=rule.value_aliases))
        else:
            expanded.append(rule)
    return NativeSourcePackage(
        source=source_identity(path, rows, source_format),
        selected=tuple(expanded), coordinate_variable=coordinate)


def occurrence_plan(variables, respondent_map):
    plans = []
    for variable, topology, bindings in variables:
        plans.append(VariableOccurrencePlan(
            variable, topology,
            tuple(OccurrenceBinding(value, key, fields)
                  for value, key, fields in bindings)))
    return GovernedRowOccurrencePlan(
        respondent_variable="PID", occasion_variable="OCCASION",
        variable_plans=tuple(plans),
        respondent_key_by_source_value=respondent_map)


def repeated_plan(variable="SCORE"):
    return occurrence_plan(
        ((variable, "REPEATED_EVENT", (
            ("0", "0", {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
            ("1", "1", {"kind": "REPEATED_EVENT", "multiplicity_index": 1}),
        )),),
        {str(i): f"P{i}" for i in range(64)})


def write_rows(path: Path, rows, labels=None, fmt="sav"):
    frame = pd.DataFrame(rows)
    kwargs = {}
    if labels:
        kwargs["column_labels"] = labels
    if fmt == "sav":
        pyreadstat.write_sav(frame, str(path), **kwargs)
    else:
        pyreadstat.write_dta(frame, str(path), **kwargs)


def event_tuples(bundle, variable="SCORE"):
    refkeys = {r.ref.key: r.respondent_key for r in bundle.projection.respondents}
    question = bundle.question_refs[variable]
    result = []
    for obj in bundle.release.public_objects:
        if not isinstance(obj, RespondentEvent):
            continue
        if dict(obj.native_question_ref) != question.as_dict():
            continue
        ref = dict(obj.scoped_respondent_ref)
        key = f"{ref['kind']}|{ref['object_id']}|{ref['content_hash']}"
        fields = dict(obj.multiplicity_order_rank_fields)
        order = fields.get("multiplicity_index", fields.get("semantic_ordinal",
                                                             fields.get("index")))
        result.append((
            refkeys[key], order, obj.typed_state,
            obj.canonical_response_value_if_authorized,
        ))
    return tuple(sorted(result))


def domain_from_bundle(bundle, variable="SCORE"):
    refkeys = {r.ref.key: r.respondent_key for r in bundle.projection.respondents}
    question = bundle.question_refs[variable]
    grouped = {}
    for obj in bundle.release.public_objects:
        if not isinstance(obj, RespondentEvent):
            continue
        if dict(obj.native_question_ref) != question.as_dict():
            continue
        ref = dict(obj.scoped_respondent_ref)
        key = f"{ref['kind']}|{ref['object_id']}|{ref['content_hash']}"
        grouped.setdefault(refkeys[key], []).append(obj)
    domain = []
    for respondent in sorted(grouped):
        events = sorted(grouped[respondent],
                        key=lambda event: event.multiplicity_order_rank_fields[
                            "multiplicity_index"])
        domain.append([{
            "event_id": event.response_event_id_or_deterministic_index,
            "multiplicity_order_rank_fields": dict(
                event.multiplicity_order_rank_fields),
            "value": event.canonical_response_value_if_authorized,
        } for event in events])
    return domain


def run_repeated(bundle, domain, variable="SCORE"):
    source = {
        "qrefs": bundle.question_refs,
        "source_auth": bundle.projection.authority_snapshots[0],
        "risk_refs": {"R": bundle.risk_set_ref},
        "universe": bundle.projection.universes[0],
        "respondents": {r.respondent_key: r for r in bundle.projection.respondents},
        "authorities": bundle.projection.authority_snapshots,
    }
    qa = _query_authority("r56-r02")
    predicate = _branch_predicate(source, qa, tag="r56-r02")
    query = _custom_query(
        source, qa, predicate, variable, topology="REPEATED_EVENT",
        domain=domain, included_states=("SUBSTANTIVE_RESPONSE",),
        tag="r56-r02")
    repository, release = build_source_backed_c11_repository(
        bundle.physical_stream, bundle.projection)
    registry = AuthorityRegistry(tuple((*bundle.projection.authority_snapshots, qa)))
    result = execute_empirical_query(
        repository=repository, query=query, predicate=predicate,
        authority_registry=registry, release_refs=(release.release_ref,))
    return result.facts[0]


def run_scalar(bundle, variable="Y"):
    source = {
        "qrefs": bundle.question_refs,
        "source_auth": bundle.projection.authority_snapshots[0],
        "risk_refs": {"R": bundle.risk_set_ref},
        "universe": bundle.projection.universes[0],
        "respondents": {r.respondent_key: r for r in bundle.projection.respondents},
        "authorities": bundle.projection.authority_snapshots,
    }
    qa = _query_authority("r56-r02-scalar")
    predicate = _branch_predicate(source, qa, tag="r56-r02-scalar")
    query = _custom_query(
        source, qa, predicate, variable, topology="SCALAR_SINGULAR",
        domain=("0", "1"), included_states=("SUBSTANTIVE_RESPONSE",),
        tag="r56-r02-scalar")
    repository, release = build_source_backed_c11_repository(
        bundle.physical_stream, bundle.projection)
    registry = AuthorityRegistry(tuple((*bundle.projection.authority_snapshots, qa)))
    result = execute_empirical_query(
        repository=repository, query=query, predicate=predicate,
        authority_registry=registry, release_refs=(release.release_ref,))
    return result.facts[0]


def s3_rows(respondents=12, occasions=2, mutate=None):
    rows = []
    for respondent in range(respondents):
        for occasion in range(occasions):
            value = respondent % 3
            if mutate == (respondent, occasion):
                value = (value + 1) % 3
            rows.append({
                "PID": float(respondent), "OCCASION": float(occasion),
                "SCORE": float(value), "MR1": float(respondent % 2) if occasion == 0 else None,
                "RANK1": float(respondent % 3) if occasion == 0 else None,
                "FORM": float(respondent % 2),
            })
    return rows


def build_s3(path: Path, rows, variable="SCORE", rules=None):
    write_rows(path, rows)
    return load_s3(path, variable=variable, rules=rules)


def load_s3(path: Path, variable="SCORE", rules=None):
    incidence = decode_sav(path)
    rules = rules or (NativeSourceRule("impl.score", variable),)
    pkg = package(path, incidence.row_count, rules)
    plan = repeated_plan(variable)
    return materialize_native_preimages(
        package=pkg, incidence=incidence, row_occurrence_plan=plan)


def test_s3_exact_respondent_occasion_value_tuples_and_repeated_consumer(tmp_path):
    path = tmp_path / "s3.sav"
    rows = s3_rows()
    bundle = build_s3(path, rows)
    expected = tuple(sorted(
        (f"{SOURCE_ID}:P{respondent}", occasion, "SUBSTANTIVE_RESPONSE",
         str(respondent % 3))
        for respondent in range(12) for occasion in range(2)))
    assert event_tuples(bundle) == expected
    assert len(event_tuples(bundle)) == 24
    domain = domain_from_bundle(bundle)
    assert bundle.release.source_artifact_ref.content_hash == bundle.source_sha256
    rebuilt_repo, rebuilt_release = build_source_backed_c11_repository(
        bundle.physical_stream, bundle.projection)
    assert rebuilt_release.release_ref == bundle.release.release_ref
    fact = run_repeated(bundle, domain)
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 12
    assert fact.raw_numerator_support == 12
    cells = fact.target_topology["complete_cell_semantic_projection"]
    assert len(cells) == 12
    assert {cell["raw_numerator_support"] for cell in cells} == {1}


def test_s3_varied_respondent_and_occasion_counts(tmp_path):
    path = tmp_path / "s3_var.sav"
    rows = s3_rows(respondents=5, occasions=3)
    write_rows(path, rows)
    pkg = package(path, len(rows), (NativeSourceRule("impl.score", "SCORE"),))
    plan = occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "0", {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
            ("1", "1", {"kind": "REPEATED_EVENT", "multiplicity_index": 1}),
            ("2", "2", {"kind": "REPEATED_EVENT", "multiplicity_index": 2}),
        )),),
        {str(i): f"P{i}" for i in range(5)})
    bundle = materialize_native_preimages(
        package=pkg, incidence=decode_sav(path), row_occurrence_plan=plan)
    assert len(event_tuples(bundle)) == 15
    assert {row["source_occasion"] for row in bundle.respondent_rows} == {
        "0", "1", "2"}
    fact = run_repeated(bundle, domain_from_bundle(bundle))
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 5


def test_s3_row_permutation_conserves_tuples_with_matching_mapping(tmp_path):
    path_a = tmp_path / "s3_a.sav"
    path_b = tmp_path / "s3_b.sav"
    rows = s3_rows(respondents=4, occasions=2)
    write_rows(path_a, rows)
    write_rows(path_b, list(reversed(rows)))
    bundle_a = build_s3(path_a, rows)
    bundle_b = build_s3(path_b, list(reversed(rows)))
    assert event_tuples(bundle_a) == event_tuples(bundle_b)
    assert run_repeated(bundle_a, domain_from_bundle(bundle_a)).raw_denominator_support == 4
    assert run_repeated(bundle_b, domain_from_bundle(bundle_b)).raw_denominator_support == 4


def test_s3_missingness_preserves_state_and_does_not_invent_support(tmp_path):
    path = tmp_path / "s3_missing.sav"
    rows = s3_rows(respondents=4, occasions=2)
    rows[1]["SCORE"] = None
    bundle = build_s3(path, rows)
    tuples = event_tuples(bundle)
    assert ("R56R02:P0", 1, "MISSING", None) in tuples
    assert len(tuples) == 8
    fact = run_repeated(bundle, domain_from_bundle(bundle))
    assert fact.typed_state in {"UNRESOLVED", "INTEGRITY_FAILURE"}
    assert fact.typed_state != "SUPPORTED"


def test_s3_equal_values_at_different_occasions_are_distinct(tmp_path):
    path = tmp_path / "s3_equal.sav"
    rows = []
    for respondent in range(3):
        for occasion in range(2):
            rows.append({
                "PID": float(respondent), "OCCASION": float(occasion),
                "SCORE": 1.0, "FORM": 0.0,
            })
    write_rows(path, rows)
    bundle = build_s3(path, rows)
    assert event_tuples(bundle) == tuple(sorted(
        (f"R56R02:P{respondent}", occasion, "SUBSTANTIVE_RESPONSE", "1")
        for respondent in range(3) for occasion in range(2)))
    fact = run_repeated(bundle, domain_from_bundle(bundle))
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 3
    assert fact.raw_numerator_support == 3


def test_s3_different_column_labels_do_not_change_tuples(tmp_path):
    path_a = tmp_path / "s3_label_a.sav"
    path_b = tmp_path / "s3_label_b.sav"
    rows = s3_rows(respondents=3, occasions=2)
    write_rows(path_a, rows, labels=["person", "occasion", "score", "mr", "rank", "form"])
    write_rows(path_b, rows, labels=["PID", "OCC", "S", "M", "R", "F"])
    assert event_tuples(build_s3(path_a, rows)) == event_tuples(build_s3(path_b, rows))


def test_s1_rectangular_scalar_remains_supported(tmp_path):
    path = tmp_path / "s1.sav"
    rows = []
    for i in range(6):
        rows.append({"A": float(i % 2), "B": float((i // 2) % 2),
                     "Y": float((i % 2) ^ ((i // 2) % 2)),
                     "G": float(i % 2)})
    write_rows(path, rows)
    pkg = package(
        path, len(rows),
        (NativeSourceRule("impl.a", "A"), NativeSourceRule("impl.b", "B"),
         NativeSourceRule("impl.y", "Y")),
        coordinate="G")
    bundle = materialize_native_preimages(
        package=pkg, incidence=decode_sav(path))
    assert len(event_tuples(bundle, "Y")) == 6
    fact = run_scalar(bundle, "Y")
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 6
    assert {c["raw_numerator_support"] for c in
            fact.target_topology["complete_cell_semantic_projection"]} == {3}


def test_s2_separate_units_are_refused_not_pooled(tmp_path):
    path = tmp_path / "s2.dta"
    write_rows(path, [{"HID": 1.0, "PID": 1.0, "HMEAS": 1.0,
                       "OUTCOME": 1.0, "OCCASION": 0.0}], fmt="dta")
    with pytest.raises(NativePreimageRefusal) as caught:
        package(
            path, 1,
            (NativeSourceRule("impl.h", "HMEAS", unit="household"),
             NativeSourceRule("impl.o", "OUTCOME", unit="person")),
            coordinate="HID", units={"HMEAS": "household", "OUTCOME": "person"})
    assert caught.value.code == "CROSS_UNIT_POOLING_UNAUTHORIZED"


def test_mr_rank_and_form_topology_fields_are_preserved(tmp_path):
    path = tmp_path / "s3_topology.sav"
    rows = []
    for respondent in range(3):
        for occasion in range(2):
            rows.append({
                "PID": float(respondent), "OCCASION": float(occasion),
                "MR1": float(respondent % 2) if occasion == 0 else None,
                "RANK1": float(respondent % 3) if occasion == 0 else None,
                "FORM": float(respondent % 2),
            })
    write_rows(path, rows)
    pkg = package(
        path, len(rows),
        (NativeSourceRule("impl.mr", "MR1"),
         NativeSourceRule("impl.rank", "RANK1")),
        coordinate="OCCASION")
    plan = occurrence_plan(
        (("MR1", "MULTISELECT", (
            ("0", "0", {"kind": "MULTISELECT", "multiplicity_index": 0}),
            ("1", "1", {"kind": "MULTISELECT", "multiplicity_index": 1}))),
         ("RANK1", "ORDERED_SEQUENCE", (
             ("0", "0", {"kind": "ORDERED_SEQUENCE", "semantic_ordinal": 0}),
             ("1", "1", {"kind": "ORDERED_SEQUENCE", "semantic_ordinal": 1})))),
        {str(i): f"P{i}" for i in range(3)})
    bundle = materialize_native_preimages(
        package=pkg, incidence=decode_sav(path), row_occurrence_plan=plan)
    kinds = {dict(event.multiplicity_order_rank_fields)["kind"]
             for event in bundle.release.public_objects
             if isinstance(event, RespondentEvent)}
    assert kinds == {"MULTISELECT", "ORDERED_SEQUENCE"}
    assert len([event for event in bundle.release.public_objects
                if isinstance(event, RespondentEvent)]) == 12


def test_unadministered_rule_is_held_not_projected(tmp_path):
    path = tmp_path / "s3_admin.sav"
    rows = s3_rows(respondents=2, occasions=2)
    rows[0]["OTHER"] = 1.0
    rows[1]["OTHER"] = None
    rows[2]["OTHER"] = 0.0
    rows[3]["OTHER"] = 1.0
    write_rows(path, rows)
    pkg = package(
        path, len(rows),
        (NativeSourceRule("impl.score", "SCORE"),
         NativeSourceRule("impl.other", "OTHER", administered=False)),
        coordinate="OCCASION")
    plan = occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "0", {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
            ("1", "1", {"kind": "REPEATED_EVENT", "multiplicity_index": 1}))),),
        {"0": "P0", "1": "P1"})
    bundle = materialize_native_preimages(
        package=pkg, incidence=decode_sav(path), row_occurrence_plan=plan)
    assert bundle.held and bundle.held[0].classification == "HELD_NOT_ADMINISTERED"
    assert set(bundle.question_refs) == {"SCORE"}


def test_wrong_duplicate_and_ambiguous_maps_refuse_before_c11(tmp_path):
    path = tmp_path / "s3_map.sav"
    rows = s3_rows(respondents=3, occasions=2)
    write_rows(path, rows)
    pkg = package(path, len(rows), (NativeSourceRule("impl.score", "SCORE"),))
    incidence = decode_sav(path)
    with pytest.raises(NativePreimageRefusal) as duplicate:
        materialize_native_preimages(
            package=pkg, incidence=incidence,
            row_occurrence_plan=GovernedRowOccurrencePlan(
                "PID", "OCCASION",
                (VariableOccurrencePlan("SCORE", "REPEATED_EVENT", (
                    OccurrenceBinding("0", "0", {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
                    OccurrenceBinding("1", "0", {"kind": "REPEATED_EVENT", "multiplicity_index": 1}),
                )),),
                {"0": "P0", "1": "P1", "2": "P2"}))
    assert duplicate.value.code == "DUPLICATE_OCCURRENCE_KEY"
    with pytest.raises(NativePreimageRefusal) as missing:
        materialize_native_preimages(
            package=pkg, incidence=incidence,
            row_occurrence_plan=GovernedRowOccurrencePlan(
                "PID", "OCCASION",
                (VariableOccurrencePlan("SCORE", "REPEATED_EVENT", (
                    OccurrenceBinding("0", "0", {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
                    OccurrenceBinding("1", "1", {"kind": "REPEATED_EVENT", "multiplicity_index": 1}),
                )),),
                {"0": "P0", "1": "P1"}))
    assert missing.value.code == "UNMAPPED_SOURCE_RESPONDENT"
    with pytest.raises(NativePreimageRefusal) as duplicate_row:
        duplicate_rows = [dict(row) for row in rows]
        duplicate_rows.append(dict(duplicate_rows[0]))
        path2 = tmp_path / "s3_dup_row.sav"
        write_rows(path2, duplicate_rows)
        pkg2 = package(path2, len(duplicate_rows),
                       (NativeSourceRule("impl.score", "SCORE"),))
        materialize_native_preimages(
            package=pkg2, incidence=decode_sav(path2),
            row_occurrence_plan=repeated_plan("SCORE"))
    assert duplicate_row.value.code in {"DUPLICATE_OCCURRENCE_IDENTITY",
                                        "C11_VALIDATION_REFUSED"}


def test_mutation_flips_same_repeated_assertion_and_fresh_process_restores(tmp_path):
    baseline_path = tmp_path / "baseline.sav"
    mutant_path = tmp_path / "mutant.sav"
    rows = s3_rows(respondents=4, occasions=2)
    write_rows(baseline_path, rows)
    write_rows(mutant_path, s3_rows(respondents=4, occasions=2, mutate=(1, 0)))
    baseline = build_s3(baseline_path, rows)
    baseline = load_s3(baseline_path)
    domain = domain_from_bundle(baseline)
    baseline_fact = run_repeated(baseline, domain)
    assert baseline_fact.typed_state == "SUPPORTED"
    mutant = build_s3(mutant_path, s3_rows(respondents=4, occasions=2, mutate=(1, 0)))
    mutant_fact = run_repeated(mutant, domain)
    assert mutant_fact.typed_state != "SUPPORTED" or \
        mutant_fact.ref.key != baseline_fact.ref.key
    script = (
        "import importlib.util,json,sys;"
        "p=sys.argv[1];f=sys.argv[2];"
        "s=importlib.util.spec_from_file_location('r56test',p);"
        "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
        "b=m.load_s3(__import__('pathlib').Path(f));"
        "print(json.dumps(m.repeated_fingerprint(b)))"
    )
    env = dict(os.environ, PYTHONPATH=str(REPO), PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(
        [sys.executable, "-B", "-c", script, str(Path(__file__)), str(baseline_path)],
        cwd=str(REPO), env=env, capture_output=True, text=True, timeout=120)
    assert completed.returncode == 0, completed.stderr[-3000:]
    restored = json.loads(completed.stdout.strip().splitlines()[-1])
    assert restored == json.loads(json.dumps(repeated_fingerprint(baseline)))


def repeated_fingerprint(bundle):
    domain = domain_from_bundle(bundle)
    fact = run_repeated(bundle, domain)
    return {
        "state": fact.typed_state,
        "ref": fact.ref.key,
        "denominator": fact.raw_denominator_support,
        "numerator": fact.raw_numerator_support,
        "cells": sorted(
            (tuple((dict(event)["event_id"], dict(event)["value"],
                    dict(event)["multiplicity_order_rank_fields"].get(
                        "multiplicity_index"))
                   for event in cell["cell"]),
             cell["raw_numerator_support"])
            for cell in fact.target_topology.get(
                "complete_cell_semantic_projection", [])),
    }


def test_scalar_form_across_multiple_occasions_is_refused_not_collapsed(tmp_path):
    path = tmp_path / "s3_form.sav"
    rows = s3_rows(respondents=2, occasions=2)
    write_rows(path, rows)
    with pytest.raises(NativePreimageRefusal) as caught:
        VariableOccurrencePlan("FORM", "SCALAR_SINGULAR", (
            OccurrenceBinding("0", "0", {"kind": "SCALAR_SINGULAR", "index": 0}),
            OccurrenceBinding("1", "1", {"kind": "SCALAR_SINGULAR", "index": 1}),
        ))
    assert caught.value.code == "SCALAR_OCCURRENCE_PLAN_AMBIGUOUS"


def test_duplicate_and_unmapped_occurrence_maps_fail_closed(tmp_path):
    path = tmp_path / "s3_occ_map.sav"
    rows = s3_rows(respondents=2, occasions=3)
    write_rows(path, rows)
    pkg = package(path, len(rows), (NativeSourceRule("impl.score", "SCORE"),))
    incidence = decode_sav(path)
    with pytest.raises(NativePreimageRefusal) as duplicate:
        VariableOccurrencePlan("SCORE", "REPEATED_EVENT", (
            OccurrenceBinding("0", "0", {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
            OccurrenceBinding("0", "1", {"kind": "REPEATED_EVENT", "multiplicity_index": 1}),
        ))
    assert duplicate.value.code == "DUPLICATE_OCCURRENCE_SOURCE_VALUE"
    plan = occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "0", {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
            ("1", "1", {"kind": "REPEATED_EVENT", "multiplicity_index": 1}))),),
        {"0": "P0", "1": "P1"})
    with pytest.raises(NativePreimageRefusal) as unmapped:
        materialize_native_preimages(
            package=pkg, incidence=incidence, row_occurrence_plan=plan)
    assert unmapped.value.code == "UNMAPPED_SOURCE_OCCASION"


def test_duplicate_respondent_key_mapping_fails_closed(tmp_path):
    path = tmp_path / "s3_dup_key.sav"
    rows = s3_rows(respondents=2, occasions=2)
    write_rows(path, rows)
    with pytest.raises(NativePreimageRefusal) as caught:
        GovernedRowOccurrencePlan(
            "PID", "OCCASION",
            (VariableOccurrencePlan("SCORE", "REPEATED_EVENT", (
                OccurrenceBinding("0", "0", {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
                OccurrenceBinding("1", "1", {"kind": "REPEATED_EVENT", "multiplicity_index": 1}),
            )),),
            {"0": "P0", "1": "P0"})
    assert caught.value.code == "DUPLICATE_RESPONDENT_KEY_MAPPING"


# ---------------------------------------------------------------------------
# R02V independent review additions.
#
# The author's tests above are retained unchanged. These helpers freeze the
# expected respondent/occasion/value tuples and, separately, the exact I03
# target domain from the generated source bytes and the governed row/occasion
# map before the candidate release is inspected. The event identity formula
# is the one in the unchanged C11 facade (_event); it is reproduced here so the
# domain is not built from emitted event IDs.
# ---------------------------------------------------------------------------

def _r02v_hash(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=True).encode()
    ).hexdigest()


def _r02v_ref(kind, tag, material=None):
    return ExactRef(
        kind, f"urn:rawlsing:r56:{kind.lower()}:{tag}",
        _r02v_hash({"kind": kind, "tag": tag, "material": material}))


def _r02v_order_value(fields):
    for name in ("multiplicity_index", "semantic_ordinal", "semantic_order",
                 "semantic_order_key", "ordinal", "order", "rank", "index"):
        if name in fields:
            return fields[name]
    return None


def _r02v_order_sort_key(fields):
    value = _r02v_order_value(fields)
    if isinstance(value, bool) or value is None:
        return (2, str(value))
    if isinstance(value, int):
        return (0, value)
    return (1, str(value))


def _r02v_plan(respondents, occasions, variable="SCORE"):
    return occurrence_plan(
        ((variable, "REPEATED_EVENT", tuple(
            (str(occasion), f"occ-{occasion}",
             {"kind": "REPEATED_EVENT", "multiplicity_index": occasion})
            for occasion in range(occasions))),),
        {str(respondent): f"P{respondent}" for respondent in range(respondents)})


def _r02v_expected_domain_and_tuples(package_, incidence, plan, variable="SCORE"):
    """Return the source-derived exact I03 domain and exact event tuples."""
    authorities = build_authority_set(source=package_.source, as_of=package_.as_of)
    source_auth = authorities[0]
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_r02v_ref(
            "REPLAY_ROOT", f"universe-{package_.source.source_id}"),
        raw_source_identity=f"RAW-{package_.source.family}-{package_.source.wave}",
        source_family=package_.source.family,
        study_product_release=f"{package_.study_product_id}/{package_.release_id}",
        instrument_release=package_.instrument_release_id,
        country_geography="ZZ",
        sampling_geography="ZZ-SYNTHETIC",
        raw_wave=package_.source.wave,
        canonical_wave_if_governed=None,
        field_or_reference_time=package_.as_of,
        target_population_and_sample_frame="SYNTHETIC_SOURCEFREE",
        sampling_design_regime="TEST_ONLY",
        respondent_namespace=f"NS-{package_.source.source_id}",
        source_artifact_import_lineage=f"LINEAGE-{package_.source.source_id}",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    mapping = {token(key): str(value)
               for key, value in
               plan.respondent_key_by_source_value.items()}
    rows = {}
    for cell in incidence.iter_cells():
        rows.setdefault(cell.row_ordinal, {})[cell.variable_name] = cell
    source_tokens_by_key = {}
    for row in rows.values():
        source_key = mapping[token(
            row[plan.respondent_variable].raw_value)]
        source_tokens_by_key.setdefault(source_key, set()).add(
            token(row[plan.respondent_variable].raw_value))
    respondents = {}
    for source_key in sorted(source_tokens_by_key):
        source_ref = _r02v_ref(
            "SOURCE_RESPONDENT",
            f"{package_.source.source_id}-{source_key}",
            {"source_tokens": sorted(source_tokens_by_key[source_key])})
        respondents[source_key] = RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=f"{package_.source.source_id}:{source_key}",
            source_native_respondent_key_ref_or_typed_absence=source_ref,
            identity_map_authority_ref_or_typed_absence=TypedAbsence(
                "NOT_APPLICABLE"),
        )
    native_question_ref = _r02v_ref(
        "QUESTION_NATIVE", f"{package_.source.source_id}-{variable}",
        {"wave": package_.source.wave, "variable": variable})
    question = QuestionVariableBinding(
        empirical_universe_ref=universe.ref,
        native_question_ref=native_question_ref,
        instrument_question_version=package_.source.wave,
        canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
        component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        semantic_authority_ref=source_auth.authority_ref,
        topology_authority_ref=source_auth.authority_ref,
    )
    projection_ref = _r02v_ref(
        "C11_SEMANTIC_PROJECTION",
        f"{package_.source.source_id}-{package_.source.wave}")
    rule = next(item for item in package_.selected
                if item.source_variable_code == variable)
    variable_plan = plan.plan_by_variable[variable]
    grouped = {}
    expected_tuples = []
    for row_ordinal in sorted(rows):
        row = rows[row_ordinal]
        source_key = mapping[token(row[plan.respondent_variable].raw_value)]
        occasion_token = token(row[plan.occasion_variable].raw_value)
        binding = variable_plan.by_source_value[occasion_token]
        cell = row[variable]
        fields = dict(binding.fields)
        fields.setdefault("kind", variable_plan.topology_kind)
        envelope = {
            "schema": OCCURRENCE_BINDING_SCHEMA,
            "source_declaration": cell.source_missing_declaration,
            "occurrence_key": binding.occurrence_key,
            "source_value": binding.source_value,
            "fields": fields,
        }
        physical_key = physical_value_binding_key(
            cell.raw_value, cell.missing_state, envelope)
        material = {
            "contract": CONTRACT_ID,
            "projection": projection_ref.as_dict(),
            "source_sha": package_.source.declared_sha256,
            "row": row_ordinal,
            "respondent": respondents[source_key].ref.as_dict(),
            "question": question.ref.as_dict(),
            "slot": (cell.variable_ordinal, cell.variable_name),
            "physical_value_key": physical_key,
            "occurrence": binding.occurrence_key,
        }
        event_id = (
            "urn:rawlsing:pre553:c05r2a:event:sha256:"
            + semantic_hash({**material, "role": "EVENT"}))
        order = _r02v_order_value(fields)
        if cell.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE:
            raw_token = token(cell.raw_value)
            canonical = rule.value_aliases.get(raw_token, raw_token)
            state = "SUBSTANTIVE_RESPONSE"
            cell_value = canonical
        else:
            canonical = None
            state = "MISSING"
            cell_value = {"typed_response_state": "MISSING"}
        grouped.setdefault(source_key, []).append({
            "event_id": event_id,
            "multiplicity_order_rank_fields": fields,
            "value": cell_value,
        })
        expected_tuples.append((
            respondents[source_key].respondent_key, order, state, canonical))
    domain = [
        sorted(grouped[source_key], key=lambda event: _r02v_order_sort_key(
            event["multiplicity_order_rank_fields"]))
        for source_key in sorted(grouped)
    ]
    return domain, tuple(sorted(expected_tuples, key=str))


def _r02v_run_query(bundle, domain, variable, topology, included_states, tag):
    source = {
        "qrefs": bundle.question_refs,
        "source_auth": bundle.projection.authority_snapshots[0],
        "risk_refs": {"R": bundle.risk_set_ref},
        "universe": bundle.projection.universes[0],
        "respondents": {respondent.respondent_key: respondent
                        for respondent in bundle.projection.respondents},
        "authorities": bundle.projection.authority_snapshots,
    }
    query_authority = _query_authority(tag)
    predicate = _branch_predicate(source, query_authority, tag=tag)
    query = _custom_query(
        source, query_authority, predicate, variable, topology=topology,
        domain=domain, included_states=included_states, tag=tag)
    repository, release = build_source_backed_c11_repository(
        bundle.physical_stream, bundle.projection)
    registry = AuthorityRegistry(
        tuple((*bundle.projection.authority_snapshots, query_authority)))
    return execute_empirical_query(
        repository=repository, query=query, predicate=predicate,
        authority_registry=registry, release_refs=(release.release_ref,)).facts[0]


def _r02v_cell_set(fact):
    return {
        canonical_json(cell["cell"])
        for cell in fact.target_topology.get(
            "complete_cell_semantic_projection", [])
    }


def _r02v_baseline_fingerprint(path):
    incidence = decode_sav(path)
    package_ = package(
        path, incidence.row_count,
        (NativeSourceRule("impl.score", "SCORE"),))
    plan = _r02v_plan(4, 2)
    domain, tuples = _r02v_expected_domain_and_tuples(
        package_, incidence, plan)
    bundle = materialize_native_preimages(
        package=package_, incidence=incidence, row_occurrence_plan=plan)
    assert event_tuples(bundle) == tuples
    assert domain_from_bundle(bundle) == domain
    fact = _r02v_run_query(
        bundle, domain, "SCORE", "REPEATED_EVENT",
        ("SUBSTANTIVE_RESPONSE",), "r02v-restore")
    assert fact.typed_state == "SUPPORTED"
    return {
        "state": fact.typed_state,
        "ref": fact.ref.key,
        "denominator": fact.raw_denominator_support,
        "numerator": fact.raw_numerator_support,
        "cells": sorted(_r02v_cell_set(fact)),
    }


def test_r02v_prospective_domain_exact_tuples_permuted_and_alternative_labels(tmp_path):
    rows = []
    for respondent in range(4):
        for occasion in range(3):
            rows.append({
                "PID": float(respondent),
                "OCCASION": float(occasion),
                "SCORE": float((respondent * 5 + occasion * 2) % 4),
            })
    interleaved = rows[1::2] + rows[0::2]
    path = tmp_path / "r02v_permuted.sav"
    write_rows(path, interleaved)
    incidence = decode_sav(path)
    package_ = package(
        path, incidence.row_count,
        (NativeSourceRule("impl.score", "SCORE"),))
    plan = occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "alt-zero",
             {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
            ("1", "alt-one",
             {"kind": "REPEATED_EVENT", "multiplicity_index": 1}),
            ("2", "alt-two",
             {"kind": "REPEATED_EVENT", "multiplicity_index": 2}),
        )),),
        {str(respondent): f"ALT{respondent}" for respondent in range(4)})
    expected_domain, expected_tuples = _r02v_expected_domain_and_tuples(
        package_, incidence, plan)
    assert len(expected_tuples) == 12
    assert len(expected_domain) == 4
    bundle = materialize_native_preimages(
        package=package_, incidence=incidence, row_occurrence_plan=plan)
    assert event_tuples(bundle) == expected_tuples
    assert domain_from_bundle(bundle) == expected_domain
    fact = _r02v_run_query(
        bundle, expected_domain, "SCORE", "REPEATED_EVENT",
        ("SUBSTANTIVE_RESPONSE",), "r02v-permuted")
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 4
    assert fact.raw_numerator_support == 4
    assert _r02v_cell_set(fact) == {
        canonical_json(cell) for cell in expected_domain}


def test_r02v_prospective_domain_catches_omission_remap_and_value_fault(tmp_path):
    path = tmp_path / "r02v_fault.sav"
    rows = [
        {"PID": float(respondent), "OCCASION": float(occasion),
         "SCORE": float((respondent * 2 + occasion) % 4)}
        for respondent in range(4) for occasion in range(2)
    ]
    write_rows(path, rows)
    incidence = decode_sav(path)
    package_ = package(
        path, incidence.row_count,
        (NativeSourceRule("impl.score", "SCORE"),))
    plan = _r02v_plan(4, 2)
    expected_domain, expected_tuples = _r02v_expected_domain_and_tuples(
        package_, incidence, plan)
    baseline = materialize_native_preimages(
        package=package_, incidence=incidence, row_occurrence_plan=plan)
    baseline_fact = _r02v_run_query(
        baseline, expected_domain, "SCORE", "REPEATED_EVENT",
        ("SUBSTANTIVE_RESPONSE",), "r02v-fault-baseline")
    assert baseline_fact.typed_state == "SUPPORTED"

    baseline_cells = tuple(incidence.iter_cells())
    omitted = tuple(cell for cell in baseline_cells
                    if not (cell.row_ordinal == 1
                            and cell.variable_name == "SCORE"))
    omitted_stream = ExactPhysicalCellStream(
        source_sha256=incidence.source_sha256,
        row_count=incidence.row_count,
        cell_iter_factory=lambda: omitted)
    with pytest.raises(NativePreimageRefusal) as refusal:
        materialize_native_preimages(
            package=package_, incidence=omitted_stream,
            row_occurrence_plan=plan)
    assert refusal.value.code == "SELECTED_VARIABLE_CELL_ABSENT"

    remap_plan = occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "occ-0",
             {"kind": "REPEATED_EVENT", "multiplicity_index": 1}),
            ("1", "occ-1",
             {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
        )),),
        {str(respondent): f"P{respondent}" for respondent in range(4)})
    remapped = materialize_native_preimages(
        package=package_, incidence=incidence, row_occurrence_plan=remap_plan)
    assert event_tuples(remapped) != expected_tuples
    remapped_fact = _r02v_run_query(
        remapped, expected_domain, "SCORE", "REPEATED_EVENT",
        ("SUBSTANTIVE_RESPONSE",), "r02v-fault-remap")
    assert remapped_fact.typed_state != "SUPPORTED"
    assert remapped_fact.ref.key != baseline_fact.ref.key

    value_cells = tuple(
        replace(cell, raw_value=1.0)
        if cell.row_ordinal == 1 and cell.variable_name == "SCORE"
        else cell
        for cell in baseline_cells)
    value_stream = ExactPhysicalCellStream(
        source_sha256=incidence.source_sha256,
        row_count=incidence.row_count,
        cell_iter_factory=lambda: value_cells)
    value_bundle = materialize_native_preimages(
        package=package_, incidence=value_stream, row_occurrence_plan=plan)
    value_fact = _r02v_run_query(
        value_bundle, expected_domain, "SCORE", "REPEATED_EVENT",
        ("SUBSTANTIVE_RESPONSE",), "r02v-fault-value")
    assert value_fact.typed_state != "SUPPORTED"
    assert value_fact.ref.key != baseline_fact.ref.key

    restored = _r02v_baseline_fingerprint(path)
    script = (
        "import importlib.util,json,sys;"
        "p=sys.argv[1];f=sys.argv[2];"
        "s=importlib.util.spec_from_file_location('r02vtest',p);"
        "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
        "print(json.dumps(m._r02v_baseline_fingerprint("
        "__import__('pathlib').Path(f))))"
    )
    env = dict(os.environ, PYTHONPATH=str(REPO), PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(
        [sys.executable, "-B", "-c", script, str(Path(__file__)), str(path)],
        cwd=str(REPO), env=env, capture_output=True, text=True, timeout=120)
    assert completed.returncode == 0, completed.stderr[-3000:]
    fresh = json.loads(completed.stdout.strip().splitlines()[-1])
    assert fresh == restored


def test_r02v_missingness_is_typed_and_resolvable(tmp_path):
    path = tmp_path / "r02v_missing.sav"
    rows = s3_rows(respondents=3, occasions=2)
    rows[1]["SCORE"] = None
    write_rows(path, rows)
    incidence = decode_sav(path)
    package_ = package(
        path, incidence.row_count,
        (NativeSourceRule("impl.score", "SCORE"),))
    plan = _r02v_plan(3, 2)
    expected_domain, expected_tuples = _r02v_expected_domain_and_tuples(
        package_, incidence, plan)
    assert ("R56R02:P0", 1, "MISSING", None) in expected_tuples
    bundle = materialize_native_preimages(
        package=package_, incidence=incidence, row_occurrence_plan=plan)
    assert event_tuples(bundle) == expected_tuples
    fact = _r02v_run_query(
        bundle, expected_domain, "SCORE", "REPEATED_EVENT",
        ("SUBSTANTIVE_RESPONSE", "MISSING"), "r02v-missing-positive")
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 3
    assert fact.raw_numerator_support == 3
    assert _r02v_cell_set(fact) == {
        canonical_json(cell) for cell in expected_domain}
    substantive_only = _r02v_run_query(
        bundle, expected_domain, "SCORE", "REPEATED_EVENT",
        ("SUBSTANTIVE_RESPONSE",), "r02v-missing-substantive-only")
    assert substantive_only.typed_state != "SUPPORTED"


def test_r02v_envelope_preserves_raw_declaration_and_binds_occurrence():
    source_sha = "a" * 64
    original_declaration = {"kind": "discrete", "value": -9.0}
    cells = (
        PhysicalCell(1, 1, "PID", 1.0,
                     PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(1, 2, "OCCASION", 0.0,
                     PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(1, 3, "SCORE", -9.0,
                     PhysicalMissingState.FORMAT_USER_MISSING_VALUE,
                     original_declaration),
        PhysicalCell(2, 1, "PID", 1.0,
                     PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(2, 2, "OCCASION", 1.0,
                     PhysicalMissingState.OBSERVED_STORAGE_VALUE, None),
        PhysicalCell(2, 3, "SCORE", -9.0,
                     PhysicalMissingState.FORMAT_USER_MISSING_VALUE,
                     original_declaration),
    )
    source = NativeSourceIdentity(
        source_id=SOURCE_ID, family="SYNTHETIC", wave="W1",
        canonical_filename="envelope.sav", declared_sha256=source_sha,
        source_format="SAV", expected_rows=2)
    package_ = NativeSourcePackage(
        source=source,
        selected=(NativeSourceRule("impl.score", "SCORE"),),
        coordinate_variable="OCCASION")
    plan = occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "zero", {"kind": "REPEATED_EVENT",
                           "multiplicity_index": 0}),
            ("1", "one", {"kind": "REPEATED_EVENT",
                          "multiplicity_index": 1}),
        )),),
        {"1": "P0"})
    stream = ExactPhysicalCellStream(
        source_sha256=source_sha, row_count=2,
        cell_iter_factory=lambda: cells)
    bundle = materialize_native_preimages(
        package=package_, incidence=stream, row_occurrence_plan=plan)
    transformed = {
        (cell.row_ordinal, cell.variable_name): cell
        for cell in bundle.physical_stream.iter_cells()
    }
    transformed_scores = []
    for row_ordinal, occurrence_key, source_value in (
            (1, "zero", "0"), (2, "one", "1")):
        cell = transformed[(row_ordinal, "SCORE")]
        assert cell.raw_value == -9.0
        assert cell.missing_state is PhysicalMissingState.FORMAT_USER_MISSING_VALUE
        declaration = dict(cell.source_missing_declaration)
        assert declaration["schema"] == OCCURRENCE_BINDING_SCHEMA
        assert declaration["source_declaration"] == original_declaration
        assert declaration["occurrence_key"] == occurrence_key
        assert declaration["source_value"] == source_value
        assert declaration["fields"] == {
            "kind": "REPEATED_EVENT",
            "multiplicity_index": 0 if occurrence_key == "zero" else 1,
        }
        transformed_scores.append(cell)
    assert transformed[(1, "PID")].source_missing_declaration is None
    assert transformed[(2, "PID")].source_missing_declaration is None
    first_key = physical_value_binding_key(
        transformed_scores[0].raw_value,
        transformed_scores[0].missing_state,
        transformed_scores[0].source_missing_declaration)
    second_key = physical_value_binding_key(
        transformed_scores[1].raw_value,
        transformed_scores[1].missing_state,
        transformed_scores[1].source_missing_declaration)
    assert first_key != second_key
    identical_key = physical_value_binding_key(
        transformed_scores[0].raw_value,
        transformed_scores[0].missing_state,
        dict(transformed_scores[0].source_missing_declaration))
    assert identical_key == first_key


def test_r02v_s1_scalar_and_s2_separate_unit_positives(tmp_path):
    scalar_path = tmp_path / "r02v_s1.sav"
    scalar_rows = [
        {"A": float(i % 2), "B": float((i // 2) % 2),
         "Y": float(i % 2), "G": float(i % 2)}
        for i in range(7)
    ]
    write_rows(scalar_path, scalar_rows)
    scalar_package = package(
        scalar_path, len(scalar_rows),
        (NativeSourceRule("impl.y", "Y"),), coordinate="G")
    scalar_bundle = materialize_native_preimages(
        package=scalar_package, incidence=decode_sav(scalar_path))
    assert event_tuples(scalar_bundle, "Y") == tuple(sorted(
        (f"{SOURCE_ID}:ROW-{row:04d}", 0, "SUBSTANTIVE_RESPONSE",
         str((row - 1) % 2)) for row in range(1, 8)))
    scalar_fact = run_scalar(scalar_bundle, "Y")
    assert scalar_fact.typed_state == "SUPPORTED"
    assert scalar_fact.raw_denominator_support == 7
    assert scalar_fact.raw_numerator_support == 7
    assert {cell["raw_numerator_support"] for cell in
            scalar_fact.target_topology["complete_cell_semantic_projection"]} == {
        3, 4}

    person_path = tmp_path / "r02v_s2_person.sav"
    person_rows = [{"PID": float(i), "OUTCOME": float(i % 2)}
                   for i in range(1, 4)]
    write_rows(person_path, person_rows)
    person_package = package(
        person_path, len(person_rows),
        (NativeSourceRule("impl.outcome", "OUTCOME", unit="person"),),
        coordinate="PID")
    person_bundle = materialize_native_preimages(
        package=person_package, incidence=decode_sav(person_path))
    assert event_tuples(person_bundle, "OUTCOME") == tuple(sorted(
        (f"{SOURCE_ID}:ROW-{row:04d}", 0, "SUBSTANTIVE_RESPONSE",
         str(row % 2)) for row in range(1, 4)))
    person_fact = run_scalar(person_bundle, "OUTCOME")
    assert person_fact.typed_state == "SUPPORTED"
    assert person_fact.raw_denominator_support == 3

    household_path = tmp_path / "r02v_s2_household.sav"
    household_rows = [{"HID": float(10 * i), "HMEAS": float(i % 2)}
                      for i in range(1, 4)]
    write_rows(household_path, household_rows)
    household_package = package(
        household_path, len(household_rows),
        (NativeSourceRule("impl.h", "HMEAS", unit="household"),),
        coordinate="HID")
    household_bundle = materialize_native_preimages(
        package=household_package, incidence=decode_sav(household_path))
    assert event_tuples(household_bundle, "HMEAS") == tuple(sorted(
        (f"{SOURCE_ID}:ROW-{row:04d}", 0, "SUBSTANTIVE_RESPONSE",
         str(row % 2)) for row in range(1, 4)))
    household_fact = run_scalar(household_bundle, "HMEAS")
    assert household_fact.typed_state == "SUPPORTED"
    assert household_fact.raw_denominator_support == 3
    assert (person_bundle.release.release_ref
            != household_bundle.release.release_ref)

    with pytest.raises(NativePreimageRefusal) as caught:
        package(
            household_path, len(household_rows),
            (NativeSourceRule("impl.h", "HMEAS", unit="household"),
             NativeSourceRule("impl.p", "OUTCOME", unit="person")),
            coordinate="HID",
            units={"HMEAS": "household", "OUTCOME": "person"})
    assert caught.value.code == "CROSS_UNIT_POOLING_UNAUTHORIZED"


def test_r02v_incomplete_order_fields_do_not_fabricate_support(tmp_path):
    path = tmp_path / "r02v_incomplete_order.sav"
    rows = [{"PID": 0.0, "OCCASION": 0.0, "SCORE": 7.0},
            {"PID": 1.0, "OCCASION": 1.0, "SCORE": 9.0}]
    write_rows(path, rows)
    incidence = decode_sav(path)
    package_ = package(
        path, incidence.row_count,
        (NativeSourceRule("impl.score", "SCORE"),))
    plan = occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "zero", {"kind": "REPEATED_EVENT"}),
            ("1", "one", {"kind": "REPEATED_EVENT"}),
        )),),
        {"0": "P0", "1": "P1"})
    bundle = materialize_native_preimages(
        package=package_, incidence=incidence, row_occurrence_plan=plan)
    domain, _ = _r02v_expected_domain_and_tuples(
        package_, incidence, plan)
    fact = _r02v_run_query(
        bundle, domain, "SCORE", "REPEATED_EVENT",
        ("SUBSTANTIVE_RESPONSE",), "r02v-incomplete-order")
    assert fact.typed_state in {"INTEGRITY_FAILURE", "UNRESOLVED"}
    assert fact.typed_state != "SUPPORTED"


def test_r02v_normalized_duplicate_respondent_key_is_refused(tmp_path):
    path = tmp_path / "r02v_normalized_key.sav"
    rows = [{"PID": 0.0, "OCCASION": 0.0, "SCORE": 7.0},
            {"PID": 1.0, "OCCASION": 1.0, "SCORE": 9.0}]
    write_rows(path, rows)
    incidence = decode_sav(path)
    package_ = package(
        path, incidence.row_count,
        (NativeSourceRule("impl.score", "SCORE"),))
    plan = occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "zero", {"kind": "REPEATED_EVENT",
                           "multiplicity_index": 0}),
            ("1", "one", {"kind": "REPEATED_EVENT",
                          "multiplicity_index": 1}),
        )),),
        {0: "1", 1: 1})
    with pytest.raises(NativePreimageRefusal) as caught:
        materialize_native_preimages(
            package=package_, incidence=incidence, row_occurrence_plan=plan)
    assert caught.value.code == "DUPLICATE_RESPONDENT_KEY_MAPPING"


def test_r02v_ambiguous_normalized_source_key_is_refused(tmp_path):
    path = tmp_path / "r02v_ambiguous_key.sav"
    rows = [{"PID": 0.0, "OCCASION": 0.0, "SCORE": 7.0},
            {"PID": 1.0, "OCCASION": 1.0, "SCORE": 9.0}]
    write_rows(path, rows)
    incidence = decode_sav(path)
    package_ = package(
        path, incidence.row_count,
        (NativeSourceRule("impl.score", "SCORE"),))
    plan = occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "zero", {"kind": "REPEATED_EVENT",
                           "multiplicity_index": 0}),
            ("1", "one", {"kind": "REPEATED_EVENT",
                          "multiplicity_index": 1}),
        )),),
        {0: "P0", "0": "P1", 1: "P2"})
    with pytest.raises(NativePreimageRefusal):
        materialize_native_preimages(
            package=package_, incidence=incidence, row_occurrence_plan=plan)


def test_r02v_mr_rank_admin_are_consumed_at_their_topology(tmp_path):
    path = tmp_path / "r02v_mr_rank.sav"
    rows = []
    for respondent in range(2):
        for occasion in range(2):
            rows.append({
                "PID": float(respondent),
                "OCCASION": float(occasion),
                "MR1": float(respondent) if occasion == 0 else None,
                "RANK1": float(respondent) if occasion == 0 else None,
                "OTHER": 1.0,
            })
    write_rows(path, rows)
    incidence = decode_sav(path)
    package_ = package(
        path, incidence.row_count,
        (NativeSourceRule("impl.mr", "MR1"),
         NativeSourceRule("impl.rank", "RANK1"),
         NativeSourceRule("impl.other", "OTHER", administered=False)),
        coordinate="OCCASION")
    plan = occurrence_plan(
        (("MR1", "MULTISELECT", (
            ("0", "mr-0", {"kind": "MULTISELECT", "multiplicity_index": 0}),
            ("1", "mr-1", {"kind": "MULTISELECT", "multiplicity_index": 1}),
        )),
         ("RANK1", "ORDERED_SEQUENCE", (
             ("0", "rank-0", {"kind": "ORDERED_SEQUENCE",
                              "semantic_ordinal": 0}),
             ("1", "rank-1", {"kind": "ORDERED_SEQUENCE",
                              "semantic_ordinal": 1}),
         ))),
        {"0": "P0", "1": "P1"})
    bundle = materialize_native_preimages(
        package=package_, incidence=incidence, row_occurrence_plan=plan)
    assert [item.classification for item in bundle.held] == [
        "HELD_NOT_ADMINISTERED"]
    assert set(bundle.question_refs) == {"MR1", "RANK1"}
    events = [event for event in bundle.release.public_objects
              if isinstance(event, RespondentEvent)]
    assert {dict(event.multiplicity_order_rank_fields)["kind"]
            for event in events} == {"MULTISELECT", "ORDERED_SEQUENCE"}
    assert len([event for event in events
                if event.typed_state == "SUBSTANTIVE_RESPONSE"]) == 4
    assert len([event for event in events
                if event.typed_state == "MISSING"]) == 4
    multiselect_domain = [["0"], ["1"]]
    ordered_domain = [["0"], ["1"]]
    multiselect_fact = _r02v_run_query(
        bundle, multiselect_domain, "MR1", "MULTISELECT",
        ("SUBSTANTIVE_RESPONSE",), "r02v-multiselect")
    assert multiselect_fact.typed_state == "SUPPORTED"
    assert multiselect_fact.raw_denominator_support == 2
    assert _r02v_cell_set(multiselect_fact) == {
        canonical_json(cell) for cell in multiselect_domain}
    ordered_fact = _r02v_run_query(
        bundle, ordered_domain, "RANK1", "ORDERED_SEQUENCE",
        ("SUBSTANTIVE_RESPONSE",), "r02v-ordered")
    assert ordered_fact.typed_state == "SUPPORTED"
    assert ordered_fact.raw_denominator_support == 2
    assert _r02v_cell_set(ordered_fact) == {
        canonical_json(cell) for cell in ordered_domain}
