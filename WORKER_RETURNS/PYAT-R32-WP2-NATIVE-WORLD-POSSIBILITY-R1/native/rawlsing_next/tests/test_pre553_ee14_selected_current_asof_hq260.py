"""HQ260 G03 — B5/C1-03R selected CURRENT/as-of source-free lifecycle court.

BOUNDED, SOURCE-FREE, NON-AUTHORIZING QUALIFICATION COURT.

What this court is for
----------------------
G3 of `PYAT_CONTROL_ROOM/EE14_SOURCE_FREE_SELECTED_USE_COMPETENCE_HQ260_R1.md` requires
the *existing* accepted B5/C1-03R lifecycle owner — not a new parallel state machine — to
register a FIXTURE-only selected release/product and answer actual current/as-of queries
through the owner, with historical replay, affected/unaffected dependency transition and
typed fail-closed refusals.

It uses the two accepted owners unchanged:

* ``LearnedProductLifecycleExecutor`` (``pre553_learned_product_lifecycle``) —
  ``stage_release`` / ``register_product`` / ``publish_product`` / ``selection_key`` /
  ``select_current`` / ``supersede_current`` / ``declare_invalidation`` /
  ``resolve_current_as_of`` / ``export_checkpoint`` / ``from_checkpoint``.
* ``resolve_current_analytical_product`` (``pre553_analytical_replay_dependency``) for
  the owner-unknown dependent refusal at the analytical grain.

What this court does NOT do
---------------------------
* It adds **no** production adapter and no second state machine. If the accepted owner
  drift changes the surface below, this court fails loudly rather than adapting around it.
* It claims **no** EE14/T1 model use, no source permission, no issuer/AT07 authority, no
  native F7, no actor/V3, no pair grant and no temporal sign. Every identity here is a
  clearly-scoped ``urn:hq260:g3:fixture:`` fixture; test-created refs are identities for a
  state machine, never authority.
* It does not re-run the two accepted owner courts
  (``test_pre553_learned_product_lifecycle.py``, ``test_pre553_analytical_replay_dependency.py``).
  It adds the *selected-current join* and a real **fresh-process** checkpoint
  reconstruction.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from rawlsing_next import pre553_analytical_replay_dependency as ARD
from rawlsing_next import pre553_learned_product_lifecycle as B5
from rawlsing_next.pre553_authority_maintenance import (
    AuthorityMaintenanceExecutor,
    SemanticDeterminantGraph,
)
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash

FIXTURE_ROOT = "urn:hq260:g3:fixture"


def _h(tag: str) -> str:
    return hashlib.sha256(tag.encode("utf-8")).hexdigest()


def _er(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"{FIXTURE_ROOT}:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _ar(authority_id: str, version: str = "1.0.0") -> AuthorityRef:
    return AuthorityRef(authority_id, version, _h(f"auth:{authority_id}:{version}"))


#: Determinants. D1 is the "changed" determinant; D2 is the untouched sibling.
D1 = _er("Determinant", "d1")
D2 = _er("Determinant", "d2")

EVENT_AUTHORITY = _er("EventAuthority", "ea1")
EVENT_RULE = _er("EventRule", "er1")
SELECTION_ATTESTATION = _er("SelectionAttestation", "att1")
SCOPE = _er("SelectionScope", "scope1")
PURPOSE = _er("SelectionPurpose", "purpose1")
SUPERSESSION_BASIS = _er("SupersessionBasis", "sb1")
DEPENDENCY_CLOSURE = _er("DependencyClosure", "dc1")


def _subject(tag: str, determinants: tuple[ExactRef, ...]) -> B5.LearnedProductLifecycleSubject:
    """A source-free fixture learned-product release view.

    This is the fixture-only 'selected release/product' identity: it is deliberately
    *not* an authorized release. The B5 owner treats it as an opaque exact release and
    the court never claims it carries any permission.
    """
    return B5.LearnedProductLifecycleSubject(
        release_ref=_er("LearnedProductRelease", tag),
        product_ref=_er("LearnedProduct", tag),
        product_family_ref=_er("LearnedProductFamily", "family1"),
        producer_owner_ref=_er("ProducerOwner", "owner1"),
        producer_contract_ref=_er("ProducerContract", "contract1"),
        semantic_projection_hash=_h(f"projection:{tag}"),
        authority_snapshot_refs=(_ar("HQ260-G3-FIXTURE-SEMANTIC"),),
        direct_dependency_refs=(),
        determinant_refs=tuple(determinants),
        determinant_set_hash=semantic_hash([d.as_dict() for d in determinants]),
        replay_root_ref=_er("ReplayRoot", "rr1"),
        selection_scope_ref=SCOPE,
        build_or_release_receipt_refs=(_er("BuildReceipt", f"build-{tag}"),),
        producer_permission_ceiling_ref=_er("ProducerPermissionCeiling", "pc1"),
    )


RELEASE_A = _subject("release-a", (D1,))
RELEASE_B = _subject("release-b", (D2,))
RELEASE_C = _subject("release-c", (D1,))


def _publish(executor: B5.LearnedProductLifecycleExecutor, subject) -> None:
    executor.stage_release(subject)
    executor.register_product(
        subject.release_ref,
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
    )
    executor.publish_product(
        subject.release_ref,
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
    )


def _selection_key(executor: B5.LearnedProductLifecycleExecutor):
    return executor.selection_key(
        product_family_ref=RELEASE_A.product_family_ref,
        selection_scope_ref=SCOPE,
        selection_purpose_ref=PURPOSE,
    )


def _select(executor, key, subject, *, previous=None):
    return executor.select_current(
        key.ref,
        subject.release_ref,
        expected_previous_receipt_ref=previous,
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
        selection_attestation_ref=SELECTION_ATTESTATION,
    )


def _scenario():
    """A, B and C published; A selected current. Returns (executor, key, receipt_a)."""
    executor = B5.LearnedProductLifecycleExecutor()
    for subject in (RELEASE_A, RELEASE_B, RELEASE_C):
        _publish(executor, subject)
    key = _selection_key(executor)
    receipt_a = _select(executor, key, RELEASE_A)
    return executor, key, receipt_a


# ===========================================================================
# 1. Positive: selected CURRENT is a property of the OWNER receipt
# ===========================================================================

def test_g3_selected_current_derives_from_the_owner_receipt():
    executor, key, receipt_a = _scenario()
    resolution = executor.resolve_current_as_of(
        key.ref, as_of_event_ref=receipt_a.current_select_event_ref
    )
    assert resolution.state == "CURRENT_SELECTED"
    assert resolution.selected_release_ref == RELEASE_A.release_ref
    # the currentness is reported WITH the exact owner receipt that established it
    assert resolution.receipt_ref == receipt_a.ref
    # the owner exposes the same receipt through its own index API
    assert executor.current_selection_receipt_ref(key.ref) == receipt_a.ref


def test_g3_currentness_is_not_readable_off_a_release_object_or_cache():
    """No cache/timestamp/flagname path may report currentness.

    The B5 subject carries no currentness field at all, and the owner exposes no
    latest/default/current accessor other than the exact-as-of resolver.
    """
    for forbidden in ("current", "is_current", "currentness", "selected", "as_of"):
        assert not hasattr(RELEASE_A, forbidden), forbidden
    for forbidden in (
        "latest_release",
        "current_release",
        "default_release",
        "newest_release",
        "current_as_of_now",
    ):
        assert not hasattr(B5.LearnedProductLifecycleExecutor, forbidden), forbidden


def test_g3_second_purpose_or_scope_cannot_inherit_currentness():
    executor, key, receipt_a = _scenario()
    other_key = executor.selection_key(
        product_family_ref=RELEASE_A.product_family_ref,
        selection_scope_ref=SCOPE,
        selection_purpose_ref=_er("SelectionPurpose", "purpose2"),
    )
    unresolved = executor.resolve_current_as_of(
        other_key.ref, as_of_event_ref=receipt_a.current_select_event_ref
    )
    assert unresolved.state == "UNKNOWN_CURRENTNESS"
    assert unresolved.selected_release_ref is None


# ===========================================================================
# 2. Positive: the same scenario answers by event AND by checkpoint
# ===========================================================================

def test_g3_as_of_event_and_as_of_checkpoint_agree():
    executor, key, receipt_a = _scenario()
    checkpoint = executor.export_checkpoint()
    by_event = executor.resolve_current_as_of(
        key.ref, as_of_event_ref=receipt_a.current_select_event_ref
    )
    by_checkpoint = executor.resolve_current_as_of(key.ref, as_of_checkpoint=checkpoint)
    assert by_event.state == by_checkpoint.state == "CURRENT_SELECTED"
    assert by_event.selected_release_ref == by_checkpoint.selected_release_ref
    assert by_event.receipt_ref == by_checkpoint.receipt_ref


def test_g3_tampered_checkpoint_is_refused():
    executor, key, receipt_a = _scenario()
    checkpoint = executor.export_checkpoint()
    tampered = json.loads(json.dumps(checkpoint))
    tampered["checkpoint_hash"] = "0" * 64
    with pytest.raises(B5.LearnedProductLifecycleConflict):
        executor.resolve_current_as_of(key.ref, as_of_checkpoint=tampered)


# ===========================================================================
# 3. Fresh-process checkpoint reconstruction (the genuinely new G3 evidence)
# ===========================================================================

def reconstruct_and_resolve(checkpoint_path: str) -> dict:
    """Module-level entry point executed inside a FRESH interpreter process."""
    payload = json.loads(Path(checkpoint_path).read_text())
    executor = B5.LearnedProductLifecycleExecutor.from_checkpoint(payload["checkpoint"])
    key = executor.selection_key(
        product_family_ref=ExactRef(**payload["family"]),
        selection_scope_ref=ExactRef(**payload["scope"]),
        selection_purpose_ref=ExactRef(**payload["purpose"]),
    )
    resolution = executor.resolve_current_as_of(
        key.ref, as_of_checkpoint=payload["checkpoint"]
    )
    return {
        "state": resolution.state,
        "selected_release_ref": (
            resolution.selected_release_ref.as_dict()
            if resolution.selected_release_ref
            else None
        ),
        "receipt_ref": resolution.receipt_ref.as_dict() if resolution.receipt_ref else None,
    }


def test_g3_fresh_process_checkpoint_reconstruction(tmp_path):
    executor, key, receipt_a = _scenario()
    checkpoint = executor.export_checkpoint()
    payload_path = tmp_path / "g3_checkpoint.json"
    payload_path.write_text(
        json.dumps(
            {
                "checkpoint": checkpoint,
                "family": RELEASE_A.product_family_ref.as_dict(),
                "scope": SCOPE.as_dict(),
                "purpose": PURPOSE.as_dict(),
            }
        )
    )
    driver = tmp_path / "g3_fresh_process.py"
    driver.write_text(
        "import importlib.util, json, sys\n"
        f"spec = importlib.util.spec_from_file_location('g3_court', {str(Path(__file__))!r})\n"
        "module = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(module)\n"
        "print(json.dumps(module.reconstruct_and_resolve(sys.argv[1])))\n"
    )
    repo_root = str(Path(__file__).resolve().parents[2])
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        [repo_root] + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else [])
    )
    completed = subprocess.run(
        [sys.executable, str(driver), str(payload_path)],
        capture_output=True,
        text=True,
        check=False,
        cwd=repo_root,
        env=env,
    )
    assert completed.returncode == 0, completed.stderr
    fresh = json.loads(completed.stdout.strip().splitlines()[-1])
    assert fresh["state"] == "CURRENT_SELECTED"
    assert fresh["selected_release_ref"] == RELEASE_A.release_ref.as_dict()
    assert fresh["receipt_ref"] == receipt_a.ref.as_dict()

    # and a fresh process asked about a key it never selected reports UNKNOWN
    key_ref_absent = _er("SelectionKey", "never-created")
    payload = json.loads(payload_path.read_text())
    restored = B5.LearnedProductLifecycleExecutor.from_checkpoint(payload["checkpoint"])
    with pytest.raises(B5.LearnedProductLifecycleError):
        restored.resolve_current_as_of(key_ref_absent, as_of_checkpoint=payload["checkpoint"])


# ===========================================================================
# 4. Historical replay: supersession preserves the prior exact product
# ===========================================================================

def test_g3_historical_as_of_still_resolves_the_prior_product():
    executor, key, receipt_a = _scenario()
    receipt_b = executor.supersede_current(
        key.ref,
        predecessor_release_ref=RELEASE_A.release_ref,
        successor_release_ref=RELEASE_B.release_ref,
        expected_previous_receipt_ref=receipt_a.ref,
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
        selection_attestation_ref=SELECTION_ATTESTATION,
        supersession_basis_ref=SUPERSESSION_BASIS,
    )
    now = executor.resolve_current_as_of(
        key.ref, as_of_event_ref=receipt_b.current_select_event_ref
    )
    then = executor.resolve_current_as_of(
        key.ref, as_of_event_ref=receipt_a.current_select_event_ref
    )
    assert now.state == then.state == "CURRENT_SELECTED"
    assert now.selected_release_ref == RELEASE_B.release_ref
    assert then.selected_release_ref == RELEASE_A.release_ref
    assert now.receipt_ref != then.receipt_ref
    # the superseded release is still exact-addressable as history
    assert executor.lifecycle_state(RELEASE_A.release_ref).registered is True


# ===========================================================================
# 5. Affected/unaffected dependency transition and typed stale refusal
# ===========================================================================

def test_g3_affected_and_unaffected_dependency_transition():
    executor, key, receipt_a = _scenario()
    invalidation = executor.declare_invalidation(
        [D1],
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
        dependency_closure_receipt_ref=DEPENDENCY_CLOSURE,
        selection_attestation_ref=SELECTION_ATTESTATION,
        current_transitions={key.ref.key: None},
    )
    affected = {
        ref.object_id
        for ref in (
            invalidation.directly_affected_release_refs
            + invalidation.transitively_affected_release_refs
        )
    }
    unaffected = {ref.object_id for ref in invalidation.unaffected_product_refs}
    # D1 reaches A and C; the D2-only sibling B is untouched
    assert RELEASE_A.release_ref.object_id in affected
    assert RELEASE_C.release_ref.object_id in affected
    assert RELEASE_B.product_ref.object_id in unaffected
    assert RELEASE_B.product_ref.object_id not in affected

    resolution = executor.resolve_current_as_of(
        key.ref, as_of_event_ref=executor.events[-1].ref
    )
    assert resolution.state == "NO_CURRENT"
    assert resolution.selected_release_ref is None


def test_g3_invalidated_release_cannot_be_served_as_current():
    executor, key, receipt_a = _scenario()
    executor.declare_invalidation(
        [D1],
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
        dependency_closure_receipt_ref=DEPENDENCY_CLOSURE,
        selection_attestation_ref=SELECTION_ATTESTATION,
        current_transitions={key.ref.key: None},
    )
    latest = executor.events[-1].ref
    no_current = executor.resolve_current_as_of(key.ref, as_of_event_ref=latest)
    assert no_current.state == "NO_CURRENT"
    # the historical exact receipt still resolves the OLD product, never as current
    historical = executor.resolve_current_as_of(
        key.ref, as_of_event_ref=receipt_a.current_select_event_ref
    )
    assert historical.selected_release_ref == RELEASE_A.release_ref
    # and the invalidated product may not be re-selected as current
    with pytest.raises(B5.LearnedProductLifecycleError, match="invalidated/withdrawn"):
        _select(executor, key, RELEASE_A, previous=no_current.receipt_ref)


# ===========================================================================
# 6. Hostile: unknown selection and self-proclaimed current
# ===========================================================================

def test_g3_unknown_selection_key_is_refused_not_guessed():
    executor, key, receipt_a = _scenario()
    fabricated = _er("SelectionKey", "fabricated-by-caller")
    with pytest.raises(B5.LearnedProductLifecycleError):
        executor.resolve_current_as_of(
            fabricated, as_of_event_ref=receipt_a.current_select_event_ref
        )


def test_g3_self_proclaimed_current_receipt_is_refused():
    executor, key, receipt_a = _scenario()
    fabricated_receipt = _er("CurrentSelectionReceipt", "fabricated-by-caller")
    with pytest.raises(B5.LearnedProductLifecycleError):
        executor.resolve_selection_exact(key.ref, fabricated_receipt)


def test_g3_staged_but_unselected_release_is_unknown_not_current():
    executor = B5.LearnedProductLifecycleExecutor()
    for subject in (RELEASE_A, RELEASE_B, RELEASE_C):
        _publish(executor, subject)
    key = _selection_key(executor)
    resolution = executor.resolve_current_as_of(
        key.ref, as_of_event_ref=executor.events[-1].ref
    )
    assert resolution.state == "UNKNOWN_CURRENTNESS"
    assert resolution.selected_release_ref is None


# ===========================================================================
# 7. Analytical-grain owner-unknown refusal (existing owner, zero-release state)
# ===========================================================================

def test_g3_owner_unknown_analytical_dependent_is_never_current():
    executor = AuthorityMaintenanceExecutor(
        determinant_graph=SemanticDeterminantGraph(known_dependent_refs=(_er("AnalyticalProduct", "known"),))
    )
    with pytest.raises(ARD.OwnerUnknownDependent):
        ARD.resolve_current_analytical_product(
            executor=executor, dependent_ref=_er("AnalyticalProduct", "absent")
        )


# ===========================================================================
# 8. Scope guards
# ===========================================================================

def test_g3_no_new_adapter_module_was_manufactured():
    assert importlib.util.find_spec("rawlsing_next.pre553_ee14_selected_current_asof") is None


def test_g3_court_claims_no_service_or_model_use_permission():
    """Neither the owners nor this court expose a permission-issuing surface."""
    this_module = sys.modules[__name__]
    forbidden = (
        "issue_permission",
        "grant_permission",
        "authorize_service",
        "grant_model_use",
        "issue_model_use",
    )
    for module in (B5, ARD, this_module):
        for name in forbidden:
            assert not hasattr(module, name), (module.__name__, name)
