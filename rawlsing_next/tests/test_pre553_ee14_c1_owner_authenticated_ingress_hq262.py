"""HQ262 G01 -- G1 owner-only C1 -> authenticated F8 selected ingress court.

SOURCE-FREE. TEST_ONLY_UNISSUED model/use refs. NOT AN EE14 GRANT. NOT A TRUST ROOT.
NOT DEPLOYED SECURITY. G1_INTERNAL_OWNER_PATH_CANDIDATE_ONLY.

The whole point of this court is that the external client is a DATA-ONLY caller. Every
hostile below is attempted against the public `serve` surface, not against private state.
"""
from __future__ import annotations

import pytest

import rawlsing_next.tests.test_pre553_analytical_composition as C1T
from rawlsing_next.pre553_analytical_composition import (
    compose_positioned_subject_possibility,
)
from rawlsing_next.pre553_ee14_c1_owner_authenticated_ingress import (
    CONTRACT,
    ALLOWED_CELLS,
    OwnerOnlySelectedIngress,
    SelectedIngressError,
    SelectedIngressPermissionError,
    SelectedRequest,
)
from rawlsing_next.source_backed_positioned_subject_possibility import (
    evaluate_positioned_subject_possibility,
)

MARKER = "TEST_ONLY_UNISSUED__NOT_AN_EE14_GRANT__G1_INTERNAL_OWNER_PATH_CANDIDATE_ONLY"

# TEST-ONLY UNISSUED applicability/G2 scope material. Not a real permission.
OWNER_SCOPE = {
    "scope_id": "TEST_ONLY_UNISSUED_APPLICABILITY_SCOPE",
    "purpose": "SOURCE_FREE_DEVELOPMENT_ONLY",
    "issued": False,
    "ee14_grant": None,
}


@pytest.fixture(scope="module")
def source_free():
    """Real source-free C1 fixture from the accepted producer test helpers.

    The accepted at07 helper needs a MonkeyPatch; it is created and undone locally so
    this module-scoped fixture stays valid.
    """
    mp = pytest.MonkeyPatch()
    # at07 is a pytest fixture in the producer test module; call its underlying function.
    inner = getattr(C1T.at07, "__wrapped__", C1T.at07)
    try:
        yield inner(mp)
    finally:
        mp.undo()


def _ingress(at07):
    source, query_auth, registry = at07
    predicate, producer_query = C1T._producer(source, query_auth, "forward")
    consumer_query, binding = C1T._consumer(source, "forward")
    witness = C1T._witness(source, "forward", consumer_query, binding,
                           producer_query, predicate)
    common = {
        "repository": source["repo"],
        "empirical_query": producer_query,
        "predicate": predicate,
        "authority_registry": registry,
        "release_refs": (source["release_ref"],),
        "consumer_query": consumer_query,
        "model_rule": C1T._model(source),
        "condition_binding_witness": witness,
    }
    # two permitted cells, each with OWNER-HELD inputs
    cell_inputs = {
        "q1": {"empirical_query": producer_query, "predicate": predicate,
               "consumer_query": consumer_query, "model_rule": C1T._model(source)},
        "q2": {"empirical_query": producer_query, "predicate": predicate,
               "consumer_query": consumer_query, "model_rule": C1T._model(source)},
    }
    return OwnerOnlySelectedIngress(c1_inputs=common, cell_inputs=cell_inputs,
                                    applicability_scope=OWNER_SCOPE)


@pytest.fixture(scope="module")
def ingress(source_free):
    return _ingress(source_free)


def _stratum(at07):
    _source, _query_auth, _registry = at07
    consumer_query, _binding = C1T._consumer(_source, "forward")
    return tuple(consumer_query.conditioner_ids)


# ============================================================== POSITIVE

@pytest.mark.parametrize("cell", ALLOWED_CELLS)
def test_positive_owner_originated_ingress(ingress, source_free, cell):
    """Positive: the owner executes C1 and the receipt binds the full C1 identity."""
    ids = _stratum(source_free)
    r = ingress.serve(SelectedRequest(cell=cell, stratum_ids=ids))
    assert r.contract == CONTRACT
    assert r.cell == cell
    assert len(r.c1_identity_hash) == 64
    assert r.c1_evidence_ref_key
    assert r.c1_evidence_authority_keys, "C1-originated evidence must carry authority custody"
    assert r.c1_evidence_provenance_keys, "C1-originated evidence must carry provenance"
    assert len(r.f8_result_hash) == 64
    assert r.applicability_scope_hash
    assert len(r.origin_receipt_hash) == 64
    # a technical receipt is NOT an authorisation
    assert r.authorizing is False


def test_positive_receipt_binds_full_c1_lineage_not_just_f8(ingress, source_free):
    ids = _stratum(source_free)
    r = ingress.serve(SelectedRequest(cell="q1", stratum_ids=ids))
    # the receipt carries C1 identity AND the C1 evidence preimage AND the F8 hash, so a
    # caller who keeps only the F8 number cannot reconstruct a selected receipt
    assert r.c1_identity_hash != r.f8_result_hash
    assert r.origin_receipt_hash not in (r.c1_identity_hash, r.f8_result_hash)


def test_positive_is_deterministic_for_the_same_request(ingress, source_free):
    ids = _stratum(source_free)
    a = ingress.serve(SelectedRequest(cell="q1", stratum_ids=ids))
    b = ingress.serve(SelectedRequest(cell="q1", stratum_ids=ids))
    assert a.origin_receipt_hash == b.origin_receipt_hash
    assert a.f8_result_hash == b.f8_result_hash


