from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from rawlsing_next._pre553_query_predicate import _build_release_index, _eval_predicate
from rawlsing_next.pre553_discovery_exact import _combine_predicates
from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    authority_ref,
    exact_ref,
    make_empirical_predicate,
    semantic_hash,
)
from rawlsing_next.pre553_runtime_authority import (
    ACTIVE_POSITIVE_BINDING,
    CONCRETE_BINDING_SCHEMA,
    Pre553RuntimeAuthoritySet,
)
from rawlsing_next.pre553_runtime_composition import compose_predicates_runtime
from rawlsing_next.pre553_runtime_context import (
    bind_runtime,
    execute_empirical_query_runtime,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _build_source,
    _h,
    _cell_map,
    _query,
    _query_authority,
    _ref,
    _registry,
    _response_leaf,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).resolve().parent / "fixtures"

R4_FILES = {
    "dialect": FIXTURES / "ee_p2r6a_r4a_01_dialect.json",
    "respondent": FIXTURES / "ee_p2r6a_r4a_02_respondent.json",
    "mixed": FIXTURES / "ee_p2r6a_r4a_03_mixed.json",
    "derived": FIXTURES / "ee_p2r6a_r4a_04_derived.json",
    "successor": FIXTURES / "ee_p2r6a_r4a_05_successor.json",
}
R5_FILES = {
    "realization": ROOT / "WORKER_RETURNS/EE-P2R5A/02_RELEASE_REALIZATION_RELATION_AUTHORITY.json",
    "schema": ROOT / "WORKER_RETURNS/EE-P2R5A/03_CONCRETE_REALIZATION_BINDING_SCHEMA.json",
    "clause": ROOT / "WORKER_RETURNS/EE-P2R5A/04_R4A_RELEASE_PRECONDITION_SUCCESSOR_CLAUSE.json",
}

ADOPTED = (
    "3ef0317887f6910838636d3816237a81d5a56b38e07595c8cc1f7c5e7f1fae74",
    "0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55",
    "225e4b80390500451834ea784d955465eb9f145a4cd1f798dace51f3a6d3baa4",
    "b87c387f9d222c83106c8d47d369af44f5c5368b274fd85e7a08b12c20d49cae",
    "9da19997168612891f59012e69674bac59fbee417d9b30b003171f3074168bf5",
    "a1da1ea78dce423ea3520726d0477b058057482d67964056743e08389d9045a0",
    "d8e3d9a19fa36599e8cd6b1bc8e82092c425fd9119be478f7ba79335d05a1b3e",
    "d9aa476c493810651baefa8bad23990d9dd80812a48670ad2052353f0e7d52a2",
)


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def authority_data():
    return {
        **{name: _load(path) for name, path in R4_FILES.items()},
        **{name: _load(path) for name, path in R5_FILES.items()},
    }


def _runtime(data, *, bindings=(), include_r4=True, include_r5=True):
    kwargs = {
        "adopted_authority_hashes": ADOPTED,
        "realization_bindings": bindings,
    }
    if include_r4:
        kwargs.update({
            "predicate_dialect_matrices": (data["dialect"],),
            "respondent_compatibility_authorities": (data["respondent"],),
            "mixed_composition_authorities": (data["mixed"],),
            "derived_predicate_contracts": (data["derived"],),
            "public_predicate_successor_authorities": (data["successor"],),
        })
    if include_r5:
        kwargs.update({
            "release_realization_authorities": (data["realization"],),
            "realization_binding_schemas": (data["schema"],),
            "release_precondition_clauses": (data["clause"],),
        })
    return Pre553RuntimeAuthoritySet(**kwargs)


