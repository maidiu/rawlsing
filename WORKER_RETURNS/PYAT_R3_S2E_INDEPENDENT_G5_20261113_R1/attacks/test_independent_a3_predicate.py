"""Additional G5: invented executed predicate outside issued I05 role set."""
from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_query import I03GroupedExecutionScope
from rawlsing_next.pre553_s2e_exact_conservation import (
    S2EOutputConservationError,
    census_native_batch,
    require_same_native_output_graph,
)
from rawlsing_next.tests.test_pyat919_s2e_a_whole_native_batch import _batch, _native_case


def test_invented_executed_predicate_outside_issued_roles_refused():
    case = _native_case()
    with I03GroupedExecutionScope() as scope:
        manifest, receipts, outputs, baseline, _, _ = _batch(case, scope=scope)
    unit = next(u for u in manifest.units if u.job_kind == "DISCOVERY")
    original = outputs[unit.unit_hash]
    extra = case[2][2][1]  # legitimate F2 Y predicate, not an I05 role
    assert extra.ref.key not in {p.ref.key for p in original.executed_predicates}
    forged = replace(
        original,
        executed_predicates=tuple(sorted((*original.executed_predicates, extra), key=lambda p: p.ref.key)),
    )
    with pytest.raises(S2EOutputConservationError, match="S2E_I05_EXECUTED_OBJECT_CLOSURE_MISMATCH"):
        census_native_batch(
            manifest, receipts, {**outputs, unit.unit_hash: forged},
            require_complete=True, runtime_catalog=case[1],
        )
    require_same_native_output_graph(
        baseline,
        census_native_batch(manifest, receipts, outputs, require_complete=True, runtime_catalog=case[1]),
    )
