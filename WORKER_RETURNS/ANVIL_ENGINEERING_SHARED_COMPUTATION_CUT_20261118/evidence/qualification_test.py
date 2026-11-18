"""Bounded qualification prototype for the proposed grouped prepared I03 cut.

This file is NOT a production test and is not applied to the product tree. It
executes the existing grouped engine directly against the existing tiny
prepared-saved fixture to prove the proposed mechanism. The current public
seam is also exercised and must remain RED until the proposal is granted.
"""
from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next._pre553_query_common import _parse_target_plan, _profile
from rawlsing_next._pre553_query_eval import (
    _build_fact, _evaluate_index_group,
)
from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.pre553_empirical_query import (
    EmpiricalQueryExecutionError, I03GroupedExecutionScope,
    execute_empirical_query,
)
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture


def _current_public_red(prepared, admission, predicate, query):
    with pytest.raises(
        EmpiricalQueryExecutionError,
        match="grouped native I03 cache not yet qualified for cold sourcefree estate",
    ):
        execute_empirical_query(
            repository=prepared._session,
            query=query,
            predicate=predicate,
            authority_registry=admission._runtime_catalog.authority_registry,
            release_refs=(admission.release_ref,),
            group_scope=I03GroupedExecutionScope(),
        )


def test_current_guard_is_red_and_existing_group_engine_reuses_compatible_core(
    tmp_path, monkeypatch,
):
    _source, _qa, predicate, _other, queries, admission = _fixture(
        monkeypatch, tmp_path / "shared-cut", "SHARED-CUT",
    )
    with admission.prepared_i03() as prepared:
        selected = queries["selected"]
        raw = queries["raw"]
        _current_public_red(prepared, admission, predicate, selected)

        baseline_selected = prepared.execute_i03(
            query_ref=selected.ref, predicate_ref=predicate.ref,
        ).facts[0]
        baseline_raw = prepared.execute_i03(
            query_ref=raw.ref, predicate_ref=predicate.ref,
        ).facts[0]

        # The proposed direct-session index cache is what makes these two
        # indices the SAME object. The prototype supplies that stable index
        # explicitly; the current product still creates a fresh index per call.
        index = prepared._session.indices_for(
            query=selected, release_refs=(admission.release_ref,),
        )[0][1]
        again = prepared._session.indices_for(
            query=raw, release_refs=(admission.release_ref,),
        )[0][1]
        assert index is not again, "prototype documents the current absent index cache"

        # Simulate only the proposed direct-session identity extension. The
        # product patch adds these two exact fields to _DirectReleaseIdentity
        # and caches the same index object for the prepared session lifetime.
        proposed_release = SimpleNamespace(
            release_ref=index.release.release_ref,
            replay_manifest=index.release.replay_manifest,
            semantic_release_hash=index.release.release_ref.content_hash,
            source_release_manifest_hash=admission.manifest_sha256,
        )
        proposed_index = replace(index, release=proposed_release)

        registry = admission._runtime_catalog.authority_registry
        scope = I03GroupedExecutionScope()
        try:
            observed = {}
            for name, query in (("selected", selected), ("raw", raw)):
                plan = _parse_target_plan(query, registry)
                profile = _profile(query)
                evaluation = _evaluate_index_group(
                    (proposed_index,), query=query, predicate=predicate,
                    plan=plan, profile=profile, registry=registry,
                    group_scope=scope,
                )
                observed[name] = _build_fact(
                    (proposed_index,), query=query, predicate=predicate,
                    plan=plan, profile=profile, evaluation=evaluation,
                    registry=registry,
                )
            assert canonical_json(observed["selected"]) == canonical_json(
                baseline_selected
            )
            assert canonical_json(observed["raw"]) == canonical_json(
                baseline_raw
            )
            receipt = scope.receipt()
            assert receipt["core_builds"] == 1, receipt
            assert receipt["core_hits"] == 1, receipt
            assert receipt["fallbacks"] == 0, receipt
            assert receipt["weighted_materializations"] == 1, receipt
            assert receipt["raw_materializations"] == 1, receipt
        finally:
            scope.close()

        # A different target plan is not shareable under the existing key.
        incompatible = I03GroupedExecutionScope()
        try:
            for name in ("selected", "f2"):
                query = queries[name]
                plan = _parse_target_plan(query, registry)
                profile = _profile(query)
                _evaluate_index_group(
                    (proposed_index,), query=query, predicate=predicate,
                    plan=plan, profile=profile, registry=registry,
                    group_scope=incompatible,
                )
            receipt = incompatible.receipt()
            assert receipt["core_builds"] == 2, receipt
            assert receipt["core_hits"] == 0, receipt
        finally:
            incompatible.close()
