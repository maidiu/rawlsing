"""C1 combined-path receipt: accepted R04 decoder -> R02 adapter -> facade/C11 -> I03.

Prints exact source/identity/tuples/domain/fact values and custody attack results.
"""
import hashlib
import json
import mmap
import os
import sys
import tempfile
from pathlib import Path

REPO = Path.cwd()
sys.path.insert(0, str(REPO))

from rawlsing_next.pre553_physical_decoder import decode_dta, decode_sav  # noqa: E402
from rawlsing_next.pre553_source_native_preimage_adapter import (  # noqa: E402
    NativePreimageRefusal,
    NativeSourceRule,
    materialize_native_preimages,
)
from rawlsing_next.tests.test_universal_source_projection import (  # noqa: E402
    _r02v_expected_domain_and_tuples,
    _r02v_plan,
    domain_from_bundle,
    event_tuples,
    occurrence_plan,
    package,
    run_repeated,
    write_rows,
)


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(n, m, mutate=None):
    out = []
    for r in range(n):
        for o in range(m):
            v = (r * 2 + o) % 4
            if mutate == (r, o):
                v = (v + 1) % 4
            out.append({"PID": float(r), "OCCASION": float(o), "SCORE": float(v)})
    return out


def _load(path, fmt, n, m):
    decoder = decode_sav if fmt == "sav" else decode_dta
    digest = _sha(path)
    incidence = decoder(path, expected_source_sha256=digest)
    rules = (NativeSourceRule("impl.score", "SCORE"),)
    pkg = package(path, incidence.row_count, rules, source_format=fmt.upper())
    plan = _r02v_plan(n, m)
    expected_domain, expected_tuples = _r02v_expected_domain_and_tuples(pkg, incidence, plan)
    bundle = materialize_native_preimages(package=pkg, incidence=incidence,
                                         row_occurrence_plan=plan)
    return incidence, pkg, plan, expected_domain, expected_tuples, bundle, digest


def positive(composite_sha):
    receipt = {"composite_sha": composite_sha, "components": {}}
    tmp = Path(tempfile.mkdtemp(prefix="c1-combined-"))
    for fmt in ("sav", "dta"):
        path = tmp / f"combined.{fmt}"
        write_rows(path, _rows(4, 2), fmt=fmt)
        digest = _sha(path)
        incidence, _p, _pl, domain, tuples, bundle, loaded = _load(path, fmt, 4, 2)
        try:
            fact = run_repeated(bundle, domain)
            receipt["components"][fmt] = {
                "source_bytes": path.stat().st_size,
                "source_sha256": digest,
                "loaded_source_sha256": loaded,
                "source_format": incidence.source_format,
                "custody": dict(incidence.source_custody),
                "source_artifact_hash": bundle.release.source_artifact_ref.content_hash,
                "release_content_hash": bundle.release.release_ref.content_hash,
                "tuples": [list(row) for row in tuples],
                "domain": domain,
                "fact_ref": fact.ref.content_hash,
                "typed_state": fact.typed_state,
                "denominator": fact.raw_denominator_support,
                "numerator": fact.raw_numerator_support,
                "cells": fact.target_topology["complete_cell_semantic_projection"],
            }
        finally:
            incidence.close()
    return receipt


