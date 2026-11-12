"""S1-C hostile SOURCEFREE R03 compiler/issued-reader/fate conservation tests.

The independently *supplied* census in these tests is a test-double frozen
before runtime compilation. It is NOT an original35 scientific issuer.
"""
from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_operation_fate_census import (
    CensusRefusal, FrozenInputCensus, ScientificFate, SourceQualifiedCandidate,
    execute_censused_sourcefree, verify_frozen_inputs,
)
from rawlsing_next.tests.test_universal_workload import (
    AS_OF, HOST, PURPOSE, _frontier_bundle, _frontier_fixture,
)
from rawlsing_next.universal_grammar.enumerate import enumerate_frontier
from rawlsing_next.universal_grammar.types import (
    ADMINISTRATION_UNKNOWN, ELIGIBLE, Occurrence,
)


def _freeze_packet(frontier, *, scope_id="R3-S1C-SOURCEFREE-PACKET"):
    """Two explicitly materialized independent inputs, never compiler output."""
    sources = []
    fates = []
    for op in frontier.operations:
        sources.append(SourceQualifiedCandidate(
            operation_id=op.op_id,
            operation_hash=op.canonical_hash,
            source_id=op.source_id,
            dataset_id=op.dataset_id,
            wave=op.wave,
            edition=op.edition,
            source_sha256=op.source_sha256,
            instrument_ref=op.instrument_ref,
            universe_scope=op.scope,
            occurrence_ids=tuple(
                k.key for k in (
                    tuple(op.targets) + tuple(k for k, _ in op.conditions)
                )
            ),
            meaning_ref="SOURCEFREE_TEST_ONLY_INVENTORY_SEMANTICS",
            source_authority_ref="R61-TEST-ONLY-OWNER",
            source_decision_ref="SOURCEFREE_TEST_ONLY_NOT_CURRENT_PERMISSION",
        ))
        fates.append(ScientificFate(
            operation_id=op.op_id,
            operation_hash=op.canonical_hash,
            disposition=op.disposition,
            eligibility_decision_ref="SOURCEFREE_R61_TEST_ONLY_NOT_ISSUED",
            u_item_ref=frontier.u_item_root or "ABSENT:TEST_ONLY_U_ITEM",
            u_unit_ref=frontier.u_unit_root or "ABSENT:TEST_ONLY_U_UNIT",
            u_app_ref=frontier.u_app_root or "ABSENT:TEST_ONLY_U_APP",
            e_pre_ref_or_absence=frontier.e_pre_root or "ABSENT:NO_ORIGINAL_EPRE",
            reason=";".join(op.reasons) or "EXPLICIT_TEST_ONLY_ELIGIBILITY",
        ))
    return FrozenInputCensus(
        scope_id=scope_id, source_candidates=tuple(sources),
        scientific_fates=tuple(fates),
        source_census_ref=semantic_hash([x.material() for x in sources]),
        science_census_ref=semantic_hash([x.material() for x in fates]),
        deferred_scope_records=tuple(frontier.deferred),
        unknown_scope_records=tuple(frontier.unknown),
        excluded_scope_records=tuple(frontier.excluded),
        inventory_ledger_records=tuple(
            row.material() for row in frontier.inventory_ledger
        ),
    )


def _fixture(tmp_path, *, budget=None):
    bundle, _ = _frontier_bundle(tmp_path / "s1c.sav")
    inventory, policy, frontier = _frontier_fixture(bundle, budget=budget)
    return bundle, inventory, policy, frontier, _freeze_packet(frontier)


def _run(bundle, inventory, policy, frontier, census, factory=None):
    return execute_censused_sourcefree(
        census=census, inventory=inventory, policy=policy, frontier=frontier,
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE,
        source_factory=factory or (lambda _ref: bundle.physical_stream),
    )