def _fixture_source(data):
    q = data["dialect"]["exact_question_value_bindings"]
    qrefs = {
        "X": ExactRef("QUESTION_NATIVE", "urn:test:r6a:question:x", q["q310"]["question_content_hash"]),
        "Y": ExactRef("QUESTION_NATIVE", "urn:test:r6a:question:y", q["q311"]["question_content_hash"]),
    }
    return _build_source(
        "r6a-runtime",
        [
            {"id": "R1", "responses": {"X": 1, "Y": 1}},
            {"id": "R2", "responses": {"X": 2, "Y": 0}},
            {"id": "R3", "responses": {"Y": 0}},
        ],
        question_refs_override=qrefs,
        source_hash_override=data["realization"]["identity_material"]["source_sha256"],
    )


def _valid_binding(data, source, *, marker=None):
    schema = data["schema"]
    material = copy.deepcopy(schema["future_binding_required_fields"])
    release = source["repo"].resolve_release_exact(source["release_ref"])
    material["relation_authority_ref"] = copy.deepcopy(data["realization"]["authority_ref"])
    material["runtime_i02_release_ref"] = release.release_ref.as_dict()
    material["runtime_candidate_projection_hash"] = release.replay_manifest.semantic_projection_hash
    material["runtime_replay_manifest_ref"] = release.replay_manifest.ref.as_dict()
    material["runtime_m01_m18_coverage"] = {
        key: list(value) for key, value in release.m01_m18_coverage.items()
    }
    material["c11_repository_exact_resolution_receipt"] = release.release_ref.as_dict()
    if marker is not None:
        material["fixture_binding_marker"] = marker
    digest = semantic_hash(material)
    return {
        "schema": CONCRETE_BINDING_SCHEMA,
        "typed_state": ACTIVE_POSITIVE_BINDING,
        "binding_ref": ExactRef(
            "ReleaseRealizationBinding@1.0.0",
            f"urn:test:r6a:binding:{digest}",
            digest,
        ).as_dict(),
        "identity_material": material,
    }


def _selector_leaf(data, source, native="1", operation="survey_response_EQ"):
    q = data["dialect"]["exact_question_value_bindings"]["q310"]
    return {
        "op": "LEAF",
        "leaf_type": "SURVEY_RESPONSE_EVENT",
        "operation": operation,
        "question_ref": source["qrefs"]["X"],
        "response_value_ref": ExactRef(
            "RESPONSE_VALUE_STATE",
            f"urn:test:r6a:value:{native}",
            q["values"][native],
        ),
        "source_native_value": native,
        "release_ref": exact_ref(data["dialect"]["exact_scope"]["release_ref"]),
    }


def _eval_selector(data, source, runtime, leaf, respondent_id):
    index = _build_release_index(
        source["repo"].resolve_release_exact(source["release_ref"]),
        source["universe"].ref,
    )
    index.runtime_authorities = runtime
    index.runtime_repository = source["repo"]
    child_ref = authority_ref(
        data["mixed"]["identity_material"]["allowed_input_grammar_refs"][1]
    )
    index.runtime_predicate_grammar_authority_ref = child_ref
    used, used_auth = [], []
    return _eval_predicate(
        leaf,
        respondent=source["respondents"][respondent_id],
        index=index,
        registry=_registry(source),
        used=used,
        used_auth=used_auth,
    )


def _fixture_predicate(*, ast, grammar_ref, binding, scope_refs, tag):
    return make_empirical_predicate(
        predicate_ast=ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(grammar_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"r6a-{tag}"),
        grammar_authority_ref=grammar_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=(),
        scope_refs=scope_refs,
        same_respondent_binding_semantics=binding,
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", f"r6a-{tag}"),),
    )


