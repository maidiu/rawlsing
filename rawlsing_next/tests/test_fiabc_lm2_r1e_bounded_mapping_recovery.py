from __future__ import annotations

from dataclasses import replace
import importlib.util
import json
from pathlib import Path

import pytest

from rawlsing_next.fiabc_lm2_r1e_wvs7_mapping_authority import (
    AUTHORITY_KIND,
    MAPPING_AUTHORITY_MATERIAL,
    MAPPING_AUTHORITY_REF,
    MAPPING_ROWS,
    NEGATIVE_LIMITS,
    PREDICATE_GRAMMAR_AUTH_REF,
    SOURCE_AUTH_REF,
    TARGET_USE,
    mapping_authority_snapshot,
)
from rawlsing_next.pre553_c11_integrity import C11IntegrityError
from rawlsing_next.pre553_empirical_authority import (
    Pre553AuthorityError,
    require_positive_authority,
)
from rawlsing_next.pre553_physical_decoder import PhysicalVariable
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
    SourceBackedC11FacadeError,
    build_validated_source_backed_c11_release_from_stream,
    raw_physical_value_witness,
)
from rawlsing_next.pre553_independent_parity_oracle import (
    WVS7_FAMILY_COUNTS,
    WVS7_LOCK2_IDENTITY,
    WVS7_ORDERED_CANDIDATE_HASHES,
)
from rawlsing_next.tests.test_pre553_source_backed_c11_facade import _fixture

ROOT = Path(__file__).resolve().parents[2]
MAT = ROOT / "WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py"
spec = importlib.util.spec_from_file_location("fiabc_lm2_r1e_r6s", MAT)
assert spec and spec.loader
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

OLD_SOURCE_AUTHORITY_HASH = "c7336ce479b8625b71e33743a05e43525c387dd50e4be1bb7af313667f9c341f"
OLD_PROJECTION_AUTHORITY_HASH = "01719af5d17d36cdcc998be83908f7d640ce96d49a76edcd722bf755c9065a4a"
OLD_PROJECTION_IDENTITY = "838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d"
LOCK2 = "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
STRUCTURAL = "151907b3163959d0eb5ebb020fa5253d33447362420e465600035744112fe5bc"
PARENTAGE = "5037c55bf1a017112c0fe5f18ca5905696d66dfefcc4d8f47dcb0e7fcb13f37c"
PHYSICAL = "9845c24da0c03adb4dfd65118b7c8c39a60a30337f33cc4177ffc6c848d02390"

def vars3():
    special = tuple({"kind": "discrete", "value": v} for v in (-5, -4, -2, -1))
    return (
        PhysicalVariable(301, "Q291G5", "double", None, {}, special, {}, {}),
        PhysicalVariable(302, "Q291P5", "double", None, {}, special, {}, {}),
        PhysicalVariable(7, "B_COUNTRY", "double", "ISO 3166-1 numeric country code", {}, (), {}, {}),
    )

def fields3():
    return dict(m.build_projection_fields(
        physical_variables=vars3(),
        row_country_values=(231, 704, 840),
        enforce_frozen_dimensions=False,
    ))


def _snapshot_with(snapshot, **semantic_changes):
    semantic_fields = dict(snapshot.semantic_fields)
    semantic_fields.update(semantic_changes)
    return AuthoritySnapshot(
        typed_state=snapshot.typed_state,
        authority_snapshot_refs=snapshot.authority_snapshot_refs,
        dependency_refs=snapshot.dependency_refs,
        producer_replay_locator_or_reference_root=snapshot.producer_replay_locator_or_reference_root,
        **semantic_fields,
    )

def test_r01_authority_ceiling_is_distinct_and_source_authority_is_not_relabeled():
    snap = mapping_authority_snapshot()
    assert snap.authority_kind == "NATIVE_CANONICAL_MAPPING_HARMONIZATION"
    assert MAPPING_AUTHORITY_REF != SOURCE_AUTH_REF
    assert SOURCE_AUTH_REF.authority_content_hash == OLD_SOURCE_AUTHORITY_HASH
    assert SOURCE_AUTH_REF.authority_id == "EE-P2F2-WVS7-SOURCE-SEMANTICS-TOPOLOGY"