def test_s1c_full_frozen_census_reaches_real_issued_reader(tmp_path):
    bundle, inventory, policy, frontier, census = _fixture(tmp_path)
    result = _run(bundle, inventory, policy, frontier, census)
    assert result["grade"] == "TEST_ONLY_SOURCEFREE"
    assert result["declared_operation_count"] == len(census.source_candidates)
    assert result["scientific_fate_count"] == len(census.scientific_fates)
    assert result["compiled_operation_count"] == result["declared_operation_count"]
    assert result["received_operation_count"] == result["declared_operation_count"]
    assert result["candidate_anti_join"]["no_drop_ok"]
    assert result["operation_anti_join"]["no_drop_ok"]
    assert result["native_fact_count"] > 0
    assert result["issued_candidate_count"] > 0
    assert result["source_factory_calls"] > 0
    assert result["checkpoint_hash"]
    assert result["deferred_scope_records"] == list(frontier.deferred)
    assert any(x.get("kind") == "ARITY_DEFERRED"
               for x in result["deferred_scope_records"])
    assert set(row["operation_id"] for row in result["operation_fates"]) == {
        row.operation_id for row in census.source_candidates
    }
    # Unweighted descriptive RAW is executable even though an unrelated
    # population-weighted estimand lacks weight/design evidence.
    sample_ids = {
        op.op_id for op in frontier.operations
        if op.disposition == ELIGIBLE and op.measure_kind == "SAMPLE"
    }
    assert sample_ids
    completed = {
        row["operation_id"] for row in result["operation_fates"]
        if row["execution_state"] == "COMPLETED"
    }
    assert sample_ids & completed
    unsupported = [
        row for row in result["operation_fates"]
        if row["lowering_status"] == "UNSUPPORTED_RUNTIME"
    ]
    assert unsupported
    assert all(not row["received_candidate_ids"] and not row["fact_refs"]
               for row in unsupported)


def test_s1c_omission_and_count_preserving_substitution_fail_before_source_open(tmp_path):
    bundle, inventory, policy, frontier, census = _fixture(tmp_path)
    opened = []
    original = frontier.operations
    removed = original[0]
    omitted = replace(frontier, operations=original[1:])
    with pytest.raises(CensusRefusal, match="FROZEN_VS_FRONTIER_ANTI_JOIN"):
        _run(bundle, inventory, policy, omitted, census,
             lambda ref: opened.append(ref))
    # Replacing one ID with a duplicate cannot pass on unchanged counts.
    substituted = replace(frontier, operations=(original[1],) + original[1:])
    with pytest.raises(CensusRefusal, match="DUPLICATE_FRONTIER_OPERATION"):
        _run(bundle, inventory, policy, substituted, census,
             lambda ref: opened.append(ref))
    assert not opened
    assert removed.op_id in {r.operation_id for r in census.source_candidates}


def test_s1c_source_fate_duplicates_and_cross_set_losses(tmp_path):
    bundle, inventory, policy, frontier, census = _fixture(tmp_path)
    removed = census.source_candidates[0]
    fewer_sources = census.source_candidates[1:]
    fewer_fates = census.scientific_fates[1:]
    duplicate_sources = census.source_candidates + (removed,)
    for bad, code in (
        (replace(census, source_candidates=fewer_sources),
         "SOURCE_CENSUS_HASH_DRIFT"),
        (replace(census, scientific_fates=fewer_fates),
         "SCIENCE_CENSUS_HASH_DRIFT"),
        (replace(census, source_candidates=duplicate_sources),
         "SOURCE_CENSUS_HASH_DRIFT"),
        (replace(census, source_candidates=fewer_sources,
                 source_census_ref=semantic_hash(
                     [x.material() for x in fewer_sources])),
         "SOURCE_VS_SCIENCE_ANTI_JOIN"),
        (replace(census, scientific_fates=fewer_fates,
                 science_census_ref=semantic_hash(
                     [x.material() for x in fewer_fates])),
         "SOURCE_VS_SCIENCE_ANTI_JOIN"),
        (replace(census, source_candidates=duplicate_sources,
                 source_census_ref=semantic_hash(
                     [x.material() for x in duplicate_sources])),
         "DUPLICATE_SOURCE_CANDIDATE"),
    ):
        with pytest.raises(CensusRefusal, match=code):
            verify_frozen_inputs(bad, inventory=inventory,
                                 policy=policy, frontier=frontier)


