# Test results

```sh
# From the assigned worktree:
git archive 895980397cc0533043c7ca0e493ebbb455666c1e rawlsing_next WORKER_RETURNS/PYAT-HQ281-C02J-REAL-B5-M2-PRODUCER-TRUST-R1 | tar -x -C /tmp/p02r-c02j-pinned
cd /tmp/p02r-c02j-pinned
PYTHONPATH=/tmp/p02r-c02j-pinned python3 -m pytest -q rawlsing_next/tests/test_pre553_learned_product_lifecycle.py rawlsing_next/tests/test_pre553_learned_product_release.py rawlsing_next/tests/test_pre553_empirical_objects_authority.py
PYTHONPATH=/tmp/p02r-c02j-pinned python3 -m rawlsing_next.repro.c02j_owner_court
PYTHONPATH=/tmp/p02r-c02j-pinned python3 /Users/matthewsmith/.codex/worktrees/p02r-c02j/Rawlsing/WORKER_RETURNS/PYAT-HQ282-P02R-C02J-INDEPENDENT-INTERFACE-VERIFICATION-R1/repro/review.py
```

Owner suite exit 0: 83 passed in 0.54s. Baseline court exit 0. Final independent review exit 1: 41 PASS, 14 FAIL, 0 SKIP, 3 UNTESTED. The nonzero exit preserves failed requirements. `run.py` provides a portable fresh-archive reproduction command; it was added as a convenience and was not itself executed in this review. `owners.txt` transcribes captured terminal output; the JSONL files are redirected process output.

One initial baseline launch failed before Python started because its output directory was absent (shell exit 1). It was corrected and executed successfully. The first independent run misclassified incomplete replay during fixture setup; that case was repaired to mutate complete replay material after custody construction and then test publication. Intermediate logs were replaced by the final run. The final shell invocation was run alone to confirm exit 1.

PASS denotes the explicit requirement in each case name. FAIL denotes accepted invalid behavior or rejected valid behavior, not a test-runner crash. Coordinated-replacement and self-declaration failures demonstrate absent external authority checks already acknowledged by the candidate. Historical-checkpoint failure describes an interface inconsistency; no time-scoped revocation policy is implemented. Any exception counts as rejection in basic negative probes; exact exception classes and messages are retained so unrelated refusal mechanisms remain visible.

