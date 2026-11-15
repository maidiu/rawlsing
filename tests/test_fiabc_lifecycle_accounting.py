import unittest

from rawlsing_next.fiabc_lifecycle_accounting import (
    AccountingContractError,
    AccountingDisposition,
    ActionObservation,
    CallableLifecycleActionAdapter,
    CallableTelemetryAdapter,
    EvidenceKind,
    LifecycleAction,
    LifecycleActionRequest,
    LifecycleBinding,
    MetricState,
    PreservedCompatibilityProof,
    PreservedMetricEvidence,
    PreservedReceiptEvidence,
    ProcessIsolationReceipt,
    TelemetryMetric,
    WAVE2_PRESERVED_WORK_POLICIES,
    adjudicate_preserved_work,
    build_lits_a_preserved_receipt,
    build_lits_b_semantic_only_receipt,
    execute_lifecycle_action,
)


LITS_SHA = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"


def _binding(candidate="A", terminal="terminal-identity"):
    isolation = ProcessIsolationReceipt(
        source_id="LITS_I",
        candidate_id=candidate,
        process_token=f"proc-{candidate}",
        candidate_root_identity=f"root-{candidate}",
        fresh_process_for_cell=True,
        cross_candidate_state_reachable=False,
        isolation_contract_identity="i06a-contract",
    )
    return LifecycleBinding(
        source_id="LITS_I",
        source_sha256=LITS_SHA,
        candidate_id=candidate,
        candidate_owner_identity=f"owner-{candidate}",
        workload_id="lock1-lock2-workload",
        authority_set_identity="authority-set",
        runtime_binding_identity="runtime-binding",
        state_scope_identity=f"state-scope-{candidate}",
        expected_terminal_identity=terminal,
        isolation=isolation,
    )


def _request(action, *, candidate="A", metrics=(), operation="governed-op"):
    return LifecycleActionRequest(
        binding=_binding(candidate=candidate),
        action=action,
        governed_operation_id=operation,
        expected_metric_names=tuple(metrics),
    )


def _observation(request, **overrides):
    base = dict(
        action=request.action,
        binding_id=request.binding.binding_id,
        source_id=request.binding.source_id,
        candidate_id=request.binding.candidate_id,
        performed=True,
        evidence_kind=EvidenceKind.EXECUTED_CANDIDATE_ACTION,
        action_id="action-1",
        state_before_id="state-before",
        state_after_id="state-after",
        terminal_identity=request.binding.expected_terminal_identity,
        candidate_state_object_ids_before=("candidate-state-1",),
        candidate_state_object_ids_after=("candidate-state-1",),
        evidence_refs=("evidence-ref",),
    )
    base.update(overrides)
    return ActionObservation(**base)


def _telemetry(request, observation, *pairs):
    return tuple(
        TelemetryMetric(
            name=name,
            state=MetricState.MEASURED,
            value=value,
            unit=unit,
            action_id=observation.action_id,
            binding_id=request.binding.binding_id,
        )
        for name, value, unit in pairs
    )