def test_s1c_source_edition_occurrence_and_op_hash_refuse(tmp_path):
    bundle, inventory, policy, frontier, census = _fixture(tmp_path)
    first = census.source_candidates[0]
    variants = (
        (replace(first, edition="FALSE_EDITION"), "SOURCE_EDITION_UNIVERSE_DRIFT"),
        (replace(first, source_sha256="0" * 64), "SOURCE_EDITION_UNIVERSE_DRIFT"),
        (replace(first, occurrence_ids=("DROPPED",)), "OCCURRENCE_IDENTITY_DRIFT"),
        (replace(first, operation_hash="f" * 64), "OPERATION_IDENTITY_DRIFT"),
        (replace(first, source_grade="ORIGINAL35_ISSUED"), "NON_SOURCEFREE_AUTHORITY_UNISSUED"),
        (replace(first, source_authority_ref="FORGED-OWNER"),
         "SOURCE_AUTHORITY_NOT_IN_FROZEN_INVENTORY"),
    )
    for candidate, code in variants:
        candidates = (candidate,) + census.source_candidates[1:]
        bad = replace(census, source_candidates=candidates,
                      source_census_ref=semantic_hash([x.material() for x in candidates]))
        with pytest.raises(CensusRefusal, match=code):
            verify_frozen_inputs(bad, inventory=inventory,
                                 policy=policy, frontier=frontier)


def test_s1c_fate_mutation_refuses_eligibility_inflation(tmp_path):
    bundle, inventory, policy, frontier, census = _fixture(tmp_path)
    noneligible = next(
        i for i, item in enumerate(census.scientific_fates)
        if item.disposition != ELIGIBLE
    )
    old = census.scientific_fates[noneligible]
    forged = replace(old, disposition=ELIGIBLE)
    scientific_fates = (
        census.scientific_fates[:noneligible] +
        (forged,) + census.scientific_fates[noneligible + 1:]
    )
    bad = replace(census, scientific_fates=scientific_fates,
                  science_census_ref=semantic_hash(
                      [x.material() for x in scientific_fates]
                  ))
    with pytest.raises(CensusRefusal, match="ELIGIBILITY_DRIFT"):
        verify_frozen_inputs(bad, inventory=inventory,
                             policy=policy, frontier=frontier)
    # A real unknown or inapplicable operation must not be silently converted
    # to an administered, scientifically eligible denominator.
    assert old.disposition != ELIGIBLE


def test_s1c_budget_pending_are_accounted_not_fake_completed(tmp_path):
    bundle, inventory, policy, frontier, census = _fixture(tmp_path, budget=5)
    assert frontier.pending_operation_ids
    result = _run(bundle, inventory, policy, frontier, census)
    pending = set(frontier.pending_operation_ids)
    rows = {row["operation_id"]: row for row in result["operation_fates"]}
    assert pending <= set(rows)
    assert all(rows[op]["execution_state"] == "PENDING" for op in pending)
    assert all(not rows[op]["received_candidate_ids"] for op in pending)
    assert result["declared_operation_count"] == result["received_operation_count"]


def test_s1c_routing_unknown_is_retained_without_administered_positive(tmp_path):
    bundle, inventory, policy, _, _ = _fixture(tmp_path)
    changed = tuple(
        replace(occ, administration=ADMINISTRATION_UNKNOWN,
                route_state="UNKNOWN_ROUTING")
        if occ.key.item_id == "A" else occ
        for occ in inventory.occurrences
    )
    altered_inventory = replace(inventory, occurrences=changed)
    frontier = enumerate_frontier(altered_inventory, policy)
    census = _freeze_packet(frontier, scope_id="S1C-ROUTING-UNKNOWN")
    first = verify_frozen_inputs(census, inventory=altered_inventory,
                                 policy=policy, frontier=frontier)
    assert first["source_candidate_count"] == len(frontier.operations)
    affected = [
        op for op in frontier.operations
        if any(k.item_id == "A" for k in (
            tuple(op.targets) + tuple(k for k, _ in op.conditions)
        ))
    ]
    assert affected
    assert all(op.disposition != ELIGIBLE for op in affected)
    # Unknown is neither proved inapplicable nor observed zero.
    assert any(op.disposition in {"UNKNOWN", "HELD"} for op in affected)
    result = _run(bundle, altered_inventory, policy, frontier, census)
    rows = {row["operation_id"]: row for row in result["operation_fates"]}
    assert all(not rows[op.op_id]["received_candidate_ids"]
               for op in affected if op.disposition != ELIGIBLE)
    assert all(not rows[op.op_id]["fact_refs"]
               for op in affected if op.disposition != ELIGIBLE)
    assert result["operation_anti_join"]["no_drop_ok"]


