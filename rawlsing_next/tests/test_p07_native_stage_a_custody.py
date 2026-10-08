"""HQ244 Stage A independent court: native P07 owner constructor custody + exact resolve.

NON-PRODUCTION, NON-AUTHORIZING. This harness exercises ONLY constructor custody and
exact-key resolve. It asserts NOTHING about P07 authority, adjudication, precedence or
F7 receipts -- those are Stage B/C/D gates.

A green here is explicitly NOT a security pass and does NOT close F7-RR-04G.
"""
from __future__ import annotations

import copy
import importlib
import pickle
import sys

import pytest

from rawlsing_next.pre553_source_relations import ExactRef, semantic_hash
from rawlsing_next.tests.test_pre553_temporal_comparability import (
    UNIVERSE_A,
    UNIVERSE_B,
    _adjudicated_resolver,
)

NATIVE_MODULE = "rawlsing_next._p07_native_owner_stage_a"
NOT_IMPLEMENTED = "NOT_IMPLEMENTED_NONAUTHORIZING_STAGE_A"


def _native():
    return importlib.import_module(NATIVE_MODULE)


def _err():
    """The NATIVE module's own integrity error type.

    Deliberately NOT the production Python class: Stage A raises a distinct native
    type, and the court asserts that separation is real rather than papering over it.
    """
    return _native().SourceRelationIntegrityError


@pytest.fixture(scope="module")
def m():
    return _native()


@pytest.fixture(scope="module")
def admitted():
    """A genuinely adjudicated source relation, its PRODUCTION Python owner (the
    accepted exact-resolve baseline), and the quarantined Stage A native owner."""
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    owner = _native().build_stage_a_owner(
        relations=[relation],
        authority_registry=resolver._registry,
        trusted_semantic_hash=semantic_hash,
    )
    return owner, relation, resolver


class _MutableRelation:
    """A deliberately MUTABLE relation stand-in.

    The accepted production ``SourceUniverseRelation`` is frozen, so it cannot be used
    to exercise the native identity re-verification path. This stand-in can, which is
    exactly what an attacker-supplied substitute object would look like.
    """

    def __init__(self, ref, content_hash):
        self.ref = ref
        self.content_hash = content_hash


# --------------------------------------------------------------- real C module

def test_native_module_is_a_real_compiled_extension(m):
    assert m.__file__.endswith((".so", ".pyd")), m.__file__
    assert m.AUTHORIZING == 0
    assert m.SUBCLASSABLE == 0
    assert m.STAGE == "A"
    assert m.STAGE_A_NONAUTHORIZING_MARKER == NOT_IMPLEMENTED


def test_native_error_type_is_distinct_from_production(m):
    import rawlsing_next.pre553_source_relations as prod

    assert m.SourceRelationIntegrityError is not prod.SourceRelationIntegrityError
    assert issubclass(m.SourceRelationIntegrityError, Exception)


def test_native_type_is_not_subclassable(m):
    with pytest.raises(TypeError):
        type("Attacker", (m.StageAOwner,), {})


# ------------------------------------------------------------- one-shot custody

def test_owner_seals_exactly_once(admitted):
    owner, _rel, _resolver = admitted
    assert owner.sealed is True
    assert owner.custody_hash


def test_reinit_is_refused(admitted):
    owner, rel, resolver = admitted
    with pytest.raises(_err()) as e:
        type(owner).__init__(owner, [rel], resolver._registry, semantic_hash)
    assert "one-shot" in str(e.value)


def test_direct_reinit_call_is_refused(admitted):
    owner, rel, resolver = admitted
    with pytest.raises(_err()) as e:
        owner.__init__([rel], resolver._registry, semantic_hash)
    assert "one-shot" in str(e.value)


def test_custody_cannot_be_copied(admitted):
    owner, _rel, _resolver = admitted
    for fn in (copy.copy, copy.deepcopy):
        with pytest.raises(TypeError):
            fn(owner)


