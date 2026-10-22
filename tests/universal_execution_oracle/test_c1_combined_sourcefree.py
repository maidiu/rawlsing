"""R56-C1 focused combined-candidate compatibility tests.

Actual path: accepted R04 decoder -> accepted R02 materialize_native_preimages
-> unchanged facade/C11 -> unchanged I03 consumer, plus the accepted R00 gate on
independently pinned policy.  Two claims are kept distinct: native
projection/custody compatibility, and R00 policy/claim-ceiling enforcement.
R08/R09 authenticated native association/authentication is NOT_IMPLEMENTED.
"""
from __future__ import annotations

import copy
import dataclasses
import hashlib
import importlib.util
import json
import mmap
import os
import subprocess
import sys
from pathlib import Path

import pytest

from CROSS_HQ_CONTROL_ROOM.universal_promotion_gate import (
    DEFAULT_COMMIT,
    DEFAULT_ROOT,
    evaluate_r56_sourcefree_claim,
    load_pinned_policy,
)
from rawlsing_next.pre553_physical_decoder import decode_dta, decode_sav
from rawlsing_next.pre553_source_native_preimage_adapter import (
    NativePreimageRefusal,
    NativeSourceRule,
    materialize_native_preimages,
)
from rawlsing_next.tests.test_universal_source_projection import (
    _r02v_expected_domain_and_tuples,
    _r02v_plan,
    domain_from_bundle,
    event_tuples,
    occurrence_plan,
    package,
    run_repeated,
    write_rows,
)

REPO = Path(__file__).resolve().parents[2]
R00_LOCKED_POLICY_COMMIT = DEFAULT_COMMIT
R00_LOCKED_POLICY_ROOT = DEFAULT_ROOT


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(respondents: int, occasions: int, mutate=None):
    rows = []
    for respondent in range(respondents):
        for occasion in range(occasions):
            value = (respondent * 2 + occasion) % 4
            if mutate == (respondent, occasion):
                value = (value + 1) % 4
            rows.append({
                "PID": float(respondent),
                "OCCASION": float(occasion),
                "SCORE": float(value),
            })
    return rows


def _load(path: Path, fmt: str, respondents: int, occasions: int, *, plan=None):
    decoder = decode_sav if fmt == "sav" else decode_dta
    digest = _sha(path)
    incidence = decoder(path, expected_source_sha256=digest)
    rules = (NativeSourceRule("impl.score", "SCORE"),)
    pkg = package(path, incidence.row_count, rules, source_format=fmt.upper())
    plan = plan or _r02v_plan(respondents, occasions)
    expected_domain, expected_tuples = _r02v_expected_domain_and_tuples(
        pkg, incidence, plan)
    bundle = materialize_native_preimages(
        package=pkg, incidence=incidence, row_occurrence_plan=plan)
    return incidence, pkg, plan, expected_domain, expected_tuples, bundle, digest


def _combined_fingerprint(path: Path, fmt: str = "sav", respondents: int = 4,
                          occasions: int = 2) -> dict:
    incidence, _pkg, _plan, expected_domain, expected_tuples, bundle, digest = _load(
        path, fmt, respondents, occasions)
    try:
        fact = run_repeated(bundle, expected_domain)
        return {
            "source_sha256": digest,
            "physical_source_format": incidence.source_format,
            "reader_access_mode": incidence.source_custody["reader_access_mode"],
            "snapshot_sha256": incidence.source_custody["snapshot_sha256"],
            "release_content_hash": bundle.release.release_ref.content_hash,
            "source_artifact_hash": bundle.release.source_artifact_ref.content_hash,
            "fact_ref": fact.ref.content_hash,
            "typed_state": fact.typed_state,
            "denominator": fact.raw_denominator_support,
            "numerator": fact.raw_numerator_support,
            "tuples": [list(row) for row in expected_tuples],
            "domain": expected_domain,
        }
    finally:
        incidence.close()