def test_s1c_proved_inapplicable_form_is_retained_not_denominator(tmp_path):
    """Disjoint source-declared administration forms create a real typed fate."""
    bundle, inventory, policy, _, _ = _fixture(tmp_path)
    changed = tuple(
        replace(occ, forms=("DISJOINT_B_FORM",)) if occ.key.item_id == "B"
        else occ
        for occ in inventory.occurrences
    )
    altered_inventory = replace(inventory, occurrences=changed)
    frontier = enumerate_frontier(altered_inventory, policy)
    census = _freeze_packet(frontier, scope_id="S1C-DISJOINT-FORM")
    inapplicable = {
        op.op_id for op in frontier.operations
        if op.disposition == "INAPPLICABLE_PROVED"
    }
    assert inapplicable
    result = _run(bundle, altered_inventory, policy, frontier, census)
    rows = {row["operation_id"]: row for row in result["operation_fates"]}
    assert inapplicable <= set(rows)
    assert all(rows[op]["scientific_disposition"] == "INAPPLICABLE_PROVED"
               and rows[op]["received_candidate_ids"] == []
               and rows[op]["fact_refs"] == []
               for op in inapplicable)
    assert result["operation_anti_join"]["no_drop_ok"]


def test_s1c_changed_valid_eligible_operation_and_restoration(tmp_path):
    """Changing one permitted operation class changes actual I05 receipts."""
    bundle, inventory, policy, frontier, census = _fixture(tmp_path)
    baseline = _run(bundle, inventory, policy, frontier, census)
    assert any(op.claim_class == "JOINT" and op.disposition == ELIGIBLE
               for op in frontier.operations)

    # Sourcefree policy decision removes JOINT eligibility; no operation is
    # silently deleted, because the new declared frontier retains its denied
    # operation IDs and independently re-frozen scientific fate rows.
    narrower_policy = replace(
        policy, allowed_classes=tuple(
            cls for cls in policy.allowed_classes if cls != "JOINT"
        ),
    )
    changed_frontier = enumerate_frontier(inventory, narrower_policy)
    changed_census = _freeze_packet(
        changed_frontier, scope_id="S1C-CHANGED-SOURCEFREE-ISSUER-DECISION"
    )
    changed = _run(bundle, inventory, narrower_policy,
                   changed_frontier, changed_census)
    restored = _run(bundle, inventory, policy, frontier, census)
    assert changed["operation_anti_join"]["no_drop_ok"]
    assert changed["issued_candidate_count"] < baseline["issued_candidate_count"]
    assert changed["checkpoint_hash"] != baseline["checkpoint_hash"]
    assert restored["checkpoint_hash"] == baseline["checkpoint_hash"]
    assert restored["frozen_census_hash"] == baseline["frozen_census_hash"]


def test_s1c_changed_value_and_restore_real_fact_identity(tmp_path):
    from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
    from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
    bundle, inventory, policy, frontier, census = _fixture(tmp_path)
    original = _run(bundle, inventory, policy, frontier, census)
    cells = tuple(bundle.physical_stream.iter_cells())

    def altered_cells():
        return tuple(
            replace(c, raw_value=1.0 - float(c.raw_value))
            if c.variable_name == "A" and
            c.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE
            else c for c in cells
        )
    altered = ExactPhysicalCellStream(
        source_sha256=bundle.source_sha256,
        row_count=bundle.physical_stream.row_count,
        cell_iter_factory=altered_cells,
    )
    changed = _run(bundle, inventory, policy, frontier, census,
                   lambda _ref: altered)
    restored = _run(bundle, inventory, policy, frontier, census)
    def facts(result):
        return {
            r["operation_id"]: tuple(x["content_hash"] for x in r["fact_refs"])
            for r in result["operation_fates"]
        }
    assert facts(original) != facts(changed)
    assert facts(original) == facts(restored)
    assert original["checkpoint_hash"] == restored["checkpoint_hash"]
    assert original["checkpoint_hash"] != changed["checkpoint_hash"]
    assert changed["operation_anti_join"]["no_drop_ok"]