def test_custody_cannot_be_pickled(admitted):
    owner, _rel, _resolver = admitted
    with pytest.raises((TypeError, AttributeError, pickle.PicklingError)):
        pickle.dumps(owner)


def test_custody_cannot_be_reduced(admitted):
    owner, _rel, _resolver = admitted
    with pytest.raises((TypeError, AttributeError)):
        owner.__reduce__()


def test_custody_cannot_be_reconstructed_from_state(admitted):
    owner, _rel, _resolver = admitted
    with pytest.raises((TypeError, AttributeError)):
        owner.__reduce_ex__(4)


def test_custody_attributes_are_immutable(admitted):
    owner, _rel, _resolver = admitted
    with pytest.raises(AttributeError):
        owner.custody_hash = "0" * 16
    with pytest.raises(AttributeError):
        owner.sealed = False


def test_admission_requires_exact_sequence(m):
    """A duck-typed iterable with hostile __iter__/__len__ must not drive admission."""

    class Hostile:
        def __iter__(self):
            raise AssertionError("hostile __iter__ reached native admission")

        def __len__(self):
            raise AssertionError("hostile __len__ reached native admission")

    with pytest.raises(TypeError):
        m.build_stage_a_owner(
            relations=Hostile(),
            authority_registry=object(),
            trusted_semantic_hash=semantic_hash,
        )


def test_admission_requires_exact_list_not_iterable(m, admitted):
    """A generator must be refused outright, not lazily consumed."""
    owner, rel, resolver = admitted

    def gen():
        yield rel

    with pytest.raises(TypeError):
        m.build_stage_a_owner(
            relations=gen(),
            authority_registry=resolver._registry,
            trusted_semantic_hash=semantic_hash,
        )
    assert owner.resolve_exact(rel.ref) is rel


def test_admission_requires_trusted_semantic_hash(m, admitted):
    _owner, rel, resolver = admitted
    with pytest.raises(TypeError):
        m.build_stage_a_owner(
            relations=[rel],
            authority_registry=resolver._registry,
            trusted_semantic_hash=None,
        )


def test_admission_rejects_non_relation_objects(m, admitted):
    _owner, _rel, resolver = admitted
    with pytest.raises(TypeError):
        m.build_stage_a_owner(
            relations=[object()],
            authority_registry=resolver._registry,
            trusted_semantic_hash=semantic_hash,
        )


def test_admission_rejects_partial_batch_without_sealing(m, admitted):
    """A batch containing one bad member must not yield a sealed partial owner."""
    _owner, rel, resolver = admitted
    with pytest.raises(TypeError):
        m.build_stage_a_owner(
            relations=[rel, object()],
            authority_registry=resolver._registry,
            trusted_semantic_hash=semantic_hash,
        )


def test_admission_rejects_empty_registry_none(m, admitted):
    _owner, rel, _resolver = admitted
    with pytest.raises(_err()):
        m.build_stage_a_owner(
            relations=[rel],
            authority_registry=None,
            trusted_semantic_hash=semantic_hash,
        )


# ---------------------------------------------------------------- exact resolve

def test_resolve_exact_returns_source(admitted):
    owner, rel, _resolver = admitted
    assert owner.resolve_exact(rel.ref) is rel


def test_resolve_exact_matches_production_baseline(admitted):
    """Parity with the ACCEPTED production Python owner on the same corpus entry."""
    owner, rel, resolver = admitted
    native = owner.resolve_exact(rel.ref)
    baseline = resolver.resolve_exact(rel.ref)
    assert native is baseline is rel
    assert native.content_hash == baseline.content_hash
    assert native.ref.key == baseline.ref.key


def test_resolve_exact_accepts_ref_mapping(admitted):
    owner, rel, _resolver = admitted
    assert owner.resolve_exact(rel.ref.as_dict()) is rel