def test_r02_and_r18_source_semantics_alone_cannot_authorize_canonical_response():
    fx = _fixture("lm2-r1e-r02-r18")
    p = fx["projection"]
    slot = p.response_slots[0]
    values = tuple(
        replace(v, transform_authority_ref=fx["source_auth"].authority_ref)
        if v.canonical_value is not None else v
        for v in slot.values
    )
    bad = replace(p, response_slots=(replace(slot, values=values), *p.response_slots[1:]))
    stream = ExactPhysicalCellStream(fx["source_sha"], 3, lambda: iter(fx["cells"]))
    with pytest.raises((SourceBackedC11FacadeError, C11IntegrityError, Pre553AuthorityError), match="authority|mapping"):
        build_validated_source_backed_c11_release_from_stream(stream, bad)

def test_r03_exact_derived_mapping_authority_is_accepted_by_source_free_r6s_binding():
    fields = fields3()
    bound = m.bind_exact_projection_fields(fields)
    assert bound.response_slots
    assert all(
        rule.transform_authority_ref == MAPPING_AUTHORITY_REF
        for slot in bound.response_slots
        for rule in slot.values
        if rule.canonical_value is not None
    )

def test_r04_relabel_counterfeit_is_rejected_by_exact_snapshot_binding():
    fields = fields3()
    exact = mapping_authority_snapshot()
    counterfeit = _snapshot_with(exact, authority_kind="SOURCE_SEMANTICS_TOPOLOGY")
    fields["authority_snapshots"] = tuple(
        counterfeit if a.authority_ref == MAPPING_AUTHORITY_REF else a
        for a in fields["authority_snapshots"]
    )
    with pytest.raises(ValueError, match="parent/provenance substitution"):
        m.bind_exact_projection_fields(fields)

def test_r05_canonical_question_mapping_remains_absent():
    fields = fields3()
    assert all(q.canonical_question_ref_or_typed_absence.state == "NOT_AUTHORIZED"
               for q in fields["questions"])

def test_r06_special_states_remain_noncanonical():
    fields = fields3()
    for slot in fields["response_slots"]:
        special = [r for r in slot.values if r.canonical_value is None]
        assert special
        assert all(r.transform_authority_ref is None for r in special)

def test_r07_lexical_token_similarity_mutation_is_rejected():
    fields = fields3()
    slot = fields["response_slots"][0]
    values = list(slot.values)
    i = next(i for i, rule in enumerate(values) if rule.canonical_value == "1")
    values[i] = replace(values[i], canonical_value="01")
    fields["response_slots"] = (replace(slot, values=tuple(values)), *fields["response_slots"][1:])
    with pytest.raises(ValueError, match="program semantic token set drift"):
        m.bind_exact_projection_fields(fields)

def test_r08_cross_source_equivalence_is_explicitly_absent():
    assert "NO_CROSS_SOURCE_EQUIVALENCE" in NEGATIVE_LIMITS
    assert MAPPING_AUTHORITY_MATERIAL["cross_source_relation"] == "NONE_AUTHORIZED"
    assert MAPPING_AUTHORITY_MATERIAL["source"]["source_sha256"] == m.SOURCE_SHA256

def test_r09_exact_parent_and_provenance_mutation_is_rejected():
    fields = fields3()
    exact = mapping_authority_snapshot()
    assert {x["authority_id"] for x in exact.parent_authority_refs} == {
        SOURCE_AUTH_REF.authority_id,
        PREDICATE_GRAMMAR_AUTH_REF.authority_id,
    }
    mutated = _snapshot_with(exact, parent_authority_refs=(SOURCE_AUTH_REF.as_dict(),))
    fields["authority_snapshots"] = tuple(
        mutated if a.authority_ref == MAPPING_AUTHORITY_REF else a
        for a in fields["authority_snapshots"]
    )
    with pytest.raises(ValueError, match="parent/provenance substitution"):
        m.bind_exact_projection_fields(fields)

