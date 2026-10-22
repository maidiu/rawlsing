from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import RespondentEvent
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_source_backed_c11_facade import (
    build_source_backed_c11_repository,
)
from rawlsing_next.pre553_source_native_preimage_adapter import (
    GovernedRowOccurrencePlan,
    NativePreimageRefusal,
    NativeSourceIdentity,
    NativeSourcePackage,
    NativeSourceRule,
    OccurrenceBinding,
    VariableOccurrencePlan,
    materialize_native_preimages,
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