def _mixed_inputs(data, source):
    mixed = data["mixed"]["identity_material"]
    compat = data["respondent"]["identity_material"]
    parent_grammar, child_grammar = tuple(
        authority_ref(x) for x in mixed["allowed_input_grammar_refs"]
    )
    base_scope = exact_ref(compat["exact_scope"]["base_release_ref"])
    frozen_scope = exact_ref(compat["exact_scope"]["release_ref"])
    parent = _fixture_predicate(
        ast={"op": "LEAF", "leaf_type": "DERIVED_BRANCH_COHORT", "fixture": "parent"},
        grammar_ref=parent_grammar,
        binding=compat["parent_binding"],
        scope_refs=(base_scope,),
        tag="parent",
    )
    child = _fixture_predicate(
        ast=_selector_leaf(data, source),
        grammar_ref=child_grammar,
        binding=compat["child_binding"],
        scope_refs=(frozen_scope,),
        tag="child",
    )
    return parent, child


def test_banked_adopted_authority_graph_loads_exactly(authority_data):
    runtime = _runtime(authority_data)
    assert isinstance(runtime, Pre553RuntimeAuthoritySet)
    assert authority_data["respondent"]["authority_content_hash"] == ADOPTED[0]
    assert authority_data["mixed"]["authority_content_hash"] == ADOPTED[1]
    assert authority_data["derived"]["contract_content_hash"] == ADOPTED[2]
    assert authority_data["successor"]["authority_candidate_content_hash"] == ADOPTED[3]
    assert authority_data["realization"]["authority_ref"]["content_hash"] == ADOPTED[4]
    assert authority_data["schema"]["schema_ref"]["content_hash"] == ADOPTED[5]
    assert authority_data["clause"]["clause_ref"]["content_hash"] == ADOPTED[6]
    assert authority_data["realization"]["aggregate_candidate_ref"]["content_hash"] == ADOPTED[7]


def test_legacy_same_grammar_same_binding_composition_is_exactly_unchanged(authority_data):
    source = _fixture_source(authority_data)
    parent, _ = _mixed_inputs(authority_data, source)
    sibling = _fixture_predicate(
        ast={"op": "LEAF", "leaf_type": "DERIVED_BRANCH_COHORT", "fixture": "sibling"},
        grammar_ref=parent.grammar_authority_ref,
        binding=parent.same_respondent_binding_semantics,
        scope_refs=tuple(exact_ref(x) for x in parent.scope_refs),
        tag="sibling",
    )
    tag = {"fixture": "legacy-equality"}
    old = _combine_predicates((parent, sibling), op="AND", tag_material=tag)
    new = compose_predicates_runtime((parent, sibling), op="AND", tag_material=tag)
    assert new.ref == old.ref
    assert new.semantic_projection() == old.semantic_projection()


def test_legacy_response_leaf_evaluator_remains_unchanged(authority_data):
    source = _fixture_source(authority_data)
    qauth = _query_authority("r6a-legacy")
    leaf = _response_leaf(source, qauth, "X", 1)
    index = _build_release_index(
        source["repo"].resolve_release_exact(source["release_ref"]),
        source["universe"].ref,
    )
    assert _eval_predicate(
        leaf,
        respondent=source["respondents"]["R1"],
        index=index,
        registry=_registry(source),
        used=[],
        used_auth=[],
    ) is True
    assert _eval_predicate(
        leaf,
        respondent=source["respondents"]["R2"],
        index=index,
        registry=_registry(source),
        used=[],
        used_auth=[],
    ) is False


def test_child_dialect_fails_without_exact_adopted_interpreter(authority_data):
    source = _fixture_source(authority_data)
    leaf = _selector_leaf(authority_data, source)
    index = _build_release_index(
        source["repo"].resolve_release_exact(source["release_ref"]),
        source["universe"].ref,
    )
    with pytest.raises(Pre553AuthorityError):
        _eval_predicate(
            leaf,
            respondent=source["respondents"]["R1"],
            index=index,
            registry=_registry(source),
            used=[],
            used_auth=[],
        )


def test_unrecognized_child_dialect_fails_closed(authority_data):
    source = _fixture_source(authority_data)
    binding = _valid_binding(authority_data, source)
    runtime = _runtime(authority_data, bindings=(binding,))
    leaf = _selector_leaf(authority_data, source, operation="survey_response_UNKNOWN")
    with pytest.raises(Pre553AuthorityError):
        _eval_selector(authority_data, source, runtime, leaf, "R1")