| Independent case | Result | Actual behavior / reason |
|---|---|---|
| `raw_normal_publication` | PASS | {"publication": "PUBLISHED"} |
| `overlay_normal_non_authorizing` | PASS | {"authorizing": false, "current": false, "published": true, "registered": true} |
| `reject_expected_release_key` | PASS | {"error": "VerifierAuthenticationError", "reason": "constructed B5 subject does not authenticate against non-mutable owner-held material for slot 'R'; mismatched fields: release_key", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `reject_expected_release_content_hash` | PASS | {"error": "VerifierAuthenticationError", "reason": "constructed B5 subject does not authenticate against non-mutable owner-held material for slot 'R'; mismatched fields: release_content_hash", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `reject_expected_producer_subject_key` | PASS | {"error": "VerifierAuthenticationError", "reason": "constructed B5 subject does not authenticate against non-mutable owner-held material for slot 'R'; mismatched fields: producer_subject_key", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `reject_expected_product_key` | PASS | {"error": "VerifierAuthenticationError", "reason": "constructed B5 subject does not authenticate against non-mutable owner-held material for slot 'R'; mismatched fields: product_key", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `reject_expected_selection_scope_key` | PASS | {"error": "VerifierAuthenticationError", "reason": "constructed B5 subject does not authenticate against non-mutable owner-held material for slot 'R'; mismatched fields: selection_scope_key", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `reject_expected_authority_snapshot_keys` | PASS | {"error": "VerifierAuthenticationError", "reason": "constructed B5 subject does not authenticate against non-mutable owner-held material for slot 'R'; mismatched fields: authority_snapshot_keys", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `reject_expected_permission_ceiling_key` | PASS | {"error": "VerifierAuthenticationError", "reason": "constructed B5 subject does not authenticate against non-mutable owner-held material for slot 'R'; mismatched fields: permission_ceiling_key", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `reject_expected_receipt_keys` | PASS | {"error": "VerifierAuthenticationError", "reason": "constructed B5 subject does not authenticate against non-mutable owner-held material for slot 'R'; mismatched fields: receipt_keys", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `reject_presented_release_ref` | PASS | {"error": "VerifierUnknownReleaseError", "reason": "release Other / urn:c02j:other:release_ref:sha256:879856f8ebfc6630eb443126281d1ac1156de4616a4299aa407fc3b8acea457f / 879856f8ebfc6630eb443126281d1ac1156de4616a4299aa407fc3b8acea457f is not registered with any verifier; direct unmediated publication is refused", "refusal_class": "UNKNOWN_RELEASE", "rejected": true} |
| `reject_presented_product_ref` | PASS | {"error": "VerifierAuthenticationError", "reason": "presented subject fields do not match the frozen owner-held expectation for slot 'R'; mismatched fields: product_key", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `reject_presented_producer_permission_ceiling_ref` | PASS | {"error": "VerifierAuthenticationError", "reason": "presented subject fields do not match the frozen owner-held expectation for slot 'R'; mismatched fields: permission_ceiling_key", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `reject_presented_authority_snapshot_refs` | PASS | {"error": "VerifierAuthenticationError", "reason": "presented subject fields do not match the frozen owner-held expectation for slot 'R'; mismatched fields: authority_snapshot_keys", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `reject_presented_build_or_release_receipt_refs` | PASS | {"error": "VerifierAuthenticationError", "reason": "presented subject fields do not match the frozen owner-held expectation for slot 'R'; mismatched fields: receipt_keys", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `separate_prior_expectation_rejects_replacement` | PASS | {"error": "VerifierAuthenticationError", "expectation_replaced": false, "reason": "constructed B5 subject does not authenticate against non-mutable owner-held material for slot 'R'; mismatched fields: direct_dependency_keys, m2_release_projection_hash, producer_contract_key, producer_subject_key, release_content_hash, release_key, replay_closure_key, replay_root_key, semantic_anatomy_key, semantic_projection_hash", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true} |
| `independent_authority_required_for_coordinated_replacement` | FAIL | {"expectation_replaced": true, "rejected": false} |
| `independent_permission_required_for_matching_self_declaration` | FAIL | {"rejected": false} |
| `alias_mutation_rejected_after_freeze` | PASS | {"error": "VerifierAuthenticationError", "reason": "constructed B5 subject does not authenticate against non-mutable owner-held material for slot 'R'; mismatched fields: determinant_keys, determinant_set_hash", "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "rejected": true, "same_repository": true} |
| `raw_reject_unapproved_event_refs` | FAIL | {"events": 3, "rejected": false} |
| `overlay_reject_unapproved_event_refs` | FAIL | {"events": 3, "rejected": false} |
| `raw_restore_valid_published` | PASS | {"current_saved": false, "modification": null, "rejected": false} |
| `raw_restore_valid_current` | PASS | {"current_saved": true, "modification": null, "rejected": false} |
| `raw_reject_checkpoint_truncated` | FAIL | {"current_saved": false, "modification": "truncated", "rejected": false} |
| `raw_reject_checkpoint_incomplete` | PASS | {"current_saved": false, "error": "LearnedProductLifecycleConflict", "modification": "incomplete", "reason": "checkpoint publication does not cover exact registered set", "refusal_class": null, "rejected": true} |
| `raw_reject_checkpoint_altered_state` | FAIL | {"current_saved": false, "modification": "altered_state", "rejected": false} |
| `raw_reject_checkpoint_bad_hash` | PASS | {"current_saved": false, "error": "LearnedProductLifecycleConflict", "modification": "bad_hash", "reason": "lifecycle checkpoint hash mismatch", "refusal_class": null, "rejected": true} |
| `overlay_restore_valid_published` | FAIL | {"current_saved": false, "error": "VerifierCheckpointError", "modification": null, "reason": "checkpoint subject release is absent from the held M2 repository: RELEASE_SUBJECT_NOT_FOUND: exact producer subject is not registered", "refusal_class": "CHECKPOINT_UNRESOLVED", "rejected": true} |
| `overlay_restore_valid_current` | FAIL | {"current_saved": true, "error": "VerifierCheckpointError", "modification": null, "reason": "checkpoint subject release is absent from the held M2 repository: RELEASE_SUBJECT_NOT_FOUND: exact producer subject is not registered", "refusal_class": "CHECKPOINT_UNRESOLVED", "rejected": true} |
| `overlay_reject_checkpoint_truncated` | PASS | {"current_saved": false, "error": "VerifierCheckpointError", "modification": "truncated", "reason": "checkpoint subject release is absent from the held M2 repository: RELEASE_SUBJECT_NOT_FOUND: exact producer subject is not registered", "refusal_class": "CHECKPOINT_UNRESOLVED", "rejected": true} |
| `overlay_reject_checkpoint_incomplete` | PASS | {"current_saved": false, "error": "LearnedProductLifecycleConflict", "modification": "incomplete", "reason": "checkpoint publication does not cover exact registered set", "refusal_class": null, "rejected": true} |
| `overlay_reject_checkpoint_altered_state` | PASS | {"current_saved": false, "error": "VerifierCheckpointError", "modification": "altered_state", "reason": "checkpoint subject release is absent from the held M2 repository: RELEASE_SUBJECT_NOT_FOUND: exact producer subject is not registered", "refusal_class": "CHECKPOINT_UNRESOLVED", "rejected": true} |
| `overlay_reject_checkpoint_bad_hash` | PASS | {"current_saved": false, "error": "LearnedProductLifecycleConflict", "modification": "bad_hash", "reason": "lifecycle checkpoint hash mismatch", "refusal_class": null, "rejected": true} |
| `reject_revoked_release` | PASS | {"error": "VerifierRevocationError", "reason": "release urn:rawlsing:pre553:m2:release:sha256:a4bc97e5c5a541d4fbeeba5381f9ad4af9a8844572953b460a6fa01de5bd3a7a is revoked for this verifier; publication is refused before B5", "refusal_class": "AUTHORITY_REVOKED", "rejected": true} |
| `reject_revoked_authority` | PASS | {"error": "VerifierRevocationError", "reason": "semantic authority ref(s) AUTH-c02j-semantic are revoked; publication is refused before B5", "refusal_class": "AUTHORITY_REVOKED", "rejected": true} |
| `reject_revoked_consumed` | PASS | {"error": "VerifierRevocationError", "reason": "consumed model/walkback authority ref(s) urn:c02j:modelauthority:c02j-model:sha256:775219c95551c6ded650ba7ea95e0c86019130516dccd01167ea3c17020229ed are revoked; publication is refused before B5", "refusal_class": "AUTHORITY_REVOKED", "rejected": true} |
| `reject_revoked_replay` | PASS | {"error": "VerifierRevocationError", "reason": "M2 replay reconstruction closure urn:rawlsing:pre553:m2:closure:replay_reconstruction:sha256:d0f8c76467867f5b918d673afb4b1632bf31557194187f64e9c2c3b65f8b7c8e is revoked; publication is refused before B5", "refusal_class": "AUTHORITY_REVOKED", "rejected": true} |
| `reject_obsolete_replay_grade` | PASS | {"error": "VerifierReplayError", "reason": "M2 replay reconstruction closure urn:rawlsing:pre553:m2:closure:replay_reconstruction:sha256:793f98cd8d7add18a2ea5803c8bbd5d352ced9cd77908990990b63462e62d078 declares grade 'HISTORICAL_EXPLANATION_ONLY' but slot 'R' requires 'EXACT_DETERMINISTIC_REBUILD'", "refusal_class": "REPLAY_CLOSURE_REFUSED", "rejected": true} |
| `reject_incomplete_replay` | PASS | {"error": "VerifierReplayError", "reason": "M2 replay reconstruction closure urn:rawlsing:pre553:m2:closure:replay_reconstruction:sha256:d0f8c76467867f5b918d673afb4b1632bf31557194187f64e9c2c3b65f8b7c8e is explicitly incomplete", "refusal_class": "REPLAY_CLOSURE_REFUSED", "rejected": true} |
| `recertification_checks_revocation` | FAIL | {"rejected": false} |
| `withdrawn_release_not_selectable` | PASS | {"error": "LearnedProductLifecycleError", "reason": "invalidated/withdrawn product cannot be selected current", "refusal_class": null, "rejected": true} |
| `no_current_requires_registered_verifier` | FAIL | {"rejected": false} |
| `withdrawal_requires_registered_verifier` | FAIL | {"rejected": false} |
| `m2_restrict_low_level_foreign` | FAIL | {"rejected": false} |
| `m2_restrict_new_subject_held_repo` | FAIL | {"rejected": false} |
| `stable_concurrent_facade_calls` | PASS | {"all_non_authorizing": true, "count": 8, "same_event_identity": true} |
| `raw_historical_event` | PASS | {"current": "NO_CURRENT", "historical": "CURRENT_SELECTED", "rejected": false} |
| `raw_historical_checkpoint` | PASS | {"current": "NO_CURRENT", "historical": "CURRENT_SELECTED", "rejected": false} |
| `overlay_historical_event` | PASS | {"current": "NO_CURRENT", "historical": "CURRENT_SELECTED", "rejected": false} |
| `overlay_historical_checkpoint` | FAIL | {"error": "VerifierRevocationError", "reason": "release urn:rawlsing:pre553:m2:release:sha256:a4bc97e5c5a541d4fbeeba5381f9ad4af9a8844572953b460a6fa01de5bd3a7a is revoked for this verifier; publication is refused before B5", "rejected": true} |
| `unknown_registry_stage_protocol` | PASS | {"error": "VerifierUnknownReleaseError", "reason": "release LearnedProductReleaseCore / urn:rawlsing:pre553:m2:release:sha256:a4bc97e5c5a541d4fbeeba5381f9ad4af9a8844572953b460a6fa01de5bd3a7a / a4bc97e5c5a541d4fbeeba5381f9ad4af9a8844572953b460a6fa01de5bd3a7a is not registered with any verifier; direct unmediated publication is refused", "refusal_class": "UNKNOWN_RELEASE", "rejected": true} |
| `unknown_registry_register_product` | PASS | {"error": "VerifierUnknownReleaseError", "reason": "release LearnedProductReleaseCore / urn:rawlsing:pre553:m2:release:sha256:a4bc97e5c5a541d4fbeeba5381f9ad4af9a8844572953b460a6fa01de5bd3a7a / a4bc97e5c5a541d4fbeeba5381f9ad4af9a8844572953b460a6fa01de5bd3a7a is not registered with any verifier; direct unmediated publication is refused", "refusal_class": "UNKNOWN_RELEASE", "rejected": true} |
| `unknown_registry_publish_product` | PASS | {"error": "VerifierUnknownReleaseError", "reason": "release LearnedProductReleaseCore / urn:rawlsing:pre553:m2:release:sha256:a4bc97e5c5a541d4fbeeba5381f9ad4af9a8844572953b460a6fa01de5bd3a7a / a4bc97e5c5a541d4fbeeba5381f9ad4af9a8844572953b460a6fa01de5bd3a7a is not registered with any verifier; direct unmediated publication is refused", "refusal_class": "UNKNOWN_RELEASE", "rejected": true} |
| `unknown_registry_select_current` | PASS | {"error": "VerifierUnknownReleaseError", "reason": "release LearnedProductReleaseCore / urn:rawlsing:pre553:m2:release:sha256:a4bc97e5c5a541d4fbeeba5381f9ad4af9a8844572953b460a6fa01de5bd3a7a / a4bc97e5c5a541d4fbeeba5381f9ad4af9a8844572953b460a6fa01de5bd3a7a is not registered with any verifier; direct unmediated publication is refused", "refusal_class": "UNKNOWN_RELEASE", "rejected": true} |
| `unknown_registry_record_recertification` | PASS | {"error": "VerifierUnknownReleaseError", "reason": "release LearnedProductReleaseCore / urn:rawlsing:pre553:m2:release:sha256:a4bc97e5c5a541d4fbeeba5381f9ad4af9a8844572953b460a6fa01de5bd3a7a / a4bc97e5c5a541d4fbeeba5381f9ad4af9a8844572953b460a6fa01de5bd3a7a is not registered with any verifier; direct unmediated publication is refused", "refusal_class": "UNKNOWN_RELEASE", "rejected": true} |
| `expiration_clock` | UNTESTED | "No expiry timestamp or clock gate in the candidate; not implemented." |
| `concurrent_repository_mutation` | UNTESTED | "Not exercised; no synchronization demonstrated by stable concurrent reads." |
| `live_independent_issuers` | UNTESTED | "No independent expectation, permission or revocation issuer available in this source-free scope." |

## Existing court observations

The original script increments total_cases for metadata as well as behavioral rows, has no general assertion over its emitted refusal booleans, and its no-root record is descriptive. The following is reproduced output, not a claim that every named property was independently asserted. Of its 24 pre-completion records, 5 are controls (start, two phases, construction notice, patch-removal notice), leaving 19 behavioral/descriptive observations. The checkpoint negative results are affected by the valid-restoration defect.

| Emitted case | Observed fields |
|---|---|
| `COURT_START` | {"phases": 2} |
| `PHASE` | {"phase": "UNPATCHED"} |
| `UNPATCHED_B1_raw_publishes` | {"publication": "PUBLISHED"} |
| `UNPATCHED_B2_forgery_publishes` | {"ceiling_is_forged": true} |
| `UNPATCHED_B3_current_selected` | {"current_events": ["CURRENT_SELECTED"]} |
| `UNPATCHED_H_checkpoint_self_hash` | {"current_present": true, "rehydrated": true} |
| `UNPATCHED_D1_minted_release` | {"release_key": "urn:rawlsing:pre553:m2:release:sha256:9bb149bfe9644151ce1be6e2bb09c47198f9bfc5eaf5e210385ad6606a0c627a"} |
| `PHASE` | {"phase": "PATCHED"} |
| `PATCHED_direct_stage_unknown` | {"refusal_class": "UNKNOWN_RELEASE", "refused": true} |
| `PATCHED_registered_forged_ceiling` | {"mismatched": ["permission_ceiling_key", "receipt_keys", "replay_root_key"], "refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "refused": true} |
| `PATCHED_no_credential_surface` | {"has_credential_field": false, "request_fields": ["slot"]} |
| `PATCHED_no_root_to_swap` | {"repo_is_request_addressable": false, "verifier_holds_repo_object": true} |
| `PATCHED_self_made_expectation_publish` | {"refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "refused": true} |
| `PATCHED_self_made_expectation_constructed` | {"constructed": true} |
| `PATCHED_self_made_event_refs` | {"event_attribution_unproved": true, "subject_still_held_authenticated": true} |
| `PATCHED_revoked_release` | {"refusal_class": "AUTHORITY_REVOKED", "refused": true} |
| `PATCHED_fake_permission` | {"refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "refused": true} |
| `PATCHED_fake_checkpoint_hash` | {"refusal_class": "CHECKPOINT_UNRESOLVED", "refused": true} |
| `PATCHED_legitimate_positive` | {"authorizing": false, "current_selection_performed": false, "publication": "PUBLISHED"} |
| `PATCHED_foreign_m2_registration` | {"refusal_class": "UNREGISTERED_REPOSITORY", "refused": true} |
| `PATCHED_mutated_repo_publish` | {"refusal_class": "IDENTITY_AUTHENTICATION_FAILED", "refused": true} |
| `PATCHED_stale_replay_grade` | {"refusal_class": "REPLAY_CLOSURE_REFUSED", "refused": true} |
| `PATCHED_truncated_replay` | {"error": "VerifierCheckpointError", "refusal_class": "CHECKPOINT_UNRESOLVED", "refused": true} |
| `PATCH_REMOVED` | {"patch_active": false} |
| `COURT_COMPLETE` | {"total_cases": 24} |
