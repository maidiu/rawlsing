"""Independent G5 S2-D scope false-refusal witness.

The accepted S2-C estate exposes an exact admitted source artifact root.  The
native I03 owner accepts a query/predicate whose exact scope_refs include that
admitted source artifact as lawful exact scope metadata.  The S2-D saved
admission currently rejects every scope kind except EmpiricalUniverse and
C11LogicalRelease, so it refuses the exact admitted source scope as "foreign".

This harness proves the actual native first-reader positive and the saved
admission false refusal.  It is review-only and writes only to the supplied
private proofroot.

Usage:
  PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1 TMPDIR=<proofroot> \
  python3 WORKER_RETURNS/PYAT991_S2D_G5/scope_false_refusal.py <proofroot>
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

from rawlsing_next.pre553_direct_estate_i03 import _ref_from_key
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalQuerySpec,
    exact_ref,
)
from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03
from rawlsing_next.tests import test_pre553_direct_estate_i03 as s2c
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.tests.test_pyat991_s2d_a_counter import (
    _catalog_with,
    _with_extra_scopes,
)
from rawlsing_next.tests.test_pyat991_s2d_saved_admission import (
    _admission,
    _i03_parts,
    _source_with_candidate,
)


class _MonkeyPatch:
    def __init__(self) -> None:
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


def _scoped_query_and_predicate(predicate, query, extra_refs, *, tag: str):
    scoped_predicate = _with_extra_scopes(predicate, tuple(extra_refs))
    scoped_query = _with_extra_scopes(query, tuple(extra_refs))
    fields = dict(scoped_query.semantic_fields)
    fields["condition_predicate_ref"] = scoped_predicate.ref
    deps = tuple(
        sorted(
            {
                *(exact_ref(value) for value in scoped_query.dependency_refs),
                scoped_predicate.ref,
            },
            key=lambda ref: ref.key,
        )
    )
    scoped_query = EmpiricalQuerySpec(
        typed_state=scoped_query.typed_state,
        authority_snapshot_refs=scoped_query.authority_snapshot_refs,
        dependency_refs=deps,
        producer_replay_locator_or_reference_root=(
            scoped_query.producer_replay_locator_or_reference_root
        ),
        **{key: value for key, value in fields.items() if key != "dependency_refs"},
    )
    return scoped_predicate, scoped_query


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        raise SystemExit("usage: scope_false_refusal.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("proofroot must be the approved private temp path")
    proofroot.mkdir(parents=True, exist_ok=True)
    tag = "G5-ADMITTED-SOURCE-SCOPE"
    source, candidate = _source_with_candidate(
        _MonkeyPatch(),
        tag,
        [{"id": "R1", "responses": {"Y": 0}}, {"id": "R2", "responses": {"Y": 1}}],
    )
    qauth, predicate, query, base_catalog = _i03_parts(source, tag)
    root, receipt = s2c._cold(
        proofroot, candidate, source["universe"].ref, "g5-source-scope"
    )
    source_kind = receipt.i02.source.split("|", 1)[0]
    admitted_source_scope = _ref_from_key(receipt.i02.source, source_kind)

    scoped_predicate, scoped_query = _scoped_query_and_predicate(
        predicate, query, (admitted_source_scope,), tag=tag
    )
    scoped_catalog = _catalog_with(
        authorities=base_catalog.authorities,
        predicate=scoped_predicate,
        query=scoped_query,
    )
    oracle = native._run(source, qauth, scoped_predicate, scoped_query)
    oracle_fact = oracle.facts[0]

    private_estate = s2c.VerifiedDirectEstate(
        root,
        exact_path=receipt.path,
        independently_held_manifest_sha256=receipt.manifest_sha256,
        independently_held_i02=receipt.i02,
        current_authorizer=lambda _roots: True,
    )
    saved_native_executor = CarrierNeutralResearchExecutor(
        repository=private_estate,
        release_refs=(source["release_ref"],),
        runtime_catalog=scoped_catalog,
    )
    saved_native_result = saved_native_executor.execute_i03(
        query_ref=scoped_query.ref, predicate_ref=scoped_predicate.ref
    )
    saved_native_fact = saved_native_result.facts[0]

    admission = _admission(root, receipt, source, scoped_catalog)
    base_admission = _admission(root, receipt, source, base_catalog)
    base_observed = execute_saved_i03(
        base_admission, query_ref=query.ref, predicate_ref=predicate.ref
    )
    try:
        saved_observed = execute_saved_i03(
            admission,
            query_ref=scoped_query.ref,
            predicate_ref=scoped_predicate.ref,
        )
        saved_outcome = {
            "state": "ACCEPTED",
            "fact_ref": saved_observed.facts[0].ref.as_dict(),
        }
    except Exception as exc:  # exact refusal evidence
        saved_outcome = {
            "state": "REFUSED",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }

    evidence = {
        "schema": "PYAT991_S2D_G5_SCOPE_WITNESS@1",
        "native_oracle": {
            "state": oracle_fact.typed_state,
            "raw_denominator_support": oracle_fact.raw_denominator_support,
            "fact_ref": oracle_fact.ref.as_dict(),
        },
        "saved_estate_native_i03": {
            "state": saved_native_fact.typed_state,
            "raw_denominator_support": saved_native_fact.raw_denominator_support,
            "fact_ref": saved_native_fact.ref.as_dict(),
        },
        "saved_base_positive": {
            "state": base_observed.facts[0].typed_state,
            "fact_ref": base_observed.facts[0].ref.as_dict(),
        },
        "admitted_source_scope": admitted_source_scope.as_dict(),
        "scoped_query_ref": scoped_query.ref.as_dict(),
        "scoped_predicate_ref": scoped_predicate.ref.as_dict(),
        "saved_admitted_source_scope": saved_outcome,
        "expected": (
            "saved admission preserves the exact admitted SOURCE_ARTIFACT scope "
            "as lawful exact scope metadata and returns the native SUPPORTED fact; "
            "only foreign source/universe/release/authority scope must refuse"
        ),
        "defect": saved_outcome["state"] == "REFUSED",
        "original_contract_basis": (
            "EmpiricalQuerySpec.scope_refs and EmpiricalPredicate.scope_refs are "
            "required set-like exact scope references with no universe/release-only "
            "type whitelist; the native I03 owner accepts the exact admitted source "
            "artifact as scope metadata. The saved admission's arbitrary whitelist "
            "discards a valid native request."
        ),
    }
    (proofroot / "scope_witness_evidence.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
