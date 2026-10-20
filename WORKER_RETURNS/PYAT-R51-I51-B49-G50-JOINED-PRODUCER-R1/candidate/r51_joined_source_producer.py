"""R51 sourcefree joined producer: B49 selected source/native preimage → G50 symbolic frontier → B49 native U43/C11/I03/Batch consumer.

No raw source, no native source right, no issued M48 policy, no ADP019/actor.
The B49 one-target TEST_ONLY operation adapter is intentionally narrow: a G50
JOINT/CONDITIONAL operation is reported as a typed unsupported native arity,
never silently flattened into a different scientific claim.
"""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pandas as pd

from rawlsing_next.pre553_inherited_source_rules import (
    SourceAuthorityCorpus, all35_coverage_ledger, select_source_rules,
)
from rawlsing_next.pre553_physical_decoder import PhysicalSourceIncidence, PhysicalVariable
from rawlsing_next.pre553_source_native_preimage_adapter import (
    InstrumentInventory, NativeInstrumentVariable, build_authority_set,
    materialize_native_preimages,
)
from rawlsing_next.pre553_native_workload_binding import (
    OperationFixture, build_projection_catalog, build_test_only_workload,
    execute_test_only_workload,
)
from g50.enumerate import enumerate_frontier
from g50.types import ItemOccurrence, MeasurePlan, ScientificGrammarPolicy, SourceDecisionBundle

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "inputs"
CORPUS_PATH = INPUTS / "source_authority_corpus.json"
AS_OF = "2026-10-20"
SCOPE = "LiTS-I-SYNTHETIC"
SOURCE_ROWS = (
    (1, 2, "US", 1, "S1"),
    (3, 4, "US", 2, "S2"),
    (5, None, "US", 3, "S3"),
)
SOURCE_COLUMNS = ("q301_2", "q301_7", "country", "w1", "id")
MUTATED_ROWS = (
    (1, 2, "US", 1, "S1"),
    (1, 4, "US", 2, "S2"),
    (5, None, "US", 3, "S3"),
)
RESERVED = ("ID", "Y", "H", "RT", "X1", "X2", "SET", "RANK", "REP", "A")
PROPOSAL_OWNER = "M48_PROPOSED@91f70358a7682e983276e79777bc591841162392"
POLICY_ID = "R51-M48-PROPOSED-CANDIDATE-1"


class JoinRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _hash(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode()).hexdigest()


def corpus() -> SourceAuthorityCorpus:
    return SourceAuthorityCorpus.from_document(json.loads(CORPUS_PATH.read_text()))


def selected_package():
    return select_source_rules(corpus(), family="LiTS", wave="I", as_of=AS_OF)


def incidence(rows=SOURCE_ROWS, sha=None):
    sha = sha or selected_package().source.declared_sha256
    variables = tuple(
        PhysicalVariable(i, name, None, f"label-{name}", {}, (), {}, {})
        for i, name in enumerate(SOURCE_COLUMNS, 1)
    )
    return PhysicalSourceIncidence(
        source_sha256=sha, source_format="SYNTHETIC", row_count=len(rows),
        variables=variables, reader_configuration={"fixture": "r51"},
        file_metadata={"fixture": "r51"}, _frame=pd.DataFrame(rows, columns=SOURCE_COLUMNS),
    )


def inventory(sha=None):
    sha = sha or selected_package().source.declared_sha256
    return InstrumentInventory(
        source_id="27", source_sha256=sha,
        variables=tuple(
            NativeInstrumentVariable(name, i, (), "TEST_ONLY_REPRESENTATION")
            for i, name in enumerate(SOURCE_COLUMNS, 1)
        ),
        respondent_count=3, id_variable="id", country_variable="country",
        weight_variable="w1", country_scope=("US",),
    )


def b49_bundle(rows=SOURCE_ROWS):
    package = selected_package()
    authorities = build_authority_set(source=package.source, as_of=AS_OF)
    return materialize_native_preimages(
        package=package, inventory=inventory(package.source.declared_sha256),
        incidence=incidence(rows, package.source.declared_sha256),
        authorities=authorities, as_of=AS_OF,
    )