def test_s1c_actual_source_open_and_c11_build_census(tmp_path, monkeypatch):
    """Measure the actual bounded test-only Batch/C11/I05 builder, not U43."""
    from rawlsing_next import pre553_native_workload_binding as binding

    bundle, inventory, policy, frontier, census = _fixture(tmp_path)
    builds = {"bounded_i05_c11": 0}
    original = binding.build_source_backed_c11_repository

    def counted_builder(*args, **kwargs):
        builds["bounded_i05_c11"] += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(binding, "build_source_backed_c11_repository",
                        counted_builder)
    result = _run(bundle, inventory, policy, frontier, census)
    assert result["source_factory_calls"] == 1
    assert result["native_fact_count"] > 0
    assert builds["bounded_i05_c11"] == 1
    # This scoped R03 path uses an actual issued test-only envelope with
    # Batch/C11/I05 once. It does NOT execute the broader normal/resume U43
    # route or claim S1-D CURRENT-authenticated native production.
    print("S1C_RESOURCE_COUNTS", {
        "declared": result["declared_operation_count"],
        "compiled": result["compiled_operation_count"],
        "receipt_rows": result["received_operation_count"],
        "fate_counts": result["fate_counts"],
        "deferred_scope_count": result["deferred_scope_count"],
        "unsupported_runtime_rows": sum(
            row["lowering_status"] == "UNSUPPORTED_RUNTIME"
            for row in result["operation_fates"]
        ),
        "issued_candidates": result["issued_candidate_count"],
        "native_facts": result["native_fact_count"],
        "source_factory_calls": result["source_factory_calls"],
        "bounded_i05_c11_builds": builds["bounded_i05_c11"],
        "elapsed_seconds": round(result["elapsed_seconds"], 6),
    })


def test_s1c_b_unknown_and_excluded_axis_severance_before_source_open(tmp_path):
    """B's reproduced G3 hole: nonoperation negative evidence was unchecked.

    Before the B repair, both changes below passed verify_frozen_inputs:
    all operation IDs, dispositions and deferred rows were unchanged.
    """
    bundle, inventory, policy, frontier, _ = _fixture(tmp_path)
    marked = replace(
        frontier,
        unknown=tuple(frontier.unknown) + ({
            "kind": "ROUTING_UNKNOWN", "occurrence": "INDEPENDENT_SOURCE_ITEM_X",
            "reason": "NO_ADMINISTRATION_PROOF",
        },),
        excluded=tuple(frontier.excluded) + ({
            "kind": "EXCLUDED_SOURCE_ITEM", "occurrence": "INDEPENDENT_SOURCE_ITEM_Y",
            "reason": "NOT_IN_DECLARED_OPERATION_DOMAIN",
        },),
    )
    census = _freeze_packet(marked, scope_id="B-FROZEN-NEGATIVE-AXES")
    assert verify_frozen_inputs(census, inventory=inventory,
                                policy=policy, frontier=marked)["source_candidate_count"]
    opened = []
    for changed, code in (
        (replace(marked, unknown=tuple(frontier.unknown)),
         "UNKNOWN_CENSUS_DRIFT"),
        (replace(marked, excluded=tuple(frontier.excluded)),
         "EXCLUDED_CENSUS_DRIFT"),
    ):
        with pytest.raises(CensusRefusal, match=code):
            execute_censused_sourcefree(
                census=census, inventory=inventory, policy=policy,
                frontier=changed, bundle=bundle, as_of=AS_OF,
                host=HOST, purpose=PURPOSE,
                source_factory=lambda ref: opened.append(ref),
            )
    assert opened == []