# ============================================================== HOSTILES

def test_hostile_client_cannot_supply_evidence_at_all(ingress):
    """There is no request field through which evidence can arrive."""
    import dataclasses
    bad = SelectedRequest(cell="q1", stratum_ids=("x",))
    with pytest.raises(dataclasses.FrozenInstanceError):
        bad.evidence = object()                      # frozen request
    assert not hasattr(SelectedRequest, "evidence")
    assert not hasattr(SelectedRequest, "authority_refs")
    assert not hasattr(SelectedRequest, "c1_result")


def test_hostile_unknown_cell_refused(ingress, source_free):
    ids = _stratum(source_free)
    with pytest.raises(SelectedIngressError):
        ingress.serve(SelectedRequest(cell="q3", stratum_ids=ids))


@pytest.mark.parametrize("bad", [
    None, 42, "q1", [], {}, object(), b"q1",
    type("Sneaky", (), {})(),
])
def test_hostile_non_request_shapes_refused(ingress, bad):
    with pytest.raises(SelectedIngressError):
        ingress.serve(bad)


def test_hostile_stratum_mismatch_refused_without_substitution(ingress, source_free):
    """A client asking for a grain the C1 owner did not produce is refused."""
    with pytest.raises(SelectedIngressError) as e:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=("not", "the", "grain")))
    assert "grain" in str(e.value) or "substitution" in str(e.value)


def test_hostile_stratum_ids_must_be_plain_strings(ingress):
    for bad in ((), ["a"], ("a", 1), (object(),), (None,)):
        with pytest.raises(SelectedIngressError):
            ingress.serve(SelectedRequest(cell="q1", stratum_ids=bad))


def test_hostile_recomputed_caller_hash_is_unusable(ingress, source_free):
    """A caller-recomputed digest is not a receipt: the ingress never reads one."""
    ids = _stratum(source_free)
    r = ingress.serve(SelectedRequest(cell="q1", stratum_ids=ids))
    forged = "0" * 64
    # the honest receipt is NOT recomputable from the F8 number the client can observe
    assert r.origin_receipt_hash != forged
    # and there is no request channel to submit a hash into
    assert not hasattr(SelectedRequest, "origin_receipt_hash")
    assert not hasattr(SelectedRequest, "hash")


def test_low_level_f8_direct_call_can_never_mint_a_selected_receipt(source_free):
    """F8 has no notion of the selected receipt; a direct call yields only the numeric."""
    source, query_auth, registry = source_free
    predicate, producer_query = C1T._producer(source, query_auth, "forward")
    consumer_query, _binding = C1T._consumer(source, "forward")
    witness = C1T._witness(source, "forward", consumer_query, _binding,
                           producer_query, predicate)
    composed = compose_positioned_subject_possibility(
        repository=source["repo"], empirical_query=producer_query, predicate=predicate,
        authority_registry=registry, release_refs=(source["release_ref"],),
        consumer_query=consumer_query, model_rule=C1T._model(source),
        condition_binding_witness=witness)
    ev = composed.possibility_slice_evidence_or_null
    low = evaluate_positioned_subject_possibility(
        query=consumer_query, rule=C1T._model(source), evidence=(ev,))
    assert not hasattr(low, "origin_receipt_hash")
    assert not hasattr(low, "authorizing")
    for field in ("c1_identity_hash", "applicability_scope_hash"):
        assert not hasattr(low, field)


def test_receipt_is_not_a_grant_and_grants_no_permission(ingress, source_free):
    ids = _stratum(source_free)
    r = ingress.serve(SelectedRequest(cell="q1", stratum_ids=ids))
    assert r.authorizing is False
    assert not hasattr(r, "grant_ref")
    assert not hasattr(r, "ee14_grant")
    assert not hasattr(r, "currentness")
    assert OWNER_SCOPE["issued"] is False and OWNER_SCOPE["ee14_grant"] is None


def test_owner_scope_material_is_read_only(ingress):
    scope = ingress.owner_scope_material()
    with pytest.raises(TypeError):
        scope["injected"] = True


def test_owner_setup_requires_every_permitted_cell(source_free):
    source, query_auth, registry = source_free
    predicate, producer_query = C1T._producer(source, query_auth, "forward")
    consumer_query, _b = C1T._consumer(source, "forward")
    witness = C1T._witness(source, "forward", consumer_query, _b, producer_query, predicate)
    common = {
        "repository": source["repo"], "empirical_query": producer_query,
        "predicate": predicate, "authority_registry": registry,
        "release_refs": (source["release_ref"],), "consumer_query": consumer_query,
        "model_rule": C1T._model(source), "condition_binding_witness": witness,
    }
    with pytest.raises(SelectedIngressError):
        OwnerOnlySelectedIngress(c1_inputs=common, cell_inputs={},
                                applicability_scope=OWNER_SCOPE)


def test_strong_same_process_monkeypatch_adversary_is_labelled_unproved():
    """Explicitly UNPROVED under the data-only contract. Not claimed as covered."""
    import rawlsing_next.pre553_ee14_c1_owner_authenticated_ingress as M
    assert "UNPROVED" in M.__doc__
    assert "NOT DEPLOYED" in M.__doc__.upper() or "NOT DEPLOYED SECURITY" in M.__doc__