def _item(item_id: str, domain: tuple[int, ...]) -> ItemOccurrence:
    return ItemOccurrence(
        item_id=item_id, label=item_id, unit="adult", topology="SCALAR_SINGULAR",
        forms=("F",), domain=domain, target_role=True, conditioner_role=True,
        route_state="KNOWN", semantic_state="CERTIFIED_DIRECTIONAL", scope=SCOPE,
        administered=True,
    )


def g50_bundle(b49=None) -> SourceDecisionBundle:
    """Normalize only exact B49 selected administered items.

    Domains are frozen from the sourcefree fixture, not from current values:
    outcome values must not define E_pre membership.
    """
    b49 = b49 or b49_bundle()
    package = selected_package()
    by_code = {item.source_variable_code for item in b49.administered}
    if not {"q301_2", "q301_7"} <= by_code:
        raise JoinRefusal("B49_ADMINISTERED_PAIR_MISSING")
    items = (_item("q301_2", (1, 3, 5)), _item("q301_7", (2, 4)))
    for code in RESERVED:
        items += (_item(code, (0, 1)),)
    return SourceDecisionBundle(
        bundle_id="R51-B49-LiTS-I-JOIN-1",
        source_id=package.source.source_id, wave=package.source.wave,
        edition=package.source.declared_sha256,
        source_sha256=package.source.declared_sha256, scope=SCOPE,
        items=items,
        measure_plans=(
            MeasurePlan("M-SAMPLE", "SAMPLE", None, None,
                        "achieved-sample-description", "UNQUANTIFIED_SAMPLE"),
        ),
        risk_set_ref="RISK-R51-LiTS-I", route_states=("KNOWN",),
        unit_transforms=("ADULT_SELF",), state_map={"MISSING": "NOT_ADMINISTERED"},
        authority_refs=(package.authority_object_identity,),
        current_selection=None, inventory_complete=True,
        held=("CURRENT_SOURCE_HOST_PURPOSE_NOT_GRANTED",),
        unresolved=("D2_COMPLETE_ADMINISTERED_OCCURRENCES",
                    "D3_ROUTE_UNIT_STATE_FOR_UNKNOWN", "D5_ISSUED_GRAMMAR_POLICY"),
    )


def policy(target_roles=("q301_2", "q301_7")) -> ScientificGrammarPolicy:
    return ScientificGrammarPolicy(
        policy_id=POLICY_ID, grade="PROPOSED_TEST_ONLY",
        allowed_classes=("DIST", "CONDITIONAL", "JOINT", "CO_TRAVEL"),
        separate_classes=("CROSS_SOURCE", "TEMPORAL", "POSSIBILITY", "STRUCTURAL"),
        target_roles=tuple(target_roles),
        conditioner_roles=("q301_2", "q301_7"),
        denied_roles=("ID",), bounds={"J": 2, "K": 1, "D": 1},
        population_requires_weight=True,
        exclusions=("ADMIN_ID_TARGET", "TARGET_LEAKAGE", "UNLINKED_UNIT_JOINT",
                    "UNKNOWN_ROUTE", "DISJOINT_FORMS", "UNSANCTIONED_TOPOLOGY",
                    "POPULATION_WITHOUT_WEIGHT", "REVERSE_ROLE_NOT_AUTHORIZED",
                    "TARGET_ALIAS_AS_CONDITIONER"),
        validation_policy="EXPLORATORY_DESCRIPTIVE_ONLY_UNTIL_COMPETENT_VALIDATION",
        exploration_policy="FINITE_FULL_SYMBOLIC_FRONTIER_NO_UNARY_PRUNE",
        stop_policy="EXACT_COMPLETE_OR_BUDGET_PARTIAL",
        owner_refs=(PROPOSAL_OWNER,), authority_refs=("urn:r51:proposal:policy",),
    )


def frontier(bundle=None, pol=None):
    return enumerate_frontier(bundle or g50_bundle(), pol or policy())


def find_eligible(front, *, target="q301_2", claim_class="DIST"):
    for op in front.eligible():
        if op.claim_class == claim_class and op.targets == (target,):
            return op
    raise JoinRefusal("NO_ELIGIBLE_OPERATION", f"{claim_class}:{target}")


