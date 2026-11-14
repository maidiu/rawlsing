"""Semantic oracle, change/restore and hostile checks for the locality experiment."""
from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys

import pytest

pytest.importorskip("pyarrow")

AUTHOR_ROOT = Path(__file__).resolve().parents[1]
REPO = AUTHOR_ROOT.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(AUTHOR_ROOT))

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError,
    VerifiedDirectEstate,
    write_direct_estate,
)
import rawlsing_next._pre553_query_eval as query_eval

from fixture_1006 import ShapeSpec, build_context
from query_1006 import build_query_bundle, execute_bundle_oracle
from locality_probe import _locality_sorted, REAL_SORTED, _jsonable


def _write(tmp_path: Path, shape: ShapeSpec):
    root = tmp_path / shape.name
    root.mkdir(parents=True, mode=0o700)
    ctx = build_context(shape)
    bundle = build_query_bundle(ctx)
    receipt = write_direct_estate(
        ctx.direct_sections(), ctx.universe.ref, root, chunk_rows=16,
    )
    return root, ctx, bundle, receipt


def _open(root: Path, receipt, bundle, *, authorizer=lambda _roots: True):
    return SavedC11Admission.open(
        root=root, exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        release_ref=receipt.reconstructed_v1_release_ref,
        runtime_catalog=bundle.catalog,
        current_authorizer=authorizer,
    )


def _run(admission, bundle, name: str):
    query, predicate = bundle.by_name(name)
    return admission.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)


def _signature(result):
    return tuple(
        {
            "ref": fact.ref.as_dict(),
            "projection": _jsonable(fact.semantic_projection()),
            "replay_ref": _jsonable(fact.replay_ref),
            "denominator": fact.raw_denominator_support,
            "state": fact.typed_state,
        }
        for fact in result.facts
    )


def test_candidate_exact_oracle_parity_and_change_restore(tmp_path):
    original = ShapeSpec(
        "locality-original", 64, include_weights=True,
        tag="PYAT1006-LOCALITY-ORIGINAL",
    )
    changed = replace(
        original, name="locality-changed", mutate_respondent=3,
        mutate_question="C",
    )
    root_a, ctx_a, bundle_a, receipt_a = _write(tmp_path, original)
    root_b, ctx_b, bundle_b, receipt_b = _write(tmp_path, changed)
    repo_a, release_a = ctx_a.native_oracle()
    repo_b, release_b = ctx_b.native_oracle()
    oracle_a = execute_bundle_oracle(
        repo_a, release_a, bundle_a,
        qa=bundle_a.catalog.authorities[-2],
        dauth=bundle_a.catalog.authorities[-1],
    )
    oracle_b = execute_bundle_oracle(
        repo_b, release_b, bundle_b,
        qa=bundle_b.catalog.authorities[-2],
        dauth=bundle_b.catalog.authorities[-1],
    )
    admission_a = _open(root_a, receipt_a, bundle_a)
    admission_b = _open(root_b, receipt_b, bundle_b)
    baseline = {
        name: _signature(_run(admission_a, bundle_a, name))
        for name in ("selected", "f2_reverse", "f4_three", "weighted", "repeated")
    }
    query_eval.sorted = _locality_sorted
    try:
        candidate = {
            name: _signature(_run(admission_a, bundle_a, name))
            for name in ("selected", "f2_reverse", "f4_three", "weighted", "repeated")
        }
        candidate_b = {
            name: _signature(_run(admission_b, bundle_b, name))
            for name in ("selected", "f2_reverse", "f4_three", "weighted", "repeated")
        }
        restored = {
            name: _signature(_run(admission_a, bundle_a, name))
            for name in ("selected", "f2_reverse", "f4_three", "weighted", "repeated")
        }
    finally:
        query_eval.sorted = REAL_SORTED
    for name in baseline:
        assert candidate[name] == baseline[name], name
        assert baseline[name] == _signature(oracle_a[name]), name
        assert candidate_b[name] == _signature(oracle_b[name]), name
        assert restored[name] == baseline[name], name
    assert candidate_b["selected"] != baseline["selected"]
    assert candidate_b["f2_reverse"] != baseline["f2_reverse"]
    assert candidate_b["f4_three"] != baseline["f4_three"]
    assert restored["selected"] == baseline["selected"]


def test_candidate_does_not_bypass_current_root_or_tamper_checks(tmp_path):
    shape = ShapeSpec(
        "locality-hostile", 32, include_weights=False,
        tag="PYAT1006-LOCALITY-HOSTILE",
    )
    root, ctx, bundle, receipt = _write(tmp_path, shape)
    query_eval.sorted = _locality_sorted
    try:
        with pytest.raises(Exception):
            _open(root, receipt, bundle, authorizer=lambda _roots: False)
        wrong = replace(receipt.i02, source="SOURCE_ARTIFACT:forged:0")
        with pytest.raises(Exception):
            SavedC11Admission.open(
                root=root, exact_path=receipt.path,
                independently_held_manifest_sha256=receipt.manifest_sha256,
                independently_held_i02=wrong,
                release_ref=receipt.reconstructed_v1_release_ref,
                runtime_catalog=bundle.catalog,
                current_authorizer=lambda _roots: True,
            )
        (Path(receipt.path) / "event_locator.parquet").unlink()
        with pytest.raises(DirectEstateError):
            VerifiedDirectEstate(
                root, exact_path=receipt.path,
                independently_held_manifest_sha256=receipt.manifest_sha256,
                independently_held_i02=receipt.i02,
                current_authorizer=lambda _roots: True,
            )
    finally:
        query_eval.sorted = REAL_SORTED