def test_s1c_b_inventory_ledger_fate_severance_and_restoration(tmp_path):
    """No silent per-occurrence administrative status loss despite ID parity."""
    bundle, inventory, policy, frontier, census = _fixture(tmp_path)
    assert frontier.inventory_ledger
    baseline = _run(bundle, inventory, policy, frontier, census)
    original = frontier.inventory_ledger[0]
    poison = replace(original, disposition=(
        "UNKNOWN" if original.disposition != "UNKNOWN" else "HELD"
    ))
    changed = replace(
        frontier, inventory_ledger=(poison,) + frontier.inventory_ledger[1:]
    )
    with pytest.raises(CensusRefusal, match="INVENTORY_LEDGER_CENSUS_DRIFT"):
        verify_frozen_inputs(census, inventory=inventory,
                             policy=policy, frontier=changed)
    restored = _run(bundle, inventory, policy, frontier, census)
    assert restored["checkpoint_hash"] == baseline["checkpoint_hash"]
    assert restored["frozen_census_hash"] == baseline["frozen_census_hash"]
    assert restored["inventory_ledger_hash"] == baseline["inventory_ledger_hash"]
    assert restored["operation_anti_join"]["no_drop_ok"]
    assert restored["candidate_anti_join"]["no_drop_ok"]


def test_s1c_b_rehashed_negative_axis_cannot_launder_other_frontier(tmp_path):
    """A source-side rehash cannot substitute for the real frontier state."""
    _, inventory, policy, frontier, census = _fixture(tmp_path)
    marked = replace(frontier, unknown=tuple(frontier.unknown) + ({
        "reason": "ROUTING_UNKNOWN", "source": "separate occurrence"
    },))
    # Honest old frozen declaration, tampered frontier.  Rehashing all
    # operation manifests would still give exactly the same operation hashes.
    assert census.source_census_ref == _freeze_packet(marked).source_census_ref
    assert census.science_census_ref == _freeze_packet(marked).science_census_ref
    with pytest.raises(CensusRefusal, match="UNKNOWN_CENSUS_DRIFT"):
        verify_frozen_inputs(census, inventory=inventory,
                             policy=policy, frontier=marked)



def test_s1c_a_counter_rehashed_occurrence_false_admin_fails_before_source_open(tmp_path):
    """B bypass: forge BOTH inventory-negative copies, leaving real source UNKNOWN.

    The old B verifier compared frozen ledger to supplied frontier ledger only.
    It did not recompute the administrative state from the frozen inventory.
    This tests false authorization in the *reported source evidence*, not a
    claim that actual I05 issued a disallowed operation.
    """
    bundle, inventory, policy, _, _ = _fixture(tmp_path)
    unknown_inventory = replace(inventory, occurrences=tuple(
        replace(o, administration=ADMINISTRATION_UNKNOWN, route_state="KNOWN")
        if o.key.item_id == "A" else o
        for o in inventory.occurrences
    ))
    sourcefront = enumerate_frontier(unknown_inventory, policy)
    census = _freeze_packet(sourcefront, scope_id="A-COUNTER-INVENTORY-UNKNOWN")
    before = next(x for x in sourcefront.inventory_ledger if x.occurrence_id ==
                  next(o.key.key for o in unknown_inventory.occurrences
                       if o.key.item_id == "A"))
    assert before.administration == ADMINISTRATION_UNKNOWN
    assert before.disposition == "UNKNOWN"
    fake_ledger = tuple(
        replace(x, administration="ADMINISTERED", disposition=ELIGIBLE,
                reasons=()) if x.occurrence_id == before.occurrence_id else x
        for x in sourcefront.inventory_ledger
    )
    fake_frontier = replace(sourcefront, inventory_ledger=fake_ledger)
    fake_census = replace(
        census, inventory_ledger_records=tuple(x.material() for x in fake_ledger)
    )
    # All source/science operation IDs and roots are the same; both B axes
    # have been changed coherently. An honest recomputation must reject this.
    assert fake_census.source_census_ref == census.source_census_ref
    assert fake_census.science_census_ref == census.science_census_ref
    opens = []
    with pytest.raises(CensusRefusal, match="INVENTORY_LEDGER_INVENTORY_MISMATCH"):
        _run(bundle, unknown_inventory, policy, fake_frontier, fake_census,
             lambda ref: opens.append(ref))
    assert not opens
    restored = _run(bundle, unknown_inventory, policy, sourcefront, census)
    assert restored["candidate_anti_join"]["no_drop_ok"]
    assert restored["operation_anti_join"]["no_drop_ok"]


