"""Independent G5 split foreign-source scope negatives for S2-D.

Tests a foreign SOURCE_ARTIFACT scope independently in the query only and in the
predicate only, with the other object left at the admitted baseline.  Both must
refuse; this prevents the new source allowance from becoming kind-wide or being
checked in only one object.

Review-only; writes to the caller's private proofroot.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
from unittest.mock import patch

from rawlsing_next.pre553_direct_estate_i03 import _ref_from_key
from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec, ExactRef, exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11AdmissionError
from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03
from rawlsing_next.tests import test_pre553_direct_estate_i03 as s2c
from rawlsing_next.tests.test_pyat991_s2d_a_counter import _catalog_with, _with_extra_scopes
from rawlsing_next.tests.test_pyat991_s2d_saved_admission import (
    _admission,
    _i03_parts,
    _source_with_candidate,
)


class _MonkeyPatch:
    def __init__(self):
        self._patches = []

    def context(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        for item in self._patches:
            item.stop()
        self._patches.clear()

    def setattr(self, obj, name, value):
        item = patch.object(obj, name, value)
        item.start()
        self._patches.append(item)


def _build_query_with_scope(predicate, query, scope):
    scoped_query = _with_extra_scopes(query, (scope,))
    fields = dict(scoped_query.semantic_fields)
    fields["condition_predicate_ref"] = predicate.ref
    deps = tuple(
        sorted(
            {
                *(exact_ref(value) for value in scoped_query.dependency_refs),
                predicate.ref,
            },
            key=lambda ref: ref.key,
        )
    )
    return EmpiricalQuerySpec(
        typed_state=scoped_query.typed_state,
        authority_snapshot_refs=scoped_query.authority_snapshot_refs,
        dependency_refs=deps,
        producer_replay_locator_or_reference_root=(
            scoped_query.producer_replay_locator_or_reference_root
        ),
        **{key: value for key, value in fields.items() if key != "dependency_refs"},
    )


def _build_scope_only_on_predicate(predicate, query, scope):
    scoped_predicate = _with_extra_scopes(predicate, (scope,))
    fields = dict(query.semantic_fields)
    fields["condition_predicate_ref"] = scoped_predicate.ref
    deps = tuple(
        sorted(
            {
                *(exact_ref(value) for value in query.dependency_refs),
                scoped_predicate.ref,
            },
            key=lambda ref: ref.key,
        )
    )
    scoped_query = EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=deps,
        producer_replay_locator_or_reference_root=(
            query.producer_replay_locator_or_reference_root
        ),
        **{key: value for key, value in fields.items() if key != "dependency_refs"},
    )
    return scoped_predicate, scoped_query


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        raise SystemExit("usage: scope_foreign_split.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("proofroot must be the approved private temp path")
    proofroot.mkdir(parents=True, exist_ok=True)
    tag = "S2D-G5-FOREIGN-SOURCE-SPLIT"
    source, candidate = _source_with_candidate(
        _MonkeyPatch(),
        tag,
        [{"id": "R1", "responses": {"Y": 0}}, {"id": "R2", "responses": {"Y": 1}}],
    )
    qauth, predicate, query, base_catalog = _i03_parts(source, tag)
    root, receipt = s2c._cold(proofroot, candidate, source["universe"].ref, "g5-split")
    admitted = _ref_from_key(
        receipt.i02.source, receipt.i02.source.split("|", 1)[0]
    )
    foreign = ExactRef(admitted.kind, "urn:test:foreign-source-scope", "c" * 64)

    query_only = _build_query_with_scope(predicate, query, foreign)
    query_catalog = _catalog_with(
        authorities=base_catalog.authorities,
        predicate=predicate,
        query=query_only,
    )
    query_admission = _admission(root, receipt, source, query_catalog)
    query_result = {}
    try:
        execute_saved_i03(
            query_admission,
            query_ref=query_only.ref,
            predicate_ref=predicate.ref,
        )
        query_result = {"state": "ACCEPTED"}
    except SavedC11AdmissionError as exc:
        query_result = {"state": "REFUSED", "error": str(exc)}

    scoped_predicate, predicate_only = _build_scope_only_on_predicate(
        predicate, query, foreign
    )
    predicate_catalog = _catalog_with(
        authorities=base_catalog.authorities,
        predicate=scoped_predicate,
        query=predicate_only,
    )
    predicate_admission = _admission(root, receipt, source, predicate_catalog)
    predicate_result = {}
    try:
        execute_saved_i03(
            predicate_admission,
            query_ref=predicate_only.ref,
            predicate_ref=scoped_predicate.ref,
        )
        predicate_result = {"state": "ACCEPTED"}
    except SavedC11AdmissionError as exc:
        predicate_result = {"state": "REFUSED", "error": str(exc)}

    evidence = {
        "schema": "PYAT991_S2D_G5_SOURCE_SCOPE_SPLIT@1",
        "admitted_source": admitted.as_dict(),
        "foreign_source": foreign.as_dict(),
        "query_only_foreign_source": query_result,
        "predicate_only_foreign_source": predicate_result,
        "both_refused": query_result["state"] == "REFUSED"
        and predicate_result["state"] == "REFUSED",
    }
    (proofroot / "scope_foreign_split_evidence.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if evidence["both_refused"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
