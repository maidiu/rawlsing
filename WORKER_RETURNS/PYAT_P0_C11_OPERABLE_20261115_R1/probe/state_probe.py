"""Exact typed-state and negative probes on the same saved estate.

This is a supplement to the 100-operation court, not part of its distinct-op
count.  It preserves the observed MISSING/zero/sparse/repeated states and a
deliberate ZERO_SUPPORT negative on the same fixture.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = BASE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor, RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.tests.test_pre553_empirical_query import _predicate

from fixture_1006 import ShapeSpec, build_context
from ops import Battery, _and, _leaf, _query_ex

RESPONDENTS = 128
TAG = "PYAT-COUNTRY-REUSE-20261115"


def j(value):
    return json.loads(canonical_json(value))


def fact_material(result):
    fact = result.facts[0]
    return {
        "typed_state": fact.typed_state,
        "fact_ref": j(fact.ref),
        "replay_ref": j(fact.replay_ref),
        "raw_denominator_support": fact.raw_denominator_support,
        "raw_numerator_support": fact.raw_numerator_support,
        "weighted_denominator_support": getattr(
            fact, "weighted_denominator_support_if_authorized", None
        ),
        "cells": [
            {
                "cell": j(row["cell"]),
                "cell_state": row["cell_state"],
                "raw_numerator_support": row["raw_numerator_support"],
            }
            for row in fact.target_topology["complete_cell_semantic_projection"]
        ],
    }


def main() -> int:
    receipt = json.loads((BASE / "evidence" / "estate_receipt.json").read_text())
    ctx = build_context(ShapeSpec("country-reuse", RESPONDENTS, include_weights=True, tag=TAG))
    battery = Battery(ctx)
    ops = battery.build(core_count=80, weighted_count=20)
    source = battery.source
    qa = battery.qa
    impossible = _predicate(
        source, qa,
        _and(_leaf(source, qa, "A", 1), _leaf(source, qa, "A", 0)),
        tag=f"{TAG}-impossible-A1-A0",
    )
    impossible_query = _query_ex(
        source, qa, impossible, ("C",), measure="RAW",
        tag=f"{TAG}-q-impossible-A1-A0",
    )
    base_catalog = battery.catalog()
    catalog = RuntimeObjectCatalog(
        authorities=base_catalog.authorities,
        predicates=tuple({p.ref.key: p for p in (*base_catalog.predicates, impossible)}.values()),
        queries=tuple({q.ref.key: q for q in (*base_catalog.queries, impossible_query)}.values()),
        discovery_authorities=base_catalog.discovery_authorities,
    )
    by_id = {op.op_id: op for op in ops}
    probes = [
        ("marginal_B", by_id["marginal_B"].predicate, by_id["marginal_B"].query),
        ("marginal_D", by_id["marginal_D"].predicate, by_id["marginal_D"].query),
        ("mr_repeated_a1", by_id["mr_repeated_a1"].predicate, by_id["mr_repeated_a1"].query),
        ("impossible_A1_A0_to_C", impossible, impossible_query),
    ]
    admission = SavedC11Admission.open(
        root=receipt["root"],
        exact_path=Path(receipt["root"]) / receipt["exact_path"],
        independently_held_manifest_sha256=receipt["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**receipt["i02"]),
        release_ref=exact_ref(receipt["reconstructed_v1_release_ref"]),
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )
    repo, release = ctx.native_oracle()
    executor = CarrierNeutralResearchExecutor(
        repository=repo, release_refs=(release,), runtime_catalog=catalog,
    )
    result = {"schema": "PYAT_COUNTRY_REUSE_STATE_PROBE@1", "grade": "SOURCEFREE_TEST_ONLY", "probes": {}}
    for name, predicate, query in probes:
        saved = admission.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
        native = executor.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
        result["probes"][name] = {
            "saved": fact_material(saved),
            "native": fact_material(native),
            "exact_saved_vs_native": (
                canonical_json(saved.facts[0]) == canonical_json(native.facts[0])
            ),
        }
    (BASE / "evidence" / "state_probe.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "probes": {
            name: {
                "state": row["saved"]["typed_state"],
                "raw_denominator": row["saved"]["raw_denominator_support"],
                "cells": len(row["saved"]["cells"]),
                "exact": row["exact_saved_vs_native"],
            }
            for name, row in result["probes"].items()
        }
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