def test_s1c_a_counter_joint_forged_unknown_and_excluded_drops_refuse(tmp_path):
    """B bypass: both frozen and live negative lists omit a genuine op fate."""
    _, inventory, policy, frontier, _ = _fixture(tmp_path)
    assert frontier.excluded
    excluded_op = next(
        x for x in frontier.excluded if isinstance(x.get("op_id"), str)
    )
    kept_excluded = tuple(
        x for x in frontier.excluded if x["op_id"] != excluded_op["op_id"]
    )
    forged_excluded = replace(frontier, excluded=kept_excluded)
    forged_excluded_census = _freeze_packet(forged_excluded)
    # B's two-way freeze/frontier comparison passes this co-mutated omission.
    with pytest.raises(CensusRefusal, match="EXCLUDED_OPERATION_NEGATIVE_LOSS"):
        verify_frozen_inputs(forged_excluded_census,
                             inventory=inventory, policy=policy,
                             frontier=forged_excluded)

    unknown_inventory = replace(inventory, occurrences=tuple(
        replace(o, administration=ADMINISTRATION_UNKNOWN, route_state="KNOWN")
        if o.key.item_id == "A" else o for o in inventory.occurrences
    ))
    unknown_frontier = enumerate_frontier(unknown_inventory, policy)
    assert unknown_frontier.unknown
    unknown_op = next(
        x for x in unknown_frontier.unknown if isinstance(x.get("op_id"), str)
    )
    kept_unknown = tuple(
        x for x in unknown_frontier.unknown if x["op_id"] != unknown_op["op_id"]
    )
    forged_unknown = replace(unknown_frontier, unknown=kept_unknown)
    forged_unknown_census = _freeze_packet(forged_unknown)
    with pytest.raises(CensusRefusal, match="UNKNOWN_OPERATION_NEGATIVE_LOSS"):
        verify_frozen_inputs(forged_unknown_census,
                             inventory=unknown_inventory, policy=policy,
                             frontier=forged_unknown)



def test_s1c_a_counter_independent_nonoperation_negatives_preserved(tmp_path):
    """The new cross-owner check must not erase B's separate source negatives.

    An independently declared non-operation hold has no op_id, so it is
    conserved byte-for-byte and does not remove valid RAW I05 results.
    """
    bundle, inventory, policy, frontier, census = _fixture(tmp_path)
    baseline = _run(bundle, inventory, policy, frontier, census)
    extra_unknown = {
        "kind": "EXTERNALLY_DECLARED_SOURCE_ROUTE_UNKNOWN",
        "occurrence": "UNENUMERATED_SOURCE_ITEM_X",
        "reason": "NO_SOURCE_ISSUER_QUALIFICATION",
    }
    extra_excluded = {
        "kind": "EXTERNALLY_DECLARED_SOURCE_EXCLUSION",
        "occurrence": "UNENUMERATED_SOURCE_ITEM_Y",
        "reason": "OUTSIDE_CURRENT_OPERATION_DOMAIN",
    }
    extended = replace(
        frontier,
        unknown=frontier.unknown + (extra_unknown,),
        excluded=frontier.excluded + (extra_excluded,),
    )
    extended_census = _freeze_packet(
        extended, scope_id="A-COUNTER-EXTERNAL-NEGATIVE-PRESERVATION"
    )
    result = _run(bundle, inventory, policy, extended, extended_census)
    assert result["candidate_anti_join"]["no_drop_ok"]
    assert result["operation_anti_join"]["no_drop_ok"]
    assert result["unknown_scope_records"][-1] == extra_unknown
    assert result["excluded_scope_records"][-1] == extra_excluded
    assert result["issued_candidate_count"] == baseline["issued_candidate_count"]
    assert result["native_fact_count"] == baseline["native_fact_count"]
    assert [
        (r["operation_id"], r["fact_refs"]) for r in result["operation_fates"]
    ] == [
        (r["operation_id"], r["fact_refs"]) for r in baseline["operation_fates"]
    ]