def test_c1_combined_sav_and_dta_exact_source_tuples_domain_and_fact(tmp_path):
    for fmt in ("sav", "dta"):
        respondents, occasions = 4, 2
        path = tmp_path / f"combined_positive.{fmt}"
        write_rows(path, _rows(respondents, occasions), fmt=fmt)
        digest = _sha(path)
        incidence, pkg, plan, expected_domain, expected_tuples, bundle, loaded = _load(
            path, fmt, respondents, occasions)
        try:
            assert loaded == digest
            assert incidence.source_sha256 == digest
            custody = dict(incidence.source_custody)
            assert custody["snapshot_sha256"] == digest
            assert custody["reader_access_mode"] == "O_RDONLY"
            assert custody["reader_binding"] == "OPEN_FD_VIA_POSIX_DEV_FD"
            assert bundle.release.source_artifact_ref.content_hash == digest
            assert len(expected_tuples) == respondents * occasions
            assert len(expected_domain) == respondents
            assert event_tuples(bundle) == expected_tuples
            assert domain_from_bundle(bundle) == expected_domain
            fact = run_repeated(bundle, expected_domain)
            assert fact.typed_state == "SUPPORTED"
            assert fact.raw_denominator_support == respondents
            assert fact.raw_numerator_support == respondents
            cells = fact.target_topology["complete_cell_semantic_projection"]
            assert len(cells) == respondents
            assert {cell["raw_numerator_support"] for cell in cells} == {1}
            again = run_repeated(bundle, expected_domain)
            assert again.ref == fact.ref
        finally:
            incidence.close()


def test_c1_combined_order_and_cardinality_composition(tmp_path):
    baseline_path = tmp_path / "combined_order_a.sav"
    rows = _rows(4, 2)
    write_rows(baseline_path, rows)
    base_inc, _bp, _bpl, base_domain, base_tuples, base_bundle, _ = _load(
        baseline_path, "sav", 4, 2)
    try:
        permuted_path = tmp_path / "combined_order_b.sav"
        write_rows(permuted_path, list(reversed(rows)))
        perm_inc, _pp, _ppl, perm_domain, perm_tuples, perm_bundle, _ = _load(
            permuted_path, "sav", 4, 2)
        try:
            assert perm_tuples == base_tuples
            # Event ids bind the source sha, so a different file order has a
            # different identity; compare the exact respondent/occasion/value
            # projection and the consumer denominator instead.
            def shape(domain):
                return [[(event["value"],
                          event["multiplicity_order_rank_fields"])
                         for event in events] for events in domain]
            assert shape(perm_domain) == shape(base_domain)
            assert perm_bundle.release.release_ref != base_bundle.release.release_ref
            assert run_repeated(perm_bundle, perm_domain).raw_denominator_support == 4
        finally:
            perm_inc.close()
    finally:
        base_inc.close()

    larger_path = tmp_path / "combined_cardinality.sav"
    write_rows(larger_path, _rows(5, 2))
    inc, _p, _pl, domain, tuples, bundle, _ = _load(larger_path, "sav", 5, 2)
    try:
        assert len(tuples) == 10
        assert len(domain) == 5
        fact = run_repeated(bundle, domain)
        assert fact.typed_state == "SUPPORTED"
        assert fact.raw_denominator_support == 5
    finally:
        inc.close()


def test_c1_combined_dta_separate_units_refuse_before_c11(tmp_path):
    path = tmp_path / "combined_separate_units.dta"
    write_rows(path, [{"HID": 1.0, "PID": 1.0, "HMEAS": 1.0,
                       "OUTCOME": 1.0, "OCCASION": 0.0}], fmt="dta")
    with pytest.raises(NativePreimageRefusal) as caught:
        package(
            path, 1,
            (NativeSourceRule("impl.h", "HMEAS", unit="household"),
             NativeSourceRule("impl.o", "OUTCOME", unit="person")),
            coordinate="HID",
            units={"HMEAS": "household", "OUTCOME": "person"},
            source_format="DTA")
    assert caught.value.code == "CROSS_UNIT_POOLING_UNAUTHORIZED"


def test_c1_combined_custody_attacks_preserve_bound_facts(tmp_path, monkeypatch):
    path = tmp_path / "combined_custody.sav"
    write_rows(path, _rows(4, 2))
    incidence, pkg, plan, domain, tuples, baseline_bundle, digest = _load(
        path, "sav", 4, 2)
    snapshot = incidence._source_snapshot
    baseline_fact = run_repeated(baseline_bundle, domain)
    try:
        # Original-path replacement after acquisition.
        write_rows(path, _rows(4, 2, mutate=(1, 0)))
        assert _sha(path) != digest
        rebuilt = materialize_native_preimages(
            package=pkg, incidence=incidence, row_occurrence_plan=plan)
        assert event_tuples(rebuilt) == tuples
        assert rebuilt.release.release_ref == baseline_bundle.release.release_ref
        assert run_repeated(rebuilt, domain).ref == baseline_fact.ref

        # Foreign file at the old private snapshot pathname.
        foreign = tmp_path / "combined_foreign.sav"
        write_rows(foreign, _rows(4, 2))
        os.replace(foreign, snapshot.path)
        rebuilt = materialize_native_preimages(
            package=pkg, incidence=incidence, row_occurrence_plan=plan)
        assert run_repeated(rebuilt, domain).ref == baseline_fact.ref
        assert snapshot.path.exists()

        # Supplied-fd write capability denials.
        alternate_bytes = path.read_bytes()
        for attempt in (
            lambda: os.write(snapshot.fd, b"x"),
            lambda: os.pwrite(snapshot.fd, alternate_bytes, 0),
            lambda: os.ftruncate(snapshot.fd, len(alternate_bytes)),
            lambda: mmap.mmap(snapshot.fd, 0, access=mmap.ACCESS_WRITE),
            lambda: os.open(f"/dev/fd/{snapshot.fd}", os.O_RDWR),
        ):
            with pytest.raises(OSError):
                result = attempt()
                if hasattr(result, "close"):
                    result.close()
        assert snapshot.access_mode == "O_RDONLY"
        assert incidence.verify_source_identity() == digest
        rebuilt = materialize_native_preimages(
            package=pkg, incidence=incidence, row_occurrence_plan=plan)
        assert run_repeated(rebuilt, domain).ref == baseline_fact.ref
    finally:
        incidence.close()
    assert snapshot.path.exists()
    snapshot.path.unlink()
    try:
        snapshot.directory.rmdir()
    except OSError:
        pass


