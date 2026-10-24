"""R03V independent hostile/coverage probes (TEST_ONLY)."""
from __future__ import annotations

from dataclasses import replace
import inspect
from pathlib import Path

import pytest

from rawlsing_next.pre553_universal_workload import (
    RecursiveWorkloadFragment, UniversalOperation, UniversalWorkloadResult,
    bind_recursive_execution, compile_universal_workload,
    execute_universal_workload,
)
from rawlsing_next.tests.test_universal_grammar import _campaign_fixture
from rawlsing_next.tests.test_universal_source_projection import build_s3, s3_rows

AS_OF = "2026-10-23"
HOST = "r03v-independent"
PURPOSE = "TEST_ONLY_SOURCEFREE"


def _bundle(tmp_path: Path, *, mutate=None):
    path = tmp_path / ("r03v_%s.sav" % ("mut" if mutate else "base"))
    return build_s3(path, s3_rows(respondents=4, occasions=2, mutate=mutate))


def _run(bundle):
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    result = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    return compilation, result


def test_H1_compiler_consumes_grammar_or_scientific_frontier():
    parameters = set(inspect.signature(compile_universal_workload).parameters)
    assert parameters & {"grammar", "frontier", "scientific_frontier", "expected_frontier"}, (
        "compile_universal_workload has no grammar/scientific-frontier input; "
        "it only enumerates administered unary item/value pairs"
    )
    fields = set(UniversalOperation.__dataclass_fields__)
    assert {"conditions", "ordered_targets", "operation_class", "comparator"} <= fields, (
        "UniversalOperation cannot represent conditional/joint/root-parent operations"
    )


def test_H2_antijoin_requires_native_receipt_and_fact_content(tmp_path):
    bundle = _bundle(tmp_path)
    compilation, result = _run(bundle)
    assert result.anti_join()["no_drop_ok"]
    stripped = replace(result, receipt_refs=(), fact_refs=(), native_results=())
    assert stripped.anti_join()["no_drop_ok"] is False, (
        "anti_join still reports no-drop after all native receipts/facts/results are removed"
    )


def test_H3_antijoin_requires_expected_native_job_identity(tmp_path):
    bundle = _bundle(tmp_path)
    compilation, result = _run(bundle)
    assert result.anti_join()["no_drop_ok"]
    altered = replace(result, compilation=replace(compilation, expected_jobs=()))
    assert altered.anti_join()["no_drop_ok"] is False, (
        "anti_join ignores expected_jobs and only compares R03 operation ids"
    )


def test_H4_recursive_fragment_is_composed_into_the_workload():
    parameters = set(inspect.signature(execute_universal_workload).parameters)
    assert parameters & {"recursive_fragment", "campaign", "execution_ref", "recursive_executions"}, (
        "execute_universal_workload has no path for the R01 D3 fragment; "
        "bind_recursive_execution only decorates unrelated receipts"
    )
    fields = set(UniversalWorkloadResult.__dataclass_fields__)
    assert {"recursive_fragments", "recursive_receipt_refs", "recursive_fact_refs"} & fields, (
        "UniversalWorkloadResult has no composed R01 recursive ledger"
    )


def test_H5_typed_operation_states_are_retained(tmp_path):
    fields = set(UniversalWorkloadResult.__dataclass_fields__)
    assert {"operation_states", "typed_states", "status_by_operation"} & fields, (
        "UniversalWorkloadResult has no per-operation typed state ledger; "
        "unsupported/error/unrun/valid-empty cannot be distinguished"
    )
    bundle = _bundle(tmp_path)
    compilation, result = _run(bundle)
    assert all(op.status in {"COMPILED", "UNSUPPORTED_RUNTIME"} for op in compilation.operations)
    assert result.failed == ()


def test_P1_actual_source_value_fault_changes_and_restores_facts(tmp_path):
    base = _bundle(tmp_path)
    mutated = _bundle(tmp_path, mutate=(0, 0))
    base_compilation, base_result = _run(base)
    mutated_compilation, mutated_result = _run(mutated)
    assert base_result.anti_join()["no_drop_ok"]
    assert mutated_result.anti_join()["no_drop_ok"]
    assert base_result.fact_refs != mutated_result.fact_refs, (
        "changing one physical source response value did not change dependent facts"
    )
    restored = _run(base)
    assert restored[1].fact_refs == base_result.fact_refs