def test_adopted_child_dialect_is_exact_native_equality_and_missing_false(authority_data):
    source = _fixture_source(authority_data)
    binding = _valid_binding(authority_data, source)
    runtime = _runtime(authority_data, bindings=(binding,))
    leaf = _selector_leaf(authority_data, source, native="1")
    before = copy.deepcopy(leaf)
    assert _eval_selector(authority_data, source, runtime, leaf, "R1") is True
    assert _eval_selector(authority_data, source, runtime, leaf, "R2") is False
    assert _eval_selector(authority_data, source, runtime, leaf, "R3") is False
    assert leaf == before


def test_adopted_child_dialect_executes_through_public_i03_runtime_entrypoint(authority_data):
    source = _fixture_source(authority_data)
    binding = _valid_binding(authority_data, source)
    runtime = _runtime(authority_data, bindings=(binding,))
    qauth = _query_authority("r6a-runtime-i03")
    child_grammar = authority_ref(
        authority_data["mixed"]["identity_material"]["allowed_input_grammar_refs"][1]
    )
    frozen_scope = exact_ref(authority_data["dialect"]["exact_scope"]["release_ref"])
    predicate = _fixture_predicate(
        ast=_selector_leaf(authority_data, source, native="1"),
        grammar_ref=child_grammar,
        binding=authority_data["respondent"]["identity_material"]["child_binding"],
        scope_refs=(frozen_scope,),
        tag="runtime-i03-child",
    )
    query = _query(source, qauth, predicate, ("Y",), tag="runtime-i03-child")
    result = execute_empirical_query_runtime(
        runtime_authorities=runtime,
        repository=source["repo"],
        query=query,
        predicate=predicate,
        authority_registry=_registry(source, qauth),
        release_refs=(source["release_ref"],),
    )
    fact = result.facts[0]
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 1
    assert _cell_map(fact)["1"]["raw_numerator_support"] == 1


def test_i05_existing_combiner_dispatches_mixed_only_under_bound_runtime(authority_data):
    source = _fixture_source(authority_data)
    parent, child = _mixed_inputs(authority_data, source)
    runtime = _runtime(authority_data)
    with bind_runtime(runtime):
        derived = _combine_predicates(
            (parent, child),
            op="AND",
            tag_material={"case": "i05-production-dispatch"},
        )
    assert authority_ref(derived.grammar_authority_ref) == authority_ref(
        authority_data["mixed"]["candidate_authority_ref"]
    )


def test_mixed_successor_dispatches_nested_child_dialect_by_exact_authority_chain(authority_data):
    source = _fixture_source(authority_data)
    runtime = _runtime(authority_data)
    successor_ref = authority_ref(authority_data["mixed"]["candidate_authority_ref"])
    leaf = _selector_leaf(authority_data, source)
    contract = runtime.resolve_predicate_dialect(successor_ref, leaf)
    child_ref = authority_ref(
        authority_data["mixed"]["identity_material"]["allowed_input_grammar_refs"][1]
    )
    assert contract.grammar_ref == child_ref


def test_zero_realization_bindings_fails_closed_before_selector(authority_data):
    source = _fixture_source(authority_data)
    runtime = _runtime(authority_data, bindings=())
    with pytest.raises(Pre553AuthorityError, match="zero active positive"):
        _eval_selector(
            authority_data, source, runtime, _selector_leaf(authority_data, source), "R1"
        )


def test_multiple_realization_bindings_fails_closed(authority_data):
    source = _fixture_source(authority_data)
    binding = _valid_binding(authority_data, source)
    runtime = _runtime(authority_data, bindings=(binding, copy.deepcopy(binding)))
    scope = exact_ref(authority_data["dialect"]["exact_scope"]["release_ref"])
    with pytest.raises(Pre553AuthorityError, match="multiple active positive"):
        runtime.require_realized_release(
            scope,
            repository=source["repo"],
            runtime_release_ref=source["release_ref"],
        )


