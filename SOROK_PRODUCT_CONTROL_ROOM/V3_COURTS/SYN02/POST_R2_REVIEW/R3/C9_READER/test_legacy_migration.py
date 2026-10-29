from dataclasses import asdict
import hashlib
import json
import pytest
from actor_reader import ReaderHeld
from legacy_migration import LegacyActorSourceV1, LegacyFactBindingV1, migrate_legacy_actor


def source(data, bindings=()):
    text = json.dumps(data, sort_keys=True)
    return LegacyActorSourceV1("A", "historic-cut", text, hashlib.sha256(text.encode()).hexdigest(), tuple(bindings))


def test_exact_material_time_care_event_values_survive_without_clamping_or_mutation():
    data = {"year": 2004, "capacity": {"money": 37}, "events_this_year": [
        {"event_id": "care-1", "care_supplied": True, "interval_end": 42}]}
    bindings = [LegacyFactBindingV1(path, "TEST_ONLY_RECEIPT") for path in [
        ("year",), ("capacity", "money"), ("events_this_year", 0, "event_id"),
        ("events_this_year", 0, "care_supplied"), ("events_this_year", 0, "interval_end")]]
    original = source(data, bindings)
    record = migrate_legacy_actor(original)
    assert [json.loads(row.value_json) for row in record.retained_candidates] == [2004, 37, "care-1", True, 42]
    assert all(row.source_sha256 == original.source_sha256 for row in record.retained_candidates)
    assert original == source(data, bindings)
    assert record.status == "PARTIAL_HELD_SOURCE_OWNER_ADMISSION"


def test_default_50_is_not_imported_without_specific_evidence_and_real_50_is_not_clamped():
    original = source({"capacity": {"money": 50, "health": 50}})
    assert migrate_legacy_actor(original).retained_candidates == ()
    bound = source({"capacity": {"money": 50}}, [LegacyFactBindingV1(("capacity", "money"), "TEST_ONLY_MONEY_OBSERVATION")])
    assert migrate_legacy_actor(bound).retained_candidates[0].value_json == "50"


def test_absent_observation_stays_unknown_without_hopeful_or_zero_default():
    record = migrate_legacy_actor(source({"expectation_baseline": {"care": "hopeful"}},
        [LegacyFactBindingV1(("capacity", "social_support"), "TEST_ONLY_PARENT_CARE"),
         LegacyFactBindingV1(("reproduction_constraints", "caregiving_load"), "TEST_ONLY_CARE")]))
    assert not record.retained_candidates
    assert {row.reason for row in record.unknowns} == {"FIELD_NOT_ADMITTED_TO_MATERIAL_CANDIDATE", "MISSING_SOURCE_VALUE"}
    assert record.quarantine[0].category == "EXPECTATION_DEFAULT_RULE_HELD"


def test_age_narrator_pressure_memory_and_placeholders_cannot_enter_actor_candidates():
    data = {"age": 7, "child_model": {"type": "x"}, "rendered_output": "Narrator invented memory",
            "pressure_flow_memory": {"secret": "analyst-only"}, "cracks": [{"placeholder": 1}],
            "registers": {"style": 50}, "metabolic_style": "changed"}
    record = migrate_legacy_actor(source(data, [LegacyFactBindingV1((key,), "TEST_ONLY") for key in data]))
    assert record.retained_candidates == ()
    assert all(row.reason == "FIELD_NOT_ADMITTED_TO_MATERIAL_CANDIDATE" for row in record.unknowns)
    text = json.dumps(asdict(record))
    assert "Narrator invented memory" not in text and "analyst-only" not in text
    assert "ANALYST_TRACE_NOT_ACTOR_MEMORY" in text


def test_world_institution_values_remain_world_owned_not_actor_scalar_facts():
    record = migrate_legacy_actor(source({"collective_infrastructure": 91, "field": {"housing": "secure"}},
        [LegacyFactBindingV1(("collective_infrastructure",), "TEST_ONLY")]))
    assert not record.retained_candidates
    assert all(row.category == "WORLD_OWNER_ADMISSION_HELD" for row in record.quarantine)


def test_repeated_migration_is_idempotent_and_has_no_storage_api():
    binding = LegacyFactBindingV1(("year",), "TEST_ONLY")
    original = source({"year": 2001}, [binding])
    observed = migrate_legacy_actor(original)
    # Independent reconstruction must preserve the exact bound value/source,
    # not merely compare an expression with itself.
    replay_source = source(dict(year=2001), [LegacyFactBindingV1(("year",), "TEST_ONLY")])
    replayed = migrate_legacy_actor(replay_source)
    assert observed.retained_candidates[0].value_json == "2001"
    assert observed.retained_candidates[0].source_sha256 == original.source_sha256
    assert replayed == observed
    assert observed.status == "PARTIAL_HELD_SOURCE_OWNER_ADMISSION"
    assert not hasattr(observed, "write") and not hasattr(observed, "commit")
    # Causal/source severance: changed admitted scalar must change exact output;
    # absence of a qualified binding must not manufacture an actor fact.
    changed = migrate_legacy_actor(source({"year": 2002}, [binding]))
    assert changed.retained_candidates[0].value_json == "2002"
    assert changed.retained_candidates != observed.retained_candidates
    unbound = migrate_legacy_actor(source({"year": 2001}))
    assert unbound.retained_candidates == ()


def test_source_tamper_refuses_and_no_native_proof_is_manufactured():
    from dataclasses import replace
    original = source({"year": 2000})
    with pytest.raises(ReaderHeld, match="LEGACY_SOURCE_HASH_MISMATCH"):
        migrate_legacy_actor(replace(original, source_json='{"year":2001}'))
    with pytest.raises(ReaderHeld, match="LEGACY_BINDING_SCOPE_HELD"):
        migrate_legacy_actor(source({"year": 2000}, [LegacyFactBindingV1(("year",), "fake-native", "SOURCE_QUALIFIED")]))


def test_container_binding_does_not_smuggle_unqualified_nested_defaults():
    record = migrate_legacy_actor(source({"reproduction_constraints": {"debt": 10, "legal_status": 100}},
        [LegacyFactBindingV1(("reproduction_constraints",), "TEST_ONLY")]))
    assert not record.retained_candidates
    assert record.unknowns[0].reason == "EXACT_SCALAR_BINDING_REQUIRED"


def test_classification_fields_match_the_pinned_actual_backbone_source():
    import ast
    from pathlib import Path
    from legacy_migration import WORLD_FIELDS, NARRATOR_FIELDS, ANALYST_FIELDS, PLACEHOLDER_FIELDS, NONCAUSAL_FIELDS, OBSERVABLE_FIELDS
    path = Path('/Users/matthewsmith/Desktop/Rawlsing/Rawlsing_code_bundle_staging/v3/core/state.py')
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2'
    node = next(row for row in ast.parse(raw).body if isinstance(row, ast.ClassDef) and row.name == 'BackboneState')
    fields = {row.target.id for row in node.body if isinstance(row, ast.AnnAssign) and isinstance(row.target, ast.Name)}
    assert set().union(WORLD_FIELDS, NARRATOR_FIELDS, ANALYST_FIELDS, PLACEHOLDER_FIELDS, NONCAUSAL_FIELDS, OBSERVABLE_FIELDS) <= fields