def lower_to_b49(operation) -> OperationFixture:
    if len(operation.targets) != 1:
        raise JoinRefusal("B49_ONE_TARGET_ADAPTER_UNSUPPORTED",
                          f"arity={len(operation.targets)} operation={operation.op_id}")
    if operation.conditions:
        raise JoinRefusal("B49_ONE_TARGET_ADAPTER_UNSUPPORTED",
                          f"conditions={operation.conditions} operation={operation.op_id}")
    target = operation.targets[0]
    response = {"q301_2": "1", "q301_7": "2"}.get(target)
    if response is None:
        raise JoinRefusal("B49_TARGET_NOT_IN_ADMINISTERED_INVENTORY", target)
    return OperationFixture(fixture_id=f"R51-{operation.op_id.split(':')[-1][:12]}",
                            target_variable_code=target, response_value=response)


def execute_joined(operation=None, *, rows=SOURCE_ROWS):
    """Run the selected G50 operation through the real B49 U43/C11/I03/Batch consumer."""
    b49 = b49_bundle(rows)
    op = operation or find_eligible(frontier())
    fixture = lower_to_b49(op)
    catalog, request = build_projection_catalog(bundle=b49, operation=fixture, as_of=AS_OF)
    issued = build_test_only_workload(
        bundle=b49, projection=b49.projection, catalog=catalog, request=request,
        operation=fixture, as_of=AS_OF, host="local-r51", purpose="TEST_ONLY_SOURCEFREE",
    )
    result = execute_test_only_workload(
        issued=issued, source_factory=lambda _ref: incidence(rows, b49.source_sha256),
        host="local-r51", purpose="TEST_ONLY_SOURCEFREE",
    )
    fact = result.native_outputs[0].facts[0]
    fields = dict(fact.semantic_fields)
    join_receipt = {
        "schema": "R51_JOINED_SOURCE_TO_NATIVE_CONSUMER@1",
        "sourcefree_test_only": True,
        "source_id": selected_package().source.source_id,
        "family": selected_package().source.family,
        "wave": selected_package().source.wave,
        "source_sha256": b49.source_sha256,
        "b49_package_hash": selected_package().package_hash,
        "b49_administered_ids": list(b49.administered_ids),
        "g50_bundle_id": g50_bundle(b49).bundle_id,
        "g50_bundle_hash": g50_bundle(b49).content_hash,
        "g50_policy_id": operation.policy_id if operation else POLICY_ID,
        "g50_policy_grade": "PROPOSED_TEST_ONLY",
        "g50_operation_id": op.op_id,
        "g50_claim_class": op.claim_class,
        "g50_targets": list(op.targets),
        "g50_conditions": [list(x) for x in op.conditions],
        "frontier_e_pre_root": frontier(pol=operation_policy()).e_pre_root if operation else None,
        "b49_fixture_id": fixture.fixture_id,
        "b49_target_variable_code": fixture.target_variable_code,
        "b49_response_value": fixture.response_value,
        "b49_native_fact_ref": fact.ref.as_dict(),
        "b49_batch_state": result.summary.batch_state,
        "b49_native_numerator": fields.get("raw_numerator_support"),
        "b49_native_denominator": fields.get("raw_denominator_support"),
        "consumer": "PRE553_I03_EXACT_EMPIRICAL_QUERY@1.0.0",
        "consumer_execution_detail": fields.get("execution_detail"),
        "adp019_admission_receipt": "ADP019_ADMISSION_RECEIPT_ABSENT",
        "e2_performed": False,
        "native_actor_admitted": False,
        "original_e_pre": None,
        "original_u": None,
        "current_source_host_purpose_grant": None,
    }
    return result, join_receipt


def operation_policy():
    return policy()


def source_value_mutation():
    good_op = find_eligible(frontier())
    good, good_receipt = execute_joined(good_op)
    bad, bad_receipt = execute_joined(good_op, rows=MUTATED_ROWS)
    return good_receipt, bad_receipt


def policy_mutation_removes_operation():
    op = find_eligible(frontier())
    mutated = frontier(pol=policy(target_roles=("q301_7",)))
    remaining = [(x.op_id, x.disposition) for x in mutated.operations
                 if x.claim_class == "DIST" and x.targets == ("q301_2",)]
    return op, remaining


def coverage():
    return all35_coverage_ledger(corpus())


def canary_rows():
    import csv
    with (INPUTS / "28_CANARY_DISPOSITION.csv").open(newline="", encoding="utf8") as fh:
        return list(csv.DictReader(fh))
