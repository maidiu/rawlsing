"""Independent G5 ordering/negative witness for the PARTIAL repair.

Checks that forged binding, wrong admission type, revoked CURRENT and a CURRENT
change after the saved-binding check all refuse before protected entry/output/
receipt work, while a legitimate PARTIAL still resumes exact final outputs.
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import sys

import rawlsing_next.pre553_issued_workload as issued_module
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import (
    CurrentIssuer, HOST, PURPOSE,
)
from rawlsing_next.tests.test_pyat991_s2d_five_readers import _admission_for, _fixture


def _forged(checkpoint, binding):
    forged = replace(
        checkpoint, saved_binding=replace(binding, manifest_sha256="0" * 64),
    )
    return replace(
        forged, checkpoint_hash=issued_module._checkpoint_content_hash(forged),
    )


class _Spies:
    def __init__(self):
        self.counts = {
            "validate_entry_material": 0,
            "validate_entry_outputs": 0,
            "restore_receipt": 0,
            "restore_output_material": 0,
        }
        self.originals = {}

    def __enter__(self):
        for name, attr in (
            ("validate_entry_material", "_validate_entry_material"),
            ("validate_entry_outputs", "_validate_entry_outputs"),
            ("restore_receipt", "_restore_receipt"),
            ("restore_output_material", "_restore_output_material"),
        ):
            original = getattr(issued_module, attr)
            self.originals[name] = original

            def spy(*args, _name=name, _original=original, **kwargs):
                self.counts[_name] += 1
                return _original(*args, **kwargs)

            setattr(issued_module, attr, spy)
        return self

    def __exit__(self, *_args):
        for name, original in self.originals.items():
            attr = {
                "validate_entry_material": "_validate_entry_material",
                "validate_entry_outputs": "_validate_entry_outputs",
                "restore_receipt": "_restore_receipt",
                "restore_output_material": "_restore_output_material",
            }[name]
            setattr(issued_module, attr, original)


def _attempt(issued, resolver, admission, checkpoint):
    factory_calls = {"n": 0}

    def factory():
        factory_calls["n"] += 1
        return admission

    error = None
    with _Spies() as spies:
        try:
            issued_module.resume_joined_workloads(
                workloads=(issued,), resolver=resolver,
                saved_admission_factory=factory, source_factory=None,
                host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
                expected_checkpoint_ref=checkpoint.checkpoint_hash,
                allow_test_only=True,
            )
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        counts = dict(spies.counts)
    return {"factory_calls": factory_calls["n"], "counts": counts, "error": error}


class _FlipResolver:
    def __init__(self, record, changed, flip_at):
        self.record = record
        self.changed = changed
        self.flip_at = flip_at
        self.calls = 0

    def resolve_current(self, _ref):
        self.calls += 1
        return self.changed if self.calls >= self.flip_at else self.record


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: independent_partial_order.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("proofroot must be the approved private temp path")
    tmp = proofroot / "partial-order-witness"
    tmp.mkdir(parents=True, exist_ok=True)
    _, _, _, issued, root, receipt, issuer = _fixture(tmp)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    full = issued_module.execute_issued_workload(
        issued.workload, issuer, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    partial = issued_module.execute_issued_workload(
        issued.workload, issuer, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE, allow_test_only=True,
        max_units=1,
    )
    binding = admission.binding_receipt()
    checkpoint = issued_module.capture_joined_checkpoint(
        (partial,), saved_binding=binding,
    )
    assert checkpoint.entries[0].state == "PARTIAL"

    forged = _attempt(issued, issuer, admission, _forged(checkpoint, binding))

    class WrongType:
        pass

    wrong_type_factory = {"calls": 0}

    def bad_factory():
        wrong_type_factory["calls"] += 1
        return WrongType()

    wrong_type_error = None
    with _Spies() as spies:
        try:
            issued_module.resume_joined_workloads(
                workloads=(issued,), resolver=issuer,
                saved_admission_factory=bad_factory, source_factory=None,
                host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
                expected_checkpoint_ref=checkpoint.checkpoint_hash,
                allow_test_only=True,
            )
        except Exception as exc:
            wrong_type_error = f"{type(exc).__name__}: {exc}"
        wrong_type_counts = dict(spies.counts)

    revoked_issuer = CurrentIssuer((issued.record,))
    revoked_issuer.revoke()
    revoked = _attempt(issued, revoked_issuer, admission, checkpoint)

    changed = replace(
        issued.record,
        source_permission_ref=ExactRef(
            "TEST_ONLY_SOURCE_PERMISSION", "urn:test:s2d:flip", "a" * 64,
        ),
    )
    flip = _FlipResolver(issued.record, changed, flip_at=3)
    flipped = _attempt(issued, flip, admission, checkpoint)

    legitimate_error = None
    with _Spies() as legitimate_spies:
        try:
            legitimate = issued_module.resume_joined_workloads(
                workloads=(issued,), resolver=issuer,
                saved_admission_factory=lambda: admission, source_factory=None,
                host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
                expected_checkpoint_ref=checkpoint.checkpoint_hash,
                allow_test_only=True,
            )
        except Exception as exc:
            legitimate_error = f"{type(exc).__name__}: {exc}"
            legitimate = None
        legitimate_counts = dict(legitimate_spies.counts)
    legitimate_refs = (
        None if legitimate is None
        else sorted(ref.key for ref in legitimate.output_refs)
    )
    expected_refs = sorted(ref.key for ref in full.output_refs)
    evidence = {
        "schema": "PYAT991_ALL_SEVEN_G5_PARTIAL_ORDER_RECHECK@1",
        "forged_partial": forged,
        "wrong_type": {
            "factory_calls": wrong_type_factory["calls"],
            "counts": wrong_type_counts,
            "error": wrong_type_error,
        },
        "revoked_current": revoked,
        "current_flip_after_binding": {
            "flip_at_call": 3,
            "resolver_calls": flip.calls,
            **flipped,
        },
        "legitimate_partial": {
            "counts": legitimate_counts,
            "error": legitimate_error,
            "output_refs_equal_full": legitimate_refs == expected_refs,
        },
        "all_negatives_zero_protected_work": all(
            value == 0
            for row in (forged["counts"], wrong_type_counts, revoked["counts"], flipped["counts"])
            for value in row.values()
        ),
        "defect_reproduced": (
            forged["counts"] != {
                "validate_entry_material": 0,
                "validate_entry_outputs": 0,
                "restore_receipt": 0,
                "restore_output_material": 0,
            }
        ),
    }
    (proofroot / "partial_order_recheck.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8",
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if (
        evidence["all_negatives_zero_protected_work"]
        and not evidence["defect_reproduced"]
        and legitimate_refs == expected_refs
    ) else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