def test_source_release_and_authority_mismatch_fail_closed(authority_data):
    source = _fixture_source(authority_data)
    scope = exact_ref(authority_data["dialect"]["exact_scope"]["release_ref"])

    bad_source = _valid_binding(authority_data, source)
    bad_source["identity_material"]["source_artifact_sha256"] = "0" * 64
    digest = semantic_hash(bad_source["identity_material"])
    bad_source["binding_ref"] = ExactRef(
        "ReleaseRealizationBinding@1.0.0", f"urn:test:r6a:bad-source:{digest}", digest
    ).as_dict()
    with pytest.raises(Pre553AuthorityError):
        _runtime(authority_data, bindings=(bad_source,)).require_realized_release(
            scope, repository=source["repo"], runtime_release_ref=source["release_ref"]
        )

    wrong_scope = ExactRef("C11LogicalRelease", "urn:test:r6a:wrong-scope", _h("wrong-scope"))
    with pytest.raises(Pre553AuthorityError):
        _runtime(authority_data, bindings=(_valid_binding(authority_data, source),)).require_realized_release(
            wrong_scope, repository=source["repo"], runtime_release_ref=source["release_ref"]
        )

    bad_authority = _valid_binding(authority_data, source)
    bad_authority["identity_material"]["relation_authority_ref"] = ExactRef(
        "ReleaseRealizationAuthorityCandidate@1.0.0",
        "urn:test:r6a:wrong-authority",
        _h("wrong-authority"),
    ).as_dict()
    digest = semantic_hash(bad_authority["identity_material"])
    bad_authority["binding_ref"] = ExactRef(
        "ReleaseRealizationBinding@1.0.0", f"urn:test:r6a:bad-authority:{digest}", digest
    ).as_dict()
    with pytest.raises(Pre553AuthorityError):
        _runtime(authority_data, bindings=(bad_authority,)).require_realized_release(
            scope, repository=source["repo"], runtime_release_ref=source["release_ref"]
        )


def test_absent_repository_target_fails_closed(authority_data):
    source = _fixture_source(authority_data)
    binding = _valid_binding(authority_data, source)
    missing = ExactRef("C11LogicalRelease", "urn:test:r6a:missing-runtime", _h("missing-runtime"))
    binding["identity_material"]["runtime_i02_release_ref"] = missing.as_dict()
    binding["identity_material"]["c11_repository_exact_resolution_receipt"] = missing.as_dict()
    digest = semantic_hash(binding["identity_material"])
    binding["binding_ref"] = ExactRef(
        "ReleaseRealizationBinding@1.0.0", f"urn:test:r6a:missing:{digest}", digest
    ).as_dict()
    runtime = _runtime(authority_data, bindings=(binding,))
    scope = exact_ref(authority_data["dialect"]["exact_scope"]["release_ref"])
    with pytest.raises(Pre553AuthorityError, match="absent from exact C11Repository"):
        runtime.require_realized_release(
            scope, repository=source["repo"], runtime_release_ref=missing
        )


def test_one_valid_fixture_binding_to_sealed_i02_release_succeeds(authority_data):
    source = _fixture_source(authority_data)
    binding = _valid_binding(authority_data, source)
    runtime = _runtime(authority_data, bindings=(binding,))
    scope = exact_ref(authority_data["dialect"]["exact_scope"]["release_ref"])
    release = runtime.require_realized_release(
        scope, repository=source["repo"], runtime_release_ref=source["release_ref"]
    )
    assert release.release_ref == source["release_ref"]
    assert release.source_artifact_ref.content_hash == authority_data["realization"]["identity_material"]["source_sha256"]
    assert set(release.m01_m18_coverage) == {f"M{i:02d}" for i in range(1, 19)}