def test_r10_target_use_scope_escape_is_rejected():
    snap = mapping_authority_snapshot()
    require_positive_authority(
        snap,
        authority_kind=AUTHORITY_KIND,
        target_use_ref=TARGET_USE,
    )
    with pytest.raises(Pre553AuthorityError, match="target_use_refs"):
        require_positive_authority(
            snap,
            authority_kind=AUTHORITY_KIND,
            target_use_ref="SOME_OTHER_USE",
        )

def test_r11_lock2_and_complete_46_candidate_frontier_are_conserved():
    assert m.LOCK2 == LOCK2 == WVS7_LOCK2_IDENTITY
    assert len(WVS7_ORDERED_CANDIDATE_HASHES) == 46
    assert len(set(WVS7_ORDERED_CANDIDATE_HASHES)) == 46
    assert WVS7_FAMILY_COUNTS == {
        "UNARY_SOCIAL_FORK": 10,
        "PAIR_RESPONSE_COTRAVEL": 1,
        "BRANCH_CONDITIONED_DISTRIBUTION": 10,
        "BOUNDED_K_WAY_RESPONSE_CONFIGURATION": 25,
    }

def test_r12_physical_expectation_conserved():
    doc = json.loads((ROOT / "WORKER_RETURNS/FIABC-LM2/04_WVS7_CANONICAL_PHYSICAL_EXPECTATION.json").read_text())
    assert doc["expectation_identity"] == PHYSICAL

def test_r13_structural_preimage_and_parentage_conserved():
    doc = json.loads((ROOT / "WORKER_RETURNS/FIABC-LM2/02_WVS7_STRUCTURAL_PARENTAGE_RECEIPT.json").read_text())
    assert doc["bundle_identity"] == PARENTAGE
    assert doc["derivative_receipt"]["derivative"]["identity"] == STRUCTURAL

def test_r14_semantic_identity_changes_only_downstream_of_mapping_ref():
    assert m.PROJECTION_AUTH_REF.authority_content_hash != OLD_PROJECTION_AUTHORITY_HASH
    assert m.PROJECTION_IDENTITY_REF.content_hash != OLD_PROJECTION_IDENTITY
    assert m.LOCK2 == LOCK2

def test_r17_native_only_mutation_cannot_preserve_frozen_string_workload():
    fields = fields3()
    native_only_slots = []
    for slot in fields["response_slots"]:
        native_only_values = tuple(
            replace(rule, canonical_value=None, transform_authority_ref=None)
            if rule.canonical_value is not None else rule
            for rule in slot.values
        )
        native_only_slots.append(replace(slot, values=native_only_values))
    fields["response_slots"] = tuple(native_only_slots)
    with pytest.raises(ValueError, match="program semantic token set drift|substantive mapping authority"):
        m.bind_exact_projection_fields(fields)

    witness = raw_physical_value_witness(1)
    assert isinstance(witness, dict)
    assert witness != "1"
    assert witness["$raw_physical_value"]["token"]["t"] == "int"
    assert witness["$raw_physical_value"]["token"]["v"] == "1"

def test_mapping_rows_are_exact_ten_pair_graph_and_no_special_code_is_present():
    assert len(MAPPING_ROWS) == 10
    assert {row[0] for row in MAPPING_ROWS} == {"Q291G5", "Q291P5"}
    assert {row[1] for row in MAPPING_ROWS} == {1, 2, 3, 4, 5}
    assert {row[4] for row in MAPPING_ROWS} == {"1", "2", "3", "4", "5"}
    assert not ({-5, -4, -2, -1} & {row[1] for row in MAPPING_ROWS})