def custody_and_faults():
    tmp = Path(tempfile.mkdtemp(prefix="c1-custody-"))
    path = tmp / "custody.sav"
    write_rows(path, _rows(4, 2))
    original_bytes = path.read_bytes()
    digest = _sha(path)
    incidence = decode_sav(path, expected_source_sha256=digest)
    rules = (NativeSourceRule("impl.score", "SCORE"),)
    pkg = package(path, incidence.row_count, rules)
    plan = _r02v_plan(4, 2)
    domain, tuples = _r02v_expected_domain_and_tuples(pkg, incidence, plan)
    baseline_bundle = materialize_native_preimages(package=pkg, incidence=incidence,
                                                   row_occurrence_plan=plan)
    baseline_fact = run_repeated(baseline_bundle, domain)
    snapshot = incidence._source_snapshot
    out = {
        "baseline_fact_ref": baseline_fact.ref.content_hash,
        "baseline_tuples": [list(row) for row in tuples],
        "reader_access_mode": snapshot.access_mode,
    }

    # path replacement after acquisition
    write_rows(path, _rows(4, 2, mutate=(1, 0)))
    rebuilt = materialize_native_preimages(package=pkg, incidence=incidence,
                                           row_occurrence_plan=plan)
    out["original_path_replacement_same_fact"] = (
        run_repeated(rebuilt, domain).ref == baseline_fact.ref)
    foreign = tmp / "foreign.sav"
    write_rows(foreign, _rows(4, 2))
    os.replace(foreign, snapshot.path)
    rebuilt = materialize_native_preimages(package=pkg, incidence=incidence,
                                           row_occurrence_plan=plan)
    out["private_path_replacement_same_fact"] = (
        run_repeated(rebuilt, domain).ref == baseline_fact.ref)
    out["foreign_survives_read"] = snapshot.path.exists()
    denials = {}
    for name, fn in {
        "write": lambda: os.write(snapshot.fd, b"x"),
        "pwrite": lambda: os.pwrite(snapshot.fd, original_bytes, 0),
        "ftruncate": lambda: os.ftruncate(snapshot.fd, 1),
        "mmap_write": lambda: mmap.mmap(snapshot.fd, 0, access=mmap.ACCESS_WRITE),
        "reopen_O_RDWR": lambda: os.open(f"/dev/fd/{snapshot.fd}", os.O_RDWR),
    }.items():
        try:
            value = fn()
            if hasattr(value, "close"):
                value.close()
            elif isinstance(value, int):
                os.close(value)
            denials[name] = "NOT_DENIED"
        except OSError as exc:
            denials[name] = f"denied errno={exc.errno}"
    out["fd_denials"] = denials
    out["digest_after_denials"] = hashlib.sha256(
        os.pread(snapshot.fd, snapshot.size, 0)).hexdigest() == digest
    out["fact_after_denials_same"] = (
        run_repeated(materialize_native_preimages(
            package=pkg, incidence=incidence, row_occurrence_plan=plan), domain).ref
        == baseline_fact.ref)
    collision_plan = occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "occ-0", {"kind": "REPEATED_EVENT", "multiplicity_index": 0}),
            ("1", "occ-1", {"kind": "REPEATED_EVENT", "multiplicity_index": 1}),
        )),),
        {0.0: "P0", "0": "P1", 1: "P2"})
    try:
        materialize_native_preimages(package=pkg, incidence=incidence,
                                     row_occurrence_plan=collision_plan)
        out["collision_refusal"] = None
    except NativePreimageRefusal as exc:
        out["collision_refusal"] = exc.code
    incidence.close()
    out["foreign_survives_close"] = snapshot.path.exists()
    if snapshot.path.exists():
        snapshot.path.unlink()
    try:
        snapshot.directory.rmdir()
    except OSError:
        pass

    # value fault then exact restore
    fault_path = tmp / "fault.sav"
    write_rows(fault_path, _rows(4, 2))
    fault_original_bytes = fault_path.read_bytes()
    fault_digest = _sha(fault_path)
    fault_inc = decode_sav(fault_path, expected_source_sha256=fault_digest)
    fault_pkg = package(fault_path, fault_inc.row_count, rules)
    fault_plan = _r02v_plan(4, 2)
    fault_domain, _ = _r02v_expected_domain_and_tuples(fault_pkg, fault_inc, fault_plan)
    fault_bundle = materialize_native_preimages(
        package=fault_pkg, incidence=fault_inc, row_occurrence_plan=fault_plan)
    baseline_fault_fact = run_repeated(fault_bundle, fault_domain)
    fault_inc.close()
    write_rows(fault_path, _rows(4, 2, mutate=(1, 0)))
    changed_digest = _sha(fault_path)
    changed_inc = decode_sav(fault_path, expected_source_sha256=changed_digest)
    changed_pkg = package(fault_path, changed_inc.row_count, rules)
    changed_domain, _ = _r02v_expected_domain_and_tuples(changed_pkg, changed_inc, fault_plan)
    changed_bundle = materialize_native_preimages(
        package=changed_pkg, incidence=changed_inc, row_occurrence_plan=fault_plan)
    changed_fact = run_repeated(changed_bundle, changed_domain)
    changed_inc.close()
    out["value_fault_changes_same_query"] = (
        changed_fact.ref != baseline_fault_fact.ref
        or changed_fact.typed_state != baseline_fault_fact.typed_state)
    fault_path.write_bytes(fault_original_bytes)
    restored_inc = decode_sav(fault_path, expected_source_sha256=fault_digest)
    restored_pkg = package(fault_path, restored_inc.row_count, rules)
    restored_domain, _ = _r02v_expected_domain_and_tuples(
        restored_pkg, restored_inc, fault_plan)
    restored_bundle = materialize_native_preimages(
        package=restored_pkg, incidence=restored_inc, row_occurrence_plan=fault_plan)
    restored_fact = run_repeated(restored_bundle, restored_domain)
    restored_inc.close()
    out["restore_same_fact"] = restored_fact.ref == baseline_fault_fact.ref
    return out


if __name__ == "__main__":
    composite = sys.argv[1] if len(sys.argv) > 1 else "UNKNOWN"
    print(json.dumps({
        "positive": positive(composite),
        "custody_and_faults": custody_and_faults(),
    }, indent=2, sort_keys=True, default=str))