class LifecycleHostileTests(unittest.TestCase):
    def test_formula_assigned_recomputation_units_cannot_pass(self):
        request = _request(
            LifecycleAction.SOURCE_INVALIDATION,
            metrics=("source_release_invalidation_recomputation_units",),
        )
        observation = _observation(
            request,
            evidence_kind=EvidenceKind.FORMULA_DERIVED,
            invalidation_trigger_identity="source-release-2",
            invalidated_unit_ids=("u1",),
            recomputed_unit_ids=("u1", "u2"),
        )
        action = CallableLifecycleActionAdapter(lambda _r: observation)
        telemetry = CallableTelemetryAdapter(
            lambda r, o: _telemetry(
                r,
                o,
                ("source_release_invalidation_recomputation_units", 2, "units"),
            )
        )
        with self.assertRaises(AccountingContractError):
            execute_lifecycle_action(request, action, telemetry)

    def test_executed_invalidation_rejects_formula_like_count_not_matching_observed_units(self):
        request = _request(
            LifecycleAction.SOURCE_INVALIDATION,
            metrics=("source_release_invalidation_recomputation_units",),
        )
        observation = _observation(
            request,
            invalidation_trigger_identity="source-release-2",
            invalidated_unit_ids=("u1", "u2"),
            recomputed_unit_ids=("u1", "u2"),
        )
        action = CallableLifecycleActionAdapter(lambda _r: observation)
        telemetry = CallableTelemetryAdapter(
            lambda r, o: _telemetry(
                r,
                o,
                ("source_release_invalidation_recomputation_units", 3, "units"),
            )
        )
        with self.assertRaises(AccountingContractError):
            execute_lifecycle_action(request, action, telemetry)

    def test_lifecycle_metric_name_cannot_attach_to_wrong_action(self):
        request = _request(
            LifecycleAction.STALE_STATE_RECOVERY,
            metrics=("delete_rebuild_wall_ns",),
        )
        with self.assertRaises(AccountingContractError):
            request.validate()

    def test_law_hash_cannot_pass_stale_or_corrupt_exercise(self):
        for lifecycle_action in (
            LifecycleAction.STALE_STATE_RECOVERY,
            LifecycleAction.CORRUPT_STATE_RECOVERY,
        ):
            with self.subTest(lifecycle_action=lifecycle_action):
                request = _request(lifecycle_action)
                if lifecycle_action is LifecycleAction.STALE_STATE_RECOVERY:
                    observation = _observation(
                        request,
                        evidence_kind=EvidenceKind.LAW_HASH_ONLY,
                        stale_determinant_before="d1",
                        stale_determinant_after="d2",
                        stale_detected=True,
                        recovery_performed=True,
                    )
                else:
                    observation = _observation(
                        request,
                        evidence_kind=EvidenceKind.LAW_HASH_ONLY,
                        corrupt_target_id="candidate-state-1",
                        corruption_injected=True,
                        corrupt_detected=True,
                        recovery_performed=True,
                    )
                action = CallableLifecycleActionAdapter(lambda _r, o=observation: o)
                telemetry = CallableTelemetryAdapter(lambda _r, _o: ())
                with self.assertRaises(AccountingContractError):
                    execute_lifecycle_action(request, action, telemetry)

    def test_generic_temporary_file_cannot_pass_interruption_recovery(self):
        request = _request(
            LifecycleAction.INTERRUPTION_RECOVERY,
            operation="real-candidate-build",
        )
        observation = _observation(
            request,
            evidence_kind=EvidenceKind.GENERIC_TEMP_FILE,
            interrupted_operation_id="real-candidate-build",
            interrupted_candidate_state_id="candidate-state-1",
            interruption_injected=True,
            recovered_operation_id="real-candidate-build",
            recovery_performed=True,
        )
        action = CallableLifecycleActionAdapter(lambda _r: observation)
        telemetry = CallableTelemetryAdapter(lambda _r, _o: ())
        with self.assertRaises(AccountingContractError):
            execute_lifecycle_action(request, action, telemetry)

    def test_rebuild_receipt_without_actual_deletion_and_regeneration_fails(self):
        request = _request(
            LifecycleAction.DELETION_REGENERATION,
            metrics=("delete_rebuild_wall_ns",),
        )
        observation = _observation(
            request,
            deleted_object_ids=(),
            regenerated_object_ids=(),
            regeneration_lineage=(),
        )
        action = CallableLifecycleActionAdapter(lambda _r: observation)
        telemetry = CallableTelemetryAdapter(
            lambda r, o: _telemetry(r, o, ("delete_rebuild_wall_ns", 50, "ns"))
        )
        with self.assertRaises(AccountingContractError):
            execute_lifecycle_action(request, action, telemetry)

    def test_warm_run_without_valid_retained_candidate_owned_state_fails(self):
        request = _request(
            LifecycleAction.WARM_RETAINED_STATE_USE,
            metrics=("warm_retained_state_bytes",),
        )
        observation = _observation(
            request,
            retained_state_id="not-present",
            retained_state_candidate_id="A",
        )
        action = CallableLifecycleActionAdapter(lambda _r: observation)
        telemetry = CallableTelemetryAdapter(
            lambda r, o: _telemetry(
                r, o, ("warm_retained_state_bytes", 100, "bytes")
            )
        )
        with self.assertRaises(AccountingContractError):
            execute_lifecycle_action(request, action, telemetry)

    def test_preserved_telemetry_with_incompatible_state_binding_gets_no_numeric_credit(self):
        request = _request(
            LifecycleAction.COLD_FIRST_REALIZATION,
            metrics=("build_or_open_wall_ns",),
        )
        preserved = build_lits_a_preserved_receipt(
            source_sha256=LITS_SHA,
            semantic_identity="semantic",
            terminal_identity=request.binding.expected_terminal_identity,
            telemetry={"wall_ns": 123},
        )
        proof = PreservedCompatibilityProof(
            preserved_receipt_ref=preserved.receipt_ref,
            current_binding_id=request.binding.binding_id,
            workload_compatible=True,
            runtime_binding_compatible=True,
            state_binding_compatible=False,
            isolation_compatible=True,
            operation_compatible=True,
            metric_definition_matches=frozenset({"build_or_open_wall_ns"}),
            proof_refs=("proof",),
        )
        result = adjudicate_preserved_work(
            request=request,
            preserved=preserved,
            compatibility=proof,
        )
        self.assertEqual(
            result.disposition,
            AccountingDisposition.PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY,
        )
        self.assertIsNone(result.metrics[0].value)
        self.assertEqual(
            result.metrics[0].state,
            MetricState.MEASUREMENT_NOT_CAPTURED,
        )

    def test_missing_preserved_telemetry_remains_null_not_zero(self):
        request = _request(
            LifecycleAction.COLD_FIRST_REALIZATION,
            candidate="B",
            metrics=("build_or_open_wall_ns",),
        )
        preserved = build_lits_b_semantic_only_receipt(
            source_sha256=LITS_SHA,
            semantic_identity="c11-semantic",
        )
        result = adjudicate_preserved_work(
            request=request,
            preserved=preserved,
            compatibility=None,
        )
        self.assertEqual(
            result.disposition,
            AccountingDisposition.PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY,
        )
        self.assertIsNone(result.metrics[0].value)
        self.assertNotEqual(result.metrics[0].value, 0)

    def test_unreached_lifecycle_stage_cannot_emit_numeric_metric(self):
        request = _request(
            LifecycleAction.COLD_FIRST_REALIZATION,
            metrics=("build_or_open_wall_ns",),
        )
        preserved = PreservedReceiptEvidence(
            work_id="P009",
            receipt_ref=WAVE2_PRESERVED_WORK_POLICIES["P009"].evidence_ref,
            source_id="LITS_I",
            source_sha256=LITS_SHA,
            candidate_id="A",
            operation=LifecycleAction.COLD_FIRST_REALIZATION,
            semantic_identity="stop-evidence",
            terminal_identity=None,
            stage_reached=False,
            metrics=(
                PreservedMetricEvidence(
                    canonical_name="build_or_open_wall_ns",
                    unit="ns",
                    value=1,
                    historical_field="invented",
                    directly_observed=True,
                ),
            ),
        )
        with self.assertRaises(AccountingContractError):
            adjudicate_preserved_work(
                request=request,
                preserved=preserved,
                compatibility=None,
            )

    def test_candidate_a_preserved_work_cannot_satisfy_candidate_b_obligation(self):
        request = _request(
            LifecycleAction.COLD_FIRST_REALIZATION,
            candidate="B",
            metrics=("build_or_open_wall_ns",),
        )
        preserved = build_lits_a_preserved_receipt(
            source_sha256=LITS_SHA,
            semantic_identity="semantic",
            terminal_identity=request.binding.expected_terminal_identity,
            telemetry={"wall_ns": 123},
        )
        with self.assertRaises(AccountingContractError):
            adjudicate_preserved_work(
                request=request,
                preserved=preserved,
                compatibility=None,
            )

    def test_successful_fresh_process_replay_reproduces_governed_terminal_identity(self):
        request = _request(
            LifecycleAction.FRESH_PROCESS_REPLAY,
            metrics=("fresh_process_replay_wall_ns",),
            operation="fresh-replay",
        )
        observation = _observation(
            request,
            parent_process_token="parent-proc",
            replay_process_token="new-proc",
        )
        action = CallableLifecycleActionAdapter(lambda _r: observation)
        telemetry = CallableTelemetryAdapter(
            lambda r, o: _telemetry(
                r, o, ("fresh_process_replay_wall_ns", 777, "ns")
            )
        )
        receipt = execute_lifecycle_action(request, action, telemetry)
        self.assertEqual(receipt.disposition, AccountingDisposition.EXECUTED_NOW)
        self.assertEqual(
            receipt.terminal_identity,
            request.binding.expected_terminal_identity,
        )
        self.assertEqual(receipt.metrics[0].value, 777)

    def test_fresh_replay_wrong_terminal_identity_fails(self):
        request = _request(
            LifecycleAction.FRESH_PROCESS_REPLAY,
            metrics=("fresh_process_replay_wall_ns",),
            operation="fresh-replay",
        )
        observation = _observation(
            request,
            terminal_identity="wrong-terminal",
            parent_process_token="parent-proc",
            replay_process_token="new-proc",
        )
        action = CallableLifecycleActionAdapter(lambda _r: observation)
        telemetry = CallableTelemetryAdapter(
            lambda r, o: _telemetry(
                r, o, ("fresh_process_replay_wall_ns", 777, "ns")
            )
        )
        with self.assertRaises(AccountingContractError):
            execute_lifecycle_action(request, action, telemetry)


if __name__ == "__main__":
    unittest.main()
