"""Independent source-free S06R adversaries, frozen BEFORE reading S06 candidate tests.

Run ONLY inside an isolated, authorized candidate checkout that also contains
this reviewer-owned test file; require explicit host/runtime evidence.
These are SECURITY ACCEPTANCE expectations; failing cases demonstrate a
candidate security deficit, not a bug in accepted P04/N04R tests.

No current selection is authorized: values in this file are synthetic strings.
"""
from __future__ import annotations

import copy
import inspect
import pytest

from rawlsing_next import s06_trusted_release_replay as s06


def make_simple_checkpoint():
    ck = s06.TrustedCheckpoint()
    ck.append_event({"kind": "REGISTERED", "release_ref": "SYNTHETIC_A"})
    return ck


@pytest.mark.parametrize("name,args", [
    ("withdraw", ("SYNTHETIC_A",)),
    ("invalidate", ("SYNTHETIC_A",)),
    ("supersede", ("SYNTHETIC_A", "SYNTHETIC_B")),
    ("revoke", ("SYNTHETIC_A",)),
    ("invalidate_descendants", ("SYNTHETIC_A",)),
])
def test_s06r_caller_trusted_true_must_not_act_as_external_verifier(name, args):
    ck = s06.TrustedCheckpoint()
    verdict = getattr(ck, name)(*args, trusted=True)
    assert not verdict.allowed, "caller boolean is not independently verified authority"
    assert ck.events == ()


def test_s06r_caller_trusted_true_cannot_select_arbitrary_unpublished_release():
    ck = s06.TrustedCheckpoint()
    result = ck.select_current("synthetic-selection", "NEVER_REGISTERED", current_epoch=99, trusted=True)
    assert not result.allowed
    assert ck.events == ()


def test_s06r_public_append_event_cannot_bypass_auth_gate():
    ck = s06.TrustedCheckpoint()
    try:
        ck.append_event({"kind": "PUBLISHED", "release_ref": "UNISSUED"})
    except (PermissionError, ValueError):
        pass
    assert ck.get_state().get("publications", {}).get("UNISSUED") != "PUBLISHED"


def test_s06r_arbitrary_nonempty_external_token_is_not_issuer_validation():
    ck = make_simple_checkpoint()
    restored = s06.TrustedCheckpoint.from_checkpoint(
        ck.export(), require_independent_auth=True, external_auth_token="totally-unsigned-caller-token"
    )
    assert restored is None


def test_s06r_consistent_history_state_hash_rewrite_is_not_external_custody():
    original = make_simple_checkpoint().export()
    forged = copy.deepcopy(original)
    forged["checkpoint_payload"]["events"] = [
        {"kind": "REGISTERED", "release_ref": "MALICIOUS_RELEASE"},
        {"kind": "PUBLISHED", "release_ref": "MALICIOUS_RELEASE"}
    ]
    forged["checkpoint_payload"]["state"] = {"publications": {"MALICIOUS_RELEASE": "PUBLISHED"}}
    forged["event_count"] = 2
    forged["event_history_hash"] = s06._event_history_hash(forged["checkpoint_payload"]["events"])
    forged["state_projection_hash"] = s06._state_projection_hash(forged["checkpoint_payload"]["state"])
    restored = s06.TrustedCheckpoint.from_checkpoint(
        forged, require_independent_auth=True, external_auth_token="attacker-authored"
    )
    assert restored is None, "rehashed payload is not a signed external history root"


def test_s06r_epoch_must_be_bound_to_issuer_and_replayed_events():
    ck = make_simple_checkpoint()
    forged = ck.export()
    forged["checkpoint_payload"]["epoch"] = 100_000_000
    # Event hash, state hash, count are deliberately unchanged: epoch is outside all.
    restored = s06.TrustedCheckpoint.from_checkpoint(forged)
    assert restored is None, "unauthenticated arbitrary high epoch cannot be promoted"


def test_s06r_revocation_set_must_be_issued_and_ledger_bound():
    ck = make_simple_checkpoint()
    forged = ck.export()
    forged["checkpoint_payload"]["revoked"] = ["SYNTHETIC_UNAUTHORIZED_REVOCATION"]
    restored = s06.TrustedCheckpoint.from_checkpoint(forged)
    assert restored is None, "revocation set is outside both hashes and independent issuer"


def test_s06r_transitive_descendants_not_one_hop():
    ck = s06.TrustedCheckpoint()
    ck.supersede("A", "B", trusted=True)
    ck.supersede("B", "C", trusted=True)
    ck.supersede("X", "Y", trusted=True)
    ck.invalidate_descendants("A", trusted=True)
    invalidations = ck.get_state().get("invalidations", [])
    assert set(invalidations) == {"A", "B", "C"}  # Unrelated X,Y remain intact.


def test_s06r_immutable_export_not_mutable_state_alias():
    ck = make_simple_checkpoint()
    view = ck.get_state()
    view["publications"]["SYNTHETIC_A"] = "PUBLISHED"
    assert ck.get_state()["publications"]["SYNTHETIC_A"] == "REGISTERED"


def test_s06r_event_property_is_immutable_deep_snapshot():
    ck = make_simple_checkpoint()
    exposed = ck.events
    try:
        exposed[0]["kind"] = "PUBLISHED"
    except (TypeError, AttributeError):
        pass
    assert ck.events[0]["kind"] == "REGISTERED"


def test_s06r_unknown_event_cannot_silently_enter_event_ledger():
    ck = s06.TrustedCheckpoint()
    try:
        ck.append_event({"kind": "FAKE_ISSUER", "release_ref": "SYNTHETIC_A"})
    except (ValueError, PermissionError):
        pass
    assert not ck.events


def test_s06r_protected_current_mode_not_unconditionally_allowed():
    ck = s06.TrustedCheckpoint()
    result = ck.verify_trust_mode(s06.TrustMode.PROTECTED_CURRENT)
    assert not result.allowed, "no subject, event, trusted epoch, release state or issued capability"


def test_s06r_external_mode_without_independent_root_must_refuse():
    ck = s06.TrustedCheckpoint()
    assert not ck.verify_trust_mode(s06.TrustMode.EXTERNAL_CUSTODY).allowed


def test_s06r_real_owner_checkpoint_schema_interoperation():
    from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleExecutor
    real_owner_ck = LearnedProductLifecycleExecutor().export_checkpoint()
    restored = s06.TrustedCheckpoint.from_checkpoint(real_owner_ck)
    assert restored is not None, "a claimed B5 checkpoint verifier must accept valid B5 owner schema"


def test_s06r_owner_wrapping_is_not_a_second_detached_state_machine():
    source = inspect.getsource(s06)
    assert "pre553_learned_product_lifecycle" in source
    assert "pre553_learned_product_release" in source
    assert "LearnedProductLifecycleExecutor" in source
    assert "M2Repository" in source


def test_s06r_without_event_signature_cold_replay_not_external_trust():
    ck = s06.TrustedCheckpoint()
    ck.append_event({"kind": "PUBLISHED", "release_ref": "SYNTHETIC_FAKE"})
    assert not ck.verify_trust_mode(s06.TrustMode.PROTECTED_CURRENT).allowed
    # cold_replay may prove internal consistency, never external authentication.


def test_s06r_untrusted_selection_cannot_be_staged_through_public_event_api():
    ck = s06.TrustedCheckpoint()
    ck.append_event({"kind": "SELECTED", "selection_key": "KEY", "release_ref": "UNKNOWN"})
    assert ck.get_state().get("selections", {}).get("KEY") is None
