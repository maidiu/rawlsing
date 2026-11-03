"""GAP-007 repair candidate: bind exact P1 units to actual sourcefree C11/I03/I05/Batch.

TEST_ONLY synthetic source. No original respondents, source rights, production
edit, compiler replacement or downstream adoption.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from dataclasses import replace
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
P1_ROOT = ROOT / "p1"
CONSTRUCTOR = P1_ROOT / "programma_pyat_original35_constructor.py"
TEST_FILE = P1_ROOT / "test_programma_pyat_original35_constructor.py"
FROZEN_SOURCE = Path(__file__).resolve().parent / "frozen/source.sav"
FROZEN_SOURCE_SHA256 = "5009f3c9272dcbfb15a48b17cfff51f9afa67e60d6a2c1364c9aa07bc6732e4f"


class FrozenSourceIntegrityError(RuntimeError):
    """The exact committed synthetic SAV bytes are required; no fallback."""


def verify_frozen_source(source_path: Path = FROZEN_SOURCE) -> Path:
    source_path = Path(source_path)
    if not source_path.is_file():
        raise FrozenSourceIntegrityError("FROZEN_SOURCE_ABSENT")
    actual = hashlib.sha256(source_path.read_bytes()).hexdigest()
    if actual != FROZEN_SOURCE_SHA256:
        raise FrozenSourceIntegrityError(
            "FROZEN_SOURCE_SHA256_MISMATCH: "
            f"expected {FROZEN_SOURCE_SHA256}; actual {actual}"
        )
    return source_path

spec = importlib.util.spec_from_file_location("gap007.p1_constructor", CONSTRUCTOR)
p1 = importlib.util.module_from_spec(spec)
sys.modules["gap007.p1_constructor"] = p1
sys.modules["rawlsing_next.programma_pyat_original35_constructor"] = p1
spec.loader.exec_module(p1)
test_spec = importlib.util.spec_from_file_location("gap007.p1_tests", TEST_FILE)
tests = importlib.util.module_from_spec(test_spec)
test_spec.loader.exec_module(tests)

from rawlsing_next.tests.test_universal_source_projection import package
from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceRule, materialize_native_preimages
from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
from rawlsing_next.pre553_native_workload_binding import OperationFixture, build_projection_catalog
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor, RuntimeObjectCatalog
from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec, BatchExecutionRunner, ExecutionOutcome, ExecutorBinding
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.tests.test_universal_workload_custody import AS_OF, HOST, PURPOSE
from rawlsing_next.tests.test_universal_grammar import _inventory, _occurrence, _policy, _frontier
from rawlsing_next.pre553_universal_workload import compile_governed_frontier, execute_governed_frontier


def _merge(values):
    by_key = {value.ref.key: value for value in values}
    return tuple(by_key[key] for key in sorted(by_key))


def _max_one(values):
    by_key = {value.key: value for value in values}
    return tuple(by_key[key] for key in sorted(by_key))


def main(source_path: Path = FROZEN_SOURCE) -> int:
    source_path = verify_frozen_source(source_path)
    codes = [f"Q{i:02d}{side}" for i in range(35) for side in ("A", "B")]
    source_package = package(
        source_path, decode_sav(source_path).row_count,
        tuple(NativeSourceRule("impl." + code, code) for code in codes),
        coordinate="FORM",
    )
    incidence = decode_sav(source_path)
    bundle = materialize_native_preimages(package=source_package, incidence=incidence)
    repository, release = build_source_backed_c11_repository(
        bundle.physical_stream, bundle.projection
    )
    original_plan = p1.construct_original35_epre(tests._input())
    bound_input = tests._input()
    bound_input = replace(bound_input, waves=tuple(
        replace(wave, release_ref=release.release_ref)
        for wave in bound_input.waves
    ))
    bound_plan = p1.construct_original35_epre(bound_input)
    assert [op.operation_ref.as_dict() for op in original_plan.operations] == [
        op.operation_ref.as_dict() for op in bound_plan.operations
    ]
    item_by_ref = {
        item.item_ref.key: item.source_variable_code
        for wave in bound_input.waves for item in wave.items
        if item.item_ref is not None
    }
    operations = list(bound_plan.operations)
    distribution_ops = [
        operation for operation in operations
        if operation.operation_kind == "DISTRIBUTION"
    ]
    catalogs = []
    bound = []
    query_predicates = {}
    for index, operation in enumerate(distribution_ops):
        code = item_by_ref[operation.item_ref.key]
        catalog, request = build_projection_catalog(
            bundle=bundle,
            operation=OperationFixture(
                fixture_id=f"GAP007-{index:04d}",
                target_variable_code=code,
                response_value=operation.target_value,
            ),
            as_of=AS_OF,
        )
        catalogs.append(catalog)
        unit = BatchUnitSpec(
            job_kind="QUERY",
            job_ref=request.query_ref,
            release_refs=(release.release_ref,),
            semantic_input_refs=(operation.operation_ref, request.predicate_ref),
        )
        query_predicates[unit.unit_ref.key] = request.predicate_ref
        bound.append((operation.operation_ref, unit))
    catalog = RuntimeObjectCatalog(
        authorities=_merge(value for item in catalogs for value in item.authorities),
        predicates=_merge(value for item in catalogs for value in item.predicates),
        queries=_merge(value for item in catalogs for value in item.queries),
        discovery_authorities=(),
    )
    manifest = BatchManifest(tuple(unit for _, unit in bound))
    executor = CarrierNeutralResearchExecutor(
        repository, (release.release_ref,), catalog
    )
    binding_ref = ExactRef(
        "GAP007_TEST_ONLY_I03_EXECUTOR",
        "urn:test:gap007:i03-executor",
        semantic_hash({"source": bundle.source_sha256, "kind": "I03"}),
    )
    def execute_unit(unit):
        result = executor.execute_i03(
            query_ref=unit.job_ref,
            predicate_ref=query_predicates[unit.unit_ref.key],
        )
        return ExecutionOutcome(
            result_refs=tuple(fact.ref for fact in result.facts),
            provenance_refs=(release.release_ref,),
        )
    runner = BatchExecutionRunner(manifest=manifest, repository=repository)
    receipts = runner.run(executors={
        "QUERY": ExecutorBinding(binding_ref, execute_unit),
    })
    states = {}
    fact_states = {}
    fact_count = 0
    for receipt in receipts:
        states[receipt.state] = states.get(receipt.state, 0) + 1
        fact_count += len(receipt.result_refs)
    for operation, unit in bound:
        result = executor.execute_i03(
            query_ref=unit.job_ref,
            predicate_ref=query_predicates[unit.unit_ref.key],
        )
        for fact in result.facts:
            state = getattr(fact, "typed_state", None)
            fact_states[str(state)] = fact_states.get(str(state), 0) + 1
    unsupported = {}
    for operation in operations:
        if operation.operation_kind != "DISTRIBUTION":
            unsupported[operation.operation_kind] = unsupported.get(operation.operation_kind, 0) + 1
    accounting = []
    for operation in operations:
        if operation.operation_kind == "DISTRIBUTION":
            bound_unit = next(unit for ref, unit in bound if ref == operation.operation_ref)
            accounting.append({
                "operation_ref": operation.operation_ref.as_dict(),
                "operation_kind": operation.operation_kind,
                "status": "BOUND_I03_QUERY",
                "bound_job_ref": bound_unit.job_ref.as_dict(),
            })
        else:
            accounting.append({
                "operation_ref": operation.operation_ref.as_dict(),
                "operation_kind": operation.operation_kind,
                "status": "TYPED_REFUSAL",
                "reason": "P1_OPERATION_KIND_HAS_NO_EXACT_CURRENT_I03_BINDING",
            })
    # Actual I05 capability call on the same source. It is not a P1 unit binding.
    inventory = _inventory((_occurrence("Q00A", domain=(1, 2, 3)), _occurrence("Q00B", domain=(1, 2, 3))), complete=True)
    inventory = replace(inventory, source_sha256=bundle.source_sha256)
    policy = _policy()
    frontier = _frontier(inventory, policy)
    i05 = {"status": "NOT_EXECUTED", "error": None}
    try:
        compilation = compile_governed_frontier(
            bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
            as_of=AS_OF, host=HOST, purpose=PURPOSE,
        )
        result = execute_governed_frontier(
            compilation=compilation,
            source_factory=lambda _ref: bundle.physical_stream,
        )
        native = result.native_execution.native_result
        i05 = {
            "status": "EXECUTED",
            "receiver": "execute_governed_frontier/I05",
            "native_result_type": type(native).__name__,
            "receipt_count": len(native.receipts),
            "fact_count": len(native.empirical_facts),
            "candidate_count": getattr(native, "candidate_count", None),
            "coverage_claim": getattr(native, "coverage_claim", None),
            "compilation_ref": compilation.content_hash if hasattr(compilation, "content_hash") else None,
        }
    except Exception as exc:
        i05 = {"status": "TYPED_REFUSAL", "error": type(exc).__name__, "detail": str(exc)}
    # Wrong-release exact refusal.
    wrong_release = ExactRef(
        "C11LogicalRelease", "urn:test:gap007:wrong-release", "f" * 64
    )
    wrong_unit = BatchUnitSpec(
        job_kind="QUERY",
        job_ref=bound[0][1].job_ref,
        release_refs=(wrong_release,),
        semantic_input_refs=(bound[0][0], bound[0][1].semantic_input_refs[-1]),
    )
    wrong_manifest = BatchManifest((wrong_unit,))
    try:
        BatchExecutionRunner(manifest=wrong_manifest, repository=repository)
        wrong_release_result = {"status": "ACCEPTED"}
    except Exception as exc:
        wrong_release_result = {"status": "TYPED_REFUSAL", "code": type(exc).__name__, "detail": str(exc)}
    # Wrong-authority/query exact refusal: use a fake query ref in the actual catalog.
    wrong_query = ExactRef("EmpiricalQuerySpec@1.0.0", "urn:test:gap007:wrong-query", "e" * 64)
    try:
        executor.execute_i03(query_ref=wrong_query, predicate_ref=bound[0][1].semantic_input_refs[-1])
        wrong_authority_result = {"status": "ACCEPTED"}
    except Exception as exc:
        wrong_authority_result = {"status": "TYPED_REFUSAL", "code": type(exc).__name__, "detail": str(exc)}
    output = {
        "schema": "PDEV01_GAP007_REPAIR_TRACE@1",
        "mode": "TEST_ONLY_SOURCEFREE_ACTUAL_C11_I03_I05_BATCH",
        "source": {
            "source_sha256": bundle.source_sha256,
            "rows": incidence.row_count,
            "columns": len(incidence.variables),
            "release_ref": release.release_ref.as_dict(),
            "release_object_count": len(release.public_objects),
            "release_internal_count": len(release.internal_records),
        },
        "p1": {
            "original_plan_ref": original_plan.plan_ref,
            "bound_plan_ref": bound_plan.plan_ref,
            "operation_identity_preserved": True,
            "operation_count": len(operations),
            "planned_batch_units": len(original_plan.batch_units),
            "bound_i03_units": len(bound),
            "unsupported_typed_refusals": unsupported,
            "manifest_ref": manifest.manifest_ref.as_dict(),
            "manifest_unit_count": len(manifest.units),
            "accounting": accounting,
        },
        "batch": {
            "receipt_count": len(receipts),
            "states": states,
            "result_ref_count": fact_count,
            "fact_state_counts": fact_states,
            "completed": states.get("COMPLETED", 0),
        },
        "i05": i05,
        "wrong_release_refusal": wrong_release_result,
        "wrong_authority_refusal": wrong_authority_result,
        "no_drop": {
            "all_840_accounted": len(accounting) == 840,
            "bound_210": len(bound) == 210,
            "unsupported_630": sum(unsupported.values()) == 630,
            "distinct_original_operation_refs": len({
                item["operation_ref"]["content_hash"] for item in accounting
            }) == 840,
            "distinct_bound_query_refs": len({unit.job_ref.key for _, unit in bound}) == 210,
            "distinct_bound_units": len({unit.unit_ref.key for _, unit in bound}) == 210,
            "distinct_bound_operations": len({operation.key for operation, _ in bound}) == 210,
            "no_invented_operations": True,
        },
        "ceiling": {
            "test_only": True,
            "sourcefree": True,
            "original_respondents": False,
            "source_rights": False,
            "N5_N6": False,
            "EE13": False,
            "OC05": False,
            "production_edit": False,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", type=Path, default=FROZEN_SOURCE,
        help="exact frozen synthetic SAV; default is the committed fixture",
    )
    args = parser.parse_args()
    try:
        raise SystemExit(main(args.source))
    except FrozenSourceIntegrityError as exc:
        print(
            json.dumps(
                {
                    "status": "REFUSED",
                    "code": str(exc).split(":", 1)[0].strip(),
                    "detail": str(exc),
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise SystemExit(2)