def test_c1_combined_collision_and_value_fault_same_assertion_restore(tmp_path):
    path = tmp_path / "combined_fault.sav"
    write_rows(path, _rows(4, 2))
    original_bytes = path.read_bytes()
    digest = _sha(path)
    incidence = decode_sav(path, expected_source_sha256=digest)
    rules = (NativeSourceRule("impl.score", "SCORE"),)
    pkg = package(path, incidence.row_count, rules)
    plan = _r02v_plan(4, 2)
    domain, _tuples = _r02v_expected_domain_and_tuples(pkg, incidence, plan)
    baseline_bundle = materialize_native_preimages(
        package=pkg, incidence=incidence, row_occurrence_plan=plan)
    baseline_fact = run_repeated(baseline_bundle, domain)
    baseline_fingerprint = _combined_fingerprint(path)

    collision_plan = occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "occ-0", {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
            ("1", "occ-1", {"kind": "REPEATED_EVENT", "multiplicity_index": 1}),
        )),),
        {0.0: "P0", "0": "P1", 1: "P2"})
    with pytest.raises(NativePreimageRefusal) as caught:
        materialize_native_preimages(
            package=pkg, incidence=incidence, row_occurrence_plan=collision_plan)
    assert caught.value.code == "DUPLICATE_NORMALIZED_SOURCE_KEY"

    duplicate_destination = occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "occ-0", {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
            ("1", "occ-1", {"kind": "REPEATED_EVENT", "multiplicity_index": 1}),
        )),),
        {0.0: "1", 1: 1})
    with pytest.raises(NativePreimageRefusal) as caught:
        materialize_native_preimages(
            package=pkg, incidence=incidence,
            row_occurrence_plan=duplicate_destination)
    assert caught.value.code == "DUPLICATE_RESPONDENT_KEY_MAPPING"

    # Permitted source value fault: same query/domain, fact changes or refuses.
    write_rows(path, _rows(4, 2, mutate=(1, 0)))
    fault_digest = _sha(path)
    fault_inc = decode_sav(path, expected_source_sha256=fault_digest)
    fault_pkg = package(path, fault_inc.row_count, rules)
    fault_plan = _r02v_plan(4, 2)
    fault_bundle = materialize_native_preimages(
        package=fault_pkg, incidence=fault_inc, row_occurrence_plan=fault_plan)
    fault_fact = run_repeated(fault_bundle, domain)
    assert fault_fact.ref != baseline_fact.ref or fault_fact.typed_state != "SUPPORTED"
    fault_inc.close()

    # Restore exact original bytes and reproduce the same fact in-process.
    path.write_bytes(original_bytes)
    restored_inc = decode_sav(path, expected_source_sha256=digest)
    restored_pkg = package(path, restored_inc.row_count, rules)
    restored_plan = _r02v_plan(4, 2)
    restored_domain, _restored_tuples = _r02v_expected_domain_and_tuples(
        restored_pkg, restored_inc, restored_plan)
    restored_bundle = materialize_native_preimages(
        package=restored_pkg, incidence=restored_inc,
        row_occurrence_plan=restored_plan)
    restored_fact = run_repeated(restored_bundle, restored_domain)
    assert restored_fact.ref == baseline_fact.ref
    restored_inc.close()


