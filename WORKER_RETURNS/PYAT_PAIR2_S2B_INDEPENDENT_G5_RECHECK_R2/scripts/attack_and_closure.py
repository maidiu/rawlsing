"""Independent G5-R1 recheck: malformed coverage typed refusal + fd closure.

Runs the original physical-rehash-only attack against both direct and derived
certificates, plus malformed-object/body variants. The untouched original
certificate must still cold-open and select.
"""
import json
import os
import shutil
import sqlite3
import tempfile
from dataclasses import replace
from pathlib import Path

from rawlsing_next._pre553_external_i02_certificate import (
    ExternalI02IntegrityError, VerifiedExternalI02, _digest_file,
    _logical_root, build_sourcefree_external_i02,
)
from rawlsing_next.tests.test_pre553_direct_i02_sourcefree import (
    _build_direct, _direct,
)
from rawlsing_next.tests.test_pre553_verified_semantic_range import (
    _build_source, _release,
)
from rawlsing_next.pre553_empirical_objects import exact_ref


def _cases(coverage_text):
    coverage = json.loads(coverage_text)
    missing = dict(coverage); missing.pop("M01")
    extra = dict(coverage); extra["M19"] = ["EmpiricalUniverse"]
    empty = dict(coverage); empty["M01"] = []
    nontext = dict(coverage); nontext["M01"] = [123]
    nonarray = dict(coverage); nonarray["M01"] = "EmpiricalUniverse"
    wrongbody = dict(coverage); wrongbody["M01"] = ["FAKE_FAMILY"]
    return (
        ("invalid-json", "{not-json"),
        ("missing-key", None),
        ("json-null", "null"),
        ("json-number", "123"),
        ("json-array", "[]"),
        ("json-string", '"M01"'),
        ("json-empty-object", "{}"),
        ("missing-atom", json.dumps(missing)),
        ("extra-atom", json.dumps(extra)),
        ("empty-body", json.dumps(empty)),
        ("nontext-token", json.dumps(nontext)),
        ("nonarray-body", json.dumps(nonarray)),
        ("wrong-body", json.dumps(wrongbody)),
    )


def _run_factory(label, original, roots, coverage_text, positive):
    print(label, "positive_original", positive)
    for case_label, value in _cases(coverage_text):
        for attempt in range(3):
            case = original.with_name(original.stem + "-" + case_label + "-" + str(attempt) + ".sqlite")
            shutil.copyfile(original, case)
            db = sqlite3.connect(case)
            try:
                if value is None:
                    db.execute("DELETE FROM main.header WHERE name='coverage'")
                else:
                    db.execute("UPDATE main.header SET value=? WHERE name='coverage'", (value,))
                db.commit()
            finally:
                db.close()
            forged = replace(roots, physical=_digest_file(case))
            before = len(os.listdir("/proc/self/fd"))
            try:
                VerifiedExternalI02(case, roots=forged)
            except ExternalI02IntegrityError as exc:
                after = len(os.listdir("/proc/self/fd"))
                if after > before:
                    raise AssertionError((label, case_label, "fd leak", before, after)) from exc
                print(label, case_label, attempt, "TYPED", type(exc).__name__, "fds", before, after)
            except BaseException as exc:
                raise AssertionError((label, case_label, "untyped", type(exc).__name__, str(exc))) from exc
            else:
                raise AssertionError((label, case_label, "ACCEPTED"))
    # Even a caller who forges BOTH roots cannot turn a malformed header into
    # an accepted certificate; the type refusal precedes any native selection.
    forged_case = original.with_name(original.stem + "-forged-both.sqlite")
    shutil.copyfile(original, forged_case)
    db = sqlite3.connect(forged_case)
    try:
        db.execute("UPDATE main.header SET value='{not-json' WHERE name='coverage'")
        db.commit()
        forged_logical = _logical_root(db, schema=roots.schema)
    finally:
        db.close()
    forged_both = replace(
        roots, physical=_digest_file(forged_case), logical=forged_logical,
    )
    try:
        VerifiedExternalI02(forged_case, roots=forged_both)
    except ExternalI02IntegrityError as exc:
        print(label, "forged-both-malformed", "TYPED", type(exc).__name__)
    else:
        raise AssertionError((label, "forged-both-malformed ACCEPTED"))
    with VerifiedExternalI02(original, roots=roots) as certified:
        selected = list(certified.selector_refs(*positive, native_only=True))
        if not selected:
            raise AssertionError((label, "valid original served no selector"))
        print(label, "valid_original_selection", len(selected))


def main():
    with tempfile.TemporaryDirectory(prefix="g5r2-review-") as td:
        root = Path(td)
        # Direct certificate.
        candidate, _, _ = _direct("g5r2-review-malformed")
        direct_path = root / "direct.sqlite"
        direct_roots = _build_direct(candidate, direct_path)
        db = sqlite3.connect(direct_path)
        try:
            direct_coverage = db.execute(
                "SELECT value FROM main.header WHERE name='coverage'"
            ).fetchone()[0]
        finally:
            db.close()
        event = candidate.respondent_events[0]
        _run_factory(
            "direct", direct_path, direct_roots, direct_coverage,
            (exact_ref(event.scoped_respondent_ref).key,
             exact_ref(event.native_question_ref)),
        )
        # Derived legacy-schema certificate (same generic cold verifier).
        source = _build_source("g5r2-review-derived", [
            {"id": "R1", "responses": {"Y": 1}},
            {"id": "R2", "responses": {"Y": 0}},
        ])
        derived_path = root / "derived.sqlite"
        derived_roots = build_sourcefree_external_i02(
            _release(source), source["universe"].ref, derived_path,
        )
        db = sqlite3.connect(derived_path)
        try:
            derived_coverage = db.execute(
                "SELECT value FROM main.header WHERE name='coverage'"
            ).fetchone()[0]
        finally:
            db.close()
        respondent = source["respondents"]["R1"].ref.key
        _run_factory(
            "derived", derived_path, derived_roots, derived_coverage,
            (respondent, source["qrefs"]["Y"]),
        )
    print("G5R1_INDEPENDENT_ATTACK_AND_FD_CLOSURE_PASS")


if __name__ == "__main__":
    main()
