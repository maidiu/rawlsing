from copy import deepcopy

from rawlsing_next.rabochii_execution_protocol import (
    validate_court_spec,
    validate_execution_state,
)


SHA_A = "1" * 40
SHA_B = "2" * 40


def _state():
    return {
        "schema_id": "RABOCHII_EXECUTION_STATE@1.0.0",
        "profile": "IMPLEMENT",
        "phase": "IMPLEMENT",
        "semantic_candidate_sha": SHA_A,
        "branch_tip_sha": SHA_A,
        "evidence_execution_sha": None,
        "terminal_definition_revision": 1,
        "revision_authority_ref": None,
        "frozen_terminal_claim_ids": ["C1"],
        "claims": [{
            "id": "C1",
            "type": "DETERMINISTIC_EXECUTION",
            "status": "READY",
            "proof_mode": "EXACT",
            "required_proofs": 1,
            "proof_owners": [],
        }],
        "current_action": {
            "advances_claim_id": "C1",
            "description": "Run the frozen court.",
        },
        "mutation_envelope": {"allowed_paths": ["rawlsing_next/"], "forbidden_paths": ["main"]},
        "fresh_state": {
            "checked": False,
            "branch_tip_sha": None,
            "observed_proof_owner_ids": [],
        },
        "terminal": {"status": "OPEN", "blocker_class": None, "blocking_claim_ids": []},
    }


def _owner(owner_id="O1", *, status="PROVEN", subject_sha=SHA_A, compatible=True):
    return {
        "id": owner_id,
        "status": status,
        "subject_sha": subject_sha,
        "compatibility": "VERIFIED" if compatible else "UNVERIFIED",
        "volatility": "IMMUTABLE",
        "relevant_tree_equivalent": subject_sha == SHA_A,
    }


def test_valid_ready_implementation_state():
    assert validate_execution_state(_state()) == ()


def test_pending_external_is_lawful_with_one_tracked_owner():
    state = _state()
    state["phase"] = "VERIFY_REGRESSION"
    state["profile"] = "VERIFY_REGRESSION"
    state["claims"][0]["status"] = "IN_FLIGHT"
    state["claims"][0]["proof_owners"] = [_owner(status="IN_FLIGHT")]
    state["terminal"]["status"] = "PENDING_EXTERNAL"
    assert validate_execution_state(state) == ()


def test_duplicate_same_proposition_execution_is_rejected():
    state = _state()
    state["claims"][0]["status"] = "IN_FLIGHT"
    state["claims"][0]["proof_owners"] = [
        _owner("CI", status="IN_FLIGHT"),
        _owner("LOCAL", status="IN_FLIGHT"),
    ]
    errors = validate_execution_state(state)
    assert any("exceed required_proofs=1" in error for error in errors)


def test_explicit_independent_multiplicity_is_allowed():
    state = _state()
    claim = state["claims"][0]
    claim["type"] = "INDEPENDENT_AUDIT"
    claim["status"] = "PROVEN"
    claim["required_proofs"] = 2
    claim["proof_owners"] = [_owner("A"), _owner("B")]
    state["phase"] = "TERMINAL"
    state["profile"] = "TERMINAL"
    state["current_action"] = None
    state["terminal"]["status"] = "PASS"
    assert validate_execution_state(state) == ()


def test_worker_cannot_move_finish_line_without_authority():
    state = _state()
    state["terminal_definition_revision"] = 2
    errors = validate_execution_state(state)
    assert any("revision_authority_ref" in error for error in errors)


def test_profile_transition_requires_authority():
    state = _state()
    state["profile_transition_from"] = "REAL_EXECUTION"
    errors = validate_execution_state(state)
    assert any("profile_transition_authority_ref" in error for error in errors)


def test_evidence_tip_beyond_semantic_candidate_requires_tree_equivalence():
    state = _state()
    claim = state["claims"][0]
    claim["status"] = "PROVEN"
    claim["proof_owners"] = [{
        **_owner("CI", subject_sha=SHA_B),
        "relevant_tree_equivalent": False,
    }]
    state["phase"] = "CLOSURE_ONLY"
    state["profile"] = "CLOSURE_ONLY"
    state["current_action"] = {"advances_claim_id": None, "description": "write return"}
    errors = validate_execution_state(state)
    assert any("relevant_tree_equivalent=true" in error for error in errors)


def test_green_terminal_claims_force_closure_only():
    state = _state()
    state["claims"][0]["status"] = "PROVEN"
    state["claims"][0]["proof_owners"] = [_owner()]
    errors = validate_execution_state(state)
    assert any("phase must be CLOSURE_ONLY or TERMINAL" in error for error in errors)
    assert any("may not reopen an already PROVEN claim" in error for error in errors)