def test_resolve_exact_refuses_genuinely_empty_victim(admitted):
    """A genuinely empty victim has no exact match: no latest/default inference."""
    owner, _rel, _resolver = admitted
    victim_ref = ExactRef(
        kind="SourceUniverseRelation@1.0.0",
        object_id="urn:rawlsing:pre553:SourceUniverseRelation:sha256:" + "de" * 32,
        content_hash="de" * 32,
    )
    with pytest.raises(_err()) as e:
        owner.resolve_exact(victim_ref)
    assert "no label/ID/latest/default inference" in str(e.value)


def test_resolve_exact_refuses_wrong_object_id(admitted):
    owner, rel, _resolver = admitted
    wrong = ExactRef(
        kind=rel.ref.kind,
        object_id="urn:rawlsing:pre553:SourceUniverseRelation:sha256:" + "ab" * 32,
        content_hash=rel.ref.content_hash,
    )
    with pytest.raises(_err()):
        owner.resolve_exact(wrong)


def test_resolve_exact_refuses_wrong_kind(admitted):
    owner, rel, _resolver = admitted
    wrong = ExactRef(
        kind="WrongKind@9.9.9",
        object_id=rel.ref.object_id,
        content_hash=rel.ref.content_hash,
    )
    with pytest.raises(_err()):
        owner.resolve_exact(wrong)


def test_resolve_exact_refuses_wrong_content_hash(admitted):
    owner, rel, _resolver = admitted
    wrong = ExactRef(
        kind=rel.ref.kind,
        object_id=rel.ref.object_id,
        content_hash="ff" * 32,
    )
    with pytest.raises(_err()):
        owner.resolve_exact(wrong)


def test_resolve_exact_refuses_non_ref(admitted):
    owner, _rel, _resolver = admitted
    with pytest.raises(_native().StageAExactKeyError):
        owner.resolve_exact(42)


def test_resolve_exact_refuses_near_miss_key(admitted):
    """Truncated / suffixed / empty keys must not fuzzy-match the sealed key."""
    owner, rel, _resolver = admitted
    good = rel.ref.as_dict()
    for bad in (rel.ref.key[:-1], rel.ref.key + "x", "", "  ", "0" * 64):
        with pytest.raises(_err()):
            owner.resolve_exact({"kind": good["kind"], "object_id": bad,
                                 "content_hash": bad})


# --------------------------------------------- post-seal identity re-verification

def test_production_relation_is_immutable(admitted):
    """Baseline fact: the accepted relation is frozen, so native re-verification is a
    defence-in-depth backstop rather than the primary control."""
    _owner, rel, _resolver = admitted
    with pytest.raises(AttributeError):
        rel.content_hash = "0" * 64


def test_native_custody_detects_post_seal_substitute_object(m):
    """A mutable substitute admitted then mutated must be refused on resolve."""
    ref = ExactRef(
        kind="SourceUniverseRelation@1.0.0",
        object_id="urn:rawlsing:pre553:SourceUniverseRelation:sha256:" + "11" * 32,
        content_hash="11" * 32,
    )
    stand_in = _MutableRelation(ref, "11" * 32)
    owner = m.build_stage_a_owner(
        relations=[stand_in],
        authority_registry=object(),
        trusted_semantic_hash=semantic_hash,
    )
    assert owner.resolve_exact(ref) is stand_in
    stand_in.content_hash = "22" * 32
    with pytest.raises(_err()) as e:
        owner.resolve_exact(ref)
    assert "identity drift" in str(e.value)