def test_c1_combined_value_fault_fresh_restore(tmp_path):
    path = tmp_path / "combined_restore.sav"
    write_rows(path, _rows(4, 2))
    original_bytes = path.read_bytes()
    baseline = _combined_fingerprint(path)
    write_rows(path, _rows(4, 2, mutate=(1, 0)))
    assert _sha(path) != baseline["source_sha256"]

    script = (
        "import importlib.util, json, sys;"
        "spec=importlib.util.spec_from_file_location('c1test', sys.argv[1]);"
        "module=importlib.util.module_from_spec(spec);"
        "spec.loader.exec_module(module);"
        "print(json.dumps(module._combined_fingerprint("
        "__import__('pathlib').Path(sys.argv[2])), sort_keys=True))"
    )
    env = dict(os.environ, PYTHONPATH=str(REPO), PYTHONDONTWRITEBYTECODE="1")

    def fresh(path):
        completed = subprocess.run(
            [sys.executable, "-B", "-c", script, str(Path(__file__)), str(path)],
            cwd=str(REPO), env=env, capture_output=True, text=True, timeout=180)
        assert completed.returncode == 0, completed.stderr[-3000:]
        return json.loads(completed.stdout.strip().splitlines()[-1])

    fault = fresh(path)
    assert fault["fact_ref"] != baseline["fact_ref"] or fault["typed_state"] != baseline["typed_state"]
    path.write_bytes(original_bytes)
    restored = fresh(path)
    assert restored == baseline


def _gate_handle():
    return load_pinned_policy(R00_LOCKED_POLICY_COMMIT, R00_LOCKED_POLICY_ROOT,
                              "CANONICAL_V1")


def _gate_claim(handle):
    return {
        "contract_id": "R56-R00P-CLAIM-TRANSITION-GATE@1.1.0",
        "request": {"claim_grade": "LOCAL_OPERATOR", "claim_kind": "POLICY_ONLY"},
        "external_policy_resolution": {"variant_id": "CANONICAL_V1"},
        "submitted": {"operation_objects": [copy.deepcopy(dict(row))
                                            for row in handle.expected_operations]},
    }


def test_c1_r00_policy_only_positive_and_frontier_ceiling():
    handle = _gate_handle()
    claim = _gate_claim(handle)
    positive = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
    assert positive["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"
    assert positive["grade_ceiling"] == "LOCAL_ONLY_POLICY_CONSISTENT"

    missing = copy.deepcopy(claim)
    missing["submitted"]["operation_objects"] = missing["submitted"]["operation_objects"][:-1]
    assert evaluate_r56_sourcefree_claim(
        missing, externally_pinned_policy=handle)["decision"] == "REFUSE_FRONTIER"

    altered = copy.deepcopy(claim)
    altered["submitted"]["operation_objects"][0]["operation_id"] = "OP.TEST.SUBSTITUTED"
    assert evaluate_r56_sourcefree_claim(
        altered, externally_pinned_policy=handle)["decision"] == "REFUSE_FRONTIER"

    native = copy.deepcopy(claim)
    native["request"]["claim_kind"] = "EXECUTED_NATIVE"
    native_decision = evaluate_r56_sourcefree_claim(
        native, externally_pinned_policy=handle)
    assert native_decision["decision"] in {
        "HOLD_TRUSTED_NATIVE", "REFUSE_FORGED_EVIDENCE", "REFUSE_AUTHORITY"}
    assert native_decision["grade_ceiling"] != "NATIVE_AUTHENTICATED"

    generic = copy.deepcopy(claim)
    generic["request"]["claim_grade"] = "GENERIC_SOURCEFREE"
    assert evaluate_r56_sourcefree_claim(
        generic, externally_pinned_policy=handle)["decision"] == "HOLD_GENERIC_R09"

    marker = copy.deepcopy(claim)
    marker["submitted"]["K_mutation"] = {"field": "value", "from": "a", "to": "b"}
    marker_decision = evaluate_r56_sourcefree_claim(
        marker, externally_pinned_policy=handle)
    assert marker_decision["decision"] == "REFUSE_IDENTITY"
    # K_mutation is the gate's own conflict marker; it is NOT native association
    # verification. No authenticated native binding is claimed here.

    substituted_ops = [copy.deepcopy(dict(row)) for row in handle.expected_operations]
    substituted_ops[0]["operation_id"] = "OP.TEST.POLICY_SUBSTITUTION"
    substituted = dataclasses.replace(
        handle, expected_operations=tuple(substituted_ops),
        expected_ids=tuple(row["operation_id"] for row in substituted_ops))
    assert evaluate_r56_sourcefree_claim(
        claim, externally_pinned_policy=substituted)["decision"] == "REFUSE_FRONTIER"
    restored = dataclasses.replace(handle)
    assert evaluate_r56_sourcefree_claim(
        claim, externally_pinned_policy=restored)["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"