def test_blocker_requires_fresh_global_state():
    state = _state()
    state["claims"][0]["status"] = "BLOCKED"
    state["terminal"] = {
        "status": "BLOCKED",
        "blocker_class": "BLOCKED_INSUFFICIENT_EVIDENCE",
        "blocking_claim_ids": ["C1"],
    }
    errors = validate_execution_state(state)
    assert any("fresh_state.checked=true" in error for error in errors)


def test_blocker_cannot_ignore_still_active_proof_owner():
    state = _state()
    state["claims"][0]["status"] = "BLOCKED"
    state["claims"][0]["proof_owners"] = [_owner("CI", status="IN_FLIGHT")]
    state["fresh_state"] = {
        "checked": True,
        "branch_tip_sha": SHA_A,
        "observed_proof_owner_ids": ["CI"],
    }
    state["terminal"] = {
        "status": "BLOCKED",
        "blocker_class": "BLOCKED_INSUFFICIENT_EVIDENCE",
        "blocking_claim_ids": ["C1"],
    }
    errors = validate_execution_state(state)
    assert any("still has active proof owner CI" in error for error in errors)


def test_pass_requires_compatible_proof_and_terminal_phase():
    state = _state()
    state["claims"][0]["status"] = "PROVEN"
    state["claims"][0]["proof_owners"] = [_owner(compatible=False)]
    state["phase"] = "TERMINAL"
    state["profile"] = "TERMINAL"
    state["current_action"] = None
    state["terminal"]["status"] = "PASS"
    errors = validate_execution_state(state)
    assert any("PROVEN owner requires VERIFIED compatibility" in error for error in errors)
    assert any("claim is PROVEN but only 0 compatible proof owners" in error for error in errors)


def test_court_spec_accepts_only_bounded_pytest_surface():
    spec = {
        "schema_id": "RABOCHII_COURT_SPEC@1.0.0",
        "semantic_candidate_sha": SHA_A,
        "python_version": "3.12",
        "determinism_mode": "EXACT",
        "tests": [
            "rawlsing_next/tests/test_pre553_empirical_query.py",
            "rawlsing_next/tests/test_wave1_gt12_a2_real_gt1.py",
        ],
        "env": {
            "PYTHONHASHSEED": "0",
            "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        },
    }
    assert validate_court_spec(spec) == ()


def test_court_spec_rejects_shell_escape_and_arbitrary_env():
    spec = {
        "schema_id": "RABOCHII_COURT_SPEC@1.0.0",
        "semantic_candidate_sha": SHA_A,
        "python_version": "3.12",
        "determinism_mode": "EXACT",
        "tests": ["../../etc/passwd"],
        "env": {"PATH": "/tmp"},
    }
    errors = validate_court_spec(spec)
    assert any("safe relative path" in error for error in errors)
    assert any("rawlsing_next/tests/*.py" in error for error in errors)
    assert any("env key 'PATH' is not allowed" in error for error in errors)


def _real_execution_state():
    state = _state()
    state["profile"] = "REAL_EXECUTION"
    state["phase"] = "REAL_EXECUTION"
    state["current_action"] = {
        "kind": "EXECUTE_STAGE",
        "advances_claim_id": "C1",
        "description": "Execute the current bounded stage.",
    }
    state["checkpoint_state"] = {
        "mode": "WRITE_AHEAD",
        "last_completed_stage": "VALIDATE",
        "volatile_result_pending": False,
        "recompute_cost": "HIGH",
        "durable_checkpoint_ref": "git:checkpoint-before-execute",
    }
    return state


def test_real_execution_requires_write_ahead_checkpoint_state():
    state = _state()
    state["profile"] = "REAL_EXECUTION"
    state["phase"] = "REAL_EXECUTION"
    errors = validate_execution_state(state)
    assert any("REAL_EXECUTION requires checkpoint_state" in error for error in errors)


def test_real_execution_with_durable_checkpoint_can_continue():
    assert validate_execution_state(_real_execution_state()) == ()


def test_volatile_expensive_result_forces_persist_as_next_action():
    state = _real_execution_state()
    state["checkpoint_state"]["volatile_result_pending"] = True
    state["checkpoint_state"]["durable_checkpoint_ref"] = None
    errors = validate_execution_state(state)
    assert any("next legal action must be PERSIST_CHECKPOINT" in error for error in errors)


def test_volatile_result_is_valid_only_when_current_action_persists_it():
    state = _real_execution_state()
    state["checkpoint_state"]["volatile_result_pending"] = True
    state["checkpoint_state"]["durable_checkpoint_ref"] = None
    state["current_action"] = {
        "kind": "PERSIST_CHECKPOINT",
        "advances_claim_id": "C1",
        "description": "Persist the expensive result before further execution.",
    }
    assert validate_execution_state(state) == ()


def test_volatile_pending_cannot_claim_already_durable_checkpoint():
    state = _real_execution_state()
    state["checkpoint_state"]["volatile_result_pending"] = True
    errors = validate_execution_state(state)
    assert any("cannot coexist with durable_checkpoint_ref" in error for error in errors)