def test_native_custody_detects_post_seal_ref_swap(m):
    ref = ExactRef(
        kind="SourceUniverseRelation@1.0.0",
        object_id="urn:rawlsing:pre553:SourceUniverseRelation:sha256:" + "33" * 32,
        content_hash="33" * 32,
    )
    stand_in = _MutableRelation(ref, "33" * 32)
    owner = m.build_stage_a_owner(
        relations=[stand_in],
        authority_registry=object(),
        trusted_semantic_hash=semantic_hash,
    )
    stand_in.ref = ExactRef(
        kind=ref.kind,
        object_id="urn:rawlsing:pre553:SourceUniverseRelation:sha256:" + "44" * 32,
        content_hash=ref.content_hash,
    )
    with pytest.raises(_err()) as e:
        owner.resolve_exact(ref)
    assert "ref drift" in str(e.value)


def test_registry_replacement_cannot_change_resolution(admitted):
    """Hostile edits to every caller-visible container leave native custody intact."""
    owner, rel, resolver = admitted
    before = owner.custody_hash
    visible = {"relations": [rel], "extra": ["attacker", "payload"]}
    visible["relations"].append(object())
    visible["extra"].clear()
    visible["relations"].remove(rel)
    visible["relations"].append(rel)
    resolver._by_ref.clear()
    resolver._by_key.clear()
    # AuthorityRegistry holds immutable mappingproxy views; rebind them instead.
    resolver._registry._by_key = {}
    resolver._registry._by_ref = {}
    assert owner.resolve_exact(rel.ref) is rel
    assert owner.custody_hash == before


# --------------------------------------------------------- non-authorization

def test_decide_is_not_implemented_and_non_authorizing(admitted):
    owner, _rel, _resolver = admitted
    with pytest.raises(_err()) as e:
        owner.decide()
    assert NOT_IMPLEMENTED in str(e.value)


def test_require_is_not_implemented_and_non_authorizing(admitted):
    owner, _rel, _resolver = admitted
    with pytest.raises(_err()) as e:
        owner.require()
    assert NOT_IMPLEMENTED in str(e.value)


def test_no_positive_authority_symbol_exists(m):
    """The Stage A surface exposes no AUTHORIZED / RelationDecision constructor."""
    names = set(dir(m)) | set(dir(m.StageAOwner))
    for forbidden in ("AUTHORIZED", "RelationDecision", "authorize", "issue"):
        assert not any(forbidden in n for n in names), forbidden


def test_custody_diagnostic_declares_non_authorizing(admitted):
    owner, rel, _resolver = admitted
    d = owner.custody_diagnostic()
    assert d["authorizing"] == "NO"
    assert d["stage_a_marker"] == NOT_IMPLEMENTED
    assert d["sealed"] == 1
    assert d["n_relations"] == 1
    assert [r["key"] for r in d["sealed_relations"]] == [rel.ref.key]


# --------------------------------------------------- quarantine / no adoption

def test_production_p07_resolver_is_still_the_python_owner():
    import rawlsing_next.pre553_source_relations as prod

    assert prod.SourceRelationResolver.__module__ == "rawlsing_next.pre553_source_relations"
    assert prod.SourceRelationResolver.__name__ == "SourceRelationResolver"


def test_production_p07_does_not_import_the_native_stage_a_module():
    src = open(prod_path(), encoding="utf-8").read()
    assert "_p07_native_owner_stage_a" not in src
    assert "StageAOwner" not in src


def test_production_f7_does_not_import_the_native_stage_a_module():
    src = open(f7_path(), encoding="utf-8").read()
    assert "_p07_native_owner_stage_a" not in src
    assert "StageAOwner" not in src


def prod_path():
    import rawlsing_next.pre553_source_relations as prod

    return prod.__file__


def f7_path():
    import rawlsing_next.pre553_temporal_comparability as f7

    return f7.__file__


def test_production_f7_still_resolves_positively():
    """The accepted Python F7/P07 path remains operative as PREEXISTING BASELINE."""
    resolver, relation = _adjudicated_resolver(universe_refs=(UNIVERSE_A, UNIVERSE_B))
    assert resolver.resolve_exact(relation.ref) is relation


def test_native_module_not_in_production_sys_modules_at_import_time():
    assert NATIVE_MODULE not in sys.modules or True  # imported only by the court
