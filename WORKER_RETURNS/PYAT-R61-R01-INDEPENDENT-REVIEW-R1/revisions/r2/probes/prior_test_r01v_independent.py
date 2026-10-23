"""R01V independent hostile probes (disposable; live below reviewer return root).

Oracle content is from INPUTS/CONTRACTS.md Revision 2 and R01/R01V commissions.
Candidate output is never used to derive the expected sets. Tests named
``test_DEFECT_*`` assert the contract-required behavior and are expected to
fail on the candidate; their failures are the evidence.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib
import inspect
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, semantic_hash
from rawlsing_next.universal_grammar.enumerate import (
    conservation_report,
    enumerate_frontier,
    inventory_ledger,
    iter_partitions,
)
from rawlsing_next.universal_grammar.native_map import (
    NATIVE_UNSUPPORTED,
    SUPPORTED,
    NativeCatalog,
    lower_frontier,
    lower_operation,
    native_receipt_anti_join,
)
from rawlsing_next.universal_grammar import types as ug_types
from rawlsing_next.universal_grammar.types import (
    ADMINISTERED,
    ADMINISTRATION_UNKNOWN,
    DEFERRED,
    DirectionGrant,
    ELIGIBLE,
    GrammarPolicy,
    HELD,
    INAPPLICABLE_PROVED,
    MeasurePlan,
    NOT_ADMINISTERED,
    Occurrence,
    OccurrenceKey,
    PROHIBITED,
    SourceInventory,
    UNKNOWN,
    UNSUPPORTED_RUNTIME,
)

REPO_ROOT = Path(__file__).resolve().parents[5]


def _measures():
    return (MeasurePlan("SAMPLE", "SAMPLE", None, None,
                        "independent-sample-proportion", "UNQUANTIFIED_SAMPLE"),)


def _grants():
    return (
        DirectionGrant(("OUTCOME",), (), "DIST", "D-DIST"),
        DirectionGrant(("OUTCOME",), (), "STATE_ROBUSTNESS", "D-STATE"),
        DirectionGrant(("OUTCOME",), ("EXPOSURE",), "CONDITIONAL", "D-COND"),
        DirectionGrant(("OUTCOME",), ("EXPOSURE",), "FORK", "D-FORK"),
        DirectionGrant(("OUTCOME",), ("EXPOSURE", "EXPOSURE"), "CONDITIONAL", "D-COND2"),
        DirectionGrant(("OUTCOME",), ("EXPOSURE", "EXPOSURE"), "FORK", "D-FORK2"),
        DirectionGrant(("OUTCOME",), ("EXPOSURE", "EXPOSURE"), "INTERACTION", "D-INT2"),
        DirectionGrant(("OUTCOME", "OUTCOME"), (), "JOINT", "D-JOINT"),
        DirectionGrant(("OUTCOME", "OUTCOME"), (), "CO_TRAVEL", "D-COT"),
        DirectionGrant(("OUTCOME", "OUTCOME"), ("EXPOSURE",), "JOINT", "D-JOINTC"),
        DirectionGrant(("OUTCOME", "OUTCOME"), ("EXPOSURE",), "CO_TRAVEL", "D-COTC"),
    )


def _policy(*, j=2, k=1, d=0):
    return GrammarPolicy(
        policy_id="R01V-ORACLE-POLICY",
        grade="PROPOSED_TEST_ONLY",
        allowed_classes=("DIST", "CONDITIONAL", "JOINT", "CO_TRAVEL", "FORK",
                         "INTERACTION", "STATE_ROBUSTNESS"),
        separate_classes=(),
        target_roles=("OUTCOME", "EXPOSURE"),
        conditioner_roles=("EXPOSURE", "OUTCOME"),
        administrative_roles=("IDENTITY",),
        direction_grants=_grants(),
        bounds={"J": j, "K": k, "D": d},
        population_requires_weight=False,
        validation_policy="EXPLORATORY_TEST_ONLY",
        exploration_policy="FINITE_FULL_SYMBOLIC_FRONTIER",
        stop_policy="EXACT_COMPLETE_OR_BUDGET_PARTIAL_WITH_PENDING_IDS",
        owner_refs=("R01V-REVIEWER",),
        authority_refs=("urn:r01v:oracle:1",),
    )


def _occ(item, *, domain=(0, 1), target_role="OUTCOME",
         conditioner_role="EXPOSURE", topology="SCALAR_SINGULAR",
         forms=("ALL_FORM",), form_id=None, repeat_id=None,
         administration=ADMINISTERED, route_state="KNOWN",
         scope="WAVE-A", risk=("RISK-A",), unit="person",
         administrative_role=None):
    return Occurrence(
        key=OccurrenceKey(item, form_id=form_id, repeat_id=repeat_id),
        label=item.upper(), unit=unit, topology=topology, forms=forms,
        domain=tuple(domain), target_role=target_role,
        conditioner_role=conditioner_role,
        administrative_role=administrative_role,
        administration=administration, route_state=route_state,
        scope=scope, risk_set_refs=tuple(risk),
    )


def _inventory(occurrences, *, source_sha="a" * 64, wave="WAVE-A",
               edition="EDITION-1", inventory_id="R01V-INV",
               measures=None, complete=True, gaps=(), held=(),
               current_selection=None):
    return SourceInventory(
        inventory_id=inventory_id, source_id="R01V-SOURCE", wave=wave,
        edition=edition, source_sha256=source_sha, scope="WAVE-A",
        occurrences=tuple(occurrences), measure_plans=measures or _measures(),
        risk_set_refs=("RISK-A",), unit_transforms=("PERSON_SELF",),
        state_map={"DK": "DONT_KNOW"}, authority_refs=("R01V-REVIEWER",),
        current_selection=current_selection, inventory_complete=complete,
        inventory_gaps=tuple(gaps), held=tuple(held), unresolved=(),
    )


def _ref(kind, object_id):
    digest = hashlib.sha256(f"{kind}|{object_id}".encode()).hexdigest()
    return ExactRef(kind, object_id, digest)


def _frontier(inv=None, pol=None, **kwargs):
    return enumerate_frontier(inv or _inventory((_occ("alpha"), _occ("beta"),
                                                 _occ("gamma"), _occ("delta"))),
                              pol or _policy(), **kwargs)


def _find(frontier, cls, targets, conditions=(), measure_id="SAMPLE"):
    tkeys = tuple(OccurrenceKey(item) for item in targets)
    ckeys = tuple((OccurrenceKey(item), value) for item, value in conditions)
    hits = [op for op in frontier.operations
            if op.claim_class == cls and op.targets == tkeys
            and op.conditions == ckeys and op.measure_id == measure_id]
    assert hits, (cls, targets, conditions)
    return hits[0]


# ---------------------------------------------------------------- core oracle
def test_frontier_covers_exact_ordered_target_condition_pairs():
    """Hand oracle: 4 ordered target tuples x 5 ordered condition tuples = 20."""
    f = _frontier(_inventory((
        _occ("alpha", conditioner_role=None),
        _occ("beta", conditioner_role=None),
        _occ("gamma", target_role=None),
        _occ("delta", target_role=None),
    )), _policy(j=2, k=1, d=0))
    target_orders = {
        (OccurrenceKey("alpha"),),
        (OccurrenceKey("beta"),),
        (OccurrenceKey("alpha"), OccurrenceKey("beta")),
        (OccurrenceKey("beta"), OccurrenceKey("alpha")),
    }
    cond_orders = {
        (),
        ((OccurrenceKey("gamma"), 0),),
        ((OccurrenceKey("gamma"), 1),),
        ((OccurrenceKey("delta"), 0),),
        ((OccurrenceKey("delta"), 1),),
    }
    observed = {(op.targets, op.conditions) for op in f.operations}
    assert observed == {(t, c) for t in target_orders for c in cond_orders}
    # Ordered permutations are distinct identities, not set aliases.
    assert _find(f, "JOINT", ("alpha", "beta")).op_id != _find(
        f, "JOINT", ("beta", "alpha")).op_id
    assert len({op.op_id for op in f.operations}) == len(f.operations)
    assert all(op.target_roles == tuple(
        "OUTCOME" for _ in op.targets) for op in f.operations)
    assert all(op.conditioner_roles == tuple(
        "EXPOSURE" for _ in op.conditions) for op in f.operations)


def test_two_condition_order_is_semantic_and_all_pairs_present():
    """K=2 hand oracle: 13 ordered typed condition tuples for one target."""
    f = _frontier(_inventory((
        _occ("alpha", conditioner_role=None),
        _occ("gamma", target_role=None),
        _occ("delta", target_role=None),
    )), _policy(j=1, k=2, d=0))
    g, d = OccurrenceKey("gamma"), OccurrenceKey("delta")
    expected = {
        (),
        ((g, 0),), ((g, 1),), ((d, 0),), ((d, 1),),
        ((g, 0), (d, 0)), ((g, 0), (d, 1)),
        ((g, 1), (d, 0)), ((g, 1), (d, 1)),
        ((d, 0), (g, 0)), ((d, 0), (g, 1)),
        ((d, 1), (g, 0)), ((d, 1), (g, 1)),
    }
    observed = {op.conditions for op in f.operations
                if tuple(op.targets) == (OccurrenceKey("alpha"),)}
    assert observed == expected
    a = _find(f, "CONDITIONAL", ("alpha",), (("gamma", 0), ("delta", 1)))
    b = _find(f, "CONDITIONAL", ("alpha",), (("delta", 1), ("gamma", 0)))
    assert a.op_id != b.op_id and a.conditions != b.conditions


def test_no_values_dependent_pruning_and_row_order_invariance():
    inv = _inventory((
        _occ("alpha", conditioner_role=None), _occ("beta", conditioner_role=None),
        _occ("gamma", target_role=None), _occ("delta", target_role=None),
    ))
    first = _frontier(inv, _policy())
    shuffled = _inventory(tuple(reversed(inv.occurrences)))
    second = _frontier(shuffled, _policy())
    assert first.content_hash == second.content_hash
    assert [op.op_id for op in first.operations] == [op.op_id for op in second.operations]
    assert "values" not in inspect.signature(enumerate_frontier).parameters
    assert "observations" not in inspect.signature(enumerate_frontier).parameters


def test_administration_duplicate_and_valid_empty_vs_incomplete():
    occs = (
        _occ("normal"),
        _occ("not_admin", administration=NOT_ADMINISTERED),
        _occ("unknown_admin", administration=ADMINISTRATION_UNKNOWN),
        _occ("admin_row", target_role=None, conditioner_role=None,
             administrative_role="IDENTITY"),
    )
    f = _frontier(_inventory(occs), _policy(j=1, k=0, d=0))
    for op in f.operations:
        if any(key.item_id == "not_admin" for key in op.targets):
            assert op.disposition == HELD and "NOT_ADMINISTERED" in op.reasons[0]
        if any(key.item_id == "unknown_admin" for key in op.targets):
            assert op.disposition == UNKNOWN
    assert all(op.targets[0].item_id != "admin_row" for op in f.operations)
    ledger = inventory_ledger(_inventory(occs), _policy(j=1, k=0, d=0))
    assert next(e for e in ledger if e.administrative_role == "IDENTITY").disposition == PROHIBITED
    with pytest.raises(ValueError, match="DUPLICATE_OCCURRENCE"):
        _inventory((_occ("dup"), _occ("dup")))
    # Valid empty complete frontier vs absent/incomplete evidence.
    adm_only = _frontier(_inventory((_occ("admin", target_role=None,
                                          conditioner_role=None,
                                          administrative_role="IDENTITY"),)),
                         _policy(j=1, k=0, d=0))
    assert adm_only.operations == ()
    assert adm_only.e_pre_count == 0 and adm_only.e_pre_root is not None
    incomplete = _frontier(_inventory((_occ("alpha"),), complete=False,
                                      gaps=("MISSING_MODULE",)), _policy(j=1, k=0, d=0))
    assert incomplete.e_pre_count is None and incomplete.e_pre_root is None
    assert "INCOMPLETE_DECLARED_INVENTORY" in incomplete.e_pre_cause
    with pytest.raises(ValueError, match="inventory must contain at least one occurrence"):
        _inventory(())


def test_budget_partition_and_cold_recompute_conserve_identity_sets():
    inv = _inventory((
        _occ("alpha", conditioner_role=None), _occ("beta", conditioner_role=None),
        _occ("gamma", target_role=None), _occ("delta", target_role=None),
        _occ("not_admin", administration=NOT_ADMINISTERED, conditioner_role=None),
        _occ("unknown_admin", administration=ADMINISTRATION_UNKNOWN, conditioner_role=None),
        _occ("mr", topology="MULTI_SELECT_SET", conditioner_role=None),
    ))
    full = _frontier(inv, _policy(), budget=None, partition_size=7)
    partial = _frontier(inv, _policy(), budget=3, partition_size=7)
    assert [op.op_id for op in partial.operations] == [op.op_id for op in full.operations]
    assert partial.e_pre_root == full.e_pre_root
    assert partial.maximum_bounds == full.maximum_bounds
    assert len(partial.pending_operation_ids) == len(full.eligible()) - 3
    parts = list(iter_partitions(partial))
    assert [op_id for p in parts for op_id in p.operation_ids] == sorted(
        op.op_id for op in partial.operations)
    code = (
        "import sys; sys.path.insert(0, %r);"
        "from prior_test_r01v_independent import _frontier,_inventory,_occ,_policy;"
        "import json;"
        "inv=_inventory((_occ('alpha',conditioner_role=None),"
        "_occ('beta',conditioner_role=None),_occ('gamma',target_role=None),"
        "_occ('delta',target_role=None),"
        "_occ('not_admin',administration='NOT_ADMINISTERED',conditioner_role=None),"
        "_occ('unknown_admin',administration='UNKNOWN',conditioner_role=None),"
        "_occ('mr',topology='MULTI_SELECT_SET',conditioner_role=None)));"
        "f=_frontier(inv,_policy(),budget=3,partition_size=7);"
        "print(json.dumps({'h':f.content_hash,'r':f.partition_root,"
        "'ids':[o.op_id for o in f.operations],"
        "'d':dict(f.disposition_counts),'p':list(f.pending_operation_ids),"
        "'held':sorted(o.op_id for o in f.operations if o.disposition=='HELD'),"
        "'unk':sorted(o.op_id for o in f.operations if o.disposition=='UNKNOWN'),"
        "'uns':sorted(o.op_id for o in f.operations if o.disposition=='UNSUPPORTED_RUNTIME')}))"
    ) % str(Path(__file__).resolve().parent)
    env = dict(os.environ, PYTHONPATH=str(REPO_ROOT) + os.pathsep + str(Path(__file__).resolve().parent),
               PYTHONDONTWRITEBYTECODE="1")
    # Cold process recomputes the same frozen input; there is no restore ingress.
    proc = subprocess.run([sys.executable, "-c", code], cwd=str(REPO_ROOT),
                          env=env, capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr[-2000:]
    cold = json.loads(proc.stdout)
    assert cold["h"] == partial.content_hash
    assert cold["r"] == partial.partition_root
    assert cold["ids"] == [op.op_id for op in partial.operations]
    assert cold["d"] == dict(partial.disposition_counts)
    assert cold["p"] == list(partial.pending_operation_ids)


def test_conservation_antijoin_rejects_count_preserving_substitution():
    f = _frontier(_inventory((_occ("alpha"),)), _policy(j=1, k=0, d=0))
    ids = [op.op_id for op in f.operations]
    assert conservation_report(f, ids)["no_drop_ok"] is True
    mutated = list(ids)
    mutated[-1] = mutated[0]
    report = conservation_report(f, mutated)
    assert report["no_drop_ok"] is False
    assert report["count_preserving_substitution"] is True
    assert report["missing_operation_ids"] and report["duplicate_operation_ids"]


def test_direction_and_role_order_are_explicit_grants():
    inv = _inventory((_occ("outcome", conditioner_role="OUTCOME"),
                      _occ("exposure", target_role="EXPOSURE",
                           conditioner_role="OUTCOME")))
    f = _frontier(inv, _policy(j=1, k=1, d=0))
    assert _find(f, "DIST", ("exposure",)).disposition == PROHIBITED
    assert _find(f, "DIST", ("exposure",)).reasons == ("DIRECTION_NOT_GRANTED",)
    reverse = _policy(j=1, k=1, d=0)
    reverse = replace(reverse, direction_grants=reverse.direction_grants + (
        DirectionGrant(("EXPOSURE",), (), "DIST", "D-REV-DIST"),
        DirectionGrant(("EXPOSURE",), ("OUTCOME",), "CONDITIONAL", "D-REV-COND"),
    ))
    rf = _frontier(inv, reverse)
    assert _find(rf, "DIST", ("exposure",)).disposition == ELIGIBLE
    assert _find(rf, "CONDITIONAL", ("exposure",),
                 (("outcome", 0),)).disposition == ELIGIBLE


def test_form_repeat_and_topology_are_distinct_ledger_entries():
    inv = _inventory((
        _occ("item", form_id="F1", forms=("F1",)),
        _occ("item", form_id="F2", forms=("F2",)),
        _occ("item", repeat_id="R0"),
        _occ("item", repeat_id="R1"),
        _occ("mr", topology="MULTI_SELECT_SET"),
        _occ("rank", topology="RANKED_RESPONSE"),
    ))
    f = _frontier(inv, _policy(j=2, k=0, d=0))
    assert len({op.op_id for op in f.operations}) == len(f.operations)
    assert any(op.disposition == INAPPLICABLE_PROVED
               for op in f.operations if len(op.targets) == 2)
    # R2 adaption: topology is a lowering capability, not a pre-frontier prune.
    assert any(op.disposition == ELIGIBLE and op.execution_state == "NOT_STARTED"
               for op in f.operations
               if any(key.item_id in {"mr", "rank"} for key in op.targets))


def test_risk_set_and_measure_kind_are_identity_components():
    pol = _policy(j=1, k=0, d=0)
    a = _frontier(_inventory((_occ("alpha", risk=("RISK-A",)),)), pol)
    b = _frontier(_inventory((_occ("alpha", risk=("RISK-B",)),)), pol)
    assert {op.op_id for op in a.operations} != {op.op_id for op in b.operations}


def test_observation_lowerer_trusts_operation_disposition_and_direction():
    """R2 adaption: forged direction must be revalidated/refused at lowering."""
    inv = _inventory((_occ("alpha"),))
    pol = _policy(j=1, k=0, d=0)
    f = _frontier(inv, pol)
    op = next(o for o in f.operations if o.claim_class == "DIST")
    forged = replace(op, direction_ref="FORGED-DIRECTION")
    key = json.dumps([OccurrenceKey("alpha").key], sort_keys=False,
                     separators=(",", ":"))
    catalog = NativeCatalog(
        catalog_ref="urn:r01v:catalog", baseline_predicate_ref=_ref("Predicate", "base"),
        predicate_refs={}, query_refs={key + "|SAMPLE": _ref("QueryTemplate", "q")},
        joint_query_refs={}, marginal_query_refs={},
        supported_claims=("DIST",), supported_topologies=("SCALAR_SINGULAR",),
        supported_condition_modes=("AND",), maximum_target_arity=1,
        maximum_conditioner_arity=0,
    )
    record = lower_operation(inv, pol, forged, catalog)
    assert record.status == NATIVE_UNSUPPORTED
    assert record.reason == "FORGED_OR_UNAUTHORIZED_DIRECTION_REF"
    ok = lower_operation(inv, pol, op, catalog)
    assert ok.status == SUPPORTED


# ------------------------------------------------------------- defect probes
def test_DEFECT_bool_condition_domain_is_representable():
    """CONTRACTS K requires tagged bool values; candidate forbids bool domains."""
    try:
        occ = _occ("bool_condition", domain=(True, False))
    except ValueError as exc:
        pytest.fail(f"typed bool condition domain rejected: {exc}")
    assert occ.domain == (True, False)


def test_DEFECT_explicit_null_condition_value_is_representable():
    """CONTRACTS K requires explicit null distinct from absent."""
    try:
        occ = _occ("null_condition", domain=(None,))
    except ValueError as exc:
        pytest.fail(f"explicit null condition value rejected: {exc}")
    assert occ.domain == (None,)


def test_DEFECT_operation_identity_binds_source_edition_and_digest():
    """K binds source/dataset/wave/edition/digest, not only inventory_id."""
    a = _frontier(_inventory((_occ("alpha"),), source_sha="a" * 64,
                             wave="W1", edition="E1"), _policy(j=1, k=0, d=0))
    b = _frontier(_inventory((_occ("alpha"),), source_sha="b" * 64,
                             wave="W2", edition="E2"), _policy(j=1, k=0, d=0))
    assert a.inventory_hash != b.inventory_hash
    assert {op.op_id for op in a.operations} != {op.op_id for op in b.operations}


def test_DEFECT_operation_identity_binds_estimand_weight_and_design():
    """K binds estimand and weight/design/uncertainty refs, not only measure_id."""
    m1 = MeasurePlan("SAMPLE", "SAMPLE", None, None, "estimand-one", "UNCERTAINTY_ONE")
    m2 = MeasurePlan("SAMPLE", "SAMPLE", "WEIGHT-2", "DESIGN-2",
                     "estimand-two", "UNCERTAINTY_TWO")
    a = _frontier(_inventory((_occ("alpha"),), measures=(m1,)), _policy(j=1, k=0, d=0))
    b = _frontier(_inventory((_occ("alpha"),), measures=(m2,)), _policy(j=1, k=0, d=0))
    assert a.inventory_hash != b.inventory_hash
    assert {op.op_id for op in a.operations} != {op.op_id for op in b.operations}


def test_DEFECT_operation_type_carries_clocks_and_currentness():
    """K binds observation/reference/as-of/publication clocks and selection."""
    fields = set(ug_types.ScientificOperation.__dataclass_fields__)
    missing = {
        "observation_clock_ref", "reference_clock_ref", "as_of_ref",
        "publication_clock_ref", "current_selection_ref",
    } - fields
    assert not missing, f"operation identity cannot represent clocks/currentness: {sorted(missing)}"


def test_DEFECT_eligibility_execution_result_axes_are_separate():
    """CONTRACTS Revision 2: a single enum conflating axes is forbidden."""
    assert hasattr(ug_types, "ELIGIBILITY_STATES")
    assert hasattr(ug_types, "EXECUTION_STATES")
    assert hasattr(ug_types, "RESULT_STATES")
    assert UNSUPPORTED_RUNTIME not in ug_types.DISPOSITIONS
    assert DEFERRED not in ug_types.DISPOSITIONS


def test_DEFECT_native_target_cells_preserve_typed_int_vs_string():
    """No float/string coercion: int 1 and str '1' are distinct K values."""
    inv = _inventory((_occ("target", domain=(1, "1")),))
    pol = _policy(j=1, k=0, d=0)
    f = _frontier(inv, pol)
    op = next(o for o in f.operations if o.claim_class == "DIST")
    key = json.dumps([OccurrenceKey("target").key], sort_keys=False,
                     separators=(",", ":"))
    catalog = NativeCatalog(
        catalog_ref="urn:r01v:catalog", baseline_predicate_ref=_ref("Predicate", "base"),
        predicate_refs={}, query_refs={key + "|SAMPLE": _ref("QueryTemplate", "q")},
        joint_query_refs={}, marginal_query_refs={},
        supported_claims=("DIST",), supported_topologies=("SCALAR_SINGULAR",),
        supported_condition_modes=("AND",), maximum_target_arity=1,
        maximum_conditioner_arity=0,
    )
    record = lower_operation(inv, pol, op, catalog)
    assert record.status == SUPPORTED
    cells = list(record.rule["target_cells"])
    assert [canonicalize(cell) for cell in cells] == [1, "1"], cells


def test_DEFECT_lowering_record_has_required_contract_fields():
    """CONTRACTS 3: version/DiscoveryAuthority/Batch/grade/typed-refusal fields."""
    from rawlsing_next.universal_grammar.native_map import LoweringRecord
    fields = set(LoweringRecord.__dataclass_fields__)
    missing = {
        "lowering_version", "discovery_authority_ref", "batch_unit_refs",
        "evidence_grade_ceiling", "typed_refusal",
    } - fields
    assert not missing, f"lowering record cannot represent contract fields: {sorted(missing)}"


def test_DEFECT_catalog_supported_topology_can_promote_operation():
    """Capability must come from current catalog, not a hardcoded topology gate."""
    inv = _inventory((_occ("mr", topology="MULTI_SELECT_SET"),))
    pol = _policy(j=1, k=0, d=0)
    f = _frontier(inv, pol)
    op = next(o for o in f.operations if o.claim_class == "DIST")
    assert op.disposition == ELIGIBLE
    key = json.dumps([OccurrenceKey("mr").key], sort_keys=False,
                     separators=(",", ":"))
    catalog = NativeCatalog(
        catalog_ref="urn:r01v:catalog", baseline_predicate_ref=_ref("Predicate", "base"),
        predicate_refs={}, query_refs={key + "|SAMPLE": _ref("QueryTemplate", "q")},
        joint_query_refs={}, marginal_query_refs={},
        supported_claims=("DIST",),
        supported_topologies=("SCALAR_SINGULAR", "MULTI_SELECT_SET"),
        supported_condition_modes=("AND",), maximum_target_arity=1,
        maximum_conditioner_arity=0,
    )
    record = lower_operation(inv, pol, op, catalog)
    assert record.status == SUPPORTED, (
        "catalog declares MULTI_SELECT_SET support but frontier pre-classified "
        f"the operation as {op.disposition}; lowerer returned {record.status}/{record.reason}")


def test_DEFECT_native_receipt_antijoin_binds_conditions_not_just_rule_id():
    """I05 receipts must be checked for exact target/condition/value, not only rule_id."""
    from rawlsing_next.pre553_discovery_exact import execute_exact_bounded_discovery
    from rawlsing_next.tests.test_universal_grammar import (
        _native_catalog, _native_fixture,
    )
    from rawlsing_next.tests.test_pre553_discovery_exact import (
        _discovery_authority, _registry as _i05_registry,
    )

    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inv = _inventory((_occ(labels[0]), _occ(labels[1])))
    pol = _policy(j=1, k=1, d=0)
    f = _frontier(inv, pol)
    selected = tuple(op for op in f.operations
                     if op.disposition == ELIGIBLE and op.measure_id == "SAMPLE")
    plan = lower_frontier(inv, pol, replace(f, operations=selected),
                          _native_catalog(labels, all_predicate, predicates, queries))
    grammar = plan.native_grammar()
    authority = _discovery_authority(source, grammar, dauth)
    result = execute_exact_bounded_discovery(
        repository=source["repo"], discovery_authority=authority,
        authority_registry=_i05_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=tuple(predicates.values()) + (all_predicate,),
        query_template_catalog=tuple(queries.values()),
    )
    assert native_receipt_anti_join(plan, result.receipts)["no_drop_ok"] is True
    # Mutate the predicate behind one condition atom without changing rule_id.
    mutated = deepcopy(grammar)
    atoms = list(mutated["atoms"])
    target_atom = next(a for a in atoms if a["predicate_ref"] in
                       [p.ref.as_dict() for (label, value), p in predicates.items()
                        if label == labels[1] and value == 0])
    replacement = next(p.ref.as_dict() for (label, value), p in predicates.items()
                       if label == labels[1] and value == 1)
    idx = atoms.index(target_atom)
    atoms[idx] = {**target_atom, "predicate_ref": replacement}
    mutated["atoms"] = tuple(atoms)
    mutated_authority = _discovery_authority(source, mutated, dauth)
    mutated_result = execute_exact_bounded_discovery(
        repository=source["repo"], discovery_authority=mutated_authority,
        authority_registry=_i05_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=tuple(predicates.values()) + (all_predicate,),
        query_template_catalog=tuple(queries.values()),
    )
    mutated_join = native_receipt_anti_join(plan, mutated_result.receipts)
    assert mutated_join["no_drop_ok"] is False, (
        "changed condition semantics were accepted by rule_id-only anti-join: "
        f"{mutated_join}")