def test_absent_and_wrong_mixed_authority_fail_closed(authority_data):
    source = _fixture_source(authority_data)
    parent, child = _mixed_inputs(authority_data, source)
    with pytest.raises(Exception):
        compose_predicates_runtime((parent, child), op="AND", tag_material={"case": "absent"})

    fake_grammar = AuthorityRef(
        "urn:test:r6a:wrong-parent",
        "1.0.0",
        _h("wrong-parent-grammar"),
    )
    wrong_parent = _fixture_predicate(
        ast=parent.predicate_ast,
        grammar_ref=fake_grammar,
        binding=parent.same_respondent_binding_semantics,
        scope_refs=tuple(exact_ref(x) for x in parent.scope_refs),
        tag="wrong-parent",
    )
    with pytest.raises(Exception):
        compose_predicates_runtime(
            (wrong_parent, child),
            op="AND",
            tag_material={"case": "wrong"},
            runtime_authorities=_runtime(authority_data),
        )


def test_authorized_mixed_and_uses_explicit_successor_authority(authority_data):
    source = _fixture_source(authority_data)
    runtime = _runtime(authority_data)
    parent, child = _mixed_inputs(authority_data, source)
    parent_ref, child_ref = parent.ref, child.ref
    parent_projection = copy.deepcopy(parent.semantic_projection())
    child_projection = copy.deepcopy(child.semantic_projection())

    derived = compose_predicates_runtime(
        (parent, child),
        op="AND",
        tag_material={"case": "authorized-mixed"},
        runtime_authorities=runtime,
    )
    reverse = compose_predicates_runtime(
        (child, parent),
        op="AND",
        tag_material={"case": "authorized-mixed"},
        runtime_authorities=runtime,
    )
    successor_ref = authority_ref(authority_data["mixed"]["candidate_authority_ref"])
    derived_binding = authority_data["derived"]["identity_material"]["deterministic_construction"][
        "same_respondent_binding_semantics"
    ]
    assert authority_ref(derived.grammar_authority_ref) == successor_ref
    assert derived.same_respondent_binding_semantics == derived_binding
    assert successor_ref in tuple(authority_ref(x) for x in derived.authority_snapshot_refs)
    assert set(exact_ref(x) for x in derived.dependency_refs) == {parent.ref, child.ref}
    assert derived.ref == reverse.ref
    assert parent.ref == parent_ref and child.ref == child_ref
    assert parent.semantic_projection() == parent_projection
    assert child.semantic_projection() == child_projection


@pytest.mark.parametrize("op", ["OR", "NOT"])
def test_mixed_or_and_not_fail_closed(authority_data, op):
    source = _fixture_source(authority_data)
    parent, child = _mixed_inputs(authority_data, source)
    with pytest.raises(Exception):
        compose_predicates_runtime(
            (parent, child),
            op=op,
            tag_material={"case": op},
            runtime_authorities=_runtime(authority_data),
        )


def test_frozen_selector_identities_are_not_reminted(authority_data):
    matrix_hashes = tuple(authority_data["dialect"]["exact_scope"]["selector_predicate_hashes"])
    successor_hashes = tuple(
        authority_data["successor"]["identity_material"]["exact_frozen_inputs"]["f02"][
            "selector_hashes"
        ]
    )
    assert matrix_hashes == successor_hashes
    before = json.dumps(authority_data["dialect"], sort_keys=True, separators=(",", ":"))
    source = _fixture_source(authority_data)
    parent, child = _mixed_inputs(authority_data, source)
    child_ref = child.ref
    compose_predicates_runtime(
        (parent, child),
        op="AND",
        tag_material={"case": "identity-preservation"},
        runtime_authorities=_runtime(authority_data),
    )
    after = json.dumps(authority_data["dialect"], sort_keys=True, separators=(",", ":"))
    assert before == after
    assert child.ref == child_ref
